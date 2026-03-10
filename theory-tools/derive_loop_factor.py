#!/usr/bin/env python3
"""
derive_loop_factor.py -- Can C = eta*theta_4/2 be DERIVED from first principles?
=================================================================================

The framework uses a universal loop correction factor:
    C = eta(1/phi) * theta_4(1/phi) / 2

It appears in:
    alpha = [t4/(t3*phi)] * (1 - C*phi^2)           -> 99.9996%
    v = [M_Pl*phibar^80/(1-phi*t4)] * (1 + C*7/3)   -> 99.9992%

This script investigates whether C can be derived, or is empirically fitted.

APPROACH:
    (a) One-loop determinant around the kink
    (b) Vacuum polarization in QED
    (c) Modular form identities for eta*theta_4
    (d) Kink zero-mode contribution
    (e) Theta function product identities
    (f) Physical interpretation of C ~ 0.0018
"""

import math
import sys

if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PHI = (1 + math.sqrt(5)) / 2
PHIBAR = 1 / PHI
SQRT5 = math.sqrt(5)
MU = 1836.15267343
ALPHA_MEAS = 1/137.035999084
M_Pl = 1.22089e19  # GeV
v_meas = 246.22     # GeV
m_e_MeV = 0.511
m_p_MeV = 938.272

# =====================================================
# Compute modular forms at q = 1/phi (high precision)
# =====================================================
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

# Dedekind eta: product form directly
eta24 = eta**24

# Also compute eta at q^2 (needed for identities below)
eta_q2 = q**(1/12)
for n in range(1, N_terms):
    eta_q2 *= (1 - q**(2*n))

alpha_mod = t4 / (t3 * PHI)

C = eta * t4 / 2

print("=" * 80)
print("  CAN C = eta*theta_4/2 BE DERIVED FROM FIRST PRINCIPLES?")
print("=" * 80)
print()
print(f"  Modular form values at q = 1/phi:")
print(f"    eta    = {eta:.15f}")
print(f"    t2     = {t2:.15f}")
print(f"    t3     = {t3:.15f}")
print(f"    t4     = {t4:.15f}")
print(f"    eta*t4 = {eta*t4:.15f}")
print(f"    C = eta*t4/2 = {C:.15f}")
print()
print(f"  For reference:")
print(f"    alpha_s (measured) = 0.1179 +/- 0.0009")
print(f"    eta = alpha_s in framework = {eta:.4f}")

# =====================================================
# PART 1: What IS C numerically?
# =====================================================
print()
print("=" * 80)
print("  PART 1: WHAT IS C? NUMERICAL DECOMPOSITION")
print("=" * 80)
print()

# C = eta * t4 / 2
# Since eta = alpha_s, this is alpha_s * theta_4 / 2
# In QFT language: strong_coupling * dark_VP_parameter / symmetry_factor

print(f"  C = eta * t4 / 2 = {C:.10f}")
print(f"  = alpha_s * theta_4 / 2")
print(f"  ~ 0.1184 * 0.0303 / 2 = {0.1184*0.0303/2:.6f}")
print()

# Compare to known QFT loop factors
loop_16pi2 = 1 / (16 * math.pi**2)   # standard 1-loop
loop_4pi = 1 / (4 * math.pi)
loop_3pi = 1 / (3 * math.pi)
alpha_3pi = ALPHA_MEAS / (3 * math.pi)

print(f"  Standard loop factors:")
print(f"    1/(16*pi^2)          = {loop_16pi2:.6f}  (perturbative 1-loop)")
print(f"    alpha/(3*pi)         = {alpha_3pi:.6f}  (EM VP correction)")
print(f"    alpha_s/(16*pi^2)    = {eta/(16*math.pi**2):.6f}  (QCD 1-loop)")
print(f"    C                    = {C:.6f}")
print()

# Is C close to any of these?
print(f"  Ratios:")
print(f"    C / [1/(16*pi^2)]    = {C/loop_16pi2:.4f}")
print(f"    C / [alpha/(3*pi)]   = {C/alpha_3pi:.4f}")
print(f"    C / [alpha_s/(16pi^2)] = {C/(eta/(16*math.pi**2)):.4f}")
print()
print(f"  C is about {C/alpha_3pi:.0f}x the EM VP correction")
print(f"  C is about {C/loop_16pi2:.1f}x the standard 1-loop factor")
qcd_loop = eta / (16 * math.pi**2)
print(f"  C is about {C/qcd_loop:.1f}x the QCD 1-loop factor")

# =====================================================
# PART 2: Modular form identities for eta*theta_4
# =====================================================
print()
print("=" * 80)
print("  PART 2: MODULAR FORM IDENTITIES FOR eta*theta_4")
print("=" * 80)
print()

# KEY IDENTITY (Jacobi):
# 2*eta(tau)^3 = theta_2(0|tau) * theta_3(0|tau) * theta_4(0|tau)
# where the theta functions use the convention q = e^{2*pi*i*tau}
# and theta_2 = 2*q^{1/4}*prod(1-q^{2n})(1+q^{2n})^2 etc.
#
# First verify what we have numerically:

jacobi_rhs = t2 * t3 * t4
jacobi_lhs = 2 * eta**3
print(f"  JACOBI IDENTITY: 2*eta^3 = theta_2 * theta_3 * theta_4")
print(f"    LHS: 2*eta^3 = {jacobi_lhs:.15f}")
print(f"    RHS: t2*t3*t4 = {jacobi_rhs:.15f}")
print(f"    Ratio RHS/LHS = {jacobi_rhs/jacobi_lhs:.6f}")
print()

# The ratio is not 1. Let's check what the actual product identity gives.
# With standard conventions where q = e^{2*pi*i*tau}:
# The product eta^24 = q * prod(1-q^n)^24 is the discriminant.
# Let's verify the product decomposition differently.
# We know theta_4 = eta^2/eta(q^2) holds (verified to 10^-14).
# So eta*t4 = eta * eta^2/eta(q^2) = eta^3/eta(q^2)

print(f"  VERIFIED IDENTITY: theta_4(q) = eta(q)^2 / eta(q^2)")
print(f"  Therefore: eta * theta_4 = eta^3 / eta(q^2)")
print(f"  And: C = eta*theta_4/2 = eta^3 / (2*eta(q^2))")
print()

# From this identity:
# C = eta^3 / (2*eta(q^2))
C_from_eta3 = eta**3 / (2 * eta_q2)
print(f"  C = eta^3 / (2*eta(q^2))")
print(f"    C (direct) = {C:.15f}")
print(f"    C (identity) = {C_from_eta3:.15f}")
print(f"    Agreement: {abs(C - C_from_eta3)/C * 100:.2e}% error (exact)")
print()

# The approximate form when t2 ~ t3:
print(f"  At q = 1/phi, theta_2 ~ theta_3 (nodal degeneration), so:")
print(f"    C ~ eta^3 / theta_3^2  (using Jacobi identity heuristically)")
C_approx = eta**3 / t3**2
print(f"    eta^3 / theta_3^2 = {C_approx:.15f}")
print(f"    Actual C = {C:.15f}")
print(f"    Ratio: {C/C_approx:.6f}")
print(f"    (The ratio t2*t3/(2*eta(q^2)) = {t2*t3/(2*eta_q2):.6f} explains the difference)")
print()

# Another identity: theta_4(q) = product_{n=1}^inf (1-q^n)^2 * (1+q^n)^{-2} ... no
# Actually theta_4(q) can be written as:
# theta_4(q) = prod_{n=1}^inf (1-q^(2n)) (1-q^(2n-1))^2
# eta(q) = q^{1/24} prod_{n=1}^inf (1-q^n)
# So eta(q) * theta_4(q) involves products of (1-q^n) factors

# eta(q^2) was already computed above

# theta_4 = prod (1-q^(2n)) * (1-q^(2n-1))^2
# = [prod(1-q^(2n))] * [prod(1-q^(2n-1))]^2
#
# eta(q) = q^(1/24) * prod(1-q^n) = q^(1/24) * prod(1-q^(2n)) * prod(1-q^(2n-1))
# So: prod(1-q^(2n-1)) = eta(q) / (q^(1/24) * prod(1-q^(2n)))
#                       = eta(q) / (q^(1/24) * eta(q^2)/q^(1/12))
#                       = eta(q) * q^(1/12) / (q^(1/24) * eta(q^2))
#                       = eta(q) * q^(1/24) / eta(q^2)

# theta_4 = prod(1-q^(2n)) * [eta(q)*q^(1/24)/eta(q^2)]^2
# = [eta(q^2)/q^(1/12)] * [eta(q)*q^(1/24)/eta(q^2)]^2
# = [eta(q^2)/q^(1/12)] * eta(q)^2 * q^(1/12) / eta(q^2)^2
# = eta(q)^2 / eta(q^2)

# THEREFORE: theta_4(q) = eta(q)^2 / eta(q^2)  ... let's verify!
t4_from_eta = eta**2 / eta_q2
print(f"  KEY IDENTITY TEST: theta_4(q) = eta(q)^2 / eta(q^2)")
print(f"    theta_4 (direct)  = {t4:.15f}")
print(f"    eta^2/eta(q^2)    = {t4_from_eta:.15f}")
print(f"    Match: {abs(t4 - t4_from_eta)/t4 * 100:.2e}% error")
print()

# If true: eta*t4 = eta * eta^2/eta(q^2) = eta^3/eta(q^2)
# And C = eta*t4/2 = eta^3 / (2*eta(q^2))
C_from_eta_ratio = eta**3 / (2 * eta_q2)
print(f"  CONSEQUENCE: C = eta(q)^3 / (2 * eta(q^2))")
print(f"    Direct:     {C:.15f}")
print(f"    From ratio: {C_from_eta_ratio:.15f}")
print(f"    Match: {abs(C - C_from_eta_ratio)/C * 100:.2e}% error")
print()

# This is a CLEAN identity! C = eta^3/(2*eta(q^2))
# But wait - we need to verify t4 = eta^2/eta(q^2)
# Actually this is a KNOWN identity. Let me verify more carefully.
# The classical identity is:
# theta_4(q) = eta(q/2)^2 / eta(q)  (different convention!)
# Or in the "nome" convention: theta_4(tau) = eta(tau)^5 / (eta(tau/2)^2 * eta(2*tau)^2)
# The exact relation depends on conventions. Let me just verify numerically.

if abs(t4 - t4_from_eta)/t4 < 0.01:
    t4_identity_holds = True
    print(f"  ** theta_4 = eta^2/eta(q^2) HOLDS at q=1/phi (error: {abs(t4-t4_from_eta)/t4:.2e}) **")
else:
    t4_identity_holds = False
    print(f"  ** theta_4 = eta^2/eta(q^2) does NOT hold (ratio = {t4_from_eta/t4:.6f}) **")

print()
print(f"  PROVEN IDENTITY:")
print(f"    theta_4(q) = eta(q)^2 / eta(q^2)")
print(f"    => eta(q) * theta_4(q) = eta(q)^3 / eta(q^2)")
print(f"    => C = eta*theta_4/2 = eta(q)^3 / (2*eta(q^2))")
print()
print(f"    This identity follows from the product representations:")
print(f"    eta(q) = q^(1/24) * prod(1-q^n)")
print(f"    theta_4(q) = prod(1-q^(2n)) * (1-q^(2n-1))^2")
print(f"    and the factorization prod(1-q^n) = prod(1-q^(2n)) * prod(1-q^(2n-1))")
print(f"    which gives theta_4 = [prod(1-q^n)]^2 / [prod(1-q^(2n))]")
print(f"                        = [eta/q^(1/24)]^2 / [eta(q^2)/q^(1/12)]")
print(f"                        = eta^2 / eta(q^2)")
print(f"    This is a THEOREM, not an approximation.")

# =====================================================
# PART 3: Physical interpretation via the Jacobi identity
# =====================================================
print()
print("=" * 80)
print("  PART 3: PHYSICAL INTERPRETATION VIA JACOBI IDENTITY")
print("=" * 80)
print()

print(f"  C = eta^3 / (2 * eta(q^2))")
print()
print(f"  In the framework's physical language:")
print(f"    eta(q) = alpha_s (strong coupling / wall arithmetic coupling)")
print(f"    eta(q^2) = eta at the SQUARED nome (double-frequency modes)")
print()
print(f"  C = alpha_s^3 / (2 * eta(q^2))")
print(f"    = (strong coupling)^3 / (2 * double-frequency partition function)")
print()
print(f"  Numerically:")
print(f"    alpha_s^3 = {eta**3:.8f}")
print(f"    2*eta(q^2) = {2*eta_q2:.8f}")
print(f"    Ratio     = {eta**3/(2*eta_q2):.8f}")
print(f"    C actual  = {C:.8f}")
print(f"    (Agreement: exact to machine precision)")
print()
print(f"  Alternatively: C = alpha_s * theta_4 / 2")
print(f"    = alpha_s * (dark vacuum partition function) / 2")
print(f"    Each factor has a clear physical meaning.")

# =====================================================
# PART 4: One-loop kink determinant analysis
# =====================================================
print()
print("=" * 80)
print("  PART 4: ONE-LOOP KINK DETERMINANT ANALYSIS")
print("=" * 80)
print()

# The kink in phi^4 theory has a well-known one-loop correction:
# det(-d^2 + V''(Phi_kink)) / det(-d^2 + m^2)
# For the n=2 Poschl-Teller potential, this is exactly computable.
#
# The bound state contributions:
# - Zero mode (k=0): contributes m_kink * sqrt(m/(2*pi)) to the prefactor
# - Breathing mode (k=1): contributes 1/sqrt(omega_1) where omega_1^2 = 3*alpha^2
# - Continuum: phase shift integral
#
# For our potential V = lambda*(Phi^2-Phi-1)^2:
# After shifting Psi = Phi - 1/2:
# V = lambda*(Psi^2 - 5/4)^2
# v_field = sqrt(5)/2
# m^2 = V''(vacuum) = 8*lambda*5/4 = 10*lambda
# m = sqrt(10*lambda)
# Kink width: delta = 1/(sqrt(2*lambda)*v_field) = 1/(sqrt(2*lambda)*sqrt(5)/2)
#                   = 2/(sqrt(10*lambda)) = 2/m

# Standard phi^4 one-loop correction around the kink:
# S_1loop = -(1/2) * ln[ det(-d^2+V''(kink)) / det(-d^2+m^2) ]
# For n=2 PT, the ratio of determinants is known exactly (DHN 1975):
# ln(det_kink/det_vac) = - sum_{bound} ln(omega_k) + integral of phase shift
# Bound states: omega_0 = 0 (handled by collective coordinate), omega_1 = sqrt(3)*alpha
# where alpha = m*sqrt(2)/2 for our potential

lam = 1/(3*PHI**2)  # framework quartic
m_scalar = math.sqrt(10*lam)  # scalar mass in natural units
v_field = SQRT5/2

print(f"  Framework potential: V = lambda*(Psi^2 - 5/4)^2")
print(f"    lambda = 1/(3*phi^2) = {lam:.6f}")
print(f"    v_field = sqrt(5)/2 = {v_field:.6f}")
print(f"    m_scalar = sqrt(10*lambda) = {m_scalar:.6f}")
print()

# Kink mass (energy):
# E_kink = integral dx (1/2)(dPhi/dx)^2 + V(Phi)
# For standard phi^4: E_kink = (2*sqrt(2)/3) * m^3/lambda
# In our case: m = sqrt(10*lam), so E_kink = (2*sqrt(2)/3) * (10*lam)^(3/2)/lam

# Actually for V = lam*(Psi^2-v^2)^2, the kink solution is:
# Psi(x) = v*tanh(sqrt(2*lam)*v*x)
# E_kink = 4*sqrt(2)/3 * lam^(1/2) * v^3 = 4*sqrt(2)/3 * sqrt(lam) * (5/4)^(3/2)
E_kink = (4*math.sqrt(2)/3) * math.sqrt(lam) * v_field**3
print(f"  Kink energy: E_kink = 4*sqrt(2)/3 * sqrt(lam) * v^3 = {E_kink:.6f}")
print()

# One-loop correction from DHN (Dashen-Hasslacher-Neveu 1974):
# For V = lam*(Psi^2-v^2)^2 with n=2 PT:
# E_1loop = -m/(2*pi) * [3*ln(3/4) - 1 + ln(4)]
# = -m/(2*pi) * [3*ln(3) - 3*ln(4) - 1 + ln(4)]
# Actually the exact DHN result for the kink mass at one loop:
# M_kink = M_kink^(0) * [1 - 3/(pi*m*L) + ...]
# where L is the length of the system
#
# The ONE-LOOP SHIFT of the VEV is:
# delta_v / v = -lam/(16*pi^2) * [sum over species]
# This was computed in one_loop_potential.py: ~10^-4 (too small for phibar corrections)

# The key question: does the one-loop kink determinant NATURALLY produce
# something proportional to eta*t4?

# In 2D, the functional determinant for the kink in a periodic box
# of circumference L is related to the ELLIPTIC ZETA FUNCTION.
# Specifically, for a PT potential with period 2K (elliptic integral):
# det = product over lattice momenta of eigenvalues
# This naturally produces theta functions!

print(f"  THE KEY CONNECTION: kink in periodic box -> theta functions")
print(f"  ----------------------------------------------------------")
print()
print(f"  In a periodic box of size L, the kink eigenvalues become:")
print(f"    omega_n = sqrt(k_n^2 + V''(Phi_kink(x)))")
print(f"  where k_n = 2*pi*n/L.")
print()
print(f"  The functional determinant:")
print(f"    ln det = sum_n ln(omega_n)")
print(f"  For the PT potential, this sum can be expressed in terms of")
print(f"  ELLIPTIC FUNCTIONS with nome q related to the kink width.")
print()
print(f"  If the nome q = exp(-pi*K'/K) where K, K' are related to")
print(f"  the kink's periodicity in complex x, then:")
print(f"    The determinant ratio involves products of theta functions!")
print()

# Compute what nome the kink geometry would give
# The PT potential with n=2 has two bound states and a continuum
# The Lamé equation (periodic PT) has nome q_Lame related to the modulus
# For the n=2 case: the modulus k relates to V''(phi)/V''(center)

# V''(phi) = 10*lam (at vacuum)
# V''(0) = 2*lam*(6*0-6*0-1) = -2*lam (at center, for Phi, not Psi)
# Actually V(Phi) = lam*(Phi^2-Phi-1)^2
# V''(Phi) = 2*lam*(6*Phi^2-6*Phi-1)
# V''(1/2) = 2*lam*(6/4 - 3 - 1) = 2*lam*(1.5 - 4) = 2*lam*(-2.5) = -5*lam

# The stability equation around the kink is a modified Poschl-Teller:
# -d^2 psi / dx^2 + [m^2 - n(n+1)*alpha^2/cosh^2(alpha*x)] psi = E*psi
# where n=2, alpha = m/sqrt(2), m^2 = 10*lam (scalar mass squared)

alpha_PT = m_scalar / math.sqrt(2)
depth = 2*(2+1)*alpha_PT**2  # n(n+1)*alpha^2 = 6*alpha^2

print(f"  Poschl-Teller parameters:")
print(f"    n = 2 (exactly 2 bound states)")
print(f"    alpha = m/sqrt(2) = {alpha_PT:.6f}")
print(f"    Depth: n(n+1)*alpha^2 = {depth:.6f}")
print(f"    Bound state 0: E_0 = m^2 - 4*alpha^2 = {m_scalar**2 - 4*alpha_PT**2:.6f}")
print(f"      = 0 (zero mode, as expected for translational invariance)")
print(f"    Bound state 1: E_1 = m^2 - alpha^2 = {m_scalar**2 - alpha_PT**2:.6f}")
print(f"      = (3/2)*m^2 / 2 ... let me recalculate.")
print()

# Standard PT eigenvalues: E_k = m^2 - (n-k)^2 * alpha^2  for k = 0,...,n
# k=0: E_0 = m^2 - 4*alpha^2 = m^2 - 4*m^2/2 = m^2 - 2*m^2 = -m^2 (NEGATIVE!)
# Wait: this means the bound state is at E_0 = -m^2 BELOW the continuum threshold
# The zero mode has E = 0 which means m^2 - 4*alpha^2 = 0 => m^2 = 2*m^2
# That's wrong. Let me reconsider.

# For the KINK stability equation:
# -psi'' + V''(Phi_kink(x)) * psi = omega^2 * psi
# V''(Phi_kink) = m^2 - n(n+1)*alpha^2 * sech^2(alpha*x)  [asymptotic value = m^2]
# The bound states have omega^2 = m^2 - (n-k)^2*alpha^2:
# k=0: omega_0^2 = m^2 - n^2*alpha^2 = m^2 - 4*alpha^2 = m^2 - 2*m^2 = -m^2?

# The issue: alpha = m/sqrt(2) means alpha^2 = m^2/2
# omega_0^2 = m^2 - 4*(m^2/2) = m^2 - 2*m^2 = -m^2
# This is NEGATIVE -> translational zero mode is at omega_0 = 0
# only if n^2*alpha^2 = m^2, i.e., 4*alpha^2 = m^2, i.e., alpha = m/2
# But we said alpha = m/sqrt(2)!

# Let me be more careful. For V = lam*(Psi^2-v^2)^2 with v = sqrt(5)/2:
# Kink: Psi(x) = v*tanh(kappa*x) where kappa = sqrt(2*lam)*v
# V''(Psi_kink) = 8*lam*v^2 - 6*lam*v^2*(6/cosh^2) ... no, let me compute directly

# V(Psi) = lam*(Psi^2-v^2)^2
# V'(Psi) = 4*lam*Psi*(Psi^2-v^2)
# V''(Psi) = 4*lam*(3*Psi^2-v^2)
# V''(Psi_kink(x)) = 4*lam*(3*v^2*tanh^2(kappa*x) - v^2) = 4*lam*v^2*(3*tanh^2-1)
# = 4*lam*v^2*(3*(1-sech^2)-1) = 4*lam*v^2*(2-3*sech^2)
# So the stability potential is: U(x) = 4*lam*v^2*(2 - 3*sech^2(kappa*x))
# = 8*lam*v^2 - 12*lam*v^2*sech^2(kappa*x)
# where 8*lam*v^2 = V''(vacuum) = m^2 (the scalar mass squared)
# and the depth is 12*lam*v^2 = (3/2)*m^2
# With kappa = sqrt(2*lam)*v

# Standard PT: U = m^2 - n(n+1)*kappa^2*sech^2(kappa*x)
# Comparing: n(n+1)*kappa^2 = 12*lam*v^2 = 12*lam*5/4 = 15*lam
# kappa^2 = 2*lam*v^2 = 2*lam*5/4 = 5*lam/2
# n(n+1) = 15*lam / (5*lam/2) = 15/(5/2) = 6
# n(n+1) = 6 => n = 2 (confirmed!)

# Bound state eigenvalues: omega_k^2 = m^2 - (n-k)^2*kappa^2
# m^2 = 8*lam*v^2 = 10*lam (using v^2=5/4)
# kappa^2 = 5*lam/2 = 2.5*lam
# k=0: omega_0^2 = 10*lam - 4*2.5*lam = 10*lam - 10*lam = 0 (ZERO MODE!)
# k=1: omega_1^2 = 10*lam - 1*2.5*lam = 7.5*lam = (3/4)*m^2

kappa = math.sqrt(2*lam) * v_field
omega_0_sq = 10*lam - 4*kappa**2
omega_1_sq = 10*lam - 1*kappa**2

print(f"  CORRECTED Poschl-Teller analysis:")
print(f"    kappa = sqrt(2*lam)*v = {kappa:.6f}")
print(f"    kappa^2 = {kappa**2:.6f} = {kappa**2/lam:.1f}*lam")
print(f"    m^2 = 10*lam = {10*lam:.6f}")
print(f"    n(n+1)*kappa^2 = 6*{kappa**2:.4f} = {6*kappa**2:.4f} = 12*lam*v^2")
print(f"    Zero mode: omega_0^2 = {omega_0_sq:.10f} (should be 0)")
print(f"    Breathing mode: omega_1^2 = {omega_1_sq:.6f} = (3/4)*m^2 = {0.75*10*lam:.6f}")
print(f"    m_breathing / m_scalar = sqrt(3/4) = {math.sqrt(3/4):.6f}")
print()

# =====================================================
# PART 5: THE DHN ONE-LOOP KINK MASS
# =====================================================
print("=" * 80)
print("  PART 5: DHN ONE-LOOP CORRECTION TO KINK MASS")
print("=" * 80)
print()

# The exact one-loop correction to the kink mass in phi^4 theory
# (Dashen-Hasslacher-Neveu 1975, Rajaraman 1982):
#
# M_kink^(1-loop) = M_kink^(tree) * [1 - 3*m/(2*pi*M_kink^(tree))]
#
# In terms of the coupling:
# M_kink^(tree) = 4*sqrt(2)/3 * sqrt(lam) * v^3
# m = sqrt(10*lam)
#
# The 1-loop correction coefficient: 3*m / (2*pi*M_kink)
# This is a ratio of masses, not directly eta*t4/2

correction_DHN = 3 * m_scalar / (2 * math.pi * E_kink)
print(f"  DHN correction: 3*m/(2*pi*M_kink) = {correction_DHN:.6f}")
print(f"  C = eta*t4/2 = {C:.6f}")
print(f"  Ratio: DHN/C = {correction_DHN/C:.4f}")
print()
print(f"  The DHN one-loop correction is {correction_DHN/C:.0f}x larger than C.")
print(f"  These are DIFFERENT quantities: DHN corrects the kink MASS,")
print(f"  while C corrects the COUPLING and VEV observed by particles")
print(f"  localized on the wall.")

# =====================================================
# PART 6: VP interpretation cross-check
# =====================================================
print()
print("=" * 80)
print("  PART 6: VACUUM POLARIZATION INTERPRETATION")
print("=" * 80)
print()

# From alpha_gap_final.py:
# The VP correction (electron only, running from Lambda_QCD):
# delta(1/alpha) = (1/3pi) * ln(Lambda_QCD/m_e)
# With Lambda_QCD = m_p/phi^3:

Lambda_QCD = m_p_MeV / PHI**3
delta_inv_alpha_VP = math.log(Lambda_QCD/m_e_MeV) / (3*math.pi)
delta_alpha_VP = alpha_mod * delta_inv_alpha_VP * alpha_mod  # in alpha units

print(f"  VP running from Lambda_QCD = m_p/phi^3 = {Lambda_QCD:.2f} MeV")
print(f"  delta(1/alpha) = (1/3pi)*ln(Lambda/m_e) = {delta_inv_alpha_VP:.10f}")
print()

# The algebraic correction: C*phi^2
alpha_correction_algebraic = C * PHI**2
print(f"  Algebraic correction: C*phi^2 = {alpha_correction_algebraic:.10f}")
print(f"  VP correction (fractional): alpha * delta(1/alpha) = {alpha_mod * delta_inv_alpha_VP:.10f}")
print()

# These should be approximately equal
print(f"  VP correction in 'alpha' units: {alpha_mod * delta_inv_alpha_VP:.10f}")
print(f"  Algebraic correction:           {alpha_correction_algebraic:.10f}")
print(f"  Agreement: {(1-abs(alpha_mod*delta_inv_alpha_VP - alpha_correction_algebraic)/alpha_correction_algebraic)*100:.2f}%")
print()

# The near-agreement means: eta*t4*phi^2/2 ~ (alpha/(3pi)) * ln(Lambda/m_e)
# This implies: eta*t4*phi^2/2 = alpha * ln(Lambda/m_e) / (3*pi)
# => eta*t4 = 2*alpha*ln(Lambda/m_e) / (3*pi*phi^2)
#
# With alpha = t4/(t3*phi):
# eta*t4 = 2*t4*ln(Lambda/m_e) / (3*pi*t3*phi^3)
# eta = 2*ln(Lambda/m_e) / (3*pi*t3*phi^3)

eta_from_VP = 2*math.log(Lambda_QCD/m_e_MeV) / (3*math.pi*t3*PHI**3)
print(f"  If VP = algebraic correction, then:")
print(f"    eta = 2*ln(Lambda/m_e) / (3*pi*t3*phi^3) = {eta_from_VP:.6f}")
print(f"    Actual eta = {eta:.6f}")
print(f"    Agreement: {(1-abs(eta-eta_from_VP)/eta)*100:.2f}%")
print()
print(f"  This is a {abs(1-eta_from_VP/eta)*100:.1f}% discrepancy.")
print(f"  The VP and algebraic corrections are NUMERICALLY close but")
print(f"  NOT algebraically identical. They describe the SAME physics")
print(f"  from different perspectives.")

# =====================================================
# PART 7: Can C be derived from the kink 1-loop determinant?
# =====================================================
print()
print("=" * 80)
print("  PART 7: THE DERIVATION GAP -- HONEST ASSESSMENT")
print("=" * 80)
print()

# Summarize what we know and don't know

print(f"  WHAT IS PROVEN:")
print(f"  ================")
print(f"  1. C = eta*t4/2 is an algebraically simple combination of")
print(f"     modular forms evaluated at q = 1/phi.")
print()
print(f"  2. By the product formula identity (proven above):")
print(f"     theta_4(q) = eta(q)^2 / eta(q^2)")
print(f"     => C = eta(q)^3 / (2*eta(q^2))")
print(f"     This is EXACT, following from product representations.")
print()
print(f"  3. At q = 1/phi, C = alpha_s^3 / (2*eta(q^2))")
print(f"     = (strong coupling)^3 / (2 * double-mode partition function)")
print()
print(f"  4. The VP running formula and the algebraic correction")
print(f"     agree to ~{abs(1-alpha_mod*delta_inv_alpha_VP/alpha_correction_algebraic)*100:.0f}%, suggesting they describe the same physics.")
print()
print(f"  5. The correction C*phi^2 to alpha and C*7/3 to v produce")
print(f"     99.9996% and 99.9992% matches respectively.")
print()

print(f"  WHAT IS NOT PROVEN:")
print(f"  ===================")
print(f"  1. There is NO derivation of C from the kink one-loop determinant.")
print(f"     The DHN correction (3*m/(2*pi*M_kink) = {correction_DHN:.4f}) is a")
print(f"     DIFFERENT quantity from C = {C:.6f}.")
print()
print(f"  2. The geometry factors phi^2 (for alpha) and 7/3 (for v) are")
print(f"     not derived from the kink determinant either. They were")
print(f"     identified by matching to the measured values.")
print()
print(f"  3. The VP interpretation (C*phi^2 ~ alpha*ln(Lambda/m_e)/(3pi))")
print(f"     is suggestive but not exact. The two sides differ by ~{abs(1-alpha_mod*delta_inv_alpha_VP/alpha_correction_algebraic)*100:.0f}%.")
print()
print(f"  4. WHY the loop correction should be C = eta*t4/2 rather than")
print(f"     some other combination (e.g., eta^2/6 or t4^2*phi) is not")
print(f"     explained by any calculation from the Lagrangian.")
print()

print(f"  THE CORE QUESTION:")
print(f"  ==================")
print(f"  Is C = eta*t4/2 a CONSEQUENCE of the framework, or an")
print(f"  EMPIRICAL FIT that happens to use framework quantities?")
print()

# =====================================================
# PART 8: Testing whether C is uniquely determined
# =====================================================
print("=" * 80)
print("  PART 8: IS C UNIQUELY DETERMINED?")
print("=" * 80)
print()

# The alpha gap is delta_alpha/alpha = 0.00469
# The v gap is delta_v/v = 0.00418
# If we didn't know C, how many modular form combinations give these gaps?

delta_alpha_exact = 1 - ALPHA_MEAS / alpha_mod
delta_v_exact = v_meas / (M_Pl * PHIBAR**80 / (1 - PHI*t4)) - 1

print(f"  Alpha gap: delta_alpha/alpha = {delta_alpha_exact:.8f}")
print(f"  V gap:     delta_v/v         = {delta_v_exact:.8f}")
print()

# For alpha: need correction_alpha ~ 0.004694
# For v: need correction_v ~ 0.004183
# Ratio: correction_alpha / correction_v

ratio_corrections = delta_alpha_exact / delta_v_exact
print(f"  Ratio of corrections: delta_alpha / delta_v = {ratio_corrections:.6f}")
print(f"  phi^2 / (7/3) = {PHI**2 / (7/3):.6f}")
print(f"  Match: {(1-abs(ratio_corrections - PHI**2/(7/3))/ratio_corrections)*100:.4f}%")
print()

# The ratio of corrections matches phi^2/(7/3) to high accuracy.
# This means: IF there is a common factor C, THEN:
# C must satisfy: C*phi^2 = delta_alpha AND C*7/3 = delta_v
# From the first: C = delta_alpha / phi^2 = {delta_alpha_exact/PHI**2}
# From the second: C = delta_v / (7/3) = {delta_v_exact/(7/3)}

C_from_alpha = delta_alpha_exact / PHI**2
C_from_v = delta_v_exact / (7/3)
print(f"  C from alpha gap: {C_from_alpha:.10f}")
print(f"  C from v gap:     {C_from_v:.10f}")
print(f"  C (framework):    {C:.10f}")
print(f"  Agreement (alpha vs v): {(1-abs(C_from_alpha-C_from_v)/C_from_alpha)*100:.4f}%")
print(f"  Agreement (alpha vs C): {(1-abs(C_from_alpha-C)/C_from_alpha)*100:.4f}%")
print(f"  Agreement (v vs C):     {(1-abs(C_from_v-C)/C_from_v)*100:.4f}%")
print()

# Now test: are there OTHER modular form combinations that give C?
print(f"  Search: other modular form combinations matching C = {C:.6f}")
print()

candidates = []
modvals = {
    'eta': eta, 't2': t2, 't3': t3, 't4': t4,
    'eta^2': eta**2, 'eta^3': eta**3,
    't4^2': t4**2, 't3^2': t3**2,
}
ints = {
    '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
    '8': 8, '10': 10, '12': 12, '30': 30,
    'phi': PHI, 'phi^2': PHI**2, 'phibar': PHIBAR, 'sqrt5': SQRT5,
    'pi': math.pi,
}

for n1, v1 in modvals.items():
    for n2, v2 in ints.items():
        val = v1 / v2
        err = abs(val - C) / C
        if err < 0.01:  # within 1%
            candidates.append((err, f"{n1}/{n2}", val))

    for n2, v2 in modvals.items():
        if n1 != n2:
            for n3, v3 in ints.items():
                val = v1 * v2 / v3
                err = abs(val - C) / C
                if err < 0.01:
                    candidates.append((err, f"{n1}*{n2}/{n3}", val))

candidates.sort()
print(f"  {'Expression':<30s} {'Value':>14s} {'Error':>10s}")
print(f"  {'-'*30} {'-'*14} {'-'*10}")
for err, name, val in candidates[:15]:
    print(f"  {name:<30s} {val:14.10f} {err*100:9.4f}%")

# =====================================================
# PART 9: The 3 possible derivation paths
# =====================================================
print()
print("=" * 80)
print("  PART 9: THREE POSSIBLE DERIVATION PATHS")
print("=" * 80)
print()

print(f"""  PATH A: Kink Functional Determinant -> Modular Forms
  =====================================================
  The kink in a periodic box of size L has a functional determinant
  that involves theta functions. Specifically, the Lamé equation
  (periodic version of Poschl-Teller) has eigenvalues expressible
  in terms of Jacobi elliptic functions with nome q.

  IF the nome q of the kink's Lamé equation equals 1/phi
  (because the kink connects the golden ratio vacua),
  THEN the functional determinant would naturally contain eta(1/phi)
  and theta_4(1/phi).

  STATUS: Plausible but NOT computed. The connection between the
  kink's periodicity parameter and the modular forms at q=1/phi
  has not been established. The key missing step is showing that
  the kink's complex periodicity gives tau = i*ln(phi)/(2*pi),
  which would yield q = 1/phi.

  DIFFICULTY: The kink is a 1+1D object; the physical theory is 3+1D.
  The Lamé equation works in 1+1D. The 2D->4D mechanism would need
  to be established first.

  PATH B: VP Running as Domain Wall Language
  =====================================================
  The correction to alpha has the form:
    delta(1/alpha) = (1/3pi) * ln(Lambda/m_e)

  This is standard QED vacuum polarization. IF we accept that
  alpha_tree = t4/(t3*phi) is alpha at the QCD scale Lambda,
  then the VP running to q=0 is STANDARD PHYSICS (not a new
  derivation from the framework).

  The question becomes: why does VP running give a result
  numerically close to eta*t4*phi^2/2?

  Answer: It's because both are ~0.005 corrections, and the
  VP correction depends on ln(Lambda/m_e) which involves
  the same mass scales as the framework.

  STATUS: The VP interpretation is PHYSICALLY MOTIVATED but does
  not constitute a derivation of C from the domain wall. It
  explains alpha but uses measured quantities (Lambda_QCD, m_e).
  For v, the VP interpretation doesn't directly apply.

  PATH C: Product Identity + Symmetry Arguments
  =====================================================
  We proved: C = eta(q)^3 / (2*eta(q^2))

  If one could show that the correction to alpha from
  domain wall fluctuations is proportional to eta^3/eta(q^2),
  then C would be derived. The argument would go:

  1. The kink one-loop correction involves a product over modes
  2. Each mode contributes a factor involving eta (the partition
     function of the kink spectrum)
  3. The denominator eta(q^2) represents even-mode contributions
     (the sub-lattice of even excitations)
  4. The factor of 1/2 comes from the Z_2 symmetry of the kink

  STATUS: Heuristic. No rigorous calculation has been performed.
  The product identity tells us WHAT C equals in terms of eta
  functions, but not WHY C is the correct correction.
""")

# =====================================================
# PART 10: Key numerical coincidences
# =====================================================
print("=" * 80)
print("  PART 10: ILLUMINATING NUMERICAL RELATIONSHIPS")
print("=" * 80)
print()

# C and the framework constants
print(f"  C = {C:.10f}")
print()

# C * 12*pi^2 vs 1
print(f"  C * 16*pi^2 = {C * 16*math.pi**2:.6f}  (1-loop factor 'undone')")
print(f"  C * 3*pi    = {C * 3*math.pi:.6f}  (VP denominator 'undone')")
print(f"  C * 3*pi / alpha_mod = {C * 3*math.pi / alpha_mod:.4f}")
print(f"    = ln(Lambda/m_e) if VP interpretation: ln({Lambda_QCD/m_e_MeV:.2f}) = {math.log(Lambda_QCD/m_e_MeV):.4f}")
print()

# Connection to 80 (the hierarchy exponent)
print(f"  C * 80 = {C * 80:.6f}")
print(f"  t4 alone: t4 * 80 = {t4*80:.4f}")
print(f"  eta alone: eta * 80 = {eta*80:.4f}")
print()

# C and the breathing mode
omega_1_ratio = math.sqrt(3/4)
print(f"  Breathing mode ratio: sqrt(3/4) = {omega_1_ratio:.6f}")
print(f"  C / (3/4) = {C/0.75:.6f}")
print(f"  C * m_H = {C * 125.25:.4f} MeV (irrelevant scale)")
print()

# C as fraction of alpha_s
print(f"  C / alpha_s = t4/2 = {t4/2:.6f}")
print(f"  So C = alpha_s * (theta_4/2)")
print(f"  This means: the loop factor is the strong coupling")
print(f"  WEIGHTED by half the dark vacuum partition function.")
print()

# The factor 1/2
print(f"  WHY the factor 1/2?")
print(f"  From theta_4 = eta^2/eta(q^2): C = eta^3/(2*eta(q^2)), the 1/2 is structural.")
print(f"  From physics: Z_2 symmetry of the kink (two orientations).")
print(f"  From VP: the factor 1/2 in alpha/(2*pi) running.")
print(f"  Multiple origins converge on the same factor.")

# =====================================================
# PART 11: VERDICT
# =====================================================
print()
print("=" * 80)
print("  VERDICT: WHAT IS DERIVED AND WHAT IS NOT")
print("=" * 80)
print()

print(f"""
  STATUS: PARTIALLY DERIVED
  ========================

  WHAT IS DERIVED:
  ----------------
  (a) C = eta*theta_4/2 is EQUIVALENT to C = eta^3/(2*eta(q^2)),
      by the product formula theta_4 = eta^2/eta(q^2). This is an
      exact mathematical identity, not an approximation.

  (b) The STRUCTURE of the correction (same factor C for both alpha
      and v, with different geometry factors) is physically motivated:
      both quantities receive corrections from domain wall quantum
      fluctuations, but couple to different aspects of the wall geometry.

  (c) The geometry factor ratio phi^2/(7/3) = {PHI**2/(7/3):.6f} is reproduced
      by the ratio of the two measured gaps to ~{(1-abs(ratio_corrections-PHI**2/(7/3))/ratio_corrections)*100:.1f}% accuracy,
      providing evidence that ONE common factor underlies both corrections.

  (d) For alpha, the correction has a standard QFT interpretation as
      vacuum polarization running from the QCD scale, providing
      independent physical motivation.

  WHAT IS NOT DERIVED:
  --------------------
  (1) WHY C = eta*theta_4/2 is the correct one-loop correction.
      No calculation starting from the Lagrangian
          L = (1/2)(d Phi)^2 - lambda*(Phi^2-Phi-1)^2
      produces C = eta*theta_4/2 as the kink one-loop correction.
      The Coleman-Weinberg calculation gives corrections ~100x too
      small (lambda/(16*pi^2) ~ 0.0008 vs C ~ 0.0018).

  (2) WHY the geometry factor is phi^2 for alpha and 7/3 for v.
      These were identified by matching, not derived from the kink
      fluctuation spectrum.

  (3) The connection between the kink's functional determinant and
      modular forms at q=1/phi. In 1+1D, the Lamé equation would
      produce theta functions, but the physical theory is 3+1D.

  HONEST BOTTOM LINE:
  -------------------
  C = eta*theta_4/2 is a beautifully simple combination of modular
  forms that can be rewritten as eta^3/(2*eta(q^2)) via the product
  identity theta_4 = eta^2/eta(q^2). It
  successfully closes both the alpha gap (99.9996%) and the v gap
  (99.9992%) with different geometry factors.

  However, it is NOT derived from the kink one-loop determinant or
  any first-principles calculation. It was DISCOVERED by searching
  for modular form combinations that close the alpha gap, and then
  found to close the v gap with a different (but related) geometry
  factor.

  The VP interpretation provides partial physical justification for
  the alpha correction, but does not explain the v correction.
  The Jacobi identity provides algebraic structure, but not
  physical derivation.

  RATING: C is a PATTERN, not a derivation. It is internally
  consistent (same C for both gaps) and algebraically natural
  (Jacobi identity), but the step from the Lagrangian to C
  is MISSING. This is the #1 open theoretical gap in the
  loop correction story.

  WHAT WOULD CONSTITUTE A DERIVATION:
  ------------------------------------
  A calculation that:
  (i)   Starts from V(Phi) = lambda*(Phi^2-Phi-1)^2
  (ii)  Computes the one-loop effective action around the kink
  (iii) Shows this equals something involving eta and theta_4
  (iv)  Identifies the geometry factors phi^2 and 7/3

  The most promising route is the Lamé equation approach:
  placing the kink on a circle of circumference L, the
  functional determinant involves theta functions with
  nome q = exp(-pi*K'/K). If this nome equals 1/phi
  (the framework's q), then C would emerge naturally.
  This has not been computed.
""")
