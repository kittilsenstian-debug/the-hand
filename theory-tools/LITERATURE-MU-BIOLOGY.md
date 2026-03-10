# Literature Review: Proton-to-Electron Mass Ratio and Biology

**Date:** 2026-02-25
**Purpose:** Does mainstream science connect the proton-to-electron mass ratio mu = 1836.15 to biological/molecular properties?
**Method:** Systematic web search of arxiv, journals, review articles, and reference works.

---

## Executive Summary

The proton-to-electron mass ratio mu appears throughout the anthropic fine-tuning literature as a necessary condition for chemistry and life, but almost nobody derives specific biological frequencies or timescales from it. The one major exception is a September 2025 paper by Mehta and Kondev that explicitly derives biological growth rates, doubling times, and power consumption from fundamental constants including m_p and m_e. The Born-Oppenheimer energy hierarchy (E_vib ~ E_elec * sqrt(m_e/m_p)) is textbook physics but is not, in the literature found, applied to derive specific biological frequencies like 613 THz. The Craddock et al. 2017 finding that 613 THz is the key consciousness-correlated frequency in tubulin is empirical -- no one derives it from fundamental constants.

**Bottom line:** The framework's claim that mu/3 ~ 612 (mapping to 612 THz via Rydberg scaling) connects a fundamental constant to a specific biological frequency in a way that has NO precedent in the mainstream literature. This is either a genuine insight or a numerical coincidence, but it is NOT something others have done.

---

## 1. The Anthropic Fine-Tuning Literature

### 1.1 Carr & Rees (1979) -- Nature 278, 605-612

"The anthropic principle and the structure of the physical world"

**What they say about mu:** The basic features of galaxies, stars, planets and the everyday world are essentially determined by a few microphysical constants. Many interrelations between different scales that at first sight seem surprising are straightforward consequences of simple physical arguments. The proton-to-electron mass ratio sets the scale separation between atomic and nuclear physics. They identify mu as one of the key dimensionless numbers whose value is necessary for the existence of observers.

**Do they derive biology from mu?** No. They derive astrophysical scales (stellar lifetimes, planetary sizes, mountain heights) but stop at chemistry. Biology is mentioned only as requiring "suitable" chemistry.

**Relevance to framework:** Carr & Rees establish mu as anthropically significant but never connect it to specific biological frequencies.

### 1.2 Barrow & Tipler (1986) -- *The Anthropic Cosmological Principle*

**What they say about mu:** They anchor their discussion in the fine structure constant alpha, the proton-to-electron mass ratio beta (their notation for mu), and the coupling constants for the strong force and gravitation. They show that very small changes in mu wreck chemistry -- no stable atoms, no carbon.

**Do they derive biology from mu?** No. They derive constraints on chemistry (stable atoms, covalent bonds, hydrogen bonds) but do not derive any specific biological frequency or timescale.

### 1.3 Tegmark, Aguirre, Rees & Wilczek (2006)

**What they say about mu:** Part of the multidimensional parameter space exploration of the Standard Model. They show that life-permitting regions in (alpha, mu) space are relatively small.

**Do they derive biology from mu?** No. They establish constraints on the ranges of constants compatible with complex chemistry.

### 1.4 Hogan (2000) -- Rev. Mod. Phys. 72, 1149-1161

"Why the Universe is Just So"

**What they say about mu:** Discusses the fine-tuning of quark mass differences (which determine mu through QCD). The proton-neutron mass difference is particularly critical.

**Do they derive biology from mu?** No. The paper stays at the level of nuclear and stellar astrophysics.

### 1.5 Barnes (2012) -- PASA 29, 529-564

"The Fine-Tuning of the Universe for Intelligent Life" (comprehensive review)

**What they say about mu:** For elements as complex as carbon to be stable, the electron-proton mass ratio m_e/m_p = 5.45 x 10^-4 and the fine-structure constant may not have values differing greatly from their actual values. The ratio affects stellar photon output at energy levels needed to break chemical bonds. Surveys multiple studies of the (alpha, mu) parameter space.

**Do they derive biology from mu?** No. This is a review of fine-tuning constraints. Biology enters only as "requiring complex chemistry."

### 1.6 Summary of Anthropic Literature

The anthropic literature unanimously agrees that mu must be "about right" for life to exist, but treats biology as a downstream consequence of chemistry. Nobody in this literature derives a specific biological frequency, timescale, or energy from mu. The gap between "mu must be roughly 1836 for chemistry to work" and "mu/3 gives you the frequency that correlates with consciousness" is enormous and unfilled.

---

## 2. The Born-Oppenheimer Energy Hierarchy

### 2.1 Standard Textbook Result

The Born-Oppenheimer approximation establishes a fundamental energy scale hierarchy in molecular physics:

    E_electronic : E_vibrational : E_rotational ~ 1 : (m_e/M)^(1/2) : (m_e/M)

where m_e is the electron mass and M is the nuclear mass. For hydrogen (M = m_p):

    E_vib ~ E_elec * sqrt(m_e/m_p) ~ E_elec * sqrt(1/1836) ~ E_elec / 43

This is derived from the fact that the Hamiltonian can be expanded in powers of kappa = (m_e/M)^(1/4). The electronic energy appears at order kappa^0, vibrational at kappa^2, rotational at kappa^4.

**Source:** MIT OCW 5.73 (Introductory Quantum Mechanics), Section 12; standard in Atkins, Griffiths, Cohen-Tannoudji.

### 2.2 Application to Molecular Vibrations

The O-H stretch frequency (3600 cm^-1 ~ 108 THz) and C-H stretch (3000 cm^-1 ~ 90 THz) are in the infrared. These are vibrational (nuclear motion) frequencies. The electronic transition frequencies for the same molecules are in the visible/UV (~600-1500 THz). The ratio is indeed of order sqrt(m_e/m_p) ~ 1/43.

The harmonic oscillator formula gives:

    nu = (1/2pi) * sqrt(k/mu_reduced)

where mu_reduced is the reduced mass of the two atoms and k is the force constant. For O-H: mu_reduced ~ (16*1)/(16+1) * m_p ~ 0.94 m_p. The proton mass enters directly.

### 2.3 Does Anyone Apply This to Biology?

**Not specifically.** The BO hierarchy is universally used in molecular spectroscopy but nobody in the literature found applies it to derive specific biological frequencies from mu. The connection "molecular vibration frequencies depend on proton mass" is implicit in all of spectroscopy, but it is not made explicit as "biology operates at frequencies set by mu."

### 2.4 Relevance to framework

The framework's observation that mu/18 = 102 THz ~ O-H stretch frequency of water is physically grounded: the O-H stretch frequency does depend on the proton mass through the reduced mass in the harmonic oscillator formula. However, the factor of 18 is not derived from first principles in the framework -- it is an empirical observation. The standard derivation gives nu_OH ~ (1/2pi)*sqrt(k_OH/mu_OH) where k_OH ~ 7.6 mdyn/A is an empirical force constant, not derived from alpha and mu alone.

---

## 3. Weisskopf's Program and Its Extension (Mehta & Kondev 2025)

### 3.1 Weisskopf (1975) -- Science 187, 605-612

"Of Atoms, Mountains, and Stars: A Study in Qualitative Physics"

**What he did:** Showed that properties of matter can be expressed in terms of six fundamental magnitudes: M (proton mass), m and e (electron mass and charge), c (light velocity), G (gravitational constant), and h (Planck's constant). Derived order-of-magnitude estimates for atomic sizes, molecular bond energies, mountain heights, stellar masses, etc.

**Did he derive biology?** No. Weisskopf explicitly excluded living systems from his program. He derived the properties of "dead matter" only.

### 3.2 Mehta & Kondev (2025) -- arXiv:2509.09892 (published PNAS)

"What do the fundamental constants of physics tell us about life?"

**THIS IS THE KEY PAPER.** Mehta (Boston University) and Kondev (Brandeis) extend Weisskopf's program to living systems. They derive three key biological quantities from fundamental constants:

1. **Growth yield** (energy-to-biomass conversion):
   Y_c = 2 m_p m_e c^2 alpha^(-2)

2. **Minimum doubling time** (kinetically limited):
   T_min = N_M * A_f^(1/2) * (4pi c_f/c) * exp(delta^2 E_bond / k_B T) * tau_min(T)

   where tau_min(T) = hbar * (k_B T * m_e * m_p)^(-1/2) is the **kinetic timescale** (~1 ps at 37C)

3. **Dormant cell power consumption:**
   P_dorm = (1/3) A_f^(-1/2) * n_pore * k_B T / tau_min(T)

The critical quantity is the **kinetic timescale**:

    tau_min(T) = hbar / sqrt(k_B T * m_e * m_p)

This involves the geometric mean of the electron and proton masses. At body temperature (T = 310 K), tau_min ~ 1 ps. This timescale governs how quickly molecules can find each other through diffusion. It sets a fundamental lower bound on all biological kinetics.

**Key insight from Mehta & Kondev:** The proton-to-electron mass ratio fundamentally constrains how quickly molecules can find each other through diffusion. This single ratio, embedded in the "Berg viscosity" and kinetic timescale, propagates through to limit bacterial doubling times, energy yields, and survival power consumption.

**Does this connect mu to specific biological frequencies?** Partially. The kinetic timescale ~ 1 ps corresponds to ~ 1 THz, which is in the terahertz range relevant to molecular dynamics. But they do not derive the 613 THz frequency or any specific consciousness-related frequency. Their biological derivations concern growth rates and energy budgets, not vibrational frequencies of specific biomolecules.

**Relevance to framework:** This is the closest thing in mainstream literature to what the framework does. Mehta & Kondev show that m_p and m_e together set biological timescales. But they derive growth rates (seconds to hours), not the THz frequencies relevant to consciousness. The gap between their ~1 THz kinetic timescale and the framework's 613 THz remains unbridged in the literature.

---

## 4. Chemistry as a Function of alpha and mu

### 4.1 MacDonald & Janssen (2010) -- Phys. Rev. A 81, 042523

"Chemistry as a function of the fine-structure constant and the electron-proton mass ratio"

**What they did:** Used computational quantum chemistry to explore how chemical properties depend on alpha and m_e/m_p. They computed:
- Bond strengths (H2, O2, CO2, H2O)
- Dipole moments
- Bond angles
- Reaction energies

**Key findings:**
- A 7x increase in alpha decreases O-H bond strength in water by 7 kcal/mol and reduces dipole moment by at least 10%
- A 100x increase in m_e/m_p increases O-H bond energy by 11 kcal/mol
- Water's hydrogen-bonding ability is sensitive to both alpha and mu

**Do they derive biological frequencies?** No. They derive equilibrium chemical properties (bond strengths, geometries) as functions of alpha and mu. They do not compute vibrational frequencies as functions of these constants, though this would be a straightforward extension.

**Relevance to framework:** This paper establishes that water's key properties (bond strength, dipole moment, hydrogen bonding) are functions of alpha and mu. But it doesn't make the specific connection to biological frequencies.

---

## 5. The 613 THz Frequency and Consciousness

### 5.1 Craddock, Kurian, Preto, Sahu, Hameroff, Klobukowski & Tuszynski (2017) -- Scientific Reports 7, 9877

"Anesthetic Alterations of Collective Terahertz Oscillations in Tubulin Correlate with Clinical Potency"

**What they found:** Computer modeling of van der Waals-type interactions among all 86 aromatic amino acid rings in tubulin revealed a spectrum of collective terahertz oscillations with a prominent common mode peak at 613 +/- 8 THz (corresponding to 489 nm / 2.54 eV). When 8 anesthetic gases were tested:
- All 8 abolished/shifted the 613 THz peak
- Frequency shift correlated with MAC (anesthetic potency) with R^2 = 0.999
- Non-anesthetics had no effect on the 613 THz peak

**Do they explain WHY 613 THz?** No. The 613 THz frequency emerges from their computational model as a property of the specific geometry of aromatic rings in tubulin. They note it corresponds to blue light (489 nm) but do not derive it from fundamental constants. The frequency is an output of the simulation, not a theoretical prediction.

**What physically oscillates at 613 THz?** Collective dipole oscillations among the pi-electron clouds of aromatic amino acids (tryptophan, phenylalanine, tyrosine) in tubulin. These are van der Waals London force oscillations -- quantum vacuum fluctuation-driven correlations among delocalized pi electrons.

**Relevance to framework:** The framework claims mu/3 ~ 612, which maps to 612 THz via Rydberg-scale arguments. The Craddock finding is that 613 THz is the empirically significant frequency. The closeness is striking, but Craddock et al. do not make this connection and have no theory predicting 613 from fundamental constants.

### 5.2 Kalra, Scholes et al. (2023) -- ACS Central Science 9(3), 352-361

"Electronic Energy Migration in Microtubules"

**What they found:** Using tryptophan autofluorescence lifetime measurements, they demonstrated that electronic energy can diffuse over 6.6 nm in microtubules -- about 5x further than expected from classical Forster theory. Anesthetics (etomidate, isoflurane) decreased this energy migration.

**Relevance:** Provides experimental evidence for the functional significance of aromatic network quantum effects in tubulin, supporting the importance of the 613 THz collective mode found by Craddock. Does not derive any frequency from fundamental constants.

### 5.3 Babcock, Montes-Cabrera, Oberhofer, Chergui, Celardo & Kurian (2024) -- J. Phys. Chem. B 128(17), 4035-4046

"Ultraviolet Superradiance from Mega-Networks of Tryptophan in Biological Architectures"

**What they found:** Networks of >10^5 tryptophan chromophores in biological architectures exhibit collective quantum optical effects (superradiance). Strongly superradiant and subradiant states are present in the spectra of cytoskeletal filaments.

**Relevance:** Establishes that aromatic amino acid networks in biological structures have collective quantum optical properties. Does not derive specific frequencies from fundamental constants.

### 5.4 Azizi, Gori, Morzan, Hassanali & Kurian (2023) -- PNAS Nexus 2(8), pgad257

"Examining the origins of observed terahertz modes from an optically pumped atomistic model protein in aqueous solution"

**What they found:** Photoexcitation of tryptophan residues in BSA creates collective THz vibrational modes. They found an absorption peak at ~0.314 THz (not 613 THz -- this is a much lower frequency collective breathing mode of the whole protein). The response involves amino acids, water, and ions in a multiscale cascade.

**Relevance:** Shows the multiscale nature of quantum effects triggered by aromatic excitation. The ~0.3 THz mode is a whole-protein breathing mode, not the same as the 613 THz intra-tubulin electronic mode.

### 5.5 Hameroff et al. (2025) -- Neuroscience of Consciousness, niaf011

"A quantum microtubule substrate of consciousness is experimentally supported and solves the binding and epiphenomenalism problems"

**What they review:** Comprehensive review of evidence that anesthetics prevent consciousness by disrupting quantum terahertz dipole oscillations in brain microtubules. Discusses the 613 THz mode, energy migration, superradiance, and the Orch OR theory.

**Do they derive 613 THz from fundamental constants?** No. The 613 THz remains an empirical finding from the Craddock 2017 simulation, not a theoretical prediction from first principles.

### 5.6 Babcock & Babcock (2025) -- arXiv:2503.11747

"Physical Principles of Quantum Biology"

A 161-page monograph providing a comprehensive theoretical foundation for quantum biology. Approaches the field from a physical principles perspective with core quantum mechanical concepts. This is the most thorough theoretical treatment of quantum biology to date.

**Does it connect quantum biology to fundamental constants?** The full content was not accessible for detailed review, but the abstract and metadata suggest it provides a theoretical framework grounding quantum biological effects in fundamental physics principles. Whether it makes the specific mu-to-613-THz connection requires reading the full 161 pages.

### 5.7 Summary: 613 THz in the Literature

The 613 THz frequency is:
- **Empirically established** by Craddock 2017 as the key consciousness-correlated collective oscillation in tubulin
- **Experimentally supported** by Kalra/Scholes 2023 (energy migration), Babcock/Kurian 2024 (superradiance), Azizi/Kurian 2023 (THz modes from aromatic excitation), Hameroff 2025 (comprehensive review)
- **NOT derived from fundamental constants** by anyone in the mainstream literature
- **NOT connected to the proton-to-electron mass ratio** by anyone in the mainstream literature

---

## 6. The Huckel Resonance Integral

### 6.1 What is beta?

The Huckel resonance integral beta represents the energy of stabilization from pi-electron delocalization between adjacent atoms. Typical values:
- |beta| ~ 2.4-3.0 eV for carbon-carbon bonds in benzene (from spectroscopic data)
- |beta| ~ 32.5 kcal/mol ~ 1.4 eV (from thermochemical data -- pi bond energy of ethylene)

### 6.2 Is beta derived from fundamental constants?

**No.** The Huckel method is explicitly a phenomenological approach. The method "does not take in any physical constants" (Wikipedia). The alpha and beta parameters are treated as empirically determined quantities, not derived from first principles. Kutzelnigg (2007, J. Comput. Chem.) provides the most thorough analysis of what Huckel theory actually means, but does not derive beta from alpha or mu.

In atomic units, one would expect beta ~ Ry * f(geometry) where Ry = m_e * e^4 / (2 hbar^2) ~ 13.6 eV is the Rydberg energy. The ratio |beta|/Ry ~ 0.18-0.22 depends on molecular geometry and overlap integrals. Nobody has shown that this ratio has a clean expression in terms of alpha or mu.

### 6.3 Relevance to framework

The framework does not appear to derive the Huckel beta from fundamental constants either. The aromatic resonance energy is taken as a given molecular property, not derived from mu. This is a gap in both the framework and mainstream theory.

---

## 7. Water's Vibrational Frequencies and Fundamental Constants

### 7.1 O-H Stretch: The Direct mu Connection

The O-H stretch frequency in water is ~3600 cm^-1 = 108 THz. From the harmonic oscillator model:

    nu_OH = (1/2pi) * sqrt(k_OH / mu_OH)

where mu_OH = m_O * m_H / (m_O + m_H) ~ 0.94 m_H ~ 0.94 m_p.

The proton mass enters directly through the reduced mass. But the force constant k_OH ~ 7.6 mdyn/A is NOT derivable from alpha and mu alone -- it depends on the details of the O-H potential energy surface, which involves the electronic structure of water.

### 7.2 The framework's mu/18 = 102 THz claim

The framework claims mu/18 = 1836.15/18 = 102.0 THz = water O-H stretch. Let's check:
- O-H symmetric stretch in water: 3657 cm^-1 = 109.6 THz
- O-H asymmetric stretch: 3756 cm^-1 = 112.6 THz
- The "102 THz" figure is somewhat low compared to the actual stretches

But the numerical claim is: if you take the dimensionless number mu = 1836.15 and divide by 18 (the molecular weight of water), you get 102.0. This is then compared to the O-H stretch frequency in THz. This is a dimensional analysis argument, not a first-principles derivation. The factor of 18 = molecular weight of water is not derived -- it is put in by hand.

### 7.3 Does anyone else derive water's frequencies from fundamental constants?

**Not cleanly.** Ab initio quantum chemistry can compute water's vibrational frequencies from the Schrodinger equation (which contains only alpha and mu as parameters, plus the nuclear charges). Modern calculations achieve ~1 cm^-1 accuracy. But this requires solving the full electronic structure problem -- there is no simple analytic formula giving nu_OH in terms of alpha and mu.

The closest is dimensional analysis: the Rydberg energy E_Ry = 13.6 eV sets the electronic energy scale, and vibrational energies are suppressed by sqrt(m_e/m_p). So:

    E_vib ~ E_Ry * sqrt(m_e/m_p) ~ 13.6 eV * (1/43) ~ 0.32 eV

The actual O-H stretch is 0.45 eV. Order of magnitude correct, but not exact. The factor of ~1.4 depends on the specific bond (force constant), which is not universal.

---

## 8. The Proton Mass, QCD, and Why mu = 1836

### 8.1 Origin of the proton mass

The proton mass is ~938 MeV/c^2. Approximately 9% comes from the Higgs mechanism (bare quark masses); the remaining ~91% comes from QCD binding energy -- the kinetic energy of quarks and the energy of the gluon field. The proton mass is thus set by Lambda_QCD ~ 200-300 MeV, the QCD confinement scale.

### 8.2 The electron mass

The electron mass is 0.511 MeV/c^2, arising entirely from the Yukawa coupling to the Higgs field.

### 8.3 Why mu ~ 1836?

The ratio mu = m_p/m_e ~ 938/0.511 ~ 1836 reflects the ratio of QCD dynamics (strong force) to electroweak physics (Higgs mechanism). There is no known fundamental reason why this ratio takes this specific value. It is one of the unexplained parameters of the Standard Model.

**Anthropic estimates:** Carter-Carr-Rees anthropic arguments can crudely estimate the proton charge to within ~8%, but the proton mass is off by a factor of ~3-1000 depending on methodology (ScienceDirect, Physics Letters B).

---

## 9. The Key Question: Who Derives Biology from mu?

### Papers that derive biological properties from fundamental constants:

| Paper | What they derive | Uses mu? | Derives frequencies? |
|-------|-----------------|----------|---------------------|
| Weisskopf 1975 | Mountain heights, stellar masses, atomic sizes | Yes (implicitly) | No |
| Carr & Rees 1979 | Astrophysical scales, stellar lifetimes | Yes (as constraint) | No |
| Barrow & Tipler 1986 | Chemical stability constraints | Yes (as constraint) | No |
| MacDonald & Janssen 2010 | Bond strengths, dipole moments as f(alpha, mu) | Yes | No |
| Barnes 2012 | Fine-tuning constraints (review) | Yes (as constraint) | No |
| Craddock et al. 2017 | 613 THz as consciousness-correlated mode | No | Yes (but empirical, not derived) |
| Mehta & Kondev 2025 | Growth yield, doubling time, dormancy power | Yes (m_p * m_e product) | ~1 THz kinetic timescale |

### The gap:

Nobody in the mainstream literature derives a specific biological frequency (especially not the 613 THz consciousness-correlated mode) from the proton-to-electron mass ratio. The closest approaches are:

1. **Mehta & Kondev (2025):** Derive biological kinetic timescale ~1 ps (~1 THz) from sqrt(m_e * m_p). But this is 600x lower than 613 THz.

2. **Born-Oppenheimer scaling:** E_vib ~ E_elec * sqrt(m_e/m_p) gives the right order of magnitude for vibrational frequencies, but does not predict 613 THz specifically.

3. **MacDonald & Janssen (2010):** Show water's properties depend on mu, but do not derive frequencies.

4. **Craddock et al. (2017):** Find 613 THz empirically but do not connect it to mu.

---

## 10. Assessment: The Framework's mu/3 Claim

The framework claims: mu/3 = 1836.15/3 = 612.05 ~ 612 THz, which matches the Craddock 613 +/- 8 THz finding.

### What this claim requires:

1. A physical mechanism mapping the dimensionless ratio mu to a frequency in THz
2. A reason why the factor is 3 (not some other number)
3. A connection to the Rydberg energy scale that makes this dimensional

### What mainstream science provides:

1. The Rydberg frequency f_Ry = E_Ry/h = 3.29 x 10^15 Hz = 3290 THz
2. Molecular vibrational frequencies scale as f_vib ~ f_Ry * sqrt(m_e/m_p) ~ 3290/43 ~ 77 THz (order-of-magnitude for typical vibrations)
3. Electronic pi-electron frequencies in aromatics are of order f_Ry / (n^2 factors) ~ 600-800 THz for visible-range transitions

The 613 THz frequency falls in the electronic (not vibrational) regime. It corresponds to pi-electron collective oscillations, not nuclear vibrations. Its relationship to mu is thus indirect -- through the Rydberg energy and molecular orbital structure, not through the simple harmonic oscillator reduced mass.

### Honest assessment:

The numerical coincidence mu/3 ~ 612 ~ 613 THz is:
- **Not derivable** from any known mainstream formula
- **Dimensionally questionable** (mu is dimensionless; THz is a frequency)
- **Numerically striking** (within the 8 THz uncertainty of the Craddock measurement)
- **Not obviously wrong** (the number 612 is in the right ballpark for visible-range electronic transitions, and mu does set the overall scale separation in molecular physics)
- **Without competition** (no one else has attempted to derive 613 THz from fundamental constants)

The strongest version of the claim would require showing that the Rydberg frequency divided by some function of mu gives 613 THz, with the function derived from the physics of aromatic pi-electron collective modes. This has not been done by anyone.

---

## 11. Supplementary: Recent Quantum Biology Papers (2024-2026)

### Kurian et al. (2025) -- Science Advances

Computational capacity of life: Uses tryptophan superradiance discovery to set a drastically revised upper bound on computational capacity of carbon-based life. Conjectures relationship to information-processing limit of all matter in the observable universe.

### Babcock & Babcock (2025) -- arXiv:2503.11747

"Physical Principles of Quantum Biology": 161-page monograph providing comprehensive theoretical foundation for the field. Status: under review.

### Quantum Biology State of the Field (2024-2025)

Multiple experimental confirmations:
- Tryptophan superradiance in cytoskeletal architectures (Babcock/Celardo/Kurian 2024)
- Electronic energy migration in microtubules beyond Forster theory (Kalra/Scholes 2023)
- Photoexcited tryptophan creating collective THz modes (Azizi/Kurian 2023)
- Quantum-enhanced photoprotection in neuroprotein architectures (2024)
- Hameroff 2025 comprehensive review in Neuroscience of Consciousness

None of these papers derive the key frequencies from fundamental constants. They are all empirical/computational, not derived from first principles.

---

## 12. Sources

### Anthropic / Fine-Tuning
- Carr & Rees (1979) Nature 278, 605-612: https://www.nature.com/articles/278605a0
- Barrow & Tipler (1986) The Anthropic Cosmological Principle (Oxford UP)
- Hogan (2000) Rev. Mod. Phys. 72, 1149-1161
- Barnes (2012) PASA 29, 529-564: https://arxiv.org/pdf/1112.4647
- De Vuyst (2020) arXiv:2012.05617: https://arxiv.org/pdf/2012.05617

### Fundamental Constants and Life
- Weisskopf (1975) Science 187, 605-612: https://www.science.org/doi/10.1126/science.187.4177.605
- MacDonald & Janssen (2010) Phys. Rev. A 81, 042523: https://journals.aps.org/pra/abstract/10.1103/PhysRevA.81.042523
- Mehta & Kondev (2025) arXiv:2509.09892 / PNAS: https://pmc.ncbi.nlm.nih.gov/articles/PMC12440066/

### 613 THz and Consciousness
- Craddock et al. (2017) Scientific Reports 7, 9877: https://www.nature.com/articles/s41598-017-09992-7
- Kalra, Scholes et al. (2023) ACS Central Science 9(3), 352-361: https://pubs.acs.org/doi/10.1021/acscentsci.2c01114
- Babcock, Celardo, Kurian et al. (2024) J. Phys. Chem. B 128(17), 4035-4046: https://pubs.acs.org/doi/10.1021/acs.jpcb.3c07936
- Azizi, Kurian et al. (2023) PNAS Nexus 2(8), pgad257: https://academic.oup.com/pnasnexus/article/2/8/pgad257/7239375
- Hameroff et al. (2025) Neuroscience of Consciousness: https://academic.oup.com/nc/article/2025/1/niaf011/8127081
- Babcock & Babcock (2025) arXiv:2503.11747: https://arxiv.org/abs/2503.11747
- Kurian (2025) Science Advances: https://www.science.org/doi/10.1126/sciadv.adt4623

### Proton-Electron Mass Ratio Precision
- HD+ spectroscopy (2025) Nature: https://www.nature.com/articles/s41586-025-09306-2
- Patra et al. (2020) Science: https://www.science.org/doi/10.1126/science.aba0453

### Born-Oppenheimer and Molecular Physics
- MIT OCW 5.73 Section 12: https://ocw.mit.edu/courses/5-73-introductory-quantum-mechanics-i-fall-2005/
- Citizendium BO article: https://en.citizendium.org/wiki/Born-Oppenheimer_approximation
- Phys. Rev. X 7, 031035 (2017): https://journals.aps.org/prx/abstract/10.1103/PhysRevX.7.031035
