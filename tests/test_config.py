
import pytest


def test_default_config_is_valid():
    """Config loads with defaults when no env vars are set."""
    from fastmcp_blueprint.config import ServerConfig

    config = ServerConfig.from_env()
    assert config.host == "localhost"
    assert config.port == 8000
    assert config.log_format == "rich"
    assert config.auth_provider == ""


def test_invalid_log_format_raises(monkeypatch):
    monkeypatch.setenv("LOG_FORMAT", "yaml")

    from fastmcp_blueprint.config import ServerConfig

    with pytest.raises(ValueError, match="LOG_FORMAT"):
        ServerConfig.from_env()


def test_invalid_auth_provider_raises(monkeypatch):
    monkeypatch.setenv("AUTH_PROVIDER", "bad")

    from fastmcp_blueprint.config import ServerConfig

    with pytest.raises(ValueError, match="AUTH_PROVIDER"):
        ServerConfig.from_env()


def test_valid_auth_providers_accepted(monkeypatch):
    from fastmcp_blueprint.config import ServerConfig

    for provider in ("", "remote", "oauth_proxy"):
        monkeypatch.setenv("AUTH_PROVIDER", provider)
        config = ServerConfig.from_env()
        assert config.auth_provider == provider


def test_env_vars_override_defaults(monkeypatch):
    monkeypatch.setenv("HOST", "0.0.0.0")
    monkeypatch.setenv("PORT", "9000")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("NAME", "TestServer")

    from fastmcp_blueprint.config import ServerConfig

    config = ServerConfig.from_env()
    assert config.host == "0.0.0.0"
    assert config.port == 9000
    assert config.log_level == "DEBUG"
    assert config.name == "TestServer"


def test_ssl_fields_default_to_none():
    from fastmcp_blueprint.config import ServerConfig

    config = ServerConfig.from_env()
    assert config.ssl_certfile is None
    assert config.ssl_keyfile is None
