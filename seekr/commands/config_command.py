from seekr.commands.abstract import AbstractCommand


class ConfigCommand(AbstractCommand):
    identifier = "config"
    destination_command = "command"
    destination_description = "Available configuration commands"
    help_text = "Manage Seekr configuration"
    description = (
        "Manage Seekr configuration values, including ignored paths and saved "
        "preferences."
    )
    epilog = (
        "Examples:\n"
        "  seekr config init\n"
        "  seekr config show\n"
        "  seekr config get ignores\n"
        "  seekr config set ignores --path .venv"
    )

    def build(self): ...
