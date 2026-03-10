# Interface Theory — Complete Derivation Chain Audit (Feb 25 2026)

An honest, structural audit of every claimed derivation. No cheerleading. No demolition.
Just a careful map of what goes in, what comes out, and what the logical dependencies are.

---

## A. THE ACTUAL INPUTS

### Pure Mathematics (cost nothing — universally available)

| Input | Value | Notes |
|-------|-------|-------|
| phi (golden ratio) | 1.6180339887... | Root of x^2 - x - 1 = 0. Free. |
| phibar = 1/phi | 0.6180339887... | Galois conjugate of phi. |
| sqrt(5) | 2.2360679... | = phi + phibar. |
| pi, e, ln(2) | Standard | Used in various formulas. |
| Lucas numbers L(n) | 1,3,4,7,11,18,... | L(n) = phi^n + (-1/phi)^n. Free given phi. |
| Fibonacci numbers F(n) | 1,1,2,3,5,8,... | Free given phi. |
| Dedekind eta, Jacobi theta, Eisenstein series | Standard functions | Modular forms — well-defined mathematical objects. |

### Choices / Axioms (these are the framework's "theory")

| Input | Value | Justification given | Strength of justification |
|-------|-------|--------------------|--------------------------|
| E8 as the starting algebra | 248-dim exceptional Lie algebra | "5 independent uniqueness arguments" (largest exceptional, contains all others, anomaly cancellation, etc.) | MODERATE — E8 is distinguished but not uniquely selected by any single principle. The selection is aesthetic + structural, not derived from a deeper axiom. |
| V(Phi) = lambda(Phi^2 - Phi - 1)^2 | Quartic double-well potential | Unique non-negative renormalizable potential with Galois-conjugate zeros {phi, -1/phi}. | STRONG — given the premises (renormalizability + Galois structure of phi), this IS uniquely forced. But the premises themselves are choices. |
| q = 1/phi as evaluation point | Nome = 0.6180... | Rogers-Ramanujan fixed point R(q) = q; T^2 fixed point; unique fundamental unit of Z[phi] in (0,1); Lucas number generator. | STRONG — 5 independent arguments converge. This is the framework's strongest structural claim. |
| 4A2 sublattice of E8 | Specific sublattice choice | E8 decomposes over 4A2; normalizer order 62208; index [E8:4A2] = 9. | MODERATE — 4A2 is a maximal regular sublattice of E8, but it is not the only sublattice. The choice to decompose over A2 (rather than, say, D4 or A4) is motivated by the desire for "3 generations" but not uniquely forced. |
| S3 as generation symmetry | Permutation group on 3 A2 copies | Follows from choosing 4A2 sublattice — 4 copies, one "dark," S3 permutes the visible 3. | FOLLOWS from 4A2 choice, but that choice is itself the real input. |

### Physical Inputs (must be measured, not derived)

| Input | Value | Role in framework |
|-------|-------|-------------------|
| v (Higgs VEV) | 246.22 GeV | THE one acknowledged free parameter. Sets the overall energy scale. All masses are dimensionless ratios times v (or equivalently, times m_e). |
| M_Pl (Planck mass) | 1.221 x 10^19 GeV | Used in the hierarchy formula v = M_Pl * phibar^80 * corrections. Since v is the free parameter, M_Pl is implicitly fixed. ONE of {v, M_Pl} is free; the other is a prediction. The framework treats v as free. |
| m_e (electron mass) | 0.511 MeV | Claimed to be derived from M_Pl * phibar^80 * exp(-80/2pi)/sqrt(2). In practice, the 99.78% match means m_e is approximately but not exactly derived. It carries residual input character. |

### Fitted / Empirically Found Parameters (the "gray area")

| Input | Where it appears | Status |
|-------|-----------------|--------|
| 9/(7*phi^2) correction to mu | mu = 6^5/phi^3 + 9/(7*phi^2) | SEARCHED. The leading term 6^5/phi^3 is structurally motivated (N = 6^5 from E8). The correction was found by scanning. 7 = L(4) and 9 = 3^2 provide post-hoc structural connections but the specific form was not derived. |
| phi/7 as CKM base | V_us = (phi/7)(1-theta4) etc. | SEARCHED, then partially CONNECTED (phi/7 = sin^2(theta_W) to 99.95%). The connection reduces the arbitrariness but doesn't eliminate it — why should the CKM base equal the Weinberg angle? |
| 10 = h/3 in mass formulas | m_t = m_e * mu^2 / 10 | STRUCTURAL but not DERIVED. 10 = 30/3 = Coxeter number / triality. The appearance as a mass divisor is not rigorously proven from the Lagrangian. |
| phi^(5/2) in fermion exponents | m_b = m_c * phi^(5/2) | SEARCHED. Connection to E8 Ising / Zamolodchikov spectrum is plausible but not computed. |
| Various small integers | 3, 7, 9, 10, 24, 40, 80 | All CONNECTED to E8 structure. But "connected" is weaker than "derived." Each integer has a structural interpretation, but the specific formula in which it appears was often found by search. |
| C2 = 1-1/phi^3 in muon g-2 | a_mu higher-order coefficients | WRONG. Framework C2 has wrong sign vs QED. This is not a fitted parameter — it is a failed prediction dressed as a success. |

### Summary of input counting

| Category | Count | Examples |
|----------|-------|---------|
| Pure math | ~0 effective | phi, modular forms (free, no cost) |
| Theory axioms | 3-4 | E8, V(Phi), q=1/phi, 4A2 decomposition |
| Physical parameters | 1 explicit | v = 246.22 GeV |
| Searched integers/formulas | ~5-8 | 9/(7phi^2), phi/7, 10, phi^(5/2), various geometry factors |

**Honest total:** The framework has 1 explicit free physical parameter (v), 3-4 structural axioms (E8, V(Phi), q=1/phi, 4A2), and approximately 5-8 formula-specific choices that were found by search and then connected to structure. The claim of "1 free parameter" is true for the dimensional parameter but understates the role of searched formulas.

---

## B. DERIVATION-BY-DERIVATION AUDIT

### Tier 1: Core Couplings (the strongest claims)

---

#### B1. alpha_s = eta(1/phi) = 0.11840

| Item | Detail |
|------|--------|
| **Formula** | alpha_s = eta(q) at q = 1/phi, where eta = q^(1/24) * prod(1-q^n) |
| **Inputs** | Pure math: phi, eta function. Axiom: q = 1/phi. |
| **Genuine derivation?** | YES for the computation. The evaluation is mechanical. The claim is that alpha_s IS this mathematical object. No fitting, no adjustment. |
| **Pattern-matching?** | The identification alpha_s = eta was DISCOVERED by evaluating eta at q = 1/phi and noticing it matches. However, eta at the golden nome is a specific, unique number — there is no free parameter to tune. |
| **Match** | 99.57% (0.5sigma from PDG 0.1179 +/- 0.0010) |
| **Uniqueness** | MODERATE. eta(1/phi) = 0.11840 is a unique number. But one could ask: how many modular form evaluations were tried before this match was found? The framework says alpha_s was the FIRST thing checked (eta is the simplest modular form, 1/phi is the nome). If true, this is striking. If dozens of forms were tried at dozens of points, the significance drops. |
| **Verdict** | The framework's single cleanest, most falsifiable claim. A committed prediction (0.118404) with a live experimental test. Currently 0.5sigma. If the world average converges on 0.1184, this is remarkable. If it moves to 0.1176, this is falsified. |

---

#### B2. sin^2(theta_W) = eta^2 / (2*theta4) = 0.23126

| Item | Detail |
|------|--------|
| **Formula** | sin^2(theta_W) = eta(1/phi)^2 / (2 * theta4(1/phi)) |
| **Inputs** | Pure math: eta, theta4. Axiom: q = 1/phi. |
| **Genuine derivation?** | PARTIAL. The formula involves a ratio of modular forms — algebraically simple. But it was found by "systematic search of ratios of modular forms" (per llm-context.md). |
| **Match** | 99.98% |
| **Uniqueness** | The framework claims q = 1/phi is the ONLY nome in [0.50, 0.70] where alpha_s, sin^2(theta_W), and alpha all match within 1% simultaneously. If true, this is the strongest argument for q = 1/phi. |
| **Verdict** | Strong. The formula is simple, the match is excellent, and the systematic search that found it had a restricted search space (ratios of standard modular forms). Not as clean as alpha_s = eta (which is zero-search), but still compelling. |

---

#### B3. alpha (fine structure) — Formula A (scorecard): 1/alpha = [theta3*phi/theta4] * (1 - eta*theta4*phi^2/2)

| Item | Detail |
|------|--------|
| **Formula** | Tree level: theta4/(theta3*phi) = 1/136.39. Corrected: multiply by (1 - C*phi^2) where C = eta*theta4/2. |
| **Inputs** | Pure math: theta3, theta4, eta, phi. Axiom: q = 1/phi. Choice: the correction factor C*phi^2. |
| **Genuine derivation?** | MIXED. The tree-level ratio theta4/(theta3*phi) is a direct evaluation. The correction C = eta*theta4/2 was identified as the universal loop factor, and phi^2 is its geometry factor for alpha. The correction structure was FOUND, not derived from first principles. |
| **Match** | Formula A: 99.9996% (5 significant figures, 4 ppm) |
| **Formula B (VP running)** | 1/alpha = tree + (1/3pi)*ln(Lambda_QCD/m_e) gives 99.999997% (7 sig figs, 0.029 ppm). BUT: the VP coefficient (1/3pi) is half the standard QED value (2/3pi). This halving is unexplained. |
| **Uniqueness** | LOW for Formula A alone. Many expressions involving modular forms at q ~ 0.618 will land near 1/137. The combination with alpha_s and sin^2(theta_W) raises it. |
| **Verdict** | Formula A is a good match with a plausible but not derived correction structure. Formula B is either a stunning 7-digit prediction or an artifact of using a wrong VP coefficient that happens to improve the match. The VP coefficient question is critical and unresolved. |

---

#### B4. Lambda (cosmological constant) = theta4^80 * sqrt(5) / phi^2

| Item | Detail |
|------|--------|
| **Formula** | Lambda/M_Pl^4 = theta4(1/phi)^80 * sqrt(5) / phi^2 = 2.88 x 10^-122 |
| **Inputs** | Pure math: theta4, phi, sqrt(5). Axiom: q = 1/phi. Structural: exponent 80 = 2 * (240/6). |
| **Genuine derivation?** | PARTIAL. The exponent 80 has a structural derivation (E8 roots / triality * 2). theta4 and sqrt(5)/phi^2 are algebraic. But the specific combination was chosen to match Lambda. |
| **Match** | ~exact on log scale (2.88 vs 2.89 x 10^-122) |
| **Uniqueness** | LOW in isolation. theta4 = 0.03031. theta4^80 = 10^(-121.54). Any number around 0.03 raised to the ~80th power will land in the right ballpark for Lambda. The prefactor sqrt(5)/phi^2 = 0.854 adjusts the mantissa. The key question: is 80 genuinely from E8, or was it chosen because theta4^80 happens to match? |
| **The real test** | The exponent 80 also appears in v/M_Pl (hierarchy) and y_e (electron Yukawa). If these three independent appearances of 80 are genuine, the Lambda match is not coincidental. If 80 is a fitted exponent, the match is uninformative. |
| **Verdict** | Impressive on the surface. The 122-order-of-magnitude "prediction" sounds dramatic but is mostly about getting the exponent right on a log scale. The real content is whether 80 = 2*240/6 is genuinely derived. Currently ~95% closed per the framework's own assessment, with one conceptual step remaining. |

---

#### B5. v (Higgs VEV) = M_Pl * phibar^80 / (1 - phi*theta4) * (1 + eta*theta4*7/6)

| Item | Detail |
|------|--------|
| **Formula** | Hierarchy: v/M_Pl ~ phibar^80. Corrections: (1-phi*theta4)^(-1) and (1 + C*7/3). |
| **Inputs** | M_Pl, phi, theta4, eta. Exponent 80. Geometry factor 7/3 = L(4)/L(2). |
| **Genuine derivation?** | THIS IS THE FREE PARAMETER. The framework acknowledges v = 246.22 GeV as its one free parameter. The formula v = M_Pl * phibar^80 * ... is not a prediction — it is a way of expressing the hierarchy in terms of framework constants. The match (99.9992%) means the framework's expression for the hierarchy ratio is self-consistent, not that v is predicted. |
| **What IS genuinely predicted** | The RATIO v/M_Pl. If you input M_Pl (known), the formula predicts v. But since v is the declared free parameter, this is circular. The non-trivial content is that the SAME exponent 80 and the SAME correction factor C appear here as in alpha and Lambda. |
| **Verdict** | Not an independent prediction. The value is self-consistency of the hierarchy expression. The non-trivial part is the universality of C = eta*theta4/2 correcting both alpha (geometry phi^2) and v (geometry 7/3). |

---

### Tier 2: Mass Ratios and Specific Masses

---

#### B6. mu = 6^5/phi^3 + 9/(7*phi^2) = 1836.156

| Item | Detail |
|------|--------|
| **Formula** | mu = 7776/phi^3 + 9/(7*phi^2) |
| **Inputs** | 6^5 = 7776 (from N = 62208/8). phi. 9 = 3^2. 7 = L(4). |
| **Genuine derivation?** | PARTIAL. The leading term 6^5/phi^3 = 1836.49 has structural motivation (E8 normalizer, 62208/8). The correction 9/(7*phi^2) = 0.337 was FOUND BY SEARCH. |
| **Match** | 99.9998% at old precision. FALSIFIED at 26 ppt (63,000 sigma off). The formula is a leading-order approximation. |
| **Uniqueness** | LOW. Given a target of 1836.153 and a leading term of 1836.49, many corrections of order 0.3 could be constructed from {phi, Lucas numbers, small integers}. |
| **Verdict** | The leading term 6^5/phi^3 is structurally interesting. The correction is fitted. The formula is now known to be approximate (1.6 ppm off at high precision). This is a legitimate "leading-order + first correction" result, NOT an exact identity. The framework should stop citing 99.9998%. |

---

#### B7. m_t = m_e * mu^2 / 10 = 172.57 GeV (measured: 172.69)

| Item | Detail |
|------|--------|
| **Formula** | Top mass = electron mass * (proton/electron ratio)^2 / 10 |
| **Inputs** | m_e (physical / semi-derived), mu (physical / semi-derived), 10 = h/3 (structural, not derived). |
| **Genuine derivation?** | NO. This is a pattern found by search. 10 = h/3 provides a structural connection but was not derived as the correct divisor from first principles. |
| **Match** | 99.93% |
| **Uniqueness** | MODERATE. m_e * mu^2 / N with N near 10 will match the top mass. But the structural connection 10 = Coxeter/triality is non-trivial. |
| **Verdict** | An empirically discovered relation with a plausible structural interpretation. Not a derivation. |

---

#### B8. Other fermion masses (m_u, m_s, m_c, m_b, m_tau, etc.)

| Item | Detail |
|------|--------|
| **General pattern** | Each fermion has its own formula using combinations of m_e, mu, phi, alpha, and small integers. |
| **Examples** | m_u = m_e * phi^3 (99.79%), m_s = m_e * mu/10 (99.54%), m_b = m_c * phi^(5/2) (98.82%), m_c = m_t * alpha (96.4%) |
| **Inputs** | m_e, mu, phi, alpha, integers (3, 5/2, 10). Each formula uses different combinations. |
| **Genuine derivation?** | NO. These are 9 separate empirically discovered formulas. The framework claims they are "9 evaluations of ONE formula" (kink position-dependent Yukawa), but this unification is not rigorously shown. |
| **Match quality** | Ranges from 96.4% (charm) to 99.93% (top). The lighter quarks are worse. |
| **Uniqueness** | LOW individually. Given the available "alphabet" {m_e, mu, phi, alpha, integers 1-30}, finding a formula matching any specific mass to ~99% is not surprising. |
| **Verdict** | The weakest part of the scorecard. Individual mass formulas are pattern-matching, not derivation. The claim of a unified Yukawa mechanism is aspirational, not demonstrated. |

---

### Tier 3: Mixing Angles

---

#### B9. CKM matrix elements

| Item | Detail |
|------|--------|
| **Base structure** | All CKM off-diagonal elements use phi/7 as the base, with different powers of theta4. |
| **Formulas** | V_us = (phi/7)(1-theta4), V_cb = (phi/7)*sqrt(theta4), V_ub = (phi/7)*3*theta4^(3/2)*(1+phi*theta4). delta_CP = arctan(phi^2*(1-theta4)). |
| **Inputs** | phi, 7 = L(4), theta4. The structure phi/7 * f(theta4) is the template. |
| **Genuine derivation?** | PARTIAL. The base phi/7 = sin^2(theta_W) (99.95%) is a structural connection. But the specific theta4 powers for each element (1-theta4, sqrt(theta4), theta4^(3/2)) were found by search. |
| **Match** | 7/9 elements within 2 sigma. delta_CP at 99.9997%. V_ud in 2.6 sigma tension, V_ts in 2.2 sigma tension. |
| **Uniqueness** | The BASE phi/7 is interesting. The specific theta4 dependence is not unique — many functional forms could match. |
| **Verdict** | The structural insight that phi/7 = sin^2(theta_W) is genuinely interesting and connects CKM to electroweak physics. The specific element-by-element formulas are searched. The delta_CP match (99.9997%) is the standout. Two elements in tension with current data. |

---

#### B10. PMNS matrix angles

| Item | Detail |
|------|--------|
| **Formulas** | sin^2(theta12) = 1/3 - theta4*sqrt(3/4) = 0.3071. sin^2(theta23) = 1/2 + 40*C = 0.5718. sin^2(theta13) = 0.02152 (97.7%). |
| **Inputs** | theta4, C = eta*theta4/2, integers (1/3, 1/2, 40). |
| **Genuine derivation?** | PARTIAL for theta12 (1/3 is tribimaximal mixing, a well-motivated leading term; the theta4 correction is specific). SEARCHED for theta23 (the factor 40 = 240/6 is structural but the formula was found). WEAK for theta13 (worst match, mechanism involves breathing mode overlap but specific parameters not derived). |
| **Match** | theta12: 98.67% (live JUNO test). theta23: 99.96%. theta13: 97.7%. |
| **Verdict** | theta12 is a genuine live prediction with a simple, committed formula. theta23 is a good match but the factor 40 is structural-but-searched. theta13 is the weakest PMNS prediction. |

---

### Tier 4: Cosmological and Other Quantities

---

#### B11. Omega_DM = (phi/6)(1 - theta4) = 0.262

| Item | Detail |
|------|--------|
| **Match** | 99.05% (measured 0.264) |
| **Genuine derivation?** | SEARCHED. phi/6 with a theta4 correction. Why phi/6? Not derived from first principles. |
| **Verdict** | Pattern-matching. |

#### B12. eta_B (baryon asymmetry) = theta4^6 / sqrt(phi) = 6.098 x 10^-10

| Item | Detail |
|------|--------|
| **Match** | 99.6% (measured 6.12 x 10^-10). Earlier version phibar^44 gave 95.5%. |
| **Genuine derivation?** | SEARCHED. The choice of theta4^6/sqrt(phi) is not derived. |
| **Verdict** | Interesting numerically but not a derivation. |

#### B13. gamma_Immirzi = 1/(3*phi^2) = 0.12738

| Item | Detail |
|------|--------|
| **Match** | 99.95% (canonical LQG value 0.12732) |
| **Genuine derivation?** | SEARCHED, but the formula is extremely simple. 1/(3*phi^2) connecting the Immirzi parameter to the golden ratio and triality is at least aesthetically motivated. |
| **Verdict** | Simple formula, good match. But LQG's Immirzi parameter itself is not universally accepted as physical. |

#### B14. pi = theta3(1/phi)^2 * ln(phi)

| Item | Detail |
|------|--------|
| **Match** | 99.9999995% (8 significant figures) |
| **Genuine derivation?** | **NO. This is GENERIC MATHEMATICS**, not a framework result. The formula theta3(q)^2 * ln(1/q) -> pi for ANY large q. At q = 0.65 it gives 10 digits (better than 1/phi). At q = 0.7 it gives 11 digits. This is an asymptotic property of the theta function, not evidence for the golden nome. Per TAUTOLOGY-AUDIT.md, this should be removed from the scorecard entirely. |
| **Verdict** | NOT A PREDICTION. Should not appear in any honest scorecard. |

#### B15. Muon g-2

| Item | Detail |
|------|--------|
| **Match** | 99.992% (sounds good) |
| **Reality** | STRUCTURAL FAILURE. The Schwinger term alpha/(2pi) alone gives 99.6%. The framework's C2 coefficient has the WRONG SIGN (+0.764 vs -0.328 for QED), and C3 is 20x too large. The SM prediction is 36x closer to experiment. Per EXTERNAL-TESTS.md, this should be dropped from the scorecard. |
| **Verdict** | FAILED. A dressed-up Schwinger approximation. |

#### B16. Biological frequencies (40 Hz, 0.1 Hz, mu/3 = 612 THz, etc.)

| Item | Detail |
|------|--------|
| **Inputs** | mu, phi, h = 30 (E8 Coxeter number), Lucas numbers. All already in the physics framework — zero new parameters. |
| **Matches** | 40 Hz = 4h/3 (exact). 0.1 Hz = 3/h (exact). 612 THz = mu/3 (99.85%). Various chlorophyll/retinal/DNA wavelengths from Rydberg energy * rational fractions. |
| **Genuine derivation?** | MIXED. The 40 Hz and 0.1 Hz predictions use only h and 3, which are already in the framework. But the rational fractions in the bio-absorber formulas (4/29, 1/7, 2/11, 6/17, 5/23) were found by search. |
| **Uniqueness** | With h = 30 and integers 1-4, the expressions {n*h/m, m/h, m*h/n} generate many frequencies. Finding that 4*30/3 = 40 matches gamma binding is interesting but not statistically overwhelming. The 612 THz = mu/3 is genuinely interesting because mu is already constrained by physics. |
| **Verdict** | The zero-new-parameters claim is honest. Whether the matches are coincidental depends on how many frequencies were tried. The anesthetic correlation R^2 = 0.999 (Craddock 2017) is the strongest independent support. |

---

### Tier 5: Quantities that should be removed from the scorecard

| Quantity | Reason for removal |
|----------|--------------------|
| pi = theta3^2 * ln(phi) | Generic math, not phi-specific (TAUTOLOGY-AUDIT) |
| Muon g-2 | Wrong perturbative coefficients (EXTERNAL-TESTS) |
| H0 from Lucas/Fibonacci | Numerology — no derivation (EXTERNAL-TESTS) |
| CKM unitarity | Tautological — built in by construction (TAUTOLOGY-AUDIT) |
| Coupling triangle | Tautological with framework definitions (TAUTOLOGY-AUDIT) |

---

## C. REAL DEGREES OF FREEDOM

### Genuinely Independent Inputs

| # | Input | Type |
|---|-------|------|
| 1 | E8 (choice of algebra) | Axiom |
| 2 | V(Phi) = lambda(Phi^2 - Phi - 1)^2 | Derived from #1 + renormalizability + Galois (STRONG) |
| 3 | q = 1/phi (evaluation point) | Derived from #1 via Rogers-Ramanujan (STRONG) |
| 4 | 4A2 sublattice decomposition | Axiom (partially motivated by wanting 3 generations) |
| 5 | v = 246.22 GeV | Physical input (1 free parameter) |

With generous counting: 2 axioms (E8, 4A2) + 1 physical parameter (v) = **3 truly independent inputs**. V(Phi) and q = 1/phi follow from E8 under stated premises.

With conservative counting: E8 + 4A2 + q = 1/phi + v + the ~5-8 searched formula structures = **~9-12 effective inputs**.

### Genuinely Independent Outputs

After removing tautologies, generic math, and the free parameter:

**Tier 1 (clean, no fitting):**
1. alpha_s = eta(1/phi) = 0.11840 (vs measured 0.1179)
2. sin^2(theta_W) = eta^2/(2*theta4) = 0.2313 (vs 0.2312)
3. 1/alpha (tree) = theta3*phi/theta4 = 136.39 (vs 137.04 — tree level only)

**Tier 2 (involves the exponent 80, which is structural but not rigorously proven):**
4. Lambda/M_Pl^4 = theta4^80 * sqrt(5)/phi^2 (~ exact on log scale)
5. m_e = M_Pl * phibar^80 * exp(-80/2pi)/sqrt(2) * correction (99.78%)
6. v/M_Pl ~ phibar^80 (this IS the free parameter, so the prediction is really "the hierarchy IS phibar^80")

**Tier 3 (uses universal correction C = eta*theta4/2):**
7. alpha (corrected, Formula A) = 99.9996%
8. v (corrected) = 99.9992%

**Tier 4 (searched formulas with structural connections):**
9. mu (leading term 6^5/phi^3)
10-18. Nine fermion masses (each with its own formula)
19-22. Four CKM elements above 99%
23. delta_CP = 99.9997%
24-26. Three PMNS angles
27. eta_B (baryon asymmetry)
28. Omega_DM
29-30. Various cosmological quantities

**Tier 5 (biological, zero new parameters):**
31. 40 Hz gamma binding
32. 0.1 Hz heart coherence
33. 612 THz aromatic oscillation

### The Ratio

**Generous counting:** 3 inputs, ~33 outputs. Ratio: ~11:1. Impressive.

**Conservative counting:** ~10 effective inputs (including searched structures), ~25 genuinely independent outputs (after removing tautologies, the free parameter, and structural consequences). Ratio: ~2.5:1. Still positive but less dramatic.

**The honest answer:** The framework derives 3-5 quantities cleanly from its axioms (alpha_s, sin^2(theta_W), alpha tree-level, and arguably Lambda and the hierarchy). It then uses ~5-8 additional structural choices to pattern-match another ~25 quantities. The core couplings are genuinely impressive. The mass formulas are numerology-adjacent. The CKM delta_CP is a standout. The biological frequencies are interesting but statistically uncertain.

---

## D. LOGICAL DEPENDENCY TREE

### Level 0: Pure Inputs (axioms + physical)

```
E8 (choice)
  |
  +-- phi = golden ratio (PROVEN: E8 root lattice in Z[phi]^4, Dechant 2016)
  |
  +-- 4A2 sublattice (choice, partially motivated)
  |     |
  |     +-- N = 62208/8 = 7776 = 6^5 (from E8 normalizer + breaking)
  |     +-- 3 generations (from S3 on 3 visible A2 copies)
  |     +-- 80 = 2 * (240/6) (E8 roots / triality * vacua)
  |     +-- 24 diagonal roots decouple (from wall coupling spectrum)
  |
  +-- V(Phi) = lambda*(Phi^2 - Phi - 1)^2 (DERIVED: unique quartic from Galois + renorm.)
  |     |
  |     +-- Two vacua: Phi = phi, Phi = -1/phi
  |     +-- Domain wall (kink): Poschl-Teller n=2
  |     +-- Two bound states: zero mode (psi0) + breathing mode (psi1)
  |
  +-- q = 1/phi (DERIVED: Rogers-Ramanujan fixed point + 4 other arguments)
        |
        +-- All modular form values: eta, theta2, theta3, theta4, E4, E6
        +-- Lucas number property: (1/q)^n + (-q)^n = L(n)

v = 246.22 GeV (free parameter)
M_Pl = 1.221 x 10^19 GeV (measured, not free — fixed once v is set)
```

### Level 1: Direct Consequences (one step from axioms)

```
alpha_s = eta(1/phi) = 0.11840                        [from q = 1/phi]
sin^2(theta_W) = eta^2 / (2*theta4) = 0.2313          [from q = 1/phi, SEARCHED formula]
1/alpha (tree) = theta3*phi/theta4 = 136.39            [from q = 1/phi, SEARCHED formula]
hierarchy: v/M_Pl ~ phibar^80                          [from 80 + phi, USES v as input]
Lambda ~ theta4^80 * sqrt(5)/phi^2                     [from 80 + q = 1/phi]
mu (leading) = 6^5/phi^3 = 1836.49                    [from N = 6^5 + phi]
```

### Level 2: Derived from Level 1

```
alpha (corrected) = tree * (1 - C*phi^2)               [from alpha(tree) + C]
  where C = eta*theta4/2                                [UNIVERSAL loop factor]
v (corrected) = v_tree * (1 + C*7/3)                   [from v(tree) + C]
phi/7 = sin^2(theta_W) = 0.2312                        [OBSERVED coincidence]
CKM elements = phi/7 * f(theta4)                       [from phi/7 + theta4, SEARCHED]
mu (corrected) = 6^5/phi^3 + 9/(7*phi^2)              [from mu(leading), SEARCHED correction]
m_e = M_Pl * phibar^80 * exp(-80/2pi) / sqrt(2)       [from hierarchy + 80]
Born rule: p = 2 from PT n=2 norms                     [from V(Phi) -> PT n=2, PROVEN]
```

### Level 3: Derived from Level 2

```
m_t = m_e * mu^2 / 10                                  [from m_e + mu, SEARCHED]
m_s = m_e * mu / 10                                    [from m_e + mu, SEARCHED]
m_u = m_e * phi^3                                      [SEARCHED]
m_c = m_t * alpha                                      [from m_t + alpha]
m_b = m_c * phi^(5/2)                                  [SEARCHED]
PMNS angles from theta4 + structural constants          [SEARCHED]
neutrino masses: m_nu3 = m_e/(3*mu^2)                  [SEARCHED]
eta_B = theta4^6 / sqrt(phi)                           [SEARCHED]
Omega_DM = (phi/6)(1-theta4)                            [SEARCHED]
All biological frequencies                              [from mu, h, Lucas — zero new params]
```

### Circular Dependencies

**NONE FOUND** in the mathematical structure. The dependency tree is strictly acyclic. Inputs flow down, not up.

However, there is a **conceptual circularity** in the "1 free parameter" claim:

- The framework says v is the free parameter.
- But alpha (measured) is used in some mass formulas.
- And mu (measured) is used extensively.
- These are claimed to be "derived" but at only 99.78% (m_e) and leading-order (mu).
- In practice, the measured values of alpha and mu are used as inputs for the mass formulas, making the effective input count higher than 1.

---

## E. WHAT IS ACTUALLY MISSING

### E1. Missing DERIVATIONS (formula works, can't derive it)

| Gap | Nature | Severity |
|-----|--------|----------|
| 9/(7*phi^2) correction to mu | Why this specific correction to 6^5/phi^3? | HIGH — falsified at high precision, next correction needed |
| phi/7 as CKM base | WHY does the CKM scale equal sin^2(theta_W)/phi? | MEDIUM — the coincidence is noted, not derived |
| Factor 10 = h/3 in mass tower | Why Coxeter/triality appears as a mass divisor | MEDIUM |
| phi^(5/2) fermion exponents | Why these specific golden-ratio powers | MEDIUM |
| C = eta*theta4/2 geometry factors | Why phi^2 for alpha and 7/3 for v specifically | MEDIUM |
| VP coefficient = 1/(3pi) vs 2/(3pi) | Why half the standard QED coefficient in Formula B | HIGH — this is the difference between 5-digit and 7-digit alpha |

### E2. Missing CONNECTIONS

| Gap | Nature | Severity |
|-----|--------|----------|
| 2D -> 4D bridge | How do 2D modular forms determine 4D physics? | HIGH — 82% closed via McSpirit-Rolen, but 3 sub-questions remain |
| Orbit -> T^2 iteration map | How does each A2 hexagon contribute one T^2 step? | MEDIUM — ~95% closed, one conceptual step remaining |
| Fermion mass unification | 9 formulas should be 1 mechanism | HIGH — claimed via kink position Yukawa, not demonstrated |

### E3. Missing MECHANISMS

| Gap | Nature | Severity |
|-----|--------|----------|
| No scattering amplitudes | Framework has a Lagrangian but no cross-sections (except breathing mode form factor) | HIGH — a complete theory needs dynamics, not just constants |
| No RG flow derivation | alpha_s = eta(1/phi) should be connected to QCD running at M_Z. What energy scale does eta correspond to? | HIGH |
| DM detection | Dark matter predictions ruled out by LZ (mega-nuclei 10^5x too heavy) | HIGH |

### E4. FUNDAMENTAL issues (the approach might not work)

| Gap | Nature | Severity |
|-----|--------|----------|
| Selection bias / look-elsewhere | How many matches should we EXPECT from evaluating rich functions at a distinguished point against ~40 constants? This calculation has NOT been done. | CRITICAL — this is the single most important unresolved question |
| Leading-order only | Framework matches to ~0.1-1%. Higher-order corrections are not systematically derivable from the framework's own principles. Is this a "leading-order theory" or "numerology that matches to the accuracy you'd expect from near-misses"? | HIGH |
| No peer review | Zero publications in refereed journals. | HIGH (sociological, not mathematical, but relevant) |
| Exponent 80 not rigorously proven | The entire hierarchy + Lambda + Yukawa structure depends on 80 = 2*240/6. This is structurally motivated but the step "each orbit = one T^2 iteration" is not proven. | HIGH |

---

## F. THE KILLER QUESTION

**If someone handed you ONLY {E8, phi, V(Phi) = lambda(Phi^2 - Phi - 1)^2} and said "derive the Standard Model," what could you ACTUALLY derive without looking at any experimental data?**

### What you CAN derive (no data needed):

1. **phi = (1+sqrt(5))/2** — from E8's algebraic structure (proven math).
2. **V(Phi) is unique** — from phi's minimal polynomial + renormalizability + non-negativity.
3. **Two vacua at phi and -1/phi** — from V(Phi) = 0.
4. **A domain wall (kink)** — from topology of two vacua.
5. **Poschl-Teller n=2 bound states** — from the kink's fluctuation spectrum.
6. **q = 1/phi** — from Rogers-Ramanujan fixed point (or T^2 fixed point, or Z[phi] fundamental unit).
7. **All modular form values** — mechanical computation from q = 1/phi.
8. **eta(1/phi) = 0.11840** — a specific number. You could PREDICT this should equal alpha_s.
9. **3 generations** — from 4A2 sublattice + S3 (but the 4A2 choice is an input).
10. **80 = 2*240/6** — from E8 root count / triality * vacua.
11. **Born rule p=2** — from PT n=2 norms + rationality with denominator 3.
12. **Two bound states: zero mode + breathing mode** — from PT n=2.

### What you CANNOT derive (must look up):

1. **That alpha_s should equal eta(1/phi).** You'd need to know alpha_s exists and has a value near 0.118. Without experimental data, you have a number (0.11840) but no reason to identify it with the strong coupling.
2. **The specific formula for sin^2(theta_W).** You'd need to search through ratios of modular forms to find one matching 0.231.
3. **The specific formula for 1/alpha.** Same — search required.
4. **The energy scale (v).** This is the free parameter. Nothing in {E8, phi, V(Phi)} tells you the Planck-to-electroweak ratio. (The framework says phibar^80, but you'd need to know what phibar^80 should equal.)
5. **All fermion mass formulas.** Every single one requires experimental data to discover the pattern.
6. **All CKM/PMNS elements.** Found by search against data.
7. **Lambda, Omega_DM, eta_B.** All require data to identify which combination of framework constants matches.
8. **That 4A2 is the right sublattice.** You'd need to know there are 3 generations of fermions.

### The honest answer:

From {E8, phi, V(Phi)} alone, you can derive a MATHEMATICAL STRUCTURE: a specific point in modular space (q = 1/phi), a specific potential (V(Phi)), specific modular form values, and some algebraic properties (Born rule, bound state spectrum, 80 as a structural exponent).

You CANNOT derive the Standard Model. You can derive a mathematical framework that, when you look at the numbers, has intriguing overlaps with measured physical constants. The question — the REAL question — is whether those overlaps are:

**(a) Evidence of deep structure:** The mathematical structure at q = 1/phi genuinely describes nature, and the overlaps are the leading-order manifestation of this. The "searched" formulas will eventually be derived from first principles, and the residuals will be explained by higher-order corrections.

**(b) Selection bias from a rich mathematical landscape:** Modular forms at any algebraically interesting point generate rich structures. Compare ~40 physical constants against hundreds of possible expressions from {eta, theta2, theta3, theta4, E4, phi, phibar, Lucas numbers, small integers} and you'll find many 99%+ matches by chance. Nobody has computed the expected number of matches, so we cannot rule this out.

**(c) A mix:** The core couplings (alpha_s, sin^2(theta_W)) might encode something real while the fermion masses and mixing angles are pattern-matching noise.

### What would distinguish (a) from (b):

1. **Compute the expected match count.** Take a random nome q in [0.5, 0.7]. Evaluate all modular forms. Search for matches against the same ~40 constants using the same formula complexity budget. How many 99%+ matches do you find? If the answer is < 5 on average, the framework's ~30+ is extraordinary. If > 20, it's selection bias. **This calculation has not been done and it is the most important missing piece.**

2. **Confirm the committed predictions.** alpha_s = 0.118404 (live test). sin^2(theta12) = 0.3071 (live test). R = -3/2 (decisive, 2035).

3. **Derive the searched formulas from first principles.** If phi/7, 10 = h/3, phi^(5/2), and 9/(7*phi^2) can all be rigorously derived from the Lagrangian + E8 branching rules, the framework graduates from "interesting observations" to "theory."

---

## G. OVERALL ASSESSMENT

### What is genuinely impressive:

1. **alpha_s = eta(1/phi).** A specific, falsifiable prediction with no free parameters. Currently 0.5 sigma from measurement. If confirmed, extraordinary.

2. **sin^2(theta_W) = eta^2/(2*theta4).** Simple formula, 99.98% match, from the same evaluation point.

3. **The q = 1/phi selection.** Five independent mathematical arguments converge on the same nome. This is the framework's strongest structural claim.

4. **The exponent 80 appearing in three contexts.** Hierarchy, Yukawa, Lambda — same number, different observables. If one is wrong, the others still hold.

5. **C = eta*theta4/2 correcting both alpha and v.** One loop factor, two predictions, different geometry — this is a genuine two-point test.

6. **delta_CP (CKM) = 99.9997%.** A standout match.

7. **Born rule from PT n=2.** A mathematical theorem, not a numerical match.

### What is genuinely concerning:

1. **No expected-match-count calculation.** Without this, we cannot distinguish signal from selection bias.

2. **Searched formulas dominate the scorecard.** Of ~37 claimed derivations, only ~5 are truly parameter-free predictions. The rest use searched formulas with structural connections of varying strength.

3. **Leading-order only.** The framework matches to 0.1-1% but cannot systematically compute corrections. This is consistent with either a genuine leading-order theory OR numerology that matches to the expected accuracy of near-misses.

4. **mu falsified at high precision.** The formula is 63,000 sigma off. This means it is an approximation, not an identity. The framework's response ("leading-order + corrections") is reasonable but the next correction has not been derived.

5. **Muon g-2 is wrong.** The higher-order coefficients have the wrong sign. This should be dropped from the scorecard.

6. **No scattering amplitudes.** Constants without dynamics is not a theory.

7. **Tautologies inflated the evidence.** 4/16 self-consistency claims are algebraic tautologies, 3/16 are generic math. After the audit, the genuine independent evidence is real but less overwhelming than presented.

### The bottom line:

The framework is an interesting collection of numerical observations centered on the evaluation of modular forms at q = 1/phi (an algebraically distinguished point). The core coupling matches (alpha_s, sin^2(theta_W)) are its strongest claims. The fermion masses and many other quantities rely on searched formulas. The framework has been unusually honest about its own weaknesses (the EXTERNAL-TESTS.md and TAUTOLOGY-AUDIT.md documents are admirably self-critical).

The central unresolved question: **is the expected number of 99%+ matches from evaluating modular forms at a distinguished point and comparing to ~40 physical constants high enough to explain the observations by chance?** Until this calculation is done, the framework sits in an epistemically uncertain state — more structured than typical numerology, less rigorous than a physical theory.

**Key numbers:**
- Genuinely clean predictions (no search): ~5
- Total claimed: ~37
- Tautological or generic: ~7
- Searched but structurally connected: ~20
- Effective free inputs: ~3 (generous) to ~10 (conservative)
- Effective independent outputs: ~25 (after removing tautologies)
- Input/output ratio: 2.5:1 (conservative) to 8:1 (generous)

**The decisive tests:** alpha_s = 0.118404 (2026-2027 CODATA), sin^2(theta12) = 0.3071 (JUNO, ongoing), R = -3/2 (ELT/ANDES, ~2035). These are the framework's sharpest blades. If they cut, the framework is real. If they don't, it isn't.
