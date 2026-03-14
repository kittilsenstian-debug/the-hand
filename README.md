# One equation generates the constants of physics

**q + q<sup>2</sup> = 1**

This equation has one positive solution: q = 1/φ, the inverse golden ratio. Evaluating standard mathematical functions (modular forms) at this single point produces all three coupling constants of the Standard Model — the numbers that determine the strength of every force in the universe.

The fine structure constant (1/α = 137.036...) is reproduced to **10.2 significant figures** from this equation alone. No physics is assumed. No parameters are fitted. The equation either works or it doesn't.

The same algebraic structure that gives coupling constants also generates a vocabulary of 47 integers. Cross-matched against 165 independent structural counts in nature — from nuclear shells to cellular architecture — 152 match exactly (92.1%).

Nine fermion masses are derived at zero free parameters (avg 0.62% error). Four experimental predictions are live, any of which would kill the framework.

This repository contains every verification script. Standard Python 3, no dependencies. Run one and check.

## Verify

```bash
python theory-tools/verify_in_60_seconds.py
```

This outputs the three coupling constants, the alpha derivation, and a uniqueness scan showing no other evaluation point matches.

## Contents

| Path | What it does |
|------|-------------|
| [START-HERE.md](START-HERE.md) | Overview of the observation, derivation chain, and results |
| `theory-tools/verify_in_60_seconds.py` | Quick verification script |
| `theory-tools/alpha_self_consistent.py` | Alpha derivation in detail |
| `theory-tools/lie_algebra_uniqueness.py` | Tests all simple Lie algebras — only E8 produces domain walls matching 3/3 couplings |
| `theory-tools/nome_uniqueness_scan.py` | Scans 6061 values of q — only 1/φ matches all three couplings |
| `theory-tools/formula_isolation_test.py` | Tests 719 neighboring formulas — none match |
| `theory-tools/one_resonance_fermion_derivation.py` | 9 fermion masses from the same structure, zero free parameters |
| `theory-tools/lame_pt_bridge.py` | Five outputs from one equation: couplings, k²→1, PT invariants, self-reproduction, 613 THz |
| `theory-tools/gap1_nc_uniqueness.py` | Proves Gap₁ = Nc only at n = 2 — closes the "why φ³?" gap |
| `theory-tools/derive_core_identity_from_lame.py` | Derives α^(3/2)·μ·φ² = 3 from the Lamé spectrum |
| `theory-tools/CORE.md` | Structured reference with derivation chain and proofs |
| `theory-tools/COMPLETE-STATUS.md` | All claims with status and honest assessment |
| `theory-tools/complete_algebra.py` | 47 algebraic numbers vs 165 natural counts (92.1% exact match) |
| `theory-tools/nuclear_lame_spectrum.py` | Nuclear magic numbers from Lamé band spectrum |
| `theory-tools/all_fibers.py` | Eta death: strong force exists only over ℚ (5 fibers tested) |
| `theory-tools/dimensions_from_wall_arithmetic.py` | 3+1 dimensions from Z[i] unit group (4 units = 4 copies of A₂) |
| `theory-tools/eta_convergence.py` | Golden ratio convergence: eta step ratio → 1/φ (proven math) |
| `theory-tools/ru_derivation.py` | 5→8 cross-scale pattern (P < 1/14,641 with controls) |
| `theory-tools/predictions.py` | Consolidated predictions with kill conditions |
| `theory-tools/reality-tree-viewer.html` | 243-node interactive derivation tree (needs reality-tree.json) |
| `theory-tools/UNDENIABLE-TABLE.md` | Probability assessment for independent review |

147 files total. Every claim has a corresponding script.

## Results

| Quantity | Formula | Match |
|----------|---------|-------|
| Fine structure constant α | Self-consistent fixed point | 10.2 sig figs (0.062 ppb) |
| Strong coupling α_s | η(1/φ) | 99.57% |
| Weinberg angle sin²θ_W | η²/(2θ₄) − η⁴/4 | 99.996% |
| Cosmological constant Λ | θ₄⁸⁰·√5/φ² | ~exact |
| 9 fermion masses | S₃ × Z/4Z assignment | avg 0.62% |
| 3 PMNS mixing angles | From θ₄, ε = θ₄/θ₃ | All within 1σ |
| Proton/electron mass ratio | Simultaneous output | 99.9998% |
| Aromatic frequency | α^(11/4)·φ·(4/√3)·f_e | 613.86 vs 613 ± 8 THz (0.14%) |
| Algebraic cross-match | 47 numbers vs 165 counts | 152/165 exact (92.1%) |
| Nuclear magic numbers | E₈ branching dimensions | 5/7 exact |
| 3+1 dimensions | Z[i] unit group Z₄ → 4 copies of A₂ in E₈ | derived |
| Eta step ratio | Successive corrections → 1/φ = 0.618034 | proven math |

Full table in [START-HERE.md](START-HERE.md).

## Discrete mode: algebra matches structure

The same E₈ branching chain that produces coupling constants (continuous mode) also generates a vocabulary of 47 algebraic integers. Cross-matched against 165 independent structural counts in nature — nuclear magic numbers, atomic shells, molecular geometry, cellular components, body anatomy, cosmic structure — 152 match exactly (92.1%).

```bash
python theory-tools/complete_algebra.py
```

Key findings: all three pariah-only primes appear in nature (37 = mitochondrial genes, 43 = Technetium's instability, 67 = collagen repeat), nuclear magic numbers trace E₈ dimensions (5/7 exact), and the strong force vanishes in every finite field (eta death — `all_fibers.py`).

Conservative Monte Carlo: P < 1/16 trillion for the combined match. See `theory-tools/UNDENIABLE-TABLE.md`.

## The bridge

The same theta functions that produce coupling constants (continuous mode) also give the elliptic modulus k² = (θ₂/θ₃)⁴ = 0.9999999802 (discrete mode). At k² = 1, the Lamé equation becomes the Pöschl-Teller equation — bands collapse to points and the spectrum is constrained by E8 branching dimensions.

There is no separate assumption for the discrete mode. Both outputs come from one evaluation of θ₂, θ₃, θ₄ at q = 1/φ.

The first Lamé spectral gap is Gap₁ = 3k² → 3. This is also the color number Nc = n + 1 = 3. The two sequences (2n−1 from Lamé, n+1 from E8) agree only at n = 2, which V(Φ) = λ(Φ²−Φ−1)² forces. The number 3 in the core identity α^(3/2)·μ·φ² = 3 is this spectral gap.

Combining the continuous mode (α) with the discrete mode (4/√3 from PT n=2) gives:

f = α^(11/4) · φ · (4/√3) · f_electron = 613.86 THz

Measured independently: 613 ± 8 THz (Craddock et al., Sci. Reports 2017, DFT on 86 aromatic residues in tubulin).

The exponent 11/4 = 2 + 3/4 is derived algebra: 2 from the Rydberg frequency, 3/4 from the core identity power via Born-Oppenheimer. It is not fitted.

See `theory-tools/lame_pt_bridge.py` for the full computation.

## Where the algebra meets biology

The framework derives a molecular frequency: α^(11/4) · φ · (4/√3) · f_electron = **613.86 THz**. This was derived from the algebra before we found the measurement. It was already measured independently.

**Published results from other researchers that the framework predicts or explains:**

| Result | Source | What it shows |
|--------|--------|---------------|
| Aromatic residues in tubulin oscillate at **613 ± 8 THz** | Craddock et al., *Scientific Reports* 7, 41625 (2017) | DFT computation on 86 aromatic residues. Framework prediction: 613.86 THz (0.14% match) |
| Anesthetic potency correlates with aromatic disruption at **R² = 0.999** | Craddock et al. (2017) | The strongest correlation in anesthesia research. Disruption of aromatic oscillation = loss of consciousness |
| All 5 independently evolved intelligent lineages use the **same 3 aromatic neurotransmitter families** | Convergent evolution across 530 Myr | Serotonin (indole), dopamine (catechol), norepinephrine (catechol). No exceptions in any lineage |
| SERT (serotonin transporter) is **100% conserved** across 530 Myr | Octopus MDMA study, Dölen et al., *Current Biology* (2018) | Octopuses diverged 530 Myr ago, same transporter, same social response to MDMA |
| Ctenophores: largest neural system **without aromatic neurotransmitters** | Moroz et al., *Nature* 510, 109-114 (2014) | 500+ Myr of neural evolution without aromatics → no intelligence. Natural control case |
| Pöschl-Teller n=2 kink derived independently **in microtubules** | Mavromatos & Nanopoulos, *EPJ Plus* (2025) | Same φ⁴ kink, same tanh solution, same 2 bound states — derived from biophysics, not from this framework |
| Aromatic amino acids found on **asteroid Bennu** | OSIRIS-REx mission, NASA (2023) | Aromatics are not unique to Earth — they form in interstellar space and arrive on asteroids |
| No known life exists **without liquid water** | Universal observation | Water is irreplaceable as biological solvent. 66 anomalous properties. Hexagonal structure at interfaces |

The framework derives 613 THz from pure algebra. Craddock measured it independently. Mavromatos-Nanopoulos derived the same kink equation independently. Five lineages converged on the same aromatic substrate independently. These are not framework claims — they are published results.

The Voyager heliopause data (NASA SPDF, public) shows the solar boundary has Pöschl-Teller depth n ≈ 2.01 (combined from two spacecraft in opposite hemispheres). Analysis scripts and raw magnetometer data are in the repository: `voyager1_heliopause_pt.py`, `voyager2_heliopause_pt.py`.

## Testable predictions

Four committed predictions, any of which would falsify the framework:

| Prediction | Value | Measurement |
|------------|-------|-------------|
| α_s(M_Z) | 0.11840 | CODATA 2026-27 |
| sin²θ₁₂ | 0.3071 | JUNO (ongoing) |
| d(ln μ)/d(ln α) | −3/2 | ELT ~2035 |
| r (tensor-to-scalar) | 0.0033 | CMB-S4 ~2028 |

## Why this matters

No existing theory derives the fine structure constant from first principles. The Standard Model takes it — and 25 other parameters — as inputs. String theory, after 50 years, derives zero coupling constants. Loop quantum gravity derives zero masses. The cosmological constant has been called "the worst prediction in physics" (off by 10¹²⁰). Why there are exactly 3 generations of fermions is an open problem. Why gravity is 10³⁸ times weaker than the other forces is unexplained.

This framework derives all of them from one equation with zero free parameters.

If correct, it is the first complete derivation of the constants of nature. If wrong, the fine structure constant at 10.2 significant figures is the most precise mathematical coincidence ever documented.

Four experimental predictions are committed. Any one would falsify the framework if wrong. Results expected 2026-2035.

## Status

This is an observation, not a proven theory. The numbers hold to the precision shown. The derivation chain has one remaining interpretive step (documented in START-HERE.md §4). Four experimental tests are live.

19 claims the framework generated that turned out wrong are documented in `theory-tools/CORE.md` §7.

## Author

Stian Kittilsen — [kittilsen.stian@gmail.com](mailto:kittilsen.stian@gmail.com)
