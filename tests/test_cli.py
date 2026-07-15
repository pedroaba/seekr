from pathlib import Path

from typer.testing import CliRunner

from seekr.cli import cli
from seekr.commands.config_get_command import ConfigGetCommandParams
from seekr.commands.config_init_command import ConfigInitCommandParams
from seekr.commands.config_set_ignores_command import ConfigSetIgnoresCommandParams
from seekr.commands.config_show_command import ConfigShowCommandParams
from seekr.commands.init_command import InitCommandParams
from seekr.commands.search_command import SearchCommandParams

runner = CliRunner()


def capture_command(monkeypatch, command_name):
    calls = []

    class CommandSpy:
        def __init__(self, params):
            calls.append((params, False))

        def execute(self):
            params, _ = calls[-1]
            calls[-1] = (params, True)

    monkeypatch.setattr(cli, command_name, CommandSpy)
    return calls


def test_init_command_receives_params_dataclass(monkeypatch):
    calls = capture_command(monkeypatch, "InitCommand")

    result = runner.invoke(
        cli.app,
        ["init", "--show", "--number-of-paths-showing", "25", "--force"],
    )

    assert result.exit_code == 0
    assert calls == [
        (
            InitCommandParams(
                show_mapped_paths=True,
                number_of_paths_showing=25,
                force=True,
            ),
            True,
        )
    ]


def test_explicit_search_command_receives_params_dataclass(monkeypatch):
    calls = capture_command(monkeypatch, "SearchCommand")

    result = runner.invoke(
        cli.app,
        ["search", "report", "final", "--limit", "5", "--precision", "90"],
    )

    assert result.exit_code == 0
    assert calls == [
        (
            SearchCommandParams(
                query=["report", "final"],
                limit=5,
                precision=90,
            ),
            True,
        )
    ]


def test_implicit_search_receives_params_dataclass(monkeypatch):
    calls = capture_command(monkeypatch, "SearchCommand")

    result = runner.invoke(cli.app, ["faculdade", "engenharia"])

    assert result.exit_code == 0
    assert calls == [
        (
            SearchCommandParams(
                query=["faculdade", "engenharia"],
                limit=10,
                precision=80,
            ),
            True,
        )
    ]


def test_config_init_command_receives_params_dataclass(monkeypatch):
    calls = capture_command(monkeypatch, "ConfigInitCommand")

    result = runner.invoke(cli.app, ["config", "init", "--reset"])

    assert result.exit_code == 0
    assert calls == [(ConfigInitCommandParams(reset=True), True)]


def test_config_show_command_receives_params_dataclass(monkeypatch):
    calls = capture_command(monkeypatch, "ConfigShowCommand")

    result = runner.invoke(cli.app, ["config", "show"])

    assert result.exit_code == 0
    assert calls == [(ConfigShowCommandParams(), True)]


def test_config_get_command_receives_params_dataclass(monkeypatch):
    calls = capture_command(monkeypatch, "ConfigGetCommand")

    result = runner.invoke(cli.app, ["config", "get", "ignores", "--format"])

    assert result.exit_code == 0
    assert calls == [
        (
            ConfigGetCommandParams(
                key_names=["ignores"],
                format_output=True,
            ),
            True,
        )
    ]


def test_config_set_ignores_command_receives_params_dataclass(monkeypatch):
    calls = capture_command(monkeypatch, "ConfigSetIgnoresCommand")

    result = runner.invoke(
        cli.app,
        [
            "config",
            "set",
            "ignores",
            "--path",
            ".venv",
            "--path",
            "build",
            "--path-nickname",
            "__pycache__",
            "--override",
            "--no-commit",
        ],
    )

    assert result.exit_code == 0
    assert calls == [
        (
            ConfigSetIgnoresCommandParams(
                paths=[Path(".venv"), Path("build")],
                nicknames=["__pycache__"],
                override=True,
                no_commit=True,
            ),
            True,
        )
    ]


def test_config_set_ignores_rejects_options_without_a_path(monkeypatch):
    calls = capture_command(monkeypatch, "ConfigSetIgnoresCommand")

    result = runner.invoke(
        cli.app,
        ["config", "set", "ignores", "--override"],
    )

    assert result.exit_code == 2
    assert "Provide at least one path or path nickname" in result.output
    assert calls == []
