import subprocess
import sys
from getpass import getuser

import keyring
from cryptography.fernet import Fernet
from keyring.errors import KeyringError

from seekr.constants.app import AppInfo
from seekr.texts.keyring_troubleshooting import KeyringTroubleshootingText


class SecureStore:
    def __init__(self):
        self.__diagnose()
        self.__username = getuser()

    def set(self, service: str, value: str | bytes) -> bool:
        try:
            if isinstance(value, bytes):
                value = value.decode("utf-8")

            keyring.set_password(service, self.__username, value)
            return True
        except Exception as error:
            print(error.with_traceback(None))
            return False

    def get(self, service: str) -> str | None:
        return keyring.get_password(service, self.__username)

    def update(self, service: str, value: str) -> bool:
        return self.set(service, value)

    def delete(self, service: str) -> bool:
        try:
            keyring.delete_password(service, self.__username)
            return True
        except Exception as error:
            print(error.with_traceback(None))
            return False

    @staticmethod
    def __diagnose() -> str:
        try:
            result = subprocess.run(
                [sys.executable, "-m", "keyring", "diagnose"],
                capture_output=True,
                text=True,
                check=True,
            )

            return result.stdout.strip()
        except subprocess.CalledProcessError as error:
            diagnose_output = error.stdout or error.stderr or ""

            KeyringTroubleshootingText.display(
                error=str(error),
                diagnose_output=diagnose_output,
            )

            raise RuntimeError("Keyring diagnose failed.") from error

        except KeyringError as error:
            KeyringTroubleshootingText.display(error=str(error))
            raise RuntimeError("Keyring backend failed.") from error
