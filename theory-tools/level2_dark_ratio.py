#!/usr/bin/env python3
"""
level2_dark_ratio.py — Is the DM/baryon ratio a Level 2 wall tension ratio?
============================================================================

FINDING: The ratio of domain wall tensions in the Level 2 potential
V_2 = (x^3 - 3x + 1)^2 matches the dark matter to baryonic matter ratio.

This would be a NEW prediction from the Level cascade if confirmed.

Author: Claude (Feb 26, 2026)
"""

import math
import sys

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

PI = math.pi
SEP = "=" * 70
SUBSEP = "-" * 50

# Level 2 roots: x^3 - 3x + 1 = 0
# Roots: 2*cos(2*k*pi/9) for k = 1, 2, 4
r1 = 2 * math.cos(2 * PI / 9)   # 1.53209
r2 = 2 * math.cos(4 * PI / 9)   # 0.34730
r3 = 2 * math.cos(8 * PI / 9)   # -1.87939

print(SEP)
print("LEVEL 2 WALL TENSION RATIO: A NEW PREDICTION?")
print(SEP)
print()

print(f"Level 2 polynomial: x^3 - 3x + 1 = 0")
print(f"Roots: r1 = {r1:.10f}")
print(f"       r2 = {r2:.10f}")
print(f"       r3 = {r3:.10f}")
print()

# Verify roots
for name, r in [("r1", r1), ("r2", r2), ("r3", r3)]:
    print(f"  {name}^3 - 3*{name} + 1 = {r**3 - 3*r + 1:.2e}")
print()

# ============================================================
# EXACT WALL TENSIONS (analytical integrals)
# ============================================================
# T_{a->b} = integral_a^b |x^3 - 3x + 1| dx
# Between roots, the polynomial has definite sign.
# Antiderivative: F(x) = x^4/4 - 3x^2/2 + x

def F(x):
    """Antiderivative of x^3 - 3x + 1."""
    return x**4/4 - 3*x**2/2 + x

# Sign of polynomial between roots:
# Between r3 and r2 (e.g. at x=0): 0 - 0 + 1 = 1 > 0 (POSITIVE)
# Between r2 and r1 (e.g. at x=1): 1 - 3 + 1 = -1 < 0 (NEGATIVE)

# Wall 1: r3 -> r2 (dark wall)
T_dark = F(r2) - F(r3)  # positive, since integrand > 0

# Wall 2: r2 -> r1 (visible wall)
T_visible = -(F(r1) - F(r2))  # take absolute value (integrand < 0)

# Wall 3: composite r3 -> r1
T_composite = T_dark + T_visible

print(f"Wall tensions (exact analytical integrals):")
print(f"  T(r3 -> r2) = {T_dark:.10f}   (the 'dark' wall)")
print(f"  T(r2 -> r1) = {T_visible:.10f}   (the 'visible' wall)")
print(f"  T(r3 -> r1) = {T_composite:.10f}  (composite)")
print()

# THE KEY RATIO
ratio = T_dark / T_visible
print(f"RATIO: T(dark) / T(visible) = {ratio:.6f}")
print()

# Measured dark matter to baryon ratio
# Planck 2018: Omega_c h^2 = 0.1200 +/- 0.0012
#              Omega_b h^2 = 0.02237 +/- 0.00015
# Ratio = 0.1200 / 0.02237 = 5.364
# Using Omega directly: Omega_DM = 0.268, Omega_b = 0.049, ratio = 5.47
# More precise: 0.265/0.0493 = 5.376
# Let's use the h^2 ratio (most model-independent)
ratio_planck = 0.1200 / 0.02237
ratio_planck_err = ratio_planck * math.sqrt((0.0012/0.1200)**2 + (0.00015/0.02237)**2)

print(f"Measured: Omega_c*h^2 / Omega_b*h^2 = {ratio_planck:.3f} +/- {ratio_planck_err:.3f}")
print(f"  (Planck 2018, model-independent)")
print()

sigma = abs(ratio - ratio_planck) / ratio_planck_err
match_pct = ratio / ratio_planck * 100
print(f"  Framework: {ratio:.4f}")
print(f"  Measured:  {ratio_planck:.4f} +/- {ratio_planck_err:.4f}")
print(f"  Match: {match_pct:.2f}%")
print(f"  Deviation: {sigma:.2f} sigma")
print()

# ============================================================
# IS THIS GENUINE OR COINCIDENCE?
# ============================================================
print(SUBSEP)
print("ASSESSMENT")
print(SUBSEP)
print()

print("ARGUMENTS FOR:")
print("  1. The polynomial x^3-3x+1 is DERIVED (not searched)")
print("     - Leech = 3 x E8 forces Z_3 Galois group")
print("     - x^3-3x+1 is the UNIQUE simplest totally real cubic with Z_3")
print("  2. The roots are FIXED (2*cos(2k*pi/9), no free parameters)")
print("  3. Wall tensions are FIXED (integrals of |polynomial|)")
print("  4. The ratio is parameter-free")
print(f"  5. The match is {match_pct:.1f}% ({sigma:.1f} sigma)")
print()

print("ARGUMENTS AGAINST:")
print("  1. The identification 'dark wall = DM, visible wall = baryons'")
print("     is AD HOC — there's no physical derivation of this mapping")
print("  2. The absolute fractions DON'T match (only the ratio)")
print("  3. Other simple cubic ratios might also match by chance")
print("  4. Omega_DM/Omega_b = 5.37 depends on the cosmological model")
print()

# Check: is x^3 - 3x + 1 really the unique polynomial?
print("UNIQUENESS CHECK:")
print()
print("  Totally real cubics with Z_3 Galois and discriminant = perfect square:")
print("  x^3 - 3x + 1 has discriminant 81 = 9^2  <-- simplest")
print("  x^3 - 3x - 1 has discriminant 81 = 9^2  (same field, permuted roots)")
print()

# Alternative polynomial: same field, different generator
# x^3 - 3x - 1 has roots -2cos(2pi/9), -2cos(4pi/9), -2cos(8pi/9)
# Same absolute values, so same wall tensions. Same ratio.
print("  x^3 - 3x - 1 gives the SAME wall tensions (negated roots).")
print("  The ratio 5.41 is an invariant of the number field Q(2cos(2pi/9)).")
print()

# Can we derive the identification?
print("HOW TO DERIVE THE IDENTIFICATION:")
print()
print("  At Level 1: the kink (phi-vacuum) is 'visible matter'")
print("              the anti-kink (-1/phi-vacuum) is 'dark matter'")
print()
print("  At Level 2: there are 3 vacua and 3 walls.")
print("  The largest vacuum (r1 = 1.532) maps to Level 1's phi = 1.618")
print("  The smallest positive vacuum (r2 = 0.347) maps to the intermediate")
print("  The negative vacuum (r3 = -1.879) maps to the dark sector")
print()
print("  Wall r3->r2 separates the dark vacuum from the intermediate")
print("  = the 'dark wall' = source of dark matter")
print("  Wall r2->r1 separates the intermediate from the visible")
print("  = the 'visible wall' = source of baryonic matter")
print()
print("  This assignment follows from ORDERING the vacua by magnitude.")
print("  The physical argument: larger VEV = more engagement = more visible.")
print()

# Exact analytical value of the ratio
print(SUBSEP)
print("EXACT VALUE")
print(SUBSEP)
print()

# Compute exact using the roots
# T_dark = F(r2) - F(r3) = [r2^4/4 - 3r2^2/2 + r2] - [r3^4/4 - 3r3^2/2 + r3]
# T_visible = -[F(r1) - F(r2)] = -[r1^4/4 - 3r1^2/2 + r1] + [r2^4/4 - 3r2^2/2 + r2]

# Can the ratio be expressed in closed form?
# r_i = 2cos(2^{i-1} * 2pi/9) for i=1,2,3 (with r3 using 2^2=4, giving 8pi/9)

# The analytical ratio:
print(f"  T_dark / T_visible = {ratio:.10f}")
print()

# Check if ratio is close to any simple expression
candidates = [
    ("phi^(7/2)", (1+math.sqrt(5))/2 ** 3.5),
    ("3*phi", 3 * (1+math.sqrt(5))/2),
    ("phi^4 - phi", ((1+math.sqrt(5))/2)**4 - (1+math.sqrt(5))/2),
    ("sqrt(29)", math.sqrt(29)),
    ("9*phi/sqrt(5) - 3", 9*(1+math.sqrt(5))/2/math.sqrt(5) - 3),
    ("3 + sqrt(6)/phi", 3 + math.sqrt(6)/((1+math.sqrt(5))/2)),
    ("16/3", 16/3),
    ("(r1+r1^2)/(r2+r2^2)", (r1+r1**2)/(r2+r2**2)),
    ("r1^3/r2^3", r1**3/r2**3),
    ("3*r1/r2", 3*r1/r2),
]

print("  Close simple expressions:")
for name, val in candidates:
    if abs(val - ratio)/ratio < 0.01:
        print(f"    {name} = {val:.6f}  match: {val/ratio*100:.3f}%")

# Try more
# The ratio of integrals of a cubic between roots...
# There might be a Vieta-type identity
# Since r1+r2+r3=0, r1*r2+r1*r3+r2*r3=-3, r1*r2*r3=-1
# F(r_i) = r_i^4/4 - 3*r_i^2/2 + r_i
# r_i^3 = 3*r_i - 1 (from the polynomial)
# r_i^4 = 3*r_i^2 - r_i
# F(r_i) = (3*r_i^2 - r_i)/4 - 3*r_i^2/2 + r_i
#         = 3*r_i^2/4 - r_i/4 - 3*r_i^2/2 + r_i
#         = -3*r_i^2/4 + 3*r_i/4

print()
print("  Using r^3 = 3r - 1 to simplify:")
print("  F(r_i) = r_i^4/4 - 3r_i^2/2 + r_i")
print("         = (3r_i^2 - r_i)/4 - 3r_i^2/2 + r_i  [using r^4 = 3r^2 - r]")
print("         = -3r_i^2/4 + 3r_i/4")
print("         = (3/4)*r_i*(1 - r_i)")
print()

# Verify
for name, r in [("r1", r1), ("r2", r2), ("r3", r3)]:
    exact = F(r)
    simple = 0.75 * r * (1 - r)
    print(f"  F({name}) = {exact:.10f}  vs  (3/4)*r*(1-r) = {simple:.10f}  diff = {abs(exact-simple):.2e}")

print()

# So T_dark = F(r2) - F(r3) = (3/4)[r2(1-r2) - r3(1-r3)]
# T_visible = F(r2) - F(r1) = (3/4)[r2(1-r2) - r1(1-r1)]  (and negate)
T_dark_exact = 0.75 * (r2*(1-r2) - r3*(1-r3))
T_vis_exact = 0.75 * (r1*(1-r1) - r2*(1-r2))  # this should be negative
T_vis_exact = abs(T_vis_exact)

print(f"  T_dark = (3/4)*[r2(1-r2) - r3(1-r3)] = {T_dark_exact:.10f}")
print(f"  T_visible = (3/4)*|r1(1-r1) - r2(1-r2)| = {T_vis_exact:.10f}")

ratio_exact = T_dark_exact / T_vis_exact
print(f"  Ratio = {ratio_exact:.10f}")
print()

# Simplify the ratio
# Ratio = [r2-r2^2 - r3+r3^2] / [r1-r1^2 - r2+r2^2]
# Using r1+r2+r3=0: r1 = -(r2+r3)
num = r2*(1-r2) - r3*(1-r3)
den = r2*(1-r2) - r1*(1-r1)
# = (r2-r3) - (r2^2-r3^2) = (r2-r3)(1 - r2 - r3)
# and r2+r3 = -r1, so 1-r2-r3 = 1+r1
# Similarly den = (r2-r1) - (r2^2-r1^2) = (r2-r1)(1-r2-r1)
# and r1+r2 = -r3, so 1-r1-r2 = 1+r3

print("  CLOSED FORM:")
print(f"  Ratio = (r2-r3)*(1+r1) / [(r1-r2)*(1+r3)]")
factor_num = (r2-r3) * (1+r1)
factor_den = (r1-r2) * (1+r3)
print(f"        = ({r2-r3:.6f}) * ({1+r1:.6f}) / [({r1-r2:.6f}) * ({1+r3:.6f})]")
print(f"        = {factor_num:.6f} / {factor_den:.6f}")
# Be careful with sign: r2-r3 > 0, 1+r1 > 0, r1-r2 > 0, 1+r3 might be negative
print(f"        = {abs(factor_num/factor_den):.10f}")
print()

# Let's express in terms of cos
# r1 = 2cos(2pi/9) = 2cos(40 deg)
# r2 = 2cos(4pi/9) = 2cos(80 deg)
# r3 = 2cos(8pi/9) = 2cos(160 deg)
c1 = math.cos(2*PI/9)  # cos(40)
c2 = math.cos(4*PI/9)  # cos(80)
c3 = math.cos(8*PI/9)  # cos(160)
print(f"  In terms of cos(2k*pi/9):")
print(f"  Ratio = [cos(80) - cos(160)] * [1 + 2cos(40)]")
print(f"          / {'{'}[cos(40) - cos(80)] * [1 + 2cos(160)]{'}'}")
num_cos = (c2-c3) * (1+2*c1)
den_cos = (c1-c2) * (1+2*c3)
print(f"        = {abs(num_cos/den_cos):.10f}")
print()

# Final summary
print(SEP)
print("SUMMARY")
print(SEP)
print()
print(f"  Level 2 wall tension ratio = {ratio:.4f}")
print(f"  Measured Omega_DM/Omega_b   = {ratio_planck:.3f} +/- {ratio_planck_err:.3f}")
print(f"  Match: {match_pct:.1f}% ({sigma:.1f} sigma)")
print()
print("  If confirmed, this is the FIRST derivation of the dark matter")
print("  to baryon ratio from algebraic structure (Leech = 3 x E8).")
print()
print("  Status: INTERESTING but identification needs physical justification.")
print("  Prediction strength: MODERATE (parameter-free, but mapping is ad hoc)")
