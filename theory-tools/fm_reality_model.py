#!/usr/bin/env python3
"""
FM REALITY MODEL — Computational Modulation Matrix
====================================================
Systematically maps ALL operator combinations against ALL known
physical constants. Identifies gaps, missing oscillators, and
potential new derivations.

The idea: 6 operators generate all physics through pairwise
(and higher-order) modulation. If we compute EVERY combination
and compare to EVERY unmapped constant, we can find:
1. Which constants are already explained
2. Which constants COULD be explained by unexplored combinations
3. Whether any constants need operators NOT in our set (= missing oscillators)
"""

import sys
import math
from itertools import combinations_with_replacement, product

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

phi = (1 + math.sqrt(5)) / 2
phibar = 1 / phi

# ============================================================
# THE OPERATORS
# ============================================================

def theta2(q, N=500):
    s = 0
    for n in range(N):
        s += q**((n + 0.5)**2)
    return 2 * s

def theta3(q, N=500):
    s = 1
    for n in range(1, N):
        s += 2 * q**(n**2)
    return s

def theta4(q, N=500):
    s = 1
    for n in range(1, N):
        s += 2 * (-1)**n * q**(n**2)
    return s

def eta_func(q, N=500):
    s = 1
    for n in range(1, N):
        s *= (1 - q**n)
    return q**(1/24) * s

q = phibar
q2 = phibar**2

t2 = theta2(q)
t3 = theta3(q)
t4 = theta4(q)
et = eta_func(q)
et_dark = eta_func(q2)
t3_dark = theta3(q2)
t4_dark = theta4(q2)
C = et * t4 / 2

# The 6 primary operators + their values
OPERATORS = {
    "eta":    et,
    "theta3": t3,
    "theta4": t4,
    "phi":    phi,
    "3":      3.0,
    "40":     40.0,
}

# Extended set including dark sector and derived
OPERATORS_EXT = {
    **OPERATORS,
    "eta_d":  et_dark,
    "t3_d":   t3_dark,
    "t4_d":   t4_dark,
    "C":      C,
    "2":      2.0,
    "sqrt5":  math.sqrt(5),
    "7":      7.0,
    "80":     80.0,
}

# ============================================================
# ALL KNOWN PHYSICAL CONSTANTS (dimensionless or in natural units)
# ============================================================

# Status: MAPPED = has framework formula, UNMAPPED = no formula yet
CONSTANTS = {
    # === GAUGE COUPLINGS ===
    "alpha_s (strong)":          {"value": 0.1184,     "status": "MAPPED", "formula": "eta(q)"},
    "sin2_thetaW (weak)":       {"value": 0.23121,    "status": "MAPPED", "formula": "eta^2/(2*t4)"},
    "1/alpha_EM":                {"value": 137.036,    "status": "MAPPED", "formula": "t3*phi/t4 + VP"},

    # === FERMION MASSES (as ratios to electron) ===
    "m_u/m_e":                   {"value": 4.30,       "status": "PARTIAL", "formula": "phi^3 (99.8%)"},
    "m_d/m_e":                   {"value": 9.39,       "status": "UNMAPPED"},
    "m_s/m_e":                   {"value": 185.1,      "status": "UNMAPPED"},
    "m_c/m_e":                   {"value": 2490,       "status": "UNMAPPED"},
    "m_b/m_e":                   {"value": 8180,       "status": "UNMAPPED"},
    "m_t/m_e":                   {"value": 336500,     "status": "PARTIAL", "formula": "mu^2/10"},
    "m_mu/m_e":                  {"value": 206.77,     "status": "UNMAPPED"},
    "m_tau/m_e":                 {"value": 3477,       "status": "UNMAPPED"},

    # === MASS RATIOS (within generations) ===
    "m_c/m_t":                   {"value": 0.00740,    "status": "UNMAPPED"},
    "m_u/m_t":                   {"value": 1.28e-5,    "status": "UNMAPPED"},
    "m_s/m_b":                   {"value": 0.0227,     "status": "UNMAPPED"},
    "m_d/m_b":                   {"value": 0.00115,    "status": "UNMAPPED"},
    "m_mu/m_tau":                {"value": 0.0595,     "status": "UNMAPPED"},
    "m_e/m_tau":                 {"value": 2.88e-4,    "status": "UNMAPPED"},
    "m_b/m_c":                   {"value": 3.28,       "status": "PARTIAL", "formula": "phi^(5/2)"},

    # === CKM MATRIX ===
    "Vus (Cabibbo)":             {"value": 0.2243,     "status": "MAPPED", "formula": "C/et"},
    "Vcb":                       {"value": 0.0422,     "status": "MAPPED", "formula": "C"},
    "Vub":                       {"value": 0.00394,    "status": "MAPPED", "formula": "C^2/et"},
    "Jarlskog J":                {"value": 3.18e-5,    "status": "MAPPED", "formula": "C^3/(6*sqrt(3))"},
    "delta_CKM (CP phase)":     {"value": 1.144,      "status": "PARTIAL"},  # radians

    # === PMNS MATRIX ===
    "sin2_theta12 (solar)":     {"value": 0.307,      "status": "MAPPED", "formula": "1/3-t4*sqrt(3/4)"},
    "sin2_theta23 (atm)":       {"value": 0.572,      "status": "MAPPED", "formula": "1/2+40C"},
    "sin2_theta13 (reactor)":   {"value": 0.0220,     "status": "UNMAPPED"},
    "delta_PMNS (CP)":          {"value": 3.77,       "status": "UNMAPPED"},  # radians, ~216 deg

    # === MASS SCALES ===
    "mu (p/e mass ratio)":       {"value": 1836.15,    "status": "MAPPED", "formula": "6^5/phi^3+9/(7phi^2)"},
    "v/M_Pl (hierarchy)":       {"value": 1.01e-17,   "status": "MAPPED", "formula": "phibar^80"},
    "m_H/v (Higgs coupling)":   {"value": 0.509,      "status": "UNMAPPED"},  # 125.1/245.5
    "m_W/m_Z":                   {"value": 0.8815,     "status": "DERIVED"},  # = cos(thetaW)

    # === COSMOLOGY ===
    "Lambda (cosmo const)":     {"value": 2.89e-122,  "status": "MAPPED", "formula": "t4^80*sqrt5/phi^2"},
    "eta_B (baryon asym)":      {"value": 6.1e-10,    "status": "MAPPED", "formula": "t4^6/sqrt(phi)"},
    "Omega_DM/Omega_b":         {"value": 5.36,       "status": "MAPPED", "formula": "cubic x^3-3x+1"},
    "n_s (spectral index)":     {"value": 0.9649,     "status": "CLAIMED", "formula": "29/30"},
    "r (tensor/scalar)":        {"value": 0.0033,     "status": "CLAIMED"},

    # === NEUTRINO SECTOR ===
    "Delta_m21^2/Delta_m31^2":  {"value": 0.0297,     "status": "UNMAPPED"},  # ratio of mass splittings
    "sum_m_nu (eV)":            {"value": 0.06,       "status": "UNMAPPED"},  # minimum from oscillations

    # === LOOP GRAVITY ===
    "gamma_Immirzi":             {"value": 0.2375,     "status": "MAPPED", "formula": "1/(3*phi^2)"},

    # === FUNDAMENTAL RATIOS ===
    "alpha/alpha_s":             {"value": 0.0617,     "status": "DERIVED"},
    "sin2tW * alpha_s":         {"value": 0.02737,    "status": "UNMAPPED"},
    "m_t/m_W":                   {"value": 2.14,       "status": "UNMAPPED"},
    "m_H/m_W":                   {"value": 1.556,      "status": "UNMAPPED"},
    "m_H/m_t":                   {"value": 0.727,      "status": "UNMAPPED"},
}

# ============================================================
# SYSTEMATIC COMBINATION GENERATOR
# ============================================================

print("=" * 80)
print("  FM REALITY MODEL: Systematic Operator Combination Scan")
print("=" * 80)
print()

# Generate ALL 2-operator combinations: a*b, a/b, a^b, a+b, a-b
# Also: a^2, a^3, a^(1/2), etc.

def safe_pow(base, exp):
    """Safe power that handles edge cases."""
    try:
        if base <= 0 and exp != int(exp):
            return None
        result = base ** exp
        if math.isnan(result) or math.isinf(result):
            return None
        return result
    except (OverflowError, ValueError, ZeroDivisionError):
        return None

# Build combination table
combos = {}

ops = list(OPERATORS.items())

# 1. Single operator functions
for name, val in ops:
    combos[name] = val
    combos[f"{name}^2"] = val**2
    combos[f"{name}^3"] = val**3
    if val > 0:
        combos[f"sqrt({name})"] = math.sqrt(val)
        combos[f"1/{name}"] = 1/val
    combos[f"{name}^(1/3)"] = val**(1/3) if val > 0 else None
    combos[f"{name}^4"] = val**4
    combos[f"{name}^6"] = val**6

# 2. All 2-operator products and ratios
for i, (n1, v1) in enumerate(ops):
    for j, (n2, v2) in enumerate(ops):
        if i <= j:
            combos[f"{n1}*{n2}"] = v1 * v2
        if i != j:
            if v2 != 0:
                combos[f"{n1}/{n2}"] = v1 / v2
            combos[f"{n1}+{n2}"] = v1 + v2
            if i < j:
                combos[f"{n1}-{n2}"] = v1 - v2
                combos[f"{n2}-{n1}"] = v2 - v1
            p = safe_pow(v1, v2)
            if p is not None and abs(p) < 1e200:
                combos[f"{n1}^{n2}"] = p

# 3. Key 3-operator combos (the known ones + systematic)
for i, (n1, v1) in enumerate(ops):
    for j, (n2, v2) in enumerate(ops):
        for k, (n3, v3) in enumerate(ops):
            if i < j < k:
                combos[f"{n1}*{n2}*{n3}"] = v1 * v2 * v3
                combos[f"{n1}*{n2}/{n3}"] = v1 * v2 / v3 if v3 != 0 else None
                combos[f"{n1}/{n2}*{n3}"] = v1 / v2 * v3 if v2 != 0 else None
                combos[f"{n1}/{n2}/{n3}"] = v1 / v2 / v3 if v2 != 0 and v3 != 0 else None

# 4. Power combos that appear in framework
combos["t4^80"] = t4**80
combos["phibar^80"] = phibar**80
combos["t4^6/sqrt(phi)"] = t4**6 / math.sqrt(phi)
combos["eta^2/(2*t4)"] = et**2 / (2*t4)
combos["t3*phi/t4"] = t3 * phi / t4
combos["1/3-t4*sqrt(3/4)"] = 1/3 - t4 * math.sqrt(3/4)
combos["1/2+40*C"] = 0.5 + 40 * C
combos["C/eta"] = C / et
combos["C^2/eta"] = C**2 / et
combos["phi^3"] = phi**3
combos["phi^(5/2)"] = phi**2.5
combos["1/(3*phi^2)"] = 1 / (3 * phi**2)
combos["6^5/phi^3"] = 6**5 / phi**3
combos["eta*t4/2"] = et * t4 / 2
combos["t4^80*sqrt5/phi^2"] = t4**80 * math.sqrt(5) / phi**2
combos["t4/t3 (eps_h)"] = t4 / t3

# 5. Bessel-inspired combos (from FM picture)
eps_h = t4 / t3
combos["eps_h"] = eps_h
combos["eps_h^2"] = eps_h**2
combos["eps_h^3"] = eps_h**3
combos["eps_h^(1/2)"] = math.sqrt(eps_h)
combos["eps_h^(3/2)"] = eps_h**1.5
combos["eps_h*phi"] = eps_h * phi
combos["eps_h/phi"] = eps_h / phi
combos["eps_h*et"] = eps_h * et
combos["eps_h*3"] = eps_h * 3

# 6. Dark sector combos
combos["eta_d"] = et_dark
combos["eta_d/eta"] = et_dark / et
combos["eta_d*t4"] = et_dark * t4
combos["eta^2/eta_d"] = et**2 / et_dark  # = t4 by creation identity
combos["eta_d^2"] = et_dark**2
combos["t4_d"] = t4_dark
combos["t3_d"] = t3_dark

# Clean None values
combos = {k: v for k, v in combos.items() if v is not None}

print(f"Generated {len(combos)} operator combinations")
print()

# ============================================================
# MATCH FINDER: Compare every combo to every unmapped constant
# ============================================================

print("=" * 80)
print("  SCANNING FOR MATCHES: Unmapped Constants vs All Combinations")
print("=" * 80)
print()

THRESHOLD = 0.02  # 2% match threshold

unmapped = {k: v for k, v in CONSTANTS.items() if v["status"] == "UNMAPPED"}
partial = {k: v for k, v in CONSTANTS.items() if v["status"] == "PARTIAL"}

print(f"Unmapped constants: {len(unmapped)}")
print(f"Partially mapped:   {len(partial)}")
print(f"Fully mapped:       {sum(1 for v in CONSTANTS.values() if v['status'] == 'MAPPED')}")
print()

# For each unmapped constant, find best matching combinations
print("-" * 80)
print(f"{'Constant':>30s}  {'Value':>12s}  {'Best Match':>30s}  {'Combo Value':>12s}  {'Error':>8s}")
print("-" * 80)

hits = {}
for const_name, const_info in sorted(CONSTANTS.items(), key=lambda x: x[1]["status"]):
    if const_info["status"] in ("MAPPED", "DERIVED"):
        continue

    target = const_info["value"]
    if target == 0:
        continue

    best_match = None
    best_err = float('inf')
    best_val = None

    for combo_name, combo_val in combos.items():
        if combo_val == 0:
            continue

        # Check both combo_val and its negative
        for cv in [combo_val, -combo_val]:
            if target != 0:
                err = abs(cv - target) / abs(target)
            else:
                err = abs(cv)

            if err < best_err:
                best_err = err
                best_match = combo_name
                best_val = cv

    status_mark = "*" if const_info["status"] == "PARTIAL" else " "

    if best_err < THRESHOLD:
        marker = "<-- HIT!"
    elif best_err < 0.05:
        marker = "<-- close"
    else:
        marker = ""

    if abs(target) < 0.001:
        t_str = f"{target:.2e}"
        v_str = f"{best_val:.2e}" if best_val else "---"
    else:
        t_str = f"{target:.6f}"
        v_str = f"{best_val:.6f}" if best_val else "---"

    print(f"{status_mark} {const_name:>28s}  {t_str:>12s}  {best_match:>30s}  {v_str:>12s}  {best_err*100:>6.1f}%  {marker}")

    if best_err < THRESHOLD:
        hits[const_name] = {"combo": best_match, "error": best_err, "value": best_val}

print()
print(f"HITS (< {THRESHOLD*100}% error): {len(hits)}")
for name, info in hits.items():
    print(f"  {name}: {info['combo']} = {info['value']:.6f} (err {info['error']*100:.2f}%)")

# ============================================================
# GAP MAP: Which operator pairs have NO assigned constant?
# ============================================================
print()
print("=" * 80)
print("  GAP MAP: Operator Pairs Without Assigned Physics")
print("=" * 80)
print()

# The matrix from last session - which pairs ARE assigned
assigned_pairs = {
    ("eta", "eta"):       "sin2_tW",
    ("eta", "theta4"):    "C (correction)",
    ("eta", "3"):         "CORE IDENTITY",
    ("eta", "40"):        "sin2_theta23",
    ("theta3", "theta3"): "Y1+Y2",
    ("theta3", "theta4"): "epsilon_h (hierarchy)",
    ("theta3", "phi"):    "1/alpha_tree",
    ("theta4", "theta4"): "Y1-Y2 (near 0)",
    ("theta4", "phi"):    "sin2_theta12",
    ("theta4", "40"):     "Lambda (via t4^80)",
    ("phi", "phi"):       "v/M_Pl (via phi^80)",
    ("phi", "3"):         "mu (via 6^5/phi^3)",
    ("phi", "40"):        "hierarchy (phi^80)",
    ("3", "3"):           "DM ratio (cubic)",
    ("3", "40"):          "80 = 240/3",
    ("40", "40"):         "G (phibar^160)",
}

op_names = list(OPERATORS.keys())
print("FILLED cells (have assigned physics):")
for pair, phys in sorted(assigned_pairs.items()):
    val1, val2 = OPERATORS[pair[0]], OPERATORS[pair[1]]
    product = val1 * val2
    ratio = val1 / val2 if val2 != 0 else None
    print(f"  {pair[0]:>8s} x {pair[1]:>8s} = {product:>12.6f}  (ratio: {ratio:.6f})  --> {phys}")

print()
print("EMPTY cells (no assigned physics):")
empty_cells = []
for i, op1 in enumerate(op_names):
    for j, op2 in enumerate(op_names):
        if i <= j:
            key = (op1, op2)
            rev = (op2, op1)
            if key not in assigned_pairs and rev not in assigned_pairs:
                v1, v2 = OPERATORS[op1], OPERATORS[op2]
                product = v1 * v2
                ratio = v1 / v2 if v2 != 0 else None
                ratio_inv = v2 / v1 if v1 != 0 else None

                # Check if product or ratio matches any unmapped constant
                matches_p = []
                matches_r = []
                for cname, cinfo in unmapped.items():
                    target = cinfo["value"]
                    if target == 0:
                        continue
                    if abs(product - target) / abs(target) < 0.05:
                        matches_p.append(cname)
                    if ratio and abs(ratio - target) / abs(target) < 0.05:
                        matches_r.append(cname)
                    if ratio_inv and abs(ratio_inv - target) / abs(target) < 0.05:
                        matches_r.append(f"{cname} (inv)")

                match_str = ""
                if matches_p:
                    match_str += f" PRODUCT matches: {', '.join(matches_p)}"
                if matches_r:
                    match_str += f" RATIO matches: {', '.join(matches_r)}"

                empty_cells.append((op1, op2, product, ratio, match_str))
                marker = "<-- MATCH" if (matches_p or matches_r) else ""
                print(f"  {op1:>8s} x {op2:>8s} = {product:>12.6f}  (ratio: {ratio:.6f})  {marker}")
                if match_str:
                    print(f"{'':>40s}{match_str}")

# ============================================================
# MISSING OSCILLATOR ANALYSIS
# ============================================================
print()
print("=" * 80)
print("  MISSING OSCILLATOR ANALYSIS")
print("  Are there constants that CANNOT come from 6 operators?")
print("=" * 80)
print()

# For each unmapped constant, what's the minimum error achievable
# from any combination of our operators?
print("Constants that resist ALL operator combinations:")
print(f"  (minimum error > 5% from any combo of {len(combos)} tried)")
print()

stubborn = {}
for const_name, const_info in CONSTANTS.items():
    if const_info["status"] in ("MAPPED", "DERIVED"):
        continue

    target = const_info["value"]
    if target == 0:
        continue

    best_err = float('inf')
    best_combo = None

    for combo_name, combo_val in combos.items():
        if combo_val == 0:
            continue
        err = abs(combo_val - target) / abs(target)
        neg_err = abs(-combo_val - target) / abs(target)
        err = min(err, neg_err)
        if err < best_err:
            best_err = err
            best_combo = combo_name

    if best_err > 0.05:
        stubborn[const_name] = {"error": best_err, "best_combo": best_combo, "target": target}

if stubborn:
    for name, info in sorted(stubborn.items(), key=lambda x: x[1]["error"], reverse=True):
        print(f"  {name:>30s}  target={info['target']:.6f}  best={info['best_combo']} (err {info['error']*100:.1f}%)")
    print()
    print(f"  --> {len(stubborn)} constants resist simple combinations.")
    print(f"  --> These may need: higher-order combos, new operators, or dynamic computation.")
else:
    print(f"  --> ALL constants are within 5% of some operator combination!")

# ============================================================
# THE COMPLETE MAP: What Each Operator Pair Produces
# ============================================================
print()
print("=" * 80)
print("  COMPLETE MODULATION MAP")
print("  Every operator pair, what it produces, what it COULD produce")
print("=" * 80)
print()

# For each pair, show: product, ratio, what constant it's assigned to, what else it's close to
all_targets = [(k, v["value"]) for k, v in CONSTANTS.items() if v["value"] != 0]

for i, op1 in enumerate(op_names):
    for j, op2 in enumerate(op_names):
        if i > j:
            continue
        v1, v2 = OPERATORS[op1], OPERATORS[op2]
        prod = v1 * v2
        ratio = v1 / v2 if v2 != 0 else None
        ratio_inv = v2 / v1 if v1 != 0 else None

        key = (op1, op2)
        rev = (op2, op1)
        assigned = assigned_pairs.get(key) or assigned_pairs.get(rev)

        # Find what the product/ratio are close to
        close_to_prod = []
        close_to_ratio = []
        for cname, cval in all_targets:
            if cval == 0:
                continue
            if abs(prod - cval) / abs(cval) < 0.10:
                err = abs(prod - cval) / abs(cval) * 100
                close_to_prod.append(f"{cname} ({err:.1f}%)")
            if ratio and abs(ratio - cval) / abs(cval) < 0.10:
                err = abs(ratio - cval) / abs(cval) * 100
                close_to_ratio.append(f"{cname} ({err:.1f}%)")
            if ratio_inv and abs(ratio_inv - cval) / abs(cval) < 0.10:
                err = abs(ratio_inv - cval) / abs(cval) * 100
                close_to_ratio.append(f"1/({cname}) ({err:.1f}%)")

        status = "ASSIGNED" if assigned else "EMPTY"
        print(f"  [{status:>8s}] {op1:>8s} x {op2:>8s}:")
        print(f"{'':>14s}product = {prod:.8f}")
        if ratio:
            print(f"{'':>14s}ratio   = {ratio:.8f}")
        if ratio_inv and ratio_inv != ratio:
            print(f"{'':>14s}inv.rat = {ratio_inv:.8f}")
        if assigned:
            print(f"{'':>14s}--> {assigned}")
        if close_to_prod:
            print(f"{'':>14s}product ~ {'; '.join(close_to_prod)}")
        if close_to_ratio:
            print(f"{'':>14s}ratio ~ {'; '.join(close_to_ratio)}")
        print()

# ============================================================
# SUMMARY: The State of the FM Model
# ============================================================
print("=" * 80)
print("  SUMMARY: STATE OF THE FM REALITY MODEL")
print("=" * 80)
print()

n_total = len(CONSTANTS)
n_mapped = sum(1 for v in CONSTANTS.values() if v["status"] == "MAPPED")
n_partial = sum(1 for v in CONSTANTS.values() if v["status"] == "PARTIAL")
n_unmapped = sum(1 for v in CONSTANTS.values() if v["status"] == "UNMAPPED")
n_derived = sum(1 for v in CONSTANTS.values() if v["status"] in ("DERIVED", "CLAIMED"))
n_pairs_total = len(op_names) * (len(op_names) + 1) // 2
n_pairs_filled = len(assigned_pairs)
n_pairs_empty = n_pairs_total - n_pairs_filled

print(f"CONSTANTS:")
print(f"  Total tracked:    {n_total}")
print(f"  Fully mapped:     {n_mapped} ({100*n_mapped/n_total:.0f}%)")
print(f"  Partially mapped: {n_partial}")
print(f"  Unmapped:         {n_unmapped}")
print(f"  Derived/claimed:  {n_derived}")
print()

print(f"OPERATOR MATRIX (6x6 upper triangle):")
print(f"  Total cells:   {n_pairs_total}")
print(f"  Filled cells:  {n_pairs_filled} ({100*n_pairs_filled/n_pairs_total:.0f}%)")
print(f"  Empty cells:   {n_pairs_empty}")
print()

print(f"GAPS ANALYSIS:")
print(f"  Constants found by scan:  {len(hits)}")
print(f"  Stubborn (>5% off):       {len(stubborn)}")
print(f"  Combinations tried:       {len(combos)}")
print()

print("EMPTY CELLS (the gaps in the modulation matrix):")
for op1, op2, prod, ratio, matches in empty_cells:
    assigned_mark = "?" if not matches else "!"
    ratio_str = f"{ratio:.6f}" if ratio else "N/A"
    print(f"  [{assigned_mark}] {op1:>8s} x {op2:>8s}  product={prod:.6f}  ratio={ratio_str}")

print()
print("DIAGNOSIS:")
print("  The empty cells in the modulation matrix are:")
for op1, op2, prod, ratio, matches in empty_cells:
    if matches:
        print(f"    {op1} x {op2}: HAS potential matches --{matches}")
    else:
        print(f"    {op1} x {op2}: product={prod:.6f}, ratio={ratio:.6f} -- no known constant nearby")

print()
print("  If the FM model is complete with 6 operators, EVERY physical")
print("  constant should appear somewhere in the modulation matrix.")
print(f"  Currently: {n_mapped + n_partial}/{n_total} constants are accounted for.")
print(f"  The {n_unmapped} unmapped constants either:")
print("    (a) Live in higher-order combinations (3+ operators)")
print("    (b) Need a 7th operator (= missing oscillator)")
print("    (c) Are dynamical, not algebraic (fermion masses)")
