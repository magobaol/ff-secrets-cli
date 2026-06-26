"""Resolves aliases by calling the ff-secrets-server HTTP API.

The client only knows the server endpoint; resolving an alias is a GET to the
server. The registry, the backend driver and the bearer all live in
ff-secrets-server.
"""
import urllib.error
import urllib.parse
import urllib.request

from .errors import FfSecretsError


class RemoteResolver:
    def __init__(self, endpoint):
        self._endpoint = (endpoint or "").rstrip("/")

    def _get(self, path):
        if not self._endpoint:
            raise FfSecretsError("missing 'server-endpoint' in config")
        try:
            with urllib.request.urlopen(self._endpoint + path) as resp:
                return resp.read().decode("utf-8")
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", "replace").strip()
            raise FfSecretsError(body or f"server returned HTTP {e.code}")
        except urllib.error.URLError as e:
            raise FfSecretsError(f"cannot reach server at {self._endpoint}: {e.reason}")

    def read(self, alias):
        return self._get("/v1/secret/" + urllib.parse.quote(alias))

    def aliases(self, prefix=""):
        query = "?prefix=" + urllib.parse.quote(prefix) if prefix else ""
        return self._get("/v1/aliases" + query)
