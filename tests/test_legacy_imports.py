import importlib

import pygorpmrustinfo.cli as cli


def test_legacy_package_imports_resolve():
    for module_name in ["pyrpmdb", "pyrustaudit", "pygobuildinfo"]:
        module = importlib.import_module(module_name)
        assert module is not None


def test_cli_defaults_to_legacy_script_modes(monkeypatch, tmp_path):
    calls = []

    def fake_dispatch(path, mode):
        calls.append((path, mode))
        return {"ok": True}

    monkeypatch.setattr(cli, "_dispatch", fake_dispatch)
    example = tmp_path / "example"
    example.write_text("hello", encoding="utf-8")

    cli.main(["/tmp/get_rpm_info", str(example)])
    assert calls == [(str(example), "rpm")]

    calls.clear()
    cli.main(["/tmp/get_rust_audit", str(example)])
    assert calls == [(str(example), "rust")]
