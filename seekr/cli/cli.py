from pathlib import Path
from typing import Annotated

import typer
from typer import _click
from typer.core import TyperGroup

from seekr.commands.config_get_command import ConfigGetCommand, ConfigGetCommandParams
from seekr.commands.config_init_command import (
    ConfigInitCommand,
    ConfigInitCommandParams,
)
from seekr.commands.config_set_ignores_command import (
    ConfigSetIgnoresCommand,
    ConfigSetIgnoresCommandParams,
)
from seekr.commands.config_show_command import (
    ConfigShowCommand,
    ConfigShowCommandParams,
)
from seekr.commands.init_command import InitCommand, InitCommandParams
from seekr.commands.search_command import SearchCommand, SearchCommandParams

HELP_CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"]}


class SeekrGroup(TyperGroup):
    def resolve_command(
        self, ctx: _click.Context, args: list[str]
    ) -> tuple[str | None, _click.Command | None, list[str]]:
        try:
            return super().resolve_command(ctx, args)
        except _click.exceptions.UsageError:
            if args and not args[0].startswith("-"):
                search_command = self.get_command(ctx, "search")
                if search_command is not None:
                    return "search", search_command, args
            raise


app = typer.Typer(
    name="seekr",
    help=(
        "Find indexed files and directories with fuzzy search, rebuild the "
        "local index, and manage Seekr configuration."
    ),
    epilog=(
        "[bold]Examples:[/bold]\n\n"
        "[dim]  seekr faculdade trabalho final[/dim]\n\n"
        "[dim]  seekr init --show[/dim]\n\n"
        "[dim]  seekr config show[/dim]\n\n"
        "[dim]  seekr config set ignores --path .venv --path build[/dim]"
    ),
    no_args_is_help=True,
    add_completion=True,
    pretty_exceptions_enable=True,
    context_settings=HELP_CONTEXT_SETTINGS,
    rich_markup_mode="rich",
    cls=SeekrGroup,
)

config_app = typer.Typer(
    help="Manage Seekr configuration.",
    epilog=(
        "[bold]Examples:[/bold]\n\n"
        "[dim]  seekr config init[/dim]\n\n"
        "[dim]  seekr config show[/dim]\n\n"
        "[dim]  seekr config get ignores[/dim]\n\n"
        "[dim]  seekr config set ignores --path .venv[/dim]"
    ),
    no_args_is_help=True,
    context_settings=HELP_CONTEXT_SETTINGS,
    rich_markup_mode="rich",
)

config_set_app = typer.Typer(
    help="Update Seekr configuration values.",
    epilog=(
        "[bold]Example:[/bold]\n\n"
        "[dim]  seekr config set ignores --path .venv --path build[/dim]"
    ),
    no_args_is_help=True,
    context_settings=HELP_CONTEXT_SETTINGS,
    rich_markup_mode="rich",
)

app.add_typer(config_app, name="config")
config_app.add_typer(config_set_app, name="set")


@app.callback()
def main() -> None:
    pass


@app.command(
    name="init",
    help="Scan the default user folders.",
    epilog=(
        "[bold]Examples:[/bold]\n\n"
        "[dim]  seekr init[/dim]\n\n"
        "[dim]  seekr init --show[/dim]\n\n"
        "[dim]  seekr init --show --number-of-paths-showing 25[/dim]\n\n"
        "[dim]  seekr init --force[/dim]"
    ),
)
def init_root_command(
    show_mapped_paths: Annotated[
        bool,
        typer.Option(
            "-s",
            "--show",
            help="Display the files and directories found during the scan.",
        ),
    ] = False,
    number_of_paths_showing: Annotated[
        int,
        typer.Option(
            "-n",
            "--number-of-paths-showing",
            metavar="COUNT",
            help="Maximum paths displayed with --show. Use -1 to display all.",
        ),
    ] = 10,
    force: Annotated[
        bool,
        typer.Option(
            "--force",
            help="Discard the existing index and scan the default folders again.",
        ),
    ] = False,
) -> None:
    params = InitCommandParams(
        show_mapped_paths=show_mapped_paths,
        number_of_paths_showing=number_of_paths_showing,
        force=force,
    )
    InitCommand(params).execute()


@app.command(
    name="search",
    help="Search indexed files and directories.",
    epilog=(
        "[bold]Examples:[/bold]\n\n"
        "[dim]  seekr report final[/dim]\n\n"
        "[dim]  seekr search faculdade engenharia[/dim]"
    ),
)
def search_root_command(
    query: Annotated[
        list[str],
        typer.Argument(
            metavar="QUERY",
            help="One or more terms to match against indexed paths.",
        ),
    ],
    limit: Annotated[
        int,
        typer.Option(
            "-l",
            "--limit",
            metavar="COUNT",
            help="Maximum number of matching paths to display.",
        ),
    ] = 10,
    precision: Annotated[
        int,
        typer.Option(
            "--precision",
            metavar="SCORE",
            min=0,
            max=100,
            help="Minimum fuzzy-match score required, from 0 to 100.",
        ),
    ] = 80,
) -> None:
    params = SearchCommandParams(
        query=query,
        limit=limit,
        precision=precision,
    )
    SearchCommand(params).execute()


@config_app.command(
    name="init",
    help="Initialize the local configuration.",
    epilog=(
        "[bold]Examples:[/bold]\n\n"
        "[dim]  seekr config init[/dim]\n\n"
        "[dim]  seekr config init --reset[/dim]"
    ),
)
def config_init_command(
    reset: Annotated[
        bool,
        typer.Option(
            "-r",
            "--reset",
            help="Replace existing configuration values with Seekr's defaults.",
        ),
    ] = False,
) -> None:
    ConfigInitCommand(ConfigInitCommandParams(reset=reset)).execute()


@config_app.command(
    name="show",
    help="Show the current configuration.",
    epilog=("[bold]Example:[/bold]\n\n[dim]  seekr config show[/dim]"),
)
def config_show_command() -> None:
    ConfigShowCommand(ConfigShowCommandParams()).execute()


@config_app.command(
    name="get",
    help="Read specific configuration values.",
    epilog=(
        "[bold]Examples:[/bold]\n\n"
        "[dim]  seekr config get ignores[/dim]\n\n"
        "[dim]  seekr config get ignores --format[/dim]"
    ),
)
def config_get_command(
    key_names: Annotated[
        list[str],
        typer.Argument(
            metavar="KEY",
            help="One or more configuration keys to display, such as ignores.",
        ),
    ],
    format_output: Annotated[
        bool,
        typer.Option(
            "-f",
            "--format",
            help="Format structured values as indented JSON.",
        ),
    ] = False,
) -> None:
    params = ConfigGetCommandParams(
        key_names=key_names,
        format_output=format_output,
    )
    ConfigGetCommand(params).execute()


@config_set_app.command(
    name="ignores",
    help="Configure ignored paths and path nicknames.",
    no_args_is_help=True,
    epilog=(
        "[bold]Examples:[/bold]\n\n"
        "[dim]  seekr config set ignores --path .venv --path build[/dim]\n\n"
        "[dim]  seekr config set ignores --path-nickname __pycache__[/dim]\n\n"
        "[dim]  seekr config set ignores --override --path dist[/dim]"
    ),
)
def config_set_ignores_command(
    paths: Annotated[
        list[Path] | None,
        typer.Option(
            "-p",
            "--path",
            help=(
                "Filesystem path to ignore. Repeat the option to provide more "
                "than one path."
            ),
        ),
    ] = None,
    nicknames: Annotated[
        list[str] | None,
        typer.Option(
            "-pn",
            "--path-nickname",
            help=(
                "Path nickname or pattern to ignore. Repeat the option to provide "
                "more than one nickname."
            ),
        ),
    ] = None,
    override: Annotated[
        bool,
        typer.Option(
            "-o",
            "--override",
            help="Replace the current ignore list instead of appending to it.",
        ),
    ] = False,
    no_commit: Annotated[
        bool,
        typer.Option(
            "--no-commit",
            help="Apply the change in memory without saving it to disk.",
        ),
    ] = False,
) -> None:
    if not paths and not nicknames:
        raise typer.BadParameter("Provide at least one path or path nickname.")

    params = ConfigSetIgnoresCommandParams(
        paths=paths or [],
        nicknames=nicknames or [],
        override=override,
        no_commit=no_commit,
    )
    ConfigSetIgnoresCommand(params).execute()
