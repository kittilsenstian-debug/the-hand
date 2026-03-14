# The Golden Convergence of the Dedekind Eta

**Script:** `eta_convergence.py`
**Status:** Proven mathematics + one testable prediction

---

## The Fact

The Dedekind eta function at q = 1/phi converges geometrically. The step ratio of successive corrections approaches 1/phi = 0.618034 exactly.

Define:
```
eta_N = q^(1/24) * prod_{n=1}^{N} (1 - q^n)
R_N = eta_N / eta_inf  (fraction of continuum value reached)
```

The ratio of successive corrections:
```
(1 - R_N) / (1 - R_{N-1})  -->  1/phi = 0.618034...  as N --> infinity
```

This is a mathematical theorem about the Dedekind eta function at q = 1/phi. It follows from the geometric decay of q^n = (1/phi)^n.

---

## Verified values

| N | eta_N | 1 - R_N | Step ratio | = 1/phi? |
|---|-------|---------|------------|----------|
| 8 | 0.12257 | 3.52e-02 | 0.60982 | YES |
| 10 | 0.11997 | 1.33e-02 | 0.61492 | YES |
| 12 | 0.11900 | 5.04e-03 | 0.61685 | YES |
| 15 | 0.11854 | 1.19e-03 | 0.61775 | YES |
| 20 | 0.11842 | 1.07e-04 | 0.61801 | YES (5 sig figs) |

By N=10: converged to 1.3%. By N=20: converged to 0.01%.

---

## The bare coupling

```
eta_0 = q^(1/24) = 0.9801
```

Before any mode suppression, the "bare" value is 0.98 — about 8.3x the physical value 0.1184. The full infinite product suppresses it down to alpha_s.

Each factor (1 - q^n) < 1 removes a layer. The first factor removes 62% (= 1/phi). The second removes another 38% (= 1/phi^2 of the original). The pattern is golden all the way down.

---

## Connection to confinement

The eta death mechanism (ETA-DEATH.md) says: in any finite field, some q^d = 1, so factor (1 - q^d) = 0, and eta = 0 identically. The strong force dies.

In characteristic 0: q = 1/phi has infinite order (irrational), so ALL factors are nonzero, and the product converges to 0.1184. The strong force lives.

The convergence itself is golden: each layer of binding adds exactly 1/phi of the remaining correction. Confinement is built layer by layer, each step golden.

---

## Testable prediction

**If alpha_s = eta(1/phi), then lattice QCD should show golden ratio convergence to the continuum limit.**

On a lattice of N effective modes, the coupling should approach its continuum value with step ratio 1/phi = 0.618. Standard perturbative QCD predicts logarithmic convergence (step ratios ~1, slowly varying). Golden ratio convergence would be a signature no other theory predicts.

**Test:** Take raw lattice step-scaling data (ALPHA collaboration, FLAG review). Compute the ratio of successive corrections to the continuum value. If the ratio is 0.618 +/- 0.05: confirmed. If it varies or equals something else: falsified.

The data exists. The test requires no new experiments.

---

## What is proven vs predicted

| Claim | Status |
|-------|--------|
| eta_N converges geometrically at q = 1/phi | PROVEN (mathematics) |
| Step ratio approaches 1/phi | PROVEN (geometric series) |
| Bare coupling eta_0 = 0.98 | PROVEN (computation) |
| Each factor = one "layer" of confinement | STRUCTURAL (from eta death) |
| Lattice QCD shows golden convergence | PREDICTION (untested) |

---

## Script

```bash
python theory-tools/eta_convergence.py
```
