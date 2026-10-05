from __future__ import annotations

from datetime import date
from pathlib import Path


def build_notes_template(title: str, today: date | None = None) -> str:
    current_date = today or date.today()
    return f"""# {title}

Created: {current_date.isoformat()}

## Purpose

- 

## Decisions

- 

## Issues

- 

## Next Steps

- 
"""


def create_notes_file(path: Path, title: str, overwrite: bool = False) -> Path:
    if path.exists() and not overwrite:
        raise FileExistsError(path)

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(build_notes_template(title), encoding="utf-8")
    return path

