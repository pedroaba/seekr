from dataclasses import dataclass
from enum import StrEnum

from seekr.application.ports.config_repository import ConfigRepository


class InitializeConfigStatus(StrEnum):
    INITIALIZED = "initialized"
    RESET = "reset"


@dataclass(frozen=True, slots=True)
class InitializeConfigInput:
    reset: bool = False


@dataclass(frozen=True, slots=True)
class InitializeConfigOutput:
    status: InitializeConfigStatus


class InitializeConfig:
    def __init__(self, repository: ConfigRepository) -> None:
        self._repository = repository

    def execute(self, request: InitializeConfigInput) -> InitializeConfigOutput:
        self._repository.initialize(reset=request.reset)
        status = (
            InitializeConfigStatus.RESET
            if request.reset
            else InitializeConfigStatus.INITIALIZED
        )
        return InitializeConfigOutput(status=status)
