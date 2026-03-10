#!/usr/bin/env python3
"""
golden_closure.py -- Fibonacci ratio closure in dictionary products
====================================================================
Explores how products of F/L dictionary entries produce consecutive
Fibonacci ratios F(n)/F(n+1) (which converge to 1/phi) or F(n+1)/F(n)
(which converge to phi).

Key known examples:
  alpha_s * m_c * m_b = F(16)/F(15) ~ phi (0.0001%)
  g/2 * m_t/m_Z = F(11)/F(12) ~ 1/phi (0.0035%)
  K_lepton = F(3)/F(4) = 2/3 (exact, also a Fibonacci ratio!)

ASCII-safe output for Windows.
"""

from math import sqrt, gcd, log
from itertools import combinations
from collections import defaultdict

# =====================================================================
# FIBONACCI AND LUCAS
# =====================================================================

def F(n):
    if n < 0: return ((-1) ** (n + 1)) * F(-n)
    if n == 0: return 0
    if n == 1: return 1
    a, b = 0, 1
    for _ in range(n - 1): a, b = b, a + b
    return b

def L(n):
    if n < 0: return ((-1) ** n) * L(-n)
    if n == 0: return 2
    if n == 1: return 1
    a, b = 2, 1
    for _ in range(n - 1): a, b = b, a + b
    return b

phi = (1 + sqrt(5)) / 2
phibar = 1 / phi

fib_table = {F(n): n for n in range(0, 40)}
luc_table = {L(n): n for n in range(0, 35)}

def identify_int(val):
    if not isinstance(val, int): return None
    if val in fib_table: return "F(%d)" % fib_table[val]
    if val in luc_table: return "L(%d)" % luc_table[val]
    return None

# =====================================================================
# THE COMPLETE F/L DICTIONARY
# =====================================================================

def entry(name, num, den, formula_str=""):
    return {"name": name, "num": num, "den": den,
            "value": num / den if den != 0 else 0,
            "formula": formula_str if formula_str else "%d/%d" % (num, den)}

D = []

# F(15)=610 denominator family
D.append(entry("alpha_s", L(3)*L(8), F(15), "L(3)*L(8)/F(15)"))
D.append(entry("V_us", F(11), F(15), "F(11)/F(15)"))
D.append(entry("V_cb", L(4)+L(6), F(15), "(L(4)+L(6))/F(15)"))
D.append(entry("sin2_23", L(5)+L(12), F(15), "(L(5)+L(12))/F(15)"))
D.append(entry("m_t/m_H", L(7)**2, F(15), "L(7)^2/F(15)"))

# L(9)=76 denominator family
D.append(entry("V_ud", L(9)-F(3), L(9), "(L(9)-F(3))/L(9)"))
D.append(entry("1-V_ud", F(3), L(9), "F(3)/L(9)"))
D.append(entry("sin2_12", L(9)-3*F(3), 3*L(9), "(L(9)-3F(3))/(3L(9))"))

# L(2)=3 denominator
D.append(entry("M_H", F(14), L(2), "F(14)/L(2)"))
D.append(entry("m_t", L(13), L(2), "L(13)/L(2)"))

# L(3)=4 denominator
D.append(entry("v", F(16), L(3), "F(16)/L(3)"))
D.append(entry("M_W", L(12), L(3), "L(12)/L(3)"))
D.append(entry("m_c", F(5), L(3), "F(5)/L(3)"))

# F(5)=5 denominator
D.append(entry("m_b", F(8), F(5), "F(8)/F(5)"))

# L(13)=521 denominator
D.append(entry("y_t", L(5)*L(8), L(13), "L(5)*L(8)/L(13)"))

# F(14)=377 denominator
D.append(entry("y_b", L(2)**2, F(14), "L(2)^2/F(14)"))

# L(15)=1364 denominator
D.append(entry("y_tau", F(3)*L(4), L(15), "F(3)*L(4)/L(15)"))

# L(22)=39603 denominator
D.append(entry("y_mu", L(2)*F(6), L(22), "L(2)*F(6)/L(22)"))

# L(19)=9349 denominator
D.append(entry("y_s", F(5), L(19), "F(5)/L(19)"))
D.append(entry("V_tb", L(19)-F(6), L(19), "(L(19)-F(6))/L(19)"))

# F(25)=75025 denominator
D.append(entry("y_d", F(3), F(25), "F(3)/F(25)"))

# CKM additional
D.append(entry("V_ub", 1, L(7)+F(13), "1/(L(7)+F(13))"))
D.append(entry("V_cd", L(7), F(6)+L(10), "L(7)/(F(6)+L(10))"))
D.append(entry("V_cs", F(4)+L(14)-L(5), F(4)+L(14), "(F(4)+L(14)-L(5))/(F(4)+L(14))"))
D.append(entry("V_td", 1, F(3)+L(10), "1/(F(3)+L(10))"))
D.append(entry("V_ts", F(7), F(7)+L(12), "F(7)/(F(7)+L(12))"))

# PMNS
D.append(entry("sin2_13", L(5), L(10)+F(14), "L(5)/(L(10)+F(14))"))

# Cosmological
D.append(entry("Omega_m", L(7), F(4)+F(11), "L(7)/(F(4)+F(11))"))
D.append(entry("Omega_L", F(13), L(6)+L(12), "F(13)/(L(6)+L(12))"))
D.append(entry("n_s", F(10), F(3)+F(10), "F(10)/(F(3)+F(10))"))
D.append(entry("sigma_8", L(8), L(5)+L(8), "L(8)/(L(5)+L(8))"))
D.append(entry("Omega_b", L(4)+L(11), F(19), "(L(4)+L(11))/F(19)"))
D.append(entry("Omega_c", L(5)+F(11), F(14), "(L(5)+F(11))/F(14)"))

# Other physics
D.append(entry("gamma_I", F(3), L(6), "F(3)/L(6)"))
D.append(entry("R_c", F(5), L(7), "F(5)/L(7)"))
D.append(entry("a_e", L(2), F(18), "L(2)/F(18)"))
D.append(entry("alpha_2", L(2), F(11), "L(2)/F(11)"))
D.append(entry("g_half", L(8), F(12), "L(8)/F(12)"))

# Koide
D.append(entry("K_lepton", F(3), F(4), "F(3)/F(4)"))
D.append(entry("K_up", L(5), F(7), "L(5)/F(7)"))
D.append(entry("K_down", F(6), L(5), "F(6)/L(5)"))

# Mass ratios
D.append(entry("m_H/m_Z", L(5), F(6), "L(5)/F(6)"))
D.append(entry("m_t/m_Z", F(11), L(8), "F(11)/L(8)"))

# Small masses
D.append(entry("m_mu", F(7)*F(8), F(18), "F(7)*F(8)/F(18)"))
D.append(entry("m_u", L(2)**2, F(19), "L(2)^2/F(19)"))

# Biological
D.append(entry("r_tensor", L(6), L(12), "L(6)/L(12)"))
D.append(entry("Chl_a", L(3), L(7), "L(3)/L(7)"))
D.append(entry("Chl_b", 1, L(4), "1/L(4)"))
D.append(entry("retinal", F(3), L(5), "F(3)/L(5)"))

# H0 proxy
D.append(entry("H0", L(6)+L(13), F(6), "(L(6)+L(13))/F(6)"))

# Pure framework
D.append(entry("1_3_const", 1, L(2), "1/L(2)"))
D.append(entry("2_3_const", F(3), L(2), "F(3)/L(2)"))

N_entries = len(D)


# =====================================================================
# CHECK FUNCTIONS
# =====================================================================

def check_consec_fib(val, tol_pct=0.1):
    """Check if val matches F(n)/F(n+1) or F(n+1)/F(n) for consecutive n,
    or L(n)/L(n+1), or F(n)/L(n), L(n)/F(n)."""
    if val <= 0: return []
    results = []
    for n in range(1, 31):
        for num_val, den_val, label in [
            (F(n), F(n+1), "F(%d)/F(%d)" % (n, n+1)),
            (F(n+1), F(n), "F(%d)/F(%d)" % (n+1, n)),
            (L(n), L(n+1), "L(%d)/L(%d)" % (n, n+1)),
            (L(n+1), L(n), "L(%d)/L(%d)" % (n+1, n)),
        ]:
            if den_val == 0: continue
            target = num_val / den_val
            if target <= 0: continue
            e = abs(val - target) / target * 100
            if e < tol_pct:
                results.append((label, target, e))
        if F(n) > 0:
            for num_val, den_val, label in [
                (F(n), L(n), "F(%d)/L(%d)" % (n, n)),
                (L(n), F(n), "L(%d)/F(%d)" % (n, n)),
            ]:
                target = num_val / den_val
                e = abs(val - target) / target * 100
                if e < tol_pct:
                    results.append((label, target, e))
    results.sort(key=lambda x: x[2])
    return results


def check_broad_fib(val, tol_pct=0.05):
    """Check against broader set of F/L ratios."""
    if val <= 0: return []
    results = []
    for n in range(1, 22):
        for m in range(1, 22):
            if n == m: continue
            for num_val, den_val, label in [
                (F(n), F(m), "F(%d)/F(%d)" % (n, m)),
                (L(n), L(m), "L(%d)/L(%d)" % (n, m)),
                (F(n), L(m), "F(%d)/L(%d)" % (n, m)),
                (L(n), F(m), "L(%d)/F(%d)" % (n, m)),
            ]:
                if den_val == 0: continue
                target = num_val / den_val
                if target <= 0: continue
                e = abs(val - target) / target * 100
                if e < tol_pct:
                    results.append((label, target, e))
    results.sort(key=lambda x: x[2])
    return results


SEP = "=" * 80
DASH = "-" * 80

print(SEP)
print("GOLDEN CLOSURE: Fibonacci Ratio Products in the F/L Dictionary")
print(SEP)
print()
print("Dictionary: %d entries loaded" % N_entries)
print("phi = %.15f" % phi)
print("1/phi = %.15f" % phibar)
print()

# =====================================================================
# SECTION 1: Dictionary listing
# =====================================================================
print(SEP)
print("SECTION 1: COMPLETE DICTIONARY WITH F/L RATIONAL VALUES")
print(SEP)
print()
print("  %3s  %-14s  %12s  %-30s  %-12s  %-12s" % (
    "#", "Name", "Value", "Formula", "Num ID", "Den ID"))
print("  " + "-" * 95)
for i, e in enumerate(D):
    num_id = identify_int(e["num"]) or str(e["num"])
    den_id = identify_int(e["den"]) or str(e["den"])
    print("  %3d  %-14s  %12.8f  %-30s  %-12s  %-12s" % (
        i+1, e["name"], e["value"], e["formula"], num_id, den_id))
print()
print("Total entries: %d" % N_entries)
print()

# =====================================================================
# SECTION 2: ALL PAIRS -- F(n)/F(n+1) check
# =====================================================================
print(SEP)
print("SECTION 2: PAIR PRODUCTS MATCHING FIBONACCI/LUCAS RATIOS (within 0.1%%)")
print(SEP)
print()

pair_hits = []
for i in range(N_entries):
    for j in range(i+1, N_entries):
        prod = D[i]["value"] * D[j]["value"]
        if prod <= 0: continue
        matches = check_consec_fib(prod, tol_pct=0.1)
        if matches:
            best = matches[0]
            pair_hits.append((best[2], D[i]["name"], D[j]["name"],
                              prod, best[0], best[1]))

pair_hits.sort()
print("Found %d pair products matching Fibonacci/Lucas ratios:" % len(pair_hits))
print()
if pair_hits:
    print("  %-14s  %-14s  %12s  %-20s  %12s  %10s" % (
        "Entry A", "Entry B", "Product", "Matches", "Target", "Err %%"))
    print("  " + "-" * 90)
    for err, n1, n2, prod, label, target in pair_hits[:60]:
        marker = " ***" if err < 0.01 else " **" if err < 0.05 else ""
        print("  %-14s  %-14s  %12.8f  %-20s  %12.8f  %8.4f%%%s" % (
            n1, n2, prod, label, target, err, marker))
print()

# =====================================================================
# SECTION 3: TRIPLE PRODUCTS (top 35 entries)
# =====================================================================
print(SEP)
print("SECTION 3: TRIPLE PRODUCTS MATCHING CONSECUTIVE FIBONACCI RATIOS")
print("           (A*B*C ~ F(n)/F(n+1), using 35 most important entries)")
print(SEP)
print()

important_names = [
    "alpha_s", "V_us", "V_cb", "sin2_23", "m_t/m_H",
    "V_ud", "1-V_ud", "sin2_12",
    "M_H", "m_t", "v", "M_W", "m_c", "m_b",
    "y_t", "y_b", "y_tau",
    "V_ub", "V_cd", "V_cs", "V_td", "V_ts", "V_tb",
    "gamma_I", "R_c", "g_half",
    "K_lepton", "K_up", "K_down",
    "m_H/m_Z", "m_t/m_Z",
    "Omega_m", "Omega_L",
    "1_3_const", "2_3_const",
]

imp_D = [e for e in D if e["name"] in important_names]
print("Using %d important entries for triple search" % len(imp_D))
print()

triple_hits = []
for combo in combinations(range(len(imp_D)), 3):
    prod = 1.0
    for idx in combo: prod *= imp_D[idx]["value"]
    if prod <= 0: continue
    matches = check_consec_fib(prod, tol_pct=0.1)
    if matches:
        best = matches[0]
        names = [imp_D[idx]["name"] for idx in combo]
        triple_hits.append((best[2], names, prod, best[0], best[1]))

triple_hits.sort()
print("Found %d triple products matching Fibonacci/Lucas ratios:" % len(triple_hits))
print()
for rank, (err, names, prod, label, target) in enumerate(triple_hits[:40]):
    marker = " ***" if err < 0.01 else " **" if err < 0.05 else ""
    print("  [%2d] %-14s * %-14s * %-14s" % (rank+1, names[0], names[1], names[2]))
    print("       = %.10f ~ %s = %.10f  (err=%.6f%%)%s" % (
        prod, label, target, err, marker))
print()

# =====================================================================
# SECTION 4: CANCELLATION TRACKING
# =====================================================================
print(SEP)
print("SECTION 4: ALGEBRAIC CANCELLATION IN GOLDEN PRODUCTS")
print(SEP)
print()

print("PRODUCT 1: alpha_s * m_c * m_b")
print()
print("  alpha_s = L(3)*L(8) / F(15)  =  %d*%d / %d  = %d/%d" % (L(3), L(8), F(15), L(3)*L(8), F(15)))
print("  m_c     = F(5) / L(3)         =  %d/%d" % (F(5), L(3)))
print("  m_b     = F(8) / F(5)         =  %d/%d" % (F(8), F(5)))
print()
print("  Numerator:   L(3) * L(8) * F(5) * F(8) = %d * %d * %d * %d = %d" % (
    L(3), L(8), F(5), F(8), L(3)*L(8)*F(5)*F(8)))
print("  Denominator: F(15) * L(3) * F(5)        = %d * %d * %d = %d" % (
    F(15), L(3), F(5), F(15)*L(3)*F(5)))
print()
print("  Cancel L(3)=%d: gone from both" % L(3))
print("  Cancel F(5)=%d: gone from both" % F(5))
print()
print("  Remaining: L(8)*F(8) / F(15) = %d*%d / %d = %d/%d" % (
    L(8), F(8), F(15), L(8)*F(8), F(15)))
print()
print("  KEY IDENTITY: L(8)*F(8) = F(16) = %d" % F(16))
print("  Verify: %d * %d = %d = F(16)? %s" % (L(8), F(8), L(8)*F(8),
    "YES" if L(8)*F(8) == F(16) else "NO"))
print()
print("  Result: alpha_s * m_c * m_b = F(16)/F(15) = %d/%d = %.15f" % (
    F(16), F(15), F(16)/F(15)))
print("  phi = %.15f" % phi)
print("  Error: %.6f%%" % (abs(F(16)/F(15) - phi)/phi * 100))
print()

print("PRODUCT 2: g_half * m_t/m_Z")
print()
print("  g_half = L(8)/F(12) = %d/%d" % (L(8), F(12)))
print("  m_t/m_Z = F(11)/L(8) = %d/%d" % (F(11), L(8)))
print()
print("  Cancel L(8)=%d: F(11)/F(12) = %d/%d = %.15f" % (L(8), F(11), F(12), F(11)/F(12)))
print("  1/phi = %.15f" % phibar)
print("  Error: %.6f%%" % (abs(F(11)/F(12) - phibar)/phibar * 100))
print()

print("PRODUCT 3: K_lepton (trivial but fundamental)")
print()
print("  K_lepton = F(3)/F(4) = %d/%d = %.15f" % (F(3), F(4), F(3)/F(4)))
print("  This IS a consecutive Fibonacci ratio (n=3).")
print("  1/phi = %.15f" % phibar)
print("  Difference from 1/phi: %.4f%%" % (abs(F(3)/F(4) - phibar)/phibar * 100))
print("  But 2/3 is the EXACT charge quantum, not an approximation to phi.")
print()

# =====================================================================
# SECTION 5: L(n)*F(n) = F(2n) IDENTITY
# =====================================================================
print(SEP)
print("SECTION 5: THE KEY IDENTITY L(n)*F(n) = F(2n)")
print(SEP)
print()

print("This identity is what makes the golden product alpha_s * m_c * m_b work.")
print("After cancellation, we get L(8)*F(8)/F(15), and L(8)*F(8) = F(16).")
print()
print("  %3s  %10s  %10s  %15s  %12s  %7s" % (
    "n", "L(n)", "F(n)", "L(n)*F(n)", "F(2n)", "Match?"))
print("  " + "-" * 65)

all_match = True
for n in range(1, 21):
    prod = L(n) * F(n)
    f2n = F(2*n)
    match = "YES" if prod == f2n else "NO"
    if prod != f2n: all_match = False
    print("  %3d  %10d  %10d  %15d  %12d  %7s" % (n, L(n), F(n), prod, f2n, match))

print()
if all_match:
    print("  THEOREM VERIFIED: L(n)*F(n) = F(2n) for all n = 1..20")
else:
    print("  THEOREM FAILS for some n!")
print()

print("  PROOF of L(n)*F(n) = F(2n):")
print("    L(n) = phi^n + (-1/phi)^n")
print("    F(n) = (phi^n - (-1/phi)^n) / sqrt(5)")
print("    L(n)*F(n) = (phi^(2n) - (-1/phi)^(2n)) / sqrt(5)")
print("              = (phi^(2n) - phi^(-2n)) / sqrt(5)")
print("              = F(2n)  [by Binet formula]  QED.")
print()

# Additional: L(n)^2 - 5*F(n)^2 = 4*(-1)^n
print("  Related identity: L(n)^2 - 5*F(n)^2 = 4*(-1)^n")
print()
print("  %3s  %12s  %12s  %12s  %12s" % ("n", "L(n)^2", "5*F(n)^2", "Diff", "4*(-1)^n"))
print("  " + "-" * 56)
for n in range(1, 12):
    l2 = L(n)**2
    f52 = 5 * F(n)**2
    diff = l2 - f52
    expected = 4 * ((-1)**n)
    print("  %3d  %12d  %12d  %12d  %12d  %s" % (n, l2, f52, diff, expected,
        "OK" if diff == expected else "FAIL"))
print()

# F(m)*L(n) identity
print("  Product identity: F(m)*L(n) = F(m+n) + (-1)^(n+1) * F(m-n)")
print("  Verify m=8,n=8: F(8)*L(8) = F(16) + (-1)^9*F(0) = %d + %d = %d" % (
    F(16), (-1)**9 * F(0), F(16) + (-1)**9 * F(0)))
print("  Direct: F(8)*L(8) = %d*%d = %d  CHECK: %s" % (
    F(8), L(8), F(8)*L(8), "OK" if F(8)*L(8) == F(16) else "FAIL"))
print()

# More: what is L(n)*L(n)?
print("  Also: L(n)^2 = L(2n) + 2*(-1)^n   and   F(n)^2 = [L(2n) - 2*(-1)^n] / 5")
print()
print("  %3s  %12s  %12s  %12s  %7s" % ("n", "L(n)^2", "L(2n)+2(-1)^n", "F(n)^2", "Match?"))
print("  " + "-" * 50)
for n in range(1, 12):
    l2 = L(n)**2
    expected_l = L(2*n) + 2*((-1)**n)
    f2 = F(n)**2
    expected_f = (L(2*n) - 2*((-1)**n)) // 5 if (L(2*n) - 2*((-1)**n)) % 5 == 0 else -1
    match = "OK" if l2 == expected_l and f2 == expected_f else "FAIL"
    print("  %3d  %12d  %12d  %12d  %7s" % (n, l2, expected_l, f2, match))
print()

# =====================================================================
# SECTION 6: GENERAL THEOREM
# =====================================================================
print(SEP)
print("SECTION 6: GENERAL THEOREM -- When do products give F(n)/F(n+1)?")
print(SEP)
print()

print("""THEOREM: Any product of dictionary entries whose algebraic form reduces
to F(n)/F(n+1) (for some n >= 1) will approximate phi to accuracy:

  |F(n+1)/F(n) - phi| = 1 / (sqrt(5) * F(n)^2)   [exact]

PROOF:
  By Binet: F(n) = (phi^n - (-phi)^(-n)) / sqrt(5)
  Then F(n+1)/F(n) = phi * [1 - (-1)^(n+1) * phi^(-2n-2)] /
                           [1 - (-1)^(n+1) * phi^(-2n)]

  For the error term:
    F(n+1)/F(n) - phi = (-1)^n / (sqrt(5) * F(n)^2 * [1 + 1/(sqrt(5)*F(n))])

  Asymptotically: |F(n+1)/F(n) - phi| ~ 1 / (sqrt(5) * F(n)^2)
                                       ~ phibar^(2n) / sqrt(5)

  The KEY POINT: the algebraic cancellation determines n. The closer
  n is to infinity, the closer the ratio is to phi. The specific
  dictionary entries do not matter -- only their F/L structure.
""")

print("  Convergence table:")
print()
print("  %3s  %20s  %20s  %12s" % ("n", "F(n+1)/F(n)", "|ratio - phi|", "Digits"))
print("  " + "-" * 60)
for n in range(1, 26):
    ratio = F(n+1) / F(n)
    err = abs(ratio - phi)
    digits = -log(err + 1e-300, 10)
    print("  %3d  %20.15f  %20.2e  %10.1f" % (n, ratio, err, digits))

print()
print("  At n=15: F(16)/F(15) matches phi to ~6 digits (1e-6)")
print("  At n=11: F(12)/F(11) matches phi to ~4 digits (5e-5)")
print("  At n=3:  F(4)/F(3) = 3/2 matches phi to only 7%% (2/3 vs 0.618)")
print()

# =====================================================================
# SECTION 7: F(15)-DENOMINATOR MULTIPLICATION TABLE
# =====================================================================
print(SEP)
print("SECTION 7: MULTIPLICATION TABLE FOR F(15)-DENOMINATOR ENTRIES")
print(SEP)
print()

f15_entries = [e for e in D if e["den"] == F(15)]
print("Entries with denominator F(15)=%d:" % F(15))
for e in f15_entries:
    ni = identify_int(e["num"]) or str(e["num"])
    print("  %-14s = %4d/610  [num = %s]" % (e["name"], e["num"], ni))
print()

print("Pairwise products (numerator * numerator / F(15)^2):")
print()
hdr = "  %-14s" + "  %-14s" * len(f15_entries)
print(hdr % tuple(["A \ B"] + [e["name"] for e in f15_entries]))
print("  " + "-" * (15 * (len(f15_entries) + 1)))

for i in range(len(f15_entries)):
    row = "  %-14s" % f15_entries[i]["name"]
    for j in range(len(f15_entries)):
        prod_num = f15_entries[i]["num"] * f15_entries[j]["num"]
        prod_den = F(15) * F(15)
        g = gcd(prod_num, prod_den)
        sn = prod_num // g
        sd = prod_den // g
        fl = identify_int(sn)
        if fl:
            row += "  %-14s" % ("%s/%d" % (fl, sd))
        else:
            row += "  %-14s" % ("%d/%d" % (sn, sd))
    print(row)
print()

# Products of F(15) entries with entries from other denominators
print("F(15) entries times other-denominator entries giving Fib ratios:")
print()
other_entries = [e for e in D if e["den"] != F(15)]
f15_other_hits = []

for e15 in f15_entries:
    for eother in other_entries:
        prod = e15["value"] * eother["value"]
        if prod <= 0: continue
        matches = check_consec_fib(prod, tol_pct=0.1)
        if matches:
            best = matches[0]
            # Track what cancels
            f15_other_hits.append((best[2], e15["name"], eother["name"],
                                   prod, best[0], best[1],
                                   e15["num"], e15["den"],
                                   eother["num"], eother["den"]))

f15_other_hits.sort()
for err, n1, n2, prod, label, target, num1, den1, num2, den2 in f15_other_hits[:25]:
    marker = " ***" if err < 0.01 else " **" if err < 0.05 else ""
    pn = num1 * num2
    pd = den1 * den2
    g = gcd(pn, pd)
    print("  %-14s * %-14s = %.8f ~ %s (%.4f%%)%s" % (
        n1, n2, prod, label, err, marker))
    print("    Algebraic: %d*%d / %d*%d = %d/%d" % (
        num1, num2, den1, den2, pn//g, pd//g))
print()

# =====================================================================
# SECTION 8: CHAINS AND LOOPS
# =====================================================================
print(SEP)
print("SECTION 8: FIBONACCI RATIO CHAINS AND LOOPS")
print("           A*B ~ F(n)/F(n+1), B*C ~ F(m)/F(m+1), etc.")
print(SEP)
print()

edges = defaultdict(list)
for err, n1, n2, prod, label, target in pair_hits:
    edges[n1].append((n2, label, err, prod))
    edges[n2].append((n1, label, err, prod))

# Chains of length 2
print("Chains (A--B--C where A*B and B*C both give Fibonacci ratios):")
print()

chains_found = []
for b_name in edges:
    neighbors = edges[b_name]
    for i in range(len(neighbors)):
        for j in range(i+1, len(neighbors)):
            a_name, label_ab, err_ab, _ = neighbors[i]
            c_name, label_bc, err_bc, _ = neighbors[j]
            if a_name != c_name:
                chains_found.append((
                    err_ab + err_bc, a_name, b_name, c_name,
                    label_ab, label_bc, err_ab, err_bc))

chains_found.sort()
seen_chains = set()
printed = 0
for total_err, a, b, c, lab_ab, lab_bc, e_ab, e_bc in chains_found:
    key = tuple(sorted([a, c])) + (b,)
    if key in seen_chains: continue
    seen_chains.add(key)
    if printed >= 25: break
    print("  %s -- %s -- %s" % (a, b, c))
    print("    %s * %s ~ %s  (%.4f%%)" % (a, b, lab_ab, e_ab))
    print("    %s * %s ~ %s  (%.4f%%)" % (b, c, lab_bc, e_bc))
    # Check A*C too
    entry_a = next((e for e in D if e["name"] == a), None)
    entry_c = next((e for e in D if e["name"] == c), None)
    if entry_a and entry_c:
        ac_prod = entry_a["value"] * entry_c["value"]
        ac_matches = check_consec_fib(ac_prod, tol_pct=0.5)
        if ac_matches:
            print("    BONUS: %s * %s ~ %s  (%.4f%%)" % (
                a, c, ac_matches[0][0], ac_matches[0][2]))
    print()
    printed += 1

# Closed loops
print("Closed loops (A*B, B*C, and C*A all give Fibonacci ratios):")
print()

pair_set = {}
for err, n1, n2, prod, label, target in pair_hits:
    pair_set[(n1, n2)] = (label, err)
    pair_set[(n2, n1)] = (label, err)

loop_found = []
for b_name in edges:
    neighbors_b = edges[b_name]
    for i in range(len(neighbors_b)):
        a_name = neighbors_b[i][0]
        for j in range(i+1, len(neighbors_b)):
            c_name = neighbors_b[j][0]
            if (a_name, c_name) in pair_set:
                lab_ab = neighbors_b[i][1]
                err_ab = neighbors_b[i][2]
                lab_bc = neighbors_b[j][1]
                err_bc = neighbors_b[j][2]
                lab_ac, err_ac = pair_set[(a_name, c_name)]
                total = err_ab + err_bc + err_ac
                loop_found.append((total, a_name, b_name, c_name,
                                   lab_ab, lab_bc, lab_ac,
                                   err_ab, err_bc, err_ac))

loop_found.sort()
if loop_found:
    seen_loops = set()
    printed_loops = 0
    for item in loop_found:
        total, a, b, c = item[0], item[1], item[2], item[3]
        key = tuple(sorted([a, b, c]))
        if key in seen_loops: continue
        seen_loops.add(key)
        if printed_loops >= 15: break
        print("  LOOP: %s -- %s -- %s -- %s" % (a, b, c, a))
        print("    %s * %s ~ %s  (%.4f%%)" % (a, b, item[4], item[7]))
        print("    %s * %s ~ %s  (%.4f%%)" % (b, c, item[5], item[8]))
        print("    %s * %s ~ %s  (%.4f%%)" % (a, c, item[6], item[9]))
        print()
        printed_loops += 1
else:
    print("  No closed loops found.")
print()

# =====================================================================
# SECTION 9: EXTENDED PAIR SEARCH (broader F/L ratios, 0.05%)
# =====================================================================
print(SEP)
print("SECTION 9: PAIR PRODUCTS MATCHING BROADER F/L RATIOS (within 0.05%%)")
print(SEP)
print()

broad_hits = []
for i in range(N_entries):
    for j in range(i+1, N_entries):
        prod = D[i]["value"] * D[j]["value"]
        if prod <= 0 or prod > 100: continue
        matches = check_broad_fib(prod, tol_pct=0.05)
        if matches:
            best = matches[0]
            broad_hits.append((best[2], D[i]["name"], D[j]["name"],
                               prod, best[0], best[1]))

broad_hits.sort()
print("Found %d pair products matching ANY F/L ratio within 0.05%%:" % len(broad_hits))
print()

if broad_hits:
    shown = set()
    count = 0
    for err, n1, n2, prod, label, target in broad_hits:
        key = (min(n1,n2), max(n1,n2))
        if key in shown: continue
        shown.add(key)
        if count >= 50: break
        marker = " ***" if err < 0.005 else " **" if err < 0.02 else ""
        print("  %-14s * %-14s = %.10f ~ %s = %.10f  (%.6f%%)%s" % (
            n1, n2, prod, label, target, err, marker))
        count += 1
print()

# =====================================================================
# SECTION 10: SUMMARY
# =====================================================================
print(SEP)
print("SECTION 10: SUMMARY AND KEY RESULTS")
print(SEP)
print()

print("KEY FINDINGS:")
print()
print("1. L(n)*F(n) = F(2n) is the MASTER IDENTITY for golden products.")
print("   When cancellation leaves L(k)*F(k)/F(2k-1), we get F(2k)/F(2k-1) ~ phi.")
print("   This is PROVEN from Binet formulas.")
print()
print("2. Consecutive Fibonacci ratios F(n+1)/F(n) converge to phi as:")
print("   |F(n+1)/F(n) - phi| ~ 1/(sqrt(5)*F(n)^2) ~ phibar^(2n)/sqrt(5)")
print("   The approximation quality depends ONLY on n (the index),")
print("   not on which dictionary entries were multiplied.")
print()
print("3. K_lepton = 2/3 = F(3)/F(4) is simultaneously:")
print("   - The fractional charge quantum (exact)")
print("   - A consecutive Fibonacci ratio (n=3)")
print("   - The worst approximation to 1/phi in the Fibonacci sequence")
print("   This is the SIMPLEST golden closure.")
print()
print("4. GENERAL THEOREM: Products that algebraically reduce to F(n)/F(n+1)")
print("   AUTOMATICALLY approximate phi. The proof uses only:")
print("   (a) L(n)*F(n) = F(2n) -- for cancellation simplification")
print("   (b) L(a)*L(b) = L(a+b) + (-1)^b*L(a-b) -- for numerator products")
print("   (c) F(a)*F(b) = [F(a+b) + (-1)^(b+1)*F(a-b)] / sqrt(5) -- unused directly")
print("   (d) Binet formula -- for convergence rate")
print()
print("5. Structural pattern: entries whose denominators share Fibonacci factors")
print("   are the ones whose products cancel to leave clean F(n)/F(n+1).")
print("   The F(15)=610 denominator family is the richest source.")
print()

# Verification of all three known products
print("VERIFICATION OF THREE KNOWN PRODUCTS:")
print()

as_val = L(3)*L(8)/F(15)
mc_val = F(5)/L(3)
mb_val = F(8)/F(5)
prod1 = as_val * mc_val * mb_val
print("  1. alpha_s * m_c * m_b = %.15f" % prod1)
print("     F(16)/F(15)         = %.15f" % (F(16)/F(15)))
print("     phi                 = %.15f" % phi)
print("     Error from phi: %.7f%%" % (abs(prod1-phi)/phi*100))
print("     Algebraic: L(8)*F(8)/F(15) = F(16)/F(15) [by L(n)*F(n)=F(2n)]")
print()

gh_val = L(8)/F(12)
mtz_val = F(11)/L(8)
prod2 = gh_val * mtz_val
print("  2. g_half * m_t/m_Z = %.15f" % prod2)
print("     F(11)/F(12)      = %.15f" % (F(11)/F(12)))
print("     1/phi            = %.15f" % phibar)
print("     Error from 1/phi: %.7f%%" % (abs(prod2-phibar)/phibar*100))
print("     Algebraic: L(8) cancels, leaving F(11)/F(12)")
print()

kl_val = F(3)/F(4)
print("  3. K_lepton = F(3)/F(4) = %d/%d = %.15f" % (F(3), F(4), kl_val))
print("     1/phi               = %.15f" % phibar)
print("     Error from 1/phi:   %.4f%%" % (abs(kl_val-phibar)/phibar*100))
print("     (F(3)/F(4) = 2/3 is a poor approximation to 1/phi")
print("      but is EXACTLY the charge quantum)")
print()

print("STATISTICS:")
print("  Dictionary entries:             %d" % N_entries)
print("  Pair products ~ Fib ratio:      %d" % len(pair_hits))
print("  Triple products ~ Fib ratio:    %d" % len(triple_hits))
print("  Chains (length 2):              %d" % len(set(seen_chains)))
print("  Closed loops:                   %d" % len(loop_found))
print("  Broad F/L ratio matches:        %d" % len(broad_hits))
print()

print(SEP)
print("END OF GOLDEN CLOSURE ANALYSIS")
print(SEP)
