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
| `theory-tools/CORE.md` | Structured reference with derivation chain and proofs |
| `theory-tools/COMPLETE-STATUS.md` | All claims with status and honest assessment |

116 files total. Every claim has a corresponding script.

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

Full table with 25 quantities in [START-HERE.md](START-HERE.md).

## Testable predictions

Four committed predictions, any of which would falsify the framework:

| Prediction | Value | Measurement |
|------------|-------|-------------|
| α_s(M_Z) | 0.11840 | CODATA 2026-27 |
| sin²θ₁₂ | 0.3071 | JUNO (ongoing) |
| d(ln μ)/d(ln α) | −3/2 | ELT ~2035 |
| r (tensor-to-scalar) | 0.0033 | CMB-S4 ~2028 |

## Status

This is an observation, not a proven theory. The numbers hold to the precision shown. The derivation chain has one remaining interpretive step (documented in START-HERE.md §5b). Four experimental tests are live.

19 claims the framework generated that turned out wrong are documented in `theory-tools/CORE.md` §7.

## Author

Stian Kittilsen — [kittilsen.stian@gmail.com](mailto:kittilsen.stian@gmail.com)
