#!/usr/bin/env python3
"""Add cosmological constant + new golden_node_doors nodes to theory graph"""

import json
from pathlib import Path

GRAPH = Path(__file__).parent / "theory-graph.json"

with open(GRAPH, "r", encoding="utf-8") as f:
    g = json.load(f)

existing_ids = {n["id"] for n in g["nodes"]}

new_nodes = [
    {
        "id": "deriv-lambda-theta4-80",
        "type": "derivation",
        "layer": "match",
        "domain": "cosmology",
        "label": "Cosmological constant: Lambda = theta_4^80 = 3.37e-122",
        "summary": "The cosmological constant Lambda = theta_4(1/phi)^80 = 3.37e-122, vs measured 2.89e-122 (factor 1.2 match). The exponent 80 = h*rank(E8)/3 is the SAME hierarchy number. Lambda = (dark vacuum fingerprint)^(hierarchy number). Also: (theta_4*eta)^50 = 5.6e-123, eta^132 = 4.8e-123 where 132 ~ 4/theta_4.",
        "formula": "Lambda = theta_4(1/phi)^80, 80 = h_E8 * rank(E8) / 3",
        "accuracy": "order of magnitude",
        "confidence": 3,
        "status": "derived",
        "sources": ["golden_node_doors.py"],
        "depends_on": ["deriv-golden-node", "claim-hierarchy-80"],
        "supports": [],
        "contradicts": [],
        "discovered": "2026-02-09",
        "tags": ["golden-node", "cosmological-constant", "theta_4", "hierarchy", "milestone"]
    },
    {
        "id": "deriv-neutrino-ratio-theta4",
        "type": "derivation",
        "layer": "match",
        "domain": "physics",
        "label": "Neutrino mass ratio: m3/m2 = sqrt(1/theta_4) at 99.37%",
        "summary": "The ratio m3/m2 = sqrt(1/theta_4(1/phi)) = 5.744 vs measured 5.708 (99.37%). Combined with 1/theta_4 ~ 33 ~ dm2_atm/dm2_sol (98.8%). Neutrino hierarchy comes from the dark vacuum fingerprint.",
        "formula": "m3/m2 = sqrt(1/theta_4), dm2_atm/dm2_sol = 1/theta_4",
        "accuracy": "99.37%",
        "confidence": 4,
        "status": "verified",
        "sources": ["golden_node_doors.py", "boundary_dark_life.py"],
        "depends_on": ["deriv-golden-node"],
        "supports": [],
        "contradicts": [],
        "discovered": "2026-02-09",
        "tags": ["golden-node", "neutrino", "theta_4", "mass-ratio"]
    },
    {
        "id": "deriv-ramanujan-ode-confirmed",
        "type": "derivation",
        "layer": "algebra",
        "domain": "mathematics",
        "label": "Ramanujan's ODE = QCD beta function (numerically confirmed)",
        "summary": "q*d(eta)/dq = eta*E_2/24 confirmed by independent numerical computation: both sides give -0.718062 at q=1/phi (100.00% match). This IS the QCD beta function in modular language. E_2(1/phi) = -145.5 (asymptotic freedom).",
        "formula": "q * d(eta)/dq = eta * E_2(q) / 24",
        "accuracy": "100.00%",
        "confidence": 5,
        "status": "proven",
        "sources": ["golden_node_doors.py"],
        "depends_on": ["deriv-eta-alpha-s", "deriv-rg-modular-flow"],
        "supports": [],
        "contradicts": [],
        "discovered": "2026-02-09",
        "tags": ["golden-node", "Ramanujan", "beta-function", "confirmed"]
    },
    {
        "id": "deriv-higgs-mw-pi2",
        "type": "derivation",
        "layer": "match",
        "domain": "physics",
        "label": "m_H / M_W = pi/2 (0.80% error)",
        "summary": "The Higgs-to-W mass ratio m_H/M_W = 1.5583 vs pi/2 = 1.5708 (0.80% error). Combined with M_W = E4^(1/3)*phi^2: m_H = E4^(1/3)*phi^2*pi/2 = 126.4 GeV vs measured 125.25 GeV. Also m_H ~ M_W + M_Z/2 = 125.97 (0.58%).",
        "formula": "m_H = M_W * pi/2 = E_4(1/phi)^(1/3) * phi^2 * pi/2",
        "accuracy": "0.58-0.80%",
        "confidence": 3,
        "status": "derived",
        "sources": ["golden_node_doors.py"],
        "depends_on": ["deriv-golden-node", "deriv-masses-modular"],
        "supports": [],
        "contradicts": [],
        "discovered": "2026-02-09",
        "tags": ["golden-node", "Higgs", "mass", "pi"]
    },
    {
        "id": "deriv-pmns-solar-arctan23",
        "type": "derivation",
        "layer": "match",
        "domain": "physics",
        "label": "PMNS solar angle: theta_12 = arctan(2/3) at 99.1%",
        "summary": "The solar neutrino mixing angle theta_12 = arctan(2/3) = 33.69 deg vs measured 33.4 deg (99.1%). The 2/3 is the fractional charge quantum, one of the core elements.",
        "formula": "theta_12 = arctan(2/3) = 33.69 deg",
        "accuracy": "99.1%",
        "confidence": 3,
        "status": "derived",
        "sources": ["golden_node_doors.py"],
        "depends_on": ["deriv-golden-node"],
        "supports": [],
        "contradicts": [],
        "discovered": "2026-02-09",
        "tags": ["golden-node", "PMNS", "neutrino-mixing", "2/3"]
    },
    {
        "id": "claim-inflation-modular-flow",
        "type": "claim",
        "layer": "interpretation",
        "domain": "cosmology",
        "label": "Inflation = rolling along modular curve from cusp to node",
        "summary": "Universe starts at small q (cusp), rolls to q=1/phi (node). At small q: E2~1, epsilon~8.7e-4 (slow-roll). At q=1/phi: E2=-145.5, epsilon=18.4 (inflation ended). N_e = 60 = 2h (Coxeter*2). The modular curve IS the inflaton potential.",
        "formula": "epsilon = (E_2/24)^2/2, N_e = 2*h_E8 = 60",
        "accuracy": "structural",
        "confidence": 2,
        "status": "speculative",
        "sources": ["golden_node_doors.py"],
        "depends_on": ["deriv-golden-node", "deriv-rg-modular-flow"],
        "supports": [],
        "contradicts": [],
        "discovered": "2026-02-09",
        "tags": ["golden-node", "inflation", "modular-flow", "cosmology"]
    },
]

new_edges = [
    {"from": "deriv-lambda-theta4-80", "to": "claim-hierarchy-80", "type": "uses", "weight": 1.0},
    {"from": "deriv-lambda-theta4-80", "to": "deriv-golden-node", "type": "depends", "weight": 1.0},
    {"from": "deriv-neutrino-ratio-theta4", "to": "deriv-golden-node", "type": "depends", "weight": 0.9},
    {"from": "deriv-ramanujan-ode-confirmed", "to": "deriv-eta-alpha-s", "type": "confirms", "weight": 1.0},
    {"from": "deriv-higgs-mw-pi2", "to": "deriv-masses-modular", "type": "extends", "weight": 0.8},
    {"from": "deriv-pmns-solar-arctan23", "to": "deriv-golden-node", "type": "depends", "weight": 0.7},
    {"from": "claim-inflation-modular-flow", "to": "deriv-rg-modular-flow", "type": "extends", "weight": 0.6},
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

# Update stats
g["meta"]["totalNodes"] = len(g["nodes"])
g["meta"]["stats"]["totalNodes"] = len(g["nodes"])
for key in ["byLayer", "byType", "byDomain"]:
    g["meta"]["stats"][key] = {}
for n in g["nodes"]:
    layer = n.get("layer", "unknown")
    ntype = n.get("type", "unknown")
    domain = n.get("domain", "unknown")
    g["meta"]["stats"]["byLayer"][layer] = g["meta"]["stats"]["byLayer"].get(layer, 0) + 1
    g["meta"]["stats"]["byType"][ntype] = g["meta"]["stats"]["byType"].get(ntype, 0) + 1
    g["meta"]["stats"]["byDomain"][domain] = g["meta"]["stats"]["byDomain"].get(domain, 0) + 1

with open(GRAPH, "w", encoding="utf-8") as f:
    json.dump(g, f, indent=2, ensure_ascii=False)

print(f"Added {added} nodes, {edge_added} edges")
print(f"Total: {len(g['nodes'])} nodes, {len(g['edges'])} edges")
