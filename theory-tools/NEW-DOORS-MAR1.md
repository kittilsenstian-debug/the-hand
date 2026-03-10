# NEW DOORS -- Mar 1 2026

*Genuinely new questions that emerged from today's work but have NOT been pursued.*
*Each door is labeled: COMPUTABLE (script-able in hours), RESEARCH (needs literature/math), or STRUCTURAL (conceptual).*

---

## Door 1: The Representation vs Dimension Problem [RESEARCH]

**The problem:** WHAT-IS-IT-REALLY (Section 4) states plainly: "The 248-dimensional representation of Th is NOT the adjoint of E8. It is the action of Th on a 248-dimensional space that has no proven connection to E8's Lie algebra structure."

This is the single most important mathematical question in the framework. The entire chain Monster -> Th -> E8 rests on a DIMENSION match (248 = 248), not a representation-theoretic identification.

**What would settle it:**

1. **Check if the 248-dim rep of Th decomposes as an E8 module.** Concretely: E8 has known subgroups. Does Th appear as a subgroup of Aut(E8) = E8 itself (the automorphism group of E8 is E8's Lie group)? If Th embeds in E8(F_q) for some finite field F_q, the 248-dim rep might restrict to the adjoint of E8. Known: E8(F_3) contains Th (Thompson 1976 -- this is literally how Thompson discovered it). So Th IS a subgroup of E8(F_3). The 248-dim rep of E8(F_3) restricts to Th. Does this restriction give the 248-dim irrep of Th, or does it decompose?

2. **The key reference:** Thompson's original paper (1976) and Griess-Ryba (1999, "Finite simple groups which projectively embed in an exceptional Lie group are classified!"). Griess and Ryba proved that Th embeds in E8(C) (the complex Lie group). This means the 248-dim adjoint of E8(C) restricts to a 248-dim representation of Th. The question is whether this restricted rep is IRREDUCIBLE (i.e., equals the 248-dim irrep of Th) or decomposes.

3. **If the restriction is irreducible:** The dimension match is NOT a coincidence -- it is a theorem. The 248-dim rep of Th IS the adjoint of E8, restricted. This would be a genuine mathematical result connecting sporadic groups to exceptional Lie algebras.

4. **If it decomposes:** The dimension match is indeed coincidental, and the chain weakens.

**Status:** This is KNOWN MATHEMATICS that nobody in the framework has looked up. Griess-Ryba (1999) likely settles it. The paper should be findable. Priority: URGENT. A single afternoon of literature search could either solidify or weaken the central chain.

**Prediction:** Based on Griess-Ryba proving Th embeds in E8(C), the restriction is very likely irreducible (otherwise the embedding would be into a proper subgroup, not into E8 itself). But this needs VERIFICATION, not assumption.

---

## Door 2: The Adelic Completion Problem [RESEARCH]

**The problem:** WHAT-IS-IT-REALLY (Section 1) identifies a genuine tension: coupling constants (eta(1/phi) = 0.11840...) are transcendental, but Z[phi] contains only algebraic numbers. The couplings live in the archimedean completion R, not in Z[phi] itself.

**The question nobody has asked:** Has anyone studied modular forms as adelic objects over Q(sqrt(5))? This is the natural mathematical setting.

**What's known:**

1. The Langlands program for GL(2) over Q(sqrt(5)) is partially developed. Hilbert modular forms over Q(sqrt(5)) are well-studied (Shimura, van der Geer, etc.).

2. Hilbert modular forms for Q(sqrt(5)) live on a 2-dimensional upper half-plane H x H, parametrized by (tau_1, tau_2) where tau_2 = sigma(tau_1) is the Galois conjugate. The "golden nome" q = 1/phi would give q_conjugate = -phi (the conjugate embedding). But |q_conjugate| = phi > 1, so the conjugate series DIVERGES. This is the Pisot property showing up in a new way.

3. The divergence of the conjugate series means: the framework's modular forms are NOT Hilbert modular forms in the usual sense. They live at a point where the archimedean completion at one place converges and at the other place diverges. This is a SPECIAL point in the adelic picture -- it is where the two archimedean completions of Q(sqrt(5)) behave maximally differently.

**New insight:** The Pisot property (|phi| > 1, |1/phi| < 1) means exactly that modular forms at q = 1/phi converge at one archimedean place and diverge at the other. This SELECTS a preferred archimedean place. "Our physics" = the place where the series converges. The "other side" = the place where it diverges. The dark sector might literally be the conjugate archimedean completion.

**Literature to search:**
- Bruinier, van der Geer, Harder, Zagier: "The 1-2-3 of Modular Forms" (Hilbert modular forms chapter)
- Gundlach: Hilbert modular surfaces for Q(sqrt(5))
- Doi-Naganuma lifting: connects elliptic modular forms to Hilbert modular forms

**Priority:** HIGH. This is the framework's natural mathematical habitat. Someone should check whether the point (tau, sigma(tau)) = (i*ln(phi)/2pi, i*ln(phi)/2pi) (both embeddings give the same tau because phi is totally positive) has any special properties in the Hilbert modular surface for Q(sqrt(5)).

**Correction to the above:** Actually, phi and its conjugate -1/phi have different signs. The two embeddings of Q(sqrt(5)) into R send sqrt(5) to +sqrt(5) and -sqrt(5). So phi maps to phi and to (1-sqrt(5))/2 = -1/phi. The nomes would be q_1 = exp(2*pi*i*tau) at one place and q_2 = exp(2*pi*i*sigma(tau)) at the other. If tau is purely imaginary with Im(tau) = ln(phi)/(2*pi), then q_1 = 1/phi. At the conjugate place... the tau value maps to the same imaginary part (ln is applied to |phi| at both places). So q_2 = 1/phi also. The conjugation acts on the COEFFICIENTS of the modular forms, not on the nome. This needs careful computation.

---

## Door 3: Other Self-Referential Universes [COMPUTABLE]

**The problem:** Gap D in ABSOLUTE-CORE-MAP asks: x^3 - x^2 - 1 = 0 has a Pisot root alpha_T = 1.46557... (the "tribonacci constant" -- smallest Pisot number of degree 3). Does it give a "universe"?

**What to compute:**

1. The ring Z[alpha_T] where alpha_T^3 = alpha_T^2 + 1.
2. The nome q = 1/alpha_T = 0.68233...
3. eta(q), theta_3(q), theta_4(q) at this nome.
4. Do any combinations match physical constants? If so, WHICH ones? If not, does the failure mode tell us something?

**Key differences from the golden case:**
- Degree 3, not 2. The minimal polynomial is cubic. Z[alpha_T] has rank 3 over Z (vs rank 2 for Z[phi]).
- Galois group is S_3 (vs Z_2 for Q(sqrt(5))). This gives a BIGGER Galois group acting on the modular forms.
- The Pisot property still holds (|alpha_T| > 1, both conjugates have |z| < 1). But there are TWO conjugates, both inside the unit circle. The "dark sector" would be 2-dimensional, not 1-dimensional.
- Modular forms at q = 0.682 are further from the cusp than q = 0.618. Still non-perturbative, but less so.

**What FAILURE would mean:** If q = 1/alpha_T gives garbage (no coupling matches at all), it strengthens the claim that the golden ratio is uniquely selected. The failure mode would show that the nome-coupling correspondence is specific to q = 1/phi, not a generic feature of Pisot nomes.

**What SUCCESS would mean:** If it gives a different consistent set of couplings, the framework predicts MULTIPLE possible universes parametrized by Pisot numbers. The golden ratio would be "our" universe, the tribonacci constant would be "another" universe, etc. The number of Pisot numbers is countable, so the number of possible universes would be countable.

**Known:** There are exactly 2 Pisot numbers below the golden ratio: 1 (trivial, degree 1) and the smallest Pisot number theta_0 = 1.32472... (root of x^3 - x - 1 = 0). Should also compute modular forms at q = 1/theta_0 = 0.75488.

**Effort:** A few hours. Model on nome_uniqueness_scan.py.

---

## Door 4: The 194 -> 25 Question [COMPUTABLE]

**The problem:** The SM has ~25 free parameters (6 quark masses, 3 lepton masses, 3 neutrino masses, 3 CKM angles + 1 phase, 3 PMNS angles + 1 phase, 3 coupling constants, Higgs mass, Higgs VEV = 25). The Monster has 194 conjugacy classes. Is 25 a meaningful fraction of 194?

**Observations nobody has made:**

1. 194 - 25 = 169 = 13^2. Is this algebraically meaningful? 13 is the largest prime dividing |M11| = 7920 = 2^4 * 3^2 * 5 * 11. But 13 does NOT divide |M11|. It divides |M| though (Monster order includes 13^3). So 13^2 is a natural number in Monster arithmetic.

2. 194 = 2 * 97. 97 is prime. Is 97 special? 97 = 100 - 3. Not obviously meaningful.

3. Better decomposition: count by type.
   - 194 conjugacy classes of M give 194 McKay-Thompson series
   - But only 171 DISTINCT genus-0 groups (Cummins-Gannon 2003)
   - So 194 - 171 = 23 classes share genus-0 groups with other classes
   - 23 = dimension of the Leech lattice minus 1. Coincidence? (Leech = 24 dimensions, but 23 is the dimension of the lattice's "shadow" -- the vectors perpendicular to a fixed minimal vector.)
   - 171 = 9 * 19 = (3^2) * 19. 19 divides |M|.

4. A more productive question: of the 194 McKay-Thompson series, HOW MANY are needed to determine the modular forms eta, theta_3, theta_4 at q = 1/phi? Since eta and theta are weight-1/2 forms and the McKay-Thompson series are weight-0 functions, the connection goes through the Monster VOA partition function. The answer might be: very few (maybe 3-5 conjugacy classes suffice to pin down the level-2 structure). The OTHER 189+ classes would then encode ADDITIONAL physics beyond the SM.

**What to compute:** Given the known table of McKay-Thompson series (available in ATLAS or in Borcherds' tables), which conjugacy classes have series that distinguish q = 1/phi from other nomes? In other words: how many of the 194 series are needed to prove "the nome is 1/phi"?

**Priority:** MEDIUM. The 194 = 25 + 169 decomposition is probably coincidence. The "how many classes pin down the nome" question is genuinely interesting.

---

## Door 5: Breaking the QM Circularity [STRUCTURAL]

**The problem:** ABSOLUTE-CORE-MAP Gap F identifies a genuine circularity. The framework uses the Schrodinger equation to find the PT bound states of V(Phi), then claims to "derive" quantum mechanics from those bound states. The Schrodinger equation is assumed in order to derive it.

**Three possible escape routes:**

**Route A: Derive the Schrodinger equation from the domain wall.**

The domain wall profile Phi(x) = phi * tanh(kappa*x) + 1/2 is a CLASSICAL solution. The fluctuation equation around it is:

  [-d^2/dx^2 + V''(Phi(x))] * psi = omega^2 * psi

This is the Schrodinger equation in disguise (with V_eff = V''(Phi)). But this fluctuation equation comes from LINEARIZING the classical field equation, not from quantum mechanics. The eigenvalue problem is the same as Sturm-Liouville theory, which predates QM by a century.

**The insight:** The PT eigenvalue problem is NOT intrinsically quantum. It is a classical eigenvalue problem for small perturbations around a soliton. The SPECIFIC feature that becomes "quantum" is:
- Discrete eigenvalues = quantization
- Orthogonality of eigenmodes = superposition
- Reflectionless potential = unitarity

So the claim could be: QM is what soliton perturbation theory looks like to an internal observer. The Schrodinger equation is derived FROM the classical field equation BY linearization around the kink. No QM is assumed -- it EMERGES from classical field theory + self-referential observation.

**Route B: Spectral theory without QM.**

The PT potential is a special case of Lame equation, which is pure 19th-century mathematics (Lame 1837, Hermite 1877). The eigenvalue problem, bound states, and scattering matrix are all computable without any reference to quantum mechanics. The framework could DEFINE quantum mechanics as "the spectral theory of the golden kink fluctuation operator." This is not circular because spectral theory is older than QM.

**Route C: Categorical approach.**

Define a "self-referential fluctuation category" whose objects are sections of a sheaf over the kink background and whose morphisms are the spectral projections. Show that this category has the structure of a Hilbert space (innerproduct from the L^2 pairing on the kink background). The "quantization" is then a THEOREM about this category, not an assumption.

**Priority:** HIGH for Route A (it's the simplest and most compelling). The key claim is: the Schrodinger equation is the linearized classical field equation around a soliton. This is standard mathematical physics but reframed as a derivation of QM.

---

## Door 6: Domain Wall Holography [RESEARCH]

**The problem:** Gap H in ABSOLUTE-CORE-MAP notes that the framework has a natural holographic structure: the domain wall is a brane, the modular forms are conformal, and the wall lives in one dimension lower than the bulk. But nobody has explored whether there is an AdS/CFT structure.

**What's already in place:**

1. The SMS theorem (Shiromizu-Maeda-Sasaki 2000) derives Einstein equations on the wall from bulk gravity. This IS holography -- 4D gravity from 5D bulk, mediated by a brane.

2. The modular forms live on the upper half-plane (2D). The domain wall is 1D. The physical spacetime is 3+1D. The dimensions are: 2D (modular surface) -> 1D (wall) -> 4D (spacetime). The "extra" dimensions come from the E8 internal space.

3. The c = 2 CFT identification (from PT n = 2 bound states giving central charge c = 2) is exactly the right structure for a holographic boundary theory. A c = 2 CFT has specific operator content that could be matched to the PT spectrum.

**New observations:**

4. **Domain wall holography is a real research field.** Key papers: DeWolfe-Freedman-Gubser-Horowitz (2000, "Integrating out geometry: holographic Wilsonian RG for general spacetimes"), Bak-Gutperle-Hirano (2003, "domain wall/QFT correspondence"), Skenderis-Townsend (1999, "domain walls and moduli flow"). These are not fringe papers -- they are mainstream string theory. The SPECIFIC setup (quartic potential, PT bound states, modular form boundary conditions) has NOT been studied, but the general framework exists.

5. **The modular form boundary conditions are NEW.** Standard domain wall holography uses exponential potentials (supergravity) or polynomial potentials with integer exponents. Nobody has studied a wall where the boundary theory is organized by level-2 modular forms. This could be a genuinely new contribution to the holography literature, independent of whether the framework's physical claims are correct.

6. **The PT potential is special in holography.** The PT potential is one of a handful of exactly solvable potentials in quantum mechanics. In the holography context, exact solvability means the bulk-to-boundary propagator can be computed in closed form. This would give EXACT holographic correlators -- a rare and valuable thing in AdS/CFT.

**Concrete computation:** Write the 5D bulk metric for a domain wall with V(Phi) = (Phi^2 - Phi - 1)^2, solve the linearized bulk equations, and compute the holographic 2-point function. If the 2-point function organizes as a modular form at q = 1/phi, that would be a significant result.

**Priority:** MEDIUM-HIGH. This connects to mainstream physics literature. Even if the framework's specific claims fail, the mathematical structure (exactly solvable domain wall holography with modular boundary conditions) might be publishable.

---

## Door 7: The F4/E6 Coincidence [COMPUTABLE]

**The problem:** F4 and E6 both have Coxeter number h = 12. F4 is non-simply-laced (two root lengths). E6 is simply-laced (one root length). They share Coxeter number but have different rank (4 vs 6), different dimension (52 vs 78), and different structure.

**What this means in the framework:**

1. h(E6)/6 = 2 = F(3) (Fibonacci). h(F4)/6 = 2 = F(3) (same). So F4 and E6 sit at the SAME Fibonacci depth. In the exceptional chain types framework, E6 = lepton type (d = 2). F4 shares this depth.

2. F4 is the automorphism group of the exceptional Jordan algebra J3(O) (3x3 Hermitian matrices over the octonions). E6 is the automorphism group of the COMPLEXIFIED exceptional Jordan algebra J3(O_C). So F4 = "real" version, E6 = "complex" version. In the framework, does this mean: F4 = Level 0 (real, undifferentiated) lepton, E6 = Level 1 (complex, differentiated) lepton?

3. The Freudenthal-Tits magic square connects F4, E6, E7, E8 through tensor products of composition algebras. In this square:
   - F4 = R tensor O (reals x octonions)
   - E6 = C tensor O (complexes x octonions)
   - E7 = H tensor O (quaternions x octonions)
   - E8 = O tensor O (octonions x octonions)

   The progression R -> C -> H -> O is the same as the Cayley-Dickson construction. In the framework, this maps to: Level 0 (F4, real) -> lepton (E6, complex) -> down (E7, quaternionic) -> up (E8, octonionic). The levels of self-reference INCREASE with the composition algebra.

4. F4 contains G2 as a subgroup (G2 = automorphisms of octonions, F4 = automorphisms of exceptional Jordan algebra built from octonions). The framework maps G2 to Level 0 (the Ly fiber at p = 5). So the chain is: G2 (Level 0, octonion automorphisms) -> F4 (Jordan algebra, "structured nothing") -> E6 (complexified, leptons emerge).

**Concrete question:** Does dim(F4) = 52 appear anywhere in the framework? 52 = 4 * 13. 13 appears in the Monster order. But more relevantly: 78 - 52 = 26 = dim(bosonic string target). Is this meaningful?

Also: 248 - 78 = 170 = 2 * 5 * 17. 248 - 52 = 196 = 14^2 = 196. And 196883 - 248 = 196635 (the "hidden" Monster dimensions). 196 and 196635 share the prefix 196 -- likely coincidence, but worth noting.

**What to compute:** The full magic square structure evaluated at q = 1/phi. If each entry of the 4x4 magic square gives a coupling constant, we would get 16 numbers. Do any of them match physical quantities beyond the 4 already used (E6, E7, E8, and possibly F4)?

**Priority:** MEDIUM. The magic square connection is mathematically deep but might be a dead end for physics.

---

## Door 8: What Do Conway Groups Control? [STRUCTURAL]

**The problem:** Co1, Co2, Co3 are the automorphism groups of the Leech lattice (Co1 = Aut(Leech)/Z2, Co2 = stabilizer of a type-2 vector, Co3 = stabilizer of a type-3 vector). The framework maps the Leech lattice to Level 2. But what SPECIFIC physics do the Conway groups control?

**What's known:**

1. Co1 has min rep 276 (faithful). But it also acts on a 24-dim space (the Leech lattice itself, not faithfully -- the center acts trivially). The 24-dim action of Co1 on the Leech lattice gives the Leech lattice automorphism structure.

2. The Leech lattice has 196560 minimal vectors (norm 4 in the standard normalization). These organize into shells: 196560 at norm 4, 16773120 at norm 6, etc. The theta function of the Leech lattice is a modular form of weight 12 for SL(2,Z).

3. The Monster VOA has c = 24 = rank(Leech). The Leech lattice VOA is a SUB-VOA of the Monster VOA. The Monster VOA = Leech lattice VOA + twisted sector. So the Leech lattice is the "ground floor" and the Monster adds the "twisted floor."

**New question:** If the Monster controls Level 1 physics (SM, forces, particles), what does the Leech lattice sub-structure control?

**Hypothesis:** The Leech lattice controls the DARK SECTOR. Evidence:
- Level 2 wall tension ratio = 5.41, matching Omega_DM/Omega_b at 0.73 sigma.
- The Leech lattice has no roots (no vectors of norm 2). This means: no gauge bosons in the dark sector. No forces. Dark matter is UNCHARGED. This matches observation.
- The 196560 minimal vectors at norm 4 could correspond to dark matter states. They are heavier than massless (norm > 2) but lighter than typical massive states. This gives a natural WIMP-scale if the norm-mass correspondence works.

**What Co2 and Co3 might do:** Co2 and Co3 are stabilizers of different-type vectors in the Leech lattice. Different vector types could correspond to different dark matter species. Co2 (type-2 stabilizer) might control the lightest dark particle. Co3 (type-3 stabilizer) might control the next species.

**Concrete check:** The rep dimensions of Co2 are 23, 253, 275, 2024, 2277. The number 23 = Leech rank - 1. Does 253 = 23*11 = C(23,2) appear in dark matter models? Does 2024 appear? (Note: 2024 also appears in Co3's reps.)

**Priority:** MEDIUM. The "Leech = dark sector" hypothesis is testable within the framework but requires understanding what "dark sector physics" means concretely.

---

## Door 9: The Baby Monster Mystery [RESEARCH]

**The problem:** The Baby Monster B has minimal representation dimension 4371. It sits between the Monster (min rep 196883) and the rest of the Happy Family. The dimension 4371 does not match any obvious Lie algebra dimension.

**Observations:**

1. 4371 = 3 * 1457. 1457 = 31 * 47. Both 31 and 47 divide |M| (Monster order). 47 is the framework's "anomalous" prime (only inert Monster-only prime, Pisano period 1/3 of max).

2. 4371 = 4096 + 275 = 2^12 + 275. Is this meaningful? 2^12 = 4096 is the number of elements in GF(2)^12 (the binary vector space of dimension 12 = fermion count). 275 = C(24,2) + C(24,1) + 1 = ... no, 275 = 11 * 25 = 11 * 5^2. More usefully: 276 = C(24,2) = min faithful rep of Co1. So 4371 = 2^12 + 276 - 1 = 4096 + 275. The "minus 1" is suspicious.

3. Better decomposition: The Baby Monster is a double cover of a centralizer in the Monster. Specifically, if you take an involution (element of order 2) in the Monster, its centralizer has shape 2.B (a double cover of B). The 4371-dim rep decomposes as 4371 = 4371 under the Baby Monster's action on the "transposition class" of the Monster.

4. The OTHER small reps of B: 96255 and 96256. Note 96256 = 2^16 * 3/2... no. 96256 = 96256. Let me check: 96256 = 2^10 * 94 = 1024 * 94? No, 1024 * 94 = 96256. And 94 = 2 * 47. There's 47 again. So 96256 = 2^11 * 47. That's striking: the prime 47 (the framework's anomalous prime) appears in the Baby Monster's representation dimension.

5. 96255 = 96256 - 1 = 2^11 * 47 - 1. The pair (96255, 96256) differs by 1, like (196883, 196884) for the Monster. For the Monster: 196884 = 2^2 * 3 * 47 * 349. There's 47 again.

**New conjecture:** The prime 47 plays a distinguished role connecting the Monster, Baby Monster, and the framework. It appears in:
- |M|: as a factor of the Monster order
- Baby Monster: 96256 = 2^11 * 47
- Pisano period: pi(47) = 32 = (1/3) * 96, anomalously small
- Monster: 196884 = 4 * 3 * 47 * 349

**What to investigate:** Is there a chain Monster -> B -> ? that parallels Monster -> j -> E8? Does the Baby Monster's 4371-dim rep have Lie-algebraic structure the way Th's 248-dim rep has E8 structure?

**Key reference to find:** Norton's "Anatomy of the Monster" and any work on B's representation theory by Wilson or Linton.

**Priority:** LOW-MEDIUM. The Baby Monster is well-studied but its role in physics frameworks is not. The 47 connection is potentially important.

---

## Door 10: Coxeter Number Sum = 80 [COMPUTABLE]

**The observation (from the user):** Sum of Coxeter numbers for the E-series:
h(E8) + h(E7) + h(E6) + h(D5) + h(A4) + h(A3) + h(A2) + h(A1) = 30 + 18 + 12 + 8 + 5 + 4 + 3 + 2 = 82

Wait -- let me recalculate. The E-series in Dynkin diagram terms is:
- E8: h = 30
- E7: h = 18
- E6: h = 12
- D5: h = 8
- A4: h = 5
- A3: h = 4
- A2: h = 3
- A1: h = 2

Sum = 30 + 18 + 12 + 8 + 5 + 4 + 3 + 2 = 82. NOT 80. Close but not exact.

**However**, the user's original suggestion was about E-series Coxeter numbers. Let me check the chain differently. The GUT chain is E8 -> E7 -> E6 -> SO(10) = D5 -> SU(5) = A4. If we sum just the exceptional part:

h(E8) + h(E7) + h(E6) = 30 + 18 + 12 = 60 = |A5| = |icosahedral group|. (This is already known from today's work.)

If we include D5: 60 + 8 = 68.
If we include A4: 68 + 5 = 73.
If we include A3: 73 + 4 = 77.
If we include A2: 77 + 3 = 80. BINGO.

So: **h(E8) + h(E7) + h(E6) + h(D5) + h(A4) + h(A3) + h(A2) = 80 = the hierarchy exponent.**

This sum includes ALL algebras from E8 down to A2 (= SU(3)) in the GUT chain, EXCLUDING A1 (= SU(2) = the electroweak partner). The sum equals 80 = 2 * (240/6) = the exponent in phibar^80.

**Is this meaningful or coincidence?**

Arguments for meaningful:
- The sum runs over exactly the algebras in the E8 -> SM breaking chain, stopping at the color algebra SU(3) = A2.
- Excluding A1 is natural if A1 is the "bridge" (electroweak symmetry breaking generates mass, which is the LAST step before observation).
- 80 = 2 * 40, and there are exactly 40 A2 hexagons in E8 (proven). Each hexagon contributes one phibar^2 = one T^2 iteration. 80 = sum of Coxeter numbers = 2 * (number of hexagons). The factor 2 might be: each hexagon is visited TWICE (once for each vacuum, phi and -1/phi).

Arguments against:
- The "GUT chain" E8 -> E7 -> E6 -> D5 -> A4 -> A3 -> A2 is a specific CHOICE of breaking chain. Other chains exist (e.g., E8 -> D8 -> ...). The sum depends on which chain you choose.
- 82 (including A1) does not equal 80. The exclusion of A1 is ad hoc unless justified.
- Coxeter numbers grow roughly linearly with rank, so the partial sums of any decreasing sequence will hit near any target number eventually.

**What to compute:**
1. Do OTHER breaking chains give 80? E.g., E8 -> D8 -> D7 -> ... -> D4 -> A3 -> A2 -> A1: h = 30+14+12+10+8+6+4+3+2 = 89. Does NOT give 80.
2. Is E8 -> E7 -> E6 -> D5 -> A4 -> A3 -> A2 the UNIQUE chain summing to 80? This is a finite check.
3. The product h(E8) * h(E7) * h(E6) = 30 * 18 * 12 = 6480 = 2^4 * 3^4 * 5. Does 6480 appear anywhere? 6480 = 6! * 9 = 720 * 9. Or 6480 = 8! / (8-3)! * ? ... 8 * 810 = 6480. Not obviously meaningful. But: 6480/240 = 27 = 3^3 = dim(fund(E6)). So h(E8)*h(E7)*h(E6)/|roots(E8)| = dim(fund(E6)). This IS a known identity (or should be checked).

**Priority:** HIGH. The sum = 80 result is trivially computable and either strengthens or weakens the hierarchy exponent's derivation.

---

## Door 11: The Schrodinger Equation from Sturm-Liouville [STRUCTURAL]

**Expanding on Door 5, Route A.** This deserves its own door because it's potentially the most important conceptual advance available.

The linearized classical field equation around a static kink is:

  delta^2 L / delta Phi^2 |_{Phi=Phi_kink} * psi = 0

which gives:

  [-d^2/dx^2 + V''(Phi_kink(x))] * psi_n = lambda_n * psi_n

This is mathematically identical to the time-independent Schrodinger equation. But it is derived from CLASSICAL field theory -- specifically, from the condition that the second variation of the action around the kink solution is stationary. No quantum mechanics is assumed. No hbar appears (it can be set to 1 by choice of units, or equivalently, it IS the kink's natural frequency scale).

**The deeper point:** The full time-dependent Schrodinger equation i*hbar * d|psi>/dt = H|psi> has two features beyond the eigenvalue problem:
1. The factor of i (imaginary unit) -- which makes it a WAVE equation rather than a diffusion equation.
2. The first-order time derivative -- which gives UNITARY evolution.

Both features follow from the domain wall setup:
1. The factor of i comes from the Pisot property: the kink's fluctuation spectrum is OSCILLATORY (bound states have real frequencies), not decaying, because the PT potential is reflectionless. The reflectionless condition forces the phase shifts to be real, which requires i in the time evolution.
2. The first-order time derivative comes from the CHIRAL zero mode (Jackiw-Rebbi 1976). The zero mode satisfies a first-order equation (Dirac, not Klein-Gordon). The full spectrum inherits this first-order structure from the zero mode's chirality.

**If this argument holds:** The Schrodinger equation is DERIVED, not assumed. The circle in Gap F is broken. QM is what linearized classical soliton field theory looks like when the soliton has a PT potential (reflectionless + chiral zero mode).

**What's needed:** A clean mathematical derivation showing that linearized field theory around a reflectionless soliton with chiral zero modes NECESSARILY gives the Schrodinger equation. This should be findable in the soliton literature (Rajaraman 1982, Manton-Sutcliffe 2004) but reframed.

---

## Door 12: Holomorphic Anomaly and the Framework [RESEARCH]

**A door nobody has opened.** The holomorphic anomaly equation (BCOV 1993) controls the modular dependence of topological string partition functions:

  d_bar F_g = (1/2) C_bar^{ij} (D_i D_j F_{g-1} + sum_{r=1}^{g-1} D_i F_r * D_j F_{g-r})

This equation governs how the genus-g contribution to the topological string changes as you move on the moduli space of Calabi-Yau manifolds. At q = 1/phi, we are at a SPECIFIC point on such a moduli space. The holomorphic anomaly equation at this point would give CORRECTIONS to the tree-level coupling constants.

**Connection to the framework:** The VP corrections (1-loop, 2-loop, etc.) to alpha might BE the holomorphic anomaly corrections evaluated at q = 1/phi. If so:
- The 1-loop correction alpha*ln(phi)/pi is the genus-1 holomorphic anomaly.
- The 2-loop correction (alpha/pi)^2 * (5 + 1/phi^4) is the genus-2 contribution.
- The all-orders summation (the self-consistent fixed point giving 10.2 sig figs) is the solution to the holomorphic anomaly equation.

**What to check:** The holomorphic anomaly equation for a 1-parameter family of Calabi-Yau manifolds whose complex structure modulus is tau = i*ln(phi)/(2*pi). Is the resulting tower of corrections consistent with the framework's perturbative expansion?

**Priority:** MEDIUM. Requires topological string theory expertise. But if it works, it connects the framework to mainstream string mathematics and provides a DERIVATION of the VP corrections from first principles.

---

## Door 13: The Full ADE Classification [COMPUTABLE]

**Nobody has checked:** The ADE classification (A_n, D_n, E_6, E_7, E_8) classifies singularities, platonic solids, subgroups of SU(2), simply-laced Dynkin diagrams, and many other mathematical objects. The framework uses E8 exclusively. But the FULL ADE classification might organize more physics.

**Specifically:**

1. The ADE groups are classified by their Coxeter numbers:
   - A_n: h = n+1
   - D_n: h = 2(n-1)
   - E_6: h = 12
   - E_7: h = 18
   - E_8: h = 30

2. The McKay correspondence maps each ADE group to a finite subgroup of SU(2):
   - A_n -> Z_{n+1} (cyclic)
   - D_n -> Dic_{n-2} (binary dihedral)
   - E_6 -> Binary tetrahedral (2T, order 24)
   - E_7 -> Binary octahedral (2O, order 48)
   - E_8 -> Binary icosahedral (2I, order 120)

3. At q = 1/phi: the binary icosahedral group (2I) has order 120 = 2 * |A5| = 2 * 60. The icosahedral connection is already known in the framework (icosahedral cusp identity). But the OTHER McKay correspondences at q = 1/phi are unexplored.

**Question:** The binary tetrahedral group (2T, order 24) maps to E6. The Leech lattice has c = 24. Is there a direct connection between 2T and the Leech lattice? (Answer: YES -- the Leech lattice can be constructed from the E8 lattice using a "tripling" construction, and 24 = 3 * 8 = rank(Leech).) Does evaluating E6 modular forms (if such a thing exists) at q = 1/phi give lepton physics?

**What to compute:** For each ADE group, evaluate the corresponding McKay correspondence structure at q = 1/phi. Do the A-type groups give anything? (A_4 = SU(5), h = 5 = F(5)/6 * 6 = h(E8)/6... no, h(A4) = 5 = h(E8)/6. This is the Fibonacci depth of the up-type. Already noticed.)

**Priority:** MEDIUM. The full ADE structure at the golden nome is unexplored territory.

---

## Door 14: The Iwasawa Main Conjecture for Q(sqrt(5)) [RESEARCH]

**The deepest possible connection.** The Iwasawa main conjecture (proved by Mazur-Wiles for Q, Wiles for totally real fields) connects:
- The p-adic L-function of a number field (analytic side)
- The structure of ideal class groups in Z_p-extensions (algebraic side)

For Q(sqrt(5)):
- The p-adic L-functions at each prime p encode arithmetic information about Z[phi] in a tower of field extensions.
- The class number of Q(sqrt(5)) is 1 (trivial class group), so the main conjecture takes a simple form.
- But the CYCLOTOMIC Z_p-extensions are non-trivial and might encode physics.

**Why this matters:** If the framework is correct that "physics = arithmetic of Z[phi]," then the Iwasawa theory of Q(sqrt(5)) IS the deep theory of physics. The p-adic L-functions would encode coupling constants at each energy scale (via the Iwasawa tower). The main conjecture would guarantee that these coupling constants are self-consistent.

**Specific question:** The Kubota-Leopoldt p-adic L-function of Q(sqrt(5)) at p = 5 (the ramification prime) is degenerate. What happens? This is the framework's "Ly fiber" in the language of Iwasawa theory.

**Priority:** LOW (requires professional number theorist). But if the connection exists, it provides the framework's missing PROOF of why q = 1/phi is forced.

---

## Door 15: The 2-3 Oscillation and Hexagonal Structure [COMPUTABLE]

**New correlation to test:** The 2-3 oscillation (Z2 x Z3 = Z6) predicts that the hierarchy has hexagonal structure. The golden ratio phi = (1+sqrt(5))/2 satisfies phi^6 = 8*phi + 5, which connects the 6th power to 8 and 5 (Fibonacci numbers).

**Concrete tests:**

1. The nesting cascade has levels: dark energy -> BH -> star -> planet -> organism -> cell. That is 6 levels. Predicted by Z6.

2. The "measurement levels" identified on Feb 28 go: Level 0 (algebra) -> Level 3 (eyes) -> Level 7 (shamanism) -> Level 10 (science) -> Level 11 (QM) -> Level 12 (this framework). The GAPS are: 3, 4, 3, 1, 1. These sum to 12 = 2 * 6. Is the hexagonal periodicity visible?

3. Hexagonal tilings have exactly 3 neighbors per vertex (in the honeycomb lattice) and exactly 6 neighbors per face (in the triangular lattice). The 2-3 oscillation maps to: faces have 6 (= 2*3) edges, vertices have 3 edges, edges have 2 endpoints. This is the Euler formula for planar graphs: V - E + F = 2. For the infinite honeycomb: each vertex has 3 edges, each edge has 2 faces, each face has 6 edges. So 3/2 * V = E, 6/2 * F = E. Euler: V - E + F = 0 (for infinite planar). So V = 2E/3, F = E/3. The ratio V:E:F = 2:3:1 = 2:3:1. The 2 and 3 appear as the vertex-to-edge and edge-to-face ratios.

**Priority:** LOW-MEDIUM. The Z6 periodicity is the easiest structural prediction to test.

---

## CORRELATIONS TO TEST (from today's work)

### C1. Sum of exceptional Coxeter numbers = 60 = |A5|
h(E8) + h(E7) + h(E6) = 30 + 18 + 12 = 60.
|A5| = 60 (order of alternating group, = rotational icosahedral symmetry).
Already noted in `fibonacci_coxeter_deep.py`. Question: is this a THEOREM or a coincidence? The connection through the icosahedral group suggests it should be provable.

### C2. h(E8)*h(E7)*h(E6)/|roots(E8)| = 6480/240 = 27 = dim(fund(E6))
Is this known? It connects the Coxeter numbers of all three exceptional algebras to the fundamental representation of the smallest one.

### C3. Coxeter number chain sum to 80
h(E8) + h(E7) + h(E6) + h(D5) + h(A4) + h(A3) + h(A2) = 80.
See Door 10 for full analysis.

### C4. Baby Monster and p = 47
96256 = 2^11 * 47. 196884 = 4 * 3 * 47 * 349. The prime 47 connects Monster and Baby Monster representation dimensions. Framework identifies p = 47 as anomalous (Pisano period 1/3 of max, only inert Monster-only prime).

### C5. 4371 = 2^12 + 275 = 4096 + 275
Baby Monster min rep decomposes as (binary 12-vectors) + (Co1 faithful rep - 1)? Check: 275 = 276 - 1. This would mean: B's action on 4371 dimensions decomposes as "12 fermion positions in binary" + "Leech lattice automorphism (minus trivial)." If true, B connects fermions (12) to dark sector (Leech/Co1).

### C6. Magic square at golden nome
The Freudenthal-Tits magic square: R, C, H, O tensor R, C, H, O gives 16 Lie algebras. What are their dimensions? R tensor O = F4(52), C tensor O = E6(78), H tensor O = E7(133), O tensor O = E8(248). The OTHER 12 entries include A1(3), A2(8), C3(21), F4(52), A2(8), A2xA2(16), A5(35), E6(78), C3(21), A5(35), D6(66), E7(133), F4(52), E6(78), E7(133), E8(248). Evaluate the modular forms associated with each at q = 1/phi.

### C7. The 194 - 171 = 23 split
194 conjugacy classes, 171 distinct genus-0 groups, 23 shared. Is 23 the same 23 as rank(Leech) - 1?

---

## PRIORITY RANKING

**Immediate (hours, potentially decisive):**
1. **Door 1** (Griess-Ryba literature search) -- settles whether Th -> E8 is rigorous or numerological
2. **Door 10** (Coxeter sum = 80) -- trivially computable, could strengthen hierarchy exponent
3. **Door 3** (tribonacci universe) -- compute modular forms at q = 1/alpha_T and q = 1/theta_0

**Short-term (days):**
4. **Door 5/11** (QM from soliton linearization) -- clean up the circularity
5. **Door 7** (magic square at golden nome) -- systematic check of all 16 entries
6. **Door 4** (194 classes: which ones pin down the nome?) -- number theory computation

**Medium-term (weeks, needs literature):**
7. **Door 6** (domain wall holography with PT potential) -- publishable if it works
8. **Door 2** (Hilbert modular forms for Q(sqrt(5))) -- the natural mathematical setting
9. **Door 12** (holomorphic anomaly = VP corrections) -- needs topological string expertise
10. **Door 8** (Conway groups and dark sector) -- requires Leech lattice rep theory

**Long-term (research program):**
11. **Door 9** (Baby Monster 4371) -- deep group theory
12. **Door 14** (Iwasawa main conjecture) -- needs professional number theorist
13. **Door 13** (full ADE at golden nome) -- systematic but large

---

*15 new doors. 7 new correlations to test. None of these appear in ALL-OPEN-DOORS.md.
The single most urgent action is Door 1: look up Griess-Ryba 1999 and determine whether Th's 248-dim rep IS the adjoint of E8 restricted, or merely dimension-matched. This settles the central mathematical question of the entire framework.*

*Written Mar 1 2026.*
