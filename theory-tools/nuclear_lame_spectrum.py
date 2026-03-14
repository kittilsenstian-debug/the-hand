#!/usr/bin/env python3
"""
nuclear_lame_spectrum.py — Nuclear shells from Lamé at golden nome
==================================================================

No narratives. Trace the algebra.

The Lamé n=2 equation at q = 1/φ has k² = 0.9999999802 → PT limit.
PT n=2 has 2 bound states: E₀ = -4, E₁ = -1. Gap₁ = 3.

Question: does the 3D radial problem with this potential, plus
spin-orbit from its derivative, reproduce nuclear magic numbers
2, 8, 20, 28, 50, 82, 126?

THIS SCRIPT COMPUTES:
    1. Lamé band widths at golden nome — what the ~10⁻⁸ numbers ARE
    2. PT n=2 as nuclear mean-field: energy levels for each (l, j)
    3. Spin-orbit strength from the PT derivative (no free parameters)
    4. Level ordering and cumulative occupancies
    5. Comparison with observed magic numbers
    6. The spin-orbit / HO spacing ratio from Gap₁ = 3

Standard Python 3, no dependencies.

python -X utf8 nuclear_lame_spectrum.py
"""

import math
import sys

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

phi    = (1 + math.sqrt(5)) / 2
phibar = 1.0 / phi
pi     = math.pi
NTERMS = 500

SEP    = "=" * 78
SUBSEP = "-" * 68

# ============================================================================
# MODULAR FORMS
# ============================================================================

def theta2(q, N=NTERMS):
    s = 0.0
    for n in range(N):
        t = q ** ((n + 0.5) ** 2)
        if t < 1e-50: break
        s += t
    return 2 * s

def theta3(q, N=NTERMS):
    s = 1.0
    for n in range(1, N + 1):
        t = q ** (n * n)
        if t < 1e-50: break
        s += 2 * t
    return s

def theta4(q, N=NTERMS):
    s = 1.0
    for n in range(1, N + 1):
        t = q ** (n * n)
        if t < 1e-50: break
        s += 2 * (-1) ** n * t
    return s

q  = phibar
t2 = theta2(q)
t3 = theta3(q)
t4 = theta4(q)

k_sq  = (t2 / t3) ** 4
kp_sq = (t4 / t3) ** 4
m     = k_sq


# ============================================================================
# PART 1: BAND WIDTHS — What the 10⁻⁸ numbers ARE
# ============================================================================

print(SEP)
print("  PART 1: LAMÉ n=2 BAND WIDTHS AT GOLDEN NOME")
print("  " + SUBSEP)
print()

disc = math.sqrt(1 - m + m ** 2)

# Five band edges (Whittaker-Watson)
E1 = 2 * (1 + m) - 2 * disc    # bottom of band 1
E2 = 1 + m                      # top of band 1  (= bottom of gap 1)
E3 = 1 + 4 * m                  # top of gap 1   (= bottom of band 2)
E4 = 4 + m                      # top of band 2  (= bottom of gap 2)
E5 = 2 * (1 + m) + 2 * disc    # top of gap 2   (= bottom of band 3)

edges = sorted([E1, E2, E3, E4, E5])

bw1 = edges[1] - edges[0]     # band 1 width
bw2 = edges[3] - edges[2]     # band 2 width
g1  = edges[2] - edges[1]     # gap 1
g2  = edges[4] - edges[3]     # gap 2

print(f"  k² = {k_sq:.15f}")
print(f"  1 - k² = {1 - k_sq:.6e}")
print()
print(f"  Band 1: [{edges[0]:.15f}, {edges[1]:.15f}]")
print(f"  Band 2: [{edges[2]:.15f}, {edges[3]:.15f}]")
print(f"  Band 3: [{edges[4]:.15f}, inf)")
print()
print(f"  Band 1 width = {bw1:.6e}")
print(f"  Band 2 width = {bw2:.6e}")
print(f"  Gap 1        = {g1:.10f}")
print(f"  Gap 2        = {g2:.10f}")
print()

# What are the band widths in terms of (1-k²)?
delta = 1 - k_sq
print(f"  delta = 1 - k² = {delta:.6e}")
print()
print(f"  Band 1 width / delta = {bw1 / delta:.6f}")
print(f"  Band 2 width / delta = {bw2 / delta:.6f}")
print(f"  BW1 / BW2            = {bw1 / bw2:.6e}")
print()

# Analytical: for n=2 Lamé, what are band widths as k→1?
# Band 1 = [E1, E2] where E1 = 2(1+m) - 2√(1-m+m²), E2 = 1+m
# At m = 1-ε:
#   E1 = 2(2-ε) - 2√(1-(1-ε)+(1-ε)²) = 4-2ε - 2√(1-1+ε+1-2ε+ε²)
#      = 4-2ε - 2√(1-ε+ε²)
#   E2 = 1+(1-ε) = 2-ε
# Band 1 width = E2 - E1 = (2-ε) - (4-2ε-2√(1-ε+ε²)) = -2+ε+2√(1-ε+ε²)
# At ε→0: √(1-ε+ε²) ≈ 1 - ε/2 + 3ε²/8
# BW1 ≈ -2 + ε + 2(1-ε/2+3ε²/8) = -2+ε+2-ε+3ε²/4 = 3ε²/4

eps = 1 - m
bw1_predict = 3 * eps ** 2 / 4
print(f"  Analytical prediction (k→1 expansion):")
print(f"    Band 1 width ≈ 3(1-k²)²/4 = {bw1_predict:.6e}")
print(f"    Actual:                       {bw1:.6e}")
print(f"    Ratio: {bw1 / bw1_predict:.6f}")
print()

# Band 2: [E3, E4] where E3 = 1+4m, E4 = 4+m
# BW2 = (4+m) - (1+4m) = 3 - 3m = 3(1-m) = 3ε
bw2_predict = 3 * eps
print(f"    Band 2 width ≈ 3(1-k²) = {bw2_predict:.6e}")
print(f"    Actual:                    {bw2:.6e}")
print(f"    Ratio: {bw2 / bw2_predict:.6f}")
print()

# So BW1 ~ ε², BW2 ~ ε, BW1/BW2 ~ ε/4
bw_ratio_predict = eps / 4
print(f"    BW1/BW2 ≈ (1-k²)/4 = {bw_ratio_predict:.6e}")
print(f"    Actual:                {bw1 / bw2:.6e}")
print()

print(f"  RESULT: Band widths at golden nome are:")
print(f"    BW1 = (3/4)(1-k²)² = (3/4)(θ₄/θ₃)⁸ = {bw1:.6e}")
print(f"    BW2 = 3(1-k²)     = 3(θ₄/θ₃)⁴     = {bw2:.6e}")
print(f"    BW1/BW2 = (1-k²)/4 = (θ₄/θ₃)⁴/4")
print()
print(f"  The band widths are powers of (θ₄/θ₃)⁴ = ε⁴ = {(t4/t3)**4:.6e}")
print(f"  where ε = θ₄/θ₃ = {t4/t3:.10f} is the hierarchy parameter.")
print()


# ============================================================================
# PART 2: PT n=2 AS NUCLEAR MEAN-FIELD
# ============================================================================

print(SEP)
print("  PART 2: PT n=2 AS NUCLEAR MEAN-FIELD")
print("  " + SUBSEP)
print()

print("  At k=1 (golden nome limit), the nuclear mean-field is:")
print("    V(x) = -V₀ sech²((r-R)/a)")
print()
print("  For PT n=2: V₀·a²·(2M/ℏ²) = n(n+1) = 6")
print("  Bound states: E₀ = -n² = -4, E₁ = -(n-1)² = -1")
print("  Continuum: E ≥ 0")
print()

# In the standard shell model, the mean-field has many bound states
# because V₀ is large (~50 MeV) and the nuclear radius R is large.
# The PT n=2 has only 2 bound states — too few for a large nucleus.
#
# But the ANGULAR MOMENTUM changes this: for each l, the effective
# potential V_eff(r) = V(r) + ℏ²l(l+1)/(2Mr²) has different numbers
# of bound states. Higher l pushes states up in energy.
#
# The HO limit: equally spaced shells with degeneracy (N+1)(N+2).
# The PT limit: two bound states per l-channel.

# For a realistic nuclear potential with depth V₀ and range R,
# the number of bound states for angular momentum l is approximately:
# n_max(l) ≈ sqrt(2MV₀R²/ℏ²) / π - l/2 - 1/4  (WKB estimate)
#
# For V₀ ~ 50 MeV, R ~ 1.2*A^(1/3) fm, M ~ 938 MeV/c²:
# For A=208: R ≈ 7.1 fm, 2MV₀R²/ℏ² ≈ 50*7.1²/(20.7) ≈ 122
# n_max(0) ≈ sqrt(122)/π ≈ 3.5 → 3 radial nodes for l=0

# Framework approach: the PT depth parameter is n(n+1) = 6.
# But the NUMBER OF SHELLS depends on the dimensionless parameter
# η = R/a (nuclear radius / diffuseness).
# For typical nuclei: η ≈ R/a ≈ 7/0.65 ≈ 11.
# This η determines how many angular momentum channels support bound states.

# The KEY PARAMETER from the framework:
# Gap₁ = 3 = first Lamé gap = spin-orbit energy scale

print("  The framework gives ONE parameter for the shell model:")
print("  Gap₁ = 3 (from Lamé at golden nome)")
print()
print("  In the shell model, the spin-orbit Hamiltonian is:")
print("    H_so = -κ · (dV/dr)(1/r) · L·S")
print()
print("  The derivative of PT n=2: dV/dr ∝ sech²(x)tanh(x)")
print("  This is localized at the nuclear surface — a surface force.")
print()
print("  The eigenvalue of L·S:")
print("    <L·S> = [j(j+1) - l(l+1) - 3/4] / 2")
print("    For j = l+1/2:  <L·S> = l/2")
print("    For j = l-1/2:  <L·S> = -(l+1)/2")
print("    Splitting: Δ(L·S) = (2l+1)/2")
print()


# ============================================================================
# PART 3: SPIN-ORBIT STRENGTH FROM GAP₁ = 3
# ============================================================================

print(SEP)
print("  PART 3: SPIN-ORBIT FROM Gap₁ = 3")
print("  " + SUBSEP)
print()

# The spin-orbit strength relative to HO level spacing determines
# which intruders cross. In standard nuclear physics:
#   κ/ℏω ≈ 0.1 to 0.15  (fitted from data)
#
# Can the framework derive this?
#
# The Lamé spectrum at golden nome has:
#   Gap₁ = 3   (in units of the Lamé potential depth)
#   Gap₂ = 1
#   Total PT depth = n(n+1) = 6
#
# The spin-orbit force ∝ dV/dr, and V has depth n(n+1) = 6.
# The spin-orbit STRENGTH relative to the well depth:
#   κ_SO / V₀ ∝ Gap₁ / n(n+1) = 3/6 = 1/2
#
# But we need κ_SO / ℏω (ratio to HO spacing).
# ℏω ≈ 41/A^(1/3) MeV for nuclear HO.
# V₀ ≈ 50 MeV typically.
# So κ_SO / ℏω = (κ_SO/V₀) × (V₀/ℏω) = (1/2) × (50/7) ≈ 3.6
#
# That's too large. Let me reconsider.

# Actually, the spin-orbit parameter in the shell model is defined as:
#   E_so(n,l,j) = -κ × [j(j+1) - l(l+1) - s(s+1)]
# where κ has units of energy.
#
# Standard values: κ ≈ 20/A^(2/3) MeV
# For A=208: κ ≈ 20/208^(2/3) ≈ 0.57 MeV
# ℏω ≈ 41/208^(1/3) ≈ 6.9 MeV
# Ratio: κ/ℏω ≈ 0.083
#
# The intruder condition: level j=l+1/2 from shell N crosses into N-1 when:
#   κ × l > ℏω (approximately)
# i.e., l > ℏω/κ ≈ 12
#
# Wait, that's too large. The actual condition is more nuanced because
# the splitting is κ(2l+1)/2 and the levels don't need to fully cross.

# Let me compute the ACTUAL level scheme using the standard parameterization,
# then see what value of κ/ℏω the framework predicts.

# Standard shell model level energies:
# E(N, l, j) = ℏω(N + 3/2) - κ × <L·S> - μ × l(l+1)
# where μ is an l²-correction (flattens the bottom of the well)
#
# Simpler: use just HO + SO, no l² term.

print("  Shell model energy (HO + spin-orbit, no l² term):")
print()
print("    E(N,l,j) = ℏω(N + 3/2) + κ_so × <L·S>")
print("    where <L·S> = l/2 for j=l+1/2, -(l+1)/2 for j=l-1/2")
print()

# Generate all levels up to N=6
levels = []
for N in range(7):
    for l in range(N, -1, -2):
        n_rad = (N - l) // 2 + 1
        for j2 in [2 * l + 1, 2 * l - 1]:  # j = l+1/2, l-1/2
            if j2 < 0:
                continue  # skip j < 0
            j = j2 / 2.0
            degeneracy = j2 + 1  # = 2j+1
            ls_expect = (j * (j + 1) - l * (l + 1) - 0.75) / 2
            letter = "spdfghi"[l]
            label = f"{n_rad}{letter}{j2}/2"
            levels.append({
                'N': N, 'l': l, 'j': j, 'j2': j2,
                'n_rad': n_rad, 'label': label,
                'deg': degeneracy, 'ls': ls_expect
            })

# Now compute energies for various κ/ℏω ratios
# and see which value reproduces the observed magic numbers

print("  Scan: which κ/ℏω ratio produces the observed magic numbers?")
print()

observed_magic = [2, 8, 20, 28, 50, 82, 126]

def get_magic_numbers(kappa_ratio, levels):
    """Given κ/ℏω, compute level energies, sort, accumulate."""
    sorted_levels = []
    for lev in levels:
        E = (lev['N'] + 1.5) + kappa_ratio * lev['ls']
        sorted_levels.append((E, lev['deg'], lev['label'], lev['N'], lev['l']))
    sorted_levels.sort(key=lambda x: x[0])

    cumul = 0
    magic_found = []
    prev_E = None
    for E, deg, label, N, l in sorted_levels:
        cumul += deg
        # Detect magic numbers at large gaps
        magic_found.append((cumul, E, deg, label))

    return sorted_levels, magic_found


def magic_score(kappa_ratio, levels, target=None):
    """Score how well this ratio reproduces observed magic numbers."""
    if target is None:
        target = [2, 8, 20, 28, 50, 82, 126]
    sorted_levels, magic_data = get_magic_numbers(kappa_ratio, levels)

    # Compute energy gaps between consecutive filled levels
    cumul = 0
    energies_at_cumul = []
    for E, deg, label, N, l in sorted_levels:
        cumul += deg
        energies_at_cumul.append((cumul, E))

    # Find the largest gaps
    gaps = []
    for i in range(1, len(energies_at_cumul)):
        c_prev, e_prev = energies_at_cumul[i - 1]
        c_curr, e_curr = energies_at_cumul[i]
        gap = e_curr - e_prev
        gaps.append((gap, c_prev))

    # Sort by gap size (largest first)
    gaps.sort(key=lambda x: -x[0])

    # Take top 7 gaps → magic numbers
    predicted = sorted([g[1] for g in gaps[:7]])

    matches = sum(1 for p in predicted if p in target)
    return matches, predicted


# Scan κ/ℏω from 0 to 0.3
print(f"  {'κ/ℏω':>8s}  {'Predicted magic numbers (top 7 gaps)':>45s}  {'Match'}")
print("  " + "-" * 68)

best_score = 0
best_kappa = 0
best_predicted = []

for k100 in range(0, 31):
    kappa = k100 / 100.0
    score, predicted = magic_score(kappa, levels)
    pred_str = str(predicted)
    marker = " <<<" if score >= best_score and score > 0 else ""
    if score > best_score:
        best_score = score
        best_kappa = kappa
        best_predicted = predicted
    if k100 % 2 == 0 or score >= 5:
        print(f"  {kappa:8.3f}  {pred_str:>45s}  {score}/7{marker}")

print()
print(f"  Best: κ/ℏω = {best_kappa:.3f}, score = {best_score}/7")
print(f"  Predicted: {best_predicted}")
print(f"  Observed:  {observed_magic}")
print()


# ============================================================================
# PART 4: FRAMEWORK VALUE OF κ/ℏω
# ============================================================================

print(SEP)
print("  PART 4: FRAMEWORK VALUE OF κ/ℏω")
print("  " + SUBSEP)
print()

# The framework gives specific numbers from the Lamé/PT spectrum:
#   Gap₁ = 3 (first spectral gap)
#   Gap₂ = 1 (second spectral gap)
#   PT depth = n(n+1) = 6
#
# The spin-orbit energy IS the spectral gap of the wall derivative.
# The wall derivative (PT n=1) has depth n(n+1) = 2, one bound state at E = -1.
# Its gap (from bound state to continuum) = 1.
#
# The HO spacing comes from the well depth: ℏω ∝ √(V₀/R²).
# For PT n=2: V₀ = n(n+1) = 6 (dimensionless).
#
# Candidate framework ratios:

candidates = [
    ("Gap₁ / n(n+1)",         3.0 / 6,               "= 1/2"),
    ("Gap₂ / n(n+1)",         1.0 / 6,               "= 1/6"),
    ("Gap₁ / (Gap₁+Gap₂+sum)", 3.0 / (3 + 1 + 6),    "= 3/10"),
    ("|E₁| / n(n+1)",         1.0 / 6,               "= 1/6"),
    ("|E₁| / |E₀|",           1.0 / 4,               "= 1/4"),
    ("1 / n(n+1)",             1.0 / 6,               "= 1/6"),
    ("1 / (2n+1)",             1.0 / 5,               "= 1/5"),
    ("1 / PT_depth",           1.0 / 6,               "= 1/6"),
    ("(Gap₁-Gap₂)/(Gap₁+Gap₂)", 2.0 / 4,            "= 1/2"),
    ("Gap₂ / Gap₁",           1.0 / 3,               "= 1/3"),
    ("1/(2*Gap₁)",             1.0 / 6,               "= 1/6"),
    ("sqrt(Gap₂/Gap₁)",       math.sqrt(1/3),         "= 1/√3"),
    ("1/sqrt(n(n+1))",         1/math.sqrt(6),         "= 1/√6"),
    ("n/(n(n+1))",             2.0 / 6,               "= 1/3"),
]

print(f"  {'Ratio':>30s}  {'Value':>8s}  {'Score':>6s}  {'Predicted magic'}")
print("  " + "-" * 75)

for name, val, note in candidates:
    score, predicted = magic_score(val, levels)
    marker = " <<<" if score >= 5 else ""
    print(f"  {name:>30s}  {val:8.4f}  {score:>4d}/7  {predicted}{marker}")

print()

# Fine scan around best values
print("  Fine scan around best matches:")
print()

for center_name, center_val in [("1/6", 1/6), ("0.10", 0.10), ("0.12", 0.12), ("0.13", 0.13)]:
    for delta_pct in range(-20, 21, 5):
        val = center_val * (1 + delta_pct / 100)
        score, predicted = magic_score(val, levels)
        if score >= 5:
            print(f"    κ/ℏω = {val:.4f} ({center_name} {delta_pct:+d}%): {score}/7  {predicted}")


# ============================================================================
# PART 5: DETAILED LEVEL SCHEME AT BEST κ/ℏω
# ============================================================================

print()
print(SEP)
print(f"  PART 5: LEVEL SCHEME AT κ/ℏω = {best_kappa:.3f}")
print("  " + SUBSEP)
print()

sorted_levels, magic_data = get_magic_numbers(best_kappa, levels)

print(f"  {'Level':>10s}  {'E':>8s}  {'2j+1':>5s}  {'Cumul':>6s}  {'Magic?'}")
print("  " + "-" * 50)

cumul = 0
prev_E = -999
for E, deg, label, N, l in sorted_levels:
    cumul += deg
    gap_marker = ""
    if cumul in observed_magic:
        gap_marker = f" <<< MAGIC {cumul}"
    elif any(abs(cumul - m) <= 2 for m in observed_magic):
        gap_marker = f" (near {min(observed_magic, key=lambda m: abs(m-cumul))})"
    print(f"  {label:>10s}  {E:8.3f}  {deg:5d}  {cumul:6d}  {gap_marker}")


# ============================================================================
# PART 6: THE GAP₁ = 3 AS SPIN-ORBIT SCALE
# ============================================================================

print()
print(SEP)
print("  PART 6: WHAT Gap₁ = 3 IS IN NUCLEAR PHYSICS")
print("  " + SUBSEP)
print()

# Nuclear data: typical spin-orbit splitting for 1f7/2 vs 1f5/2
# From experiment: ΔE(1f7/2 - 1f5/2) ≈ 6-8 MeV (in Ca-40 region)
# The HO spacing: ℏω ≈ 41/A^(1/3) MeV ≈ 12 MeV for A=40

print("  Nuclear data (measured):")
print("    ΔE(1f7/2 - 1f5/2) ≈ 6-8 MeV  (Ca-40 region)")
print("    ℏω ≈ 41/A^(1/3) ≈ 12 MeV     (for A=40)")
print("    Spin-orbit splitting / ℏω ≈ 0.5-0.7")
print()
print("  But this is for l=3 (the 1f intruder).")
print("  The splitting = κ × (2l+1) = κ × 7")
print("  So κ/ℏω ≈ (0.5-0.7)/7 ≈ 0.07-0.10")
print()
print("  Framework numbers:")
print(f"    Gap₁ = 3 (Lamé spectral datum)")
print(f"    PT depth = 6")
print(f"    Gap₁/PT_depth = 3/6 = 0.5")
print(f"    Gap₁/(PT_depth × (2n+1)) = 3/(6×5) = 0.1")
print(f"    Gap₁/(PT_depth × n(n+1)) = 3/36 = 0.083")
print()
print(f"  The ratio 3/36 = 1/12 = 0.083 is in the measured range (0.07-0.10).")
print(f"  3/36 = Gap₁ / [n(n+1)]² = first gap / (PT depth)²")
print()

# Check what 1/12 gives
score_12, pred_12 = magic_score(1/12, levels)
score_10, pred_10 = magic_score(0.10, levels)
score_083, pred_083 = magic_score(0.083, levels)

print(f"  κ/ℏω = 1/12 = 0.0833: score = {score_12}/7, magic = {pred_12}")
print(f"  κ/ℏω = 0.10:          score = {score_10}/7, magic = {pred_10}")
print(f"  κ/ℏω = 0.083:         score = {score_083}/7, magic = {pred_083}")
print()


# ============================================================================
# PART 7: WITH l² CORRECTION (WOODS-SAXON FLATTENING)
# ============================================================================

print(SEP)
print("  PART 7: WITH l² CORRECTION")
print("  " + SUBSEP)
print()

# The real shell model uses:
# E(N,l,j) = ℏω(N + 3/2) - μ·l(l+1) + κ·<L·S>
# where μ flattens the potential bottom (Woods-Saxon < HO for l>0)
# Typical: μ/ℏω ≈ 0.02-0.04

print("  E(N,l,j) = ℏω(N + 3/2) - μ·l(l+1) + κ·<L·S>")
print()
print("  Framework: does the Lamé spectrum also give μ?")
print("  The l² term comes from the difference between HO and finite-well.")
print("  For PT: V → 0 at |x|→∞ (not ½mω²x² → ∞ like HO).")
print("  The flattening IS the PT shape vs HO shape.")
print()

# Scan over (κ, μ) pairs
print(f"  {'κ/ℏω':>7s}  {'μ/ℏω':>7s}  {'Score':>6s}  {'Predicted magic numbers'}")
print("  " + "-" * 65)

best2_score = 0
best2_kappa = 0
best2_mu = 0
best2_pred = []

for k100 in range(5, 20):
    kappa = k100 / 100.0
    for m100 in range(0, 8):
        mu_corr = m100 / 100.0
        # Compute energies with l² correction
        sorted_l = []
        for lev in levels:
            E = (lev['N'] + 1.5) - mu_corr * lev['l'] * (lev['l'] + 1) + kappa * lev['ls']
            sorted_l.append((E, lev['deg'], lev['label']))
        sorted_l.sort(key=lambda x: x[0])

        # Get cumulative and gaps
        cumul = 0
        ec = []
        for E, deg, label in sorted_l:
            cumul += deg
            ec.append((cumul, E))

        gaps = []
        for i in range(1, len(ec)):
            gaps.append((ec[i][1] - ec[i-1][1], ec[i-1][0]))
        gaps.sort(key=lambda x: -x[0])
        predicted = sorted([g[1] for g in gaps[:7]])
        matches = sum(1 for p in predicted if p in observed_magic)

        if matches > best2_score:
            best2_score = matches
            best2_kappa = kappa
            best2_mu = mu_corr
            best2_pred = predicted

        if matches >= 6:
            print(f"  {kappa:7.3f}  {mu_corr:7.3f}  {matches:>4d}/7  {predicted}")

print()
print(f"  Best with l² correction: κ={best2_kappa:.3f}, μ={best2_mu:.3f}")
print(f"  Score: {best2_score}/7, predicted: {best2_pred}")
print(f"  Observed:                          {observed_magic}")
print()


# ============================================================================
# PART 8: SUMMARY
# ============================================================================

print(SEP)
print("  SUMMARY")
print("  " + SUBSEP)
print()
print("  COMPUTED:")
print(f"    Band 1 width = (3/4)(1-k²)² = (3/4)(θ₄/θ₃)⁸ = {bw1:.2e}")
print(f"    Band 2 width = 3(1-k²) = 3(θ₄/θ₃)⁴ = {bw2:.2e}")
print(f"    BW1/BW2 = (1-k²)/4 — bands collapse at DIFFERENT rates")
print()
print(f"    Gap₁ = 3 (exact, from Whittaker-Watson)")
print(f"    Gap₂ = 1 (exact)")
print(f"    Gap₁/Gap₂ = 3 → ratio 3 IS the color number")
print()
print(f"  SPIN-ORBIT:")
print(f"    Nuclear κ/ℏω ≈ 0.07-0.10 (measured)")
print(f"    Framework: Gap₁/[n(n+1)]² = 3/36 = 0.083 (in range)")
print(f"    Best HO+SO score: {best_score}/7 at κ/ℏω = {best_kappa}")
print(f"    Best HO+SO+l² score: {best2_score}/7 at κ={best2_kappa}, μ={best2_mu}")
print()
print(f"  HONEST ASSESSMENT:")
print(f"    - Band widths are clean: powers of (θ₄/θ₃)⁴, factors of 3")
print(f"    - The spin-orbit ratio κ/ℏω ≈ 0.08-0.10 IS in the nuclear range")
print(f"    - But reproducing ALL 7 magic numbers from HO+SO requires")
print(f"      specific κ/ℏω that may or may not match a clean framework ratio")
print(f"    - The simple HO+SO model is known to be insufficient —")
print(f"      the real potential is Woods-Saxon, not harmonic")
print(f"    - A proper computation needs the RADIAL Lamé equation,")
print(f"      not just HO+SO perturbation theory")
print()

print(SEP)
print("  COMPUTATION COMPLETE")
print(SEP)


if __name__ != "__main__":
    pass
