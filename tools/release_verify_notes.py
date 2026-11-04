#!/usr/bin/env python
"""Print the "Verify" footer of a GitHub Release body from its SHA256SUMS.

The footer puts the expected hash next to each download, prints the release
public key, and gives the same copyable commands as the README, so a cautious
user can check a build without leaving the release page. CI appends it to the
release notes right after signing the manifest.

Usage::

    python tools/release_verify_notes.py SHA256SUMS >> RELEASE_NOTES.md
"""

from __future__ import annotations

import sys

from waves.waves_ui.signing import parse_sha256sums, public_key_pem

README_VERIFY_URL = "https://github.com/Yakuza112v2/BitWave#download-prüfen"


def verify_notes(manifest_text: str) -> str:
    sums = parse_sha256sums(manifest_text)
    lines = [
        "### 🔐 Download prüfen",
        "",
        "| Datei | SHA-256 |",
        "| --- | --- |",
    ]
    lines.extend(f"| `{name}` | `{digest}` |" for name, digest in sorted(sums.items()))
    lines += [
        "",
        "`SHA256SUMS` enthält die Prüfsummen. `SHA256SUMS.sig` ist die Ed25519-Signatur mit dem BitWave-Schlüssel. Dieser öffentliche Schlüssel ist auch fest in der App hinterlegt:",
        "",
        "```",
        public_key_pem().rstrip("\n"),
        "```",
        "",
        "Mit Git Bash und OpenSSL 3 im Ordner mit ZIP-Archiv, `SHA256SUMS` und `SHA256SUMS.sig`:",
        "",
        "```bash",
        "printf '%s\\n' '-----BEGIN PUBLIC KEY-----' '"
        + public_key_pem().splitlines()[1]
        + "' '-----END PUBLIC KEY-----' > bitwave-release.pem",
        "base64 --decode < SHA256SUMS.sig > SHA256SUMS.sig.bin",
        "openssl pkeyutl -verify -pubin -inkey bitwave-release.pem -rawin -in SHA256SUMS -sigfile SHA256SUMS.sig.bin",
        "grep -v '^#' SHA256SUMS | tr -d '\\r' | shasum -a 256 --ignore-missing -c -",
        "```",
        "",
        f"Windows-Anleitung und Einzelheiten: [Download prüfen]({README_VERIFY_URL}).",
    ]
    return "\n".join(lines) + "\n"


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: release_verify_notes.py <SHA256SUMS>", file=sys.stderr)
        return 2
    with open(argv[1], encoding="utf-8") as fh:
        sys.stdout.write(verify_notes(fh.read()))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
