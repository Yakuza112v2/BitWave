"""Publishing must not mutate releases before signature and checksum checks."""
import base64
import importlib.util
import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

import pytest
from Crypto.PublicKey import ECC
from bitwave.bitwave_ui import signing

ROOT = Path(__file__).resolve().parents[1]


def publisher(monkeypatch):
    monkeypatch.syspath_prepend(str(ROOT / "tools"))
    spec = importlib.util.spec_from_file_location("publish_windows_release", ROOT / "tools/publish_windows_release.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    monkeypatch.setenv("GH_TOKEN", "mock-token")
    monkeypatch.setattr(sys, "argv", ["publish", "v0.2.3-Beta", "--commit", "a" * 40])
    monkeypatch.setattr(module.subprocess, "run", Mock())
    return module


def arrange(module, monkeypatch, manifest, signature):
    assets = [{"name": n, "id": i, "url": n} for i, n in enumerate(["bitwave_windows-x64.zip", "SHA256SUMS", "SHA256SUMS.sig"])]
    release = {"id": 1, "tag_name": "v0.2.3-Beta", "assets": assets}
    api = Mock()
    api.request.return_value = SimpleNamespace(content=b"json", raise_for_status=lambda: None, json=lambda: [release])
    payloads = {"SHA256SUMS": manifest, "SHA256SUMS.sig": signature.encode(), "bitwave_windows-x64.zip": b"tampered"}
    api.get.side_effect = lambda url, **kw: SimpleNamespace(raise_for_status=lambda: None, iter_content=lambda size: [payloads[url]])
    monkeypatch.setattr(module.requests, "Session", lambda: api)
    return api


def test_invalid_signature_never_changes_any_release(monkeypatch):
    module = publisher(monkeypatch)
    api = arrange(module, monkeypatch, b"# bitwave-version: v0.2.3-Beta\n", "invalid")
    with pytest.raises(AssertionError, match="signature"):
        module.main()
    assert all(c.args[0] == "GET" for c in api.request.call_args_list)
    api.post.assert_not_called()


def test_tampered_archive_never_changes_any_release(monkeypatch):
    module = publisher(monkeypatch)
    key = ECC.generate(curve="Ed25519")
    public = base64.b64encode(key.public_key().export_key(format="raw")).decode()
    manifest = ("# bitwave-version: v0.2.3-Beta\n" + "0" * 64 + "  bitwave_windows-x64.zip\n").encode()
    signature = signing.sign(manifest, key.export_key(format="PEM"))
    monkeypatch.setattr(module, "verify", lambda m, s: signing.verify(m, s, public))
    api = arrange(module, monkeypatch, manifest, signature)
    with pytest.raises(AssertionError):
        module.main()
    assert all(c.args[0] == "GET" for c in api.request.call_args_list)
    api.post.assert_not_called()
