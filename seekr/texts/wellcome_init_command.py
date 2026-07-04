from time import sleep

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from seekr.texts.protocol import TextCommandProtocol


class WellcomeInitCommand(TextCommandProtocol):
    @staticmethod
    def display() -> None:
        console = Console()
        console.print("[bold cyan]Initializing system configuration...[/bold cyan]")
        sleep(0.5)

        welcome_text = Text()
        welcome_text.append("Welcome to ", style="bold white")
        welcome_text.append("Seekr", style="bold cyan")
        welcome_text.append("\n\n")
        welcome_text.append(
            "Seekr will prepare fuzzy search indexing for your main folders:",
            style="white",
        )
        welcome_text.append("\n\n")
        welcome_text.append("• Downloads\n", style="green")
        welcome_text.append("• Documents\n", style="green")
        welcome_text.append("• Images\n", style="green")
        welcome_text.append("• Desktop", style="green")

        console.print(
            Panel(
                welcome_text,
                title="[bold cyan]Seekr Setup[/bold cyan]",
                subtitle="[dim]Local fuzzy file search[/dim]",
                border_style="cyan",
                padding=(1, 2),
            )
        )
