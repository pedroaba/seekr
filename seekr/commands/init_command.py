from argparse import Namespace

from seekr.commands.abstract import AbstractCommand
from seekr.constants.paths import DefaultToScan
from seekr.decorators.finish_command import finish_command_execution
from seekr.texts import TextDisplayer, TextDisplayerClassKeys
from seekr.texts.found_paths import FoundPathsText, Metadata
from seekr.utils.walker import Walker


class InitCommand(AbstractCommand):
    identifier = "init"
    help_text = "Scan the default user folders"
    description = (
        "Scan Seekr's default folders for files and directories. The default "
        "locations are Downloads, Documents, Desktop, Pictures, Videos, and Music."
    )
    epilog = "Examples:\n  seekr init\n  seekr init --show"

    def build(self):
        self.parser.add_argument(
            "-s",
            "--show",
            dest="show_mapped_paths",
            action="store_true",
            default=False,
            help="Display the files and directories found during the scan.",
        )

        self.parser.add_argument(
            "-n",
            "--number-of-paths-showing",
            dest="number_of_paths_showing",
            type=int,
            default=10,
            help="Number of paths to show. If pass -1 show all paths.",
        )

    @finish_command_execution
    def handle(self, namespace: Namespace):
        TextDisplayer.display(TextDisplayerClassKeys.WELLCOME_INIT_COMMAND)

        default_paths = DefaultToScan()
        paths_to_map = default_paths.get()

        walker = Walker(paths_to_map)
        response = walker.walk()

        total = len(response.results)

        if namespace.show_mapped_paths:
            position_to_slice_results = (
                namespace.number_of_paths_showing
                if namespace.number_of_paths_showing > 0
                else total
            )
            results = response.results[:position_to_slice_results]

            FoundPathsText(results).display(
                metadata=Metadata(
                    number_of_paths_showing=len(results),
                    total_files=response.total_files,
                    total_dirs=response.total_dirs,
                    total=total,
                )
            )
