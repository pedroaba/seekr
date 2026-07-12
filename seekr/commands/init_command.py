from argparse import Namespace

from seekr.commands.abstract import AbstractCommand
from seekr.constants.paths import DefaultToScan
from seekr.decorators.finish_command import finish_command_execution
from seekr.texts import TextDisplayer, TextDisplayerClassKeys
from seekr.texts.found_paths import FoundPathsText
from seekr.utils.walker import Walker


class InitCommand(AbstractCommand):
    identifier = "init"

    def build(self):
        self.parser.add_argument(
            "-s",
            "--show",
            dest="show_mapped_paths",
            action="store_true",
            default=False,
        )

    @finish_command_execution
    def handle(self, namespace: Namespace):
        TextDisplayer.display(TextDisplayerClassKeys.WELLCOME_INIT_COMMAND)

        default_paths = DefaultToScan()
        paths_to_map = default_paths.get()

        walker = Walker(paths_to_map)
        found_paths = walker.walk()
        if namespace.show_mapped_paths:
            FoundPathsText(found_paths).display()

        # TODO: Adicionar a contagem de arquivos e pastas no footer
        # TODO: Mapear os dados para uma estrutura leve para consulta
        # TODO: Processar os dados através de um fuzzy ou método parecido
        # TODO: Salvar esses dados processados em algum lugar de forma criptografada
        # TODO: Indicar para o usuário que foi mapeado com sucesso e mostrar como
        #  realizar a pesquisa pelo seekr
