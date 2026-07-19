import json
from pathlib import Path
from typing import Any

from rich import box, print_json
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from seekr.application.ports.path_services import PathRedactor
from seekr.application.use_cases.build_index import BuildIndexOutput, BuildIndexStatus
from seekr.application.use_cases.initialize_config import (
    InitializeConfigOutput,
    InitializeConfigStatus,
)
from seekr.application.use_cases.search_paths import SearchPathsOutput
from seekr.application.use_cases.set_ignores import SetIgnoresOutput
from seekr.domain.entities.indexed_path import IndexedPath


class RichCliPresenter:
    def __init__(self, path_redactor: PathRedactor) -> None:
        self._console = Console()
        self._path_redactor = path_redactor

    def display_build_index(
        self,
        result: BuildIndexOutput,
        *,
        show: bool,
        display_limit: int,
    ) -> None:
        if result.status is BuildIndexStatus.ALREADY_EXISTS:
            self._console.print(
                Panel(
                    "[bold yellow]Seekr has already been initialized.[/bold yellow]\n\n"
                    "An existing index was preserved. Use "
                    "[bold cyan]seekr init --force[/bold cyan] to rebuild it.",
                    title="Seekr setup",
                    border_style="yellow",
                )
            )
            return
        self._console.print(
            f"[bold green]Index created:[/bold green] "
            f"{result.total_files} files and {result.total_dirs} directories."
        )
        if show:
            paths = result.paths if display_limit < 0 else result.paths[:display_limit]
            self._display_paths(paths, title="Found paths", include_source=True)

    def display_search(self, result: SearchPathsOutput) -> None:
        if not result.paths:
            self._console.print(
                Panel(
                    "[yellow]No matching paths found.[/yellow]",
                    title="Seekr search",
                    border_style="yellow",
                )
            )
            return
        self._display_paths(result.paths, title="Search results", include_parent=True)

    def display_initialize_config(self, result: InitializeConfigOutput) -> None:
        if result.status is InitializeConfigStatus.RESET:
            message = "[bold yellow]Configuration reset successfully.[/bold yellow]"
            title = "Seekr configuration reset"
        else:
            message = "[bold green]Configuration initialized successfully.[/bold green]"
            title = "Seekr configuration"
        self._console.print(Panel(message, title=title))

    def display_config(self, config: dict[str, Any]) -> None:
        print_json(json.dumps(config, indent=4))

    def display_config_values(
        self,
        values: dict[str, Any],
        *,
        formatted: bool,
    ) -> None:
        table = Table(title="Seekr Configuration", box=box.ROUNDED, show_lines=True)
        table.add_column("Key", style="bold")
        table.add_column("Value", overflow="fold")
        for key, value in values.items():
            rendered = (
                json.dumps(value, indent=2, ensure_ascii=False)
                if formatted and isinstance(value, dict | list | tuple)
                else str(value)
            )
            table.add_row(key, rendered)
        self._console.print(table)

    def display_set_ignores(self, result: SetIgnoresOutput) -> None:
        if result.committed:
            self._console.print("[green]Ignore rules saved.[/green]")
            return
        self._console.print(
            "[yellow]Changes were applied in memory but were not saved.[/yellow]"
        )

    def _display_paths(
        self,
        paths: list[IndexedPath],
        *,
        title: str,
        include_source: bool = False,
        include_parent: bool = False,
    ) -> None:
        table = Table(
            title=f"{title} ({len(paths)})",
            box=box.ROUNDED,
            show_lines=True,
        )
        table.add_column("#", justify="right", style="dim")
        if include_source:
            table.add_column("Source")
        table.add_column("Type")
        table.add_column("Path", overflow="fold")
        if include_parent:
            table.add_column("Parent", overflow="fold")
        table.add_column("Modified")
        for position, result in enumerate(paths, start=1):
            row = [str(position)]
            if include_source:
                row.append(result.source_alias or Path(result.parent_path).name)
            row.extend(
                [
                    self._path_type(result),
                    self._path_redactor.redact(Path(result.filepath)),
                ]
            )
            if include_parent:
                row.append(self._path_redactor.redact(Path(result.parent_path)))
            row.append(result.modified_path_at.strftime("%Y-%m-%d %H:%M"))
            table.add_row(*row)
        self._console.print(table)

    @staticmethod
    def _path_type(path: IndexedPath) -> str:
        if path.is_folder:
            return "Directory"
        if path.is_file:
            return "File"
        return "Path"
