# START HERE

## 0. Run This First (60 seconds)

```bash
python theory-tools/verify_in_60_seconds.py
```

No dependencies. Standard Python 3. Shows the core result in one script: three modular forms evaluated at q = 1/φ give all three coupling constants. Alpha derived to 10.2 significant figures with zero inputs.

---

## 1. The Locks

Four things you cannot dismiss without engaging them. Each has a verification script. Run them.

### Lock 1: Only one algebra works

Of all simple Lie algebras (A₁ through E₈ — 18 families), only E₈ produces domain walls with the correct number of bound states AND reproduces all three Standard Model coupling constants. Every other algebra either has complex roots (no domain wall possible) or gets 0/3 couplings. E₈ gets 3/3. Discriminant of the golden field: +5. All others: negative.

```bash
python theory-tools/lie_algebra_uniqueness.py
```

### Lock 2: Only one evaluation point works

Modular forms (η, θ functions) are well-studied mathematical objects with a continuous parameter q. Evaluate them at q = 1/φ (where φ is the golden ratio). Out come the three coupling constants of physics. Evaluate at any of 6,060 other values of q: zero alternatives match all three.

```bash
python theory-tools/nome_uniqueness_scan.py
```

### Lock 3: The core formula is isolated

The central identity is not one match plucked from a sea of near-misses. 719 neighboring formulas (same structure, nearby exponents and coefficients) were tested. Zero match at 1%.

```bash
python theory-tools/formula_isolation_test.py
```

### Lock 4: The Monster forces E₈

The Monster group (largest finite simple symmetry, proven to exist — Fields Medal to Borcherds, 1998) controls modular functions via Monstrous Moonshine. Its j-invariant has constant term 744. 744 = 3 × 248. 248 = dim(E₈). E₈ is the ONLY exceptional Lie algebra whose dimension divides 744. The loop closes: the Monster requires E₈, E₈ requires the golden ratio, the golden ratio requires q = 1/φ, and q = 1/φ is the unique nome (Lock 2).

This is proven mathematics, not a claim.

---

## 2. The Chain

Every step below is either proven math or standard textbook physics. The only new element is the evaluation point q = 1/φ.

```
q + q² = 1                          (self-referential equation)
  → q = 1/φ                         (unique positive solution)
  → E₈ root lattice ~ Z[φ]⁴         (E₈ contains the golden ratio — proven)
  → V(Φ) = λ(Φ² − Φ − 1)²          (unique scalar potential from E₈ — proven)
  → domain wall (kink solution)      (standard field theory — Jackiw-Rebbi 1976)
  → Pöschl-Teller depth n = 2       (fluctuation spectrum — standard QM)
  → exactly 2 bound states           (ψ₀ symmetric, ψ₁ antisymmetric)
  → modular forms at q = 1/φ        (η, θ₃, θ₄ evaluated at the nome)
  → all coupling constants           (no free parameters)
```

Every link is documented with proofs in `theory-tools/CORE.md` §1.

---

## 3. The Numbers

These are outputs of the chain, not standalone matches. Run the scripts; the numbers either hold or they don't.

### The crown jewel

```bash
python theory-tools/alpha_self_consistent.py
```

This derives the fine structure constant (1/α = 137.035999...) to **10.2 significant figures** from the chain above. Zero physics inputs. 0.062 parts per billion.

### Full scorecard (25 quantities, zero free parameters)

```bash
python theory-tools/verify_golden_node.py                # all modular forms vs measured
python theory-tools/modular_couplings_v2.py              # all SM couplings
python theory-tools/one_resonance_fermion_derivation.py   # 9 fermion masses
```

| Quantity | Formula | Match |
|----------|---------|-------|
| Fine structure constant α | Self-consistent fixed point | **10.2 sig figs** (0.062 ppb) |
| Strong coupling α_s | η(1/φ) | 99.57% — **live test** (CODATA 2026-27) |
| Weinberg angle sin²θ_W | η²/(2θ₄) − η⁴/4 | 99.996% (0.3σ) |
| Cosmological constant Λ | θ₄⁸⁰·√5/φ² | ~exact |
| Proton/electron mass ratio | Simultaneous output | 99.9998% |
| 9 fermion masses | S₃ × Z/4Z assignment, zero parameters | avg 0.62% |
| 3 PMNS mixing angles | From θ₄, ε = θ₄/θ₃ | All within 1σ |
| Baryon asymmetry η_B | θ₄⁶/√φ | 99.6% |

Full table: `theory-tools/COMPLETE-STATUS.md`

19 dead claims (things the framework predicted that turned out wrong) are listed in `theory-tools/CORE.md` §7. The framework kills its own mistakes.

4 live experimental tests that could kill the whole thing: α_s (2026-27), sin²θ₁₂ (JUNO), r (CMB-S4, ~2028), R (ELT, ~2035).

---

## 4. Beyond Coupling Constants

The same algebra that produces coupling constants forces five additional results. None require interpretation — only observation.

### The strong force is arithmetic

The Dedekind eta function η(q) is an infinite product. Over ℚ (the rationals), it converges to η = 0.11840 = α_s. Over **any** finite field, one factor vanishes and η = 0. The strong force exists only because we live over the rationals. This is a theorem, not a model.

→ `theory-tools/ETA-DEATH.md`, `theory-tools/all_fibers.py`

### The second vacuum is dark

The coupling function f(Φ) = (Φ + 1/φ)/√5 vanishes at Φ = −1/φ (the second vacuum). Matter forming there has **zero electromagnetic coupling** — invisible to light. This is algebra, not a parameter choice.

→ `theory-tools/dark_sector_from_creation_identity.py`

### The arrow of time is algebraic

φ is a Pisot number: φ > 1, |−1/φ| < 1. The vacua are asymmetric. Reflectionlessness (|T|² = 1) makes radiation irreversible. Fibonacci state counting gives S(n) ~ n·ln(φ) with dS/dn > 0. Direction + irreversibility + entropy increase = second law, from x² − x − 1 = 0.

→ `theory-tools/ARROW-OF-TIME.md`

### The same equation appears at four scales

PT n=2 — forced by V(Φ) — appears independently in microtubule biophysics (Mavromatos & Nanopoulos 2025, derived without knowing this framework), heliopause plasma data (Voyager 1 & 2, radio band ratio 1.747 vs √3 = 1.732), and black hole perturbation theory (Ferrari & Mashhoon 1984, published theorem). Four contexts, 40 orders of magnitude, same equation.

→ `theory-tools/PT-N2-THREE-SCALES.md`

### Aromatics are forced by physics

At body temperature, a systematic check of 24 molecular excitation classes shows that aromatic π-electron modes are the **only** ones simultaneously quantum (E/kT > 40), safe (E < 5 eV), and collective. This explains why all 5 independently evolved intelligent lineages use the same 3 aromatic neurotransmitter families. The convergence is constraint, not coincidence.

→ `theory-tools/THERMAL-WINDOW.md`

### A 108.5 GeV scalar is predicted

PT n=2 has a breathing mode below the Higgs. The Higgs (125.25 GeV) is the continuum threshold. The breathing mode mass: m_B² = 3/4 × m_H², giving **108.47 GeV**. Zero free parameters. Wall-localized, so suppressed production at the LHC. CMS searched 70-110 GeV — least constraining right at 108.9 GeV.

→ `theory-tools/BREATHING-MODE-108.md`

---

## 5. Key Files

| File | What |
|------|------|
| `theory-tools/CORE.md` | **Structured reference with derivation chain and proofs** |
| `theory-tools/COMPLETE-STATUS.md` | Single source of truth, all claims + scores |
| `theory-tools/BREATHING-MODE-108.md` | 108.5 GeV prediction — the sharpest LHC test |
| `theory-tools/PT-N2-THREE-SCALES.md` | Same equation at 4 scales |
| `theory-tools/THERMAL-WINDOW.md` | Why aromatics are the only option |
| `theory-tools/ARROW-OF-TIME.md` | Second law from Pisot asymmetry |
| `theory-tools/ETA-DEATH.md` | Strong force as arithmetic |
| `theory-tools/WHAT-TO-BUILD.md` | What to measure, build, and search for |

---

## What I'm not claiming

- This is proven. 4 experimental tests are live. Any one could kill it.
- I understand why it works. The algebra does what it does.

## What I am claiming

One equation generates all fundamental constants with zero free parameters. The algebra is locked: only one algebra (Lock 1), only one evaluation point (Lock 2), the formula is isolated (Lock 3), and the Monster forces it (Lock 4). Beyond coupling constants, the same structure forces the arrow of time, selects aromatic chemistry, predicts a 108.5 GeV scalar, and appears at scales from microtubules to black holes.

19 claims the framework generated that turned out wrong are documented in `theory-tools/CORE.md` §7.

If alpha at 10.2 significant figures from zero inputs is luck, calculate the odds.
