from rich.console import Console
from rich.panel import Panel


class CommitDisabledWarningText:
    @staticmethod
    def display() -> None:
        Console().print(
            Panel(
                "[bold yellow]Commit disabled[/bold yellow]\n\n"
                "The configuration changes were not saved to the configuration file.\n"
                "[dim]They are being used only in memory and will be lost "
                "when the program exits or the computer is restarted.[/dim]",
                title="Temporary configuration",
                border_style="yellow",
                padding=(1, 2),
            )
        )
