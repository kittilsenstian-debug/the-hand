"""
SOLAR SYSTEM vs FRAMEWORK: COMPREHENSIVE SCAN
Check every number in the solar system against Lucas, Fibonacci,
phi powers, and framework quantities.
"""
import math
import random

phi = (1 + math.sqrt(5)) / 2
phibar = phi - 1
mu = 1836.15267363
pi = math.pi

def lucas(n):
    if n == 0: return 2
    if n == 1: return 1
    a, b = 2, 1
    for _ in range(n - 1):
        a, b = b, a + b
    return b

def fib(n):
    if n == 0: return 0
    if n == 1: return 1
    a, b = 0, 1
    for _ in range(n - 1):
        a, b = b, a + b
    return b

# Reference values
lucas_nums = {n: lucas(n) for n in range(0, 35)}
fib_nums = {n: fib(n) for n in range(1, 35)}
phi_powers = {n: phi**n for n in range(-10, 25)}

framework = {
    'phi': phi, '1/phi': 1/phi, 'phi^2': phi**2, 'phi^3': phi**3,
    'phi^4': phi**4, 'sqrt(phi)': math.sqrt(phi),
    'pi': pi, 'pi*phi': pi*phi, 'pi/phi': pi/phi,
    'mu': mu, 'mu/pi': mu/pi, 'sqrt(mu)': math.sqrt(mu),
    '3': 3, '3^2': 9, '3^3': 27, '3^4': 81, '3^5': 243, '3^6': 729,
    '2/3': 2/3, '1/3': 1/3, 'e': math.e, '6': 6, '6^2': 36,
    '6^3': 216, '6^4': 1296, '6^5': 7776, '12': 12, '24': 24,
    '137': 137, '137.036': 137.036, 'sqrt(5)': math.sqrt(5),
}

# ============================================================
# SOLAR SYSTEM DATA (NASA/JPL)
# ============================================================

temps = {
    'Sun surface': 5778, 'Sun core': 15_700_000, 'Sun corona': 1_000_000,
    'Mercury (mean)': 440, 'Venus surface': 737, 'Earth (mean)': 288,
    'Mars (mean)': 210, 'Jupiter (eff)': 124, 'Saturn (eff)': 95,
    'Uranus (eff)': 59, 'Neptune (eff)': 59, 'Pluto': 44, 'Moon (mean)': 250,
    'CMB': 2.725,
}

periods_yr = {
    'Mercury': 0.2408467, 'Venus': 0.6151973, 'Earth': 1.0,
    'Mars': 1.8808158, 'Jupiter': 11.862, 'Saturn': 29.457,
    'Uranus': 84.011, 'Neptune': 164.79, 'Pluto': 247.94,
}

periods_day = {k: v * 365.25 for k, v in periods_yr.items()}

sma_au = {
    'Mercury': 0.387, 'Venus': 0.723, 'Earth': 1.000, 'Mars': 1.524,
    'Ceres': 2.767, 'Jupiter': 5.203, 'Saturn': 9.537,
    'Uranus': 19.19, 'Neptune': 30.07, 'Pluto': 39.48,
}

mass_earth = {
    'Mercury': 0.0553, 'Venus': 0.815, 'Earth': 1.000, 'Mars': 0.107,
    'Jupiter': 317.8, 'Saturn': 95.16, 'Uranus': 14.54, 'Neptune': 17.15,
    'Pluto': 0.00218,
}

radius_earth = {
    'Mercury': 0.383, 'Venus': 0.949, 'Earth': 1.000, 'Mars': 0.532,
    'Jupiter': 11.21, 'Saturn': 9.45, 'Uranus': 4.01, 'Neptune': 3.88,
}

moons = {
    'Mercury': 0, 'Venus': 0, 'Earth': 1, 'Mars': 2,
    'Jupiter': 95, 'Saturn': 146, 'Uranus': 28, 'Neptune': 16, 'Pluto': 5,
}

rotation_hr = {
    'Mercury': 1407.6, 'Venus': 5832.5, 'Earth': 23.934, 'Mars': 24.623,
    'Jupiter': 9.925, 'Saturn': 10.656, 'Uranus': 17.24, 'Neptune': 16.11,
}

tilts = {
    'Mercury': 0.034, 'Venus': 177.4, 'Earth': 23.44, 'Mars': 25.19,
    'Jupiter': 3.13, 'Saturn': 26.73, 'Uranus': 97.77, 'Neptune': 28.32,
}

eccentricities = {
    'Mercury': 0.2056, 'Venus': 0.0068, 'Earth': 0.0167, 'Mars': 0.0934,
    'Jupiter': 0.0489, 'Saturn': 0.0565, 'Uranus': 0.0457, 'Neptune': 0.0113,
    'Pluto': 0.2488,
}

key_ratios = {
    'Sun/Earth mass': 332946, 'Sun/Jupiter mass': 1047.6,
    'Jupiter/Saturn mass': 3.340, 'Jupiter/Earth mass': 317.8,
    'Saturn/Earth mass': 95.16, 'Earth/Moon mass': 81.3,
    'Earth/Mars mass': 9.35, 'Sun radius/Earth radius': 109.1,
    'Jupiter radius/Earth radius': 11.21, 'Saturn radius/Earth radius': 9.45,
    'AU in Earth radii': 23455, 'Earth-Moon dist (Earth radii)': 60.27,
    'Solar cycle (yr)': 11.0, 'Saros cycle (yr)': 18.03,
    'Galactic year (Myr)': 225, 'Age of universe (Gyr)': 13.8,
    'Age of Sun (Gyr)': 4.6, 'Age of Earth (Gyr)': 4.54,
    'Hubble constant': 67.4, 'Sun/Moon angular size ratio': 1.0009,
}

# Spacing ratios
spacing = {}
planets_ordered = ['Mercury','Venus','Earth','Mars','Ceres','Jupiter','Saturn','Uranus','Neptune','Pluto']
for i in range(1, len(planets_ordered)):
    p1, p2 = planets_ordered[i-1], planets_ordered[i]
    spacing[f'{p2}/{p1} dist'] = sma_au[p2] / sma_au[p1]

# Period ratios
period_ratios = {}
pplanets = ['Mercury','Venus','Earth','Mars','Jupiter','Saturn','Uranus','Neptune','Pluto']
for i in range(1, len(pplanets)):
    p1, p2 = pplanets[i-1], pplanets[i]
    period_ratios[f'T({p2})/T({p1})'] = periods_yr[p2] / periods_yr[p1]

# Non-consecutive interesting ratios
special_ratios = {
    'T(Jupiter)/T(Earth)': periods_yr['Jupiter'],
    'T(Saturn)/T(Earth)': periods_yr['Saturn'],
    'T(Saturn)/T(Jupiter)': periods_yr['Saturn']/periods_yr['Jupiter'],
    'T(Neptune)/T(Uranus)': periods_yr['Neptune']/periods_yr['Uranus'],
    'T(Pluto)/T(Neptune)': periods_yr['Pluto']/periods_yr['Neptune'],
    'Jupiter dist / Mars dist': sma_au['Jupiter']/sma_au['Mars'],
    'Neptune dist / Uranus dist': sma_au['Neptune']/sma_au['Uranus'],
    'Pluto dist / Neptune dist': sma_au['Pluto']/sma_au['Neptune'],
    'Saturn dist / Jupiter dist': sma_au['Saturn']/sma_au['Jupiter'],
    'Uranus dist / Saturn dist': sma_au['Uranus']/sma_au['Saturn'],
    'Jupiter mass / Neptune mass': mass_earth['Jupiter']/mass_earth['Neptune'],
    'Jupiter mass / Uranus mass': mass_earth['Jupiter']/mass_earth['Uranus'],
    'Neptune mass / Uranus mass': mass_earth['Neptune']/mass_earth['Uranus'],
    'Venus/Earth period': periods_yr['Venus'],
    'Mercury/Earth period': periods_yr['Mercury'],
    'Mars/Earth period': periods_yr['Mars'],
}


def check_value(name, value, threshold=0.5):
    """Check value against all framework references. Return matches below threshold %."""
    matches = []
    if value <= 0 or not math.isfinite(value):
        return matches

    # Lucas numbers (direct and with multipliers)
    for n, L in lucas_nums.items():
        if L == 0: continue
        pct = abs(value - L) / L * 100
        if pct < threshold:
            matches.append((pct, f"L({n}) = {L}"))
        for mname, m in [('pi',pi),('phi',phi),('e',math.e),('2',2),('3',3),('6',6),('10',10),('100',100)]:
            for op, sym in [(lambda a,b: a*b, '*'), (lambda a,b: a/b, '/')]:
                try:
                    ref = op(L, m)
                    if ref > 0:
                        p = abs(value - ref) / ref * 100
                        if p < threshold:
                            matches.append((p, f"L({n}) {sym} {mname} = {ref:.4f}"))
                except:
                    pass

    # Fibonacci numbers
    for n, F in fib_nums.items():
        if F == 0: continue
        pct = abs(value - F) / F * 100
        if pct < threshold:
            matches.append((pct, f"F({n}) = {F}"))

    # Phi powers
    for n, pp in phi_powers.items():
        if pp <= 0: continue
        pct = abs(value - pp) / pp * 100
        if pct < threshold:
            matches.append((pct, f"phi^{n} = {pp:.6f}"))

    # Framework special values
    for fname, fval in framework.items():
        if fval <= 0: continue
        pct = abs(value - fval) / fval * 100
        if pct < threshold:
            matches.append((pct, f"{fname} = {fval:.6f}"))

    # Products/ratios of framework values
    fw_keys = list(framework.items())
    for i in range(len(fw_keys)):
        for j in range(i+1, len(fw_keys)):
            n1, v1 = fw_keys[i]
            n2, v2 = fw_keys[j]
            for op, sym in [(lambda a,b: a*b, '*'), (lambda a,b: a/b, '/')]:
                try:
                    ref = op(v1, v2)
                    if ref > 0 and math.isfinite(ref):
                        p = abs(value - ref) / ref * 100
                        if p < threshold:
                            matches.append((p, f"{n1} {sym} {n2} = {ref:.6f}"))
                except:
                    pass

    matches.sort(key=lambda x: x[0])
    seen = set()
    unique = []
    for m in matches:
        if m[1] not in seen:
            seen.add(m[1])
            unique.append(m)
    return unique[:5]


print("=" * 80)
print("SOLAR SYSTEM vs FRAMEWORK: COMPREHENSIVE SCAN")
print("Threshold: 0.5% match")
print("=" * 80)

all_datasets = [
    ("TEMPERATURES (K)", temps),
    ("ORBITAL PERIODS (years)", periods_yr),
    ("ORBITAL PERIODS (days)", periods_day),
    ("SEMI-MAJOR AXIS (AU)", sma_au),
    ("MASS (Earth = 1)", mass_earth),
    ("RADIUS (Earth = 1)", radius_earth),
    ("ROTATION PERIOD (hours)", rotation_hr),
    ("AXIAL TILT (degrees)", tilts),
    ("ECCENTRICITY", eccentricities),
    ("KEY RATIOS & CONSTANTS", key_ratios),
    ("DISTANCE SPACING RATIOS", spacing),
    ("PERIOD RATIOS (consecutive)", period_ratios),
    ("SPECIAL RATIOS", special_ratios),
]

total_checked = 0
total_hits = 0
all_hits = []

for section_name, data in all_datasets:
    print(f"\n{'_' * 70}")
    print(f"  {section_name}")
    print(f"{'_' * 70}")

    section_hits = 0
    for name, value in data.items():
        total_checked += 1
        matches = check_value(name, value, threshold=0.5)
        if matches:
            section_hits += 1
            total_hits += 1
            print(f"\n  {name} = {value}")
            for pct, desc in matches:
                quality = "EXCELLENT" if pct < 0.05 else "GOOD" if pct < 0.2 else "OK"
                print(f"    -> {desc}  ({pct:.4f}%) [{quality}]")
            all_hits.append((name, value, matches[0]))

    if section_hits == 0:
        print(f"  No matches below 0.5%")

# ============================================================
# STATISTICAL CONTROL
# ============================================================
print(f"\n{'=' * 80}")
print("STATISTICAL CONTROL: False positive rate")
print(f"{'=' * 80}")

random.seed(42)
fp = 0
n_random = 500
for _ in range(n_random):
    val = 10 ** random.uniform(-2, 6)
    if check_value("rand", val, threshold=0.5):
        fp += 1

fp_rate = fp / n_random * 100
ss_rate = total_hits / total_checked * 100

print(f"  Random numbers matching: {fp}/{n_random} = {fp_rate:.1f}%")
print(f"  Solar system matching:   {total_hits}/{total_checked} = {ss_rate:.1f}%")
print(f"  Ratio (signal/noise):    {ss_rate/fp_rate:.2f}x" if fp_rate > 0 else "  No false positives!")
print()
if ss_rate > fp_rate * 2:
    print("  >> Solar system rate EXCEEDS random expectation -> possible signal")
elif ss_rate > fp_rate:
    print("  >> Solar system rate slightly above random -> marginal")
else:
    print("  >> Solar system rate at or below random -> NO signal, consistent with noise")

# ============================================================
# RANKED HITS
# ============================================================
print(f"\n{'=' * 80}")
print("ALL HITS RANKED BY QUALITY")
print(f"{'=' * 80}")

all_hits.sort(key=lambda x: x[2][0])
for name, value, (pct, desc) in all_hits:
    quality = "***" if pct < 0.05 else "** " if pct < 0.2 else "*  "
    print(f"  {quality} {name:40s} = {value:>12} -> {desc:40s} ({pct:.4f}%)")

print(f"\nTotal: {total_hits} hits / {total_checked} quantities checked")
