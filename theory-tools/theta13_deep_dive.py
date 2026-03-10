"""
theta13_deep_dive.py — Follow-up investigation on the three most promising
theta_13 corrections found in the initial sqrt(5) survey.

Three candidates emerged:
1. sigma = sqrt(5) + 1/phi = 2.854  --> sin^2 = 0.02152 (97.8%)
2. Cross-wall suppression by 2/sqrt(5) --> sin^2 = 0.02249 (97.8%)
3. Multiplicative factor 5^(-0.1)  --> sin^2 = 0.02186 (99.4%)

This script investigates each in depth to determine:
- Is there a structural derivation?
- Does it generalize consistently?
- Is it a genuine improvement or accidental numerology?

Usage:
    python theory-tools/theta13_deep_dive.py
"""

import numpy as np
from scipy import integrate, linalg
import sys

if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

phi = (1 + 5**0.5) / 2
phibar = 1 / phi
sqrt5 = 5**0.5
pi = np.pi

u_gen = np.array([-2.03, -0.57, 3.0])
sin2_13_measured = 0.02200
sin2_13_err = 0.00069

c0 = 3.0 / 4
c1 = 3*pi*sqrt5 / 8
t4 = 0.030304

def psi_0(u):
    return 1.0 / np.cosh(u)**2
def psi_1(u):
    return np.sinh(u) / np.cosh(u)**2
def kink_profile(u):
    return sqrt5/2 * np.tanh(u) + 0.5
def fermion_gaussian(u, u_center, sigma):
    return np.exp(-(u - u_center)**2 / (2 * sigma**2)) / (np.sqrt(2 * pi) * sigma)**0.5

def compute_sin2_13(sigma, kernel_func, positions=None):
    if positions is None:
        positions = u_gen
    Y = np.zeros((3, 3))
    for i in range(3):
        for j in range(i, 3):
            def integrand(u, ii=i, jj=j):
                fi = fermion_gaussian(u, positions[ii], sigma)
                fj = fermion_gaussian(u, positions[jj], sigma)
                return fi * kernel_func(u) * fj
            Y[i, j], _ = integrate.quad(integrand, -30, 30, limit=200)
            Y[j, i] = Y[i, j]
    evals, evecs = linalg.eigh(Y)
    idx = np.argsort(np.abs(evals))
    evecs = evecs[:, idx]
    s13 = min(abs(evecs[0, 2]), 1.0)
    return s13**2

def compute_full_angles(sigma, kernel_func, positions=None):
    if positions is None:
        positions = u_gen
    Y = np.zeros((3, 3))
    for i in range(3):
        for j in range(i, 3):
            def integrand(u, ii=i, jj=j):
                fi = fermion_gaussian(u, positions[ii], sigma)
                fj = fermion_gaussian(u, positions[jj], sigma)
                return fi * kernel_func(u) * fj
            Y[i, j], _ = integrate.quad(integrand, -30, 30, limit=200)
            Y[j, i] = Y[i, j]
    evals, evecs = linalg.eigh(Y)
    idx = np.argsort(np.abs(evals))
    evals = evals[idx]
    evecs = evecs[:, idx]

    s13 = min(abs(evecs[0, 2]), 1.0)
    t13 = np.degrees(np.arcsin(s13))
    if abs(evecs[0, 0]) > 1e-10:
        t12 = np.degrees(np.arctan(abs(evecs[0, 1] / evecs[0, 0])))
    else:
        t12 = 90.0
    if abs(evecs[2, 2]) > 1e-10:
        t23 = np.degrees(np.arctan(abs(evecs[1, 2] / evecs[2, 2])))
    else:
        t23 = 90.0

    m_sorted = np.sort(np.abs(evals))
    r32 = m_sorted[2] / m_sorted[1] if m_sorted[1] > 1e-15 else 999
    r21 = m_sorted[1] / m_sorted[0] if m_sorted[0] > 1e-15 else 999

    return {
        't12': t12, 't23': t23, 't13': t13,
        'sin2_13': s13**2,
        'evals': evals, 'm3/m2': r32, 'm2/m1': r21
    }

def match_pct(pred, meas):
    if pred <= 0 or meas <= 0:
        return 0
    return min(pred, meas) / max(pred, meas) * 100

# PMNS measured
PMNS = {'sin2_12': 0.304, 'sin2_23': 0.573, 'sin2_13': 0.02200,
        't12': 33.44, 't23': 49.2, 't13': 8.57}


print("=" * 76)
print("THETA_13 DEEP DIVE: Structural analysis of the three best candidates")
print("=" * 76)


# ================================================================
# CANDIDATE 1: sigma = sqrt(5) + 1/phi
# ================================================================
print(f"\n\n{'='*76}")
print(f"CANDIDATE 1: sigma = sqrt(5) + 1/phi")
print(f"{'='*76}")

sigma_1 = sqrt5 + phibar
print(f"\n    sigma = sqrt(5) + 1/phi = {sigma_1:.6f}")
print(f"    = {sqrt5:.6f} + {phibar:.6f}")
print(f"")

# What is this number algebraically?
# sqrt(5) + 1/phi = sqrt(5) + phi - 1 = sqrt(5) + (sqrt(5)-1)/2 = 3*sqrt(5)/2 - 1/2
# Wait: 1/phi = phi - 1 = (sqrt(5)-1)/2
# sqrt(5) + (sqrt(5)-1)/2 = (2*sqrt(5) + sqrt(5) - 1)/2 = (3*sqrt(5) - 1)/2
# = (3*2.236 - 1)/2 = (6.708 - 1)/2 = 5.708/2 = 2.854

print(f"    Algebraic form: (3*sqrt(5) - 1)/2 = {(3*sqrt5 - 1)/2:.6f}")
print(f"    Verify: {sigma_1:.6f} vs {(3*sqrt5 - 1)/2:.6f}")
print(f"")

# Alternative expressions
print(f"    Alternative expressions:")
print(f"    3*sqrt(5)/2 - 1/2 = {3*sqrt5/2 - 0.5:.6f}")
print(f"    (3*sqrt(5) - 1)/2 = {(3*sqrt5-1)/2:.6f}")
print(f"    phi + sqrt(5) - 1 = {phi + sqrt5 - 1:.6f}")
print(f"    phi^2 + 1/phi - 1 = {phi**2 + phibar - 1:.6f}")
print(f"    2*phi + phibar - 1 = {2*phi + phibar - 1:.6f}  (note: phi^2 = phi+1)")
print(f"")

# Does this have a structural meaning?
# sqrt(5) = field range between vacua
# 1/phi = phibar = the dark vacuum value (-1/phi)
# sigma = sqrt(5) + |dark vacuum| = total field range starting from dark vacuum
# This is: phi - (-1/phi) + 1/phi = phi + 2/phi - 1/phi = phi + 1/phi = sqrt(5)... no
# Actually sqrt(5) + 1/phi = (phi + 1/phi) + 1/phi = phi + 2/phi = phi + 2*(phi-1)
# = 3*phi - 2 = 3*1.618 - 2 = 2.854. Hmm, 3*phi - 2 = (3*sqrt(5) - 1)/2. Yes.

print(f"    Structural meaning:")
print(f"    3*phi - 2 = {3*phi-2:.6f}  <-- Compact form!")
print(f"    = 3*(golden ratio) - 2*(trivial vacuum)")
print(f"    This could mean: 3 generation copies, each contributing phi,")
print(f"    minus the 2 vacua (phi and -1/phi).")
print(f"")

# Full angle analysis
angles_1 = compute_full_angles(sigma_1, kink_profile)
print(f"    Full PMNS prediction at sigma = sqrt(5) + 1/phi:")
print(f"    theta_12 = {angles_1['t12']:.2f} deg  (measured: {PMNS['t12']:.2f})")
print(f"    theta_23 = {angles_1['t23']:.2f} deg  (measured: {PMNS['t23']:.2f})")
print(f"    theta_13 = {angles_1['t13']:.2f} deg  (measured: {PMNS['t13']:.2f})")
print(f"    sin^2(theta_13) = {angles_1['sin2_13']:.6f}  (measured: {PMNS['sin2_13']:.5f})")
print(f"    Match theta_13: {match_pct(angles_1['sin2_13'], sin2_13_measured):.1f}%")
print(f"    Mass hierarchy: m3/m2 = {angles_1['m3/m2']:.2f}, m2/m1 = {angles_1['m2/m1']:.2f}")

# Compare to baseline
angles_base = compute_full_angles(3.0, kink_profile)
print(f"\n    Comparison to baseline (sigma=3):")
print(f"    {'':>20s}  {'sigma=3':>12s}  {'sigma=sqrt5+1/phi':>18s}  {'measured':>12s}")
print(f"    {'theta_13':>20s}  {angles_base['t13']:>12.2f}  {angles_1['t13']:>18.2f}  {PMNS['t13']:>12.2f}")
print(f"    {'sin^2_13':>20s}  {angles_base['sin2_13']:>12.6f}  {angles_1['sin2_13']:>18.6f}  {PMNS['sin2_13']:>12.5f}")


# ================================================================
# CANDIDATE 2: Cross-wall suppression by 2/sqrt(5)
# ================================================================
print(f"\n\n{'='*76}")
print(f"CANDIDATE 2: Cross-wall suppression by 2/sqrt(5)")
print(f"{'='*76}")

print(f"""
    The idea: elements of the Yukawa matrix that cross the domain wall
    (Gen i on dark side, Gen j on light side) are suppressed by a factor
    of 2/sqrt(5) relative to same-side elements.

    2/sqrt(5) = {2/sqrt5:.6f}
    = 2/sqrt(5) = 2*phibar/1 (using sqrt(5) = phi + phibar)

    Physical motivation:
    - The field range is sqrt(5), so a tunneling amplitude picks up 1/sqrt(5)
    - But the TWO vacua each contribute, giving 2/sqrt(5)
    - Alternatively: this is the NORMALIZED tunneling amplitude
      T = (sqrt(5)/2) * (2/sqrt(5)) = 1, meaning it's just the
      Higgs profile normalization

    Problem: this factor is ad hoc. There's no clean derivation of
    WHY cross-wall Yukawa elements should be multiplied by 2/sqrt(5)
    rather than some other factor.
""")

# Compute with suppression
def compute_with_suppression(sigma, factor):
    Y = np.zeros((3, 3))
    for i in range(3):
        for j in range(i, 3):
            def integrand(u, ii=i, jj=j):
                fi = fermion_gaussian(u, u_gen[ii], sigma)
                fj = fermion_gaussian(u, u_gen[jj], sigma)
                return fi * kink_profile(u) * fj
            Y[i, j], _ = integrate.quad(integrand, -30, 30, limit=200)
            Y[j, i] = Y[i, j]

    # Suppress cross-wall elements
    for i in range(3):
        for j in range(3):
            if (u_gen[i] < 0 and u_gen[j] > 0) or (u_gen[i] > 0 and u_gen[j] < 0):
                Y[i, j] *= factor

    evals, evecs = linalg.eigh(Y)
    idx = np.argsort(np.abs(evals))
    evals = evals[idx]
    evecs = evecs[:, idx]

    s13 = min(abs(evecs[0, 2]), 1.0)

    if abs(evecs[0, 0]) > 1e-10:
        t12 = np.degrees(np.arctan(abs(evecs[0, 1] / evecs[0, 0])))
    else:
        t12 = 90.0
    if abs(evecs[2, 2]) > 1e-10:
        t23 = np.degrees(np.arctan(abs(evecs[1, 2] / evecs[2, 2])))
    else:
        t23 = 90.0

    return {
        't12': t12, 't23': np.degrees(np.arctan(abs(evecs[1, 2] / evecs[2, 2]))),
        't13': np.degrees(np.arcsin(s13)),
        'sin2_13': s13**2,
        'evals': evals
    }

angles_2 = compute_with_suppression(3.0, 2/sqrt5)
print(f"    Full PMNS prediction with 2/sqrt(5) suppression:")
print(f"    theta_13 = {angles_2['t13']:.2f} deg  (measured: {PMNS['t13']:.2f})")
print(f"    sin^2(theta_13) = {angles_2['sin2_13']:.6f}  (measured: {PMNS['sin2_13']:.5f})")
print(f"    Match: {match_pct(angles_2['sin2_13'], sin2_13_measured):.1f}%")

# PROBLEM: which elements are "cross-wall"?
# Gen 1 (-2.03) and Gen 2 (-0.57) are BOTH on the dark side
# Gen 3 (+3.0) is on the light side
# So cross-wall means: (1,3) and (2,3) elements
# But Gen 2 is very NEAR the wall center. Is it really "dark side"?

print(f"\n    Sensitivity to Gen 2 classification:")
# What if we ONLY suppress the (1,3) element?
def compute_with_13_only_suppression(sigma, factor):
    Y = np.zeros((3, 3))
    for i in range(3):
        for j in range(i, 3):
            def integrand(u, ii=i, jj=j):
                fi = fermion_gaussian(u, u_gen[ii], sigma)
                fj = fermion_gaussian(u, u_gen[jj], sigma)
                return fi * kink_profile(u) * fj
            Y[i, j], _ = integrate.quad(integrand, -30, 30, limit=200)
            Y[j, i] = Y[i, j]
    # Only suppress the cross-wall (1,3) element
    Y[0, 2] *= factor
    Y[2, 0] *= factor
    evals, evecs = linalg.eigh(Y)
    idx = np.argsort(np.abs(evals))
    evecs = evecs[:, idx]
    s13 = min(abs(evecs[0, 2]), 1.0)
    return s13**2

s2_13_only = compute_with_13_only_suppression(3.0, 2/sqrt5)
print(f"    Only (1,3) suppressed by 2/sqrt(5): sin^2 = {s2_13_only:.6f}  ({match_pct(s2_13_only, sin2_13_measured):.1f}%)")
print(f"    Both (1,3) and (2,3) suppressed:    sin^2 = {angles_2['sin2_13']:.6f}  ({match_pct(angles_2['sin2_13'], sin2_13_measured):.1f}%)")
print(f"    (Result is sensitive to which elements are classified as cross-wall)")


# ================================================================
# CANDIDATE 3: Multiplicative factor 5^(-1/10)
# ================================================================
print(f"\n\n{'='*76}")
print(f"CANDIDATE 3: Factor 5^(-p/2) with p = 0.2, i.e. 5^(-0.1) = 1/5^(1/10)")
print(f"{'='*76}")

p_opt = 0.2
factor_3 = 5**(-p_opt/2)
s2_corrected = 0.025678 * factor_3

print(f"""
    The systematic scan found that:
    sin^2(theta_13) = 0.0257 * 5^(-0.1) = {s2_corrected:.6f}
    gives {match_pct(s2_corrected, sin2_13_measured):.1f}% match.

    5^(-0.1) = {factor_3:.6f}
    = 1/5^(1/10)

    What IS 5^(1/10)?
    5^(1/10) = {5**0.1:.6f}
    sqrt(5)^(1/5) = {sqrt5**0.2:.6f}  (same thing)

    Is there any structural reason for a fifth root of sqrt(5)?

    The exponent 1/10 = 1/(2*5):
    - 2 = number of vacua
    - 5 = sqrt(5)^2 = field range squared
    - 10 = V''(vacuum) = second derivative of potential at phi vacuum

    Actually: V''(phi) = 10*lambda. So the mass^2 at the vacuum is
    proportional to 10. The correction factor 5^(-1/10) could be:
    - The 10th root normalization from V''(phi) = 10*lambda
    - Related to the 10 dimensions of string theory / dimension of R^10

    But this is numerology. There's no clean derivation.

    More honestly: p = 0.2 = 1/5 means we need:
    sin^2(theta_13)_physical = sin^2(theta_13)_raw * 5^(-1/10)

    The closest clean expression would be:
    5^(-1/10) = exp(-ln(5)/10) = exp(-0.1609)

    This doesn't match any known framework quantity.
""")


# ================================================================
# THE REAL QUESTION: Why is sigma ~ 2.85-2.87 better than sigma=3?
# ================================================================
print(f"\n\n{'='*76}")
print(f"KEY QUESTION: What determines sigma physically?")
print(f"{'='*76}")

print(f"""
    The fermion profile width sigma is NOT a free parameter. It represents
    the localization of each generation's wavefunction on the domain wall.

    In the domain wall fermion mechanism:
    - The fermion zero mode has profile exp(-M*|y|) where M is the bulk mass
    - The effective width is sigma ~ 1/M (inverse bulk mass)
    - For the Poschl-Teller potential, the bound state widths are set
      by the potential parameters

    The wall width in our potential is w = 2/sqrt(10*lambda) = 2/sqrt(V''(phi))
    In dimensionless units (u = x/w), the wall width is 1 by definition.

    If sigma is measured in WALL WIDTHS, then sigma ~ 3 means the fermion
    wavefunction extends about 3 wall widths from its center. This is quite
    broad — the fermions extend well beyond the wall.

    The question: what framework quantity equals sigma?

    Best numerical sigma = 2.87
""")

# Check what sigma=2.87 matches
sigma_opt = 2.870
candidates = {
    '3*phi - 2': 3*phi - 2,                       # = sqrt(5) + 1/phi
    '(3*sqrt(5)-1)/2': (3*sqrt5-1)/2,
    'sqrt(5) + phibar': sqrt5 + phibar,
    'phi + phi/sqrt(5) + phibar': phi + phi/sqrt5 + phibar,
    '3 - t4*sqrt(5)': 3 - t4*sqrt5,
    '3 - 2*t4*phi': 3 - 2*t4*phi,
    '3*(1-t4*phi)': 3*(1-t4*phi),
    '3 - 1/phi^4': 3 - 1/phi**4,
    '3 - phibar^4': 3 - phibar**4,
    'pi - phibar^2': pi - phibar**2,
    'e (Euler)': np.e,
    'phi^2 + phibar^2': phi**2 + phibar**2,       # = sqrt(5)^2 - 1 = 4... no
    'sqrt(8)': np.sqrt(8),
    '3 - 2/sqrt(5*pi)': 3 - 2/np.sqrt(5*pi),
    '3*phibar + phi': 3*phibar + phi,
    'pi*phibar + 1': pi*phibar + 1,
    'h_reduced = 30/(2*pi) * phibar': 30/(2*pi) * phibar,
    '3 - phi/sqrt(5*pi)': 3 - phi/np.sqrt(5*pi),
}

print(f"    Candidate expressions for sigma = {sigma_opt:.3f}:")
print(f"    {'expression':>30s}  {'value':>10s}  {'match to 2.870':>14s}")
print(f"    {'-'*30}  {'-'*10}  {'-'*14}")

for name, val in sorted(candidates.items(), key=lambda x: -match_pct(x[1], sigma_opt)):
    m = match_pct(val, sigma_opt)
    if m > 98:
        print(f"    {name:>30s}  {val:>10.6f}  {m:>13.2f}%  <--")
    elif m > 95:
        print(f"    {name:>30s}  {val:>10.6f}  {m:>13.2f}%")


# ================================================================
# COMPREHENSIVE: sigma = 3*phi-2 vs sigma = 3, all angles
# ================================================================
print(f"\n\n{'='*76}")
print(f"COMPREHENSIVE COMPARISON: sigma = 3*phi-2 vs sigma = 3")
print(f"{'='*76}")

sigma_new = 3*phi - 2
angles_new = compute_full_angles(sigma_new, kink_profile)
angles_old = compute_full_angles(3.0, kink_profile)

print(f"\n    {'Quantity':>20s}  {'sigma=3':>12s}  {'sigma=3phi-2':>12s}  {'measured':>12s}  {'old match':>10s}  {'new match':>10s}")
print(f"    {'-'*20}  {'-'*12}  {'-'*12}  {'-'*12}  {'-'*10}  {'-'*10}")

quantities = [
    ('theta_12 (deg)', angles_old['t12'], angles_new['t12'], PMNS['t12']),
    ('theta_23 (deg)', angles_old['t23'], angles_new['t23'], PMNS['t23']),
    ('theta_13 (deg)', angles_old['t13'], angles_new['t13'], PMNS['t13']),
    ('sin^2(theta_13)', angles_old['sin2_13'], angles_new['sin2_13'], PMNS['sin2_13']),
]

for name, old, new, meas in quantities:
    mo = match_pct(old, meas)
    mn = match_pct(new, meas)
    arrow = "  +++" if mn > mo + 3 else ("  ---" if mn < mo - 3 else "")
    print(f"    {name:>20s}  {old:>12.4f}  {new:>12.4f}  {meas:>12.4f}  {mo:>9.1f}%  {mn:>9.1f}%{arrow}")


# ================================================================
# WHAT IF sigma DEPENDS ON GENERATION?
# ================================================================
print(f"\n\n{'='*76}")
print(f"EXPLORATION: Generation-dependent sigma")
print(f"{'='*76}")

print(f"""
    In the domain wall fermion mechanism, each generation has a DIFFERENT
    bulk mass M_i, and therefore a different localization width sigma_i = 1/M_i.

    The heaviest generation (Gen 3, tau) should be MOST localized
    (smallest sigma), while the lightest (Gen 1, e) should be most spread.

    If sigma_i scales with the generation's kink coupling position:
    sigma_3 ~ 1/|u_3| = 1/3 (in inverse position units)
    sigma_2 ~ 1/|u_2| = 1/0.57 = 1.75
    sigma_1 ~ 1/|u_1| = 1/2.03 = 0.49

    But this gives very small sigma values. Let's try:
    sigma_i = sigma_0 * (1 + alpha * |u_i|)
    where sigma_0 is the base width.
""")

# The simplest generation-dependent version: sigma scales with
# distance from wall center
def compute_sin2_13_gen_sigma(sigma_0, scale_factor):
    Y = np.zeros((3, 3))
    sigmas = [sigma_0 * (1 + scale_factor * abs(u)) for u in u_gen]

    for i in range(3):
        for j in range(i, 3):
            # Use geometric mean of the two sigmas for the overlap
            sigma_ij = np.sqrt(sigmas[i] * sigmas[j])
            def integrand(u, ii=i, jj=j, sij=sigma_ij):
                fi = fermion_gaussian(u, u_gen[ii], sigmas[ii])
                fj = fermion_gaussian(u, u_gen[jj], sigmas[jj])
                return fi * kink_profile(u) * fj
            Y[i, j], _ = integrate.quad(integrand, -30, 30, limit=200)
            Y[j, i] = Y[i, j]

    evals, evecs = linalg.eigh(Y)
    idx = np.argsort(np.abs(evals))
    evecs = evecs[:, idx]
    s13 = min(abs(evecs[0, 2]), 1.0)
    return s13**2

# This is getting too parameter-heavy. Let's be honest about it.
print(f"    Generation-dependent sigma adds a free parameter. Skipping.")
print(f"    (This would be fitting, not deriving.)")


# ================================================================
# THE MOST HONEST TEST: Fix sigma from other physics
# ================================================================
print(f"\n\n{'='*76}")
print(f"HONEST TEST: Can sigma be fixed from OTHER observables?")
print(f"{'='*76}")

print(f"""
    The real test: if sigma is determined by some OTHER physical quantity
    (not theta_13), and that value ALSO gives a good theta_13, then we
    have a genuine prediction.

    From FINDINGS-v2.md, the mass hierarchy m_tau/m_mu = 16.82 should
    also emerge from the domain wall. Let's find what sigma gives the
    correct mass hierarchy and check if it also gives good theta_13.
""")

# Scan sigma for mass hierarchy
print(f"    sigma scan: mass hierarchy AND theta_13")
print(f"    {'sigma':>8s}  {'m3/m2':>8s}  {'m2/m1':>8s}  {'sin^2_13':>10s}  {'match_13':>10s}  {'m3/m2 match':>12s}")
print(f"    {'-'*8}  {'-'*8}  {'-'*8}  {'-'*10}  {'-'*10}  {'-'*12}")

for sigma_100 in range(150, 500, 10):
    sigma = sigma_100 / 100.0
    angles = compute_full_angles(sigma, kink_profile)
    m_match = match_pct(angles['m3/m2'], 16.82)
    s_match = match_pct(angles['sin2_13'], sin2_13_measured)
    if s_match > 80 or m_match > 50:
        print(f"    {sigma:>8.2f}  {angles['m3/m2']:>8.2f}  {angles['m2/m1']:>8.2f}  "
              f"{angles['sin2_13']:>10.6f}  {s_match:>9.1f}%  {m_match:>11.1f}%")


# ================================================================
# THE t4*sqrt(5)*phi CORRECTION
# ================================================================
print(f"\n\n{'='*76}")
print(f"ANALYSIS: The t4 * sqrt(5) * phi correction")
print(f"{'='*76}")

k_opt = sqrt5 * phi
correction = 1 - k_opt * t4
corrected = 0.025678 * correction

print(f"""
    The t4 correction with k = sqrt(5)*phi:
    sin^2(theta_13) = 0.0257 * (1 - sqrt(5)*phi*t4)
                    = 0.0257 * (1 - {sqrt5*phi:.6f} * {t4:.6f})
                    = 0.0257 * (1 - {sqrt5*phi*t4:.6f})
                    = 0.0257 * {correction:.6f}
                    = {corrected:.6f}
    Match: {match_pct(corrected, sin2_13_measured):.1f}%

    What is sqrt(5)*phi?
    sqrt(5)*phi = {sqrt5*phi:.6f}
    = sqrt(5) * phi = sqrt(5) * (1+sqrt(5))/2 = (sqrt(5) + 5)/2 = (5 + sqrt(5))/2
    = phi^2 * sqrt(5)/phi = phi * sqrt(5) = sqrt(5*phi^2) = sqrt(5*(phi+1)) = sqrt(5*phi+5)

    Numerically: {sqrt5*phi:.6f}
    phi^3 = {phi**3:.6f}  (different: {match_pct(sqrt5*phi, phi**3):.1f}%)
    Hmm, phi^3 = phi^2+phi = phi+1+phi = 2*phi+1 = 2*1.618+1 = 4.236
    sqrt(5)*phi = 2.236*1.618 = 3.618 = phi + 2 = phi^2 + 1

    Wait: sqrt(5)*phi = sqrt(5)*(1+sqrt(5))/2 = (sqrt(5)+5)/2 = {(sqrt5+5)/2:.6f}

    And: phi + 2 = {phi+2:.6f}  (YES, they're equal!)
    Because phi + 2 = (1+sqrt(5))/2 + 2 = (5+sqrt(5))/2 = sqrt(5)*phi. CONFIRMED.

    So the correction is: (1 - (phi+2)*t4)

    Structural interpretation of k = phi + 2:
    - phi = golden ratio (our vacuum)
    - 2 = number of vacua / Z2 factor
    - phi + 2 = "vacuum + both sides"
    - (phi+2) * t4 = total dark vacuum leakage including both sides

    This IS structurally motivated. The dark vacuum correction t4 acts
    through phi + 2 = sqrt(5)*phi channels because:
    1. The kink traverses phi (one vacuum) + 2 (both vacuum edges)
    2. Or: the phi^3 = phi*(phi+1) = phi*phi^2 decomposition

    However, the VALUE (phi+2)*t4 = {(phi+2)*t4:.6f} is quite specific.
    The general t4 correction pattern (1 - k*t4) has k=1 for V_us,
    k=phi for the hierarchy, etc. Having k = phi+2 for theta_13
    would need independent motivation.
""")


# ================================================================
# FINAL SUMMARY
# ================================================================
print(f"\n\n{'='*76}")
print(f"FINAL SUMMARY")
print(f"{'='*76}")

print(f"""
    BASELINE: sin^2(theta_13) = 0.0257  (sigma=3, kink kernel, 85.7% match)
    TARGET:   sin^2(theta_13) = 0.0220 +/- 0.0007

    THREE CANDIDATE IMPROVEMENTS:

    1. sigma = sqrt(5) + 1/phi = 3*phi - 2 = {3*phi-2:.4f}
       sin^2 = {compute_sin2_13(3*phi-2, kink_profile):.6f}  ({match_pct(compute_sin2_13(3*phi-2, kink_profile), sin2_13_measured):.1f}%)
       Structural meaning: (3*sqrt(5)-1)/2, or 3 generations times phi minus 2 vacua
       Involves sqrt(5): YES (sqrt(5) + phibar = (3*sqrt(5)-1)/2)
       Problem: sigma=3 was chosen empirically too; this is just a DIFFERENT empirical sigma

    2. Cross-wall suppression by 2/sqrt(5)
       sin^2 = {angles_2['sin2_13']:.6f}  (97.8%)
       Structural meaning: normalized tunneling amplitude
       Involves sqrt(5): YES (2/sqrt(5))
       Problem: no derivation of WHY this suppression factor; depends on which
                elements are classified as "cross-wall"

    3. t4 correction: sin^2 * (1 - (phi+2)*t4) = sin^2 * (1 - sqrt(5)*phi*t4)
       sin^2 = {0.025678 * (1 - sqrt5*phi*t4):.6f}  ({match_pct(0.025678*(1-sqrt5*phi*t4), sin2_13_measured):.1f}%)
       Structural meaning: dark vacuum leakage through phi+2 channels
       Involves sqrt(5): YES (sqrt(5)*phi = phi+2)
       Problem: the coefficient k = phi+2 needs independent derivation

    BOTTOM LINE:
    - The sqrt(5) connection is REAL in the sense that sqrt(5) is the
      field range between vacua, and cross-wall quantities should involve it
    - HOWEVER, no single modification gives a CLEAN, DERIVED improvement
    - The best numerical improvement comes from sigma = sqrt(5) + 1/phi (97.8%)
      or the t4 correction with k = sqrt(5)*phi (96.2%)
    - Both are structurally suggestive but not rigorously derived
    - The 85.7% baseline may simply reflect that sigma=3 is an approximation,
      and the true sigma (from the physical bulk mass) is closer to 2.85-2.87
    - The continuous optimum sigma = 2.87 is suspiciously close to both
      sqrt(5) + 1/phi = 2.854 and e = 2.718 and 3 - 1/phi^4 = 2.854
""")

print("=" * 76)
print("END OF DEEP DIVE")
print("=" * 76)
