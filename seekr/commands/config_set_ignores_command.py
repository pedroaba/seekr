from dataclasses import dataclass, field
from pathlib import Path

from seekr.config import SeekrConfig
from seekr.models.path import PathModel
from seekr.texts.commit_disable_warning import CommitDisabledWarningText
from seekr.utils.validators.nickname import NicknameValidator
from seekr.utils.validators.path import PathValidator


@dataclass(frozen=True, slots=True)
class ConfigSetIgnoresCommandParams:
    paths: list[Path] = field(default_factory=list)
    nicknames: list[str] = field(default_factory=list)
    override: bool = False
    no_commit: bool = False


class ConfigSetIgnoresCommand:
    def __init__(self, params: ConfigSetIgnoresCommandParams) -> None:
        self.params = params

    def execute(self) -> None:
        ignores_patterns: list[PathModel] = []

        for path in self.params.paths:
            path_str = str(PathValidator(path).validate())
            ignores_patterns.append(PathModel(path_str, is_system_path=True))

        for nickname in self.params.nicknames:
            validated_nickname = NicknameValidator(nickname).validate()
            ignores_patterns.append(PathModel(validated_nickname, is_nickname=True))

        config = SeekrConfig.get_instance()

        if self.params.override:
            config.set_property("ignores", ignores_patterns)
        else:
            ignores_patterns_saved: list[PathModel] = (
                config.get_property("ignores", defaults=[])
                .map(lambda _, value, __: PathModel.from_json(value))
                .get()
            )

            for path_to_add in ignores_patterns:
                if path_to_add not in ignores_patterns_saved:
                    ignores_patterns_saved.append(path_to_add)

            config.set_property("ignores", ignores_patterns_saved)

        if self.params.no_commit:
            CommitDisabledWarningText.display()
            return

        config.commit()
