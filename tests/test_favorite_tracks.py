"""Favorite writes are explicit, account-bound and leave downloads untouched."""
from types import SimpleNamespace
from unittest.mock import Mock
from PySide6.QtCore import QCoreApplication, QObject
from bitwave.bitwave_ui.bridge_favorites import FavoriteTracksMixin


class Bridge(FavoriteTracksMixin, QObject):
    pass


class Pool:
    def __init__(self): self.jobs = []
    def start(self, job): self.jobs.append(job)
    def finish(self):
        self.jobs.pop(0).run()
        QCoreApplication.processEvents()


def bridge(ok=True):
    app = QCoreApplication.instance() or QCoreApplication([])
    b = Bridge()
    b._init_favorite_tracks()
    b._favorite_tracks_pool = Pool()
    b._logged_in = True
    b._factory_reset = False
    b._browse_gen = 7
    b.tidal = SimpleNamespace(session=SimpleNamespace(user=SimpleNamespace(favorites=SimpleNamespace(remove_track=Mock(return_value=ok)))))
    b._lib_cache = {"tracks": {"items": [{"id": str(i)} for i in range(50)], "offset": 50, "more": True}}
    b._lib_reval_ts = {"tracks": 99}
    b._lib_loading = {"tracks"}
    b._fav_ids = {"tracks": (1, {"1", "2"}), "albums": (1, {"9"})}
    b._home_cache = [{"target": "tracks", "items": [{"id": "1"}, {"id": "2"}]}]
    b._save_page_cache = Mock()
    b._set_status = Mock()
    b._queue = [{"media_id": "1", "status": "done"}]
    b._test_app = app
    return b


def test_success_removes_only_favorite_and_adjusts_paging(tmp_path):
    b = bridge()
    downloaded = tmp_path / "track.flac"
    downloaded.write_bytes(b"audio")
    removed = []
    b.favoriteTrackRemoved.connect(removed.append)
    b.removeFavoriteTrack("1")
    assert len(b._lib_cache["tracks"]["items"]) == 50  # no optimistic removal
    b._favorite_tracks_pool.finish()
    b.tidal.session.user.favorites.remove_track.assert_called_once_with("1")
    assert removed == ["1"]
    assert b._lib_cache["tracks"]["offset"] == 49
    assert len(b._lib_cache["tracks"]["items"]) == 49
    assert b._lib_cache["tracks"]["more"] is True
    assert b._home_cache[0]["items"] == [{"id": "2"}]
    assert "tracks" not in b._fav_ids and "albums" in b._fav_ids
    assert b._favorite_tracks_epoch == 1
    assert b._queue == [{"media_id": "1", "status": "done"}]
    assert downloaded.read_bytes() == b"audio"
    b._save_page_cache.assert_called_once()


def test_failed_write_keeps_the_track_and_all_caches():
    b = bridge(False)
    b.removeFavoriteTrack("1")
    b._favorite_tracks_pool.finish()
    assert len(b._lib_cache["tracks"]["items"]) == 50
    assert b._favorite_tracks_epoch == 0
    assert "tracks" in b._fav_ids
    b._save_page_cache.assert_not_called()
    assert not b._favorite_track_pending


def test_duplicate_click_does_not_send_duplicate_writes():
    b = bridge()
    b.removeFavoriteTrack("1")
    b.removeFavoriteTrack("1")
    assert len(b._favorite_tracks_pool.jobs) == 1
    b._favorite_tracks_pool.finish()


def test_queued_write_never_uses_a_new_account():
    b = bridge()
    original = b.tidal.session.user.favorites.remove_track
    b.removeFavoriteTrack("1")
    b._browse_gen += 1
    b.tidal.session = SimpleNamespace(user=SimpleNamespace(favorites=SimpleNamespace(remove_track=Mock())))
    b._favorite_tracks_pool.finish()
    original.assert_not_called()
    b.tidal.session.user.favorites.remove_track.assert_not_called()
    assert len(b._lib_cache["tracks"]["items"]) == 50


def test_result_after_logout_is_ignored():
    b = bridge()
    def logout_on_response(_):
        b._logged_in = False
        b._browse_gen += 1
        return True
    b.tidal.session.user.favorites.remove_track.side_effect = logout_on_response
    b.removeFavoriteTrack("1")
    b._favorite_tracks_pool.finish()
    assert len(b._lib_cache["tracks"]["items"]) == 50
    b._save_page_cache.assert_not_called()


def test_request_exception_releases_busy_and_allows_retry():
    b = bridge()
    b.tidal.session.user.favorites.remove_track.side_effect = RuntimeError("offline")
    b.removeFavoriteTrack("1")
    b._favorite_tracks_pool.finish()
    assert not b._favorite_track_pending
    assert len(b._lib_cache["tracks"]["items"]) == 50
    b.removeFavoriteTrack("1")
    assert len(b._favorite_tracks_pool.jobs) == 1


def test_invalid_or_signed_out_request_never_calls_tidal():
    b = bridge()
    for value in ("", "-1", "1/2", "abc", "１２"):
        b.removeFavoriteTrack(value)
    b._logged_in = False
    b.removeFavoriteTrack("1")
    assert not b._favorite_tracks_pool.jobs


def test_read_started_before_removal_cannot_append_stale_rows():
    from bitwave.bitwave_ui.backend import BitWaveBridge
    b = bridge()
    b._lib_gen = 1
    b._lib_sort = {}
    b._lib_loading.clear()
    b.threadpool = Pool()
    b.libraryMore = Mock()
    b._lib_count = lambda cat, rows: len(rows)
    b._dress_library_rows = lambda cat, rows: rows
    b._lib_status = lambda *args: "loaded"
    b._library_page = lambda *args: ([{"id": "stale"}], True)
    BitWaveBridge.loadMoreLibrary(b, "tracks")
    b.removeFavoriteTrack("1")
    b._favorite_tracks_pool.finish()
    b.threadpool.finish()
    b.libraryMore.emit.assert_not_called()
    assert len(b._lib_cache["tracks"]["items"]) == 49
    assert b._lib_cache["tracks"]["offset"] == 49


def test_removal_outside_current_window_keeps_its_paging():
    b = bridge()
    b.removeFavoriteTrack("999")
    b._favorite_tracks_pool.finish()
    assert b._lib_cache["tracks"]["offset"] == 50
    assert len(b._lib_cache["tracks"]["items"]) == 50


def test_first_page_still_revalidates_after_a_favorite_is_removed():
    from bitwave.bitwave_ui.backend import BitWaveBridge, _LIBRARY_PAGE
    b = bridge()
    b._lib_cache["tracks"] = {"items": [{"id": str(i)} for i in range(_LIBRARY_PAGE)], "offset": _LIBRARY_PAGE, "more": True}
    b.removeFavoriteTrack("1")
    b._favorite_tracks_pool.finish()
    assert b._lib_cache["tracks"]["offset"] == _LIBRARY_PAGE - 1
    b._lib_gen = 1
    b._lib_sort = {}
    b.threadpool = Pool()
    b.libraryLoaded = Mock()
    b._lib_count = lambda cat, rows: len(rows)
    b._dress_library_rows = lambda cat, rows: rows
    b._lib_status = lambda *args: "loaded"
    b._set_busy = Mock()
    b._library_page = Mock(return_value=([{"id": "new"}], False))
    BitWaveBridge.loadLibrary(b, "tracks", True)
    assert len(b.threadpool.jobs) == 1
    b.threadpool.finish()
    b._library_page.assert_called_once_with("tracks", 0, _LIBRARY_PAGE)
    assert b._lib_cache["tracks"]["items"] == [{"id": "new"}]
    assert b._lib_cache["tracks"]["offset"] == _LIBRARY_PAGE
