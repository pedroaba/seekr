import unittest

from seekr.application.use_cases.initialize_config import (
    InitializeConfig,
    InitializeConfigInput,
    InitializeConfigStatus,
)
from tests.fakes import InMemoryConfigRepository


class InitializeConfigTest(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = InMemoryConfigRepository()
        self.use_case = InitializeConfig(self.repository)

    def test_it_initializes_configuration_preserving_existing_values(self) -> None:
        result = self.use_case.execute(InitializeConfigInput(reset=False))

        self.assertEqual(InitializeConfigStatus.INITIALIZED, result.status)
        self.assertEqual([False], self.repository.initialize_calls)

    def test_it_resets_configuration_when_requested(self) -> None:
        result = self.use_case.execute(InitializeConfigInput(reset=True))

        self.assertEqual(InitializeConfigStatus.RESET, result.status)
        self.assertEqual([True], self.repository.initialize_calls)
