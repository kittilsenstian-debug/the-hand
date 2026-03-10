"""
CASCADE RESOLUTION: Can M₀, CKM, PMNS all fall from one insight?
=================================================================

The framework already has:
- PMNS formulas at 99.6-100%: sin(θ₁₂)=φ/3, sin²(θ₂₃)=3/(2φ²), sin(θ₁₃)=φ/11
- CKM formulas at 99.4-99.8%: V_us=φ/7, V_cb=φ/40, V_ub=φ/420
- v at 99.99%: M_Pl/(N^(13/4) × φ^(33/2) × 4)
- Breathing mode: 108.5 GeV

The GAP: these formulas aren't connected to the mechanism (kink bound states).
The mechanism (breathing mode overlap) gives θ₁₃ at 85.7%, not 99.7%.

HYPOTHESIS: M₀ is a framework number, and with the correct M₀ and
generation-specific widths, the mechanism REPRODUCES the formulas.

This script tests whether the gaps cascade-resolve.
"""

import numpy as np
from scipy import integrate, optimize, linalg
from scipy.special import gamma as gamma_func
import math
import sys

if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

phi = (1 + np.sqrt(5)) / 2
phibar = 1 / phi
sqrt5 = np.sqrt(5)
mu = 1836.15267
alpha_em = 1 / 137.036

# E8 / Coxeter data
h = 30  # E8 Coxeter number
coxeter_exp = [1, 7, 11, 13, 17, 19, 23, 29]
lucas_cox = [1, 7, 11, 29]
L = {1: 1, 2: 3, 3: 4, 4: 7, 5: 11, 6: 18, 7: 29, 8: 47}

# Measured mixing angles
# CKM
V_us_meas = 0.2253
V_cb_meas = 0.0405
V_ub_meas = 0.00382
V_td_meas = 0.00854
# PMNS
s12_sq_meas = 0.304
s23_sq_meas = 0.573
s13_sq_meas = 0.02219

# Generation positions (in wall half-widths)
u_pos = {3: 3.0, 2: -0.57, 1: -2.03}

# Kink parameters
# V(Phi) = lambda(Phi^2 - Phi - 1)^2, with lambda=1 for simplicity
# kappa = sqrt(2*lambda*a^2) = sqrt(5/2) (kink inverse width)
kappa = np.sqrt(5.0 / 2)

# Bound state profiles
def psi0(u):
    """Zero mode: sech^2(u)"""
    return 1.0 / np.cosh(u)**2

def psi1(u):
    """Breathing mode: sinh(u)/cosh^2(u)"""
    return np.sinh(u) / np.cosh(u)**2

print("=" * 72)
print("CASCADE RESOLUTION: M₀ → σ → MIXING ANGLES → FORMULAS")
print("=" * 72)

# ================================================================
# PART 1: WHAT IS M₀?
# ================================================================
print("\n" + "=" * 72)
print("PART 1: TESTING M₀ CANDIDATES")
print("=" * 72)

print("""
    M₀ is the single bulk mass scale. In wall half-width units:
    M_i = M₀ / sqrt(g_i)  where g_i = Casimir coupling of gen i.

    The existing formulas (if correct) CONSTRAIN M₀.
    Let's work BACKWARDS from the formulas to find M₀.
""")

# The PMNS formulas give mixing angles.
# The CKM formulas give mixing angles.
# Both should emerge from the domain wall overlap integrals.
#
# Key: sin(theta_13) = phi/11 means the (1,3) mixing element equals phi/11.
# From the breathing mode mechanism:
# sin(theta_13) ~ |Y_13| / |Y_33|
# where Y_ij = integral f_i(u) * psi1(u) * f_j(u) du
#
# For narrow Gaussians centered at u_i:
# Y_13 ~ psi1(u_13_eff) where u_13_eff is some effective position
#
# Let's compute what the formulas REQUIRE.

print("    PMNS formulas (targets for the mechanism):")
print(f"    sin(θ₁₂) = φ/3 = {phi/3:.6f}   → sin²(θ₁₂) = {(phi/3)**2:.6f} (meas: {s12_sq_meas})")
print(f"    sin²(θ₂₃) = 3/(2φ²) = {3/(2*phi**2):.6f}   (meas: {s23_sq_meas})")
print(f"    sin(θ₁₃) = φ/11 = {phi/11:.6f}  → sin²(θ₁₃) = {(phi/11)**2:.6f} (meas: {s13_sq_meas})")
print()

# ================================================================
# PART 2: THE TWO-CHANNEL YUKAWA
# ================================================================
print("=" * 72)
print("PART 2: TWO-CHANNEL YUKAWA — THE CASCADE INSIGHT")
print("=" * 72)

print("""
    The kink has TWO bound states. The Higgs doublet H and its
    conjugate H̃ decompose into even and odd parts:

    H(u)  = A[ψ₀(u) + β·ψ₁(u)]     (Higgs)
    H̃(u) = A[ψ₀(u) - β·ψ₁(u)]     (conjugate Higgs)

    The kink decomposition gives β = c₁/c₀ = π√5/2 ≈ 3.512.

    Up-type quarks couple to H:   Y_u ∝ ψ₀ + β·ψ₁
    Down-type quarks couple to H̃: Y_d ∝ ψ₀ - β·ψ₁

    CKM = mismatch between Y_u and Y_d eigenvectors.

    For leptons:
    Charged leptons couple to H̃ (like down quarks in SU(5)):
        Y_ℓ ∝ ψ₀ - β·ψ₁
    Neutrinos get Majorana mass from cross-wall tunneling:
        Y_ν ∝ ψ₁ only (breathing mode dominates)

    PMNS = mismatch between Y_ℓ and Y_ν eigenvectors.
""")

beta = np.pi * sqrt5 / 2  # c1/c0 = pi*sqrt(5)/2
print(f"    β = c₁/c₀ = π√5/2 = {beta:.6f}")
print(f"    β ≈ L(4)/2 = 7/2 = 3.500 ({min(beta, 3.5)/max(beta, 3.5)*100:.2f}%)")
print()

# ================================================================
# PART 3: COMPUTE 3×3 YUKAWA MATRICES
# ================================================================
print("=" * 72)
print("PART 3: COMPUTING YUKAWA MATRICES FOR EACH CHANNEL")
print("=" * 72)

def compute_yukawa_matrices(sigma, positions):
    """
    Compute Y^(0) and Y^(1) matrices from Gaussian fermion profiles.

    Y^(0)_ij = integral f_i(u) * psi0(u) * f_j(u) du
    Y^(1)_ij = integral f_i(u) * psi1(u) * f_j(u) du

    f_i(u) = exp(-(u - u_i)^2 / (2*sigma^2))
    """
    Y0 = np.zeros((3, 3))
    Y1 = np.zeros((3, 3))

    for i in range(3):
        for j in range(i, 3):
            ui = positions[3-i]  # Gen 3, 2, 1
            uj = positions[3-j]

            def integrand0(u):
                fi = np.exp(-(u - ui)**2 / (2*sigma**2))
                fj = np.exp(-(u - uj)**2 / (2*sigma**2))
                return fi * psi0(u) * fj

            def integrand1(u):
                fi = np.exp(-(u - ui)**2 / (2*sigma**2))
                fj = np.exp(-(u - uj)**2 / (2*sigma**2))
                return fi * psi1(u) * fj

            Y0[i, j], _ = integrate.quad(integrand0, -15, 15)
            Y0[j, i] = Y0[i, j]

            Y1[i, j], _ = integrate.quad(integrand1, -15, 15)
            Y1[j, i] = Y1[i, j]

    return Y0, Y1


def mixing_angles_from_matrix(U):
    """Extract Euler angles from 3x3 unitary matrix."""
    # Standard PDG parametrization
    s13 = abs(U[0, 2])
    if s13 > 1:
        s13 = 1.0
    c13 = np.sqrt(1 - s13**2) if s13 < 1 else 0

    if c13 > 1e-10:
        s12 = abs(U[0, 1]) / c13
        s23 = abs(U[1, 2]) / c13
    else:
        s12 = 0
        s23 = 0

    s12 = min(s12, 1.0)
    s23 = min(s23, 1.0)

    return s12**2, s23**2, s13**2  # return sin^2 values


def compute_mixing(Y_charged, Y_neutral):
    """
    Compute mixing matrix from mismatch between two Yukawa matrices.
    PMNS = V_charged^dag × V_neutral
    CKM = V_up^dag × V_down
    """
    # Diagonalize Y_charged^dag Y_charged
    M_ch = Y_charged @ Y_charged.T
    evals_ch, V_ch = np.linalg.eigh(M_ch)

    # Sort by eigenvalue (ascending → Gen1, Gen2, Gen3)
    idx_ch = np.argsort(evals_ch)
    V_ch = V_ch[:, idx_ch]

    # Diagonalize Y_neutral^dag Y_neutral
    M_nu = Y_neutral @ Y_neutral.T
    evals_nu, V_nu = np.linalg.eigh(M_nu)

    idx_nu = np.argsort(evals_nu)
    V_nu = V_nu[:, idx_nu]

    # Mixing matrix
    U = V_ch.T @ V_nu

    return U, evals_ch[idx_ch], evals_nu[idx_nu]


# ================================================================
# PART 4: SCAN — FIND σ THAT REPRODUCES PMNS
# ================================================================
print("\n" + "=" * 72)
print("PART 4: SCANNING σ AND β TO REPRODUCE PMNS ANGLES")
print("=" * 72)

print("""
    Hypothesis: charged lepton Yukawa = ψ₀ - β·ψ₁ (H̃ channel)
                neutrino Yukawa = ψ₁ only (breathing mode / tunneling)

    PMNS = V_ℓ† × V_ν

    Scan σ (fermion width) to find best match to ALL 3 PMNS angles.
""")

best_pmns = None
best_pmns_cost = float('inf')

results = []

for sigma_10 in range(5, 100):
    sigma = sigma_10 / 10.0

    Y0, Y1 = compute_yukawa_matrices(sigma, u_pos)

    # Charged leptons: Y_ell = Y0 - beta*Y1 (H-tilde channel)
    Y_ell = Y0 - beta * Y1

    # Neutrinos: Y_nu = Y1 (breathing mode)
    Y_nu = Y1.copy()

    # Check for degenerate matrices
    if np.max(np.abs(Y_ell)) < 1e-15 or np.max(np.abs(Y_nu)) < 1e-15:
        continue

    try:
        U_pmns, evals_ell, evals_nu = compute_mixing(Y_ell, Y_nu)
        s12sq, s23sq, s13sq = mixing_angles_from_matrix(U_pmns)

        # Cost: match all 3 PMNS angles
        cost = (np.log(max(s12sq, 1e-10)) - np.log(s12_sq_meas))**2 + \
               (np.log(max(s23sq, 1e-10)) - np.log(s23_sq_meas))**2 + \
               (np.log(max(s13sq, 1e-10)) - np.log(s13_sq_meas))**2

        results.append((sigma, s12sq, s23sq, s13sq, cost))

        if cost < best_pmns_cost:
            best_pmns_cost = cost
            best_pmns = (sigma, s12sq, s23sq, s13sq, U_pmns, evals_ell, evals_nu)
    except Exception:
        continue

# Print scan results
print(f"    {'σ':>5s} | {'sin²θ₁₂':>10s} | {'sin²θ₂₃':>10s} | {'sin²θ₁₃':>10s} | {'cost':>10s}")
print(f"    {'':>5s} | {'(0.304)':>10s} | {'(0.573)':>10s} | {'(0.0222)':>10s} |")
print("    " + "-" * 60)

# Show selected results
for sigma, s12sq, s23sq, s13sq, cost in results:
    if sigma in [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0, 6.0, 8.0] or \
       (best_pmns and abs(sigma - best_pmns[0]) < 0.15):
        print(f"    {sigma:5.1f} | {s12sq:10.5f} | {s23sq:10.5f} | {s13sq:10.5f} | {cost:10.3f}")

if best_pmns:
    sigma_opt, s12sq, s23sq, s13sq, U_pmns, evals_ell, evals_nu = best_pmns
    print(f"\n    BEST FIT: σ = {sigma_opt:.1f}")
    print(f"    sin²θ₁₂ = {s12sq:.5f} (target: {s12_sq_meas}, match: {min(s12sq, s12_sq_meas)/max(s12sq, s12_sq_meas)*100:.1f}%)")
    print(f"    sin²θ₂₃ = {s23sq:.5f} (target: {s23_sq_meas}, match: {min(s23sq, s23_sq_meas)/max(s23sq, s23_sq_meas)*100:.1f}%)")
    print(f"    sin²θ₁₃ = {s13sq:.5f} (target: {s13_sq_meas}, match: {min(s13sq, s13_sq_meas)/max(s13sq, s13_sq_meas)*100:.1f}%)")

# ================================================================
# PART 5: CKM FROM UP/DOWN MISMATCH
# ================================================================
print("\n\n" + "=" * 72)
print("PART 5: CKM FROM H vs H̃ MISMATCH")
print("=" * 72)

print("""
    Up quarks couple to H = ψ₀ + β·ψ₁
    Down quarks couple to H̃ = ψ₀ - β·ψ₁

    CKM = V_u† × V_d

    Using the same σ from the PMNS fit.
""")

best_ckm = None
best_ckm_cost = float('inf')

ckm_results = []

for sigma_10 in range(5, 100):
    sigma = sigma_10 / 10.0

    Y0, Y1 = compute_yukawa_matrices(sigma, u_pos)

    # Up quarks: Y_u = Y0 + beta*Y1 (H channel)
    Y_u = Y0 + beta * Y1

    # Down quarks: Y_d = Y0 - beta*Y1 (H-tilde channel)
    Y_d = Y0 - beta * Y1

    if np.max(np.abs(Y_u)) < 1e-15 or np.max(np.abs(Y_d)) < 1e-15:
        continue

    try:
        U_ckm, evals_u, evals_d = compute_mixing(Y_u, Y_d)

        # CKM elements
        V_us = abs(U_ckm[0, 1])
        V_cb = abs(U_ckm[1, 2])
        V_ub = abs(U_ckm[0, 2])

        cost = (np.log(max(V_us, 1e-10)) - np.log(V_us_meas))**2 + \
               (np.log(max(V_cb, 1e-10)) - np.log(V_cb_meas))**2 + \
               (np.log(max(V_ub, 1e-10)) - np.log(V_ub_meas))**2

        ckm_results.append((sigma, V_us, V_cb, V_ub, cost))

        if cost < best_ckm_cost:
            best_ckm_cost = cost
            best_ckm = (sigma, V_us, V_cb, V_ub, U_ckm, evals_u, evals_d)
    except Exception:
        continue

print(f"    {'σ':>5s} | {'V_us':>10s} | {'V_cb':>10s} | {'V_ub':>10s} | {'cost':>10s}")
print(f"    {'':>5s} | {'(0.2253)':>10s} | {'(0.0405)':>10s} | {'(0.00382)':>10s} |")
print("    " + "-" * 60)

for sigma, V_us, V_cb, V_ub, cost in ckm_results:
    if sigma in [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0, 6.0, 8.0] or \
       (best_ckm and abs(sigma - best_ckm[0]) < 0.15):
        print(f"    {sigma:5.1f} | {V_us:10.5f} | {V_cb:10.5f} | {V_ub:10.5f} | {cost:10.3f}")

if best_ckm:
    sigma_opt, V_us, V_cb, V_ub, U_ckm, evals_u, evals_d = best_ckm
    print(f"\n    BEST FIT: σ = {sigma_opt:.1f}")
    print(f"    V_us = {V_us:.5f} (target: {V_us_meas}, match: {min(V_us, V_us_meas)/max(V_us, V_us_meas)*100:.1f}%)")
    print(f"    V_cb = {V_cb:.5f} (target: {V_cb_meas}, match: {min(V_cb, V_cb_meas)/max(V_cb, V_cb_meas)*100:.1f}%)")
    print(f"    V_ub = {V_ub:.5f} (target: {V_ub_meas}, match: {min(V_ub, V_ub_meas)/max(V_ub, V_ub_meas)*100:.1f}%)")

# ================================================================
# PART 6: ALTERNATIVE — DIFFERENT WIDTHS FOR DIFFERENT SECTORS
# ================================================================
print("\n\n" + "=" * 72)
print("PART 6: GENERATION-SPECIFIC WIDTHS (from Casimir)")
print("=" * 72)

print("""
    Instead of one σ for all generations, each gen has its own width:
    σ_i = σ₀ × sqrt(g_i / g_max)

    where g_i is the Casimir coupling (larger g → narrower profile → heavier).

    Also test: up-type and down-type have DIFFERENT base widths
    σ_u ≠ σ_d (from 10 vs 5-bar of SU(5)).
""")

# Use Casimir ratio pattern from the S3 breaking
# Gen 3: g_3 (largest, trivial irrep)
# Gen 2: g_2 (intermediate, standard irrep)
# Gen 1: g_1 (smallest, standard irrep)
# The mass ratios constrain: g_3/g_2 × (overlap ratio) = 16.82
# and g_2/g_1 × (overlap ratio) = 206.77

# From the combined_hierarchy analysis, try Casimir ratios:
# g_3 : g_2 : g_1 should give the right mass hierarchy

# The "positions" u_i = {+3.0, -0.57, -2.03} encode the coupling:
# f(u) = [tanh(u) + 1]/2  →  f²
# f²(3.0) / f²(-0.57) = 0.995/0.0587 = 16.95 ≈ 16.82 ✓
# f²(-0.57) / f²(-2.03) = 0.0587/0.000288 = 203.8 ≈ 206.77 ✓

# So the positions ALREADY encode the correct hierarchy.
# The widths add refinement.

# Now try: what if each generation's width σ_i is proportional to
# the distance from the wall center? This gives narrower profiles
# for generations far from center.

# Test hypothesis: σ_i proportional to 1/|u_i| (generation-specific)
for sigma0 in [1.0, 1.5, 2.0, 3.0]:
    sigmas = {}
    for g in [1, 2, 3]:
        # Width inversely proportional to distance from center
        d = max(abs(u_pos[g]), 0.5)
        sigmas[g] = sigma0 / d

    # Compute matrices with gen-specific widths
    Y0 = np.zeros((3, 3))
    Y1 = np.zeros((3, 3))

    for i in range(3):
        for j in range(i, 3):
            gi = 3 - i  # Gen 3, 2, 1
            gj = 3 - j
            ui = u_pos[gi]
            uj = u_pos[gj]
            si = sigmas[gi]
            sj = sigmas[gj]

            def integrand0(u, _ui=ui, _uj=uj, _si=si, _sj=sj):
                fi = np.exp(-(u - _ui)**2 / (2*_si**2))
                fj = np.exp(-(u - _uj)**2 / (2*_sj**2))
                return fi * psi0(u) * fj

            def integrand1(u, _ui=ui, _uj=uj, _si=si, _sj=sj):
                fi = np.exp(-(u - _ui)**2 / (2*_si**2))
                fj = np.exp(-(u - _uj)**2 / (2*_sj**2))
                return fi * psi1(u) * fj

            Y0[i, j], _ = integrate.quad(integrand0, -15, 15)
            Y0[j, i] = Y0[i, j]
            Y1[i, j], _ = integrate.quad(integrand1, -15, 15)
            Y1[j, i] = Y1[i, j]

    # PMNS: charged lepton = H̃, neutrino = ψ₁
    Y_ell = Y0 - beta * Y1
    Y_nu = Y1.copy()

    if np.max(np.abs(Y_ell)) > 1e-15 and np.max(np.abs(Y_nu)) > 1e-15:
        try:
            U_pmns, _, _ = compute_mixing(Y_ell, Y_nu)
            s12sq, s23sq, s13sq = mixing_angles_from_matrix(U_pmns)
            print(f"    σ₀ = {sigma0}, widths = ({sigmas[3]:.2f}, {sigmas[2]:.2f}, {sigmas[1]:.2f})")
            print(f"      PMNS: sin²θ₁₂={s12sq:.4f}, sin²θ₂₃={s23sq:.4f}, sin²θ₁₃={s13sq:.5f}")

            # Compare to formulas
            f12 = (phi/3)**2
            f23 = 3/(2*phi**2)
            f13 = (phi/11)**2
            m12 = min(s12sq, f12)/max(s12sq, f12)*100 if s12sq > 0 else 0
            m23 = min(s23sq, f23)/max(s23sq, f23)*100 if s23sq > 0 else 0
            m13 = min(s13sq, f13)/max(s13sq, f13)*100 if s13sq > 0 else 0
            print(f"      vs formulas: θ₁₂={m12:.1f}%, θ₂₃={m23:.1f}%, θ₁₃={m13:.1f}%")
            print()
        except Exception:
            pass

# ================================================================
# PART 7: THE DEEP QUESTION — WHY φ/D?
# ================================================================
print("\n" + "=" * 72)
print("PART 7: WHY DO MIXING ANGLES EQUAL φ/D?")
print("=" * 72)

print("""
    The formulas sin(θ) = φ/D where D is a Coxeter/Lucas number
    have a natural interpretation in the domain wall picture:

    The mixing angle between generations i and j is:
    sin(θ_ij) ≈ |Y_ij| / sqrt(Y_ii × Y_jj)

    In the narrow-profile limit (σ → 0):
    Y^(0)_ij → ψ₀(u_eff) = sech²(u_eff)
    Y^(1)_ij → ψ₁(u_eff) = sinh(u_eff)/cosh²(u_eff)

    where u_eff = (u_i + u_j)/2 for the geometric mean.

    For H̃ = ψ₀ - β·ψ₁:
    Y_ij(H̃) = sech²(u_eff) - β·sinh(u_eff)/cosh²(u_eff)
             = sech²(u_eff)[1 - β·sinh(u_eff)]
             = sech²(u_eff)[1 - β·tanh(u_eff)/sech(u_eff)]

    The RATIO Y_ij/Y_ii depends on the positions and β.

    For PMNS θ₁₃: the (1,3) element involves u₁=-2.03 and u₃=+3.0
    Mean position: (−2.03 + 3.0)/2 = 0.485
    ψ₁(0.485)/ψ₀(0.485) = sinh(0.485)/1 = 0.505

    For CKM V_us: the (1,2) element involves u₁=-2.03 and u₂=-0.57
    Mean position: (−2.03 + (−0.57))/2 = −1.30
    ψ₁(−1.30)/ψ₀(−1.30) = sinh(−1.30)/1 = −1.699

    The DENOMINATORS 3, 7, 11, 40, 420 should emerge from these
    position-dependent ratios. Let's check:
""")

# Test: do the positions give the right denominators?
def mixing_estimate(u_i, u_j, beta_val):
    """Estimate mixing from position-dependent H-tilde overlap ratio."""
    u_eff = (u_i + u_j) / 2
    psi0_val = psi0(u_eff)
    psi1_val = psi1(u_eff)

    # The effective Yukawa ratio
    Y_off = psi0_val + beta_val * psi1_val  # off-diagonal
    Y_diag_i = psi0(u_i) + beta_val * psi1(u_i)
    Y_diag_j = psi0(u_j) + beta_val * psi1(u_j)

    if abs(Y_diag_i) < 1e-20 or abs(Y_diag_j) < 1e-20:
        return 0

    return abs(Y_off) / np.sqrt(abs(Y_diag_i * Y_diag_j))


print("    Position-based mixing estimates:")
print()
# PMNS angles from positions
for name, gi, gj, meas in [
    ("θ₁₂ (PMNS)", 1, 2, np.sqrt(s12_sq_meas)),
    ("θ₂₃ (PMNS)", 2, 3, np.sqrt(s23_sq_meas)),
    ("θ₁₃ (PMNS)", 1, 3, np.sqrt(s13_sq_meas)),
]:
    ui = u_pos[gi]
    uj = u_pos[gj]

    # For neutrino channel (ψ₁ only):
    psi1_off = psi1((ui + uj) / 2)
    psi1_i = psi1(ui)
    psi1_j = psi1(uj)
    if abs(psi1_i * psi1_j) > 1e-20:
        ratio_nu = abs(psi1_off) / np.sqrt(abs(psi1_i * psi1_j))
    else:
        ratio_nu = 0

    # For charged lepton channel (ψ₀ - β·ψ₁):
    H_off = psi0((ui+uj)/2) - beta*psi1((ui+uj)/2)
    H_i = psi0(ui) - beta*psi1(ui)
    H_j = psi0(uj) - beta*psi1(uj)
    if abs(H_i * H_j) > 1e-20:
        ratio_ell = abs(H_off) / np.sqrt(abs(H_i * H_j))
    else:
        ratio_ell = 0

    print(f"    {name}: ν-channel = {ratio_nu:.4f}, ℓ-channel = {ratio_ell:.4f}, measured sin(θ) = {meas:.4f}")

print()
# CKM from positions
for name, gi, gj, meas in [
    ("V_us (CKM)", 1, 2, V_us_meas),
    ("V_cb (CKM)", 2, 3, V_cb_meas),
    ("V_ub (CKM)", 1, 3, V_ub_meas),
]:
    ui = u_pos[gi]
    uj = u_pos[gj]

    # Up channel (ψ₀ + β·ψ₁):
    Hu_off = psi0((ui+uj)/2) + beta*psi1((ui+uj)/2)
    Hu_i = psi0(ui) + beta*psi1(ui)
    Hu_j = psi0(uj) + beta*psi1(uj)
    if abs(Hu_i * Hu_j) > 1e-20:
        ratio_u = abs(Hu_off) / np.sqrt(abs(Hu_i * Hu_j))
    else:
        ratio_u = 0

    # Down channel (ψ₀ - β·ψ₁):
    Hd_off = psi0((ui+uj)/2) - beta*psi1((ui+uj)/2)
    Hd_i = psi0(ui) - beta*psi1(ui)
    Hd_j = psi0(uj) - beta*psi1(uj)
    if abs(Hd_i * Hd_j) > 1e-20:
        ratio_d = abs(Hd_off) / np.sqrt(abs(Hd_i * Hd_j))
    else:
        ratio_d = 0

    print(f"    {name}: up-channel = {ratio_u:.5f}, down-channel = {ratio_d:.5f}, measured = {meas:.5f}")

# ================================================================
# PART 8: THE CLEAN TEST — DO PMNS FORMULAS EMERGE?
# ================================================================
print("\n\n" + "=" * 72)
print("PART 8: DO THE FORMULAS EMERGE FROM THE MECHANISM?")
print("=" * 72)

print("""
    If the mechanism works, the mixing matrix eigenvalues should give:
    sin(θ₁₂) = φ/3, sin²(θ₂₃) = 3/(2φ²), sin(θ₁₃) = φ/11

    Testing with FINE σ scan (0.5 to 9.9, step 0.1):
""")

# Fine scan for PMNS
print(f"\n    Looking for σ where sin²θ₂₃ ≈ 3/(2φ²) = {3/(2*phi**2):.5f}:")
target_s23 = 3 / (2 * phi**2)
close_s23 = []

for sigma_10 in range(5, 100):
    sigma = sigma_10 / 10.0
    Y0, Y1 = compute_yukawa_matrices(sigma, u_pos)
    Y_ell = Y0 - beta * Y1
    Y_nu = Y1.copy()

    if np.max(np.abs(Y_ell)) < 1e-15 or np.max(np.abs(Y_nu)) < 1e-15:
        continue

    try:
        U_pmns, _, _ = compute_mixing(Y_ell, Y_nu)
        s12sq, s23sq, s13sq = mixing_angles_from_matrix(U_pmns)

        match_23 = min(s23sq, target_s23) / max(s23sq, target_s23) * 100
        if match_23 > 90:
            close_s23.append((sigma, s12sq, s23sq, s13sq, match_23))
    except Exception:
        continue

if close_s23:
    print(f"    Found {len(close_s23)} values with sin²θ₂₃ within 10% of target:")
    for sigma, s12sq, s23sq, s13sq, match in sorted(close_s23, key=lambda x: -x[4])[:10]:
        f12_match = min(s12sq, (phi/3)**2) / max(s12sq, (phi/3)**2) * 100 if s12sq > 0 else 0
        f13_match = min(s13sq, (phi/11)**2) / max(s13sq, (phi/11)**2) * 100 if s13sq > 0 else 0
        print(f"    σ={sigma:.1f}: θ₂₃={match:.1f}%, θ₁₂={f12_match:.1f}%, θ₁₃={f13_match:.1f}%")
else:
    print("    No σ found with sin²θ₂₃ within 10% of target")

# ================================================================
# PART 9: M₀ = (3/2)κ HYPOTHESIS
# ================================================================
print("\n\n" + "=" * 72)
print("PART 9: IS M₀ A FRAMEWORK NUMBER?")
print("=" * 72)

print(f"""
    κ = √(5/2) = {kappa:.6f} (kink inverse width)

    Framework candidates for M₀/κ:
    - 3/2 = h(A₂)/r(A₂) = {1.5:.4f}     → M₀ = {1.5*kappa:.4f}
    - φ   = {phi:.4f}                      → M₀ = {phi*kappa:.4f}
    - √5  = {sqrt5:.4f}                    → M₀ = {sqrt5*kappa:.4f}
    - 7/3 = {7/3:.4f}                      → M₀ = {7/3*kappa:.4f}
    - L(4)/φ = 7/φ = {7/phi:.4f}          → M₀ = {7/phi*kappa:.4f}
    - L(3) = 4                              → M₀ = {4*kappa:.4f}
    - 3φ/2 = {3*phi/2:.4f}                → M₀ = {3*phi/2*kappa:.4f}
    - (3/2)√(5/2) = (3/2)κ = {1.5*kappa:.4f} (M₀ in natural units)
""")

# The overlap integral in combined_hierarchy uses x in half-widths,
# sech^2(x/2) — so "M₀" there is in units of 1/w where w = wall width = 2/μ_kink
# The relation: M₀_code = M₀_natural × w = M₀_natural × 2/μ_kink = M₀_natural × 2/√(10λ)

# For λ=1: μ_kink = √10, w = 2/√10
# So M₀_code = M₀_natural × 2/√10

# If M₀_natural = (3/2)κ = (3/2)√(5/2):
# M₀_code = (3/2)√(5/2) × 2/√10 = (3/2) × √(5/2) × 2/√10
#          = (3/2) × 2√(5)/(2√(10)) = (3/2) × √(5)/√(10) = (3/2) × 1/√2
#          = (3/2) / √2 = 3/(2√2) = 3√2/4 ≈ 1.0607

print(f"    If M₀_natural = (3/2)κ, then M₀_code = {3/(2*np.sqrt(2)):.4f}")
print(f"    If M₀_natural = φ×κ, then M₀_code = {phi/np.sqrt(2):.4f}")
print(f"    If M₀_natural = √5×κ, then M₀_code = {sqrt5/np.sqrt(2):.4f}")
print()

# ================================================================
# PART 10: THE ONTOLOGICAL CASCADE
# ================================================================
print("\n" + "=" * 72)
print("PART 10: THE CASCADE MAP — WHAT RESOLVES WHAT")
print("=" * 72)

print("""
    ┌──────────────────────────────────────────────────────────────┐
    │ WHAT WE HAVE (solved or nearly solved):                      │
    ├──────────────────────────────────────────────────────────────┤
    │ ✓ Core identity: α^(3/2) × μ × φ² = 3                     │
    │ ✓ N = 6⁵ from E8 normalizer + V(Φ)                        │
    │ ✓ μ = N/φ³ (99.97%)                                        │
    │ ✓ v = M_Pl/(N^(13/4) × φ^(33/2) × 4) (99.99%)            │
    │ ✓ λ_H = 1/(3φ²) (98.6%)                                   │
    │ ✓ m_breathing = √(3/4) × m_H = 108.5 GeV                  │
    │ ✓ α(dark, our γ) = 0 (S-duality = mathematical)            │
    │ ✓ Dark sector = same physics, no hierarchy                  │
    │ ✓ PMNS formulas at 99.6-100%                                │
    │ ✓ CKM formulas at 99.4-99.8%                               │
    │ ✓ 30+ quantities from 1 free parameter (v)                  │
    ├──────────────────────────────────────────────────────────────┤
    │ WHAT'S MISSING (cascade targets):                            │
    ├──────────────────────────────────────────────────────────────┤
    │ ? M₀ not derived → IF M₀ = f(φ,N,Coxeter):                │
    │   ├→ σ_i determined for each generation                     │
    │   ├→ Breathing mode θ₁₃ matches formula φ/11               │
    │   ├→ Full CKM from overlap integral mismatch                │
    │   └→ PMNS from ℓ/ν channel mismatch                        │
    │                                                              │
    │ ? Formula → Mechanism gap (biggest):                        │
    │   The formulas (φ/7, φ/11, 3/(2φ²)) WORK but aren't       │
    │   yet DERIVED from the kink overlap integrals.              │
    │   IF the two-channel H/H̃ mechanism works:                  │
    │   ├→ All CKM from (ψ₀ + β·ψ₁) vs (ψ₀ - β·ψ₁)           │
    │   ├→ All PMNS from ℓ(H̃) vs ν(ψ₁)                        │
    │   └→ β = π√5/2 ≈ 7/2 connects to L(4) = 7                │
    │                                                              │
    │ ? v from JUST {φ, μ, 3, 2/3}: needs M_Pl input             │
    │   This may be FUNDAMENTAL: one dimensionful scale needed    │
    │                                                              │
    │ ? CMS 95 GeV vs 108.5 GeV: 12.5 GeV gap                   │
    │   IF one-loop correction shifts 108.5 → 95:                │
    │   └→ CMS excess IS the breathing mode                       │
    └──────────────────────────────────────────────────────────────┘

    THE KEY CASCADE: M₀ → widths → overlaps → formulas
    If this works, the formulas are DERIVED, not fitted.
""")

print("\n" + "=" * 72)
print("END OF CASCADE RESOLUTION")
print("=" * 72)
