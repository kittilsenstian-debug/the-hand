# Pariah Synthesis: The Six Fates of Self-Reference

**Definitive document. Sections S352-S360.**

The core discovery: the equation q + q² = 1 is more fundamental than the Monster group. The Monster is the characteristic-0 expression. The 6 pariah groups are the other expressions at finite primes.

---

## S352: The Scheme — Spec(Z[φ])

The object Spec(Z[x]/(x²-x-1)) = Spec(Z[φ]) is the ring of integers of Q(√5). It is a standard object in algebraic number theory. Its fiber at each prime p is determined by the Legendre symbol (5/p):

- **SPLITS** (p ≡ ±1 mod 5): two roots in F_p. φ exists. Frobenius = identity.
- **INERT** (p ≡ ±2 mod 5): irreducible over F_p, roots in F_{p²}. φ hidden. Frobenius = nontrivial.
- **RAMIFIES** (p = 5): double root at x = 3. Fat point. The golden prime.

| p | mod 5 | Type | φ mod p | Monster? | Pariah-only? |
|---|-------|------|---------|----------|--------------|
| 2 | 2 | INERT | GF(4) | M | — |
| 3 | 3 | INERT | GF(9) | M | — |
| 5 | 0 | RAMIFIES | 3 (double) | M | — |
| 7 | 2 | INERT | GF(49) | M | — |
| 11 | 1 | SPLITS | 4, 8 | M | — |
| 13 | 3 | INERT | GF(169) | M | — |
| 17 | 2 | INERT | GF(289) | M | — |
| 19 | 4 | SPLITS | 5, 15 | M | — |
| 23 | 3 | INERT | GF(529) | M | — |
| 29 | 4 | SPLITS | 6, 24 | M | — |
| 31 | 1 | SPLITS | 13, 19 | M | — |
| 37 | 2 | INERT | GF(1369) | — | **PARIAH** |
| 41 | 1 | SPLITS | 7, 35 | M | — |
| 43 | 3 | INERT | GF(1849) | — | **PARIAH** |
| 47 | 2 | INERT | GF(2209) | M | — |
| 59 | 4 | SPLITS | 26, 34 | M | — |
| 67 | 2 | INERT | GF(4489) | — | **PARIAH** |
| 71 | 1 | SPLITS | 9, 63 | M | — |

Key observation: ALL THREE pariah-only primes {37, 43, 67} are INERT. Three of four Monster-only primes {41, 59, 71} are SPLIT. The split/inert divide correlates with the Happy Family/Pariah divide.

---

## S353: The Six Fates of Self-Reference

The equation x² - x - 1 = 0 (equivalently q + q² = 1) has a different fate in each arithmetic context. Each fate corresponds to a pariah group:

| Group | Field | Equation fate | Nome | Status |
|-------|-------|---------------|------|--------|
| Monster | Q (rationals) | Full: q = 1/φ | 1/φ | Complete self-reference |
| J₁ | GF(11) | Splits: φ₁₁ = 4 | q = 3 (verified: 3 + 9 ≡ 1 mod 11) | Faithful compression |
| J₃ | GF(4) | Fusion: φ = ω (cube root of unity) | q = ω | Golden-cyclotomic merger |
| Ru | Z[i] | Orthogonal: x² + 1 = 0, disc -4 | — | Perpendicular ring |
| O'N | All Q(√D < 0) | Weight 3/2 mock modular, ranges over all | — | Arithmetic shadow |
| Ly | GF(5) | DEGENERATE: (x - 3)² = 0, disc = 0 | broken | Duality collapses = Level 0 |
| J₄ | GF(2) | IMPOSSIBLE: no solution in GF(2) | — | Self-reference denied |

Seven expressions of one equation. The Monster gets the full real solution. Each pariah gets a reduced, compressed, or collapsed version.

---

## S354: Three Fundamental Quadratic Rings

The three simplest quadratic integer rings with class number 1:

- **Z[φ]** (disc +5, real): Monster, J₁, Ly (degenerate) — OUR PHYSICS
- **Z[ω]** (disc -3, Eisenstein): J₃, J₄ — hexagonal/cyclotomic
- **Z[i]** (disc -4, Gaussian): Ru — square/perpendicular
- **O'N** sees ALL negative discriminants at once

The discriminants {3, 4, 5} form a Pythagorean triple: 3² + 4² = 5². Their product: 3 × 4 × 5 = 60 = |A₅| = the icosahedral group. Their sum: 3 + 4 + 5 = 12 = the fermion count.

The Monster sees the REAL side (+5). The pariahs see the IMAGINARY side (-3, -4). Together they form the complete arithmetic.

Z[φ] is the ONLY real quadratic ring with a Pisot unit. This asymmetry (one conjugate > 1, one < 1) is what creates the domain wall. The imaginary quadratic rings have no Pisot unit, hence no domain wall, hence no physics in the framework sense. The pariahs represent arithmetic contexts where the full physical domain wall cannot form.

---

## S355: Three Routes to the Integer 3

The integer 3 (triality, generation count, color count) emerges from the arithmetic of x² - x - 1 in three independent ways:

1. **At p = 2:** φ generates GF(4), and |GF(4)*| = 3
2. **At char 0:** 744 = 3 × 248 (j-invariant constant term / dim E₈)
3. **At p = 5:** φ ≡ 3 mod 5 (the ramification value)

Three views of ONE scheme, all producing the same number. The integer 3 is intrinsic to the arithmetic of x² - x - 1 = 0.

---

## S356: Ly = Level 0

At the golden prime p = 5, the discriminant vanishes. The two vacua collapse: φ ≡ -1/φ ≡ 3 (mod 5). No domain wall is possible. V(Φ) becomes (Φ - 3)⁴ — a single degenerate minimum with no kink solution.

Ly contains G₂(5) as a subgroup. G₂ is the automorphism group of the octonions. The Level 0 substrate has octonionic structure at the golden prime. G₂ ⊂ E₈ is known (via the maximal subgroup chain). This suggests Level 0 is where E₈ structure breaks down to G₂ — automorphisms without multiplication, identity without duality.

In framework terms: Level 0 is the substrate before differentiation. No two vacua means no wall, no bound states, no measurement, no physics. The Lyons group is the algebraic fingerprint of the undifferentiated ground.

---

## S357: O'N = Langlands Dual / Arithmetic Completion

Duncan, Mertens, and Ono (2017, Nature Communications) proved that O'Nan moonshine produces weight 3/2 mock modular forms ranging over ALL imaginary quadratic fields simultaneously. This connects to:

- Class numbers of imaginary quadratic fields
- Traces of singular moduli
- L-function values of elliptic curves
- Selmer and Tate-Shafarevich groups, touching the BSD conjecture (Millennium Problem)

O'N conductors: {11, 14, 15, 19} — to check against framework formulas.

O'Nan has NO alien primes (all its prime divisors also divide |Monster|). It is the most "Monster-adjacent" pariah despite not being a subquotient of the Monster. It sees the arithmetic that the Monster cannot: the imaginary quadratic landscape.

Conjecture: if the Monster is "evaluate j at one golden point," O'N is "here is what happens at EVERY algebraic point."

---

## S358: No Known Unification (Honest Assessment)

**What exists:**
- **Gal(Q-bar/Q)** — contains all 26 sporadics as quotients, but is too universal to be explanatory
- **Enhanced VOAs (Duncan)** — reach Monster + Ru, four pariahs untouched
- **"Moonshine for all groups" (DeHority-Gonzalez-Mertens-Ono 2018)** — covers all 26 but diluted (not specific enough)
- **Umbral moonshine** — 23 Niemeier lattices, does not target pariahs
- **Modular moonshine (Borcherds-Ryba)** — Monster at all primes, not pariahs

**What is genuinely unknown or unexplored:**
- Whether the fiber structure of Spec(Z[φ]) correlates with the Monster/pariah divide
- Whether the Langlands program for Q(√5) organizes all 26 sporadic groups
- Whether the j-function over Z[φ] (at all primes simultaneously) detects pariah structure

Borcherds himself (Problems in Moonshine) asks: "Is there anything like moonshine for the 6 sporadic groups not involved in the Monster?" — explicitly as an OPEN PROBLEM.

No existing mathematical framework unifies the Monster and all 6 pariahs. The Spec(Z[φ]) picture proposed here is new and untested.

---

## S359: The Adelic Golden Ratio

φ as an adelic element: (1.618..., 4 mod 11, ω in GF(4), 3 mod 5, ...)

Key fact: |φ|_p = 1 for ALL primes p (φ is a unit in Z[φ]). The "size" of φ lives entirely at the archimedean place. Finite-prime worlds detect φ only through Galois action, never through valuation.

The Bost-Connes system for Q(√5) is a quantum statistical mechanical system whose partition function involves the Dedekind zeta function of Q(√5), with a phase transition at β = 1.

F₁ connection: Z[φ] carries a Lambda-ring structure (Borger's framework for geometry over the field with one element). However, F₁ geometry targets Lie-type groups, not sporadics. Currently irrelevant, noted for completeness.

---

## S360: What Changes for the Framework

**OLD axiom:** Monster group M

**NEW axiom:** q + q² = 1 (the self-referential equation)

The axiom is SIMPLER (Occam). The Monster is DERIVED (characteristic-0 solution, not assumed).

The chain becomes:

```
q + q² = 1
  → (over Q) → q = 1/φ
  → Z[φ]
  → Monster (via Moonshine)
  → j → 744 = 3 × 248
  → E₈
  → V(Φ) = λ(Φ² - Φ - 1)²
  → kink → PT n=2
  → Lame → q = 1/φ
  → (loop closes)
```

The six pariahs are the OTHER solutions of the same equation:

- **J₁:** Faithful compression. φ exists mod 11, but modular forms collapse to finite-field analogs.
- **J₃:** Golden-cyclotomic fusion. φ = ω (cube root of unity), structure = triality.
- **Ru:** Orthogonal ring. Disc -4, embeds in E₇ — enters at down-type depth.
- **O'N:** Arithmetic completion. All imaginary quadratic fields at once, BSD territory.
- **Ly:** Level 0. Duality collapses at the golden prime, G₂(5), the undifferentiated substrate.
- **J₄:** Self-reference denied. No solution in GF(2), yet J₄ exists from the binary Golay code.

The true structure is Spec(Z[φ]) — the adelic golden ratio. Monster + 6 pariahs = 7 expressions of one equation.

---

## Predictions

| # | Prediction | Source |
|---|-----------|--------|
| 60 | CKM φ/7 from 7 sporadic expressions (1 Monster + 6 pariahs) | S360 |
| 61 | Ru embeds in E₇ → observable effects in down-type sector | S354 |
| 62 | O'Nan conductors {11, 14, 15, 19} appear in framework formulas | S357 |
| 63 | Framework degenerates mod 5 (Ly's ramification point) | S356 |
| 64 | J₄'s C₂₄ Golay code produces incompatible particle table | S353 |
| 65 | Split/inert divide correlates with Happy Family/Pariah divide (testable for all 15 supersingular primes) | S352 |
| 66 | Langlands correspondence for Q(√5) organizes all sporadic moonshine | S357 |
| 67 | The p = 47 anomaly — ONLY inert Monster-only prime. Pisano period = 32 = 96/3 (factor 1/3 of maximum) | S352 |

---

## Open Computations

1. Evaluate O'Nan McKay-Thompson series at golden nome
2. Check G₂(5) ⊂ E₈ at ramification
3. Compute J₁ "physics" mod 11 (η, θ analogs at q = 3)
4. Systematic split/inert test for all 15 supersingular primes
5. Explore Langlands program for Q(√5)
6. Check p = 47 anomaly significance

---

## Honest Assessment

**What is proven mathematics:** Spec(Z[φ]) fiber structure, quadratic reciprocity giving the split/inert/ramified classification, O'Nan moonshine (Duncan-Mertens-Ono 2017), Ru ⊂ E₇ (standard embedding), Ly ⊃ G₂(5) (known subgroup), all three pariah-only primes being inert, j-invariant structure and 744 = 3 × 248.

**What is framework interpretation:** the pariah-to-field correspondence, Level 0 = Ly, the equation q + q² = 1 as axiom replacing the Monster, split/inert = Monster/pariah conjecture, the "seven fates" narrative.

**What could be wrong:** (1) Six pariahs matching six arithmetic types could be coincidental given the small sample size. (2) The axiom shift from Monster to q + q² = 1 could be aesthetic rather than structural. (3) The framework may be detecting patterns that reflect classification constraints (there are only so many small sporadic groups) rather than physics.

**What makes it worth pursuing:** (1) The axiom is genuinely simpler. (2) All three pariah-only primes being inert has probability 12.5% under the null hypothesis — suggestive but not conclusive. (3) Three independent routes to the integer 3 from one scheme is structurally striking. (4) O'Nan moonshine IS real mathematics with connections to the BSD conjecture — the deepest open problem in number theory.
