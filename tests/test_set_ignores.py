import unittest
from pathlib import Path

from seekr.application.use_cases.set_ignores import SetIgnores, SetIgnoresInput
from tests.fakes import InMemoryConfigRepository, StubPathValidator


class SetIgnoresTest(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = InMemoryConfigRepository({"version": "v1", "ignores": []})
        self.validator = StubPathValidator()
        self.use_case = SetIgnores(self.repository, self.validator)

    def test_it_validates_and_appends_path_and_nickname_rules(self) -> None:
        result = self.use_case.execute(
            SetIgnoresInput(
                paths=[Path("build")],
                nicknames=["  __pycache__  "],
            )
        )

        self.assertEqual(2, len(result.ignores))
        self.assertEqual("/validated/build", result.ignores[0].resource)
        self.assertTrue(result.ignores[0].is_system_path)
        self.assertEqual("__pycache__", result.ignores[1].resource)
        self.assertTrue(result.ignores[1].is_nickname)
        self.assertEqual([Path("build")], self.validator.calls)
        self.assertEqual(1, self.repository.commit_count)

    def test_it_does_not_add_duplicate_rules(self) -> None:
        self.repository.data["ignores"] = [
            {
                "resource": "__pycache__",
                "is_nickname": True,
                "is_system_path": False,
            }
        ]

        result = self.use_case.execute(SetIgnoresInput(nicknames=["__pycache__"]))

        self.assertEqual(1, len(result.ignores))

    def test_it_replaces_existing_rules_when_override_is_enabled(self) -> None:
        self.repository.data["ignores"] = [
            {
                "resource": "old",
                "is_nickname": True,
                "is_system_path": False,
            }
        ]

        result = self.use_case.execute(
            SetIgnoresInput(nicknames=["new"], override=True)
        )

        self.assertEqual(["new"], [rule.resource for rule in result.ignores])

    def test_it_updates_memory_without_committing_when_requested(self) -> None:
        result = self.use_case.execute(
            SetIgnoresInput(nicknames=["cache"], no_commit=True)
        )

        self.assertFalse(result.committed)
        self.assertEqual(0, self.repository.commit_count)
        self.assertEqual("cache", self.repository.data["ignores"][0]["resource"])

    def test_it_rejects_an_unsafe_nickname(self) -> None:
        with self.assertRaisesRegex(ValueError, "glob characters"):
            self.use_case.execute(SetIgnoresInput(nicknames=["../cache*"]))
