from types import SimpleNamespace

import pytest
from click.testing import CliRunner

import pylingual.main as cli


@pytest.mark.parametrize(
    ("options", "environment", "expected_host", "expected_port"),
    [
        ([], {}, None, 6379),
        (["--redis-host", "127.0.0.1"], {}, "127.0.0.1", 6379),
        (["-r", "localhost", "--redis-port", "6380"], {}, "localhost", 6380),
        ([], {"PYLINGUAL_REDIS_HOST": "cache", "PYLINGUAL_REDIS_PORT": "6381"}, "cache", 6381),
        (["--redis-host", "localhost", "--redis-port", "6380"], {"PYLINGUAL_REDIS_HOST": "cache", "PYLINGUAL_REDIS_PORT": "6381"}, "localhost", 6380),
        (["--redis-host", ""], {"PYLINGUAL_REDIS_HOST": "cache"}, None, 6379),
    ],
)
def test_cli_passes_redis_settings_to_decompile(monkeypatch, tmp_path, options, environment, expected_host, expected_port):
    for name in ("PYLINGUAL_REDIS_HOST", "PYLINGUAL_REDIS_PORT"):
        monkeypatch.delenv(name, raising=False)
    for name, value in environment.items():
        monkeypatch.setenv(name, value)

    pyc = tmp_path / "example.pyc"
    pyc.write_bytes(b"")
    calls = []

    def decompile(**kwargs):
        calls.append(kwargs)
        return SimpleNamespace(original_pyc=SimpleNamespace(pyc_path=pyc), equivalence_results=[])

    monkeypatch.setattr(cli, "decompile", decompile)
    monkeypatch.setattr(cli, "transformers", SimpleNamespace(logging=SimpleNamespace(disable_default_handler=lambda: None, add_handler=lambda handler: None)))
    # main replaces these methods for its progress display; restore them after each invocation.
    for name in ("init", "progress"):
        monkeypatch.setattr(cli.TrackedList, name, getattr(cli.TrackedList, name))
    monkeypatch.setattr(cli.TrackedList, "__del__", lambda self: None, raising=False)

    result = CliRunner().invoke(cli.main, ["--quiet", "--out-dir", str(tmp_path / "output"), *options, str(pyc)])

    assert result.exit_code == 0, result.output
    assert len(calls) == 1
    assert calls[0]["redis_cache_server_ip"] == expected_host
    assert calls[0]["redis_port"] == expected_port


@pytest.mark.parametrize("port", ["0", "65536", "not-a-port"])
def test_cli_rejects_invalid_redis_ports(port):
    result = CliRunner().invoke(cli.main, ["--redis-port", port])
    assert result.exit_code == 2
    assert "Invalid value for '--redis-port'" in result.output
