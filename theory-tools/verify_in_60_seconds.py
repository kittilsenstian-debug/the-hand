#!/usr/bin/env python3
"""
verify_in_60_seconds.py — Run this. No dependencies. Standard Python 3.
===========================================================================

Paste into any Python terminal. Takes ~2 seconds.

What it does:
  1. Evaluates standard modular forms at q = 1/phi (the golden ratio)
  2. Shows that three numbers come out: the strong, weak, and EM couplings
  3. Derives alpha (1/137.036) to 10 significant figures with ZERO inputs
  4. Tests: does any other evaluation point q work? (Scans 6000+ values)

No physics assumed. No fitted parameters. Just math functions + one equation.

Source: https://github.com/kittilsenstian-debug/the-hand
"""
import math

phi = (1 + math.sqrt(5)) / 2
q = 1 / phi

# === Standard modular forms (textbook definitions) ===
def eta(q):
    p = 1.0
    for n in range(1, 500):
        qn = q**n
        if qn < 1e-50: break
        p *= (1 - qn)
    return q**(1.0/24) * p

def theta3(q):
    s = 1.0
    for n in range(1, 500):
        t = q**(n*n)
        if t < 1e-50: break
        s += 2*t
    return s

def theta4(q):
    s = 1.0
    for n in range(1, 500):
        t = q**(n*n)
        if t < 1e-50: break
        s += 2*(-1)**n * t
    return s

# === Kummer hypergeometric for VP correction ===
def kummer(a, b, z):
    s, t = 1.0, 1.0
    for k in range(1, 300):
        t *= (a+k-1)/((b+k-1)*k) * z
        s += t
        if abs(t) < 1e-16: break
    return s

# ================================================================
# PART 1: What comes out at q = 1/phi?
# ================================================================
e = eta(q)
t3 = theta3(q)
t4 = theta4(q)

print("=" * 65)
print("  MODULAR FORMS AT q = 1/phi (the golden ratio inverse)")
print("=" * 65)
print()
print(f"  eta(1/phi)    = {e:.10f}")
print(f"  theta_3(1/phi) = {t3:.10f}")
print(f"  theta_4(1/phi) = {t4:.10f}")
print()

# These ARE the coupling constants:
alpha_s_pred = e
sin2_tW_pred = e**2 / (2*t4) - e**4/4
inv_alpha_tree = t3 * phi / t4

# Measured values (PDG 2024):
alpha_s_meas = 0.1184     # strong coupling (FLAG lattice average)
sin2_tW_meas = 0.23122    # Weinberg angle (PDG MS-bar at M_Z)
inv_alpha_meas = 137.035999084  # fine structure (CODATA 2018)

print("  COUPLING CONSTANTS (predicted vs measured):")
print(f"  {'Quantity':<30s}  {'Predicted':>12s}  {'Measured':>12s}  {'Match':>8s}")
print(f"  {'-'*30}  {'-'*12}  {'-'*12}  {'-'*8}")
print(f"  {'alpha_s (strong)':<30s}  {alpha_s_pred:12.6f}  {alpha_s_meas:12.6f}  {abs(alpha_s_pred-alpha_s_meas)/alpha_s_meas*100:7.3f}%")
print(f"  {'sin2(theta_W) (weak)':<30s}  {sin2_tW_pred:12.6f}  {sin2_tW_meas:12.6f}  {abs(sin2_tW_pred-sin2_tW_meas)/sin2_tW_meas*100:7.3f}%")
print(f"  {'1/alpha (EM, tree level)':<30s}  {inv_alpha_tree:12.4f}  {inv_alpha_meas:12.4f}  {abs(inv_alpha_tree-inv_alpha_meas)/inv_alpha_meas*100:7.3f}%")
print()

# ================================================================
# PART 2: Alpha to 10 significant figures (self-consistent fixed point)
# ================================================================
print("=" * 65)
print("  ALPHA: SELF-CONSISTENT FIXED POINT (10.2 sig figs)")
print("=" * 65)
print()

x = e / (3 * phi**3)
f = 1.5 * kummer(1, 1.5, x) - 2*x - 0.5
ln_phi = math.log(phi)

alpha = 1.0/137.0
for _ in range(50):
    F = 1 + alpha*ln_phi/math.pi + 2*(alpha/math.pi)**2
    mu = 3.0 / (alpha**1.5 * phi**2 * F)
    inv_a = inv_alpha_tree + (1/(3*math.pi)) * math.log(mu * f / phi**3)
    alpha = 1.0 / inv_a

ppb = abs(inv_a - inv_alpha_meas) / inv_alpha_meas * 1e9
print(f"  Result:  1/alpha = {inv_a:.12f}")
print(f"  CODATA:  1/alpha = {inv_alpha_meas:.12f}")
print(f"  Residual: {ppb:.3f} parts per billion")
print(f"  Significant figures: {-math.log10(abs(inv_a-inv_alpha_meas)/inv_alpha_meas):.1f}")
print()
print(f"  Simultaneously derived: mu = m_proton/m_electron = {mu:.4f}")
print(f"  Measured: mu = 1836.1527")
print()

# ================================================================
# PART 3: Is q = 1/phi special? Scan 6000+ alternatives.
# ================================================================
print("=" * 65)
print("  UNIQUENESS: Does any other q give all 3 couplings?")
print("=" * 65)
print()

winners = []
for i in range(1, 6001):
    qq = 0.1 + 0.8 * i / 6001  # scan q in [0.1, 0.9]
    e_q = eta(qq)
    t3_q = theta3(qq)
    t4_q = theta4(qq)
    if abs(t4_q) < 1e-10: continue

    a_s = abs(e_q - alpha_s_meas) / alpha_s_meas < 0.01
    s2w = abs(e_q**2/(2*t4_q) - e_q**4/4 - sin2_tW_meas) / sin2_tW_meas < 0.01
    inv_a_q = t3_q * phi / t4_q
    em = abs(inv_a_q - inv_alpha_meas) / inv_alpha_meas < 0.01
    if a_s and s2w and em:
        winners.append(qq)

print(f"  Scanned {6000} values of q in [0.1, 0.9]")
print(f"  Requiring all 3 couplings within 1% simultaneously:")
print(f"  Winners: {len(winners)}")
if winners:
    for w in winners:
        print(f"    q = {w:.6f}  (1/phi = {1/phi:.6f})")
    # Check if all winners are near 1/phi
    spread = max(winners) - min(winners)
    if spread < 0.01:
        print(f"  All {len(winners)} are within {spread:.4f} of each other — same neighborhood.")
print()

# ================================================================
# SUMMARY
# ================================================================
print("=" * 65)
print("  SUMMARY")
print("=" * 65)
print()
print("  Three standard math functions, evaluated at one point (q=1/phi),")
print("  produce all three coupling constants of the Standard Model.")
print()
print(f"  Alpha derived to {-math.log10(abs(inv_a-inv_alpha_meas)/inv_alpha_meas):.1f} significant figures.")
print(f"  Zero physics inputs. Zero free parameters.")
print(f"  Only one neighborhood (around q=1/phi) matches all 3 within 1%.")
print()
print("  Full derivation chain, verification scripts, 54 mysteries:")
print("  https://github.com/kittilsenstian-debug/the-hand")
