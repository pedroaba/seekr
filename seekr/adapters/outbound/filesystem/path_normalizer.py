import re
import unicodedata
from pathlib import Path


class PathNormalizer:
    @staticmethod
    def normalize(path: str | Path) -> str:
        resolved = Path(path).absolute().resolve()
        normalized = unicodedata.normalize("NFKD", str(resolved).strip().lower())
        return re.sub(r"/", " ", normalized)
