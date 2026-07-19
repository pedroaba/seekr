from pathlib import Path
from typing import Annotated, cast

import typer
from typer.core import TyperCommand, TyperGroup

from seekr.adapters.inbound.cli.presenter import RichCliPresenter
from seekr.application.use_cases.build_index import BuildIndexInput
from seekr.application.use_cases.get_config import GetConfigInput
from seekr.application.use_cases.initialize_config import InitializeConfigInput
from seekr.application.use_cases.search_paths import SearchPathsInput
from seekr.application.use_cases.set_ignores import SetIgnoresInput
from seekr.bootstrap import ApplicationContainer


class SeekrGroup(TyperGroup):
    def resolve_command(
        self,
        ctx: typer.Context,
        args: list[str],
    ) -> tuple[str | None, TyperCommand | TyperGroup | None, list[str]]:
        if args and not args[0].startswith("-"):
            requested_command = self.get_command(ctx, args[0])
            if requested_command is None:
                search_command = self.get_command(ctx, "search")
                if search_command is not None:
                    return "search", cast(TyperCommand, search_command), args

        return cast(
            tuple[str | None, TyperCommand | TyperGroup | None, list[str]],
            super().resolve_command(ctx, args),
        )


class CliApplication:
    CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"]}

    def __init__(
        self,
        container: ApplicationContainer | None = None,
        presenter: RichCliPresenter | None = None,
    ) -> None:
        self._container = container or ApplicationContainer()
        self._presenter = presenter or RichCliPresenter(self._container.path_redactor())
        self.app = typer.Typer(
            name="seekr",
            help="Find indexed files and directories with fuzzy search.",
            no_args_is_help=True,
            add_completion=True,
            context_settings=self.CONTEXT_SETTINGS,
            rich_markup_mode="rich",
            cls=SeekrGroup,
        )
        self._config_app = typer.Typer(
            help="Manage Seekr configuration.",
            no_args_is_help=True,
            context_settings=self.CONTEXT_SETTINGS,
        )
        self._config_set_app = typer.Typer(
            help="Update Seekr configuration values.",
            no_args_is_help=True,
            context_settings=self.CONTEXT_SETTINGS,
        )
        self._register_commands()

    def _register_commands(self) -> None:
        self.app.add_typer(self._config_app, name="config")
        self._config_app.add_typer(self._config_set_app, name="set")
        self.app.command(name="init", help="Scan the default user folders.")(
            self.initialize_index
        )
        self.app.command(name="search", help="Search indexed paths.")(self.search)
        self._config_app.command(name="init")(self.initialize_configuration)
        self._config_app.command(name="show")(self.show_configuration)
        self._config_app.command(name="get")(self.get_configuration)
        self._config_set_app.command(name="ignores")(self.set_configuration_ignores)

    def initialize_index(
        self,
        show: Annotated[bool, typer.Option("-s", "--show")] = False,
        number_of_paths_showing: Annotated[
            int,
            typer.Option("-n", "--number-of-paths-showing"),
        ] = 10,
        force: Annotated[bool, typer.Option("--force")] = False,
    ) -> None:
        result = self._container.build_index().execute(BuildIndexInput(force=force))
        self._presenter.display_build_index(
            result,
            show=show,
            display_limit=number_of_paths_showing,
        )

    def search(
        self,
        query: Annotated[list[str], typer.Argument(metavar="QUERY")],
        limit: Annotated[int, typer.Option("-l", "--limit")] = 10,
        precision: Annotated[
            int,
            typer.Option("--precision", min=0, max=100),
        ] = 80,
    ) -> None:
        result = self._container.search_paths().execute(
            SearchPathsInput(query=query, limit=limit, precision=precision)
        )
        self._presenter.display_search(result)

    def initialize_configuration(
        self,
        reset: Annotated[bool, typer.Option("-r", "--reset")] = False,
    ) -> None:
        result = self._container.initialize_config().execute(
            InitializeConfigInput(reset=reset)
        )
        self._presenter.display_initialize_config(result)

    def show_configuration(self) -> None:
        result = self._container.show_config().execute()
        self._presenter.display_config(result.config)

    def get_configuration(
        self,
        key_names: Annotated[list[str], typer.Argument(metavar="KEY")],
        format_output: Annotated[
            bool,
            typer.Option("-f", "--format"),
        ] = False,
    ) -> None:
        result = self._container.get_config().execute(
            GetConfigInput(key_names=key_names)
        )
        self._presenter.display_config_values(
            result.values,
            formatted=format_output,
        )

    def set_configuration_ignores(
        self,
        paths: Annotated[list[Path] | None, typer.Option("-p", "--path")] = None,
        nicknames: Annotated[
            list[str] | None,
            typer.Option("-pn", "--path-nickname"),
        ] = None,
        override: Annotated[bool, typer.Option("-o", "--override")] = False,
        no_commit: Annotated[bool, typer.Option("--no-commit")] = False,
    ) -> None:
        if not paths and not nicknames:
            raise typer.BadParameter("Provide at least one path or path nickname.")
        result = self._container.set_ignores().execute(
            SetIgnoresInput(
                paths=paths or [],
                nicknames=nicknames or [],
                override=override,
                no_commit=no_commit,
            )
        )
        self._presenter.display_set_ignores(result)
