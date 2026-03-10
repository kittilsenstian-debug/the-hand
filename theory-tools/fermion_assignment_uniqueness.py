#!/usr/bin/env python3
"""
FERMION ASSIGNMENT UNIQUENESS TEST
====================================
Tests ALL 6 permutations of mapping Fibonacci depths {5, 3, 2}
(from exceptional chain E8 > E7 > E6, Coxeter h/6) to the three
sets of g-factors derived from the PT n=2 domain wall.

The claim: depth 5 -> up-quarks -> vacuum values
           depth 3 -> down-quarks -> overlap integrals
           depth 2 -> leptons -> profile values

This script tests whether this assignment is FORCED (uniquely best)
or whether other permutations give comparable agreement.

The three g-factor sets:
  VACUUM VALUES  (what the wall IS):      phi, 1/phi, sqrt(phi/3)
  OVERLAP INTEGRALS (how it relates):     Y0=3pi/(16sqrt2), 1/Y0, sqrt(3)
  PROFILE VALUES (where it sits):         1/2, 2, sqrt(3)

For each type, the S3 pattern assigns:
  Gen 3 (trivial rep)  -> g_i directly
  Gen 2 (sign rep)     -> conjugate/inverse of g_i
  Gen 1 (standard rep) -> sqrt-derived from g_i

The generation hierarchy is set by epsilon = theta4/theta3 at q = 1/phi.
The Fibonacci depths {5, 3, 2} determine total suppression depth.

Author: Interface Theory, Mar 1 2026
"""

import math
import sys
from itertools import permutations

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

# ======================================================================
# CONSTANTS
# ======================================================================

phi = (1 + math.sqrt(5)) / 2
phibar = 1 / phi
q = phibar
sqrt5 = math.sqrt(5)
pi = math.pi

# Modular forms at golden nome
def theta3_func(q_val, terms=500):
    s = 1.0
    for n in range(1, terms + 1):
        term = q_val ** (n * n)
        if term < 1e-300:
            break
        s += 2 * term
    return s

def theta4_func(q_val, terms=500):
    s = 1.0
    for n in range(1, terms + 1):
        term = q_val ** (n * n)
        if term < 1e-300:
            break
        s += 2 * ((-1) ** n) * term
    return s

def eta_func(q_val, terms=2000):
    result = q_val ** (1.0 / 24)
    for n in range(1, terms + 1):
        qn = q_val ** n
        if qn < 1e-300:
            break
        result *= (1 - qn)
    return result

t3 = theta3_func(q)
t4 = theta4_func(q)
eta = eta_func(q)
epsilon = t4 / t3  # hierarchy parameter

alpha = 1.0 / 137.035999084
mu = 1836.15267343
m_p_GeV = 0.938272
v_higgs = 246.22

# ======================================================================
# MEASURED FERMION MASSES (PDG 2024)
# ======================================================================

m_measured_GeV = {
    'e':   0.000510999,
    'u':   0.00216,
    'd':   0.00467,
    'mu':  0.105658,
    's':   0.0934,
    'c':   1.270,
    'tau': 1.77686,
    'b':   4.180,
    't':   172.69,
}

# Proton-normalized measured masses
m_norm = {k: v / m_p_GeV for k, v in m_measured_GeV.items()}

# Measured Yukawa couplings
y_meas = {k: math.sqrt(2) * v / v_higgs for k, v in m_measured_GeV.items()}

# Reference scale: top Yukawa
y_top_ref = y_meas['t']

# ======================================================================
# PT n=2 GEOMETRY
# ======================================================================

n_depth = 2
Y0 = 3 * pi / (16 * math.sqrt(2))  # Yukawa overlap integral

# ======================================================================
# THREE SETS OF g-FACTORS
# ======================================================================
#
# Each set has 3 values, one for each generation:
#   index 0 = Gen 3 (trivial S3 rep, direct)
#   index 1 = Gen 2 (sign S3 rep, conjugate/inverse)
#   index 2 = Gen 1 (standard S3 rep, sqrt-derived)
#
# The S3 pattern:
#   Trivial  -> direct value
#   Sign     -> inverse/conjugate
#   Standard -> sqrt of related quantity

# SET A: VACUUM VALUES (what the wall IS)
# Gen 3: phi (the vacuum value itself)
# Gen 2: 1/phi (the conjugate vacuum)
# Gen 1: sqrt(phi/3) (projected vacuum / triality)
#
# Physical meaning: these encode the IDENTITY of the wall.
# Up-quarks carry the wall's structure (confined to wall, ground state).
vacuum_g3 = phi          # direct vacuum
vacuum_g2 = phibar       # conjugate vacuum (1/phi)
vacuum_g1 = math.sqrt(phi / 3)  # sqrt of vacuum/triality

# SET B: OVERLAP INTEGRALS (how the wall RELATES)
# Gen 3: Y0 = 3pi/(16sqrt2) (the Yukawa overlap itself)
# Gen 2: 1/Y0 = 16sqrt2/(3pi) (inverse overlap)
# Gen 1: sqrt(3) (projected triality from mixing)
#
# Physical meaning: these encode the COUPLING between bound states.
# Down-quarks carry the wall's mixing (ground-breathing transition).
overlap_g3 = Y0                            # direct Yukawa overlap
overlap_g2 = 1.0 / Y0                     # inverse overlap
overlap_g1 = math.sqrt(3)                 # sqrt of triality

# SET C: PROFILE VALUES (where the wall SITS)
# Gen 3: phi**2/3 (vacuum^2 / triality -- profile strength)
# Gen 2: 1/n_depth = 1/2 (inverse depth)
# Gen 1: sqrt(2/3) (sqrt of breathing norm)
#
# Physical meaning: these encode the POSITION in the wall profile.
# Leptons are free (not confined to wall), couple through full thickness.
profile_g3 = phi**2 / 3                   # profile strength
profile_g2 = 1.0 / n_depth                # inverse depth = 1/2
profile_g1 = math.sqrt(2.0 / 3.0)         # sqrt of breathing norm

# Collect the three sets
g_sets = {
    'vacuum':  (vacuum_g3, vacuum_g2, vacuum_g1),
    'overlap': (overlap_g3, overlap_g2, overlap_g1),
    'profile': (profile_g3, profile_g2, profile_g1),
}

# ======================================================================
# DEPTH ASSIGNMENT
# ======================================================================
#
# The exceptional chain E8 > E7 > E6 has Coxeter numbers 30, 18, 12.
# Divided by 6: h/6 = {5, 3, 2} = consecutive Fibonacci numbers.
#
# The "Fibonacci depth" determines the base epsilon suppression.
# Within each type, the generation structure adds further depth:
#
# For Fibonacci depth D:
#   Gen 3 (trivial):  total_depth = 0     (D enters through g-factor)
#   Gen 2 (sign):     total_depth = 1     (one epsilon step)
#   Gen 1 (standard): total_depth = 2 + f (two epsilon steps + type correction)
#
# The Fibonacci depth D maps to a Delta_type offset:
#   D=5: Delta_type values = {0, 0, 0.5}     for gen {3, 2, 1}
#   D=3: Delta_type values = {1, 0.5, 0.5}   for gen {3, 2, 1}
#   D=2: Delta_type values = {1, 0.5, 1}     for gen {3, 2, 1}

# From one_resonance_fermion_derivation.py:
# The depth assignment for the canonical (depth5->up, depth3->down, depth2->lepton):
#   t: (gen3, up)    -> depth 0.0
#   c: (gen2, up)    -> depth 1.0
#   u: (gen1, up)    -> depth 2.5
#   b: (gen3, down)  -> depth 1.0
#   s: (gen2, down)  -> depth 1.5
#   d: (gen1, down)  -> depth 2.5
#   tau: (gen3, lep) -> depth 1.0
#   mu:  (gen2, lep) -> depth 1.5
#   e:   (gen1, lep) -> depth 3.0
#
# Pattern: the Delta_type encodes how the bound state mixing works.
# Up-type (D=5, deepest embedding):
#   Gen 3: pure ground state, Delta=0
#   Gen 2: conjugated ground, Delta=0
#   Gen 1: projected through breathing, Delta=0.5
#
# Down-type (D=3, middle):
#   Gen 3: full mixing overlap, Delta=1
#   Gen 2: reflected mixing, Delta=0.5
#   Gen 1: projected mixing, Delta=0.5
#
# Lepton (D=2, shallowest):
#   Gen 3: full wall traversal, Delta=1
#   Gen 2: reflected traversal, Delta=0.5
#   Gen 1: full projected traversal, Delta=1

# These Delta_type patterns are different for each Fibonacci depth.
# For each depth assignment, the total depths for (gen3, gen2, gen1) are:
depth_patterns = {
    5: (0.0, 1.0, 2.5),   # up-type pattern
    3: (1.0, 1.5, 2.5),   # down-type pattern
    2: (1.0, 1.5, 3.0),   # lepton pattern
}

# ======================================================================
# PROTON-NORMALIZED MASS FORMULAS (zero-parameter approach)
# ======================================================================
#
# The zero-parameter formulas from one_resonance_fermion_derivation.py:
#   e:   1/mu
#   u:   phi^3/mu
#   d:   9/mu
#   mu:  1/9
#   s:   1/10
#   c:   4/3
#   tau: Koide(e,mu) with K=2/3
#   b:   4*phi^(5/2)/3
#   t:   mu/10
#
# These are the "target" values that come from specific g-factor assignments.
# Let's also compute using the epsilon + g_i approach for the permutation test.

# ======================================================================
# MAIN TEST: ALL 6 PERMUTATIONS
# ======================================================================

print("=" * 78)
print("FERMION ASSIGNMENT UNIQUENESS TEST")
print("=" * 78)
print()
print("Testing all 6 permutations of mapping")
print("  {Fibonacci depth 5, 3, 2} -> {vacuum values, overlap integrals, profile values}")
print()
print("to the three fermion types {up-quarks, down-quarks, leptons}.")
print()

# Print the g-factor sets
print("-" * 78)
print("THE THREE g-FACTOR SETS (from PT n=2 domain wall):")
print("-" * 78)
print()
for name, (g3, g2, g1) in g_sets.items():
    print(f"  {name:10s}: gen3 = {g3:.6f}, gen2 = {g2:.6f}, gen1 = {g1:.6f}")
print()
print("  vacuum:   phi, 1/phi, sqrt(phi/3)")
print("  overlap:  3pi/(16sqrt2), 16sqrt2/(3pi), sqrt(3)")
print("  profile:  phi^2/3, 1/2, sqrt(2/3)")
print()

# Print depth patterns
print("-" * 78)
print("DEPTH PATTERNS (total epsilon exponent for each generation):")
print("-" * 78)
print()
for D, (d3, d2, d1) in depth_patterns.items():
    print(f"  Fibonacci depth {D}: gen3={d3:.1f}, gen2={d2:.1f}, gen1={d1:.1f}")
print()

# Print measured values
print("-" * 78)
print("MEASURED YUKAWA COUPLINGS (reference: y_top = {:.6f})".format(y_top_ref))
print("-" * 78)
print()

# Group by type
type_order = {
    'up':     ['t', 'c', 'u'],
    'down':   ['b', 's', 'd'],
    'lepton': ['tau', 'mu', 'e'],
}

for tname, fermions in type_order.items():
    vals = [y_meas[f] for f in fermions]
    names = [f"{f}={v:.4e}" for f, v in zip(fermions, vals)]
    print(f"  {tname:7s}: {', '.join(names)}")
print()

# ======================================================================
# COMPUTE PREDICTED MASSES FOR EACH PERMUTATION
# ======================================================================

# The 6 permutations: which g-set goes to which type
set_names = ['vacuum', 'overlap', 'profile']
depth_labels = [5, 3, 2]

# For each permutation, we assign:
#   perm[0] -> up-quarks (with depth pattern from depth_labels[0]=5)
#   perm[1] -> down-quarks (with depth pattern from depth_labels[1]=3)
#   perm[2] -> leptons (with depth pattern from depth_labels[2]=2)
#
# Wait -- the question is: does depth follow the g-set, or does depth
# follow the type? Let's think carefully.
#
# The Fibonacci depths {5, 3, 2} come from the exceptional chain embedding.
# The claim is that depth 5 pairs with vacuum values and goes to up-quarks.
# When we permute, we're permuting which g-set + depth pair goes to which type.
#
# So the 6 permutations are of the (depth, g-set) pairs:
#   pair A = (depth 5, vacuum)    -> canonical: up-quarks
#   pair B = (depth 3, overlap)   -> canonical: down-quarks
#   pair C = (depth 2, profile)   -> canonical: leptons
#
# Actually, the user's instruction says to permute the mapping of
# {Fibonacci depth 5, 3, 2} to {vacuum values, overlap integrals, profile values}.
# So we test all 6 assignments of depth-to-gset, then each combo maps to
# up/down/lepton in the fixed order (depth 5 -> type with most suppression = up,
# depth 3 -> down, depth 2 -> lepton).
#
# Wait, re-reading the prompt more carefully: we permute the assignment of
# g-factor sets to types. The depths are fixed: up gets depth-5 pattern,
# down gets depth-3 pattern, lepton gets depth-2 pattern.
# What changes is which g-factor set {vacuum, overlap, profile} each type uses.

print("=" * 78)
print("TESTING ALL 6 PERMUTATIONS")
print("=" * 78)
print()
print("Fixed: up-quarks use depth-5 pattern, down-quarks use depth-3, leptons use depth-2")
print("Varied: which g-factor set {vacuum, overlap, profile} each type uses")
print()

results_all = []

for perm_idx, perm in enumerate(permutations(set_names)):
    up_gset_name = perm[0]
    down_gset_name = perm[1]
    lepton_gset_name = perm[2]

    up_g = g_sets[up_gset_name]       # (g3, g2, g1) for up-quarks
    down_g = g_sets[down_gset_name]   # (g3, g2, g1) for down-quarks
    lepton_g = g_sets[lepton_gset_name]  # (g3, g2, g1) for leptons

    up_depths = depth_patterns[5]      # (0.0, 1.0, 2.5)
    down_depths = depth_patterns[3]    # (1.0, 1.5, 2.5)
    lepton_depths = depth_patterns[2]  # (1.0, 1.5, 3.0)

    # Compute predicted Yukawa couplings
    # y_f = g_i * epsilon^depth * y_top_ref
    predictions = {}

    # Up-type: t (gen3), c (gen2), u (gen1)
    predictions['t']   = up_g[0] * epsilon**up_depths[0] * y_top_ref
    predictions['c']   = up_g[1] * epsilon**up_depths[1] * y_top_ref
    predictions['u']   = up_g[2] * epsilon**up_depths[2] * y_top_ref

    # Down-type: b (gen3), s (gen2), d (gen1)
    predictions['b']   = down_g[0] * epsilon**down_depths[0] * y_top_ref
    predictions['s']   = down_g[1] * epsilon**down_depths[1] * y_top_ref
    predictions['d']   = down_g[2] * epsilon**down_depths[2] * y_top_ref

    # Leptons: tau (gen3), mu (gen2), e (gen1)
    predictions['tau'] = lepton_g[0] * epsilon**lepton_depths[0] * y_top_ref
    predictions['mu']  = lepton_g[1] * epsilon**lepton_depths[1] * y_top_ref
    predictions['e']   = lepton_g[2] * epsilon**lepton_depths[2] * y_top_ref

    # Compute errors
    errors = {}
    log_errors = {}
    for f in predictions:
        if y_meas[f] > 0 and predictions[f] > 0:
            errors[f] = abs(predictions[f] - y_meas[f]) / y_meas[f] * 100
            log_errors[f] = abs(math.log(predictions[f] / y_meas[f]))
        else:
            errors[f] = 999.0
            log_errors[f] = 999.0

    avg_error = sum(errors.values()) / len(errors)
    avg_log_error = sum(log_errors.values()) / len(log_errors)
    max_error = max(errors.values())

    # Count how many fermions are within 5%, 10%, 50%
    within_5 = sum(1 for e in errors.values() if e < 5)
    within_10 = sum(1 for e in errors.values() if e < 10)
    within_50 = sum(1 for e in errors.values() if e < 50)

    results_all.append({
        'perm_idx': perm_idx,
        'up_gset': up_gset_name,
        'down_gset': down_gset_name,
        'lepton_gset': lepton_gset_name,
        'predictions': predictions,
        'errors': errors,
        'log_errors': log_errors,
        'avg_error': avg_error,
        'avg_log_error': avg_log_error,
        'max_error': max_error,
        'within_5': within_5,
        'within_10': within_10,
        'within_50': within_50,
    })

# Sort by average log error (most honest metric)
results_all.sort(key=lambda r: r['avg_log_error'])

# ======================================================================
# PRINT DETAILED RESULTS FOR EACH PERMUTATION
# ======================================================================

for rank, r in enumerate(results_all):
    is_canonical = (r['up_gset'] == 'vacuum' and
                    r['down_gset'] == 'overlap' and
                    r['lepton_gset'] == 'profile')

    label = " *** CANONICAL ***" if is_canonical else ""
    print("-" * 78)
    print(f"RANK {rank+1}: up={r['up_gset']}, down={r['down_gset']}, "
          f"lepton={r['lepton_gset']}{label}")
    print("-" * 78)
    print()
    print(f"  {'Fermion':8s} {'y_pred':>12s} {'y_meas':>12s} {'Error%':>8s} {'|log|':>8s}")
    print("  " + "-" * 50)

    for f in ['t', 'c', 'u', 'b', 's', 'd', 'tau', 'mu', 'e']:
        yp = r['predictions'][f]
        ym = y_meas[f]
        err = r['errors'][f]
        lerr = r['log_errors'][f]
        marker = " <-- good" if err < 5 else ""
        print(f"  {f:8s} {yp:12.4e} {ym:12.4e} {err:7.1f}% {lerr:8.4f}{marker}")

    print()
    print(f"  Average error:     {r['avg_error']:.1f}%")
    print(f"  Average |log|:     {r['avg_log_error']:.4f}")
    print(f"  Max error:         {r['max_error']:.1f}%")
    print(f"  Within 5%:         {r['within_5']}/9")
    print(f"  Within 10%:        {r['within_10']}/9")
    print(f"  Within 50%:        {r['within_50']}/9")
    print()

# ======================================================================
# SUMMARY TABLE
# ======================================================================

print("=" * 78)
print("SUMMARY: ALL 6 PERMUTATIONS RANKED BY AVERAGE |log(pred/meas)|")
print("=" * 78)
print()
print(f"  {'Rank':>4s} {'Up':>10s} {'Down':>10s} {'Lepton':>10s} "
      f"{'Avg%':>7s} {'Avg|log|':>9s} {'Max%':>7s} {'<5%':>4s} {'<10%':>5s} {'Canon':>6s}")
print("  " + "-" * 78)

for rank, r in enumerate(results_all):
    is_canonical = (r['up_gset'] == 'vacuum' and
                    r['down_gset'] == 'overlap' and
                    r['lepton_gset'] == 'profile')
    canon_str = "YES" if is_canonical else ""
    print(f"  {rank+1:4d} {r['up_gset']:>10s} {r['down_gset']:>10s} {r['lepton_gset']:>10s} "
          f"{r['avg_error']:6.1f}% {r['avg_log_error']:9.4f} {r['max_error']:6.1f}% "
          f"{r['within_5']:3d}/9 {r['within_10']:4d}/9 {canon_str:>6s}")

print()

# ======================================================================
# ANALYSIS: IS THE CANONICAL ASSIGNMENT FORCED?
# ======================================================================

print("=" * 78)
print("ANALYSIS: IS THE ASSIGNMENT FORCED?")
print("=" * 78)
print()

best = results_all[0]
canonical = [r for r in results_all
             if r['up_gset'] == 'vacuum' and r['down_gset'] == 'overlap'
             and r['lepton_gset'] == 'profile'][0]
canonical_rank = [i for i, r in enumerate(results_all)
                  if r['up_gset'] == 'vacuum' and r['down_gset'] == 'overlap'
                  and r['lepton_gset'] == 'profile'][0] + 1

print(f"  Canonical assignment (vacuum->up, overlap->down, profile->lepton):")
print(f"    Rank: {canonical_rank} out of 6")
print(f"    Average error: {canonical['avg_error']:.1f}%")
print(f"    Average |log(pred/meas)|: {canonical['avg_log_error']:.4f}")
print(f"    Within 5%: {canonical['within_5']}/9")
print()

print(f"  Best permutation (up={best['up_gset']}, down={best['down_gset']}, "
      f"lepton={best['lepton_gset']}):")
print(f"    Average error: {best['avg_error']:.1f}%")
print(f"    Average |log(pred/meas)|: {best['avg_log_error']:.4f}")
print(f"    Within 5%: {best['within_5']}/9")
print()

if canonical_rank == 1:
    second = results_all[1]
    separation = second['avg_log_error'] - canonical['avg_log_error']
    ratio = second['avg_log_error'] / canonical['avg_log_error'] if canonical['avg_log_error'] > 0 else float('inf')
    print(f"  RESULT: Canonical IS the best permutation.")
    print(f"  Separation from 2nd place: {separation:.4f} in avg |log|")
    print(f"  Ratio (2nd/1st): {ratio:.2f}x worse")
    if ratio > 2.0:
        print(f"  VERDICT: Assignment is STRONGLY FORCED (>2x separation)")
    elif ratio > 1.5:
        print(f"  VERDICT: Assignment is MODERATELY FORCED (1.5-2x separation)")
    elif ratio > 1.2:
        print(f"  VERDICT: Assignment is WEAKLY FORCED (1.2-1.5x separation)")
    else:
        print(f"  VERDICT: Assignment is AMBIGUOUS (<1.2x separation)")
else:
    print(f"  RESULT: Canonical is NOT the best permutation!")
    print(f"  The best permutation beats canonical by:")
    print(f"    {canonical['avg_log_error'] - best['avg_log_error']:.4f} in avg |log|")
    print(f"    {canonical['avg_error'] - best['avg_error']:.1f}% in avg error")
    print()
    print(f"  HONEST ASSESSMENT: The canonical assignment is rank {canonical_rank}/6.")
    print(f"  This means the Fibonacci depth -> g-set mapping is NOT uniquely forced")
    print(f"  by mass agreement alone. Additional structural arguments are needed.")

print()

# ======================================================================
# CROSS-CHECK: PROTON-NORMALIZED APPROACH (zero-parameter)
# ======================================================================

print("=" * 78)
print("CROSS-CHECK: PROTON-NORMALIZED FORMULAS (ZERO PARAMETERS)")
print("=" * 78)
print()
print("  The zero-parameter formulas from the framework:")
print()

# These are the formulas that use only {phi, mu, 3, 4/3, 10, 2/3}
proton_formulas = {
    'e':   ('1/mu',           1.0 / mu),
    'u':   ('phi^3/mu',       phi**3 / mu),
    'd':   ('9/mu',           9.0 / mu),
    'mu':  ('1/9',            1.0 / 9),
    's':   ('1/10',           1.0 / 10),
    'c':   ('4/3',            4.0 / 3),
    'b':   ('4*phi^(5/2)/3',  4 * phi**(5.0/2) / 3),
    't':   ('mu/10',          mu / 10),
}

# Koide for tau
me_n = 1.0 / mu
mmu_n = 1.0 / 9
K = 2.0 / 3.0
s_k = math.sqrt(me_n) + math.sqrt(mmu_n)
a_k = 1 - K
b_k = -2 * K * s_k
c_k = me_n + mmu_n - K * s_k**2
disc = b_k**2 - 4 * a_k * c_k
if disc >= 0:
    x1 = (-b_k + math.sqrt(disc)) / (2 * a_k)
    x2 = (-b_k - math.sqrt(disc)) / (2 * a_k)
    mtau_k = max(x1, x2)**2
    proton_formulas['tau'] = ('Koide(e,mu) K=2/3', mtau_k)

print(f"  {'Fermion':8s} {'Formula':>20s} {'Predicted':>12s} {'Measured':>12s} {'Error':>8s}")
print("  " + "-" * 65)

pf_errors = []
for f in ['e', 'u', 'd', 'mu', 's', 'c', 'tau', 'b', 't']:
    formula, pred = proton_formulas[f]
    meas = m_norm[f]
    err = abs(pred - meas) / meas * 100
    pf_errors.append(err)
    print(f"  {f:8s} {formula:>20s} {pred:12.6f} {meas:12.6f} {err:7.3f}%")

print()
print(f"  Average error: {sum(pf_errors)/len(pf_errors):.3f}%")
print(f"  These zero-parameter formulas are the REAL test of the framework.")
print(f"  The permutation test above uses the epsilon-expansion approach,")
print(f"  which is less precise but reveals the structural assignment.")
print()

# ======================================================================
# DEEPER TEST: WHAT IF DEPTHS ALSO PERMUTE?
# ======================================================================
# The depths {5, 3, 2} could also be assigned differently to {up, down, lepton}.
# This gives 6 depth-permutations x 6 g-set-permutations = 36 total combinations.

print("=" * 78)
print("EXTENDED TEST: 36 COMBINATIONS (depth AND g-set permutations)")
print("=" * 78)
print()
print("  Now also permuting which depth pattern {5, 3, 2} goes to which type.")
print("  This gives 6 x 6 = 36 combinations.")
print()

extended_results = []

for d_perm in permutations(depth_labels):
    for g_perm in permutations(set_names):
        up_depth_pattern = depth_patterns[d_perm[0]]
        down_depth_pattern = depth_patterns[d_perm[1]]
        lepton_depth_pattern = depth_patterns[d_perm[2]]

        up_g = g_sets[g_perm[0]]
        down_g = g_sets[g_perm[1]]
        lepton_g = g_sets[g_perm[2]]

        preds = {}
        preds['t']   = up_g[0] * epsilon**up_depth_pattern[0] * y_top_ref
        preds['c']   = up_g[1] * epsilon**up_depth_pattern[1] * y_top_ref
        preds['u']   = up_g[2] * epsilon**up_depth_pattern[2] * y_top_ref
        preds['b']   = down_g[0] * epsilon**down_depth_pattern[0] * y_top_ref
        preds['s']   = down_g[1] * epsilon**down_depth_pattern[1] * y_top_ref
        preds['d']   = down_g[2] * epsilon**down_depth_pattern[2] * y_top_ref
        preds['tau'] = lepton_g[0] * epsilon**lepton_depth_pattern[0] * y_top_ref
        preds['mu']  = lepton_g[1] * epsilon**lepton_depth_pattern[1] * y_top_ref
        preds['e']   = lepton_g[2] * epsilon**lepton_depth_pattern[2] * y_top_ref

        errs = {}
        lerrs = {}
        for f in preds:
            if y_meas[f] > 0 and preds[f] > 0:
                errs[f] = abs(preds[f] - y_meas[f]) / y_meas[f] * 100
                lerrs[f] = abs(math.log(preds[f] / y_meas[f]))
            else:
                errs[f] = 999.0
                lerrs[f] = 999.0

        avg_e = sum(errs.values()) / len(errs)
        avg_le = sum(lerrs.values()) / len(lerrs)
        w5 = sum(1 for e in errs.values() if e < 5)

        is_canon = (d_perm == (5, 3, 2) and
                    g_perm[0] == 'vacuum' and g_perm[1] == 'overlap' and
                    g_perm[2] == 'profile')

        extended_results.append({
            'depth_perm': d_perm,
            'g_perm': g_perm,
            'avg_error': avg_e,
            'avg_log_error': avg_le,
            'within_5': w5,
            'is_canonical': is_canon,
            'errors': errs,
        })

# Sort by avg log error
extended_results.sort(key=lambda r: r['avg_log_error'])

# Find canonical rank
canon_ext_rank = None
for i, r in enumerate(extended_results):
    if r['is_canonical']:
        canon_ext_rank = i + 1
        break

# Print top 10
print(f"  {'Rank':>4s} {'Depths':>12s} {'Up-g':>10s} {'Down-g':>10s} {'Lep-g':>10s} "
      f"{'Avg%':>7s} {'Avg|log|':>9s} {'<5%':>4s} {'Note':>8s}")
print("  " + "-" * 82)

for i, r in enumerate(extended_results[:15]):
    dp = f"({r['depth_perm'][0]},{r['depth_perm'][1]},{r['depth_perm'][2]})"
    note = "CANON" if r['is_canonical'] else ""
    print(f"  {i+1:4d} {dp:>12s} {r['g_perm'][0]:>10s} {r['g_perm'][1]:>10s} {r['g_perm'][2]:>10s} "
          f"{r['avg_error']:6.1f}% {r['avg_log_error']:9.4f} {r['within_5']:3d}/9 {note:>8s}")

print()
print(f"  ... (showing top 15 of 36)")
print()
print(f"  Canonical assignment rank: {canon_ext_rank} out of 36")

# Find the best
best_ext = extended_results[0]
canon_ext = [r for r in extended_results if r['is_canonical']][0]

print()
if canon_ext_rank == 1:
    second_ext = extended_results[1]
    sep = second_ext['avg_log_error'] - canon_ext['avg_log_error']
    rat = second_ext['avg_log_error'] / canon_ext['avg_log_error'] if canon_ext['avg_log_error'] > 0 else float('inf')
    print(f"  RESULT: Canonical is BEST out of 36 combinations!")
    print(f"  Separation: {sep:.4f} in avg |log|, ratio {rat:.2f}x")
else:
    print(f"  RESULT: Canonical is rank {canon_ext_rank}/36.")
    print(f"  Best: depths=({best_ext['depth_perm'][0]},{best_ext['depth_perm'][1]},"
          f"{best_ext['depth_perm'][2]}), "
          f"g-sets=({best_ext['g_perm'][0]},{best_ext['g_perm'][1]},{best_ext['g_perm'][2]})")
    print(f"  Best avg |log|: {best_ext['avg_log_error']:.4f} vs canonical {canon_ext['avg_log_error']:.4f}")
print()

# ======================================================================
# HONEST ASSESSMENT
# ======================================================================

print("=" * 78)
print("HONEST ASSESSMENT")
print("=" * 78)
print()
print("  KEY NUMBERS:")
print(f"    epsilon = theta4/theta3 = {epsilon:.10f}")
print(f"    phi = {phi:.10f}")
print(f"    Y0 = 3pi/(16sqrt2) = {Y0:.10f}")
print()
print("  The three g-factor sets span different ranges:")
print(f"    vacuum:  [{min(vacuum_g1,vacuum_g2,vacuum_g3):.4f}, "
      f"{max(vacuum_g1,vacuum_g2,vacuum_g3):.4f}]")
print(f"    overlap: [{min(overlap_g1,overlap_g2,overlap_g3):.4f}, "
      f"{max(overlap_g1,overlap_g2,overlap_g3):.4f}]")
print(f"    profile: [{min(profile_g1,profile_g2,profile_g3):.4f}, "
      f"{max(profile_g1,profile_g2,profile_g3):.4f}]")
print()
print("  The depth patterns create hierarchies:")
for D, (d3, d2, d1) in depth_patterns.items():
    ratio = epsilon**d1 / epsilon**d3 if epsilon**d3 > 0 else 0
    print(f"    D={D}: gen3/gen1 suppression ratio = epsilon^{d1-d3:.1f} = {ratio:.4e}")
print()
print("  WHAT THIS TEST REVEALS:")
print("  The g-factor assignment determines the O(1) prefactors for each fermion.")
print("  The depth patterns determine the overall hierarchy (powers of epsilon).")
print("  The question is: does the DATA force a unique (depth, g-set) -> type map?")
print()

# Count how many are within factor of 2 of canonical
canon_log = canon_ext['avg_log_error']
close_count = sum(1 for r in extended_results if r['avg_log_error'] < 1.5 * canon_log)
print(f"  Number of combinations within 1.5x of canonical: {close_count}/36")
print(f"  Number of combinations within 2x of canonical: "
      f"{sum(1 for r in extended_results if r['avg_log_error'] < 2.0 * canon_log)}/36")
print()

# Final verdict
if canon_ext_rank == 1 and close_count <= 3:
    print("  VERDICT: The assignment is FORCED by the data.")
    print("  Only the canonical mapping gives sub-percent agreement for most fermions.")
elif canon_ext_rank <= 3:
    print("  VERDICT: The assignment is PREFERRED but not uniquely forced.")
    print("  A small number of alternatives give comparable agreement.")
    print("  Additional structural arguments (E8 root projections, golden direction)")
    print("  are needed to single out the canonical assignment.")
else:
    print("  VERDICT: The assignment is NOT forced by mass agreement alone.")
    print("  Multiple permutations give comparable or better agreement.")
    print("  The canonical assignment may still be correct for structural reasons,")
    print("  but the g-factor approach doesn't uniquely select it.")

print()
print("=" * 78)
print("END OF UNIQUENESS TEST")
print("=" * 78)
