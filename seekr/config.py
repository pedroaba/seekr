from platform import system
from typing import Any

from platformdirs import PlatformDirs

from seekr.constants.defaults import get_default_config
from seekr.exceptions.os import UnknownOperationalSystemError
from seekr.security.crypto import Crypto
from seekr.utils.file_manager import FileManager


class SeekrConfig:
    SUPPORTED_OPERATING_SYSTEMS = {"windows", "linux", "darwin"}

    APP_COMPANY = "Pedroaba Tech"
    APP_NAME = "seekr"

    def __init__(self):
        self.__config_path = self._get_config_folder()

        # file must be a cryptography binary file
        self.__config_file = self.__config_path.user_config_path / "seekr-config"
        self.__key_path = self.__config_path.user_config_path / "keys"

        # crypto instance
        self.__crypto = Crypto(self.__key_path)

        # file manager configuration
        self.__file_manager = FileManager(self.__config_file)
        self.__file_manager.set_decrypt_fn(self.__crypto.decrypt)
        self.__file_manager.set_encrypt_fn(self.__crypto.encrypt)

        self.__user_data_buffer = {}

        self.__build()

    def __build(self):
        is_first_access = False
        if not self.__config_file.exists():
            self.__config_file.parent.mkdir(parents=True, exist_ok=True)
            self.__config_file.touch(exist_ok=True)
            is_first_access = True

        if is_first_access:
            self.__user_data_buffer = get_default_config()
            self.commit()
            return

        file_content = self.__file_manager.read()
        self.__user_data_buffer = file_content

    def _get_config_folder(self):
        """
        Get the path to the appdata folder based on the operating system.
        """
        os_name = system().lower()

        if os_name not in self.SUPPORTED_OPERATING_SYSTEMS:
            raise UnknownOperationalSystemError(os_name)

        return PlatformDirs(self.APP_NAME, self.APP_COMPANY)

    def commit(self):
        # commit config with binary and cryptographic content
        self.__file_manager.write(self.__user_data_buffer)
        print(f"File writen on {self.__key_path.absolute()}")

    def set_property(self, property_name: str, property_value: Any) -> None:
        # set property on buffer to save after
        pass
