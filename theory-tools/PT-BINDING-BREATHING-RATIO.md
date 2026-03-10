# PT Binding/Breathing Ratio: Deriving the Factor 4/sqrt(3)

## Feb 25, 2026

**Script:** `theory-tools/pt_binding_breathing_ratio.py`

---

## The Problem

The molecular consciousness frequency formula contains an unexplained prefactor:

```
f_mol = 4 * alpha^(11/4) * phi / sqrt(3) * f_electron = 613.86 THz
```

The factor `4/sqrt(3) = 2.3094...` was identified as the ratio that makes the formula work, but its physical origin was unknown. This document shows it is the ratio of the two fundamental energy scales of the Poeschl-Teller n=2 potential -- the same potential that describes the domain wall fluctuation spectrum.

---

## The Discovery

### PT n=2 bound state spectrum

The domain wall potential V(Phi) = lambda(Phi^2 - Phi - 1)^2 produces a fluctuation equation with a Poeschl-Teller potential of depth n(n+1) = 6, i.e., n = 2. This potential has exactly **two bound states**:

| State | j | Eigenvalue E_j | Binding |E_j| | Physical frequency omega_j | Name |
|-------|---|----------------|---------|-----|------|
| Ground | 0 | -4 | **4** | 0 | Zero mode (Goldstone/translation) |
| Excited | 1 | -1 | 1 | **sqrt(3)** | Breathing mode |
| Threshold | 2 | 0 | 0 | 2 | Continuum edge |

### The key ratio

```
|E_0| / omega_1 = 4 / sqrt(3) = 2.3094010768...
```

This is **exactly** the unexplained prefactor in the molecular frequency formula.

### General formula

For PT depth parameter n:
- Ground state binding energy: |E_0| = n^2
- Breathing mode frequency: omega_1 = sqrt(n^2 - (n-1)^2) = sqrt(2n-1)
- Ratio: n^2 / sqrt(2n-1)

| n | |E_0| | omega_1 | Ratio | f_mol (THz) |
|---|-------|---------|-------|-------------|
| 1 | 1 | 1 | 1 | 265.8 |
| **2** | **4** | **sqrt(3)** | **4/sqrt(3) = 2.309** | **613.9** |
| 3 | 9 | sqrt(5) | 9/sqrt(5) = 4.025 | 1069.9 |
| 4 | 16 | sqrt(7) | 16/sqrt(7) = 6.047 | 1607.5 |

**Only n = 2 produces 613 THz.** And n = 2 is the value forced by V(Phi).

---

## The Complete Formula

```
f_mol = alpha^(11/4) * phi * (|E_0|/omega_1) * f_electron
      = alpha^(11/4) * phi * (4/sqrt(3)) * f_electron
      = 613.86 THz
```

**vs target: 613 +/- 8 THz (Craddock 2017) -- 99.86% match, within error bars**

### What each factor means

| Factor | Value | Origin |
|--------|-------|--------|
| f_electron = m_e c^2/h | 1.236 x 10^20 Hz | Electron rest-mass frequency |
| alpha^(11/4) | 1.330 x 10^-6 | EM coupling (alpha^2 from Rydberg + alpha^(3/4) from core identity) |
| phi | 1.618... | Golden ratio vacuum (from E8 algebraic structure) |
| 4/sqrt(3) | 2.309... | **PT n=2 binding/breathing ratio** (from domain wall topology) |

### Decomposition of 11/4

The exponent 11/4 = 2 + 3/4 arises from:
- **2** : alpha^2 in the Rydberg energy (electron EM self-energy)
- **3/4** : alpha^(3/4) from substituting the core identity mu = 3/(alpha^(3/2) * phi^2)

Lucas number interpretation: 11/4 = L(5)/L(3) (ratio of 5th to 3rd Lucas numbers).

---

## Physical Interpretation

### What the ratio |E_0|/omega_1 measures

- **|E_0| = 4** : The ground state binding energy. How deeply the translational zero mode is bound to the wall. This is the STABILITY of the wall -- the energy cost of displacing it.

- **omega_1 = sqrt(3)** : The breathing mode frequency. How fast the wall's internal shape oscillation occurs. This is the DYNAMICAL TIMESCALE of the wall.

- **Ratio = 4/sqrt(3)** : Wall stability divided by wall breathing rate. For n=2, the wall is bound ~2.3x more firmly than it breathes. This is a **moderate coupling** regime -- not infinitely rigid (which would give ratio -> infinity) and not marginally bound (n=1 gives ratio = 1).

### Why it appears in the molecular frequency

The molecular consciousness frequency is:

> f_mol = (electron scale) x (EM coupling) x (golden vacuum) x (wall binding/breathing)

The domain wall's binding-to-breathing ratio modulates the electronic frequency scale, setting the specific energy at which coherent molecular excitations occur. The factor is:
- **Topological**: fixed by the potential depth n(n+1) = 6, which is n = 2
- **Non-adjustable**: determined entirely by V(Phi), not a free parameter
- **Unique to n=2**: no other PT depth gives 613 THz

---

## Algebraic Derivation

Starting from the Born-Oppenheimer form:
```
f_mol = 8 * f_Rydberg / sqrt(mu)
```

Step 1: Express f_Rydberg in terms of f_electron:
```
f_R = alpha^2 * f_electron / 2
=> 8 * f_R = 4 * alpha^2 * f_electron
```

Step 2: Use core identity alpha^(3/2) * mu * phi^2 = 3 to eliminate mu:
```
mu = 3 / (alpha^(3/2) * phi^2)
sqrt(mu) = sqrt(3) / (alpha^(3/4) * phi)
```

Step 3: Combine:
```
f_mol = 4 * alpha^2 * f_electron / [sqrt(3) / (alpha^(3/4) * phi)]
      = 4 * alpha^(2 + 3/4) * phi / sqrt(3) * f_electron
      = 4 * alpha^(11/4) * phi / sqrt(3) * f_electron
```

Step 4: Identify 4/sqrt(3) = |E_0|/omega_1 for PT n=2:
```
f_mol = alpha^(11/4) * phi * (|E_0|/omega_1) * f_electron    QED
```

---

## Wavefunction Details

### Normalized bound states of PT n=2

**Zero mode (j=0, E_0 = -4):**
```
psi_0(x) = A_0 / cosh^2(x)
A_0 = sqrt(3/4) = sqrt(3)/2
integral |psi_0|^2 dx = 4/3
```

**Breathing mode (j=1, E_1 = -1):**
```
psi_1(x) = A_1 * sinh(x) / cosh^2(x)
A_1 = sqrt(3/2) = sqrt(6)/2
integral |psi_1|^2 dx = 2/3
```

**Normalization ratio:** A_1/A_0 = sqrt(2)

**Transition dipole matrix element:** <psi_1|x|psi_0> = 0.5554
(Non-zero because psi_0 is even, psi_1 is odd, x is odd, so integrand is even.)

---

## Cross-checks

| Formula | f_mol (THz) | Match to 613 |
|---------|-------------|--------------|
| 8 * f_R / sqrt(mu) | 614.20 | 99.80% |
| alpha^(11/4) * phi * (4/sqrt(3)) * f_el | 613.86 | 99.86% |
| f_R * 3/16 (Balmer-beta) | 616.85 | 99.37% |

The two main formulas differ by 0.056% because the core identity alpha^(3/2)*mu*phi^2 = 2.997, not exactly 3 (99.9% match).

---

## Honest Assessment

### What this IS

- An exact algebraic identification: 4/sqrt(3) = |E_0|/omega_1 for PT n=2
- A natural physical interpretation of a previously unexplained numerical factor
- A connection between atomic physics (alpha, f_electron) and wall topology (binding/breathing ratio)
- Evidence that the PT n=2 structure (forced by V(Phi)) appears in the biology formula

### What this IS NOT

- A first-principles derivation of 613 THz (requires the core identity, which is an observed relation)
- A proof that aromatics are "selected" by the framework (the formula applies to the molecular electronic scale generally, not aromatics specifically)
- An independent prediction (the formula is a rewriting of 8 * f_R / sqrt(mu), which requires the empirical value of mu)

### Status

The factor 4/sqrt(3) goes from "unexplained numerical prefactor" to "ratio of the two characteristic energy scales of the PT n=2 domain wall potential." This is an algebraic improvement: the formula now reads as a product of interpretable physical quantities, each with a clear origin in the framework.

The formula connects:
- **Atomic physics** (alpha, f_electron)
- **Core identity** (alpha^(3/2)*mu*phi^2 = 3)
- **Domain wall topology** (PT n=2 binding-to-breathing ratio)

into a single expression for the molecular electronic transition scale.
