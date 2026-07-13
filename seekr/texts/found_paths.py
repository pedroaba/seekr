from dataclasses import dataclass

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from seekr.utils.walker import WalkResult


@dataclass(frozen=True)
class Metadata:
    number_of_paths_showing: int
    total: int

    total_files: int
    total_dirs: int


class FoundPathsText:
    RESULT_COUNT_TEXT = "Showing {number_of_paths_showing} of {total} paths"

    def __init__(self, results: list[WalkResult]):
        self.__results = results

    def display(self, metadata: Metadata | None = None) -> None:
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

        caption = (
            self.RESULT_COUNT_TEXT.format(
                number_of_paths_showing=metadata.number_of_paths_showing,
                total=metadata.total,
            )
            if metadata
            else None
        )

        table = Table(
            title=f"Found paths ({len(self.__results)})",
            title_style="bold cyan",
            header_style="bold bright_cyan",
            box=box.ROUNDED,
            border_style="dim cyan",
            show_lines=True,
            caption=caption,
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
        console.print(self._summary_table(metadata))

    def _summary_table(self, metadata: Metadata | None) -> Table:
        if metadata:
            total_files = metadata.total_files
            total_dirs = metadata.total_dirs
        else:
            total_files = sum(result.is_file for result in self.__results)
            total_dirs = sum(result.is_dir for result in self.__results)

        table = Table(
            title="Mapping summary",
            title_style="bold cyan",
            box=box.ROUNDED,
            border_style="dim cyan",
        )
        table.add_column("Directories", justify="right")
        table.add_column("Files", justify="right")
        table.add_column("Total", justify="right")
        table.add_row(
            str(total_dirs),
            str(total_files),
            str(total_dirs + total_files),
        )
        return table

    @staticmethod
    def _result_type(result: WalkResult) -> str:
        if result.is_dir:
            return "Directory"
        if result.is_file:
            return "File"
        return "Path"
