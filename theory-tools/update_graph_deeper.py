#!/usr/bin/env python3
"""Add deeper theta_4 findings: Cabibbo correction, Lambda_QCD, Hubble tension, confinement, Koide"""
import json
from pathlib import Path

GRAPH = Path(__file__).parent / "theory-graph.json"
with open(GRAPH, "r", encoding="utf-8") as f:
    g = json.load(f)

existing_ids = {n["id"] for n in g["nodes"]}

new_nodes = [
    {
        "id": "deriv-vus-t4-corrected",
        "type": "derivation",
        "layer": "match",
        "domain": "physics",
        "label": "V_us = (phi/7)(1-t4) at 99.49% (Cabibbo angle)",
        "summary": "Cabibbo angle corrected by theta_4: V_us = (phi/7)(1-theta_4) = 0.2241 vs measured 0.2253 (99.49%). Up from phi/7 alone at 97.40%. The dark fingerprint theta_4 = 0.030 corrects the CKM mixing. V_ud = sqrt(1-(phi/7)^2) = 0.9729 (99.92%).",
        "formula": "V_us = (phi/7)(1 - theta_4)",
        "accuracy": "99.49%",
        "confidence": 4,
        "status": "verified",
        "sources": ["theta4_deeper.py"],
        "depends_on": ["claim-theta4-master-key"],
        "supports": [],
        "contradicts": [],
        "discovered": "2026-02-09",
        "tags": ["golden-node", "theta_4", "CKM", "Cabibbo"]
    },
    {
        "id": "deriv-lambda-qcd-phi",
        "type": "derivation",
        "layer": "match",
        "domain": "physics",
        "label": "Lambda_QCD = m_p/phi^3 at 97.93%",
        "summary": "QCD confinement scale from golden ratio: Lambda_QCD = m_p/phi^3 = 0.2215 GeV vs measured 0.217 GeV (97.93%). The proton mass divided by phi-cubed gives the scale where QCD confines.",
        "formula": "Lambda_QCD = m_p / phi^3",
        "accuracy": "97.93%",
        "confidence": 3,
        "status": "verified",
        "sources": ["theta4_deeper.py"],
        "depends_on": ["deriv-golden-node"],
        "supports": [],
        "contradicts": [],
        "discovered": "2026-02-09",
        "tags": ["golden-node", "QCD", "confinement"]
    },
    {
        "id": "claim-hubble-tension-t4",
        "type": "claim",
        "layer": "interpretation",
        "domain": "cosmology",
        "label": "Hubble tension: H_late/H_early ~ (1+t4)^3",
        "summary": "The Hubble tension ratio H0(local)/H0(Planck) = 1.083 may be explained by (1+theta_4)^3 = 1.094 (within 1%). Three layers of theta_4 correction between early and late universe. Also: eta*t4*8*pi = 0.090 vs needed 0.083 correction.",
        "formula": "H_late/H_early ~ (1 + theta_4)^3",
        "accuracy": "~99%",
        "confidence": 2,
        "status": "claimed",
        "sources": ["theta4_deeper.py"],
        "depends_on": ["claim-theta4-master-key"],
        "supports": [],
        "contradicts": [],
        "discovered": "2026-02-09",
        "tags": ["golden-node", "theta_4", "Hubble-tension", "cosmology"]
    },
    {
        "id": "claim-eta-peak-confinement",
        "type": "claim",
        "layer": "interpretation",
        "domain": "physics",
        "label": "Eta function peak at q=0.037 = confinement scale",
        "summary": "The Dedekind eta function peaks at q ~ 0.037 with eta_max = 0.838, encoding QCD confinement. At q < 0.037 (UV), eta decreases (asymptotic freedom). At q > 0.037 (IR), eta decreases (deep confinement). The Standard Model at q=1/phi sits on the UV side.",
        "formula": "eta_max = 0.838 at q = 0.037",
        "accuracy": "structural",
        "confidence": 4,
        "status": "derived",
        "sources": ["theta4_deeper.py"],
        "depends_on": ["deriv-golden-node"],
        "supports": [],
        "contradicts": [],
        "discovered": "2026-02-09",
        "tags": ["golden-node", "eta", "confinement", "QCD"]
    },
    {
        "id": "claim-koide-charge-quantum",
        "type": "claim",
        "layer": "interpretation",
        "domain": "physics",
        "label": "Koide formula 2/3 = charge quantum (E8 embedding)",
        "summary": "The Koide formula (m_e+m_mu+m_tau)/(sqrt(m_e)+sqrt(m_mu)+sqrt(m_tau))^2 = 2/3 at 99.999% is not accidental. The 2/3 IS the fractional charge quantum from E8 -> SM gauge embedding. Same element {2/3} from our fundamental set {mu, phi, 3, 2/3}.",
        "formula": "Koide ratio = 2/3 (charge quantum)",
        "accuracy": "99.999%",
        "confidence": 4,
        "status": "claimed",
        "sources": ["theta4_deeper.py"],
        "depends_on": ["deriv-golden-node"],
        "supports": [],
        "contradicts": [],
        "discovered": "2026-02-09",
        "tags": ["golden-node", "Koide", "charge-quantum", "lepton-masses"]
    },
    {
        "id": "claim-137-derived",
        "type": "claim",
        "layer": "interpretation",
        "domain": "physics",
        "label": "137 is derived: 1/alpha = phi*t3/t4 (bosonic/fermionic ratio)",
        "summary": "The number 137 is NOT fundamental. It is the ratio 1/alpha = phi * theta_3/theta_4 = 136.39. This equals phi times the bosonic-to-fermionic partition function ratio at the Golden Node. The 'mystery of 137' dissolves in modular form language.",
        "formula": "1/alpha = phi * theta_3 / theta_4",
        "accuracy": "99.53%",
        "confidence": 4,
        "status": "derived",
        "sources": ["theta4_deeper.py"],
        "depends_on": ["claim-theta4-master-key", "deriv-golden-node"],
        "supports": [],
        "contradicts": [],
        "discovered": "2026-02-09",
        "tags": ["golden-node", "alpha", "137", "demystified"]
    },
    {
        "id": "pred-neutrino-sum-59",
        "type": "prediction",
        "layer": "match",
        "domain": "physics",
        "label": "Neutrino mass sum = 59.2 meV (testable)",
        "summary": "Complete neutrino spectrum: m1 = 0.54 meV, m2 = 8.69 meV (= m_e*alpha^4*6), m3 = 49.9 meV (= m2*sqrt(1/theta_4)). Total sum = 59.2 meV. Normal ordering predicted. Testable by DESI, Euclid, CMB-S4 (target sensitivity ~60 meV).",
        "formula": "m_nu_sum = m1 + m2 + m3 = 59.2 meV",
        "accuracy": "prediction",
        "confidence": 3,
        "status": "predicted",
        "sources": ["theta4_deeper.py"],
        "depends_on": ["claim-theta4-master-key"],
        "supports": [],
        "contradicts": [],
        "discovered": "2026-02-09",
        "tags": ["golden-node", "theta_4", "neutrinos", "prediction", "testable"]
    },
]

new_edges = [
    {"from": "claim-theta4-master-key", "to": "deriv-vus-t4-corrected", "type": "explains", "weight": 0.9},
    {"from": "claim-theta4-master-key", "to": "claim-hubble-tension-t4", "type": "explains", "weight": 0.5},
    {"from": "deriv-golden-node", "to": "claim-eta-peak-confinement", "type": "explains", "weight": 0.8},
    {"from": "deriv-golden-node", "to": "claim-koide-charge-quantum", "type": "explains", "weight": 0.7},
    {"from": "claim-theta4-master-key", "to": "claim-137-derived", "type": "explains", "weight": 1.0},
    {"from": "claim-theta4-master-key", "to": "pred-neutrino-sum-59", "type": "explains", "weight": 0.9},
    {"from": "deriv-golden-node", "to": "deriv-lambda-qcd-phi", "type": "derives", "weight": 0.7},
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
