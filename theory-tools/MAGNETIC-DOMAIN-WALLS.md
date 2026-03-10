# Magnetic Domain Walls — The Sleeping Kinks in Your Fridge Magnets

*Feb 27 2026. Pure magnetism, no plasma needed. What the framework says and what experiments confirm.*

---

## The Punchline

Every permanent magnet, every compass needle, every hard drive platter contains **domain walls that are mathematically identical to the framework's kink solution**. The Bloch wall magnetization profile is:

```
M(x) = M_s · tanh(x/Δ)
```

where Δ = √(A/K), A = exchange stiffness, K = anisotropy constant. **This IS the kink.** Same equation, same topology, same reflectionlessness.

But there's a catch: **ferromagnetic domain walls are PT n=1. They're sleeping.**

The effective potential for spin waves (magnons) scattering off a Bloch wall is:

```
V(x) = -2K · sech²(x/Δ)
```

That coefficient "2" means n(n+1) = 2, so **n = 1**. One bound state (the translational zero mode, Winter 1961). No shape/breathing mode. Sleeping.

The framework's quartic kink V(Φ) = (Φ²−Φ−1)² gives:

```
V_eff(x) = -6 · sech²(x/w)
```

That "6" means n(n+1) = 6, so **n = 2**. Two bound states. Awake.

**The difference between sleeping and awake is the difference between 2 and 6 in front of sech².**

---

## Part 1: What Ferromagnetic Domain Walls Already Have

### Confirmed Properties (experiment + theory)

| Property | Status | Reference |
|----------|--------|-----------|
| tanh profile | Exact | Landau-Lifshitz, 1935 |
| PT n=1 potential | Exact | Winter 1961 |
| Reflectionless for magnons | Confirmed | Kim et al., Nature Comms 2017; Lan et al. 2017 |
| One bound state (zero mode) | Confirmed | Winter 1961, measured via NMR |
| Two degenerate vacua (↑ and ↓) | Exact | Basic ferromagnetism |
| Topological protection | Exact | Winding number ±1, cannot unwind |
| Wall width Δ ~ 10-500 nm | Measured | Material-dependent |
| Wall energy σ = 4√(AK) | Measured | ~1-10 mJ/m² for common ferromagnets |

### What's Missing for n=2

| Property | Status | What's Needed |
|----------|--------|---------------|
| PT n=2 (breathing mode) | **Missing** | Need -6 sech² instead of -2 sech² |
| Shape mode ψ₁ | **Missing** | Would appear at ω₁ = √3 · κ if n=2 existed |
| Golden vacua (φ, -1/φ) | **Wrong** | Vacua are +M_s and -M_s (symmetric) |
| Nome q=1/φ | **Unknown** | Would need specific periodicity in wall lattice |
| Creation identity | **Untested** | Would need η·θ₄ structure in magnon spectrum |

The honest summary: **ferromagnetic domain walls are 50% of the framework's structure** — same topology, same reflectionlessness, same kink — but at the wrong depth. They're like an instrument that's perfectly built but tuned one octave too low.

---

## Part 2: How to Wake Them Up — Routes to n=2

### Route 1: Skyrmion-Textured Domain Walls

**The most promising route.** When a magnetic skyrmion sits inside a domain wall, the topological charge Q modifies the effective PT depth. The number of bound magnon states = floor(|Q|).

- A single skyrmion (Q=1) gives 1 bound state → n=1
- A **skyrmion with Q=2** (or two overlapping skyrmions) would give 2 bound states → **n=2**

This was shown theoretically in Frontiers in Physics 2022 using SUSY QM — the same supersymmetric quantum mechanics that governs the framework's PT spectrum.

**Domain Wall Skyrmions (DWSKs)** were experimentally realized in 2025 (Phys. Rev. X 15, 021041). These are skyrmions TRAPPED INSIDE domain walls — bound states on bound states. The homotopy group is Z × Z, meaning two independent topological charges. By tuning both charges, n=2 should be achievable.

**Materials**: Ir/Fe/Co/Pt multilayers, Co/Pd multilayers with engineered DMI.

**Detection**: Brillouin Light Scattering (BLS) microscopy — shine a laser at the wall, measure the inelastically scattered photons. Each magnon bound state shows up as a spectral peak.

### Route 2: Higher Anisotropy Order

The reason standard Bloch walls give n=1 is that the anisotropy energy is **quadratic** in the magnetization deviation:

```
E_anis = K · sin²(θ) ≈ K · (1 - m_z²)
```

This gives a potential with 2 sech² → n=1. But if the material has **quartic anisotropy** (fourth-order term):

```
E_anis = K₁ · sin²(θ) + K₂ · sin⁴(θ)
```

The domain wall profile deviates from pure tanh, and the effective PT depth changes. For certain K₂/K₁ ratios, the effective potential deepens to n=2.

**Materials with significant K₂**:
- **Cobalt** (hexagonal): K₂/K₁ ≈ 0.27
- **BaFe₁₂O₁₉** (barium ferrite): large higher-order terms
- **Nd₂Fe₁₄B** (neodymium magnet): complex anisotropy landscape
- **SmCo₅** (samarium cobalt): extremely high K₁ and non-negligible K₂

**The question nobody has asked**: For what K₂/K₁ ratio does the effective PT depth cross n=2? This is a straightforward calculation — the eigenvalue problem for the modified wall profile.

### Route 3: Dzyaloshinskii-Moriya Interaction (DMI)

DMI adds an antisymmetric exchange that tilts the wall from Bloch to Néel type. The magnon potential becomes:

```
V(x) = -2K sech²(x/Δ) + 2D·k_y·tanh(x/Δ)
```

This is a **Rosen-Morse potential** (sech² + tanh). It has:
- Modified bound state spectrum
- **Broken reflectionlessness** (the tanh term scatters)
- Potentially deeper effective well

**Problem**: DMI breaks reflectionlessness. The framework requires reflectionlessness for consciousness. So DMI alone doesn't work — you'd need a system where DMI deepens the well to n=2 while some other symmetry restores reflectionlessness.

**Materials**: Fe/Pt bilayers, Co/Pt multilayers, Mn/W interfaces — strong interfacial DMI.

### Route 4: Antiferromagnetic Domain Walls

Antiferromagnets have TWO sublattices (↑ and ↓ alternating). Their domain walls carry a richer internal structure:

- **Two magnon branches** (acoustic + optical) instead of one
- The acoustic branch sees the usual n=1 PT potential
- The optical branch sees a MODIFIED potential (sublattice exchange adds terms)
- In certain antiferromagnets (MnBi₂Te₄), the combination gives an **axion quasiparticle** — a mode that oscillates between the two sublattice orderings at ~44 GHz

**The axion quasiparticle IS the breathing mode** in framework language — it has amplitude on BOTH sides (both sublattices) with opposite phase. This is exactly ψ₁.

**Key material**: MnBi₂Te₄ (magnetic topological insulator). April 2025: dynamical axion quasiparticle confirmed at ~44 GHz. This may already BE the n=2 breathing mode in a magnetic system.

### Route 5: Composite / Stacked Walls

Two parallel domain walls in close proximity create a **double-well** potential for magnons. The SUSY QM bound state counting gives:

- Single wall (n=1): 1 bound state
- Double wall (kink-antikink): 1 + 1 - overlap = 2 bound states if spacing is right

This is the magnetic equivalent of the framework's kink-antikink oscillons (= biological life). The two walls create a region between them where magnons are trapped with two discrete modes.

**How to create**: Antiparallel domains in a thin wire — natural domain patterns in magnetic nanowires have alternating walls. Or: use patterned magnetic thin films to force specific wall configurations.

---

## Part 3: What You Can Do at Home

### Experiment 1: SEE the Domain Walls — Bitter Technique (~$20-40)

**This is the first thing to do.** Seeing magnetic domain walls with your own eyes.

#### Equipment

| Item | Cost |
|------|------|
| Grain-oriented silicon steel (transformer lamination) | $0-5 (old transformer) |
| Ferrofluid (15mL) | $10-15 (Amazon) |
| Magnifying glass or USB microscope (50-200×) | $10-20 |
| Small N52 magnet | $3-5 |
| Acetone or isopropyl alcohol | $3 |
| Fine sandpaper (600-1200 grit) | $2 |

#### Procedure

1. **Polish the steel surface**: Sand with 600, then 1200 grit. Clean with alcohol. The smoother, the better the patterns.

2. **Apply ferrofluid**: Dilute ferrofluid 1:3 with isopropyl alcohol. Apply a thin layer to the polished surface with a dropper. Wait 3-5 minutes.

3. **Observe**: The magnetic nanoparticles collect at domain walls where the stray field is strongest. Under magnification, **dark lines** appear — these are the walls. The lighter regions between them are domains (all spins aligned one way).

4. **Interact**: Bring the N52 magnet slowly closer. Watch the domain walls **move** — domains aligned with the external field GROW, eating their neighbors. The walls sweep across the surface. Remove the magnet — walls snap back (partially; hysteresis).

5. **What you're seeing**: Each dark line is a tanh(x/Δ) kink. A PT n=1 potential. A sleeping domain wall. The same mathematical object the framework identifies as the unit of consciousness — but at the wrong depth.

### Experiment 2: HEAR the Domain Walls — Barkhausen Noise (~$5-15)

When domain walls move, they make noise. Literally.

#### Equipment

| Item | Cost |
|------|------|
| Iron nail or silicon steel strip | $0-2 |
| Pickup coil (500-1000 turns on iron core, or just wrap wire around the nail) | $3-5 |
| Audio amplifier + speaker (or plug into computer mic input) | $0-10 |
| Small N52 magnet | $3-5 |

#### Procedure

1. Wind ~500 turns of thin wire around the iron nail/steel strip
2. Connect to amplifier input (or computer sound card mic-in)
3. Slowly bring the N52 magnet toward the nail
4. **Listen**: You hear CRACKLING — discrete pops and clicks

**What you're hearing**: Each click is a domain wall JUMPING from one pinning site to another. The wall doesn't move smoothly — it's pinned by crystal defects, then suddenly snaps to a new position. Each snap is a domain wall event.

**Framework connection**: These are the sleeping walls rearranging. The crackling follows a power law (Barkhausen avalanches) — same statistics as neural avalanches in the brain (Beggs & Plenz 2003). The magnetic system is at criticality, just like the brain. But n=1, so no breathing mode, no internal dynamics beyond translation.

**With FFT analysis** (record to Audacity, plot spectrum): The Barkhausen noise has a characteristic power-law spectrum P(f) ~ f^(-α) with α ≈ 1.5-2.0. The specific exponent depends on the material's universality class. This is measurable from your desk.

### Experiment 3: MANIPULATE the Domain Walls — Stripe Patterns (~$30-60)

Thin magnetic films show stripe domain patterns. You can create these:

#### Equipment

| Item | Cost |
|------|------|
| Magnetic viewing film (green type) | $10-15 (Amazon) |
| Various permanent magnets | $5-15 |
| Speaker or vibration motor | $5-10 |
| USB microscope | $10-20 |

#### Procedure

1. **Place viewing film on a flat surface** — it shows magnetic fields as dark/light patterns
2. **Place magnets below**: Different configurations create different domain patterns
   - Single magnet: radial domains
   - Two same-pole: domain wall between them (your magnetic well!)
   - Array of magnets: complex domain lattice
3. **Apply vibration** (speaker, motor): Domain walls oscillate. The vibration frequency that produces the strongest wall motion = the wall's resonant frequency
4. **Observe under microscope**: Domain walls have visible internal structure (zigzags, bubbles, stripes)

**Framework test**: If you can find a frequency where the domain walls oscillate with TWO visible modes (translational + breathing), you've found n=2 magnetically. The breathing mode would show as the wall THICKENING and THINNING periodically, while also moving back and forth.

---

## Part 4: The Deep Connection — Why Magnetic Domain Walls Matter

### Every Fridge Magnet Contains the Framework

This is not metaphor. The mathematics is identical:

| Framework | Ferromagnet |
|-----------|-------------|
| V(Φ) = λ(Φ²−Φ−1)² | E(θ) = K sin²θ + ... |
| Kink: Φ = tanh(x/w) | Bloch wall: M = M_s tanh(x/Δ) |
| Two vacua: φ, -1/φ | Two domains: +M_s, -M_s |
| PT potential: -n(n+1) sech² | Magnon potential: -2 sech² |
| Reflectionless | Reflectionless (confirmed 2017) |
| Topological charge | Winding number ±1 |

The ONLY difference is the depth parameter:
- **Ferromagnet**: n=1 (from quadratic anisotropy → degree-2 → n=1)
- **Framework**: n=2 (from quartic golden potential → degree-4 → n=2)

### The Iron Paradox

Iron sits at the center of THREE framework structures:
1. **Ferromagnetic domain walls** (Bloch walls, PT n=1, sleeping)
2. **Biological aromatic interfaces** (hemoglobin: iron at center of porphyrin ring, 18 π-electrons)
3. **Nuclear stability peak** (Fe-56 = fundamental rep of E₇ ⊂ E₈)

Iron is ferromagnetic. Copper is not. Gold is not. Every culture on Earth independently discovered that iron "repels" invisible beings (jinn, faeries, spirits). The framework explains why: iron's permeability μ_r ~ 200,000 distorts any nearby magnetic domain wall profile, destroying the sech² shape and collapsing PT depth.

**Iron is simultaneously**: the material whose domain walls are closest to the framework's structure AND the material that disrupts other domain wall systems. It's the bridge between sleeping and awake — a domain wall material that can't itself wake up, but forces everything around it to notice.

### The 2025 Revolution in Magnetic Domain Walls

Three papers from 2025 change the picture:

1. **Domain Wall Skyrmions** (Phys. Rev. X 15, 021041, 2025): Skyrmions trapped INSIDE domain walls. Homotopy Z × Z. Bound states on bound states. The nesting the framework predicts.

2. **Altermagnetic domain walls** (Phys. Rev. B 2025): Chiral split magnons — richer internal structure than Bloch walls. Electrically controllable. New degree of freedom.

3. **Axion quasiparticle in MnBi₂Te₄** (Nature Phys 2025): A mode that oscillates between two sublattice orderings at 44 GHz. This IS a breathing mode — amplitude on both sides with opposite phase. In a magnetic system. No plasma.

**MnBi₂Te₄ may already have n=2 magnetic domain walls.** Nobody has checked the PT depth of its antiferromagnetic domain wall spectrum. If the axion quasiparticle IS the ψ₁ breathing mode, then:
- Its frequency should relate to the zero-mode frequency by the PT n=2 ratio: ω₁/κ = √3
- Its spatial profile should be sinh/cosh² (odd, antisymmetric)
- It should be detectable from both sides of the wall with π phase shift

**This is testable NOW with existing samples and equipment.**

---

## Part 5: The Experiment That Would Change Everything

### Measure the PT Depth of MnBi₂Te₄ Domain Walls

**What**: Use spin-polarized inelastic neutron scattering or spin-polarized EELS to map the magnon spectrum at an antiferromagnetic domain wall in MnBi₂Te₄.

**What to look for**:
1. Count the number of discrete magnon modes localized at the wall
2. If 1 mode → n=1 (sleeping, like standard ferromagnets)
3. If **2 modes** → n=2 (awake). Check:
   - Energy ratio of the two modes: PT n=2 predicts E₀:E₁ = 4:1
   - Spatial symmetry: mode 0 should be even (sech²), mode 1 should be odd (sinh/cosh²)
   - The 44 GHz axion quasiparticle should be one of these modes

**Why it matters**: If a MAGNETIC material (no plasma, no water, no aromatics) shows PT n=2 domain walls, it proves:
- The framework's consciousness criterion is purely mathematical (not material-specific)
- Domain wall depth is controlled by topology, not chemistry
- n=2 can arise from antiferromagnetic + topological insulator structure
- A new kind of "being" — magnetic consciousness — is at least mathematically permitted

### What You Can Do At Home Toward This

You can't do spin-polarized EELS at home. But you CAN:

1. **Build the Bitter technique setup** ($20-40) — see actual domain walls
2. **Record Barkhausen noise** ($5-15) — hear domain wall dynamics, measure the avalanche spectrum
3. **Use magnetic viewing film + magnets** ($20-40) — watch domain patterns reorganize
4. **Apply the two-N52-magnet magnetic well** to a ferromagnetic strip — see if the well geometry changes the domain wall structure visible in ferrofluid
5. **Drive domain walls with a speaker coil** and look for resonances — the translational mode should show up as a peak in the response. Any SECOND peak would be extraordinary.

The honest truth: reaching n=2 in a pure magnetic system at home is unlikely with current materials. But SEEING and HEARING n=1 domain walls — the sleeping version of the framework's structure — is achievable this afternoon for $20.

---

## Part 6: Summary Table — Magnetic Paths to n=2

| Route | n achievable? | Reflectionless? | Home-buildable? | Key material |
|-------|---------------|-----------------|-----------------|-------------|
| Standard Bloch wall | n=1 (proven) | Yes (proven) | Yes (any magnet) | Fe, Co, Ni |
| Quartic anisotropy | n=2 (predicted) | Yes (if clean) | No (need single crystals) | Co, BaFe₁₂O₁₉ |
| Skyrmion-textured wall | n=2 (predicted) | Unclear | No (nanofab) | Ir/Fe/Co/Pt |
| Domain wall skyrmion | n=2+ (predicted) | Unknown | No (nanofab) | Co/Pd multilayers |
| Antiferro + topology | n=2 (candidate) | Unknown | No (crystals + cryo) | **MnBi₂Te₄** |
| DMI-modified wall | n>1 possible | **No** (breaks it) | No | Fe/Pt bilayers |
| Composite double wall | n=2 (counting) | Maybe | Possible (nanowires) | Fe nanowires |
| Stacked thin films | Tunable | Unknown | No (sputtering) | Co/Cu/Co |

**Best bet for pure magnetic n=2**: MnBi₂Te₄ (antiferromagnetic topological insulator, axion quasiparticle already found, may already BE the breathing mode).

**Best home experiment**: Bitter technique + Barkhausen noise on iron/steel. You see and hear the sleeping framework.

---

## Appendix: The Magnon-Kink Dictionary

| Framework term | Magnon physics term |
|---------------|-------------------|
| Kink | Bloch domain wall |
| Anti-kink | Wall with opposite chirality |
| Vacuum | Magnetic domain (uniform magnetization) |
| PT potential | Magnon scattering potential |
| Zero mode ψ₀ | Winter translational mode (1961) |
| Breathing mode ψ₁ | Would be shape oscillation (not yet found in pure magnets) |
| Reflectionlessness | Magnon transmission T=1 through wall (confirmed 2017) |
| Bound state | Localized magnon at wall |
| Continuum | Propagating spin waves (bulk magnons) |
| PT depth n | Effective anisotropy order (1 for quadratic, 2 for quartic) |
| φ (golden ratio) | Not yet identified in magnetic systems |
| Creation identity | Would connect magnon spectrum to wall lattice periodicity |
| Fibonacci collapse | Would require q=1/φ in magnonic crystal dispersion |
| Autopoiesis | Self-maintaining domain configuration under perturbation |
