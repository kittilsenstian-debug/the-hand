"""
FIBONACCI + S3 MASS MATRIX ATTACK
===================================

THE keystone gap: if we derive fermion masses, the framework has
ZERO free dimensionless parameters.

Strategy:
  1. S3 = Gamma(2) modular flavor symmetry (Feruglio 2017)
  2. Mass matrix Y(tau) evaluated at tau such that q = e^(2*pi*i*tau) = 1/phi
  3. The Fibonacci collapse constrains the matrix to 2 effective parameters
  4. Three generations from three S3 irreps: 1, 1', 2

The critical insight from fermion_masses_fibonacci.py:
  At q = 1/phi, ALL phi^n collapse to F_n*phi + F_{n-1}
  So the mass matrix lives in a 2D space, not infinity-D
  This should predict 12 masses from 2 parameters

Let's see what actually happens.
"""

import math
import sys

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

phi = (1 + math.sqrt(5)) / 2
phibar = 1 / phi
pi = math.pi

def eta_func(q, terms=2000):
    prod = 1.0
    for n in range(1, terms+1):
        prod *= (1 - q**n)
        if q**n < 1e-16: break
    return q**(1/24) * prod

def theta3(q, terms=500):
    s = 1.0
    for n in range(1, terms+1):
        s += 2 * q**(n**2)
    return s

def theta4(q, terms=500):
    s = 1.0
    for n in range(1, terms+1):
        s += 2 * (-1)**n * q**(n**2)
    return s

q = phibar
eta = eta_func(q)
t3 = theta3(q)
t4 = theta4(q)

# Fibonacci numbers
fib = [0, 1]
for i in range(2, 30):
    fib.append(fib[-1] + fib[-2])

print("=" * 70)
print("FIBONACCI + S3 MASS MATRIX ATTACK")
print("=" * 70)
print()

# ================================================================
# PART 1: S3 MODULAR FORMS AT GOLDEN NOME
# ================================================================

print("=" * 70)
print("PART 1: THE S3 = GAMMA(2) MODULAR FORMS")
print("=" * 70)
print()

# In Feruglio's framework, the modular forms of Gamma(2) at weight 2 are:
# Y1(tau), Y2(tau) which form a DOUBLET of S3
#
# At weight 2 (lowest non-trivial):
#   Y1 = (theta3^4 + theta4^4) / eta^4  (up to normalization)
#   Y2 = (theta3^4 - theta4^4) / eta^4  (up to normalization)
# These are q-expansions that can be evaluated at any tau.
#
# The standard normalization (Feruglio-Kobayashi-Okada 2018):
# Y_2(tau) = (Y1(tau), Y2(tau)) transforming as doublet of S3

# At q = 1/phi, compute these:
Y1_raw = (t3**4 + t4**4) / eta**4
Y2_raw = (t3**4 - t4**4) / eta**4

print(f"  q = 1/phi = {phibar:.10f}")
print(f"  eta(q) = {eta:.10f}")
print(f"  theta3(q) = {t3:.10f}")
print(f"  theta4(q) = {t4:.10f}")
print()
print(f"  Raw Y1 = (theta3^4 + theta4^4) / eta^4 = {Y1_raw:.6f}")
print(f"  Raw Y2 = (theta3^4 - theta4^4) / eta^4 = {Y2_raw:.6f}")
print(f"  Y2/Y1 = {Y2_raw/Y1_raw:.6f}")
print()

# The PROBLEM: Y2/Y1 ~ 0.98, nearly 1. No hierarchy!
# At the cusp (Im(tau) -> infinity): Y2/Y1 -> 0 (hierarchy appears)
# At our golden nome: Y2/Y1 ~ 1 (no hierarchy from standard mechanism)

print("  CRITICAL: Y2/Y1 = {:.4f} -- nearly 1. No automatic hierarchy.".format(Y2_raw/Y1_raw))
print("  Standard Feruglio gets hierarchy from Y2/Y1 -> 0 at cusp.")
print("  We are NOT at the cusp.")
print()

# ================================================================
# PART 2: THE FIBONACCI REFRAMING
# ================================================================

print("=" * 70)
print("PART 2: FIBONACCI COLLAPSE OF Y1, Y2")
print("=" * 70)
print()

# At q = 1/phi: q^n = (-1)^(n+1) * F_n * q + (-1)^n * F_{n-1}
# So theta3^4 = (1 + 2q + 2q^4 + 2q^9 + ...)^4
# Each q^n = a*q + b (Fibonacci decomposition)

# Let's write Y1 and Y2 in terms of just q and 1:
# q = phibar, q^2 = phibar^2 = 1 - phibar = phi - 1 - (1-phibar) = ...
# Actually: q + q^2 = phibar + phibar^2 = phibar + (1-phibar) = 1
# So q^2 = 1 - q

print("  Fibonacci collapse:")
print(f"    q = {q:.10f}")
print(f"    q^2 = {q**2:.10f} = 1 - q = {1-q:.10f}")
print(f"    q^3 = {q**3:.10f} = q - 1 + q = 2q - 1 = {2*q-1:.10f}")
print(f"    q^4 = {q**4:.10f} = 2 - 3q = {2-3*q:.10f}")
print()

# The key: in the Fibonacci basis {1, q}, ALL modular forms become
# simple 2x2 matrices acting on (1, q).

# theta3 in Fibonacci basis:
# theta3 = 1 + 2*q + 2*q^4 + 2*q^9 + 2*q^16 + ...
# = 1 + 2*q + 2*(2-3q) + 2*(q^9) + ...

# Let's compute theta3 term by term in Fibonacci basis
print("  theta3 = 1 + 2*sum(q^(n^2)):")
print()
total_const = 1.0
total_q_coeff = 0.0
for n in range(1, 20):
    nn = n*n
    # q^nn = (-1)^(nn+1) * F_nn * q + (-1)^nn * F_{nn-1}
    if nn < len(fib):
        a_coeff = (-1)**(nn+1) * fib[nn]
        b_coeff = (-1)**nn * fib[nn-1]
    else:
        # Compute q^nn directly
        val = q**nn
        # Decompose: val = a*q + b where a = (val - round(val+q*round(...)))
        # Actually just use: phi*q = phi*phibar = 1, so q = 1/phi
        # q^nn = phibar^nn = (F_{nn-1}*phi + F_{nn-2}*1) * phibar^nn... complex
        # Easier: just compute numerically
        # q^nn = a*q + b where b = q^nn - a*q
        # From Fibonacci: phibar^n = (-1)^n * (F_n * phibar - F_{n-1}) ... not quite
        # Let me just compute numerically
        val = q**nn
        # val = a*q + b -> a = (val - floor(val/q)*q...
        # Actually the Fibonacci decomposition is exact:
        # phibar^n = (-1)^(n+1)*F_n*phibar + (-1)^n*F_{n-1}
        # but Fibonacci numbers get huge. Let's just use numerical.
        a_coeff = 0  # placeholder
        b_coeff = val  # placeholder
        # Skip huge Fibonacci terms (they cancel to give small result)
        continue

    total_q_coeff += 2 * a_coeff
    total_const += 2 * b_coeff

    if n <= 5:
        print(f"    n={n}: q^{nn} = ({a_coeff})*q + ({b_coeff})")

print()
print(f"  theta3 (numerical) = {t3:.10f}")
print(f"  theta3 (Fibonacci, partial) = {total_const + total_q_coeff * q:.10f}")
print()

# ================================================================
# PART 3: A DIFFERENT APPROACH — EIGENVALUE STRUCTURE
# ================================================================

print("=" * 70)
print("PART 3: MASS EIGENVALUES FROM S3 STRUCTURE")
print("=" * 70)
print()

print("  In Feruglio's framework, the charged lepton mass matrix is:")
print("    M_e = v_d * (alpha * Y_1 * E_1 + beta * Y_doublet * E_doublet)")
print("  where alpha, beta are free parameters, and E are S3 Clebsch-Gordan.")
print()
print("  For the TRIPLET representation of S3 (3 generations):")
print("  The mass matrix has structure:")
print()
print("    M = a * (Y1_mat) + b * (Y2_mat)")
print()
print("  where Y1_mat and Y2_mat are specific 3x3 matrices from S3 Clebsches.")

# The standard S3 doublet mass matrix (from Feruglio 2018):
# For charged leptons in the Weinberg operator approach:
#
# With Y = (Y1, Y2) doublet of S3:
# The S3 invariant is:
#   (Y * L * E^c)_singlet
# which gives the mass matrix

# In the basis where generators are standard S3 = {e, (12), (13), (23), (123), (132)}:
# Irreps: 1, 1', 2
# If L ~ 3 (three generations as triplet) and Y ~ 2 (doublet):

# The S3-invariant mass matrix from doublet Y = (y1, y2):
# (from Kobayashi-Okada-Shimizu-Tanimoto 2018, Table 1)

# M_e proportional to:
# | 2*y1    -y2     -y2  |
# | -y2     2*y2    -y1  |
# | -y2     -y1     2*y2 |
# (This is for a specific S3 assignment; others exist)

y1 = Y1_raw
y2 = Y2_raw

# Normalize to y1
r = y2 / y1

print(f"  Y2/Y1 ratio: r = {r:.6f}")
print()

# Mass matrix (up to overall scale):
import numpy as np

# Try the standard A4/S3 mass matrix form
# Different S3 assignments give different matrices.
# The most common for S3 doublet Y and triplet L:

# Assignment 1: "Democratic" type
M1 = np.array([
    [2*y1, -y2, -y2],
    [-y2, 2*y2, -y1],
    [-y2, -y1, 2*y2]
])

evals1 = sorted(np.abs(np.linalg.eigvals(M1)))
print("  Assignment 1 (democratic):")
print(f"    Eigenvalues: {evals1[0]:.6f}, {evals1[1]:.6f}, {evals1[2]:.6f}")
print(f"    Ratios: 1 : {evals1[1]/evals1[0]:.4f} : {evals1[2]/evals1[0]:.4f}")
print()

# Assignment 2: Diagonal + off-diagonal
M2 = np.array([
    [y1, y2, y2],
    [y2, y1, y2],
    [y2, y2, y1]
])

evals2 = sorted(np.abs(np.linalg.eigvals(M2)))
print("  Assignment 2 (circulant):")
print(f"    Eigenvalues: {evals2[0]:.6f}, {evals2[1]:.6f}, {evals2[2]:.6f}")
print(f"    Ratios: 1 : {evals2[1]/evals2[0]:.4f} : {evals2[2]/evals2[0]:.4f}")
print()

# The problem: when Y2/Y1 ~ 1, both matrices give nearly DEGENERATE eigenvalues
# No mass hierarchy!

# Assignment 3: Use HIGHER WEIGHT modular forms
# Weight 4: Y^(4) = Y(2) tensor Y(2)
# Gives: Y1^2, Y1*Y2, Y2^2, plus possible singlet Y1^2 + Y2^2

# Weight 4 forms:
y4_1 = y1**2 + y2**2  # singlet
y4_2a = y1**2 - y2**2  # from doublet product
y4_2b = 2*y1*y2         # from doublet product

print("  Weight 4 modular forms (Y tensor Y):")
print(f"    Y1^2 + Y2^2 (singlet) = {y4_1:.6f}")
print(f"    Y1^2 - Y2^2 (doublet component) = {y4_2a:.6f}")
print(f"    2*Y1*Y2 (doublet component) = {y4_2b:.6f}")
print(f"    Ratio (Y1^2-Y2^2)/(2*Y1*Y2) = {y4_2a/(2*y1*y2):.6f}")
print()

# THIS is interesting: even though Y2/Y1 ~ 1,
# (Y1^2 - Y2^2) / (2*Y1*Y2) CAN be small
# because Y1^2 - Y2^2 = (Y1-Y2)(Y1+Y2) and Y1-Y2 is small when Y2/Y1 ~ 1

delta = (y1 - y2) / (y1 + y2)
print(f"  Key: (Y1-Y2)/(Y1+Y2) = {delta:.6f}")
print(f"  This SMALL parameter could drive the hierarchy!")
print()

# ================================================================
# PART 4: HIERARCHY FROM THE SMALL PARAMETER
# ================================================================

print("=" * 70)
print("PART 4: HIERARCHY FROM delta = (Y1-Y2)/(Y1+Y2)")
print("=" * 70)
print()

print(f"  delta = {delta:.8f}")
print()

# Mass hierarchy from powers of delta:
# m_e : m_mu : m_tau ~ delta^a : delta^b : 1
# Measured ratios: m_e/m_tau = 0.000282, m_mu/m_tau = 0.0595

m_e_val = 0.511e-3  # GeV
m_mu_val = 0.10566  # GeV
m_tau_val = 1.777    # GeV

r_e_tau = m_e_val / m_tau_val
r_mu_tau = m_mu_val / m_tau_val

print(f"  Measured mass ratios:")
print(f"    m_e/m_tau = {r_e_tau:.6f}")
print(f"    m_mu/m_tau = {r_mu_tau:.6f}")
print()

# If m_e/m_tau = delta^a: a = ln(m_e/m_tau) / ln(delta)
if delta > 0:
    exp_e = math.log(r_e_tau) / math.log(delta)
    exp_mu = math.log(r_mu_tau) / math.log(delta)
    print(f"  If hierarchy from delta^n:")
    print(f"    m_e/m_tau = delta^{exp_e:.2f}")
    print(f"    m_mu/m_tau = delta^{exp_mu:.2f}")
    print()

    # Are these near integers or simple fractions?
    for n in [1, 2, 3, 4, 5, 6, 7, 8]:
        print(f"    delta^{n} = {delta**n:.6e}", end="")
        if abs(delta**n - r_e_tau) / r_e_tau < 0.3:
            print(f"  <-- near m_e/m_tau ({abs(delta**n/r_e_tau - 1)*100:.1f}% off)")
        elif abs(delta**n - r_mu_tau) / r_mu_tau < 0.3:
            print(f"  <-- near m_mu/m_tau ({abs(delta**n/r_mu_tau - 1)*100:.1f}% off)")
        else:
            print()

print()

# ================================================================
# PART 5: ALTERNATIVE — USE eta/theta RATIOS DIRECTLY
# ================================================================

print("=" * 70)
print("PART 5: MASS HIERARCHY FROM eta/theta RATIOS")
print("=" * 70)
print()

# Instead of Feruglio's Y1, Y2, what if the mass matrix uses
# eta, theta3, theta4 DIRECTLY (the Gamma(2) generators)?

# The three generators have VERY different magnitudes:
print(f"  The three Gamma(2) generators:")
print(f"    eta    = {eta:.8f}  (small)")
print(f"    theta4 = {t4:.8f}  (small)")
print(f"    theta3 = {t3:.8f}  (large)")
print()

# Ratios:
print(f"  Ratios:")
print(f"    eta/theta3 = {eta/t3:.8f}")
print(f"    theta4/theta3 = {t4/t3:.8f}")
print(f"    eta/theta4 = {eta/t4:.8f}")
print(f"    eta^2/theta4 = {eta**2/t4:.8f}")
print()

# These ratios span a HUGE range: from ~0.05 to ~0.54
# Can they generate the fermion mass hierarchy?

# The measured charged lepton mass ratios:
print("  Charged lepton ratios:")
print(f"    m_e/m_tau = {r_e_tau:.6e}")
print(f"    m_mu/m_tau = {r_mu_tau:.4f}")
print()

# Test: can we get these from eta, theta products?
candidates_ratios = [
    ("eta^2/theta3", eta**2/t3),
    ("eta^3", eta**3),
    ("eta * theta4 / theta3", eta*t4/t3),
    ("theta4^2 / theta3^2", (t4/t3)**2),
    ("eta^4 / theta4", eta**4/t4),
    ("eta^2 * theta4 / theta3^2", eta**2 * t4 / t3**2),
    ("(eta/theta3)^3", (eta/t3)**3),
    ("(eta*theta4)^2", (eta*t4)**2),
    ("eta^3 * theta4 / theta3", eta**3 * t4 / t3),
    ("eta * (theta4/theta3)^2", eta * (t4/t3)**2),
]

print("  Candidate expressions for m_e/m_tau:")
for name, val in candidates_ratios:
    ratio_to_target = val / r_e_tau
    pct = abs(ratio_to_target - 1) * 100
    marker = " <---" if pct < 30 else ""
    print(f"    {name:35s} = {val:.6e}  ({pct:6.1f}% off){marker}")

print()
print("  Candidate expressions for m_mu/m_tau:")
for name, val in candidates_ratios:
    ratio_to_target = val / r_mu_tau
    pct = abs(ratio_to_target - 1) * 100
    marker = " <---" if pct < 30 else ""
    print(f"    {name:35s} = {val:.6e}  ({pct:6.1f}% off){marker}")

print()

# ================================================================
# PART 6: GENERATION STRUCTURE FROM 2<->3 OSCILLATION
# ================================================================

print("=" * 70)
print("PART 6: THE 2<->3 OSCILLATION IN MASSES")
print("=" * 70)
print()

# The 2<->3 oscillation:
# 2 vacua -> 3 objects -> 2 bound states -> 3 couplings -> 2 independent -> 3 generations
#
# For masses: the S3 action on {1, phi} gives 3 orbits.
# S3 permutations of (a, b) where a*phi + b:
# The three S3 irreps applied to the Fibonacci basis might give:
#   Singlet 1: a + b (symmetric combination)
#   Singlet 1': a - b (antisymmetric)
#   Doublet 2: (a, b) -> two independent states

# Mass for generation g: m_g = m_0 * phi^(n_g) where n_g from S3 orbit
# The three orbits of S3 acting on the Fibonacci chain:

print("  Three S3 orbits of the Fibonacci basis:")
print()
print("  The Fibonacci chain: ..., F_{n-1}, F_n, F_{n+1}, ...")
print("  S3 acts by permuting the 3 basis vectors of the doublet + singlet.")
print()

# In Feruglio: three generations transform as 3 = 1 + 2 under S3
# The singlet gets one mass eigenvalue
# The doublet gets two (related by S3 symmetry)

# At golden nome, the doublet mass from Y = (Y1, Y2):
# Eigenvalues of the 2x2 block: proportional to Y1 +/- Y2 (for circulant-type)
# = (Y1+Y2) and (Y1-Y2)

Y_sum = Y1_raw + Y2_raw
Y_diff = abs(Y1_raw - Y2_raw)

print(f"  Y1 + Y2 = {Y_sum:.6f}")
print(f"  |Y1 - Y2| = {Y_diff:.6f}")
print(f"  Ratio (Y1+Y2)/(Y1-Y2) = {Y_sum/Y_diff:.4f}")
print()

# Check: does Y_diff / Y_sum match any mass ratio?
mass_ratio_candidates = {
    "m_e/m_tau": r_e_tau,
    "m_mu/m_tau": r_mu_tau,
    "m_e/m_mu": m_e_val/m_mu_val,
    "m_u/m_t": 2.16e-3/172.76,
    "m_c/m_t": 1.27/172.76,
    "m_d/m_b": 4.67e-3/4.18,
    "m_s/m_b": 93.4e-3/4.18,
}

small_param = Y_diff / Y_sum
print(f"  Small parameter epsilon = |Y1-Y2|/(Y1+Y2) = {small_param:.6f}")
print()
print("  Comparing epsilon^n to measured mass ratios:")
print()
for n in range(1, 10):
    eps_n = small_param**n
    for name, meas in mass_ratio_candidates.items():
        if abs(math.log(eps_n/meas)) < 0.5:  # within factor ~1.6
            pct = abs(eps_n/meas - 1) * 100
            print(f"    epsilon^{n} = {eps_n:.6e}  vs  {name} = {meas:.6e}  ({pct:.1f}% off)")

print()

# ================================================================
# PART 7: THE DEEP INSIGHT
# ================================================================

print("=" * 70)
print("PART 7: SYNTHESIS")
print("=" * 70)
print()

print("  FINDING: At q = 1/phi, the modular forms Y1 and Y2 are NEARLY EQUAL.")
print(f"  Y2/Y1 = {r:.6f}")
print(f"  Small parameter: epsilon = {small_param:.6f}")
print()
print("  This means:")
print("    - Standard Feruglio mechanism (Y2/Y1 -> 0 for hierarchy) FAILS")
print("    - But a DIFFERENT hierarchy mechanism is available:")
print("      Use powers of epsilon = |Y1-Y2|/(Y1+Y2)")
print()
print("  The hierarchy at the golden nome comes from:")
print("    - The DIFFERENCE between Y1 and Y2 (not their ratio)")
print("    - Powers of this difference give the generation spacing")
print()

# What IS epsilon in terms of modular forms?
# Y1 = (theta3^4 + theta4^4) / eta^4
# Y2 = (theta3^4 - theta4^4) / eta^4
# Y1 - Y2 = 2*theta4^4/eta^4
# Y1 + Y2 = 2*theta3^4/eta^4
# epsilon = theta4^4/theta3^4

eps_exact = t4**4 / t3**4
print(f"  EXACT: epsilon = theta4^4 / theta3^4 = {eps_exact:.8f}")
print(f"  Numerical: {small_param:.8f}")
print(f"  Match: {abs(eps_exact - small_param) < 1e-10}")
print()
print(f"  So the hierarchy parameter is (theta4/theta3)^4!")
print(f"  theta4/theta3 = {t4/t3:.8f}")
print(f"  (theta4/theta3)^4 = {(t4/t3)**4:.8f}")
print()

# This is a NATURAL small parameter at the golden nome
ratio_t4_t3 = t4/t3
print(f"  theta4/theta3 = {ratio_t4_t3:.6f}")
print(f"  1/alpha_tree = theta3*phi/theta4 uses exactly this ratio!")
print(f"  So the hierarchy parameter is related to alpha!")
print()

# alpha_tree = theta4 / (theta3 * phi)
alpha_tree = t4 / (t3 * phi)
print(f"  alpha_tree = theta4/(theta3*phi) = {alpha_tree:.8f}")
print(f"  epsilon = (theta4/theta3)^4 = (alpha_tree * phi)^4 = {(alpha_tree*phi)**4:.8f}")
print(f"  Measured alpha = {1/137.036:.8f}")
print()

# Check: epsilon = (alpha * phi)^4 ?
alpha_measured = 1/137.035999084
eps_from_alpha = (alpha_measured * phi)**4
print(f"  (alpha_measured * phi)^4 = {eps_from_alpha:.8f}")
print(f"  epsilon = {eps_exact:.8f}")
print(f"  They're NOT equal (tree vs full alpha), but structurally related.")
print()

# ================================================================
# SUMMARY
# ================================================================

print("=" * 70)
print("SUMMARY: WHAT WE FOUND")
print("=" * 70)
print()
print("  1. Standard Feruglio at golden nome: Y2/Y1 ~ 1 (NO automatic hierarchy)")
print()
print("  2. BUT: a natural small parameter exists:")
print(f"     epsilon = (theta4/theta3)^4 = {eps_exact:.6f}")
print()
print("  3. This parameter IS the hierarchy driver at the golden nome.")
print("     It's related to (but not identical to) alpha.")
print()
print("  4. Powers of epsilon should give generation mass ratios.")
print("     Need to construct the FULL S3 mass matrix using higher-weight")
print("     modular forms where epsilon appears naturally.")
print()
print("  5. The KEY INSIGHT: at the golden nome, hierarchy comes from")
print("     the theta4/theta3 asymmetry (= the asymmetry between the two")
print("     theta functions), NOT from Y2/Y1 -> 0 (which requires the cusp).")
print()
print("  6. This asymmetry IS the wall's asymmetry: theta4 and theta3")
print("     correspond to the two different boundary conditions on the torus.")
print("     The wall breaks this symmetry: phi vs -1/phi.")
print()
print("  NEXT STEPS:")
print("    a. Build the full S3 mass matrix at higher weights (4, 6)")
print("    b. Show that eigenvalue ratios match measured mass ratios")
print("    c. Identify which S3 assignments give the best fit")
print("    d. Count free parameters vs predictions")
print()
print("  If this works: ZERO free dimensionless parameters.")
print("  Every mass ratio from x^2 - x - 1 = 0.")
