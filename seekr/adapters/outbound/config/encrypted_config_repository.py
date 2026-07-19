import json
from copy import deepcopy
from typing import Any

from cryptography.fernet import InvalidToken
from platformdirs import PlatformDirs

from seekr.adapters.outbound.config.binary_file_store import BinaryFileStore
from seekr.adapters.outbound.config.default_config_factory import DefaultConfigFactory
from seekr.adapters.outbound.config.fernet_cipher import FernetCipher
from seekr.adapters.outbound.config.keyring_secure_store import KeyringSecureStore
from seekr.application.ports.config_repository import ConfigRepository


class EncryptedConfigRepository(ConfigRepository):
    KEY_SERVICE = "seekr_crypto_key"

    def __init__(
        self,
        application_name: str = "seekr",
        company: str = "Pedroaba Tech",
    ) -> None:
        config_path = PlatformDirs(application_name, company).user_config_path
        self._file = BinaryFileStore(config_path / "seekr-config")
        self._secure_store = KeyringSecureStore()
        self._secure_store.diagnose()
        key = self._secure_store.get(self.KEY_SERVICE)
        self._cipher = FernetCipher(key.encode("utf-8") if key else None)
        if key is None:
            self._secure_store.set(self.KEY_SERVICE, self._cipher.key.decode("utf-8"))
        self._defaults = DefaultConfigFactory()
        self._data: dict[str, Any] = {}

    def initialize(self, reset: bool = False) -> None:
        if reset or not self._file.exists:
            self._data = self._defaults.create()
            self.commit()
            return
        try:
            self._data = self._cipher.decrypt(self._file.read())
        except InvalidToken, json.JSONDecodeError, OSError, ValueError:
            self._data = self._defaults.create()
            self.commit()

    def read(self) -> dict[str, Any]:
        return deepcopy(self._data)

    def replace(self, data: dict[str, Any]) -> None:
        self._data = deepcopy(data)

    def commit(self) -> None:
        self._file.write(self._cipher.encrypt(self._data))
