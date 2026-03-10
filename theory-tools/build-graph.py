"""
build-graph.py — Rebuild theory-graph.json from multiple sources.

Usage:
    python build-graph.py              # Full rebuild
    python build-graph.py --scan-only  # Report what would change, don't write

Sources (in priority order):
1. theory-graph.json — new hand-curated nodes (preserved as-is)
2. theory.json — legacy 463-node graph (migrated to new schema)
3. public/full-theory/findings/ — HTML files with content-boxes
4. public/full-theory/raw-llm/ — markdown conversation artifacts

Output: theory-graph.json (updated in-place, merging new + legacy)
"""

import json
import os
import re
import sys
from pathlib import Path
from datetime import date

# Handle Windows console encoding
if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SCRIPT_DIR = Path(__file__).parent
ROOT = SCRIPT_DIR.parent
GRAPH_PATH = SCRIPT_DIR / "theory-graph.json"
LEGACY_PATH = ROOT / "theory.json"
LAYERED_PATH = ROOT / "theory-layered.json"
FINDINGS_DIR = ROOT / "public" / "full-theory" / "findings"
RAW_LLM_DIR = ROOT / "public" / "full-theory" / "raw-llm"

# Domain inference from node IDs
DOMAIN_PATTERNS = {
    "physics": ["alpha", "gauge", "quark", "lepton", "higgs", "boson", "hadron",
                 "nucleon", "ckm", "pmns", "lagrangian", "potential", "coupling",
                 "renormalization", "qed", "qcd", "electroweak", "speed-of-light",
                 "planck", "vacuum", "domain-wall", "kink"],
    "biology": ["water", "aromatic", "chlorophyll", "photosynthesis", "anesthesia",
                "membrane", "protein", "dna", "rna", "codon", "amino", "cell",
                "neurotransmit", "serotonin", "dopamine", "melatonin", "tryptophan",
                "ez-water", "biointerfacial", "libet"],
    "consciousness": ["consciousness", "awareness", "qualia", "experience",
                      "free-will", "agency", "sleep", "dream", "meditation",
                      "psychedelic", "anesthesia", "nde"],
    "cosmology": ["dark-matter", "dark-energy", "omega", "hubble", "cosmic",
                  "black-hole", "cosmological", "universe", "cmb", "baryonic"],
    "math": ["e8", "lucas", "fibonacci", "golden-ratio", "weyl", "normalizer",
             "a2", "root-system", "lattice", "group", "algebra"],
}

# Layer inference
LAYER_KEYWORDS = {
    "algebra": ["deriv", "proof", "identity", "equation", "potential", "lagrangian",
                "kink", "bound-state", "lucas", "e8", "normalizer"],
    "match": ["match", "fit", "accuracy", "derivation", "predict", "measured",
              "comparison", "wavelength", "mass-ratio"],
    "interpretation": ["claim", "interpret", "consciousness", "meaning", "narrative",
                       "philosophy", "implication", "speculative"],
}


def infer_domain(node_id, label=""):
    """Guess domain from node ID and label."""
    text = (node_id + " " + label).lower()
    scores = {}
    for domain, keywords in DOMAIN_PATTERNS.items():
        scores[domain] = sum(1 for kw in keywords if kw in text)
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "physics"


def infer_layer(node_id, node_type, label=""):
    """Guess layer from node ID and type."""
    text = (node_id + " " + node_type + " " + label).lower()
    if node_type in ("fact", "anomaly"):
        return "match"
    if node_type in ("boundary", "open"):
        return "interpretation"
    if node_type == "falsifies":
        return "algebra"
    scores = {}
    for layer, keywords in LAYER_KEYWORDS.items():
        scores[layer] = sum(1 for kw in keywords if kw in text)
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "match"


def migrate_legacy_node(legacy_node, layered_lookup):
    """Convert a theory.json node to theory-graph.json schema."""
    nid = legacy_node["id"]
    ntype = legacy_node.get("type", "claim")
    label = legacy_node.get("label", nid)
    content = legacy_node.get("content", "")

    # Skip pure structural nodes
    if ntype in ("index", "link", "supported_by", "supports", "weakened_by", "weakens"):
        return None

    # Normalize type
    type_map = {
        "anomalie": "anomaly",
        "predictions": "prediction",
    }
    ntype = type_map.get(ntype, ntype)

    # Get layer from layered.json if available
    layer_info = layered_lookup.get(nid, {})
    layer = layer_info.get("layer", infer_layer(nid, ntype, label))
    if layer == "other" or layer == "science":
        layer = infer_layer(nid, ntype, label)

    # Get domain
    domain = layer_info.get("domain", infer_domain(nid, label))
    if domain == "unknown":
        domain = infer_domain(nid, label)

    # Build depends_on from backlinks
    depends_on = []
    for bl in legacy_node.get("backlinks", []):
        if bl.get("type") in ("supported_by", "link"):
            depends_on.append(bl["from"])

    # Build supports from supports array
    supports = []
    for s in legacy_node.get("supports", []):
        if isinstance(s, dict):
            supports.append(s.get("id", ""))
        elif isinstance(s, str):
            supports.append(s)

    # Extract first sentence as summary
    summary = content.split(".")[0].strip() if content else label
    if len(summary) > 200:
        summary = summary[:197] + "..."

    return {
        "id": nid,
        "type": ntype,
        "layer": layer,
        "domain": domain,
        "label": label,
        "summary": summary,
        "formula": None,
        "accuracy": None,
        "confidence": legacy_node.get("confidence", 2),
        "status": legacy_node.get("status", "claimed"),
        "sources": legacy_node.get("sources", []),
        "depends_on": depends_on,
        "supports": supports,
        "contradicts": [],
        "discovered": None,
        "tags": [ntype, domain, layer],
    }


def scan_findings(findings_dir):
    """Scan HTML findings for potential new nodes."""
    found = []
    if not findings_dir.exists():
        return found

    for fpath in findings_dir.iterdir():
        if fpath.suffix not in (".html", ".md"):
            continue

        text = fpath.read_text(encoding="utf-8", errors="replace")
        # Look for content-box titles
        for match in re.finditer(r'class="box-title"[^>]*>(.*?)</p>', text, re.DOTALL):
            title = re.sub(r"<[^>]+>", "", match.group(1)).strip()
            if title:
                found.append({
                    "source": str(fpath.relative_to(ROOT)),
                    "label": title,
                    "type": "finding",
                })

        # Look for h2/h3 headers
        for match in re.finditer(r"<h[23][^>]*>(.*?)</h[23]>", text, re.DOTALL):
            title = re.sub(r"<[^>]+>", "", match.group(1)).strip()
            if title and len(title) > 3:
                found.append({
                    "source": str(fpath.relative_to(ROOT)),
                    "label": title,
                    "type": "section",
                })

    return found


def scan_raw_llm(raw_dir):
    """Scan raw LLM conversations for unlinked discoveries."""
    found = []
    if not raw_dir.exists():
        return found

    for fpath in raw_dir.iterdir():
        if fpath.suffix not in (".md", ".txt", ".html"):
            continue

        text = fpath.read_text(encoding="utf-8", errors="replace")
        rel = str(fpath.relative_to(ROOT))

        # Look for markdown headers (# style)
        for match in re.finditer(r"^#{1,3}\s+(.+)$", text, re.MULTILINE):
            title = match.group(1).strip()
            if title and len(title) > 3:
                found.append({
                    "source": rel,
                    "label": title,
                    "type": "raw-llm-section",
                })

        # Look for plain-text section headers (short lines preceded by blank line)
        for match in re.finditer(r"\n\s*\n\s{0,4}([A-Z][^\n]{3,80})\s*\n", text):
            title = match.group(1).strip()
            # Filter out sentences (headers are typically short, no periods mid-text)
            if title and len(title) < 80 and "." not in title[:-1]:
                found.append({
                    "source": rel,
                    "label": title,
                    "type": "raw-llm-section",
                })

        # Also add the file itself as an item (filename = topic)
        stem = fpath.stem
        if stem and len(stem) > 2:
            found.append({
                "source": rel,
                "label": stem,
                "type": "raw-llm-file",
            })

    return found


def cross_reference(nodes, findings, raw_items):
    """Find mentions of existing node labels in new material."""
    cross_refs = []
    node_labels = {n["id"]: n["label"].lower() for n in nodes}

    all_sources = findings + raw_items
    for item in all_sources:
        item_text = item["label"].lower()
        for nid, nlabel in node_labels.items():
            # Check if any significant word overlap
            label_words = set(w for w in nlabel.split() if len(w) > 3)
            item_words = set(w for w in item_text.split() if len(w) > 3)
            overlap = label_words & item_words
            if len(overlap) >= 2:
                cross_refs.append({
                    "node_id": nid,
                    "found_in": item["source"],
                    "matched_words": list(overlap),
                })

    return cross_refs


def main():
    scan_only = "--scan-only" in sys.argv

    # 1. Load existing theory-graph.json (new curated nodes)
    if GRAPH_PATH.exists():
        with open(GRAPH_PATH, "r", encoding="utf-8") as f:
            graph = json.load(f)
    else:
        graph = {"meta": {}, "nodeTypes": {}, "nodes": [], "edges": []}

    curated_ids = {n["id"] for n in graph["nodes"]}
    print(f"Curated nodes in theory-graph.json: {len(curated_ids)}")

    # 2. Load legacy theory.json
    legacy_nodes = []
    if LEGACY_PATH.exists():
        with open(LEGACY_PATH, "r", encoding="utf-8") as f:
            legacy = json.load(f)
        legacy_nodes = legacy.get("nodes", [])
        legacy_edges = legacy.get("edges", [])
        print(f"Legacy nodes in theory.json: {len(legacy_nodes)}")
    else:
        legacy_edges = []
        print("No theory.json found")

    # 3. Load layered.json for layer/domain hints
    layered_lookup = {}
    if LAYERED_PATH.exists():
        with open(LAYERED_PATH, "r", encoding="utf-8") as f:
            layered = json.load(f)
        for n in layered.get("nodes", []):
            layered_lookup[n["id"]] = n
        print(f"Layered hints: {len(layered_lookup)} nodes")

    # 4. Migrate legacy nodes (skip those already curated)
    migrated_count = 0
    skipped_count = 0
    for ln in legacy_nodes:
        if ln["id"] in curated_ids:
            skipped_count += 1
            continue
        migrated = migrate_legacy_node(ln, layered_lookup)
        if migrated:
            graph["nodes"].append(migrated)
            curated_ids.add(migrated["id"])
            migrated_count += 1

    print(f"Migrated from legacy: {migrated_count} (skipped {skipped_count} structural/duplicate)")

    # 5. Migrate legacy edges (dedup against existing)
    existing_edges = {(e["from"], e["to"]) for e in graph.get("edges", [])}
    edge_count = 0
    for e in legacy_edges:
        key = (e["from"], e["to"])
        if key not in existing_edges:
            graph["edges"].append({
                "from": e["from"],
                "to": e["to"],
                "type": e.get("type", "link"),
                "weight": e.get("weight"),
            })
            existing_edges.add(key)
            edge_count += 1
    print(f"Migrated edges: {edge_count} new ({len(existing_edges)} total)")

    # 6. Scan findings/ and raw-llm/
    findings = scan_findings(FINDINGS_DIR)
    raw_items = scan_raw_llm(RAW_LLM_DIR)
    print(f"\nScanned findings/: {len(findings)} items")
    print(f"Scanned raw-llm/: {len(raw_items)} items")

    # 7. Cross-reference
    cross_refs = cross_reference(graph["nodes"], findings, raw_items)
    print(f"Cross-references found: {len(cross_refs)}")

    # 8. Find orphan nodes (no depends_on and no supports)
    orphans = []
    all_ids = {n["id"] for n in graph["nodes"]}
    for n in graph["nodes"]:
        deps = [d for d in n.get("depends_on", []) if d in all_ids]
        sups = [s for s in n.get("supports", []) if s in all_ids]
        if not deps and not sups and n["type"] not in ("fact", "boundary", "falsifies"):
            orphans.append(n["id"])

    # 9. Update stats
    by_layer = {}
    by_type = {}
    by_domain = {}
    for n in graph["nodes"]:
        layer = n.get("layer", "unknown")
        by_layer[layer] = by_layer.get(layer, 0) + 1
        ntype = n.get("type", "unknown")
        by_type[ntype] = by_type.get(ntype, 0) + 1
        domain = n.get("domain", "unknown")
        by_domain[domain] = by_domain.get(domain, 0) + 1

    graph["meta"]["totalNodes"] = len(graph["nodes"])
    graph["meta"]["lastModified"] = str(date.today())
    graph["meta"]["stats"] = {
        "totalNodes": len(graph["nodes"]),
        "byLayer": by_layer,
        "byType": by_type,
        "byDomain": by_domain,
    }

    # 10. Report
    print(f"\n{'='*60}")
    print(f"SUMMARY")
    print(f"{'='*60}")
    print(f"Total nodes: {len(graph['nodes'])}")
    print(f"  By layer:  {json.dumps(by_layer)}")
    print(f"  By type:   {json.dumps(by_type)}")
    print(f"  By domain: {json.dumps(by_domain)}")
    print(f"Total edges: {len(graph['edges'])}")
    print(f"Orphan nodes: {len(orphans)}")
    if orphans[:10]:
        print(f"  First 10: {orphans[:10]}")
    print(f"New cross-references: {len(cross_refs)}")
    if cross_refs[:5]:
        for cr in cross_refs[:5]:
            print(f"  {cr['node_id']} <- {cr['found_in']} ({cr['matched_words']})")

    # 11. Write output
    if not scan_only:
        with open(GRAPH_PATH, "w", encoding="utf-8") as f:
            json.dump(graph, f, indent=2, ensure_ascii=False)
        print(f"\nWritten to {GRAPH_PATH}")
    else:
        print(f"\n[SCAN ONLY] Would write {len(graph['nodes'])} nodes to {GRAPH_PATH}")


if __name__ == "__main__":
    main()
