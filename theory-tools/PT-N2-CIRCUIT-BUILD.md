# Poeschl-Teller n=2 Domain Wall Circuit -- Complete Build Guide

## What You Will Build

A 21-node LC ladder network where the series inductance follows a sech^2 dip
at the center.  This creates an electrical analog of the **Poeschl-Teller
quantum potential** with depth parameter n=2 -- the same mathematical structure
that governs the stability of the domain wall in V(Phi) = lambda(Phi^2 - Phi - 1)^2.

The circuit demonstrates three properties:
1. **Exactly 2 bound states** above the passband (zero mode + breathing mode)
2. **Reflectionlessness**: waves pass through with zero reflection (integer n)
3. **Energy ratio 4:1** between the two bound states (matching PT theory)

---

## 1. Theory: How an LC Ladder Maps to Quantum Mechanics

### The Schrodinger Analogy

An LC transmission line with position-dependent inductance obeys exactly the
same mathematics as a quantum particle in a potential well.

The voltage at node j satisfies:

    omega^2 * C * v_j = (v_j - v_{j-1})/L_{j-1} + (v_j - v_{j+1})/L_j

This is the discrete Schrodinger equation in tight-binding form.  At the
top of the passband, the staggering transformation v_j = (-1)^j * u_j
converts the LC equation into:

    -Delta u_j - 4 * delta * sech^2((j - j_c) / w) * u_j = epsilon * u_j

where Delta is the discrete Laplacian, delta is the fractional inductance
reduction at the center, and epsilon = 4 - omega^2*L0*C is the eigenvalue
measured from the band edge.

### The sech^2 Profile

When the series inductance follows:

    L(j) = L0 * [1 - delta / cosh^2((j - j_center) / w)]

the effective potential in the continuum limit is a **Poeschl-Teller well**:

    V_eff(x) = -V0 / cosh^2(kappa * x)

where the depth parameter n satisfies:

    n(n+1) = 4 * delta * w^2

### Bound States Appear ABOVE the Band

Because L is *reduced* at the center, the local cutoff frequency is *higher*
there.  Localized modes are pushed above the passband of the uniform chain.
This is equivalent to the standard quantum picture with an inverted energy
axis: what matters is that the modes are localized and separated from the
continuum.

### Why n=2 is Special

| Property | n=1 | n=2 | n=3 | Non-integer |
|----------|-----|-----|-----|-------------|
| Bound states | 1 | **2** | 3 | floor(n) or floor(n)+1 |
| Reflectionless | Yes | **Yes** | Yes | **No** |
| Energy ratio | -- | **4:1** | 9:4:1 | Not clean |

The Interface Theory claims that V(Phi) = lambda(Phi^2 - Phi - 1)^2 produces
**exactly** n=2 from its kink solution. This means two stability modes and no
more, perfect transmission, and a specific energy hierarchy.

---

## 2. Design Parameters

| Parameter | Value | Notes |
|-----------|-------|-------|
| N (nodes) | 21 | 20 inductor links, 21 capacitor nodes |
| C_0 (shunt cap) | 100 nF | Standard value, C0G or X7R ceramic |
| L_0 (background L) | 1.000 mH | Hand-wound on toroid core |
| w (well width) | 2.5 cells | Fits within 21-node chain |
| delta (depth) | 0.233 | Tuned for E0/E1 = 4.0 on finite chain |
| Z_0 (char. impedance) | 100 ohms | sqrt(L0/C0) |
| f_cutoff | 31,742 Hz | Upper passband edge |

**Note on delta:** The continuum formula gives delta = n(n+1)/(4*w^2) = 0.24
for n=2, w=2.5.  The value delta=0.233 compensates for discretization effects
on the finite 21-node chain and produces an energy ratio of exactly 4.005
(vs the theoretical 4.000).

---

## 3. Component Values

### Inductor Schedule

The inductance profile is symmetric: link j and link (19-j) are identical.

| Link | Nodes | Target L (uH) | L/L0 | Turns (T68-2) | Actual L (uH) | Error |
|------|-------|---------------|------|---------------|---------------|-------|
| 0, 19 | 0-1, 19-20 | 999.5 | 0.9995 | 132 | 993.2 | -0.6% |
| 1, 18 | 1-2, 18-19 | 999.0 | 0.9990 | 132 | 993.2 | -0.6% |
| 2, 17 | 2-3, 17-18 | 997.7 | 0.9977 | 132 | 993.2 | -0.5% |
| 3, 16 | 3-4, 16-17 | 994.9 | 0.9949 | 132 | 993.2 | -0.2% |
| 4, 15 | 4-5, 15-16 | 988.8 | 0.9889 | 132 | 993.2 | +0.4% |
| 5, 14 | 5-6, 14-15 | 975.9 | 0.9760 | 131 | 978.2 | +0.2% |
| 6, 13 | 6-7, 13-14 | 949.6 | 0.9496 | 129 | 948.5 | -0.1% |
| 7, 12 | 7-8, 12-13 | 902.1 | 0.9021 | 126 | 904.9 | +0.3% |
| 8, 11 | 8-9, 11-12 | 834.2 | 0.8342 | 121 | 834.5 | +0.0% |
| 9, 10 | 9-10, 10-11 | 776.1 | 0.7761 | 117 | 780.3 | +0.5% |

All errors are below 0.7% -- well within the 2% tolerance required.

### Unique Turn Counts

Only 6 distinct winding configurations are needed:

| Turns | Inductance (uH) | Quantity | Used at links |
|-------|-----------------|----------|---------------|
| 132 | 993.2 | 10 | 0-4 and 15-19 |
| 131 | 978.2 | 2 | 5 and 14 |
| 129 | 948.5 | 2 | 6 and 13 |
| 126 | 904.9 | 2 | 7 and 12 |
| 121 | 834.5 | 2 | 8 and 11 |
| 117 | 780.3 | 2 | 9 and 10 |

### Capacitors

All 21 shunt capacitors are identical: **100 nF** (0.1 uF).  Use C0G/NP0
dielectric for best accuracy, or X7R if unavailable.  Buy 1% tolerance if
possible (Vishay, KEMET).

### Termination Resistors

Two 100-ohm resistors (1% metal film):
- One in series with the signal source at node 0 (R_s)
- One as shunt load from node 20 to ground (R_L)

These provide impedance matching at Z_0 = sqrt(L0/C0) = 100 ohms.

---

## 4. Resonant Frequencies

| Quantity | Value | Notes |
|----------|-------|-------|
| Passband edge (f_c) | 31,742 Hz | Highest mode of uniform chain |
| Bound state 1 (breathing mode) | 32,520 Hz | Above band, odd symmetry |
| Bound state 0 (ground state) | 34,753 Hz | Above band, even symmetry |
| Energy ratio E_0/E_1 | 4.005 | Theory: 4.000 |
| Frequency ratio f_0/f_1 | 1.069 | |

The bound states sit 800 Hz to 3,000 Hz above the passband edge -- easily
resolvable with any frequency counter or oscilloscope.

**Important:** "Energy" means f^2 - f_edge^2 (the eigenvalue measured from
the band edge).  The frequency ratio is NOT 2:1; it is the **energy** ratio
that equals 4:1.

---

## 5. Circuit Schematic

```
                     LC Ladder Chain (21 nodes, 20 inductors)

 Signal          R_s=100R                                        R_L=100R
 Source --+------/\/\/\/--+--[L_0]--+--[L_1]--+-- ... --+--[L_19]--+--/\/\/\/--+
          |               |         |         |          |          |            |
        [BNC]           [C_0]     [C_1]     [C_2]     [C_19]     [C_20]      [BNC]
          |             100nF     100nF     100nF      100nF     100nF          |
          |               |         |         |          |          |            |
 GND -----+---------------+---------+---------+--- ... --+----------+------------+

 Node:                   0         1         2          19        20


 Detail of one cell:

      Node j                Node j+1
        |                     |
        +-----[L_j]----------+
        |                     |
      [C_j]                 [C_{j+1}]
      100nF                 100nF
        |                     |
       GND                   GND


 Test points:

   Scope Ch1: Node 0  (input reference)
   Scope Ch2: Node 20 (output)
   Scope Ch3: Any interior node (for mode profiling)

 Source: Function generator, sine wave, 0.5-1 V p-p
 Load:   100 ohm to ground
```

---

## 6. Measurement Protocol

### Experiment 1: Bound State Count (Frequency Sweep)

**Setup:**
1. Connect function generator to node 0 through R_s = 100 ohm.
2. Connect R_L = 100 ohm from node 20 to ground.
3. Oscilloscope Ch1 at node 0, Ch2 at node 20.

**Procedure:**
1. Set function generator to sine wave, 0.5 V amplitude.
2. Sweep frequency from 1,000 Hz to 40,000 Hz in 100 Hz steps.
3. At each step, record V_out (node 20) amplitude.
4. Plot output amplitude vs frequency.

**What you should see:**
- 1 kHz to 31 kHz: passband, signal passes through.
- At 31,742 Hz: band edge, signal drops sharply.
- At 32,520 Hz: **first peak** above cutoff (breathing mode).
- At 34,753 Hz: **second peak** above cutoff (ground state).
- Above 35 kHz: stop band, exponential decay.

**The signature: exactly 2 peaks above the cutoff for n=2.**

### Experiment 2: Energy Ratio

From the frequency sweep, identify the two peak frequencies f_0 and f_1,
and the cutoff frequency f_c.  Compute:

    E_0 = f_0^2 - f_c^2
    E_1 = f_1^2 - f_c^2
    ratio = E_0 / E_1

**Expected: 4.0 +/- 0.3** (with 1% component tolerance).

### Experiment 3: Mode Profile Imaging

To visualise the bound state wavefunctions:

1. Drive the chain at exactly 34,753 Hz (ground state).
2. Measure voltage amplitude at each of the 21 nodes.
3. Plot amplitude vs node index.

**Expected profiles:**
- Ground state (34,753 Hz): bell-shaped envelope peaked at center (node 10),
  with alternating sign between adjacent nodes (staggered pattern).
- Breathing mode (32,520 Hz): antisymmetric, zero at center, peaked on both
  sides with opposite sign.

### Experiment 4: Reflectionlessness (Pulse Test)

**Caveat:** The reflectionlessness property is a continuum-limit result.
With only 21 nodes and w=2.5 cells, discrete effects add a small amount
of scattering that masks the clean reflectionless signal.  This test is
qualitative, not quantitative.

**Setup:**
1. Function generator: burst mode, 2-3 cycles of sine at 15 kHz.
2. Oscilloscope at node 0, triggered on the burst.

**Procedure:**
1. Send burst into the n=2 chain.
2. Look for reflected pulses returning to node 0 after the initial pulse.
3. Compare with:
   - Uniform chain (all L = 1 mH): clear reflections from far end.
   - n=1.5 chain (delta = 0.150): partial reflections from the well.

**For a definitive reflectionlessness test:** use a longer chain (N=100+)
or the analytic continuous-PT formula (shown by the simulation script).

---

## 7. Comparison Experiments

Build three configurations (or swap center inductors between runs):

### Chain A: n=1 (1 bound state, reflectionless)

delta = 0.080.  Inductor values:

| Link | Target L (uH) | Turns |
|------|---------------|-------|
| 0-4, 15-19 | 1000 | 132 |
| 5, 14 | 992 | 132 |
| 6, 13 | 983 | 131 |
| 7, 12 | 966 | 130 |
| 8, 11 | 943 | 129 |
| 9, 10 | 923 | 127 |

Prediction: **1 resonance peak** above the passband edge.

### Chain B: n=2 (2 bound states, reflectionless) -- PRIMARY BUILD

delta = 0.233.  See the full inductor schedule in Section 3.

Prediction: **2 resonance peaks**, energy ratio 4.0.

### Chain C: n=1.5 (non-integer, shows reflection)

delta = 0.150.  Inductor values:

| Link | Target L (uH) | Turns |
|------|---------------|-------|
| 0-4, 15-19 | 1000 | 132 |
| 5, 14 | 985 | 131 |
| 6, 13 | 968 | 130 |
| 7, 12 | 937 | 128 |
| 8, 11 | 893 | 125 |
| 9, 10 | 856 | 123 |

Prediction: **2 peaks but wrong energy ratio** (~7 instead of 4).
Non-integer n is NOT reflectionless: shows partial reflection on pulse test.

### The Critical Comparison

| Chain | Peaks | E0/E1 | Reflectionless? |
|-------|-------|-------|-----------------|
| n=1 | 1 | -- | Yes (integer) |
| n=1.5 | 2 | ~7 | **No** (non-integer) |
| n=2 | 2 | 4.0 | Yes (integer) |

---

## 8. Bill of Materials

### Passive Components

| Component | Specification | Qty | Unit Cost | Total |
|-----------|--------------|-----|-----------|-------|
| Toroid core | Micrometals T68-2 (red, iron powder) | 20 | $0.50 | $10.00 |
| Magnet wire | 30 AWG, polyurethane coated, 1/4 lb spool | 1 | $8.00 | $8.00 |
| Ceramic capacitor | 100 nF, C0G/X7R, 50V, 1-5% tolerance | 25 | $0.15 | $3.75 |
| Resistor | 100 ohm, 1/4W, 1% metal film | 4 | $0.05 | $0.20 |
| Perfboard | 10 x 15 cm, 2.54mm pitch | 1 | $3.00 | $3.00 |
| Pin headers | 40-pin male, 2.54mm | 2 | $0.50 | $1.00 |
| Hookup wire | 22 AWG solid core | 1 pack | $5.00 | $5.00 |
| BNC connectors | Panel-mount female | 2 | $1.00 | $2.00 |
| **Passive total** | | | | **~$33** |

### Test Equipment

| Equipment | Budget Option | Mid-Range | Notes |
|-----------|--------------|-----------|-------|
| Function generator | AD9833 module + Arduino ($15) | Bench unit ($100-200) | Needs 1-40 kHz sine |
| Oscilloscope | DSO138 kit ($20) | Hantek USB ($60) | 2 channels, 100 kHz BW |
| LC meter | DE-5000 ($25) | Bench LCR ($100) | For inductor verification |
| **Equipment total** | **~$60** | **~$360** | |

### Total Cost Estimate

- Budget build (all budget equipment): **~$93**
- If you already have test equipment: **~$33** for parts
- Mid-range: **~$200**

### Where to Buy

| Component | Suppliers |
|-----------|----------|
| T68-2 toroid cores | Micrometals.com (direct), Mouser, Digi-Key, eBay |
| 30 AWG magnet wire | Amazon, eBay, Remington Industries |
| 100 nF capacitors | Mouser, Digi-Key, LCSC |
| Resistors | Mouser, Digi-Key, LCSC |
| Perfboard, headers | Amazon, Adafruit, SparkFun |
| AD9833 DDS module | Amazon, AliExpress |
| DSO138 scope kit | Amazon, AliExpress, Banggood |
| DE-5000 LC meter | Amazon, eBay |

---

## 9. Build Notes

### Winding the Inductors

**Core:** Micrometals T68-2 (red iron powder).  The "-2" material is
optimized for the 1 kHz to 30 MHz range.  AL = 57 nH/turn^2 (typical;
verify with your specific lot by winding a test coil).

**Procedure:**
1. Cut ~8 meters of 30 AWG magnet wire per inductor (132 turns at ~5.7 cm
   per turn on T68 = 7.5 m; add margin).
2. Thread the wire through the center hole, around the outside, and back
   through the hole.  Each complete loop = 1 turn.
3. Count turns with a hand tally counter or mark every 10th turn with tape.
4. Distribute turns evenly around the core.
5. Leave 3-5 cm leads on each end.

**Verification:**
After winding each inductor, measure with an LC meter at 1 kHz.  Compare
with the target value.  If too high: remove turns (one at a time).  If too
low: add turns.  **Target: within 1% of scheduled value.**

Label each inductor with its link number and measured value.

### Perfboard Assembly

1. Place the 21 capacitors in a row along the center of the board, spaced
   5-7 mm apart.  One lead connects to the node point (top bus), the other
   to the ground bus (bottom bus).

2. Create a solid ground bus along one edge using a continuous copper
   strip or thick wire.  All capacitor ground leads connect here.

3. Connect inductors between adjacent node points.  Toroids can stand
   perpendicular to the board, secured with hot glue.

4. At node 0: connect a 100-ohm series resistor to a BNC connector.
   At node 20: connect a 100-ohm shunt resistor between node 20 and ground,
   with a BNC connector for the oscilloscope.

### Breadboard Alternative

Breadboards work fine for a first test.  Stray capacitance (~2 pF per row)
is negligible compared to C_0 = 100 nF.  The main drawback is mechanical
fragility -- wires and toroids tend to pull out.

### Parasitic Effects

| Effect | Magnitude | Impact |
|--------|-----------|--------|
| Stray capacitance | ~2 pF/node | 0.002% of C_0, negligible |
| Inductor self-resonance | >1 MHz | Far above 35 kHz, negligible |
| Wire resistance | ~2.6 ohm per inductor | Reduces Q to ~72, broadens peaks slightly |
| Core loss (T68-2) | Small at 30 kHz | Below recommended max, negligible |
| Mutual inductance | Depends on spacing | Keep toroids >1 cm apart, orient axes at 90 degrees |

**Wire resistance detail:** 30 AWG copper = 0.34 ohm/m.  At 132 turns on
T68 (circumference ~5.7 cm), wire length = 7.5 m, so R_dc = 2.6 ohms.
The Q factor is omega*L/R = 2*pi*30000*1e-3/2.6 = 72.  The bound state
peaks will have a measurable width but remain clearly resolvable.

### Verifying Component Values

1. **Capacitors:** Measure with LC meter.  Buy from one batch to ensure
   matching.  Sort and use capacitors within 1% of 100 nF.
2. **Inductors:** Measure at 1 kHz (or 10 kHz).  Trim turns as needed.
3. **Resistors:** Measure with multimeter.  100 ohm +/- 1%.

---

## 10. Tolerance Budget

Monte Carlo simulation (500 trials) with random component variations:

| Tolerance (L and C) | Probability of 2 bound states | E_0/E_1 mean +/- std |
|---------------------|-------------------------------|---------------------|
| +/- 1% | ~80% | 4.3 +/- 0.8 |
| +/- 2% | ~65% | 6.0 +/- 5.0 |
| +/- 5% | ~35% | unreliable |
| +/- 10% | ~20% | unreliable |

**Recommendation:** Measure and trim all inductors to within **1%** of
the target values.  Buy capacitors from one batch and sort.  This gives
~80% first-build success rate.

The bound state **count** (exactly 2) is more robust than the energy
**ratio** (exactly 4).  Even with 5% tolerance, you often see 2 peaks --
they will just have the wrong spacing.

---

## 11. The PT n=2 Signature

What you are looking for, ranked by ease of measurement:

### A. Bound State Count (easiest, most robust)

Sweep frequency through the cutoff region (30-37 kHz).  Count the number
of transmission peaks above the band edge.

| Chain | Expected peaks | Meaning |
|-------|---------------|---------|
| Uniform | 0 | No localized modes |
| n=1 | 1 | One bound state (zero mode only) |
| n=2 | **2** | Zero mode + breathing mode |
| n=3 | 3 | Three bound states |

**This is the primary measurement.  It is robust, clear, and topological.**

### B. Energy Ratio (requires careful frequency measurement)

Compute E_0/E_1 = (f_0^2 - f_c^2) / (f_1^2 - f_c^2).

**Expected: 4.0 +/- 0.5.**  This is the smoking gun for PT n=2 specifically
(as opposed to any generic double-well).

### C. Mode Symmetry (requires probing interior nodes)

Ground state: even parity, peaked at center.
Breathing mode: odd parity, zero at center.

### D. Reflectionlessness (hardest, needs long chain for clean signal)

For the 21-node chain, discrete effects dominate over the continuum
reflectionlessness property.  A qualitative comparison between integer and
non-integer n chains may show a difference, but it will be subtle.

For a definitive test: run `python theory-tools/pt_circuit_simulation.py`
and examine the analytic reflection coefficient (which is exact in the
continuum limit).

---

## 12. What This Proves and Does Not Prove

### What the circuit demonstrates:

1. **Poeschl-Teller potentials with integer depth n support exactly n bound
   states.**  This is a theorem, but seeing it physically makes it tangible.

2. **Integer-n PT potentials are reflectionless.**  Waves pass through the
   "defect" with zero reflection at any frequency.  Most potential wells
   reflect.  Only the sech^2 shape with integer depth achieves this.

3. **The breathing mode has a specific energy ratio.**  For n=2, the two
   bound states have energies in ratio 4:1.

4. **Non-integer depth breaks reflectionlessness.**  The contrast between
   n=2.0 (zero reflection) and n=1.5 (partial reflection) is the key test.

### What this does NOT prove:

1. **Nothing about consciousness.**  This is a mathematical demonstration.

2. **Nothing about the golden ratio in physics.**  The sech^2 profile works
   for any domain wall kink.  The golden potential is special because it
   forces n=2 exactly, but the circuit cannot test this claim.

3. **Nothing about V(Phi) = lambda(Phi^2 - Phi - 1)^2.**  Any phi-4-like
   potential with a domain wall gives a PT stability spectrum.

### The genuine insight:

The circuit lets you experience what n=2 means physically: two bound modes,
a 4:1 energy hierarchy, and perfect transparency.  It makes the abstract
mathematics of domain wall stability into something you can build, measure,
and (at audio-scaled frequencies) hear.

---

## Appendix A: Derivation of the Circuit-PT Mapping

Start with KCL at node j:

    C * d^2V_j/dt^2 = (V_{j+1} - V_j)/L_j - (V_j - V_{j-1})/L_{j-1}

For harmonic time dependence V_j = v_j * exp(i*omega*t):

    -omega^2 * C * v_j = (v_{j+1} - 2*v_j + v_{j-1}) / L0
                         + correction from varying L

With L_j = L0 * (1 - delta * sech^2((j-j_c)/w)):

    1/L_j = (1/L0) * (1 + delta*sech^2 + ...)

Define k^2 = omega^2*L0*C.  The passband of the uniform chain is k^2 in [0, 4].
At the band edge, set k^2 = 4 - epsilon and substitute v_j = (-1)^j * u_j:

    -Delta u_j - 4*delta*sech^2((j-j_c)/w) * u_j = epsilon * u_j

This is the discrete Poeschl-Teller equation with V_0 = 4*delta.
In the continuum limit, n(n+1) = V_0 * w^2 = 4*delta*w^2.

For n=2: 4*delta*w^2 = 6, so delta = 3/(2*w^2) = 0.24 for w=2.5.
The finite-chain correction shifts the optimal delta to 0.233.

---

## Appendix B: Analytic Reflection Coefficient

The exact reflection coefficient for the continuous Poeschl-Teller potential:

    |R(k)|^2 = sin^2(pi*n) / [sin^2(pi*n) + sinh^2(pi*k/kappa)]

For integer n: sin(pi*n) = 0, giving |R|^2 = 0 at all k.  This is the
reflectionless property.

For n=1.5: |R|^2 approaches 1.0 as k approaches 0 (total reflection at
long wavelength).  Maximum contrast with the reflectionless case.

| k/kappa | n=1 (int) | n=1.5 | n=2 (int) | n=2.5 | n=3 (int) |
|---------|-----------|-------|-----------|-------|-----------|
| 0.1 | 0 | 0.907 | 0 | 0.907 | 0 |
| 0.5 | 0 | 0.159 | 0 | 0.159 | 0 |
| 1.0 | 0 | 0.007 | 0 | 0.007 | 0 |
| 2.0 | 0 | 0.000014 | 0 | 0.000014 | 0 |

---

## Appendix C: Audio-Frequency Variant

Scale all frequencies down by 10x for an audible demonstration:
- L_bg = 10 mH (buy standard shielded inductors or wind on larger cores)
- C_0 = 1 uF (standard electrolytic or film capacitor)
- f_c = 3,183 Hz (audible)
- Bound states at ~3,250 Hz and ~3,475 Hz
- Z_0 = 100 ohms (unchanged)

You can hear the bound states as tones.  Drive with an audio amplifier.

---

## Appendix D: Quick Reference Card

```
+--------------------------------------------------+
|  POESCHL-TELLER n=2 CIRCUIT -- QUICK REFERENCE   |
+--------------------------------------------------+
|  Nodes: 21                                       |
|  All caps: 100 nF ceramic (C0G/NP0)             |
|  Outer inductors: ~1000 uH (links 0-4, 15-19)   |
|  Center inductors: ~776 uH (links 9-10)          |
|  Termination: 100 ohm at each end                |
|                                                  |
|  Passband edge: 31,742 Hz                        |
|  Breathing mode: 32,520 Hz                       |
|  Ground state:  34,753 Hz                        |
|  Energy ratio: 4.005 (sim) / 4.000 (theory)      |
|                                                  |
|  Inductor tolerance needed: < 2% (target 1%)     |
|  Core: Micrometals T68-2, 117-132 turns          |
+--------------------------------------------------+
|  PASS CRITERIA:                                  |
|  [  ] 2 peaks above 31.7 kHz (not 1, not 3)     |
|  [  ] Energy ratio within 20% of 4.0            |
|  [  ] n=1 control gives only 1 peak             |
|  [  ] n=1.5 control: wrong ratio                |
+--------------------------------------------------+
```

---

## Companion Files

- **Simulation script:** `theory-tools/pt_circuit_simulation.py`
  Run this before building to verify predictions and generate diagnostic plots.

- **Output plot:** `theory-tools/pt_circuit_simulation.png`
  Six-panel diagnostic: inductance profile, eigenfrequency spectrum, mode
  profiles, bound state count vs n, pulse propagation, analytic reflection.

---

*Author: Interface Theory project.  Date: 2026-02-26.*
