from platform import system

from rich.console import Console, Group
from rich.panel import Panel
from rich.rule import Rule
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text


class KeyringTroubleshootingText:
    @staticmethod
    def display(
        error: str | None = None,
        diagnose_output: str | None = None,
    ) -> None:
        console = Console()
        os_name = system()

        console.print(
            Panel.fit(
                Text(
                    "Keyring backend unavailable or misconfigured",
                    style="bold red",
                ),
                border_style="red",
            )
        )

        if error:
            console.print(
                Panel(
                    error,
                    title="Error",
                    title_align="left",
                    border_style="red",
                )
            )

        if diagnose_output:
            console.print(
                Panel(
                    diagnose_output,
                    title="keyring diagnose output",
                    title_align="left",
                    border_style="yellow",
                )
            )

        console.print(Rule("[bold cyan]How to fix it[/bold cyan]"))

        steps = Table(
            show_header=True,
            header_style="bold cyan",
            border_style="dim",
            expand=True,
        )

        steps.add_column("#", style="bold", width=4)
        steps.add_column("Step", style="bold")
        steps.add_column("Command / Action", overflow="fold")

        steps.add_row(
            "1",
            "Make sure your operating-system credential store is available",
            "Use Keychain Access, Credential Manager, GNOME Keyring, or KWallet.",
        )

        steps.add_row(
            "2",
            "Apply the operating-system steps below",
            "Then run `seekr config secure-store check`.",
        )

        steps.add_row(
            "3",
            "If the check passes, run the app again",
            "Repeat the Seekr command that failed.",
        )

        match os_name:
            case "Linux":
                KeyringTroubleshootingText._add_linux_steps(steps)

            case "Darwin":
                KeyringTroubleshootingText._add_macos_steps(steps)

            case "Windows":
                KeyringTroubleshootingText._add_windows_steps(steps)

            case _:
                steps.add_row(
                    "4",
                    "Unsupported or unknown OS",
                    "Check if your platform has a compatible keyring backend.",
                )

                steps.add_row(
                    "5",
                    "Run the secure-store check",
                    "seekr config secure-store check",
                )

        console.print(steps)

        console.print(Rule("[bold cyan]Recommended check command[/bold cyan]"))
        console.print(KeyringTroubleshootingText._check_command())

        console.print(Rule("[bold cyan]If it still fails[/bold cyan]"))
        console.print(
            Panel(
                "Open an issue at https://github.com/jaraco/keyring/issues "
                "with your OS/version, the Seekr command that failed, the full "
                "error above, and the output from `seekr config secure-store check`.",
                title="Report upstream",
                title_align="left",
                border_style="yellow",
            )
        )

        console.print(
            Panel(
                "After fixing the environment, run your command again or run "
                "`seekr config secure-store check`. If the problem persists, "
                "include the check output in the upstream issue.",
                title="Next step",
                title_align="left",
                border_style="green",
            )
        )

    @staticmethod
    def _add_linux_steps(steps: Table) -> None:
        steps.add_row(
            "4",
            "Install the Secret Service components used by Linux keyrings",
            "sudo apt install gnome-keyring libsecret-1-0 dbus-user-session",
        )

        steps.add_row(
            "5",
            "Make sure a desktop credential service is running",
            "Open GNOME Keyring or KWallet, or start a desktop session.",
        )

        steps.add_row(
            "6",
            "If running headless, start a D-Bus session",
            "dbus-run-session -- sh",
        )

        steps.add_row(
            "7",
            "Unlock or create the GNOME keyring inside the D-Bus session",
            "gnome-keyring-daemon --unlock, then enter the password and press Ctrl+D.",
        )

        steps.add_row(
            "8",
            "Run the check inside the same D-Bus session",
            "seekr config secure-store check",
        )

    @staticmethod
    def _add_macos_steps(steps: Table) -> None:
        steps.add_row(
            "4",
            "Open Keychain Access and check the login keychain",
            "Applications > Utilities > Keychain Access",
        )

        steps.add_row(
            "5",
            "Unlock the login keychain",
            "Right-click `login` keychain > Unlock Keychain `login`",
        )

        steps.add_row(
            "6",
            "Run the secure-store check",
            "seekr config secure-store check",
        )

    @staticmethod
    def _add_windows_steps(steps: Table) -> None:
        steps.add_row(
            "4",
            "Open Credential Manager",
            "Control Panel > Credential Manager > Windows Credentials",
        )

        steps.add_row(
            "5",
            "Check if Windows credentials are available",
            "Make sure your Windows user session is unlocked and active.",
        )

        steps.add_row(
            "6",
            "Run the secure-store check",
            "seekr config secure-store check",
        )

    @staticmethod
    def _check_command() -> Group:
        commands = """
seekr config secure-store check
"""
        return Group(Syntax(commands.strip(), "bash", word_wrap=True))
