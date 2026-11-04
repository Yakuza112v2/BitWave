"""Keep source imports, packaging, and displayed identity on the BitWave name."""
from pathlib import Path
import re
import tomllib

ROOT = Path(__file__).resolve().parents[1]


def test_current_source_has_only_bitwave_identity():
    previous = "".join(map(chr, [119, 97, 118, 101, 115]))
    old_author = "".join(map(chr, [105, 97, 109, 112, 114, 105, 118, 97, 99, 121]))
    pattern = re.compile(r"(?<![A-Za-z])" + previous + r"(?![A-Za-z])|" + old_author, re.I)
    problems = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or any(p.startswith(".") for p in path.relative_to(ROOT).parts):
            continue
        if path.suffix not in {".py", ".qml", ".js", ".tsv", ".md", ".toml", ".sh"}:
            continue
        if pattern.search(path.relative_to(ROOT).as_posix()):
            problems.append(str(path.relative_to(ROOT)))
        text = path.read_text(encoding="utf-8")
        if pattern.search(text):
            problems.append(str(path.relative_to(ROOT)))
    assert not problems, problems
    assert not (ROOT / previous).exists()
    assert (ROOT / "bitwave/bitwave_ui/__main__.py").is_file()
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]
    assert project["authors"] == [{"name": "Yakuza112v2"}]
