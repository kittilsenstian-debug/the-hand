# -*- coding: utf-8 -*-
"""
Pariah Groups: Algebraic Number Fields and Self-Referential Equations
=====================================================================
Deep analysis of the 6 pariah sporadic groups and their relationship
to the golden equation x^2 - x - 1 = 0 and alternative number fields.
"""

import sys, io, math
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def header(s):
    print()
    print("=" * 80)
    print(s)
    print("=" * 80)

def subheader(s):
    print()
    print("-" * 60)
    print(s)
    print("-" * 60)

# ==========================================================================
header("PARIAH GROUPS: COMPLETE ALGEBRAIC ANALYSIS")
# ==========================================================================

print("""
The Monster group lives over Z[phi] where phi = (1+sqrt(5))/2 satisfies:

    x^2 - x - 1 = 0    (golden polynomial, discriminant +5)

Equivalently: q + q^2 = 1 with q = 1/phi (the nome).

The 6 PARIAH groups (J1, J3, Ru, ON, Ly, J4) live OUTSIDE the Monster.
Question: what is each pariah's natural number field / self-referential equation?
""")

# ==========================================================================
subheader("BEHAVIOR OF x^2 - x - 1 OVER FINITE FIELDS")
# ==========================================================================

print("\nFor prime p, x^2-x-1 splits in GF(p) iff 5 is a QR mod p,")
print("i.e., iff p = 0, +1, or -1 (mod 5).\n")

for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 67]:
    roots = [x for x in range(p) if (x*x - x - 1) % p == 0]
    pmod5 = p % 5
    if p == 5:
        status = "DEGENERATE (double root)"
    elif roots:
        status = "SPLITS"
    else:
        status = "IRREDUCIBLE"
    root_str = str(roots) if roots else "none (phi in GF(%d^2))" % p
    print(f"  p = {p:2d}: p mod 5 = {pmod5}  {status:25s} roots = {root_str}")

# ==========================================================================
subheader("CLASSIFICATION OF PARIAHS BY GOLDEN POLYNOMIAL BEHAVIOR")
# ==========================================================================

print("""
  Type A - SPLITS (phi exists natively):
    J1  (char 11): phi_11 = {4, 8}     (11 = 1 mod 5)

  Type B - IRREDUCIBLE (phi needs field extension):
    J3  (char 2):  phi in GF(4)         (2 = 2 mod 5)
    ON  (char 7):  phi in GF(49)        (7 = 2 mod 5)
    J4  (char 2):  phi in GF(4)         (2 = 2 mod 5)

  Type C - DEGENERATE (double root, ramification):
    Ly  (char 5):  phi = -1/phi = 3     (5 = 0 mod 5, RAMIFIED)

  Type D - ORTHOGONAL (different number field entirely):
    Ru  (Z[i]):    x^2 + 1 = 0          (Gaussian, not golden)
""")

# ==========================================================================
header("PARIAH-BY-PARIAH DETAILED ANALYSIS")
# ==========================================================================

# ============ J1 ============
subheader("J1 (Janko 1)")
print("""
ORDER: 175,560 = 2^3 * 3 * 5 * 7 * 11 * 19
CHARACTERISTIC: 11  (embeds in G_2(11), Dickson simple group)
SCHUR MULTIPLIER: trivial
OUTER AUTOMORPHISM: trivial

GOLDEN POLYNOMIAL over GF(11):
  x^2 - x - 1 = 0 has roots phi_11 = 4 and phi_11' = 8
  Verification: 4^2 - 4 - 1 = 11 = 0 (mod 11)
                8^2 - 8 - 1 = 55 = 0 (mod 11)
  phi * phi' = 4 * 8 = 32 = 10 = -1 (mod 11)  [correct: phi*phi'=-1]
  phi + phi' = 4 + 8 = 12 = 1 (mod 11)         [correct: phi+phi'=1]

CHARACTER FIELD: Q(zeta_5, zeta_19)
  Irrationalities in character table:
    b5 = (-1 + sqrt(5))/2 = 1/phi  (golden ratio conjugate!)
    Appears in: 56-dim and 77-dim representations
    Also: 19th roots of unity in 120-dim representations

SELF-REFERENTIAL EQUATION: x^2 - x - 1 = 0 (mod 11)
  The SAME golden equation, reduced modulo 11.
  J1 lives where phi EXISTS natively in the prime field.

THE J1 "NOME": q = 4 or q = 8 in GF(11)
  Self-reference check: q + q^2 mod 11
    4 + 16 = 20 = 9 (mod 11)  -- NOT 1!
  But: q + q^2 = q(1+q) = 4*5 = 20 = 9 = -2 (mod 11)
  And: phi^2 = phi + 1, so phi + phi^2 = 2*phi + 1 = 2*4+1 = 9 (mod 11)
  The self-reference q+q^2 = 1 lifts to q+q^2 = 1 in Z[phi], which
  reduces to 9 = 1 (mod 11) -- FALSE because we need q=1/phi, not phi.

  Using q = 1/phi = 8 (since 4*8=32=10=-1, so 1/4=8*(-1)^{-1}...):
    Actually 1/phi = -1/phi' = phi - 1 = 4-1 = 3 (mod 11)
    Wait: phi*(phi-1) = phi^2 - phi = 1, so 1/phi = phi-1 = 3 (mod 11)
    Check: 3 + 3^2 = 3 + 9 = 12 = 1 (mod 11)  YES!

  q_J1 = 3 in GF(11), and q + q^2 = 1 (mod 11). SELF-REFERENCE HOLDS!

REMARKABLE: The nome q = 1/phi = phi - 1 = 3 in GF(11),
and q + q^2 = 1 is SATISFIED. J1 inherits the Monster's self-reference
but "compressed" into a finite field.

KEY DISCRIMINANT: disc(Q(zeta_5)) = 5^3 = 125
                  disc(Q(sqrt(5))) = 5
""")

# ============ J3 ============
subheader("J3 (Janko 3 / Higman-McKay)")
print("""
ORDER: 50,232,960 = 2^7 * 3^5 * 5 * 17 * 19
CHARACTERISTIC: 2  (9-dim rep of 3.J3 over GF(4), 18-dim over GF(9))
SCHUR MULTIPLIER: Z_3  (triple cover 3.J3 has key representations)
OUTER AUTOMORPHISM: Z_2

GOLDEN POLYNOMIAL over GF(2):
  x^2 - x - 1 becomes x^2 + x + 1 (mod 2)  [since -1 = 1 in char 2]
  This is Phi_3(x), the THIRD CYCLOTOMIC POLYNOMIAL!
  IRREDUCIBLE over GF(2), roots in GF(4).

GF(4) = GF(2)[w] where w^2 + w + 1 = 0:
  Elements: {0, 1, w, w^2 = w+1}
  w is simultaneously:
    - a primitive CUBE ROOT OF UNITY
    - the GOLDEN RATIO reduced mod 2

SELF-REFERENCE VERIFICATION:
  q = w in GF(4):  q + q^2 = w + w^2 = w + (w+1) = 1  (char 2!)
  q + q^2 = 1 is SATISFIED in GF(4).

PROFOUND FUSION: In characteristic 2, the golden equation x^2-x-1=0
BECOMES the cyclotomic equation x^2+x+1=0. The golden ratio and the
cube root of unity are THE SAME OBJECT. This is why J3 (and J4) live
at the intersection of golden and cyclotomic worlds.

J3 NATURAL EQUATION: x^2 + x + 1 = 0  (Phi_3, discriminant -3)

DISCRIMINANT COMPARISON:
  Monster: disc(x^2-x-1) = +5  (real quadratic, golden)
  J3:      disc(x^2+x+1) = -3  (imaginary quadratic, Eisenstein)

  Q(sqrt(5)) is the golden field (real, units are powers of phi)
  Q(sqrt(-3)) is the Eisenstein field (imaginary, units are 6th roots)

  In char 2, these MERGE: sqrt(5) = sqrt(-3) = 1 (mod 2)

PRIMES: {2, 3, 5, 17, 19}
  17 = Fermat prime F_2 = 2^(2^2) + 1
  19 appears in J1 too (shared with J1!)
""")

# ============ Ru ============
subheader("Ru (Rudvalis)")
print("""
ORDER: 145,926,144,000 = 2^14 * 3^3 * 5^3 * 7 * 13 * 29
CHARACTERISTIC: none specific (but key rep is over Gaussian integers Z[i])
SCHUR MULTIPLIER: Z_2  (double cover 2.Ru acts on lattice)
OUTER AUTOMORPHISM: trivial

NATURAL NUMBER FIELD: Q(i) = Q(sqrt(-1))
  Defining equation: x^2 + 1 = 0
  Ring of integers: Z[i] (Gaussian integers)
  Discriminant: -4
  Class number: 1 (unique factorization)
  Units: {1, i, -1, -i} = Z_4 (FINITE, unlike Z[phi])

28-DIMENSIONAL LATTICE:
  Double cover 2.Ru acts on a rank-28 lattice over Z[i]
  4 * 4060 = 16,240 minimal vectors
  Reducing mod (1+i) gives action over GF(2)

EMBEDDING IN E7:
  Ru embeds in E7(5) (algebraic group of type E7 over GF(5))
  E7 fundamental representation: 56-dim, decomposes as 28 + 28*
  The 28 of Ru IS the 28 of E7.
  E7 has 126 roots, Coxeter number 18, determinant of Cartan matrix = 2

Ru SELF-REFERENTIAL EQUATION: x^2 + 1 = 0
  Compare to Monster: x^2 - x - 1 = 0

DISCRIMINANT TABLE:
  Monster (golden): x^2 - x - 1 = 0, disc = +5
  Ru (Gaussian):    x^2     + 1 = 0, disc = -4
  J3 (Eisenstein):  x^2 + x + 1 = 0, disc = -3

These are the THREE simplest quadratic integer rings:
  Z[phi]  (disc +5, real, infinite units, Pisot)
  Z[i]    (disc -4, imaginary, 4 units)
  Z[w]    (disc -3, imaginary, 6 units)

The PARIAHS EXPLORE THE OTHER QUADRATIC RINGS that the Monster ignores.

PRIMES: {2, 3, 5, 7, 13, 29}
  13 = Fibonacci prime F_7
  29 = 4 + 5^2 (Gaussian norm of 2+5i)
""")

# ============ ON ============
subheader("ON (O'Nan)")
print("""
ORDER: 460,815,505,920 = 2^9 * 3^4 * 5 * 7^3 * 11 * 19 * 31
CHARACTERISTIC: 7  (45-dim rep of 3.ON over GF(7))
SCHUR MULTIPLIER: Z_3  (triple cover 3.ON has key reps)
OUTER AUTOMORPHISM: Z_2

GOLDEN POLYNOMIAL over GF(7):
  x^2 - x - 1 (mod 7): IRREDUCIBLE (5 is not QR mod 7)
  phi lives in GF(49) = GF(7^2), NOT in GF(7)

  The O'Nan group CANNOT SEE phi in its prime field.

O'NAN MOONSHINE (Duncan-Mertens-Ono 2017):
  Graded virtual ON-module: W = direct_sum W_n (n > 0, n = 0,3 mod 4)
  McKay-Thompson series: weight 3/2 mock modular forms
  Level: Gamma_0(4N) for element of order N

  Identity series: F_1 = -q^{-4} + 2 + 26752 q^3 + 143376 q^4 + ...

  Connected to elliptic curves:
    E_11: y^2 + y = x^3 - x^2 - 10x - 20     (conductor 11)
    E_15: y^2 + xy + y = x^3 + x^2 - 10x - 10 (conductor 15)
    E_19: (conductor 19)
    E_14: (conductor 14)

  Coefficients encode class numbers h(D) for Q(sqrt(D)), D < 0
  Congruences: for p | |ON|, character values related to:
    - class numbers
    - p-parts of Selmer groups
    - Tate-Shafarevich groups of elliptic curve twists

ON NATURAL EQUATION: The "equation" is not algebraic but MODULAR.
  ON lives in the world of weight 3/2, which is HALF-INTEGER weight.
  This is between the Monster (weight 0, j-function) and geometry.

  The natural "nome" for ON: tau in the upper half-plane H
  evaluated via Shimura correspondence (weight 3/2 -> weight 2)
  The key discriminants are negative: D < -4

  The 9 Heegner numbers (class number 1):
    -3, -4, -7, -8, -11, -19, -43, -67, -163

  Note: 11 and 19 are BOTH primes of ON AND Heegner discriminants!
  The conductors 11 and 19 of the key elliptic curves match.

ON SEES THE ARITHMETIC OF IMAGINARY QUADRATIC FIELDS.
  While Monster sees Q(sqrt(5)), O'Nan sees Q(sqrt(D)) for ALL D < 0.

PRIMES: {2, 3, 5, 7, 11, 19, 31}
  7 = characteristic (phi invisible)
  11 = Heegner, conductor
  19 = Heegner, conductor, shared with J1 and J3
  31 = Mersenne prime 2^5 - 1
""")

# ============ Ly ============
subheader("Ly (Lyons)")
print("""
ORDER: 51,765,179,004,000,000 = 2^8 * 3^7 * 5^6 * 7 * 11 * 31 * 37 * 67
CHARACTERISTIC: 5  (111-dim rep over GF(5), contains G_2(5))
SCHUR MULTIPLIER: trivial
OUTER AUTOMORPHISM: trivial

GOLDEN POLYNOMIAL over GF(5): ***DEGENERATE***
  x^2 - x - 1 (mod 5): discriminant = 5 = 0 (mod 5)
  DOUBLE ROOT: phi_5 = 3 (multiplicity 2)
  x^2 - x - 1 = (x - 3)^2 (mod 5)

  phi = -1/phi = 3 in GF(5)
  Verification: 3^2 - 3 - 1 = 5 = 0 (mod 5)
  And: -1/3 = -(1/3) = -(2) = -2 = 3 (mod 5)  [since 3*2=6=1]

THE TWO VACUA MERGE.
  In V(Phi) = (Phi^2 - Phi - 1)^2, the two minima at phi and -1/phi
  COLLAPSE to a single point at characteristic 5.
  No domain wall can exist. The kink is degenerate.

RAMIFICATION: 5 is the UNIQUE ramification prime of Q(sqrt(5))/Q.
  The prime ideal (5) = (sqrt(5))^2 in Z[phi].
  Ly lives at the SINGULAR FIBER of the golden family.

  This is like a cusp on a modular curve -- the special degenerate point.

G_2(5) as maximal subgroup:
  G_2 = automorphism group of the octonions
  G_2(5) = Chevalley group of type G_2 over GF(5)
  14-dimensional Lie algebra, 2 = rank

Ly NATURAL EQUATION: x^2 - x - 1 = 0 (mod 5), i.e., (x-3)^2 = 0
  This is the golden equation at its RAMIFICATION POINT.
  Not a new equation -- the golden equation in its most singular form.

  Self-ref: q = 3, q + q^2 = 3 + 9 = 12 = 2 (mod 5)
  NOT 1. The self-reference BREAKS at the ramification point.

Ly "NOME": q = 3 in GF(5), but self-reference fails.
  The "nome" is a double root, like trying to define 1/0.
  Ly lives where the golden self-reference DEGENERATES.

PRIMES: {2, 3, 5, 7, 11, 31, 37, 67}
  5 = ramification prime (!!!)
  67 = HEEGNER NUMBER (class number 1 for Q(sqrt(-67)))
  37 = irregular prime, |Ly| has 37 as factor
  31 = Mersenne prime, shared with ON
""")

# ============ J4 ============
subheader("J4 (Janko 4)")
print("""
ORDER: 86,775,571,046,077,562,880
     = 2^21 * 3^3 * 5 * 7 * 11^3 * 23 * 29 * 31 * 37 * 43
CHARACTERISTIC: 2  (112-dim rep over GF(2), binary Golay code)
SCHUR MULTIPLIER: trivial
OUTER AUTOMORPHISM: trivial

GOLDEN POLYNOMIAL over GF(2): IRREDUCIBLE (same as J3)
  x^2 - x - 1 = x^2 + x + 1 = Phi_3(x) (mod 2)
  Roots in GF(4), not in GF(2)

CRITICAL DIFFERENCE FROM J3:
  J3 extends to GF(4) for its key representation (9-dim of 3.J3)
  J4 stays in GF(2) for its key representation (112-dim)

  J4 REFUSES the extension to GF(4) where phi lives.
  It is the most "phi-averse" of all pariahs.

GOLAY CODE CONNECTION:
  J4 constructed via the extended binary Golay code C_24
  [24, 12, 8] code over GF(2)
  24 = Leech lattice dimension = c_Monster (!)
  12 = code dimension = number of fermions?
  8 = minimum distance

  J4 acts on 112 = dim of key representation
  112 = 4 * 28 (four copies of Ru's 28?)
  112 = 16 * 7 (or 2^4 * 7)

  Connection to M24 (Mathieu group, happy family member):
  J4 "borrows" from M24 via the Golay code but is NOT in the happy family.

J4 NATURAL EQUATION: x^2 + x + 1 = 0 (mod 2)
  Same as J3. But J4 refuses the solution by staying in GF(2).

  In GF(2), x^2 + x + 1 = 1 for x=0, and = 1 for x=1.
  NO SOLUTION EXISTS. The equation is a CONTRADICTION in GF(2).

  J4 lives in a field where self-reference is IMPOSSIBLE.
  It cannot solve q + q^2 = 1 in any form.

PRIMES: {2, 3, 5, 7, 11, 23, 29, 31, 37, 43}
  23 = dimension of binary Golay codeword - 1
  43 = HEEGNER NUMBER (class number 1 for Q(sqrt(-43)))
  11^3 divides |J4| (highest power of 11 in any sporadic group order)
  29 and 37 shared with other pariahs
""")

# ==========================================================================
header("SYNTHESIS: THE PARIAH EQUATIONS")
# ==========================================================================

print("""
SUMMARY TABLE OF SELF-REFERENTIAL EQUATIONS:
============================================

Group  | Equation         | Disc  | Field        | q+q^2=1? | Status
-------|------------------|-------|--------------|----------|--------
Monster| x^2-x-1=0       | +5    | Q(sqrt(5))   | YES      | Self-referential
J1     | x^2-x-1=0 mod11 | +5    | GF(11)       | YES      | Inherited (q=3)
J3     | x^2+x+1=0       | -3    | Q(sqrt(-3))  | YES*     | Golden=cyclotomic
Ru     | x^2+1=0          | -4    | Q(i)         | NO       | Orthogonal
ON     | (mock modular)    | var.  | Q(sqrt(D<0)) | N/A      | Arithmetic
Ly     | (x-3)^2=0 mod 5  | 0     | GF(5)        | NO       | Degenerate
J4     | x^2+x+1=0 mod 2  | -3    | GF(2)        | NEVER    | Impossible

* In GF(4): w + w^2 = 1 where w = cube root of unity = golden ratio mod 2

DISCRIMINANT PATTERN:
  Monster: +5  (real quadratic, unique Pisot)
  J3/J4:   -3  (Eisenstein integers, hexagonal lattice)
  Ru:       -4  (Gaussian integers, square lattice)
  ON:     {-D}  (ALL imaginary quadratic fields)
  Ly:        0  (ramification point of +5)

THE THREE FUNDAMENTAL QUADRATIC RINGS:
  Z[phi]  : disc +5   -> Monster (golden, infinite units, Pisot)
  Z[w]    : disc -3   -> J3, J4  (Eisenstein, 6 units, hexagonal)
  Z[i]    : disc -4   -> Ru      (Gaussian, 4 units, square)

And two degenerate cases:
  disc 0 (ramified) -> Ly (golden equation at its singular point)
  mock modular       -> ON (sees all negative discriminants at once)
""")

# ==========================================================================
header("DEEPER PATTERNS")
# ==========================================================================

print("""
1. THE GOLDEN EQUATION'S FATE:
   x^2 - x - 1 = 0 has three possible fates over a prime p:

   (a) SPLITS: p = 1, 4 (mod 5) -- phi exists, two roots
       -> J1 at p=11 (phi IS there, finite field version)

   (b) STAYS: p = 2, 3 (mod 5) -- phi needs extension, becomes cyclotomic
       -> J3, J4 at p=2 (golden = cyclotomic = Eisenstein)
       -> ON at p=7 (phi invisible, group uses mock modular instead)

   (c) DEGENERATES: p = 5 -- two vacua merge, ramification
       -> Ly at p=5 (the singular fiber of the golden family)

2. PARIAHS AS "SHADOWS" OF THE GOLDEN SELF-REFERENCE:
   The Monster embodies q + q^2 = 1 over Q (characteristic 0).
   Each pariah is what happens when you project this to a finite field:

   - J1: perfect projection (q=3 in GF(11) satisfies q+q^2=1)
   - J3: twisted projection (golden becomes cyclotomic in char 2)
   - Ru: orthogonal projection (Q(i) instead of Q(sqrt(5)))
   - ON: arithmetic shadow (sees all Q(sqrt(D)) through moonshine)
   - Ly: degenerate projection (ramification destroys the wall)
   - J4: impossible projection (no solution exists in GF(2))

3. WHY EXACTLY 6 PARIAHS?
   The golden polynomial x^2-x-1 has discriminant 5, a prime.
   Over the "landscape" of primes:
   - 1 splits (trivially, J1-type)
   - 1 ramifies (at p=5 itself, Ly-type)
   - 1 stays inert (various options: J3/J4, ON)
   - 1 orthogonal direction (Ru, Q(i))

   The 6 pariahs may correspond to the 6 WAYS the golden equation
   can fail to be what it is over Q.

4. SHARED PRIMES:
   19 appears in J1, J3, AND ON (3 of 6 pariahs!)
   31 appears in ON and Ly
   37 appears in Ly and J4
   29 appears in Ru and J4

   The Heegner numbers in pariah orders:
     43 in J4,  67 in Ly
   These are class-number-1 discriminants -- the "exceptional"
   imaginary quadratic fields with unique factorization.

5. THE HIERARCHY OF SELF-REFERENCE:
   Monster:  q + q^2 = 1  (full self-reference, infinite field)
   J1:       q + q^2 = 1  (mod 11) (finite self-reference)
   J3/GF(4): w + w^2 = 1  (golden = cyclotomic fusion)
   Ly:       3 + 9 = 2    (mod 5) (broken self-reference)
   Ru:       orthogonal    (different equation entirely)
   J4/GF(2): impossible    (no self-reference at all)
   ON:       mock modular  (self-reference through arithmetic)
""")

# ==========================================================================
header("O'NAN MOONSHINE DETAILS (Duncan-Mertens-Ono 2017)")
# ==========================================================================

print("""
The most mathematically developed pariah moonshine.

STRUCTURE:
  Graded virtual ON-module W = direct_sum_{n>0, n=0,3(mod 4)} W_n
  Identity McKay-Thompson series:
    F_1(tau) = -q^{-4} + 2 + 26752 q^3 + 143376 q^4 + 8288256 q^7 + ...
  where q = e^{2*pi*i*tau}

  26752 = dim(chi_7)  (7th irrep of ON)
  143376 = 1 + 58311 + 85064  (decomposition into irreps)

ELLIPTIC CURVES:
  E_11: y^2 + y = x^3 - x^2 - 10x - 20       (X_0(11), conductor 11)
  E_15: y^2 + xy + y = x^3 + x^2 - 10x - 10   (conductor 15)

  For fundamental discriminants d < -4, (d/11) != 0:
    dim(W_{|d|}) relates to class number h(d) modulo 11
    and to Selmer/Tate-Shafarevich groups of E_11^{(d)}

WEIGHT 3/2:
  This is HALF-INTEGER weight -- between the Monster's weight 0 (j-function)
  and the weight 2 of elliptic curve newforms.

  Weight 3/2 forms connect to:
  - Shimura correspondence -> weight 2
  - Class numbers via Cohen-Zagier
  - Half-integral weight = spinor-like (covering group needed)

  The "O'Nan nome" is not a fixed algebraic number like q=1/phi.
  Instead, ON's moonshine is ARITHMETIC: it ranges over all negative
  discriminants, encoding class numbers and BSD data.

  If Monster moonshine asks "what is j(1/phi)?",
  O'Nan moonshine asks "what are L(E_d, 1) for all quadratic twists?"
""")

# ==========================================================================
header("CANDIDATE 'PARIAH NOMES'")
# ==========================================================================

print("""
By analogy with q = 1/phi for the Monster:

J1:  q_J1 = 3 in GF(11)
     (This is 1/phi mod 11: phi=4, 1/4=-1*8/(-1)...
      phi-1=3, and phi*(phi-1)=phi^2-phi=1, so 1/phi=phi-1=3)
     q + q^2 = 3 + 9 = 12 = 1 (mod 11)  WORKS!

J3:  q_J3 = w in GF(4)  (primitive cube root of unity)
     q + q^2 = w + w^2 = 1 (in characteristic 2)  WORKS!

Ru:  q_Ru = ???  (no obvious analog; the natural number is i)
     The "nome" might be related to the Gaussian prime 1+i
     which satisfies (1+i)^2 = 2i, and |1+i|^2 = 2.

ON:  q_ON: no fixed nome; the moonshine ranges over all tau in H
     Natural points: tau = sqrt(-D)/2 for Heegner discriminants D
     Most natural: tau_11 = (1+sqrt(-11))/2 (conductor 11 CM point)

Ly:  q_Ly = 3 in GF(5) (degenerate double root)
     q + q^2 = 2 (mod 5)  -- FAILS (broken self-reference)
     Alternative: the cusp of x^2-x-1=0 at p=5, like a node on a curve.

J4:  q_J4 = NONE (no solution to x^2+x+1=0 in GF(2))
     J4 is the pariah with NO NOME at all.
     It lives in the field where self-reference cannot be expressed.
""")

print()
print("=" * 80)
print("END OF ANALYSIS")
print("=" * 80)
