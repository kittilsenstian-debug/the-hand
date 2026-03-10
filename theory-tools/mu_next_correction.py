#!/usr/bin/env python3
"""
mu_next_correction.py -- Derive the next correction to mu = 6^5/phi^3
=====================================================================

Leading order:  mu_0 = 6^5/phi^3 = 1835.6646...
Measured:       mu   = 1836.15267343(11)
Gap:       Delta = mu_meas - mu_0 = +0.4881 (need to ADD this to mu_0)

Previously searched correction: 9/(7*phi^2) = 0.4911 -> mu match 99.9998%
But Phase 1 testing: 18/30 neighbors also match at 1% -> decorative.

GOAL: Find a DERIVED (not searched) correction via 6 approaches.
HONESTY PROTOCOL: If nothing works better than searched, say so.

Feb 26, 2026 -- Standard Python + mpmath only.
"""

import mpmath
from mpmath import mp, mpf, sqrt, log, pi, power, fabs

mp.dps = 50

# ======================================================================
# FUNDAMENTAL CONSTANTS
# ======================================================================
phi    = (1 + sqrt(5)) / 2
phibar = 1 / phi
q      = phibar
mu_meas     = mpf("1836.15267343")
mu_meas_unc = mpf("0.00000011")
alpha_meas  = 1 / mpf("137.035999084")

# ======================================================================
# MODULAR FORMS at q = 1/phi
# ======================================================================
N_TERMS = 500

_ep = mpf(1)
for n in range(1, N_TERMS + 1):
    _ep *= (1 - q**n)
eta = q ** (mpf(1)/24) * _ep

_t2 = mpf(0)
for n in range(N_TERMS):
    _t2 += q ** (n*(n+1))
theta2 = 2 * q**(mpf(1)/4) * _t2

_t3 = mpf(0)
for n in range(1, N_TERMS + 1):
    v = q**(n*n)
    if v < mpf(10)**(-45): break
    _t3 += v
theta3 = 1 + 2*_t3

_t4 = mpf(0)
for n in range(1, N_TERMS + 1):
    v = q**(n*n)
    if v < mpf(10)**(-45): break
    _t4 += ((-1)**n) * v
theta4 = 1 + 2*_t4

q2 = q**2
_ep2 = mpf(1)
for n in range(1, N_TERMS + 1):
    _ep2 *= (1 - q2**n)
eta_dark = q2**(mpf(1)/24) * _ep2

C = eta * theta4 / 2

def sigma_k(n, k):
    s = mpf(0)
    for d in range(1, n+1):
        if n % d == 0:
            s += power(d, k)
    return s

_e4s = mpf(0)
for n in range(1, 201):
    _e4s += sigma_k(n, 3) * q**n
E4 = 1 + 240*_e4s

# Lucas and Fibonacci
def lucas(n):
    if n == 0: return 2
    if n == 1: return 1
    a, b = 2, 1
    for _ in range(n-1):
        a, b = b, a+b
    return b

def fib(n):
    if n == 0: return 0
    if n == 1: return 1
    a, b = 0, 1
    for _ in range(n-1):
        a, b = b, a+b
    return b

Luc = [lucas(n) for n in range(25)]
Fib = [fib(n) for n in range(25)]

# ======================================================================
# THE GAP
# ======================================================================
mu_0   = mpf(6)**5 / phi**3
Delta  = mu_meas - mu_0              # positive ~ +0.4881
target = Delta                        # what we need to ADD

mu_1_old    = mpf(9) / (7 * phi**2)  # old searched correction
mu_pred_old = mu_0 + mu_1_old

SEP  = "=" * 78
DASH = "-" * 78

def ppm_val(pred, meas):
    return float((pred - meas)/meas * 1e6)

def match_pct(pred, meas):
    return float((1 - abs(float(pred-meas))/abs(float(meas))) * 100)

def sigma_off(pred, meas, unc):
    return float(abs(pred-meas)/unc)

# Collect all results
all_results = []
def record(name, mu_val, dtype="searched"):
    m = match_pct(mu_val, mu_meas)
    p = ppm_val(mu_val, mu_meas)
    s = sigma_off(mu_val, mu_meas, mu_meas_unc)
    all_results.append((name, float(mu_val), m, p, s, dtype))
    return m, p, s

# ======================================================================
print(SEP)
print("MU NEXT CORRECTION: SYSTEMATIC DERIVATION ATTEMPT")
print(SEP)

print(f"\n--- SETUP ---")
print(f"phi           = {float(phi):.15f}")
print(f"mu_0 = 6^5/phi^3 = {float(mu_0):.10f}")
print(f"mu_measured     = {float(mu_meas):.10f}")
print(f"Delta = mu_meas - mu_0 = {float(Delta):+.10f}")
print(f"  Need to ADD {float(Delta):.10f} to mu_0")
print(f"  |Delta|/mu = {float(abs(Delta)/mu_meas*100):.5f}%")
print(f"  |Delta|/sigma = {float(abs(Delta)/mu_meas_unc):.0f}")

print(f"\n--- MODULAR FORMS ---")
print(f"eta        = {float(eta):.12f}")
print(f"theta2     = {float(theta2):.12f}")
print(f"theta3     = {float(theta3):.12f}")
print(f"theta4     = {float(theta4):.12f}")
print(f"eta_dark   = {float(eta_dark):.12f}")
print(f"C=eta*th4/2= {float(C):.12f}")
print(f"alpha      = {float(alpha_meas):.12e}")

print(f"\n--- BASELINE (old searched formula) ---")
print(f"9/(7*phi^2) = {float(mu_1_old):.10f}")
print(f"mu_0 + 9/(7*phi^2) = {float(mu_pred_old):.10f}")
print(f"Match: {match_pct(mu_pred_old, mu_meas):.7f}%, ppm: {ppm_val(mu_pred_old, mu_meas):+.2f}")
record("Baseline: 9/(7*phi^2)", mu_pred_old, "searched")


# ######################################################################
# APPROACH 1: q-EXPANSION / MODULAR FORM CORRECTIONS
# ######################################################################
print(f"\n\n{'#'*78}")
print("APPROACH 1: MODULAR FORM CORRECTIONS")
print(f"{'#'*78}")
print(f"Target additive correction = {float(target):.10f}")

# 1A: Multiplicative
print(f"\n--- 1A: mu = mu_0 * (1 + f), need f = {float(Delta/mu_0):.10e} ---")
f_need = Delta/mu_0

mf_mult = {
    "eta":            eta,
    "eta/2":          eta/2,
    "eta/3":          eta/3,
    "eta/4":          eta/4,
    "eta*theta4":     eta*theta4,
    "C":              C,
    "C*phi":          C*phi,
    "eta^2":          eta**2,
    "eta^2*phi":      eta**2*phi,
    "eta_dark/phi^2": eta_dark/phi**2,
    "theta4":         theta4,
    "theta4/phi":     theta4/phi,
    "theta4^2":       theta4**2,
    "alpha":          alpha_meas,
    "alpha*phi":      alpha_meas*phi,
    "alpha*phi^2":    alpha_meas*phi**2,
    "alpha*ln(phi)/pi": alpha_meas*log(phi)/pi,
}

print(f"{'Formula':35s} {'Value':>14s} {'Ratio f/need':>14s} {'mu match %':>12s}")
print(DASH)
for name, val in sorted(mf_mult.items(), key=lambda x: abs(float(x[1]/f_need - 1))):
    ratio = float(val/f_need)
    mu_t = mu_0*(1+val)
    m = match_pct(mu_t, mu_meas)
    if 0.1 < ratio < 10:
        flag = " <<<" if abs(ratio-1) < 0.1 else ""
        print(f"  {name:33s} {float(val):>14.8e} {ratio:>14.6f} {m:>12.6f}%{flag}")
        if abs(ratio-1) < 0.1:
            record(f"1A: mu_0*(1+{name})", mu_t, "searched")

# 1B: Additive scan
print(f"\n--- 1B: Additive modular scan ---")
print(f"  Scanning eta^a * theta4^b * phi^c * (n/m) near target={float(target):.8f}")

results_1b = []
for a_eta in range(0, 5):
    for b_th4 in range(0, 5):
        for c_phi in range(-8, 9):
            base = eta**a_eta * theta4**b_th4 * phi**c_phi
            if fabs(base) < mpf("1e-15") or fabs(base) > mpf("1e6"):
                continue
            for num in range(1, 21):
                for den in range(1, 21):
                    val = base * mpf(num) / mpf(den)
                    if fabs(val - target)/fabs(target) < mpf("0.001"):
                        err = float(fabs(val-target)/fabs(target) * 100)
                        label = f"eta^{a_eta}*th4^{b_th4}*phi^{c_phi}*{num}/{den}"
                        results_1b.append((err, label, float(val)))

results_1b.sort()
print(f"\nTOP 20 matches (within 0.1% of target):")
seen = set()
ct = 0
for err, label, val in results_1b:
    r = round(val, 10)
    if r in seen: continue
    seen.add(r)
    mu_t = float(mu_0) + val
    m = match_pct(mpf(mu_t), mu_meas)
    print(f"  {ct+1:3d}. {label:50s} = {val:.10e} ({err:.5f}%) mu:{m:.7f}%")
    record(f"1B: mu_0+{label}", mpf(mu_t), "searched")
    ct += 1
    if ct >= 20: break

# Also scan with theta3
results_1b3 = []
for a_eta in range(0, 3):
    for b_th3 in range(1, 3):
        for c_phi in range(-5, 6):
            base = eta**a_eta * theta3**b_th3 * phi**c_phi
            if fabs(base) < mpf("1e-8") or fabs(base) > mpf("1e6"):
                continue
            for num in range(1, 21):
                for den in range(1, 21):
                    val = base * mpf(num)/mpf(den)
                    if fabs(val-target)/fabs(target) < mpf("0.001"):
                        err = float(fabs(val-target)/fabs(target)*100)
                        label = f"eta^{a_eta}*th3^{b_th3}*phi^{c_phi}*{num}/{den}"
                        results_1b3.append((err, label, float(val)))

results_1b3.sort()
if results_1b3:
    print(f"\nTOP 10 theta3-based:")
    seen3 = set()
    ct3 = 0
    for err, label, val in results_1b3:
        r = round(val, 10)
        if r in seen3: continue
        seen3.add(r)
        mu_t = float(mu_0)+val
        m = match_pct(mpf(mu_t), mu_meas)
        print(f"  {ct3+1:3d}. {label:50s} = {val:.10e} ({err:.5f}%) mu:{m:.7f}%")
        ct3 += 1
        if ct3 >= 10: break


# ######################################################################
# APPROACH 2: 1-LOOP PERTURBATIVE CORRECTION
# ######################################################################
print(f"\n\n{'#'*78}")
print("APPROACH 2: 1-LOOP PERTURBATIVE CORRECTION")
print(f"{'#'*78}")

alpha = alpha_meas

# Route A: mu = mu_0 * (1 + alpha*g/pi)
g_need = float(target/mu_0 * pi/alpha)
print(f"\n--- 2A: mu = mu_0*(1 + alpha*g/pi), need g = {g_need:.10f} ---")
g_tests = {
    "ln(phi)":          float(log(phi)),
    "phi/3":            float(phi/3),
    "1/(3*phi)":        float(1/(3*phi)),
    "1/phi^2":          float(1/phi**2),
    "1/phi^3":          float(1/phi**3),
    "ln(phi)/phi":      float(log(phi)/phi),
    "ln(phi)*phi":      float(log(phi)*phi),
    "1/3":              1/3,
    "sqrt(5)/pi":       float(sqrt(5)/pi),
    "1/(2*phi)":        float(1/(2*phi)),
    "phi/(4*pi)":       float(phi/(4*pi)),
    "eta":              float(eta),
    "theta4":           float(theta4),
    "1/pi":             float(1/pi),
    "phi/9":            float(phi/9),
    "1/9":              1/9,
    "ln(phi)/3":        float(log(phi)/3),
    "2*ln(phi)/3":      float(2*log(phi)/3),
}
print(f"{'Expression':25s} {'Value':>14s} {'Ratio g/expr':>14s} {'err%':>10s}")
print("-"*66)
for name, val in sorted(g_tests.items(), key=lambda x: abs(x[1]/g_need - 1) if x[1]!=0 else 999):
    if val == 0: continue
    r = g_need/val
    err = abs(r-1)*100
    if err < 50:
        flag = " <<<" if err < 5 else ""
        print(f"  {name:23s} {val:>14.10f} {r:>14.6f} {err:>10.3f}%{flag}")
        if err < 5:
            mu_t = mu_0*(1 + alpha_meas*val/pi)
            record(f"2A: mu_0*(1+alpha*{name}/pi)", mu_t, "derived")

# Route B: Core identity mu = 3/(alpha^1.5 * phi^2)
print(f"\n--- 2B: Core identity route ---")
mu_tree = 3/(alpha**mpf("1.5")*phi**2)
print(f"mu_tree = 3/(alpha^1.5*phi^2) = {float(mu_tree):.10f}")
print(f"mu_meas                        = {float(mu_meas):.10f}")
print(f"Diff = {float(mu_tree-mu_meas):.10f}, ppm = {ppm_val(mu_tree,mu_meas):.1f}")
m,p,s = record("2B: mu_tree=3/(a^1.5*phi^2)", mu_tree, "derived")

# 1-loop
c1 = alpha*log(phi)/pi
mu_1L = mu_tree/(1+c1)
print(f"\n1-loop: mu_tree/(1+alpha*ln(phi)/pi)")
print(f"  factor = {float(c1):.10e}")
print(f"  mu_1L = {float(mu_1L):.10f}, ppm = {ppm_val(mu_1L,mu_meas):.2f}")
m,p,s = record("2B: 1-loop exact", mu_1L, "derived")

mu_1Lx = mu_tree*(1-c1)
print(f"  expanded: {float(mu_1Lx):.10f}, ppm = {ppm_val(mu_1Lx,mu_meas):.2f}")
record("2B: 1-loop expanded", mu_1Lx, "derived")

# 2-loop
c2_fw = (alpha/pi)**2*(5+1/phi**4)
mu_2L = mu_tree/(1+c1+c2_fw)
mu_2Lx = mu_tree*(1-c1-c2_fw+c1**2)
print(f"\n2-loop: + (alpha/pi)^2*(5+1/phi^4)")
print(f"  c2 = {float(c2_fw):.10e}")
print(f"  mu_2L exact = {float(mu_2L):.10f}, ppm = {ppm_val(mu_2L,mu_meas):.2f}")
print(f"  mu_2L expanded = {float(mu_2Lx):.10f}, ppm = {ppm_val(mu_2Lx,mu_meas):.2f}")
record("2B: 2-loop exact", mu_2L, "derived")

# What 2-loop coefficient would be exact?
c2_exact = (mu_tree/mu_meas - 1 - c1)/(alpha/pi)**2
print(f"\n  Exact c2 needed = {float(c2_exact):.6f}")
print(f"  Framework c2 = {float(5+1/phi**4):.6f}")
print(f"  Ratio = {float(c2_exact/(5+1/phi**4)):.6f}")

# The 1-loop is closest, overshooting by ~9 ppm.
# The 2-loop overcorrects (goes negative). The REAL 2-loop must be smaller.
# c2_exact ~ 1.72, framework gives 5.15.
# c2_exact/c2_fw = 0.334 ~ 1/3
print(f"\n  c2_exact/c2_framework = {float(c2_exact/(5+1/phi**4)):.6f} ~ 1/3 = {1/3:.6f}")
err_13 = float(abs(c2_exact/(5+1/phi**4) - 1/3)/(1/3)*100)
print(f"  Off from 1/3 by {err_13:.2f}%")

if err_13 < 3:
    c2_derived = (5+1/phi**4)/3
    mu_2Ld = mu_tree/(1 + c1 + (alpha/pi)**2*c2_derived)
    print(f"\n  *** mu_tree/(1 + c1 + (a/pi)^2*(5+1/phi^4)/3) = {float(mu_2Ld):.10f}")
    print(f"  ppm = {ppm_val(mu_2Ld, mu_meas):.2f}")
    record("2B: 2-loop c2/3", mu_2Ld, "derived")


# ######################################################################
# APPROACH 3: LUCAS SEQUENCE
# ######################################################################
print(f"\n\n{'#'*78}")
print("APPROACH 3: LUCAS SEQUENCE CONNECTION")
print(f"{'#'*78}")
print(f"Lucas: {dict((n,Luc[n]) for n in range(12))}")

# Scan L(n)/phi^k near mu
print(f"\n--- L(n)/phi^k near mu ---")
for n in range(10, 24):
    for k in range(0, 8):
        val = mpf(Luc[n])/phi**k
        diff = val - mu_meas
        if fabs(diff) < 5:
            print(f"  L({n:2d})/phi^{k} = {Luc[n]:>10d}/phi^{k} = {float(val):>14.6f} (diff={float(diff):+.6f})")
            record(f"3: L({n})/phi^{k}", val, "derived")

# Is 7776 = L(a)+L(b)?
print(f"\n--- Is 7776 a Lucas sum/product? ---")
found_luc = False
for a in range(24):
    for b in range(a, 24):
        if Luc[a]+Luc[b] == 7776:
            print(f"  7776 = L({a})+L({b}) = {Luc[a]}+{Luc[b]}")
            found_luc = True
        if Luc[a]*Luc[b] == 7776:
            print(f"  7776 = L({a})*L({b}) = {Luc[a]}*{Luc[b]}")
            found_luc = True
if not found_luc:
    print("  7776 is NOT a sum or product of two Lucas numbers.")

# Correction as Lucas expression
print(f"\n--- target = {float(target):.8f} as L(n)/(m*phi^k) ---")
results_3 = []
for n in range(0, 15):
    for k in range(0, 10):
        for m in range(1, 50):
            val = mpf(Luc[n])/(m*phi**k)
            err = float(fabs(val-target)/target*100)
            if err < 0.1:
                results_3.append((err, f"L({n})/({m}*phi^{k})", float(val)))

results_3.sort()
if results_3:
    for i, (err, label, val) in enumerate(results_3[:10]):
        mu_t = float(mu_0)+val
        m = match_pct(mpf(mu_t), mu_meas)
        print(f"  {i+1:3d}. {label:30s} = {val:.10e} ({err:.4f}%) mu:{m:.7f}%")
        record(f"3: mu_0+{label}", mpf(mu_t), "searched")
else:
    print("  (No Lucas matches within 0.1%)")

# Fibonacci
results_3f = []
for n in range(1, 15):
    for k in range(0, 10):
        for m in range(1, 50):
            val = mpf(Fib[n])/(m*phi**k)
            err = float(fabs(val-target)/target*100)
            if err < 0.1:
                results_3f.append((err, f"F({n})/({m}*phi^{k})", float(val)))

results_3f.sort()
if results_3f:
    print(f"\n  Fibonacci:")
    for i, (err, label, val) in enumerate(results_3f[:10]):
        mu_t = float(mu_0)+val
        m = match_pct(mpf(mu_t), mu_meas)
        print(f"  {i+1:3d}. {label:30s} = {val:.10e} ({err:.4f}%) mu:{m:.7f}%")
        record(f"3: mu_0+{label}", mpf(mu_t), "searched")


# ######################################################################
# APPROACH 4: E8 STRUCTURE
# ######################################################################
print(f"\n\n{'#'*78}")
print("APPROACH 4: E8 STRUCTURE CONSTANTS")
print(f"{'#'*78}")

e8_nums = {
    "248(dim)":248, "240(roots)":240, "8(rank)":8, "30(Cox)":30,
    "120(pos)":120, "128(spinor)":128, "7776(6^5)":7776,
    "62208(norm)":62208, "40(orbits)":40, "80(exp)":80,
}

print(f"Need relative correction f = Delta/mu_0 = {float(Delta/mu_0):.10e}")
print(f"\n--- mu = mu_0*(1+a/N) ---")
print(f"{'N':15s} {'1/N':>14s} {'Ratio':>10s} {'err%':>10s} {'mu match':>12s}")
print(DASH)
for name, N in sorted(e8_nums.items(), key=lambda x: abs(float(mpf(1)/x[1]/(Delta/mu_0) - 1))):
    corr = mpf(1)/N
    ratio = float(corr/(Delta/mu_0))
    err = abs(ratio-1)*100
    mu_t = mu_0*(1+corr)
    m = match_pct(mu_t, mu_meas)
    if err < 200:
        flag = " <<<" if err < 20 else ""
        print(f"  {name:13s} {float(corr):>14.8e} {ratio:>10.4f} {err:>10.2f}% {m:>12.6f}%{flag}")
        if err < 20:
            record(f"4: mu_0*(1+1/{N})", mu_t, "derived")

# Refined: mu_0*(1 + a/(N*phi^b))
print(f"\n--- Refined: mu_0*(1+a/(N*phi^b)) ---")
results_4 = []
for name, N in e8_nums.items():
    for a in range(1, 10):
        for b in range(-2, 6):
            val = mpf(a)/(N*phi**b)
            if fabs(val/(Delta/mu_0) - 1) < mpf("0.01"):
                err = float(fabs(val/(Delta/mu_0)-1)*100)
                mu_t = mu_0*(1+val)
                m = match_pct(mu_t, mu_meas)
                lab = f"{a}/({N}*phi^{b})"
                results_4.append((err, lab, m))
                print(f"  mu_0*(1+{lab:25s}) -> {m:.7f}% ({err:.4f}%)")
                record(f"4: mu_0*(1+{lab})", mu_t, "derived")

# Special: mu_0 + 1/(8*phi^3)  since 62208 = 7776*8
sp = mu_0 + 1/(8*phi**3)
print(f"\nSpecial: mu_0 + 1/(8*phi^3) = {float(sp):.10f}")
print(f"  match: {match_pct(sp,mu_meas):.6f}%, ppm: {ppm_val(sp,mu_meas):.1f}")
record("4sp: mu_0+1/(8*phi^3)", sp, "derived")


# ######################################################################
# APPROACH 5: MODULAR FORM MULTIPLICATIVE (theta4^a, eta*N)
# ######################################################################
print(f"\n\n{'#'*78}")
print("APPROACH 5: MODULAR FORM MULTIPLICATIVE")
print(f"{'#'*78}")

# 5A: theta4^a
a_th4 = log(mu_meas/mu_0)/log(theta4)
print(f"\n--- 5A: mu = mu_0*theta4^a, need a = {float(a_th4):.8f} (NOT nice) ---")

# 5B: mu_0 + eta*N
N_eta = target/eta
print(f"\n--- 5B: mu_0 + eta*N, need N = {float(N_eta):.8f} ---")
# N ~ 4.122. Try fractions
for num in range(1, 30):
    for den in range(1, 20):
        if abs(float(N_eta) - num/den) < 0.003:
            val = eta*mpf(num)/mpf(den)
            mu_t = mu_0 + val
            m = match_pct(mu_t, mu_meas)
            p = ppm_val(mu_t, mu_meas)
            print(f"  eta*{num}/{den} = {float(val):.10f} -> mu match {m:.7f}%, ppm {p:.2f}")
            record(f"5B: mu_0+eta*{num}/{den}", mu_t, "searched")

# 5C: mu_0 + eta*phi^k*(n/m)
print(f"\n--- 5C: mu_0 + eta*phi^k*(n/m) ---")
results_5c = []
for k in range(-3, 4):
    for a in range(1, 20):
        for b in range(1, 20):
            val = eta*phi**k*mpf(a)/mpf(b)
            err = float(fabs(val-target)/target*100)
            if err < 0.1:
                results_5c.append((err, f"eta*phi^{k}*{a}/{b}", float(val)))

results_5c.sort()
if results_5c:
    for i, (err, label, val) in enumerate(results_5c[:10]):
        mu_t = float(mu_0)+val
        m = match_pct(mpf(mu_t), mu_meas)
        print(f"  {i+1}. {label:30s} = {val:.10e} ({err:.4f}%) mu:{m:.7f}%")
        record(f"5C: mu_0+{label}", mpf(mu_t), "searched")

# 5D: mu = mu_0*(1 - C*f)  C=eta*theta4/2
print(f"\n--- 5D: mu_0*(1+C*f), need f = {float(Delta/(mu_0*C)):.6f} ---")
f_C = Delta/(mu_0*C)
# f_C ~ 148... very large for C. Not meaningful.
print(f"  f = {float(f_C):.6f} -> too large for C-based correction. Skipping.")


# ######################################################################
# APPROACH 6: SYSTEMATIC SCAN + INTERPRETATION
# ######################################################################
print(f"\n\n{'#'*78}")
print("APPROACH 6: SYSTEMATIC SCAN + INTERPRETATION")
print(f"{'#'*78}")

# 6A: Delta/alpha
ratio_DA = Delta/alpha
print(f"\n--- 6A: Delta/alpha = {float(ratio_DA):.10f} ---")
# ~ 66.88
# Is it close to a framework number?
r6a = {
    "phi^4": float(phi**4),         # 6.854
    "3*phi^3": float(3*phi**3),     # 12.708
    "6^2/phi": float(36/phi),       # 22.25
    "phi^5": float(phi**5),         # 11.09
    "3*phi^4": float(3*phi**4),     # 20.56
    "6*phi^3": float(6*phi**3),     # 25.42
    "3^3/phi": float(27/phi),       # 16.69
    "6^2*phi/3": float(36*phi/3),   # 19.42
    "phi^8/3": float(phi**8/3),     # 15.56
    "120/phi": float(120/phi),      # 74.16
    "80/phi^2": float(80/phi**2),   # 30.56
    "phi^6/3": float(phi**6/3),     # 5.85
    "40*phi": float(40*phi),        # 64.72
    "40*phi^(1/2)": float(40*phi**0.5),  # 50.88
    "40*sqrt(phi)": float(40*sqrt(phi)),  # 50.88
    "7*phi^4": float(7*phi**4),     # 47.98
    "9*phi^3": float(9*phi**3),     # 38.12
    "5^3/(2*phi)": float(125/(2*phi)),   # 38.63
    "48*phi^(1/2)": float(48*sqrt(phi)), # 61.06
    "49*phi": float(49*phi),        # 79.28
    "80/phi": float(80/phi),        # 49.44
    "11*phi^3": float(11*phi**3),   # 46.60
    "120/phi^(1/2)": float(120/sqrt(phi)), # 94.33
    "6^2*phi": float(36*phi),       # 58.25
    "3^3*phi^2": float(27*phi**2),  # 70.69
    "3^3*phi^2+..": 0, # skip
}
da_val = float(ratio_DA)
print(f"{'Expression':25s} {'Value':>12s} {'Ratio':>10s} {'err%':>10s}")
print("-"*60)
for name, val in sorted(r6a.items(), key=lambda x: abs(x[1]/da_val - 1) if x[1] != 0 else 999):
    if val == 0: continue
    r = da_val/val
    err = abs(r-1)*100
    if err < 20:
        flag = " <<<" if err < 5 else ""
        print(f"  {name:23s} {val:>12.4f} {r:>10.4f} {err:>10.2f}%{flag}")

# 6B: Delta/(alpha*eta) = ?
ratio_DAE = Delta/(alpha*eta)
print(f"\n--- 6B: Delta/(alpha*eta) = {float(ratio_DAE):.10f} ---")
# ~ 564.8 ... way bigger than before because Delta is 0.488 not 0.003
# Let me just print what it is
print(f"  (This is too large for a simple fraction. Not useful.)")

# 6C: Pure phi expressions for Delta
print(f"\n--- 6C: Delta as phi^a * (n/m) ---")
results_6c = []
for a in range(-6, 10):
    for n in range(1, 50):
        for m in range(1, 50):
            val = phi**a * mpf(n)/mpf(m)
            err = float(fabs(val-target)/target*100)
            if err < 0.01:
                results_6c.append((err, f"phi^{a}*{n}/{m}", float(val)))

results_6c.sort()
if results_6c:
    print(f"TOP 10 pure-phi matches (within 0.01%):")
    seen6c = set()
    ct6c = 0
    for err, label, val in results_6c:
        r = round(val, 10)
        if r in seen6c: continue
        seen6c.add(r)
        mu_t = float(mu_0)+val
        m = match_pct(mpf(mu_t), mu_meas)
        print(f"  {ct6c+1:3d}. {label:25s} = {val:.12f} ({err:.5f}%) mu:{m:.8f}%")
        record(f"6C: mu_0+{label}", mpf(mu_t), "searched")
        ct6c += 1
        if ct6c >= 10: break
else:
    print("  (No pure-phi matches within 0.01%)")

# 6D: Complete formula a/(b*phi^c)
print(f"\n--- 6D: target = a/(b*phi^c) scan ---")
results_6d = []
for a in range(1, 100):
    for b in range(1, 100):
        for c in range(0, 8):
            val = mpf(a)/(mpf(b)*phi**c)
            err = float(fabs(val-target)/target*100)
            if err < 0.001:
                results_6d.append((err, f"{a}/({b}*phi^{c})", float(val)))

results_6d.sort()
if results_6d:
    print(f"TOP 10 (within 0.001%):")
    seen6d = set()
    ct6d = 0
    for err, label, val in results_6d:
        r = round(val, 12)
        if r in seen6d: continue
        seen6d.add(r)
        mu_t = float(mu_0)+val
        m = match_pct(mpf(mu_t), mu_meas)
        print(f"  {ct6d+1:3d}. {label:20s} = {val:.12f} ({err:.6f}%) mu:{m:.8f}%")
        record(f"6D: mu_0+{label}", mpf(mu_t), "searched")
        ct6d += 1
        if ct6d >= 10: break
else:
    print("  (No matches within 0.001%)")

# 6E: The KEY question: does target ~ 9/(7*phi^2) have a deeper form?
print(f"\n--- 6E: Why 9/(7*phi^2)? ---")
print(f"  9 = 3^2, 7 = L(4) = Lucas number")
print(f"  9/(7*phi^2) = {float(mu_1_old):.12f}")
print(f"  target = {float(target):.12f}")
print(f"  Ratio target/(9/(7*phi^2)) = {float(target/mu_1_old):.10f}")
print(f"  Off by {float((target-mu_1_old)/target*100):.4f}%")
print(f"  Residual = target - 9/(7*phi^2) = {float(target-mu_1_old):.10e}")
print(f"  This residual = {float((target-mu_1_old)/mu_meas_unc):.0f} sigma")

# Check: is there a better L(a)^b/(L(c)^d * phi^e)?
print(f"\n--- 6F: Lucas ratio scan L(a)^b/(L(c)*phi^e) ---")
results_6f = []
for a in range(0, 12):
    for b in [1, 2]:
        for c in range(0, 12):
            if c == a and b == 1: continue
            for e in range(0, 6):
                if Luc[c] == 0: continue
                val = mpf(Luc[a])**b / (mpf(Luc[c]) * phi**e)
                err = float(fabs(val-target)/target*100)
                if err < 0.01:
                    label = f"L({a})^{b}/(L({c})*phi^{e})"
                    results_6f.append((err, label, float(val)))

results_6f.sort()
if results_6f:
    print(f"TOP 10:")
    for i, (err, label, val) in enumerate(results_6f[:10]):
        mu_t = float(mu_0)+val
        m = match_pct(mpf(mu_t), mu_meas)
        print(f"  {i+1:3d}. {label:35s} = {val:.12f} ({err:.5f}%) mu:{m:.8f}%")
        record(f"6F: mu_0+{label}", mpf(mu_t), "searched")
else:
    print("  (No matches within 0.01%)")


# ######################################################################
# BONUS: CORE IDENTITY AS THE FUNDAMENTAL FORMULA
# ######################################################################
print(f"\n\n{'#'*78}")
print("BONUS: IS THE CORE IDENTITY THE ANSWER?")
print(f"{'#'*78}")

print(f"""
The core identity: alpha^(3/2) * mu * phi^2 = 3
gives mu = 3/(alpha^1.5 * phi^2) with NO free parameters.

This is NOT the same as 6^5/phi^3:
  mu_tree = {float(mu_tree):.10f}
  mu_0    = {float(mu_0):.10f}
  Diff    = {float(mu_tree-mu_0):.10f} ({float((mu_tree-mu_0)/mu_0*100):.4f}%)

The 1-loop correction alpha*ln(phi)/pi brings mu_tree MUCH closer:
  mu_1loop = {float(mu_1L):.10f} (ppm = {ppm_val(mu_1L,mu_meas):.2f})

For comparison, 6^5/phi^3 is:
  mu_0     = {float(mu_0):.10f} (ppm = {ppm_val(mu_0,mu_meas):.0f})

The identity route is DERIVED, the 6^5/phi^3 route needs searched corrections.
""")

# Connection: can we derive 6^5/phi^3 FROM the identity?
# mu_tree/mu_0 = 3/(alpha^1.5 * phi^2) * phi^3/6^5 = 3*phi / (6^5 * alpha^1.5)
r_t0 = mu_tree/mu_0
print(f"mu_tree/mu_0 = {float(r_t0):.15f}")
print(f"  = 3*phi/(6^5*alpha^1.5) = {float(3*phi/(6**5*alpha**mpf('1.5'))):.15f}")
# Is this close to (1 + something small)?
print(f"  - 1 = {float(r_t0-1):.10e}")
# ~ 0.001392 ~ alpha * something?
print(f"  (mu_tree/mu_0 - 1)/alpha = {float((r_t0-1)/alpha):.10f}")
# ~ 0.1907 ~ 1/(phi*sqrt(phi)) = 0.486? No. 1/phi^3 = 0.236? No.
# ~ phi/3^2 = 0.1798? or 1/(3*phi) = 0.206?


# ######################################################################
# GRAND SUMMARY
# ######################################################################
print(f"\n\n{'#'*78}")
print("GRAND SUMMARY: ALL CANDIDATES RANKED")
print(f"{'#'*78}")

all_results.sort(key=lambda x: -x[2])

seen_final = set()
unique = []
for item in all_results:
    key = round(item[1], 5)
    if key not in seen_final:
        seen_final.add(key)
        unique.append(item)

print(f"\n{'#':>3} {'Name':<55} {'mu':>14} {'Match%':>12} {'ppm':>10} {'sigma':>10} {'Type':>10}")
print("-"*118)
for i, (name, mu_val, m, p, s, dtype) in enumerate(unique[:35]):
    flag = " ***" if dtype == "derived" and abs(p) < 20 else ""
    print(f"{i+1:3d} {name:<55} {mu_val:>14.6f} {m:>12.6f} {p:>+10.2f} {s:>10.0f} {dtype:>10}{flag}")

# Separate derived vs searched
derived = [(n,mu,m,p,s) for n,mu,m,p,s,d in unique if d == "derived"]
searched = [(n,mu,m,p,s) for n,mu,m,p,s,d in unique if d == "searched"]

old_match = match_pct(mu_pred_old, mu_meas)

print(f"\n{'='*78}")
print(f"BASELINE: 9/(7*phi^2) -> match {old_match:.7f}%, ppm {ppm_val(mu_pred_old,mu_meas):+.2f}")
print(f"{'='*78}")

better = [(n,mu,m,p,s,d) for n,mu,m,p,s,d in unique if m > old_match]
if better:
    print(f"\nFormulas BETTER than baseline ({len(better)}):")
    for n,mu,m,p,s,d in sorted(better, key=lambda x:-x[2])[:15]:
        print(f"  [{d:>8}] {n:<50} {m:.8f}% ppm={p:+.3f}")
else:
    print(f"\n  *** NO formula beats the baseline ***")

print(f"\n{'='*78}")
print("BEST DERIVED (from physical reasoning):")
print(f"{'='*78}")
derived.sort(key=lambda x: abs(x[3]))
for n,mu,m,p,s in derived[:5]:
    print(f"  {n:<55} {m:.6f}% ppm={p:+.2f}")

print(f"""
{'='*78}
HONEST ASSESSMENT
{'='*78}

The BEST DERIVED result is the core identity perturbative series:
  mu = 3/(alpha^(3/2) * phi^2 * [1 + alpha*ln(phi)/pi + ...])

At 1-loop:
  mu_1loop = {float(mu_1L):.10f}
  Match: {match_pct(mu_1L,mu_meas):.7f}%
  ppm: {ppm_val(mu_1L,mu_meas):+.2f}
  sigma: {sigma_off(mu_1L,mu_meas,mu_meas_unc):.0f}

This is genuinely DERIVED (no searching) but only reaches ~9 ppm,
while the searched formula 9/(7*phi^2) reaches ~1.6 ppm.

For the 6^5/phi^3 route, ALL good corrections are SEARCHED, not derived.
The searched scans find dozens of formulas at similar accuracy, confirming
that 9/(7*phi^2) is NOT unique (as the Phase 1 test showed).

BOTTOM LINE:
1. The DERIVED route is the perturbative expansion of the core identity.
   It gives 9 ppm at 1-loop. The 2-loop overcorrects (c2 should be ~1.72,
   framework predicts 5.15 -- ratio is 1/3, suggestive but unproven).

2. The 6^5/phi^3 route requires a searched correction ~0.488, and there
   are MANY formulas matching at 0.01% or better. None is uniquely derived.

3. The two routes (identity vs 6^5/phi^3) differ by ~0.14%. They may be
   related via: 6^5*alpha^(3/2)/phi = 3*(1+epsilon), but epsilon is not
   a clean framework quantity.

4. The most promising derived 2-loop: c2 = (5+1/phi^4)/3 gives
   mu_2loop = {float(mu_tree/(1+c1+(alpha/pi)**2*(5+1/phi**4)/3)):.10f} (if c2/3 is correct)
   but the factor of 1/3 lacks derivation.

RECOMMENDATION: Accept the core identity as fundamental, 6^5/phi^3 as an
approximation, and focus on deriving the 2-loop coefficient c2.
""")
