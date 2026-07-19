from datetime import datetime
from typing import Any


class DefaultConfigFactory:
    @staticmethod
    def create(self) -> dict[str, Any]:
        now = datetime.now().isoformat(sep=" ")
        return {
            "version": "v1",
            "created_at": now,
            "updated_at": now,
            "ignores": [],
        }
