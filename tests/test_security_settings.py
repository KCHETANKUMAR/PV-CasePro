import importlib
import config

def test_demo_mode_defaults_to_read_only(monkeypatch):
    monkeypatch.delenv("PV_CASEPRO_DEMO_MODE",raising=False)
    importlib.reload(config)
    assert config.DEMO_MODE is True

def test_local_write_mode_requires_explicit_opt_in(monkeypatch):
    monkeypatch.setenv("PV_CASEPRO_DEMO_MODE","0")
    importlib.reload(config)
    assert config.DEMO_MODE is False
