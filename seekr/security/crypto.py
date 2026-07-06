import json
from pathlib import Path

from cryptography.fernet import Fernet

from seekr.enconder import InternalJsonEncoder


class NoCryptKeyException(AttributeError):
    def __init__(self) -> None:
        super().__init__("You must have a key file before encrypt or decrypt data,"
                         "see: https://pypi.org/project/cryptography/")


class Crypto:
    def __init__(self) -> None:
        self.__key: bytes = b""

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
