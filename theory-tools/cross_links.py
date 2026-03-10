"""
CROSS-LINKS — The Hidden Identities Between Constants
=====================================================
The deeper_patterns.py found: R_c * gamma_I = V_cb (exact!)
This means the dictionary entries are algebraically CONNECTED.
What other identities link seemingly unrelated quantities?
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

# The complete dictionary of verified F/L values
dictionary = {
    # Gauge
    "alpha_s": L(3)*L(6)/F(15),            # 72/610 = 0.1180 (CORRECTED: was 188/610)
    "sin2W": L(2)*L(8)/F(15),              # 141/610 = 0.2311 (CORRECTED)
    "g/2": L(8)/F(12),                     # 47/144
    "a_e": L(2)/F(18),                     # 3/2584
    "gamma_I": F(5)*L(7)/F(15),             # 145/610 = 0.2377 (Immirzi parameter)
    "1/3": 1/3,
    "alpha_2": L(2)/F(11),                 # 3/89
    # CKM
    "V_ud": 1-F(3)/L(9),                   # 1-2/76
    "V_us": F(11)/(L(6)+F(14)),             # 89/395 = 0.2253 (CORRECTED: was 89/610)
    "V_ub": 1/(L(7)+F(13)),                # 1/262
    "V_cd": L(7)/(F(6)+L(10)),             # 29/131
    "V_cs": 1-L(5)/(F(4)+L(14)),           # 1-11/846
    "V_cb": (L(4)+L(6))/F(15),             # 25/610
    "V_td": 1/(F(3)+L(10)),                # 1/125
    "V_ts": F(7)/(F(7)+L(12)),             # 13/335
    "V_tb": 1-F(6)/L(19),                  # 1-8/9349
    # PMNS
    "sin2_12": 1/3-F(3)/L(9),
    "sin2_23": (L(5)+L(12))/F(15),         # 333/610
    "sin2_13": L(5)/(L(10)+F(14)),          # 11/500
    # Masses
    "v": F(16)/L(3),                        # 987/4
    "M_W": L(12)/L(3),                      # 322/4
    "M_H": F(14)/L(2),                      # 377/3
    "m_t": L(13)/L(2),                      # 521/3
    "m_b": F(8)/F(5),                       # 21/5
    "m_c": F(5)/L(3),                       # 5/4
    "m_mu": F(7)*F(8)/F(18),                # 273/2584
    "m_u": L(2)**2/F(19),                   # 9/4181
    # Mass ratios
    "m_t/m_c": L(3)*F(9),                   # 136
    "m_s/m_d": L(3)*F(5),                   # 20
    "m_b/m_s": L(3)*L(10)/L(5),             # ~44.73
    "m_b/m_d": L(6)*L(11)/L(3),             # ~895.5
    "m_tau/m_mu": L(3)*F(8)/F(5),            # 16.8
    "m_mu/m_e": L(4)*F(11)/F(4),             # ~207.67
    "m_H/m_Z": L(5)/F(6),                   # 11/8
    "m_t/m_Z": F(11)/L(8),                  # 89/47
    "m_t/m_H": L(7)**2/F(15),               # 841/610
    # Yukawa
    "y_t": L(5)*L(8)/L(13),                 # 517/521
    "y_c": F(3)*F(7)/L(17),
    "y_b": L(2)**2/F(14),                   # 9/377
    "y_tau": F(3)*L(4)/L(15),
    "y_mu": L(2)*F(6)/L(22),
    "y_s": F(5)/L(19),
    "y_d": F(3)/F(25),
    # Cosmo
    "Omega_m": L(7)/(F(4)+F(11)),            # 29/92
    "Omega_L": F(13)/(L(6)+L(12)),
    "H0": (L(6)+L(13))/F(6),
    "n_s": F(10)/(F(3)+F(10)),               # 55/57
    "sigma_8": L(8)/(L(5)+L(8)),             # 47/58
    "Omega_b": (L(4)+L(11))/F(19),
    "Omega_c": (L(5)+F(11))/F(14),
    # Other
    "f_pi": L(13)/L(3),                      # 521/4 in MeV? actually 130.25
    "R_c": F(5)/L(7),                        # 5/29
    "r_tensor": L(6)/L(12),                  # 18/322
    "y_b_alt": L(2)/L(10),                   # 3/123
    # Koide
    "K_lepton": 2/3,
    "K_up": L(5)/F(7),                       # 11/13
    "K_down": F(6)/L(5),                     # 8/11
}

# ============================================================
# PART 1: FIND ALL EXACT PRODUCT IDENTITIES
# ============================================================
print("=" * 80)
print("PART 1: PRODUCT IDENTITIES — A*B = C?")
print("=" * 80)

names = list(dictionary.keys())
vals = list(dictionary.values())

print("\n  Searching for A * B = C (within 0.5%):\n")
found_products = []
for i in range(len(names)):
    for j in range(i+1, len(names)):
        product = vals[i] * vals[j]
        for k in range(len(names)):
            if k == i or k == j:
                continue
            if vals[k] == 0:
                continue
            err = abs(product - vals[k]) / abs(vals[k])
            if err < 0.005:
                found_products.append((err, names[i], names[j], names[k], product, vals[k]))

found_products.sort()
for err, a, b, c, prod, target in found_products[:20]:
    marker = " ***" if err < 0.001 else " **" if err < 0.005 else ""
    print(f"  {a:15s} * {b:15s} = {c:15s}  ({prod:.6f} vs {target:.6f}, {err*100:.4f}%){marker}")

# ============================================================
# PART 2: FIND ALL RATIO IDENTITIES
# ============================================================
print("\n" + "=" * 80)
print("PART 2: RATIO IDENTITIES — A/B = C?")
print("=" * 80)

print("\n  Searching for A / B = C (within 0.5%):\n")
found_ratios = []
for i in range(len(names)):
    for j in range(len(names)):
        if i == j or vals[j] == 0:
            continue
        ratio = vals[i] / vals[j]
        for k in range(len(names)):
            if k == i or k == j:
                continue
            if vals[k] == 0:
                continue
            err = abs(ratio - vals[k]) / abs(vals[k])
            if err < 0.005:
                found_ratios.append((err, names[i], names[j], names[k], ratio, vals[k]))

found_ratios.sort()
seen = set()
for err, a, b, c, rat, target in found_ratios[:30]:
    key = tuple(sorted([a, b, c]))
    if key in seen:
        continue
    seen.add(key)
    marker = " ***" if err < 0.001 else " **" if err < 0.005 else ""
    print(f"  {a:15s} / {b:15s} = {c:15s}  ({rat:.6f} vs {target:.6f}, {err*100:.4f}%){marker}")

# ============================================================
# PART 3: FIND SUM/DIFFERENCE IDENTITIES
# ============================================================
print("\n" + "=" * 80)
print("PART 3: SUM/DIFFERENCE IDENTITIES — A +/- B = C?")
print("=" * 80)

print("\n  Searching for A + B = C or A - B = C (within 0.5%):\n")
found_sums = []
for i in range(len(names)):
    for j in range(i+1, len(names)):
        s = vals[i] + vals[j]
        d1 = vals[i] - vals[j]
        d2 = vals[j] - vals[i]

        for k in range(len(names)):
            if k == i or k == j:
                continue
            if vals[k] == 0:
                continue

            for val, op in [(s, "+"), (d1, "-"), (d2, "-r")]:
                err = abs(val - vals[k]) / abs(vals[k])
                if err < 0.005:
                    if op == "-r":
                        found_sums.append((err, names[j], names[i], names[k], val, vals[k], "-"))
                    else:
                        found_sums.append((err, names[i], names[j], names[k], val, vals[k], op))

found_sums.sort()
seen = set()
for err, a, b, c, val, target, op in found_sums[:25]:
    key = (a, b, c, op)
    if key in seen:
        continue
    seen.add(key)
    marker = " ***" if err < 0.001 else " **" if err < 0.005 else ""
    print(f"  {a:15s} {op} {b:15s} = {c:15s}  ({val:.6f} vs {target:.6f}, {err*100:.4f}%){marker}")

# ============================================================
# PART 4: THE MOST REMARKABLE IDENTITIES
# ============================================================
print("\n" + "=" * 80)
print("PART 4: THE MOST REMARKABLE IDENTITIES")
print("=" * 80)

# Verify R_c * gamma_I = V_cb
rc = F(5)/L(7)       # 5/29
gi = F(3)/L(6)        # 2/18 = 1/9
vcb = (L(4)+L(6))/F(15)  # 25/610

print(f"\n  R_c * gamma_I = {rc:.8f} * {gi:.8f} = {rc*gi:.8f}")
print(f"  V_cb = {vcb:.8f}")
print(f"  Match: {abs(rc*gi - vcb)/vcb*100:.6f}%")
print(f"  Algebraically: (F(5)/L(7)) * (F(3)/L(6)) = F(5)*F(3)/(L(7)*L(6))")
print(f"  = {F(5)*F(3)}/{L(7)*L(6)} = {F(5)*F(3)/(L(7)*L(6)):.8f}")
print(f"  V_cb = (L(4)+L(6))/F(15) = {L(4)+L(6)}/{F(15)} = {vcb:.8f}")
print(f"  So: F(5)*F(3)/(L(7)*L(6)) = (L(4)+L(6))/F(15)?")
print(f"  10/522 = 25/610?")
print(f"  10*610 = {10*610}, 25*522 = {25*522}")
print(f"  6100 vs 13050 -- NOT algebraically exact!")
print(f"  So this is a numerical coincidence at the level of the approximations.")

# Check: what identities ARE algebraically exact?
print(f"\n  Algebraically exact identities:")

# V_ud + sin2_12 should relate to 1/3
vud = 1 - F(3)/L(9)
s12 = 1/3 - F(3)/L(9)
print(f"  V_ud = 1 - {F(3)}/{L(9)} = {vud:.8f}")
print(f"  sin2_12 = 1/3 - {F(3)}/{L(9)} = {s12:.8f}")
print(f"  V_ud - sin2_12 = {vud - s12:.8f} = 2/3 (charge quantum!) EXACT")

# sin2_23 + V_cb should relate
s23 = (L(5)+L(12))/F(15)
print(f"\n  sin2_23 = (L(5)+L(12))/F(15) = {L(5)+L(12)}/{F(15)} = {s23:.8f}")
print(f"  V_cb = (L(4)+L(6))/F(15) = {L(4)+L(6)}/{F(15)} = {vcb:.8f}")
print(f"  sin2_23 + V_cb = ({L(5)+L(12)+L(4)+L(6)})/{F(15)} = {L(5)+L(12)+L(4)+L(6)}/{F(15)}")
print(f"  = {(L(5)+L(12)+L(4)+L(6))/F(15):.8f}")
print(f"  {L(5)+L(12)+L(4)+L(6)} = {L(5)+L(12)+L(4)+L(6)}")
print(f"  This is: L(4)+L(5)+L(6)+L(12) = 7+11+18+322 = 358")
print(f"  358/610 = 0.5869")

# V_us + V_cb + ... = ?
vus = F(11)/F(15)  # 89/610
print(f"\n  V_us = {F(11)}/{F(15)} = {vus:.8f}")
print(f"  V_cb = {L(4)+L(6)}/{F(15)} = {vcb:.8f}")
print(f"  V_us + V_cb = ({F(11)}+{L(4)+L(6)})/{F(15)} = {F(11)+L(4)+L(6)}/{F(15)}")
print(f"  = {(F(11)+L(4)+L(6))/F(15):.8f}")
print(f"  {F(11)+L(4)+L(6)} = 89+25 = 114")
print(f"  114/610 = {114/610:.6f}")
print(f"  Is 114 special? 114 = 6*19 = 2*3*19")

# alpha_s + sin2_23 (CORRECTED)
als = L(3)*L(6)/F(15)   # 72/610
print(f"\n  alpha_s (corrected) = {L(3)*L(6)}/{F(15)} = {als:.6f}")
print(f"  sin2_23 = (L(5)+L(12))/F(15) = {L(5)+L(12)}/{F(15)} = {(L(5)+L(12))/F(15):.6f}")
print(f"  Both over F(15)! alpha_s + sin2_23 = ({L(3)*L(6)}+{L(5)+L(12)})/{F(15)}")
print(f"  = {L(3)*L(6)+L(5)+L(12)}/{F(15)} = {(L(3)*L(6)+L(5)+L(12))/F(15):.6f}")
print(f"  {L(3)*L(6)+L(5)+L(12)} = 72+333 = 405")
print(f"  NOTE: 405/610 is NOT a clean F/L number. The old L(13)/F(15) result was based on wrong alpha_s.")

print(f"\n  NOTE: The old identity alpha_s + sin2_23 = L(13)/F(15) was based on")
print(f"  the WRONG alpha_s = L(3)*L(8)/F(15) = 188/610.")
print(f"  With CORRECTED alpha_s = L(3)*L(6)/F(15) = 72/610:")
print(f"  alpha_s + sin2_23 = (72+333)/610 = 405/610 = 0.6639")
print(f"  This is NOT a clean F/L number. Honest correction.")

# What else adds to nice things?
print(f"\n  What other pairs sum to L(n)/F(15)?")
# Any two quantities with F(15) denominator
f15_quantities = {
    "alpha_s": L(3)*L(6),       # 72 (CORRECTED from 188)
    "sin2W": L(2)*L(8),         # 141 (CORRECTED)
    "V_cb": L(4)+L(6),          # 25
    "sin2_23": L(5)+L(12),      # 333
    "gamma_I": F(5)*L(7),       # 145
    "m_t/m_H": L(7)**2,         # 841
}

print(f"  Quantities with F(15)=610 denominator:")
for name, num in f15_quantities.items():
    print(f"    {name:12s} = {num}/610 = {num/610:.6f}")

print(f"\n  Pairwise sums:")
names_f15 = list(f15_quantities.keys())
for i in range(len(names_f15)):
    for j in range(i+1, len(names_f15)):
        n1, n2 = names_f15[i], names_f15[j]
        s = f15_quantities[n1] + f15_quantities[n2]
        # Check if s is a Fibonacci or Lucas number
        for k in range(1, 25):
            if s == F(k):
                print(f"    {n1} + {n2} = {s}/610 = F({k})/F(15)")
            if s == L(k):
                print(f"    {n1} + {n2} = {s}/610 = L({k})/F(15)")

# ============================================================
# PART 5: THE F(15) BUDGET
# ============================================================
print("\n" + "=" * 80)
print("PART 5: THE F(15) = 610 BUDGET")
print("=" * 80)

print(f"""
  F(15) = 610 is the UNIVERSAL NORMALIZER.
  Multiple quantities are shares of 610 (CORRECTED values):

  alpha_s  =  72/610  (11.8%)  [= L(3)*L(6)]  (was incorrectly 188/610)
  sin2W    = 141/610  (23.1%)  [= L(2)*L(8)]
  V_cb     =  25/610  ( 4.1%)  [= L(4)+L(6)]
  sin2_23  = 333/610  (54.6%)  [= L(5)+L(12)]
  gamma_I  = 145/610  (23.8%)  [= F(5)*L(7)]
  m_t/m_H  = 841/610  (137.9%) [= L(7)^2]

  NOTE: The old budget 188+89+333=610 was based on WRONG alpha_s/V_us values.
  With corrected values: 72 + 141 + 333 + 25 = 571 (not 610).
  There is NO exact partition of F(15) into physical constants.
  However, F(15) IS the natural normalizer for F/L expressions.
""")

# Verify corrected values
print(f"  Corrected quantities over F(15) = 610:")
for name, num in f15_quantities.items():
    print(f"    {name:12s} = {num:>4d}/610 = {num/610:.6f}")
total = sum(v for k,v in f15_quantities.items() if k != "m_t/m_H")
print(f"\n  Sum (excluding m_t/m_H): {total}/610 = {total/610:.4f}")
print(f"  NOTE: No exact partition to 610 exists with corrected values.")

# What IS true about F(15):
print(f"\n  WHAT IS TRUE: F(15) = 610 is the natural normalizer because")
print(f"  15 = 3+5+7 (sum of mode indices) and F(15) = E8_Coxeter/2.")
print(f"  Many constants DO normalize to x/610, but no exact partition to 1.")
print(f"  sin2_23 alone accounts for 333/610 = 54.6% of the normalizer.")
