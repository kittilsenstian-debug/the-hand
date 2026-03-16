#!/usr/bin/env python3
"""
algebraic_periodic_table.py — The periodic table as E8 weight diagram
======================================================================

Every element Z=1-92 written in algebraic notation.
Tests whether chemically distinguished elements cluster on E8 dimensions.

Questions:
  1. Do noble gases have algebraically special Z?
  2. Do the elements of life (C,N,O,P,S,Fe) land on E8 dimensions?
  3. Do electron shell capacities (2,8,18,32) decompose algebraically?
  4. Do period lengths and group structures reflect E8 branching?
  5. Is there a representation-theoretic reason for the periodic table's shape?

python -X utf8 algebraic_periodic_table.py
"""

import sys, io, math

try:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
except:
    pass

# =====================================================================
# ALGEBRAIC DATA
# =====================================================================

ALLOWED = {
    1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 14, 15, 16, 18, 20, 21, 24,
    26, 27, 28, 30, 33, 36, 37, 40, 43, 45, 48, 52, 54, 56, 60,
    64, 67, 71, 72, 78, 80, 120, 126, 133, 240, 248, 744
}

# Algebraic sources for key numbers
SOURCES = {
    1: "unity", 2: "Z2/vacua", 3: "rep(SM)/triality", 4: "rank(A4)",
    5: "rank(D5)", 6: "rank(E6)", 7: "rank(E7)", 8: "rank(E8)",
    10: "rep(D5)", 12: "h(E6)", 14: "dim(G2)", 15: "dim(su(4))",
    16: "rep(D5)", 18: "h(E7)", 20: "roots(A4)", 21: "dim(so(7))",
    24: "dim(A4)", 26: "|sporadic|", 27: "rep(E6)/J3(O)",
    28: "dim(so(8))/2.Ru", 30: "h(E8)", 33: "3*L(5)",
    36: "dim(so(9))", 37: "pariah J1", 40: "roots(D5)",
    43: "pariah J4", 45: "dim(D5)", 48: "240/5",
    52: "dim(F4)", 54: "2*J3(O)", 56: "rep(E7)",
    60: "240/4", 64: "4^3", 67: "pariah O'N", 71: "pariah Ly",
    72: "roots(E6)", 78: "dim(E6)", 80: "240/3",
    120: "240/2", 126: "roots(E7)", 133: "dim(E7)",
}

def alg_score(n):
    if n in ALLOWED:
        return 3, "EXACT", SOURCES.get(n, "")
    for a in sorted(ALLOWED):
        if a < 2: continue
        if a * a > n: break
        if n % a == 0:
            b = n // a
            if b in ALLOWED and b >= a:
                return 2, "PROD", f"{a}*{b}"
    for a in sorted(ALLOWED):
        if a >= n: break
        b = n - a
        if b in ALLOWED and b >= a:
            return 1, "SUM", f"{a}+{b}"
    return 0, "MISS", ""

# =====================================================================
# ELEMENT DATA
# =====================================================================

SYMBOLS = [
    "", "H","He","Li","Be","B","C","N","O","F","Ne",
    "Na","Mg","Al","Si","P","S","Cl","Ar","K","Ca",
    "Sc","Ti","V","Cr","Mn","Fe","Co","Ni","Cu","Zn",
    "Ga","Ge","As","Se","Br","Kr","Rb","Sr","Y","Zr",
    "Nb","Mo","Tc","Ru","Rh","Pd","Ag","Cd","In","Sn",
    "Tl","Sb","Te","I","Xe","Cs","Ba","La","Ce","Pr",
    "Nd","Pm","Sm","Eu","Gd","Tb","Dy","Ho","Er","Tm",
    "Yb","Lu","Hf","Ta","W","Re","Os","Ir","Pt","Au",
    "Hg","Tl","Pb","Bi","Po","At","Rn","Fr","Ra","Ac",
    "Th","Pa","U"
]

# Chemical categories
NOBLE_GASES = {2, 10, 18, 36, 54, 86}
ALKALI_METALS = {3, 11, 19, 37, 55, 87}
ALKALINE_EARTH = {4, 12, 20, 38, 56, 88}
HALOGENS = {9, 17, 35, 53, 85}
LIFE_ELEMENTS = {1, 6, 7, 8, 15, 16, 26, 20}  # H,C,N,O,P,S,Fe,Ca
TRANSITION_METALS = set(range(21, 31)) | set(range(39, 49)) | set(range(72, 81))
LANTHANIDES = set(range(57, 72))

# Most abundant stable isotope mass numbers (approximate)
STABLE_A = {
    1:1, 2:4, 3:7, 4:9, 5:11, 6:12, 7:14, 8:16, 9:19, 10:20,
    11:23, 12:24, 13:27, 14:28, 15:31, 16:32, 17:35, 18:40, 19:39, 20:40,
    21:45, 22:48, 23:51, 24:52, 25:55, 26:56, 27:59, 28:58, 29:63, 30:64,
    31:69, 32:74, 33:75, 34:80, 35:79, 36:84, 37:85, 38:88, 39:89, 40:90,
    41:93, 42:98, 43:98, 44:102, 45:103, 46:106, 47:107, 48:114, 49:115, 50:120,
    51:121, 52:130, 53:127, 54:132, 55:133, 56:138, 57:139, 58:140, 59:141, 60:142,
    61:145, 62:152, 63:153, 64:158, 65:159, 66:164, 67:165, 68:166, 69:169, 70:174,
    71:175, 72:180, 73:181, 74:184, 75:187, 76:192, 77:193, 78:195, 79:197, 80:202,
    81:205, 82:208, 83:209, 84:209, 85:210, 86:222, 87:223, 88:226, 89:227, 90:232,
    91:231, 92:238,
}

def header(t):
    print(f"\n{'='*78}")
    print(f"  {t}")
    print(f"{'='*78}")


def main():
    print("=" * 78)
    print("  THE ALGEBRAIC PERIODIC TABLE")
    print("  Every element as an E8 address")
    print("=" * 78)

    # ---------------------------------------------------------------
    # FULL TABLE
    # ---------------------------------------------------------------
    header("COMPLETE TABLE: Z=1-92")

    all_data = []
    for Z in range(1, 93):
        A = STABLE_A.get(Z, 2*Z)
        N = A - Z
        zs, zt, zd = alg_score(Z)
        ns, nt, nd = alg_score(N)
        a_sc, at, ad = alg_score(A)

        cat = ""
        if Z in NOBLE_GASES: cat = "noble"
        elif Z in ALKALI_METALS: cat = "alkali"
        elif Z in ALKALINE_EARTH: cat = "alk-earth"
        elif Z in HALOGENS: cat = "halogen"
        elif Z in LIFE_ELEMENTS: cat = "LIFE"
        elif Z in LANTHANIDES: cat = "lanthanide"

        all_data.append({
            "Z": Z, "sym": SYMBOLS[Z] if Z < len(SYMBOLS) else "?",
            "A": A, "N": N,
            "zs": zs, "zt": zt, "zd": zd,
            "ns": ns, "nt": nt, "nd": nd,
            "as": a_sc, "at": at, "ad": ad,
            "total": zs + ns + a_sc, "cat": cat,
        })

    # Print compact table
    print(f"\n  {'Z':>3s} {'Sym':>3s} {'A':>4s}  {'Z-type':>7s} {'Z-source':>15s}  "
          f"{'N':>3s} {'N-type':>7s}  {'A-type':>7s}  {'Tot':>3s} {'Category':>10s}")
    print("  " + "-" * 78)

    for d in all_data:
        src = d["zd"][:15] if d["zd"] else d["zt"]
        marker = ""
        if d["zs"] == 3: marker = " <--"
        print(f"  {d['Z']:>3d} {d['sym']:>3s} {d['A']:>4d}  {d['zt']:>7s} {src:>15s}  "
              f"{d['N']:>3d} {d['nt']:>7s}  {d['at']:>7s}  {d['total']:>3d}/9 {d['cat']:>10s}{marker}")

    # ---------------------------------------------------------------
    # NOBLE GASES
    # ---------------------------------------------------------------
    header("NOBLE GASES — Complete electron shells")

    print(f"\n  Noble gases have completely filled electron shells.")
    print(f"  If shell closure = representation completion, noble Z should be algebraic.\n")

    print(f"  {'Gas':>4s}  {'Z':>3s}  {'Score':>5s}  {'Type':>7s}  {'Source':>20s}  {'Shell config':>20s}")
    noble_data = [
        (2, "He", "1s2"),
        (10, "Ne", "2p6"),
        (18, "Ar", "3p6"),
        (36, "Kr", "4p6"),
        (54, "Xe", "5p6"),
        (86, "Rn", "6p6"),
    ]

    noble_exact = 0
    noble_any = 0
    for Z, sym, config in noble_data:
        s, t, d = alg_score(Z)
        if s == 3: noble_exact += 1
        if s > 0: noble_any += 1
        src = d if d else t
        print(f"  {sym:>4s}  {Z:>3d}  {s:>5d}/3  {t:>7s}  {src:>20s}  [{config}]")

    print(f"\n  {noble_exact}/6 noble gas Z are EXACT allowed integers")
    print(f"  {noble_any}/6 have any algebraic decomposition")

    # Shell closures: cumulative electrons
    print(f"\n  Shell closure pattern:")
    print(f"  He(2) = 2")
    print(f"  Ne(10) = 2 + 8")
    print(f"  Ar(18) = 2 + 8 + 8")
    print(f"  Kr(36) = 2 + 8 + 18 + 8   (but Madelung: 2+8+8+18)")
    print(f"  Xe(54) = 2 + 8 + 18 + 18 + 8   (Madelung: 2+8+8+18+18)")
    print(f"  Rn(86) = ... + 32")

    # Differences between noble gases
    diffs = [10-2, 18-10, 36-18, 54-36, 86-54]
    print(f"\n  Differences between consecutive noble gases:")
    for i, diff in enumerate(diffs):
        s, t, d = alg_score(diff)
        src = d if d else t
        prev = [2,10,18,36,54][i]
        nxt = [10,18,36,54,86][i]
        print(f"    {nxt} - {prev} = {diff}  [{t}: {src}]")

    # ---------------------------------------------------------------
    # ELECTRON SHELLS AS REPRESENTATIONS
    # ---------------------------------------------------------------
    header("ELECTRON SHELLS AS REPRESENTATIONS")

    print(f"\n  Shell capacity = 2n^2 for quantum number n")
    print(f"  The factor 2 = Z2 (spin degeneracy = vacua).\n")

    shells = [
        (1, 2, "K", "1s"),
        (2, 8, "L", "2s,2p"),
        (3, 18, "M", "3s,3p,3d"),
        (4, 32, "N", "4s,4p,4d,4f"),
    ]

    print(f"  {'Shell':>5s} {'n':>2s}  {'2n^2':>4s}  {'n^2':>3s}  {'Alg(2n^2)':>12s}  {'Alg(n^2)':>12s}  {'Subshells':>15s}")
    for n, cap, name, subs in shells:
        nsq = n * n
        cs, ct, cd = alg_score(cap)
        ns, nt, nd = alg_score(nsq)
        c_src = cd if cd else ct
        n_src = nd if nd else nt
        print(f"  {name:>5s} {n:>2d}  {cap:>4d}  {nsq:>3d}  {c_src:>12s}  {n_src:>12s}  {subs:>15s}")

    # Subshell capacities
    print(f"\n  Subshell capacities = 2(2l+1) for angular momentum l:")
    subshells = [
        ("s", 0, 2),
        ("p", 1, 6),
        ("d", 2, 10),
        ("f", 3, 14),
    ]
    print(f"  {'Type':>4s} {'l':>2s} {'2(2l+1)':>7s}  {'Alg':>12s}  {'Source':>20s}")
    for name, l, cap in subshells:
        s, t, d = alg_score(cap)
        src = d if d else t
        print(f"  {name:>4s} {l:>2d} {cap:>7d}  {t:>12s}  {src:>20s}")

    # ---------------------------------------------------------------
    # PERIOD LENGTHS
    # ---------------------------------------------------------------
    header("PERIOD LENGTHS — Madelung filling order")

    print(f"\n  Period lengths (number of elements per row):")
    periods = [2, 8, 8, 18, 18, 32, 32]
    for i, p in enumerate(periods):
        s, t, d = alg_score(p)
        src = d if d else t
        print(f"  Period {i+1}: {p:>3d} elements  [{t}: {src}]")

    print(f"\n  Unique period lengths: {{2, 8, 18, 32}}")
    print(f"  = {{2*1^2, 2*2^2, 2*3^2, 2*4^2}} = 2n^2")
    print(f"  Each appears TWICE (except 2), giving the doubled structure.")
    print(f"  The doubling = Z2 action (spin up/down fills same orbitals)")

    # ---------------------------------------------------------------
    # ELEMENTS OF LIFE
    # ---------------------------------------------------------------
    header("ELEMENTS OF LIFE")

    life = [
        (1, "H", "most abundant, simplest"),
        (6, "C", "all organic chemistry, hexagonal rings"),
        (7, "N", "DNA bases, amino groups, information"),
        (8, "O", "water, respiration, substrate"),
        (15, "P", "DNA backbone, ATP energy"),
        (16, "S", "disulfide bonds, redox"),
        (20, "Ca", "bones, signaling, structure"),
        (26, "Fe", "hemoglobin, electron transport"),
    ]

    print(f"\n  {'Z':>3s} {'Sym':>3s}  {'Score':>5s} {'Type':>7s} {'Source':>20s}  Role")
    exact_life = 0
    for Z, sym, role in life:
        s, t, d = alg_score(Z)
        src = d if d else t
        if s == 3: exact_life += 1
        print(f"  {Z:>3d} {sym:>3s}  {s:>5d}/3 {t:>7s} {src:>20s}  {role}")

    print(f"\n  {exact_life}/{len(life)} life elements have Z EXACTLY in the allowed set")

    # Compare to non-life elements in same range
    non_life_in_range = [Z for Z in range(1, 27) if Z not in {z for z, _, _ in life}]
    non_exact = sum(1 for Z in non_life_in_range if alg_score(Z)[0] == 3)
    print(f"  Non-life elements Z=1-26: {non_exact}/{len(non_life_in_range)} exact")

    # ---------------------------------------------------------------
    # CHEMICALLY SPECIAL ELEMENTS ON ALGEBRAIC DIMENSIONS
    # ---------------------------------------------------------------
    header("WHICH ALGEBRAIC DIMENSIONS ARE CHEMICALLY SPECIAL?")

    print(f"\n  For each Z in the allowed set (up to 92), what element is it?\n")

    print(f"  {'Z':>3s} {'Sym':>3s}  {'Algebraic source':>25s}  {'Chemical property':>40s}")
    print("  " + "-" * 78)

    special_props = {
        1: "Simplest. Most abundant in universe.",
        2: "Noble gas. First complete shell.",
        3: "Lightest alkali metal. One valence e-.",
        4: "Alkaline earth. Rigid, light, toxic.",
        5: "Metalloid. Boron clusters = icosahedra.",
        6: "Organic chemistry. Hexagonal rings. Life.",
        7: "DNA bases. Triple bond N2. Information.",
        8: "Most abundant in crust. Water. Substrate.",
        10: "Noble gas. Complete L shell.",
        12: "Chlorophyll center. Lightweight structural.",
        14: "Silicon. Semiconductors. Second C analog.",
        15: "DNA backbone. ATP. Energy currency.",
        16: "Disulfide bonds. Redox chemistry.",
        18: "Noble gas. Complete M-like shell.",
        20: "Bones, teeth, signaling. Structure.",
        21: "First transition metal (Sc).",
        24: "Chromium. Catalysis, stainless steel.",
        26: "Iron. Hemoglobin. Endpoint of fusion.",
        27: "Cobalt. B12 vitamin center.",
        28: "Nickel. Doubly magic nucleus.",
        30: "Zinc. Enzyme cofactor. Zinc fingers (DNA binding).",
        33: "Arsenic. Toxic. Phosphorus mimic.",
        36: "Noble gas (Kr). Complete N-like shell.",
        37: "Rubidium. Alkali metal. Atomic clocks.",
        40: "Zirconium. Refractory. Nuclear fuel cladding.",
        43: "Technetium. NO stable isotopes. All radioactive.",
        45: "Rhodium. Rarest stable element. Catalysis.",
        48: "Cadmium. Toxic. Zinc group.",
        52: "Tellurium. Chalcogen. Semiconductor.",
        54: "Xenon. Noble gas. General anesthetic.",
        56: "Barium. Alkaline earth. Dense.",
        60: "Neodymium. Strongest permanent magnets.",
        64: "Gadolinium. MRI contrast. Highest neutron capture.",
        67: "Holmium. Highest magnetic moment of any element.",
        71: "Lutetium. Last lanthanide. PET scanners.",
        72: "Hafnium. Nuclear reactor control. Zr twin.",
        78: "Platinum. Noblest metal. Catalysis.",
        80: "Mercury. ONLY liquid metal. Transformer.",
    }

    for Z in sorted(ALLOWED):
        if Z > 92 or Z == 0:
            continue
        sym = SYMBOLS[Z] if Z < len(SYMBOLS) else "?"
        src = SOURCES.get(Z, "")
        prop = special_props.get(Z, "")
        marker = ""
        if Z in NOBLE_GASES: marker = " [NOBLE]"
        elif Z in LIFE_ELEMENTS: marker = " [LIFE]"
        elif Z == 43: marker = " [NO STABLE ISOTOPES]"
        elif Z == 80: marker = " [ONLY LIQUID METAL]"
        elif Z == 78: marker = " [NOBLEST METAL]"
        elif Z == 67: marker = " [MAX MAGNETIC]"
        print(f"  {Z:>3d} {sym:>3s}  {src:>25s}  {prop[:40]}{marker}")

    # ---------------------------------------------------------------
    # THE PARIAH ELEMENTS
    # ---------------------------------------------------------------
    header("PARIAH ELEMENTS — Elements at pariah primes")

    pariah_elements = [
        (37, "Rb", "J1", "GF(11)", "Alkali metal. Atomic clocks. Time itself."),
        (43, "Tc", "J4", "GF(2)", "NO stable isotopes. Self-reference impossible = no stability."),
        (67, "Ho", "O'N", "all Q(sqrt(D))", "Highest magnetic moment. Universal sensitivity."),
        (71, "Lu", "Ly", "GF(5)", "Last lanthanide. Boundary of the f-block."),
    ]

    print(f"\n  Four elements sit at pariah-group numbers:\n")
    for Z, sym, pariah, field, prop in pariah_elements:
        print(f"  Z={Z} ({sym}) = {pariah} [{field}]")
        print(f"    {prop}")
        print()

    print(f"  Technetium (Z=43 = J4) is the LIGHTEST element with")
    print(f"  NO stable isotopes. J4 is where self-reference is IMPOSSIBLE.")
    print(f"  An element that cannot be stable at the number where")
    print(f"  self-reference cannot hold.")
    print()
    print(f"  Holmium (Z=67 = O'N) has the highest magnetic moment")
    print(f"  of any element. O'N ranges over ALL imaginary quadratic fields.")
    print(f"  Maximum magnetic response at universal sensitivity.")

    # ---------------------------------------------------------------
    # TRANSITION METAL d-BLOCK STRUCTURE
    # ---------------------------------------------------------------
    header("d-BLOCK STRUCTURE (transition metals)")

    print(f"\n  First transition series: Z=21-30 (Sc to Zn)")
    print(f"  10 elements filling d-orbitals. 10 = rep(D5).\n")

    for Z in range(21, 31):
        s, t, d = alg_score(Z)
        sym = SYMBOLS[Z]
        src = d if d else t
        in_set = "EXACT" if s == 3 else ("prod/sum" if s > 0 else "miss")
        print(f"  Z={Z:>2d} ({sym:>2s})  {in_set:>8s}  {src}")

    exact_d1 = sum(1 for Z in range(21, 31) if alg_score(Z)[0] == 3)
    print(f"\n  {exact_d1}/10 first-row d-metals are EXACT allowed integers")

    # ---------------------------------------------------------------
    # ELECTRON SHELL DERIVATION ATTEMPT
    # ---------------------------------------------------------------
    header("SHELL STRUCTURE FROM E8 BRANCHING")

    print(f"""
  The shell capacities 2, 8, 18, 32 = 2n^2 for n=1,2,3,4.

  Standard explanation: angular momentum l = 0..n-1 gives
  (2l+1) orbitals per subshell, 2 electrons per orbital (spin).
  Sum = 2 * sum(2l+1, l=0..n-1) = 2n^2.

  Algebraic reading:

  n=1: capacity 2 = Z2 (vacua). The simplest shell.
       One subshell: s (l=0), 2 electrons.

  n=2: capacity 8 = rank(E8). The substrate dimension.
       Two subshells: s(2) + p(6).
       6 = rank(E6) = order(S3).

  n=3: capacity 18 = h(E7). Coxeter number of E7.
       Three subshells: s(2) + p(6) + d(10).
       10 = rep(D5). Ten d-orbitals-worth of electrons.

  n=4: capacity 32 = 4 * 8 = rank(A4) * rank(E8).
       Four subshells: s(2) + p(6) + d(10) + f(14).
       14 = dim(G2). Fourteen f-orbitals-worth of electrons.

  The subshell capacities {{2, 6, 10, 14}} = {{2(2l+1)}} for l=0,1,2,3.

  Algebraic decomposition:
    s:  2 = Z2 (vacua)
    p:  6 = rank(E6) = |S3|
    d: 10 = rep(D5) = spinor dimension
    f: 14 = dim(G2) = automorphisms of octonions

  These are NOT random Lie algebra dimensions. They follow
  the COMPLEMENTARY chain within E8:
    G2 (14) is the automorphism group of the octonions
    D5 (10) is the spinor group SO(10)
    E6 (6 as rank) is the first exceptional algebra containing D5
    Z2 (2) is the fundamental binary

  The subshell sequence s,p,d,f maps to:
    vacua -> permutations -> spinors -> octonion automorphisms
""")

    # ---------------------------------------------------------------
    # CUMULATIVE ANALYSIS
    # ---------------------------------------------------------------
    header("CUMULATIVE STATISTICS")

    categories = {
        "Noble gases": NOBLE_GASES,
        "Alkali metals": ALKALI_METALS,
        "Alkaline earth": ALKALINE_EARTH,
        "Halogens": HALOGENS,
        "Life elements": {z for z, _, _ in life},
        "1st d-block": set(range(21, 31)),
        "Lanthanides": LANTHANIDES,
        "All Z=1-92": set(range(1, 93)),
    }

    print(f"\n  {'Category':>20s}  {'Count':>5s}  {'Exact':>5s}  {'Any':>5s}  "
          f"{'%Exact':>6s}  {'%Any':>6s}  {'Expected%':>9s}")
    print("  " + "-" * 72)

    # Expected rate: fraction of integers 1-92 in allowed set
    allowed_up_to_92 = len([x for x in ALLOWED if 1 <= x <= 92])
    expected_rate = allowed_up_to_92 / 92

    for cat_name, cat_set in categories.items():
        cat_set_bounded = {z for z in cat_set if 1 <= z <= 92}
        n = len(cat_set_bounded)
        exact = sum(1 for z in cat_set_bounded if alg_score(z)[0] == 3)
        any_match = sum(1 for z in cat_set_bounded if alg_score(z)[0] > 0)
        pct_exact = exact / n * 100 if n > 0 else 0
        pct_any = any_match / n * 100 if n > 0 else 0
        print(f"  {cat_name:>20s}  {n:>5d}  {exact:>5d}  {any_match:>5d}  "
              f"{pct_exact:>5.1f}%  {pct_any:>5.1f}%  {expected_rate*100:>8.1f}%")

    print(f"\n  Base rate: {allowed_up_to_92} of 92 integers (1-92) are in the allowed set = {expected_rate*100:.1f}%")

    # ---------------------------------------------------------------
    # THE FORBIDDEN ELEMENTS
    # ---------------------------------------------------------------
    header("MISSES: Elements with Z not decomposable at all")

    misses = [d for d in all_data if d["zs"] == 0]
    print(f"\n  {len(misses)} elements have Z with no algebraic decomposition:\n")
    for d in misses:
        print(f"  Z={d['Z']:>3d} ({d['sym']:>2s})")

    if not misses:
        print(f"  NONE. Every element Z=1-92 has Z in the allowed set or decomposable.")

    print(f"\n{'='*78}")
    print(f"  DONE")
    print(f"{'='*78}")


if __name__ == "__main__":
    main()
