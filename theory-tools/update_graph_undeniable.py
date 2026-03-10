#!/usr/bin/env python3
"""Add undeniability nodes: GUT scale, baryon asymmetry, 3+1 dims, r, w"""
import json
from pathlib import Path

GRAPH = Path(__file__).parent / "theory-graph.json"
with open(GRAPH, "r", encoding="utf-8") as f:
    g = json.load(f)

existing_ids = {n["id"] for n in g["nodes"]}

new_nodes = [
    {
        "id": "deriv-gut-scale-t4",
        "type": "derivation",
        "layer": "match",
        "domain": "physics",
        "label": "GUT scale: M_GUT = M_Pl * t4^2 = 1.12e16 GeV",
        "summary": "Grand unification scale from modular forms: M_GUT = M_Pl * theta_4^2 = 1.12e16 GeV. This is precisely the expected GUT scale (~10^16 GeV). theta_4 = 0.0303 squared gives the ratio M_GUT/M_Pl ~ 10^-3. Proton lifetime testable at Hyper-Kamiokande.",
        "formula": "M_GUT = M_Pl * theta_4^2",
        "accuracy": "99%",
        "confidence": 3,
        "status": "derived",
        "sources": ["theta4_undeniable.py"],
        "depends_on": ["claim-theta4-master-key"],
        "supports": [],
        "contradicts": [],
        "discovered": "2026-02-09",
        "tags": ["golden-node", "theta_4", "GUT", "unification"]
    },
    {
        "id": "pred-baryon-asymmetry-t4",
        "type": "prediction",
        "layer": "match",
        "domain": "cosmology",
        "label": "Baryon asymmetry: eta_B ~ t4^6/phi = 4.8e-10 (within 0.8x)",
        "summary": "Baryon-to-photon ratio eta_B ~ theta_4^6/phi = 4.79e-10 vs measured 6.1e-10. Order of magnitude from pure modular forms (log10 off by 0.10). Six domain wall layers of theta_4 attenuation divided by phi gives matter-antimatter asymmetry.",
        "formula": "eta_B ~ theta_4^6 / phi",
        "accuracy": "order-of-magnitude",
        "confidence": 2,
        "status": "claimed",
        "sources": ["theta4_undeniable.py"],
        "depends_on": ["claim-theta4-master-key"],
        "supports": [],
        "contradicts": [],
        "discovered": "2026-02-09",
        "tags": ["golden-node", "theta_4", "baryon-asymmetry", "cosmology"]
    },
    {
        "id": "pred-tensor-scalar-r",
        "type": "prediction",
        "layer": "match",
        "domain": "cosmology",
        "label": "Tensor-to-scalar ratio: r = 16*t4^2/t3^2 = 0.00225",
        "summary": "Inflation tensor-to-scalar ratio from modular forms: r = 16*theta_4^2/theta_3^2 = 0.00225. This equals the slow-roll result r = 16/(2*N_e^2) where N_e = 2h = 60. Current bound r < 0.036: comfortably consistent. Detectable by next-gen CMB experiments (CMB-S4, LiteBIRD).",
        "formula": "r = 16 * theta_4^2 / theta_3^2",
        "accuracy": "prediction",
        "confidence": 3,
        "status": "predicted",
        "sources": ["theta4_undeniable.py"],
        "depends_on": ["claim-theta4-master-key"],
        "supports": [],
        "contradicts": [],
        "discovered": "2026-02-09",
        "tags": ["golden-node", "theta_4", "inflation", "prediction", "testable"]
    },
    {
        "id": "pred-dark-energy-w",
        "type": "prediction",
        "layer": "interpretation",
        "domain": "cosmology",
        "label": "Dark energy w = -1 exactly (vacuum identity)",
        "summary": "Dark energy equation of state w = -1 exactly predicted. Omega_DE = 1 - eta*phi^2 is a vacuum identity, not dynamics. Dark energy is 'everything not modular matter'. PREDICTION: future measurements will converge to w = -1.000. Current measurement w = -1.03 +/- 0.03: consistent within 1 sigma.",
        "formula": "w = -1 (exact)",
        "accuracy": "prediction",
        "confidence": 4,
        "status": "predicted",
        "sources": ["theta4_undeniable.py"],
        "depends_on": ["deriv-omega-de-modular"],
        "supports": [],
        "contradicts": [],
        "discovered": "2026-02-09",
        "tags": ["golden-node", "dark-energy", "prediction", "testable"]
    },
    {
        "id": "claim-3plus1-from-4a2",
        "type": "claim",
        "layer": "interpretation",
        "domain": "physics",
        "label": "3+1 dimensions = 3 visible A2 + 1 dark A2",
        "summary": "The 3+1 structure of spacetime mirrors the 4A2 sublattice split: 3 visible A2 copies permuted by S3 (= spatial rotations) and 1 dark A2 (= time, distinguished, irreversible via Pisot property of phi). The 3:1 ratio is the SAME mathematical structure in both cases.",
        "formula": "3+1 = 3(visible A2) + 1(dark A2)",
        "accuracy": "structural",
        "confidence": 3,
        "status": "claimed",
        "sources": ["theta4_undeniable.py"],
        "depends_on": ["deriv-golden-node"],
        "supports": [],
        "contradicts": [],
        "discovered": "2026-02-09",
        "tags": ["golden-node", "dimensions", "spacetime", "interpretation"]
    },
]

new_edges = [
    {"from": "claim-theta4-master-key", "to": "deriv-gut-scale-t4", "type": "explains", "weight": 0.9},
    {"from": "claim-theta4-master-key", "to": "pred-baryon-asymmetry-t4", "type": "explains", "weight": 0.5},
    {"from": "claim-theta4-master-key", "to": "pred-tensor-scalar-r", "type": "explains", "weight": 0.8},
    {"from": "deriv-omega-de-modular", "to": "pred-dark-energy-w", "type": "derives", "weight": 1.0},
    {"from": "claim-3plus1-from-4a2", "to": "deriv-golden-node", "type": "derives", "weight": 0.7},
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
