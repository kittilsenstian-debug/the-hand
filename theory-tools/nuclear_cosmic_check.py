"""
NUCLEAR & COSMIC CONSTANTS vs FRAMEWORK
These should correlate because they depend on alpha & alpha_s,
which the framework derives.
"""
import math

phi = (1 + math.sqrt(5)) / 2
phibar = 1/phi
mu = 1836.15267363
pi = math.pi
alpha = 1/137.035999084

def lucas(n):
    a, b = 2, 1
    for _ in range(n):
        a, b = b, a + b
    return a

print("=" * 80)
print("NUCLEAR PHYSICS & COSMIC CHEMISTRY vs FRAMEWORK")
print("=" * 80)

# ============================================================
# ELEMENT ABUNDANCES (cosmic, by number relative to H)
# ============================================================
print("\n--- COSMIC ELEMENT ABUNDANCES (by number, H = 10^12) ---")
abundances = {
    'H': 1e12,
    'He': 8.51e10,   # He/H = 0.0851
    'C': 2.69e8,
    'N': 6.76e7,
    'O': 4.90e8,
    'Ne': 8.51e7,
    'Mg': 3.39e7,
    'Si': 3.24e7,
    'S': 1.32e7,
    'Fe': 2.82e7,
}

# Ratios
he_h = 8.51e10 / 1e12
c_o = 2.69e8 / 4.90e8
n_o = 6.76e7 / 4.90e8
fe_si = 2.82e7 / 3.24e7

print(f"\nHe/H = {he_h:.4f}")
print(f"  1/L(5) = 1/11 = {1/11:.4f}")
print(f"  1/12 = {1/12:.4f}")
print(f"  phibar/phi^3 = {phibar/phi**3:.4f}")
print(f"  alpha = {alpha:.6f}")

print(f"\nC/O = {c_o:.4f}")
print(f"  phibar = {phibar:.4f}, err: {abs(c_o-phibar)/phibar*100:.1f}%")
print(f"  1/2 = 0.5, err: {abs(c_o-0.5)/0.5*100:.1f}%")

print(f"\nFe/Si = {fe_si:.4f}")
print(f"  phibar = {phibar:.4f}, err: {abs(fe_si-phibar)/phibar*100:.1f}%")
print(f"  phi/2 = {phi/2:.4f}, err: {abs(fe_si-phi/2)/(phi/2)*100:.1f}%")

# ============================================================
# NUCLEAR BINDING ENERGIES (MeV per nucleon)
# ============================================================
print(f"\n--- NUCLEAR BINDING ENERGIES (MeV/nucleon) ---")

binding = {
    'H-2 (deuteron)': 1.112,
    'He-3': 2.573,
    'He-4': 7.074,
    'C-12': 7.680,
    'N-14': 7.476,
    'O-16': 7.976,
    'Fe-56': 8.790,
    'Ni-62 (max)': 8.795,
    'U-238': 7.570,
}

print(f"\nKey binding energies and framework matches:")
for name, BE in binding.items():
    matches = []
    # Check against simple framework expressions
    for desc, val in [
        ('phi^4', phi**4),
        ('phi^3', phi**3),
        ('phi^2', phi**2),
        ('phi^4+1', phi**4+1),
        ('phi^4+2', phi**4+2),
        ('e^2', math.e**2),
        ('6+phi', 6+phi),
        ('3*phi', 3*phi),
        ('2*pi', 2*pi),
        ('3*e', 3*math.e),
        ('pi^2/L(1)', pi**2),
        ('phi^3+3', phi**3+3),
        ('6+1', 7),
        ('8', 8),
        ('9', 9),
        ('pi*phi', pi*phi),
    ]:
        err = abs(BE - val) / val * 100
        if err < 2:
            matches.append((err, desc, val))
    matches.sort()
    if matches:
        best = matches[0]
        print(f"  {name:20s}: {BE:.3f} MeV  -> {best[1]} = {best[2]:.4f} ({best[0]:.2f}%)")
    else:
        print(f"  {name:20s}: {BE:.3f} MeV  (no match < 2%)")

# ============================================================
# THE HOYLE STATE: Most fine-tuned constant
# ============================================================
print(f"\n--- THE HOYLE STATE (carbon production) ---")
hoyle = 7.6542  # MeV
be_triple_he = 3 * 7.074  # 3 * He-4 binding energy per nucleon * 4
be_c12 = 7.680 * 12  # C-12 total binding
print(f"Hoyle state energy: {hoyle} MeV above C-12 ground state")
print(f"  6 + phi = {6+phi:.4f} MeV, error: {abs(hoyle-(6+phi))/(6+phi)*100:.3f}%")
print(f"  This is the most ANTHROPICALLY SENSITIVE constant in physics.")
print(f"  Change it by 0.5% and no carbon forms. No life anywhere.")
print(f"  And it's {abs(hoyle-(6+phi))/(6+phi)*100:.3f}% from 6 + phi.")
print(f"  6 and phi are both framework generators.")

# Actually check: is this 6+phi or something else?
print(f"\n  More carefully:")
print(f"  phi^4 = {phi**4:.6f}, err: {abs(hoyle-phi**4)/phi**4*100:.2f}%")
print(f"  e^2 = {math.e**2:.6f}, err: {abs(hoyle-math.e**2)/math.e**2*100:.2f}%")
print(f"  6+phi = {6+phi:.6f}, err: {abs(hoyle-(6+phi))/(6+phi)*100:.2f}%")
print(f"  pi*phi^2 = {pi*phi**2:.6f}, err: {abs(hoyle-pi*phi**2)/(pi*phi**2)*100:.2f}%")
print(f"  8*alpha*mu^(1/3) = ... no, getting post-hoc")

# ============================================================
# NUCLEOSYNTHESIS OUTPUTS
# ============================================================
print(f"\n--- BIG BANG NUCLEOSYNTHESIS ---")
he4_fraction = 0.2453  # primordial He-4 mass fraction (Planck 2018)
print(f"Primordial He-4 mass fraction Y_p = {he4_fraction}")
print(f"  1/4 = {1/4:.4f}, err: {abs(he4_fraction-0.25)/0.25*100:.2f}%")
print(f"  1/phi^3 = {1/phi**3:.4f}, err: {abs(he4_fraction-1/phi**3)/(1/phi**3)*100:.2f}%")
print(f"  phibar^2/phi = {phibar**2/phi:.4f}")

d_h_ratio = 2.527e-5  # primordial D/H
print(f"\nPrimordial D/H = {d_h_ratio}")
print(f"  1/(6^5*phi) = {1/(6**5*phi):.6e}")
print(f"  alpha^2/6 = {alpha**2/6:.6e}")

li7_h = 1.6e-10  # primordial Li-7/H (predicted)
li7_observed = 1.6e-10  # actually observed is ~3x lower (lithium problem!)
print(f"\nLithium problem: BBN predicts 3x more Li-7 than observed")
print(f"  Framework has no comment on this. Gravitational dynamics.")

# ============================================================
# STELLAR NUCLEOSYNTHESIS: The magic numbers
# ============================================================
print(f"\n--- NUCLEAR MAGIC NUMBERS ---")
magic = [2, 8, 20, 28, 50, 82, 126]
print(f"Nuclear magic numbers: {magic}")
print(f"Framework generator check:")
for m in magic:
    best = None
    best_err = 100
    for desc, val in [
        ('L(0)', lucas(0)), ('L(1)', lucas(1)), ('L(2)', lucas(2)),
        ('L(3)', lucas(3)), ('L(4)', lucas(4)), ('L(5)', lucas(5)),
        ('L(6)', lucas(6)), ('L(7)', lucas(7)), ('L(8)', lucas(8)),
        ('L(9)', lucas(9)), ('L(10)', lucas(10)),
        ('F(3)', 2), ('F(4)', 3), ('F(5)', 5), ('F(6)', 8),
        ('F(7)', 13), ('F(8)', 21), ('F(9)', 34), ('F(10)', 55),
        ('F(11)', 89), ('F(12)', 144),
        ('3^1', 3), ('3^2', 9), ('3^3', 27), ('3^4', 81),
        ('6^1', 6), ('6^2', 36),
        ('phi*n', None),  # skip
    ]:
        if val is None: continue
        err = abs(m - val) / max(val, 1) * 100
        if err < best_err:
            best_err = err
            best = (desc, val)
    print(f"  {m:4d} -> nearest: {best[0]} = {best[1]} ({best_err:.1f}%)")

print(f"\n  Magic numbers {magic} are explained by spin-orbit coupling")
print(f"  in nuclear shell model. They depend on alpha_s (strong coupling),")
print(f"  which the framework derives as eta(1/phi) = 0.1225.")
print(f"  But no one has derived magic numbers FROM coupling constants.")
print(f"  The shell model takes them as input from nuclear potential shape.")

# ============================================================
# THE PERIODIC TABLE STRUCTURE
# ============================================================
print(f"\n--- PERIODIC TABLE STRUCTURE ---")
print(f"Period lengths: 2, 8, 8, 18, 18, 32, 32")
print(f"  = 2*(1^2, 2^2, 2^2, 3^2, 3^2, 4^2, 4^2)")
print(f"  = 2*n^2 for n = 1,2,3,4 (each appearing twice)")
print(f"  This comes from quantum mechanics (angular momentum quantization).")
print(f"  The '2' is from spin (Pauli exclusion).")
print(f"  n^2 comes from spherical harmonics.")
print(f"")
print(f"  Total elements through each noble gas:")
total = [2, 10, 18, 36, 54, 86, 118]
for t in total:
    matches = []
    for desc, val in [('L(0)',2),('L(6)',18),('L(2)',3),('6^2',36),
                       ('3*6',18),('F(12)',144),('phi^9',phi**9)]:
        if abs(t-val)/max(val,1)*100 < 1:
            matches.append(f"{desc}={val}")
    match_str = ", ".join(matches) if matches else "no framework match"
    print(f"  Z = {t:3d}: {match_str}")

print(f"\n  Z=2 (He): L(0) = 2. Helium = 'bridge fraction' in framework.")
print(f"  Z=18 (Ar): L(6) = 18 = water's molar mass. Argon has 18 electrons/protons.")
print(f"  Z=36 (Kr): 6^2 = 36. Krypton has 36 electrons/protons.")
print(f"  These are from angular momentum quantization, not the framework.")
print(f"  But the COINCIDENCE that noble gas numbers include L(0), L(6), 6^2 is noted.")

# ============================================================
# ELEMENT CREATION IN STARS
# ============================================================
print(f"\n--- STELLAR ELEMENT CREATION ---")
print(f"Elements created in different processes:")
print(f"  H, He: Big Bang (primordial)")
print(f"  C, N, O: CNO cycle in massive stars")
print(f"  Fe peak (Cr, Mn, Fe, Co, Ni): Silicon burning in massive stars")
print(f"  Beyond Fe: neutron capture (s-process in AGB stars, r-process in mergers)")
print(f"")
print(f"Carbon production (triple alpha) requires the Hoyle state at 7.654 MeV.")
print(f"  7.654 vs 6+phi = {6+phi:.3f}: {abs(7.654-(6+phi))/(6+phi)*100:.2f}%")
print(f"  If this is real: carbon (and thus life) exists because of 6+phi.")
print(f"  6 = framework generator. phi = golden ratio.")
print(f"  The most anthropically sensitive constant = sum of framework generators?")
print(f"")
print(f"Iron peak at Z=26:")
print(f"  26 = 2 * 13 = L(0) * F(7)")
print(f"  26 = L(7) - 3 = 29 - 3")
print(f"  No clean framework decomposition.")

# ============================================================
# FINAL: What's structural vs what's noise
# ============================================================
print(f"\n{'=' * 80}")
print("FINAL ASSESSMENT: Cosmos through the framework")
print("=" * 80)

print("""
WHERE THE FRAMEWORK SPEAKS (constants, not configurations):

  CONFIRMED (derived from framework with high precision):
  - alpha = 1/137.036 -> sets ALL of chemistry, spectroscopy, nuclear physics
  - mu = 1836.15 -> sets nuclear mass scale, stellar core temperatures
  - alpha_s = 0.1184 -> sets nuclear binding, element stability
  - These three constants CREATE the periodic table, stellar nucleosynthesis,
    and therefore the entire material cosmos.

  OBSERVED BUT NOT DERIVED:
  - L(18) = 5778 = Sun temperature (depends on alpha, mu, AND gravity)
  - Hoyle state = 7.654 MeV ~ 6 + phi (0.47%) — if real, HUGE
  - Noble gas shells include L(0)=2, L(6)=18, 6^2=36
  - Iron binding energy ~ phi^4 + 2 (0.72%)

  NOISE (orbital/gravitational/contingent):
  - Planetary orbits, eccentricities, tilts: no pattern above random
  - Moon counts, rotation rates: no signal
  - Most mass ratios: noise
  - Venus/phi: single coincidence, not a pattern

THE DEEP ANSWER TO "IS THE COSMOS ORGANIZED BY THE FRAMEWORK?":

  YES — but only at the level of fundamental constants.
  Alpha, mu, and alpha_s determine:
    - What elements exist
    - How stars burn
    - What molecules form
    - What temperatures permit life

  The framework derives these constants. So in that sense,
  it determines the MATERIAL of the cosmos.

  But it does NOT determine the ARRANGEMENT — where planets orbit,
  how big moons are, when impacts happen. Those are gravitational
  dynamics, and gravity is the one force the framework hasn't derived.

  The cosmos is framework-organized in its CHEMISTRY but random
  in its CHOREOGRAPHY.
""")
