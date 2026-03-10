#!/usr/bin/env python3
"""Add CKM breakthrough, breathing mode, R=-3/2, self-consistency findings to graph."""
import json
from pathlib import Path

GRAPH = Path(__file__).parent / "theory-graph.json"
with open(GRAPH, "r", encoding="utf-8") as f:
    g = json.load(f)

existing_ids = {n["id"] for n in g["nodes"]}

new_nodes = [
    {
        "id": "deriv-vcb-t4",
        "type": "derivation",
        "layer": "match",
        "domain": "physics",
        "label": "V_cb = (phi/7)*sqrt(t4) at 99.35%",
        "summary": "CKM element V_cb from Golden Node: V_cb = (phi/7)*sqrt(theta_4) = 0.0402 vs measured 0.0405. Same base phi/7 as V_us, with t4 suppressing generation mixing. The CKM hierarchy is: (1-t4), sqrt(t4), 3*t4^(3/2).",
        "formula": "V_cb = (phi/7) * sqrt(theta_4)",
        "accuracy": "99.35%",
        "confidence": 4,
        "status": "verified",
        "sources": ["new_continent.py"],
        "depends_on": ["claim-theta4-master-key", "deriv-vus-t4-corrected"],
        "supports": [],
        "contradicts": [],
        "discovered": "2026-02-09",
        "tags": ["golden-node", "theta_4", "CKM", "V_cb"]
    },
    {
        "id": "deriv-vub-triality",
        "type": "derivation",
        "layer": "match",
        "domain": "physics",
        "label": "V_ub = (phi/7)*3*t4^(3/2) at 95.8% (triality factor)",
        "summary": "V_ub = (phi/7)*3*theta_4^(3/2) = 0.00366 vs measured 0.00382. The factor of 3 IS the triality quantum number from S3 generation symmetry. Complete CKM hierarchy: V_us ~ (1-t4), V_cb ~ sqrt(t4), V_ub ~ 3*t4^(3/2).",
        "formula": "V_ub = (phi/7) * 3 * theta_4^(3/2)",
        "accuracy": "95.76%",
        "confidence": 3,
        "status": "verified",
        "sources": ["new_continent.py"],
        "depends_on": ["claim-theta4-master-key", "deriv-vus-t4-corrected"],
        "supports": [],
        "contradicts": [],
        "discovered": "2026-02-09",
        "tags": ["golden-node", "theta_4", "CKM", "V_ub", "triality"]
    },
    {
        "id": "claim-ckm-phi7-hierarchy",
        "type": "claim",
        "layer": "interpretation",
        "domain": "physics",
        "label": "Complete CKM from phi/7 base + t4 hierarchy",
        "summary": "All CKM mixing angles derive from two inputs: phi/7 (A2 mixing base from E8) and theta_4 (Golden Node dark fingerprint). V_us=(phi/7)(1-t4), V_cb=(phi/7)sqrt(t4), V_ub=(phi/7)*3*t4^(3/2). Unitarity: V_ud=sqrt(1-V_us^2-V_ub^2)=0.9745 (99.92%). Jarlskog invariant gives delta_CP=74.5 deg.",
        "formula": "CKM = phi/7 * {(1-t4), sqrt(t4), 3*t4^(3/2)}",
        "accuracy": ">95%",
        "confidence": 4,
        "status": "derived",
        "sources": ["new_continent.py", "self_consistency_matrix.py"],
        "depends_on": ["claim-theta4-master-key", "deriv-golden-node"],
        "supports": [],
        "contradicts": [],
        "discovered": "2026-02-09",
        "tags": ["golden-node", "CKM", "hierarchy", "triality", "breakthrough"]
    },
    {
        "id": "deriv-breathing-mode-mass",
        "type": "derivation",
        "layer": "match",
        "domain": "physics",
        "label": "Breathing mode mass = 76.7 GeV (Poschl-Teller)",
        "summary": "Domain wall breathing mode from Poschl-Teller analysis: m_B = m_H*sqrt(3/8) = 76.7 GeV. Production cross-section ~20% of Higgs (coupling suppressed by 1/sqrt(5)). Near CMS 95.4 GeV excess (20% off, needs correction).",
        "formula": "m_B = m_H * sqrt(3/8) = 76.7 GeV",
        "accuracy": "prediction",
        "confidence": 3,
        "status": "predicted",
        "sources": ["new_continent.py"],
        "depends_on": ["deriv-domain-wall-bound-states", "deriv-potential"],
        "supports": [],
        "contradicts": [],
        "discovered": "2026-02-09",
        "tags": ["breathing-mode", "Poschl-Teller", "LHC", "prediction"]
    },
    {
        "id": "pred-varying-R-minus-3-2",
        "type": "prediction",
        "layer": "match",
        "domain": "cosmology",
        "label": "Varying constants R = d(ln alpha)/d(ln mu) = -3/2",
        "summary": "From coupling function f(Phi): R = -3/2 (tree: -2/3, with QCD correction 9/4). No other theory predicts exactly -3/2. SM: R=0, Bekenstein: R=+/-1. Testable by ELT/ANDES ~2035 (need delta_alpha ~ 10^-8). Webb et al. (2011): R = -1.6 +/- 1.2 (consistent).",
        "formula": "R = d(ln alpha)/d(ln mu) = -3/2",
        "accuracy": "prediction",
        "confidence": 4,
        "status": "predicted",
        "sources": ["new_continent.py"],
        "depends_on": ["deriv-coupling-function", "deriv-lagrangian"],
        "supports": [],
        "contradicts": [],
        "discovered": "2026-02-09",
        "tags": ["varying-constants", "prediction", "testable", "unique"]
    },
    {
        "id": "claim-alpha-s-sin2tw-locked",
        "type": "claim",
        "layer": "algebra",
        "domain": "physics",
        "label": "alpha_s = sqrt(2*sin2tW*t4) at 99.98%",
        "summary": "Cross-constraint: eta = alpha_s AND eta^2/(2*t4) = sin2tW => alpha_s = sqrt(2*sin2tW*t4) = 0.11838 vs 0.1184. Three quantities (alpha_s, sin2tW, theta_4) locked by one algebraic relation. This is NOT a fit.",
        "formula": "alpha_s = sqrt(2 * sin2tW * theta_4)",
        "accuracy": "99.98%",
        "confidence": 5,
        "status": "derived",
        "sources": ["self_consistency_matrix.py"],
        "depends_on": ["deriv-golden-node"],
        "supports": [],
        "contradicts": [],
        "discovered": "2026-02-09",
        "tags": ["golden-node", "cross-constraint", "alpha_s", "sin2tW", "structural"]
    },
    {
        "id": "analysis-self-consistency",
        "type": "analysis",
        "layer": "algebra",
        "domain": "physics",
        "label": "Self-consistency matrix: 10 predictions, 10x overdetermination",
        "summary": "12 predictions tested, 10 above 97%, 6 above 99%. One free parameter (mu) predicts 10 quantities: alpha, sin2tW, alpha_s, Omega_DM, lambda_H, m_H/v, V_us, V_cb, Lambda_QCD, mu=t3^8. Overdetermination ratio 10x vs ~1x for numerology. Random number test: P < 0.002.",
        "formula": "10 predictions from 1 parameter",
        "accuracy": "statistical",
        "confidence": 5,
        "status": "verified",
        "sources": ["self_consistency_matrix.py"],
        "depends_on": ["deriv-core-identity", "deriv-golden-node"],
        "supports": [],
        "contradicts": [],
        "discovered": "2026-02-09",
        "tags": ["self-consistency", "anti-numerology", "overdetermination", "statistics"]
    },
]

new_edges = [
    {"from": "claim-theta4-master-key", "to": "deriv-vcb-t4", "type": "explains", "weight": 0.9},
    {"from": "claim-theta4-master-key", "to": "deriv-vub-triality", "type": "explains", "weight": 0.8},
    {"from": "deriv-vus-t4-corrected", "to": "claim-ckm-phi7-hierarchy", "type": "supports", "weight": 1.0},
    {"from": "deriv-vcb-t4", "to": "claim-ckm-phi7-hierarchy", "type": "supports", "weight": 1.0},
    {"from": "deriv-vub-triality", "to": "claim-ckm-phi7-hierarchy", "type": "supports", "weight": 1.0},
    {"from": "deriv-domain-wall-bound-states", "to": "deriv-breathing-mode-mass", "type": "derives", "weight": 0.8},
    {"from": "deriv-coupling-function", "to": "pred-varying-R-minus-3-2", "type": "derives", "weight": 0.9},
    {"from": "deriv-golden-node", "to": "claim-alpha-s-sin2tw-locked", "type": "derives", "weight": 1.0},
    {"from": "deriv-core-identity", "to": "analysis-self-consistency", "type": "supports", "weight": 1.0},
    {"from": "deriv-golden-node", "to": "analysis-self-consistency", "type": "supports", "weight": 1.0},
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

# Update stats
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
