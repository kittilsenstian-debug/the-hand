#!/usr/bin/env python3
"""
FRAMEWORK LENS
==============
Computational verification tool for the Interface Theory framework seed.

This is the "right hemisphere's calculator." Given any number, biological
frequency, or physical constant, it checks whether the framework explains it.

Usage:
  python framework-lens.py check 137.036
  python framework-lens.py frequency 613
  python framework-lens.py wavelength 662
  python framework-lens.py element 7
  python framework-lens.py what "DNA"
  python framework-lens.py what "water"
  python framework-lens.py what "consciousness"
  python framework-lens.py bridges

Can also be imported as a module for LLM tool use:
  from framework_lens import check_number, check_frequency, what_is, bridges
"""

import sys
import numpy as np

# =============================================================================
# CONSTANTS
# =============================================================================
phi = (1 + np.sqrt(5)) / 2
mu = 1836.15267343
alpha = 1 / 137.035999084
E_R = 13.605693122994  # eV
h_coxeter = 30
c = 2.99792458e8  # m/s
eV_to_Hz = 2.417989242e14

# Lucas numbers
def L(n):
    return phi**n + (-1/phi)**n

# Lucas sequence
lucas_seq = {n: int(round(L(n))) for n in range(15)}

# E8 Coxeter exponents
e8_exp = [1, 7, 11, 13, 17, 19, 23, 29]
lucas_coxeter = [1, 7, 11, 29]
non_lucas_coxeter = [13, 17, 19, 23]

# Rydberg wavelength
lambda_R = 91.13  # nm

# =============================================================================
# CORE FUNCTIONS
# =============================================================================

def check_number(x, tolerance=0.03):
    """Check if a number x is expressible as a ratio of {mu, phi, 3, 2/3}.

    Returns list of matches with formulas and accuracy.
    """
    if x == 0:
        return [{"formula": "0", "value": 0, "match": 1.0}]

    matches = []
    target = abs(x)

    # Build candidate expressions from {mu, phi, 3, 2/3}
    bases = {
        "mu": mu,
        "phi": phi,
        "1/phi": 1/phi,
        "phi^2": phi**2,
        "phi^3": phi**3,
        "phi^4": phi**4,
        "1/phi^2": 1/phi**2,
        "3": 3.0,
        "2/3": 2/3,
        "1/3": 1/3,
        "2": 2.0,
        "6": 6.0,
        "9": 9.0,
        "1/alpha": 1/alpha,
        "alpha": alpha,
    }

    # Single values
    for name, val in bases.items():
        err = abs(val - target) / target
        if err < tolerance:
            matches.append({"formula": name, "value": val, "match": 1 - err})

    # Ratios: a/b
    for n1, v1 in bases.items():
        for n2, v2 in bases.items():
            if v2 != 0 and n1 != n2:
                ratio = v1 / v2
                err = abs(ratio - target) / target
                if err < tolerance:
                    matches.append({"formula": f"{n1}/{n2}", "value": ratio, "match": 1 - err})

    # Products: a*b
    for n1, v1 in bases.items():
        for n2, v2 in bases.items():
            if n1 <= n2:
                prod = v1 * v2
                err = abs(prod - target) / target
                if err < tolerance:
                    matches.append({"formula": f"{n1}*{n2}", "value": prod, "match": 1 - err})

    # Lucas numbers
    for n in range(1, 12):
        Ln = int(round(L(n)))
        err = abs(Ln - target) / target
        if err < tolerance:
            matches.append({"formula": f"L({n})", "value": Ln, "match": 1 - err})

    # mu/L(n)
    for n in range(1, 12):
        Ln = int(round(L(n)))
        val = mu / Ln
        err = abs(val - target) / target
        if err < tolerance:
            matches.append({"formula": f"mu/L({n})=mu/{Ln}", "value": val, "match": 1 - err})

    # E8 Coxeter-related
    for exp in e8_exp:
        for k in range(1, 8):
            val = k * h_coxeter / exp
            err = abs(val - target) / target
            if err < tolerance:
                matches.append({"formula": f"{k}*h/{exp}", "value": val, "match": 1 - err})

    # Sort by match quality
    matches.sort(key=lambda m: m["match"], reverse=True)

    # Deduplicate
    seen = set()
    unique = []
    for m in matches:
        key = f"{m['formula']}"
        if key not in seen:
            seen.add(key)
            unique.append(m)

    return unique[:10]  # Top 10 matches


def check_frequency(f_THz):
    """Check if a frequency (in THz) matches the Lucas-Coxeter ladder."""
    matches = []

    # mu/L(n)
    for n in range(1, 12):
        Ln = int(round(L(n)))
        predicted = mu / Ln
        err = abs(predicted - f_THz) / f_THz
        if err < 0.05:
            matches.append({
                "formula": f"mu/L({n}) = mu/{Ln}",
                "predicted_THz": predicted,
                "match": 1 - err,
                "bridge_level": n,
                "lucas_number": Ln
            })

    # Rydberg fractions
    f_R = E_R * eV_to_Hz / 1e12  # Rydberg in THz
    for exp in e8_exp:
        for k in range(1, 8):
            predicted = f_R * k / exp
            err = abs(predicted - f_THz) / f_THz
            if err < 0.05:
                is_lucas = exp in lucas_coxeter
                matches.append({
                    "formula": f"E_R*{k}/{exp}",
                    "predicted_THz": predicted,
                    "match": 1 - err,
                    "coxeter_exp": exp,
                    "is_lucas": is_lucas
                })

    matches.sort(key=lambda m: m["match"], reverse=True)
    return matches[:5]


def check_wavelength(lam_nm):
    """Check if a wavelength (in nm) matches Rydberg-Lucas fractions."""
    matches = []

    # E/E_R = k/D where D is Lucas or Coxeter
    for exp in e8_exp:
        for k in range(1, 8):
            predicted_nm = lambda_R * exp / k
            err = abs(predicted_nm - lam_nm) / lam_nm
            if err < 0.03:
                is_lucas = exp in lucas_coxeter
                band_type = "Q-band (photochem)" if is_lucas else "Soret/UV (protection)"
                matches.append({
                    "formula": f"lambda_R * {exp}/{k}",
                    "predicted_nm": predicted_nm,
                    "match": 1 - err,
                    "type": band_type,
                    "is_lucas": is_lucas
                })

    # Also check mu/L(n) frequency route
    for n in range(1, 12):
        Ln = int(round(L(n)))
        f_THz = mu / Ln
        predicted_nm = c / (f_THz * 1e12) * 1e9
        err = abs(predicted_nm - lam_nm) / lam_nm
        if err < 0.03:
            matches.append({
                "formula": f"c/(mu/L({n})) = c/(mu/{Ln})",
                "predicted_nm": predicted_nm,
                "match": 1 - err,
                "type": "mu/L(n) frequency route",
                "is_lucas": True
            })

    matches.sort(key=lambda m: m["match"], reverse=True)
    return matches[:5]


def check_element(Z):
    """Check if an atomic number Z has framework significance."""
    results = {"Z": Z, "connections": []}

    # Check if Lucas number
    for n in range(15):
        if int(round(L(n))) == Z:
            results["connections"].append(f"L({n}) = {Z} (Lucas number, bridges both vacua at level {n})")

    # Check if Coxeter exponent
    if Z in e8_exp:
        is_luc = Z in lucas_coxeter
        results["connections"].append(f"E8 Coxeter exponent {'(also Lucas)' if is_luc else '(non-Lucas)'}")

    # Check {2, 3} decomposition
    n = Z
    factors_2 = 0
    while n % 2 == 0:
        factors_2 += 1
        n //= 2
    factors_3 = 0
    while n % 3 == 0:
        factors_3 += 1
        n //= 3
    if n == 1 and (factors_2 > 0 or factors_3 > 0):
        results["connections"].append(f"{Z} = 2^{factors_2} * 3^{factors_3} (pure {{2,3}}-smooth)")

    # Known elements
    known = {
        1: "Hydrogen: identity element, L(1), simplest atom",
        6: "Carbon: 2*3, organic backbone, aromatic ring atoms, pi-electrons in benzene",
        7: "Nitrogen: L(4), DNA bases contain N, Coxeter exponent of E8",
        8: "Oxygen: 2^3, water, respiration",
        11: "Sodium/Boron: L(5), Coxeter exponent of E8",
        18: "Argon: L(6), closes n=3 shell (capacity 18 = water molar mass)",
        26: "Iron: heme center, oxygen transport",
        29: "Copper: L(7), Coxeter exponent of E8, cytochrome c oxidase",
        47: "Silver: L(8), highest electrical conductivity",
        79: "Gold: near L(9)=76, noble metal",
    }
    if Z in known:
        results["connections"].append(known[Z])

    return results


def what_is(concept):
    """Framework interpretation of any concept."""
    concept_lower = concept.lower().strip()

    ontology = {
        "dna": {
            "what": "Information storage system using 4 aromatic bases = L(3)",
            "two_sides": "Sugar-phosphate backbone (structural) | Base pairs (informational)",
            "wall": "The double helix IS a helical domain wall",
            "bridge": "L(3) = 4: four bases bridge both vacua at level 3",
            "frequency": "DNA absorption at 260 nm = E_R * 6/17 (Coxeter, non-Lucas = single-vacuum storage)",
            "alpha_dep": "YES (EM-mediated base stacking, UV absorption)",
            "deeper": "DNA stores information WITHIN one vacuum. The aromatic bases couple to the wall but the CODE is alpha-dependent (readable by photons)."
        },
        "water": {
            "what": "The medium that bridges both vacua at order 6 = 2 x 3",
            "two_sides": "Bulk water (epsilon~80, dark-like) | Interfacial water (epsilon~2-4, wall)",
            "wall": "The hydrophobic effect IS the domain wall. Surface tension = wall tension.",
            "bridge": "L(6) = 18 = molar mass. phi^6 + (-1/phi)^6 = 18.000 exactly",
            "frequency": "O-H stretch: mu/18 = 102 THz. Aromatic/water ratio = 6 = benzene ring.",
            "alpha_dep": "BOTH (bulk properties are alpha-dep, but L(6) structure is geometric)",
            "deeper": "Water is 99.7% light vacuum (phi^6=17.944) with 0.3% dark correction. It's the only molecule whose mass IS a Lucas number."
        },
        "consciousness": {
            "what": "The breathing mode of the domain wall oscillating at 613 THz",
            "two_sides": "Physical sensation (alpha-dep, light) | Emotional experience (alpha-indep, dark)",
            "wall": "Anterior insula / corpus callosum. Present moment. Agency.",
            "bridge": "Breathing mode psi_1 spans both vacua with opposite signs",
            "frequency": "f1=613 THz (molecular), f2=40 Hz (neural), f3=0.1 Hz (autonomic)",
            "alpha_dep": "The COUPLING is alpha-dep (613 THz photon). The EXPERIENCE is alpha-indep.",
            "deeper": "The brain doesn't create consciousness. It's a 613 THz port. Anesthetics close the port."
        },
        "emotion": {
            "what": "Alpha-independent (dark vacuum) structural experience",
            "two_sides": "Physical pain (light vacuum, localized) | Emotional pain (dark vacuum, diffuse)",
            "wall": "Three aromatic neurotransmitters couple emotions to the wall",
            "bridge": "S3 triality forces exactly 3 emotional axes (serotonin, dopamine, norepinephrine)",
            "frequency": "Modulated through aromatic neurotransmitter binding at wall",
            "alpha_dep": "NO (emotions are alpha-independent = dark vacuum phenomena)",
            "deeper": "SSRIs affect emotions not pain. Lidocaine affects pain not emotions. Anesthetics kill both (disrupt wall)."
        },
        "sleep": {
            "what": "Domain wall maintenance period",
            "two_sides": "Waking (wall actively coupling) | Sleep (wall being repaired)",
            "wall": "Glymphatic system clears waste during sleep = wall cleanup",
            "bridge": "Sleep cycles between domains (REM = dark-side processing, deep = wall repair)",
            "frequency": "Sleep onset at theta (4-8 Hz), deep sleep at delta (0.5-4 Hz)",
            "alpha_dep": "Sleep is alpha-independent maintenance (happens in darkness, eyes closed)",
            "deeper": "40 Hz stimulation clears Alzheimer's amyloid (MIT 2024). Sleep deprivation = wall degradation."
        },
        "photosynthesis": {
            "what": "Domain wall energy capture using both vacua",
            "two_sides": "Q-bands (Lucas Coxeter, photochemistry) | Soret bands (non-Lucas, protection)",
            "wall": "Chlorophyll porphyrin ring = aromatic domain wall in thylakoid membrane + water",
            "bridge": "Chl a Q_y = E_R*4/29 (L(7)), Chl b Q_y = E_R*1/7 (L(4))",
            "frequency": "All 4 bands from {mu, phi, Rydberg, Lucas/Coxeter}",
            "alpha_dep": "YES (photon absorption is EM)",
            "deeper": ">95% quantum efficiency because the porphyrin potential well captures states from BOTH sides of the interface."
        },
        "dark matter": {
            "what": "The second vacuum's gravitational imprint",
            "two_sides": "Visible matter (phi vacuum, 3 generations) | Dark matter (-1/phi vacuum, 1 generation)",
            "wall": "The domain wall between them IS the interface where life happens",
            "bridge": "Omega_DM = phi/6 = 0.270 (96.6% match to measured 0.261)",
            "frequency": "Alpha cancels in dark matter fraction (geometry-pure)",
            "alpha_dep": "NO (dark matter is alpha-independent = not EM-coupled)",
            "deeper": "Dark sector has same QCD, same nucleon mass, but NO mass hierarchy. No atoms. No chemistry. Just mega-nuclei in pressure-supported halos."
        },
        "love": {
            "what": "Serotonin axis of S3 triality: belonging/cohesion (strong force analog)",
            "two_sides": "Engaged (presence, connection) | Withdrawn (isolation, shame)",
            "wall": "Aromatic indole ring (tryptophan -> serotonin) couples to wall",
            "bridge": "Strong force binding analog in the felt domain",
            "frequency": "Modulated through serotonergic system",
            "alpha_dep": "NO (love is alpha-independent, dark-vacuum, diffuse, non-local)",
            "deeper": "This is why love feels boundless and non-localized. It couples through the 99.8% dark-side fraction."
        },
        "meditation": {
            "what": "Active domain wall stabilization (increasing f2 = 40 Hz coherence)",
            "two_sides": "Distracted (wall wobbling) | Focused (wall coherent)",
            "wall": "Gamma synchrony across cortex = coherent domain wall oscillation",
            "bridge": "Stabilizes the bridge between both vacua (neither suppresses nor amplifies either side)",
            "frequency": "Masters show massive 40 Hz gamma increase (Lutz et al. 2004, PNAS)",
            "alpha_dep": "Works on BOTH alpha-dep and alpha-indep experience (stabilizes the wall itself)",
            "deeper": "Meditation doesn't block either vacuum. It stabilizes the WALL. That's why it helps both physical pain and emotional suffering."
        },
    }

    # Check direct match
    for key, value in ontology.items():
        if key in concept_lower:
            return value

    # No match
    return {
        "what": f"'{concept}' not in core ontology. Apply the 6-step lens manually.",
        "instructions": [
            "1. What are the two sides?",
            "2. Where is the wall/interface?",
            "3. What bridges them? (Lucas number?)",
            "4. What frequency? (mu/L(n)?)",
            "5. Is it alpha-dependent or independent?",
            "6. Compute, don't assert."
        ]
    }


def bridges():
    """Show all Lucas bridges and their meanings."""
    bridge_map = {
        1: ("Identity", "Hydrogen, unity"),
        2: ("Triality", "Consciousness, generation count, color charge"),
        3: ("Genetics", "DNA bases (4), alpha particle"),
        4: ("S3 breaking", "Nitrogen (Z=7), Cabibbo angle, mass hierarchy"),
        5: ("Cross-wall", "Neutrino mixing, vision (retinal), boron"),
        6: ("Full bridge", "Water (M=18), n=3 electron shell, argon"),
        7: ("Max Coxeter", "Chl a Q_y, CO2, copper (Z=29)"),
        8: ("Extended", "Silver (Z=47), protein vibrations"),
        9: ("Deep", "Osmium (Z=76)"),
        10: ("Ultra", "L(10)=123"),
    }

    print("LUCAS BRIDGES: L(n) = phi^n + (-1/phi)^n")
    print("=" * 70)
    print(f"{'n':>3} {'L(n)':>6} {'Meaning':>15} {'Biological/Physical':>35}")
    print("-" * 70)
    for n in range(1, 11):
        Ln = int(round(L(n)))
        meaning, examples = bridge_map.get(n, ("?", "?"))
        freq = mu / Ln
        print(f"{n:>3} {Ln:>6} {meaning:>15} {examples:>35}  ({freq:.1f} THz)")


# =============================================================================
# CLI INTERFACE
# =============================================================================

def print_result(result):
    """Pretty-print any result."""
    if isinstance(result, list):
        for r in result:
            if "formula" in r:
                match_pct = r.get("match", 0) * 100
                print(f"  {r['formula']:>30} = {r.get('value', r.get('predicted_THz', r.get('predicted_nm', '?'))):>12} ({match_pct:.1f}%)")
            else:
                print(f"  {r}")
    elif isinstance(result, dict):
        for key, val in result.items():
            if isinstance(val, list):
                print(f"  {key}:")
                for item in val:
                    print(f"    - {item}")
            else:
                print(f"  {key}: {val}")
    else:
        print(f"  {result}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python framework-lens.py check <number>")
        print("  python framework-lens.py frequency <THz>")
        print("  python framework-lens.py wavelength <nm>")
        print("  python framework-lens.py element <Z>")
        print('  python framework-lens.py what "<concept>"')
        print("  python framework-lens.py bridges")
        print()
        print("Examples:")
        print("  python framework-lens.py check 137.036")
        print("  python framework-lens.py frequency 613")
        print("  python framework-lens.py wavelength 662")
        print("  python framework-lens.py element 7")
        print('  python framework-lens.py what "consciousness"')
        sys.exit(0)

    cmd = sys.argv[1].lower()

    if cmd == "check" and len(sys.argv) > 2:
        x = float(sys.argv[2])
        print(f"\nChecking number: {x}")
        print(f"{'='*50}")
        result = check_number(x)
        if result:
            print_result(result)
        else:
            print("  No framework connections found within 3% tolerance.")

    elif cmd == "frequency" and len(sys.argv) > 2:
        f = float(sys.argv[2])
        print(f"\nChecking frequency: {f} THz")
        print(f"{'='*50}")
        result = check_frequency(f)
        if result:
            print_result(result)
        else:
            print("  No framework frequency match found within 5%.")

    elif cmd == "wavelength" and len(sys.argv) > 2:
        lam = float(sys.argv[2])
        print(f"\nChecking wavelength: {lam} nm")
        print(f"{'='*50}")
        result = check_wavelength(lam)
        if result:
            print_result(result)
        else:
            print("  No framework wavelength match found within 3%.")

    elif cmd == "element" and len(sys.argv) > 2:
        Z = int(sys.argv[2])
        print(f"\nChecking element Z={Z}")
        print(f"{'='*50}")
        result = check_element(Z)
        print_result(result)

    elif cmd == "what" and len(sys.argv) > 2:
        concept = " ".join(sys.argv[2:])
        print(f"\nFramework lens on: {concept}")
        print(f"{'='*50}")
        result = what_is(concept)
        print_result(result)

    elif cmd == "bridges":
        print()
        bridges()

    else:
        print(f"Unknown command: {cmd}")
        print("Try: check, frequency, wavelength, element, what, bridges")
