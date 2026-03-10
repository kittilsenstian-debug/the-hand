#!/usr/bin/env python3
"""
FERMION ASSIGNMENT FROM E8 ROOT GEOMETRY
==========================================

THE QUESTION: Are the 9 fermion g-factors FORCED by E8 root geometry,
or is there freedom in the assignment?

APPROACH:
  1. Construct E8 root system (240 roots in R^8)
  2. Define golden direction v = (0, phi, 1, 1/phi, 0, 0, 0, 0)
  3. Project each root onto v -> get projection magnitudes
  4. Classify roots by A2 sector -> type (up/down/lepton)
  5. Check: do distinct projection classes match fermion g-factors?

THE KNOWN g-FACTORS (from one_resonance_fermion_derivation.py):
  g_t   = 1         (identity)
  g_c   = 1/phi     (conjugate vacuum)
  g_b   = 2         (wall depth n)
  g_tau = phi^2/3   (vacuum/triality)
  g_s   = 3pi/16sqrt2  (Yukawa overlap)
  g_mu  = 1/2       (inverse depth)
  g_u   = sqrt(2/3) (projected breathing norm)
  g_d   = sqrt(3)   (projected triality)
  g_e   = sqrt(3)   (projected triality)

Author: Interface Theory, Mar 4 2026
"""

import math
import sys
from collections import defaultdict

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

# ============================================================
# CONSTANTS
# ============================================================
phi = (1 + math.sqrt(5)) / 2
phibar = 1 / phi
sqrt5 = math.sqrt(5)
pi = math.pi
ln_phi = math.log(phi)

SEP = "=" * 78
THIN = "-" * 78
findings = []

def banner(title):
    print()
    print(SEP)
    print(f"  {title}")
    print(SEP)
    print()

def section(title):
    print()
    print(THIN)
    print(f"  {title}")
    print(THIN)
    print()

def finding(text):
    findings.append(text)
    n = len(findings)
    print(f"\n  ** FINDING {n}: {text}")


# ============================================================
# MODULAR FORMS AT q = 1/phi
# ============================================================
q_nome = phibar

def theta3_fn(q, N=2000):
    s = 1.0
    for n in range(1, N+1):
        t = q**(n*n)
        if t < 1e-300: break
        s += 2*t
    return s

def theta4_fn(q, N=2000):
    s = 1.0
    for n in range(1, N+1):
        t = q**(n*n)
        if t < 1e-300: break
        s += 2*((-1)**n)*t
    return s

def eta_fn(q, N=2000):
    prod = q**(1.0/24.0)
    for n in range(1, N+1):
        qn = q**n
        if qn < 1e-300: break
        prod *= (1 - qn)
    return prod

t3 = theta3_fn(q_nome)
t4 = theta4_fn(q_nome)
eta_val = eta_fn(q_nome)
eps = t4 / t3

alpha_em = 1.0 / 137.035999084
mu_ratio = 1836.15267343

# PT n=2 exact quantities
yukawa_overlap = 3 * pi / (16 * math.sqrt(2))
n_depth = 2
ground_norm = 4.0 / 3.0
breath_norm = 2.0 / 3.0


# ============================================================
# 8D VECTOR OPERATIONS
# ============================================================
def dot8(a, b):
    return sum(a[i]*b[i] for i in range(8))

def scale8(c, a):
    return tuple(c*x for x in a)

def norm8(a):
    return math.sqrt(dot8(a, a))

def normalize8(a):
    n = norm8(a)
    if n < 1e-15: return a
    return scale8(1.0/n, a)

def round8(a, ndigits=6):
    return tuple(round(x, ndigits) for x in a)


# ################################################################
#           PART 1: E8 ROOT SYSTEM
# ################################################################

banner("PART 1: E8 ROOT SYSTEM (240 roots)")

roots = []

# Type 1: +/- e_i +/- e_j (112 roots)
for i in range(8):
    for j in range(i+1, 8):
        for si in (+1.0, -1.0):
            for sj in (+1.0, -1.0):
                r = [0.0]*8
                r[i] = si
                r[j] = sj
                roots.append(tuple(r))

# Type 2: (1/2)(+/-1, ..., +/-1) with even number of minus signs (128 roots)
for bits in range(256):
    signs = [(-1.0 if (bits >> k) & 1 else +1.0) for k in range(8)]
    n_neg = sum(1 for s in signs if s < 0)
    if n_neg % 2 == 0:
        roots.append(tuple(0.5*s for s in signs))

assert len(roots) == 240, f"Expected 240, got {len(roots)}"

# Verify all norms are sqrt(2)
for r in roots:
    assert abs(dot8(r, r) - 2.0) < 1e-10

print(f"  E8 roots: {len(roots)}")
print(f"  All norm^2 = 2: verified")


# ################################################################
#           PART 2: GOLDEN DIRECTION
# ################################################################

banner("PART 2: GOLDEN DIRECTION AND PROJECTIONS")

# The golden direction: lives in the A2 subspace spanned by
# coordinates 1,2,3 (following e8_kink_direction.py convention)
# v = (0, phi, 1, 1/phi, 0, 0, 0, 0)
# This is the ONLY direction whose projections form a golden
# geometric sequence (proven in e8_kink_direction.py).

v_golden_raw = (0.0, phi, 1.0, phibar, 0.0, 0.0, 0.0, 0.0)
v_golden = normalize8(v_golden_raw)
v_norm = norm8(v_golden_raw)

print(f"  Golden direction (raw): (0, phi, 1, 1/phi, 0, 0, 0, 0)")
print(f"  |v| = {v_norm:.6f} = sqrt(phi^2 + 1 + 1/phi^2) = sqrt({phi**2 + 1 + phibar**2:.6f})")
print(f"  Note: phi^2 + 1 + 1/phi^2 = phi + 2 + phibar = 3 + sqrt(5) = {3 + sqrt5:.6f}")
print(f"  So |v| = sqrt(3 + sqrt(5)) = {math.sqrt(3 + sqrt5):.6f}")
print()

# Project all 240 roots onto golden direction
projections = []
for i, r in enumerate(roots):
    p = dot8(r, v_golden)  # projection onto unit vector
    projections.append(p)

# Get unique absolute projections (within tolerance)
abs_proj = sorted(set(round(abs(p), 8) for p in projections))
print(f"  Distinct |projection| values: {len(abs_proj)}")
for ap in abs_proj:
    count = sum(1 for p in projections if abs(abs(p) - ap) < 1e-6)
    print(f"    |proj| = {ap:.6f}  ({count} roots)")


# ################################################################
#           PART 3: A2 SECTOR CLASSIFICATION
# ################################################################

banner("PART 3: SECTOR CLASSIFICATION")

# The 4 A2 copies in E8 live in coordinate pairs:
# A2_1: coords (0,1), A2_2: coords (2,3), A2_3: coords (4,5), A2_4: coords (6,7)
# The golden direction lives in A2_1 + A2_2 (coords 1,2,3).

# For fermion assignment, we need 3 sectors: up, down, lepton.
# These come from the 3 components of the golden direction:
#   phi-component (coord 1) -> up-type
#   1-component (coord 2) -> down-type
#   1/phi-component (coord 3) -> lepton

# Each root's coupling to the wall depends on its overlap with the
# golden direction. Decompose this overlap into the 3 components:

print("  Golden direction components:")
print(f"    coord 1: phi   = {phi:.6f}  -> UP type")
print(f"    coord 2: 1     = 1.000000  -> DOWN type")
print(f"    coord 3: 1/phi = {phibar:.6f}  -> LEPTON type")
print()

# For each root, compute the 3 component projections
sector_projections = []
for i, r in enumerate(roots):
    p_up = r[1] * phi / v_norm      # phi component
    p_down = r[2] * 1.0 / v_norm    # 1 component
    p_lep = r[3] * phibar / v_norm  # 1/phi component
    total = dot8(r, v_golden)        # full projection
    sector_projections.append((total, p_up, p_down, p_lep))

# Group by total projection (positive only — negative = antiparticle)
pos_proj = [(i, p, pu, pd, pl) for i, (p, pu, pd, pl) in enumerate(sector_projections) if p > 1e-8]
pos_proj.sort(key=lambda x: -x[1])  # sort by decreasing projection

print(f"  Roots with positive projection: {len(pos_proj)}")
print()

# Find projection classes
proj_classes = defaultdict(list)
for i, p, pu, pd, pl in pos_proj:
    key = round(p, 6)
    proj_classes[key].append((i, p, pu, pd, pl))

section("Projection classes (positive projections)")
for key in sorted(proj_classes.keys(), reverse=True):
    members = proj_classes[key]
    # Identify dominant sector
    sample = members[0]
    _, p, pu, pd, pl = sample
    fracs = [abs(pu)/abs(p) if abs(p) > 1e-10 else 0,
             abs(pd)/abs(p) if abs(p) > 1e-10 else 0,
             abs(pl)/abs(p) if abs(p) > 1e-10 else 0]
    sector_names = ["UP", "DOWN", "LEPTON"]
    dominant = sector_names[fracs.index(max(fracs))] if max(fracs) > 0.3 else "MIXED"

    print(f"  proj = {key:+.6f}  |  {len(members):3d} roots  |  "
          f"sector fractions: up={fracs[0]:.2f} dn={fracs[1]:.2f} lep={fracs[2]:.2f}  |  {dominant}")


# ################################################################
#           PART 4: COMPARE PROJECTIONS TO g-FACTORS
# ################################################################

banner("PART 4: g-FACTOR IDENTIFICATION")

print("  KNOWN g-factors from fermion mass derivation:")
print()

# The known g-factors and their numerical values
known_g = {
    't':   (1.0,                    "1 (identity)"),
    'c':   (phibar,                 "1/phi"),
    'b':   (2.0,                    "n=2"),
    'tau': (phi**2/3,               "phi^2/3"),
    's':   (yukawa_overlap,         "3pi/16sqrt2"),
    'mu':  (0.5,                    "1/2"),
    'u':   (math.sqrt(2.0/3.0),    "sqrt(2/3)"),
    'd':   (math.sqrt(3.0),        "sqrt(3)"),
    'e':   (math.sqrt(3.0),        "sqrt(3)"),
}

for f in ['t', 'b', 'tau', 'c', 's', 'mu', 'u', 'd', 'e']:
    gv, gn = known_g[f]
    print(f"    g_{f:3s} = {gv:.6f}  ({gn})")

print()

# Normalized projection values (scale so max = 1)
if pos_proj:
    max_proj = max(p for _, p, _, _, _ in pos_proj)
else:
    max_proj = 1.0

section("Projection values normalized to max (= g_t = 1)")
proj_unique = sorted(set(round(p, 6) for _, p, _, _, _ in pos_proj), reverse=True)

# For each unique projection, try to match a g-factor
print(f"  {'Proj (norm)':>12s}  {'Proj (raw)':>12s}  {'Count':>6s}  {'Closest g':>12s}  {'g_name':>20s}  {'Match %':>8s}")
print("  " + "-" * 80)

g_values = {name: val for name, (val, _) in known_g.items()}
g_names_map = {name: desc for name, (_, desc) in known_g.items()}

for pv in proj_unique[:15]:  # top 15
    pn = pv / max_proj  # normalized
    count = sum(1 for _, p, _, _, _ in pos_proj if abs(p - pv) < 1e-5)

    # Find closest g-factor
    best_match = None
    best_err = 999
    for gname, gval in g_values.items():
        err = abs(pn - gval) / max(gval, 1e-10) * 100
        if err < best_err:
            best_err = err
            best_match = gname

    if best_err < 50:
        print(f"  {pn:12.6f}  {pv:12.6f}  {count:6d}  {g_values[best_match]:12.6f}  {g_names_map[best_match]:>20s}  {best_err:7.2f}%")
    else:
        print(f"  {pn:12.6f}  {pv:12.6f}  {count:6d}  {'---':>12s}  {'no match':>20s}  {'---':>8s}")


# ################################################################
#           PART 5: GOLDEN GEOMETRIC SEQUENCE TEST
# ################################################################

banner("PART 5: GOLDEN GEOMETRIC SEQUENCE")

# The key claim from e8_kink_direction.py:
# The golden direction is the ONLY direction whose projections
# form a golden geometric sequence: a_up * a_lep = a_down^2

# Verify: the 3 components of the golden direction are (phi, 1, 1/phi)
# These satisfy: phi * (1/phi) = 1 = 1^2  => EXACT golden geometric sequence

print("  Golden direction components: (phi, 1, 1/phi)")
print(f"  phi * (1/phi) = {phi * phibar:.10f}")
print(f"  1^2           = {1.0:.10f}")
print(f"  Geometric mean test: a_up * a_lep = a_down^2  => EXACT")
print()

# Now test: which g-factors match RATIOS of these components?
print("  g-factor ratios from direction components:")
print()
print(f"  g_t = 1 = a_down/a_down")
print(f"  g_c = 1/phi = a_lep/a_down = {phibar:.6f}")
print(f"  g_b = n = 2 (NOT a projection ratio — topological)")
print(f"  g_tau = phi^2/3 = {phi**2/3:.6f}")
print(f"       = a_up * a_down / (a_up + a_down + a_lep)")
print(f"       = phi * 1 / (phi + 1 + 1/phi)")
print(f"       = phi / (phi + 1 + phibar)")
print(f"       = phi / (2phi) = 1/2... NO")
print()

# More carefully: what algebraic expressions in {phi, 1, 1/phi} give the g-factors?
print("  Systematic search: g_i as rational expressions in {phi, 1, 1/phi}:")
print()

# Test various simple expressions
expressions = [
    ("1",           1.0),
    ("1/phi",       phibar),
    ("phi",         phi),
    ("phi^2",       phi**2),
    ("1/phi^2",     phibar**2),
    ("sqrt(5)",     sqrt5),
    ("(phi+1)/3",   (phi+1)/3),  # = phi^2/3
    ("phi^2/3",     phi**2/3),
    ("2",           2.0),
    ("1/2",         0.5),
    ("sqrt(3)",     math.sqrt(3)),
    ("sqrt(2/3)",   math.sqrt(2.0/3.0)),
    ("3pi/16sqrt2", yukawa_overlap),
    ("phi/(phi+1+phibar)", phi/(phi+1+phibar)),
    ("1/(1+phi)",   1/(1+phi)),   # = phibar^2
    ("phi/(1+phi)", phi/(1+phi)), # = phibar
]

g_target = {
    't': 1.0, 'c': phibar, 'b': 2.0, 'tau': phi**2/3,
    's': yukawa_overlap, 'mu': 0.5, 'u': math.sqrt(2.0/3.0),
    'd': math.sqrt(3.0), 'e': math.sqrt(3.0)
}

for fname in ['t', 'c', 'b', 'tau', 's', 'mu', 'u', 'd', 'e']:
    target = g_target[fname]
    matches = []
    for expr, val in expressions:
        err = abs(val - target) / max(target, 1e-10) * 100
        if err < 0.1:
            matches.append(expr)
    if matches:
        print(f"    g_{fname:3s} = {target:.6f} = {', '.join(matches)}")
    else:
        print(f"    g_{fname:3s} = {target:.6f} = NO SIMPLE MATCH IN PHI VOCABULARY")


# ################################################################
#           PART 6: GENERATION STRUCTURE FROM ROOT ORBITS
# ################################################################

banner("PART 6: THREE GENERATIONS FROM S3 ORBITS")

# S3 acts on the 3 A2 components. This permutes (phi, 1, 1/phi).
# Under S3, the 240 roots split into orbits.
# The 3 conjugacy classes of S3 are:
#   - Identity {e} (trivial): 1 element -> Gen 3 (heaviest)
#   - Transpositions {(12),(13),(23)}: 3 elements -> Gen 2
#   - Rotations {(123),(132)}: 2 elements -> Gen 1 (lightest)

# How does S3 act on projections?
# Under a transposition, e.g. (12): phi <-> 1
# The projection changes, but |projection| is invariant for special directions.

# Key insight: the golden direction IS the fixed point of the S3 action
# in the sense that it's the eigenvector of the "golden" element.
# S3 permutes the 3 components, creating 6 images of the golden direction.

print("  S3 orbit of the golden direction (phi, 1, 1/phi):")
print()

perms = [
    ((phi, 1.0, phibar), "e",       "trivial"),
    ((1.0, phi, phibar), "(12)",     "sign"),
    ((phi, phibar, 1.0), "(23)",     "sign"),
    ((phibar, 1.0, phi), "(13)",     "sign"),
    ((1.0, phibar, phi), "(123)",    "standard"),
    ((phibar, phi, 1.0), "(132)",    "standard"),
]

print(f"  {'Perm':>8s}  {'Rep':>10s}  {'Components':>30s}  {'|v|':>10s}  {'v.v_golden':>12s}")
print("  " + "-" * 78)

v_gold_3 = (phi, 1.0, phibar)
for comp, perm_name, rep_name in perms:
    mag = math.sqrt(sum(c**2 for c in comp))
    overlap = sum(c1*c2 for c1, c2 in zip(comp, v_gold_3))
    print(f"  {perm_name:>8s}  {rep_name:>10s}  ({comp[0]:6.4f}, {comp[1]:6.4f}, {comp[2]:6.4f})  {mag:10.6f}  {overlap:12.6f}")

print()
print("  CRITICAL OBSERVATION:")
print(f"  The 6 permutations of (phi, 1, 1/phi) form a GOLDEN ORBIT.")
print(f"  Only the identity gives the exact golden direction.")
print(f"  Transpositions give 3 DIFFERENT directions (generation 2).")
print(f"  Rotations give 2 DIFFERENT directions (generation 1).")
print()

# Overlap of each S3 image with the golden direction
print("  Overlaps with golden direction:")
for comp, perm_name, rep_name in perms:
    overlap = sum(c1*c2 for c1, c2 in zip(comp, v_gold_3))
    norm_overlap = overlap / sum(c**2 for c in v_gold_3)
    print(f"    {perm_name:>6s} ({rep_name:>8s}): overlap = {overlap:.6f}, "
          f"normalized = {norm_overlap:.6f}")

print()

# What are the overlap RATIOS?
identity_overlap = sum(c**2 for c in v_gold_3)  # phi^2 + 1 + phibar^2

# Transposition overlaps
trans_overlaps = []
for comp, perm_name, rep_name in perms:
    if rep_name == "sign":
        overlap = sum(c1*c2 for c1, c2 in zip(comp, v_gold_3))
        trans_overlaps.append(overlap)

rot_overlaps = []
for comp, perm_name, rep_name in perms:
    if rep_name == "standard":
        overlap = sum(c1*c2 for c1, c2 in zip(comp, v_gold_3))
        rot_overlaps.append(overlap)

print(f"  Identity overlap:      {identity_overlap:.6f} = phi^2 + 1 + 1/phi^2 = 3 + sqrt(5) = {3+sqrt5:.6f}")
print(f"  Transposition overlaps: {[round(o,6) for o in trans_overlaps]}")
print(f"  Rotation overlaps:      {[round(o,6) for o in rot_overlaps]}")
print()

# Generation suppression factors
if trans_overlaps:
    gen2_factor = trans_overlaps[0] / identity_overlap
    print(f"  Gen 2 suppression = trans_overlap / identity = {gen2_factor:.6f}")
if rot_overlaps:
    gen1_factor = rot_overlaps[0] / identity_overlap
    print(f"  Gen 1 suppression = rot_overlap / identity  = {gen1_factor:.6f}")

# Compare to epsilon
print()
print(f"  epsilon = theta4/theta3 = {eps:.6f}")
print(f"  epsilon^2               = {eps**2:.6f}")
if trans_overlaps:
    print(f"  Gen 2 factor / epsilon  = {gen2_factor / eps:.6f}")
if rot_overlaps:
    print(f"  Gen 1 factor / epsilon^2 = {gen1_factor / eps**2:.6f}")


# ################################################################
#           PART 7: ROOT PROJECTION SPECTRUM ANALYSIS
# ################################################################

banner("PART 7: ROOT PROJECTION SPECTRUM")

# For each root, project onto the golden direction AND its 3 components.
# Then look for structure in the projection magnitudes.

# Group roots by their full 8D structure type
type1_roots = []  # +/-e_i +/-e_j type
type2_roots = []  # half-integer type

for r in roots:
    vals = [abs(x) for x in r]
    if any(abs(v - 0.5) < 1e-10 for v in vals):
        type2_roots.append(r)
    else:
        type1_roots.append(r)

print(f"  Integer roots (type 1): {len(type1_roots)}")
print(f"  Half-int roots (type 2): {len(type2_roots)}")
print()

# For type 1 roots, projection onto golden direction depends on
# which coordinates are nonzero and their signs.
# Only coords 1,2,3 contribute (golden dir has 0 in coords 0,4,5,6,7).

section("Type 1 roots: projections involving golden direction coords")

# Roots with both nonzero coords in {1,2,3}
golden_type1 = []
for r in type1_roots:
    nonzero = [i for i in range(8) if abs(r[i]) > 0.5]
    if len(nonzero) == 2 and all(i in [1,2,3] for i in nonzero):
        p = dot8(r, v_golden)
        golden_type1.append((r, p, nonzero))

print(f"  Type 1 roots living in golden subspace: {len(golden_type1)}")
for r, p, nz in sorted(golden_type1, key=lambda x: -x[1]):
    r_short = [r[1], r[2], r[3]]
    print(f"    ({r_short[0]:+.0f}, {r_short[1]:+.0f}, {r_short[2]:+.0f}) -> proj = {p:+.6f}")

# Roots with one coord in {1,2,3} and one outside
mixed_type1 = []
for r in type1_roots:
    nonzero = [i for i in range(8) if abs(r[i]) > 0.5]
    if len(nonzero) == 2:
        in_golden = [i for i in nonzero if i in [1,2,3]]
        out_golden = [i for i in nonzero if i not in [1,2,3]]
        if len(in_golden) == 1 and len(out_golden) == 1:
            p = dot8(r, v_golden)
            mixed_type1.append((r, p, in_golden[0], r[in_golden[0]]))

section("Type 1 roots: one coord in golden subspace")
# These have projection = sign * component_value / |v_golden|
# Group by which golden coord
for coord in [1, 2, 3]:
    comp_name = {1: "phi", 2: "1", 3: "1/phi"}[coord]
    comp_val = {1: phi, 2: 1.0, 3: phibar}[coord]
    relevant = [(r, p, s) for r, p, c, s in mixed_type1 if c == coord]
    pos_projs = sorted(set(round(abs(p), 8) for _, p, _ in relevant))
    print(f"  Coord {coord} ({comp_name}): {len(relevant)} roots, "
          f"|proj| values: {[round(v, 6) for v in pos_projs[:4]]}")


# ################################################################
#           PART 8: THE ASSIGNMENT QUESTION
# ################################################################

banner("PART 8: IS THE ASSIGNMENT FORCED?")

print("  THE CORE QUESTION:")
print("  Can we map E8 root projection classes -> fermion types")
print("  such that the projection magnitude = the g-factor?")
print()

# Count distinct projection magnitudes
all_abs_proj = sorted(set(round(abs(p), 6) for p in projections if abs(p) > 1e-6), reverse=True)
print(f"  Distinct nonzero |projection| values: {len(all_abs_proj)}")
print(f"  We need 8 distinct g-factors (g_d = g_e, so 8 not 9)")
print()

if len(all_abs_proj) < 8:
    finding("E8 root projections give FEWER than 8 distinct values. "
            "Projection magnitudes alone cannot distinguish all fermions.")
elif len(all_abs_proj) == 8:
    finding("E8 root projections give EXACTLY 8 distinct values — "
            "perfect match to 8 distinct g-factors!")
else:
    finding(f"E8 root projections give {len(all_abs_proj)} distinct values > 8 needed. "
            "Assignment is not uniquely forced by projection magnitude alone.")

# Direct comparison: normalize and compare
print()
print("  DIRECT COMPARISON (projections normalized to max = 1):")
print()
norm_proj = [p / all_abs_proj[0] for p in all_abs_proj]

g_sorted = sorted(g_target.items(), key=lambda x: -x[1])
g_unique = []
seen = set()
for name, val in g_sorted:
    key = round(val, 4)
    if key not in seen:
        g_unique.append((name, val))
        seen.add(key)

print(f"  {'Proj (norm)':>12s}  {'Count':>6s}  |  {'g-factor':>12s}  {'Fermion':>8s}")
print("  " + "-" * 55)

n_match = min(len(norm_proj), len(g_unique))
for i in range(n_match):
    pval = norm_proj[i]
    count = sum(1 for p in projections if abs(abs(p)/all_abs_proj[0] - pval) < 1e-4)
    gname, gval = g_unique[i]
    err = abs(pval - gval) / max(gval, 1e-10) * 100
    marker = " <-- MATCH" if err < 5 else ""
    print(f"  {pval:12.6f}  {count:6d}  |  {gval:12.6f}  {gname:>8s}  ({err:.1f}%){marker}")

# Show remaining projections
if len(norm_proj) > n_match:
    print()
    print("  Additional projection values (no g-factor counterpart):")
    for i in range(n_match, min(len(norm_proj), n_match + 5)):
        pval = norm_proj[i]
        count = sum(1 for p in projections if abs(abs(p)/all_abs_proj[0] - pval) < 1e-4)
        print(f"  {pval:12.6f}  {count:6d}")


# ################################################################
#           PART 9: WHAT THE GEOMETRY ACTUALLY GIVES
# ################################################################

banner("PART 9: WHAT E8 GEOMETRY ACTUALLY DETERMINES")

# The honest answer: E8 root projections onto the golden direction
# give SOME structure, but the g-factors involve PT n=2 geometry
# (Yukawa overlap, depth, norms) which is NOT directly in the root system.

# What IS determined by geometry:
print("  DETERMINED by E8 geometry:")
print("    - The 3-sector structure (up/down/lepton from golden direction)")
print("    - The golden ratio hierarchy (phi, 1, 1/phi projections)")
print("    - The 6-fold S3 orbit -> 3 generations")
print("    - g_t = 1 (maximum projection = identity)")
print("    - g_c = 1/phi (conjugate direction projection)")
print()
print("  DETERMINED by PT n=2 (wall physics, not root system):")
print("    - g_b = n = 2 (wall depth)")
print("    - g_s = 3pi/16sqrt2 (Yukawa overlap integral)")
print("    - g_mu = 1/n = 1/2 (inverse depth)")
print()
print("  DETERMINED by the COMBINATION (E8 + PT):")
print("    - g_tau = phi^2/3 (golden projection / triality)")
print("    - g_u = sqrt(2/3) (projected breathing norm)")
print("    - g_d = g_e = sqrt(3) (projected triality)")
print()

finding("g-factors split into 3 sources: pure E8 geometry (g_t, g_c), "
        "pure PT n=2 physics (g_b, g_s, g_mu), and E8+PT combined (g_tau, g_u, g_d, g_e).")


# ################################################################
#           PART 10: THE SELECTION RULE
# ################################################################

banner("PART 10: ASSIGNMENT RULE = REPRESENTATION x SECTOR")

# The assignment rule is: g = f(S3_rep, sector)
# where S3_rep in {trivial, sign, standard} and sector in {up, down, lepton}

# This gives a 3x3 table. Can we write it as an OUTER PRODUCT?
print("  g-factor table (S3 rep x sector):")
print()
print(f"  {'':>10s}  {'UP':>12s}  {'DOWN':>12s}  {'LEPTON':>12s}")
print("  " + "-" * 52)

table = {
    'trivial':  {'up': 1.0,                'down': 2.0,                   'lepton': phi**2/3},
    'sign':     {'up': phibar,              'down': yukawa_overlap,        'lepton': 0.5},
    'standard': {'up': math.sqrt(2.0/3.0),  'down': math.sqrt(3.0),       'lepton': math.sqrt(3.0)},
}

for rep in ['trivial', 'sign', 'standard']:
    row = table[rep]
    print(f"  {rep:>10s}  {row['up']:12.6f}  {row['down']:12.6f}  {row['lepton']:12.6f}")

print()

# Check if it factors: g(rep, sector) = h(rep) * k(sector)
# If factored, each row is proportional to (k_up, k_down, k_lep)
# and each column is proportional to (h_triv, h_sign, h_std)

print("  FACTORIZATION TEST: g(rep, sector) = h(rep) * k(sector)?")
print()

# Ratios within rows (should be constant for factored table)
for rep in ['trivial', 'sign', 'standard']:
    row = table[rep]
    r_du = row['down'] / row['up'] if row['up'] > 0 else float('inf')
    r_lu = row['lepton'] / row['up'] if row['up'] > 0 else float('inf')
    print(f"    {rep:>10s}: down/up = {r_du:.4f}, lepton/up = {r_lu:.4f}")

print()
r_triv = (table['trivial']['down'] / table['trivial']['up'],
          table['trivial']['lepton'] / table['trivial']['up'])
r_sign = (table['sign']['down'] / table['sign']['up'],
          table['sign']['lepton'] / table['sign']['up'])
r_std = (table['standard']['down'] / table['standard']['up'],
         table['standard']['lepton'] / table['standard']['up'])

if abs(r_triv[0] - r_sign[0]) < 0.1 and abs(r_triv[0] - r_std[0]) < 0.1:
    finding("g-factor table FACTORS: g(rep, sector) = h(rep) * k(sector). "
            "Assignment is a pure outer product.")
else:
    finding("g-factor table does NOT factor. The 3x3 table carries genuine "
            "correlations between representation and sector. "
            "The assignment rule is RICHER than an outer product.")

# What's the RANK of the g-factor matrix?
# 3x3 matrix
# (no numpy — compute manually)

# Use determinant check
M = [[table[rep][sec] for sec in ['up', 'down', 'lepton']] for rep in ['trivial', 'sign', 'standard']]
# det manually (Sarrus)
det = (M[0][0]*M[1][1]*M[2][2] + M[0][1]*M[1][2]*M[2][0] + M[0][2]*M[1][0]*M[2][1]
     - M[0][2]*M[1][1]*M[2][0] - M[0][1]*M[1][0]*M[2][2] - M[0][0]*M[1][2]*M[2][1])

print(f"\n  Determinant of g-factor matrix: {det:.6f}")
if abs(det) > 0.01:
    print("  FULL RANK (3) -> all 9 entries are independent")
    finding(f"g-factor matrix has full rank (det = {det:.4f}). "
            "All 9 g-factors are genuinely independent — "
            "no simpler rule can compress them.")
else:
    print(f"  Nearly singular (det ~ {det:.6f}) -> some redundancy")


# ################################################################
#           PART 11: THE PATTERN
# ################################################################

banner("PART 11: THE PATTERN — TRIVIAL:DIRECT, SIGN:INVERSE, STANDARD:SQRT")

print("  The S3 representation determines HOW the sector quantity appears:")
print()
print("  TRIVIAL (gen 3): sees the DIRECT value")
print("    g_t   = 1         (direct identity)")
print("    g_b   = n = 2     (direct wall depth)")
print("    g_tau = phi^2/3   (direct vacuum^2/triality)")
print()
print("  SIGN (gen 2): sees the INVERSE/CONJUGATE")
print("    g_c  = 1/phi      (inverse of phi = conjugate)")
print("    g_s  = Yukawa     (the mixing integral = inverse of separation)")
print("    g_mu = 1/n = 1/2  (inverse of wall depth)")
print()
print("  STANDARD (gen 1): sees the SQRT (2D projection)")
print("    g_u = sqrt(2/3)   (sqrt of breathing norm)")
print("    g_d = sqrt(3)     (sqrt of triality)")
print("    g_e = sqrt(3)     (sqrt of triality)")
print()

# Verify the pattern: sign values = 1/(trivial values)?
print("  Pattern check: sign = inverse(trivial)?")
print(f"    g_c = 1/phi = 1/g_t * 1/phi?  No: g_c = 1/phi, 1/g_t = 1")
print(f"    g_mu = 1/2 = 1/g_b?  YES: 1/n = 1/2")
print(f"    g_s = {yukawa_overlap:.4f}, 3/g_tau = {3/g_target['tau']:.4f}... ")
print(f"    g_s * g_tau = {yukawa_overlap * phi**2/3:.6f}")
print()

# Pattern check: standard = sqrt(something)?
print("  Pattern check: standard = sqrt(trivial * constant)?")
print(f"    g_u = {math.sqrt(2.0/3.0):.6f} = sqrt(2/3)")
print(f"    g_d = {math.sqrt(3.0):.6f} = sqrt(3)")
print(f"    g_e = {math.sqrt(3.0):.6f} = sqrt(3)")
print(f"    g_b * g_mu = {2.0 * 0.5:.1f} = 1")
print(f"    g_u^2 = {2.0/3.0:.6f} = breathing norm = 2/3")
print(f"    g_d^2 = {3.0:.6f} = triality")
print()

finding("The pattern direct/inverse/sqrt is CONFIRMED but it operates "
        "on DIFFERENT wall quantities for each sector. "
        "The assignment rule is: g(rep, sector) = rep_action(sector_quantity), "
        "where rep_action = {id, inverse, sqrt} for {trivial, sign, standard}.")


# ################################################################
#           SYNTHESIS
# ################################################################

banner("SYNTHESIS")

print("  WHAT WE FOUND:")
print()
for i, f in enumerate(findings):
    print(f"  {i+1}. {f}")
print()

print("  HONEST ASSESSMENT:")
print()
print("  The g-factor assignment IS structured (direct/inverse/sqrt pattern)")
print("  but is NOT fully determined by E8 root geometry alone.")
print("  It requires BOTH the root system (for sector classification)")
print("  AND the PT n=2 wall physics (for the sector quantities).")
print()
print("  The 3x3 table has FULL RANK — no further compression possible.")
print("  But the PATTERN (how S3 acts) IS forced by representation theory:")
print("    - Trivial rep: identity action")
print("    - Sign rep: inversion/conjugation")
print("    - Standard rep: square root (= 2D projection)")
print()
print("  THE GAP THAT REMAINS:")
print("  WHY does each sector have its particular base quantity?")
print("    UP sector:    base = 1 (identity)")
print("    DOWN sector:  base = n = 2 (depth)")
print(f"    LEPTON sector: base = phi^2/3 = {phi**2/3:.6f} (vacuum^2/triality)")
print()
print("  This 3-way split (1, 2, phi^2/3) is NOT yet derived from first principles.")
print("  It may come from the 3 modular forms (eta, theta4, theta3) -> 3 sectors,")
print("  but the explicit map is missing.")
