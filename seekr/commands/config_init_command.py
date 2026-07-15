from dataclasses import dataclass

from seekr.config import SeekrConfig
from seekr.texts.config_initialized import ConfigInitializedText
from seekr.texts.config_reset import ConfigResetText


@dataclass(frozen=True, slots=True)
class ConfigInitCommandParams:
    reset: bool = False


class ConfigInitCommand:
    def __init__(self, params: ConfigInitCommandParams) -> None:
        self.params = params

    def execute(self) -> None:
        config = SeekrConfig.get_instance()
        config.build(reset=self.params.reset)

        if self.params.reset:
            ConfigResetText.display()
            return

        ConfigInitializedText.display()
