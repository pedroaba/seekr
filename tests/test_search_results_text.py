from datetime import datetime
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from rich.console import Console

from seekr.database.models import PathModel
from seekr.texts.search_results import SearchResultsText


def _console(output: StringIO) -> Console:
    return Console(
        file=output,
        force_terminal=False,
        color_system=None,
        width=120,
    )


def test_display_search_results_in_a_table():
    output = StringIO()
    results = [
        PathModel(
            filepath="/home/user/Documents/report.pdf",
            parent_path="/home/user/Documents",
            normalized_filepath="home user documents report pdf",
            is_folder=False,
            is_file=True,
            modified_path_at=datetime(2026, 7, 13, 14, 30),
            version=1,
        ),
        PathModel(
            filepath="/home/user/Documents/projects",
            parent_path="/home/user/Documents",
            normalized_filepath="home user documents projects",
            is_folder=True,
            is_file=False,
            modified_path_at=datetime(2026, 7, 12, 10, 15),
            version=1,
        ),
    ]

    with (
        patch("seekr.texts.search_results.Console", return_value=_console(output)),
        patch(
            "seekr.security.redact.Path.home",
            return_value=Path("/home/user"),
        ),
    ):
        SearchResultsText(results).display()

    rendered = output.getvalue()
    assert "Search results (2)" in rendered
    assert "report.pdf" in rendered
    assert "projects" in rendered
    assert "Parent" in rendered
    assert "~/Documents" in rendered
    assert "/home/user" not in rendered
    assert "File" in rendered
    assert "Directory" in rendered
    assert "2026-07-13 14:30" in rendered


def test_display_message_when_no_search_results_are_found():
    output = StringIO()

    with patch(
        "seekr.texts.search_results.Console", return_value=_console(output)
    ):
        SearchResultsText([]).display()

    assert "No matching paths found" in output.getvalue()
