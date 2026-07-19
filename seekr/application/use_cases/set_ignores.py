from dataclasses import dataclass, field
from pathlib import Path

from seekr.application.ports.config_repository import ConfigRepository
from seekr.application.ports.path_services import ExistingPathValidator
from seekr.domain.entities.ignore_rule import IgnoreRule
from seekr.domain.services.nickname_validator import NicknameValidator


@dataclass(frozen=True, slots=True)
class SetIgnoresInput:
    paths: list[Path] = field(default_factory=list)
    nicknames: list[str] = field(default_factory=list)
    override: bool = False
    no_commit: bool = False


@dataclass(frozen=True, slots=True)
class SetIgnoresOutput:
    ignores: list[IgnoreRule]
    committed: bool


class SetIgnores:
    def __init__(
        self,
        repository: ConfigRepository,
        path_validator: ExistingPathValidator,
        nickname_validator: NicknameValidator | None = None,
    ) -> None:
        self._repository = repository
        self._path_validator = path_validator
        self._nickname_validator = nickname_validator or NicknameValidator()

    def execute(self, request: SetIgnoresInput) -> SetIgnoresOutput:
        new_rules = self._build_rules(request)
        config = self._repository.read()
        rules = [] if request.override else self._read_rules(config)
        for rule in new_rules:
            if rule not in rules:
                rules.append(rule)
        config["ignores"] = [rule.to_dict() for rule in rules]
        self._repository.replace(config)
        if not request.no_commit:
            self._repository.commit()
        return SetIgnoresOutput(ignores=rules, committed=not request.no_commit)

    def _build_rules(self, request: SetIgnoresInput) -> list[IgnoreRule]:
        rules = [
            IgnoreRule(
                resource=str(self._path_validator.validate(path)),
                is_system_path=True,
            )
            for path in request.paths
        ]
        rules.extend(
            IgnoreRule(
                resource=self._nickname_validator.validate(nickname),
                is_nickname=True,
            )
            for nickname in request.nicknames
        )
        return rules

    @staticmethod
    def _read_rules(config: dict[str, object]) -> list[IgnoreRule]:
        values = config.get("ignores", [])
        if not isinstance(values, list):
            return []
        return [
            IgnoreRule.from_dict(value) for value in values if isinstance(value, dict)
        ]
