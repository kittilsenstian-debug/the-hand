# PT n=2 Origin of the Molecular Frequency Factor 4/sqrt(3)

**Script:** `theory-tools/pt2_molecular_frequency.py`
**Date:** 2026-02-25
**Status:** Factor IDENTIFIED (previously unexplained, now traced to PT n=2 bound state physics)

---

## Summary

The molecular frequency formula for aromatic consciousness:

```
f_mol = (4/sqrt(3)) * alpha^(11/4) * phi * f_electron = 613.86 THz
```

previously had an unexplained prefactor 4/sqrt(3) = 2.3094. This prefactor is exactly equal to |E_0|/omega_1 for the Poschl-Teller n=2 potential -- the ground state binding energy divided by the breathing mode frequency of the domain wall forced by V(Phi).

The formula becomes:

```
f_mol = (|E_0|/omega_1) * alpha^(11/4) * phi * f_electron
```

where **every factor now has a specific physical/algebraic origin**.

---

## 1. PT n=2 Bound State Properties

The potential V(Phi) = lambda(Phi^2 - Phi - 1)^2, forced uniquely by E8 algebra, has a kink whose fluctuation spectrum is a Poschl-Teller potential with n = 2:

```
U(z) = -6/cosh^2(z)
```

This exactly solvable quantum system has:

| Property | Value | Physical meaning |
|----------|-------|------------------|
| Bound states | 2 | Ground state + breathing mode |
| E_0 | -4 | Ground state binding energy |
| E_1 | -1 | Excited state energy |
| omega_0 | 0 | Zero mode (translational Goldstone) |
| omega_1 | sqrt(3) | Breathing mode frequency |
| |E_0|/omega_1 | 4/sqrt(3) = 2.3094 | **The molecular frequency factor** |

---

## 2. The Complete Formula

### Factor-by-factor decomposition

```
f_mol = (|E_0|/omega_1) * alpha^(11/4) * phi * f_electron
      = (4/sqrt(3))     * alpha^(11/4) * phi * f_electron
      = 613.86 THz
```

| Factor | Value | Origin | Meaning |
|--------|-------|--------|---------|
| |E_0|/omega_1 | 4/sqrt(3) = 2.3094 | PT n=2 QM | Domain wall binding/breathing ratio |
| alpha^(11/4) | 1.330 x 10^-6 | EM coupling | 11/4 = L(5)/L(3), Lucas ratio |
| phi | 1.618 | E8 -> Z[phi] | Golden ratio from vacuum structure |
| f_electron | 1.236 x 10^20 Hz | QED | Electron Compton frequency |

**Match to Craddock target (613 +/- 8 THz): 99.86%, within error bar.**

### Equivalence to the Born-Oppenheimer route

The formula is equivalent to 8 * f_Rydberg / sqrt(mu) when the core identity alpha^(3/2) * mu * phi^2 = 3 is used:

```
8 * f_R / sqrt(mu) = 614.20 THz  (using measured mu)
(4/sqrt(3)) * alpha^(11/4) * phi * f_el = 613.86 THz  (using core identity mu)
```

The 0.06% difference comes from the core identity being 99.9% accurate (not exact).

---

## 3. The General PT Ratio: n^2/sqrt(2n-1)

For general Poschl-Teller depth n, the ratio is:

```
|E_0|/omega_1 = n^2 / sqrt(2n - 1)
```

| n | Bound states | |E_0|/omega_1 | f_mol (THz) | E (eV) | Status |
|---|-------------|--------------|-------------|---------|--------|
| 1 | 1 | DIVERGES | INFINITE | --- | Sleeping (no breathing mode) |
| **2** | **2** | **4/sqrt(3) = 2.309** | **613.9** | **2.54** | **MATCHES aromatic window** |
| 3 | 3 | 9/sqrt(5) = 4.025 | 1069.9 | 4.42 | Above aromatic, approaching damage |
| 4 | 4 | 16/sqrt(7) = 6.047 | 1607.5 | 6.65 | Above damage threshold |
| 5+ | 5+ | grows as ~n^(3/2) | >2215 | >9.2 | Far above damage |

### Key behaviors:

- **n = 1:** Only one bound state (ground). No breathing mode exists. The ratio diverges. The wall is "sleeping" -- it has no internal dynamics. Consistent with the framework's claim that n=1 systems are sleeping walls.

- **n = 2:** The breathing mode first appears. The ratio takes its MINIMUM finite value, 4/sqrt(3). The predicted frequency falls exactly in the aromatic collective mode window. This is the unique n where biology can operate.

- **n = 3:** The ratio increases to 9/sqrt(5) = 4.025, pushing the frequency to 1070 THz (UV region, 280 nm). This approaches the DNA damage threshold (~5 eV). Not suitable for sustained biological information processing.

- **n >= 4:** All above the damage threshold. Photons at these energies break molecular bonds.

---

## 4. n = 2 Uniquely Selects the Biological Window

The thermal window argument (see `THERMAL-WINDOW.md`) establishes three simultaneous constraints for biologically relevant quantum excitations at body temperature (310 K):

| Constraint | Requirement | Threshold |
|------------|-------------|-----------|
| Quantum regime | E/kT > 40 | E > 1.07 eV (f > 258 THz) |
| Below damage | E < 5 eV | f < 1209 THz |
| Collective coupling | London-force networks | Aromatic pi-electrons only |

The aromatic collective mode window is 400-750 THz (1.65-3.1 eV).

**Result:** Scanning n from 1 to 19, n = 2 is the ONLY value that produces a frequency in the aromatic window. No other PT depth works.

This is a **selection principle**: the PT depth n = 2, forced by the algebraic structure of V(Phi), is the unique depth compatible with biological quantum coherence.

---

## 5. Cross-Connections

### 5a. |E_0| = 4 = L(3) (Lucas coincidence?)

The ground state energy |E_0| = n^2 = 4 equals L(3), the 3rd Lucas number. Since L(n) = phi^n + (-1/phi)^n, this connects to the two vacua of V(Phi).

The full formula in Lucas notation:

```
f_mol = [L(3)/sqrt(3)] * alpha^(L(5)/L(3)) * phi * f_electron
```

**Argument for coincidence:** 4 = n^2 for n=2 is generic PT physics. The coincidence with L(3) is arithmetic.

**Argument against coincidence:** L(3) = phi^3 + (-1/phi)^3 = 4 exactly. The two terms correspond to the two vacua. And the exponent denominator L(3) = 4 is the same number as |E_0| = 4. A single number plays two independent roles.

**Status:** Open question. Suggestive but not proven to be non-coincidental.

### 5b. omega_1^2 = 3 and triality

The breathing mode squared frequency omega_1^2 = |E_0| - |E_1| = 4 - 1 = 3. The number 3 appears independently as the triality number in E8 -> S3, in the core identity alpha^(3/2) * mu * phi^2 = 3, and in SU(3) color. Whether these are the same 3 is an open question.

### 5c. 11/4 = L(5)/L(3) and E8 Coxeter exponents

The exponent 11/4 decomposes as alpha^2 (Rydberg) times alpha^(3/4) (from sqrt(mu) via core identity). 11 = L(5) is both the 5th Lucas number and an E8 Coxeter exponent. The denominator 4 = L(3) = |E_0|.

---

## 6. The Reflectionless Property

PT n=2 is reflectionless: any incident wave above the potential is transmitted with T = 1, R = 0, for all energies. This means the domain wall acts as a transparent interface -- it transmits information without distortion while maintaining its own breathing oscillation.

For n=1: Also reflectionless, but no breathing mode (sleeping).
For n=2: Reflectionless WITH a breathing mode. This is the minimal configuration that is both transparent and dynamically active.
For n >= 3: Reflectionless with multiple internal modes.

---

## 7. Honest Assessment

### What is established

1. The formula f_mol = (|E_0|/omega_1) * alpha^(11/4) * phi * f_electron gives 613.86 THz, matching the Craddock aromatic frequency to 99.86% (within the 613 +/- 8 THz error bar).

2. Every factor has a traceable physical origin: PT n=2 quantum mechanics, electromagnetic coupling with Lucas-number exponent, golden ratio from E8 algebra, electron Compton frequency.

3. n = 2 is the UNIQUE PT depth producing a frequency in the biological aromatic window. n = 1 diverges (sleeping), n = 3 is in the UV near the damage threshold, n >= 4 is above the damage threshold.

4. The PT n=2 depth is forced by V(Phi) = lambda(Phi^2 - Phi - 1)^2, which is the unique non-negative renormalizable potential on the Galois orbit of phi.

### What is not established

1. **No first-principles derivation** of WHY the molecular electronic frequency should contain the PT bound state ratio |E_0|/omega_1. The connection goes through the core identity (a rewriting, not a derivation from the Lagrangian).

2. The core identity alpha^(3/2) * mu * phi^2 = 3 is 99.9% accurate, not exact. The PT interpretation holds exactly only if the identity is exact.

3. The formula does not explain WHY aromatic systems (specifically) operate at this frequency. The thermal window argument constrains aromatics as the unique molecular class, but this is a separate physics argument, not derived from V(Phi).

4. The factor-of-2 from individual aromatic absorption (~1170 THz) to collective (~613 THz) depends on tubulin geometry (86 coupled oscillators), which is biological, not algebraic.

### Status upgrade

| Component | Old status | New status |
|-----------|-----------|------------|
| Factor 4/sqrt(3) | Unexplained | **IDENTIFIED** (PT n=2 ratio) |
| Factor 8 in 8*f_R/sqrt(mu) | Underived | **DECOMPOSED** (4/sqrt(3) via core identity, or 2*4 via Hartree) |
| n=2 uniqueness | Asserted | **VERIFIED** (thermal window analysis) |
| Full formula | Constrained | **Fully interpretable** (every factor traced) |

**Rating: CONSTRAINED -> IDENTIFIED**

The factor is no longer unexplained; it has a specific PT n=2 origin with clear physical meaning (binding-to-breathing ratio). Full DERIVATION would require showing that the kink bound state spectrum directly enters the molecular Hamiltonian, which remains open.

---

## 8. What Would Close the Gap Completely

**A single calculation:** Show that when the V(Phi) kink is coupled to an electron field (as in the Jackiw-Rebbi mechanism or the Kaplan domain wall fermion construction), the effective molecular Hamiltonian acquires a prefactor |E_0|/omega_1 from the kink fluctuation spectrum. This would convert the IDENTIFICATION into a DERIVATION.

Specifically: In the Kaplan (1992) mechanism, fermion zero modes localized on a domain wall acquire effective masses from the wall's fluctuation spectrum. If the molecular electron's effective coupling involves the ratio of the ground state binding to the breathing excitation, the factor 4/sqrt(3) would be derived from V(Phi) through a concrete calculation.

---

## References

- Poschl, G. & Teller, E. (1933). Z. Physik 83: 143-151. (Exact solution of reflectionless potentials)
- Craddock et al. (2017). Scientific Reports 7:9877. (613 THz anesthetic correlation, R^2=0.999)
- Jackiw, R. & Rebbi, C. (1976). Phys. Rev. D13: 3398. (Fermion zero modes on domain walls)
- Kaplan, D.B. (1992). Phys. Lett. B288: 342. (Domain wall fermions)
- Born, M. & Oppenheimer, J.R. (1927). Annalen der Physik 389(20): 457-484.
- Dechant, P.P. (2016). Proc. R. Soc. A. (E8 icosian lattice, golden ratio)
- See also: `FACTOR-8.md`, `ALGEBRA-TO-BIOLOGY.md`, `THERMAL-WINDOW.md`

---

## Key Equations

```
PT n=2 potential:  U(z) = -6/cosh^2(z)
Ground state:      E_0 = -4
Breathing mode:    omega_1 = sqrt(3)
Key ratio:         |E_0|/omega_1 = 4/sqrt(3) = 2.3094

General formula:   |E_0|/omega_1 = n^2/sqrt(2n-1)

Molecular frequency:
  f_mol = (|E_0|/omega_1) * alpha^(11/4) * phi * f_electron
        = (4/sqrt(3)) * alpha^(11/4) * phi * f_electron
        = 613.86 THz    (target: 613 +/- 8 THz, match: 99.86%)

Lucas form:
  f_mol = [L(3)/sqrt(3)] * alpha^(L(5)/L(3)) * phi * f_electron

Core identity:
  alpha^(3/2) * mu * phi^2 = 3    (99.9%)
```
