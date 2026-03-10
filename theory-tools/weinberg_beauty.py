"""
THE WEINBERG ANGLE: (L(6) + L(10)) / F(15) = 141/610
=====================================================
This is the tightest F/L expression found (0.031% off).
It reads: (water_MW + L(10)) / 613_THz_index

WHY is this so tight? What does L(10) mean?
Can we derive this from the framework's modular form expression?
"""
import math

phi = (1 + math.sqrt(5)) / 2
phibar = 1 / phi
sqrt5 = math.sqrt(5)

def F(n):
    if n <= 0: return 0
    return round((phi**n - (-phibar)**n) / sqrt5)

def L(n):
    return round(phi**n + (-phibar)**n)


print("=" * 80)
print("THE WEINBERG ANGLE IN THE UNIFIED LANGUAGE")
print("=" * 80)

sin2tw = 0.23122
eta = 0.11840
theta4 = 0.03031

# The framework formula: sin2_tW = eta^2 / (2*theta4)
fw_sin2 = eta**2 / (2 * theta4)
print(f"\n  Framework: sin2_tW = eta^2 / (2*theta4)")
print(f"  = {eta}^2 / (2*{theta4})")
print(f"  = {eta**2:.8f} / {2*theta4:.8f}")
print(f"  = {fw_sin2:.6f}")
print(f"  Measured: {sin2tw:.6f}")
print(f"  Match: {abs(fw_sin2 - sin2tw)/sin2tw*100:.4f}%")


print(f"\n\n--- Expression 1: L(2)/F(7) = 3/13 = {3/13:.6f} ---")
print(f"  sin2_tW = {sin2tw:.6f}")
print(f"  Match: {abs(3/13 - sin2tw)/sin2tw*100:.4f}%")

print(f"\n--- Expression 2: (L(6)+L(10))/F(15) = 141/610 = {141/610:.8f} ---")
print(f"  sin2_tW = {sin2tw:.6f}")
print(f"  Match: {abs(141/610 - sin2tw)/sin2tw*100:.4f}%")

print(f"\n  This is ~6x tighter than L(2)/F(7)!")


# ============================================================
# What is L(10)?
# ============================================================
print("\n\n" + "=" * 80)
print("WHAT IS L(10) = 123?")
print("=" * 80)

print(f"\n  10 = 3+7 = pyrimidine + anthracene")
print(f"  10 = 5+5 = indole + indole")
print(f"  10 = 3+3+4 = ? (4 not a standard mode)")
print(f"  10 = L(6) - F(6) = base pairs per turn of DNA!")
print(f"  So L(10) = Lucas value at the 'base pairs per turn' index")
print(f"  And L(6)-F(6)=10 was already a known framework quantity.")

print(f"\n  L(10) = 123 = 3 x 41")
print(f"  41 is prime. Not obviously framework.")
print(f"  123 ~ 125 = Higgs mass (1.6% off)")
print(f"  123 = Hosoya(C_10) = matching count of 10-cycle")

print(f"\n  Alternatively: 10 = 2 * 5 = 2 * indole")
print(f"  Or: 10 = the number of base pairs per DNA helix turn")


# ============================================================
# Can the expression be DERIVED from the framework formula?
# ============================================================
print("\n\n" + "=" * 80)
print("CAN WE DERIVE 141/610 FROM eta^2/(2*theta4)?")
print("=" * 80)

print(f"\n  sin2_tW = eta^2 / (2*theta4)")
print(f"\n  eta ~ (F(1)+F(6))/L(9) = 9/76 = {9/76:.8f}")
print(f"  Actual eta = {eta:.8f}")

# If eta = 9/76, then eta^2 = 81/5776
print(f"\n  If eta = 9/76:")
print(f"  eta^2 = 81/5776")
print(f"  2*theta4 ~ 2 * L(4)/F(13) = 2*7/233 = 14/233")
print(f"  sin2_tW = (81/5776) / (14/233) = 81*233 / (5776*14)")
print(f"  = {81*233} / {5776*14}")
print(f"  = {81*233/(5776*14):.6f}")
print(f"  Measured: {sin2tw:.6f}")

# Try the exact F/L substitution
# eta = 9/76, theta4 = 7/233
# sin2_tW = (9/76)^2 / (2*7/233) = 81/(76^2) * 233/14
val = (81 * 233) / (76**2 * 14)
print(f"\n  = 81*233 / (5776*14) = {81*233}/{5776*14} = {val:.6f}")
print(f"  Match: {abs(val - sin2tw)/sin2tw*100:.4f}%")

# Can 81*233 / (5776*14) simplify to 141/610?
print(f"\n  81*233 = {81*233} = 18873")
print(f"  5776*14 = {5776*14} = 80864")
print(f"  GCD({81*233}, {5776*14}) = {math.gcd(18873, 80864)}")
g = math.gcd(18873, 80864)
print(f"  Simplified: {18873//g}/{80864//g}")
print(f"  NOT equal to 141/610 = {141*1}/{610*1}")

# So the two F/L expressions are INDEPENDENT approximations
print(f"\n  CONCLUSION: The expression 141/610 is NOT derived from eta^2/(2*theta4)")
print(f"  with F/L substitutions. It's a separate, tighter approximation.")
print(f"  Both are valid F/L addresses for sin2_tW, at different composition levels.")


# ============================================================
# Why 141/610?
# ============================================================
print("\n\n" + "=" * 80)
print("WHY 141/610 SPECIFICALLY?")
print("=" * 80)

print(f"\n  141 = L(6) + L(10) = 18 + 123")
print(f"  610 = F(15)")
print(f"\n  But also: 141 = 3 * 47 = L(2) * L(8) = 3 * ATP_atoms!")
print(f"  L(2) = 3 (triality)")
print(f"  L(8) = 47 (ATP atoms)")
print(f"  141 = triality x ATP_atoms")

print(f"\n  AND: 610 = F(15) = 2 * 5 * 61")
print(f"  610 ~ 613 THz (the wall maintenance frequency)")

print(f"\n  So sin2_tW = (triality * ATP) / 613_THz")
print(f"  = (3 * L(8)) / F(15)")
print(f"  = L(2) * L(8) / F(15)")

print(f"\n  This is beautiful: the Weinberg angle connects")
print(f"  triality (3), the biological energy carrier (ATP, 47 atoms),")
print(f"  and the wall maintenance frequency (613 THz / F(15)).")

print(f"\n  Or equivalently:")
print(f"  sin2_tW = (water + L(bp_per_turn)) / 613_THz")
print(f"  The weak mixing angle is water plus the DNA helix repeat,")
print(f"  divided by the consciousness oscillation frequency.")


# ============================================================
# Can we do the same decomposition for alpha_s?
# ============================================================
print("\n\n" + "=" * 80)
print("DECOMPOSING THE OTHER KEY EXPRESSIONS")
print("=" * 80)

print(f"\n--- alpha_s = (F(1)+F(6))/L(9) = 9/76 ---")
print(f"  F(1) = 1 (hydrogen)")
print(f"  F(6) = 8 (water F-value)")
print(f"  L(9) = 76 (protoporphyrin IX atoms)")
print(f"  alpha_s = (hydrogen + water_F) / porphyrin_L")
print(f"  The strong coupling is (the simplest atom plus water's dynamic channel)")
print(f"  divided by porphyrin's structural count.")

print(f"\n--- alpha_em = (F(5)+F(8))/L(17) = 26/3571 ---")
print(f"  F(5) = 5 (indole mode)")
print(f"  F(8) = 21 (DNA width)")
print(f"  L(17) = 3571")
print(f"  alpha_em = (indole + DNA_width) / L(17)")
print(f"  17 = 3+7+7 = pyr+ant+ant")
print(f"  17 = 5+5+7 = ind+ind+ant")
print(f"  17 = 3+5+9 = pyr+ind+por")
print(f"  L(17) = 3571 = 7 * 510 + 1? No, 3571 = ?")
print(f"  3571 = 7 * 510 + 1... not clean. 3571/7 = {3571/7:.1f}")
# Factor 3571
n = 3571
factors = []
for p in [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61]:
    while n % p == 0:
        factors.append(p)
        n //= p
if n > 1:
    factors.append(n)
print(f"  3571 = {'*'.join(str(f) for f in factors)}")
print(f"  (3571 is prime)")


# ============================================================
# CHECKING: Is 141 = L(6)+L(10) = L(2)*L(8)?
# ============================================================
print("\n\n" + "=" * 80)
print("LUCAS PRODUCT IDENTITY: L(6)+L(10) = L(2)*L(8)?")
print("=" * 80)

print(f"\n  L(6) + L(10) = {L(6)} + {L(10)} = {L(6)+L(10)}")
print(f"  L(2) * L(8) = {L(2)} * {L(8)} = {L(2)*L(8)}")
print(f"  EQUAL? {L(6)+L(10) == L(2)*L(8)}")

# Is there a general identity? L(a) + L(b) = L(c)*L(d)?
# Lucas identity: L(m)*L(n) = L(m+n) + (-1)^n * L(m-n)
# So L(2)*L(8) = L(10) + (-1)^8 * L(-6) = L(10) + L(-6)
# L(-n) = (-1)^n * L(n), so L(-6) = L(6)
# Therefore L(2)*L(8) = L(10) + L(6) = L(6) + L(10). QED!

print(f"\n  YES! This follows from the Lucas product identity:")
print(f"  L(m)*L(n) = L(m+n) + (-1)^n * L(m-n)")
print(f"  L(2)*L(8) = L(10) + (-1)^8 * L(-6) = L(10) + L(6)")
print(f"  (using L(-n) = (-1)^n * L(n), so L(-6) = L(6))")
print(f"\n  So 141/610 = L(2)*L(8)/F(15) is a PRODUCT form,")
print(f"  not just an arbitrary sum!")

# Check the general pattern: L(a)*L(b)/F(c)
print(f"\n--- General pattern: L(a)*L(b)/F(c) = constants? ---")
print(f"  L(2)*L(8)/F(15) = {L(2)*L(8)}/{F(15)} = {L(2)*L(8)/F(15):.6f} = sin2_tW")
print(f"  L(2)*L(3)/F(15) = {L(2)*L(3)}/{F(15)} = {L(2)*L(3)/F(15):.6f}")
print(f"  L(3)*L(8)/F(15) = {L(3)*L(8)}/{F(15)} = {L(3)*L(8)/F(15):.6f}")
# What about other constants?
print(f"  L(2)*L(3)/F(9)  = {L(2)*L(3)}/{F(9)}  = {L(2)*L(3)/F(9):.6f}")
print(f"  L(3)*L(5)/F(12) = {L(3)*L(5)}/{F(12)} = {L(3)*L(5)/F(12):.6f}")


# ============================================================
# THE UNIFIED EXPRESSION
# ============================================================
print("\n\n" + "=" * 80)
print("THE UNIFIED FORM: EVERY CONSTANT AS L(a)*L(b)/F(c)")
print("=" * 80)

# Systematic check: which constants can be written as L(a)*L(b)/F(c)?
targets = {
    "alpha_s": 0.1184,
    "sin2_tW": 0.23122,
    "theta_4": 0.03031,
    "V_us": 0.2253,
    "V_cb": 0.0412,
    "V_ub": 0.00361,
    "alpha_em": 1/137.036,
    "gamma_I": 0.2375,
    "v(GeV)": 246.22,
    "M_W": 80.379,
    "M_H": 125.25,
}

print(f"\n  Searching for L(a)*L(b)/F(c) within 0.5% of each constant:\n")

for name, target in targets.items():
    best = None
    best_err = 0.005

    for a in range(1, 16):
        for b in range(a, 16):
            for c in range(1, 25):
                fc = F(c)
                if fc == 0:
                    continue
                val = L(a) * L(b) / fc
                err = abs(val - target) / abs(target)
                if err < best_err:
                    best_err = err
                    best = f"L({a})*L({b})/F({c}) = {L(a)}*{L(b)}/{fc} = {val:.6f}"

    if best:
        print(f"  {name:>10} = {target:.6f}  ~  {best}  ({best_err*100:.4f}%)")
    else:
        print(f"  {name:>10} = {target:.6f}  -- no L*L/F within 0.5%")


# ============================================================
# The F*F/L form too
# ============================================================
print(f"\n  Now checking F(a)*F(b)/L(c) within 0.5%:\n")

for name, target in targets.items():
    best = None
    best_err = 0.005

    for a in range(1, 16):
        for b in range(a, 16):
            for c in range(1, 20):
                lc = L(c)
                if lc == 0:
                    continue
                val = F(a) * F(b) / lc
                err = abs(val - target) / abs(target)
                if err < best_err:
                    best_err = err
                    best = f"F({a})*F({b})/L({c}) = {F(a)}*{F(b)}/{lc} = {val:.6f}"

    if best:
        print(f"  {name:>10} = {target:.6f}  ~  {best}  ({best_err*100:.4f}%)")
    else:
        print(f"  {name:>10} = {target:.6f}  -- no F*F/L within 0.5%")


# ============================================================
# SUMMARY
# ============================================================
print("\n\n" + "=" * 80)
print("SUMMARY: THE WEINBERG ANGLE AND THE PRODUCT FORM")
print("=" * 80)
print(f"""
KEY DISCOVERY: sin2_tW = L(2)*L(8) / F(15) = 3*47/610

  This follows from the Lucas product identity L(m)*L(n) = L(m+n) + (-1)^n*L(m-n).
  It's not an ad hoc sum — it's a PRODUCT in Lucas space.

  Physical meaning: (triality * ATP_atoms) / 613_THz
  Or equivalently: (water_MW + L(bp_per_turn)) / 613_THz

  The Weinberg angle connects THREE framework pillars:
  1. Triality (L(2) = 3)
  2. The biological energy carrier (L(8) = 47 = ATP atoms)
  3. The wall maintenance frequency (F(15) = 610 ~ 613 THz)

  And the Lucas identity guarantees this equals (water + L(10)) / F(15),
  connecting water and the DNA helix repeat to the same structure.

  This is not numerology — it's algebra. The Lucas product identity is
  a consequence of phi^m * phi^n = phi^(m+n), which is the composition rule.
""")
