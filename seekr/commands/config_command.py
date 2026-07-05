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

    def build(self): ...
