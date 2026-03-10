# -*- coding: utf-8 -*-
"""
null_model_framework.py
=======================
Null-model test: compare the Interface Theory (q = 1/phi) against 4 alternative
algebraically-interesting nomes using the SAME formula complexity budget.

If q = 1/phi is genuinely special, it should match significantly more SM constants
than alternatives at the same formula complexity.

Nomes tested:
  q1 = 1/e    = 0.3679  (V = e)
  q2 = 1/pi   = 0.3183  (V = pi)
  q3 = 1/sqrt2= 0.7071  (V = sqrt(2))
  q4 = 2/3    = 0.6667  (V = 3/2)
  q5 = 1/phi  = 0.6180  (V = phi)   <-- real framework

SM targets (15):
  alpha_s, sin2_W, 1/alpha, mu, mt/me, sin2_12, sin2_23, sin2_13,
  |Vus|, |Vcb|, |Vub|, eta_B, Omega_m/Omega_L, mb/mc, mtau/mmu
"""

import mpmath
from mpmath import mp, mpf, sqrt, log, pi, exp, power, fabs
import math
import time

# Set precision to 50 decimal digits
mp.dps = 50


# ==============================================================================
# Modular forms
# ==============================================================================

def eta_func(q):
    """Dedekind eta: q^(1/24) * prod_{n>=1} (1-q^n)"""
    q = mpf(q)
    result = power(q, mpf(1)/24)
    n = 1
    while True:
        qn = power(q, n)
        if abs(qn) < mpf(10)**(-47):
            break
        result *= (1 - qn)
        n += 1
    return result


def theta2_func(q):
    """theta_2(q) = 2*sum_{n>=0} q^((n+1/2)^2)"""
    q = mpf(q)
    result = mpf(0)
    for n in range(200):
        exp_val = (n + mpf(1)/2)**2
        term = power(q, exp_val)
        if abs(term) < mpf(10)**(-47):
            break
        result += term
    return 2 * result


def theta3_func(q):
    """theta_3(q) = 1 + 2*sum_{n>=1} q^(n^2)"""
    q = mpf(q)
    result = mpf(1)
    for n in range(1, 200):
        term = power(q, n*n)
        if abs(term) < mpf(10)**(-47):
            break
        result += 2 * term
    return result


def theta4_func(q):
    """theta_4(q) = 1 + 2*sum_{n>=1} (-1)^n * q^(n^2)"""
    q = mpf(q)
    result = mpf(1)
    for n in range(1, 200):
        term = power(q, n*n)
        if abs(term) < mpf(10)**(-47):
            break
        result += 2 * ((-1)**n) * term
    return result


# ==============================================================================
# SM targets (15 quantities)
# ==============================================================================

TARGETS = [
    ("alpha_s",   0.1179,    "Strong coupling"),
    ("sin2_W",    0.23122,   "Weak mixing angle"),
    ("inv_alpha", 137.036,   "1/alpha_em"),
    ("mu",        1836.153,  "Proton/electron mass ratio"),
    ("mt_me",     338102.0,  "Top/electron mass ratio"),
    ("sin2_12",   0.307,     "Solar PMNS"),
    ("sin2_23",   0.546,     "Atm PMNS"),
    ("sin2_13",   0.02200,   "Reactor PMNS"),
    ("Vus",       0.2243,    "CKM |Vus|"),
    ("Vcb",       0.04080,   "CKM |Vcb|"),
    ("Vub",       0.003940,  "CKM |Vub|"),
    ("eta_B",     6.1e-10,   "Baryon asymmetry"),
    ("Om_ratio",  0.4450,    "Omega_m / Omega_Lambda"),
    ("mb_mc",     3.380,     "m_b / m_c"),
    ("mtau_mmu",  16.82,     "m_tau / m_mu"),
]


# ==============================================================================
# Nome definitions
# ==============================================================================

PHI = (1 + math.sqrt(5)) / 2

NOMES = [
    ("q=1/e",     1/math.e,         math.e),
    ("q=1/pi",    1/math.pi,        math.pi),
    ("q=1/sqrt2", 1/math.sqrt(2),   math.sqrt(2)),
    ("q=2/3",     2/3,              3/2),
    ("q=1/phi",   1/PHI,            PHI),   # real framework
]


# ==============================================================================
# Formula generator
# ==============================================================================

def generate_formulas(eta_v, t2, t3, t4, V_mp, q_mp):
    """
    Generate formulas from the given modular-form values and scalar V.
    Uses the SAME templates for every nome (fair comparison).
    Returns list of (float_value, formula_string, mpf_value).
    """
    formulas = []

    def add(val, name):
        try:
            fv = float(val)
            if fv > 0 and not math.isnan(fv) and not math.isinf(fv):
                formulas.append((fv, name, val))
        except Exception:
            pass

    # -- Level 0: raw modular values -------------------------------------------
    add(eta_v,   "eta")
    add(t2,      "theta2")
    add(t3,      "theta3")
    add(t4,      "theta4")
    add(V_mp,    "V")
    add(1/V_mp,  "1/V")

    # -- Level 1a: powers of V -------------------------------------------------
    for n in range(-8, 9):
        if n != 0:
            add(power(V_mp, n), "V^%d" % n)

    # -- Level 1b: powers of q -------------------------------------------------
    for n in range(-5, 6):
        if n != 0:
            add(power(q_mp, n), "q^%d" % n)

    # -- Level 1c: integer / V combos ------------------------------------------
    for N in range(1, 20):
        for b in range(1, 6):
            add(mpf(N)**b,          "%d^%d" % (N, b))
            add(mpf(N)**b / V_mp,   "%d^%d/V" % (N, b))
            add(V_mp / mpf(N),      "V/%d" % N)
            add(mpf(N) / V_mp**b,   "%d/V^%d" % (N, b))

    # -- Level 2a: eta^a * theta4^b --------------------------------------------
    for a in [-2, -1, 1, 2, 3]:
        for b in [-2, -1, 1, 2, 3]:
            try:
                val = (eta_v**a) * (t4**b)
                add(val, "eta^%d*t4^%d" % (a, b))
            except Exception:
                pass

    # -- Level 2b: eta^a * V^b -------------------------------------------------
    for a in [-3, -2, -1, 1, 2, 3]:
        for b in [-4, -3, -2, -1, 1, 2, 3, 4]:
            try:
                add((eta_v**a) * (V_mp**b), "eta^%d*V^%d" % (a, b))
            except Exception:
                pass

    # -- Level 2c: theta3^a / theta4^b -----------------------------------------
    for a in [1, 2, 3]:
        for b in [1, 2, 3]:
            add(t3**a / t4**b, "t3^%d/t4^%d" % (a, b))

    # -- Level 2d: theta3*V/theta4 family --------------------------------------
    for a in [1, 2]:
        for b in [-3, -2, -1, 1, 2, 3]:
            for c in [1, 2, 3]:
                add(t3**a * V_mp**b / t4**c, "t3^%d*V^%d/t4^%d" % (a, b, c))

    # -- Level 2e: theta4^a * V^b / c ------------------------------------------
    for a in range(1, 6):
        for b in range(-3, 4):
            for c in range(1, 12):
                add(t4**a * V_mp**b / mpf(c), "t4^%d*V^%d/%d" % (a, b, c))

    # -- Level 2f: N^a / V^b ---------------------------------------------------
    for N in range(2, 9):
        for a in range(1, 7):
            for b in range(1, 6):
                add(mpf(N)**a / V_mp**b, "%d^%d/V^%d" % (N, a, b))

    # -- Level 2g: eta * integer ratios ----------------------------------------
    for N in range(1, 15):
        for D in range(1, 15):
            add(eta_v * mpf(N) / mpf(D),    "eta*%d/%d" % (N, D))
            add(eta_v**2 * mpf(N) / mpf(D), "eta2*%d/%d" % (N, D))

    # -- Level 2h: theta2 combos -----------------------------------------------
    for a in [1, 2]:
        for b in [1, 2]:
            add(t2**a / t4**b,      "t2^%d/t4^%d" % (a, b))
            add(t2**a * V_mp / t4**b, "t2^%d*V/t4^%d" % (a, b))

    # -- Level 3a: eta^a * theta3^b * theta4^c * V^d ---------------------------
    for a in [-1, 0, 1, 2]:
        for b in [0, 1, 2]:
            for c in [-2, -1, 0, 1, 2]:
                for d in [-2, -1, 0, 1, 2]:
                    if a == 0 and b == 0 and c == 0 and d == 0:
                        continue
                    try:
                        val = (eta_v**a if a != 0 else mpf(1)) * \
                              (t3**b  if b != 0 else mpf(1)) * \
                              (t4**c  if c != 0 else mpf(1)) * \
                              (V_mp**d if d != 0 else mpf(1))
                        add(val, "e%d_t3%d_t4%d_V%d" % (a, b, c, d))
                    except Exception:
                        pass

    # -- Level 3b: 1/N +/- theta4 * sqrt(a/b) ---------------------------------
    for N in range(2, 9):
        for a in range(1, 6):
            for b in range(1, 6):
                try:
                    sq = sqrt(mpf(a)/mpf(b))
                    add(mpf(1)/N + t4*sq,   "1/%d+t4*s(%d/%d)" % (N, a, b))
                    add(mpf(1)/N - t4*sq,   "1/%d-t4*s(%d/%d)" % (N, a, b))
                    add(mpf(1)/N + t4**2*sq,"1/%d+t4^2*s(%d/%d)" % (N, a, b))
                except Exception:
                    pass

    # -- Level 3c: N^a / V^b + c/(d*V^e) --------------------------------------
    for N in range(2, 8):
        for a in range(1, 5):
            for b in range(1, 4):
                for c in range(1, 8):
                    for d in range(1, 8):
                        for e in range(1, 4):
                            try:
                                val = mpf(N)**a / V_mp**b + mpf(c)/(mpf(d) * V_mp**e)
                                add(val, "%d^%d/V^%d+%d/(%dV^%d)" % (N, a, b, c, d, e))
                            except Exception:
                                pass

    # -- Level 3d: theta4^n * sqrt(5) / V^2 (cosmological-constant-like) ------
    sqrt5 = sqrt(mpf(5))
    for n in range(1, 20):
        add(t4**n * sqrt5 / V_mp**2, "t4^%d*s5/V^2" % n)
    for n in [60, 70, 80, 90, 100]:
        try:
            add(t4**n * sqrt5 / V_mp**2, "t4^%d*s5/V^2" % n)
            add(t4**n, "t4^%d" % n)
        except Exception:
            pass

    # -- Level 3e: eta^2/(2*theta4) family (framework sin2_W formula) ----------
    add(eta_v**2 / (2*t4),        "eta^2/(2*t4)")
    add(eta_v**2 / (2*t4) * V_mp, "eta^2/(2*t4)*V")
    add(eta_v**2 / t4,            "eta^2/t4")
    add(eta_v**4 / t4**2,         "eta^4/t4^2")

    # -- Level 3f: log correction for 1/alpha ----------------------------------
    log_terms = [
        ("logV",   log(V_mp)),
        ("log1/V", -log(V_mp)),
        ("log2",   log(mpf(2))),
        ("log3",   log(mpf(3))),
    ]
    for ln_name, ln_val in log_terms:
        for c_num in range(1, 6):
            for c_den in range(1, 6):
                coeff = mpf(c_num) / (mpf(c_den) * pi)
                add(t3*V_mp/t4 + coeff*ln_val, "t3V/t4+%d/%dpi*%s" % (c_num, c_den, ln_name))

    # -- Level 4a: mu formula N^5/V^3 + M/(K*V^2) ----------------------------
    for N in [4, 5, 6, 7, 8]:
        for M in range(1, 15):
            for K in range(1, 15):
                try:
                    add(mpf(N)**5 / V_mp**3 + mpf(M)/(mpf(K)*V_mp**2),
                        "%d^5/V^3+%d/(%dV^2)" % (N, M, K))
                except Exception:
                    pass

    # -- Level 4b: higher powers of theta4 (CKM-like) -------------------------
    for a in range(1, 10):
        add(t4**a,         "t4^%d" % a)
        add(t4**a * V_mp,  "t4^%d*V" % a)
        add(t4**a / V_mp,  "t4^%d/V" % a)

    # -- Level 4c: power-law suppressions (fermion masses) --------------------
    for n in range(5, 40):
        add(power(V_mp, -n),        "V^-%d" % n)
        add(power(V_mp, -n)*10,     "10*V^-%d" % n)
        add(power(V_mp, -n)*100,    "100*V^-%d" % n)
        add(power(V_mp, -n)*1000,   "1000*V^-%d" % n)

    for n in range(1, 12):
        add(exp(-mpf(n)/V_mp),       "exp(-%d/V)" % n)
        add(exp(mpf(n)*log(V_mp)),   "exp(%d*logV)" % n)

    # -- Level 4d: mixed theta3, theta4, integer for PMNS ---------------------
    for c in range(1, 5):
        for d in [2, 3, 4, 6, 8]:
            try:
                add(mpf(1)/c + t4 * sqrt(mpf(d)/4), "1/%d+t4*s%d/2" % (c, d))
                add(mpf(1)/c - t4 * sqrt(mpf(d)/4), "1/%d-t4*s%d/2" % (c, d))
            except Exception:
                pass

    return formulas


# ==============================================================================
# Matching engine
# ==============================================================================

def find_best_matches(formulas, targets):
    """
    For each target, find the formula with the lowest % error.
    Returns dict: target_name -> (best_pct_error, best_formula_name, best_float_val)
    """
    results = {}
    for name, target_val, _ in targets:
        tv = float(target_val)
        best_err  = float('inf')
        best_name = "none"
        best_fval = None
        for fval, fname, fmp in formulas:
            if fval <= 0:
                continue
            err = abs(fval - tv) / tv * 100.0
            if err < best_err:
                best_err  = err
                best_name = fname
                best_fval = fval
        results[name] = (best_err, best_name, best_fval)
    return results


# ==============================================================================
# Main loop
# ==============================================================================

def run_all():
    print("=" * 78)
    print("NULL MODEL FRAMEWORK  --  Comparing Interface Theory vs Alternative Nomes")
    print("=" * 78)
    print("Precision: %d decimal digits (mpmath)" % mp.dps)
    print("Targets:   %d SM constants" % len(TARGETS))
    print()

    all_results = {}

    for nome_label, q_val, V_val in NOMES:
        t_start = time.time()
        q_mp = mpf(q_val)
        V_mp = mpf(V_val)

        print()
        print("-" * 60)
        print("Computing: %s  (q = %.6f, V = %.6f)" % (nome_label, q_val, V_val))

        eta_v = eta_func(q_mp)
        t2    = theta2_func(q_mp)
        t3    = theta3_func(q_mp)
        t4    = theta4_func(q_mp)

        print("  eta(q)    = %.8f" % float(eta_v))
        print("  theta2(q) = %.8f" % float(t2))
        print("  theta3(q) = %.8f" % float(t3))
        print("  theta4(q) = %.8f" % float(t4))

        print("  Generating formulas...", end="", flush=True)
        formulas = generate_formulas(eta_v, t2, t3, t4, V_mp, q_mp)
        print(" %d formulas" % len(formulas))

        results = find_best_matches(formulas, TARGETS)
        t_end = time.time()
        print("  Done in %.1fs" % (t_end - t_start))

        all_results[nome_label] = {
            "q": q_val, "V": V_val,
            "eta": float(eta_v), "t2": float(t2),
            "t3": float(t3), "t4": float(t4),
            "matches": results,
            "n_formulas": len(formulas),
        }

    return all_results


def print_summary(all_results):
    thresholds = [10.0, 1.0, 0.1, 0.01]

    # Build sorted rows (best 0.1% count first)
    summary_rows = []
    for nome_label, data in all_results.items():
        matches = data["matches"]
        counts = [sum(1 for (e, _, _) in matches.values() if e <= thr)
                  for thr in thresholds]
        summary_rows.append((nome_label, data["n_formulas"], counts, data))

    summary_rows.sort(key=lambda x: (x[2][2], x[2][1]), reverse=True)

    # ------------------------------------------------------------------
    print()
    print("=" * 78)
    print("RESULTS SUMMARY  --  matches at each error threshold")
    print("=" * 78)
    print()
    print("%-16s  %10s  %8s  %8s  %8s  %9s" % (
        "Nome", "#formulas", "<=10%", "<=1%", "<=0.1%", "<=0.01%"))
    print("-" * 78)
    for nome_label, n_forms, counts, data in summary_rows:
        marker = "  <-- REAL FRAMEWORK" if nome_label == "q=1/phi" else ""
        print("%-16s  %10d  %8d  %8d  %8d  %9d%s" % (
            nome_label, n_forms, counts[0], counts[1], counts[2], counts[3], marker))

    # ------------------------------------------------------------------
    print()
    print("=" * 78)
    print("DETAILED MATCH TABLE  (% error | formula)")
    print("=" * 78)
    print()

    # Header
    hdr = "%-14s  %12s" % ("Target", "actual")
    for nome_label, _, _, _ in summary_rows:
        hdr += "  %-22s" % nome_label
    print(hdr)
    print("-" * (14 + 12 + 25 * len(summary_rows)))

    for name, tv, desc in TARGETS:
        row = "%-14s  %12.6g" % (name, float(tv))
        for nome_label, n_forms, counts, data in summary_rows:
            err, formula, fval = data["matches"][name]
            if err < 0.01:
                tag = "***"
            elif err < 0.1:
                tag = "** "
            elif err < 1.0:
                tag = "*  "
            else:
                tag = "   "
            cell = "%s %6.2f%%  %-12s" % (tag, err, formula[:12])
            row += "  %-22s" % cell
        print(row)

    print()
    print("  Legend: *** = <0.01% error,  ** = <0.1%,  * = <1%")

    # ------------------------------------------------------------------
    print()
    print("=" * 78)
    print("PER-TARGET DETAIL  (sorted by q=1/phi performance)")
    print("=" * 78)
    print()

    phi_data = all_results.get("q=1/phi", {})
    phi_matches = phi_data.get("matches", {})

    target_rows = [(name, tv, desc, phi_matches.get(name, (999, "", None))[0])
                   for name, tv, desc in TARGETS]
    target_rows.sort(key=lambda x: x[3])

    hdr2 = "%-16s  %-26s" % ("Target", "Description")
    for nome_label, _, _, _ in summary_rows:
        lbl = nome_label.replace("q=", "")
        hdr2 += "  %-15s" % lbl
    print(hdr2)
    print("-" * (16 + 26 + 17 * len(summary_rows)))

    for name, tv, desc, phi_err in target_rows:
        row = "%-16s  %-26s" % (name, desc[:26])
        for nome_label, n_forms, counts, data in summary_rows:
            err, formula, fval = data["matches"][name]
            if err < 0.01:
                cell = "***%.4f%%" % err
            elif err < 0.1:
                cell = "** %.3f%%" % err
            elif err < 1.0:
                cell = "*  %.2f%%" % err
            elif err < 10.0:
                cell = "   %.1f%%" % err
            else:
                cell = "   MISS(%.0f%%)" % err
            row += "  %-15s" % cell
        print(row)

    # ------------------------------------------------------------------
    print()
    print("=" * 78)
    print("FINAL SCORE  --  Core 3 coupling formulas")
    print("=" * 78)
    print()

    CORE = {"alpha_s", "sin2_W", "inv_alpha"}

    print("%-16s  %-22s  %-22s  %-22s  ALL3<1%%" % (
        "Nome", "alpha_s", "sin2_W", "1/alpha"))
    print("-" * 95)
    for nome_label, n_forms, counts, data in summary_rows:
        m = data["matches"]
        r_as = m["alpha_s"]
        r_sw = m["sin2_W"]
        r_ia = m["inv_alpha"]
        all3 = all(r[0] < 1.0 for r in [r_as, r_sw, r_ia])
        marker = "  <-- REAL" if nome_label == "q=1/phi" else ""
        print("%-16s  %.3f%% (%-10s)  %.3f%% (%-10s)  %.3f%% (%-10s)  %-5s%s" % (
            nome_label,
            r_as[0], r_as[1][:10],
            r_sw[0], r_sw[1][:10],
            r_ia[0], r_ia[1][:10],
            "YES" if all3 else "NO",
            marker))

    # ------------------------------------------------------------------
    print()
    print("=" * 78)
    print("FULL 15-TARGET SCORE AT EACH THRESHOLD")
    print("=" * 78)
    print()
    print("%-16s  %6s  %6s  %8s  %9s" % ("Nome", "<=10%", "<=1%", "<=0.1%", "<=0.01%"))
    print("-" * 55)
    for nome_label, n_forms, counts, data in summary_rows:
        marker = "  <-- REAL FRAMEWORK" if nome_label == "q=1/phi" else ""
        print("%-16s  %6d  %6d  %8d  %9d%s" % (
            nome_label, counts[0], counts[1], counts[2], counts[3], marker))

    # ------------------------------------------------------------------
    print()
    print("=" * 78)
    print("STATISTICAL ASSESSMENT")
    print("=" * 78)
    print()

    phi_d     = all_results.get("q=1/phi", {})
    phi_1pct  = sum(1 for (e, _, _) in phi_d["matches"].values() if e <= 1.0)
    phi_01pct = sum(1 for (e, _, _) in phi_d["matches"].values() if e <= 0.1)

    others_1pct  = []
    others_01pct = []
    for nome_label, n_forms, counts, data in summary_rows:
        if nome_label != "q=1/phi":
            others_1pct.append(counts[1])
            others_01pct.append(counts[2])

    avg_1pct  = sum(others_1pct)  / len(others_1pct)  if others_1pct  else 0
    avg_01pct = sum(others_01pct) / len(others_01pct) if others_01pct else 0
    max_1pct  = max(others_1pct)  if others_1pct  else 0
    max_01pct = max(others_01pct) if others_01pct else 0

    print("  q=1/phi matches at <=1.0%%:  %d/15  (avg of 4 alternatives: %.1f, best: %d)" % (
        phi_1pct, avg_1pct, max_1pct))
    print("  q=1/phi matches at <=0.1%%:  %d/15  (avg of 4 alternatives: %.1f, best: %d)" % (
        phi_01pct, avg_01pct, max_01pct))
    print()
    print("  q=1/phi advantage at <=1%%:   +%.1f over average alternative" % (phi_1pct  - avg_1pct))
    print("  q=1/phi advantage at <=0.1%%: +%.1f over average alternative" % (phi_01pct - avg_01pct))

    adv = phi_01pct - avg_01pct
    if adv > 4:
        verdict = ("GENUINELY SPECIAL: q=1/phi significantly outperforms alternatives "
                   "at the same formula budget. The golden nome is not easily substituted.")
    elif adv > 1.5:
        verdict = ("MILDLY SPECIAL: q=1/phi has a real but modest advantage. "
                   "Some alternatives are competitive; the framework is real but not unique.")
    else:
        verdict = ("NOT SPECIAL: Alternative nomes match as many targets. "
                   "The framework may be doing nothing more than any algebraic punto can. "
                   "The 'matches' headline is likely inflated.")

    print()
    print("  VERDICT: %s" % verdict)

    # Core formula uniqueness
    print()
    core_winning = []
    for nome_label, n_forms, counts, data in summary_rows:
        m = data["matches"]
        if all(m[t][0] < 1.0 for t in CORE):
            core_winning.append(nome_label)

    print("  Nomes with ALL 3 core couplings matching at <=1%%: %s" % core_winning)
    if len(core_winning) == 1 and core_winning[0] == "q=1/phi":
        print("  -> Core 3 couplings (alpha_s, sin2_W, 1/alpha) are UNIQUELY satisfied")
        print("     at q=1/phi.  This is the framework's genuine non-trivial content.")
    elif len(core_winning) > 1:
        print("  -> Core 3 couplings are NOT unique to q=1/phi.")
        print("     The framework's uniqueness claim is DEFLATED.")
    else:
        print("  -> Even q=1/phi does NOT match all 3 core couplings at <=1%!")
        print("     (Check formula budget for these targets.)")

    print()
    print("=" * 78)
    print("END OF NULL MODEL TEST")
    print("=" * 78)


# ==============================================================================
# Entry point
# ==============================================================================

if __name__ == "__main__":
    all_results = run_all()
    print_summary(all_results)
