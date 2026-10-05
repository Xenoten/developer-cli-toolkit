from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re


DEFAULT_MARKERS = ("TODO", "FIXME", "HACK")
IGNORED_DIRECTORIES = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    "__pycache__",
    "build",
    "dist",
    "node_modules",
    "venv",
    ".venv",
}
TEXT_FILE_SUFFIXES = {
    ".css",
    ".html",
    ".java",
    ".js",
    ".json",
    ".md",
    ".py",
    ".rs",
    ".toml",
    ".ts",
    ".tsx",
    ".txt",
    ".yaml",
    ".yml",
}


@dataclass(frozen=True)
class TodoMatch:
    path: Path
    line_number: int
    marker: str
    text: str


def scan_todos(path: Path, markers: list[str] | None = None) -> list[TodoMatch]:
    """Scan a file or directory for TODO-style markers."""
    active_markers = tuple(markers or DEFAULT_MARKERS)
    marker_pattern = "|".join(re.escape(marker) for marker in active_markers)
    pattern = re.compile(rf"\b({marker_pattern})(?::|\s+)(.*)")

    matches: list[TodoMatch] = []
    for file_path in iter_text_files(path):
        matches.extend(scan_file(file_path, pattern))
    return matches


def iter_text_files(path: Path) -> list[Path]:
    if path.is_file():
        return [path] if is_probably_text_file(path) else []

    if not path.exists():
        return []

    files: list[Path] = []
    for file_path in path.rglob("*"):
        if any(part in IGNORED_DIRECTORIES for part in file_path.parts):
            continue
        if file_path.is_file() and is_probably_text_file(file_path):
            files.append(file_path)
    return sorted(files)


def is_probably_text_file(path: Path) -> bool:
    return path.suffix.lower() in TEXT_FILE_SUFFIXES


def scan_file(path: Path, pattern: re.Pattern[str]) -> list[TodoMatch]:
    matches: list[TodoMatch] = []

    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except UnicodeDecodeError:
        return matches

    for line_number, line in enumerate(lines, start=1):
        result = pattern.search(line)
        if result:
            matches.append(
                TodoMatch(
                    path=path,
                    line_number=line_number,
                    marker=result.group(1),
                    text=result.group(2).strip(),
                )
            )

    return matches
