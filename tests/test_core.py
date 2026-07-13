from seekr.core import SeekrCli


def test_parse_query_without_search_command():
    cli = SeekrCli()

    cli.parse(["first", "second"])

    assert cli._arguments.query == ["first", "second"]


def test_parse_does_not_treat_an_existing_command_as_a_query():
    cli = SeekrCli()

    cli.parse(["init", "--show"])

    assert cli._arguments.show_mapped_paths is True
