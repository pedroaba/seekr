import json
from dataclasses import dataclass
from typing import Any

from rich import box
from rich.console import Console
from rich.table import Table


@dataclass(frozen=True)
class Row:
    key: str
    value: Any


class ConfigShowSpecificProperty:
    def __init__(self):
        self.__rows: list[Row] = []

    def add_row(self, key: str, value: Any) -> None:
        self.__rows.append(Row(key=key, value=value))

    def display(self, format_output: bool = False) -> None:
        console = Console()

        table = Table(
            title="Seekr Configuration",
            title_style="bold cyan",
            show_header=True,
            header_style="bold bright_cyan",
            box=box.ROUNDED,
            border_style="dim cyan",
            show_lines=True
        )

        table.add_column("Key", style="bold", no_wrap=True)
        table.add_column("Value", overflow="fold")

        for row in self.__rows:
            formatted_value = ConfigShowSpecificProperty._format_value(row.value) \
                                if format_output else str(row.value)

            table.add_row(
                str(row.key),
                formatted_value,
            )

        console.print(table)

    @staticmethod
    def _format_value(value: Any) -> str:
        if isinstance(value, (dict, list, tuple)):
            return json.dumps(value, indent=2, ensure_ascii=False)

        if value is None:
            return "[dim]None[/dim]"

        if isinstance(value, bool):
            return "[green]True[/green]" if value else "[red]False[/red]"

        return str(value)
