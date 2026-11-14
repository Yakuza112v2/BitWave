"""Explicit, account-bound removal of a single TIDAL track favorite."""
from __future__ import annotations

import logging
from PySide6.QtCore import QThreadPool, Qt, Signal, Slot
from bitwave.worker import Worker

logger = logging.getLogger(__name__)


class FavoriteTracksMixin:
    favoriteTrackBusy = Signal(str, bool)
    favoriteTrackRemoved = Signal(str)
    _favoriteRemovalDone = Signal("QVariant")

    def _init_favorite_tracks(self):
        self._favorite_tracks_epoch = 0
        self._favorite_track_pending = set()
        self._favorite_tracks_closing = False
        self._favorite_tracks_pool = QThreadPool(self)
        self._favorite_tracks_pool.setMaxThreadCount(1)
        self._favoriteRemovalDone.connect(self._favorite_removal_done, Qt.QueuedConnection)

    def _favorite_request_current(self, session, gen):
        return (self._logged_in and not self._factory_reset
                and not self._favorite_tracks_closing and gen == self._browse_gen
                and session is self.tidal.session)

    @Slot(str)
    def removeFavoriteTrack(self, track_id):
        track_id = str(track_id or "")
        if not track_id.isascii() or not track_id.isdigit() or not self._logged_in:
            return
        session = self.tidal.session
        gen = self._browse_gen
        token = (gen, track_id)
        if token in self._favorite_track_pending or not self._favorite_request_current(session, gen):
            return
        self._favorite_track_pending.add(token)
        self.favoriteTrackBusy.emit(track_id, True)

        def work():
            ok = False
            if self._favorite_request_current(session, gen):
                try:
                    # Never resolve self.tidal.session here: a queued write must
                    # not follow a switch to another account.
                    ok = bool(session.user.favorites.remove_track(track_id))
                except Exception:
                    logger.exception("Could not remove TIDAL track favorite %s", track_id)
            self._favoriteRemovalDone.emit({"id": track_id, "gen": gen, "session": session, "ok": ok})

        self._favorite_tracks_pool.start(Worker(work))

    @Slot("QVariant")
    def _favorite_removal_done(self, result):
        track_id, gen = result["id"], result["gen"]
        self._favorite_track_pending.discard((gen, track_id))
        if not self._favorite_request_current(result["session"], gen):
            return
        self.favoriteTrackBusy.emit(track_id, False)
        if not result["ok"]:
            self._set_status("Could not remove the TIDAL favorite. Please try again.")
            return
        # Retire reads started before the write. Keep loaded rows and their
        # scroll position; the server's next offset shifts back by one.
        self._favorite_tracks_epoch += 1
        entry = self._lib_cache.get("tracks")
        if entry is not None:
            kept = [r for r in entry["items"] if str(r.get("id", "")) != track_id]
            if len(kept) != len(entry["items"]):
                entry["offset"] = max(0, entry["offset"] - 1)
                entry["items"] = kept
        self._lib_reval_ts.pop("tracks", None)
        self._fav_ids.pop("tracks", None)
        self._lib_loading.discard("tracks")
        if self._home_cache:
            sections = []
            for section in self._home_cache:
                section = dict(section)
                if section.get("target") == "tracks":
                    section["items"] = [r for r in section["items"] if str(r.get("id", "")) != track_id]
                if section["items"]:
                    sections.append(section)
            self._home_cache = sections
        self._home_reval_ts = 0.0
        self._save_page_cache()
        self.favoriteTrackRemoved.emit(track_id)
        self._set_status("Track removed from TIDAL favorites. Downloaded files were kept.")
