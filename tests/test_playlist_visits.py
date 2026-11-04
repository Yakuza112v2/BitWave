from bitwave.bitwave_ui.playlist_visits import PlaylistVisits


def rows(*ids):
    return [{'id': x, 'kind': 'track'} for x in ids]


def test_additions_stay_new_during_visit_then_clear_and_survive_restart(tmp_path):
    path = tmp_path / 'visits.json'
    store = PlaylistVisits(path)
    assert store.mark('user', 'p', '1', rows('old')) == [False]
    assert store.mark('user', 'p', '2', rows('old', 'added')) == [False, True]
    assert store.mark('user', 'p', '2', rows('old', 'added')) == [False, True]
    assert store.mark('user', 'p', '2', rows('old', 'added', 'later')) == [False, True, True]
    store = PlaylistVisits(path)
    assert store.mark('user', 'p', '3', rows('old', 'added', 'later')) == [False] * 3
    assert store.mark('user', 'p', '4', rows('old', 'added', 'later', 'next')) == [False] * 3 + [True]


def test_reorder_duplicates_removal_and_readdition(tmp_path):
    store = PlaylistVisits(tmp_path / 'visits.json')
    store.mark('u', 'p', '1', rows('a', 'b'))
    assert store.mark('u', 'p', '2', rows('b', 'a')) == [False, False]
    assert store.mark('u', 'p', '3', rows('a', 'b', 'a')) == [False, False, True]
    store.mark('u', 'p', '4', rows('b'))
    assert store.mark('u', 'p', '5', rows('a', 'b')) == [True, False]


def test_partial_data_does_not_acknowledge_and_accounts_and_playlists_are_separate(tmp_path):
    store = PlaylistVisits(tmp_path / 'visits.json')
    store.mark('u', 'p', '1', rows('a'))
    assert store.mark('u', 'p', '2', rows('a', 'b'), False) == [False, True]
    assert store.mark('u', 'p', '3', rows('a', 'b')) == [False, True]
    assert store.mark('other', 'p', '4', rows('a', 'b')) == [False, False]
    assert store.mark('u', 'other', '5', rows('a', 'b')) == [False, False]
    assert store.mark('', 'p', '6', rows('x')) == [False]


def test_empty_playlist_and_corrupt_file(tmp_path):
    path = tmp_path / 'visits.json'
    path.write_text('broken')
    store = PlaylistVisits(path)
    assert store.mark('u', 'p', '1', []) == []
    assert store.mark('u', 'p', '2', rows('first')) == [True]
