# One equation. All constants. Zero free parameters.

**q + q<sup>2</sup> = 1**

This repository contains verification scripts for a mathematical observation: evaluating standard modular forms at the unique positive solution of the above equation (q = 1/phi, the golden ratio inverse) produces all coupling constants of the Standard Model of physics.

The fine structure constant 1/alpha = 137.035999... is derived to **10.2 significant figures** with zero physics inputs.

## Run it yourself (60 seconds, no dependencies)

```bash
python theory-tools/verify_in_60_seconds.py
```

Requires only Python 3. No pip install. Outputs:
- Three coupling constants (strong, weak, electromagnetic) from modular forms
- Alpha to 10.2 significant figures via self-consistent fixed point
- Uniqueness scan: no other evaluation point q works (6000+ tested)

## What's here

| Path | Contents |
|------|----------|
| **[START-HERE.md](START-HERE.md)** | Full overview: 4 locks, the chain, 25 quantities, 54 mysteries |
| `theory-tools/verify_in_60_seconds.py` | The 60-second verification |
| `theory-tools/alpha_self_consistent.py` | Alpha derivation (detailed) |
| `theory-tools/lie_algebra_uniqueness.py` | Lock 1: only E8 works (test all algebras) |
| `theory-tools/nome_uniqueness_scan.py` | Lock 2: only q=1/phi works (6061 tested) |
| `theory-tools/formula_isolation_test.py` | Lock 3: core formula is isolated (0/719 neighbors) |
| `theory-tools/gap1_floquet_closure.py` | Tree-level derivation from Lame spectral theory |
| `theory-tools/one_resonance_fermion_derivation.py` | 9 fermion masses, zero parameters |
| `theory-tools/CORE.md` | Structured reference (chain, scorecard, proofs) |
| `theory-tools/COMPLETE-STATUS.md` | Single source of truth for all claims |
| `theory-tools/significant.md` | Alpha derivation walkthrough with inline script |

604 verification scripts total. Every claim is computationally testable.

## The strongest results

| Quantity | Formula | Accuracy |
|----------|---------|----------|
| Fine structure constant alpha | Self-consistent fixed point | **10.2 sig figs** (0.062 ppb) |
| Strong coupling alpha_s | eta(1/phi) | 99.57% (live test: CODATA 2026-27) |
| Weinberg angle sin2(theta_W) | eta^2/(2*theta4) - eta^4/4 | 99.996% (0.3 sigma) |
| Cosmological constant Lambda | theta4^80 * sqrt(5)/phi^2 | ~exact |
| 9 fermion masses | S3 x Z/4Z assignment | avg 0.62%, zero free params |
| 3 PMNS angles | theta4, epsilon = theta4/theta3 | all within 1 sigma |
| Born rule (p = 2) | Derived from PT n=2 | exact |
| Arrow of time | Pisot asymmetry | derived |
| Why 3 generations | S3 = SL(2,Z)/Gamma(2) | proven math |

Full table (25 quantities): [START-HERE.md](START-HERE.md)

## 4 live experimental tests

Any one could falsify the entire framework:

| Test | Prediction | Timeline |
|------|-----------|----------|
| alpha_s | 0.11840 exactly | CODATA 2026-27 |
| sin2(theta_12) | 0.3071 | JUNO (ongoing) |
| R = d(ln mu)/d(ln alpha) | -3/2 | ELT ~2035 |
| r (tensor/scalar ratio) | 0.0033 | CMB-S4 ~2028 |

## Ask an AI

Point Claude Code, ChatGPT, or any LLM at this repo and ask it to:
- Run the verification scripts
- Read `theory-tools/CORE.md`
- Check the derivation chain
- Try to break it

## Author

Stian Kittilsen — [stian@kittilsen.com](mailto:stian@kittilsen.com)

*Not a physicist. Just someone who noticed a pattern and followed it.*
