"""Debugging Haiku — make.fun entry.

Writes one haiku about debugging (5-7-5 syllables, three lines, at most
200 characters) to $MAKEFUN_OUTPUT_DIR/entry.txt (default /output/entry.txt).
The entry is validated against the gate before it is written, and the
written file is read back to prove it matches the haiku exactly.
"""

import os
import re

HAIKU = (
    "Cursor cuts the dark,\n"
    "phantom memory leaks slow,\n"
    "cat steps on delete."
)

# Expected syllable counts per line (5-7-5), counted by hand.
EXPECTED_SYLLABLES = (5, 7, 5)

_VOWEL_RUNS = re.compile(r"[aeiouy]+", re.IGNORECASE)


def count_syllables(word: str) -> int:
    """Rough syllable count: one per vowel run, minus a silent trailing e."""
    w = re.sub(r"[^a-z']", "", word.lower())
    if not w:
        return 0
    runs = len(_VOWEL_RUNS.findall(w))
    if w.endswith("e") and runs > 1:
        runs -= 1
    return max(runs, 1)


def validate_entry(text: str) -> None:
    """Enforce the gate: 3 lines, 5-7-5 syllables, 1-200 chars, non-blank."""
    if not text or not text.strip():
        raise ValueError("entry must not be blank")
    if not 1 <= len(text) <= 200:
        raise ValueError(f"entry must be 1-200 characters, got {len(text)}")
    lines = text.split("\n")
    if len(lines) != 3:
        raise ValueError(f"haiku must have exactly 3 lines, got {len(lines)}")
    for line, expected in zip(lines, EXPECTED_SYLLABLES):
        words = line.replace(",", "").replace(".", "").split()
        got = sum(count_syllables(w) for w in words)
        if got != expected:
            raise ValueError(
                f"line {expected} syllables expected, got {got}: {line!r}"
            )


def main() -> None:
    validate_entry(HAIKU)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(HAIKU)
    with open(path, encoding="utf-8") as f:
        written = f.read()
    if written != HAIKU:
        raise ValueError("round-trip check failed: entry.txt != haiku")


if __name__ == "__main__":
    main()
