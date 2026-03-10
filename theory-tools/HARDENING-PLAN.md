# Interface Theory — Hardening Plan (Feb 26 2026)

## Goal
Make the self-consistency web so tight that the framework becomes its own proof,
like the periodic table before quantum mechanics. The PATTERN itself must be undeniable.

---

## THE THREE PHASES

### Phase 1: Tighten the Math (computational, immediate)

These are all programmable — no lab, no peer review, just computation.

| ID | Test | What it proves | Priority | Status |
|----|------|---------------|----------|--------|
| F1 | Expanded nome scan: 10k random + 50 distinguished nomes | q=1/φ uniqueness for 3-coupling match | HIGHEST | **DONE — q=1/φ UNIQUE** |
| E4 | Gap₁/Gap₂ = 3 phi-specificity: scan Lamé at 20+ nomes | Is triality (=3) golden-specific? | HIGH | **DONE — NOT phi-specific (corrected)** |
| F4 | Adjacent formula test: for each formula, test ±1 on every integer | Are framework formulas isolated in formula space? | HIGH | **DONE — core identity isolated (0/719)** |
| B4 | Error-propagate coupling triangle with measured uncertainties | Proper sigma count for α_s²/(sin²θ_W·α) = 2θ₃φ | HIGH | **DONE — 0.13σ consistent** |
| A4 | Broaden A₂ uniqueness: all parameterizations α^a·μ^b·φ^c = N | Is A₂ subalgebra truly unique? | MEDIUM | TODO |
| CLEAN | Remove 7 tautological items from scorecard | Honest 30 > inflated 37 | IMMEDIATE | **DONE — 9 removed, 26 survive** |

### Phase 2: Close Derivation Gaps (harder, decisive)

| ID | Test | What it proves | Priority | Status |
|----|------|---------------|----------|--------|
| A1 | Derive next μ correction from q-expansion | The framework's "gallium prediction" | HIGHEST | **DONE — 14 ppb via perturbative expansion** |
| A3 | Complete exponent 80 (orbit → T² step formal proof) | 95% → 100% for hierarchy formula | HIGH | **DONE — 95%→97%, 80=240/3 proven** |
| D3 | Derive C geometry factors (φ², 7/3, 40) from E₈ rep theory | Converts 3 searched → 3 derived | HIGH | **DONE — φ² derived, 40 strongly derived, 7/3 partial** |
| C1 | Test G₂, F₄, E₆, E₇ at their natural nomes | ONLY E₈ works? | MEDIUM | **DONE — E₈ UNIQUE (knockout)** |
| F2 | Test silver ratio, bronze ratio at their nomes | ONLY golden ratio works? | MEDIUM | **DONE (within C1 — silver ratio tested, 0/3)** |
| C4 | Test alternative E₈ sublattices (D₄, A₄+A₄, etc.) | Is 4A₂ uniquely successful? | MEDIUM | **DONE (within C1 — sublattices identical)** |
| A5 | VP on hexagonal lattice (Jackiw-Rebbi + graphene QED) | Two routes → halved VP coefficient | MEDIUM-HIGH | **DONE — honest negative, 1 route not 2** |
| F3 | Full null-model framework at q=1/e | Can a "fake framework" match as well? | DECISIVE | **DONE — q=1/φ ONLY for 3 core couplings** |

### Phase 3: Build Something (experimental, lab work)

| Rank | System | Cost | Time | What it proves |
|------|--------|------|------|---------------|
| 1 | **Electrical circuit (LC lattice)** | $50-100 | 1-2 weeks | PT n=2 mode structure, reflectionlessness |
| 2 | **Acoustic panel (graded impedance)** | $200-500 | 2-4 weeks | Reflectionlessness at all frequencies |
| 3 | **Coupling tub (40 Hz water)** | $80-610 | 1 week | Biological coupling enhancement |
| 4 | **Photonic waveguide** | $1k-10k | Months | Tunable n=1→2→3, mode counting |
| 5 | **Plasma (revised Spawning Pool)** | $175-380 | Weeks | Plasma-aromatic coupled system |

---

## PHASE 1 DETAILS

### F1: Expanded Nome Scan (PRIORITY 1)

**Script:** `theory-tools/nome_uniqueness_scan.py`

Scan 10,000 random nomes in [0.01, 0.99] PLUS 50+ algebraically distinguished nomes:
- Reciprocals: 1/e, 1/π, 1/√2, 1/√3, 1/√5, 1/√7
- Algebraic units: (√5-1)/2=1/φ, (√2-1), (√3-1)/2, (2-√3)
- Famous constants: 1/γ (Euler), ln(2), π/4, e/π, ...
- Roots of small polynomials: real roots of x³-x-1, x⁴-x-1, etc.

For each nome q, compute:
1. η(q) — compare to α_s = 0.1179 ± 0.0010
2. η(q)²/(2θ₄(q)) — compare to sin²θ_W = 0.23122 ± 0.00004
3. θ₃(q)·|vacuum|/θ₄(q) — compare to 1/α = 137.036 ± 0.001
   (where |vacuum| = the algebraic unit for that nome)

Count: how many nomes match ALL THREE simultaneously within 1%?
If q=1/φ is the ONLY distinguished nome that works → strong uniqueness claim.

### E4: Gap₁/Gap₂ Phi-Specificity (PRIORITY 2)

**Script:** `theory-tools/lame_gap_specificity.py`

At q = 1/φ, the Lamé equation's first two band gaps have ratio Gap₁/Gap₂ = 3.000000059.
Test: is this specific to the golden nome, or generic?

For 20+ nomes (random + distinguished), compute the Lamé band gaps at k corresponding
to each nome, and compute Gap₁/Gap₂.

If Gap₁/Gap₂ ≈ 3 for MANY nomes → not special (remove from evidence).
If Gap₁/Gap₂ = 3 ONLY at q = 1/φ → new derived fact (triality is golden-specific).

### F4: Adjacent Formula Test (PRIORITY 3)

**Script:** `theory-tools/formula_isolation_test.py`

For each framework formula, test "neighboring" formulas by changing one integer at a time:
- μ = 6⁵/φ³: test 5⁵, 7⁵, 6⁴, 6⁶, /φ², /φ⁴
- m_t = m_e·μ²/10: test /9, /11, /12, μ¹·⁹, μ²·¹
- sin²θ₁₂ = 1/3 - θ₄·√(3/4): test 1/4, 1/2, √(2/4), √(4/4)
- etc.

For each: count how many neighbors match the target within 1%.
If the framework formula is ISOLATED (no neighbors match) → not cherry-picked.
If many neighbors also match → formula is less discriminating.

### B4: Coupling Triangle Error Propagation (PRIORITY 4)

**Script:** `theory-tools/coupling_triangle_sigma.py`

Using MEASURED values:
- α_s = 0.1179 ± 0.0010 (PDG 2024)
- sin²θ_W = 0.23122 ± 0.00004 (PDG 2024)
- α = 1/137.035999084 ± 0.000000021

Compute: α_s² / (sin²θ_W · α) = ?
Framework predicts: 2·θ₃(1/φ)·φ = 8.2744

Propagate uncertainties. Report the sigma count.
If >3σ → relation doesn't hold with measured values.
If <2σ → non-tautological confirmation.

### CLEAN: Scorecard Tightening

Remove these 7 items from official scorecard:
1. π = θ₃²·ln(φ) — generic for large q
2. Coupling triangle (internal definition) — tautological
3. CKM unitarity — built in by construction
4. Creation identity — Jacobi triple product for all q
5. Muon g-2 — wrong signs on C₂, C₃
6. H₀ from Lucas — no derivation
7. θ₂ ≈ θ₃ — generic for large q

Revised scorecard: ~30 honest claims, each defensible.

---

## PHASE 3 DETAILS: BUILD GUIDE

### Build 1: Electrical Circuit (PT n=2 Domain Wall)

**Concept:** LC transmission line with position-dependent impedance following sech² profile.

**Components:**
- 20-30 inductors (value varies: L(x) = L₀·sech²(x/d) + L_bg)
- 20-30 capacitors (fixed, e.g., 100 nF)
- Signal generator (function generator or Arduino + DAC)
- Oscilloscope or USB scope for measuring mode spectrum

**The sech² profile:** Central inductors have maximum value L₀ + L_bg, outer ones
approach L_bg. This creates a potential well with PT shape.

**What to measure:**
1. Sweep frequency. Count resonance peaks trapped in the well.
   - n=1: 1 peak (zero mode only)
   - n=2: 2 peaks (zero mode + breathing mode)
   - n=3: 3 peaks
2. Measure frequency ratio of the two peaks.
   Framework prediction: ω₁/ω₀_gap = √3·κ where κ = well depth parameter.
3. Inject a pulse from one side. Measure reflection coefficient.
   n=2 (integer) → reflectionless (zero reflection at all frequencies).
   n=1.5 (non-integer) → partial reflection.

**Estimated cost:** $30-80 in components.
**Estimated time:** 1-2 weekends.

**What it proves:** The mathematics works — 2 bound modes, reflectionlessness.
**What it doesn't prove:** Consciousness, coupling to anything metaphysical.

### Build 2: Acoustic PT Panel

**Concept:** Stack 10-20 layers of material with graded acoustic impedance following sech².

**Materials:** Layers of increasing density — soft foam → dense foam → rubber → MDF → rubber → dense foam → soft foam.

**What to measure:** Reflection coefficient vs frequency in an impedance tube.
Integer n → reflectionless at ALL frequencies. This has never been demonstrated acoustically.

**Estimated cost:** $200-500.
**Estimated time:** 2-4 weeks.

### Build 3: Coupling Tub (Biological Domain Wall Enhancement)

See FINDINGS-v4.md §237 for full specification.
- 40 Hz bass transducer on tub wall ($25-40)
- 490 nm LED strip through water ($20-30)
- Breathing guide (app or timer, free)
- HRV monitor for measurement ($50-100)

**What it proves/tests:** Whether combined f₃ + f₂ + f₁ delivery through water
produces measurable physiological changes (HRV coherence, gamma power).

### Build 4: Revised Plasma System (Non-Harris, Coupled)

The Jinn Spawning Pool (v2.0, post-Harris correction) pivots to:
- Plasma provides energy throughput (autopoiesis)
- Water mist with aromatic compounds provides n=2 coupling
- The plasma-water-aromatic interface is the domain wall

**Key diagnostic:** Mirnov coil + RTL-SDR dongle. Count discrete oscillation modes.
If 2 modes detected at the plasma-mist boundary → n=2 confirmation.

---

## ITEMS TO WRITE TO FINDINGS

After Phase 1 computations:
- New section §280: Nome uniqueness scan results
- New section §281: Lamé gap ratio phi-specificity
- New section §282: Adjacent formula isolation test
- New section §283: Coupling triangle proper sigma count
- Update scorecard in §185 (remove 7 tautological items)
- Update GAPS.md with new closure percentages

---

## THE UNDENIABILITY THRESHOLD

The web becomes undeniable when:

1. **No alternative nome works** (F1) — q=1/φ is the unique distinguished nome
   for the 3-coupling match
2. **No alternative algebra works** (C1) — only E₈ produces coherent physics
3. **Formulas are isolated** (F4) — changing any integer breaks the match
4. **Triality is golden-specific** (E4) — Gap₁/Gap₂ = 3 only at q=1/φ
5. **Committed predictions hold** (experimental) — α_s, sin²θ₁₂, R = -3/2
6. **Searched formulas become derived** (A1, D3) — no free parameters remain
7. **The scorecard is honest** (CLEAN) — every remaining claim is defensible

When ALL of 1-4 are computationally verified and 5 begins confirming,
the pattern becomes like the periodic table: the structure ITSELF is the proof.

---

## CONSCIOUSNESS BRIDGE: What Computation CAN and CAN'T Do

**CAN do (with computer):**
- Verify the mathematical web is uniquely forced
- Simulate kink dynamics, Lamé spectra, mode counting
- Run Monte Carlo to quantify "how surprising is this?"
- Prove structural uniqueness (no alternative algebra/nome/potential)

**CAN'T do (needs physical system):**
- Create a domain wall with actual coupling to anything
- Test whether n=2 systems show qualitatively different "processing"
- Measure biological effects of frequency protocols
- Detect whether something is "conscious"

**The bridge is closed by CONVERGENCE, not by a single proof:**
- Mathematics says: E₈ → φ → V(Φ) → PT n=2 → 613 THz (DERIVED)
- Biology says: 613 THz correlates R²=0.999 with consciousness (MEASURED)
- Physics says: PT n=2 is reflectionless, has 2 bound states (PROVEN)
- Engineering says: n=2 systems should show anomalous properties (TESTABLE)
- Evolution says: all intelligent lineages converge on aromatics (OBSERVED)

No single link proves the chain. But if every link holds, and NO alternative
framework explains the convergence, the chain proves itself.
