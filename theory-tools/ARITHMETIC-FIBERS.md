# Arithmetic Fibers of V(Φ) over Spec(Z[φ])

*The coupling constants are special values of the Dedekind zeta function of Q(√5). The pariah groups are the fibers where specific physics fails.*

```bash
python theory-tools/arithmetic_fibers.py
```

---

## L-function identities

The Dirichlet L-function L(s, χ₅) of Q(√5) at negative integers gives framework constants. These are exact — computed via generalized Bernoulli numbers.

| s | L(s, χ₅) | ζ_K(s) | What it is |
|---|-----------|--------|-----------|
| −1 | **−2/5** | 1/30 | c₂ = VP coefficient in alpha derivation |
| −3 | **2** | 1/60 | n = PT bound state count |
| −5 | −134/5 | **67**/630 | 67 = pariah-only prime (Ly, J₄) |
| −7 | 722 | **19²**/120 | 19 = O'Nan conductor, squared |

L(−1, χ₅) = −2/5 is the coefficient that takes alpha from 4 to 10 significant figures. L(−3, χ₅) = 2 is the number of Pöschl-Teller bound states. Both are exact.

The ratio ζ_K(−1)/ζ_K(−3) = 2 = PT depth.

## Pariah primes in zeta numerators

The numerators of ζ_K(−n) contain framework-connected primes:

| Prime | First appears at s = | What it is |
|-------|---------------------|-----------|
| 67 | −5 | Pariah-only prime (Ly). Index 5 = Ly characteristic. |
| 19 | −7 | O'Nan conductor. Index 7 = O'Nan characteristic. |
| 17 | −13 | J₃ order prime |
| 103 | −23 | Appears in c(−4) factorization |
| 37 | −31 | Pariah-only prime. Index 31 = O'Nan order prime. |
| 43 | not found (n ≤ 79) | J₄'s prime. Invisible to the zeta function. |

The pariah prime 67 appears at the index equal to the Ly characteristic (5). The O'Nan conductor 19 appears at the index equal to the O'Nan characteristic (7). The alien prime 37 appears at s = −67 (the other alien prime's index).

43 does not appear. J₄ is algebraically impossible. Its prime leaves no trace.

The denominators contain only primes dividing pariah group orders: {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31}.

## Fiber physics

At each prime p, reduce x² − x − 1 = 0 mod p. The result determines what physics exists at that fiber.

| p | Group | Type | φ at fiber | What survives |
|---|-------|------|-----------|--------------|
| 2 | J₃/J₄ | Inert → GF(4) | φ = ω (cube root of unity) | Nothing. V'(Φ) ≡ 0. Triality exists but can't act. |
| 5 | Ly | Ramified | Double root (φ = 3 mod 5) | Nothing. Vacua merge. No wall. |
| 7 | O'Nan | Inert → GF(49) | ord(φ) = 16, barrier exists | EM only. η = 0, θ₄ ≠ 0. GF(49)*/⟨φ⟩ = Z/3Z. |
| 11 | J₁ | Split | φ = 8 mod 11, ord = 10 | EM only. η = 0 at n = 10. |
| 29 | Ru | Split | φ = 6 mod 29, ord = 14 | Nothing. η = 0 AND sin²θ_W = 0. |

J₃ (char 2): The golden ratio becomes a cube root of unity. The potential has two vacua but V'(Φ) = 0 for all Φ — the factor 2 in V' is killed by the characteristic. Structure without dynamics.

O'Nan (char 7): φ has order 16 in GF(49)*. The full group GF(49)* has order 48. The quotient GF(49)*/⟨φ⟩ = Z/3Z. Triality is the part that φ does NOT generate — it's the coset structure. The strong force vanishes (η product hits zero at 1 − q¹⁶ = 0), but θ₄ ≠ 0: electromagnetism survives.

J₄: Requires simultaneous existence in GF(4), GF(37²), and GF(43²). At all three, φ lives in the extension field, not the base. Self-reference impossible.

## Pisano period = phi order at fiber

For every prime p tested (up to 100): the Pisano period π(p) equals the order of φ in the multiplicative group of the fiber (GF(p)* for split, GF(p²)* for inert).

| p | π(p) | Type | |GF*| | π divides |GF*| |
|---|------|------|-------|---------------|
| 2 | 3 | Inert | 3 | yes |
| 7 | 16 | Inert | 48 | yes (48 = 16 × 3) |
| 11 | 10 | Split | 10 | yes |
| 29 | 14 | Split | 28 | yes |
| 37 | 76 | Inert | 1368 | yes |
| 43 | 88 | Inert | 1848 | yes |
| 67 | 136 | Inert | 4488 | yes |

The Fibonacci sequence's periodicity at each prime is the penetration depth of the golden ratio into that fiber.

## Dark matter ratio

σ₋₁(4) = 1 + 1/2 + 1/4 = 7/4.

**(7/4)³ = 343/64 = 5.359375.**

Measured: Ω_DM/Ω_b = 5.364 ± 0.07 (Planck 2018). Match: **0.07σ**.

7 = O'Nan characteristic. 4 = disc(Z[i]) = Gaussian discriminant. Cube = triality.

This is a rational prediction with zero free parameters.

## Fine structure constant decomposition

```
1/α = φ⁷ × 4.698 × 1.00472
```

| Factor | Value | Source |
|--------|-------|--------|
| φ⁷ | 29.034 | Axiom: (1+q)/(1−q) = φ³, squared, times φ |
| Correction | 4.698 | Product over n ≥ 2 in θ₃/θ₄ ratio. Dominant: φ² (triality) |
| VP | 1.00472 | L(−1, χ₅) = −2/5 gives c₂. Correction = 0.47%. |

The axiom q + q² = 1 gives φ⁷. Triality (from the n = 2, 2n−1 = 3 factor) gives φ². The L-function gives the VP correction. Together: 10 significant figures.

## Structural identities

| Identity | Value |
|----------|-------|
| 1 + 2q = √5 | Exact. (1 + 2/φ = 2φ − 1 = √5) |
| 1 − 2q = −1/φ³ | Exact. (√5 − 2 = 1/φ³) |
| φ² + 1 + 1/φ² = 4 | Exact. PT ground state norm 4/3 = average of E₈ golden projections squared. |

The near-cancellation in θ₄ (= 1 − 2q + higher terms = 1 − 1.236 + 0.292 − ... = 0.0303) is the axiom pushing 2q past 1. The hierarchy v/M_Pl ∼ θ₄⁸⁰ is the 80th power of this cancellation.

## Verification

```bash
python theory-tools/arithmetic_fibers.py    # all results in this document
python theory-tools/all_fibers.py           # eta death at 5 finite fields (existing)
python theory-tools/j1_physics_mod11.py     # J1 compressed physics (existing)
```
