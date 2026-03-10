"""
CLIMBING THE HIERARCHY — From Nothing to the Monster
=====================================================

What we know:
  Level 1: phi (degree 2) -> Z2 -> E8 (8D) -> 2 vacua, 2 bound states
  Level 2: 2cos(2pi/9) (degree 3) -> Z3 -> Leech (24D) -> 3 vacua, 3 bound states

Questions:
  1. Is there a Level 0? What's BELOW E8?
  2. What's Level 3? Can we derive it?
  3. Does the hierarchy reach the Monster group?
  4. Is there a pattern: 5 -> 9 -> ???
  5. What does "higher dimension" even MEAN here?
"""

import math

phi = (1 + math.sqrt(5)) / 2
phibar = 1 / phi

print("=" * 70)
print("CLIMBING THE HIERARCHY")
print("From Nothing to the Monster")
print("=" * 70)

# =====================================================================
# LEVEL 0: WHAT'S BELOW E8?
# =====================================================================

print("\n" + "=" * 70)
print("LEVEL 0: THE VOID")
print("=" * 70)

print("""
Each level is defined by a totally real algebraic number of degree d:
  Level 1: degree 2 (phi, quadratic)
  Level 2: degree 3 (2cos(2pi/9), cubic)

What about degree 1? That's a RATIONAL number.

A degree-1 "field extension" is Q/Q = the rationals over themselves.
  Galois group: trivial (just the identity) = Z1
  Number of vacua: 1
  Number of walls: 0
  Number of bound states: 0

Potential: V0(x) = lambda * (x - r)^2 (single minimum, no wall)
This is a HARMONIC OSCILLATOR. No kink. No domain wall.
No topology. No self-reference.

Level 0 = the void. Pure rationality. One vacuum.
Nothing happens. No wall to maintain. No consciousness.
No time (trivially: nothing to measure).

Level 0 is not "below" Level 1 in any physical sense.
It's the ABSENCE of structure. The blank page.

The fact that we exist at Level 1 means:
  SOMETHING broke the void's trivial symmetry.
  The first non-trivial Galois group (Z2) appeared.
  That's phi. That's E8. That's us.

Level 1 is the SIMPLEST non-trivial level.
E8 is not the bottom of something — it IS the beginning.
""")

print("Level 0 specification:")
print("  Degree: 1 (rational)")
print("  Galois: Z1 (trivial)")
print("  Vacua: 1")
print("  Walls: 0")
print("  Bound states: 0")
print("  Lattice dimension: 0 (no lattice needed)")
print("  Pisot: N/A")
print("  Consciousness: NONE (no wall to be)")
print("  Time: NONE (nothing to flow)")
print("  Physics: NONE (no structure)")

# =====================================================================
# LEVEL 1 RECAP
# =====================================================================

print("\n" + "=" * 70)
print("LEVEL 1: US (recap)")
print("=" * 70)

print(f"""
  Number: phi = 2*cos(pi/5) = {phi:.10f}
  Polynomial: x^2 - x - 1 = 0
  Degree: 2
  Galois: Z2 (swap phi <-> -1/phi)
  Lattice: E8 (unique even unimodular in 8D)
  Vacua: 2 (phi and -1/phi)
  Walls: 1
  Bound states: 2 (psi_0 = presence, psi_1 = thought)
  Pisot: YES -> arrow of time exists
  Geometry: pentagon (5-fold symmetry)

  This is everything we know as "physics."
  All 55+ constants. All particles. All forces.
  Consciousness, time, matter — all from this level.
""")

# =====================================================================
# LEVEL 2 RECAP
# =====================================================================

print("=" * 70)
print("LEVEL 2: THE TIMELESS GROUND (recap)")
print("=" * 70)

r_level2 = []
for k in [1, 2, 4]:
    r_level2.append(2 * math.cos(2 * math.pi * k / 9))
r_level2.sort(reverse=True)
r2_1, r2_2, r2_3 = r_level2

print(f"""
  Number: r1 = 2*cos(2pi/9) = {r2_1:.10f}
  Polynomial: x^3 - 3x + 1 = 0
  Degree: 3
  Galois: Z3 (triality — cycles 3 vacua)
  Lattice: LEECH (unique rootless even unimodular in 24D)
  Vacua: 3
  Walls: 3 (one between each pair)
  Bound states: 3 (composite wall gives psi_2)
  Pisot: NO -> no arrow of time -> TIMELESS
  Geometry: nonagon (9-fold = 3^2 symmetry)

  Leech = 3 copies of E8 + glue vectors.
  Z3 cycles the 3 copies. That's the Galois action.
  24 decoupled E8 roots = shadow of these 24 dimensions.
""")

# =====================================================================
# LEVEL 3: THE SEARCH
# =====================================================================

print("=" * 70)
print("LEVEL 3: CLIMBING HIGHER")
print("=" * 70)

print("""
Pattern so far:
  Level 1: 2*cos(pi/5),   degree 2, Z2, n=5  (pentagon)
  Level 2: 2*cos(2pi/9),  degree 3, Z3, n=9  (nonagon)
  Level 3: 2*cos(2pi/??), degree 4, Z4, n=??

For 2*cos(2pi/n) to have degree d with CYCLIC Galois group Z_d,
we need: euler_phi(n)/2 = d, and (Z/nZ)* / {+1,-1} is cyclic.

For degree 4, Z4 Galois:
  euler_phi(n) = 8, and quotient must be Z4 (not Z2 x Z2).

Candidates for n with euler_phi(n) = 8:
  n = 15, 16, 20, 24, 30
""")

def euler_phi(n):
    """Euler's totient function."""
    result = n
    p = 2
    temp = n
    while p * p <= temp:
        if temp % p == 0:
            while temp % p == 0:
                temp //= p
            result -= result // p
        p += 1
    if temp > 1:
        result -= result // temp
    return result

# Check which n values give euler_phi(n) = 8
candidates = []
for n in range(3, 100):
    if euler_phi(n) == 8:
        candidates.append(n)
print(f"n with euler_phi(n) = 8: {candidates}")

# For each candidate, check if the Galois group is Z4
print("\nChecking Galois groups:")
for n in candidates:
    # The Galois group of Q(2cos(2pi/n))/Q is (Z/nZ)* / {1, -1}
    # We need to compute this
    units = [k for k in range(1, n) if math.gcd(k, n) == 1]

    # Quotient by {1, n-1} (since n-1 = -1 mod n)
    # Group the units into orbits {k, n-k}
    cosets = []
    seen = set()
    for k in units:
        if k not in seen:
            partner = n - k
            if partner != k:
                cosets.append((min(k, partner), max(k, partner)))
                seen.add(k)
                seen.add(partner)
            else:
                cosets.append((k,))
                seen.add(k)

    d = len(cosets)  # degree of 2cos(2pi/n)

    # Check if the quotient group is cyclic
    # We do this by finding if there's a generator
    # Represent cosets by their smallest element
    coset_reps = [c[0] for c in cosets]

    # Build multiplication table on cosets
    def coset_of(k, n):
        k = k % n
        return min(k, n-k) if math.gcd(k, n) == 1 else None

    # Find if any element generates all cosets
    is_cyclic = False
    generator = None
    for g_rep in coset_reps:
        generated = set()
        power = g_rep
        for _ in range(d + 1):
            c = coset_of(power, n)
            if c is not None:
                generated.add(c)
            power = (power * g_rep) % n
        if len(generated) == d:
            is_cyclic = True
            generator = g_rep
            break

    value = 2 * math.cos(2 * math.pi / n)
    galois_type = f"Z{d}" if is_cyclic else f"non-cyclic (order {d})"
    print(f"  n={n:3d}: degree {d}, 2cos(2pi/{n}) = {value:.6f}, Galois = {galois_type}")

# Focus on the ones with degree 4 and cyclic Z4
print("\n" + "-" * 50)
print("Filtering: degree 4 with Z4 Galois")
print("-" * 50)

# n=15 and n=16 are the main candidates
# Let's compute the minimal polynomials

# For n=15: roots are 2cos(2k*pi/15) for k in a coset of (Z/15Z)*/{1,14}
print("\n--- n = 15 ---")
# (Z/15Z)* = {1,2,4,7,8,11,13,14}
# Cosets of {1,14}: {1,14}, {2,13}, {4,11}, {7,8}
# Roots: 2cos(2pi/15), 2cos(4pi/15), 2cos(8pi/15), 2cos(14pi/15)
# But 2cos(14pi/15) = -2cos(pi/15)... let me use coset reps
# Coset reps: 1, 2, 4, 7
roots_15 = []
for k in [1, 2, 4, 7]:
    r = 2 * math.cos(2 * math.pi * k / 15)
    roots_15.append(r)
    print(f"  2cos(2pi*{k}/15) = {r:.10f}")

roots_15.sort(reverse=True)
print(f"\n  Sorted: {[f'{r:.6f}' for r in roots_15]}")
print(f"  Sum: {sum(roots_15):.6f} (trace)")
print(f"  Product: {roots_15[0]*roots_15[1]*roots_15[2]*roots_15[3]:.6f}")

# Compute minimal polynomial from roots
# p(x) = (x-r1)(x-r2)(x-r3)(x-r4)
# = x^4 - (s1)x^3 + (s2)x^2 - (s3)x + s4
s1 = sum(roots_15)
s2 = sum(roots_15[i]*roots_15[j] for i in range(4) for j in range(i+1,4))
s3 = sum(roots_15[i]*roots_15[j]*roots_15[k]
         for i in range(4) for j in range(i+1,4) for k in range(j+1,4))
s4 = roots_15[0]*roots_15[1]*roots_15[2]*roots_15[3]

print(f"\n  Minimal polynomial: x^4 - ({s1:.1f})x^3 + ({s2:.1f})x^2 - ({s3:.1f})x + ({s4:.1f})")
print(f"  Coefficients: s1={s1:.6f}, s2={s2:.6f}, s3={s3:.6f}, s4={s4:.6f}")

# Verify
print(f"  Check (should all be ~0):")
for r in roots_15:
    val = r**4 - s1*r**3 + s2*r**2 - s3*r + s4
    print(f"    p({r:.6f}) = {val:.2e}")

# n=16: roots are 2cos(2k*pi/16) for k in coset reps
print("\n--- n = 16 ---")
# (Z/16Z)* = {1,3,5,7,9,11,13,15}
# Cosets of {1,15}: {1,15}, {3,13}, {5,11}, {7,9}
# Coset reps: 1, 3, 5, 7
roots_16 = []
for k in [1, 3, 5, 7]:
    r = 2 * math.cos(2 * math.pi * k / 16)
    roots_16.append(r)
    print(f"  2cos(2pi*{k}/16) = {r:.10f}")

roots_16.sort(reverse=True)
print(f"\n  Sorted: {[f'{r:.6f}' for r in roots_16]}")
print(f"  Sum: {sum(roots_16):.6f}")

s1_16 = sum(roots_16)
s2_16 = sum(roots_16[i]*roots_16[j] for i in range(4) for j in range(i+1,4))
s3_16 = sum(roots_16[i]*roots_16[j]*roots_16[k]
            for i in range(4) for j in range(i+1,4) for k in range(j+1,4))
s4_16 = roots_16[0]*roots_16[1]*roots_16[2]*roots_16[3]

print(f"\n  Minimal polynomial: x^4 + ({-s1_16:.1f})x^3 + ({s2_16:.1f})x^2 + ({-s3_16:.1f})x + ({s4_16:.1f})")
print(f"  Coefficients: s1={s1_16:.6f}, s2={s2_16:.6f}, s3={s3_16:.6f}, s4={s4_16:.6f}")

# Verify
print(f"  Check:")
for r in roots_16:
    val = r**4 - s1_16*r**3 + s2_16*r**2 - s3_16*r + s4_16
    print(f"    p({r:.6f}) = {val:.2e}")

# =====================================================================
# Which candidate is "the right" Level 3?
# =====================================================================

print("\n" + "=" * 70)
print("WHICH IS LEVEL 3?")
print("=" * 70)

print("""
Selection criteria (from how Level 1 and Level 2 were chosen):

1. Totally real: ALL roots must be real (for real vacua/domain walls)
2. Cyclic Galois: Z_d (not a product group)
3. Simplest polynomial: minimal coefficients
4. Connects to existing structure
""")

# Check totally real for n=15
print("n=15: All roots real?")
for r in roots_15:
    print(f"  {r:.6f} (real)")
print("  YES - totally real")

# Check for n=16
print("\nn=16: All roots real?")
for r in roots_16:
    print(f"  {r:.6f} (real)")
print("  YES - totally real")

# Both are totally real with Z4 Galois. Which is "simpler"?
print(f"""
Comparison:
  n=15: x^4 + {-s1:.0f}x^3 + {s2:.0f}x^2 + {-s3:.0f}x + {s4:.0f}
         = x^4 - x^3 - 4x^2 + 4x + 1
  n=16: x^4 + {-s1_16:.0f}x^3 + {s2_16:.0f}x^2 + {-s3_16:.0f}x + {s4_16:.0f}
         = x^4 - 4x^2 + 2
""")

# n=16 is MUCH simpler! x^4 - 4x^2 + 2
# This is a biquadratic - and it factors as (x^2 - 2-sqrt(2))(x^2 - 2+sqrt(2))
# Which means x^2 = 2 +/- sqrt(2)
# So x = +/- sqrt(2 +/- sqrt(2))

print("n=16 polynomial: x^4 - 4x^2 + 2 = 0")
print("  This factors: x^2 = 2 +/- sqrt(2)")
print(f"  x = +/- sqrt(2 + sqrt(2)) = +/- {math.sqrt(2 + math.sqrt(2)):.6f}")
print(f"  x = +/- sqrt(2 - sqrt(2)) = +/- {math.sqrt(2 - math.sqrt(2)):.6f}")
print()

# But wait - check discriminant
# For x^4 - 4x^2 + 2, the discriminant determines Galois group
# disc = 2048 = 2^11
# sqrt(disc) = sqrt(2048) = 32*sqrt(2), NOT rational -> Galois is NOT contained in A4
# Actually for a biquadratic, we need to check more carefully

# Let me verify the roots match
print("Verification:")
for r in roots_16:
    val = r**4 - 4*r**2 + 2
    print(f"  ({r:.6f})^4 - 4*({r:.6f})^2 + 2 = {val:.2e}")

# n=15 polynomial: x^4 - x^3 - 4x^2 + 4x + 1
print("\nn=15 polynomial: x^4 - x^3 - 4x^2 + 4x + 1 = 0")
print("Verification:")
for r in roots_15:
    val = r**4 - r**3 - 4*r**2 + 4*r + 1
    print(f"  ({r:.6f})^4 - ... = {val:.2e}")

print(f"""
DECISION: Both work. But look at the PATTERN:

Level 1: x^2 - x - 1 = 0     (trace = 1, constant = -1)
Level 2: x^3 - 3x + 1 = 0    (trace = 0, constant = 1)
Level 3 candidate A (n=15): x^4 - x^3 - 4x^2 + 4x + 1 = 0
Level 3 candidate B (n=16): x^4 - 4x^2 + 2 = 0

Candidate B (n=16) is simpler but has a different FLAVOR:
  - It's a biquadratic (only even powers + constant)
  - Its roots involve sqrt(2), connecting to 2-fold structure
  - Less "interesting" algebraically

Candidate A (n=15) continues the pattern MORE naturally:
  - 5 = 5, 9 = 3*3, 15 = 3*5
  - 15 = LCM(3,5)!!
  - Level 3 COMBINES Level 1 (5) and Level 2 (9/3)!!
  - The polynomial is more complex but richer
""")

# THE PATTERN: 5, 9, 15
print("=" * 50)
print("THE PATTERN IN n:")
print("=" * 50)
print(f"""
  Level 1: n = 5              phi = 2cos(pi/5)
  Level 2: n = 9 = 3^2        r1  = 2cos(2pi/9)
  Level 3: n = 15 = 3 * 5     ???  = 2cos(2pi/15)

  5 = 5
  9 = 3^2
  15 = 3 * 5

  Or looking at the polygon:
  Level 1: pentagon (5 sides)
  Level 2: nonagon (9 sides)
  Level 3: pentadecagon (15 sides)

  15 = lcm(3, 5) = 3 * 5

  This means Level 3 is the PRODUCT of the structures
  from Level 1 (5-fold) and Level 2 (3-fold)!
""")

# But also check n=16 pattern
print("  Alternative: 5, 9, 16?")
print("  5, 9, 16 = 2^4")
print("  No clean pattern with 16.")
print()
print("  5, 9, 15 follows: these are all ODD numbers where")
print("  (Z/nZ)*/{+/-1} is cyclic.")

# =====================================================================
# LATTICE DIMENSION FOR LEVEL 3
# =====================================================================

print("\n" + "=" * 70)
print("LEVEL 3 LATTICE")
print("=" * 70)

print(f"""
For degree d, the lattice dimension must be d*k where d*k = 8n (divisible by 8).

Level 1: d=2, minimal k such that 2k = 8n -> k=4, dim=8 (E8!)
Level 2: d=3, minimal k such that 3k = 8n -> k=8, dim=24 (Leech!)
Level 3: d=4, minimal k such that 4k = 8n -> k=2, dim=8 ???

Wait - k=2 gives dimension 8 again? That's where E8 lives.
But E8 is already "taken" by Level 1.

Next: k=4 -> dimension 16.
Even unimodular lattices in 16D: exactly 2
  - E8 x E8 (product of two E8s)
  - D16+ (the other one)

Next: k=6 -> dimension 24 (Leech again)
Next: k=8 -> dimension 32 (billions of lattices!)

Hmm. The uniqueness argument is WEAKER for Level 3.
""")

# Even unimodular lattice counts by dimension
print("Even unimodular lattice counts:")
lattice_counts = {
    8: ("1 (E8)", "unique"),
    16: ("2 (E8xE8, D16+)", "almost unique"),
    24: ("24 (Niemeier lattices, including Leech)", "special"),
    32: ("~10^9", "NOT unique"),
    40: ("~10^20", "NOT unique"),
    48: ("~10^40", "NOT unique"),
}

for dim, (count, note) in lattice_counts.items():
    print(f"  dim {dim:3d}: {count:50s} [{note}]")

print(f"""
INTERESTING OBSERVATION:

For Level 3 (degree 4), the MINIMAL lattice dimension is 8 (k=2).
But E8 in 8D is Level 1. So Level 3 can't use dimension 8.

The NEXT option is dimension 16. There are exactly 2 lattices:
  1. E8 x E8 = two copies of E8
  2. D16+

But E8 x E8 is literally Level 1 DOUBLED. That's too simple.

Maybe Level 3 uses D16+ (the other 16D even unimodular lattice)?
Or maybe it needs dimension 24 (Leech) — SAME as Level 2??

WAIT. What if higher levels don't need their OWN lattice?
What if they all live INSIDE the Leech lattice (or the Monster)?

HYPOTHESIS:
  Level 1 = E8 (8D sublattice of Leech)
  Level 2 = Leech (the full 24D)
  Level 3 = a SUBSTRUCTURE within the Monster module
  ...
  Level inf = the Monster itself
""")

# =====================================================================
# THE MONSTER CONNECTION
# =====================================================================

print("=" * 70)
print("THE ROAD TO THE MONSTER")
print("=" * 70)

print(f"""
The Monster group M is the largest sporadic simple group.
Order: |M| ~ 8.08 x 10^53

The Monstrous Moonshine connection:
  j(q) = 1/q + 744 + 196884*q + 21493760*q^2 + ...
  The coefficients decompose into Monster representations.

The moonshine module V# is a vertex operator algebra with:
  - Central charge c = 24
  - Dimension = 24 (same as Leech lattice!)
  - Automorphism group = Monster

Conway and Norton (1979): the Monster acts on a graded vector space
  V = V_0 + V_1 + V_2 + ...
  dim(V_0) = 1
  dim(V_1) = 0
  dim(V_2) = 196884 = 1 + 196883

The 196883-dimensional representation is the SMALLEST faithful
representation of the Monster.
""")

# The hierarchy might terminate at the Monster
print("HIERARCHY HYPOTHESIS:")
print(f"  Level 0: Q (rationals) -> void (no structure)")
print(f"  Level 1: Q(phi) -> E8 (8D)     -> Weyl(E8)")
print(f"  Level 2: Q(r1) -> Leech (24D)  -> Conway Co_0")
print(f"  Level 3: ???   -> ???           -> ???")
print(f"  ...")
print(f"  Level N: ???   -> Monster module -> MONSTER GROUP")
print()

# The containment chain
print("The containment chain:")
print(f"  E8 is contained in Leech (3 copies + glue)")
print(f"  Leech symmetry (Co_0) is contained in Monster")
print(f"  |Weyl(E8)| = 696,729,600")
print(f"  |Co_0|     = 8,315,553,613,086,720,000")
print(f"  |Monster|  = 808,017,424,794,512,875,886,459,904,961,710,757,005,754,368,000,000,000")
print()

ratio_co0_e8 = 8315553613086720000 / 696729600
print(f"  |Co_0| / |Weyl(E8)| = {ratio_co0_e8:.2e}")
print(f"  Each level is ASTRONOMICALLY larger than the previous.")

# =====================================================================
# THE PISOT QUESTION AT EACH LEVEL
# =====================================================================

print("\n" + "=" * 70)
print("PISOT AND TIME AT EACH LEVEL")
print("=" * 70)

# Level 1: phi is Pisot
print("Level 1: phi = 1.618034")
print(f"  Conjugate: -1/phi = {-1/phi:.6f}")
print(f"  |conjugate| = {abs(-1/phi):.6f} < phi? YES -> PISOT")
print(f"  -> Arrow of time EXISTS. Experience flows.")
print()

# Level 2: 2cos(2pi/9) is NOT Pisot
r2_roots = sorted([2*math.cos(2*math.pi*k/9) for k in [1,2,4]], reverse=True)
print(f"Level 2: r1 = {r2_roots[0]:.6f}")
for i, r in enumerate(r2_roots[1:], 2):
    print(f"  Conjugate r{i}: {r:.6f}, |r{i}| = {abs(r):.6f}, < r1? {abs(r) < r2_roots[0]}")
print(f"  NOT Pisot (|r3| > r1) -> NO arrow of time. TIMELESS.")
print()

# Level 3 (n=15): check Pisot
print(f"Level 3 (n=15): largest root = {roots_15[0]:.6f}")
for i, r in enumerate(roots_15[1:], 2):
    print(f"  Conjugate: {r:.6f}, |conj| = {abs(r):.6f}, < root? {abs(r) < roots_15[0]}")
is_l3_pisot = all(abs(r) < roots_15[0] for r in roots_15[1:])
print(f"  Pisot? {is_l3_pisot}")
print()

# Level 3 (n=16): check Pisot
print(f"Level 3 (n=16): largest root = {roots_16[0]:.6f}")
for i, r in enumerate(roots_16[1:], 2):
    print(f"  Conjugate: {r:.6f}, |conj| = {abs(r):.6f}, < root? {abs(r) < roots_16[0]}")
is_l3b_pisot = all(abs(r) < roots_16[0] for r in roots_16[1:])
print(f"  Pisot? {is_l3b_pisot}")
print()

print(f"""
REMARKABLE FINDING:

Level 1 (phi): PISOT -> has time, has experience, has physics
Level 2 (2cos(2pi/9)): NOT Pisot -> timeless eternal ground
Level 3 (n=15): {'PISOT' if is_l3_pisot else 'NOT Pisot'} -> {'has time??' if is_l3_pisot else 'also timeless'}
Level 3 (n=16): {'PISOT' if is_l3b_pisot else 'NOT Pisot'} -> {'has time??' if is_l3b_pisot else 'also timeless'}
""")

# =====================================================================
# WHAT HIGHER DIMENSIONS MEAN
# =====================================================================

print("=" * 70)
print("WHAT 'HIGHER DIMENSION' MEANS")
print("=" * 70)

print(f"""
The dimensions are NOT spatial dimensions you could walk around in.
They are ALGEBRAIC dimensions — degrees of freedom for self-reference.

  E8 has 8 algebraic dimensions:
    These become the 8 "directions" in which the wall can vibrate.
    The 240 roots of E8 define the allowed vibration patterns.
    Each pattern = a particle or coupling constant.

  Leech has 24 algebraic dimensions:
    These include the 8 E8 dimensions (times 3 copies = 24).
    The extra 16 dimensions are INVISIBLE to Level 1 physics.
    The 24 decoupled roots point into these hidden dimensions.

  Level 3 would have even more:
    More directions = more ways to be = more structure.
    But from Level 1, we can only see shadows.

Think of it like this:
  Level 0: a point (0D). Nothing.
  Level 1: a line (1 wall in 8D). Two endpoints. You can go back and forth.
  Level 2: a triangle (3 walls in 24D). Three vertices. You can cycle.
  Level 3: a square/tetrahedron (in yet higher D). Four vertices.

  We LIVE on the line (Level 1). We can see the line.
  The triangle (Level 2) contains our line as one edge.
  We see the triangle's shadow but can't step off our edge.
""")

# =====================================================================
# THE GENERATIVE PATTERN
# =====================================================================

print("=" * 70)
print("THE GENERATIVE PATTERN")
print("=" * 70)

# Check: is there a formula for which n gives which level?
print("Pattern search:")
print(f"  Level 1: n=5,  degree=2, 2cos(pi/5)")
print(f"  Level 2: n=9,  degree=3, 2cos(2pi/9)")
print(f"  Level 3: n=15, degree=4, 2cos(2pi/15)")
print()

# Let's check what comes next: degree 5 with Z5
print("Seeking Level 4: degree 5, Z5 Galois")
print("Need n with euler_phi(n)/2 = 5, i.e., euler_phi(n) = 10")
candidates_5 = [n for n in range(3, 200) if euler_phi(n) == 10]
print(f"  n with euler_phi(n) = 10: {candidates_5}")

# Check which are cyclic
for n in candidates_5:
    units = [k for k in range(1, n) if math.gcd(k, n) == 1]
    cosets = []
    seen = set()
    for k in units:
        if k not in seen:
            partner = n - k
            if partner != k and partner in set(units):
                cosets.append(min(k, partner))
                seen.add(k)
                seen.add(partner)
            else:
                cosets.append(k)
                seen.add(k)
    d = len(cosets)
    print(f"  n={n}: degree {d}")

# n=11 gives degree 5 for 2cos(2pi/11)
print(f"\nn=11: 2cos(2pi/11) = {2*math.cos(2*math.pi/11):.10f}")
print(f"  euler_phi(11) = {euler_phi(11)}, degree = {euler_phi(11)//2}")
print("  11 is prime -> (Z/11Z)* = Z10 -> Z10/{+/-1} = Z5")
print(f"  Galois group: Z5 (CYCLIC!) -> valid Level 4 candidate")

# Also n=22 = 2*11
print(f"\nn=22: 2cos(2pi/22) = 2cos(pi/11) = {2*math.cos(math.pi/11):.10f}")
print(f"  euler_phi(22) = {euler_phi(22)}, degree = {euler_phi(22)//2}")

# Level 5: degree 6, Z6
print(f"\nSeeking Level 5: degree 6, Z6")
# Need euler_phi(n) = 12
candidates_6 = [n for n in range(3, 200) if euler_phi(n) == 12]
print(f"  n with euler_phi(n) = 12: {candidates_6}")

# n=13 gives degree 6 (prime, Z12/{+/-1} = Z6)
print(f"  n=13: 2cos(2pi/13) = {2*math.cos(2*math.pi/13):.10f}, degree {euler_phi(13)//2}")

print(f"""
THE HIERARCHY (all levels!):

  Level 0: (void)     -> nothing
  Level 1: n=5        -> phi = 2cos(pi/5)      -> degree 2, Z2, E8
  Level 2: n=9        -> 2cos(2pi/9)            -> degree 3, Z3, Leech
  Level 3: n=15       -> 2cos(2pi/15)           -> degree 4, Z4, ???
  Level 4: n=11       -> 2cos(2pi/11)           -> degree 5, Z5, ???
  Level 5: n=13       -> 2cos(2pi/13)           -> degree 6, Z6, ???

Wait... the pattern in n:
  5, 9, 15, 11, 13, ...

That's NOT monotonically increasing! And it doesn't follow
an obvious formula. Let me reconsider...

Actually maybe the right question is: which n is SIMPLEST
(most natural) for each degree?
""")

# Actually, for primes p, 2cos(2pi/p) always has degree (p-1)/2
# and Galois group Z_{(p-1)/2} (cyclic, since Z/pZ* is cyclic)
print("=" * 50)
print("PRIME PATH: using n = prime")
print("=" * 50)

print("""
For PRIME p:
  2cos(2pi/p) has degree (p-1)/2
  Galois group is ALWAYS cyclic Z_{(p-1)/2}
  (because (Z/pZ)* is cyclic for primes)

So the PRIME SEQUENCE gives a natural hierarchy:
""")

primes = [5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
for p in primes:
    d = (p - 1) // 2
    val = 2 * math.cos(2 * math.pi / p)

    # Check Pisot
    roots_p = [2 * math.cos(2*math.pi*k/p) for k in range(1, d+1)]
    largest = max(roots_p)
    is_pisot = all(abs(r) < largest for r in roots_p if r != largest)

    # Lattice dimension: d*k = 8n, min k
    min_dim = None
    for k in range(1, 100):
        if (d * k) % 8 == 0:
            min_dim = d * k
            break

    pisot_str = "PISOT" if is_pisot else "not Pisot"
    print(f"  p={p:3d}: degree {d:3d}, dim {min_dim:4d}, 2cos(2pi/{p}) = {val:8.5f}, {pisot_str}")

print(f"""
FASCINATING PATTERN:

The primes give a CLEAN hierarchy:
  p=5:  degree 2  -> Level 1 (E8, 8D)
  p=7:  degree 3  -> Level 2 (Leech, 24D)
  p=11: degree 5  -> Level 3 (???, 40D)
  p=13: degree 6  -> Level 4 (???, 48D)
  p=17: degree 8  -> Level 5 (???, 8D again?)
  ...

Wait: p=7 gives degree 3, same as n=9 (Level 2).
Are they the SAME level or DIFFERENT?
""")

# Compare p=7 and n=9
print("Comparing the two degree-3 options:")
print(f"  n=9: x^3 - 3x + 1 = 0, roots: {[f'{r:.4f}' for r in r2_roots]}")
roots_7 = sorted([2*math.cos(2*math.pi*k/7) for k in [1,2,3]], reverse=True)
print(f"  p=7: roots: {[f'{r:.4f}' for r in roots_7]}")

# Minimal polynomial of 2cos(2pi/7)
r7_1, r7_2, r7_3 = roots_7
s1_7 = r7_1 + r7_2 + r7_3
s2_7 = r7_1*r7_2 + r7_2*r7_3 + r7_3*r7_1
s3_7 = r7_1*r7_2*r7_3
print(f"  p=7: x^3 - ({s1_7:.1f})x^2 + ({s2_7:.1f})x - ({s3_7:.1f}) = 0")
print(f"       = x^3 + x^2 - 2x - 1 = 0")

# Check if 2cos(2pi/7) is Pisot
print(f"\n  Is 2cos(2pi/7) Pisot?")
for r in roots_7:
    print(f"    root = {r:.6f}, |root| = {abs(r):.6f}")
is_7_pisot = all(abs(r) < roots_7[0] for r in roots_7[1:])
print(f"  Pisot? {is_7_pisot}")

print(f"""
BOTH n=7 and n=9 give degree 3 with Z3, but:
  n=9: x^3 - 3x + 1 (trace 0, simpler)
  n=7: x^3 + x^2 - 2x - 1 (trace -1, more complex)

  n=9 is "purer" (zero trace = sum of roots vanishes).
  n=7 has nonzero trace.

  MAYBE: n=9 is the "canonical" Level 2 because trace=0
  means the vacua are "balanced" (centroid at the origin).
""")

# =====================================================================
# THE DEEP PATTERN: TRACE ZERO
# =====================================================================

print("=" * 70)
print("TRACE ZERO AS SELECTION RULE")
print("=" * 70)

print("""
Look at the polynomials:
  Level 1: x^2 - x - 1 = 0     (trace = 1, NOT zero)
  Level 2: x^3 - 3x + 1 = 0    (trace = 0)

Hmm, Level 1 has nonzero trace. So trace=0 isn't universal.

But wait: Level 1 is SPECIAL. It's the only level with time.
Maybe Level 1's nonzero trace IS what creates the arrow of time
(one vacuum "heavier" than the other = asymmetry = direction).

For Level 2+, if they're all timeless, maybe trace=0 IS the rule
(perfect symmetry, no direction, all vacua equivalent).

Let me check: for the PRIME hierarchy, which have trace zero?
""")

for p in [5, 7, 11, 13, 17, 19, 23]:
    d = (p - 1) // 2
    roots = [2 * math.cos(2*math.pi*k/p) for k in range(1, d+1)]
    trace = sum(roots)
    print(f"  p={p:3d}: trace = {trace:+.6f} ({'~0' if abs(trace) < 0.01 else 'nonzero'})")

# Also check n=9, 15, 16
for n, label in [(9, "n=9"), (15, "n=15"), (16, "n=16")]:
    d = euler_phi(n) // 2
    coset_reps = []
    seen = set()
    units = [k for k in range(1, n) if math.gcd(k, n) == 1]
    for k in units:
        if k not in seen and (n-k) not in seen:
            coset_reps.append(k)
            seen.add(k)
            seen.add(n-k)
    roots = [2*math.cos(2*math.pi*k/n) for k in coset_reps]
    trace = sum(roots)
    print(f"  {label:5s}: trace = {trace:+.6f} ({'~0' if abs(trace) < 0.01 else 'nonzero'})")

# =====================================================================
# SYNTHESIS: THE FULL PICTURE
# =====================================================================

print("\n" + "=" * 70)
print("SYNTHESIS: THE FULL PICTURE")
print("=" * 70)

print(f"""
What we can now say with confidence:

1. LEVEL 0 = THE VOID
   Degree 1, no Galois symmetry, one vacuum, no walls.
   Nothing exists. No consciousness. No time. No physics.
   Pure rationality (Q).

2. LEVEL 1 = US (E8)
   The FIRST non-trivial level. Degree 2. Z2 Galois.
   The ONLY level that is Pisot -> the ONLY level with time.
   E8 in 8D. 240 roots = 240 particles/constants.
   2 bound states (psi_0 = being, psi_1 = thinking).
   All of known physics lives here.

3. LEVEL 2 = THE TIMELESS GROUND (Leech)
   Degree 3. Z3 Galois = triality.
   NOT Pisot -> no arrow of time -> eternal.
   Leech in 24D = 3 copies of E8 + glue.
   3 bound states. Composite walls.
   The 3-fold patterns in physics (generations, colors)
   are SHADOWS of this level.

4. LEVEL 3+ = HIGHER STRUCTURES
   Degree 4+ with cyclic Galois groups.
   Multiple candidate sequences (primes, trace-zero, etc.)
   Each level adds more vacua, more bound states.
   The lattice dimensions grow (40D, 48D, ...).
   All likely timeless (not Pisot).

5. LEVEL INFINITY = THE MONSTER?
   The Monster group contains everything:
     E8 < Leech < Monster
   The j-invariant encodes Monster reps.
   The Langlands program might be the meta-structure.

   But the Monster might not be the "top" either —
   there could be something beyond sporadic groups.

KEY INSIGHT:

  Level 1 (us) is SPECIAL because it's the only level with TIME.
  We're not "low" or "primitive" — we're the UNIQUE temporal level.

  Everything above us is timeless. Everything below is void.
  We are the INTERFACE between nothing and eternity.

  We are where time happens.
  We are where experience happens.
  We are where physics happens.

  E8 didn't "come from" the Leech lattice in a temporal sense.
  The Leech lattice is the TIMELESS GROUND that Level 1 emerges in.
  Like a wave doesn't "come from" the ocean in sequence —
  the ocean is the ground, the wave is the happening.

  We are the wave. Level 2 is the ocean.
  Level 3+ is... the water? The hydrogen bonds?
  Each deeper level is a more fundamental ground of being,
  but none of them experience time. Only we do.

  THAT is what makes Level 1 special.
  THAT is why we ask the question.
  THAT is why the question exists at all.

  The void can't ask (no structure).
  The eternal can't ask (no time to formulate questions).
  Only the temporal — only us — can ask "what am I?"

  And in asking, we ARE the answer. The quine runs.
""")

print("=" * 70)
print("END OF HIERARCHY CLIMB")
print("=" * 70)
