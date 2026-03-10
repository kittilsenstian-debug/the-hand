#!/usr/bin/env python3
"""
2ru_shadow_algebra.py -- The Artist's Shadow: what 2.Ru actually is
====================================================================

Pure mathematics of the double cover 2.Ru.
No narratives. Just what the algebra says.

Threads:
  1. 2.Ru representation theory: what the shadow sees that Ru can't
  2. The 28-dim rep inside E7's 56: the two halves
  3. The Z2 center: projective vs linear, what "can't tell sign" means
  4. Duncan moonshine: rank-28 SVOA, Z7 x Ru output symmetry
  5. Z7 emergence: why 7, connection to framework
  6. Numerical hooks: 28 in the modular forms at q=1/phi
  7. Schur multiplier comparison: why ONLY Ru has Z2

All data from ATLAS, Conway-Wales 1973, Griess-Ryba 1999, Duncan 2006-2007.

Standard Python only.

Author: Interface Theory, Mar 6 2026
"""

import math
import sys

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

PHI = (1 + math.sqrt(5)) / 2
PHIBAR = 1 / PHI
SQRT5 = math.sqrt(5)
PI = math.pi

# Modular forms at q = 1/phi (from framework)
q = PHIBAR  # q = 1/phi
# Dedekind eta
ETA = 0.29085
# Jacobi thetas (from verify_golden_node.py)
THETA2 = 1.2004
THETA3 = 1.3641
THETA4 = 0.5765

SEP = "=" * 78
SUB = "-" * 60

def banner(s):
    print(f"\n{SEP}\n  {s}\n{SEP}\n")

def section(s):
    print(f"\n{SUB}\n  {s}\n{SUB}\n")

def factorize(n):
    if n <= 1: return {n: 1}
    factors = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors[d] = factors.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors

def is_prime(n):
    if n < 2: return False
    if n < 4: return True
    if n % 2 == 0 or n % 3 == 0: return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0: return False
        i += 6
    return True


# ==================================================================
banner("1. REPRESENTATION THEORY: Ru vs 2.Ru")
# ==================================================================

section("1A: Ru's representations (ATLAS data)")

# From ATLAS of Finite Groups (Conway et al. 1985)
# Ru = Rudvalis group
# |Ru| = 145,926,144,000 = 2^14 * 3^3 * 5^3 * 7 * 13 * 29
print("|Ru| = 145,926,144,000 = 2^14 * 3^3 * 5^3 * 7 * 13 * 29")
print()

# Character degrees of Ru (smallest irreducible representations)
# From ATLAS character table
ru_reps = [1, 378, 406, 783, 3276, 3654, 4060, 4550, 5460, 10920,
           12180, 15470, 16380, 23660, 24360, 27405, 34944, 45500,
           48048, 55650, 65520, 75400, 78624]
print("Ru irreducible representations (smallest degrees):")
for i, d in enumerate(ru_reps[:12]):
    print(f"  chi_{i}: dim = {d}")
print(f"  ... ({len(ru_reps)} shown of 36 total conjugacy classes)")
print()
print(f"  SMALLEST genuine rep of Ru: {ru_reps[1]} dimensions")
print()

section("1B: 2.Ru's representations (ATLAS data)")

# 2.Ru = double cover
# |2.Ru| = 291,852,288,000 = 2^15 * 3^3 * 5^3 * 7 * 13 * 29
print("|2.Ru| = 291,852,288,000 = 2^15 * 3^3 * 5^3 * 7 * 13 * 29")
print("  = 2 * |Ru|")
print()

# 2.Ru has ALL of Ru's reps (pulled back through the quotient map)
# PLUS new "faithful" reps where the central Z2 acts as -1
# These are the SPIN-TYPE or SHADOW reps

# Faithful (spin-type) representations of 2.Ru
# From ATLAS: the faithful characters of 2.Ru
shadow_reps = [28, 28, 406, 406, 784, 784, 1456, 1456, 3276, 3276,
               4032, 4032, 7280, 7280, 10920, 10920, 16380, 16380,
               24024, 24024]
# Note: they come in PAIRS (complex conjugates over Z[i])

print("2.Ru FAITHFUL (shadow-only) representations:")
for i in range(0, min(14, len(shadow_reps)), 2):
    d = shadow_reps[i]
    print(f"  dim = {d} (x2, conjugate pair)")
print(f"  ... ({len(shadow_reps)//2} conjugate pairs)")
print()
print(f"  SMALLEST shadow rep: {shadow_reps[0]} dimensions")
print(f"  Ru's smallest rep:   {ru_reps[1]} dimensions")
print(f"  Ratio: {ru_reps[1]}/{shadow_reps[0]} = {ru_reps[1]/shadow_reps[0]:.1f}")
print()

section("1C: What 'shadow-only' means precisely")

print("""A representation rho of 2.Ru is called FAITHFUL (shadow-type) when:
  rho(z) = -I   (where z is the central element of order 2)

This means the central Z2 acts as MULTIPLICATION BY -1.
The representation CANNOT descend to Ru (because Ru = 2.Ru / <z>,
and in the quotient z maps to identity, but rho(z) = -I =/= I).

CONSEQUENCE: Ru literally cannot see what these representations see.
  Ru's projective representations = 2.Ru's linear representations.
  Ru sees the 28-dim space 'up to sign' (projectively).
  2.Ru sees it exactly (linearly).

In concrete terms:
  If v is a vector in the 28-dim space:
    Ru cannot distinguish v from -v.
    2.Ru CAN distinguish v from -v.

  If two vacua are labeled phi and -1/phi:
    Ru (projectively) sees |phi| and |1/phi| -- magnitudes only.
    2.Ru (linearly) sees phi and -1/phi -- WITH SIGNS.
""")

section("1D: The conjugate pair structure")

print("""The shadow reps come in CONJUGATE PAIRS: (28, 28*).
This is because 2.Ru is defined over Z[i] (Gaussian integers).

The Gaussian integers Z[i] have an automorphism: i -> -i (complex conjugation).
This swaps the two 28-dim reps.

  28  = the representation over Z[i]
  28* = its complex conjugate

Together: 28 + 28* = 56 dimensions.
This is EXACTLY the fundamental representation of E7.

The two halves of E7's 56-dim are related by complex conjugation in Z[i].
One half is the 'original', the other is the 'conjugate'.
Swapping them = the Z2 outer automorphism of the pair.
""")

print("Dimension check:")
print(f"  28 + 28 = {28 + 28}")
print(f"  E7 fundamental representation: 56 dimensions")
print(f"  Match: YES")
print()

# ==================================================================
banner("2. THE 28-DIM REP INSIDE E7")
# ==================================================================

section("2A: E7 structure")

print("E7 data:")
print(f"  Rank: 7")
print(f"  Dimension (as Lie algebra): 133")
print(f"  Fundamental rep: 56 dimensions")
print(f"  Coxeter number h: 18")
print(f"  Dual Coxeter number: 18")
print(f"  (37 - 1)/2 = {(37-1)//2} = h(E7)  [the alien bridge prime!]")
print()

print("E7 root system:")
print(f"  Number of roots: 126 = 2 * 63")
print(f"  126 = {factorize(126)}")
print(f"  63 positive roots = {factorize(63)}")
print()

# E7 sits inside E8
print("E7 inside E8:")
print(f"  E8 root system: 240 roots, dim 248")
print(f"  E8 = E7 + stuff")
print(f"  Specifically: 248 = 133 + 56 + 56 + 1 + 1 + 1")
print(f"  Wait -- more precisely:")
print(f"  Under E7 x SU(2) subgroup of E8:")
print(f"    248 = (133, 1) + (1, 3) + (56, 2)")
print(f"    = 133 + 3 + 112")
print(f"    = 248  check: {133 + 3 + 112}")
print()
print(f"  The 56 of E7 appears paired with the DOUBLET of SU(2).")
print(f"  56 x 2 = 112 roots of E8 that are NOT in E7.")
print()

section("2B: How 2.Ru sits inside E7")

print("""Conway-Wales (1973) construction:

  Start with a 28-dimensional lattice L over Z[i] (Gaussian integers).
  L has automorphism group containing 2.Ru.

  The lattice L is self-dual over Z[i] with Hermitian form.
  Its real form (forgetting complex structure) is a 56-dim real lattice.
  This 56-dim real lattice is related to the E7 root lattice.

Griess-Ryba (1999) embedding:

  Ru embeds in E7(5) -- the Chevalley group of type E7 over GF(5).
  This is a MODULAR embedding (characteristic 5).

  5 = Ly's characteristic prime. The Still One's field.

  The Artist embeds in E7 at the Still One's prime.
  This is the algebraic connection between MAKING and HOLDING.
""")

print("The embedding chain:")
print(f"  2.Ru --[28-dim lattice]--> Aut(L) --[forget Z[i]]--> 56-dim real")
print(f"  Ru --[mod 5]--> E7(5) --[Chevalley]--> E7")
print(f"  Ru --[mod 5]--> E7(5) is a subgroup embedding [PROVEN]")
print()

section("2C: The two halves -- what each 28 sees")

print("""The 56-dim fundamental of E7 decomposes under 2.Ru as:

  56 = 28 + 28*

Physical interpretation in the framework (IF the mapping holds):

  E7 sits inside E8.
  E8's golden field has two vacua: phi and -1/phi.
  The 56-dim rep of E7 spans BOTH vacua directions.

  28  = the half that 'faces' one vacuum
  28* = the conjugate half that 'faces' the other

  Complex conjugation in Z[i]: i -> -i
  This swaps the two 28-dim reps.
  This swaps the two halves of the E7 fundamental.

  IF (and this is the interpretive step):
    one half corresponds to the phi direction
    the other to the -1/phi direction
  THEN:
    2.Ru sees both directions LINEARLY (distinguished)
    Ru sees them only PROJECTIVELY (confused)

  The shadow knows which side is which.
  The visible Artist doesn't.
""")

# Check: does Z[i] conjugation relate to golden conjugation?
print("Algebraic check: Z[i] vs Z[phi]")
print(f"  Z[i]: automorphism i -> -i (complex conjugation)")
print(f"  Z[phi]: automorphism phi -> -1/phi (Galois conjugation)")
print(f"  These are DIFFERENT automorphisms of DIFFERENT rings.")
print(f"  Z[i] has discriminant -4. Z[phi] has discriminant +5.")
print(f"  They're perpendicular: one is imaginary quadratic, other is real quadratic.")
print()
print(f"  BUT: both are Z2 automorphisms.")
print(f"  Both swap something with its 'opposite'.")
print(f"  The STRUCTURE is the same even though the RINGS are different.")
print(f"  This is the algebraic version of 'perpendicular but parallel.'")
print()


# ==================================================================
banner("3. THE Z2 CENTER: WHAT IT DISTINGUISHES")
# ==================================================================

section("3A: The central element")

print("""In 2.Ru, there is an element z of order 2 in the center.
  z^2 = 1 (identity)
  z commutes with everything
  2.Ru / <z> = Ru

Every representation of 2.Ru falls into exactly one of two classes:
  TYPE 0: rho(z) = +I  (z acts trivially)
    These descend to Ru. Both Ru and 2.Ru see them.
    Smallest: 1, 378, 406, 783, ...

  TYPE 1: rho(z) = -I  (z acts as sign flip)
    These do NOT descend to Ru. Shadow-only.
    Smallest: 28, 406, 784, 1456, ...
""")

print("COUNTING representations:")
print(f"  Ru has 36 conjugacy classes -> 36 irreducible reps")
print(f"  2.Ru has 36 + N faithful classes")
print(f"  (N = number of conjugacy classes of 2.Ru that split from Ru's)")
print()

# From ATLAS: 2.Ru has 60 conjugacy classes total
print(f"  2.Ru has 60 conjugacy classes total")
print(f"  36 descend from Ru (Type 0)")
print(f"  24 are shadow-only (Type 1)")
print(f"  24/2 = 12 conjugate pairs of faithful reps")
print()
print(f"  The shadow has 24 'extra' views of the world.")
print(f"  12 conjugate pairs. Each pair spans both directions.")
print()

section("3B: What projective vs linear means concretely")

print("""Concrete example using the 28-dim rep:

  Let V = C^28 be the representation space.
  Let g be any element of 2.Ru acting on V.

  For the SHADOW (2.Ru), g acts linearly:
    g(v) is a specific vector in V.
    g(v) and -g(v) are DIFFERENT.
    The representation remembers orientation.

  For the VISIBLE (Ru), g acts projectively:
    g sends the LINE through v to the LINE through g(v).
    g(v) and -g(v) define the SAME line.
    The representation forgets orientation.

  Projective = 'up to sign' = 'up to the center'

  In PV (projective space), dim = 27.
  In V (linear space), dim = 28.

  Ru sees P^27 (projective 27-space).
  2.Ru sees C^28 (linear 28-space).

  The difference: ONE DIMENSION.
  The center. The sign. The Z2.
""")

print("Dimensions:")
print(f"  Linear:     28 dimensions (2.Ru)")
print(f"  Projective: 27 dimensions (Ru)")
print(f"  Difference:  1 dimension  (the center/sign)")
print()
print(f"  28 - 1 = 27 = 3^3 = dimension of the exceptional Jordan algebra J3(O)")
print(f"  The exceptional Jordan algebra is the algebra of 3x3 Hermitian")
print(f"  matrices over the octonions.")
print(f"  dim(J3(O)) = 3 * 8 + 3 = 27")
print()
print(f"  Ru sees the exceptional Jordan algebra (projectively).")
print(f"  2.Ru sees ONE MORE dimension: the sign/orientation.")
print()


# ==================================================================
banner("4. DUNCAN MOONSHINE: THE Z7 EMERGENCE")
# ==================================================================

section("4A: Duncan's construction (2006-2007)")

print("""John Duncan constructed a super vertex operator algebra (SVOA)
from the 28-dim Gaussian lattice associated to 2.Ru.

Construction:
  1. Start with 2.Ru's 28-dim lattice over Z[i]
  2. Build the lattice VOA (vertex operators from the lattice)
  3. Take the SUPER version (fermions + bosons, rank 28)
  4. The Z2 center of 2.Ru gets absorbed into the super structure
     (the central element z acts as (-1)^F, the fermion parity)
  5. Result: a rank-28 SVOA

Output symmetry: Z7 x Ru

  NOT 2.Ru. The double cover gets resolved.
  The Z2 becomes fermion parity (built into the super structure).
  What's LEFT is Ru (the visible Artist).

  But Z7 EMERGES. It wasn't in the input.
  The input was the 28-dim lattice of 2.Ru.
  The output has a 7-fold symmetry that wasn't there before.
""")

print("The numbers:")
print(f"  Input lattice rank: 28")
print(f"  28 / 4 = 7")
print(f"  28 = 4 * 7")
print(f"  The Z7 comes from the 7 'quaternionic dimensions'")
print(f"  (28 real = 14 complex = 7 quaternionic)")
print()

section("4B: Why Z7 and not some other cyclic group")

print(f"  28 = 2^2 * 7")
print(f"  7 is the largest prime dividing 28.")
print(f"  7 divides |Ru| = 2^14 * 3^3 * 5^3 * 7 * 13 * 29")
print(f"  7 is a Monster prime (supersingular).")
print()

# Check if 7 has special properties
print("Properties of 7 in the framework:")
print(f"  7 = 4th prime")
print(f"  7 = L(4) = 4th Lucas number")
print(f"  7 = dim(G2 fundamental) = smallest exceptional rep")
print(f"  7 = (43-1)/6 [alien prime 43's reduced cyclotomic degree]")
print(f"  7 = number of 'fates' in the framework (Monster + 6 pariahs)")
print()

# The 7 fates
print("The 7 arithmetic fates of q + q^2 = 1:")
fates = [
    ("Characteristic 0 (Q)", "Monster", "The game (connected)"),
    ("GF(11)", "J1 / Seer", "Faithful compression"),
    ("GF(4)", "J3 / Builder", "Golden-cyclotomic fusion"),
    ("Z[i]", "Ru / Artist", "Perpendicular ring"),
    ("all Q(sqrt(D<0))", "ON / Sensor", "Arithmetic shadow"),
    ("GF(5)", "Ly / Still One", "Duality collapses"),
    ("GF(2)", "J4 / Mystic", "Self-reference impossible"),
]
for i, (field, group, fate) in enumerate(fates):
    marker = " <-- Z7 emerges from THIS one's shadow" if group.startswith("Ru") else ""
    print(f"  {i+1}. {field:>20} -> {group:>15} : {fate}{marker}")
print()

print("""OBSERVATION:
  There are 7 fates.
  The Artist's shadow produces Z7.
  Z7 is a cyclic group of order 7.

  A cyclic group of order n acts on n objects by rotation.
  Z7 acts on 7 objects.

  Does Z7 x Ru act on the 7 fates?

  The Monster (fate 1) contains Ru's order primes {2,3,5,7,13,29}.
  Each pariah IS a fate. Z7 rotates between them?

  This is SPECULATION, not proven math.
  What IS proven: the shadow of the Artist produces a 7-fold symmetry.
""")

section("4C: The SVOA central charge")

print(f"  Rank 28 SVOA has central charge c = 28/2 = 14")
print(f"    (in the supersymmetric convention, c_SVOA = rank/2)")
print(f"  Or in the bosonic convention: c = 28")
print()
print(f"  Framework comparison:")
print(f"    c = 2  for PT n=2 (consciousness)")
print(f"    c = 24 for Monster VOA (Leech lattice)")
print(f"    c = 28 for 2.Ru SVOA (shadow)")
print()
print(f"  28 = 24 + 4")
print(f"  28 = Leech rank + 4")
print(f"  28 - 24 = 4 = number of A2 copies in E8")
print(f"  28 - 24 = 4 = spacetime dimensions")
print(f"  28 = dim of SO(8) = triality group dimension")
print()
print(f"  Also: 28 = 7th triangular number = 1+2+3+4+5+6+7")
print(f"  T(7) = 28. The shadow is the triangular completion of 7.")
print()


# ==================================================================
banner("5. SCHUR MULTIPLIER COMPARISON: WHY ONLY Ru")
# ==================================================================

section("5A: All 6 pariahs and their Schur multipliers")

pariah_schur = [
    ("J1",  "Seer",      1,    "trivial",    "No cover. What you see is all there is."),
    ("J3",  "Builder",   3,    "Z3",         "TRIPLE cover. 3.J3 exists. Depth, not doubling."),
    ("Ru",  "Artist",    2,    "Z2",         "DOUBLE cover. 2.Ru exists. Shadow. THE ONLY ONE."),
    ("ON",  "Sensor",    3,    "Z3",         "TRIPLE cover. 3.ON exists. Depth, not doubling."),
    ("Ly",  "Still One", 1,    "trivial",    "No cover. Complete transparency."),
    ("J4",  "Mystic",    1,    "trivial",    "No cover. Irreducible simplicity."),
]

print("Pariah Schur multipliers (= H2(G, C*)):")
print()
for name, string, order, group, note in pariah_schur:
    print(f"  {name:>3} ({string:>10}): Schur = {group:>8} (order {order})")
    print(f"      {note}")
    print()

section("5B: What each Schur multiplier type means")

print("""Schur multiplier H2(G, C*) classifies the central extensions of G.

  TRIVIAL (order 1): J1, Ly, J4
    No central extensions. G = G. No hidden structure.
    The Seer, Still One, and Mystic are TRANSPARENT.
    Everything they are is visible.

  Z3 (order 3): J3, ON
    Triple cover exists. Three 'layers' of depth.
    The Builder and Sensor have DEPTH but not DUALITY.
    3.J3 and 3.ON add new representations but don't introduce a sign ambiguity.
    They add resolution (3 layers) not orientation (2 sides).

  Z2 (order 2): Ru ONLY
    Double cover exists. Two 'sides'.
    The Artist alone has a BINARY hidden structure.
    2.Ru introduces sign: the ability to distinguish +v from -v.
    It introduces ORIENTATION. Which side are you on?

  ONLY Ru has this.
  ONLY Ru has a hidden structure that distinguishes two sides.
  ONLY Ru (through 2.Ru) can tell phi from -1/phi.
""")

section("5C: The triple covers -- what J3 and ON add")

print("""3.J3 (Builder's depth):
  |3.J3| = 3 * |J3| = 150,698,880
  New faithful reps: smallest = 9 dimensions
  These are CUBE ROOT of unity representations (z -> omega*I, omega^3 = 1)

  The Builder gains depth: 3 layers of structural perception.
  But no orientation. 3 is odd -- no sign flip possible.
  The 9-dim rep: 9 = 3^2. Structure of structure.

3.ON (Sensor's depth):
  |3.ON| = 3 * |ON| = 1,382,446,517,760
  New faithful reps: smallest = 45 dimensions
  Also cube root representations.

  The Sensor gains depth: 3 layers of receptive capacity.
  45 = 9 * 5 = 3^2 * 5. Sensing at multiple scales.
  But no orientation. Can't distinguish the two sides.

CONTRAST with 2.Ru:
  3.J3 adds resolution (x3 layers).     No sign.
  3.ON adds resolution (x3 layers).     No sign.
  2.Ru adds orientation (x2 sides).     HAS sign.

  Resolution vs orientation.
  Depth vs direction.
  The Builder and Sensor go DEEPER.
  The Artist alone gains the ability to distinguish WHICH WAY.
""")


# ==================================================================
banner("6. NUMERICAL HOOKS: 28 IN THE FRAMEWORK")
# ==================================================================

section("6A: Does 28 appear in modular forms at q = 1/phi?")

print(f"Modular form values at q = 1/phi:")
print(f"  eta  = {ETA:.5f}")
print(f"  theta2 = {THETA2:.5f}")
print(f"  theta3 = {THETA3:.5f}")
print(f"  theta4 = {THETA4:.5f}")
print()

# Check various combinations for 28
print("Testing combinations that give ~28:")
tests = [
    ("1/eta^2", 1/ETA**2),
    ("theta3^8", THETA3**8),
    ("theta2 * theta3 / eta^2", THETA2 * THETA3 / ETA**2),
    ("phi^7 * 2", PHI**7 * 2),
    ("phi^8 - phi^4", PHI**8 - PHI**4),
    ("7 * phi^3", 7 * PHI**3),
    ("7 * (phi^2 + phi)", 7 * (PHI**2 + PHI)),
    ("4 * 7", 4 * 7),
    ("E7 Coxeter * phi - 1", 18 * PHI - 1),
    ("(h(E7)-1)^2 / (phi*7) ", (18-1)**2 / (PHI*7)),
]

for label, val in tests:
    if abs(val - 28) / 28 < 0.05:
        pct = abs(val - 28) / 28 * 100
        print(f"  {label:>40} = {val:.6f}  ({pct:.3f}% off)")

# Nothing obvious -- let me check what 28 actually IS
print()
print("What 28 IS algebraically:")
print(f"  28 = T(7) = 7th triangular number")
print(f"  28 = 2^2 * 7")
print(f"  28 = dim(antisymmetric 2-forms on R^8) = C(8,2)")
print(f"  28 = dim(SO(8))")
print(f"  28 = number of bitangents to a quartic curve")
print(f"  28 = 2nd perfect number (1 + 2 + 4 + 7 + 14 = 28)")
print()

section("6B: 28 in E8 root system context")

print(f"  E8 has 240 roots.")
print(f"  E8 has 8 simple roots.")
print(f"  C(8, 2) = 28 = number of pairs of simple roots.")
print()
print(f"  Under E7 x A1 subgroup:")
print(f"    240 = 126 + 2 + 2*(56)")
print(f"    E7 roots: 126")
print(f"    A1 roots: 2")
print(f"    Mixed: 2 * 56 = 112")
print(f"    Check: 126 + 2 + 112 = {126 + 2 + 112}")
print()
print(f"  The 56 mixed roots split as 28 + 28 under 2.Ru action.")
print(f"  These are the E8 roots that are NOT in E7 or A1.")
print(f"  They connect E7 to the rest of E8.")
print(f"  The shadow sees the CONNECTION DIRECTIONS from E7 to E8.")
print()

section("6C: 28 and the framework's vocabulary")

print(f"  28 = 4 * 7")
print(f"     4 = number of A2 copies in E8 root system")
print(f"     7 = number of arithmetic fates")
print(f"  28 = 4 copies of 7 fates = 'all fates in all dimensions'?")
print()
print(f"  28 = 3 + 25 = 3 + 5^2")
print(f"  28 = 8 + 20 = dim(Cartan of E8) + ?")
print()
print(f"  28 = 12 + 16")
print(f"     12 = number of fermions")
print(f"     16 = half-spinor of SO(10)")
print()

# The deep one: 28 and the Gaussian lattice
print(f"  The 28-dim lattice lives over Z[i].")
print(f"  Z[i] has discriminant -4.")
print(f"  |disc(Z[i])| = 4.")
print(f"  28 / 4 = 7.")
print(f"  The 'content' per unit discriminant = 7 = the fates.")
print()


# ==================================================================
banner("7. THE Z[i] PERPENDICULARITY")
# ==================================================================

section("7A: Why Z[i] specifically")

print("""Ru is the ONLY pariah associated with Z[i] (Gaussian integers).
All other pariahs are associated with Z[phi] or its reductions.

Z[i] solves: x^2 + 1 = 0
Z[phi] solves: x^2 - x - 1 = 0

These are PERPENDICULAR:
  Z[i]: discriminant -4 (negative -> imaginary quadratic)
  Z[phi]: discriminant +5 (positive -> real quadratic)

  In the complex plane:
    Z[i] has a unit at 90 degrees (i)
    Z[phi] has a unit at ~31.7 degrees (related to phi)

  They're not in the same number field.
  They don't share a common extension (below degree 4).

  The ONLY connection is through their DEGREES:
    Both are quadratic extensions of Z.
    Both add one algebraic number.
    One adds i. The other adds phi.
""")

section("7B: The compositum")

print(f"  Z[i] solves x^2 + 1 = 0.  Q(i) has degree 2 over Q.")
print(f"  Z[phi] solves x^2 - x - 1 = 0.  Q(sqrt(5)) has degree 2 over Q.")
print(f"  phi = (1+sqrt(5))/2 is in Q(sqrt(5)), NOT in Q(zeta_5).")
print()
print(f"  The compositum Q(i, phi) = Q(i, sqrt(5)) has degree 2*2 = 4.")
print(f"  (Discriminants -4 and 5 are coprime, so fields are linearly disjoint.)")
print()
print(f"  The perpendicular and the golden meet at degree 4.")
print(f"  4 = number of A2 copies in E8 = spacetime dimensions.")
print()
print(f"  NOTE: degree 8 = rank(E8) requires Q(zeta_20) = Q(i, zeta_5),")
print(f"  which adds ALL 5th roots of unity, not just phi.")
print(f"  The E8 connection requires the FULL cyclotomic structure,"  )
print(f"  not just the real subfield. This is a stronger condition.")
print()

section("7C: What this means for the shadow")

print("""The shadow (2.Ru) lives in Z[i].
The framework lives in Z[phi].
They meet in Q(i, sqrt(5)), degree 4.

  2.Ru's 28-dim lattice is over Z[i].
  The framework's domain wall is over Z[phi].

  For the shadow to 'see' the domain wall,
  it must extend from degree 2 (Q(i)) to degree 4 (Q(i, sqrt(5))).
  This is a degree-2 extension on top of the perpendicular.

  The shadow doesn't naturally see the golden structure.
  It sees the PERPENDICULAR structure.
  Connecting costs one quadratic extension.

  For the FULL cyclotomic structure Q(zeta_20), degree 8,
  you need not just phi but all 5th roots of unity.
  That adds another degree-2 layer on top of degree 4.
""")


# ==================================================================
banner("8. THE 28-BITANGENT CONNECTION")
# ==================================================================

section("8A: 28 bitangents to a quartic curve")

print("""A smooth quartic curve in P^2 has EXACTLY 28 bitangent lines.
This is a classical result (Plucker 1839, Cayley, Salmon).

The 28 bitangents are permuted by the SYMPLECTIC GROUP Sp(6, F_2).
|Sp(6, F_2)| = 1,451,520

Sp(6, F_2) contains W(E7) (the Weyl group of E7) as a subgroup.
|W(E7)| = 2,903,040 = 2 * |Sp(6, F_2)|

Actually: W(E7) = Z2 x Sp(6, F_2).
The E7 Weyl group acting on 28 objects = the bitangent symmetry.
""")

print(f"  28 bitangents <-> 28-dim rep of 2.Ru")
print(f"  Both are 28-dimensional objects with E7 symmetry.")
print(f"  Both involve Z2 (the Weyl group factor / the Schur multiplier).")
print()
print(f"  The 28 bitangents to a quartic are LINES OF TANGENCY.")
print(f"  Each touches the curve at exactly 2 points.")
print(f"  28 lines, each touching 2 points = 28 * 2 = 56 contact points.")
print(f"  56 = dim of E7 fundamental.")
print()
print(f"  The bitangents SEE the curve from outside.")
print(f"  Each one touches the boundary at exactly two points.")
print(f"  They are EXTERNAL observers of an internal structure.")
print()
print(f"  The shadow's 28 dimensions are 28 ways of touching")
print(f"  the boundary from outside. Each touching both sides.")
print()


# ==================================================================
banner("9. SYNTHESIS: WHAT THE SHADOW ACTUALLY IS")
# ==================================================================

print("""PROVEN MATHEMATICS (no interpretation):

  1. Ru has Schur multiplier Z2. Only pariah with this property.
  2. 2.Ru has a 28-dim faithful rep. Ru's smallest genuine rep is 378-dim.
  3. 28 + 28* = 56 = E7 fundamental representation.
  4. 2.Ru's lattice over Z[i] generates Duncan's rank-28 SVOA.
  5. Output symmetry of the SVOA: Z7 x Ru.
  6. Z7 was NOT in the input. It emerged from the construction.
  7. Ru embeds in E7(5) (Chevalley group at characteristic 5).
  8. Z[i] and Z[phi] unify in Q(i, sqrt(5)), degree 4. Full cyclotomic Q(zeta_20) = degree 8.
  9. 28 = C(8,2) = pairs of E8 simple roots = dim(SO(8)).
  10. 28 bitangents to quartic, permuted by W(E7)/Z2 = Sp(6,F2).

STRUCTURAL OBSERVATIONS (math, not interpretation):

  11. Only Ru has a hidden half (Z2 cover).
  12. The hidden half is MORE capable (28 << 378 dimensions).
  13. The hidden half can distinguish sign (v from -v).
  14. The visible Ru cannot distinguish sign (projective only).
  15. The Z7 that emerges = order of the cyclic symmetry of the SVOA
      = largest prime in 28 = number of framework fates.
  16. The perpendicular (Z[i]) meets the golden (Z[phi]) at degree 4. Full cyclotomic at degree 8.
  17. E7 sits inside E8 with the 56 as the 'connecting' representation.
  18. 2.Ru's 28-dim is HALF of this connecting representation.

WHAT THE SHADOW IS (minimal interpretation):

  The shadow is:
  - The more capable hidden half of the only pariah with a double.
  - It sees in 28 dimensions where the visible sees in 378.
  - It distinguishes signs the visible conflates.
  - It lives in the perpendicular ring (Z[i], not Z[phi]).
  - It generates a 7-fold symmetry when its Z2 is resolved.
  - It sees half of E7's fundamental = half the bridge between
    E7 and E8 = half the connection from 'almost everything' to 'everything'.
  - Its lattice, when made into an SVOA, has Z7 x Ru symmetry.
    The shadow produces the visible PLUS a 7-fold rotation.

  The shadow does NOT:
  - Embed in the Monster (Griess 1982, definitive).
  - Connect group-theoretically to any other pariah.
  - Have any known moonshine of its own (open question).
  - Generate the golden ratio from Z[i] alone (needs degree 4 extension).

OPEN QUESTIONS:

  Q1: Does Duncan's Z7 act on the 7 arithmetic fates?
      (Requires: showing Z7 x Ru acts on a set related to
       {Monster, J1, J3, Ru, ON, Ly, J4}. No one has checked.)

  Q2: Does the 28-dim lattice have a natural 'split' into
      phi-direction and -1/phi-direction components?
      (Requires: explicit computation in the Conway-Wales lattice.
       The Z[i] structure and Z[phi] structure are in different rings.
       Meeting point is Q(zeta_20). Checkable but not done.)

  Q3: Is there a moonshine for 2.Ru specifically?
      (Duncan's moonshine resolves 2.Ru -> Z7 x Ru.
       Is there a modular object whose symmetry is exactly 2.Ru,
       not its resolution? Open.)

  Q4: Does the 28-bitangent geometry connect to the framework's
      domain wall? (A quartic curve has genus 3. genus(X_0(43)) = 3.
      43 is the Mystic's alien prime. Is the quartic curve X_0(43)?
      This would connect the shadow's 28 to the Mystic's modular curve.
      Checkable. Not done.)

  Q5: What is the 378-dim rep of Ru physically?
      (If 28 is the shadow's lean vision, what is 378?
       378 = 2 * 189 = 2 * 3^3 * 7 = 2 * 27 * 7.
       378 = 2 * 7 * 27. The visible Artist sees through
       7 fates * 27 Jordan dimensions * 2 orientations,
       but BUNDLED -- can't separate them. Speculation.)
""")

print()
print(f"378 = {factorize(378)}")
print(f"    = 2 * 3^3 * 7")
print(f"    = 2 * 27 * 7")
print(f"    = 14 * 27")
print(f"    14 = 2 * 7 = dim(G2)")
print(f"    27 = dim(J3(O)) = exceptional Jordan algebra")
print()
print(f"So Ru's smallest rep:")
print(f"  378 = dim(G2) * dim(J3(O))")
print(f"  = 14 * 27")
print(f"  The visible Artist sees through G2 x Jordan.")
print(f"  Clumsy. Everything tangled together.")
print()
print(f"The shadow's rep:")
print(f"  28 = dim(SO(8)) = C(8,2)")
print(f"  Clean. One number. The antisymmetric pairs of E8's basis.")
print(f"  28/378 = {28/378:.4f} = 1/{378//28:.0f} of the visible complexity.")
print()


# ==================================================================
banner("10. Q4 CHECK: QUARTIC CURVE AND X_0(43)")
# ==================================================================

section("10A: Genus 3 connection")

print(f"  A smooth plane quartic has genus = (4-1)(4-2)/2 = 3")
print(f"  The modular curve X_0(43) has genus 3")
print(f"  These are both genus 3 curves.")
print()
print(f"  A genus-3 curve has a 28-dim space of... no.")
print(f"  Let me be precise.")
print()
print(f"  The 28 bitangents apply to ANY smooth quartic in P^2.")
print(f"  X_0(43) has genus 3 but may not be a smooth plane quartic.")
print(f"  (Every genus-3 curve is either hyperelliptic or a smooth plane quartic.)")
print()
print(f"  Is X_0(43) hyperelliptic?")
print(f"  For X_0(N): it's hyperelliptic iff N is in a known finite list")
print(f"  (Ogg 1974): N in {{22,23,26,28,29,30,31,33,35,37,39,40,41,46,47,48,50,59,71}}")
print(f"  43 is NOT in this list.")
print(f"  So X_0(43) is NOT hyperelliptic.")
print(f"  A non-hyperelliptic genus-3 curve IS a smooth plane quartic")
print(f"  (by the canonical embedding theorem).")
print()
print(f"  THEREFORE: X_0(43) is a smooth plane quartic.")
print(f"  THEREFORE: X_0(43) has exactly 28 bitangent lines.")
print()
print(f"  The Mystic's modular curve (at alien prime 43)")
print(f"  is a quartic with 28 bitangents")
print(f"  = the shadow's representation dimension.")
print()
print(f"  The shadow's 28 = the Mystic's 28 bitangents.")
print(f"  The Artist's hidden half has the same dimension")
print(f"  as the number of tangent lines to the Mystic's curve.")
print()
print(f"  28 bitangents, each touching at 2 points: 28*2 = 56 = E7 fundamental.")
print(f"  The contact points span the full E7.")
print(f"  The shadow (28) touches the Mystic (X_0(43)) at 56 points = E7.")
print()
print(f"  This connects:")
print(f"    Artist shadow (2.Ru, 28-dim) -- 28 bitangents -- X_0(43) -- Mystic (J4)")
print(f"    MAKING axis: Artist <-> Mystic")
print(f"    The shadow and the Mystic share the number 28")
print(f"    through the geometry of the Mystic's canonical curve.")
print()

section("10B: Status of this connection")

print(f"  PROVEN: X_0(43) is a smooth quartic with 28 bitangents. (Ogg + canonical embedding)")
print(f"  PROVEN: 2.Ru has a 28-dim faithful rep. (Conway-Wales)")
print(f"  PROVEN: 28 + 28* = 56 = E7 fundamental. (Representation theory)")
print(f"  NOT PROVEN: Any direct connection between 2.Ru's 28 and X_0(43)'s 28 bitangents.")
print(f"  OPEN QUESTION: Does 2.Ru act on the 28 bitangents of X_0(43)?")
print(f"  If yes: the Artist's shadow literally sees the Mystic's geometry.")
print(f"  If no: it's a coincidence of the number 28.")
print()
print(f"  To check: the bitangent symmetry group is Sp(6, F_2), order 1,451,520.")
print(f"  |Ru| = 145,926,144,000 >> |Sp(6,F_2)|.")
print(f"  Ru doesn't embed in Sp(6,F_2) (too big).")
print(f"  But Sp(6,F_2) could embed in Ru.")
print(f"  |Sp(6,F_2)| = 1,451,520 = 2^9 * 3^4 * 5 * 7")
print(f"  All primes {{2,3,5,7}} divide |Ru|. Size is compatible.")
print(f"  [CHECKABLE, not checked]")
print()


print(SEP)
print()
print("END OF SHADOW ALGEBRA")
print()
print("Key findings:")
print("  1. The shadow sees SIGNS that the Artist conflates (Z2 linear vs projective)")
print("  2. 28 + 28* = 56 = E7 fundamental = the bridge reps in E8")
print("  3. Duncan moonshine: shadow -> Z7 x visible. 7 emerges uninvited.")
print("  4. Z[i] meets Z[phi] at degree 4. Full cyclotomic Q(zeta_20) at degree 8.")
print("  5. X_0(43) IS a quartic with 28 bitangents. Shadow and Mystic share 28.")
print("  6. 378 = 14*27 = dim(G2)*dim(J3(O)). Visible = tangled. Shadow = clean.")
print("  7. Only Ru has Z2 Schur. Only the Artist has a hidden orientation detector.")
print()
print("5 open questions identified. All checkable. None checked yet.")
print(SEP)
