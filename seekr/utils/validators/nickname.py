import re


class NicknameValidator:
    MAX_LENGTH = 255

    _DIRECTORY_TOKENS = {".", ".."}
    _UNSAFE_PATTERN = re.compile(r"[/\\*?\[\]]")
    _CONTROL_CHARACTER_PATTERN = re.compile(r"[\x00-\x1f\x7f]")

    def __init__(self, nickname: str):
        self._value = nickname

    def validate(self) -> str:
        nickname = self._value.strip()

        if not nickname:
            raise ValueError("Nickname cannot be empty.")

        if nickname in self._DIRECTORY_TOKENS:
            raise ValueError("Nickname cannot be a directory token.")

        if len(nickname) > self.MAX_LENGTH:
            raise ValueError(f"Nickname cannot exceed {self.MAX_LENGTH} characters.")

        if self._UNSAFE_PATTERN.search(nickname):
            raise ValueError(
                "Nickname cannot contain path separators or glob characters."
            )

        if self._CONTROL_CHARACTER_PATTERN.search(nickname):
            raise ValueError("Nickname cannot contain control characters.")

        self._value = nickname
        return nickname
