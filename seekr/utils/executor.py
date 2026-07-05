from collections.abc import Callable
from typing import Any


class Executor:
    @staticmethod
    def execute(fn: Callable[[Any], Any] | None, *args, **kwargs):
        if fn is None:
            return None

        return fn(*args, **kwargs)