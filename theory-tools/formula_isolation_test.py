#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
formula_isolation_test.py

Tests whether Interface Theory's formulas are isolated in formula space --
i.e., changing any integer parameter breaks the match with experiment.

For each formula, systematically varies integer parameters and counts how
many "neighboring" formulas also hit the target within 1% (and 0.1%).

High isolation score = formula is specific, not cherry-picked.
Low isolation score = many nearby formulas work too, formula is not distinctive.
"""

import sys
import io
import math

# Force UTF-8 output on Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import mpmath
from mpmath import mp, mpf, sqrt, log, pi, power, fabs

mp.dps = 50

# ── Constants ─────────────────────────────────────────────────────────────────
phi      = (1 + sqrt(5)) / 2
phibar   = 1 / phi
q        = phibar           # golden nome q = 1/phi

# Measured values
mu_meas      = mpf("1836.15267343")    # proton-to-electron mass ratio
inv_alpha    = mpf("137.035999084")    # 1/alpha
alpha_em     = 1 / inv_alpha
mt_GeV       = mpf("172.69")          # top quark mass [GeV]
me_GeV       = mpf("0.00051099895")   # electron mass [GeV]
v_meas       = mpf("246.22")          # Higgs VEV [GeV]
M_Pl         = mpf("1.22089e19")      # Planck mass [GeV]
sin2_12_meas = mpf("0.307")           # sin^2(theta_12) solar
Lambda_meas  = mpf("2.89e-122")       # cosmological constant / M_Pl^4

# ── Modular forms at q = 1/phi ─────────────────────────────────────────────
N_terms = 300

eta_product = mpf(1)
for n in range(1, N_terms + 1):
    eta_product *= (1 - q**n)
eta_val = q**(mpf(1)/24) * eta_product

theta3_sum = mpf(0)
for n in range(1, N_terms + 1):
    theta3_sum += q**(n*n)
theta3 = 1 + 2*theta3_sum

theta4_sum = mpf(0)
for n in range(1, N_terms + 1):
    theta4_sum += ((-1)**n) * q**(n*n)
theta4 = 1 + 2*theta4_sum

# Print header values
print("=" * 72)
print("FORMULA ISOLATION TEST -- Interface Theory")
print("=" * 72)
print()
print("Golden constants (mpmath, {} digits):".format(mp.dps))
print("  phi      = {:.10f}".format(float(phi)))
print("  phibar   = {:.10f}".format(float(phibar)))
print("  q=1/phi  = {:.10f}".format(float(q)))
print("  eta(q)   = {:.10f}".format(float(eta_val)))
print("  theta3   = {:.10f}".format(float(theta3)))
print("  theta4   = {:.10f}".format(float(theta4)))
print()

# ── Helper functions ──────────────────────────────────────────────────────────
def pct_err(pred, meas):
    """Percentage deviation from target."""
    return float(fabs(pred - meas) / fabs(meas) * 100)

def isolation_score(n_neighbors, n_match_1pct):
    """n_neighbors / n_matching (= 1 / fraction matching)."""
    if n_match_1pct == 0:
        return float('inf')
    return n_neighbors / n_match_1pct

def report_section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)

def summarize(formula_name, framework_val, target, n_neighbors,
              matches_1pct, matches_01pct, best_neighbor_desc, best_neighbor_err,
              framework_err=None):
    if framework_err is None:
        framework_err = pct_err(framework_val, target)
    iso = isolation_score(n_neighbors, matches_1pct)
    print()
    print("  Formula        : {}".format(formula_name))
    print("  Framework value: {:.8g}   target: {:.8g}".format(float(framework_val), float(target)))
    print("  Framework match: {:.6f}%  (error {:.4f}%)".format(100 - framework_err, framework_err))
    print("  Neighbors tested: {}".format(n_neighbors))
    print("  Matching <1%  : {}".format(matches_1pct))
    print("  Matching <0.1%: {}".format(matches_01pct))
    print("  Best non-FW neighbor: {}  (error {:.4f}%)".format(best_neighbor_desc, best_neighbor_err))
    if iso == float('inf'):
        iso_str = "inf (no neighbors match within 1%)"
        tag = "[HIGH - formula is specific]"
    else:
        iso_str = "{:.1f}".format(iso)
        tag = "[HIGH - formula is specific]" if iso > 10 else "[LOW - many neighbors work]"
    print("  Isolation score: {}  {}".format(iso_str, tag))

# ══════════════════════════════════════════════════════════════════════════════
# 1.  mu = 6^5/phi^3 + 9/(7*phi^2)
# ══════════════════════════════════════════════════════════════════════════════
report_section("1. PROTON-ELECTRON MASS RATIO   mu = 6^5/phi^3 + 9/(7*phi^2)")
print("   Target: {:.8f}".format(float(mu_meas)))

# Framework formula
fw_mu = (mpf(6)**5) / phi**3 + mpf(9) / (7 * phi**2)
fw_err = pct_err(fw_mu, mu_meas)
print()
print("   Framework: 6^5/phi^3 + 9/(7*phi^2) = {:.8f}  ({:.6f}% match)".format(
    float(fw_mu), 100 - fw_err))

# f(a,b,c,d,e,f) = a^b / phi^c + d / (e * phi^f)
# Baseline: a=6, b=5, c=3, d=9, e=7, f=2

neighbors = []

# Vary a: 4..8 (excluding 6)
for a in [4, 5, 7, 8]:
    val = mpf(a)**5 / phi**3 + mpf(9) / (7*phi**2)
    err = pct_err(val, mu_meas)
    neighbors.append((err, "a={}: {}^5/phi^3 + 9/(7*phi^2) = {:.4f}".format(a, a, float(val))))

# Vary b: 3..7 (excluding 5)
for b in [3, 4, 6, 7]:
    val = mpf(6)**b / phi**3 + mpf(9) / (7*phi**2)
    err = pct_err(val, mu_meas)
    neighbors.append((err, "b={}: 6^{}/phi^3 + 9/(7*phi^2) = {:.4f}".format(b, b, float(val))))

# Vary c: 1..5 (excluding 3)
for c in [1, 2, 4, 5]:
    val = mpf(6)**5 / phi**c + mpf(9) / (7*phi**2)
    err = pct_err(val, mu_meas)
    neighbors.append((err, "c={}: 6^5/phi^{} + 9/(7*phi^2) = {:.4f}".format(c, c, float(val))))

# Vary d: 5..13 (excluding 9)
for d in [5, 6, 7, 8, 10, 11, 12, 13]:
    val = mpf(6)**5 / phi**3 + mpf(d) / (7*phi**2)
    err = pct_err(val, mu_meas)
    neighbors.append((err, "d={}: 6^5/phi^3 + {}/(7*phi^2) = {:.4f}".format(d, d, float(val))))

# Vary e: 3..11 (excluding 7)
for e in [3, 4, 5, 6, 8, 9, 10, 11]:
    val = mpf(6)**5 / phi**3 + mpf(9) / (e*phi**2)
    err = pct_err(val, mu_meas)
    neighbors.append((err, "e={}: 6^5/phi^3 + 9/({}*phi^2) = {:.4f}".format(e, e, float(val))))

# Vary f: 1, 3 (excluding 2)
for f in [1, 3]:
    val = mpf(6)**5 / phi**3 + mpf(9) / (7*phi**f)
    err = pct_err(val, mu_meas)
    neighbors.append((err, "f={}: 6^5/phi^3 + 9/(7*phi^{}) = {:.4f}".format(f, f, float(val))))

n1_total = len(neighbors)
n1_1pct  = sum(1 for e,_ in neighbors if e < 1.0)
n1_01pct = sum(1 for e,_ in neighbors if e < 0.1)
neighbors_sorted = sorted(neighbors, key=lambda x: x[0])
best_err1, best_desc1 = neighbors_sorted[0]

print()
print("   Neighbor scan ({} neighbors):".format(n1_total))
# Print all neighbors with their errors for transparency
for err, desc in sorted(neighbors, key=lambda x: x[0])[:8]:
    flag = " <-- MATCHES 1%" if err < 1.0 else ("" if err > 5 else " <-- near miss")
    print("     err={:7.3f}%  {}{}".format(err, desc, flag))
if n1_total > 8:
    print("     ... ({} more, all >{:.1f}% error)".format(
        n1_total - 8, sorted(neighbors, key=lambda x: x[0])[7][0]))

summarize(
    "6^5/phi^3 + 9/(7*phi^2)",
    fw_mu, mu_meas,
    n1_total, n1_1pct, n1_01pct,
    best_desc1, best_err1
)

# ══════════════════════════════════════════════════════════════════════════════
# 2. Core identity: alpha^(a/b) * mu^c * phi^d = N
# ══════════════════════════════════════════════════════════════════════════════
report_section("2. CORE IDENTITY SWEEP   alpha^(a/b) * mu^c * phi^d = N")
print("   Framework: alpha^(3/2) * mu^1 * phi^2 = 3")

# Evaluate the framework formula
fw_core = power(alpha_em, mpf(3)/2) * mu_meas * phi**2
fw_core_err = pct_err(fw_core, mpf(3))
print("   Framework value: {:.6f}  (target 3, match {:.4f}%)".format(
    float(fw_core), 100 - fw_core_err))

# Scan parameters
a_b_list = [(1,2), (1,1), (3,2), (2,1), (5,2), (3,1)]  # exponents of alpha
c_list   = [mpf(1)/2, mpf(1), mpf(3)/2, mpf(2)]
d_list   = [mpf(1), mpf(3)/2, mpf(2), mpf(5)/2, mpf(3)]
N_list   = [1, 2, 3, 4, 5, 6]

core_neighbors = []
total_core = 0

print()
print("   Scanning {}x{}x{}x{} = {} combinations...".format(
    len(a_b_list), len(c_list), len(d_list), len(N_list),
    len(a_b_list)*len(c_list)*len(d_list)*len(N_list)))

for a, b in a_b_list:
    for c in c_list:
        for d in d_list:
            for N in N_list:
                # skip exact framework
                is_fw = (a == 3 and b == 2 and c == mpf(1) and d == mpf(2) and N == 3)
                total_core += 1
                try:
                    val = power(alpha_em, mpf(a)/b) * power(mu_meas, c) * power(phi, d)
                    err = pct_err(val, mpf(N))
                    if not is_fw:
                        core_neighbors.append((err, a, b, c, d, N, float(val)))
                except Exception:
                    pass

n2_total  = len(core_neighbors)
n2_1pct   = sum(1 for e,*_ in core_neighbors if e < 1.0)
n2_01pct  = sum(1 for e,*_ in core_neighbors if e < 0.1)
core_sorted = sorted(core_neighbors, key=lambda x: x[0])

print()
print("   Top 10 best-matching combinations (excluding framework 3/2, 1, 2, 3):")
print("   {:>8} {:>8} {:>8} {:>4} {:>12} {:>10}".format(
    "exp_a", "exp_mu", "exp_phi", "N", "value", "error%"))
for row in core_sorted[:10]:
    e, a, b, c, d, N, val = row
    flag = " <--1%" if e < 1.0 else ""
    print("   {}/{:>6} {:>8.2f} {:>8.2f} {:>4}   {:>12.5f}  {:>9.4f}%{}".format(
        a, b, float(c), float(d), N, val, e, flag))

print()
print("   Framework: alpha^(3/2)*mu^1*phi^2 = {:.6f} ~ 3  (error {:.4f}%)".format(
    float(fw_core), fw_core_err))
print("   Total combinations tested: {}".format(n2_total + 1))
print("   Matching within 1%  (excluding FW): {}".format(n2_1pct))
print("   Matching within 0.1% (excluding FW): {}".format(n2_01pct))

best_e2, ba, bb, bc, bd, bN, bval = core_sorted[0]
summarize(
    "alpha^(3/2)*mu*phi^2 = 3",
    fw_core, mpf(3),
    n2_total, n2_1pct, n2_01pct,
    "alpha^({}/{})*mu^{:.1f}*phi^{:.1f}={}  ({:.5f})".format(ba, bb, float(bc), float(bd), bN, bval),
    best_e2
)

# ══════════════════════════════════════════════════════════════════════════════
# 3. m_t = m_e * mu^2 / N  (N=10)
# ══════════════════════════════════════════════════════════════════════════════
report_section("3. TOP QUARK MASS   m_t = m_e * mu^a / N")
print("   Framework: m_e*mu^2/10 = {:.5f} GeV  (target {:.5f} GeV)".format(
    float(me_GeV * mu_meas**2 / 10), float(mt_GeV)))

fw_mt  = me_GeV * mu_meas**2 / 10
fw_mt_err = pct_err(fw_mt, mt_GeV)
print("   Match: {:.4f}%  (error {:.4f}%)".format(100 - fw_mt_err, fw_mt_err))

a_vals  = [mpf("1.5"), mpf("1.8"), mpf("2.0"), mpf("2.2"), mpf("2.5")]
N_range = list(range(1, 31))

mt_neighbors = []
print()
print("   Scanning {} x {} = {} combinations...".format(
    len(a_vals), len(N_range), len(a_vals)*len(N_range)))

for a in a_vals:
    for N in N_range:
        is_fw = (a == mpf("2.0") and N == 10)
        val   = me_GeV * power(mu_meas, a) / N
        err   = pct_err(val, mt_GeV)
        if not is_fw:
            mt_neighbors.append((err, float(a), N, float(val)))

n3_total  = len(mt_neighbors)
n3_1pct   = sum(1 for e,*_ in mt_neighbors if e < 1.0)
n3_01pct  = sum(1 for e,*_ in mt_neighbors if e < 0.1)
mt_sorted = sorted(mt_neighbors, key=lambda x: x[0])

print()
print("   Top 10 best-matching (excluding framework a=2, N=10):")
print("   {:>6} {:>5} {:>14} {:>10}".format("a", "N", "value(GeV)", "error%"))
for e, a, N, val in mt_sorted[:10]:
    flag = " <--1%" if e < 1.0 else ""
    print("   {:>6.2f} {:>5}   {:>14.5f}  {:>9.4f}%{}".format(a, N, val, e, flag))

best_e3, ba3, bN3, bval3 = mt_sorted[0]
summarize(
    "m_e*mu^2/10",
    fw_mt, mt_GeV,
    n3_total, n3_1pct, n3_01pct,
    "m_e*mu^{}/N={}  ({:.5f} GeV)".format(ba3, bN3, bval3), best_e3
)

# ══════════════════════════════════════════════════════════════════════════════
# 4. sin^2(theta_12) = 1/3 - theta4 * sqrt(3/4)
# ══════════════════════════════════════════════════════════════════════════════
report_section("4. SOLAR MIXING ANGLE   sin^2(theta_12) = 1/N - theta4*sqrt(a/b)")
print("   Framework: 1/3 - theta4*sqrt(3/4) = ?  (target {:.4f})".format(
    float(sin2_12_meas)))

fw_sin12 = mpf(1)/3 - theta4 * sqrt(mpf(3)/4)
fw_sin12_err = pct_err(fw_sin12, sin2_12_meas)
print("   Framework value: {:.6f}  (match {:.4f}%)".format(
    float(fw_sin12), 100 - fw_sin12_err))

N_sin12  = [2, 3, 4, 5]
a_sin12  = [1, 2, 3, 4, 5]
b_sin12  = [1, 2, 3, 4, 5]

sin12_neighbors = []
for N in N_sin12:
    for a in a_sin12:
        for b in b_sin12:
            is_fw = (N == 3 and a == 3 and b == 4)
            if a == 0 or b == 0:
                continue
            try:
                val = mpf(1)/N - theta4 * sqrt(mpf(a)/b)
                # Skip if unphysical
                if float(val) <= 0 or float(val) >= 1:
                    continue
                err = pct_err(val, sin2_12_meas)
                if not is_fw:
                    sin12_neighbors.append((err, N, a, b, float(val)))
            except Exception:
                pass

n4_total  = len(sin12_neighbors)
n4_1pct   = sum(1 for e,*_ in sin12_neighbors if e < 1.0)
n4_01pct  = sum(1 for e,*_ in sin12_neighbors if e < 0.1)
sin12_sorted = sorted(sin12_neighbors, key=lambda x: x[0])

print()
print("   Scanning {}x{}x{} = {} combinations (physical values only)".format(
    len(N_sin12), len(a_sin12), len(b_sin12), n4_total + 1))
print()
print("   Top 10 best-matching (excluding framework N=3, a=3, b=4):")
print("   {:>6} {:>4} {:>4} {:>10} {:>10}".format("1/N", "a", "b", "value", "error%"))
for e, N, a, b, val in sin12_sorted[:10]:
    flag = " <--1%" if e < 1.0 else ""
    print("   1/{:<4}  {:>4} {:>4}   {:>10.6f}  {:>9.4f}%{}".format(N, a, b, val, e, flag))

print()
print("   (values outside [0,1] excluded as unphysical)")

best_e4, bN4, ba4, bb4, bval4 = sin12_sorted[0]
summarize(
    "1/3 - theta4*sqrt(3/4)",
    fw_sin12, sin2_12_meas,
    n4_total, n4_1pct, n4_01pct,
    "1/{} - theta4*sqrt({}/{})  ({:.6f})".format(bN4, ba4, bb4, bval4), best_e4
)

# ══════════════════════════════════════════════════════════════════════════════
# 7. Lambda = theta4^N * sqrt(5)/phi^2
# ══════════════════════════════════════════════════════════════════════════════
report_section("7. COSMOLOGICAL CONSTANT   Lambda/M_Pl^4 = theta4^N * sqrt(5)/phi^2")
print("   Framework N=80: theta4^80 * sqrt(5)/phi^2")

prefactor_lambda = sqrt(mpf(5)) / phi**2
fw_lambda = prefactor_lambda * power(theta4, 80)
fw_lam_err = pct_err(fw_lambda, Lambda_meas)
print("   theta4   = {:.8f}".format(float(theta4)))
print("   theta4^80 = {:.6e}".format(float(power(theta4, 80))))
print("   Framework value (N=80): {:.6e}  target: {:.6e}".format(
    float(fw_lambda), float(Lambda_meas)))
print("   Match: {:.6f}%  (error {:.4f}%)".format(100 - fw_lam_err, fw_lam_err))

print()
print("   Sensitivity scan N = 60..100:")
print("   {:>5}  {:>16}  {:>12}  {:>12}  {:>14}".format(
    "N", "value", "log10(val)", "log10_err", "within 1 OOM"))
lam_neighbors = []
for N in range(60, 101):
    is_fw = (N == 80)
    val = prefactor_lambda * power(theta4, N)
    log_err = abs(math.log10(float(val)) - math.log10(float(Lambda_meas)))
    err_pct = pct_err(val, Lambda_meas)
    within_1oom = "YES" if log_err < 1.0 else "no"
    fw_mark = " <-- FW" if is_fw else ""
    print("   {:>5}  {:>16.6e}  {:>12.2f}  {:>12.4f}  {:>14}{}".format(
        N, float(val), math.log10(float(val)), log_err, within_1oom, fw_mark))
    if not is_fw:
        lam_neighbors.append((err_pct, N, float(val), log_err))

n7_total  = len(lam_neighbors)
n7_1pct   = sum(1 for e,*_ in lam_neighbors if e < 1.0)
n7_01pct  = sum(1 for e,*_ in lam_neighbors if e < 0.1)
n7_1oom   = sum(1 for _,_,_,log_err in lam_neighbors if log_err < 1.0)
lam_sorted = sorted(lam_neighbors, key=lambda x: x[0])
best_e7, bN7, bval7, _ = lam_sorted[0]

print()
print("   Neighbors within 1 order of magnitude: {} of {}".format(n7_1oom, n7_total))
print("   Neighbors within 1% (by value): {}".format(n7_1pct))
print("   Neighbors within 10% (by value): {}".format(
    sum(1 for e,*_ in lam_neighbors if e < 10.0)))
print()
print("   NOTE: theta4 = {:.5f}; each step in N multiplies by theta4.".format(float(theta4)))
print("   Each N+/-1 changes value by factor {:.4f} = {:.2f}% change".format(
    float(theta4), 100*(1-float(theta4))))
print("   So N+/-1 changes value by ~{:.1f}% --> only N=80 matches within 1%.".format(
    (1-float(theta4))*100))
summarize(
    "theta4^80*sqrt(5)/phi^2",
    fw_lambda, Lambda_meas,
    n7_total, n7_1pct, n7_01pct,
    "N={}: {:.4e}".format(bN7, bval7), best_e7
)

# ══════════════════════════════════════════════════════════════════════════════
# 8. v = M_Pl * phibar^N / (1 - phi*theta4) * (1 + eta*theta4*7/6)
# ══════════════════════════════════════════════════════════════════════════════
report_section("8. HIGGS VEV   v = M_Pl * phibar^N / (1-phi*theta4) * (1+eta*theta4*7/6)")
print("   Framework N=80, target {} GeV".format(float(v_meas)))

denom_v = 1 - phi * theta4
loop_v  = 1 + eta_val * theta4 * mpf(7)/6
def higgs_vev(N):
    return M_Pl * power(phibar, N) / denom_v * loop_v

fw_v     = higgs_vev(80)
fw_v_err = pct_err(fw_v, v_meas)
print("   1 - phi*theta4    = {:.8f}".format(float(denom_v)))
print("   1 + eta*theta4*7/6 = {:.8f}".format(float(loop_v)))
print("   Framework (N=80): {:.5f} GeV  (match {:.6f}%)".format(
    float(fw_v), 100 - fw_v_err))

print()
print("   Sensitivity scan N = 70..90:")
print("   {:>5}  {:>14}  {:>10}".format("N", "v(GeV)", "error%"))
v_neighbors = []
for N in range(70, 91):
    is_fw = (N == 80)
    val   = higgs_vev(N)
    err   = pct_err(val, v_meas)
    fw_mark = " <-- FW" if is_fw else ""
    match_str = " <-- <1%" if (err < 1.0 and not is_fw) else ""
    print("   {:>5}  {:>14.5f}  {:>10.4f}%{}{}".format(
        N, float(val), err, fw_mark, match_str))
    if not is_fw:
        v_neighbors.append((err, N, float(val)))

n8_total  = len(v_neighbors)
n8_1pct   = sum(1 for e,*_ in v_neighbors if e < 1.0)
n8_01pct  = sum(1 for e,*_ in v_neighbors if e < 0.1)
v_sorted  = sorted(v_neighbors, key=lambda x: x[0])
best_e8, bN8, bval8 = v_sorted[0]

print()
print("   phibar = {:.6f}; each step in N multiplies by phibar.".format(float(phibar)))
print("   Each N+/-1 changes v by factor {:.4f} = {:.2f}% change".format(
    float(phibar), (1-float(phibar))*100))
print("   ==> Only N=80 (and maybe N=79 if error<1%) matches.")
summarize(
    "M_Pl*phibar^80/(1-phi*theta4)*(1+eta*theta4*7/6)",
    fw_v, v_meas,
    n8_total, n8_1pct, n8_01pct,
    "N={}: {:.5f} GeV".format(bN8, bval8), best_e8
)

# ══════════════════════════════════════════════════════════════════════════════
# SUMMARY TABLE
# ══════════════════════════════════════════════════════════════════════════════
print()
print("=" * 72)
print("SUMMARY: ISOLATION SCORES ACROSS ALL FORMULAS")
print("=" * 72)

def iso_str(n, k):
    s = isolation_score(n, k)
    if s == float('inf'):
        return "    inf"
    return "{:7.1f}".format(s)

print()
print("  Formula                              FW match   Nbrs  <1%  <0.1%  Isolation")
print("  " + "-"*74)
print("  1. mu = 6^5/phi^3 + 9/(7*phi^2)    {:.4f}%  {:>4}  {:>3}    {:>3}  {}".format(
    100-fw_err, n1_total, n1_1pct, n1_01pct, iso_str(n1_total, n1_1pct)))
print("  2. alpha^(3/2)*mu*phi^2 = 3          {:.4f}%  {:>4}  {:>3}    {:>3}  {}".format(
    100-fw_core_err, n2_total, n2_1pct, n2_01pct, iso_str(n2_total, n2_1pct)))
print("  3. m_e*mu^2/10 = m_t                 {:.4f}%  {:>4}  {:>3}    {:>3}  {}".format(
    100-fw_mt_err, n3_total, n3_1pct, n3_01pct, iso_str(n3_total, n3_1pct)))
print("  4. 1/3-theta4*sqrt(3/4) = sin^2 t12 {:.4f}%  {:>4}  {:>3}    {:>3}  {}".format(
    100-fw_sin12_err, n4_total, n4_1pct, n4_01pct, iso_str(n4_total, n4_1pct)))
print("  7. theta4^80*sqrt(5)/phi^2 = Lambda  {:.4f}%  {:>4}  {:>3}    {:>3}  {}".format(
    100-fw_lam_err, n7_total, n7_1pct, n7_01pct, iso_str(n7_total, n7_1pct)))
print("  8. M_Pl*phibar^80/(...) = v          {:.4f}%  {:>4}  {:>3}    {:>3}  {}".format(
    100-fw_v_err, n8_total, n8_1pct, n8_01pct, iso_str(n8_total, n8_1pct)))
print()

print("  ISOLATION SCORE KEY:")
print("    > 20  = highly isolated (formula specific, not cherry-picked)")
print("    5-20  = moderately isolated")
print("    1-5   = low isolation (many neighbors also work)")
print("    < 1   = very low (random parameter variations work)")
print()
print("  NOTE ON FORMULA 2 (CORE IDENTITY SWEEP):")
print("    Many integer combos hit SOME small integer. The real question is")
print("    whether {3/2, 1, 2, 3} is uniquely close. Low isolation here")
print("    reflects the density of small integers near alpha^(a/b)*mu^c*phi^d.")
print()
print("  NOTE ON FORMULAS 7 AND 8 (EXPONENT N=80):")
print("    High isolation guaranteed when theta4~0.03 (each step changes 97%).")
print("    But the key question is whether N=80 is derived or fitted.")
print("    Derivation: N = 2 x 240/6 = 80  (E8 roots / |W(A2)| x 2).")
print("    The formula is isolated by construction from the physics, not by luck.")
print()
print("Done.")
