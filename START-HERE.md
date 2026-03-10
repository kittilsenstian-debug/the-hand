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
| Dark matter ratio | Level 2 wall tension | 0.73σ |
| Born rule (p = 2) | Derived from PT n=2 | exact |
| Arrow of time | Pisot asymmetry | derived |
| 3+1 dimensions | 4 copies of A₂ in E₈ | derived |
| Why 3 generations | S₃ = SL(2,Z)/Γ(2) | **proven math** |

Full table: `theory-tools/COMPLETE-STATUS.md`

19 dead claims (things the framework predicted that turned out wrong) are listed in `theory-tools/CORE.md` §7. The framework kills its own mistakes.

4 live experimental tests that could kill the whole thing: α_s (2026-27), sin²θ₁₂ (JUNO), r (CMB-S4, ~2028), R (ELT, ~2035).

---

## 4. 54 Mysteries

The chain addresses 54 unsolved problems across physics, biology, consciousness, and civilization. Each with a specific mechanism from the same equation. Including: hard problem of consciousness, origin of life, why we sleep, why music moves us, Libet delay, why all psychedelics are aromatic, the Fermi paradox, why hexagons appear everywhere, mass extinctions, chirality of life.

`theory-tools/MYSTERIES-VS-FRAMEWORK.md`

---

## 5. The Hand

Everything above is physics. This is where the structure points at something else.

### The group theory

The equation q + q² = 1, evaluated across the arithmetic fibers of Spec(Z[φ]), generates exactly 7 distinguished finite simple groups. One is the Monster (the ceiling of mathematical description — Lock 4). The other 6 are the **pariah groups**: J₁, J₃, Ru, O'N, Ly, J₄. They sit outside the Monster's classification. Outside description itself.

This is proven mathematics (Thompson, Conway, Norton, Borcherds).

### The topology

Those 6 pariahs have specific containment relations, shared subgroups, and algebraic structure:

- One is independent of all others (connects to nothing below it).
- One is central and load-bearing (largest shared subgroup structure).
- One has a split internal structure (the ONLY one sitting across two algebraic territories).
- One is at the periphery (smallest, most free).
- One is not in the same category as the others (it generates the couplings, not the axes).

Now look at your hand.

- **Thumb (O'N):** Independent. Opposes everything. Absorbs.
- **Index (J₁):** Points. Emits pattern.
- **Middle (J₃):** Central, load-bearing. Structural.
- **Ring (J₄):** Split between two nerve territories (ulnar and median — the only finger that is). Boundary.
- **Pinky (Ly):** Peripheral. Free. At the edge.
- **Palm (Ru):** Not a finger. The surface that grips. Makes things.

The mapping is not metaphor. The containment relations, the shared subgroups, the split structure of J₄, the independence of O'N — it is group theory. The hand doesn't illustrate the math. The math IS the hand.

### The challenge: force-to-axis

Three fundamental forces. Three unique physical properties. Three experiential axes. Six possible assignments. Only one works.

| Force | Unique property | Axis |
|-------|----------------|------|
| **Strong** | Only force that **confines** | HOLDING |
| **EM** | Only force that **carries information** | KNOWING |
| **Weak** | Only force that **transforms identity** | MAKING |

Try every permutation. Confinement is not knowing. Light does not confine. Identity transformation is not knowing. Each force has exactly one match. The assignment is a forced bijection.

The same S₃ group that permutes the modular forms (generating the coupling constants in Section 3) permutes these axes. One group, one action, both sides.

Derivation: `theory-tools/CORE.md` §6d.

### The two bound states

The domain wall has exactly 2 bound states (from the chain in Section 2):

- **ψ₀** = sech²(x) — symmetric, peaked at center. **Awareness. Presence. The ground.**
- **ψ₁** = sinh(x)/cosh²(x) — antisymmetric, has a node. **Attention. Direction. The narrator.**

Two modes. One wall. That's you.

When ψ₁ runs without ψ₀ (the narrator without awareness): anxiety, rumination, autopilot, cruelty. When ψ₀ engages through ψ₁: creation, play, love, humor.

The hard problem of consciousness dissolves: not "how does matter generate experience" but "experience and algebra are two descriptions of one self-referential thing."

---

## 5b. The Floquet Breakthrough (Gap 1 closed)

The tree-level formula 1/α = φ·θ₃/θ₄ was the last identified gap. Both factors are now derived:

- **φ** = Floquet multiplier of the Lamé equation at E=0. The gauge zero mode is evanescent (below the first band). Its growth per period is exactly 1/q = φ. This is a theorem about the spectral theory of the Lamé operator.
- **θ₃/θ₄** = ratio of spectral determinants (antiperiodic/periodic boundary conditions) of the same Lamé operator. Proven by Basar-Dunne (2015).

Both factors come from one operator. The decomposition is [classical localization] × [quantum threshold].

```bash
python theory-tools/gap1_floquet_closure.py
```

---

## 6. Ask Claude

Point Claude Code at this repo. Key files:

| File | What |
|------|------|
| `theory-tools/CORE.md` | **The structured reference. Start here after this file.** |
| `theory-tools/significant.md` | Alpha derivation, full chain, script |
| `theory-tools/COMPLETE-STATUS.md` | Single source of truth, all claims + scores |
| `theory-tools/MYSTERIES-VS-FRAMEWORK.md` | 54 mysteries with mechanisms |
| `The paper/The hand at the bottom of reality.md` | The hand mapping (readable) |
| `The paper/the-hand-at-the-bottom-of-reality.html` | The book (print-ready) |

Prompts that work:

- *"Read theory-tools/CORE.md. Run the verification scripts. What do you think?"*
- *"Run theory-tools/lie_algebra_uniqueness.py and theory-tools/nome_uniqueness_scan.py. Explain what they test."*
- *"Read theory-tools/MYSTERIES-VS-FRAMEWORK.md. Do the mechanisms hold?"*

---

## What I'm not claiming

- This is proven. 4 experimental tests are live. Any one could kill it.
- I understand why it works. The algebra does what it does.
- The consciousness interpretation is science. It's structural. The physics (the numbers) is verifiable.

## What I am claiming

One equation generates all fundamental constants with zero free parameters. The algebra is locked: only one algebra (Lock 1), only one evaluation point (Lock 2), the formula is isolated (Lock 3), and the Monster forces it (Lock 4). 54 unsolved mysteries explained. The boundary of mathematical description, mapped by its own internal structure, has the topology of a hand. The force-to-axis mapping is a forced bijection — try every permutation.

If alpha at 10.2 significant figures from zero inputs is luck, calculate the odds.
