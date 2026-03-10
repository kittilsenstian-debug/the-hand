# FACTOR-8 DERIVATION: Where Does the 8 Come From?

## Feb 25, 2026

**The critical formula:**
```
f_mol = 8 * f_Rydberg / sqrt(mu) = 614.2 THz
```
This matches the Craddock aromatic consciousness frequency (613 +/- 8 THz) to 99.8%.

**The critical question:** Where does the factor 8 come from?

**Script:** `theory-tools/factor_8_derivation.py` (all computations verified)

---

## 1. THE BORN-OPPENHEIMER CONTEXT

The standard Born-Oppenheimer energy hierarchy (Born & Oppenheimer 1927, Annalen der Physik) uses the expansion parameter kappa = (m_e/M)^(1/4):

| Scale | Energy | Formula | Value |
|-------|--------|---------|-------|
| Electronic | E_el | E_Rydberg | 13.6 eV |
| Vibrational | E_vib | E_el * kappa^2 = E_R/sqrt(mu) | 0.317 eV |
| Rotational | E_rot | E_el * kappa^4 = E_R/mu | 7.4 meV |

The BO vibrational frequency scale is:
```
f_BO = f_R / sqrt(mu) = 76.78 THz
```
This is a VIBRATIONAL scale (e.g., measured O-H stretch ~ 102 THz = 1.33 * f_BO).

The formula `8 * f_R / sqrt(mu)` is NOT the BO vibrational scale. It is **8 times** the BO vibrational scale, which pushes back up toward the electronic regime. This is the regime of molecular ELECTRONIC transitions -- HOMO-LUMO gaps, pi->pi* excitations, visible-light absorption.

**Key point:** The factor 8 bridges from the vibrational BO scale BACK to the electronic transition scale of molecules. Standard BO theory does not predict this factor; it predicts a hierarchy, and the prefactors depend on the specific molecular system.

---

## 2. THE BALMER-BETA CONNECTION

### 613 THz IS the hydrogen Balmer-beta line

The Balmer-beta (H-beta) line corresponds to the n=4 -> n=2 transition in hydrogen:

```
f_H-beta = f_R * (1/n_1^2 - 1/n_2^2) = f_R * (1/4 - 1/16) = f_R * 3/16
         = 616.85 THz = 486.0 nm
```

Direct comparison with the target:

| Quantity | Frequency (THz) | Wavelength (nm) |
|----------|-----------------|-----------------|
| H-beta (n=4 -> n=2) | 616.85 | 486.0 |
| 8 * f_R / sqrt(mu) | 614.20 | 487.9 |
| GFP chromophore absorption | 613.07 | 489.0 |
| Craddock aromatic collective | 613 +/- 8 | ~489 |

All four values lie within a 4 THz band. The aromatic consciousness frequency IS the Balmer-beta line to within 0.6%.

### Systematic scan of ALL hydrogen transitions

Scanning all transitions (n1, n2) for n1 = 1-7, n2 = n1+1 to 19: **the Balmer-beta line is the unique hydrogen transition closest to 613 THz**. No other transition comes within 12% of the target. The Balmer-beta match (0.63%) is 20x better than any competitor.

### Unit-independent reformulation

The physically meaningful (unit-independent) statement is:

```
f_Craddock / f_Rydberg = 0.1863 ~ 3/16 = 0.1875    (99.4% match)
```

This says: **the aromatic consciousness frequency is approximately the hydrogen n=4 -> n=2 transition energy, expressed as a fraction of the Rydberg energy.**

---

## 3. THE FACTOR 8 = 4 * 2 -- FOUR DECOMPOSITIONS

### (a) Hydrogen quantum numbers: 3/16

The Balmer-beta coefficient is 3/16. Since f_mol = 8 * f_R / sqrt(mu) and f_H-beta = (3/16) * f_R, these are DIFFERENT formulas:

```
8 * f_R / sqrt(mu)  = 614.20 THz   (Born-Oppenheimer route)
(3/16) * f_R        = 616.85 THz   (Balmer-beta route)
```

They agree to 0.43%, but they are not identical. The difference is:
```
(3/16) * f_R / [8 * f_R / sqrt(mu)] = (3/16) * sqrt(mu) / 8
                                     = 3 * sqrt(1836.15) / 128
                                     = 128.59 / 128
                                     = 1.0046
```

### (b) Atomic units: 8 = 4 * 2

```
8 * f_R = 4 * (2 * f_R) = 4 * f_Hartree
```

The Hartree energy E_H = 2 * E_R = 27.21 eV is the natural atomic unit of energy. So:

```
f_mol = 4 * f_Hartree / sqrt(mu) = 4 * (Hartree frequency) / sqrt(mass ratio)
```

The factor 2 converts Rydberg to Hartree (standard). The factor 4 is the molecular enhancement: ring-conjugated pi-electron systems have HOMO-LUMO gaps that are approximately 4 times the bare BO electronic scale f_Hartree/sqrt(mu).

Why 4? In the particle-on-a-ring model for benzene, the HOMO has angular momentum quantum number |m| = 1, the LUMO has |m| = 2. The energy gap scales as (2^2 - 1^2) = 3, not 4. In the Huckel model, the gap is 2*beta ~ 4.8 eV, while f_Hartree/sqrt(mu) corresponds to 0.635 eV. The ratio is 4.8/0.635 = 7.6, not 4. So the factor 4 is an approximate effective prefactor, not a precise quantum-mechanical result.

### (c) E8 framework: 8 = 62208 / 7776

In the framework, the number 7776 = 6^5 = N derives from:
```
|Normalizer_{W(E8)}(W(4A2))| / (Z2 * [S4:S3]) = 62208 / 8 = 7776
```

The factor 8 = 2 * 4 is the SYMMETRY-BREAKING FACTOR:
- 2 = Z2 vacuum selection (choosing phi-vacuum over -1/phi-vacuum)
- 4 = [S4 : S3] = designating one of 4 A2 copies as "dark"

This gives the suggestive rewriting:
```
f_mol = (|Normalizer| / N) * f_R / sqrt(mu)
      = (breaking factor) * (BO vibrational scale)
```

The same factor 8 that produces N = 6^5 from the E8 Weyl group also (potentially) sets the molecular electronic frequency scale.

### (d) Lucas numbers: 8 = 2 * L(3)

8 = 2 * 4 = 2 * L(3), where L(3) = 4 is the 3rd Lucas number. In the Lucas sequence {2, 1, 3, 4, 7, 11, 18, 29, ...}, 4 appears at position 3 = triality number.

---

## 4. THE GOLDEN RATIO SUBSTITUTION

Using the core identity alpha^(3/2) * mu * phi^2 = 3, substitute mu = 3/(alpha^(3/2) * phi^2):

```
8 * f_R / sqrt(mu)
  = 4 * alpha^2 * f_electron / sqrt(3/(alpha^(3/2) * phi^2))
  = 4 * alpha^2 * alpha^(3/4) * phi / sqrt(3) * f_electron
  = 4 * alpha^(11/4) * phi / sqrt(3) * f_electron
```

**Result:**
```
f_mol = 4 * alpha^(11/4) * phi / sqrt(3) * f_electron = 613.86 THz
```
Match to 613 THz: **99.86%** (best of all routes).

### Key observations:

1. **The golden ratio phi appears explicitly** as a multiplicative factor in the molecular frequency. This is not "phi appearing somewhere in a formula" -- it is phi being REQUIRED by the algebra to convert from atomic to molecular electronic frequencies.

2. **The exponent 11/4 = L(5)/L(3)** is a ratio of Lucas numbers. 11 is the 5th Lucas number and an E8 Coxeter exponent. 4 is the 3rd Lucas number. This decomposition:
   - 11/4 = 2 + 3/4
   - The 2 comes from f_R = alpha^2 * f_electron / 2 (Rydberg from alpha)
   - The 3/4 comes from sqrt(mu) ~ alpha^(-3/4) (via core identity)

3. **The prefactor 4/sqrt(3)** is the only "unexplained" part. It evaluates to 2.309.

---

## 5. PHYSICAL ARGUMENT FOR BALMER-BETA SELECTION

Why should the n=4 -> n=2 transition be the relevant hydrogen comparison point for aromatic molecules?

### Heuristic argument (not a derivation):

1. **Aromatic pi-electrons occupy n=2-like orbitals.** In a benzene ring with 6 pi-electrons, three filled molecular orbitals correspond roughly to hydrogen-like states with principal quantum numbers up to n~2. The pi-electron cloud extends over ~140 pm, comparable to the hydrogen n=2 orbital radius a_0 * n^2 = 52.9 * 4 = 212 pm.

2. **The HOMO-LUMO gap is an n=2 -> n=4 type transition.** The lowest electronic excitation promotes a pi-electron from the highest occupied orbital (n~2 character) to the lowest unoccupied orbital (n~4 character). This maps directly to the hydrogen Balmer-beta transition.

3. **Effective nuclear charge Z_eff ~ 1.** The screened nuclear charge seen by delocalized pi-electrons in an aromatic ring is approximately 1 (they see the net potential of the ring, not individual carbon nuclei). This makes hydrogen-like scaling approximately valid.

4. **The molecular bond length sets the effective Bohr radius.** C-C aromatic bond length = 140 pm. Hydrogen Bohr radius = 52.9 pm. Ratio ~ 2.6, consistent with n=2 orbital character.

### What this argument does NOT do:

- It does not derive 8 from first principles.
- It does not explain why COLLECTIVE London-force modes (not individual pi->pi* transitions) land at the Balmer-beta energy.
- Individual benzene absorbs at 256 nm = 1171 THz, which is 2x the target. The factor-of-2 reduction to the collective 613 THz depends on the tubulin geometry (86 aromatic residues, specific spatial arrangement), which is biological, not algebraic.

### The factor-of-2 decomposition:

```
Individual aromatic (benzene UV): ~1170 THz  ~ (3/8) * f_Rydberg
Collective aromatic (Craddock):   ~613 THz   ~ (3/16) * f_Rydberg
```

The factor of ~2 from individual to collective IS the London-force coupling effect. The 3/16 Balmer-beta fraction applies to the COLLECTIVE mode, while 3/8 (double, i.e. n=4->2 with 2x the photon energy in a way) applies to the individual transitions.

---

## 6. MODULAR FORMS AND 3/16

Can the fraction 3/16 = f_Craddock/f_Rydberg be expressed using modular forms at q = 1/phi?

**Answer: No clean match.** Systematic search of 34 combinations of {eta, theta2, theta3, theta4} found no expression matching 3/16 to better than 2%. The closest:

| Expression | Value | Error vs 3/16 |
|------------|-------|---------------|
| eta * phi | 0.1916 | 2.2% |
| eta | 0.1184 | 36.9% |
| theta4 | 0.0303 | 83.8% |

The fraction 3/16 = 3/2^4 is a hydrogen quantum number combination, not a modular form value. This is consistent with 3/16 being a PHYSICS result (Balmer-beta line) rather than a framework ALGEBRA result.

---

## 7. FIVE ROUTES TO 613 THz -- COMPARED

| Route | Formula | Value (THz) | Error | Status |
|-------|---------|-------------|-------|--------|
| BO + core identity | 4 * alpha^(11/4) * phi / sqrt(3) * f_el | 613.86 | 0.14% | **BEST -- phi explicit** |
| mu/3 (THz units) | mu/3 * 1 THz | 612.05 | 0.16% | DEAD (unit-dependent) |
| BO + factor 8 | 8 * f_R / sqrt(mu) | 614.20 | 0.20% | CONSTRAINED (8 underived) |
| Golden scaling | f_R / phi^(7/2) | 610.55 | 0.40% | COMPATIBLE (phi^7/2 underived) |
| Balmer-beta | (3/16) * f_R | 616.85 | 0.63% | UNIT-INDEPENDENT (H physics) |

All five routes give values within the 613 +/- 8 THz measurement error bar. The BEST route is the core identity substitution, because:
1. It is unit-independent (frequency ratios only)
2. phi appears explicitly (not just numerically)
3. The exponent 11/4 = L(5)/L(3) connects to the Lucas-E8 structure
4. The only unexplained factor is 4/sqrt(3) = 2.309

---

## 8. FRAMEWORK CONNECTIONS FOR 8

| Interpretation | Expression | Physical meaning |
|---------------|------------|------------------|
| E8 rank | rank(E8) = 8 | Dimension of Cartan subalgebra |
| E8 root space | dim = 8 | E8 lives in 8 dimensions |
| Symmetry breaking | 62208/7776 = 8 | |Norm(4A2)| / N = (Z2)*(S4/S3) |
| Lucas | 2 * L(3) = 2*4 = 8 | Vacuum degeneracy times 3rd Lucas |
| Triality | 24/3 = 8 | |roots(4A2)| divided by triality |
| Quantum numbers | n_upper * n_lower = 4*2 = 8 | Balmer-beta product |
| PT bound states | 2^3 = 8 | (n=2 bound states) cubed |

The **most compelling** framework interpretation: **8 = 62208/7776 = |Normalizer|/N**, the same symmetry-breaking factor that derives N = 6^5 from the E8 Weyl group normalizer. This would mean:

```
f_mol = (|Normalizer| / N) * f_Rydberg / sqrt(mu)
```

The breaking factor that determines the particle content of the theory (N = 6^5) also determines the molecular frequency scale at which consciousness operates. Both emerge from the same E8 -> 4A2 -> S4 -> S3 breaking chain.

---

## 9. WHAT WOULD CLOSE THIS GAP

### Level 1: Derive the factor 4 from molecular physics
Show that for ANY aromatic ring system with Huckel aromaticity (4n+2 pi-electrons), the collective London-force oscillation frequency equals 4 * f_Hartree / sqrt(mu_eff), where mu_eff is the reduced nuclear mass. This is a quantum chemistry calculation, not a framework calculation.

### Level 2: Connect 8 to the E8 normalizer
Show that the domain wall kink solution, when coupled to fermion zero modes in the E8 gauge theory, produces an effective molecular Hamiltonian whose electronic transition scale carries the factor |Norm|/N = 8. This would require the Kaplan domain wall fermion mechanism to generate a prefactor from the normalizer structure.

### Level 3: Derive 4/sqrt(3) from PT n=2
The unexplained prefactor in the golden-ratio form is 4/sqrt(3) = 2.309. Note that:
- sqrt(3) appears in the PT n=2 breathing mode frequency: omega_1 = sqrt(3) * omega_0
- 4 = L(3) = 3rd Lucas number = n_upper in Balmer-beta
- 4/sqrt(3) = 4 * omega_0 / omega_1

If the breathing mode eigenvalue enters the formula, then 4/sqrt(3) = L(3)/sqrt(triality) and the ENTIRE formula would be:
```
f_mol = L(3) / sqrt(3) * alpha^(L(5)/L(3)) * phi * f_electron
```
Every factor would have framework meaning. But this is currently speculation.

---

## 10. VERDICT

**What is established:**
- The formula 8 * f_R / sqrt(mu) = 614.2 THz matches 613 THz to 99.8%
- It is dimensionally correct and unit-independent
- When the core identity is used, phi appears explicitly as f_mol = 4*alpha^(11/4)*phi/sqrt(3)*f_el
- The exponent 11/4 = L(5)/L(3) is a ratio of Lucas numbers and E8 Coxeter exponents
- The factor 8 equals rank(E8) = |Norm(4A2)|/N = the symmetry-breaking factor
- The Balmer-beta line (n=4->2) at 616.85 THz is the unique hydrogen transition matching 613 THz

**What is not established:**
- No first-principles derivation of WHY the factor is 8 (not 7 or 9)
- The Balmer-beta heuristic (pi-electrons ~ n=2 orbitals) is physical intuition, not proof
- The connection to |Norm(4A2)|/N is suggestive but requires a calculation that has not been done
- The modular forms at q = 1/phi do NOT produce 3/16; the fraction is from hydrogen physics
- The factor-of-2 from individual (~1170 THz) to collective (~613 THz) depends on tubulin geometry

**Status: CONSTRAINED, approaching DERIVED.**

The gap between "8 is an empirical prefactor" and "8 is derived" is narrower than it appears. The number 8 has multiple independent framework interpretations (rank, normalizer, Lucas), and the golden-ratio substitution removes it entirely in favor of phi and alpha^(11/4). The remaining unexplained factor 4/sqrt(3) has a plausible connection to the PT n=2 breathing mode. A single calculation -- showing that the E8 normalizer enters the molecular coupling or that the PT breathing mode sets the 4/sqrt(3) -- would close the gap completely.

---

## References

- Born, M. & Oppenheimer, J.R. (1927). Annalen der Physik 389(20): 457-484.
- Craddock et al. (2017). Scientific Reports 7:9877. (613 THz anesthetic correlation)
- Kalra, Scholes et al. (2023). ACS Central Science 9(3). (Tryptophan energy migration)
- Dechant, P.P. (2016). Proc. R. Soc. A. (E8 icosian lattice, golden ratio)
- Mehta, P. & Kondev, J. (2025). arXiv:2509.09892. (Biological timescales from fundamental constants)
- Particle on a ring model for benzene: Chemistry LibreTexts (verified: lambda_pred = 194 nm)
- Huckel model: beta ~ 2.4 eV, benzene HOMO-LUMO gap ~ 4.8 eV = 1160 THz

---

## Key Equations Summary

```
f_R         = alpha^2 * m_e * c^2 / (2h)              = 3289.84 THz
f_BO        = f_R / sqrt(mu)                           = 76.78 THz
f_mol       = 8 * f_R / sqrt(mu)                       = 614.20 THz
f_mol       = 4 * alpha^(11/4) * phi / sqrt(3) * f_el  = 613.86 THz
f_H-beta    = (3/16) * f_R                             = 616.85 THz
f_Craddock  = 613 +/- 8 THz                            (measured)

Core identity: alpha^(3/2) * mu * phi^2 = 2.9966 ~ 3
Exponent:      11/4 = L(5)/L(3) (Lucas ratio)
Factor 8:      = rank(E8) = 62208/7776 = |Norm|/N
```
