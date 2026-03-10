#!/usr/bin/env python3
"""Prune weak orphans, wire strong orphans, convert depends_on/supports to edges."""
import json
from pathlib import Path
from collections import Counter

GRAPH = Path(__file__).parent / "theory-graph.json"
with open(GRAPH, "r", encoding="utf-8") as f:
    g = json.load(f)

existing_ids = {n["id"] for n in g["nodes"]}
existing_edges = {(e["from"], e["to"]) for e in g["edges"]}

# --- PHASE 1: Convert depends_on / supports to edges ---
edge_added = 0
for n in g["nodes"]:
    nid = n["id"]
    for dep in n.get("depends_on", []):
        if dep in existing_ids and (dep, nid) not in existing_edges:
            g["edges"].append({"from": dep, "to": nid, "type": "derives", "weight": 0.7})
            existing_edges.add((dep, nid))
            edge_added += 1
    for sup in n.get("supports", []):
        if sup in existing_ids and (nid, sup) not in existing_edges:
            g["edges"].append({"from": nid, "to": sup, "type": "supports", "weight": 0.5})
            existing_edges.add((nid, sup))
            edge_added += 1

print(f"Phase 1: Wired {edge_added} edges from depends_on/supports fields")

# --- PHASE 2: Identify remaining orphans ---
edge_nodes = set()
for e in g["edges"]:
    edge_nodes.add(e["from"])
    edge_nodes.add(e["to"])

orphans = [n for n in g["nodes"] if n["id"] not in edge_nodes]
print(f"Remaining orphans after wiring: {len(orphans)}")

# --- PHASE 3: Prune weak orphans (confidence <= 1 AND orphaned) ---
prune_ids = set()
for o in orphans:
    if o.get("confidence", 0) <= 1:
        prune_ids.add(o["id"])
        print(f"  PRUNING [{o.get('confidence','?')}] {o['id']}: {o.get('label','')[:60]}")

g["nodes"] = [n for n in g["nodes"] if n["id"] not in prune_ids]
g["edges"] = [e for e in g["edges"] if e["from"] not in prune_ids and e["to"] not in prune_ids]
print(f"Phase 3: Pruned {len(prune_ids)} weak orphan nodes")

# --- PHASE 4: Auto-connect remaining orphans by tag/domain similarity ---
# Build tag index of connected nodes
connected_by_tag = {}
connected_by_domain = {}
for n in g["nodes"]:
    if n["id"] in edge_nodes and n["id"] not in prune_ids:
        for tag in n.get("tags", []):
            connected_by_tag.setdefault(tag, []).append(n["id"])
        dom = n.get("domain", "")
        connected_by_domain.setdefault(dom, []).append(n["id"])

auto_edges = 0
for o in [n for n in g["nodes"] if n["id"] not in edge_nodes]:
    # Try to find a connected node that shares tags
    best_match = None
    best_score = 0
    otags = set(o.get("tags", []))
    for tag in otags:
        for candidate in connected_by_tag.get(tag, []):
            # Count shared tags
            ctags = set()
            for cn in g["nodes"]:
                if cn["id"] == candidate:
                    ctags = set(cn.get("tags", []))
                    break
            shared = len(otags & ctags)
            if shared > best_score:
                best_score = shared
                best_match = candidate

    if best_match and best_score >= 1:
        key = (best_match, o["id"])
        if key not in existing_edges:
            g["edges"].append({"from": best_match, "to": o["id"], "type": "related", "weight": 0.3})
            existing_edges.add(key)
            auto_edges += 1
    else:
        # Connect to hub node of same domain
        dom = o.get("domain", "physics")
        hub_map = {
            "physics": "deriv-core-identity",
            "cosmology": "deriv-alpha-cancellation",
            "biology": "claim-biology-interface",
            "consciousness": "claim-consciousness-wall",
            "neuroscience": "claim-consciousness-wall",
            "math": "deriv-potential",
            "chemistry": "claim-biology-interface",
            "biochemistry": "claim-biology-interface",
        }
        hub = hub_map.get(dom, "deriv-core-identity")
        if hub in existing_ids:
            key = (hub, o["id"])
            if key not in existing_edges:
                g["edges"].append({"from": hub, "to": o["id"], "type": "context", "weight": 0.2})
                existing_edges.add(key)
                auto_edges += 1

print(f"Phase 4: Auto-connected {auto_edges} orphans by tag/domain similarity")

# --- PHASE 5: Downgrade orphans with confidence 2 that are type 'claim' or 'fit' ---
downgraded = 0
for n in g["nodes"]:
    if n["id"] not in edge_nodes and n.get("confidence", 0) == 2 and n.get("type") in ("claim", "fit"):
        # Don't delete, but mark as needs-review
        n.setdefault("tags", []).append("needs-review")
        downgraded += 1

print(f"Phase 5: Tagged {downgraded} weak claims as needs-review")

# --- PHASE 6: Final stats ---
edge_nodes_final = set()
for e in g["edges"]:
    edge_nodes_final.add(e["from"])
    edge_nodes_final.add(e["to"])

final_orphans = [n for n in g["nodes"] if n["id"] not in edge_nodes_final]
print(f"\nFinal state:")
print(f"  Nodes: {len(g['nodes'])} (was 392)")
print(f"  Edges: {len(g['edges'])} (was 701)")
print(f"  Orphans: {len(final_orphans)} (was 156)")

# Update meta
g["meta"]["totalNodes"] = len(g["nodes"])
g["meta"]["stats"]["totalNodes"] = len(g["nodes"])
for key in ["byLayer", "byType", "byDomain"]:
    g["meta"]["stats"][key] = {}
for n in g["nodes"]:
    for key, field in [("byLayer", "layer"), ("byType", "type"), ("byDomain", "domain")]:
        val = n.get(field, "?")
        g["meta"]["stats"][key][val] = g["meta"]["stats"][key].get(val, 0) + 1

with open(GRAPH, "w", encoding="utf-8") as f:
    json.dump(g, f, indent=2, ensure_ascii=False)

print(f"\nSaved to {GRAPH}")

# Print remaining orphan summary
if final_orphans:
    print(f"\nRemaining {len(final_orphans)} orphans:")
    for o in final_orphans[:15]:
        label = o.get('label','')[:60].encode('ascii', 'replace').decode()
    print(f"  [{o.get('confidence','?')}] {o['id']}: {label}")
