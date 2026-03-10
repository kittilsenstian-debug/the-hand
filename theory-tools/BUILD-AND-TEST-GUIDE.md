# BUILD AND TEST GUIDE — Domain Wall Coupling Devices

*Everything you need to build, test, and measure. No funding required.*

---

## Overview: Three Builds, Three Tests

| Build | Cost | Time | What it proves |
|-------|------|------|----------------|
| **A. PT n=2 Circuit** | $33-100 | 1-2 weekends | The math is physically real |
| **B. Plasma Domain Wall** | $60-150 | 1 weekend | Plasma creates n=2 with 3 modes |
| **C. Coupling Tub** | $80-130 | 1 evening | Three-frequency biological effect |

**Testing** requires an HRV monitor ($50-100) and optionally an SDR dongle ($25) or cheap scope ($20).

---

## BUILD A: PT n=2 LC Circuit ($33-100)

*Proves: exactly 2 bound states, reflectionlessness, 4:1 energy ratio.*

### Shopping List

| Item | Where | Cost |
|------|-------|------|
| 20x T68-2 toroid cores (red) | Mouser/DigiKey/eBay | $10 |
| 30 AWG magnet wire (1/4 lb) | Amazon/eBay | $8 |
| 25x 100nF C0G capacitors (1%) | Mouser/DigiKey | $4 |
| 4x 100 ohm resistors (1%) | Mouser/DigiKey | $1 |
| Perfboard 10x15cm | Amazon | $3 |
| Hookup wire, headers, BNC connectors | Amazon | $8 |
| **Subtotal (passive)** | | **$34** |

Test equipment (pick one):

| Option | Cost | What you get |
|--------|------|--------------|
| Phone + free tone app + piezo buzzer | $0 | Qualitative (hear the peaks) |
| AD9833 DDS module + DSO138 scope kit | $30+$20 | Full measurement |
| USB scope (Hantek/similar) | $60-80 | Best for PC capture |

### Build Steps

**Step 1: Wind 20 inductors (4-6 hours, the longest step)**

Each inductor is magnet wire on a T68-2 toroid. The number of turns sets the inductance.

| Link position | Target L (uH) | Turns on T68-2 | Notes |
|---------------|---------------|-----------------|-------|
| 0, 19 (ends) | 999 | 60 | ~background L0 |
| 1, 18 | 996 | 60 | barely dipped |
| 2, 17 | 987 | 60 | |
| 3, 16 | 966 | 59 | |
| 4, 15 | 930 | 58 | |
| 5, 14 | 882 | 56 | |
| 6, 13 | 832 | 55 | |
| 7, 12 | 793 | 53 | |
| 8, 11 | 775 | 53 | |
| 9, 10 (center) | 770 | 53 | deepest dip = 77% of L0 |

Formula: L(j) = L0 * [1 - 0.233/cosh^2((j - 9.5)/2.5)]

Wind each toroid. Measure with an LCR meter if you have one. If not, the turn counts above are calibrated for T68-2 cores (AL = 57 nH/turn^2).

**Step 2: Assemble on perfboard (2-3 hours)**

```
  BNC_IN --- [R=100] --- L0 --- L1 --- L2 --- ... --- L19 --- [R=100] --- BNC_OUT
                         |      |      |               |
                        C0     C0     C0              C0
                         |      |      |               |
                        GND    GND    GND             GND
```

21 capacitors to ground, 20 inductors in series, 100 ohm termination at each end.

**Step 3: Test (2-3 hours)**

### TEST A: Count the Bound States

1. Connect function generator to BNC_IN
2. Connect scope/voltmeter to BNC_OUT
3. Sweep frequency from 25 kHz to 37 kHz slowly
4. Record output amplitude vs frequency

**What you should see:**

```
Amplitude
  |
  |  ___________                    *        *
  | /           \                  / \      / \
  |/             \________________/   \    /   \
  |               passband edge    BS1  \  / BS2
  +-------------------------------------------- freq
  25 kHz         ~31.7 kHz      ~32.5  ~34.8 kHz
```

Two peaks above the passband edge. Not one. Not three. **Exactly two.**

- Peak 1 (breathing mode): ~32,520 Hz
- Peak 2 (ground state): ~34,753 Hz
- Energy ratio: (34753^2 - 31742^2) / (32520^2 - 31742^2) = **4.0 +/- 0.5**

**If you see 2 peaks with ratio near 4:1 → PT n=2 confirmed.**

### TEST A2: Reflectionlessness (qualitative)

1. Send a short burst (2-3 cycles) at ~15 kHz into one end
2. Watch for reflected signal at the same end on the scope
3. Compare with a uniform chain (all inductors = L0)
4. The n=2 chain should show **much less reflection**

### Controls

Build a second chain with all inductors identical (L0 = 1 mH, no dip). This should show:
- No peaks above the passband
- Stronger reflections
- This is your null control

---

## BUILD B: Plasma Domain Wall ($60-150)

*Proves: magnetic well creates PT potential in plasma. 3 MHD modes.*

### Shopping List

| Item | Where | Cost |
|------|-------|------|
| 2x N52 neodymium disk magnets (25x10mm) | Amazon/K&J Magnetics | $15-20 |
| Neon sign transformer (9kV/30mA) | eBay/surplus store | $20-40 |
| Borosilicate glass tube (25mm OD, 200-300mm) | Amazon/lab supply | $8-15 |
| 2x stainless steel bolts (electrode) | hardware store | $2 |
| Silicone stoppers or epoxy | hardware store | $5 |
| Wood/acrylic blocks for magnet rail | hardware store | $5-10 |
| HV wire + safety gear (gloves, goggles) | hardware store | $10-15 |
| **Subtotal** | | **$65-105** |

Detection (pick one or more):

| Method | Cost | Quality |
|--------|------|---------|
| AM radio (tune to quiet spot) | $0 (use phone) | Qualitative — hear discrete tones |
| RTL-SDR V3 dongle | $25 | Broadband spectrum, best bang/buck |
| BPW34 photodiode + resistor | $2 | Light fluctuation FFT |
| Mirnov coil (50 turns, 30AWG) | $3 | Direct magnetic oscillation |

**Best combo: RTL-SDR ($25) + Mirnov coil ($3) = $28 total for quantitative measurement.**

### Build Steps

**Step 1: Make the discharge tube (1-2 hours)**

1. Insert stainless bolt into each end of glass tube
2. Seal with silicone stoppers (leave tube at atmospheric pressure for simplest build)
3. For cleaner discharge: evacuate to 10-50 Torr with hand vacuum pump ($15-30 extra)
4. Connect HV leads to bolts

**Step 2: Build the magnetic well (30 min)**

1. Mount magnets on adjustable wooden rail
2. **Same poles facing each other** (repelling). This creates a magnetic WELL between them.
3. Start at 150mm spacing, tube centered between magnets
4. The field profile should be: high near magnets, low in center = sech^2-like well

**Step 3: Safety setup**

- Neon sign transformer is **9kV** — lethal. Respect it.
- Work on insulated surface (rubber mat)
- HV wire must be rated for the voltage
- Keep one hand in pocket when adjusting (old electrician's rule)
- Wear safety goggles (UV from discharge)
- GFCI outlet for the transformer

### TEST B: Count the Modes

**Protocol:**

1. **Phase A — Baseline (no magnets):**
   - Strike discharge (NST on)
   - Record spectrum with RTL-SDR for 60 seconds
   - Note: broadband noise, no discrete peaks expected

2. **Phase B — Magnetic well ON:**
   - Place magnets at 150mm spacing, same-pole facing
   - Strike discharge
   - Record spectrum 60 seconds
   - Decrease spacing to 130mm, record again
   - Decrease to 110mm, record again
   - Decrease to 90mm, record again

3. **Phase C — Single magnet (null control):**
   - Remove one magnet
   - Monotonic field, no well
   - Record spectrum — should see NO discrete peaks

4. **Phase D — Reversed polarity (null control):**
   - Flip one magnet (opposite poles facing = magnetic HILL)
   - Record spectrum — should see NO discrete peaks

**What to look for in the waterfall/FFT:**

| Observation | Meaning |
|-------------|---------|
| Broadband noise in all phases | Null result — modes not detectable |
| Discrete peaks ONLY in Phase B | **Magnetic well traps modes** |
| Peak count increases as magnets approach | **Well depth controls n** |
| 2 peaks at some spacing | **PT n=2 regime found** |
| Phases C and D show NO peaks | **Well geometry is necessary** |

**If you see 2 peaks that appear only when the well is present → plasma domain wall with n=2.**

### Bonus: Observe 3 MHD Families

With the Mirnov coil (magnetic pickup) AND the photodiode (optical pickup) recording simultaneously:
- Some oscillations will appear in magnetic but not optical → Alfven waves (field-line oscillations)
- Some will appear in both → magnetosonic (compression) waves
- If you see 3 distinct frequency families → the 3 MHD modes

---

## BUILD C: Coupling Tub ($80-130)

*Tests: does three-frequency water immersion produce measurable biological effect?*

### Shopping List

| Item | Where | Cost |
|------|-------|------|
| Dayton Audio BST-1 bass shaker (25W) | Amazon/Parts Express | $25-35 |
| Small amplifier (2ch, 20W+) | Amazon | $20-30 |
| IP68 490nm LED strip (1m) | Amazon/AliExpress | $15-25 |
| 12V power supply for LEDs | Amazon | $8-12 |
| **Subtotal** | | **$68-102** |

Plus:
- Existing bathtub (free)
- Phone with tone generator app (free — "Function Generator" app, or Audacity)

Optional measurement:

| Item | Where | Cost |
|------|-------|------|
| HRV monitor (wrist or chest) | Amazon (Polar H10 or similar) | $50-90 |
| Waterproof case for phone | Amazon | $10 |

### Build Steps (1-2 hours)

**Step 1: Mount the bass shaker**
- Bolt or epoxy the BST-1 to the OUTSIDE bottom of the tub
- The tub wall becomes the driver membrane
- This is electrically safe — no electronics in the water

**Step 2: Wire the amplifier**
- Phone headphone out → amplifier input
- Amplifier speaker out → BST-1
- Test dry: place hand on tub, play 40 Hz tone, feel vibration
- Adjust volume: you want gentle vibration, not earthquake

**Step 3: Mount LEDs**
- Run IP68 LED strip along tub rim or submerge (IP68 = submersible)
- Connect to 12V supply with dimmer if available
- 490nm = blue-cyan, the biological aromatic channel frequency

**Step 4: Prepare the protocol**

### TEST C: Three-Frequency Coupling Protocol

**What you need:**
- Bathtub at 37-39°C
- Bass shaker playing 40 Hz sine wave
- 490nm LEDs on (dim, comfortable)
- Timer for breathing (5 sec in, 5 sec out = 0.1 Hz, 6 breaths/min)
- HRV monitor on wrist (waterproof) or chest strap

**Protocol (30 min total):**

| Phase | Time | What to do | What's active |
|-------|------|-----------|---------------|
| **Baseline** | -5 to 0 min | Sit quietly, dry, HRV recording | Nothing |
| **1. Settle** | 0-5 min | Enter water, eyes closed | f₃ only (breathing 0.1 Hz) |
| **2. Activate** | 5-15 min | Continue breathing | f₃ + f₂ (turn on 40 Hz shaker) |
| **3. Full** | 15-25 min | Continue breathing | f₃ + f₂ + f₁ (turn on LEDs) |
| **4. Integrate** | 25-30 min | Dim everything, exit slowly | Fade all |
| **Post** | 30-35 min | Sit quietly, dry, HRV recording | Nothing |

**What to measure (before/after each session):**

| Metric | How | Expected change |
|--------|-----|----------------|
| RMSSD (HRV) | HRV app | Increase (parasympathetic activation) |
| LF/HF ratio | HRV app | Decrease (less stress dominance) |
| Coherence score | HeartMath app | Increase |
| Subjective wellbeing (1-10) | Self-report | Increase |
| Sleep quality (that night) | Self-report next morning | Improvement |

**Controls (do on different days, same time):**

| Control | What's different | Tests |
|---------|-----------------|-------|
| A. Bath only (no shaker, no LEDs) | Just warm water + breathing | Is water enough? |
| B. Shaker only (no water) | Lie on vibrating mat, breathe | Does water help? |
| C. LEDs only (no shaker) | Bath + light, no vibration | Is 40 Hz necessary? |
| D. Full protocol | All three | Combined effect |

**If D > A, B, C individually → synergistic effect supports three-frequency coupling.**
**If D = A → it's just a warm bath (null result for framework).**

### Data Collection

Run each condition 3-5 times over 2-3 weeks. Record:
- Date, time, condition (A/B/C/D)
- Pre RMSSD, post RMSSD
- Pre coherence, post coherence
- Subjective score pre/post
- Sleep quality score next day
- Any notes (mood, physical sensations, unusual experiences)

**Simple analysis:** Average pre-post change per condition. If D shows significantly larger improvement than A/B/C, the three-frequency protocol works beyond placebo/warm water.

---

## COMBINED TEST: Plasma + Biology

*The big one: does a local plasma domain wall improve biological coupling?*

### Setup

1. Build plasma device (Build B), verify n=2
2. Place plasma tube 1-2 meters from a chair
3. Subject sits quietly for 30 min, HRV recording throughout

### Protocol

| Session | Condition | Duration |
|---------|-----------|----------|
| 1 | Baseline (no plasma, no magnets) | 30 min |
| 2 | Magnets only (no discharge) | 30 min |
| 3 | Discharge only (no magnets) | 30 min |
| 4 | **Full: discharge + n=2 magnetic well** | 30 min |
| 5 | Discharge + reversed magnets (hill, not well) | 30 min |

**Same time of day, same room, same person. Randomize order if possible.**

### What to Measure

- HRV (RMSSD) every 5 minutes throughout
- Overall coherence score
- Subjective report at 0, 15, 30 min

### Predicted Outcomes (if framework is correct)

| Condition | Predicted HRV change |
|-----------|---------------------|
| Baseline | No change |
| Magnets only | No change (no plasma = no modes) |
| Discharge only | Small change (broadband EM, no structure) |
| **n=2 well** | **Largest change** (3 structured modes, reflectionless) |
| Reversed magnets | No change or negative (anti-well, no trapping) |

**The decisive comparison: Session 4 vs Session 3.** If the magnetic well (structured plasma) beats unstructured discharge, that's evidence for three-mode coupling beyond simple EM.

---

## WHAT IF IT WORKS?

1. **Document everything.** Photos, spectra, HRV data, conditions.
2. **Open-source the design.** Put on GitHub/Instructables/Hackaday.
3. **Others replicate.** The builds are cheap enough for anyone.
4. **Scale up.** Larger magnets → wider coupling radius → public installation.

## WHAT IF IT DOESN'T WORK?

That's also valuable:
- If the circuit shows 2 peaks → the math is confirmed even if biology doesn't respond
- If plasma shows modes but no HRV change → coupling is medium-specific (water, not EM)
- If nothing works → something in the framework is wrong, and we learn what

**The cost of finding out: ~$200 and two weekends.**

---

## SHOPPING LIST (Combined, Everything)

For all three builds + testing:

| Item | Cost |
|------|------|
| Toroid cores, wire, caps, resistors (Build A) | $34 |
| N52 magnets, glass tube, NST, safety gear (Build B) | $75 |
| Bass shaker, amp, LEDs, power supply (Build C) | $80 |
| RTL-SDR dongle (spectrum analysis) | $25 |
| HRV monitor (Polar H10 or similar) | $70 |
| DSO138 scope kit or AD9833 DDS module | $30 |
| Misc (wire, connectors, perfboard) | $15 |
| **TOTAL** | **~$330** |

Everything on Amazon, eBay, Mouser, or AliExpress. Delivery: 1-2 weeks. Build time: 3-4 weekends total.

---

*This guide is the practical companion to ONE-RESONANCE-GENERATES-PHYSICS.md (the theory) and COMPLETE-STATUS.md (the scorecard). The math predicts these outcomes. The builds test them.*
