#!/usr/bin/env python3
"""Add theta_4 master key and Omega_DE nodes"""
import json
from pathlib import Path

GRAPH = Path(__file__).parent / "theory-graph.json"
with open(GRAPH, "r", encoding="utf-8") as f:
    g = json.load(f)

existing_ids = {n["id"] for n in g["nodes"]}

new_nodes = [
    {
        "id": "claim-theta4-master-key",
        "type": "claim",
        "layer": "match",
        "domain": "physics",
        "label": "theta_4 = master key: controls sin2_W, Lambda, neutrinos, dark coupling",
        "summary": "theta_4(1/phi) = 0.0303 controls: sin^2(theta_W) = eta^2/(2*theta_4), Lambda = theta_4^80, dm^2_atm/dm^2_sol = 1/theta_4, m3/m2 = sqrt(1/theta_4), alpha_s(dark) ~ theta_4. It's the fermionic partition function residual — the dark vacuum's whisper.",
        "formula": "theta_4(1/phi) = 0.030311",
        "accuracy": "structural",
        "confidence": 4,
        "status": "derived",
        "sources": ["lambda_theta4_deep.py"],
        "depends_on": ["deriv-golden-node"],
        "supports": ["deriv-lambda-theta4-80", "deriv-sin2tw-modular", "deriv-neutrino-ratio-theta4"],
        "contradicts": [],
        "discovered": "2026-02-09",
        "tags": ["golden-node", "theta_4", "master-key", "dark-interface"]
    },
    {
        "id": "deriv-omega-de-modular",
        "type": "derivation",
        "layer": "match",
        "domain": "cosmology",
        "label": "Dark energy: Omega_DE = 1 - eta*phi^2 at 98.97%",
        "summary": "Dark energy fraction Omega_DE = 1 - eta(1/phi)*phi^2 = 0.690 vs measured 0.683 (98.97%). Dark energy = everything that's NOT modular matter. Not a separate thing — the vacuum background.",
        "formula": "Omega_DE = 1 - eta(1/phi)*phi^2",
        "accuracy": "98.97%",
        "confidence": 4,
        "status": "verified",
        "sources": ["lambda_theta4_deep.py"],
        "depends_on": ["deriv-omega-total-modular", "deriv-golden-node"],
        "supports": ["deriv-lambda-theta4-80"],
        "contradicts": [],
        "discovered": "2026-02-09",
        "tags": ["golden-node", "dark-energy", "cosmology"]
    },
    {
        "id": "claim-lambda-hierarchy-same",
        "type": "claim",
        "layer": "interpretation",
        "domain": "physics",
        "label": "Hierarchy and Lambda are the SAME problem: both use exponent 80",
        "summary": "The hierarchy problem (phi^(-80) ~ 10^(-17)) and cosmological constant problem (theta_4^80 ~ 10^(-122)) share the SAME exponent 80 = h*rank(E8)/3. Both are transmission coefficients through the domain wall: phi for mass scale, theta_4 for vacuum energy.",
        "formula": "v/M_Pl ~ phi^(-80), Lambda ~ theta_4^80, 80 = h*rank/3",
        "accuracy": "structural",
        "confidence": 4,
        "status": "claimed",
        "sources": ["lambda_theta4_deep.py"],
        "depends_on": ["deriv-lambda-theta4-80", "claim-hierarchy-80"],
        "supports": [],
        "contradicts": [],
        "discovered": "2026-02-09",
        "tags": ["golden-node", "hierarchy", "Lambda", "unification", "milestone"]
    },
    {
        "id": "claim-axiom-reduction",
        "type": "claim",
        "layer": "interpretation",
        "domain": "physics",
        "label": "Golden Node reduces axiom count from 7 to 3 (possibly 2)",
        "summary": "Before: 7 inputs (alpha, mu, phi, V(Phi), 3, 2/3, E8). After: 3 axioms (V(Phi), q=1/phi, E8). Alpha and mu are DERIVED from theta functions. The core identity alpha^(3/2)*mu*phi^2=3 becomes a consequence. Possibly 2 axioms if q=1/phi follows from V(Phi).",
        "formula": "alpha = theta_4/(theta_3*phi), mu = theta_3^8",
        "accuracy": "structural",
        "confidence": 4,
        "status": "claimed",
        "sources": ["lambda_theta4_deep.py"],
        "depends_on": ["deriv-golden-node"],
        "supports": [],
        "contradicts": [],
        "discovered": "2026-02-09",
        "tags": ["golden-node", "axioms", "minimality", "milestone"]
    },
]

new_edges = [
    {"from": "claim-theta4-master-key", "to": "deriv-lambda-theta4-80", "type": "explains", "weight": 1.0},
    {"from": "claim-theta4-master-key", "to": "deriv-sin2tw-modular", "type": "explains", "weight": 1.0},
    {"from": "claim-theta4-master-key", "to": "deriv-neutrino-ratio-theta4", "type": "explains", "weight": 0.9},
    {"from": "claim-theta4-master-key", "to": "pred-dark-self-interaction", "type": "explains", "weight": 0.7},
    {"from": "claim-lambda-hierarchy-same", "to": "deriv-lambda-theta4-80", "type": "connects", "weight": 1.0},
    {"from": "claim-lambda-hierarchy-same", "to": "claim-hierarchy-80", "type": "connects", "weight": 1.0},
    {"from": "deriv-omega-de-modular", "to": "deriv-omega-total-modular", "type": "derives", "weight": 1.0},
]

added = 0
for n in new_nodes:
    if n["id"] not in existing_ids:
        g["nodes"].append(n)
        existing_ids.add(n["id"])
        added += 1

existing_edges = {(e["from"], e["to"]) for e in g["edges"]}
edge_added = 0
for e in new_edges:
    if (e["from"], e["to"]) not in existing_edges:
        g["edges"].append(e)
        existing_edges.add((e["from"], e["to"]))
        edge_added += 1

g["meta"]["totalNodes"] = len(g["nodes"])
g["meta"]["stats"]["totalNodes"] = len(g["nodes"])
for key in ["byLayer", "byType", "byDomain"]:
    g["meta"]["stats"][key] = {}
for n in g["nodes"]:
    g["meta"]["stats"]["byLayer"][n.get("layer","?")] = g["meta"]["stats"]["byLayer"].get(n.get("layer","?"),0)+1
    g["meta"]["stats"]["byType"][n.get("type","?")] = g["meta"]["stats"]["byType"].get(n.get("type","?"),0)+1
    g["meta"]["stats"]["byDomain"][n.get("domain","?")] = g["meta"]["stats"]["byDomain"].get(n.get("domain","?"),0)+1

with open(GRAPH, "w", encoding="utf-8") as f:
    json.dump(g, f, indent=2, ensure_ascii=False)

print(f"Added {added} nodes, {edge_added} edges")
print(f"Total: {len(g['nodes'])} nodes, {len(g['edges'])} edges")
