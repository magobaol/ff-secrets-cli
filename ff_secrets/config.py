"""Loads the client config (flat YAML) and builds the resolver.

The client needs one setting: the ff-secrets-server endpoint.
"""
import os
from pathlib import Path

from .client import RemoteResolver
from .errors import FfSecretsError

CONFIG_PATH = Path(os.environ.get("FF_SECRETS_CONFIG", "~/.config/ff-secrets/config.yaml")).expanduser()


def _load_flat_yaml(path):
    """Parse a flat 'key: value' file. No nesting, no dependencies."""
    try:
        text = Path(path).read_text()
    except FileNotFoundError:
        raise FfSecretsError(f"config not found: {path}")
    data = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, _, value = line.partition(":")
        data[key.strip()] = value.strip()
    return data


def _settings():
    return _load_flat_yaml(CONFIG_PATH) if CONFIG_PATH.exists() else {}


def build_resolver():
    return RemoteResolver(_settings().get("server-endpoint"))
