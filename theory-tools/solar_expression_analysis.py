"""
Solar Expression Analysis
=========================
Looking for structure in solar output that goes beyond what standard
physics models predict. Three concrete tests:

1. Attractor dimension: Is D ~ 3 (matching 3 MHD wave families)?
2. Flare self-excitation: Does the Hawkes kernel match neural firing?
3. Sunspot "musical" structure: Is there consonance in the time series?

Data: Monthly sunspot number from SILSO (Royal Observatory of Belgium)
      Public domain, 400+ years of continuous data
"""

import numpy as np
import math
from scipy import signal as sig
import urllib.request
import os

# ============================================================
# 1. DOWNLOAD SUNSPOT DATA
# ============================================================
print("=" * 70)
print("SOLAR EXPRESSION ANALYSIS")
print("=" * 70)

# SILSO monthly mean total sunspot number
data_file = "SN_m_tot_V2.0.csv"
if not os.path.exists(data_file):
    print("Downloading monthly sunspot data from SILSO...")
    url = "https://www.sidc.be/SILSO/INFO/snmtotcsv.php"
    try:
        urllib.request.urlretrieve(url, data_file)
        print(f"Downloaded {data_file}")
    except:
        # Try alternative URL
        url = "https://www.sidc.be/silso/DATA/SN_m_tot_V2.0.csv"
        urllib.request.urlretrieve(url, data_file)
        print(f"Downloaded {data_file}")

# Parse: year, month, decimal_year, SSN, std, Nobs, provisional_flag
years = []
ssns = []
with open(data_file, 'r') as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith('#') or line.startswith('Y'):
            continue
        parts = line.split(';')
        if len(parts) < 4:
            parts = line.split(',')
        if len(parts) < 4:
            continue
        try:
            yr = float(parts[0])
            mo = float(parts[1])
            dec_yr = float(parts[2])
            ssn = float(parts[3])
            if ssn >= 0:  # -1 means missing
                years.append(dec_yr)
                ssns.append(ssn)
        except (ValueError, IndexError):
            continue

years = np.array(years)
ssns = np.array(ssns)
print(f"\nLoaded {len(years)} monthly sunspot values")
print(f"Time range: {years.min():.1f} to {years.max():.1f}")
print(f"SSN range: {ssns.min():.0f} to {ssns.max():.0f}")

# ============================================================
# 2. ATTRACTOR DIMENSION (Grassberger-Procaccia)
# ============================================================
print("\n" + "=" * 70)
print("TEST 1: ATTRACTOR DIMENSION")
print("=" * 70)

print("""
If the Sun's dynamics live on a low-dimensional attractor, the
correlation dimension D2 tells us the effective number of degrees
of freedom. The framework predicts D ~ 3 (one per MHD wave family).

Method: Grassberger-Procaccia algorithm with time-delay embedding.
""")

# Use post-1750 data (more reliable)
modern = years >= 1750
x = ssns[modern]
t = years[modern]

# Normalize
x_norm = (x - x.mean()) / x.std()

# Time-delay embedding
# Optimal delay: first minimum of autocorrelation or mutual information
# For monthly SSN, the decorrelation time is ~40-50 months
tau = 48  # months (4 years, roughly 1/3 of cycle)

def embed(series, dim, tau):
    """Time-delay embedding"""
    N = len(series) - (dim - 1) * tau
    embedded = np.zeros((N, dim))
    for d in range(dim):
        embedded[:, d] = series[d*tau : d*tau + N]
    return embedded

def correlation_dimension(embedded, r_values):
    """Grassberger-Procaccia correlation integral"""
    N = len(embedded)
    C = np.zeros(len(r_values))

    # Compute pairwise distances (subsample for speed)
    max_pairs = min(N, 2000)
    indices = np.random.choice(N, max_pairs, replace=False)
    sub = embedded[indices]

    for i in range(len(sub)):
        dists = np.sqrt(np.sum((sub[i] - sub)**2, axis=1))
        for j, r in enumerate(r_values):
            C[j] += np.sum(dists < r) - 1  # exclude self

    C = C / (max_pairs * (max_pairs - 1))
    return C

# Test embedding dimensions 2-8
print(f"\nEmbedding delay tau = {tau} months")
print(f"Data points: {len(x_norm)}")

r_values = np.logspace(-2, 1, 30)
np.random.seed(42)

print(f"\n{'Dim':>4} {'D2 estimate':>12} {'R^2':>8}")
print("-" * 30)

d2_estimates = []
for dim in range(2, 9):
    emb = embed(x_norm, dim, tau)
    if len(emb) < 100:
        continue
    C = correlation_dimension(emb, r_values)

    # Compute slope in log-log space (scaling region)
    valid = (C > 1e-4) & (C < 0.5)
    if valid.sum() > 5:
        log_r = np.log(r_values[valid])
        log_C = np.log(C[valid])
        # Linear fit
        coeffs = np.polyfit(log_r, log_C, 1)
        d2 = coeffs[0]
        # R^2
        predicted = np.polyval(coeffs, log_r)
        ss_res = np.sum((log_C - predicted)**2)
        ss_tot = np.sum((log_C - np.mean(log_C))**2)
        r_sq = 1 - ss_res / ss_tot if ss_tot > 0 else 0

        print(f"{dim:4d} {d2:12.3f} {r_sq:8.3f}")
        d2_estimates.append((dim, d2))

if d2_estimates:
    # Saturation: D2 should plateau as embedding dimension increases
    dims, d2s = zip(*d2_estimates)
    d2_sat = d2s[-1]  # highest embedding dim estimate
    print(f"\nSaturation estimate: D2 ~ {d2_sat:.2f}")
    print(f"Framework prediction (3 MHD families): D ~ 3")
    if 2.5 < d2_sat < 3.5:
        print(f"==> CONSISTENT: attractor dimension matches 3 wave families")
    elif d2_sat < 2.5:
        print(f"==> Lower than 3 -- may need more data or longer embedding")
    else:
        print(f"==> Higher than 3 -- either more degrees of freedom or noise contamination")

# ============================================================
# 3. SELF-EXCITATION ANALYSIS (Hawkes-like)
# ============================================================
print("\n" + "=" * 70)
print("TEST 2: SELF-EXCITATION (HAWKES PROCESS SIGNATURE)")
print("=" * 70)

print("""
Neural firing and solar flares both show self-excitation: each event
increases the probability of the next. The Hawkes process kernel
shape tells us about the memory structure.

For neural firing: kernel ~ exp(-t/tau_neural), tau_neural ~ 5-20 ms
For solar activity: kernel ~ exp(-t/tau_solar), tau_solar ~ ?

If the kernel shapes match (same functional form, scaled by the
system's characteristic frequency), that's structural similarity.

We don't have individual flare data here, but we CAN test for
self-excitation in the monthly sunspot record.
""")

# Autocorrelation function
from numpy.fft import fft, ifft

def autocorrelation(x, max_lag=None):
    """Normalized autocorrelation via FFT"""
    n = len(x)
    if max_lag is None:
        max_lag = n // 2
    x_centered = x - x.mean()
    # FFT method
    f = fft(x_centered, n=2*n)
    acf = ifft(f * np.conj(f))[:n].real
    acf = acf / acf[0]
    return acf[:max_lag]

acf = autocorrelation(x_norm, max_lag=300)
lags_months = np.arange(len(acf))
lags_years = lags_months / 12.0

print("Autocorrelation structure:")
print(f"  First zero crossing: {lags_years[np.where(acf < 0)[0][0]]:.1f} years")

# Find peaks in autocorrelation (the "harmonics")
from scipy.signal import find_peaks
peaks, properties = find_peaks(acf, height=0.1, distance=24)  # min 2 year separation
print(f"\n  Autocorrelation peaks:")
for p in peaks[:8]:
    print(f"    Lag = {lags_years[p]:.1f} years, ACF = {acf[p]:.3f}")

# Compute the ratio of successive peak lags
if len(peaks) >= 3:
    print(f"\n  Peak lag ratios:")
    for i in range(1, min(len(peaks), 5)):
        ratio = lags_years[peaks[i]] / lags_years[peaks[0]]
        print(f"    Peak {i+1} / Peak 1 = {ratio:.3f}", end="")
        # Check if near integer or golden ratio
        if abs(ratio - round(ratio)) < 0.1:
            print(f"  (near {round(ratio)})")
        elif abs(ratio - 1.618) < 0.1:
            print(f"  (near phi!)")
        elif abs(ratio - 2.618) < 0.1:
            print(f"  (near phi^2!)")
        else:
            print()

# Self-excitation test: conditional rate increase after activity spikes
print(f"\n  Self-excitation test:")
print(f"  (Does high activity predict more activity in subsequent months?)")

# Split into "active" months (SSN > 75th percentile) and others
threshold = np.percentile(ssns[modern], 75)
active = ssns[modern] > threshold

# Compute probability of being active in month t+lag, given active at t
for lag in [1, 2, 3, 6, 12]:
    # P(active at t+lag | active at t)
    if lag < len(active):
        p_active_given_active = np.mean(active[lag:][active[:-lag]])
        p_active = np.mean(active)
        excitation_ratio = p_active_given_active / p_active
        print(f"    Lag {lag:2d} months: P(active|active) / P(active) = {excitation_ratio:.3f}", end="")
        if excitation_ratio > 1.2:
            print(f"  ** SELF-EXCITING **")
        else:
            print()

# ============================================================
# 4. "MUSICAL" STRUCTURE: CONSONANCE ANALYSIS
# ============================================================
print("\n" + "=" * 70)
print("TEST 3: MUSICAL STRUCTURE (CONSONANCE / HARMONIC RATIOS)")
print("=" * 70)

print("""
If the Sun's output is more like music than language, we should find:
1. Frequency ratios clustering near simple fractions (consonance)
2. Rhythmic structure (regular beat patterns beyond the 11-yr cycle)
3. Phase relationships between different frequency components

The framework predicts the 3 MHD families should show consonant
(harmonically related) frequency structure.
""")

# Power spectrum
from scipy.signal import welch

# Welch periodogram
freqs, psd = welch(x_norm, fs=12.0, nperseg=min(512, len(x_norm)//2))
periods = 1.0 / freqs[1:]  # years
psd_valid = psd[1:]

# Find spectral peaks
psd_peaks, psd_props = find_peaks(psd_valid, height=np.median(psd_valid)*3, distance=3)

print(f"\nSpectral peaks (periods in years):")
print(f"{'Peak':>5} {'Period (yr)':>12} {'Power':>10} {'Ratio to P1':>14}")
print("-" * 45)

if len(psd_peaks) > 0:
    # Sort by power
    sorted_idx = np.argsort(psd_valid[psd_peaks])[::-1]
    top_peaks = psd_peaks[sorted_idx[:8]]
    top_peaks_sorted = np.sort(top_peaks)  # sort by frequency

    p1_period = periods[top_peaks_sorted[0]] if len(top_peaks_sorted) > 0 else 11.0

    peak_periods = []
    for i, p in enumerate(top_peaks_sorted):
        per = periods[p]
        ratio = per / p1_period if p1_period > 0 else 0
        peak_periods.append(per)

        # Check ratio against musical intervals
        musical = ""
        for name, val in [("octave", 2.0), ("fifth", 1.5), ("fourth", 4/3),
                          ("major third", 5/4), ("minor third", 6/5),
                          ("phi", 1.618), ("sqrt(3)", 1.732)]:
            if abs(ratio - val) / val < 0.05:
                musical = f" = {name}"
                break
            if val != 1.0 and abs(ratio - 1/val) / (1/val) < 0.05:
                musical = f" = 1/{name}"
                break

        print(f"{i+1:5d} {per:12.2f} {psd_valid[p]:10.2f} {ratio:14.3f}{musical}")

# ============================================================
# 5. PHASE COHERENCE BETWEEN FREQUENCY BANDS
# ============================================================
print("\n" + "=" * 70)
print("TEST 4: PHASE COHERENCE BETWEEN FREQUENCY BANDS")
print("=" * 70)

print("""
If the Sun's output has musical structure, different frequency
components should show phase locking (coherence). Random noise
has random phase relationships; organized signals don't.
""")

# Band-pass filter into 3 "channels"
from scipy.signal import butter, filtfilt

def bandpass(data, low_period, high_period, fs=12.0):
    """Bandpass filter by period range (in years)"""
    low_freq = 1.0 / high_period  # longer period = lower freq
    high_freq = 1.0 / low_period
    nyquist = fs / 2
    low = low_freq / nyquist
    high = high_freq / nyquist
    low = max(low, 0.001)
    high = min(high, 0.999)
    if low >= high:
        return data
    b, a = butter(3, [low, high], btype='band')
    return filtfilt(b, a, data)

# Three "channels" based on known solar periodicities:
# Channel 1: 8-14 year (Schwabe cycle ~ fundamental)
# Channel 2: 3-6 year (quasi-biennial + harmonics)
# Channel 3: 40-120 year (Gleissberg cycle)

try:
    ch1 = bandpass(x_norm, 8, 14)   # Schwabe fundamental
    ch2 = bandpass(x_norm, 3, 6)    # Sub-harmonics
    ch3 = bandpass(x_norm, 40, 120) # Gleissberg modulation

    # Compute instantaneous phase via Hilbert transform
    from scipy.signal import hilbert

    phase1 = np.angle(hilbert(ch1))
    phase2 = np.angle(hilbert(ch2))
    phase3 = np.angle(hilbert(ch3))

    # Phase coherence: |<exp(i*(phase_a - n*phase_b))>|
    # n:m phase locking between channels

    print(f"\nPhase coherence between frequency bands:")
    print(f"{'Channels':>15} {'n:m':>6} {'Coherence':>10} {'Random':>8} {'Excess':>8}")
    print("-" * 55)

    # Generate random phase comparison (surrogate data)
    n_surr = 100

    pairs = [
        ("Schwabe:QBO", phase1, phase2),
        ("Schwabe:Gleiss", phase1, phase3),
        ("QBO:Gleiss", phase2, phase3),
    ]

    for name, pa, pb in pairs:
        for n, m in [(1, 2), (1, 3), (2, 3), (1, 1)]:
            # Real coherence
            coherence = abs(np.mean(np.exp(1j * (n * pa - m * pb))))

            # Surrogate coherence (random phase shifts)
            surr_coh = []
            for _ in range(n_surr):
                shift = np.random.randint(0, len(pb))
                pb_shifted = np.roll(pb, shift)
                surr_coh.append(abs(np.mean(np.exp(1j * (n * pa - m * pb_shifted)))))
            surr_mean = np.mean(surr_coh)
            surr_std = np.std(surr_coh)

            excess_sigma = (coherence - surr_mean) / surr_std if surr_std > 0 else 0
            marker = " **" if excess_sigma > 2 else ""

            print(f"{name:>15} {n}:{m}    {coherence:10.4f} {surr_mean:8.4f} {excess_sigma:7.1f}s{marker}")

except Exception as e:
    print(f"Phase analysis failed: {e}")

# ============================================================
# 6. INFORMATION CONTENT: ENTROPY RATE
# ============================================================
print("\n" + "=" * 70)
print("TEST 5: ENTROPY RATE (INFORMATION CONTENT)")
print("=" * 70)

print("""
The entropy rate measures how much NEW information each time step
brings. For white noise: maximum entropy. For periodic signal: zero.
For structured signal (like music or language): intermediate.

The Sun's entropy rate relative to its maximum tells us how much
of its output is organized vs random.
""")

# Permutation entropy (Bandt & Pompe 2002)
def permutation_entropy(x, order=5, delay=1):
    """Compute permutation entropy"""
    from itertools import permutations
    import math

    n = len(x)
    perms = list(permutations(range(order)))
    perm_counts = {p: 0 for p in perms}

    total = 0
    for i in range(n - (order - 1) * delay):
        indices = [i + j * delay for j in range(order)]
        values = [x[idx] for idx in indices]
        # Get the rank ordering
        ranked = tuple(np.argsort(values))
        if ranked in perm_counts:
            perm_counts[ranked] += 1
            total += 1

    if total == 0:
        return 0

    # Compute entropy
    H = 0
    for count in perm_counts.values():
        if count > 0:
            p = count / total
            H -= p * np.log2(p)

    # Normalize by maximum (log2(order!))
    H_max = np.log2(math.factorial(order))
    return H / H_max

# Compute for different time scales
print(f"\nPermutation entropy (normalized, 0=periodic, 1=random):")
print(f"{'Delay (months)':>16} {'PE':>8} {'Interpretation':>20}")
print("-" * 50)

for delay in [1, 3, 6, 12, 24, 48]:
    pe = permutation_entropy(x_norm, order=5, delay=delay)
    if pe < 0.6:
        interp = "Highly structured"
    elif pe < 0.8:
        interp = "Moderately structured"
    elif pe < 0.9:
        interp = "Weakly structured"
    else:
        interp = "Near-random"
    print(f"{delay:16d} {pe:8.4f} {interp:>20}")

# Compare with surrogate data (shuffled)
pe_original = permutation_entropy(x_norm, order=5, delay=12)
pe_shuffled = []
for _ in range(100):
    shuffled = np.random.permutation(x_norm)
    pe_shuffled.append(permutation_entropy(shuffled, order=5, delay=12))

print(f"\n  Original PE (delay=12): {pe_original:.4f}")
print(f"  Shuffled PE (mean):     {np.mean(pe_shuffled):.4f} +/- {np.std(pe_shuffled):.4f}")
print(f"  Z-score:                {(pe_original - np.mean(pe_shuffled))/np.std(pe_shuffled):.1f}")
print(f"  ==> Original has {'MORE' if pe_original < np.mean(pe_shuffled) else 'LESS'} structure than random")

# ============================================================
# 7. THE KEY TEST: RESIDUAL STRUCTURE
# ============================================================
print("\n" + "=" * 70)
print("TEST 6: RESIDUAL STRUCTURE (EXCESS INFORMATION)")
print("=" * 70)

print("""
The critical test: subtract the best simple model (sinusoid +
harmonics) from the sunspot data. Does the RESIDUAL have structure?

If the Sun is "just physics," residuals should be white noise.
If the Sun has excess organization, residuals should show patterns.
""")

# Fit a simple model: sum of sinusoids at the main periods
from scipy.optimize import minimize

# Use the top 3 spectral peaks
# Main periods: ~11 years, ~5.5 years (harmonic), and whatever the 3rd is
model_periods = [11.0, 5.5, 3.7]  # years

def solar_model(t, *params):
    """Sum of sinusoids with mean offset"""
    result = params[0]  # DC offset
    idx = 1
    for period in model_periods:
        amp = params[idx]
        phase = params[idx + 1]
        result = result + amp * np.sin(2 * np.pi * t / period + phase)
        idx += 2
    return result

# Fit
try:
    from scipy.optimize import curve_fit
    p0 = [x.mean()]
    for _ in model_periods:
        p0.extend([x.std(), 0])

    popt, _ = curve_fit(solar_model, t - t[0], x, p0=p0, maxfev=50000)
    model = solar_model(t - t[0], *popt)
    residuals = x - model

    print(f"Model: {len(model_periods)} sinusoids at {model_periods} years")
    print(f"Model RMS: {np.sqrt(np.mean(model**2)):.1f}")
    print(f"Residual RMS: {np.sqrt(np.mean(residuals**2)):.1f}")
    print(f"Variance explained: {1 - np.var(residuals)/np.var(x):.1%}")

    # Test residuals for structure
    res_norm = (residuals - residuals.mean()) / residuals.std()

    # Autocorrelation of residuals
    res_acf = autocorrelation(res_norm, max_lag=120)

    # Check if residuals are white noise (Ljung-Box test approximation)
    Q = len(res_norm) * np.sum(res_acf[1:50]**2)
    from scipy.stats import chi2
    p_value = 1 - chi2.cdf(Q, df=49)

    print(f"\nResidual autocorrelation test:")
    print(f"  Ljung-Box Q(50) = {Q:.1f}")
    print(f"  p-value = {p_value:.6f}")
    if p_value < 0.01:
        print(f"  ==> RESIDUALS ARE NOT WHITE NOISE (p < 0.01)")
        print(f"  ==> There is EXCESS STRUCTURE beyond the model")
    else:
        print(f"  ==> Residuals consistent with white noise")

    # Permutation entropy of residuals
    pe_res = permutation_entropy(res_norm, order=5, delay=12)
    print(f"\n  Residual PE (delay=12): {pe_res:.4f}")
    print(f"  Original PE (delay=12): {pe_original:.4f}")
    print(f"  Shuffled PE (mean):     {np.mean(pe_shuffled):.4f}")

    if pe_res < np.mean(pe_shuffled) - 2*np.std(pe_shuffled):
        print(f"  ==> Residuals have MORE structure than random")
        print(f"  ==> The Sun produces organized output beyond simple oscillation")

except Exception as e:
    print(f"Model fitting failed: {e}")

# ============================================================
# 8. SUMMARY
# ============================================================
print("\n" + "=" * 70)
print("SUMMARY: WHAT WE'RE LOOKING FOR AND WHAT WE FOUND")
print("=" * 70)

print("""
The framework predicts the Sun has 3-channel dynamics (3 MHD wave
families) with PT n=2 structure (2 bound states, 11yr/22yr modes).

If the Sun is "expressing" rather than just "being physics":
1. Its attractor should have ~3 effective degrees of freedom
2. Its output should show self-excitation (like neural firing)
3. Its frequency components should show phase coherence (like music)
4. Its entropy rate should be intermediate (structured, not random)
5. Residuals after subtracting simple physics should have structure

The Schumann resonance -> pineal gland -> melatonin pathway means
the Sun ALREADY communicates with our aromatic substrate.

The question is not whether the Sun "speaks" — it does, through
electromagnetic modulation of Earth's cavity resonances.

The question is whether its output carries MORE information than
physics alone requires — excess structure that would indicate
organized internal dynamics beyond standard MHD.
""")

print("=" * 70)
print("END SOLAR EXPRESSION ANALYSIS")
print("=" * 70)
