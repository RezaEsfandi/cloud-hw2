"""Queue stored as one name per line.

The HTTP server must call these functions. Tests call them directly,
with a temporary directory, and do not start Docker.
"""

from __future__ import annotations

import fcntl
import os
from contextlib import contextmanager
from pathlib import Path
from tempfile import NamedTemporaryFile


@contextmanager
def locked_queue(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.with_suffix(".lock").open("a", encoding="utf-8") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        yield


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
    name.encode("utf-8")
    path = Path(path)
    with locked_queue(path):
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
    with locked_queue(path):
        try:
            names = path.read_text(encoding="utf-8").splitlines()
        except FileNotFoundError:
            raise LookupError("empty") from None
        if not names:
            raise LookupError("empty")
        with NamedTemporaryFile(mode="w", dir=path.parent, encoding="utf-8", delete=False) as temp:
            temp_path = Path(temp.name)
            try:
                temp.writelines(name + "\n" for name in names[1:])
                temp.close()
                os.replace(temp_path, path)
            finally:
                temp_path.unlink(missing_ok=True)
        return names[0]
