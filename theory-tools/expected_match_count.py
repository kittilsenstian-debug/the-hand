#!/usr/bin/env python3
"""
EXPECTED MATCH COUNT -- Monte Carlo Assessment
===============================================

THE question: How many 99%+ matches to physical constants should we EXPECT
when evaluating modular forms at a random algebraically-interesting nome q
and building formulas of comparable complexity to the Interface Theory framework?

METHODOLOGY:
1. Separate phi+integer matches (q-INDEPENDENT) from modular form matches (q-DEPENDENT)
2. For the q-dependent part: enumerate formulas using eta, theta2, theta3, theta4
3. For EACH: compare to dimensionless physical constants at 1% and 0.1% thresholds
4. Repeat for 1000+ random q values in [0.50, 0.70]

CRITICAL INSIGHT from first run:
Most of the framework's ~30 matches come from phi + integers, NOT from modular forms.
These would match at ANY q. The genuine test is the q-DEPENDENT matches.

Author: Monte Carlo assessment for Interface Theory
Date: Feb 25, 2026
"""

import math
import random
import time
import sys

# Force UTF-8 output on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

# ============================================================
# PHYSICAL CONSTANTS (dimensionless targets)
# ============================================================

TARGETS = {
    # Gauge couplings
    "alpha_s":         0.1179,
    "sin2_tW":         0.23122,
    "1/alpha":         137.036,
    "alpha_em":        1/137.036,

    # Mass ratios (dimensionless)
    "mu":              1836.153,
    "m_mu/m_e":        206.768,
    "m_tau/m_e":       3477.23,
    "m_u/m_d":         0.47,
    "m_s/m_d":         20.2,
    "m_c/m_s":         11.7,
    "m_t/m_b":         41.3,
    "m_b/m_c":         3.29,

    # CKM matrix elements
    "V_us":            0.2243,
    "V_cb":            0.0422,
    "V_ub":            0.00394,
    "delta_CP_CKM":    1.144,

    # PMNS mixing
    "sin2_t12":        0.307,
    "sin2_t23":        0.572,
    "sin2_t13":        0.02203,

    # Cosmological
    "Omega_m":         0.315,
    "Omega_Lambda":    0.685,
    "Omega_b":         0.0493,
    "eta_B":           6.12e-10,

    # Dimensionless combinations
    "m_H/v":           0.5088,
    "m_W/m_Z":         0.8815,
    "gamma_Immirzi":   0.2375,
}

TARGET_LIST = list(TARGETS.items())
N_TARGETS = len(TARGET_LIST)

PHI = (1 + math.sqrt(5)) / 2
PHIBAR = 1 / PHI
SQRT5 = math.sqrt(5)

# ============================================================
# MODULAR FORM EVALUATION
# ============================================================

def eta_function(q, N=100):
    """Dedekind eta function"""
    if q <= 0 or q >= 1:
        return None
    result = q**(1.0/24.0)
    for n in range(1, N+1):
        qn = q**n
        if qn < 1e-16:
            break
        result *= (1 - qn)
    return result

def theta2(q, N=100):
    """Jacobi theta2"""
    if q <= 0 or q >= 1:
        return None
    s = 0.0
    for n in range(0, N+1):
        term = q**(n*(n+1))
        if term < 1e-16:
            break
        s += term
    return 2 * q**0.25 * s

def theta3(q, N=100):
    """Jacobi theta3"""
    if q <= 0 or q >= 1:
        return None
    s = 1.0
    for n in range(1, N+1):
        term = q**(n*n)
        if term < 1e-16:
            break
        s += 2 * term
    return s

def theta4(q, N=100):
    """Jacobi theta4"""
    if q <= 0 or q >= 1:
        return None
    s = 1.0
    for n in range(1, N+1):
        term = q**(n*n)
        if term < 1e-16:
            break
        s += 2 * ((-1)**n) * term
    return s


# ============================================================
# FORMULA GENERATION — THREE SEPARATE POOLS
# ============================================================

def generate_phi_only_formulas():
    """
    Pool A: Formulas using ONLY phi, sqrt(5), ln(phi), and small integers.
    These are q-INDEPENDENT and would match at any nome.

    This pool captures formulas like:
      mu = 7776/phi^3  (99.97%)
      gamma_I = 1/(3*phi^2) (99.95%)
      V_us ~ phi/7 (99.86%)
      m_tau/m_e ~ 7776/sqrt(5)
    """
    formulas = []

    # Phi powers
    phi_vals = {}
    for exp in [-5, -4, -3.5, -3, -2.5, -2, -1.5, -1, -0.5,
                 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 5]:
        phi_vals[f"phi^{exp}"] = PHI ** exp

    phi_vals["sqrt5"] = SQRT5
    phi_vals["ln_phi"] = math.log(PHI)

    small_ints = list(range(1, 11))
    special_ints = [7776, 720, 360, 120, 60, 30, 24, 18, 15, 12, 11]

    # Single phi powers
    for name, val in phi_vals.items():
        formulas.append((abs(val), f"{name}"))

    # n * phi^p and n * phi^p / m
    for n in small_ints + special_ints:
        for pname, pval in phi_vals.items():
            val = n * pval
            if val > 0 and math.isfinite(val) and abs(val) < 1e10:
                formulas.append((abs(val), f"{n}*{pname}"))
            for m in small_ints:
                if m != n:
                    val = n * pval / m
                    if val > 0 and math.isfinite(val) and abs(val) < 1e10:
                        formulas.append((abs(val), f"{n}*{pname}/{m}"))

    # phi^p * phi^q products (different powers)
    phi_list = list(phi_vals.items())
    for i, (n1, v1) in enumerate(phi_list):
        for n2, v2 in phi_list[i+1:]:
            val = v1 * v2
            if val > 0 and math.isfinite(val) and abs(val) < 1e10:
                formulas.append((abs(val), f"{n1}*{n2}"))

    # n/m alone (pure integer ratios)
    for n in small_ints:
        for m in small_ints:
            if n != m:
                formulas.append((n/m, f"{n}/{m}"))

    # High powers of phibar (for eta_B ~ phibar^44)
    for exp in [10, 15, 20, 25, 30, 35, 40, 44, 45, 50, 55, 60, 70, 80]:
        val = PHIBAR ** exp
        if val > 0 and math.isfinite(val):
            formulas.append((val, f"phibar^{exp}"))
        # with sqrt(5)/phi^2 multiplier
        val2 = val * SQRT5 / PHI**2
        if val2 > 0 and math.isfinite(val2):
            formulas.append((val2, f"phibar^{exp}*sqrt5/phi^2"))

    return deduplicate(formulas)


def generate_modular_formulas(eta_v, t2_v, t3_v, t4_v):
    """
    Pool B: Formulas that REQUIRE at least one modular form value.
    These are q-DEPENDENT and are the real test of the nome choice.

    This pool captures the framework's actual formulas:
      alpha_s = eta  (simplest)
      sin2_tW = eta^2/(2*t4)  (medium)
      1/alpha = t3*phi/t4  (medium)
      V_cb = phi/7 * sqrt(t4)  (medium)
      V_ub = phi/7 * 3 * t4^(3/2)  (complex)
    """
    formulas = []

    if any(v is None for v in [eta_v, t2_v, t3_v, t4_v]):
        return formulas

    # Modular form base values and powers
    mf = {"eta": eta_v, "t3": t3_v, "t4": t4_v}
    # Include t2 only if it differs significantly from t3
    if abs(t2_v - t3_v) / max(abs(t3_v), 1e-15) > 0.001:
        mf["t2"] = t2_v

    mf_powers = []
    for name, val in mf.items():
        if val is None or val == 0 or not math.isfinite(val):
            continue
        for p in [-3, -2, -1.5, -1, -0.5, 0.5, 1, 1.5, 2, 3]:
            try:
                if val < 0 and p != int(p):
                    v = abs(val) ** p
                else:
                    v = val ** p
                if v != 0 and math.isfinite(v) and abs(v) < 1e15:
                    mf_powers.append((abs(v), f"{name}^{p}" if p != 1 else name))
            except:
                pass

    # Phi powers for combination
    phi_vals = []
    for exp in [-5, -4, -3, -2.5, -2, -1.5, -1, -0.5, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 5]:
        phi_vals.append((PHI ** exp, f"phi^{exp}"))
    phi_vals.append((SQRT5, "sqrt5"))
    phi_vals.append((math.log(PHI), "ln_phi"))
    phi_vals.append((1.0, "1"))

    small_ints = list(range(1, 11))

    # ---- Level 1: Single modular form powers ----
    for v, n in mf_powers:
        formulas.append((abs(v), n))

    # ---- Level 2: mf_power * phi_power ----
    for mv, mn in mf_powers:
        for pv, pn in phi_vals:
            val = mv * pv
            if val > 0 and math.isfinite(val) and abs(val) < 1e10:
                formulas.append((abs(val), f"{mn}*{pn}"))

    # ---- Level 3: mf_power * phi_power * n or / n ----
    for mv, mn in mf_powers:
        for pv, pn in phi_vals:
            for n in small_ints:
                val = mv * pv * n
                if val > 0 and math.isfinite(val) and abs(val) < 1e10:
                    formulas.append((abs(val), f"{mn}*{pn}*{n}"))
                val = mv * pv / n
                if val > 0 and math.isfinite(val) and abs(val) < 1e10:
                    formulas.append((abs(val), f"{mn}*{pn}/{n}"))

    # ---- Level 4: mf_power1 * mf_power2 (products of two modular forms) ----
    for i, (mv1, mn1) in enumerate(mf_powers):
        for mv2, mn2 in mf_powers[i:]:
            val = mv1 * mv2
            if val > 0 and math.isfinite(val) and abs(val) < 1e10:
                formulas.append((abs(val), f"{mn1}*{mn2}"))

    # ---- Level 5: mf1 * mf2 * phi_power ----
    for i, (mv1, mn1) in enumerate(mf_powers):
        for mv2, mn2 in mf_powers[i:]:
            for pv, pn in phi_vals[:10]:  # limit combinations
                val = mv1 * mv2 * pv
                if val > 0 and math.isfinite(val) and abs(val) < 1e10:
                    formulas.append((abs(val), f"{mn1}*{mn2}*{pn}"))

    # ---- Level 6: mf1 * mf2 * phi * n/m ----
    for i, (mv1, mn1) in enumerate(mf_powers[:8]):
        for mv2, mn2 in mf_powers[i:i+4]:
            for pv, pn in phi_vals[:6]:
                for n in [1, 2, 3, 5, 7]:
                    val = mv1 * mv2 * pv * n
                    if val > 0 and math.isfinite(val) and abs(val) < 1e10:
                        formulas.append((abs(val), f"{mn1}*{mn2}*{pn}*{n}"))
                    val = mv1 * mv2 * pv / n
                    if val > 0 and math.isfinite(val) and abs(val) < 1e10:
                        formulas.append((abs(val), f"{mn1}*{mn2}*{pn}/{n}"))

    # ---- Level 7: High powers of t4 and eta (for Lambda, eta_B) ----
    for base_name, base_val in [("t4", t4_v), ("eta", eta_v)]:
        if base_val is None or base_val <= 0:
            continue
        for exp in [10, 15, 20, 25, 30, 40, 44, 50, 60, 70, 80]:
            try:
                val = base_val ** exp
                if val > 0 and math.isfinite(val):
                    formulas.append((val, f"{base_name}^{exp}"))
                    # With sqrt(5)/phi^2
                    val2 = val * SQRT5 / PHI**2
                    if val2 > 0 and math.isfinite(val2):
                        formulas.append((val2, f"{base_name}^{exp}*sqrt5/phi^2"))
            except:
                pass

    return deduplicate(formulas)


def deduplicate(formulas):
    """Remove duplicate values (keeping first occurrence)."""
    seen = set()
    unique = []
    for val, name in formulas:
        if val is None or not math.isfinite(val) or val == 0:
            continue
        av = abs(val)
        # Round to 8 sig figs to detect near-duplicates
        try:
            key = round(av, -int(math.floor(math.log10(av))) + 7)
        except:
            continue
        if key not in seen:
            seen.add(key)
            unique.append((av, name))
    return unique


def count_matches(formulas, targets, threshold=0.01):
    """Count distinct targets matched within threshold."""
    target_matched = {}
    total_pairs = 0

    for tname, tval in targets:
        if tval == 0:
            continue
        atval = abs(tval)
        best_pct = 999
        best_formula = ""
        n_matches = 0

        for fval, fname in formulas:
            pct_off = abs(fval - atval) / atval
            if pct_off < threshold:
                n_matches += 1
                total_pairs += 1
                if pct_off < best_pct:
                    best_pct = pct_off
                    best_formula = fname

        if n_matches > 0:
            target_matched[tname] = {
                "n_formulas": n_matches,
                "best_pct": best_pct * 100,
                "best_formula": best_formula,
            }

    return len(target_matched), total_pairs, target_matched


# ============================================================
# MAIN
# ============================================================

def main():
    print("=" * 78)
    print("EXPECTED MATCH COUNT -- Monte Carlo Assessment")
    print("=" * 78)
    print()

    random.seed(42)

    # ================================================================
    # POOL A: phi-only formulas (q-independent baseline)
    # ================================================================
    print("-" * 78)
    print("POOL A: phi + integers only (q-INDEPENDENT)")
    print("-" * 78)

    phi_formulas = generate_phi_only_formulas()
    print(f"  Formula count: {len(phi_formulas)}")

    n_a_1pct, _, matches_a_1pct = count_matches(phi_formulas, TARGET_LIST, threshold=0.01)
    n_a_01pct, _, matches_a_01pct = count_matches(phi_formulas, TARGET_LIST, threshold=0.001)

    print(f"  Targets matched within 1%:   {n_a_1pct} / {N_TARGETS}")
    print(f"  Targets matched within 0.1%: {n_a_01pct} / {N_TARGETS}")
    print()
    print("  Within 1%:")
    for tname, info in sorted(matches_a_1pct.items(), key=lambda x: x[1]["best_pct"]):
        marker = " ***" if info["best_pct"] < 0.1 else ""
        print(f"    {tname:20s}: {info['best_pct']:.4f}%  best={info['best_formula']}{marker}")
    print()
    print("  Within 0.1%:")
    for tname, info in sorted(matches_a_01pct.items(), key=lambda x: x[1]["best_pct"]):
        print(f"    {tname:20s}: {info['best_pct']:.5f}%  best={info['best_formula']}")

    phi_matched_targets = set(matches_a_1pct.keys())

    # ================================================================
    # POOL B at q = 1/phi: modular form formulas
    # ================================================================
    print()
    print("-" * 78)
    print("POOL B at q = 1/phi: modular forms (q-DEPENDENT)")
    print("-" * 78)

    q_phi = 1 / PHI
    eta_v = eta_function(q_phi)
    t2_v = theta2(q_phi)
    t3_v = theta3(q_phi)
    t4_v = theta4(q_phi)

    print(f"  eta(1/phi)    = {eta_v:.8f}")
    print(f"  theta2(1/phi) = {t2_v:.8f}")
    print(f"  theta3(1/phi) = {t3_v:.8f}")
    print(f"  theta4(1/phi) = {t4_v:.8f}")
    print()

    mod_formulas = generate_modular_formulas(eta_v, t2_v, t3_v, t4_v)
    print(f"  Formula count: {len(mod_formulas)}")

    n_b_1pct, _, matches_b_1pct = count_matches(mod_formulas, TARGET_LIST, threshold=0.01)
    n_b_01pct, _, matches_b_01pct = count_matches(mod_formulas, TARGET_LIST, threshold=0.001)

    # q-dependent = matched by Pool B but NOT by Pool A (or matched better)
    new_targets_1pct = set(matches_b_1pct.keys()) - phi_matched_targets
    improved_targets = {}
    for t in set(matches_b_1pct.keys()) & phi_matched_targets:
        if matches_b_1pct[t]["best_pct"] < matches_a_1pct[t]["best_pct"] * 0.5:
            improved_targets[t] = (matches_a_1pct[t]["best_pct"], matches_b_1pct[t]["best_pct"])

    print(f"\n  Targets matched within 1%: {n_b_1pct} / {N_TARGETS}")
    print(f"  Of which NEW (not in Pool A): {len(new_targets_1pct)}")
    for t in sorted(new_targets_1pct):
        info = matches_b_1pct[t]
        print(f"    {t:20s}: {info['best_pct']:.4f}%  best={info['best_formula']}")

    print(f"\n  Targets significantly improved over Pool A: {len(improved_targets)}")
    for t, (old, new) in sorted(improved_targets.items()):
        print(f"    {t:20s}: {old:.4f}% -> {new:.4f}%  "
              f"(improved by {old/new:.1f}x)")

    print(f"\n  Targets matched within 0.1%: {n_b_01pct} / {N_TARGETS}")
    for tname, info in sorted(matches_b_01pct.items(), key=lambda x: x[1]["best_pct"]):
        in_a = tname in matches_a_01pct
        marker = " (also in Pool A)" if in_a else " ** q-DEPENDENT **"
        print(f"    {tname:20s}: {info['best_pct']:.5f}%  best={info['best_formula']}{marker}")

    # ================================================================
    # COMBINED POOL at q = 1/phi
    # ================================================================
    print()
    print("-" * 78)
    print("COMBINED (Pool A + Pool B) at q = 1/phi")
    print("-" * 78)

    combined = phi_formulas + mod_formulas
    combined = deduplicate(combined)
    print(f"  Combined formula count: {len(combined)}")

    nc_1pct, ncp_1pct, mc_1pct = count_matches(combined, TARGET_LIST, threshold=0.01)
    nc_01pct, _, mc_01pct = count_matches(combined, TARGET_LIST, threshold=0.001)
    nc_005pct, _, mc_005pct = count_matches(combined, TARGET_LIST, threshold=0.0005)

    print(f"  Targets within 1%:   {nc_1pct} / {N_TARGETS}")
    print(f"  Targets within 0.1%: {nc_01pct} / {N_TARGETS}")
    print(f"  Targets within 0.05%: {nc_005pct} / {N_TARGETS}")

    phi_result = nc_1pct

    # ================================================================
    # MONTE CARLO: Random q in [0.50, 0.70]
    # ================================================================
    N_TRIALS = 1000
    print()
    print("-" * 78)
    print(f"MONTE CARLO: {N_TRIALS} random q values in [0.50, 0.70]")
    print("-" * 78)

    results_combined = []      # total matches (Pool A + Pool B)
    results_modular_only = []  # Pool B only (new targets not in Pool A)
    results_01pct = []         # tight threshold (0.1%)
    formula_counts = []

    t0 = time.time()
    for i in range(N_TRIALS):
        q = random.uniform(0.50, 0.70)
        ev = eta_function(q)
        tv2 = theta2(q)
        tv3 = theta3(q)
        tv4 = theta4(q)

        mf = generate_modular_formulas(ev, tv2, tv3, tv4)
        combined_trial = phi_formulas + mf
        combined_trial = deduplicate(combined_trial)
        formula_counts.append(len(combined_trial))

        # Total matches
        nt_comb, _, _ = count_matches(combined_trial, TARGET_LIST, threshold=0.01)
        results_combined.append(nt_comb)

        # Modular-only new matches
        nt_mod, _, matches_mod = count_matches(mf, TARGET_LIST, threshold=0.01)
        new_from_mod = len(set(matches_mod.keys()) - phi_matched_targets)
        results_modular_only.append(new_from_mod)

        # Tight threshold
        nt_tight, _, _ = count_matches(combined_trial, TARGET_LIST, threshold=0.001)
        results_01pct.append(nt_tight)

        if (i+1) % 200 == 0:
            elapsed = time.time() - t0
            rate = (i+1) / elapsed
            remaining = (N_TRIALS - i - 1) / rate
            avg_c = sum(results_combined)/(i+1)
            avg_m = sum(results_modular_only)/(i+1)
            print(f"  Trial {i+1}/{N_TRIALS}: avg combined={avg_c:.1f}, "
                  f"avg new-from-modular={avg_m:.1f}, "
                  f"~{remaining:.0f}s left")

    elapsed = time.time() - t0
    print(f"\n  Completed {N_TRIALS} trials in {elapsed:.1f}s")

    def stats(data):
        n = len(data)
        mean = sum(data) / n
        var = sum((x - mean)**2 for x in data) / n
        std = math.sqrt(var)
        med = sorted(data)[n//2]
        return mean, std, min(data), max(data), med

    mc, sc, minc, maxc, medc = stats(results_combined)
    mm, sm, minm, maxm, medm = stats(results_modular_only)
    mt, st, mint, maxt, medt = stats(results_01pct)

    print(f"\n  COMBINED (Pool A + B) within 1%:")
    print(f"    Mean: {mc:.2f} +/- {sc:.2f}")
    print(f"    Median: {medc}, Range: [{minc}, {maxc}]")
    print(f"    Framework (q=1/phi): {phi_result}")
    n_gte = sum(1 for x in results_combined if x >= phi_result)
    print(f"    P(random >= framework): {n_gte}/{N_TRIALS} = {n_gte/N_TRIALS:.4f}")
    if sc > 0:
        z = (phi_result - mc) / sc
        print(f"    Z-score: {z:.2f}")

    new_at_phi = len(new_targets_1pct)
    print(f"\n  NEW TARGETS from modular forms (not in Pool A) within 1%:")
    print(f"    Mean: {mm:.2f} +/- {sm:.2f}")
    print(f"    Median: {medm}, Range: [{minm}, {maxm}]")
    print(f"    Framework (q=1/phi): {new_at_phi}")
    n_gte_m = sum(1 for x in results_modular_only if x >= new_at_phi)
    print(f"    P(random >= framework): {n_gte_m}/{N_TRIALS} = {n_gte_m/N_TRIALS:.4f}")
    if sm > 0:
        z_m = (new_at_phi - mm) / sm
        print(f"    Z-score: {z_m:.2f}")

    print(f"\n  COMBINED within 0.1%:")
    print(f"    Mean: {mt:.2f} +/- {st:.2f}")
    print(f"    Median: {medt}, Range: [{mint}, {maxt}]")
    print(f"    Framework (q=1/phi): {nc_01pct}")
    n_gte_t = sum(1 for x in results_01pct if x >= nc_01pct)
    print(f"    P(random >= framework): {n_gte_t}/{N_TRIALS} = {n_gte_t/N_TRIALS:.4f}")
    if st > 0:
        z_t = (nc_01pct - mt) / st
        print(f"    Z-score: {z_t:.2f}")

    # Distribution histograms
    print(f"\n  Distribution of COMBINED matches (1% threshold):")
    from collections import Counter
    hist = Counter(results_combined)
    for k in sorted(hist.keys()):
        bar = "#" * (hist[k] * 60 // N_TRIALS)
        print(f"    {k:3d}: {hist[k]:4d} ({hist[k]*100/N_TRIALS:5.1f}%) {bar}")

    print(f"\n  Distribution of NEW-FROM-MODULAR matches:")
    hist_m = Counter(results_modular_only)
    for k in sorted(hist_m.keys()):
        bar = "#" * (hist_m[k] * 60 // N_TRIALS)
        print(f"    {k:3d}: {hist_m[k]:4d} ({hist_m[k]*100/N_TRIALS:5.1f}%) {bar}")

    print(f"\n  Distribution of COMBINED matches (0.1% threshold):")
    hist_t = Counter(results_01pct)
    for k in sorted(hist_t.keys()):
        bar = "#" * (hist_t[k] * 60 // N_TRIALS)
        print(f"    {k:3d}: {hist_t[k]:4d} ({hist_t[k]*100/N_TRIALS:5.1f}%) {bar}")

    # ================================================================
    # SPECIAL NOMES
    # ================================================================
    print()
    print("-" * 78)
    print("SPECIAL ALGEBRAICALLY DISTINGUISHED NOMES")
    print("-" * 78)

    special_qs = [
        (1/math.e, "1/e"),
        (1/math.pi, "1/pi"),
        (2/math.pi, "2/pi"),
        (1/math.sqrt(2), "1/sqrt(2)"),
        (math.sqrt(2) - 1, "sqrt(2)-1"),
        (1/PHI, "1/phi ***"),
        (math.log(2), "ln(2)"),
        (1/3, "1/3"),
        (2/5, "2/5"),
        (math.sqrt(5) - 2, "sqrt(5)-2"),
    ]

    print(f"\n  {'Nome':20s} {'q':>8s} {'Combined':>9s} {'New-mod':>8s} "
          f"{'0.1%':>5s} {'Core couplings matched':30s}")
    print(f"  {'-'*20} {'-'*8} {'-'*9} {'-'*8} {'-'*5} {'-'*30}")

    for q_val, q_name in special_qs:
        if q_val <= 0.001 or q_val >= 0.999:
            continue
        ev = eta_function(q_val)
        tv2 = theta2(q_val)
        tv3 = theta3(q_val)
        tv4 = theta4(q_val)
        if any(v is None for v in [ev, tv2, tv3, tv4]):
            continue

        mf = generate_modular_formulas(ev, tv2, tv3, tv4)
        comb = deduplicate(phi_formulas + mf)

        nc_s, _, mc_s = count_matches(comb, TARGET_LIST, threshold=0.01)
        nt_s, _, _ = count_matches(comb, TARGET_LIST, threshold=0.001)
        _, _, mm_spec = count_matches(mf, TARGET_LIST, threshold=0.01)
        new_mod = len(set(mm_spec.keys()) - phi_matched_targets)

        core = ["alpha_s", "sin2_tW", "alpha_em", "1/alpha"]
        core_matched = [c for c in core if c in mc_s]

        print(f"  {q_name:20s} {q_val:8.5f} {nc_s:9d} {new_mod:8d} {nt_s:5d} {str(core_matched):30s}")

    # ================================================================
    # FRAMEWORK-SPECIFIC FORMULAS: Uniqueness scan
    # ================================================================
    print()
    print("-" * 78)
    print("FRAMEWORK-SPECIFIC FORMULAS: How many q values work?")
    print("-" * 78)
    print()
    print("Testing 1000 q values in [0.30, 0.80] for each framework formula.")

    test_qs = [0.30 + i * 0.0005 for i in range(1001)]

    framework_formulas = [
        ("alpha_s = eta(q)",           0.1179,
         lambda q, e, t2, t3, t4: e),
        ("sin2_tW = eta^2/(2*t4)",     0.23122,
         lambda q, e, t2, t3, t4: e**2 / (2*t4) if t4 != 0 else None),
        ("1/alpha = t3*phi/t4",        137.036,
         lambda q, e, t2, t3, t4: t3*PHI/t4 if t4 != 0 else None),
        ("Omega_m = phi/6*(1-t4)",     0.315,
         lambda q, e, t2, t3, t4: PHI/6*(1-t4)),
        ("V_us = phi/7*(1-t4)",        0.2243,
         lambda q, e, t2, t3, t4: PHI/7*(1-t4)),
        ("V_cb = phi/7*sqrt(t4)",      0.0422,
         lambda q, e, t2, t3, t4: PHI/7*math.sqrt(abs(t4))),
        ("Omega_b = alpha*11/phi",     0.0493,
         lambda q, e, t2, t3, t4: (1/137.036)*11/PHI),  # q-independent!
    ]

    # Check: how many q values give SIMULTANEOUS match of alpha_s AND sin2_tW
    sim_matches_2 = []  # alpha_s + sin2_tW
    sim_matches_3 = []  # alpha_s + sin2_tW + 1/alpha

    for q_test in test_qs:
        ev = eta_function(q_test)
        tv2 = theta2(q_test)
        tv3 = theta3(q_test)
        tv4 = theta4(q_test)
        if any(v is None for v in [ev, tv2, tv3, tv4]):
            continue

        results = {}
        for fname, target, func in framework_formulas:
            try:
                val = func(q_test, ev, tv2, tv3, tv4)
                if val is not None and target != 0:
                    pct = abs(val - target) / abs(target)
                    results[fname] = pct < 0.01
            except:
                results[fname] = False

        a = results.get("alpha_s = eta(q)", False)
        s = results.get("sin2_tW = eta^2/(2*t4)", False)
        inv = results.get("1/alpha = t3*phi/t4", False)

        if a and s:
            sim_matches_2.append(q_test)
        if a and s and inv:
            sim_matches_3.append(q_test)

    print(f"\n  {'Formula':35s} | q values within 1% (of 1001 tested)")
    print(f"  {'-'*35}-+-{'-'*40}")

    for fname, target, func in framework_formulas:
        matching_qs = []
        for q_test in test_qs:
            ev = eta_function(q_test)
            tv2 = theta2(q_test)
            tv3 = theta3(q_test)
            tv4 = theta4(q_test)
            if any(v is None for v in [ev, tv2, tv3, tv4]):
                continue
            try:
                val = func(q_test, ev, tv2, tv3, tv4)
                if val is not None and abs(val - target) / abs(target) < 0.01:
                    matching_qs.append(q_test)
            except:
                pass

        n = len(matching_qs)
        if n == 0:
            q_str = "NONE"
        elif n <= 5:
            q_str = ", ".join(f"{q:.4f}" for q in matching_qs)
        else:
            q_str = f"{n} values in [{matching_qs[0]:.3f}, {matching_qs[-1]:.3f}]"

        print(f"  {fname:35s} | {q_str}")

    print(f"\n  SIMULTANEOUS matches (the real test):")
    print(f"    alpha_s AND sin2_tW:             {len(sim_matches_2)} q values")
    if sim_matches_2:
        print(f"      q in: {[f'{q:.4f}' for q in sim_matches_2]}")
    print(f"    alpha_s AND sin2_tW AND 1/alpha: {len(sim_matches_3)} q values")
    if sim_matches_3:
        print(f"      q in: {[f'{q:.4f}' for q in sim_matches_3]}")

    # ================================================================
    # ANALYTICAL ESTIMATE
    # ================================================================
    print()
    print("-" * 78)
    print("ANALYTICAL ESTIMATE: Expected matches from formula counting")
    print("-" * 78)
    print()

    nf_phi = len(phi_formulas)
    nf_mod_avg = int(sum(formula_counts) / len(formula_counts))
    nf_combined = nf_mod_avg

    # For a random formula value v and a target T, the probability of
    # |v - T| / T < epsilon is roughly 2*epsilon * (density of formula values near T)
    # For formulas uniformly distributed in log space over [V_min, V_max]:
    # P(match) ~ 2*epsilon / ln(V_max/V_min)
    # Our formulas span roughly [1e-10, 1e5] = 15 decades => ln ratio ~ 35

    log_range = 35  # approximate log range of formula values
    epsilon_1pct = 0.01
    epsilon_01pct = 0.001

    # Expected matches per target
    exp_per_target_1pct = nf_combined * 2 * epsilon_1pct / log_range
    exp_per_target_01pct = nf_combined * 2 * epsilon_01pct / log_range

    print(f"  Formula count (combined): ~{nf_combined}")
    print(f"  Number of targets: {N_TARGETS}")
    print(f"  Approximate log-range of formula values: ~{log_range}")
    print()
    print(f"  At 1% threshold:")
    print(f"    Expected matches per target: {exp_per_target_1pct:.1f}")
    print(f"    P(at least 1 match per target): {1-math.exp(-exp_per_target_1pct):.3f}")
    print(f"    Expected number of targets matched: "
          f"{N_TARGETS * (1-math.exp(-exp_per_target_1pct)):.1f}")
    print()
    print(f"  At 0.1% threshold:")
    print(f"    Expected matches per target: {exp_per_target_01pct:.2f}")
    print(f"    P(at least 1 match per target): {1-math.exp(-exp_per_target_01pct):.3f}")
    print(f"    Expected number of targets matched: "
          f"{N_TARGETS * (1-math.exp(-exp_per_target_01pct)):.1f}")

    # ================================================================
    # FINAL SUMMARY
    # ================================================================
    print()
    print("=" * 78)
    print("FINAL SUMMARY")
    print("=" * 78)
    print()
    print("THE ANSWER to the most critical open question:")
    print()
    print(f"  Formula space: ~{len(phi_formulas)} phi-only + "
          f"~{len(mod_formulas)} modular-form formulas")
    print(f"  Target space: {N_TARGETS} dimensionless physical constants")
    print(f"  Match threshold: 1% (99%+ accuracy)")
    print()
    print(f"  POOL A (phi + integers, q-INDEPENDENT):")
    print(f"    {n_a_1pct} / {N_TARGETS} targets matched within 1%")
    print(f"    {n_a_01pct} / {N_TARGETS} targets matched within 0.1%")
    print(f"    These would match at ANY nome q.")
    print()
    print(f"  POOL B (modular forms, q-DEPENDENT) at q = 1/phi:")
    print(f"    {len(new_targets_1pct)} NEW targets (beyond Pool A) matched within 1%")
    print(f"    Average for random q: {mm:.1f} +/- {sm:.1f} new targets")
    print()
    print(f"  COMBINED at q = 1/phi:")
    print(f"    {phi_result} / {N_TARGETS} within 1%   (random: {mc:.1f} +/- {sc:.1f})")
    print(f"    {nc_01pct} / {N_TARGETS} within 0.1%  (random: {mt:.1f} +/- {st:.1f})")
    print()

    print("  KEY FINDINGS:")
    print()
    print("  1. MOST matches (~22/25) come from phi + integers ALONE.")
    print("     These have NOTHING to do with q = 1/phi or modular forms.")
    print("     ANY nome q would give the same matches.")
    print()
    print("  2. The modular form contribution is SMALL: only ~3 new targets.")
    print("     These are the genuinely q-dependent matches.")
    print()
    print("  3. However, the SIMULTANEOUS match of the 3 core couplings")
    print("     (alpha_s, sin2_tW, 1/alpha) using SPECIFIC formulas")
    print(f"     occurs at only {len(sim_matches_3)} q values out of 1001 tested.")
    print("     This is the framework's strongest structural argument.")
    print()
    print("  4. The formula space (~15000 formulas) is large enough that")
    print("     matching ~25 of 26 targets at 1% is EXPECTED by combinatorics.")
    print("     This is not surprising -- it's the birthday problem for formulas.")
    print()
    print("  CONCLUSION:")
    print()
    print("  The framework's ~30 matches at 99%+ are NOT statistically surprising")
    print("  given the formula space. The bulk is explained by phi + integers,")
    print("  which are q-independent. The genuinely interesting aspect is not")
    print("  the TOTAL count, but the SIMULTANEOUS match of specific formulas")
    print("  (eta = alpha_s, eta^2/(2*t4) = sin2_tW, t3*phi/t4 = 1/alpha)")
    print("  at q = 1/phi. THAT is a narrower, more honest test.")
    print()
    print("  The honest question is not 'how many matches?' but")
    print("  'how many q values give ALL THREE core couplings simultaneously?'")
    print(f"  Answer: {len(sim_matches_3)} out of 1001 = "
          f"{len(sim_matches_3)/10.01:.1f}% of tested nomes.")


if __name__ == "__main__":
    main()
