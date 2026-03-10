"""
Element Properties vs Framework Vocabulary Analysis
Tests whether properties of elements Z=1..36 can be expressed
in terms of {phi, 2, 3, L(n), F(n), Coxeter exponents, mu=1836.15}

Focus: ratios and dimensionless quantities only.
"""

import math

# ============================================================
# FRAMEWORK CONSTANTS
# ============================================================
phi = (1 + math.sqrt(5)) / 2   # 1.6180339887...
phibar = 1/phi                   # 0.6180339887...
sqrt5 = math.sqrt(5)             # 2.2360679775...
mu = 1836.15267                  # proton/electron mass ratio
E_R = 13.605693                  # Rydberg energy (eV)
a0 = 52.9177                     # Bohr radius (pm)

# Lucas numbers L(n): 2, 1, 3, 4, 7, 11, 18, 29, 47, 76, 123, 199, 322...
def lucas(n):
    if n == 0: return 2
    if n == 1: return 1
    a, b = 2, 1
    for _ in range(n-1):
        a, b = b, a+b
    return b

# Fibonacci numbers F(n): 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144...
def fib(n):
    if n == 0: return 0
    if n == 1: return 1
    a, b = 0, 1
    for _ in range(n-1):
        a, b = b, a+b
    return b

# E8 Coxeter exponents: {1, 7, 11, 13, 17, 19, 23, 29}
coxeter_e8 = [1, 7, 11, 13, 17, 19, 23, 29]
h_e8 = 30  # E8 Coxeter number

# Modular forms at q = 1/phi (from framework)
eta_val = 0.11840
theta2 = 2.55509
theta3 = 2.55509
theta4 = 0.03031

print("=" * 80)
print("FRAMEWORK REFERENCE VALUES")
print("=" * 80)
print(f"phi = {phi:.10f}")
print(f"phibar = {phibar:.10f}")
print(f"phi^2 = {phi**2:.10f}")
print(f"phi^3 = {phi**3:.10f}")
print(f"sqrt(5) = {sqrt5:.10f}")
print(f"mu = {mu}")
print(f"E_R = {E_R} eV")
print(f"a0 = {a0} pm")
print(f"theta3 at q=1/phi = {theta3}")
print()
print("Lucas numbers L(0..15):", [lucas(n) for n in range(16)])
print("Fibonacci numbers F(0..15):", [fib(n) for n in range(16)])
print("E8 Coxeter exponents:", coxeter_e8)
print(f"Sum of Coxeter exponents: {sum(coxeter_e8)}")
print()

# Build a dictionary of "framework numbers" for matching
framework_nums = {}
for n in range(20):
    framework_nums[f"L({n})"] = lucas(n)
    framework_nums[f"F({n})"] = fib(n)
# phi powers
for k in range(-5, 6):
    framework_nums[f"phi^{k}"] = phi**k
# Simple fractions of framework numbers
framework_nums["1/3"] = 1/3
framework_nums["2/3"] = 2/3
framework_nums["sqrt(5)"] = sqrt5
framework_nums["mu/1000"] = mu/1000
framework_nums["mu/1836"] = 1.0
framework_nums["3/phi"] = 3/phi
framework_nums["3/phi^2"] = 3/phi**2
framework_nums["phi/3"] = phi/3
framework_nums["2/phi"] = 2/phi
framework_nums["phi/2"] = phi/2
framework_nums["phi^2/3"] = phi**2/3
framework_nums["1/phi^2"] = 1/phi**2
framework_nums["2*phi"] = 2*phi
framework_nums["3*phi"] = 3*phi

print("=" * 80)
print("SECTION A: IONIZATION ENERGIES AS MULTIPLES OF E_R = 13.606 eV")
print("=" * 80)

# First ionization energies (eV) for Z=1..36 (NIST values)
IE_eV = {
    1: 13.5984,  # H
    2: 24.5874,  # He
    3: 5.3917,   # Li
    4: 9.3227,   # Be
    5: 8.2980,   # B
    6: 11.2603,  # C
    7: 14.5341,  # N
    8: 13.6181,  # O
    9: 17.4228,  # F
    10: 21.5645, # Ne
    11: 5.1391,  # Na
    12: 7.6462,  # Mg
    13: 5.9858,  # Al
    14: 8.1517,  # Si
    15: 10.4867, # P
    16: 10.3600, # S
    17: 12.9676, # Cl
    18: 15.7596, # Ar
    19: 4.3407,  # K
    20: 6.1132,  # Ca
    21: 6.5615,  # Sc
    22: 6.8281,  # Ti
    23: 6.7462,  # V
    24: 6.7665,  # Cr
    25: 7.4340,  # Mn
    26: 7.9024,  # Fe
    27: 7.8810,  # Co
    28: 7.6399,  # Ni
    29: 7.7264,  # Cu
    30: 9.3942,  # Zn
    31: 5.9993,  # Ga
    32: 7.8994,  # Ge
    33: 9.7886,  # As
    34: 9.7524,  # Se
    35: 11.8138, # Br
    36: 13.9996, # Kr
}

element_names = {
    1: "H", 2: "He", 3: "Li", 4: "Be", 5: "B", 6: "C", 7: "N", 8: "O",
    9: "F", 10: "Ne", 11: "Na", 12: "Mg", 13: "Al", 14: "Si", 15: "P",
    16: "S", 17: "Cl", 18: "Ar", 19: "K", 20: "Ca", 21: "Sc", 22: "Ti",
    23: "V", 24: "Cr", 25: "Mn", 26: "Fe", 27: "Co", 28: "Ni", 29: "Cu",
    30: "Zn", 31: "Ga", 32: "Ge", 33: "As", 34: "Se", 35: "Br", 36: "Kr"
}

print("\nIE / E_R ratios for all 36 elements:")
print(f"{'Z':>3} {'El':>3} {'IE(eV)':>10} {'IE/E_R':>10} {'Nearest framework':>30} {'Delta%':>10}")
print("-" * 75)

def find_nearest_framework(value, nums_dict, tolerance=0.05):
    """Find closest framework number within tolerance."""
    best_name = None
    best_delta = float('inf')
    for name, num in nums_dict.items():
        if num == 0: continue
        delta = abs(value - num) / abs(num)
        if delta < best_delta:
            best_delta = delta
            best_name = name
    return best_name, best_delta

for Z in sorted(IE_eV.keys()):
    ratio = IE_eV[Z] / E_R
    name, delta = find_nearest_framework(ratio, framework_nums)
    flag = " <---" if delta < 0.02 else ""
    print(f"{Z:3d} {element_names[Z]:>3} {IE_eV[Z]:10.4f} {ratio:10.6f}  {name:>30} = {framework_nums[name]:10.6f}  {delta*100:8.3f}%{flag}")

# Special checks mentioned in the question
print("\n--- SPECIFIC CLAIMS (Section A) ---")

# H: 13.6 / 13.606 = ~1.000
ratio_H = IE_eV[1] / E_R
print(f"H:  IE/E_R = {ratio_H:.6f} (1.000 by definition, actual deviation: {abs(ratio_H-1)*100:.4f}%)")

# He: 24.59 / 13.606 = 1.807
ratio_He = IE_eV[2] / E_R
print(f"He: IE/E_R = {ratio_He:.6f}")
print(f"    mu/1000 = {mu/1000:.6f}, delta = {abs(ratio_He - mu/1000)/ratio_He*100:.3f}%")
print(f"    NOTE: mu/1000 = 1.836, not 1.807. Claim mu/1000 is WRONG.")
print(f"    L(1) = {lucas(1)}, 2*phibar = {2*phibar:.6f}, delta from 2*phibar = {abs(ratio_He - 2*phibar)/ratio_He*100:.3f}%")
print(f"    Actually He IE = Z_eff^2 * E_R, so ratio = (Z-sigma)^2 = ({math.sqrt(ratio_He):.4f})^2")
print(f"    No clean framework number.")

# Li: 5.39 / 13.606 = 0.396
ratio_Li = IE_eV[3] / E_R
print(f"\nLi: IE/E_R = {ratio_Li:.6f}")
print(f"    1/phi^2 = {1/phi**2:.6f}, delta = {abs(ratio_Li - 1/phi**2)/(ratio_Li)*100:.3f}%")
print(f"    NOTE: 0.396 vs 0.382 = 3.6% off. NOT a clean match to 1/phi^2.")
print(f"    2/5 = {2/5:.6f}, delta = {abs(ratio_Li - 0.4)/ratio_Li*100:.3f}%")

# Noble gases
print("\n--- NOBLE GAS IE/E_R RATIOS ---")
noble_Z = [2, 10, 18, 36]
for Z in noble_Z:
    ratio = IE_eV[Z] / E_R
    print(f"  {element_names[Z]:>2} (Z={Z:2d}): IE/E_R = {ratio:.6f}")

# Noble gas ratios to each other
print("\n  Ratios between noble gas IEs:")
for i in range(len(noble_Z)):
    for j in range(i+1, len(noble_Z)):
        r = IE_eV[noble_Z[i]] / IE_eV[noble_Z[j]]
        name, delta = find_nearest_framework(r, framework_nums)
        flag = " <---" if delta < 0.02 else ""
        print(f"    IE({element_names[noble_Z[i]]})/IE({element_names[noble_Z[j]]}) = {r:.6f}  ~ {name} = {framework_nums[name]:.6f} ({delta*100:.2f}%){flag}")

# Life elements
print("\n--- LIFE ELEMENT (C, N, O, H) IE/E_R ---")
life_Z = [1, 6, 7, 8]
for Z in life_Z:
    ratio = IE_eV[Z] / E_R
    print(f"  {element_names[Z]:>2}: IE/E_R = {ratio:.6f}")

# O is almost exactly E_R!
print(f"\n  O: IE = {IE_eV[8]:.4f} eV, E_R = {E_R:.4f} eV, ratio = {IE_eV[8]/E_R:.6f}")
print(f"  Match to 1.000: {abs(IE_eV[8]/E_R - 1)*100:.3f}% -- OXYGEN IE ~ E_R to 0.09%!")

# C
ratio_C = IE_eV[6] / E_R
print(f"\n  C: IE/E_R = {ratio_C:.6f}")
print(f"    phi^(-1/2) = {phi**(-0.5):.6f}, delta = {abs(ratio_C - phi**(-0.5))/ratio_C*100:.3f}%")

# N
ratio_N = IE_eV[7] / E_R
print(f"  N: IE/E_R = {ratio_N:.6f}")
print(f"    phi^(-1/8) = {phi**(-0.125):.6f}, no.")
print(f"    Actually N/E_R = {ratio_N:.4f}, ~1.068. Not a clean framework number.")

# Check IE(N)/IE(O)
ratio_NO = IE_eV[7] / IE_eV[8]
print(f"\n  IE(N)/IE(O) = {ratio_NO:.6f}")
print(f"    phi^(-1/4) = {phi**(-0.25):.6f}, delta = {abs(ratio_NO - phi**(-0.25))/ratio_NO*100:.3f}%")

# Check IE(C)/IE(O)
ratio_CO = IE_eV[6] / IE_eV[8]
print(f"  IE(C)/IE(O) = {ratio_CO:.6f}")
print(f"    phi^(-1/2) = {phi**(-0.5):.6f}, delta = {abs(ratio_CO - phi**(-0.5))/ratio_CO*100:.3f}%")

print()
print("=" * 80)
print("SECTION B: ELECTRONEGATIVITY PATTERNS (Pauling Scale)")
print("=" * 80)

# Pauling electronegativities for Z=1..36
EN = {
    1: 2.20,  # H
    2: None,  # He (no Pauling EN)
    3: 0.98,  # Li
    4: 1.57,  # Be
    5: 2.04,  # B
    6: 2.55,  # C
    7: 3.04,  # N
    8: 3.44,  # O
    9: 3.98,  # F
    10: None, # Ne
    11: 0.93, # Na
    12: 1.31, # Mg
    13: 1.61, # Al
    14: 1.90, # Si
    15: 2.19, # P
    16: 2.58, # S
    17: 3.16, # Cl
    18: None, # Ar
    19: 0.82, # K
    20: 1.00, # Ca
    21: 1.36, # Sc
    22: 1.54, # Ti
    23: 1.63, # V
    24: 1.66, # Cr
    25: 1.55, # Mn
    26: 1.83, # Fe
    27: 1.88, # Co
    28: 1.91, # Ni
    29: 1.90, # Cu
    30: 1.65, # Zn
    31: 1.81, # Ga
    32: 2.01, # Ge
    33: 2.18, # As
    34: 2.55, # Se
    35: 2.96, # Br
    36: 3.00, # Kr
}

print("\n--- SPECIFIC ELECTRONEGATIVITY CLAIMS ---\n")

# C = 2.55 vs theta_3 = 2.55509
print(f"C electronegativity = {EN[6]}")
print(f"theta_3(1/phi) = {theta3}")
print(f"Delta = {abs(EN[6] - theta3)/theta3*100:.3f}%")
print(f"theta_2(1/phi) = {theta2}")
print(f"Delta from theta_2 = {abs(EN[6] - theta2)/theta2*100:.3f}%")
print(f"VERDICT: C EN = 2.55, theta_3 = 2.555. Match is {100*(1-abs(EN[6]-theta3)/theta3):.2f}%.")
print(f"  BUT: Pauling EN is defined to ±0.05, so 2.55 vs 2.555 is within uncertainty.")
print(f"  This is a ~0.2% match but the input precision doesn't support the claim strongly.\n")

# Se also = 2.55!
print(f"Se electronegativity = {EN[34]}")
print(f"Same value as C. Not unique to carbon.\n")

# H = 2.20 vs framework
print(f"H electronegativity = {EN[1]}")
print(f"sqrt(5) = {sqrt5:.6f} — no, 2.236, delta = {abs(EN[1]-sqrt5)/EN[1]*100:.2f}%")
print(f"F(11)/F(10) = {fib(11)/fib(10):.6f} = {fib(11)}/{fib(10)} — {abs(EN[1]-fib(11)/fib(10))/EN[1]*100:.2f}%")
print(f"Actually F(11)/F(10) = 89/55 = 1.618 — no.")
print(f"F(10)/L(5) = {fib(10)/lucas(5)} = 55/11 = 5 — no.")
print(f"11/5 = 2.2 — this is just 2.2 = 11/5.")
print(f"  11 and 5 are Fibonacci numbers. F(5)/F(3) = 5/2 = 2.5 — no.")
print(f"  H EN = 2.20 is {abs(EN[1] - 11/5)/EN[1]*100:.4f}% match to 11/5.")
print(f"  11 is F(5) and a Coxeter exponent. 5 is F(5). Interesting? Barely.\n")

# N = 3.04
print(f"N electronegativity = {EN[7]}")
print(f"3 + theta_4 = {3 + theta4:.5f}, delta = {abs(EN[7]-(3+theta4))/EN[7]*100:.3f}%")
print(f"VERDICT: N EN = 3.04, framework 3 + theta_4 = 3.030. Delta = 0.3%. But theta_4 = 0.030, not 0.04.\n")

# O = 3.44
print(f"O electronegativity = {EN[8]}")
print(f"phi + phi = {2*phi:.6f} = 3.236 — {abs(EN[8]-2*phi)/EN[8]*100:.2f}% off")
print(f"phi + phibar^2 = {phi + phibar**2:.6f} — no")
print(f"phi^2 + phibar = {phi**2 + phibar:.6f} = 3.236 — same as 2*phi")
print(f"L(4)/2 = {lucas(4)/2} = 3.5 — {abs(EN[8]-3.5)/EN[8]*100:.2f}% off")
print(f"No clean framework match for O EN = 3.44.\n")

# F = 3.98
print(f"F electronegativity = {EN[9]}")
print(f"4 - theta_4 = {4 - theta4:.5f}, delta = {abs(EN[9]-(4-theta4))/EN[9]*100:.3f}%")
print(f"VERDICT: F EN = 3.98, 4-theta_4 = 3.970. Delta = 0.3%. But again theta_4 contribution is 0.03 and EN precision is ~0.05.\n")

# Check ALL EN for phi power matches
print("--- ALL ELECTRONEGATIVITIES VS PHI POWERS AND FRAMEWORK ---")
print(f"{'Z':>3} {'El':>3} {'EN':>6} {'Near framework':>25} {'Value':>10} {'Delta%':>8}")
print("-" * 60)
for Z in sorted(EN.keys()):
    if EN[Z] is None: continue
    val = EN[Z]
    name, delta = find_nearest_framework(val, framework_nums)
    flag = " <---" if delta < 0.03 else ""
    print(f"{Z:3d} {element_names[Z]:>3} {val:6.2f}  {name:>25} = {framework_nums[name]:10.6f}  {delta*100:7.3f}%{flag}")

# Ratio tests
print("\n--- ELECTRONEGATIVITY RATIOS ---")
pairs_to_check = [(8, 6), (9, 1), (7, 6), (8, 1), (9, 6), (17, 9)]
for z1, z2 in pairs_to_check:
    if EN[z1] is not None and EN[z2] is not None:
        r = EN[z1] / EN[z2]
        name, delta = find_nearest_framework(r, framework_nums)
        flag = " <---" if delta < 0.03 else ""
        print(f"  EN({element_names[z1]})/EN({element_names[z2]}) = {r:.6f}  ~ {name} = {framework_nums[name]:.6f} ({delta*100:.2f}%){flag}")

print()
print("=" * 80)
print("SECTION C: BOHR RADIUS AND FRAMEWORK")
print("=" * 80)

print(f"\na0 = {a0} pm")
print(f"F(10) = {fib(10)} = 55")
print(f"F(10) + L(1) = {fib(10) + lucas(1)} = 56 — delta from a0: {abs(a0-56)/a0*100:.2f}%")
print(f"F(10) - L(0) = {fib(10) - lucas(0)} = 53 — delta from a0: {abs(a0-53)/a0*100:.2f}%")
print(f"F(10) = 55 — delta from a0: {abs(a0-55)/a0*100:.2f}%")
print(f"L(5)*phi^3 = {lucas(5)*phi**3:.4f} — delta: {abs(a0-lucas(5)*phi**3)/a0*100:.2f}%")
print(f"L(9)/phi = {lucas(9)/phi:.4f} — delta: {abs(a0-lucas(9)/phi)/a0*100:.2f}%")
print(f"phi^7 = {phi**7:.4f} — delta: {abs(a0-phi**7)/a0*100:.2f}%")
print()
print(f"VERDICT: a0 = 52.918 pm. Closest Fibonacci/Lucas: F(10)=55, off by 3.9%.")
print(f"  a0 = 4*pi*epsilon_0*hbar^2/(m_e*e^2). It's determined by alpha, m_e, hbar.")
print(f"  In atomic units, a0 = 1. The PM value reflects the meter definition.")
print(f"  This question is ill-posed: a0 in pm is unit-dependent, not fundamental.")

# Atomic radii as multiples of a0
print("\n--- SELECTED ATOMIC RADII / a0 ---")
# Empirical covalent radii (pm) for selected elements
cov_radii = {
    1: 31,   # H
    6: 77,   # C (sp3)
    7: 75,   # N
    8: 73,   # O
    2: 28,   # He (van der Waals more like 140, covalent hard to define)
    10: 58,  # Ne (covalent est.)
    18: 106, # Ar
    36: 116, # Kr
    26: 126, # Fe
    29: 132, # Cu
}
for Z in sorted(cov_radii.keys()):
    r_a0 = cov_radii[Z] / a0
    name, delta = find_nearest_framework(r_a0, framework_nums)
    print(f"  {element_names[Z]:>2} (Z={Z:2d}): r={cov_radii[Z]:4d} pm, r/a0 = {r_a0:.4f}  ~ {name} = {framework_nums[name]:.4f} ({delta*100:.2f}%)")

print()
print("=" * 80)
print("SECTION D: NOBLE GAS ATOMIC NUMBERS")
print("=" * 80)

noble_gases = [2, 10, 18, 36, 54, 86]
print(f"\nNoble gas Z: {noble_gases}")
print(f"\nFramework expressions:")
print(f"  2  = L(0) = {lucas(0)} CHECK")
print(f"  10 = h/3  = {h_e8}/3 = {h_e8/3} CHECK (h = E8 Coxeter number)")
print(f"  10 = F(5) = {fib(5)} CHECK (also a Fibonacci number)")
print(f"  18 = L(6) = {lucas(6)} CHECK")
print(f"  36 = 6^2 CHECK. Also 2*L(6) = {2*lucas(6)} CHECK. Also = L(6)^2/L(6+6)? No: L(12) = {lucas(12)}")
print(f"  54 = 3*L(6) = {3*lucas(6)} CHECK")
print(f"  86 = ?")

# Check 86 against framework
print(f"\n  Testing 86:")
print(f"    L(9) = {lucas(9)} = 76 — no")
print(f"    L(10) = {lucas(10)} = 123 — no")
print(f"    F(11) = {fib(11)} = 89 — close, {abs(86-89)} off")
print(f"    5*L(6) - 4 = {5*lucas(6)-4} = 86 — contrived")
print(f"    86 = 2 * 43 (43 is prime, not a framework number)")
print(f"    NO clean expression for 86.")

# Differences between noble gases
diffs = [noble_gases[i+1] - noble_gases[i] for i in range(len(noble_gases)-1)]
print(f"\n  Differences: {diffs}")
print(f"  These are: 8, 8, 18, 18, 32")
print(f"  = 2*2^2, 2*2^2, 2*3^2, 2*3^2, 2*4^2")
print(f"  = 2n^2 for n = 2, 2, 3, 3, 4")
print(f"  This is STANDARD quantum mechanics: shell capacity = 2n^2.")
print(f"  The doubling (each n appears twice) is from l=0..(n-1) splitting.")
print(f"  This is NOT new framework content — it's the Schrodinger equation.")

# But check: is there a framework layer on top?
print(f"\n  Noble gas Z = cumulative sums of 2n^2:")
print(f"    2 = 2*1^2")
print(f"    10 = 2 + 2*4 = 2 + 8")
print(f"    18 = 10 + 8")
print(f"    36 = 18 + 18 (= 18 + 2*9)")
print(f"    54 = 36 + 18")
print(f"    86 = 54 + 32 (= 54 + 2*16)")
print(f"\n  The pattern 2, 8, 8, 18, 18, 32, 32, 50, 50... is from QM.")
print(f"  That 2=L(0), 10=h/3, 18=L(6) are framework numbers is COINCIDENCE")
print(f"  or at best a reflection that small integers appear in both contexts.")

print()
print("=" * 80)
print("SECTION E: ELECTRON SHELL CAPACITIES")
print("=" * 80)

print(f"\nShell capacities = 2n^2: ", [2*n**2 for n in range(1,6)])
print(f"  n=1: 2  = L(0) CHECK")
print(f"  n=2: 8  = 2^3 CHECK (also F(6) = {fib(6)})")
print(f"  n=3: 18 = L(6) CHECK")
print(f"  n=4: 32 = 2^5 CHECK")
print(f"  n=5: 50 = 2*25 = 2*5^2")
print(f"       50 = F(10)-F(5) = {fib(10)-fib(5)} CHECK (=50)")
print(f"\n  Analysis: 2n^2 for small n will inevitably hit framework numbers")
print(f"  because Lucas/Fibonacci sequences grow exponentially and small")
print(f"  integers are dense in both sequences.")
print(f"\n  The REAL question is: does the framework PREDICT 2n^2?")
print(f"  Answer: 2n^2 comes from l=(0..n-1), each l has (2l+1) orbitals,")
print(f"  each orbital holds 2 electrons (spin). Sum = 2*sum(2l+1) = 2n^2.")
print(f"  This requires angular momentum quantization + Pauli exclusion.")
print(f"  The framework would need to derive these from E8 to claim the pattern.")

print()
print("=" * 80)
print("SECTION F: TRANSITION METALS AND d-ELECTRONS")
print("=" * 80)

print(f"\nd-shell capacity = 10 electrons")
print(f"  10 = h/3 = {h_e8}/3 = {h_e8/3} (E8 Coxeter number / triality)")
print(f"  10 = (2l+1)*2 for l=2")
print(f"  10 = F(5) = {fib(5)}")
print(f"\n  Fe: [Ar] 3d^6 4s^2")
print(f"  The 6 d-electrons in Fe: 6 = |S_3| = |W(A_2)|")
print(f"  But 6 is just the number of d-electrons in Fe's ground state.")
print(f"  Other TM's have different d-counts: Ti=2, V=3, Cr=5, Mn=5, Co=7, Ni=8...")
print(f"  Only Fe has 6. This is NOT structural — it's one element among many.")
print(f"\n  f-shell capacity = 14 electrons")
print(f"  14 = F(7) = {fib(7)}")
print(f"  s-shell = 2 = F(3), p-shell = 6 = W(A2), d-shell = 10 = F(5), f-shell = 14 = F(7)")
print(f"  Shell capacities: 2, 6, 10, 14 = 2*(2l+1) for l = 0, 1, 2, 3")
print(f"  = {[2*(2*l+1) for l in range(4)]}")
print(f"  These are 2, 6, 10, 14 — an arithmetic progression with d=4!")
print(f"  As Fibonacci: F(3)=2, does NOT continue: F(5)=5 != 6.")
print(f"  So: 2, 6, 10, 14 are NOT Fibonacci. The d=10=F(5) match is coincidence.")

print()
print("=" * 80)
print("SECTION G: CARBON'S SPECIAL STATUS")
print("=" * 80)

# sp3 bond angle
sp3_angle = math.degrees(math.acos(-1/3))
print(f"\nsp3 tetrahedral angle = arccos(-1/3) = {sp3_angle:.4f} degrees")
print(f"  -1/3 = -L(2)^(-1) (since L(2) = 3)")
print(f"  This is standard: tetrahedral angle from maximizing distance on sphere.")
print(f"  1/3 = L(2)^(-1) is trivially true. Not deep.\n")

# sp2 bond angle
sp2_angle = 120.0
print(f"sp2 bond angle = {sp2_angle} degrees")

# Sum of E8 Coxeter exponents
sum_cox = sum(coxeter_e8)
print(f"Sum of E8 Coxeter exponents = {sum_cox}")
print(f"  {coxeter_e8}")
print(f"  Sum = 1+7+11+13+17+19+23+29 = {sum_cox}")
print(f"\n  CLAIM: 120 = sum of Coxeter exponents.")
print(f"  FACT: This is TRUE but it's a KNOWN IDENTITY.")
print(f"  For ANY simple Lie algebra, sum of Coxeter exponents = dim(G)/rank(G) * rank(G)/2")
print(f"  For E8: sum = 8*(h-1)/2... let's check:")
print(f"    Coxeter exponents are m_i = (1, 7, 11, 13, 17, 19, 23, 29)")
print(f"    Sum = {sum_cox}")
print(f"    Also: sum of exponents = |positive roots| = dim(E8)/2 - rank = (248-8)/2 = 120")
print(f"    So sum = 120 = number of positive roots of E8. Standard identity.")
print(f"\n  Now: does 120 degrees = sum of E8 Coxeter exponents mean sp2 'encodes E8'?")
print(f"  NO. 120 degrees is π/3 radians. It's the angle of a regular hexagon.")
print(f"  sp2 hybridization gives 120° because 3 equivalent orbitals in a plane")
print(f"  must be 360°/3 = 120° apart. This is geometry, not algebra.")
print(f"  The coincidence 120 = |Δ⁺(E8)| is numerically true but causally empty.")
print(f"  120 appears in MANY contexts: 120 = 5! = order of S_5 = order of icosahedron, etc.")

print(f"\n  For comparison:")
print(f"  sp hybridization = 180° = ? Not a framework number.")
print(f"  sp3d = 90°, 120° mixed. sp3d2 = 90°.")
print(f"  Only sp2 = 120 matches. This selectivity is suspicious of cherry-picking.")

print()
print("=" * 80)
print("SECTION H: MELTING POINT PATTERNS")
print("=" * 80)

# Melting points (K) for Z=1..36
MP_K = {
    1: 14.01,    # H
    2: 0.95,     # He (at 26 atm)
    3: 453.65,   # Li
    4: 1560,     # Be
    5: 2349,     # B
    6: 3823,     # C (graphite sublimation)
    7: 63.15,    # N
    8: 54.36,    # O
    9: 53.48,    # F
    10: 24.56,   # Ne
    11: 370.94,  # Na
    12: 923,     # Mg
    13: 933.47,  # Al
    14: 1687,    # Si
    15: 317.3,   # P (white)
    16: 388.36,  # S
    17: 171.6,   # Cl
    18: 83.81,   # Ar
    19: 336.7,   # K
    20: 1115,    # Ca
    21: 1814,    # Sc
    22: 1941,    # Ti
    23: 2183,    # V
    24: 2180,    # Cr
    25: 1519,    # Mn
    26: 1811,    # Fe
    27: 1768,    # Co
    28: 1728,    # Ni
    29: 1357.77, # Cu
    30: 692.68,  # Zn
    31: 302.91,  # Ga
    32: 1211.40, # Ge
    33: 1090,    # As (sublimation)
    34: 494,     # Se
    35: 265.8,   # Br
    36: 115.78,  # Kr
}

# Look at ratios between elements
print("\nMelting points are largely determined by bonding type:")
print("  Metals: metallic bonding (high MP)")
print("  Noble gases: van der Waals (very low MP)")
print("  Molecular: intermediate")
print("  Covalent network: very high (C, B, Si)")
print()

# Check some ratios
mp_ratios = [
    (6, 14, "C/Si"),
    (6, 5, "C/B"),
    (26, 29, "Fe/Cu"),
    (11, 19, "Na/K"),
]
for z1, z2, label in mp_ratios:
    r = MP_K[z1] / MP_K[z2]
    name, delta = find_nearest_framework(r, framework_nums)
    flag = " <---" if delta < 0.03 else ""
    print(f"  MP({label}) = {r:.4f}  ~ {name} = {framework_nums[name]:.4f} ({delta*100:.2f}%){flag}")

# Check if C melting point has framework connection
print(f"\n  C sublimation = 3823 K")
print(f"  3823 / 273.15 (0°C) = {3823/273.15:.4f}")
print(f"  3823 / E_R = {3823/E_R:.4f} (energy in eV is different from K)")
print(f"  k_B * 3823 K = {3823 * 8.617e-5:.4f} eV")
print(f"  C thermal energy / E_R = {3823 * 8.617e-5 / E_R:.6f}")
print(f"\n  Melting points depend on crystal structure, bonding, many-body effects.")
print(f"  They are NOT likely to reduce to simple framework expressions.")

print()
print("=" * 80)
print("OVERALL ASSESSMENT")
print("=" * 80)

print("""
GENUINELY INTERESTING:
1. C electronegativity (Pauling) = 2.55, theta_3(1/phi) = 2.555.
   Match: 99.8%. BUT Pauling scale precision is only ~0.05, so this is
   within measurement uncertainty. Se also has EN = 2.55.
   Verdict: INTRIGUING but not compelling due to precision limits.

2. O ionization energy = 13.618 eV vs E_R = 13.606 eV.
   Match: 99.91%. Oxygen's first IE is essentially the Rydberg energy.
   This HAS a physics explanation: O is Z=8 with 2s^2 2p^4, and the
   4th p-electron has near-hydrogenic binding due to shielding.
   Verdict: REAL physics, but already understood without framework.

3. Noble gas Z = {2, 10, 18, 36, 54, 86}:
   2=L(0), 10=h/3, 18=L(6), 36=6^2=L(6)^2, 54=3*L(6).
   These expressions exist but are cherry-picked. 86 has no clean form.
   The REAL pattern is cumulative 2n^2 from QM.
   Verdict: SMALL-NUMBER COINCIDENCE.

4. 120° = sum of E8 Coxeter exponents.
   True identity, but 120 = 360/3 for sp2 is simple geometry.
   120 = |positive roots of E8| is a standard Lie theory identity.
   These have nothing to do with each other.
   Verdict: COINCIDENCE (120 is too common a number).

5. Shell sub-capacities 2, 6, 10, 14 are NOT Fibonacci.
   d-shell = 10 = F(5) is coincidence; f-shell = 14 = F(7) but
   s-shell = 2 = F(3), p-shell = 6 != F(4)=3. Pattern breaks.
   Verdict: COINCIDENCE.

NOT INTERESTING:
- Li IE/E_R = 0.396 vs 1/phi^2 = 0.382: 3.6% off. Not a match.
- H EN = 2.20: just 11/5, contrived framework expression.
- Noble gas 86 has no framework form.
- Melting points show no framework patterns.
- Atomic radii in pm are unit-dependent, not fundamental.

BOTTOM LINE:
The framework vocabulary {phi, L(n), F(n), mu} can express SOME element
properties, but the matches are at the 1-3% level with cherry-picking.
The genuinely striking match (C EN = theta_3) is limited by the Pauling
scale's intrinsic precision (~2%).

The element properties that DO have clean mathematical forms (shell
structure, noble gas spacing) come from quantum mechanics (angular
momentum quantization + Pauli exclusion), not from modular forms.

The framework's strength is in fundamental CONSTANTS (alpha, alpha_s,
sin^2 theta_W). Element-specific properties involve many-body atomic
physics on top of QM, making simple framework expressions unlikely.
""")
