from __future__ import annotations

import subprocess
import sys

from keyring.errors import KeyringError

from seekr.texts.keyring_troubleshooting import KeyringTroubleshootingText


class SecureStore:
    def __init__(self):
        self.__diagnose()

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