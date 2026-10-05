from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re


CHECKLIST_LINE = re.compile(r"^\s*[-*]\s+\[[ xX]\]\s+.+")
CHECKBOX_SHAPE = re.compile(r"^\s*[-*]\s+\[.*\]")


@dataclass(frozen=True)
class ChecklistIssue:
    path: Path
    line_number: int
    line: str
    message: str


def find_checklist_issues(path: Path) -> list[ChecklistIssue]:
    """Return malformed Markdown checklist lines in a file."""
    issues: list[ChecklistIssue] = []

    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if CHECKBOX_SHAPE.match(line) and not CHECKLIST_LINE.match(line):
            issues.append(
                ChecklistIssue(
                    path=path,
                    line_number=line_number,
                    line=line,
                    message="Checklist items must use '- [ ] item' or '- [x] item'.",
                )
            )

    return issues

