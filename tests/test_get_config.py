import unittest
from pathlib import Path

from seekr.application.use_cases.get_config import GetConfig, GetConfigInput
from tests.fakes import InMemoryConfigRepository, StubPathRedactor


class GetConfigTest(unittest.TestCase):
    def test_it_returns_requested_properties_and_redacts_paths(self) -> None:
        repository = InMemoryConfigRepository(
            {
                "version": "v1",
                "ignores": [
                    {
                        "resource": "/private/client/build",
                        "is_nickname": False,
                        "is_system_path": True,
                    }
                ],
            }
        )
        redactor = StubPathRedactor()

        result = GetConfig(repository, redactor).execute(
            GetConfigInput(key_names=["ignores", "missing"])
        )

        self.assertEqual("redacted:build", result.values["ignores"][0]["resource"])
        self.assertIsNone(result.values["missing"])
        self.assertEqual([Path("/private/client/build")], redactor.calls)

    def test_it_keeps_nickname_ignore_rules_visible(self) -> None:
        repository = InMemoryConfigRepository(
            {
                "ignores": [
                    {
                        "resource": "__pycache__",
                        "is_nickname": True,
                        "is_system_path": False,
                    }
                ]
            }
        )
        redactor = StubPathRedactor()

        result = GetConfig(repository, redactor).execute(
            GetConfigInput(key_names=["ignores"])
        )

        self.assertEqual("__pycache__", result.values["ignores"][0]["resource"])
        self.assertEqual([], redactor.calls)
