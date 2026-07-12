from rich.console import Console
from rich.panel import Panel


class ConfigResetText:
    @staticmethod
    def display() -> None:
        Console().print(
            Panel(
                "[bold yellow]Configuration reset successfully.[/bold yellow]\n\n"
                "The previous configuration values were replaced with Seekr's "
                "defaults.",
                title="Seekr configuration reset",
                border_style="yellow",
                padding=(1, 2),
            )
        )
