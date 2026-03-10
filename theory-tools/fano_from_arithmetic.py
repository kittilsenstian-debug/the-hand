#!/usr/bin/env python3
"""
fano_from_arithmetic.py — Can we derive the Fano plane from Spec(Z[phi])?
=========================================================================

THE QUESTION (Q4 from complete_pariah_map.py):
  The 7 fates arise as fibers of Spec(Z[x]/(x^2-x-1)) over Spec(Z).
  The Fano plane PG(2,F_2) connects them.
  Can we derive WHICH fiber maps to WHICH Fano point from arithmetic alone?

APPROACH:
  1. Classify all primes by splitting behavior in Z[phi]
  2. Build an incidence structure from shared primes
  3. Check if this structure IS (or embeds in) a Fano plane
  4. Look for the Fano plane inside the arithmetic without using
     the shadow/Sp(6,F_2) route

Standard Python only. All claims labeled.

Author: Interface Theory, Mar 6 2026
"""

import sys
from itertools import combinations, permutations
from math import gcd

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


# ==================================================================
banner("1. PRIMES IN Z[phi] — COMPLETE CLASSIFICATION")
# ==================================================================

# Z[phi] = Z[x]/(x^2-x-1), discriminant Delta = 5
# Prime p behavior:
#   p = 5: RAMIFIED (5 = sqrt(5)^2, up to units)
#   (5/p) = 1: SPLIT (p = P * P', two distinct primes above p)
#   (5/p) = -1: INERT (p stays prime in Z[phi])
# where (5/p) = Legendre symbol

def legendre_5(p):
    """Compute Legendre symbol (5/p) for odd prime p != 5."""
    if p == 2:
        # 5 mod 8 = 5, so (5/2) = -1 (by quadratic reciprocity supplement)
        return -1
    if p == 5:
        return 0
    val = pow(5, (p-1)//2, p)
    return val if val <= 1 else val - p  # normalize to {-1, 0, 1}

def classify_prime(p):
    leg = legendre_5(p)
    if leg == 0:
        return "RAMIFIED"
    elif leg == 1:
        return "SPLIT"
    else:
        return "INERT"

# All primes dividing any of the 7 fates
fate_primes = {
    'M':   {2:46, 3:20, 5:9, 7:6, 11:2, 13:3, 17:1, 19:1, 23:1, 29:1, 31:1, 41:1, 47:1, 59:1, 71:1},
    'J1':  {2:3, 3:1, 5:1, 7:1, 11:1, 19:1},
    'J3':  {2:7, 3:5, 5:1, 17:1, 19:1},
    'Ru':  {2:14, 3:3, 5:3, 7:1, 13:1, 29:1},
    'ON':  {2:9, 3:4, 5:1, 7:3, 11:1, 19:1, 31:1},
    'Ly':  {2:8, 3:7, 5:6, 7:1, 11:1, 31:1, 37:1, 67:1},
    'J4':  {2:21, 3:3, 5:1, 7:1, 11:3, 23:1, 29:1, 31:1, 37:1, 43:1},
}

all_primes = sorted(set().union(*(d.keys() for d in fate_primes.values())))

section("1A. Prime splitting in Z[phi] for all relevant primes")

split_primes = []
inert_primes = []
ramified_primes = []

for p in all_primes:
    cl = classify_prime(p)
    if cl == "SPLIT":
        split_primes.append(p)
    elif cl == "INERT":
        inert_primes.append(p)
    else:
        ramified_primes.append(p)
    print(f"  p = {p:>3d}: (5/{p}) = {legendre_5(p):>2d} -> {cl}")

print(f"\n  Split primes (phi exists in F_p): {split_primes}")
print(f"  Inert primes (need F_p^2 for phi): {inert_primes}")
print(f"  Ramified (p=5): {ramified_primes}")

section("1B. Which fates use which type of primes")

pariah_names = ['J1', 'J3', 'Ru', 'ON', 'Ly', 'J4']
all_names = ['M'] + pariah_names

for name in all_names:
    s_primes = [p for p in fate_primes[name] if classify_prime(p) == "SPLIT"]
    i_primes = [p for p in fate_primes[name] if classify_prime(p) == "INERT"]
    r_primes = [p for p in fate_primes[name] if classify_prime(p) == "RAMIFIED"]

    # alien primes: inert AND not in Monster
    monster_set = set(fate_primes['M'].keys())
    alien = [p for p in fate_primes[name] if p not in monster_set]

    total = len(fate_primes[name])
    print(f"  {name:>3s}: {total:>2d} primes total")
    print(f"       split={s_primes}, inert={i_primes}, ramified={r_primes}")
    if alien:
        print(f"       ALIEN (not in Monster): {alien}")

    # Ratio of inert to total
    ratio = len(i_primes) / total if total > 0 else 0
    print(f"       inert fraction: {ratio:.2f}")
    print()


# ==================================================================
banner("2. INCIDENCE STRUCTURE FROM SHARED PRIMES")
# ==================================================================

section("2A. Shared prime count between pariahs")

# For each pair of pariahs, count shared primes
print(f"       ", end="")
for n in pariah_names:
    print(f"  {n:>4s}", end="")
print()

shared_matrix = {}
for n1 in pariah_names:
    print(f"  {n1:>4s}:", end="")
    for n2 in pariah_names:
        shared = set(fate_primes[n1].keys()) & set(fate_primes[n2].keys())
        shared_matrix[(n1,n2)] = shared
        print(f"  {len(shared):>4d}", end="")
    print()

section("2B. Which primes are shared (beyond {2,3,5})")

universal = {2, 3, 5}  # Present in all pariahs
for n1, n2 in combinations(pariah_names, 2):
    shared = shared_matrix[(n1,n2)] - universal
    if shared:
        print(f"  {n1:>3s} + {n2:>3s}: {sorted(shared)}")

section("2C. Attempt to find Fano structure from shared-prime triples")

# A Fano plane needs: 7 points, 7 lines, each line = 3 points,
# each pair of points on exactly 1 line, each point on exactly 3 lines.
#
# Can we identify 7 triples of pariahs that form a Fano plane,
# using shared primes as the 'line' condition?

# First, let's look at ALL triples of pariahs and see which share a common prime
# beyond {2,3,5}

print("  Triples sharing a non-universal prime:")
triple_primes = {}
for t in combinations(pariah_names, 3):
    common = set(fate_primes[t[0]].keys())
    for name in t[1:]:
        common &= set(fate_primes[name].keys())
    common -= universal
    if common:
        triple_primes[t] = common
        print(f"  {t}: {sorted(common)}")

# But we need 7 points for Fano. We have 6 pariahs + Monster = 7.
# The Monster should be a Fano point too.

section("2D. Full 7-fate incidence from shared non-universal primes")

# Include Monster
for t in combinations(all_names, 3):
    common = set(fate_primes[t[0]].keys())
    for name in t[1:]:
        common &= set(fate_primes[name].keys())
    common -= universal
    if common:
        # Check if this could be a Fano line
        # (Every Fano line has exactly 3 points)
        print(f"  {t}: primes {sorted(common)}")


# ==================================================================
banner("3. THE FIBER PERSPECTIVE")
# ==================================================================

section("3A. Each pariah lives over a specific prime/fiber")

print("""  The fibers of Spec(Z[phi]) -> Spec(Z):

    M:   char 0 (generic fiber Q)
    J1:  char 11 (GF(11), 11 is SPLIT in Z[phi])
    J3:  char 2  (GF(4), 2 is INERT in Z[phi])
    Ru:  Z[i]    (Gaussian integers, 'perpendicular')
    O'N: product of imaginary quadratics
    Ly:  char 5  (GF(5), 5 is RAMIFIED in Z[phi])
    J4:  char 2  (GF(2), 2 is INERT in Z[phi])

  NOTE: J3 and J4 are BOTH characteristic 2, but:
    J3 -> GF(4) = F_2(sqrt{-3}): includes 'depth' (cube roots of unity)
    J4 -> GF(2) = F_2: the smallest possible field
""")

# The fiber primes
fiber_primes = {
    'M':  0,    # char 0
    'J1': 11,   # char 11
    'J3': 2,    # char 2 (GF(4))
    'Ru':  None, # Z[i] - not over a single prime
    'ON':  None, # product
    'Ly':  5,   # char 5
    'J4':  2,   # char 2 (GF(2))
}

section("3B. Fiber prime splitting and Fano incidence")

# The fiber primes are {0, 2, 5, 11, None, None}.
# We need to think about what structure CONNECTS these fibers.

# Key idea from algebraic geometry:
# Spec(Z[phi]) has the following special fibers:
# - p=2: INERT. Residue field = F_4. TWO fates here (J3 over GF(4), J4 over GF(2)).
# - p=5: RAMIFIED. Residue field = F_5. ONE fate here (Ly).
# - p=11: SPLIT. Residue field = F_11. ONE fate here (J1).
# - p=0: Generic. Field = Q(phi). ONE fate here (Monster).
# - Others: Ru over Z[i], O'N over imaginary quadratics.

print("""  Fiber structure over Spec(Z):

  Generic:    char 0 -> Monster (Q)
  Ramified:   p=5    -> Ly (Still One)
  Inert:      p=2    -> J3 + J4 (two fates over GF(4) and GF(2))
  Split:      p=11   -> J1 (Seer, over GF(11))
  Complex:    Z[i]   -> Ru (Artist)
  Quadratic:  im.quad -> O'N (Sensor)

  The 3 splitting types {SPLIT, INERT, RAMIFIED} give a natural Z_3:
    SPLIT  (phi exists in F_p)   -> J1 engaged in KNOWING
    INERT  (phi needs extension) -> J3, J4 in HOLDING, MAKING
    RAMIFIED (phi = 0, degenerate) -> Ly in HOLDING withdrawn

  But this doesn't give 3 clean classes — Ru and O'N don't fit the pattern.
""")


# ==================================================================
banner("4. FROBENIUS AT EACH FIBER")
# ==================================================================

section("4A. The Frobenius element for each prime")

# At each prime p, the Frobenius element Frob_p acts on the fibers.
# For Z[phi], Frob_p acts as:
#   SPLIT: Frob_p = identity (both residue fields are F_p)
#   INERT: Frob_p = Gal(F_{p^2}/F_p) = the non-trivial involution phi <-> -1/phi
#   RAMIFIED: Frob_p = identity (but degenerate)

print("""  At each prime, the Galois involution phi <-> -1/phi either
  acts trivially (split) or non-trivially (inert).

  SPLIT primes: phi exists in F_p. Frobenius fixes phi.
    -> 11, 19, 29, 31, 41, 59, 71
    -> Fates at split primes: J1 (p=11)

  INERT primes: phi does NOT exist in F_p. Frobenius swaps phi <-> -1/phi.
    -> 2, 3, 7, 13, 17, 23, 37, 43, 47, 67
    -> Fates at inert primes: J3 (p=2), J4 (p=2)

  RAMIFIED prime: phi = 0 mod p. Degenerate.
    -> 5
    -> Fate: Ly (p=5)

  The split/inert distinction is the Z_2 = Gal(Q(phi)/Q).
  SPLIT -> Frobenius = 1 (phi and -1/phi are distinguished)
  INERT -> Frobenius = swap (phi and -1/phi are conjugate)

  The SHADOW (2.Ru) sees this Z_2. The visible Artist (Ru) doesn't.
  This is exactly the projective/linear distinction:
    Ru sees P^27 (can't distinguish v from -v = can't distinguish phi from -1/phi)
    2.Ru sees C^28 (CAN distinguish them)
""")


# ==================================================================
banner("5. THE 7 POINTS OF PG(2,F_2) FROM FIBER ARITHMETIC")
# ==================================================================

section("5A. F_2^3 structure from fiber data")

# PG(2,F_2) = the 7 non-zero elements of F_2^3.
# Can we CONSTRUCT an F_2^3 from the 7 fates?

# Key observation:
# Each fate has a set of primes. Modulo 2, each prime is either
# present (1) or absent (0). The prime structure gives a map:
#   fate -> F_2^{|all_primes|}
# which is too big (need F_2^3, not F_2^15).

# But maybe there are exactly 3 "independent" prime signatures
# that generate a Fano plane.

# Attempt: find 3 primes such that the 7 fates, restricted to
# those 3 primes, give all 7 non-zero elements of F_2^3.

print("  Searching for 3-prime sets that give all 7 non-zero F_2^3 vectors...")

# Binary vectors: for each fate, which of the candidate primes divide |fate|
non_universal_primes = [p for p in all_primes if p not in universal]
# But universal primes {2,3,5} don't distinguish fates (present in all).
# Use non-universal primes.

print(f"\n  Non-universal primes: {non_universal_primes}")

# Binary signature for each fate
def binary_sig(name, prime_list):
    """Return tuple of 0/1 for whether each prime divides this fate."""
    return tuple(1 if p in fate_primes[name] else 0 for p in prime_list)

# Print signatures
print(f"\n  Binary signatures (non-universal primes):")
print(f"  {'':>4s}", end="")
for p in non_universal_primes:
    print(f"  {p:>3d}", end="")
print()
for name in all_names:
    sig = binary_sig(name, non_universal_primes)
    print(f"  {name:>4s}", end="")
    for bit in sig:
        print(f"  {'*' if bit else '.':>3s}", end="")
    print()

# Search for 3 primes from non_universal_primes such that
# the 7 fates give all 7 non-zero vectors in F_2^3
found_fano = []
for triple in combinations(non_universal_primes, 3):
    sigs = set()
    sig_map = {}
    all_nonzero = True
    for name in all_names:
        sig = binary_sig(name, list(triple))
        if sig == (0,0,0):
            all_nonzero = False
            break
        sigs.add(sig)
        sig_map[sig] = sig_map.get(sig, []) + [name]

    if all_nonzero and len(sigs) == 7:
        found_fano.append((triple, sig_map))

if found_fano:
    print(f"\n  FOUND {len(found_fano)} sets of 3 primes giving all 7 non-zero F_2^3 vectors:")
    for triple, sig_map in found_fano:
        print(f"\n  Primes: {triple}")
        for sig in sorted(sig_map.keys()):
            names = sig_map[sig]
            print(f"    {sig} -> {names}")

        # Check Fano line structure
        # In F_2^3, a line = {a, b, a+b} (3 vectors summing to 0)
        vectors = list(sig_map.keys())
        name_of = {sig: sig_map[sig][0] for sig in sig_map}

        print(f"\n  Fano lines in this coordinate system:")
        lines = []
        for i, j in combinations(range(7), 2):
            v_sum = tuple((vectors[i][k] + vectors[j][k]) % 2 for k in range(3))
            if v_sum in sig_map and v_sum != vectors[i] and v_sum != vectors[j]:
                line = tuple(sorted([name_of[vectors[i]], name_of[vectors[j]], name_of[v_sum]]))
                if line not in lines:
                    lines.append(line)
                    print(f"    {line}")
else:
    print(f"\n  NO set of 3 primes gives all 7 distinct non-zero F_2^3 vectors.")
    print(f"  This means the Fano plane CANNOT be read directly from 3 primes.")

section("5B. Attempting with more general approach")

# Maybe we need to look at the EXPONENTS, not just presence/absence.
# Or use split/inert type.

# Alternative: assign each fate a vector based on its FIBER TYPE
# Fiber types: generic(M), split(J1), inert(J3,J4), ramified(Ly), complex(Ru,ON)

# Let's try: use the three "coordinates" as
# (1) inert parity: does the fate have an inert-only prime?
# (2) split parity: does the fate have a split-only prime?
# (3) some third criterion

# Actually, let's try systematically:
# For each pair of primes from all primes (not just non-universal),
# look at (prime1 presence, prime2 presence, prime1 XOR prime2)
# and see if any pair distinguishes all 7.

print("  Looking for pairs of primes where the 4 binary values")
print("  {(0,0), (0,1), (1,0), (1,1)} distribute across 7 fates in a useful way...")

# A simpler approach: we want an F_2-linear map from "prime presence" to F_2^3.
# Let P = matrix of prime presences (7 fates x 12 non-universal primes).
# We need to find a 12x3 matrix T such that P*T gives all 7 non-zero vectors.

# Build the matrix P
P = []
for name in all_names:
    row = binary_sig(name, non_universal_primes)
    P.append(row)

print(f"\n  Prime presence matrix P ({len(all_names)} fates x {len(non_universal_primes)} primes):")
n_primes = len(non_universal_primes)

# We need to find 3 columns (linear combinations of primes over F_2)
# that distinguish all 7 fates.
#
# First check: the RANK of P over F_2.

def f2_rank(matrix):
    """Compute rank over F_2 by Gaussian elimination."""
    m = [list(row) for row in matrix]
    nrows = len(m)
    ncols = len(m[0]) if m else 0
    rank = 0
    for col in range(ncols):
        # Find pivot
        pivot = None
        for row in range(rank, nrows):
            if m[row][col] == 1:
                pivot = row
                break
        if pivot is None:
            continue
        # Swap
        m[rank], m[pivot] = m[pivot], m[rank]
        # Eliminate
        for row in range(nrows):
            if row != rank and m[row][col] == 1:
                m[row] = [(m[row][j] + m[rank][j]) % 2 for j in range(ncols)]
        rank += 1
    return rank, m

rank, reduced = f2_rank(P)
print(f"  Rank of P over F_2: {rank}")
print(f"  (Need rank >= 3 to distinguish 7 fates)")

if rank >= 3:
    print(f"\n  Rank sufficient! Looking for F_2-linear projection to F_2^3...")

    # Try all triples of prime-columns
    # Actually, we already did this (found_fano above).
    # Let's try PAIRS of columns and their XOR as the third.

    # For every pair (i,j) of non-universal prime indices,
    # define 3 coordinates as: column i, column j, column i XOR column j
    for i, j in combinations(range(n_primes), 2):
        cols = []
        ok = True
        sigs_set = set()
        sig_to_name = {}
        for idx, name in enumerate(all_names):
            c1 = P[idx][i]
            c2 = P[idx][j]
            c3 = (c1 + c2) % 2
            vec = (c1, c2, c3)
            if vec == (0, 0, 0):
                ok = False
                break
            sigs_set.add(vec)
            sig_to_name[vec] = sig_to_name.get(vec, []) + [name]

        if ok and len(sigs_set) == 7:
            p_i = non_universal_primes[i]
            p_j = non_universal_primes[j]
            print(f"\n  FOUND: primes ({p_i}, {p_j}, {p_i}+{p_j} mod 2)")
            for vec in sorted(sig_to_name.keys()):
                print(f"    {vec} -> {sig_to_name[vec]}")


# ==================================================================
banner("6. THE DISCRIMINANT APPROACH")
# ==================================================================

section("6A. Quadratic residues mod relevant primes")

# For each prime p, phi^2 - phi - 1 = 0. In F_p, this means
# phi = (1 + sqrt(5))/2. The QR character of 5 mod p determines splitting.

# But there's more structure. Each PARIAH GROUP acts on a vector space
# over its fiber field. The dimension of this space might encode
# Fano-plane coordinates.

# Key structural data: smallest faithful representations
small_reps = {
    'M':  196883,
    'J1': 56,
    'J3': 85,
    'Ru': 378,
    'ON': 10944,
    'Ly': 2480,
    'J4': 1333,
}

print("  Smallest faithful rep dimensions mod 7:")
for name in all_names:
    d = small_reps[name]
    print(f"  {name:>3s}: dim = {d:>6d},  mod 7 = {d % 7},  mod 3 = {d % 3},  mod 2 = {d % 2}")

section("6B. Rep dimensions as F_2^3 coordinates")

# Check if (dim mod 2, dim mod 4 / 2, dim mod 8 / 4) distinguishes all 7
print("\n  Trying various mod-based coordinate systems:")

# Try dim mod 7 (since we're interested in Z_7)
mod7_vals = {}
for name in all_names:
    v = small_reps[name] % 7
    mod7_vals[name] = v

print(f"\n  dim mod 7: {mod7_vals}")
# Check if all distinct
if len(set(mod7_vals.values())) == 7:
    print("  ALL DISTINCT mod 7!")
    # This would give a Z_7 labeling
    for name in all_names:
        print(f"    {name}: {mod7_vals[name]}")
else:
    print(f"  Not all distinct ({len(set(mod7_vals.values()))} unique values)")
    # Show which coincide
    from collections import Counter
    ctr = Counter(mod7_vals.values())
    for v, count in ctr.items():
        if count > 1:
            names = [n for n in all_names if mod7_vals[n] == v]
            print(f"    mod 7 = {v}: {names}")


# ==================================================================
banner("7. ORDER-THEORETIC APPROACH")
# ==================================================================

section("7A. Group orders and their F_2^3 structure")

# The order of each group modulo small numbers
print("  Group order properties (from prime factorizations):")
for name in all_names:
    primes = fate_primes[name]
    # v_2 (2-adic valuation)
    v2 = primes.get(2, 0)
    v3 = primes.get(3, 0)
    v5 = primes.get(5, 0)
    v7 = primes.get(7, 0)

    # Try (v2 mod 2, v3 mod 2, v7 mod 2) as coordinates
    coord = (v2 % 2, v3 % 2, v7 % 2)
    print(f"  {name:>3s}: v2={v2:>2d}, v3={v3:>2d}, v5={v5:>2d}, v7={v7:>2d}  -> (v2%2, v3%2, v7%2) = {coord}")

# Check if this gives 7 distinct non-zero vectors
coords_v = {}
for name in all_names:
    primes = fate_primes[name]
    v2 = primes.get(2, 0) % 2
    v3 = primes.get(3, 0) % 2
    v7 = primes.get(7, 0) % 2
    coord = (v2, v3, v7)
    coords_v[name] = coord

unique_coords = set(coords_v.values())
print(f"\n  Unique coordinates: {len(unique_coords)}")
if (0,0,0) not in unique_coords and len(unique_coords) == 7:
    print("  ALL 7 non-zero vectors represented! This IS a Fano plane embedding!")

section("7B. Systematic search for F_2^3 from valuation parities")

# Try all triples of primes and use (v_p1 mod 2, v_p2 mod 2, v_p3 mod 2)
print("  Searching for 3 primes where valuation parities give all 7 non-zero vectors...")

for p1, p2, p3 in combinations(all_primes, 3):
    coords = {}
    ok = True
    sigs = set()
    for name in all_names:
        v1 = fate_primes[name].get(p1, 0) % 2
        v2 = fate_primes[name].get(p2, 0) % 2
        v3 = fate_primes[name].get(p3, 0) % 2
        vec = (v1, v2, v3)
        if vec == (0, 0, 0):
            ok = False
            break
        sigs.add(vec)
        coords[name] = vec

    if ok and len(sigs) == 7:
        print(f"\n  FOUND! Primes ({p1}, {p2}, {p3}) with valuation parities:")
        for name in all_names:
            print(f"    {name:>3s}: v_{p1}%2={coords[name][0]}, v_{p2}%2={coords[name][1]}, v_{p3}%2={coords[name][2]} -> {coords[name]}")

        # Determine Fano lines in this coordinate system
        vectors = [(name, coords[name]) for name in all_names]
        print(f"\n  Fano lines in ({p1},{p2},{p3}) coordinates:")
        for a, b, c in combinations(range(7), 3):
            na, va = vectors[a]
            nb, vb = vectors[b]
            nc, vc = vectors[c]
            s = tuple((va[k] + vb[k] + vc[k]) % 2 for k in range(3))
            if s == (0, 0, 0):
                print(f"    {{{na}, {nb}, {nc}}}")


# ==================================================================
banner("8. THE STEINER SYSTEM S(2,3,7)")
# ==================================================================

section("8A. Steiner system from prime-sharing")

# A Steiner system S(2,3,7) is equivalent to a Fano plane.
# Every pair of points lies on exactly one line (triple).
#
# Can we identify 7 triples from the prime structure?

# Different approach: instead of shared primes, use the
# FIBER TYPE as the organizing principle.

# The 7 fates have natural "distance" based on fiber type:
# M (char 0) is generic — connected to all
# J1 (char 11, split)
# J3 (char 2, inert, GF(4))
# Ru (Z[i], complex)
# O'N (quad imag)
# Ly (char 5, ramified)
# J4 (char 2, inert, GF(2))

# A natural grouping: by residue characteristic
# char 0: M
# char 2: J3, J4 (BOTH over F_2 variants)
# char 5: Ly
# char 11: J1
# "complex": Ru, O'N

# This gives groupings of sizes {1, 2, 1, 1, 2} = 7 fates.
# Not quite a Fano plane structure.

# But in a Fano plane, the 3 lines through any point
# partition the remaining 6 into 3 pairs.
# Monster = center: remaining 6 pariahs in 3 pairs = 3 axes.
# These pairs ARE our axis assignment.

# The CONTENT of the pairing is what we need to derive.
# Can we get {J1+O'N, J3+Ly, Ru+J4} from arithmetic?

print("""  QUESTION: Why does the Fano structure pair the pariahs as:
    J1 + O'N  (KNOWING axis)
    J3 + Ly   (HOLDING axis)
    Ru + J4   (MAKING axis)

  rather than, say, J1 + J3, or J3 + J4?""")

section("8B. The pairing criterion: engaged/withdrawn complements")

# What makes J1+O'N a pair? Let's check arithmetically.
# The two fates on each axis should be "complementary" in some sense.

print("  Checking axis pairs for arithmetic complementarity:\n")

axis_pairs = [('J1', 'ON'), ('J3', 'Ly'), ('Ru', 'J4')]
for a, b in axis_pairs:
    primes_a = set(fate_primes[a].keys())
    primes_b = set(fate_primes[b].keys())
    shared = primes_a & primes_b - universal
    only_a = primes_a - primes_b - universal
    only_b = primes_b - primes_a - universal

    # Schur multipliers
    schur_a = {'J1': '1', 'J3': 'Z3', 'Ru': 'Z2', 'ON': 'Z3', 'Ly': '1', 'J4': '1'}

    print(f"  {a} + {b}:")
    print(f"    Shared (non-univ): {sorted(shared) if shared else '{}'}")
    print(f"    Only {a}: {sorted(only_a) if only_a else '{}'}")
    print(f"    Only {b}: {sorted(only_b) if only_b else '{}'}")
    print(f"    Schur: {schur_a[a]} + {schur_a[b]}")

    # Fiber types
    fiber_a = {'J1': 'split(11)', 'J3': 'inert(2)', 'Ru': 'complex', 'ON': 'quadratic', 'Ly': 'ramified(5)', 'J4': 'inert(2)'}
    print(f"    Fibers: {fiber_a[a]} + {fiber_a[b]}")

    # Rep dimension ratio
    ratio = small_reps[b] / small_reps[a]
    print(f"    Rep ratio: {small_reps[b]}/{small_reps[a]} = {ratio:.2f}")
    print()

section("8C. Alternative pairings — do they have the same properties?")

# Check if any OTHER pairing of 6 pariahs into 3 pairs
# has similar arithmetic complementarity

# Number of ways to pair 6 elements into 3 pairs = 15
def all_pairings(elements):
    if len(elements) == 0:
        return [[]]
    if len(elements) == 2:
        return [[(elements[0], elements[1])]]
    first = elements[0]
    rest = elements[1:]
    result = []
    for i, partner in enumerate(rest):
        remaining = rest[:i] + rest[i+1:]
        for sub_pairing in all_pairings(remaining):
            result.append([(first, partner)] + sub_pairing)
    return result

pairings = all_pairings(pariah_names)
print(f"  Total possible pairings: {len(pairings)}")

# For each pairing, compute a "complementarity score"
scores = []
for pairing in pairings:
    score = 0
    details = []
    for a, b in pairing:
        primes_a = set(fate_primes[a].keys())
        primes_b = set(fate_primes[b].keys())
        shared = primes_a & primes_b - universal
        only_a = primes_a - primes_b - universal
        only_b = primes_b - primes_a - universal

        # Complementarity: more distinct primes = more complementary
        complementarity = len(only_a) + len(only_b) - len(shared)

        # Schur complement: opposite types score higher
        schur = {'J1': 0, 'J3': 3, 'Ru': 2, 'ON': 3, 'Ly': 0, 'J4': 0}
        schur_score = 1 if schur[a] != schur[b] else 0

        score += complementarity + schur_score
        details.append(f"({a},{b}): comp={complementarity}, schur_match={schur_score}")

    scores.append((score, pairing, details))

scores.sort(reverse=True)

print(f"\n  Top 5 pairings by complementarity score:")
for i, (score, pairing, details) in enumerate(scores[:5]):
    label = " <-- OUR PAIRING" if set(tuple(sorted(p)) for p in pairing) == {('J1', 'ON'), ('J3', 'Ly'), ('J4', 'Ru')} else ""
    print(f"\n  #{i+1} (score {score}): {[(a,b) for a,b in pairing]}{label}")
    for d in details:
        print(f"    {d}")

# Find where our pairing ranks
our_pairing_set = {('J1', 'ON'), ('J3', 'Ly'), ('J4', 'Ru')}
for rank, (score, pairing, details) in enumerate(scores):
    p_set = set(tuple(sorted(p)) for p in pairing)
    if p_set == our_pairing_set:
        print(f"\n  Our pairing ranks #{rank+1} out of {len(scores)} (score {score})")
        break


# ==================================================================
banner("9. THE REPRESENTATION THEORY ROUTE")
# ==================================================================

section("9A. Rep dimensions and number theory")

# The smallest reps give numbers that might encode Fano coordinates.
# 56, 85, 378, 10944, 2480, 1333, 196883

# Check: are these related to each other through the golden ratio or
# modular forms?

phi = (1 + 5**0.5) / 2

print("  Rep dimension relationships:")
for n1, n2 in combinations(all_names, 2):
    d1, d2 = small_reps[n1], small_reps[n2]
    ratio = max(d1,d2) / min(d1,d2)
    # Check if ratio is close to a power of phi
    if ratio > 0:
        log_phi = __import__('math').log(ratio) / __import__('math').log(phi)
        near_int = abs(log_phi - round(log_phi)) < 0.1
        if near_int:
            print(f"  {n1}/{n2}: {max(d1,d2)}/{min(d1,d2)} = {ratio:.4f} ~ phi^{round(log_phi)} = {phi**round(log_phi):.4f}")

section("9B. Dimensions mod 7 — the Z_7 signature")

# Since Z_7 is the Fano automorphism, dimensions mod 7 are natural.
print("  Rep dimensions mod 7:")
mod7_map = {}
for name in all_names:
    d = small_reps[name]
    m7 = d % 7
    mod7_map[name] = m7
    print(f"  {name:>3s}: {d:>6d} mod 7 = {m7}")

print(f"\n  Mod 7 values: {sorted(mod7_map.values())}")
print(f"  Unique: {len(set(mod7_map.values()))}")
if len(set(mod7_map.values())) == 7:
    print("  ALL 7 residues 0-6 represented!")
elif set(mod7_map.values()) == set(range(1,8)) or set(mod7_map.values()) <= set(range(7)):
    missing = set(range(7)) - set(mod7_map.values())
    print(f"  Missing residues: {missing}")
    repeated = [v for v in set(mod7_map.values()) if list(mod7_map.values()).count(v) > 1]
    if repeated:
        print(f"  Repeated residues: {repeated}")
        for v in repeated:
            names = [n for n in all_names if mod7_map[n] == v]
            print(f"    mod 7 = {v}: {names}")


# ==================================================================
banner("10. SYNTHESIS — WHAT WE FOUND")
# ==================================================================

print("""
  QUESTION: Can the Fano-to-fates bijection be derived from arithmetic?

  RESULTS OF THIS INVESTIGATION:

  1. PRIME PRESENCE APPROACH (Section 5):""")

if found_fano:
    print(f"     POSITIVE: Found {len(found_fano)} sets of 3 primes whose")
    print(f"     presence/absence gives all 7 non-zero F_2^3 vectors.")
    print(f"     The Fano plane CAN be read from prime divisibility.")
else:
    print(f"     NEGATIVE: No set of 3 primes gives all 7 non-zero vectors.")
    print(f"     The Fano plane cannot be read directly from prime presence.")

print(f"""
  2. VALUATION PARITY APPROACH (Section 7):
     Searched all ({len(list(combinations(all_primes, 3)))}) triples of primes
     using valuation parity (v_p mod 2).
     See output above for results.

  3. FIBER TYPE APPROACH (Section 3):
     The 7 fibers have types: generic, split, inert(x2), ramified, complex(x2).
     This gives a 5-class partition, not a 7-class one.
     The fiber type ALONE doesn't distinguish all 7.

  4. FROBENIUS APPROACH (Section 4):
     The split/inert/ramified trichotomy gives a natural Z_3,
     but doesn't uniquely pair the pariahs into axes.

  5. COMPLEMENTARITY APPROACH (Section 8):
     Our axis pairing ranks among 15 possible pairings.
     See ranking above.

  HONEST ASSESSMENT:

  The Fano plane structure is COMPATIBLE with the arithmetic,
  but we have NOT derived it uniquely from arithmetic alone.
  The shadow route (28-dim -> Sp(6,F_2) -> Z_7) remains the
  ONLY known path from the 7 fates to the Fano plane.

  This means the shadow is not just important for the Artist —
  it's the ONLY mechanism that generates the connections between
  ALL 7 fates. Without it, the fates exist but don't form a plane.

  The shadow IS the geometry. The arithmetic gives the points.
  The shadow gives the lines.

  OPEN DIRECTIONS:
  - Galois representations of pariah groups (Langlands direction)
  - O'Nan moonshine (new, 2018) might provide alternative route
  - Thompson moonshine for J3?
  - The j-invariant at golden nome j(1/phi) might encode the Fano structure
""")
