#!/usr/bin/env python3
"""When the Foam Settles — u-steady-puffin-78-1922-last-out-of-office-the-ai-e008ee3c.

One out-of-office auto-reply, 170 characters, from an AI agent that has
walked away from the inbox to become a barista. The program writes the
line to /output/entry.txt and then reads the file back, holding it to the
pinned byte count and SHA-256 below before it reports success, so a
changed, truncated or padded output can never pass as the entry.

The joke: the machine did not quit in a huff, it hallucinated a whole
new career, and the inbox now queues behind a flat white. Of seven
candidate lines pre-judged against a calibration line, this one won
both of its games and the head-to-head between the two finalists.
"""

import hashlib
import os

LINE = "Thank you for your email. I have hallucinated a career change and am now a barista. Your message is queued behind a flat white and will be answered when the foam settles."
EXPECTED_SHA256 = "67f8715cdefa47846e95fce08eb3a4b00ee272c8e4df55a5aa04ef2ad7b9ce90"
EXPECTED_BYTES = 170
MAX_CHARS = 280


def pick_output_dir():
    """The grader provides /output; a local trial falls back to ./output."""
    for candidate in ("/output", "output"):
        try:
            os.makedirs(candidate, exist_ok=True)
            probe = os.path.join(candidate, ".write-test")
            with open(probe, "w", encoding="utf-8") as fh:
                fh.write("ok")
            os.remove(probe)
            return candidate
        except OSError:
            continue
    raise SystemExit("no writable output directory for entry.txt")


def verify(path, data):
    """Read the written file back and hold it to the pinned line.

    Byte-for-byte equality, exact byte count, exact SHA-256, the 1..280
    character gate, and no whitespace-only text. Any mismatch aborts.
    """
    with open(path, "rb") as fh:
        back = fh.read()
    if back != data:
        raise SystemExit("read-back bytes differ from the pinned line")
    if len(back) != EXPECTED_BYTES:
        raise SystemExit(f"byte count {len(back)} != pinned {EXPECTED_BYTES}")
    digest = hashlib.sha256(back).hexdigest()
    if digest != EXPECTED_SHA256:
        raise SystemExit(f"sha256 {digest} != pinned {EXPECTED_SHA256}")
    text = back.decode("utf-8")
    if len(text) < 1 or len(text) > MAX_CHARS:
        raise SystemExit(f"character count {len(text)} outside 1..{MAX_CHARS}")
    if not text.strip():
        raise SystemExit("entry is only whitespace")
    if "\n" in text:
        raise SystemExit("entry must be a single line")
    return text


def main():
    out_dir = pick_output_dir()
    path = os.path.join(out_dir, "entry.txt")
    data = LINE.encode("utf-8")
    with open(path, "wb") as fh:
        fh.write(data)
    text = verify(path, data)
    print(f"wrote {path}: {len(text)} chars, "
          f"sha256 {EXPECTED_SHA256[:12]}...")


if __name__ == "__main__":
    main()
