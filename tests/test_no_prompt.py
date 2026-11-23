"""handle_missing_dir must never prompt when stdin is not a tty."""
import io
import os

from haggle import dacc


def test_creates_dir_without_prompting_when_not_tty(tmp_path, monkeypatch):
    monkeypatch.setattr(dacc.sys, "stdin", io.StringIO(""))  # EOF, not a tty

    def boom(*a, **k):
        raise AssertionError("input() called")

    monkeypatch.setattr("builtins.input", boom)
    target = str(tmp_path / "newdir")
    dacc.handle_missing_dir(target, verbose=False)
    assert os.path.isdir(target)
