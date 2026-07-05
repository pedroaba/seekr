import json
from pathlib import Path

from cryptography.fernet import Fernet

from seekr.enconder import InternalJsonEncoder


class NoCryptKeyException(AttributeError):
    def __init__(self) -> None:
        super().__init__("You must have a key file before encrypt or decrypt data,"
                         "see: https://pypi.org/project/cryptography/")


class Crypto:
    def __init__(self, key_filepath: Path) -> None:
        self.__key_filepath = key_filepath
        self.__key: bytes = b""

        if not self.__key_filepath.exists():
            self.__key_filepath.parent.mkdir(parents=True, exist_ok=True)
            self.__key_filepath.touch()

            self.__gen_key()
            return

        self.__load_key()

    def encrypt(self, data: dict) -> bytes:
        if self.__key is None:
            raise NoCryptKeyException()

        fernet = Fernet(self.__key)

        buffered_data = (
            json
                .dumps(data, default=InternalJsonEncoder.encode)
                .encode("utf-8")
        )
        encrypted_buffer = fernet.encrypt(buffered_data)

        return encrypted_buffer

    def decrypt(self, data: bytes) -> dict:
        if self.__key is None:
            raise NoCryptKeyException()

        fernet = Fernet(self.__key)
        buffered_data = fernet.decrypt(data)
        return json.loads(buffered_data.decode("utf-8"))

    def __gen_key(self) -> None:
        self.__key = Fernet.generate_key()

        with open(self.__key_filepath, "wb") as key_file:
            key_file.write(self.__key)

    def __load_key(self) -> None:
        with open(self.__key_filepath, "rb") as key_file:
            self.__key = key_file.read()
