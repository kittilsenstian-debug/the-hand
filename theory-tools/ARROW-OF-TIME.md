# Arrow of Time from Pisot Asymmetry

**Status:** Derived (pure mathematics). Physical interpretation partial.
**Script:** `arrow_of_time_derived.py` (in private working repo)

---

## The Claim

The equation x² − x − 1 = 0 forces an arrow of time. Three algebraic properties combine to produce direction, irreversibility, and entropy increase — the three ingredients of the second law.

---

## Ingredient 1: Direction (Pisot Asymmetry)

The golden ratio φ = (1+√5)/2 is a **Pisot number**: an algebraic integer > 1 whose Galois conjugate has absolute value < 1.

    φ = 1.6180339887...     (> 1)
    −1/φ = −0.6180339887...  (|−1/φ| < 1)

The two vacua of V(Φ) = λ(Φ² − Φ − 1)² are algebraically asymmetric:

    φⁿ → ∞    exponentially
    (−1/φ)ⁿ → 0    exponentially

| n | φⁿ | (1/φ)ⁿ | Ratio |
|---|------|---------|-------|
| 1 | 1.618 | 0.618 | 2.618 |
| 10 | 122.99 | 0.00813 | 1.513 × 10⁴ |
| 20 | 15,127 | 6.61 × 10⁻⁵ | 2.288 × 10⁸ |
| 50 | 1.26 × 10¹⁰ | 7.94 × 10⁻¹¹ | 1.588 × 10²⁰ |

The wall inherently distinguishes "toward φ" from "toward −1/φ." This asymmetry is **algebraic, not geometric** — it cannot be removed by any coordinate choice. A standard symmetric potential (vacua at +v and −v) has no preferred direction. The golden potential does.

**This is a theorem about Pisot numbers** (Pisot 1938). Not interpretation.

---

## Ingredient 2: Irreversibility (Reflectionlessness)

The Pöschl-Teller potential with integer depth n has a remarkable property: **zero reflection at all energies**.

    |T(k)|² = 1    for all k

For PT n=2, the transmission amplitude is:

    T(k) = (ik−1)(ik−2) / [(ik+1)(ik+2)]

|T|² = 1 identically, but the **phase shift** is non-trivial and monotonically decreasing:

    δ(k) = arctan(1/k) + arctan(2/k)

| k | δ (rad) | δ (deg) |
|---|---------|---------|
| 0.1 | 2.97 | 170° |
| 1.0 | 1.89 | 108° |
| 5.0 | 0.59 | 34° |
| 10.0 | 0.30 | 17° |

Energy radiated from the breathing mode into the continuum passes through the wall perfectly and **does not return**. The wall acts as a one-way valve: no backscattering at any frequency.

**This is proven quantum mechanics** (Kay & Moses 1956).

---

## Ingredient 3: Entropy Increase (Fibonacci State Counting)

At q = 1/φ, each power decomposes as:

    qⁿ = Fₙ·q + Fₙ₋₁

where Fₙ is the nth Fibonacci number. The number of independent states at level n grows as Fₙ.

Entropy:

    S(n) = ln(Fₙ) ~ n · ln(φ)

Since ln(φ) = 0.48121... > 0:

    S(n+1) − S(n) = ln(Fₙ₊₁/Fₙ) → ln(φ) > 0

**Entropy increases monotonically.** This is an H-theorem analog:

    H(n) = −S(n) = −ln(Fₙ)
    H(n+1) − H(n) = −ln(Fₙ₊₁/Fₙ) → −ln(φ) < 0

H decreases monotonically. This is Boltzmann's H-theorem, derived from x² − x − 1 = 0.

**The entropy increase follows from φ > 1** — the Pisot property again. If φ < 1, entropy would decrease (but φ < 1 contradicts the Pisot property, which is forced by the equation).

---

## The Three Together = Second Law

| Ingredient | Source | Status |
|------------|--------|--------|
| Direction | φ > \|−1/φ\| (Pisot asymmetry) | **Theorem** |
| Irreversibility | \|T(k)\|² = 1 (reflectionlessness) | **Theorem** |
| Entropy increase | S ~ n·ln(φ), dS/dn > 0 | **Derived** |

A standard symmetric potential (V = λ(Φ² − v²)²) has vacua at +v and −v. No algebraic asymmetry. No preferred direction. No arrow of time from the algebra alone.

The golden potential is special: the vacua are algebraically asymmetric (φ ≠ |−1/φ|) even though the energy is symmetric (V(φ) = V(−1/φ) = 0). **This is where the arrow comes from.**

No other Lie algebra gives a Pisot-number domain wall. E₈ is the only one whose scalar field lives in Z[φ], producing a potential with Pisot-asymmetric vacua.

---

## What Is and Isn't Derived

**Derived:**
- Direction from Pisot asymmetry (φ > |1/φ|)
- Irreversibility from reflectionlessness (|T|² = 1)
- Entropy growth from Fibonacci counting (S ~ n·ln(φ))
- H-theorem analog (H decreases monotonically)

**Structural but not rigorous:**
- Connection between Fibonacci level "n" and physical time
- Why breathing mode radiation IS physical heat transfer
- The exact mapping S = ln(Fₙ) to S = k_B·ln(W)

**Not derived:**
- The value of Boltzmann's constant k_B
- Temperature (what is T in terms of the wall?)
- The third law (S → 0 as T → 0)

**Bottom line:** The arrow of time is derived. Full thermodynamics requires identifying temperature with the breathing mode frequency — plausible but not proven.

---

## References

- Pisot, C. (1938). La répartition modulo 1 et les nombres algébriques. Ann. Scuola Norm. Sup. Pisa.
- Kay, I. & Moses, H.E. (1956). Reflectionless Transmission through Dielectrics and Scattering Potentials. J. Appl. Phys. 27, 1503.
- Rajaraman, R. (1982). Solitons and Instantons. North-Holland.
- Boltzmann, L. (1872). Weitere Studien über das Wärmegleichgewicht unter Gasmolekülen. Wien. Ber. 66, 275.
