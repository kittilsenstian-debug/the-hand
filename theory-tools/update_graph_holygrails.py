#!/usr/bin/env python3
"""Add holy grails v3 discoveries to graph."""
import json
from pathlib import Path

GRAPH = Path(__file__).parent / "theory-graph.json"
with open(GRAPH, "r", encoding="utf-8") as f:
    g = json.load(f)

existing_ids = {n["id"] for n in g["nodes"]}

new_nodes = [
    {
        "id": "deriv-neutrino-spectrum-complete",
        "type": "derivation",
        "layer": "match",
        "domain": "physics",
        "label": "Complete neutrino spectrum: m1=0.54, m2=8.69, m3=50.7 meV",
        "summary": "All 3 neutrino masses derived. m2 = m_e*alpha^4*6 = 8.69 meV (known). m3 = m2*sqrt(34) = 50.7 meV where 34 = 1+3*L(5) from mass-squared ratio = 33 = 3*L(5). m1 from dm21^2. Sum = 59.9 meV. Normal ordering predicted.",
        "formula": "m2 = m_e*alpha^4*6, m3 = m2*sqrt(34), sum = 59.9 meV",
        "accuracy": "99.18% (dm32^2)",
        "confidence": 4,
        "status": "predicted",
        "sources": ["holy_grails_v3.py"],
        "depends_on": ["deriv-me-absolute"],
        "supports": [],
        "contradicts": [],
        "discovered": "2026-02-09",
        "tags": ["neutrino", "mass", "spectrum", "normal-ordering", "testable", "JUNO"]
    },
    {
        "id": "pred-proton-decay",
        "type": "prediction",
        "layer": "match",
        "domain": "physics",
        "label": "Proton decay: tau_p ~ 1e39 years, M_X = M_Pl*t4^2",
        "summary": "GUT scale M_X = M_Pl*t4^2 = 1.12e16 GeV. Proton lifetime tau_p ~ 1e39 years with lattice matrix element. Above Super-K limit (2.4e34 yr). Testable at Hyper-K (sensitivity 1e35 yr, ~2027).",
        "formula": "tau_p = M_X^4 / (alpha_GUT^2 * m_p * |<pi|qqq|p>|^2)",
        "accuracy": "prediction",
        "confidence": 3,
        "status": "predicted",
        "sources": ["holy_grails_v3.py"],
        "depends_on": ["claim-theta4-master-key"],
        "supports": [],
        "contradicts": [],
        "discovered": "2026-02-09",
        "tags": ["proton-decay", "GUT", "testable", "Hyper-K"]
    },
    {
        "id": "pred-pmns-cp-phase",
        "type": "prediction",
        "layer": "match",
        "domain": "physics",
        "label": "PMNS delta_CP = 4*pi/3 = 240 deg (96%) or 270 maximal",
        "summary": "PMNS CP phase prediction: 4*pi/3 = 240 degrees gives 95.65% match to measured 230 deg. Maximal CP (270 = 3*pi/2) is within 2-sigma bounds. Best framework candidate: pi + atan(phi^2) = 249 deg. Testable at DUNE/Hyper-K.",
        "formula": "delta_CP = 4*pi/3 or 3*pi/2",
        "accuracy": "95-96%",
        "confidence": 3,
        "status": "predicted",
        "sources": ["holy_grails_v3.py"],
        "depends_on": [],
        "supports": [],
        "contradicts": [],
        "discovered": "2026-02-09",
        "tags": ["PMNS", "CP-violation", "testable", "DUNE"]
    },
    {
        "id": "pred-dark-matter-mass",
        "type": "prediction",
        "layer": "interpretation",
        "domain": "cosmology",
        "label": "Dark matter: mega-nuclei A~5, m~1.2 GeV, sigma/m=0.036",
        "summary": "Dark matter = dark mega-nuclei. Dark fermion mass ~ Lambda_QCD = 221 MeV (no EM hierarchy because alpha_dark=0). A ~ Omega_DM/Omega_b ~ 5 dark nucleons. m_DM ~ 1.2 GeV. sigma/m = 0.036 cm^2/g passes Bullet Cluster (< 1). NO direct detection signal because alpha_dark = 0.",
        "formula": "m_DM ~ A * Lambda_QCD, A ~ Omega_DM/Omega_b",
        "accuracy": "prediction",
        "confidence": 3,
        "status": "predicted",
        "sources": ["holy_grails_v3.py"],
        "depends_on": ["deriv-omega-dm-t4-corrected"],
        "supports": [],
        "contradicts": [],
        "discovered": "2026-02-09",
        "tags": ["dark-matter", "mass", "mega-nuclei", "Bullet-Cluster"]
    },
    {
        "id": "pred-gw-lisa-band",
        "type": "prediction",
        "layer": "match",
        "domain": "cosmology",
        "label": "GW from domain wall: f~1.4 mHz, h2*Omega~2e-10, LISA detectable",
        "summary": "Domain wall makes EW phase transition first-order. GW peak frequency 1.4 mHz (LISA band 0.1-100 mHz). Amplitude h^2*Omega ~ 2e-10 (LISA sensitivity ~1e-12). DETECTABLE by LISA (~2035).",
        "formula": "f_peak ~ 1.4 mHz, h^2*Omega ~ 2e-10",
        "accuracy": "prediction",
        "confidence": 3,
        "status": "predicted",
        "sources": ["holy_grails_v3.py"],
        "depends_on": [],
        "supports": [],
        "contradicts": [],
        "discovered": "2026-02-09",
        "tags": ["gravitational-waves", "LISA", "domain-wall", "testable", "phase-transition"]
    },
]

new_edges = [
    {"from": "deriv-me-absolute", "to": "deriv-neutrino-spectrum-complete", "type": "derives", "weight": 0.8},
    {"from": "claim-theta4-master-key", "to": "pred-proton-decay", "type": "derives", "weight": 0.7},
    {"from": "deriv-omega-dm-t4-corrected", "to": "pred-dark-matter-mass", "type": "derives", "weight": 0.8},
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
