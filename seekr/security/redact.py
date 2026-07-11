from pathlib import Path


class RedactPath:
    REDACT_STR = "****"

    @staticmethod
    def execute(path_to_redact: Path) -> str:
        absolute_path = path_to_redact.expanduser().absolute()
        home = Path.home().absolute()

        try:
            relative_parts = absolute_path.relative_to(home).parts
        except ValueError:
            return RedactPath._outside_home(absolute_path)

        if not relative_parts:
            return "~"

        if len(relative_parts) <= 2:
            return str(Path("~", *relative_parts))

        return str(
            Path(
                "~",
                relative_parts[0],
                RedactPath.REDACT_STR,
                relative_parts[-1],
            )
        )

    @staticmethod
    def _outside_home(path_to_redact: Path) -> str:
        if path_to_redact == Path(path_to_redact.anchor):
            return path_to_redact.anchor

        return str(
            Path(
                path_to_redact.anchor,
                RedactPath.REDACT_STR,
                path_to_redact.name,
            )
        )
