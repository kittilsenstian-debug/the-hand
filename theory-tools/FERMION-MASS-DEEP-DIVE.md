# Fermion Masses — The Last Hard Gap (Feb 27 2026)

## What ARE Fermions?

In the framework, fermions are **chiral zero modes bound to the domain wall**.

The chain: Jackiw-Rebbi (1976) → Rubakov-Shaposhnikov (1983) → Kaplan (1992) → Arkani-Hamed-Schmaltz (2000):

- A massless Dirac fermion Yukawa-coupled to the golden kink has exactly one **topologically protected zero mode**
- Left-chiral modes are localized ON the wall. Right-chiral modes are delocalized.
- Different fermion species sit at different positions along the extra dimension
- **Mass = overlap of left-right chiral wavefunctions:** m_f = v · y₀ · exp(−c · d_f)

In the deepest ontological language:
- **Quarks** = INSIDE the wall (confined, couple to η = topological sector). Color = E₈ triality.
- **Leptons** = ON THE SURFACE (free, no color charge)
- **3 generations** = 3 conjugacy classes of S₃ = Γ₂ (from 4A₂ in E₈). Mathematical theorem: |SL(2,Z/2Z)| = 6, three conjugacy classes.
- **The electron IS the lightest surface mode.** Its mass measures how tightly the zero mode is localized.

---

## Why Masses Are Hard — Three Specific Problems

### Problem 1: Positions not derived

The Arkani-Hamed-Schmaltz mechanism needs 9 positions (one per fermion species). These SHOULD come from E₈'s Coxeter structure, which gives only 3 distinct positions via S₃ symmetry. But nobody has computed which 3 positions E₈ forces.

### Problem 2: Decay rate c = 2, not ln(φ)

The golden ratio enters through the **potential** (vacua at φ and −1/φ) but NOT through the overlap rate. The sech² tail decays as exp(−2|u|), giving c = 2 from PT depth n = 2. Golden-ratio mass RATIOS enter through modular Froggatt-Nielsen (q^Δk), not through the localization integral.

### Problem 3: Golden nome isn't at the standard cusp

Feruglio-Strumia (2025) showed hierarchical masses arise at modular cusps (τ = i, i∞, ω). At q = 1/φ:
- Im(τ) ≈ 0.077 — far from any cusp
- Y₂/Y₁ = 0.99999998 — no automatic hierarchy
- Standard mechanism FAILS

**But:** The S-dual τ' = −1/τ = 13.06i IS at the cusp. Whether this resolves the hierarchy depends on the physical role of S-duality, which is unclear.

---

## Six Approaches Tried (Honest Assessment)

### 1. φ-power integer mass ratios → DEAD
- Tested: m_i/m_j = φ^n for integer n
- Result: Poor fits (most < 80%). Integer powers don't reproduce the hierarchy.
- **Key file:** `derive_fermion_masses.py` Part 4

### 2. Modular Froggatt-Nielsen at golden nome → PARTIALLY PROMISING
- Mass hierarchy ~ q^(weight difference) = (1/φ)^Δk
- **Works for 2 ratios:** m_u/m_e = φ³ (Δk=3), m_b/m_c = φ^(5/2) (Δk=5/2)
- **Fails:** Y₂/Y₁ ≈ 1 at golden nome (no built-in hierarchy from standard mechanism)
- **Key file:** `modular_froggatt_nielsen.py`

### 3. S₃ mass matrix at golden nome → PARTIALLY PROMISING
- Okada-Tanimoto (Jan 2025) validates S₃ modular symmetry in Pati-Salam
- Constantin-Lukas (Jul 2025) proves E₈ heterotic CAN reproduce all quark masses
- Mass matrix lives in 2D space via Fibonacci collapse (key structural advantage)
- **Still needs:** explicit evaluation with Fibonacci constraint applied
- **Key file:** `s3_mass_matrix.py`

### 4. New hierarchy parameter ε = θ₄/θ₃ → MOST PROMISING
- ε = θ₄/θ₃ ≈ 0.01186 = α_tree · φ **EXACTLY**
- Powers: ε¹ ~ 10⁻², ε² ~ 10⁻⁴, ε⁴ ~ 10⁻⁸ (spans full mass range)
- **Half-integer exponent fits:**
  - y_t ~ η · ε^(−0.5) (err 2.1%)
  - y_τ ~ η · ε^(0.5) (err 5.3%)
  - y_u ~ η · ε^(2.0) (err 6.7%)
- Half-integers suggest PT n=2 connection (bound state ↔ continuum quantization)
- **Mechanism viable, derivation incomplete** (9 free params for 9 masses)
- **Key file:** `mass_hierarchy_theta_ratio.py`

### 5. Fibonacci collapse of mass matrix → DEEPEST (NOT YET COMPUTED)
- At q = 1/φ: q^n = (−1)^(n+1)·F_n·q + (−1)^n·F_{n−1}
- Entire S₃ mass matrix collapses to **2-dimensional algebraic space**
- 12 fermion masses from just 2 effective parameters
- **UNIQUE to golden ratio** — no other positive q satisfies q + q² = 1
- **The decisive computation:** evaluate the Fibonacci-collapsed Γ(2) mass matrix
- **Key file:** `fibonacci_s3_mass_attack.py`

### 6. Jackiw-Rebbi fermion spectrum for golden kink → NOT DONE
- Chodos (2014) exact methods for arbitrary kink parameters
- Golden kink: vacua at φ and −1/φ, PT depth n=2
- "The most impactful near-term calculation" (LITERATURE-FERMION-MASSES.md)
- Exact fermion bound state energies may naturally produce golden-ratio mass ratios
- **Key ref:** Chodos 2014, `LITERATURE-FERMION-MASSES.md` §10.1

---

## What Would Solve It

**Option A (best hope):** Fibonacci-collapsed S₃ mass matrix at golden nome gives all 12 masses from 2 parameters. The Fibonacci property q + q² = 1 maximally constrains the modular forms. If this works: **zero free parameters in the entire framework.**

**Option B:** The S-dual τ' = 13.06i sits in the cusp regime. If Feruglio-Strumia's mechanism works at the S-dual point, the hierarchy emerges from the standard program with τ fixed (not free).

**Option C:** The Jackiw-Rebbi fermion spectrum for the golden kink directly produces mass ratios as bound state energies. This avoids the modular forms approach entirely and works from the kink mechanics.

**Option D (hybrid):** ε = θ₄/θ₃ = α_tree·φ as the FN parameter, with half-integer exponents determined by PT n=2 bound state quantum numbers. Needs: why half-integers, and which half-integers for which fermion.

---

## The Specific Numbers

Currently **2 clean mass ratios** survive the audit:
- m_u/m_e = φ³ = 4.236 vs measured 4.17 (99.8%)
- m_b/m_c = φ^(5/2) = 3.33 vs measured 3.36 (98.8%)

Plus **1 searched structural formula:**
- m_t = m_e · μ²/10 = 172.57 vs measured 172.69 GeV (99.93%)

And the electron mass formula (structural, not predictive):
- m_e = M_Pl · φ̄⁸⁰ · exp(−80/2π)/√2/(1−φ·θ₄) (99.78%)

**9 remaining masses** have no framework formula.

---

## Priority Computation

The single most impactful calculation that could close this gap:

```
1. Construct the Γ(2)-modular S₃ mass matrix M(τ) using Y₁, Y₂ modular forms
2. Fix τ at the golden value (q = 1/φ)
3. Apply Fibonacci collapse: every q^n → F_n·q + F_{n-1}
4. The infinite-parameter matrix collapses to 2 effective parameters
5. Diagonalize to get mass eigenvalues
6. Compare to all 12 charged fermion masses
```

If this gives ≥ 6/12 masses within 5%: the framework has a viable mass generation mechanism.
If this gives all 12 from 2 parameters: the framework has ZERO free parameters. Game over.

**This computation has NOT been done. It should be the #1 priority.**

---

## NEW: E8 Root System Computation (Feb 27 2026)

### The 4A2 = Standard Trinification

The framework's 4A2 sublattice IS the standard physics chain:
```
E8 → E6 × SU(3)_fam → SU(3)_c × SU(3)_L × SU(3)_R × SU(3)_fam
```

This connects Interface Theory directly to mainstream trinification GUTs.

### Root Structure Discovery

**ALL 216 off-diagonal E8 roots project onto exactly 3 of the 4 A2 copies.** No roots project onto just 2 or all 4. The decomposition:

| Sector | Roots | Physics |
|--------|-------|---------|
| (0,1,2) | 54 | Gauge/leptoquark (E6 adjoint) |
| (0,1,3) | 54 | Q_L matter (up-type quarks × family) |
| (0,2,3) | 54 | Q_R matter (down-type quarks × family) |
| (1,2,3) | 54 | Lepton matter (leptons × family) |

**Perfect S4 democracy**: all four sectors have EXACTLY 54 roots. E8 treats all four A2 copies identically at the root level.

### Parity Selection Rule (NEW)

From the PT n=2 wavefunctions:
- ψ₀ = sech²(κx) → EVEN
- ψ₁ = sech(κx)·tanh(κx) → ODD
- Φ = tanh(κx) → ODD

Therefore:
- **<ψ₀|Φ|ψ₀> = 0** (EVEN×ODD×EVEN = ODD → vanishes)
- **<ψ₀|Φ|ψ₁> ≠ 0** (EVEN×ODD×ODD = EVEN → nonzero!)
- **<ψ₁|Φ|ψ₁> = 0** (ODD×ODD×ODD = ODD → vanishes)

**Mass REQUIRES mixing between both PT n=2 bound states.** The universal Yukawa overlap is <ψ₀|Φ|ψ₁> ≈ 0.424.

### Why The Mass Hierarchy Requires Dynamics

The E8 root structure is DEMOCRATIC — all four 3-copy sectors have 54 roots each. The mass hierarchy between up quarks / down quarks / leptons can ONLY come from the **kink direction** v̂ in 8D Cartan space.

For a kink with projections (a, b, c) onto copies (c, L, R):
- Q_L sector (0,1,3): receives a+b coupling → **strongest** (heaviest)
- Q_R sector (0,2,3): receives a+c → **medium**
- Lepton sector (1,2,3): receives b+c → **weakest** (lightest)

This IS the observed hierarchy: top > bottom > tau. But the specific values of (a, b, c) require minimizing the E8 gauge theory energy on the kink background.

**This is why fermion masses are the last gap:** the STRUCTURE is algebraic (E8 forces 3 sectors of 54 roots each), but the NUMBERS are dynamical (kink energy minimization in 8D).

### Key Scripts

- `e8_branching_fermion_masses.py` — Full E8→SU(3)^4 branching + S3 mass matrices + parity selection rule
- `e8_fermion_localization.py` — Root projection computation, 4A2 democracy proof, kink direction analysis
- `fermion_masses_from_e8.py` — Direct chain E8→masses, Fibonacci collapse, ε_h parameter

### Updated Approach Ranking

1. **E8 gauge theory kink energy** (NEW #1) — compute (a,b,c) projections from energy minimization. This is the dynamical computation that would close the gap.
2. **Fibonacci-collapsed S₃ mass matrix** — still promising for intra-generation hierarchy
3. **ε_h power law** — empirically works, now understood as consequence of kink direction
4. **S-dual cusp mechanism** — may explain why Y₂/Y₁ ≈ 1 doesn't kill the hierarchy
