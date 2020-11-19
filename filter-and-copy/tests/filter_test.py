import unittest
from fac import filter_extension, filter_substr


class TestFilterExtension(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.f_names = ["foo.txt", "bar.jpg", "alice.key", "bob.key"]
        super().setUpClass()

    def test_all_extensions(self):
        f_names = self.f_names
        extensions = ["*.*"]
        filtered = filter_extension(f_names, extensions)
        self.assertEqual(f_names, filtered)

    def test_single_extension(self):
        f_names = self.f_names
        extensions = ["*.txt"]
        filtered = filter_extension(f_names, extensions)
        self.assertEqual([f_names[0]], filtered)

    def test_two_extensions(self):
        f_names = self.f_names
        extensions = ["*.txt", "*.jpg"]
        filtered = filter_extension(f_names, extensions)
        self.assertEqual([f_names[0], f_names[1]], filtered)

    def test_false_extension(self):
        f_names = self.f_names
        extensions = ["txt"]
        filtered = filter_extension(f_names, extensions)
        self.assertEqual([], filtered)

    def test_no_match_extension(self):
        f_names = self.f_names
        extensions = ["*.pdf"]
        filtered = filter_extension(f_names, extensions)
        self.assertEqual([], filtered)


class TestFilterExtensionSubString(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.f_names = ["foo.txt", "foo_edited.txt", "bar.jpg", "alice_edited2.key", "bob.key"]
        super().setUpClass()

    def test_correct(self):
        f_names = self.f_names
        filter_str = "_edited"
        filtered = filter_substr(f_names, filter_str)
        expected = f_names[1:]
        expected.sort()
        self.assertEqual(expected, filtered)

    def test_false(self):
        f_names = self.f_names
        filter_str = "abc"
        filtered = filter_substr(f_names, filter_str)
        expected = f_names
        expected.sort()
        self.assertEqual(expected, filtered)

    def test_no_str(self):
        f_names = self.f_names
        filter_str = ""
        filtered = filter_substr(f_names, filter_str)
        expected = f_names
        expected.sort()
        self.assertEqual(expected, filtered)
