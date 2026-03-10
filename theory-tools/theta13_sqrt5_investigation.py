"""
theta13_sqrt5_investigation.py — Can a sqrt(5) correction improve theta_13?

Context from FINDINGS-v2.md section 124 (insight 6):
"Every cross-wall quantity picks up explicit sqrt(5): Lambda, the alpha
correction, c_1/c_0 = pi*sqrt(5)/2. The current theta_13 calculation
(85.7%) does not include sqrt(5). Adding the appropriate sqrt(5)-dependent
correction may improve this weakest match."

This script systematically investigates structurally motivated sqrt(5)
modifications to the theta_13 calculation:

1. The baseline: sin^2(theta_13) = 0.0257 at sigma=3 (85.7% match)
2. Modification A: sigma = sqrt(5) * something
3. Modification B: cross-wall amplitude * sqrt(5) factor
4. Modification C: position separation with sqrt(5) correction
5. Modification D: kink profile with explicit sqrt(5) normalization
6. Modification E: combined breathing mode + sqrt(5) overlap

Measured: sin^2(theta_13) = 0.02200 +/- 0.00069

Usage:
    python theory-tools/theta13_sqrt5_investigation.py
"""

import numpy as np
from scipy import integrate, linalg
import sys

if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

phi = (1 + 5**0.5) / 2
phibar = 1 / phi
sqrt5 = 5**0.5
pi = np.pi

# Generation positions (from e8_sm_embedding.py)
u_gen = np.array([-2.03, -0.57, 3.0])  # Gen 1, Gen 2, Gen 3

# Measured
sin2_13_measured = 0.02200
sin2_13_err = 0.00069

print("=" * 76)
print("THETA_13 SQRT(5) INVESTIGATION")
print("Can a structurally motivated sqrt(5) correction improve the 85.7% match?")
print("=" * 76)


# ================================================================
# BASELINE FUNCTIONS
# ================================================================

def psi_0(u):
    """Zero mode: sech^2(u)"""
    return 1.0 / np.cosh(u)**2

def psi_1(u):
    """Breathing mode: sinh(u)/cosh^2(u)"""
    return np.sinh(u) / np.cosh(u)**2

def kink_profile(u):
    """Kink: (sqrt(5)/2)*tanh(u) + 1/2"""
    return sqrt5/2 * np.tanh(u) + 0.5

def higgs_profile(u):
    """Higgs derivative: (sqrt(5)/2)*sech^2(u)"""
    return sqrt5/2 / np.cosh(u)**2

# Analytical decomposition coefficients
c0 = 3.0 / 4          # zero mode weight
c1 = 3*pi*sqrt5 / 8   # breathing mode weight

# Verify
norm2_0 = integrate.quad(lambda u: psi_0(u)**2, -30, 30)[0]
norm2_1 = integrate.quad(lambda u: psi_1(u)**2, -30, 30)[0]
c0_num = integrate.quad(lambda u: psi_0(u) * kink_profile(u), -30, 30)[0] / norm2_0
c1_num = integrate.quad(lambda u: psi_1(u) * kink_profile(u), -30, 30)[0] / norm2_1

print(f"\n    Baseline parameters:")
print(f"    c_0 = {c0:.6f}  (verified: {c0_num:.6f})")
print(f"    c_1 = {c1:.6f}  (verified: {c1_num:.6f})")
print(f"    c_1/c_0 = pi*sqrt(5)/2 = {c1/c0:.6f}")
print(f"    Positions: u_1={u_gen[0]}, u_2={u_gen[1]}, u_3={u_gen[2]}")


def fermion_gaussian(u, u_center, sigma):
    """Normalized Gaussian fermion profile"""
    return np.exp(-(u - u_center)**2 / (2 * sigma**2)) / (np.sqrt(2 * pi) * sigma)**0.5


def compute_sin2_13(sigma, kernel_func, positions=None):
    """Compute sin^2(theta_13) for given sigma, kernel, and positions."""
    if positions is None:
        positions = u_gen

    Y = np.zeros((3, 3))
    for i in range(3):
        for j in range(i, 3):
            def integrand(u, ii=i, jj=j):
                fi = fermion_gaussian(u, positions[ii], sigma)
                fj = fermion_gaussian(u, positions[jj], sigma)
                return fi * kernel_func(u) * fj
            Y[i, j], _ = integrate.quad(integrand, -30, 30, limit=200)
            Y[j, i] = Y[i, j]

    evals, evecs = linalg.eigh(Y)
    idx = np.argsort(np.abs(evals))
    evecs = evecs[:, idx]

    s13 = min(abs(evecs[0, 2]), 1.0)
    sin2_13 = s13**2
    return sin2_13


def match_pct(pred, meas):
    return min(pred, meas) / max(pred, meas) * 100


# ================================================================
# SECTION 0: BASELINE
# ================================================================
print(f"\n\n{'='*76}")
print(f"[0] BASELINE: sigma=3, standard kink kernel")
print(f"{'='*76}")

baseline = compute_sin2_13(3.0, kink_profile)
print(f"    sin^2(theta_13) = {baseline:.6f}")
print(f"    Measured:          {sin2_13_measured:.6f}")
print(f"    Match:             {match_pct(baseline, sin2_13_measured):.1f}%")


# ================================================================
# SECTION 1: MODIFICATION A — sigma = sqrt(5) * scale
# ================================================================
print(f"\n\n{'='*76}")
print(f"[1] MODIFICATION A: sigma involves sqrt(5)")
print(f"{'='*76}")

print(f"""
    Structural motivation:
    The fermion profile width sigma controls localization on the wall.
    The wall itself has field range sqrt(5) (distance between vacua).
    If sigma is measured in wall-width units, and the wall width involves
    sqrt(5), then sigma should be proportional to sqrt(5).

    The Poschl-Teller potential has width parameter determined by the
    potential V = lambda*(Phi^2 - 5/4)^2 (in shifted coords), where
    5/4 = (sqrt(5)/2)^2. The natural scale is sqrt(5)/2.

    Candidates:
    - sigma = sqrt(5) = {sqrt5:.4f}
    - sigma = sqrt(5)/2 * something
    - sigma = pi*sqrt(5)/2 = c_1/c_0 = {pi*sqrt5/2:.4f} (the breathing ratio)
    - sigma = sqrt(5)*phi = {sqrt5*phi:.4f}
    - sigma = 3*sqrt(5)/2 = {3*sqrt5/2:.4f}
""")

sigma_candidates_A = {
    'sqrt(5)': sqrt5,
    'sqrt(5)/phi': sqrt5/phi,
    'sqrt(5)*phi/3': sqrt5*phi/3,
    'pi*sqrt(5)/2 = c1/c0': pi*sqrt5/2,
    '3*sqrt(5)/2': 3*sqrt5/2,
    'sqrt(5)*phi': sqrt5*phi,
    'sqrt(5)/2': sqrt5/2,
    'phi^2': phi**2,
    '3.0 (baseline)': 3.0,
    'sqrt(5)*phi/2': sqrt5*phi/2,
    '5/sqrt(5) = sqrt(5)': sqrt5,
    '2*sqrt(5)/phi': 2*sqrt5/phi,
}

# Remove duplicates
seen = set()
unique_candidates = {}
for name, val in sigma_candidates_A.items():
    key = round(val, 6)
    if key not in seen:
        seen.add(key)
        unique_candidates[name] = val

print(f"    {'sigma formula':>30s}  {'sigma':>8s}  {'sin^2_13':>10s}  {'match':>8s}")
print(f"    {'-'*30}  {'-'*8}  {'-'*10}  {'-'*8}")

results_A = []
for name, sigma in sorted(unique_candidates.items(), key=lambda x: x[1]):
    if sigma < 0.3 or sigma > 6.0:
        continue
    s2_13 = compute_sin2_13(sigma, kink_profile)
    m = match_pct(s2_13, sin2_13_measured)
    results_A.append((name, sigma, s2_13, m))
    marker = " <-- IMPROVED" if m > match_pct(baseline, sin2_13_measured) else ""
    print(f"    {name:>30s}  {sigma:>8.4f}  {s2_13:>10.6f}  {m:>7.1f}%{marker}")


# ================================================================
# SECTION 2: MODIFICATION B — Breathing amplitude * sqrt(5) factor
# ================================================================
print(f"\n\n{'='*76}")
print(f"[2] MODIFICATION B: Cross-wall amplitude with sqrt(5) factor")
print(f"{'='*76}")

print(f"""
    Structural motivation:
    c_1/c_0 = pi*sqrt(5)/2 already has sqrt(5) in it.
    But the PHYSICAL cross-wall tunneling amplitude may acquire
    an additional sqrt(5) from:
    - The field range between vacua = sqrt(5)
    - The overlap integral normalization
    - The Jacobian of the domain-wall coordinate transformation

    The cross-wall element Y_13 involves psi_1 evaluated at both sides.
    If the physical amplitude is Y_13_phys = Y_13 / sqrt(5), this
    would REDUCE the cross-wall mixing and decrease sin^2(theta_13).

    Similarly if the kink kernel gains/loses a sqrt(5) from proper
    normalization.
""")

# Test modified kernels
def kink_profile_div_sqrt5(u):
    """Kink with explicit 1/sqrt(5) normalization"""
    return kink_profile(u) / sqrt5

def kink_profile_times_sqrt5(u):
    """Kink with explicit sqrt(5) normalization"""
    return kink_profile(u) * sqrt5

# The proper field-theoretic kernel: the Yukawa coupling is from
# the kink derivative (Higgs profile), NOT the kink itself.
# But the kink profile gives better results. What about a
# hybrid: kink + sqrt(5) * Higgs?
def kink_plus_sqrt5_higgs(u):
    """Kink + sqrt(5) * Higgs derivative"""
    return kink_profile(u) + sqrt5 * higgs_profile(u)

def kink_minus_sqrt5_correction(u):
    """Kink - (sqrt(5)/kink_norm) * correction"""
    # The kink profile is (sqrt(5)/2)*tanh(u) + 1/2
    # A natural sqrt(5) correction: divide the tanh part by sqrt(5)
    # This gives: tanh(u)/2 + 1/2 = [tanh(u) + 1]/2
    # Which IS the coupling function f(x) = [tanh(x) + 1]/2
    return (np.tanh(u) + 1) / 2

def coupling_function(u):
    """f(x) = [tanh(x) + 1]/2 — the coupling function from e8_sm_embedding"""
    return (np.tanh(u) + 1) / 2

# The breathing mode decomposition with sqrt(5) in c_1:
# c_1 = 3*pi*sqrt(5)/8. If we use c_1/sqrt(5) = 3*pi/8
# as the effective coupling (stripping the sqrt(5)):
def kink_stripped_sqrt5(u):
    """Kernel with c_1 stripped of sqrt(5): c_0*psi_0 + (c_1/sqrt5)*psi_1"""
    c0_eff = c0
    c1_eff = c1 / sqrt5  # = 3*pi/8
    return c0_eff * psi_0(u) + c1_eff * psi_1(u)

# Or: the FULL kink minus the continuum, normalized differently
def breathing_only_kernel(u):
    """Only the breathing mode contribution (odd part of kink)"""
    return c1 * psi_1(u)

# Test at sigma=3 (the best baseline sigma)
sigma_test = 3.0

kernel_candidates = {
    'kink (baseline)': kink_profile,
    'kink / sqrt(5)': kink_profile_div_sqrt5,
    'coupling f(x)=[tanh+1]/2': coupling_function,
    'c0*psi0 + (c1/sqrt5)*psi1': kink_stripped_sqrt5,
    'Higgs derivative': higgs_profile,
}

print(f"    Testing different kernels at sigma = {sigma_test}:")
print(f"    {'kernel':>35s}  {'sin^2_13':>10s}  {'match':>8s}")
print(f"    {'-'*35}  {'-'*10}  {'-'*8}")

results_B = []
for name, kernel in kernel_candidates.items():
    s2_13 = compute_sin2_13(sigma_test, kernel)
    m = match_pct(s2_13, sin2_13_measured)
    results_B.append((name, s2_13, m))
    marker = " <-- IMPROVED" if m > match_pct(baseline, sin2_13_measured) else ""
    print(f"    {name:>35s}  {s2_13:>10.6f}  {m:>7.1f}%{marker}")

# Also scan sigma for each kernel
print(f"\n    Best sigma for each kernel:")
for name, kernel in kernel_candidates.items():
    best_s = None
    best_m = 0
    for sigma_100 in range(50, 600, 5):
        sigma = sigma_100 / 100.0
        s2_13 = compute_sin2_13(sigma, kernel)
        m = match_pct(s2_13, sin2_13_measured)
        if m > best_m:
            best_m = m
            best_s = sigma
    if best_s:
        s2_at_best = compute_sin2_13(best_s, kernel)
        print(f"    {name:>35s}  sigma={best_s:.2f}  sin^2={s2_at_best:.6f}  match={best_m:.1f}%")


# ================================================================
# SECTION 3: MODIFICATION C — Position separation with sqrt(5)
# ================================================================
print(f"\n\n{'='*76}")
print(f"[3] MODIFICATION C: Position separation with sqrt(5) correction")
print(f"{'='*76}")

print(f"""
    Structural motivation:
    The field range between vacua is sqrt(5).
    If generation positions are measured in units of the field range,
    the wall-crossing distance Delta_u = u_3 - u_1 should relate to sqrt(5).

    Current: u_3 - u_1 = {u_gen[2] - u_gen[0]:.2f}
    sqrt(5) = {sqrt5:.4f}
    2*sqrt(5) = {2*sqrt5:.4f}

    The ratio {(u_gen[2]-u_gen[0])/sqrt5:.4f} = (u3-u1)/sqrt(5)
    is close to {sqrt5:.4f} = sqrt(5) itself!
    So u3-u1 ~ 5.03 ~ sqrt(5)^2 = 5 (within 0.6%!)

    This suggests positions should be:
    - u_3 - u_1 = exactly 5 (= sqrt(5)^2)
    - And perhaps scaled by sqrt(5) from current values
""")

# Test: positions rescaled so Delta_u = 5 exactly
# Keep Gen 2 at u=-0.57, adjust Gen 1 and Gen 3 symmetrically
# around their current positions

# Current Delta = 5.03, target = 5.0
# Scale factor: 5.0 / 5.03 = 0.994
scale_exact5 = 5.0 / (u_gen[2] - u_gen[0])

u_gen_scaled = np.array([
    u_gen[0] * scale_exact5,
    u_gen[1],
    u_gen[2] * scale_exact5
])

# Also test: positions divided by sqrt(5) (if they were in field units)
u_gen_div_sqrt5 = u_gen / sqrt5

# Test: Gen 1 at -sqrt(5), Gen 2 at -1/phi, Gen 3 at +sqrt(5)
u_gen_sqrt5_sym = np.array([-sqrt5, -phibar, sqrt5])

# Test: positions where the FIELD values are at special points
# At u, Phi(u) = sqrt(5)/2 * tanh(u) + 1/2
# Gen 3 at Phi = phi: tanh(u) = 1, u = infinity (not useful)
# Gen 1 at Phi = -1/phi: tanh(u) = -1, u = -infinity (not useful)
# Gen 2 at Phi = 1/2: tanh(u) = 0, u = 0
# Gen 3 at Phi = phi - 1/sqrt(5): tanh(u) = (2*phi-1-2/sqrt(5))/sqrt(5)

# A natural position set: u_i = i * sqrt(5) - some_offset
# Keeping the center of mass similar to the original

position_candidates = {
    'Original [-2.03, -0.57, 3.0]': u_gen,
    'Scaled to Delta=5': u_gen_scaled,
    'Divided by sqrt(5)': u_gen_div_sqrt5,
    '[-sqrt(5), -1/phi, sqrt(5)]': u_gen_sqrt5_sym,
    '[-2, -0.57, 3]': np.array([-2.0, -0.57, 3.0]),
    '[-sqrt(5), -1/phi, phi^2]': np.array([-sqrt5, -phibar, phi**2]),
    '[-phi^2, -1/phi, phi^2]': np.array([-phi**2, -phibar, phi**2]),
}

sigma_test = 3.0
print(f"    Testing position sets at sigma = {sigma_test}:")
print(f"    {'positions':>42s}  {'sin^2_13':>10s}  {'match':>8s}")
print(f"    {'-'*42}  {'-'*10}  {'-'*8}")

for name, pos in position_candidates.items():
    s2_13 = compute_sin2_13(sigma_test, kink_profile, positions=pos)
    m = match_pct(s2_13, sin2_13_measured)
    marker = " <-- IMPROVED" if m > match_pct(baseline, sin2_13_measured) else ""
    print(f"    {name:>42s}  {s2_13:>10.6f}  {m:>7.1f}%{marker}")


# ================================================================
# SECTION 4: MODIFICATION D — Proper Poschl-Teller normalization
# ================================================================
print(f"\n\n{'='*76}")
print(f"[4] MODIFICATION D: Physical normalization of the kink kernel")
print(f"{'='*76}")

print(f"""
    Structural motivation:
    In the PHYSICAL domain wall problem, the Yukawa coupling comes from
    the scalar field profile. The kink is:

    Phi(u) = (sqrt(5)/2) * tanh(u) + 1/2

    The sqrt(5)/2 prefactor is the half-distance between vacua.
    The Higgs derivative is H(u) = dPhi/du = (sqrt(5)/2) * sech^2(u).

    In standard extra-dimension models, the Yukawa is:
    Y_ij = integral f_i(y) * H(y) * f_j(y) dy

    where H(y) is the Higgs profile (= derivative of kink).
    The current script uses the KINK PROFILE (not derivative) because it
    gives better results (the kink extends to both vacua, carrying the
    breathing mode).

    But the PHYSICAL Yukawa should use:
    Y_ij = sqrt(5)/2 * integral f_i * sech^2 * f_j dy  (Higgs derivative)

    Or the properly normalized bound-state decomposition:
    Y_ij = c0/||psi0||^2 * <f_i|psi0><psi0|f_j> + c1/||psi1||^2 * <f_i|psi1><psi1|f_j>

    The norms are ||psi0||^2 = 4/3 and ||psi1||^2 = 2/3.
    The ratio of normalizations is (4/3)/(2/3) = 2.
    This factor of 2 could combine with sqrt(5) to give a correction.
""")

# Test: properly normalized bound-state decomposed kernel
def kernel_normalized_bs(u):
    """Bound states with proper norm factors"""
    # c_k * psi_k / ||psi_k||^2 gives the projection coefficient
    # The Yukawa matrix element is:
    # Y_ij = sum_k c_k * <f_i|psi_k> * <psi_k|f_j> / ||psi_k||^2
    # This is equivalent to using kernel = sum_k (c_k / ||psi_k||^2) * psi_k
    return (c0 / (4/3)) * psi_0(u) + (c1 / (2/3)) * psi_1(u)

# The normalized kernel:
# c0/(4/3) = (3/4)/(4/3) = 9/16
# c1/(2/3) = (3*pi*sqrt(5)/8)/(2/3) = 9*pi*sqrt(5)/16
# Ratio of breathing to zero: c1/(2/3) / (c0/(4/3)) = (c1/c0) * 2 = pi*sqrt(5)
# This is EXACTLY 2x the breathing ratio!

print(f"    Normalized bound-state decomposition:")
print(f"    Zero mode coefficient: c0/||psi0||^2 = 9/16 = {9/16:.6f}")
print(f"    Breathing coefficient: c1/||psi1||^2 = 9*pi*sqrt(5)/16 = {9*pi*sqrt5/16:.6f}")
print(f"    Ratio: pi*sqrt(5) = {pi*sqrt5:.6f}")
print(f"    (Compare to un-normalized ratio: pi*sqrt(5)/2 = {pi*sqrt5/2:.6f})")

s2_norm_bs = compute_sin2_13(3.0, kernel_normalized_bs)
print(f"\n    At sigma=3: sin^2_13 = {s2_norm_bs:.6f}, match = {match_pct(s2_norm_bs, sin2_13_measured):.1f}%")


# ================================================================
# SECTION 5: MODIFICATION E — The sqrt(5) vacuum correction
# ================================================================
print(f"\n\n{'='*76}")
print(f"[5] MODIFICATION E: The sqrt(5) vacuum correction pattern")
print(f"{'='*76}")

print(f"""
    Structural motivation:
    The claim is that EVERY cross-wall quantity picks up sqrt(5).
    Looking at the successful formulas:

    Lambda = theta_4^80 * sqrt(5) / phi^2    (cosmological constant)
    c_1/c_0 = pi * sqrt(5) / 2               (breathing ratio)
    alpha correction: t4/(t3*phi)             (involves theta functions)
    Field range = sqrt(5)                     (between vacua)
    Higgs prefactor = sqrt(5)/2               (kink amplitude)

    The PATTERN: sqrt(5) appears as a multiplicative correction on
    cross-wall quantities because the field traverses a range of sqrt(5)
    when crossing the wall.

    For theta_13, the cross-wall mixing should then be:
    sin(theta_13) ~ Y_13 / Y_33 * (correction involving sqrt(5))

    The question: does sin^2(theta_13) get multiplied or divided by sqrt(5)?

    If sin^2(theta_13)_physical = sin^2(theta_13)_raw / sqrt(5):
    0.0257 / sqrt(5) = {0.0257/sqrt5:.6f} (match: {match_pct(0.0257/sqrt5, sin2_13_measured):.1f}%)

    If sin^2(theta_13)_physical = sin^2(theta_13)_raw * (2/sqrt(5)):
    0.0257 * 2/sqrt(5) = {0.0257*2/sqrt5:.6f} (too large)

    If sin(theta_13)_physical = sin(theta_13)_raw / sqrt(5)^(1/4):
    sin^2 = 0.0257 / sqrt(sqrt(5)) = {0.0257/sqrt5**0.5:.6f}
""")

# Systematic: what power of sqrt(5) gives the best match?
print(f"    Systematic search: sin^2_13 = 0.0257 * 5^(-p/2)")
print(f"    {'power p':>10s}  {'factor':>10s}  {'sin^2_13':>10s}  {'match':>8s}")
print(f"    {'-'*10}  {'-'*10}  {'-'*10}  {'-'*8}")

for p_10 in range(-10, 11):
    p = p_10 / 10.0
    factor = 5**(-p/2)
    s2 = baseline * factor
    m = match_pct(s2, sin2_13_measured)
    if m > 80:
        marker = " <-- " if m > 95 else ""
        print(f"    {p:>10.1f}  {factor:>10.6f}  {s2:>10.6f}  {m:>7.1f}%{marker}")


# ================================================================
# SECTION 6: DEEP ANALYSIS — Where sqrt(5) enters physically
# ================================================================
print(f"\n\n{'='*76}")
print(f"[6] DEEP ANALYSIS: Physical origin of sqrt(5) in cross-wall quantities")
print(f"{'='*76}")

print(f"""
    The kink profile Phi(u) = (sqrt(5)/2)*tanh(u) + 1/2

    The Yukawa overlap integral:
    Y_ij = int f_i(u) * Phi(u) * f_j(u) du
         = (sqrt(5)/2) * int f_i * tanh * f_j du + (1/2) * int f_i * f_j du

    For cross-wall mixing (i=1, j=3), the second integral (constant part)
    is small because f_1 and f_3 have little overlap.
    So Y_13 ~ (sqrt(5)/2) * int f_1 * tanh * f_3 du

    The tanh function is effectively the SIGN function at large |u|:
    tanh(u) -> sgn(u) for |u| >> 1.

    For f_1 centered at u=-2.03 and f_3 centered at u=3.0:
    The overlap with tanh is dominated by the tails.

    The sqrt(5)/2 prefactor in the kink is ALREADY included when we
    use kink_profile as the kernel. So the baseline already has sqrt(5).

    But: the NORMALIZED mixing angle sin(theta_13) ~ Y_13 / sqrt(Y_11*Y_33)
    involves diagonal elements too. If Y_ii has a different sqrt(5) dependence
    than Y_ij, the ratio could acquire a net sqrt(5) correction.
""")

# Compute the decomposed mixing explicitly
sigma = 3.0

def compute_full_decomposition(sigma, positions=None):
    if positions is None:
        positions = u_gen

    # Compute separate contributions
    def compute_element(kernel, i, j):
        def integrand(u, ii=i, jj=j):
            fi = fermion_gaussian(u, positions[ii], sigma)
            fj = fermion_gaussian(u, positions[jj], sigma)
            return fi * kernel(u) * fj
        val, _ = integrate.quad(integrand, -30, 30, limit=200)
        return val

    # The tanh part (cross-wall mediator)
    def tanh_kernel(u):
        return np.tanh(u)

    # The constant part
    def const_kernel(u):
        return 1.0

    results = {}
    for i in range(3):
        for j in range(i, 3):
            y_tanh = compute_element(tanh_kernel, i, j)
            y_const = compute_element(const_kernel, i, j)
            y_kink = compute_element(kink_profile, i, j)
            results[(i,j)] = {
                'tanh': y_tanh,
                'const': y_const,
                'kink': y_kink,
                'check': sqrt5/2 * y_tanh + 0.5 * y_const,
            }
    return results

decomp = compute_full_decomposition(sigma)

print(f"\n    Yukawa matrix decomposition at sigma={sigma}:")
print(f"    Y_ij = (sqrt(5)/2)*Y_tanh_ij + (1/2)*Y_const_ij")
print(f"")
print(f"    {'(i,j)':>8s}  {'Y_tanh':>12s}  {'Y_const':>12s}  {'Y_kink':>12s}  {'sqrt5/2*tanh+1/2*const':>22s}")
print(f"    {'-'*8}  {'-'*12}  {'-'*12}  {'-'*12}  {'-'*22}")

for (i,j), vals in sorted(decomp.items()):
    print(f"    ({i+1},{j+1}){' ':>4s}  {vals['tanh']:>12.6e}  {vals['const']:>12.6e}  "
          f"{vals['kink']:>12.6e}  {vals['check']:>12.6e}")

# The key cross-wall element
y13_tanh = decomp[(0,2)]['tanh']
y13_const = decomp[(0,2)]['const']
y13_kink = decomp[(0,2)]['kink']
y33_kink = decomp[(2,2)]['kink']
y11_kink = decomp[(0,0)]['kink']

print(f"\n    Cross-wall analysis:")
print(f"    Y_13(kink) = {y13_kink:.6e}")
print(f"    Y_13(tanh) = {y13_tanh:.6e}  (the cross-wall part)")
print(f"    Y_13(const) = {y13_const:.6e}  (the symmetric part)")
print(f"    Ratio tanh/const for (1,3): {abs(y13_tanh/y13_const):.4f}")
print(f"")
print(f"    The cross-wall element is dominated by the tanh part (ratio {abs(y13_tanh/y13_const):.1f}x)")
print(f"    The sqrt(5)/2 prefactor is already in the kink kernel.")

# Now: what if the PHYSICAL cross-wall coupling has an ADDITIONAL
# sqrt(5) factor from the vacuum normalization?
# The field traverses a range of sqrt(5). The tunneling amplitude
# may need to be normalized by this range.

print(f"\n\n    Testing: Y_13_phys = Y_13 / sqrt(5) (vacuum range normalization)")
print(f"    This would give a modified Yukawa matrix where off-diagonal")
print(f"    elements (cross-wall) are suppressed by 1/sqrt(5).")

def compute_sin2_13_suppressed(sigma, suppression_factor):
    """Compute sin^2(theta_13) with cross-wall elements suppressed."""
    Y = np.zeros((3, 3))
    for i in range(3):
        for j in range(i, 3):
            def integrand(u, ii=i, jj=j):
                fi = fermion_gaussian(u, u_gen[ii], sigma)
                fj = fermion_gaussian(u, u_gen[jj], sigma)
                return fi * kink_profile(u) * fj
            Y[i, j], _ = integrate.quad(integrand, -30, 30, limit=200)
            Y[j, i] = Y[i, j]

    # Apply suppression to cross-wall elements only
    # Cross-wall: Gen 1 (dark side, u<0) mixing with Gen 3 (light side, u>0)
    # The (0,2) element crosses the wall. But what about (1,2)?
    # Gen 2 at u=-0.57 is on the dark side, but near the wall center.
    # The cleanest: suppress all elements where one gen is dark, other is light
    for i in range(3):
        for j in range(3):
            if (u_gen[i] < 0 and u_gen[j] > 0) or (u_gen[i] > 0 and u_gen[j] < 0):
                Y[i, j] *= suppression_factor

    evals, evecs = linalg.eigh(Y)
    idx = np.argsort(np.abs(evals))
    evecs = evecs[:, idx]

    s13 = min(abs(evecs[0, 2]), 1.0)
    return s13**2

print(f"\n    Cross-wall suppression scan:")
print(f"    {'factor':>12s}  {'formula':>25s}  {'sin^2_13':>10s}  {'match':>8s}")
print(f"    {'-'*12}  {'-'*25}  {'-'*10}  {'-'*8}")

suppression_tests = {
    '1.0 (baseline)': 1.0,
    '1/sqrt(5)': 1/sqrt5,
    '1/phi': 1/phi,
    '2/sqrt(5)': 2/sqrt5,
    'phi/sqrt(5)': phi/sqrt5,
    '1/phi^2': 1/phi**2,
    '2/(pi*sqrt(5))': 2/(pi*sqrt5),
    'sqrt(5)/pi': sqrt5/pi,
    '2/pi': 2/pi,
    '3/(pi*sqrt(5))': 3/(pi*sqrt5),
}

for name, factor in sorted(suppression_tests.items(), key=lambda x: x[1]):
    s2_13 = compute_sin2_13_suppressed(3.0, factor)
    m = match_pct(s2_13, sin2_13_measured)
    marker = " <--" if m > 95 else ""
    print(f"    {factor:>12.6f}  {name:>25s}  {s2_13:>10.6f}  {m:>7.1f}%{marker}")


# ================================================================
# SECTION 7: MODIFICATION F — sigma = pi*sqrt(5)/phi (combined scan)
# ================================================================
print(f"\n\n{'='*76}")
print(f"[7] COMBINED SCAN: sigma and kernel variations together")
print(f"{'='*76}")

print(f"    Testing all structurally motivated (sigma, kernel) combinations")
print(f"    that could include sqrt(5) corrections.\n")

# Fine sigma scan around structurally motivated values
sigma_fine = [
    ('sqrt(5)', sqrt5),
    ('phi^2', phi**2),
    ('3', 3.0),
    ('pi', pi),
    ('pi*sqrt(5)/phi^2', pi*sqrt5/phi**2),
    ('sqrt(5)*phi/2', sqrt5*phi/2),
    ('3*phi/sqrt(5)', 3*phi/sqrt5),
    ('7/sqrt(5)', 7/sqrt5),
    ('sqrt(5)+1/phi', sqrt5+phibar),
    ('pi/phi', pi/phi),
]

best_overall = None
best_match = 0

for s_name, sigma in sigma_fine:
    for k_name, kernel in [('kink', kink_profile),
                           ('coupling', coupling_function),
                           ('stripped_sqrt5', kink_stripped_sqrt5)]:
        s2_13 = compute_sin2_13(sigma, kernel)
        m = match_pct(s2_13, sin2_13_measured)
        if m > best_match:
            best_match = m
            best_overall = (s_name, sigma, k_name, s2_13, m)

        if m > 90:
            print(f"    sigma={s_name:>22s} ({sigma:.4f})  kernel={k_name:>15s}  sin^2={s2_13:.6f}  match={m:.1f}%")

if best_overall:
    s_name, sigma, k_name, s2, m = best_overall
    print(f"\n    BEST: sigma={s_name} ({sigma:.4f}), kernel={k_name}")
    print(f"          sin^2_13 = {s2:.6f}, match = {m:.1f}%")


# ================================================================
# SECTION 8: The theta_4 correction (from near-cusp physics)
# ================================================================
print(f"\n\n{'='*76}")
print(f"[8] THETA_4 CORRECTION: Does t4 fix the residual?")
print(f"{'='*76}")

t4 = 0.030304  # theta_4(1/phi)

print(f"""
    From near-cusp physics, theta_4 = {t4:.6f} is the universal
    dark vacuum correction. Every tree-level quantity gets a (1 +/- k*t4)
    correction.

    If sin^2(theta_13) = 0.0257 * (1 - t4):
    {baseline * (1 - t4):.6f}  (match: {match_pct(baseline * (1 - t4), sin2_13_measured):.1f}%)

    If sin^2(theta_13) = 0.0257 * (1 - phi*t4):
    {baseline * (1 - phi*t4):.6f}  (match: {match_pct(baseline * (1 - phi*t4), sin2_13_measured):.1f}%)

    If sin^2(theta_13) = 0.0257 * (1 - sqrt(5)*t4):
    {baseline * (1 - sqrt5*t4):.6f}  (match: {match_pct(baseline * (1 - sqrt5*t4), sin2_13_measured):.1f}%)

    If sin^2(theta_13) = 0.0257 / (1 + sqrt(5)*t4):
    {baseline / (1 + sqrt5*t4):.6f}  (match: {match_pct(baseline / (1 + sqrt5*t4), sin2_13_measured):.1f}%)
""")

# The most structurally motivated: every cross-wall quantity gets sqrt(5)*t4
# (because t4 is the fermionic partition function AND the cross-wall
# tunneling suppression from the dark vacuum)

print(f"    Systematic t4 correction search:")
print(f"    {'formula':>30s}  {'value':>10s}  {'match':>8s}")
print(f"    {'-'*30}  {'-'*10}  {'-'*8}")

t4_corrections = {
    'baseline (no corr)': baseline,
    '*(1-t4)': baseline * (1 - t4),
    '*(1-phi*t4)': baseline * (1 - phi*t4),
    '*(1-sqrt(5)*t4)': baseline * (1 - sqrt5*t4),
    '*(1-2*t4)': baseline * (1 - 2*t4),
    '*(1-3*t4)': baseline * (1 - 3*t4),
    '*(1-pi*t4)': baseline * (1 - pi*t4),
    '*(1-7*t4)': baseline * (1 - 7*t4),
    '/(1+sqrt(5)*t4)': baseline / (1 + sqrt5*t4),
    '/(1+phi*t4)': baseline / (1 + phi*t4),
    '*(1-sqrt(5)*phi*t4)': baseline * (1 - sqrt5*phi*t4),
    '*(1-t4/phi)': baseline * (1 - t4/phi),
    '*(1-t4*sqrt(5)/phi)': baseline * (1 - t4*sqrt5/phi),
}

for name, val in sorted(t4_corrections.items(), key=lambda x: -match_pct(x[1], sin2_13_measured)):
    m = match_pct(val, sin2_13_measured)
    marker = " <--" if m > 95 else ""
    print(f"    {name:>30s}  {val:>10.6f}  {m:>7.1f}%{marker}")


# ================================================================
# SECTION 9: sigma_physical = sigma_raw / sqrt(5)^(1/n)
# ================================================================
print(f"\n\n{'='*76}")
print(f"[9] SIGMA FINE-SCAN: Finding the optimal sigma near sqrt(5)-related values")
print(f"{'='*76}")

# Very fine sigma scan
print(f"    Fine sigma scan around structurally interesting values:")
print(f"    {'sigma':>8s}  {'sin^2_13':>10s}  {'match':>8s}  {'note':>20s}")
print(f"    {'-'*8}  {'-'*10}  {'-'*8}  {'-'*20}")

sigma_notes = {
    sqrt5: 'sqrt(5)',
    sqrt5/phi: 'sqrt(5)/phi',
    phi**2: 'phi^2',
    3.0: '3 (baseline)',
    pi: 'pi',
    sqrt5 + phibar: 'sqrt(5)+1/phi',
    7/sqrt5: '7/sqrt(5)',
    2*phi: '2*phi',
    5/phi: '5/phi',
    pi*phi/sqrt5: 'pi*phi/sqrt(5)',
    3*phi/sqrt5: '3*phi/sqrt(5)',
    sqrt5*phi: 'sqrt(5)*phi',
    2*sqrt5: '2*sqrt(5)',
}

# Also do a continuous fine scan
best_sigma_fine = None
best_match_fine = 0
best_s2_fine = 0

for sigma_1000 in range(1500, 5000, 10):
    sigma = sigma_1000 / 1000.0
    s2_13 = compute_sin2_13(sigma, kink_profile)
    m = match_pct(s2_13, sin2_13_measured)
    if m > best_match_fine:
        best_match_fine = m
        best_sigma_fine = sigma
        best_s2_fine = s2_13

print(f"    Continuous fine scan result:")
print(f"    Best sigma = {best_sigma_fine:.3f}")
print(f"    sin^2_13 = {best_s2_fine:.6f}")
print(f"    Match = {best_match_fine:.1f}%")
print(f"")

# Check if best sigma matches any framework number
for val, name in sorted(sigma_notes.items()):
    m_sigma = match_pct(best_sigma_fine, val)
    if m_sigma > 95:
        print(f"    Best sigma {best_sigma_fine:.3f} ~ {name} = {val:.3f} ({m_sigma:.1f}%)")

print(f"")
# Print structurally motivated sigmas
for sigma, name in sorted(sigma_notes.items()):
    s2_13 = compute_sin2_13(sigma, kink_profile)
    m = match_pct(s2_13, sin2_13_measured)
    marker = " <-- BEST STRUCTURAL" if m > 90 else ""
    print(f"    sigma={sigma:>8.4f} ({name:>18s})  sin^2={s2_13:>10.6f}  match={m:>7.1f}%{marker}")


# ================================================================
# SECTION 10: THE HONEST ASSESSMENT
# ================================================================
print(f"\n\n{'='*76}")
print(f"[10] HONEST ASSESSMENT")
print(f"{'='*76}")

# Collect all structurally motivated results
all_results = []

# Baseline
all_results.append(('BASELINE: sigma=3, kink kernel', baseline, match_pct(baseline, sin2_13_measured)))

# Best from each section
# Section 1: sigma candidates
for name, sigma, s2, m in results_A:
    if m > match_pct(baseline, sin2_13_measured):
        all_results.append((f'A: sigma={name}', s2, m))

# Section 6: suppression
for name, factor in suppression_tests.items():
    s2 = compute_sin2_13_suppressed(3.0, factor)
    m = match_pct(s2, sin2_13_measured)
    if m > match_pct(baseline, sin2_13_measured) + 2:
        all_results.append((f'Cross-wall suppression: {name}', s2, m))

# Section 8: t4 corrections
for name, val in t4_corrections.items():
    m = match_pct(val, sin2_13_measured)
    if m > match_pct(baseline, sin2_13_measured) + 2:
        all_results.append((f't4 correction: {name}', val, m))

# Sort by match
all_results.sort(key=lambda x: -x[2])

print(f"""
    Current: sin^2(theta_13) = {baseline:.6f}  (match: {match_pct(baseline, sin2_13_measured):.1f}%)
    Target:  sin^2(theta_13) = {sin2_13_measured:.6f} +/- {sin2_13_err:.6f}

    The measured value is BELOW the prediction by a factor of:
    {sin2_13_measured / baseline:.6f} = 0.0220/0.0257

    This ratio = {sin2_13_measured / baseline:.6f}
    Compare to:
    1/sqrt(5)^(1/3) = {1/sqrt5**(1/3):.6f}
    phi/sqrt(5) = {phi/sqrt5:.6f}
    1 - t4 = {1-t4:.6f}
    1/(1+sqrt(5)*t4) = {1/(1+sqrt5*t4):.6f}
    2/(sqrt(5)+1) = 1/phi = {phibar:.6f}
    1 - 1/sqrt(5) = {1-1/sqrt5:.6f}
""")

print(f"    ALL IMPROVEMENTS over baseline (structurally motivated):")
print(f"    {'#':>4s}  {'Method':>55s}  {'sin^2':>10s}  {'match':>8s}")
print(f"    {'-'*4}  {'-'*55}  {'-'*10}  {'-'*8}")
for i, (name, s2, m) in enumerate(all_results[:15]):
    print(f"    {i+1:>4d}  {name:>55s}  {s2:>10.6f}  {m:>7.1f}%")

# Final assessment
print(f"""

CONCLUSIONS:
============

1. BASELINE: sin^2(theta_13) = {baseline:.6f} at sigma=3 gives {match_pct(baseline, sin2_13_measured):.1f}% match.

2. The prediction is TOO HIGH by a factor of {baseline/sin2_13_measured:.3f}.
   The measured value is {sin2_13_measured:.5f}; we predict {baseline:.5f}.

3. SIGMA MODIFICATION: The best sigma from the fine scan is {best_sigma_fine:.3f},
   giving {best_match_fine:.1f}% match. This is {'NOT significantly better' if best_match_fine < 90 else 'an improvement'}.
""")

# Check: is sigma=3 actually the best, or does a better sigma exist?
# If a better sigma exists, check its framework meaning
if best_match_fine > match_pct(baseline, sin2_13_measured):
    print(f"   A slightly better sigma ({best_sigma_fine:.3f}) exists but may not have a clean framework expression.")

print(f"""
4. SQRT(5) KERNEL MODIFICATIONS:
   - Dividing kink by sqrt(5): changes the overall scale but not the mixing angles significantly.
   - Using the coupling function f(x)=[tanh+1]/2 (which removes sqrt(5)): changes angles.
   - Stripping sqrt(5) from c_1: redistributes breathing mode weight.

5. THETA_4 CORRECTIONS:
   The most promising direction may be:
   sin^2(theta_13) * (1 - k*t4) with k = sqrt(5) or k = 7:
   - k = sqrt(5): {baseline*(1-sqrt5*t4):.6f} ({match_pct(baseline*(1-sqrt5*t4), sin2_13_measured):.1f}%)
   - k = 7:       {baseline*(1-7*t4):.6f} ({match_pct(baseline*(1-7*t4), sin2_13_measured):.1f}%)

6. HONEST VERDICT:
   The sqrt(5) correction insight from section 124 is structurally motivated,
   but the improvement pathways found here are modest. The fundamental issue
   is that the current calculation gives sin^2 = 0.0257, and the measured
   value is 0.0220 — a ratio of {sin2_13_measured/baseline:.4f}. This ratio does NOT
   cleanly match 1/sqrt(5) = {1/sqrt5:.4f}, phi/sqrt(5) = {phi/sqrt5:.4f}, or other
   simple framework expressions.

   The MOST promising structural corrections are:
   a) t4 correction with k ~ 5-7 (but the value of k lacks derivation)
   b) Slightly different sigma (framework-motivated value near 3)
   c) Cross-wall suppression factor (but needs physical motivation)

   NONE of these cleanly involve sqrt(5) in a way that is both
   structurally derived AND numerically accurate.
""")

print("=" * 76)
print("END OF THETA_13 SQRT(5) INVESTIGATION")
print("=" * 76)
