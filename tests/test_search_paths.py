import unittest

from seekr.application.services.contains_words_search_engine import (
    ContainsWordsSearchEngine,
)
from seekr.application.services.fallback_search_engine import FallbackSearchEngine
from seekr.application.use_cases.search_paths import SearchPaths, SearchPathsInput
from seekr.domain.entities.indexed_path import IndexedPath
from tests.fakes import InMemoryPathRepository, StubSearchEngine


class SearchPathsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.report = IndexedPath(
            filepath="/documents/report.pdf",
            parent_path="/documents",
            normalized_filepath="documents report.pdf",
            is_folder=False,
            is_file=True,
        )
        self.archive = IndexedPath(
            filepath="/documents/archive",
            parent_path="/documents",
            normalized_filepath="documents archive",
            is_folder=True,
            is_file=False,
        )
        self.repository = InMemoryPathRepository([self.report, self.archive])
        self.engine = StubSearchEngine([1, 0])
        self.use_case = SearchPaths(self.repository, self.engine)

    def test_it_returns_paths_in_search_engine_order(self) -> None:
        result = self.use_case.execute(
            SearchPathsInput(query=["final", "report"], limit=5, precision=90)
        )

        self.assertEqual([self.archive, self.report], result.paths)
        self.assertEqual(
            [
                (
                    "final report",
                    ["documents report.pdf", "documents archive"],
                    5,
                    90,
                )
            ],
            self.engine.calls,
        )

    def test_it_returns_no_results_when_the_index_is_empty(self) -> None:
        repository = InMemoryPathRepository()
        engine = StubSearchEngine([])

        result = SearchPaths(repository, engine).execute(
            SearchPathsInput(query=["report"])
        )

        self.assertEqual([], result.paths)
        self.assertEqual([], engine.calls)

    def test_it_falls_back_to_contains_words_when_primary_search_finds_nothing(
        self,
    ) -> None:
        primary = StubSearchEngine([])
        combined_search = FallbackSearchEngine(
            primary=primary,
            fallback=ContainsWordsSearchEngine(),
        )

        result = SearchPaths(self.repository, combined_search).execute(
            SearchPathsInput(query=["DOCUMENTS", "report"], limit=1)
        )

        self.assertEqual([self.report], result.paths)
        self.assertEqual(1, len(primary.calls))

    def test_it_does_not_use_fallback_when_primary_search_finds_results(
        self,
    ) -> None:
        primary = StubSearchEngine([1])
        fallback = StubSearchEngine([0])
        combined_search = FallbackSearchEngine(
            primary=primary,
            fallback=fallback,
        )

        result = SearchPaths(self.repository, combined_search).execute(
            SearchPathsInput(query=["archive"])
        )

        self.assertEqual([self.archive], result.paths)
        self.assertEqual(1, len(primary.calls))
        self.assertEqual([], fallback.calls)
