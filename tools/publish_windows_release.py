"""Publish a verified Windows release by ID, without creating duplicate entries."""
from __future__ import annotations

import argparse
import hashlib
import os
import re
from pathlib import Path
import subprocess
import tempfile
import zipfile

import requests
from bitwave.bitwave_ui.signing import parse_sha256sums, verify
from release_verify_notes import verify_notes

REPO = "Yakuza112v2/BitWave"
API = "https://api.github.com/repos/" + REPO
ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("tag")
    parser.add_argument("--commit")
    parser.add_argument("--build-run")
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--signature", type=Path)
    args = parser.parse_args()
    assert re.fullmatch(r"v[0-9]+\.[0-9]+\.[0-9]+(?:-[A-Za-z0-9.-]+)?", args.tag)
    session = requests.Session()
    session.headers.update({"Authorization": "Bearer " + os.environ["GH_TOKEN"], "Accept": "application/vnd.github+json"})

    def api(method, path, **kwargs):
        r = session.request(method, API + path, timeout=120, **kwargs)
        r.raise_for_status()
        return r.json() if r.content else None

    commit = args.commit
    expected = None
    if args.build_run:
        run = api("GET", "/actions/runs/" + args.build_run)
        assert run["path"] == ".github/workflows/windows-release.yml"
        commit = run["head_sha"]
        jobs = api("GET", "/actions/runs/" + args.build_run + "/jobs")["jobs"]
        assert any("windows-x64" in j["name"] and j["conclusion"] == "success" for j in jobs)
        with tempfile.TemporaryDirectory() as d:
            subprocess.run(["gh", "run", "download", args.build_run, "-R", REPO, "--pattern", "sha256-*", "--dir", d], check=True)
            expected = {}
            for f in Path(d).rglob("*.sha256"):
                expected.update(parse_sha256sums(f.read_text()))
        assert expected, "Build checksums are missing"
    assert commit and re.fullmatch(r"[0-9a-f]{40}", commit)
    # A helper-only change may follow a build; application sources must match.
    subprocess.run(["git", "diff", "--exit-code", commit, "--", "bitwave", "bitwave.py", "pyproject.toml"], cwd=ROOT, check=True)
    ref = api("GET", "/git/ref/tags/" + args.tag) if args.build_run else None
    if ref:
        assert ref["object"]["sha"] == commit, "Tag does not match the successful build"
    releases = api("GET", "/releases?per_page=100")
    related = [r for r in releases if r["tag_name"] == args.tag]
    candidates = [r for r in related if any(a["name"].startswith("bitwave_windows-") and a["name"].endswith(".zip") for a in r["assets"])]
    assert len(candidates) == 1, "Expected one release containing the Windows build"
    release = candidates[0]
    assets = {a["name"]: a for a in release["assets"]}

    def download(asset, dest):
        r = session.get(asset["url"], headers={"Accept": "application/octet-stream"}, stream=True, timeout=120)
        r.raise_for_status()
        with dest.open("wb") as out:
            for chunk in r.iter_content(1024 * 1024):
                out.write(chunk)

    with tempfile.TemporaryDirectory() as d:
        folder = Path(d)
        for name, supplied in (("SHA256SUMS", args.manifest), ("SHA256SUMS.sig", args.signature)):
            if supplied:
                (folder / name).write_bytes(supplied.read_bytes())
            else:
                download(assets[name], folder / name)
        manifest = (folder / "SHA256SUMS").read_bytes()
        signature = (folder / "SHA256SUMS.sig").read_text().strip()
        assert verify(manifest, signature), "Invalid release signature"
        assert ("# bitwave-version: " + args.tag) in manifest.decode()
        sums = parse_sha256sums(manifest.decode())
        assert sums and all(n in {"bitwave_windows-x64.zip", "bitwave_windows-arm64.zip"} for n in sums)
        if expected is not None:
            assert sums == expected, "Signed sums differ from the successful build"
        for name, digest in sums.items():
            archive = folder / name
            download(assets[name], archive)
            assert hashlib.sha256(archive.read_bytes()).hexdigest() == digest
            with zipfile.ZipFile(archive) as z:
                assert "BitWave/BitWave.exe" in z.namelist()
                for source in (ROOT / "bitwave/bitwave_ui/qml").rglob("*"):
                    if not source.is_file() or source.suffix not in {".qml", ".js", ".tsv", ".png", ".qsb", ".frag"}:
                        continue
                    actual = z.read("BitWave/bitwave_ui/qml/" + source.relative_to(ROOT / "bitwave/bitwave_ui/qml").as_posix())
                    wanted = source.read_bytes()
                    if source.suffix in {".qml", ".js", ".tsv", ".frag"}:
                        actual, wanted = actual.replace(b"\r\n", b"\n"), wanted.replace(b"\r\n", b"\n")
                    assert actual == wanted, source.name
        # All validation precedes any mutation. Only empty, automatically
        # generated duplicates are removed; the tag and built assets remain.
        for other in related:
            if other["id"] == release["id"]:
                continue
            assert not other["assets"] and other["author"]["login"] == "github-actions[bot]", "Refusing to change an existing nonempty or human-authored release"
        for name in ("SHA256SUMS", "SHA256SUMS.sig"):
            payload = (folder / name).read_bytes()
            if name in assets:
                existing = folder / (name + ".existing")
                download(assets[name], existing)
                if existing.read_bytes() == payload:
                    continue
                api("DELETE", "/releases/assets/" + str(assets[name]["id"]))
            upload = "https://uploads.github.com/repos/" + REPO + "/releases/" + str(release["id"]) + "/assets"
            response = session.post(upload, params={"name": name}, headers={"Content-Type": "application/octet-stream"}, data=payload, timeout=120)
            response.raise_for_status()
        for other in related:
            if other["id"] != release["id"]:
                api("DELETE", "/releases/" + str(other["id"]))
        changes = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8").splitlines()
        notes, active = [], False
        for line in changes:
            if line.startswith("## "):
                if active:
                    break
                active = args.tag in line.split()
                continue
            if active:
                notes.append(line)
        assert notes, "Release notes are missing"
        body = "\n".join(notes).strip() + "\n\n<details><summary>Download prüfen</summary>\n\n" + verify_notes(manifest.decode()) + "\n</details>"
        beta = "-" in args.tag
        result = api("PATCH", "/releases/" + str(release["id"]), json={"tag_name": args.tag, "target_commitish": commit, "name": "BitWave " + args.tag.removeprefix("v"), "body": body, "draft": False, "prerelease": beta, "make_latest": "false" if beta else "true"})
        assert not result["draft"] and result["prerelease"] == beta
        assert api("GET", "/git/ref/tags/" + args.tag)["object"]["sha"] == commit
        print("Veröffentlicht und geprüft:", result["html_url"])


if __name__ == "__main__":
    main()
