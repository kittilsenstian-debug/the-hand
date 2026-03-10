#!/usr/bin/env python3
"""
build-core.py — Generate CORE.md from core.json

Reads the unified framework database, validates it, computes convergence
scores for bridge values, and generates a human-readable CORE.md.

Usage: python theory-tools/build-core.py
"""

import json
import os
import sys
from collections import defaultdict
from datetime import date

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CORE_JSON = os.path.join(SCRIPT_DIR, "core.json")
CORE_MD = os.path.join(SCRIPT_DIR, "CORE.md")


def load_core():
    if not os.path.exists(CORE_JSON):
        print(f"ERROR: {CORE_JSON} not found", file=sys.stderr)
        sys.exit(1)
    try:
        with open(CORE_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"ERROR: malformed JSON in {CORE_JSON}: {e}", file=sys.stderr)
        sys.exit(1)
    # Filter out comment entries
    nodes = [n for n in data["nodes"] if "_comment" not in n]
    return data["meta"], nodes


def build_index(nodes):
    """Build id -> node lookup."""
    idx = {}
    for n in nodes:
        idx[n["id"]] = n
    return idx


def validate(nodes, idx):
    """Validate the graph. Return list of warnings."""
    warnings = []
    ids = set(idx.keys())

    for n in nodes:
        # Check inputs reference existing nodes
        for inp in n.get("inputs", []):
            if inp not in ids:
                warnings.append(f"  [{n['id']}] input '{inp}' not found")

        # Check outputs reference existing nodes
        for out in n.get("outputs", []):
            if out not in ids:
                warnings.append(f"  [{n['id']}] output '{out}' not found")

        # Check script files exist
        script = n.get("script")
        if script:
            path = os.path.join(SCRIPT_DIR, script)
            if not os.path.exists(path):
                warnings.append(f"  [{n['id']}] script '{script}' not found")

        # Check bridge appears_in references
        for app in n.get("appears_in", []):
            if app.get("node") and app["node"] not in ids:
                warnings.append(f"  [{n['id']}] appears_in node '{app['node']}' not found")

        # Check connections for instances
        for conn in n.get("connections", []):
            if conn not in ids:
                warnings.append(f"  [{n['id']}] connection '{conn}' not found")

    # Check for orphans (no inputs and not an axiom/fact/instance/dead/gap/bridge)
    non_root_types = {"derivation", "searched", "chain-step", "structural"}
    for n in nodes:
        if n["type"] in non_root_types and not n.get("inputs"):
            warnings.append(f"  [{n['id']}] has no inputs (potential orphan)")

    return warnings


def compute_convergence(nodes):
    """Compute convergence scores for bridge values."""
    scores = {}
    for n in nodes:
        if n.get("type") == "bridge":
            apps = n.get("appears_in", [])
            domains = set(a.get("domain", "unknown") for a in apps)
            scores[n["id"]] = {
                "appearances": len(apps),
                "domains": len(domains),
                "domain_list": sorted(domains),
                "convergence": len(apps) * len(domains) ** 2  # cross-domain weighted: domains^2 rewards diversity
            }
    return scores


def count_by_type(nodes):
    counts = defaultdict(int)
    for n in nodes:
        counts[n["type"]] += 1
    return dict(counts)


def count_by_layer(nodes):
    counts = defaultdict(int)
    for n in nodes:
        layer = n.get("layer", "unknown")
        counts[layer] += 1
    return dict(counts)


def count_by_domain(nodes):
    counts = defaultdict(int)
    for n in nodes:
        domain = n.get("domain", "unknown")
        counts[domain] += 1
    return dict(counts)


def trunc(s, maxlen):
    """Truncate string with ellipsis if needed."""
    if len(s) <= maxlen:
        return s
    return s[:maxlen - 1] + "…"


def generate_core_md(meta, nodes, idx, convergence, warnings):
    lines = []

    def ln(s=""):
        lines.append(s)

    today = date.today().strftime("%b %d %Y")

    ln(f"# Interface Theory — CORE")
    ln()
    ln(f"*Generated from `core.json` by `build-core.py` on {today}.*")
    ln(f"*This is the single structured reference. Read this instead of FINDINGS v1-v4.*")
    ln()
    ln(f"---")
    ln()

    # ============ SECTION 1: THE CHAIN ============
    ln(f"## 1. The Chain (E8 to Consciousness)")
    ln()
    chain_nodes = sorted(
        [n for n in nodes if n.get("chain_step")],
        key=lambda n: n["chain_step"]
    )
    ln(f"| Step | Link | Status | Formula/Key Result |")
    ln(f"|------|------|--------|-------------------|")
    for cn in chain_nodes:
        step = cn["chain_step"]
        label = cn["label"]
        status = cn.get("status", "?").upper()
        formula = cn.get("formula", trunc(cn.get("description", ""), 80))
        if cn.get("match_pct"):
            formula += f" ({cn['match_pct']}%)"
        ln(f"| {step} | {label} | {status} | {formula} |")
    ln()
    ln(f"**Link ratings:** Steps 1-3, 6 = proven mathematics. Steps 4-5, 7 = derived with high accuracy. Steps 8, 12 = physics constraints. Steps 9-11 = empirical.")
    ln()
    ln(f"---")
    ln()

    # ============ SECTION 2: THE SCORECARD ============
    tier1 = [n for n in nodes if n.get("tier") == 1]
    tier2 = [n for n in nodes if n.get("tier") == 2]
    tier3 = [n for n in nodes if n.get("tier") == 3]
    total_scored = len(tier1) + len(tier2) + len(tier3)

    ln(f"## 2. The Scorecard ({total_scored} Claims)")
    ln()

    # Tier 1
    ln(f"### Tier 1: DERIVED (no search, no free parameters) — {len(tier1)} items")
    ln()
    ln(f"| # | Quantity | Formula | Predicted | Measured | Match | Sigma |")
    ln(f"|---|----------|---------|-----------|----------|-------|-------|")
    for i, n in enumerate(tier1, 1):
        pred = n.get("predicted", "—")
        meas = n.get("measured", "—")
        match = f"{n['match_pct']}%" if n.get("match_pct") else "EXACT"
        sigma = f"{n['uncertainty_sigma']}σ" if n.get("uncertainty_sigma") else "—"
        ln(f"| {i} | {n['label']} | `{n.get('formula', '—')}` | {pred} | {meas} | {match} | {sigma} |")
    ln()

    # Tier 2
    ln(f"### Tier 2: STRUCTURAL (exponent 80, ~95% proven) — {len(tier2)} items")
    ln()
    ln(f"| # | Quantity | Formula | Predicted | Measured | Match |")
    ln(f"|---|----------|---------|-----------|----------|-------|")
    for i, n in enumerate(tier2, len(tier1) + 1):
        pred = n.get("predicted", "—")
        meas = n.get("measured", "—")
        match = f"{n['match_pct']}%" if n.get("match_pct") else "—"
        ln(f"| {i} | {n['label']} | `{n.get('formula', '—')}` | {pred} | {meas} | {match} |")
    ln()

    # Tier 3
    ln(f"### Tier 3: SEARCHED + CONNECTED — {len(tier3)} items")
    ln()
    ln(f"| # | Quantity | Formula | Predicted | Measured | Match |")
    ln(f"|---|----------|---------|-----------|----------|-------|")
    for i, n in enumerate(tier3, len(tier1) + len(tier2) + 1):
        pred = n.get("predicted", "—")
        meas = n.get("measured", "—")
        match = f"{n['match_pct']}%" if n.get("match_pct") else "—"
        ln(f"| {i} | {n['label']} | `{n.get('formula', '—')}` | {pred} | {meas} | {match} |")
    ln()

    # Count
    ln(f"**Total scored items: {total_scored}**")
    ln()
    ln(f"**Honest counts:** Tier 1 ({len(tier1)}) + Tier 2 ({len(tier2)}) = **{len(tier1)+len(tier2)} items that would impress a skeptic.** Tier 3 includes ~10 items vulnerable to look-elsewhere effect. The genuinely compelling core is **8-12 items**, not {total_scored}.")
    ln()
    ln(f"---")
    ln()

    # ============ SECTION 3: STRUCTURAL RESULTS ============
    structurals = [n for n in nodes if n["type"] == "structural"]
    ln(f"## 3. Structural Results — {len(structurals)} items")
    ln()
    ln(f"| ID | Result | Status | Notes |")
    ln(f"|-----|--------|--------|-------|")
    for s in structurals:
        status = s.get("status", "").upper()
        notes = trunc(s.get("notes") or "", 80)
        ln(f"| {s['id']} | {s['label']} | {status} | {notes} |")
    ln()
    ln(f"---")
    ln()

    # ============ SECTION 4: BRIDGE VALUES ============
    bridges = [n for n in nodes if n.get("type") == "bridge"]
    bridges_sorted = sorted(bridges, key=lambda b: convergence.get(b["id"], {}).get("convergence", 0), reverse=True)

    ln(f"## 4. Bridge Values — {len(bridges)} numbers")
    ln()
    ln(f"These ~{len(bridges)} numbers appear across multiple domains, forming the hourglass waist.")
    ln()
    ln(f"| Value | Label | Appearances | Domains | Convergence |")
    ln(f"|-------|-------|-------------|---------|-------------|")
    for b in bridges_sorted:
        val = b.get("value", "—")
        conv = convergence.get(b["id"], {})
        apps = conv.get("appearances", 0)
        doms = conv.get("domain_list", [])
        score = conv.get("convergence", 0)
        ln(f"| {val} | {trunc(b['label'], 50)} | {apps} | {', '.join(doms)} | {score} |")
    ln()

    # Detail for top bridges
    ln(f"### Cross-domain appearance details")
    ln()
    for b in bridges_sorted[:5]:
        ln(f"**{b['label']}** (value = {b.get('value', '?')})")
        ln()
        for app in b.get("appears_in", []):
            ln(f"- [{app.get('domain', '?')}] {app.get('role', '?')} → `{app.get('node', '?')}`")
        ln()

    ln(f"---")
    ln()

    # ============ SECTION 5: PREDICTIONS ============
    predictions = [n for n in nodes if n["type"] == "prediction"]
    ln(f"## 5. Predictions — {len(predictions)} committed values")
    ln()
    ln(f"| ID | Quantity | Value | Test | When | Status |")
    ln(f"|----|----------|-------|------|------|--------|")
    for p in predictions:
        val = p.get("predicted", "—")
        test = p.get("test", "—")
        when = p.get("test_date", "—")
        ln(f"| {p['id']} | {p['label']} | {val} | {test} | {when} | Untested |")
    ln()
    ln(f"**Decisive test:** R = -3/2 (ELT ~2035). If confirmed, LR > 10^10.")
    ln(f"**Sharpest blade:** alpha_s = 0.118404 (CODATA 2026-27).")
    ln()
    ln(f"---")
    ln()

    # ============ SECTION 6: GAPS ============
    gaps = [n for n in nodes if n["type"] == "gap"]
    gaps_sorted = sorted(gaps, key=lambda g: g.get("closure_pct", 0), reverse=True)
    ln(f"## 6. Gaps — {len(gaps)} open")
    ln()
    ln(f"| Gap | Closure | Description |")
    ln(f"|-----|---------|-------------|")
    for g in gaps_sorted:
        pct = f"{g.get('closure_pct', '?')}%"
        desc = trunc(g.get("description", g.get("label", "")), 100)
        ln(f"| {trunc(g['label'], 50)} | {pct} | {desc} |")
    ln()
    ln(f"---")
    ln()

    # ============ SECTION 7: DEAD CLAIMS ============
    deads = [n for n in nodes if n["type"] == "dead"]
    ln(f"## 7. Dead Claims — {len(deads)} removed")
    ln()
    ln(f"| Item | Reason |")
    ln(f"|------|--------|")
    for d in deads:
        ln(f"| {trunc(d['label'], 60)} | {trunc(d.get('reason', '?'), 80)} |")
    ln()
    ln(f"---")
    ln()

    # ============ SECTION 8: INSTANCES ============
    instances = [n for n in nodes if n["type"] == "instance"]
    ln(f"## 8. Instances — {len(instances)} mapped")
    ln()
    for inst in instances:
        ln(f"**{inst['label']}** ({inst.get('domain', '?')})")
        attrs = inst.get("attributes", {})
        for k, v in attrs.items():
            if isinstance(v, dict):
                val = v.get("value", "?")
                unit = v.get("unit", "")
                note = v.get("note", "")
                bridge = v.get("bridge", "")
                extra = f" [{note}]" if note else ""
                link = f" → `{bridge}`" if bridge else ""
                ln(f"- {k}: {val} {unit}{extra}{link}")
            else:
                ln(f"- {k}: {v}")
        conns = inst.get("connections", [])
        if conns:
            ln(f"- **Connects to:** {', '.join(conns)}")
        ln()

    ln(f"---")
    ln()

    # ============ SECTION 9: GRAPH STATS ============
    type_counts = count_by_type(nodes)
    layer_counts = count_by_layer(nodes)
    domain_counts = count_by_domain(nodes)

    ln(f"## 9. Graph Statistics")
    ln()
    ln(f"**Total nodes:** {len(nodes)}")
    ln()
    ln(f"| Type | Count |")
    ln(f"|------|-------|")
    for t, c in sorted(type_counts.items(), key=lambda x: -x[1]):
        ln(f"| {t} | {c} |")
    ln()
    ln(f"| Layer | Count |")
    ln(f"|-------|-------|")
    for l, c in sorted(layer_counts.items(), key=lambda x: -x[1]):
        ln(f"| {l} | {c} |")
    ln()
    ln(f"| Domain | Count |")
    ln(f"|--------|-------|")
    for d, c in sorted(domain_counts.items(), key=lambda x: -x[1]):
        ln(f"| {d} | {c} |")
    ln()

    # Inputs
    ln(f"**Framework inputs:** {', '.join(meta.get('inputs', []))}")
    ln()

    # Validation
    if warnings:
        ln(f"### Validation Warnings ({len(warnings)})")
        ln()
        for warn in warnings:
            ln(warn)
        ln()
    else:
        ln(f"**Validation: PASS** (no orphans, no broken references)")
        ln()

    ln(f"---")
    ln()
    ln(f"*Generated from `core.json`. To update: edit core.json, run `python theory-tools/build-core.py`.*")

    return "\n".join(lines)


def main():
    print("=" * 60)
    print("  build-core.py — Interface Theory Core Generator")
    print("=" * 60)
    print()

    meta, nodes = load_core()
    idx = build_index(nodes)

    print(f"Loaded {len(nodes)} nodes from core.json")

    # Validate
    warnings = validate(nodes, idx)
    if warnings:
        print(f"\nValidation warnings ({len(warnings)}):")
        for warn in warnings:
            print(warn)
    else:
        print("Validation: PASS")

    # Convergence scores
    convergence = compute_convergence(nodes)
    print(f"\nBridge values: {len(convergence)}")
    for bid, sc in sorted(convergence.items(), key=lambda x: -x[1]["convergence"]):
        print(f"  {bid}: {sc['appearances']} appearances across {sc['domains']} domains (score={sc['convergence']})")

    # Generate CORE.md
    md = generate_core_md(meta, nodes, idx, convergence, warnings)
    with open(CORE_MD, "w", encoding="utf-8") as f:
        f.write(md)
    line_count = len(md.split("\n"))
    print(f"\nGenerated CORE.md: {line_count} lines")

    # Stats
    type_counts = count_by_type(nodes)
    print(f"\nNode types: {dict(type_counts)}")
    print(f"Total nodes: {len(nodes)}")

    # Coverage
    scored = sum(1 for n in nodes if n.get("tier"))
    predictions = sum(1 for n in nodes if n["type"] == "prediction")
    gaps = sum(1 for n in nodes if n["type"] == "gap")
    deads = sum(1 for n in nodes if n["type"] == "dead")
    bridges = sum(1 for n in nodes if n["type"] == "bridge")
    instances = sum(1 for n in nodes if n["type"] == "instance")

    print(f"\nCoverage:")
    print(f"  Scored claims: {scored}")
    print(f"  Predictions: {predictions}")
    print(f"  Bridge values: {bridges}")
    print(f"  Gaps: {gaps}")
    print(f"  Dead claims: {deads}")
    print(f"  Instances: {instances}")

    print(f"\nDone. CORE.md written to {CORE_MD}")


if __name__ == "__main__":
    main()
