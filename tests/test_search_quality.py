"""Search filtering and ordering run in the same JS engine as the UI."""
import json
from pathlib import Path
from PySide6.QtCore import QCoreApplication
from PySide6.QtQml import QJSEngine


def test_catalog_quality_filter_and_stable_order():
    app = QCoreApplication.instance() or QCoreApplication([])
    engine = QJSEngine()
    source = (Path(__file__).resolve().parents[1] / "bitwave/bitwave_ui/qml/SearchQuality.js").read_text(encoding="utf-8")
    result = engine.evaluate(source.replace(".pragma library", ""))
    assert not result.isError(), result.toString()
    rows = [{"id": str(i), "quality": q} for i, q in enumerate(["LOSSLESS", "HI-RES", "HIGH", "ATMOS", "HI-RES", "LOW", ""])]
    engine.evaluate("var rows = " + json.dumps(rows))
    def ids(expr):
        result = engine.evaluate("JSON.stringify(" + expr + ".map(function(x){return x.id}))")
        assert not result.isError(), result.toString()
        return json.loads(result.toString())
    assert ids("select(rows, true)") == ["1", "4"]
    assert ids("select(rows, false)") == [str(i) for i in range(7)]
    assert ids("byQuality(rows, false)") == ["1", "4", "0", "2", "5", "3", "6"]
    assert ids("byQuality(rows, true)") == ["3", "6", "5", "2", "0", "1", "4"]
    assert ids("select(rows, true)") == ["1", "4"]  # source was not mutated
    assert engine.evaluate('audioResult({kind:"playlist",quality:"HI-RES"})').toBool() is False
    assert engine.evaluate('isHiRes({quality:"HI_RES_LOSSLESS"})').toBool() is True
