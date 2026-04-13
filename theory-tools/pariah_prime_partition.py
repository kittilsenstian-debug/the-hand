"""
pariah_prime_partition.py — Complete prime-power analysis of the 6 pariah group orders.

Framework context:
  ENGAGED (phi vacuum):    J1 (KNOWING), J3 (HOLDING), Ru (BEING)
  WITHDRAWN (-1/phi vacuum): ON (SENSING), Ly (STILL), J4 (IMPOSSIBLE)

Computes Big Omega, axis products, cross-prime patterns, null tests.
No external dependencies.
"""

import math
import random
from collections import defaultdict
from itertools import product as iter_product

# ═══════════════════════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════════════════════

PARIAHS = {
    "J1":  {2: 3,  3: 1, 5: 1, 7: 1, 11: 1, 19: 1},
    "J3":  {2: 7,  3: 5, 5: 1, 17: 1, 19: 1},
    "Ru":  {2: 14, 3: 3, 5: 3, 7: 1, 13: 1, 29: 1},
    "ON":  {2: 9,  3: 4, 5: 1, 7: 3, 11: 1, 19: 1, 31: 1},
    "Ly":  {2: 8,  3: 7, 5: 6, 7: 1, 11: 1, 31: 1, 37: 1, 67: 1},
    "J4":  {2: 21, 3: 3, 5: 1, 7: 1, 11: 3, 23: 1, 29: 1, 31: 1, 37: 1, 43: 1},
}

CLAIMED_ORDERS = {
    "J1":  175560,
    "J3":  50232960,
    "Ru":  145926144000,
    "ON":  460815505920,
    "Ly":  51765179004000000,
    "J4":  86775571046077562880,
}

ENGAGED  = ["J1", "J3", "Ru"]   # phi vacuum
WITHDRAWN = ["ON", "Ly", "J4"]  # -1/phi vacuum

MONSTER_FACTORIZATION = {
    2: 46, 3: 20, 5: 9, 7: 6, 11: 2, 13: 3,
    17: 1, 19: 1, 23: 1, 29: 1, 31: 1,
    41: 1, 47: 1, 59: 1, 71: 1
}

# Framework-significant numbers
FIBONACCI = {1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233}
E_DIMS = {8, 78, 133, 248}       # E6, E7, E8 dimensions
E_ROOTS = {72, 126, 240}          # E6, E7, E8 root counts
COXETER = {12, 18, 30}            # E6, E7, E8 Coxeter numbers
SPORADIC_DIMS = {196883, 196884, 744}
FRAMEWORK_NUMBERS = {
    1, 2, 3, 5, 6, 7, 8, 10, 12, 13, 14, 18, 19, 20, 21, 23, 24, 26, 27, 28,
    29, 30, 31, 36, 37, 40, 43, 46, 48, 50, 56, 67, 72, 78, 80, 126, 133,
    147, 240, 248, 294, 744
}

FRAMEWORK_LABELS = {
    1: "unity",
    2: "F(3), Z2",
    3: "F(4), triality",
    5: "F(5), icosahedron",
    6: "|S3|",
    7: "Fano points",
    8: "F(6), rank(E8)",
    10: "dim(spacetime)",
    12: "h(E6)",
    13: "F(7), sporadic primes",
    14: "2*7",
    18: "h(E7)",
    19: "pariah prime",
    20: "amino acids, icosahedron vertices",
    21: "F(8), triangular(6)",
    23: "pariah prime",
    24: "c(Monster), Leech dim",
    26: "sporadic groups count",
    27: "dim(J3(O)), Albert algebra",
    28: "dim(2.Ru), perfect number",
    29: "pariah prime",
    30: "h(E8), |S3|*|S5/Z2|",
    31: "pariah prime",
    36: "3*12",
    37: "alien prime",
    40: "8*5",
    43: "alien prime",
    46: "Monster 2-exponent",
    48: "dim(C2 rep)",
    50: "half-century",
    56: "fund(E7)",
    67: "alien prime",
    72: "roots(E6)",
    78: "dim(E6)",
    80: "hierarchy exponent",
    126: "roots(E7), antisym SO(10)",
    133: "dim(E7 adj)",
    147: "alien prime sum (37+43+67)",
    240: "roots(E8), kissing number",
    248: "dim(E8)",
    294: "2*147",
    744: "j-constant, 3*248",
}


def order_from_factorization(fac):
    """Compute group order from prime factorization dict."""
    result = 1
    for p, e in fac.items():
        result *= p ** e
    return result


def big_omega(fac):
    """Total prime factor count with multiplicity."""
    return sum(fac.values())


def is_fibonacci(n):
    """Check if n is a Fibonacci number."""
    if n < 0:
        return False
    # n is Fibonacci iff 5n^2+4 or 5n^2-4 is a perfect square
    for delta in (4, -4):
        val = 5 * n * n + delta
        if val >= 0:
            s = int(math.isqrt(val))
            if s * s == val:
                return True
    return False


def framework_label(n):
    """Return framework significance label or empty string."""
    parts = []
    if is_fibonacci(n):
        parts.append(f"Fibonacci")
    if n in E_DIMS:
        parts.append(f"dim(E-series)")
    if n in E_ROOTS:
        parts.append(f"roots(E-series)")
    if n in COXETER:
        parts.append(f"Coxeter(E-series)")
    if n in FRAMEWORK_LABELS and "Fibonacci" not in FRAMEWORK_LABELS.get(n, ""):
        parts.append(FRAMEWORK_LABELS[n])
    if not parts and n in FRAMEWORK_NUMBERS:
        parts.append("framework number")
    return ", ".join(parts) if parts else ""


# ═══════════════════════════════════════════════════════════════════
# 0. VERIFY FACTORIZATIONS
# ═══════════════════════════════════════════════════════════════════

def section_verify():
    print("=" * 80)
    print("SECTION 0: FACTORIZATION VERIFICATION")
    print("=" * 80)
    all_ok = True
    for name in ["J1", "J3", "Ru", "ON", "Ly", "J4"]:
        computed = order_from_factorization(PARIAHS[name])
        claimed = CLAIMED_ORDERS[name]
        ok = (computed == claimed)
        status = "OK" if ok else "MISMATCH"
        print(f"  {name:3s}: computed = {computed:>25,d}  claimed = {claimed:>25,d}  [{status}]")
        if not ok:
            all_ok = False
    print()
    if all_ok:
        print("  All 6 factorizations verified.")
    else:
        print("  *** FACTORIZATION ERRORS DETECTED ***")
    print()


# ═══════════════════════════════════════════════════════════════════
# 1. PER-PRIME ANALYSIS
# ═══════════════════════════════════════════════════════════════════

def section_per_prime():
    print("=" * 80)
    print("SECTION 1: PER-PRIME EXPONENT TABLE")
    print("=" * 80)

    # Collect all primes
    all_primes = set()
    for fac in PARIAHS.values():
        all_primes.update(fac.keys())
    all_primes = sorted(all_primes)

    names = ["J1", "J3", "Ru", "ON", "Ly", "J4"]

    # Header
    header = f"{'p':>4s}"
    for n in names:
        header += f"  {n:>4s}"
    header += f"  {'SUM':>4s}  {'ENG':>4s}  {'WTH':>4s}  {'Significance':s}"
    print(header)
    print("-" * len(header) + "-" * 30)

    prime_data = {}
    for p in all_primes:
        exps = [PARIAHS[n].get(p, 0) for n in names]
        total = sum(exps)
        eng = sum(PARIAHS[n].get(p, 0) for n in ENGAGED)
        wth = sum(PARIAHS[n].get(p, 0) for n in WITHDRAWN)
        sig = framework_label(total)
        row = f"{p:>4d}"
        for e in exps:
            row += f"  {e:>4d}"
        row += f"  {total:>4d}  {eng:>4d}  {wth:>4d}  {sig}"
        print(row)
        prime_data[p] = {"exps": exps, "total": total, "eng": eng, "wth": wth}

    # Totals row
    print("-" * len(header) + "-" * 30)
    total_exps = [sum(PARIAHS[n].get(p, 0) for p in all_primes) for n in names]
    grand = sum(total_exps)
    eng_total = sum(total_exps[:3])
    wth_total = sum(total_exps[3:])
    row = f"{'TOT':>4s}"
    for e in total_exps:
        row += f"  {e:>4d}"
    row += f"  {grand:>4d}  {eng_total:>4d}  {wth_total:>4d}"
    print(row)
    print()

    return prime_data, all_primes


# ═══════════════════════════════════════════════════════════════════
# 2. BIG OMEGA ANALYSIS
# ═══════════════════════════════════════════════════════════════════

def section_big_omega():
    print("=" * 80)
    print("SECTION 2: BIG OMEGA (total prime-power count with multiplicity)")
    print("=" * 80)

    names_eng = ENGAGED
    names_wth = WITHDRAWN

    print()
    print("  ENGAGED (phi vacuum):")
    eng_total = 0
    for n in names_eng:
        o = big_omega(PARIAHS[n])
        eng_total += o
        print(f"    Omega({n:3s}) = {o:3d}")
    print(f"    ENGAGED TOTAL = {eng_total}")

    print()
    print("  WITHDRAWN (-1/phi vacuum):")
    wth_total = 0
    for n in names_wth:
        o = big_omega(PARIAHS[n])
        wth_total += o
        print(f"    Omega({n:3s}) = {o:3d}")
    print(f"    WITHDRAWN TOTAL = {wth_total}")

    grand = eng_total + wth_total
    print()
    print(f"  GRAND TOTAL = {grand}")
    print()

    # Check claimed values
    checks = [
        (eng_total, 46, "Monster 2-exponent"),
        (wth_total, 80, "Hierarchy exponent"),
        (grand, 126, "roots(E7)"),
    ]
    for val, expected, label in checks:
        status = "CONFIRMED" if val == expected else f"NO (got {val})"
        print(f"  CHECK: Engaged = {expected} ({label})?  {status}")
    print()

    return eng_total, wth_total, grand


# ═══════════════════════════════════════════════════════════════════
# 3. 2-EXPONENT ANALYSIS
# ═══════════════════════════════════════════════════════════════════

def section_2exp():
    print("=" * 80)
    print("SECTION 3: 2-EXPONENT ANALYSIS")
    print("=" * 80)

    names = ["J1", "J3", "Ru", "ON", "Ly", "J4"]
    two_exps = [PARIAHS[n][2] for n in names]

    # Schur multipliers (trivial = 1, nontrivial listed)
    schur = {
        "J1": "trivial",
        "J3": "Z3",
        "Ru": "Z2",
        "ON": "Z3",
        "Ly": "trivial",
        "J4": "trivial",
    }

    print()
    print("  2-exponents: ", two_exps)
    print()

    fib_sum = 0
    nonfib_sum = 0
    for n, e in zip(names, two_exps):
        fib = is_fibonacci(e)
        tag = "Fibonacci" if fib else ""
        sch = schur[n]
        fib_sch_match = (fib and sch == "trivial") or (not fib and sch != "trivial")
        corr = "MATCH" if fib_sch_match else "NO MATCH"
        print(f"    {n:3s}: 2^{e:<3d}  Fib={str(fib):<6s}  Schur={sch:<8s}  Fib<->trivial: {corr}")
        if fib:
            fib_sum += e
        else:
            nonfib_sum += e

    print()
    print(f"  Fibonacci 2-exponents sum:     {fib_sum}")
    print(f"  Non-Fibonacci 2-exponents sum: {nonfib_sum}")
    fib_label = framework_label(fib_sum)
    nonfib_label = framework_label(nonfib_sum)
    if fib_label:
        print(f"    Fibonacci sum significance: {fib_label}")
    if nonfib_label:
        print(f"    Non-Fibonacci sum significance: {nonfib_label}")
    print()

    # Schur correlation summary
    matches = sum(1 for n in names if
                  (is_fibonacci(PARIAHS[n][2]) and schur[n] == "trivial") or
                  (not is_fibonacci(PARIAHS[n][2]) and schur[n] != "trivial"))
    print(f"  Schur-Fibonacci correlation: {matches}/6 match")
    print(f"    Rule: Fibonacci 2-exponent <=> trivial Schur multiplier")
    print()


# ═══════════════════════════════════════════════════════════════════
# 4. CROSS-PRIME PATTERNS (PARIAH + MONSTER)
# ═══════════════════════════════════════════════════════════════════

def section_cross_prime(prime_data, all_primes):
    print("=" * 80)
    print("SECTION 4: CROSS-PRIME PATTERNS (Pariah sum + Monster exponent)")
    print("=" * 80)

    # All primes in either pariahs or Monster
    combined_primes = sorted(set(all_primes) | set(MONSTER_FACTORIZATION.keys()))

    print()
    print(f"  {'p':>4s}  {'Pariah':>7s}  {'Monster':>7s}  {'Sum':>5s}  Significance")
    print(f"  {'-'*4:s}  {'-'*7:s}  {'-'*7:s}  {'-'*5:s}  {'-'*30:s}")

    for p in combined_primes:
        par_sum = prime_data[p]["total"] if p in prime_data else 0
        mon_exp = MONSTER_FACTORIZATION.get(p, 0)
        total = par_sum + mon_exp
        sig = framework_label(total)
        marker = ""
        if p in {37, 43, 67}:
            marker = " [ALIEN PRIME]"
        print(f"  {p:>4d}  {par_sum:>7d}  {mon_exp:>7d}  {total:>5d}  {sig}{marker}")

    # Specific checks
    print()
    par_3 = prime_data.get(3, {}).get("total", 0)
    mon_3 = MONSTER_FACTORIZATION.get(3, 0)
    print(f"  CHECK: pariah_3_sum + monster_3_exp = {par_3} + {mon_3} = {par_3 + mon_3}")
    print(f"    = 43 (alien prime)?  {'YES' if par_3 + mon_3 == 43 else 'NO'}")

    par_5 = prime_data.get(5, {}).get("total", 0)
    print(f"  CHECK: pariah_5_sum = {par_5}")
    print(f"    = 13 (Fibonacci)?  {'YES' if par_5 == 13 else 'NO'}  is_Fibonacci: {is_fibonacci(par_5)}")

    par_7 = prime_data.get(7, {}).get("total", 0)
    mon_7 = MONSTER_FACTORIZATION.get(7, 0)
    print(f"  CHECK: pariah_7_sum + monster_7_exp = {par_7} + {mon_7} = {par_7 + mon_7}")
    sig7 = framework_label(par_7 + mon_7)
    if sig7:
        print(f"    Significance: {sig7}")

    par_11 = prime_data.get(11, {}).get("total", 0)
    mon_11 = MONSTER_FACTORIZATION.get(11, 0)
    print(f"  CHECK: pariah_11_sum + monster_11_exp = {par_11} + {mon_11} = {par_11 + mon_11}")
    sig11 = framework_label(par_11 + mon_11)
    if sig11:
        print(f"    Significance: {sig11}")

    # Grand totals
    par_grand = sum(prime_data[p]["total"] for p in all_primes)
    mon_grand = sum(MONSTER_FACTORIZATION.values())
    print()
    print(f"  GRAND: pariah_total = {par_grand}, monster_total = {mon_grand}, combined = {par_grand + mon_grand}")
    sig_comb = framework_label(par_grand + mon_grand)
    if sig_comb:
        print(f"    Combined significance: {sig_comb}")
    print()


# ═══════════════════════════════════════════════════════════════════
# 5. AXIS PRODUCT CHECK (2-exponent products by force axis)
# ═══════════════════════════════════════════════════════════════════

def section_axis_products():
    print("=" * 80)
    print("SECTION 5: AXIS PRODUCT CHECK (2-exponent products by force axis)")
    print("=" * 80)
    print()
    print("  Force axes pair engaged + withdrawn pariahs:")
    print("    KNOWING: J1 (engaged) + ON (withdrawn)")
    print("    HOLDING: J3 (engaged) + Ly (withdrawn)")
    print("    MAKING:  Ru (engaged) + J4 (withdrawn)")
    print()

    axes = [
        ("KNOWING", "J1", "ON"),
        ("HOLDING", "J3", "Ly"),
        ("MAKING",  "Ru", "J4"),
    ]

    for axis_name, eng_name, wth_name in axes:
        e1 = PARIAHS[eng_name][2]
        e2 = PARIAHS[wth_name][2]
        prod = e1 * e2
        sig = framework_label(prod)
        print(f"  {axis_name:8s}: {eng_name}(2^{e1}) x {wth_name}(2^{e2}) = {e1} x {e2} = {prod}")
        if sig:
            print(f"             Significance: {sig}")
        # Extra interpretation
        if prod == 27:
            print(f"             = dim(J3(O)), Albert algebra")
        elif prod == 56:
            print(f"             = fund(E7), minimal representation")
        elif prod == 294:
            print(f"             = 2 x 147 = 2 x (37 + 43 + 67) = 2 x (alien prime sum)")
        print()

    # Sum of products
    products = [3*9, 7*8, 14*21]
    total = sum(products)
    print(f"  Sum of axis products: {products[0]} + {products[1]} + {products[2]} = {total}")
    sig_total = framework_label(total)
    if sig_total:
        print(f"    Significance: {sig_total}")
    print()

    # Product of products
    prod_all = products[0] * products[1] * products[2]
    print(f"  Product of axis products: {products[0]} x {products[1]} x {products[2]} = {prod_all}")
    # Factor it
    n = prod_all
    factors = []
    for p in range(2, int(math.isqrt(n)) + 2):
        while n % p == 0:
            factors.append(p)
            n //= p
    if n > 1:
        factors.append(n)
    print(f"    = {' x '.join(str(f) for f in factors)}")
    print()


# ═══════════════════════════════════════════════════════════════════
# 6. NULL TEST
# ═══════════════════════════════════════════════════════════════════

def section_null_test():
    print("=" * 80)
    print("SECTION 6: NULL TEST (Monte Carlo)")
    print("=" * 80)
    print()

    names = ["J1", "J3", "Ru", "ON", "Ly", "J4"]
    omegas = [big_omega(PARIAHS[n]) for n in names]
    grand_total = sum(omegas)
    eng_actual = sum(omegas[:3])
    wth_actual = sum(omegas[3:])

    print(f"  Actual Omega values: {omegas}")
    print(f"  Grand total: {grand_total}")
    print(f"  Actual split: Engaged = {eng_actual}, Withdrawn = {wth_actual}")
    print()

    # Framework-significant pairs that sum to grand_total
    framework_pairs = []
    for a in range(1, grand_total):
        b = grand_total - a
        a_sig = a in FRAMEWORK_NUMBERS or is_fibonacci(a)
        b_sig = b in FRAMEWORK_NUMBERS or is_fibonacci(b)
        if a_sig and b_sig and a <= b:
            framework_pairs.append((a, b))

    print(f"  Framework-significant pairs summing to {grand_total}:")
    for a, b in framework_pairs:
        la = framework_label(a) or ("Fibonacci" if is_fibonacci(a) else "")
        lb = framework_label(b) or ("Fibonacci" if is_fibonacci(b) else "")
        marker = " <-- ACTUAL" if (a == eng_actual and b == wth_actual) or (a == wth_actual and b == eng_actual) else ""
        print(f"    ({a}, {b})  [{la}] + [{lb}]{marker}")

    n_sig_pairs = len(framework_pairs)
    # How many total distinct unordered pairs sum to grand_total?
    n_total_pairs = grand_total // 2  # pairs (a, grand_total-a) with a < grand_total-a
    p_any_sig = n_sig_pairs / n_total_pairs if n_total_pairs > 0 else 0
    print()
    print(f"  Total distinct unordered splits of {grand_total}: {n_total_pairs}")
    print(f"  Framework-significant pairs: {n_sig_pairs}")
    print(f"  P(random split is framework-significant) = {n_sig_pairs}/{n_total_pairs} = {p_any_sig:.4f}")

    # Monte Carlo: random assignment of 6 Big Omegas with same multiset
    # to engaged/withdrawn, check how often we get 46/80
    print()
    print("  Monte Carlo: shuffle the 6 Omega values into 2 groups of 3")

    from itertools import combinations
    # Exact enumeration: C(6,3) = 20 ways to pick 3 for "engaged"
    all_combos = list(combinations(range(6), 3))
    exact_46_80 = 0
    exact_sig = 0

    for combo in all_combos:
        eng_sum = sum(omegas[i] for i in combo)
        wth_sum = grand_total - eng_sum
        if eng_sum == 46 and wth_sum == 80:
            exact_46_80 += 1
        # Check if both are framework-significant
        eng_sig = eng_sum in FRAMEWORK_NUMBERS or is_fibonacci(eng_sum)
        wth_sig = wth_sum in FRAMEWORK_NUMBERS or is_fibonacci(wth_sum)
        if eng_sig and wth_sig:
            exact_sig += 1

    print(f"  Total ways to split 6 items into 3+3: {len(all_combos)}")
    print(f"  Splits giving (46, 80): {exact_46_80}/{len(all_combos)} = {exact_46_80/len(all_combos):.4f}")
    print(f"  Splits giving any framework-significant pair: {exact_sig}/{len(all_combos)} = {exact_sig/len(all_combos):.4f}")

    # Monte Carlo with random 6-tuples having same sum
    print()
    print("  Monte Carlo: 10,000 random 6-tuples with same sum as 2-exponents (sum=62)")

    two_exps = [PARIAHS[n][2] for n in names]
    two_sum = sum(two_exps)
    eng_2_actual = sum(two_exps[:3])  # 3+7+14 = 24
    wth_2_actual = sum(two_exps[3:])  # 9+8+21 = 38

    random.seed(42)
    N_TRIALS = 10000
    hit_actual = 0
    hit_any_sig = 0

    for _ in range(N_TRIALS):
        # Generate 6 random positive integers summing to two_sum
        # Use stick-breaking
        breaks = sorted(random.sample(range(1, two_sum), 5))
        vals = [breaks[0]] + [breaks[i] - breaks[i-1] for i in range(1, 5)] + [two_sum - breaks[4]]
        eng_s = sum(vals[:3])
        wth_s = two_sum - eng_s
        if (eng_s == eng_2_actual and wth_s == wth_2_actual):
            hit_actual += 1
        eng_fw = eng_s in FRAMEWORK_NUMBERS or is_fibonacci(eng_s)
        wth_fw = wth_s in FRAMEWORK_NUMBERS or is_fibonacci(wth_s)
        if eng_fw and wth_fw:
            hit_any_sig += 1

    print(f"  2-exponents: {two_exps}, sum = {two_sum}")
    print(f"  Actual 2-exp split: Engaged = {eng_2_actual}, Withdrawn = {wth_2_actual}")
    print(f"  Hits for exact ({eng_2_actual}, {wth_2_actual}): {hit_actual}/{N_TRIALS} = {hit_actual/N_TRIALS:.4f}")
    print(f"  Hits for any framework-significant pair: {hit_any_sig}/{N_TRIALS} = {hit_any_sig/N_TRIALS:.4f}")

    # Now the Big Omega null test: random 6-tuples summing to 126
    print()
    print(f"  Monte Carlo: 10,000 random 6-tuples with same sum as Big Omegas (sum={grand_total})")

    hit_46_80 = 0
    hit_sig_omega = 0

    for _ in range(N_TRIALS):
        breaks = sorted(random.sample(range(1, grand_total), 5))
        vals = [breaks[0]] + [breaks[i] - breaks[i-1] for i in range(1, 5)] + [grand_total - breaks[4]]
        eng_s = sum(vals[:3])
        wth_s = grand_total - eng_s
        if eng_s == 46 and wth_s == 80:
            hit_46_80 += 1
        eng_fw = eng_s in FRAMEWORK_NUMBERS or is_fibonacci(eng_s)
        wth_fw = wth_s in FRAMEWORK_NUMBERS or is_fibonacci(wth_s)
        if eng_fw and wth_fw:
            hit_sig_omega += 1

    print(f"  Hits for exact (46, 80): {hit_46_80}/{N_TRIALS} = {hit_46_80/N_TRIALS:.4f}")
    print(f"  Hits for any framework-significant pair: {hit_sig_omega}/{N_TRIALS} = {hit_sig_omega/N_TRIALS:.4f}")
    print()


# ═══════════════════════════════════════════════════════════════════
# 7. THE 126 DECOMPOSITION
# ═══════════════════════════════════════════════════════════════════

def section_126():
    print("=" * 80)
    print("SECTION 7: THE 126 DECOMPOSITION")
    print("=" * 80)
    print()

    names = ["J1", "J3", "Ru", "ON", "Ly", "J4"]
    omegas = [big_omega(PARIAHS[n]) for n in names]
    eng = sum(omegas[:3])
    wth = sum(omegas[3:])
    grand = eng + wth

    print(f"  Grand total Omega = {grand}")
    print()
    print(f"  126 = roots(E7)")
    print(f"      = dim(antisymmetric rep of SO(10))")
    print(f"      = dim(3-form on C9)")
    print(f"      = 2 x 63 = 2 x dim(su(8))")
    print()
    print(f"  Engaged = {eng}")
    if eng == 46:
        print(f"      = Monster 2-exponent")
        print(f"      = 2 x 23 (23 = pariah prime of J4)")
    print()
    print(f"  Withdrawn = {wth}")
    if wth == 80:
        print(f"      = hierarchy exponent (theta4^80 in Lambda)")
        print(f"      = sum of E-chain Coxeter numbers: h(E6)+h(E7)+h(E8)+20 = 12+18+30+20")
        print(f"      = 80S ribosome (total subunits in eukaryotic ribosome)")
        print(f"      = Mercury Z=80 (liquid metal, boundary element)")
    print()
    print("  SUMMARY:")
    print("  Pariah prime complexity = E7 roots.")
    print("  Engaged = Monster depth.")
    print("  Withdrawn = Hierarchy scale.")
    print()

    # Additional: per-group Omega values and their significance
    print("  Per-group Omega:")
    for n, o in zip(names, omegas):
        sig = framework_label(o)
        axis = "ENGAGED" if n in ENGAGED else "WITHDRAWN"
        print(f"    {n:3s} ({axis:9s}): Omega = {o:3d}  {sig}")
    print()

    # Check: sum of engaged Omegas = Monster 2-exponent
    print("  Cross-check:")
    print(f"    Omega(J1) + Omega(J3) + Omega(Ru) = {omegas[0]} + {omegas[1]} + {omegas[2]} = {eng}")
    print(f"    Monster 2-exponent = 46  =>  {'MATCH' if eng == 46 else 'NO MATCH'}")
    print()
    print(f"    Omega(ON) + Omega(Ly) + Omega(J4) = {omegas[3]} + {omegas[4]} + {omegas[5]} = {wth}")
    print(f"    Hierarchy exponent = 80  =>  {'MATCH' if wth == 80 else 'NO MATCH'}")
    print()
    print(f"    46 + 80 = {eng + wth}")
    print(f"    roots(E7) = 126  =>  {'MATCH' if eng + wth == 126 else 'NO MATCH'}")
    print()


# ═══════════════════════════════════════════════════════════════════
# ADDITIONAL: Prime set analysis
# ═══════════════════════════════════════════════════════════════════

def section_prime_sets():
    print("=" * 80)
    print("SECTION 8: PRIME SET ANALYSIS (bonus)")
    print("=" * 80)
    print()

    names = ["J1", "J3", "Ru", "ON", "Ly", "J4"]
    for n in names:
        primes = sorted(PARIAHS[n].keys())
        print(f"  {n:3s}: primes = {primes}  (count = {len(primes)})")

    # Unique primes per group (primes appearing in exactly one pariah)
    from collections import Counter
    prime_counts = Counter()
    for fac in PARIAHS.values():
        for p in fac:
            prime_counts[p] += 1

    print()
    print("  Prime occurrence counts across pariahs:")
    for p in sorted(prime_counts.keys()):
        groups = [n for n in names if p in PARIAHS[n]]
        print(f"    p={p:>3d}: appears in {prime_counts[p]} group(s): {', '.join(groups)}")

    # Primes unique to each axis
    eng_primes = set()
    wth_primes = set()
    for n in ENGAGED:
        eng_primes.update(PARIAHS[n].keys())
    for n in WITHDRAWN:
        wth_primes.update(PARIAHS[n].keys())

    only_eng = eng_primes - wth_primes
    only_wth = wth_primes - eng_primes
    shared = eng_primes & wth_primes

    print()
    print(f"  Engaged-only primes: {sorted(only_eng)}")
    print(f"  Withdrawn-only primes: {sorted(only_wth)}")
    print(f"  Shared primes: {sorted(shared)}")
    print()

    # Alien primes
    alien = {37, 43, 67}
    alien_in_eng = alien & eng_primes
    alien_in_wth = alien & wth_primes
    print(f"  Alien primes {{37, 43, 67}}:")
    print(f"    In engaged: {sorted(alien_in_eng) if alien_in_eng else 'NONE'}")
    print(f"    In withdrawn: {sorted(alien_in_wth) if alien_in_wth else 'NONE'}")
    if not alien_in_eng and alien_in_wth == alien:
        print(f"    ALL three alien primes are EXCLUSIVELY in the withdrawn axis.")
    print()


def section_alien_gap_identities():
    """Second independent lock family on the alien prime set {37, 43, 67}.

    Beyond the Big Omega (46, 80) partition above, the set itself carries
    six clean integer locks tying it to named framework structures. Full
    verification and null test: enrich_c2_gap_identities.py.
    """
    print("=" * 80)
    print("ALIEN PRIME GAP AND GENUS LOCKS  (cross-ref enrich_c2_gap_identities.py)")
    print("=" * 80)
    p1, p2, p3 = 37, 43, 67
    print(f"  Gap identities on {{37, 43, 67}}:")
    print(f"    43 - 37 = {p2 - p1:2}   = |S_3|")
    print(f"    67 - 43 = {p3 - p2:2}   = c(Monster VOA)")
    print(f"    67 - 37 = {p3 - p1:2}   = h(E_8) Coxeter number")
    print(f"    37 + 43 = {p1 + p2:2}   = hierarchy exponent v/M_Pl")
    print()
    print(f"  Genera of modular curves X_0(p):")
    print(f"    g(X_0(37)) = 2, g(X_0(43)) = 3, g(X_0(67)) = 5")
    print(f"    {{2, 3, 5}} = icosahedral Schwarz triangle vertices")
    print(f"    sum of genera = 2 + 3 + 5 = 10 = xi_inflation = 240/24")
    print(f"    product of genera = 2 * 3 * 5 = 30 = h(E_8)")
    print()
    print(f"  Null test: of 13244 prime triples in [5, 200], exactly ONE triple")
    print(f"  {{37, 43, 67}} satisfies all four gap identities AND the three")
    print(f"  genus values simultaneously. See enrich_c2_gap_identities.py.")
    print()


# ═══════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print()
    print("  PARIAH PRIME PARTITION ANALYSIS")
    print("  Complete prime-power structure of the 6 pariah sporadic groups")
    print()

    section_verify()
    prime_data, all_primes = section_per_prime()
    section_big_omega()
    section_2exp()
    section_cross_prime(prime_data, all_primes)
    section_axis_products()
    section_null_test()
    section_126()
    section_prime_sets()
    section_alien_gap_identities()

    print("=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)
