#!/usr/bin/env python3
"""
planetary_fields_habitability.py

Test the framework prediction:
  "Every solar system body with habitability potential has a magnetic boundary."

Compiles data for all major solar system bodies and computes correlation
between magnetic boundaries and habitability indicators.

Standard Python only — no external dependencies.
"""

# ============================================================
# DATA: Solar system bodies
# ============================================================
# Each entry:
#   name, type, intrinsic_field, induced_field, magnetic_boundary,
#   field_strength_nT, liquid_water, atmosphere, energy_source,
#   organics_detected, habitability_assessment, notes

bodies = [
    # ---- ROCKY PLANETS ----
    {
        "name": "Mercury",
        "type": "rocky planet",
        "intrinsic_field": "weak dipole",
        "induced_field": "no",
        "magnetic_boundary": "yes — magnetopause",
        "field_strength_nT": 300,          # ~300 nT surface equatorial
        "liquid_water": "none",
        "atmosphere": "none",              # exosphere only
        "energy_source": "solar",
        "organics_detected": False,        # water ice at poles, no organics confirmed
        "habitability": "dead",
        "notes": "Weak dipole (~1% Earth). Magnetopause at ~1.5 R_M. No atmosphere retention. Extreme temperature swings."
    },
    {
        "name": "Venus",
        "type": "rocky planet",
        "intrinsic_field": "none",
        "induced_field": "yes — solar wind interaction",
        "magnetic_boundary": "yes — induced magnetosphere (ionopause/magnetic barrier)",
        "field_strength_nT": 3,            # ~3 nT induced barrier; no intrinsic surface field
        "liquid_water": "none",            # possibly ancient; not now
        "atmosphere": "substantial",       # 92 bar CO2
        "energy_source": "solar",
        "organics_detected": False,        # phosphine claim controversial
        "habitability": "dead",            # surface T ~735 K
        "notes": "No intrinsic field. Induced magnetosphere from solar wind draping around ionosphere. "
                 "Cloud deck habitability hypothesis (Greaves 2020 phosphine, contested). "
                 "Surface is uninhabitable (735 K, 92 bar). Some consider upper atmosphere as candidate."
    },
    {
        "name": "Earth",
        "type": "rocky planet",
        "intrinsic_field": "strong dipole",
        "induced_field": "no",
        "magnetic_boundary": "yes — magnetopause",
        "field_strength_nT": 30000,        # ~25,000-65,000 nT surface
        "liquid_water": "confirmed",
        "atmosphere": "substantial",
        "energy_source": "solar, geothermal",
        "organics_detected": True,
        "habitability": "confirmed habitable",
        "notes": "The standard. Dipole moment 8e22 Am^2. Magnetopause at ~10 R_E."
    },
    {
        "name": "Mars",
        "type": "rocky planet",
        "intrinsic_field": "none (lost ~4 Gya)",
        "induced_field": "weak — solar wind interaction",
        "magnetic_boundary": "partial — crustal magnetic anomalies create mini-magnetospheres + induced boundary",
        "field_strength_nT": 5,            # ~5 nT induced; crustal fields up to ~1500 nT locally
        "liquid_water": "possible",        # subsurface brines, ancient surface water
        "atmosphere": "thin",              # 6 mbar CO2
        "energy_source": "solar",
        "organics_detected": True,         # Curiosity SAM instrument, chlorobenzene etc.
        "habitability": "candidate",
        "notes": "Lost global dipole ~4 Gya. Crustal remnant fields up to 1500 nT (Mars Global Surveyor). "
                 "Induced magnetospheric boundary from solar wind. Thin atmosphere being stripped. "
                 "Subsurface liquid water possible (MARSIS radar reflections, debated). "
                 "Curiosity confirmed organics (Eigenbrode 2018, Science). Past habitability well-established."
    },

    # ---- GAS/ICE GIANTS ----
    {
        "name": "Jupiter",
        "type": "gas giant",
        "intrinsic_field": "very strong dipole",
        "induced_field": "no",
        "magnetic_boundary": "yes — magnetopause",
        "field_strength_nT": 420000,       # ~420,000 nT equatorial surface (cloud top)
        "liquid_water": "possible",        # deep atmospheric water layer
        "atmosphere": "substantial",
        "energy_source": "solar, internal heat",
        "organics_detected": True,         # CH4, complex organics in atmosphere
        "habitability": "dead",            # no solid surface, extreme pressure
        "notes": "Strongest planetary magnetic field. Magnetosphere extends to ~100 R_J. "
                 "No solid surface. Atmospheric water layer possible but extreme conditions."
    },
    {
        "name": "Saturn",
        "type": "gas giant",
        "intrinsic_field": "strong dipole",
        "induced_field": "no",
        "magnetic_boundary": "yes — magnetopause",
        "field_strength_nT": 21000,        # ~21,000 nT equatorial
        "liquid_water": "possible",
        "atmosphere": "substantial",
        "energy_source": "solar, internal heat",
        "organics_detected": True,
        "habitability": "dead",
        "notes": "Remarkably axisymmetric dipole. Magnetopause at ~20 R_S."
    },
    {
        "name": "Uranus",
        "type": "ice giant",
        "intrinsic_field": "multipole (tilted, offset dipole)",
        "induced_field": "no",
        "magnetic_boundary": "yes — magnetopause",
        "field_strength_nT": 23000,        # ~23,000 nT surface
        "liquid_water": "possible",        # ionic water ocean deep interior
        "atmosphere": "substantial",
        "energy_source": "solar (minimal internal heat)",
        "organics_detected": True,         # CH4
        "habitability": "dead",
        "notes": "Highly tilted (59 deg) and offset dipole. Chaotic magnetosphere. "
                 "Superionic water ice interior."
    },
    {
        "name": "Neptune",
        "type": "ice giant",
        "intrinsic_field": "multipole (tilted, offset dipole)",
        "induced_field": "no",
        "magnetic_boundary": "yes — magnetopause",
        "field_strength_nT": 14000,        # ~14,000 nT surface
        "liquid_water": "possible",        # ionic water ocean deep interior
        "atmosphere": "substantial",
        "energy_source": "solar, internal heat",
        "organics_detected": True,         # CH4
        "habitability": "dead",
        "notes": "Similar to Uranus: tilted, offset multipole. Strong internal heat source."
    },

    # ---- JOVIAN MOONS ----
    {
        "name": "Io",
        "type": "moon (Jupiter)",
        "intrinsic_field": "none",
        "induced_field": "yes — strong interaction with Jupiter's magnetosphere",
        "magnetic_boundary": "yes — Io's Alfven wings / partial induced boundary",
        "field_strength_nT": 1800,         # ~1800 nT induced perturbation near Io
        "liquid_water": "none",
        "atmosphere": "thin",              # SO2, volcanic, patchy
        "energy_source": "tidal (extreme)",
        "organics_detected": False,
        "habitability": "dead",
        "notes": "Most volcanically active body. Embedded deep in Jupiter's magnetosphere. "
                 "Alfven wings create standing current system, not classical magnetopause. "
                 "SO2 atmosphere. Too hot and volcanic for habitability."
    },
    {
        "name": "Europa",
        "type": "moon (Jupiter)",
        "intrinsic_field": "none",
        "induced_field": "yes — strong induced dipole from Jupiter's field",
        "magnetic_boundary": "yes — induced magnetosphere",
        "field_strength_nT": 220,          # ~220 nT induced field (Galileo measurements)
        "liquid_water": "confirmed",       # subsurface ocean, 100+ km deep
        "atmosphere": "thin",              # tenuous O2 exosphere
        "energy_source": "tidal",
        "organics_detected": False,        # NaCl, not organics (yet; Juno/Europa Clipper pending)
        "habitability": "candidate",
        "notes": "Subsurface ocean confirmed (Galileo magnetometer, Hubble plumes). "
                 "Induced magnetic field from conducting ocean in Jupiter's rotating field. "
                 "Europa Clipper (arrived 2030s) will characterize habitability. "
                 "Tidal heating maintains liquid water. Strong habitability candidate."
    },
    {
        "name": "Ganymede",
        "type": "moon (Jupiter)",
        "intrinsic_field": "yes — intrinsic dipole (unique among moons)",
        "induced_field": "also yes — induced component from Jupiter",
        "magnetic_boundary": "yes — mini-magnetosphere within Jupiter's magnetosphere",
        "field_strength_nT": 719,          # ~719 nT intrinsic equatorial surface
        "liquid_water": "confirmed",       # subsurface ocean between ice layers (Hubble aurora study 2015)
        "atmosphere": "thin",              # tenuous O2 exosphere
        "energy_source": "tidal (weak), geothermal",
        "organics_detected": False,
        "habitability": "candidate",
        "notes": "ONLY moon with intrinsic magnetic field. Mini-magnetosphere with open/closed field lines. "
                 "Subsurface ocean confirmed by Hubble aurora oscillation study (Saur 2015, JGR). "
                 "Ocean sandwiched between ice layers — may limit rock-water interaction. "
                 "JUICE mission (ESA, arriving 2031) will characterize."
    },
    {
        "name": "Callisto",
        "type": "moon (Jupiter)",
        "intrinsic_field": "none",
        "induced_field": "yes — weak induced field from Jupiter",
        "magnetic_boundary": "yes — weak induced magnetospheric boundary",
        "field_strength_nT": 35,           # ~35 nT induced (Galileo)
        "liquid_water": "possible",        # possible deep subsurface ocean
        "atmosphere": "thin",              # tenuous CO2 exosphere
        "energy_source": "minimal",        # weak tidal, some radiogenic
        "organics_detected": False,
        "habitability": "candidate",       # weakest of Galilean candidates
        "notes": "Induced field suggests subsurface conducting layer (ocean?). "
                 "Most heavily cratered body — geologically dead surface. "
                 "Weak candidate: less tidal heating, uncertain ocean existence."
    },

    # ---- SATURNIAN MOONS ----
    {
        "name": "Titan",
        "type": "moon (Saturn)",
        "intrinsic_field": "none",
        "induced_field": "yes — interaction with Saturn's magnetosphere",
        "magnetic_boundary": "yes — induced magnetospheric boundary (Titan's ionopause)",
        "field_strength_nT": 5,            # ~5 nT induced draping field
        "liquid_water": "possible",        # subsurface water-ammonia ocean
        "atmosphere": "substantial",       # 1.5 bar N2/CH4 — thicker than Earth's
        "energy_source": "solar (weak), tidal, geothermal",
        "organics_detected": True,         # rich organic chemistry, tholins, HCN, surface lakes of CH4/C2H6
        "habitability": "candidate",
        "notes": "Only moon with substantial atmosphere (1.5 bar). Surface liquid methane/ethane lakes. "
                 "Subsurface water-ammonia ocean likely (Cassini gravity + Schumann resonance). "
                 "Within Saturn's magnetosphere; Saturn's field drapes around Titan creating magnetic boundary. "
                 "Rich prebiotic chemistry. Dragonfly mission (2030s)."
    },
    {
        "name": "Enceladus",
        "type": "moon (Saturn)",
        "intrinsic_field": "none",
        "induced_field": "yes — interaction with Saturn's magnetosphere",
        "magnetic_boundary": "yes — Enceladus creates perturbation/partial boundary in Saturn's field",
        "field_strength_nT": 25,           # Saturn's field at Enceladus ~325 nT, perturbation ~25 nT
        "liquid_water": "confirmed",       # subsurface global ocean, active geysers
        "atmosphere": "thin",              # water vapor plume, localized
        "energy_source": "tidal",
        "organics_detected": True,         # complex organics in plumes (Postberg 2018, Nature)
        "habitability": "candidate",
        "notes": "Global subsurface ocean confirmed (Cassini libration). Active south pole geysers. "
                 "Complex organics + molecular hydrogen in plumes = possible hydrothermal vents. "
                 "Embedded in Saturn's magnetosphere. Plume interaction creates local field perturbation. "
                 "Top habitability candidate after Earth."
    },
    {
        "name": "Mimas",
        "type": "moon (Saturn)",
        "intrinsic_field": "none",
        "induced_field": "minimal",
        "magnetic_boundary": "no",
        "field_strength_nT": 0,            # no significant field perturbation
        "liquid_water": "possible",        # surprising: Cassini libration suggests internal ocean (Lainey 2024)
        "atmosphere": "none",
        "energy_source": "tidal (weak)",
        "organics_detected": False,
        "habitability": "candidate",       # upgraded due to 2024 ocean discovery
        "notes": "SURPRISE: Lainey et al. 2024 (Nature) found large libration implying young internal ocean. "
                 "No magnetic signature detected. No atmosphere. Very cold. "
                 "If ocean confirmed, this is a potential COUNTEREXAMPLE: ocean body with no magnetic boundary. "
                 "However, ocean may be too young/small to generate detectable induced field. "
                 "Cassini data limited for Mimas."
    },
    {
        "name": "Rhea",
        "type": "moon (Saturn)",
        "intrinsic_field": "none",
        "induced_field": "possible weak",
        "magnetic_boundary": "no confirmed boundary",
        "field_strength_nT": 0,            # Cassini found no clear induced field
        "liquid_water": "none",
        "atmosphere": "none",              # tenuous O2/CO2 exosphere
        "energy_source": "minimal",
        "organics_detected": False,
        "habitability": "dead",
        "notes": "Second largest Saturnian moon. No significant magnetic signature. "
                 "Cassini found possible ring/debris disk (later disputed). "
                 "No ocean evidence. Geologically inactive."
    },

    # ---- NEPTUNIAN MOON ----
    {
        "name": "Triton",
        "type": "moon (Neptune)",
        "intrinsic_field": "none",
        "induced_field": "yes — interaction with Neptune's magnetosphere",
        "magnetic_boundary": "yes — induced boundary in Neptune's tilted field",
        "field_strength_nT": 10,           # estimated from Neptune's field at Triton's orbit
        "liquid_water": "possible",        # subsurface ocean suggested by tidal heating models
        "atmosphere": "thin",              # tenuous N2 atmosphere, ~1.4 Pa
        "energy_source": "tidal (retrograde orbit), geothermal",
        "organics_detected": True,         # N2, CH4, CO, CO2 ices; tholins
        "habitability": "candidate",
        "notes": "Captured KBO. Active geysers (N2). Retrograde orbit = strong tidal dissipation. "
                 "Subsurface ocean plausible (Nimmo & Spencer 2015). Within Neptune's magnetosphere. "
                 "Neptune's highly tilted field creates complex interaction. Trident mission proposed."
    },

    # ---- DWARF PLANETS ----
    {
        "name": "Pluto",
        "type": "dwarf planet",
        "intrinsic_field": "none detected",
        "induced_field": "possible — solar wind interaction",
        "magnetic_boundary": "possible — New Horizons detected interaction region",
        "field_strength_nT": 0,            # no clear field; possible weak interaction boundary
        "liquid_water": "possible",        # subsurface ocean (Nimmo 2016, Bierson 2020)
        "atmosphere": "thin",              # ~1 Pa N2 atmosphere (New Horizons)
        "energy_source": "minimal",        # some radiogenic, tidal from Charon
        "organics_detected": True,         # tholins, CH4, N2 ices, complex surface chemistry
        "habitability": "candidate",       # weak — very cold, but possible subsurface ocean
        "notes": "New Horizons found complex geology, possible subsurface ocean (Nimmo, Bierson). "
                 "Atmospheric interaction with solar wind creates bow shock-like structure (McComas 2016). "
                 "Very weak: whether this counts as 'magnetic boundary' is debatable. "
                 "Extremely cold surface (44 K). Organics present."
    },
    {
        "name": "Ceres",
        "type": "dwarf planet",
        "intrinsic_field": "none detected",
        "induced_field": "possible — solar wind interaction",
        "magnetic_boundary": "possible — Dawn detected some magnetic disturbance, ambiguous",
        "field_strength_nT": 0,            # Dawn magnetometer data ambiguous
        "liquid_water": "possible",        # subsurface brine reservoir (Occator crater, De Sanctis 2020)
        "atmosphere": "thin",              # transient water vapor exosphere
        "energy_source": "solar, radiogenic",
        "organics_detected": True,         # aliphatic organics (De Sanctis 2017, Science)
        "habitability": "candidate",       # weak but real: brines, organics
        "notes": "Dawn found organics (De Sanctis 2017), subsurface brine (Nathues 2020, Raymond 2020). "
                 "Transient water vapor. Occator crater bright spots = recent brine eruption. "
                 "Magnetic data from Dawn ambiguous — no clear magnetosphere. "
                 "Weak candidate but real: organics + brines + energy."
    },

    # ---- ASTEROID ----
    {
        "name": "Bennu",
        "type": "asteroid",
        "intrinsic_field": "none",
        "induced_field": "none",
        "magnetic_boundary": "no",
        "field_strength_nT": 0,
        "liquid_water": "none",            # hydrated minerals, no liquid
        "atmosphere": "none",
        "energy_source": "solar",
        "organics_detected": True,         # OSIRIS-REx: amino acids including aromatic (Lauretta 2024, Nature)
        "habitability": "dead",
        "notes": "C-type asteroid. OSIRIS-REx returned samples with amino acids including aromatic ones. "
                 "No liquid water (hydrated clays only). No atmosphere. No magnetic field. "
                 "Organics present but no habitability."
    },

    # ---- EARTH'S MOON ----
    {
        "name": "Luna (Moon)",
        "type": "moon (Earth)",
        "intrinsic_field": "none (lost ~3.2 Gya)",
        "induced_field": "weak — Earth's magnetotail interaction",
        "magnetic_boundary": "partial — passes through Earth's magnetotail; crustal magnetic anomalies",
        "field_strength_nT": 2,            # ~1-10 nT crustal anomalies; no global field
        "liquid_water": "none",            # ice at poles, no liquid
        "atmosphere": "none",              # exosphere
        "energy_source": "solar",
        "organics_detected": False,
        "habitability": "dead",
        "notes": "Lost global field ~3.2 Gya (Tikoo 2017). Crustal magnetic anomalies (swirls). "
                 "Passes through Earth's magnetotail ~4 days/month. Polar water ice (LCROSS). "
                 "No atmosphere, no liquid water, no habitability."
    },
]


# ============================================================
# ANALYSIS
# ============================================================

def has_magnetic_boundary(body):
    """Return True if body has any form of magnetic boundary."""
    mb = body["magnetic_boundary"].lower()
    if mb.startswith("yes"):
        return True
    if mb.startswith("no"):
        return False
    if "partial" in mb or "possible" in mb:
        return "partial"
    return False

def is_habitable_candidate(body):
    """Return True if body is 'candidate' or 'confirmed habitable'."""
    return body["habitability"] in ("candidate", "confirmed habitable")

def count_habitability_indicators(body):
    """Count positive habitability indicators (0-4)."""
    count = 0
    if body["liquid_water"] in ("confirmed", "possible"):
        count += 1
    if body["atmosphere"] in ("substantial", "thin"):
        count += 1
    if body["energy_source"] not in ("none", "minimal"):
        count += 1
    if body["organics_detected"]:
        count += 1
    return count


def main():
    print("=" * 120)
    print("SOLAR SYSTEM: MAGNETIC BOUNDARIES vs HABITABILITY")
    print("Testing: 'Every solar system body with habitability potential has a magnetic boundary'")
    print("=" * 120)
    print()

    # ---- MAIN TABLE ----
    header = f"{'Body':<16} {'Type':<20} {'Mag. Boundary':<14} {'Field (nT)':<12} {'Water':<12} {'Atmo':<14} {'Energy':<16} {'Org.':<6} {'Habit.':<12}"
    print(header)
    print("-" * len(header))

    for b in bodies:
        mb = has_magnetic_boundary(b)
        if mb is True:
            mb_str = "YES"
        elif mb == "partial":
            mb_str = "PARTIAL"
        else:
            mb_str = "NO"

        org_str = "Yes" if b["organics_detected"] else "No"

        print(f"{b['name']:<16} {b['type']:<20} {mb_str:<14} {b['field_strength_nT']:<12} "
              f"{b['liquid_water']:<12} {b['atmosphere']:<14} {b['energy_source']:<16} "
              f"{org_str:<6} {b['habitability']:<12}")

    print()

    # ---- CORRELATION ANALYSIS ----
    print("=" * 120)
    print("CORRELATION ANALYSIS")
    print("=" * 120)
    print()

    candidates = [b for b in bodies if is_habitable_candidate(b)]
    dead_bodies = [b for b in bodies if not is_habitable_candidate(b)]

    print(f"Total bodies analyzed: {len(bodies)}")
    print(f"Habitable candidates (candidate + confirmed): {len(candidates)}")
    print(f"Dead bodies: {len(dead_bodies)}")
    print()

    # Q1: Of habitable candidates, how many have magnetic boundary?
    cand_with_boundary = [b for b in candidates if has_magnetic_boundary(b) is True]
    cand_with_partial = [b for b in candidates if has_magnetic_boundary(b) == "partial"]
    cand_without = [b for b in candidates if has_magnetic_boundary(b) is False]

    print("--- Q1: Habitable candidates with magnetic boundary ---")
    print(f"  Full magnetic boundary:    {len(cand_with_boundary)}/{len(candidates)} "
          f"({100*len(cand_with_boundary)/len(candidates):.1f}%)")
    for b in cand_with_boundary:
        print(f"    - {b['name']}: {b['magnetic_boundary']}")

    print(f"  Partial/possible boundary: {len(cand_with_partial)}/{len(candidates)} "
          f"({100*len(cand_with_partial)/len(candidates):.1f}%)")
    for b in cand_with_partial:
        print(f"    - {b['name']}: {b['magnetic_boundary']}")

    print(f"  NO magnetic boundary:      {len(cand_without)}/{len(candidates)} "
          f"({100*len(cand_without)/len(candidates):.1f}%)")
    for b in cand_without:
        print(f"    *** COUNTEREXAMPLE: {b['name']}: {b['magnetic_boundary']}")
        print(f"        Habitability: {b['habitability']}, Water: {b['liquid_water']}, "
              f"Notes: {b['notes'][:120]}...")

    total_with_any = len(cand_with_boundary) + len(cand_with_partial)
    print(f"\n  Fraction with ANY boundary (full + partial): {total_with_any}/{len(candidates)} "
          f"= {100*total_with_any/len(candidates):.1f}%")
    print()

    # Q2: Of bodies with NO magnetic boundary, any habitability?
    no_boundary = [b for b in bodies if has_magnetic_boundary(b) is False]
    no_boundary_hab = [b for b in no_boundary if count_habitability_indicators(b) > 0]

    print("--- Q2: Bodies with NO magnetic boundary ---")
    print(f"  Total with no boundary: {len(no_boundary)}")
    print(f"  Of those, with any habitability indicator: {len(no_boundary_hab)}")
    for b in no_boundary_hab:
        indicators = count_habitability_indicators(b)
        print(f"    - {b['name']}: {indicators} indicator(s) — "
              f"water={b['liquid_water']}, atmo={b['atmosphere']}, "
              f"energy={b['energy_source']}, organics={b['organics_detected']}")
    print()

    # Q3: Bodies with NO magnetic boundary AND marked as candidates
    print("--- Q3: COUNTEREXAMPLES — Candidate bodies with NO magnetic boundary ---")
    counterexamples = [b for b in candidates if has_magnetic_boundary(b) is False]
    if counterexamples:
        for b in counterexamples:
            print(f"  *** {b['name']} ({b['type']})")
            print(f"      Habitability: {b['habitability']}")
            print(f"      Water: {b['liquid_water']}")
            print(f"      Atmosphere: {b['atmosphere']}")
            print(f"      Energy: {b['energy_source']}")
            print(f"      Organics: {b['organics_detected']}")
            print(f"      Notes: {b['notes']}")
            print()
    else:
        print("  None found.")
    print()

    # ---- CONTINGENCY TABLE ----
    print("=" * 120)
    print("CONTINGENCY TABLE (2x2)")
    print("=" * 120)
    print()

    # Classify: magnetic boundary (yes/partial vs no) x habitability (candidate+ vs dead)
    a = len([b for b in bodies if has_magnetic_boundary(b) in (True, "partial") and is_habitable_candidate(b)])
    b_val = len([b for b in bodies if has_magnetic_boundary(b) in (True, "partial") and not is_habitable_candidate(b)])
    c = len([b for b in bodies if has_magnetic_boundary(b) is False and is_habitable_candidate(b)])
    d = len([b for b in bodies if has_magnetic_boundary(b) is False and not is_habitable_candidate(b)])

    print(f"                          Habitable candidate    Dead")
    print(f"  Has magnetic boundary:       {a:>4}              {b_val:>4}")
    print(f"  No magnetic boundary:        {c:>4}              {d:>4}")
    print()

    # Sensitivity and specificity
    if a + c > 0:
        sensitivity = a / (a + c)
        print(f"  Sensitivity (mag boundary | habitable): {sensitivity:.1%}")
    if d + b_val > 0:
        specificity = d / (d + b_val)
        print(f"  Specificity (no boundary | dead):       {specificity:.1%}")

    # Positive/negative predictive values
    if a + b_val > 0:
        ppv = a / (a + b_val)
        print(f"  Positive predictive value:              {ppv:.1%}")
    if c + d > 0:
        npv = d / (c + d)
        print(f"  Negative predictive value:              {npv:.1%}")

    # Fisher exact-ish (for this small N, just report)
    n = a + b_val + c + d
    print(f"\n  Total classified: {n}")
    print()

    # ---- STRICT vs GENEROUS SCORING ----
    print("=" * 120)
    print("STRICT vs GENEROUS INTERPRETATION")
    print("=" * 120)
    print()

    # Strict: only "yes" counts as boundary; only "confirmed" + strong candidates
    strict_candidates = [b for b in bodies if b["habitability"] in
                         ("confirmed habitable", "candidate") and b["liquid_water"] in ("confirmed", "possible")]
    strict_with = [b for b in strict_candidates if has_magnetic_boundary(b) is True]
    strict_partial = [b for b in strict_candidates if has_magnetic_boundary(b) == "partial"]
    strict_without = [b for b in strict_candidates if has_magnetic_boundary(b) is False]

    print("STRICT: Candidates must have confirmed/possible water AND be rated candidate+")
    print(f"  Total strict candidates: {len(strict_candidates)}")
    print(f"  With clear magnetic boundary:  {len(strict_with)} "
          f"({100*len(strict_with)/max(len(strict_candidates),1):.1f}%)")
    for b in strict_with:
        print(f"    - {b['name']}")
    print(f"  With partial/possible boundary: {len(strict_partial)} "
          f"({100*len(strict_partial)/max(len(strict_candidates),1):.1f}%)")
    for b in strict_partial:
        print(f"    - {b['name']}")
    print(f"  With NO boundary:              {len(strict_without)} "
          f"({100*len(strict_without)/max(len(strict_candidates),1):.1f}%)")
    for b in strict_without:
        print(f"    *** COUNTEREXAMPLE: {b['name']} — water: {b['liquid_water']}, notes: {b['notes'][:100]}...")
    print()

    # ---- DETAILED NOTES ON EDGE CASES ----
    print("=" * 120)
    print("EDGE CASES AND HONEST ASSESSMENT")
    print("=" * 120)
    print()

    print("""MIMAS — POTENTIAL COUNTEREXAMPLE:
  Lainey et al. 2024 (Nature) discovered Mimas likely has a young internal ocean
  based on libration measurements from Cassini. No magnetic field or boundary has
  been detected. If the ocean is confirmed, Mimas would be a habitable-candidate
  body with NO magnetic boundary. However:
  - The ocean may be very young (~5-15 Myr) and beneath a thick (~20-30 km) ice shell
  - Cassini's magnetic data coverage of Mimas was limited
  - A conducting ocean SHOULD produce an induced field in Saturn's rotating field,
    but it may be too deep/small to detect (like early Europa before Galileo close passes)
  - Verdict: POSSIBLE counterexample. Needs dedicated magnetic survey.

CERES — AMBIGUOUS:
  Dawn mission found organics and subsurface brines, making Ceres a weak habitability
  candidate. Magnetic data from Dawn is ambiguous — no clear magnetosphere detected.
  - The brine reservoir is small and localized
  - Solar wind interaction may create a very weak boundary
  - Verdict: AMBIGUOUS. Not clearly a counterexample, not clearly consistent.

PLUTO — AMBIGUOUS:
  New Horizons detected a solar wind interaction region (heavy ion escape, McComas 2016).
  Whether this constitutes a "magnetic boundary" is debatable — it's more of a
  mass-loading interaction than a magnetopause.
  Subsurface ocean evidence (Nimmo 2016, Bierson 2020) makes it a weak candidate.
  - Verdict: AMBIGUOUS on both counts.

VENUS (surface) — CONSISTENT:
  Venus has an induced magnetosphere but is uninhabitable at the surface.
  Cloud-deck habitability hypothesis exists but is speculative.
  This is NOT a counterexample to the prediction, since the prediction says
  magnetic boundary is NECESSARY, not SUFFICIENT.

MERCURY — CONSISTENT:
  Has a magnetic field/boundary but is dead. Consistent: magnetic boundary
  is necessary, not sufficient. Mercury has the boundary but lacks water and atmosphere.

GAS GIANTS — CONSISTENT:
  Strong magnetic fields but no solid surfaces or habitable conditions.
  Again, boundary is necessary not sufficient.
""")

    # ---- FINAL VERDICT ----
    print("=" * 120)
    print("FINAL VERDICT")
    print("=" * 120)
    print()

    print("""PREDICTION: "Every solar system body with habitability potential has a magnetic boundary."

RESULT: LARGELY SUPPORTED, with one potential counterexample.

Strong support:
  - Earth: strong dipole, confirmed habitable
  - Europa: induced field from ocean in Jupiter's field, strong candidate
  - Ganymede: intrinsic dipole (unique moon!), subsurface ocean
  - Enceladus: within Saturn's magnetosphere, confirmed ocean + organics
  - Titan: within Saturn's magnetosphere + induced boundary, thick atmosphere + lakes
  - Mars: crustal remnants + induced boundary, past habitability + possible subsurface water
  - Triton: within Neptune's magnetosphere, possible ocean + geysers
  - Callisto: weak induced field, possible ocean

Potential counterexample:
  - Mimas: possible ocean (Lainey 2024), NO detected magnetic boundary
    However: limited magnetic data; conducting ocean SHOULD produce induced field
    that future missions may detect.

Ambiguous cases:
  - Ceres: weak candidate, ambiguous magnetic data
  - Pluto: weak candidate, ambiguous interaction region

Negative controls (consistent):
  - Luna, Io, Rhea, Bennu: no/minimal magnetic boundary, dead/no habitability
  - Mercury, gas giants: magnetic boundary present, but dead for other reasons
    (confirming boundary is necessary, not sufficient)

QUANTITATIVE SUMMARY:
""")

    # Final numbers
    clear_candidates = [b for b in candidates if b["liquid_water"] in ("confirmed", "possible")]
    n_cc = len(clear_candidates)
    n_cc_boundary = len([b for b in clear_candidates if has_magnetic_boundary(b) in (True, "partial")])
    n_cc_none = len([b for b in clear_candidates if has_magnetic_boundary(b) is False])

    print(f"  Candidate bodies with water (confirmed/possible): {n_cc}")
    print(f"  Of those with magnetic boundary (full or partial): {n_cc_boundary} ({100*n_cc_boundary/n_cc:.0f}%)")
    print(f"  Of those with NO detected boundary:               {n_cc_none} ({100*n_cc_none/n_cc:.0f}%)")
    print()
    print(f"  If Mimas ocean is confirmed and no induced field found: prediction FALSIFIED.")
    print(f"  If Mimas induced field IS found (likely): prediction holds at {n_cc}/{n_cc} = 100%.")
    print()
    print(f"  Current honest score: {n_cc_boundary}/{n_cc} = {100*n_cc_boundary/n_cc:.0f}% "
          f"(with {n_cc_none} ambiguous)")
    print()

    # Framework interpretation
    print("=" * 120)
    print("FRAMEWORK INTERPRETATION")
    print("=" * 120)
    print()
    print("""The correlation between magnetic boundaries and habitability is well-known in
planetary science (atmospheric protection from solar wind stripping). The framework
adds a STRONGER claim: the magnetic boundary is not just protective but is itself
a domain wall structure that participates in the coupling mechanism.

Standard explanation: magnetic field -> atmosphere retention -> liquid water -> life
Framework claim:     magnetic boundary IS a domain wall -> coupling medium -> habitability

These are empirically indistinguishable with current data. The framework prediction
becomes distinctive only if it predicts WHICH magnetic configurations enable
habitability (e.g., PT depth n>=2) rather than just "has boundary."

The data is consistent with the prediction but does not uniquely support the framework
interpretation over the standard planetary science explanation.
""")


if __name__ == "__main__":
    main()
