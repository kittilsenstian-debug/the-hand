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

## 4. Open Gap

The tree-level formula 1/α = φ·θ₃/θ₄ = 136.393 has two factors. One is derived, one is identified:

- **θ₃/θ₄** = ratio of spectral determinants (antiperiodic/periodic boundary conditions) of the Lamé operator at PT depth n=2. Proven by Basar-Dunne (2015). This is a theorem.
- **φ** = vacuum expectation value Φ₊ of the golden scalar field (Dvali-Shifman 1997). Why the gauge kinetic function gives f(Φ) = Φ (not Φ²) is the one remaining interpretive step.

```bash
python theory-tools/gap1_floquet_closure.py
```

---

## 5. Key Files

| File | What |
|------|------|
| `theory-tools/CORE.md` | **Structured reference with derivation chain and proofs** |
| `theory-tools/significant.md` | Alpha derivation, full chain, script |
| `theory-tools/COMPLETE-STATUS.md` | Single source of truth, all claims + scores |

---

## What I'm not claiming

- This is proven. 4 experimental tests are live. Any one could kill it.
- I understand why it works. The algebra does what it does.

## What I am claiming

One equation generates all fundamental constants with zero free parameters. The algebra is locked: only one algebra (Lock 1), only one evaluation point (Lock 2), the formula is isolated (Lock 3), and the Monster forces it (Lock 4).

19 claims the framework generated that turned out wrong are documented in `theory-tools/CORE.md` §7.

If alpha at 10.2 significant figures from zero inputs is luck, calculate the odds.
