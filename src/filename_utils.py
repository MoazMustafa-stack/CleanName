from pathlib import Path


def clean_name(filename: str) -> str:
    p = Path(filename)
    stem = p.stem
    suffix = p.suffix
    if "_" not in stem:
        return p.name
    new_stem = stem.rsplit("_", 1)[-1]
    return f"{new_stem}{suffix}"
