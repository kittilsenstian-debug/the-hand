"""
cross-reference.py — Check any file/folder against theory-graph.json

Usage:
    python cross-reference.py <path>            # Scan file or folder
    python cross-reference.py --orphans         # Find disconnected nodes
    python cross-reference.py --stats           # Show graph statistics

Examples:
    python cross-reference.py public/full-theory/raw-llm/
    python cross-reference.py "public/full-theory/findings/2026-02-08.html"
    python cross-reference.py --orphans
"""

import json
import os
import re
import sys
from pathlib import Path
from collections import defaultdict

# Handle Windows console encoding
if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SCRIPT_DIR = Path(__file__).parent
ROOT = SCRIPT_DIR.parent
GRAPH_PATH = SCRIPT_DIR / "theory-graph.json"


def load_graph():
    """Load theory-graph.json."""
    if not GRAPH_PATH.exists():
        print(f"ERROR: {GRAPH_PATH} not found. Run build-graph.py first.")
        sys.exit(1)
    with open(GRAPH_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def tokenize(text):
    """Extract significant words from text."""
    text = re.sub(r"<[^>]+>", " ", text)  # strip HTML
    text = re.sub(r"[^a-zA-Z0-9\s\-_/.]", " ", text)
    words = text.lower().split()
    # Filter short/common words
    stopwords = {"the", "and", "for", "are", "but", "not", "you", "all",
                 "can", "had", "her", "was", "one", "our", "out", "has",
                 "this", "that", "with", "from", "they", "been", "have",
                 "many", "some", "them", "than", "its", "over", "such",
                 "into", "also", "more", "very", "what", "when", "where",
                 "which", "their", "will", "each", "make", "like", "just",
                 "would", "could", "should", "about", "there", "these",
                 "those", "being", "other", "after", "before", "between"}
    return [w for w in words if len(w) > 2 and w not in stopwords]


def build_index(graph):
    """Build search index from graph nodes."""
    index = {}  # word -> set of node IDs
    node_map = {}  # id -> node

    for node in graph["nodes"]:
        nid = node["id"]
        node_map[nid] = node

        # Index by label words
        label_words = tokenize(node.get("label", ""))
        for w in label_words:
            index.setdefault(w, set()).add(nid)

        # Index by tags
        for tag in node.get("tags", []):
            for w in tag.lower().split("-"):
                if len(w) > 2:
                    index.setdefault(w, set()).add(nid)

        # Index by summary words
        summary_words = tokenize(node.get("summary", ""))
        for w in summary_words:
            index.setdefault(w, set()).add(nid)

    return index, node_map


def scan_file(fpath, index, node_map):
    """Scan a single file and find matching nodes."""
    text = fpath.read_text(encoding="utf-8", errors="replace")
    words = tokenize(text)
    word_set = set(words)

    # Score each node by word overlap
    scores = defaultdict(lambda: {"score": 0, "words": []})

    for word in word_set:
        if word in index:
            for nid in index[word]:
                scores[nid]["score"] += 1
                if len(scores[nid]["words"]) < 5:
                    scores[nid]["words"].append(word)

    # Sort by score, filter low scores
    ranked = sorted(scores.items(), key=lambda x: -x[1]["score"])
    return [(nid, data) for nid, data in ranked if data["score"] >= 3]


def find_new_concepts(fpath, index, node_map):
    """Find potential NEW concepts in a file not in the graph."""
    text = fpath.read_text(encoding="utf-8", errors="replace")
    new_items = []

    # Look for markdown headers
    for match in re.finditer(r"^#{1,3}\s+(.+)$", text, re.MULTILINE):
        title = match.group(1).strip()
        if title and len(title) > 5:
            # Check if already in graph
            title_words = set(tokenize(title))
            best_overlap = 0
            for node in node_map.values():
                label_words = set(tokenize(node.get("label", "")))
                overlap = len(title_words & label_words)
                best_overlap = max(best_overlap, overlap)
            if best_overlap < 2:
                new_items.append(title)

    # Look for plain-text headers
    for match in re.finditer(r"\n\s*\n\s{0,4}([A-Z][^\n]{5,80})\s*\n", text):
        title = match.group(1).strip()
        if "." not in title[:-1]:
            title_words = set(tokenize(title))
            best_overlap = 0
            for node in node_map.values():
                label_words = set(tokenize(node.get("label", "")))
                overlap = len(title_words & label_words)
                best_overlap = max(best_overlap, overlap)
            if best_overlap < 2:
                new_items.append(title)

    # Look for HTML headers
    for match in re.finditer(r"<h[23][^>]*>(.*?)</h[23]>", text, re.DOTALL):
        title = re.sub(r"<[^>]+>", "", match.group(1)).strip()
        if title and len(title) > 5:
            title_words = set(tokenize(title))
            best_overlap = 0
            for node in node_map.values():
                label_words = set(tokenize(node.get("label", "")))
                overlap = len(title_words & label_words)
                best_overlap = max(best_overlap, overlap)
            if best_overlap < 2:
                new_items.append(title)

    return new_items


def show_orphans(graph, node_map):
    """Find nodes with no connections."""
    all_ids = set(node_map.keys())
    # Collect all referenced IDs
    referenced = set()
    for n in graph["nodes"]:
        for d in n.get("depends_on", []):
            referenced.add(d)
        for s in n.get("supports", []):
            referenced.add(s)
    for e in graph.get("edges", []):
        referenced.add(e["from"])
        referenced.add(e["to"])

    orphans = []
    for n in graph["nodes"]:
        nid = n["id"]
        has_deps = any(d in all_ids for d in n.get("depends_on", []))
        has_sups = any(s in all_ids for s in n.get("supports", []))
        is_referenced = nid in referenced
        if not has_deps and not has_sups and not is_referenced:
            if n["type"] not in ("boundary", "falsifies"):
                orphans.append(n)

    return orphans


def show_stats(graph):
    """Display graph statistics."""
    stats = graph.get("meta", {}).get("stats", {})
    print(f"\n{'='*60}")
    print(f"Theory Graph Statistics")
    print(f"{'='*60}")
    print(f"Total nodes: {stats.get('totalNodes', len(graph['nodes']))}")
    print(f"Total edges: {len(graph.get('edges', []))}")
    print(f"\nBy layer:")
    for k, v in sorted(stats.get("byLayer", {}).items()):
        print(f"  {k:20s} {v:4d}")
    print(f"\nBy type:")
    for k, v in sorted(stats.get("byType", {}).items(), key=lambda x: -x[1]):
        print(f"  {k:20s} {v:4d}")
    print(f"\nBy domain (top 10):")
    domains = sorted(stats.get("byDomain", {}).items(), key=lambda x: -x[1])
    for k, v in domains[:10]:
        print(f"  {k:25s} {v:4d}")
    if len(domains) > 10:
        print(f"  ... and {len(domains)-10} more domains")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    graph = load_graph()
    index, node_map = build_index(graph)

    if sys.argv[1] == "--orphans":
        orphans = show_orphans(graph, node_map)
        print(f"\nOrphan nodes (no connections): {len(orphans)}")
        for n in orphans[:30]:
            print(f"  [{n['type']:12s}] {n['id']}")
            print(f"    {n.get('label', '')[:70]}")
        if len(orphans) > 30:
            print(f"  ... and {len(orphans)-30} more")
        return

    if sys.argv[1] == "--stats":
        show_stats(graph)
        return

    target = Path(sys.argv[1])
    if not target.exists():
        target = ROOT / sys.argv[1]
    if not target.exists():
        print(f"ERROR: {sys.argv[1]} not found")
        sys.exit(1)

    # Collect files to scan
    if target.is_dir():
        files = [f for f in target.rglob("*") if f.suffix in (".md", ".txt", ".html")]
    else:
        files = [target]

    total_matches = 0
    total_new = 0

    for fpath in sorted(files):
        rel = fpath.relative_to(ROOT) if fpath.is_relative_to(ROOT) else fpath
        matches = scan_file(fpath, index, node_map)
        new_concepts = find_new_concepts(fpath, index, node_map)

        if matches or new_concepts:
            print(f"\n{'='*60}")
            print(f"FILE: {rel}")
            print(f"{'='*60}")

        if matches:
            print(f"\n  MATCHED NODES ({len(matches)}):")
            for nid, data in matches[:15]:
                node = node_map[nid]
                layer = node.get("layer", "?")
                ntype = node.get("type", "?")
                score = data["score"]
                words = ", ".join(data["words"][:3])
                print(f"    [{layer:13s}|{ntype:12s}] {node.get('label', nid)[:50]}")
                print(f"      score={score}, matched: {words}")
            if len(matches) > 15:
                print(f"    ... and {len(matches)-15} more matches")
            total_matches += len(matches)

        if new_concepts:
            print(f"\n  POTENTIAL NEW FINDINGS ({len(new_concepts)}):")
            for title in new_concepts[:10]:
                print(f"    -> {title}")
            if len(new_concepts) > 10:
                print(f"    ... and {len(new_concepts)-10} more")
            total_new += len(new_concepts)

    print(f"\n{'='*60}")
    print(f"SUMMARY: {len(files)} files scanned")
    print(f"  Matched nodes: {total_matches}")
    print(f"  Potential new findings: {total_new}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
