#!/usr/bin/env python3
"""
wall_music.py -- Algorithmic Music Derived from Boundary Physics
================================================================

Every musical element is DERIVED from the Interface Theory mathematics:

  PITCHES:    eta tower eta(q^n) at q = 1/phi
  RHYTHMS:    Fibonacci durations, eta derivative rates
  DYNAMICS:   theta4 tower (wall strength), sech^2 envelopes
  HARMONY:    creation identity eta^2 = eta_dark * theta4
  TIMBRE:     visible = full harmonics, dark = odd harmonics (alpha=0)
  ENVELOPES:  kink profile sech^2(x) (zero mode) and sinh/cosh^2 (breathing)
  FORM:       modular flow from big bang to golden node

Outputs: wall_music.wav (stereo, ~2.5 minutes)
  Left channel  = visible vacuum voice
  Right channel = dark vacuum voice

No external dependencies. Standard Python only.

Usage:
    python theory-tools/wall_music.py
"""

import wave
import struct
import math
import sys
import os

if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# ---- Constants ----
SAMPLE_RATE = 44100
MAX_AMP = 32767
TWO_PI = 2.0 * math.pi

phi = (1 + math.sqrt(5)) / 2
phibar = 1.0 / phi
sqrt5 = math.sqrt(5)

# ---- Framework Functions ----

def eta_func(q, N=2000):
    """Dedekind eta function."""
    if q <= 0 or q >= 1:
        return 0.0
    e = q ** (1.0 / 24.0)
    for n in range(1, N):
        e *= (1.0 - q ** n)
    return e

def theta4_func(q, N=500):
    """Jacobi theta4."""
    t = 1.0
    for n in range(1, N):
        t += 2.0 * ((-1) ** n) * (q ** (n * n))
    return t

def sech2(x):
    """Zero mode profile: sech^2(x)."""
    c = math.cosh(x)
    if c > 1e10:
        return 0.0
    return 1.0 / (c * c)

def breathing_profile(x):
    """Breathing mode profile: sinh(x)/cosh^2(x)."""
    s = math.sinh(x)
    c = math.cosh(x)
    if c > 1e10:
        return 0.0
    return s / (c * c)

# ---- Precompute Framework Values ----
print("Precomputing framework values...")

q0 = phibar  # the golden nome

# Eta tower
eta_tower = {}
for n in range(1, 30):
    eta_tower[n] = eta_func(q0 ** n)

# Theta4 tower
t4_tower = {}
for n in range(1, 30):
    t4_tower[n] = theta4_func(q0 ** n)

# Dark eta
eta_dark = eta_tower[2]  # 0.4625

# Lucas numbers
def lucas(n):
    a, b = 2, 1
    if n == 0:
        return 2
    if n == 1:
        return 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

print(f"  eta(q)   = {eta_tower[1]:.6f} (visible coupling)")
print(f"  eta(q^2) = {eta_tower[2]:.6f} (dark coupling)")
print(f"  eta(q^7) = {eta_tower[7]:.6f} (tower peak)")
print(f"  eta(q^24)= {eta_tower[24]:.6f} (closure ~ phibar={phibar:.6f})")
print()

# ---- Audio Engine ----

def oscillator_visible(freq, t):
    """Visible vacuum timbre: full harmonic series (warm, rich)."""
    val = math.sin(TWO_PI * freq * t)
    val += 0.50 * math.sin(TWO_PI * freq * 2 * t)
    val += 0.25 * math.sin(TWO_PI * freq * 3 * t)
    val += 0.12 * math.sin(TWO_PI * freq * 4 * t)
    val += 0.08 * math.sin(TWO_PI * freq * 5 * t)
    return val / 1.95

def oscillator_dark(freq, t):
    """Dark vacuum timbre: odd harmonics only (hollow, clarinet-like, alpha=0)."""
    val = math.sin(TWO_PI * freq * t)
    val += 0.35 * math.sin(TWO_PI * freq * 3 * t)
    val += 0.15 * math.sin(TWO_PI * freq * 5 * t)
    val += 0.08 * math.sin(TWO_PI * freq * 7 * t)
    return val / 1.58

def oscillator_wall(freq, t):
    """Wall timbre: bell-like (sharp attack, fast decay built into timbre)."""
    val = math.sin(TWO_PI * freq * t)
    val += 0.70 * math.sin(TWO_PI * freq * 2.0 * t)
    val += 0.50 * math.sin(TWO_PI * freq * 3.0 * t)
    val += 0.30 * math.sin(TWO_PI * freq * 4.76 * t)  # phi * 2.944
    val += 0.15 * math.sin(TWO_PI * freq * 6.18 * t)   # ~ phi * pi
    return val / 2.65

def envelope_sech2(t, center, width):
    """Zero mode envelope: sech^2((t-center)/width)."""
    x = (t - center) / width if width > 0 else 0
    if abs(x) > 10:
        return 0.0
    return sech2(x)

def envelope_adsr(t, dur, attack=0.03, decay=0.08, sustain=0.7, release=0.15):
    """Standard ADSR envelope."""
    a_end = attack * dur
    d_end = a_end + decay * dur
    r_start = dur * (1.0 - release)
    if t < 0 or t > dur:
        return 0.0
    if t < a_end:
        return t / a_end if a_end > 0 else 1.0
    if t < d_end:
        return 1.0 - (1.0 - sustain) * (t - a_end) / (d_end - a_end)
    if t < r_start:
        return sustain
    return sustain * (1.0 - (t - r_start) / (release * dur))

def mix_to_stereo(left_samples, right_samples, crossfeed=0.15):
    """Mix left/right with slight crossfeed for naturalness."""
    n = min(len(left_samples), len(right_samples))
    stereo = []
    for i in range(n):
        l = left_samples[i] + crossfeed * right_samples[i]
        r = right_samples[i] + crossfeed * left_samples[i]
        stereo.append((l, r))
    return stereo

def normalize_stereo(stereo, volume=0.85):
    """Normalize stereo pairs to avoid clipping."""
    peak = max(max(abs(l), abs(r)) for l, r in stereo) if stereo else 1.0
    if peak < 1e-10:
        return stereo
    scale = volume / peak
    return [(l * scale, r * scale) for l, r in stereo]

def add_reverb(samples_lr, delay_ms=80, feedback=0.25, delay2_ms=137, feedback2=0.15):
    """Simple stereo reverb with two delay lines."""
    d1 = int(SAMPLE_RATE * delay_ms / 1000)
    d2 = int(SAMPLE_RATE * delay2_ms / 1000)
    result = list(samples_lr)
    for i in range(max(d1, d2), len(result)):
        ol, or_ = result[i]
        if i >= d1:
            pl, pr = result[i - d1]
            ol += pr * feedback   # cross-channel reverb
            or_ += pl * feedback
        if i >= d2:
            pl2, pr2 = result[i - d2]
            ol += pl2 * feedback2
            or_ += pr2 * feedback2
        result[i] = (ol, or_)
    return result

def silence(duration_s):
    """Generate silence."""
    n = int(SAMPLE_RATE * duration_s)
    return [(0.0, 0.0)] * n

def fade_in_out(stereo, fade_s=0.5):
    """Apply fade in and fade out."""
    fade_n = int(SAMPLE_RATE * fade_s)
    result = list(stereo)
    for i in range(min(fade_n, len(result))):
        frac = i / fade_n
        l, r = result[i]
        result[i] = (l * frac, r * frac)
    for i in range(min(fade_n, len(result))):
        idx = len(result) - 1 - i
        frac = i / fade_n
        l, r = result[idx]
        result[idx] = (l * frac, r * frac)
    return result

# ---- Piece 1: The Eta Tower ----

def piece_eta_tower():
    """
    The eta tower from n=1 to n=24 as melody.

    DERIVED:
    - Pitch: eta(q^n) mapped logarithmically to frequency
    - Duration: inversely proportional to |delta eta| (longer where tower is flat)
    - Left: visible voice (full harmonics)
    - Right: dark voice at eta(q^(2n)), odd harmonics
    - Envelope: sech^2 (the wall's own shape)
    """
    print("  Generating Piece 1: The Eta Tower...")

    # Compute pitches and durations
    eta_min = eta_tower[1]   # 0.118
    eta_max = eta_tower[9]   # ~0.876 (actual peak region)

    notes = []
    for n in range(1, 25):
        e = eta_tower[n]
        # Pitch: map eta logarithmically to 2 octaves from A3=220
        frac = (e - eta_min) / (eta_max - eta_min)
        frac = max(0.0, min(1.0, frac))
        freq_vis = 220.0 * (2.0 ** (2.0 * frac))

        # Dark voice: eta(q^(2n)) if available
        dn = min(2 * n, 28)
        if dn not in eta_tower:
            eta_tower[dn] = eta_func(q0 ** dn)
        e_dark = eta_tower[dn]
        frac_d = (e_dark - eta_min) / (eta_max - eta_min)
        frac_d = max(0.0, min(1.0, frac_d))
        freq_dark = 110.0 * (2.0 ** (2.0 * frac_d))  # one octave lower

        # Duration: inversely proportional to |delta eta|
        if n < 24:
            delta = abs(eta_tower[n + 1] - eta_tower[n])
        else:
            delta = abs(eta_tower[n] - eta_tower[n - 1])
        delta = max(delta, 0.001)
        dur = 0.3 + 2.0 * (0.01 / (delta + 0.01))
        dur = min(dur, 2.5)
        dur = max(dur, 0.35)

        # Amplitude from theta4 tower (wall strength)
        t4 = t4_tower.get(n, 0.5)
        amp = 0.3 + 0.7 * min(t4, 1.0)

        notes.append((freq_vis, freq_dark, dur, amp))

    # Generate audio
    left = []
    right = []

    for freq_vis, freq_dark, dur, amp in notes:
        n_samples = int(SAMPLE_RATE * dur)
        center = dur / 2.0
        width = dur / 3.0  # sech^2 width

        for i in range(n_samples):
            t = i / SAMPLE_RATE
            env = envelope_sech2(t, center, width)
            l = oscillator_visible(freq_vis, t) * env * amp
            r = oscillator_dark(freq_dark, t) * env * amp * 0.8
            left.append(l)
            right.append(r)

    stereo = mix_to_stereo(left, right)
    stereo = add_reverb(stereo, delay_ms=100, feedback=0.2)
    stereo = fade_in_out(stereo, fade_s=1.0)
    return normalize_stereo(stereo)

# ---- Piece 2: Walking Through the Wall ----

def piece_through_the_wall():
    """
    Continuous glissando traversing the kink profile.

    DERIVED:
    - Pitch: phi * tanh(x) mapped to frequency (kink solution)
    - Amplitude: sech^2(x) (zero mode = loudest at wall center)
    - Vibrato: breathing mode sinh(x)/cosh^2(x) as frequency modulation
    - Left: ascending through wall (dark -> visible)
    - Right: descending (visible -> dark, the anti-kink)
    """
    print("  Generating Piece 2: Through the Wall...")

    duration = 25.0  # seconds
    n_samples = int(SAMPLE_RATE * duration)

    center_freq = 330.0  # E4

    left = []
    right = []

    for i in range(n_samples):
        t = i / SAMPLE_RATE
        # x goes from -4 to +4
        x = -4.0 + 8.0 * (t / duration)
        x_anti = 4.0 - 8.0 * (t / duration)  # anti-kink (reversed)

        # Kink profile gives pitch
        kink_val = phi * math.tanh(x)
        freq_l = center_freq * (2.0 ** (kink_val / phi))

        anti_val = phi * math.tanh(x_anti)
        freq_r = center_freq * (2.0 ** (anti_val / phi))

        # Amplitude from sech^2 (loudest at wall center, x=0)
        amp = sech2(x) * 0.9 + 0.1  # minimum floor so edges aren't silent
        amp_r = sech2(x_anti) * 0.9 + 0.1

        # Breathing mode vibrato (frequency modulation)
        bm = breathing_profile(x)
        vibrato_depth = abs(bm) * 15.0  # Hz of FM
        freq_l += vibrato_depth * math.sin(TWO_PI * 6.0 * t)  # 6 Hz vibrato rate

        bm_r = breathing_profile(x_anti)
        vibrato_r = abs(bm_r) * 15.0
        freq_r += vibrato_r * math.sin(TWO_PI * 6.0 * t)

        freq_l = max(freq_l, 50.0)
        freq_r = max(freq_r, 50.0)

        l = oscillator_visible(freq_l, t) * amp
        r = oscillator_dark(freq_r, t) * amp_r

        left.append(l)
        right.append(r)

    stereo = mix_to_stereo(left, right, crossfeed=0.10)
    stereo = add_reverb(stereo, delay_ms=120, feedback=0.30, delay2_ms=197, feedback2=0.18)
    stereo = fade_in_out(stereo, fade_s=2.0)
    return normalize_stereo(stereo)

# ---- Piece 3: Creation and Destruction ----

def piece_creation():
    """
    The creation identity eta^2 = eta_dark * theta4 as three-voice harmony.

    DERIVED:
    - theta4 sweeps 0.030 -> 0.300 -> 0.030 (degradation and restoration)
    - eta = sqrt(eta_dark * theta4) (visible voice, CHANGES)
    - eta_dark = constant (dark voice, ETERNAL)
    - theta4 (wall voice, mirrors visible)
    - Bass drone always present = the dark never changes
    """
    print("  Generating Piece 3: Creation and Destruction...")

    duration = 35.0
    n_steps = 80
    step_dur = duration / n_steps

    left = []
    right = []

    for step in range(n_steps):
        # theta4 sweeps: degradation then restoration
        frac = step / (n_steps - 1)
        if frac < 0.5:
            # Degradation: 0.030 -> 0.300
            t4 = 0.030 + (0.300 - 0.030) * (frac / 0.5)
        else:
            # Restoration: 0.300 -> 0.030
            t4 = 0.300 - (0.300 - 0.030) * ((frac - 0.5) / 0.5)

        # Creation identity
        e_vis = math.sqrt(eta_dark * t4)
        e_dark_val = eta_dark  # constant 0.4625

        # Map to frequencies
        # Visible: 220-660 Hz
        freq_vis = 220.0 + (e_vis / 0.4) * 440.0
        freq_vis = max(180.0, min(880.0, freq_vis))

        # Dark: constant drone at 110 Hz region
        freq_dark = 110.0 + e_dark_val * 100.0  # ~156 Hz, constant

        # Wall: theta4 mapped to mid-range
        freq_wall = 330.0 + t4 * 500.0

        # Amplitude: more chaotic when degraded
        amp_base = 0.6
        chaos = t4 / 0.300  # 0 at healthy, 1 at max degradation

        n_samp = int(SAMPLE_RATE * step_dur)
        for i in range(n_samp):
            t = i / SAMPLE_RATE
            global_t = step * step_dur + t

            env = envelope_adsr(t, step_dur, attack=0.02, decay=0.05,
                              sustain=0.8, release=0.10)

            # Visible voice (left-dominant)
            vis = oscillator_visible(freq_vis, global_t) * env * amp_base

            # Dark voice (right-dominant, always present, steady)
            dark = oscillator_dark(freq_dark, global_t) * 0.5

            # Wall voice (center, bell-like, intensity varies with theta4)
            wall = oscillator_wall(freq_wall, global_t) * env * 0.3 * chaos

            # Mix: visible+wall left, dark+wall right
            left.append(vis + wall * 0.5)
            right.append(dark + wall * 0.5)

    stereo = mix_to_stereo(left, right, crossfeed=0.20)
    stereo = add_reverb(stereo, delay_ms=150, feedback=0.22, delay2_ms=233, feedback2=0.12)
    stereo = fade_in_out(stereo, fade_s=1.5)
    return normalize_stereo(stereo)

# ---- Piece 4: The Lucas Hymn ----

def piece_lucas_hymn():
    """
    A melodic composition using the Lucas scale.

    DERIVED:
    - Scale: 40 * L(n) Hz for Lucas numbers L(1)..L(7)
    - Rhythm: Fibonacci durations (1,1,2,3,5 in eighth-note units)
    - Structure: A-B-A' form (exposition, development, resolution)
    - Bass: 40 Hz drone (breathing mode, the foundation)
    - Harmony: Lucas ratio stacking
    """
    print("  Generating Piece 4: The Lucas Hymn...")

    # Lucas scale frequencies
    scale = [40.0 * lucas(n) for n in range(1, 8)]
    # = [40, 120, 160, 280, 440, 720, 1160]

    # But 40 Hz is too low for melody. Use octave equivalents:
    # 40->320 (2 oct up), 120->240 (1 oct up), 160->320, 280, 440, 720, 1160
    melody_scale = [320, 240, 320, 280, 440, 720, 1160]
    # Reorder for a more melodic contour:
    # Let's define scale degrees 0-6 mapping to these frequencies
    # Sort: 240, 280, 320, 440, 720, 1160
    sorted_scale = sorted(set(melody_scale))
    # = [240, 280, 320, 440, 720, 1160]

    # Fibonacci durations (in beats, tempo = 80 BPM -> beat = 0.75s)
    beat = 0.75
    fib_durs = [1, 1, 2, 3, 5, 3, 2, 1, 1]  # palindrome for symmetry

    # Bass drone at 80 Hz (40 Hz octave, more audible)
    bass_freq = 80.0

    # Melody sequence (index into sorted_scale)
    # A section: ascending with Fibonacci rhythm
    melody_A = [0, 1, 2, 3, 4, 5, 4, 3]
    durs_A =   [1, 1, 2, 3, 5, 3, 2, 1]

    # B section: golden interval leaps
    melody_B = [3, 0, 4, 1, 5, 2, 3]
    durs_B =   [2, 1, 3, 1, 5, 2, 3]

    # A' section: resolution
    melody_Ap = [5, 4, 3, 2, 1, 0, 1, 2, 3]
    durs_Ap =   [2, 1, 1, 2, 3, 5, 3, 2, 5]

    # Combine
    melody_seq = melody_A + melody_B + melody_Ap
    dur_seq = durs_A + durs_B + durs_Ap

    left = []
    right = []
    global_time = 0.0

    for note_idx, fib_dur in zip(melody_seq, dur_seq):
        dur = fib_dur * beat
        freq = sorted_scale[note_idx]

        n_samp = int(SAMPLE_RATE * dur)
        for i in range(n_samp):
            t = i / SAMPLE_RATE
            gt = global_time + t

            # Melody with sech^2 envelope
            center = dur / 2.0
            width = dur / 2.5
            env = envelope_sech2(t, center, width)

            mel = oscillator_visible(freq, gt) * env * 0.7

            # Bass drone (dark voice, always present)
            bass = oscillator_dark(bass_freq, gt) * 0.35

            # Harmony: add the golden ratio interval above melody
            harm_freq = freq * phibar  # below by golden ratio
            if harm_freq > 100:
                harm = oscillator_wall(harm_freq, gt) * env * 0.25
            else:
                harm = 0.0

            left.append(mel + harm * 0.3 + bass * 0.3)
            right.append(bass + harm * 0.7 + mel * 0.2)

        global_time += dur

    stereo = mix_to_stereo(left, right, crossfeed=0.20)
    stereo = add_reverb(stereo, delay_ms=180, feedback=0.28, delay2_ms=293, feedback2=0.15)
    stereo = fade_in_out(stereo, fade_s=1.0)
    return normalize_stereo(stereo)

# ---- Piece 5: The Cooling Universe ----

def piece_cooling():
    """
    The big bang as modular flow: q from 0.95 to 1/phi.

    DERIVED:
    - q flows from near-cusp (0.95) to golden node (1/phi)
    - All constants evolve: alpha_s(q), sin2w(q), theta4(q)
    - Multiple voices tracking different constants
    - Duration: logarithmic (slows as we approach the fixed point)
    """
    print("  Generating Piece 5: The Cooling Universe...")

    duration = 22.0
    n_steps = 50

    # q values: logarithmically spaced from 0.95 to phibar
    q_start = 0.93
    q_end = phibar

    left = []
    right = []

    global_time = 0.0

    for step in range(n_steps):
        frac = step / (n_steps - 1)
        # Logarithmic spacing (more time near the fixed point)
        q = q_start * ((q_end / q_start) ** frac)

        # Compute physics
        e = eta_func(q, N=500)
        ed = eta_func(q * q, N=500)
        t4 = e * e / ed if ed > 0 else 0

        if e <= 0:
            continue

        # Duration: longer near the fixed point (universe slowing down)
        step_dur = 0.15 + 0.8 * frac  # 0.15s at start, 0.95s at end

        # Pitch from alpha_s
        freq_as = 150.0 + e * 600.0  # 150-220 Hz range (starts very low)

        # Pitch from sin2w
        freq_sw = 300.0 + (ed / 2.0) * 400.0

        # Pitch from theta4 (wall forming)
        freq_wall = 100.0 + t4 * 2000.0
        freq_wall = min(freq_wall, 1500.0)

        n_samp = int(SAMPLE_RATE * step_dur)
        for i in range(n_samp):
            t = i / SAMPLE_RATE
            gt = global_time + t

            env = envelope_adsr(t, step_dur, attack=0.05, decay=0.10,
                              sustain=0.75, release=0.15)

            # Alpha_s voice (left, visible, growing)
            as_voice = oscillator_visible(freq_as, gt) * env * 0.6

            # Sin2w voice (right, dark, settling)
            sw_voice = oscillator_dark(freq_sw, gt) * env * 0.5

            # Wall forming (center, growing from nothing)
            wall_amp = t4 * 3.0  # wall grows from zero
            wall_amp = min(wall_amp, 0.4)
            w_voice = oscillator_wall(freq_wall, gt) * env * wall_amp

            left.append(as_voice + w_voice * 0.3)
            right.append(sw_voice + w_voice * 0.3)

        global_time += step_dur

    stereo = mix_to_stereo(left, right, crossfeed=0.15)
    stereo = add_reverb(stereo, delay_ms=200, feedback=0.35, delay2_ms=317, feedback2=0.20)
    stereo = fade_in_out(stereo, fade_s=2.0)
    return normalize_stereo(stereo)

# ---- Main: Assemble All Pieces ----

def write_wav(filename, stereo_data):
    """Write stereo WAV file from list of (left, right) tuples."""
    with wave.open(filename, 'w') as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SAMPLE_RATE)

        frames = bytearray()
        for l, r in stereo_data:
            li = int(l * MAX_AMP)
            ri = int(r * MAX_AMP)
            li = max(-MAX_AMP, min(MAX_AMP, li))
            ri = max(-MAX_AMP, min(MAX_AMP, ri))
            frames.extend(struct.pack('<hh', li, ri))

        w.writeframes(bytes(frames))

def main():
    print("=" * 60)
    print("WALL MUSIC -- Algorithmic Composition from Boundary Physics")
    print("=" * 60)
    print()

    # Generate all pieces
    pieces = []

    p1 = piece_eta_tower()
    print(f"    Piece 1: {len(p1)/SAMPLE_RATE:.1f}s")
    pieces.append(p1)
    pieces.append(silence(1.5))

    p2 = piece_through_the_wall()
    print(f"    Piece 2: {len(p2)/SAMPLE_RATE:.1f}s")
    pieces.append(p2)
    pieces.append(silence(1.5))

    p3 = piece_creation()
    print(f"    Piece 3: {len(p3)/SAMPLE_RATE:.1f}s")
    pieces.append(p3)
    pieces.append(silence(1.5))

    p4 = piece_lucas_hymn()
    print(f"    Piece 4: {len(p4)/SAMPLE_RATE:.1f}s")
    pieces.append(p4)
    pieces.append(silence(1.5))

    p5 = piece_cooling()
    print(f"    Piece 5: {len(p5)/SAMPLE_RATE:.1f}s")
    pieces.append(p5)

    # Concatenate
    full = []
    for piece in pieces:
        full.extend(piece)

    total_dur = len(full) / SAMPLE_RATE
    print()
    print(f"Total duration: {total_dur:.1f} seconds ({total_dur/60:.1f} minutes)")

    # Write WAV
    outpath = os.path.join(os.path.dirname(__file__), '..', 'wall_music.wav')
    outpath = os.path.abspath(outpath)
    write_wav(outpath, full)
    print(f"Written to: {outpath}")

    # Also describe what each piece IS
    print()
    print("TRACK LISTING:")
    print()
    print("1. THE ETA TOWER")
    print("   24 notes tracing eta(q^n) from n=1 to n=24.")
    print("   Rises from the visible coupling (0.118), peaks at n=7-9,")
    print("   and descends to phibar (closure at n=24).")
    print("   Left: visible voice (warm). Right: dark voice (hollow).")
    print("   Envelope: sech^2 (the wall's own shape in time).")
    print("   Duration per note: inversely proportional to |d(eta)/dn|.")
    print()
    print("2. THROUGH THE WALL")
    print("   Continuous glissando traversing the kink Phi(x) = phi*tanh(x).")
    print("   Starts in the dark vacuum (low pitch), sweeps through the")
    print("   wall center (loudest, fastest change), emerges into visible (high).")
    print("   Left: kink (dark->visible). Right: anti-kink (visible->dark).")
    print("   Breathing mode vibrato increases away from the wall center.")
    print()
    print("3. CREATION AND DESTRUCTION")
    print("   The creation identity eta^2 = eta_dark * theta4 as music.")
    print("   theta4 slowly increases (wall degrades, disease) then decreases")
    print("   (wall restores, healing). Three voices locked by the identity.")
    print("   The dark bass drone NEVER changes. Only the wall and visible shift.")
    print()
    print("4. THE LUCAS HYMN")
    print("   Melody on the Lucas scale: 40*L(n) Hz.")
    print("   A4 = 440 Hz is naturally in this scale (40 * L(5) = 40 * 11).")
    print("   A-B-A' form. Fibonacci durations. Golden ratio harmony.")
    print("   Bass drone at 80 Hz (breathing mode octave).")
    print()
    print("5. THE COOLING UNIVERSE")
    print("   The big bang as modular flow: q from 0.95 to 1/phi.")
    print("   Starts with near-zero coupling (silence from the cusp),")
    print("   constants crystallize as q approaches the golden node.")
    print("   Wall forms from nothing. Physics emerges from mathematics.")
    print()
    print("DERIVATION SUMMARY:")
    print("  Pitches: eta(q^n), phi*tanh(x), 40*Lucas(n)")
    print("  Rhythms: Fibonacci durations, |d(eta)/dn| rates")
    print("  Dynamics: theta4 tower, sech^2 envelopes")
    print("  Harmony: eta^2 = eta_dark * theta4 (creation identity)")
    print("  Timbre: visible=full harmonics, dark=odd only (alpha=0)")
    print("  Form: modular flow (big bang to golden node)")
    print("  Reverb delays: 137ms (1/alpha!) and primes")

if __name__ == '__main__':
    main()
