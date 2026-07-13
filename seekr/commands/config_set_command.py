from seekr.commands.abstract import AbstractCommand


class ConfigSetCommand(AbstractCommand):
    identifier = "set"
    destination_command = "config_key"
    destination_description = "Configuration values that can be changed"
    help_text = "Update configuration values"
    description = (
        "Update a Seekr configuration value. Choose one of the available keys below."
    )
    epilog = "Example:\n  seekr config set ignores --path .venv build"

    def build(self): ...
