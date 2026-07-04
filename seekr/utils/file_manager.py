from collections.abc import Callable
from pathlib import Path
from typing import Any


class FileManager:
   def __init__(self, filepath: Path) -> None:
       self._encrypt_fn = lambda _: _
       self._decrypt_fn = lambda _: _
       self._filepath = filepath

   def set_encrypt_fn(self, encrypt_fn: Callable[[Any], bytes]) -> None:
       self._encrypt_fn = encrypt_fn

   def set_decrypt_fn(self, decrypt_fn: Callable[[bytes], Any]) -> None:
       self._decrypt_fn = decrypt_fn

   def write(self, data: Any):
       content_to_write = self._encrypt_fn(data)

       with self._filepath.open("wb") as file:
           file.write(content_to_write)

   def read(self) -> Any:
       content = None
       with self._filepath.open("rb") as file:
           content = self._decrypt_fn(file.read())
       return content
