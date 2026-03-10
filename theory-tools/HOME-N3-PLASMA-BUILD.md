# Home-Scale n>1 Plasma: Build & Measure Guide

*Feb 27 2026. Practical guide to creating and detecting trapped MHD modes at home.*

---

## The Core Insight

Harris current sheets (B = B₀·tanh(x/a)) **always** give PT n=1. This is topological — you cannot escape it by scaling up. To get n>1 you need a **magnetic well**: a region where B is minimum at center and rises on both sides. This is the exact opposite of a current sheet.

The master equation:

```
V_eff(x) = -d²/dx²[ln B(x)] = -B''(x)/B(x) + [B'(x)/B(x)]²
```

For a magnetic well B(x) = B₀(1 + δ·sech²(x/a)):
- The curvature at the center gives effective PT depth
- δ > 0 means a WELL (minimum at center)
- The larger the well depth δ relative to the background, the higher the PT n

For n=2: need n(n+1) = 6 units of normalized curvature
For n=3: need n(n+1) = 12 units

**Key realization**: You don't need a $100M FRC. You need two magnets facing same-pole, with plasma between them. That's it.

---

## Part 1: The Simplest n>1 Build (~$30-80)

### Approach: Two Opposing N52 Magnets + Discharge Tube

Two powerful neodymium magnets with same poles facing each other create a magnetic mirror / magnetic well geometry. The field is minimum at the midpoint and rises sharply toward each magnet. Any plasma in that well sees a sech²-like potential with depth controlled by magnet strength and spacing.

#### Equipment

| Item | Spec | Cost | Source |
|------|------|------|--------|
| N52 neodymium disk magnets (×2) | 25mm × 10mm, ~1.4T surface | $12-20 | Amazon/eBay |
| Neon sign transformer (NST) | 9kV/30mA | $20-40 | eBay/surplus |
| Glass tube | 200-300mm, ~25mm OD borosilicate | $5-15 | eBay/lab supply |
| Electrodes | Stainless steel bolts + silicone stoppers | $5 | Hardware store |
| Magnet holder | Wood/acrylic blocks, adjustable spacing | $5-10 | DIY |
| Wire, connectors, safety gear | Insulated HV wire, gloves, goggles | $10-15 | Hardware store |

**Total: ~$60-100**

#### Build

1. **Glass tube discharge cell**: Seal stainless steel bolt electrodes into each end of the glass tube with silicone. Leave air at atmospheric pressure (easiest) or use a small hand vacuum pump to pull partial vacuum (~10-50 Torr) for cleaner discharge.

2. **Magnetic well**: Mount the two N52 magnets on a rail with **same poles facing** (they repel). Space them ~100-150mm apart with the glass tube between them, centered at the midpoint. Use wooden blocks or an acrylic track.

3. **Field profile**: At midpoint between two opposing 25mm N52 disks spaced 120mm:
   - B_center ≈ 30-50 mT (minimum)
   - B_near_magnet ≈ 200-400 mT (maximum)
   - Ratio B_max/B_min ≈ 6-10x → significant well depth
   - Profile approximates sech² with δ ≈ 5-9

4. **Strike the discharge**: Connect NST to electrodes. The plasma fills the tube. The magnetic well TRAPS certain wave modes — they bounce between the magnetic mirrors.

5. **Adjust spacing**: Moving magnets closer = deeper well = higher effective n. Moving apart = shallower well. This is your PT depth knob.

#### Why This Should Give n>1

A standard discharge tube with no magnets: no trapped modes (free propagation).
A discharge tube with ONE magnet: monotonic field, no well, traveling modes only.
A discharge tube with TWO same-pole magnets: magnetic well = potential well for MHD perturbations. The confined wave modes are exactly the bound states of V_eff.

The well depth parameter δ controls n. For two 25mm N52 disks at 120mm spacing, the normalized curvature is large enough that n=2 is very plausible. Getting confirmed n=3 would require either stronger magnets, closer spacing, or a more carefully shaped field.

### Variant: Ring Magnets

Two ring magnets (same-pole) create a more uniform well across the tube cross-section. Less fringing = cleaner mode structure. 50mm OD ring magnets with 20mm ID, tube through the center holes, ~$15-25 each.

### Variant: Plasma Globe + External Magnets

The absolute cheapest approach ($0 + existing plasma globe):

1. Take any plasma globe (the ones from novelty shops)
2. Place two N52 magnets on opposite sides, same pole facing the globe
3. Watch the plasma filaments CHANGE — they will concentrate in the magnetic well region between the magnets
4. The visible change in filament behavior is direct evidence of the well trapping modes

This is qualitative only — you can see the well's effect but can't count modes. Good for demonstration, not measurement.

---

## Part 2: How to Measure It — 5 Methods, Cheapest First

### Method 1: AM Radio (~$0-10)

**The simplest possible detector.** Plasma oscillations at kHz-MHz frequencies are directly receivable by any AM radio.

1. Tune an AM radio to a quiet spot on the dial
2. Place it 30-50cm from the plasma
3. Turn plasma on/off, move magnets
4. Listen for tone changes and count distinct pitches

**What you're hearing**: The plasma has natural oscillation frequencies. Trapped modes show up as discrete tones. Untrapped modes show up as broadband hiss. More magnets = more tones = more bound states.

**Limitations**: Qualitative. You can hear the modes but can't precisely count or characterize them. Good for "is something there?"

### Method 2: Microphone + FFT (~$0-5)

Plasma makes sound (ion acoustic modes). Especially in atmospheric/partial-vacuum discharge:

1. Place any microphone near the discharge tube
2. Record audio with Audacity (free)
3. Run FFT (Analyze → Plot Spectrum)
4. Look for discrete spectral peaks vs continuous spectrum

**Key**: Magnetic well ON should show discrete peaks. Magnets removed should show broadband. Count the peaks.

**Limitations**: Sound modes may not directly correspond to MHD modes. Coupling from EM to acoustic is indirect. But discrete peaks vs no peaks is diagnostic.

### Method 3: BPW34 Photodiode (~$5-10)

The BPW34 silicon PIN photodiode detects plasma light fluctuations at MHz bandwidth. This is real plasma diagnostics on a budget.

#### Circuit

```
                   +5V
                    |
                   [1kΩ]
                    |
        BPW34 ──────┤──── Signal Out → oscilloscope/sound card
        (reverse    |
         biased)  [0.1µF]
                    |
                   GND
```

1. BPW34 reverse-biased through 1kΩ load resistor
2. AC-couple output through 0.1µF cap
3. Feed into:
   - Oscilloscope (best: see waveforms directly)
   - Sound card line-in (cheap: use Audacity FFT)
   - USB oscilloscope ($20-50 if you don't have one)

4. Point at the discharge tube (small aperture preferred — pinhole or short tube to sample specific plasma region)

**What you see**: The FFT of light fluctuations shows the plasma oscillation spectrum. Trapped modes = discrete peaks. Free modes = continuum. The NUMBER of discrete peaks below the continuum edge = number of bound states = PT depth estimate.

**This is the core measurement.** If you see:
- 1 discrete peak → n=1 (sleeping, like Harris)
- 2 discrete peaks → n=2 (awake, like biology)
- 3 discrete peaks → n=3 (deeply awake, beyond biology)

### Method 4: Mirnov Coil (~$3-5)

A small pickup coil measures magnetic fluctuations directly. This IS what fusion labs use, just smaller.

#### Build

1. Wind 50-100 turns of 30 AWG magnet wire on a 10mm former (pen cap, dowel)
2. Twist the leads together (reduces electric field pickup)
3. Connect to oscilloscope or sound card (through 100Ω termination)

#### Use

1. Place the coil 20-50mm from the discharge tube
2. Orient perpendicular to the tube axis (picks up radial B fluctuations)
3. Run FFT on the signal
4. Same analysis: count discrete spectral peaks

**Advantage over photodiode**: Directly measures magnetic fluctuations (the actual MHD modes), not optical proxies. Cleaner signal-to-physics correspondence.

**Build time**: 15 minutes.

### Method 5: RTL-SDR Dongle (~$30)

The RTL-SDR V3 covers 500 kHz to 1.7 GHz. Use with free SDR# or SDR++ software.

1. Connect RTL-SDR to laptop
2. Use a short wire antenna (10-20cm) or the Mirnov coil as antenna
3. Open SDR# in FM/AM mode
4. Scan the waterfall display for discrete emission lines from the plasma
5. Compare: magnets present vs removed

**Advantage**: Huge bandwidth. See everything from kHz to GHz simultaneously on the waterfall display. Can capture screenshots for documentation.

**Best settings**: Sample rate 2.4 MSPS, gain auto or manual ~20-30 dB, waterfall + spectrum view.

---

## Part 3: The Experimental Protocol

### Phase A: Baseline (No Magnets)

1. Strike discharge in tube (no magnets)
2. Record spectrum with ALL available detectors for 60 seconds
3. Save FFT snapshots
4. Note: should see broadband or few weak features (no well = no trapping)

### Phase B: Magnetic Well (Two Opposing Magnets)

1. Place N52 magnets at starting spacing (e.g., 150mm)
2. Strike discharge
3. Record spectrum 60 seconds
4. **Gradually decrease spacing** in 10mm steps: 150, 140, 130, ..., 80mm
5. At each step: record spectrum, note number of discrete peaks
6. Save all data

**Prediction (framework)**: As spacing decreases, well deepens. New discrete peaks should APPEAR one by one. The sequence should be:
- Wide spacing: 0-1 peaks (shallow well, n≤1)
- Medium spacing: 2 peaks (n=2 threshold)
- Close spacing: 3 peaks (n=3 if well is deep enough)

### Phase C: Single Magnet Control

1. Remove one magnet (keep the other)
2. Monotonic field — no well
3. Should see NO discrete trapped modes (only traveling waves)
4. This is the null control

### Phase D: Reversed Polarity Control

1. Flip one magnet (opposite poles facing = attraction = field MAXIMUM at center)
2. This is a magnetic hill, not a well
3. Should see NO trapped modes (anti-trapping)
4. Strongest null control

### What Constitutes Evidence

| Observation | Interpretation |
|---|---|
| No change between phases A-D | Null result. Modes not detectable by this method. |
| Discrete peaks appear in Phase B only | **Magnetic well traps modes.** Count peaks = effective n. |
| Peak count increases as magnets approach | **Well depth controls n.** Exactly the PT prediction. |
| Phase C and D show no peaks | **Confirmed: well geometry is necessary.** |
| 2 peaks with specific energy ratio ~4:1 | **Strong match to PT n=2** (E₀:E₁ = 4:1 for n=2). |
| 3 peaks with ratios matching n=3 | **PT n=3 achieved.** Framework prediction beyond biology. |

---

## Part 4: Beyond Magnets — Other Home Routes

### Route 2: Ferrofluid Analog (~$20-40)

Ferrofluid in a Hele-Shaw cell (two glass plates, ~1mm gap) between two same-pole magnets creates visible domain wall structures. Not plasma, but the SAME sech² potential governs the interface dynamics.

1. Ferrofluid ($15-25, Amazon)
2. Two glass slides + spacer tape → Hele-Shaw cell
3. Two N52 magnets, same pole facing
4. Watch the fluid interface form a wall structure
5. Tap/shake the cell → observe trapped oscillation modes at the interface

**What you see**: The interface between ferrofluid-rich and ferrofluid-poor regions oscillates. Trapped modes are visible as standing wave patterns along the interface. Count the nodes.

This is a CLASSICAL ANALOG of the quantum PT problem. Same math, visible to the naked eye.

### Route 3: Speaker Coil Modulation (~$30-50)

Replace permanent magnets with speaker coils (or electromagnets wound on iron bolts):

1. Two coils on iron cores, same-pole configuration
2. Drive with audio amplifier at variable frequency
3. The magnetic well OSCILLATES in time
4. Parametric driving: can selectively excite specific trapped modes

**Advantage**: You can SWEEP the driving frequency and watch modes light up one by one. Each mode has a specific resonance frequency — you literally tune into them like radio stations.

### Route 4: Microwave ECR with Permanent Magnets (~$50-200)

Electron Cyclotron Resonance at 2.45 GHz requires B = 87.5 mT. Two N52 disk magnets (50mm) in a magnetic well geometry can achieve this at the mirror points while having a lower field at center.

1. Magnetron from a microwave oven (free, careful extraction)
2. Two large N52 magnets creating well with B ≈ 87.5 mT at mirrors
3. Small vacuum chamber (jar + hand pump)
4. ECR heats electrons → plasma forms in well → modes are trapped

**Warning**: Microwave radiation is dangerous. Proper shielding required. This is the most capable home setup but also the most hazardous. Faraday cage mandatory.

---

## Part 5: What Each Measurement Means for the Framework

### If you see 2 trapped modes in a magnetic well:

- **Confirmed**: Magnetic wells create PT n=2 potentials (already well-known in plasma physics)
- **Framework connection**: Same n=2 that biology uses, created with magnets instead of chemistry
- **Implies**: The heliosphere (magnetic well between solar wind and ISM) should also show n≈2
- **Cross-check**: Matches Voyager analysis (n=2.01-2.38)

### If you see 3 trapped modes:

- **Confirmed**: n=3 is physically achievable in lab-scale plasma
- **Framework connection**: This is the Level 2 regime (x³−3x+1=0, Z₃ triality)
- **Biology can't go there** (UV damage at f_mol(n=3)=1070 THz)
- **Plasma CAN** — no thermal window constraint
- **Prediction**: n=3 plasma should show qualitatively different collective behavior (3-body correlations, triality symmetry breaking)

### If the energy ratio E₀/E₁ ≈ 4:1 for n=2:

- **Strong confirmation**: PT n=2 predicts exactly 4:1 (binding:breathing = 4n²/(n²-1)² at n=2)
- **This is the number to match.** It distinguishes PT from generic double-well potentials.

### If discrete modes appear/disappear exactly at predicted magnet spacings:

- **Strong confirmation**: V_eff formula correctly predicts mode trapping thresholds
- **Use**: Calibrate well depth vs spacing → predict exactly when n=3 threshold is crossed

---

## Part 6: Safety

### Electrical

- **NST**: 9kV can kill. Use insulated leads, one hand rule, capacitor bleeder resistors.
- **Magnetron**: 2.45 GHz + 1kV. Lethal if mishandled. Full Faraday cage. Never operate with door open.
- **Capacitors**: Bleed all caps before touching anything.

### Magnetic

- **N52 magnets are STRONG.** Two 25mm disks will pinch flesh and break bones at close range.
- Always approach slowly. Never let them snap together freely.
- Keep away from electronics, credit cards, pacemakers.
- Handle with thick gloves.

### Plasma

- UV from discharge tubes. Don't stare at it.
- Ozone production at atmospheric pressure. Ventilate.
- Glass tubes can implode under vacuum. Use borosilicate, safety glasses.

---

## Part 7: Priority Ranking

**If you build one thing, build this:**

1. **Glass tube + two N52 magnets + BPW34 photodiode** ($60-80 total)
   - Simplest system that answers the question
   - Variable well depth (adjust spacing)
   - Quantitative measurement (FFT of light fluctuations)
   - Clear null controls (remove magnets, flip polarity)
   - 2-3 hours to build, 1-2 hours to measure

2. **Add Mirnov coil** (+$3, +15 min)
   - Direct magnetic fluctuation measurement
   - Cross-check photodiode results

3. **Add RTL-SDR** (+$30)
   - Broadband spectrum overview
   - Waterfall display is visually compelling for documentation

4. **Add speaker coils** (+$20-30)
   - Active driving lets you find modes by sweeping frequency
   - More controlled than just counting spontaneous peaks

**The question "can we get n=3 at home?" reduces to**: can two N52 magnets at ~80mm spacing create a magnetic well deep enough that the normalized curvature exceeds n(n+1)=12? The field profiles suggest yes for 50mm-diameter magnets, but the answer is in the measurement. That's the whole point.

---

## Appendix: Quick Reference Card

```
WHAT TO BUY (minimum):
  2× N52 neodymium disk magnets, 25mm×10mm        $12-20
  1× Neon sign transformer 9kV/30mA               $20-40
  1× Borosilicate tube 250mm, 25mm OD              $5-15
  2× Stainless steel bolts + silicone stoppers      $5
  1× BPW34 photodiode                               $2
  1× 1kΩ resistor + 0.1µF cap                       $1
  Wire, connectors, safety gear                     $10-15
  TOTAL:                                            ~$60-100

WHAT TO MEASURE:
  FFT of photodiode signal → count discrete peaks below continuum

  0-1 peaks = n≤1 (sleeping)
  2 peaks   = n=2 (awake)
  3 peaks   = n=3 (beyond biology)

CONTROLS:
  A. No magnets → baseline (broadband)
  B. Two magnets same-pole → well → trapped modes
  C. One magnet → no well → no trapping
  D. Two magnets opposite-pole → hill → anti-trapping

THE NUMBER THAT MATTERS:
  Energy ratio of lowest two modes: PT n=2 predicts 4:1
```
