import json
from typing import Any

from cryptography.fernet import Fernet


class FernetCipher:
    def __init__(self, key: bytes | None = None) -> None:
        self._key = key or Fernet.generate_key()

    @property
    def key(self) -> bytes:
        return self._key

    def encrypt(self, data: dict[str, Any]) -> bytes:
        return Fernet(self._key).encrypt(json.dumps(data).encode("utf-8"))

    def decrypt(self, data: bytes) -> dict[str, Any]:
        value = json.loads(Fernet(self._key).decrypt(data).decode("utf-8"))
        if not isinstance(value, dict):
            raise ValueError("Seekr configuration must be a JSON object.")
        return value
