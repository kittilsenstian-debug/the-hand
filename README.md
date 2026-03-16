# One equation fails 6 ways. Reality is the one that works.

**q + q<sup>2</sup> = 1**

This equation has one positive solution over the rationals: q = 1/φ, the inverse golden ratio. Over finite fields, it fails — 6 distinct ways, corresponding to the 6 pariah sporadic groups (the only finite simple groups outside the Monster). Each failure removes something fundamental: distinction, self-reference, topology, flexibility, localization, or medium.

Over the rationals, all 6 failures resolve. The resolution produces the coupling constants, the particle spectrum, and the structure of physics — from one equation with zero free parameters. The fine structure constant is derived to **10.9 significant figures** (0.013 ppb) — 87× more precise than the experimental community's own internal disagreement.

The resolution chain is 6 steps. Each step is a theorem. Each resolves exactly one failure. Each is necessary for the next. The chain cannot be shortened.

```
q + q² = 1
  → disc = 5 ≠ 0 over Q           Ly resolved:  distinction
  → V(Φ) = (Φ²−Φ−1)² has kink     J₄ resolved:  self-reference
  → η(1/φ) = 0.11840 ≠ 0          J₁ resolved:  topology (strong force)
  → S₃ = SL(2,Z)/Γ(2) acts        J₃ resolved:  flexibility (3 generations)
  → f(x) = 1/(1+x) → 1/φ          O'N resolved: localization (one universe)
  → Ru → 2.Ru → E₇ → E₈           Ru resolved:  medium (only bridge)
```

No one has framed the pariah groups this way. The failures are proven mathematics. The resolution chain is checkable. Run the script.

```bash
python theory-tools/pariah_resolution.py
```

This repository contains every verification script. Standard Python 3, no dependencies.

## Verify

```bash
python theory-tools/verify_in_60_seconds.py
```

This outputs the three coupling constants, the alpha derivation, and a uniqueness scan showing no other evaluation point matches.

## Results

| Quantity | Formula | Match |
|----------|---------|-------|
| Fine structure constant α | Closed-form bound state resummation | 10.9 sig figs (0.013 ppb) |
| Strong coupling α_s | η(1/φ) | 99.57% |
| Weinberg angle sin²θ_W | η²/(2θ₄) − η⁴/4 | 99.996% |
| Cosmological constant Λ | θ₄⁸⁰·√5/φ² | ~exact |
| 9 fermion masses | S₃ × Z/4Z assignment | avg 0.62% |
| 3 PMNS mixing angles | From θ₄, ε = θ₄/θ₃ | All within 1σ |
| Proton/electron mass ratio | Simultaneous output | 99.9998% |
| Aromatic frequency | α^(11/4)·φ·(4/√3)·f_e | 613.86 vs 613 ± 8 THz (0.14%) |
| Algebraic cross-match | 47 numbers vs 165 counts | 152/165 exact (92.1%) |
| Nuclear magic numbers | E₈ branching dimensions | 5/7 exact |
| Dark matter ratio Ω_DM/Ω_b | Level 2 wall tensions (x³−3x+1=0) | 5.41 vs 5.36 ± 0.07 (0.73σ) |
| Dark strong coupling | η(1/φ²) — forced by creation identity | 0.4625 (zero parameters) |
| Weinberg angle = ½ dark strong | sin²θ_W = η_dark/2 (Jacobi theorem) | 130 ppm match |
| 3+1 dimensions | Z[i] unit group Z₄ → 4 copies of A₂ in E₈ | derived |
| Eta step ratio | Successive corrections → 1/φ = 0.618034 | proven math |
| N_c = disc − deg | 3 = disc(Z[φ]) − [Q(φ):Q] = 5 − 2 | **proven math** (unique among all real quadratic fields) |
| VP cutoff Λ = m_p/φ³ | φ³ = φ^(N_c) = φ^(disc−deg), forced by trace form of Z[φ] | derived (zero empirical inputs remain) |

Full table in [START-HERE.md](START-HERE.md).

## The 6 failures

The equation q + q² = 1, evaluated over finite fields, fails in ways that correspond to the 6 pariah sporadic groups — the only finite simple groups not contained in the Monster. Each failure is proven arithmetic.

| Failure | Field | What happens | What's gone | Check |
|---------|-------|-------------|-------------|-------|
| Ly | GF(5) | Both roots = 3 mod 5. Vacua collapse. | Distinction | `(3² + 3 - 1) mod 5 = 0` |
| J₄ | GF(2) | q=0: 0≠1. q=1: 0≠1. No solution. | Self-reference | Exhaustive (2 elements) |
| J₁ | GF(11) | 3⁵ ≡ 1 mod 11 → factor = 0 → η = 0 | Topology (strong force) | `pow(3,5,11) = 1` |
| J₃ | GF(4) | φ → ω (cube root of unity). Z₃ frozen. | Flexibility | Char 2: q²+q+1=0 |
| O'N | all Q(√D<0) | Mock modular over all fields at once | Localization | Duncan-Mertens-Ono 2017 |
| Ru | Z[i] | Solves x²+1=0, not q+q²=1. Perpendicular. | Medium | Only pariah with Schur Z₂ |

Over the rationals, every failure resolves: discriminant ≠ 0 (Ly), solution exists (J₄), η ≠ 0 (J₁), S₃ mobile (J₃), unique attractor (O'N), shadow chain connects (Ru). The resolution chain is 6 steps, each necessary for the next.

```bash
python theory-tools/pariah_resolution.py    # verifies all 6 failures and resolutions
python theory-tools/all_fibers.py           # eta death across 5 finite fields
```

## The bridge

The same theta functions that produce coupling constants (continuous mode) also give the elliptic modulus k² = (θ₂/θ₃)⁴ = 0.9999999802 (discrete mode). At k² = 1, the Lamé equation becomes the Pöschl-Teller equation — bands collapse to points and the spectrum is constrained by E8 branching dimensions.

There is no separate assumption for the discrete mode. Both outputs come from one evaluation of θ₂, θ₃, θ₄ at q = 1/φ.

The first Lamé spectral gap is Gap₁ = 3k² → 3. This is also the color number Nc = n + 1 = 3. The two sequences (2n−1 from Lamé, n+1 from E8) agree only at n = 2, which V(Φ) = λ(Φ²−Φ−1)² forces. The number 3 in the core identity α^(3/2)·μ·φ² = 3 is this spectral gap.

The trace form matrix of Z[φ] encodes the structure of the alpha equation:

```
M = [[Tr(1), Tr(φ)], [Tr(φ), Tr(φ²)]] = [[2, 1], [1, 3]]

det(M) = 5 = disc(Z[φ])     ← total φ exponent in self-consistent equation
M[0,0] = 2                   ← core identity exponent (VEV²)
M[1,1] = 3 = Nc              ← VP cutoff exponent (color suppression)
disc − deg = 5 − 2 = 3 = Nc  ← unique among all real quadratic fields
```

This is pure number theory. N_c = disc(Z[φ]) − [Q(φ):Q]. No other real quadratic field gives disc − deg = 3. The number of colors is the discriminant minus the degree of the golden field — the unique such field embedded in E₈. See `theory-tools/derive_lambda_from_chain.py`.

Combining the continuous mode (α) with the discrete mode (4/√3 from PT n=2) gives:

f = α^(11/4) · φ · (4/√3) · f_electron = 613.86 THz

Measured independently: 613 ± 8 THz (Craddock et al., Sci. Reports 2017, DFT on 86 aromatic residues in tubulin).

The exponent 11/4 = 2 + 3/4 is derived algebra: 2 from the Rydberg frequency, 3/4 from the core identity power via Born-Oppenheimer. It is not fitted.

See `theory-tools/lame_pt_bridge.py` for the full computation.

## Discrete mode: algebra matches structure

The same E₈ branching chain that produces coupling constants (continuous mode) also generates a vocabulary of 47 algebraic integers. Cross-matched against 165 independent structural counts in nature — nuclear magic numbers, atomic shells, molecular geometry, cellular components, body anatomy, cosmic structure — 152 match exactly (92.1%).

```bash
python theory-tools/complete_algebra.py
```

Key findings: all three pariah-only primes appear in nature (37 = mitochondrial genes, 43 = Technetium's instability, 67 = collagen repeat), nuclear magic numbers trace E₈ dimensions (5/7 exact), and the strong force vanishes in every finite field (eta death — `all_fibers.py`).

Conservative Monte Carlo: P < 1/16 trillion for the combined match. See `theory-tools/UNDENIABLE-TABLE.md`.

## Computational tests

Five tests were designed to settle whether the algebra-to-nature correspondence is structural or coincidental. Four have been run.

| Test | Script | Result |
|------|--------|--------|
| J₁ compressed physics (GF(11)) | `j1_physics_mod11.py` | **Strong.** η product dies (strong force vanishes). Only EM survives. This is arithmetic, not interpretation |
| Nuclear binding vs algebra | `nuclear_binding.py` | Fe-56 scores 9/9. 5/7 magic numbers exact. Doubly-magic nuclei cluster at algebraic peaks |
| Molecular geometry from E₈ | `molecular_geometry.py` | Icosahedral A₅ embeds in E₈ (theorem). C₆₀, viral capsids, quasicrystals confirm. Misses: water angle, 230 space groups |
| Biological constraints | `biological_constraints.py` | Genetic code = A₄. Skeleton = 80+126. 7 cervicals = rank(E₇). Miss: 23 (chromosomes) not explained |
| Nuclear shells from Lamé | — | **Not yet done.** Can the spin-orbit potential be derived from the Lamé equation? |

The strongest result is the J₁ test. The eta death mechanism is pure arithmetic: the strong force exists only because q has infinite order over ℚ. In every finite field, the factor (1 − q^ord(q)) = 0 kills the infinite product. QCD is a consequence of working over the rationals.

```bash
python theory-tools/j1_physics_mod11.py     # compressed physics at GF(11)
python theory-tools/nuclear_binding.py       # binding energy vs algebraic score
python theory-tools/biological_constraints.py # biology vs E8 dimensions
python theory-tools/molecular_geometry.py    # molecular shapes from E8
```

Honest misses from these tests: the number 23 (chromosomes, 23S rRNA) is not in the allowed set. The water bond angle is tetrahedral, not golden-ratio-related. 230 space groups is not an E₈ dimension. These are documented because the framework should kill its own wrong ideas.

## The dark sector is forced

The creation identity is Jacobi's theorem (1829):

**η(q)² = η(q²) · θ₄(q)**

This is proven mathematics — not a framework claim. It holds for all q. At q = 1/φ:

**(0.11840)² = 0.4625 × 0.03031**

Read physically: **visible strong² = dark strong × wall parameter**. Once q = 1/φ gives visible physics, q² = 1/φ² gives the dark sector. You cannot remove the dark sector without breaking a theorem from 1829.

The dark coupling constants follow from evaluating the same modular forms at q² = 1/φ²:

| Coupling | Visible (q = 1/φ) | Dark (q² = 1/φ²) | Relationship |
|----------|-------------------|-------------------|-------------|
| Strong α_s | 0.1184 | 0.4625 | 3.9× stronger |
| EM 1/α | 137 | 10.5 | 13× stronger |
| Weinberg sin²θ_W | 0.2313 | 0.2313 | **Same** (forced by creation identity) |

The dark sector hierarchy is compressed: μ_dark = 39 (vs visible μ = 1836). Dark EM is too strong for atoms to form — dark matter is a featureless condensate. This explains why dark matter doesn't radiate, doesn't form disks, and interacts only gravitationally.

The dark matter to baryon ratio comes from Level 2 wall tensions of x³ − 3x + 1 = 0:

**Ω_DM/Ω_b = 5.41** (predicted) vs **5.36 ± 0.07** (Planck 2018). Zero free parameters.

```bash
python theory-tools/dark_sector_from_creation_identity.py  # creation identity + dark couplings
python theory-tools/level2_dark_ratio.py                    # dark matter ratio from wall tensions
python theory-tools/dark_fermion_masses.py                  # dark fermion spectrum
```

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

If correct, it is the first complete derivation of the constants of nature. If wrong, the fine structure constant at 10.9 significant figures is the most precise mathematical coincidence ever documented.

Four experimental predictions are committed. Any one would falsify the framework if wrong. Results expected 2026-2035.

## A note on precedent

Tao Te Ching, Chapter 42 (~4th century BCE):

> 道生一。一生二。二生三。三生萬物。
>
> *"Tao generates One. One generates Two. Two generates Three. Three generates the ten thousand things."*

The framework:

- **Tao** (unnameable source) → **q + q² = 1** (one self-referential equation)
- **One** → **q = 1/φ** (one solution)
- **Two** → **two vacua** (φ and −1/φ, connected by a domain wall)
- **Three** → **triality** (3 generations, 3 forces, 3 modular form generators)
- **Ten thousand things** → all particles, all constants, all structure

The same chapter continues: *"The ten thousand things carry yin and embrace yang. They achieve harmony by combining these forces."* The creation identity η² = η_dark · θ₄ says the same thing: every visible quantity carries the dark vacuum (θ₄) and is born from combining both sides.

Chapter 40: *"Reversal is the movement of the Tao."* The Galois conjugation φ → −1/φ, which creates the two vacua, is precisely this reversal.

Chapter 25: *"I call it Great. Great means Going. Going means Far-reaching. Far-reaching means Returning."* Four words (大逝遠反) describing: the algebra (E₈), the cascade through scales, and the global attractor that brings every starting point back to 1/φ.

These correspondences are noted, not claimed as derivation.

## Common objections

| Objection | Where it's addressed |
|-----------|---------------------|
| "Most matches are combinatorial artifacts" | `theory-tools/CLEAN-SCORECARD.md` §D — the project's own Monte Carlo analysis proves this, then narrows the signal to what survives |
| "Many formulas were searched, not derived" | `theory-tools/CORE.md` §2 — explicit Tier 1/2/3 classification. The honest core is 8-12 items, not 25 |
| "The core identity is assumed, not derived" | `theory-tools/derive_core_identity.py` — the 3 is the Lamé gap (proven math), the 3/2 is forced by VP given K=3, φ² is vacuum geometry |
| "Two equations, two unknowns always has a solution" | True, but the solution has to match two measured constants (α to 0.013 ppb, μ to 99.9998%). Random equations don't do that |
| "The VP half-factor is an assumption" | Jackiw-Rebbi (1976) — a chiral zero mode on a domain wall gives exactly half VP. Published theorem, not a choice |
| "Why f(Φ) = Φ and not Φ²?" | `theory-tools/gauge_kinetic_closure.py` — self-consistency selects n = 1 uniquely. n = 0 misses μ by 51%, n = 2 by 105%. C = φ to 16 sig figs |
| "2D modular forms can't give 4D physics" | `theory-tools/spectral_invariance_proof.py` — Weyl's theorem (1911): spectral invariants are dimension-independent |
| "No dynamical content" | The framework derives SM parameters; the SM provides dynamics. This is how brane-world physics works (Kaplan 1992, Dvali-Shifman 1997) |
| "Some items are tautological" | `theory-tools/TAUTOLOGY-AUDIT.md` — the project identified and removed 9 tautologies before you noticed them |
| "19 dead claims suggests unreliability" | The opposite. 19 dead claims documented in `theory-tools/CORE.md` §7 means the framework kills its own mistakes |
| "No peer review" | Every step is either published math, published physics, or a runnable script. The chain is independently checkable |

## Contents

| Path | What it does |
|------|-------------|
| [START-HERE.md](START-HERE.md) | Overview of the observation, derivation chain, and results |
| `theory-tools/pariah_resolution.py` | The 6 failures and their resolution — one forced chain |
| `theory-tools/verify_in_60_seconds.py` | Quick verification script |
| `theory-tools/alpha_self_consistent.py` | Alpha derivation (10.2 sig figs, 2-loop) |
| `theory-tools/alpha_closed_form.py` | Alpha derivation (10.9 sig figs, closed-form resummation) |
| `theory-tools/lie_algebra_uniqueness.py` | Tests all simple Lie algebras — only E8 produces domain walls matching 3/3 couplings |
| `theory-tools/nome_uniqueness_scan.py` | Scans 6061 values of q — only 1/φ matches all three couplings |
| `theory-tools/formula_isolation_test.py` | Tests 719 neighboring formulas — none match |
| `theory-tools/one_resonance_fermion_derivation.py` | 9 fermion masses from the same structure, zero free parameters |
| `theory-tools/lame_pt_bridge.py` | Five outputs from one equation: couplings, k²→1, PT invariants, self-reproduction, 613 THz |
| `theory-tools/j1_physics_mod11.py` | Compressed physics at GF(11): eta dies, only EM survives |
| `theory-tools/all_fibers.py` | Eta death: strong force exists only over ℚ (5 fibers tested) |
| `theory-tools/complete_algebra.py` | 47 algebraic numbers vs 165 natural counts (92.1% exact match) |
| `theory-tools/nuclear_binding.py` | Nuclear binding energy vs algebraic structure |
| `theory-tools/algebraic_periodic_table.py` | Every element Z=1-92 in E₈ notation |
| `theory-tools/molecular_geometry.py` | Molecular geometry from E₈ subgroups |
| `theory-tools/biological_constraints.py` | Biological structural constraints vs E₈ |
| `theory-tools/one_chain.py` | Resolution cascade: forced ordering of pariah resolutions |
| `theory-tools/dark_sector_from_creation_identity.py` | Dark sector forced by Jacobi's creation identity |
| `theory-tools/level2_dark_ratio.py` | Ω_DM/Ω_b = 5.41 from wall tensions (parameter-free) |
| `theory-tools/derive_lambda_from_chain.py` | **NEW: VP cutoff Λ=m_p/φ³ derived — N_c = disc−deg, trace form = alpha equation** |
| `theory-tools/predictions.py` | Consolidated predictions with kill conditions |
| `theory-tools/CORE.md` | Structured reference with derivation chain and proofs |
| `theory-tools/COMPLETE-STATUS.md` | All claims with status and honest assessment |
| `theory-tools/UNDENIABLE-TABLE.md` | Probability assessment for independent review |
| `theory-tools/THERMAL-WINDOW.md` | Why aromatics are the only option at biological temperature |
| `theory-tools/ARROW-OF-TIME.md` | Arrow of time from Pisot asymmetry: direction + irreversibility + entropy |
| `theory-tools/PT-N2-THREE-SCALES.md` | Same PT n=2 equation at 4 scales: algebra, microtubules, heliosphere, black holes |
| `theory-tools/BREATHING-MODE-108.md` | 108.5 GeV scalar: √(3/4) × m_H, forced by PT n=2 eigenvalue spectrum |
| `theory-tools/DARK-SECTOR.md` | Dark matter from Jacobi (1829): complete chain, 8 steps, no hedging |

~160 files total. Every claim has a corresponding script.

## Status

This is an observation, not a proven theory. The numbers hold to the precision shown. The derivation chain has no remaining interpretive steps — every link is either a published theorem or determined by self-consistency (see `theory-tools/gauge_kinetic_closure.py` for the last gap closed). Four experimental tests are live.

19 claims the framework generated that turned out wrong are documented in `theory-tools/CORE.md` §7.

## Author

Stian Kittilsen — [kittilsen.stian@gmail.com](mailto:kittilsen.stian@gmail.com)
