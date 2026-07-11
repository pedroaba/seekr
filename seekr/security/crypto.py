import json

from cryptography.fernet import Fernet

from seekr.enconder import InternalJsonEncoder


class NoCryptKeyException(AttributeError):
    def __init__(self) -> None:
        super().__init__("You must have a key file before encrypt or decrypt data,"
                         "see: https://pypi.org/project/cryptography/")


class Crypto:
    def __init__(self, key: bytes | None = None) -> None:
        self.__key = key or b""

    @property
    def key(self) -> bytes:
        if self.__key is None or self.__key == b"":
            raise NoCryptKeyException()

        return self.__key

    def initialize(self) -> None:
        if self.__key is not None and self.__key != b"":
            return

        fernet = Fernet.generate_key()
        self.__key = fernet

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
