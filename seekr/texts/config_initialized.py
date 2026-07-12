from rich.console import Console
from rich.panel import Panel


class ConfigInitializedText:
    @staticmethod
    def display() -> None:
        Console().print(
            Panel(
                "[bold green]Configuration initialized successfully.[/bold green]\n\n"
                "Existing configuration values were preserved. Nothing is "
                "overwritten unless [bold]--reset[/bold] is provided.",
                title="Seekr configuration",
                border_style="green",
                padding=(1, 2),
            )
        )
