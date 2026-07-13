from rich.console import Console
from rich.panel import Panel

from seekr.texts.protocol import TextCommandProtocol


class InitAlreadyCompletedText(TextCommandProtocol):
    @staticmethod
    def display() -> None:
        Console().print(
            Panel(
                "[bold yellow]Seekr has already been initialized.[/bold yellow]\n\n"
                "An existing file and directory index was found. To protect "
                "your current data, Seekr preserved it and skipped the scan.\n\n"
                "To discard the existing index and scan your folders again, run:\n"
                "[bold cyan]seekr init --force[/bold cyan]",
                title="Seekr setup",
                border_style="yellow",
                padding=(1, 2),
            )
        )
