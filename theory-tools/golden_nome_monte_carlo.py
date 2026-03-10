#!/usr/bin/env python3
"""
GOLDEN NOME MONTE CARLO — Is q = 1/phi Statistically Exceptional?
===================================================================

THE MOST IMPORTANT CALCULATION for Interface Theory:

The framework evaluates modular forms at nome q = 1/phi ~ 0.618 and claims
to match ~37 Standard Model constants. This script tests whether q = 1/phi
is genuinely exceptional compared to random nomes, using IDENTICAL formula
templates for all nomes.

Tests:
  A) Total match count at different precision tiers (0.01%, 0.1%, 1%)
  B) Simultaneous match of 3 core coupling formulas
  C) The "56 relation" test
  D) Best-performing nome identification
  E) Distribution analysis and percentile ranking

Uses ONLY standard Python. No external dependencies.

Author: Monte Carlo assessment for Interface Theory
Date: Feb 25, 2026
"""

import math
import random
import time
import sys

# Force UTF-8 output on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

# ============================================================
# CONSTANTS
# ============================================================

PHI = (1 + math.sqrt(5)) / 2   # 1.6180339887...
PHIBAR = 1 / PHI               # 0.6180339887... = phi - 1
SQRT5 = math.sqrt(5)
LN_PHI = math.log(PHI)

# ============================================================
# MODULAR FORM EVALUATION
# ============================================================

def eta_function(q, N=100):
    """Dedekind eta function: q^(1/24) * prod(1 - q^n)"""
    if q <= 0 or q >= 1:
        return None
    result = q ** (1.0 / 24.0)
    for n in range(1, N + 1):
        qn = q ** n
        if qn < 1e-16:
            break
        result *= (1 - qn)
    return result

def theta2(q, N=50):
    """Jacobi theta2: 2*q^(1/4) * sum(q^(n(n+1)))"""
    if q <= 0 or q >= 1:
        return None
    s = 0.0
    for n in range(0, N + 1):
        term = q ** (n * (n + 1))
        if term < 1e-16:
            break
        s += term
    return 2 * q ** 0.25 * s

def theta3(q, N=50):
    """Jacobi theta3: 1 + 2*sum(q^(n^2))"""
    if q <= 0 or q >= 1:
        return None
    s = 1.0
    for n in range(1, N + 1):
        term = q ** (n * n)
        if term < 1e-16:
            break
        s += 2 * term
    return s

def theta4(q, N=50):
    """Jacobi theta4: 1 + 2*sum((-1)^n * q^(n^2))"""
    if q <= 0 or q >= 1:
        return None
    s = 1.0
    for n in range(1, N + 1):
        term = q ** (n * n)
        if term < 1e-16:
            break
        s += 2 * ((-1) ** n) * term
    return s

def eval_modular(q):
    """Evaluate all four modular forms at nome q. Returns (eta, t2, t3, t4) or None."""
    e = eta_function(q)
    t2 = theta2(q)
    t3 = theta3(q)
    t4 = theta4(q)
    if any(v is None for v in [e, t2, t3, t4]):
        return None
    if any(v == 0 for v in [t3, t4]):
        return None
    return (e, t2, t3, t4)


# ============================================================
# TARGET PHYSICAL CONSTANTS
# ============================================================

TARGETS = {
    # Gauge couplings
    "alpha_s":         0.1179,       # strong coupling at M_Z
    "sin2_tW":         0.23122,      # Weinberg angle
    "1/alpha":         137.036,      # fine structure inverse
    "alpha_em":        1/137.036,    # fine structure

    # Mass ratios (dimensionless)
    "mu":              1836.153,     # proton/electron mass
    "m_mu/m_e":        206.768,      # muon/electron mass
    "m_tau/m_e":       3477.23,      # tau/electron mass
    "m_u/m_d":         0.47,         # up/down quark mass ratio
    "m_s/m_d":         20.2,         # strange/down quark mass ratio
    "m_c/m_s":         11.7,         # charm/strange quark mass ratio
    "m_t/m_b":         41.3,         # top/bottom quark mass ratio
    "m_b/m_c":         3.29,         # bottom/charm quark mass ratio

    # CKM matrix elements
    "V_us":            0.2243,       # CKM V_us
    "V_cb":            0.0422,       # CKM V_cb
    "V_ub":            0.00394,      # CKM V_ub

    # PMNS mixing angles
    "sin2_t12":        0.307,        # solar mixing
    "sin2_t23":        0.572,        # atmospheric mixing
    "sin2_t13":        0.02203,      # reactor mixing

    # Cosmological
    "Omega_m":         0.315,        # matter fraction
    "Omega_Lambda":    0.685,        # dark energy fraction
    "Omega_b":         0.0493,       # baryon fraction
    "eta_B":           6.12e-10,     # baryon asymmetry

    # Dimensionless combinations
    "m_H/v":           0.5088,       # Higgs mass / VEV
    "m_W/m_Z":         0.8815,       # W/Z mass ratio
    "gamma_Immirzi":   0.2375,       # Immirzi parameter (LQG)
}

TARGET_LIST = list(TARGETS.items())
N_TARGETS = len(TARGET_LIST)


# ============================================================
# FORMULA TEMPLATES
#
# These are the SAME for every nome q. Each template takes
# (q, eta, t2, t3, t4) and returns a numerical value.
# We use phi as a constant (it's part of the template).
# ============================================================

def build_formula_templates():
    """
    Build a list of (name, function) pairs.
    Each function takes (eta, t2, t3, t4, q) and returns a value.
    Returns list of (name, func).
    """
    templates = []

    # Helper: safe evaluation
    def safe(val):
        if val is None or not math.isfinite(val):
            return None
        if abs(val) > 1e15 or abs(val) < 1e-15:
            return None
        return abs(val)

    # ---- GROUP 1: Single modular form (the simplest) ----
    # Template 1: eta alone (framework's alpha_s formula)
    templates.append(("eta", lambda e, t2, t3, t4, q: safe(e)))

    # Powers of eta
    for p in [0.5, 2, 3, -1, -0.5, -2]:
        pname = f"eta^{p}"
        templates.append((pname, lambda e, t2, t3, t4, q, _p=p: safe(e**_p)))

    # Powers of theta3
    for p in [0.5, 1, 2, 3, -1, -0.5, -2]:
        pname = f"t3^{p}"
        templates.append((pname, lambda e, t2, t3, t4, q, _p=p: safe(t3**_p)))

    # Powers of theta4
    for p in [0.5, 1, 2, 3, -1, -0.5, -2]:
        pname = f"t4^{p}"
        templates.append((pname, lambda e, t2, t3, t4, q, _p=p: safe(t4**_p)))

    # Powers of theta2
    for p in [0.5, 1, 2, -1]:
        pname = f"t2^{p}"
        templates.append((pname, lambda e, t2, t3, t4, q, _p=p: safe(t2**_p)))

    # ---- GROUP 2: Two-form products/ratios ----
    # Template 2: eta^2/(2*t4) (framework's sin^2 theta_W)
    templates.append(("eta^2/(2*t4)", lambda e, t2, t3, t4, q: safe(e**2 / (2*t4))))

    # Template 3: t3*phi/t4 (framework's 1/alpha)
    templates.append(("t3*phi/t4", lambda e, t2, t3, t4, q: safe(t3*PHI/t4)))

    # Other two-form ratios
    templates.append(("eta/t4", lambda e, t2, t3, t4, q: safe(e/t4)))
    templates.append(("eta/t3", lambda e, t2, t3, t4, q: safe(e/t3)))
    templates.append(("eta*t3", lambda e, t2, t3, t4, q: safe(e*t3)))
    templates.append(("eta*t4", lambda e, t2, t3, t4, q: safe(e*t4)))
    templates.append(("t3/t4", lambda e, t2, t3, t4, q: safe(t3/t4)))
    templates.append(("t4/t3", lambda e, t2, t3, t4, q: safe(t4/t3)))
    templates.append(("t2/t3", lambda e, t2, t3, t4, q: safe(t2/t3)))
    templates.append(("t2/t4", lambda e, t2, t3, t4, q: safe(t2/t4)))
    templates.append(("eta^2*t3", lambda e, t2, t3, t4, q: safe(e**2*t3)))
    templates.append(("eta^2*t4", lambda e, t2, t3, t4, q: safe(e**2*t4)))
    templates.append(("eta^2/t3", lambda e, t2, t3, t4, q: safe(e**2/t3)))
    templates.append(("t3^2/t4", lambda e, t2, t3, t4, q: safe(t3**2/t4)))
    templates.append(("t4^2/t3", lambda e, t2, t3, t4, q: safe(t4**2/t3)))
    templates.append(("eta*t3/t4", lambda e, t2, t3, t4, q: safe(e*t3/t4)))
    templates.append(("eta*t4/t3", lambda e, t2, t3, t4, q: safe(e*t4/t3)))

    # ---- GROUP 3: With phi multipliers ----
    phi_factors = [
        ("phi", PHI), ("1/phi", PHIBAR), ("phi^2", PHI**2),
        ("1/phi^2", PHIBAR**2), ("sqrt5", SQRT5), ("ln_phi", LN_PHI),
        ("phi^3", PHI**3), ("1/phi^3", PHIBAR**3),
        ("phi^0.5", PHI**0.5), ("phi^1.5", PHI**1.5),
    ]

    # Single modular * phi
    for mname, mfunc_idx in [("eta", 0), ("t3", 2), ("t4", 3), ("t2", 1)]:
        for pname, pval in phi_factors:
            name = f"{mname}*{pname}"
            if mfunc_idx == 0:
                templates.append((name, lambda e, t2, t3, t4, q, _p=pval: safe(e*_p)))
            elif mfunc_idx == 1:
                templates.append((name, lambda e, t2, t3, t4, q, _p=pval: safe(t2*_p)))
            elif mfunc_idx == 2:
                templates.append((name, lambda e, t2, t3, t4, q, _p=pval: safe(t3*_p)))
            elif mfunc_idx == 3:
                templates.append((name, lambda e, t2, t3, t4, q, _p=pval: safe(t4*_p)))

    # Two-form ratios * phi
    for pname, pval in phi_factors:
        templates.append((f"eta^2/(2*t4)*{pname}",
                          lambda e, t2, t3, t4, q, _p=pval: safe(e**2/(2*t4)*_p)))
        templates.append((f"t3/t4*{pname}",
                          lambda e, t2, t3, t4, q, _p=pval: safe(t3/t4*_p)))
        templates.append((f"eta/t4*{pname}",
                          lambda e, t2, t3, t4, q, _p=pval: safe(e/t4*_p)))
        templates.append((f"eta*t3*{pname}",
                          lambda e, t2, t3, t4, q, _p=pval: safe(e*t3*_p)))
        templates.append((f"eta*t4*{pname}",
                          lambda e, t2, t3, t4, q, _p=pval: safe(e*t4*_p)))
        templates.append((f"eta^2*t3*{pname}",
                          lambda e, t2, t3, t4, q, _p=pval: safe(e**2*t3*_p)))

    # ---- GROUP 4: With small integer multipliers/divisors ----
    small_ints = [2, 3, 4, 5, 6, 7, 8, 9, 10]

    for n in small_ints:
        templates.append((f"eta*{n}", lambda e, t2, t3, t4, q, _n=n: safe(e*_n)))
        templates.append((f"eta/{n}", lambda e, t2, t3, t4, q, _n=n: safe(e/_n)))
        templates.append((f"t3/{n}", lambda e, t2, t3, t4, q, _n=n: safe(t3/_n)))
        templates.append((f"t4/{n}", lambda e, t2, t3, t4, q, _n=n: safe(t4/_n)))
        templates.append((f"t3*{n}", lambda e, t2, t3, t4, q, _n=n: safe(t3*_n)))
        templates.append((f"t4*{n}", lambda e, t2, t3, t4, q, _n=n: safe(t4*_n)))
        templates.append((f"eta^2/{n}", lambda e, t2, t3, t4, q, _n=n: safe(e**2/_n)))

    # Two-form * integer * phi
    for n in [2, 3, 5, 7]:
        for pname, pval in phi_factors[:5]:
            templates.append((f"eta*t3*{pname}*{n}",
                              lambda e, t2, t3, t4, q, _p=pval, _n=n: safe(e*t3*_p*_n)))
            templates.append((f"eta*t3*{pname}/{n}",
                              lambda e, t2, t3, t4, q, _p=pval, _n=n: safe(e*t3*_p/_n)))
            templates.append((f"t3/t4*{pname}*{n}",
                              lambda e, t2, t3, t4, q, _p=pval, _n=n: safe(t3/t4*_p*_n)))
            templates.append((f"t3/t4*{pname}/{n}",
                              lambda e, t2, t3, t4, q, _p=pval, _n=n: safe(t3/t4*_p/_n)))
            templates.append((f"eta/t4*{pname}*{n}",
                              lambda e, t2, t3, t4, q, _p=pval, _n=n: safe(e/t4*_p*_n)))
            templates.append((f"eta/t4*{pname}/{n}",
                              lambda e, t2, t3, t4, q, _p=pval, _n=n: safe(e/t4*_p/_n)))

    # ---- GROUP 5: q-dependent but not through modular forms ----
    # t3^2 * ln(1/q) (the pi formula)
    templates.append(("t3^2*ln(1/q)", lambda e, t2, t3, t4, q: safe(t3**2 * math.log(1/q))))

    # ---- GROUP 6: Higher power combinations ----
    templates.append(("eta^3/t4", lambda e, t2, t3, t4, q: safe(e**3/t4)))
    templates.append(("eta^3*t3", lambda e, t2, t3, t4, q: safe(e**3*t3)))
    templates.append(("eta^3*t4", lambda e, t2, t3, t4, q: safe(e**3*t4)))
    templates.append(("t3^2*t4", lambda e, t2, t3, t4, q: safe(t3**2*t4)))
    templates.append(("t3*t4^2", lambda e, t2, t3, t4, q: safe(t3*t4**2)))
    templates.append(("eta*t3^2", lambda e, t2, t3, t4, q: safe(e*t3**2)))
    templates.append(("eta*t4^2", lambda e, t2, t3, t4, q: safe(e*t4**2)))
    templates.append(("eta^2*t3^2", lambda e, t2, t3, t4, q: safe(e**2*t3**2)))
    templates.append(("eta*t3^2/t4", lambda e, t2, t3, t4, q: safe(e*t3**2/t4)))
    templates.append(("eta*t4^2/t3", lambda e, t2, t3, t4, q: safe(e*t4**2/t3)))

    # With phi multipliers on higher powers
    for pname, pval in phi_factors[:6]:
        templates.append((f"eta^3/t4*{pname}",
                          lambda e, t2, t3, t4, q, _p=pval: safe(e**3/t4*_p)))
        templates.append((f"eta*t3^2*{pname}",
                          lambda e, t2, t3, t4, q, _p=pval: safe(e*t3**2*_p)))
        templates.append((f"t3^2*t4*{pname}",
                          lambda e, t2, t3, t4, q, _p=pval: safe(t3**2*t4*_p)))
        templates.append((f"eta*t3^2/t4*{pname}",
                          lambda e, t2, t3, t4, q, _p=pval: safe(e*t3**2/t4*_p)))

    # ---- GROUP 7: High powers (for cosmological constant, baryon asymmetry) ----
    for base_name in ["t4", "eta"]:
        for exp in [6, 8, 10, 20, 40, 44, 60, 80]:
            name = f"{base_name}^{exp}"
            if base_name == "t4":
                templates.append((name, lambda e, t2, t3, t4, q, _exp=exp: safe(t4**_exp)))
                templates.append((f"{name}*sqrt5/phi^2",
                    lambda e, t2, t3, t4, q, _exp=exp: safe(t4**_exp * SQRT5/PHI**2)))
            else:
                templates.append((name, lambda e, t2, t3, t4, q, _exp=exp: safe(e**_exp)))
                templates.append((f"{name}*sqrt5/phi^2",
                    lambda e, t2, t3, t4, q, _exp=exp: safe(e**_exp * SQRT5/PHI**2)))

    # ---- GROUP 8: Phi-only formulas (q-independent, included for fairness) ----
    # These represent the framework's non-modular matches
    phi_only_vals = []
    for exp in [-5, -4, -3.5, -3, -2.5, -2, -1.5, -1, -0.5, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 5]:
        phi_only_vals.append((f"PHI^{exp}", PHI**exp))

    for n in [2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 15, 18, 24, 30, 60, 120, 360, 720, 7776]:
        for exp in [-3, -2, -1, -0.5, 0.5, 1, 1.5, 2, 3]:
            val = n * PHI**exp
            if 1e-12 < val < 1e12:
                templates.append((f"{n}*phi^{exp}",
                    lambda e, t2, t3, t4, q, _v=val: safe(_v)))
            val2 = PHI**exp / n
            if 1e-12 < val2 < 1e12:
                templates.append((f"phi^{exp}/{n}",
                    lambda e, t2, t3, t4, q, _v=val2: safe(_v)))

    # n/m ratios
    for n in range(1, 11):
        for m in range(1, 11):
            if n != m:
                templates.append((f"{n}/{m}",
                    lambda e, t2, t3, t4, q, _v=n/m: safe(_v)))

    # 1/(3*phi^2) = gamma_Immirzi
    templates.append(("1/(3*phi^2)", lambda e, t2, t3, t4, q: safe(1/(3*PHI**2))))

    # 7776/phi^3 = mu (6^5/phi^3)
    templates.append(("6^5/phi^3", lambda e, t2, t3, t4, q: safe(7776/PHI**3)))

    # phibar high powers (for eta_B)
    for exp in [20, 30, 40, 44, 50, 60, 70, 80]:
        templates.append((f"phibar^{exp}",
            lambda e, t2, t3, t4, q, _exp=exp: safe(PHIBAR**_exp)))
        templates.append((f"phibar^{exp}*sqrt5/phi^2",
            lambda e, t2, t3, t4, q, _exp=exp: safe(PHIBAR**_exp * SQRT5/PHI**2)))

    return templates


def evaluate_templates(templates, eta_v, t2_v, t3_v, t4_v, q_val):
    """Evaluate all templates at given modular form values. Returns list of (name, value)."""
    results = []
    for name, func in templates:
        try:
            val = func(eta_v, t2_v, t3_v, t4_v, q_val)
            if val is not None:
                results.append((name, val))
        except:
            pass
    return results


def count_target_matches(formula_values, threshold=0.01):
    """
    Count how many distinct targets are matched by at least one formula.
    Returns (n_targets_matched, details_dict).
    """
    matched = {}
    for tname, tval in TARGET_LIST:
        atval = abs(tval)
        if atval == 0:
            continue
        best_pct = float('inf')
        best_name = ""
        for fname, fval in formula_values:
            pct = abs(fval - atval) / atval
            if pct < best_pct:
                best_pct = pct
                best_name = fname
        if best_pct < threshold:
            matched[tname] = {"pct": best_pct * 100, "formula": best_name}
    return len(matched), matched


# ============================================================
# THE THREE CORE FORMULAS — FIXED, NOT SCANNED
# ============================================================

def test_core_formulas(eta_v, t3_v, t4_v):
    """
    Test the 3 specific framework formulas (not template scan):
      1) alpha_s = eta(q)                  target: 0.1179
      2) sin^2(theta_W) = eta^2/(2*t4)    target: 0.23122
      3) 1/alpha = t3*phi/t4              target: 137.036

    Returns dict with values and percent errors.
    """
    result = {}

    # Formula 1: alpha_s
    val1 = eta_v
    err1 = abs(val1 - 0.1179) / 0.1179
    result["alpha_s"] = {"val": val1, "target": 0.1179, "err_pct": err1 * 100}

    # Formula 2: sin^2 theta_W
    val2 = eta_v**2 / (2 * t4_v)
    err2 = abs(val2 - 0.23122) / 0.23122
    result["sin2_tW"] = {"val": val2, "target": 0.23122, "err_pct": err2 * 100}

    # Formula 3: 1/alpha
    val3 = t3_v * PHI / t4_v
    err3 = abs(val3 - 137.036) / 137.036
    result["1/alpha"] = {"val": val3, "target": 137.036, "err_pct": err3 * 100}

    return result


def test_56_relation(t3_v, t4_v):
    """
    Test the 56 relation:
      alpha_q = t4/(t3*phi)           (simplified tree-level alpha)
      mu_q = 6^5/phi^3                (constant)
      Test: alpha_q^(-1/4) * sqrt(mu_q) * phi^(-2) ~ 56?

    Returns (value, ppm_deviation).
    """
    alpha_q = t4_v / (t3_v * PHI)
    mu_q = 7776 / PHI**3  # 6^5/phi^3

    try:
        val = alpha_q**(-0.25) * math.sqrt(mu_q) * PHI**(-2)
        ppm = abs(val - 56) / 56 * 1e6
        return val, ppm
    except:
        return None, None


# ============================================================
# MAIN MONTE CARLO
# ============================================================

def main():
    print("=" * 80)
    print("  GOLDEN NOME MONTE CARLO")
    print("  Is q = 1/phi Statistically Exceptional?")
    print("=" * 80)
    print()

    random.seed(42)
    t_start = time.time()

    # Build templates (same for all nomes)
    templates = build_formula_templates()
    n_templates = len(templates)
    print(f"Formula templates: {n_templates}")
    print(f"Target constants:  {N_TARGETS}")
    print()

    # ================================================================
    # STEP 1: Evaluate q = 1/phi
    # ================================================================
    print("-" * 80)
    print("STEP 1: q = 1/phi (the framework's claimed special nome)")
    print("-" * 80)
    print()

    q_phi = 1.0 / PHI
    mf_phi = eval_modular(q_phi)
    eta_phi, t2_phi, t3_phi, t4_phi = mf_phi

    print(f"  q = 1/phi = {q_phi:.10f}")
    print(f"  eta(q)    = {eta_phi:.10f}")
    print(f"  theta2(q) = {t2_phi:.10f}")
    print(f"  theta3(q) = {t3_phi:.10f}")
    print(f"  theta4(q) = {t4_phi:.10f}")
    print()

    # Core formula test at q = 1/phi
    core_phi = test_core_formulas(eta_phi, t3_phi, t4_phi)
    print("  Core formulas at q = 1/phi:")
    for name, info in core_phi.items():
        print(f"    {name:12s}: {info['val']:.6f} vs {info['target']:.6f}  "
              f"(error: {info['err_pct']:.4f}%)")

    # 56 relation at q = 1/phi
    val56_phi, ppm56_phi = test_56_relation(t3_phi, t4_phi)
    print(f"\n  56 relation at q = 1/phi: {val56_phi:.8f}  (deviation: {ppm56_phi:.1f} ppm)")

    # Full template scan at q = 1/phi
    fvals_phi = evaluate_templates(templates, eta_phi, t2_phi, t3_phi, t4_phi, q_phi)

    # Count at different precision tiers
    phi_tier1_n, phi_tier1 = count_target_matches(fvals_phi, threshold=0.0001)  # 0.01%
    phi_tier2_n, phi_tier2 = count_target_matches(fvals_phi, threshold=0.001)   # 0.1%
    phi_tier3_n, phi_tier3 = count_target_matches(fvals_phi, threshold=0.01)    # 1%

    print(f"\n  Match counts at q = 1/phi ({len(fvals_phi)} formula values):")
    print(f"    Tier 1 (within 0.01%, 4+ sig figs): {phi_tier1_n} / {N_TARGETS}")
    print(f"    Tier 2 (within 0.1%,  3+ sig figs): {phi_tier2_n} / {N_TARGETS}")
    print(f"    Tier 3 (within 1%,    2+ sig figs): {phi_tier3_n} / {N_TARGETS}")

    print(f"\n  Tier 3 matches (within 1%):")
    for tname, info in sorted(phi_tier3.items(), key=lambda x: x[1]["pct"]):
        tier = "T1" if tname in phi_tier1 else ("T2" if tname in phi_tier2 else "T3")
        print(f"    [{tier}] {tname:20s}: {info['pct']:.4f}%  via {info['formula']}")

    # ================================================================
    # STEP 2: Monte Carlo over random nomes
    # ================================================================
    N_TRIALS = 10000
    Q_MIN, Q_MAX = 0.30, 0.70

    print()
    print("-" * 80)
    print(f"STEP 2: Monte Carlo with {N_TRIALS} random nomes in [{Q_MIN}, {Q_MAX}]")
    print("-" * 80)
    print()

    # Storage
    mc_tier1 = []  # 0.01% match counts
    mc_tier2 = []  # 0.1% match counts
    mc_tier3 = []  # 1% match counts
    mc_core_simultaneous = 0   # all 3 core within 1%
    mc_core_tight = 0          # all 3 core within 0.1%
    mc_56_within_1ppm = 0
    mc_56_within_10ppm = 0
    mc_56_within_100ppm = 0
    mc_56_within_1000ppm = 0
    mc_56_values = []
    mc_best_tier3 = 0
    mc_best_tier3_q = None
    mc_best_tier2 = 0
    mc_best_tier2_q = None

    # Track which nomes match all 3 core simultaneously
    core_match_qs = []

    t0 = time.time()
    for trial in range(N_TRIALS):
        q = random.uniform(Q_MIN, Q_MAX)
        mf = eval_modular(q)
        if mf is None:
            mc_tier1.append(0)
            mc_tier2.append(0)
            mc_tier3.append(0)
            continue

        e, tv2, tv3, tv4 = mf

        # Full template evaluation
        fvals = evaluate_templates(templates, e, tv2, tv3, tv4, q)

        # Precision tiers
        n1, _ = count_target_matches(fvals, threshold=0.0001)
        n2, _ = count_target_matches(fvals, threshold=0.001)
        n3, _ = count_target_matches(fvals, threshold=0.01)
        mc_tier1.append(n1)
        mc_tier2.append(n2)
        mc_tier3.append(n3)

        if n3 > mc_best_tier3:
            mc_best_tier3 = n3
            mc_best_tier3_q = q
        if n2 > mc_best_tier2:
            mc_best_tier2 = n2
            mc_best_tier2_q = q

        # Core formula simultaneous test
        core = test_core_formulas(e, tv3, tv4)
        all_1pct = all(core[k]["err_pct"] < 1.0 for k in core)
        all_01pct = all(core[k]["err_pct"] < 0.1 for k in core)
        if all_1pct:
            mc_core_simultaneous += 1
            core_match_qs.append(q)
        if all_01pct:
            mc_core_tight += 1

        # 56 relation test
        val56, ppm56 = test_56_relation(tv3, tv4)
        if val56 is not None:
            mc_56_values.append(ppm56)
            if ppm56 < 1:
                mc_56_within_1ppm += 1
            if ppm56 < 10:
                mc_56_within_10ppm += 1
            if ppm56 < 100:
                mc_56_within_100ppm += 1
            if ppm56 < 1000:
                mc_56_within_1000ppm += 1

        # Progress
        if (trial + 1) % 2000 == 0:
            elapsed = time.time() - t0
            rate = (trial + 1) / elapsed
            remaining = (N_TRIALS - trial - 1) / rate
            print(f"  Trial {trial+1}/{N_TRIALS}: "
                  f"avg T3={sum(mc_tier3)/(trial+1):.1f}, "
                  f"core_sim={mc_core_simultaneous}, "
                  f"~{remaining:.0f}s remaining")

    elapsed_total = time.time() - t0
    print(f"\n  Completed {N_TRIALS} trials in {elapsed_total:.1f}s")

    # ================================================================
    # STEP 3: Results Analysis
    # ================================================================
    print()
    print("=" * 80)
    print("  RESULTS")
    print("=" * 80)

    # Helper function for statistics
    def stats(data):
        n = len(data)
        if n == 0:
            return 0, 0, 0, 0, 0
        mean = sum(data) / n
        var = sum((x - mean) ** 2 for x in data) / n
        std = math.sqrt(var)
        med = sorted(data)[n // 2]
        return mean, std, min(data), max(data), med

    # ---- 3a: Distribution of match counts ----
    print()
    print("-" * 80)
    print("3a. DISTRIBUTION OF MATCH COUNTS")
    print("-" * 80)

    for tier_name, tier_data, phi_count in [
        ("Tier 3 (1% threshold)", mc_tier3, phi_tier3_n),
        ("Tier 2 (0.1% threshold)", mc_tier2, phi_tier2_n),
        ("Tier 1 (0.01% threshold)", mc_tier1, phi_tier1_n),
    ]:
        mean, std, mn, mx, med = stats(tier_data)
        n_gte = sum(1 for x in tier_data if x >= phi_count)
        pctile = 100 * (1 - n_gte / N_TRIALS)

        print(f"\n  {tier_name}:")
        print(f"    Random nomes:  mean={mean:.2f}, std={std:.2f}, "
              f"median={med}, range=[{mn}, {mx}]")
        print(f"    q = 1/phi:     {phi_count}")
        print(f"    Percentile:    {pctile:.1f}th  "
              f"({n_gte}/{N_TRIALS} random nomes >= framework)")
        if std > 0:
            z = (phi_count - mean) / std
            print(f"    Z-score:       {z:.2f}")

        # Histogram
        from collections import Counter
        hist = Counter(tier_data)
        print(f"    Histogram:")
        for k in sorted(hist.keys()):
            bar_len = max(1, hist[k] * 50 // N_TRIALS)
            marker = " <-- q=1/phi" if k == phi_count else ""
            print(f"      {k:3d}: {hist[k]:5d} ({hist[k]*100/N_TRIALS:5.1f}%) "
                  f"{'#' * bar_len}{marker}")

    # ---- 3b: Simultaneous core formula match ----
    print()
    print("-" * 80)
    print("3b. SIMULTANEOUS CORE FORMULA MATCH")
    print("-" * 80)
    print(f"    (eta = alpha_s) AND (eta^2/(2*t4) = sin^2 theta_W) AND (t3*phi/t4 = 1/alpha)")
    print()
    print(f"  All 3 within 1%:   {mc_core_simultaneous} / {N_TRIALS} = "
          f"{mc_core_simultaneous/N_TRIALS*100:.3f}%")
    print(f"  All 3 within 0.1%: {mc_core_tight} / {N_TRIALS} = "
          f"{mc_core_tight/N_TRIALS*100:.4f}%")

    # Does q = 1/phi match all 3?
    phi_all3_1pct = all(core_phi[k]["err_pct"] < 1.0 for k in core_phi)
    phi_all3_01pct = all(core_phi[k]["err_pct"] < 0.1 for k in core_phi)
    print(f"\n  q = 1/phi matches all 3 within 1%?  {'YES' if phi_all3_1pct else 'NO'}")
    print(f"  q = 1/phi matches all 3 within 0.1%? {'YES' if phi_all3_01pct else 'NO'}")

    if core_match_qs:
        print(f"\n  Random nomes that match all 3 within 1%:")
        for cq in core_match_qs[:20]:
            cmf = eval_modular(cq)
            if cmf:
                ce, _, ct3, ct4 = cmf
                cc = test_core_formulas(ce, ct3, ct4)
                errs = ", ".join(f"{k}:{cc[k]['err_pct']:.3f}%" for k in cc)
                print(f"    q = {cq:.6f}  ({errs})")
        if len(core_match_qs) > 20:
            print(f"    ... and {len(core_match_qs)-20} more")

    # ---- 3c: The 56 relation ----
    print()
    print("-" * 80)
    print("3c. THE 56 RELATION TEST")
    print("-" * 80)
    print(f"    alpha_q^(-1/4) * sqrt(mu_q) * phi^(-2) = 56?")
    print(f"    where alpha_q = t4/(t3*phi), mu_q = 6^5/phi^3")
    print()
    print(f"  At q = 1/phi:     value = {val56_phi:.8f}, deviation = {ppm56_phi:.1f} ppm")
    print()
    print(f"  Random nomes within   1 ppm of 56: {mc_56_within_1ppm} / {N_TRIALS} "
          f"({mc_56_within_1ppm/N_TRIALS*100:.3f}%)")
    print(f"  Random nomes within  10 ppm of 56: {mc_56_within_10ppm} / {N_TRIALS} "
          f"({mc_56_within_10ppm/N_TRIALS*100:.3f}%)")
    print(f"  Random nomes within 100 ppm of 56: {mc_56_within_100ppm} / {N_TRIALS} "
          f"({mc_56_within_100ppm/N_TRIALS*100:.3f}%)")
    print(f"  Random nomes within 1000 ppm of 56: {mc_56_within_1000ppm} / {N_TRIALS} "
          f"({mc_56_within_1000ppm/N_TRIALS*100:.3f}%)")

    if mc_56_values:
        mean56, std56, min56, max56, med56 = stats(mc_56_values)
        print(f"\n  Deviation distribution (ppm): mean={mean56:.0f}, "
              f"median={med56:.0f}, min={min56:.1f}, max={max56:.0f}")
        # Percentile of phi
        n_better56 = sum(1 for x in mc_56_values if x <= ppm56_phi)
        print(f"  q=1/phi percentile: {n_better56/len(mc_56_values)*100:.1f}th "
              f"(lower = better)")

    # ---- 3d: Best performing nome ----
    print()
    print("-" * 80)
    print("3d. BEST PERFORMING NOME")
    print("-" * 80)
    print()
    print(f"  Best at Tier 3 (1%):  q = {mc_best_tier3_q:.8f}  "
          f"({mc_best_tier3} targets matched)")
    print(f"  Best at Tier 2 (0.1%): q = {mc_best_tier2_q:.8f}  "
          f"({mc_best_tier2} targets matched)")
    print(f"  q = 1/phi:            Tier 3: {phi_tier3_n}, Tier 2: {phi_tier2_n}")

    is_best_t3 = phi_tier3_n >= mc_best_tier3
    is_best_t2 = phi_tier2_n >= mc_best_tier2
    print(f"\n  Is q = 1/phi the best at Tier 3? {'YES' if is_best_t3 else 'NO'}")
    print(f"  Is q = 1/phi the best at Tier 2? {'YES' if is_best_t2 else 'NO'}")

    # Evaluate the best nome in detail
    if mc_best_tier3_q is not None and not is_best_t3:
        print(f"\n  Detail for best Tier 3 nome (q = {mc_best_tier3_q:.8f}):")
        mf_best = eval_modular(mc_best_tier3_q)
        if mf_best:
            eb, t2b, t3b, t4b = mf_best
            fvals_best = evaluate_templates(templates, eb, t2b, t3b, t4b, mc_best_tier3_q)
            _, best_matches = count_target_matches(fvals_best, threshold=0.01)
            for tname, info in sorted(best_matches.items(), key=lambda x: x[1]["pct"]):
                print(f"    {tname:20s}: {info['pct']:.4f}%  via {info['formula']}")
            # Core formulas at best nome
            core_best = test_core_formulas(eb, t3b, t4b)
            print(f"  Core formulas at best nome:")
            for name, info in core_best.items():
                print(f"    {name:12s}: {info['val']:.6f} vs {info['target']:.6f}  "
                      f"(error: {info['err_pct']:.4f}%)")

    # ---- 3e: Special algebraic nomes ----
    print()
    print("-" * 80)
    print("3e. SPECIAL ALGEBRAICALLY DISTINGUISHED NOMES")
    print("-" * 80)
    print()

    special_nomes = [
        (1/PHI,           "1/phi (FRAMEWORK)"),
        (1/PHI**2,        "1/phi^2"),
        (SQRT5 - 2,       "sqrt(5)-2"),
        (1/math.e,        "1/e"),
        (1/math.pi,       "1/pi"),
        (2/math.pi,       "2/pi"),
        (1/math.sqrt(2),  "1/sqrt(2)"),
        (math.sqrt(2)-1,  "sqrt(2)-1"),
        (math.log(2),     "ln(2)"),
        (1/3,             "1/3"),
        (2/5,             "2/5"),
        (0.5,             "1/2"),
        (math.sqrt(3)-1,  "sqrt(3)-1"),
        ((math.sqrt(5)-1)/3, "(sqrt5-1)/3"),
    ]

    print(f"  {'Nome':25s} {'q':>10s} {'T3':>4s} {'T2':>4s} {'T1':>4s} "
          f"{'Core3?':>7s} {'56_ppm':>10s}")
    print(f"  {'-'*25} {'-'*10} {'-'*4} {'-'*4} {'-'*4} {'-'*7} {'-'*10}")

    for q_val, q_name in special_nomes:
        if q_val <= 0.001 or q_val >= 0.999:
            continue
        mf = eval_modular(q_val)
        if mf is None:
            print(f"  {q_name:25s} {q_val:10.6f}  -- failed --")
            continue
        e, tv2, tv3, tv4 = mf
        fvals = evaluate_templates(templates, e, tv2, tv3, tv4, q_val)
        n1, _ = count_target_matches(fvals, threshold=0.0001)
        n2, _ = count_target_matches(fvals, threshold=0.001)
        n3, _ = count_target_matches(fvals, threshold=0.01)

        core = test_core_formulas(e, tv3, tv4)
        all3 = all(core[k]["err_pct"] < 1.0 for k in core)

        v56, p56 = test_56_relation(tv3, tv4)
        p56_str = f"{p56:.1f}" if p56 is not None else "N/A"

        print(f"  {q_name:25s} {q_val:10.6f} {n3:4d} {n2:4d} {n1:4d} "
              f"{'YES' if all3 else 'no':>7s} {p56_str:>10s}")

    # ================================================================
    # STEP 4: q-DEPENDENT vs q-INDEPENDENT analysis
    # ================================================================
    print()
    print("-" * 80)
    print("3f. q-DEPENDENT vs q-INDEPENDENT MATCHES")
    print("-" * 80)
    print()
    print("  Identifying which targets are matched by q-independent (phi-only) formulas")
    print("  vs which REQUIRE modular forms at a specific q.")
    print()

    # Evaluate templates at a dummy q (phi-only formulas return same values)
    # We identify phi-only templates by checking if they give same value at q=0.4 and q=0.6
    mf_test1 = eval_modular(0.4)
    mf_test2 = eval_modular(0.6)
    if mf_test1 and mf_test2:
        fv1 = evaluate_templates(templates, *mf_test1, 0.4)
        fv2 = evaluate_templates(templates, *mf_test2, 0.6)

        # Build dict for easy lookup
        fv1_dict = {name: val for name, val in fv1}
        fv2_dict = {name: val for name, val in fv2}

        # Phi-only formulas: same value at both q's
        phi_only_fvals = []
        q_dep_fvals_phi = []
        for name, val in fvals_phi:
            v1 = fv1_dict.get(name)
            v2 = fv2_dict.get(name)
            if v1 is not None and v2 is not None and abs(v1 - v2) / max(abs(v1), 1e-15) < 0.0001:
                phi_only_fvals.append((name, val))
            else:
                q_dep_fvals_phi.append((name, val))

        n_phi_only_t3, phi_only_matches = count_target_matches(phi_only_fvals, threshold=0.01)
        n_q_dep_t3, q_dep_matches = count_target_matches(q_dep_fvals_phi, threshold=0.01)

        # Which targets are ONLY matched by q-dependent formulas?
        phi_only_targets = set(phi_only_matches.keys())
        q_dep_only_targets = set(q_dep_matches.keys()) - phi_only_targets

        print(f"  Phi-only formulas: {len(phi_only_fvals)} values, "
              f"match {n_phi_only_t3} targets within 1%")
        print(f"  q-dependent formulas: {len(q_dep_fvals_phi)} values, "
              f"match {n_q_dep_t3} targets within 1%")
        print(f"  Targets matched ONLY by q-dependent formulas: {len(q_dep_only_targets)}")
        for t in sorted(q_dep_only_targets):
            info = q_dep_matches[t]
            print(f"    {t:20s}: {info['pct']:.4f}% via {info['formula']}")

        # Which targets get BETTER match from q-dep formulas?
        improved = {}
        for t in set(q_dep_matches.keys()) & phi_only_targets:
            if q_dep_matches[t]["pct"] < phi_only_matches[t]["pct"] * 0.5:
                improved[t] = (phi_only_matches[t]["pct"], q_dep_matches[t]["pct"])

        if improved:
            print(f"\n  Targets significantly improved by q-dependent formulas:")
            for t, (old, new) in sorted(improved.items()):
                print(f"    {t:20s}: {old:.4f}% -> {new:.4f}% ({old/new:.1f}x better)")

    # ================================================================
    # FINAL SUMMARY
    # ================================================================
    print()
    print("=" * 80)
    print("  FINAL HONEST ASSESSMENT")
    print("=" * 80)
    print()

    # Percentiles for phi
    n_gte_t3 = sum(1 for x in mc_tier3 if x >= phi_tier3_n)
    n_gte_t2 = sum(1 for x in mc_tier2 if x >= phi_tier2_n)
    n_gte_t1 = sum(1 for x in mc_tier1 if x >= phi_tier1_n)
    pctile_t3 = 100 * (1 - n_gte_t3 / N_TRIALS)
    pctile_t2 = 100 * (1 - n_gte_t2 / N_TRIALS)
    pctile_t1 = 100 * (1 - n_gte_t1 / N_TRIALS)

    mean3, std3, _, _, _ = stats(mc_tier3)
    mean2, std2, _, _, _ = stats(mc_tier2)
    mean1, std1, _, _, _ = stats(mc_tier1)

    print(f"  1. TOTAL MATCH COUNT (is q=1/phi exceptional at raw counting?)")
    print(f"     Tier 3 (1%):   phi={phi_tier3_n}, random={mean3:.1f}+/-{std3:.1f}, "
          f"percentile={pctile_t3:.1f}%")
    print(f"     Tier 2 (0.1%): phi={phi_tier2_n}, random={mean2:.1f}+/-{std2:.1f}, "
          f"percentile={pctile_t2:.1f}%")
    print(f"     Tier 1 (0.01%):phi={phi_tier1_n}, random={mean1:.1f}+/-{std1:.1f}, "
          f"percentile={pctile_t1:.1f}%")
    print()

    print(f"  2. SIMULTANEOUS CORE FORMULA MATCH (the strongest test)")
    print(f"     Fraction of random nomes matching ALL 3 core formulas within 1%:")
    print(f"     {mc_core_simultaneous}/{N_TRIALS} = {mc_core_simultaneous/N_TRIALS*100:.2f}%")
    print(f"     Within 0.1%: {mc_core_tight}/{N_TRIALS} = "
          f"{mc_core_tight/N_TRIALS*100:.3f}%")
    if mc_core_simultaneous > 0:
        print(f"     => NOT unique to q=1/phi, but {'RARE' if mc_core_simultaneous < N_TRIALS*0.01 else 'not rare'}")
    else:
        print(f"     => UNIQUE to q=1/phi in this sample (p < {1/N_TRIALS})")
    print()

    print(f"  3. THE 56 RELATION")
    print(f"     At q=1/phi: deviation = {ppm56_phi:.1f} ppm")
    n_better = sum(1 for x in mc_56_values if x <= ppm56_phi) if mc_56_values else 0
    print(f"     Random nomes closer to 56: {n_better}/{N_TRIALS} = "
          f"{n_better/N_TRIALS*100:.2f}%")
    print()

    print(f"  4. BEST OVERALL NOME")
    print(f"     At Tier 3: q = {mc_best_tier3_q:.8f} with {mc_best_tier3} matches "
          f"(phi: {phi_tier3_n})")
    print(f"     At Tier 2: q = {mc_best_tier2_q:.8f} with {mc_best_tier2} matches "
          f"(phi: {phi_tier2_n})")
    print()

    print(f"  5. BOTTOM LINE")
    print()
    # Determine verdict
    exceptional_count = 0
    if pctile_t3 > 95:
        exceptional_count += 1
    if pctile_t2 > 95:
        exceptional_count += 1
    if mc_core_simultaneous < N_TRIALS * 0.01:
        exceptional_count += 1
    if n_better < N_TRIALS * 0.05:
        exceptional_count += 1

    if exceptional_count >= 3:
        verdict = "q = 1/phi IS statistically exceptional on multiple measures."
    elif exceptional_count >= 2:
        verdict = ("q = 1/phi shows SOME exceptional properties, but "
                  "the total match count is partly explained by combinatorics.")
    elif exceptional_count >= 1:
        verdict = ("q = 1/phi has ONE exceptional feature (likely simultaneous "
                  "core formulas), but is otherwise unremarkable.")
    else:
        verdict = ("q = 1/phi is NOT statistically exceptional. The match count "
                  "is typical for random nomes given this formula space.")

    print(f"     {verdict}")
    print()
    print(f"     The honest decomposition:")
    print(f"     - phi+integer formulas (q-INDEPENDENT) provide the bulk of matches.")
    print(f"       These would work at ANY nome.")
    print(f"     - The q-DEPENDENT contribution is the simultaneous core formula")
    print(f"       match. This is the framework's real claim.")
    print(f"     - The 56 relation is {'informative' if n_better < N_TRIALS * 0.05 else 'not compelling'} "
          f"(phi at {n_better/N_TRIALS*100:.1f} percentile)")

    total_time = time.time() - t_start
    print(f"\n  Total computation time: {total_time:.1f}s")


if __name__ == "__main__":
    main()
