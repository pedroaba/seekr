from typing import TYPE_CHECKING

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

if TYPE_CHECKING:
    from seekr.utils.walker import WalkResult


class FoundPathsText:
    RESULT_COUNT_TEXT = "Showing 10 of 200 paths"

    def __init__(self, results: list[WalkResult]):
        self.__results = results

    def display(self) -> None:
        console = Console()

        if not self.__results:
            console.print(
                Panel(
                    "[yellow]No paths found.[/yellow]",
                    title="Seekr scan",
                    border_style="yellow",
                )
            )
            return

        table = Table(
            title=f"Found paths ({len(self.__results)})",
            title_style="bold cyan",
            header_style="bold bright_cyan",
            box=box.ROUNDED,
            border_style="dim cyan",
            show_lines=True,
            caption=self.RESULT_COUNT_TEXT,
            caption_style="dim",
        )
        table.add_column("Source", style="bold", no_wrap=True)
        table.add_column("Type", no_wrap=True)
        table.add_column("Path", overflow="fold")

        for result in self.__results:
            table.add_row(
                result.location.alias,
                self._result_type(result),
                str(result.relative_path),
            )

        console.print(table)

    @staticmethod
    def _result_type(result: WalkResult) -> str:
        if result.is_dir:
            return "Directory"
        if result.is_file:
            return "File"
        return "Path"
