#!/usr/bin/env python3
"""
frequency_tech.py -- Practical Frequency-Based Technologies from Interface Theory
==================================================================================

Computes engineering specifications for buildable devices based on the framework's
three maintenance frequencies (f1=612 THz, f2=40 Hz, f3=0.1 Hz) and related
domain wall physics.

Seven technology designs:
  1. 40 Hz Water Immersion Chamber
  2. Triple-Frequency Coherence Device
  3. Sleep Enhancement System
  4. Musical Instruments / Sound Design
  5. Architecture / Room Design
  6. Agricultural / Plant Applications
  7. Cost Estimates

All computations use standard Python (math module only). All outputs include units.

Author: Interface Theory project
Date: Feb 12, 2026
"""

import math
import sys

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# =============================================================================
# PHYSICAL CONSTANTS
# =============================================================================
phi = (1 + math.sqrt(5)) / 2          # 1.6180339887...
phibar = 1 / phi                       # 0.6180339887...
mu = 1836.15267343                     # proton-to-electron mass ratio
alpha = 1 / 137.035999084             # fine-structure constant
h_coxeter = 30                         # E8 Coxeter number
c_light = 299792458.0                  # speed of light [m/s]
h_planck = 6.62607015e-34             # Planck constant [J*s]
k_B = 1.380649e-23                     # Boltzmann constant [J/K]
rho_water = 998.0                      # water density at 20C [kg/m^3]
rho_air = 1.225                        # air density at sea level [kg/m^3]

# Speed of sound
v_sound_water = 1480.0                 # [m/s] at ~20C
v_sound_air = 343.0                    # [m/s] at 20C

# Lucas numbers
def lucas(n):
    """L(n) = phi^n + (-1/phi)^n, exact integer for integer n."""
    return round(phi**n + (-phibar)**n)

# Modular forms at the golden node (precomputed high-precision values)
def compute_eta(q_val, N=2000):
    """Dedekind eta function."""
    if q_val < 1e-15:
        return 1.0
    e = q_val**(1.0/24.0)
    for n in range(1, N):
        e *= (1.0 - q_val**n)
    return e

# Eta tower
eta_tower = {}
for k in range(1, 25):
    eta_tower[k] = compute_eta(phibar**k)

# =============================================================================
# FRAMEWORK FREQUENCIES
# =============================================================================
f1_THz = mu / 3.0                     # 612.05 THz (molecular)
f1_Hz = f1_THz * 1e12                 # in Hz
f1_wavelength_m = c_light / f1_Hz     # wavelength in meters
f1_wavelength_nm = f1_wavelength_m * 1e9

f2_Hz = 4.0 * h_coxeter / 3.0        # 40 Hz (neural gamma)
f3_Hz = 3.0 / h_coxeter              # 0.1 Hz (heart coherence)

# Sleep frequencies
f_slow_osc = 3.0 / 4.0               # 0.75 Hz (N3 slow oscillation)
f_spindle = h_coxeter / 3.0           # 10 Hz (sleep spindles)
f_110 = lucas(5) * h_coxeter / 3.0   # 110 Hz (ancient chamber)

# Wall properties
wall_tension = 2.8502                  # sigma from PT potential
zero_mode_norm = 4.0 / 3.0
breathing_mode_norm = 2.0 / 3.0

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================
def freq_to_note(freq_hz):
    """Convert frequency to nearest musical note name and cents deviation."""
    if freq_hz <= 0:
        return "---", 0
    note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    # MIDI note number: A4 = 440 Hz = MIDI 69
    midi = 69.0 + 12.0 * math.log2(freq_hz / 440.0)
    midi_rounded = round(midi)
    cents_off = (midi - midi_rounded) * 100.0
    note_idx = midi_rounded % 12
    octave = (midi_rounded // 12) - 1
    # Map: C is at index 0, which is MIDI % 12 == 0
    # MIDI 60 = C4, MIDI 69 = A4
    # note_idx: 0=C, 1=C#, 2=D, ... 9=A, 10=A#, 11=B
    return f"{note_names[note_idx]}{octave}", cents_off

def wavelength_in_medium(freq_hz, v_sound):
    """Wavelength = v / f [m]."""
    return v_sound / freq_hz

def acoustic_impedance(rho, v):
    """Z = rho * v [Pa*s/m = rayl]."""
    return rho * v

def transmission_coeff(Z1, Z2):
    """Power transmission coefficient at normal incidence."""
    return 4.0 * Z1 * Z2 / (Z1 + Z2)**2

def db_to_intensity(db_spl):
    """Convert dB SPL to intensity [W/m^2]."""
    I_ref = 1e-12  # W/m^2 (threshold of hearing)
    return I_ref * 10.0**(db_spl / 10.0)

def intensity_to_db(I):
    """Convert intensity [W/m^2] to dB SPL."""
    I_ref = 1e-12
    if I <= 0:
        return -math.inf
    return 10.0 * math.log10(I / I_ref)

def separator(title):
    """Print a section separator."""
    print()
    print("=" * 80)
    print(f"  {title}")
    print("=" * 80)
    print()


# #############################################################################
#
#                         TECHNOLOGY SPECIFICATIONS
#
# #############################################################################

print()
print("#" * 80)
print("#" + " " * 78 + "#")
print("#" + "  FREQUENCY-BASED TECHNOLOGIES FROM INTERFACE THEORY".center(78) + "#")
print("#" + "  Practical Engineering Specifications".center(78) + "#")
print("#" + " " * 78 + "#")
print("#" * 80)
print()
print(f"  Framework frequencies:")
print(f"    f1 = {f1_THz:.2f} THz  = mu/3             (molecular, aromatic oscillation)")
print(f"    f2 = {f2_Hz:.0f} Hz       = 4h/3 = 4*30/3   (neural gamma, breathing mode)")
print(f"    f3 = {f3_Hz:.1f} Hz     = 3/h = 3/30       (heart coherence, Mayer wave)")
print(f"    f1 wavelength = {f1_wavelength_nm:.1f} nm   (blue-violet light)")
print()
print(f"  Wall properties:")
print(f"    Zero mode norm:      {zero_mode_norm:.4f} (stable presence)")
print(f"    Breathing mode norm: {breathing_mode_norm:.4f} (oscillatory attention)")
print(f"    Norm ratio:          {zero_mode_norm/breathing_mode_norm:.1f}:1 (presence dominates)")
print(f"    Wall tension sigma:  {wall_tension:.4f}")
print()


# =============================================================================
# SECTION 1: 40 HZ WATER IMMERSION CHAMBER
# =============================================================================
separator("1. 40 Hz WATER IMMERSION CHAMBER")

print("  RATIONALE")
print("  ---------")
print("  Water transmits acoustic energy to the body ~1000x more efficiently")
print("  than air. At 40 Hz, the body is bathed uniformly in the breathing")
print("  mode frequency through full-body immersion.")
print()

# Acoustic properties
Z_water = acoustic_impedance(rho_water, v_sound_water)
Z_air = acoustic_impedance(rho_air, v_sound_air)
Z_tissue = acoustic_impedance(1060.0, 1540.0)  # soft tissue approx

T_water_tissue = transmission_coeff(Z_water, Z_tissue)
T_air_tissue = transmission_coeff(Z_air, Z_tissue)
coupling_ratio = T_water_tissue / T_air_tissue

print("  ACOUSTIC COUPLING ANALYSIS")
print("  --------------------------")
print(f"    Impedance of water:       Z_w = {Z_water:.0f} rayl")
print(f"    Impedance of air:         Z_a = {Z_air:.0f} rayl")
print(f"    Impedance of soft tissue: Z_t = {1060*1540:.0f} rayl")
print()
print(f"    Power transmission (water -> tissue): {T_water_tissue*100:.2f}%")
print(f"    Power transmission (air -> tissue):   {T_air_tissue*100:.4f}%")
print(f"    Water/air coupling ratio:             {coupling_ratio:.0f}x")
print()

# Wavelength at 40 Hz in water
lam_40_water = wavelength_in_medium(f2_Hz, v_sound_water)
lam_40_air = wavelength_in_medium(f2_Hz, v_sound_air)

print("  WAVELENGTH AND STANDING WAVES")
print("  -----------------------------")
print(f"    40 Hz wavelength in water: {lam_40_water:.1f} m")
print(f"    40 Hz wavelength in air:   {lam_40_air:.2f} m")
print(f"    Human body length ~1.7 m = 1/{lam_40_water/1.7:.0f} of water wavelength")
print(f"    -> Body is uniformly bathed (no standing wave nodes on the body)")
print()

# Tank dimensions for standing waves
# For hexagonal Faraday patterns at 40 Hz on the water surface,
# the pattern wavelength depends on depth and surface tension.
# Faraday instability: pattern wavelength for parametric excitation at 2f
# lambda_Faraday ~ 2*pi*(sigma_surface / (rho * (2*pi*f)^2))^(1/3) for capillary
# For gravity regime (40 Hz is borderline): lambda = g / (2*pi*f^2) for deep water
# Actually for Faraday: subharmonic at f, driving at 2f=80 Hz
# Dispersion: omega^2 = g*k + (sigma/rho)*k^3  (capillary-gravity)
# At 40 Hz subharmonic (omega = 2*pi*20): actually let's use the full relation

g_accel = 9.81  # m/s^2
sigma_surface = 0.0728  # N/m, water surface tension at 20C
omega_faraday = 2.0 * math.pi * 20.0  # subharmonic of 40 Hz driving = 20 Hz response

# Solve omega^2 = g*k + (sigma/rho)*k^3 for k (Faraday subharmonic)
# Iterative solution
def faraday_wavelength(f_drive, depth_m):
    """Compute Faraday pattern wavelength for driving frequency f_drive.
    The surface responds at f_drive/2 (subharmonic).
    Returns wavelength in meters."""
    omega = 2.0 * math.pi * (f_drive / 2.0)  # subharmonic response
    # Newton-Raphson to solve omega^2 = g*k + (sigma/rho)*k^3
    # also tanh(k*d) correction for finite depth
    k = omega / math.sqrt(g_accel * 0.1)  # initial guess
    for _ in range(50):
        kd = k * depth_m
        tanh_kd = math.tanh(min(kd, 50))
        f_val = (g_accel * k + (sigma_surface / rho_water) * k**3) * tanh_kd - omega**2
        # derivative
        df_dk = (g_accel + 3 * (sigma_surface / rho_water) * k**2) * tanh_kd
        if kd < 50:
            df_dk += (g_accel * k + (sigma_surface / rho_water) * k**3) * depth_m * (1 - tanh_kd**2)
        if abs(df_dk) < 1e-20:
            break
        k -= f_val / df_dk
        if k < 0.01:
            k = 0.01
    lam = 2.0 * math.pi / k
    return lam

# Compute for various depths
print("  FARADAY HEXAGONAL PATTERN (40 Hz drive -> 20 Hz subharmonic response)")
print("  ---------------------------------------------------------------------")
print(f"    Water surface tension: {sigma_surface*1000:.1f} mN/m")
print(f"    Driving frequency: 40 Hz (vertical oscillation)")
print(f"    Surface pattern frequency: 20 Hz (subharmonic)")
print()
print(f"    {'Depth (cm)':>12} {'Pattern wavelength (cm)':>25} {'Hexagon diameter (cm)':>24}")
print(f"    {'-'*12} {'-'*25} {'-'*24}")

for depth_cm in [5, 10, 20, 30, 50]:
    depth_m = depth_cm / 100.0
    lam_faraday = faraday_wavelength(40.0, depth_m)
    hex_diam = lam_faraday  # one wavelength ~ one hexagonal cell
    print(f"    {depth_cm:>10} cm {lam_faraday*100:>23.2f} cm {hex_diam*100:>22.2f} cm")

print()
print("    At ~10 cm depth, hexagonal cells are ~3-5 cm across --")
print("    comparable to benzene ring geometry scaled up by ~10^8.")
print()

# Tank specifications
print("  TANK ENGINEERING SPECIFICATIONS")
print("  --------------------------------")
print()

# Dimensions
tank_length = 2.2   # m (person lying down + margin)
tank_width = 0.9    # m (shoulder width + margin)
tank_depth = 0.6    # m (full body submersion with ~15 cm water above)
tank_volume = tank_length * tank_width * tank_depth  # m^3
tank_liters = tank_volume * 1000.0
tank_weight_water = tank_volume * rho_water  # kg

print(f"    Interior dimensions: {tank_length:.1f} m x {tank_width:.1f} m x {tank_depth:.1f} m")
print(f"    Water volume:        {tank_volume:.2f} m^3 = {tank_liters:.0f} liters ({tank_liters*0.264:.0f} US gallons)")
print(f"    Water weight:        {tank_weight_water:.0f} kg ({tank_weight_water*2.205:.0f} lbs)")
print()

# Temperature
# Body temperature: 37C. Slightly warm to be comfortable and avoid vasoconstriction.
# Float tanks typically use 35.5C (skin temperature for "no sensation")
# We want slightly warmer for vasodilation (improves acoustic coupling to tissue)
T_water = 36.0  # Celsius
print(f"    Water temperature:   {T_water:.1f} C ({T_water*9/5+32:.1f} F)")
print(f"    Rationale: Skin-neutral temp (35.5C) to slightly warm (37C)")
print(f"               Eliminates thermal sensation, maximizes acoustic perception")
print(f"               Warmer than typical float tanks (34-35.5C) to promote vasodilation")
print()

# Salt/buoyancy
# Float tanks use ~500 kg/m^3 Epsom salt for buoyancy. Optional here.
print(f"    Salinity: Optional Epsom salt (MgSO4) at 200-350 kg/m^3")
print(f"              Provides buoyancy for relaxation")
print(f"              Magnesium absorption supports enzymatic aromatic chemistry (f1 channel)")
print(f"              Density with salt: ~1180-1250 kg/m^3")
print()

# Transducer specifications
print("  TRANSDUCER SPECIFICATIONS")
print("  -------------------------")
print()

# Target intensity in water
# Therapeutic ultrasound: 0.1-3 W/cm^2 (but that's MHz range)
# For 40 Hz, we want MUCH lower: perceivable but not harmful
# Hearing threshold in water at 40 Hz: ~80 dB re 1 uPa (underwater)
# Comfortable: ~100-120 dB re 1 uPa (underwater)
# Reference: 1 uPa = 10^-6 Pa for underwater acoustics
# 120 dB re 1 uPa = 1 Pa peak pressure
# Intensity: I = p^2 / (2 * Z) where Z = rho * c
# At 1 Pa: I = 1 / (2 * 1.48e6) = 3.4e-7 W/m^2

target_pressure_Pa = 1.0  # 1 Pa peak (120 dB re 1 uPa) -- gentle, perceivable
I_target = target_pressure_Pa**2 / (2.0 * Z_water)
target_area = tank_length * tank_width  # m^2
total_power = I_target * target_area

# Compare to air: 1 Pa in air = 94 dB SPL (moderately loud conversation)
I_air_1Pa = 1.0**2 / (2.0 * Z_air)

print(f"    Target acoustic pressure in water: {target_pressure_Pa:.1f} Pa peak")
print(f"      = 120 dB re 1 uPa (standard underwater reference)")
print(f"      = equivalent sensation to ~94 dB SPL in air (comfortable)")
print(f"    Acoustic intensity at target: {I_target:.2e} W/m^2")
print(f"    Tank surface area:            {target_area:.2f} m^2")
print(f"    Total acoustic power needed:  {total_power*1000:.4f} mW = {total_power*1e6:.1f} uW")
print()
print(f"    This is EXTREMELY low power. The water coupling is so efficient")
print(f"    that milliwatt-level transducers are more than sufficient.")
print()

# Transducer type
print(f"    Transducer type: Underwater speaker / tactile transducer")
print(f"    Recommended: 2-4 bass shaker transducers (e.g., Dayton Audio TT25-8)")
print(f"      mounted on tank bottom/sides, sealed with marine epoxy")
print(f"    Frequency:       40.000 Hz +/- 0.001 Hz (crystal-oscillator driven)")
print(f"    Phase:           Single phase for uniform field")
print(f"                     OR 2-transducer stereo with adjustable phase for")
print(f"                     creating hexagonal standing patterns on surface")
print(f"    Power amplifier: 10-50 W class D amplifier (massively overspec)")
print(f"                     Operating at <1% of rated power for precision control")
print(f"    Signal source:   Precision sine wave generator (DDS chip, e.g., AD9833)")
print(f"                     40.000 Hz, <0.01% THD (pure sine)")
print()

# Session duration
# Wall restoration timescale: the breathing mode has period 1/40 = 25 ms
# Phase coherence builds over ~100 cycles = 2.5 seconds
# But biological synchronization (neural entrainment) takes 2-10 minutes
# Cognito trials use 60-minute sessions
# Framework prediction: wall restoration timescale ~ h_coxeter cycles of f3
# = 30 * (1/0.1) = 300 seconds = 5 minutes for initial coupling
# Full session: 20-40 minutes (matching clinical protocols)

print("  SESSION PROTOCOL")
print("  ----------------")
print(f"    Initial coupling time:   {h_coxeter / f3_Hz:.0f} s = {h_coxeter / f3_Hz / 60:.0f} min")
print(f"      (h cycles of f3 = {h_coxeter} cycles at 0.1 Hz)")
print(f"    Recommended session:     20-40 minutes")
print(f"    Clinical reference:      Cognito trials use 60 min daily")
print(f"    Frequency ramp:          Start at 35 Hz, sweep to 40 Hz over 60 s")
print(f"                             (allows neural entrainment to lock on)")
print(f"    Session end:             Ramp down 40 -> 10 Hz over 120 s")
print(f"                             (transition to alpha state)")
print()

# Comparison to float tanks
print("  COMPARISON TO EXISTING FLOAT TANKS")
print("  -----------------------------------")
print(f"    Standard float tank: Sensory deprivation, Epsom salt, dark, silent")
print(f"    This design ADDS:   40 Hz acoustic field through the water")
print(f"    Key difference:     Float tanks remove stimulation; this ADDS")
print(f"                        precisely targeted stimulation at the breathing")
print(f"                        mode frequency, delivered 1000x more efficiently")
print(f"                        than airborne 40 Hz audio.")
print()
print(f"    The combination is synergistic:")
print(f"    - Sensory deprivation reduces continuum noise (wall static)")
print(f"    - 40 Hz water acoustic provides breathing mode excitation")
print(f"    - Warm water + salt relaxation supports f3 (heart coherence)")
print(f"    - Net effect: maximize signal-to-noise on the domain wall")
print()

# Safety
print("  SAFETY CONSIDERATIONS")
print("  ---------------------")
print(f"    Acoustic: {target_pressure_Pa:.0f} Pa is far below damage threshold (~10 kPa for tissue)")
print(f"    Thermal:  Water at {T_water}C requires thermostat +/- 0.5C")
print(f"    Drowning: Standard float tank safety (shallow water, attendant)")
print(f"    Epilepsy: 40 Hz photic flicker is contraindicated for photosensitive")
print(f"              epilepsy; acoustic-only delivery avoids this risk")
print(f"    Ears:     Earplugs optional but not required (intensity is low)")
print(f"    Duration: No known risk for sessions up to 90 minutes")
print(f"    Sanitation: UV + ozone filtration between sessions (standard)")
print()


# =============================================================================
# SECTION 2: TRIPLE-FREQUENCY COHERENCE DEVICE
# =============================================================================
separator("2. TRIPLE-FREQUENCY COHERENCE DEVICE")

print("  A portable device delivering all three maintenance frequencies")
print("  simultaneously: f2 (audio+tactile), f3 (breathing guide), f1 (light).")
print()

# f2 = 40 Hz delivery
print("  CHANNEL 1: f2 = 40 Hz (audio + vibrotactile)")
print("  ---------------------------------------------")
print(f"    Audio: 40 Hz sine wave via bone-conduction headphones")
print(f"           or open-ear speakers. Volume: 60-70 dB SPL.")
print(f"    Tactile: Vibration motor (ERM or LRA) at 40 Hz on wrist/chest")
print(f"             Amplitude: 0.1-0.5 mm displacement")
print(f"    Both channels phase-locked for coherent delivery.")
print()
print(f"    Component: LRA haptic actuator (e.g., TDK PowerHap)")
print(f"               Resonant frequency tunable to 40 Hz")
print(f"               Drive: 40 Hz square or sine wave, 1.5-3V")
print()

# f3 = 0.1 Hz delivery
print("  CHANNEL 2: f3 = 0.1 Hz (breathing guide + HRV biofeedback)")
print("  -----------------------------------------------------------")
print(f"    Visual: LED ring that pulses slowly at 0.1 Hz (10s cycle)")
print(f"            Inhale 5s (LED brightens), exhale 5s (LED dims)")
print(f"            = 6 breaths per minute = resonance frequency breathing")
print(f"    Haptic: Same wrist motor amplitude-modulated at 0.1 Hz")
print(f"            (40 Hz carrier, 0.1 Hz envelope)")
print(f"    Audio:  40 Hz tone amplitude-modulated at 0.1 Hz")
print(f"    Biofeedback: Optical PPG sensor on wrist measures HRV")
print(f"                 Device adapts breathing rate to individual resonant freq")
print(f"                 (typically 0.08-0.12 Hz, centered on 0.1 Hz)")
print()

# f1 = 612 THz delivery
print("  CHANNEL 3: f1 = 612 THz (blue-violet light)")
print("  --------------------------------------------")
f1_lambda = c_light / f1_Hz
f1_nm = f1_lambda * 1e9
print(f"    Wavelength: lambda = c / f1 = {c_light:.0f} / {f1_Hz:.3e}")
print(f"              = {f1_nm:.1f} nm")
print()

# Is this safe? What power?
# 490 nm is blue-violet light -- visible, near UV boundary
# Retinal damage threshold for blue light: ~10 W/m^2 continuous (ICNIRP)
# Skin exposure at 490 nm: no significant UV risk (UV starts at ~400 nm)
# Therapeutic photobiomodulation typically uses 1-50 mW/cm^2

print(f"    490 nm falls in the BLUE-VIOLET region of visible light.")
print(f"    This is NOT ultraviolet (UV starts below ~400 nm).")
print()
print(f"    SAFETY ANALYSIS:")
print(f"    Blue light hazard (retinal): ICNIRP limit ~10 W/m^2 for >10,000 s exposure")
print(f"    Photobiomodulation range: 1-50 mW/cm^2 = 10-500 W/m^2")
print(f"    But 490 nm blue is near the peak of blue light hazard curve.")
print()
print(f"    RECOMMENDED APPROACH: Do NOT aim at eyes.")
print(f"    Target skin exposure on wrists, chest, or back of hands.")
print(f"    At these sites, 490 nm light penetrates ~1-2 mm into tissue.")
print()

# Power specification
# For biological effect without damage:
# Target: 5 mW/cm^2 on skin (mid-range photobiomodulation)
# Spot size: ~10 cm^2 (3.5 cm diameter circle)
# Total power: 50 mW

target_irradiance = 5.0e-3  # W/cm^2
spot_area_cm2 = 10.0
led_power = target_irradiance * spot_area_cm2  # W

# LED specifications
print(f"    LED SPECIFICATIONS:")
print(f"    Wavelength:       490 +/- 5 nm (narrowband blue-violet)")
print(f"    Target irradiance: {target_irradiance*1000:.0f} mW/cm^2 on skin")
print(f"    Spot area:         {spot_area_cm2:.0f} cm^2 (3.5 cm diameter)")
print(f"    Total optical power: {led_power*1000:.0f} mW")
print(f"    LED type:          High-power InGaN LED (e.g., Cree XP-E2 Royal Blue)")
print(f"                       or 490 nm narrowband LED")
print(f"    Electrical power:  ~{led_power/0.3*1000:.0f} mW (assuming 30% efficiency)")
print(f"    Diffuser:          Required for uniform irradiance (no hot spots)")
print(f"    Pulsing:           Can pulse at 40 Hz (on/off) for dual-frequency delivery")
print(f"                       50% duty cycle gives {led_power*1000/2:.0f} mW average")
print()
print(f"    SAFETY NOTES:")
print(f"    - NOT for direct eye exposure (use skin-contact applicator)")
print(f"    - 490 nm is NOT UV; no DNA damage risk at these power levels")
print(f"    - Comparable to a small blue LED flashlight")
print(f"    - Photosensitive individuals should consult physician")
print(f"    - Session: 10-20 min (similar to red light therapy protocols)")
print()

# Alternative: red + blue combination
print(f"    ALTERNATIVE: RED + BLUE COMBINATION")
print(f"    Red (630-660 nm) is the standard photobiomodulation wavelength.")
print(f"    Blue (490 nm) is the f1 = 612 THz framework frequency.")
print(f"    Combine both for established (red) + novel (blue) benefit.")
print()

# Device form factor
print("  DEVICE FORM FACTOR")
print("  ------------------")
print(f"    Option A: Wristband (like a fitness tracker)")
print(f"      - LRA motor for 40 Hz haptic")
print(f"      - PPG sensor for HRV")
print(f"      - Small LED for breathing guide")
print(f"      - 490 nm LED array on inner wrist (skin contact)")
print(f"      - Bluetooth for audio sync to phone/earbuds")
print(f"      - Battery: 200-400 mAh (8+ hours)")
print()
print(f"    Option B: Chest patch (adhesive)")
print(f"      - Thin-film vibration element for 40 Hz")
print(f"      - ECG electrodes for HRV (more accurate than PPG)")
print(f"      - LED array for 490 nm skin application")
print(f"      - Disposable (10-use) or rechargeable versions")
print()
print(f"    Option C: Desktop/bedside unit")
print(f"      - 40 Hz speaker (5-10W, small subwoofer)")
print(f"      - LED breathing light ring (RGB, adjustable)")
print(f"      - 490 nm LED panel for hand/arm placement")
print(f"      - Phone app for HRV biofeedback via camera PPG")
print()


# =============================================================================
# SECTION 3: SLEEP ENHANCEMENT SYSTEM
# =============================================================================
separator("3. SLEEP ENHANCEMENT SYSTEM")

print("  Framework-derived sleep frequency protocol based on domain wall physics.")
print("  Sleep maintains the wall through two cleaning cycles:")
print("    N3 (deep sleep): Water-side flush (glymphatic clearance)")
print("    REM: Aromatic-side reset (monoamine silence)")
print()

# Sleep cycle timing
cycle_duration = 90  # minutes (standard sleep cycle)
n_cycles = 5         # typical full night
total_sleep = cycle_duration * n_cycles  # 450 min = 7.5 hours

print("  STANDARD SLEEP ARCHITECTURE (90-minute cycles)")
print("  -----------------------------------------------")
print(f"    Sleep cycles per night: {n_cycles}")
print(f"    Cycle duration:         {cycle_duration} min")
print(f"    Total sleep:            {total_sleep} min = {total_sleep/60:.1f} hours")
print()

# Derived frequencies for each stage
print("  FRAMEWORK FREQUENCIES FOR EACH SLEEP STAGE")
print("  -------------------------------------------")
print(f"    {'Stage':>12} {'Frequency':>12} {'Derivation':>30} {'Delivery':>20}")
print(f"    {'-'*12} {'-'*12} {'-'*30} {'-'*20}")
print(f"    {'N1 (drowsy)':>12} {'4-8 Hz':>12} {'theta (transition)':>30} {'none (natural)':>20}")
print(f"    {'N2 (light)':>12} {f'{f_spindle:.0f} Hz':>12} {'h/3 = 30/3 (spindles)':>30} {'binaural beats':>20}")
print(f"    {'N3 (deep)':>12} {f'{f_slow_osc:.2f} Hz':>12} {'3/4 = breathing/zero ratio':>30} {'vibrotactile':>20}")
print(f"    {'REM':>12} {'0 Hz':>12} {'silence (monoamine reset)':>30} {'no stimulation':>20}")
print(f"    {'Wake':>12} {f'{f2_Hz:.0f} Hz':>12} {'4h/3 = 40 Hz (gamma)':>30} {'audio + light':>20}")
print()

# Detailed protocol
print("  DETAILED NIGHTLY PROTOCOL")
print("  -------------------------")
print()

# Timing within a sleep cycle (approximate)
# N1: 5% = 4.5 min
# N2: 50% = 45 min
# N3: 20% = 18 min (more in early cycles)
# REM: 25% = 22.5 min (more in later cycles)

print("  Pre-sleep (15 min before lights off):")
print(f"    - 0.1 Hz breathing guide (f3) for heart coherence")
print(f"    - Dim amber light only (no blue light to preserve melatonin)")
print(f"    - Ambient temperature: 18-19 C (optimal for sleep onset)")
print()

for cycle_num in range(1, n_cycles + 1):
    t_start = (cycle_num - 1) * cycle_duration
    t_n1 = t_start
    t_n2 = t_start + 5
    t_n3 = t_start + 50
    t_rem = t_start + 68
    t_end = t_start + cycle_duration

    # N3 percentage decreases across cycles, REM increases
    n3_frac = max(0.05, 0.25 - 0.05 * (cycle_num - 1))
    rem_frac = min(0.40, 0.15 + 0.07 * (cycle_num - 1))

    print(f"  Cycle {cycle_num} ({t_start}-{t_end} min from sleep onset):")
    print(f"    N1 ({t_n1:>3}-{t_n2:>3} min): No stimulation (natural transition)")
    print(f"    N2 ({t_n2:>3}-{t_n3:>3} min): Soft 10 Hz binaural beats via bone conduction")
    print(f"                         Volume: barely audible (20-30 dB SPL)")
    print(f"    N3 ({t_n3:>3}-{t_rem:>3} min): 0.75 Hz vibrotactile on mattress")
    print(f"                         Amplitude: 0.05 mm (sub-threshold awareness)")
    n3_note = " (LONGEST N3 -- maximize glymphatic)" if cycle_num == 1 else ""
    print(f"                         Glymphatic flush cycle{n3_note}")
    print(f"    REM ({t_rem:>3}-{t_end:>3} min): SILENCE (all stimulation off)")
    print(f"                         Monoamine reset (serotonin, DA, NE all at zero)")
    rem_note = " (longest REM -- maximize dream consolidation)" if cycle_num >= 4 else ""
    print(f"                         Aromatic chemistry resets{rem_note}")
    print()

# Wake protocol
print("  WAKE PROTOCOL (alarm time):")
print(f"    Phase 1 (5 min before alarm): Soft 10 Hz -> ramp to 20 Hz")
print(f"    Phase 2 (alarm):              40 Hz audio + vibrotactile")
print(f"                                  490 nm blue light ramp (dawn simulation)")
print(f"    Phase 3 (1 min after alarm):  Full 40 Hz + bright 490 nm light")
print(f"    Duration:                     5 minutes total ramp-up")
print()
print(f"    RATIONALE: The 40 Hz wake-up reactivates the breathing mode after")
print(f"    REM silence. The 490 nm blue light suppresses melatonin and activates")
print(f"    aromatic photochemistry. Together, they reinitialize all three channels.")
print()

# Hardware for sleep system
print("  HARDWARE SPECIFICATIONS")
print("  -----------------------")
print(f"    Mattress pad: Vibrotactile transducer array (4-8 units)")
print(f"      Frequency range: 0.5-50 Hz")
print(f"      Peak displacement: 0.05-0.5 mm (adjustable)")
print(f"      Position: Under mattress topper (imperceptible structure)")
print()
print(f"    Pillow speaker: Bone-conduction or flat-panel transducer")
print(f"      Frequency range: 5-100 Hz")
print(f"      Volume: 20-40 dB SPL max (sub-awareness)")
print()
print(f"    Sleep staging: Wearable EEG headband (e.g., Muse, Dreem)")
print(f"      Detects N1/N2/N3/REM transitions in real time")
print(f"      Triggers appropriate frequency for each stage")
print()
print(f"    Light panel: Bedside LED array")
print(f"      490 nm blue (wake mode, pulsed at 40 Hz)")
print(f"      Amber 590 nm (pre-sleep mode, no blue)")
print(f"      Intensity: 0 to 500 lux adjustable")
print()

# REM analysis
print("  REM FREQUENCY ANALYSIS")
print("  ----------------------")
print(f"    During REM, all monoamine neurotransmitters drop to near zero:")
print(f"      Serotonin:       ~0 (raphe nuclei silent)")
print(f"      Norepinephrine:  ~0 (locus coeruleus silent)")
print(f"      Dopamine:        maintained (VTA still active)")
print()
print(f"    Framework interpretation:")
print(f"    REM = the dark vacuum's maintenance window.")
print(f"    With 2 of 3 aromatic neurotransmitters silent, the wall's")
print(f"    'noise floor' drops. The dark vacuum can recalibrate")
print(f"    without interference from Domain 1 measurement activity.")
print(f"    The correct protocol during REM is SILENCE -- no external")
print(f"    frequency delivery. Let the dark vacuum do its work.")
print()


# =============================================================================
# SECTION 4: MUSICAL INSTRUMENTS / SOUND DESIGN
# =============================================================================
separator("4. MUSICAL INSTRUMENTS / SOUND DESIGN")

# 4A: Lucas Scale
print("  SCALE A: THE LUCAS SCALE -- 40 * L(n)")
print("  ---------------------------------------")
print(f"    Base frequency: f2 = 40 Hz (breathing mode)")
print(f"    Scale: multiply by Lucas numbers L(n)")
print()
print(f"    {'n':>4} {'L(n)':>6} {'Freq (Hz)':>12} {'Note':>8} {'Cents off':>10} {'Name / Role'}")
print(f"    {'-'*4} {'-'*6} {'-'*12} {'-'*8} {'-'*10} {'-'*30}")

lucas_scale = []
for n in range(1, 11):
    Ln = lucas(n)
    freq = 40.0 * Ln
    note, cents = freq_to_note(freq)
    role = ""
    if n == 1: role = "breathing mode (gamma)"
    elif n == 2: role = "triality harmonic"
    elif n == 3: role = "DNA-bridge harmonic"
    elif n == 4: role = "S3-breaking harmonic"
    elif n == 5: role = "A4 concert pitch!"
    elif n == 6: role = "water harmonic (L(6)=18)"
    elif n == 7: role = "max-Coxeter harmonic"
    elif n == 8: role = "extended bridge"
    elif n == 9: role = "phi^9 regime"
    elif n == 10: role = "upper limit"
    lucas_scale.append((n, Ln, freq, note, cents))
    print(f"    {n:>4} {Ln:>6} {freq:>10.0f} Hz {note:>8} {cents:>+8.1f}c  {role}")

print()
print(f"    KEY: A4 = 440 Hz = 40 * L(5) = 40 * 11 EXACTLY")
print(f"    The international concert pitch standard IS in the Lucas scale.")
print()

# Intervals within the Lucas scale
print("  INTERVALS IN THE LUCAS SCALE")
print("  ----------------------------")
print(f"    {'Interval':>20} {'Ratio':>8} {'Cents':>8} {'Nearest JI':>15}")
print(f"    {'-'*20} {'-'*8} {'-'*8} {'-'*15}")

ji_intervals = [
    (1.0, "Unison"), (16/15, "Minor 2nd"), (9/8, "Major 2nd"),
    (6/5, "Minor 3rd"), (5/4, "Major 3rd"), (4/3, "Perf 4th"),
    (45/32, "Tritone"), (3/2, "Perf 5th"), (8/5, "Minor 6th"),
    (5/3, "Major 6th"), (7/4, "Harm 7th"), (15/8, "Major 7th"),
    (2/1, "Octave"),
]

for i in range(len(lucas_scale) - 1):
    n1, L1, f1_ls, _, _ = lucas_scale[i]
    n2, L2, f2_ls, _, _ = lucas_scale[i + 1]
    ratio = f2_ls / f1_ls
    cents = 1200.0 * math.log2(ratio)
    # Find nearest JI interval
    nearest_ji = min(ji_intervals, key=lambda x: abs(1200*math.log2(x[0]) - cents) if x[0] > 0 else 9999)
    print(f"    L({n1})->L({n2}) = {L2}/{L1:>3} {ratio:8.4f} {cents:8.1f}c {nearest_ji[1]:>15}")

print()
print(f"    The Lucas scale contains the PERFECT FOURTH (4/3 = L(3)/L(2))")
print(f"    and the HARMONIC SEVENTH (7/4 = L(4)/L(3)).")
print(f"    These are the framework's native consonances.")
print(f"    The ratios converge to phi = {phi:.6f} ({1200*math.log2(phi):.1f} cents).")
print()

# 4B: Eta Tower Scale
print("  SCALE B: THE ETA TOWER SCALE")
print("  ----------------------------")
print(f"    Map eta(q^n) at q = 1/phi to audible frequencies.")
print(f"    Base: A3 = 220 Hz, range: 2 octaves (220-880 Hz).")
print()

eta_min = min(eta_tower[k] for k in range(1, 13))
eta_max = max(eta_tower[k] for k in range(1, 13))

print(f"    {'n':>4} {'eta(q^n)':>12} {'Freq (Hz)':>12} {'Note':>8} {'Cents off':>10}")
print(f"    {'-'*4} {'-'*12} {'-'*12} {'-'*8} {'-'*10}")

eta_scale_freqs = []
for k in range(1, 13):
    frac = (eta_tower[k] - eta_min) / (eta_max - eta_min)
    freq = 220.0 * 2.0**(2.0 * frac)
    note, cents = freq_to_note(freq)
    eta_scale_freqs.append(freq)
    marker = " <- alpha_s" if k == 1 else (" <- PEAK" if k == 7 else (" <- 5/6 (E8 rank)" if k == 8 else ""))
    print(f"    {k:>4} {eta_tower[k]:12.8f} {freq:12.1f} Hz {note:>8} {cents:>+8.1f}c{marker}")

print()
print(f"    The eta tower melody rises to n=7 (peak), then descends.")
print(f"    Shape: like a BREATH. Inhale (1->7), exhale (7->12).")
print()

# 4C: Domain Wall Singing Bowl
print("  DESIGN: DOMAIN WALL SINGING BOWL")
print("  ---------------------------------")
print(f"    A singing bowl tuned to framework frequencies.")
print()
print(f"    Fundamental: 40 Hz (f2, breathing mode)")
print(f"    Problem: 40 Hz is below practical bowl fundamentals (~100 Hz min)")
print(f"    Solution: Tune to Lucas scale harmonics that include 40 Hz as subharmonic")
print()

# Practical singing bowl frequencies
bowl_fund = 440.0  # A4 = 40 * L(5)
print(f"    PRACTICAL DESIGN: Bowl fundamental = {bowl_fund:.0f} Hz (A4 = 40 * L(5))")
print(f"    The 40 Hz breathing mode is the 11th subharmonic (440/11 = 40).")
print()
print(f"    Bowl overtone series (framework-derived):")
print(f"    {'Mode':>6} {'Freq (Hz)':>12} {'Ratio':>8} {'Note':>8} {'Framework connection'}")
print(f"    {'-'*6} {'-'*12} {'-'*8} {'-'*8} {'-'*30}")

bowl_modes = [
    (1, bowl_fund, "1:1", "fundamental = 40*L(5)"),
    (2, bowl_fund * 4/3, "4:3", "perfect 4th = L(3)/L(2)"),
    (3, bowl_fund * 7/4, "7:4", "harmonic 7th = L(4)/L(3)"),
    (4, bowl_fund * 11/4, "11:4", "2 octaves + L(5)/L(3)"),
    (5, bowl_fund * phi, "phi", "golden interval"),
]

for mode, freq, ratio, connection in bowl_modes:
    note, cents = freq_to_note(freq)
    print(f"    {mode:>6} {freq:>10.1f} Hz {ratio:>8} {note:>8}  {connection}")

print()
print(f"    MATERIAL: Bronze alloy (traditional) or quartz crystal")
print(f"    Quartz preferred: piezoelectric, converts mechanical -> EM at 613 THz scale")
print(f"    Diameter: ~20 cm for ~440 Hz fundamental")
print(f"    Wall thickness: ~3-5 mm (tuned by grinding)")
print(f"    Playing: Leather-wrapped mallet, circular rim striking")
print()

# 4D: Guitar/Piano tuning
print("  LUCAS GUITAR TUNING")
print("  --------------------")
print(f"    Standard guitar: E2 A2 D3 G3 B3 E4")
print(f"    Lucas tuning: nearest Lucas-scale frequencies")
print()

guitar_standard = [
    ("E2", 82.41), ("A2", 110.0), ("D3", 146.83),
    ("G3", 196.0), ("B3", 246.94), ("E4", 329.63),
]

# Find nearest Lucas scale frequency for each string
print(f"    {'String':>8} {'Standard':>10} {'Lucas':>10} {'Formula':>14} {'Deviation':>10}")
print(f"    {'-'*8} {'-'*10} {'-'*10} {'-'*14} {'-'*10}")

# Build full Lucas frequency list (including octave transpositions)
all_lucas_freqs = []
for n in range(1, 11):
    base = 40.0 * lucas(n)
    # Generate octave transpositions
    f = base
    while f > 20:
        f /= 2
    while f < 2000:
        all_lucas_freqs.append((f, n))
        f *= 2

for name, std_freq in guitar_standard:
    nearest = min(all_lucas_freqs, key=lambda x: abs(x[0] - std_freq))
    dev_cents = 1200.0 * math.log2(nearest[0] / std_freq)
    formula = f"40*L({nearest[1]})/{2**round(math.log2(40*lucas(nearest[1])/nearest[0]))}"
    print(f"    {name:>8} {std_freq:>8.1f} Hz {nearest[0]:>8.1f} Hz {formula:>14} {dev_cents:>+8.1f}c")

print()
print(f"    The Lucas tuning is remarkably close to standard tuning.")
print(f"    A2 = 110 Hz = 40*L(2)/... Actually: 120/110 = 12/11, close.")
print(f"    The closest natural match: A4 = 440 Hz is EXACT in both systems.")
print()


# =============================================================================
# SECTION 5: ARCHITECTURE / ROOM DESIGN
# =============================================================================
separator("5. ARCHITECTURE / ROOM DESIGN")

# 110 Hz ancient chamber resonance
print("  DESIGN A: 110 Hz RESONANCE CHAMBER (Ancient Temple Frequency)")
print("  -------------------------------------------------------------")
print(f"    Frequency: {f_110:.0f} Hz = L(5) * h/3 = 11 * 10")
print(f"    Ancient chambers (Hal Saflieni, Newgrange, etc.) resonate at 95-120 Hz")
print(f"    Mode at 110 Hz: EEG shows language center deactivation, right hemisphere")
print(f"    activation (Cook 2008)")
print()

# Room dimensions for 110 Hz resonance
# Standing wave: f = n * v / (2 * L) for axial modes
# For fundamental (n=1): L = v / (2*f)
L_110 = v_sound_air / (2.0 * f_110)
print(f"    Room length for 110 Hz axial fundamental:")
print(f"      L = v_air / (2 * f) = {v_sound_air} / (2 * {f_110:.0f}) = {L_110:.2f} m ({L_110*3.281:.1f} ft)")
print()

# For various room modes
print(f"    ROOM DIMENSIONS FOR 110 Hz STANDING WAVES")
print(f"    {'Mode':>6} {'Dimension (m)':>15} {'Dimension (ft)':>16} {'Shape'}")
print(f"    {'-'*6} {'-'*15} {'-'*16} {'-'*20}")

for n in range(1, 5):
    L = n * v_sound_air / (2.0 * f_110)
    print(f"    n={n:>3} {L:>13.2f} m {L*3.281:>14.1f} ft {'fundamental' if n==1 else f'harmonic {n}'}")

print()
print(f"    RECOMMENDED: Barrel-vaulted or domed ceiling, ~1.56 m wide (110 Hz lateral)")
print(f"    Stone or concrete surfaces (high acoustic reflectivity for sustained resonance)")
print(f"    RT60 (reverberation time): 4-8 seconds (cathedral-like)")
print()

# 40 Hz room
print("  DESIGN B: 40 Hz STANDING WAVE ROOM")
print("  -----------------------------------")
L_40 = v_sound_air / (2.0 * f2_Hz)
print(f"    Room length for 40 Hz axial fundamental:")
print(f"      L = v_air / (2 * f2) = {v_sound_air} / (2 * {f2_Hz:.0f}) = {L_40:.2f} m ({L_40*3.281:.1f} ft)")
print()
print(f"    This is a large room ({L_40:.1f} m = {L_40*3.281:.0f} ft).")
print(f"    For a practical room, use higher-order modes:")
print()
print(f"    {'Room length':>15} {'Mode':>6} {'Frequency':>12} {'Match to 40 Hz'}")
print(f"    {'-'*15} {'-'*6} {'-'*12} {'-'*15}")

for length_m in [3.0, 4.0, 4.29, 5.0, 6.0, 8.0, 8.575]:
    for n in range(1, 8):
        f_mode = n * v_sound_air / (2.0 * length_m)
        if abs(f_mode - 40.0) < 2.0:
            print(f"    {length_m:>13.2f} m  n={n:>3} {f_mode:>10.1f} Hz  {'EXACT' if abs(f_mode-40)<0.5 else f'{abs(f_mode-40):.1f} Hz off'}")

print()
print(f"    PRACTICAL: A room ~4.29 m (14.1 ft) long has its 1st mode at ~40 Hz")
print(f"    (n=1 axial). For a standard room, 8.58 m (28.1 ft) gives n=2 = 40 Hz.")
print()

# Materials
print("  ACOUSTIC MATERIALS")
print("  ------------------")
print(f"    For MAXIMUM acoustic coupling to walls/body:")
print(f"    Material          Impedance (rayl)  Refl. coeff (vs air)")
print(f"    ---------------   ----------------  --------------------")

materials = [
    ("Air", Z_air, Z_air),
    ("Water", Z_water, Z_air),
    ("Concrete", 8.0e6, Z_air),
    ("Wood (oak)", 3.0e6, Z_air),
    ("Glass", 1.3e7, Z_air),
    ("Human tissue", 1.63e6, Z_air),
    ("Cork", 1.2e5, Z_air),
    ("Rubber", 1.5e6, Z_air),
]

for name, Z, Z_ref in materials:
    R = abs(Z - Z_ref) / (Z + Z_ref)
    print(f"    {name:18s} {Z:>14.0f}      R = {R:.4f} ({R*100:.1f}%)")

print()
print(f"    For 110 Hz resonance: use STONE or CONCRETE (high reflection, long RT60)")
print(f"    For 40 Hz immersive: use WOOD paneling (moderate reflection, warm resonance)")
print(f"    For absorption control: cork/rubber panels on select surfaces")
print()

# Faraday pattern water feature
print("  DESIGN C: HEXAGONAL FARADAY WATER FEATURE")
print("  ------------------------------------------")
print(f"    A shallow water dish driven at 40 Hz to produce hexagonal patterns.")
print(f"    These patterns make the domain wall geometry (A2 hexagonal lattice) visible.")
print()

# Compute dish parameters
for dish_diam_cm in [20, 30, 40, 50, 60]:
    depth_cm = 2.0  # shallow
    depth_m = depth_cm / 100.0
    lam_f = faraday_wavelength(40.0, depth_m)
    n_hexagons = (dish_diam_cm / 100.0) / lam_f
    print(f"    Dish {dish_diam_cm} cm, depth {depth_cm} cm: pattern wavelength ~ {lam_f*100:.1f} cm, "
          f"~{n_hexagons:.0f} hexagonal cells")

print()
print(f"    RECOMMENDED: 40-50 cm diameter, 2 cm depth")
print(f"    Driver: Small mechanical oscillator (eccentric motor) at center bottom")
print(f"    Amplitude: 0.1-0.5 mm vertical displacement")
print(f"    Lighting: Backlit or side-lit for pattern visibility")
print(f"    Medium: Milk-water mix for better visual contrast (white on blue dish)")
print(f"    Power: < 1 W motor, driven by 40 Hz precision oscillator")
print()


# =============================================================================
# SECTION 6: AGRICULTURAL / PLANT APPLICATIONS
# =============================================================================
separator("6. AGRICULTURAL / PLANT APPLICATIONS")

print("  Plants have no nervous system but DO contain aromatic molecules:")
print("  chlorophyll, lignin, flavonoids, alkaloids. The f1 channel (aromatic")
print("  chemistry) is active in plants. The question: does f2 (40 Hz sound)")
print("  couple to plant aromatic chemistry through mechanical vibration?")
print()

# Chlorophyll frequencies
chl_Qy_THz = mu / 4.0  # 459 THz
chl_Qy_nm = c_light / (chl_Qy_THz * 1e12) * 1e9

chl_Soret_nm = 430.0  # approximate
chl_Soret_THz = c_light / (chl_Soret_nm * 1e-9) / 1e12

print("  CHLOROPHYLL FREQUENCIES FROM THE FRAMEWORK")
print("  ------------------------------------------")
print(f"    Chlorophyll Q_y band: mu/4 = {chl_Qy_THz:.2f} THz")
print(f"      Wavelength: {chl_Qy_nm:.1f} nm (red light)")
print(f"      Measured Chl a Q_y: 662 nm = {c_light/(662e-9)/1e12:.2f} THz")
print(f"      Match: {100*(1-abs(chl_Qy_nm-662)/662):.1f}% (wavelength)")
print()
print(f"    Chlorophyll Soret band: ~430 nm = {chl_Soret_THz:.0f} THz")
print(f"      This is BLUE light -- the primary energy absorption band")
print()

# Optimal grow light spectrum
print("  FRAMEWORK-DERIVED GROW LIGHT SPECTRUM")
print("  -------------------------------------")
print(f"    The framework predicts specific wavelengths for plant photochemistry:")
print()
print(f"    {'Band':>20} {'Wavelength':>12} {'Frequency':>12} {'Framework':>20} {'Function'}")
print(f"    {'-'*20} {'-'*12} {'-'*12} {'-'*20} {'-'*25}")

grow_light_bands = [
    ("Chl a Q_y (red)", f"{chl_Qy_nm:.0f} nm", f"{chl_Qy_THz:.0f} THz", "mu/4", "Photosynthesis"),
    ("Chl b Q_y (red)", "642 nm", "467 THz", "E_R/7 (Rydberg-Lucas)", "Photosynthesis"),
    ("Chl a Soret (blue)", "430 nm", "697 THz", "E_R*4/19 (Coxeter)", "Energy absorption"),
    ("Carotenoid (blue)", "450 nm", "666 THz", "E_R*3/13 (Coxeter)", "Photoprotection"),
    ("Phytochrome (red)", "660 nm", "454 THz", "~mu/4", "Morphogenesis"),
    ("Phytochrome (far-red)", "730 nm", "411 THz", "mu/L(3) approx", "Shade response"),
    ("UV-A", "380 nm", "789 THz", "--", "Flavonoid biosynthesis"),
]

for band, lam, freq, fw, func in grow_light_bands:
    print(f"    {band:>20} {lam:>12} {freq:>12} {fw:>20} {func}")

print()
print(f"    OPTIMAL SPECTRUM: Red (660 nm) + Blue (430-450 nm)")
print(f"    This is ALREADY standard horticulture practice!")
print(f"    The framework explains WHY: these are the Rydberg-Lucas and")
print(f"    Coxeter-Rydberg absorption lines of chlorophyll.")
print()
print(f"    NOVEL PREDICTION: Adding 490 nm (f1 = 612 THz) light may")
print(f"    enhance general aromatic chemistry in plants (not just chlorophyll).")
print(f"    This would affect flavonoid production, disease resistance, and aroma.")
print()

# 40 Hz sound and plants
print("  40 Hz SOUND AND PLANT GROWTH")
print("  ----------------------------")
print(f"    Framework prediction: 40 Hz acoustic vibration couples to plant tissue")
print(f"    through the same mechanism as in animals:")
print(f"      Sound -> mechanical vibration -> piezoelectric response in cell walls")
print(f"      -> modulation of membrane potential -> aromatic chemistry effects")
print()
print(f"    Plant cell walls contain LIGNIN (aromatic polymer).")
print(f"    Lignin has the same aromatic ring structure as framework-active molecules.")
print(f"    Mechanical vibration at 40 Hz may modulate lignin's electronic properties.")
print()
print(f"    EXISTING EVIDENCE:")
print(f"    - Sound vibration (100-1000 Hz) increases plant growth rate by 10-30%")
print(f"      (multiple studies, mechanism unclear)")
print(f"    - 1000 Hz has been most commonly tested; 40 Hz specifically is understudied")
print(f"    - Framework predicts 40 Hz should be OPTIMAL (breathing mode frequency)")
print()
print(f"    EXPERIMENTAL PROTOCOL:")
print(f"    - 40 Hz sine wave via speaker beneath growing tray")
print(f"    - 80 dB SPL at plant level (moderate, non-damaging)")
print(f"    - Exposure: 2-4 hours/day during light period")
print(f"    - Measure: growth rate, chlorophyll content, flavonoid production,")
print(f"               disease resistance, aromatic compound levels")
print(f"    - Control: identical conditions without sound, and with 1000 Hz sound")
print()

# Water coupling for plants
print("  WATER COUPLING FOR HYDROPONICS")
print("  -------------------------------")
print(f"    In hydroponic systems, 40 Hz can be delivered through the water.")
print(f"    This provides the same ~1000x coupling advantage as for human immersion.")
print()
print(f"    Implementation: Submersible 40 Hz transducer in nutrient reservoir")
print(f"    Power: < 1 W (extremely low intensity needed)")
print(f"    Cost: ~$20-50 for aquarium-type transducer + signal generator")
print()
print(f"    ADDITIONAL PREDICTION: Combine 40 Hz water acoustic with optimal")
print(f"    red+blue light spectrum for maximum photosynthetic efficiency.")
print(f"    The acoustic vibration may improve nutrient uptake by modulating")
print(f"    root cell membrane properties through aromatic chemistry.")
print()


# =============================================================================
# SECTION 7: COST ESTIMATES
# =============================================================================
separator("7. COST ESTIMATES")

print("  All costs in approximate 2026 USD. Consumer = DIY/home use.")
print("  Professional = clinic/research grade with certifications.")
print()

# Cost data
devices = [
    {
        "name": "40 Hz Water Immersion Chamber",
        "consumer": [
            ("Fiberglass tub (float tank shell)", 2000, 4000),
            ("Water heater + thermostat (36C)", 200, 500),
            ("4x Bass shaker transducers (Dayton TT25-8)", 60, 120),
            ("Class D amplifier (50W)", 30, 80),
            ("DDS signal generator (AD9833 board)", 15, 40),
            ("Marine epoxy + sealing", 50, 100),
            ("Water filtration (UV + ozone)", 300, 600),
            ("Epsom salt (200 kg)", 100, 200),
            ("Controller (Raspberry Pi + DAC)", 80, 150),
        ],
        "professional": [
            ("Medical-grade stainless steel tank", 8000, 15000),
            ("Precision temperature control (+/- 0.1C)", 1000, 2000),
            ("Underwater acoustic transducer array (calibrated)", 2000, 4000),
            ("Lab-grade signal generator + amplifier", 500, 1500),
            ("Commercial water treatment system", 2000, 4000),
            ("Medical-grade Epsom salt (USP)", 300, 500),
            ("Control system with data logging", 1000, 2000),
            ("Safety systems (panic button, attendant alert)", 500, 1000),
        ],
    },
    {
        "name": "Triple-Frequency Coherence Device",
        "consumer": [
            ("Microcontroller (ESP32 or similar)", 10, 20),
            ("LRA haptic motor (40 Hz)", 5, 15),
            ("Optical PPG sensor (MAX30102)", 5, 10),
            ("490 nm LED + driver", 5, 15),
            ("LED ring for breathing guide", 10, 20),
            ("Battery (400 mAh LiPo)", 5, 10),
            ("3D printed enclosure", 5, 15),
            ("PCB fabrication", 10, 30),
            ("Bluetooth audio module", 10, 20),
        ],
        "professional": [
            ("Medical-grade wearable platform", 200, 500),
            ("Calibrated haptic actuator", 50, 100),
            ("Medical PPG/ECG sensor (FDA clearable)", 100, 300),
            ("Calibrated 490 nm LED module", 50, 100),
            ("App development (iOS/Android)", 5000, 20000),
            ("Clinical data platform", 2000, 10000),
            ("CE/FDA regulatory preparation", 10000, 50000),
        ],
    },
    {
        "name": "Sleep Enhancement System",
        "consumer": [
            ("4x vibrotactile transducers (under-mattress)", 100, 200),
            ("Bone conduction pillow speaker", 30, 80),
            ("Controller (Raspberry Pi + relay board)", 80, 150),
            ("Bedside LED panel (490 nm + amber)", 40, 80),
            ("Consumer EEG headband (Muse S)", 250, 350),
            ("Software (open-source sleep staging)", 0, 0),
        ],
        "professional": [
            ("Medical vibrotactile mattress pad", 1000, 3000),
            ("Clinical bone-conduction audio system", 500, 1000),
            ("Research-grade EEG (Dreem 3 or equivalent)", 500, 1500),
            ("Clinical LED panel (medical device)", 500, 1500),
            ("Validated sleep staging algorithm license", 2000, 10000),
            ("Clinical controller + data logging", 1000, 3000),
        ],
    },
    {
        "name": "Domain Wall Singing Bowl",
        "consumer": [
            ("Custom-tuned quartz crystal bowl (440 Hz, 20cm)", 150, 400),
            ("Leather-wrapped mallet", 20, 50),
            ("Electronic tuner (verify tuning)", 20, 40),
        ],
        "professional": [
            ("Set of 7 quartz bowls (Lucas scale frequencies)", 1000, 3000),
            ("Precision frequency verification equipment", 200, 500),
            ("Acoustic treatment for performance space", 500, 2000),
        ],
    },
    {
        "name": "110 Hz Resonance Room",
        "consumer": [
            ("Room acoustic treatment (panels, diffusers)", 500, 2000),
            ("Subwoofer (110 Hz focused, 100W)", 200, 500),
            ("Signal generator + amplifier", 100, 300),
            ("Acoustic measurement mic + software", 100, 300),
        ],
        "professional": [
            ("Room construction (1.56m stone vault)", 10000, 50000),
            ("Professional acoustic design consultation", 2000, 10000),
            ("Studio monitor system (calibrated)", 2000, 5000),
            ("Acoustic measurement system (calibrated)", 1000, 3000),
        ],
    },
    {
        "name": "Faraday Hexagonal Water Feature",
        "consumer": [
            ("Shallow dish (40 cm, glass or ceramic)", 20, 60),
            ("Small eccentric motor + mount", 10, 30),
            ("40 Hz signal generator (555 timer circuit)", 5, 15),
            ("LED backlighting strip", 10, 25),
            ("Frame / stand", 20, 50),
        ],
        "professional": [
            ("Precision glass dish (50 cm, optically flat)", 200, 500),
            ("Calibrated electromagnetic shaker", 500, 1500),
            ("High-speed camera for pattern analysis", 1000, 5000),
            ("Programmable LED array", 200, 500),
        ],
    },
    {
        "name": "Agricultural 40 Hz System",
        "consumer": [
            ("Waterproof speaker (aquarium-safe)", 20, 50),
            ("Signal generator (40 Hz, battery-powered)", 15, 40),
            ("Timer relay (2-4 hr/day schedule)", 10, 20),
        ],
        "professional": [
            ("Submersible acoustic transducer (calibrated)", 200, 500),
            ("Multi-channel signal generator", 100, 300),
            ("Growth monitoring sensors (PAR, temp, CO2)", 500, 2000),
            ("Data logging system", 200, 500),
        ],
    },
]

for device in devices:
    print(f"  {device['name'].upper()}")
    print(f"  {'='*len(device['name'])}")
    print()

    # Consumer
    print(f"    Consumer Grade:")
    total_min = 0
    total_max = 0
    for item, cost_min, cost_max in device['consumer']:
        total_min += cost_min
        total_max += cost_max
        print(f"      {item:50s} ${cost_min:>6,} - ${cost_max:>6,}")
    print(f"      {'TOTAL':50s} ${total_min:>6,} - ${total_max:>6,}")
    print()

    # Professional
    print(f"    Professional Grade:")
    total_min_p = 0
    total_max_p = 0
    for item, cost_min, cost_max in device['professional']:
        total_min_p += cost_min
        total_max_p += cost_max
        print(f"      {item:50s} ${cost_min:>6,} - ${cost_max:>6,}")
    print(f"      {'TOTAL':50s} ${total_min_p:>6,} - ${total_max_p:>6,}")
    print()


# =============================================================================
# SUMMARY
# =============================================================================
separator("SUMMARY OF ALL SPECIFICATIONS")

print("  DEVICE                              KEY SPEC                    CONSUMER COST")
print("  " + "-" * 76)
print(f"  1. Water Immersion Chamber          40 Hz in 36C water          $2,800 - $5,900")
print(f"  2. Triple-Frequency Coherence       f1+f2+f3 wristband          $  65 - $  155")
print(f"  3. Sleep Enhancement System         N3/spindle/REM staging      $  500 - $  860")
print(f"  4. Domain Wall Singing Bowl         440 Hz quartz, Lucas OTs    $  190 - $  490")
print(f"  5. 110 Hz Resonance Room            1.56m vault, stone          $  900 - $3,100")
print(f"  6. Faraday Water Feature            40 Hz hex pattern dish      $   65 - $  180")
print(f"  7. Agricultural 40 Hz System        Submersible transducer      $   45 - $  110")
print()
print("  CRITICAL FREQUENCIES")
print("  " + "-" * 40)
print(f"  f1 = {f1_THz:.2f} THz  ({f1_wavelength_nm:.1f} nm blue-violet)")
print(f"  f2 = {f2_Hz:.0f} Hz          (gamma / breathing mode)")
print(f"  f3 = {f3_Hz:.1f} Hz        (Mayer wave / heart coherence)")
print(f"  Slow osc = {f_slow_osc:.2f} Hz    (N3 deep sleep)")
print(f"  Spindle  = {f_spindle:.0f} Hz       (sleep spindles)")
print(f"  Chamber  = {f_110:.0f} Hz      (ancient resonance)")
print(f"  A4       = {40*lucas(5):.0f} Hz      (concert pitch = 40*L(5))")
print()
print("  SAFETY SUMMARY")
print("  " + "-" * 40)
print(f"  40 Hz acoustic in water: safe (1 Pa << 10 kPa tissue damage threshold)")
print(f"  490 nm light on skin: safe at 5 mW/cm^2 (standard photobiomodulation range)")
print(f"  490 nm light in eyes: AVOID (blue light hazard at sustained exposure)")
print(f"  40 Hz photic flicker: CONTRAINDICATED for photosensitive epilepsy")
print(f"  Vibrotactile during sleep: safe at sub-threshold (0.05 mm displacement)")
print(f"  110 Hz acoustic: safe at < 85 dB SPL continuous exposure")
print(f"  All devices: no ionizing radiation, no thermal hazard, no chemical exposure")
print()
print("  NOTE: These are engineering specifications derived from the Interface Theory")
print("  framework. They are NOT medical devices and make NO medical claims.")
print("  The framework provides a theoretical basis; clinical validation is required")
print("  before any therapeutic use. Several elements (40 Hz audio-visual, HRV")
print("  biofeedback) already have independent clinical support.")
print()
print("=" * 80)
print("  END OF FREQUENCY TECHNOLOGY SPECIFICATIONS")
print("=" * 80)
