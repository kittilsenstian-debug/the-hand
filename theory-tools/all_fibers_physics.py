#!/usr/bin/env python3
"""
all_fibers_physics.py — Complete landscape of physics at every prime fiber
=========================================================================

The fundamental equation q + q² = 1 defines Spec(Z[φ]).
At each prime p, this equation reduces mod p, giving a "fiber" — a universe
with its own compressed physics.

For each prime p ≤ 100 we compute:
  - Classification: SPLIT (two roots in GF(p)), INERT (roots in GF(p²)), RAMIFIED (p=5)
  - The golden ratio φ mod p (or in GF(p²))
  - Modular-form shadows: η(q), θ₃(q), θ₄(q) mod p
  - Which "forces" survive (strong ~ η≠0, weak ~ θ₃≠θ₄, EM ~ 1/α defined)
  - Multiplicative order of q (controls when η dies)
  - Connection to sporadic groups

Key insight: η(q) = q^(1/24) · ∏(1-qⁿ). In finite fields, if q has finite
multiplicative order m, then q^m = 1, so (1-q^m) = 0, killing the product.
Thus η = 0 whenever ord(q) is in the product range, i.e., ord(q) < ∞ — which
is ALWAYS in a finite field. The question is whether we truncate the product
at n < ord(q), or whether the full product dies.

We handle the q^(1/24) prefactor by working with η²⁴ = Δ = q · ∏(1-qⁿ)²⁴
when 24th roots don't exist.

Standard Python, no dependencies.
"""

import sys
import io
import math

# Ensure UTF-8 output
if hasattr(sys.stdout, 'buffer'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


# =============================================================================
# ARITHMETIC UTILITIES
# =============================================================================

def is_prime(n):
    if n < 2: return False
    if n < 4: return True
    if n % 2 == 0 or n % 3 == 0: return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0: return False
        i += 6
    return True

def primes_up_to(n):
    return [p for p in range(2, n + 1) if is_prime(p)]

def mod_inv(a, p):
    """Multiplicative inverse of a mod p via Fermat."""
    a = a % p
    if a == 0:
        return None
    return pow(a, p - 2, p)

def mod_sqrt(a, p):
    """All square roots of a mod p (brute force, p small)."""
    a = a % p
    return [x for x in range(p) if (x * x) % p == a]

def mult_order(a, p):
    """Multiplicative order of a in GF(p). Returns None if a=0."""
    a = a % p
    if a == 0:
        return None
    val = a
    for k in range(1, p):
        if val == 1:
            return k
        val = (val * a) % p
    return p - 1  # should not reach here for prime p


# =============================================================================
# GF(p²) ARITHMETIC (for inert primes)
# =============================================================================

class GFp2:
    """
    Element of GF(p²) = GF(p)[x]/(x²-x-1).
    Elements represented as (a, b) meaning a + b*φ where φ²=φ+1.
    """
    def __init__(self, a, b, p):
        self.a = a % p
        self.b = b % p
        self.p = p

    def __repr__(self):
        if self.b == 0:
            return f"{self.a}"
        elif self.a == 0:
            return f"{self.b}φ"
        else:
            return f"{self.a}+{self.b}φ"

    def __eq__(self, other):
        if isinstance(other, int):
            return self.a == other % self.p and self.b == 0
        return self.a == other.a and self.b == other.b and self.p == other.p

    def __add__(self, other):
        if isinstance(other, int):
            return GFp2((self.a + other) % self.p, self.b, self.p)
        return GFp2((self.a + other.a) % self.p, (self.b + other.b) % self.p, self.p)

    def __radd__(self, other):
        if isinstance(other, int):
            return self.__add__(other)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, int):
            return GFp2((self.a - other) % self.p, self.b, self.p)
        return GFp2((self.a - other.a) % self.p, (self.b - other.b) % self.p, self.p)

    def __neg__(self):
        return GFp2((-self.a) % self.p, (-self.b) % self.p, self.p)

    def __mul__(self, other):
        p = self.p
        if isinstance(other, int):
            return GFp2((self.a * other) % p, (self.b * other) % p, p)
        # (a + bφ)(c + dφ) = ac + (ad+bc)φ + bd·φ²
        # φ² = φ + 1, so = ac + bd + (ad + bc + bd)φ
        a, b = self.a, self.b
        c, d = other.a, other.b
        return GFp2((a*c + b*d) % p, (a*d + b*c + b*d) % p, p)

    def __rmul__(self, other):
        if isinstance(other, int):
            return self.__mul__(other)
        return NotImplemented

    def __pow__(self, n):
        if n == 0:
            return GFp2(1, 0, self.p)
        if n < 0:
            return self.inv().__pow__(-n)
        result = GFp2(1, 0, self.p)
        base = GFp2(self.a, self.b, self.p)
        while n > 0:
            if n & 1:
                result = result * base
            base = base * base
            n >>= 1
        return result

    def is_zero(self):
        return self.a == 0 and self.b == 0

    def inv(self):
        """Inverse: 1/(a+bφ) = (a+b-bφ) / (a²+ab-b²)"""
        p = self.p
        a, b = self.a, self.b
        # norm = a² + ab - b² (norm form for x²-x-1)
        norm = (a*a + a*b - b*b) % p
        if norm == 0:
            raise ZeroDivisionError(f"({a}+{b}φ) has no inverse mod {p}")
        norm_inv = pow(norm, p - 2, p)
        # conjugate of a+bφ is (a+b) - bφ
        return GFp2(((a + b) * norm_inv) % p, ((-b) * norm_inv) % p, p)

    def mult_order(self):
        """Multiplicative order in GF(p²)*."""
        if self.is_zero():
            return None
        val = GFp2(self.a, self.b, self.p)
        one = GFp2(1, 0, self.p)
        for k in range(1, self.p * self.p):
            if val == one:
                return k
            val = val * self
        return self.p * self.p - 1


# =============================================================================
# CLASSIFY PRIMES
# =============================================================================

def classify_prime(p):
    """
    Classify x²-x-1 mod p.
    Discriminant = 5. Legendre symbol (5/p):
      +1 → SPLIT (p ≡ ±1 mod 5)
      -1 → INERT (p ≡ ±2 mod 5)
       0 → RAMIFIED (p = 5)
    """
    if p == 2:
        # x²-x-1 ≡ x²+x+1 mod 2: discriminant 1-4 = -3 ≡ 1 mod 2
        # But x²+x+1 has no roots in GF(2) (check: 0→1, 1→1+1+1=1)
        # Need GF(4). p=2 is INERT (since 5 ≡ 1 mod 2... but 2|disc?)
        # Actually: disc = 5. For p=2: 5 mod 2 = 1, (1/2)... Legendre undefined for p=2.
        # Direct check: x²-x-1 mod 2 = x²+x+1. No roots in GF(2). INERT.
        return "INERT"
    if p == 5:
        return "RAMIFIED"
    if p % 5 in (1, 4):
        return "SPLIT"
    else:
        return "INERT"

def find_roots_mod_p(p):
    """Find roots of x²-x-1 ≡ 0 mod p. Returns list of roots."""
    roots = []
    for x in range(p):
        if (x * x - x - 1) % p == 0:
            roots.append(x)
    return roots


# =============================================================================
# MODULAR FORM SHADOWS mod p
# =============================================================================

def eta_product_mod_p(q, p, N=None):
    """
    Compute ∏_{n=1}^{N} (1 - q^n) mod p.

    If N is None, we use N = ord(q) - 1 (the largest n before the product
    hits a zero factor). If ord(q) ≤ N_max, a factor (1-q^{ord(q)}) = 0
    kills the entire product.

    Returns (product, killed_at) where killed_at is the n where 1-q^n=0, or None.
    """
    if N is None:
        N = p  # default upper bound

    prod = 1
    qn = q  # q^1
    for n in range(1, N + 1):
        factor = (1 - qn) % p
        if factor == 0:
            return (0, n)
        prod = (prod * factor) % p
        qn = (qn * q) % p
    return (prod, None)

def eta24_mod_p(q, p, N=None):
    """
    Compute Δ(q) = q · ∏(1-qⁿ)²⁴ mod p.
    This is η²⁴ (avoids needing 24th roots).
    """
    prod, killed = eta_product_mod_p(q, p, N)
    if killed is not None:
        return (0, killed)
    delta = (q * pow(prod, 24, p)) % p
    return (delta, None)

def theta3_mod_p(q, p, N=None):
    """
    θ₃(q) = 1 + 2·∑_{n=1}^{N} q^{n²} mod p.
    """
    if N is None:
        N = int(math.sqrt(p)) + 5  # n² grows fast, stabilizes mod p

    result = 1
    for n in range(1, N + 1):
        qn2 = pow(q, n * n, p)
        result = (result + 2 * qn2) % p
    return result

def theta4_mod_p(q, p, N=None):
    """
    θ₄(q) = 1 + 2·∑_{n=1}^{N} (-1)ⁿ·q^{n²} mod p.
    """
    if N is None:
        N = int(math.sqrt(p)) + 5

    result = 1
    for n in range(1, N + 1):
        qn2 = pow(q, n * n, p)
        sign = 1 if n % 2 == 0 else p - 1  # (-1)^n mod p
        result = (result + 2 * sign * qn2) % p
    return result

def theta2_mod_p(q, p, N=None):
    """
    θ₂(q) = 2·∑_{n=0}^{N} q^{(n+1/2)²} mod p.
    Issue: (n+1/2)² = n²+n+1/4. Need 4th root of q or work with q^{4(n+1/2)²}.
    Instead: θ₂(q) = 2·q^{1/4}·∑ q^{n²+n}. We compute the sum part.
    """
    if N is None:
        N = int(math.sqrt(p)) + 5
    result = 0
    for n in range(0, N + 1):
        exp = n * n + n  # n² + n
        qe = pow(q, exp, p)
        result = (result + qe) % p
    return (2 * result) % p  # without the q^{1/4} prefactor


# =============================================================================
# GF(p²) MODULAR FORM SHADOWS (for inert primes)
# =============================================================================

def eta_product_gfp2(phi, p, N=None):
    """
    Compute ∏_{n=1}^{N} (1 - q^n) in GF(p²), where q = 1/φ = φ-1 (conjugate root).
    Returns (product_gfp2, killed_at_n).
    """
    if N is None:
        N = p * p  # upper bound for order in GF(p²)*

    # q = 1/φ in GF(p²): since φ²=φ+1, 1/φ = φ-1 = (p-1, 1) in our basis
    q = GFp2((phi.a + p - 1) % p, phi.b, p)  # φ - 1
    # Actually 1/φ = φ - 1 since φ(φ-1) = φ²-φ = 1. Yes.

    one = GFp2(1, 0, p)
    prod = GFp2(1, 0, p)
    qn = GFp2(q.a, q.b, p)

    for n in range(1, min(N + 1, p * p)):
        factor = one - qn
        if factor.is_zero():
            return (GFp2(0, 0, p), n)
        prod = prod * factor
        qn = qn * q
    return (prod, None)

def theta3_gfp2(phi, p, N=None):
    """θ₃(q) = 1 + 2·∑ q^{n²} in GF(p²)."""
    if N is None:
        N = int(math.sqrt(p * p)) + 5

    q = GFp2((phi.a + p - 1) % p, phi.b, p)
    one = GFp2(1, 0, p)
    result = GFp2(1, 0, p)

    for n in range(1, N + 1):
        qn2 = q ** (n * n)
        result = result + qn2 + qn2  # + 2·q^{n²}
    return result

def theta4_gfp2(phi, p, N=None):
    """θ₄(q) = 1 + 2·∑ (-1)ⁿ·q^{n²} in GF(p²)."""
    if N is None:
        N = int(math.sqrt(p * p)) + 5

    q = GFp2((phi.a + p - 1) % p, phi.b, p)
    result = GFp2(1, 0, p)

    for n in range(1, N + 1):
        qn2 = q ** (n * n)
        if n % 2 == 0:
            result = result + qn2 + qn2
        else:
            result = result - qn2 - qn2
    return result


# =============================================================================
# SPORADIC GROUP DATA
# =============================================================================

# Monster primes (primes dividing |M|)
MONSTER_PRIMES = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 41, 47, 59, 71}

# Pariah group defining characteristics / associated primes
# J₁: char 11 (|J₁| = 175560 = 2³·3·5·7·11·19)
# J₃: char 2 (|J₃| = 50232960 = 2⁷·3⁵·5·17·19)
# J₄: char 2 (|J₄| = 86775571046077562880 = 2²¹·3³·5·7·11³·23·29·31·37·43)
# Ly: char 5 (|Ly| = 51765179004000000 = 2⁸·3⁷·5⁶·7·11·31·37·67)
# Ru: char 2 (GF(2)) but also p=29 important
# O'N: char 7? (|O'N| = 460815505920 = 2⁹·3⁴·5·7³·11·19·31)

PARIAH_GROUPS = {
    "J1": {"order_primes": {2, 3, 5, 7, 11, 19}, "char": 11},
    "J3": {"order_primes": {2, 3, 5, 17, 19}, "char": 2},
    "J4": {"order_primes": {2, 3, 5, 7, 11, 23, 29, 31, 37, 43}, "char": 2},
    "Ly": {"order_primes": {2, 3, 5, 7, 11, 31, 37, 67}, "char": 5},
    "Ru": {"order_primes": {2, 3, 5, 7, 13, 29}, "char": 2},
    "ON": {"order_primes": {2, 3, 5, 7, 11, 19, 31}, "char": 7},
}

# All primes dividing any pariah group order
PARIAH_PRIMES = set()
for g in PARIAH_GROUPS.values():
    PARIAH_PRIMES |= g["order_primes"]

# Primes where a pariah group has its defining characteristic
PARIAH_CHAR_PRIMES = {g["char"] for g in PARIAH_GROUPS.values()}


# =============================================================================
# CONVERGENCE CONTROL
# =============================================================================

def convergence_bound_eta(q, p):
    """
    For the eta product ∏(1-qⁿ), once qⁿ starts cycling (period = ord(q)),
    the product over one full period is a fixed quantity. The "interesting"
    computation is up to ord(q).

    Returns recommended N for the product truncation.
    """
    if q % p == 0:
        return 1  # q=0, trivial
    o = mult_order(q, p)
    if o is None:
        return 1
    return o  # compute one full cycle

def convergence_bound_theta(q, p):
    """
    For θ₃ = 1 + 2∑q^{n²}, the exponents n² mod (p-1) cycle with period
    dividing p-1 (by Fermat). So q^{n²} cycles. But n² mod ord(q) is the key.

    We need enough terms that n² mod ord(q) has covered all residues.
    Safe bound: ord(q) * sqrt(ord(q)).
    """
    if q % p == 0:
        return 1
    o = mult_order(q, p)
    if o is None:
        return 1
    # n² mod o takes at most o distinct values
    # to see them all, we need n up to about o
    return min(o + 5, p + 10)


# =============================================================================
# DETERMINE STABILIZED THETA VALUES
# =============================================================================

def stabilized_theta3(q, p):
    """Compute θ₃(q) mod p, checking for stabilization."""
    if q % p == 0:
        return 1  # all terms vanish

    o = mult_order(q, p)
    # q^{n²} depends on n² mod o
    # collect all distinct n² mod o values
    seen_residues = set()
    result = 1  # constant term

    # We need to find all distinct values of q^{n²} mod p
    # This means all distinct n² mod o
    # Keep going until we've seen no new residues for o consecutive n
    stale_count = 0
    for n in range(1, max(3 * o, 50)):
        r = (n * n) % o
        qn2 = pow(q, n * n, p)
        old_result = result
        result = (result + 2 * qn2) % p
        if r not in seen_residues:
            seen_residues.add(r)
            stale_count = 0
        else:
            stale_count += 1
        # Once we've gone o steps without a new residue, the partial sums
        # may still change because we're adding 2*q^{n²} each time.
        # The SUM stabilizes only if q^{n²} eventually cycles with period T
        # and the sum over one period is 0 mod p.

    # Better approach: detect period of partial sums directly
    # Compute enough terms and look for periodicity
    partial_sums = [1]
    for n in range(1, max(4 * o + 20, 100)):
        qn2 = pow(q, n * n, p)
        prev = partial_sums[-1]
        partial_sums.append((prev + 2 * qn2) % p)

    # Check: does it stabilize?
    # Look at the last quarter and see if it's constant
    L = len(partial_sums)
    quarter = L // 4
    tail = partial_sums[3*quarter:]
    if len(set(tail)) == 1:
        return tail[0]

    # If not constant, look for period in differences
    # The differences d_n = 2*q^{n²} mod p have period dividing lcm(o, something)
    # Sum over one period of d_n might not be 0, so theta diverges mod p.
    # In that case, return the "characteristic" — the sum mod p over one full period.

    # Actually for finite sums: theta_3 is formally an infinite series.
    # In char p, the series is p-periodic in the COEFFICIENTS but the exponents n²
    # grow. The series converges p-adically. For our purposes: if q^o = 1,
    # then q^{n²} depends only on n² mod o. The sum ∑_{n=1}^∞ q^{n²}
    # = ∑_{r=0}^{o-1} q^r · #{n : n²≡r mod o, n≥1}
    # = ∑_{r=0}^{o-1} q^r · (∞ or 0) ... this diverges unless we work p-adically.

    # RESOLUTION: In GF(p), infinite sums don't converge in the usual sense.
    # We work with TRUNCATED modular forms: sum up to N = ord(q)-1 terms.
    # This captures the "one-cycle" information.

    result = 1
    for n in range(1, o):
        qn2 = pow(q, n * n, p)
        result = (result + 2 * qn2) % p
    return result

def stabilized_theta4(q, p):
    """Compute θ₄(q) mod p with same approach."""
    if q % p == 0:
        return 1

    o = mult_order(q, p)
    result = 1
    for n in range(1, o):
        qn2 = pow(q, n * n, p)
        sign = 1 if n % 2 == 0 else p - 1
        result = (result + 2 * sign * qn2) % p
    return result


# =============================================================================
# SECTION 1: MASTER TABLE FOR SPLIT PRIMES
# =============================================================================

def compute_split_fiber(p):
    """Compute all physics data for a split prime."""
    roots = find_roots_mod_p(p)
    if not roots:
        return None

    # Convention: q = 1/φ = smaller root? Both satisfy q+q²=1.
    # φ = the root with φ² = φ+1. If r is a root of x²-x-1, then r² = r+1.
    # So both roots r satisfy r²=r+1, meaning both ARE φ mod p.
    # The conjugate is 1-φ = -1/φ. So the two roots are φ and -1/φ mod p.
    # Since q = 1/φ and the other root of x²-x-1 is -φ+1 = -(φ-1) = -1/φ...
    # Actually x²-x-1=0 has roots (1±√5)/2. If √5 exists mod p:
    #   φ = (1+√5)/2,  -1/φ = (1-√5)/2
    # So φ mod p = one root, and 1/φ = φ-1 mod p.

    r1, r2 = roots[0], roots[1] if len(roots) > 1 else roots[0]

    # Identify which is φ and which is -1/φ
    # φ + (-1/φ) = φ - (φ-1) = 1. So φ + (-1/φ) = 1 mod p.
    # φ · (-1/φ) = -1 mod p.
    # Both roots sum to 1 (Vieta) and multiply to -1.

    # q = 1/φ = φ - 1
    phi = r1  # call this φ
    q = (phi - 1) % p  # 1/φ = φ - 1
    phi2 = r2  # = -1/φ mod p

    # Verify
    assert (q + q * q) % p == 1 % p, f"q+q²≠1 for p={p}, q={q}"

    # Multiplicative order of q
    ord_q = mult_order(q, p)

    # Eta product: ∏_{n=1}^{ord_q - 1} (1 - q^n) mod p
    # (truncated before the killing factor)
    eta_prod, killed_at = eta_product_mod_p(q, p, N=ord_q)

    # The FULL infinite product always dies at n = ord_q (since 1-q^{ord_q} = 0).
    # So η = 0 for ALL split primes in the strict infinite-product sense.
    # The interesting question is the TRUNCATED product up to n = ord_q - 1.
    eta_trunc, _ = eta_product_mod_p(q, p, N=ord_q - 1 if ord_q and ord_q > 1 else 1)

    # Theta functions (truncated at ord_q - 1 terms)
    t3 = stabilized_theta3(q, p)
    t4 = stabilized_theta4(q, p)

    # "1/α" — in the framework: 1/α ≈ θ₃·φ/θ₄
    # mod p: (θ₃ · φ · inv(θ₄)) mod p
    if t4 != 0:
        alpha_inv = (t3 * phi * mod_inv(t4, p)) % p
    else:
        alpha_inv = None  # undefined

    # Force survival
    strong = eta_trunc != 0
    weak = t3 != t4
    em = alpha_inv is not None and alpha_inv != 0

    return {
        'p': p,
        'type': 'SPLIT',
        'phi': phi,
        'phi2': phi2,
        'q': q,
        'ord_q': ord_q,
        'eta_trunc': eta_trunc,
        'eta_killed_at': ord_q,  # always dies at ord_q
        'theta3': t3,
        'theta4': t4,
        'alpha_inv': alpha_inv,
        'strong': strong,
        'weak': weak,
        'em': em,
    }


def compute_inert_fiber(p):
    """Compute physics for an inert prime (requires GF(p²))."""
    # φ = (0, 1) in GF(p²) basis {1, φ}
    # Actually φ is the element φ itself in GF(p)[φ]/(φ²-φ-1)
    phi = GFp2(0, 1, p)

    # Verify: φ² = φ + 1
    phi2 = phi * phi
    expected = GFp2(1, 1, p)  # 1 + φ
    assert phi2 == expected, f"φ²≠φ+1 for p={p}: got {phi2}"

    # q = 1/φ = φ - 1
    one = GFp2(1, 0, p)
    q = phi - 1

    # Verify q + q² = 1
    q2 = q * q
    s = q + q2
    assert s == one, f"q+q²≠1 for p={p}: got {s}"

    # Order of q in GF(p²)*
    ord_q = q.mult_order()

    # Eta product in GF(p²) — truncated at ord_q - 1
    zero = GFp2(0, 0, p)
    prod = GFp2(1, 0, p)
    qn = GFp2(q.a, q.b, p)
    killed_at = None

    N = min(ord_q if ord_q else p*p, p*p)
    for n in range(1, N):
        factor = one - qn
        if factor.is_zero():
            killed_at = n
            break
        prod = prod * factor
        qn = qn * q

    eta_trunc = prod if killed_at is None else zero
    eta_killed = killed_at if killed_at else ord_q

    # Theta3 in GF(p²)
    t3 = GFp2(1, 0, p)
    for n in range(1, min(ord_q if ord_q else p+5, p+5)):
        qn2 = q ** (n * n)
        t3 = t3 + qn2 + qn2

    # Theta4 in GF(p²)
    t4 = GFp2(1, 0, p)
    for n in range(1, min(ord_q if ord_q else p+5, p+5)):
        qn2 = q ** (n * n)
        if n % 2 == 0:
            t4 = t4 + qn2 + qn2
        else:
            t4 = t4 - qn2 - qn2

    # 1/α = θ₃·φ/θ₄
    if not t4.is_zero():
        alpha_inv = t3 * phi * t4.inv()
    else:
        alpha_inv = None

    strong = not eta_trunc.is_zero() if isinstance(eta_trunc, GFp2) else eta_trunc != 0
    weak = t3 != t4
    em = alpha_inv is not None and (not alpha_inv.is_zero() if isinstance(alpha_inv, GFp2) else True)

    return {
        'p': p,
        'type': 'INERT',
        'phi': phi,
        'q': q,
        'ord_q': ord_q,
        'eta_trunc': eta_trunc,
        'eta_killed_at': eta_killed,
        'theta3': t3,
        'theta4': t4,
        'alpha_inv': alpha_inv,
        'strong': strong,
        'weak': weak,
        'em': em,
    }


def compute_ramified_fiber():
    """p=5: x²-x-1 ≡ x²-x-1 mod 5. disc=5≡0. Double root at x = (1±0)/2."""
    p = 5
    # x²-x-1 mod 5. x=3: 9-3-1=5≡0. Double root at x=3.
    # φ ≡ 3 mod 5. q = 1/φ = φ-1 = 2 mod 5.
    phi = 3
    q = 2
    assert (q + q*q) % p == 1

    ord_q = mult_order(q, p)
    eta_trunc, killed = eta_product_mod_p(q, p, N=ord_q - 1 if ord_q > 1 else 1)
    t3 = stabilized_theta3(q, p)
    t4 = stabilized_theta4(q, p)

    if t4 != 0:
        alpha_inv = (t3 * phi * mod_inv(t4, p)) % p
    else:
        alpha_inv = None

    strong = eta_trunc != 0
    weak = t3 != t4
    em = alpha_inv is not None and alpha_inv != 0

    # V(Φ) = (Φ²-Φ-1)² has Φ=3 as double root = both vacua merge. No kink!

    return {
        'p': p,
        'type': 'RAMIFIED',
        'phi': phi,
        'q': q,
        'ord_q': ord_q,
        'eta_trunc': eta_trunc,
        'eta_killed_at': ord_q,
        'theta3': t3,
        'theta4': t4,
        'alpha_inv': alpha_inv,
        'strong': strong,
        'weak': weak,
        'em': em,
        'note': 'DOUBLE ROOT: vacua merge, no kink possible. Level 0 (Ly).',
    }


# =============================================================================
# MAIN COMPUTATION
# =============================================================================

def main():
    print("=" * 100)
    print("ALL FIBERS OF Spec(Z[φ]): PHYSICS AT EVERY PRIME")
    print("q + q² = 1  reduced mod p for all primes p ≤ 100")
    print("=" * 100)

    all_primes = primes_up_to(100)
    results = []

    # =========================================================================
    # SECTION 1: SPLIT PRIMES (φ exists in GF(p))
    # =========================================================================
    print("\n" + "=" * 100)
    print("SECTION 1: SPLIT PRIMES (p ≡ ±1 mod 5, discriminant 5 is QR)")
    print("=" * 100)

    split_primes = [p for p in all_primes if classify_prime(p) == "SPLIT"]
    print(f"\nSplit primes ≤ 100: {split_primes}")
    print(f"Count: {len(split_primes)}")

    for p in split_primes:
        data = compute_split_fiber(p)
        results.append(data)

        forces = []
        if data['strong']: forces.append('S')
        if data['weak']: forces.append('W')
        if data['em']: forces.append('EM')
        force_str = '+'.join(forces) if forces else 'NONE'

        in_monster = 'M' if p in MONSTER_PRIMES else ' '
        in_pariah = 'P' if p in PARIAH_PRIMES else ' '

        print(f"\n  p={p:3d} [{in_monster}{in_pariah}] | φ≡{data['phi']:3d} | q≡{data['q']:3d} | "
              f"ord(q)={data['ord_q']:4d} | "
              f"η_trunc={data['eta_trunc']:4d} | "
              f"θ₃={data['theta3']:4d} | θ₄={data['theta4']:4d} | "
              f"1/α={str(data['alpha_inv']):>5s} | "
              f"forces={force_str}")

    # =========================================================================
    # SECTION 2: RAMIFIED PRIME (p=5)
    # =========================================================================
    print("\n" + "=" * 100)
    print("SECTION 2: RAMIFIED PRIME (p = 5)")
    print("=" * 100)

    data5 = compute_ramified_fiber()
    results.append(data5)

    forces = []
    if data5['strong']: forces.append('S')
    if data5['weak']: forces.append('W')
    if data5['em']: forces.append('EM')
    force_str = '+'.join(forces) if forces else 'NONE'

    print(f"\n  p=  5 [MP] | φ≡{data5['phi']:3d} | q≡{data5['q']:3d} | "
          f"ord(q)={data5['ord_q']:4d} | "
          f"η_trunc={data5['eta_trunc']:4d} | "
          f"θ₃={data5['theta3']:4d} | θ₄={data5['theta4']:4d} | "
          f"1/α={str(data5['alpha_inv']):>5s} | "
          f"forces={force_str}")
    print(f"  NOTE: {data5['note']}")

    # =========================================================================
    # SECTION 3: INERT PRIMES (φ exists only in GF(p²))
    # =========================================================================
    print("\n" + "=" * 100)
    print("SECTION 3: INERT PRIMES (p ≡ ±2 mod 5, φ requires GF(p²))")
    print("=" * 100)

    inert_primes = [p for p in all_primes if classify_prime(p) == "INERT"]
    print(f"\nInert primes ≤ 100: {inert_primes}")
    print(f"Count: {len(inert_primes)}")

    # Compute select inert primes (small ones — GF(p²) gets expensive)
    inert_computed = []
    inert_limit = 50  # GF(p²) order computation is O(p²), keep moderate

    for p in inert_primes:
        if p > inert_limit:
            print(f"\n  p={p:3d}: INERT (GF({p}²) computation skipped for speed, p > {inert_limit})")
            continue

        print(f"\n  Computing GF({p}²) physics for p={p}...")
        try:
            data = compute_inert_fiber(p)
            inert_computed.append(data)

            forces = []
            if data['strong']: forces.append('S')
            if data['weak']: forces.append('W')
            if data['em']: forces.append('EM')
            force_str = '+'.join(forces) if forces else 'NONE'

            in_monster = 'M' if p in MONSTER_PRIMES else ' '
            in_pariah = 'P' if p in PARIAH_PRIMES else ' '

            eta_str = str(data['eta_trunc']) if isinstance(data['eta_trunc'], GFp2) else str(data['eta_trunc'])
            t3_str = str(data['theta3'])
            t4_str = str(data['theta4'])
            ai_str = str(data['alpha_inv']) if data['alpha_inv'] else 'undef'

            print(f"  p={p:3d} [{in_monster}{in_pariah}] | φ={data['phi']} | q={data['q']} | "
                  f"ord(q)={data['ord_q']} | "
                  f"η_trunc={eta_str} | "
                  f"θ₃={t3_str} | θ₄={t4_str} | "
                  f"1/α={ai_str} | "
                  f"forces={force_str}")
        except Exception as e:
            print(f"  p={p}: ERROR: {e}")

    results.extend(inert_computed)

    # =========================================================================
    # SECTION 4: p=2 SPECIAL CASE (char 2, GF(4), J₃ triality)
    # =========================================================================
    print("\n" + "=" * 100)
    print("SECTION 4: SPECIAL CASE p = 2 (GF(4), J₃ triality universe)")
    print("=" * 100)

    print("""
  In GF(2): x²-x-1 = x²+x+1 (since -1=+1 in char 2). No roots in GF(2).
  In GF(4) = GF(2)[ω]/(ω²+ω+1): the golden polynomial IS the field-defining polynomial!
  So φ = ω (primitive cube root of unity).

  q = 1/φ = ω² (since ω·ω² = ω³ = 1, and ω²+ω = 1 = ω⁴+ω² in GF(4)).
  Verify: q + q² = ω² + ω⁴ = ω² + ω = 1. ✓

  Properties:
    - φ³ = 1, so ALL powers cycle with period 3
    - η: ∏(1-qⁿ). q=ω², q²=ω, q³=1, so (1-q³)=0 → η = 0
    - θ₃ = 1 + 2∑q^{n²}. But char 2 means 2=0, so θ₃ = 1.
    - θ₄ = 1 + 2∑(-q)^{n²} = 1 (same reason, 2=0).
    - θ₃ = θ₄ = 1 → weak force DEAD (no differentiation)
    - η = 0 → strong force DEAD
    - 1/α = θ₃·φ/θ₄ = 1·ω/1 = ω → EM EXISTS but α = ω² (cube root of unity!)

  INTERPRETATION: Triality universe. All three forces fuse into one Z₃-symmetric
  coupling. The strong/weak distinction dissolves. Only a single "rotation" remains.
  This is where J₃ (Janko's third group) lives — with its 9-dim rep over GF(4).
""")

    # =========================================================================
    # SECTION 5: ORDER ANALYSIS — WHY η DIES
    # =========================================================================
    print("\n" + "=" * 100)
    print("SECTION 5: MULTIPLICATIVE ORDER OF q AND η-KILLING")
    print("=" * 100)

    print("""
  η(q) = q^{1/24} · ∏_{n≥1} (1-qⁿ)

  In GF(p), q has finite multiplicative order m = ord(q).
  Then q^m = 1, so the factor (1-q^m) = 0, killing the infinite product.

  The TRUNCATED η (product up to n = m-1) can be nonzero.
  This truncated value is what we tabulate — it represents the
  "finite shadow" of the strong force at each prime.

  Importantly: η_trunc = 0 can happen even before n = ord(q)
  if some q^k = 1 for k < ord(q). This happens when q is a root
  of unity of order dividing some n < m.
""")

    print(f"\n  {'p':>4s} | {'type':>8s} | {'q mod p':>7s} | {'ord(q)':>7s} | {'η_trunc':>8s} | "
          f"{'η=0?':>5s} | {'kill at':>7s} | Monster | Pariah")
    print("  " + "-" * 90)

    for p in all_primes:
        cl = classify_prime(p)
        if cl == "SPLIT":
            roots = find_roots_mod_p(p)
            phi = roots[0]
            q = (phi - 1) % p
            o = mult_order(q, p)
            eta_t, killed = eta_product_mod_p(q, p, N=o - 1 if o and o > 1 else 1)
            in_m = 'Y' if p in MONSTER_PRIMES else 'N'
            in_p = 'Y' if p in PARIAH_PRIMES else 'N'
            print(f"  {p:4d} | {'SPLIT':>8s} | {q:7d} | {o:7d} | {eta_t:8d} | "
                  f"{'YES' if eta_t == 0 else 'no':>5s} | {o:7d} | "
                  f"{'  Y   ' if p in MONSTER_PRIMES else '  N   '} | "
                  f"{'  Y' if p in PARIAH_PRIMES else '  N'}")
        elif cl == "RAMIFIED":
            q = 2
            o = mult_order(q, p)
            eta_t, _ = eta_product_mod_p(q, p, N=o - 1 if o and o > 1 else 1)
            print(f"  {p:4d} | {'RAMIFIED':>8s} | {q:7d} | {o:7d} | {eta_t:8d} | "
                  f"{'YES' if eta_t == 0 else 'no':>5s} | {o:7d} | "
                  f"{'  Y   '} | {'  Y'}")
        else:
            # Inert — skip GF(p²) here, just note
            print(f"  {p:4d} | {'INERT':>8s} | {'GF(p²)':>7s} | {'GF(p²)':>7s} | "
                  f"{'GF(p²)':>8s} | {'?':>5s} | {'?':>7s} | "
                  f"{'  Y   ' if p in MONSTER_PRIMES else '  N   '} | "
                  f"{'  Y' if p in PARIAH_PRIMES else '  N'}")

    # =========================================================================
    # SECTION 6: PATTERN ANALYSIS
    # =========================================================================
    print("\n" + "=" * 100)
    print("SECTION 6: PATTERN ANALYSIS")
    print("=" * 100)

    # 6a: Monster vs non-Monster behavior
    print("\n--- 6a: Monster primes vs non-Monster primes (split only) ---")

    monster_split = [r for r in results if r['type'] == 'SPLIT' and r['p'] in MONSTER_PRIMES]
    non_monster_split = [r for r in results if r['type'] == 'SPLIT' and r['p'] not in MONSTER_PRIMES]

    if monster_split:
        avg_ord_m = sum(r['ord_q'] for r in monster_split) / len(monster_split)
        strong_count_m = sum(1 for r in monster_split if r['strong'])
        weak_count_m = sum(1 for r in monster_split if r['weak'])
        em_count_m = sum(1 for r in monster_split if r['em'])
        print(f"\n  Monster split primes ({len(monster_split)}):")
        print(f"    Average ord(q): {avg_ord_m:.1f}")
        print(f"    Strong surviving: {strong_count_m}/{len(monster_split)}")
        print(f"    Weak surviving:   {weak_count_m}/{len(monster_split)}")
        print(f"    EM surviving:     {em_count_m}/{len(monster_split)}")

    if non_monster_split:
        avg_ord_nm = sum(r['ord_q'] for r in non_monster_split) / len(non_monster_split)
        strong_count_nm = sum(1 for r in non_monster_split if r['strong'])
        weak_count_nm = sum(1 for r in non_monster_split if r['weak'])
        em_count_nm = sum(1 for r in non_monster_split if r['em'])
        print(f"\n  Non-Monster split primes ({len(non_monster_split)}):")
        print(f"    Average ord(q): {avg_ord_nm:.1f}")
        print(f"    Strong surviving: {strong_count_nm}/{len(non_monster_split)}")
        print(f"    Weak surviving:   {weak_count_nm}/{len(non_monster_split)}")
        print(f"    EM surviving:     {em_count_nm}/{len(non_monster_split)}")

    # 6b: Pariah primes
    print("\n--- 6b: Pariah-associated primes ---")
    pariah_only = PARIAH_PRIMES - MONSTER_PRIMES
    print(f"  Primes in pariah orders but NOT in Monster: {sorted(pariah_only)}")
    for p in sorted(pariah_only):
        if p > 100:
            continue
        cl = classify_prime(p)
        groups = [name for name, info in PARIAH_GROUPS.items() if p in info['order_primes']]
        print(f"    p={p}: {cl}, appears in {', '.join(groups)}")

    # 6c: Richness ordering
    print("\n--- 6c: Richness ordering (split primes, by force count) ---")

    split_results = [r for r in results if r['type'] == 'SPLIT']

    def richness(r):
        score = 0
        if r['strong']: score += 4
        if r['weak']: score += 2
        if r['em']: score += 1
        return score

    split_results.sort(key=lambda r: (-richness(r), r['p']))

    for r in split_results:
        forces = []
        if r['strong']: forces.append('Strong')
        if r['weak']: forces.append('Weak')
        if r['em']: forces.append('EM')
        in_m = '(Monster)' if r['p'] in MONSTER_PRIMES else ''
        in_p = '(Pariah)' if r['p'] in PARIAH_PRIMES else ''
        print(f"    p={r['p']:3d}: {'+'.join(forces) if forces else 'DEAD'} "
              f"  ord(q)={r['ord_q']}  1/α={r['alpha_inv']}  {in_m} {in_p}")

    # 6d: Primes where strong force survives (η_trunc ≠ 0)
    print("\n--- 6d: Which primes preserve the strong force? ---")
    strong_primes = [r['p'] for r in results if r['type'] == 'SPLIT' and r['strong']]
    weak_only = [r['p'] for r in results if r['type'] == 'SPLIT' and not r['strong']]
    print(f"  Strong survives (η_trunc ≠ 0): {strong_primes}")
    print(f"  Strong dies (η_trunc = 0):     {weak_only}")

    # 6e: θ₃ = θ₄ primes (weak force dead)
    print("\n--- 6e: Which primes kill the weak force? (θ₃ = θ₄) ---")
    weak_dead = [r['p'] for r in results if r['type'] == 'SPLIT' and not r['weak']]
    weak_alive = [r['p'] for r in results if r['type'] == 'SPLIT' and r['weak']]
    print(f"  Weak dead (θ₃=θ₄):   {weak_dead}")
    print(f"  Weak alive (θ₃≠θ₄):  {weak_alive}")

    # =========================================================================
    # SECTION 7: SPECIAL PRIME DEEP DIVES
    # =========================================================================
    print("\n" + "=" * 100)
    print("SECTION 7: SPECIAL PRIME DEEP DIVES")
    print("=" * 100)

    # p = 11 (J₁)
    print("\n--- p = 11: The J₁ prime (EM-only universe) ---")
    if 11 in [r['p'] for r in results]:
        r11 = [r for r in results if r['p'] == 11][0]
        print(f"  φ ≡ {r11['phi']} mod 11")
        print(f"  q ≡ {r11['q']} mod 11")
        print(f"  ord(q) = {r11['ord_q']}")
        print(f"  η_trunc = {r11['eta_trunc']}")
        print(f"  θ₃ = {r11['theta3']}, θ₄ = {r11['theta4']}")
        print(f"  1/α = {r11['alpha_inv']}")
        print(f"  Forces: S={'Y' if r11['strong'] else 'N'} W={'Y' if r11['weak'] else 'N'} EM={'Y' if r11['em'] else 'N'}")

        # Powers of q=3 mod 11
        q = r11['q']
        print(f"\n  Powers of q={q} mod 11:")
        val = 1
        for k in range(11):
            val = (val * q) % 11 if k > 0 else q
            if k == 0: val = q
            print(f"    q^{k+1} = {val}")
            if val == 1:
                print(f"    → Order = {k+1}")
                break

    # p = 29 (split, in Monster, in J₄ and Ru)
    print("\n--- p = 29: Monster + Pariah (J₄, Ru) prime ---")
    if 29 in [r['p'] for r in results]:
        r29 = [r for r in results if r['p'] == 29][0]
        print(f"  φ ≡ {r29['phi']} mod 29")
        print(f"  q ≡ {r29['q']} mod 29")
        print(f"  ord(q) = {r29['ord_q']}")
        print(f"  η_trunc = {r29['eta_trunc']}")
        print(f"  θ₃ = {r29['theta3']}, θ₄ = {r29['theta4']}")
        print(f"  1/α = {r29['alpha_inv']}")
        print(f"  Forces: S={'Y' if r29['strong'] else 'N'} W={'Y' if r29['weak'] else 'N'} EM={'Y' if r29['em'] else 'N'}")

    # p = 59 (largest Monster prime that's split and not pariah)
    print("\n--- p = 59: Large Monster prime ---")
    if 59 in [r['p'] for r in results]:
        r59 = [r for r in results if r['p'] == 59][0]
        print(f"  φ ≡ {r59['phi']} mod 59")
        print(f"  q ≡ {r59['q']} mod 59")
        print(f"  ord(q) = {r59['ord_q']}")
        print(f"  η_trunc = {r59['eta_trunc']}")
        print(f"  θ₃ = {r59['theta3']}, θ₄ = {r59['theta4']}")
        print(f"  Forces: S={'Y' if r59['strong'] else 'N'} W={'Y' if r59['weak'] else 'N'} EM={'Y' if r59['em'] else 'N'}")

    # =========================================================================
    # SECTION 8: ROOT-OF-UNITY ANALYSIS
    # =========================================================================
    print("\n" + "=" * 100)
    print("SECTION 8: ROOT-OF-UNITY STRUCTURE OF q")
    print("=" * 100)

    print("""
  In GF(p), every nonzero element is a root of unity (q^{p-1} = 1).
  The multiplicative order of q = 1/φ divides p-1.

  Key: if ord(q) = m, then q^m = 1, so (1-q^m) = 0 in the eta product.
  The truncated eta (to n < m) can still be nonzero.

  But there's a deeper structure: q satisfies q² + q = 1, so
  q is a root of x² + x - 1 = 0 in GF(p). The Frobenius acts on {q, q^p}.
  Since q^p is the other root (the Galois conjugate), q^p = -1/q = 1-q = q².
  Wait: actually q^p ≡ q or q^p ≡ q' where q' is the conjugate root.
  For SPLIT primes, q ∈ GF(p), so q^p = q (Frobenius fixes q).
""")

    print(f"\n  {'p':>4s} | {'ord(q)':>7s} | {'p-1':>5s} | {'(p-1)/ord':>9s} | {'ord|24?':>8s} | "
          f"{'q root of unity pattern':>30s}")
    print("  " + "-" * 80)

    for r in results:
        if r['type'] != 'SPLIT':
            continue
        p = r['p']
        o = r['ord_q']
        if o is None or o == 0:
            continue
        ratio = (p - 1) // o if o > 0 else 0
        divides_24 = "YES" if 24 % o == 0 else "no"

        # Pattern: what is q as a power of a primitive root?
        # Find a primitive root mod p
        for g in range(2, p):
            if mult_order(g, p) == p - 1:
                prim_root = g
                break
        else:
            prim_root = None

        if prim_root:
            # q = g^k for some k
            val = 1
            for k in range(p - 1):
                val = (val * prim_root) % p
                if val == r['q']:
                    pattern = f"g^{k+1} (g={prim_root}, index {k+1}/{p-1})"
                    break
            else:
                pattern = "?"
        else:
            pattern = "no prim root found"

        print(f"  {p:4d} | {o:7d} | {p-1:5d} | {ratio:9d} | {divides_24:>8s} | {pattern}")

    # =========================================================================
    # SECTION 9: V(Φ) POTENTIAL ANALYSIS AT EACH PRIME
    # =========================================================================
    print("\n" + "=" * 100)
    print("SECTION 9: THE POTENTIAL V(Φ) = (Φ² - Φ - 1)² MOD p")
    print("=" * 100)

    print("""
  V(Φ) = (Φ² - Φ - 1)² has vacua where Φ² - Φ - 1 = 0, i.e., Φ = φ, -1/φ.
  The kink interpolates between these two vacua.

  For SPLIT primes: two distinct vacua mod p → kink exists
  For RAMIFIED (p=5): vacua merge → no kink (Level 0)
  For INERT: vacua exist only in GF(p²) → "hidden" kink

  We can also check: does V(Φ) have any OTHER zeros mod p?
  V(Φ) = 0 mod p iff Φ² - Φ - 1 ≡ 0 mod p.
  These are exactly the roots we already found.
""")

    for p in all_primes:
        cl = classify_prime(p)
        roots = find_roots_mod_p(p)

        if cl == "SPLIT":
            r1, r2 = roots
            sep = (r1 - r2) % p
            # "Distance" between vacua
            # In char 0: φ - (-1/φ) = φ + 1/φ = √5
            # mod p: r1 - r2 ≡ ±√5 mod p
            sqrt5_candidates = mod_sqrt(5, p)
            print(f"  p={p:3d} SPLIT:  vacua at {r1}, {r2}.  "
                  f"Separation = {sep} mod {p}.  "
                  f"√5 mod {p} = {sqrt5_candidates}.  "
                  f"Match: {'✓' if sep in sqrt5_candidates or (p-sep) in sqrt5_candidates else '✗'}")
        elif cl == "RAMIFIED":
            print(f"  p={p:3d} RAMIFIED: single vacuum at {roots[0]} (double root). NO KINK.")
        else:
            print(f"  p={p:3d} INERT:   no vacua in GF({p}). Kink lives in GF({p}²).")

    # =========================================================================
    # SECTION 10: PISANO PERIODS AND FIBONACCI CONNECTION
    # =========================================================================
    print("\n" + "=" * 100)
    print("SECTION 10: PISANO PERIODS — FIBONACCI MOD p")
    print("=" * 100)

    print("""
  The Fibonacci sequence F_n satisfies the same recurrence as powers of φ.
  The Pisano period π(p) = period of F_n mod p.

  Connection to ord(q):
    - For split primes: ord(q) divides π(p)
    - π(p) divides p-1 if p ≡ ±1 mod 5 (split), divides 2(p+1) if inert

  The Fibonacci sequence IS the discrete cascade of q+q²=1.
""")

    print(f"\n  {'p':>4s} | {'type':>8s} | {'π(p)':>6s} | {'ord(q)':>7s} | {'π(p)/ord':>8s} | "
          f"{'p-1':>5s} | {'π(p)|(p-1)?':>11s}")
    print("  " + "-" * 70)

    for p in all_primes:
        cl = classify_prime(p)
        pi_p = pisano_period(p)

        if cl == "SPLIT":
            roots = find_roots_mod_p(p)
            q = (roots[0] - 1) % p
            o = mult_order(q, p)
            ratio = pi_p // o if o and o > 0 else 0
            divides = "YES" if (p - 1) % pi_p == 0 else "no"
            print(f"  {p:4d} | {'SPLIT':>8s} | {pi_p:6d} | {o:7d} | {ratio:8d} | "
                  f"{p-1:5d} | {divides:>11s}")
        elif cl == "RAMIFIED":
            print(f"  {p:4d} | {'RAMIFIED':>8s} | {pi_p:6d} | {'4':>7s} | {pi_p//4:8d} | "
                  f"{p-1:5d} | {'YES' if (p-1) % pi_p == 0 else 'no':>11s}")
        else:
            print(f"  {p:4d} | {'INERT':>8s} | {pi_p:6d} | {'GF(p²)':>7s} | {'?':>8s} | "
                  f"{p-1:5d} | {'—':>11s}")

    # =========================================================================
    # SECTION 11: CONSOLIDATED MASTER TABLE
    # =========================================================================
    print("\n" + "=" * 100)
    print("SECTION 11: MASTER TABLE — ALL PRIMES p ≤ 100")
    print("=" * 100)

    header = (f"  {'p':>3s} | {'Type':>8s} | {'φ mod p':>8s} | {'q':>5s} | {'ord(q)':>7s} | "
              f"{'η_tr':>5s} | {'θ₃':>5s} | {'θ₄':>5s} | {'1/α':>5s} | "
              f"{'S':>1s}{'W':>2s}{'E':>2s} | {'M':>1s}{'P':>2s} | Notes")
    print(header)
    print("  " + "-" * 100)

    for p in all_primes:
        cl = classify_prime(p)
        in_m = 'Y' if p in MONSTER_PRIMES else ' '
        in_p = 'Y' if p in PARIAH_PRIMES else ' '

        if cl == "SPLIT":
            r = [x for x in results if x['p'] == p and x['type'] == 'SPLIT']
            if r:
                r = r[0]
                s_flag = '✓' if r['strong'] else '·'
                w_flag = '✓' if r['weak'] else '·'
                e_flag = '✓' if r['em'] else '·'

                notes = []
                if p in MONSTER_PRIMES and p in PARIAH_PRIMES:
                    groups = [name for name, info in PARIAH_GROUPS.items() if p in info['order_primes']]
                    notes.append(f"M+{','.join(groups)}")
                elif p in MONSTER_PRIMES:
                    notes.append("Monster")

                if r['ord_q'] and r['ord_q'] <= 5:
                    notes.append(f"LOW ORDER")

                print(f"  {p:3d} | {'SPLIT':>8s} | {r['phi']:8d} | {r['q']:5d} | {r['ord_q']:7d} | "
                      f"{r['eta_trunc']:5d} | {r['theta3']:5d} | {r['theta4']:5d} | "
                      f"{str(r['alpha_inv']):>5s} | "
                      f"{s_flag} {w_flag} {e_flag} | {in_m} {in_p} | {'; '.join(notes)}")
            else:
                print(f"  {p:3d} | {'SPLIT':>8s} | {'?':>8s}")

        elif cl == "RAMIFIED":
            r = data5
            s_flag = '✓' if r['strong'] else '·'
            w_flag = '✓' if r['weak'] else '·'
            e_flag = '✓' if r['em'] else '·'
            print(f"  {p:3d} | {'RAMIFIED':>8s} | {r['phi']:8d} | {r['q']:5d} | {r['ord_q']:7d} | "
                  f"{r['eta_trunc']:5d} | {r['theta3']:5d} | {r['theta4']:5d} | "
                  f"{str(r['alpha_inv']):>5s} | "
                  f"{s_flag} {w_flag} {e_flag} | {in_m} {in_p} | NO KINK (Ly)")

        else:  # INERT
            inert_data = [x for x in results if x.get('p') == p and x.get('type') == 'INERT']
            if inert_data:
                r = inert_data[0]
                s_flag = '✓' if r['strong'] else '·'
                w_flag = '✓' if r['weak'] else '·'
                e_flag = '✓' if r['em'] else '·'
                ai_str = str(r['alpha_inv']) if r['alpha_inv'] else '?'
                print(f"  {p:3d} | {'INERT':>8s} | {'GF('+str(p)+'²)':>8s} | {'':>5s} | "
                      f"{str(r['ord_q']):>7s} | "
                      f"{'GFp2':>5s} | {'GFp2':>5s} | {'GFp2':>5s} | "
                      f"{ai_str:>5s} | "
                      f"{s_flag} {w_flag} {e_flag} | {in_m} {in_p} | φ∈GF({p}²)")
            else:
                print(f"  {p:3d} | {'INERT':>8s} | {'GF('+str(p)+'²)':>8s} | {'':>5s} | "
                      f"{'?':>7s} | {'?':>5s} | {'?':>5s} | {'?':>5s} | {'?':>5s} | "
                      f"{'?':>1s} {'?':>1s} {'?':>1s} | {in_m} {in_p} | needs GF({p}²)")

    # =========================================================================
    # SECTION 12: SYNTHESIS — WHAT THE LANDSCAPE TELLS US
    # =========================================================================
    print("\n" + "=" * 100)
    print("SECTION 12: SYNTHESIS")
    print("=" * 100)

    total_split = len([r for r in results if r['type'] == 'SPLIT'])
    strong_alive_count = len([r for r in results if r['type'] == 'SPLIT' and r['strong']])
    weak_alive_count = len([r for r in results if r['type'] == 'SPLIT' and r['weak']])
    em_alive_count = len([r for r in results if r['type'] == 'SPLIT' and r['em']])
    all_three = len([r for r in results if r['type'] == 'SPLIT'
                     and r['strong'] and r['weak'] and r['em']])

    print(f"""
  STATISTICS (split primes only, {total_split} total):
    Strong force survives:  {strong_alive_count}/{total_split}
    Weak force survives:    {weak_alive_count}/{total_split}
    EM survives:            {em_alive_count}/{total_split}
    All three forces:       {all_three}/{total_split}

  CLASSIFICATION OF UNIVERSES:
    char 0 (Q):     Full physics — Monster, all forces, consciousness
    p = 5:          Level 0 — vacua merge, no kink, no physics (Ly)
    p = 2 (GF(4)):  Triality — all forces fuse to Z₃ rotation (J₃)
    p = 11:         EM-only — strong and weak dead (J₁)

  HIERARCHY OF RICHNESS:
    The richest non-char-0 fiber is the one with the most surviving forces
    AND the highest multiplicative order for q (more "room" for structure).
""")

    # Find richest prime
    if split_results:
        richest = max(split_results, key=lambda r: (richness(r), r['ord_q']))
        forces = []
        if richest['strong']: forces.append('Strong')
        if richest['weak']: forces.append('Weak')
        if richest['em']: forces.append('EM')
        print(f"  RICHEST SPLIT PRIME: p = {richest['p']}")
        print(f"    Forces: {'+'.join(forces)}")
        print(f"    ord(q) = {richest['ord_q']}")
        print(f"    1/α = {richest['alpha_inv']}")
        print(f"    Monster: {'YES' if richest['p'] in MONSTER_PRIMES else 'NO'}")
        print(f"    Pariah:  {'YES' if richest['p'] in PARIAH_PRIMES else 'NO'}")

    # Correlation: Monster primes richer?
    print("\n  MONSTER vs NON-MONSTER CORRELATION:")
    m_rich = [richness(r) for r in results if r['type'] == 'SPLIT' and r['p'] in MONSTER_PRIMES]
    nm_rich = [richness(r) for r in results if r['type'] == 'SPLIT' and r['p'] not in MONSTER_PRIMES]
    if m_rich and nm_rich:
        avg_m = sum(m_rich) / len(m_rich)
        avg_nm = sum(nm_rich) / len(nm_rich)
        print(f"    Monster split primes avg richness:     {avg_m:.2f}")
        print(f"    Non-Monster split primes avg richness: {avg_nm:.2f}")
        if avg_m > avg_nm:
            print(f"    → Monster primes ARE richer on average")
        elif avg_m < avg_nm:
            print(f"    → Monster primes are NOT richer (surprising!)")
        else:
            print(f"    → No difference")

    # Split/inert correlation with Monster
    print("\n  SPLIT/INERT vs MONSTER:")
    m_primes_list = sorted(MONSTER_PRIMES)
    for p in m_primes_list:
        if p <= 100:
            print(f"    p={p:3d}: {classify_prime(p)}")
    m_split = len([p for p in MONSTER_PRIMES if p <= 100 and classify_prime(p) == "SPLIT"])
    m_inert = len([p for p in MONSTER_PRIMES if p <= 100 and classify_prime(p) == "INERT"])
    m_ram = len([p for p in MONSTER_PRIMES if p <= 100 and classify_prime(p) == "RAMIFIED"])
    print(f"    Monster primes: {m_split} split, {m_inert} inert, {m_ram} ramified")

    all_split_count = len([p for p in all_primes if classify_prime(p) == "SPLIT"])
    all_inert_count = len([p for p in all_primes if classify_prime(p) == "INERT"])
    print(f"    All primes ≤100: {all_split_count} split, {all_inert_count} inert, 1 ramified")
    if all_split_count + all_inert_count > 0:
        expected_split_ratio = all_split_count / (all_split_count + all_inert_count)
        actual_split_ratio = m_split / (m_split + m_inert) if (m_split + m_inert) > 0 else 0
        print(f"    Expected split ratio: {expected_split_ratio:.2f}")
        print(f"    Monster split ratio:  {actual_split_ratio:.2f}")

    # =========================================================================
    # SECTION 13: KEY FINDINGS AND INTERPRETIVE NOTES
    # =========================================================================
    print("\n" + "=" * 100)
    print("SECTION 13: KEY FINDINGS")
    print("=" * 100)

    print("""
  FINDING 1: ALL SPLIT PRIMES HAVE ALL THREE FORCES (truncated product)
  =====================================================================
  Every split prime p ≡ ±1 mod 5 shows η_trunc ≠ 0, θ₃ ≠ θ₄, and 1/α defined.
  Under truncation at ord(q)-1 terms, no force dies at ANY split prime.

  This means the "J₁ = EM-only" result was about the INFINITE product:
    η_∞ = 0 always (since q^m=1 for m=ord(q), killing a factor)
  The truncated product captures the "one-cycle shadow" of the strong force.

  REINTERPRETATION: The distinction between fibers is NOT "which forces survive"
  but rather the DEPTH of the force (ord(q) = how many levels of structure exist).
  p=11 has ord(q)=5 (shallowest), p=79 has ord(q)=78 (deepest).

  FINDING 2: INERT PRIMES SHOW REAL FORCE DEATH
  =====================================================
  At p=2 (GF(4)) and p=7 (GF(49)): θ₃ = θ₄ → weak force genuinely dead.
  At p=2: also η_trunc = 1 (trivially nonzero, ord=3 means only 2 factors).
  These inert primes require GF(p²) and show genuinely different physics.

  The weak force death at p=2 is EXACTLY the triality universe prediction:
  when φ = ω (cube root of unity), all distinction between θ₃ and θ₄ vanishes.

  p=7 is NEW: weak force dead in GF(49). θ₃ = θ₄ = 3φ.
  This is a SECOND triality-like fiber, unreported before.

  FINDING 3: ord(q) = (p-1)/gcd(p-1, Pisano period structure)
  =============================================================
  For split primes, ord(q) always divides p-1 AND the Pisano period π(p).
  In fact ord(q) = π(p)/2 when π(p) is even, or ord(q) = π(p) otherwise.
  Specifically: π(p)/ord(q) ∈ {1, 2} for ALL split primes computed.

  This means: π(p)/ord(q) = 1 iff q is a primitive Fibonacci root mod p
             π(p)/ord(q) = 2 iff q and its conjugate have the same order

  FINDING 4: FASCINATING θ₄ = 1 PATTERN
  =======================================
  At p = 11, 19, 29, 59, 71: θ₄ ≡ 1 mod p. These are all Monster primes.
  At Monster split primes with θ₄ ≠ 1: p = 31, 41.
  At non-Monster split primes: θ₄ is NEVER 1 (p=61,79,89 all have θ₄ ≠ 1).

  Possible pattern: θ₄ = 1 correlates with Monster membership.
  Of 7 Monster split primes: 5 have θ₄ = 1 (71%).
  Of 3 non-Monster split primes: 0 have θ₄ = 1 (0%).

  If real: θ₄ ≡ 1 (mod p) could be a NUMBER-THEORETIC characterization
  of Monster primes, complementing the group-theoretic definition.

  FINDING 5: p = 3 IS THE RICHEST INERT PRIME
  =============================================
  At p=3 in GF(9): all three forces survive! η_trunc ≠ 0, θ₃ ≠ θ₄, 1/α = 2.
  The triality prime 3 doesn't kill physics — it compresses it into GF(9).
  Compare: p=2 (GF(4)) and p=7 (GF(49)) both lose the weak force.
  p=3 is special: the "inner 3" of S₃ flavor symmetry is the only small
  inert prime where full physics survives.

  FINDING 6: (p-1)/ord(q) = 1 or 2 DICHOTOMY
  =============================================
  For all split primes, (p-1)/ord(q) is either 1 or 2.
  = 1: q is a PRIMITIVE ROOT mod p (p = 31, 41, 61, 79)
  = 2: q has "half-primitive" order (p = 11, 19, 29, 59, 71, 89)

  Primitive root primes: q generates all of GF(p)*. Maximum structure.
  Half-order primes: q generates a subgroup of index 2. Less structure.

  Is there a correlation with Monster? Monster split primes with ratio 2:
  p = 11, 19, 29, 59, 71 (5 primes). With ratio 1: p = 31, 41 (2 primes).
  Non-Monster with ratio 2: p = 89. With ratio 1: p = 61, 79.
  Suggestive but sample too small.

  FINDING 7: VACUUM SEPARATION = √5 mod p (always)
  ==================================================
  For every split prime, the two vacua φ and -1/φ have separation ≡ ±√5 mod p.
  This is just algebra (φ - (-1/φ) = √5), but it confirms that the
  "inter-vacuum distance" — the kink width in the framework — is controlled
  by √5 at every prime. The golden ratio geometry persists mod p.
""")

    # Final: one-line per prime summary
    print("\n  COMPACT SUMMARY — ALL 25 PRIMES:")
    print("  " + "-" * 90)

    universe_types = {
        5: "Level 0: no kink (Ly)",
        2: "Triality: φ=ω, weak dead (J₃)",
    }

    for p in all_primes:
        cl = classify_prime(p)
        in_m = 'M' if p in MONSTER_PRIMES else ' '
        in_p = 'P' if p in PARIAH_PRIMES else ' '

        if p in universe_types:
            desc = universe_types[p]
        elif cl == "SPLIT":
            r = [x for x in results if x['p'] == p and x['type'] == 'SPLIT']
            if r:
                r = r[0]
                o = r['ord_q']
                t4_note = ", θ₄=1" if r['theta4'] == 1 else ""
                desc = f"SPLIT: ord(q)={o}, depth={(p-1)//o}, 1/α={r['alpha_inv']}{t4_note}"
            else:
                desc = "SPLIT: not computed"
        elif cl == "INERT":
            inert_data = [x for x in results if x.get('p') == p and x.get('type') == 'INERT']
            if inert_data:
                r = inert_data[0]
                w = "weak alive" if r['weak'] else "WEAK DEAD"
                desc = f"INERT(GF({p}²)): ord(q)={r['ord_q']}, {w}"
            else:
                desc = f"INERT(GF({p}²)): not computed"
        else:
            desc = f"{cl}"

        print(f"    p={p:3d} [{in_m}{in_p}] {desc}")

    print("\n" + "=" * 100)
    print("COMPUTATION COMPLETE")
    print("=" * 100)


# Helper at module level for Pisano
def pisano_period(p):
    """Compute the Pisano period π(p) = period of Fibonacci sequence mod p."""
    if p == 0: return 0
    f_prev, f_curr = 0, 1
    for i in range(1, 6 * p + 4):
        f_prev, f_curr = f_curr, (f_prev + f_curr) % p
        if f_prev == 0 and f_curr == 1:
            return i
    return -1


if __name__ == "__main__":
    main()
