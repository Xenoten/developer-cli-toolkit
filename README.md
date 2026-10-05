# Developer CLI Toolkit

A small command-line toolkit for everyday developer housekeeping tasks.

This project is part of a software engineering portfolio. It is intentionally modest in scope: the goal is to demonstrate clear structure, useful error handling, testable logic, and practical documentation rather than a flashy feature set.

## Features

- Scan a project for TODO-style comments.
- Validate Markdown checklist syntax.
- Create a simple project notes file from a template.

## Why This Project Exists

Many developer tasks are small, repetitive, and easy to neglect. This CLI collects a few useful checks that help keep a project understandable and maintainable.

The portfolio focus is on:

- Clean command boundaries.
- Testable parsing logic.
- Helpful error messages.
- Simple, maintainable code.
- Documentation that makes the tool easy to run.

## Project Structure

```text
developer-cli-toolkit/
  README.md
  pyproject.toml
  src/
    devtoolkit/
      __init__.py
      cli.py
      checklist.py
      notes.py
      todo_scan.py
  tests/
    test_checklist.py
    test_notes.py
    test_todo_scan.py
```

## Requirements

- Python 3.11 or newer.

The first version uses only the Python standard library.

On this machine, a working Python install was found at:

```text
C:\msys64\ucrt64\bin\python.exe
```

## Running the CLI

From this folder:

```powershell
python -m devtoolkit --help
```

If running directly from the source tree without installing, set `PYTHONPATH` first:

```powershell
$env:PYTHONPATH = ".\src"
python -m devtoolkit --help
```

If `python` still resolves to the Windows Store alias, use the full local path:

```powershell
$env:PYTHONPATH = ".\src"
& "C:\msys64\ucrt64\bin\python.exe" -m devtoolkit --help
```

## Commands

### Scan TODOs

```powershell
python -m devtoolkit todos .
```

Scans text files for markers such as `TODO`, `FIXME`, and `HACK`.

### Validate Markdown Checklists

```powershell
python -m devtoolkit checklist README.md
```

Flags checklist lines that look malformed.

Valid examples:

```markdown
- [ ] Write tests
- [x] Update README
```

### Create Project Notes

```powershell
python -m devtoolkit notes PROJECT_NOTES.md --title "Developer CLI Toolkit"
```

Creates a reusable notes file with sections for decisions, issues, and next steps.

## Running Tests

```powershell
$env:PYTHONPATH = ".\src"
python -m unittest discover -s tests
```

Verified locally with:

```powershell
$env:PYTHONPATH = ".\src"
& "C:\msys64\ucrt64\bin\python.exe" -m unittest discover -s tests
```

## Engineering Notes

- The CLI layer in `cli.py` handles arguments and user-facing output.
- Core logic lives in small modules that can be tested without running shell commands.
- File scanning avoids common generated or dependency folders by default.
- The first version avoids external packages to keep setup simple.

## Known Limitations

- TODO scanning is text-based and does not parse programming languages.
- Markdown checklist validation is intentionally conservative.
- The notes command does not overwrite existing files unless explicitly requested.

## Future Improvements

- Add JSON output for automation.
- Add a project health summary command.
- Add packaging/install instructions.
- Add optional configuration for ignored paths and TODO markers.
- Add CI once the repository is public.
