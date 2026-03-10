"""
budget_equations.py -- Exhaustive search for budget equations in the F/L dictionary
===================================================================================
Known budget: alpha_s + V_us + sin2_23 = 1  (188 + 89 + 333 = 610 = F(15))

Question: Are there OTHER such budgets?  Over other denominators?
"""

from math import sqrt, log, gcd
from itertools import combinations
from collections import defaultdict
from functools import reduce

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

fib_table = {F(n): n for n in range(0, 35)}
luc_table = {L(n): n for n in range(0, 35)}

def identify_FL(val):
    if not isinstance(val, int): return None
    if val in fib_table: return "F(%d)" % fib_table[val]
    if val in luc_table: return "L(%d)" % luc_table[val]
    for i in range(1, 20):
        for j in range(i, 20):
            if F(i) + F(j) == val: return "F(%d)+F(%d)" % (i, j)
            if L(i) + L(j) == val: return "L(%d)+L(%d)" % (i, j)
            if F(i) + L(j) == val: return "F(%d)+L(%d)" % (i, j)
            if L(i) + F(j) == val: return "L(%d)+F(%d)" % (i, j)
            if F(i) * F(j) == val: return "F(%d)*F(%d)" % (i, j)
            if L(i) * L(j) == val: return "L(%d)*L(%d)" % (i, j)
            if F(i) * L(j) == val: return "F(%d)*L(%d)" % (i, j)
    for i in range(1, 22):
        for j in range(1, 22):
            if i > j and L(i) - L(j) == val: return "L(%d)-L(%d)" % (i, j)
            if L(i) - F(j) == val and L(i) > F(j): return "L(%d)-F(%d)" % (i, j)
    return None

def entry(name, num, den, formula_str=""):
    return {
        "name": name, "num": num, "den": den,
        "value": num / den if den != 0 else 0,
        "formula": formula_str if formula_str else "%d/%d" % (num, den),
    }

def my_lcm(a, b): return a * b // gcd(a, b)

# =====================================================================
# THE COMPLETE F/L DICTIONARY
# =====================================================================

D = []

# --- F(15)=610 denominator family ---
D.append(entry("alpha_s",      L(3)*L(8),      F(15),  "L(3)*L(8)/F(15) = 188/610"))
D.append(entry("V_us",         F(11),           F(15),  "F(11)/F(15) = 89/610"))
D.append(entry("V_cb",         L(4)+L(6),       F(15),  "(L(4)+L(6))/F(15) = 25/610"))
D.append(entry("sin2_23",      L(5)+L(12),      F(15),  "(L(5)+L(12))/F(15) = 333/610"))
D.append(entry("m_t/m_H",      L(7)**2,         F(15),  "L(7)^2/F(15) = 841/610"))

# --- L(9)=76 denominator family ---
D.append(entry("V_ud",         L(9)-F(3),       L(9),   "(L(9)-F(3))/L(9) = 74/76"))
D.append(entry("1-V_ud",       F(3),            L(9),   "F(3)/L(9) = 2/76"))
D.append(entry("sin2_12",      L(9)-3*F(3),     3*L(9), "(L(9)-3*F(3))/(3*L(9)) = 70/228"))

# --- L(2)=3 denominator ---
D.append(entry("M_H",          F(14),           L(2),   "F(14)/L(2) = 377/3"))
D.append(entry("m_t",          L(13),           L(2),   "L(13)/L(2) = 521/3"))

# --- L(3)=4 denominator ---
D.append(entry("v",            F(16),           L(3),   "F(16)/L(3) = 987/4"))
D.append(entry("M_W",          L(12),           L(3),   "L(12)/L(3) = 322/4"))
D.append(entry("m_c",          F(5),            L(3),   "F(5)/L(3) = 5/4"))

# --- F(5)=5 denominator ---
D.append(entry("m_b",          F(8),            F(5),   "F(8)/F(5) = 21/5"))

# --- L(13)=521 denominator ---
D.append(entry("y_t",          L(5)*L(8),       L(13),  "L(5)*L(8)/L(13) = 517/521"))

# --- F(14)=377 denominator ---
D.append(entry("y_b",          L(2)**2,         F(14),  "L(2)^2/F(14) = 9/377"))

# --- L(15)=1364 denominator ---
D.append(entry("y_tau",        F(3)*L(4),       L(15),  "F(3)*L(4)/L(15) = 14/1364"))

# --- L(22)=39603 denominator ---
D.append(entry("y_mu",         L(2)*F(6),       L(22),  "L(2)*F(6)/L(22) = 24/39603"))

# --- L(19)=9349 denominator ---
D.append(entry("y_s",          F(5),            L(19),  "F(5)/L(19) = 5/9349"))
D.append(entry("V_tb",         L(19)-F(6),      L(19),  "(L(19)-F(6))/L(19) = 9341/9349"))

# --- F(25)=75025 denominator ---
D.append(entry("y_d",          F(3),            F(25),  "F(3)/F(25) = 2/75025"))

# --- CKM additional ---
D.append(entry("V_ub",         1,               L(7)+F(13), "1/(L(7)+F(13)) = 1/262"))
D.append(entry("V_cd",         L(7),            F(6)+L(10), "L(7)/(F(6)+L(10)) = 29/131"))
D.append(entry("V_cs",         F(4)+L(14)-L(5), F(4)+L(14), "835/846"))
D.append(entry("V_td",         1,               F(3)+L(10), "1/(F(3)+L(10)) = 1/125"))
D.append(entry("V_ts",         F(7),            F(7)+L(12), "F(7)/(F(7)+L(12)) = 13/335"))

# --- PMNS ---
D.append(entry("sin2_13",      L(5),            L(10)+F(14), "L(5)/(L(10)+F(14)) = 11/500"))

# --- Cosmological ---
D.append(entry("Omega_m",      L(7),            F(4)+F(11), "L(7)/(F(4)+F(11)) = 29/92"))
D.append(entry("Omega_L",      F(13),           L(6)+L(12), "F(13)/(L(6)+L(12)) = 233/340"))
D.append(entry("n_s",          F(10),           F(3)+F(10), "F(10)/(F(3)+F(10)) = 55/57"))
D.append(entry("sigma_8",      L(8),            L(5)+L(8),  "L(8)/(L(5)+L(8)) = 47/58"))
D.append(entry("Omega_b",      L(4)+L(11),      F(19),  "(L(4)+L(11))/F(19) = 206/4181"))
D.append(entry("Omega_c",      L(5)+F(11),      F(14),  "(L(5)+F(11))/F(14) = 100/377"))

# --- Other physics ---
D.append(entry("gamma_I",      F(3),            L(6),   "F(3)/L(6) = 2/18"))
D.append(entry("R_c",          F(5),            L(7),   "F(5)/L(7) = 5/29"))
D.append(entry("a_e",          L(2),            F(18),  "L(2)/F(18) = 3/2584"))
D.append(entry("alpha_2",      L(2),            F(11),  "L(2)/F(11) = 3/89"))
D.append(entry("g_half",       L(8),            F(12),  "L(8)/F(12) = 47/144"))

# --- Koide ---
D.append(entry("K_lepton",     2,               3,      "2/3"))
D.append(entry("K_up",         L(5),            F(7),   "L(5)/F(7) = 11/13"))
D.append(entry("K_down",       F(6),            L(5),   "F(6)/L(5) = 8/11"))

# --- Mass ratios ---
D.append(entry("m_H/m_Z",      L(5),            F(6),   "L(5)/F(6) = 11/8"))
D.append(entry("m_t/m_Z",      F(11),           L(8),   "F(11)/L(8) = 89/47"))

# --- Small masses ---
D.append(entry("m_mu",         F(7)*F(8),       F(18),  "F(7)*F(8)/F(18) = 273/2584"))
D.append(entry("m_u",          L(2)**2,         F(19),  "L(2)^2/F(19) = 9/4181"))

# --- Biological ---
D.append(entry("r_tensor",     L(6),            L(12),  "L(6)/L(12) = 18/322"))
D.append(entry("Chl_a",        L(3),            L(7),   "L(3)/L(7) = 4/29"))
D.append(entry("Chl_b",        1,               L(4),   "1/L(4) = 1/7"))
D.append(entry("retinal",      2,               L(5),   "2/L(5) = 2/11"))

# --- H0 proxy ---
D.append(entry("H0",           L(6)+L(13),      F(6),   "(L(6)+L(13))/F(6) = 539/8"))

# --- Pure framework ---
D.append(entry("1_3_const",    1,               3,      "1/3"))
D.append(entry("2_3_const",    2,               3,      "2/3"))

N = len(D)

print("=" * 80)
print("BUDGET EQUATIONS -- Exhaustive Search")
print("=" * 80)
print()
print("Dictionary: %d entries loaded" % N)
print()

# Show dictionary
print("-" * 80)
print("COMPLETE DICTIONARY (sorted by value)")
print("-" * 80)
sorted_D = sorted(D, key=lambda x: x["value"])
for i, e in enumerate(sorted_D):
    print("  %3d. %-14s = %12.8f  [%s]" % (i+1, e["name"], e["value"], e["formula"]))
print()

# =====================================================================
# PART 1: SUBSETS SUMMING TO 1 (size 3-5)
# =====================================================================
print("=" * 80)
print("PART 1: SUBSETS OF 3-5 QUANTITIES SUMMING TO 1 (within 0.01%)")
print("=" * 80)
print()

candidates = [e for e in D if 0 < e["value"] < 1.0]
print("Candidates (in (0,1)): %d quantities" % len(candidates))
print()

target_1 = 1.0
tol = 0.0001  # 0.01%

budget_results_1 = []

for size in [3, 4, 5]:
    for combo in combinations(range(len(candidates)), size):
        s = sum(candidates[i]["value"] for i in combo)
        if abs(s - target_1) / target_1 < tol:
            names = [candidates[i]["name"] for i in combo]
            vals = [candidates[i]["value"] for i in combo]
            err = abs(s - target_1) / target_1 * 100
            budget_results_1.append((err, size, names, vals, s))

budget_results_1.sort()
print("Found %d budget equations summing to 1:" % len(budget_results_1))
print()

for rank, (err, size, names, vals, s) in enumerate(budget_results_1[:40]):
    name_str = " + ".join(names)
    val_str = " + ".join(["%.6f" % v for v in vals])
    marker = " *** EXACT" if err < 0.001 else " **" if err < 0.005 else ""
    print("  [%d] %s" % (rank+1, name_str))
    print("      = %s = %.8f  (err=%.6f%%)%s" % (val_str, s, err, marker))

    # Gather entries
    entries = []
    for n in names:
        for e in candidates:
            if e["name"] == n:
                entries.append(e)
                break

    dens = [e["den"] for e in entries]
    if len(set(dens)) == 1:
        num_sum = sum(e["num"] for e in entries)
        den_common = dens[0]
        fl_id = identify_FL(num_sum)
        fl_den = identify_FL(den_common)
        print("      Common denom %d%s, numerator sum = %d%s" %
              (den_common, (" = " + fl_den if fl_den else ""),
               num_sum, (" = " + fl_id if fl_id else "")))
        if num_sum == den_common:
            print("      *** EXACT PARTITION: numerator sum = denominator ***")
    else:
        all_dens = [e["den"] for e in entries]
        try:
            common = reduce(my_lcm, all_dens)
            nums_scaled = [e["num"] * (common // e["den"]) for e in entries]
            total_num = sum(nums_scaled)
            fl_total = identify_FL(total_num)
            fl_common = identify_FL(common)
            print("      LCM denom: %d%s, scaled num sum: %d%s" %
                  (common, (" = " + fl_common if fl_common else ""),
                   total_num, (" = " + fl_total if fl_total else "")))
            if total_num == common:
                print("      *** EXACT PARTITION over LCM denominator ***")
        except Exception:
            pass
    print()

# =====================================================================
# PART 2: SUBSETS SUMMING TO OTHER SPECIAL VALUES
# =====================================================================
print("=" * 80)
print("PART 2: SUBSETS OF 2-4 QUANTITIES SUMMING TO SPECIAL VALUES")
print("=" * 80)
print()

special_targets = {}
for label, val in [("phi", phi), ("1/phi", phibar), ("2", 2.0),
                    ("1/2", 0.5), ("2/3", 2.0/3), ("1/3", 1.0/3)]:
    special_targets[label] = val

for n in range(2, 14):
    for m in range(2, 14):
        val_fl = F(n) / L(m) if L(m) != 0 else 0
        val_lf = L(n) / F(m) if F(m) != 0 else 0
        if 0.05 < val_fl < 5.0:
            label = "F(%d)/L(%d)=%d/%d" % (n, m, F(n), L(m))
            special_targets[label] = val_fl
        if 0.05 < val_lf < 5.0:
            label = "L(%d)/F(%d)=%d/%d" % (n, m, L(n), F(m))
            special_targets[label] = val_lf

for n in range(2, 14):
    for m in range(n+1, 14):
        if F(m) != 0:
            val = F(n) / F(m)
            if 0.05 < val < 5.0:
                special_targets["F(%d)/F(%d)=%d/%d" % (n, m, F(n), F(m))] = val
        if L(m) != 0:
            val = L(n) / L(m)
            if 0.05 < val < 5.0:
                special_targets["L(%d)/L(%d)=%d/%d" % (n, m, L(n), L(m))] = val

all_pos = [e for e in D if e["value"] > 0]
budget_results_2 = []

for tname, tval in special_targets.items():
    if tval <= 0: continue
    for size in [2, 3, 4]:
        for combo in combinations(range(len(all_pos)), size):
            s = sum(all_pos[i]["value"] for i in combo)
            if abs(s - tval) / tval < tol:
                names = [all_pos[i]["name"] for i in combo]
                err = abs(s - tval) / tval * 100
                budget_results_2.append((err, tname, tval, size, names, s))

budget_results_2.sort()
seen_sets = set()
unique_results_2 = []
for item in budget_results_2:
    key = (frozenset(item[4]), item[1])
    if key not in seen_sets:
        seen_sets.add(key)
        unique_results_2.append(item)

print("Found %d budget equations to special values (showing top 60):" % len(unique_results_2))
print()
shown = 0
for rank, (err, tname, tval, size, names, s) in enumerate(unique_results_2):
    if shown >= 60: break
    name_str = " + ".join(names)
    marker = " *** EXACT" if err < 0.001 else " **" if err < 0.005 else ""
    print("  [%d] %s = %s  (target %.8f)" % (rank+1, name_str, tname, tval))
    print("      sum = %.8f, err = %.6f%%%s" % (s, err, marker))
    entries = [e for e in all_pos if e["name"] in names]
    dens = [e["den"] for e in entries]
    if len(set(dens)) == 1 and len(dens) == len(names):
        num_sum = sum(e["num"] for e in entries)
        fl_id = identify_FL(num_sum)
        if fl_id:
            print("      Numerator sum %d = %s (common denom %d)" % (num_sum, fl_id, dens[0]))
    print()
    shown += 1

# =====================================================================
# PART 3: COMMON-DENOMINATOR PARTITIONS
# =====================================================================
print("=" * 80)
print("PART 3: COMMON-DENOMINATOR PARTITIONS")
print("=" * 80)
print()

denom_groups = defaultdict(list)
for e in D:
    if e["den"] is not None and e["den"] > 1:
        denom_groups[e["den"]].append(e)

for den in sorted(denom_groups.keys()):
    group = denom_groups[den]
    if len(group) < 2: continue
    fl_den = identify_FL(den)
    den_label = " = %s" % fl_den if fl_den else ""
    print("-" * 70)
    print("DENOMINATOR %d%s  (%d quantities)" % (den, den_label, len(group)))
    print("-" * 70)
    for e in group:
        fl_num = identify_FL(e["num"])
        num_label = " = %s" % fl_num if fl_num else ""
        print("  %-14s  %5d/%d  = %.8f   [num%s]" % (e["name"], e["num"], den, e["value"], num_label))

    print()
    print("  Subset sums of numerators:")
    found_any = False
    for size in range(2, min(len(group)+1, 7)):
        for combo in combinations(range(len(group)), size):
            num_sum = sum(group[i]["num"] for i in combo)
            fl_id = identify_FL(num_sum)
            names = [group[i]["name"] for i in combo]
            ratio = num_sum / den
            specials_hit = []
            if abs(ratio - 1.0) < 0.0002: specials_hit.append("= 1!")
            if abs(ratio - phi) < 0.002: specials_hit.append("~ phi")
            if abs(ratio - phibar) < 0.002: specials_hit.append("~ 1/phi")
            if abs(ratio - 0.5) < 0.002: specials_hit.append("~ 1/2")
            if abs(ratio - 2.0/3) < 0.002: specials_hit.append("~ 2/3")
            if abs(ratio - 1.0/3) < 0.002: specials_hit.append("~ 1/3")
            if num_sum == den: specials_hit.append("PARTITION OF 1")
            if fl_id or specials_hit:
                found_any = True
                name_str = " + ".join(names)
                spec_str = "  ".join(specials_hit) if specials_hit else ""
                print("    %s: sum = %d" % (name_str, num_sum), end="")
                if fl_id: print(" = %s" % fl_id, end="")
                if spec_str: print("  [%s]" % spec_str, end="")
                print("  (ratio = %.6f)" % ratio)
    if not found_any:
        print("    (no F/L numerator sums or special ratios found)")
    print()

# =====================================================================
# PART 4: F(15)=610 DEEP DIVE
# =====================================================================
print("=" * 80)
print("PART 4: F(15)=610 DEEP DIVE")
print("=" * 80)
print()

f15 = {"alpha_s": 188, "V_us": 89, "V_cb": 25, "sin2_23": 333, "m_t/m_H": 841}
print("Quantities over F(15)=610:")
for name, num in f15.items():
    fl_id = identify_FL(num) or "?"
    print("  %-12s = %4d/610  (%.4f)  num = %s" % (name, num, num/610, fl_id))

print()
print("All partitions of 610:")
items = list(f15.items())
for size in range(2, len(items)+1):
    for combo in combinations(range(len(items)), size):
        s = sum(items[i][1] for i in combo)
        if s == 610:
            names = [items[i][0] for i in combo]
            nums = [items[i][1] for i in combo]
            print("  %s = %s = 610 = F(15)" % (" + ".join(names), " + ".join(str(n) for n in nums)))

print()
print("Pairwise numerator sums that are F/L:")
for i in range(len(items)):
    for j in range(i+1, len(items)):
        s = items[i][1] + items[j][1]
        fl_id = identify_FL(s)
        if fl_id:
            print("  %s + %s = %d + %d = %d = %s" % (items[i][0], items[j][0], items[i][1], items[j][1], s, fl_id))

print()
print("Triple numerator sums that are F/L:")
for combo in combinations(range(len(items)), 3):
    s = sum(items[i][1] for i in combo)
    fl_id = identify_FL(s)
    if fl_id:
        names = [items[i][0] for i in combo]
        nums = [items[i][1] for i in combo]
        print("  %s = %s = %d = %s" % (" + ".join(names), " + ".join(str(n) for n in nums), s, fl_id))
print()

# =====================================================================
# PART 5: ANTI-BUDGETS (products = special values)
# =====================================================================
print("=" * 80)
print("PART 5: ANTI-BUDGETS -- Pairs whose PRODUCT hits special values")
print("=" * 80)
print()

print("--- Pairs with product ~ 1 (within 1%) ---")
anti_budgets = []
for i in range(len(D)):
    for j in range(i+1, len(D)):
        if D[i]["value"] > 0 and D[j]["value"] > 0:
            p = D[i]["value"] * D[j]["value"]
            if abs(p - 1.0) < 0.01:
                err = abs(p - 1.0) * 100
                anti_budgets.append((err, D[i]["name"], D[j]["name"], D[i]["value"], D[j]["value"], p))

anti_budgets.sort()
if anti_budgets:
    for err, n1, n2, v1, v2, p in anti_budgets:
        marker = " *** EXACT" if err < 0.1 else ""
        print("  %-14s * %-14s = %.6f * %.6f = %.8f  (err=%.4f%%)%s" % (n1, n2, v1, v2, p, err, marker))
        e1 = next(e for e in D if e["name"] == n1)
        e2 = next(e for e in D if e["name"] == n2)
        prod_num = e1["num"] * e2["num"]
        prod_den = e1["den"] * e2["den"]
        fl_num = identify_FL(prod_num)
        fl_den = identify_FL(prod_den)
        print("    Algebraic: (%d*%d)/(%d*%d) = %d/%d" % (e1["num"], e2["num"], e1["den"], e2["den"], prod_num, prod_den))
        if fl_num: print("    Numerator %d = %s" % (prod_num, fl_num))
        if fl_den: print("    Denominator %d = %s" % (prod_den, fl_den))
else:
    print("  (none found)")

print()
print("--- Pairs with product ~ phi or 1/phi (within 0.5%) ---")
phi_prods = []
for i in range(len(D)):
    for j in range(i+1, len(D)):
        if D[i]["value"] > 0 and D[j]["value"] > 0:
            p = D[i]["value"] * D[j]["value"]
            for tname, tval in [("phi", phi), ("1/phi", phibar)]:
                if abs(p - tval) / tval < 0.005:
                    err = abs(p - tval) / tval * 100
                    phi_prods.append((err, D[i]["name"], D[j]["name"], p, tname, tval))

phi_prods.sort()
for err, n1, n2, p, tname, tval in phi_prods[:15]:
    print("  %-14s * %-14s = %.8f ~ %s (%.8f), err=%.4f%%" % (n1, n2, p, tname, tval, err))

print()
print("--- Pairs with product ~ 2/3, 1/3, or 1/2 (within 0.5%) ---")
frac_prods = []
for i in range(len(D)):
    for j in range(i+1, len(D)):
        if D[i]["value"] > 0 and D[j]["value"] > 0:
            p = D[i]["value"] * D[j]["value"]
            for tname, tval in [("2/3", 2.0/3), ("1/3", 1.0/3), ("1/2", 0.5)]:
                if abs(p - tval) / tval < 0.005:
                    err = abs(p - tval) / tval * 100
                    frac_prods.append((err, D[i]["name"], D[j]["name"], p, tname, tval))

frac_prods.sort()
for err, n1, n2, p, tname, tval in frac_prods[:15]:
    print("  %-14s * %-14s = %.8f ~ %s (%.8f), err=%.4f%%" % (n1, n2, p, tname, tval, err))
print()

# =====================================================================
# PART 6: TRIPLE PRODUCTS = SPECIAL VALUES
# =====================================================================
print("=" * 80)
print("PART 6: TRIPLE PRODUCTS = SPECIAL VALUES")
print("=" * 80)
print()

small_D = [e for e in D if 0 < e["value"] < 10]
prod_targets = {"1": 1.0, "phi": phi, "1/phi": phibar, "2": 2.0,
                "1/2": 0.5, "1/3": 1.0/3, "2/3": 2.0/3}

triple_prods = []
for combo in combinations(range(len(small_D)), 3):
    p = 1.0
    for i in combo: p *= small_D[i]["value"]
    for tname, tval in prod_targets.items():
        if tval > 0 and abs(p - tval) / tval < 0.005:
            names = [small_D[i]["name"] for i in combo]
            err = abs(p - tval) / tval * 100
            triple_prods.append((err, tname, names, p, tval))

triple_prods.sort()
print("Triple products hitting special values (top 30):")
for rank, (err, tname, names, p, tval) in enumerate(triple_prods[:30]):
    marker = " ***" if err < 0.05 else " **" if err < 0.5 else ""
    print("  [%d] %s = %.8f ~ %s (%.8f), err=%.4f%%%s" % (rank+1, " * ".join(names), p, tname, tval, err, marker))
print()

# =====================================================================
# PART 7: MASS DIFFERENCES / SUMS
# =====================================================================
print("=" * 80)
print("PART 7: MASS DIFFERENCES / SUMS")
print("=" * 80)
print()

print("--- Over L(2)=3 denominator ---")
print()
print("m_t = L(13)/L(2) = 521/3 = %.4f GeV" % (521/3))
print("M_H = F(14)/L(2) = 377/3 = %.4f GeV" % (377/3))
print()
diff = 521 - 377
fl_diff = identify_FL(diff)
print("m_t - M_H = (L(13) - F(14))/L(2) = %d/3 = %.4f GeV" % (diff, diff/3))
print("  %d = %s" % (diff, fl_diff if fl_diff else "not F/L"))
print()
print("IDENTITY: L(n) - F(n+1) = F(n-1)")
print("  L(13) - F(14) = F(12) = 144. CHECK: %d = %d  [%s]" % (L(13)-F(14), F(12), "OK" if L(13)-F(14)==F(12) else "FAIL"))
print()

sm = 521 + 377
fl_sm = identify_FL(sm)
print("m_t + M_H = (L(13) + F(14))/L(2) = %d/3 = %.4f GeV" % (sm, sm/3))
if fl_sm:
    print("  %d = %s" % (sm, fl_sm))
else:
    print("  %d is not a simple F/L number" % sm)
    print("  L(n) + F(n+1) = F(n-1) + 2*F(n+1) = F(12) + 2*F(14) = 144 + 754 = 898")
print()

print("--- Over L(3)=4 denominator ---")
print()
diff2 = 987 - 322
fl_diff2 = identify_FL(diff2)
print("v - M_W = (F(16) - L(12))/L(3) = %d/4 = %.4f GeV" % (diff2, diff2/4))
print("  %d = %s" % (diff2, fl_diff2 if fl_diff2 else "not F/L (665 = 5*7*19 = F(5)*L(4)*19)"))
print()
diff3 = 987 - 5
fl_diff3 = identify_FL(diff3)
print("v - m_c = (F(16) - F(5))/L(3) = %d/4 = %.4f GeV" % (diff3, diff3/4))
print("  %d = %s" % (diff3, fl_diff3 if fl_diff3 else "not F/L"))
print()
sm2 = 322 + 5
fl_sm2 = identify_FL(sm2)
print("M_W + m_c = (L(12) + F(5))/L(3) = %d/4 = %.4f GeV" % (sm2, sm2/4))
print("  %d = %s" % (sm2, fl_sm2 if fl_sm2 else "not F/L"))
print()

# =====================================================================
# PART 8: CKM UNITARITY
# =====================================================================
print("=" * 80)
print("PART 8: CKM UNITARITY (rows/columns sum |V|^2 = 1)")
print("=" * 80)
print()

V_ud_v = (L(9) - F(3)) / L(9)
V_us_v = F(11) / F(15)
V_ub_v = 1 / (L(7) + F(13))
V_cd_v = L(7) / (F(6) + L(10))
V_cs_v = (F(4) + L(14) - L(5)) / (F(4) + L(14))
V_cb_v = (L(4) + L(6)) / F(15)
V_td_v = 1 / (F(3) + L(10))
V_ts_v = F(7) / (F(7) + L(12))
V_tb_v = (L(19) - F(6)) / L(19)

rows = [
    ("Row 1", [("V_ud", V_ud_v), ("V_us", V_us_v), ("V_ub", V_ub_v)]),
    ("Row 2", [("V_cd", V_cd_v), ("V_cs", V_cs_v), ("V_cb", V_cb_v)]),
    ("Row 3", [("V_td", V_td_v), ("V_ts", V_ts_v), ("V_tb", V_tb_v)]),
]
for rname, elems in rows:
    sq_sum = sum(v**2 for _, v in elems)
    print("  %s: |%s|^2 + |%s|^2 + |%s|^2 = %.8f  (err: %.4f%%)" % (rname, elems[0][0], elems[1][0], elems[2][0], sq_sum, abs(sq_sum-1)*100))
print()

cols = [
    ("Col 1", [("V_ud", V_ud_v), ("V_cd", V_cd_v), ("V_td", V_td_v)]),
    ("Col 2", [("V_us", V_us_v), ("V_cs", V_cs_v), ("V_ts", V_ts_v)]),
    ("Col 3", [("V_ub", V_ub_v), ("V_cb", V_cb_v), ("V_tb", V_tb_v)]),
]
for cname, elems in cols:
    sq_sum = sum(v**2 for _, v in elems)
    print("  %s: |%s|^2 + |%s|^2 + |%s|^2 = %.8f  (err: %.4f%%)" % (cname, elems[0][0], elems[1][0], elems[2][0], sq_sum, abs(sq_sum-1)*100))
print()

# =====================================================================
# PART 9: ALGEBRAIC PROOF OF THE F(15) BUDGET
# =====================================================================
print("=" * 80)
print("PART 9: ALGEBRAIC PROOF OF THE F(15) BUDGET")
print("=" * 80)
print()

print("THEOREM: alpha_s + V_us + sin2_23 = 1")
print()
print("PROOF:")
print("  alpha_s = L(3)*L(8)/F(15) = 188/610")
print("  V_us    = F(11)/F(15)      = 89/610")
print("  sin2_23 = (L(5)+L(12))/F(15) = 333/610")
print()
print("  Step 1: L(3)*L(8) = L(11) - L(5)  [Lucas product identity]")
print("    L(m)*L(n) = L(m+n) + (-1)^n * L(m-n)")
print("    L(3)*L(8) = L(11) + (-1)^8 * L(-5) = L(11) + L(-5)")
print("    L(-5) = (-1)^5 * L(5) = -L(5)")
print("    Therefore: L(3)*L(8) = L(11) - L(5) = 199 - 11 = 188. CHECK.")
print()
print("  Step 2: alpha_s + sin2_23 = [L(11)-L(5) + L(5)+L(12)] / F(15)")
print("    = [L(11) + L(12)] / F(15)")
print("    = L(13) / F(15)   [Lucas recurrence: L(n)+L(n+1)=L(n+2)]")
print("    = 521/610")
print()
print("  Step 3: alpha_s + V_us + sin2_23 = [L(13) + F(11)] / F(15)")
print()
print("  Key identity: L(n) + F(n-2) = F(n+2)")
print("    Proof: L(n) = F(n-1) + F(n+1)")
print("    L(n) + F(n-2) = F(n-1) + F(n+1) + F(n-2)")
print("                  = [F(n-2) + F(n-1)] + F(n+1)")
print("                  = F(n) + F(n+1)")
print("                  = F(n+2). QED.")
print()
print("  With n=13: L(13) + F(11) = F(15) = 610")
print()
print("  Therefore: alpha_s + V_us + sin2_23 = F(15)/F(15) = 1. QED.")
print()
print("  THREE IDENTITIES USED:")
print("    (a) Lucas product: L(a)*L(b) = L(a+b) + (-1)^b * L(a-b)")
print("    (b) Lucas recurrence: L(n) + L(n+1) = L(n+2)")
print("    (c) Cross identity: L(n) + F(n-2) = F(n+2)")
print()

# =====================================================================
# PART 10: SUMMARY AND VERIFICATION
# =====================================================================
print("=" * 80)
print("PART 10: SUMMARY")
print("=" * 80)
print()

print("CONFIRMED EXACT BUDGETS (algebraically proven):")
print()
print("  1. alpha_s + V_us + sin2_23 = 1  [THE F(15) PARTITION]")
print("     188 + 89 + 333 = 610 = F(15)")
print()
print("  2. alpha_s + sin2_23 = L(13)/F(15) = 521/610")
print("     = m_t numerator / universal normalizer")
print()
print("  3. m_t - M_H = F(12)/L(2) = 144/3 = 48 GeV")
print("     From L(n) - F(n+1) = F(n-1)")
print()
print("  4. V_ud - sin2_12 = 2/3 exactly (the charge quantum)")
print()
print("  5. CKM unitarity: rows/columns sum |V|^2 ~ 1")
print()

print("=" * 80)
print("NUMERICAL VERIFICATION")
print("=" * 80)
print()

checks = [
    ("alpha_s + V_us + sin2_23",         188/610 + 89/610 + 333/610,    1.0),
    ("alpha_s + sin2_23 = L(13)/F(15)",  188/610 + 333/610,             521/610),
    ("L(13) + F(11) = F(15)",            521 + 89,                      610),
    ("L(3)*L(8) = L(11)-L(5)",           4*47,                          199-11),
    ("m_t - M_H numerator = F(12)",      521 - 377,                     144),
    ("F(12) check",                      F(12),                         144),
    ("V_ud - sin2_12 = 2/3",            (74/76) - (70/228),            2/3),
    ("L(13)+F(11)=F(15) check",         L(13) + F(11),                 F(15)),
    ("L(11)+L(12)=L(13) check",         L(11) + L(12),                 L(13)),
]

for label, computed, expected in checks:
    if expected != 0:
        err = abs(computed - expected) / abs(expected)
    else:
        err = abs(computed - expected)
    match = "OK" if err < 1e-10 else "APPROX (%.2e)" % err
    print("  %-38s: %.8f = %.8f  [%s]" % (label, computed, expected, match))

print()
print("Done.")
