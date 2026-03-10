"""
Golden Scheme Analysis: x^2 - x - 1 = 0 as arithmetic variety

Analyzes the fiber structure of Spec(Z[phi]) at each prime,
connecting Monster primes, pariah primes, splitting behavior,
Frobenius elements, Pisano periods, and the origin of integer 3.

No dependencies. Run: python golden_scheme_analysis.py
"""

# ──────────────────────────────────────────────────────────────
# Pariah group orders (prime factorizations)
# ──────────────────────────────────────────────────────────────

PARIAH_ORDERS = {
    'J1':  {2:3,  3:1, 5:1, 7:1, 11:1, 19:1},
    'J3':  {2:7,  3:5, 5:1, 17:1, 19:1},
    'J4':  {2:21, 3:3, 5:1, 7:1, 11:3, 23:1, 29:1, 31:1, 37:1, 43:1},
    'Ly':  {2:8,  3:7, 5:6, 7:1, 11:1, 31:1, 37:1, 67:1},
    'Ru':  {2:14, 3:3, 5:3, 7:1, 13:1, 29:1},
    'ON':  {2:9,  3:4, 5:1, 7:3, 11:1, 19:1, 31:1},
}

MONSTER_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 41, 47, 59, 71]

def all_pariah_primes():
    s = set()
    for primes in PARIAH_ORDERS.values():
        s.update(primes.keys())
    return sorted(s)

def solve_mod(p):
    """Solutions to x^2 - x - 1 = 0 mod p"""
    return [x for x in range(p) if (x*x - x - 1) % p == 0]

def splitting_type(p):
    if p == 5:
        return 'RAMIFIES'
    sols = solve_mod(p)
    return 'SPLITS' if len(sols) == 2 else 'INERT'

def pisano_period(p):
    """Period of Fibonacci sequence mod p"""
    prev, curr = 0, 1
    for i in range(1, 6*p + 3):
        prev, curr = curr, (prev + curr) % p
        if prev == 0 and curr == 1:
            return i
    return -1

def factorize(n):
    if n <= 1:
        return []
    factors = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1
    if n > 1:
        factors.append(n)
    return factors

# ──────────────────────────────────────────────────────────────
# Main analysis
# ──────────────────────────────────────────────────────────────

if __name__ == '__main__':
    pariah_p = all_pariah_primes()
    all_primes = sorted(set(MONSTER_PRIMES + pariah_p))

    monster_only = [p for p in MONSTER_PRIMES if p not in pariah_p]
    pariah_only = [p for p in pariah_p if p not in MONSTER_PRIMES]
    shared = [p for p in MONSTER_PRIMES if p in pariah_p]

    print("=" * 75)
    print("GOLDEN SCHEME: Spec(Z[x]/(x^2 - x - 1)) FIBER ANALYSIS")
    print("=" * 75)
    print()

    print(f"Monster primes (supersingular): {MONSTER_PRIMES}")
    print(f"All pariah primes:              {pariah_p}")
    print(f"Monster-only:                   {monster_only}")
    print(f"Pariah-only:                    {pariah_only}")
    print(f"Shared:                         {shared}")
    print()

    header = f"{'p':>4} | {'mod5':>4} | {'Type':>8} | {'phi mod p':>14} | {'M?':>3} | {'P?':>3} | {'pi(p)':>6} | {'2(p+1)':>6} | {'p-1':>4}"
    print(header)
    print("-" * len(header))

    for p in all_primes:
        sols = solve_mod(p)
        stype = splitting_type(p)
        in_m = 'M' if p in MONSTER_PRIMES else ' '
        in_p = 'P' if p in pariah_p else ' '
        pi_p = pisano_period(p)
        phi_str = ','.join(str(s) for s in sols) if sols else f'F_{p}^2'

        print(f"{p:>4} | {p%5:>4} | {stype:>8} | {phi_str:>14} | {in_m:>3} | {in_p:>3} | {pi_p:>6} | {2*(p+1):>6} | {p-1:>4}")

    print()
    print("=" * 75)
    print("KEY RESULT: PARIAH-ONLY PRIMES ARE ALL INERT")
    print("=" * 75)
    print()

    m_only_split = sum(1 for p in monster_only if splitting_type(p) == 'SPLITS')
    m_only_inert = sum(1 for p in monster_only if splitting_type(p) == 'INERT')
    p_only_split = sum(1 for p in pariah_only if splitting_type(p) == 'SPLITS')
    p_only_inert = sum(1 for p in pariah_only if splitting_type(p) == 'INERT')

    print(f"Monster-only: {m_only_split}/{len(monster_only)} split, {m_only_inert}/{len(monster_only)} inert")
    print(f"Pariah-only:  {p_only_split}/{len(pariah_only)} split, {p_only_inert}/{len(pariah_only)} inert")
    print(f"P(all 3 inert by chance) = (1/2)^3 = {0.5**3:.1%}")
    print()

    print("Frobenius at Monster-only primes:")
    for p in monster_only:
        frob = 'id (phi visible)' if splitting_type(p) == 'SPLITS' else 'sigma (phi hidden)'
        print(f"  Frob_{p} = {frob}")

    print()
    print("Frobenius at Pariah-only primes:")
    for p in pariah_only:
        frob = 'id (phi visible)' if splitting_type(p) == 'SPLITS' else 'sigma (phi hidden)'
        print(f"  Frob_{p} = {frob}")

    print()
    print("=" * 75)
    print("THREE ROUTES TO 3")
    print("=" * 75)
    print()
    print("Route 1 (fiber at p=2): phi generates F_4 = GF(4), |F_4*| = 3")
    print("  x^2 - x - 1 = x^2 + x + 1 mod 2 (irreducible)")
    print("  F_4 = {0, 1, phi, phi+1}, multiplicative order of phi = 3")
    print()
    print("Route 2 (generic fiber): 744 = 3 x 248")
    print("  j(tau) = q^{-1} + 744 + ..., and dim(E_8) = 248")
    print("  ONLY E_8 has its dimension divide 744 among exceptional algebras")
    print()
    sols_5 = solve_mod(5)
    print(f"Route 3 (fiber at p=5): phi = {sols_5[0]} mod 5")
    print(f"  {sols_5[0]}^2 - {sols_5[0]} - 1 = {sols_5[0]**2 - sols_5[0] - 1} = 0 mod 5. CHECK.")
    print()

    print("=" * 75)
    print("PISANO PERIOD ANOMALY")
    print("=" * 75)
    print()
    print("Inert primes: pi(p) vs 2(p+1)")
    for p in all_primes:
        if splitting_type(p) == 'INERT':
            pi_p = pisano_period(p)
            ratio = pi_p / (2*(p+1))
            tag = ''
            if p in monster_only:
                tag = ' <-- MONSTER-ONLY'
            elif p in pariah_only:
                tag = ' <-- PARIAH-ONLY (maximal!)'
            print(f"  p={p:>3}: pi(p)={pi_p:>4}, 2(p+1)={2*(p+1):>4}, ratio={ratio:.4f}{tag}")

    print()
    print("p=47 is the ONLY Monster-only inert prime.")
    print("Its Pisano period 32 = 96/3 is exactly 1/3 of the maximum.")
    print("All pariah-only primes achieve the MAXIMUM Pisano period.")

    print()
    print("=" * 75)
    print("ADELIC PERSPECTIVE")
    print("=" * 75)
    print()
    print("phi is a UNIT in Z[phi] (since phi * (-1/phi) = -1).")
    print("Therefore |phi|_p = 1 for ALL primes p.")
    print("The 'size' of phi lives entirely at the archimedean place.")
    print("p-adic worlds detect phi only through Frobenius (Galois action).")
    print()
    print("Split primes: Frobenius = id. phi is 'just a number' in F_p.")
    print("Inert primes: Frobenius = sigma. phi is 'entangled with its conjugate.'")
    print("The Monster lives where phi is 'just a number.'")
    print("The pariahs live where phi is 'entangled.'")
