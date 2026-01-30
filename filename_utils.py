"""Small utility module for filename transformations.

Keep the core logic separate from the GUI so it can be easily tested
and reused without importing `tkinter`.
"""
from pathlib import Path


def clean_name(filename: str) -> str:
    """Return filename keeping only the part after the last underscore.

    - Preserves the extension.
    - If there is no underscore, returns the original filename.
    """
    p = Path(filename)
    stem = p.stem
    suffix = p.suffix
    if "_" not in stem:
        return p.name
    new_stem = stem.rsplit("_", 1)[-1]
    return f"{new_stem}{suffix}"
