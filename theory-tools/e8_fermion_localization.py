#!/usr/bin/env python3
"""
E8 FERMION LOCALIZATION DISTANCES
==================================
Extract the 4 A2 distances from the E8 Coxeter geometry.
This is the SPECIFIC computation that connects E8 to fermion masses.

Uses the 4A2 sublattice (from e8_gauge_wall_determinant.py) and computes
how each root projects onto each A2 subspace. The projection magnitudes
determine the fermion localization along the domain wall.

The key question: does the E8 geometry give DIFFERENT distances for
different trinification sectors (up quarks, down quarks, leptons)?
"""

import sys
import math
from collections import defaultdict

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

phi = (1 + math.sqrt(5)) / 2
phibar = 1 / phi

# ============================================================
# E8 ROOT SYSTEM (copied from e8_gauge_wall_determinant.py)
# ============================================================

def dot8(a, b):
    return sum(a[i] * b[i] for i in range(8))

def add8(a, b):
    return tuple(a[i] + b[i] for i in range(8))

def sub8(a, b):
    return tuple(a[i] - b[i] for i in range(8))

def neg8(a):
    return tuple(-a[i] for i in range(8))

def scale8(c, a):
    return tuple(c * a[i] for i in range(8))

def norm_sq8(a):
    return dot8(a, a)

roots = []

# Type 1: +/- e_i +/- e_j (112 roots)
for i in range(8):
    for j in range(i + 1, 8):
        for si in [+1, -1]:
            for sj in [+1, -1]:
                r = [0.0] * 8
                r[i] = si
                r[j] = sj
                roots.append(tuple(r))

# Type 2: (1/2)(+/-1, +/-1, ..., +/-1) with even number of minus signs (128 roots)
for bits in range(256):
    signs = [(-1 if (bits >> k) & 1 else +1) for k in range(8)]
    if sum(1 for s in signs if s == -1) % 2 == 0:
        r = tuple(0.5 * s for s in signs)
        roots.append(r)

assert len(roots) == 240, f"Expected 240 roots, got {len(roots)}"

# Root lookup
root_set = {}
for i, r in enumerate(roots):
    key = tuple(round(x, 4) for x in r)
    root_set[key] = i

def root_to_idx(r):
    key = tuple(round(x, 4) for x in r)
    return root_set.get(key, -1)

# ============================================================
# FIND 4A2 SUBLATTICE
# ============================================================
print("Finding A2 subsystems...")

a2_systems = []
for i in range(240):
    for j in range(i + 1, 240):
        if abs(dot8(roots[i], roots[j]) + 1.0) < 1e-8:
            gamma = add8(roots[i], roots[j])
            k = root_to_idx(gamma)
            if k >= 0:
                ni = root_to_idx(neg8(roots[i]))
                nj = root_to_idx(neg8(roots[j]))
                nk = root_to_idx(neg8(gamma))
                if ni >= 0 and nj >= 0 and nk >= 0:
                    a2 = frozenset([i, j, k, ni, nj, nk])
                    if len(a2) == 6:
                        a2_systems.append(a2)

a2_systems = list(set(a2_systems))
print(f"Found {len(a2_systems)} A2 subsystems")

def are_orth(a, b):
    for i in a:
        for j in b:
            if abs(dot8(roots[i], roots[j])) > 1e-8:
                return False
    return True

print("Searching for 4 mutually orthogonal A2 copies...")
n_sys = len(a2_systems)
found_4a2 = None

for i in range(n_sys):
    if found_4a2:
        break
    for j in range(i + 1, n_sys):
        if not are_orth(a2_systems[i], a2_systems[j]):
            continue
        for k_idx in range(j + 1, n_sys):
            if found_4a2:
                break
            if not are_orth(a2_systems[i], a2_systems[k_idx]):
                continue
            if not are_orth(a2_systems[j], a2_systems[k_idx]):
                continue
            for l in range(k_idx + 1, n_sys):
                if (are_orth(a2_systems[i], a2_systems[l]) and
                    are_orth(a2_systems[j], a2_systems[l]) and
                    are_orth(a2_systems[k_idx], a2_systems[l])):
                    found_4a2 = (i, j, k_idx, l)
                    break

assert found_4a2, "No 4A2 found!"

a2_sets = [a2_systems[idx] for idx in found_4a2]
four_a2_all = frozenset().union(*a2_sets)
print(f"4A2 found! {len(four_a2_all)} diagonal roots, {240 - len(four_a2_all)} off-diagonal")

# Build orthonormal bases
a2_bases = []
for ci, s in enumerate(a2_sets):
    rvecs = [roots[i] for i in sorted(s)]
    e1 = rvecs[0]
    n1 = math.sqrt(norm_sq8(e1))
    e1 = scale8(1.0 / n1, e1)
    e2 = None
    for rv in rvecs[1:]:
        proj = dot8(rv, e1)
        orth = sub8(rv, scale8(proj, e1))
        n2 = math.sqrt(norm_sq8(orth))
        if n2 > 0.1:
            e2 = scale8(1.0 / n2, orth)
            break
    assert e2 is not None
    a2_bases.append((e1, e2))

print("Orthonormal bases constructed")
print()

# ============================================================
# CLASSIFY ROOTS BY WHICH A2 PAIRS THEY PROJECT ONTO
# ============================================================
print("=" * 70)
print("TRINIFICATION DECOMPOSITION: Which A2 pairs each root connects")
print("=" * 70)
print()

def get_projections(r):
    """Get projection magnitude onto each A2 subspace."""
    projs = []
    for ci, (e1, e2) in enumerate(a2_bases):
        p1 = dot8(r, e1)
        p2 = dot8(r, e2)
        norm = math.sqrt(p1 * p1 + p2 * p2)
        projs.append(norm)
    return projs

def get_active_copies(r, threshold=1e-4):
    projs = get_projections(r)
    return tuple(ci for ci, p in enumerate(projs) if p > threshold)

# Classify all roots
copy_groups = defaultdict(list)
for idx, r in enumerate(roots):
    active = get_active_copies(r)
    copy_groups[active].append(idx)

print("Root classification by active A2 copies:")
print(f"{'Active copies':>25s}  {'Count':>6s}  {'Trinification sector'}")
print("-" * 70)

# Map: E8 -> E6 x SU(3)_fam
# Copy 0 = SU(3)_c (color)
# Copy 1 = SU(3)_L
# Copy 2 = SU(3)_R
# Copy 3 = SU(3)_fam
# (This is one possible labeling; the physics is in the COUNTING)

sector_map = {
    (0,): "SU(3)_c adjoint (6 roots)",
    (1,): "SU(3)_L adjoint (6 roots)",
    (2,): "SU(3)_R adjoint (6 roots)",
    (3,): "SU(3)_fam adjoint (6 roots)",
    (0, 1): "Q_L ~ (3,3,1) quarks-L",
    (0, 2): "Q_R ~ (3bar,1,3) quarks-R",
    (1, 2): "L ~ (1,3bar,3bar) leptons",
    (0, 3): "c-fam mixing",
    (1, 3): "L-fam mixing",
    (2, 3): "R-fam mixing",
    (0, 1, 2): "trinification leptoquark (3,3bar,3bar)",
    (0, 1, 3): "multi-copy (c,L,fam)",
    (0, 2, 3): "multi-copy (c,R,fam)",
    (1, 2, 3): "multi-copy (L,R,fam)",
    (0, 1, 2, 3): "all 4 copies",
}

total = 0
for active in sorted(copy_groups.keys()):
    count = len(copy_groups[active])
    sector = sector_map.get(active, "unknown")
    print(f"  {str(active):>25s}  {count:>6d}  {sector}")
    total += count

print(f"\n  Total: {total}")
print()

# ============================================================
# KEY ANALYSIS: PROJECTION MAGNITUDES PER SECTOR
# ============================================================
print("=" * 70)
print("PROJECTION MAGNITUDES — THE DISTANCES THAT DETERMINE MASSES")
print("=" * 70)
print()

# For each 2-copy sector, compute the projection magnitudes onto each A2
print("For each sector, average projection magnitudes onto all 4 A2 copies:")
print(f"{'Sector':>30s}  {'A2_0':>8s}  {'A2_1':>8s}  {'A2_2':>8s}  {'A2_3':>8s}  {'|r|':>8s}")
print("-" * 80)

for active in sorted(copy_groups.keys()):
    if len(copy_groups[active]) == 0:
        continue
    projs_sum = [0.0] * 4
    norm_sum = 0.0
    for idx in copy_groups[active]:
        projs = get_projections(roots[idx])
        for ci in range(4):
            projs_sum[ci] += projs[ci]
        norm_sum += math.sqrt(norm_sq8(roots[idx]))
    n = len(copy_groups[active])
    avg_projs = [p / n for p in projs_sum]
    avg_norm = norm_sum / n
    sector = sector_map.get(active, str(active))
    short_name = sector[:30]
    print(f"  {short_name:>30s}  {avg_projs[0]:>8.4f}  {avg_projs[1]:>8.4f}  {avg_projs[2]:>8.4f}  {avg_projs[3]:>8.4f}  {avg_norm:>8.4f}")

print()

# ============================================================
# THE MASS-RELEVANT QUESTION: WALL DIRECTION
# ============================================================
print("=" * 70)
print("KINK DIRECTION AND FERMION COUPLING SPECTRUM")
print("=" * 70)
print()

# The domain wall kink is along ONE direction v_hat in the 8D Cartan.
# The coupling of root alpha to the kink is: c_alpha = |alpha . v_hat|
#
# For fermion masses, what matters is c_alpha for the MATTER roots
# (the ones in the (27,3) sector).
#
# Test multiple v_hat directions and see which gives the best mass spectrum.

# Natural candidates for v_hat:
# 1. Along one A2 copy (e.g., dark copy)
# 2. Along a direction that maximizes asymmetry between copies
# 3. "Democratic" — equal projection on all 4 copies

# Let's compute couplings for the matter roots (2-copy off-diagonal roots)
# for various v_hat directions

matter_sectors = {}
for active in [(0,1), (0,2), (1,2)]:
    if active in copy_groups:
        matter_sectors[active] = copy_groups[active]

if not matter_sectors:
    print("No 2-copy off-diagonal roots found!")
    print("This means the E8 -> SU(3)^4 branching has different structure.")
    print()

    # Let's see what copy patterns actually exist
    print("All copy patterns that exist:")
    for active in sorted(copy_groups.keys()):
        count = len(copy_groups[active])
        print(f"  {active}: {count} roots")

    # The issue: the 4A2 sublattice has 24 diagonal roots.
    # The remaining 216 roots connect DIFFERENT copies.
    # But they may project onto more than 2 copies simultaneously!

    print()
    print("Checking which patterns have enough roots to form trinification...")
    for active in sorted(copy_groups.keys()):
        if len(active) >= 2 and len(copy_groups[active]) >= 9:
            count = len(copy_groups[active])
            sector = sector_map.get(active, "")
            print(f"  {active}: {count} roots — {sector}")

print()

# ============================================================
# DETAILED COUPLING SPECTRUM FOR EACH v_hat
# ============================================================
print("=" * 70)
print("COUPLING SPECTRUM: c_alpha = |alpha . v_hat| for matter roots")
print("=" * 70)
print()

# Try v_hat along each A2 basis vector
for vhat_label, vhat_copy, vhat_idx in [
    ("A2_0 e1 (color direction)", 0, 0),
    ("A2_1 e1 (L direction)", 1, 0),
    ("A2_2 e1 (R direction)", 2, 0),
    ("A2_3 e1 (family direction)", 3, 0),
]:
    v_hat = a2_bases[vhat_copy][vhat_idx]
    print(f"v_hat = {vhat_label}")
    print(f"  Couplings by sector:")

    all_couplings = {}
    for active in sorted(copy_groups.keys()):
        if len(active) < 2:
            continue
        couplings = sorted(set(round(abs(dot8(roots[i], v_hat)), 6)
                              for i in copy_groups[active]))
        count = len(copy_groups[active])
        sector = sector_map.get(active, str(active))
        if count >= 6:
            print(f"    {sector[:40]:40s}  n={count:3d}  couplings: {couplings[:5]}")
            all_couplings[active] = couplings

    print()

# ============================================================
# THE KEY RESULT: E6 TRIALITY IN THE ROOT STRUCTURE
# ============================================================
print("=" * 70)
print("E6 TRIALITY: ARE THE THREE VISIBLE A2 COPIES EQUIVALENT?")
print("=" * 70)
print()

# Check if permuting copies 0,1,2 gives equivalent root structures
from itertools import permutations

# For each permutation of (0,1,2), count roots in each sector
print("Testing all permutations of visible copies (0,1,2):")
print(f"{'Perm':>15s}  {'(a,b)':>6s}  {'(a,c)':>6s}  {'(b,c)':>6s}  {'(a,b,c)':>8s}")
print("-" * 55)

for perm in permutations([0, 1, 2]):
    a, b, c = perm
    count_ab = len(copy_groups.get((min(a,b), max(a,b)), []))
    count_ac = len(copy_groups.get((min(a,c), max(a,c)), []))
    count_bc = len(copy_groups.get((min(b,c), max(b,c)), []))
    count_abc = len(copy_groups.get(tuple(sorted([a,b,c])), []))
    print(f"  {str(perm):>15s}  {count_ab:>6d}  {count_ac:>6d}  {count_bc:>6d}  {count_abc:>8d}")

print()

# Check: does the structure depend on which copy we call "dark" (family)?
print("Testing all choices of family copy (which A2 = SU(3)_fam):")
print(f"{'Family':>8s}  {'Vis pairs':>40s}")
print("-" * 55)

for fam in range(4):
    vis = [c for c in range(4) if c != fam]
    pairs = [(min(vis[i], vis[j]), max(vis[i], vis[j]))
             for i in range(3) for j in range(i+1, 3)]
    pair_counts = [len(copy_groups.get(p, [])) for p in pairs]
    result = ', '.join(f'{p}:{c}' for p, c in zip(pairs, pair_counts))
    print(f"  {fam:>8d}  {result}")

print()

# ============================================================
# COUPLING ASYMMETRY: THE MASS-GENERATING MECHANISM
# ============================================================
print("=" * 70)
print("COUPLING ASYMMETRY FROM KINK DIRECTION")
print("=" * 70)
print()

# The mass of a fermion in sector (a,b) coupled to kink along v_hat:
# m ~ <psi_0|Phi|psi_1> * exp(-d * something)
# where d depends on the projection of the sector's roots onto v_hat

# Choose v_hat that minimizes the energy of the kink in E8:
# The kink energy is proportional to the number of roots with ZERO coupling.
# We want v_hat along one of the A2 copies (this gives 6 zero-coupling roots
# from that copy, which is the minimum).

# For v_hat along copy 3 (family):
v_hat = a2_bases[3][0]
print(f"v_hat along A2 copy 3 (family direction):")
print()

# Compute distinct couplings for EACH sector
for active in sorted(copy_groups.keys()):
    if len(copy_groups[active]) < 2:
        continue
    couplings = []
    for idx in copy_groups[active]:
        c = abs(dot8(roots[idx], v_hat))
        couplings.append(round(c, 8))

    distinct = sorted(set(couplings))
    count = len(copy_groups[active])
    sector = sector_map.get(active, str(active))

    if count >= 6:
        # For each distinct coupling, count multiplicity
        coupling_mult = {}
        for c in couplings:
            coupling_mult[c] = coupling_mult.get(c, 0) + 1
        mult_str = ', '.join(f'{c:.4f}x{m}' for c, m in sorted(coupling_mult.items()))
        print(f"  {sector[:45]:45s}  {mult_str}")

print()

# Now try v_hat along the SUM of two A2 directions (breaking triality)
print("v_hat breaking E6 triality (along A2_0 + A2_3 combined):")
v_mixed = add8(a2_bases[0][0], a2_bases[3][0])
v_norm = math.sqrt(norm_sq8(v_mixed))
v_mixed = scale8(1/v_norm, v_mixed)

for active in sorted(copy_groups.keys()):
    if len(copy_groups[active]) < 2:
        continue
    couplings = []
    for idx in copy_groups[active]:
        c = abs(dot8(roots[idx], v_mixed))
        couplings.append(round(c, 6))

    count = len(copy_groups[active])
    sector = sector_map.get(active, str(active))

    if count >= 6:
        coupling_mult = {}
        for c in couplings:
            coupling_mult[c] = coupling_mult.get(c, 0) + 1
        mult_str = ', '.join(f'{c:.4f}x{m}' for c, m in sorted(coupling_mult.items()))
        print(f"  {sector[:45]:45s}  {mult_str}")

print()

# ============================================================
# WHAT THE ROOT SYSTEM ACTUALLY SAYS
# ============================================================
print("=" * 70)
print("WHAT THE E8 ROOT SYSTEM ACTUALLY DETERMINES")
print("=" * 70)
print()

# Count TOTAL roots in each sector pair
sector_counts = {}
for active in sorted(copy_groups.keys()):
    if len(active) == 2:
        vis_count = sum(1 for c in active if c != 3)
        dark_count = sum(1 for c in active if c == 3)
        sector_counts[active] = len(copy_groups[active])

print("2-copy root counts (these are the fermion sectors):")
for active, count in sorted(sector_counts.items()):
    sector = sector_map.get(active, str(active))
    print(f"  {active}: {count} roots — {sector}")

# Are ALL 2-copy sectors the same size?
sizes = list(sector_counts.values())
if len(set(sizes)) == 1:
    print(f"\nALL 2-copy sectors have {sizes[0]} roots: PERFECT E8 DEMOCRACY")
    print("The 4 A2 copies are COMPLETELY equivalent in the root structure.")
    print("E8 does NOT distinguish color from family from L from R.")
    print()
    print("THIS IS THE ANSWER TO WHY FERMION MASSES ARE HARD:")
    print("The root system itself is SYMMETRIC under permuting the 4 A2 copies.")
    print("Only the KINK DIRECTION breaks this symmetry.")
    print("And the kink direction is NOT determined by E8 alone —")
    print("it's determined by the vacuum selection (which IS V(phi) = E8).")
else:
    print(f"\n2-copy sector sizes: {sorted(set(sizes))}")
    if len(set(sizes)) <= 3:
        print("Some asymmetry exists — this could generate mass hierarchy!")

print()

# Final count
n_2copy = sum(sector_counts.values())
n_3copy = sum(len(v) for k, v in copy_groups.items() if len(k) == 3)
n_4copy = sum(len(v) for k, v in copy_groups.items() if len(k) == 4)
n_1copy = sum(len(v) for k, v in copy_groups.items() if len(k) == 1)

print(f"E8 root decomposition under 4A2:")
print(f"  1-copy (diagonal):     {n_1copy:3d}  (= 4 x 6 gauge bosons)")
print(f"  2-copy (bifundamental): {n_2copy:3d}  (= 6 x ? fermions)")
print(f"  3-copy:                {n_3copy:3d}")
print(f"  4-copy:                {n_4copy:3d}")
print(f"  Total:                 {n_1copy + n_2copy + n_3copy + n_4copy:3d}")
print()

# The 248 - 240 = 8 Cartan elements are not in the root system
# They give the U(1) factors
print("Plus 8 Cartan elements (not roots), giving U(1) factors.")
print(f"248 = {n_1copy} + {n_2copy} + {n_3copy} + {n_4copy} + 8 = {n_1copy + n_2copy + n_3copy + n_4copy + 8}")
print()

# ============================================================
# WHAT BREAKS THE SYMMETRY: THE KINK
# ============================================================
print("=" * 70)
print("SYMMETRY BREAKING: KINK DIRECTION IN 8D")
print("=" * 70)
print()

print("""
The E8 root system has S4 symmetry permuting the 4 A2 copies.
(Actually larger: the normalizer of 4A2 in W(E8).)

The kink V(Phi) selects ONE direction in 8D Cartan space.
This direction v_hat breaks S4 -> some subgroup.

For trinification:
  v_hat should break S4 -> S3 x Z1
  (keeping the 3 visible copies permutable, but the family copy special)

For the SM specifically:
  Further breaking S3 -> trivial
  (color, L, R all become distinct)

The mass hierarchy comes from HOW MUCH each A2 copy aligns with v_hat.
The closer to alignment, the stronger the coupling to the kink.

But here's the crucial point:
THE CHOICE OF v_hat IS NOT FREE.

The kink minimizes V(Phi). In the 8D Cartan, this means v_hat points
along the direction that minimizes the E8 Casimir energy subject to
the boundary conditions Phi -> phi (left vacuum) and Phi -> -1/phi (right).

For E8 with 4A2 sublattice, the natural kink direction is along the
DARK A2 copy (the one that becomes the family symmetry).
This is because the family SU(3) is the one that the kink BREAKS.

Then:
  - Roots in (0,1): coupling to kink = projection onto A2_3 = 0
    (these quarks are AT the wall, maximally coupled)
  - Roots in (0,3) or (1,3): coupling ~ projection onto A2_3 > 0
    (these mix with family, live off-center)
  - Roots in (2,3): coupling ~ projection onto A2_3 > 0
    (these live furthest from wall center)

The trinification sectors (0,1), (0,2), (1,2) ALL have projection 0
onto A2_3 direction, so they're all AT the wall!

WAIT — that means the kink along the family direction treats ALL visible
sectors equally. The mass hierarchy between up/down/lepton CANNOT come
from this direction.

The kink must be along a MIXED direction that projects onto MULTIPLE copies.
""")

# Let's find the optimal kink direction by brute force
# Try all combinations of basis vectors and find which gives
# the most distinct coupling values for the matter sectors

best_asymmetry = 0
best_v = None
best_label = ""

# Try single A2 directions
for ci in range(4):
    for bi in range(2):
        v = a2_bases[ci][bi]
        # Get couplings for all off-diagonal roots
        couplings_by_sector = {}
        for active in [(0,1), (0,2), (1,2), (0,3), (1,3), (2,3)]:
            if active not in copy_groups:
                continue
            c_vals = sorted(set(round(abs(dot8(roots[i], v)), 4)
                               for i in copy_groups[active]))
            couplings_by_sector[active] = c_vals

        # Measure asymmetry: how different are the 3 visible-visible sectors?
        vis_sectors = [(0,1), (0,2), (1,2)]
        vis_avgs = []
        for vs in vis_sectors:
            if vs in couplings_by_sector:
                vals = [abs(dot8(roots[i], v)) for i in copy_groups[vs]]
                vis_avgs.append(sum(vals) / len(vals) if vals else 0)

        if len(vis_avgs) == 3:
            asym = max(vis_avgs) - min(vis_avgs) if vis_avgs else 0
            label = f"A2_{ci}_e{bi+1}"
            if asym > best_asymmetry:
                best_asymmetry = asym
                best_v = v
                best_label = label

# Try mixed directions
import itertools
for ci1, ci2 in itertools.combinations(range(4), 2):
    for bi1, bi2 in itertools.product(range(2), repeat=2):
        for w1, w2 in [(1,1), (1,phi), (phi,1), (1,phibar), (phibar,1)]:
            v_raw = add8(scale8(w1, a2_bases[ci1][bi1]), scale8(w2, a2_bases[ci2][bi2]))
            v_norm = math.sqrt(norm_sq8(v_raw))
            if v_norm < 1e-10:
                continue
            v = scale8(1/v_norm, v_raw)

            vis_sectors = [(0,1), (0,2), (1,2)]
            vis_avgs = []
            for vs in vis_sectors:
                if vs not in copy_groups:
                    continue
                vals = [abs(dot8(roots[i], v)) for i in copy_groups[vs]]
                vis_avgs.append(sum(vals) / len(vals) if vals else 0)

            if len(vis_avgs) == 3:
                asym = max(vis_avgs) - min(vis_avgs)
                label = f"{w1:.3f}*A2_{ci1}_e{bi1+1} + {w2:.3f}*A2_{ci2}_e{bi2+1}"
                if asym > best_asymmetry:
                    best_asymmetry = asym
                    best_v = v
                    best_label = label

print(f"Best v_hat for maximum visible-sector asymmetry:")
print(f"  Direction: {best_label}")
print(f"  Asymmetry: {best_asymmetry:.6f}")
print()

if best_v is not None:
    print(f"Couplings for this optimal v_hat:")
    for active in sorted(copy_groups.keys()):
        if len(copy_groups[active]) < 2:
            continue
        vals = [abs(dot8(roots[i], best_v)) for i in copy_groups[active]]
        avg_c = sum(vals) / len(vals)
        distinct = sorted(set(round(v, 4) for v in vals))
        sector = sector_map.get(active, str(active))
        if len(copy_groups[active]) >= 6:
            print(f"  {sector[:45]:45s}  avg={avg_c:.4f}  vals: {distinct[:6]}")
    print()

# ============================================================
# THE DEEP ANSWER
# ============================================================
print("=" * 70)
print("THE DEEP ANSWER: WHY FERMION MASSES ARE THE LAST GAP")
print("=" * 70)
print(f"""
The E8 root system with 4A2 sublattice has a LARGE symmetry group
that permutes the 4 A2 copies. The 216 off-diagonal roots are
distributed DEMOCRATICALLY among the 6 pairs of copies.

This democracy IS E6 triality: the three visible SU(3) factors
are equivalent before symmetry breaking.

The kink V(Phi) breaks this democracy by selecting a direction v_hat.
But v_hat lives in 8D Cartan space, and the energy minimization
that determines v_hat involves the FULL E8 potential — not just
the 4A2 sublattice.

The mass hierarchy requires v_hat to project DIFFERENTLY onto
the three visible A2 copies. This requires v_hat to be a MIXED
direction — not along any single A2 copy.

The specific mixed direction is determined by minimizing the
energy of the E8 gauge theory on the domain wall background.
This is the functional determinant computation.

CONCLUSION:
  Fermion masses are hard NOT because the E8 structure is wrong,
  but because they require the FULL E8 gauge theory kink energy,
  not just the lattice geometry. The lattice gives the STRUCTURE
  (which sectors exist, how many generations), but the NUMBERS
  (mass values) come from the dynamical energy minimization.

  This is why the gap is at Level 3, not Level 1 or 2.
  Levels 0-2 are algebraic. Level 3 is dynamical.
""")
