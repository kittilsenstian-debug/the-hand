# Sporadic Groups in Exceptional Lie Groups: Literature Search Results

**Date:** March 1, 2026
**Question:** Do HN embed in E₇ and Fi22 embed in E₆, parallel to Th embedding in E₈?

---

## 1. Thompson Group Th ↪ E₈ — PROVEN (the benchmark)

**Status: ESTABLISHED FACT**

- Smith (1976) constructed Th as the automorphism group of a certain lattice in the **248-dimensional Lie algebra of E₈**.
- Th does **NOT** preserve the full Lie bracket, but **preserves the Lie bracket mod 3**.
- Therefore Th is a subgroup of the Chevalley group **E₈(3)** (E₈ over GF(3)).
- The subgroup of Th that preserves the full Lie bracket (over Z) is a maximal subgroup called the **Dempwolff group**, which IS a subgroup of the compact Lie group E₈.
- The connection to the Monster: Th × Z₃ is the centralizer of an element of **order 3** (class 3C) in the Monster.
- Via the Monster VOA, Th acts on a VOA **over the field with 3 elements**.

**Key dimensions:** dim(E₈) = **248** = Th's representation space.
**Key prime:** p = **3** (Th centralizes order-3 element in Monster).

**References:**
- Thompson, J.G. (1976). A conjugacy theorem for E₈. *J. Algebra* 38, 525–530.
- Smith, P.E. (1976). A simple subgroup of M? and E₈. *Bull. London Math. Soc.* 8, 161–165.
- [Thompson sporadic group — Wikipedia](https://en.wikipedia.org/wiki/Thompson_sporadic_group)

---

## 2. Harada-Norton HN and E₇ — STRONG DIMENSIONAL EVIDENCE, EMBEDDING NOT PROVEN

**Status: TANTALIZING BUT UNCONFIRMED as a direct Lie-algebraic embedding**

### What IS proven:
1. HN acts on a **133-dimensional algebra over GF(5)** with a commutative but nonassociative product (the "Norton algebra"), analogous to the Griess algebra.
2. The adjoint representation of E₇ has dimension **133**. This is the same number.
3. HN centralizes an element of **order 5** in the Monster, and acts on a VOA **over the field with 5 elements**.
4. 133×133 matrices over GF(5) generating HN have been explicitly constructed (Ryba & Wilson, 1994).
5. The ATLAS lists a 133-dimensional representation of HN over GF(5) (confirmed available).
6. HN also has 133-dimensional representations over GF(4), GF(9), GF(11), GF(19), GF(49) — so 133 is a fundamental dimension of HN across many characteristics, not just p=5.

### What is NOT proven (or found in the literature):
- **No source found** stating that HN is a subgroup of E₇(5) (E₇ Chevalley group over GF(5)).
- **No source found** stating that HN preserves the E₇ Lie bracket mod 5.
- **No source found** stating that the 133-dimensional Norton algebra is the E₇ adjoint restricted to HN.
- The Norton algebra is **commutative and nonassociative**; the E₇ Lie algebra is **anticommutative** (Lie bracket). These are different algebra structures on 133-dimensional spaces.

### The parallel would be:
| Group | Dimension | Prime | Monster centralizer | Chevalley embedding? |
|-------|-----------|-------|--------------------|--------------------|
| Th | 248 = dim(E₈) | 3 | C_M(3C) | Th ↪ E₈(3) ✓ PROVEN |
| HN | 133 = dim(E₇) | 5 | C_M(5A) | HN ↪ E₇(5)? **UNKNOWN** |

### Why the parallel is suggestive but not automatic:
- Th preserves the E₈ Lie bracket **mod 3** — this is a specific algebraic fact about how the lattice automorphisms interact with the Lie structure.
- For HN, the 133-dim algebra over GF(5) is Norton's commutative nonassociative algebra, **not** the E₇ Lie algebra reduced mod 5. Nobody appears to have checked whether HN preserves any E₇ Lie bracket structure.
- The Griess-Ryba classification (1999, 2002) classifies finite simple groups that **projectively embed** in exceptional Lie groups over **C** (complex numbers), not over finite fields. This classification may not address the finite-field question directly.

### Assessment:
The dimensional coincidence 133 = dim(E₇) combined with the structural parallel (order-5 centralizer in Monster, VOA over GF(5)) is **highly suggestive** but remains a **conjecture** as far as this search can determine. The critical question — does HN preserve the E₇ Lie bracket mod 5, making it a subgroup of E₇(5)? — appears to be **open or at least not widely published**.

**References:**
- Norton, S.P. (1975). Construction of HN.
- Harada, K. (1976). On the simple group F of order 2¹⁴ · 3⁶ · 5⁶ · 7 · 11 · 19. *Proc. Conf. Finite Groups*, 119–276.
- Ryba, A.J.E. & Wilson, R.A. (1994). Matrix generators for the Harada-Norton group. *Experimental Mathematics* 3(2), 137–145. [Project Euclid](https://projecteuclid.org/journals/experimental-mathematics/volume-3/issue-2/Matrix-generators-for-the-Harada-Norton-group/em/1062620907.full)
- [ATLAS: HN representations](https://brauer.maths.qmul.ac.uk/Atlas/spor/HN/)
- [Harada-Norton group — Groupprops](https://groupprops.subwiki.org/wiki/Linear_representation_theory_of_Harada-Norton_group)

---

## 3. Fischer Fi22 and E₆ — PROVEN (via twisted form ²E₆)

**Status: ESTABLISHED FACT (but via ²E₆, not E₆ directly)**

### What IS proven:
1. **Fi22 is a subgroup of ²E₆(2²)** (the twisted Chevalley group of type E₆ over GF(4)). This is well-documented and computationally verified.
2. The perfect **triple cover 3.Fi22** has an irreducible representation of dimension **27** over GF(4). This arises directly from the embedding in ²E₆(2²), since the minimal faithful representation of E₆ is the 27-dimensional minuscule representation.
3. Fi22 has an irreducible **real representation of dimension 78**. Note: dim(E₆) = **78**. Reducing an integral form mod 3 gives a 77+1 decomposition.
4. Fi22 was constructed by Bernd Fischer (1971, 1976) via **3-transposition theory**.
5. A new, explicit, elementary construction of Fi22 inside ²E₆(2²) was given in 2020.

### Important subtleties:
- The embedding is in **²E₆** (a **twisted** or Steinberg form of E₆), not in the split Chevalley group E₆. The group ²E₆(q²) is the quasi-split form depending on a quadratic extension of fields.
- ²E₆(2²) is sometimes written ²E₆(2) in some notations (e.g., Wilson's Atlas).
- The 27-dimensional representation of 3.Fi22 connects to the E₆ **minuscule** representation.

### The parallel:
| Group | Key dim | Construction | Chevalley embedding |
|-------|---------|-------------|-------------------|
| Th | 248 = dim(E₈) | Lattice in E₈ Lie alg | Th ↪ E₈(3) ✓ |
| HN | 133 = dim(E₇) | 133-dim algebra/GF(5) | HN ↪ E₇(5)? UNKNOWN |
| Fi22 | 78 = dim(E₆), 27 = fund(E₆) | 3-transpositions | Fi22 ↪ ²E₆(2²) ✓ |

### Assessment:
Fi22 ↪ ²E₆(2²) is proven. The twist (²E₆ vs E₆) is a genuine mathematical distinction — ²E₆ is related to E₆ but is a different group. The 27-dimensional representation of the triple cover connecting to E₆'s minuscule representation is a strong structural link. The 78-dimensional real representation matching dim(E₆) adds further evidence of deep connection.

**References:**
- Fischer, B. (1971). Finite groups generated by 3-transpositions. *Inventiones Math.* 13, 232–246.
- Fischer, B. (1976). Finite groups generated by 3-transpositions, II.
- [Fischer group Fi22 — Wikipedia](https://en.wikipedia.org/wiki/Fischer_group_Fi22)
- [Fischer group Fi22 — HandWiki](https://handwiki.org/wiki/Fischer_group_Fi22)
- [Fi22 — Groupprops](https://groupprops.subwiki.org/wiki/Fischer_group:Fi22)
- "A new existence proof of Fi22 in 2E6(2), a computational approach." *Communications in Algebra* 48(7), 2766–2780 (2020). [DOI](https://www.tandfonline.com/doi/abs/10.1080/00927872.2020.1722826)

---

## 4. The McKay Observations (different from embeddings!)

**IMPORTANT DISTINCTION:** The McKay E₈/E₇/E₆ observations are about **involution class structure**, not about subgroup embeddings. They are:

| Lie algebra | Sporadic group | McKay observation |
|------------|---------------|-------------------|
| E₈ | Monster M | Products of 2A involutions → 9 classes matching affine Ê₈ labels (1,2,3,4,5,6,4,2,3) |
| E₇ | Baby Monster B | Products of 2A involutions in 2.B → 8 classes matching affine Ê₇ labels (1,2,3,4,3,2,1,2) |
| E₆ | Fischer Fi₂₄' | Products of 2A involutions in 3.Fi₂₄' → 7 classes matching affine Ê₆ labels |

These connect **Monster/Baby/Fischer-24'** to E₈/E₇/E₆ — a **different** triple from the embedding triple (Th/HN?/Fi22).

The McKay observations have been given VOA-theoretic explanations:
- E₈: Höhn (2003), relating to Monster VOA V♮
- E₇: Höhn & Lam (2010), relating to Baby Monster VOA VB♮, via c=7/10 Virasoro vectors. [arXiv:1002.1777](https://arxiv.org/abs/1002.1777)
- E₆: Höhn & Lam (2010), relating to Fischer Fi₂₄' via 3-transposition property.

**References:**
- McKay, J. (1980). Graphs, singularities, and finite groups.
- Höhn, G. & Lam, C.H. (2010). "McKay's E₇ observation on the Baby Monster" and "McKay's E₆ observation on the largest Fischer group." [arXiv:1002.1777](https://arxiv.org/abs/1002.1777)
- He, Y.-H. & McKay, J. (2015). Sporadic and Exceptional. [arXiv:1505.06742](https://arxiv.org/abs/1505.06742)

---

## 5. Griess-Ryba Classification

Griess and Ryba (1999, 2002) classified finite simple groups that projectively embed in exceptional Lie groups **over C**.

- **Paper 1:** "Finite simple groups which projectively embed in an exceptional Lie group are classified!" *Bull. AMS* 36(1), 75–93 (1999). [AMS](https://www.ams.org/journals/bull/1999-36-01/S0273-0979-99-00771-5/)
- **Paper 2:** "Quasisimple finite subgroups of exceptional algebraic groups." *J. Group Theory* (2002).

This classification addresses embeddings in the **complex** exceptional Lie groups. The full table of which sporadics embed in which exceptionals was not found in the web search (would require accessing the paper directly), but key known results include:
- Th embeds in E₈(C) via the Smith lattice construction
- The Dempwolff group (maximal subgroup of Th) embeds in compact E₈

The classification over **finite fields** (Chevalley groups like E₈(3), E₇(5), etc.) is a related but different question.

---

## 6. J₁ and E₇ — DIMENSIONAL COINCIDENCE ONLY

**Status: NO KNOWN EMBEDDING**

- J₁ (Janko's first group) has smallest faithful complex representation of dimension **56**.
- E₇ has fundamental (minuscule) representation of dimension **56**.
- The Freudenthal triple system on which Aut = E₇ acts is 56-dimensional.
- J₁ embeds in G₂(11) via a 7-dimensional representation over GF(11).
- Since G₂ ⊂ E₇, there is a chain J₁ ↪ G₂(11) ↪ ... but this goes through G₂, not through the 56-dimensional representation.
- **No source found** connecting J₁'s 56-dim rep to E₇'s 56-dim fundamental.

The 56 is likely a coincidence. J₁ is a **pariah** (not in the Monster), so it lives outside the Monster-E₈ ecosystem entirely.

**References:**
- [Janko group J1 — Wikipedia](https://en.wikipedia.org/wiki/Janko_group_J1)
- [Linear representation theory of J1 — Groupprops](https://groupprops.subwiki.org/wiki/Linear_representation_theory_of_Janko_group:J1)

---

## 7. The Complete Picture: Two Distinct Sporadic-Exceptional Correspondences

There are actually **two separate** sporadic-exceptional correspondences in the literature:

### Correspondence A: McKay Observations (involution classes → affine Dynkin)
| Exceptional | Sporadic | Nature | Status |
|------------|----------|--------|--------|
| E₈ | Monster M | 2A products → Ê₈ labels | PROVEN (VOA) |
| E₇ | Baby Monster B | 2A products → Ê₇ labels | PROVEN (VOA) |
| E₆ | Fischer Fi₂₄' | 2A products → Ê₆ labels | PROVEN (VOA) |

### Correspondence B: Chevalley group embeddings (adjoint dim → sporadic)
| Exceptional | dim(adjoint) | Sporadic | Prime | Embedding status |
|------------|-------------|----------|-------|-----------------|
| E₈ | 248 | Th (Thompson) | 3 | **PROVEN**: Th ↪ E₈(3) |
| E₇ | 133 | HN (Harada-Norton) | 5 | **CONJECTURED/OPEN**: HN has 133-dim rep over GF(5) |
| E₆ | 78 | Fi22 (Fischer) | 2 | **PROVEN**: Fi22 ↪ ²E₆(2²) |

### Primes in Monster centralizers:
| Sporadic | Monster centralizer | Prime | adjoint dim |
|----------|-------------------|-------|-------------|
| Th | C_M(3C) = Th × Z₃ | 3 | 248 = dim(E₈) |
| HN | C_M(5A) = HN × Z₅ | 5 | 133 = dim(E₇) |
| Fi22 | subquotient of M | 2 | 78 = dim(E₆) |

The primes (3, 5, 2) and the adjoint dimensions (248, 133, 78) align across these three sporadic groups. This is the pattern your framework noticed.

---

## 8. Honest Assessment

### What is PROVEN:
1. **Th ↪ E₈(3)** — via Smith's lattice construction (1976). Rock solid.
2. **Fi22 ↪ ²E₆(2²)** — proven, computationally verified, new proof in 2020. Note the **twist** (²E₆, not E₆).
3. **HN has 133-dim rep over GF(5)** — proven, in ATLAS. The dimension matches E₇.
4. **McKay observations** for M/B/Fi₂₄' with E₈/E₇/E₆ — proven via VOA theory.

### What is NOT proven (but highly suggestive):
1. **HN ↪ E₇(5)** — the critical missing piece. The dimensional evidence is strong (133 = dim(E₇), p = 5 from Monster centralizer), and the parallel with Th ↪ E₈(3) is compelling, but **no paper found** establishing this embedding.
2. Whether the Norton 133-dim commutative nonassociative algebra over GF(5) is **related to** the E₇ Lie algebra mod 5. They are different algebra types (commutative vs anticommutative), so the connection, if any, would need to go through a different route (e.g., symmetric square, Jordan algebra, etc.).

### What would settle it:
- Check computationally whether HN, acting on a 133-dim space over GF(5), preserves any bilinear form compatible with the E₇ Lie bracket mod 5.
- Alternatively, check whether |HN| divides |E₇(5)| (the order of the Chevalley group E₇ over GF(5)).
- Consult the full Griess-Ryba (1999/2002) classification tables directly.

### For the framework:
The pattern Th/E₈(3) — HN/E₇(5)? — Fi22/²E₆(2²) with primes 3, 5, 2 is genuinely striking. Even if HN ↪ E₇(5) turns out not to hold as a strict group embedding, the dimensional correspondence 248/133/78 = dim(E₈)/dim(E₇)/dim(E₆) with the Monster centralizer primes 3/5/2 is a real mathematical pattern that deserves investigation.

The **2⁴⁶ partition** claim (Th(2¹⁵) + HN(2¹⁴) + Fi22(2¹⁷) = 2⁴⁶ from Monster order) would add another layer if verified, but this is a separate claim from the Lie-algebraic embeddings.

---

## Summary Table

| Question | Answer | Confidence |
|----------|--------|------------|
| Th ↪ E₈? | YES, via E₈(3) | **PROVEN** |
| HN ↪ E₇? | 133-dim rep exists over GF(5), but embedding in E₇(5) **not found** in literature | **OPEN/CONJECTURED** |
| Fi22 ↪ E₆? | YES, via ²E₆(2²) (twisted form) | **PROVEN** |
| J₁ and E₇(56-dim)? | Dimensional coincidence only, no embedding found | **UNLIKELY** |
| Norton algebra = E₇ adjoint? | Different algebra types (commutative vs Lie), not directly | **NO** (but may be related) |
| McKay observations | M↔E₈, B↔E₇, Fi₂₄'↔E₆ (different triple!) | **PROVEN** |
