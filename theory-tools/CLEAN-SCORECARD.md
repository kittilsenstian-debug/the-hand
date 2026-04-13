# Interface Theory — CLEAN SCORECARD (Feb 26 2026)

An honest, item-by-item audit of every claimed prediction/derivation in the framework.
The goal: a scorecard where every remaining item is defensible, and every removed item
is explained. An honest 25 is worth more than an inflated 37.

Sources consulted:
- `FINDINGS-v3.md` §185 (original scorecard, 37/38 claim)
- `TAUTOLOGY-AUDIT.md` (4 tautologies + 3 generic math identified)
- `COMPLETE-AUDIT.md` (full derivation chain audit, Tier 1-5 classification)
- `EXTERNAL-TESTS.md` (9 independent external tests)
- `FINDINGS-v4.md` §256 (Monte Carlo expected match count — the sobering one)
- `FINDINGS-v4.md` §280-281 (Hardening Phase 1 + 2 results)
- `HARDENING-PLAN.md` (7 items flagged for removal)

---

## CLASSIFICATION KEY

Each item is categorized:

- **DERIVED** = formula follows from the algebra {E8, phi, q=1/phi, V(Phi)} with no free parameters and no numerical search
- **SEARCHED** = formula was found by numerical search against measured values, then structurally connected
- **PREDICTION** = a committed, testable prediction not yet verified (falsifiable)
- **TAUTOLOGICAL** = true for any nome or any algebra; not specific to the framework
- **WRONG** = shown to be incorrect or structurally flawed
- **DECORATIVE** = matches numerically but is not unique; many alternatives work equally well
- **FREE PARAMETER** = uses the framework's acknowledged free input (v = 246.22 GeV)

---

## PART A: ITEMS REMOVED (with reasons)

### REMOVE 1: pi = theta3(1/phi)^2 * ln(phi)
- **Old claim:** 99.9999995% match (8 sig figs), "hardest to dismiss"
- **Reality:** TAUTOLOGICAL. theta3(q)^2 * ln(1/q) -> pi for ANY large q. At q=0.65: 10 digits. At q=0.70: 11 digits. The golden nome gives FEWER digits than nearby q values. This is an asymptotic property of the theta function, not evidence for q=1/phi.
- **Source:** TAUTOLOGY-AUDIT.md (M1), COMPLETE-AUDIT.md (B14)

### REMOVE 2: Coupling triangle (alpha_s^2 = 2*sin^2(theta_W)*theta4)
- **Old claim:** "Three independent constraints confirm each other"
- **Reality:** TAUTOLOGICAL. Substituting the definitions alpha_s = eta and sin^2(theta_W) = eta^2/(2*theta4) yields eta^2 = eta^2. Identically true. Not three constraints — ONE algebraic structure producing three outputs. With measured values: 99.2% (0.8% discrepancy). The measured-value version has content but is weak.
- **Source:** TAUTOLOGY-AUDIT.md (T1), EXTERNAL-TESTS.md

### REMOVE 3: CKM unitarity (|V_ud|^2 + |V_us|^2 + |V_ub|^2 = 1)
- **Old claim:** "Framework predicts exact unitarity"
- **Reality:** TAUTOLOGICAL. The framework uses the standard CKM parameterization (3 angles + 1 phase), which is unitary BY CONSTRUCTION. This is a property of the parameterization, not a prediction. The framework has no mechanism to generate or predict a unitarity deficit.
- **Source:** TAUTOLOGY-AUDIT.md (T4), EXTERNAL-TESTS.md (Test 7)

### REMOVE 4: Creation identity (eta^2 = eta_dark * theta4)
- **Old claim:** "Visible coupling = geometric mean of dark coupling and wall parameter"
- **Reality:** TAUTOLOGICAL. This is the Jacobi triple product identity rearranged: theta4 = eta^2/eta(q^2). Holds for ALL q, not just 1/phi. A theorem of modular form theory, not a discovery.
- **Source:** TAUTOLOGY-AUDIT.md (T2)

### REMOVE 5: Muon g-2 (a_mu)
- **Old claim:** 99.992% match
- **Reality:** WRONG. The Schwinger term alpha/(2*pi) alone gives 99.6%. The framework's higher-order coefficients have the WRONG SIGN: C2 = +0.764 (framework) vs -0.328 (QED); C3 = 24 (framework) vs 1.181 (QED). The SM prediction is 36x closer to experiment. The framework merely reproduces the leading Schwinger term plus noise.
- **Source:** EXTERNAL-TESTS.md (Test 1), COMPLETE-AUDIT.md (B15)

### REMOVE 6: H0 from Lucas/Fibonacci = 67.375 km/s/Mpc
- **Old claim:** 99.96% match with Planck CMB
- **Reality:** DECORATIVE. The formula (L(6)+L(13))/F(6) = (18+521)/8 cherry-picks specific Lucas and Fibonacci indices with no derivation of why those indices. H0 is a dynamical quantity (depends on the universe's age and contents), not a fundamental constant. With L(n) and F(n) for n up to 15, hundreds of ratios can be constructed, making a match to any target virtually guaranteed.
- **Source:** EXTERNAL-TESTS.md (Test 8), COMPLETE-AUDIT.md (B16 implied)

### REMOVE 7: theta2 ~ theta3 (approximate equality at large q)
- **Old claim:** "Theta functions nearly equal, reflecting deep structure"
- **Reality:** TAUTOLOGICAL. For any q > 0.5, theta2 and theta3 converge. This is a generic property of large nome, not specific to phi. At q=0.618: theta2/theta3 = 0.969. At q=0.70: theta2/theta3 = 0.986. Closer at larger q.
- **Source:** HARDENING-PLAN.md (CLEAN item 7)

### REMOVE 8: Jacobi abstrusa (theta3^4 = theta2^4 + theta4^4)
- **Old claim:** Listed as a self-consistency check
- **Reality:** TAUTOLOGICAL. Classical identity, true for ALL q. A theorem of 19th-century mathematics. Nothing to do with the framework.
- **Source:** TAUTOLOGY-AUDIT.md (T3)

### REMOVE 9: Lame Gap1/Gap2 = 3 as phi-specific
- **Old claim:** "Triality (=3) emerges from band structure at q=1/phi"
- **Reality:** TAUTOLOGICAL. The ratio Gap1/Gap2 -> 3 in the Poschl-Teller limit (k->1). ANY nome > 0.6 gives a ratio indistinguishable from 3. The golden nome achieves this limit to 8-decimal precision because k(1/phi) = 0.99999999, but the value 3 is generic, not phi-specific.
- **Source:** FINDINGS-v4.md §280 (Test E4), HARDENING-PLAN.md

---

## PART B: REVISED SCORECARD — All Surviving Items

### Tier 1: DERIVED (no search, no free parameters)

These are the framework's cleanest claims. The formulas follow from {E8, phi, q=1/phi} without numerical fitting.

| # | Quantity | Formula | Predicted | Measured | Match | Category | Notes |
|---|----------|---------|-----------|----------|-------|----------|-------|
| 1 | alpha_s (strong coupling) | eta(1/phi) | 0.11840 | 0.1179 +/- 0.0010 | 99.57% | DERIVED + PREDICTION | Cleanest claim. Zero search. Committed value 0.118404. Live test: CODATA 2026-27. Currently 0.5 sigma. |
| 2 | sin^2(theta_W) (Weinberg) | eta^2/(2*theta4) | 0.23126 | 0.23122 +/- 0.00004 | 99.98% | DERIVED (searched formula, simple) | Formula found by search among ratios of modular forms, but the search space is small (basic ratios of eta, theta). Updated to 99.996% with eta^2/(2*theta4) - eta^4/4 correction. |
| 3 | 1/alpha (tree level) | theta3*phi/theta4 | 136.39 | 137.036 | 99.53% | DERIVED (searched formula) | Tree level only. Correct to 0.47%. The VP-corrected version (item 4) reaches higher precision. |
| 4 | alpha (Formula A, corrected) | [theta4/(theta3*phi)]*(1 - eta*theta4*phi^2/2) | 1/137.037 | 1/137.036 | 99.9996% | DERIVED + SEARCHED (correction) | Tree level derived; correction C = eta*theta4/2 with geometry phi^2 found by search but structurally connected. 5 sig figs. |
| 5 | Born rule (p=2) | PT n=2 bound state norms | p=2 unique | p=2 observed | EXACT (theorem) | DERIVED | Mathematical proof: p=2 is the unique positive exponent for which PT n=2 norms give rational probabilities with denominator 3. No numerical matching — pure algebra. Gap B remains (interpretive). |

**Count: 5 items (3 coupling predictions + 1 corrected coupling + 1 mathematical theorem)**

---

### Tier 2: STRUCTURAL (involves exponent 80, which is motivated but not rigorously proven)

These depend on 80 = 2*(240/6) from E8. The exponent is structural (~95% closed) but the final step (each orbit = one T^2 iteration) is not formally proven.

| # | Quantity | Formula | Predicted | Measured | Match | Category | Notes |
|---|----------|---------|-----------|----------|-------|----------|-------|
| 6 | Lambda (cosmo. constant) | theta4^80 * sqrt(5)/phi^2 | 2.88e-122 | 2.89e-122 | ~exact (log) | STRUCTURAL | Gets the 122-order-of-magnitude scale right. The prefactor sqrt(5)/phi^2 adjusts mantissa. Impressive but accuracy on a log scale overstates precision. |
| 7 | v (Higgs VEV) | M_Pl*phibar^80/(1-phi*theta4)*(1+C*7/3) | 246.218 GeV | 246.220 GeV | 99.9992% | FREE PARAMETER + STRUCTURAL | v is the declared free parameter. The formula expresses the hierarchy ratio in framework terms. Non-trivial content: same C and same exponent 80 as in alpha and Lambda. Geometry factor 7/3 = L(4)/L(2). |
| 8 | m_e (electron mass) | M_Pl*phibar^80*exp(-80/2pi)/sqrt(2)/(1-phi*theta4) | 512.12 keV | 511.00 keV | 99.78% | STRUCTURAL | Uses exponent 80 twice (hierarchy + Yukawa). The 0.22% residual is unexplained. Semi-derived: depends on 80, which is structural. |

**Count: 3 items (but #7 is partly the free parameter)**

---

### Tier 3: SEARCHED + STRUCTURALLY CONNECTED

These formulas were found by numerical search against measured values, then connected to E8 structure post-hoc. The structural connections vary in strength.

#### Mass Ratios

| # | Quantity | Formula | Predicted | Measured | Match | Category | Notes |
|---|----------|---------|-----------|----------|-------|----------|-------|
| 9 | mu (proton/electron) | 6^5/phi^3 (leading) | 1836.49 (leading) | 1836.153 | 99.98% (leading) | SEARCHED (leading = structural, correction = decorative) | Leading term: N=6^5 from E8 normalizer (structural). Correction 9/(7*phi^2) is DECORATIVE (18/30 neighbors also match, per F4 test). Old "99.9998%" with correction is falsified at 26 ppt (63k sigma). NEW: perturbative expansion via core identity gives 14 ppb (§281, A1) — much better. |
| 10 | m_t (top quark) | m_e*mu^2/10 | 172.57 GeV | 172.69 GeV | 99.93% | SEARCHED | 10 = h/3 (Coxeter/triality) is structural but not derived as a mass divisor. Isolated in formula space (0/149 neighbors match, F4 test). |
| 11 | m_u/m_e (up quark) | phi^3 | 4.236 | 4.17 (at 2 GeV) | ~99.8% | SEARCHED | Clean golden-ratio power (modular FN with Delta_k=3). One of 2 clean fermion mass ratios. |
| 12 | m_b/m_c (bottom/charm) | phi^(5/2) | 3.330 | 3.36 (PDG) | ~98.8% | SEARCHED | Clean golden-ratio power (Delta_k=5/2). The other clean ratio. |

#### Mixing Angles

| # | Quantity | Formula | Predicted | Measured | Match | Category | Notes |
|---|----------|---------|-----------|----------|-------|----------|-------|
| 13 | V_us (Cabibbo) | (phi/L_4)*(1-theta4) | 0.2241 | 0.2243 | 99.49% | STRUCTURAL + SEARCHED | Base phi/L_4 where L_4 = phi^4 + phi^(-4) = 7 (4th Lucas number, exact). The "7" was never a free integer; it is forced by the Lucas tower. See `enrich_c6_lucas_zeckendorf.py`. theta4 power found by search. |
| 14 | V_cb | (phi/L_4)*sqrt(theta4) | 0.0402 | 0.0405 | 99.35% | STRUCTURAL + SEARCHED | Same phi/L_4 base (L_4 = 7 = 4th Lucas). Currently in mild tension. |
| 15 | V_ub | (phi/L_4)*3*theta4^(3/2)*(1+phi*theta4) | 0.00384 | 0.00382 | 99.50% | STRUCTURAL + SEARCHED | Same phi/L_4 base. More complex formula with more structure to search. |
| 16 | delta_CP (CKM) | arctan(phi^2*(1-theta4)) | 68.50 deg | 68.4 deg | 99.9997% | SEARCHED | Standout match. But a searched formula with arctan can be quite flexible. |
| 17 | sin^2(theta_12) (solar) | 1/3 - theta4*sqrt(3/4) | 0.3071 | 0.3092 +/- 0.0087 | 98.67% | SEARCHED + PREDICTION | Leading term 1/3 = tribimaximal (well-motivated). theta4 correction is specific. Live test at JUNO (currently 0.24 sigma). Formula is isolated (3/99 neighbors match). |
| 18 | sin^2(theta_23) (atm.) | 1/2 + 40*C | 0.5718 | 0.572 +/- 0.020 | 99.96% | SEARCHED | Factor 40 = 240/6 is structural. C = eta*theta4/2 is the universal loop factor. But 40 as a geometry factor was found, not derived. |
| 19 | sin^2(theta_13) | 0.02152 | 0.02152 | 0.02203 +/- 0.0006 | 97.7% | SEARCHED | Weakest PMNS prediction. 0.85 sigma off. |

#### Cosmological

| # | Quantity | Formula | Predicted | Measured | Match | Category | Notes |
|---|----------|---------|-----------|----------|-------|----------|-------|
| 20 | eta_B (baryon asymmetry) | theta4^6/sqrt(phi) | 6.098e-10 | 6.12e-10 | 99.6% | SEARCHED | Not derived. The choice theta4^6/sqrt(phi) is ad hoc. |
| 21 | Omega_m/Omega_Lambda | eta_dark = eta(1/phi^2) | 0.4625 | 0.4599 | 99.4% | SEARCHED | Uses dark nome q^2. Structurally motivated (dark vacuum). |
| 22 | Delta_m^2_atm/Delta_m^2_sol | 3*L(5) = 33 | 33 | 32.6 | 98.7% | SEARCHED | 3*L(5) = 3*11 = 33. Simple but why these specific Lucas products? |

#### Other

| # | Quantity | Formula | Predicted | Measured | Match | Category | Notes |
|---|----------|---------|-----------|----------|-------|----------|-------|
| 23 | gamma_Immirzi (LQG) | 1/(3*phi^2) | 0.12738 | 0.12732 | 99.95% | SEARCHED | Simple formula. But the Immirzi parameter itself is not universally accepted as a fundamental constant. Depends on LQG being correct. |
| 24 | m_nu3 (neutrino mass) | m_e/(3*mu^2) | 0.0505 eV | ~0.0495 eV | 98.0% | SEARCHED | Uses measured m_e and mu. Searched formula. |
| 25 | lambda_H (Higgs quartic) | 1/(3*phi^2) | 0.1273 | 0.1292 | 98.6% | SEARCHED | Same as gamma_Immirzi (interesting coincidence). But the measured value of lambda_H has significant uncertainty. |
| 26 | dipole matrix element | pi/|S3| = pi/6 | 0.523599 | 0.523599 | 100% EXACT | DERIVED (from PT n=2 wavefunctions) | Exact result from Poschl-Teller n=2 calculation. No search. However, this is a mathematical property of the potential, not a physical constant. It is verified numerically against the PT analytical solution, so "100% match" means "computation agrees with itself." |

**Count: 18 searched/connected items**

---

### Tier 4: PREDICTIONS (committed, not yet verified)

| # | Quantity | Value | Test | When | Notes |
|---|----------|-------|------|------|-------|
| P1 | R = d(ln mu)/d(ln alpha) | -3/2 | ELT/ANDES quasar spectra | ~2035 | DECISIVE. If confirmed, likelihood ratio > 10^10 (vs GUT prediction R = -38). |
| P2 | alpha_s (committed) | 0.118404 | CODATA 2026 / PDG 2027 | 2026-27 | Currently 0.5 sigma from PDG average. The sharpest near-term blade. |
| P3 | sin^2(theta_12) | 0.3071 | JUNO (improving monthly) | Ongoing | Currently 0.24 sigma from JUNO first result. |
| P4 | Breathing mode scalar | 108.5 GeV | LHC Run 3 diphoton | 2025-28 | No signal at 108 GeV (CMS searched 70-110). |
| P5 | r (tensor-to-scalar) | 0.0033 | CMB-S4, LiteBIRD | 2028+ | Untested. |
| P6 | n_s (spectral index) | 0.96667 | CMB-S4 | 2028+ | Currently 99.8% match with Planck. Will sharpen. |

**Note:** P2 and P3 overlap with items 1 and 17 in the main scorecard. They are committed predictions with specific numerical values.

---

### Tier 5: GENUINELY INDEPENDENT STRUCTURAL RESULTS (not numerical matches)

These are structural arguments, not numerical predictions, but they form the framework's backbone.

| # | Result | Status | Notes |
|---|--------|--------|-------|
| S1 | A2 uniqueness: only 1 of 18 simple Lie algebras satisfies alpha^(h/r)*mu*phi^deg(p) = h | Computationally verified | 450x margin over next best. But the parameterization was chosen because it works for A2 (partial circularity). |
| S2 | E8 uniqueness: only E8 (of 5 exceptional algebras) produces all 3 core couplings | Computationally verified (§281, C1) | No other algebra gets even ONE coupling within 5%. DECISIVE. Domain wall existence proof: only E8 (real discriminant +5) has real kink vacua. |
| S3 | Nome uniqueness: q=1/phi is the only distinguished nome matching all 3 couplings simultaneously | Computationally verified (§280, F1) | 6061 nomes tested. Triple-match window is ~0.2% wide. q=1/phi is the unique algebraically motivated nome inside it. |
| S4 | Core identity isolation: alpha^(3/2)*mu*phi^2 = 3 has 0/719 neighbors within 1% | Computationally verified (§280, F4) | Genuinely non-trivial. Not cherry-picked from a dense forest. |
| S5 | Exponent 80 in three independent observables | Structural, ~95% proven | 80 = 2*(240/6) appears in v/M_Pl (hierarchy), y_e (Yukawa), Lambda (CC). Three different physical quantities requiring the same number. |
| S6 | C = eta*theta4/2 corrects both alpha and v | Two-point test | ONE algebraic quantity corrects TWO observables with DIFFERENT geometry factors (phi^2 for alpha, 7/3 for v). If C were fitted to alpha, there is no reason it should also work for v. |
| S7 | S3 = Gamma_2 modular flavor symmetry | Validated by mainstream (Okada-Tanimoto 2025) | Framework's generation symmetry IS the mainstream modular flavor symmetry. Not a numerical prediction but a structural identification. |
| S8 | Alpha Formula B (VP running) | 9 sig figs (0.15 ppb, 1.9 sigma) | 1/alpha = theta3*phi/theta4 + (1/3pi)*ln(Lambda_ref/m_e). VP coefficient derived from Jackiw-Rebbi. c2=2/5 from Graham kink pressure. This is the framework's most precise numerical result, pending full mainstream validation of the VP derivation. |

---

## PART C: ITEMS WITH CAVEATS (honest flags)

These items remain in the scorecard but carry important qualifications.

| # | Item | Caveat |
|---|------|--------|
| 6 | Lambda (CC) | Accuracy on a log scale overstates precision. Any number ~0.03 raised to the ~80th power lands in the right ballpark. The real content is whether 80 is genuine. |
| 7 | v (Higgs VEV) | Partly the free parameter. The non-trivial content is the hierarchy expression and the universality of C. |
| 8 | m_e (electron mass) | 99.78% is good but not spectacular. The 0.22% residual is unexplained. |
| 9 | mu (proton/electron) | Leading term structural, correction decorative. Old precision claim (99.9998%) should be retired. New perturbative expansion (14 ppb, §281) is the genuine result. |
| 16 | delta_CP (CKM) | Standout match (99.9997%) but arctan formulas with phi are flexible. Searched. |
| 23 | gamma_Immirzi | Depends on LQG being correct. If LQG is wrong, the constant is meaningless. |
| 26 | Dipole element | Mathematical property of PT n=2, not an independent physical prediction. "100% match" means computation = analytical solution. |

---

## PART D: THE EXPECTED MATCH COUNT (the critical context)

From the Monte Carlo analysis (§256, `expected_match_count.py`):

- With ~18,000 formulas from {phi, modular forms, integers 1-10}, a RANDOM nome in [0.50, 0.70] matches **25.1 +/- 0.3** of 26 targets at 1%.
- At 0.1% threshold, q=1/phi produces 24 matches vs random average 22.9 +/- 1.4 (Z = 0.75) — entirely unremarkable.
- Pool A (phi + integers only, NO modular forms) already matches 21 of 26 targets within 1%.
- Modular forms add only ~5 new targets beyond what phi + integers reach.

**What IS genuinely non-trivial (from the same analysis):**
- The three SPECIFIC formulas (eta = alpha_s, eta^2/(2*theta4) = sin^2(theta_W), theta3*phi/theta4 = 1/alpha) simultaneously hold at only **0.2%** of tested nomes.
- q=1/phi is the ONLY algebraically motivated nome in this 0.2% window (§280, F1).

**Implication:** Most of the "30+ matches" headline is a combinatorial artifact. The genuine signal is narrow: three coupling formulas at q=1/phi.

---

## PART E: BOTTOM LINE NUMBERS

### Items Removed: 8
1. pi formula (generic math)
2. Coupling triangle (tautological)
3. CKM unitarity (tautological)
4. ~~Creation identity (tautological)~~ — **UN-RETIRED Apr 13.** The identity `η² = η(q²)·θ₄` is not tautological: it is the level-1↔level-2 bridge that makes sin²θ_W = η²/(2θ₄) (G3) and α_{s,dark} = η(1/φ²) (D3) the same result, not two independent derivations. See `enrich_c5_creation_identity.py`. Classified as PROVEN MATH (structural bridge).
5. Muon g-2 (wrong)
6. H0 from Lucas (decorative, no derivation)
7. theta2 ~ theta3 (generic for large q)
8. Jacobi abstrusa (tautological)
9. Lame gap ratio = 3 (generic PT limit, not phi-specific)

### Items Remaining: 26 (in main scorecard) + 6 predictions + 8 structural results

### Breakdown by category:

| Category | Count | Items |
|----------|-------|-------|
| DERIVED (clean, no search) | 5 | alpha_s, sin^2(theta_W), 1/alpha tree, alpha corrected, Born rule p=2 |
| STRUCTURAL (exponent 80) | 3 | Lambda, v (partly free param), m_e |
| SEARCHED + CONNECTED | 18 | mu, m_t, m_u/m_e, m_b/m_c, V_us, V_cb, V_ub, delta_CP, sin^2(theta_12), sin^2(theta_23), sin^2(theta_13), eta_B, Omega_m/Omega_Lambda, Delta_m^2 ratio, gamma_Immirzi, m_nu3, lambda_H, dipole element |
| PREDICTION (untested) | 6 | R=-3/2, alpha_s=0.118404, sin^2(theta_12)=0.3071, breathing mode 108.5 GeV, r=0.0033, n_s=0.96667 |
| STRUCTURAL RESULTS | 8 | A2 uniqueness, E8 uniqueness, nome uniqueness, core identity isolation, exponent 80 in 3 places, C corrects 2 observables, S3=Gamma_2, Formula B (9 sig figs) |

### The honest count of genuinely independent, non-tautological, defensible NUMERICAL claims:

**Conservative (hardest to argue with):** 5 clean derived + 2 structural + 2 best searched = **~9 genuinely compelling results**

These are:
1. alpha_s = eta(1/phi) [DERIVED, live test]
2. sin^2(theta_W) = eta^2/(2*theta4) [DERIVED, 99.98%]
3. 1/alpha at 5 sig figs (Formula A) [DERIVED+SEARCHED, 99.9996%]
4. Born rule p=2 from PT n=2 [DERIVED, exact theorem]
5. Lambda = theta4^80 * sqrt(5)/phi^2 [STRUCTURAL, ~exact on log scale]
6. Exponent 80 in hierarchy + Yukawa + Lambda [STRUCTURAL, 3 independent checks]
7. delta_CP = 99.9997% [SEARCHED but standout]
8. C corrects both alpha and v with different geometry [TWO-POINT, non-trivial]
9. Formula B alpha at 9 sig figs [STRUCTURAL+DERIVED, pending VP validation]

**Moderate (defensible with caveats):** Add the well-connected searched items:
- mu leading term (6^5/phi^3), m_t, sin^2(theta_12), sin^2(theta_23), V_us (phi/7 base), eta_B, Omega_m/Omega_Lambda, m_u/m_e = phi^3, m_b/m_c = phi^(5/2)
- Total: **~18 defensible results**

**Generous (everything that matches above 97% and is not tautological):**
- All 26 remaining scorecard items
- Total: **26 results** (down from the old 37)

---

## PART F: HONEST INPUT/OUTPUT RATIO

### Inputs

| # | Input | Type | Cost |
|---|-------|------|------|
| 1 | E8 (choice of Lie algebra) | Axiom | 1 |
| 2 | V(Phi) = lambda*(Phi^2 - Phi - 1)^2 | Follows from #1 + renormalizability + Galois | 0 (derived, given premises) |
| 3 | q = 1/phi (evaluation point) | Follows from #1 via Rogers-Ramanujan | 0 (derived, given premises) |
| 4 | 4A2 sublattice decomposition | Axiom (wanting 3 generations) | 1 |
| 5 | v = 246.22 GeV (energy scale) | Physical input | 1 |
| 6 | phi/7 as CKM base | Searched, then connected | 0.5 |
| 7 | Various searched formulas (~5-8) | Found by search, structurally connected | 0.5 each |

**Generous counting:** 3 axioms (E8, 4A2, v). Everything else follows.
- Inputs: 3
- Outputs: 26
- Ratio: **8.7 : 1**

**Conservative counting:** 3 axioms + ~7 searched structures = ~10 effective inputs.
- Inputs: 10
- Outputs: 26
- Ratio: **2.6 : 1**

**Most honest counting (outputs = only Tier 1 + Tier 2):**
- Inputs: 3 axioms
- Outputs: 8 clean results (Tier 1: 5, Tier 2: 3)
- Ratio: **2.7 : 1**

---

## PART G: COMPARISON — OLD vs CLEAN

| Metric | Old Scorecard | Clean Scorecard |
|--------|--------------|-----------------|
| Total claimed items | 37-38 | **26** |
| "Above 97%" | 37/38 | 24/26 |
| "Above 99%" | 34/38 | 17/26 |
| Tautological items included | 4+ | **0** |
| Wrong items included | 1+ (g-2) | **0** |
| Generic/decorative items | 3+ | **0** |
| Clean derived (no search) | ~5 | **5** (unchanged) |
| Honest input/output ratio | "1 parameter, 37 outputs" | **3 axioms, 26 outputs (generous) / 10 inputs, 26 outputs (conservative)** |

---

## PART H: WHAT THE FRAMEWORK SHOULD LEAD WITH

After cleaning, the framework's strongest arguments are (in order of strength):

1. **E8 uniqueness** (S2) — Only E8 among 5 exceptional Lie algebras produces SM couplings. Algebraic knockout: only E8 has real domain wall vacua.

2. **Three core coupling formulas at q=1/phi** (items 1-3, S3) — These simultaneously hold at only 0.2% of tested nomes, and q=1/phi is the unique algebraically motivated nome in the window.

3. **Alpha at 9 significant figures** (S8) — Formula B with derived VP coefficient reaches 0.15 ppb. Pending full validation of VP derivation pathway.

4. **Born rule p=2 from PT n=2** (item 5) — A mathematical theorem, not a numerical match. Connects quantum measurement to E8 via the domain wall.

5. **Committed falsifiable predictions** (P1-P3) — R=-3/2 (decisive, 2035), alpha_s = 0.118404 (2026-27), sin^2(theta_12) = 0.3071 (JUNO, ongoing). These are the framework's sharpest blades.

6. **Exponent 80 in three independent contexts** (S5) — Hierarchy, Yukawa, and Lambda use the same structural number 2*(240/6) from E8.

---

## PART I: WHAT THE FRAMEWORK SHOULD STOP CLAIMING

1. "37 predictions from 1 parameter" — Inflated. Say "26 results from 3 axioms (conservative: ~10 effective inputs)."
2. "pi = theta3^2*ln(phi) is the crown jewel" — Generic math. Removed.
3. "Self-consistency web with 16 cross-checks" — 7 of 16 were tautological or generic. Say "6 genuinely independent structural constraints plus several algebraic identities."
4. "30+ matches proves the framework" — The Monte Carlo shows 25+ matches is generic for any nome in [0.50, 0.70]. The real signal is the 3-coupling match.
5. "99.9998% on mu" — Falsified at 26 ppt. Say "leading-order approximation at 1.6 ppm, improved to 14 ppb via perturbative expansion."
6. "Muon g-2 consistent" — Wrong higher-order coefficients. Dropped.
7. "Coupling triangle is three independent constraints" — It's one equation rearranged three ways. Tautological.

---

## PART J: THE DECISIVE TESTS

The clean scorecard makes the framework more falsifiable, not less. Three tests decide its fate:

| Test | Value | When | If confirmed | If falsified |
|------|-------|------|-------------|-------------|
| R = d(ln mu)/d(ln alpha) | -3/2 (vs GUT: -38) | ELT/ANDES ~2035 | LR > 10^10. Framework essentially proven. | Framework dead. |
| alpha_s | 0.118404 | CODATA 2026-27 | Strong evidence. | If world average -> 0.1176 +/- 0.0003, framework excluded. |
| sin^2(theta_12) | 0.3071 | JUNO (ongoing) | Moderate evidence. | If JUNO -> 0.310 +/- 0.003, mild tension. |

---

*Document generated Feb 26 2026. This supersedes the §185 scorecard in FINDINGS-v3.md for all assessments of evidence strength. The §185 table remains as historical record of what was claimed; this document is the honest assessment of what survives audit.*
