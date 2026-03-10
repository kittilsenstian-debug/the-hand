#!/usr/bin/env python3
"""
cross_scale_frequency.py -- Cross-scale test of the PT frequency formula
=========================================================================

Formula under test:
    f = alpha^(11/4) * phi * g(n) * f_base

where g(n) = n^2 / sqrt(2n - 1) is the PT binding/breathing ratio for
Poeschl-Teller depth parameter n.

For the BIOLOGICAL scale (n=2, f_base = f_electron):
    f = alpha^(11/4) * phi * 4/sqrt(3) * f_electron = 613.86 THz
    Target: 613 +/- 8 THz (Craddock 2017)  -->  99.86% match

QUESTION: Does this formula produce meaningful frequencies at OTHER scales
where the framework claims domain wall consciousness exists?

IMPORTANT NOTE on the g(n) function:
-------------------------------------
The user stated g(n) = n^2 / sqrt(n^2 - 1).  The PT-BINDING-BREATHING-RATIO.md
document derives g(n) = n^2 / sqrt(2n - 1).  These AGREE at n=2 (both give
4/sqrt(3) = 2.309) but DISAGREE for n != 2.  The correct PT spectrum gives:
  |E_0| = n^2,  |E_1| = (n-1)^2,  omega_1 = sqrt(|E_0| - |E_1|) = sqrt(2n-1)
So g(n) = n^2 / sqrt(2n-1) is the physically correct generalization.

We test BOTH versions below for completeness.

Author: Interface Theory project
Date: 2026-02-25
"""

import math

# =============================================================================
# CONSTANTS (NIST 2022 CODATA)
# =============================================================================
c       = 2.99792458e8        # m/s
h_pl    = 6.62607015e-34      # J s
hbar    = 1.054571817e-34     # J s
m_e     = 9.1093837015e-31    # kg
m_p     = 1.67262192369e-27   # kg
e_ch    = 1.602176634e-19     # C
eps0    = 8.8541878128e-12    # F/m
k_B     = 1.380649e-23        # J/K
G_N     = 6.67430e-11         # m^3 kg^-1 s^-2

alpha   = 7.2973525693e-3     # fine structure constant
mu      = m_p / m_e           # 1836.15267...
phi     = (1 + math.sqrt(5)) / 2  # golden ratio = 1.6180339887...

# Derived frequencies
f_electron = m_e * c**2 / h_pl     # electron rest-mass frequency ~1.236e20 Hz
f_Rydberg  = alpha**2 * f_electron / 2  # Rydberg frequency ~3.290e15 Hz
f_Planck   = math.sqrt(c**5 / (hbar * G_N)) / (2 * math.pi)  # Planck frequency

# Modular form values at q = 1/phi (from framework)
eta_q  = 0.11840
theta4 = 0.03031

SEP  = "=" * 80
DASH = "-" * 80

# =============================================================================
# PT BINDING/BREATHING RATIO FUNCTIONS
# =============================================================================
def g_correct(n):
    """Correct PT ratio: n^2 / sqrt(2n - 1).
    From E_j = -(n-j)^2:  |E_0| = n^2,  omega_1 = sqrt(2n-1)."""
    if n < 1:
        return float('nan')
    return n**2 / math.sqrt(2*n - 1)

def g_user(n):
    """User-stated ratio: n^2 / sqrt(n^2 - 1).
    Agrees with g_correct at n=2 but differs elsewhere."""
    if n <= 1:
        return float('nan')
    return n**2 / math.sqrt(n**2 - 1)

def formula(f_base, n, version='correct'):
    """The frequency formula: f = alpha^(11/4) * phi * g(n) * f_base"""
    g = g_correct(n) if version == 'correct' else g_user(n)
    return alpha**(11.0/4.0) * phi * g * f_base

def match_pct(predicted, measured):
    """Percentage match: 100 * (1 - |pred - meas| / meas)"""
    if measured == 0:
        return float('nan')
    return 100 * (1 - abs(predicted - measured) / abs(measured))

def find_best_n(f_base, f_target, n_range=range(1, 101), version='correct'):
    """Find integer n that best matches the target frequency."""
    best_n = 1
    best_match = -1e30
    for n in n_range:
        f_pred = formula(f_base, n, version)
        m = match_pct(f_pred, f_target)
        if not math.isnan(m) and m > best_match:
            best_match = m
            best_n = n
    return best_n, best_match, formula(f_base, best_n, version)

def find_best_n_float(f_base, f_target, version='correct'):
    """Find real-valued n that would match the target frequency exactly.
    f = alpha^(11/4) * phi * n^2 / sqrt(2n-1) * f_base = f_target
    => n^2 / sqrt(2n-1) = f_target / (alpha^(11/4) * phi * f_base)
    Solve numerically."""
    target_ratio = f_target / (alpha**(11.0/4.0) * phi * f_base)
    # Binary search
    lo, hi = 0.5, 1e10
    for _ in range(200):
        mid = (lo + hi) / 2
        if version == 'correct':
            val = mid**2 / math.sqrt(2*mid - 1) if mid > 0.5 else 0
        else:
            val = mid**2 / math.sqrt(mid**2 - 1) if mid > 1 else 0
        if val < target_ratio:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


# =============================================================================
# HELPER: Express frequency in human-readable units
# =============================================================================
def freq_str(f_hz):
    """Format frequency in most natural units."""
    if f_hz is None or f_hz <= 0 or math.isnan(f_hz) or math.isinf(f_hz):
        return "N/A"
    if f_hz < 1e-9:
        return f"{f_hz:.4e} Hz"
    if f_hz < 1e-6:
        return f"{f_hz*1e9:.4f} nHz"
    elif f_hz < 1e-3:
        return f"{f_hz*1e6:.4f} uHz"
    elif f_hz < 1:
        return f"{f_hz*1e3:.4f} mHz"
    elif f_hz < 1e3:
        return f"{f_hz:.4f} Hz"
    elif f_hz < 1e6:
        return f"{f_hz/1e3:.4f} kHz"
    elif f_hz < 1e9:
        return f"{f_hz/1e6:.4f} MHz"
    elif f_hz < 1e12:
        return f"{f_hz/1e9:.4f} GHz"
    elif f_hz < 1e15:
        return f"{f_hz/1e12:.4f} THz"
    elif f_hz < 1e18:
        return f"{f_hz/1e15:.4f} PHz"
    else:
        return f"{f_hz:.4e} Hz"


# =============================================================================
# MAIN ANALYSIS
# =============================================================================
print(SEP)
print("CROSS-SCALE FREQUENCY TEST")
print("Formula: f = alpha^(11/4) * phi * g(n) * f_base")
print("where g(n) = n^2 / sqrt(2n-1) [correct PT]  or  n^2/sqrt(n^2-1) [user]")
print(SEP)
print()

# Core constants
print(f"alpha        = {alpha:.10e}  (1/{1/alpha:.6f})")
print(f"phi          = {phi:.10f}")
print(f"mu           = {mu:.8f}")
print(f"alpha^(11/4) = {alpha**(11/4):.10e}")
print(f"phi * alpha^(11/4) = {phi * alpha**(11/4):.10e}")
print(f"f_electron   = {f_electron:.6e} Hz")
print(f"f_Rydberg    = {f_Rydberg:.6e} Hz")
print(f"f_Planck     = {f_Planck:.6e} Hz")
print()
print(f"Core identity check: alpha^(3/2) * mu * phi^2 = {alpha**1.5 * mu * phi**2:.6f} (target: 3)")
print()

# PT ratio table
print(DASH)
print("PT binding/breathing ratio g(n) for n = 1..10")
print(DASH)
print(f"{'n':>4}  {'g_correct':>12}  {'g_user':>12}  {'agree?':>8}")
for n in range(1, 11):
    gc = g_correct(n)
    gu = g_user(n) if n > 1 else float('nan')
    agree = "YES" if (n == 2) else ("n/a" if n == 1 else "NO")
    print(f"{n:4d}  {gc:12.6f}  {gu:12.6f}  {agree:>8}")
print()
print("NOTE: g_correct and g_user ONLY agree at n=2.")
print("      g_correct = n^2/sqrt(2n-1) is the physically derived PT formula.")
print("      g_user    = n^2/sqrt(n^2-1) coincidentally matches at n=2.")
print()


# =========================================================================
# SCALE 1: BIOLOGICAL  (water + aromatics, f_base = f_electron)
# =========================================================================
print(SEP)
print("SCALE 1: BIOLOGICAL (water + aromatics)")
print(f"  f_base = f_electron = {freq_str(f_electron)}")
print(SEP)

f_craddock = 613e12  # Hz (Craddock 2017, aromatic consciousness mode)
f_bio_n2 = formula(f_electron, 2)

print(f"\n  Formula (n=2): {freq_str(f_bio_n2)}")
print(f"  Target:        {freq_str(f_craddock)} +/- 8 THz (Craddock 2017)")
print(f"  Match:         {match_pct(f_bio_n2, f_craddock):.2f}%")
print(f"  Within error:  {'YES' if abs(f_bio_n2 - f_craddock) < 8e12 else 'NO'}")
print()

# What other n values give
print("  Other PT depths with f_base = f_electron:")
print(f"  {'n':>4}  {'f (THz)':>12}  {'Nearest known':>30}  {'Match':>8}")
known_bio = [
    (102e12, "O-H stretch (~102 THz)"),
    (180e12, "C=O stretch (~180 THz)"),
    (400e12, "UV-A edge (~400 THz)"),
    (613e12, "Craddock aromatic (613 THz)"),
    (750e12, "UV edge (~750 THz)"),
    (1050e12, "Trp UV abs (~1050 THz)"),
]

for n in range(1, 11):
    f_pred = formula(f_electron, n)
    # Find nearest known frequency
    nearest = min(known_bio, key=lambda x: abs(x[0] - f_pred))
    m = match_pct(f_pred, nearest[0])
    marker = " <-- MATCH" if m > 99 else (" <-- close" if m > 95 else "")
    print(f"  {n:4d}  {f_pred/1e12:12.2f}  {nearest[1]:>30}  {m:7.2f}%{marker}")
print()


# =========================================================================
# SCALE 2: CELLULAR (cell division and mitotic oscillators)
# =========================================================================
print(SEP)
print("SCALE 2: CELLULAR")
print(SEP)

f_cell_div = 1.0 / (24 * 3600)        # ~24 hours cell cycle
f_mitotic  = 1.0 / (30 * 60)           # ~30 min mitotic oscillator
f_calcium  = 0.01                       # ~0.01-1 Hz calcium oscillations

print(f"\n  Known cellular frequencies:")
print(f"    Cell division cycle:      {freq_str(f_cell_div)} (~24 hr)")
print(f"    Mitotic oscillator:       {freq_str(f_mitotic)} (~30 min)")
print(f"    Calcium oscillations:     {freq_str(f_calcium)} (~10 mHz to 1 Hz)")
print()

# Can ANY base frequency + integer n produce these?
# For f_electron as base, what n would be needed?
n_cell_div = find_best_n_float(f_electron, f_cell_div)
n_mitotic  = find_best_n_float(f_electron, f_mitotic)
n_calcium  = find_best_n_float(f_electron, f_calcium)

print(f"  If f_base = f_electron:")
print(f"    Cell division would need n = {n_cell_div:.1e}  (absurdly large)")
print(f"    Mitotic oscillator needs n = {n_mitotic:.1e}  (absurdly large)")
print(f"    Calcium oscillation needs n = {n_calcium:.1e}  (absurdly large)")
print()
print("  VERDICT: Formula with f_base = f_electron cannot reach cellular")
print("  timescales for any reasonable n. The formula is specific to the")
print("  molecular electronic energy scale, not to slow biological clocks.")
print()

# Try: what if f_base is the thermal frequency kT/h at body temp?
f_thermal = k_B * 310 / h_pl   # ~6.45e12 Hz = 6.45 THz
print(f"  Alternative: f_base = kT_body/h = {freq_str(f_thermal)} ({f_thermal/1e12:.2f} THz)")
for n in range(1, 6):
    f_pred = formula(f_thermal, n)
    print(f"    n={n}: {freq_str(f_pred)}")
print("  Still far above cellular frequencies.")
print()


# =========================================================================
# SCALE 3: NEURAL (EEG bands)
# =========================================================================
print(SEP)
print("SCALE 3: NEURAL (EEG bands)")
print(SEP)

eeg_bands = {
    'delta':  (1, 4),
    'theta':  (4, 8),
    'alpha':  (8, 13),
    'beta':   (13, 30),
    'gamma':  (30, 100),
    'high-gamma': (100, 200),
}

print(f"\n  EEG frequency bands:")
for name, (lo, hi) in eeg_bands.items():
    mid = (lo + hi) / 2
    print(f"    {name:>12}: {lo:3d} - {hi:3d} Hz  (center {mid:.1f} Hz)")
print()

# Golden ratio in EEG band centers?
print("  Golden ratio test on EEG band CENTER frequencies:")
eeg_centers = [(name, (lo+hi)/2) for name, (lo, hi) in eeg_bands.items()]
for i in range(len(eeg_centers) - 1):
    n1, f1 = eeg_centers[i]
    n2, f2 = eeg_centers[i+1]
    ratio = f2 / f1
    phi_match = match_pct(ratio, phi)
    print(f"    {n2:>12}/{n1:<12} = {f2:.1f}/{f1:.1f} = {ratio:.4f}  (phi = {phi:.4f}, match {phi_match:.1f}%)")
print()
print("  NOTE: The ratios between adjacent EEG bands are NOT consistently phi.")
print("  They vary from ~1.5 to ~3.1. The 'golden ratio in EEG' claims in the")
print("  literature refer to specific ratios (e.g., beta/alpha ~ 2.0-2.4),")
print("  not a universal phi structure.")
print()

# Try the formula with f_base = f_electron
gamma_40 = 40.0  # Hz, the canonical gamma frequency
n_for_40Hz = find_best_n_float(f_electron, gamma_40)
print(f"  To get 40 Hz gamma from f_electron: need n = {n_for_40Hz:.1e} (absurd)")
print()

# What if f_base is the Rydberg frequency?
print(f"  Try f_base = f_Rydberg = {freq_str(f_Rydberg)}:")
for n in range(1, 6):
    f_pred = formula(f_Rydberg, n)
    print(f"    n={n}: {freq_str(f_pred)}")
print("  Still electromagnetic (THz-PHz), not neural (Hz).")
print()

# What about inverse formula: what f_base would give EEG bands?
for name, f_eeg in [('delta', 2.5), ('theta', 6.0), ('alpha', 10.5),
                     ('beta', 21.5), ('gamma', 40.0)]:
    f_base_needed = f_eeg / (alpha**(11.0/4.0) * phi * g_correct(2))
    print(f"  For {name:>6} ({f_eeg:.1f} Hz), need f_base = {freq_str(f_base_needed)}")

print()
print("  The required base frequencies (~10^7 Hz = 10 MHz) have no obvious")
print("  physical significance in neural or molecular physics.")
print()
print("  VERDICT: The formula cannot produce EEG frequencies from any")
print("  natural base frequency. EEG rhythms arise from GABA_A receptor")
print("  kinetics and cortical E-I loop architecture (Wang & Buzsaki 1996),")
print("  not from alpha^(11/4) scaling of an electronic frequency.")
print()


# =========================================================================
# SCALE 4: CARDIAC (heart rate, HRV)
# =========================================================================
print(SEP)
print("SCALE 4: CARDIAC")
print(SEP)

f_heart = 1.0     # ~1 Hz resting heart rate
f_hrv   = 0.1     # ~0.1 Hz cardiovascular resonance (Lehrer & Gevirtz 2014)
f_resp  = 0.25    # ~0.25 Hz respiratory rate

print(f"\n  Known cardiac frequencies:")
print(f"    Heart rate:     {freq_str(f_heart)} (~60 bpm)")
print(f"    HRV coherence:  {freq_str(f_hrv)} (~0.1 Hz, baroreflex resonance)")
print(f"    Respiratory:    {freq_str(f_resp)} (~15 breaths/min)")
print()

# Needed base for n=2
f_base_heart = f_heart / (alpha**(11.0/4.0) * phi * g_correct(2))
f_base_hrv = f_hrv / (alpha**(11.0/4.0) * phi * g_correct(2))
print(f"  To match 1 Hz (heart):   need f_base = {freq_str(f_base_heart)}")
print(f"  To match 0.1 Hz (HRV):   need f_base = {freq_str(f_base_hrv)}")
print()
print("  VERDICT: No natural base frequency produces cardiac timescales.")
print("  Heart rate is set by sinoatrial node pacemaker currents. The 0.1 Hz")
print("  HRV resonance is the baroreflex loop delay (~10 s round-trip).")
print()


# =========================================================================
# SCALE 5: STELLAR (plasma + EM)
# =========================================================================
print(SEP)
print("SCALE 5: STELLAR (plasma + EM coupling)")
print(SEP)

# Solar oscillation frequencies
f_5min = 1.0 / (5 * 60)          # 5-min oscillation = 3.3 mHz (p-modes)
f_3min = 1.0 / (3 * 60)          # 3-min oscillation = 5.6 mHz (chromospheric)
f_solar_cycle = 1.0 / (11 * 365.25 * 24 * 3600)  # 11-yr cycle ~ 2.9 nHz

# Plasma frequencies
f_plasma_corona  = 100e6   # ~100 MHz (solar corona, n_e ~ 10^8 cm^-3)
f_plasma_photo   = 10e9    # ~10 GHz  (photosphere, n_e ~ 10^13 cm^-3)
f_plasma_chromos = 1e9     # ~1 GHz   (chromosphere)

print(f"\n  Known solar frequencies:")
print(f"    5-min oscillation (p-mode): {freq_str(f_5min)}")
print(f"    3-min oscillation (chromo): {freq_str(f_3min)}")
print(f"    Solar cycle (11 yr):        {freq_str(f_solar_cycle)}")
print()
print(f"  Solar plasma frequencies:")
print(f"    Corona   (n_e ~ 10^8 cm^-3): {freq_str(f_plasma_corona)}")
print(f"    Chromosphere:                 {freq_str(f_plasma_chromos)}")
print(f"    Photosphere (n_e ~ 10^13):    {freq_str(f_plasma_photo)}")
print()

# Test: f_base = plasma frequency at various depths
print("  Formula results with f_base = solar plasma frequencies:")
print(f"  {'f_base':>20}  {'n':>3}  {'f_predicted':>16}  {'Known match?':>30}")
for name, f_base in [("f_plasma_corona", f_plasma_corona),
                      ("f_plasma_chromo", f_plasma_chromos),
                      ("f_plasma_photo", f_plasma_photo)]:
    for n in [1, 2, 3, 4, 5]:
        f_pred = formula(f_base, n)
        # Check against known solar frequencies
        known_solar = [
            (f_5min, "5-min oscillation"),
            (f_3min, "3-min oscillation"),
            (f_solar_cycle, "solar cycle"),
        ]
        nearest = min(known_solar, key=lambda x: abs(x[0] - f_pred))
        m = match_pct(f_pred, nearest[0])
        note = f"{nearest[1]} ({m:.1f}%)" if m > 50 else f"no match ({freq_str(f_pred)})"
        if n == 2:
            print(f"  {name:>20}  {n:3d}  {freq_str(f_pred):>16}  {note}")
        elif n == 1:
            print(f"  {name:>20}  {n:3d}  {freq_str(f_pred):>16}  {note}")

print()

# What if we use f_base = f_electron for stellar scale?
print("  Formula with f_base = f_electron at very high n:")
for n in [100, 1000, 10000, 100000]:
    f_pred = formula(f_electron, n)
    nearest_solar = min(
        [(f_5min, "5-min"), (f_3min, "3-min"), (f_solar_cycle, "11-yr")],
        key=lambda x: abs(x[0] - f_pred)
    )
    m = match_pct(f_pred, nearest_solar[0])
    print(f"    n={n:>7d}: {freq_str(f_pred):>16}  (nearest solar: {nearest_solar[1]}, match {m:.1f}%)")
print()

# Inverse: what n gives the 5-min oscillation from various bases?
print("  To match the solar 5-min oscillation (3.33 mHz):")
for name, f_base in [("f_electron", f_electron), ("f_plasma_corona", f_plasma_corona)]:
    n_needed = find_best_n_float(f_base, f_5min)
    print(f"    f_base = {name}: need n = {n_needed:.1e}")
print()

# The 5:3 ratio test
ratio_5_3 = (1.0/3.0) / (1.0/5.0)  # = 5/3
print(f"  The 5-min/3-min period ratio: 5/3 = {5/3:.6f}")
print(f"  phi = {phi:.6f}")
print(f"  Match: {match_pct(5/3, phi):.2f}% -- suggestive but NOT close (3% off)")
print()

# Schumann resonance test
f_schumann = 7.83  # Hz (fundamental Schumann resonance)
print(f"  Schumann resonance: {freq_str(f_schumann)}")
n_for_schumann = find_best_n_float(f_electron, f_schumann)
print(f"    Need n = {n_for_schumann:.1e} from f_electron (absurd)")
print()

print("  VERDICT: The formula does NOT naturally produce solar oscillation")
print("  frequencies from plasma frequencies or any other natural base.")
print("  The formula is off by many orders of magnitude.")
print("  Solar oscillations arise from acoustic waves in the stellar")
print("  interior (p-modes) and MHD processes, not from alpha^(11/4)")
print("  scaling of a base frequency.")
print()


# =========================================================================
# SCALE 6: GALACTIC (dark matter + magnetic)
# =========================================================================
print(SEP)
print("SCALE 6: GALACTIC")
print(SEP)

f_galactic_rot = 1.0 / (225e6 * 365.25 * 24 * 3600)  # ~225 Myr
f_milky_bar = 1.0 / (200e6 * 365.25 * 24 * 3600)  # bar rotation ~200 Myr
f_spiral_arm = 1.0 / (600e6 * 365.25 * 24 * 3600)  # spiral pattern ~600 Myr

print(f"\n  Known galactic frequencies:")
print(f"    Galactic rotation:   {freq_str(f_galactic_rot)} (~225 Myr)")
print(f"    Bar rotation:        {freq_str(f_milky_bar)} (~200 Myr)")
print(f"    Spiral arm pattern:  {freq_str(f_spiral_arm)} (~600 Myr)")
print()

# What base would give galactic rotation?
f_base_gal = f_galactic_rot / (alpha**(11.0/4.0) * phi * g_correct(2))
print(f"  For galactic rotation with n=2: need f_base = {freq_str(f_base_gal)}")
print(f"  This is ~{f_base_gal:.2e} Hz = completely arbitrary.")
print()

# Galactic magnetic field oscillation?
# Typical galactic B ~ 1-10 microGauss
# Larmor frequency for proton in 5 uG field:
B_gal = 5e-10  # 5 microGauss = 5e-10 Tesla
f_larmor_gal = e_ch * B_gal / (2 * math.pi * m_p)  # proton Larmor
print(f"  Proton Larmor freq in galactic B ({B_gal*1e6:.0f} uG): {freq_str(f_larmor_gal)}")
print(f"  Formula with this as f_base (n=2): {freq_str(formula(f_larmor_gal, 2))}")
print()
print("  VERDICT: No connection. Galactic timescales are set by gravity")
print("  and angular momentum, not by EM coupling constants.")
print()


# =========================================================================
# SCALE 7: PLANCK SCALE
# =========================================================================
print(SEP)
print("SCALE 7: PLANCK SCALE")
print(SEP)

print(f"\n  f_Planck = sqrt(c^5 / (hbar * G)) / (2pi) = {f_Planck:.6e} Hz")
print()

# The user asks about alpha^(11/4) * phi * 4/sqrt(3) * f_Planck
f_planck_n2 = formula(f_Planck, 2)
print(f"  Formula (n=2): alpha^(11/4) * phi * 4/sqrt(3) * f_Planck")
print(f"               = {f_planck_n2:.6e} Hz = {freq_str(f_planck_n2)}")
print()

# Compare to known frequencies
known_high = [
    (f_electron, "f_electron"),
    (f_Rydberg, "f_Rydberg"),
    (m_p * c**2 / h_pl, "f_proton"),
    (125.25e9 * e_ch / h_pl, "f_Higgs"),
]
print("  Comparison with known particle frequencies:")
for f_known, name in known_high:
    m = match_pct(f_planck_n2, f_known)
    ratio = f_planck_n2 / f_known
    print(f"    f_formula / {name:>12} = {ratio:.6e}  (match: {m:.2f}%)")
print()

# Interesting: does alpha^(11/4) * phi * 4/sqrt(3) * f_Planck give the GUT scale?
f_GUT = 1e16 * 1e9 * e_ch / h_pl  # ~10^16 GeV in Hz
m_formula = match_pct(f_planck_n2, f_GUT)
print(f"  GUT scale (~10^16 GeV): {f_GUT:.3e} Hz")
print(f"  Formula / GUT scale:    {f_planck_n2/f_GUT:.3e} (match: {m_formula:.1f}%)")
print()

# What about getting v (Higgs VEV) from Planck?
# v/M_Pl = phibar^80 according to framework
# Does alpha^(11/4) * phi * g(n) relate?
factor = alpha**(11.0/4.0) * phi * g_correct(2)
phibar80 = (1/phi)**80
print(f"  alpha^(11/4) * phi * g(2) = {factor:.6e}")
print(f"  phibar^80                 = {phibar80:.6e}")
print(f"  Ratio                     = {factor/phibar80:.6e}")
print(f"  These are 10 orders of magnitude apart. No connection.")
print()

print("  VERDICT: The formula at the Planck scale produces ~10^37 Hz.")
print("  This is between the Planck and GUT scales -- no known physical")
print("  frequency matches. The formula has no special meaning at the")
print("  Planck scale.")
print()


# =========================================================================
# COMPREHENSIVE SCAN: Try many base frequencies
# =========================================================================
print(SEP)
print("COMPREHENSIVE SCAN: Many base frequencies x PT depths")
print(SEP)
print()

# Known target frequencies across all scales
targets = [
    # (freq_Hz, name, category)
    (0.1,           "HRV coherence (0.1 Hz)",        "cardiac"),
    (1.0,           "Heart rate (~1 Hz)",              "cardiac"),
    (7.83,          "Schumann resonance (7.83 Hz)",   "geophysical"),
    (10.5,          "Alpha EEG (10.5 Hz)",            "neural"),
    (40.0,          "Gamma EEG (40 Hz)",              "neural"),
    (432.0,         "A=432 Hz tuning (speculative)",  "acoustic"),
    (f_5min,        "Solar p-mode (3.3 mHz)",         "stellar"),
    (f_solar_cycle, "Solar cycle (2.9 nHz)",          "stellar"),
    (102e12,        "O-H stretch (102 THz)",          "molecular"),
    (613e12,        "Craddock aromatic (613 THz)",    "molecular"),
    (1050e12,       "Trp UV abs (1050 THz)",          "molecular"),
]

# Base frequencies to try
bases = [
    (f_electron,       "f_electron"),
    (f_Rydberg,        "f_Rydberg"),
    (f_Planck,         "f_Planck"),
    (f_thermal,        "kT_body/h"),
    (f_plasma_corona,  "f_plasma_corona"),
    (f_plasma_photo,   "f_plasma_photo"),
    (k_B * 5778 / h_pl, "kT_Sun/h"),   # Sun surface temp
    (m_p * c**2 / h_pl, "f_proton"),
]

print(f"Searching for ANY (f_base, n) combination that matches known frequencies")
print(f"to better than 99%...")
print()

found_any = False
for f_target, target_name, category in targets:
    print(f"  Target: {target_name} ({freq_str(f_target)})")
    for f_base, base_name in bases:
        best_n, best_match, f_pred = find_best_n(f_base, f_target, range(1, 201))
        if best_match > 99.0:
            found_any = True
            print(f"    ** MATCH: f_base={base_name}, n={best_n}, "
                  f"f_pred={freq_str(f_pred)}, match={best_match:.2f}%")
        elif best_match > 95.0:
            print(f"     ~ close: f_base={base_name}, n={best_n}, "
                  f"f_pred={freq_str(f_pred)}, match={best_match:.2f}%")
    print()

if not found_any:
    print("  No matches above 99% found beyond the known biological one.")
print()


# =========================================================================
# THE HONEST QUESTION: Is g(n) necessary, or does alpha^(11/4)*phi alone work?
# =========================================================================
print(SEP)
print("CONTROL TEST: What does alpha^(11/4) * phi alone tell us?")
print(SEP)
print()

# The "bare" formula without PT
f_bare = alpha**(11.0/4.0) * phi * f_electron
print(f"  alpha^(11/4) * phi * f_electron = {freq_str(f_bare)} = {f_bare/1e12:.2f} THz")
print(f"  This is a MOLECULAR ELECTRONIC SCALE frequency by construction:")
print(f"    alpha^2 gives Rydberg from electron scale")
print(f"    alpha^(3/4) converts from mu to phi via core identity")
print(f"    = 265.8 THz (near infrared)")
print()

# How much freedom does g(n) give?
print(f"  The PT ratio g(n) provides a multiplicative adjustment:")
for n in range(1, 8):
    f_pred = formula(f_electron, n)
    print(f"    n={n}: g(n)={g_correct(n):.4f}, f = {f_pred/1e12:.2f} THz")
print()
print(f"  g(n) ranges from 1.0 (n=1) to ~{g_correct(7):.1f} (n=7), so the formula")
print(f"  can scan from {formula(f_electron,1)/1e12:.0f} THz to {formula(f_electron,7)/1e12:.0f} THz")
print(f"  (roughly the optical to near-UV range) for small integer n.")
print(f"  With n=2, it hits the visible range (613 THz).")
print()


# =========================================================================
# THE KEY QUESTION: What makes n=2 special?
# =========================================================================
print(SEP)
print("WHY n=2? The formula's only real prediction")
print(SEP)
print()
print("  The formula has three ingredients:")
print("    1. alpha^(11/4) -- combines Rydberg (alpha^2) with core identity (alpha^(3/4))")
print("    2. phi          -- from the golden ratio vacuum")
print("    3. g(n)         -- PT binding/breathing ratio for depth n")
print()
print("  Ingredients 1 and 2 are FIXED by the framework. They set the scale")
print("  to ~265.8 THz (bare formula without PT). This is already in the")
print("  molecular electronic energy range, regardless of the framework --")
print("  it is just the Born-Oppenheimer electronic-to-vibrational bridge")
print("  rewritten using the core identity.")
print()
print("  Ingredient 3 (g(n) with n=2) is the ONLY part that comes from the")
print("  domain wall theory. V(Phi) = lambda(Phi^2 - Phi - 1)^2 forces n=2")
print("  (PT depth 6), which gives g(2) = 4/sqrt(3) = 2.309, pushing the")
print("  bare scale up to 613.86 THz.")
print()
print("  But n=2 ONLY appears in the formula for the MOLECULAR electronic")
print("  scale. At other scales (neural, cardiac, stellar, galactic), there")
print("  is no base frequency that combines with alpha^(11/4) * phi * g(2)")
print("  to produce known frequencies.")
print()


# =========================================================================
# BONUS: Alternative formula without Born-Oppenheimer interpretation
# =========================================================================
print(SEP)
print("BONUS: Is there a scale-free version of the formula?")
print(SEP)
print()

# The formula f = alpha^(11/4) * phi * g(n) * f_base contains f_base which
# is scale-dependent. Can we define dimensionless ratios?

print("  Dimensionless ratio approach: f_target / f_base = alpha^(11/4) * phi * g(n)")
print()

# At the biological scale:
ratio_bio = f_craddock / f_electron
print(f"  Biological: f_Craddock / f_electron = {ratio_bio:.6e}")
print(f"  alpha^(11/4) * phi * g(2)           = {alpha**(11/4) * phi * g_correct(2):.6e}")
print(f"  Match: {match_pct(alpha**(11/4) * phi * g_correct(2), ratio_bio):.2f}%")
print()

# At the stellar scale: what would the analogous ratio be?
# If Sun has "consciousness" via plasma, what frequency / what base?
print("  For a stellar analog, we'd need:")
print("    f_stellar_consciousness / f_stellar_base = alpha^(11/4) * phi * g(n)")
print("  where f_stellar_consciousness and f_stellar_base are unknown.")
print("  This is unfalsifiable without knowing the stellar frequencies.")
print()


# =========================================================================
# SUMMARY TABLE
# =========================================================================
print(SEP)
print("SUMMARY TABLE")
print(SEP)
print()
print(f"{'Scale':<15} {'Base freq':>16} {'n':>3} {'Predicted':>16} {'Target':>16} {'Match':>8} {'Verdict':>12}")
print(DASH)

summary = [
    ("Biological", f_electron, 2, f_craddock, "99.86%", "WORKS"),
    ("Cellular",   f_electron, 2, f_cell_div, "---", "FAILS"),
    ("Neural",     f_electron, 2, 40.0, "---", "FAILS"),
    ("Cardiac",    f_electron, 2, 1.0, "---", "FAILS"),
    ("Stellar",    f_plasma_corona, 2, f_5min, "---", "FAILS"),
    ("Galactic",   None, 2, f_galactic_rot, "---", "FAILS"),
    ("Planck",     f_Planck, 2, None, "---", "NO TARGET"),
]

for name, f_base, n, f_tgt, m_str, verdict in summary:
    if f_base is not None:
        f_pred = formula(f_base, n)
        pred_str = freq_str(f_pred)
    else:
        pred_str = "N/A"
    if f_tgt is not None:
        tgt_str = freq_str(f_tgt)
    else:
        tgt_str = "N/A"
    if f_base is not None and f_tgt is not None and f_tgt > 0:
        actual_match = match_pct(f_pred, f_tgt)
        m_str = f"{actual_match:.1f}%" if actual_match > 0 else "<0%"
    print(f"{name:<15} {freq_str(f_base) if f_base else 'N/A':>16} {n:>3} {pred_str:>16} {tgt_str:>16} {m_str:>8} {verdict:>12}")
print()


# =========================================================================
# FINAL ASSESSMENT
# =========================================================================
print(SEP)
print("FINAL ASSESSMENT")
print(SEP)
print("""
The formula f = alpha^(11/4) * phi * n^2/sqrt(2n-1) * f_electron = 613.86 THz
is SPECIFIC TO THE MOLECULAR ELECTRONIC SCALE, not universal.

What it DOES:
  1. Correctly reproduces the Born-Oppenheimer electronic transition scale
     for molecular pi-electron systems (visible light range).
  2. The PT depth n=2 (from V(Phi)) selects exactly 613 THz within the
     visible range -- a genuine, non-trivial prediction matching Craddock.
  3. The golden ratio phi enters naturally through the core identity
     alpha^(3/2) * mu * phi^2 = 3, not as an ad-hoc insertion.

What it does NOT do:
  1. It does NOT produce frequencies at any other scale (neural, cardiac,
     stellar, galactic, Planck). The gap is many orders of magnitude.
  2. There is no natural "base frequency" at non-molecular scales that
     makes the formula work.
  3. The formula is the Born-Oppenheimer molecular electronic scale
     REWRITTEN using the core identity. It is real algebra, but it is
     molecular physics, not universal physics.

The honest conclusion:
  The formula works at ONE scale (molecular) because that is the scale
  it describes. It is not a universal consciousness frequency formula.
  The framework's claim that consciousness exists at stellar/galactic
  scales would require DIFFERENT formulas with different base frequencies,
  not this one.
""")

print("Script completed successfully.")
