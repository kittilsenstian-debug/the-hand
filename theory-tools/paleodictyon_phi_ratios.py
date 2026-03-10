#!/usr/bin/env python3
"""
paleodictyon_phi_ratios.py — Check Paleodictyon dimensions for golden ratio
=============================================================================

All published dimensional data checked against phi = 1.6180339887...
and related constants (1/phi, phi^2, sqrt(5), sqrt(3), etc.)

Author: Claude (Feb 27, 2026)
"""

import math
import sys

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

phi = (1 + math.sqrt(5)) / 2
phibar = phi - 1  # = 1/phi = 0.6180339887
sqrt5 = math.sqrt(5)
sqrt3 = math.sqrt(3)
PI = math.pi

SEP = "=" * 72
SUBSEP = "-" * 55

print(SEP)
print("PALEODICTYON DIMENSIONS: PHI RATIO SEARCH")
print(SEP)
print()

# ============================================================
# ALL PUBLISHED DIMENSIONS (from compiled data)
# ============================================================
print("PART 1: ALL KNOWN DIMENSIONS")
print(SUBSEP)
print()

# Key measurements from Rona et al. 2009, CCZ study, Bohringer et al. 2021,
# Nature Sci Rep 2023 (subarctic), Uchman 2003, CFD analysis 2022

dims = {
    # From PALEODICTYON-ANALYSIS.md and Paleodictyon.md
    "specimen_diameter_min_cm": 2.4,
    "specimen_diameter_max_cm": 7.5,
    "mesh_element_min_cm": 1.0,
    "mesh_element_max_cm": 3.0,
    "mesh_typical_cm": 1.5,        # most common value cited
    "surface_hole_diameter_mm": 1.0,
    "vertical_shaft_diameter_mm": 1.0,
    "vertical_shaft_length_mm": 2.5,  # "2-3 mm" -> midpoint
    "tunnel_depth_below_surface_mm": 2.5,  # "2-3 mm below surface"
    "ridge_rim_height_mm": 2.5,     # "2-3 mm high"
    "central_mound_height_mm": 4.5, # "up to 4-5 mm"
    "holes_per_unit_min": 18,
    "holes_per_unit_max": 24,
    "vertex_angle_deg": 120,

    # CCZ specimens (Marine Biodiversity 2017)
    "ccz_mean_diameter_mm": 45,
    "ccz_std_diameter_mm": 16,

    # Giant fossil specimens
    "fossil_mesh_max_cm": 13,
    "fossil_coverage_max_m2": 0.5,

    # CFD analysis (2022) - optimized mound
    "optimal_mound_height_mm": 4.0,  # "4 mm mound height matches predicted optimum"

    # Number of rows observed
    "rows_min": 2,
    "rows_max": 8,  # estimated from spiral growth description
}

print("  Published measurements:")
print()
for key, val in dims.items():
    unit = key.split("_")[-1]
    name = key.rsplit("_", 1)[0].replace("_", " ")
    print(f"    {name:40s} = {val:8.1f} {unit}")
print()

# ============================================================
# CHECK ALL PAIRWISE RATIOS AGAINST PHI-RELATED CONSTANTS
# ============================================================
print(SEP)
print("PART 2: PAIRWISE RATIO ANALYSIS")
print(SUBSEP)
print()

# Convert everything to mm for comparison
dims_mm = {
    "specimen_diam_min": 24.0,
    "specimen_diam_max": 75.0,
    "mesh_element_min": 10.0,
    "mesh_element_max": 30.0,
    "mesh_typical": 15.0,
    "hole_diameter": 1.0,
    "shaft_diameter": 1.0,
    "shaft_length": 2.5,
    "tunnel_depth": 2.5,
    "ridge_height": 2.5,
    "mound_height": 4.5,
    "mound_optimal": 4.0,
    "ccz_mean_diam": 45.0,
}

# Target ratios to check
targets = {
    "phi": phi,                      # 1.6180
    "1/phi": 1/phi,                  # 0.6180
    "phi^2": phi**2,                 # 2.6180
    "sqrt(5)": sqrt5,               # 2.2361
    "sqrt(3)": sqrt3,               # 1.7321
    "2": 2.0,
    "3": 3.0,
    "phi+1=phi^2": phi + 1,         # 2.6180
    "2*phi": 2*phi,                  # 3.2361
    "phi^3": phi**3,                 # 4.2361
    "1+1/phi": 1 + 1/phi,           # 1.6180 (= phi itself)
    "2+1/phi": 2 + 1/phi,           # 2.6180 (= phi^2)
    "3/phi": 3/phi,                  # 1.8541
    "pi/phi": PI/phi,               # 1.9416
    "phi/2": phi/2,                  # 0.8090
    "sqrt(phi)": math.sqrt(phi),    # 1.2720
}

print("  Checking all dimension pairs against phi-related constants:")
print()
print(f"  {'Ratio':45s} {'Value':>8s} {'Closest':>10s} {'Match':>8s} {'Error':>8s}")
print(f"  {'-'*45} {'-'*8} {'-'*10} {'-'*8} {'-'*8}")

hits = []
keys = list(dims_mm.keys())

for i in range(len(keys)):
    for j in range(len(keys)):
        if i == j:
            continue
        a_name = keys[i]
        b_name = keys[j]
        a_val = dims_mm[a_name]
        b_val = dims_mm[b_name]

        if b_val == 0:
            continue

        ratio = a_val / b_val

        # Find closest target
        best_name = None
        best_err = float('inf')
        for t_name, t_val in targets.items():
            if t_val == 0:
                continue
            err = abs(ratio / t_val - 1)
            if err < best_err:
                best_err = err
                best_name = t_name
                best_val = t_val

        if best_err < 0.05:  # within 5%
            label = f"{a_name} / {b_name}"
            hits.append((label, ratio, best_name, best_val, best_err))

# Sort by error
hits.sort(key=lambda x: x[4])

for label, ratio, target_name, target_val, err in hits:
    pct = err * 100
    star = "***" if pct < 1 else "**" if pct < 2 else "*" if pct < 3 else ""
    print(f"  {label:45s} {ratio:8.4f} {target_name:>10s} {target_val:8.4f} {pct:6.2f}% {star}")

print()

# ============================================================
# SPECIFIC RATIOS TO EXAMINE
# ============================================================
print(SEP)
print("PART 3: SPECIFIC RATIOS OF INTEREST")
print(SUBSEP)
print()

# Key structural ratios
tests = [
    ("specimen/mesh (min/min)", 24/10, "How many mesh elements across?"),
    ("specimen/mesh (max/max)", 75/30, ""),
    ("specimen/mesh (typical)", 45/15, "CCZ mean / typical mesh"),
    ("mesh/shaft_length", 15/2.5, "Mesh spacing / vertical extent"),
    ("mesh/hole_diam", 15/1, "Mesh spacing / hole size"),
    ("mound_height/tunnel_depth", 4.5/2.5, "Vertical profile ratio"),
    ("mound_optimal/tunnel_depth", 4.0/2.5, "CFD optimal / depth"),
    ("shaft_length/hole_diam", 2.5/1.0, "Shaft aspect ratio"),
    ("ccz_diam/ccz_std", 45/16, "Mean/std (normal distribution check)"),
    ("mesh_max/mesh_min", 30/10, "Mesh size range"),
    ("specimen_max/specimen_min", 75/24, "Specimen size range"),
    ("holes_max/holes_min", 24/18, "Hole count range"),
    ("mound/ridge", 4.5/2.5, "Central mound / rim height"),
]

print(f"  {'Ratio':45s} {'Value':>8s}  {'phi?':>8s}  {'1/phi?':>8s}  Notes")
print(f"  {'-'*45} {'-'*8}  {'-'*8}  {'-'*8}  {'-'*25}")

for name, val, note in tests:
    phi_err = abs(val/phi - 1) * 100
    phibar_err = abs(val/phibar - 1) * 100
    phi2_err = abs(val/phi**2 - 1) * 100
    sqrt5_err = abs(val/sqrt5 - 1) * 100
    sqrt3_err = abs(val/sqrt3 - 1) * 100

    best = min(phi_err, phibar_err, phi2_err, sqrt5_err, sqrt3_err)

    flags = ""
    if phi_err < 5: flags += f" phi:{phi_err:.1f}%"
    if phibar_err < 5: flags += f" 1/phi:{phibar_err:.1f}%"
    if phi2_err < 5: flags += f" phi²:{phi2_err:.1f}%"
    if sqrt5_err < 5: flags += f" √5:{sqrt5_err:.1f}%"
    if sqrt3_err < 5: flags += f" √3:{sqrt3_err:.1f}%"

    if not flags:
        flags = " (no phi match)"

    print(f"  {name:45s} {val:8.4f} {flags}  {note}")

print()

# ============================================================
# THE MOUND HEIGHT / DEPTH RATIO
# ============================================================
print(SEP)
print("PART 4: THE MOUND HEIGHT / TUNNEL DEPTH RATIO")
print(SUBSEP)
print()

# Central mound: 4-5 mm (let's use the CFD optimal: 4 mm)
# Tunnel depth: 2-3 mm below surface
# This ratio is the most structurally meaningful

for mound in [4.0, 4.5, 5.0]:
    for depth in [2.0, 2.5, 3.0]:
        ratio = mound / depth
        phi_err = abs(ratio / phi - 1) * 100
        print(f"  mound={mound}mm / depth={depth}mm = {ratio:.4f}  (phi = {phi:.4f}, err = {phi_err:.1f}%)")

print()
print("  BEST MATCH: mound=4mm / depth=2.5mm = 1.6000 (phi err = 1.1%)")
print(f"              mound=5mm / depth=3mm   = {5/3:.4f} (phi err = {abs(5/3/phi-1)*100:.1f}%)")
print()

# ============================================================
# THE 3+1 VERTEX: RATIO OF HORIZONTAL TO VERTICAL
# ============================================================
print(SEP)
print("PART 5: HORIZONTAL vs VERTICAL DIMENSIONS")
print(SUBSEP)
print()

# 3 horizontal tunnels, each ~15mm long to next vertex
# 1 vertical shaft, ~2.5mm long
# Ratio of "horizontal scale" to "vertical scale"

h_scale = 15.0  # mm, typical mesh element (half the distance vertex to vertex)
v_scale = 2.5   # mm, vertical shaft length

ratio_hv = h_scale / v_scale
print(f"  Mesh spacing / shaft length = {h_scale} / {v_scale} = {ratio_hv:.1f}")
print(f"  = 6  (this is just the aspect ratio of the structure)")
print()

# But the HALF-mesh (distance from vertex to center of hex) vs shaft
half_mesh = h_scale / sqrt3  # for regular hexagon, center-to-vertex = side/sqrt(3)
# Actually for hexagon with edge a: center-to-vertex = a, center-to-edge = a*sqrt(3)/2
# If mesh spacing = distance between parallel edges = a*sqrt(3), then a = mesh/sqrt(3)
a_hex = 15.0 / sqrt3  # edge length
center_to_vertex = a_hex
center_to_edge = a_hex * sqrt3 / 2

print(f"  For hexagonal mesh with spacing {h_scale}mm between parallel edges:")
print(f"    Edge length a = {a_hex:.2f} mm")
print(f"    Center to vertex = {center_to_vertex:.2f} mm")
print(f"    Center to edge midpoint = {center_to_edge:.2f} mm")
print()

ratio_cv = center_to_vertex / v_scale
ratio_ce = center_to_edge / v_scale
print(f"  Center-to-vertex / shaft = {ratio_cv:.4f}")
print(f"    phi^2 = {phi**2:.4f}, err = {abs(ratio_cv/phi**2 - 1)*100:.1f}%")
print()
print(f"  Center-to-edge / shaft = {ratio_ce:.4f}")
print(f"    3 = 3.0000, err = {abs(ratio_ce/3 - 1)*100:.1f}%")
print()

# ============================================================
# SIZE DISTRIBUTION: IS IT LOG-NORMAL WITH PHI PARAMETERS?
# ============================================================
print(SEP)
print("PART 6: CCZ SIZE DISTRIBUTION")
print(SUBSEP)
print()

# CCZ: mean = 45 mm, std = 16 mm
# Coefficient of variation = std/mean
cv = 16.0 / 45.0
print(f"  CCZ specimens: mean = 45 mm, std = 16 mm")
print(f"  Coefficient of variation = {cv:.4f}")
print(f"  1/phi^2 = {1/phi**2:.4f} (err = {abs(cv/(1/phi**2) - 1)*100:.1f}%)")
print(f"  1/sqrt(5) = {1/sqrt5:.4f} (err = {abs(cv/(1/sqrt5) - 1)*100:.1f}%)")
print(f"  1/3 = {1/3:.4f} (err = {abs(cv/(1/3) - 1)*100:.1f}%)")
print()

# Mean/std ratio
ms = 45.0 / 16.0
print(f"  mean/std = {ms:.4f}")
print(f"  phi + 1 = phi^2 = {phi**2:.4f} (err = {abs(ms/phi**2 - 1)*100:.1f}%)")
print(f"  sqrt(8) = {math.sqrt(8):.4f} (err = {abs(ms/math.sqrt(8) - 1)*100:.1f}%)")
print()

# ============================================================
# HOLE COUNT AND HEXAGONAL NUMBERS
# ============================================================
print(SEP)
print("PART 7: HOLE COUNT AND HEXAGONAL GEOMETRY")
print(SUBSEP)
print()

# 18-24 holes per unit
# A hexagonal ring with n shells has 3n(n+1) + 1 vertices
# n=1: 7, n=2: 19, n=3: 37
# Or for peripheral holes only: 6n per ring
# n=1: 6, n=2: 12, n=3: 18, n=4: 24

print("  Holes per unit: 18-24 (observed)")
print()
print("  Hexagonal ring peripheral hole counts:")
for n in range(1, 8):
    peripheral = 6 * n
    cumulative = 3 * n * (n + 1) + 1
    print(f"    Ring {n}: {peripheral} peripheral, {cumulative} cumulative")

print()
print("  18 holes = 3 complete rings of peripheral holes (6+12=18?)")
print("  Actually 18 = 6*3 = ring 3 has 18 peripheral holes")
print("  24 = 6*4 = ring 4 has 24 peripheral holes")
print()
print("  Or: the 18-24 range spans rings 3 to 4.")
print("  Cumulative vertices: ring 2 = 19, ring 3 = 37")
print("  19 is close to 18... could be n=2 hexagonal number - 1")
print()

# Check if 18/24 ratio is interesting
r_holes = 24/18
print(f"  24/18 = {r_holes:.4f}")
print(f"  4/3 = {4/3:.4f} (EXACT)")
print(f"  This is just 24/18 = 4/3. Not phi-related.")
print()

# ============================================================
# THE KEY RATIO: MOUND-TO-DEPTH
# ============================================================
print(SEP)
print("PART 8: THE ONE PROMISING RATIO")
print(SUBSEP)
print()

print("  The CFD analysis (2022) found that the 4mm mound height")
print("  is the OPTIMAL value — not a random measurement.")
print("  It balances ventilation efficiency and erosion resistance.")
print()
print("  The tunnel depth (2-3mm) is set by the sediment physics.")
print()
print("  So the ratio mound_height / tunnel_depth is FUNCTIONAL,")
print("  not arbitrary. It's the aspect ratio that WORKS BEST.")
print()

# The real question: does the optimal aspect ratio = phi?
mound = 4.0  # mm (CFD optimal)
depth_range = [2.0, 2.5, 3.0]  # mm

for d in depth_range:
    r = mound / d
    print(f"  {mound}mm / {d}mm = {r:.4f}  ", end="")
    if abs(r/phi - 1) < 0.02:
        print(f"*** WITHIN 2% OF PHI ({phi:.4f}) ***")
    elif abs(r/phi - 1) < 0.05:
        print(f"** within 5% of phi **")
    else:
        print(f"(phi err = {abs(r/phi - 1)*100:.1f}%)")

print()
print("  BUT: this depends on whether tunnel depth is 2.0 or 2.5 or 3.0 mm.")
print("  The published data gives '2-3 mm' — not precise enough to confirm phi.")
print()
print("  TO CONFIRM: need precise measurement of mound height and tunnel depth")
print("  on the same specimen. If mound/depth = 1.618 +/- 0.05, that's significant.")
print()

# ============================================================
# SPECIMEN/MESH SIZE RATIO
# ============================================================
print(SEP)
print("PART 9: SPECIMEN SIZE / MESH SIZE")
print(SUBSEP)
print()

# If the specimen grows outward in rings, and the number of rings
# determines the specimen size, then specimen/mesh should be
# an integer or relate to the growth law

# Typical specimen: 45mm diameter (CCZ mean)
# Typical mesh: 15mm
# Ratio = 3
# For the range: 24-75mm / 10-30mm

print("  CCZ mean diameter / typical mesh = 45 / 15 = 3.0")
print("  Specimen range: 24-75mm, mesh range: 10-30mm")
print()
print("  This ratio (3) is the NUMBER OF MESH ROWS across the specimen.")
print("  The spiral growth adds rows one at a time from center.")
print()

# Check if the growth follows a Fibonacci/golden spiral
print("  If growth follows golden spiral:")
print("  After n additions, radius ~ phi^n (in mesh units)")
print()
for n in range(1, 8):
    radius = phi**n
    diameter = 2 * radius * 15  # in mm, using 15mm mesh
    print(f"    n={n}: radius = {radius:.2f} mesh units = {radius*15:.0f} mm diam = {2*radius*15:.0f} mm")

print()
print("  Observed range 24-75 mm corresponds to n ~ 1-2 mesh radii")
print("  Not enough data to distinguish golden spiral from simple linear growth.")
print()

# ============================================================
# OVERALL ASSESSMENT
# ============================================================
print(SEP)
print("OVERALL ASSESSMENT")
print(SEP)
print()

print("  PROMISING:")
print("  1. Mound height / tunnel depth ~ 1.6 (within 1-5% of phi,")
print("     depending on exact depth measurement)")
print("     BUT: measurement precision insufficient (reported as ranges)")
print()
print("  2. Specimen max/min = 75/24 = 3.125 ~ phi^2/sqrt(phi)?")
print("     No — this is just biological variation. NOT convincing.")
print()
print("  NOT PHI-RELATED:")
print("  3. Mesh spacing ~ 1-3 cm: matches Benard scaling (2 x layer depth)")
print("  4. Hole count 18-24: just ring geometry (6n for n=3,4)")
print("  5. Vertex angle 120°: standard hexagonal, not phi-specific")
print("  6. CCZ CV = 0.356: not close to any phi constant")
print()
print("  WHAT WOULD BE DECISIVE:")
print("  - Precise measurement of mound_height / tunnel_depth ratio")
print("    on 50+ specimens. If mean = 1.618 +/- 0.03, that's a discovery.")
print("  - Mesh spacing / oxygen_penetration_depth ratio.")
print("    If it's phi, the mesh is sized by the domain wall, not Benard.")
print("  - Growth spiral pitch. If golden spiral, not Archimedean, that's")
print("    strong evidence for phi in the growth law.")
print()
print("  HONEST CONCLUSION:")
print("  The existing published data is TOO IMPRECISE to confirm or deny")
print("  phi ratios. Measurements are reported as ranges ('2-3 mm', '1-2 cm'),")
print("  not as precise values with error bars. The one promising ratio")
print("  (mound/depth ~ 1.6) is tantalizing but inconclusive.")
print()
print("  NEEDED: A dedicated morphometric study of 50+ specimens")
print("  measuring mound height, tunnel depth, mesh spacing, hole diameter,")
print("  shaft length, and spiral pitch to 0.1mm precision.")
print("  This data may already exist in Rona's unpublished ROV surveys.")
print()
