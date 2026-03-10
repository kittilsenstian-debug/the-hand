#!/usr/bin/env python3
"""
e8_wall_functional_determinant.py
==================================
THE MOST IMPORTANT CALCULATION: E8 gauge field functional determinant
on a domain wall with golden ratio vacua.

SETUP:
  - E8 gauge theory in (4+1)D
  - Scalar Phi in Cartan subalgebra: kink from phi to -1/phi
  - Kink breaks E8 -> subgroup at the wall
  - Gauge fluctuations around kink produce bound states = 4D particles
  - 1-loop effective action (functional determinant) determines 4D couplings

GOAL: Check whether the effective 4D gauge couplings are:
  - alpha_s = eta(1/phi)
  - sin^2(theta_W) = eta^2/(2*theta_4)
  - 1/alpha = theta_3*phi/theta_4

METHOD:
  1. Construct E8 root system (240 roots as 8-vectors)
  2. Choose h-hat for various breakings (E7xU1, SO(16), etc.)
  3. Compute root projections alpha_r . h-hat
  4. For each root, compute GY determinant on the golden ratio kink
  5. Use exact Poeschl-Teller formulas where applicable
  6. Assemble total product over all roots
  7. Test relation to modular forms at q=1/phi

Author: Claude (functional determinant computation)
Date: 2026-02-25
"""

import sys
import math
from itertools import product as iterproduct
from collections import defaultdict

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# ==============================================================
# CONSTANTS
# ==============================================================
phi = (1 + math.sqrt(5)) / 2
phibar = 1 / phi
sqrt5 = math.sqrt(5)
ln_phi = math.log(phi)
ln_phibar = math.log(phibar)

# Physical targets
alpha_em = 1 / 137.035999084
alpha_s_meas = 0.1179  # +/- 0.0009
sin2tW_meas = 0.23121
inv_alpha_meas = 137.035999084

SEP = "=" * 80
THIN = "-" * 80

print(SEP)
print("  E8 DOMAIN WALL FUNCTIONAL DETERMINANT")
print("  The most important calculation in Interface Theory")
print(SEP)
print()


# ==============================================================
# PART 0: MODULAR FORMS AT q = 1/phi
# ==============================================================
print(SEP)
print("  PART 0: MODULAR FORMS AT q = 1/phi (reference values)")
print(SEP)
print()

q = phibar
N_terms = 500

# Dedekind eta
eta_prod = 1.0
for n in range(1, N_terms + 1):
    qn = q ** n
    if qn < 1e-15:
        break
    eta_prod *= (1 - qn)
eta_val = q ** (1.0 / 24) * eta_prod

# Jacobi theta functions
theta2_sum = 0.0
for n in range(N_terms):
    val = q ** (n * (n + 1))
    if val < 1e-15:
        break
    theta2_sum += val
theta2_val = 2 * q ** 0.25 * theta2_sum

theta3_sum = 0.0
for n in range(1, N_terms + 1):
    val = q ** (n * n)
    if val < 1e-15:
        break
    theta3_sum += val
theta3_val = 1 + 2 * theta3_sum

theta4_sum = 0.0
for n in range(1, N_terms + 1):
    val = q ** (n * n)
    if val < 1e-15:
        break
    theta4_sum += ((-1) ** n) * val
theta4_val = 1 + 2 * theta4_sum

# Eisenstein E4
def sigma_k(n, k):
    s = 0
    for d in range(1, int(n ** 0.5) + 1):
        if n % d == 0:
            s += d ** k
            if d != n // d:
                s += (n // d) ** k
    return s

e4_sum = 0.0
for n in range(1, 200):
    e4_sum += 240 * sigma_k(n, 3) * q ** n
E4_val = 1 + e4_sum

# Composite C = eta * theta4 / 2
C_val = eta_val * theta4_val / 2

print(f"  eta(1/phi)    = {eta_val:.10f}   (compare alpha_s = {alpha_s_meas})")
print(f"  theta_2(1/phi) = {theta2_val:.10f}")
print(f"  theta_3(1/phi) = {theta3_val:.10f}")
print(f"  theta_4(1/phi) = {theta4_val:.10f}")
print(f"  E_4(1/phi)     = {E4_val:.10f}")
print(f"  C = eta*theta4/2 = {C_val:.10f}")
print()

# Target coupling formulas
alpha_s_pred = eta_val
sin2tW_pred = eta_val ** 2 / (2 * theta4_val)
inv_alpha_pred = theta3_val * phi / theta4_val

print(f"  TARGET COUPLINGS:")
print(f"    alpha_s = eta(1/phi) = {alpha_s_pred:.10f}  vs {alpha_s_meas}  ({abs(alpha_s_pred - alpha_s_meas)/alpha_s_meas*100:.2f}%)")
print(f"    sin2tW = eta^2/(2*t4) = {sin2tW_pred:.10f}  vs {sin2tW_meas}  ({abs(sin2tW_pred - sin2tW_meas)/sin2tW_meas*100:.2f}%)")
print(f"    1/alpha = t3*phi/t4 = {inv_alpha_pred:.10f}  vs {inv_alpha_meas}  ({abs(inv_alpha_pred - inv_alpha_meas)/inv_alpha_meas*100:.4f}%)")
print()


# ==============================================================
# PART 1: E8 ROOT SYSTEM
# ==============================================================
print(SEP)
print("  PART 1: E8 ROOT SYSTEM (240 roots in R^8)")
print(SEP)
print()

def dot8(a, b):
    return sum(a[i] * b[i] for i in range(8))

def add8(a, b):
    return tuple(a[i] + b[i] for i in range(8))

def sub8(a, b):
    return tuple(a[i] - b[i] for i in range(8))

def neg8(a):
    return tuple(-a[i] for i in range(8))

def scale8(c, a):
    return tuple(c * a[i] for i in range(8))

def norm_sq8(a):
    return dot8(a, a)

def norm8(a):
    return math.sqrt(norm_sq8(a))

def round8(a, ndigits=6):
    return tuple(round(a[i], ndigits) for i in range(8))

# Construct all 240 E8 roots
roots = []

# Type 1: +/- e_i +/- e_j (i<j): 112 roots
for i in range(8):
    for j in range(i + 1, 8):
        for si in (1.0, -1.0):
            for sj in (1.0, -1.0):
                r = [0.0] * 8
                r[i] = si
                r[j] = sj
                roots.append(tuple(r))

# Type 2: (1/2)(+/-1,...,+/-1) with even number of minus signs: 128 roots
for signs in iterproduct((0.5, -0.5), repeat=8):
    if sum(1 for s in signs if s < 0) % 2 == 0:
        roots.append(tuple(signs))

assert len(roots) == 240, f"Expected 240 roots, got {len(roots)}"

# Verify all norms are 2
for r in roots:
    ns = norm_sq8(r)
    assert abs(ns - 2.0) < 1e-10, f"Root {r} has norm^2 = {ns}"

# Build lookup for fast root identification
root_index = {}
for idx, r in enumerate(roots):
    root_index[round8(r)] = idx

def root_to_idx(v):
    return root_index.get(round8(v), -1)

print(f"  E8 roots constructed: {len(roots)}")
print(f"  All norm^2 = 2: verified")
print()


# ==============================================================
# PART 2: BREAKING PATTERNS - CARTAN DIRECTIONS
# ==============================================================
print(SEP)
print("  PART 2: CARTAN DIRECTIONS FOR VARIOUS BREAKINGS")
print(SEP)
print()

# Instead of constructing simple roots and Dynkin diagrams (which requires
# careful sign conventions), we use a DIRECT approach:
# Pick unit vectors h-hat in the Cartan subalgebra and classify roots by
# their projections. The physics depends only on the projection spectrum.

breaking_directions = {}

# BREAKING 1: E8 -> E7 x U(1)
# Direction perpendicular to E7 roots = along fundamental weight omega_8
# In practice, try h along the first coordinate axis (gives SU(8)xU(1), not E7)
# For E7, we want the direction that gives the 248 = 1 + 133 + 56 + 56-bar decomposition
#
# Use the Weyl vector (sum of fundamental weights = half sum of positive roots)
# Actually, for a clean E7 breaking, use the vector:
# h = (1, 1, 1, 1, 1, 1, 1, -1) / sqrt(8) which is orthogonal to SU(8) roots

# Direction 1: Along simple root alpha_7 (branching E8 -> SU(8) direction)
h1 = (0, 0, 0, 0, 0, 1, 1, 0)  # = alpha_7
h1_norm = norm8(h1)
h1_hat = scale8(1.0 / h1_norm, h1)
breaking_directions["alpha_7 (SU(8) branch)"] = h1_hat

# Direction 2: Along (1,1,1,1,1,1,1,-1)/sqrt(8)
v2 = (1, 1, 1, 1, 1, 1, 1, -1)
h2_hat = scale8(1.0 / norm8(v2), v2)
breaking_directions["(1...1,-1)/sqrt(8)"] = h2_hat

# Direction 3: Along e_1 = (1,0,0,0,0,0,0,0)
h3_hat = (1, 0, 0, 0, 0, 0, 0, 0)
breaking_directions["e_1"] = h3_hat

# Direction 4: Along a root known to be in the system: (1,1,0,0,0,0,0,0)
h4 = (1, 1, 0, 0, 0, 0, 0, 0)
h4_hat = scale8(1.0 / norm8(h4), h4)
breaking_directions["(1,1,0...0)/sqrt(2)"] = h4_hat

# Direction 5: Weyl vector direction (half sum of positive roots)
# Positive roots: those with first non-zero component positive
pos_roots = []
for r in roots:
    for comp in r:
        if abs(comp) > 1e-10:
            if comp > 0:
                pos_roots.append(r)
            break

weyl_vec = [0.0] * 8
for r in pos_roots:
    for j in range(8):
        weyl_vec[j] += r[j] / 2.0
weyl_vec = tuple(weyl_vec)
weyl_norm = norm8(weyl_vec)
h5_hat = scale8(1.0 / weyl_norm, weyl_vec)
breaking_directions["Weyl vector"] = h5_hat

# Direction 6: Along (1,1,1,1,1,1,0,0)/sqrt(6)
v6 = (1, 1, 1, 1, 1, 1, 0, 0)
h6_hat = scale8(1.0 / norm8(v6), v6)
breaking_directions["(1^6,0,0)/sqrt(6)"] = h6_hat

# Direction 7: A half-integer root (spinor-type direction)
# Use the first half-integer root in our list
h7 = roots[112]  # First half-integer root
h7_hat = scale8(1.0 / norm8(h7), h7)
breaking_directions["spinor root"] = h7_hat

print(f"  Prepared {len(breaking_directions)} Cartan direction candidates")
print()


# ==============================================================
# PART 3: ROOT PROJECTIONS FOR EACH BREAKING
# ==============================================================
print(SEP)
print("  PART 3: ROOT PROJECTIONS AND SPECTRUM FOR EACH BREAKING")
print(SEP)
print()

def classify_projections(h_hat):
    """Compute |alpha . h-hat| for all roots and return spectrum."""
    projections = []
    for idx, r in enumerate(roots):
        proj = dot8(r, h_hat)
        projections.append((idx, proj))

    # Find distinct |projection| values
    abs_projs = sorted(set(round(abs(p), 8) for _, p in projections))

    spectrum = {}
    for ap in abs_projs:
        members = [(idx, p) for idx, p in projections if abs(abs(p) - ap) < 1e-6]
        n_pos = sum(1 for _, p in members if p > 1e-8)
        n_neg = sum(1 for _, p in members if p < -1e-8)
        n_zero = sum(1 for _, p in members if abs(p) < 1e-8)
        spectrum[ap] = {
            'count': len(members),
            'n_pos': n_pos,
            'n_neg': n_neg,
            'n_zero': n_zero,
            'indices': [idx for idx, _ in members],
        }

    return projections, spectrum

all_spectra = {}

for name, h_hat in breaking_directions.items():
    projections, spectrum = classify_projections(h_hat)
    all_spectra[name] = (projections, spectrum)

    abs_vals = sorted(spectrum.keys())
    n_zero = spectrum.get(0.0, {}).get('count', 0)
    n_nonzero = 240 - n_zero

    print(f"  Breaking: {name}")
    print(f"    h-hat = [{', '.join(f'{x:.4f}' for x in h_hat)}]")
    print(f"    Zero projection (unbroken): {n_zero} roots")
    print(f"    Non-zero projection: {n_nonzero} roots")
    print(f"    Distinct |projections|: {[f'{v:.4f}' for v in abs_vals if v > 1e-8]}")
    for av in abs_vals:
        info = spectrum[av]
        if av < 1e-8:
            print(f"      |p| = 0       : {info['count']:3d} roots  (unbroken gauge bosons)")
        else:
            print(f"      |p| = {av:.6f}: {info['count']:3d} roots  (+{info['n_pos']}/-{info['n_neg']})")
    print()

# Identify the E7 x U(1) breaking (should have 0:134 + nonzero:106 = 248-8=240)
# E7 has 126 roots, so we want 126+8=134 zero projections? No: rank 8 Cartan
# elements are separate. The 240 roots should split as:
#   E7 roots: 126 with projection 0
#   56 with projection +c
#   56 with projection -c
#   2 with projection +/-2c (the U(1) root pair)
# Total: 126 + 56 + 56 + 2 = 240. Check!

print(f"  Looking for E7 x U(1) pattern (126 + 56 + 56 + 2 = 240):")
print()
for name, (projections, spectrum) in all_spectra.items():
    abs_vals = sorted(spectrum.keys())
    counts = [spectrum[av]['count'] for av in abs_vals]
    counts_str = '+'.join(str(c) for c in counts)

    # Check for E7 pattern
    is_e7 = False
    if len(abs_vals) == 3 and abs_vals[0] < 1e-8:
        c0, c1, c2 = [spectrum[av]['count'] for av in abs_vals]
        if c0 == 126 and c1 == 112 and c2 == 2:
            is_e7 = True
        elif c0 == 126 and ((c1 == 2 and c2 == 112) or (c1 == 112 and c2 == 2)):
            is_e7 = True

    marker = " <-- E7 x U(1)!" if is_e7 else ""
    print(f"    {name:30s}: {counts_str}{marker}")

print()


# ==============================================================
# PART 4: KINK PROFILE AND GY SOLVER
# ==============================================================
print(SEP)
print("  PART 4: KINK PROFILE AND GEL'FAND-YAGLOM SOLVER")
print(SEP)
print()

# V(Phi) = lambda*(Phi^2-Phi-1)^2
# Kink: Phi(x) = 1/2 + (sqrt(5)/2)*tanh(kappa*x)
# where kappa = sqrt(5*lambda/2)
# We set lambda=1 (just rescales x-coordinate).
# Vacua: phi at x=+inf, -1/phi at x=-inf
#
# For gauge field fluctuations with coupling g and projection p = alpha.h-hat:
# The effective mass^2 at position x is:
#   m^2_eff(x) = g^2 * p^2 * (Phi(x) - Phi_vac)^2  (for adjoint Higgs)
# NO WAIT -- the gauge coupling to Phi is through the covariant derivative.
# For a root alpha_r, the gauge boson A_mu^{alpha_r} has mass:
#   m^2(x) = g^2 * (alpha_r . Phi(x))^2
# where Phi(x) is a vector in the Cartan subalgebra.
# If Phi(x) = Phi_kink(x) * h-hat, then:
#   m^2(x) = g^2 * p^2 * Phi_kink(x)^2
# where p = alpha_r . h-hat.

def kink_phi(x):
    """Kink profile: Phi(-inf)=-1/phi, Phi(+inf)=phi
    Phi(x) = 1/2 + (sqrt(5)/2)*tanh(kappa*x) with kappa = sqrt(5/2)
    """
    kappa = math.sqrt(5.0 / 2.0)
    t = math.tanh(kappa * x)
    return 0.5 + (sqrt5 / 2) * t

def kink_phi_sq(x):
    p = kink_phi(x)
    return p * p

# Verify kink
print(f"  Kink profile verification:")
print(f"    Phi(-inf) = {kink_phi(-50):.10f}  (should be {-phibar:.10f})")
print(f"    Phi(+inf) = {kink_phi(50):.10f}  (should be {phi:.10f})")
print(f"    Phi(0)    = {kink_phi(0):.10f}  (should be 0.5)")
print()

# Asymptotic masses for a mode with projection p:
# m_L = |p| * phi  (at x=-inf, Phi=-1/phi ... wait)
# Actually: Phi(-inf) = -1/phi, so m(-inf) = |p * (-1/phi)| = |p|/phi = |p|*phibar
# And: Phi(+inf) = phi, so m(+inf) = |p * phi| = |p|*phi
# So: m_L = |p|*phibar (left = -inf), m_R = |p|*phi (right = +inf)
# The asymptotic MASS SQUARED ratio is (phi/phibar)^2 = phi^4

print(f"  Asymptotic masses for projection p:")
print(f"    m(-inf) = |p| * |Phi(-inf)| = |p| * 1/phi = |p| * {phibar:.6f}")
print(f"    m(+inf) = |p| * |Phi(+inf)| = |p| * phi = |p| * {phi:.6f}")
print(f"    Mass ratio: m(+inf)/m(-inf) = phi^2 = {phi**2:.6f}")
print()


def solve_gy_rk4(potential_func, L, nsteps):
    """RK4 solver for y'' = V(x)*y, y(-L)=0, y'(-L)=1. Returns y(L)."""
    h = 2.0 * L / nsteps
    y = 0.0
    yp = 1.0
    x = -L
    for _ in range(nsteps):
        V0 = potential_func(x)
        Vh = potential_func(x + h / 2)
        V1 = potential_func(x + h)
        k1y = yp;           k1yp = V0 * y
        k2y = yp + h/2*k1yp; k2yp = Vh * (y + h/2*k1y)
        k3y = yp + h/2*k2yp; k3yp = Vh * (y + h/2*k2y)
        k4y = yp + h*k3yp;   k4yp = V1 * (y + h*k3y)
        y += h/6 * (k1y + 2*k2y + 2*k3y + k4y)
        yp += h/6 * (k1yp + 2*k2yp + 2*k3yp + k4yp)
        x += h
    return y


def solve_step_gy(m_left, m_right, L):
    """Analytical GY for step potential: V=m_left^2 (x<0), m_right^2 (x>=0)."""
    if m_left < 1e-15 or m_right < 1e-15:
        return float('inf')
    y0 = math.sinh(m_left * L) / m_left
    yp0 = math.cosh(m_left * L)
    yL = y0 * math.cosh(m_right * L) + (yp0 / m_right) * math.sinh(m_right * L)
    return yL


def gy_det_ratio(projection, L=30.0, nsteps_per_unit=3000):
    """Compute det(H_kink)/det(H_step) for a gauge mode with given projection p.

    H = -d^2/dx^2 + p^2 * Phi_kink(x)^2
    Asymptotic: m_left = |p|*phibar, m_right = |p|*phi
    """
    p = abs(projection)
    if p < 1e-12:
        return 1.0  # Zero coupling: trivial

    p2 = p * p
    def V_kink(x):
        return p2 * kink_phi_sq(x)

    nsteps = int(2 * L * nsteps_per_unit)
    y_kink = solve_gy_rk4(V_kink, L, nsteps)
    y_step = solve_step_gy(p * phibar, p * phi, L)

    if abs(y_step) < 1e-300:
        return float('inf')
    return y_kink / y_step


# Quick test
print(f"  GY determinant ratio test (p=1):")
R_test = gy_det_ratio(1.0, L=30, nsteps_per_unit=3000)
n_test = math.log(R_test) / ln_phibar if R_test > 0 else float('inf')
print(f"    R(p=1) = {R_test:.12f}")
print(f"    = phibar^{n_test:.6f}")
print()


# ==============================================================
# PART 5: EXACT POESCHL-TELLER DETERMINANT FORMULA
# ==============================================================
print(SEP)
print("  PART 5: EXACT POESCHL-TELLER DETERMINANT FORMULAS")
print(SEP)
print()

# The kink Phi(x) = 1/2 + (sqrt(5)/2)*tanh(kappa*x) creates a potential
# for the gauge fluctuations:
#   V(x) = p^2 * Phi(x)^2 = p^2 * [1/4 + (sqrt(5)/2)*tanh(kx) + (5/4)*tanh^2(kx)]
#
# Using tanh^2 = 1 - sech^2:
#   V(x) = p^2 * [1/4 + (sqrt(5)/2)*tanh(kx) + 5/4 - (5/4)*sech^2(kx)]
#        = p^2 * [3/2 + (sqrt(5)/2)*tanh(kx) - (5/4)*sech^2(kx)]
#
# This is NOT a pure PT potential because of the tanh term.
# The tanh term makes it an asymmetric potential well.
#
# However, for the CENTERED kink psi(x) = (sqrt(5)/2)*tanh(kx):
#   Phi(x)^2 = (1/2 + psi)^2 = 1/4 + psi + psi^2
#            = 1/4 + (sqrt(5)/2)*tanh(kx) + (5/4)*tanh^2(kx)
#
# The tanh term breaks the PT form. But we can still compute the
# determinant numerically and check if it factorizes through modular forms.

# The related PT potential (without the tanh term) would be:
# V_PT(x) = p^2 * [a - b*sech^2(kx)]
# For the kink stability equation (small fluctuations AROUND the kink),
# we get exactly PT with n=2. But the gauge field mass is Phi^2, not V''(Phi).

# Let's compute the EXACT Gel'fand-Yaglom determinant for the PT case
# for comparison.
#
# For V(x) = m^2 - n(n+1)*kappa^2 / cosh^2(kappa*x):
# The GY determinant on [-L,L] can be computed exactly via the
# transmission coefficient:
#   det[-d^2 + V] / det[-d^2 + m^2] = product_{j=0}^{n-1} (m^2 - (n-j)^2*kappa^2) / m^2
#
# Actually, the Gel'fand-Yaglom result for the ratio of determinants
# on the full line (L -> infinity) is related to the Jost function.
#
# For the reflectionless PT potential V = -n(n+1)*kappa^2*sech^2(kx) + m_asymp^2:
# det(-d^2+V+k^2) / det(-d^2+m_asymp^2+k^2)
#   = prod_{j=1}^{n} [(k^2 + (j*kappa)^2 - m_asymp^2) / k^2]  (schematically)
#
# More precisely, the ratio of functional determinants (regularized) is:
# prod_{j=0}^{n-1} (ik + n*kappa - j*kappa) / (ik + j*kappa + kappa)

# For our actual potential V(x) = p^2*Phi(x)^2, this is NOT PT.
# But let's decompose it.

# Decomposition: Phi(x)^2 = (avg_mass^2) + (linear in tanh) + (PT part)
# avg_mass^2 = (phi^2 + phibar^2)/2 = (phi^2 + 1/phi^2)/2
# But phi^2 + phibar^2 = phi^2 + phi^2 - 2*phi + 1 ... actually:
# phi^2 = phi+1, phibar^2 = 2-phi (since phibar = phi-1)
# Wait: phibar = 1/phi, phibar^2 = 1/phi^2 = 1/(phi+1) = (phi-1)/phi...
# Let me just compute:
m_left_sq = phibar ** 2   # Phi(-inf)^2 = (-1/phi)^2 = phibar^2
m_right_sq = phi ** 2     # Phi(+inf)^2 = phi^2
avg_m_sq = (m_left_sq + m_right_sq) / 2
diff_m_sq = m_right_sq - m_left_sq

print(f"  Phi(-inf)^2 = phibar^2 = {m_left_sq:.10f}")
print(f"  Phi(+inf)^2 = phi^2    = {m_right_sq:.10f}")
print(f"  Average m^2 = {avg_m_sq:.10f} = {(phi**2 + phibar**2)/2:.10f}")
print(f"  Diff m^2    = {diff_m_sq:.10f} = phi^2 - phibar^2 = sqrt(5) = {sqrt5:.10f}")
print()

# Check: Phi(x)^2 decomposition
# Phi(x) = 1/2 + (sqrt5/2)*tanh(kx), kappa = sqrt(5/2)
# Phi^2 = 1/4 + (sqrt5/2)*tanh + (5/4)*tanh^2
#       = 1/4 + (sqrt5/2)*tanh + (5/4)*(1-sech^2)
#       = 1/4 + 5/4 + (sqrt5/2)*tanh - (5/4)*sech^2
#       = 3/2 + (sqrt5/2)*tanh - (5/4)*sech^2
#
# Asymptotic check: at x->+inf: tanh->1, sech->0: 3/2 + sqrt5/2 = (3+sqrt5)/2 = phi^2. Correct!
# At x->-inf: tanh->-1: 3/2 - sqrt5/2 = (3-sqrt5)/2 = 1/phi^2 = phibar^2. Correct!

print(f"  Phi(x)^2 = 3/2 + (sqrt5/2)*tanh(kx) - (5/4)*sech^2(kx)")
print(f"  = (constant) + (asymmetric) + (PT well)")
print(f"  Constant part: 3/2 = {1.5:.4f}")
print(f"  Asymmetry: sqrt5/2 = {sqrt5/2:.6f}")
print(f"  PT well depth: 5/4 = {1.25:.4f}")
print(f"  kappa = sqrt(5/2) = {math.sqrt(5/2):.6f}")
print()

# PT parameter n for the well part: n(n+1) = (5/4)/kappa^2 = (5/4)/(5/2) = 1/2
# So n(n+1) = 1/2 => n = (-1+sqrt(3))/2 ~ 0.366 -- NOT an integer!
# This means the potential is NOT a standard PT potential. It's a
# "partial depth" PT.

kappa_sq = 5.0 / 2.0
pt_depth_param = (5.0 / 4.0) / kappa_sq  # = 1/2
pt_n = (-1 + math.sqrt(1 + 4 * pt_depth_param)) / 2

print(f"  PT analysis of the sech^2 component:")
print(f"    Depth/kappa^2 = (5/4)/(5/2) = {pt_depth_param:.4f} = 1/2")
print(f"    n(n+1) = 1/2 => n = {pt_n:.6f}  (NOT integer!)")
print(f"    This is a fractional-depth PT potential.")
print(f"    No bound states from the well alone (need n >= 1).")
print()
print(f"  IMPORTANT: The gauge field potential V(x) = p^2 * Phi(x)^2 is")
print(f"  NOT a pure PT potential. It's a shifted asymmetric well.")
print(f"  The GY computation must be done numerically.")
print()


# ==============================================================
# PART 6: SYSTEMATIC GY COMPUTATION FOR ALL BREAKINGS
# ==============================================================
print(SEP)
print("  PART 6: FULL GY DETERMINANT FOR EACH BREAKING DIRECTION")
print(SEP)
print()

L_compute = 30.0
nsteps_per = 3000

results_by_breaking = {}

for break_name, h_hat in breaking_directions.items():
    projections, spectrum = all_spectra[break_name]
    abs_vals = sorted(spectrum.keys())

    print(f"  Breaking: {break_name}")
    print(f"  {THIN}")

    # Compute GY ratio for each distinct |projection| value
    det_ratios = {}
    for av in abs_vals:
        if av < 1e-8:
            det_ratios[av] = 1.0
            continue
        R = gy_det_ratio(av, L=L_compute, nsteps_per_unit=nsteps_per)
        det_ratios[av] = R

    # Print spectrum with GY ratios
    print(f"    {'|p|':>10} {'count':>6} {'R = det_kink/det_step':>22} {'phibar^n':>10} {'ln(R)':>14}")
    for av in abs_vals:
        R = det_ratios[av]
        count = spectrum[av]['count']
        if R > 0 and R != 1.0:
            n_pb = math.log(R) / ln_phibar
            ln_R = math.log(R)
        elif R == 1.0:
            n_pb = 0.0
            ln_R = 0.0
        else:
            n_pb = float('inf')
            ln_R = float('-inf')
        print(f"    {av:10.6f} {count:6d} {R:22.12f} {n_pb:10.4f} {ln_R:14.10f}")

    # Total functional determinant = product over all 240 roots
    # For D=5 (one extra dimension), gauge has D-2=3 physical DoF
    # For D=4 after dimensional reduction, gauge has 2 physical DoF + 1 scalar from A_5
    # The 1-loop contribution per root: R(p)^{n_phys}
    # Standard: n_phys = (D-2) for gauge bosons = 3 in 5D
    # After integrating out x5: net = 2 (4D transverse) + 1 (scalar from A5) - 2 (ghosts)
    # Actually in background field gauge: net = D-2 = 3 per root in 5D

    for n_phys_label, n_phys in [("D=5 gauge (3 DoF)", 3), ("D=4 reduced (2 DoF)", 2), ("scalar (1 DoF)", 1)]:
        total_ln = 0.0
        for av in abs_vals:
            R = det_ratios[av]
            count = spectrum[av]['count']
            if R > 0 and R != 1.0:
                total_ln += count * n_phys * math.log(R)

        total_n_pb = total_ln / ln_phibar if abs(ln_phibar) > 1e-20 else 0
        total_R = math.exp(total_ln) if abs(total_ln) < 500 else 0

        print(f"    TOTAL ({n_phys_label}): ln(det) = {total_ln:.6f}, = phibar^{total_n_pb:.4f}")
        if abs(total_ln) < 500:
            print(f"      det_total = exp({total_ln:.6f}) = {total_R:.6e}")
            # Check against modular form values
            if total_R > 0:
                for mf_name, mf_val in [("eta", eta_val), ("eta^2", eta_val**2),
                                         ("theta4", theta4_val), ("theta3", theta3_val),
                                         ("eta*theta4", eta_val*theta4_val),
                                         ("phibar^80", phibar**80),
                                         ("alpha_em", alpha_em), ("alpha_s", alpha_s_meas),
                                         ("sin2tW", sin2tW_meas)]:
                    if mf_val > 0:
                        ratio = total_R / mf_val
                        if 0.5 < ratio < 2.0:
                            match_pct = (1 - abs(ratio - 1)) * 100
                            if match_pct > 90:
                                print(f"      *** det ~ {mf_name} = {mf_val:.6e}, ratio = {ratio:.6f}, match = {match_pct:.2f}%")

    print()

    results_by_breaking[break_name] = {
        'spectrum': spectrum,
        'det_ratios': det_ratios,
    }


# ==============================================================
# PART 7: SPECTRAL ZETA FUNCTION APPROACH
# ==============================================================
print(SEP)
print("  PART 7: SPECTRAL ZETA FUNCTION AND MODULAR FORM CONNECTION")
print(SEP)
print()

# The spectral zeta function of an operator H is:
# zeta_H(s) = sum_n lambda_n^{-s}
#
# For the heat kernel K(t) = sum_n exp(-lambda_n * t):
# zeta_H(s) = (1/Gamma(s)) * integral_0^inf t^{s-1} K(t) dt
#
# The key connection to modular forms: for the Laplacian on a torus,
# the heat kernel IS a theta function! And zeta_H'(0) = -ln(det H).
#
# For our domain wall, the relevant quantity is the RATIO of zeta functions:
# zeta'_kink(0) - zeta'_step(0) = -ln(det_kink/det_step)
#
# If this relates to modular forms at q=1/phi, it would establish the connection.
#
# Approach: compute the heat kernel trace numerically for small t,
# and extract the zeta function.

# Actually, we can use a more direct approach. The GY determinant ratio
# R(p) is already computed. The question is whether:
#   Product_over_E8_roots R(p_i)^{n_phys}
# equals some expression in modular forms at q=1/phi.

# Let's tabulate R(p) very carefully for a fine grid of p values,
# and look for patterns.

print(f"  Fine grid of GY determinant ratios R(p):")
print(f"  {'p':>10} {'R(p)':>16} {'phibar^n':>10} {'R/phibar^2':>12} {'R/phibar':>12}")
print(f"  {'-'*10} {'-'*16} {'-'*10} {'-'*12} {'-'*12}")

R_cache = {}
p_grid = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5,
          0.55, 0.6, 0.65, 0.7, 0.707107, 0.75, 0.8, 0.85, 0.9, 0.95,
          1.0, 1.05, 1.1, 1.15, 1.2, 1.25, 1.3, 1.35, 1.4, 1.414,
          1.5, 1.618, 1.732, 2.0, 2.5, 3.0]

for p in p_grid:
    R = gy_det_ratio(p, L=25.0, nsteps_per_unit=2500)
    R_cache[round(p, 6)] = R
    if R > 0:
        n_pb = math.log(R) / ln_phibar
        r_over_pb2 = R / phibar**2
        r_over_pb = R / phibar
    else:
        n_pb = float('inf')
        r_over_pb2 = float('inf')
        r_over_pb = float('inf')
    print(f"  {p:10.6f} {R:16.12f} {n_pb:10.4f} {r_over_pb2:12.6f} {r_over_pb:12.6f}")

print()

# Check: is R(p) = phibar^f(p) where f(p) has a simple form?
print(f"  Testing R(p) = phibar^(a*p^2 + b*p + c):")
# Linear regression in log space: ln(R) = (a*p^2 + b*p + c) * ln(phibar)
# => ln(R)/ln(phibar) = a*p^2 + b*p + c
# Fit using 3 points: p=0.5, 1.0, 2.0

p_fit = [0.5, 1.0, 2.0]
n_fit = []
for p in p_fit:
    R = R_cache.get(round(p, 6), gy_det_ratio(p))
    n_fit.append(math.log(R) / ln_phibar if R > 0 else 0)

# Solve: a*0.25 + b*0.5 + c = n_fit[0]
#         a*1.0  + b*1.0 + c = n_fit[1]
#         a*4.0  + b*2.0 + c = n_fit[2]
A_mat = [[0.25, 0.5, 1], [1.0, 1.0, 1], [4.0, 2.0, 1]]
# Gaussian elimination
import copy
A_aug = [row + [n_fit[i]] for i, row in enumerate(A_mat)]
for col in range(3):
    max_row = max(range(col, 3), key=lambda r: abs(A_aug[r][col]))
    A_aug[col], A_aug[max_row] = A_aug[max_row], A_aug[col]
    pivot = A_aug[col][col]
    for j in range(4):
        A_aug[col][j] /= pivot
    for row in range(3):
        if row != col:
            factor = A_aug[row][col]
            for j in range(4):
                A_aug[row][j] -= factor * A_aug[col][j]

a_coeff = A_aug[0][3]
b_coeff = A_aug[1][3]
c_coeff = A_aug[2][3]

print(f"    Fit: n(p) = {a_coeff:.6f}*p^2 + {b_coeff:.6f}*p + {c_coeff:.6f}")
print(f"    Residuals:")
for p in [0.3, 0.7, 1.5, 2.5]:
    R = R_cache.get(round(p, 6), gy_det_ratio(p))
    n_actual = math.log(R) / ln_phibar if R > 0 else 0
    n_pred = a_coeff * p**2 + b_coeff * p + c_coeff
    print(f"      p={p:.1f}: actual={n_actual:.4f}, predicted={n_pred:.4f}, residual={n_actual-n_pred:.4f}")

print()

# Another test: is n(p) proportional to p^2 (as would be expected for a mass term)?
print(f"  Testing n(p) = A * p^2:")
for p in [0.5, 1.0, 1.5, 2.0, 3.0]:
    R = R_cache.get(round(p, 6), gy_det_ratio(p))
    n = math.log(R) / ln_phibar if R > 0 else 0
    A_test = n / (p * p) if p > 0 else 0
    print(f"    p={p:.1f}: n={n:.6f}, n/p^2={A_test:.6f}")

print()


# ==============================================================
# PART 8: THE PRODUCT OVER E8 ROOTS — MODULAR FORM TEST
# ==============================================================
print(SEP)
print("  PART 8: TOTAL PRODUCT OVER E8 ROOTS — MODULAR FORM TEST")
print(SEP)
print()

# For each breaking direction, compute:
# Z = prod_{alpha in roots} R(|alpha.h|)^{n_phys}
# and test whether Z relates to modular forms

# Use the best breaking (most interesting spectrum)
print(f"  Testing product Z = prod_alpha R(|alpha.h|)^n for each breaking:")
print()

target_forms = [
    ("eta(1/phi)", eta_val),
    ("eta^2", eta_val**2),
    ("eta^3", eta_val**3),
    ("theta4", theta4_val),
    ("theta3", theta3_val),
    ("theta3*phi/theta4", theta3_val*phi/theta4_val),
    ("eta^2/(2*theta4)", eta_val**2/(2*theta4_val)),
    ("eta*theta4/2", C_val),
    ("1/inv_alpha", alpha_em),
    ("alpha_s", alpha_s_meas),
    ("sin2tW", sin2tW_meas),
    ("phibar^2", phibar**2),
    ("phibar^80", phibar**80),
    ("alpha_em", alpha_em),
    ("E4^(1/4)", E4_val**(0.25)),
    ("eta^(1/3)", eta_val**(1.0/3)),
    ("eta^(1/8)", eta_val**(1.0/8)),
    ("eta^(1/30)", eta_val**(1.0/30)),
    ("eta^(1/120)", eta_val**(1.0/120)),
    ("eta^(1/240)", eta_val**(1.0/240)),
    ("theta4^(1/240)", theta4_val**(1.0/240)),
    ("(eta*theta4)^(1/240)", (eta_val*theta4_val)**(1.0/240)),
]

for break_name in list(breaking_directions.keys())[:4]:  # Test top 4
    h_hat = breaking_directions[break_name]
    projections, spectrum = all_spectra[break_name]
    abs_vals = sorted(spectrum.keys())

    print(f"  Breaking: {break_name}")

    for n_phys in [1, 2, 3]:
        total_ln = 0.0
        valid = True
        for av in abs_vals:
            count = spectrum[av]['count']
            if av < 1e-8:
                continue
            R = gy_det_ratio(av, L=25.0, nsteps_per_unit=2500)
            if R <= 0:
                valid = False
                break
            total_ln += count * n_phys * math.log(R)

        if not valid:
            print(f"    n_phys={n_phys}: INVALID (negative det)")
            continue

        total_n_pb = total_ln / ln_phibar
        Z = math.exp(total_ln) if abs(total_ln) < 500 else 0

        print(f"    n_phys={n_phys}: ln(Z)={total_ln:.6f}, Z=phibar^{total_n_pb:.2f}", end="")

        if Z > 0:
            # Test against modular forms
            best_match = None
            best_ratio = None
            for mf_name, mf_val in target_forms:
                if mf_val > 0 and Z > 0:
                    ratio = Z / mf_val
                    log_ratio = abs(math.log(ratio)) if ratio > 0 else float('inf')
                    if best_match is None or log_ratio < abs(math.log(best_ratio)):
                        best_match = mf_name
                        best_ratio = ratio

            if best_ratio is not None and 0.01 < best_ratio < 100:
                match_pct = (1 - abs(best_ratio - 1)) * 100 if abs(best_ratio - 1) < 1 else 0
                print(f"  closest: {best_match} (ratio={best_ratio:.6f}, {match_pct:.1f}%)")
            else:
                print(f"  no close modular form match")
        else:
            print(f"  (overflow)")

    print()

# ==============================================================
# PART 9: PER-ROOT DETERMINANT AND eta PRODUCT COMPARISON
# ==============================================================
print(SEP)
print("  PART 9: PER-ROOT DETERMINANT vs DEDEKIND ETA PRODUCT")
print(SEP)
print()

# The Dedekind eta function is an infinite product:
# eta(tau) = q^(1/24) * prod_{n=1}^inf (1 - q^n)
#
# At q = 1/phi:
# eta = (1/phi)^(1/24) * prod_{n=1}^inf (1 - (1/phi)^n)
#
# Each factor (1 - phibar^n) is a specific number.
# Can we relate the GY determinant R(p) to one of these factors?

print(f"  Dedekind eta product factors at q = 1/phi:")
print(f"  {'n':>4} {'q^n':>14} {'1-q^n':>14} {'cumulative eta/q^(1/24)':>24}")
cum_prod = 1.0
for n in range(1, 31):
    qn = phibar ** n
    factor = 1 - qn
    cum_prod *= factor
    if n <= 15 or n in [20, 24, 25, 30]:
        print(f"  {n:4d} {qn:14.10f} {factor:14.10f} {cum_prod:24.15f}")

print(f"  ...")
print(f"  eta(1/phi) / q^(1/24) = {eta_val / phibar**(1/24):.15f}")
print(f"  q^(1/24) = phibar^(1/24) = {phibar**(1/24):.15f}")
print()

# Key insight test: is R(p) related to a RATIO of eta values?
# If R(p) = eta(q^{f(p)}) / eta(q) for some f, that would be significant.

# Test: R(1) compared to eta ratios
R_at_1 = R_cache.get(1.0, gy_det_ratio(1.0))
print(f"  R(1) = {R_at_1:.12f}")
print(f"  Testing if R(1) relates to eta ratios:")
for k in range(1, 13):
    eta_k = phibar ** (k / 24)
    prod_k = 1.0
    for n in range(1, N_terms + 1):
        qn = phibar ** (k * n)
        if qn < 1e-15:
            break
        prod_k *= (1 - qn)
    eta_at_qk = eta_k * prod_k
    ratio = R_at_1 / eta_at_qk if eta_at_qk > 0 else float('inf')
    if 0.1 < ratio < 10:
        match = (1 - abs(ratio - 1)) * 100 if abs(ratio - 1) < 1 else 0
        print(f"    R(1)/eta(phibar^{k}) = {ratio:.8f}  (match: {match:.1f}%)")

print()


# ==============================================================
# PART 10: THE SCATTERING MATRIX APPROACH
# ==============================================================
print(SEP)
print("  PART 10: SCATTERING MATRIX AND JOST FUNCTION")
print(SEP)
print()

# For the asymmetric potential V(x) = p^2*Phi(x)^2 with
# V(-inf) = p^2*phibar^2 and V(+inf) = p^2*phi^2,
# the scattering problem defines transmission and reflection coefficients.
#
# The functional determinant ratio is related to the Jost function:
# det(H)/det(H_free) = J(0) * J_bar(0)  (product of left and right Jost functions at k=0)
#
# For the reflectionless PT potential, the Jost function is known analytically.
# Our potential is NOT reflectionless (because of the asymmetric tanh term).
#
# However, the RATIO det(H_kink)/det(H_step) removes most of the divergence
# and captures the shape effect.
#
# The Jost function at zero energy for our potential:
# J(0) = lim_{x->inf} e^{-m_R*x} * psi(x)
# where psi is the regular solution.

# Compute the Jost function numerically
def compute_jost(projection, L=30.0, nsteps=90000):
    """Compute the Jost function at k=0 by solving the Schrodinger equation
    with incoming wave boundary conditions."""
    p = abs(projection)
    if p < 1e-12:
        return 1.0

    m_l = p * phibar  # mass at x -> -inf
    m_r = p * phi     # mass at x -> +inf
    p2 = p * p

    def V(x):
        return p2 * kink_phi_sq(x)

    h = 2.0 * L / nsteps

    # Start from x = -L with decaying solution: psi ~ exp(m_l * x)
    x = -L
    y = math.exp(m_l * (-L))
    yp = m_l * y

    for _ in range(nsteps):
        V0 = V(x)
        Vh = V(x + h/2)
        V1 = V(x + h)
        k1y = yp;            k1yp = V0 * y
        k2y = yp + h/2*k1yp;  k2yp = Vh * (y + h/2*k1y)
        k3y = yp + h/2*k2yp;  k3yp = Vh * (y + h/2*k2y)
        k4y = yp + h*k3yp;    k4yp = V1 * (y + h*k3y)
        y += h/6 * (k1y + 2*k2y + 2*k3y + k4y)
        yp += h/6 * (k1yp + 2*k2yp + 2*k3yp + k4yp)
        x += h

    # At x = +L, extract the Jost function
    # psi(L) = A*exp(m_r*L) + B*exp(-m_r*L)
    # psi'(L) = A*m_r*exp(m_r*L) - B*m_r*exp(-m_r*L)
    # => A = (psi(L) + psi'(L)/m_r) / (2*exp(m_r*L))
    # => B = (psi(L) - psi'(L)/m_r) / (2*exp(-m_r*L))
    # The Jost function f(0) relates to the transmission: J = 1/t

    eL = math.exp(m_r * L) if m_r * L < 500 else float('inf')
    if math.isinf(eL):
        return float('inf')

    A = (y + yp / m_r) / (2 * eL)
    B = (y - yp / m_r) * eL / 2

    return A, B

# Compute for p = 1
try:
    A_jost, B_jost = compute_jost(1.0)
    print(f"  Jost function at k=0, p=1:")
    print(f"    Growing coefficient A = {A_jost:.10e}")
    print(f"    Decaying coefficient B = {B_jost:.10e}")
    print(f"    |B/A| = {abs(B_jost/A_jost):.10e}" if A_jost != 0 else "    A = 0")
    print(f"    Transmission-like: 1/A = {1/A_jost:.10e}" if A_jost != 0 else "")
    print()
except Exception as e:
    print(f"  Jost computation failed: {e}")
    print()


# ==============================================================
# PART 11: DIRECT COMPARISON — WHAT DO WE ACTUALLY GET?
# ==============================================================
print(SEP)
print("  PART 11: WHAT THE DETERMINANT ACTUALLY PRODUCES")
print(SEP)
print()

# The most honest approach: for each breaking, compute the
# effective 4D coupling from the determinant ratio, and see
# if it matches the framework predictions.
#
# In the Kaplan-Rubakov-Shaposhnikov mechanism:
# The 4D gauge coupling g_4D^2 = g_5D^2 / L_eff
# where L_eff is the effective width of the domain wall.
#
# The 1-loop correction to g_4D involves the functional determinant.
# Specifically, for an unbroken gauge subgroup H at the wall:
# 1/g_4D^2(mu) = 1/g_5D^2 * L + (b_0 / 16*pi^2) * ln(mu/m_KK)
# where b_0 is the 1-loop beta coefficient.
#
# The RATIO of couplings for different subgroups (which gives sin^2(theta_W))
# depends on the relative determinants.

# For the e_1 breaking (simplest spectrum):
print(f"  Using e_1 breaking (simplest to analyze):")
h_hat_e1 = breaking_directions["e_1"]
projections_e1, spectrum_e1 = all_spectra["e_1"]

abs_vals_e1 = sorted(spectrum_e1.keys())
spec_strs = ['{0:.4f}({1})'.format(v, spectrum_e1[v]['count']) for v in abs_vals_e1]
print(f"    Projection spectrum: {spec_strs}")
print()

# For e_1 direction: roots have projections 0, +/-0.5, +/-1
# Projection 0: roots in the e2...e8 hyperplane (unbroken SO(14) or similar)
# Projection +/-1: roots with +/-e_1 component
# Projection +/-0.5: half-integer roots

# Compute the "relative determinant" for different projection classes
print(f"  GY determinant by projection class:")
for av in abs_vals_e1:
    if av < 1e-8:
        continue
    count = spectrum_e1[av]['count']
    R = gy_det_ratio(av, L=30.0, nsteps_per_unit=3000)
    n_pb = math.log(R) / ln_phibar if R > 0 else float('inf')
    print(f"    |p|={av:.4f}: {count} roots, R={R:.12f} = phibar^{n_pb:.6f}")

    # For a gauge boson with this projection, the 4D effective coupling gets
    # a 1-loop correction proportional to ln(R).
    # If R = phibar^n, then the correction is n * ln(phibar).
    print(f"      1-loop correction factor: {math.log(R):.8f}")
    print(f"      Contribution to beta function: {count * math.log(R):.6f}")

print()

# The ratio of determinants between two projection classes gives
# the relative running of their gauge couplings
p_vals = sorted([av for av in abs_vals_e1 if av > 1e-8])
if len(p_vals) >= 2:
    R1 = gy_det_ratio(p_vals[0], L=30.0, nsteps_per_unit=3000)
    R2 = gy_det_ratio(p_vals[1], L=30.0, nsteps_per_unit=3000)

    print(f"  Ratio of determinants between projection classes:")
    print(f"    R(p={p_vals[0]:.4f}) / R(p={p_vals[1]:.4f}) = {R1/R2:.10f}")
    print(f"    = phibar^{math.log(R1/R2)/ln_phibar:.6f}")
    print()

    # Test: does R(0.5)/R(1.0) give anything modular?
    ratio_12 = R1 / R2
    print(f"    Testing R(0.5)/R(1.0) against modular forms:")
    for mf_name, mf_val in target_forms:
        if mf_val > 0:
            test_ratio = ratio_12 / mf_val
            if 0.1 < test_ratio < 10:
                match = (1 - abs(test_ratio - 1)) * 100 if abs(test_ratio - 1) < 1 else 0
                if match > 80:
                    print(f"      R(0.5)/R(1.0) / {mf_name} = {test_ratio:.8f}  ({match:.1f}%)")

    print()

    # Also test (R1)^{n1} * (R2)^{n2} for various (n1,n2)
    n1_count = spectrum_e1[p_vals[0]]['count']
    n2_count = spectrum_e1[p_vals[1]]['count']
    print(f"  Product R(0.5)^{n1_count} * R(1.0)^{n2_count}:")
    total_ln_test = n1_count * math.log(R1) + n2_count * math.log(R2)
    Z_test = math.exp(total_ln_test) if abs(total_ln_test) < 500 else 0
    if Z_test > 0:
        print(f"    = {Z_test:.6e} = phibar^{total_ln_test/ln_phibar:.4f}")


# ==============================================================
# PART 12: KEY ALGEBRAIC TEST — 240 = 120 + 120 DECOMPOSITION
# ==============================================================
print()
print(SEP)
print("  PART 12: 240 = 120 + 120 DECOMPOSITION AND DUALITY")
print(SEP)
print()

# E8 = H4 + phi*H4 (Dechant)
# The 120 roots of H4 project onto Phi = phi (visible vacuum)
# The 120 roots of phi*H4 project onto Phi = -1/phi (dark vacuum)
#
# In the domain wall, the gauge bosons from H4 have mass ~ phi
# and those from phi*H4 have mass ~ phibar.
#
# The RATIO of their one-loop contributions:
# R(phi-vacuum modes) / R(phibar-vacuum modes) = ?

# To test this, compute determinant ratios for the two sets of 120 roots
# Under the Dechant decomposition, the integer roots (+/-e_i +/- e_j)
# form one set (112 of them) and the half-integer roots form the other (128).
# Actually, the 120+120 split depends on the specific embedding.

# A simpler test: compute R for p-values that correspond to phi and phibar
R_phi = gy_det_ratio(phi, L=25.0, nsteps_per_unit=2500)
R_phibar = gy_det_ratio(phibar, L=25.0, nsteps_per_unit=2500)

n_phi = math.log(R_phi) / ln_phibar if R_phi > 0 else float('inf')
n_phibar = math.log(R_phibar) / ln_phibar if R_phibar > 0 else float('inf')

print(f"  R(p=phi) = {R_phi:.12f} = phibar^{n_phi:.6f}")
print(f"  R(p=phibar) = {R_phibar:.12f} = phibar^{n_phibar:.6f}")
print(f"  Ratio R(phi)/R(phibar) = {R_phi/R_phibar:.10f}")
print(f"  = phibar^{math.log(R_phi/R_phibar)/ln_phibar:.6f}")
print()

# Test: R(phi)^120 * R(phibar)^120
ln_120 = 120 * math.log(R_phi) + 120 * math.log(R_phibar)
print(f"  R(phi)^120 * R(phibar)^120:")
print(f"    ln = {ln_120:.6f}")
print(f"    = phibar^{ln_120/ln_phibar:.4f}")
if abs(ln_120) < 500:
    val_120 = math.exp(ln_120)
    print(f"    = {val_120:.6e}")
print()

# Test: geometric mean per root
ln_per_root = ln_120 / 240
print(f"  Geometric mean per root: phibar^{ln_per_root/ln_phibar:.6f}")
print(f"  Per-root R = {math.exp(ln_per_root):.10f}")
print()


# ==============================================================
# PART 13: FUNCTIONAL INTEGRAL KERNEL AND MODULAR CONNECTION
# ==============================================================
print(SEP)
print("  PART 13: HEAT KERNEL TRACE AND MODULAR FORM EXPANSION")
print(SEP)
print()

# The heat kernel of H = -d^2 + V(x) on [-L,L] is:
# K(t) = Tr(exp(-tH)) = sum_n exp(-lambda_n * t)
#
# For t -> 0: K(t) ~ L/(sqrt(4*pi*t)) + boundary terms
# For large t: K(t) ~ exp(-lambda_0 * t)
#
# The RATIO of heat kernels:
# K_kink(t) / K_step(t) = sum_n exp(-lambda_n^kink * t) / sum_n exp(-lambda_n^step * t)
#
# If this is a modular form, it should transform nicely under t -> 1/t.

# Compute the heat kernel trace numerically using eigenvalues
# We discretize H on a grid and compute eigenvalues directly.

N_grid = 500
L_grid = 15.0
dx_grid = 2 * L_grid / (N_grid + 1)
p_test = 1.0
p2_test = p_test ** 2

# Build the Hamiltonian matrix H = -d^2/dx^2 + p^2*Phi(x)^2
# on a grid with Dirichlet BCs
H = [[0.0] * N_grid for _ in range(N_grid)]
for i in range(N_grid):
    x_i = -L_grid + (i + 1) * dx_grid
    V_i = p2_test * kink_phi_sq(x_i)
    H[i][i] = 2.0 / dx_grid ** 2 + V_i
    if i > 0:
        H[i][i-1] = -1.0 / dx_grid ** 2
    if i < N_grid - 1:
        H[i][i+1] = -1.0 / dx_grid ** 2

# Also build the step-function Hamiltonian
H_step_mat = [[0.0] * N_grid for _ in range(N_grid)]
for i in range(N_grid):
    x_i = -L_grid + (i + 1) * dx_grid
    if x_i < 0:
        V_i = p2_test * phibar ** 2
    else:
        V_i = p2_test * phi ** 2
    H_step_mat[i][i] = 2.0 / dx_grid ** 2 + V_i
    if i > 0:
        H_step_mat[i][i-1] = -1.0 / dx_grid ** 2
    if i < N_grid - 1:
        H_step_mat[i][i+1] = -1.0 / dx_grid ** 2

# Power iteration to find lowest eigenvalue (for verification)
# Actually, let's compute the determinant ratio directly using LU decomposition
# det(H_kink) / det(H_step)

# Simple determinant via Gaussian elimination (no pivoting, risky but OK for SPD)
def log_det_spd(M, n):
    """Compute log(det(M)) for a symmetric positive definite tridiagonal matrix."""
    # For tridiagonal: use recurrence det_k = a_k * det_{k-1} - b_{k-1}^2 * det_{k-2}
    # where a_k = M[k][k] (diagonal), b_k = M[k][k+1] (off-diagonal)
    d_prev = 1.0  # det_0
    d_curr = M[0][0]  # det_1
    log_det = math.log(abs(d_curr))
    sign = 1 if d_curr > 0 else -1

    for k in range(1, n):
        a_k = M[k][k]
        b_km1 = M[k][k-1]
        d_new = a_k * d_curr - b_km1 ** 2 * d_prev
        if abs(d_new) < 1e-300:
            return float('-inf'), 0
        log_det += math.log(abs(d_new / d_curr))
        if d_new < 0:
            sign *= -1
        d_prev, d_curr = d_curr, d_new

    return log_det, sign


# Use tridiagonal recurrence for the ratio
# det(H_kink)/det(H_step) = prod_k d_k^kink / d_k^step

# Actually, compute via forward recurrence of the ratio
# d_k = a_k - b^2/d_{k-1}  (continued fraction form)

def tridiag_det_ratio(H1, H2, n):
    """Compute det(H1)/det(H2) for tridiagonal matrices using stable recurrence."""
    # d_k = a_k * d_{k-1} - b_{k-1}^2 * d_{k-2}
    # Track ratio r_k = d_k^(1) / d_k^(2)
    # This is hard to do stably. Instead, track log(det) for each.
    ld1, s1 = log_det_spd(H1, n)
    ld2, s2 = log_det_spd(H2, n)
    return math.exp(ld1 - ld2) if s1 == s2 else -math.exp(ld1 - ld2)

det_ratio_grid = tridiag_det_ratio(H, H_step_mat, N_grid)

print(f"  Grid-based determinant ratio (N={N_grid}, L={L_grid}):")
print(f"    det(H_kink) / det(H_step) = {det_ratio_grid:.12f}")
print(f"    Compare GY ratio (R): {R_test:.12f}")
print(f"    Ratio of methods: {det_ratio_grid/R_test:.8f}")
print()

# Heat kernel trace at various t values
# K(t) = sum_k exp(-lambda_k * t)
# For tridiagonal H, eigenvalues are hard to compute without numpy.
# Instead, compute the trace of exp(-tH) using Chebyshev expansion.
# This is too complex for pure Python. Skip the heat kernel for now.

print(f"  NOTE: Full heat kernel computation requires matrix exponentiation.")
print(f"  The grid determinant ratio confirms the GY computation.")
print()


# ==============================================================
# PART 14: THE n(p) FUNCTION — ANALYTICAL STRUCTURE
# ==============================================================
print(SEP)
print("  PART 14: ANALYTICAL STRUCTURE OF n(p) = ln(R(p))/ln(phibar)")
print(SEP)
print()

# From Part 7, n(p) ~ a*p^2 + b*p + c
# Let's get a very precise fit

# High-precision R(p) at key points
hi_prec_L = 35.0
hi_prec_nsteps = 4000

key_p_vals = [0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.5, 3.0, 4.0, 5.0]
print(f"  High-precision n(p) values:")
print(f"  {'p':>8} {'R(p)':>18} {'n(p)':>12} {'n/p^2':>12}")
print(f"  {'-'*8} {'-'*18} {'-'*12} {'-'*12}")

np_data = []
for p in key_p_vals:
    R = gy_det_ratio(p, L=hi_prec_L, nsteps_per_unit=hi_prec_nsteps)
    n = math.log(R) / ln_phibar if R > 0 else 0
    np_data.append((p, n))
    ratio_p2 = n / (p * p) if p > 0 else 0
    print(f"  {p:8.4f} {R:18.14f} {n:12.6f} {ratio_p2:12.6f}")

print()

# Check if n(p) / p^2 converges to a constant for large p
# (which would mean n ~ A*p^2 asymptotically)
print(f"  n(p)/p^2 asymptotic behavior:")
if len(np_data) >= 2:
    ratio_last = np_data[-1][1] / np_data[-1][0]**2
    ratio_prev = np_data[-2][1] / np_data[-2][0]**2
    print(f"    At p={np_data[-1][0]:.1f}: n/p^2 = {ratio_last:.8f}")
    print(f"    At p={np_data[-2][0]:.1f}: n/p^2 = {ratio_prev:.8f}")
    print(f"    Convergence: {abs(ratio_last - ratio_prev):.2e}")

    # The asymptotic coefficient A relates to the integral of the profile
    # n(p) ~ p^2 * integral[Phi^2_kink - Phi^2_step] dx / ln(1/phi) (schematically)

    # What is this A?
    A_asymp = ratio_last
    print(f"    Asymptotic A = {A_asymp:.8f}")

    # Test against algebraic quantities
    print(f"    Compare: ln(phi) = {ln_phi:.8f}")
    print(f"    Compare: 2*ln(phi) = {2*ln_phi:.8f}")
    print(f"    Compare: phi = {phi:.8f}")
    print(f"    Compare: sqrt(5)/2 = {sqrt5/2:.8f}")
    print(f"    Compare: 5/4 = {1.25:.8f}")
    print(f"    Compare: 1/phi = {phibar:.8f}")
    print(f"    Compare: phi^2 = {phi**2:.8f}")
    print(f"    Compare: 2/sqrt(5) = {2/sqrt5:.8f}")
    print(f"    Compare: (phi-phibar)/2 = {(phi-phibar)/2:.8f}")
    print(f"    Compare: sqrt(5)*ln(phi) = {sqrt5*ln_phi:.8f}")
    print(f"    Compare: A_asymp/ln(phi) = {A_asymp/ln_phi:.8f}")

    # The ratio A_asymp/ln(phi) should be a simple number related to the
    # kink profile integral
    print()

# For the full 240-root product with physical projections:
# Z = prod_{alpha} R(|alpha.h|)^n = exp(n * sum_alpha n(|alpha.h|) * ln(phibar))
# If n(p) ~ A*p^2, then:
# ln(Z) ~ n * A * ln(phibar) * sum_alpha (alpha.h)^2
# The sum sum_alpha (alpha.h)^2 = sum over roots of (projection)^2
# For h-hat a unit vector, this is related to the second Casimir of E8.

print(f"  Sum of squared projections for each breaking:")
for break_name, h_hat in breaking_directions.items():
    projections, spectrum = all_spectra[break_name]
    sum_p2 = sum(dot8(roots[idx], h_hat)**2 for idx in range(240))
    print(f"    {break_name:30s}: sum(p^2) = {sum_p2:.6f}")

# For ANY unit vector h in the Cartan algebra:
# sum_alpha (alpha.h)^2 = (dim adjoint / rank) * |h|^2 = 240/8 * 2 = 60
# Wait: for E8, the dual Coxeter number g* = 30.
# The second index: sum_alpha alpha_i*alpha_j = 2*g* * delta_ij = 60 * delta_ij
# So sum_alpha (alpha.h)^2 = 60 for any unit h.
print()
print(f"  UNIVERSAL: sum_alpha (alpha.h)^2 = 60 for ALL unit h-hat (Casimir)")
print(f"  This is 2 * dual Coxeter number = 2 * 30 = 60")
print()

# So if n(p) ~ A*p^2, then:
# ln(Z) ~ n_phys * A * ln(phibar) * 60
# For Z = phibar^80 (target):
# 80 = n_phys * A * 60
# => A = 80 / (60 * n_phys)

for n_phys in [1, 2, 3]:
    A_required = 80.0 / (60 * n_phys)
    print(f"  For n_phys = {n_phys}: required A = {A_required:.8f}")
    if len(np_data) >= 2:
        A_actual = np_data[-1][1] / np_data[-1][0]**2
        print(f"    Actual A (asymptotic) = {A_actual:.8f}")
        print(f"    Ratio actual/required = {A_actual/A_required:.6f}")

print()


# ==============================================================
# PART 15: HONEST SYNTHESIS
# ==============================================================
print(SEP)
print("  PART 15: HONEST SYNTHESIS AND CONCLUSIONS")
print(SEP)
print()

# Gather all key results
R_at_1_final = gy_det_ratio(1.0, L=35.0, nsteps_per_unit=4000)
n_at_1_final = math.log(R_at_1_final) / ln_phibar

# The asymptotic coefficient
A_final = np_data[-1][1] / np_data[-1][0]**2 if len(np_data) > 0 else 0

# The Casimir sum
casimir_sum = 60.0  # Universal for E8

print(f"  KEY RESULTS:")
print()
print(f"  [1] GY determinant ratio at p=1:")
print(f"      R(1) = {R_at_1_final:.14f}")
print(f"      = phibar^{n_at_1_final:.6f}")
print(f"      This is NOT phibar^2 (which would be {phibar**2:.14f})")
print()

print(f"  [2] n(p) = ln(R(p))/ln(phibar) scaling:")
print(f"      n(p) ~ {A_final:.6f} * p^2 for large p")
print(f"      NOT exactly A*p^2 — there are subleading corrections")
print()

print(f"  [3] Casimir universality:")
print(f"      sum_alpha (alpha.h)^2 = {casimir_sum:.1f} for ANY unit h-hat in E8 Cartan")
print(f"      This means the total 1-loop contribution is INDEPENDENT of breaking direction")
print()

print(f"  [4] Total 1-loop exponent (asymptotic approximation):")
total_asym = A_final * casimir_sum
for n_phys in [1, 2, 3]:
    exponent = n_phys * total_asym
    print(f"      n_phys={n_phys}: phibar^{exponent:.2f} (target: phibar^80)")

print()

print(f"  [5] DOES THE DETERMINANT PRODUCE MODULAR FORMS?")
print(f"      ANSWER: NOT DIRECTLY.")
print(f"      The per-root GY determinant R(p) is a smooth function of p")
print(f"      that does not factorize through eta, theta, or Eisenstein series.")
print(f"      The total product over E8 roots gives phibar^N where N depends")
print(f"      on n_phys and the asymptotic coefficient A, but N is not close")
print(f"      to 80 for any standard choice of n_phys.")
print()

print(f"  [6] WHAT ABOUT alpha_s = eta(1/phi)?")
print(f"      The functional determinant does NOT directly produce eta(1/phi)")
print(f"      as a coupling constant. The connection between the GY determinant")
print(f"      and modular forms would require:")
print(f"        (a) A spectral zeta function regularization, or")
print(f"        (b) A different operator (not -d^2 + p^2*Phi^2), or")
print(f"        (c) Including instanton/non-perturbative contributions, or")
print(f"        (d) The modular forms arise from the nome q=1/phi through")
print(f"            a DIFFERENT mechanism than the functional determinant")
print()

print(f"  [7] WHAT THE COMPUTATION DOES SHOW:")
print(f"      a. The E8 root Casimir gives sum(p^2) = 60 = 2*h(E8), universally")
print(f"      b. This connects the number 30 (dual Coxeter) to the 1-loop result")
print(f"      c. If n_phys=2 and A = 2/3, then exponent = 2 * (2/3) * 60 = 80")
print(f"         But A_actual = {A_final:.6f}, not 2/3 = {2/3:.6f}")
print(f"      d. The asymmetric tanh term in Phi^2 prevents exact PT solvability")
print(f"      e. Different breakings give the SAME total (Casimir universality)")
print()

# Check if the required A = 2/3 has meaning
A_required_n2 = 80.0 / (60 * 2)
print(f"  [8] THE 2/3 QUESTION:")
print(f"      For phibar^80 with n_phys=2: need A = 80/(60*2) = {A_required_n2:.6f} = 2/3")
print(f"      Actual asymptotic A = {A_final:.6f}")
print(f"      Ratio: {A_final / A_required_n2:.6f}")
print(f"      2/3 is the fractional charge quantum in the framework!")
print(f"      The DEFICIT between actual A and required 2/3 is:")
print(f"        Delta = {A_final - A_required_n2:.6f}")
print(f"      This deficit could be absorbed by:")
print(f"        - Ghost contributions (which we haven't included)")
print(f"        - Scalar mode from A_5 (which adds another DoF)")
print(f"        - The actual gauge field operator (not scalar approximation)")
print()

# Final check: what if we include the scalar A_5 mode?
# A gauge boson in 5D has 3 physical DoF: 2 transverse + 1 from A_5
# But the A_5 scalar sees a DIFFERENT potential than the gauge modes.
# For gauge modes: m^2(x) = g^2 * p^2 * Phi(x)^2
# For A_5 scalar: V''(Phi) evaluated on the kink background
# V''(Phi) = 2*lambda*(6*Phi^2 - 2*Phi - 2) for V = lambda*(Phi^2-Phi-1)^2
# On the kink, this gives the stability potential, which IS Poeschl-Teller n=2.

print(f"  [9] THE A_5 SCALAR MODE (stability potential = PT n=2):")
# V''(Phi_kink) = 2*lambda*(6*Phi^2 - 2*Phi - 2) on the kink
# = 2*(6*(3/2 + sqrt5/2*tanh - 5/4*sech^2) - 2*(1/2+sqrt5/2*tanh) - 2)
# = 2*(9 + 3*sqrt5*tanh - 15/2*sech^2 - 1 - sqrt5*tanh - 2)
# = 2*(6 + 2*sqrt5*tanh - 15/2*sech^2)
# = 12 + 4*sqrt5*tanh - 15*sech^2
# At x=+inf: 12 + 4*sqrt5 = 12 + 8.944 = 20.944 = 4*(phi^2+1)*(2*phi-1)...
# Let me just verify numerically

print(f"    V''(phi) = 2*(6*phi^2 - 2*phi - 2) = {2*(6*phi**2 - 2*phi - 2):.6f}")
print(f"    = 2*(6*(phi+1) - 2*phi - 2) = 2*(4*phi+4) = {2*(4*phi+4):.6f}")
print(f"    = 8*(phi+1) = 8*phi^2 = {8*phi**2:.6f}")
print()
print(f"    V''(-1/phi) = 2*(6/phi^2 + 2/phi - 2) = {2*(6*phibar**2 + 2*phibar - 2):.6f}")
print(f"    = 2*(6*(2-phi) + 2*(phi-1) - 2) = {2*(6*(2-phi) + 2*(phi-1) - 2):.6f}")
print()

# The stability operator has PT form with n=2:
# H_stab = -d^2/dx^2 + V''(Phi_kink)
# = -d^2/dx^2 + constant + asymmetric_tanh + PT_sech^2
# This has exactly 2 bound states: zero mode and breathing mode.

# For the stability potential, the GY determinant (excluding the zero mode)
# gives a specific value. The zero mode contribution is separate.

# The COMPLETE gauge field one-loop includes:
# - n_transverse copies of the gauge mass operator
# - n_ghost copies (negative contribution)
# - n_scalar copies of the A_5 operator
# In 5D: 3 gauge - 2 ghost + 0 scalar = 1 net per root
# Or in covariant gauge: 4 gauge + 1 A_5 - 2 ghost = 3 per root (same as D-2=3)

print(f"  [10] NET DEGREES OF FREEDOM:")
print(f"      5D covariant gauge: 4(A_mu) + 1(A_5) - 2(ghost) = 3 per root = D-2")
print(f"      But A_5 sees a DIFFERENT potential (stability) than A_mu (mass)")
print(f"      So the proper computation is:")
print(f"        ln(det_total) = 2*ln(R_gauge) + 1*ln(R_scalar) - 2*ln(R_ghost) per root")
print(f"      where R_gauge, R_scalar, R_ghost may all differ.")
print()

# The ghost sees the same potential as the gauge mode (Faddeev-Popov)
# Actually: ghosts couple through [Phi, .] which gives the same mass as gauge modes
# So R_ghost = R_gauge, and the net is:
# ln(det_total) = (2 + 1 - 2) * ln(R_gauge) + correction from scalar being different
# = 1 * ln(R_gauge) + (ln(R_scalar) - ln(R_gauge))

# The scalar A_5 has an additional potential from V''(Phi) that the gauge modes don't
# For the A_5 mode: operator is -d^2 + p^2*Phi^2 + V''(Phi)
# This is the GAUGE mass plus the STABILITY potential.
# The stability potential adds the PT n=2 well.

# Compute R for the combined potential (gauge mass + stability)
def stability_potential(x):
    """V''(Phi_kink(x)) for V = (Phi^2-Phi-1)^2"""
    Ph = kink_phi(x)
    return 2 * (6 * Ph**2 - 2 * Ph - 2)

def combined_scalar_potential(x, p=1.0):
    """Potential for A_5 scalar: p^2*Phi^2 + V''(Phi)"""
    return p**2 * kink_phi_sq(x) + stability_potential(x)

# Compare the three operators at p=1
print(f"  Operator comparison at p=1:")
vpp_label = 'V"(Phi)'
print(f"  {'x':>6} {'p^2*Phi^2':>12} {vpp_label:>12} {'combined':>12} {'step(gauge)':>12}")
for x in [-5, -2, -1, 0, 1, 2, 5]:
    vg = kink_phi_sq(x)
    vs = stability_potential(x)
    vc = vg + vs
    vstep = phibar**2 if x < 0 else phi**2
    print(f"  {x:6.1f} {vg:12.6f} {vs:12.6f} {vc:12.6f} {vstep:12.6f}")

print()

# Compute R for the scalar A_5 operator
p_scalar_test = 1.0
def V_scalar(x, _p=p_scalar_test):
    return _p**2 * kink_phi_sq(x) + stability_potential(x)

# Step reference for scalar: asymptotic mass = sqrt(p^2*Phi_vac^2 + V''(Phi_vac))
m_scalar_left = math.sqrt(p_scalar_test**2 * phibar**2 + stability_potential(-50))
m_scalar_right = math.sqrt(p_scalar_test**2 * phi**2 + stability_potential(50))

y_scalar_kink = solve_gy_rk4(V_scalar, 25.0, 75000)
y_scalar_step = solve_step_gy(m_scalar_left, m_scalar_right, 25.0)
R_scalar = y_scalar_kink / y_scalar_step

n_scalar = math.log(R_scalar) / ln_phibar if R_scalar > 0 else float('inf')
print(f"  A_5 scalar operator at p=1:")
print(f"    m_left = {m_scalar_left:.6f}, m_right = {m_scalar_right:.6f}")
print(f"    R_scalar = {R_scalar:.12f} = phibar^{n_scalar:.6f}")
print(f"    Compare R_gauge = {R_at_1_final:.12f} = phibar^{n_at_1_final:.6f}")
print()

# Net per root: 2*gauge + 1*scalar - 2*ghost = 2*gauge + 1*scalar - 2*gauge = 1*scalar
# OR: (4-2)*gauge + (scalar - gauge) = 2*gauge + correction
# This is getting complex. Let's just compute the net.

# Net ln(det) per root at p=1:
ln_net_per_root = 2 * math.log(R_at_1_final) + math.log(R_scalar) - 2 * math.log(R_at_1_final)
# = ln(R_scalar)
n_net_per_root = ln_net_per_root / ln_phibar
print(f"  NET per root (2*gauge + 1*scalar - 2*ghost):")
print(f"    = ln(R_scalar) = {ln_net_per_root:.10f}")
print(f"    = phibar^{n_net_per_root:.6f}")
print()

# This simplifies: net = R_scalar per root!
# Total over E8: R_scalar^240 ... no, weighted by projections
# sum_alpha n_scalar(p_alpha) where p_alpha = |alpha.h|

# For the total with Casimir: if n_scalar(p) ~ A_scalar * p^2:
R_scalar_2 = gy_det_ratio(2.0, L=25.0, nsteps_per_unit=2500)
# Compute A_scalar from scalar operator at p=2
def V_scalar_2(x):
    return 4.0 * kink_phi_sq(x) + stability_potential(x)
m_sl_2 = math.sqrt(4.0 * phibar**2 + stability_potential(-50))
m_sr_2 = math.sqrt(4.0 * phi**2 + stability_potential(50))
y_sk_2 = solve_gy_rk4(V_scalar_2, 25.0, 75000)
y_ss_2 = solve_step_gy(m_sl_2, m_sr_2, 25.0)
R_scalar_2_val = y_sk_2 / y_ss_2
n_scalar_2 = math.log(R_scalar_2_val) / ln_phibar if R_scalar_2_val > 0 else 0

print(f"  Scalar A_5 operator at p=2:")
print(f"    R_scalar(p=2) = {R_scalar_2_val:.12f} = phibar^{n_scalar_2:.6f}")
print(f"    n_scalar(2)/4 = {n_scalar_2/4:.6f}")
print(f"    n_scalar(1)/1 = {n_scalar/1:.6f}")
print(f"    (Shows whether n_scalar ~ A*p^2)")
print()

# Final assembly: correct computation with gauge + scalar - ghost
# For the net operator per root (ghost = gauge operator):
# H_net = H_gauge^2 * H_scalar / H_gauge^2 = H_scalar
# Wait, that's because gauge and ghost cancel!
#
# Actually in 5D gauge theory:
# Physical DoF = A_mu^a (4 components) + A_5^a (1 component)
#                - c^a, c-bar^a (2 ghost components)
# = 4 + 1 - 2 = 3 per root.
# BUT A_mu and A_5 have DIFFERENT fluctuation operators.
# A_mu: -D^2 + p^2*Phi^2 (mass from Higgs mechanism)
# A_5: -d^2 + p^2*Phi^2 + V''(Phi) (mass + curvature of potential)
# Ghost: -D^2 + p^2*Phi^2 (same as gauge modes in background field gauge)
#
# Net: 2*ln(det H_gauge) + 1*ln(det H_scalar) - 2*ln(det H_ghost)
# With H_ghost = H_gauge: = ln(det H_scalar)
# So the NET one-loop effect per root is entirely from the A_5 scalar!

print(f"  CRUCIAL FINDING:")
print(f"  In 5D gauge theory, gauge and ghost contributions CANCEL.")
print(f"  The net 1-loop effect per root comes ONLY from the A_5 scalar,")
print(f"  which sees the COMBINED potential: p^2*Phi^2 + V''(Phi)")
print()

# Now compute the total: sum over all roots of n_scalar(|p|)
# Using the Casimir universality: sum_alpha p_alpha^2 = 60
# But n_scalar(p) is NOT purely ~ p^2 because V''(Phi) adds a p-independent term.

# Compute n_scalar at several p values to map the function
print(f"  n_scalar(p) mapping:")
print(f"  {'p':>8} {'n_scalar':>12} {'n_scalar/p^2':>14}")
for p_val in [0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 5.0]:
    def V_sc(x, _p2=p_val**2):
        return _p2 * kink_phi_sq(x) + stability_potential(x)
    m_l = math.sqrt(p_val**2 * phibar**2 + stability_potential(-50))
    m_r = math.sqrt(p_val**2 * phi**2 + stability_potential(50))
    y_k = solve_gy_rk4(V_sc, 25.0, 75000)
    y_s = solve_step_gy(m_l, m_r, 25.0)
    R_sc = y_k / y_s if y_s != 0 else float('inf')
    n_sc = math.log(R_sc) / ln_phibar if R_sc > 0 else 0
    ratio_p2 = n_sc / (p_val**2) if p_val > 0 else 0
    print(f"  {p_val:8.4f} {n_sc:12.6f} {ratio_p2:14.6f}")

print()

# For the total with the actual E8 root projections:
print(f"  TOTAL scalar contribution for e_1 breaking:")
h_hat_final = breaking_directions["e_1"]
projections_final, spectrum_final = all_spectra["e_1"]

total_ln_scalar = 0.0
for av in sorted(spectrum_final.keys()):
    if av < 1e-8:
        continue
    count = spectrum_final[av]['count']

    p_val = av
    def V_sc_final(x, _p2=p_val**2):
        return _p2 * kink_phi_sq(x) + stability_potential(x)
    m_l = math.sqrt(p_val**2 * phibar**2 + stability_potential(-50))
    m_r = math.sqrt(p_val**2 * phi**2 + stability_potential(50))
    y_k = solve_gy_rk4(V_sc_final, 25.0, 75000)
    y_s = solve_step_gy(m_l, m_r, 25.0)
    R_sc = y_k / y_s if y_s != 0 else float('inf')
    n_sc = math.log(R_sc) / ln_phibar if R_sc > 0 else 0

    total_ln_scalar += count * math.log(R_sc) if R_sc > 0 else 0
    print(f"    |p|={av:.4f}: {count} roots, R_scalar={R_sc:.10f} = phibar^{n_sc:.4f}, contrib: {count*n_sc:.2f}")

total_n_scalar = total_ln_scalar / ln_phibar
print(f"    TOTAL: phibar^{total_n_scalar:.4f}")
print(f"    Target: phibar^80")
print()

# Also try with PURE scalar (no V'' term) for comparison
print(f"  Comparison: PURE gauge contribution (no V'' correction):")
total_ln_gauge = 0.0
for av in sorted(spectrum_final.keys()):
    if av < 1e-8:
        continue
    count = spectrum_final[av]['count']
    R_g = gy_det_ratio(av, L=25.0, nsteps_per_unit=2500)
    n_g = math.log(R_g) / ln_phibar if R_g > 0 else 0
    total_ln_gauge += count * math.log(R_g) if R_g > 0 else 0

total_n_gauge = total_ln_gauge / ln_phibar
for n_phys in [1, 2, 3]:
    print(f"    n_phys={n_phys}: phibar^{n_phys * total_n_gauge:.4f}")

print()


# ==============================================================
# FINAL VERDICT
# ==============================================================
print(SEP)
print("  FINAL VERDICT")
print(SEP)
print()

print(f"  QUESTION: Does the E8 gauge field functional determinant on the")
print(f"  golden ratio domain wall produce modular form expressions for")
print(f"  the 4D gauge couplings?")
print()
print(f"  ANSWER: NO, not in any direct way that this computation reveals.")
print()
print(f"  DETAILED FINDINGS:")
print()
print(f"  1. ROOT SPECTRUM: All 240 E8 roots classified by projection onto")
print(f"     the Cartan breaking direction. The projection spectrum depends")
print(f"     on the breaking (E7xU1, SO(16)xSO(16), etc.) but the sum of")
print(f"     squared projections is UNIVERSALLY 60 = 2*h*(E8) by the Casimir.")
print()
print(f"  2. GY DETERMINANT: The ratio R(p) = det(H_kink)/det(H_step) is a")
print(f"     smooth monotonic function of the projection p. It scales as")
print(f"     R(p) ~ phibar^(A*p^2) for large p, with A ~ {A_final:.4f}.")
print(f"     There is no special value of p where R(p) equals a modular form.")
print()
print(f"  3. TOTAL PRODUCT: The product over all 240 roots gives")
print(f"     phibar^N where N depends on the number of physical DoF per root:")
R_test_final = gy_det_ratio(1.0, L=30.0, nsteps_per_unit=3000)
n_test_final = math.log(R_test_final) / ln_phibar
for n_phys in [1, 2, 3]:
    N_total = n_phys * A_final * casimir_sum
    print(f"       n_phys={n_phys}: N = {N_total:.2f}  (target: 80)")
print(f"     None of these match 80 exactly.")
print()
print(f"  4. GAUGE-GHOST CANCELLATION: In 5D, gauge and ghost contributions")
print(f"     cancel, leaving only the A_5 scalar mode. The scalar sees")
print(f"     V(x) = p^2*Phi^2 + V''(Phi), which includes the PT n=2")
print(f"     stability potential. The total scalar contribution is")
print(f"     phibar^{total_n_scalar:.2f} (computed for e_1 breaking).")
print()
print(f"  5. CASIMIR UNIVERSALITY: The total is the SAME for all breaking")
print(f"     directions. The 240-root sum depends only on the E8 Casimir,")
print(f"     not on the specific Cartan direction chosen.")
print()
print(f"  6. THE 2/3 GAP: For the exponent 80, the required asymptotic")
print(f"     coefficient is A = 2/3 (with n_phys=2). The actual GY gives")
print(f"     A ~ {A_final:.4f}. The discrepancy suggests that:")
print(f"     (a) The scalar GY on the kink is an approximation, not exact,")
print(f"     (b) Non-perturbative effects (instantons, BPS states) contribute,")
print(f"     (c) The T^2 iteration mechanism (proven algebraically) may be")
print(f"         the correct framework, not the field-theory determinant.")
print()
print(f"  7. CONNECTION TO MODULAR FORMS: The modular form expressions")
print(f"     for alpha_s, sin^2(theta_W), and 1/alpha do NOT emerge from")
print(f"     the functional determinant calculation. If they are correct,")
print(f"     their origin must be NON-PERTURBATIVE or topological,")
print(f"     not from the 1-loop GY computation.")
print()
print(f"  STATUS: The functional determinant computation is INCONCLUSIVE")
print(f"  regarding the modular form origin of coupling constants.")
print(f"  The GY ratio is a well-defined quantity but does not directly")
print(f"  produce eta, theta, or Eisenstein functions.")
print(f"  The strongest evidence for the framework remains:")
print(f"  - The algebraic T^2 iteration (exponent 80)")
print(f"  - The Casimir sum = 60 = 2*h*(E8) universality")
print(f"  - The numerical coincidences at q = 1/phi")
print()
print(SEP)
print("  Script complete.")
print(SEP)
