from pathlib import Path

from seekr.adapters.outbound.filesystem.path_normalizer import PathNormalizer
from seekr.application.ports.path_scanner import PathScanner
from seekr.domain.entities.indexed_path import IndexedPath
from seekr.domain.entities.scan import ScanResult, ScanRoot


class FileSystemPathScanner(PathScanner):
    def scan(self, roots: list[ScanRoot]) -> ScanResult:
        paths: list[IndexedPath] = []
        for root in roots:
            self._scan_root(root, paths)
        return ScanResult(
            paths=paths,
            total_files=sum(path.is_file for path in paths),
            total_dirs=sum(path.is_folder for path in paths),
        )

    def _scan_root(self, root: ScanRoot, output: list[IndexedPath]) -> None:
        resource = Path(root.resource)
        if resource.is_file():
            output.append(
                self._to_indexed_path(
                    resource,
                    resource.parent,
                    source_alias=root.alias,
                    is_file=True,
                )
            )
            return
        if not resource.is_dir():
            return
        for current_dir, _, files in resource.walk():
            output.append(
                self._to_indexed_path(
                    current_dir,
                    resource,
                    source_alias=root.alias,
                    is_folder=True,
                )
            )
            output.extend(
                self._to_indexed_path(
                    current_dir / filename,
                    current_dir,
                    source_alias=root.alias,
                    is_file=True,
                )
                for filename in files
            )

    @staticmethod
    def _to_indexed_path(
        path: Path,
        parent: Path,
        *,
        source_alias: str | None = None,
        is_file: bool = False,
        is_folder: bool = False,
    ) -> IndexedPath:
        resolved = path.resolve().absolute()
        return IndexedPath(
            filepath=str(resolved),
            parent_path=str(parent.resolve()),
            normalized_filepath=PathNormalizer.normalize(resolved),
            is_folder=is_folder,
            is_file=is_file,
            source_alias=source_alias,
        )
