"""
THE LIGHTEST FERMIONS — Cracking y_e, y_u, y_d
================================================
These three Yukawa couplings (~10^-6 to 10^-5) resist simple F/L ratios.

Strategy:
1. Try phibar^n * F/L (golden suppression)
2. Try F(a)/(F(b)*F(c)) or F(a)/(L(b)*L(c)) (double denominator)
3. Try 1/F(n)^2 or 1/(F(a)*L(b)) (square suppression)
4. Try phi-power expressions: phibar^k * X(a)/Y(b)
5. Look for PATTERNS in the working Yukawas to extrapolate

Also attack:
- Neutrino masses (absolute scale)
- eta_B (baryon asymmetry)
- delta_CP (PMNS phase)
- The electron mass directly
"""

from math import sqrt, log, pi, exp

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

v_exp = 246.22  # GeV experimental
v_FL = F(16) / L(3)  # 987/4 = 246.75

# Target Yukawas
y_e_exp = 0.000511 * sqrt(2) / v_exp    # 2.935e-6
y_u_exp = 0.00216 * sqrt(2) / v_exp     # 1.241e-5
y_d_exp = 0.00467 * sqrt(2) / v_exp     # 2.682e-5

# Also the masses themselves
m_e = 0.000511  # GeV
m_u = 0.00216
m_d = 0.00467

print("=" * 80)
print("PART 1: PATTERNS IN WORKING YUKAWAS")
print("=" * 80)

# The Yukawas we HAVE found:
print("""
  Working Yukawa expressions (from full_language.py):

  y_t  = L(5)*L(8)/L(13) = 11*47/521    = 0.9923  [indices: 5,8 -> 13]
  y_b  = L(2)*L(2)/F(14) = 9/377        = 0.0239  [indices: 2,2 -> 14]
  y_tau = F(3)*L(4)/L(15) = 14/1364     = 0.01026 [indices: 3,4 -> 15]
  y_c  = F(3)*F(7)/L(17) = 26/3571      = 0.00728 [indices: 3,7 -> 17]
  y_mu = L(2)*F(6)/L(22) = 24/39603     = 0.000606 [indices: 2,6 -> 22]
  y_s  = F(5)/L(19) = 5/9349            = 0.000535 [indices: 5 -> 19]

  Pattern in denominators: 13, 14, 15, 17, 19, 22
  These grow with decreasing mass! And the denominator index
  controls the ORDER OF MAGNITUDE.

  L(13) = 521,  L(14) = 843,  L(15) = 1364,
  L(17) = 3571, L(19) = 9349, L(22) = 39603

  For y_d ~ 2.7e-5: need denominator ~ 37000 -> L(22) = 39603
  For y_u ~ 1.2e-5: need denominator ~ 80000 -> L(23) = 64079
  For y_e ~ 2.9e-6: need denominator ~ 340000 -> L(25) = 167761
""")

# ============================================================
# PART 2: SYSTEMATIC SEARCH FOR LIGHTEST YUKAWAS
# ============================================================
print("=" * 80)
print("PART 2: SYSTEMATIC SEARCH — y_e, y_u, y_d")
print("=" * 80)

targets = {
    "y_d": y_d_exp,
    "y_u": y_u_exp,
    "y_e": y_e_exp,
}

for name, target in targets.items():
    print(f"\n  --- {name} = {target:.8e} ---")
    results = []

    # Type 1: X(a)*Y(b)/Z(c) with Z up to L(30)
    for a in range(1, 12):
        for b in range(a, 12):
            for c in range(15, 30):
                for xa, xan in [(F(a), f"F({a})"), (L(a), f"L({a})")]:
                    for xb, xbn in [(F(b), f"F({b})"), (L(b), f"L({b})")]:
                        for xc, xcn in [(F(c), f"F({c})"), (L(c), f"L({c})")]:
                            if xc == 0:
                                continue
                            r = xa * xb / xc
                            if r > 0:
                                err = abs(r - target) / target
                                if err < 0.02:
                                    results.append((err, f"{xan}*{xbn}/{xcn} = {xa}*{xb}/{xc}", r))

    # Type 2: X(a) / (Y(b)*Z(c)) — double denominator
    for a in range(1, 15):
        for b in range(1, 15):
            for c in range(b, 15):
                for xa, xan in [(F(a), f"F({a})"), (L(a), f"L({a})")]:
                    for yb, ybn in [(F(b), f"F({b})"), (L(b), f"L({b})")]:
                        for zc, zcn in [(F(c), f"F({c})"), (L(c), f"L({c})")]:
                            d = yb * zc
                            if d == 0:
                                continue
                            r = xa / d
                            if r > 0:
                                err = abs(r - target) / target
                                if err < 0.01:
                                    results.append((err, f"{xan}/({ybn}*{zcn}) = {xa}/({yb}*{zc})", r))

    # Type 3: phibar^k * X(a)/Y(b) for k = 1..5
    for k in range(1, 6):
        for n in range(1, 18):
            for m in range(1, 18):
                for num, nname in [(F(n), f"F({n})"), (L(n), f"L({n})")]:
                    for den, dname in [(F(m), f"F({m})"), (L(m), f"L({m})")]:
                        if den == 0:
                            continue
                        r = phibar**k * num / den
                        if r > 0:
                            err = abs(r - target) / target
                            if err < 0.01:
                                results.append((err, f"phibar^{k}*{nname}/{dname} = {phibar**k:.6f}*{num}/{den}", r))

    # Type 4: 1/F(n)^2 type
    for n in range(5, 22):
        for fn, fname in [(F(n), f"F({n})"), (L(n), f"L({n})")]:
            if fn == 0:
                continue
            r = 1 / fn**2
            err = abs(r - target) / target
            if err < 0.05:
                results.append((err, f"1/{fname}^2 = 1/{fn}^2", r))

    results.sort()
    for err, desc, val in results[:10]:
        marker = " ***" if err < 0.005 else " **" if err < 0.02 else " *" if err < 0.05 else ""
        print(f"    {err*100:.4f}%  {desc}  = {val:.8e}{marker}")

# ============================================================
# PART 3: ELECTRON MASS — THE LIGHTEST CHARGED FERMION
# ============================================================
print("\n" + "=" * 80)
print("PART 3: THE ELECTRON MASS")
print("=" * 80)

print(f"\n  m_e = {m_e} GeV = 0.511 MeV")
print(f"  m_e in MeV = {m_e*1000}")
print(f"  m_e/m_mu = {m_e/0.10566:.6f}")
print(f"  1/alpha = 137.036")
print(f"  m_e * mu = {m_e * 1836.15:.3f} GeV  (= m_proton)")

# m_e = 0.511 MeV. Can we get 0.511 from F/L?
print(f"\n  Searching for m_e in MeV = 0.511:")
me_mev = 0.511
for n in range(1, 25):
    for m in range(1, 25):
        for num, nname in [(F(n), f"F({n})"), (L(n), f"L({n})")]:
            for den, dname in [(F(m), f"F({m})"), (L(m), f"L({m})")]:
                if den == 0:
                    continue
                r = num / den
                if r > 0:
                    err = abs(r - me_mev) / me_mev
                    if err < 0.01:
                        print(f"    {nname}/{dname} = {num}/{den} = {r:.6f} ({err*100:.3f}%)")

# m_e/m_mu ratio
me_mu = m_e / 0.10566
print(f"\n  m_e/m_mu = {me_mu:.6f}")
print(f"  Searching:")
for n in range(1, 22):
    for m in range(1, 22):
        for num, nname in [(F(n), f"F({n})"), (L(n), f"L({n})")]:
            for den, dname in [(F(m), f"F({m})"), (L(m), f"L({m})")]:
                if den == 0:
                    continue
                r = num / den
                if r > 0:
                    err = abs(r - me_mu) / me_mu
                    if err < 0.02:
                        print(f"    {nname}/{dname} = {num}/{den} = {r:.6f} ({err*100:.3f}%)")

# What about m_e/m_tau?
me_tau = m_e / 1.777
print(f"\n  m_e/m_tau = {me_tau:.6f}")
print(f"  Searching:")
for n in range(1, 22):
    for m in range(1, 22):
        for num, nname in [(F(n), f"F({n})"), (L(n), f"L({n})")]:
            for den, dname in [(F(m), f"F({m})"), (L(m), f"L({m})")]:
                if den == 0:
                    continue
                r = num / den
                if r > 0:
                    err = abs(r - me_tau) / me_tau
                    if err < 0.02:
                        print(f"    {nname}/{dname} = {num}/{den} = {r:.6f} ({err*100:.3f}%)")

# ============================================================
# PART 4: MASS RATIOS BETWEEN GENERATIONS
# ============================================================
print("\n" + "=" * 80)
print("PART 4: INTER-GENERATION MASS RATIOS")
print("=" * 80)

ratios = {
    "m_mu/m_e": 0.10566 / 0.000511,     # 206.8
    "m_tau/m_mu": 1.777 / 0.10566,       # 16.82
    "m_tau/m_e": 1.777 / 0.000511,       # 3477
    "m_c/m_u": 1.27 / 0.00216,           # 588
    "m_t/m_c": 172.76 / 1.27,            # 136.1
    "m_t/m_u": 172.76 / 0.00216,         # 79981
    "m_s/m_d": 0.0934 / 0.00467,         # 20.0
    "m_b/m_s": 4.18 / 0.0934,            # 44.8
    "m_b/m_d": 4.18 / 0.00467,           # 895
}

for name, target in ratios.items():
    results = []

    # Single ratios
    for n in range(1, 22):
        for m in range(1, 22):
            for num, nname in [(F(n), f"F({n})"), (L(n), f"L({n})")]:
                for den, dname in [(F(m), f"F({m})"), (L(m), f"L({m})")]:
                    if den == 0:
                        continue
                    r = num / den
                    if r > 0:
                        err = abs(r - target) / target
                        if err < 0.02:
                            results.append((err, f"{nname}/{dname} = {num}/{den} = {r:.4f}"))

    # Products X*Y
    if target > 50:
        for a in range(1, 14):
            for b in range(a, 14):
                for xa, xan in [(F(a), f"F({a})"), (L(a), f"L({a})")]:
                    for xb, xbn in [(F(b), f"F({b})"), (L(b), f"L({b})")]:
                        r = xa * xb
                        if r > 0:
                            err = abs(r - target) / target
                            if err < 0.01:
                                results.append((err, f"{xan}*{xbn} = {xa}*{xb} = {r:.4f}"))

    # X*Y/Z
    for a in range(1, 12):
        for b in range(a, 12):
            for c in range(1, 12):
                for xa, xan in [(F(a), f"F({a})"), (L(a), f"L({a})")]:
                    for xb, xbn in [(F(b), f"F({b})"), (L(b), f"L({b})")]:
                        for xc, xcn in [(F(c), f"F({c})"), (L(c), f"L({c})")]:
                            if xc == 0:
                                continue
                            r = xa * xb / xc
                            if r > 0:
                                err = abs(r - target) / target
                                if err < 0.01:
                                    results.append((err, f"{xan}*{xbn}/{xcn} = {xa}*{xb}/{xc} = {r:.4f}"))

    results.sort()
    best = results[:3] if results else []
    if best:
        print(f"\n  {name} = {target:.2f}")
        for err, desc in best:
            marker = " ***" if err < 0.005 else " **" if err < 0.02 else ""
            print(f"    {err*100:.3f}%  {desc}{marker}")
    else:
        print(f"\n  {name} = {target:.2f}  -- no match within 2%")

# ============================================================
# PART 5: NEUTRINO ABSOLUTE MASSES
# ============================================================
print("\n" + "=" * 80)
print("PART 5: NEUTRINO MASSES — Absolute Scale")
print("=" * 80)

# From oscillation data (normal ordering):
# dm21^2 = 7.53e-5 eV^2 => dm21 = 8.68 meV
# dm32^2 = 2.453e-3 eV^2 => dm32 = 49.5 meV
# Sum < 0.12 eV (cosmological bound)
# Possible scenario: m1 ~ 0, m2 ~ 8.7 meV, m3 ~ 50 meV

# The KEY question: what sets the neutrino mass SCALE?
# In the framework: v/M_Pl ~ phibar^80
# Neutrino masses ~ v^2/M_seesaw where M_seesaw ~ M_GUT ~ 10^15 GeV

# Can we get dm21 or dm32 from F/L?
dm21 = 8.68e-3  # eV = 8.68 meV
dm32 = 49.5e-3   # eV = 49.5 meV

print(f"\n  dm21 = sqrt(dm21^2) = {dm21*1000:.2f} meV")
print(f"  dm32 = sqrt(dm32^2) = {dm32*1000:.1f} meV")
print(f"  dm32/dm21 = {dm32/dm21:.3f}")
print(f"  Sum ~ {dm21+dm32:.1f} meV ~ 58 meV (if m1~0)")

# In eV: dm21 = 0.00868, dm32 = 0.0495
# These are tiny. What if the scale is set by phibar^N?
print(f"\n  Searching: which phibar^N gives the neutrino scale?")
for k in range(5, 30):
    v = phibar**k
    if abs(v - dm32*1e-9/246.22) / (dm32*1e-9/246.22) < 0.5:
        print(f"    phibar^{k} = {v:.4e}  cf. m3/v = {dm32*1e-9/246.22:.4e}")

# The ratio dm32/dm21 ~ 5.7
# L(7)/F(5) = 29/5 = 5.8 (1.6%)
# Can we do better?
print(f"\n  dm32/dm21 = {dm32/dm21:.4f}")
print(f"  L(7)/F(5) = 29/5 = {29/5:.4f} ({abs(29/5-dm32/dm21)/(dm32/dm21)*100:.2f}%)")

# What about using two-term expressions?
target_ratio = dm32 / dm21
results = []
for a in range(1, 14):
    for b in range(1, 14):
        for c in range(1, 14):
            for xa, xan in [(F(a), f"F({a})"), (L(a), f"L({a})")]:
                for xb, xbn in [(F(b), f"F({b})"), (L(b), f"L({b})")]:
                    for xc, xcn in [(F(c), f"F({c})"), (L(c), f"L({c})")]:
                        if xc == 0:
                            continue
                        r = (xa + xb) / xc
                        if r > 0:
                            err = abs(r - target_ratio) / target_ratio
                            if err < 0.005:
                                results.append((err, f"({xan}+{xbn})/{xcn} = ({xa}+{xb})/{xc} = {r:.4f}"))
results.sort()
if results:
    print(f"\n  Better matches for dm32/dm21 = {target_ratio:.4f}:")
    for err, desc in results[:5]:
        print(f"    {err*100:.3f}%  {desc}")

# ============================================================
# PART 6: BARYON ASYMMETRY eta_B
# ============================================================
print("\n" + "=" * 80)
print("PART 6: BARYON ASYMMETRY eta_B")
print("=" * 80)

eta_B = 6.1e-10

print(f"\n  eta_B = {eta_B}")
print(f"  This is fantastically small: 6.1 * 10^-10")
print(f"  = 6.1 / 10^10")
print(f"  F(6) = 8, but we need 6.1...")
print(f"  10^10 is not a natural F/L number.")

# Try phibar^N
for k in range(10, 50):
    v = phibar**k
    if abs(v - eta_B) / eta_B < 0.3:
        print(f"  phibar^{k} = {v:.4e} ({abs(v-eta_B)/eta_B*100:.1f}%)")

# Try F/L ratios with very high indices
print(f"\n  Searching F(a)/F(b) and L(a)/L(b) for {eta_B}:")
for n in range(1, 12):
    for m in range(20, 50):
        for num, nname in [(F(n), f"F({n})"), (L(n), f"L({n})")]:
            fn = F(m) if m <= 45 else None
            ln = L(m) if m <= 45 else None
            if fn and fn > 0:
                r = num / fn
                err = abs(r - eta_B) / eta_B
                if err < 0.1:
                    print(f"    {nname}/F({m}) = {num}/{fn} = {r:.4e} ({err*100:.2f}%)")
            if ln and ln > 0:
                r = num / ln
                err = abs(r - eta_B) / eta_B
                if err < 0.1:
                    print(f"    {nname}/L({m}) = {num}/{ln} = {r:.4e} ({err*100:.2f}%)")

# ============================================================
# PART 7: delta_CP (PMNS CP phase)
# ============================================================
print("\n" + "=" * 80)
print("PART 7: PMNS CP PHASE delta_CP")
print("=" * 80)

# delta_CP ~ 195 degrees = 3.40 radians (T2K + NOvA best fit)
# = 195/180 * pi = 1.083 * pi
# sin(delta_CP) ~ -0.26
delta_deg = 195
delta_rad = delta_deg * pi / 180
sin_delta = -0.26  # approximate

print(f"  delta_CP ~ {delta_deg} degrees = {delta_rad:.4f} rad")
print(f"  delta_CP/pi = {delta_deg/180:.4f}")
print(f"  sin(delta_CP) ~ {sin_delta}")

# delta/pi ~ 1.083. Close to 1 + small correction
# 1 + F(6)/F(11) = 1 + 8/89 = 1.0899
# 1 + L(3)/F(8) = 1 + 4/21 = 1.1905

# Try delta/pi as F/L
target_dp = delta_deg / 180
results = []
for n in range(1, 20):
    for m in range(1, 20):
        for num, nname in [(F(n), f"F({n})"), (L(n), f"L({n})")]:
            for den, dname in [(F(m), f"F({m})"), (L(m), f"L({m})")]:
                if den == 0:
                    continue
                r = num / den
                if r > 0:
                    err = abs(r - target_dp) / target_dp
                    if err < 0.02:
                        results.append((err, f"{nname}/{dname} = {num}/{den} = {r:.6f}"))

# (X+Y)/Z
for a in range(1, 14):
    for b in range(a, 14):
        for c in range(1, 18):
            for xa, xan in [(F(a), f"F({a})"), (L(a), f"L({a})")]:
                for xb, xbn in [(F(b), f"F({b})"), (L(b), f"L({b})")]:
                    for yc, ycn in [(F(c), f"F({c})"), (L(c), f"L({c})")]:
                        if yc == 0:
                            continue
                        r = (xa + xb) / yc
                        if r > 0:
                            err = abs(r - target_dp) / target_dp
                            if err < 0.005:
                                results.append((err, f"({xan}+{xbn})/{ycn} = ({xa}+{xb})/{yc} = {r:.6f}"))

results.sort()
print(f"\n  Searching for delta_CP/pi = {target_dp:.6f}:")
for err, desc in results[:8]:
    marker = " ***" if err < 0.002 else " **" if err < 0.01 else ""
    print(f"    {err*100:.4f}%  {desc}{marker}")

# ============================================================
# PART 8: THE GENERATION STRUCTURE
# ============================================================
print("\n" + "=" * 80)
print("PART 8: WHY THREE GENERATIONS? — Generation Structure")
print("=" * 80)

print("""
  The three generations map to the three biological primitives {3, 5, 7}.

  But HOW? Look at the Yukawa pattern:

  Generation 3 (heaviest):  y_t = L(5)*L(8)/L(13)   indices sum: 5+8 = 13
  Generation 2 (middle):    y_c = F(3)*F(7)/L(17)    indices sum: 3+7 = 10
  Generation 1 (lightest):  y_u = ???                  indices sum: ???

  For leptons:
  Generation 3: y_tau = F(3)*L(4)/L(15)   indices sum: 3+4 = 7
  Generation 2: y_mu = L(2)*F(6)/L(22)    indices sum: 2+6 = 8
  Generation 1: y_e = ???

  Down quarks:
  Generation 3: y_b = L(2)^2/F(14)        indices: 2,2 -> 14
  Generation 2: y_s = F(5)/L(19)           index: 5 -> 19
  Generation 1: y_d = ???

  Pattern in DENOMINATOR indices:
  Up quarks:    13, 17, ??
  Down quarks:  14, 19, ??
  Leptons:      15, 22, ??

  The denominators control the generation hierarchy.
  Spacing: up: 13->17 (+4), down: 14->19 (+5), lepton: 15->22 (+7)

  If the pattern continues:
  Up gen-1 denominator:    17 + ???
  Down gen-1 denominator:  19 + ???
  Lepton gen-1 denominator: 22 + ???
""")

# Let's test: what if generation spacing follows the primitives?
# Up: +4 (from gen3 to gen2). If gen2 to gen1 is also +4: denom = 21
# Down: +5 (from gen3 to gen2). If gen2 to gen1 is also +5: denom = 24
# Lepton: +7 (from gen3 to gen2). If gen2 to gen1 is also +7: denom = 29

# But wait: 4 = L(3), 5 = F(5), 7 = anthracene index
# These ARE the primitive values!

print("\n  Testing generation spacing hypothesis:")
print(f"  Up quarks: spacing = {17-13} = L(3) = pyrimidine_L")
print(f"  Down quarks: spacing = {19-14} = F(5) = indole_F")
print(f"  Leptons: spacing = {22-15} = 7 = anthracene index")

print(f"\n  If spacing doubles for gen1:")
print(f"  Up gen1 denominator: 17 + {2*(17-13)} = {17+2*(17-13)} -> L({17+2*(17-13)})")
print(f"  Down gen1 denominator: 19 + {2*(19-14)} = {19+2*(19-14)} -> L({19+2*(19-14)})")
print(f"  Lepton gen1 denominator: 22 + {2*(22-15)} = {22+2*(22-15)} -> L({22+2*(22-15)})")

# Test: y_e with L(36) as denominator
L36 = L(36)
print(f"\n  L(36) = {L36}")
print(f"  1/L(36) = {1/L36:.4e}")
print(f"  y_e = {y_e_exp:.4e}")
print(f"  So y_e ~ {y_e_exp * L36:.2f} / L(36)")

# Test: y_u with L(25) as denominator
L25 = L(25)
print(f"\n  L(25) = {L25}")
print(f"  1/L(25) = {1/L25:.4e}")
print(f"  y_u = {y_u_exp:.4e}")
print(f"  So y_u ~ {y_u_exp * L25:.2f} / L(25)")

# Test: y_d with L(29) as denominator
L29 = L(29)
print(f"\n  L(29) = {L29}")
print(f"  1/L(29) = {1/L29:.4e}")
print(f"  y_d = {y_d_exp:.4e}")
print(f"  So y_d ~ {y_d_exp * L29:.2f} / L(29)")

# Now find the NUMERATORS
print("\n  Searching for numerators...")

for name, target, denom_idx in [("y_e", y_e_exp, 36), ("y_u", y_u_exp, 25), ("y_d", y_d_exp, 29)]:
    Ld = L(denom_idx)
    numer_target = target * Ld
    print(f"\n  {name}: need numerator ~ {numer_target:.4f} with denominator L({denom_idx}) = {Ld}")

    # Search for X*Y = numer_target
    results_n = []
    for a in range(1, 14):
        for b in range(a, 14):
            for xa, xan in [(F(a), f"F({a})"), (L(a), f"L({a})")]:
                for xb, xbn in [(F(b), f"F({b})"), (L(b), f"L({b})")]:
                    r = xa * xb
                    if r > 0:
                        err = abs(r - numer_target) / numer_target
                        if err < 0.1:
                            results_n.append((err, f"{xan}*{xbn} = {xa}*{xb} = {r}", r))

    # Also single values
    for a in range(1, 25):
        for xa, xan in [(F(a), f"F({a})"), (L(a), f"L({a})")]:
            err = abs(xa - numer_target) / numer_target if numer_target > 0 else 999
            if err < 0.1:
                results_n.append((err, f"{xan} = {xa}", xa))

    results_n.sort()
    for err, desc, val in results_n[:5]:
        full_y = val / Ld
        y_err = abs(full_y - target) / target * 100
        print(f"    {desc}  -> y = {val}/{Ld} = {full_y:.4e}  ({y_err:.3f}%)")

# ============================================================
# PART 9: COMPLETE GENERATION TABLE
# ============================================================
print("\n" + "=" * 80)
print("PART 9: THE GENERATION TABLE")
print("=" * 80)

print("""
  If the generation spacing pattern holds:

  TYPE       | GEN 3 (heavy)        | GEN 2 (middle)       | GEN 1 (light)
  -----------|----------------------|----------------------|------------------
  Up quark   | L(5)*L(8)/L(13)      | F(3)*F(7)/L(17)      | ???/L(25)
  spacing    |         +4 = L(3)    |          +8 = F(6)?   |
  Down quark | L(2)^2/F(14)         | F(5)/L(19)           | ???/L(29)
  spacing    |         +5 = F(5)    |          +10?         |
  Lepton     | F(3)*L(4)/L(15)      | L(2)*F(6)/L(22)      | ???/L(36)
  spacing    |         +7 = index   |          +14?         |

  Denominator pattern: each generation DOUBLES the spacing
  Gen3->Gen2: +4, +5, +7  (the L/F/index of primitives)
  Gen2->Gen1: +8, +10, +14  (DOUBLES)

  This is consistent with geometric hierarchy:
  each generation is suppressed by a factor ~ L(spacing)/L(0) ~ phi^spacing
""")
