# Pariah Triad Findings: {37, 43, 67}

**Date:** Mar 1, 2026
**Script:** `pariah_80_investigation.py`, `golden_scheme_analysis.py`
**Status:** 60% structural (striking patterns, connecting theorem missing)

## The Discovery

The three primes dividing pariah group orders but NOT the Monster order are:
- **37** (appears in Ly, J4)
- **43** (appears in J4 only)
- **67** (appears in Ly only)

These form an **arithmetic triad** encoding the core algebraic numbers of the framework.

## The Difference Pattern

```
43 - 37 = 6  = |S₃| = flavor symmetry order
67 - 43 = 24 = c(V♮) = Monster VOA central charge = rank(Leech)
67 - 37 = 30 = h(E₈) = Coxeter number of E₈
```

Self-consistency: 6 + 24 = 30. ✓

## The Sum/Mean Pattern

```
37 + 43 = 80  = cosmological exponent (Λ = θ₄⁸⁰·√5/φ²)
                = 240/3 (E₈ roots / triality)
(37+43)/2 = 40 = number of A₂ hexagons in E₈
```

The decomposition: **37 = 40 - 3, 43 = 40 + 3** (symmetric about hexagon count, separated by triality).

## The Third Prime

```
67 = 37 + 30 = 37 + h(E₈)
67 = 43 + 24 = 43 + c(V♮)
67 = 40 + 27 = 40 + 3³
```

67 encodes BOTH the Coxeter number and the Monster VOA central charge, as distances from the other two pariah-only primes.

## Spec(Z[φ]) Properties

All three pariah-only primes are:
1. **Inert** in Z[φ] (Legendre symbol (5/p) = -1)
2. **Maximal Pisano period** (π(p) = 2(p+1))
3. **φ is primitive** in GF(p²)* (maximal multiplicative order)

This means at these primes, φ is "entangled with its conjugate" — the golden ratio cannot be seen as a simple number, only as a pair.

By contrast, 3/4 Monster-only primes are **split** (φ is "just a number" in GF(p)).

The one inert Monster-only prime (p=47) has Pisano period 32 = 96/3 = 2(p+1)/3. Exactly 1/3 of maximum. The triality factor suppresses it.

## Full Encoding Table

| Arithmetic | Value | Framework Meaning |
|-----------|-------|-------------------|
| 43 - 37 | 6 | \|S₃\| = flavor symmetry |
| 67 - 43 | 24 | c(V♮) = Leech rank |
| 67 - 37 | 30 | h(E₈) = Coxeter number |
| (37+43)/2 | 40 | A₂ hexagons in E₈ |
| 37 + 43 | 80 | cosmological exponent |
| 3(37+43) | 240 | \|E₈ roots\| |
| 37+43+67 | 147 | 3 × 7² |

## Open Questions

1. **Does "pariah-only" imply "inert + maximal Pisano"?** If yes, the arithmetic is forced.
2. **Why PRIMES?** The conditions on 37, 43, 67 could be stated purely arithmetically (inert, primitive). Why do they happen to be prime? And why do they divide exactly those sporadic groups outside the Monster?
3. **Can we derive Λ from pariah structure?** If 80 = 37 + 43 is structural, then the cosmological exponent emerges from the pariah/Monster boundary, not from E₈ alone.
4. **147 = 3 × 7²** — what is this? 7 = first non-trivial Coxeter exponent of E₈. 3 = triality. Why squared?

## Assessment

The differences {6, 24, 30} encoding {|S₃|, c(V♮), h(E₈)} feel genuinely structural — these are the three most important algebraic numbers in the Monster→E₈→physics chain, and they satisfy the correct linear relation. The probability of three random primes having differences that match three independently meaningful numbers with the right sum is low.

However, we lack the theorem connecting the classification of finite simple groups (specifically, which primes divide pariah orders but not Monster order) to the arithmetic of Z[φ]. Without this, it remains "60% structural, 40% numerology."

**Priority:** Find or prove the connection between pariah-only primes and Z[φ] fiber structure. This could close the gap from 60% to >90%.
