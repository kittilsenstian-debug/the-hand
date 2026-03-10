"""
Statistical analysis: Are the pariah-only primes {37, 43, 67} having
genus values {2, 3, 5} (consecutive Fibonacci numbers) surprising?

Analysis:
1. Compute g(X_0(p)) for all primes p < 200
2. Verify which primes are truly "pariah-only" (in pariah orders, not in Monster)
3. Assess statistical significance of the Fibonacci coincidence
"""

from math import gcd, floor, sqrt
from itertools import combinations

# ============================================================
# PART 1: Genus computation for X_0(p), p prime
# ============================================================

def legendre_symbol(a, p):
    """Compute the Legendre symbol (a/p) for odd prime p."""
    if a % p == 0:
        return 0
    val = pow(a, (p - 1) // 2, p)
    return val if val <= 1 else val - p  # convert p-1 to -1

def genus_X0_prime(p):
    """
    Genus of X_0(p) for prime p.

    Formula (standard, e.g. Diamond-Shurman Prop. 3.1.1):
    g = 1 + (p-13)/12 + floor((p-1)/4)*0 ...

    More precisely for prime N=p:
    g = 1 + (p+1)/12 - nu2/4 - nu3/3 - 1/2
    Wait, let me use the exact formula.

    For N=p prime, the genus formula is:
    g(X_0(p)) = floor((p-13)/12) + delta
    where delta depends on p mod 12.

    Actually, the clean formula:
    g = 1 + mu/12 - nu2/4 - nu3/3 - nu_inf/2
    where mu = p+1 (index of Gamma_0(p) in SL(2,Z))
    nu2 = 1 + (-1|p) (number of elliptic points of order 2)
    nu3 = 1 + (-3|p) (number of elliptic points of order 3)
    nu_inf = 2 (number of cusps for prime level)

    So: g = 1 + (p+1)/12 - (1+(-1|p))/4 - (1+(-3|p))/3 - 1
         = (p+1)/12 - (1+(-1|p))/4 - (1+(-3|p))/3

    This gives a rational number; genus is always a non-negative integer.
    Let me verify with known values first.
    """
    if p == 2:
        # Special case
        return 0
    if p == 3:
        return 0

    mu = p + 1  # index

    # Legendre symbols
    leg_minus1 = legendre_symbol(-1, p)  # (-1|p)
    leg_minus3 = legendre_symbol(-3, p)  # (-3|p)

    nu2 = 1 + leg_minus1
    nu3 = 1 + leg_minus3
    nu_inf = 2  # for prime level

    # Genus formula
    g = 1 + mu/12 - nu2/4 - nu3/3 - nu_inf/2

    # Should be integer (or very close)
    g_int = round(g)
    assert abs(g - g_int) < 0.001, f"Non-integer genus {g} for p={p}"
    return max(0, g_int)

def sieve_primes(n):
    """Simple sieve of Eratosthenes."""
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, n+1, i):
                is_prime[j] = False
    return [p for p in range(2, n+1) if is_prime[p]]

# Fibonacci numbers (enough for our range)
def fibonacci_set(max_val):
    fibs = set()
    a, b = 0, 1
    while a <= max_val:
        fibs.add(a)
        a, b = b, a + b
    return fibs

# Consecutive Fibonacci triples
def consecutive_fib_triples(max_val):
    """Return all consecutive Fibonacci triples (a, b, c) with c <= max_val."""
    fibs = []
    a, b = 0, 1
    while a <= max_val:
        fibs.append(a)
        a, b = b, a + b
    triples = []
    for i in range(len(fibs) - 2):
        if fibs[i+2] <= max_val:
            triples.append((fibs[i], fibs[i+1], fibs[i+2]))
    return triples

print("=" * 70)
print("PART 1: Genus of X_0(p) for primes p < 200")
print("=" * 70)

primes = sieve_primes(200)
fibs = fibonacci_set(200)

# Known values for verification
known = {2: 0, 3: 0, 5: 0, 7: 0, 11: 1, 13: 0, 17: 1, 19: 1, 23: 2,
         29: 2, 31: 2, 37: 2, 41: 3, 43: 3, 47: 4, 53: 4, 59: 5,
         61: 4, 67: 5, 71: 6, 73: 5, 79: 6, 83: 7, 89: 7}

print(f"\n{'p':>5} {'genus':>6} {'Fib?':>5}  {'Verified':>10}")
print("-" * 35)

genus_map = {}
fib_primes = []
for p in primes:
    g = genus_X0_prime(p)
    genus_map[p] = g
    is_fib = g in fibs

    # Verification against known values
    verify = ""
    if p in known:
        verify = "OK" if known[p] == g else f"MISMATCH (expected {known[p]})"

    marker = " <-- FIB" if is_fib else ""
    print(f"{p:>5} {g:>6} {str(is_fib):>5}  {verify:>10}{marker}")

    if is_fib:
        fib_primes.append((p, g))

print(f"\nPrimes with Fibonacci genus (p < 200): {len(fib_primes)} out of {len(primes)}")
for p, g in fib_primes:
    print(f"  p={p}, g={g}")

# ============================================================
# PART 2: Which primes are "pariah-only"?
# ============================================================

print("\n" + "=" * 70)
print("PART 2: Pariah group orders and Monster order — prime factorizations")
print("=" * 70)

# Monster group order (exact)
# |M| = 2^46 · 3^20 · 5^9 · 7^6 · 11^2 · 13^3 · 17 · 19 · 23 · 29 · 31 · 41 · 47 · 59 · 71
monster_primes = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 41, 47, 59, 71}

print(f"\nMonster primes: {sorted(monster_primes)}")
print(f"Number of Monster primes: {len(monster_primes)}")

# The 6 pariah sporadic groups and their orders
# Sources: ATLAS of finite groups / standard references
pariah_orders = {
    "J1": {
        "order": 175560,
        "factored": "2^3 · 3 · 5 · 7 · 11 · 19",
        "primes": {2, 3, 5, 7, 11, 19}
    },
    "J3": {
        "order": 50232960,
        "factored": "2^7 · 3^5 · 5 · 10 · 17 · 19",
        "primes": {2, 3, 5, 17, 19}
    },
    "J4": {
        "order": 86775571046077562880,
        "factored": "2^21 · 3^3 · 5 · 7 · 11^3 · 23 · 29 · 31 · 37 · 43",
        "primes": {2, 3, 5, 7, 11, 23, 29, 31, 37, 43}
    },
    "Ru": {
        "order": 145926144000,
        "factored": "2^14 · 3^3 · 5^3 · 7 · 13 · 29",
        "primes": {2, 3, 5, 7, 13, 29}
    },
    "O'N": {
        "order": 460815505920,
        "factored": "2^9 · 3^4 · 5 · 7^3 · 11 · 19 · 31",
        "primes": {2, 3, 5, 7, 11, 19, 31}
    },
    "Ly": {
        "order": 51765179004000000,
        "factored": "2^8 · 3^7 · 5^6 · 7 · 11 · 31 · 37 · 67",
        "primes": {2, 3, 5, 7, 11, 31, 37, 67}
    }
}

# Collect all pariah primes
all_pariah_primes = set()
for name, data in pariah_orders.items():
    all_pariah_primes |= data["primes"]
    print(f"\n{name}: {data['factored']}")
    print(f"  Primes: {sorted(data['primes'])}")

print(f"\nAll primes dividing any pariah order: {sorted(all_pariah_primes)}")

# Pariah-only primes: in at least one pariah, NOT in Monster
pariah_only = all_pariah_primes - monster_primes
print(f"\nPariah-ONLY primes (in pariah but NOT Monster): {sorted(pariah_only)}")

# Check which pariah groups contain each pariah-only prime
for p in sorted(pariah_only):
    groups = [name for name, data in pariah_orders.items() if p in data["primes"]]
    g = genus_map.get(p, "N/A")
    print(f"  p={p}: genus={g}, appears in {groups}")

# Primes in BOTH Monster and pariah
shared = all_pariah_primes & monster_primes
print(f"\nPrimes in BOTH Monster and pariah: {sorted(shared)}")

# Verify the claim
print(f"\n*** CLAIM CHECK: pariah-only primes = {{37, 43, 67}}? ***")
if pariah_only == {37, 43, 67}:
    print("  CONFIRMED: {37, 43, 67} are the only pariah-only primes.")
else:
    print(f"  RESULT: pariah-only primes = {sorted(pariah_only)}")

# Check genera
genera_of_pariah_only = sorted([genus_map[p] for p in pariah_only])
print(f"\n*** CLAIM CHECK: genera = {{2, 3, 5}}? ***")
print(f"  Genera: {genera_of_pariah_only}")
if genera_of_pariah_only == [2, 3, 5]:
    print("  CONFIRMED: genera are {2, 3, 5} = consecutive Fibonacci numbers.")
else:
    print("  NOT confirmed as stated.")

# ============================================================
# PART 3: Statistical significance
# ============================================================

print("\n" + "=" * 70)
print("PART 3: Statistical significance analysis")
print("=" * 70)

# Q1: How many primes p<200 have Fibonacci genus?
print(f"\nPrimes with Fibonacci genus (out of {len(primes)} primes < 200):")
print(f"  Count: {len(fib_primes)}")
print(f"  Fraction: {len(fib_primes)/len(primes):.3f}")

# Q2: Among primes < 100 (closer to the pariah range)
primes_100 = [p for p in primes if p < 100]
fib_primes_100 = [(p, g) for p, g in fib_primes if p < 100]
print(f"\nPrimes < 100 with Fibonacci genus: {len(fib_primes_100)} out of {len(primes_100)}")
for p, g in fib_primes_100:
    print(f"  p={p}, g={g}")

# Q3: How many 3-element subsets of primes < 100 have genera = 3 consecutive Fibonacci?
consec_fib = consecutive_fib_triples(50)  # genus won't exceed ~50 for p<200
print(f"\nConsecutive Fibonacci triples up to genus 50: {consec_fib}")

# For each consecutive Fibonacci triple, find primes with those genera
print("\nFor each consecutive Fibonacci triple (a, b, c):")
print("How many 3-subsets of primes < 100 have genera {a, b, c}?")

genus_to_primes_100 = {}
for p in primes_100:
    g = genus_map[p]
    if g not in genus_to_primes_100:
        genus_to_primes_100[g] = []
    genus_to_primes_100[g].append(p)

total_triples_matching = 0
for a, b, c in consec_fib:
    pa = genus_to_primes_100.get(a, [])
    pb = genus_to_primes_100.get(b, [])
    pc = genus_to_primes_100.get(c, [])
    count = len(pa) * len(pb) * len(pc)
    total_triples_matching += count
    if count > 0 or (a, b, c) == (2, 3, 5):
        print(f"  ({a}, {b}, {c}): {len(pa)}×{len(pb)}×{len(pc)} = {count} triples")
        if pa: print(f"    genus={a}: {pa}")
        if pb: print(f"    genus={b}: {pb}")
        if pc: print(f"    genus={c}: {pc}")

total_3subsets = len(primes_100) * (len(primes_100)-1) * (len(primes_100)-2) // 6
print(f"\nTotal 3-element subsets of primes < 100: {total_3subsets}")
print(f"3-subsets with ANY consecutive Fibonacci genera: {total_triples_matching}")
print(f"Probability (random 3-subset has consecutive Fib genera): {total_triples_matching/total_3subsets:.6f}")

# Q4: The specific triple {2, 3, 5}
pa = genus_to_primes_100.get(2, [])
pb = genus_to_primes_100.get(3, [])
pc = genus_to_primes_100.get(5, [])
count_235 = len(pa) * len(pb) * len(pc)
print(f"\n3-subsets with genera exactly {{2, 3, 5}}: {count_235}")
print(f"  genus=2 primes: {pa}")
print(f"  genus=3 primes: {pb}")
print(f"  genus=5 primes: {pc}")
print(f"Probability of {{2,3,5}} by random 3-subset: {count_235/total_3subsets:.6f}")

# Q5: But the real question - given that there are EXACTLY 3 pariah-only primes,
# what's the probability their genera form consecutive Fibonacci numbers?
print("\n" + "-" * 50)
print("KEY QUESTION: Given 3 specific primes, what's P(consecutive Fibonacci genera)?")
print("-" * 50)

# The genera of primes < 100 range from 0 to about 7
all_genera_100 = [genus_map[p] for p in primes_100]
max_g = max(all_genera_100)
print(f"\nGenera range for primes < 100: 0 to {max_g}")
print(f"Genus distribution:")
for g in range(max_g + 1):
    count = all_genera_100.count(g)
    if count > 0:
        fib_mark = " (Fibonacci)" if g in fibs else ""
        print(f"  g={g}: {count} primes{fib_mark}")

# Number of ordered triples that are consecutive Fibonacci
# Among genera 0-7: consecutive Fib triples are (0,1,1), (1,1,2), (1,2,3), (2,3,5)
relevant_fib_triples = [(a,b,c) for a,b,c in consec_fib if c <= max_g]
print(f"\nConsecutive Fibonacci triples within genus range: {relevant_fib_triples}")

# Monte Carlo: pick 3 random primes from those < 100, check if genera are consec Fib
import random
random.seed(42)
N_trials = 1_000_000
hits = 0

fib_triple_set = set()
for a, b, c in consec_fib:
    fib_triple_set.add((a, b, c))

for _ in range(N_trials):
    sample = random.sample(primes_100, 3)
    genera = tuple(sorted([genus_map[p] for p in sample]))
    if genera in fib_triple_set:
        hits += 1

p_mc = hits / N_trials
print(f"\nMonte Carlo ({N_trials:,} trials): P(3 random primes < 100 have consec Fib genera) = {p_mc:.6f}")
print(f"  That's about 1 in {1/p_mc:.0f}" if p_mc > 0 else "  Zero hits!")

# Q6: But there's a subtlety. The pariah-only primes are NOT random —
# they're LARGE primes (37, 43, 67). What if we condition on being > 30?
print("\n" + "-" * 50)
print("CONDITIONING: primes > 30 and < 100")
print("-" * 50)
large_primes_100 = [p for p in primes_100 if p > 30]
print(f"Primes 30 < p < 100: {large_primes_100}")
genera_large = {p: genus_map[p] for p in large_primes_100}
print("Genera:", {p: g for p, g in sorted(genera_large.items())})

hits_large = 0
for _ in range(N_trials):
    sample = random.sample(large_primes_100, 3)
    genera = tuple(sorted([genus_map[p] for p in sample]))
    if genera in fib_triple_set:
        hits_large += 1

p_mc_large = hits_large / N_trials
print(f"Monte Carlo: P(3 random primes from 30<p<100 have consec Fib genera) = {p_mc_large:.6f}")
if p_mc_large > 0:
    print(f"  That's about 1 in {1/p_mc_large:.0f}")

# Q7: Exact count for large primes
print("\nExact enumeration for primes 30 < p < 100:")
total_large_triples = len(large_primes_100) * (len(large_primes_100)-1) * (len(large_primes_100)-2) // 6
print(f"Total 3-subsets: {total_large_triples}")

genus_to_large = {}
for p in large_primes_100:
    g = genus_map[p]
    if g not in genus_to_large:
        genus_to_large[g] = []
    genus_to_large[g].append(p)

exact_hits = 0
for a, b, c in consec_fib:
    pa = genus_to_large.get(a, [])
    pb = genus_to_large.get(b, [])
    pc = genus_to_large.get(c, [])
    count = len(pa) * len(pb) * len(pc)
    exact_hits += count
    if count > 0:
        print(f"  ({a},{b},{c}): {len(pa)}×{len(pb)}×{len(pc)} = {count}")

print(f"Total hits: {exact_hits} / {total_large_triples}")
print(f"Exact probability: {exact_hits/total_large_triples:.6f} = 1 in {total_large_triples/exact_hits:.1f}")

# ============================================================
# PART 4: Broader look — genus distribution and Fibonacci density
# ============================================================

print("\n" + "=" * 70)
print("PART 4: How dense are Fibonacci numbers among small integers?")
print("=" * 70)

# Fibonacci numbers up to 10: {0, 1, 2, 3, 5, 8}
# That's 6 out of 11 values (0-10), or 55%!
# The genera of our primes 30 < p < 100 range from 2 to 7.
# Fibonacci numbers in {2,3,4,5,6,7}: {2, 3, 5} = 3 out of 6 = 50%

print("\nFibonacci numbers among small integers:")
for n in [5, 8, 10, 15, 20]:
    fib_count = len([f for f in fibonacci_set(n) if f <= n])
    print(f"  0..{n}: {fib_count}/{n+1} = {fib_count/(n+1):.1%} are Fibonacci")

genus_range = range(2, 8)  # the actual range for primes 30-100
fib_in_range = [g for g in genus_range if g in fibs]
print(f"\nIn the actual genus range {{2..7}} for primes 30<p<100:")
print(f"  Fibonacci: {fib_in_range} = {len(fib_in_range)}/{len(list(genus_range))} = {len(fib_in_range)/len(list(genus_range)):.1%}")

# ============================================================
# PART 5: The REAL question — consecutive Fibonacci specifically
# ============================================================

print("\n" + "=" * 70)
print("PART 5: How many 3-subsets of primes have STRICTLY CONSECUTIVE Fib genera?")
print("=" * 70)

# Among ALL primes < 200
genus_to_all = {}
for p in primes:
    g = genus_map[p]
    if g not in genus_to_all:
        genus_to_all[g] = []
    genus_to_all[g].append(p)

print("\nFor primes < 200, consecutive Fibonacci triples that are achievable:")
for a, b, c in consec_fib:
    pa = genus_to_all.get(a, [])
    pb = genus_to_all.get(b, [])
    pc = genus_to_all.get(c, [])
    count = len(pa) * len(pb) * len(pc)
    if count > 0:
        print(f"  ({a},{b},{c}): {len(pa)}×{len(pb)}×{len(pc)} = {count} ordered triples")

# ============================================================
# PART 6: Coxeter number connection check
# ============================================================

print("\n" + "=" * 70)
print("PART 6: Additional claimed patterns")
print("=" * 70)

# Claim: genus = Coxeter number h / 6?
# Coxeter numbers: A_n: n+1, D_n: 2(n-1), E6: 12, E7: 18, E8: 30
# For p=37: g=2. h/6=2 → h=12 (E6 Coxeter number!)
# For p=43: g=3. h/6=3 → h=18 (E7 Coxeter number!)
# For p=67: g=5. h/6=5 → h=30 (E8 Coxeter number!)

print("\nClaim: genus = Coxeter_number / 6?")
coxeter = {"E6": 12, "E7": 18, "E8": 30}
for p, name in [(37, "E6"), (43, "E7"), (67, "E8")]:
    g = genus_map[p]
    h = coxeter[name]
    print(f"  p={p}: g={g}, {name} Coxeter h={h}, h/6={h/6:.1f}, match={g == h/6}")

# This is also a pattern. But is it forced by both being related to the same prime?
print("\nNote: This adds another layer, but it could be coincidental selection.")
print("The Coxeter numbers of E6, E7, E8 are 12, 18, 30.")
print("Divided by 6: 2, 3, 5. These ARE the genera. But why /6?")
print("Because X_0(p) genus ~ p/12 for large p, and the Coxeter numbers")
print("happen to scale with the primes in a compatible way? Let's check:")
for p, name in [(37, "E6"), (43, "E7"), (67, "E8")]:
    h = coxeter[name]
    print(f"  p={p}: g(p)={genus_map[p]}, p/12={p/12:.2f}, h/6={h/6}")

# ============================================================
# SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

print("""
VERIFIED FACTS:
1. The pariah-only primes ARE exactly {37, 43, 67}. CONFIRMED.
2. Their genera ARE {2, 3, 5}. CONFIRMED.
3. {2, 3, 5} ARE consecutive Fibonacci numbers. CONFIRMED.

STATISTICAL ASSESSMENT:
""")

print(f"- Among primes 30 < p < 100 ({len(large_primes_100)} primes):")
print(f"  genera range from {min(genus_map[p] for p in large_primes_100)} to {max(genus_map[p] for p in large_primes_100)}")
print(f"  P(random 3-subset has consecutive Fibonacci genera) = {exact_hits/total_large_triples:.4f}")
print(f"  = about 1 in {total_large_triples/exact_hits:.0f}")

print(f"""
- Fibonacci numbers are DENSE among small integers:
  In the range 2-7 (actual genus range), 3/6 = 50% are Fibonacci.

- The "consecutive" constraint is the main filter:
  Getting 3 Fibonacci genera is not hard (~50% chance per genus).
  Getting them CONSECUTIVE is moderately constraining.

- But {2, 3, 5} is the ONLY consecutive Fibonacci triple in range 2-7.
  So the question reduces to: do the 3 pariah-only primes
  each land on genus 2, 3, and 5 respectively?

BOTTOM LINE:
  The probability is about 1 in {total_large_triples/exact_hits:.0f} — {'' if exact_hits/total_large_triples < 0.01 else 'NOT '}extremely rare.
  It is a genuine coincidence worth noting, but not astronomically unlikely.
  The Coxeter number connection (h/6 = g) adds interest but may be
  a restatement rather than an independent fact.
""")

# Final: what fraction of the genera are individually Fibonacci?
print("Individual genus probabilities:")
for p in [37, 43, 67]:
    g = genus_map[p]
    # How many primes 30<p<100 have this genus?
    same_g = [q for q in large_primes_100 if genus_map[q] == g]
    print(f"  p={p}, g={g}: {len(same_g)}/{len(large_primes_100)} primes have this genus")
    print(f"    Those primes: {same_g}")
