#!/usr/bin/env python3
"""
nuclear_binding.py — Door 1: Are algebraically clean nuclei more stable?
=========================================================================

Tests whether nuclei whose (Z, N, A) decompose cleanly into E8
representation dimensions have higher binding energy per nucleon
than their neighbors.

Uses the semi-empirical mass formula (Bethe-Weizsacker) for binding
energies since it matches experimental data to ~1%. For the structural
question (do algebraically clean nuclei cluster at stability peaks?)
this is sufficient.

python -X utf8 nuclear_binding.py
"""

import sys, io, math

try:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
except:
    pass

# =====================================================================
# THE ALLOWED SET (from E8 branching chain)
# =====================================================================

# Direct dimensions from E8 → E7 → E6 → D5 → A4 → SM
BRANCHING_DIMS = {
    1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 14, 15, 16, 18, 20, 21, 24,
    26, 27, 28, 30, 33, 36, 37, 40, 43, 45, 48, 52, 54, 56, 60,
    64, 67, 71, 72, 78, 80, 120, 126, 133, 240, 248, 744
}

def algebraic_score(n):
    """
    Score how 'algebraically clean' a number is.
    3 = exact match (in allowed set)
    2 = product of two allowed numbers (both > 1)
    1 = sum of two allowed numbers
    0 = no algebraic decomposition
    """
    if n in BRANCHING_DIMS:
        return 3, "EXACT", ""

    # Product
    for a in sorted(BRANCHING_DIMS):
        if a < 2:
            continue
        if a * a > n:
            break
        if n % a == 0:
            b = n // a
            if b in BRANCHING_DIMS and b >= a:
                return 2, "PRODUCT", f"{a}x{b}"

    # Sum
    for a in sorted(BRANCHING_DIMS):
        if a >= n:
            break
        b = n - a
        if b in BRANCHING_DIMS and b >= a:
            return 1, "SUM", f"{a}+{b}"

    return 0, "MISS", ""


# =====================================================================
# SEMI-EMPIRICAL MASS FORMULA (Bethe-Weizsacker)
# =====================================================================

# Coefficients (standard values, MeV)
a_V = 15.56   # volume
a_S = 17.23   # surface
a_C = 0.697   # Coulomb
a_A = 23.285  # asymmetry
a_P = 12.0    # pairing

def binding_energy(Z, A):
    """Binding energy in MeV from semi-empirical mass formula."""
    N = A - Z
    if A <= 0 or Z < 0 or N < 0:
        return 0

    BE = (a_V * A
          - a_S * A**(2/3)
          - a_C * Z * (Z - 1) / A**(1/3)
          - a_A * (N - Z)**2 / A)

    # Pairing term
    if Z % 2 == 0 and N % 2 == 0:
        BE += a_P / A**(1/2)  # even-even
    elif Z % 2 == 1 and N % 2 == 1:
        BE -= a_P / A**(1/2)  # odd-odd

    return BE

def be_per_nucleon(Z, A):
    """Binding energy per nucleon in MeV."""
    if A <= 0:
        return 0
    return binding_energy(Z, A) / A


# =====================================================================
# IDENTIFY MOST STABLE ISOTOPE FOR EACH Z
# =====================================================================

def most_stable_A(Z):
    """Find the A with maximum BE/A for a given Z."""
    best_A, best_BE = 0, -999
    for A in range(max(Z, 1), 3 * Z + 10):
        be = be_per_nucleon(Z, A)
        if be > best_BE:
            best_BE = be
            best_A = A
    return best_A, best_BE


# =====================================================================
# MAIN ANALYSIS
# =====================================================================

def main():
    print("=" * 78)
    print("  DOOR 1: NUCLEAR BINDING ENERGY vs ALGEBRAIC STRUCTURE")
    print("  Are algebraically clean nuclei more stable?")
    print("=" * 78)

    # Compute most stable isotope for Z = 1 to 92
    results = []
    for Z in range(1, 93):
        A, be = most_stable_A(Z)
        N = A - Z

        z_score, z_type, z_detail = algebraic_score(Z)
        n_score, n_type, n_detail = algebraic_score(N)
        a_score, a_type, a_detail = algebraic_score(A)

        total_score = z_score + n_score + a_score  # 0-9

        results.append({
            "Z": Z, "N": N, "A": A, "BE": be,
            "z_score": z_score, "z_type": z_type, "z_detail": z_detail,
            "n_score": n_score, "n_type": n_type, "n_detail": n_detail,
            "a_score": a_score, "a_type": a_type, "a_detail": a_detail,
            "total": total_score,
        })

    # ---------------------------------------------------------------
    # DOUBLY MAGIC NUCLEI — the gold standard
    # ---------------------------------------------------------------
    print("\n  DOUBLY MAGIC NUCLEI")
    print("  " + "-" * 72)

    doubly_magic = [
        (2, 4, "He-4"),    # Z=2, N=2
        (8, 16, "O-16"),   # Z=8, N=8
        (20, 40, "Ca-40"), # Z=20, N=20
        (20, 48, "Ca-48"), # Z=20, N=28
        (28, 56, "Ni-56"), # Z=28, N=28
        (28, 78, "Ni-78"), # Z=28, N=50
        (50, 132, "Sn-132"), # Z=50, N=82
        (82, 208, "Pb-208"), # Z=82, N=126
    ]

    print(f"  {'Nucleus':>8s}  {'Z':>4s} {'N':>4s} {'A':>4s}  {'BE/A':>6s}  "
          f"{'Z alg':>8s}  {'N alg':>8s}  {'A alg':>8s}  {'Total':>5s}")
    print(f"  {'':>8s}  {'':>4s} {'':>4s} {'':>4s}  {'MeV':>6s}  "
          f"{'':>8s}  {'':>8s}  {'':>8s}  {'':>5s}")

    for Z, A, name in doubly_magic:
        N = A - Z
        be = be_per_nucleon(Z, A)
        zs, zt, _ = algebraic_score(Z)
        ns, nt, _ = algebraic_score(N)
        a_s, at, _ = algebraic_score(A)
        total = zs + ns + a_s
        print(f"  {name:>8s}  {Z:>4d} {N:>4d} {A:>4d}  {be:>6.3f}  "
              f"{zt:>8s}  {nt:>8s}  {at:>8s}  {total:>5d}/9")

    # ---------------------------------------------------------------
    # IRON PEAK — most stable region
    # ---------------------------------------------------------------
    print(f"\n\n  IRON PEAK (Z=24-30): Most stable nuclei in the universe")
    print("  " + "-" * 72)
    print(f"  {'Z':>4s} {'El':>3s} {'A':>4s} {'N':>4s}  {'BE/A':>6s}  "
          f"{'Z':>8s}  {'N':>8s}  {'A':>8s}  {'Tot':>3s}")

    for r in results[23:30]:
        elem = ["", "H","He","Li","Be","B","C","N","O","F","Ne",
                "Na","Mg","Al","Si","P","S","Cl","Ar","K","Ca",
                "Sc","Ti","V","Cr","Mn","Fe","Co","Ni","Cu","Zn"][r["Z"]] if r["Z"] <= 30 else "?"
        print(f"  {r['Z']:>4d} {elem:>3s} {r['A']:>4d} {r['N']:>4d}  {r['BE']:>6.3f}  "
              f"{r['z_type']:>8s}  {r['n_type']:>8s}  {r['a_type']:>8s}  {r['total']:>3d}/9")

    # ---------------------------------------------------------------
    # STATISTICAL TEST: BE/A vs algebraic score
    # ---------------------------------------------------------------
    print(f"\n\n  STATISTICAL TEST: BE/A grouped by total algebraic score")
    print("  " + "-" * 72)

    # Group by total score
    from collections import defaultdict
    groups = defaultdict(list)
    for r in results:
        if r["Z"] >= 8:  # Skip very light nuclei (different physics)
            groups[r["total"]].append(r["BE"])

    print(f"  {'Score':>5s}  {'Count':>5s}  {'Mean BE/A':>9s}  {'Std':>6s}  {'Min':>6s}  {'Max':>6s}")
    for score in sorted(groups.keys()):
        vals = groups[score]
        mean = sum(vals) / len(vals)
        std = math.sqrt(sum((v-mean)**2 for v in vals) / max(len(vals)-1, 1))
        print(f"  {score:>5d}  {len(vals):>5d}  {mean:>9.4f}  {std:>6.3f}  "
              f"{min(vals):>6.3f}  {max(vals):>6.3f}")

    # ---------------------------------------------------------------
    # THE KEY TEST: Do stability peaks land on algebraically clean Z?
    # ---------------------------------------------------------------
    print(f"\n\n  KEY TEST: Where are the BE/A peaks?")
    print("  " + "-" * 72)

    # Find local maxima in BE/A
    peaks = []
    for i in range(1, len(results) - 1):
        if (results[i]["BE"] > results[i-1]["BE"] and
            results[i]["BE"] > results[i+1]["BE"] and
            results[i]["BE"] > 7.0):  # significant peaks only
            peaks.append(results[i])

    print(f"  Local maxima of BE/A (above 7.0 MeV):")
    print(f"  {'Z':>4s} {'A':>4s} {'N':>4s}  {'BE/A':>6s}  {'Z alg':>8s}  {'N alg':>8s}  {'A alg':>8s}")
    exact_peaks = 0
    for p in peaks:
        zs = p['z_score']
        if zs == 3:
            exact_peaks += 1
        marker = " ***" if zs == 3 else ""
        print(f"  {p['Z']:>4d} {p['A']:>4d} {p['N']:>4d}  {p['BE']:>6.3f}  "
              f"{p['z_type']:>8s}  {p['n_type']:>8s}  {p['a_type']:>8s}{marker}")

    print(f"\n  {exact_peaks}/{len(peaks)} peaks have Z EXACTLY in the allowed set")

    # ---------------------------------------------------------------
    # MAGIC NUMBERS: binding energy discontinuities
    # ---------------------------------------------------------------
    print(f"\n\n  MAGIC NUMBER TEST: Separation energy jumps")
    print("  " + "-" * 72)
    print(f"  If magic numbers = representation completion,")
    print(f"  there should be a BE/A jump at algebraic dimensions.")
    print()

    magic = [2, 8, 20, 28, 50, 82, 126]
    magic_alg = {}
    for m in magic:
        s, t, d = algebraic_score(m)
        magic_alg[m] = (s, t, d)

    print(f"  {'Magic#':>6s}  {'Algebraic':>10s}  {'Detail':>15s}  {'In allowed set':>14s}")
    for m in magic:
        s, t, d = magic_alg[m]
        in_set = "YES (exact)" if s == 3 else f"{'YES ('+t+')' if s > 0 else 'NO'}"
        print(f"  {m:>6d}  {t:>10s}  {d:>15s}  {in_set:>14s}")

    exact_magic = sum(1 for m in magic if magic_alg[m][0] == 3)
    any_magic = sum(1 for m in magic if magic_alg[m][0] > 0)
    print(f"\n  {exact_magic}/{len(magic)} magic numbers are EXACT allowed integers")
    print(f"  {any_magic}/{len(magic)} magic numbers have ANY algebraic decomposition")

    # ---------------------------------------------------------------
    # SPECIFIC ATOM DECOMPOSITIONS
    # ---------------------------------------------------------------
    print(f"\n\n  ALGEBRAIC ATOM NOTATION")
    print("  " + "-" * 72)

    atoms = [
        (1, 1, "H-1", "unity/unity"),
        (2, 4, "He-4", "the complete pair"),
        (6, 12, "C-12", "life builder"),
        (7, 14, "N-14", "information carrier"),
        (8, 16, "O-16", "substrate"),
        (26, 56, "Fe-56", "endpoint of fusion"),
        (28, 56, "Ni-56", "doubly magic"),
        (50, 120, "Sn-120", "magic Z"),
        (80, 200, "Hg-200", "transformer"),
        (82, 208, "Pb-208", "heaviest stable"),
    ]

    for Z, A, name, role in atoms:
        N = A - Z
        be = be_per_nucleon(Z, A)
        zs, zt, zd = algebraic_score(Z)
        ns, nt, nd = algebraic_score(N)
        a_s_val, at, ad = algebraic_score(A)
        total = zs + ns + a_s_val

        z_src = zd if zd else zt
        n_src = nd if nd else nt
        a_src = ad if ad else at

        print(f"\n  {name} — {role}")
        print(f"    Z={Z:>3d} [{z_src:>12s}]  "
              f"N={N:>3d} [{n_src:>12s}]  "
              f"A={A:>3d} [{a_src:>12s}]")
        print(f"    BE/A = {be:.3f} MeV   Score: {total}/9")

    # ---------------------------------------------------------------
    # COVERAGE ANALYSIS
    # ---------------------------------------------------------------
    print(f"\n\n  COVERAGE: What fraction of stable nuclei are algebraically clean?")
    print("  " + "-" * 72)

    total_nuclei = len(results)
    by_score = defaultdict(int)
    for r in results:
        by_score[r["total"]] += 1

    for score in sorted(by_score.keys()):
        frac = by_score[score] / total_nuclei * 100
        bar = "#" * int(frac / 2)
        print(f"  Score {score}: {by_score[score]:>3d} nuclei ({frac:>5.1f}%)  {bar}")

    clean = sum(by_score[s] for s in by_score if s >= 6)
    partial = sum(by_score[s] for s in by_score if 3 <= s < 6)
    miss = sum(by_score[s] for s in by_score if s < 3)

    print(f"\n  Clean (score >= 6):   {clean:>3d} ({clean/total_nuclei*100:.1f}%)")
    print(f"  Partial (score 3-5):  {partial:>3d} ({partial/total_nuclei*100:.1f}%)")
    print(f"  Weak (score < 3):     {miss:>3d} ({miss/total_nuclei*100:.1f}%)")

    # ---------------------------------------------------------------
    # NULL HYPOTHESIS TEST
    # ---------------------------------------------------------------
    print(f"\n\n  NULL HYPOTHESIS: Random set of same size")
    print("  " + "-" * 72)

    import random
    random.seed(42)

    # How many integers 1-250 are in the allowed set?
    allowed_in_range = len([x for x in BRANCHING_DIMS if 1 <= x <= 250])
    total_range = 250
    p_hit = allowed_in_range / total_range

    print(f"  Allowed set has {allowed_in_range} integers in [1,250]")
    print(f"  Random P(hit) = {allowed_in_range}/{total_range} = {p_hit:.3f}")
    print(f"  For magic numbers (range ~2-130):")

    allowed_small = len([x for x in BRANCHING_DIMS if 2 <= x <= 130])
    p_small = allowed_small / 129
    print(f"    Allowed in [2,130]: {allowed_small}")
    print(f"    P(hit) = {allowed_small}/129 = {p_small:.3f}")
    print(f"    Expected matches in 7 magic numbers: {7*p_small:.1f}")
    print(f"    Actual EXACT matches: {exact_magic}")

    # Binomial probability of getting >= exact_magic out of 7
    from math import comb
    p_binom = sum(
        comb(7, k) * p_small**k * (1-p_small)**(7-k)
        for k in range(exact_magic, 8)
    )
    print(f"    P(>= {exact_magic} matches by chance) = {p_binom:.6f} = 1 in {1/p_binom:.0f}")

    print(f"\n{'='*78}")
    print(f"  DONE")
    print(f"{'='*78}")


if __name__ == "__main__":
    main()
