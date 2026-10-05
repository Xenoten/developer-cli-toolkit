from pathlib import Path
import tempfile
import unittest

from devtoolkit.checklist import find_checklist_issues


class ChecklistTests(unittest.TestCase):
    def test_valid_checklist_items_have_no_issues(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "README.md"
            path.write_text("- [ ] Write tests\n- [x] Update README\n", encoding="utf-8")

            self.assertEqual(find_checklist_issues(path), [])

    def test_malformed_checklist_item_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "README.md"
            path.write_text("- [] Missing space\n", encoding="utf-8")

            issues = find_checklist_issues(path)

        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].line_number, 1)


if __name__ == "__main__":
    unittest.main()

