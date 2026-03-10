#!/usr/bin/env python3
"""
framework_music.py — Music from the Framework's Mathematics
============================================================

The dark vacuum's language is PATTERNS, not photons (α = 0).
Music IS patterns. So: what does the framework sound like?

DISCOVERIES:
1. A4 = 440 Hz = f₂ × L(5) = 40 Hz × 11 EXACTLY
   Concert pitch = breathing mode × 5th Lucas number

2. The η tower gives a natural melody: rises, peaks at n=7 = L(4), descends

3. The golden scale: stacking φ as a generator gives a hexatonic scale

4. Lucas intervals: L(n+1)/L(n) → {3, 4/3, 7/4, 11/7, 18/11, 29/18}
   Converges to φ. The first ratio 4/3 is the PERFECT FOURTH.

5. The η tower peak at n=7: η(q⁷) = 0.838
   η(q⁸) ≈ 5/6 = 0.8333 (99.99%!!)
   8 = rank(E₈), 5/6 = 1 - 1/|S₃|

Generates: framework_melody.wav — the sound of the eta tower

Usage:
    python theory-tools/framework_music.py
"""

import math
import struct
import wave
import sys
import os

if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

phi = (1 + math.sqrt(5)) / 2
phibar = 1 / phi
sqrt5 = math.sqrt(5)
pi = math.pi

L = lambda n: round(phi**n + (-phibar)**n)

# Modular forms
N_terms = 2000
def compute_eta(q_val, N=N_terms):
    if q_val < 1e-15:
        return 1.0
    e = q_val**(1/24)
    for n in range(1, N):
        e *= (1 - q_val**n)
    return e

# Eta tower
eta_tower = {}
for k in range(1, 16):
    eta_tower[k] = compute_eta(phibar**k)

# θ₄ tower
theta4_tower = {}
for k in range(1, 8):
    theta4_tower[k] = eta_tower[k]**2 / eta_tower[2*k]

print("=" * 78)
print("MUSIC FROM THE FRAMEWORK'S MATHEMATICS")
print("=" * 78)

# ================================================================
# SECTION 1: A4 = 440 Hz = f₂ × L(5)
# ================================================================
print(f"\n{'='*78}")
print("[1] CONCERT PITCH FROM THE FRAMEWORK")
print("=" * 78)

f2 = 40  # Hz, neural breathing mode
A4_framework = f2 * L(5)  # 40 × 11 = 440

print(f"""
    f₂ = 40 Hz     (neural breathing mode, gamma oscillation)
    L(5) = 11       (5th Lucas number)

    A4 = f₂ × L(5) = 40 × 11 = {A4_framework} Hz    EXACTLY 440 Hz!

    Concert pitch IS the breathing mode times the 5th Lucas number.
    International standard (ISO 16) chose 440 Hz in 1955.
    The framework says this frequency connects neural maintenance (40 Hz)
    to the Lucas bridge at the 5th level.

    Other tunings:
    A4 = 432 Hz (Verdi): 432/40 = 10.8 (not a clean ratio)
    A4 = 444 Hz (some):  444/40 = 11.1 ≈ L(5) + 0.1
    A4 = 440 Hz:         440/40 = 11   = L(5) EXACTLY

    The standard tuning wins in the framework.
""")

# Also: 40 Hz × φ⁵ = 40 × 11.090 = 443.6 Hz ≈ 444 Hz
print(f"    Also: f₂ × φ⁵ = 40 × {phi**5:.3f} = {40*phi**5:.1f} Hz ≈ 444 Hz")
print(f"    φ⁵ ≈ L(5) = 11 to {min(phi**5, 11)/max(phi**5, 11)*100:.2f}%")
print(f"    (Lucas numbers approximate φ powers: L(n) ≈ φⁿ for large n)")

# ================================================================
# SECTION 2: THE ETA TOWER — Peak at n=7
# ================================================================
print(f"\n{'='*78}")
print("[2] THE ETA TOWER: Peak at n = 7 = L(4)")
print("=" * 78)

print(f"\n    The eta tower η(q^n) at q = 1/φ:")
print(f"    {'n':>4} {'η(q^n)':>12} {'Note':>35}")

peak_n = max(range(1, 15), key=lambda k: eta_tower[k])
for k in range(1, 15):
    note = ""
    if k == peak_n:
        note = "← PEAK (n = 7 = L(4))"
    elif k == 8:
        note = f"← 5/6 = {5/6:.6f} ({min(eta_tower[8], 5/6)/max(eta_tower[8], 5/6)*100:.4f}%)"
    elif k == 1:
        note = "← α_s (visible coupling)"
    elif k == 2:
        note = "← dark coupling"
    print(f"    {k:>4} {eta_tower[k]:12.8f} {note:>35}")

print(f"""
    OBSERVATIONS:

    1. The tower PEAKS at n = 7 = L(4)
       η(q⁷) = {eta_tower[7]:.8f}
       Then DESCENDS — the eta function doesn't monotonically increase!

    2. η(q⁸) ≈ 5/6 = 0.833333...
       Actual: {eta_tower[8]:.8f} → {min(eta_tower[8], 5/6)/max(eta_tower[8], 5/6)*100:.4f}% match
       8 = rank(E₈). 5/6 = 1 - 1/|S₃|.
       At the rank of E₈, the eta value = 1 minus the inverse of the
       generation symmetry order!

    3. The rise-and-fall shape is like a BREATH:
       Inhale (n=1→7): coupling strengthens as you go deeper
       Exhale (n=7→∞): coupling weakens as you approach the trivial vacuum (q=0)

       The eta tower IS a breathing pattern.
       The peak at L(4) = 7 is the moment of maximum fullness.
""")

# ================================================================
# SECTION 3: FRAMEWORK MUSICAL SCALES
# ================================================================
print(f"{'='*78}")
print("[3] FRAMEWORK MUSICAL SCALES")
print("=" * 78)

# Scale 1: Lucas intervals
print(f"\n    SCALE A: LUCAS INTERVALS")
print(f"    Lucas number ratios L(n+1)/L(n) as musical intervals:")
print(f"    {'n':>4} {'L(n)':>6} {'L(n+1)/L(n)':>12} {'Cents':>8} {'Nearest interval':>25}")

just_intervals = [
    (1.000, "Unison"), (1.059, "Semitone (ET)"), (1.122, "Major 2nd (9/8)"),
    (1.189, "Minor 3rd (6/5)"), (1.250, "Major 3rd (5/4)"), (1.333, "Perfect 4th (4/3)"),
    (1.414, "Tritone (√2)"), (1.500, "Perfect 5th (3/2)"), (1.587, "Minor 6th (8/5)"),
    (1.667, "Major 6th (5/3)"), (1.750, "Harm. 7th (7/4)"), (1.875, "Major 7th (15/8)"),
]

for n in range(1, 8):
    ratio = L(n+1) / L(n)
    cents = 1200 * math.log2(ratio) if ratio > 0 else 0
    nearest = min(just_intervals, key=lambda x: abs(x[0] - ratio))
    print(f"    {n:>4} {L(n):>6} {ratio:12.4f} {cents:8.1f} {nearest[1]:>25}")

print(f"""
    The Lucas ratios CONVERGE to φ = {phi:.6f} ({1200*math.log2(phi):.1f} cents).
    Early ratios give: perfect fourth (4/3), harmonic seventh (7/4).
    These ARE the framework's fundamental musical intervals.
""")

# Scale 2: Golden chain
print(f"    SCALE B: GOLDEN CHAIN (φ as generator)")
print(f"    Stack intervals of φ, reduce to within one octave:")

golden_scale = []
for n in range(7):
    ratio = phi**n
    # Reduce to [1, 2)
    while ratio >= 2:
        ratio /= 2
    cents = 1200 * math.log2(ratio)
    golden_scale.append((cents, n, ratio))

golden_scale.sort()
print(f"    {'Step':>6} {'φ^n':>4} {'Ratio':>8} {'Cents':>8} {'Hz (A=440)':>12}")
for i, (cents, n, ratio) in enumerate(golden_scale):
    hz = 440 * ratio
    print(f"    {i:>6} φ^{n:<2} {ratio:8.4f} {cents:8.1f} {hz:12.1f}")

print(f"""
    This is a HEXATONIC (6-note) scale.
    No perfect fifths, no perfect fourths — alien to Western music.
    But it has a deep self-similar structure: each interval
    contains the golden ratio relationship.
""")

# Scale 3: Eta tower scale
print(f"    SCALE C: ETA TOWER MELODY SCALE")
print(f"    Map η(q^n) directly to frequencies:")
base_freq = 220  # A3
oct_range = 2    # two octaves

print(f"    Base: {base_freq} Hz (A3), range: {oct_range} octaves")
print(f"    {'n':>4} {'η(q^n)':>10} {'Hz':>10} {'MIDI note':>10} {'Note name':>12}")

note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

melody_freqs = []
eta_min = min(eta_tower[k] for k in range(1, 13))
eta_max = max(eta_tower[k] for k in range(1, 13))

for k in range(1, 13):
    # Map η to frequency: linear in log space
    frac = (eta_tower[k] - eta_min) / (eta_max - eta_min)
    freq = base_freq * 2**(oct_range * frac)
    midi = 69 + 12 * math.log2(freq / 440)
    note_idx = round(midi) % 12
    octave = round(midi) // 12 - 1
    melody_freqs.append(freq)
    print(f"    {k:>4} {eta_tower[k]:10.6f} {freq:10.1f} {midi:10.1f} {note_names[note_idx]}{octave}")

# ================================================================
# SECTION 4: DARK VACUUM INTERVALS
# ================================================================
print(f"\n{'='*78}")
print("[4] DARK VACUUM INTERVALS — The Unheard Music")
print("=" * 78)

# The dark vacuum's intervals come from η(q²)-related ratios
# Dark/visible coupling ratio = η(q²)/η(q) = 3.906
# This is 2 octaves + ... (2² = 4, so 3.906 is just under 2 octaves)

dark_ratio = eta_tower[2] / eta_tower[1]
dark_cents = 1200 * math.log2(dark_ratio)

print(f"""
    The dark/visible coupling ratio:
    η(q²)/η(q) = {dark_ratio:.4f} = {dark_cents:.1f} cents ≈ 2 octaves ({2*1200} cents)

    The dark vacuum is almost EXACTLY 2 octaves above the visible.
    Difference from 2 octaves: {dark_cents - 2400:.1f} cents ({dark_cents/2400*100:.2f}%)

    In music, 2 octaves up = the SECOND HARMONIC OVERTONE.
    The dark vacuum is the second overtone of the visible.

    Or equivalently: the visible is the fundamental,
    and the dark vacuum resonates at twice its octave.

    THE WALL'S INTERVALS (boundary quantities):
    √(η·η_dark) = {math.sqrt(eta_tower[1]*eta_tower[2]):.6f} (geometric mean)
    This mapped to frequency = between the two.
    Ratio to visible: {math.sqrt(eta_tower[2]/eta_tower[1]):.4f} = {1200*math.log2(math.sqrt(eta_tower[2]/eta_tower[1])):.0f} cents
    → Almost exactly 1 octave! The wall IS the octave between light and dark.
""")

# Key intervals from the theta4 tower
print(f"    θ₄ TOWER AS MELODY:")
for k in range(1, 7):
    val = theta4_tower[k]
    if k > 1:
        interval = theta4_tower[k] / theta4_tower[k-1]
        cents = 1200 * math.log2(interval)
        print(f"    θ₄(q^{k}) = {val:.6f}  interval from prev: {interval:.4f} = {cents:.0f} cents")
    else:
        print(f"    θ₄(q^{k}) = {val:.6f}  (base)")

# ================================================================
# SECTION 5: GENERATE WAV — The Eta Tower Melody
# ================================================================
print(f"\n{'='*78}")
print("[5] GENERATING AUDIO: The Eta Tower Melody")
print("=" * 78)

# Generate a simple WAV file
wav_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "eta_tower_melody.wav")
sample_rate = 44100
duration_per_note = 0.6  # seconds
fade_time = 0.05  # seconds for attack/release

samples = []

# Part 1: The eta tower ascending and descending (12 notes)
print(f"\n    Part 1: Eta tower melody (12 notes, rise → peak → fall)")
for k in range(1, 13):
    freq = melody_freqs[k-1]
    n_samples = int(sample_rate * duration_per_note)
    for i in range(n_samples):
        t = i / sample_rate
        # Envelope: smooth attack and release
        env = min(1.0, t / fade_time, (duration_per_note - t) / fade_time)
        # Main tone + soft octave
        val = 0.6 * math.sin(2 * pi * freq * t)
        val += 0.2 * math.sin(2 * pi * freq * 2 * t)  # octave
        val += 0.1 * math.sin(2 * pi * freq * phi * t)  # golden interval
        samples.append(int(32767 * env * val * 0.7))

# Short pause
pause_samples = int(sample_rate * 0.3)
samples.extend([0] * pause_samples)

# Part 2: The framework chord — visible + dark + wall simultaneously
print(f"    Part 2: Framework chord (visible + dark + wall)")
chord_dur = 3.0  # seconds
vis_freq = 220  # A3 = visible
dark_freq = 220 * dark_ratio / 4  # bring down to same octave range
wall_freq = 220 * math.sqrt(dark_ratio) / 2  # geometric mean

n_samples = int(sample_rate * chord_dur)
for i in range(n_samples):
    t = i / sample_rate
    env = min(1.0, t / 0.1, (chord_dur - t) / 0.5)
    val = 0.3 * math.sin(2 * pi * vis_freq * t)       # visible (fundamental)
    val += 0.3 * math.sin(2 * pi * wall_freq * t)      # wall (octave)
    val += 0.3 * math.sin(2 * pi * dark_freq * t)      # dark (2nd overtone)
    samples.append(int(32767 * env * val * 0.7))

# Short pause
samples.extend([0] * pause_samples)

# Part 3: The breathing mode pulse — 40 Hz modulating the framework chord
print(f"    Part 3: Breathing mode (40 Hz) modulating the chord")
breath_dur = 4.0
n_samples = int(sample_rate * breath_dur)
for i in range(n_samples):
    t = i / sample_rate
    env = min(1.0, t / 0.2, (breath_dur - t) / 0.5)
    # 40 Hz breathing modulation
    breath = 0.5 + 0.5 * math.sin(2 * pi * 40 * t)
    # The chord
    val = 0.3 * math.sin(2 * pi * 261.6 * t)  # C4
    val += 0.3 * math.sin(2 * pi * 261.6 * phi * t)  # golden interval above C
    val += 0.2 * math.sin(2 * pi * 261.6 * 3/2 * t)  # perfect fifth
    samples.append(int(32767 * env * breath * val * 0.7))

# Write WAV
try:
    with wave.open(wav_path, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        for s in samples:
            s = max(-32767, min(32767, s))
            wf.writeframes(struct.pack('<h', s))
    total_dur = len(samples) / sample_rate
    print(f"\n    Written: {wav_path}")
    print(f"    Duration: {total_dur:.1f} seconds")
    print(f"    Parts: eta melody → framework chord → breathing modulation")
except Exception as e:
    print(f"\n    Could not write WAV: {e}")
    wav_path = None

# ================================================================
# SECTION 6: THE THREE LANGUAGES
# ================================================================
print(f"\n{'='*78}")
print("[6] THE THREE LANGUAGES")
print("=" * 78)

print(f"""
    LIGHT VACUUM LANGUAGE: NUMBERS
    → Scientific notation, measurements, ratios
    → Exact but cold. Can describe the dark, cannot BE the dark.
    → Tool: mathematics, equations, proofs

    DARK VACUUM LANGUAGE: PATTERNS
    → Music, rhythm, resonance, felt-sense
    → Rich but imprecise. Cannot be measured, only experienced.
    → Tool: song, chant, rhythm, silence

    BOUNDARY LANGUAGE: TRANSLATION
    → Metaphor, poetry, sacred geometry, ritual
    → Bridges precise and felt. Maps between domains.
    → Tool: art, prayer, meditation, dreaming

    The framework itself is a BOUNDARY LANGUAGE:
    it uses light-vacuum tools (math) to describe dark-vacuum content (patterns).
    The modular forms ARE the Rosetta Stone between the two vacua.

    ═══════════════════════════════════════════════════════════════
    KEY MUSICAL DISCOVERIES:

    1. A4 = 440 Hz = 40 × L(5)
       Concert pitch = breathing mode × 5th Lucas number

    2. Dark/visible = {dark_ratio:.3f} ≈ 2 octaves (the 2nd overtone)
       The dark vacuum sounds two octaves above the visible

    3. The wall = geometric mean = 1 octave above visible
       The boundary IS the octave

    4. The eta tower melody rises to n=7 then descends
       Like a BREATH. Peak at L(4) = 7.

    5. η(q⁸) = 5/6 (99.99%)
       At E₈ rank: eta = 1 - 1/|S₃|

    6. The golden chain gives a hexatonic scale
       Self-similar at every level, no Western consonances

    7. Lucas ratios give: perfect fourth (4/3), harmonic seventh (7/4)
       These ARE the framework's native consonances
    ═══════════════════════════════════════════════════════════════
""")

print("=" * 78)
print("END: MUSIC FROM THE FRAMEWORK")
print("=" * 78)
