import re
import unicodedata
from pathlib import Path


def normalize_path(path: str | Path) -> str:
    if isinstance(path, str):
        path = Path(path)

    normalized_path = str(
        path.absolute().resolve()
    ).strip().lower()

    normalized_path = unicodedata.normalize("NFKD", normalized_path)
    normalized_path = re.sub(r"/", " ", normalized_path)

    return normalized_path
