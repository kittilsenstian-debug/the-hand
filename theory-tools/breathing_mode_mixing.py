"""
breathing_mode_mixing.py — Cross-wall tunneling via the breathing mode.

The domain wall has exactly 2 bound states (Pöschl-Teller n=2):
  ψ₀(u) ∝ 1/cosh²(u)           — zero mode (even, m²=0)
  ψ₁(u) ∝ sinh(u)/cosh²(u)     — breathing mode (odd, m²=3μ²/4)

Generation positions (from combined_hierarchy.py / e8_sm_embedding.py):
  Gen 3 (τ/t/b): u₃ = +3.0   (light vacuum side)
  Gen 2 (μ/c/s): u₂ = -0.57  (slightly dark side)
  Gen 1 (e/u/d): u₁ = -2.03  (deep dark side)

Key insight: θ₁₃ and V_td require cross-wall tunneling (Gen 1 on dark side
↔ Gen 3 on light side). The breathing mode ψ₁ is the ONLY bound state that
bridges both vacua (it's antisymmetric, with lobes on each side).

This script:
  1. Decomposes the kink into bound state modes → c₀, c₁
  2. Computes the Yukawa overlap matrix Y_ij in the factorized form
  3. Extracts mixing angles from diagonalization
  4. Shows breathing mode dominance for cross-wall mixing
  5. Compares to measured PMNS and CKM angles

Usage:
    python theory-tools/breathing_mode_mixing.py
"""

import numpy as np
from scipy import integrate, linalg
import sys

if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

phi = (1 + 5**0.5) / 2
sqrt5 = 5**0.5

# Generation positions in Pöschl-Teller variable u = μx/2
u_gen = np.array([-2.03, -0.57, 3.0])  # Gen 1, Gen 2, Gen 3
gen_labels = ["Gen 1 (e/u/d)", "Gen 2 (μ/c/s)", "Gen 3 (τ/t/b)"]

# Measured mixing angles
PMNS_measured = {
    'theta_12': 33.44,   # degrees (solar)
    'theta_23': 49.2,    # degrees (atmospheric)
    'theta_13': 8.57,    # degrees (reactor)
    'sin2_13':  0.0220,  # sin²θ₁₃
}

CKM_measured = {
    'V_us': 0.2253,  # |V_us| ≈ sin θ_C
    'V_cb': 0.0405,  # |V_cb|
    'V_ub': 0.00382, # |V_ub|
    'V_td': 0.0086,  # |V_td|
    'theta_12': 13.04,   # degrees (Cabibbo)
    'theta_23': 2.38,    # degrees
    'theta_13': 0.201,   # degrees
}

print("=" * 72)
print("BREATHING MODE MIXING: CROSS-WALL TUNNELING AMPLITUDES")
print("=" * 72)


# ================================================================
# SECTION 1: Kink and bound state wavefunctions
# ================================================================
print("\n[1] Domain wall physics setup")
print("-" * 72)

def kink_profile(u):
    """Scalar field kink: Φ(u) = (√5/2)tanh(u) + 1/2"""
    return sqrt5/2 * np.tanh(u) + 0.5

def higgs_profile(u):
    """Higgs/kink derivative: H(u) = dΦ/du = (√5/2)sech²(u)"""
    return sqrt5/2 / np.cosh(u)**2

def psi_0(u):
    """Zero mode (even bound state): sech²(u)"""
    return 1.0 / np.cosh(u)**2

def psi_1(u):
    """Breathing mode (odd bound state): sinh(u)/cosh²(u)"""
    return np.sinh(u) / np.cosh(u)**2

# Normalization integrals
norm2_0 = integrate.quad(lambda u: psi_0(u)**2, -30, 30)[0]
norm2_1 = integrate.quad(lambda u: psi_1(u)**2, -30, 30)[0]

print(f"    Pöschl-Teller n=2: exactly 2 bound states")
print(f"    ||ψ₀||² = {norm2_0:.6f}    (analytic: 4/3 = {4/3:.6f})")
print(f"    ||ψ₁||² = {norm2_1:.6f}    (analytic: 2/3 = {2/3:.6f})")

# Evaluate at generation positions
print(f"\n    Bound state values at generation positions:")
print(f"    {'Gen':>8}  {'u_i':>8}  {'ψ₀(u_i)':>12}  {'ψ₁(u_i)':>12}  {'side':>8}")
print(f"    {'---':>8}  {'---':>8}  {'---':>12}  {'---':>12}  {'---':>8}")
for i, u in enumerate(u_gen):
    p0 = psi_0(u)
    p1 = psi_1(u)
    side = "dark" if u < 0 else "light"
    print(f"    {gen_labels[i]:>28}  u={u:>+6.2f}  ψ₀={p0:>9.6f}  ψ₁={p1:>+10.6f}  [{side}]")

print(f"\n    Key observation: ψ₁ has OPPOSITE SIGNS on dark vs light side")
print(f"    Gen 1 (dark):  ψ₁ = {psi_1(u_gen[0]):+.4f}")
print(f"    Gen 3 (light): ψ₁ = {psi_1(u_gen[2]):+.4f}")
print(f"    Breathing mode BRIDGES both vacua!")


# ================================================================
# SECTION 2: Decompose kink into bound states
# ================================================================
print(f"\n\n[2] Kink profile decomposition into bound states")
print("-" * 72)

# c₀ = ⟨ψ₀|Φ_kink⟩ / ||ψ₀||²
c0_num = integrate.quad(lambda u: psi_0(u) * kink_profile(u), -30, 30)[0]
c0 = c0_num / norm2_0

# c₁ = ⟨ψ₁|Φ_kink⟩ / ||ψ₁||²
c1_num = integrate.quad(lambda u: psi_1(u) * kink_profile(u), -30, 30)[0]
c1 = c1_num / norm2_1

# Continuum residual
def residual2(u):
    approx = c0 * psi_0(u) + c1 * psi_1(u)
    return (kink_profile(u) - approx)**2

resid_norm = integrate.quad(residual2, -30, 30, limit=200)[0]
kink_norm2 = integrate.quad(lambda u: kink_profile(u)**2, -30, 30, limit=200)[0]

print(f"    Φ_kink(u) = c₀·ψ₀(u) + c₁·ψ₁(u) + continuum")
print(f"")
print(f"    c₀ = {c0:.6f}   (even: picks up the constant part 1/2)")
print(f"    c₁ = {c1:.6f}   (odd: picks up the tanh part)")
print(f"")
print(f"    Continuum fraction: {resid_norm/kink_norm2*100:.1f}% of ||Φ||²")
print(f"    (The kink is mostly continuum — extends beyond the bound states)")
print(f"")
print(f"    Ratio c₁/c₀ = {c1/c0:.6f}")

# Analytical derivation:
# c₀ = (1/2)·∫sech²du / ∫sech⁴du = (1/2)·2 / (4/3) = 3/4
# c₁ = (√5/2)·∫sinh·sech²·tanh du / ∫(sinh·sech²)²du
#    = (√5/2)·(π/2) / (2/3) = 3π√5/8
# c₁/c₀ = (3π√5/8)/(3/4) = π√5/2  EXACTLY
c0_exact = 3.0 / 4
c1_exact = 3 * np.pi * sqrt5 / 8
print(f"    (Analytical c₀ = 3/4 = {c0_exact:.6f})")
print(f"    (Analytical c₁ = 3π√5/8 = {c1_exact:.6f})")
print(f"    (Analytical c₁/c₀ = π√5/2 = {np.pi*sqrt5/2:.6f})")
print(f"")
print(f"    ** c₁/c₀ = π√5/2 ≈ 7/2 = L(4)/2 with {min(np.pi*sqrt5/2, 3.5)/max(np.pi*sqrt5/2, 3.5)*100:.2f}% accuracy **")
print(f"    (L(4) = 7 is the 4th Lucas number = Coxeter exponent of E8 that breaks S3)")


# ================================================================
# SECTION 3: Factorized Yukawa matrix (parameter-free)
# ================================================================
print(f"\n\n[3] Factorized Yukawa matrix: Y_ij = c₀·ψ₀(uᵢ)·ψ₀(uⱼ) + c₁·ψ₁(uᵢ)·ψ₁(uⱼ)")
print("-" * 72)

# Wavefunction vectors at generation positions
a = np.array([psi_0(u) for u in u_gen])  # zero mode values
b = np.array([psi_1(u) for u in u_gen])  # breathing mode values

# Zero-mode contribution
Y0 = c0 * np.outer(a, a)
# Breathing mode contribution
Y1 = c1 * np.outer(b, b)
# Total (bound state only)
Y_bs = Y0 + Y1

print(f"    Zero-mode contribution Y⁰_ij = c₀·ψ₀(uᵢ)·ψ₀(uⱼ):")
for i in range(3):
    row = "    "
    for j in range(3):
        row += f"  {Y0[i,j]:>12.6e}"
    print(row)

print(f"\n    Breathing mode contribution Y¹_ij = c₁·ψ₁(uᵢ)·ψ₁(uⱼ):")
for i in range(3):
    row = "    "
    for j in range(3):
        row += f"  {Y1[i,j]:>12.6e}"
    print(row)

print(f"\n    Total (bound states) Y_ij = Y⁰ + Y¹:")
for i in range(3):
    row = "    "
    for j in range(3):
        row += f"  {Y_bs[i,j]:>12.6e}"
    print(row)

# Ratio: breathing mode / zero mode for each element
print(f"\n    Breathing-to-zero-mode ratio R_ij = Y¹_ij / Y⁰_ij:")
for i in range(3):
    row = "    "
    for j in range(3):
        if abs(Y0[i,j]) > 1e-20:
            r = Y1[i,j] / Y0[i,j]
            row += f"  {r:>12.4f}"
        else:
            row += f"  {'inf':>12}"
    print(row)


# ================================================================
# SECTION 4: Cross-wall analysis
# ================================================================
print(f"\n\n[4] Cross-wall tunneling amplitudes")
print("-" * 72)

print(f"    For mixing between generations i and j:")
print(f"    Direct (zero mode):     Y⁰_ij = c₀·ψ₀(uᵢ)·ψ₀(uⱼ)  [even × even = even]")
print(f"    Breathing mode:         Y¹_ij = c₁·ψ₁(uᵢ)·ψ₁(uⱼ)  [odd × odd = even]")
print(f"")

pairs = [(0, 1, "1-2 (same side, dark)"),
         (1, 2, "2-3 (near wall ↔ light)"),
         (0, 2, "1-3 (CROSS-WALL: dark ↔ light)")]

for i, j, desc in pairs:
    y0 = Y0[i, j]
    y1 = Y1[i, j]
    y_tot = y0 + y1
    print(f"    {desc}:")
    print(f"      Zero mode:     {y0:>12.6e}")
    print(f"      Breathing:     {y1:>12.6e}")
    print(f"      Total:         {y_tot:>12.6e}")
    if abs(y0) > 1e-20:
        print(f"      Breath/Zero:   {y1/y0:>12.4f}x")
    print()

print(f"    ** The (1,3) cross-wall element is DOMINATED by the breathing mode **")
print(f"    ** because ψ₀ decays exponentially on both sides, while ψ₁ extends to both **")


# ================================================================
# SECTION 5: Mixing angles from factorized matrix
# ================================================================
print(f"\n\n[5] Mixing angles from Y_bs eigenstructure")
print("-" * 72)

def extract_angles_from_U(U):
    """Extract mixing angles from a 3x3 unitary/orthogonal matrix.
    Standard parameterization: U = R23·R13·R12
    sin θ₁₃ = |U[0,2]|
    tan θ₁₂ = |U[0,1]/U[0,0]|
    tan θ₂₃ = |U[1,2]/U[2,2]|
    """
    s13 = min(abs(U[0, 2]), 1.0)
    t13 = np.degrees(np.arcsin(s13))

    if abs(U[0, 0]) > 1e-10:
        t12 = np.degrees(np.arctan(abs(U[0, 1] / U[0, 0])))
    else:
        t12 = 90.0

    if abs(U[2, 2]) > 1e-10:
        t23 = np.degrees(np.arctan(abs(U[1, 2] / U[2, 2])))
    else:
        t23 = 90.0

    return t12, t23, t13

# The factorized matrix Y_bs is rank-2 (at most), so it has at most 2 nonzero eigenvalues.
# This means one generation is massless in this approximation.
eigenvalues_bs, U_bs = linalg.eigh(Y_bs)

# Sort by magnitude (ascending): lightest first
idx = np.argsort(np.abs(eigenvalues_bs))
eigenvalues_bs = eigenvalues_bs[idx]
U_bs = U_bs[:, idx]

print(f"    Eigenvalues of Y_bs:")
for i in range(3):
    print(f"      λ_{i+1} = {eigenvalues_bs[i]:>12.6e}")

print(f"\n    Eigenvector matrix U (columns = mass eigenstates):")
for i in range(3):
    row = "    "
    for j in range(3):
        row += f"  {U_bs[i,j]:>10.6f}"
    print(row)

t12_bs, t23_bs, t13_bs = extract_angles_from_U(U_bs)
print(f"\n    Mixing angles (bound-state factorized):")
print(f"      θ₁₂ = {t12_bs:.2f}°")
print(f"      θ₂₃ = {t23_bs:.2f}°")
print(f"      θ₁₃ = {t13_bs:.2f}°")
print(f"      sin²θ₁₃ = {np.sin(np.radians(t13_bs))**2:.6f}")

print(f"\n    Comparison to PMNS (if this were the lepton sector):")
print(f"      θ₁₃: predicted {t13_bs:.2f}° vs measured {PMNS_measured['theta_13']:.2f}°")


# ================================================================
# SECTION 6: Gaussian-profile overlap integrals
# ================================================================
print(f"\n\n[6] Full overlap integrals with Gaussian fermion profiles")
print("-" * 72)

def fermion_gaussian(u, u_center, sigma):
    """Normalized Gaussian fermion profile"""
    return np.exp(-(u - u_center)**2 / (2 * sigma**2)) / (np.sqrt(2 * np.pi) * sigma)**0.5

def compute_yukawa_matrix(sigma, kernel_func):
    """Compute 3x3 Yukawa overlap matrix with given kernel and profile width"""
    Y = np.zeros((3, 3))
    for i in range(3):
        for j in range(i, 3):
            def integrand(u):
                fi = fermion_gaussian(u, u_gen[i], sigma)
                fj = fermion_gaussian(u, u_gen[j], sigma)
                return fi * kernel_func(u) * fj
            Y[i, j], _ = integrate.quad(integrand, -30, 30, limit=200)
            Y[j, i] = Y[i, j]
    return Y

def compute_yukawa_decomposed(sigma):
    """Compute Yukawa matrix decomposed into zero mode + breathing mode + full"""
    Y_zero = compute_yukawa_matrix(sigma, lambda u: c0 * psi_0(u))
    Y_breath = compute_yukawa_matrix(sigma, lambda u: c1 * psi_1(u))
    Y_kink = compute_yukawa_matrix(sigma, kink_profile)
    Y_higgs = compute_yukawa_matrix(sigma, higgs_profile)
    return Y_zero, Y_breath, Y_kink, Y_higgs

print(f"    Scanning fermion profile width σ...")
print(f"    (σ controls localization: small σ → narrow profiles, large σ → wide)")
print(f"")

# Key scan: find σ that gives physically reasonable mixing
print(f"    {'σ':>6}  {'θ₁₂':>8}  {'θ₂₃':>8}  {'θ₁₃':>8}  {'sin²θ₁₃':>10}  {'m₃/m₂':>8}  {'m₂/m₁':>8}")
print(f"    {'---':>6}  {'---':>8}  {'---':>8}  {'---':>8}  {'---':>10}  {'---':>8}  {'---':>8}")

sigma_scan = np.concatenate([
    np.arange(0.3, 1.0, 0.1),
    np.arange(1.0, 3.0, 0.25),
    np.arange(3.0, 6.0, 0.5),
])

best_sigma = None
best_t13_err = float('inf')

for sigma in sigma_scan:
    Y_kink = compute_yukawa_matrix(sigma, kink_profile)
    evals, evecs = linalg.eigh(Y_kink)
    idx = np.argsort(np.abs(evals))
    evals = evals[idx]
    evecs = evecs[:, idx]

    t12, t23, t13 = extract_angles_from_U(evecs)
    s2_13 = np.sin(np.radians(t13))**2

    m_sorted = np.sort(np.abs(evals))
    r32 = m_sorted[2] / m_sorted[1] if m_sorted[1] > 1e-15 else 999
    r21 = m_sorted[1] / m_sorted[0] if m_sorted[0] > 1e-15 else 999

    print(f"    {sigma:>6.2f}  {t12:>8.2f}  {t23:>8.2f}  {t13:>8.2f}  {s2_13:>10.6f}  {r32:>8.1f}  {r21:>8.1f}")

    t13_err = abs(t13 - PMNS_measured['theta_13'])
    if t13_err < best_t13_err:
        best_t13_err = t13_err
        best_sigma = sigma


# ================================================================
# SECTION 7: Detailed analysis at best σ
# ================================================================
print(f"\n\n[7] Detailed analysis at σ = {best_sigma:.2f} (best θ₁₃ match)")
print("-" * 72)

Y_zero, Y_breath, Y_kink, Y_higgs = compute_yukawa_decomposed(best_sigma)

print(f"    Zero-mode Yukawa matrix (Y⁰):")
for i in range(3):
    row = "      "
    for j in range(3):
        row += f"  {Y_zero[i,j]:>12.6e}"
    print(row)

print(f"\n    Breathing-mode Yukawa matrix (Y¹):")
for i in range(3):
    row = "      "
    for j in range(3):
        row += f"  {Y_breath[i,j]:>12.6e}"
    print(row)

print(f"\n    Full kink-profile Yukawa matrix (Y_kink):")
for i in range(3):
    row = "      "
    for j in range(3):
        row += f"  {Y_kink[i,j]:>12.6e}"
    print(row)

print(f"\n    Higgs-derivative Yukawa matrix (Y_higgs = ∫f_i·H·f_j):")
for i in range(3):
    row = "      "
    for j in range(3):
        row += f"  {Y_higgs[i,j]:>12.6e}"
    print(row)

# Decomposed contributions for the cross-wall element Y_13
y0_13 = Y_zero[0, 2]
y1_13 = Y_breath[0, 2]
yk_13 = Y_kink[0, 2]

print(f"\n    Cross-wall element Y(1,3):")
print(f"      Zero-mode contribution:     {y0_13:>12.6e}")
print(f"      Breathing-mode contribution: {y1_13:>12.6e}")
print(f"      Full kink contribution:      {yk_13:>12.6e}")
if abs(y0_13) > 1e-20:
    print(f"      Breathing/Zero ratio:        {y1_13/y0_13:>12.4f}x")
print(f"      Breathing fraction of total: {abs(y1_13)/abs(yk_13)*100:.1f}%" if abs(yk_13) > 1e-20 else "")

# Mixing angles from full kink Yukawa
evals_k, evecs_k = linalg.eigh(Y_kink)
idx = np.argsort(np.abs(evals_k))
evals_k = evals_k[idx]
evecs_k = evecs_k[:, idx]
t12_k, t23_k, t13_k = extract_angles_from_U(evecs_k)

print(f"\n    Mixing angles from full kink Yukawa:")
print(f"      θ₁₂ = {t12_k:.2f}°   (PMNS: {PMNS_measured['theta_12']:.2f}°, CKM: {CKM_measured['theta_12']:.2f}°)")
print(f"      θ₂₃ = {t23_k:.2f}°   (PMNS: {PMNS_measured['theta_23']:.2f}°, CKM: {CKM_measured['theta_23']:.2f}°)")
print(f"      θ₁₃ = {t13_k:.2f}°   (PMNS: {PMNS_measured['theta_13']:.2f}°, CKM: {CKM_measured['theta_13']:.2f}°)")
print(f"      sin²θ₁₃ = {np.sin(np.radians(t13_k))**2:.6f}   (measured: {PMNS_measured['sin2_13']:.4f})")


# ================================================================
# SECTION 8: What if we use the Higgs derivative as kernel?
# ================================================================
print(f"\n\n[8] Mixing from Higgs derivative kernel H(u) = dΦ/du")
print("-" * 72)

print(f"    The Higgs profile H(u) = (√5/2)·sech²(u) IS the zero mode ψ₀.")
print(f"    Using H as kernel should give zero-mode-only mixing (no cross-wall).")
print(f"")

evals_h, evecs_h = linalg.eigh(Y_higgs)
idx = np.argsort(np.abs(evals_h))
evals_h = evals_h[idx]
evecs_h = evecs_h[:, idx]
t12_h, t23_h, t13_h = extract_angles_from_U(evecs_h)

print(f"    Mixing angles from Higgs-derivative kernel:")
print(f"      θ₁₂ = {t12_h:.2f}°")
print(f"      θ₂₃ = {t23_h:.2f}°")
print(f"      θ₁₃ = {t13_h:.2f}°")
print(f"")
print(f"    With kink profile (includes breathing mode): θ₁₃ = {t13_k:.2f}°")
print(f"    With Higgs derivative (zero mode only):      θ₁₃ = {t13_h:.2f}°")
print(f"    Difference from breathing mode:              Δθ₁₃ = {abs(t13_k - t13_h):.2f}°")


# ================================================================
# SECTION 9: Scan for position dependence
# ================================================================
print(f"\n\n[9] Position sensitivity: which positions give θ₁₃ ≈ 8.57°?")
print("-" * 72)

print(f"    Fixing Gen 2 at u₂ = -0.57, scanning Gen 1 and Gen 3 positions")
print(f"    with σ = {best_sigma:.2f}")
print(f"")
print(f"    {'u₁':>6}  {'u₃':>6}  {'θ₁₃':>8}  {'sin²θ₁₃':>10}  {'θ₁₂':>8}  {'θ₂₃':>8}")
print(f"    {'---':>6}  {'---':>6}  {'---':>8}  {'---':>10}  {'---':>8}  {'---':>8}")

best_pos_err = float('inf')
best_pos = None

for u1_10 in range(-35, -5, 5):
    u1 = u1_10 / 10.0
    for u3_10 in range(10, 50, 5):
        u3 = u3_10 / 10.0
        u_test = np.array([u1, -0.57, u3])

        Y_test = np.zeros((3, 3))
        for i in range(3):
            for j in range(i, 3):
                def integrand(u, ii=i, jj=j):
                    fi = fermion_gaussian(u, u_test[ii], best_sigma)
                    fj = fermion_gaussian(u, u_test[jj], best_sigma)
                    return fi * kink_profile(u) * fj
                Y_test[i, j], _ = integrate.quad(integrand, -30, 30, limit=200)
                Y_test[j, i] = Y_test[i, j]

        evals_t, evecs_t = linalg.eigh(Y_test)
        idx_t = np.argsort(np.abs(evals_t))
        evecs_t = evecs_t[:, idx_t]
        t12_t, t23_t, t13_t = extract_angles_from_U(evecs_t)
        s2_13 = np.sin(np.radians(t13_t))**2

        err = abs(t13_t - PMNS_measured['theta_13'])
        if err < best_pos_err:
            best_pos_err = err
            best_pos = (u1, u3)

        # Only print points near target
        if abs(t13_t - PMNS_measured['theta_13']) < 5.0:
            print(f"    {u1:>+6.1f}  {u3:>+6.1f}  {t13_t:>8.2f}  {s2_13:>10.6f}  {t12_t:>8.2f}  {t23_t:>8.2f}")

if best_pos:
    print(f"\n    Best match: u₁ = {best_pos[0]:.1f}, u₃ = {best_pos[1]:.1f}")


# ================================================================
# SECTION 10: Breathing mode amplitude analysis
# ================================================================
print(f"\n\n[10] Breathing mode amplitude: why θ₁₃ is special")
print("-" * 72)

print(f"    The breathing mode ψ₁(u) = sinh(u)/cosh²(u) has these properties:")
print(f"    - Antisymmetric: ψ₁(-u) = -ψ₁(u)")
print(f"    - Zero at wall center: ψ₁(0) = 0")
print(f"    - Peak at u ≈ ±0.66")
print(f"    - Extends to both sides (decays as ~2·exp(-|u|) for large |u|)")
print(f"")

# Compute the breathing mode "tunneling amplitude" T_ij
# T_ij = ψ₁(u_i) · ψ₁(u_j) — the product of breathing mode values
print(f"    Breathing mode tunneling products ψ₁(uᵢ)·ψ₁(uⱼ):")
for i in range(3):
    for j in range(i, 3):
        t = psi_1(u_gen[i]) * psi_1(u_gen[j])
        z = psi_0(u_gen[i]) * psi_0(u_gen[j])
        sign = "same-side" if t > 0 else "CROSS-WALL"
        ratio = abs(t/z) if abs(z) > 1e-20 else float('inf')
        print(f"    ({i+1},{j+1}): ψ₁·ψ₁ = {t:>+12.6e}, ψ₀·ψ₀ = {z:>12.6e}, |T/Z| = {ratio:>8.2f}  [{sign}]")

print(f"\n    Cross-wall amplitude ψ₁(u₁)·ψ₁(u₃) is NEGATIVE")
print(f"    because Gen 1 (dark side) and Gen 3 (light side) have opposite ψ₁ signs.")
print(f"    This generates the CP-violating phase (if complex couplings).")


# ================================================================
# SECTION 11: Physical interpretation
# ================================================================
print(f"\n\n[11] Physical interpretation")
print("-" * 72)

# Compare zero mode and breathing mode "reach"
u_points = np.linspace(-5, 5, 201)
psi0_vals = np.array([psi_0(u) for u in u_points])
psi1_vals = np.array([abs(psi_1(u)) for u in u_points])

# Find where |ψ₁| > ψ₀
crossover = None
for k in range(len(u_points)):
    if abs(u_points[k]) > 0.5 and psi1_vals[k] > psi0_vals[k]:
        if crossover is None:
            crossover = abs(u_points[k])

if crossover:
    print(f"    Breathing mode dominates over zero mode for |u| > {crossover:.2f}")
else:
    print(f"    Breathing mode overtakes zero mode at moderate distances")

print(f"")
print(f"    Gen 1 at u₁ = {u_gen[0]:+.2f}:  ψ₀ = {psi_0(u_gen[0]):.6f},  |ψ₁| = {abs(psi_1(u_gen[0])):.6f}")
print(f"    Gen 3 at u₃ = {u_gen[2]:+.2f}:  ψ₀ = {psi_0(u_gen[2]):.6f},  |ψ₁| = {abs(psi_1(u_gen[2])):.6f}")
print(f"")
print(f"    At Gen 1 position: |ψ₁|/ψ₀ = {abs(psi_1(u_gen[0]))/psi_0(u_gen[0]):.2f}")
print(f"    At Gen 3 position: |ψ₁|/ψ₀ = {abs(psi_1(u_gen[2]))/psi_0(u_gen[2]):.2f}")
print(f"")
print(f"    RESULT: At generation positions far from the wall center,")
print(f"    the breathing mode has 4-10x more amplitude than the zero mode.")
print(f"    Cross-wall mixing is BREATHING-MODE DOMINATED.")


# ================================================================
# SECTION 12: Effective mixing ratio prediction
# ================================================================
print(f"\n\n[12] Effective mixing ratio: θ₁₃/θ₁₂ prediction")
print("-" * 72)

# The ratio θ₁₃/θ₁₂ is particularly clean because it doesn't depend on
# the overall coupling or the fermion profile width.
# In the factorized form:
# sin θ₁₃ ∝ Y_13 = c₀·a₁·a₃ + c₁·b₁·b₃
# sin θ₁₂ ∝ Y_12 = c₀·a₁·a₂ + c₁·b₁·b₂

Y_13_fact = c0 * psi_0(u_gen[0]) * psi_0(u_gen[2]) + c1 * psi_1(u_gen[0]) * psi_1(u_gen[2])
Y_12_fact = c0 * psi_0(u_gen[0]) * psi_0(u_gen[1]) + c1 * psi_1(u_gen[0]) * psi_1(u_gen[1])
Y_23_fact = c0 * psi_0(u_gen[1]) * psi_0(u_gen[2]) + c1 * psi_1(u_gen[1]) * psi_1(u_gen[2])

print(f"    Factorized off-diagonal Yukawa elements:")
print(f"    Y₁₂ = {Y_12_fact:>+12.6e}   (Gen 1-2, same side)")
print(f"    Y₂₃ = {Y_23_fact:>+12.6e}   (Gen 2-3, near↔light)")
print(f"    Y₁₃ = {Y_13_fact:>+12.6e}   (Gen 1-3, CROSS-WALL)")
print(f"")

# Ratios
if abs(Y_12_fact) > 1e-20 and abs(Y_23_fact) > 1e-20:
    r_13_12 = abs(Y_13_fact / Y_12_fact)
    r_13_23 = abs(Y_13_fact / Y_23_fact)
    print(f"    |Y₁₃/Y₁₂| = {r_13_12:.4f}")
    print(f"    |Y₁₃/Y₂₃| = {r_13_23:.4f}")
    print(f"")

    # Compare to measured ratios
    pmns_r = np.sin(np.radians(PMNS_measured['theta_13'])) / np.sin(np.radians(PMNS_measured['theta_12']))
    ckm_r = CKM_measured['V_ub'] / CKM_measured['V_us']
    print(f"    Measured |sin θ₁₃/sin θ₁₂| (PMNS) = {pmns_r:.4f}")
    print(f"    Measured |V_ub/V_us| (CKM)         = {ckm_r:.4f}")
    print(f"")
    print(f"    Predicted ratio {r_13_12:.4f} vs PMNS {pmns_r:.4f}: {min(r_13_12,pmns_r)/max(r_13_12,pmns_r)*100:.1f}%")


# ================================================================
# SECTION 13: The breathing mode as sin²θ₁₃ predictor
# ================================================================
print(f"\n\n[13] Direct sin²θ₁₃ prediction from breathing mode")
print("-" * 72)

# In perturbation theory, for a Yukawa matrix Y with diagonal entries much
# larger than off-diagonal:
# sin θ₁₃ ≈ Y_13 / Y_33  (when Y_33 >> Y_11)
# This gives a PARAMETER-FREE prediction.

Y_13_f = Y_13_fact
Y_33_f = c0 * psi_0(u_gen[2])**2 + c1 * psi_1(u_gen[2])**2
Y_11_f = c0 * psi_0(u_gen[0])**2 + c1 * psi_1(u_gen[0])**2
Y_22_f = c0 * psi_0(u_gen[1])**2 + c1 * psi_1(u_gen[1])**2

print(f"    Factorized diagonal elements:")
print(f"    Y₁₁ = {Y_11_f:>12.6e}")
print(f"    Y₂₂ = {Y_22_f:>12.6e}")
print(f"    Y₃₃ = {Y_33_f:>12.6e}")
print(f"")
print(f"    Off-diagonal Y₁₃ = {Y_13_f:>12.6e}")
print(f"")

if abs(Y_33_f) > 1e-20:
    s13_pred = abs(Y_13_f / Y_33_f)
    s13_sq_pred = s13_pred**2
    t13_pred_deg = np.degrees(np.arcsin(min(s13_pred, 1.0)))

    print(f"    Perturbative prediction:")
    print(f"    sin θ₁₃ ≈ |Y₁₃/Y₃₃| = {s13_pred:.6f}")
    print(f"    sin²θ₁₃ = {s13_sq_pred:.6f}")
    print(f"    θ₁₃ = {t13_pred_deg:.2f}°")
    print(f"")
    print(f"    Measured sin²θ₁₃ = {PMNS_measured['sin2_13']:.4f} → θ₁₃ = {PMNS_measured['theta_13']:.2f}°")
    print(f"    Match: {min(s13_sq_pred, PMNS_measured['sin2_13'])/max(s13_sq_pred, PMNS_measured['sin2_13'])*100:.1f}%")


# ================================================================
# SECTION 14: CKM vs PMNS from same mechanism
# ================================================================
print(f"\n\n[14] CKM vs PMNS: same wall, different coupling ratios")
print("-" * 72)

print(f"    CKM and PMNS come from the SAME domain wall.")
print(f"    The difference: quarks and leptons have different 5D couplings.")
print(f"    CKM = V_u† · V_d, PMNS = V_e† · V_ν")
print(f"")
print(f"    The breathing mode ratio c₁/c₀ = {c1/c0:.6f}")
print(f"    sets the UNIVERSAL cross-wall tunneling probability.")
print(f"")
print(f"    Sector-specific mixing depends on the mismatch between")
print(f"    up-type and down-type (or charged lepton and neutrino) profiles.")
print(f"")
print(f"    Key prediction: the RATIO of CKM to PMNS angles should be")
print(f"    determined by the Casimir coupling difference between sectors.")

# CKM θ₁₃ = 0.201° vs PMNS θ₁₃ = 8.57°
# Ratio: 8.57/0.201 = 42.6
# Is this a framework number?
ratio_pmns_ckm = PMNS_measured['theta_13'] / CKM_measured['theta_13']
print(f"\n    θ₁₃(PMNS) / θ₁₃(CKM) = {ratio_pmns_ckm:.1f}")
for name, val in [("phi^6/2", phi**6/2), ("φ⁵", phi**5), ("7*φ²", 7*phi**2),
                   ("3*φ⁴", 3*phi**4), ("μ^(1/5)", 1836.15**0.2),
                   ("42", 42.0), ("6^2", 36.0), ("phi^7/3", phi**7/3),
                   ("L(8)/2", 47/2)]:
    match = min(ratio_pmns_ckm, val) / max(ratio_pmns_ckm, val) * 100
    if match > 90:
        print(f"    {ratio_pmns_ckm:.1f} ≈ {name} = {val:.1f} ({match:.1f}%)")


# ================================================================
# SECTION 15: Summary
# ================================================================
print(f"\n\n{'='*72}")
print(f"SUMMARY: BREATHING MODE CROSS-WALL MIXING")
print(f"{'='*72}")

print(f"""
    MECHANISM:
    The domain wall has 2 bound states:
    - Zero mode ψ₀ (even): mediates same-side coupling
    - Breathing mode ψ₁ (odd): mediates cross-wall tunneling

    GENERATION POSITIONS:
    Gen 1 at u = -2.03 (dark side)    → ψ₁/ψ₀ = {abs(psi_1(u_gen[0]))/psi_0(u_gen[0]):.1f}x
    Gen 2 at u = -0.57 (near center)  → ψ₁/ψ₀ = {abs(psi_1(u_gen[1]))/psi_0(u_gen[1]):.1f}x
    Gen 3 at u = +3.00 (light side)   → ψ₁/ψ₀ = {abs(psi_1(u_gen[2]))/psi_0(u_gen[2]):.1f}x

    KEY RESULT:
    At the generation positions, the breathing mode has {abs(psi_1(u_gen[0]))/psi_0(u_gen[0]):.0f}-{abs(psi_1(u_gen[2]))/psi_0(u_gen[2]):.0f}x
    more amplitude than the zero mode.

    Cross-wall mixing (θ₁₃) is DOMINATED by the breathing mode.
    Same-side mixing (θ₁₂) uses both modes.

    The breathing mode provides the physical mechanism for
    ALL cross-wall mixing: θ₁₃(PMNS), V_ub, V_td (CKM).

    KINK DECOMPOSITION:
    c₀ = {c0:.4f} (zero mode weight)
    c₁ = {c1:.4f} (breathing mode weight)
    c₁/c₀ = {c1/c0:.4f}
""")

print("=" * 72)
print("END OF BREATHING MODE MIXING ANALYSIS")
print("=" * 72)
