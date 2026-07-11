import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from seekr.exceptions.file import FileOrFolderDoesNotExist
from seekr.utils.validators.path import PathValidator


class PathValidatorTest(unittest.TestCase):
    def test_it_returns_an_absolute_normalized_existing_path(self):
        with TemporaryDirectory() as directory:
            expected = Path(directory).resolve()

            result = PathValidator(Path(directory)).validate()

        self.assertEqual(expected, result)

    def test_it_accepts_an_existing_file(self):
        with TemporaryDirectory() as directory:
            file_path = Path(directory) / "ignore.txt"
            file_path.touch()

            result = PathValidator(file_path).validate()

        self.assertEqual(file_path.resolve(), result)

    def test_it_rejects_a_path_that_does_not_exist(self):
        missing_path = Path("path-that-does-not-exist")

        with self.assertRaises(FileOrFolderDoesNotExist):
            PathValidator(missing_path).validate()
