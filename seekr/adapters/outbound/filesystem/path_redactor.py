from pathlib import Path

from seekr.application.ports.path_services import PathRedactor


class HomePathRedactor(PathRedactor):
    REDACTION = "****"

    def redact(self, path: Path) -> str:
        absolute = path.expanduser().resolve()
        home = Path.home().resolve()
        try:
            relative_parts = absolute.relative_to(home).parts
        except ValueError:
            return self._outside_home(absolute)
        if not relative_parts:
            return "~"
        if len(relative_parts) <= 2:
            return str(Path("~", *relative_parts))
        return str(Path("~", relative_parts[0], self.REDACTION, relative_parts[-1]))

    def _outside_home(self, path: Path) -> str:
        if path == Path(path.anchor):
            return path.anchor
        return str(Path(path.anchor, self.REDACTION, path.name))
