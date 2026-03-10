# Huckel Bridge: Does the HOMO-LUMO Gap of Aromatics Connect to mu/3?

**Date:** 2026-02-25
**Script:** `theory-tools/huckel_bridge.py`
**Status:** HONEST ASSESSMENT -- the connection is weaker than claimed

---

## Executive Summary

The framework claims mu/3 = 612 THz is the "aromatic oscillation frequency" and a deep connection between particle physics and biology. This document reports the results of a rigorous quantum chemistry calculation testing that claim.

**Verdict: The claim is a unit-dependent numerical coincidence, not a derived result.**

- The HOMO-LUMO gap of benzene is 4.90 eV = 1184 THz, roughly **double** mu/3
- The individual aromatic amino acids (Trp, Tyr, Phe) absorb at 250-290 nm = 1030-1200 THz, far from 613 THz
- The Craddock 613 THz is a **collective** London dispersion oscillation of 86 aromatics in tubulin, not a single-molecule property
- The "mu/3 = 613 THz" equation requires multiplying a dimensionless number by 1 THz (an SI unit with no fundamental significance)
- The unit-independent statement is: f_Craddock ~ (3/16) * f_Rydberg = H_beta (the hydrogen Balmer-beta line at 617 THz)
- Three different formulas (mu/3, 8*f_R/sqrt(mu), 3*f_R/16) all give ~612-617 THz but are **not algebraically equivalent** (differ by 0.35%)

---

## Part 1: Huckel Energy Levels

Using the standard Huckel molecular orbital method with |beta| = 2.72 eV (spectroscopic resonance integral):

| Molecule | N_pi | Huckel gap (eV) | Expt S1 (eV) | Expt (nm) | f (THz) | vs 613 THz |
|----------|------|----------------|--------------|-----------|---------|------------|
| Benzene | 6 | 5.44 | 4.90 | 253 | 1185 | 6.7% |
| Naphthalene | 10 | 3.36 | 3.97 | 312 | 960 | 43.4% |
| Anthracene | 14 | 3.29 | 3.31 | 375 | 800 | 69.4% |
| Tetracene | 18 | 2.83 | 2.63 | 471 | 636 | 96.3% |
| Pentacene | 22 | 2.73 | 2.14 | 580 | 517 | 84.4% |
| Indole (Trp) | 10 | 3.58 | 4.36 | 284 | 1054 | 28.0% |
| GFP (S65T) | 12 | 3.74 | 2.54 | 489 | 614 | **99.8%** |

**Key result:** Benzene is at 1184 THz, almost exactly 2x the target. Only GFP matches 613 THz, and GFP is a jellyfish protein, not a universal aromatic property. The biologically relevant aromatics (indole/tryptophan, tyrosine, phenylalanine) absorb at 250-290 nm, far from 489 nm.

## Part 2: What the Craddock 613 THz Actually Is

The Craddock et al. 2017 (Scientific Reports 7:9877) value is **not** a single-molecule absorption. It is:

1. Take the tubulin alpha-beta dimer crystal structure
2. Identify all 86 aromatic amino acids (Trp, Tyr, Phe)
3. Compute collective dipole oscillation modes of London dispersion forces among pi-electron clouds
4. Find ~400+ normal modes spanning 480-700 THz
5. The mode at 613 +/- 8 THz shows the strongest shift when anesthetics are docked

This is a **many-body DFT calculation** specific to tubulin's 3D structure. Different proteins would give different frequencies. The individual aromatics absorb in the UV; the 613 THz emerges from their **collective** coupling.

## Part 3: The Dimensional Analysis Problem

The identity "mu/3 = 613 THz" is unit-dependent:

- mu = m_p / m_e = 1836.15267 (dimensionless)
- mu/3 = 612.05 (dimensionless)
- This equals 612.05 only in **THz** (= 10^12 Hz)
- In GHz: mu/3 GHz = 0.612 GHz (meaningless)
- In PHz: mu/3 PHz = 612050 PHz (meaningless)

The factor 10^12 is a human convention (base-10 number system, SI prefixes). It has no physical significance.

## Part 4: Unit-Independent Reformulations

Three different routes all give ~612-617 THz:

| Route | Formula | Value (THz) | Physical meaning |
|-------|---------|-------------|-----------------|
| mu/3 | mu/3 * 1 THz | 612.05 | Dimensionless number * anthropic unit |
| Born-Oppenheimer | 8 * f_R / sqrt(mu) | 614.20 | Molecular vibration scale * 8 |
| H_beta | (3/16) * f_Rydberg | 616.85 | Hydrogen Balmer-beta line |

These are **not** algebraically equivalent. Testing the identity mu^(3/2)/3 = 4*alpha^2*m_e*c^2/(h*10^12) gives a ratio of 0.9965 -- they differ by 0.35%.

The **physically meaningful** comparison is:

> f_Craddock / f_Rydberg = 0.1863 ~ 3/16 = 0.1875 (99.4% match)

This says the Craddock frequency has energy close to the hydrogen H_beta line. The H_beta connection is unit-independent and corresponds to real atomic physics (the n=4 to n=2 transition).

## Part 5: Acene Scaling Law

The HOMO-LUMO gap of linear acenes decreases with system size:

- Fit: E_gap = 21.64/N + 1.49 eV (R^2 = 0.93)
- To reach 2.54 eV (= 613 THz), need N ~ 20 conjugated atoms
- This is between tetracene (18 atoms) and pentacene (22 atoms)
- Biology does NOT use linear acenes for consciousness-related functions

## Part 6: Why Everything Falls Near 613 THz

The visible light range (400-700 nm = 430-750 THz) is set by:
- E_Rydberg = 13.6 eV (hydrogen ionization)
- Visible photon energies = E_R * (small fractions) ~ 1.8-3.1 eV
- These fractions come from Balmer/Lyman series: 1/4, 3/16, 5/36, etc.

Since biology evolved under sunlight, biological chromophores necessarily operate in the 400-700 nm window. The Rydberg energy itself depends on alpha^2 * m_e * c^2, and mu = m_p/m_e, so **any** combination of alpha, mu, and small integers will produce values scattered across the visible range.

The "coincidence" that mu/3 falls in the visible range is approximately equivalent to saying:
> mu/3 * h * 10^12 ~ alpha^2 * m_e * c^2 / 10

which reduces to mu^(3/2) ~ 10^4 * alpha^2 / 3. This holds to 0.35%, but there is no known reason it should be exact.

## Part 7: The Honest Scorecard

| Claim | Status | Evidence |
|-------|--------|----------|
| "Benzene HOMO-LUMO gap = mu/3" | **FALSE** | Benzene gap is 4.90 eV = 1184 THz, not 612 THz |
| "Aromatic absorption is at 613 THz" | **MISLEADING** | Individual aromatics absorb at 250-290 nm (UV), not 489 nm |
| "mu/3 = 613 THz" | **UNIT-DEPENDENT** | Only works in THz; no fundamental reason for this unit choice |
| "mu/3 THz = H_beta" | **APPROXIMATE** | 612.05 vs 616.85 THz = 99.2% match, but different formulas |
| "Craddock R^2 = 0.999" | **REAL** | Published experimental result, but specific to tubulin |
| "8*f_R/sqrt(mu) = 614 THz" | **REAL** | Valid Born-Oppenheimer scaling, but applies to vibrations not electronic transitions |
| "f_Craddock / f_Rydberg ~ 3/16" | **REAL, UNIT-INDEPENDENT** | The strongest honest statement |

## Part 8: What Would Close the Gap

To establish a genuine connection between mu and aromatic chemistry, one would need:

**A) Microscopic derivation:** Show that a specific aromatic system has E_transition = alpha^2 * m_e * c^2 * 3/32 from quantum mechanics, AND explain why biology selected this system.

**B) Many-body derivation:** Show that London dispersion oscillations in a network of N aromatic residues at separation R give f = m_p*c^2/(3h), with N and R determined by protein-folding physics.

**C) Statistical test:** Compute how many numerical coincidences of this quality one expects when searching through combinations of {alpha, mu, phi, small integers} and comparing to ~20 biological frequencies. If mu/3 = 612 THz is significantly more precise than expected by chance, that would be evidence.

**D) Independent measurement:** If other aromatic-rich proteins (not just tubulin) also show collective oscillation modes near 613 THz, that would suggest a universal feature rather than a tubulin-specific one.

None of these have been done.

## Part 9: Recommended Framework Update

The following changes should be made to the framework documentation:

1. **Downgrade** "mu/3 = 613 THz" from "derived" to "suggestive numerical coincidence"
2. **Add** the dimensional analysis caveat: "mu/3 interpreted as THz requires the SI prefix tera (10^12), which is not a fundamental unit"
3. **Replace** "aromatic absorption at 613 THz" with "collective London dispersion oscillation in tubulin at 613 THz (Craddock 2017)"
4. **Highlight** the unit-independent statement: "f_Craddock / f_Rydberg ~ 3/16 (H_beta ratio)" as the strongest formulation
5. **Acknowledge** that individual aromatic amino acids absorb in the UV (250-290 nm), not at 489 nm
6. **Keep** the mu/18 = O-H stretch connection (102 THz), which has the same dimensional issue but is independently interesting

## Part 10: What Survives

Despite the mu/3 problem, several observations remain noteworthy:

1. **All neurotransmitters are aromatic** -- this is a real biochemical fact, not a numerical claim
2. **Anesthetics disrupt aromatic stacking** -- the Craddock R^2 = 0.999 correlation is published and real
3. **Tubulin aromatics have collective oscillations** -- confirmed computationally (Craddock 2017) and experimentally (Kalra, Scholes et al. 2023)
4. **The visible-light window is set by the Rydberg scale** -- this is standard atomic physics
5. **Biology operates in the 2-3 eV energy range** -- constrained by stellar spectra and atmospheric transmission

The framework's biology claims should be rebuilt on these solid foundations rather than the unit-dependent mu/3 coincidence.

---

**Bottom line:** The HOMO-LUMO gap of benzene does NOT equal mu/3. The 613 THz is a tubulin-specific collective oscillation, not a universal aromatic frequency. The identity "mu/3 = 613 THz" is real arithmetic but depends on the anthropic choice of THz as the unit. The strongest honest reformulation is f_Craddock ~ (3/16) * f_Rydberg, which connects to the hydrogen Balmer-beta line in a unit-independent way.
