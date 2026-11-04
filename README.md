# BitWave

A native desktop app for saving music from your own TIDAL account for offline listening, maintained by [Yakuza112v2](https://github.com/Yakuza112v2).

BitWave is based on [Waves by iamprivacy](https://github.com/iamprivacy/Waves). The original license, authorship notices and project history are retained. See [UPSTREAM_README.md](UPSTREAM_README.md) for upstream features and acknowledgments.

## Downloads

Official BitWave releases: <https://github.com/Yakuza112v2/BitWave/releases>.

| Platform | Downloads |
| --- | --- |
| Windows | `bitwave_windows-x64.zip`, `bitwave_windows-arm64.zip` |
| macOS 15+ | `bitwave_macos-intel.zip`, `bitwave_macos-apple-silicon.zip` |
| macOS 12–14 | `bitwave_macos-intel_legacy.zip`, `bitwave_macos-apple-silicon_legacy.zip` |
| Linux | `bitwave_linux-x64.zip`, `bitwave_linux-arm64.zip`, corresponding `.AppImage` files |

Extract the archive and launch **BitWave**. A paid TIDAL account is required. Sign in with your own account on first launch. Use downloads only where you have permission to do so.

## Independent settings

BitWave starts with its own settings, sign-in, cache and update directory. It does not import or modify Waves profiles.

- Windows: `%APPDATA%/BitWave`
- macOS: `~/Library/Application Support/BitWave`
- Linux: `~/.config/BitWave`

Source checkouts use `BitWave-dev`. `XDG_CONFIG_HOME` overrides the base directory on every platform.

## Updates

The app's optional update check uses **Yakuza112v2/BitWave**. Release manifests are signed with BitWave's own Ed25519 key and checked before installation. Unsigned, modified or downgraded updates are refused.

The repository is private during migration. Public in-app updates become available after it is made public and the first signed BitWave release is published. Existing Waves installations remain separate and must install BitWave explicitly.

## Verify a download

Optional, for anyone who wants to check a download before the first launch. Every release carries two small files next to the builds: `SHA256SUMS`, one line per asset with its SHA-256, and `SHA256SUMS.sig`, an Ed25519 signature over that file made with the BitWave release key. The release page also prints each asset's hash in its **Verify** section. This is the public half of the release key, compiled into every build and checked by the in-app updater before it installs anything:

```
-----BEGIN PUBLIC KEY-----
MCowBQYDK2VwAyEAjQFMgwjIhp1dbcCAy31oUy4jX3E80+28Fb+MpQ+nZJA=
-----END PUBLIC KEY-----
```

**macOS or Linux**, from a folder holding the zip, `SHA256SUMS` and `SHA256SUMS.sig`. The signature step needs OpenSSL 3. Most current Linux distributions ship it; on macOS the built-in `openssl` is LibreSSL, which cannot check it, so install OpenSSL 3 with `brew install openssl@3` and run the third command with `$(brew --prefix openssl@3)/bin/openssl` in place of `openssl`:

```bash
printf '%s\n' '-----BEGIN PUBLIC KEY-----' 'MCowBQYDK2VwAyEAjQFMgwjIhp1dbcCAy31oUy4jX3E80+28Fb+MpQ+nZJA=' '-----END PUBLIC KEY-----' > bitwave-release.pem
base64 --decode < SHA256SUMS.sig > SHA256SUMS.sig.bin
openssl pkeyutl -verify -pubin -inkey bitwave-release.pem -rawin -in SHA256SUMS -sigfile SHA256SUMS.sig.bin
grep -v '^#' SHA256SUMS | tr -d '\r' | shasum -a 256 --ignore-missing -c -
```

The third command must print `Signature Verified Successfully` and the last one `<asset>: OK` for the zip you downloaded (on a system without `shasum`, use `sha256sum` in its place). Any other output means the file does not match this release: delete it and download it again.

**Windows** (PowerShell), from the same folder, with `bitwave_windows-x64.zip` replaced by the zip you downloaded:

```powershell
(Get-FileHash .\bitwave_windows-x64.zip -Algorithm SHA256).Hash.ToLower()
Select-String -Path SHA256SUMS -Pattern bitwave_windows-x64.zip
```

The two hashes must be identical. To also check the signature on Windows, run the macOS/Linux commands in Git Bash, which ships OpenSSL.

## Run from source

Requires Python 3.12 or 3.13.

```sh
poetry install --all-extras --with dev
poetry run python -m waves.waves_ui
```

The internal Python package remains `waves` to keep imports and bundled resources stable. The installed distribution and application are BitWave.

## Publish a release

See [BITWAVE_RELEASE.md](BITWAVE_RELEASE.md) for the signing setup and release steps. Platform builds run through GitHub Actions. BitWave does not currently publish a Homebrew, Scoop or winget package.

## License and credits

[AGPL-3.0-only](LICENSE). Based on Waves by iamprivacy, which grew out of Tidal-DL-NG and Tidaler. Original copyright notices and third-party acknowledgments are retained. Not affiliated with TIDAL.
