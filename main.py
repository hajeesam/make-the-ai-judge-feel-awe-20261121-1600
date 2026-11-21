"""Write a quiet moment of awe to entry.txt.

The entry text is a single 242-character vignette: a baker waiting
while dough rises in the dark, rain writing on the window glass.
This program writes that text, exactly as-is, to ``entry.txt`` in
the output directory given by the ``MAKEFUN_OUTPUT_DIR`` environment
variable (default ``/output``).

Standard library only. Deterministic. No network access.
"""

import os
import sys

ENTRY_TEXT = (
    "The dough will not hurry. The baker dims the oven light and sits "
    "by the window. Outside, rain writes on the glass. She checks "
    "nothing, lifts nothing. Somewhere in the dark of the bowl the "
    "dough is rising anyway, soft as snow settling on snow."
)

MIN_LENGTH = 1
MAX_LENGTH = 280


def validate_text(text):
    """Check that *text* is a valid entry: 1-280 Unicode code points,
    and not only whitespace. Raises ValueError with a clear message
    when the text is invalid."""
    length = len(text)
    if length < MIN_LENGTH or length > MAX_LENGTH:
        raise ValueError(
            "entry text must be between %d and %d characters, "
            "got %d" % (MIN_LENGTH, MAX_LENGTH, length)
        )
    if not text.strip():
        raise ValueError("entry text must not be only whitespace")
    return text


def main():
    try:
        validate_text(ENTRY_TEXT)
    except ValueError as exc:
        print("error: invalid entry text: %s" % exc, file=sys.stderr)
        return 1

    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "entry.txt")
    # Write atomically: a reader never sees a half-written entry.
    tmp_path = output_path + ".tmp"
    with open(tmp_path, "w", encoding="utf-8", newline="") as handle:
        handle.write(ENTRY_TEXT)
    os.replace(tmp_path, output_path)
    print("wrote %s (%d characters)" % (output_path, len(ENTRY_TEXT)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
