#!/usr/bin/env python3
"""Assign a unique Picsum hero + unique Picsum inline to every medi post.

Uses _data/picsum-pool.json (refresh with picsum API if needed).
Ensures 200 heroes + 200 inlines = 400 distinct image IDs.
"""
from __future__ import annotations

import json
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
POSTS = ROOT / "_posts"
POOL = ROOT / "_data" / "picsum-pool.json"
ASSIGN = ROOT / "_data" / "image-assignments.json"


def ensure_pool(min_count: int = 400) -> list[dict]:
    if POOL.exists():
        data = json.loads(POOL.read_text())
        if len(data) >= min_count:
            return data
    all_imgs: list[dict] = []
    page = 1
    while len(all_imgs) < min_count + 50:
        url = f"https://picsum.photos/v2/list?page={page}&limit=50"
        with urllib.request.urlopen(url, timeout=30) as r:
            chunk = json.loads(r.read().decode())
        if not chunk:
            break
        all_imgs.extend(chunk)
        page += 1
    seen = set()
    uniq = []
    for im in all_imgs:
        if im["id"] in seen:
            continue
        seen.add(im["id"])
        uniq.append(im)
    POOL.parent.mkdir(exist_ok=True)
    POOL.write_text(json.dumps(uniq, indent=2))
    return uniq


def main() -> None:
    pool = ensure_pool(400)
    ids = [str(im["id"]) for im in pool]
    posts = sorted(POSTS.glob("*.md"))
    n = len(posts)
    if len(ids) < n * 2:
        raise SystemExit(f"Need {n*2} images, pool has {len(ids)}")

    heroes = ids[0:n]
    inlines = ids[n : n * 2]
    assign = {}

    for i, f in enumerate(posts):
        hero_url = f"https://picsum.photos/id/{heroes[i]}/1200/630"
        inline_url = f"https://picsum.photos/id/{inlines[i]}/800/500"
        assign[f.name] = {
            "hero": hero_url,
            "inline": inline_url,
            "hero_id": heroes[i],
            "inline_id": inlines[i],
        }

        text = f.read_text(encoding="utf-8")
        text = re.sub(
            r'^hero_image:\s*".*"',
            f'hero_image: "{hero_url}"',
            text,
            count=1,
            flags=re.M,
        )
        text = re.sub(
            r'^hero_caption:\s*".*"',
            'hero_caption: "Photo: Picsum"',
            text,
            count=1,
            flags=re.M,
        )

        def repl_img(m: re.Match) -> str:
            return f"![{m.group(1)}]({inline_url})"

        new_text, count = re.subn(
            r"!\[([^\]]*)\]\(https?://[^)]+\)", repl_img, text, count=1
        )
        if count == 0:
            parts = new_text.split("---", 2)
            body = parts[2]
            body = (
                body.rstrip()
                + f"\n\n![Quiet everyday light]({inline_url})\n"
                + "*A still moment from an ordinary day.*\n"
            )
            new_text = "---" + parts[1] + "---" + body
        f.write_text(new_text, encoding="utf-8")

    ASSIGN.write_text(json.dumps(assign, indent=2))
    print(f"Updated {n} posts with {n} unique heroes + {n} unique inlines")


if __name__ == "__main__":
    main()
