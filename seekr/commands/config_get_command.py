from dataclasses import dataclass
from pathlib import Path

from seekr.config import SeekrConfig
from seekr.security.redact import RedactPath
from seekr.texts.config_show_specific_property import ConfigShowSpecificProperty


@dataclass(frozen=True, slots=True)
class ConfigGetCommandParams:
    key_names: list[str]
    format_output: bool = False


class ConfigGetCommand:
    def __init__(self, params: ConfigGetCommandParams) -> None:
        self.params = params

    def execute(self) -> None:
        config = SeekrConfig.get_instance()
        config_show_specific_property = ConfigShowSpecificProperty()

        for property_name in self.params.key_names:
            property_value = config.get_property(property_name, None)
            if property_name == "ignores":
                ignores = []

                for ignore in property_value.get():
                    if ignore["is_nickname"]:
                        ignores.append(ignore)
                        continue

                    ignores.append(
                        {
                            **ignore,
                            "resource": RedactPath.execute(Path(ignore["resource"])),
                        }
                    )

                config_show_specific_property.add_row(property_name, ignores)
                continue

            config_show_specific_property.add_row(property_name, property_value.get())

        config_show_specific_property.display(self.params.format_output)
