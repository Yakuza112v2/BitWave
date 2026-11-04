"""The search sort control is remembered across launches.

The order is stored by NAME (relevance, date, name, popularity) rather than
by index, so the option list can change without a saved choice landing on
the wrong entry, and the direction is a real bool. ``setBitWavePref`` coerces
against the default's type, so both survive a round trip through it.
"""

from __future__ import annotations

from types import SimpleNamespace

from bitwave.bitwave_ui import backend


def _bridge():
    b = backend.BitWaveBridge.__new__(backend.BitWaveBridge)
    b._bitwave_prefs = backend.BitWaveBridge._default_bitwave_prefs(b)
    b._save_bitwave_prefs = lambda: None
    b._factory_reset = False
    b.settings = SimpleNamespace(data=SimpleNamespace())
    return b


def test_the_sort_prefs_default_to_relevance_descending():
    prefs = backend.BitWaveBridge._default_bitwave_prefs(_bridge())
    assert prefs["search_sort"] == "relevance"
    assert prefs["search_sort_asc"] is False


def test_the_sort_prefs_round_trip_with_their_types():
    b = _bridge()
    b.setBitWavePref("search_sort", "popularity")
    b.setBitWavePref("search_sort_asc", True)
    assert b.bitwavePref("search_sort") == "popularity"
    assert b.bitwavePref("search_sort_asc") is True
    # The QML side hands the bool over as a real bool, but a string form
    # (the str-coercing path) must not turn "false" into a truthy value.
    b.setBitWavePref("search_sort_asc", "false")
    assert b.bitwavePref("search_sort_asc") is False
