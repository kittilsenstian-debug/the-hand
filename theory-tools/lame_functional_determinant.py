#!/usr/bin/env python3
"""
lame_functional_determinant.py -- THE HOLY GRAIL COMPUTATION
=============================================================

Compute the functional determinant of the n=2 Lame FLUCTUATION operator
at the golden nome q = 1/phi.

THE PHYSICS:
  The kink phi(x) = v*tanh(kappa*x) has a fluctuation operator:
    M = -d^2/dx^2 + V''(phi_kink(x)) = -d^2/dx^2 + m^2 - n(n+1)*kappa^2*sech^2(kappa*x)
  with n = 2 (for phi^4 theory). This is the Poschl-Teller operator.

  On a PERIODIC domain (kink lattice), the sech^2 potential becomes
  the Lame potential:
    M_Lame = -d^2/dx^2 + c - n(n+1)*k^2*sn^2(x,k)
  where c is a constant ensuring the same asymptotic behavior.

  Actually, the standard LAME EQUATION with the kink-relevant sign is:
    [-d^2/dx^2 - n(n+1)*k^2*sn^2(x,k)] psi = -E * psi
  equivalently:
    [-d^2/dx^2 + E_shift - n(n+1)*k^2*sn^2(x,k)] psi = lambda * psi
  where E_shift = n(n+1)*k^2 * <sn^2> is chosen to set <V> = 0.

  KEY QUESTION: Does the ratio det(M_Lame)/det(M_free) equal eta(1/phi)
  or a simple function thereof?

APPROACH:
  1. Compute the spectrum of the PHYSICAL fluctuation operator:
     H = -d^2/dx^2 - 6k^2*sn^2(x,k) + <6k^2*sn^2>
     which has a zero mode (translational) and bound states.
  2. Also compute the STANDARD Lame: H' = -d^2/dx^2 + 6k^2*sn^2(x,k)
  3. Use multiple methods: ODE/monodromy, spectral grid, zeta-regularization
  4. Compare all results against eta, theta functions at q = 1/phi.

REFERENCES:
  - Dunne & Rao (1999) "Lame Instantons" hep-th/9906113
  - Dunne (2007) "Functional Determinants in QFT" arXiv:0711.1178
  - McKean & van Moerbeke (1975) "The spectrum of Hill's equation"
  - Whittaker & Watson, "Modern Analysis" Ch. XXIII
"""

import sys
import numpy as np
from scipy import linalg as la
from scipy.special import ellipj

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import mpmath
from mpmath import mp, mpf, pi, sqrt, log, exp
from mpmath import ellipk, ellipe

# Set high precision
mp.dps = 50

# =================================================================
# FUNDAMENTAL CONSTANTS
# =================================================================
phi = (1 + sqrt(5)) / 2
phibar = 1 / phi
q_golden = phibar
ln_phi = log(phi)
SQRT5 = sqrt(5)

print("=" * 80)
print("  THE HOLY GRAIL: LAME FUNCTIONAL DETERMINANT AT THE GOLDEN NOME")
print("=" * 80)
print()

# =================================================================
# PART 0: HIGH-PRECISION MODULAR FORMS AT q = 1/phi
# =================================================================
print("PART 0: HIGH-PRECISION MODULAR FORMS AT q = 1/phi")
print("-" * 80)

def eta_dedekind(q, N=3000):
    result = q ** (mpf(1)/24)
    for n in range(1, N+1):
        result *= (1 - q**n)
        if abs(q**n) < mpf(10)**(-mp.dps):
            break
    return result

def theta_func(index, q, N=3000):
    if index == 2:
        s = mpf(0)
        for n in range(N):
            s += q**(n*(n+1))
        return 2 * q**mpf('0.25') * s
    elif index == 3:
        s = mpf(1)
        for n in range(1, N):
            s += 2 * q**(n*n)
        return s
    elif index == 4:
        s = mpf(1)
        for n in range(1, N):
            s += 2 * (-1)**n * q**(n*n)
        return s

q = q_golden
eta_val = eta_dedekind(q)
t2 = theta_func(2, q)
t3 = theta_func(3, q)
t4 = theta_func(4, q)

# Eta at dark node
eta_dark = eta_dedekind(q**2)

print(f"  q = 1/phi = {mpmath.nstr(q, 25)}")
print(f"  eta(q)     = {mpmath.nstr(eta_val, 25)}")
print(f"  eta(q^2)   = {mpmath.nstr(eta_dark, 20)}")
print(f"  theta_2    = {mpmath.nstr(t2, 25)}")
print(f"  theta_3    = {mpmath.nstr(t3, 25)}")
print(f"  theta_4    = {mpmath.nstr(t4, 25)}")
print(f"  t2/t3      = {mpmath.nstr(t2/t3, 20)} (nodal => ~1)")
print()

# Elliptic modulus
k = t2**2 / t3**2
kprime = t4**2 / t3**2
m_param = k**2  # parameter for mpmath/scipy
K_val = ellipk(m_param)
Kp_val = ellipk(kprime**2)
period = 2 * K_val

print(f"  k = theta_2^2/theta_3^2 = {mpmath.nstr(k, 25)}")
print(f"  k' = theta_4^2/theta_3^2 = {mpmath.nstr(kprime, 15)}")
print(f"  1-k^2 = {mpmath.nstr(1-k**2, 10)}")
print(f"  K(k)  = {mpmath.nstr(K_val, 20)}")
print(f"  K'(k) = {mpmath.nstr(Kp_val, 20)}")
print(f"  K'/K  = {mpmath.nstr(Kp_val/K_val, 15)} = ln(phi)/pi = {mpmath.nstr(ln_phi/pi, 15)}")
print(f"  Period T = 2K = {mpmath.nstr(period, 15)}")
print()

# Average of sn^2 over one period
E_elliptic = ellipe(m_param)
sn2_avg = (K_val - E_elliptic) / (m_param * K_val)
print(f"  <sn^2> = (K-E)/(k^2*K) = {mpmath.nstr(sn2_avg, 15)}")
print()

# Convert key values to float for scipy computations
k_f = float(k)
m_f = float(m_param)
K_f = float(K_val)
T_f = float(period)
eta_f = float(eta_val)
t2_f = float(t2)
t3_f = float(t3)
t4_f = float(t4)
eta_dark_f = float(eta_dark)
phi_f = float(phi)
phibar_f = float(phibar)
sn2_avg_f = float(sn2_avg)

# =================================================================
# PART 1: n=2 LAME BAND EDGES
# =================================================================
print("=" * 80)
print("PART 1: n=2 LAME BAND EDGES")
print("-" * 80)
print()

# For H_+ = -d^2/dx^2 + 6k^2*sn^2(x,k), band edges are:
k2 = k**2
k4 = k2**2
disc = sqrt(1 - k2 + k4)

E_edges_plus = sorted([
    2*(1+k2) - 2*disc,  # ~0 in PT limit
    1 + k2,             # ~2 in PT limit
    1 + 4*k2,           # ~5 in PT limit
    4 + k2,             # ~5 in PT limit
    2*(1+k2) + 2*disc   # ~6 in PT limit
])

print("  POSITIVE Lame: H = -d^2 + 6k^2*sn^2")
print(f"  Band edges [PT limit: 0, 2, 5, 5, 6]:")
for i, e in enumerate(E_edges_plus):
    print(f"    E_{i+1} = {mpmath.nstr(e, 20)}")
print()

# For H_- = -d^2/dx^2 - 6k^2*sn^2(x,k) + const, the PHYSICAL kink operator,
# the band edges are SHIFTED. The eigenvalues of -d^2 - 6k^2*sn^2 are:
# -(band edges of +6k^2*sn^2), i.e., the spectrum is reflected.
# But actually, the Lame equation -y'' - n(n+1)k^2 sn^2 y = E y has
# band edges at -E_j (negative of the positive case).

# For the kink fluctuation operator:
# H_kink = -d^2 - 6k^2*sn^2 + m^2
# where m^2 = 6k^2 in the PT limit (the scalar mass squared).
# More precisely, for the phi^4 kink:
# V''(phi_kink) = m^2 - 6*kappa^2*sech^2(kappa*x)
# The PT eigenvalues (in units where kappa=1) are:
# lambda_0 = 0 (zero mode), lambda_1 = 3 (breathing mode), continuum starts at 4
# (These are for V_PT = -6*sech^2, eigenvalues E = 0, 3, 4+p^2)
# The full fluctuation operator: -d^2 + 4 - 6*sech^2 has eigenvalues 0, 3, 4+p^2
# (i.e., the mass term m^2=4 shifts the PT spectrum from {-4, -1, p^2} to {0, 3, 4+p^2})

# For the periodic case: H_kink = -d^2 + 6k^2(1-sn^2) = -d^2 + 6k^2*cn^2*dn^2/...
# Wait, let me think more carefully.
# In the PT limit: sech^2(x) = 1 - tanh^2(x). So:
# -6*sech^2 = -6 + 6*tanh^2 = -6 + 6*sn^2(x, k=1)
# The fluctuation operator is: -d^2 + 4 - 6*sech^2 = -d^2 -2 + 6*tanh^2
# In the Lame generalization: -d^2 + c + 6*k^2*sn^2
# where c = -2 in the PT limit (c = 6k^2 - 6 - m^2... depends on convention).

# ACTUALLY, the cleanest approach: just shift the POSITIVE Lame by a constant.
# If H_+ = -d^2 + 6k^2*sn^2 has eigenvalues E_j, then
# H_shifted = -d^2 + 6k^2*sn^2 - <6k^2*sn^2> has eigenvalues E_j - <V>
# where <V> = 6k^2*<sn^2>.

V_avg = 6 * m_param * sn2_avg
print(f"  <V> = 6k^2*<sn^2> = {mpmath.nstr(V_avg, 15)}")
print()

# Shifted eigenvalues (mean-subtracted)
E_shifted = [e - V_avg for e in E_edges_plus]
print(f"  Mean-subtracted band edges:")
for i, e in enumerate(E_shifted):
    print(f"    E_{i+1} - <V> = {mpmath.nstr(e, 15)}")
print()

# =================================================================
# PART 2: NUMERICAL EIGENVALUE COMPUTATION
# =================================================================
print("=" * 80)
print("PART 2: NUMERICAL EIGENVALUE COMPUTATION ON GRID")
print("-" * 80)
print()

# We compute three operators on a periodic grid [0, 2K]:
# A) H_+ = -d^2 + 6k^2*sn^2      (positive Lame, all eigenvalues > 0)
# B) H_kink = -d^2 + 6k^2*(1-2*sn^2) = H_+ - 12k^2*sn^2 + 6k^2
#    Actually, let me use H_kink = -d^2 + m^2 - 6k^2*sn^2
#    where m^2 = 2(1+k^2) is the "mass" at the minimum of the Lame potential.
#    In PT limit: m^2 = 4.
# C) H_free = -d^2 + m^2 (constant mass, for comparison)

# The m^2 for the kink fluctuation operator:
# At the minima of V(Phi) = lambda*(Phi^2-Phi-1)^2, V'' = 2*lambda*(6*Phi^2-2*Phi-2+4*Phi^2-2*Phi)
# Actually, at the minima Phi = phi, phi_bar:
# V''(phi) = lambda * (12*phi^2 - 4*phi - 2) = lambda * (12*phi + 10) = lambda * (12*phi+10)
# With lambda = 1/(3*phi^2): V''(phi) = (12*phi+10)/(3*phi^2) = (12+10/phi)/(3*phi)
# = (12+10*phibar)/(3*phi) = (12+6.18...)/(3*1.618..) hmm too complicated.

# Let's use the standard normalization: the PT potential is
# V_PT = -n(n+1)*sech^2(x) = -6*sech^2(x) for n=2
# The bound state energies are: E_0 = -4, E_1 = -1
# Continuum starts at E = 0.
# The fluctuation operator about the kink is:
# M = -d^2 + m^2 + V_PT = -d^2 + 4 - 6*sech^2
# (where m^2 = 4 is the squared mass at the vacuum)
# Eigenvalues: 0 (zero mode), 3 (breathing), 4+p^2 (continuum)

# In the Lame generalization (periodic kink array):
# M_Lame = -d^2 + E_shift - 6k^2*sn^2(x,k)
# We choose E_shift so that the "continuum threshold" matches.
# In PT: continuum at m^2=4, and -6*sech^2 adds bound states below.
# For Lame: the "top of the potential" is 6k^2 (max of sn^2 is 1).
# The "continuum" starts at E_shift.
# Match: E_shift = n(n+1)k^2 = 6k^2 (the potential maximum).
# Then M_Lame = -d^2 + 6k^2 - 6k^2*sn^2 = -d^2 + 6k^2*cn^2*dn^2/(...)
# Hmm, actually: 1 - sn^2 = cn^2, so
# M_Lame = -d^2 + 6k^2*(1 - sn^2) = -d^2 + 6k^2*cn^2(x,k)

# The eigenvalues of M_Lame = eigenvalues of (-d^2 + 6k^2*sn^2) shifted:
# lambda_j(M_Lame) = 6k^2 - E_j(Lame)
# where E_j(Lame) are eigenvalues of -d^2 + 6k^2*sn^2.
# So: eigenvalues of M_Lame = 6k^2 - E_j

# Band edges of M_Lame (in decreasing E order from the positive Lame):
shift_val = 6 * m_param  # 6k^2
E_kink_edges = sorted([shift_val - e for e in E_edges_plus])

print(f"  6k^2 = {mpmath.nstr(shift_val, 15)}")
print(f"  Kink fluctuation operator: M = -d^2 + 6k^2*cn^2(x,k)")
print(f"  = -d^2 + 6k^2 - 6k^2*sn^2")
print(f"  Eigenvalues = 6k^2 - E_j(positive Lame)")
print()
print(f"  Kink band edges [PT limit: 0, 1, 1, 4, 6]:")
for i, e in enumerate(E_kink_edges):
    print(f"    lambda_{i+1} = {mpmath.nstr(e, 15)}")
print()

# In the PT limit: 6 - {0,2,5,5,6} = {6,4,1,1,0}
# Sorted: {0, 1, 1, 4, 6}
# The zero mode (lambda=0) and breathing mode (lambda=3 in continuous, near 1 in band edge)
# Actually wait: PT eigenvalues for -d^2 - 6*sech^2 are: E = -4, -1, p^2
# Kink fluctuation: -d^2 + 4 - 6*sech^2 has eigenvalues: 0, 3, 4+p^2
# But band edges of -d^2 + 6*sn^2 are: 0, 2, 5, 5, 6
# And 6 - {0,2,5,5,6} = {6,4,1,1,0}
# So the kink operator 6k^2*cn^2 has band edges at ~ 0, 1, 1, 4, 6.
# The "zero mode" is at 0, and the breathing mode region is 1 < E < 4.
# This is different from the isolated kink where breathing = 3.
# The band structure means: band [0,~1], gap [~1,~1], band [~1,~4], gap [~4,~6], band >6

print("  NOTE: For the kink operator M = -d^2 + 6k^2*cn^2:")
print("  In the PT limit (k->1), cn(x)->sech(x), recovering the standard PT.")
print("  Band edges: {0, 1, 1, 4, 6} in PT limit.")
print("  Zero mode is at E=0 (bottom of lowest band).")
print("  Breathing mode region: 1 < E < 4.")
print()

# =================================================================
# PART 3: GRID COMPUTATION OF BOTH OPERATORS
# =================================================================
print("=" * 80)
print("PART 3: NUMERICAL SPECTRUM VIA GRID DISCRETIZATION")
print("-" * 80)
print()

def build_periodic_hamiltonian(N_g, V_func_values, T):
    """Build NxN matrix for -d^2/dx^2 + V(x_i) with periodic BCs."""
    dx = T / N_g
    H = np.zeros((N_g, N_g))
    for i in range(N_g):
        H[i, i] = 2.0 / dx**2 + V_func_values[i]
        H[i, (i+1) % N_g] = -1.0 / dx**2
        H[i, (i-1) % N_g] = -1.0 / dx**2
    return H

# Grid computation
for N_grid in [400, 800, 1600]:
    dx = T_f / N_grid
    x_grid = np.array([i * T_f / N_grid for i in range(N_grid)])

    sn_grid, cn_grid, dn_grid, _ = ellipj(x_grid, m_f)

    # Operator A: Positive Lame: -d^2 + 6k^2*sn^2
    V_plus = 6 * m_f * sn_grid**2

    # Operator B: Kink fluctuation: -d^2 + 6k^2*cn^2 = -d^2 + 6k^2*(1-sn^2)
    V_kink = 6 * m_f * cn_grid**2

    # Operator C: Free massive: -d^2 + m_asymp^2
    # In the kink operator, the asymptotic value (at the vacuum) is:
    # cn^2(0) = 1, cn^2(K) = 1-k^2 ~ 0
    # Actually, cn(x,k) oscillates. The asymptotic mass for the kink is:
    # V_kink(x -> half-period) = 6k^2 cn^2(K) = 6k^2*(1-k^2) ~ 0
    # V_kink(x = 0) = 6k^2*cn^2(0) = 6k^2*1 = 6k^2
    # The AVERAGE: <V_kink> = 6k^2*<cn^2> = 6k^2*(1 - <sn^2>)
    V_kink_avg = 6 * m_f * (1 - sn2_avg_f)
    V_free_const = np.full(N_grid, V_kink_avg)

    # Build and diagonalize
    H_plus = build_periodic_hamiltonian(N_grid, V_plus, T_f)
    H_kink_mat = build_periodic_hamiltonian(N_grid, V_kink, T_f)
    H_free = build_periodic_hamiltonian(N_grid, V_free_const, T_f)

    eigs_plus = la.eigvalsh(H_plus)
    eigs_kink = la.eigvalsh(H_kink_mat)
    eigs_free = la.eigvalsh(H_free)

    if N_grid == 800:
        eigs_plus_800 = eigs_plus
        eigs_kink_800 = eigs_kink
        eigs_free_800 = eigs_free

    print(f"  N = {N_grid}:")
    print(f"    Positive Lame lowest 6: {eigs_plus[:6]}")
    print(f"    Kink operator lowest 6: {eigs_kink[:6]}")
    print(f"    Free operator lowest 3: {eigs_free[:3]}")
    print()

print()

# =================================================================
# PART 4: KINK OPERATOR DETAILED ANALYSIS (N=800)
# =================================================================
print("=" * 80)
print("PART 4: KINK OPERATOR DETAILED ANALYSIS")
print("-" * 80)
print()

eigs_k = eigs_kink_800
eigs_f = eigs_free_800

print(f"  Kink operator H_kink = -d^2 + 6k^2*cn^2(x,k) on [0, 2K], periodic BC")
print(f"  N_grid = 800")
print()

# The kink operator spectrum:
# - Lowest eigenvalue should be near 0 (zero mode, lifted by periodicity)
# - Next should be near 1 (edge of gap 1)
# - Then near 1 (other edge of gap 1 -- tiny gap)
# - Then band up to near 4
# - Then near 6

print(f"  Lowest 15 eigenvalues:")
for i in range(15):
    print(f"    lambda_{i:2d} = {eigs_k[i]:18.12f}")
print()

# The free operator (constant potential = <V_kink>):
print(f"  Free operator (constant V = <V_kink> = {V_kink_avg:.10f}):")
print(f"  Lowest 10 eigenvalues:")
for i in range(10):
    print(f"    mu_{i:2d} = {eigs_f[i]:18.12f}")
print()

# =================================================================
# PART 5: ZETA-REGULARIZED DETERMINANT RATIOS
# =================================================================
print("=" * 80)
print("PART 5: ZETA-REGULARIZED DETERMINANT RATIOS")
print("-" * 80)
print()

# Method 1: det'(H_kink) / det'(H_free) skipping zero modes
# The kink operator's lowest eigenvalue is very small (near zero mode).
# The free operator's lowest eigenvalue is <V_kink> ≈ 0.585 (NOT zero, since V_free = const > 0).

# So H_kink has a near-zero mode but H_free does not (for constant V > 0).
# The correct comparison is:
# det(H_kink) / det(H_free)  [including all eigenvalues]
# or
# det'(H_kink) / det(H_free)  [removing just the zero mode from H_kink]

# Method 1a: Full ratio (with near-zero mode)
log_det_full = 0.0
for i in range(800):
    if eigs_k[i] > 1e-15 and eigs_f[i] > 0:
        log_det_full += np.log(eigs_k[i]) - np.log(eigs_f[i])
det_full_ratio = np.exp(log_det_full)

print(f"  Method 1a: det(H_kink)/det(H_free) [all eigenvalues]")
print(f"    = {det_full_ratio:.15e}")
print(f"    log = {log_det_full:.15f}")
print()

# Method 1b: Skip first eigenvalue of kink (zero mode)
log_det_prime = 0.0
for i in range(1, 800):
    if eigs_k[i] > 1e-15 and eigs_f[i-1] > 0:
        log_det_prime += np.log(eigs_k[i]) - np.log(eigs_f[i-1])
det_prime_ratio = np.exp(log_det_prime)

print(f"  Method 1b: det'(H_kink)/det(H_free) [skip zero mode]")
print(f"    = {det_prime_ratio:.15e}")
print(f"    log = {log_det_prime:.15f}")
print()

# Method 2: Compare with the truly free operator -d^2 (no mass)
# H_0 = -d^2 on [0, T] periodic: eigenvalues = (2*pi*n/T)^2
eigs_free_massless = np.zeros(800)
for i in range(800):
    n = (i+1)//2 if i > 0 else 0
    sign = 1  # eigenvalues are doubly degenerate for n > 0
    eigs_free_massless[i] = (2*np.pi*n/T_f)**2

# Sort them (they should already be sorted)
eigs_free_massless.sort()

# det'(H_kink)/det'(H_0): skip zero mode from both
log_ratio_2 = 0.0
for i in range(1, 800):  # skip i=0 from both
    if eigs_k[i] > 1e-10 and eigs_free_massless[i] > 1e-10:
        log_ratio_2 += np.log(eigs_k[i]) - np.log(eigs_free_massless[i])
det_ratio_2 = np.exp(log_ratio_2)

print(f"  Method 2: det'(H_kink)/det'(-d^2) [both zero modes removed]")
print(f"    = {det_ratio_2:.15e}")
print(f"    log = {log_ratio_2:.15f}")
print()

# Method 3: Compare POSITIVE Lame with free
# H_+ = -d^2 + 6k^2*sn^2 vs H_0 = -d^2  (both have zero mode near zero)
eigs_p = eigs_plus_800

log_ratio_3 = 0.0
for i in range(1, 800):
    if eigs_p[i] > 1e-10 and eigs_free_massless[i] > 1e-10:
        log_ratio_3 += np.log(eigs_p[i]) - np.log(eigs_free_massless[i])
det_ratio_3 = np.exp(log_ratio_3)

print(f"  Method 3: det'(H_+)/det'(-d^2) [positive Lame / free]")
print(f"    = {det_ratio_3:.15e}")
print(f"    log = {log_ratio_3:.15f}")
print()

# =================================================================
# PART 6: SHIFTED DETERMINANT (more reliable)
# =================================================================
print("=" * 80)
print("PART 6: SHIFTED DETERMINANT det(H+s)/det(H_0+s)")
print("-" * 80)
print()

# This avoids zero mode issues entirely.
# det(H_kink + s) / det(-d^2 + s) for various s

print(f"  {'s':>8} {'log det(H_k+s)/det(H_0+s)':>28} {'det ratio':>22}")
print(f"  {'-'*8} {'-'*28} {'-'*22}")

shift_results = {}
for s in [0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 20.0, 50.0]:
    lr = 0.0
    for i in range(800):
        lk = eigs_k[i] + s
        l0 = eigs_free_massless[i] + s
        if lk > 0 and l0 > 0:
            lr += np.log(lk) - np.log(l0)
    dr = np.exp(lr)
    shift_results[s] = (lr, dr)
    print(f"  {s:8.1f} {lr:28.15f} {dr:22.15e}")

print()

# The physically relevant shifted determinant might be at s = 6k^2 (the mass^2):
s_mass = 6 * m_f
lr_mass = 0.0
for i in range(800):
    lk = eigs_k[i] + s_mass
    l0 = eigs_free_massless[i] + s_mass
    if lk > 0 and l0 > 0:
        lr_mass += np.log(lk) - np.log(l0)
dr_mass = np.exp(lr_mass)
print(f"  At s = 6k^2 = {s_mass:.6f} (vacuum mass^2):")
print(f"    log ratio = {lr_mass:.15f}")
print(f"    det ratio = {dr_mass:.15e}")
print()

# =================================================================
# PART 7: HEAT KERNEL COMPARISON
# =================================================================
print("=" * 80)
print("PART 7: HEAT KERNEL TRACE - Tr[e^(-t*H_kink)] vs Tr[e^(-t*H_0)]")
print("-" * 80)
print()

# The heat kernel is K(t) = sum exp(-t*lambda_n)
# The DIFFERENCE K_kink(t) - K_0(t) encodes the spectral information.

print(f"  {'t':>10} {'K_kink(t)':>18} {'K_free(t)':>18} {'K_k - K_0':>18} {'relative':>12}")
print(f"  {'-'*10} {'-'*18} {'-'*18} {'-'*18} {'-'*12}")

for t in [0.001, 0.01, 0.05, 0.1, 0.2, 0.5, 1.0, 2.0, 5.0, 10.0]:
    K_kink_t = np.sum(np.exp(-t * eigs_k))
    K_free_t = np.sum(np.exp(-t * eigs_free_massless))
    diff = K_kink_t - K_free_t
    rel = diff / K_free_t if K_free_t != 0 else 0
    print(f"  {t:10.3f} {K_kink_t:18.8f} {K_free_t:18.8f} {diff:18.8f} {rel:12.8f}")

print()

# =================================================================
# PART 8: THE KEY COMPARISON WITH MODULAR FORMS
# =================================================================
print("=" * 80)
print("PART 8: THE KEY COMPARISON WITH MODULAR FORMS")
print("-" * 80)
print()

# Let's look at the det ratio from the POSITIVE Lame at mass^2 shift
# det(H_+ + s) / det(-d^2 + s) at various s

print("  POSITIVE LAME det(H_+ + s) / det(-d^2 + s):")
print(f"  {'s':>8} {'log ratio':>20} {'det ratio':>22}")
print(f"  {'-'*8} {'-'*20} {'-'*22}")

for s in [0.1, 0.5, 1.0, 2.0, 5.0, 10.0]:
    lr = 0.0
    for i in range(800):
        lp = eigs_p[i] + s
        l0 = eigs_free_massless[i] + s
        if lp > 0 and l0 > 0:
            lr += np.log(lp) - np.log(l0)
    dr = np.exp(lr)
    print(f"  {s:8.1f} {lr:20.10f} {dr:22.15e}")

print()

# Now check the HEAT KERNEL at special values
# The integrated heat kernel gives:
# integral_0^inf [K(t) - K_0(t)] * t^{s-1} dt = Gamma(s) * [zeta(s) - zeta_0(s)]
# At s = -1/2 (in some conventions): this relates to the Casimir energy
# At s = 0: this is proportional to det'/det'_0

# Compute the SPECTRAL ASYMMETRY using the heat kernel:
# K_diff(t) = K_kink(t) - K_free(t) at small t gives:
# K_diff(t) ~ -<V>*t*T/(4*pi*t)^{1/2} + O(t^{3/2})
# The coefficient gives the potential effect.

print("  Small-t heat kernel expansion:")
print("  K_diff(t) = a_{-1/2}/sqrt(t) + a_0 + a_1*sqrt(t) + ...")
for t in [0.0001, 0.0005, 0.001, 0.005]:
    K_k = np.sum(np.exp(-t * eigs_k))
    K_0 = np.sum(np.exp(-t * eigs_free_massless))
    diff = K_k - K_0
    # a_{-1/2} ~ diff * sqrt(t)
    a_half = diff * np.sqrt(t)
    print(f"  t = {t:.4f}: K_diff = {diff:15.6f}, K_diff*sqrt(t) = {a_half:15.8f}")

print()

# =================================================================
# PART 9: THE FUNDAMENTAL QUESTION - ETA MATCH
# =================================================================
print("=" * 80)
print("PART 9: SEARCHING FOR ETA IN THE DETERMINANT")
print("-" * 80)
print()

# The most natural quantity: the one-loop partition function
# Z_1loop = [det(H_kink)]^{-1/2}
# If Z = 1/eta, then det = eta^2.
# If Z = eta, then det = 1/eta^2.
# We check det'(H_kink)/det'(H_0) and det(H_+ + s)/det(H_0 + s).

# From the det' computation:
print(f"  det'(H_kink)/det'(H_0) = {det_ratio_2:.6e}")
print(f"  det'(H_+)/det'(H_0)   = {det_ratio_3:.6e}")
print()

# These are huge numbers, suggesting the ratio diverges.
# This makes sense: the kink operator has a near-zero mode that
# lifts to a tiny eigenvalue, creating a large product ratio.
# The free operator has exactly zero at n=0, and we removed it.

# Let's instead look at a CONVERGENT quantity:
# The LOG of the determinant ratio, normalized per unit length.
print(f"  Normalized log determinant (per unit length 2K):")
print(f"    log[det'(H_kink)/det'(H_0)] / (2K) = {log_ratio_2 / T_f:.15f}")
print(f"    For comparison:")
print(f"      eta = {eta_f:.15f}")
print(f"      log(eta) = {np.log(eta_f):.15f}")
print(f"      -log(eta) = {-np.log(eta_f):.15f}")
print(f"      log(eta)/(2K) = {np.log(eta_f)/T_f:.15f}")
print()

# Actually, the more standard normalization: the CASIMIR ENERGY
# E_Casimir = (1/2) * sum [lambda_n^{1/2} - mu_n^{1/2}]
# (zeta-regularized)

# Let's compute the SPECTRAL ZETA FUNCTION at integer points:
# zeta_diff(s) = sum [lambda_n^{-s} - mu_n^{-s}]
print(f"  Spectral zeta function difference zeta_kink(s) - zeta_free(s):")
for s_val in [2.0, 3.0, 4.0, 5.0]:
    z_k = np.sum(eigs_k[1:]**(-s_val))  # skip near-zero mode
    z_0 = np.sum(eigs_free_massless[1:]**(-s_val))
    print(f"    zeta_diff({s_val:.0f}) = {z_k - z_0:.15f}")

print()

# =================================================================
# PART 10: THE CORRECT FORMULATION - FORMAN'S RESULT
# =================================================================
print("=" * 80)
print("PART 10: FORMAN'S FORMULA FOR PERIODIC BC")
print("-" * 80)
print()

# Forman's theorem: for a Hill operator H = -d^2 + V(x) on [0, T]:
# det_periodic(H - E) = 2 - Delta(E)
# where Delta(E) is the Hill discriminant (trace of monodromy matrix).
#
# This means:
# det_periodic(H_kink) = 2 - Delta_kink(0)
# where Delta_kink is the Hill discriminant for the kink operator.
#
# For the KINK operator H_kink = -d^2 + 6k^2*cn^2(x,k):
# We need Delta_kink(0) = y1(T) + y2'(T) for the ODE:
# y'' = -6k^2*cn^2(x,k) * y

print("  Computing Hill discriminant for KINK operator: -d^2 + 6k^2*cn^2(x,k)")
print("  via RK4 integration over one period T = 2K")
print()

def compute_hill_disc_kink(E_val, m_val, K_per, nsteps=20000):
    """Compute Hill discriminant for -y'' - [6k^2*cn^2(x,k) - E]*y = 0."""
    T = 2 * K_per
    h = T / nsteps

    def rhs(x, state):
        y, yp = state[0], state[1]
        sn = mpmath.ellipfun('sn', x, m=m_val)
        cn2 = 1 - m_val * sn**2  # cn^2 = 1 - k^2*sn^2
        V = 6 * m_val * cn2  # This is 6k^2*cn^2
        return [yp, (V - E_val) * y]

    def rk4_step(f, t, y, h):
        k1 = f(t, y)
        k2 = f(t + h/2, [y[i] + h/2*k1[i] for i in range(2)])
        k3 = f(t + h/2, [y[i] + h/2*k2[i] for i in range(2)])
        k4 = f(t + h,   [y[i] + h*k3[i] for i in range(2)])
        return [y[i] + h/6*(k1[i] + 2*k2[i] + 2*k3[i] + k4[i]) for i in range(2)]

    # Solution 1: y(0)=1, y'(0)=0
    state1 = [mpf(1), mpf(0)]
    x = mpf(0)
    for _ in range(nsteps):
        state1 = rk4_step(rhs, x, state1, h)
        x += h

    # Solution 2: y(0)=0, y'(0)=1
    state2 = [mpf(0), mpf(1)]
    x = mpf(0)
    for _ in range(nsteps):
        state2 = rk4_step(rhs, x, state2, h)
        x += h

    delta = state1[0] + state2[1]
    return delta, state1, state2

print("  Integrating with 20000 steps...")
delta_kink_0, mono1, mono2 = compute_hill_disc_kink(mpf(0), m_param, K_val, nsteps=20000)

print(f"  Monodromy matrix for kink operator at E=0:")
print(f"    y1(T) = {mpmath.nstr(mono1[0], 20)}")
print(f"    y2(T) = {mpmath.nstr(mono2[0], 20)}")
print(f"    y1'(T) = {mpmath.nstr(mono1[1], 20)}")
print(f"    y2'(T) = {mpmath.nstr(mono2[1], 20)}")
print(f"    det(M) = {mpmath.nstr(mono1[0]*mono2[1] - mono1[1]*mono2[0], 15)} (should be 1)")
print(f"    Delta_kink(0) = {mpmath.nstr(delta_kink_0, 20)}")
print()

det_per_kink = 2 - delta_kink_0
print(f"  det_periodic(H_kink) = 2 - Delta_kink(0) = {mpmath.nstr(det_per_kink, 20)}")
print()

# Also for the POSITIVE Lame:
print("  Computing Hill discriminant for POSITIVE Lame: -d^2 + 6k^2*sn^2(x,k)")
print("  at E = 0, with 20000 steps...")

def compute_hill_disc_positive(E_val, m_val, K_per, nsteps=20000):
    """Hill discriminant for -y'' + [6k^2*sn^2(x,k) - E]*y = 0."""
    T = 2 * K_per
    h = T / nsteps

    def rhs(x, state):
        y, yp = state[0], state[1]
        sn = mpmath.ellipfun('sn', x, m=m_val)
        V = 6 * m_val * sn**2
        return [yp, (V - E_val) * y]

    def rk4_step(f, t, y, h):
        k1 = f(t, y)
        k2 = f(t + h/2, [y[i] + h/2*k1[i] for i in range(2)])
        k3 = f(t + h/2, [y[i] + h/2*k2[i] for i in range(2)])
        k4 = f(t + h,   [y[i] + h*k3[i] for i in range(2)])
        return [y[i] + h/6*(k1[i] + 2*k2[i] + 2*k3[i] + k4[i]) for i in range(2)]

    state1 = [mpf(1), mpf(0)]
    x = mpf(0)
    for _ in range(nsteps):
        state1 = rk4_step(rhs, x, state1, h)
        x += h

    state2 = [mpf(0), mpf(1)]
    x = mpf(0)
    for _ in range(nsteps):
        state2 = rk4_step(rhs, x, state2, h)
        x += h

    delta = state1[0] + state2[1]
    return delta, state1, state2

delta_pos_0, _, _ = compute_hill_disc_positive(mpf(0), m_param, K_val, nsteps=20000)

print(f"  Delta_positive(0) = {mpmath.nstr(delta_pos_0, 20)}")
det_per_pos = 2 - delta_pos_0
print(f"  det_periodic(H_+) = 2 - Delta_+(0) = {mpmath.nstr(det_per_pos, 20)}")
print()

# =================================================================
# PART 11: THE KEY - HILL DISCRIMINANT AT BAND EDGE E_1
# =================================================================
print("=" * 80)
print("PART 11: HILL DISCRIMINANT NEAR THE BAND EDGES")
print("-" * 80)
print()

# For the kink operator, the band edges are at 6k^2 - E_j.
# The lowest band edge is near 0 (the zero mode).
# delta_kink(E) = 2 at E = E_kink_edge = 6k^2 - E_5(positive Lame)

# Let's check the kink Hill discriminant at several energies
print("  Kink operator Hill discriminant at various E:")
kink_test_E = [mpf(0), mpf('0.01'), mpf('0.05'), mpf('0.1'), mpf('0.5'),
               mpf(1), mpf(2), mpf(3), mpf(4), mpf(5), mpf(6)]

for E_test in kink_test_E:
    d, _, _ = compute_hill_disc_kink(E_test, m_param, K_val, nsteps=10000)
    print(f"    E = {mpmath.nstr(E_test, 6):>8}  Delta = {mpmath.nstr(d, 14)}")

print()

# =================================================================
# PART 12: DIRICHLET DETERMINANT (Gelfand-Yaglom, no zero mode issue)
# =================================================================
print("=" * 80)
print("PART 12: GELFAND-YAGLOM DIRICHLET DETERMINANT")
print("-" * 80)
print()

# For Dirichlet BC on [0, T]:
# det_Dir(H - E) / det_Dir(-d^2 - E) = y_2(T, E) / y_2^free(T, E)
# where y_2 is the solution with y_2(0)=0, y_2'(0)=1.
# For the free operator at E=0: y_2^free(x) = x, so y_2(T) = T.
# For the free operator at E=E0: y_2^free(x) = sin(sqrt(E0)*x)/sqrt(E0).

# The Gelfand-Yaglom ratio for the kink operator at E=0:
# R = y_2(T) / T where y_2 is for the kink operator.

# From the monodromy computation: y2(T) = mono2[0] from the kink
y2_kink_T = mono2[0]
GY_ratio_kink = y2_kink_T / period

print(f"  Kink operator, Dirichlet BC:")
print(f"    y_2(T) = {mpmath.nstr(y2_kink_T, 20)}")
print(f"    y_2^free(T) = T = {mpmath.nstr(period, 15)}")
print(f"    GY ratio = y_2(T)/T = {mpmath.nstr(GY_ratio_kink, 20)}")
print()

# Compare with modular forms
targets = {
    "eta": eta_val,
    "eta^2": eta_val**2,
    "eta^3": eta_val**3,
    "1/eta": 1/eta_val,
    "1/eta^2": 1/eta_val**2,
    "theta_4": t4,
    "theta_4^2": t4**2,
    "theta_3": t3,
    "theta_3^2": t3**2,
    "eta*theta_4": eta_val*t4,
    "eta^2/theta_4": eta_val**2/t4,
    "(t3*t4)^2": (t3*t4)**2,
    "2K/pi = t3^2": t3**2,
    "phi": phi,
    "phi^2": phi**2,
    "phibar": phibar,
    "1": mpf(1),
    "SQRT5": SQRT5,
    "3": mpf(3),
}

print(f"  Checking GY ratio against modular forms:")
print(f"  {'Expression':>20} {'Value':>20} {'GY/val':>20} {'log ratio':>15}")
print(f"  {'-'*20} {'-'*20} {'-'*20} {'-'*15}")
for name, val in targets.items():
    if abs(val) > mpf(10)**(-40):
        ratio = GY_ratio_kink / val
        log_r = log(abs(ratio))
        print(f"  {name:>20} {mpmath.nstr(val, 12):>20} {mpmath.nstr(ratio, 12):>20} {mpmath.nstr(log_r, 10):>15}")

print()

# =================================================================
# PART 13: ALTERNATIVE - USE cn^2 = 1 - k^2*sn^2 TO RELATE OPERATORS
# =================================================================
print("=" * 80)
print("PART 13: RELATING KINK AND POSITIVE LAME")
print("-" * 80)
print()

# H_kink = -d^2 + 6k^2*cn^2 = -d^2 + 6k^2*(1 - k^2*sn^2/... )
# Wait: cn^2(x,k) = 1 - sn^2(x,k). So:
# H_kink = -d^2 + 6k^2*(1 - sn^2) = -d^2 + 6k^2 - 6k^2*sn^2
# = (6k^2) * I - H_+ + (I * something)
# No wait: H_+ = -d^2 + 6k^2*sn^2
# So: H_kink = -d^2 + 6k^2 - 6k^2*sn^2 = 6k^2*I - (-d^2 + 6k^2*sn^2) + 2*(-d^2)
# Hmm, that's not right. Simply:
# H_kink = -d^2 + 6k^2 - 6k^2*sn^2
# H_+ = -d^2 + 6k^2*sn^2
# So: H_kink + H_+ = -2*d^2 + 6k^2
# And: H_kink = 6k^2 - H_+ (only if d^2 terms cancel, which they don't)

# Actually the key relation is:
# eigenvalue_j(H_kink) = 6k^2 - eigenvalue_j(H_+) WRONG (derivative terms differ)
# No, both have the SAME -d^2. So:
# H_kink = -d^2 + 6k^2 - 6k^2*sn^2
# If phi_j is eigenfunction of H_+ with eigenvalue E_j:
# H_+ phi_j = E_j phi_j => (-d^2 + 6k^2*sn^2) phi_j = E_j phi_j
# Then: H_kink phi_j = (-d^2 + 6k^2 - 6k^2*sn^2) phi_j
#                     = (6k^2 - 6k^2*sn^2) phi_j + (-d^2) phi_j
#                     = 6k^2*phi_j - 6k^2*sn^2*phi_j + (-d^2) phi_j
#                     = 6k^2*phi_j - (H_+ - (-d^2)) phi_j + (-d^2) phi_j
#                     = 6k^2*phi_j - H_+ phi_j + 2*(-d^2) phi_j
# This doesn't simplify unless we know -d^2 phi_j separately.

# But for the EIGENVALUE SPECTRUM: the Hill discriminants satisfy:
# Delta_kink(E) = Delta_+(6k^2 - E)
# because the substitution E -> 6k^2 - E in the Lame equation
# corresponds to cn^2 <-> sn^2 (which is a half-period shift x -> x + K).
# THIS IS THE KEY RELATION.

delta_kink_check = delta_pos_0  # Delta_+(0) should equal Delta_kink(6k^2)

d_kink_6k2, _, _ = compute_hill_disc_kink(shift_val, m_param, K_val, nsteps=10000)

print(f"  Relation: Delta_kink(E) = Delta_+(6k^2 - E)")
print(f"    Delta_+(0) = {mpmath.nstr(delta_pos_0, 15)}")
print(f"    Delta_kink(6k^2={mpmath.nstr(shift_val,6)}) = {mpmath.nstr(d_kink_6k2, 15)}")
print(f"    Match: {mpmath.nstr(abs(1 - d_kink_6k2/delta_pos_0), 5)}")
print()

# This means: det_per(H_kink - E) = det_per(H_+ - (6k^2 - E))
# So: det_per(H_kink) = det_per(H_+ - 6k^2) = 2 - Delta_+(6k^2)

delta_pos_6k2, _, _ = compute_hill_disc_positive(shift_val, m_param, K_val, nsteps=10000)
det_per_from_relation = 2 - delta_pos_6k2

print(f"  Delta_+(6k^2) = {mpmath.nstr(delta_pos_6k2, 15)}")
print(f"  det_per(H_kink) = 2 - Delta_+(6k^2) = {mpmath.nstr(det_per_from_relation, 15)}")
print(f"  Direct: det_per(H_kink) = {mpmath.nstr(det_per_kink, 15)}")
print(f"  Match: {mpmath.nstr(abs(1 - det_per_from_relation/det_per_kink), 5)}")
print()

# =================================================================
# PART 14: SPECTRAL DETERMINANT VIA THETA FUNCTIONS (ANALYTICAL)
# =================================================================
print("=" * 80)
print("PART 14: ANALYTICAL FORMULA FOR LAME DETERMINANT")
print("-" * 80)
print()

# For a Hill operator on [0, T], the Hill discriminant is:
# Delta(E) = 2 + (product formula involving band edges)
# For the n=2 Lame, the 5 band edges e_1 < ... < e_5 determine:
# Delta(E) - 2 = -[(2K)^2 / (product normalization)] * prod_j (E - e_j^periodic)
# where e_j^periodic are the eigenvalues with periodic BC.

# For n=2: 3 periodic eigenvalues (E_1, E_3, E_5) and 2 antiperiodic (E_2, E_4).
# Hill's result:
# 2 - Delta(E) = (2K/pi)^2 * prod_{n=0}^inf [(e_n^+ - E) / (n*pi/K)^2]
# where e_n^+ are ALL periodic eigenvalues (band edges + higher bands).

# For n=2, the first 3 are the band edges. The higher ones (n >= 3) are
# e_n^+ ~ (n*pi/K)^2 + corrections.

# The FINITE product of the 3 band edges gives the leading behavior.
# The infinite product of corrections gives a convergent factor.

# Actually, for the positive Lame -d^2 + 6k^2*sn^2 with n=2,
# the 3 periodic band edges are: E_1, E_3, E_5

# At E = 0:
# 2 - Delta_+(0) = -[C * E_1 * E_3 * E_5] * [correction from higher modes]

# The correction from higher modes is the RATIO:
# prod_{n=3}^inf [e_n^+/(n*pi/K)^2]
# which should be close to 1 for the well-separated modes.

# Let's compute: 2 - Delta_+(0) and compare with E_1*E_3*E_5
E1 = E_edges_plus[0]
E3 = E_edges_plus[2]
E5 = E_edges_plus[4]

product_edges = E1 * E3 * E5
print(f"  Periodic band edges: E_1 = {mpmath.nstr(E1, 15)}")
print(f"                       E_3 = {mpmath.nstr(E3, 15)}")
print(f"                       E_5 = {mpmath.nstr(E5, 15)}")
print(f"  Product E_1*E_3*E_5 = {mpmath.nstr(product_edges, 15)}")
print(f"  2 - Delta_+(0) = {mpmath.nstr(det_per_pos, 15)}")
print()

# The full Hill formula:
# 2 - Delta(0) = -T^2 * prod_{n=0}^inf [lambda_n^per / ((n*pi/K)^2 - 0)]
# For n=0: contributes lambda_0 / (regularized 0)
# This is where the regularization matters.

# Let me try a different approach: use the KNOWN result for the Lame determinant.
# From Dunne & Rao (1999): the one-instanton fluctuation determinant for
# the n=2 PT potential is:
# det'(-d^2 - 6*sech^2 + 4) / det(-d^2 + 4) = 1/12
# (with the zero mode removed)

# For the PERIODIC case (Lame), the analogous quantity involves:
# the ratio evaluated at the instanton turning points.

# The key formula from spectral theory of finite-gap operators:
# For the Lame operator, the functional determinant can be expressed
# as a THETA function of the spectral curve.

# For genus g=2 (n=2), the theta function is a 2-variable theta function.
# But at the golden nome (nodal degeneration), this FACTORIZES into
# products of genus-1 theta functions.

print("  KNOWN RESULT (Dunne-Rao): For isolated n=2 PT kink (k=1):")
print("    det'(-d^2 + 4 - 6*sech^2) / det(-d^2 + 4) = 1/12")
print("    This is the ratio with zero mode removed.")
print()

# Check numerically using our grid computation:
# H_kink has eigenvalues lambda_j. The lowest is near 0 (zero mode).
# H_free_massive has eigenvalue m^2 + (2*pi*n/T)^2.
# The ratio det'(H_kink)/det(H_free_massive) should approach 1/12
# as k -> 1 (period -> infinity).

# For our k: let's compute this ratio
V_mass = 6 * m_f  # This is 6k^2, the asymptotic mass of the kink operator
eigs_massive = np.array([(2*np.pi*n/T_f)**2 + V_mass for n in range(400)])
# Each n>0 is doubly degenerate
eigs_massive_full = np.zeros(800)
eigs_massive_full[0] = V_mass
for i in range(1, 800):
    n = (i+1)//2
    eigs_massive_full[i] = (2*np.pi*n/T_f)**2 + V_mass
eigs_massive_full.sort()

# det'(H_kink) / det(H_free_massive)
log_DR = 0.0
for i in range(1, 800):  # skip zero mode of kink
    if eigs_k[i] > 1e-10 and eigs_massive_full[i-1] > 0:
        log_DR += np.log(eigs_k[i]) - np.log(eigs_massive_full[i-1])
DR_value = np.exp(log_DR)

print(f"  det'(H_kink)/det(H_free_massive) at golden nome:")
print(f"    = {DR_value:.15f}")
print(f"    Dunne-Rao PT value = 1/12 = {1/12:.15f}")
print(f"    Ratio to 1/12 = {DR_value * 12:.10f}")
print()

# The deviation from 1/12 is the INSTANTON CORRECTION.
# If this correction is related to eta(q)...
deviation = DR_value - 1.0/12
correction_factor = DR_value * 12
print(f"  Correction factor = 12 * det'_ratio = {correction_factor:.15f}")
print(f"  1 + correction to 1/12:")
print(f"    correction = {correction_factor - 1:.15f}")
print()

# Check if the correction is related to modular forms
print(f"  Checking correction against modular forms:")
corr = correction_factor - 1
print(f"    correction = {corr:.10f}")
print(f"    eta         = {eta_f:.10f}")
print(f"    theta_4     = {t4_f:.10f}")
print(f"    phibar      = {phibar_f:.10f}")
print(f"    corr/phibar = {corr/phibar_f:.10f}")
print(f"    corr/eta    = {corr/eta_f:.10f}")
print(f"    corr/t4     = {corr/t4_f:.10f}")
print(f"    corr/(phibar^2) = {corr/phibar_f**2:.10f}")
print()

# =================================================================
# PART 15: CONVERGENCE STUDY OF THE DUNNE-RAO CORRECTION
# =================================================================
print("=" * 80)
print("PART 15: CONVERGENCE STUDY OF THE det' RATIO")
print("-" * 80)
print()

for N_g in [200, 400, 800, 1200, 1600]:
    dx = T_f / N_g
    x_g = np.array([i * T_f / N_g for i in range(N_g)])
    sn_g, cn_g, _, _ = ellipj(x_g, m_f)

    V_k = 6 * m_f * cn_g**2
    H_k = build_periodic_hamiltonian(N_g, V_k, T_f)
    eigs_k_g = la.eigvalsh(H_k)

    # Free massive operator eigenvalues
    eigs_m_g = np.zeros(N_g)
    eigs_m_g[0] = V_mass
    for i in range(1, N_g):
        n = (i+1)//2
        eigs_m_g[i] = (2*np.pi*n/T_f)**2 + V_mass
    eigs_m_g.sort()

    # det'(H_kink)/det(H_massive)
    lr = 0.0
    for i in range(1, N_g):
        if eigs_k_g[i] > 1e-10 and eigs_m_g[i-1] > 0:
            lr += np.log(eigs_k_g[i]) - np.log(eigs_m_g[i-1])
    dr = np.exp(lr)
    corr_g = dr * 12

    print(f"  N={N_g:5d}: det'_ratio = {dr:.12f}  12*ratio = {corr_g:.12f}  correction = {corr_g-1:.8f}")

print()

# =================================================================
# PART 16: HALF-PERIOD DETERMINANT (Dirichlet on [0, K])
# =================================================================
print("=" * 80)
print("PART 16: HALF-PERIOD COMPUTATION")
print("-" * 80)
print()

# The kink sits at x=0 to x=K (half period). The other half is the anti-kink.
# On [0, K] with appropriate BC, we get the single-kink contribution.

# Compute GY for the kink operator on [0, K] (half period) with Dirichlet BC
def compute_half_period_GY(m_val, K_per, nsteps=10000):
    """Gelfand-Yaglom on [0, K] for kink operator."""
    h = K_per / nsteps

    def rhs(x, state):
        y, yp = state[0], state[1]
        sn = mpmath.ellipfun('sn', x, m=m_val)
        cn2 = 1 - m_val * sn**2
        V = 6 * m_val * cn2
        return [yp, V * y]

    def rk4_step(f, t, y, h):
        k1 = f(t, y)
        k2 = f(t + h/2, [y[i] + h/2*k1[i] for i in range(2)])
        k3 = f(t + h/2, [y[i] + h/2*k2[i] for i in range(2)])
        k4 = f(t + h,   [y[i] + h*k3[i] for i in range(2)])
        return [y[i] + h/6*(k1[i] + 2*k2[i] + 2*k3[i] + k4[i]) for i in range(2)]

    # y(0) = 0, y'(0) = 1 (Dirichlet at 0)
    state = [mpf(0), mpf(1)]
    x = mpf(0)
    for _ in range(nsteps):
        state = rk4_step(rhs, x, state, h)
        x += h

    # GY ratio = y(K) / K  (since free solution y_free = x gives y_free(K) = K)
    return state[0] / K_per, state[0]

gy_half, y_half = compute_half_period_GY(m_param, K_val, nsteps=20000)

print(f"  GY ratio on [0, K] (half period): {mpmath.nstr(gy_half, 20)}")
print(f"  y_2(K) = {mpmath.nstr(y_half, 20)}")
print(f"  K = {mpmath.nstr(K_val, 15)}")
print()

# Check this against modular forms
print(f"  Checking half-period GY against modular forms:")
for name, val in targets.items():
    if abs(val) > mpf(10)**(-40):
        ratio = gy_half / val
        if abs(ratio) > mpf('0.01') and abs(ratio) < mpf('1000'):
            print(f"    GY/{name} = {mpmath.nstr(ratio, 15)}")

print()

# =================================================================
# PART 17: THE DUNNE FORMULA - det IN TERMS OF DISCRIMINANT
# =================================================================
print("=" * 80)
print("PART 17: DECOMPOSITION OF det'(H_kink) / det(H_massive)")
print("-" * 80)
print()

# The Dunne-Rao result for the isolated kink (k=1):
# det'_PT / det_massive = 1/12
#
# For the periodic kink (nome q):
# det'_Lame / det_massive = (1/12) * F(q)
# where F(q) is the instanton correction factor.
# F(q) -> 1 as q -> 0 (isolated kink limit).
# At q = 1/phi, we computed F(q) = 12 * det'_ratio.
#
# THE QUESTION: Is F(1/phi) related to eta(1/phi)?

# Use best converged value (N=1200 from convergence study, but N=800 is what we have)
# From the output above, F = 12 * det'_ratio

# Let's also try with higher order finite difference for the grid
N_best = 1600
dx = T_f / N_best
x_g = np.array([i * T_f / N_best for i in range(N_best)])
sn_g, cn_g, _, _ = ellipj(x_g, m_f)
V_k = 6 * m_f * cn_g**2
H_k = build_periodic_hamiltonian(N_best, V_k, T_f)
eigs_best = la.eigvalsh(H_k)

eigs_m_best = np.zeros(N_best)
eigs_m_best[0] = V_mass
for i in range(1, N_best):
    n = (i+1)//2
    eigs_m_best[i] = (2*np.pi*n/T_f)**2 + V_mass
eigs_m_best.sort()

lr_best = 0.0
for i in range(1, N_best):
    if eigs_best[i] > 1e-10 and eigs_m_best[i-1] > 0:
        lr_best += np.log(eigs_best[i]) - np.log(eigs_m_best[i-1])
DR_best = np.exp(lr_best)
F_golden = DR_best * 12

print(f"  Best estimate (N={N_best}):")
print(f"  det'(H_kink)/det(H_massive) = {DR_best:.15f}")
print(f"  F(q=1/phi) = 12 * ratio = {F_golden:.15f}")
print(f"  log(F) = {np.log(F_golden):.15f}")
print()

print(f"  Checking F against modular forms and simple expressions:")

check_vals = [
    ("1", 1.0),
    ("eta", eta_f),
    ("eta^2", eta_f**2),
    ("1/eta", 1/eta_f),
    ("1/eta^2", 1/eta_f**2),
    ("theta_4", t4_f),
    ("1/theta_4", 1/t4_f),
    ("eta/theta_4", eta_f/t4_f),
    ("theta_4/eta", t4_f/eta_f),
    ("eta*theta_4", eta_f*t4_f),
    ("phibar", phibar_f),
    ("phibar^2", phibar_f**2),
    ("phi", phi_f),
    ("phi^2", phi_f**2),
    ("1/12", 1/12),
    ("eta/12", eta_f/12),
    ("SQRT5", np.sqrt(5)),
    ("3*eta^2", 3*eta_f**2),
    ("theta_3^2/theta_4^2", (t3_f/t4_f)**2),
    ("1/(2*theta_4)", 1/(2*t4_f)),
    ("pi/(2K)", np.pi/(2*K_f)),
    ("(pi/K)^2", (np.pi/K_f)**2),
    ("eta_dark", eta_dark_f),
    ("eta_dark/eta", eta_dark_f/eta_f),
    ("eta/eta_dark", eta_f/eta_dark_f),
    ("(eta/eta_dark)^2", (eta_f/eta_dark_f)**2),
    ("sin2tW = eta^2/(2*t4)", eta_f**2/(2*t4_f)),
    ("C = eta*t4/2", eta_f*t4_f/2),
]

print(f"  {'Expression':>25} {'Value':>20} {'F/val':>15} {'log(F/val)':>15}")
print(f"  {'-'*25} {'-'*20} {'-'*15} {'-'*15}")
for name, val in check_vals:
    if val > 0:
        r = F_golden / val
        lr = np.log(r) if r > 0 else float('nan')
        marker = ""
        if abs(lr) < 0.05:
            marker = " <=== MATCH!"
        elif abs(r - 1) < 0.05:
            marker = " <=== MATCH!"
        print(f"  {name:>25} {val:20.12f} {r:15.10f} {lr:15.10f}{marker}")

print()

# =================================================================
# PART 18: RATIO AT DIFFERENT NOMES (q-dependence)
# =================================================================
print("=" * 80)
print("PART 18: THE INSTANTON CORRECTION F(q) vs q")
print("-" * 80)
print()

# Compute F(q) = 12 * det'(H_kink)/det(H_massive) for several values of q.
# For each q, we need to find k, compute K, build the grid, and diagonalize.

print(f"  {'q':>10} {'k':>15} {'K(k)':>12} {'F(q)':>15} {'eta(q)':>12} {'F/eta':>12}")
print(f"  {'-'*10} {'-'*15} {'-'*12} {'-'*15} {'-'*12} {'-'*12}")

def compute_F_at_nome(q_val, N_g=800):
    """Compute F(q) = 12 * det'(H_kink)/det(H_massive) at nome q."""
    # Modular forms at this q
    t2_q = float(theta_func(2, mpf(q_val)))
    t3_q = float(theta_func(3, mpf(q_val)))
    t4_q = float(theta_func(4, mpf(q_val)))
    eta_q = float(eta_dedekind(mpf(q_val)))

    k_q = t2_q**2 / t3_q**2
    m_q = k_q**2
    K_q = float(ellipk(mpf(m_q)))
    T_q = 2 * K_q
    V_m_q = 6 * m_q  # mass^2

    dx = T_q / N_g
    x_g = np.array([i * T_q / N_g for i in range(N_g)])

    sn_g, cn_g, _, _ = ellipj(x_g, m_q)
    V_k = 6 * m_q * cn_g**2

    H_k = build_periodic_hamiltonian(N_g, V_k, T_q)
    eigs = la.eigvalsh(H_k)

    eigs_m = np.zeros(N_g)
    eigs_m[0] = V_m_q
    for i in range(1, N_g):
        n = (i+1)//2
        eigs_m[i] = (2*np.pi*n/T_q)**2 + V_m_q
    eigs_m.sort()

    lr = 0.0
    for i in range(1, N_g):
        if eigs[i] > 1e-10 and eigs_m[i-1] > 0:
            lr += np.log(eigs[i]) - np.log(eigs_m[i-1])
    F = 12 * np.exp(lr)
    return F, k_q, K_q, eta_q

for q_test in [0.05, 0.1, 0.2, 0.3, 0.4, 0.5, phibar_f, 0.65, 0.7]:
    try:
        F_q, k_q, K_q, eta_q = compute_F_at_nome(q_test, N_g=600)
        F_eta = F_q / eta_q if eta_q > 0 else float('nan')
        marker = " <-- golden" if abs(q_test - phibar_f) < 0.01 else ""
        print(f"  {q_test:10.4f} {k_q:15.10f} {K_q:12.6f} {F_q:15.10f} {eta_q:12.8f} {F_eta:12.6f}{marker}")
    except Exception as e:
        print(f"  {q_test:10.4f} ERROR: {e}")

print()

# =================================================================
# PART 19: FINAL SUMMARY AND HONEST ASSESSMENT
# =================================================================
print("=" * 80)
print("PART 19: FINAL SUMMARY AND HONEST ASSESSMENT")
print("-" * 80)
print()

print(f"""
  THE LAME FUNCTIONAL DETERMINANT AT THE GOLDEN NOME
  ===================================================

  Operator: H_kink = -d^2/dx^2 + 6k^2*cn^2(x,k)  (kink fluctuation operator)
  Period:   T = 2K = {T_f:.10f}
  Nome:     q = 1/phi = {phibar_f:.10f}
  Modulus:  k = {k_f:.15f}

  RESULTS:
  --------

  1. Hill discriminant at E=0 (mpmath ODE integration):
     Delta_kink(0) = {float(delta_kink_0):.6e}
     det_per(H_kink) = 2 - Delta(0) = {float(det_per_kink):.6e}

  2. Dunne-Rao correction factor F(q) = 12 * det'(H_kink)/det(H_massive):
     F(1/phi) = {F_golden:.10f}  (N={N_best})

  3. Gelfand-Yaglom ratio on half-period [0, K]:
     y_2(K)/K = {float(gy_half):.10f}

  KEY MODULAR FORM VALUES:
     eta(1/phi)    = {eta_f:.10f}
     eta(1/phi^2)  = {eta_dark_f:.10f}
     theta_4(1/phi) = {t4_f:.10f}
     C = eta*t4/2  = {eta_f*t4_f/2:.10f}

  DOES F(1/phi) EQUAL eta(1/phi)?
     F(1/phi) = {F_golden:.10f}
     eta(1/phi) = {eta_f:.10f}
     Ratio F/eta = {F_golden/eta_f:.10f}
""")

# Check if the q-dependence helps identify the function
print("  Q-DEPENDENCE ANALYSIS:")
print("  If F(q) = some modular form, the q-dependence reveals which one.")
print("  The table above shows F(q) vs q alongside eta(q).")
print("  Look for: F(q) = A * eta(q)^B * theta_4(q)^C * ... ")
print()

print("  HONEST ASSESSMENT:")
print("  ==================")
print()
print("  The computation reveals that F(q) = 12 * det'(H_kink)/det(H_massive)")
print(f"  at q = 1/phi equals approximately {F_golden:.6f}.")
print(f"  eta(1/phi) = {eta_f:.6f}.")
print()
print(f"  F/eta = {F_golden/eta_f:.6f}")
print(f"  F/eta^2 = {F_golden/eta_f**2:.6f}")
print(f"  F/theta_4 = {F_golden/t4_f:.6f}")
print(f"  F*12 = {F_golden*12:.6f}")
print(f"  log(F)/log(eta) = {np.log(F_golden)/np.log(eta_f):.6f}")
print()

# Check if F is a RATIONAL number times something nice
# Round to simple fractions
from fractions import Fraction
for denom in range(1, 25):
    numer = round(F_golden * denom)
    frac_val = numer / denom
    if abs(frac_val - F_golden) / F_golden < 0.01:
        print(f"  F ~ {numer}/{denom} = {frac_val:.10f}  (error: {abs(frac_val-F_golden)/F_golden*100:.4f}%)")

print()
print("  Script complete.")
print("=" * 80)
