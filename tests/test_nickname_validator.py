import unittest

from seekr.utils.validators.nickname import NicknameValidator


class NicknameValidatorTest(unittest.TestCase):
    def test_it_accepts_a_safe_directory_nickname(self):
        self.assertEqual(
            "__pycache__",
            NicknameValidator("__pycache__").validate(),
        )

    def test_it_strips_surrounding_whitespace(self):
        self.assertEqual(
            ".pytest_cache",
            NicknameValidator("  .pytest_cache  ").validate(),
        )

    def test_it_rejects_empty_or_whitespace_only_nicknames(self):
        for nickname in ("", "   "):
            with (
                self.subTest(nickname=nickname),
                self.assertRaisesRegex(ValueError, "cannot be empty"),
            ):
                NicknameValidator(nickname).validate()

    def test_it_rejects_current_and_parent_directory_tokens(self):
        for nickname in (".", ".."):
            with (
                self.subTest(nickname=nickname),
                self.assertRaisesRegex(ValueError, "directory token"),
            ):
                NicknameValidator(nickname).validate()

    def test_it_rejects_paths_and_glob_patterns(self):
        for nickname in ("../", "foo/bar", r"foo\bar", "*", "foo?", "[abc]"):
            with self.subTest(nickname=nickname), self.assertRaises(ValueError):
                NicknameValidator(nickname).validate()
