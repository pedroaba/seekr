import json
from collections.abc import Callable
from dataclasses import asdict, is_dataclass
from inspect import isclass
from platform import system
from typing import Any

from cryptography.fernet import InvalidToken
from platformdirs import PlatformDirs
from platformdirs.macos import MacOS
from platformdirs.unix import Unix
from platformdirs.windows import Windows

from seekr.constants.app import AppInfo
from seekr.constants.defaults import get_default_config
from seekr.exceptions.os import UnknownOperationalSystemError
from seekr.security.crypto import Crypto
from seekr.security.secure_store import SecureStore
from seekr.utils.file_manager import FileManager


class SeekrConfig:
    SUPPORTED_OPERATING_SYSTEMS = {"windows", "linux", "darwin"}

    APP_COMPANY = "Pedroaba Tech"
    APP_NAME = "seekr"
    
    __instance = None

    def __init__(self):
        self.__config_path = self._get_config_folder()

        # file must be a cryptography binary file
        self.__config_file = self.__config_path.user_config_path / "seekr-config"
        self.__key_path = self.__config_path.user_config_path / "keys"

        # crypto instance
        self.__secure_store = SecureStore()
        key = self.__secure_store.get(AppInfo.CRYPTO_KEY_INFO)

        self.__crypto = Crypto(
            bytes(key, "utf-8") if key is not None else None,
        )
        self.__crypto.initialize()

        if key is None:
            self.__secure_store.set(
                AppInfo.CRYPTO_KEY_INFO, self.__crypto.key.decode("utf-8"))

        # file manager configuration
        self.__file_manager = FileManager(self.__config_file)
        self.__file_manager.set_decrypt_fn(self.__crypto.decrypt)
        self.__file_manager.set_encrypt_fn(self.__crypto.encrypt)

        self.__user_data_buffer = {}

        self.__build()

    @staticmethod
    def get_dirs() -> Unix | MacOS | Windows:
        return SeekrConfig._get_config_folder()

    def __build(self, *, reset: bool = False):
        is_first_access = False
        if not self.__config_file.exists() or reset:
            self.__config_file.parent.mkdir(parents=True, exist_ok=True)
            self.__config_file.touch(exist_ok=True)
            is_first_access = True

        if is_first_access:
            self.__user_data_buffer = get_default_config()
            self.commit()
            return

        try:
            file_content = self.__file_manager.read()
            self.__user_data_buffer = file_content
        except (InvalidToken, json.JSONDecodeError, OSError):
            self.__build(reset=True)

    @staticmethod
    def _get_config_folder():
        """
        Get the path to the appdata folder based on the operating system.
        """
        os_name = system().lower()

        if os_name not in SeekrConfig.SUPPORTED_OPERATING_SYSTEMS:
            raise UnknownOperationalSystemError(os_name)

        return PlatformDirs(SeekrConfig.APP_NAME, SeekrConfig.APP_COMPANY)

    def commit(self):
        # commit config with binary and cryptographic content
        self.__file_manager.write(self.__user_data_buffer)

    def set_property(self, property_name: str, property_value: Any) -> None:
        # set property on buffer to save after
        value_to_set = property_value
        if isinstance(property_value, list):
            values_list_as_dict = []
            for item in property_value:
                values_list_as_dict.append(asdict(item))

            value_to_set = values_list_as_dict

        self.__user_data_buffer[property_name] = value_to_set

    def get_property(self, property_name: str, defaults: Any = None) -> Property:
        if property_name not in self.__user_data_buffer:
            return Property(property_name, defaults)
        return Property(property_name, self.__user_data_buffer[property_name])

    def get(self):
        return self.__user_data_buffer
    
    @classmethod
    def get_instance(cls) -> SeekrConfig:
        if not cls.__instance:
            cls.__instance = SeekrConfig()

        return cls.__instance


class Property:
    def __init__(self, property_name: str, property_value: Any) -> None:
        self.__name = property_name
        self.__value = property_value

    def transform(self, transform_fn: Callable[[str, Any], Any]) -> Property:
        """Used to transform the property's value to another property's value.

        :param transform_fn:
        :return:
        """
        self.__value = transform_fn(self.__name, self.__value)
        return self
    
    def map(self, map_fn: Callable[[str, Any, int], Any]) -> Property:
        """Transforms each item in the property's list value using the 
        provided mapping function.

        The mapping function is called for each item in the property's current value and
        receives the property name, the current item, and the item's index.
    
        :param map_fn: A function used to transform each item in the property's value.
                       It receives the property name, the current item, and the 
                       item index.
        :return: A new Property containing the transformed values.
        """

        new_value = []
        for index, item in enumerate(self.__value):
            new_value.append(map_fn(self.__name, item, index))

        self.__value = new_value
        return self

    def is_dict(self) -> bool:
        return isinstance(self.__value, dict)

    def is_list(self) -> bool:
        return isinstance(self.__value, list)

    def is_tuple(self) -> bool:
        return isinstance(self.__value, tuple)

    def is_number(self) -> bool:
        return isinstance(self.__value, int | float)

    def is_string(self) -> bool:
        return isinstance(self.__value, str)

    @staticmethod
    def __check_list_item_type_is_json(item: Any) -> bool:
        return isinstance(item, dict) or is_dataclass(item) or isclass(item)

    def get(self) -> Any:
        return self.__value
