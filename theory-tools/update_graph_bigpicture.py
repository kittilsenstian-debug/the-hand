#!/usr/bin/env python3
"""Add big picture + near-cusp discoveries to graph."""
import json
from pathlib import Path

GRAPH = Path(__file__).parent / "theory-graph.json"
with open(GRAPH, "r", encoding="utf-8") as f:
    g = json.load(f)

existing_ids = {n["id"] for n in g["nodes"]}

new_nodes = [
    {
        "id": "deriv-hierarchy-t4-corrected",
        "type": "derivation",
        "layer": "match",
        "domain": "physics",
        "label": "v = M_Pl*phibar^80/(1-phi*t4) at 99.58%",
        "summary": "Electroweak hierarchy CORRECTED by theta_4: v = M_Pl*phibar^80/(1-phi*t4) = 245.19 GeV vs 246.22 GeV. Up from 94.7% (uncorrected). The dark vacuum renormalizes the hierarchy exponential through phi*theta_4 = golden ratio times dark fingerprint.",
        "formula": "v = M_Pl * phibar^80 / (1 - phi*theta_4)",
        "accuracy": "99.58%",
        "confidence": 4,
        "status": "verified",
        "sources": ["near_cusp_physics.py"],
        "depends_on": ["claim-theta4-master-key", "deriv-golden-node"],
        "supports": [],
        "contradicts": [],
        "discovered": "2026-02-09",
        "tags": ["hierarchy", "theta_4", "electroweak", "correction", "breakthrough"]
    },
    {
        "id": "deriv-omega-dm-t4-corrected",
        "type": "derivation",
        "layer": "match",
        "domain": "cosmology",
        "label": "Omega_DM = (phi/6)(1-t4) at 99.69%",
        "summary": "Dark matter density with theta_4 correction: Omega_DM = (phi/6)(1-theta_4) = 0.2615 vs 0.2607. Up from phi/6 = 0.2697 (96.56%). The dark vacuum leakage suppresses the geometric dark matter density.",
        "formula": "Omega_DM = (phi/6)(1 - theta_4)",
        "accuracy": "99.69%",
        "confidence": 4,
        "status": "verified",
        "sources": ["big_picture.py"],
        "depends_on": ["claim-theta4-master-key", "deriv-alpha-cancellation"],
        "supports": [],
        "contradicts": [],
        "discovered": "2026-02-09",
        "tags": ["dark-matter", "theta_4", "cosmological", "correction"]
    },
    {
        "id": "pred-breathing-mode-76GeV",
        "type": "prediction",
        "layer": "match",
        "domain": "physics",
        "label": "Breathing mode = m_H*sqrt(3/8) = 76.7 GeV",
        "summary": "Domain wall breathing mode from Poschl-Teller: m_B = m_H*sqrt(3/8) = 76.7 GeV (definitive). After V(Phi) shift to symmetric form V=lambda*(Psi^2-5/4)^2, standard kink analysis gives exactly 2 bound states: zero mode (Higgs) and breathing at sqrt(3/8)*m_H. Previous 108.5 GeV was incorrect lambda. With 8*t4 correction: 95.3 GeV (matches CMS 95.4 excess).",
        "formula": "m_B = m_H * sqrt(3/8) = 76.7 GeV",
        "accuracy": "prediction",
        "confidence": 4,
        "status": "predicted",
        "sources": ["near_cusp_physics.py"],
        "depends_on": ["deriv-domain-wall-bound-states", "deriv-potential"],
        "supports": [],
        "contradicts": [],
        "discovered": "2026-02-09",
        "tags": ["breathing-mode", "Poschl-Teller", "prediction", "testable", "CMS"]
    },
    {
        "id": "claim-t4-universal-correction",
        "type": "claim",
        "layer": "interpretation",
        "domain": "physics",
        "label": "theta_4 is a universal dark-vacuum correction",
        "summary": "Every tree-level prediction gets a (1-k*t4) correction from dark vacuum leakage. Demonstrated: V_us (97.4->99.5%), Omega_DM (96.6->99.7%), hierarchy (94.7->99.6%), V_ub (95.8->98.7%). Direction: (1-t4) for dark-suppressed, (1+t4) for enhanced quantities.",
        "formula": "X_corrected = X_tree * (1 +/- k*theta_4)",
        "accuracy": "structural",
        "confidence": 4,
        "status": "claimed",
        "sources": ["big_picture.py", "near_cusp_physics.py"],
        "depends_on": ["claim-theta4-master-key"],
        "supports": [],
        "contradicts": [],
        "discovered": "2026-02-09",
        "tags": ["theta_4", "universal", "correction", "dark-vacuum"]
    },
    {
        "id": "claim-near-cusp-geometry",
        "type": "claim",
        "layer": "algebra",
        "domain": "physics",
        "label": "q=1/phi is near-cusp: j=5.4e18, tau=0.077i",
        "summary": "At q=1/phi: j-invariant = 5.4e18 (nearly degenerate), tau = 0.077i (near cusp), discriminant nearly zero. The elliptic curve is an extremely elongated torus (almost a cylinder = domain wall). The hierarchy exists BECAUSE the degeneration is almost but not quite complete. E6^2/E4^3 = 1 to 15 digits. sqrt(|E6/E4|) = 13.06 = F(7) at 99.56%.",
        "formula": "j(1/phi) = 5.4e18, tau = i*ln(phi)/(2*pi)",
        "accuracy": "structural",
        "confidence": 5,
        "status": "derived",
        "sources": ["big_picture.py", "near_cusp_physics.py"],
        "depends_on": ["deriv-golden-node"],
        "supports": [],
        "contradicts": [],
        "discovered": "2026-02-09",
        "tags": ["near-cusp", "j-invariant", "modular", "geometry", "domain-wall"]
    },
]

new_edges = [
    {"from": "claim-theta4-master-key", "to": "deriv-hierarchy-t4-corrected", "type": "explains", "weight": 1.0},
    {"from": "claim-theta4-master-key", "to": "deriv-omega-dm-t4-corrected", "type": "explains", "weight": 0.9},
    {"from": "deriv-golden-node", "to": "claim-near-cusp-geometry", "type": "derives", "weight": 1.0},
    {"from": "claim-theta4-master-key", "to": "claim-t4-universal-correction", "type": "explains", "weight": 1.0},
    {"from": "deriv-potential", "to": "pred-breathing-mode-76GeV", "type": "derives", "weight": 0.9},
    {"from": "claim-near-cusp-geometry", "to": "deriv-hierarchy-t4-corrected", "type": "supports", "weight": 0.8},
]

existing_edges = {(e["from"], e["to"]) for e in g["edges"]}
added_n = 0
for n in new_nodes:
    if n["id"] not in existing_ids:
        g["nodes"].append(n)
        existing_ids.add(n["id"])
        added_n += 1

added_e = 0
for e in new_edges:
    if (e["from"], e["to"]) not in existing_edges:
        g["edges"].append(e)
        existing_edges.add((e["from"], e["to"]))
        added_e += 1

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

print(f"Added {added_n} nodes, {added_e} edges")
print(f"Total: {len(g['nodes'])} nodes, {len(g['edges'])} edges")
