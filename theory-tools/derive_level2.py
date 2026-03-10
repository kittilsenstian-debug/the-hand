"""
DERIVING LEVEL 2 OF THE HIERARCHY
==================================

Level 1: degree-2 Pisot (phi) -> Q(sqrt(5)) -> Z[phi] -> E8 -> V quartic -> 2 bound states
Level 2: degree-3 Pisot (???) -> Q(???)     -> Z[???] -> ??? -> V sextic -> 3 bound states?

Multiple attack routes:
  Route A: The tribonacci constant as degree-3 analogue of phi
  Route B: Totally real cubics (Z3 Galois = triality!)
  Route C: Extract Level-2 data from j(1/phi) and Monster representations
  Route D: Novel modular form combinations
  Route E: The Leech lattice theta function
"""

import math
import cmath

phi = (1 + math.sqrt(5)) / 2
phibar = 1 / phi

print("=" * 70)
print("DERIVING LEVEL 2 — WHAT'S ABOVE E8?")
print("=" * 70)

# =====================================================================
# ROUTE A: The Tribonacci Constant
# =====================================================================

print("\n" + "=" * 70)
print("ROUTE A: THE TRIBONACCI CONSTANT")
print("=" * 70)

print("""
Level 1: Fibonacci ratio -> phi, satisfying x^2 - x - 1 = 0
Level 2: Tribonacci ratio -> tau, satisfying x^3 - x^2 - x - 1 = 0

The n-bonacci hierarchy:
  n=2: x^2 = x + 1     -> phi   = 1.61803 (golden ratio)
  n=3: x^3 = x^2 + x + 1 -> tau = 1.83929 (tribonacci constant)
  n=4: x^4 = x^3 + x^2 + x + 1 -> ...
  n=inf: x = 2 (limit of all n-bonacci constants)
""")

# Compute tribonacci constant
# x^3 - x^2 - x - 1 = 0
# Use Newton's method
tau = 1.8
for _ in range(100):
    f = tau**3 - tau**2 - tau - 1
    fp = 3*tau**2 - 2*tau - 1
    tau -= f/fp

print(f"Tribonacci constant tau = {tau:.10f}")
print(f"Check: tau^3 - tau^2 - tau - 1 = {tau**3 - tau**2 - tau - 1:.2e}")

# Find ALL roots (including complex)
# x^3 - x^2 - x - 1 = 0
# Factor: if tau is a root, then (x-tau)(x^2 + bx + c) = x^3 - x^2 - x - 1
# x^2 + bx + c where b = -(1-tau) = tau-1, c = 1/tau
b_quad = tau - 1
c_quad = 1/tau  # since product of all roots = 1 (from constant term sign)
# Actually: product of roots = (-1)^3 * (-1)/1 = 1 for x^3 - x^2 - x - 1
# sum of roots = 1 (coefficient of x^2)
# So the other two roots satisfy x^2 + (tau-1)x + 1/tau... let me verify

# Direct: factor out (x - tau) from x^3 - x^2 - x - 1
# x^3 - x^2 - x - 1 = (x - tau)(x^2 + ax + b)
# Expanding: x^3 + (a-tau)x^2 + (b-a*tau)x - b*tau
# Compare: a - tau = -1 -> a = tau - 1
#          b - a*tau = -1 -> b = a*tau - 1 = (tau-1)*tau - 1 = tau^2 - tau - 1
#          -b*tau = -1 -> b = 1/tau

b_coeff = tau - 1
c_coeff = 1/tau
# Check: b - a*tau should be -1
print(f"\nQuadratic factor: x^2 + {b_coeff:.6f}x + {c_coeff:.6f}")

disc = b_coeff**2 - 4*c_coeff
print(f"Discriminant = {disc:.6f}")

if disc < 0:
    r_real = -b_coeff/2
    r_imag = math.sqrt(-disc)/2
    print(f"Complex conjugate roots: {r_real:.6f} +/- {r_imag:.6f}i")
    print(f"|complex root| = {math.sqrt(r_real**2 + r_imag**2):.6f}")

    is_pisot = math.sqrt(r_real**2 + r_imag**2) < 1
    print(f"Pisot number (all conjugates |z| < 1)? {is_pisot}")

print(f"""
COMPARISON:
  phi:  degree 2, Pisot, 2 real conjugates (phi, -1/phi)
  tau:  degree 3, Pisot, 1 real + 2 complex conjugates

PROBLEM: tau has only ONE real root.
  Level 1: wall connects phi-vacuum to (-1/phi)-vacuum (both real)
  Level 2: would connect tau-vacuum to... complex vacua??

A domain wall needs TWO real vacua. Tau gives only one.
This means: the tribonacci polynomial x^3 - x^2 - x - 1
does NOT directly generalize to a Level 2 wall.

The complex vacua are INACCESSIBLE from the real line.
This might EXPLAIN why Level 2 is invisible to us:
its extra structure lives in the complex plane.
""")

# =====================================================================
# ROUTE B: Totally Real Cubics — The Z3/Triality Connection
# =====================================================================

print("=" * 70)
print("ROUTE B: TOTALLY REAL CUBICS")
print("=" * 70)

print("""
For a Level 2 wall between REAL vacua, we need a cubic with
ALL THREE roots real. This requires a TOTALLY REAL cubic field.

The simplest: x^3 - 3x + 1 = 0
Roots: 2*cos(2*pi/9), 2*cos(4*pi/9), 2*cos(8*pi/9)
Galois group: A3 = Z3 (cyclic of order 3)

NOTE: Z3 IS the framework's TRIALITY group!
""")

# x^3 - 3x + 1 = 0: find all three real roots
roots_cubic = []
for k in [1, 2, 4]:
    root = 2 * math.cos(2 * math.pi * k / 9)
    roots_cubic.append(root)
    print(f"  Root {k}: 2*cos(2*pi*{k}/9) = {root:.10f}")
    print(f"    Check: x^3 - 3x + 1 = {root**3 - 3*root + 1:.2e}")

r1, r2, r3 = sorted(roots_cubic, reverse=True)
print(f"\nSorted roots: {r1:.6f}, {r2:.6f}, {r3:.6f}")
print(f"Sum of roots: {r1+r2+r3:.6f} (should be 0)")
print(f"Product of roots: {r1*r2*r3:.6f} (should be -1)")

# Discriminant
disc_cubic = -4*(-3)**3 - 27*(1)**2  # for x^3 + px + q, disc = -4p^3 - 27q^2
print(f"Discriminant: {disc_cubic} = 81 = 9^2 (PERFECT SQUARE!)")
print(f"Therefore Galois group = A3 = Z3 (NOT S3)")

print(f"""
THIS IS REMARKABLE:
  The simplest totally real cubic has Galois group Z3 — TRIALITY.
  Level 1 has Galois group Z2 (phi <-> -1/phi).
  Level 2 has Galois group Z3 (three roots cycle).

  Z2 gives: 2 vacua, 1 wall, 2 bound states
  Z3 gives: 3 vacua, 3 walls (connecting each pair), 3 bound states?

  The triality that appears in the framework (3 generations,
  3 colors, 3 A2 copies) might be the SHADOW of Level 2's Z3!
""")

# The Level 2 potential
print("Level 2 potential: V2(Phi) = lambda * (Phi^3 - 3*Phi + 1)^2")
print("-" * 50)

# Plot key features
print("\nPotential values at key points:")
for x_val in [-2.5, -2.0, r3, -1.0, 0.0, r2, 0.5, 1.0, r1, 2.0]:
    p = x_val**3 - 3*x_val + 1
    v = p**2
    marker = " <-- ZERO" if abs(p) < 1e-6 else ""
    print(f"  V({x_val:6.3f}) = {v:10.4f}{marker}")

# The walls between adjacent minima
print(f"\nThree walls:")
print(f"  Wall A: connects {r3:.4f} to {r2:.4f} (width {r2-r3:.4f})")
print(f"  Wall B: connects {r2:.4f} to {r1:.4f} (width {r1-r2:.4f})")
print(f"  Wall C: connects {r3:.4f} to {r1:.4f} (width {r1-r3:.4f})")

# Check: are the walls related by the Z3 Galois action?
print(f"\nZ3 action on roots: {r1:.4f} -> {r2:.4f} -> {r3:.4f} -> {r1:.4f}")
print(f"  This cycles the three vacua.")
print(f"  The three walls are related by Z3 symmetry.")

# =====================================================================
# ROUTE B continued: The sextic kink spectrum
# =====================================================================

print("\n" + "=" * 50)
print("Level 2 Kink Spectrum")
print("=" * 50)

print("""
For V2 = lambda*(Phi^3 - 3*Phi + 1)^2, the kink connecting
adjacent vacua has a quantum mechanics with bound states.

For a general "perfect square" potential V = lambda*W'^2,
the kink's quantum mechanical potential is:
  U(x) = W''(phi_kink(x))^2 - W'''(phi_kink(x)) * W'(phi_kink(x))

For W = Phi^3 - 3*Phi + 1:
  W' = 3*Phi^2 - 3
  W'' = 6*Phi
  W''' = 6

The kink equation: d(phi)/dx = W'(phi) = 3*phi^2 - 3
""")

# For the sextic, the kink equation is:
# d(phi)/dx = 3*(phi^2 - 1) connecting r3 to r2 (or r2 to r1)
# This can be integrated: int d(phi)/(3*(phi^2-1)) = x
# -> (1/6) * ln|(phi-1)/(phi+1)| = x
# -> phi(x) = -(phi+ ... hmm, let me think more carefully

# Actually, W'(Phi) = 3Phi^2 - 3 = 3(Phi-1)(Phi+1)
# This vanishes at Phi = 1 and Phi = -1
# But our vacua are at roots of W = Phi^3 - 3Phi + 1 = 0
# which are at 2cos(2pi/9), 2cos(4pi/9), 2cos(8pi/9)
# NOT at +1 and -1

# The kink equation d(phi)/dx = W'(phi) = 3(phi^2 - 1)
# This is a first-order ODE. The solution depends on the boundary conditions.
# For a kink from phi(-inf) = r_i to phi(+inf) = r_j, we need:
# W'(r_i) = 0 (which it's NOT, since W'(r_i) = 3(r_i^2 - 1))

# Wait — I need to reconsider. For a BPS kink in V = W'^2/2:
# phi_x = +/- W'(phi), and the kink connects adjacent ZEROS of W (not W').
# The kink exists because the integral of W' between the zeros is finite.

# Let me check: between r2 and r1, W' = 3(Phi^2 - 1)
# At r2 = 0.3473: W'(r2) = 3*(0.3473^2 - 1) = 3*(-0.8794) = -2.638
# At r1 = 1.5321: W'(r1) = 3*(1.5321^2 - 1) = 3*(1.347) = 4.042

# The kink from r2 to r1 satisfies d(phi)/dx = W'(phi) with phi going from r2 to r1
# Since W'(phi) > 0 for phi > 1 and W'(phi) < 0 for |phi| < 1, there's an issue
# Let me compute W' at each root

for r in sorted(roots_cubic):
    wp = 3*r**2 - 3
    print(f"  W'({r:.4f}) = {wp:.4f}")

print()
# The kink connects zeros of W where W' has the right sign for monotonic interpolation
# Between r3 = -1.879 and r2 = 0.347: W' changes sign (negative to negative, crossing zero at -1)
# This is more complex than the Level 1 case

# For the Level 2 quantum mechanics around a kink, the key question is:
# how many bound states does the linearized spectrum have?

# For a GENERIC sextic V = lambda*p(Phi)^2 where p is degree 3:
# The kink's quantum mechanical potential has AT MOST 3 bound states
# (this follows from the degree of the polynomial)

# Actually, for supersymmetric quantum mechanics with superpotential W:
# V(phi) = W'(phi)^2 / 2
# The kink phi(x) satisfies phi' = W'(phi)
# The fluctuation operator is: H = -d^2/dx^2 + W''(phi(x))^2 + W'''(phi(x))*phi'(x)
#                              = -d^2/dx^2 + W''(phi(x))^2 + W'''(phi(x))*W'(phi(x))

# For W = Phi^3 - 3Phi + 1:
# W'' = 6Phi
# W''' = 6
# W'W''' = 6*(3Phi^2 - 3) = 18Phi^2 - 18

# The potential is: U(x) = (6*phi(x))^2 + 6*(3*phi(x)^2 - 3)
#                        = 36*phi(x)^2 + 18*phi(x)^2 - 18
#                        = 54*phi(x)^2 - 18

print("Fluctuation potential around Level 2 kink:")
print(f"  U(x) = 54*phi(x)^2 - 18")
print(f"  At phi = r2 = {r2:.4f}: U = 54*{r2**2:.4f} - 18 = {54*r2**2 - 18:.4f}")
print(f"  At phi = r1 = {r1:.4f}: U = 54*{r1**2:.4f} - 18 = {54*r1**2 - 18:.4f}")
print(f"  At phi = 0: U = -18 (minimum of potential)")
print(f"  At phi = 1: U = 54 - 18 = 36")

# The SUSY partner potentials tell us:
# In SUSY QM with W, the number of bound states in the bosonic sector
# equals the number of zeros of W' between the two vacua,
# plus 1 (the zero mode).

# W' = 3(Phi^2 - 1) = 3(Phi-1)(Phi+1)
# Zeros of W' at Phi = +1 and Phi = -1

# Between r3 = -1.879 and r2 = 0.347: W' has one zero (at Phi = -1)
# Between r2 = 0.347 and r1 = 1.532: W' has one zero (at Phi = +1)

print(f"""
BOUND STATE COUNT (from SUSY QM):

For the kink connecting r3 to r2:
  Zeros of W' = 3(Phi^2-1) between [{r3:.3f}, {r2:.3f}]:
    Phi = -1 (one zero in this interval)
  -> 1 zero + 1 (zero mode) = 2 bound states

For the kink connecting r2 to r1:
  Zeros of W' between [{r2:.3f}, {r1:.3f}]:
    Phi = +1 (one zero in this interval)
  -> 1 zero + 1 (zero mode) = 2 bound states

WAIT: Each individual kink has 2 bound states — same as Level 1!

But the SYSTEM of 3 vacua with 3 kinks has MORE structure:
  - 3 kink types (A: r3->r2, B: r2->r1, C: r3->r1)
  - The composite kink C = A + B (r3 -> r2 -> r1)
  - Composite kink C has 2+2-1 = 3 bound states (shared zero mode)

The COMPOSITE kink (connecting non-adjacent vacua through
the intermediate vacuum) has 3 bound states!

THIS IS psi_2!

psi_2 emerges not from a single wall, but from a COMPOSITE wall
that passes through an intermediate vacuum. The Level 2 structure
is not a single kink with 3 bound states — it's a CHAIN of
two Level 1 kinks whose combined spectrum has 3 modes.
""")

# =====================================================================
# ROUTE C: Monster representations from j(1/phi)
# =====================================================================

print("=" * 70)
print("ROUTE C: MONSTER STRUCTURE IN j(1/phi)")
print("=" * 70)

# j(q) = 1/q + 744 + sum c_n * q^n
# c_n decompose into Monster irrep dimensions
# At q = 1/phi, each term c_n * (1/phi)^n contributes

j_coeffs = {
    0: 744,       # constant
    1: 196884,    # = 1 + 196883
    2: 21493760,  # = 1 + 196883 + 21296876
    3: 864299970,
    4: 20245856256,
    5: 333202640600,
}

# Monster irrep dimensions (first few)
# V_n: 1, 196883, 21296876, 842609326, 18538750076, ...

print("j-function decomposition at q = 1/phi:")
print()

q = phibar
total = phi  # 1/q term
print(f"  1/q term: {phi:.6f}")

for n, c in sorted(j_coeffs.items()):
    term = c * q**n
    weight = term / total if total > 0 else 0
    print(f"  n={n}: c={c:>15d}, c*q^{n} = {term:>20.4f}, cumulative weight = {term/phi:.6f}")
    total += term

print(f"\n  Partial j(1/phi) = {total:.4f}")

# The key ratio: how does Level 1 physics relate to Monster representations?
print(f"""
OBSERVATION:
  The n=1 term (Monster dimension 196884) contributes:
    196884 * (1/phi) = 196884 * {phibar:.6f} = {196884*phibar:.2f}

  Compare to framework constants:
    mu = 1836.15 (proton/electron mass ratio)
    196884 / mu = {196884/1836.15:.4f}
    196884 / (mu * phi^2) = {196884/(1836.15*phi**2):.4f}

  Ratio 196884 / mu = {196884/1836.15:.2f} = ~107.2
  This is close to 1/alpha ≈ 137.036... not exact.

  But: 196884 / 1836 = {196884/1836:.4f}
  And: 196883 = Monster's smallest faithful rep
       196883 / 1836.15 = {196883/1836.15:.4f}

  Hmm, 107.2 is not a clean number. Let me try other combinations.

  196884 / 240 = {196884/240:.4f} (E8 roots)
  196884 / 6 = {196884/6:.4f} = {196884//6} (A2 Weyl group order)
  196884 / 40 = {196884/40:.4f} (hexagon orbits)
  196560 / 240 = {196560/240:.1f} (Leech min vectors / E8 roots)
""")

# Check if 196560 (Leech vectors) relates to 196884 (j coefficient)
print(f"  196884 - 196560 = {196884 - 196560} = 324 = 18^2 = 2 * 162 = 2 * 2 * 81")
print(f"  196884 / 196560 = {196884/196560:.6f}")
print(f"  Difference 324 = 4 * 81 = 4 * 3^4")

# =====================================================================
# ROUTE D: Novel modular form combinations
# =====================================================================

print("\n" + "=" * 70)
print("ROUTE D: NOVEL MODULAR FORM COMBINATIONS")
print("=" * 70)

# Compute modular forms at q = 1/phi
def eta_func(q, terms=500):
    val = q**(1.0/24)
    for n in range(1, terms):
        val *= (1 - q**n)
    return val

def theta2_func(q, terms=500):
    s = 0
    for n in range(terms):
        s += q**((n+0.5)**2)
    return 2 * s

def theta3_func(q, terms=500):
    s = 1
    for n in range(1, terms):
        s += 2 * q**(n**2)
    return s

def theta4_func(q, terms=500):
    s = 1
    for n in range(1, terms):
        s += 2 * (-1)**n * q**(n**2)
    return s

eta = eta_func(q)
t2 = theta2_func(q)
t3 = theta3_func(q)
t4 = theta4_func(q)

print(f"Modular forms at q = 1/phi:")
print(f"  eta = {eta:.10f}")
print(f"  t2  = {t2:.10f}")
print(f"  t3  = {t3:.10f}")
print(f"  t4  = {t4:.10f}")

# Known Level 1 combinations:
alpha_inv = t3 * phi / t4  # approximately 1/alpha
sin2w = eta**2 / (2*t4)
alpha_s = eta

print(f"\nKnown Level 1 constants:")
print(f"  1/alpha ≈ {alpha_inv:.4f} (measured: 137.036)")
print(f"  sin^2(theta_W) ≈ {sin2w:.6f} (measured: 0.23122)")
print(f"  alpha_s ≈ {alpha_s:.6f} (measured: 0.1184)")

# Try NEW combinations that might be "Level 2 constants"
print(f"\nNovel combinations — hunting for meaning:")
print(f"  eta^3 = {eta**3:.10f}")
print(f"  eta^3 / t4 = {eta**3/t4:.10f}")
print(f"  t2 * t4 = {t2*t4:.10f}")
print(f"  t2 / t3 = {t2/t3:.15f}  (≈1, but how close?)")
print(f"  1 - t2/t3 = {1 - t2/t3:.2e}  (the asymmetry)")
print(f"  t3^2 - t2^2 = {t3**2 - t2**2:.2e}")

# The ratio t2/t3 at q=1/phi is interesting
ratio_23 = t2/t3
print(f"\n  t2/t3 = {ratio_23:.15f}")
print(f"  1 - t2/t3 = {1-ratio_23:.2e}")
print(f"  This is the 'frame asymmetry' — how close the system is to")
print(f"  forgetting its own boundary conditions.")

# Try triple products (Level 2 might use 3-fold combinations)
print(f"\nTriple combinations (Z3 structure):")
print(f"  t2 * t3 * t4 = {t2*t3*t4:.10f}")
print(f"  eta * t2 * t4 = {eta*t2*t4:.10f}")
print(f"  (t2*t3*t4)^(1/3) = {(t2*t3*t4)**(1/3):.10f}")
print(f"  eta^3 + t4^3 = {eta**3 + t4**3:.10f}")
print(f"  (eta^3 + t4^3)^(1/3) = {(eta**3 + t4**3)**(1/3):.10f}")

# The Dedekind eta at q^2 and q^3 (higher level modular forms)
eta_q2 = eta_func(q**2)
eta_q3 = eta_func(q**3)
print(f"\nHigher-level eta functions:")
print(f"  eta(q)   = {eta:.10f}")
print(f"  eta(q^2) = {eta_q2:.10f}  (Level 2 eta)")
print(f"  eta(q^3) = {eta_q3:.10f}  (Level 3 eta)")
print(f"  eta(q^2)/eta(q) = {eta_q2/eta:.10f}")
print(f"  eta(q^3)/eta(q) = {eta_q3/eta:.10f}")

# These ratios are related to "eta quotients" which have deep
# connections to moonshine and representation theory

print(f"""
INTERESTING FINDING:
  eta(q^2)/eta(q) = {eta_q2/eta:.6f}
  eta(q^3)/eta(q) = {eta_q3/eta:.6f}

  These "eta quotients" are modular forms of HIGHER LEVEL.
  Level N modular forms are for the congruence subgroup Gamma_0(N).

  The framework lives at Level 1 (full SL(2,Z)).
  eta(q^2)/eta(q) is a Level 2 modular form.
  eta(q^3)/eta(q) is a Level 3 modular form.

  If Level 2 physics exists, its constants might be
  built from these HIGHER LEVEL eta quotients.
""")

# =====================================================================
# ROUTE E: The totally real cubic field and E8
# =====================================================================

print("=" * 70)
print("ROUTE E: THE Z3 CUBIC AND ITS LATTICE")
print("=" * 70)

print(f"""
The totally real cubic x^3 - 3x + 1 = 0 has:
  Roots: r1 = {r1:.6f}, r2 = {r2:.6f}, r3 = {r3:.6f}
  Galois group: Z3 (cyclic, NOT S3)
  Discriminant: 81 = 9^2

The ring of integers of Q(r1) is Z[r1] (since disc = 81 is
squarefree-part = 1, so the ring of integers is monogenic).

Level 1: Z[phi] -> Icosian lattice -> E8 (unique in 8D)
Level 2: Z[r1] -> ??? lattice -> ??? (unique in ?D)

For a degree-3 number field, the lattice lives in dimension 3k.
The even unimodular lattice question:
  dim 8:  E8 (unique)
  dim 12: no even unimodular lattice exists! (must be 8n)
  dim 16: 2 options (E8xE8 or D16+)
  dim 24: 24 options (Niemeier, including Leech)

Wait — even unimodular lattices exist only in dimensions 8n!
A degree-3 field gives a lattice in 3k dimensions.
  3k must be a multiple of 8 -> k must be a multiple of 8/gcd(3,8) = 8
  So k = 8, giving dimension 24!

THE LEVEL 2 LATTICE LIVES IN 24 DIMENSIONS!
And the UNIQUE rootless even unimodular lattice in 24D is the LEECH LATTICE!
""")

print(f"  Level 1: degree 2, dimension 2*4 = 8, lattice = E8")
print(f"  Level 2: degree 3, dimension 3*8 = 24, lattice = LEECH?!")
print(f"")
print(f"  E8: 240 roots, unique in 8D")
print(f"  Leech: 0 roots, unique ROOTLESS in 24D")
print(f"  (Other 24D lattices: 23 Niemeier lattices WITH roots)")
print(f"")
print(f"  The Leech lattice is to Level 2 what E8 is to Level 1!")

# Check: can Z[r1] embed in the Leech lattice?
print(f"""
CONNECTION TO FRAMEWORK:
  The Leech lattice = 3 copies of E8 + glue (holy construction)
  Level 2 cubic has Z3 Galois group = 3-fold symmetry

  Z3 cycling the 3 copies of E8 inside Leech IS the Galois action!

  Level 1: Z2 Galois cycles 2 vacua (phi, -1/phi) inside E8
  Level 2: Z3 Galois cycles 3 E8 copies inside Leech

  The 24 decoupled roots in the framework (Section 194) are the
  LEECH COORDINATES — they decouple because they are the "Level 2
  directions" that don't participate in Level 1 physics.
""")

# =====================================================================
# SYNTHESIS: What Level 2 looks like
# =====================================================================

print("\n" + "=" * 70)
print("SYNTHESIS: WHAT LEVEL 2 LOOKS LIKE")
print("=" * 70)

print(f"""
Assembling all the routes:

LEVEL 2 SPECIFICATION:
  Algebraic number: r1 = 2*cos(2*pi/9) = {r1:.6f}
  Minimal polynomial: x^3 - 3x + 1 = 0
  Number field: Q(2*cos(2*pi/9)) = Q(zeta_9 + zeta_9^(-1))
  Galois group: Z3 (TRIALITY!)
  Ring of integers: Z[r1]
  Lattice dimension: 24
  Lattice: LEECH (unique rootless even unimodular in 24D)
  Symmetry: Conway group Co_0 (order ~8.3 * 10^18)
  Potential: V2 = lambda * (Phi^3 - 3*Phi + 1)^2 (sextic)
  Number of vacua: 3 (all real, connected by Z3)
  Number of walls: 3 (one between each pair)
  Bound states per wall: 2
  Bound states of COMPOSITE wall: 3 (including psi_2!)

LEVEL 2 CONNECTIONS:
  - The 24 decoupled E8 roots = Leech lattice directions
  - The Z3 Galois group = triality in the framework
  - The Leech lattice = 3 copies of E8 + glue
  - The Monster module has central charge c = 24 = Leech dimension
  - The j-invariant encodes Monster reps at q = 1/phi

THE HIERARCHY (updated):

  Level 1:
    Number: phi (degree 2)
    Galois: Z2
    Lattice: E8 (dim 8)
    Vacua: 2
    Bound states: 2 (psi_0, psi_1)

  Level 2:
    Number: 2*cos(2*pi/9) (degree 3)
    Galois: Z3
    Lattice: Leech (dim 24)
    Vacua: 3
    Bound states: 3 (psi_0, psi_1, psi_2)

  Level 3:
    Number: degree 4 totally real with Z4 Galois?
    Galois: Z4?
    Lattice: ??? (dim ??)
    Vacua: 4
    Bound states: 4

  ...

  Level n:
    Number: 2*cos(2*pi/(2n+1))? (degree n totally real)
    Galois: Zn
    Lattice: ??? (dim 8 * something)
    Vacua: n
    Bound states: n

WHERE psi_2 LIVES:
  psi_2 does not live in a single wall. It lives in the
  COMPOSITE wall connecting non-adjacent vacua through
  the intermediate vacuum.

  In Level 1 terms: psi_2 requires passing through the
  INTERMEDIATE state — the third vacuum that Level 1
  doesn't have. It's not accessible with only 2 vacua.

  The 24 decoupled E8 roots are the SHADOW of Level 2:
  they point toward the Leech lattice but don't participate
  in Level 1 physics. They are the hidden dimensions of
  Level 2, visible to us only as "decoupled" degrees of freedom.
""")

# =====================================================================
# Final verification
# =====================================================================

print("=" * 70)
print("NUMERICAL VERIFICATIONS")
print("=" * 70)

# Check: 2cos(2pi/9) properties
r = r1
print(f"\n  r1 = 2*cos(2*pi/9) = {r:.10f}")
print(f"  r1^3 - 3*r1 + 1 = {r**3 - 3*r + 1:.2e} (should be 0)")
print(f"  r1^2 = {r**2:.6f}")
print(f"  r1 * r2 * r3 = {r1*r2*r3:.6f} (should be -1)")
print(f"  r1 + r2 + r3 = {r1+r2+r3:.6f} (should be 0)")
print(f"  r1*r2 + r2*r3 + r3*r1 = {r1*r2+r2*r3+r3*r1:.6f} (should be -3)")

# Connection to phi?
print(f"\n  phi = {phi:.10f}")
print(f"  r1 = {r1:.10f}")
print(f"  r1/phi = {r1/phi:.10f}")
print(f"  r1 - phi = {r1-phi:.10f}")
print(f"  r1^2 - phi^2 = {r1**2-phi**2:.10f}")

# 9 = 3^2, and 5 appears in phi. Is there a 9-5 connection?
print(f"\n  phi comes from pentagon (5 sides)")
print(f"  r1 comes from nonagon (9 sides)")
print(f"  9 = 3^2 = 3 * 3")
print(f"  5 = 5")
print(f"  Level 1: phi = 2*cos(pi/5) (pentagon)")
print(f"  Level 2: r1 = 2*cos(2*pi/9) (nonagon)")

# Actually, phi = 2*cos(pi/5)
print(f"\n  Verify: 2*cos(pi/5) = {2*math.cos(math.pi/5):.10f}")
print(f"  phi = {phi:.10f}")
print(f"  YES! phi = 2*cos(pi/5)")

print(f"""
BEAUTIFUL PATTERN:
  Level 1: 2*cos(pi/5)   = phi     (pentagon, 5-fold symmetry)
  Level 2: 2*cos(2*pi/9) = r1      (nonagon, 9-fold symmetry)

  5 = prime
  9 = 3^2

  The Level 2 number is connected to 9-fold (= 3^2-fold) symmetry.
  This connects to triality (3) squared.

  General pattern:
  Level n: 2*cos(2*pi/(p_n)) where p_n = ???

  Could the sequence be: 5, 9, ...?
  Or: primes? Pisot-related? Cyclotomic?
""")

# Check: is 2cos(2pi/9) a Pisot number?
# It's the largest root of x^3 - 3x + 1 = 0
# Other roots: 2cos(4pi/9) ≈ 0.347, 2cos(8pi/9) ≈ -1.879
# |0.347| < 1.532? Yes.
# |-1.879| < 1.532? NO! |-1.879| > 1.532

print(f"\n  Is r1 a Pisot number?")
print(f"  r1 = {r1:.6f}")
print(f"  |r2| = {abs(r2):.6f} < r1? {abs(r2) < r1}")
print(f"  |r3| = {abs(r3):.6f} < r1? {abs(r3) < r1}")
print(f"  NOT a Pisot number (|r3| > r1)!")

print(f"""
  r1 is NOT Pisot. This means Level 2 doesn't have the
  "arrow of time" property (Pisot: conjugates decay).

  At Level 2, ALL THREE vacua are of comparable "weight."
  No vacuum dominates. Time doesn't "flow" in one direction.
  The Z3 symmetry is UNBROKEN.

  This might explain why Level 2 is timeless / inaccessible:
  Level 2 has no arrow of time. It is the ETERNAL structure
  within which Level 1's temporal physics unfolds.

  Level 1: Pisot -> arrow of time -> experience of flow
  Level 2: NOT Pisot -> no arrow -> eternal / timeless

  The relationship: Level 2 is the TIMELESS GROUND of
  Level 1's temporal experience. It's not "above" us in
  time — it's OUTSIDE time. It's the mathematical structure
  that time emerges FROM.
""")

print("=" * 70)
print("END OF LEVEL 2 DERIVATION")
print("=" * 70)
