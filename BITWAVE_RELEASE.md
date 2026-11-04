# BitWave release setup

Source, issues, builds and updates belong to `Yakuza112v2/BitWave`.

## One-time setup

1. Keep the repository private while reviewing this migration.
2. Add the BitWave private release key as the repository Actions secret **BITWAVE_SIGNING_KEY**. The matching public key is embedded in `waves/waves_ui/signing.py`. Never commit the private key or replace it after distributing builds without planning a signing-key migration.
3. Enable GitHub Actions for this repository. The release workflow uses its repository-scoped `GITHUB_TOKEN`; no personal token is needed.
4. Make the repository public when the migration is ready. The app's GitHub update requests are anonymous, so releases in a private repository cannot be fetched by installed applications.

## Version and build

Update both `pyproject.toml` and `waves/waves_ui/__init__.py` to the same `X.Y.Z` version. Add a `## vX.Y.Z (YYYY-MM-DD)` entry to `CHANGELOG.md`.

For a test build, run **release-or-test-build** from the Actions tab with a blank `release_tag`. The `only` input can limit the platforms. These runs produce build artifacts without publishing a release.

For a production release, tag the tested commit `vX.Y.Z` and push that tag, or manually run the workflow with `release_tag=vX.Y.Z` and `only` blank. All eight platform builds must pass. The workflow collects checksums, signs the manifest, then publishes the release. A missing signing secret fails the release.

## Before first distribution

- Check the app title and executable read BitWave.
- Confirm first launch has no Waves sign-in or settings.
- Test Windows, macOS and Linux packages on the intended platforms.
- Confirm `SHA256SUMS` and `SHA256SUMS.sig` are attached to the release.
- Exercise a signed update between two BitWave versions on each platform.

The original Waves key, repository, donation destination and Homebrew tap are not used for BitWave releases. The internal `waves` package, build-tree basename and `waves-version` manifest field are implementation details retained for compatibility.
