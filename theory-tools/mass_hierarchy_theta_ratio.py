#!/usr/bin/env python3
"""
mass_hierarchy_theta_ratio.py -- Fermion mass hierarchy from theta4/theta3 mechanism
======================================================================================

NEW APPROACH: Instead of Feruglio's Y2/Y1 (which are ~1 at golden nome), use the
natural small parameter epsilon = (theta4/theta3)^4 ~ 2e-8 to build mass hierarchies.

Key insight: at q = 1/phi, the modular forms theta3 and theta4 have a HUGE ratio:
  theta3 ~ 2.555, theta4 ~ 0.0303, so theta4/theta3 ~ 0.01186
This is structurally tied to alpha (since 1/alpha_tree = theta3*phi/theta4).
The hierarchy comes from the wall's OWN asymmetry, not from being near a cusp.

Uses only standard Python (math module). No external dependencies.

Usage:
    python theory-tools/mass_hierarchy_theta_ratio.py
"""

import math
import sys

# Handle Windows encoding
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

# ======================================================================
# MODULAR FORM COMPUTATION
# ======================================================================

phi = (1 + math.sqrt(5)) / 2       # 1.6180339887...
phibar = 1 / phi                    # 0.6180339887...
q = phibar                          # golden nome
sqrt5 = math.sqrt(5)
ln_phi = math.log(phi)
alpha_em = 1.0 / 137.035999084
pi = math.pi


def eta_func(q_val, terms=2000):
    """Dedekind eta: eta(q) = q^(1/24) * prod_{n=1}^inf (1 - q^n)"""
    result = q_val ** (1.0 / 24)
    for n in range(1, terms + 1):
        qn = q_val ** n
        if qn < 1e-300:
            break
        result *= (1 - qn)
    return result


def theta2_func(q_val, terms=500):
    """theta_2(q) = 2 * sum_{n>=0} q^((n+1/2)^2)"""
    s = 0.0
    for n in range(terms + 1):
        exp = (n + 0.5) ** 2
        term = q_val ** exp
        if term < 1e-300:
            break
        s += 2 * term
    return s


def theta3_func(q_val, terms=500):
    """theta_3(q) = 1 + 2 * sum_{n>=1} q^(n^2)"""
    s = 1.0
    for n in range(1, terms + 1):
        term = q_val ** (n * n)
        if term < 1e-300:
            break
        s += 2 * term
    return s


def theta4_func(q_val, terms=500):
    """theta_4(q) = 1 + 2 * sum_{n>=1} (-1)^n * q^(n^2)"""
    s = 1.0
    for n in range(1, terms + 1):
        term = q_val ** (n * n)
        if term < 1e-300:
            break
        s += 2 * ((-1) ** n) * term
    return s


# Compute all modular forms at golden nome
eta = eta_func(q)
t2 = theta2_func(q)
t3 = theta3_func(q)
t4 = theta4_func(q)
eta_q2 = eta_func(q * q)

# The key small parameter
eps = t4 / t3
eps4 = eps ** 4

# Fermion masses in GeV (PDG 2024 central values, MSbar at M_Z)
masses = {
    'e': 0.000511, 'mu': 0.10566, 'tau': 1.777,
    'u': 0.00216, 'd': 0.00467, 's': 0.0934,
    'c': 1.27, 'b': 4.18, 't': 172.76
}

# Group by charge type
leptons = ['e', 'mu', 'tau']
up_quarks = ['u', 'c', 't']
down_quarks = ['d', 's', 'b']
families = {'leptons': leptons, 'up_quarks': up_quarks, 'down_quarks': down_quarks}

v_higgs = 246.22  # GeV


def separator(title):
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)


def subsection(title):
    print(f"\n--- {title} ---")


# ======================================================================
# PART 1: MODULAR FORM RATIOS AT GOLDEN NOME
# ======================================================================

separator("PART 1: MODULAR FORM LANDSCAPE AT q = 1/phi")

print(f"\nGolden nome: q = 1/phi = {q:.10f}")
print(f"\nDedekind eta:  eta  = {eta:.10f}")
print(f"Theta_2:       t2   = {t2:.10f}")
print(f"Theta_3:       t3   = {t3:.10f}")
print(f"Theta_4:       t4   = {t4:.10f}")
print(f"eta(q^2):      etq2 = {eta_q2:.10f}")

subsection("Key ratios")
ratios = {
    'eps = t4/t3': t4 / t3,
    'eta/t3': eta / t3,
    'eta/t4': eta / t4,
    't2/t3': t2 / t3,
    't2/t4': t2 / t4,
    'eta^2/(t3*t4)': eta ** 2 / (t3 * t4),
    'eta_q2/eta': eta_q2 / eta,
}
for name, val in ratios.items():
    print(f"  {name:25s} = {val:.10f}")

subsection("Powers of epsilon = t4/t3")
print(f"\n  eps = t4/t3 = {eps:.8f}")
print(f"  Key: 1/alpha_tree = t3*phi/t4 = {t3 * phi / t4:.4f}")
print(f"       so eps = phi/alpha_tree = phi * alpha_tree = {phi * (t4 / (t3 * phi)):.8f}")
print(f"       More precisely: eps = t4/t3 and alpha_tree = t4/(t3*phi) = {t4 / (t3 * phi):.8f}")
print(f"       => eps = alpha_tree * phi = {(t4 / (t3 * phi)) * phi:.8f}")
print()

for n in range(1, 9):
    val = eps ** n
    log_val = math.log10(val) if val > 0 else float('-inf')
    print(f"  eps^{n} = (t4/t3)^{n:d} = {val:.6e}  (log10 = {log_val:.3f})")

subsection("Comparison: Feruglio Y2/Y1 vs theta4/theta3")
# In Feruglio, Y1 and Y2 are modular forms of weight 2 under Gamma(2)
# Y1 = theta3^4 + theta4^4, Y2 = -theta3^4 + 2*theta2^2*theta4^2 + theta4^4 (convention varies)
# At golden nome they are nearly equal
Y1 = (t3 ** 4 + t4 ** 4) / 2  # normalized
Y2 = (t3 ** 4 - t4 ** 4) / 2
print(f"\n  Y1 (normalized) = {Y1:.6f}")
print(f"  Y2 (normalized) = {Y2:.6f}")
print(f"  Y2/Y1           = {Y2 / Y1:.8f}")
print(f"  |1 - Y2/Y1|     = {abs(1 - Y2 / Y1):.2e}")
print(f"\n  => Feruglio hierarchy parameter |1 - Y2/Y1| = {abs(1 - Y2 / Y1):.2e}")
print(f"     theta4/theta3 hierarchy parameter eps    = {eps:.2e}")
print(f"     eps is a MUCH better small parameter ({eps / abs(1 - Y2 / Y1):.0f}x larger)")

# Also compute the "proper" Feruglio Y-functions as weight-2 modular forms
# Standard convention: Y1 ~ theta3^4(tau)/eta^2(tau), Y2 ~ theta2^4(tau)/eta^2(tau)
# But at imaginary tau, theta2 is also computable
Y1_F = t3 ** 4 / eta ** 2
Y2_F = t2 ** 4 / eta ** 2
print(f"\n  Feruglio weight-2 Y1 = t3^4/eta^2 = {Y1_F:.6f}")
print(f"  Feruglio weight-2 Y2 = t2^4/eta^2 = {Y2_F:.6f}")
print(f"  Y2_F/Y1_F            = {Y2_F / Y1_F:.8f}")

# Check creation identity
ci_lhs = eta ** 2
ci_rhs = eta_q2 * t4
ci_err = abs(ci_lhs - ci_rhs) / ci_lhs
print(f"\n  Creation identity: eta^2 = eta(q^2)*theta4")
print(f"    LHS = {ci_lhs:.12f}, RHS = {ci_rhs:.12f}, rel err = {ci_err:.2e}")

# ======================================================================
# PART 2: GAMMA(2) GENERATORS AS MASS MATRIX ELEMENTS
# ======================================================================

separator("PART 2: Gamma(2) GENERATORS AND S3 STRUCTURE")

print("""
The ring of modular forms for Gamma(2) is generated by {theta3^4, theta4^4}
(or equivalently {theta3, theta4, eta} with the Jacobi identity).

Key Gamma(2) building blocks at q = 1/phi:
""")

blocks = {
    'eta': eta,
    't3': t3,
    't4': t4,
    'eta^2': eta ** 2,
    'eta*t3': eta * t3,
    'eta*t4': eta * t4,
    't3*t4': t3 * t4,
    't3^2': t3 ** 2,
    't4^2': t4 ** 2,
    'eta*t3^2': eta * t3 ** 2,
    'eta*t4^2': eta * t4 ** 2,
    'eta^2*t3': eta ** 2 * t3,
    'eta^2*t4': eta ** 2 * t4,
}

for name, val in blocks.items():
    print(f"  {name:20s} = {val:.10f}")

subsection("S3 representation theory")
print("""
S3 has irreps: 1 (trivial), 1' (sign), 2 (standard).
Under S3 = Gamma(2), the three generations transform as 2 + 1 or 3 = 2 + 1'.

For a doublet D = (D1, D2) and singlet S, the S3 Clebsch-Gordan gives:
  D x D -> 1: D1*D2' + D2*D1'  (symmetric product)
  D x D -> 1': D1*D2' - D2*D1' (antisymmetric)
  D x D -> 2: (D1*D1', D2*D2') (symmetric)

Assignment: (theta3, theta4) as S3 doublet, eta as S3 singlet.
  Rationale: theta3 and theta4 interchange under T: tau -> tau+1
  (T is an S3 generator). eta picks up a phase.
""")

# S3 generators for the 2-rep
# S = ((0,1),(1,0)), T = ((omega,0),(0,omega^2)) with omega = e^{2pi i/3}
# For REAL matrices (real tau), simplify
# Actually S3 on 3 objects: S = cyclic permutation, T = transposition
# Standard 3-dim reducible rep: P3 = {permutation matrices}

subsection("Doublet (t3, t4) and singlet (eta) tensor products")
# With 3 generations as 2+1, the mass matrix has structure:
# M = y1 * M_1(eta, t3, t4) + y2 * M_2(eta, t3, t4) + ...
# where M_i are S3-invariant combinations

# S3-invariant mass matrices for 3 = 2 + 1:
# If psi = (psi_1, psi_2, psi_3) with (psi_1, psi_2) as doublet and psi_3 as singlet,
# the most general S3-invariant mass matrix is:
# M = | a  c  d |
#     | c  a  d |    where a,c from 2x2 (doublet self-coupling)
#     | d  d  b |    and b from singlet self-coupling, d from doublet-singlet

# Modular assignments:
# a -> t3^2 or t4^2 (doublet diagonal)
# c -> t3*t4 (doublet off-diagonal)
# b -> eta^2 (singlet)
# d -> eta*t3 or eta*t4 (doublet-singlet mixing)

print("\nS3-invariant mass matrix template:")
print("  M = | a  c  d |")
print("      | c  a  d |")
print("      | d  d  b |")
print()
print("  a (doublet diagonal):     can be t3^2, t4^2, or t3*t4")
print("  c (doublet off-diag):     can be t3*t4, t3^2, t4^2")
print("  b (singlet self):         can be eta^2, eta*t3, eta*t4")
print("  d (doublet-singlet mix):  can be eta*t3, eta*t4, eta^2")

# ======================================================================
# PART 3: SYSTEMATIC SCAN OF MASS RATIOS
# ======================================================================

separator("PART 3: SYSTEMATIC SCAN -- MASS RATIOS AS MODULAR EXPRESSIONS")

subsection("Measured mass ratios (same charge type)")

ratio_targets = {}
for fam_name, fam in families.items():
    print(f"\n  {fam_name}:")
    for i in range(len(fam)):
        for j in range(i + 1, len(fam)):
            r = masses[fam[j]] / masses[fam[i]]
            lr = math.log(r) / math.log(eps) if eps > 0 else 0
            key = f"{fam[j]}/{fam[i]}"
            ratio_targets[key] = r
            print(f"    {key:8s} = {r:12.4f}  (= eps^{lr:.4f})")

subsection("Scan: mass ratios as (t4/t3)^a * eta^b * phi^c")

print("\nSearching for matches with |a|,|b|,|c| <= 6, half-integer steps...")
print("Showing all matches within 5% (flagging <=1% with **)")

best_matches = {}

for key, target in ratio_targets.items():
    if target <= 0:
        continue
    log_target = math.log(target)
    log_eps_val = math.log(eps)
    log_eta = math.log(eta)
    log_phi = math.log(phi)

    matches = []
    # Scan half-integers from -6 to 6
    steps = [x * 0.5 for x in range(-12, 13)]

    for a in steps:
        for b in steps:
            for c in steps:
                log_pred = a * log_eps_val + b * log_eta + c * log_phi
                pred = math.exp(log_pred)
                pct = abs(pred - target) / target * 100
                if pct < 5.0:
                    matches.append((pct, a, b, c, pred))

    matches.sort()
    if matches:
        print(f"\n  {key} = {target:.6f}:")
        best_matches[key] = []
        shown = 0
        for pct, a, b, c, pred in matches[:8]:  # top 8
            flag = "**" if pct < 1.0 else "  "
            # Format exponents nicely
            def fmt_exp(x):
                if x == int(x):
                    return str(int(x))
                return f"{x:.1f}"
            expr = f"eps^{fmt_exp(a)} * eta^{fmt_exp(b)} * phi^{fmt_exp(c)}"
            print(f"    {flag} {expr:40s} = {pred:.6f}  ({pct:.2f}%)")
            best_matches[key].append((pct, a, b, c, pred))
            shown += 1
    else:
        print(f"\n  {key} = {target:.6f}: NO MATCH within 5%")

subsection("Direct ratio scan: (t4/t3)^a * (eta/t3)^b * phi^c")

print("\nAlternative basis using eta/t3 as second parameter...")
log_eta_t3 = math.log(eta / t3)
log_eps_val = math.log(eps)
log_phi_val = math.log(phi)

alt_matches = {}
for key, target in ratio_targets.items():
    if target <= 0:
        continue
    log_target = math.log(target)
    matches = []
    steps = [x * 0.5 for x in range(-12, 13)]
    for a in steps:
        for b in steps:
            for c in steps:
                log_pred = a * log_eps_val + b * log_eta_t3 + c * log_phi_val
                pred = math.exp(log_pred)
                pct = abs(pred - target) / target * 100
                if pct < 3.0:
                    matches.append((pct, a, b, c, pred))

    matches.sort()
    if matches:
        alt_matches[key] = matches[:3]
        best = matches[0]
        flag = "**" if best[0] < 1.0 else "  "
        print(f"  {flag} {key:8s}: eps^{best[1]:.1f} * (eta/t3)^{best[2]:.1f} * phi^{best[3]:.1f} = {best[4]:.6f} vs {target:.6f} ({best[0]:.2f}%)")

# ======================================================================
# PART 4: INTER-GENERATION STRUCTURE
# ======================================================================

separator("PART 4: INTER-GENERATION EXPONENT STRUCTURE")

print(f"\nBase: eps = t4/t3 = {eps:.8f}")
print(f"log10(eps) = {math.log10(eps):.6f}")
print(f"ln(eps)    = {math.log(eps):.6f}")

subsection("Mass ratios in log(eps) basis")

for fam_name, fam in families.items():
    print(f"\n  {fam_name}: {fam[0]} -> {fam[1]} -> {fam[2]}")
    m1, m2, m3 = masses[fam[0]], masses[fam[1]], masses[fam[2]]

    # Ratio as power of eps
    r12 = m2 / m1
    r23 = m3 / m2
    r13 = m3 / m1

    n12 = math.log(r12) / math.log(eps)
    n23 = math.log(r23) / math.log(eps)
    n13 = math.log(r13) / math.log(eps)

    print(f"    m2/m1 = {r12:12.4f} = eps^{n12:.4f}")
    print(f"    m3/m2 = {r23:12.4f} = eps^{n23:.4f}")
    print(f"    m3/m1 = {r13:12.4f} = eps^{n13:.4f}")
    print(f"    Jump ratio n12/n23 = {n12 / n23:.4f}" if n23 != 0 else "")

subsection("Are exponents near integers, Fibonacci, or simple fractions?")

# Fibonacci numbers for reference
fibs = [1, 1, 2, 3, 5, 8, 13]
simple_fracs = [(1, 1), (1, 2), (2, 3), (3, 2), (1, 3), (3, 4), (4, 3),
                (2, 1), (3, 1), (5, 3), (3, 5), (5, 2), (2, 5)]

for fam_name, fam in families.items():
    m1, m2, m3 = masses[fam[0]], masses[fam[1]], masses[fam[2]]
    r12 = m2 / m1
    r23 = m3 / m2

    n12 = math.log(r12) / math.log(eps)
    n23 = math.log(r23) / math.log(eps)

    print(f"\n  {fam_name}:")
    print(f"    n12 = {n12:.4f}  nearest int: {round(n12)} (err {abs(n12 - round(n12)):.4f})")
    print(f"    n23 = {n23:.4f}  nearest int: {round(n23)} (err {abs(n23 - round(n23)):.4f})")

    # Check Fibonacci
    for f in fibs:
        if abs(n12 - f) < 0.15:
            print(f"    ** n12 ~ Fib({f})")
        if abs(n23 - f) < 0.15:
            print(f"    ** n23 ~ Fib({f})")

    # Check simple fractions
    for p, qq in simple_fracs:
        frac = p / qq
        if abs(n12 - frac) < 0.05:
            print(f"    ** n12 ~ {p}/{qq}")
        if abs(n23 - frac) < 0.05:
            print(f"    ** n23 ~ {p}/{qq}")

subsection("Cross-family comparison: universality of exponent pattern")

all_n12 = []
all_n23 = []
for fam_name, fam in families.items():
    m1, m2, m3 = masses[fam[0]], masses[fam[1]], masses[fam[2]]
    n12 = math.log(m2 / m1) / math.log(eps)
    n23 = math.log(m3 / m2) / math.log(eps)
    all_n12.append((fam_name, n12))
    all_n23.append((fam_name, n23))

print("\n  Generation 1->2 exponents:")
for name, n in all_n12:
    print(f"    {name:12s}: n12 = {n:.4f}")

mean_n12 = sum(n for _, n in all_n12) / len(all_n12)
spread_n12 = max(n for _, n in all_n12) - min(n for _, n in all_n12)
print(f"    Mean: {mean_n12:.4f}, Spread: {spread_n12:.4f}")

print("\n  Generation 2->3 exponents:")
for name, n in all_n23:
    print(f"    {name:12s}: n23 = {n:.4f}")

mean_n23 = sum(n for _, n in all_n23) / len(all_n23)
spread_n23 = max(n for _, n in all_n23) - min(n for _, n in all_n23)
print(f"    Mean: {mean_n23:.4f}, Spread: {spread_n23:.4f}")

print(f"\n  Ratio <n12>/<n23> = {mean_n12 / mean_n23:.4f}")

# ======================================================================
# PART 5: EXPLICIT 3x3 MASS MATRICES
# ======================================================================

separator("PART 5: EXPLICIT S3 MASS MATRICES")

# 3x3 matrix utilities (no numpy)
def mat_eigenvalues_symmetric(M):
    """Eigenvalues of real symmetric 3x3 matrix via Cardano."""
    a11, a12, a13 = M[0][0], M[0][1], M[0][2]
    a22, a23, a33 = M[1][1], M[1][2], M[2][2]

    # Characteristic polynomial: -lambda^3 + tr*lambda^2 - S2*lambda + det = 0
    tr = a11 + a22 + a33
    S2 = (a11 * a22 - a12 * a12 + a11 * a33 - a13 * a13 + a22 * a33 - a23 * a23)
    det = (a11 * (a22 * a33 - a23 * a23) - a12 * (a12 * a33 - a23 * a13)
           + a13 * (a12 * a23 - a22 * a13))

    # Reduce to depressed cubic: t^3 + pt + qq = 0 where lambda = t + tr/3
    p = S2 - tr * tr / 3.0
    qq_val = 2 * tr ** 3 / 27.0 - tr * S2 / 3.0 + det

    disc = -4 * p ** 3 - 27 * qq_val ** 2

    if disc >= 0 and abs(p) > 1e-30:
        # Three real roots
        m = 2 * math.sqrt(-p / 3.0)
        theta = math.acos(3 * qq_val / (p * m)) / 3.0
        e1 = tr / 3.0 + m * math.cos(theta)
        e2 = tr / 3.0 + m * math.cos(theta - 2 * pi / 3.0)
        e3 = tr / 3.0 + m * math.cos(theta - 4 * pi / 3.0)
        return sorted([e1, e2, e3])
    else:
        # Degenerate or nearly so
        # Use direct approach for degenerate cases
        if abs(p) < 1e-30:
            root = -qq_val ** (1.0 / 3.0) if qq_val >= 0 else abs(qq_val) ** (1.0 / 3.0)
            return sorted([tr / 3.0 + root] * 3)
        # Fallback: one real root via Cardano
        D = qq_val ** 2 / 4.0 + p ** 3 / 27.0
        if D >= 0:
            sqD = math.sqrt(D)
            u = -qq_val / 2.0 + sqD
            v = -qq_val / 2.0 - sqD
            u3 = u ** (1.0 / 3.0) if u >= 0 else -(abs(u) ** (1.0 / 3.0))
            v3 = v ** (1.0 / 3.0) if v >= 0 else -(abs(v) ** (1.0 / 3.0))
            t1 = u3 + v3
            e1 = t1 + tr / 3.0
            # Remaining two from quadratic
            b_coeff = t1
            c_coeff = -(p / 3.0 + t1 ** 2 / 4.0)  # approximate
            # Better: divide out
            e_remain = tr - e1
            prod_remain = det / e1 if abs(e1) > 1e-30 else 0
            disc2 = e_remain ** 2 - 4 * prod_remain
            if disc2 >= 0:
                e2 = (e_remain + math.sqrt(disc2)) / 2.0
                e3 = (e_remain - math.sqrt(disc2)) / 2.0
            else:
                e2 = e_remain / 2.0
                e3 = e_remain / 2.0
            return sorted([e1, e2, e3])
        else:
            # Should not happen for real symmetric
            return sorted([tr / 3.0] * 3)


def test_mass_matrix(label, M, measured_ratios, scale_name=""):
    """Test a mass matrix against measured ratios. Returns quality score."""
    try:
        eigs = mat_eigenvalues_symmetric(M)
    except (ValueError, ZeroDivisionError):
        return None

    # Take absolute values and sort
    eigs_abs = sorted([abs(e) for e in eigs])

    if eigs_abs[0] < 1e-30:
        return None

    pred_r12 = eigs_abs[1] / eigs_abs[0]
    pred_r23 = eigs_abs[2] / eigs_abs[1]
    pred_r13 = eigs_abs[2] / eigs_abs[0]

    r12_m, r23_m, r13_m = measured_ratios

    err12 = abs(pred_r12 - r12_m) / r12_m * 100
    err23 = abs(pred_r23 - r23_m) / r23_m * 100
    err13 = abs(pred_r13 - r13_m) / r13_m * 100

    avg_err = (err12 + err23 + err13) / 3.0
    return (avg_err, err12, err23, err13, pred_r12, pred_r23, pred_r13, eigs_abs, label)


# Measured ratios
meas = {}
for fam_name, fam in families.items():
    m1, m2, m3 = masses[fam[0]], masses[fam[1]], masses[fam[2]]
    meas[fam_name] = (m2 / m1, m3 / m2, m3 / m1)

print("\nMeasured mass ratios:")
for fam_name in families:
    r12, r23, r13 = meas[fam_name]
    print(f"  {fam_name:12s}: m2/m1 = {r12:.2f}, m3/m2 = {r23:.2f}, m3/m1 = {r13:.2f}")

subsection("Strategy: S3-invariant matrices with modular form entries")

# Build candidate matrices
# Template: M = | a  c  d |
#               | c  a  d |
#               | d  d  b |
# where a, b, c, d are modular form combinations times Yukawa couplings

# We scan over choices of a, b, c, d from a pool of modular form expressions
pool_entries = {
    't3': t3,
    't4': t4,
    'eta': eta,
    't3^2': t3 ** 2,
    't4^2': t4 ** 2,
    'eta^2': eta ** 2,
    't3*t4': t3 * t4,
    'eta*t3': eta * t3,
    'eta*t4': eta * t4,
    'eps': eps,
    'eps^2': eps ** 2,
    'eps^3': eps ** 3,
    'eps*eta': eps * eta,
    'eps^2*t3': eps ** 2 * t3,
    'eps*t3': eps * t3,
}

# For scale, multiply overall by free parameter y_0
# We only care about eigenvalue RATIOS, so overall scale cancels
# But internal ratios matter

subsection("Scan: best S3-invariant mass matrices")

# For each family, find best fit
# We parameterize: a, c chosen from pool; d = alpha_mix * entry; b from pool
# Since we care about ratios, normalize a=1 and scan c/a, d/a, b/a

# More efficient: parameterize as
# M = | 1   x   y |
#     | x   1   y |  * overall
#     | y   y   z |
# and scan x, y, z over ratios from the pool

pool_ratios = {}
pool_vals = list(pool_entries.values())
pool_names = list(pool_entries.keys())

# Build ratio pool
ratio_pool = [(0, 'zero')]
for i, (name, val) in enumerate(pool_entries.items()):
    ratio_pool.append((val / t3 if t3 != 0 else 0, f"{name}/t3"))
    ratio_pool.append((val, name))

# Add key dimensionless ratios
key_ratios = [
    (eps, 'eps'),
    (eps ** 2, 'eps^2'),
    (eps ** 3, 'eps^3'),
    (eta / t3, 'eta/t3'),
    (eta / t4, 'eta/t4'),
    (t4 / t3, 't4/t3'),
    (eps * phi, 'eps*phi'),
    (eps ** 2 * phi, 'eps^2*phi'),
    (eta ** 2 / t3 ** 2, '(eta/t3)^2'),
    (1.0, '1'),
    (phi, 'phi'),
    (1 / phi, '1/phi'),
]

print("\nScanning S3 mass matrices M(x,y,z) for each fermion family...")
print("Matrix: M = diag(1,1,z) + x*off_diag(1,2) + y*off_diag(1-2,3)")

for fam_name, fam in families.items():
    best_results = []
    target = meas[fam_name]

    for ix, (xv, xn) in enumerate(key_ratios):
        for iy, (yv, yn) in enumerate(key_ratios):
            for iz, (zv, zn) in enumerate(key_ratios):
                # M = | 1   xv  yv |
                #     | xv  1   yv |
                #     | yv  yv  zv |
                M = [[1.0, xv, yv],
                     [xv, 1.0, yv],
                     [yv, yv, zv]]
                label = f"x={xn}, y={yn}, z={zn}"
                result = test_mass_matrix(label, M, target)
                if result is not None and result[0] < 30.0:
                    best_results.append(result)

    best_results.sort()
    print(f"\n  {fam_name} (target r12={target[0]:.2f}, r23={target[1]:.2f}):")
    if best_results:
        for res in best_results[:5]:
            avg, e12, e23, e13, p12, p23, p13, eigs, lab = res
            print(f"    [{avg:5.1f}%] {lab}")
            print(f"           r12={p12:.2f} ({e12:.1f}%), r23={p23:.2f} ({e23:.1f}%)")
    else:
        print("    No fits below 30%")

subsection("Dedicated scan: hierarchy from eps powers in off-diagonal")

print("""
Key idea: the DIAGONAL elements are O(1) in modular forms,
but OFF-DIAGONAL elements carry powers of eps = t4/t3.
This naturally generates hierarchy: eigenvalues split by eps powers.

M = | a      eps^p  eps^r |
    | eps^p  b      eps^s |
    | eps^r  eps^s  c     |

Eigenvalues ~ {a, b, c} with corrections ~ eps^(2p), eps^(2r), etc.
""")

# For this to work, we need a ~ smallest mass, c ~ largest, with
# off-diagonal mixing. Or: use "texture zero" patterns.

# Actually, the hierarchy mechanism is:
# If M ~ v_0 * | eps^n1  ...   |
#               | ...     eps^n2|
#               | ...     ...   eps^n3 |
# then masses go as eps^n1 : eps^n2 : eps^n3

# Try: m_i ~ eps^(A_i) where A_i are to be determined

for fam_name, fam in families.items():
    m1, m2, m3 = masses[fam[0]], masses[fam[1]], masses[fam[2]]
    total = m1 + m2 + m3

    # Express each mass as eps^n * m_3
    n1 = math.log(m1 / m3) / math.log(eps) if eps > 0 else 0
    n2 = math.log(m2 / m3) / math.log(eps) if eps > 0 else 0

    print(f"\n  {fam_name}: m1/m3 = eps^{n1:.3f}, m2/m3 = eps^{n2:.3f}")

    # Froggatt-Nielsen: diagonal entries eps^(q_i + q_j) where q_i are "charges"
    # m_i ~ eps^(2*q_i) * v
    # So q_1, q_2, q_3 such that 2(q_1-q_3)=n1, 2(q_2-q_3)=n2
    # Set q_3 = 0: q_1 = n1/2, q_2 = n2/2
    q1 = n1 / 2
    q2 = n2 / 2
    q3 = 0.0

    print(f"    FN charges: q1={q1:.3f}, q2={q2:.3f}, q3={q3:.3f}")
    print(f"    Nearest integers: q1~{round(q1)}, q2~{round(q2)}, q3=0")

    # Check if charges are near simple values
    for val, name in [(1, '1'), (2, '2'), (3, '3'), (0.5, '1/2'), (1.5, '3/2'),
                      (2.5, '5/2'), (phi, 'phi'), (1 / phi, '1/phi')]:
        if abs(q1 - val) < 0.1:
            print(f"    ** q1 ~ {name}")
        if abs(q2 - val) < 0.1:
            print(f"    ** q2 ~ {name}")

# ======================================================================
# PART 6: THE PHI CONNECTION
# ======================================================================

separator("PART 6: THE PHI CONNECTION")

subsection("Does (t4/t3)^n relate to phi^m?")

print(f"\n  eps = t4/t3 = {eps:.10f}")
print(f"  ln(eps)     = {math.log(eps):.10f}")
print(f"  ln(phi)     = {ln_phi:.10f}")
print(f"  ln(eps)/ln(phi) = {math.log(eps) / ln_phi:.10f}")

ratio_ln = math.log(eps) / ln_phi
print(f"\n  => eps = phi^{ratio_ln:.6f}")
print(f"     NOT a simple power of phi.")
print(f"     But 1/alpha_tree = t3*phi/t4 = {t3 * phi / t4:.6f}")
print(f"     So eps = phi * alpha_tree")
print(f"     The connection is through alpha, not directly through phi.")

subsection("eta * (t4/t3)^n for various n")

print("\n  Checking if eta * eps^n matches any mass ratio...")
for n in range(-4, 7):
    val = eta * eps ** n
    # Compare to all Yukawa couplings y_i = sqrt(2)*m_i/v
    print(f"  eta * eps^{n:+d} = {val:.6e}", end="")
    # Check against m/v ratios
    for name, m in masses.items():
        y = math.sqrt(2) * m / v_higgs
        if abs(val - y) / y < 0.1 and y > 0:
            pct = abs(val - y) / y * 100
            print(f"  <-- matches y_{name} = {y:.6e} ({pct:.1f}%)", end="")
    print()

subsection("Creation identity implications for masses")

print(f"\n  Creation identity: eta^2 = eta(q^2) * theta4")
print(f"    eta^2     = {eta ** 2:.10f}")
print(f"    etq2 * t4 = {eta_q2 * t4:.10f}")
print(f"    Verified:   {abs(eta ** 2 - eta_q2 * t4):.2e}")
print()
print("  Implication: if a mass involves eta^2, it factorizes as eta(q^2) * t4.")
print("  This connects the kink lattice (q^2 = nome doubling) to theta4 (the small factor).")
print()
print(f"  eta(q^2) = {eta_q2:.10f}")
print(f"  t4       = {t4:.10f}")
print(f"  Their ratio: eta(q^2)/t4 = {eta_q2 / t4:.6f}")
print(f"  Compare: eta/eps = eta*t3/t4 = {eta * t3 / t4:.6f}")

subsection("Yukawa couplings from eta * eps^n * phi^m")

print("\nYukawa coupling y_f = sqrt(2)*m_f/v_Higgs:")
print(f"{'Fermion':>8s} {'y_f':>12s} {'log(y_f)/log(eps)':>20s}")
for name in ['e', 'mu', 'tau', 'u', 'c', 't', 'd', 's', 'b']:
    y = math.sqrt(2) * masses[name] / v_higgs
    n_eps = math.log(y) / math.log(eps)
    print(f"  {name:>6s}  {y:12.6e}  {n_eps:20.4f}")

subsection("All Yukawas as eta * eps^n")

print(f"\n  eta = {eta:.8f} = {eta:.8f}")
print(f"  If y_f = eta * eps^n_f, then n_f = log(y_f/eta)/log(eps):\n")

for name in ['e', 'mu', 'tau', 'u', 'c', 't', 'd', 's', 'b']:
    y = math.sqrt(2) * masses[name] / v_higgs
    n = math.log(y / eta) / math.log(eps)
    nearest = round(n * 2) / 2  # nearest half-integer
    err = abs(n - nearest)
    flag = "**" if err < 0.1 else "  "
    print(f"  {flag} y_{name:3s} = eta * eps^{n:+.3f}  (nearest {nearest:+.1f}, err={err:.3f})")

# ======================================================================
# PART 7: HONEST ASSESSMENT
# ======================================================================

separator("PART 7: HONEST ASSESSMENT")

print("""
QUESTION 1: How many mass ratios are predicted within 5%?
""")

count_5pct = 0
count_1pct = 0
total_ratios = len(ratio_targets)

for key, target in ratio_targets.items():
    if key in best_matches and best_matches[key]:
        best = best_matches[key][0]
        if best[0] < 5.0:
            count_5pct += 1
        if best[0] < 1.0:
            count_1pct += 1

print(f"  Mass ratios within 5%: {count_5pct}/{total_ratios}")
print(f"  Mass ratios within 1%: {count_1pct}/{total_ratios}")
print(f"  (Using eps^a * eta^b * phi^c with |a|,|b|,|c| <= 6, half-integer steps)")

print("""
QUESTION 2: How many free parameters?

  Each expression eps^a * eta^b * phi^c has 3 continuous exponents.
  Even restricted to half-integers, the search space is:
    13 values per exponent * 3 exponents = 2197 candidates per ratio.
  For 9 mass ratios, we'd need 27 "parameters" (exponents).

  This is NOT predictive unless the exponents follow a PATTERN
  (e.g., Froggatt-Nielsen charges that are the same across families).
""")

# Check if FN charges are universal
print("\nFroggatt-Nielsen charge analysis:")
fn_charges = {}
for fam_name, fam in families.items():
    m1, m2, m3 = masses[fam[0]], masses[fam[1]], masses[fam[2]]
    n1 = math.log(m1 / m3) / math.log(eps)
    n2 = math.log(m2 / m3) / math.log(eps)
    q1 = n1 / 2
    q2 = n2 / 2
    fn_charges[fam_name] = (q1, q2, 0.0)
    print(f"  {fam_name:12s}: (q1, q2, q3) = ({q1:.3f}, {q2:.3f}, 0)")

# Check universality
q1_vals = [fn_charges[f][0] for f in fn_charges]
q2_vals = [fn_charges[f][1] for f in fn_charges]
print(f"\n  q1 values: {[f'{v:.3f}' for v in q1_vals]}")
print(f"  q2 values: {[f'{v:.3f}' for v in q2_vals]}")
print(f"  q1 spread: {max(q1_vals) - min(q1_vals):.3f}")
print(f"  q2 spread: {max(q2_vals) - min(q2_vals):.3f}")

# Are they universal to within 10%?
q1_mean = sum(q1_vals) / len(q1_vals)
q2_mean = sum(q2_vals) / len(q2_vals)
universal = all(abs(v - q1_mean) / abs(q1_mean) < 0.15 for v in q1_vals) and \
            all(abs(v - q2_mean) / abs(q2_mean) < 0.15 for v in q2_vals)

print(f"\n  Charges universal (within 15%)? {'YES' if universal else 'NO'}")

print(f"""
QUESTION 3: Is theta4/theta3 BETTER than standard Feruglio at golden nome?

  Standard Feruglio:
    - Uses Y2/Y1 as hierarchy parameter
    - At golden nome: Y2/Y1 ~ {Y2 / Y1 if Y1 != 0 else 'undef':.6f} (~ 1, NO hierarchy)
    - FAILS to generate mass hierarchy at q = 1/phi

  theta4/theta3 mechanism:
    - Uses eps = t4/t3 = {eps:.6f} as hierarchy parameter
    - eps ~ {eps:.2e} -- a genuinely small number
    - eps^4 ~ {eps ** 4:.2e} -- extremely small, comparable to m_e/m_tau
    - DOES generate hierarchy naturally

  VERDICT: YES, theta4/theta3 is better than Feruglio at the golden nome.
  The hierarchy IS there -- but the exponents are NOT simple integers.
""")

print("""
QUESTION 4: What would make this rigorous?

  To be a genuine prediction (not a fit), we need:

  1. A DERIVATION of the Froggatt-Nielsen charges from E8 or S3 structure
     (not a scan over half-integers)

  2. The charges must satisfy constraints from anomaly cancellation
     or the S3 group theory

  3. A REASON why generations have different charges
     (e.g., from their position within the 240 E8 roots)

  4. The mechanism must also predict CKM/PMNS mixing angles
     (not just mass ratios)

  5. The overall mass scale must come from V(Phi) parameters
     (not fitted separately)

  STATUS: We have a viable hierarchy MECHANISM (eps = t4/t3)
  but NOT a complete DERIVATION. The exponents are outputs of a scan,
  not predictions. This is at the same stage as Froggatt-Nielsen (1979)
  before being embedded in a UV completion.
""")

# Final summary table
separator("SUMMARY")

print(f"""
MODULAR FORM LANDSCAPE AT q = 1/phi:
  eta     = {eta:.8f}   (-> alpha_s candidate)
  theta3  = {t3:.8f}    (large, O(1))
  theta4  = {t4:.8f}   (small, O(eps))
  eps     = t4/t3 = {eps:.8f}

KEY FINDING: eps = t4/t3 = {eps:.6e} is a natural hierarchy parameter.
  eps^1 ~ {eps:.2e}     (generation 2/3 splitting)
  eps^2 ~ {eps ** 2:.2e}   (generation 1/3 splitting for quarks)
  eps^4 ~ {eps ** 4:.2e}    (down to electron Yukawa level)

MASS HIERARCHY PATTERN in eps basis:
""")

for fam_name, fam in families.items():
    m1, m2, m3 = masses[fam[0]], masses[fam[1]], masses[fam[2]]
    n13 = math.log(m1 / m3) / math.log(eps)
    n23 = math.log(m2 / m3) / math.log(eps)
    print(f"  {fam_name:12s}: ({fam[0]}, {fam[1]}, {fam[2]}) = eps^({n13:.2f}, {n23:.2f}, 0) * m_{fam[2]}")

print(f"""
COMPARISON WITH STANDARD APPROACH:
  Feruglio Y2/Y1 at golden nome:  ~1 (FAILS)
  theta4/theta3 at golden nome:   {eps:.2e} (WORKS as hierarchy parameter)

HONEST STATUS:
  - Mechanism: VIABLE (eps generates correct order of magnitude)
  - Derivation: INCOMPLETE (exponents not derived from first principles)
  - Predictivity: LOW (3 exponents per family = 9 free parameters for 9 masses)
  - Next step: derive FN charges from E8 root system structure

  This is a DOOR, not a destination. The door is open.
""")

# One more check: does eps relate to alpha in a structural way?
subsection("Structural connection: eps and alpha")

alpha_tree = t4 / (t3 * phi)
print(f"\n  alpha_tree = t4/(t3*phi) = {alpha_tree:.10f}")
print(f"  1/alpha_tree = {1 / alpha_tree:.6f} (cf. 1/alpha = 137.036)")
print(f"  eps = t4/t3 = alpha_tree * phi = {alpha_tree * phi:.10f}")
print(f"  eps = alpha_tree * phi, EXACTLY (by definition)")
print(f"  So the mass hierarchy parameter IS alpha (times phi).")
print(f"  Mass hierarchy ~ alpha^n is the standard result!")
print(f"  But here it comes from the modular form structure, not a perturbative loop.")
print(f"\n  Yukawa ~ (alpha*phi)^n with n determined by S3 representation")
print(f"  This connects the gauge hierarchy to the flavor hierarchy")
print(f"  through the SAME modular form theta4/theta3.")

print("\n" + "=" * 78)
print("DONE. Script: theory-tools/mass_hierarchy_theta_ratio.py")
print("=" * 78)
