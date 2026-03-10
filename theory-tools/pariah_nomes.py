#!/usr/bin/env python3
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
"""
pariah_nomes.py — Self-reference equation q + q² = 1 over finite fields
=========================================================================

The golden ratio equation x² - x - 1 = 0 defines the Monster's physics.
The 6 pariah sporadic groups live OUTSIDE the Monster. What happens when
we push q + q² = 1 into their characteristic fields?

Each pariah group has a "natural" finite field (its smallest faithful
representation, or the field of its modular moonshine). We solve
x² - x - 1 = 0 in each and see what breaks.

Result: a hierarchy of self-reference capacity.
  - Monster (char 0, Z[phi]): full self-reference, physics
  - J1 (GF(11)): self-reference works, but modular forms collapse
  - J3 (GF(4)): phi = omega (golden = triality), fusion
  - Ly (GF(5)): two vacua collapse, ramification, no domain wall
  - Ru (Z[i]): wrong quadratic ring, no solution
  - J4 (GF(2)): self-reference impossible
  - O'N: moonshine elliptic curves with Lucas conductors

Standard Python only. No dependencies.
"""

import math

# ============================================================
# Utility functions
# ============================================================

def mod_inv(a, p):
    """Modular inverse of a mod p using extended Euclidean algorithm."""
    if a % p == 0:
        return None
    g, x, _ = extended_gcd(a % p, p)
    if g != 1:
        return None
    return x % p

def extended_gcd(a, b):
    """Extended Euclidean algorithm. Returns (gcd, x, y) with a*x + b*y = gcd."""
    if a == 0:
        return b, 0, 1
    g, x1, y1 = extended_gcd(b % a, a)
    return g, y1 - (b // a) * x1, x1

def solve_quadratic_mod_p(a, b, c, p):
    """
    Solve ax² + bx + c ≡ 0 (mod p) by brute force.
    Returns list of solutions in {0, 1, ..., p-1}.
    """
    solutions = []
    for x in range(p):
        if (a * x * x + b * x + c) % p == 0:
            solutions.append(x)
    return solutions

def fibonacci_mod(n, m):
    """Compute F(n) mod m."""
    if n <= 0:
        return 0
    a, b = 0, 1
    for _ in range(n - 1):
        a, b = b, (a + b) % m
    return b

def pisano_period(m):
    """Compute the Pisano period pi(m) = period of Fibonacci sequence mod m."""
    if m <= 1:
        return 1
    a, b = 0, 1
    for i in range(1, 6 * m + 1):  # pi(m) <= 6m
        a, b = b, (a + b) % m
        if a == 0 and b == 1:
            return i
    return -1  # should not happen

def lucas_number(n):
    """Compute L(n), the nth Lucas number. L(0)=2, L(1)=1."""
    if n == 0:
        return 2
    if n == 1:
        return 1
    a, b = 2, 1
    for _ in range(n - 1):
        a, b = b, a + b
    return b

def fib(n):
    """Compute F(n), the nth Fibonacci number. F(0)=0, F(1)=1."""
    if n <= 0:
        return 0
    if n == 1:
        return 1
    a, b = 0, 1
    for _ in range(n - 1):
        a, b = b, a + b
    return b

# Framework constants (for reference)
PHI = (1 + math.sqrt(5)) / 2
Q_GOLD = 1.0 / PHI  # q = 1/phi satisfies q + q^2 = 1

print("=" * 72)
print("PARIAH NOMES: Self-Reference Equation q + q² = 1 Over Finite Fields")
print("=" * 72)
print()
print(f"Over Q: phi = {PHI:.10f}, q = 1/phi = {Q_GOLD:.10f}")
print(f"Check: q + q² = {Q_GOLD + Q_GOLD**2:.15f}")
print()


# ============================================================
# 1. GF(11) — J₁ nome verification
# ============================================================

print("=" * 72)
print("§1. GF(11) — Janko group J₁")
print("=" * 72)
print()
print("|J₁| = 175,560 = 2³ · 3 · 5 · 7 · 11 · 19")
print("Smallest faithful representation: 7-dimensional over GF(11)")
print()

p = 11
print(f"Solving x² - x - 1 ≡ 0 (mod {p}):")
print(f"  i.e. x² + {p-1}x + {p-1} ≡ 0 (mod {p})")
sols = solve_quadratic_mod_p(1, -1, -1, p)
print(f"  Solutions: {sols}")

# Verify phi and phi'
phi_11 = sols[0] if len(sols) >= 1 else None
phi_prime_11 = sols[1] if len(sols) >= 2 else None
print()
if phi_11 is not None:
    print(f"  φ₁₁ = {phi_11}")
    print(f"    Check: {phi_11}² - {phi_11} - 1 = {phi_11**2 - phi_11 - 1} ≡ {(phi_11**2 - phi_11 - 1) % p} (mod {p})")
if phi_prime_11 is not None:
    print(f"  φ'₁₁ = {phi_prime_11}")
    print(f"    Check: {phi_prime_11}² - {phi_prime_11} - 1 = {phi_prime_11**2 - phi_prime_11 - 1} ≡ {(phi_prime_11**2 - phi_prime_11 - 1) % p} (mod {p})")

print()
print("Now solving q + q² ≡ 1 (mod 11), i.e. q² + q - 1 ≡ 0 (mod 11):")
q_sols = solve_quadratic_mod_p(1, 1, -1, p)
print(f"  Solutions: {q_sols}")
for q in q_sols:
    val = (q + q * q) % p
    print(f"    q = {q}: q + q² = {q + q*q} ≡ {val} (mod {p})  {'✓' if val == 1 else '✗'}")

print()
print("Note: q = 1/φ in GF(11).")
if phi_11 is not None:
    inv_phi_11 = mod_inv(phi_11, p)
    print(f"  1/φ₁₁ = 1/{phi_11} ≡ {inv_phi_11} (mod {p})")
    if inv_phi_11 in q_sols:
        print(f"  Confirmed: 1/φ₁₁ = {inv_phi_11} is a solution of q + q² ≡ 1")

# Truncated modular forms mod 11
print()
print("Truncated Dedekind eta product mod 11:")
print("  η(q) = q^(1/24) · Π(1 - q^n) — infinite product, but mod 11 we")
print("  can only compute partial products since q^n cycles.")
print()

# Compute q^n mod 11 for q=3
q_11 = q_sols[0] if q_sols else 3
print(f"  Powers of q={q_11} mod {p}:")
qn = 1
powers = []
for n in range(12):
    powers.append(qn)
    print(f"    q^{n} ≡ {qn} (mod {p})")
    qn = (qn * q_11) % p
# Find the cycle
cycle_len = None
for i in range(1, len(powers)):
    if powers[i] == 1:
        cycle_len = i
        break
if cycle_len:
    print(f"  Order of q={q_11} in GF({p})* is {cycle_len}")
    print(f"  (Compare: |GF({p})*| = {p-1})")

# Partial eta: product of (1 - q^n) for n=1..cycle
print()
print(f"  Partial η-product (1-q)(1-q²)...(1-q^{cycle_len or 10}) mod {p}:")
eta_partial = 1
for n in range(1, (cycle_len or 10) + 1):
    qn_val = pow(q_11, n, p)
    factor = (1 - qn_val) % p
    eta_partial = (eta_partial * factor) % p
    print(f"    n={n}: (1 - q^{n}) = (1 - {qn_val}) ≡ {factor}, running product ≡ {eta_partial}")

print(f"\n  η_partial(q={q_11}) ≡ {eta_partial} (mod {p})")

# Coupling residues
print()
print("Coupling residues mod 11:")
print(f"  α_s = η(1/φ) = 0.11840...  In framework: η ≡ {eta_partial} (mod {p})")
# sin^2 theta_W ~ eta^2 / (2*theta4)
eta_sq = (eta_partial * eta_partial) % p
inv2 = mod_inv(2, p)
print(f"  η² ≡ {eta_sq} (mod {p})")
print(f"  1/2 ≡ {inv2} (mod {p})")
print(f"  η²/2 ≡ {(eta_sq * inv2) % p} (mod {p})")
print()
print("  Interpretation: modular forms are well-defined mod 11, but the")
print("  infinite product truncates to a FINITE group element. The rich")
print("  perturbative structure (VP corrections, Fibonacci collapse) is lost.")
print("  J₁ sees self-reference, but not physics.")


# ============================================================
# 2. GF(4) — J₃ golden-cyclotomic fusion
# ============================================================

print()
print("=" * 72)
print("§2. GF(4) — Janko group J₃ (Higman-Janko-McKay)")
print("=" * 72)
print()
print("|J₃| = 50,232,960 = 2⁷ · 3⁵ · 5 · 17 · 19")
print("Smallest faithful representation: 9-dimensional over GF(4)")
print()

print("In characteristic 2, -1 ≡ 1, so:")
print("  x² - x - 1  ≡  x² + x + 1  (mod 2)")
print()
print("But x² + x + 1 = Φ₃(x), the 3rd cyclotomic polynomial!")
print("Its roots are the primitive cube roots of unity ω, ω².")
print()

# Verify in GF(2)
print("Over GF(2) = {0, 1}:")
for x in [0, 1]:
    val = (x * x + x + 1) % 2
    print(f"  x={x}: x²+x+1 = {x*x+x+1} ≡ {val} (mod 2)  {'= 0 ✓' if val == 0 else '≠ 0'}")

print()
print("No solutions in GF(2). Must extend to GF(4) = GF(2)[ω]/(ω²+ω+1).")
print()
print("GF(4) has elements: {0, 1, ω, ω²} where ω² + ω + 1 = 0, i.e. ω² = ω + 1.")
print()
print("Verify: ω + ω² = ω + (ω + 1) = 2ω + 1 = 0 + 1 = 1  (since 2≡0 in char 2)")
print()
print("So in GF(4): ω + ω² = 1  ←→  q + q² = 1")
print()
print("THE GOLDEN RATIO EQUATION AND THE CUBE ROOT OF UNITY EQUATION")
print("ARE THE SAME EQUATION IN CHARACTERISTIC 2.")
print()
print("φ = ω: structure (golden self-reference) and triality (cube root)")
print("        are the SAME OBJECT in J₃'s natural field.")
print()

# Arithmetic in GF(4)
print("GF(4) multiplication table (for reference):")
print("    ·  | 0   1   ω   ω²")
print("  -----+----------------")
print("    0  | 0   0   0   0")
print("    1  | 0   1   ω   ω²")
print("    ω  | 0   ω   ω²  1")
print("    ω² | 0   ω²  1   ω")
print()
print("This is Z₃ (the multiplicative group GF(4)* ≅ Z₃).")
print("Triality IS the multiplicative structure of the golden field in char 2.")
print()
print("Implications:")
print("  - The 3 in 'triality' and the 3 in 'three generations' and the 3")
print("    in 'three couplings' and the golden ratio are ALL THE SAME THING")
print("    when viewed from J₃'s perspective.")
print("  - J₃ is the pariah that comes closest to Monster physics:")
print("    it sees the fusion of φ and ω, which the Monster keeps separate.")


# ============================================================
# 3. GF(5) — Lyons group degeneration
# ============================================================

print()
print("=" * 72)
print("§3. GF(5) — Lyons group Ly")
print("=" * 72)
print()
print("|Ly| = 51,765,179,004,000,000 = 2⁸ · 3⁷ · 5⁶ · 7 · 11 · 31 · 37 · 67")
print("Smallest faithful representation: 111-dimensional over GF(5)")
print()

p = 5
print(f"Solving x² - x - 1 ≡ 0 (mod {p}):")
sols = solve_quadratic_mod_p(1, -1, -1, p)
print(f"  Solutions: {sols}")
print()

# Check discriminant
disc = ((-1)**2 - 4 * 1 * (-1)) % p  # b² - 4ac = 1 + 4 = 5
print(f"Discriminant = 1 + 4 = 5 ≡ {5 % p} (mod {p})  ← ZERO!")
print("This is RAMIFICATION. The two roots collide.")
print()

# The double root
# x = (1 ± 0) / 2 = 1/2 mod 5 = 3
inv2_5 = mod_inv(2, 5)
double_root = (1 * inv2_5) % 5
print(f"Double root: x = 1/(2) ≡ 1·{inv2_5} ≡ {double_root} (mod {p})")
print(f"Check: x² - x - 1 = {double_root**2} - {double_root} - 1 = {double_root**2 - double_root - 1} ≡ {(double_root**2 - double_root - 1) % p} (mod {p})")
print()

# Factor
print(f"Factorization: x² - x - 1 ≡ (x - {double_root})² (mod {p})")
# verify (x-3)^2 = x^2 - 6x + 9 = x^2 - x - 1 mod 5?
# x^2 - 6x + 9 mod 5 = x^2 - x + 4 = x^2 + 4x + 4 mod 5
# Hmm, let's be more careful
print("  Verify: (x - 3)² = x² - 6x + 9 ≡ x² - x + 4 ≡ x² + 4x + 4 (mod 5)")
# x^2 - x - 1 mod 5 = x^2 + 4x + 4 mod 5. Check: -1 mod 5 = 4, -1 mod 5 = 4. Yes!
print("  And:    x² - x - 1 ≡ x² + 4x + 4 (mod 5)")
print("  These are the same! ✓")
print()

print("Physical meaning:")
print(f"  φ ≡ {double_root} (mod 5)")
print(f"  -1/φ ≡ {(-mod_inv(double_root, p)) % p} (mod 5)")
inv_dr = mod_inv(double_root, p)
neg_inv = (-inv_dr) % p
print(f"    (1/3 ≡ {inv_dr}, so -1/3 ≡ {neg_inv} mod 5)")
print(f"  THE TWO VACUA COLLIDE: φ ≡ -1/φ ≡ {double_root} (mod 5)")
print()

# V(Phi) mod 5
print("Potential V(Φ) = (Φ² - Φ - 1)² mod 5:")
print("  Φ  | Φ²-Φ-1 (mod 5) | V(Φ) (mod 5)")
print("  ---+-----------------+--------------")
for phi_val in range(p):
    inner = (phi_val**2 - phi_val - 1) % p
    v_val = (inner * inner) % p
    mark = " ← DOUBLE ZERO" if v_val == 0 else ""
    print(f"  {phi_val}  |       {inner}         |      {v_val}{mark}")

print()
print("V(3) = 0 but it's a DOUBLE zero (multiplicity 4 in the polynomial).")
print("There is no domain wall because both vacua are the same point.")
print()

# Self-reference test
print("Self-reference test: q + q² ≡ 1 (mod 5)?")
q_sols_5 = solve_quadratic_mod_p(1, 1, -1, p)
print(f"  Solving q² + q - 1 ≡ 0 (mod 5): solutions = {q_sols_5}")
for q in range(p):
    val = (q + q * q) % p
    mark = " ← !!!" if val == 1 else ""
    print(f"    q = {q}: q + q² = {q + q*q} ≡ {val} (mod 5){mark}")

print()
if not q_sols_5:
    print("  Wait — q + q² = 1 DOES have solutions mod 5 (same double root).")
    # q^2 + q - 1 = 0 mod 5. disc = 1+4 = 5 = 0 mod 5. Double root at q = -1/2 = 2 mod 5.
    q_root = (-1 * inv2_5) % p
    print(f"  Double root at q = -1/2 ≡ {q_root} (mod 5)")
    val = (q_root + q_root * q_root) % p
    print(f"  Check: {q_root} + {q_root}² = {q_root + q_root**2} ≡ {val} (mod 5)  {'✓' if val == 1 else '✗'}")
else:
    for q in q_sols_5:
        print(f"  q = {q}: self-reference equation satisfied (degenerate)")

print()
print("ANALYSIS: The equation q + q² = 1 is 'satisfied' mod 5 only in a")
print("degenerate way — both roots coincide, meaning there is no distinct")
print("q vs q² (no asymmetry). The Pisot property (one root > 1, conjugate")
print("< 1) that forces the arrow of time does not exist. The Lyons group")
print("lives in a timeless, wall-less landscape.")


# ============================================================
# 4. GF(2) — J₄ impossibility
# ============================================================

print()
print("=" * 72)
print("§4. GF(2) — Janko group J₄")
print("=" * 72)
print()
print("|J₄| = 86,775,571,046,077,562,880")
print("    = 2²¹ · 3³ · 5 · 7 · 11³ · 23 · 29 · 31 · 37 · 43")
print("Smallest faithful representation: 112-dimensional over GF(2)")
print()

p = 2
print(f"Solving x² - x - 1 ≡ 0 (mod {p}):")
print(f"  In char 2: x² - x - 1 ≡ x² + x + 1 (mod 2)")
print()
for x in [0, 1]:
    val = (x * x + x + 1) % 2
    print(f"  x = {x}: x² + x + 1 = {x*x + x + 1} ≡ {val} (mod 2)  {'✓' if val == 0 else '✗'}")

print()
print("NO SOLUTIONS in GF(2). The polynomial x² + x + 1 is irreducible over GF(2).")
print()
print("Self-reference test: q + q² ≡ 1 (mod 2)?")
for q in [0, 1]:
    val = (q + q * q) % 2
    print(f"  q = {q}: q + q² = {q + q*q} ≡ {val} (mod 2)  {'✓' if val == 1 else '✗'}")

print()
print("  q = 0: 0 + 0 = 0 ≠ 1")
print("  q = 1: 1 + 1 = 0 ≠ 1  (since 2 ≡ 0)")
print()
print("Self-reference is IMPOSSIBLE in GF(2).")
print("In characteristic 2, q + q² = q(1 + q) = q · (1 ⊕ q),")
print("and for this to equal 1, we'd need both q and 1⊕q nonzero,")
print("but q=1 gives 1·0 = 0. The XOR structure of GF(2) prevents")
print("any element from being its own complement in the required way.")
print()
print("J₄ lives in the field where self-reference is structurally forbidden.")
print("It is the most alien of the pariahs.")


# ============================================================
# 5. Z[i] — Rudvalis group's ring
# ============================================================

print()
print("=" * 72)
print("§5. Z[i] — Rudvalis group Ru")
print("=" * 72)
print()
print("|Ru| = 145,926,144,000 = 2¹⁴ · 3³ · 5³ · 7 · 13 · 29")
print("Ru has a 28-dimensional representation over Z[i] (Gaussian integers)")
print("(the Conway-Wales representation)")
print()

print("The Gaussian integers Z[i] are the ring of integers of Q(√(-1)).")
print("Discriminant: -4")
print()
print("Can q + q² = 1 be solved in Z[i]?")
print()
print("  q² + q - 1 = 0  →  q = (-1 ± √5) / 2")
print()
print("Need: is √5 in Q(i)?")
print("  Q(i) = Q(√(-1)). Contains √(-1) = i.")
print("  √5 would require Q(√5), a DIFFERENT quadratic extension.")
print("  Q(i) ∩ Q(√5) = Q (they share only rationals).")
print()

# Check: is 5 a square in Z[i]?
print("Is 5 a square in Z[i]?")
print("  5 = (2 + i)(2 - i) in Z[i]  (Gaussian prime factorization)")
print("  For 5 = z² we'd need z = a + bi with a² - b² = 5, 2ab = 0.")
print("  2ab = 0 → a = 0 or b = 0.")
print("  a = 0: -b² = 5 → impossible (negative).")
print("  b = 0: a² = 5 → a = √5 ∉ Z.")
print("  Therefore 5 is NOT a square in Z[i]. ✓")
print()
print("  q + q² = 1 has NO solutions in Z[i].")
print()

# Connection between Z[i] and Z[phi]?
print("Connection between Z[i] and Z[φ]?")
print("  Z[φ] = Z[(1+√5)/2], ring of integers of Q(√5), discriminant +5")
print("  Z[i] = Z[√(-1)], ring of integers of Q(√(-1)), discriminant -4")
print()
print("  These are fundamentally different quadratic rings:")
print("  - Z[φ] is REAL (both embeddings into R)")
print("  - Z[i] is IMAGINARY (one embedding, conjugate pair into C)")
print("  - Z[φ] has Pisot unit φ (crucial for arrow of time)")
print("  - Z[i] has unit group {±1, ±i} (finite, cyclic of order 4)")
print()
print("  The Rudvalis group's Gaussian structure is orthogonal to golden")
print("  structure. It can see squares and rotations (i⁴ = 1) but not")
print("  self-similar growth (φⁿ = F(n)φ + F(n-1)).")
print()
print("  Compositum Q(i, √5) = Q(i, φ) is a degree-4 extension of Q,")
print("  which is the splitting field of x⁴ + x² - 1 = (x²-x-1)(x²+x-1)")
print("  evaluated at ix. Both structures coexist there, but neither")
print("  pariah nor Monster naturally lives in this larger ring.")


# ============================================================
# 6. Summary table
# ============================================================

print()
print("=" * 72)
print("§6. Summary: Self-Reference Capacity of Sporadic Groups")
print("=" * 72)
print()

header = f"{'Group':<10} {'Order (approx)':<18} {'Field':<10} {'q+q²=1?':<14} {'Status':<28}"
print(header)
print("-" * len(header))

table = [
    ("Monster",  "8.08 × 10⁵³",  "char 0",    "φ, -1/φ",      "FULL: physics, time, walls"),
    ("Baby M",   "4.15 × 10³³",  "char 0",    "(inherited)",   "Inside Monster"),
    ("  ...",     "",              "",          "",              "(19 more happy family)"),
    ("─" * 8,    "─" * 14,       "─" * 8,     "─" * 12,        "─" * 26),
    ("J₁",       "1.76 × 10⁵",   "GF(11)",    "q=3, q=7",     "TRUNCATED: no perturbation"),
    ("J₃",       "5.02 × 10⁷",   "GF(4)",     "q=ω (cube rt)", "FUSED: φ = ω (golden=triality)"),
    ("Ly",       "5.18 × 10¹⁶",  "GF(5)",     "DEGENERATE",   "COLLAPSED: 2 vacua = 1"),
    ("Ru",       "1.46 × 10¹¹",  "Z[i]",      "NO",           "ORTHOGONAL: wrong ring"),
    ("O'N",      "4.61 × 10⁸",   "(special)",  "(moonshine)",  "ELLIPTIC: conductors 11,14,15,19"),
    ("J₄",       "8.68 × 10¹⁹",  "GF(2)",     "IMPOSSIBLE",   "FORBIDDEN: XOR kills self-ref"),
]

for row in table:
    print(f"{row[0]:<10} {row[1]:<18} {row[2]:<10} {row[3]:<14} {row[4]:<28}")


# ============================================================
# 7. The three fundamental quadratic rings
# ============================================================

print()
print("=" * 72)
print("§7. The Three Fundamental Quadratic Rings")
print("=" * 72)
print()

print("Every quadratic integer ring Z[√d] with class number 1 and small |d|")
print("falls into one of three families. The pariahs explore all three.")
print()

rings = [
    ("Z[φ]",   "+5",  "Real",       "φ (infinite, Pisot)", "Monster (physics)",
     "Self-similar growth, Fibonacci, domain walls, arrow of time"),
    ("Z[ω]",   "-3",  "Eisenstein", "{±1, ±ω, ±ω²} (Z₆)", "J₃, J₄ (triality)",
     "Hexagonal symmetry, cube roots of unity, equilateral geometry"),
    ("Z[i]",   "-4",  "Gaussian",   "{±1, ±i} (Z₄)",       "Ru (rotation)",
     "Square symmetry, quarter-turns, orthogonal structure"),
]

header2 = f"{'Ring':<8} {'Disc':<6} {'Type':<12} {'Unit group':<24} {'Pariah':<22} {'Structure'}"
print(header2)
print("-" * 110)
for r in rings:
    print(f"{r[0]:<8} {r[1]:<6} {r[2]:<12} {r[3]:<24} {r[4]:<22} {r[5]}")

print()
print("Key insight: these three rings have discriminants 5, -3, -4.")
print(f"  |5| + |-3| + |-4| = 12 = number of fermions")
print(f"  |5| × |-3| × |-4| = 60 = |A₅| = |icosahedral group|")
print(f"  (5, 3, 4) is a Pythagorean-adjacent triple: 3² + 4² = 5²")
print()
print("The three quadratic rings are related by 3² + 4² = 5².")
print("Physics (disc 5) contains the Pythagorean sum of rotation (disc 4)")
print("and triality (disc 3).")


# ============================================================
# 8. O'Nan moonshine connection
# ============================================================

print()
print("=" * 72)
print("§8. O'Nan Moonshine — Elliptic Curve Conductors")
print("=" * 72)
print()

print("|O'N| = 460,815,505,920 = 2⁹ · 3⁴ · 5 · 7³ · 11 · 19 · 31")
print()
print("O'Nan moonshine (Duncan-Mertens-Ono 2017) connects O'N to")
print("weight 3/2 mock modular forms and elliptic curves of conductors:")
print()

conductors = [11, 14, 15, 19]
print("Conductor | Factorization | Framework connection")
print("----------+---------------+------------------------------------------")

connections = {
    11: "L(5) = 11 (5th Lucas number, sunspot period ~11 yr)",
    14: "2 × 7 = 2 × L(4). Also: 14 = dim of G₂ adjoint rep",
    15: "3 × 5 = 3 × F(5). Also: 15 = dim of B₂ = SO(5) adjoint",
    19: "Prime. Divides |J₁|, |O'N|, |J₃|. Pisano period π(19) = 18",
}

for c in conductors:
    # Factorize
    n = c
    factors = []
    for d in range(2, n + 1):
        while n % d == 0:
            factors.append(d)
            n //= d
    fact_str = " × ".join(str(f) for f in factors) if len(factors) > 1 else str(c) + " (prime)"
    print(f"    {c:>4}  | {fact_str:<13} | {connections[c]}")

print()
print("Lucas/Fibonacci content of conductors:")
print(f"  L(1)=1, L(2)=3, L(3)=4, L(4)=7, L(5)=11, L(6)=18, L(7)=29")
print(f"  F(1)=1, F(2)=1, F(3)=2, F(4)=3, F(5)=5, F(6)=8, F(7)=13")
print()

# Check if 19 relates to framework
print("Is 19 special in the framework?")
print(f"  19 is prime")
print(f"  19 = 20 - 1 = s/d mass ratio - 1")
print(f"  19 divides |J₁| = 2³·3·5·7·11·19")
print(f"  19 divides |O'N| = 2⁹·3⁴·5·7³·11·19·31")
print(f"  19 divides |J₃| = 2⁷·3⁵·5·17·19")
print(f"  So 19 links THREE pariah groups (J₁, J₃, O'N).")
print(f"  Pisano period π(19) = {pisano_period(19)}")
print(f"  Note: 18 = L(6) = 3 × 6. And 19 - 1 = 18.")
print(f"  Fermat's little theorem: φ^18 ≡ 1 (mod 19) — golden ratio")
print(f"  has order dividing 18 in GF(19).")
print()

# Verify
sols_19 = solve_quadratic_mod_p(1, -1, -1, 19)
print(f"  x² - x - 1 ≡ 0 (mod 19): solutions = {sols_19}")
for s in sols_19:
    # Find order
    val = s
    for k in range(1, 20):
        if val == 1:
            print(f"    φ₁₉ = {s} has multiplicative order {k} in GF(19)*")
            break
        val = (val * s) % 19


# ============================================================
# 9. Fibonacci at pariah primes — Pisano periods
# ============================================================

print()
print("=" * 72)
print("§9. Fibonacci at Pariah Primes — Pisano Periods")
print("=" * 72)
print()

print("The Pisano period π(p) is the period of the Fibonacci sequence mod p.")
print("It measures how 'far' GF(p) is from seeing the full golden structure.")
print()

pariah_primes = [2, 5, 7, 11, 13, 19, 23, 29, 31, 37, 43]
# Labels for which pariah uses which prime
prime_labels = {
    2:  "J₄ (char), J₃ (char 2²)",
    5:  "Ly (disc = 0)",
    7:  "J₁, Ly, O'N",
    11: "J₁, J₄, O'N",
    13: "Ru",
    19: "J₁, J₃, O'N",
    23: "J₄",
    29: "Ru, J₄",
    31: "O'N, Ly, J₄",
    37: "Ly, J₄",
    43: "J₄",
}

print(f"{'Prime p':<10} {'π(p)':<8} {'π(p)/p-1':<12} {'F(p) mod p':<12} {'Pariah connection'}")
print("-" * 75)

for p in pariah_primes:
    pi_p = pisano_period(p)
    fp = fibonacci_mod(p, p)
    ratio = pi_p / (p - 1) if p > 1 else 0
    label = prime_labels.get(p, "")
    print(f"  {p:<8} {pi_p:<8} {ratio:<12.4f} {fp:<12} {label}")

print()
print("Observations:")
print(f"  π(5) = 20 is anomalously large (ratio 5.0). This is because")
print(f"  5 = disc(Z[φ]) — the Fibonacci sequence takes 20 steps to")
print(f"  return to (0,1) mod 5, reflecting the ramification.")
print()
print(f"  π(11) = 10 = |GF(11)*|. The Fibonacci sequence has FULL period")
print(f"  in GF(11). This means J₁ sees the complete Fibonacci structure.")
print()

# Wall's conjecture connection
print("Wall's conjecture: π(p) | p² - 1 for all primes p.")
print("For Fibonacci primes (p | F(p) ± 1), π(p) | p ± 1.")
print()
for p in pariah_primes:
    pi_p = pisano_period(p)
    divides_p_minus_1 = (p - 1) % pi_p == 0
    divides_p_plus_1 = (p + 1) % pi_p == 0
    divides_p2_minus_1 = ((p * p - 1) % pi_p == 0)
    which = []
    if divides_p_minus_1:
        which.append(f"p-1={p-1}")
    if divides_p_plus_1:
        which.append(f"p+1={p+1}")
    print(f"  p={p:>2}: π(p)={pi_p:>3}, divides {', '.join(which) if which else f'p²-1={p*p-1}'}")


# ============================================================
# 10. Grand summary
# ============================================================

print()
print("=" * 72)
print("§10. GRAND SUMMARY: Hierarchy of Self-Reference")
print("=" * 72)
print()

print("""
The equation q + q² = 1 encodes self-reference: the thing (q) and its
self-interaction (q²) together make unity (1). Over different algebraic
structures, this equation reveals a hierarchy:

LEVEL 5 — FULL PHYSICS (Monster, char 0, Z[φ])
  q = 1/φ = 0.6180339887...
  Two distinct vacua (φ and -1/φ), domain wall between them.
  Pisot property → arrow of time. Fibonacci → memory.
  Modular forms → all coupling constants.
  Result: the physical universe.

LEVEL 4 — TRUNCATED (J₁, GF(11))
  q = 3 or 7 (mod 11). Self-reference works.
  But modular forms truncate to finite products.
  No perturbative expansion, no VP corrections.
  Result: self-reference without fine structure.

LEVEL 3 — FUSED (J₃, GF(4))
  q = ω (cube root of unity). Golden = cyclotomic.
  φ and triality are the SAME object.
  No distinction between structure and generation.
  Result: self-reference without differentiation.

LEVEL 2 — DEGENERATE (Ly, GF(5))
  q = 2 (double root). Two vacua collapse to one.
  No domain wall, no asymmetry, no arrow of time.
  Self-reference equation formally satisfied but content-free.
  Result: self-reference without separation.

LEVEL 1 — ORTHOGONAL (Ru, Z[i])
  No solution. Wrong quadratic ring entirely.
  Gaussian integers see rotation (i⁴ = 1) but not growth (φⁿ).
  Result: structure without self-reference.

LEVEL 0 — IMPOSSIBLE (J₄, GF(2))
  q + q² = q(1+q) = q·q̄ = 0 ≠ 1 for all q.
  XOR arithmetic makes self-reference a contradiction.
  The most radically alien mathematical universe.
  Result: no self-reference, no physics, nothing.

The 6 pariah sporadic groups are not random exceptions —
they are the 6 ways self-reference can FAIL to produce physics.
Each failure mode is structurally distinct:
  J₄:  impossible    (wrong arithmetic)
  Ru:  orthogonal    (wrong ring)
  Ly:  degenerate    (ramification)
  J₃:  fused         (over-identification)
  J₁:  truncated     (no fine structure)
  O'N: elliptic      (moonshine without modularity)

The Monster succeeds because Z[φ] in characteristic 0 is the
UNIQUE setting where:
  (a) q + q² = 1 has two distinct irrational roots
  (b) one root is a Pisot number (→ arrow of time)
  (c) modular forms at q converge (→ coupling constants)
  (d) Fibonacci recurrence produces memory (→ bound states)
  (e) the nome is transcendental (→ infinite precision physics)
""")

# ============================================================
# Numerical verification block
# ============================================================

print("=" * 72)
print("NUMERICAL VERIFICATION BLOCK")
print("=" * 72)
print()

# Core checks
q = Q_GOLD
print(f"q = 1/φ = {q:.15f}")
print(f"q + q² = {q + q**2:.15f}  (should be 1)")
print(f"φ + (-1/φ) = {PHI + (-1/PHI):.15f}  (should be 1 = √5 - 2/φ... wait)")
print(f"φ - 1/φ = {PHI - 1/PHI:.15f}  (should be 1)")
print(f"φ · (-1/φ) = {PHI * (-1/PHI):.15f}  (should be -1)")
print()

# Lucas numbers at pariah-related indices
print("Lucas numbers at key indices:")
for n in [4, 5, 6, 7, 10, 11, 18, 19]:
    print(f"  L({n}) = {lucas_number(n)}")

print()
print("Fibonacci numbers at key indices:")
for n in [5, 7, 10, 11, 18, 19, 20]:
    print(f"  F({n}) = {fib(n)}")

print()
print("=" * 72)
print("END OF PARIAH NOMES COMPUTATION")
print("=" * 72)
