#!/usr/bin/env python3
"""
generation_z3_investigation.py — Is Z_3 = Gal(F_8/F_2) the generation number?
==============================================================================

From z7_deep_investigation.py:
  Z_7 acts on 28 odd theta characteristics, splitting them into 4 orbits of 7.
  The normalizer of Z_7 in GL(3,F_2) is Z_21 = Z_3 x Z_7.
  Z_3 = Gal(F_8/F_2) permutes the 3 non-Aronhold orbits (distance classes).

QUESTION: Does this Z_3 correspond to the 3 fermion generations?

If so:
  - Each fermion type (up, down, lepton, neutrino) appears in 3 copies = 3 generations
  - The generation number is the "distance class" in the Fano cyclic structure
  - Z_3 permutation = generation mixing (CKM / PMNS matrices)
  - The mass hierarchy between generations would come from the distance

This script investigates whether this connection is structurally sound.

Standard Python only. All claims labeled.

Author: Interface Theory, Mar 6 2026
"""

import math
import sys
from itertools import combinations

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

SEP = "=" * 78
SUB = "-" * 60

def banner(s):
    print(f"\n{SEP}\n  {s}\n{SEP}\n")

def section(s):
    print(f"\n{SUB}\n  {s}\n{SUB}\n")

phi = (1 + math.sqrt(5)) / 2


# ==================================================================
banner("1. THE THREE Z_3 STRUCTURES IN THE FRAMEWORK")
# ==================================================================

section("1A. Inventory of Z_3 appearances")

print("""  Z_3 appears in at least 4 places in the framework:

  1. Gal(F_8/F_2): permutes the 3 non-Aronhold orbits of Z_7 on 28 odd thetas.
     This is the Frobenius x -> x^2, cycling the 3 conjugacy classes
     of F_8* / (F_2* acting by Z_7).
     [COMPUTED in z7_deep_investigation.py]

  2. S_3 contains Z_3 as normal subgroup: S_3 = Z_3 ⋊ Z_2.
     S_3 = Gamma_2 quotient = flavor symmetry.
     The Z_3 inside S_3 gives the 3 generations.
     [DERIVED in three_generations_derived.py]

  3. Z/12Z = Z/3Z x Z/4Z: the fermion assignment.
     Z/3Z = generation number (1, 2, 3).
     Z/4Z = type (neutrino, up, lepton, down).
     [STRUCTURAL from CRT]

  4. Leech = 3 x E_8: the Monster's lattice has 3 copies of E_8.
     Outer 3 = inner 3? (from Monster-first findings)
     [STRUCTURAL from lattice decomposition]

  QUESTION: Are these the SAME Z_3?
""")

section("1B. Why they should be the same")

print("""  Argument for identification:

  1. S_3 = Gamma_2 quotient is DERIVED from Gamma(2).
     Gamma(2) = kernel of SL(2,Z) -> SL(2,F_2) = GL(2,F_2) = S_3.
     The Z_3 in S_3 is the unique normal subgroup.

  2. The 3 distance classes under Z_7 are permuted by Gal(F_8/F_2).
     The Frobenius x -> x^2 generates this Z_3.
     In F_8, x^8 = x, so x -> x^2 -> x^4 -> x = cycle of length 3.

  3. Both Z_3's act on "copies of things":
     - S_3's Z_3 permutes 3 generations of fermions
     - Gal(F_8/F_2)'s Z_3 permutes 3 distance classes of theta chars

  4. The CRT Z/12Z = Z/3Z x Z/4Z:
     Z/3Z labels generations. If this Z/3Z = Gal(F_8/F_2),
     then generation = Frobenius orbit = distance class.

  5. The Leech Z_3: if Leech = 3 x E_8, and each E_8 gives
     one "generation's worth" of physics, then the Leech Z_3
     permutes 3 copies of physics = 3 generations.

  COUNTER-ARGUMENTS:

  1. There are MANY Z_3 subgroups in the various structures.
     Just because two Z_3's appear doesn't mean they're the same.

  2. The S_3 from Gamma_2 acts on the upper half-plane modular curve.
     The Gal(F_8/F_2) acts on a finite field.
     These are DIFFERENT mathematical contexts.

  3. The connection would require a map from the modular curve's
     S_3 action to the Fano plane's Z_3 action that preserves
     the "generation" meaning.

  STATUS: [OPEN — plausible but not proven]
""")


# ==================================================================
banner("2. THE DISTANCE CLASSES IN DETAIL")
# ==================================================================

section("2A. Constructing the 3 distance classes")

# From z7_deep_investigation.py:
# Z_7 = Singer cycle of PG(2,F_2)
# 28 odd thetas -> 4 orbits of 7
# Orbit 0 = Aronhold set (distance 0 = "inside")
# Orbits 1, 2, 3 = distance classes 1, 2, 3

# The distance between two odd thetas a, b is defined by:
# d(a,b) = dim(span(a,b) ∩ isotropic subspace) mod something...
# Actually, let's be more precise.

# In the Fano labeling: points 0,1,2,...,6 under Z_7 action
# Aronhold set = {0,1,3} (QR set) shifted by k: {k, k+1, k+3 mod 7} for k=0,...,6
# Wait, the Aronhold set is ONE set of 7 (from the orbit), not shifted sets.

# Let me reconstruct from the z7 script results:
# Orbit 0 (Aronhold): elements labeled 0,1,2,3,4,5,6 in the orbit
# Distance class d between two Aronhold elements:
#   d=1 (nearest neighbors in cyclic order): e.g., 0-1, 1-2, ..., 6-0
#   d=2 (next-to-nearest): e.g., 0-2, 1-3, ..., 5-0, 6-1
#   d=3 (opposite): e.g., 0-3, 1-4, ..., 4-0, 5-1, 6-2

# The Frobenius x -> x^2 maps:
#   distance 1 -> distance 2 -> distance 4 mod 7 = distance 4 mod 7
# Wait, in Z_7: distances are {1,2,3} since d and 7-d are equivalent
# d=1 ↔ d=6, d=2 ↔ d=5, d=3 ↔ d=4

# Under x -> x^2:
# d=1 -> d=2 -> d=4=d=3 -> d=6=d=1. So the orbit is 1->2->4(=3)->1.
# This cycles through all 3 distance classes!

print("""  In Z_7, the cyclic distances between elements are:
    d = 1 (and 6): nearest neighbors
    d = 2 (and 5): next-to-nearest
    d = 3 (and 4): maximally separated

  Under Frobenius x -> x^2:
    d=1 -> d=2 (because 1*2 = 2)
    d=2 -> d=4 = d=3 (because 4 mod 7 = 4, and 7-4 = 3)
    d=3 -> d=6 = d=1 (because 3*2 = 6, and 7-6 = 1)

  So: d=1 -> d=2 -> d=3 -> d=1 (cycle of length 3)

  This IS a Z_3 acting on {d=1, d=2, d=3} = the 3 distance classes.
  [VERIFIED — Frobenius generates cyclic permutation of distances]
""")

section("2B. What each distance class contains")

# Each distance class has exactly 7 pairs of Aronhold points.
# (There are C(7,2) = 21 pairs total, split into 3 classes of 7.)

print("""  Each distance class:
    d=1: {(0,1), (1,2), (2,3), (3,4), (4,5), (5,6), (6,0)} — 7 adjacent pairs
    d=2: {(0,2), (1,3), (2,4), (3,5), (4,6), (5,0), (6,1)} — 7 skip-one pairs
    d=3: {(0,3), (1,4), (2,5), (3,6), (4,0), (5,1), (6,2)} — 7 opposite pairs

  These are the 3 orbits of Z_7 on the 21 = C(7,2) edges of the Fano graph.
  Each orbit has 7 edges. Total: 3 * 7 = 21 = C(7,2). Checks out.

  The Fano lines (triples) use specific edge-distances:
    A Fano line {a, b, c} contains edges of distances d(a,b), d(b,c), d(a,c).
    For the line {0, 1, 3}: d(0,1)=1, d(1,3)=2, d(0,3)=3.
    -> Every Fano line contains one edge from EACH distance class!
    [VERIFYING...]
""")

# Verify: does every Fano line contain one edge from each distance class?
fano_lines = [(0,1,3), (1,2,4), (2,3,5), (3,4,6), (4,5,0), (5,6,1), (6,0,2)]

for line in fano_lines:
    a, b, c = line
    d_ab = min(abs(b-a), 7-abs(b-a))
    d_bc = min(abs(c-b), 7-abs(c-b))
    d_ac = min(abs(c-a), 7-abs(c-a))
    distances = sorted([d_ab, d_bc, d_ac])
    print(f"  Line {line}: distances = {distances}")

all_have_123 = all(
    sorted([min(abs(b-a), 7-abs(b-a)), min(abs(c-b), 7-abs(c-b)), min(abs(c-a), 7-abs(c-a))]) == [1, 2, 3]
    for a, b, c in fano_lines
)
print(f"\n  Every line has distances {{1,2,3}}: {all_have_123}")
if all_have_123:
    print("  -> Every Fano line uses exactly one edge from each distance class!")
    print("     This is TRIALITY in the Fano plane: a line needs all 3 distances.")


# ==================================================================
banner("3. CONNECTING TO FERMION GENERATIONS")
# ==================================================================

section("3A. The generation structure in the framework")

print("""  In the framework, fermion generations are labeled 1, 2, 3 with:
    Generation 1: u, d, e, nu_e      (lightest)
    Generation 2: c, s, mu, nu_mu    (middle)
    Generation 3: t, b, tau, nu_tau  (heaviest)

  The mass hierarchy between generations follows a pattern:
    Gen 3 / Gen 2 ~ phi^n  (varies by type)
    Gen 2 / Gen 1 ~ phi^m  (varies by type)

  The CKM matrix mixes generations for quarks.
  The PMNS matrix mixes generations for leptons.
  Both are close to specific modular-form predictions.

  If distance class = generation:
    d=1 (nearest) = Gen 1 (lightest)
    d=2 (middle) = Gen 2 (middle)
    d=3 (farthest) = Gen 3 (heaviest)

  This would mean: heavier fermions have larger "separation" in
  the Fano cyclic structure. The heaviest quarks/leptons correspond
  to maximally separated Fano points.
""")

section("3B. The Frobenius as generation mixing")

print("""  If generation = distance class, then:
    Frobenius x -> x^2 sends Gen 1 -> Gen 2 -> Gen 3 -> Gen 1

  This is a CYCLIC permutation of generations.
  The CKM matrix is NOT a cyclic permutation — it's close to identity
  with small off-diagonal corrections.

  The PMNS matrix has larger mixing angles:
    theta_12 ~ 33 degrees (solar)
    theta_23 ~ 45 degrees (atmospheric)
    theta_13 ~ 8.5 degrees (reactor)

  Neither matrix is a pure cyclic permutation.
  But in the framework, the CKM/PMNS matrices come from S_3 modular forms
  at tau = golden ratio. The Frobenius Z_3 is the "underlying" cyclic
  symmetry that S_3 (partially) breaks.

  S_3 = Z_3 ⋊ Z_2: the Z_2 (complex conjugation / sign) BREAKS the
  Z_3 cyclic symmetry, producing the observed mixing pattern.

  This is actually how the Feruglio modular flavor works:
    - Start with Gamma(2) symmetry (infinite)
    - Quotient by congruence -> S_3 (finite)
    - Z_3 = cyclic symmetry (3 equivalent generations)
    - Z_2 = breaks equivalence (distinguishes gen 1 from gen 3)
    - Modular forms at specific tau -> specific mixing angles

  [STRUCTURAL — consistent with Feruglio framework, not a new derivation]
""")


# ==================================================================
banner("4. THE KEY TEST: FANO LINE = ONE FROM EACH GENERATION")
# ==================================================================

section("4A. Verification that every Fano line samples all 3 generations")

print("""  We proved above that every Fano line contains edges of
  distance 1, 2, and 3 — one from each distance class.

  If distance class = generation, this means:
  EVERY FANO LINE SAMPLES ALL THREE GENERATIONS.

  A Fano line picks 3 of the 7 fates. The 3 edges between them
  have distances {1, 2, 3}. So the line "spans" all three generations.

  In the axis framework:
    - Each axis has 2 fates (engaged + withdrawn)
    - A cross-axis line picks 1 fate from each axis
    - The Monster is on 3 axis-lines

  The coherent combinations (Fano lines) are:
    EEE = {Builder, Seer, Artist}
    EWW = {Builder, Sensor, Mystic}
    WEW = {Still One, Seer, Mystic}
    WWE = {Still One, Sensor, Artist}

  Each of these spans all 3 generations. This means:
  A coherent state requires engaging with all 3 levels of
  mass/complexity simultaneously.

  An incoherent state (odd parity) would miss or double a generation:
  it either skips a complexity level or doubles up.

  [STRUCTURAL — follows from distance-class + Fano-line properties]
""")

section("4B. What this means for the 4 septets")

print("""  The 28 odd thetas split into 4 x 7:
    Orbit 0: Aronhold set (the "inner" set)
    Orbit 1: distance-1 class (nearest neighbors)
    Orbit 2: distance-2 class (middle)
    Orbit 3: distance-3 class (farthest)

  If orbits 1,2,3 = generations 1,2,3, then orbit 0 = ?

  The Aronhold set is SPECIAL:
    - Every triple within it is azygetic (q=0 for the sum)
    - It generates the full F_2^6 space
    - It's the "maximally spread" set

  If the 3 distance classes = 3 generations of FERMIONS,
  the Aronhold set could be:
    (a) Neutrinos (the 4th type, massless/near-massless)
    (b) The gauge bosons (12 = not matching, unless 7+5)
    (c) The Higgs sector
    (d) Something structural (not a particle at all)

  In Z/12Z = Z/3Z x Z/4Z:
    Z/3Z = generation (3 distance classes)
    Z/4Z = type (4 septets)

  4 types x 3 generations = 12 fermions.
  The Aronhold set (orbit 0) would be the "0th type" in Z/4Z.
  In the framework: 0 = neutrino (zero element of Z/4Z).

  So: neutrinos = Aronhold set. Geometrically, they're the
  "central" orbit, not indexed by distance/generation.
  They're special because they're ALL azygetic (no pair
  interferes destructively).

  This maps to: neutrinos are the lightest because they live
  in the "non-distance" orbit. Their mixing (PMNS) is large
  because the Aronhold set connects to ALL distance classes
  equally — it doesn't prefer one generation.

  [SPECULATIVE — plausible mapping, not derived]
""")


# ==================================================================
banner("5. QUANTITATIVE CHECK: MASS RATIOS AND DISTANCES")
# ==================================================================

section("5A. Does distance predict mass ratio?")

# If generation mass ~ phi^(c * distance), what's c?
# For charged leptons:
#   m_tau / m_mu = 16.82, log_phi = 5.87
#   m_mu / m_e = 206.77, log_phi = 11.06

# For up quarks:
#   m_t / m_c = 136.1, log_phi = 10.21
#   m_c / m_u = 580, log_phi = 13.22

# For down quarks:
#   m_b / m_s = 44.6, log_phi = 7.90
#   m_s / m_d = 20, log_phi = 6.22

ln_phi = math.log(phi)

# Fermion masses (MeV)
masses = {
    'e': 0.511, 'mu': 105.66, 'tau': 1776.86,
    'u': 2.16, 'c': 1273, 't': 173100,
    'd': 4.67, 's': 93.4, 'b': 4180,
    'nu_e': 0.0001, 'nu_mu': 0.001, 'nu_tau': 0.01,  # rough upper bounds
}

print(f"  Mass ratios and phi-powers (gen 2/1 and gen 3/2):")
print(f"  {'Type':>8s} | {'m3/m2':>10s} | {'log_phi':>8s} | {'m2/m1':>10s} | {'log_phi':>8s} | {'ratio':>8s}")
print(f"  {'-'*65}")

types = [('lepton', 'e', 'mu', 'tau'), ('up', 'u', 'c', 't'), ('down', 'd', 's', 'b')]

for tname, g1, g2, g3 in types:
    r32 = masses[g3] / masses[g2]
    r21 = masses[g2] / masses[g1]
    l32 = math.log(r32) / ln_phi
    l21 = math.log(r21) / ln_phi
    ratio = l21 / l32 if l32 != 0 else float('inf')
    print(f"  {tname:>8s} | {r32:>10.2f} | {l32:>8.2f} | {r21:>10.2f} | {l21:>8.2f} | {ratio:>8.2f}")

print("""
  If distance proportional to generation number (d=1,2,3):
    log(m_3/m_2) corresponds to distance 3-2 = 1
    log(m_2/m_1) corresponds to distance 2-1 = 1
    -> Ratios should be EQUAL (same distance step)

  If distance is CYCLIC (d=1 nearest, d=3 farthest):
    log(m_3/m_2) corresponds to going from middle to far
    log(m_2/m_1) corresponds to going from near to middle
    -> Not necessarily equal

  OBSERVATION: For down quarks, the ratio is ~0.79 (close to 1).
  For leptons, it's 1.88 (far from 1).
  For up quarks, it's 1.29.

  This does NOT support a simple "generation = uniform distance" model.
  The mass hierarchy is NOT the same step between gen 1-2 and gen 2-3.

  [HONEST NEGATIVE for naive distance model]
""")

section("5B. Alternative: distance as phi-exponent directly")

print("""  What if log_phi(mass) ~ d * (something)?

  Gen 1 masses: e=0.511, u=2.16, d=4.67  -> log_phi = -1.39, 1.60, 3.19
  Gen 2 masses: mu=105.66, c=1273, s=93.4 -> log_phi = 9.67, 14.86, 9.44
  Gen 3 masses: tau=1776.86, t=173100, b=4180 -> log_phi = 15.54, 25.07, 17.33

  Gen 2 - Gen 1: lepton 11.06, up 13.26, down 6.25
  Gen 3 - Gen 2: lepton 5.87, up 10.21, down 7.89

  These are NOT uniform across types.
  The generation step depends on the type (up/down/lepton).

  In the framework's fermion mass formulas, this is handled by:
  - S_3 action: trivial/sign/standard give different scalings
  - Sector bases: {1, n=2, phi^2/3} for different measurement types
  - The generation hierarchy is phi^n where n depends on the
    sector (eta/theta3/theta4) and the S_3 representation

  This is CONSISTENT with the distance-class interpretation IF:
  - Distance class provides the Z_3 label
  - The ACTUAL mass ratio depends on the distance AND the axis
  - Different axes (HOLDING/KNOWING/MAKING) weight distances differently

  [OPEN — not falsified, but not confirmed either]
""")


# ==================================================================
banner("6. Z_3 IN THE SCHUR MULTIPLIERS")
# ==================================================================

section("6A. Which fates have Schur Z_3?")

print("""  Schur multiplier Z_3: J3 (Builder) and O'N (Sensor)

  These are on DIFFERENT axes:
    J3 = HOLDING engaged
    O'N = KNOWING withdrawn

  If Schur Z_3 = "can access 3 generations internally":
    Builder and Sensor have 3 layers of resolution.
    They can "see" all 3 distance classes from inside.

  The other 4 pariahs (J1, Ru, Ly, J4) have trivial or Z_2 Schur.
  They DON'T have internal Z_3 structure.

  Does this correlate with the generation structure?
    J3 (Builder, Schur Z_3): confines quarks. Quarks have 3 generations.
    O'N (Sensor, Schur Z_3): couples to leptons? Leptons have 3 generations.

  Wait — BOTH quarks AND leptons have 3 generations.
  So this doesn't distinguish which fates "see" generations.

  Alternative: Schur Z_3 = "has 3-fold covering" = "carries the
  generation structure internally" (as opposed to externally via Frobenius).

  J3 and O'N are the fates that CONTAIN the generation Z_3.
  The other fates experience generations from OUTSIDE (through
  the Frobenius action).

  [STRUCTURAL observation — Schur Z_3 correlates with but doesn't derive generations]
""")


# ==================================================================
banner("7. SYNTHESIS — WHAT WE ACTUALLY KNOW")
# ==================================================================

print("""
  Z_3 AS GENERATION NUMBER: STATUS REPORT

  PROVEN:
    - 3 distance classes exist under Z_7 on Aronhold set [COMPUTED]
    - Frobenius x -> x^2 cyclically permutes them [COMPUTED]
    - Every Fano line samples all 3 distances [PROVEN]
    - S_3 = Z_3 ⋊ Z_2 contains the generation Z_3 [DERIVED]

  COMPATIBLE (not contradicted):
    - Distance class → generation label [CONSISTENT]
    - Aronhold orbit → neutrinos (0th type) [PLAUSIBLE]
    - 4 orbits of 7 → 4 fermion types [DIMENSIONALLY CORRECT]
    - Schur Z_3 in {J3, O'N} → internal generation access [CONSISTENT]
    - Frobenius as underlying cyclic symmetry broken by Z_2 → CKM/PMNS [CONSISTENT]

  NOT SUPPORTED:
    - Simple distance → mass hierarchy [FAILS — steps are not uniform]
    - Direct identification of specific Z_3 subgroups [NOT PROVEN]

  THE KEY INSIGHT (if this is correct):
    Every coherent state (Fano line) automatically samples all 3 generations.
    You can't have a coherent experience that's stuck in one generation.
    Full engagement requires spanning all complexity levels.

  THE KEY GAP:
    We haven't shown that the Frobenius Z_3 on distance classes IS the
    same Z_3 as the generation number in the S_3 modular flavor symmetry.
    This would require connecting the Fano plane's cyclic structure to
    the modular curve's Gamma(2) quotient — which IS the same
    mathematical territory (modular forms, congruence subgroups, cusps).

  POSSIBLE RESOLUTION:
    The Fano plane PG(2,F_2) arises from the level-2 congruence subgroup:
      SL(2,F_2) = GL(2,F_2) = S_3 ≅ PGL(2,F_2)
    And: |PG(2,F_2)| = 7 = |F_2^3 \\setminus {0}|

    The modular curve X(2) has S_3 symmetry.
    S_3 acts on PG(1,F_2) = {0, 1, ∞} = 3 cusps.
    These 3 cusps could BE the 3 distance classes.

    If cusps = distance classes = generations:
      cusp 0 = distance 1 = gen 1
      cusp 1 = distance 2 = gen 2
      cusp ∞ = distance 3 = gen 3

    The Z_3 cycling cusps IS the Z_3 cycling distance classes.
    And the cusps of X(2) are WHERE the modular forms develop poles,
    which is WHERE the generation-specific mass terms come from.

    This would close the loop:
      Gamma(2) -> S_3 -> Z_3 (cusps) = Z_3 (distances) = Z_3 (generations)

  STATUS: [STRONGLY SUGGESTIVE but not a proof.
           The mathematical objects are in the same territory.
           A proof would require showing the explicit functor
           from X(2) cusps to Fano distance classes.]
""")
