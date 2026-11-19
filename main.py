"""Run the news-image-20261118 entry.

The front page (entry.png) is drawn by draw.py and shipped in this
repository. All this program does is place a copy of it where the
grader expects it, as entry.png. It needs nothing beyond the Python
standard library, touches no network, and its output is identical on
every run because the source file never changes.
"""

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
IMAGE_NAME = "entry.png"


def copy_entry() -> Path:
    """Copy the shipped front page into the output directory."""
    import os

    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    source = ROOT / IMAGE_NAME
    if not source.is_file():
        raise FileNotFoundError(f"{IMAGE_NAME} is missing next to main.py")
    destination = out_dir / IMAGE_NAME
    shutil.copyfile(source, destination)
    return destination


if __name__ == "__main__":
    written = copy_entry()
    print("wrote", written)
