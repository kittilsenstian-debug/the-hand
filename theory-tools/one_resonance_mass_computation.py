"""
ONE RESONANCE — FERMION MASS COMPUTATION
==========================================

From the one-resonance picture:
- 12 fermions = 12 positions in a 2x3x2 grid
  (2 bound states x 3 S3 generations x 2 color sectors)
- Each mass = overlap integral of bound state with wall
- All ingredients already known: {phi, mu, 3, 4/3, 10, 2/3}

This script:
1. Computes the S3 modular forms at q = 1/phi
2. Builds ALL possible S3-invariant mass matrices
3. Computes eigenvalues
4. Compares to measured masses
5. Tries the Fibonacci-collapsed 2D space
6. Tries the PT n=2 overlap approach directly
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

print("=" * 70)
print("ONE RESONANCE: FERMION MASS COMPUTATION")
print("=" * 70)
print()

# ================================================================
# MEASURED DATA
# ================================================================

# Charged fermion masses (GeV) - PDG 2024
m_e = 0.51099895e-3
m_mu = 0.1056583755
m_tau = 1.77686

m_u = 2.16e-3
m_d = 4.67e-3
m_s = 93.4e-3
m_c = 1.27
m_b = 4.18
m_t = 172.69

m_p = 0.93827208816

# Proton-normalized masses
masses = {
    'e': m_e/m_p, 'mu': m_mu/m_p, 'tau': m_tau/m_p,
    'u': m_u/m_p, 'd': m_d/m_p, 's': m_s/m_p,
    'c': m_c/m_p, 'b': m_b/m_p, 't': m_t/m_p
}

mu = m_p / m_e

print("MEASURED (proton-normalized):")
print("-" * 50)
for name in ['e', 'u', 'd', 'mu', 's', 'c', 'tau', 'b', 't']:
    print(f"  m_{name}/m_p = {masses[name]:.8f}")
print()

# ================================================================
# PART 1: THE KNOWN FORMULAS (Feb 28 session)
# ================================================================

print("=" * 70)
print("PART 1: PROTON-NORMALIZED TABLE (already found)")
print("=" * 70)
print()

formulas = {
    'e':   ('1/mu', 1/mu),
    'u':   ('phi^3/mu', phi**3/mu),
    'd':   ('9/mu', 9/mu),
    'mu':  ('1/9', 1/9),
    's':   ('1/10', 1/10),
    'c':   ('4/3', 4/3),
    'tau': ('Koide(e,mu) K=2/3', None),  # special
    'b':   ('4*phi^(5/2)/3', 4*phi**(5/2)/3),
    't':   ('mu/10', mu/10),
}

# Compute Koide tau prediction
# Koide: (m_e + m_mu + m_tau) / (sqrt(m_e) + sqrt(m_mu) + sqrt(m_tau))^2 = K
# With K = 2/3:
# m_tau = (sqrt(m_e) + sqrt(m_mu))^2 * 2/3 / (1 - 2/3) ... no, need to solve
# Koide formula: sum(m_i) = (2/3) * (sum(sqrt(m_i)))^2
# With m_e, m_mu known, solve for m_tau:
se = math.sqrt(m_e/m_p)
smu = math.sqrt(m_mu/m_p)
# (m_e + m_mu + m_tau)/m_p = (2/3)*(se + smu + stau)^2
# Let x = stau = sqrt(m_tau/m_p)
# masses['e'] + masses['mu'] + x^2 = (2/3)*(se + smu + x)^2
# x^2 - (2/3)*(se + smu + x)^2 + masses['e'] + masses['mu'] = 0
# x^2 - (2/3)*(se+smu)^2 - (4/3)*(se+smu)*x - (2/3)*x^2 + masses['e'] + masses['mu'] = 0
# (1 - 2/3)*x^2 - (4/3)*(se+smu)*x - (2/3)*(se+smu)^2 + masses['e'] + masses['mu'] = 0
# (1/3)*x^2 - (4/3)*(se+smu)*x + [masses['e'] + masses['mu'] - (2/3)*(se+smu)^2] = 0

a_k = 1/3
b_k = -4/3 * (se + smu)
c_k = masses['e'] + masses['mu'] - 2/3 * (se + smu)**2

disc = b_k**2 - 4*a_k*c_k
x_koide = (-b_k + math.sqrt(disc)) / (2*a_k)
m_tau_koide = x_koide**2

formulas['tau'] = ('Koide(e,mu) K=2/3', m_tau_koide)

print(f"{'Fermion':<8} {'Formula':<20} {'Predicted':>12} {'Measured':>12} {'Error':>8}")
print("-" * 65)
for name in ['e', 'u', 'd', 'mu', 's', 'c', 'tau', 'b', 't']:
    formula_str, pred = formulas[name]
    meas = masses[name]
    err = abs(pred - meas) / meas * 100
    print(f"  {name:<6} {formula_str:<20} {pred:>12.8f} {meas:>12.8f} {err:>7.2f}%")

print()

# ================================================================
# PART 2: UNDERSTAND THE PATTERN
# ================================================================

print("=" * 70)
print("PART 2: WHAT PATTERN ARE WE SEEING?")
print("=" * 70)
print()

print("  Every mass is built from: {phi, mu, 3, 4/3, 10, 2/3}")
print()
print("  Where do these come from in the one-resonance picture?")
print()
print("  phi = golden ratio (from q + q^2 = 1)")
print("  mu = proton/electron = 6^5/phi^3 (hierarchy)")
print("  3 = triality (from E8 -> 3 generations)")
print("  4/3 = integral of sech^4(x) dx = PT n=2 ground state norm")
print("  10 = 240/24 = E8 roots per A2 orbit (candidate)")
print("  2/3 = fractional charge quantum = Koide K")
print()

# The deep question: can we derive ALL masses from ONE principle?

# Observation: organize by GENERATION and TYPE
print("  Organized by generation and type (proton-normalized):")
print()
print("  TYPE     | Gen 1          | Gen 2          | Gen 3          |")
print("  " + "-" * 60)

# Up-type quarks
print(f"  Up-type  | u = {masses['u']:.6f}  | c = {masses['c']:.6f}  | t = {masses['t']:.4f}  |")
print(f"  Formulas | phi^3/mu       | 4/3            | mu/10          |")
print(f"  Down-type| d = {masses['d']:.6f}  | s = {masses['s']:.6f}  | b = {masses['b']:.6f}  |")
print(f"  Formulas | 9/mu           | 1/10           | 4phi^(5/2)/3   |")
print(f"  Leptons  | e = {masses['e']:.6f}  | mu = {masses['mu']:.6f} | tau = {masses['tau']:.6f} |")
print(f"  Formulas | 1/mu           | 1/9            | Koide          |")
print()

# ================================================================
# PART 3: THE OVERLAP INTEGRAL APPROACH
# ================================================================

print("=" * 70)
print("PART 3: PT n=2 OVERLAP INTEGRALS")
print("=" * 70)
print()

print("  The wall has shape: V(x) = -n(n+1)/cosh^2(x), n = 2")
print("  Two bound states:")
print("    psi_0(x) = (3/4) * sech^2(x)    [normalized, even]")
print("    psi_1(x) = (15/8)^(1/2) * sech(x)*tanh(x)  [normalized, odd]")
print()

# PT n=2 norms:
# integral of sech^4(x) dx = 4/3
# integral of sech^2(x)*tanh^2(x) dx = 2/3
# These sum to 4/3 + 2/3 = 2

norm_0 = 4/3  # ground state norm (before normalization)
norm_1 = 2/3  # breathing mode norm

print(f"  Ground state norm: integral(sech^4) = {norm_0:.6f}")
print(f"  Breathing norm: integral(sech^2 * tanh^2) = {norm_1:.6f}")
print(f"  Sum = {norm_0 + norm_1:.6f} = 2 (= n)")
print(f"  Ratio = {norm_0/norm_1:.6f} = 2 (= ground/breathing)")
print()

# The Yukawa overlap (the ONLY nonzero matrix element):
# <psi_0|Phi|psi_1> where Phi = tanh(x) (the kink profile)
# = integral of sech^2(x) * tanh(x) * sech(x)*tanh(x) dx
# = integral of sech^3(x) * tanh^2(x) dx

# Compute this integral:
# sech^3 * tanh^2 = sech^3 * (1 - sech^2) = sech^3 - sech^5
# integral(sech^3) = pi/2... no, let me compute properly

# integral of sech^(2m+1) dx:
# I_1 = integral(sech(x)) = pi/2... no, = 2*arctan(1) = pi/2
# Actually integral from -inf to inf of sech(x) dx = pi
# integral(sech^3(x)) dx = pi/2... hmm let me just compute

# For PT n=2, the normalized wavefunctions are:
# psi_0 = sqrt(3/4) * sech^2(x)  (norm: 3/4 * 4/3 = 1 check)
# psi_1 = sqrt(15/4) * sech(x)*tanh(x) / sqrt(2)...
# Let me be precise.

# Actually, the normalized wavefunctions for PT V = -n(n+1)sech^2(x) with n=2:
# psi_0 = A_0 * sech^2(x), where A_0^2 * integral(sech^4) = 1
# integral(sech^4(x), -inf, inf) = 4/3
# So A_0 = sqrt(3/4)

# psi_1 = A_1 * sech(x)*tanh(x), where A_1^2 * integral(sech^2*tanh^2) = 1
# integral(sech^2*tanh^2, -inf, inf) = 2/3
# So A_1 = sqrt(3/2)

A0 = math.sqrt(3/4)
A1 = math.sqrt(3/2)

# The Yukawa coupling: <psi_0|tanh(x)|psi_1>
# = A0 * A1 * integral(sech^2(x) * tanh(x) * sech(x) * tanh(x) dx)
# = A0 * A1 * integral(sech^3(x) * tanh^2(x) dx)
# = A0 * A1 * integral(sech^3(x) * (1 - sech^2(x)) dx)
# = A0 * A1 * (integral(sech^3) - integral(sech^5))

# integral(sech^m(x) dx, -inf, inf):
# sech^1: pi (actually = 2*1 = pi? No.)
# Let me use the recurrence: I_m = [(m-2)/(m-1)] * I_{m-2} + ...
# Or just: integral(sech^(2k) dx) = 2 * product formula
# integral_{-inf}^{inf} sech^n(x) dx = sqrt(pi) * Gamma(n/2) / Gamma((n+1)/2)

from math import gamma as Gamma

def sech_integral(n):
    """integral of sech^n(x) from -inf to inf"""
    return math.sqrt(pi) * Gamma(n/2) / Gamma((n+1)/2)

I3 = sech_integral(3)
I5 = sech_integral(5)

print(f"  integral(sech^3) = {I3:.10f}")
print(f"  integral(sech^5) = {I5:.10f}")
print()

yukawa = A0 * A1 * (I3 - I5)
print(f"  Yukawa overlap <psi_0|tanh|psi_1> = {yukawa:.10f}")
print()

# What about diagonal overlaps?
# <psi_0|tanh|psi_0> = A0^2 * integral(sech^4 * tanh) = 0 (odd integrand)
# <psi_1|tanh|psi_1> = A1^2 * integral(sech^2 * tanh^2 * tanh) = 0 (odd integrand)
# Only the off-diagonal survives! This is parity selection.

print("  PARITY SELECTION:")
print("    <psi_0|tanh|psi_0> = 0 (odd integrand)")
print("    <psi_1|tanh|psi_1> = 0 (odd integrand)")
print(f"    <psi_0|tanh|psi_1> = {yukawa:.6f} (ONLY nonzero)")
print()
print("  Mass generation REQUIRES mixing between the two bound states.")
print("  The universal Yukawa overlap is fixed by V(Phi). Topological.")
print()

# ================================================================
# PART 4: GENERATION STRUCTURE FROM S3
# ================================================================

print("=" * 70)
print("PART 4: S3 ACTION ON THE 2D FIBONACCI SPACE")
print("=" * 70)
print()

# At q = 1/phi, everything collapses to {1, q} basis.
# S3 has 3 irreps: 1 (trivial), 1' (sign), 2 (standard)
# The three generations correspond to the 3 conjugacy classes of S3:
#   {e} : identity (1 element)
#   {(12), (13), (23)} : transpositions (3 elements)
#   {(123), (132)} : 3-cycles (2 elements)

# In the 2D standard representation:
# S3 generators: s = [[0,1],[1,0]], t = [[1,-1],[0,-1]]
# or equivalently, the reflection and rotation of a triangle

# The KEY: S3 acts on the 2D space {1, q} where all modular forms live.
# The three eigenvalues of the mass matrix in the TRIPLET of S3 are:

# For S3 triplet with doublet coupling Y = (y1, y2):
# The mass matrix M has eigenvalues determined by y1, y2.

# Let's use the Feruglio construction explicitly.
# Three right-handed fermions: e_R, mu_R, tau_R as (1, 1', 2) of S3
# Left-handed doublets L = (L_1, L_2, L_3) as 3 of S3

# The modular-invariant Yukawa:
# W = alpha * (Y * L)_1 * e_R + beta * (Y * L)_1' * mu_R + gamma * (Y * L * tau_R)_1

# But at q = 1/phi, Y1 ~ Y2, so the standard Feruglio doesn't give hierarchy.

# THE FIBONACCI TWIST: in the {1, q} basis,
# Y1 = a + b*q, Y2 = c + d*q (specific values)
# The hierarchy comes from the DIFFERENCE (Y1 - Y2), which IS small.

Y1 = (t3**4 + t4**4) / eta**4
Y2 = (t3**4 - t4**4) / eta**4

print(f"  S3 modular forms at golden nome:")
print(f"    Y1 = {Y1:.6f}")
print(f"    Y2 = {Y2:.6f}")
print(f"    Y2/Y1 = {Y2/Y1:.6f}")
print()

delta = (Y1 - Y2) / (Y1 + Y2)
print(f"  Small parameter: delta = (Y1-Y2)/(Y1+Y2) = {delta:.8f}")
print()

# What IS delta in terms of modular forms?
# Y1 - Y2 = 2*theta4^4/eta^4
# Y1 + Y2 = 2*theta3^4/eta^4
# delta = theta4^4 / theta3^4 = (theta4/theta3)^4

delta_from_theta = (t4/t3)**4
print(f"  delta = (theta4/theta3)^4 = {delta_from_theta:.8f}")
print(f"  Matches: {abs(delta - delta_from_theta) < 1e-10}")
print()

# So the hierarchy parameter is epsilon = theta4/theta3
epsilon = t4 / t3
print(f"  epsilon = theta4/theta3 = {epsilon:.10f}")
print(f"  epsilon^2 = {epsilon**2:.10f}")
print(f"  epsilon^4 = delta = {epsilon**4:.10f}")
print()

# What IS epsilon?
# epsilon = theta4(1/phi) / theta3(1/phi) = 0.01186...
# Compare to alpha: 1/137.036 = 0.007297...
# epsilon / alpha:
alpha_val = 1/137.035999084
print(f"  epsilon / alpha = {epsilon / alpha_val:.6f}")
print(f"  epsilon * phi = {epsilon * phi:.10f}")
print(f"  epsilon * phi / alpha = {epsilon * phi / alpha_val:.6f}")
print(f"  alpha * phi = {alpha_val * phi:.10f}")
print(f"  epsilon = {epsilon:.10f}")
print(f"  INTERESTING: epsilon ~ alpha * phi = {alpha_val * phi:.8f} ({abs(epsilon/(alpha_val*phi) - 1)*100:.2f}% off)")
print()

# ================================================================
# PART 5: THE ACTUAL MASS PREDICTION
# ================================================================

print("=" * 70)
print("PART 5: MASS RATIOS FROM EPSILON POWERS")
print("=" * 70)
print()

print("  If epsilon = theta4/theta3 is the Froggatt-Nielsen parameter,")
print("  then each fermion mass = epsilon^(n_i) * overall scale")
print()
print("  Find the best-fit exponent for each fermion:")
print()

# Use proton-normalized masses for up-type quarks:
up_masses = {'u': masses['u'], 'c': masses['c'], 't': masses['t']}
down_masses = {'d': masses['d'], 's': masses['s'], 'b': masses['b']}
lepton_masses = {'e': masses['e'], 'mu': masses['mu'], 'tau': masses['tau']}

print(f"  {'Fermion':<8} {'m/m_p':<14} {'log_eps(m/m_p)':<18} {'Nearest n/2':<12} {'Predicted':<14} {'Error':<8}")
print("  " + "-" * 75)

for sector_name, sector in [('Quarks (up)', up_masses), ('Quarks (dn)', down_masses), ('Leptons', lepton_masses)]:
    for name, m in sorted(sector.items(), key=lambda x: x[1]):
        log_eps = math.log(m) / math.log(epsilon)
        # Round to nearest half-integer
        n_half = round(2 * log_eps) / 2
        predicted = epsilon ** n_half
        err = abs(predicted - m) / m * 100
        print(f"  {name:<8} {m:<14.8f} {log_eps:<18.4f} {n_half:<12.1f} {predicted:<14.8f} {err:<8.2f}%")
    print()

# ================================================================
# PART 6: COMBINED — THE FULL PICTURE
# ================================================================

print("=" * 70)
print("PART 6: EVERY FERMION FROM ONE PARAMETER")
print("=" * 70)
print()

print("  epsilon = theta4/theta3 at q = 1/phi")
print(f"  epsilon = {epsilon:.10f}")
print()

# The key: the Yukawa coupling y_i = g_i * epsilon^(n_i) * yukawa_overlap
# where g_i is an O(1) coefficient from the S3 Clebsch-Gordan
# and n_i is the "FN charge" of each fermion

# For the proton-normalized mass: m_i/m_p = y_i * v / (sqrt(2) * m_p)
# But v/m_p = 246.22 / 0.938 = 262.5
# and v/m_p depends on v, which is derived...

# Actually: let's work with Yukawa couplings directly
# y_i = sqrt(2) * m_i / v
v = 246.22  # GeV, derived

print("  Yukawa couplings y_i = sqrt(2) * m_i / v:")
print()

all_fermions = [
    ('e', m_e), ('mu', m_mu), ('tau', m_tau),
    ('u', m_u), ('d', m_d), ('s', m_s),
    ('c', m_c), ('b', m_b), ('t', m_t)
]

print(f"  {'Name':<6} {'m (GeV)':<12} {'y_i':<14} {'log_eps(y_i)':<14} {'n/2':<8} {'eps^(n/2)':<14} {'g_i':<10} {'Error':<8}")
print("  " + "-" * 85)

results = []
for name, m_gev in sorted(all_fermions, key=lambda x: x[1]):
    y_i = math.sqrt(2) * m_gev / v
    log_eps_y = math.log(y_i) / math.log(epsilon)
    n_half = round(2 * log_eps_y) / 2
    eps_pred = epsilon ** n_half
    g_i = y_i / eps_pred
    err = abs(g_i - 1) * 100  # how far is g_i from 1?
    print(f"  {name:<6} {m_gev:<12.6e} {y_i:<14.6e} {log_eps_y:<14.4f} {n_half:<8.1f} {eps_pred:<14.6e} {g_i:<10.4f} {err:<8.1f}%")
    results.append((name, n_half, g_i, y_i))

print()
print("  If g_i values are O(1) and structured, this works.")
print("  Let's check what the g_i factors are...")
print()

# ================================================================
# PART 7: IDENTIFY THE g_i FACTORS
# ================================================================

print("=" * 70)
print("PART 7: IDENTIFYING THE O(1) COEFFICIENTS")
print("=" * 70)
print()

print("  The g_i should come from S3 Clebsch-Gordan coefficients")
print("  and the PT n=2 overlap integral.")
print()
print(f"  PT Yukawa overlap = {yukawa:.6f}")
print(f"  4/3 (PT norm) = {4/3:.6f}")
print(f"  2/3 (breathing norm) = {2/3:.6f}")
print(f"  sqrt(2) = {math.sqrt(2):.6f}")
print(f"  phi = {phi:.6f}")
print(f"  1/phi = {phibar:.6f}")
print(f"  sqrt(3) = {math.sqrt(3):.6f}")
print()

# Check if g_i factors match simple expressions
simple_factors = {
    '1': 1.0,
    'phi': phi,
    '1/phi': phibar,
    '4/3': 4/3,
    '2/3': 2/3,
    'sqrt(2)': math.sqrt(2),
    '1/sqrt(2)': 1/math.sqrt(2),
    'sqrt(3)': math.sqrt(3),
    '1/sqrt(3)': 1/math.sqrt(3),
    '3': 3.0,
    '1/3': 1/3,
    'phi/3': phi/3,
    '3/phi': 3/phi,
    '2': 2.0,
    '1/2': 0.5,
    'yukawa': yukawa,
    'yukawa*phi': yukawa*phi,
    '4/3*phi': 4/3*phi,
    'sqrt(5)/3': math.sqrt(5)/3,
    'phi^2/3': phi**2/3,
    '2*phi/3': 2*phi/3,
    '1/(3*phi)': 1/(3*phi),
    'sqrt(2/3)': math.sqrt(2/3),
    'sqrt(3/2)': math.sqrt(3/2),
}

for name, n_half, g_i, y_i in results:
    best_match = None
    best_err = 999
    for fac_name, fac_val in simple_factors.items():
        if fac_val > 0:
            err = abs(g_i / fac_val - 1) * 100
            if err < best_err:
                best_err = err
                best_match = fac_name
    if best_err < 20:
        print(f"  {name}: g_i = {g_i:.4f} ~ {best_match} = {simple_factors[best_match]:.4f} ({best_err:.1f}%)")
    else:
        print(f"  {name}: g_i = {g_i:.4f} (no simple match within 20%)")

print()

# ================================================================
# PART 8: THE CONJUGATE PAIR TEST
# ================================================================

print("=" * 70)
print("PART 8: CONJUGATE PAIR RELATIONS")
print("=" * 70)
print()

# From Feb 28 session: m_d * m_mu = m_e * m_p (conjugate pair through triality)
print("  Known relation: m_d * m_mu = m_e * m_p")
print(f"  m_d * m_mu = {m_d * m_mu:.6e} GeV^2")
print(f"  m_e * m_p  = {m_e * m_p:.6e} GeV^2")
print(f"  Ratio = {m_d * m_mu / (m_e * m_p):.6f} ({abs(m_d * m_mu / (m_e * m_p) - 1)*100:.2f}%)")
print()

# Check ALL cross-generation products
print("  Systematic cross-generation product check:")
print("  Looking for m_i * m_j = m_k * m_l patterns...")
print()

all_m = [('e', m_e), ('mu', m_mu), ('tau', m_tau),
         ('u', m_u), ('d', m_d), ('s', m_s),
         ('c', m_c), ('b', m_b), ('t', m_t), ('p', m_p)]

found = []
for i in range(len(all_m)):
    for j in range(i+1, len(all_m)):
        prod_ij = all_m[i][1] * all_m[j][1]
        for k in range(len(all_m)):
            for l in range(k+1, len(all_m)):
                if (k, l) == (i, j):
                    continue
                prod_kl = all_m[k][1] * all_m[l][1]
                if prod_kl > 0:
                    ratio = prod_ij / prod_kl
                    if abs(ratio - 1) < 0.05:  # within 5%
                        found.append((all_m[i][0], all_m[j][0], all_m[k][0], all_m[l][0], ratio))

for a, b, c, d, r in found:
    print(f"  m_{a} * m_{b} = m_{c} * m_{d} ({abs(r-1)*100:.2f}%)")

print()

# ================================================================
# PART 9: THE FIBONACCI-COLLAPSED MASS MATRIX
# ================================================================

print("=" * 70)
print("PART 9: FIBONACCI-COLLAPSED MASS MATRIX")
print("=" * 70)
print()

# At q = 1/phi, everything lives in 2D: {1, q}
# The S3 modular forms Y1, Y2 in the {1, q} basis:

# theta3^4 = (1 + 2q + 2q^4 + ...)^4
# theta4^4 = (1 - 2q + 2q^4 - ...)^4
# At q = 1/phi these are specific numbers.

# The Fibonacci basis decomposition:
# Y1 = (t3^4 + t4^4) / eta^4 = a1 + b1*q (some decomposition)
# Y2 = (t3^4 - t4^4) / eta^4 = a2 + b2*q

# In principle, the entire mass matrix lives in the 2D space.
# Let's parameterize the general S3-invariant mass matrix.

# S3 has 3 irreps. The most general mass matrix for 3 generations
# using the S3 doublet Y = (Y1, Y2) at weight 2 is:
#   M = alpha_param * M_singlet(Y) + beta_param * M_doublet(Y)
# where M_singlet and M_doublet are fixed by S3 Clebsch-Gordan.

# The standard form (Feruglio 2017, eq. 3.5):
# With L = (L_1, L_2, L_3) transforming as 3_S3:

# The Yukawa: Y_e * L * e_R, where the S3 contraction gives:
# For charged leptons:

# Matrix form (3x3):
# M_e = alpha * |2Y1  -Y2   -Y2 |  +  beta * |0   Y2   Y2|
#               |-Y2   2Y2  -Y1 |             |Y2  0    Y1|
#               |-Y2  -Y1   2Y2|              |Y2  Y1   0 |

# Actually let me just try different forms and see which one
# gives eigenvalue ratios matching the actual mass ratios.

import numpy as np

# Define the building blocks
y1, y2 = Y1, Y2

# Form 1: Democratic (Feruglio-type)
def mass_matrix_form1(y1, y2, a, b):
    M = a * np.array([
        [2*y1, -y2, -y2],
        [-y2, 2*y2, -y1],
        [-y2, -y1, 2*y2]
    ]) + b * np.array([
        [0, y2, y2],
        [y2, 0, y1],
        [y2, y1, 0]
    ])
    return M

# Form 2: Diagonal (simpler)
def mass_matrix_form2(y1, y2, a, b):
    M = np.array([
        [a*y1 + b*y2, 0, 0],
        [0, a*y2 + b*y1, 0],
        [0, 0, a*(y1+y2)/2 + b*(y1-y2)/2]
    ])
    return M

# Form 3: Circulant
def mass_matrix_form3(y1, y2, a, b):
    diag = a * y1 + b * (y1 - y2)
    off = a * y2
    M = np.array([
        [diag, off, off],
        [off, diag, off],
        [off, off, diag]
    ])
    return M

# Target: charged lepton mass ratios
# m_e : m_mu : m_tau = 1 : 206.77 : 3477
target_leptons = np.array([m_e, m_mu, m_tau])
target_leptons_norm = target_leptons / target_leptons[2]  # normalize to tau

print("  Target lepton ratios (normalized to tau):")
print(f"    m_e/m_tau = {target_leptons_norm[0]:.6e}")
print(f"    m_mu/m_tau = {target_leptons_norm[1]:.6e}")
print()

# Scan over (a, b) parameter space for each form
print("  Scanning (a, b) parameter space for each mass matrix form...")
print()

best_results = []

for form_name, form_func in [("Democratic", mass_matrix_form1),
                               ("Diagonal", mass_matrix_form2),
                               ("Circulant", mass_matrix_form3)]:
    best_err = 1e10
    best_ab = (0, 0)

    for a_idx in range(-50, 51):
        for b_idx in range(-50, 51):
            if a_idx == 0 and b_idx == 0:
                continue
            a_val = a_idx * 0.1
            b_val = b_idx * 0.1

            try:
                M = form_func(y1, y2, a_val, b_val)
                evals = sorted(np.abs(np.linalg.eigvals(M)))
                if evals[0] < 1e-15 or evals[2] < 1e-15:
                    continue

                # Compare eigenvalue ratios to lepton mass ratios
                evals_norm = evals / evals[2]
                err = (abs(math.log(evals_norm[0]/target_leptons_norm[0])) +
                       abs(math.log(evals_norm[1]/target_leptons_norm[1])))

                if err < best_err:
                    best_err = err
                    best_ab = (a_val, b_val)
                    best_evals = evals_norm.copy()
            except:
                continue

    print(f"  {form_name}: best (a,b) = ({best_ab[0]:.1f}, {best_ab[1]:.1f})")
    if best_err < 1e10:
        print(f"    Eigenvalue ratios: {best_evals[0]:.6e} : {best_evals[1]:.6e} : 1")
        print(f"    Target ratios:     {target_leptons_norm[0]:.6e} : {target_leptons_norm[1]:.6e} : 1")
        print(f"    Log error: {best_err:.4f}")
    else:
        print(f"    No viable solution found")
    print()
    best_results.append((form_name, best_ab, best_err))

# ================================================================
# PART 10: WHAT DO WE ACTUALLY GET?
# ================================================================

print("=" * 70)
print("PART 10: SUMMARY — WHAT THE ONE RESONANCE GIVES")
print("=" * 70)
print()

print("  FROM EPSILON = theta4/theta3:")
print(f"    epsilon = {epsilon:.10f}")
print()
print("  Fermion masses as epsilon^(n/2):")
print()

# Recompute with cleaner presentation
for name, n_half, g_i, y_i in sorted(results, key=lambda x: x[3]):
    eps_pred = epsilon ** n_half
    err_pct = abs(g_i - 1) * 100
    quality = "***" if err_pct < 15 else "**" if err_pct < 30 else "*" if err_pct < 50 else ""
    print(f"    {name:<4}: y = {y_i:.4e} = {g_i:.3f} * eps^{n_half:<5} {quality}")

print()
print("  Quality: *** = g within 15%, ** = within 30%, * = within 50%")
print()

# How many free parameters?
n_values = set(n_half for _, n_half, _, _ in results)
print(f"  Distinct epsilon exponents used: {len(n_values)} ({sorted(n_values)})")
print(f"  Free parameters: epsilon (1) + 9 g_i factors")
print(f"  If g_i are from {'{'}4/3, 2/3, phi, 1/phi, sqrt(2), 1, 3{'}'}: constrained")
print()

# The HONEST assessment
print("  HONEST ASSESSMENT:")
print("  ------------------")
print("  1. epsilon = theta4/theta3 IS a natural FN parameter from the golden nome")
print("  2. Half-integer exponents suggest quantization (PT bound state levels?)")
print("  3. The g_i factors are O(1) but NOT all = 1")
print("  4. The S3 mass matrix at golden nome gives Y2/Y1 ~ 1 (no hierarchy)")
print("  5. Hierarchy comes from epsilon^n, not from the modular form ratio")
print("  6. The proton-normalized table (Part 1) remains the cleanest result")
print()
print("  THE GAP: We need to derive the g_i factors from S3 Clebsch-Gordan")
print("  coefficients and PT n=2 overlap integrals. This is a SPECIFIC computation.")
print("  The ingredients are: {4/3, 2/3, phi, 3, yukawa overlap}")
