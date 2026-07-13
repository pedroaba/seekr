from pathlib import Path

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from seekr.database.models import PathModel
from seekr.security.redact import RedactPath


class SearchResultsText:
    def __init__(self, results: list[PathModel]):
        self.__results = results

    def display(self) -> None:
        console = Console()

        if not self.__results:
            console.print(
                Panel(
                    "[yellow]No matching paths found.[/yellow]",
                    title="Seekr search",
                    border_style="yellow",
                )
            )
            return

        table = Table(
            title=f"Search results ({len(self.__results)})",
            title_style="bold cyan",
            header_style="bold bright_cyan",
            box=box.ROUNDED,
            border_style="dim cyan",
            show_lines=True,
        )
        table.add_column("#", justify="right", style="dim", no_wrap=True)
        table.add_column("Type", no_wrap=True)
        table.add_column("Path", overflow="fold")
        table.add_column("Parent", overflow="fold")
        table.add_column("Modified", no_wrap=True)

        for position, result in enumerate(self.__results, start=1):
            table.add_row(
                str(position),
                self._result_type(result),
                RedactPath.execute(Path(result.filepath)),
                RedactPath.execute(Path(result.parent_path)),
                result.modified_path_at.strftime("%Y-%m-%d %H:%M"),
            )

        console.print(table)

    @staticmethod
    def _result_type(result: PathModel) -> str:
        if result.is_folder:
            return "Directory"
        if result.is_file:
            return "File"
        return "Path"
