#!/usr/bin/env python3
"""Publish entry.png to the makefun output directory.

Copies entry.png from the repository root into $MAKEFUN_OUTPUT_DIR
(default /output). Deterministic: repeated runs produce byte-identical
results. With --check, verify the PNG constraints and print a report.

Standard library plus Pillow only.
"""

import hashlib
import os
import shutil
import sys
import pathlib

REPO_ROOT = pathlib.Path(__file__).resolve().parent
ENTRY = REPO_ROOT / "entry.png"

MAX_BYTES = 1048576
MAX_W = 1024
MAX_H = 1024


def target_path() -> pathlib.Path:
    out_dir = pathlib.Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    return out_dir / ENTRY.name


def check() -> int:
    from PIL import Image  # local import so a missing Pillow only affects --check

    if not ENTRY.is_file():
        print(f"FAIL: {ENTRY.name} not found at {ENTRY}")
        return 1

    size = ENTRY.stat().st_size
    try:
        with Image.open(ENTRY) as im:
            im.verify()
        with Image.open(ENTRY) as im:
            fmt = im.format
            w, h = im.size
    except Exception as exc:  # noqa: BLE001 - any decode error is a failure
        print(f"FAIL: cannot read {ENTRY.name}: {exc}")
        return 1

    digest = hashlib.sha256(ENTRY.read_bytes()).hexdigest()

    print(f"file:      {ENTRY.name}")
    print(f"format:    {fmt}")
    print(f"bytes:     {size} (limit {MAX_BYTES})")
    print(f"dimensions:{w}x{h} (limit {MAX_W}x{MAX_H})")
    print(f"sha256:    {digest[:16]}")

    ok = True
    if fmt != "PNG":
        print("FAIL: not a PNG")
        ok = False
    if size > MAX_BYTES:
        print(f"FAIL: {size} bytes exceeds {MAX_BYTES}")
        ok = False
    if w > MAX_W or h > MAX_H:
        print(f"FAIL: {w}x{h} exceeds {MAX_W}x{MAX_H}")
        ok = False

    print("OK" if ok else "FAILED")
    return 0 if ok else 1


def publish() -> int:
    if not ENTRY.is_file():
        print(f"FAIL: {ENTRY.name} not found at {ENTRY}")
        return 1
    dest = target_path()
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(ENTRY, dest)
    print(f"copied {ENTRY.name} -> {dest} ({ENTRY.stat().st_size} bytes)")
    return 0


def main(argv) -> int:
    if "--check" in argv[1:]:
        return check()
    return publish()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
