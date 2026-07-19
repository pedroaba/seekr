import unittest
from datetime import datetime

from seekr.application.use_cases.build_index import (
    BuildIndex,
    BuildIndexInput,
    BuildIndexStatus,
)
from seekr.domain.entities.indexed_path import IndexedPath
from seekr.domain.entities.scan import ScanResult, ScanRoot
from tests.fakes import (
    InMemoryPathRepository,
    StubPathScanner,
    StubScanRootsProvider,
)


class BuildIndexTest(unittest.TestCase):
    def setUp(self) -> None:
        self.root = ScanRoot(resource="/documents", alias="documents")
        self.path = IndexedPath(
            filepath="/documents/report.pdf",
            parent_path="/documents",
            normalized_filepath="documents report.pdf",
            is_folder=False,
            is_file=True,
            modified_path_at=datetime(2026, 7, 18, 10, 0),
        )
        self.scan_result = ScanResult(paths=[self.path], total_files=1, total_dirs=0)
        self.repository = InMemoryPathRepository()
        self.scanner = StubPathScanner(self.scan_result)
        self.roots = StubScanRootsProvider([self.root])
        self.use_case = BuildIndex(self.repository, self.scanner, self.roots)

    def test_it_scans_roots_and_replaces_the_index(self) -> None:
        result = self.use_case.execute(BuildIndexInput())

        self.assertEqual(BuildIndexStatus.CREATED, result.status)
        self.assertEqual([self.path], result.paths)
        self.assertEqual(1, result.total_files)
        self.assertEqual(0, result.total_dirs)
        self.assertEqual([[self.path]], self.repository.replace_calls)
        self.assertEqual([[self.root]], self.scanner.calls)

    def test_it_preserves_an_existing_index_without_force(self) -> None:
        self.repository.paths = [self.path]

        result = self.use_case.execute(BuildIndexInput(force=False))

        self.assertEqual(BuildIndexStatus.ALREADY_EXISTS, result.status)
        self.assertEqual([], self.repository.replace_calls)
        self.assertEqual([], self.scanner.calls)

    def test_it_rebuilds_an_existing_index_when_forced(self) -> None:
        old_path = IndexedPath(
            filepath="/old.txt",
            parent_path="/",
            normalized_filepath="old.txt",
            is_folder=False,
            is_file=True,
        )
        self.repository.paths = [old_path]

        result = self.use_case.execute(BuildIndexInput(force=True))

        self.assertEqual(BuildIndexStatus.CREATED, result.status)
        self.assertEqual([self.path], self.repository.paths)
        self.assertEqual([[self.root]], self.scanner.calls)
