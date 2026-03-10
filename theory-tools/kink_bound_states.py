"""
kink_bound_states.py — Derive generation positions from domain wall physics.

The E8 embedding proved that S3 is EXACT in the root structure.
Mass hierarchy comes entirely from the scalar field Phi(x).

The question: WHERE along the kink do the 3 generations sit?
Answer: they are BOUND STATES of the domain wall potential.

Physics:
  V(Phi) = lambda * (Phi^2 - Phi - 1)^2
  Kink: Phi(x) = (sqrt5/2) * tanh(mu*x/2) + 1/2
  where mu^2 = V''(phi) = 10*lambda

  Fluctuations around the kink satisfy a Schrodinger equation:
  -psi'' + U(x) * psi = E * psi

  where U(x) = V''(Phi_kink(x)) is a Poschl-Teller potential.

  The bound states of U(x) give the generation spectrum.

Usage:
    python theory-tools/kink_bound_states.py
"""

import numpy as np
import sys
import math

if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

phi = (1 + 5**0.5) / 2
psi_val = -1 / phi
sqrt5 = 5**0.5

print("=" * 70)
print("DOMAIN WALL BOUND STATES -> GENERATION SPECTRUM")
print("=" * 70)

# ============================================================
# PART 1: The kink and its fluctuation potential
# ============================================================
print("\n[1] The kink solution and fluctuation potential...")

print(f"""
    V(Phi) = lambda * (Phi^2 - Phi - 1)^2

    Vacua: Phi = phi = {phi:.6f} and Phi = -1/phi = {psi_val:.6f}
    Separation: sqrt(5) = {sqrt5:.6f}

    Kink: Phi_k(x) = (sqrt5/2) * tanh(mu*x/2) + 1/2
    where mu^2 = V''(phi) = 10*lambda

    At the vacua: V''(phi) = V''(-1/phi) = 10*lambda = mu^2
    At the center: V''(1/2) = 2*lambda*[6*(1/4) - 6*(1/2) - 1]
                             = 2*lambda*[3/2 - 3 - 1] = -5*lambda
""")

# V''(Phi) = 2*lambda * (6*Phi^2 - 6*Phi - 1)
# Check:
# V''(phi) = 2*lambda*(6*phi^2 - 6*phi - 1) = 2*lambda*(6*(phi+1) - 6*phi - 1)
#          = 2*lambda*(6+6-6-1-6+6) hmm let me recalculate
# phi^2 = phi + 1
# V''(phi) = 2*lambda*(6*(phi+1) - 6*phi - 1) = 2*lambda*(6*phi + 6 - 6*phi - 1) = 2*lambda*5 = 10*lambda ✓

# V''(1/2) = 2*lambda*(6/4 - 3 - 1) = 2*lambda*(3/2 - 4) = 2*lambda*(-5/2) = -5*lambda ✓

# The effective potential for fluctuations:
# U(x) = V''(Phi_k(x)) - mu^2
# This is a potential WELL centered at x=0

# Substituting the kink into V'':
# Phi_k = (sqrt5/2)*tanh(z) + 1/2 where z = mu*x/2
# Phi_k^2 = 5/4*tanh^2(z) + sqrt5/2*tanh(z) + 1/4
# 6*Phi_k^2 - 6*Phi_k - 1 = 6*(5/4*t^2 + sqrt5/2*t + 1/4) - 6*(sqrt5/2*t + 1/2) - 1
#   = 30/4*t^2 + 3*sqrt5*t + 3/2 - 3*sqrt5*t - 3 - 1
#   = (15/2)*t^2 - 5/2
#   = (15*t^2 - 5)/2
# where t = tanh(z)

# So V''(Phi_k) = 2*lambda*(15*tanh^2(z) - 5)/2 = lambda*(15*tanh^2(z) - 5)
# = lambda*(15*(1 - 1/cosh^2(z)) - 5)
# = lambda*(10 - 15/cosh^2(z))

# Therefore:
# U(x) = V''(Phi_k) - mu^2 = lambda*(10 - 15/cosh^2(z)) - 10*lambda
#       = -15*lambda / cosh^2(mu*x/2)

print("    Effective Schrodinger potential for fluctuations:")
print("    U(x) = -15*lambda / cosh^2(mu*x/2)")
print()
print("    This is the POSCHL-TELLER potential!")
print("    V_PT(u) = -n(n+1) / cosh^2(u)")
print("    with n(n+1) = 15*lambda / (mu^2/4) = 15*lambda * 4 / (10*lambda) = 6")
print("    n(n+1) = 6 -> n = 2")

# ============================================================
# PART 2: Poschl-Teller bound states
# ============================================================
print("\n\n[2] Poschl-Teller bound state spectrum...")

print(f"""
    For V(u) = -n(n+1)/cosh^2(u) with n = 2:

    The bound state energies (relative to the bulk mass mu^2):

    m_k^2 = mu^2 * [1 - ((n-k)/n)^2]   for k = 0, 1, ..., n

    k = 0: m_0^2 = mu^2 * [1 - (2/2)^2] = 0          (ZERO MODE)
    k = 1: m_1^2 = mu^2 * [1 - (1/2)^2] = 3*mu^2/4   (BREATHING MODE)
    k = 2: m_2^2 = mu^2 * [1 - 0]       = mu^2        (CONTINUUM EDGE)
""")

# Wait, let me re-derive this more carefully using the standard Poschl-Teller results.
# The modified Poschl-Teller potential in the kink context:
#
# The Schrodinger equation: -psi'' + U(x)*psi = omega^2 * psi
# with U(x) = -15*lambda/cosh^2(mu*x/2)
#
# Change variables: u = mu*x/2, then:
# -(mu/2)^2 * d^2psi/du^2 - 15*lambda/cosh^2(u) * psi = omega^2 * psi
# d^2psi/du^2 + [15*lambda*4/mu^2 / cosh^2(u)] * psi = -4*omega^2/mu^2 * psi
# d^2psi/du^2 + 6/cosh^2(u) * psi = -4*omega^2/mu^2 * psi
#
# Standard PT: d^2psi/du^2 + s(s+1)/cosh^2(u) * psi = E * psi
# with s(s+1) = 6, so s = 2
# Bound states: E_j = -(s-j)^2 for j = 0, 1, ..., floor(s)
# E_0 = -4, E_1 = -1, E_2 = 0
#
# So: -4*omega^2_j/mu^2 = -(s-j)^2
# omega^2_j = (s-j)^2 * mu^2 / 4
#
# j=0: omega_0^2 = 4*mu^2/4 = mu^2    (this is NOT a bound state — it's the bulk mass)
# Wait, omega^2 here is measured from the BOTTOM of the well.
#
# Actually, let me reconsider. The physical mass of the bound state fluctuation is:
# m^2 = mu^2 - |E_j| * mu^2/4
# where E_j is the binding energy
#
# For j=0 (deepest bound): m_0^2 = mu^2 - 4*mu^2/4 = 0 → ZERO MODE ✓
# For j=1: m_1^2 = mu^2 - 1*mu^2/4 = 3*mu^2/4 → BREATHING MODE ✓
# For j=2: m_2^2 = mu^2 - 0 = mu^2 → CONTINUUM THRESHOLD ✓

# So we get EXACTLY 2 bound states (j=0 and j=1).
# j=0 is the zero mode (massless, Goldstone of translations)
# j=1 is the breathing mode with m^2 = 3*mu^2/4

print("    RESULT: The n=2 Poschl-Teller has exactly 2 bound states:")
print("    j=0: m^2 = 0         (zero mode, translation)")
print("    j=1: m^2 = 3*mu^2/4  (breathing mode)")
print()
print("    This gives only 2 states, not 3.")
print("    WE NEED 3 GENERATIONS!")
print()

# ============================================================
# PART 3: The missing dimension — TRANSVERSE modes
# ============================================================
print("=" * 70)
print("[3] Transverse modes in 8D root space")
print("=" * 70)

print(f"""
    The 1D kink has 2 bound states. But we need 3 generations.
    The resolution: we're in 8D, not 1D.

    The scalar field Phi lives in the 8-dimensional E8 root space.
    The kink interpolates in ONE direction (call it x_8).
    The other 7 directions are TRANSVERSE.

    Under the 4A2 decomposition, the 8 dimensions split as:
    - 2D for each of 4 A2 copies = 8D total
    - Kink direction is WITHIN the dark A2 subspace (copy 3)
    - The 6 visible dimensions (copies 0,1,2) are transverse

    For each generation (A2 copy), the transverse fluctuations
    couple to the kink potential. But there's a TWIST:

    The off-diagonal roots (216 of them) connect 3 copies simultaneously.
    Each off-diagonal root is a (3,3,3) representation — it spans
    3 of the 4 A2 subspaces.

    For the 54 roots connecting copies (0,1,2) — the visible sector:
    These are PURELY transverse to the kink direction.
    They see NO kink potential at all!
    Their fluctuations are just free massive modes at m = mu.

    For the 3x54 = 162 roots connecting one visible + two others
    (including dark): these DO couple to the kink.
    Each visible copy has 54 such roots involving the dark copy.
""")

# The 4 groups of off-diagonal roots:
# (0,1,2): 54 roots — purely visible, no dark
# (0,1,3): 54 roots — copies 0,1 visible + dark
# (0,2,3): 54 roots — copies 0,2 visible + dark
# (1,2,3): 54 roots — copies 1,2 visible + dark

# Each visible copy participates in:
# (0,1,2): 54 roots — no dark connection
# (0,1,3): 54 roots — dark connection, with gen 0 and 1
# (0,2,3): 54 roots — dark connection, with gen 0 and 2
# (1,2,3): 54 roots — dark connection, with gen 1 and 2

# For generation 0:
# No dark: 54 (purely transverse, m = mu)
# With dark: 54 (from 013) + 54 (from 023) = 108 total
# Same for all generations (S3 symmetry verified)

print("    Each generation couples to the kink via 108 dark-connected roots.")
print("    Plus 54 purely-visible roots that don't couple to the kink.")
print()

# ============================================================
# PART 4: The coupled kink-transverse system
# ============================================================
print("=" * 70)
print("[4] The coupled system: kink + transverse A2")
print("=" * 70)

print(f"""
    The key insight: the generation mass isn't from 1D bound states.
    It's from how the TRANSVERSE A2 fluctuations couple to the kink.

    For a fermion in generation i (living in A2 copy i):
    - Its "bulk mass" comes from the A2 root length: m_bulk = mu
    - Its coupling to the kink comes from the dark-connected roots
    - The effective 4D Yukawa is determined by the OVERLAP INTEGRAL:

        y_i = integral[ f_L(x) * Phi_kink(x) * f_R(x) ] dx

    where f_L, f_R are the left/right chiral fermion profiles on the wall.
""")

# In the domain wall fermion mechanism:
# - A bulk fermion with mass M has chiral zero modes localized on the wall
# - The localization profile is: f(x) ~ exp(-M * |x|)
# - Left-handed: localized on one side, Right-handed: on the other

# The key: the BULK MASS M determines which side the fermion localizes on.
# If M > 0: left-handed on phi-vacuum side
# If M < 0: left-handed on -1/phi-vacuum side

# The effective 4D Yukawa coupling:
# y_4D = y_5D * integral[ f_L(x) * H(x) * f_R(x) ] dx
# where H(x) is the Higgs profile (related to the kink derivative)

# H(x) = d(Phi_kink)/dx = (sqrt5/2) * (mu/2) / cosh^2(mu*x/2)
# = sqrt5*mu/4 / cosh^2(mu*x/2)

# This is localized at x=0 (the wall center).

# The overlap integral depends on M_L and M_R (bulk masses of L and R fermions).
# For symmetric localization (M_L = M_R = M):
# y_4D ~ integral exp(-2M|x|) / cosh^2(mu*x/2) dx

# For M*w >> 1 (w = 2/mu = wall width):
# y_4D ~ exp(-2M*0) * (something) = O(1)  (if fermion localized at wall)

# For M*w << 1 (delocalized fermion):
# y_4D ~ mu / M  (suppressed)

print("    DOMAIN WALL FERMION MECHANISM:")
print()
print("    Bulk fermion mass M determines localization profile:")
print("    f(x) ~ exp(-M * |x|) for large |x|")
print()
print("    The Higgs/kink profile:")
print("    H(x) = dPhi/dx = (sqrt5*mu/4) / cosh^2(mu*x/2)")
print("    Localized at x=0 with width w = 2/mu")
print()
print("    Effective 4D Yukawa:")
print("    y_4D ~ integral f_L(x) * H(x) * f_R(x) dx")
print()

# ============================================================
# PART 5: Computing the overlap integrals
# ============================================================
print("=" * 70)
print("[5] Overlap integrals for each generation")
print("=" * 70)

# The overlap integral for a fermion with bulk mass M:
# I(M) = integral_{-inf}^{inf} exp(-2*M*|x|) / cosh^2(mu*x/2) dx
#
# Let u = mu*x/2, du = mu*dx/2:
# I(M) = (2/mu) * integral exp(-4*M*u/mu) / cosh^2(u) du  (for u > 0, doubled)
# = (4/mu) * integral_0^inf exp(-4*M*u/mu) / cosh^2(u) du
#
# Let alpha = 4*M/mu = 2*M*w
# I = (4/mu) * integral_0^inf exp(-alpha*u) / cosh^2(u) du
#
# This integral has a known solution:
# integral_0^inf exp(-alpha*u) / cosh^2(u) du = 2*alpha / (alpha^2 - 1)  for alpha > 1
# Wait, that's not right. Let me compute it properly.
#
# integral_0^inf exp(-a*u) * sech^2(u) du
# sech^2(u) = 4*exp(-2u) / (1 + exp(-2u))^2
# = 4 * sum_{n=1}^inf (-1)^{n+1} * n * exp(-2nu)
# integral = 4 * sum (-1)^{n+1} * n / (a + 2n)
#
# For a = 0: integral = 4 * sum (-1)^{n+1} * n / (2n) = 2 * sum (-1)^{n+1} = 1 (via Abel)
# Actually for a=0: integral sech^2(u) du from 0 to inf = tanh(inf) - tanh(0) = 1 ✓
#
# For general a > 0, the integral can be written in terms of digamma functions:
# I(a) = a * [psi((a+2)/4) - psi(a/4)] / 2
# where psi is the digamma function.
#
# But more practically, we can just compute it numerically.

from scipy import integrate

mu_val = 1.0  # Set mu = 1 (we work in units of mu)

def higgs_profile(x):
    """The kink derivative: H(x) = dPhi/dx"""
    return sqrt5 / 4 / np.cosh(x / 2)**2

def fermion_profile(x, M):
    """Bulk fermion localization profile"""
    return np.exp(-abs(M) * abs(x))

def overlap_integral(M):
    """Compute the 4D Yukawa as overlap integral"""
    def integrand(x):
        return fermion_profile(x, M) * higgs_profile(x) * fermion_profile(x, M)
    result, _ = integrate.quad(integrand, -20, 20)
    return result

# Compute overlap for a range of bulk masses
print("    Overlap integral I(M) = integral f(x)^2 * H(x) dx")
print("    (in units where mu = 1, wall width w = 2)")
print()
print(f"    {'M (bulk mass)':>14} {'I(M)':>12} {'I(M)/I(0)':>12} {'log ratio':>12}")
print(f"    {'-'*14} {'-'*12} {'-'*12} {'-'*12}")

I0 = overlap_integral(0)
M_values = np.arange(0, 3.5, 0.25)
for M in M_values:
    I_M = overlap_integral(M)
    ratio = I_M / I0
    log_ratio = np.log(ratio) if ratio > 0 else float('-inf')
    print(f"    {M:>14.2f} {I_M:>12.6f} {ratio:>12.6f} {log_ratio:>12.4f}")

print()

# ============================================================
# PART 6: What bulk masses give the observed hierarchy?
# ============================================================
print("=" * 70)
print("[6] Reverse-engineering bulk masses from observed masses")
print("=" * 70)

# Lepton masses: m_e = 0.511 MeV, m_mu = 105.658 MeV, m_tau = 1776.86 MeV
# Mass ratios: m_tau/m_mu = 16.82, m_mu/m_e = 206.77, m_tau/m_e = 3477.3

# In the domain wall fermion mechanism:
# m_4D ~ v * y_4D ~ v * I(M)
# where v is the Higgs VEV

# So: m_tau/m_mu = I(M_tau) / I(M_mu)
#     m_mu/m_e = I(M_mu) / I(M_e)

# We need to find M_tau, M_mu, M_e such that the ratios work out.

# Strategy: fix M_tau (heaviest, most localized) and scan for M_mu, M_e

print("    Target ratios:")
print(f"    m_tau/m_mu = 16.82")
print(f"    m_mu/m_e  = 206.77")
print(f"    m_tau/m_e  = 3477.3")
print()

# The tau is the heaviest -> smallest bulk mass (most localized at wall)
# The electron is lightest -> largest bulk mass (least overlap with wall)

# Scan: find M_mu and M_e for each M_tau
print("    Scanning bulk masses...")
print()

best_match = None
best_error = float('inf')

# M_tau should be small (well-localized)
for M_tau_10 in range(0, 20):  # M_tau from 0 to 2
    M_tau = M_tau_10 / 10.0
    I_tau = overlap_integral(M_tau)

    # Find M_mu: I_tau / I_mu = 16.82
    target_I_mu = I_tau / 16.82

    # Binary search for M_mu
    M_lo, M_hi = M_tau, 5.0
    for _ in range(50):
        M_mid = (M_lo + M_hi) / 2
        if overlap_integral(M_mid) > target_I_mu:
            M_lo = M_mid
        else:
            M_hi = M_mid
    M_mu = (M_lo + M_hi) / 2
    I_mu = overlap_integral(M_mu)

    # Find M_e: I_mu / I_e = 206.77
    target_I_e = I_mu / 206.77

    M_lo_e, M_hi_e = M_mu, 10.0
    for _ in range(50):
        M_mid = (M_lo_e + M_hi_e) / 2
        if overlap_integral(M_mid) > target_I_e:
            M_lo_e = M_mid
        else:
            M_hi_e = M_mid
    M_e = (M_lo_e + M_hi_e) / 2
    I_e = overlap_integral(M_e)

    # Check ratios
    ratio_tau_mu = I_tau / I_mu if I_mu > 0 else float('inf')
    ratio_mu_e = I_mu / I_e if I_e > 0 else float('inf')
    error = abs(ratio_tau_mu - 16.82) / 16.82 + abs(ratio_mu_e - 206.77) / 206.77

    if error < best_error:
        best_error = error
        best_match = (M_tau, M_mu, M_e, I_tau, I_mu, I_e)

if best_match:
    M_tau, M_mu, M_e, I_tau, I_mu, I_e = best_match
    print(f"    Best fit bulk masses (in units of mu):")
    print(f"    M_tau = {M_tau:.3f}")
    print(f"    M_mu  = {M_mu:.3f}")
    print(f"    M_e   = {M_e:.3f}")
    print()
    print(f"    Overlap integrals:")
    print(f"    I(M_tau) = {I_tau:.6f}")
    print(f"    I(M_mu)  = {I_mu:.6f}")
    print(f"    I(M_e)   = {I_e:.6f}")
    print()
    print(f"    Mass ratios:")
    print(f"    m_tau/m_mu = I_tau/I_mu = {I_tau/I_mu:.2f}  (target: 16.82)")
    print(f"    m_mu/m_e   = I_mu/I_e   = {I_mu/I_e:.2f}  (target: 206.77)")
    print()

    # Check if bulk mass differences are related to framework elements
    print(f"    Bulk mass differences:")
    dM_12 = M_mu - M_tau
    dM_23 = M_e - M_mu
    dM_13 = M_e - M_tau
    print(f"    M_mu - M_tau  = {dM_12:.4f}")
    print(f"    M_e - M_mu   = {dM_23:.4f}")
    print(f"    M_e - M_tau  = {dM_13:.4f}")
    print(f"    Ratio (M_e-M_mu)/(M_mu-M_tau) = {dM_23/dM_12:.4f}")
    print()

    # Check against framework numbers
    print(f"    Framework number checks:")
    ratio_spacing = dM_23 / dM_12
    for name, val in [("phi", phi), ("3/2", 1.5), ("phi^2", phi**2),
                       ("2", 2.0), ("phi+1", phi+1), ("3", 3.0),
                       ("sqrt5", sqrt5), ("2*phi", 2*phi),
                       ("phi^3/2", phi**3/2), ("5/3", 5/3),
                       ("7/4", 7/4), ("L(5)/L(4)", 11/7)]:
        match = min(ratio_spacing, val) / max(ratio_spacing, val) * 100
        if match > 90:
            print(f"    Spacing ratio {ratio_spacing:.4f} ~ {name} = {val:.4f} ({match:.1f}%)")

    # Check if bulk masses themselves match framework
    print()
    print(f"    Bulk mass structure:")
    for name, M, gen in [("tau", M_tau, 3), ("mu", M_mu, 2), ("e", M_e, 1)]:
        # Check against simple framework numbers
        for label, val in [("1/phi", 1/phi), ("1/phi^2", 1/phi**2),
                           ("1/3", 1/3), ("2/3", 2/3), ("1/7", 1/7),
                           ("phi/3", phi/3), ("1/sqrt5", 1/sqrt5),
                           ("3/phi^3", 3/phi**3), ("2/phi", 2/phi),
                           ("alpha^(1/2)", 0.0854), ("1/11", 1/11),
                           ("phi/7", phi/7), ("3/7", 3/7),
                           ("2/7", 2/7), ("1/phi^3", 1/phi**3)]:
            match_pct = min(M, val) / max(M, val) * 100 if M > 0 and val > 0 else 0
            if match_pct > 95:
                print(f"      M_{name} = {M:.4f} ~ {label} = {val:.4f} ({match_pct:.1f}%)")


# ============================================================
# PART 7: Check for QUARK sector too
# ============================================================
print("\n\n" + "=" * 70)
print("[7] Quark sector bulk masses")
print("=" * 70)

# Up-type quarks: m_t = 172.5 GeV, m_c = 1.27 GeV, m_u = 2.16 MeV
# Mass ratios: m_t/m_c = 135.8, m_c/m_u = 588
# Down-type quarks: m_b = 4.18 GeV, m_s = 93.4 MeV, m_d = 4.67 MeV
# Mass ratios: m_b/m_s = 44.8, m_s/m_d = 20.0

sectors = [
    ("Leptons", 16.82, 206.77),
    ("Up quarks", 135.8, 588.0),
    ("Down quarks", 44.8, 20.0),
]

results = {}

for sector_name, r32, r21 in sectors:
    print(f"\n    --- {sector_name}: m3/m2 = {r32:.1f}, m2/m1 = {r21:.1f} ---")

    best = None
    best_err = float('inf')

    for M3_10 in range(0, 30):
        M3 = M3_10 / 10.0
        I3 = overlap_integral(M3)

        target_I2 = I3 / r32
        M_lo, M_hi = M3, 10.0
        for _ in range(50):
            M_mid = (M_lo + M_hi) / 2
            if overlap_integral(M_mid) > target_I2:
                M_lo = M_mid
            else:
                M_hi = M_mid
        M2 = (M_lo + M_hi) / 2
        I2 = overlap_integral(M2)

        target_I1 = I2 / r21
        if target_I1 < 1e-15:
            continue
        M_lo_1, M_hi_1 = M2, 15.0
        for _ in range(50):
            M_mid = (M_lo_1 + M_hi_1) / 2
            if overlap_integral(M_mid) > target_I1:
                M_lo_1 = M_mid
            else:
                M_hi_1 = M_mid
        M1 = (M_lo_1 + M_hi_1) / 2
        I1 = overlap_integral(M1)

        err = abs(I3/I2 - r32)/r32 + abs(I2/I1 - r21)/r21
        if err < best_err:
            best_err = err
            best = (M3, M2, M1, I3, I2, I1)

    if best:
        M3, M2, M1, I3, I2, I1 = best
        print(f"    M_3 = {M3:.3f}, M_2 = {M2:.3f}, M_1 = {M1:.3f}")
        print(f"    I_3/I_2 = {I3/I2:.1f} (target {r32:.1f})")
        print(f"    I_2/I_1 = {I2/I1:.1f} (target {r21:.1f})")

        dM12 = M2 - M3
        dM23 = M1 - M2
        ratio = dM23 / dM12 if dM12 > 0 else float('inf')
        print(f"    Spacing: dM_12 = {dM12:.4f}, dM_23 = {dM23:.4f}, ratio = {ratio:.4f}")

        results[sector_name] = (M3, M2, M1, dM12, dM23, ratio)


# ============================================================
# PART 8: Universal pattern?
# ============================================================
print("\n\n" + "=" * 70)
print("[8] Universal pattern across sectors")
print("=" * 70)

if results:
    print(f"\n    {'Sector':>14} {'M_3':>8} {'M_2':>8} {'M_1':>8} {'dM_12':>8} {'dM_23':>8} {'ratio':>8}")
    print(f"    {'-'*14} {'-'*8} {'-'*8} {'-'*8} {'-'*8} {'-'*8} {'-'*8}")
    for name, (M3, M2, M1, dM12, dM23, ratio) in results.items():
        print(f"    {name:>14} {M3:>8.3f} {M2:>8.3f} {M1:>8.3f} {dM12:>8.4f} {dM23:>8.4f} {ratio:>8.3f}")

    # Check if spacing ratios match across sectors
    ratios = [r[-1] for r in results.values()]
    if len(ratios) > 1:
        print(f"\n    Spacing ratios: {[f'{r:.3f}' for r in ratios]}")
        avg_ratio = sum(ratios) / len(ratios)
        print(f"    Average: {avg_ratio:.4f}")

        for name, val in [("phi", phi), ("3/2", 1.5), ("2", 2.0),
                           ("phi^2", phi**2), ("3", 3.0), ("sqrt5", sqrt5),
                           ("5/3", 5/3), ("7/4", 7/4), ("11/7", 11/7)]:
            match = min(avg_ratio, val) / max(avg_ratio, val) * 100
            if match > 85:
                print(f"    Average ratio {avg_ratio:.4f} ~ {name} = {val:.4f} ({match:.1f}%)")

print("\n" + "=" * 70)
print("END OF DOMAIN WALL BOUND STATE ANALYSIS")
print("=" * 70)
