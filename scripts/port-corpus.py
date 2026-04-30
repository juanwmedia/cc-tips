#!/usr/bin/env python3
"""
port-corpus.py — orchestration for porting tips from ~/.claude/skills/claude-code-tip/examples
into the cc-tips plugin.

Two modes:
  --pair      Pair source files by frontmatter (title_es, title_en) tuple,
              query wmedia.es DB once via SSH for hub_topic mapping, write
              .port/pair-index.json.
  --manifest  Read frontmatter and content from cleaned tip files in tips/,
              join with topic data from pair-index.json, sort by date, assign
              ids 1..N, write manifest.json.

Pure mechanical: pairing + DB lookup + manifest assembly. Does NOT transform
tip content. Content transformation between --pair and --manifest is done by
LLM workers.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

PLUGIN_ROOT = Path(os.path.expanduser("~/code/cc-tips"))
EXAMPLES_DIR = Path(os.path.expanduser("~/.claude/skills/claude-code-tip/examples"))
DB_HOST = "forge@frontendleap.com"
DB_PATH = "/home/forge/wmedia.es/database/database.sqlite"
GH_OWNER = "juanwmedia"
GH_REPO = "cc-tips"
WMEDIA_BASE = "https://wmedia.es"
RAW_BASE = f"https://raw.githubusercontent.com/{GH_OWNER}/{GH_REPO}/main/tips"
VALID_TOPICS = {
    "skills", "mcp", "hooks", "subagents", "plugins", "memory-context",
    "models-cost", "permissions", "sessions", "autonomous", "fundamentals",
}
DEFAULT_TOPIC = "fundamentals"


def parse_frontmatter(text: str) -> dict | None:
    m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return None
    fm = {}
    for line in m.group(1).splitlines():
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        fm[key.strip()] = value.strip().strip('"').strip("'")
    return fm


def read_examples() -> list[tuple[Path, dict]]:
    out = []
    for path in sorted(EXAMPLES_DIR.glob("*.md")):
        text = path.read_text()
        fm = parse_frontmatter(text)
        if fm is None:
            print(f"WARNING: no frontmatter in {path.name}", file=sys.stderr)
            continue
        out.append((path, fm))
    return out


def pair_files(files: list[tuple[Path, dict]]) -> tuple[list[dict], list]:
    groups = defaultdict(list)
    for path, fm in files:
        key = (fm.get("title_es", ""), fm.get("title_en", ""))
        if not key[0] or not key[1]:
            print(f"WARNING: missing titles in {path.name}", file=sys.stderr)
            continue
        groups[key].append((path, fm))

    pairs = []
    singletons = []
    for key, members in groups.items():
        if len(members) != 2:
            singletons.append({"key": list(key), "files": [p.name for p, _ in members]})
            continue
        es_member = next((p for p, _ in members if p.name.endswith("-es.md")), None)
        en_member = next((p for p, _ in members if p.name.endswith("-en.md")), None)
        if es_member is None or en_member is None:
            singletons.append({"key": list(key), "files": [p.name for p, _ in members]})
            continue

        slug_es = es_member.stem[:-3] if es_member.stem.endswith("-es") else es_member.stem
        slug_en = en_member.stem[:-3] if en_member.stem.endswith("-en") else en_member.stem

        date = None
        for _, fm in members:
            if "date" in fm:
                date = fm["date"]
                break

        pairs.append({
            "title_es": key[0],
            "title_en": key[1],
            "slug_es": slug_es,
            "slug_en": slug_en,
            "date": date,
            "source_es": str(es_member),
            "source_en": str(en_member),
        })
    return pairs, singletons


def fetch_topic_map() -> dict[str, str]:
    """Return {slug: hub_topic} keyed by both slug_en and slug_es."""
    sql = "SELECT slug_en, slug_es, COALESCE(hub_topic, '') FROM tips;"
    cmd = ["ssh", DB_HOST, f"sqlite3 -separator '|' {DB_PATH} \"{sql}\""]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=30)
    except subprocess.CalledProcessError as e:
        print(f"DB query failed: {e.stderr}", file=sys.stderr)
        sys.exit(1)
    except subprocess.TimeoutExpired:
        print("DB query timed out", file=sys.stderr)
        sys.exit(1)

    topic_map = {}
    for line in result.stdout.splitlines():
        parts = line.split("|")
        if len(parts) != 3:
            continue
        slug_en, slug_es, topic = parts
        topic = topic if topic in VALID_TOPICS else ""
        if slug_en:
            topic_map[slug_en] = topic
        if slug_es:
            topic_map[slug_es] = topic
    return topic_map


def cmd_pair() -> int:
    files = read_examples()
    pairs, singletons = pair_files(files)
    print(f"Paired: {len(pairs)} | Singletons: {len(singletons)}", file=sys.stderr)

    topic_map = fetch_topic_map()
    print(f"Topic map entries: {len(topic_map)}", file=sys.stderr)

    untagged = []
    for pair in pairs:
        topic = topic_map.get(pair["slug_en"]) or topic_map.get(pair["slug_es"]) or ""
        if not topic:
            untagged.append(pair["slug_en"])
            topic = DEFAULT_TOPIC
        pair["topic"] = topic

    out_dir = PLUGIN_ROOT / ".port"
    out_dir.mkdir(parents=True, exist_ok=True)
    pair_index_path = out_dir / "pair-index.json"
    pair_index_path.write_text(
        json.dumps({"pairs": pairs, "singletons": singletons}, indent=2, ensure_ascii=False)
    )
    print(f"Wrote {pair_index_path}", file=sys.stderr)

    if untagged:
        (PLUGIN_ROOT / "port-untagged.txt").write_text("\n".join(untagged) + "\n")
        print(
            f"WARNING: {len(untagged)} tips lacked a hub_topic in DB; defaulted to '{DEFAULT_TOPIC}'. See port-untagged.txt",
            file=sys.stderr,
        )

    if singletons:
        (PLUGIN_ROOT / "port-singletons.txt").write_text(
            json.dumps(singletons, indent=2, ensure_ascii=False) + "\n"
        )

    return 0


def extract_summary(content: str) -> str:
    """Extract a one-line summary from TL;DR or first paragraph after frontmatter."""
    m = re.match(r"^---\n.*?\n---\n", content, re.DOTALL)
    body = content[m.end():] if m else content
    body = body.strip()

    tldr = re.search(
        r"^>\s*\*\*TL;DR\*\*:?\s*(.+?)(?:\n\s*\n|\Z)",
        body,
        re.MULTILINE | re.DOTALL,
    )
    if tldr:
        text = re.sub(r"\s+", " ", tldr.group(1).strip())
        return text[:300]

    paragraphs = re.split(r"\n\s*\n", body)
    for p in paragraphs:
        p = p.strip()
        if not p or p.startswith("#") or p.startswith("```") or p.startswith(">"):
            continue
        text = re.sub(r"\s+", " ", p)
        return text[:300]
    return ""


def cmd_manifest() -> int:
    pair_index_path = PLUGIN_ROOT / ".port" / "pair-index.json"
    if not pair_index_path.exists():
        print(f"Missing {pair_index_path}. Run --pair first.", file=sys.stderr)
        return 1

    pair_data = json.loads(pair_index_path.read_text())
    pairs = pair_data["pairs"]
    pairs.sort(key=lambda p: p.get("date", "") or "")

    tips_dir = PLUGIN_ROOT / "tips"
    if not tips_dir.exists():
        print(f"Missing {tips_dir}. Worker batch did not produce cleaned tips.", file=sys.stderr)
        return 1

    entries = []
    missing_count = 0
    for idx, pair in enumerate(pairs, start=1):
        slug_es = pair["slug_es"]
        slug_en = pair["slug_en"]
        es_path = tips_dir / f"{slug_es}-es.md"
        en_path = tips_dir / f"{slug_en}-en.md"

        if not es_path.exists() or not en_path.exists():
            missing = []
            if not es_path.exists():
                missing.append(es_path.name)
            if not en_path.exists():
                missing.append(en_path.name)
            print(f"Tip {idx} ({slug_en}): missing files: {missing}", file=sys.stderr)
            missing_count += 1
            continue

        summary_es = extract_summary(es_path.read_text())
        summary_en = extract_summary(en_path.read_text())

        entries.append({
            "id": idx,
            "slug": slug_en,
            "slug_es": slug_es,
            "slug_en": slug_en,
            "topic": pair.get("topic", DEFAULT_TOPIC),
            "version": 1,
            "title_es": pair["title_es"],
            "title_en": pair["title_en"],
            "summary_es": summary_es,
            "summary_en": summary_en,
            "url_es": f"{RAW_BASE}/{slug_es}-es.md",
            "url_en": f"{RAW_BASE}/{slug_en}-en.md",
            "external_url_es": f"{WMEDIA_BASE}/es/tips/{slug_es}",
            "external_url_en": f"{WMEDIA_BASE}/en/tips/{slug_en}",
            "contributed_by_github_username": None,
        })

    manifest = {
        "version": "1.0.0",
        "tips": entries,
    }
    manifest_path = PLUGIN_ROOT / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False))
    print(f"Wrote {manifest_path} ({len(entries)} entries, {missing_count} skipped)", file=sys.stderr)
    return 0 if missing_count == 0 else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pair", action="store_true", help="pair sources + fetch topics")
    parser.add_argument("--manifest", action="store_true", help="assemble manifest from cleaned tips")
    args = parser.parse_args()

    if args.pair == args.manifest:
        parser.error("Specify exactly one of --pair or --manifest")

    return cmd_pair() if args.pair else cmd_manifest()


if __name__ == "__main__":
    sys.exit(main())
