#!/usr/bin/env python3
"""Pre-publish QA for medi posts. Exit 1 on quality failures.

Checks:
- duplicate H2 headings within a post
- forbidden padding phrases
- word count >= 1000
- hero_image present
- at least one inline image
- duplicate images across posts (hero or first inline)
"""
from __future__ import annotations

import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
POSTS = ROOT / "_posts"
MIN_WORDS = 1000
FORBIDDEN = [
    "One more gentle reminder",
    "You do not have to solve your whole social life tonight",
]


def fail(msg: str, errors: list[str]) -> None:
    errors.append(msg)


def main() -> int:
    errors: list[str] = []
    posts = sorted(POSTS.glob("*.md"))
    if not posts:
        print("No posts found", file=sys.stderr)
        return 1

    heroes: dict[str, str] = {}
    inlines: dict[str, str] = {}

    for f in posts:
        text = f.read_text(encoding="utf-8")
        parts = text.split("---", 2)
        if len(parts) < 3:
            fail(f"{f.name}: missing frontmatter", errors)
            continue
        fm, body = parts[1], parts[2]

        for phrase in FORBIDDEN:
            if phrase in body:
                fail(f"{f.name}: forbidden phrase {phrase!r}", errors)

        heads = re.findall(r"^## (.+)$", body, re.M)
        for h, n in Counter(heads).items():
            if n > 1:
                fail(f"{f.name}: duplicate H2 {h!r} x{n}", errors)

        words = len(re.findall(r"\w+", body))
        if words < MIN_WORDS:
            fail(f"{f.name}: only {words} words (<{MIN_WORDS})", errors)

        hm = re.search(r'^hero_image:\s*"([^"]+)"', fm, re.M)
        if not hm:
            fail(f"{f.name}: missing hero_image", errors)
        else:
            hero = hm.group(1)
            if hero in heroes:
                fail(f"{f.name}: duplicate hero with {heroes[hero]}", errors)
            else:
                heroes[hero] = f.name

        imgs = re.findall(r"!\[[^\]]*\]\((https?://[^)]+)\)", body)
        if not imgs:
            fail(f"{f.name}: missing inline image", errors)
        else:
            inline = imgs[0]
            if inline in inlines:
                fail(f"{f.name}: duplicate inline with {inlines[inline]}", errors)
            else:
                inlines[inline] = f.name
            if hm and inline == hm.group(1):
                fail(f"{f.name}: hero and inline are the same URL", errors)

        # consecutive duplicate long lines
        lines = [ln.strip() for ln in body.splitlines() if len(ln.strip()) > 80]
        for a, b in zip(lines, lines[1:]):
            if a == b:
                fail(f"{f.name}: consecutive duplicate paragraph", errors)
                break

    if errors:
        print(f"QA FAILED — {len(errors)} issue(s):", file=sys.stderr)
        for e in errors[:80]:
            print(f"  - {e}", file=sys.stderr)
        if len(errors) > 80:
            print(f"  … +{len(errors)-80} more", file=sys.stderr)
        return 1

    print(f"QA OK — {len(posts)} posts, unique heroes={len(heroes)}, unique inlines={len(inlines)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
