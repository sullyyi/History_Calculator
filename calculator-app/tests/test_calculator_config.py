import os
from pathlib import Path

import pytest

from app.calculator_config import load_config
from app.exceptions import ConfigurationError


def test_load_config_defaults(monkeypatch, tmp_path: Path):
    # Ensure env vars are unset so defaults are used
    monkeypatch.delenv("CALC_HISTORY_PATH", raising=False)
    monkeypatch.delenv("CALC_AUTO_LOAD", raising=False)
    monkeypatch.delenv("CALC_AUTO_SAVE", raising=False)

    cfg = load_config()
    assert str(cfg.history_path).endswith("history.csv")
    assert cfg.auto_load is True
    assert cfg.auto_save is False


@pytest.mark.parametrize("val", ["TRUE", "true", "1", "yes", "on", "Y"])
def test_load_config_bool_true(monkeypatch, tmp_path: Path, val: str):
    monkeypatch.setenv("CALC_HISTORY_PATH", str(tmp_path / "history.csv"))
    monkeypatch.setenv("CALC_AUTO_LOAD", val)
    monkeypatch.setenv("CALC_AUTO_SAVE", val)

    cfg = load_config()
    assert cfg.auto_load is True
    assert cfg.auto_save is True


@pytest.mark.parametrize("val", ["FALSE", "false", "0", "no", "off", "N"])
def test_load_config_bool_false(monkeypatch, tmp_path: Path, val: str):
    monkeypatch.setenv("CALC_HISTORY_PATH", str(tmp_path / "history.csv"))
    monkeypatch.setenv("CALC_AUTO_LOAD", val)
    monkeypatch.setenv("CALC_AUTO_SAVE", val)

    cfg = load_config()
    assert cfg.auto_load is False
    assert cfg.auto_save is False


def test_load_config_rejects_empty_history_path(monkeypatch):
    monkeypatch.setenv("CALC_HISTORY_PATH", "   ")
    with pytest.raises(ConfigurationError):
        load_config()


@pytest.mark.parametrize("bad", ["maybe", "sometimes", "2", "truthy", ""])
def test_load_config_rejects_invalid_bool(monkeypatch, tmp_path: Path, bad: str):
    monkeypatch.setenv("CALC_HISTORY_PATH", str(tmp_path / "history.csv"))
    monkeypatch.setenv("CALC_AUTO_LOAD", bad)
    with pytest.raises(ConfigurationError):
        load_config()