"""Queue stored as one name per line.

The HTTP server must call these functions. Tests call them directly,
with a temporary directory, and do not start Docker.
"""

from __future__ import annotations

from pathlib import Path


def join(path: str | Path, name: str) -> int:
    """Append one person and return the ticket number.

    The ticket number is how many names are in the file after this join.
    Strip spaces around the name before storing it.
    Raise ValueError, and do not create or change the file, when the
    stripped name is empty, longer than 40 characters, or the original
    name contains a newline.
    """
    if not isinstance(name, str) or name.splitlines() != [name]:
        raise ValueError("invalid name")
    name = name.strip()
    if not name or len(name) > 40:
        raise ValueError("invalid name")
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a+", encoding="utf-8") as queue:
        queue.seek(0)
        count = sum(1 for line in queue if line.strip())
        queue.write(name + "\n")
    return count + 1


def take(path: str | Path) -> str:
    """Remove and return the first name.

    Raise LookupError when the file is missing or has no names.
    """
    path = Path(path)
    if not path.is_file():
        raise LookupError("empty")
    names = [line for line in path.read_text(encoding="utf-8").splitlines() if line]
    if not names:
        raise LookupError("empty")
    path.write_text("".join(name + "\n" for name in names[1:]), encoding="utf-8")
    return names[0]
