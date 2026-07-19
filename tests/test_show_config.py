import unittest
from pathlib import Path

from seekr.application.use_cases.show_config import ShowConfig
from tests.fakes import InMemoryConfigRepository, StubPathRedactor


class ShowConfigTest(unittest.TestCase):
    def test_it_redacts_filesystem_ignore_rules_without_mutating_config(self) -> None:
        original = {
            "version": "v1",
            "ignores": [
                {
                    "resource": "/private/client/build",
                    "is_nickname": False,
                    "is_system_path": True,
                },
                {
                    "resource": "__pycache__",
                    "is_nickname": True,
                    "is_system_path": False,
                },
            ],
        }
        repository = InMemoryConfigRepository(original)
        redactor = StubPathRedactor()

        result = ShowConfig(repository, redactor).execute()

        self.assertEqual("redacted:build", result.config["ignores"][0]["resource"])
        self.assertEqual("__pycache__", result.config["ignores"][1]["resource"])
        self.assertEqual(original, repository.data)
        self.assertEqual([Path("/private/client/build")], redactor.calls)
