from pathlib import Path
import tempfile
import unittest

from devtoolkit.todo_scan import scan_todos


class TodoScanTests(unittest.TestCase):
    def test_scan_file_finds_default_markers(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "example.py"
            path.write_text("# TODO: add validation\nprint('done')\n", encoding="utf-8")

            matches = scan_todos(path)

        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0].marker, "TODO")
        self.assertEqual(matches[0].text, "add validation")

    def test_scan_directory_ignores_dependency_folders(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "src"
            dependency = root / "node_modules"
            source.mkdir()
            dependency.mkdir()
            (source / "app.py").write_text("# FIXME: handle edge case\n", encoding="utf-8")
            (dependency / "ignored.py").write_text("# TODO: ignore me\n", encoding="utf-8")

            matches = scan_todos(root)

        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0].marker, "FIXME")

    def test_scan_does_not_match_descriptive_marker_words(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "README.md"
            path.write_text("This command scans TODO-style comments.\n", encoding="utf-8")

            matches = scan_todos(path)

        self.assertEqual(matches, [])


if __name__ == "__main__":
    unittest.main()
