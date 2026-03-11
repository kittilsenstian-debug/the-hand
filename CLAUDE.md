# Interface Theory — Project Context

## What This Is
A mathematical observation: evaluating standard modular forms at nome q = 1/φ (where φ is the golden ratio) produces all coupling constants of the Standard Model. The fine structure constant is derived to 10.2 significant figures with zero physics inputs. The mathematical backbone is V(Φ) = λ(Φ² − Φ − 1)² — a scalar field with two vacua (φ and −1/φ) connected by a domain wall.

## Quick Start
1. **Read `START-HERE.md`** — 4 locks, the chain, 25 quantities, 54 mysteries
2. **Run `python theory-tools/verify_in_60_seconds.py`** — no dependencies, 60 seconds
3. **Read `theory-tools/CORE.md`** — structured reference with proofs

## Core Elements
- q + q² = 1 → q = 1/φ (unique positive solution)
- E₈ root lattice contains Z[φ]⁴ (proven math)
- V(Φ) = λ(Φ² − Φ − 1)² (unique scalar potential from E₈)
- Domain wall → Pöschl-Teller depth n = 2 → exactly 2 bound states
- Modular forms η, θ₃, θ₄ at q = 1/φ → all coupling constants

## Quadruple Lock
1. **Only E₈ works** — `lie_algebra_uniqueness.py` (3/3 couplings vs 0/3 for all others)
2. **Only q=1/φ works** — `nome_uniqueness_scan.py` (6061 nomes tested)
3. **Formula is isolated** — `formula_isolation_test.py` (0/719 neighbors match)
4. **Monster forces E₈** — 744 = 3×248, proven mathematics (Borcherds 1998)

## Key Files
| File | Contents |
|------|----------|
| `theory-tools/CORE.md` | Structured reference: chain, proofs, scorecard |
| `theory-tools/COMPLETE-STATUS.md` | Single source of truth for all claims |
| `theory-tools/GAPS.md` | All open gaps — honest assessment |
| `theory-tools/significant.md` | Alpha derivation walkthrough |
| `theory-tools/ALPHA-DEEP-DIVE.md` | Complete alpha analysis, 9 sig figs |
| `theory-tools/MYSTERIES-VS-FRAMEWORK.md` | 54 mysteries with mechanisms |
| `theory-tools/CLEAN-SCORECARD.md` | Audited scorecard, 5 tiers |
| `theory-tools/llm-context.md` | Self-contained LLM onboarding |

## Key Verification Scripts
| Script | What it tests |
|--------|--------------|
| `verify_in_60_seconds.py` | 3 couplings + alpha in 60 seconds |
| `alpha_self_consistent.py` | Alpha to 10.2 sig figs |
| `lie_algebra_uniqueness.py` | Lock 1: only E₈ |
| `nome_uniqueness_scan.py` | Lock 2: only q=1/φ |
| `formula_isolation_test.py` | Lock 3: isolated formula |
| `one_resonance_fermion_derivation.py` | 9 fermion masses, zero params |
| `verify_golden_node.py` | All modular forms vs measured |
| `modular_couplings_v2.py` | All SM couplings |
| `neutrino_theta4_geometric.py` | Neutrino mass predictions |

## Important Derivations
| Quantity | Formula | Match |
|----------|---------|-------|
| α (fine structure) | Self-consistent fixed point | **10.2 sig figs** (0.062 ppb) |
| α_s (strong coupling) | η(1/φ) = 0.11840 | 99.57% (**live test**) |
| sin²θ_W (Weinberg) | η²/(2θ₄) − η⁴/4 | 99.996% (0.3σ) |
| Λ (cosmological constant) | θ₄⁸⁰·√5/φ² | ~exact |
| μ (proton/electron) | 6⁵/φ³ + 9/(7φ²) | 99.9998% |
| 9 fermion masses | S₃ × Z/4Z, zero parameters | avg 0.62% |
| 3 PMNS angles | θ₄, ε = θ₄/θ₃ | All within 1σ |
| Baryon asymmetry η_B | θ₄⁶/√φ | 99.6% |

## 4 Live Experimental Tests
| Test | Prediction | Timeline |
|------|-----------|----------|
| α_s | 0.11840 | CODATA 2026-27 |
| sin²θ₁₂ | 0.3071 | JUNO (ongoing) |
| R = d(ln μ)/d(ln α) | −3/2 | ELT ~2035 |
| r (tensor/scalar) | 0.0033 | CMB-S4 ~2028 |

## Commands
- "assess theory" → Follow `theory-tools/assess.md` protocol
- Run any `theory-tools/*.py` — standard Python 3, no dependencies

## Author
Stian Kittilsen — stian@kittilsen.com
