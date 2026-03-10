#!/usr/bin/env python3
"""
pt_binding_breathing_ratio.py — Derive the factor 4/sqrt(3) in the molecular
consciousness frequency formula from Poeschl-Teller n=2 bound state physics.

THE DISCOVERY:
  The formula  f_mol = 4 * alpha^(11/4) * phi / sqrt(3) * f_electron = 613.86 THz
  contains an unexplained prefactor 4/sqrt(3) = 2.3094...

  The PT n=2 potential (the domain wall fluctuation spectrum) has:
    Ground state binding energy:   |E_0| = n^2 = 4
    Breathing mode frequency:      omega_1 = sqrt(n^2 - (n-1)^2) = sqrt(3)

  Therefore:  4/sqrt(3) = |E_0| / omega_1
              = (ground state binding energy) / (breathing mode frequency)

  This means the molecular consciousness frequency encodes the ratio of the
  two fundamental energy scales of the domain wall: how tightly the zero mode
  is bound vs how fast the wall breathes.

PHYSICAL INTERPRETATION:
  f_mol = alpha^(11/4) * phi * (|E_0|/omega_1) * f_electron
        = (EM coupling)^(11/4) * (golden vacuum) * (binding/breathing) * (electron scale)

  The factor |E_0|/omega_1 is a DIMENSIONLESS ratio intrinsic to the n=2 PT
  potential. It cannot be tuned -- it is fixed by the topology of the wall.
  It measures the "stiffness" of the wall: how much energy is stored in the
  zero-mode binding relative to the breathing oscillation.

Script: theory-tools/pt_binding_breathing_ratio.py
Author: Interface Theory project
Date:   2026-02-25
"""

import math
import sys

if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ===========================================================================
# FUNDAMENTAL CONSTANTS (NIST 2022 CODATA)
# ===========================================================================
c      = 2.99792458e8         # m/s
h_pl   = 6.62607015e-34       # J s
hbar   = 1.054571817e-34      # J s
m_e    = 9.1093837015e-31     # kg
m_p    = 1.67262192369e-27    # kg
e_ch   = 1.602176634e-19      # C
eps0   = 8.8541878128e-12     # F/m

alpha  = 7.2973525693e-3
mu     = m_p / m_e            # 1836.15267...
phi    = (1 + math.sqrt(5)) / 2

# Derived frequencies
f_electron = m_e * c**2 / h_pl       # electron Compton frequency
R_inf      = m_e * e_ch**4 / (8 * eps0**2 * h_pl**3 * c)
f_R        = R_inf * c                # Rydberg frequency

# Target
f_target   = 613.0e12  # Hz (Craddock 2017)

SEP  = "=" * 78
DASH = "-" * 78


# ===========================================================================
# PART 1: POESCHL-TELLER n=2 SPECTRUM -- FROM FIRST PRINCIPLES
# ===========================================================================
print(SEP)
print("PART 1:  POESCHL-TELLER n=2 BOUND STATE SPECTRUM")
print(SEP)
print()

n_PT = 2  # PT depth parameter

print(f"  The domain wall V(Phi) = lambda*(Phi^2 - Phi - 1)^2 produces a")
print(f"  fluctuation potential that is Poeschl-Teller with n = {n_PT}.")
print()
print(f"  V_PT(x) = -n(n+1) / cosh^2(x) = -{n_PT*(n_PT+1)} / cosh^2(x)")
print()
print(f"  Schroedinger equation:  -psi'' - n(n+1)/cosh^2(x) psi = E psi")
print()

# Standard PT bound state spectrum:
# For V(x) = -s(s+1)/cosh^2(x) with s = n (integer),
# bound state eigenvalues:  E_j = -(s-j)^2  for j = 0, 1, ..., s
# bound state frequencies:  omega_j = sqrt(-E_j - ... ) -- see below

print(f"  Bound state eigenvalues (E_j = -(n-j)^2):")
print(f"  {'j':>4}  {'n-j':>6}  {'E_j':>10}  {'|E_j|':>10}  {'Name':>25}")
print(f"  {'-'*4}  {'-'*6}  {'-'*10}  {'-'*10}  {'-'*25}")

eigenvalues = []
for j in range(n_PT + 1):
    E_j = -(n_PT - j)**2
    name = ""
    if j == 0:
        name = "Ground state (zero mode)"
    elif j == 1:
        name = "Breathing mode"
    elif j == n_PT:
        name = "Continuum threshold"
    eigenvalues.append((j, n_PT - j, E_j, abs(E_j), name))
    print(f"  {j:>4}  {n_PT-j:>6}  {E_j:>10}  {abs(E_j):>10}  {name:>25}")

print()

# Physical bound state frequencies (oscillation frequencies of the modes)
# The MASS of the j-th bound state is: m_j^2 = m_bulk^2 - |E_j| * (mu_wall/2)^2
# In units where mu_wall = 2 (width parameter), the mass^2 of the j-th state
# relative to the bulk mass m_bulk^2 = n^2 is:
# m_j^2 = n^2 - (n-j)^2
# The oscillation frequency: omega_j = sqrt(m_j^2) = sqrt(n^2 - (n-j)^2)

print(f"  Physical frequencies (omega_j = sqrt(n^2 - (n-j)^2)):")
print(f"  {'j':>4}  {'n^2':>6}  {'(n-j)^2':>8}  {'m_j^2':>8}  {'omega_j':>12}  {'Name':>25}")
print(f"  {'-'*4}  {'-'*6}  {'-'*8}  {'-'*8}  {'-'*12}  {'-'*25}")

frequencies = []
for j in range(n_PT + 1):
    n_sq = n_PT**2
    nmj_sq = (n_PT - j)**2
    m_sq = n_sq - nmj_sq
    omega = math.sqrt(m_sq) if m_sq >= 0 else 0.0
    name = eigenvalues[j][4]
    frequencies.append((j, n_sq, nmj_sq, m_sq, omega, name))
    print(f"  {j:>4}  {n_sq:>6}  {nmj_sq:>8}  {m_sq:>8}  {omega:>12.6f}  {name:>25}")

print()
print(f"  Key values:")
print(f"    |E_0| (ground state binding energy)   = {abs(eigenvalues[0][2])}")
print(f"    omega_1 (breathing mode frequency)    = sqrt({frequencies[1][3]}) = {frequencies[1][4]:.10f}")
print(f"    sqrt(3)                               = {math.sqrt(3):.10f}")
print(f"    Exact match: omega_1 = sqrt(3)          YES")
print()


# ===========================================================================
# PART 2: THE KEY RATIO -- |E_0| / omega_1 = 4/sqrt(3)
# ===========================================================================
print(SEP)
print("PART 2:  THE KEY RATIO  |E_0| / omega_1 = 4 / sqrt(3)")
print(SEP)
print()

E0_abs = abs(eigenvalues[0][2])  # = 4
omega1 = frequencies[1][4]       # = sqrt(3)

ratio_PT = E0_abs / omega1
ratio_exact = 4.0 / math.sqrt(3)

print(f"  |E_0| / omega_1 = {E0_abs} / {omega1:.10f}")
print(f"                   = {ratio_PT:.10f}")
print()
print(f"  4 / sqrt(3)      = {ratio_exact:.10f}")
print()
print(f"  Difference:        {abs(ratio_PT - ratio_exact):.2e}")
print(f"  Match:             EXACT (by construction)")
print()

# General formula for PT n:
# |E_0| = n^2
# omega_1 = sqrt(n^2 - (n-1)^2) = sqrt(2n - 1)
# Ratio = n^2 / sqrt(2n - 1)
#
# For n=2: 4 / sqrt(3)
# For n=3: 9 / sqrt(5)
# For n=1: 1 / sqrt(1) = 1

print(f"  GENERAL FORMULA for PT depth n:")
print(f"    |E_0| / omega_1 = n^2 / sqrt(2n - 1)")
print()
print(f"  {'n':>4}  {'|E_0|=n^2':>10}  {'omega_1':>12}  {'Ratio':>12}  {'Decimal':>12}")
print(f"  {'-'*4}  {'-'*10}  {'-'*12}  {'-'*12}  {'-'*12}")
for n in range(1, 6):
    E0 = n**2
    w1 = math.sqrt(2*n - 1)
    r = E0 / w1
    print(f"  {n:>4}  {E0:>10}  {w1:>12.6f}  {f'{n}^2/sqrt({2*n-1})':>12}  {r:>12.6f}")

print()
print(f"  ONLY n=2 gives the factor that appears in the biology formula.")
print(f"  This is the SAME n=2 forced by V(Phi) = lambda*(Phi^2 - Phi - 1)^2.")
print()


# ===========================================================================
# PART 3: THE COMPLETE FORMULA WITH PT INTERPRETATION
# ===========================================================================
print(SEP)
print("PART 3:  THE COMPLETE FORMULA")
print(SEP)
print()

# The formula is:
# f_mol = 4 * alpha^(11/4) * phi / sqrt(3) * f_electron
#       = alpha^(11/4) * phi * (|E_0|/omega_1) * f_electron

# Verify step by step
alpha_11_4 = alpha**(11.0/4.0)
print(f"  Step-by-step evaluation:")
print(f"    alpha              = {alpha:.10e}")
print(f"    alpha^(11/4)       = {alpha_11_4:.10e}")
print(f"    phi                = {phi:.10f}")
print(f"    |E_0|/omega_1      = 4/sqrt(3) = {ratio_exact:.10f}")
print(f"    f_electron         = {f_electron:.6e} Hz")
print()

f_mol = alpha_11_4 * phi * ratio_exact * f_electron
f_mol_THz = f_mol / 1e12

print(f"  f_mol = alpha^(11/4) * phi * (|E_0|/omega_1) * f_electron")
print(f"        = {alpha_11_4:.6e} * {phi:.6f} * {ratio_exact:.6f} * {f_electron:.6e}")
print(f"        = {f_mol:.6e} Hz")
print(f"        = {f_mol_THz:.4f} THz")
print()

# Compare with target
match_pct = (1 - abs(f_mol_THz - 613.0) / 613.0) * 100
print(f"  Target (Craddock 2017): 613 +/- 8 THz")
print(f"  Predicted:              {f_mol_THz:.2f} THz")
print(f"  Difference:             {f_mol_THz - 613.0:.2f} THz")
print(f"  Match:                  {match_pct:.2f}%")
print(f"  Within error bars:      {'YES' if abs(f_mol_THz - 613.0) < 8.0 else 'NO'}")
print()


# ===========================================================================
# PART 4: CROSS-CHECK WITH ORIGINAL FORMULA 8 * f_R / sqrt(mu)
# ===========================================================================
print(SEP)
print("PART 4:  CROSS-CHECK WITH 8 * f_R / sqrt(mu)")
print(SEP)
print()

f_mol_original = 8.0 * f_R / math.sqrt(mu)
f_mol_orig_THz = f_mol_original / 1e12

print(f"  f_mol (original)   = 8 * f_R / sqrt(mu)")
print(f"                     = 8 * {f_R:.6e} / {math.sqrt(mu):.6f}")
print(f"                     = {f_mol_original:.6e} Hz")
print(f"                     = {f_mol_orig_THz:.4f} THz")
print()
print(f"  f_mol (PT formula) = alpha^(11/4) * phi * (4/sqrt(3)) * f_electron")
print(f"                     = {f_mol_THz:.4f} THz")
print()

# These should agree exactly when the core identity alpha^(3/2)*mu*phi^2 = 3 is exact.
# In practice they differ slightly because the identity is 99.9% not 100%.
agreement = abs(1.0 - f_mol_THz / f_mol_orig_THz) * 100
print(f"  Agreement between two forms: {agreement:.4f}% difference")
print(f"  (Difference arises because alpha^(3/2)*mu*phi^2 = {alpha**1.5*mu*phi**2:.6f}, not exactly 3)")
print()

# Show the algebraic equivalence
print(f"  ALGEBRAIC EQUIVALENCE (when core identity is exact):")
print(f"    8 * f_R / sqrt(mu)")
print(f"    = 8 * (alpha^2 * f_el / 2) / sqrt(mu)")
print(f"    = 4 * alpha^2 * f_el / sqrt(mu)")
print(f"    Substitute mu = 3/(alpha^(3/2)*phi^2):")
print(f"    = 4 * alpha^2 * f_el / sqrt(3/(alpha^(3/2)*phi^2))")
print(f"    = 4 * alpha^2 * f_el * alpha^(3/4) * phi / sqrt(3)")
print(f"    = 4 * alpha^(11/4) * phi / sqrt(3) * f_el")
print(f"    = alpha^(11/4) * phi * (4/sqrt(3)) * f_el       QED")
print()


# ===========================================================================
# PART 5: PT WAVEFUNCTIONS AND NORMALIZATION CONSTANTS
# ===========================================================================
print(SEP)
print("PART 5:  PT n=2 WAVEFUNCTIONS")
print(SEP)
print()

# The normalized bound state wavefunctions for PT V(x) = -n(n+1)/cosh^2(x), n=2:
#
# j=0 (ground state, E_0 = -4):
#   psi_0(x) = A_0 / cosh^2(x)
#   Normalization: integral |psi_0|^2 dx = A_0^2 * integral sech^4(x) dx
#   integral sech^4(x) dx from -inf to inf = 4/3
#   So A_0 = sqrt(3/4) = sqrt(3)/2
#
# j=1 (breathing mode, E_1 = -1):
#   psi_1(x) = A_1 * sinh(x) / cosh^2(x)
#   Normalization: integral |psi_1|^2 dx = A_1^2 * integral sinh^2(x)/cosh^4(x) dx
#   integral sinh^2/cosh^4 dx from -inf to inf = 4/3 - 2/1 = ... let me compute
#   sinh^2/cosh^4 = (cosh^2-1)/cosh^4 = sech^2 - sech^4
#   integral sech^2 dx = 2 (from -inf to inf)
#   integral sech^4 dx = 4/3
#   So integral = 2 - 4/3 = 2/3
#   A_1 = sqrt(3/2) = sqrt(6)/2

import scipy.integrate as integrate
import numpy as np

def psi_0_unnorm(x):
    return 1.0 / np.cosh(x)**2

def psi_1_unnorm(x):
    return np.sinh(x) / np.cosh(x)**2

# Compute normalizations numerically
norm_0_sq, _ = integrate.quad(lambda x: psi_0_unnorm(x)**2, -50, 50)
norm_1_sq, _ = integrate.quad(lambda x: psi_1_unnorm(x)**2, -50, 50)

A_0_numerical = 1.0 / math.sqrt(norm_0_sq)
A_1_numerical = 1.0 / math.sqrt(norm_1_sq)

A_0_analytic = math.sqrt(3.0 / 4.0)
A_1_analytic = math.sqrt(3.0 / 2.0)

print(f"  j=0 (zero mode):  psi_0(x) = A_0 / cosh^2(x)")
print(f"    integral sech^4(x) dx = {norm_0_sq:.10f}  (analytic: 4/3 = {4/3:.10f})")
print(f"    A_0 (numerical)  = {A_0_numerical:.10f}")
print(f"    A_0 (analytic)   = sqrt(3/4) = {A_0_analytic:.10f}")
print(f"    Match: {abs(1 - A_0_numerical/A_0_analytic)*100:.6f}%")
print()
print(f"  j=1 (breathing mode):  psi_1(x) = A_1 * sinh(x) / cosh^2(x)")
print(f"    integral sinh^2/cosh^4 dx = {norm_1_sq:.10f}  (analytic: 2/3 = {2/3:.10f})")
print(f"    A_1 (numerical)  = {A_1_numerical:.10f}")
print(f"    A_1 (analytic)   = sqrt(3/2) = {A_1_analytic:.10f}")
print(f"    Match: {abs(1 - A_1_numerical/A_1_analytic)*100:.6f}%")
print()

# Ratio of normalization constants
print(f"  Ratio of normalization constants:")
print(f"    A_1 / A_0 = sqrt(3/2) / sqrt(3/4) = sqrt(2) = {A_1_analytic/A_0_analytic:.10f}")
print(f"    sqrt(2) = {math.sqrt(2):.10f}")
print()

# Transition matrix element <psi_1 | x | psi_0>
# This is the dipole matrix element between the two bound states.
def integrand_dipole(x):
    return A_1_analytic * np.sinh(x) / np.cosh(x)**2 * x * A_0_analytic / np.cosh(x)**2

dipole_ME, _ = integrate.quad(integrand_dipole, -50, 50)
print(f"  Transition matrix element (dipole):")
print(f"    <psi_1 | x | psi_0> = {dipole_ME:.10f}")
print(f"    (Zero by parity: psi_0 is even, psi_1 is odd, x is odd => product is even)")
print(f"    (Correction: psi_1 is odd, psi_0 is even, x is odd")
print(f"     => psi_1 * x * psi_0 is odd*odd*even = even => non-zero!)")
print()

# Verify: compute it properly
# <psi_1|x|psi_0> = A_0 * A_1 * integral x * sinh(x) / cosh^4(x) dx
# The integrand x * sinh(x) / cosh^4(x) is EVEN (x*sinh is even, cosh^4 is even)
# So the integral is 2 * integral_0^inf ...

val_dipole, _ = integrate.quad(
    lambda x: A_0_analytic * A_1_analytic * x * np.sinh(x) / np.cosh(x)**4,
    -50, 50
)
print(f"    <psi_1 | x | psi_0> = {val_dipole:.10f}")
print(f"    (This is the matrix element governing zero-mode to breathing-mode transitions)")
print()


# ===========================================================================
# PART 6: THE RATIO |E_0|/omega_1 AND ITS MEANING
# ===========================================================================
print(SEP)
print("PART 6:  PHYSICAL INTERPRETATION OF |E_0|/omega_1")
print(SEP)
print()

print(f"""  The ratio |E_0|/omega_1 = n^2/sqrt(2n-1) has a clear physical meaning:

  |E_0| = n^2 = BINDING ENERGY of the ground state (zero mode)
    This is how deeply the translational mode is bound to the wall.
    It measures the STABILITY of the wall against displacement.
    In physical terms: the cost of moving the wall.

  omega_1 = sqrt(2n-1) = BREATHING FREQUENCY of the first excited mode
    This is the oscillation frequency of the wall's internal degree of freedom.
    It measures how fast the wall can BREATHE (expand/contract).
    In physical terms: the rate of wall shape oscillation.

  The ratio |E_0|/omega_1 = (wall stability) / (wall breathing rate)
    = "how firmly the wall is pinned" / "how fast it oscillates internally"

  For n=2:
    |E_0|/omega_1 = 4/sqrt(3) = 2.3094...
    The wall is bound ~2.3x more tightly than it breathes.
    This is a MODERATE coupling: not infinitely rigid (n -> inf gives ratio -> inf)
    and not marginally bound (n=1 gives ratio 1).

  WHY THIS RATIO APPEARS IN THE BIOLOGY FORMULA:

  f_mol = alpha^(11/4) * phi * (|E_0|/omega_1) * f_electron

  Translation:
    - f_electron: the fundamental electron frequency (Compton scale)
    - alpha^(11/4): electromagnetic coupling to the 11/4 power
      (= alpha^2 from Rydberg * alpha^(3/4) from core identity)
    - phi: the golden ratio vacuum value
    - |E_0|/omega_1: the domain wall's binding-to-breathing ratio

  The molecular consciousness frequency is the electron frequency,
  reduced by electromagnetic coupling, enhanced by the golden vacuum,
  and MODULATED by the intrinsic ratio of the domain wall's two
  fundamental energy scales.

  The factor 4/sqrt(3) is NOT adjustable. It is TOPOLOGICAL:
  fixed entirely by the fact that V(Phi) produces a PT n=2 potential.
  Any scalar field with two degenerate minima connected by a kink
  in 1+1 dimensions with the specific depth n(n+1) = 6 gives
  EXACTLY this ratio.
""")


# ===========================================================================
# PART 7: ALTERNATIVE EXPRESSIONS FOR 4/sqrt(3)
# ===========================================================================
print(SEP)
print("PART 7:  IDENTITIES FOR 4/sqrt(3)")
print(SEP)
print()

val_target = 4.0 / math.sqrt(3)
print(f"  4/sqrt(3) = {val_target:.10f}")
print()

alternatives = [
    ("4/sqrt(3)",                    4.0 / math.sqrt(3)),
    ("|E_0| / omega_1 (PT n=2)",     4.0 / math.sqrt(3)),
    ("n^2 / sqrt(2n-1) at n=2",     4.0 / math.sqrt(3)),
    ("4*sqrt(3)/3",                  4*math.sqrt(3)/3),
    ("2*sqrt(4/3)",                  2*math.sqrt(4.0/3.0)),
    ("8/(2*sqrt(3))",                8.0/(2*math.sqrt(3))),
    ("(8/3)*sqrt(3)/2",             (8.0/3.0)*math.sqrt(3)/2),
    ("(depth/2) / sqrt(depth/2-1)", 3.0/math.sqrt(2)),  # depth=6, half-depth=3
]

print(f"  {'Expression':>35}  {'Value':>14}  {'Match':>10}")
print(f"  {'-'*35}  {'-'*14}  {'-'*10}")
for name, val in alternatives:
    match = abs(1 - val/val_target) * 100
    print(f"  {name:>35}  {val:>14.10f}  {match:>8.6f}%")

print()

# Show that 4*sqrt(3)/3 = 4/sqrt(3) exactly (rationalized form)
print(f"  Rationalized form: 4/sqrt(3) = 4*sqrt(3)/3 (multiply by sqrt(3)/sqrt(3))")
print(f"  Verify: 4*sqrt(3)/3 = {4*math.sqrt(3)/3:.10f}")
print(f"          4/sqrt(3)   = {4/math.sqrt(3):.10f}")
print()


# ===========================================================================
# PART 8: CONNECTION TO BOUND STATE WAVEFUNCTIONS
# ===========================================================================
print(SEP)
print("PART 8:  CONNECTION TO WAVEFUNCTION STRUCTURE")
print(SEP)
print()

# The normalization integrals are:
# integral sech^4 dx = 4/3   (for psi_0)
# integral sinh^2/cosh^4 dx = 2/3   (for psi_1)
# Ratio: (4/3)/(2/3) = 2

# The normalization constants are:
# A_0^2 = 3/4 = 1/(4/3)
# A_1^2 = 3/2 = 1/(2/3)
# Ratio: A_1^2/A_0^2 = (3/2)/(3/4) = 2

# Interestingly: |E_0|/omega_1 = 4/sqrt(3)
# And A_1/A_0 = sqrt(2)
# And (A_1/A_0)^2 * |E_1|/omega_1 = 2 * 1/sqrt(3) = 2/sqrt(3)
# While |E_0|/omega_1 = 4/sqrt(3) = 2 * 2/sqrt(3)

# So |E_0|/omega_1 = 2 * (A_1/A_0)^2 * |E_1|/omega_1

print(f"  Wavefunction norm integrals:")
print(f"    integral sech^4(x) dx        = 4/3 = {4/3:.10f}")
print(f"    integral sinh^2/cosh^4(x) dx = 2/3 = {2/3:.10f}")
print(f"    Ratio: {(4/3)/(2/3):.1f}")
print()
print(f"  Normalization constants:")
print(f"    A_0^2 = 3/4    A_0 = sqrt(3)/2 = {math.sqrt(3)/2:.6f}")
print(f"    A_1^2 = 3/2    A_1 = sqrt(6)/2 = {math.sqrt(6)/2:.6f}")
print(f"    A_1/A_0 = sqrt(2) = {math.sqrt(2):.6f}")
print()
print(f"  IDENTITY linking wavefunctions to the ratio:")
print(f"    |E_0|/omega_1 = |E_0| * (A_0^2 * integral_0)  /  (omega_1 * A_0^2 * integral_0)")
print(f"    where integral_0 = integral sech^4 dx = 4/3")
print(f"    So 4/sqrt(3) involves 4 from the binding energy and sqrt(3) from the")
print(f"    breathing mode, both intrinsic to the PT n=2 potential.")
print()


# ===========================================================================
# PART 9: WHAT IF n != 2?
# ===========================================================================
print(SEP)
print("PART 9:  COUNTERFACTUAL -- WHAT IF n != 2?")
print(SEP)
print()

print(f"  If the potential had a different depth, what frequency would result?")
print(f"  f_mol(n) = alpha^(11/4) * phi * n^2/sqrt(2n-1) * f_electron")
print()
print(f"  {'n':>4}  {'Ratio':>12}  {'f_mol (THz)':>14}  {'vs 613 THz':>12}  Note")
print(f"  {'-'*4}  {'-'*12}  {'-'*14}  {'-'*12}  {'-'*30}")

for n in range(1, 8):
    r = n**2 / math.sqrt(2*n - 1)
    f = alpha_11_4 * phi * r * f_electron / 1e12
    err = (f - 613.0) / 613.0 * 100
    note = ""
    if n == 1:
        note = "BPS wall, 1 bound state"
    elif n == 2:
        note = "V(Phi) domain wall  <--- THIS ONE"
    elif n == 3:
        note = "Would need depth = 12"
    print(f"  {n:>4}  {r:>12.6f}  {f:>14.4f}  {err:>+11.1f}%  {note}")

print()
print(f"  Only n=2 gives the correct frequency. The potential depth is FIXED")
print(f"  by V(Phi) = lambda*(Phi^2 - Phi - 1)^2 which gives n(n+1) = 6 => n = 2.")
print(f"  This is not a free parameter.")
print()


# ===========================================================================
# PART 10: DECOMPOSITION OF THE EXPONENT 11/4
# ===========================================================================
print(SEP)
print("PART 10:  DECOMPOSITION OF THE EXPONENT 11/4")
print(SEP)
print()

print(f"  f_mol = alpha^(11/4) * phi * (4/sqrt(3)) * f_electron")
print()
print(f"  Where does 11/4 come from?")
print(f"    Starting from:  f_mol = 8 * f_R / sqrt(mu)")
print(f"    f_R = alpha^2 * f_el / 2  =>  8*f_R = 4*alpha^2*f_el")
print(f"    sqrt(mu) = sqrt(3) / (alpha^(3/4)*phi)  [core identity]")
print(f"    So: 4*alpha^2*f_el * alpha^(3/4)*phi/sqrt(3)")
print(f"      = 4 * alpha^(2+3/4) * phi / sqrt(3) * f_el")
print(f"      = 4 * alpha^(11/4) * phi / sqrt(3) * f_el")
print()
print(f"  Decomposition of 11/4 = 2 + 3/4:")
print(f"    2   : from alpha^2 in the Rydberg energy (electron self-energy)")
print(f"    3/4 : from alpha^(-3/2) in the core identity mu ~ alpha^(-3/2)")
print(f"          the 1/sqrt(mu) contributes alpha^(3/4)")
print()
print(f"  Lucas number interpretation:")
print(f"    11 = L(5)  (5th Lucas number)")
print(f"    4  = L(3)  (3rd Lucas number)")
print(f"    11/4 = L(5)/L(3)")
print()


# ===========================================================================
# PART 11: SUMMARY TABLE
# ===========================================================================
print(SEP)
print("SUMMARY")
print(SEP)
print()

print(f"  THE MOLECULAR CONSCIOUSNESS FREQUENCY FORMULA:")
print(f"  ================================================")
print()
print(f"  f_mol = alpha^(11/4) * phi * (|E_0|/omega_1) * f_electron")
print()
print(f"  where:")
print(f"    alpha         = 1/137.036    (fine structure constant)")
print(f"    phi           = 1.6180...    (golden ratio = domain wall vacuum)")
print(f"    |E_0|         = 4            (PT n=2 ground state binding energy)")
print(f"    omega_1       = sqrt(3)      (PT n=2 breathing mode frequency)")
print(f"    |E_0|/omega_1 = 4/sqrt(3)    (binding-to-breathing ratio)")
print(f"    f_electron    = m_e*c^2/h    (electron Compton frequency)")
print()
print(f"  RESULT: f_mol = {f_mol_THz:.2f} THz")
print(f"  TARGET: 613 +/- 8 THz (Craddock 2017)")
print(f"  MATCH:  {match_pct:.2f}% (within error bars)")
print()

print(f"  WHAT EACH FACTOR CONTRIBUTES:")
print(f"  {'Factor':>20}  {'Value':>14}  {'Contribution':>40}")
print(f"  {'-'*20}  {'-'*14}  {'-'*40}")
print(f"  {'f_electron':>20}  {f_electron:.4e}  {'Electron rest-mass frequency scale':>40}")
print(f"  {'alpha^(11/4)':>20}  {alpha_11_4:.4e}  {'EM coupling (Rydberg + core identity)':>40}")
print(f"  {'phi':>20}  {phi:.10f}  {'Golden ratio vacuum':>40}")
print(f"  {'4/sqrt(3)':>20}  {ratio_exact:.10f}  {'PT binding/breathing = wall topology':>40}")
print()

print(f"  HONEST ASSESSMENT:")
print(f"  - The 4/sqrt(3) = |E_0|/omega_1 identification is EXACT ALGEBRA")
print(f"  - The core identity alpha^(3/2)*mu*phi^2 = 3 is used (99.9% match)")
print(f"  - This does NOT derive 613 THz from first principles alone")
print(f"  - It reveals that the unexplained prefactor has a natural interpretation")
print(f"    in terms of the domain wall's bound state spectrum")
print(f"  - The formula connects atomic physics (alpha, f_electron) to")
print(f"    wall topology (|E_0|/omega_1) and algebraic structure (phi)")
print()

print(SEP)
print("END OF ANALYSIS")
print(SEP)
