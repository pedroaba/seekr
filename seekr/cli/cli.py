import typer

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
        "[dim]  seekr config set ignores --path .venv build[/dim]"
    ),
    no_args_is_help=True,
    add_completion=True,
    pretty_exceptions_enable=True,
    context_settings={"help_option_names": ["-h", "--help"]},
    rich_markup_mode="rich",
)


@app.callback()
def main() -> None:
    pass
