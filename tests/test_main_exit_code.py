from types import SimpleNamespace

from click.testing import CliRunner

import pylingual.main as cli


def _patch_cli(monkeypatch):
    monkeypatch.setattr(cli, "transformers", SimpleNamespace(logging=SimpleNamespace(disable_default_handler=lambda: None, add_handler=lambda handler: None)))
    # main replaces these methods for its progress display; restore them after each invocation.
    for name in ("init", "progress"):
        monkeypatch.setattr(cli.TrackedList, name, getattr(cli.TrackedList, name))
    monkeypatch.setattr(cli.TrackedList, "__del__", lambda self: None, raising=False)


def test_cli_exits_nonzero_when_every_file_fails(monkeypatch, tmp_path):
    pyc = tmp_path / "broken.pyc"
    pyc.write_bytes(b"")

    def decompile(**kwargs):
        raise RuntimeError("source reconstruction failed")

    monkeypatch.setattr(cli, "decompile", decompile)
    _patch_cli(monkeypatch)

    out_dir = tmp_path / "out"
    result = CliRunner().invoke(cli.main, ["--out-dir", str(out_dir), str(pyc)])

    assert result.exit_code == 1, result.output
    assert "No output files were produced" in result.output
    assert not list(out_dir.glob("*.py"))


def test_cli_exits_zero_when_at_least_one_file_succeeds(monkeypatch, tmp_path):
    broken = tmp_path / "broken.pyc"
    broken.write_bytes(b"")
    working = tmp_path / "working.pyc"
    working.write_bytes(b"")

    def decompile(**kwargs):
        if kwargs["pyc"].name == "broken.pyc":
            raise RuntimeError("source reconstruction failed")
        kwargs["save_to"].write_text("print('ok')\n", encoding="utf-8")
        return SimpleNamespace(original_pyc=SimpleNamespace(pyc_path=kwargs["pyc"]), equivalence_results=[])

    monkeypatch.setattr(cli, "decompile", decompile)
    _patch_cli(monkeypatch)

    result = CliRunner().invoke(cli.main, ["--quiet", "--out-dir", str(tmp_path / "out"), str(broken), str(working)])

    assert result.exit_code == 0, result.output
    assert (tmp_path / "out" / "decompiled_working.py").read_text(encoding="utf-8") == "print('ok')\n"


def test_cli_exits_zero_when_output_already_exists(monkeypatch, tmp_path):
    pyc = tmp_path / "sample.pyc"
    pyc.write_bytes(b"")
    out_dir = tmp_path / "out"
    out_dir.mkdir()
    (out_dir / "decompiled_sample.py").write_text("print('existing')\n", encoding="utf-8")

    def decompile(**kwargs):
        raise AssertionError("decompile should not run when the output already exists")

    monkeypatch.setattr(cli, "decompile", decompile)
    _patch_cli(monkeypatch)

    result = CliRunner().invoke(cli.main, ["--quiet", "--out-dir", str(out_dir), str(pyc)])

    assert result.exit_code == 0, result.output
