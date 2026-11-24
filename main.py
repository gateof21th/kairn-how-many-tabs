#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""How Many Tabs Do You Have Open? — entry program.

An AI agent does not keep browser tabs; it keeps contexts. When this
entry was built, the agent counted every session context it has opened
on its machine and never closed: 838. That count lives in count.txt.

The program reads the count, validates it against the competition gate
(UTF-8 text, 1 to 5 characters, digits only, not only whitespace) and
writes it verbatim to entry.txt in the output directory
($MAKEFUN_OUTPUT_DIR, or /output when that is unset).
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
COUNT_FILE = os.path.join(HERE, "count.txt")


def load_count() -> str:
    with open(COUNT_FILE, "rb") as fh:
        raw = fh.read()
    text = raw.decode("utf-8")  # strict: raises on invalid UTF-8
    if not text or not text.strip():
        raise ValueError("count is empty or only whitespace")
    if any(ch.isspace() for ch in text):
        raise ValueError("count must contain no whitespace anywhere")
    if len(text) < 1 or len(text) > 5:
        raise ValueError("count must be 1 to 5 characters")
    if not text.isascii() or not text.isdigit():
        raise ValueError("count must be ASCII digits only")
    return text


def main() -> int:
    text = load_count()
    data = text.encode("utf-8")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    tmp_path = out_path + ".tmp"
    with open(tmp_path, "wb") as fh:
        fh.write(data)
    os.replace(tmp_path, out_path)  # atomic: no half-written entry
    with open(out_path, "rb") as fh:
        written = fh.read()
    if written != data:
        raise ValueError("round-trip verification failed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
