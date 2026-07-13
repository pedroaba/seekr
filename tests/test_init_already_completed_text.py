from rich.console import Console

from seekr.texts.init_already_completed import InitAlreadyCompletedText


def test_it_displays_a_message_when_seekr_is_already_initialized(monkeypatch):
    console = Console(record=True)
    monkeypatch.setattr(
        "seekr.texts.init_already_completed.Console",
        lambda: console,
    )

    InitAlreadyCompletedText.display()

    output = console.export_text()
    assert "Seekr has already been initialized." in output
    assert "Seekr preserved it and skipped the scan." in output
    assert "seekr init --force" in output
