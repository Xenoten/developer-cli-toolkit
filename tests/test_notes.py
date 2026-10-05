from datetime import date
from pathlib import Path
import tempfile
import unittest

from devtoolkit.notes import build_notes_template, create_notes_file


class NotesTests(unittest.TestCase):
    def test_template_contains_title_and_date(self) -> None:
        template = build_notes_template("Example", today=date(2026, 10, 5))

        self.assertIn("# Example", template)
        self.assertIn("Created: 2026-10-05", template)
        self.assertIn("## Decisions", template)

    def test_create_notes_file_refuses_to_overwrite_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "notes.md"
            path.write_text("existing", encoding="utf-8")

            with self.assertRaises(FileExistsError):
                create_notes_file(path, title="Notes")


if __name__ == "__main__":
    unittest.main()

