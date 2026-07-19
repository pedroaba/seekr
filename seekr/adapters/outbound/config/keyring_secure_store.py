# Required for the fixed, application-controlled keyring diagnostic command.
import subprocess  # nosec B404
import sys
from getpass import getuser

import keyring


class KeyringSecureStore:
    def __init__(self) -> None:
        self._username = getuser()

    @staticmethod
    def diagnose(self) -> str:
        result = subprocess.run(  # nosec B603
            [sys.executable, "-m", "keyring", "diagnose"],
            capture_output=True,
            text=True,
            check=True,
        )

        return result.stdout.strip()

    def get(self, service: str) -> str | None:
        return keyring.get_password(service, self._username)

    def set(self, service: str, value: str) -> None:
        keyring.set_password(service, self._username, value)
