import unittest
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from rich.console import Console

from seekr.models.path import PathModel
from seekr.texts.found_paths import FoundPathsText, Metadata
from seekr.utils.walker import WalkResult


class FoundPathsTextTest(unittest.TestCase):
    def setUp(self):
        self.output = StringIO()
        self.console = Console(
            file=self.output,
            force_terminal=False,
            color_system=None,
            width=120,
        )

    def test_it_displays_the_found_paths_in_a_table(self):
        results = [
            WalkResult(
                location=PathModel(
                    resource="/home/pedro/Documents",
                    path_alias="documents",
                ),
                relative_path=Path("/home/pedro/Documents/report.pdf"),
                is_file=True,
            ),
            WalkResult(
                location=PathModel(
                    resource="/home/pedro/Downloads",
                    path_alias="downloads",
                ),
                relative_path=Path("/home/pedro/Downloads/archive"),
                is_dir=True,
            ),
        ]

        with patch("seekr.texts.found_paths.Console", return_value=self.console):
            FoundPathsText(results).display(
                metadata=Metadata(
                    number_of_paths_showing=2,
                    total=200,
                    total_files=120,
                    total_dirs=80,
                )
            )

        rendered = self.output.getvalue()
        self.assertIn("Found paths", rendered)
        self.assertIn("report.pdf", rendered)
        self.assertIn("archive", rendered)
        self.assertIn("documents", rendered)
        self.assertIn("downloads", rendered)
        self.assertIn("File", rendered)
        self.assertIn("Directory", rendered)
        self.assertIn("Showing 2 of 200 paths", rendered)
        self.assertIn("Mapping summary", rendered)
        self.assertIn("Directories", rendered)
        self.assertIn("Files", rendered)
        self.assertIn("80", rendered)
        self.assertIn("120", rendered)

    def test_it_displays_a_message_when_no_paths_are_found(self):
        with patch("seekr.texts.found_paths.Console", return_value=self.console):
            FoundPathsText([]).display()

        self.assertIn("No paths found", self.output.getvalue())
