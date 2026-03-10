"""
THE CASCADE ENGINE
==================
Set it free. Generate EVERYTHING from {3, 5, 7} and see what maps.
Every composition index n produces:
  - F(n), L(n) — the dual encoding
  - L(n)-F(n) = 2*F(n-1) — the residual
  - All F(n)/L(m), L(n)/L(m), F(n)/F(m) ratios — the coupling space
  - All L(a)*L(b)/F(15) products — the normalized spectrum
  - Phi-power address: log_phi(X) for each known constant

Then: mark everything that matches known physics.
Empty positions = predictions.
"""
import math
import json

phi = (1 + math.sqrt(5)) / 2
phibar = 1 / phi
sqrt5 = math.sqrt(5)

def F(n):
    if n <= 0: return 0
    return round((phi**n - (-phibar)**n) / sqrt5)

def L(n):
    return round(phi**n + (-phibar)**n)


# ============================================================
# THE KNOWN UNIVERSE — everything we can match against
# ============================================================
KNOWN = {
    # Biology
    "water MW": (18, "g/mol", "exact"),
    "pyrimidine pi_e": (4, "electrons", "exact"),
    "indole pi_e": (10, "electrons", "exact"),
    "benzene pi_e": (6, "electrons", "exact"),
    "anthracene pi_e": (14, "electrons", "exact"),
    "porphyrin pi_e": (18, "electrons", "exact"),
    "DNA pitch": (34, "Angstrom", "exact"),
    "DNA width": (21, "Angstrom", "exact"),
    "bp spacing": (3.4, "Angstrom", "derived"),
    "bp per turn": (10, "count", "exact"),
    "ATP atoms": (47, "count", "exact"),
    "PP-IX atoms": (76, "count", "exact"),
    "Chl a carbons": (55, "count", "exact"),
    "Heme B carbons": (34, "count", "exact"),
    "AcCoA atoms": (89, "count", "exact"),
    "H-bond stretch": (143, "cm-1", "approx"),

    # Coupling constants
    "alpha_s": (0.1184, "dimless", "measured"),
    "sin2_tW": (0.23122, "dimless", "measured"),
    "alpha_em": (1/137.036, "dimless", "measured"),
    "1/alpha_em": (137.036, "dimless", "measured"),
    "1/3 charge": (1/3, "dimless", "exact"),
    "2/3 charge": (2/3, "dimless", "exact"),
    "gamma_Immirzi": (0.2375, "dimless", "measured"),

    # CKM
    "V_ud": (0.97373, "dimless", "measured"),
    "V_us": (0.2253, "dimless", "measured"),
    "V_ub": (0.00361, "dimless", "measured"),
    "V_cd": (0.2251, "dimless", "measured"),
    "V_cs": (0.97350, "dimless", "measured"),
    "V_cb": (0.0412, "dimless", "measured"),
    "V_td": (0.00854, "dimless", "measured"),
    "V_ts": (0.0404, "dimless", "measured"),
    "V_tb": (0.99915, "dimless", "measured"),

    # PMNS
    "sin2_12": (0.307, "dimless", "measured"),
    "sin2_23": (0.546, "dimless", "measured"),
    "sin2_13": (0.0220, "dimless", "measured"),

    # Masses (in GeV)
    "v Higgs VEV": (246.22, "GeV", "measured"),
    "M_W": (80.379, "GeV", "measured"),
    "M_H": (125.25, "GeV", "measured"),
    "M_Z": (91.188, "GeV", "measured"),

    # Mass ratios
    "mu p/e": (1836.15, "ratio", "measured"),
    "m_mu/m_e": (206.77, "ratio", "measured"),
    "m_tau/m_mu": (16.82, "ratio", "measured"),
    "m_c/m_s": (13.6, "ratio", "measured"),
    "m_b/m_c": (3.29, "ratio", "measured"),
    "m_t/m_b": (41.33, "ratio", "measured"),
    "m_s/m_d": (20.0, "ratio", "measured"),
    "m_b/m_s": (44.75, "ratio", "measured"),

    # Cosmological
    "Koide ratio": (2/3, "dimless", "measured"),

    # Frequencies
    "613 THz": (613, "THz", "framework"),
    "40 Hz gamma": (40, "Hz", "framework"),

    # Modular form values
    "eta q=1/phi": (0.1184, "dimless", "computed"),
    "theta4 q=1/phi": (0.03031, "dimless", "computed"),
    "theta3 q=1/phi": (2.5551, "dimless", "computed"),
}


# ============================================================
# LAYER 1: THE COMPOSITION LATTICE
# ============================================================
print("=" * 80)
print("LAYER 1: THE COMPOSITION LATTICE")
print("=" * 80)

# Generate all composition indices reachable from {3, 5, 7}
primitives = [3, 5, 7]
reachable = set(primitives)
compositions = {}  # index -> list of decompositions

# Build compositions up to n=25
for target in range(3, 26):
    comps = []
    # Single mode
    if target in primitives:
        comps.append((target,))
    # Two modes
    for a in primitives + [6, 9]:  # include derived modes
        rem = target - a
        if rem >= 3 and rem in reachable:
            comp = tuple(sorted([a, rem]))
            if comp not in comps:
                comps.append(comp)
    # Three modes
    for a in primitives:
        for b in primitives:
            rem = target - a - b
            if rem >= 3 and rem in reachable:
                comp = tuple(sorted([a, b, rem]))
                if comp not in comps:
                    comps.append(comp)

    if comps or target in range(3, 26):
        reachable.add(target)
        compositions[target] = comps

print(f"\n  Reachable indices from {{3,5,7}}: {sorted(reachable)}")
print(f"\n  {'n':>3} {'F(n)':>8} {'L(n)':>8} {'L-F':>6} {'parity':>7} compositions -> KNOWN MATCHES")
print("-" * 95)

# For each index, find matches
node_data = []

for n in sorted(reachable):
    fn = F(n)
    ln = L(n)
    residual = ln - fn
    parity = "ODD" if n % 2 == 1 else "EVEN"
    comps = compositions.get(n, [])
    comp_str = ", ".join("+".join(str(x) for x in c) for c in comps[:3])

    # Find matches in KNOWN
    matches_f = []
    matches_l = []
    matches_r = []
    for name, (val, unit, qual) in KNOWN.items():
        if isinstance(val, (int, float)):
            if fn > 0 and abs(fn - val) / max(abs(val), 1) < 0.02:
                matches_f.append(name)
            if ln > 0 and abs(ln - val) / max(abs(val), 1) < 0.02:
                matches_l.append(name)
            if residual > 0 and abs(residual - val) / max(abs(val), 1) < 0.02:
                matches_r.append(name)

    match_str = ""
    if matches_f:
        match_str += f"  F={','.join(matches_f)}"
    if matches_l:
        match_str += f"  L={','.join(matches_l)}"
    if matches_r:
        match_str += f"  R={','.join(matches_r)}"

    node_data.append({
        "n": n, "F": fn, "L": ln, "residual": residual,
        "parity": parity, "compositions": comps,
        "matches_F": matches_f, "matches_L": matches_l, "matches_R": matches_r
    })

    print(f"  {n:>3} {fn:>8} {ln:>8} {residual:>6} {parity:>7} {comp_str:>30}{match_str}")


# ============================================================
# LAYER 2: THE RATIO SPACE (couplings)
# ============================================================
print("\n\n" + "=" * 80)
print("LAYER 2: THE RATIO SPACE — ALL F/L COUPLINGS")
print("=" * 80)

print("\nAll X(n)/Y(m) ratios that match known constants (within 0.5%):\n")

ratio_matches = []
bio_indices = sorted(reachable)

for n in bio_indices:
    for m in bio_indices:
        if m == n:
            continue
        for (t1, t2, label) in [('F','L','F/L'), ('L','F','L/F'), ('L','L','L/L'), ('F','F','F/F')]:
            num = F(n) if t1 == 'F' else L(n)
            den = F(m) if t2 == 'F' else L(m)
            if den == 0:
                continue
            ratio = num / den

            for name, (val, unit, qual) in KNOWN.items():
                if isinstance(val, (int, float)) and val > 0 and val < 1e4:
                    err = abs(ratio - val) / val
                    if err < 0.005:
                        ratio_matches.append((err, name, f"{t1}({n})/{t2}({m})", num, den, ratio))

# Also check 1 - X/Y
for n in bio_indices:
    for m in bio_indices:
        for (t1, t2) in [('F','L'), ('L','F'), ('F','F'), ('L','L')]:
            num = F(n) if t1 == 'F' else L(n)
            den = F(m) if t2 == 'F' else L(m)
            if den == 0 or num >= den:
                continue
            ratio = 1 - num/den
            for name, (val, unit, qual) in KNOWN.items():
                if isinstance(val, (int, float)) and 0.9 < val < 1:
                    err = abs(ratio - val) / val
                    if err < 0.001:
                        ratio_matches.append((err, name, f"1-{t1}({n})/{t2}({m})", num, den, ratio))

# Sort by precision
ratio_matches.sort()

# Print unique (deduplicated by constant name, keeping best match)
seen = set()
for err, name, expr, num, den, ratio in ratio_matches:
    if name not in seen:
        seen.add(name)
        print(f"  {name:>20} = {ratio:.6f}  via {expr:>16} = {num}/{den}  ({err*100:.4f}%)")


# ============================================================
# LAYER 3: THE F(15) SPECTRUM
# ============================================================
print("\n\n" + "=" * 80)
print("LAYER 3: THE F(15) = 610 SPECTRUM")
print("=" * 80)

print("\nAll L(a)*L(b)/F(15) values mapped against known constants:\n")

f15_spectrum = []
for a in range(1, 13):
    for b in range(a, 13):
        val = L(a) * L(b) / F(15)
        matched = None
        best_err = 0.015
        for name, (cval, unit, qual) in KNOWN.items():
            if isinstance(cval, (int, float)) and 0 < cval < 1:
                err = abs(val - cval) / cval
                if err < best_err:
                    best_err = err
                    matched = (name, err)
        f15_spectrum.append((a, b, val, matched))

print(f"  {'(a,b)':>8} {'L(a)*L(b)':>10} {'value':>10} {'match':>25}")
print("-" * 60)
for a, b, val, matched in f15_spectrum:
    if val < 1.0 and val > 0.001:
        m_str = f"{matched[0]} ({matched[1]*100:.3f}%)" if matched else "--- UNMAPPED ---"
        marker = "***" if matched else "   "
        print(f"  ({a},{b}):  {L(a):>3}*{L(b):>3} = {L(a)*L(b):>5}  {val:>10.6f}  {marker} {m_str}")


# ============================================================
# LAYER 4: PREDICTIONS — empty positions
# ============================================================
print("\n\n" + "=" * 80)
print("LAYER 4: PREDICTIONS — UNMAPPED POSITIONS")
print("=" * 80)

print("""
These F/L values at reachable indices have NO known match.
They are PREDICTIONS — quantities that SHOULD exist if the language is real.
""")

# Unmapped F values
print("--- Unmapped F(n) values ---\n")
for n in sorted(reachable):
    fn = F(n)
    if fn < 10000:
        matched = False
        for name, (val, unit, qual) in KNOWN.items():
            if isinstance(val, (int, float)) and abs(fn - val)/max(abs(val),1) < 0.03:
                matched = True
                break
        if not matched:
            comps = compositions.get(n, [])
            comp_str = "+".join(str(x) for x in comps[0]) if comps else "?"
            print(f"  F({n}) = {fn:>6}  ({comp_str})  PREDICTION: should be a count/length/frequency")

# Unmapped L values
print("\n--- Unmapped L(n) values ---\n")
for n in sorted(reachable):
    ln = L(n)
    if ln < 10000:
        matched = False
        for name, (val, unit, qual) in KNOWN.items():
            if isinstance(val, (int, float)) and abs(ln - val)/max(abs(val),1) < 0.03:
                matched = True
                break
        if not matched:
            comps = compositions.get(n, [])
            comp_str = "+".join(str(x) for x in comps[0]) if comps else "?"
            print(f"  L({n}) = {ln:>6}  ({comp_str})  PREDICTION: should be a structural count")

# Unmapped couplings in F(15) spectrum
print("\n--- Unmapped couplings in L(a)*L(b)/F(15) spectrum ---\n")
for a, b, val, matched in f15_spectrum:
    if val < 0.5 and val > 0.001 and not matched:
        print(f"  L({a})*L({b})/F(15) = {L(a)}*{L(b)}/610 = {val:.6f}  PREDICTION: should be a coupling constant")


# ============================================================
# THE GRAPH: connections between constants
# ============================================================
print("\n\n" + "=" * 80)
print("THE CONNECTION GRAPH")
print("=" * 80)

print("""
Constants are CONNECTED when they share mode indices in their F/L address.
This creates a graph where the edges are the biological modes.
""")

# Build adjacency from shared indices
addresses = {
    "alpha_s": {"indices": [1,6,9], "expr": "(F(1)+F(6))/L(9)"},
    "sin2_tW": {"indices": [2,8,15], "expr": "L(2)*L(8)/F(15)"},
    "1/3": {"indices": [4,7,15], "expr": "L(4)*L(7)/F(15)"},
    "alpha_em": {"indices": [5,8,17], "expr": "(F(5)+F(8))/L(17)"},
    "V_ud": {"indices": [3,9], "expr": "1-F(3)/L(9)"},
    "V_us": {"indices": [6,11,14], "expr": "F(11)/(L(6)+F(14))"},
    "V_ub": {"indices": [6,16], "expr": "F(6)/L(16)"},
    "V_ts": {"indices": [7,12], "expr": "F(7)/L(12)"},
    "V_td": {"indices": [3,13], "expr": "F(3)/F(13)"},
    "V_tb": {"indices": [6,19], "expr": "1-F(6)/L(19)"},
    "sin2_12": {"indices": [3,9], "expr": "1/3-F(3)/L(9)"},
    "sin2_23": {"indices": [3,11], "expr": "1/2+L(3)/F(11)"},
    "sin2_13": {"indices": [4,12], "expr": "L(4)/L(12)"},
    "v": {"indices": [3,16], "expr": "F(16)/L(3)"},
    "M_W": {"indices": [3,12], "expr": "L(12)/L(3)"},
    "M_H": {"indices": [2,14], "expr": "F(14)/L(2)"},
    "gamma_I": {"indices": [5,7,15], "expr": "F(5)*L(7)/F(15)"},
    "F(15)/613THz": {"indices": [15], "expr": "F(15)=610"},
    "water": {"indices": [6], "expr": "L(6)=18"},
    "DNA_pitch": {"indices": [9], "expr": "F(9)=34"},
    "ATP": {"indices": [8], "expr": "L(8)=47"},
}

# Count shared edges
print(f"\n  Most connected mode indices:\n")
index_count = {}
for name, data in addresses.items():
    for idx in data["indices"]:
        if idx not in index_count:
            index_count[idx] = []
        index_count[idx].append(name)

for idx in sorted(index_count.keys()):
    names = index_count[idx]
    if len(names) >= 2:
        modes = {3:"pyr", 5:"ind", 6:"wat", 7:"ant", 8:"pyr+ind", 9:"por",
                 12:"wat+wat", 14:"ant+ant", 15:"pyr+ind+ant", 16:"por+ant"}.get(idx, "")
        print(f"  n={idx:>2} ({modes:>12}): connects {len(names)} constants: {', '.join(names)}")


# ============================================================
# EXPORT: Full data as JSON for visualization
# ============================================================
graph_data = {
    "primitives": [3, 5, 7],
    "derived_modes": [6, 8, 9, 10, 11, 12, 14, 15],
    "nodes": [],
    "addresses": addresses,
    "predictions": [],
}

for nd in node_data:
    graph_data["nodes"].append({
        "n": nd["n"],
        "F": nd["F"],
        "L": nd["L"],
        "residual": nd["residual"],
        "parity": nd["parity"],
        "matches_F": nd["matches_F"],
        "matches_L": nd["matches_L"],
    })

# Save
with open("theory-tools/cascade-graph.json", "w") as f:
    json.dump(graph_data, f, indent=2)
print(f"\n\n  Graph data saved to theory-tools/cascade-graph.json")


# ============================================================
# FINAL: THE COMPLETE MAP — one screen
# ============================================================
print("\n\n" + "=" * 80)
print("THE COMPLETE MAP — EVERYTHING ON ONE SCREEN")
print("=" * 80)

print("""
                    THE UNIFIED LANGUAGE
                    ====================

    ALPHABET: {3, 5, 7} = pyrimidine, indole, anthracene
    DERIVED:  6=3+3 (water), 9=3+6 (porphyrin), 8=3+5, 15=3+5+7

    DUAL ENCODING: phi^n = (L(n) + F(n)*sqrt(5)) / 2
      L(n) = structure (Galois-even, structural counts)
      F(n) = dynamics (Galois-odd, geometric lengths/frequencies)

    THREE LAYERS:
    =============

    LAYER 1 — COUNTING (exact)
    F(8)=21 DNA width    L(6)=18 water     F(9)=34 DNA pitch
    F(10)=55 Chl carbons L(8)=47 ATP       L(9)=76 PP-IX
    F(11)=89 AcCoA       L(12)=322 E8      F(15)=610 ~613 THz

    LAYER 2 — COUPLINGS (as shares of F(15)=610)
    alpha_s  = L(3)*L(6)/F(15) = 72/610   (pyr*wat / total)
    sin2_tW  = L(2)*L(8)/F(15) = 141/610  (tri*ATP / total)
    1/3      = L(4)*L(7)/F(15) = 203/610  (Cox*ant / total)
    gamma_I  = F(5)*L(7)/F(15) = 145/610  (ind*ant / total)

    LAYER 3 — MIXING MATRICES (as deviations from simple fractions)
    CKM:                              PMNS:
    V_ud = 1-2/76     99.995%        sin2_12 = 1/3-2/76   99.994%
    V_us = 89/395      99.993%        sin2_23 = 1/2+4/89   99.81%
    V_ub = 8/2207      99.59%         sin2_13 = 7/322       98.8%
    V_td = 2/233       99.49%
    V_ts = 13/322      99.93%
    V_tb = 1-8/9349    99.9997%

    LAYER 4 — MASSES AND SCALES
    v = F(16)/L(3) = 987/4 GeV        mu = 6^5/phi^3
    M_W = L(12)/L(3) = 322/4 GeV      m_e = (1/2)(1+sin2_13) MeV
    M_H = F(14)/L(2) = 377/3 GeV      80 = 120*2/3 (Lambda exp)

    DEEP STRUCTURE:
    ===============
    - F(15) = total modes (3+5+7) is the UNIVERSAL NORMALIZER
    - sin2_tW/alpha_s = L(8)/(L(3)*6) = ATP/(pyr*water)
    - The selection rule: a+b = 9,10,11 with |a-b| = mode index
    - L(7)=29 is the universal lepton scale factor
    - V_us * 80 = 18 = water (Cabibbo * Lambda_exp = water)
    - Modular forms at q=1/phi give Layer 3+ precision
    - Everything is Z[phi] evaluated at the Golden Node
""")
