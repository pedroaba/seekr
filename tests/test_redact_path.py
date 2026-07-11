import unittest
from pathlib import Path
from unittest.mock import patch

from seekr.security.redact import RedactPath


class RedactPathTest(unittest.TestCase):
    def setUp(self):
        self.home = Path("/home/pedro")

    def test_it_redacts_sensitive_directories_below_the_home(self):
        path = self.home / "repositories" / "client-x" / "secrets"

        with patch("seekr.security.redact.Path.home", return_value=self.home):
            result = RedactPath.execute(path)

        self.assertEqual(
            f"~/repositories/{RedactPath.REDACT_STR}/secrets",
            result,
        )

    def test_it_redacts_an_absolute_path_outside_the_home(self):
        path = Path("/srv/private-company/client-x/secrets")

        with patch("seekr.security.redact.Path.home", return_value=self.home):
            result = RedactPath.execute(path)

        self.assertEqual(f"/{RedactPath.REDACT_STR}/secrets", result)
        self.assertNotIn("private-company", result)
        self.assertNotIn("client-x", result)

    def test_it_preserves_a_file_directly_below_the_home(self):
        path = self.home / "config.json"

        with patch("seekr.security.redact.Path.home", return_value=self.home):
            result = RedactPath.execute(path)

        self.assertEqual("~/config.json", result)

    def test_it_represents_the_home_directory_with_a_tilde(self):
        with patch("seekr.security.redact.Path.home", return_value=self.home):
            result = RedactPath.execute(self.home)

        self.assertEqual("~", result)

    def test_it_converts_a_relative_path_to_an_obfuscated_absolute_path(self):
        relative_path = Path("client-x/secrets")
        working_directory = Path.cwd()

        with patch(
            "seekr.security.redact.Path.home",
            return_value=working_directory.parent,
        ):
            result = RedactPath.execute(relative_path)

        self.assertEqual(
            f"~/{working_directory.name}/{RedactPath.REDACT_STR}/secrets",
            result,
        )

    def test_it_handles_the_filesystem_root(self):
        with patch("seekr.security.redact.Path.home", return_value=self.home):
            result = RedactPath.execute(Path("/"))

        self.assertEqual("/", result)
