#!/usr/bin/env python3
"""
close_to_99.py — Systematically apply the unified loop correction to all sub-99% quantities
========================================================================================

PROVEN PATTERN (from unified_gap_closure.py):
    corrected = tree_level * (1 +/- C * G)
where:
    C = eta * theta_4 / 2  (universal loop factor = 0.001794)
    G = geometry factor from {phi, phi^2, phibar, sqrt(5), L(n)/L(m), integers, ...}

This already fixed:
    alpha:  99.53% -> 99.9996%  (G = phi^2, sign = -)
    v:      99.58% -> 99.9992%  (G = 7/3 = L(4)/L(2), sign = +)

NOW APPLYING TO:
    lambda_H:        98.4%   tree = 1/(3*phi^2)
    eta_B:           95.5%   tree = phibar^44
    dm32^2/dm21^2:   97.9%   tree = 3*phi^5
    m_c:             96.4%   tree = m_t * alpha (depends on alpha value)
    m_n - m_p:       97.0%   tree = (m_d - m_u) / (phi + phibar^2)
    theta_23 PMNS:   95.0%   tree = 45 + arctan(theta_4) degrees
    theta_13 PMNS:   85.7%   tree = breathing mode at sigma=3
"""

import math

# ==============================================================================
# CONSTANTS
# ==============================================================================

PHI = (1 + math.sqrt(5)) / 2
PHIBAR = 1 / PHI
SQRT5 = math.sqrt(5)

# Lucas numbers
L = [None, 1, 3, 4, 7, 11, 18, 29, 47, 76, 123]  # L[n] = L(n)

# Modular forms at q = 1/phi
q = PHIBAR
N_terms = 2000

eta = q**(1/24)
for n in range(1, N_terms):
    eta *= (1 - q**n)

t2_raw = 0.0
for n in range(0, 200):
    t2_raw += q**((n+0.5)**2)
t2 = 2 * t2_raw

t3 = 1.0
for n in range(1, N_terms):
    t3 *= (1 - q**(2*n)) * (1 + q**(2*n-1))**2

t4 = 1.0
for n in range(1, N_terms):
    t4 *= (1 - q**(2*n)) * (1 - q**(2*n-1))**2

# Eisenstein E4
E4 = 1.0
for n in range(1, 500):
    s3 = 0
    for d in range(1, n+1):
        if n % d == 0:
            s3 += d**3
    E4 += 240 * s3 * q**n

# Universal loop factor
C = eta * t4 / 2

print("=" * 90)
print("CLOSE TO 99%: Systematic Loop Correction for All Sub-99% Quantities")
print("=" * 90)
print()
print(f"  Modular forms at q = 1/phi:")
print(f"    eta  = {eta:.12f}")
print(f"    t3   = {t3:.12f}")
print(f"    t4   = {t4:.12f}")
print(f"    E4   = {E4:.4f}")
print(f"    C    = eta*t4/2 = {C:.12f}")
print()

# ==============================================================================
# MEASURED VALUES
# ==============================================================================

ALPHA = 1/137.035999084
M_Z = 91.1876  # GeV
v_meas = 246.22  # GeV
m_e = 0.51099895  # MeV
m_mu = 105.6584  # MeV
m_tau = 1776.86  # MeV
m_u = 2.16  # MeV
m_d = 4.67  # MeV
m_s = 93.4  # MeV
m_c = 1270.0  # MeV
m_b = 4180.0  # MeV
m_t = 172690.0  # MeV (172.69 GeV)
MU = 1836.15267343

# Mixing
sin2_t13_meas = 0.0220  # sin^2(theta_13) PMNS
sin2_t23_meas = 0.572   # sin^2(theta_23) PMNS (best fit, NO)
theta_23_meas = math.degrees(math.asin(math.sqrt(sin2_t23_meas)))  # ~49.13 deg

# CKM measured
V_us_meas = 0.2253
V_cb_meas = 0.0405
V_ub_meas = 0.00382

# Cosmological
lambda_H_meas = 0.12916  # Higgs quartic
eta_B_meas = 6.14e-10  # baryon asymmetry
dm32_dm21_meas = 29.7  # dm32^2/dm21^2
mn_mp_meas = 1.2934  # MeV

# Framework derived
alpha_s_meas = 0.1179
sin2tW_meas = 0.23121

# ==============================================================================
# GEOMETRY FACTOR VOCABULARY
# ==============================================================================

geo_factors = {
    "1": 1.0,
    "2": 2.0,
    "3": 3.0,
    "phi": PHI,
    "phi^2": PHI**2,
    "phi^3": PHI**3,
    "phibar": PHIBAR,
    "phibar^2": PHIBAR**2,
    "sqrt(5)": SQRT5,
    "1/phi": PHIBAR,
    "2/3": 2/3,
    "3/2": 3/2,
    "7/3": 7/3,
    "L(4)/3": L[4]/3,
    "L(5)/3": L[5]/3,
    "L(4)/L(2)": L[4]/L[2],
    "L(5)/L(2)": L[5]/L[2],
    "L(5)/L(3)": L[5]/L[3],
    "L(6)/L(4)": L[6]/L[4],
    "L(7)/L(5)": L[7]/L[5],
    "phi+1": PHI+1,
    "phi*sqrt(5)": PHI*SQRT5,
    "pi": math.pi,
    "pi/phi": math.pi/PHI,
    "pi*phi": math.pi*PHI,
    "pi*sqrt(5)/2": math.pi*SQRT5/2,
    "2*phi": 2*PHI,
    "phi/3": PHI/3,
    "5": 5.0,
    "7": 7.0,
    "h/3=10": 10.0,
    "phi^2/3": PHI**2/3,
    "2*phi^2/3": 2*PHI**2/3,
    "sqrt(5)/3": SQRT5/3,
    "sqrt(5)*phi": SQRT5*PHI,
    "4/3": 4/3,
    "5/3": 5/3,
    "L(4)=7": 7.0,
    "L(5)=11": 11.0,
    "phi^4": PHI**4,
    "30": 30.0,
    "h=30": 30.0,
    "80": 80.0,
    "phi^2-1": PHI**2 - 1,
    "2*sqrt(5)/3": 2*SQRT5/3,
    "phi*phibar^2": PHI*PHIBAR**2,
    "3*phi": 3*PHI,
    "(phi+phibar^2)": PHI + PHIBAR**2,  # = 2
    "phi^2*sqrt(5)/3": PHI**2*SQRT5/3,
}


def find_best_correction(tree_val, measured_val, label, try_both_signs=True):
    """Try C * G correction for all geometry factors, both signs."""
    results = []

    tree_match = abs(tree_val / measured_val - 1) * 100

    for name, G in geo_factors.items():
        for sign_label, sign in [("+", 1), ("-", -1)]:
            if not try_both_signs and sign == -1:
                continue
            corrected = tree_val * (1 + sign * C * G)
            match = (1 - abs(corrected / measured_val - 1)) * 100
            improvement = match - (100 - tree_match)
            if match > (100 - tree_match):  # only report improvements
                results.append((match, name, sign_label, corrected, G, improvement))

    results.sort(key=lambda x: -x[0])
    return results[:8], tree_match


def find_best_additive(tree_val, measured_val, label):
    """Try additive corrections: tree + C * G * scale."""
    results = []
    tree_match = (1 - abs(tree_val / measured_val - 1)) * 100

    for name, G in geo_factors.items():
        for sign_label, sign in [("+", 1), ("-", -1)]:
            corrected = tree_val + sign * C * G
            match = (1 - abs(corrected / measured_val - 1)) * 100
            if match > tree_match:
                results.append((match, name, sign_label, corrected, G))

    results.sort(key=lambda x: -x[0])
    return results[:5], tree_match


# ==============================================================================
# 1. HIGGS QUARTIC lambda_H
# ==============================================================================
print("=" * 90)
print("1. HIGGS QUARTIC: lambda_H = 1/(3*phi^2)")
print("-" * 90)

lambda_tree = 1 / (3 * PHI**2)
results, tree_match = find_best_correction(lambda_tree, lambda_H_meas, "lambda_H")

print(f"  Tree level:  {lambda_tree:.6f}")
print(f"  Measured:    {lambda_H_meas:.6f}")
print(f"  Tree match:  {100-tree_match:.2f}%")
print()

# Also try: lambda_H = (2+t4)/(3*phi^2) etc
lambda_t4 = (2 + t4) / (6 * PHI**2)  # from m_H formula: m_H^2 = 2*lambda*v^2
print(f"  With theta_4: (2+t4)/(6*phi^2) = {lambda_t4:.6f}")
print(f"  Match: {(1 - abs(lambda_t4/lambda_H_meas - 1))*100:.2f}%")
print()

# Direct from Higgs mass: lambda = m_H^2 / (2*v^2)
m_H_pred = v_meas * math.sqrt((2 + t4) / (3 * PHI**2))
lambda_from_mH = m_H_pred**2 / (2 * v_meas**2)
print(f"  From m_H formula: lambda = m_H^2/(2v^2) = {lambda_from_mH:.6f}")
print(f"  Match: {(1 - abs(lambda_from_mH/lambda_H_meas - 1))*100:.2f}%")
print()

if results:
    print(f"  Best loop corrections (tree * (1 +/- C*G)):")
    for match, name, sign, corr, G, imp in results[:5]:
        print(f"    G = {name:20s} ({sign}): {corr:.6f}  -> {match:.4f}%  (+{imp:.2f}pp)")

# Try: lambda = 1/(3*phi^2) * (1 + C * G) where we need ~1.5% increase
needed_G = (lambda_H_meas / lambda_tree - 1) / C
print(f"\n  Needed geometry factor: G = {needed_G:.4f}")
# Check what this is close to
for name, G in sorted(geo_factors.items(), key=lambda x: abs(x[1] - needed_G)):
    if abs(G - needed_G) / abs(needed_G) < 0.1:
        print(f"    Close to {name} = {G:.4f} ({abs(G/needed_G - 1)*100:.2f}% off)")

print()

# ==============================================================================
# 2. BARYON ASYMMETRY eta_B
# ==============================================================================
print("=" * 90)
print("2. BARYON ASYMMETRY: eta_B = phibar^44")
print("-" * 90)

eta_B_tree = PHIBAR**44
results, tree_match = find_best_correction(eta_B_tree, eta_B_meas, "eta_B")

print(f"  Tree level:  {eta_B_tree:.4e}")
print(f"  Measured:    {eta_B_meas:.4e}")
print(f"  Tree match:  {100-tree_match:.2f}%")
print()

if results:
    print(f"  Best loop corrections:")
    for match, name, sign, corr, G, imp in results[:5]:
        print(f"    G = {name:20s} ({sign}): {corr:.4e}  -> {match:.4f}%  (+{imp:.2f}pp)")

# The gap is ~4.5% -- C alone is 0.18%, so we need G ~ 25
needed_G = (eta_B_meas / eta_B_tree - 1) / C
print(f"\n  Needed geometry factor: G = {needed_G:.4f}")
for name, G in sorted(geo_factors.items(), key=lambda x: abs(x[1] - needed_G)):
    if abs(G - needed_G) / abs(needed_G) < 0.15:
        print(f"    Close to {name} = {G:.4f} ({abs(G/needed_G - 1)*100:.2f}% off)")

# Also try: different exponent
print(f"\n  Exponent scan: phibar^n")
best_exp_match = 0
best_n = 44
for n in range(40, 50):
    val = PHIBAR**n
    match = (1 - abs(val / eta_B_meas - 1)) * 100
    marker = " <--" if match > best_exp_match else ""
    if match > 90:
        print(f"    n={n}: phibar^{n} = {val:.4e}, match = {match:.2f}%{marker}")
    if match > best_exp_match:
        best_exp_match = match
        best_n = n

# Try phibar^44 * (1 + C*G) with larger combinations
print(f"\n  Extended search: phibar^44 * (1 + C*G1*G2)")
for n1, g1 in geo_factors.items():
    for n2, g2 in geo_factors.items():
        if g1 * g2 > 100:
            continue
        for sign in [1, -1]:
            corr = eta_B_tree * (1 + sign * C * g1 * g2)
            match = (1 - abs(corr / eta_B_meas - 1)) * 100
            if match > 99.0:
                s = "+" if sign > 0 else "-"
                print(f"    G = {n1}*{n2} = {g1*g2:.4f} ({s}): {corr:.4e} -> {match:.4f}%")

print()

# ==============================================================================
# 3. NEUTRINO MASS RATIO dm32^2/dm21^2
# ==============================================================================
print("=" * 90)
print("3. NEUTRINO MASS RATIO: dm32^2/dm21^2 = 3*phi^5")
print("-" * 90)

dm_tree = 3 * PHI**5
results, tree_match = find_best_correction(dm_tree, dm32_dm21_meas, "dm_ratio")

print(f"  Tree level:  {dm_tree:.4f}")
print(f"  Measured:    {dm32_dm21_meas:.4f}")
print(f"  Tree match:  {100-tree_match:.2f}%")
print()

if results:
    print(f"  Best loop corrections:")
    for match, name, sign, corr, G, imp in results[:5]:
        print(f"    G = {name:20s} ({sign}): {corr:.4f}  -> {match:.4f}%  (+{imp:.2f}pp)")

needed_G = (dm32_dm21_meas / dm_tree - 1) / C
print(f"\n  Needed geometry factor: G = {needed_G:.4f}")
for name, G in sorted(geo_factors.items(), key=lambda x: abs(x[1] - needed_G)):
    if abs(G - needed_G) / abs(needed_G) < 0.15:
        print(f"    Close to {name} = {G:.4f} ({abs(G/needed_G - 1)*100:.2f}% off)")

# Also try theta_4 corrections directly
print(f"\n  Direct theta_4 corrections:")
for expr_name, val in [
    ("3*phi^5*(1-t4)", 3*PHI**5*(1-t4)),
    ("3*phi^5*(1-t4/phi)", 3*PHI**5*(1-t4/PHI)),
    ("3*phi^5*(1+t4)", 3*PHI**5*(1+t4)),
    ("3*phi^5*(1-t4/3)", 3*PHI**5*(1-t4/3)),
    ("3*phi^5/(1+t4)", 3*PHI**5/(1+t4)),
    ("3*phi^5/(1-t4)", 3*PHI**5/(1-t4)),
    ("3*phi^5-1", 3*PHI**5-1),
    ("3*phi^5-phi", 3*PHI**5-PHI),
    ("3*phi^5-phibar", 3*PHI**5-PHIBAR),
    ("L(7)+phibar", L[7]+PHIBAR),
    ("L(7)+phibar^2", L[7]+PHIBAR**2),
    ("L(7)+1", L[7]+1),
    ("h-phibar", 30-PHIBAR),
    ("h-phibar^2", 30-PHIBAR**2),
]:
    match = (1 - abs(val / dm32_dm21_meas - 1)) * 100
    if match > 97:
        print(f"    {expr_name:30s} = {val:.4f}, match = {match:.4f}%")

print()

# ==============================================================================
# 4. CHARM QUARK MASS
# ==============================================================================
print("=" * 90)
print("4. CHARM QUARK MASS: m_c = m_e * mu / 10 * sqrt(2/3)  or  m_t * alpha")
print("-" * 90)

# Two routes
m_c_route1 = m_e * MU / 10 * math.sqrt(2/3)  # from mu-tower
m_c_route2 = m_t * ALPHA * 1000  # m_t * alpha, converting to MeV
m_c_route3 = m_e * MU / 10  # simpler version

print(f"  Route 1: m_e*mu/10*sqrt(2/3) = {m_c_route1:.2f} MeV, match = {(1-abs(m_c_route1/m_c-1))*100:.2f}%")
print(f"  Route 2: m_t*alpha           = {m_c_route2:.2f} MeV, match = {(1-abs(m_c_route2/m_c-1))*100:.2f}%")
print(f"  Route 3: m_e*mu/10           = {m_c_route3:.2f} MeV (= m_s's formula, too low for charm)")
print()

# Use route 2 as tree and try corrections
m_c_tree = m_t * ALPHA * 1000
results, tree_match = find_best_correction(m_c_tree, m_c, "m_c")

print(f"  Tree (m_t*alpha):  {m_c_tree:.2f} MeV")
print(f"  Measured:          {m_c:.2f} MeV")
print(f"  Tree match:        {100-tree_match:.2f}%")
print()

if results:
    print(f"  Best loop corrections:")
    for match, name, sign, corr, G, imp in results[:5]:
        print(f"    G = {name:20s} ({sign}): {corr:.2f} MeV  -> {match:.4f}%")

# Try corrected alpha
alpha_corrected = (t4 / (t3 * PHI)) * (1 - eta*t4*PHI**2/2)
m_c_with_corrected_alpha = m_t * alpha_corrected * 1000
print(f"\n  With VP-corrected alpha: m_t*alpha_corr = {m_c_with_corrected_alpha:.2f} MeV")
print(f"  Match: {(1-abs(m_c_with_corrected_alpha/m_c-1))*100:.2f}%")

# Direct theta_4 corrections
print(f"\n  Direct corrections to m_c = m_t * alpha:")
for expr_name, val in [
    ("m_t*alpha*(1+t4)", m_c_tree*(1+t4)),
    ("m_t*alpha*(1+t4/phi)", m_c_tree*(1+t4/PHI)),
    ("m_t*alpha*(1+2*t4)", m_c_tree*(1+2*t4)),
    ("m_t*alpha*(1+3*t4)", m_c_tree*(1+3*t4)),
    ("m_t*alpha/(1-t4)", m_c_tree/(1-t4)),
    ("m_t*alpha/(1-2*t4)", m_c_tree/(1-2*t4)),
    ("m_t*alpha*(1+t4*phi)", m_c_tree*(1+t4*PHI)),
    ("m_t*alpha*(1+t4*phi^2)", m_c_tree*(1+t4*PHI**2)),
    ("m_t*alpha*(1+eta/3)", m_c_tree*(1+eta/3)),
    ("m_t*alpha*(1+eta/phi)", m_c_tree*(1+eta/PHI)),
    ("m_t*alpha_corr", m_c_with_corrected_alpha),
    ("m_e*mu*phi^3/10", m_e*MU*PHI**3/(10)),
    ("m_e*mu/h*(phi+1)", m_e*MU/30*(PHI+1)),
    ("m_e*MU*sqrt(2/3)", m_c_route1),
]:
    match = (1 - abs(val / m_c - 1)) * 100
    if match > 96:
        print(f"    {expr_name:30s} = {val:.2f} MeV, match = {match:.4f}%")

print()

# ==============================================================================
# 5. NEUTRON-PROTON MASS DIFFERENCE
# ==============================================================================
print("=" * 90)
print("5. NEUTRON-PROTON MASS DIFFERENCE")
print("-" * 90)

mn_mp_tree = (m_d - m_u) / (PHI + PHIBAR**2)
print(f"  Tree: (m_d - m_u)/(phi + phibar^2) = {mn_mp_tree:.4f} MeV")
print(f"  Measured: {mn_mp_meas:.4f} MeV")
print(f"  Tree match: {(1-abs(mn_mp_tree/mn_mp_meas-1))*100:.2f}%")
print()

# Note: phi + phibar^2 = phi + 1/phi^2 = phi + phi-1 ... wait
# phi + phibar^2 = 1.618 + 0.382 = 2.0
print(f"  phi + phibar^2 = {PHI + PHIBAR**2:.6f} (= 2.0)")
print(f"  So tree = (m_d - m_u)/2 = {(m_d - m_u)/2:.4f}")
print()

# Try different denominators
print(f"  Denominator scan:")
for expr_name, denom in [
    ("2", 2),
    ("phi+phibar^2", PHI + PHIBAR**2),
    ("phi^2-1", PHI**2-1),
    ("sqrt(5)-1", SQRT5-1),
    ("phi", PHI),
    ("2*(1-t4)", 2*(1-t4)),
    ("2*(1+t4)", 2*(1+t4)),
    ("2/(1+t4)", 2/(1+t4)),
    ("2-t4", 2-t4),
    ("phi+phibar^2-t4", PHI+PHIBAR**2-t4),
    ("sqrt(5)/phi", SQRT5/PHI),
    ("3/phi", 3/PHI),
    ("phi+1/3", PHI+1/3),
    ("phi+phibar^3", PHI+PHIBAR**3),
]:
    val = (m_d - m_u) / denom
    match = (1 - abs(val / mn_mp_meas - 1)) * 100
    if match > 95:
        print(f"    denom = {expr_name:20s} = {denom:.6f}: mn-mp = {val:.4f}, match = {match:.2f}%")

# The issue is m_d - m_u = 2.51 MeV (PDG), measured mn-mp = 1.2934 MeV
# So denominator should be ~1.94
target_denom = (m_d - m_u) / mn_mp_meas
print(f"\n  Target denominator: {target_denom:.6f}")
print(f"  2 - t4*phi = {2 - t4*PHI:.6f}")
print(f"  2 - t4*phi^2 = {2 - t4*PHI**2:.6f}")

# Also: EM correction is known to be ~-0.76 MeV
# QCD-only: mn-mp(QCD) = 2.52 +/- 0.17 MeV  (BMW 2015)
# EM contribution: mn-mp(EM) = -1.00 +/- 0.16 MeV
print(f"\n  NOTE: mn-mp has known EM correction ~ -0.76 MeV")
print(f"  QCD-only prediction: (m_d-m_u)/2 = {(m_d-m_u)/2:.4f}")
print(f"  With EM: (m_d-m_u)/2 + EM = needs EM ~ {mn_mp_meas - (m_d-m_u)/2:.4f} MeV")
print(f"  Framework EM correction: -alpha*m_p*3/(4*phi) = {-ALPHA*938.272*3/(4*PHI):.4f} MeV")
mn_mp_with_em = (m_d - m_u) / 2 - ALPHA * 938.272 * 3 / (4 * PHI)
print(f"  Total: {mn_mp_with_em:.4f} MeV, match = {(1-abs(mn_mp_with_em/mn_mp_meas-1))*100:.2f}%")

print()

# ==============================================================================
# 6. THETA_23 PMNS
# ==============================================================================
print("=" * 90)
print("6. THETA_23 PMNS: sin^2(theta_23)")
print("-" * 90)

# Current formula: sin^2(theta_23) = 3/(2*phi^2)
sin2_t23_tree = 3 / (2 * PHI**2)
# Alternative: theta_23 = 45 + arctan(theta_4)
theta_23_alt = 45 + math.degrees(math.atan(t4))
sin2_t23_alt = math.sin(math.radians(theta_23_alt))**2

print(f"  Formula 1: sin^2(t23) = 3/(2*phi^2) = {sin2_t23_tree:.6f}")
print(f"  Match: {(1-abs(sin2_t23_tree/sin2_t23_meas-1))*100:.2f}%")
print()
print(f"  Formula 2: theta_23 = 45+arctan(t4) = {theta_23_alt:.4f} deg")
print(f"  sin^2 = {sin2_t23_alt:.6f}")
print(f"  Match: {(1-abs(sin2_t23_alt/sin2_t23_meas-1))*100:.2f}%")
print()

# The measurement has large uncertainty: sin^2(theta_23) = 0.572 +/- 0.018
# But best fit is 0.572 (NO) or 0.578 (IO)
# 3/(2*phi^2) = 0.5729 is actually quite good!

# Try corrections
results, tree_match = find_best_correction(sin2_t23_tree, sin2_t23_meas, "sin2_t23")
print(f"  Tree match: {100-tree_match:.2f}%")
if results:
    print(f"  Best loop corrections to 3/(2*phi^2):")
    for match, name, sign, corr, G, imp in results[:5]:
        print(f"    G = {name:20s} ({sign}): {corr:.6f}  -> {match:.4f}%")

# Direct theta_4 scans
print(f"\n  Direct corrections:")
for expr_name, val in [
    ("3/(2*phi^2)*(1-t4/3)", sin2_t23_tree*(1-t4/3)),
    ("3/(2*phi^2)*(1+t4/phi)", sin2_t23_tree*(1+t4/PHI)),
    ("3/(2*phi^2)*(1-t4/phi)", sin2_t23_tree*(1-t4/PHI)),
    ("3/(2*phi^2)*(1-t4*phibar)", sin2_t23_tree*(1-t4*PHIBAR)),
    ("3/(2*phi^2)+t4/phi^2", sin2_t23_tree + t4/PHI**2),
    ("(3-t4)/(2*phi^2)", (3-t4)/(2*PHI**2)),
    ("(3+t4)/(2*phi^2)", (3+t4)/(2*PHI**2)),
    ("3/(2*phi^2+t4)", 3/(2*PHI**2+t4)),
    ("3/(2*(phi^2-t4))", 3/(2*(PHI**2-t4))),
    ("(3+t4)/(2*(phi^2+t4))", (3+t4)/(2*(PHI**2+t4))),
]:
    match = (1 - abs(val / sin2_t23_meas - 1)) * 100
    if match > 99:
        print(f"    {expr_name:35s} = {val:.6f}, match = {match:.4f}%")

# Note: maximal mixing (45 deg) gives sin^2 = 0.5; measured ~0.572
# Deviation from maximal: delta = 0.072
# In framework: delta = t4/phi^2 = 0.01157... not enough
# Need delta ~ 3/(2*phi^2) - 0.5 = 0.0729
# Or: sin^2 = 1/2 + deviation_from_maximal
deviation = sin2_t23_meas - 0.5
print(f"\n  Deviation from maximal mixing: {deviation:.6f}")
print(f"  3/(2*phi^2) - 1/2 = {3/(2*PHI**2) - 0.5:.6f}")
print(f"  phibar^2/sqrt(5) = {PHIBAR**2/SQRT5:.6f}")
print(f"  1/(2*phi^(5/2)) = {1/(2*PHI**(5/2)):.6f}")

print()

# ==============================================================================
# 7. THETA_13 PMNS (the hardest one)
# ==============================================================================
print("=" * 90)
print("7. THETA_13 PMNS: sin^2(theta_13)")
print("-" * 90)

# Current: sin^2(theta_13) = 0.0257 at sigma=3 (85.7%)
# With sigma = 3 - phibar^4: 0.02152 (97.8%)
sin2_t13_sigma3 = 0.02567  # from breathing mode at sigma=3
sigma_corrected = 3 - PHIBAR**4  # = sqrt(5) + 1/phi = 2.854
# Need to compute this properly...
# From the script: sigma = 3 - phibar^4 gives sin^2 = 0.02152

print(f"  Current: sin^2(t13) = 0.0257 at sigma=3, match = {(1-abs(0.0257/sin2_t13_meas-1))*100:.2f}%")
print(f"  With sigma = 3-phibar^4 = {sigma_corrected:.4f}: sin^2 ~ 0.02152")
print(f"  Match with correction: {(1-abs(0.02152/sin2_t13_meas-1))*100:.2f}%")
print()

# The breathing mode formula: sin^2(t13) ~ |c1*psi1(u1)*psi1(u3)|^2 / (c0*psi0...)
# Let's try direct algebraic formulas
print(f"  Algebraic formula scan for sin^2(theta_13) = 0.0220:")
targets_t13 = []
for expr_name, val in [
    ("t4/phi", t4/PHI),
    ("t4*phibar", t4*PHIBAR),
    ("t4/(phi+1)", t4/(PHI+1)),
    ("t4/phi^2", t4/PHI**2),
    ("t4*2/3", t4*2/3),
    ("t4/sqrt(5)", t4/SQRT5),
    ("t4*phibar/sqrt(5)", t4*PHIBAR/SQRT5),
    ("eta^2/phi", eta**2/PHI),
    ("eta^2/phi^2", eta**2/PHI**2),
    ("eta^2/(3*phi)", eta**2/(3*PHI)),
    ("eta*t4", eta*t4),
    ("eta*t4*phi", eta*t4*PHI),
    ("2*C", 2*C),
    ("C*phi^3", C*PHI**3),
    ("C*phi^4", C*PHI**4),
    ("2*C*phi^3", 2*C*PHI**3),
    ("2*C*phi^4", 2*C*PHI**4),
    ("C*L(5)", C*L[5]),
    ("C*L(6)", C*L[6]),
    ("C*h/3", C*10),
    ("2*C*h/3", 2*C*10),
    ("eta^2*t4", eta**2*t4),
    ("phibar^8", PHIBAR**8),
    ("phibar^8/phi", PHIBAR**8/PHI),
    ("3*phibar^8", 3*PHIBAR**8),
    ("phibar^7/3", PHIBAR**7/3),
    ("phibar^7/phi", PHIBAR**7/PHI),
    ("eta/(3*phi^2)", eta/(3*PHI**2)),
    ("1/(3*h*phi)", 1/(3*30*PHI)),
    ("1/(2*h*phi)", 1/(2*30*PHI)),
    ("phibar^3/h", PHIBAR**3/30),
    ("2/(3*h)", 2/(3*30)),
    ("t4^2/t3", t4**2/t3),
    ("t4^2*phi", t4**2*PHI),
    ("eta*phibar^3", eta*PHIBAR**3),
    ("eta*phibar^4", eta*PHIBAR**4),
    ("(2/3)/h", (2/3)/30),
    ("(2/3)/(h+phi)", (2/3)/(30+PHI)),
    ("phibar^4/(3*phi)", PHIBAR**4/(3*PHI)),
    ("C*3*phi^2", C*3*PHI**2),
    ("C*2*phi^3", 2*C*PHI**3),
]:
    match = (1 - abs(val / sin2_t13_meas - 1)) * 100
    if match > 95:
        targets_t13.append((match, expr_name, val))

targets_t13.sort(key=lambda x: -x[0])
for match, name, val in targets_t13[:10]:
    print(f"    sin^2(t13) = {name:25s} = {val:.6f}, match = {match:.2f}%")

print()

# ==============================================================================
# 8. V_us (Cabibbo angle) - just below 99%
# ==============================================================================
print("=" * 90)
print("8. V_us (CABIBBO): phi/7 * (1 - t4)")
print("-" * 90)

V_us_tree = PHI / 7 * (1 - t4)
V_us_pure = PHI / 7

print(f"  phi/7 = {V_us_pure:.6f}")
print(f"  phi/7*(1-t4) = {V_us_tree:.6f}")
print(f"  Measured: {V_us_meas:.6f}")
print(f"  Match: {(1-abs(V_us_tree/V_us_meas-1))*100:.4f}%")
print()

# Try corrections
for expr_name, val in [
    ("phi/7*(1-t4)*(1+C*phi^2)", V_us_tree*(1+C*PHI**2)),
    ("phi/7*(1-t4)*(1+C*7/3)", V_us_tree*(1+C*7/3)),
    ("phi/7*(1-t4)*(1+C*phi)", V_us_tree*(1+C*PHI)),
    ("phi/7*(1-t4^2)", PHI/7*(1-t4**2)),
    ("phi/7*(1-t4-t4^2)", PHI/7*(1-t4-t4**2)),
    ("phi/7*(1-t4+t4^2/2)", PHI/7*(1-t4+t4**2/2)),
    ("phi/7*(1-t4)/(1-t4^2)", PHI/7*(1-t4)/(1-t4**2)),
    ("sin2tW/phi*(1-t4)", sin2tW_meas/PHI*(1-t4)),
    ("eta^2/(2*t4*phi)*(1-t4)", eta**2/(2*t4*PHI)*(1-t4)),
]:
    match = (1 - abs(val / V_us_meas - 1)) * 100
    if match > 99:
        print(f"    {expr_name:40s} = {val:.6f}, match = {match:.4f}%")

print()

# ==============================================================================
# 9. lambda_H deeper: propagate corrected v
# ==============================================================================
print("=" * 90)
print("9. PROPAGATING CORRECTIONS: lambda_H from corrected v and m_H")
print("-" * 90)

# m_H formula: m_H = v * sqrt((2+t4)/(3*phi^2))
m_H_meas = 125.25  # GeV
v_corrected = 246.218  # from unified_gap_closure

m_H_pred_corrected = v_corrected * math.sqrt((2 + t4) / (3 * PHI**2))
lambda_from_corrected = m_H_pred_corrected**2 / (2 * v_corrected**2)

print(f"  m_H from corrected v: {m_H_pred_corrected:.4f} GeV (measured {m_H_meas})")
print(f"  Match: {(1-abs(m_H_pred_corrected/m_H_meas-1))*100:.4f}%")
print(f"  lambda from corrected: {lambda_from_corrected:.6f} (measured {lambda_H_meas})")
print(f"  Match: {(1-abs(lambda_from_corrected/lambda_H_meas-1))*100:.4f}%")
print()

# The issue: lambda_tree = 1/(3*phi^2) gives the wrong value because
# lambda = m_H^2/(2v^2), and we need to get m_H right first
# Let's try: m_H^2 = (2+t4)*v^2/(3*phi^2)   but with loop correction to (2+t4)
for expr_name, m_H_sq_factor in [
    ("(2+t4)/(3*phi^2)", (2+t4)/(3*PHI**2)),
    ("(2+t4)/(3*phi^2)*(1+C*phi^2)", (2+t4)/(3*PHI**2)*(1+C*PHI**2)),
    ("(2+t4)/(3*phi^2)*(1+C*7/3)", (2+t4)/(3*PHI**2)*(1+C*7/3)),
    ("(2+t4)/(3*phi^2)*(1+2*C*phi^2)", (2+t4)/(3*PHI**2)*(1+2*C*PHI**2)),
    ("(2+t4+t4^2)/(3*phi^2)", (2+t4+t4**2)/(3*PHI**2)),
    ("(2+t4)/(3*phi^2-t4)", (2+t4)/(3*PHI**2-t4)),
    ("(2+2*t4)/(3*phi^2)", (2+2*t4)/(3*PHI**2)),
    ("(2+t4+eta*t4)/(3*phi^2)", (2+t4+eta*t4)/(3*PHI**2)),
]:
    m_H_pred = v_corrected * math.sqrt(m_H_sq_factor)
    lam = m_H_pred**2 / (2 * v_corrected**2)
    m_match = (1 - abs(m_H_pred / m_H_meas - 1)) * 100
    l_match = (1 - abs(lam / lambda_H_meas - 1)) * 100
    if m_match > 99.5:
        print(f"    {expr_name:40s}: m_H={m_H_pred:.4f} ({m_match:.4f}%), lam={lam:.6f} ({l_match:.2f}%)")

print()

# ==============================================================================
# SUMMARY
# ==============================================================================
print("=" * 90)
print("SUMMARY: IMPROVEMENTS FOUND")
print("=" * 90)
print()
print("  Quantity            Old Formula                      Old Match   New Formula / Status")
print("  --------            -----------                      ---------   --------------------")
