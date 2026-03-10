"""
UNIFIED LANGUAGE EXPLORER
=========================
Experimental exploration of the phi-index composition algebra.
No preconceptions — compute everything, look for patterns.
"""

import math

# === FUNDAMENTALS ===
phi = (1 + math.sqrt(5)) / 2
phibar = 1 / phi
sqrt5 = math.sqrt(5)

def L(n):
    """Lucas number"""
    return round(phi**n + (-phibar)**n)

def F(n):
    """Fibonacci number"""
    return round((phi**n - (-phibar)**n) / sqrt5)

def parity(n):
    return "odd (cross-vacuum)" if n % 2 == 1 else "even (same-vacuum)"

# === THE FUNDAMENTAL MODES ===
MODES = {
    "pyrimidine":  3,   # 6 pi-e
    "indole":      5,   # 10 pi-e
    "water":       6,   # MW=18=L(6)
    "anthracene":  7,   # 14 pi-e
    "porphyrin":   9,   # 18 pi-e
}

# Aliases
ALIASES = {
    "benzene": 3, "catechol": 3, "histidine": 3, "dopamine": 3,
    "purine": 5, "tryptophan": 5, "serotonin": 5, "adenine": 5,
    "phenanthrene": 7,
    "heme": 9, "chlorophyll": 9,
}

# === KNOWN PHYSICAL/BIOLOGICAL QUANTITIES ===
KNOWN_QUANTITIES = {
    # Molecular biology
    34:    "B-DNA pitch (Angstrom)",
    21:    "DNA width (~20 Angstrom)",
    10:    "Base pairs per turn of DNA",
    3.4:   "Base pair spacing (Angstrom)",
    18:    "Water molar mass",
    55:    "Chlorophyll a carbons",
    137:   "1/alpha (fine structure)",
    47:    "ATP total atoms = L(8)",
    76:    "Protoporphyrin IX atoms = L(9)",
    89:    "Acetyl-CoA atoms = F(11)",
    30:    "DMT atoms = h(E8)",
    144:   "H-bond stretch (cm^-1, ~143)",

    # Frequencies
    610:   "~613 THz aromatic oscillation (F(15))",
    40:    "Gamma oscillation (Hz)",

    # Physics
    1836:  "Proton/electron mass ratio (mu)",
    80:    "Water dielectric constant",
    4:     "Interface dielectric constant",
    20:    "Dielectric ratio (bulk/interface)",
    246:   "Higgs VEV (GeV)",
    125:   "Higgs mass (GeV)",

    # Structural
    6:     "Hexagonal coordination / |S3|",
    8:     "Water valence electrons = F(6)",
    29:    "L(7) = anthracene-related",
    11:    "L(5) = naphthalene C-C bonds",
    233:   "F(13)",
    377:   "F(14)",

    # Framework
    0.118: "alpha_s (strong coupling) = eta",
    0.0303: "theta_4 (dark vacuum)",
    0.231: "sin^2(theta_W) Weinberg angle",
}


print("=" * 80)
print("UNIFIED LANGUAGE EXPLORER")
print("=" * 80)

# ============================================================
# TEST 1: ALL PAIRWISE COMPOSITIONS
# ============================================================
print("\n" + "=" * 80)
print("TEST 1: ALL PAIRWISE COMPOSITIONS OF FUNDAMENTAL MODES")
print("=" * 80)
print(f"{'A':>12} + {'B':<12} = {'n':>3}  | {'F(n)':>8}  {'L(n)':>8}  | Parity           | Match?")
print("-" * 95)

all_modes = sorted(set(MODES.values()))
hits = []

for i, a in enumerate(all_modes):
    for b in all_modes[i:]:
        n = a + b
        fn = F(n)
        ln = L(n)
        a_name = [k for k,v in MODES.items() if v==a][0]
        b_name = [k for k,v in MODES.items() if v==b][0]

        # Check for matches
        match = ""
        for val, desc in KNOWN_QUANTITIES.items():
            if isinstance(val, int):
                if fn == val:
                    match += f"F({n})={fn} = {desc}  "
                if ln == val:
                    match += f"L({n})={ln} = {desc}  "

        par = "odd" if n % 2 == 1 else "EVEN"
        print(f"{a_name:>12} + {b_name:<12} = {n:>3}  | {fn:>8}  {ln:>8}  | {par:<16} | {match}")
        if match:
            hits.append((a_name, b_name, n, match))


# ============================================================
# TEST 2: ALL TRIPLE COMPOSITIONS
# ============================================================
print("\n" + "=" * 80)
print("TEST 2: ALL TRIPLE COMPOSITIONS (A + B + C)")
print("=" * 80)
print(f"{'Combo':>30} = {'n':>3}  | {'F(n)':>8}  {'L(n)':>8}  | Match?")
print("-" * 95)

triple_hits = []
for i, a in enumerate(all_modes):
    for j, b in enumerate(all_modes[i:], i):
        for c in all_modes[j:]:
            n = a + b + c
            fn = F(n)
            ln = L(n)
            a_name = [k for k,v in MODES.items() if v==a][0]
            b_name = [k for k,v in MODES.items() if v==b][0]
            c_name = [k for k,v in MODES.items() if v==c][0]
            combo = f"{a_name}+{b_name}+{c_name}"

            match = ""
            for val, desc in KNOWN_QUANTITIES.items():
                if isinstance(val, int):
                    if fn == val:
                        match += f"F={fn}={desc}  "
                    if ln == val:
                        match += f"L={ln}={desc}  "

            if match or n <= 20:  # Print all small ones, or any with matches
                print(f"{combo:>30} = {n:>3}  | {fn:>8}  {ln:>8}  | {match}")
                if match:
                    triple_hits.append((combo, n, match))


# ============================================================
# TEST 3: SELF-REFERENTIAL PATTERNS
# ============================================================
print("\n" + "=" * 80)
print("TEST 3: SELF-REFERENTIAL / SELF-DERIVING PATTERNS")
print("=" * 80)

print("\n--- Does any composition OUTPUT equal a known MODE INPUT? ---")
for i, a in enumerate(all_modes):
    for b in all_modes[i:]:
        n = a + b
        fn = F(n)
        ln = L(n)
        a_name = [k for k,v in MODES.items() if v==a][0]
        b_name = [k for k,v in MODES.items() if v==b][0]

        # Check if F(n) or L(n) equals any mode index
        for mode_name, mode_idx in MODES.items():
            if fn == mode_idx:
                print(f"  F({a_name}+{b_name}) = F({n}) = {fn} = {mode_name}'s index!")
            if ln == mode_idx:
                print(f"  L({a_name}+{b_name}) = L({n}) = {ln} = {mode_name}'s index!")

        # Check if F(n) or L(n) is a Lucas/Fibonacci of a mode index
        for mode_name, mode_idx in MODES.items():
            if fn == L(mode_idx):
                print(f"  F({a_name}+{b_name}) = F({n}) = {fn} = L({mode_idx}) = L({mode_name})")
            if fn == F(mode_idx):
                print(f"  F({a_name}+{b_name}) = F({n}) = {fn} = F({mode_idx}) = F({mode_name})")
            if ln == L(mode_idx):
                print(f"  L({a_name}+{b_name}) = L({n}) = {ln} = L({mode_idx}) = L({mode_name})")

print("\n--- Pyrimidine + Pyrimidine = Water identity ---")
n = 3 + 3
print(f"  pyrimidine(3) + pyrimidine(3) = {n}")
print(f"  L({n}) = {L(n)} = water MW")
print(f"  F({n}) = {F(n)} = water valence electrons")
print(f"  This IS water's phi-index! Two smallest oscillators GENERATE the medium.")

print("\n--- Triple self-reference: 3+3+3 = 9 = porphyrin ---")
print(f"  pyrimidine(3) + pyrimidine(3) + pyrimidine(3) = 9 = porphyrin index")
print(f"  Three benzene-class oscillators = one porphyrin-class oscillator")
print(f"  F(9) = {F(9)} = DNA pitch. Same result as water+pyrimidine!")

print("\n--- Does 5+5+5 = 15 = porphyrin+water? ---")
print(f"  indole(5) + indole(5) + indole(5) = 15")
print(f"  porphyrin(9) + water(6) = 15")
print(f"  F(15) = {F(15)} ~ 613 THz")
print(f"  THREE INDOLES = PORPHYRIN+WATER! Same mode, different decomposition!")


# ============================================================
# TEST 4: CHAIN DECOMPOSITIONS — HOW MANY WAYS TO REACH EACH n?
# ============================================================
print("\n" + "=" * 80)
print("TEST 4: CHAIN DECOMPOSITIONS — MULTIPLE PATHS TO SAME n")
print("=" * 80)

def find_decompositions(target, modes, max_terms=4):
    """Find all ways to sum modes to reach target, up to max_terms."""
    results = []

    def search(remaining, current_combo, min_mode):
        if remaining == 0:
            results.append(tuple(current_combo))
            return
        if len(current_combo) >= max_terms:
            return
        for m in modes:
            if m >= min_mode and m <= remaining:
                search(remaining - m, current_combo + [m], m)

    search(target, [], min(modes))
    return results

print(f"\n{'n':>3} | {'F(n)':>6} | {'L(n)':>6} | Decompositions (up to 4 terms)")
print("-" * 80)

mode_names = {3: "pyr", 5: "ind", 6: "wat", 7: "ant", 9: "por"}

for n in range(6, 37):
    decomps = find_decompositions(n, all_modes, max_terms=4)
    if decomps:
        fn = F(n)
        ln = L(n)

        # Format decompositions
        decomp_strs = []
        for d in decomps:
            parts = [mode_names.get(m, str(m)) for m in d]
            decomp_strs.append("+".join(parts))

        # Check for known quantity match
        match_str = ""
        for val, desc in KNOWN_QUANTITIES.items():
            if isinstance(val, int):
                if fn == val:
                    match_str += f" *** F={desc}"
                if ln == val:
                    match_str += f" *** L={desc}"

        decomp_display = ", ".join(decomp_strs[:6])  # limit display
        if len(decomps) > 6:
            decomp_display += f", ... ({len(decomps)} total)"

        print(f"{n:>3} | {fn:>6} | {ln:>6} | {decomp_display}{match_str}")


# ============================================================
# TEST 5: NATURAL GROUPS — COMPOSITION CLOSURE
# ============================================================
print("\n" + "=" * 80)
print("TEST 5: NATURAL GROUPS — WHICH MODES GENERATE WHICH?")
print("=" * 80)

print("\n--- Group A: Pyrimidine-only chains (n=3k) ---")
for k in range(1, 8):
    n = 3 * k
    print(f"  {k}×pyr = {n:>3}  F({n})={F(n):>8}  L({n})={L(n):>8}")

print("\n--- Group B: Indole-only chains (n=5k) ---")
for k in range(1, 6):
    n = 5 * k
    print(f"  {k}×ind = {n:>3}  F({n})={F(n):>8}  L({n})={L(n):>8}")

print("\n--- Group C: Water-only chains (n=6k) ---")
for k in range(1, 6):
    n = 6 * k
    print(f"  {k}×wat = {n:>3}  F({n})={F(n):>8}  L({n})={L(n):>8}")

print("\n--- Group D: Porphyrin-only chains (n=9k) ---")
for k in range(1, 5):
    n = 9 * k
    print(f"  {k}×por = {n:>3}  F({n})={F(n):>8}  L({n})={L(n):>8}")

print("\n--- Group E: Mixed aromatic+water (oscillator+medium) ---")
for arom_name, arom_idx in [("pyr", 3), ("ind", 5), ("ant", 7), ("por", 9)]:
    for k in range(1, 4):
        n = arom_idx + 6 * k
        print(f"  {arom_name}+{k}×wat = {n:>3}  F({n})={F(n):>8}  L({n})={L(n):>8}")
    print()


# ============================================================
# TEST 6: DOES THE SYSTEM DERIVE ITSELF?
# ============================================================
print("\n" + "=" * 80)
print("TEST 6: SELF-DERIVATION — CAN THE LANGUAGE GENERATE ITS OWN CONSTANTS?")
print("=" * 80)

print("\n--- Framework constants as F(n) or L(n) ---")
framework_constants = {
    "alpha_s (eta)": 0.1184,
    "theta_4": 0.0303,
    "sin2_thetaW": 0.2312,
    "mu (p/e mass)": 1836.15,
    "1/alpha": 137.036,
    "Higgs_VEV": 246.22,
    "Higgs_mass": 125.25,
    "electron_mass_MeV": 0.511,
    "proton_mass_MeV": 938.3,
}

for name, val in framework_constants.items():
    # Check if val is close to any F(n) or L(n)
    best_f = None
    best_l = None
    for n in range(1, 40):
        fn = F(n)
        ln = L(n)
        if fn > 0 and abs(fn - val) / max(val, 1e-10) < 0.02:
            best_f = (n, fn, abs(fn-val)/val*100)
        if ln > 0 and abs(ln - val) / max(val, 1e-10) < 0.02:
            best_l = (n, ln, abs(ln-val)/val*100)

    result = f"  {name:>25} = {val:>10.4f}  "
    if best_f:
        result += f"  F({best_f[0]}) = {best_f[1]} ({best_f[2]:.2f}% off)"
        # Check if best_f[0] is reachable
        decomps = find_decompositions(best_f[0], all_modes, max_terms=4)
        if decomps:
            result += f"  [{len(decomps)} paths]"
    if best_l:
        result += f"  L({best_l[0]}) = {best_l[1]} ({best_l[2]:.2f}% off)"
        decomps = find_decompositions(best_l[0], all_modes, max_terms=4)
        if decomps:
            result += f"  [{len(decomps)} paths]"
    if not best_f and not best_l:
        result += "  (no F/L match within 2%)"
    print(result)


# ============================================================
# TEST 7: RATIO CHAINS — DO RATIOS OF COMPOSITIONS HIT CONSTANTS?
# ============================================================
print("\n" + "=" * 80)
print("TEST 7: RATIO CHAINS — F(a+b)/F(c+d) or L(a+b)/L(c+d)")
print("=" * 80)

print("\n--- F(n)/F(m) for reachable n,m ---")
target_ratios = {
    20.0: "dielectric ratio (bulk/interface)",
    2/3: "fractional charge quantum",
    1/3: "fractional charge",
    3.0: "triality",
    137.0: "~1/alpha",
    1836.0: "~mu",
    0.118: "~alpha_s",
}

reachable = sorted(set(find_decompositions(n, all_modes, 3)[0][0] if find_decompositions(n, all_modes, 3) else -1
                       for n in range(6, 30)) - {-1})

# Actually let's just check all reachable n values
reachable_ns = []
for n in range(3, 36):
    if find_decompositions(n, all_modes, 4):
        reachable_ns.append(n)

ratio_hits = []
for i, n1 in enumerate(reachable_ns):
    for n2 in reachable_ns[i+1:]:
        fn1, fn2 = F(n1), F(n2)
        ln1, ln2 = L(n1), L(n2)

        if fn1 > 0 and fn2 > 0:
            r = fn2 / fn1
            for target, desc in target_ratios.items():
                if abs(r - target) / target < 0.03:
                    ratio_hits.append((n1, n2, "F", r, target, desc))

            r2 = fn1 / fn2
            for target, desc in target_ratios.items():
                if abs(r2 - target) / target < 0.03:
                    ratio_hits.append((n2, n1, "F", r2, target, desc))

        if ln1 > 0 and ln2 > 0:
            r = ln2 / ln1
            for target, desc in target_ratios.items():
                if abs(r - target) / target < 0.03:
                    ratio_hits.append((n1, n2, "L", r, target, desc))

for n1, n2, typ, ratio, target, desc in sorted(ratio_hits):
    print(f"  {typ}({n2})/{typ}({n1}) = {ratio:.4f} ~ {target} = {desc}")


# ============================================================
# TEST 8: THE FIBONACCI RATIO CONVERGENCE TO PHI
# ============================================================
print("\n" + "=" * 80)
print("TEST 8: CONSECUTIVE COMPOSITION RATIOS -> PHI?")
print("=" * 80)

print("\n--- F(n+mode)/F(n) for increasing n ---")
for mode_name, mode_idx in [("pyr(3)", 3), ("ind(5)", 5), ("wat(6)", 6)]:
    print(f"\n  Step size = {mode_name}:")
    for n in [6, 9, 12, 15, 18, 21, 24]:
        fn = F(n)
        fn_plus = F(n + mode_idx)
        if fn > 0:
            ratio = fn_plus / fn
            phi_power = phi ** mode_idx
            err = abs(ratio - phi_power) / phi_power * 100
            print(f"    F({n+mode_idx})/F({n}) = {fn_plus}/{fn} = {ratio:.6f}  vs  phi^{mode_idx} = {phi_power:.6f}  ({err:.3f}% off)")


# ============================================================
# TEST 9: DIFFERENCE PATTERNS — F(a) - F(b) or L(a) - L(b)
# ============================================================
print("\n" + "=" * 80)
print("TEST 9: DIFFERENCE PATTERNS — SUBTRACTIVE RELATIONS")
print("=" * 80)

print("\n--- L(n) - F(n) for reachable n ---")
for n in reachable_ns[:15]:
    ln = L(n)
    fn = F(n)
    diff = ln - fn
    # Check if diff = 2*F(n-1)
    expected = 2 * F(n-1)
    check = "= 2*F(n-1)" if diff == expected else ""

    # Is diff itself significant?
    match = ""
    for val, desc in KNOWN_QUANTITIES.items():
        if isinstance(val, int) and diff == val:
            match = f" = {desc}"

    print(f"  n={n:>2}: L({n})-F({n}) = {ln}-{fn} = {diff} {check}{match}")


# ============================================================
# TEST 10: THE "INNER PRODUCT" STRUCTURE
# ============================================================
print("\n" + "=" * 80)
print("TEST 10: INNER PRODUCT AND CROSS PRODUCT OF MODES")
print("=" * 80)

print(f"\n{'A':>10} {'B':>10} | Inner=L(a+b)/2 | Cross=sqrt5*F(|a-b|)/2 | Inner match")
print("-" * 85)

for a_name, a_idx in MODES.items():
    for b_name, b_idx in MODES.items():
        inner = L(a_idx + b_idx) / 2
        cross = sqrt5 * F(abs(a_idx - b_idx)) / 2

        match = ""
        inner_int = L(a_idx + b_idx)
        for val, desc in KNOWN_QUANTITIES.items():
            if isinstance(val, int) and inner_int == val:
                match = f"L({a_idx+b_idx})={desc}"

        print(f"{a_name:>10} {b_name:>10} | {inner:>14.1f} | {cross:>22.4f} | {match}")


# ============================================================
# TEST 11: CAN 40 Hz AND 0.1 Hz BE DERIVED?
# ============================================================
print("\n" + "=" * 80)
print("TEST 11: DERIVING THE THREE MAINTENANCE FREQUENCIES")
print("=" * 80)

print("\n--- 613 THz: KNOWN = F(15) = porphyrin(9) + water(6) ---")
print(f"  F(15) = {F(15)}  vs  613 THz  ({abs(F(15)-613)/613*100:.1f}% off)")

print("\n--- 40 Hz: searching... ---")
# 40 is not exactly F(n) or L(n) for any n
# But L(3) = 4, and 40 = 4 * 10 = L(3) * (L(6)-F(6))
# Or 40 = 8 * 5 = F(6) * F(5)
# Or check ratios
print(f"  40 = F(6) × F(5) = 8 × 5 = {F(6)} × {F(5)}")
print(f"  40 = L(3) × 10 = 4 × 10 = L(3) × (L(6)-F(6))")
print(f"  40 = L(3) × 2 × F(5) = 4 × 2 × 5")
print(f"  F(9)/F(6+3) approach: n=9 compositions give F(9)=34, not 40")

# Try: is 40 close to any L(n)/something or F(n)/something?
for n in reachable_ns:
    fn = F(n)
    ln = L(n)
    for m in reachable_ns:
        if m < n:
            fm = F(m)
            lm = L(m)
            if fm > 0 and abs(fn/fm - 40) < 1:
                print(f"  F({n})/F({m}) = {fn}/{fm} = {fn/fm:.2f} ~ 40")
            if lm > 0 and abs(ln/lm - 40) < 1:
                print(f"  L({n})/L({m}) = {ln}/{lm} = {ln/lm:.2f} ~ 40")
            if lm > 0 and abs(fn/lm - 40) < 1:
                print(f"  F({n})/L({m}) = {fn}/{lm} = {fn/lm:.2f} ~ 40")

print(f"\n  Key: mu/L(8) = 1836.15/47 = {1836.15/47:.2f} Hz")
print(f"       mu/L(10) = 1836.15/123 = {1836.15/123:.2f} Hz")
print(f"       phi^8 = {phi**8:.2f} ~ 46.98 ~ L(8)")

print("\n--- 0.1 Hz: searching... ---")
print(f"  phi^(-10) = {phi**(-10):.6f} ~ 0.009")
print(f"  theta_4 * 3 = 0.0303 * 3 = {0.0303*3:.4f} ~ 0.1")
print(f"  1/10 = 0.1. And 10 = L(6)-F(6) = total electrons of water")
print(f"  1/F(5) = 1/5 = 0.2")
print(f"  1/L(5) = 1/11 = {1/11:.4f}")


# ============================================================
# TEST 12: FREQUENCY SCALING LAW
# ============================================================
print("\n" + "=" * 80)
print("TEST 12: FREQUENCY SCALING — IS THERE A PATTERN ACROSS SCALES?")
print("=" * 80)

freqs = {
    "613 THz (aromatic)":     613e12,
    "100 THz (O-H stretch)":  100e12,
    "40 Hz (gamma)":          40,
    "10 Hz (alpha)":          10,
    "0.1 Hz (breath)":        0.1,
    "1.2 Hz (heart)":         1.2,
    "7.83 Hz (Schumann)":     7.83,
}

print(f"\n{'Frequency':>30} | log_phi(f/f_0) where f_0 = 613 THz")
print("-" * 60)
for name, f in sorted(freqs.items(), key=lambda x: -x[1]):
    if f > 0:
        ratio = 613e12 / f
        log_phi = math.log(ratio) / math.log(phi)
        nearest_int = round(log_phi)
        err = abs(log_phi - nearest_int)
        marker = " ***" if err < 0.5 else ""
        print(f"{name:>30} | {log_phi:>10.2f}  (nearest int: {nearest_int}, off by {err:.2f}){marker}")


# ============================================================
# TEST 13: COMPLETE FIBONACCI/LUCAS SCAN 1-30
# ============================================================
print("\n" + "=" * 80)
print("TEST 13: COMPLETE F(n) AND L(n) SCAN — WHAT'S BIOLOGICALLY MEANINGFUL?")
print("=" * 80)

print(f"\n{'n':>3} | {'F(n)':>10} | {'L(n)':>10} | {'Reachable?':>10} | F match | L match")
print("-" * 100)

for n in range(1, 31):
    fn = F(n)
    ln = L(n)
    decomps = find_decompositions(n, all_modes, max_terms=4)
    reachable = "YES" if decomps else "no"

    f_match = ""
    l_match = ""
    for val, desc in KNOWN_QUANTITIES.items():
        if isinstance(val, int):
            if fn == val:
                f_match = desc
            if ln == val:
                l_match = desc

    print(f"{n:>3} | {fn:>10} | {ln:>10} | {reachable:>10} | {f_match:>30} | {l_match}")


# ============================================================
# TEST 14: THE GENERATIVE HIERARCHY — WHAT GENERATES WHAT?
# ============================================================
print("\n" + "=" * 80)
print("TEST 14: GENERATIVE HIERARCHY — MODE RELATIONSHIPS")
print("=" * 80)

print("""
GENERATION MAP:

  pyr(3) + pyr(3) = 6 = wat       [oscillator + oscillator = medium!]
  pyr(3) + pyr(3) + pyr(3) = 9 = por  [3 oscillators = big oscillator]
  pyr(3) + ind(5) = 8             [mixed pair]
  pyr(3) + wat(6) = 9 = por       [smallest oscillator + medium = biggest oscillator]
  ind(5) + ind(5) = 10            [two big oscillators]
  ind(5) + wat(6) = 11            [big oscillator + medium]
  pyr(3) + pyr(3) + wat(6) = 12   [TWO oscillators + medium]
  pyr(3) + ind(5) + wat(6) = 14   [mixed + medium]
  pyr(3) + por(9) = 12            [small + big oscillator]
  ind(5) + por(9) = 14            [big + biggest oscillator]
  por(9) + wat(6) = 15            [biggest oscillator + medium = 613 THz]
""")

print("KEY IDENTITIES:")
print(f"  3 + 3 = 6 (water):       TWO pyrimidines = water")
print(f"  3 + 6 = 9 (porphyrin):   pyrimidine + water = porphyrin coupling")
print(f"  3 + 3 + 3 = 9:           THREE pyrimidines = porphyrin (same!)")
print(f"  5 + 5 + 5 = 15:          THREE indoles = 613 THz (same as por+wat!)")
print(f"  6 + 9 = 15:              water + porphyrin = 613 THz")
print(f"")
print(f"  THEREFORE: 3+3 = wat, 3+wat = por, por+wat = 613 THz")
print(f"  The WHOLE CHAIN: 3 → 6 → 9 → 15")
print(f"  Each step adds 3 (triality)! [3, 3+3=6, 6+3=9, 9+6=15]")
print(f"  Or: 3, 2×3, 3×3, 5×3")
print(f"  Multipliers: 1, 2, 3, 5 = F(1), F(3), F(4), F(5)")
print(f"  Wait — that's Fibonacci!")

print(f"\n  Let's check the FIBONACCI-MULTIPLIED triality chain:")
for k in range(1, 10):
    fk = F(k)
    n = 3 * fk
    fn = F(n)
    ln = L(n)
    decomps = find_decompositions(n, all_modes, max_terms=4)
    has_path = "YES" if decomps else "no"

    match = ""
    for val, desc in KNOWN_QUANTITIES.items():
        if isinstance(val, int) and (fn == val or ln == val):
            if fn == val: match += f"F={desc} "
            if ln == val: match += f"L={desc} "

    print(f"  3×F({k}) = 3×{fk} = {n:>3}  F({n})={fn:>8}  L({n})={ln:>8}  reachable={has_path}  {match}")


# ============================================================
# FINAL: SUMMARY OF ALL HITS
# ============================================================
print("\n" + "=" * 80)
print("SUMMARY: ALL PHYSICAL/BIOLOGICAL MATCHES FROM COMPOSITION ALGEBRA")
print("=" * 80)

print("\n--- Pairwise hits ---")
for a, b, n, match in hits:
    print(f"  {a} + {b} = {n}: {match}")

print("\n--- Triple hits ---")
for combo, n, match in triple_hits:
    print(f"  {combo} = {n}: {match}")

print("\n--- Key ratio hits ---")
for n1, n2, typ, ratio, target, desc in sorted(set(ratio_hits)):
    print(f"  {typ}({n2})/{typ}({n1}) = {ratio:.4f} ~ {target} = {desc}")
