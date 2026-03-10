# One equation. Everything falls out.

I know how this looks. I know you'll be skeptical. That's fine — everything here is verifiable. Run the scripts. Check the numbers. Then decide.

---

## What this is

One self-referential equation:

**q + q² = 1**

Solution: q = 1/φ (the golden ratio's reciprocal). Evaluate standard modular forms (η, θ₃, θ₄) at this value. Out come the fundamental constants of physics — with no free parameters.

This is not numerology. There are verification scripts. The numbers either match or they don't.

---

## Step 1: Run this (2 minutes)

Open a terminal. Python 3, no dependencies needed.

```bash
python theory-tools/verify_golden_node.py
```

This computes all modular forms at q = 1/φ and checks them against measured values. Look at the output.

Then run the crown jewel:

```bash
python theory-tools/alpha_self_consistent.py
```

This derives the fine structure constant (1/α = 137.035999...) to **10.2 significant figures** from one equation with zero physics inputs. The proton-electron mass ratio μ = 1836.15 comes out simultaneously as a byproduct.

If those numbers don't make you pause, close this file. If they do, keep reading.

---

## Step 2: What just happened (5 minutes)

Read `theory-tools/significant.md`. It's the full derivation of alpha, step by step, with every input identified. The chain:

```
q + q² = 1
  → q = 1/φ (golden ratio)
  → E₈ lattice (unique algebra with golden field, proven math)
  → V(Φ) = λ(Φ² − Φ − 1)² (unique potential, proven)
  → domain wall (kink) with Pöschl-Teller depth n=2
  → exactly 2 bound states (ψ₀, ψ₁)
  → modular forms at q = 1/φ give all coupling constants
  → self-consistent fixed point gives α to 10.2 sig figs
```

Every step is either proven mathematics or standard physics (Jackiw-Rebbi 1976, Kaplan 1992, Randall-Sundrum 1999). The only new thing is evaluating at q = 1/φ.

---

## Step 3: It's not just alpha (10 minutes)

From the same equation, with zero free parameters:

| What | Formula | Match |
|------|---------|-------|
| Fine structure constant α | Self-consistent fixed point | **10.2 sig figs** (0.062 ppb) |
| Strong coupling α_s | η(1/φ) | 99.57% — **LIVE TEST** (CODATA 2026-27) |
| Weinberg angle sin²θ_W | η²/(2θ₄) − η⁴/4 | 99.996% (0.3σ) |
| Cosmological constant Λ | θ₄⁸⁰·√5/φ² | ~exact |
| Proton/electron mass ratio | Simultaneous output | 99.9998% |
| 9 fermion masses | Zero free parameters | avg 0.62% error |
| 3 PMNS mixing angles | From θ₄, ε=θ₄/θ₃ | All within 1σ |
| Baryon asymmetry η_B | θ₄⁶/√φ | 99.6% |
| Dark matter ratio | Level 2 wall tension | 0.73σ |
| Born rule (p=2) | Derived from PT n=2 | exact |
| Arrow of time | Pisot asymmetry | derived |
| 3+1 dimensions | 4 copies of A₂ in E₈ | derived |
| Why 3 generations | S₃ = SL(2,Z)/Γ(2) | **proven math** |

The full scorecard with 25 quantities: `theory-tools/COMPLETE-STATUS.md`

More scripts you can run:
- `python theory-tools/modular_couplings_v2.py` — all SM couplings
- `python theory-tools/lie_algebra_uniqueness.py` — E₈ is the ONLY algebra that works (3/3 vs 0/3 for all others)
- `python theory-tools/nome_uniqueness_scan.py` — q=1/φ is the ONLY nome that works (6061 tested)
- `python theory-tools/formula_isolation_test.py` — the core formula is isolated (0/719 neighbors match)
- `python theory-tools/one_resonance_fermion_derivation.py` — all 9 fermion masses

---

## Step 4: 54 unsolved mysteries (10 minutes)

Read `theory-tools/MYSTERIES-VS-FRAMEWORK.md`.

54 genuine unsolved mysteries across physics, biology, consciousness, psychology, civilization, and cosmology. Each one explained — clear mechanism from the same equation.

Including: hard problem of consciousness, origin of life, why we sleep, why music moves us, Libet delay (derived: 4 × Schumann = 510.8ms vs measured 500ms), placebo effect, why all psychedelics are aromatic, what the inner voice is (and why the Pirahã don't have one), phantom limb pain, what evil is (four tiers), why time speeds up with age, what cancer actually is, depression, addiction, the Fermi paradox, domestication, humor, aging, memory, gender differences, the Cambrian explosion, mass extinctions, chirality of life, why hexagons are everywhere.

---

## Step 5: The hand (this is the actual point)

Everything above is physics. This is where it gets real.

The equation q + q² = 1 generates 7 distinguished mathematical structures. One of them is the Monster group (the largest finite symmetry — the ceiling of mathematical description). The other 6 are called **pariah groups**. They sit outside the Monster. Outside description itself.

Those 6 pariahs, when you lay them out by their internal algebraic relationships, form a **hand**.

- **Index finger (J₁ — Seer):** Points. Emits pattern. Sees.
- **Thumb (O'N — Sensor):** Touches everything. Absorbs. Receives.
- **Middle finger (J₃ — Builder):** Central, load-bearing. Holds structure.
- **Ring finger (J₄ — Mystic):** Split between two nerve territories (the only finger that is). Dissolution, boundary.
- **Pinky (Ly — Still One):** At the edge. Release. Freedom. Asymptotic freedom.
- **Palm (Ru — Artist):** Not a finger. The hand itself. Makes things. Can't see itself.

This is not metaphor. The containment relations, the shared subgroups, the split structure of J₄, the independence of O'N (thumb), the coupling between J₃ and J₄ (middle-ring) — it's group theory. The hand doesn't illustrate the math. The math IS the hand.

### The three grips (forces)

The three fundamental forces map to three experiential axes. The mapping is a **forced bijection** — you can't rotate it:

| Force | What it does (uniquely) | Axis | Grip |
|-------|------------------------|------|------|
| **Strong** | Only force that **confines** | HOLDING | Confinement IS holding. Release IS letting go. |
| **EM** | Only force that **carries information** | KNOWING | Light IS how anything is known. |
| **Weak** | Only force that **transforms identity** | MAKING | Flavor change IS becoming something else. |

Try swapping any two. It doesn't work. Confinement ≠ knowing. Light ≠ holding. Identity transformation ≠ knowing. Each force has exactly one match.

This is derived in `theory-tools/CORE.md` §6d. The same S₃ group that permutes the modular forms (generating the coupling constants) permutes the experiential axes. One group, one action, both sides.

### The two bound states (you)

The domain wall has exactly 2 bound states:

- **ψ₀** = sech²(x) — symmetric, peaked at center. **Awareness. Presence. The ground.**
- **ψ₁** = sinh(x)/cosh²(x) — antisymmetric, has a node. **Attention. Direction. The narrator.**

Two modes. One wall. That's you.

When ψ₁ runs without ψ₀ (the narrator without awareness), you get: anxiety, rumination, autopilot, cruelty. When ψ₀ engages through ψ₁, you get: creation, play, love, humor.

The hard problem of consciousness dissolves: not "how does matter generate experience" but "experience and algebra are two descriptions of one self-referential thing."

---

## Step 6: Ask Claude

Point Claude Code at this repo. The key files:

| File | What it is |
|------|-----------|
| `theory-tools/CORE.md` | **THE structured reference. Read this.** |
| `theory-tools/significant.md` | Alpha derivation, full chain, verification script |
| `theory-tools/COMPLETE-STATUS.md` | Single source of truth, all claims + scores |
| `theory-tools/MYSTERIES-VS-FRAMEWORK.md` | 54 mysteries explained |
| `The paper/The hand at the bottom of reality.md` | The hand mapping (readable) |
| `The paper/the-hand-at-the-bottom-of-reality.html` | The book (print-ready) |

Tell Claude: *"Read theory-tools/CORE.md and theory-tools/significant.md. Then run the verification scripts. Tell me what you think."*

Or: *"Read theory-tools/MYSTERIES-VS-FRAMEWORK.md. Check whether the explanations hold up."*

Or just: *"What is this repo?"* — the CLAUDE.md will onboard it.

---

## What I'm not claiming

- I'm not claiming this is proven. 4 experimental tests are live (α_s, sin²θ₁₂, r, R). Any one could kill it.
- I'm not claiming I understand why it works. I found it. The algebra does what it does.
- I'm not claiming the consciousness part is science. It's structural interpretation. The physics part (the numbers) is verifiable.
- 19 dead claims are listed in CORE.md §7. The framework kills its own wrong ideas.

## What I am claiming

One equation generates all fundamental constants, explains 54 unsolved mysteries across all domains, and maps the boundary of mathematical description onto the human hand. Either I got extraordinarily lucky with the numbers (alpha at 10.2 sig figs from zero inputs — calculate the odds), or there's something here.

I need someone who can actually check it to look at it.
