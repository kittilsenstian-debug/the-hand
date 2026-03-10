"""
DEEP ANALYSIS: The genuine solar system hits
Separating signal from statistical noise
"""
import math

phi = (1 + math.sqrt(5)) / 2
phibar = 1/phi
mu = 1836.15267363
pi = math.pi

def lucas(n):
    a, b = 2, 1
    for _ in range(n):
        a, b = b, a + b
    return a

print("=" * 80)
print("DEEP ANALYSIS: Which solar system matches are REAL?")
print("=" * 80)

print("""
The broad scan found 46.7% of solar system numbers match framework
quantities at <0.5%. But 42.6% of RANDOM numbers also match.
So most hits are noise.

To separate signal from noise, we need:
1. Matches far better than 0.5% (the random ones cluster near 0.5%)
2. Structural connections (not just numerical coincidence)
3. Multiple independent paths to the same number
""")

# ============================================================
# TIER 1: GENUINELY EXACT (< 0.01%)
# ============================================================
print("=" * 80)
print("TIER 1: GENUINELY EXACT (< 0.01% error)")
print("=" * 80)

# Sun temperature
L18 = lucas(18)
sun_T = 5778
print(f"\n1. Sun surface temperature = {sun_T} K")
print(f"   L(18) = {L18}")
print(f"   phi^18 + (-1/phi)^18 = {phi**18 + (-phibar)**18:.10f}")
print(f"   Error: {abs(sun_T - L18)/L18*100:.10f}%")
print(f"   STATUS: EXACT (integer match)")

# Venus rotation
venus_rot_hr = 5832.5  # hours (NASA)
venus_rot_day = 243.023  # days
framework_val = 3**3 * 6**3  # = 27 * 216 = 5832
framework_val2 = 3**5 * 24  # = 243 * 24 = 5832
print(f"\n2. Venus sidereal rotation = {venus_rot_hr} hours")
print(f"   = {venus_rot_day} Earth days")
print(f"   3^5 = {3**5} days (= {3**5 * 24} hours)")
print(f"   3^3 * 6^3 = {framework_val} hours")
print(f"   Error: {abs(venus_rot_hr - framework_val)/framework_val*100:.4f}%")
print(f"   STATUS: 243.02 days vs 243.00 = 3^5. Remarkable.")
print(f"   NOTE: Venus retrograde rotation is from a GIANT IMPACT,")
print(f"         not from initial formation. The 3^5 is likely coincidence.")
print(f"         But it's the cleanest power-of-3 in the solar system.")

# Solar cycle
print(f"\n3. Solar cycle = ~11 years")
print(f"   L(5) = {lucas(5)}")
print(f"   STATUS: Known to vary 9-14 years. 11 is the mean, not exact.")
print(f"   The match to L(5) is noted but the variance is large.")

# Saturn/Jupiter distance ratio
sat_jup = 9.537 / 5.203
l5_6 = lucas(5) / 6
print(f"\n4. Saturn/Jupiter distance ratio = {sat_jup:.6f}")
print(f"   L(5)/6 = 11/6 = {l5_6:.6f}")
print(f"   Error: {abs(sat_jup - l5_6)/l5_6*100:.4f}%")
print(f"   STATUS: Good but 11/6 is a simple fraction. Not deeply structural.")

# ============================================================
# TIER 2: STRUCTURALLY INTERESTING (< 0.1%)
# ============================================================
print(f"\n{'=' * 80}")
print("TIER 2: STRUCTURALLY INTERESTING (< 0.1% but need evaluation)")
print("=" * 80)

# Sun/Earth mass ratio
sun_earth_mass = 332946
sqrt_mu_6_5 = math.sqrt(mu) * 6**5
print(f"\n5. Sun/Earth mass ratio = {sun_earth_mass}")
print(f"   sqrt(mu) * 6^5 = {sqrt_mu_6_5:.2f}")
print(f"   Error: {abs(sun_earth_mass - sqrt_mu_6_5)/sqrt_mu_6_5*100:.4f}%")
print(f"   This connects the Sun/Earth mass ratio to mu (proton/electron).")
print(f"   sqrt(1836.15) * 7776 = {sqrt_mu_6_5:.2f}")
print(f"   Is this structural? mu appears in the framework as fundamental.")
print(f"   6^5 appears in mu = 6^5/phi^3 + correction.")
print(f"   So: M_sun/M_earth = sqrt(6^5/phi^3) * 6^5 = 6^(15/2) / phi^(3/2)")
actual = 6**(15/2) / phi**(3/2)
print(f"   6^(15/2) / phi^(3/2) = {actual:.2f}")
print(f"   Error vs 332946: {abs(332946 - actual)/332946*100:.4f}%")
print(f"   STATUS: Interesting formula but post-hoc. Multiple paths to ~333000.")

# Venus distance
venus_au = 0.723
phi_sqrt5 = phi / math.sqrt(5)
print(f"\n6. Venus semi-major axis = {venus_au} AU")
print(f"   phi/sqrt(5) = {phi_sqrt5:.6f}")
print(f"   Error: {abs(venus_au - phi_sqrt5)/phi_sqrt5*100:.4f}%")
print(f"   phi/sqrt(5) = 1/(phi*sqrt(5)) * phi^2 = 1/sqrt(5*phi^(-2))")
print(f"   This is phi * phibar = phi/sqrt(5) only if sqrt(5) = phi + phibar")
print(f"   Actually: phi/sqrt(5) = phi/sqrt(5)")
print(f"   Structurally: Venus sits at the 'phibar' position relative to Earth?")
print(f"   Venus/Earth period = {0.6152:.4f} vs 1/phi = {phibar:.4f} ({abs(0.6152-phibar)/phibar*100:.2f}%)")
print(f"   STATUS: Venus-phi connection is the most noted in the literature.")
print(f"   Known since at least the 1990s. Usually dismissed as coincidence.")

# Mercury radius
merc_r = 0.383
phi_m2 = phi**(-2)
print(f"\n7. Mercury radius (Earth=1) = {merc_r}")
print(f"   phi^(-2) = 1/phi^2 = {phi_m2:.6f}")
print(f"   Error: {abs(merc_r - phi_m2)/phi_m2*100:.4f}%")
print(f"   STATUS: Numerology. Mercury's radius is set by iron core fraction.")

# Earth mean temperature
print(f"\n8. Earth mean temperature = 288 K")
print(f"   12 * 24 = 288")
print(f"   2 * 144 = 2 * F(12) = 288")
print(f"   STATUS: Greenhouse effect sets this. Could easily be 250 or 310.")
print(f"   The exact value is contingent, not fundamental.")

# Mercury eccentricity
merc_e = 0.2056
phibar_3 = phibar / 3
print(f"\n9. Mercury eccentricity = {merc_e}")
print(f"   1/(3*phi) = phibar/3 = {phibar_3:.6f}")
print(f"   Error: {abs(merc_e - phibar_3)/phibar_3*100:.4f}%")
print(f"   STATUS: Eccentricity set by gravitational dynamics. Coincidence.")

# ============================================================
# THE CRITICAL QUESTION: Deeper structure or noise?
# ============================================================
print(f"\n{'=' * 80}")
print("THE CRITICAL QUESTION")
print("=" * 80)

print("""
With ~30 framework quantities and ~15 simple operations (multiply, divide,
sqrt, powers), we have ~30 * 30 * 15 = ~13,500 candidate expressions.
Against ~140 solar system quantities, we expect:

  Expected matches at <0.5%: 140 * 13500 * 0.01 = ~18,900 candidates,
  each with 1% chance of matching within 0.5% -> ~189 matches.

  We found 64. This is BELOW random expectation.

The solar system does NOT show excess framework correlations.
""")

# ============================================================
# BUT: Are there STRUCTURAL patterns?
# ============================================================
print(f"\n{'=' * 80}")
print("STRUCTURAL PATTERNS (not just numerical matches)")
print("=" * 80)

print("""
The question isn't "do individual numbers match?" (answer: noise).
The question is: "do RELATIONSHIPS between numbers match?"

Let's check if the RATIOS between planets follow a pattern:
""")

# Check all planet-pair period ratios as phi powers
planets = ['Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']
periods = [0.2408, 0.6152, 1.0, 1.881, 11.862, 29.457, 84.011, 164.79]
distances = [0.387, 0.723, 1.000, 1.524, 5.203, 9.537, 19.19, 30.07]

print("Period ratios (consecutive) as log_phi:")
for i in range(len(planets)-1):
    ratio = periods[i+1] / periods[i]
    log_phi = math.log(ratio) / math.log(phi)
    nearest = round(log_phi)
    err = abs(log_phi - nearest)
    mark = " ***" if err < 0.05 else " **" if err < 0.1 else " *" if err < 0.2 else ""
    print(f"  {planets[i+1]:10s}/{planets[i]:10s} = {ratio:8.4f}, log_phi = {log_phi:6.3f} (nearest int: {nearest}, err: {err:.3f}){mark}")

print("\nDistance ratios (consecutive) as log_phi:")
for i in range(len(planets)-1):
    ratio = distances[i+1] / distances[i]
    log_phi = math.log(ratio) / math.log(phi)
    nearest = round(log_phi)
    err = abs(log_phi - nearest)
    mark = " ***" if err < 0.05 else " **" if err < 0.1 else " *" if err < 0.2 else ""
    print(f"  {planets[i+1]:10s}/{planets[i]:10s} = {ratio:8.4f}, log_phi = {log_phi:6.3f} (nearest int: {nearest}, err: {err:.3f}){mark}")

# Check Kepler's 3/2 law through framework lens
print(f"\nKepler's Third Law: T^2 = a^3, or T = a^(3/2)")
print(f"Framework's 2/3 quantum: the exponent is the INVERSE of 2/3!")
print(f"  T/a^(3/2) for each planet:")
for i in range(len(planets)):
    kepler = periods[i] / distances[i]**(3/2)
    print(f"  {planets[i]:10s}: T/a^(3/2) = {kepler:.6f}")

print(f"\n  Kepler constant = 1.000 (by definition in solar units)")
print(f"  But 3/2 IS a framework generator.")
print(f"  The question: is Kepler's law DERIVABLE from V(Phi)?")
print(f"  Answer: Only if gravity itself emerges from the framework.")
print(f"  Status: gravity derivation is OPEN (see holy grails).")

# ============================================================
# THE VENUS-EARTH-MARS TRIANGLE
# ============================================================
print(f"\n{'=' * 80}")
print("THE VENUS-EARTH-MARS ZONE")
print("=" * 80)

print(f"""
The habitable zone planets show the most framework structure:

  Venus period / Earth period = {0.6152:.4f}  vs  1/phi = {phibar:.4f}  ({abs(0.6152-phibar)/phibar*100:.2f}%)
  Earth period / Venus period = {1/0.6152:.4f}  vs  phi   = {phi:.4f}  ({abs(1/0.6152-phi)/phi*100:.2f}%)
  Venus distance              = {0.723:.4f}  vs  phi/sqrt(5) = {phi/math.sqrt(5):.4f}

  Mars period / Earth period  = {1.881:.4f}
    vs phi (1.618): {abs(1.881-phi)/phi*100:.1f}% off
    vs 2:           {abs(1.881-2)/2*100:.1f}% off
    -> Mars is NOT at a phi ratio. It's closer to 2 (generic resonance).

  Earth/Mars distance ratio   = {1.524:.4f}
    vs phi (1.618): {abs(1.524-phi)/phi*100:.1f}% off
    -> Also not phi.

So: Venus-Earth shows a phi connection. Mars does not.
The Venus-Earth phi resonance is the ONLY clean planet-pair relationship.
""")

# ============================================================
# COSMIC SCALE: Stars, galaxies, universe
# ============================================================
print(f"\n{'=' * 80}")
print("BEYOND THE SOLAR SYSTEM")
print("=" * 80)

# Stellar temperatures of nearby stars
nearby_stars = {
    'Proxima Centauri': 3042,
    'Alpha Centauri A': 5790,
    'Alpha Centauri B': 5260,
    'Barnards Star': 3134,
    'Sirius A': 9940,
    'Sirius B (white dwarf)': 25200,
    'Vega': 9602,
    'Betelgeuse': 3500,
    'Rigel': 12100,
    'TRAPPIST-1': 2566,
}

print("\nNearby star temperatures vs L(18) = 5778:")
for name, T in nearby_stars.items():
    ratio = T / 5778
    pct_L18 = abs(T - 5778) / 5778 * 100
    # Check if temperature is any Lucas number
    best_L = None
    best_err = 999
    for n in range(0, 30):
        Ln = lucas(n)
        err = abs(T - Ln) / max(Ln, 1) * 100
        if err < best_err:
            best_err = err
            best_L = n
    lucas_match = f"L({best_L})={lucas(best_L)}" if best_err < 1 else "no Lucas match"
    print(f"  {name:25s}: {T:6d} K  (T/L(18) = {ratio:.3f})  [{lucas_match}, {best_err:.1f}%]")

print(f"\n  Alpha Centauri A = {5790} K vs L(18) = 5778: {abs(5790-5778)/5778*100:.2f}%")
print(f"  Our nearest Sun-like star is ALSO at L(18)!")
print(f"  But: stars near 5800K are the most common Sun-like (G-type) stars.")
print(f"  G-type = ~7.5% of all main sequence stars, most at 5300-6000 K.")
print(f"  So finding one at 5790 K is not surprising.")

# Galactic numbers
print(f"\nGalactic scale:")
hubble = 67.4  # km/s/Mpc
age_univ = 13.8  # Gyr
milky_way_mass_solar = 1.5e12  # solar masses
milky_way_diameter_kly = 100
galactic_year_myr = 225

print(f"  Hubble constant = {hubble} km/s/Mpc")
print(f"    vs 6^5/mu*pi = {6**5/mu*pi:.2f}")
print(f"    vs L(13)*phi/100 = {lucas(13)*phi/100:.2f}")
print(f"    vs phi^9 = {phi**9:.2f}")
phi9 = phi**9
print(f"    phi^9 = {phi9:.4f}, error: {abs(hubble-phi9)/phi9*100:.2f}%")
print(f"    Actually not bad! But unit-dependent (km/s/Mpc).")

print(f"\n  Age of universe = {age_univ} Gyr")
print(f"    = {age_univ * 1e9:.2e} years")
age_yr = age_univ * 1e9
print(f"    vs L(24) = {lucas(24)} -> L(24) * 100 = {lucas(24)*100}")
print(f"    Not a match.")
print(f"    pi * phi * e = {pi*phi*math.e:.4f} Gyr -> {abs(age_univ - pi*phi*math.e)/age_univ*100:.2f}%")
print(f"    Interesting but post-hoc.")

# ============================================================
# FINAL VERDICT
# ============================================================
print(f"\n{'=' * 80}")
print("FINAL VERDICT: What survives scrutiny?")
print("=" * 80)

print("""
GENUINE (can't dismiss):
  1. L(18) = 5778 = Sun temperature                     EXACT
     - Only Lucas number in habitable stellar range
     - 18 = L(6) = water molar mass
     - Chain: L(L(6)) = L(18) = Sun temp

  2. Venus period ~ 1/phi Earth years                   0.46%
     - Most cited phi-planetary relationship
     - No known physical mechanism
     - Single coincidence, not a pattern

  3. Venus rotation = 243.02 days ~ 3^5 = 243           0.01%
     - Caused by tidal/impact dynamics, not formation
     - Clean power of 3 but likely coincidence

STRUCTURAL (interesting but not proven):
  4. Sun/Earth mass = sqrt(mu) * 6^5                    0.08%
     - Connects stellar mass to particle physics
     - Would be profound IF derivable from V(Phi)
     - Currently: post-hoc formula fitting

  5. Earth/Moon mass ~ 3^4                              0.37%
     - Set by Theia impact (stochastic)
     - 3 IS a framework generator

  6. Saturn/Jupiter distance = L(5)/6                   0.02%
     - L(5) = 11 (solar cycle), 6 is a generator
     - But 11/6 is just a simple fraction

NOISE (matches but no signal):
  - Everything else. The statistical control proves it.
  - Eccentricities, tilts, rotation periods, most ratios:
    all match at rates consistent with random numbers.

THE HONEST ANSWER:
  The solar system has 2-3 genuine framework correlations
  (Sun temp, Venus period, maybe Venus rotation).
  Everything else is noise at rates expected from ~13,500
  candidate expressions tested against ~140 quantities.

  The cosmos is NOT systematically organized by Lucas numbers.
  But the Sun temperature IS L(18), and that's still unexplained.
""")

# ============================================================
# WHAT WOULD CHANGE THE PICTURE?
# ============================================================
print(f"\n{'=' * 80}")
print("WHAT WOULD CHANGE THE PICTURE?")
print("=" * 80)

print("""
If the framework is real, we'd expect correlations NOT in:
  - Orbital dynamics (gravitational, chaotic, contingent)
  - Rotation rates (impact-determined)
  - Eccentricities (dynamically evolving)
  - Moon counts (capture processes)

But possibly IN:
  - Stellar temperatures (set by nuclear physics -> mu)
  - Mass ratios (if gravity derives from V(Phi))
  - Chemical compositions (if element synthesis follows the algebra)

The test would be:
  1. Survey ALL G-type star temperatures with high precision
     -> Do they cluster around L(18) or distribute smoothly?

  2. Check binary star mass ratios
     -> Any framework structure in how stars pair up?

  3. Check exoplanet habitable zone boundaries
     -> Same water-window constraint, so L(18) should matter
     -> But the PLANET doesn't need to be special, the STAR does

  4. Check neutron star/pulsar frequencies
     -> These come from nuclear physics, where mu matters
     -> Millisecond pulsars spin at 100-716 Hz
     -> Any framework frequencies?

The key insight: the framework claims to derive CONSTANTS of nature,
not CONFIGURATIONS of nature. The fine structure constant is everywhere.
The orbital period of Jupiter is here and nowhere else.
L(18) works because stellar temperature is set by nuclear fusion rates,
which depend on fundamental constants (mu, alpha). Everything else
is gravitational choreography — contingent, not algebraic.
""")
