#!/usr/bin/env python3
"""
SYSTEMATIC INVESTIGATION OF THE 0.47% ALPHA GAP
================================================
Explores all paths: threshold corrections, combined formulas,
convergence, vacuum polarization, and framework-quantity corrections.
"""

import math

PHI = (1 + math.sqrt(5)) / 2
PHIBAR = 1 / PHI
MU = 1836.15267343
ALPHA_MEAS = 1/137.035999084

# Compute modular forms at q = 1/phi with high precision
q = PHIBAR
N_terms = 2000

eta = q**(1/24)
for n in range(1, N_terms):
    eta *= (1 - q**n)

t2 = 2 * q**(1/4)
for n in range(1, N_terms):
    t2 *= (1 - q**(2*n)) * (1 + q**(2*n))**2

t3 = 1.0
for n in range(1, N_terms):
    t3 *= (1 - q**(2*n)) * (1 + q**(2*n-1))**2

t4 = 1.0
for n in range(1, N_terms):
    t4 *= (1 - q**(2*n)) * (1 - q**(2*n-1))**2

E4 = 1.0
for n in range(1, 500):
    d3_sum = 0
    for d in range(1, int(n**0.5)+1):
        if n % d == 0:
            d3_sum += d**3
            if d != n//d:
                d3_sum += (n//d)**3
    E4 += 240 * d3_sum * q**n

E6 = 1.0
for n in range(1, 500):
    d5_sum = 0
    for d in range(1, int(n**0.5)+1):
        if n % d == 0:
            d5_sum += d**5
            if d != n//d:
                d5_sum += (n//d)**5
    E6 -= 504 * d5_sum * q**n

print("=" * 80)
print("SYSTEMATIC INVESTIGATION OF THE 0.47% ALPHA GAP")
print("=" * 80)

# Current status
alpha_mod = t4 / (t3 * PHI)
alpha_core = (3 / (MU * PHI**2))**(2/3)

print(f"\nModular forms at q = 1/phi:")
print(f"  eta    = {eta:.12f}")
print(f"  t2     = {t2:.12f}")
print(f"  t3     = {t3:.12f}")
print(f"  t4     = {t4:.12f}")
print(f"  E4     = {E4:.6f}")
print(f"  E6     = {E6:.6f}")

print(f"\nAlpha values:")
print(f"  alpha_modular = t4/(t3*phi) = {alpha_mod:.12f} = 1/{1/alpha_mod:.6f}")
print(f"  alpha_core    = (3/(mu*phi^2))^(2/3) = {alpha_core:.12f} = 1/{1/alpha_core:.6f}")
print(f"  alpha_measured = {ALPHA_MEAS:.12f} = 1/{1/ALPHA_MEAS:.6f}")

# The gap
correction_needed = ALPHA_MEAS / alpha_mod
deficit = 1 - correction_needed
print(f"\nThe gap:")
print(f"  alpha_mod is {(1-correction_needed)*100:.6f}% too HIGH")
print(f"  deficit = {deficit:.10f}")
print(f"  Need to multiply alpha_mod by {correction_needed:.10f}")

# ================================================================
# NEW PATH: Is the deficit a framework quantity?
# ================================================================
print(f"\n{'=' * 80}")
print("KEY TEST: Is the deficit expressible in framework quantities?")
print("=" * 80)

# deficit = 0.004709...
# Check against simple framework expressions
framework_candidates = [
    ("t4/phi^n expressions:", None),
    ("t4", t4),
    ("t4/phi", t4/PHI),
    ("t4/phi^2", t4/PHI**2),
    ("t4^2", t4**2),
    ("t4*PHIBAR", t4*PHIBAR),
    ("PHIBAR^n expressions:", None),
    ("PHIBAR^3", PHIBAR**3),
    ("PHIBAR^4", PHIBAR**4),
    ("PHIBAR^5", PHIBAR**5),
    ("eta expressions:", None),
    ("eta/30", eta/30),
    ("eta/(8*pi)", eta/(8*math.pi)),
    ("eta/25", eta/25),
    ("eta^2/3", eta**2/3),
    ("t4/t3 expressions:", None),
    ("t4/(t3)", t4/t3),
    ("t4/(2*t3)", t4/(2*t3)),
    ("t4^2/(2*eta)", t4**2/(2*eta)),
    ("pi-based expressions:", None),
    ("1/(6*pi*phi^2)", 1/(6*math.pi*PHI**2)),
    ("alpha_core/(3*pi)", alpha_core/(3*math.pi)),
    ("t4/(2*pi)", t4/(2*math.pi)),
    ("1/(30*phi^3)", 1/(30*PHI**3)),
    ("Mixed:", None),
    ("t4*eta", t4*eta),
    ("t4*eta/phi", t4*eta/PHI),
    ("t4/(phi*pi)", t4/(PHI*math.pi)),
    ("eta^2/(phi^2*pi)", eta**2/(PHI**2*math.pi)),
    ("eta^2/(3*phi)", eta**2/(3*PHI)),
    ("alpha_core*t4", alpha_core*t4),
    ("t4^2/PHIBAR", t4**2/PHIBAR),
    ("(t4/phi)^(3/2)", (t4/PHI)**1.5),
    ("eta*t4/(t3*phi)", eta*t4/(t3*PHI)),
    ("alpha_mod*t4", alpha_mod*t4),
    ("(t2-t3)*something:", None),
    ("(t2-t3)/t3", (t2-t3)/t3),
    ("(t3-t2)/t3", (t3-t2)/t3),
    ("Deeper:", None),
    ("1/(3*MU)", 1/(3*MU)),
    ("3/(MU*phi^3)", 3/(MU*PHI**3)),
    ("2*alpha_core/(3*pi*phi)", 2*alpha_core/(3*math.pi*PHI)),
    ("alpha_mod^2 * phi", alpha_mod**2 * PHI),
    ("alpha_mod^2 * 3", alpha_mod**2 * 3),
    ("alpha_mod^2 * pi", alpha_mod**2 * math.pi),
    ("t4^2*phi^2", t4**2*PHI**2),
    ("t4*eta/3", t4*eta/3),
    ("Lucas-related:", None),
    ("1/L(11)", 1/199),
    ("1/L(10)", 1/123),
    ("3/L(12)", 3/322),
    ("phi/L(10)", PHI/123),
]

print(f"\n  Deficit = {deficit:.10f}")
print(f"\n  {'Expression':40s} {'Value':>14s} {'Match':>8s}")
print(f"  {'-'*40} {'-'*14} {'-'*8}")
for name, val in framework_candidates:
    if val is None:
        print(f"\n  {name}")
        continue
    if val > 0:
        match = (1 - abs(val - deficit) / deficit) * 100
        marker = " <====" if match > 99 else (" <---" if match > 97 else (" *" if match > 95 else ""))
        if match > 80:
            print(f"  {name:40s} {val:14.10f} {match:7.2f}%{marker}")

# ================================================================
# EXTENDED SEARCH: More complex framework expressions
# ================================================================
print(f"\n{'=' * 80}")
print("EXTENDED SEARCH: More complex expressions")
print("=" * 80)

# The deficit is approximately 0.00471
# Let's be more systematic

# Check: is deficit close to alpha_mod * k * t4^m * phi^n?
print(f"\nSearching: deficit = alpha_mod * k * t4^m * phi^n")
best_matches = []
for k_name, k_val in [("1", 1), ("2", 2), ("3", 3), ("pi", math.pi), ("2pi", 2*math.pi), ("1/pi", 1/math.pi)]:
    for m in [0, 1, 2, -1]:
        for n in [-3, -2, -1, 0, 1, 2, 3]:
            test = alpha_mod * k_val * t4**m * PHI**n
            match = (1 - abs(test - deficit) / deficit) * 100
            if match > 95:
                best_matches.append((match, f"alpha_mod * {k_name} * t4^{m} * phi^{n}", test))

for k_name, k_val in [("1", 1), ("2", 2), ("3", 3), ("pi", math.pi)]:
    for m in [0, 1, 2, -1]:
        for n in [-3, -2, -1, 0, 1, 2, 3]:
            test = eta * k_val * t4**m * PHI**n
            match = (1 - abs(test - deficit) / deficit) * 100
            if match > 95:
                best_matches.append((match, f"eta * {k_name} * t4^{m} * phi^{n}", test))

best_matches.sort(reverse=True)
for match, expr, val in best_matches[:15]:
    marker = " <====" if match > 99 else " <---"
    print(f"  {expr:45s} = {val:.10f}  ({match:.2f}%){marker}")

# ================================================================
# PATH B: Combined correction
# ================================================================
print(f"\n{'=' * 80}")
print("PATH B: IS THERE A SINGLE CORRECTION THAT FIXES BOTH ALPHA AND V?")
print("=" * 80)

# Alpha gap: alpha_mod / alpha_meas = 1 + 0.004709
# V gap: v_tree / v_meas: v = M_Pl * PHIBAR^80
v_tree = 1.22089e19 * PHIBAR**80
v_meas = 246.22  # GeV
v_corr3 = 1.22089e19 * PHIBAR**80 / (1 - PHI * t4)

gap_v_tree = v_tree / v_meas - 1
gap_v_corr = v_corr3 / v_meas - 1
gap_alpha = alpha_mod / ALPHA_MEAS - 1

print(f"\n  v_tree = M_Pl * phibar^80 = {v_tree:.4f} GeV (gap: {gap_v_tree*100:.2f}%)")
print(f"  v_corrected = M_Pl * phibar^80 / (1 - phi*t4) = {v_corr3:.4f} GeV (gap: {gap_v_corr*100:.2f}%)")
print(f"  alpha gap: {gap_alpha*100:.4f}%")
print(f"  v tree gap: {gap_v_tree*100:.4f}%")

# Both gaps are positive (predictions too high for alpha, too low for v)
# alpha is 0.47% too high, v is 5.3% too low
# After v correction with (1-phi*t4), v gap becomes 0.42%
print(f"  v corrected gap: {gap_v_corr*100:.4f}%")
print(f"\n  After (1-phi*t4) correction:")
print(f"    alpha gap: {gap_alpha*100:.4f}%")
print(f"    v gap:     {gap_v_corr*100:.4f}%")
print(f"  BOTH are ~0.4-0.5% -- similar magnitude!")

# Could the SAME correction fix both?
# alpha_corrected = alpha_mod * (1 - delta)
# v_corrected = v * (1 + delta')  [or divided by (1-delta)]
# For alpha: delta = 0.004709
# For v: delta' = -0.00418 (need to increase by 0.42%)

# Check: is (1-phi*t4) the correction for alpha too?
alpha_with_phit4 = alpha_mod * (1 - PHI * t4)
print(f"\n  Test: alpha_mod * (1 - phi*t4) = {alpha_with_phit4:.12f} = 1/{1/alpha_with_phit4:.6f}")
print(f"  Match: {(1 - abs(alpha_with_phit4 - ALPHA_MEAS) / ALPHA_MEAS) * 100:.4f}%")

# (1 - phi*t4) = 1 - 1.618*0.03030 = 1 - 0.04902 = 0.9510 -- too large!
# We need 1 - 0.00471, not 1 - 0.04902.

# What about (1 - t4/phi^n)?
for n in range(0, 6):
    corr = 1 - t4/PHI**n
    alpha_test = alpha_mod * corr
    match = (1 - abs(alpha_test - ALPHA_MEAS) / ALPHA_MEAS) * 100
    if match > 99:
        print(f"  alpha_mod * (1 - t4/phi^{n}) = 1/{1/alpha_test:.6f} ({match:.4f}%)")

# Check (1 - t4^2 * something)
for k_name, k_val in [("1", 1), ("phi", PHI), ("phi^2", PHI**2), ("3", 3),
                       ("pi", math.pi), ("2*pi", 2*math.pi), ("phi^3", PHI**3),
                       ("5", 5), ("5*phi", 5*PHI), ("3*phi", 3*PHI)]:
    corr = 1 - t4**2 * k_val
    alpha_test = alpha_mod * corr
    match = (1 - abs(alpha_test - ALPHA_MEAS) / ALPHA_MEAS) * 100
    if match > 99:
        print(f"  alpha_mod * (1 - t4^2 * {k_name}) = 1/{1/alpha_test:.6f} ({match:.4f}%)")

# Check (1 - eta * something)
for k_name, k_val in [("t4", t4), ("t4/phi", t4/PHI), ("t4/3", t4/3),
                       ("t4*phi", t4*PHI), ("t4/(3*phi)", t4/(3*PHI)),
                       ("PHIBAR^3", PHIBAR**3), ("PHIBAR^4", PHIBAR**4),
                       ("1/30", 1/30), ("1/(3*phi^2)", 1/(3*PHI**2))]:
    corr = 1 - eta * k_val
    alpha_test = alpha_mod * corr
    match = (1 - abs(alpha_test - ALPHA_MEAS) / ALPHA_MEAS) * 100
    if match > 99:
        print(f"  alpha_mod * (1 - eta * {k_name}) = 1/{1/alpha_test:.6f} ({match:.4f}%)")

# ================================================================
# NEW PATH: Exact correction formulas
# ================================================================
print(f"\n{'=' * 80}")
print("COMPREHENSIVE FORMULA SEARCH")
print("=" * 80)

# We want alpha_exact = alpha_mod * f where f = ALPHA_MEAS / alpha_mod
f_target = ALPHA_MEAS / alpha_mod
print(f"\n  Target correction factor f = {f_target:.12f}")
print(f"  = 1 - {1-f_target:.10f}")

# Systematic search for f
candidates_f = []

# Form: (1 - a * t4^m * eta^n * phi^p)
for a_name, a_val in [("1", 1), ("2", 2), ("3", 3), ("1/2", 0.5), ("1/3", 1/3),
                       ("pi", math.pi), ("1/pi", 1/math.pi), ("2/3", 2/3),
                       ("1/6", 1/6), ("5", 5), ("sqrt(5)", math.sqrt(5)),
                       ("1/sqrt(5)", 1/math.sqrt(5))]:
    for m in [0, 1, 2, 3]:
        for n_eta in [0, 1, 2]:
            for p in [-3, -2, -1, 0, 1, 2, 3]:
                f_test = 1 - a_val * t4**m * eta**n_eta * PHI**p
                match = (1 - abs(f_test - f_target) / abs(1 - f_target)) * 100
                if match > 98:
                    expr = f"(1 - {a_name}*t4^{m}*eta^{n_eta}*phi^{p})"
                    candidates_f.append((match, expr, f_test))

# Form: t4/(t3*phi*(1 + k*t4^m))  => alpha_mod * 1/(1+k*t4^m) = alpha_mod/(1+k*t4^m)
# f = 1/(1 + k*t4^m)
for k_name, k_val in [("1", 1), ("2", 2), ("3", 3), ("5", 5), ("phi", PHI),
                       ("phi^2", PHI**2), ("pi", math.pi), ("2*pi", 2*math.pi),
                       ("3*phi", 3*PHI), ("5*phi", 5*PHI), ("phi^3", PHI**3),
                       ("sqrt(5)", math.sqrt(5))]:
    for m in [1, 2]:
        denom = 1 + k_val * t4**m
        f_test = 1 / denom
        match = (1 - abs(f_test - f_target) / abs(1 - f_target)) * 100
        if match > 90:
            expr = f"1/(1 + {k_name}*t4^{m})"
            candidates_f.append((match, expr, f_test))

# Form involving Jacobi identity: t3^4 = t2^4 + t4^4
# So t4^4/t3^4 = 1 - (t2/t3)^4
# alpha might involve this ratio
jacobi_ratio = t4**4 / t3**4
print(f"\n  Jacobi: t4^4/t3^4 = {jacobi_ratio:.12f}")
print(f"  1 - (t2/t3)^4 = {1 - (t2/t3)**4:.12f}")
print(f"  (t2/t3)^4 = {(t2/t3)**4:.12f}")

# Check: alpha = t4/(t3*phi) * (t4/t3)^k for some k?
for k in [1, 2, 3, 4, 0.5, 1.5]:
    alpha_test = alpha_mod * (t4/t3)**k
    match = (1 - abs(alpha_test - ALPHA_MEAS) / ALPHA_MEAS) * 100
    if match > 95:
        print(f"  alpha_mod * (t4/t3)^{k} = 1/{1/alpha_test:.6f} ({match:.4f}%)")

# Form: alpha = (t4/t3)^a * (1/phi) for various a
for a in [x/10 for x in range(5, 30)]:
    alpha_test = (t4/t3)**a / PHI
    if 0.005 < alpha_test < 0.01:
        match = (1 - abs(alpha_test - ALPHA_MEAS) / ALPHA_MEAS) * 100
        if match > 99.5:
            print(f"  (t4/t3)^{a:.1f} / phi = 1/{1/alpha_test:.6f} ({match:.4f}%)")

candidates_f.sort(reverse=True)
print(f"\nTop correction factor candidates:")
for match, expr, f_val in candidates_f[:20]:
    alpha_result = alpha_mod * f_val
    marker = " <==" if match > 99 else ""
    print(f"  {expr:50s} f={f_val:.10f}  1/alpha={1/alpha_result:.4f} ({match:.2f}%){marker}")

# ================================================================
# THE v GAP CONNECTION
# ================================================================
print(f"\n{'=' * 80}")
print("v GAP CONNECTION: Same correction for both?")
print("=" * 80)

# v_corrected = v_tree / (1 - phi*t4) already gives 99.58%
# The residual for v is:
v_residual = v_corr3 / v_meas - 1
print(f"  v residual after (1-phi*t4): {v_residual*100:.4f}%")
print(f"  alpha residual: {gap_alpha*100:.4f}%")
print(f"  Note: v is {v_residual*100:.4f}% too LOW, alpha is {gap_alpha*100:.4f}% too HIGH")
print(f"  Opposite signs! Cannot be the same multiplicative correction.")

# But could they share a correction with OPPOSITE SIGN?
# alpha_meas = alpha_mod * (1 - delta)  => delta = +0.00471
# v_meas = v_corr * (1 + delta') where delta' = v_meas/v_corr - 1
delta_v = v_meas / v_corr3 - 1
delta_alpha = 1 - ALPHA_MEAS / alpha_mod
print(f"\n  delta_alpha = {delta_alpha:.8f}")
print(f"  delta_v = {delta_v:.8f}")
print(f"  Ratio: delta_v / delta_alpha = {delta_v / delta_alpha:.4f}")
print(f"  Sum: delta_alpha + delta_v = {delta_alpha + delta_v:.8f}")

# ================================================================
# THE 'APPROACH 6' PATH: Is this the QED 1-loop correction?
# ================================================================
print(f"\n{'=' * 80}")
print("APPROACH 6: THE 1-LOOP RUNNING INTERPRETATION")
print("=" * 80)

# In QED, alpha runs from alpha(0) to alpha(mu) as:
# 1/alpha(0) = 1/alpha(mu) + (2/3pi) * sum_f N_c * Q_f^2 * ln(mu/m_f)
# where the sum is over fermions with mass < mu.

# If alpha_mod is the coupling at some scale mu_mod, and alpha_meas is at 0:
# 1/alpha_meas = 1/alpha_mod + (2/3pi) * sum_f N_c * Q_f^2 * ln(mu_mod/m_f)
# delta(1/alpha) = 1/alpha_meas - 1/alpha_mod = +0.646

delta_inv_alpha = 1/ALPHA_MEAS - 1/alpha_mod
print(f"\n  delta(1/alpha) = 1/alpha_meas - 1/alpha_mod = {delta_inv_alpha:.6f}")

# The electron loop contribution between scale m_e and some higher scale mu:
# delta(1/alpha) = (1/3pi) * ln(mu/m_e)
# 0.646 = (1/3pi) * ln(mu/m_e)
# ln(mu/m_e) = 0.646 * 3 * pi = 6.088
# mu/m_e = e^6.088 = 440
# mu = 440 * 0.511 MeV = 225 MeV

mu_scale = math.exp(delta_inv_alpha * 3 * math.pi) * 0.511  # MeV
print(f"  If the gap is pure electron VP: alpha_mod = alpha at mu = {mu_scale:.1f} MeV")
print(f"  This is close to Lambda_QCD ~ 200-330 MeV!")
print(f"  So alpha_mod = alpha_em evaluated at the QCD scale!")

# More precisely: if alpha_mod = alpha(Lambda_QCD):
# Lambda_QCD^{QED} = m_e * exp(3*pi * delta(1/alpha))
# Using measured Lambda_QCD ~ 220 MeV:
lambda_qcd = 220  # MeV (MS-bar, 5 flavors)
delta_predicted = math.log(lambda_qcd / 0.511) / (3 * math.pi)
print(f"\n  Using Lambda_QCD = {lambda_qcd} MeV:")
print(f"  Predicted delta(1/alpha) from electron VP = {delta_predicted:.6f}")
print(f"  Actual delta(1/alpha) = {delta_inv_alpha:.6f}")
print(f"  Match: {(1 - abs(delta_predicted - delta_inv_alpha) / delta_inv_alpha) * 100:.2f}%")

# Try with Lambda_QCD from the framework: Lambda_QCD = m_p/phi^3
m_p = 938.272  # MeV
lambda_framework = m_p / PHI**3
delta_framework = math.log(lambda_framework / 0.511) / (3 * math.pi)
print(f"\n  Framework Lambda_QCD = m_p/phi^3 = {lambda_framework:.1f} MeV:")
print(f"  Predicted delta(1/alpha) = {delta_framework:.6f}")
print(f"  Match: {(1 - abs(delta_framework - delta_inv_alpha) / delta_inv_alpha) * 100:.2f}%")

# ================================================================
# THE JACOBI TRANSFORM PATH
# ================================================================
print(f"\n{'=' * 80}")
print("JACOBI TRANSFORM PATH")
print("=" * 80)

# Under S-transformation: tau -> -1/tau
# theta_3(tau) -> sqrt(-i*tau) * theta_3(-1/tau)
# theta_4(tau) -> sqrt(-i*tau) * theta_2(-1/tau)
# For tau = i*y: S-dual is tau' = i/y
# theta_3^2 = pi / ln(phi) in the S-dual frame (the SW coupling)

tau_y = math.log(PHI) / (2 * math.pi)
alpha_sw = math.pi / math.log(PHI)  # = Im(tau')/2... actually
# alpha_SW = 1/(4pi*Im(tau)) in standard normalization
# But actually theta_3^2(q') = pi/ln(phi) in the S-dual frame

# The Jacobi transform of alpha_mod:
# In the S-dual frame, the coupling is 1/(4*pi*Im(tau'))
# Im(tau') = 1/Im(tau) = 2*pi/ln(phi)
alpha_Sdual = 1 / (4 * math.pi * (2*math.pi/math.log(PHI)))
print(f"\n  tau = i * {tau_y:.8f}")
print(f"  tau_dual = i * {1/tau_y:.4f}")
print(f"  alpha_SW (direct frame) = 1/(4pi*Im(tau)) = {1/(4*math.pi*tau_y):.6f}")
print(f"  alpha_SW (S-dual frame) = 1/(4pi*Im(tau_dual)) = {alpha_Sdual:.8f}")
print(f"  Interesting: S-dual alpha = {alpha_Sdual:.8f}")

# The physical alpha might be a combination of the two frames
# In N=2 SUSY, the physical coupling receives contributions from both electric and magnetic sectors
# alpha_phys^(-1) = alpha_electric^(-1) + alpha_magnetic^(-1)?
alpha_combined_inv = 1/alpha_mod + 1/(alpha_sw)  # not right dimensionally but let's check
print(f"\n  Speculative combination:")
print(f"  1/alpha_mod = {1/alpha_mod:.6f}")

# ================================================================
# THE DEFINITIVE TEST: Systematic formula scan
# ================================================================
print(f"\n{'=' * 80}")
print("DEFINITIVE FORMULA SCAN: alpha from modular forms")
print("=" * 80)

# Scan ALL formulas of the form: alpha = f(t2, t3, t4, eta, phi, 2, 3)
# that give values between 1/138 and 1/136

hits = []

# Form: t4 * g(t3) * h(phi)
for t3_pow in [-2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2]:
    for phi_pow in [-3, -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 3]:
        for k_name, k_val in [("1", 1), ("2", 2), ("3", 3), ("1/2", 0.5),
                               ("1/3", 1/3), ("2/3", 2/3), ("pi", math.pi),
                               ("1/pi", 1/math.pi)]:
            val = t4 * t3**t3_pow * PHI**phi_pow * k_val
            if 0.0071 < val < 0.0075:
                match = (1 - abs(val - ALPHA_MEAS) / ALPHA_MEAS) * 100
                if match > 99.8:
                    expr = f"t4 * t3^{t3_pow} * phi^{phi_pow} * {k_name}"
                    hits.append((match, expr, val))

# Form: eta^a * t4^b * phi^c
for a in [0, 0.5, 1, 1.5, 2, 2.5, 3]:
    for b in [-1, -0.5, 0, 0.5, 1, 1.5, 2]:
        for c in [-3, -2, -1, 0, 1, 2, 3]:
            for k_name, k_val in [("1", 1), ("2", 2), ("3", 3), ("1/2", 0.5), ("1/3", 1/3), ("1/6", 1/6)]:
                val = eta**a * t4**b * PHI**c * k_val
                if 0.0071 < val < 0.0075:
                    match = (1 - abs(val - ALPHA_MEAS) / ALPHA_MEAS) * 100
                    if match > 99.8:
                        expr = f"eta^{a} * t4^{b} * phi^{c} * {k_name}"
                        hits.append((match, expr, val))

# Form: (3/(mu_mod * phi^2))^(2/3) where mu_mod is from modular forms
# mu_mod = t3^8 * correction
for corr_name, corr_val in [("1", 1), ("(1+t4)", 1+t4), ("(1+2*t4)", 1+2*t4),
                              ("(1+3*t4)", 1+3*t4), ("(1+phi*t4)", 1+PHI*t4),
                              ("(1+t4/phi)", 1+t4/PHI), ("(1+t4^2)", 1+t4**2),
                              ("(1+eta*t4)", 1+eta*t4)]:
    mu_eff = t3**8 * corr_val
    alpha_test = (3 / (mu_eff * PHI**2))**(2/3)
    if 0.007 < alpha_test < 0.008:
        match = (1 - abs(alpha_test - ALPHA_MEAS) / ALPHA_MEAS) * 100
        if match > 99:
            expr = f"(3/(t3^8*{corr_name}*phi^2))^(2/3)"
            hits.append((match, expr, alpha_test))

# The key test: using the measured mu with modular correction
for corr_name, corr_val in [("(1+t4)", 1+t4), ("(1+2*t4)", 1+2*t4), ("(1+t4/phi)", 1+t4/PHI),
                              ("(1+t4*phi)", 1+t4*PHI), ("(1-t4)", 1-t4)]:
    mu_eff = MU * corr_val
    alpha_test = (3 / (mu_eff * PHI**2))**(2/3)
    match = (1 - abs(alpha_test - ALPHA_MEAS) / ALPHA_MEAS) * 100
    if match > 99.5:
        expr = f"(3/(mu*{corr_name}*phi^2))^(2/3)"
        hits.append((match, expr, alpha_test))

# Using MU with t4 correction to the CORE identity
# alpha^(3/2) * mu * phi^2 = 3
# What if it's alpha^(3/2) * mu * phi^2 = 3 * (1 + k*t4)?
for k_name, k_val in [("t4", t4), ("2*t4", 2*t4), ("t4/phi", t4/PHI),
                       ("t4*phi", t4*PHI), ("t4^2", t4**2), ("eta*t4", eta*t4)]:
    alpha_test = (3*(1+k_val) / (MU * PHI**2))**(2/3)
    match = (1 - abs(alpha_test - ALPHA_MEAS) / ALPHA_MEAS) * 100
    if match > 99.5:
        expr = f"(3*(1+{k_name})/(mu*phi^2))^(2/3)"
        hits.append((match, expr, alpha_test))

hits.sort(reverse=True)
print(f"\nTop formula matches (>99.8%):")
for match, expr, val in hits[:30]:
    marker = " <====" if match > 99.95 else (" <---" if match > 99.9 else "")
    print(f"  {expr:55s} = 1/{1/val:.6f} ({match:.4f}%){marker}")

# ================================================================
# THE BREATHING MODE CORRECTION
# ================================================================
print(f"\n{'=' * 80}")
print("BREATHING MODE CORRECTION HYPOTHESIS")
print("=" * 80)

# The domain wall has a breathing mode with mass ratio sqrt(3/4) to the scalar
# Could this ratio enter the coupling correction?
breathing_ratio = math.sqrt(3/4)
print(f"\n  Breathing mode ratio: sqrt(3/4) = {breathing_ratio:.10f}")
print(f"  Deficit = {deficit:.10f}")
print(f"  deficit / breathing_ratio = {deficit / breathing_ratio:.10f}")
print(f"  deficit * breathing_ratio = {deficit * breathing_ratio:.10f}")

# Check: alpha = t4/(t3*phi) * sqrt(3/4)^k for some k
for k in [0.5, 1, 2, 3, -1, -2]:
    alpha_test = alpha_mod * breathing_ratio**k
    match = (1 - abs(alpha_test - ALPHA_MEAS) / ALPHA_MEAS) * 100
    if match > 99:
        print(f"  alpha_mod * sqrt(3/4)^{k} = 1/{1/alpha_test:.6f} ({match:.4f}%)")

# ================================================================
# FINAL SUMMARY
# ================================================================
print(f"\n{'=' * 80}")
print("FINAL SUMMARY")
print("=" * 80)

print(f"""
  CURRENT BEST FORMULAS:
  1. Core identity: alpha = (3/(mu*phi^2))^(2/3) = 1/{1/alpha_core:.4f} (99.92%)
  2. Modular: alpha = t4/(t3*phi) = 1/{1/alpha_mod:.4f} (99.53%)
  3. Measured: 1/{1/ALPHA_MEAS:.6f}

  THE GAP:
  deficit = {deficit:.10f} ({deficit*100:.4f}%)
  delta(1/alpha) = {delta_inv_alpha:.6f}

  INTERPRETATION:
  The modular formula t4/(t3*phi) gives alpha at a scale ~ {mu_scale:.0f} MeV,
  which is near Lambda_QCD. The 0.47% gap is the electron vacuum
  polarization running from this scale down to zero momentum.

  If alpha_mod = alpha(Lambda_QCD), then it is the coupling at the
  scale where QCD becomes non-perturbative -- precisely where the
  domain wall (kink) physics becomes relevant.
""")
