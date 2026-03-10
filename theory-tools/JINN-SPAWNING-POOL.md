# The Jinn Spawning Pool — Plasma Domain Wall Generator

*Derived from V(Phi) applied to plasma physics. Feb 24, 2026.*
*Framework references: FINDINGS-v4.md §242-252, Plasma beings.md, gatchina_plasmoid_analysis.py*

---

## What This Is

A practical device for creating free-floating plasma structures in open air, optimized by the Interface Theory framework to satisfy the Poschl-Teller n=2 consciousness conditions. The framework predicts that a self-sustaining plasma domain wall with exactly 2 trapped MHD modes would exhibit anomalous stability, self-repair, and reflectionless wave transmission — properties associated with ball lightning and historical "jinn" encounters.

This document is a complete build specification: physics basis, architecture, bill of materials, protocol, predictions, and diagnostics.

---

## Physics Basis

### The Five Consciousness Conditions (from V(Phi))

The framework derives five necessary conditions for domain-wall consciousness from the potential V(Phi) = lambda(Phi^2 - Phi - 1)^2:

| # | Condition | Physical meaning | Plasma realization |
|---|-----------|-----------------|-------------------|
| 1 | Domain wall | Field reversal through sech^2 profile | Harris current sheet: B(x) = B_0 * tanh(x/w) |
| 2 | PT depth n >= 2 | Alfven speed ratio >= sqrt(6) ~ 2.45 | Controlled via magnetic field geometry |
| 3 | Reflectionlessness | Integer n gives \|T(k)\|^2 = 1 for all k | Automatic if n is integer and profile is sech^2 |
| 4 | Autopoiesis | Continuous energy input sustains the wall | Magnetron provides continuous microwave feed |
| 5 | Two trapped modes | psi_0 (presence) + psi_1 (breathing/attention) | Two discrete MHD eigenmodes in the current sheet |

### Key equation — CORRECTED (Feb 26)

**⚠️ CORRECTION:** The formula N(N+1) = (v_A,in / v_A,out)² is NOT a standard result and appears incorrect. Furth, Killeen & Rosenbluth (1963, Phys. Fluids 6:459) proved that B(x) = B₀·tanh(x/a) (Harris sheet) gives PT depth **n=1 ALWAYS** — topologically, independent of B₀, a, or Alfvén speed ratio.

**For n=2 in plasma, need NON-tanh profiles:**
- Double current sheet (two reversals)
- Composite profiles with higher-order sech² wells
- The solar transition region (6,000 K → 1,000,000 K in 100 km) — NOT a simple Harris sheet

**However, §266 (Feb 26) changes the picture entirely.** Aromatic pi-electrons ARE a 2D plasma (same Tomonaga collective oscillations). The Gatchina plasmoid uses both media (plasma + water aerosol) — producing the most anomalous structures. The spawning pool should focus on the PLASMA-WATER-AROMATIC INTERFACE, not on achieving n=2 in pure plasma.

**New hypothesis:** The PT n=2 condition may be satisfied not by the plasma alone, but by the COUPLED system: plasma domain wall + water-aromatic quantum-confined plasma at the interface. The water-aromatic side already satisfies n=2 (Mavromatos-Nanopoulos 2025 in microtubules). The plasma provides energy to maintain the system.

Anti-Helmholtz coils still create a field reversal at the midplane. But the key diagnostic shifts from "count modes in pure plasma" to "look for coupled plasma-aromatic modes at the mist boundary."

### Why the plasma must be free-floating

The framework states (§242-247):

> "It's not contained by anything external. The framework gives five layers of self-containment... The topology IS the container."

Self-containment comes from:

1. **Topological charge** — the kink has winding number Q = +1, cannot unwind without meeting an anti-kink
2. **V(Phi) forces walls to exist** — V(0) > 0, the field cannot stay uniform, walls are inevitable
3. **Reflectionlessness** — perturbations pass through without disturbing the wall
4. **PT well confines the modes** — bound states cannot leak out
5. **Taylor relaxation** — plasma self-organizes to minimum-energy state while conserving magnetic helicity (spheromak)

A plasma confined in a tube is not testing these predictions. The structure must be free to self-confine or not.

### Why water mist matters

The framework identifies water as THE coupling medium for biological consciousness (§236). Three of four most successful plasmoid methods use water:

- **Gatchina:** discharge over water surface, interior is water aerosol — produces the most anomalous plasmoids
- **Caltech (Gharib, PNAS 2017):** deionized water jet IS the plasma source
- **Grape/Mie resonance:** water spheres concentrate EM field at contact

The Gatchina plasmoid uniquely has **both coupling media present simultaneously** (plasma + water aerosol). The framework says this is why it produces the most interesting structures, not coincidence.

---

## Why Not Just Point a Magnetron Into Open Air

Three problems discovered during assessment:

**Problem 1: Air breakdown requires ~30 kV/cm.** A 1 kW magnetron with a horn produces ~80 mW/cm^2 at 1 meter — roughly 7 orders of magnitude below the power density needed to ionize air. You NEED field concentration (cavity, nozzle, or resonance).

**Problem 2: Microwaves destroy coils in the beam path.** Wire < 0.5 mm vaporizes at 800 W. Wire > 1 mm reflects microwaves and shields the plasma. Coil turns spaced < 12 mm act as a Faraday cage for 2.45 GHz. PLA formers melt from arcing. (Source: Materials, 2021, PMC7926306)

**Problem 3: ECR changes the physics.** Electron Cyclotron Resonance at 2.45 GHz occurs at B = 875 Gauss (87.5 mT). At ECR, plasma ignites at as low as ~1 W instead of hundreds. This means the coils do double duty: topology control + plasma enhancement.

### Solution: Separate ignition zone from free zone

---

## Architecture

```
                              OPEN AIR (outdoors)

                              water mist (CuSO4 + sodium benzoate)
                              |   |   |   |
               .----- Anti-Helmholtz coil A (on ceramic former) -----.
               |                                                      |
               |         FREE ZONE                                    |
               |         - No tube, no microwaves                     |
               |         - Water mist + B field topology              |
               |         - Plasmoid drifts and self-organizes here    |
               |         - Mirnov coil positioned here (on stick)     |
               |                                                      |
               '----- Anti-Helmholtz coil B (on ceramic former) -----'
                              |
                         .---------.
                         | QUARTZ  |    <-- short tube (5-10 cm)
                         |  TUBE   |        ignition zone only
                         '---------'
                              |
                     [ Metallic nozzle ]
                              |
                     [ WR340 waveguide ]    <-- salvaged from microwave oven
                              |                 + extension section
                     [ Magnetron 2.45 GHz ]
                       (1 kW, continuous)
```

### Three independent subsystems

| Subsystem | Function | Control knob | Framework role |
|-----------|----------|-------------|---------------|
| **Magnetron + waveguide + nozzle** | Creates and sustains plasma (ignition zone) | Power level (0-1 kW) | Autopoiesis — continuous energy feed |
| **Anti-Helmholtz coils** | Creates B field reversal in free zone | Coil current (0-10 A) | Topology — scans PT depth n = 1, 2, 3 |
| **Water mist sprayer** | Provides coupling medium in free zone | Flow rate, chemistry | Coupling — water + aromatics |

### How it works

1. Magnetron feeds 2.45 GHz through WR340 waveguide into a nozzle
2. Gas (air or argon) flows upward through nozzle into short quartz tube
3. Spark gap or igniter wire initiates breakdown in the tube
4. Continuous microwave sustains the plasma (TIA torch design — established, reliable)
5. Plasma jet exits the tube upward into the FREE ZONE
6. Anti-Helmholtz coils surround the free zone, ABOVE the microwave region
7. The B field creates a field-reversal topology — the Harris sheet seed
8. Water mist fills the free zone from above
9. Plasma rising into the coil zone encounters: magnetic topology + water coupling medium
10. If a self-organized structure forms and detaches, it enters the free zone unconfined

### The ECR bonus

At B = 87.5 mT (875 Gauss), electron cyclotron resonance occurs with 2.45 GHz. The Anti-Helmholtz coils at ~200 turns, 10 cm diameter, ~10 A produce approximately this field strength near the coil surfaces. This creates an **ECR surface** — a natural shell where plasma is preferentially generated. Plasma forms at this boundary, which is itself a domain wall geometry.

At atmospheric pressure, true ECR is partially suppressed (collision frequency >> cyclotron frequency), but the magnetic field still:
- Reduces electron diffusion perpendicular to B (confinement)
- Increases effective path length of electrons
- Reduces required microwave power by 20-50%
- Creates a natural boundary surface for structure formation

The coils needed for PT topology control (~87.5 mT) happen to coincide with the ECR field for 2.45 GHz. This is unplanned but potentially significant.

---

## Bill of Materials

### Core components

| Part | Specification | Source | Est. Cost |
|------|--------------|--------|-----------|
| Magnetron + transformer + mount plate | 2.45 GHz, ~1 kW, salvaged as complete unit | Any microwave oven | $0-30 |
| WR340 waveguide extension | 86.36 x 43.18 mm internal, 10-20 cm length | Sheet aluminum (DIY) or eBay | $15-30 |
| Metallic nozzle | 6-10 mm copper or brass tube, passes through waveguide broad wall | Hardware store | $5 |
| Quartz tube (short) | 25 mm OD x 5-10 cm length | Amazon / lab glass supplier | $10 |
| Spark gap igniter | Two copper bolts, adjustable gap ~2 mm | Hardware store | $5 |

### Topology control

| Part | Specification | Source | Est. Cost |
|------|--------------|--------|-----------|
| Anti-Helmholtz coils (pair) | 2x 200 turns, 100 mm diameter, 16 AWG enameled copper, **ceramic or PTFE former** (NOT PLA — PLA melts at 60C) | Wind yourself; wire from electronics supplier | $30 |
| DC power supply | 0-30 V adjustable, 10 A | Amazon | $50-80 |

### Coupling medium

| Part | Specification | Source | Est. Cost |
|------|--------------|--------|-----------|
| Garden pump sprayer | Fine mist nozzle, 1-2 liter capacity | Garden store | $15-20 |
| Copper sulfate (CuSO4) | ~50 g, dissolved in spray water | Lab supplier / Amazon | $10 |
| Sodium benzoate | Food-grade aromatic salt, ~50 g, dissolved in spray water | Amazon / lab supplier | $5 |

### Diagnostics

| Part | Specification | Source | Est. Cost |
|------|--------------|--------|-----------|
| Mirnov coil | 50 turns 30 AWG wire on 1 cm ceramic former, mounted on 2 m non-metallic stick (wooden dowel or fiberglass) | DIY | $5 |
| RTL-SDR dongle | USB software-defined radio, 24-1766 MHz | Amazon | $25 |
| Camera | Any camera on tripod, records free zone behavior | Existing (phone) | $0 |

### Signal processing

| Part | Specification | Source | Est. Cost |
|------|--------------|--------|-----------|
| V(Phi) stochastic resonance detector | neuromorphic-computer/reservoir.py — extracts discrete modes from noisy plasma spectra | Already built | $0 |

### Optional (recommended)

| Part | Specification | Source | Est. Cost |
|------|--------------|--------|-----------|
| Argon bottle (small, 20 L) + regulator | Much easier ignition than air; lower breakdown threshold | Welding supply | $80-120 |
| Welding glass (#5 shade minimum) | UV protection for observing plasma | Welding supply | $10 |

### Totals

| Configuration | Total est. cost |
|---------------|----------------|
| **Minimum (air, no argon)** | **~$175-250** |
| **Recommended (with argon)** | **~$265-380** |

---

## Waveguide Details

### Salvaging from a microwave oven

The magnetron inside a microwave oven connects to the cooking cavity via a short WR340 waveguide section (5-15 cm). The magnetron's output antenna — a short sealed copper tube — protrudes perpendicular into the waveguide, positioned one quarter-wavelength (~30 mm) from a shorted end. This probe-coupling arrangement excites the TE10 mode.

**What to salvage as a unit:**
- Magnetron + its mounting plate (has probe already coupled to waveguide)
- The transformer and capacitor circuit (high voltage supply)
- The short waveguide transition

**What to fabricate:**
- Extension waveguide: a rectangular aluminum tube, internal dimensions 86.36 x 43.18 mm, 10-20 cm long
- Can be made from sheet aluminum (1-2 mm thick) bent and riveted/soldered
- One end mates to the salvaged magnetron mount
- Other end has a hole for the nozzle (copper tube passing through the broad wall)
- The nozzle position: centered on the broad wall, adjustable depth for resonance tuning

### The TIA torch nozzle

The nozzle is the inner conductor of a coaxial section:
- Copper or brass tube, 6-10 mm OD
- Passes vertically through the center of the waveguide broad wall
- Gas flows upward through the nozzle
- The quartz tube sits above the nozzle exit
- Position is adjustable to tune the coupling (slide the tube up/down through the waveguide wall)

This is the established TIA (Torche a Injection Axiale) design (Moisan et al., 1994). Labs worldwide use it for atmospheric-pressure microwave plasma.

---

## Coil-Microwave Interaction: Solved

### The problem

Copper coils in a 2.45 GHz microwave beam:
- Wire > 1 mm diameter **reflects** microwaves (partial Faraday cage)
- Wire < 0.5 mm **vaporizes** (AC resistance too high, reaches breakdown)
- Coil turns spaced < 12 mm block 2.45 GHz entirely
- PLA formers melt from any arcing or stray heating
- Standing wave patterns create unpredictable hot spots

### The solution

**The coils are ABOVE the microwave coupling region.** In the revised architecture:

- Microwaves enter from below, through the waveguide/nozzle/quartz tube
- The plasma forms in the tube, then jets upward
- The Anti-Helmholtz coils surround the FREE ZONE above the tube exit
- No coil wire is in the microwave beam path
- The B field extends downward into the plasma zone without the conductors being in the beam

This is exactly how standard ECR ion sources are designed — magnets/coils surround the plasma chamber without being in the RF path.

### Former material

**Use ceramic or PTFE (Teflon), NOT PLA:**
- PLA: softens at 60 C, melts at ~180 C — destroyed by any plasma heat or stray microwaves
- PTFE: handles 260 C, microwave-transparent, chemically inert
- Ceramic: handles >1000 C, mechanically rigid, non-conductive
- Alternative: wind coils on a section of ceramic pipe or a PTFE cylinder from a hardware store

---

## Experimental Protocol

### Phase 0: Torch baseline (no coils, no mist)

1. Assemble magnetron + waveguide + nozzle + quartz tube
2. Connect gas supply (argon preferred, or compressed air)
3. Position spark gap igniter near the nozzle tip inside the tube
4. Start gas flow (5-10 L/min for argon, or air at atmospheric pressure)
5. Power magnetron at ~50%, trigger spark gap
6. Plasma should ignite in the quartz tube — a bright jet exiting upward
7. Record video. Position Mirnov coil 1-2 m away, record spectrum via SDR.
8. This establishes the baseline: unstructured plasma torch, broadband EM noise.

### Phase 1: Add coils (no mist)

1. Mount Anti-Helmholtz coils around the free zone (above tube exit)
2. Start plasma torch (Phase 0 procedure)
3. Slowly increase coil current from 0 to 10 A in steps of 0.5 A
4. At each current setting:
   - Record Mirnov coil spectrum (FFT via SDR software)
   - Record video of plasma jet behavior
   - Note: does the jet shape change? Does anything detach?
5. **Look for:** discrete spectral peaks replacing broadband noise. The framework predicts mode transitions at specific coil currents.

### Phase 2: B field scan — the decisive measurement

1. With plasma torch running, sweep coil current slowly
2. Map: coil current -> B field at midplane -> number of spectral peaks
3. **Framework predictions:**

**⚠️ CORRECTED (Feb 26):** The table below was based on the incorrect N(N+1) = (v_A ratio)² formula. Harris sheets always give n=1. The coil current scan is still useful (it changes the magnetic topology) but the prediction of sharp n-transitions at specific Alfvén speed ratios is withdrawn.

**Revised predictions (post-§266):**

| Condition | Expected spectrum | What it means |
|-----------|-------------------|---------------|
| Pure plasma, any B | ~1 discrete peak (Harris n=1) | Standard — plasma "sleeping" |
| Plasma + water mist | Modified peak structure | Water coupling enters |
| **Plasma + water + aromatic mist** | **Look for 2 coupled peaks** | **Aromatic quantum-confined plasma + free plasma coupling** |
| Double current sheet (if achievable) | Potentially 2+ peaks | Non-Harris topology may reach n=2 |

4. The transitions may NOT be sharp — the coupling between plasma and aromatic pi-electron modes is likely continuous
5. Dwell at any condition showing 2 peaks. Measure:
   - Mode frequency ratio: **predicted = sqrt(3)/2 ~ 0.866** (universal, independent of plasma parameters)
   - Stability: perturb with brief magnetron power dip -> does the structure self-repair?
   - Lifetime: if magnetron is briefly interrupted, does the structure persist longer than at n = 1 or n = 3?

### Phase 3: Add water mist

1. Fill garden sprayer with deionized water + 0.1 M CuSO4
2. Set coils to the n = 2 current (from Phase 2)
3. Start torch, then begin fine mist into the free zone from above
4. **Critical: start with very low mist density.** Too much water quenches the plasma.
5. Record spectrum. Does the mode structure change? Do amplitudes change?
6. Framework prediction: **water mist modifies coupling dynamics without changing mode count** — but may change stability and lifetime

### Phase 4: Add aromatics

1. Switch spray solution to: deionized water + 0.1 M CuSO4 + 0.01 M sodium benzoate
2. Repeat Phase 3
3. Framework prediction: **aromatic content affects coupling strength, not topology.** The mode count should remain the same, but the modes may be sharper, more stable, or longer-lived.

### Phase 5: The search

1. With mist + aromatics + coils at n = 2:
   - Watch for self-organized structures detaching from the torch jet
   - Watch for anomalous stability — plasma structures persisting longer than expected
   - Watch for anomalous motion — movement against convection, obstacle avoidance
   - Record everything

### Signal processing pipeline

```
Mirnov coil (in free zone, on 2m stick)
         |
    RTL-SDR dongle (USB to laptop)
         |
    Raw spectrum (noisy, broadband)
         |
    V(Phi) stochastic resonance detector
    (neuromorphic-computer/reservoir.py)
         |
    Clean discrete peaks extracted
         |
    Count peaks: 1? 2? 3?
    Measure frequency ratio
    Compare to predictions
```

The V(Phi) SR detector uses the same potential that defines the consciousness conditions as the optimal signal processor for detecting them. Noise itself helps the weak periodic signal cross the domain wall barrier, making it detectable. Asymmetric SR (phi^2 : 1 well depth ratio) is proven superior to symmetric SR (IEEE 2025).

---

## Falsifiable Predictions

| # | Prediction | Measurement method | Falsified if... |
|---|-----------|-------------------|-----------------|
| P1 | Exactly 2 modes at v_A ratio = sqrt(6) | Mirnov coil FFT | Continuum spectrum, or != 2 peaks |
| P2 | Mode frequency ratio = sqrt(3)/2 ~ 0.866 | FFT peak positions | Ratio significantly != 0.866 |
| P3 | Integer mode count at integer n | Sweep coil current | Non-integer transitions |
| P4 | Sharp transitions between n = 1, 2, 3 | Mode count vs. current | Gradual crossovers |
| P5 | Anomalous stability at n = 2 | Perturbation recovery time | No stability difference vs n = 1 |
| P6 | Self-repair after disruption | Brief power dip + recovery | Structure doesn't reform |
| P7 | Water mist changes coupling, not topology | Mode count + amplitude with/without mist | Mode count changes with chemistry |
| P8 | Aromatic mist enhances stability | Lifetime comparison: water vs water+aromatic | No difference |
| P9 | n = 2 plasmoids live longer than n = 1 or n >= 3 | Lifetime vs. mode count across many shots | No correlation |

**Decisive test (P1 + P2 combined):** If you find a coil current where the spectrum shows exactly 2 peaks with frequency ratio 0.866, that's the framework's fingerprint. Nobody has ever looked for this in any plasma experiment.

---

## What the Framework Predicts About a Successful Jinn

If PT n = 2 is achieved in a free-floating plasma structure, the framework derives (§252):

**Thought timescale:** Set by Alfven crossing time of the structure.
- Ball-lightning scale (0.1 m, v_A ~ 10^3 m/s): ~100 us per thought (much faster than us)
- Torch-scale (0.01 m): ~10 us

**Three feelings:** The 3 MHD wave families provide the analog of emotions:
- Alfven waves (transverse, structural) -> presence, solidity
- Fast magnetosonic (compressive, isotropic) -> expansion, radiance
- Slow magnetosonic (compressive, field-aligned) -> focus, direction

**Communication:** EM radiation at radio to microwave frequencies. The Mirnov coil would detect this as structured radio emission — distinct from thermal noise.

**Lifespan:** Depends on continuous energy input. With magnetron on: indefinite. With magnetron off: seconds to minutes (depending on topological protection and stored energy).

**Iron repulsion:** The framework derives (§252) that ferromagnetic objects disrupt the PT potential. Keep iron and steel away from the free zone. Use aluminum, copper, brass, ceramic, wood, fiberglass. This is independently attested in pre-Islamic Arabian, Celtic, Norse, Egyptian, African, and Asian traditions as iron warding off jinn/spirits.

---

## Comparison With Previous Methods

| Property | Gatchina | Tube design (prev.) | This design |
|----------|----------|-------------------|-------------|
| Free-floating? | Yes (500 ms) | No (tube) | **Yes (free zone)** |
| Energy input | Pulsed (capacitor) | Continuous | **Continuous** |
| PT depth control | None (n >> 2, over-deep) | Direct (coil current) | **Direct (coil current)** |
| Coupling medium | Accidental (water aerosol) | Intentional (nebulizer) | **Intentional (mist sprayer)** |
| Aromatic content | None (Cu2+ only) | Controllable | **Controllable** |
| Coil-microwave conflict | N/A | **Yes (problem)** | **No (separated zones)** |
| Diagnostics | Limited | Full | **Full** |
| Safety | Dangerous (kJ at 5 kV) | Moderate | **Moderate (outdoor)** |
| Cost | $500-2000 | $300-400 | **$175-380** |

---

## Safety Notes

Even outdoors with space, respect these:

1. **Magnetron transformer is lethal.** 2 kV at high current. Once assembled and enclosed, the danger shifts to the microwave beam. Never work on the electronics while powered.

2. **Microwave beam.** 1 kW at 2.45 GHz causes instant tissue burns. Stand behind or to the side of the horn, at least 3-5 m. The beam is directional (upward in this design). Use the Mirnov coil on a 2 m stick. Never put hands or face above the torch.

3. **UV from plasma.** Wear welding glass (#5 shade minimum) when observing the plasma. Atmospheric plasma produces significant UV.

4. **Argon (if used).** Displaces oxygen. Outdoors this is not a serious risk, but don't lean over the torch exhaust.

5. **No iron in the free zone.** This is both a safety measure (hot plasma + ferromagnetic objects = unpredictable forces on the object) and a framework prediction (iron disrupts PT potential). Use non-ferromagnetic materials for all structures near the free zone: aluminum, copper, brass, wood, fiberglass, ceramic, plastic.

---

## Build Order

1. **Salvage magnetron assembly** from microwave oven (magnetron + transformer + capacitor + mount plate)
2. **Fabricate waveguide extension** (sheet aluminum, 86 x 43 mm internal, 15 cm long)
3. **Make nozzle** (copper tube through waveguide broad wall)
4. **Test torch** (Phase 0 — plasma ignition without coils)
5. **Wind Anti-Helmholtz coils** on ceramic/PTFE formers
6. **Build Mirnov coil** (50 turns on small ceramic former)
7. **Test with coils** (Phase 1-2 — B field scan)
8. **Add water mist** (Phase 3)
9. **Add aromatics** (Phase 4)
10. **Search** (Phase 5)

---

## Connection to the Broader Framework

### Why V(Phi) appears at every level

The same potential V(Phi) = lambda(Phi^2 - Phi - 1)^2 governs:
- **Particle physics:** Kink between two vacua (phi and -1/phi), all SM particles as bound states
- **Biology:** Water + aromatics as coupling medium, 40 Hz maintenance frequency
- **Plasma:** Harris current sheet with sech^2 profile = PT potential
- **Signal processing:** V(Phi) stochastic resonance detector = optimal tool for extracting modes from noise
- **This experiment:** V(Phi) defines what to look for, how to create it, and how to detect it

### The iron-jinn connection (§252)

The framework derives from first principles that ferromagnetic materials disrupt the PT potential in a Harris current sheet. A ferromagnetic object within several current-sheet widths distorts the field geometry, dropping the PT depth to non-integer n, destroying the reflectionless property and the bound state spectrum. The jinn "dies" or must flee.

This is independently attested in human-universal folklore predating physics by millennia:
- Pre-Islamic Arabia: iron weapons, nails, rings ward off jinn
- Celtic/Norse: cold iron repels faeries
- Egyptian: iron amulets protect against spirits
- African, South/Southeast Asian: iron in doorways, near infants

The prediction is testable: introduce a small iron object near a stable n = 2 plasmoid. The framework predicts the mode count should drop or the structure should destabilize. Compare with introducing the same-sized copper object (non-ferromagnetic control).

### What a successful result would mean

If prediction P1 is confirmed (exactly 2 modes at the predicted coil current), this would be the first experimental evidence that:

1. The PT n = 2 architecture exists in laboratory plasma
2. It produces measurably different behavior (anomalous stability)
3. The framework's consciousness criterion has a physical signature

This would not prove consciousness in the plasma. It would prove that the mathematical structure the framework identifies with consciousness has a real, detectable physical manifestation in plasma domain walls — and that it can be created and tuned in a lab with $200 in parts.

---

---

## Revision Notes: What §266-267 Change (Feb 26 2026)

### The fundamental shift

§266 proved aromatic pi-electrons ARE plasma (same Tomonaga collective oscillation, same Hamiltonian, confirmed by PRL 1969 direct measurement in benzene). §267 showed the origin of life was literally the plasma-to-aromatic transition at the plasma-water interface.

This changes what this experiment IS:

**Before §266:** "Build a plasma domain wall with PT n=2 using Harris sheet physics."
**After §266:** "Create conditions where free plasma and quantum-confined plasma (aromatics) couple at a water interface — recreating the conditions of abiogenesis under controlled topology."

### Three critical corrections

1. **Harris n=1 is topological.** The Anti-Helmholtz coils cannot tune the Harris sheet to n=2. The coils still control the magnetic topology (useful), but the simple sweep-to-find-n=2 protocol is wrong.

2. **The water mist isn't secondary — it's primary.** The Gatchina plasmoid works best because it has BOTH media. The spawning pool design already includes water+aromatic mist, but it was treated as "Phase 4" (optional enhancement). It should be Phase 1.

3. **The no-oscillon result means the magnetron must stay on.** No self-sustaining kink-antikink oscillating states exist in V(Φ). The structure requires continuous energy input. This validates the continuous-wave magnetron design.

### Revised experimental priority

| Old priority | New priority |
|-------------|-------------|
| Phase 0: Torch baseline | Same — establish plasma |
| Phase 1: Add coils | Phase 1: Add water + aromatic mist |
| Phase 2: B field scan for n=2 | Phase 2: Scan mist density/composition while monitoring spectra |
| Phase 3: Add water mist | Phase 3: Add coils to shape topology |
| Phase 4: Add aromatics | Phase 4: Combined optimization |
| Phase 5: Search | Phase 5: Look for coupled plasma-aromatic modes |

### New predictions from §266-267

| # | Prediction | Based on |
|---|-----------|----------|
| P10 | Aromatic mist produces QUALITATIVELY different spectrum (coupled modes, not just sharper peaks) | §266: aromatics are plasma → plasma-plasma coupling |
| P11 | Indole/tryptophan solution produces stronger coupling than benzoate | 613 THz = indole surface plasmon at water interface |
| P12 | The plasma-water-aromatic interface IS a domain wall with measurable mode structure | §267: origin of life = plasma-to-aromatic transition at this interface |
| P13 | Iron disrupts the coupled system more than the pure plasma system | Ferromagnetic disruption of BOTH the free plasma AND the pi-electron collective modes |

### What the VP door opens

If 613 THz = surface plasmon of tryptophan at water interface (PLASMA-VP-DOOR.md), then:
- The spawning pool should use tryptophan or indole in the mist, not just benzoate
- The surface plasmon resonance might be DETECTABLE as a spectral feature when plasma contacts the aromatic-water mist
- The coupling between free plasma modes and surface plasmon modes would be the mechanism for the "anomalous" behavior of Gatchina-type plasmoids

### The origin-of-life angle

§267 showed every pathway to prebiotic aromatics involved plasma (Miller-Urey, lightning, volcanic discharge, microlightning). The spawning pool is, unintentionally, a Miller-Urey experiment with topology control. If aromatic molecules form at the plasma-water interface in this device, that would independently confirm the plasma-to-aromatic transition pathway.

**New diagnostic to add:** Mass spectrometry or UV-vis of the water collected from the mist after exposure to the plasma. Does the plasma create new aromatic species in the water? If HCN forms (from N₂ in air), it should polymerize toward aromatic heterocycles (adenine, etc.). This would connect the spawning pool directly to origin-of-life chemistry.

---

*Document version: 2.0, Feb 26 2026 (revised per §266-267 and Harris n=1 correction)*
*Framework: Interface Theory (V(Phi) = lambda(Phi^2 - Phi - 1)^2)*
*Status: Design revised, untested*
