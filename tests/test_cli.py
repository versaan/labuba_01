"""Tests for the CLI entry point."""

import sys

from typing import Any

import pytest

from toolkit.__main__ import main


def test_cli_calc_success(monkeypatch: Any, capsys: Any) -> None:
    """Test CLI calculator successful execution with exit code 0."""
    monkeypatch.setattr(sys, "argv", ["toolkit", "calc", "2 + 2 * 2"])
    with pytest.raises(SystemExit) as exit_info:
        main()
    assert exit_info.value.code == 0
    captured = capsys.readouterr()
    assert "6" in captured.out


def test_cli_convert_success(monkeypatch: Any, capsys: Any) -> None:
    """Test CLI converter successful execution with exit code 0."""
    monkeypatch.setattr(sys, "argv", ["toolkit", "convert", "1000", "--from", "m", "--to", "km"])
    with pytest.raises(SystemExit) as exit_info:
        main()
    assert exit_info.value.code == 0
    captured = capsys.readouterr()
    assert "1.0" in captured.out


def test_cli_calc_error_stderr(monkeypatch: Any, capsys: Any) -> None:
    """Test CLI calculator error output to stderr and exit code 2."""
    monkeypatch.setattr(sys, "argv", ["toolkit", "calc", "10 / 0"])
    with pytest.raises(SystemExit) as exit_info:
        main()
    assert exit_info.value.code == 2
    captured = capsys.readouterr()
    assert captured.err != ""


def test_cli_convert_error_stderr(monkeypatch: Any, capsys: Any) -> None:
    """Test CLI converter error output to stderr and exit code 2."""
    monkeypatch.setattr(sys, "argv", ["toolkit", "convert", "10", "--from", "kg", "--to", "m"])
    with pytest.raises(SystemExit) as exit_info:
        main()
    assert exit_info.value.code == 2
    captured = capsys.readouterr()
    assert captured.err != ""
