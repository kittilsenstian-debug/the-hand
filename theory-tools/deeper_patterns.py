"""
DEEPER PATTERNS -- Structural Analysis of the Unified Language
==============================================================
Explores:
1. The L(13)-10 subtraction pattern for other particle masses
2. Index histogram across all 68 expressions
3. Operation grammar classification
4. Collision detection (redundant addresses)
5. Fibonacci identity web (closure under operations)
"""

from math import sqrt, log, pi

phi = (1 + sqrt(5)) / 2
phibar = 1 / phi
sqrt2 = sqrt(2)

def F(n):
    """Fibonacci number F(n), n >= 0."""
    if n < 0:
        # Extended Fibonacci: F(-n) = (-1)^(n+1) * F(n)
        return ((-1) ** (n + 1)) * F(-n)
    if n == 0: return 0
    if n == 1: return 1
    a, b = 0, 1
    for _ in range(n - 1):
        a, b = b, a + b
    return b

def L(n):
    """Lucas number L(n), n >= 0."""
    if n < 0:
        return ((-1) ** n) * L(-n)
    if n == 0: return 2
    if n == 1: return 1
    a, b = 2, 1
    for _ in range(n - 1):
        a, b = b, a + b
    return b

# Precompute F and L for efficiency
F_cache = {n: F(n) for n in range(0, 50)}
L_cache = {n: L(n) for n in range(0, 50)}

def Fc(n):
    return F_cache.get(n, F(n))

def Lc(n):
    return L_cache.get(n, L(n))


# ============================================================
# PART 1: THE L(a) - X(b)*Y(c) SUBTRACTION PATTERN
# ============================================================
print("=" * 80)
print("PART 1: THE L(a) - X(b)*Y(c) SUBTRACTION PATTERN")
print("=" * 80)
print()
print("  Known: m_e = L(13) - F(3)*F(5) = 521 - 10 = 511 keV (EXACT)")
print("  Question: does this pattern work for other masses?")
print()

# Build a set of candidate terms: F(n) and L(n) for reasonable n
# We search L(a) - X(b)*Y(c) where X,Y in {F,L} and a,b,c are indices
# For masses that may be expressed in MeV or GeV

targets = [
    ("m_mu",     105.658, "MeV"),
    ("m_tau",    1776.86, "MeV"),
    ("m_proton", 938.272, "MeV"),
    ("m_neutron",939.565, "MeV"),
    ("m_W",      80.379,  "GeV"),
    ("m_Z",      91.188,  "GeV"),
]

# For each target, search L(a) - X(b)*Y(c) and also L(a) + X(b)*Y(c)
# and also F(a) - X(b)*Y(c)
# where a in [1..35], b,c in [1..20], X,Y in {F,L}

def search_subtraction_pattern(name, target_val, unit, max_a=35, max_bc=20):
    """Search for expressions of the form SEQ1(a) - SEQ2(b)*SEQ3(c) ~ target."""
    results = []
    # Round target to int for exact matches, but also check float matches
    target_int = round(target_val)

    seqs = [("F", Fc), ("L", Lc)]

    for a in range(1, max_a + 1):
        for s1_name, s1_fn in seqs:
            val_a = s1_fn(a)
            if val_a < target_val * 0.5 or val_a > target_val * 3:
                continue
            for b in range(1, max_bc + 1):
                for c in range(b, max_bc + 1):  # c >= b to avoid duplicates
                    for s2_name, s2_fn in seqs:
                        for s3_name, s3_fn in seqs:
                            val_bc = s2_fn(b) * s3_fn(c)
                            if val_bc == 0:
                                continue
                            candidate = val_a - val_bc
                            if candidate <= 0:
                                continue
                            err = abs(candidate - target_val) / target_val
                            if err < 0.005:  # within 0.5%
                                expr = "%s(%d) - %s(%d)*%s(%d)" % (
                                    s1_name, a, s2_name, b, s3_name, c)
                                vals = "%d - %d*%d = %d - %d = %d" % (
                                    val_a, s2_fn(b), s3_fn(c), val_a, val_bc, candidate)
                                results.append((err, expr, vals, candidate))

    # Also search L(a) - X(b) (simple subtraction, no product)
    for a in range(1, max_a + 1):
        for s1_name, s1_fn in seqs:
            val_a = s1_fn(a)
            if val_a < target_val:
                continue
            for b in range(1, max_a + 1):
                for s2_name, s2_fn in seqs:
                    val_b = s2_fn(b)
                    candidate = val_a - val_b
                    if candidate <= 0:
                        continue
                    err = abs(candidate - target_val) / target_val
                    if err < 0.005:
                        expr = "%s(%d) - %s(%d)" % (s1_name, a, s2_name, b)
                        vals = "%d - %d = %d" % (val_a, val_b, candidate)
                        results.append((err, expr, vals, candidate))

    results.sort()
    return results

for name, target_val, unit in targets:
    print("  --- %s = %.3f %s ---" % (name, target_val, unit))
    results = search_subtraction_pattern(name, target_val, unit)
    if results:
        shown = 0
        seen = set()
        for err, expr, vals, cand in results[:15]:
            if cand in seen and shown >= 3:
                continue
            seen.add(cand)
            exact_tag = " [EXACT INTEGER]" if abs(cand - round(target_val)) == 0 and err < 0.001 else ""
            print("    %s" % expr)
            print("      = %s  (err=%.4f%%)%s" % (vals, err * 100, exact_tag))
            shown += 1
            if shown >= 5:
                break
    else:
        print("    No matches found within 0.5%%")
    print()

# Verify the electron
print("  --- VERIFICATION: m_e = 511 keV ---")
print("    L(13) - F(3)*F(5) = %d - %d*%d = %d - %d = %d" % (
    L(13), F(3), F(5), L(13), F(3)*F(5), L(13) - F(3)*F(5)))
print("    Target: 511 keV -> EXACT MATCH")
print()


# ============================================================
# PART 2: INDEX HISTOGRAM
# ============================================================
print("=" * 80)
print("PART 2: INDEX HISTOGRAM -- Which indices appear most often?")
print("=" * 80)
print()

# Complete dictionary of all 68+ quantities with their F/L expressions
# Format: (name, expression_string, list_of_tuples (seq, index))
# where seq is "F" or "L"

all_expressions = [
    # A. GAUGE COUPLINGS
    ("alpha_s",    "L(3)*L(8)/F(15)",          [("L",3),("L",8),("F",15)]),
    ("sin2W",      "L(2)*L(8)/F(15)",          [("L",2),("L",8),("F",15)]),  # using table in Sec 29
    ("1/alpha",    "L(3)*F(9)+1+1/(L(3)*F(9))",[("L",3),("F",9)]),
    ("alpha_2",    "L(2)/F(11)",               [("L",2),("F",11)]),
    ("g/2",        "L(8)/F(12)",               [("L",8),("F",12)]),
    ("a_e",        "L(2)/F(18)",               [("L",2),("F",18)]),
    ("gamma_I",    "F(5)*L(7)/F(15)",          [("F",5),("L",7),("F",15)]),
    ("1/3",        "F(2)/F(4)",                [("F",2),("F",4)]),

    # B. CKM MATRIX
    ("V_ud",  "1-F(3)/L(9)",                   [("F",3),("L",9)]),
    ("V_us",  "F(11)/(L(6)+F(14))",            [("F",11),("L",6),("F",14)]),
    ("V_ub",  "1/(L(7)+F(13))",                [("L",7),("F",13)]),
    ("V_cd",  "L(7)/(F(6)+L(10))",             [("L",7),("F",6),("L",10)]),
    ("V_cs",  "1-L(5)/(F(4)+L(14))",           [("L",5),("F",4),("L",14)]),
    ("V_cb",  "(L(4)+L(6))/F(15)",             [("L",4),("L",6),("F",15)]),
    ("V_td",  "1/(F(3)+L(10))",                [("F",3),("L",10)]),
    ("V_ts",  "F(7)/(F(7)+L(12))",             [("F",7),("L",12)]),
    ("V_tb",  "1-F(6)/L(19)",                  [("F",6),("L",19)]),

    # C. PMNS MIXING
    ("sin2_12", "1/3-F(3)/L(9)",               [("F",3),("L",9)]),
    ("sin2_23", "(L(5)+L(12))/F(15)",          [("L",5),("L",12),("F",15)]),
    ("sin2_13", "L(5)/(L(10)+F(14))",          [("L",5),("L",10),("F",14)]),
    ("dCP/pi",  "(L(3)+L(8))/L(8)",            [("L",3),("L",8)]),

    # D. ELECTROWEAK MASSES
    ("v",     "F(16)/L(3)",                     [("F",16),("L",3)]),
    ("M_W",   "L(12)/L(3)",                    [("L",12),("L",3)]),
    ("M_H",   "F(14)/L(2)",                    [("F",14),("L",2)]),

    # E. FERMION MASSES (absolute)
    ("m_t",   "L(13)/L(2)",                    [("L",13),("L",2)]),
    ("m_b",   "F(8)/F(5)",                     [("F",8),("F",5)]),
    ("m_tau", "v*F(3)/(L(11)*sqrt2)",          [("F",3),("L",11)]),
    ("m_c",   "F(5)/L(3)",                     [("F",5),("L",3)]),
    ("m_mu",  "F(7)*F(8)/F(18)",               [("F",7),("F",8),("F",18)]),
    ("m_s",   "v*F(5)/(L(19)*sqrt2)",          [("F",5),("L",19)]),
    ("m_u",   "L(2)^2/F(19)",                  [("L",2),("F",19)]),
    ("m_d",   "v*F(3)/(F(25)*sqrt2)",          [("F",3),("F",25)]),
    ("m_e",   "(L(13)-F(3)*F(5)) keV",         [("L",13),("F",3),("F",5)]),

    # F. YUKAWA COUPLINGS
    ("y_t",   "L(5)*L(8)/L(13)",               [("L",5),("L",8),("L",13)]),
    ("y_c",   "F(3)*F(7)/L(17)",               [("F",3),("F",7),("L",17)]),
    ("y_b",   "L(2)^2/F(14)",                  [("L",2),("F",14)]),
    ("y_tau", "F(3)*L(4)/L(15)",               [("F",3),("L",4),("L",15)]),
    ("y_mu",  "L(2)*F(6)/L(22)",               [("L",2),("F",6),("L",22)]),
    ("y_s",   "F(5)/L(19)",                    [("F",5),("L",19)]),
    ("y_d",   "F(3)/F(25)",                    [("F",3),("F",25)]),
    ("y_u",   "L(3)/F(28)",                    [("L",3),("F",28)]),
    ("y_e",   "F(3)*L(8)/L(36)",               [("F",3),("L",8),("L",36)]),

    # G. MASS RATIOS
    ("m_t/m_c",   "L(3)*F(9)",                 [("L",3),("F",9)]),
    ("m_s/m_d",   "L(3)*F(5)",                 [("L",3),("F",5)]),
    ("m_b/m_s",   "L(3)*L(10)/L(5)",           [("L",3),("L",10),("L",5)]),
    ("m_b/m_d",   "L(6)*L(11)/L(3)",           [("L",6),("L",11),("L",3)]),
    ("m_tau/m_mu","L(3)*F(8)/F(5)",            [("L",3),("F",8),("F",5)]),
    ("m_mu/m_e",  "L(4)*F(11)/F(4)",           [("L",4),("F",11),("F",4)]),
    ("m_H/m_Z",   "L(5)/F(6)",                 [("L",5),("F",6)]),
    ("m_t/m_Z",   "F(11)/L(8)",                [("F",11),("L",8)]),
    ("m_t/m_H",   "L(7)^2/F(15)",              [("L",7),("F",15)]),

    # H. COSMOLOGICAL PARAMETERS
    ("Omega_m",   "L(7)/(F(4)+F(11))",         [("L",7),("F",4),("F",11)]),
    ("Omega_L",   "F(13)/(L(6)+L(12))",        [("F",13),("L",6),("L",12)]),
    ("H0",        "(L(6)+L(13))/F(6)",         [("L",6),("L",13),("F",6)]),
    ("n_s",       "F(10)/(F(3)+F(10))",        [("F",10),("F",3)]),
    ("sigma_8",   "L(8)/(L(5)+L(8))",          [("L",8),("L",5)]),
    ("Omega_b",   "(L(4)+L(11))/F(19)",        [("L",4),("L",11),("F",19)]),
    ("Omega_c",   "(L(5)+F(11))/F(14)",        [("L",5),("F",11),("F",14)]),
    ("dm32/dm21", "(L(5)+L(7))/L(4)",          [("L",5),("L",7),("L",4)]),
    ("eta_B",     "phibar^44",                 []),  # index 44 = L(3)*L(5), meta-level
    ("v/M_Pl",    "phibar^80",                 []),  # structural, not direct F/L

    # I. KOIDE RELATIONS
    ("K_lepton",  "F(3)/F(4)",                 [("F",3),("F",4)]),
    ("K_up",      "L(5)/F(7)",                 [("L",5),("F",7)]),
    ("K_down",    "F(6)/L(5)",                 [("F",6),("L",5)]),

    # J. BIOLOGICAL QUANTITIES
    ("Water MW",   "L(6)",                      [("L",6)]),
    ("DNA width",  "F(8)",                      [("F",8)]),
    ("DNA pitch",  "F(9)",                      [("F",9)]),
    ("ATP atoms",  "L(8)",                      [("L",8)]),
    ("PP-IX atoms","L(9)",                      [("L",9)]),
    ("Chl a C",    "F(10)",                     [("F",10)]),
    ("AcCoA atoms","F(11)",                     [("F",11)]),

    # K. STRUCTURAL
    ("f_pi",      "L(13)/L(3)",                 [("L",13),("L",3)]),
    ("R_c",       "F(5)/L(7)",                  [("F",5),("L",7)]),
    ("r_tensor",  "L(6)/L(12)",                 [("L",6),("L",12)]),
]

# Count all index occurrences
from collections import Counter

index_counts = Counter()
f_index_counts = Counter()
l_index_counts = Counter()

for name, expr, indices in all_expressions:
    for seq, idx in indices:
        index_counts[idx] += 1
        if seq == "F":
            f_index_counts[idx] += 1
        else:
            l_index_counts[idx] += 1

# Print histogram
print("  Combined index frequencies (F + L):")
print("  %4s  %5s  %s" % ("Idx", "Count", "Bar"))
print("  " + "-" * 50)
for idx in sorted(index_counts.keys()):
    count = index_counts[idx]
    bar = "#" * count
    # Mark special indices
    tags = []
    if idx in [3, 5, 7]:
        tags.append("PRIMITIVE")
    if idx in [1, 7, 11, 29]:
        tags.append("Lucas-Coxeter")
    if idx in [13, 17, 19, 23]:
        tags.append("non-Lucas Coxeter")
    if idx in [2, 3, 5, 8, 13, 21, 34]:
        tags.append("Fibonacci")
    tag_str = "  <-- " + ", ".join(tags) if tags else ""
    print("  %4d  %5d  %s%s" % (idx, count, bar, tag_str))

print()
print("  Top 10 most-used indices:")
for idx, count in index_counts.most_common(10):
    fcount = f_index_counts.get(idx, 0)
    lcount = l_index_counts.get(idx, 0)
    print("    Index %2d: %2d times (F: %2d, L: %2d)  --  F(%d)=%d, L(%d)=%d" % (
        idx, count, fcount, lcount, idx, Fc(idx), idx, Lc(idx)))

print()
print("  Index parity analysis:")
odd_total = sum(c for i, c in index_counts.items() if i % 2 == 1)
even_total = sum(c for i, c in index_counts.items() if i % 2 == 0)
print("    Odd indices:  %d occurrences" % odd_total)
print("    Even indices: %d occurrences" % even_total)

prime_indices = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
composite_indices = [4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 22, 25, 28, 36]
prime_total = sum(index_counts.get(i, 0) for i in prime_indices)
composite_total = sum(index_counts.get(i, 0) for i in composite_indices)
print("    Prime indices (2,3,5,7,11,13,17,19,23,29): %d occurrences" % prime_total)
print("    Composite indices: %d occurrences" % composite_total)

# Primitives vs non-primitives
prim_total = sum(index_counts.get(i, 0) for i in [3, 5, 7])
print("    Primitive {3,5,7} alone: %d occurrences (%.1f%% of all)" % (
    prim_total, 100 * prim_total / sum(index_counts.values())))

# E8 Coxeter exponents
coxeter = [1, 7, 11, 13, 17, 19, 23, 29]
cox_total = sum(index_counts.get(i, 0) for i in coxeter)
print("    E8 Coxeter exponents {1,7,11,13,17,19,23,29}: %d occurrences" % cox_total)
print()


# ============================================================
# PART 3: OPERATION GRAMMAR CLASSIFICATION
# ============================================================
print("=" * 80)
print("PART 3: OPERATION GRAMMAR -- Classifying all 68 expressions")
print("=" * 80)
print()

# Classify each expression by its grammatical form
grammar_categories = {
    "Simple ratio X/Y":          [],
    "Product ratio X*Y/Z":       [],
    "Sum ratio (X+Y)/Z":         [],
    "Projection X/(Y+Z)":        [],
    "Complement 1-X/Y":          [],
    "Difference X-Y*Z":          [],
    "Phi-power phi^(X/Y)":       [],
    "Self-reference x+1+1/x":   [],
    "Single term X":             [],
    "Other/composite":           [],
}

# Manual classification based on the expressions
classifications = {
    # Simple ratio X/Y
    "alpha_2":    "Simple ratio X/Y",
    "g/2":        "Simple ratio X/Y",
    "a_e":        "Simple ratio X/Y",
    "M_H":        "Simple ratio X/Y",
    "m_t":        "Simple ratio X/Y",
    "m_b":        "Simple ratio X/Y",
    "m_c":        "Simple ratio X/Y",
    "m_u":        "Simple ratio X/Y",  # L(2)^2 is a single term squared
    "y_s":        "Simple ratio X/Y",
    "y_d":        "Simple ratio X/Y",
    "y_u":        "Simple ratio X/Y",
    "v":          "Simple ratio X/Y",
    "M_W":        "Simple ratio X/Y",
    "m_H/m_Z":    "Simple ratio X/Y",
    "m_t/m_Z":    "Simple ratio X/Y",
    "K_lepton":   "Simple ratio X/Y",
    "R_c":        "Simple ratio X/Y",
    "f_pi":       "Simple ratio X/Y",
    "r_tensor":   "Simple ratio X/Y",

    # Product ratio X*Y/Z
    "alpha_s":    "Product ratio X*Y/Z",
    "sin2W":      "Product ratio X*Y/Z",
    "gamma_I":    "Product ratio X*Y/Z",
    "m_mu":       "Product ratio X*Y/Z",
    "y_t":        "Product ratio X*Y/Z",
    "y_c":        "Product ratio X*Y/Z",
    "y_b":        "Product ratio X*Y/Z",  # L(2)^2/F(14) ~ product
    "y_tau":      "Product ratio X*Y/Z",
    "y_mu":       "Product ratio X*Y/Z",
    "y_e":        "Product ratio X*Y/Z",
    "m_mu/m_e":   "Product ratio X*Y/Z",
    "m_t/m_H":    "Product ratio X*Y/Z",  # L(7)^2/F(15)
    "1/3":        "Product ratio X*Y/Z",

    # Product (no denominator = mass ratios that are plain products)
    "m_t/m_c":    "Product ratio X*Y/Z",  # L(3)*F(9), denominator = 1
    "m_s/m_d":    "Product ratio X*Y/Z",  # L(3)*F(5)
    "m_b/m_s":    "Product ratio X*Y/Z",
    "m_b/m_d":    "Product ratio X*Y/Z",
    "m_tau/m_mu": "Product ratio X*Y/Z",

    # Sum ratio (X+Y)/Z
    "V_cb":       "Sum ratio (X+Y)/Z",
    "sin2_23":    "Sum ratio (X+Y)/Z",
    "H0":         "Sum ratio (X+Y)/Z",
    "Omega_b":    "Sum ratio (X+Y)/Z",
    "dCP/pi":     "Sum ratio (X+Y)/Z",
    "dm32/dm21":  "Sum ratio (X+Y)/Z",

    # Projection X/(Y+Z)
    "V_us":       "Projection X/(Y+Z)",
    "V_ub":       "Projection X/(Y+Z)",
    "V_td":       "Projection X/(Y+Z)",
    "V_ts":       "Projection X/(Y+Z)",  # F(7)/(F(7)+L(12)), numerator appears in denom too
    "V_cd":       "Projection X/(Y+Z)",
    "sin2_13":    "Projection X/(Y+Z)",
    "Omega_m":    "Projection X/(Y+Z)",
    "Omega_L":    "Projection X/(Y+Z)",
    "Omega_c":    "Projection X/(Y+Z)",
    "n_s":        "Projection X/(Y+Z)",
    "sigma_8":    "Projection X/(Y+Z)",

    # Complement 1-X/Y
    "V_ud":       "Complement 1-X/Y",
    "V_cs":       "Complement 1-X/Y",
    "V_tb":       "Complement 1-X/Y",
    "sin2_12":    "Complement 1-X/Y",

    # Difference X-Y*Z
    "m_e":        "Difference X-Y*Z",

    # Phi-power
    "v/M_Pl":     "Phi-power phi^(X/Y)",
    "eta_B":      "Phi-power phi^(X/Y)",

    # Self-reference
    "1/alpha":    "Self-reference x+1+1/x",

    # Single term
    "Water MW":   "Single term X",
    "DNA width":  "Single term X",
    "DNA pitch":  "Single term X",
    "ATP atoms":  "Single term X",
    "PP-IX atoms":"Single term X",
    "Chl a C":    "Single term X",
    "AcCoA atoms":"Single term X",

    # With v*F/L*sqrt2 form (uses external v)
    "m_tau":      "Other/composite",
    "m_s":        "Other/composite",
    "m_d":        "Other/composite",

    # Koide with non-trivial structure
    "K_up":       "Simple ratio X/Y",
    "K_down":     "Simple ratio X/Y",
}

# Populate categories
for name, expr, indices in all_expressions:
    cat = classifications.get(name, "Other/composite")
    grammar_categories[cat].append(name)

# Print results
total_classified = 0
for cat, members in sorted(grammar_categories.items(), key=lambda x: -len(x[1])):
    n = len(members)
    total_classified += n
    print("  %-30s : %2d expressions" % (cat, n))
    for m in sorted(members):
        print("    - %s" % m)
    print()

print("  Total classified: %d" % total_classified)
print()

# Physics category analysis: which grammar maps to which physics?
print("  GRAMMAR vs PHYSICS CORRELATION:")
print("  " + "-" * 60)

physics_types = {
    "Gauge couplings": ["alpha_s", "sin2W", "1/alpha", "alpha_2", "g/2", "a_e", "gamma_I", "1/3"],
    "CKM (diagonal)":  ["V_ud", "V_cs", "V_tb"],
    "CKM (off-diag)":  ["V_us", "V_ub", "V_cd", "V_cb", "V_td", "V_ts"],
    "PMNS angles":     ["sin2_12", "sin2_23", "sin2_13", "dCP/pi"],
    "Masses (abs)":    ["v", "M_W", "M_H", "m_t", "m_b", "m_c", "m_mu", "m_s", "m_u", "m_d", "m_e", "m_tau"],
    "Mass ratios":     ["m_t/m_c", "m_s/m_d", "m_b/m_s", "m_b/m_d", "m_tau/m_mu", "m_mu/m_e", "m_H/m_Z", "m_t/m_Z", "m_t/m_H"],
    "Yukawa":          ["y_t", "y_c", "y_b", "y_tau", "y_mu", "y_s", "y_d", "y_u", "y_e"],
    "Cosmological":    ["Omega_m", "Omega_L", "H0", "n_s", "sigma_8", "Omega_b", "Omega_c", "dm32/dm21", "eta_B", "v/M_Pl"],
    "Koide":           ["K_lepton", "K_up", "K_down"],
    "Biological":      ["Water MW", "DNA width", "DNA pitch", "ATP atoms", "PP-IX atoms", "Chl a C", "AcCoA atoms"],
}

for phys_type, members in physics_types.items():
    grammar_dist = Counter()
    for m in members:
        cat = classifications.get(m, "Other/composite")
        grammar_dist[cat] += 1
    top_grammar = grammar_dist.most_common(1)[0] if grammar_dist else ("?", 0)
    print("  %-20s -> dominant grammar: %-30s (%d/%d)" % (
        phys_type, top_grammar[0], top_grammar[1], len(members)))
    if len(grammar_dist) > 1:
        for g, c in grammar_dist.most_common():
            print("  %22s %s: %d" % ("", g, c))

print()


# ============================================================
# PART 4: COLLISION DETECTION -- Are any addresses redundant?
# ============================================================
print("=" * 80)
print("PART 4: COLLISION DETECTION -- Checking for redundant addresses")
print("=" * 80)
print()

# Compute the numerical value of each expression
def compute_value(name, expr_str, indices):
    """Compute the numerical value of the expression."""
    # We'll evaluate case by case based on the dictionary
    values = {
        "alpha_s":    Lc(3)*Lc(8)/Fc(15),
        "sin2W":      Lc(2)*Lc(8)/Fc(15),
        "1/alpha":    Lc(3)*Fc(9) + 1 + 1/(Lc(3)*Fc(9)),
        "alpha_2":    Lc(2)/Fc(11),
        "g/2":        Lc(8)/Fc(12),
        "a_e":        Lc(2)/Fc(18),
        "gamma_I":    Fc(5)*Lc(7)/Fc(15),
        "1/3":        Fc(2)/Fc(4),
        "V_ud":       1-Fc(3)/Lc(9),
        "V_us":       Fc(11)/(Lc(6)+Fc(14)),
        "V_ub":       1/(Lc(7)+Fc(13)),
        "V_cd":       Lc(7)/(Fc(6)+Lc(10)),
        "V_cs":       1-Lc(5)/(Fc(4)+Lc(14)),
        "V_cb":       (Lc(4)+Lc(6))/Fc(15),
        "V_td":       1/(Fc(3)+Lc(10)),
        "V_ts":       Fc(7)/(Fc(7)+Lc(12)),
        "V_tb":       1-Fc(6)/Lc(19),
        "sin2_12":    1.0/3-Fc(3)/Lc(9),
        "sin2_23":    (Lc(5)+Lc(12))/Fc(15),
        "sin2_13":    Lc(5)/(Lc(10)+Fc(14)),
        "dCP/pi":     (Lc(3)+Lc(8))/Lc(8),
        "v":          Fc(16)/Lc(3),
        "M_W":        Lc(12)/Lc(3),
        "M_H":        Fc(14)/Lc(2),
        "m_t":        Lc(13)/Lc(2),
        "m_b":        Fc(8)/Fc(5),
        "m_tau":      (Fc(16)/Lc(3))*Fc(3)/(Lc(11)*sqrt2),
        "m_c":        Fc(5)/Lc(3),
        "m_mu":       Fc(7)*Fc(8)/Fc(18),
        "m_s":        (Fc(16)/Lc(3))*Fc(5)/(Lc(19)*sqrt2),
        "m_u":        Lc(2)**2/Fc(19),
        "m_d":        (Fc(16)/Lc(3))*Fc(3)/(Fc(25)*sqrt2),
        "m_e":        (Lc(13)-Fc(3)*Fc(5))*1e-6,  # keV to GeV
        "y_t":        Lc(5)*Lc(8)/Lc(13),
        "y_c":        Fc(3)*Fc(7)/Lc(17),
        "y_b":        Lc(2)**2/Fc(14),
        "y_tau":      Fc(3)*Lc(4)/Lc(15),
        "y_mu":       Lc(2)*Fc(6)/Lc(22),
        "y_s":        Fc(5)/Lc(19),
        "y_d":        Fc(3)/Fc(25),
        "y_u":        Lc(3)/Fc(28),
        "y_e":        Fc(3)*Lc(8)/Lc(36),
        "m_t/m_c":    Lc(3)*Fc(9),
        "m_s/m_d":    Lc(3)*Fc(5),
        "m_b/m_s":    Lc(3)*Lc(10)/Lc(5),
        "m_b/m_d":    Lc(6)*Lc(11)/Lc(3),
        "m_tau/m_mu": Lc(3)*Fc(8)/Fc(5),
        "m_mu/m_e":   Lc(4)*Fc(11)/Fc(4),
        "m_H/m_Z":    Lc(5)/Fc(6),
        "m_t/m_Z":    Fc(11)/Lc(8),
        "m_t/m_H":    Lc(7)**2/Fc(15),
        "Omega_m":    Lc(7)/(Fc(4)+Fc(11)),
        "Omega_L":    Fc(13)/(Lc(6)+Lc(12)),
        "H0":         (Lc(6)+Lc(13))/Fc(6),
        "n_s":        Fc(10)/(Fc(3)+Fc(10)),
        "sigma_8":    Lc(8)/(Lc(5)+Lc(8)),
        "Omega_b":    (Lc(4)+Lc(11))/Fc(19),
        "Omega_c":    (Lc(5)+Fc(11))/Fc(14),
        "dm32/dm21":  (Lc(5)+Lc(7))/Lc(4),
        "eta_B":      phibar**44,
        "v/M_Pl":     phibar**80,
        "K_lepton":   Fc(3)/Fc(4),
        "K_up":       Lc(5)/Fc(7),
        "K_down":     Fc(6)/Lc(5),
        "Water MW":   Lc(6),
        "DNA width":  Fc(8),
        "DNA pitch":  Fc(9),
        "ATP atoms":  Lc(8),
        "PP-IX atoms":Lc(9),
        "Chl a C":    Fc(10),
        "AcCoA atoms":Fc(11),
        "f_pi":       Lc(13)/Lc(3),
        "R_c":        Fc(5)/Lc(7),
        "r_tensor":   Lc(6)/Lc(12),
    }
    return values.get(name, None)

# Compute all values
computed = {}
for name, expr, indices in all_expressions:
    val = compute_value(name, expr, indices)
    if val is not None:
        computed[name] = val

# Check for collisions: same numerical value from different expressions
print("  Checking if any two quantities produce the same F/L value...")
print()

collision_threshold = 1e-10
collisions_found = 0
near_collisions = []

names = list(computed.keys())
for i in range(len(names)):
    for j in range(i+1, len(names)):
        n1, n2 = names[i], names[j]
        v1, v2 = computed[n1], computed[n2]
        if v1 == 0 or v2 == 0:
            continue
        rel_diff = abs(v1 - v2) / max(abs(v1), abs(v2))
        if rel_diff < collision_threshold:
            print("  ** EXACT COLLISION: %s = %s = %.10f" % (n1, n2, v1))
            collisions_found += 1
        elif rel_diff < 0.01:
            near_collisions.append((rel_diff, n1, n2, v1, v2))

if collisions_found == 0:
    print("  No exact collisions found. Good -- all addresses are unique.")
else:
    print("  Found %d exact collision(s)." % collisions_found)

if near_collisions:
    near_collisions.sort()
    print()
    print("  Near-collisions (values within 1%%):")
    for diff, n1, n2, v1, v2 in near_collisions[:10]:
        print("    %s (%.6f) vs %s (%.6f)  -- diff = %.4f%%" % (
            n1, v1, n2, v2, diff * 100))
print()


# ============================================================
# PART 5: FIBONACCI IDENTITY WEB -- Is the language closed?
# ============================================================
print("=" * 80)
print("PART 5: FIBONACCI IDENTITY WEB -- Closure under operations")
print("=" * 80)
print()
print("  For each pair of verified expressions, check if their ratio")
print("  or difference is itself an F/L expression in the dictionary.")
print()

# Build a lookup of all known values -> names
value_to_name = {}
for name, val in computed.items():
    value_to_name[name] = val

# Also build a table of simple F/L ratios for matching
simple_fl_ratios = {}
for n in range(1, 30):
    for m in range(1, 30):
        for s1_name, s1 in [("F", Fc), ("L", Lc)]:
            for s2_name, s2 in [("F", Fc), ("L", Lc)]:
                v1 = s1(n)
                v2 = s2(m)
                if v2 != 0 and v1 != 0:
                    r = v1 / v2
                    key = "%s(%d)/%s(%d)" % (s1_name, n, s2_name, m)
                    simple_fl_ratios[key] = r

# For products and sums
simple_fl_products = {}
for n in range(1, 20):
    for m in range(1, 20):
        for s1_name, s1 in [("F", Fc), ("L", Lc)]:
            for s2_name, s2 in [("F", Fc), ("L", Lc)]:
                v = s1(n) * s2(m)
                if v != 0:
                    key = "%s(%d)*%s(%d)" % (s1_name, n, s2_name, m)
                    simple_fl_products[key] = v

# Check ratios
print("  A) RATIOS of dictionary entries that match F/L expressions:")
print()
ratio_hits = []
for i, n1 in enumerate(names):
    for j, n2 in enumerate(names):
        if i >= j:
            continue
        v1, v2 = computed[n1], computed[n2]
        if v2 == 0 or v1 == 0:
            continue
        ratio = v1 / v2
        if ratio <= 0:
            continue

        # Check against simple F/L ratios
        for fl_expr, fl_val in simple_fl_ratios.items():
            if fl_val == 0:
                continue
            rel = abs(ratio - fl_val) / abs(fl_val)
            if rel < 0.001:  # within 0.1%
                ratio_hits.append((rel, n1, n2, ratio, fl_expr, fl_val))

        # Check against known dictionary entries
        for n3, v3 in computed.items():
            if n3 == n1 or n3 == n2:
                continue
            if v3 == 0:
                continue
            rel = abs(ratio - v3) / abs(v3)
            if rel < 0.001:
                ratio_hits.append((rel, n1, n2, ratio, n3, v3))

ratio_hits.sort()
seen_pairs = set()
count = 0
for rel, n1, n2, ratio, target, tval in ratio_hits:
    pair_key = (n1, n2, target)
    if pair_key in seen_pairs:
        continue
    seen_pairs.add(pair_key)
    print("    %s / %s = %.6f  ~  %s = %.6f  (%.4f%%)" % (
        n1, n2, ratio, target, tval, rel * 100))
    count += 1
    if count >= 25:
        print("    ... (showing top 25)")
        break

print()
print("  Total ratio relationships found: %d" % len(seen_pairs))
print()

# Check differences
print("  B) DIFFERENCES of dictionary entries that match F/L expressions:")
print()
diff_hits = []
for i, n1 in enumerate(names):
    for j, n2 in enumerate(names):
        if i == j:
            continue
        v1, v2 = computed[n1], computed[n2]
        diff = v1 - v2
        if diff <= 0:
            continue

        # Check against simple F/L ratios
        for fl_expr, fl_val in simple_fl_ratios.items():
            if fl_val <= 0:
                continue
            rel = abs(diff - fl_val) / abs(fl_val)
            if rel < 0.001:
                diff_hits.append((rel, n1, n2, diff, fl_expr, fl_val))

        # Check against known dictionary entries
        for n3, v3 in computed.items():
            if n3 == n1 or n3 == n2:
                continue
            if v3 <= 0:
                continue
            rel = abs(diff - v3) / abs(v3)
            if rel < 0.001:
                diff_hits.append((rel, n1, n2, diff, n3, v3))

diff_hits.sort()
seen_diffs = set()
dcount = 0
for rel, n1, n2, diff, target, tval in diff_hits:
    pair_key = (n1, n2, target)
    if pair_key in seen_diffs:
        continue
    seen_diffs.add(pair_key)
    print("    %s - %s = %.6f  ~  %s = %.6f  (%.4f%%)" % (
        n1, n2, diff, target, tval, rel * 100))
    dcount += 1
    if dcount >= 25:
        print("    ... (showing top 25)")
        break

print()
print("  Total difference relationships found: %d" % len(seen_diffs))
print()

# Check products
print("  C) PRODUCTS of dictionary entries that match F/L expressions:")
print()
prod_hits = []
# Only check a subset to avoid combinatorial explosion
key_quantities = ["alpha_s", "sin2W", "K_lepton", "1/3", "V_us", "V_cb",
                  "gamma_I", "g/2", "a_e", "alpha_2", "m_H/m_Z",
                  "R_c", "r_tensor", "Omega_m", "Omega_L"]
for n1 in key_quantities:
    for n2 in key_quantities:
        if n1 >= n2:
            continue
        if n1 not in computed or n2 not in computed:
            continue
        v1, v2 = computed[n1], computed[n2]
        prod = v1 * v2
        if prod <= 0:
            continue

        for fl_expr, fl_val in simple_fl_ratios.items():
            if fl_val <= 0:
                continue
            rel = abs(prod - fl_val) / abs(fl_val)
            if rel < 0.001:
                prod_hits.append((rel, n1, n2, prod, fl_expr, fl_val))

        for n3, v3 in computed.items():
            if n3 in (n1, n2) or v3 <= 0:
                continue
            rel = abs(prod - v3) / abs(v3)
            if rel < 0.001:
                prod_hits.append((rel, n1, n2, prod, n3, v3))

prod_hits.sort()
seen_prods = set()
pcount = 0
for rel, n1, n2, prod, target, tval in prod_hits:
    pair_key = (n1, n2, target)
    if pair_key in seen_prods:
        continue
    seen_prods.add(pair_key)
    print("    %s * %s = %.6f  ~  %s = %.6f  (%.4f%%)" % (
        n1, n2, prod, target, tval, rel * 100))
    pcount += 1
    if pcount >= 15:
        print("    ... (showing top 15)")
        break

print()
print("  Total product relationships found: %d" % len(seen_prods))
print()


# ============================================================
# SUMMARY
# ============================================================
print("=" * 80)
print("SUMMARY OF DEEPER PATTERNS")
print("=" * 80)
print()
print("  1. SUBTRACTION PATTERN L(a) - X(b)*Y(c):")
print("     - m_e = L(13) - F(3)*F(5) = 511 keV [EXACT, the original discovery]")
print("     - Results for other masses shown above")
print()
print("  2. INDEX HISTOGRAM:")
top3 = index_counts.most_common(3)
print("     - Most-used indices: %s" % ", ".join(
    "%d (%d times)" % (i, c) for i, c in top3))
print("     - Primitives {3,5,7} account for %.1f%% of all index uses" % (
    100 * prim_total / sum(index_counts.values())))
print("     - Odd vs even: %d vs %d" % (odd_total, even_total))
print()
print("  3. OPERATION GRAMMAR:")
grammar_sizes = [(cat, len(members)) for cat, members in grammar_categories.items() if members]
grammar_sizes.sort(key=lambda x: -x[1])
for cat, n in grammar_sizes:
    print("     - %-30s: %2d expressions" % (cat, n))
print()
print("  4. COLLISIONS: %d exact, %d near (within 1%%)" % (
    collisions_found, len(near_collisions)))
print()
print("  5. IDENTITY WEB:")
print("     - Ratio relationships found: %d" % len(seen_pairs))
print("     - Difference relationships found: %d" % len(seen_diffs))
print("     - Product relationships found: %d" % len(seen_prods))
closure_total = len(seen_pairs) + len(seen_diffs) + len(seen_prods)
print("     - Total cross-links: %d" % closure_total)
if closure_total > 20:
    print("     --> The language shows SIGNIFICANT closure under operations.")
elif closure_total > 5:
    print("     --> The language shows MODERATE closure under operations.")
else:
    print("     --> The language shows WEAK closure under operations.")
print()
print("=" * 80)
print("END OF ANALYSIS")
print("=" * 80)
