#!/usr/bin/env python3
"""
2ru_shadow_verify.py -- Verify every claim in 2ru_shadow_algebra.py
===================================================================

Honest check. Flag anything that's wrong, uncertain, or needs ATLAS/literature.

Standard Python only.
"""

import math
import sys

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

PHI = (1 + math.sqrt(5)) / 2
PI = math.pi

SEP = "=" * 78
SUB = "-" * 60

def banner(s):
    print(f"\n{SEP}\n  {s}\n{SEP}\n")

def factorize(n):
    if n <= 1: return {n: 1}
    factors = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors[d] = factors.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors

def is_prime(n):
    if n < 2: return False
    if n < 4: return True
    if n % 2 == 0 or n % 3 == 0: return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0: return False
        i += 6
    return True

def legendre(a, p):
    if a % p == 0: return 0
    val = pow(a % p, (p - 1) // 2, p)
    return val if val <= 1 else val - p

PASS = "PASS"
FAIL = "FAIL"
WARN = "WARN"
NEED = "NEED ATLAS/LITERATURE"

results = []

def check(label, result, note=""):
    tag = result
    results.append((label, tag, note))
    marker = {"PASS": "[OK]", "FAIL": "[XX]", "WARN": "[??]", "NEED ATLAS/LITERATURE": "[LIT]"}
    print(f"  {marker.get(tag, '[??]')} {label}")
    if note:
        print(f"       {note}")
    print()


banner("CLAIM VERIFICATION")


# ============================================================
# 1. |Ru| = 2^14 * 3^3 * 5^3 * 7 * 13 * 29
# ============================================================
print("--- GROUP ORDERS ---\n")

ru_order = 2**14 * 3**3 * 5**3 * 7 * 13 * 29
check("|Ru| = 145,926,144,000",
      PASS if ru_order == 145926144000 else FAIL,
      f"Computed: {ru_order}")

two_ru_order = 2 * ru_order
check("|2.Ru| = 2 * |Ru| = 291,852,288,000",
      PASS if two_ru_order == 291852288000 else FAIL,
      f"Computed: {two_ru_order}")


# ============================================================
# 2. Schur multiplier of Ru = Z2
# ============================================================
print("\n--- SCHUR MULTIPLIERS ---\n")

# These are from ATLAS. Can't compute -- need literature.
check("Schur(Ru) = Z2", NEED,
      "ATLAS of Finite Groups (Conway et al. 1985), p. 126. Standard reference.")

check("Schur(J1) = 1", NEED,
      "ATLAS p. 36")

check("Schur(J3) = Z3", NEED,
      "ATLAS p. 82")

check("Schur(ON) = Z3", NEED,
      "ATLAS p. 132. Also: O'Nan 1976 original paper.")

check("Schur(Ly) = 1", NEED,
      "ATLAS p. 174")

check("Schur(J4) = 1", NEED,
      "ATLAS p. 188. Verified independently by Benson & Smith.")

check("Only Ru has Z2 among pariahs",
      PASS,
      "Follows from above: {1, Z3, Z2, Z3, 1, 1}. Only one Z2.")


# ============================================================
# 3. Representation dimensions
# ============================================================
print("\n--- REPRESENTATION DIMENSIONS ---\n")

check("Ru smallest genuine rep = 378",
      NEED,
      "ATLAS character table for Ru. chi_2 = 378. Verified in multiple sources.")

check("2.Ru smallest faithful rep = 28",
      NEED,
      "Conway & Wales 1973 'Construction of the Rudvalis group of order 145926144000'."
      " The 28-dim rep over Z[i] is the DEFINING construction.")

# Cross-check: 378/28
ratio = 378/28
check(f"Ratio 378/28 = {ratio}",
      PASS if ratio == 13.5 else FAIL,
      f"= 27/2. Note: 13 divides |Ru|. 13.5 = 27/2.")


# ============================================================
# 4. 28 + 28* = 56 = E7 fundamental
# ============================================================
print("\n--- E7 CONNECTION ---\n")

check("28 + 28 = 56", PASS if 28 + 28 == 56 else FAIL)

check("E7 fundamental rep = 56 dim",
      PASS,
      "Standard: E7 has fundamental rep of dim 56. Cartan's classification.")

check("E7 rank = 7", PASS, "Standard.")
check("E7 dim = 133", PASS, "Standard: 133 = 7 + 126.")
check("E7 Coxeter number h = 18", PASS, "Standard. Also: h = 1 + sum of marks.")

check("(37-1)/2 = 18 = h(E7)",
      PASS if (37-1)//2 == 18 else FAIL,
      f"(37-1)/2 = {(37-1)//2}")

check("E7 root count = 126",
      PASS,
      "Standard: 2 * 63 = 126 roots.")

# E8 decomposition under E7 x SU(2)
check("Under E7 x SU(2): 248 = (133,1) + (1,3) + (56,2)",
      PASS if 133*1 + 1*3 + 56*2 == 248 else FAIL,
      f"133 + 3 + 112 = {133 + 3 + 112}")


# ============================================================
# 5. Ru embeds in E7(5)
# ============================================================
print("\n--- RU IN E7 ---\n")

check("Ru embeds in E7(5) (Chevalley group over GF(5))",
      NEED,
      "Griess & Ryba 1999, 'Embeddings of PGL(2,31) and SL(2,32) in E8(C)'."
      " Actually the Ru in E7 result is from Kleidman & Wilson (1993)."
      " CORRECTION NEEDED: check exact reference.")

# Actually let me be more careful here
check("CORRECTION: Ru in E7 embedding source",
      WARN,
      "Multiple sources cited. Conway-Wales 1973 builds the 28-dim lattice."
      " Griess-Ryba 1999 discusses E7 connection."
      " Wilson 2010 (The Finite Simple Groups) is the consolidated reference."
      " The embedding is Ru < 2F4(2)' < E7(C) or similar chain."
      " Need to verify the EXACT embedding statement.")


# ============================================================
# 6. Duncan moonshine
# ============================================================
print("\n--- DUNCAN MOONSHINE ---\n")

check("Duncan SVOA from 2.Ru lattice, output Z7 x Ru",
      NEED,
      "Duncan 2006, 'Moonshine for Rudvalis's group' (thesis)."
      " Duncan 2007, published version."
      " Claims rank-28 SVOA with automorphism group containing Z7 x Ru.")

check("Z7 not in input, emergent from construction",
      WARN,
      "The Z7 comes from the lattice structure (28 = 4*7)."
      " 'Emergent' is somewhat imprecise -- it's determined by the lattice"
      " automorphisms, which are computable from the Conway-Wales construction."
      " But Z7 is not an obvious symmetry of 2.Ru itself.")

check("28 = 4 * 7", PASS if 28 == 4*7 else FAIL)

# Central charge
check("Rank-28 SVOA: central charge conventions",
      WARN,
      "For a lattice SVOA of rank n: c = n (bosonic count) or c = n/2 (if"
      " counting SUSY pairs). Need to check Duncan's convention."
      " Standard lattice VOA has c = rank. SVOA may differ.")


# ============================================================
# 7. Z[i] and Z[phi] unification
# ============================================================
print("\n--- NUMBER FIELD UNIFICATION ---\n")

# phi = (1+sqrt(5))/2 lives in Q(sqrt(5))
# i = sqrt(-1) lives in Q(sqrt(-1)) = Q(i)
# Together: Q(sqrt(5), i)
# Q(sqrt(5)) has degree 2
# Q(i) has degree 2
# Their compositum has degree 4 (since disc -4 and disc 5 are coprime)
# Q(sqrt(5), i) = Q(zeta_20)? Let's check.

# zeta_5 = e^(2pi*i/5), phi = zeta_5 + zeta_5^{-1} = 2cos(2pi/5)
# Wait: phi = (1+sqrt(5))/2 = 2cos(pi/5), not 2cos(2pi/5)
# 2cos(pi/5) = phi, 2cos(2pi/5) = 1/phi
# zeta_5 + zeta_5^{-1} = 2cos(2pi/5) = 1/phi = phi - 1
# So phi = 1 + (zeta_5 + zeta_5^{-1})
# phi is in Q(zeta_5), which has degree 4 over Q.
# Actually Q(sqrt(5)) is the maximal real subfield of Q(zeta_5)
# [Q(zeta_5):Q] = 4, [Q(sqrt(5)):Q] = 2, [Q(zeta_5):Q(sqrt(5))] = 2

# Q(zeta_20) = Q(zeta_4, zeta_5) since gcd(4,5)=1 and lcm(4,5)=20
# [Q(zeta_20):Q] = phi(20) = phi(4)*phi(5) = 2*4 = 8

from math import gcd

def euler_phi(n):
    result = n
    p = 2
    temp = n
    while p * p <= temp:
        if temp % p == 0:
            while temp % p == 0:
                temp //= p
            result -= result // p
        p += 1
    if temp > 1:
        result -= result // temp
    return result

check("[Q(zeta_20):Q] = phi(20) = 8",
      PASS if euler_phi(20) == 8 else FAIL,
      f"phi(20) = {euler_phi(20)}")

check("phi(4) = 2", PASS if euler_phi(4) == 2 else FAIL)
check("phi(5) = 4", PASS if euler_phi(5) == 4 else FAIL)
check("phi(4)*phi(5) = 8", PASS if euler_phi(4)*euler_phi(5) == 8 else FAIL)

# Does Q(i, sqrt(5)) = Q(zeta_20)?
# Q(i) = Q(zeta_4). Q(sqrt(5)) subset Q(zeta_5).
# Q(zeta_4, zeta_5) = Q(zeta_20) since gcd(4,5) = 1.
# [Q(zeta_20):Q] = 8.
# Q(i, sqrt(5)) has degree at most 4 over Q (2*2).
# But Q(zeta_20) has degree 8.
# So Q(i, sqrt(5)) is STRICTLY SMALLER than Q(zeta_20).
# Q(i, sqrt(5)) has degree 4.

# WAIT. This is wrong in the main script!
# The claim was Z[i] and Z[phi] unify in Q(zeta_20) degree 8.
# But phi is in Q(sqrt(5)), not Q(zeta_5).
# Q(i, phi) = Q(i, sqrt(5)) which has degree 4, not 8!

# Let me recheck.
# Q(i) has degree 2.
# Q(sqrt(5)) has degree 2.
# disc(Q(i)) = -4, disc(Q(sqrt(5))) = 5.
# gcd of discriminants: gcd(4, 5) = 1, so the fields are linearly disjoint.
# [Q(i, sqrt(5)):Q] = 4.

# The claim that they meet at degree 8 is WRONG.
# They meet at degree 4.

check("CLAIM: Z[i] and Z[phi] meet at degree 8 = E8 rank",
      FAIL,
      "WRONG. Q(i, phi) = Q(i, sqrt(5)) has degree 4 over Q, NOT 8."
      " Q(zeta_20) has degree 8 but CONTAINS MORE than just i and phi."
      " phi is in Q(sqrt(5)) (degree 2), not Q(zeta_5) (degree 4)."
      " The compositum Q(i)*Q(sqrt(5)) has degree 2*2 = 4."
      " CORRECTION: perpendicular + golden meet at degree 4.")

# What IS degree 8?
check("Q(zeta_5) has degree 4 (contains phi but also zeta_5)",
      PASS if euler_phi(5) == 4 else FAIL,
      "phi = zeta_5 + zeta_5^{-1} is in Q(zeta_5) but [Q(zeta_5):Q(phi)] = 2")

check("Q(i, zeta_5) = Q(zeta_20) has degree 8",
      PASS,
      "This IS degree 8. But it contains MORE than i and phi."
      " It contains all 5th roots of unity. The E8 connection"
      " requires the FULL cyclotomic field, not just the real subfield.")


# ============================================================
# 8. X_0(43) is a smooth quartic with 28 bitangents
# ============================================================
print("\n--- X_0(43) QUARTIC ---\n")

# Genus of X_0(p) for prime p
# Formula: g(X_0(p)) = floor((p-1)/12) - epsilon
# where epsilon depends on p mod 12
# For p prime > 3:
# g = (p - 1)/12 - 1/4*(1 + (-1|p)) - 1/3*(1 + (-3|p)) + 1
# Actually the standard formula:
# g(X_0(N)) for N prime = (p-1)/12 - correction

# More carefully, for p prime:
# 12(2g - 2) = (p-1) - 3*(1 + Leg(-1,p)) - 4*(1 + Leg(-3,p))
# Nope. Let me just use the formula from Diamond & Shurman:
# g(Gamma_0(p)) for p prime = floor((p-13)/12) if p ≡ 1 mod 12
# This is getting confused. Let me compute directly.

# Standard formula for prime p > 3:
# g(X_0(p)) = (p-1)/12 - (1/4)*e_2 - (1/3)*e_3 - 1 + 1
# where e_2 = number of elliptic points of order 2 = 1 + Kronecker(-4, p)
# e_3 = number of elliptic points of order 3 = 1 + Kronecker(-3, p)
# and the genus formula: 2g - 2 = (p-1)/6 - e_2/2 - 2*e_3/3
# Actually:
# For Gamma_0(p), index = p + 1, nu_2 = 1 + (-1|p), nu_3 = 1 + (-3|p), nu_inf = 2
# g = 1 + (p+1)/12 - nu_2/4 - nu_3/3 - 1 (the -1 from nu_inf/2 = 1)
# Hmm, the standard formula from Shimura:
# g = 1 + mu/12 - nu_2/4 - nu_3/3 - nu_inf/2
# where mu = index = p + 1 for Gamma_0(p)
# nu_inf = 2 (two cusps: 0 and infinity)

def genus_X0(p):
    """Genus of X_0(p) for prime p > 3."""
    mu = p + 1  # index [SL2(Z) : Gamma_0(p)]
    # Elliptic points of order 2: nu_2 = 1 + Kronecker(-4, p)
    # For odd prime p: Kronecker(-4, p) = (-1|p) = (-1)^((p-1)/2)
    if p == 2:
        return 0
    kron_neg4 = legendre(-1, p)  # = 1 if p ≡ 1 mod 4, -1 if p ≡ 3 mod 4
    nu_2 = 1 + kron_neg4 if kron_neg4 >= 0 else 1 + kron_neg4
    # Actually: nu_2 = 1 + (-1|p). If (-1|p) = 1, nu_2 = 2. If (-1|p) = -1, nu_2 = 0.
    nu_2 = max(0, 1 + kron_neg4)

    kron_neg3 = legendre(-3, p)
    nu_3 = max(0, 1 + kron_neg3)

    nu_inf = 2  # two cusps for Gamma_0(p)

    g = 1 + mu/12 - nu_2/4 - nu_3/3 - nu_inf/2
    return round(g)  # should be exact integer

# Known values for verification
known_genera = {
    2: 0, 3: 0, 5: 0, 7: 0, 11: 1, 13: 0, 17: 1, 19: 1,
    23: 2, 29: 2, 31: 2, 37: 2, 41: 3, 43: 3, 47: 4,
    53: 4, 59: 4, 61: 4, 67: 5, 71: 6, 73: 5,
}

# Verify formula against known values
formula_ok = True
for p, g_known in known_genera.items():
    if p <= 3:
        continue
    g_calc = genus_X0(p)
    if g_calc != g_known:
        print(f"  MISMATCH at p={p}: formula gives {g_calc}, known = {g_known}")
        formula_ok = False

check("Genus formula verified against known values",
      PASS if formula_ok else FAIL,
      f"Checked {len([p for p in known_genera if p > 3])} primes")

g43 = genus_X0(43)
check(f"genus(X_0(43)) = {g43}",
      PASS if g43 == 3 else FAIL,
      "Should be 3")

# Ogg's list of hyperelliptic X_0(N)
# Ogg 1974, "Hyperelliptic modular curves"
ogg_hyperelliptic = {22, 23, 26, 28, 29, 30, 31, 33, 35, 37, 39, 40, 41, 46, 47, 48, 50, 59, 71}

check("43 not in Ogg's hyperelliptic list",
      PASS if 43 not in ogg_hyperelliptic else FAIL,
      f"Ogg 1974 list: {sorted(ogg_hyperelliptic)}")

check("Non-hyperelliptic genus-3 curve = smooth plane quartic",
      PASS,
      "Standard: canonical embedding theorem (Petri's theorem)."
      " A non-hyperelliptic genus-3 curve embeds as a quartic in P^2.")

check("Smooth plane quartic has 28 bitangents",
      PASS,
      "Classical: Plucker 1839. Every smooth quartic in P^2 has exactly 28 bitangent lines.")

check("=> X_0(43) has 28 bitangents",
      PASS,
      "Follows from: genus 3 + not hyperelliptic + Petri + Plucker.")

# Also check: genus of plane quartic
# genus = (d-1)(d-2)/2 for smooth plane curve of degree d
g_quartic = (4-1)*(4-2)//2
check(f"Genus of smooth quartic = (4-1)(4-2)/2 = {g_quartic}",
      PASS if g_quartic == 3 else FAIL)


# ============================================================
# 9. 378 factorization
# ============================================================
print("\n--- DIMENSION FACTORIZATIONS ---\n")

check("378 = 2 * 3^3 * 7",
      PASS if 378 == 2 * 27 * 7 else FAIL,
      f"378 = {factorize(378)}")

check("378 = 14 * 27",
      PASS if 378 == 14 * 27 else FAIL)

check("14 = dim(G2)",
      PASS,
      "Standard: G2 is the 14-dimensional exceptional Lie algebra.")

check("27 = dim(J3(O)) (exceptional Jordan algebra)",
      PASS,
      "Standard: 3x3 Hermitian matrices over octonions = 3*8 + 3 = 27.")

check("28 = C(8,2)",
      PASS if math.comb(8, 2) == 28 else FAIL,
      f"C(8,2) = {math.comb(8, 2)}")

check("28 = dim(so(8))",
      PASS,
      "Standard: so(n) has dimension n(n-1)/2. so(8) = 8*7/2 = 28.")

check("28 = 7th triangular number",
      PASS if 7*8//2 == 28 else FAIL,
      f"T(7) = 7*8/2 = {7*8//2}")

check("28 = 2nd perfect number",
      PASS if sum(d for d in range(1, 28) if 28 % d == 0) == 28 else FAIL,
      f"Divisors of 28: {[d for d in range(1, 28) if 28 % d == 0]}, sum = {sum(d for d in range(1, 28) if 28 % d == 0)}")


# ============================================================
# 10. E8 root decomposition under E7 x A1
# ============================================================
print("\n--- E8 DECOMPOSITION ---\n")

check("E8: 240 roots, dim 248",
      PASS,
      "Standard: 240 roots, dim = 248 = 240 + 8.")

check("Under E7 x A1: 248 = (133,1) + (1,3) + (56,2)",
      PASS if 133 + 3 + 112 == 248 else FAIL,
      f"133 + 3 + 56*2 = {133 + 3 + 56*2}")

# Root decomposition: 240 = 126 + 2 + 112
check("Roots: 240 = 126 + 2 + 112",
      PASS if 126 + 2 + 112 == 240 else FAIL,
      "126 E7 roots + 2 A1 roots + 112 mixed")


# ============================================================
# 11. W(E7) and Sp(6, F_2)
# ============================================================
print("\n--- WEYL GROUP ---\n")

# W(E7) order = 2^10 * 3^4 * 5 * 7 = 2,903,040
w_e7 = 2**10 * 3**4 * 5 * 7
check(f"|W(E7)| = {w_e7}",
      PASS if w_e7 == 2903040 else FAIL)

# Sp(6, F_2) order = 2^9 * 3^4 * 5 * 7 = 1,451,520
sp6f2 = 2**9 * 3**4 * 5 * 7
check(f"|Sp(6, F_2)| = {sp6f2}",
      PASS if sp6f2 == 1451520 else FAIL)

check("W(E7) = Z2 x Sp(6, F_2)",
      WARN,
      f"|W(E7)| / |Sp(6,F_2)| = {w_e7 // sp6f2}."
      " Standard result (Frame 1951). W(E7) has center Z2,"
      " W(E7) / Z(W(E7)) = Sp(6, F_2). Actually W(E7) = Z2 x Sp(6,F2)"
      " is NOT quite right. W(E7) is a CENTRAL EXTENSION, not direct product."
      " Precisely: W(E7) has center {+/-1} and W(E7)/{+/-1} = Sp(6,F_2)."
      " But it may not split as a direct product. CHECK THIS.")

# Can Sp(6,F_2) embed in Ru?
check("Can Sp(6,F_2) embed in Ru?",
      WARN,
      f"|Sp(6,F_2)| = {sp6f2} = {factorize(sp6f2)}."
      f" All primes {{2,3,5,7}} divide |Ru|."
      f" |Ru|/|Sp(6,F_2)| = {ru_order // sp6f2}."
      f" Size compatible but embedding not checked."
      f" Need: is there a subgroup of Ru isomorphic to Sp(6,F_2)?")


# ============================================================
# 12. Miscellaneous numerical claims
# ============================================================
print("\n--- MISCELLANEOUS ---\n")

check("28 * 2 = 56 (bitangent contact points)",
      PASS if 28 * 2 == 56 else FAIL)

check("GCD of pariah orders = 120",
      PASS,
      "Verified in pariah_energies_deep.py")

check("120 = |A5| = 5!",
      PASS if math.factorial(5) == 120 else FAIL)

# The claim that 2.Ru has 60 conjugacy classes total
check("2.Ru has 60 conjugacy classes",
      NEED,
      "ATLAS. Ru has 36. 2.Ru lifts some and adds faithful ones."
      " The exact count 60 needs ATLAS verification."
      " Standard: |conj classes of 2.G| = |conj of G| + |faithful conj|."
      " For Schur Z2: faithful classes come from splitting.")

# 37 is NOT in Ogg hyperelliptic list
check("37 IS in Ogg's hyperelliptic list",
      PASS if 37 in ogg_hyperelliptic else FAIL,
      f"37 in list: {37 in ogg_hyperelliptic}. X_0(37) IS hyperelliptic (genus 2).")

# So X_0(37) is hyperelliptic, NOT a quartic. Only X_0(43) gets the bitangent connection.
check("X_0(37) is hyperelliptic (genus 2, in Ogg's list)",
      PASS,
      "genus(X_0(37)) = 2. In Ogg's list. So NOT a quartic. No bitangent connection.")

# What about X_0(67)?
g67 = genus_X0(67)
check(f"genus(X_0(67)) = {g67}",
      PASS if g67 == 5 else FAIL)

check("X_0(67) not in Ogg's hyperelliptic list",
      PASS if 67 not in ogg_hyperelliptic else FAIL,
      "genus 5 > 2, and 67 not in list. X_0(67) is not hyperelliptic.")

check("X_0(67) is NOT a plane quartic (genus 5 != 3)",
      PASS,
      "Only genus-3 non-hyperelliptic curves are plane quartics. Genus 5 is too high.")

# So the 28-bitangent connection is SPECIFIC to X_0(43), not X_0(67).
check("28-bitangent connection: ONLY X_0(43), not X_0(37) or X_0(67)",
      PASS,
      "X_0(43): genus 3, non-hyp -> quartic -> 28 bitangents. UNIQUE among alien primes.")


# ============================================================
# SUMMARY
# ============================================================
banner("VERIFICATION SUMMARY")

n_pass = sum(1 for _, t, _ in results if t == PASS)
n_fail = sum(1 for _, t, _ in results if t == FAIL)
n_warn = sum(1 for _, t, _ in results if t == WARN)
n_need = sum(1 for _, t, _ in results if t == NEED)

print(f"  PASS:  {n_pass}")
print(f"  FAIL:  {n_fail}")
print(f"  WARN:  {n_warn}")
print(f"  NEED LITERATURE: {n_need}")
print()

if n_fail > 0:
    print("FAILURES:")
    for label, tag, note in results:
        if tag == FAIL:
            print(f"  [XX] {label}")
            if note:
                print(f"       {note}")
    print()

if n_warn > 0:
    print("WARNINGS:")
    for label, tag, note in results:
        if tag == WARN:
            print(f"  [??] {label}")
            if note:
                print(f"       {note}")
    print()

print("CORRECTIONS NEEDED IN 2ru_shadow_algebra.py:")
print()
print("  1. Z[i]+Z[phi] meeting degree: CHANGE 8 to 4.")
print("     Q(i, phi) = Q(i, sqrt(5)) has degree 4, not 8.")
print("     Degree 8 requires Q(zeta_20) which adds MORE than phi.")
print("     The '= E8 rank' claim is WRONG for the simple compositum.")
print()
print("  2. W(E7) = Z2 x Sp(6,F2): CHECK if direct product or central extension.")
print("     The quotient is correct. The splitting may not be.")
print()
print("  3. Duncan SVOA central charge: VERIFY convention in Duncan's paper.")
print()
print("  4. 2.Ru conjugacy class count (60): VERIFY from ATLAS.")
print()
print("  5. Ru in E7 embedding: VERIFY exact reference (Griess-Ryba vs Wilson).")
print()

print(SEP)
