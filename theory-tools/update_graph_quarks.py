#!/usr/bin/env python3
"""Add quark mass derivations to graph."""
import json
from pathlib import Path

GRAPH = Path(__file__).parent / "theory-graph.json"
with open(GRAPH, "r", encoding="utf-8") as f:
    g = json.load(f)

existing_ids = {n["id"] for n in g["nodes"]}

new_nodes = [
    {
        "id": "deriv-mu-up-phi3",
        "type": "derivation",
        "layer": "match",
        "domain": "physics",
        "label": "m_u = m_e * phi^3 at 99.57%",
        "summary": "Up quark mass from electron and golden ratio: m_u = m_e * phi^3 = 2.169 MeV vs 2.16 MeV. The lightest quark is the electron mass times the cube of the golden ratio. Wall position x_u ~ 29/phi^2 (Coxeter exponent 29).",
        "formula": "m_u = m_e * phi^3",
        "accuracy": "99.57%",
        "confidence": 4,
        "status": "verified",
        "sources": ["quark_mass_scale.py"],
        "depends_on": ["deriv-me-absolute"],
        "supports": [],
        "contradicts": [],
        "discovered": "2026-02-09",
        "tags": ["quark", "up", "phi", "mass", "Kaplan"]
    },
    {
        "id": "deriv-md-mu200",
        "type": "derivation",
        "layer": "match",
        "domain": "physics",
        "label": "m_d = m_e * mu / 200 at 99.35%",
        "summary": "Down quark mass: m_d = m_e * mu / 200 = m_s / 20 = 4.70 MeV vs 4.67 MeV. Wall position x_d = 17/phi (Coxeter exponent 17). The 200 = 2 * 10 * 10 = 2 * (h/3)^2.",
        "formula": "m_d = m_e * mu / 200",
        "accuracy": "99.35%",
        "confidence": 3,
        "status": "verified",
        "sources": ["quark_mass_scale.py"],
        "depends_on": ["deriv-me-absolute"],
        "supports": [],
        "contradicts": [],
        "discovered": "2026-02-09",
        "tags": ["quark", "down", "mu", "mass", "Kaplan"]
    },
    {
        "id": "deriv-mc-mt-alpha",
        "type": "derivation",
        "layer": "match",
        "domain": "physics",
        "label": "m_c = m_t * alpha at 99.25%",
        "summary": "Charm mass from top and alpha: m_c = m_t * alpha = 1.261 GeV vs 1.27 GeV. Wall position x_c = 13/phi^2 (Coxeter exponent 13). The charm-top ratio IS the fine structure constant.",
        "formula": "m_c = m_t * alpha",
        "accuracy": "99.25%",
        "confidence": 4,
        "status": "verified",
        "sources": ["quark_mass_scale.py"],
        "depends_on": ["deriv-me-absolute"],
        "supports": [],
        "contradicts": [],
        "discovered": "2026-02-09",
        "tags": ["quark", "charm", "alpha", "mass", "top"]
    },
    {
        "id": "deriv-mb-mc-2phi",
        "type": "derivation",
        "layer": "match",
        "domain": "physics",
        "label": "m_b = m_c * 2*phi at 97.58%",
        "summary": "Bottom mass from charm and phi: m_b = m_c * 2*phi = 4.079 GeV vs 4.18 GeV. Wall position x_b = 6/phi (6 = |S3|). The bottom-charm ratio is twice the golden ratio.",
        "formula": "m_b = m_c * 2*phi",
        "accuracy": "97.58%",
        "confidence": 3,
        "status": "verified",
        "sources": ["quark_mass_scale.py"],
        "depends_on": ["deriv-mc-mt-alpha"],
        "supports": [],
        "contradicts": [],
        "discovered": "2026-02-09",
        "tags": ["quark", "bottom", "phi", "mass", "S3"]
    },
    {
        "id": "claim-mu-generation-tower",
        "type": "claim",
        "layer": "algebra",
        "domain": "physics",
        "label": "mu-generation tower: m_f = m_e * mu^n / (h/3)",
        "summary": "Fermion masses follow a tower structure in powers of mu with denominator h/3 = 10: n=0 gives electron, n=1 gives strange quark (m_s = m_e*mu/10), n=2 gives top quark (m_t = m_e*mu^2/10). The denominator 10 = h/3 = Coxeter number / triality. The tower selects exactly the 'diagonal' fermions (t, s, e) that sit on distinct S3 representations.",
        "formula": "m_f = m_e * mu^n / (h/3), n=0,1,2",
        "accuracy": "structural",
        "confidence": 4,
        "status": "claimed",
        "sources": ["quark_mass_scale.py", "absolute_mass_scale.py"],
        "depends_on": ["deriv-me-absolute"],
        "supports": [],
        "contradicts": [],
        "discovered": "2026-02-09",
        "tags": ["generation", "tower", "mu", "Coxeter", "triality"]
    },
    {
        "id": "claim-quark-coxeter-positions",
        "type": "claim",
        "layer": "algebra",
        "domain": "physics",
        "label": "Quark wall positions = Coxeter / phi^k",
        "summary": "All quark positions on the domain wall follow x_q = C/phi^k where C is an E8 Coxeter exponent: x_b = 6/phi (99.55%), x_c = 13/phi^2 (99.00%), x_d = 17/phi (99.85%), x_u = 29/phi^2 (98.09%). Compare leptons: x_e = 13 (99.04%), x_mu = 7 (99.82%). The Coxeter exponents literally label fermion positions on the wall.",
        "formula": "x_q = Coxeter_exponent / phi^k",
        "accuracy": "98-99.9%",
        "confidence": 4,
        "status": "claimed",
        "sources": ["quark_mass_scale.py"],
        "depends_on": ["claim-80-dual-role", "deriv-ye-wall-position"],
        "supports": [],
        "contradicts": [],
        "discovered": "2026-02-09",
        "tags": ["Coxeter", "wall-position", "quarks", "E8", "pattern"]
    },
]

new_edges = [
    {"from": "deriv-me-absolute", "to": "deriv-mu-up-phi3", "type": "derives", "weight": 0.9},
    {"from": "deriv-me-absolute", "to": "deriv-md-mu200", "type": "derives", "weight": 0.9},
    {"from": "deriv-me-absolute", "to": "deriv-mc-mt-alpha", "type": "derives", "weight": 0.9},
    {"from": "deriv-mc-mt-alpha", "to": "deriv-mb-mc-2phi", "type": "derives", "weight": 0.8},
    {"from": "deriv-me-absolute", "to": "claim-mu-generation-tower", "type": "supports", "weight": 1.0},
    {"from": "claim-quark-coxeter-positions", "to": "deriv-mu-up-phi3", "type": "explains", "weight": 0.8},
    {"from": "claim-quark-coxeter-positions", "to": "deriv-md-mu200", "type": "explains", "weight": 0.8},
    {"from": "claim-80-dual-role", "to": "claim-quark-coxeter-positions", "type": "supports", "weight": 0.7},
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
