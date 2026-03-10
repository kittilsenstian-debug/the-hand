#!/usr/bin/env python3
"""
S3 MODULAR MASS MATRIX AT THE GOLDEN NODE
==========================================

Constructs the actual S3 = Gamma(2) modular mass matrix at tau corresponding
to q = 1/phi and tests whether it reproduces fermion masses.

Key references:
  - Feruglio (2017): "Are neutrino masses modular forms?" arXiv:1706.08749
  - Okada & Tanimoto (2025): "Fermion masses and mixing in Pati-Salam
    with S3 modular symmetry," arXiv:2501.00302
  - Okada & Orikasa (2019): "Modular S3 symmetric radiative seesaw model,"
    arXiv:1907.04716
  - Kobayashi et al. (2019): "Modular S3-invariant flavor model in SU(5) GUT,"
    PTEP 2020

Interface Theory context:
  - q = 1/phi = 0.6180... (golden nome)
  - tau = i * ln(phi) / (2*pi) = 0.07663i
  - S-dual: tau' = -1/tau = 13.06i
  - S3 = Weyl(A2), the generation symmetry from 4A2 in E8

Standard Python only. No external dependencies.
"""

import math

# ============================================================
# PHYSICAL CONSTANTS AND SETUP
# ============================================================

phi = (1 + math.sqrt(5)) / 2      # 1.6180339887...
phibar = 1 / phi                    # 0.6180339887... = phi - 1
q_golden = phibar                   # The golden nome

# Physical constants (PDG 2024)
m_e = 0.51099895       # MeV (electron)
m_mu = 105.6583755     # MeV (muon)
m_tau = 1776.86        # MeV (tau)
m_u = 2.16             # MeV (up quark, MSbar at 2 GeV)
m_d = 4.67             # MeV (down quark)
m_s = 93.4             # MeV (strange quark)
m_c = 1270.0           # MeV (charm quark)
m_b = 4180.0           # MeV (bottom quark)
m_t = 172760.0         # MeV (top quark)
mu_ratio = 1836.15267343  # proton/electron mass ratio
alpha_em = 1/137.035999084
v_higgs = 246220.0     # MeV (Higgs VEV)

# CKM matrix elements (PDG 2024)
V_us_meas = 0.2243
V_cb_meas = 0.0422
V_ub_meas = 0.00394

# PMNS mixing angles (NuFIT 6.0, NO)
sin2_t12_meas = 0.303
sin2_t23_meas = 0.572
sin2_t13_meas = 0.02203

# Neutrino mass-squared differences (eV^2)
dm21_sq = 7.41e-5
dm31_sq = 2.507e-3

banner = lambda t: print(f"\n{'='*78}\n{t}\n{'='*78}")
section = lambda t: print(f"\n--- {t} ---")

# ============================================================
# MODULAR FORM COMPUTATION
# ============================================================

def eta_func(q, terms=2000):
    """Dedekind eta function: eta(q) = q^(1/24) * prod_{n=1}^inf (1 - q^n)"""
    result = q**(1.0/24)
    for n in range(1, terms+1):
        qn = q**n
        if qn < 1e-15:
            break
        result *= (1 - qn)
    return result

def theta2_func(q, terms=300):
    """Jacobi theta_2: theta_2(q) = 2*sum_{n>=0} q^((n+1/2)^2)"""
    s = 0.0
    for n in range(0, terms+1):
        term = q**((n + 0.5)**2)
        if term < 1e-15:
            break
        s += 2 * term
    return s

def theta3_func(q, terms=300):
    """Jacobi theta_3: theta_3(q) = 1 + 2*sum_{n>=1} q^(n^2)"""
    s = 1.0
    for n in range(1, terms+1):
        term = q**(n*n)
        if term < 1e-15:
            break
        s += 2 * term
    return s

def theta4_func(q, terms=300):
    """Jacobi theta_4: theta_4(q) = 1 + 2*sum_{n>=1} (-1)^n * q^(n^2)"""
    s = 1.0
    for n in range(1, terms+1):
        term = q**(n*n)
        if term < 1e-15:
            break
        s += 2 * ((-1)**n) * term
    return s

# Compute at golden nome
eta = eta_func(q_golden)
t2 = theta2_func(q_golden)
t3 = theta3_func(q_golden)
t4 = theta4_func(q_golden)
q = q_golden

# tau = i * ln(phi) / (2*pi)
tau_im = math.log(phi) / (2 * math.pi)
tau_S_im = 1.0 / tau_im  # S-dual: tau' = i/tau_im

# ============================================================
# SIMPLE 3x3 MATRIX UTILITIES (no numpy)
# ============================================================

def mat_mul(A, B):
    """Multiply two 3x3 matrices"""
    n = len(A)
    m = len(B[0])
    p = len(B)
    C = [[0.0]*m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            for k in range(p):
                C[i][j] += A[i][k] * B[k][j]
    return C

def mat_transpose(A):
    n = len(A)
    m = len(A[0])
    return [[A[j][i] for j in range(n)] for i in range(m)]

def mat_adj_transpose(A):
    """Hermitian conjugate (for real matrices, just transpose)"""
    return mat_transpose(A)

def eigenvalues_3x3_symmetric(M):
    """
    Eigenvalues of a real symmetric 3x3 matrix using Cardano's formula.
    Returns sorted eigenvalues (ascending).
    """
    a = M[0][0]; b = M[0][1]; c = M[0][2]
    d = M[1][1]; e = M[1][2]; f = M[2][2]

    p1 = b*b + c*c + e*e
    if p1 < 1e-30:
        # Matrix is diagonal
        eigs = sorted([a, d, f])
        return eigs

    q_coeff = (a + d + f) / 3.0
    p2 = (a - q_coeff)**2 + (d - q_coeff)**2 + (f - q_coeff)**2 + 2*p1
    p = math.sqrt(p2 / 6.0)

    # B = (1/p) * (M - q*I)
    B = [[(M[i][j] - (q_coeff if i == j else 0)) / p for j in range(3)] for i in range(3)]

    # det(B)
    detB = (B[0][0]*(B[1][1]*B[2][2] - B[1][2]*B[2][1])
          - B[0][1]*(B[1][0]*B[2][2] - B[1][2]*B[2][0])
          + B[0][2]*(B[1][0]*B[2][1] - B[1][1]*B[2][0]))

    r = detB / 2.0
    r = max(-1.0, min(1.0, r))

    phi_angle = math.acos(r) / 3.0

    eig1 = q_coeff + 2*p*math.cos(phi_angle)
    eig3 = q_coeff + 2*p*math.cos(phi_angle + 2*math.pi/3)
    eig2 = 3*q_coeff - eig1 - eig3

    return sorted([eig1, eig2, eig3])

def singular_values_3x3(M):
    """
    Singular values of a 3x3 matrix M.
    These are sqrt(eigenvalues of M^T * M).
    Returns sorted ascending.
    """
    Mt = mat_transpose(M)
    MtM = mat_mul(Mt, M)
    eigs = eigenvalues_3x3_symmetric(MtM)
    svs = [math.sqrt(max(0, e)) for e in eigs]
    return sorted(svs)


# ============================================================
banner("S3 MODULAR MASS MATRIX AT THE GOLDEN NODE")
# ============================================================

print(f"""
Golden nome: q = 1/phi = {q_golden:.10f}
phi = {phi:.10f}, phibar = {phibar:.10f}
tau = {tau_im:.10f} i  (purely imaginary)
S-dual tau' = {tau_S_im:.6f} i

Modular forms at q = 1/phi:
  eta(q)    = {eta:.8f}
  theta_2   = {t2:.8f}
  theta_3   = {t3:.8f}
  theta_4   = {t4:.8f}
""")


# ============================================================
banner("PART 1: S3 REPRESENTATION THEORY")
# ============================================================

print("""
S3 (symmetric group on 3 elements) has 3 irreducible representations:
  1  : trivial singlet (dimension 1)
  1' : sign representation (dimension 1)
  2  : standard doublet (dimension 2)

Tensor product rules:
  1  x 1  = 1
  1  x 1' = 1'
  1' x 1' = 1
  1  x 2  = 2
  1' x 2  = 2
  2  x 2  = 1 + 1' + 2

Clebsch-Gordan decomposition for 2 x 2:
  For doublets a = (a1, a2) and b = (b1, b2):

    1  (trivial singlet):  a1*b1 + a2*b2
    1' (sign singlet):     a1*b2 - a2*b1
    2  (doublet):          (a1*b2 + a2*b1,  a1*b1 - a2*b2)

  [Convention from arXiv:1907.04716 / Okada-Tanimoto 2025]

For 2 x 1:
  a = (a1, a2) in 2,  b in 1:
    Result in 2:  (a1*b, a2*b)

For 2 x 1':
  a = (a1, a2) in 2,  b in 1':
    Result in 2:  (a2*b, -a1*b)   [note the sign flip]
""")


# ============================================================
banner("PART 2: MODULAR FORMS FOR GAMMA(2) AT q = 1/phi")
# ============================================================

section("2A. Weight-2 modular forms (S3 doublet)")

# The weight-2 modular forms for Gamma(2) forming an S3 doublet.
#
# From arXiv:1907.04716 and Okada-Tanimoto 2025:
#   Y1(tau) = (1/(4*pi*i)) * [eta'(tau/2)/eta(tau/2) + eta'((tau+1)/2)/eta((tau+1)/2) - 8*eta'(2*tau)/eta(2*tau)]
#   Y2(tau) = (sqrt(3)/(4*pi*i)) * [eta'(tau/2)/eta(tau/2) - eta'((tau+1)/2)/eta((tau+1)/2)]
#
# But there is a simpler relation via theta functions.
# The space of weight-2 forms for Gamma(2) is spanned by any 2 of:
#   theta_2(tau)^4,  theta_3(tau)^4,  theta_4(tau)^4
# subject to the Jacobi identity: theta_3^4 = theta_2^4 + theta_4^4
#
# The standard S3 doublet basis is:
#   Y1(tau) = (theta_3(q)^4 + theta_4(q)^4) / (2 * eta(q)^8)  [normalized]
#   Y2(tau) = (theta_3(q)^4 - theta_4(q)^4) / (2 * eta(q)^8)  [normalized]
#
# With q-expansion normalization Y1 -> 1/8 + 3q + ..., Y2 -> sqrt(3)*q^(1/2)*(1+...)
#
# The exact normalization depends on convention. Let's use the convention from the
# q-expansion given in the literature:
#   Y1 = 1/8 + 3*q + 3*q^2 + 12*q^3 + 3*q^4 + ...
#   Y2 = sqrt(3) * q^(1/2) * (1 + 4*q + 6*q^2 + 8*q^3 + ...)

# Direct computation from q-expansion (most reliable at q = 1/phi)
def Y1_qexp(q, terms=200):
    """Weight-2 modular form Y1 for Gamma(2), q-expansion."""
    # Y1 = 1/8 + sum_{n>=1} c_n * q^n
    # The coefficients are related to divisor sums.
    # Y1(tau) = (1/12)(E2(tau) - 2*E2(2*tau)) where E2 is the weight-2 Eisenstein
    # But E2 is quasi-modular. For Gamma(2), the weight-2 forms are genuine modular.
    #
    # Actually, the canonical construction uses:
    # Y1 = (1/8)(theta_3(q^2)^4 + theta_4(q^2)^4) with appropriate normalization
    #
    # Let me use the eta-product formula directly.
    # For Gamma(2), the weight-2 modular forms can be expressed as:
    #   f1 = theta_3^4 / eta^8  (but this diverges from standard normalization)
    #
    # Simplest approach: use the UNNORMALIZED theta-function basis
    # and normalize so the doublet satisfies the S3 algebra.
    #
    # The key property is: (Y1, Y2) form an S3 doublet of weight 2.
    # Under T: tau -> tau + 1, (Y1, Y2) -> (Y1, -Y2)  [since T generates Z2 in S3]
    # Under S: tau -> -1/tau, (Y1, Y2) -> tau^2 * R * (Y1, Y2) where R is a rotation

    # Use theta^4 basis directly (unnormalized but well-defined)
    pass

# Use theta function values directly
# Two independent weight-2 forms for Gamma(2):
# Convention 1 (symmetric): Y1 = theta_3^4 + theta_4^4, Y2 = theta_3^4 - theta_4^4
# Convention 2 (Okada): Y1 ~ 1/8 + 3q + ...,  Y2 ~ sqrt(3)*q^(1/2) + ...
#
# The theta^4 values at q = 1/phi:
t3_4 = t3**4
t4_4 = t4**4
t2_4 = t2**4

# Check Jacobi identity: theta_3^4 = theta_2^4 + theta_4^4
jacobi_check = abs(t3_4 - t2_4 - t4_4) / t3_4

# Convention 1: unnormalized
Y1_unnorm = (t3_4 + t4_4) / 2
Y2_unnorm = (t3_4 - t4_4) / 2

# Convention 2: The Okada q-expansion convention
# From q-expansion: Y1 = 1/8 + 3q + 3q^2 + 12q^3 + ...
# Let's compute Y1 numerically from this expansion
def Y1_series(q, terms=500):
    """Compute Y1 from q-expansion coefficients.
    Y1 = 1/8 + sum_{n>=1} sigma_1^odd(n) * q^n  (approximately)
    Actually Y1 is related to a specific Eisenstein-like series for Gamma(2).

    The exact formula: Y1(tau) = 1 + 24*sum_{n=1}^inf n*q^(2n)/(1-q^(2n))
    divided by some normalization...

    Let me compute directly: Y1 = theta_3(q)^4 + theta_4(q)^4,
    normalized so leading term = 1/8.
    """
    val = (theta3_func(q)**4 + theta4_func(q)**4) / 2
    # The leading term of (theta_3^4 + theta_4^4)/2 in q-expansion is:
    # theta_3^4 = 1 + 8q + 24q^2 + 32q^3 + 24q^4 + ...
    # theta_4^4 = 1 - 8q + 24q^2 - 32q^3 + 24q^4 + ...
    # (theta_3^4 + theta_4^4)/2 = 1 + 24q^2 + 24q^4 + ...
    # But the literature says Y1 = 1/8 + 3q + ...
    # These are DIFFERENT normalizations!
    return val

# Let me compute the actual q-expansion terms to identify the right normalization.
# theta_3(q)^4 = (1 + 2q + 2q^4 + 2q^9 + ...)^4
# At leading order in q:
# = 1 + 8q + 24q^2 + 32q^3 + 24q^4 + 48q^5 + ...
# (these are the coefficients r_4(n) = number of representations as sum of 4 squares)

# theta_4(q)^4 = (1 - 2q + 2q^4 - 2q^9 + ...)^4
# = 1 - 8q + 24q^2 - 32q^3 + 24q^4 - 48q^5 + ...

# So:
# (theta_3^4 + theta_4^4)/2 = 1 + 24q^2 + 24q^4 + 96q^6 + ...
# (theta_3^4 - theta_4^4)/2 = 8q + 32q^3 + 48q^5 + ...
#
# But the literature's Y1 = 1/8 + 3q + 3q^2 + 12q^3 + ...
# And Y2 = sqrt(3)*q^(1/2)*(1 + 4q + 6q^2 + ...)
#
# These have a q^(1/2) in Y2, suggesting they use a DIFFERENT nome convention
# or a different basis.
#
# KEY INSIGHT: The literature Y1, Y2 are defined using eta-quotients, NOT
# directly as theta^4. The connection is:
#
# From arXiv:1907.04716 Eq. (7):
#   Y1 = (i/(4*pi)) * [eta'(tau/2)/eta(tau/2) + eta'((tau+1)/2)/eta((tau+1)/2) - 8*eta'(2*tau)/eta(2*tau)]
#   Y2 = (i*sqrt(3)/(4*pi)) * [eta'(tau/2)/eta(tau/2) - eta'((tau+1)/2)/eta((tau+1)/2)]
#
# These are logarithmic derivatives of eta at shifted arguments.
# For numerical computation, use the identity:
#   eta'(tau)/eta(tau) = (2*pi*i/24) * E2(tau)
#   where E2(tau) = 1 - 24*sum_{n>=1} sigma_1(n)*q^n  (Eisenstein series)
#
# But E2 is quasi-modular for SL(2,Z) and weight-2 for Gamma(2).
#
# Alternative approach: use the THETA FUNCTION basis and convert.
# The modular forms of weight 2 for Gamma(2) have dimension 2.
# Any two linearly independent weight-2 forms span the space.
# The S3 doublet property depends on the CHOICE of basis.
#
# For the physics, what matters is the S3-INVARIANT mass matrix,
# which is basis-independent. So let me work with the theta^4 basis
# and derive everything from there.

# PRACTICAL CHOICE: Use the convention where
#   y1 = theta_3^4 / eta^8    (a common normalization in modular form literature)
#   y2 = theta_2^4 / eta^8    (the other independent form)
# or equivalently
#   Y1 = (theta_3^4 + theta_4^4) / (2 * eta^8)
#   Y2 = (theta_3^4 - theta_4^4) / (2 * eta^8)

eta_8 = eta**8

# But eta^8 at q = 1/phi is TINY, so these blow up. Let me just use the
# unnormalized versions for the mass matrix.

# CLEANEST APPROACH: Follow Feruglio's framework directly.
# The mass matrix depends on Y = (Y1, Y2) only through ratios and products.
# So the overall normalization cancels. I'll use:
#   Y1 = theta_3^4 + theta_4^4  (proportional to S3 component 1)
#   Y2 = theta_3^4 - theta_4^4  (proportional to S3 component 2)
# and absorb normalization into the free coupling constants.

Y1 = t3_4 + t4_4
Y2 = t3_4 - t4_4

print(f"""
Weight-2 modular forms for Gamma(2) at q = 1/phi:

  theta_3^4 = {t3_4:.8f}
  theta_4^4 = {t4_4:.8f}
  theta_2^4 = {t2_4:.8f}

  Jacobi identity check: theta_3^4 - theta_2^4 - theta_4^4 = {t3_4-t2_4-t4_4:.2e}
  (relative error: {jacobi_check:.2e})

S3 doublet (Y1, Y2) [unnormalized]:
  Y1 = theta_3^4 + theta_4^4 = {Y1:.8f}
  Y2 = theta_3^4 - theta_4^4 = {Y2:.8f}

Ratio: Y2/Y1 = {Y2/Y1:.8f}
  This is ~1, meaning the two doublet components are COMPARABLE in size.
  At q << 1 (cusp regime), Y2/Y1 -> 0, giving hierarchy.
  At q = 1/phi, there is NO automatic hierarchy within the doublet.
""")

section("2B. Higher-weight modular forms")

# Weight-4 forms from S3 tensor products of (Y1, Y2)
# Using CG: 2 x 2 = 1 + 1' + 2
#   1  (singlet):  Y1*Y1 + Y2*Y2
#   1' (sign):     Y1*Y2 - Y2*Y1 = 0  (vanishes for self-product!)
#   2  (doublet):  (Y1*Y2 + Y2*Y1, Y1*Y1 - Y2*Y2) = (2*Y1*Y2, Y1^2 - Y2^2)

Y4_1  = Y1**2 + Y2**2           # Weight-4 singlet (trivial)
Y4_1p = 0.0                     # Weight-4 sign singlet (vanishes for self-product)
Y4_2a = 2*Y1*Y2                 # Weight-4 doublet component 1
Y4_2b = Y1**2 - Y2**2           # Weight-4 doublet component 2

# Weight-6 forms
# From (Y1, Y2) x (Y4_2a, Y4_2b):  doublet x doublet
Y6_1  = Y1 * Y4_2a + Y2 * Y4_2b    # = 2*Y1^2*Y2 + Y2*(Y1^2 - Y2^2) = 3*Y1^2*Y2 - Y2^3
Y6_1p = Y1 * Y4_2b - Y2 * Y4_2a    # = Y1*(Y1^2 - Y2^2) - 2*Y1*Y2^2 = Y1^3 - 3*Y1*Y2^2
Y6_2a = Y1 * Y4_2b + Y2 * Y4_2a    # = Y1^3 - Y1*Y2^2 + 2*Y1*Y2^2 = Y1^3 + Y1*Y2^2
Y6_2b = Y1 * Y4_2a - Y2 * Y4_2b    # = 2*Y1^2*Y2 - Y1^2*Y2 + Y2^3 = Y1^2*Y2 + Y2^3

# Also: singlet x doublet
Y6_s2a = Y4_1 * Y1   # = (Y1^2 + Y2^2)*Y1
Y6_s2b = Y4_1 * Y2   # = (Y1^2 + Y2^2)*Y2

print(f"""
Weight-4 modular forms:
  1  (singlet):   Y1^2 + Y2^2        = {Y4_1:.6f}
  1' (sign):      [vanishes for Y x Y]
  2a (doublet):   2*Y1*Y2            = {Y4_2a:.6f}
  2b (doublet):   Y1^2 - Y2^2       = {Y4_2b:.6f}

Weight-6 modular forms:
  1  (singlet):   3*Y1^2*Y2 - Y2^3  = {Y6_1:.6f}   (check: {3*Y1**2*Y2 - Y2**3:.6f})
  1' (sign):      Y1^3 - 3*Y1*Y2^2  = {Y6_1p:.6f}   (check: {Y1**3 - 3*Y1*Y2**2:.6f})
  2a (doublet):   Y1^3 + Y1*Y2^2    = {Y6_2a:.6f}   (check: {Y1**3 + Y1*Y2**2:.6f})
  2b (doublet):   Y1^2*Y2 + Y2^3    = {Y6_2b:.6f}   (check: {Y1**2*Y2 + Y2**3:.6f})

Key ratios at q = 1/phi:
  Y2/Y1 = {Y2/Y1:.6f}  (weight 2)
  Y4_2a/Y4_1 = {Y4_2a/Y4_1:.6f}  (weight 4)
  Y4_2b/Y4_1 = {Y4_2b/Y4_1:.6f}  (weight 4)
  Y6_1p/Y6_1 = {Y6_1p/Y6_1:.6f}  (weight 6)
""")


# ============================================================
banner("PART 3: THE YUKAWA MASS MATRIX")
# ============================================================

print("""
CONSTRUCTION PRINCIPLE:
For 3 generations with assignment (psi_1, psi_2) ~ 2 and psi_3 ~ 1' under S3,
the Yukawa coupling must be S3-invariant.

The mass matrix M_ij multiplies: (left-handed)_i * (right-handed)_j

Left-handed:  L = (L1, L2) in 2,  L3 in 1'
Right-handed: R = (R1, R2) in 2,  R3 in 1'

The most general weight-2k Yukawa at leading order:

For the (2,2) block [rows 1-2, columns 1-2]:
  The bilinear L_i * R_j transforms as 2 x 2 = 1 + 1' + 2
  To make S3-invariant with Y doublet:
    - (Y1, Y2) couples to the doublet in L x R
    - Need overall S3 singlet

For L(2) x R(2):
  L1*R1 + L2*R2 -> singlet 1 -> couples to singlet modular form
  L1*R2 - L2*R1 -> singlet 1' -> couples to sign modular form
  (L1*R2 + L2*R1, L1*R1 - L2*R2) -> doublet 2 -> couples to Y doublet

So the (2,2) block of the mass matrix is:
  M_11 = a*(Y1) + c    [from doublet CG: Y1 couples to 11-22, singlet to 11+22]
  M_12 = a*(Y2)        [from doublet CG: Y2 couples to 12+21]
  M_21 = a*(Y2)        [symmetric from doublet CG]
  M_22 = -a*(Y1) + c   [note the minus from CG convention]

Wait -- let me be more careful about the S3 CG conventions.
""")

section("3A. Careful construction of S3-invariant mass matrix")

print("""
S3 CG for DOUBLET x DOUBLET -> SINGLET:
  If a = (a1, a2) in 2 and b = (b1, b2) in 2, then:
    Trivial singlet 1: a1*b1 + a2*b2
    Sign singlet 1':   a1*b2 - a2*b1

S3 CG for DOUBLET x DOUBLET -> DOUBLET:
  (a1*b2 + a2*b1,  a1*b1 - a2*b2)  [components of the resulting doublet]

For mass matrix: we need L_i * R_j * Y_k to contain a singlet.

CASE 1: L in 2, R in 2.
  L_i * R_j has:
    1: L1*R1 + L2*R2 (this is Tr of the matrix -> diagonal part)
    1': L1*R2 - L2*R1 (antisymmetric -> off-diagonal antisymmetric part)
    2: (L1*R2 + L2*R1, L1*R1 - L2*R2)

  To make a singlet from 2 x 2 (the L*R doublet times Y doublet):
    Y1*(L1*R1 - L2*R2) + Y2*(L1*R2 + L2*R1)

  This gives the 2x2 mass matrix block:
    M = a * | Y1    Y2  |  +  c * | 1  0 | * Y4_singlet
            | Y2   -Y1  |         | 0  1 |

  where the first term comes from the doublet channel and the second from
  the singlet channel (which requires a weight-4 singlet modular form to
  balance the weights).

  If we restrict to weight-2 modular forms only (simplest case), the (2,2) block is:
    M_22block = a * | Y1    Y2  |
                    | Y2   -Y1  |

  If we allow a weight-4 singlet:
    M_22block = a * | Y1    Y2  |  +  c * (Y1^2 + Y2^2) * | 1  0 |
                    | Y2   -Y1  |                           | 0  1 |

CASE 2: L in 2, R3 in 1'.
  L_i * R3 transforms as 2 x 1' = 2.
  This couples to Y doublet:
    Y1*L2*R3 + Y2*(-L1)*R3  [using 2 x 1' CG]
  Wait, for 2 x 1': (a1, a2) x b -> (a2*b, -a1*b)
  So L x R3 = (L2*R3, -L1*R3) in doublet.
  Then doublet x doublet -> singlet: Y1*(L2*R3) + Y2*(-L1*R3) = Y1*L2*R3 - Y2*L1*R3

  This gives column 3 of the mass matrix (rows 1,2):
    M_13 = -b * Y2   (coefficient of L1*R3)
    M_23 =  b * Y1   (coefficient of L2*R3)

CASE 3: L3 in 1', R in 2.
  L3 * R_j transforms as 1' x 2 = 2.
  1' x 2: b x (a1, a2) -> (a2*b, -a1*b)
  So L3 * R = (R2*L3, -R1*L3) in doublet.
  Then doublet x doublet -> singlet: Y1*(R2*L3) + Y2*(-R1*L3) = Y1*R2*L3 - Y2*R1*L3

  This gives row 3 of the mass matrix (columns 1,2):
    M_31 = -d * Y2   (coefficient of L3*R1)
    M_32 =  d * Y1   (coefficient of L3*R2)

CASE 4: L3 in 1', R3 in 1'.
  1' x 1' = 1 (trivial singlet).
  So L3*R3 is a singlet. To balance modular weight, couple to a singlet modular form.
  At weight 2: there is no weight-2 singlet (Y is a doublet).
  At weight 4: Y4_1 = Y1^2 + Y2^2 is the singlet.
  At weight 0: just a constant.

  So: M_33 = e * (Y1^2 + Y2^2) [if we need weight 4 for total weight balance]
  Or: M_33 = e * 1             [if no modular weight needed here]

The total modular weight of the Yukawa must be consistent.
In the Feruglio framework, if matter fields have modular weights k_L and k_R,
then the modular form in the Yukawa must have weight k_Y = -(k_L + k_R) + k_H
(where k_H is the Higgs weight, often 0).

For simplicity, let's consider two scenarios:

SCENARIO A: All fermions have modular weight 0.
  Then Y has weight 2, and the Yukawa is weight 2.
  The mass matrix is built entirely from weight-2 forms.

SCENARIO B: Mixed modular weights.
  L1,L2 have weight k, L3 has weight k', etc.
  Higher-weight modular forms enter for different (i,j) entries.
""")

section("3B. Scenario A: Weight-2 mass matrix (most constrained)")

print("""
With all modular forms at weight 2, the mass matrix takes the form:

  M = v * | a*Y1     a*Y2     -b*Y2  |
          | a*Y2    -a*Y1      b*Y1  |
          | -d*Y2    d*Y1      0     |

This has 3 free parameters: a, b, d (complex in general, real in CP-conserving limit).
The (3,3) entry is 0 because 1' x 1' = 1 and there is no weight-2 singlet.

The matrix has ZERO DETERMINANT (since M_33 = 0), so one eigenvalue is always 0.
This naturally gives a HIERARCHY: m_1 = 0, m_2, m_3.

This is the FRITZSCH-like texture from S3! The lightest generation is massless
at leading order -- mass arises from higher-order corrections.
""")

# Compute the weight-2-only mass matrix
def mass_matrix_weight2(a, b, d, Y1_val, Y2_val):
    """Weight-2-only S3 mass matrix. Returns 3x3 matrix."""
    return [
        [ a*Y1_val,   a*Y2_val,  -b*Y2_val],
        [ a*Y2_val,  -a*Y1_val,   b*Y1_val],
        [-d*Y2_val,   d*Y1_val,   0.0      ]
    ]

# Check: what are the singular values?
a_test, b_test, d_test = 1.0, 1.0, 1.0
M_test = mass_matrix_weight2(a_test, b_test, d_test, Y1, Y2)
svs_test = singular_values_3x3(M_test)

print(f"Test matrix (a=b=d=1):")
for row in M_test:
    print(f"  [{row[0]:>10.4f}  {row[1]:>10.4f}  {row[2]:>10.4f}]")
print(f"\nSingular values: {svs_test[0]:.6f}, {svs_test[1]:.6f}, {svs_test[2]:.6f}")
print(f"Ratios: sv2/sv3 = {svs_test[1]/svs_test[2]:.6f}, sv1/sv2 = {svs_test[0]/svs_test[1]:.6f}")
print(f"Overall hierarchy sv1/sv3 = {svs_test[0]/svs_test[2]:.6f}")

print(f"\nAt q = 1/phi, the weight-2 matrix gives at most a factor ~{svs_test[2]/svs_test[0]:.1f} hierarchy.")
print(f"The measured top/up ratio is {m_t/m_u:.0f}.")
print(f"CONCLUSION: Weight-2 alone is GROSSLY INSUFFICIENT for the mass hierarchy.")


section("3C. Scenario B: Mixed-weight mass matrix (realistic)")

print("""
Realistic model: allow different modular weights for different generations.
This is the MODULAR FROGGATT-NIELSEN mechanism.

Following Okada-Tanimoto 2025 (Model I), assign:
  (F1, F2) ~ 2, weight k1
  F3 ~ 1', weight k3

The Yukawa term F_i * F_j^c * H * Y_{ij} requires:
  weight(Y_{ij}) = -(k1_i + k1_j) + k_H  (modular weight balance)

For the (1,1) block: weight k_Y = -2*k1 + k_H
For the (1,3) or (3,1): weight k_Y = -(k1 + k3) + k_H
For the (3,3): weight k_Y = -2*k3 + k_H

Different weights for different blocks create DIFFERENT powers of the nome
in the q-expansion, generating the mass hierarchy.

The MOST GENERAL mass matrix (allowing weights 2, 4, 6) is:

  M = v * | a*Y4_2b + c*Y4_1    a*Y4_2a        -b*Y2_2    e*Y6_1'   |
          | a*Y4_2a             -a*Y4_2b + c*Y4_1  b*Y2_1  f*Y6_1    |
          | -d*Y2_2              d*Y2_1             h*Y4_1             |

where Y2 = (Y2_1, Y2_2), Y4 = (Y4_2a, Y4_2b) are doublets,
Y4_1 is the weight-4 singlet, and Y6 terms are weight-6.

Let me construct the CANONICAL Okada-Tanimoto model.
""")

# The Okada-Orikasa model (arXiv:1907.04716) charged lepton mass matrix:
# M_l = (v_H/sqrt(2)) * [[sigma_l * Y4_1,  gamma_l * Y1,    gamma_l * Y2   ],
#                          [beta_l * Y4_2a,  alpha_l * Y2,    alpha_l * Y1   ],
#                          [beta_l * Y4_2b,  alpha_l * Y1,   -alpha_l * Y2   ]]
#
# where Y4_1 = Y1^2 + Y2^2,  Y4_2a = 2*Y1*Y2,  Y4_2b = Y1^2 - Y2^2
# and alpha_l, beta_l, gamma_l, sigma_l are free coupling constants.

def mass_matrix_okada(alpha, beta, gamma, sigma, Y1v, Y2v):
    """Okada-Orikasa (1907.04716) charged lepton mass matrix structure.
    4 free parameters. Uses weight-2 and weight-4 modular forms.

    Assignment: (L2, L3) ~ 2, L1 ~ 1'; (eR2, eR3) ~ 2, eR1 ~ 1'
    """
    Y4_1 = Y1v**2 + Y2v**2
    Y4_2a = 2*Y1v*Y2v
    Y4_2b = Y1v**2 - Y2v**2

    M = [
        [sigma * Y4_1,   gamma * Y1v,   gamma * Y2v  ],
        [beta * Y4_2a,   alpha * Y2v,   alpha * Y1v  ],
        [beta * Y4_2b,   alpha * Y1v,  -alpha * Y2v  ]
    ]
    return M


section("3D. Parameter counting for each sector")

print("""
PARAMETER COUNTING:

  Okada-Orikasa model (each sector):
    4 complex parameters: alpha, beta, gamma, sigma
    For REAL (CP-conserving) case: 4 real parameters
    Must fit: 3 masses = 3 observables
    System is UNDERCONSTRAINED (4 params for 3 observables)

    For full complex case: 8 real parameters for 3 masses + CP phase
    Still underconstrained.

  To also fit CKM/PMNS:
    Up sector:   4 params -> 3 up masses
    Down sector: 4 params -> 3 down masses + 3 CKM angles + 1 CKM phase
    Lepton:      4 params -> 3 charged lepton masses
    Neutrino:    + params for seesaw -> 3 neutrino masses + 3 PMNS angles + phases
    PLUS: tau (the modulus) = 1 complex parameter (or 1 real for imaginary tau)

  Total free parameters: ~13-17 (sector-dependent)
  Total observables: ~22 (9 masses + 4 CKM + 6 PMNS + 3 neutrino masses)

  With tau FIXED at q = 1/phi: remove 1-2 free parameters.
  -> Still ~12-16 free parameters for ~22 observables.

  This is COMPARABLE to the SM Yukawa sector itself (13 free parameters).
  The modular framework DOES NOT dramatically reduce parameter count
  unless tau is fixed AND the assignment is restrictive.
""")


# ============================================================
banner("PART 4: NUMERICAL FIT -- CHARGED LEPTONS")
# ============================================================

section("4A. Fit charged lepton masses")

# Target mass ratios (better to fit ratios than absolute masses)
m_e_target = m_e
m_mu_target = m_mu
m_tau_target = m_tau

# The mass matrix M gives masses as singular values of M (times v/sqrt(2))
# For the Okada structure, try to find alpha, beta, gamma, sigma
# such that singular values ~ m_e, m_mu, m_tau (up to overall scale)

print(f"""
Target lepton masses (MeV):
  m_e   = {m_e:.6f}
  m_mu  = {m_mu:.4f}
  m_tau = {m_tau:.2f}

Mass ratios:
  m_mu/m_e   = {m_mu/m_e:.4f}
  m_tau/m_e  = {m_tau/m_e:.2f}
  m_tau/m_mu = {m_tau/m_mu:.4f}

Attempting fit with Okada matrix structure...
""")

# Simple optimization: grid search + refinement
# The overall scale is one parameter, leaving 3 parameters for 2 ratios.
# We can normalize: set the overall scale so largest SV = m_tau.

def fit_quality_lepton(params, Y1v, Y2v, targets):
    """Returns sum of squared log-ratio errors."""
    alpha, beta, gamma, sigma = params
    M = mass_matrix_okada(alpha, beta, gamma, sigma, Y1v, Y2v)
    svs = singular_values_3x3(M)

    if svs[2] < 1e-20:
        return 1e10

    # Normalize so largest SV matches largest target
    scale = targets[2] / svs[2]
    pred = [s * scale for s in svs]

    # Log-ratio errors (handle zero singular values with penalty)
    err = 0
    for i in range(3):
        if pred[i] > 1e-30 and targets[i] > 0:
            err += (math.log(pred[i]/targets[i]))**2
        elif targets[i] > 0:
            # Penalize zero prediction for nonzero target
            err += 100.0  # large penalty
    return err

# Simple grid search
lepton_targets = sorted([m_e, m_mu, m_tau])

best_err = 1e10
best_params = None

print("Running grid search for Okada matrix (this may take a moment)...")

count = 0
for alpha in [0.01, 0.05, 0.1, 0.5, 1.0, 2.0, 5.0, 10.0]:
    for beta in [0.001, 0.01, 0.05, 0.1, 0.5, 1.0, 2.0, 5.0, -0.01, -0.1, -1.0, -5.0]:
        for gamma in [0.001, 0.01, 0.05, 0.1, 0.5, 1.0, 2.0, 5.0]:
            for sigma in [1e-5, 1e-4, 1e-3, 0.01, 0.1, 0.5, 1.0]:
                params = (alpha, beta, gamma, sigma)
                err = fit_quality_lepton(params, Y1, Y2, lepton_targets)
                if err < best_err:
                    best_err = err
                    best_params = params
                count += 1

print(f"\nGrid search complete ({count} points).")
print(f"Best error: {best_err:.6f}")
if best_params:
    print(f"Best params: alpha={best_params[0]:.6f}, beta={best_params[1]:.6f}, "
          f"gamma={best_params[2]:.6f}, sigma={best_params[3]:.6f}")

print(f"\nNOTE: With Y1 ~ Y2 ~ 42.6 at q = 1/phi, the Okada matrix has")
print(f"nearly degenerate rows/columns. The smallest singular value is typically")
print(f"ZERO or very small, making it impossible to fit 3 nonzero masses with")
print(f"just 4 parameters in this structure.")

# Refine with local search
def refine_fit(params, Y1v, Y2v, targets, steps=5000, lr=0.01):
    """Simple gradient-free local optimization."""
    best = list(params)
    best_e = fit_quality_lepton(best, Y1v, Y2v, targets)

    for step in range(steps):
        # Random perturbation
        trial = [b * (1 + lr * (2*(hash((step, i)) % 1000)/1000 - 1))
                 for i, b in enumerate(best)]
        # Avoid zero
        trial = [max(abs(t), 1e-10) * (1 if b >= 0 else -1) for t, b in zip(trial, best)]
        e = fit_quality_lepton(trial, Y1v, Y2v, targets)
        if e < best_e:
            best = trial
            best_e = e

        # Decrease learning rate
        if step % 1000 == 999:
            lr *= 0.5

    return tuple(best), best_e

# Better refinement: systematic coordinate descent
def coordinate_descent(params, Y1v, Y2v, targets, iterations=200):
    """Coordinate descent optimization."""
    best = list(params)
    best_e = fit_quality_lepton(best, Y1v, Y2v, targets)

    for iteration in range(iterations):
        for i in range(4):
            # Try multiplying parameter i by various factors
            for factor in [0.5, 0.7, 0.8, 0.9, 0.95, 0.99, 1.01, 1.05, 1.1, 1.2, 1.3, 1.5, 2.0]:
                trial = list(best)
                trial[i] = trial[i] * factor
                e = fit_quality_lepton(trial, Y1v, Y2v, targets)
                if e < best_e:
                    best = trial
                    best_e = e
            # Try flipping sign
            trial = list(best)
            trial[i] = -trial[i]
            e = fit_quality_lepton(trial, Y1v, Y2v, targets)
            if e < best_e:
                best = trial
                best_e = e

    return tuple(best), best_e

refined_params, refined_err = coordinate_descent(best_params, Y1, Y2, lepton_targets)
print(f"\nAfter refinement:")
print(f"Error: {refined_err:.8f}")
print(f"Params: alpha={refined_params[0]:.6f}, beta={refined_params[1]:.6f}, "
      f"gamma={refined_params[2]:.6f}, sigma={refined_params[3]:.6f}")

# Show the resulting masses
M_lep = mass_matrix_okada(refined_params[0], refined_params[1],
                           refined_params[2], refined_params[3], Y1, Y2)
svs_lep = singular_values_3x3(M_lep)
scale_lep = m_tau / svs_lep[2]
pred_lep = [s * scale_lep for s in svs_lep]

print(f"\nPredicted vs measured lepton masses:")
print(f"  {'':12} {'Predicted':>12} {'Measured':>12} {'Ratio':>10} {'Match%':>10}")
for name, pred, meas in [("m_e", pred_lep[0], m_e),
                          ("m_mu", pred_lep[1], m_mu),
                          ("m_tau", pred_lep[2], m_tau)]:
    ratio = pred/meas if meas > 0 else 0
    match = 100 * min(pred, meas) / max(pred, meas)
    print(f"  {name:<12} {pred:>12.6f} {meas:>12.6f} {ratio:>10.6f} {match:>9.2f}%")

print(f"\nMass ratios:")
if pred_lep[0] > 1e-10:
    print(f"  m_mu/m_e:  predicted = {pred_lep[1]/pred_lep[0]:.4f}, measured = {m_mu/m_e:.4f}")
else:
    print(f"  m_mu/m_e:  predicted = inf (m_e = 0!), measured = {m_mu/m_e:.4f}")
    print(f"  NOTE: The Okada matrix structure gives m_e = 0 at this q value.")
    print(f"  This is the FRITZSCH TEXTURE: lightest generation massless at leading order.")
    print(f"  The electron mass would arise from higher-order (weight-6+) corrections.")
print(f"  m_tau/m_mu: predicted = {pred_lep[2]/max(pred_lep[1],1e-20):.4f}, measured = {m_tau/m_mu:.4f}")

section("4B. General S3 mass matrix with weight-2 + weight-4 + weight-6 terms")

print("""
Since Y1 ~ Y2 at q = 1/phi, the Okada matrix is nearly singular.
To get 3 nonzero masses, we need the GENERAL S3 matrix including all
weight terms up to weight 6.

General matrix (6 independent parameters: a, b, c, d, e, f):

  M = | a*Y4_1 + b*Y4_2b    b*Y4_2a         c*Y1 + d*Y6_1p/Y4_1  |
      | b*Y4_2a             a*Y4_1 - b*Y4_2b  c*Y2 - d*Y6_1/Y4_1   |
      | e*Y1 + f*Y6_1p/Y4_1  e*Y2 - f*Y6_1/Y4_1   g*Y4_1          |

But since Y1 ~ Y2, many entries become nearly equal.
Let me instead use a PERTURBATIVE approach.
""")

# The key issue: at q = 1/phi, Y1 and Y2 are nearly equal.
# Define: Y_avg = (Y1 + Y2)/2, delta_Y = (Y1 - Y2)/2
# Then Y1 = Y_avg + delta_Y, Y2 = Y_avg - delta_Y
# with delta_Y / Y_avg ~ 2e-8 (TINY!)

Y_avg = (Y1 + Y2) / 2
delta_Y = (Y1 - Y2) / 2

print(f"Perturbative decomposition:")
print(f"  Y_avg  = (Y1+Y2)/2 = {Y_avg:.8f}")
print(f"  delta_Y = (Y1-Y2)/2 = {delta_Y:.8e}")
print(f"  delta_Y / Y_avg = {delta_Y/Y_avg:.2e}")
print(f"")
print(f"Since delta_Y/Y_avg ~ {delta_Y/Y_avg:.2e}, the S3 doublet is")
print(f"essentially DEGENERATE at q = 1/phi.")
print(f"")
print(f"This means: the S3 symmetry is approximately UNBROKEN!")
print(f"All 3 generations would be nearly degenerate without large")
print(f"differences in the coupling constants.")
print(f"")
print(f"In physical terms: at q = 1/phi, the S3 modular forms cannot")
print(f"distinguish between the two doublet components. The symmetry")
print(f"breaking that separates generations must come from elsewhere:")
print(f"  (a) Different modular WEIGHTS for different blocks")
print(f"  (b) Higher-order corrections (multi-instanton effects)")
print(f"  (c) The domain wall mechanism (Poschl-Teller spectrum)")
print(f"  (d) Or: work in the S-DUAL frame where Y2'/Y1' ~ 10^-36")

section("4C. What DOES distinguish generations at q = 1/phi?")

print(f"""
The modular forms that have DIFFERENT values at q = 1/phi:

  Weight 2: Y1 = {Y1:.6f}, Y2 = {Y2:.6f}  (ratio: {Y2/Y1:.8f})
  Weight 4: Y4_1 = {Y4_1:.4f}, Y4_2b = {Y4_2b:.6f}  (ratio: {Y4_2b/Y4_1:.2e})
  Weight 6: Y6_1 = {Y6_1:.4f}, Y6_1p = {Y6_1p:.4f}  (ratio: {Y6_1p/Y6_1:.8f})

  The ONLY quantity with significant breaking is:
    Y4_2b = Y1^2 - Y2^2 = {Y4_2b:.8f}
  which is proportional to delta_Y * Y_avg.

  But Y4_2b / Y4_1 = {Y4_2b/Y4_1:.2e} -- this is TINY.

  Compare needed hierarchy:
    m_e/m_tau = {m_e/m_tau:.6f}
    m_u/m_t = {m_u/m_t:.2e}

  The modular form hierarchy at q = 1/phi is ~10^-8 (from Y4_2b/Y4_1).
  The needed mass hierarchy is ~10^-5 (charged leptons) to ~10^-5 (quarks).

  Interesting: the SQUARE of the modular hierarchy (10^-8)^2 ~ 10^-16
  would be too extreme, while 10^-8 alone is closer to what's needed
  for some ratios but not others.

KEY FINDING: The only source of hierarchy from modular forms at q = 1/phi
is theta_4^4 = {t4_4:.8e}, which enters as the DIFFERENCE between theta_3^4
and theta_2^4. This tiny quantity is the SEED of all mass hierarchy in the
S3 framework at the golden nome.

  theta_4 = {t4:.8f}
  theta_4^4 = {t4_4:.8e}
  theta_4^4 / theta_3^4 = {t4_4/t3_4:.2e}

  Compare: this is remarkably close to some mass ratios:
    m_e/m_mu = {m_e/m_mu:.6f}
    sqrt(m_e/m_mu) = {math.sqrt(m_e/m_mu):.6f}

  Hypothesis: mass ratios might go as POWERS of theta_4 at q = 1/phi.
  theta_4 = {t4:.8f}
  theta_4^2 = {t4**2:.8e}
  theta_4^4 = {t4**4:.8e}
  theta_4^8 = {t4**8:.2e}

  m_e/m_tau = {m_e/m_tau:.6e}   vs theta_4^2 = {t4**2:.6e}  (NO)
  m_u/m_t = {m_u/m_t:.6e}   vs theta_4^2 = {t4**2:.6e}  (NO)
  m_d/m_b = {m_d/m_b:.6e}   vs theta_4^2 = {t4**2:.6e}  (NO)

  None of the mass ratios match simple powers of theta_4.
""")


# ============================================================
banner("PART 5: NUMERICAL FIT -- QUARKS")
# ============================================================

section("5A. Up-type quarks")

up_targets = sorted([m_u, m_c, m_t])

best_err_u = 1e10
best_params_u = None

for alpha in [0.01, 0.1, 0.5, 1.0, 2.0, 5.0, 10.0]:
    for beta in [0.01, 0.1, 0.5, 1.0, 2.0, 5.0, 10.0, -1.0, -0.1]:
        for gamma in [0.01, 0.1, 0.5, 1.0, 2.0, 5.0, 10.0]:
            for sigma in [0.0001, 0.001, 0.01, 0.1, 0.5, 1.0]:
                params = (alpha, beta, gamma, sigma)
                err = fit_quality_lepton(params, Y1, Y2, up_targets)
                if err < best_err_u:
                    best_err_u = err
                    best_params_u = params

refined_u, refined_err_u = coordinate_descent(best_params_u, Y1, Y2, up_targets)

M_up = mass_matrix_okada(refined_u[0], refined_u[1], refined_u[2], refined_u[3], Y1, Y2)
svs_up = singular_values_3x3(M_up)
scale_up = m_t / svs_up[2]
pred_up = [s * scale_up for s in svs_up]

print(f"Up-quark sector fit:")
print(f"  Params: alpha={refined_u[0]:.6f}, beta={refined_u[1]:.6f}, "
      f"gamma={refined_u[2]:.6f}, sigma={refined_u[3]:.6f}")
print(f"  Error: {refined_err_u:.8f}")
print(f"\n  {'':12} {'Predicted':>12} {'Measured':>12} {'Match%':>10}")
for name, pred, meas in [("m_u", pred_up[0], m_u),
                          ("m_c", pred_up[1], m_c),
                          ("m_t", pred_up[2], m_t)]:
    match = 100 * min(pred, meas) / max(pred, meas)
    print(f"  {name:<12} {pred:>12.4f} {meas:>12.4f} {match:>9.2f}%")

section("5B. Down-type quarks")

down_targets = sorted([m_d, m_s, m_b])

best_err_d = 1e10
best_params_d = None

for alpha in [0.01, 0.1, 0.5, 1.0, 2.0, 5.0, 10.0]:
    for beta in [0.01, 0.1, 0.5, 1.0, 2.0, 5.0, 10.0, -1.0, -0.1]:
        for gamma in [0.01, 0.1, 0.5, 1.0, 2.0, 5.0, 10.0]:
            for sigma in [0.0001, 0.001, 0.01, 0.1, 0.5, 1.0]:
                params = (alpha, beta, gamma, sigma)
                err = fit_quality_lepton(params, Y1, Y2, down_targets)
                if err < best_err_d:
                    best_err_d = err
                    best_params_d = params

refined_d, refined_err_d = coordinate_descent(best_params_d, Y1, Y2, down_targets)

M_down = mass_matrix_okada(refined_d[0], refined_d[1], refined_d[2], refined_d[3], Y1, Y2)
svs_down = singular_values_3x3(M_down)
scale_down = m_b / svs_down[2]
pred_down = [s * scale_down for s in svs_down]

print(f"Down-quark sector fit:")
print(f"  Params: alpha={refined_d[0]:.6f}, beta={refined_d[1]:.6f}, "
      f"gamma={refined_d[2]:.6f}, sigma={refined_d[3]:.6f}")
print(f"  Error: {refined_err_d:.8f}")
print(f"\n  {'':12} {'Predicted':>12} {'Measured':>12} {'Match%':>10}")
for name, pred, meas in [("m_d", pred_down[0], m_d),
                          ("m_s", pred_down[1], m_s),
                          ("m_b", pred_down[2], m_b)]:
    match = 100 * min(pred, meas) / max(pred, meas)
    print(f"  {name:<12} {pred:>12.4f} {meas:>12.4f} {match:>9.2f}%")


# ============================================================
banner("PART 6: THE S-DUAL DESCRIPTION (WEIGHTON MECHANISM)")
# ============================================================

section("6A. S-duality transformation")

print(f"""
The modular S transformation: tau -> -1/tau

For tau = {tau_im:.8f}i (corresponding to q = 1/phi):
  tau' = S(tau) = -1/tau = -1/({tau_im:.8f}i) = i/{tau_im:.8f} = {tau_S_im:.6f}i

The S-dual nome:
  q' = exp(2*pi*i * tau') = exp(-2*pi * {tau_S_im:.6f})
""")

q_dual = math.exp(-2*math.pi*tau_S_im)
print(f"  q' = {q_dual:.2e}")
print(f"  ln(q') = {math.log(q_dual):.4f}")
print(f"  1/q' = {1/q_dual:.2e}")

print(f"""
S-transformation of modular forms:
  eta(tau) = sqrt(-i*tau) * eta(-1/tau)  =>  eta(tau) = sqrt(tau_im) * eta(tau')

  eta at original nome: {eta:.8f}
  sqrt(tau_im) = {math.sqrt(tau_im):.8f}

  eta(tau') should be: eta(tau) / sqrt(tau_im) = {eta/math.sqrt(tau_im):.8f}
""")

# Compute modular forms at the S-dual point
eta_dual = eta_func(q_dual)
t3_dual = theta3_func(q_dual)
t4_dual = theta4_func(q_dual)
t2_dual = theta2_func(q_dual)

print(f"""
Direct computation at q' = {q_dual:.2e}:
  eta(q')    = {eta_dual:.8f}
  theta_3(q') = {t3_dual:.8f}
  theta_4(q') = {t4_dual:.8f}
  theta_2(q') = {t2_dual:.8f}

S-transformation check (eta(tau) = sqrt(Im(tau)) * eta(tau')):
  eta(q) = {eta:.8f}
  sqrt(tau_im) * eta(q') = {math.sqrt(tau_im) * eta_dual:.8f}
  Match: {100 * min(eta, math.sqrt(tau_im)*eta_dual) / max(eta, math.sqrt(tau_im)*eta_dual):.4f}%

NOTE: The S-transformation formula uses eta(tau) = sqrt(-i*tau) * eta(-1/tau),
which for purely imaginary tau = i*t gives:
  eta(i*t) = sqrt(t) * eta(i/t)  [NOT sqrt(i*t), see modular form conventions]
  -> This should be: eta(q) = sqrt(tau_im) * eta(q')  [up to phases]
""")

# Check the S-transformation more carefully
# For tau = i*t (purely imaginary):
# eta(i*t) = sqrt(1/t) * eta(i/t)  [standard formula, note 1/t not t]
# So eta(q) should equal sqrt(1/tau_im) * eta(q')

check_S = math.sqrt(1.0/tau_im) * eta_dual
print(f"  Corrected: sqrt(1/tau_im) * eta(q') = {check_S:.8f}")
print(f"  vs eta(q) = {eta:.8f}")
print(f"  Corrected match: {100 * min(eta, check_S) / max(eta, check_S):.4f}%")

section("6B. Mass hierarchy in the S-dual picture")

print(f"""
In the S-dual frame (q' ~ {q_dual:.2e}), the Fourier expansion converges FAST.
The nome q' is tiny, so modular forms have extreme hierarchy:

  Y1(tau') ~ 1 + O(q')  (nearly constant)
  Y2(tau') ~ q'^(1/2) * (...)  (exponentially suppressed)

S-dual modular form values:
  theta_3(q')^4 = {t3_dual**4:.8f}  (nearly 1)
  theta_4(q')^4 = {t4_dual**4:.8f}  (nearly 1)
  theta_2(q')^4 = {t2_dual**4:.2e}  (exponentially small!)

  Y1' = theta_3'^4 + theta_4'^4 = {t3_dual**4 + t4_dual**4:.8f}
  Y2' = theta_3'^4 - theta_4'^4 = {t3_dual**4 - t4_dual**4:.2e}

  Y2'/Y1' = {(t3_dual**4 - t4_dual**4)/(t3_dual**4 + t4_dual**4):.2e}

So in the S-dual description:
  Y2/Y1 ratio ~ {(t3_dual**4 - t4_dual**4)/(t3_dual**4 + t4_dual**4):.2e}  (EXTREME hierarchy!)

Compare to original:
  Y2/Y1 ratio ~ {Y2/Y1:.6f}  (no hierarchy)

THE KEY INSIGHT:
  At q = 1/phi, the doublet components Y1, Y2 are comparable -> no hierarchy from
  the doublet structure alone. The mass hierarchy must come from the FREE PARAMETERS
  (coupling constants a, b, c, d) rather than from the modular forms themselves.

  At q' = S-dual, the doublet has extreme hierarchy -> automatic mass hierarchy,
  but the S-transformation mixes the parameters too.

  The Feruglio-Strumia tension is REAL: q = 1/phi is NOT in the hierarchical
  regime for the modular forms. Hierarchy comes from parameter tuning, not from
  the nome.
""")


# ============================================================
banner("PART 7: FRAMEWORK FORMULAS vs FERUGLIO MASS MATRIX")
# ============================================================

section("7A. The framework's fermion mass formulas")

print("""
The Interface Theory's current mass formulas (from llm-context.md and FINDINGS):

  Charged leptons:
    m_e = 0.51100 MeV (input, not derived)
    m_mu = from Casimir/kink calculation (not from modular forms directly)
    m_tau = combined formula

  Up quarks:
    m_u = m_e * phi^3 = {:.4f} MeV (measured: {:.4f})
    m_c = m_t * alpha = {:.2f} MeV (measured: {:.2f})
    m_t = m_e * mu^2/10 = {:.2f} MeV (measured: {:.2f})

  Down quarks:
    m_b/m_c = phi^(5/2) = {:.4f}

  Key structural feature: the formulas involve {{m_e, mu, phi, alpha, integers}}.
  They do NOT directly use modular forms {{Y1, Y2, eta, theta}}.
""".format(
    m_e * phi**3, m_u,
    m_t * alpha_em, m_c,
    m_e * mu_ratio**2 / 10, m_t,
    phi**2.5
))

section("7B. Can the framework formulas be expressed as Feruglio mass matrix entries?")

print("""
Key question: are the framework's searched formulas EQUIVALENT to
the Feruglio mass matrix at q = 1/phi?

Test 1: m_t = m_e * mu^2 / 10
  In modular language: the top quark mass involves mu (proton/electron ratio),
  which is itself claimed to be 6^5/phi^3 (the framework's mu formula).
  If this is true, m_t = m_e * (6^5/phi^3)^2 / 10 = m_e * 6^10 / (10*phi^6)
  = {:.2f} MeV

  In the Feruglio matrix, the top mass is the LARGEST singular value.
  At q = 1/phi, it would be ~ v * |alpha_33| * f(Y1, Y2),
  where f is some function of modular forms.

  There's no obvious way that Y1, Y2 (which are O(1) numbers at q = 1/phi)
  produce the specific combination 6^5/phi^3 = mu.
""".format(m_e * (7776/phi**3)**2 / 10))

print("""
Test 2: m_u = m_e * phi^3
  phi^3 = {:.6f}
  In the Feruglio matrix, this would be a small singular value.
  phi^3 is a PURE golden ratio power -> consistent with Froggatt-Nielsen
  where mass ~ q^k with q = 1/phi. Here k = 3 (three powers of phibar suppression).

Test 3: m_b/m_c = phi^(5/2)
  phi^(5/2) = {:.6f}
  Again a pure golden ratio power -> k = 5/2 (half-integer weight difference).
  This IS what the modular FN mechanism predicts for delta_k = 5/2.

Test 4: m_c = m_t * alpha
  alpha = 1/137.036 = {:.6f}
  alpha is NOT a simple modular form value at q = 1/phi.
  The framework derives alpha from modular forms: alpha ~ [theta_4/(theta_3*phi)]*(1-...)
  So m_c/m_t = alpha IS a modular form expression, just a complicated one.
""".format(phi**3, phi**2.5, alpha_em))

section("7C. Equivalence test: modular forms as building blocks")

print(f"""
At q = 1/phi, the fundamental modular quantities are:
  eta     = {eta:.8f}      (= alpha_s in framework)
  theta_3 = {t3:.8f}
  theta_4 = {t4:.8f}
  theta_2 = {t2:.8f}

The framework's key physical constants in terms of these:
  alpha = [theta_4/(theta_3*phi)] * (1 - eta*theta_4*phi^2/2) = {(t4/(t3*phi))*(1 - eta*t4*phi**2/2):.8f}
    vs measured 1/137.036 = {alpha_em:.8f}

  mu = 6^5/phi^3 = {7776/phi**3:.4f}
    NOT an obvious modular form expression.

  The framework's alpha uses theta_3, theta_4, eta, phi.
  But mu uses only phi and the integer 6.

CONCLUSION: The framework's mass formulas are NOT simply the Feruglio mass
matrix evaluated at q = 1/phi. They are a HYBRID:
  - Some ratios (m_u/m_e ~ phi^3, m_b/m_c ~ phi^(5/2)) are pure golden-power
    expressions consistent with modular FN at q = 1/phi.
  - Other formulas (m_t ~ mu^2, m_c ~ m_t*alpha) use mu and alpha, which
    themselves involve theta functions but in NON-STANDARD ways.
  - The mu formula (6^5/phi^3) uses the integer 6 and phi, but NOT modular forms
    directly. It could be a coincidence or could relate to the E8 structure.

The framework is NOT Feruglio's program with tau fixed.
It is something MORE SPECIFIC but LESS SYSTEMATIC.
""")


# ============================================================
banner("PART 8: WHAT THE S3 MATRIX PREDICTS")
# ============================================================

section("8A. CKM from misalignment of up and down mass matrices")

print("""
In the S3 modular framework, the CKM matrix arises from the MISALIGNMENT
between the up-quark and down-quark mass matrices:

  V_CKM = U_uL^dag * U_dL

where U_uL and U_dL are the left-handed rotation matrices that diagonalize
M_u * M_u^dag and M_d * M_d^dag respectively.

With the SAME tau (same Y1, Y2 values) for both sectors, the CKM angles
are determined by the DIFFERENCES in coupling constants between sectors.

For a rough prediction at q = 1/phi:
""")

# Compute CKM-like mixing from our fitted up and down matrices
# The CKM matrix is V = U_uL^dag * U_dL

# First, compute M * M^dag for each sector
def mat_mul_transpose(M):
    """Compute M * M^T for a 3x3 matrix"""
    Mt = mat_transpose(M)
    return mat_mul(M, Mt)

# The mixing angles come from the ratio of off-diagonal to diagonal elements
# For a rough estimate, use the Wolfenstein-like parameterization

# The Cabibbo angle is approximately:
# theta_C ~ |M_12/M_22| ~ |Y2/Y1| (from the mass matrix structure)
# At q = 1/phi: |Y2/Y1| = |theta_3^4 - theta_4^4|/|theta_3^4 + theta_4^4|

cabibbo_pred = abs(Y2/Y1)
print(f"  Naive Cabibbo prediction: |Y2/Y1| = {cabibbo_pred:.6f}")
print(f"  Measured V_us = {V_us_meas:.4f}")
print(f"  Match: {100*min(cabibbo_pred, V_us_meas)/max(cabibbo_pred, V_us_meas):.1f}%")
print()

# The Cabibbo angle in the S3 framework depends on the DIFFERENCE between
# up and down sector parameters, not just Y2/Y1.
# But Y2/Y1 sets a NATURAL SCALE for the off-diagonal mixing.

# At q << 1 (cusp): Y2/Y1 ~ 0, so mixing is small -> realistic
# At q = 1/phi: Y2/Y1 ~ 1, so mixing is LARGE -> unrealistic without fine-tuning

print(f"""
  PROBLEM: At q = 1/phi, Y2/Y1 = {Y2/Y1:.4f} ~ 1.
  This means the NATURAL mixing angle is O(1), not small.
  Getting the small Cabibbo angle (0.22) requires cancellation between
  the up and down sector contributions.

  In the cusp regime (q << 1): Y2/Y1 ~ 0, giving naturally small mixing.
  In the S-dual picture (q' ~ {q_dual:.2e}): Y2'/Y1' ~ {abs((t3_dual**4 - t4_dual**4)/(t3_dual**4 + t4_dual**4)):.2e}
  The S-dual gives naturally small mixing -> realistic CKM structure.
""")

section("8B. PMNS predictions")

print("""
The PMNS matrix comes from the misalignment between charged leptons and neutrinos.
In the S3 framework, the neutrino mass matrix (via seesaw) also uses Y1, Y2.

For the PMNS solar angle, the framework already predicts:
  sin^2(theta_12) = 1/3 - theta_4 * sqrt(3/4) = {:.4f}
  Measured: {:.4f}

This formula uses theta_4 directly -- it IS a modular form expression.
But it's NOT derived from the standard S3 mass matrix diagonalization.

The S3 modular mass matrix would predict PMNS angles from the STRUCTURE
of the lepton mass matrices (charged lepton + neutrino sectors), NOT from
an ad hoc formula involving theta_4.

This is a DIFFERENT mechanism from the framework's current approach.
""".format(1/3 - t4*math.sqrt(3/4), sin2_t12_meas))

section("8C. New mass relations from S3 structure")

print("""
The S3 modular mass matrix at q = 1/phi implies some STRUCTURAL relations:

1. The weight-2-only matrix always has det(M) = 0.
   -> One generation is massless at leading order.
   -> Lightest fermion mass arises from higher-order corrections.
   -> This is compatible with m_u being small (but m_u != 0 experimentally).

2. The eigenvalue ratio m_2/m_3 depends on |Y2/Y1|^2.
   At q = 1/phi: |Y2/Y1|^2 = {:.6f}
   This gives m_2/m_3 ~ {:.4f} (for simple parameter choices)
   Compare: m_c/m_t = {:.6f}, m_s/m_b = {:.6f}, m_mu/m_tau = {:.6f}

   None of these match well -> the simple structure doesn't work.

3. For the specific Okada matrix structure, the eigenvalue constraint is:
   m1 * m2 * m3 proportional to det(M), which involves products of Y1, Y2.
   At q = 1/phi: det = 0 for weight-2-only case.

4. The KOIDE RELATION: (m_e + m_mu + m_tau)/(sqrt(m_e) + sqrt(m_mu) + sqrt(m_tau))^2 = 2/3
   Measured: {:.8f}
   Can the S3 matrix reproduce this? Only for specific parameter choices.
""".format(
    (Y2/Y1)**2,
    abs(Y2/Y1),
    m_c/m_t, m_s/m_b, m_mu/m_tau,
    (m_e + m_mu + m_tau) / (math.sqrt(m_e) + math.sqrt(m_mu) + math.sqrt(m_tau))**2
))


# ============================================================
banner("PART 9: THE CRITICAL ASSESSMENT")
# ============================================================

section("9A. Summary of findings")

print(f"""
======================================================================
THE S3 MODULAR MASS MATRIX AT q = 1/phi: CRITICAL ASSESSMENT
======================================================================

1. MODULAR FORMS AT q = 1/phi:
   - The weight-2 S3 doublet (Y1, Y2) is WELL-DEFINED.
   - Both components are O(1): Y1 = {Y1:.4f}, Y2 = {Y2:.4f}, ratio = {Y2/Y1:.4f}.
   - NO automatic hierarchy within the doublet.
   - This is because q = 1/phi = 0.618 is NOT small.

2. MASS HIERARCHY:
   - The Feruglio mass matrix at q = 1/phi does NOT naturally produce
     the observed mass hierarchies (m_t/m_u ~ 80000).
   - Hierarchy must come from PARAMETER TUNING in the coupling constants,
     not from the modular forms themselves.
   - In contrast, at q << 1 (near cusp), modular forms give hierarchy for free.

3. CKM MIXING:
   - At q = 1/phi, Y2/Y1 ~ 1, giving naturally LARGE mixing angles.
   - The observed Cabibbo angle (0.22) requires cancellation.
   - In the S-dual picture (q' ~ {q_dual:.2e}), mixing is naturally small.

4. PARAMETER COUNTING:
   - The Okada-type mass matrix has 4 free parameters per sector.
   - For 3 sectors + tau: ~13-17 free parameters.
   - This is comparable to the SM Yukawa sector (13 parameters).
   - Fixing tau at q = 1/phi saves 1-2 parameters.
   - NET GAIN: ~1-2 fewer free parameters than SM. Modest.

5. FRAMEWORK vs FERUGLIO:
   - The framework's formulas are NOT equivalent to the Feruglio mass matrix.
   - Some mass ratios (m_u/m_e ~ phi^3, m_b/m_c ~ phi^(5/2)) are consistent
     with modular Froggatt-Nielsen at q = 1/phi.
   - Other formulas (m_t ~ mu^2, m_c ~ alpha*m_t) involve quantities (mu, alpha)
     that are themselves derived from modular forms but in non-standard ways.
   - The framework is a HYBRID: part modular forms, part numerology,
     part E8 structure.

6. THE FERUGLIO-STRUMIA TENSION:
   - Feruglio-Strumia (2025) shows hierarchical masses require tau near
     i, i*infinity, or omega.
   - q = 1/phi gives tau = 0.077i, which is NONE of these.
   - The S-dual tau' = 13.1i is closer to the cusp (i*infinity).
   - Resolution possibility: work in the S-DUAL frame where the hierarchy
     is natural, then map back. But this changes the S3 representation
     assignments and coupling structure.

7. WHAT WORKS:
   - S3 = Gamma(2) IS the right group (matches E8's A2 Weyl group).
   - The Fritzsch-like texture (one massless generation) is natural.
   - Pure phi-power mass ratios ARE compatible with modular FN mechanism.
   - The mathematical framework is well-defined and computable.

8. WHAT DOESN'T WORK:
   - q = 1/phi is in the WRONG regime for automatic mass hierarchy.
   - Parameter count is not significantly reduced vs SM.
   - The framework's actual mass formulas are not the Feruglio matrix.
   - The mu formula (6^5/phi^3) has no clear modular form interpretation.
""")

section("9B. Key prediction: is alpha_s = eta(1/phi) connected to the mass matrix?")

print(f"""
The framework's most striking claim: alpha_s = eta(1/phi) = {eta:.6f}

In the S3 modular mass matrix, eta(q) appears in the NORMALIZATION of the
modular forms (e.g., Y_normalized = Y / eta^8), but NOT directly in the
mass eigenvalues.

The mass eigenvalues depend on Y1, Y2 and the coupling constants.
eta enters only through the normalization convention.

However, in the modular Froggatt-Nielsen mechanism, mass ~ q^k, and
eta(q) = q^(1/24) * prod(1-q^n) is closely related to q.
At q = 1/phi: eta = phibar^(1/24) * prod(1 - phibar^n)

The connection alpha_s = eta(1/phi) is NOT a prediction of the S3 mass matrix.
It is a SEPARATE numerical observation about the Dedekind eta function.
If true, it would be a striking coincidence or a deep connection -- but the
S3 mass matrix framework does not explain WHY alpha_s should equal eta.

Final answer: The S3 modular mass matrix at q = 1/phi is a VALID mathematical
construction but does NOT naturally reproduce the observed fermion mass hierarchy
without parameter tuning. The framework's searched mass formulas are not
equivalent to the Feruglio matrix. The most promising direction is to work in
the S-DUAL frame and investigate whether the extreme hierarchy at q' ~ 10^-36
can be mapped back to produce the observed masses.
""")


# ============================================================
banner("PART 10: NUMERICAL SUMMARY TABLE")
# ============================================================

print(f"""
{'='*78}
MODULAR FORM VALUES AT q = 1/phi = {phibar:.10f}
{'='*78}

{'Quantity':<30} {'Value':>15} {'Notes':<30}
{'-'*78}
tau (imaginary)                  {tau_im:>15.8f} Very small Im(tau)
tau' = S(tau)                    {tau_S_im:>15.6f} Large Im(tau') -> near cusp
q = exp(-2pi*Im(tau))            {q_golden:>15.10f} Golden nome
q' = exp(-2pi*Im(tau'))          {q_dual:>15.2e} Exponentially small

eta(q)                           {eta:>15.8f} = alpha_s (framework claim)
theta_2(q)                       {t2:>15.8f}
theta_3(q)                       {t3:>15.8f}
theta_4(q)                       {t4:>15.8f}

Y1 = theta_3^4 + theta_4^4      {Y1:>15.8f} S3 doublet component 1
Y2 = theta_3^4 - theta_4^4      {Y2:>15.8f} S3 doublet component 2
Y2/Y1 (hierarchy indicator)      {Y2/Y1:>15.8f} ~1 -> no hierarchy

Y4_singlet = Y1^2 + Y2^2        {Y4_1:>15.6f} Weight-4 singlet
Y4_doublet = (2Y1Y2, Y1^2-Y2^2) {Y4_2a:>15.6f}
                                 {Y4_2b:>15.6f}

eta(q')                          {eta_dual:>15.8f} Near 1 at cusp
theta_3(q')                      {t3_dual:>15.8f} Near 1 at cusp
theta_4(q')                      {t4_dual:>15.8f} Near 1 at cusp

Y1' = t3'^4 + t4'^4             {t3_dual**4 + t4_dual**4:>15.8f}
Y2' = t3'^4 - t4'^4             {t3_dual**4 - t4_dual**4:>15.2e} TINY -> extreme hierarchy
Y2'/Y1'                          {(t3_dual**4 - t4_dual**4)/(t3_dual**4 + t4_dual**4):>15.2e} Natural hierarchy in S-dual

{'='*78}
LEPTON MASS FIT (Okada matrix, 4 params + overall scale)
{'='*78}
{'':12} {'Predicted':>12} {'Measured':>12} {'Match':>10}
""")

for name, pred, meas in [("m_e", pred_lep[0], m_e),
                          ("m_mu", pred_lep[1], m_mu),
                          ("m_tau", pred_lep[2], m_tau)]:
    match = 100 * min(pred, meas) / max(pred, meas)
    print(f"  {name:<12} {pred:>12.6f} {meas:>12.6f} {match:>9.2f}%")

print(f"""
{'='*78}
UP QUARK MASS FIT (Okada matrix, 4 params + overall scale)
{'='*78}
{'':12} {'Predicted':>12} {'Measured':>12} {'Match':>10}
""")

for name, pred, meas in [("m_u", pred_up[0], m_u),
                          ("m_c", pred_up[1], m_c),
                          ("m_t", pred_up[2], m_t)]:
    match = 100 * min(pred, meas) / max(pred, meas)
    print(f"  {name:<12} {pred:>12.4f} {meas:>12.4f} {match:>9.2f}%")

print(f"""
{'='*78}
DOWN QUARK MASS FIT (Okada matrix, 4 params + overall scale)
{'='*78}
{'':12} {'Predicted':>12} {'Measured':>12} {'Match':>10}
""")

for name, pred, meas in [("m_d", pred_down[0], m_d),
                          ("m_s", pred_down[1], m_s),
                          ("m_b", pred_down[2], m_b)]:
    match = 100 * min(pred, meas) / max(pred, meas)
    print(f"  {name:<12} {pred:>12.4f} {meas:>12.4f} {match:>9.2f}%")

print(f"""
{'='*78}
CRITICAL CONCLUSION
{'='*78}

The S3 modular mass matrix at q = 1/phi CAN fit fermion masses with 4-5
parameters per sector (comparable to the SM). But it does NOT naturally
produce the observed hierarchy -- the hierarchy must be put in by hand
through the coupling constants.

The framework's searched mass formulas (m_t = m_e*mu^2/10, m_u = m_e*phi^3, etc.)
are NOT derivable from the standard Feruglio mass matrix. They appear to be
a DIFFERENT approach that happens to share some features (S3 symmetry, phi powers)
with the modular framework.

The most promising path forward:
1. Work in the S-DUAL frame (q' ~ 10^-36) where hierarchy is natural
2. Derive the modular WEIGHTS of each generation from E8 structure
3. Show that the weight assignments in the S-dual reproduce the specific
   mass formulas the framework uses
4. Or: abandon the Feruglio mass matrix and derive masses directly from
   the Jackiw-Rebbi spectrum of the domain wall (Poschl-Teller n=2)

The q = 1/phi point IS algebraically distinguished, but it is NOT a good
point for the standard modular FN mechanism. Either the mechanism must be
modified, or the masses come from a different source (domain wall spectrum).
""")
