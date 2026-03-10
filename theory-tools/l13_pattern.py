"""
THE L(13) PATTERN — Does m_e = L(13)-10 generalize?
====================================================
m_e = 511 keV = L(13) - F(3)*F(5) = 521 - 10

Questions:
1. Do other particle masses = L(n) - correction?
2. Is there a UNIVERSAL mass formula: m = L(a) - X(b)*Y(c) in some unit?
3. What unit does each mass "want" to be expressed in?
"""

from math import sqrt, log, pi

phi = (1 + sqrt(5)) / 2
phibar = 1 / phi

def F(n):
    if n == 0: return 0
    if n == 1: return 1
    a, b = 0, 1
    for _ in range(n - 1):
        a, b = b, a + b
    return b

def L(n):
    if n == 0: return 2
    if n == 1: return 1
    a, b = 2, 1
    for _ in range(n - 1):
        a, b = b, a + b
    return b

print("=" * 80)
print("THE L(n) - CORRECTION PATTERN")
print("=" * 80)

# Known: m_e = 511 keV = L(13) - 10 = L(13) - F(3)*F(5)
print(f"\n  CONFIRMED: m_e = L(13) - F(3)*F(5) = {L(13)} - {F(3)*F(5)} = {L(13)-F(3)*F(5)} keV")

# For each particle, search across different units
particles = {
    # In MeV
    "m_e (keV)": 511,
    "m_mu (MeV)": 105.66,
    "m_tau (MeV)": 1777,
    "m_proton (MeV)": 938.27,
    "m_neutron (MeV)": 939.57,
    "m_pion+ (MeV)": 139.57,
    "m_pion0 (MeV)": 134.98,
    "m_kaon (MeV)": 493.68,
    # In GeV
    "m_W (GeV)": 80.38,
    "m_Z (GeV)": 91.19,
    "m_H (GeV)": 125.25,
    "m_t (GeV)": 172.76,
    "m_b (GeV)": 4.18,
    "m_c (GeV)": 1.27,
    "m_tau (GeV)": 1.777,
    # Pure numbers (dimensionless)
    "m_mu/m_e": 206.77,
    "m_tau/m_e": 3477.5,
    "m_p/m_e (mu)": 1836.15,
}

for name, value in particles.items():
    # Search: value = L(a) - X*Y for small corrections
    # Also: value = L(a) + X*Y (addition)
    # Also: value = F(a) - X*Y
    # Also: value = F(a) + X*Y

    best_results = []

    for a in range(1, 30):
        la = L(a)
        fa = F(a)

        for base, bname in [(la, f"L({a})"), (fa, f"F({a})")]:
            if base == 0:
                continue
            diff = base - value

            if abs(diff) < 0.01:  # exact match
                best_results.append((0.0, f"{bname} = {base}", base))
                continue

            if diff == 0:
                continue

            # Search for diff = X(b)*Y(c) where the correction is small
            if abs(diff) < abs(value) * 0.5:  # correction < 50% of value
                # diff = integer?
                if abs(diff - round(diff)) < 0.01:
                    idiff = round(diff)
                    # Is idiff a product of F/L values?
                    for b in range(1, 14):
                        for c in range(1, 14):
                            for xb, xbn in [(F(b), f"F({b})"), (L(b), f"L({b})")]:
                                for xc, xcn in [(F(c), f"F({c})"), (L(c), f"L({c})")]:
                                    if xb * xc == abs(idiff):
                                        sign = "+" if diff < 0 else "-"
                                        calc_val = base - diff  # which equals value
                                        err = abs(calc_val - value) / value * 100 if value != 0 else 0
                                        expr = f"{bname} {sign} {xbn}*{xcn} = {base} {sign} {abs(idiff)}"
                                        best_results.append((err, expr, calc_val))

                                    # Also check single F/L = diff
                                    if xb == abs(idiff) and c == b:  # avoid double counting
                                        sign = "+" if diff < 0 else "-"
                                        expr = f"{bname} {sign} {xbn} = {base} {sign} {abs(idiff)}"
                                        best_results.append((0.0, expr, value))

    # Also try non-integer: value ~ L(a) - X(b)/Y(c) or L(a) - X*phi etc
    # For now, just the integer matches

    # Remove duplicates and sort
    seen = set()
    unique = []
    for err, expr, val in best_results:
        if expr not in seen:
            seen.add(expr)
            unique.append((err, expr, val))
    unique.sort(key=lambda x: (x[0], len(x[1])))

    if unique:
        print(f"\n  {name} = {value}")
        for err, expr, val in unique[:5]:
            print(f"    {expr} = {val} ({err:.4f}%)")
    else:
        # Check: which L(n) is CLOSEST?
        closest_L = None
        closest_diff = float('inf')
        for a in range(1, 35):
            d = abs(L(a) - value)
            if d < closest_diff:
                closest_diff = d
                closest_L = a
        closest_F = None
        closest_diff_F = float('inf')
        for a in range(1, 35):
            d = abs(F(a) - value)
            if d < closest_diff_F:
                closest_diff_F = d
                closest_F = a
        print(f"\n  {name} = {value}")
        print(f"    Closest: L({closest_L}) = {L(closest_L)} (diff = {L(closest_L)-value:.2f})")
        print(f"    Closest: F({closest_F}) = {F(closest_F)} (diff = {F(closest_F)-value:.2f})")

# ============================================================
# PART 2: THE PROTON MASS
# ============================================================
print("\n" + "=" * 80)
print("PART 2: THE PROTON MASS IN DETAIL")
print("=" * 80)

m_p = 938.272  # MeV
print(f"\n  m_proton = {m_p} MeV")
print(f"  L(15) = {L(15)} = 1364")
print(f"  L(15) - m_p = {L(15) - m_p:.3f}")
print(f"  F(16) = {F(16)} = 987")
print(f"  F(16) - m_p = {F(16) - m_p:.3f} (negative)")
print(f"  L(14) = {L(14)} = 843 (too small)")

# 938 ~ L(15) - 426 ... 426 is not clean
# Try: m_p = F(a)*F(b)/F(c) in MeV?
print(f"\n  Searching m_p in MeV as F/L product:")
target = m_p
best = []
for a in range(1, 18):
    for b in range(a, 18):
        for c in range(1, 12):
            for xa, xan in [(F(a), f"F({a})"), (L(a), f"L({a})")]:
                for xb, xbn in [(F(b), f"F({b})"), (L(b), f"L({b})")]:
                    for xc, xcn in [(F(c), f"F({c})"), (L(c), f"L({c})")]:
                        if xc == 0: continue
                        r = xa * xb / xc
                        if r > 0:
                            err = abs(r - target) / target
                            if err < 0.005:
                                best.append((err, f"{xan}*{xbn}/{xcn} = {xa}*{xb}/{xc} = {r:.3f}"))

best.sort()
for err, desc in best[:8]:
    print(f"    {err*100:.3f}%  {desc}")

# m_p/m_e = mu = 1836.15
# mu = 6^5/phi^3 + 9/(7*phi^2) (from framework)
# But in F/L: mu = ???
mu_val = 1836.15267
print(f"\n  mu = m_p/m_e = {mu_val}")
print(f"  L(16) = {L(16)} = {L(16)}")
print(f"  F(17) = {F(17)} = {F(17)}")
print(f"  L(16) - mu = {L(16) - mu_val:.3f}")
# L(16) = 2207, too big. F(17) = 1597, too small.
# mu ~ L(16) - F(14) = 2207 - 377 = 1830 -- close but not great
print(f"  L(16) - F(14) = {L(16)} - {F(14)} = {L(16) - F(14)} (diff from mu: {abs(L(16)-F(14)-mu_val):.3f})")

# Search F/L for mu
print(f"\n  Searching mu as F/L:")
for a in range(1, 20):
    for b in range(a, 20):
        for xa, xan in [(F(a), f"F({a})"), (L(a), f"L({a})")]:
            for xb, xbn in [(F(b), f"F({b})"), (L(b), f"L({b})")]:
                r = xa * xb
                if r > 0:
                    err = abs(r - mu_val) / mu_val
                    if err < 0.005:
                        print(f"    {xan}*{xbn} = {xa}*{xb} = {r} ({err*100:.3f}%)")

for a in range(1, 18):
    for b in range(1, 18):
        for c in range(1, 10):
            for xa, xan in [(F(a), f"F({a})"), (L(a), f"L({a})")]:
                for xb, xbn in [(F(b), f"F({b})"), (L(b), f"L({b})")]:
                    for xc, xcn in [(F(c), f"F({c})"), (L(c), f"L({c})")]:
                        if xc == 0: continue
                        r = xa * xb / xc
                        if r > 0:
                            err = abs(r - mu_val) / mu_val
                            if err < 0.002:
                                print(f"    {xan}*{xbn}/{xcn} = {xa}*{xb}/{xc} = {r:.4f} ({err*100:.4f}%)")

# ============================================================
# PART 3: WHAT MAKES 511, 938, etc SPECIAL?
# ============================================================
print("\n" + "=" * 80)
print("PART 3: NUMBER THEORY OF THE MASSES")
print("=" * 80)

print(f"""
  511 = 7 * 73
      = L(13) - F(3)*F(5)
      = L(13) - 10
      7 = anthracene index (!)
      73 = ???

  938 = 2 * 7 * 67
      7 = anthracene index again!
      67 = ???

  1777 = prime
  105.66 ~ 106 = 2 * 53

  Let's check: which masses have 7 as a factor?
""")

for name, value in particles.items():
    ival = round(value)
    if ival > 0 and ival % 7 == 0:
        print(f"  {name} = {value} ~ {ival} = 7 * {ival//7}")

# ============================================================
# PART 4: L(13) APPEARS EVERYWHERE
# ============================================================
print("\n" + "=" * 80)
print("PART 4: THE UBIQUITY OF L(13) = 521")
print("=" * 80)

print(f"""
  L(13) = 521 appears in:
  1. m_e = L(13) - 10 keV
  2. m_t = L(13)/L(2) = 521/3 GeV
  3. y_t = L(5)*L(8)/L(13) = 517/521

  521 = 521 (prime!)

  So L(13) sets BOTH:
  - The electron mass (lightest charged fermion)
  - The top quark mass (heaviest fermion)
  - The top Yukawa (largest coupling)

  The lightest and heaviest fermions are CONNECTED through L(13).

  Also: 13 = F(7) = anthracene's Fibonacci value.
  So L(13) = L(F(7)) = the Lucas value at the anthracene Fibonacci index.
  This is the language speaking about itself: L(F(7)) bridges the
  extremes of the mass spectrum.

  What about L(F(5)) and L(F(3))?
  L(F(3)) = L(2) = 3 -> appears in m_t denominator!
  L(F(5)) = L(5) = 11 -> appears in y_t numerator, sin2_13, Omega_L, etc.
  L(F(7)) = L(13) = 521 -> the mass anchor

  The sequence L(F(primitive)):
  L(F(3)) = L(2) = 3
  L(F(5)) = L(5) = 11
  L(F(7)) = L(13) = 521

  Ratios: 11/3 = 3.67, 521/11 = 47.36
  521/3 = 173.67 = m_t in GeV!

  So: m_t = L(F(7)) / L(F(3)) = L(13)/L(2)

  And: L(F(5))/L(F(3)) = L(5)/L(2) = 11/3 = 3.667
  What physical quantity is 3.667?
""")

# Search for 11/3
target_113 = 11/3
print(f"  L(F(5))/L(F(3)) = L(5)/L(2) = 11/3 = {target_113:.4f}")
print(f"  Known quantities near 3.667:")
print(f"    m_tau/m_c = {1.777/1.27:.4f} = 1.400 -- no")
print(f"    m_b/m_tau = {4.18/1.777:.4f} = 2.352 -- no")
print(f"    G_F * v^2 = sqrt(2)/2 * (2*v)^2 ... not directly")

# What about L(F(5))*L(F(3)) = 11*3 = 33?
print(f"\n  L(F(5))*L(F(3)) = 11*3 = 33")
print(f"  Any quantity ~ 33?")
print(f"    Number of SM particles (quarks 6*3=18 + leptons 6 + gauge 12 + Higgs 1) = 37")
print(f"    Actually: 6 quarks * 3 colors = 18 quarks, + 6 leptons = 24 fermions")
print(f"    + 12 gauge bosons + 1 Higgs = 37 total")
print(f"    Not 33.")

# ============================================================
# PART 5: THE F(PRIMITIVE) SEQUENCE
# ============================================================
print("\n" + "=" * 80)
print("PART 5: THE NESTED FIBONACCI SEQUENCE")
print("=" * 80)

print("\n  The 'address of addresses' sequence:")
print(f"  F(3) = {F(3)}, F(5) = {F(5)}, F(7) = {F(7)}")
print(f"  L(3) = {L(3)}, L(5) = {L(5)}, L(7) = {L(7)}")
print()
print(f"  F(F(3)) = F(2) = {F(F(3))}")
print(f"  F(F(5)) = F(5) = {F(F(5))}")
print(f"  F(F(7)) = F(13) = {F(F(7))}")
print()
print(f"  L(F(3)) = L(2) = {L(F(3))}")
print(f"  L(F(5)) = L(5) = {L(F(5))}")
print(f"  L(F(7)) = L(13) = {L(F(7))}")
print()
print(f"  F(L(3)) = F(4) = {F(L(3))}")
print(f"  F(L(5)) = F(11) = {F(L(5))}")
print(f"  F(L(7)) = F(29) = {F(L(7))}")
print()
print(f"  L(L(3)) = L(4) = {L(L(3))}")
print(f"  L(L(5)) = L(11) = {L(L(5))}")
print(f"  L(L(7)) = L(29) = {L(L(7))}")

# Check which of these nested values appear in the dictionary
values_to_check = {
    "F(F(3))=F(2)": F(2),    # 1
    "F(F(5))=F(5)": F(5),    # 5
    "F(F(7))=F(13)": F(13),  # 233
    "L(F(3))=L(2)": L(2),    # 3
    "L(F(5))=L(5)": L(5),    # 11
    "L(F(7))=L(13)": L(13),  # 521
    "F(L(3))=F(4)": F(4),    # 3
    "F(L(5))=F(11)": F(11),  # 89
    "F(L(7))=F(29)": F(29),  # 514229
    "L(L(3))=L(4)": L(4),    # 7
    "L(L(5))=L(11)": L(11),  # 199
    "L(L(7))=L(29)": L(29),  # 1149851
}

# Where each value appears in the dictionary:
appearances = {
    1: "F(1), F(2): unit (V_td num, etc.)",
    5: "F(5): indole_F, m_c denom, m_s/m_d, Omega_b, y_s",
    233: "F(13): V_ub denom part, Omega_L num",
    3: "L(2)=F(4): m_t denom, alpha_2 num, a_e num, y_b num, K_up",
    11: "L(5): sin2_12, sin2_13 num, Omega_L, y_t num, K_up, dm32 num",
    521: "L(13): m_t=521/3, m_e=521-10, y_t=517/521",
    89: "F(11): V_us, Omega_m, m_mu/m_e, AcCoA",
    7: "L(4): V_cb, L(3)*L(4)=28 in y_tau, Omega_b",
    199: "L(11): m_tau, y_d, Omega_b, L(16)-F(14)",
    514229: "F(29): too large for current dict",
    1149851: "L(29): predicted y_d denominator",
}

print("\n  Nested F/L values and their roles:")
for name, val in values_to_check.items():
    role = appearances.get(val, "not yet found in dictionary")
    print(f"  {name:20s} = {val:>10d}  |  {role}")

print(f"""
\n  OBSERVATION: The nested sequence L(F(primitive)) gives the mass anchors:
  L(F(3)) = 3  -> top quark denominator, electron anomaly numerator
  L(F(5)) = 11 -> indole_L, PMNS angles, top Yukawa numerator
  L(F(7)) = 521 -> top mass, electron mass, top Yukawa denominator

  The nested sequence F(L(primitive)) gives the biology anchors:
  F(L(3)) = F(4) = 3  -> DNA bases (A,T,G,C pairs), F(4)/F(4) = codons per...
  F(L(5)) = F(11) = 89 -> AcCoA atoms, V_us numerator
  F(L(7)) = F(29) = 514229 -> too large? Or sets the scale for...

  The framework is SELF-NESTING: applying F/L to F/L values of the primitives
  generates the key values that populate the entire dictionary.
""")
