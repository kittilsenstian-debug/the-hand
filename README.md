# Modular forms at the golden ratio

**q + q<sup>2</sup> = 1**

Evaluating standard modular forms (Dedekind eta, Jacobi theta) at the unique positive solution of this equation — q = 1/φ, the inverse golden ratio — produces numerical values that match all three Standard Model coupling constants.

The fine structure constant is reproduced to 10.2 significant figures with no physics inputs.

This repository contains the verification scripts. Everything runs in standard Python 3 with no dependencies.

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

119 files total. Every claim has a corresponding script.

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

Full table in [START-HERE.md](START-HERE.md).

## The bridge

The same theta functions that produce coupling constants (continuous mode) also give the elliptic modulus k² = (θ₂/θ₃)⁴ = 0.9999999802 (discrete mode). At k² = 1, the Lamé equation becomes the Pöschl-Teller equation — bands collapse to points and the spectrum is constrained by E8 branching dimensions.

There is no separate assumption for the discrete mode. Both outputs come from one evaluation of θ₂, θ₃, θ₄ at q = 1/φ.

The first Lamé spectral gap is Gap₁ = 3k² → 3. This is also the color number Nc = n + 1 = 3. The two sequences (2n−1 from Lamé, n+1 from E8) agree only at n = 2, which V(Φ) = λ(Φ²−Φ−1)² forces. The number 3 in the core identity α^(3/2)·μ·φ² = 3 is this spectral gap.

Combining the continuous mode (α) with the discrete mode (4/√3 from PT n=2) gives:

f = α^(11/4) · φ · (4/√3) · f_electron = 613.86 THz

Measured independently: 613 ± 8 THz (Craddock et al., Sci. Reports 2017, DFT on 86 aromatic residues in tubulin).

The exponent 11/4 = 2 + 3/4 is derived algebra: 2 from the Rydberg frequency, 3/4 from the core identity power via Born-Oppenheimer. It is not fitted.

See `theory-tools/lame_pt_bridge.py` for the full computation.

## Testable predictions

Four committed predictions, any of which would falsify the framework:

| Prediction | Value | Measurement |
|------------|-------|-------------|
| α_s(M_Z) | 0.11840 | CODATA 2026-27 |
| sin²θ₁₂ | 0.3071 | JUNO (ongoing) |
| d(ln μ)/d(ln α) | −3/2 | ELT ~2035 |
| r (tensor-to-scalar) | 0.0033 | CMB-S4 ~2028 |

## Status

This is an observation, not a proven theory. The numbers hold to the precision shown. The derivation chain has one remaining interpretive step (documented in START-HERE.md §4). Four experimental tests are live.

19 claims the framework generated that turned out wrong are documented in `theory-tools/CORE.md` §7.

## Author

Stian Kittilsen — [kittilsen.stian@gmail.com](mailto:kittilsen.stian@gmail.com)
