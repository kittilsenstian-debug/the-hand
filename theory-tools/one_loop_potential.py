#!/usr/bin/env python3
"""
one_loop_potential.py — One-Loop Effective Potential for V(Phi)
==============================================================

THE QUESTION:
The phibar corrections found empirically in path_to_100.py bring
18/18 derivations above 99%. But they were found by search, not derived.
Can we DERIVE them from the one-loop effective potential?

THE METHOD:
Coleman-Weinberg (1973) one-loop effective potential:

    V_eff(Phi) = V_tree(Phi) + V_1loop(Phi)

    V_1loop = (1/(64*pi^2)) * sum_i (-1)^F_i * n_i * M_i^4(Phi)
              * [ln(M_i^2(Phi)/mu_R^2) - c_i]

where:
    M_i(Phi) = field-dependent mass of species i
    n_i = degrees of freedom
    F_i = 0 for bosons, 1 for fermions
    mu_R = renormalization scale
    c_i = 3/2 for scalars/fermions (MS-bar), 5/6 for gauge bosons

For V(Phi) = lambda*(Phi^2 - Phi - 1)^2:

    Scalar mass: M_scalar^2 = V''(Phi) = lambda * [12*Phi^2 - 6*Phi - 4 + ...]
    Gauge boson masses: M_gauge^2 = g^2 * Phi^2 / 4  (for Higgs-like coupling)
    Fermion masses: M_f^2 = y_f^2 * f^2(x_f) * Phi^2 / 2

We evaluate at both vacua (phi and -1/phi) and compute the SHIFT
in observable quantities.

REFERENCES:
    - Coleman & Weinberg (1973) Phys.Rev.D 7:1888
    - Quiros (1999) hep-ph/9901312 "Finite temperature field theory"
    - Ford, Jones, Stephenson, Einhorn (1993) hep-ph/9305305
"""

import math
import numpy as np

phi = (1 + math.sqrt(5)) / 2       # 1.618033988...
phibar = 1 / phi                     # 0.618033988...
phi2 = phi * phi                     # 2.618033988...
sqrt5 = math.sqrt(5)
mu_p = 1836.15267343                 # proton-to-electron mass ratio
alpha_em = 1/137.035999084
h_cox = 30                           # Coxeter number of E8
N = 7776                             # = 6^5

def L(n):
    """Lucas number: L(n) = phi^n + (-phibar)^n"""
    return phi**n + (-phibar)**n

print("="*70)
print("ONE-LOOP EFFECTIVE POTENTIAL FOR V(Phi) = lambda*(Phi^2-Phi-1)^2")
print("="*70)

# ============================================================
# PART 1: TREE-LEVEL ANALYSIS
# ============================================================
print("""
================================================================
PART 1: TREE-LEVEL POTENTIAL AND ITS DERIVATIVES
================================================================
""")

# V(Phi) = lambda * (Phi^2 - Phi - 1)^2
# Let's define W(Phi) = Phi^2 - Phi - 1  so V = lambda * W^2

# Derivatives:
# W'(Phi)  = 2*Phi - 1
# V'(Phi)  = 2*lambda * W * W' = 2*lambda*(Phi^2-Phi-1)*(2*Phi-1)
# V''(Phi) = 2*lambda*[W'*W' + W*W''] = 2*lambda*[(2Phi-1)^2 + (Phi^2-Phi-1)*2]
#          = 2*lambda*[4Phi^2 - 4Phi + 1 + 2Phi^2 - 2Phi - 2]
#          = 2*lambda*[6Phi^2 - 6Phi - 1]

lam = 1 / (3 * phi2)  # lambda = 1/(3*phi^2) from framework

def V(Phi):
    W = Phi**2 - Phi - 1
    return lam * W**2

def Vprime(Phi):
    W = Phi**2 - Phi - 1
    Wp = 2*Phi - 1
    return 2*lam * W * Wp

def Vpp(Phi):
    """V''(Phi) — the scalar mass-squared at field value Phi"""
    return 2*lam * (6*Phi**2 - 6*Phi - 1)

# Evaluate at both vacua
for vac_name, vac_val in [("phi vacuum", phi), ("-1/phi vacuum", -phibar)]:
    print(f"  At {vac_name} (Phi = {vac_val:.6f}):")
    print(f"    V(Phi)   = {V(vac_val):.10f}  (should be 0)")
    print(f"    V'(Phi)  = {Vprime(vac_val):.10f}  (should be 0)")
    print(f"    V''(Phi) = {Vpp(vac_val):.10f}  (scalar mass^2 in lambda units)")
    print()

# At phi: V'' = 2*lam*(6*phi^2 - 6*phi - 1) = 2*lam*(6*(phi+1) - 6*phi - 1) = 2*lam*(6+6-6-1... wait
# phi^2 = phi + 1, so 6*phi^2 = 6*phi + 6
# V''(phi) = 2*lam*(6*phi+6-6*phi-1) = 2*lam*5 = 10*lam
m2_scalar_phi = Vpp(phi)
m2_scalar_dark = Vpp(-phibar)

print(f"  Scalar mass^2 at phi vacuum:    V''(phi)   = 10*lambda = {m2_scalar_phi:.6f}")
print(f"  Scalar mass^2 at dark vacuum:   V''(-1/phi) = 10*lambda = {m2_scalar_dark:.6f}")
print(f"  (Both equal by vacuum symmetry Phi -> 1/2 - (Phi - 1/2) = 1-Phi)")
print(f"  V''(-1/phi) = 2*lam*(6*phibar^2 + 6*phibar - 1)")
val_check = 2*lam*(6*phibar**2 + 6*phibar - 1)
print(f"  Check: 6*phibar^2 + 6*phibar - 1 = 6*(2-phi) + 6*phibar - 1 = {6*phibar**2+6*phibar-1:.6f}")
print(f"  = {val_check:.6f}")

# KEY: The two vacua give EQUAL scalar masses. Symmetry Phi -> 1 - Phi.

# ============================================================
# PART 2: COLEMAN-WEINBERG ONE-LOOP CORRECTION
# ============================================================
print(f"""
================================================================
PART 2: COLEMAN-WEINBERG ONE-LOOP POTENTIAL
================================================================

    V_1loop(Phi) = (1/(64*pi^2)) * Str[M^4(Phi) * (ln(M^2/mu_R^2) - c)]

    where Str = supertrace = sum over bosons - sum over fermions.

    For our theory, the field-dependent masses come from:

    A. SCALAR FLUCTUATION around Phi:
       M_scalar^2(Phi) = V''(Phi) = 2*lambda*(6*Phi^2 - 6*Phi - 1)

    B. GAUGE BOSONS (coupled via E8):
       M_W^2(Phi) ~ g^2 * Phi^2 / 4  (for each broken generator)

    C. FERMIONS (domain wall mechanism):
       M_f^2(Phi) = y_f^2 * Phi^2  (position-dependent Yukawa)

    The KEY is: at the phi vacuum, V_1loop shifts the vacuum energy
    and the scalar mass. This shifts all derived quantities.
""")

# Number of degrees of freedom from the SM content
# In the SM at the electroweak scale:
n_W = 6          # W+, W- (3 polarizations each)
n_Z = 3          # Z (3 polarizations)
n_H = 1          # Higgs (1 real scalar after SSB)
n_Goldstone = 3  # eaten by W+, W-, Z
n_top = 12       # top quark (3 colors * 2 spins * 2 particle/antiparticle)
n_bottom = 12    # etc for other quarks
n_leptons = 4    # tau (2 spins * 2)

# In E8 framework:
# 248 generators, of which 12 remain unbroken (SM gauge bosons)
# So 248 - 12 = 236 broken generators -> 236 massive gauge bosons at high scale
# At low energy, only the SM content matters

print("  Degrees of freedom (low-energy SM content):")
print(f"    Scalar (Higgs):  n_H = {n_H}")
print(f"    W bosons:        n_W = {n_W}")
print(f"    Z boson:         n_Z = {n_Z}")
print(f"    Top quark:       n_t = {n_top}")
print(f"    (Other fermions contribute but are mass-suppressed)")

# ============================================================
# PART 3: COMPUTE V_1LOOP AT BOTH VACUA
# ============================================================
print(f"""
================================================================
PART 3: THE LOOP EXPANSION PARAMETER
================================================================

    The key question: what is the EXPANSION PARAMETER for loops?

    In standard QFT:  loop factor ~ g^2/(16*pi^2) ~ 0.001 to 0.01

    In our framework, the natural expansion parameter should be
    related to the coupling constants of the theory.

    HYPOTHESIS: The loop expansion parameter is phibar^2.

    WHY? Because:
    1. phibar = 1/phi = 0.618... is the coupling to the dark vacuum
    2. phibar^2 = 0.382... = 2 - phi = 3 - phi^2
    3. Tree-level uses phi (visible vacuum)
    4. First correction should be phibar^2 (one trip to dark vacuum and back)
    5. phibar^2 / (4*pi) = 0.030... ~ alpha_em/137 * mu ~ same order

    Let's CHECK: is phibar^2/(4*pi) close to any known loop factor?
""")

loop_phibar2 = phibar**2
loop_standard = 1 / (16 * math.pi**2)   # ~ 0.00633
loop_phibar2_4pi = phibar**2 / (4 * math.pi)   # ~ 0.0304

print(f"  phibar^2 = {loop_phibar2:.6f}")
print(f"  phibar^2/(4*pi) = {loop_phibar2_4pi:.6f}")
print(f"  1/(16*pi^2) = {loop_standard:.6f}  (standard loop factor)")
print(f"  lambda = {lam:.6f}")
print(f"  lambda * phibar^2 = {lam * loop_phibar2:.6f}")
print(f"  lambda / (16*pi^2) = {lam / (16*math.pi**2):.6f}")

# ============================================================
# PART 4: EXPLICIT COLEMAN-WEINBERG COMPUTATION
# ============================================================
print(f"""
================================================================
PART 4: EXPLICIT COMPUTATION OF V_1LOOP
================================================================

    V_1loop = (1/(64*pi^2)) * sum_i [n_i * (-1)^F_i * M_i^4(Phi)
              * (ln(M_i^2(Phi)/mu_R^2) - c_i)]

    We evaluate this for the dominant contributions: scalar self-coupling
    and top quark.

    Renormalization scale: mu_R^2 = M_scalar^2(phi) = V''(phi) = 10*lambda
    (choosing the scale at the vacuum eliminates the log for the scalar)
""")

# The renormalization scale
mu_R_sq = 10 * lam  # V''(phi) in dimensionless units

# A: SCALAR CONTRIBUTION at the phi vacuum
# M_scalar^2(phi) = 10*lambda (we just computed this)
# In the CW formula with mu_R^2 = M_scalar^2(phi):
# V_scalar_1loop = (1/(64*pi^2)) * 1 * (10*lam)^2 * (ln(1) - 3/2)
#                = (1/(64*pi^2)) * 100*lam^2 * (-3/2)
# This just renormalizes the cosmological constant at the vacuum

print("  A. SCALAR self-energy contribution:")
scalar_CW = (1/(64*math.pi**2)) * 1 * (10*lam)**2 * (-3/2)
print(f"     V_scalar_1loop(phi) = {scalar_CW:.8f} (in lambda units)")

# B: TOP QUARK CONTRIBUTION
# m_t ~ y_t * phi * v/sqrt(2)
# In dimensionless units (measuring everything in units of the VEV):
# M_t^2(Phi) = y_t^2 * Phi^2
# y_t ~ 1 (top Yukawa is order 1 in SM)
y_t = 1.0  # approximate
M_t_sq_phi = y_t**2 * phi**2

print(f"\n  B. TOP QUARK contribution:")
print(f"     M_t^2(phi) = y_t^2 * phi^2 = {M_t_sq_phi:.6f}")
top_CW = -(1/(64*math.pi**2)) * n_top * M_t_sq_phi**2 * (math.log(M_t_sq_phi/mu_R_sq) - 3/2)
print(f"     V_top_1loop(phi) = {top_CW:.8f}")

# C: GAUGE BOSON CONTRIBUTION
# M_W^2(Phi) = g^2 * Phi^2 / 4
g_weak = math.sqrt(4 * math.pi * alpha_em / 0.23121)  # g from alpha and sin^2(theta_W)
M_W_sq_phi = g_weak**2 * phi**2 / 4

print(f"\n  C. GAUGE BOSON contribution (W, Z):")
print(f"     g_weak = {g_weak:.6f}")
print(f"     M_W^2(phi) = {M_W_sq_phi:.6f}")
gauge_CW = (1/(64*math.pi**2)) * (n_W + n_Z) * M_W_sq_phi**2 * (math.log(M_W_sq_phi/mu_R_sq) - 5/6)
print(f"     V_gauge_1loop(phi) = {gauge_CW:.8f}")

print(f"\n  TOTAL 1-LOOP CORRECTION at phi vacuum:")
V1_total = scalar_CW + top_CW + gauge_CW
print(f"     V_1loop(phi) = {V1_total:.8f}")
print(f"     V_tree(phi)  = {V(phi):.8f}  (= 0 by construction)")
print(f"     Ratio V_1loop/V''_tree = {abs(V1_total)/(10*lam):.6f}")

# ============================================================
# PART 5: SHIFT IN VACUUM POSITION
# ============================================================
print(f"""
================================================================
PART 5: SHIFT IN THE VACUUM POSITION
================================================================

    The one-loop correction shifts the vacuum from phi to phi + delta_phi.

    From V_eff'(phi + delta) = 0:
    delta_phi = -V_1loop'(phi) / V_tree''(phi)

    V_1loop'(Phi) comes from differentiating the CW potential.

    For the SCALAR part:
    d/dPhi [M_s^4 * (ln(M_s^2/mu^2) - 3/2)]
    = d/dPhi [(V''(Phi))^2 * (ln(V''/mu^2) - 3/2)]

    This is complex. Let's compute NUMERICALLY.
""")

# Numerical derivative of V_1loop
def V_1loop(Phi):
    """Full one-loop CW potential at field value Phi"""
    # Scalar mass squared
    M_s_sq = Vpp(Phi)
    if M_s_sq <= 0:
        return 0  # tachyonic region, skip

    # Top quark
    M_t_sq = y_t**2 * Phi**2
    if M_t_sq <= 0:
        M_t_sq = 1e-30

    # W/Z bosons
    M_W_sq = g_weak**2 * Phi**2 / 4
    if M_W_sq <= 0:
        M_W_sq = 1e-30

    result = 0
    # Scalar (n=1, boson, c=3/2)
    if M_s_sq > 0:
        result += (1/(64*math.pi**2)) * 1 * M_s_sq**2 * (math.log(abs(M_s_sq/mu_R_sq)) - 3/2)

    # Top quark (n=12, fermion, c=3/2)
    result -= (1/(64*math.pi**2)) * n_top * M_t_sq**2 * (math.log(abs(M_t_sq/mu_R_sq)) - 3/2)

    # Gauge bosons (n=9, boson, c=5/6)
    if M_W_sq > 0:
        result += (1/(64*math.pi**2)) * (n_W+n_Z) * M_W_sq**2 * (math.log(abs(M_W_sq/mu_R_sq)) - 5/6)

    return result

def V_eff(Phi):
    return V(Phi) + V_1loop(Phi)

# Find the shifted vacuum numerically
eps = 1e-8
Phi_vals = np.linspace(phi - 0.1, phi + 0.1, 10000)
V_effs = [V_eff(p) for p in Phi_vals]
min_idx = np.argmin(V_effs)
phi_shifted = Phi_vals[min_idx]

# Refine
Phi_vals2 = np.linspace(phi_shifted - 0.001, phi_shifted + 0.001, 100000)
V_effs2 = [V_eff(p) for p in Phi_vals2]
min_idx2 = np.argmin(V_effs2)
phi_shifted = Phi_vals2[min_idx2]

delta_phi = phi_shifted - phi

print(f"  Tree-level vacuum:     Phi_0 = {phi:.10f}")
print(f"  One-loop vacuum:       Phi_1 = {phi_shifted:.10f}")
print(f"  Shift:                 delta  = {delta_phi:.10f}")
print(f"  Relative shift:        delta/phi = {delta_phi/phi:.8f}")
print(f"  delta/phibar^2 = {delta_phi/phibar**2:.8f}")

# Also check the dark vacuum
Phi_vals_dark = np.linspace(-phibar - 0.1, -phibar + 0.1, 10000)
V_effs_dark = [V_eff(p) for p in Phi_vals_dark]
min_idx_dark = np.argmin(V_effs_dark)
dark_shifted = Phi_vals_dark[min_idx_dark]
delta_dark = dark_shifted - (-phibar)

print(f"\n  Dark vacuum tree:      Phi_0 = {-phibar:.10f}")
print(f"  Dark vacuum one-loop:  Phi_1 = {dark_shifted:.10f}")
print(f"  Shift:                 delta  = {delta_dark:.10f}")

# ============================================================
# PART 6: DO THE SHIFTS EXPLAIN PHIBAR CORRECTIONS?
# ============================================================
print(f"""
================================================================
PART 6: CONNECTING LOOP CORRECTIONS TO PHIBAR TERMS
================================================================

    The empirical corrections from path_to_100.py all have the form:
    Q_corrected = Q_tree + (p/q) * phibar^n

    If these come from the one-loop potential, then:
    delta_Q / Q_tree ~ V_1loop / V_tree ~ lambda / (16*pi^2)

    Let's compute what the ONE-LOOP correction PREDICTS for each
    quantity and compare to the empirical phibar corrections.

    The key insight: when a quantity depends on Phi at the vacuum,
    Q = Q(phi), then the one-loop correction is:
    delta_Q = Q'(phi) * delta_phi + (1/2) * Q''(phi) * delta_phi^2 + ...

    For quantities like mu = N/Phi^3:
    delta_mu / mu = -3 * delta_phi / phi
""")

# Compute predictions for key quantities
print("  QUANTITY-BY-QUANTITY PREDICTIONS:")
print(f"  {'Quantity':<20} {'Tree':>10} {'delta(1-loop)':>14} {'delta/tree':>12} {'Empirical':>12} {'Match?':>8}")
print("  " + "-"*80)

# mu = N/phi^3
mu_tree = N / phi**3
delta_mu = -3 * mu_tree * delta_phi / phi  # d(1/phi^3)/dphi = -3/phi^4
mu_empirical = phibar**2 / 1  # from path_to_100: +1/1*phibar^2
print(f"  {'mu':.<20} {mu_tree:>10.4f} {delta_mu:>+14.6f} {delta_mu/mu_tree:>+12.8f} {mu_empirical:>+12.6f}")

# alpha_s = 1/(2*phi^3)
alpha_s_tree = 1/(2*phi**3)
delta_alpha_s = -3 * alpha_s_tree * delta_phi / phi
alpha_s_emp = -phibar**10/60  # from path_to_100: -1/60*phibar^10
print(f"  {'alpha_s':.<20} {alpha_s_tree:>10.6f} {delta_alpha_s:>+14.8f} {delta_alpha_s/alpha_s_tree:>+12.8f} {alpha_s_emp:>+12.8f}")

# Omega_DM = phi/6
Omega_tree = phi/6
delta_Omega = delta_phi / 6  # d(phi/6)/dphi = 1/6
Omega_emp = -phibar**5/60  # from path_to_100: -1/60*phibar^5
print(f"  {'Omega_DM':.<20} {Omega_tree:>10.6f} {delta_Omega:>+14.8f} {delta_Omega/Omega_tree:>+12.8f} {Omega_emp:>+12.8f}")

# V_us = phi/7
V_us_tree = phi/7
delta_V_us = delta_phi/7
V_us_emp = -phibar**3/40  # from path_to_100
print(f"  {'V_us':.<20} {V_us_tree:>10.6f} {delta_V_us:>+14.8f} {delta_V_us/V_us_tree:>+12.8f} {V_us_emp:>+12.8f}")

# n_s = 1 - 1/h (no phi dependence!)
ns_emp = -phibar**4/60
print(f"  {'n_s':.<20} {'0.96667':>10} {'no phi dep':>14} {'—':>12} {ns_emp:>+12.8f}")

# dm2_ratio = 33 (no phi dependence!)
dm2_emp = -phibar**2/1
print(f"  {'dm2_ratio':.<20} {'33':>10} {'no phi dep':>14} {'—':>12} {dm2_emp:>+12.8f}")

# ============================================================
# PART 7: THE DEEPER STRUCTURE — WHAT THE LOOP REVEALS
# ============================================================
print(f"""
================================================================
PART 7: WHAT THE LOOP CALCULATION ACTUALLY REVEALS
================================================================

    RESULT 1: The vacuum shift delta_phi is TINY ({delta_phi:.2e}).
    This is because V''(phi) = 10*lambda is relatively large,
    making the vacuum very stiff.

    RESULT 2: The vacuum shift goes as:
    delta_phi ~ lambda / (16*pi^2) * (stuff of order 1)
    ~ {lam / (16*math.pi**2):.6f}

    RESULT 3: The empirical phibar corrections are MUCH LARGER:
    phibar^2 = {phibar**2:.6f}
    phibar^3 = {phibar**3:.6f}

    This means: THE PHIBAR CORRECTIONS DO NOT COME FROM
    STANDARD COLEMAN-WEINBERG ONE-LOOP CORRECTIONS.

    They are TOO LARGE by a factor of ~{phibar**2 / (lam/(16*math.pi**2)):.0f}.

    IMPLICATION: If the phibar corrections are real, they come from
    a DIFFERENT mechanism than perturbative loop corrections.
""")

# ============================================================
# PART 8: WHAT COULD THE PHIBAR CORRECTIONS ACTUALLY BE?
# ============================================================
print(f"""
================================================================
PART 8: ALTERNATIVE ORIGINS FOR PHIBAR CORRECTIONS
================================================================

    If not perturbative loops, what could generate corrections of
    order phibar^n?

    HYPOTHESIS A: DOMAIN WALL TUNNELING
    =================================
    Non-perturbative effects (instantons/tunneling) between vacua
    go as exp(-S_bounce). For a domain wall:

    S_bounce ~ wall_tension * Volume / T
             ~ (delta_V * delta_Phi / lambda) * L^3

    The tunneling amplitude goes as exp(-S) which for a thin wall
    could give corrections of order exp(-c/lambda) rather than
    exp(-1/g^2).

    In our case: the "bounce" between phi and -1/phi crosses
    a barrier of height V(1/2) = lambda*(1/4 - 1/2 - 1)^2 = lambda * 25/16.
""")

V_barrier = V(0.5)
print(f"    Barrier height: V(1/2) = lambda * (1/4-1/2-1)^2 = lambda * {(0.25-0.5-1)**2:.4f}")
print(f"    = {V_barrier:.6f}")
print(f"    sqrt(2*V_barrier) = {math.sqrt(2*V_barrier):.6f}")

# Domain wall tension (energy per unit area)
# sigma = integral dx [V(Phi(x)) + (1/2)(dPhi/dx)^2]
# For our kink: dPhi/dx = (sqrt5/2) * (1/2delta) * sech^2(x/2delta)
# sigma ~ sqrt(2*lambda) * (delta_Phi)^3 / 6 for phi^4
delta_Phi = phi - (-phibar)  # = sqrt(5)
sigma_wall = math.sqrt(2 * lam) * delta_Phi**3 / 6
print(f"    Wall tension sigma ~ sqrt(2*lambda) * (sqrt5)^3 / 6 = {sigma_wall:.6f}")

# Thin-wall bounce action (1D)
# S_1D ~ sigma * delta_Phi / V_barrier
# For degenerate vacua this is actually infinite (no tunneling needed)
# but for SHIFTED vacua (from loop effects), it's finite
print(f"""
    For DEGENERATE vacua: tunneling amplitude is NOT suppressed!
    The two vacua have V(phi) = V(-1/phi) = 0 exactly.
    There is NO barrier penalty for the wall itself.

    The domain wall is a ZERO-ENERGY field configuration.
    Domain wall excitations (bound states) contribute to
    the partition function with weight proportional to
    exp(-m_bound * beta) where m_bound is the bound state mass.

    DOMAIN WALL BOUND STATES:
""")

# ============================================================
# PART 9: DOMAIN WALL BOUND STATES AND THEIR CONTRIBUTION
# ============================================================

# The kink in phi^4 theory has exactly TWO bound states:
# 1. Zero mode: m_0 = 0 (translation)
# 2. Breathing mode: m_1 = sqrt(3/2) * m_scalar

m_scalar = math.sqrt(10 * lam)  # in natural units
m_breathing = math.sqrt(3) * m_scalar / math.sqrt(2)
m_breathing_alt = math.sqrt(3/2) * m_scalar

print(f"    Scalar mass:       m_s = sqrt(10*lambda) = {m_scalar:.6f}")
print(f"    Breathing mode:    m_1 = sqrt(3/2)*m_s = {m_breathing_alt:.6f}")
print(f"    Ratio m_1/m_s = sqrt(3/2) = {math.sqrt(3/2):.6f}")
print(f"    (In GeV: m_1 ~ sqrt(3/2) * 125 = {math.sqrt(3/2)*125:.1f} GeV)")

# The breathing mode contributes to the EFFECTIVE potential at the vacuum
# as a thermal/quantum fluctuation. Its contribution to observables is:
# delta_Q ~ (m_1/M)^2 * Q_tree ~ (3/2) * (m_scalar/M)^2 * Q_tree

# KEY QUESTION: What is the ratio m_1/M where M is the relevant scale?

# In the framework: m_scalar ~ m_H = 125 GeV, M ~ v = 246 GeV
ratio_mH_v = 125.0 / 246.0
print(f"\n    Ratio m_H/v = {ratio_mH_v:.6f}")
print(f"    (m_H/v)^2 = {ratio_mH_v**2:.6f}")
print(f"    phibar^2 = {phibar**2:.6f}")
print(f"    Ratio: phibar^2 / (m_H/v)^2 = {phibar**2/ratio_mH_v**2:.4f}")

print(f"""
    INTERESTING: phibar^2 = {phibar**2:.4f} and (m_H/v)^2 = {ratio_mH_v**2:.4f}
    are within a factor of {phibar**2/ratio_mH_v**2:.1f} of each other.

    But they're NOT equal. So the breathing mode alone doesn't explain it.
""")

# ============================================================
# PART 10: THE SELF-REFERENTIAL EXPANSION
# ============================================================
print(f"""
================================================================
PART 9: THE SELF-REFERENTIAL EXPANSION
================================================================

    HYPOTHESIS B: SELF-REFERENTIAL PERTURBATION THEORY
    ===================================================

    The potential V(Phi) = lambda*(Phi^2-Phi-1)^2 is SELF-REFERENTIAL:
    its roots ARE the coefficients that define it.

    Phi^2 - Phi - 1 = 0  =>  Phi = phi  (the vacuum IS the equation)

    Standard perturbation theory expands around one vacuum:
    Phi = phi + delta

    But this theory says: the expansion parameter should be
    determined by the theory ITSELF, not imposed externally.

    The natural expansion is in powers of phibar = 1/phi,
    because phibar is the RATIO of the two vacua:

    |dark vacuum| / |visible vacuum| = phibar/phi = phibar^2 = {phibar**2:.6f}

    This gives: corrections ~ phibar^(2n) for the n-th order,
    where each power of phibar^2 represents one "round trip"
    from the visible vacuum to the dark vacuum and back.
""")

# Compute what self-referential expansion predicts
print("    SELF-REFERENTIAL CORRECTIONS (phibar^2 = dark/visible ratio):")
print()
for n in range(1, 8):
    corr = phibar**(2*n)
    print(f"    Order {n}: phibar^{2*n} = {corr:.8f}  ({corr*100:.4f}%)")

print(f"""
    The tree-level residuals are typically 0.1-3%.

    phibar^2 = {phibar**2:.4f} = 38.2%  -> too large for most residuals
    phibar^3 = {phibar**3:.4f} = 23.6%  -> still too large
    phibar^4 = {phibar**4:.4f} = 14.6%  -> large
    phibar^5 = {phibar**5:.6f} = 9.0%   -> possible
    ...
    phibar^8 = {phibar**8:.6f} = 2.1%   -> matches typical residuals!
    phibar^9 = {phibar**9:.6f} = 1.3%
    phibar^10 = {phibar**10:.6f} = 0.8%
    phibar^12 = {phibar**12:.6f} = 0.3%

    The typical residuals (1-3%) correspond to phibar^7 through phibar^10.

    But the EMPIRICAL corrections from path_to_100.py use:
    - Coefficients (p/q) where q comes from framework elements
    - Powers n = 2 through 13

    The combination (p/q)*phibar^n gives the RIGHT SIZE when
    q ~ 30-60 and n ~ 2-5 (i.e., phibar^n/q ~ 0.01-0.03).
""")

# ============================================================
# PART 10: HONEST ASSESSMENT
# ============================================================
print(f"""
================================================================
PART 10: HONEST ASSESSMENT — WHAT DID WE LEARN?
================================================================

    1. STANDARD CW ONE-LOOP: Does NOT explain phibar corrections.
       The loop factor lambda/(16*pi^2) ~ {lam/(16*math.pi**2):.6f} is too small
       by a factor of ~{phibar**2 / (lam/(16*math.pi**2)):.0f} compared to phibar^2.

    2. DOMAIN WALL BOUND STATES: Breathing mode mass ratio
       m_1/v ~ {math.sqrt(3/2)*125/246:.4f} is close to phibar = {phibar:.4f}
       but not exact. This is SUGGESTIVE but not a derivation.

    3. SELF-REFERENTIAL EXPANSION: The idea that corrections go as
       phibar^n (dark-to-visible ratio) is aesthetically consistent
       with the framework but is NOT derived from any Lagrangian.

    4. THE EMPIRICAL CORRECTIONS ARE REAL in the sense that:
       - They USE framework elements (h=30, L(n), |S3|=6)
       - They SYSTEMATICALLY improve all 18 quantities
       - The pattern (phibar^n with framework coefficients) is consistent

    5. BUT: We cannot currently DERIVE them from first principles.
       The theoretical gap remains:

       WHAT IS NEEDED:
       a) A non-perturbative calculation (instanton, lattice, or exact)
          of the effective potential including domain wall contributions
       b) OR: a proof that the self-referential structure of
          V(Phi) = lambda*(Phi^2-Phi-1)^2 REQUIRES corrections
          to go as phibar^n with specific algebraic coefficients
       c) OR: an alternative mechanism entirely

    BOTTOM LINE:
    The phibar corrections are currently an EMPIRICAL PATTERN,
    not a derived result. They are consistent with the framework
    but could also be coincidental curve-fitting.

    The one-loop CW potential tells us perturbative corrections
    are ~100x too small to explain the pattern, so if the pattern
    is real, something NON-PERTURBATIVE is happening.
""")

# ============================================================
# PART 11: A CLUE — THE VACUUM ENERGY DIFFERENCE
# ============================================================
print(f"""
================================================================
PART 11: A CLUE — SELF-REFERENTIAL IDENTITY
================================================================

    There's something remarkable about phibar^2:

    phibar^2 = 2 - phi = 3 - phi^2 = {phibar**2:.10f}

    And: phi^2 = phi + 1  (the defining equation)
    So:  phibar^2 = 3 - (phi + 1) = 2 - phi

    The CORE IDENTITY of the theory is: alpha^(3/2)*mu*phi^2 = 3
    Rearranging: alpha^(3/2)*mu = 3/phi^2 = 3*(phibar/phi)^0...

    Actually: 3 = phi^2 + phibar^2 = L(2) (the second Lucas number)

    So: alpha^(3/2)*mu*phi^2 = phi^2 + phibar^2

    This means: THE TREE-LEVEL IDENTITY ALREADY CONTAINS phibar^2!

    The "3" in the core identity is NOT just triality.
    It's phi^2 + phibar^2 = the sum of BOTH vacuum contributions.

    Separating:
    alpha^(3/2)*mu*phi^2 = phi^2 + phibar^2

    Tree level (phi^2 only):
    alpha_tree^(3/2)*mu_tree*phi^2 = phi^2
    => alpha_tree^(3/2)*mu_tree = 1  (just the visible vacuum)

    Full result (both vacua):
    alpha^(3/2)*mu*phi^2 = phi^2 + phibar^2
    => alpha^(3/2)*mu = 1 + phibar^2/phi^2 = 1 + phibar^4
""")

alpha_tree_only = (1 / mu_p)**(2/3)  # from alpha^3/2 * mu = 1
alpha_full = ((1 + phibar**4) / mu_p)**(2/3)  # from alpha^3/2*mu = 1+phibar^4
alpha_identity = (3 / (mu_p * phi**2))**(2/3)

print(f"    alpha (tree, visible only):  1/{1/alpha_tree_only:.4f}")
print(f"    alpha (both vacua, full):    1/{1/alpha_full:.4f}")
print(f"    alpha (standard identity):   1/{1/alpha_identity:.4f}")
print(f"    alpha (measured):            1/137.036")
print(f"    phibar^4 contribution:       {phibar**4:.6f} = {phibar**4*100:.3f}% correction")

# This is a key insight! Let's check if the SPLIT matters for mu
print(f"""
    SEPARATING THE IDENTITY:

    Full:  alpha^(3/2) * mu * phi^2 = 3 = L(2) = phi^2 + phibar^2

    If we write mu = mu_tree * (1 + epsilon):
    alpha^(3/2) * mu_tree * (1+eps) * phi^2 = phi^2 + phibar^2

    Tree: alpha^(3/2) * mu_tree * phi^2 = phi^2
    Correction: alpha^(3/2) * mu_tree * eps * phi^2 = phibar^2
    => eps = phibar^2/phi^2 = phibar^4 = {phibar**4:.8f}

    So the "correction" to mu from including the dark vacuum is:
    delta_mu / mu = phibar^4 = {phibar**4:.6f}

    Actual residual of mu = N/phi^3 vs measured:
    (N/phi^3 - 1836.15267) / 1836.15267 = {(N/phi**3 - 1836.15267)/1836.15267:.6f}

    These have DIFFERENT SIGNS. But the MAGNITUDES:
    phibar^4 = {phibar**4:.6f}
    |residual| = {abs((N/phi**3-1836.15267)/1836.15267):.6f}

    Different by factor {phibar**4/abs((N/phi**3-1836.15267)/1836.15267):.1f}.
    Not a match. But the IDEA of separating L(2) = phi^2 + phibar^2
    is algebraically natural.
""")

# ============================================================
# PART 12: WHAT THIS MEANS FOR THE FRAMEWORK
# ============================================================
print(f"""
================================================================
PART 12: SUMMARY AND IMPLICATIONS
================================================================

    WHAT WE PROVED:
    1. The one-loop CW potential shifts the vacuum by delta ~ {delta_phi:.2e}
       This is perturbatively small and DOES NOT explain phibar corrections.

    2. The empirical phibar corrections are 100x larger than perturbative
       loop effects, suggesting a non-perturbative origin.

    3. The SELF-REFERENTIAL IDENTITY 3 = phi^2 + phibar^2 naturally
       splits into visible (phi^2) and dark (phibar^2) contributions,
       providing a STRUCTURAL reason for phibar corrections.

    4. Domain wall bound states (breathing mode at sqrt(3/2)*m_H)
       contribute at a scale similar to phibar but not exactly matching.

    OPEN QUESTIONS:
    A. Is there a non-perturbative method (resurgence, exact WKB,
       lattice) that gives phibar^n corrections directly?
    B. Does the self-referential structure V=(Phi^2-Phi-1)^2 have
       special properties under resurgent asymptotic expansion?
    C. Can the domain wall partition function be computed exactly?

    THEORETICAL STATUS:
    - The phibar corrections LOOK physically motivated
    - They are NOT derived from standard perturbation theory
    - A non-perturbative derivation would be a major advance
    - Until then, they remain an empirical pattern
""")
