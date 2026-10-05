from __future__ import annotations

import argparse
from pathlib import Path
import sys

from devtoolkit.checklist import find_checklist_issues
from devtoolkit.notes import create_notes_file
from devtoolkit.todo_scan import scan_todos


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="devtoolkit",
        description="Small developer productivity checks.",
    )
    subcommands = parser.add_subparsers(dest="command", required=True)

    todos = subcommands.add_parser("todos", help="Scan files for TODO-style markers.")
    todos.add_argument("path", type=Path, help="File or directory to scan.")
    todos.add_argument(
        "--marker",
        action="append",
        dest="markers",
        help="Marker to search for. Can be supplied more than once.",
    )
    todos.set_defaults(handler=handle_todos)

    checklist = subcommands.add_parser("checklist", help="Validate Markdown checklist lines.")
    checklist.add_argument("path", type=Path, help="Markdown file to validate.")
    checklist.set_defaults(handler=handle_checklist)

    notes = subcommands.add_parser("notes", help="Create a project notes file.")
    notes.add_argument("path", type=Path, help="Notes file to create.")
    notes.add_argument("--title", default="Project Notes", help="Title for the notes file.")
    notes.add_argument("--force", action="store_true", help="Overwrite an existing file.")
    notes.set_defaults(handler=handle_notes)

    return parser


def handle_todos(args: argparse.Namespace) -> int:
    matches = scan_todos(args.path, markers=args.markers)
    if not matches:
        print("No TODO-style markers found.")
        return 0

    for match in matches:
        print(f"{match.path}:{match.line_number}: {match.marker}: {match.text}")
    return 0


def handle_checklist(args: argparse.Namespace) -> int:
    if not args.path.exists():
        print(f"File not found: {args.path}", file=sys.stderr)
        return 2

    issues = find_checklist_issues(args.path)
    if not issues:
        print("Checklist looks good.")
        return 0

    for issue in issues:
        print(f"{issue.path}:{issue.line_number}: {issue.message}", file=sys.stderr)
        print(f"  {issue.line}", file=sys.stderr)
    return 1


def handle_notes(args: argparse.Namespace) -> int:
    try:
        created_path = create_notes_file(args.path, title=args.title, overwrite=args.force)
    except FileExistsError:
        print(f"File already exists: {args.path}. Use --force to overwrite.", file=sys.stderr)
        return 1

    print(f"Created notes file: {created_path}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.handler(args)

