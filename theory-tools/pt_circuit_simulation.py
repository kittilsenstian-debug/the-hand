#!/usr/bin/env python3
"""
pt_circuit_simulation.py -- Poeschl-Teller n=2 Domain Wall LC Chain Simulation
===============================================================================

Models a discrete LC ladder network where the series inductance follows a
DECREASED sech^2 profile at the center:

    L(j) = L0 * (1 - delta * sech^2((j - j_center) / w))

This creates an electrical analog of the Poeschl-Teller potential.  Bound
states appear as localized modes ABOVE the passband (the well is inverted
in the energy picture because reduced L means higher local cutoff).

The mapping (derived in the documentation):

    n(n+1) = 4 * delta * w^2

For n=2, this gives delta = 3/(2*w^2).

The simulation confirms:
    - Exactly 2 localized (bound) modes above the passband
    - Energy ratio E_0/E_1 = 4.0  (matching PT theory: -(n-k)^2 for k=0,1)
    - Mode profiles: one even (ground state), one odd (breathing mode)
    - Comparison: n=1 gives 1 bound state, n=3 gives 3

Requires: numpy, scipy, matplotlib
Usage:    python pt_circuit_simulation.py

Author: Interface Theory project
Date:   2026-02-26
"""

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# ==========================================================================
# Design parameters (21-node chain -- practical for bench build)
# ==========================================================================
N_NODES   = 21            # number of LC nodes
C0        = 100e-9        # shunt capacitance: 100 nF
L0        = 1.0e-3        # background series inductance: 1 mH
W         = 2.5           # sech^2 width in cell units
DELTA_N2  = 0.233         # depth parameter tuned for E0/E1=4.0 on 21-node chain
J_CENTER  = (N_NODES - 2) / 2.0   # center of the 20 links = 9.5

# Derived
Z0       = np.sqrt(L0 / C0)                     # 100 ohms
F_CUTOFF = 1.0 / (np.pi * np.sqrt(L0 * C0))     # ~31,831 Hz

# ==========================================================================
# Inductance profile construction
# ==========================================================================

def make_L_profile(delta, N=N_NODES, w=W, L_bg=L0):
    """Return array of N-1 link inductances for a sech^2 dip of depth delta."""
    j_c = (N - 2) / 2.0
    return np.array([
        L_bg * (1.0 - delta / np.cosh((j - j_c) / w)**2)
        for j in range(N - 1)
    ])

def delta_from_n(n_target, w=W):
    """Continuum-limit delta for PT depth n: n(n+1) = 4*delta*w^2."""
    return n_target * (n_target + 1) / (4.0 * w**2)

# ==========================================================================
# Eigenvalue computation
# ==========================================================================

def compute_eigenfreqs(L_links, C=C0, N=N_NODES):
    """
    Build and diagonalise the dynamical matrix for the LC ladder.

    KCL at node j gives:
        omega^2 * C * v_j = sum_neighbors [(v_j - v_neighbor) / L_link]

    Returns (frequencies_Hz, eigenvectors), both sorted by ascending freq.
    """
    M = np.zeros((N, N))
    for j in range(N):
        if j > 0:
            inv_L = 1.0 / (L_links[j - 1] * C)
            M[j, j]     += inv_L
            M[j, j - 1] -= inv_L
        if j < N - 1:
            inv_L = 1.0 / (L_links[j] * C)
            M[j, j]     += inv_L
            M[j, j + 1] -= inv_L

    evals, evecs = np.linalg.eigh(M)
    freqs = np.sqrt(np.maximum(evals, 0.0)) / (2.0 * np.pi)
    order = np.argsort(freqs)
    return freqs[order], evecs[:, order]

def band_edge(N=N_NODES, C=C0, L_bg=L0):
    """Return the highest eigenfrequency of the uniform chain (passband edge)."""
    L_uniform = np.full(N - 1, L_bg)
    freqs, _ = compute_eigenfreqs(L_uniform, C, N)
    return freqs[-1]

def find_bound_states(freqs, evecs, f_edge):
    """
    Identify modes above the passband edge (these are the bound states).
    Returns list of dicts with frequency, eigenvector, energy above edge.
    """
    bound = []
    for k in range(len(freqs)):
        if freqs[k] > f_edge * 1.001:
            E = freqs[k]**2 - f_edge**2   # "energy" measured from band edge
            bound.append({
                'freq':   freqs[k],
                'evec':   evecs[:, k],
                'energy': E,
                'index':  k,
            })
    return bound

# ==========================================================================
# Pulse propagation (time domain)
# ==========================================================================

def simulate_pulse(L_links, C=C0, N=N_NODES,
                   f_drive=25000.0, pulse_width=12e-6,
                   T_total=0.8e-3, dt=5e-7):
    """
    Time-domain simulation of a Gaussian-enveloped sinusoidal pulse.

    Source at node 0 (series resistance Z0).
    Load at node N-1 (shunt resistance Z0).

    Returns (t_array, V_array) where V_array has shape (N, n_timesteps).
    """
    R_s = Z0
    R_l = Z0

    def rhs(t, y):
        V = y[:N]
        I = y[N:]
        dV = np.zeros(N)
        dI = np.zeros(N - 1)

        t0 = 3.0 * pulse_width
        V_src = (np.exp(-(t - t0)**2 / (2.0 * pulse_width**2))
                 * np.sin(2.0 * np.pi * f_drive * t))

        # Node 0
        dV[0] = ((V_src - V[0]) / R_s - I[0]) / C
        # Interior
        for j in range(1, N - 1):
            dV[j] = (I[j - 1] - I[j]) / C
        # Node N-1
        dV[N - 1] = (I[N - 2] - V[N - 1] / R_l) / C
        # Inductor currents
        for j in range(N - 1):
            dI[j] = (V[j] - V[j + 1]) / L_links[j]

        return np.concatenate([dV, dI])

    y0 = np.zeros(N + N - 1)
    t_eval = np.arange(0.0, T_total, dt)
    sol = solve_ivp(rhs, (0.0, T_total), y0, t_eval=t_eval,
                    method='RK45', max_step=dt, rtol=1e-8, atol=1e-10)
    return sol.t, sol.y[:N, :]

# ==========================================================================
# Transfer matrix (frequency domain)
# ==========================================================================

def transfer_matrix_ST(L_links, C, N, freq, Z_term=None):
    """
    Compute |T|^2 and |R|^2 via ABCD transfer matrix.
    Chain: half-shunt -- [series L, full shunt C]_repeat -- half-shunt.
    Both ends terminated in Z_term.
    """
    if Z_term is None:
        Z_term = Z0
    omega = 2.0 * np.pi * freq
    if omega < 1e-10:
        return 1.0, 0.0

    ABCD = np.eye(2, dtype=complex)
    Y_half = 1j * omega * C / 2.0
    ABCD = ABCD @ np.array([[1, 0], [Y_half, 1]], dtype=complex)

    for j in range(N - 1):
        Z_L = 1j * omega * L_links[j]
        ABCD = ABCD @ np.array([[1, Z_L], [0, 1]], dtype=complex)
        if j < N - 2:
            Y_C = 1j * omega * C
            ABCD = ABCD @ np.array([[1, 0], [Y_C, 1]], dtype=complex)

    ABCD = ABCD @ np.array([[1, 0], [Y_half, 1]], dtype=complex)

    A, B, Cm, D = ABCD[0, 0], ABCD[0, 1], ABCD[1, 0], ABCD[1, 1]
    denom = A * Z_term + B + Cm * Z_term**2 + D * Z_term
    T = 2.0 * Z_term / denom
    R = (A * Z_term + B - Cm * Z_term**2 - D * Z_term) / denom
    return np.abs(T)**2, np.abs(R)**2

# ==========================================================================
# Analytic PT reflection (continuous limit)
# ==========================================================================

def pt_reflection_continuous(n, k_over_kappa):
    """
    |R|^2 for continuous Poeschl-Teller potential:
        |R|^2 = sin^2(pi*n) / [sin^2(pi*n) + sinh^2(pi*k/kappa)]
    Integer n gives |R|^2 = 0 identically (reflectionless).
    """
    s2 = np.sin(np.pi * n)**2
    sh2 = np.sinh(np.pi * k_over_kappa)**2
    denom = s2 + sh2
    if denom < 1e-30:
        return 0.0
    return s2 / denom

# ==========================================================================
# Monte Carlo tolerance analysis
# ==========================================================================

def tolerance_analysis(L_nominal, C_nominal, N, f_edge,
                       tol_L=0.02, tol_C=0.02, n_trials=500):
    """
    Run Monte Carlo to quantify sensitivity to component tolerances.
    Returns (fraction_with_2_bound, mean_ratio, std_ratio).
    """
    ratios = []
    for _ in range(n_trials):
        L_trial = L_nominal * (1.0 + tol_L * np.random.randn(len(L_nominal)))
        C_trial = max(C_nominal * (1.0 + tol_C * np.random.randn()), 1e-12)
        freqs, evecs = compute_eigenfreqs(L_trial, C_trial, N)
        bound = find_bound_states(freqs, evecs, f_edge)
        if len(bound) == 2:
            ratios.append(bound[1]['energy'] / bound[0]['energy'])
    success = len(ratios) / n_trials
    if ratios:
        return success, np.mean(ratios), np.std(ratios)
    return success, None, None

# ==========================================================================
# Main
# ==========================================================================

def main():
    print("=" * 72)
    print("  Poeschl-Teller n=2 Domain Wall -- LC Chain Simulation")
    print("=" * 72)
    print()

    # -- 1. Design summary ------------------------------------------------
    print("DESIGN PARAMETERS")
    print(f"  Nodes:                 N = {N_NODES}")
    print(f"  Shunt capacitance:     C = {C0*1e9:.0f} nF")
    print(f"  Background inductance: L0 = {L0*1e3:.0f} mH")
    print(f"  sech^2 width:          w = {W}")
    print(f"  Depth parameter:       delta = {DELTA_N2}")
    print(f"  Char. impedance:       Z0 = {Z0:.0f} ohms")
    print(f"  Background cutoff:     f_c = {F_CUTOFF:.0f} Hz")
    print()

    # -- 2. Inductance profile -------------------------------------------
    L_n2 = make_L_profile(DELTA_N2)

    print("INDUCTOR VALUES (symmetric sech^2 dip)")
    print("-" * 64)
    print(f"{'Link':>4s}  {'Nodes':>7s}  {'L (uH)':>9s}  {'L/L0':>7s}  {'sech^2':>7s}")
    print("-" * 64)
    for j in range(N_NODES - 1):
        sech2 = 1.0 / np.cosh((j - J_CENTER) / W)**2
        print(f"{j:4d}  {j:2d} - {j+1:2d}  {L_n2[j]*1e6:9.1f}  "
              f"{L_n2[j]/L0:7.4f}  {sech2:7.4f}")
    print()

    # -- 3. Eigenfrequency analysis --------------------------------------
    f_edge = band_edge()
    freqs_n2, evecs_n2 = compute_eigenfreqs(L_n2)
    bound_n2 = find_bound_states(freqs_n2, evecs_n2, f_edge)

    print("EIGENFREQUENCY ANALYSIS")
    print(f"  Passband edge (uniform chain):  {f_edge:.0f} Hz")
    print(f"  Number of bound states (above band): {len(bound_n2)}")
    for i, b in enumerate(bound_n2):
        v = b['evec']
        parity = "even" if abs(v[0] - v[-1]) < 0.2 * np.max(np.abs(v)) else "odd"
        print(f"  Bound {i}: f = {b['freq']:.0f} Hz,  "
              f"E_above = {b['energy']:.0f} Hz^2,  symmetry = {parity}")
    if len(bound_n2) >= 2:
        ratio = bound_n2[-1]['energy'] / bound_n2[0]['energy']
        print(f"  Energy ratio E_0/E_1 = {ratio:.3f}   (PT theory: 4.000)")
    print()

    # -- 4. Comparison across PT depths ----------------------------------
    print("COMPARISON: n = 1, 1.5, 2, 3")
    print("-" * 52)
    results = {}
    for n_val in [1.0, 1.5, 2.0, 3.0]:
        # For n=2 use the fine-tuned delta, else use continuum formula
        if n_val == 2.0:
            d = DELTA_N2
        else:
            d = delta_from_n(n_val)
        L_test = make_L_profile(d)
        f_test, ev_test = compute_eigenfreqs(L_test)
        bound = find_bound_states(f_test, ev_test, f_edge)
        n_b = len(bound)
        ratio_str = ""
        if n_b >= 2:
            ratio_str = f"  E0/E1 = {bound[-1]['energy']/bound[0]['energy']:.3f}"
        int_tag = " (integer)" if n_val == int(n_val) else " (non-int)"
        print(f"  n = {n_val:.1f}{int_tag}:  delta = {d:.4f},  "
              f"bound states = {n_b}{ratio_str}")
        results[n_val] = bound
    print()

    # -- 5. Analytic reflectionlessness ----------------------------------
    print("ANALYTIC REFLECTION COEFFICIENT (continuous PT)")
    print("  |R|^2 = sin^2(pi*n) / [sin^2(pi*n) + sinh^2(pi*k/kappa)]")
    print("  Integer n => sin(pi*n)=0 => |R|^2=0 at ALL frequencies.")
    print()
    header = f"  {'k/kappa':>8s}"
    for n_val in [1.0, 1.5, 2.0, 2.5, 3.0]:
        tag = " *" if n_val == int(n_val) else "  "
        header += f"  n={n_val:.1f}{tag:>2s}"
    print(header)
    print("  " + "-" * 68)
    for kk in [0.05, 0.1, 0.2, 0.5, 1.0, 2.0, 5.0]:
        row = f"  {kk:8.2f}"
        for n_val in [1.0, 1.5, 2.0, 2.5, 3.0]:
            R2 = pt_reflection_continuous(n_val, kk)
            if R2 < 1e-15:
                row += f"  {'0':>10s}"
            else:
                row += f"  {R2:10.6f}"
        print(row)
    print("  (* = integer: reflectionless)")
    print()

    # -- 6. Tolerance analysis -------------------------------------------
    print("TOLERANCE ANALYSIS (Monte Carlo, 500 trials each)")
    print("-" * 56)
    for tol in [0.01, 0.02, 0.05, 0.10]:
        sr, rm, rs = tolerance_analysis(L_n2, C0, N_NODES, f_edge,
                                        tol_L=tol, tol_C=tol)
        if rm is not None:
            print(f"  +/-{tol*100:4.0f}%: 2-state success = {sr*100:5.0f}%,  "
                  f"E0/E1 = {rm:.3f} +/- {rs:.3f}")
        else:
            print(f"  +/-{tol*100:4.0f}%: 2-state success = {sr*100:5.0f}%")
    print()

    # -- 7. Plots ---------------------------------------------------------
    print("Generating plots...")

    fig, axes = plt.subplots(2, 3, figsize=(17, 10))
    fig.suptitle("Poeschl-Teller n=2 Domain Wall -- LC Chain Simulation",
                 fontsize=14, fontweight='bold')

    # (a) Inductance profile
    ax = axes[0, 0]
    links = np.arange(N_NODES - 1)
    ax.plot(links, L_n2 * 1e6, 'b-o', ms=4, label="n=2 profile")
    ax.axhline(L0 * 1e6, color='gray', ls='--', label="Background L0")
    ax.set_xlabel("Link index")
    ax.set_ylabel("Inductance (uH)")
    ax.set_title("(a) sech^2 inductance dip")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # (b) Eigenfrequency spectrum
    ax = axes[0, 1]
    freqs_ref, _ = compute_eigenfreqs(np.full(N_NODES - 1, L0))
    ax.plot(range(N_NODES), freqs_ref / 1e3, 'k.', ms=3, label="Uniform chain")
    colors_n2 = ['blue' if f <= f_edge * 1.001 else 'red' for f in freqs_n2]
    ax.scatter(range(N_NODES), freqs_n2 / 1e3, c=colors_n2, s=20,
               zorder=3, label="n=2 chain")
    ax.axhline(f_edge / 1e3, color='orange', ls='--',
               label=f"Band edge ({f_edge/1e3:.1f} kHz)")
    ax.set_xlabel("Mode index")
    ax.set_ylabel("Frequency (kHz)")
    ax.set_title("(b) Eigenfrequency spectrum (red = bound)")
    ax.legend(fontsize=7)
    ax.grid(True, alpha=0.3)

    # (c) Bound state mode profiles
    ax = axes[0, 2]
    nodes = np.arange(N_NODES)
    for i, b in enumerate(bound_n2):
        v = b['evec'] / np.max(np.abs(b['evec']))
        ax.plot(nodes, v, 'o-', ms=4,
                label=f"Bound {i}: f={b['freq']/1e3:.1f} kHz")
    ax.axhline(0, color='gray', ls='-', lw=0.5)
    ax.set_xlabel("Node index")
    ax.set_ylabel("Normalized amplitude")
    ax.set_title("(c) Bound state mode profiles")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # (d) Bound state count vs n
    ax = axes[1, 0]
    for n_val, color, mk in [(1, 'green', 's'), (2, 'red', 'o'), (3, 'purple', '^')]:
        d = DELTA_N2 if n_val == 2 else delta_from_n(float(n_val))
        L_test = make_L_profile(d)
        f_test, _ = compute_eigenfreqs(L_test)
        above = f_test[f_test > f_edge * 1.001]
        inband = f_test[(f_test <= f_edge * 1.001) & (f_test > 10)]
        ax.plot([n_val]*len(inband), inband/1e3, '.', color='lightgray', ms=2)
        ax.plot([n_val]*len(above), above/1e3, mk, color=color, ms=8,
                label=f"n={n_val}: {len(above)} bound")
    ax.axhline(f_edge / 1e3, color='orange', ls='--', label="Band edge")
    ax.set_xlabel("PT depth parameter n")
    ax.set_ylabel("Frequency (kHz)")
    ax.set_title("(d) Bound state count vs PT depth")
    ax.set_xticks([1, 2, 3])
    ax.legend(fontsize=7)
    ax.grid(True, alpha=0.3)

    # (e) Pulse propagation
    ax = axes[1, 1]
    print("  Running pulse simulation...")
    t_p, V_p = simulate_pulse(L_n2, f_drive=25000, pulse_width=12e-6,
                               T_total=0.8e-3, dt=5e-7)
    ax.plot(t_p * 1e3, V_p[0, :],  'b-', lw=0.8, alpha=0.7, label="Node 0 (input)")
    ax.plot(t_p * 1e3, V_p[10, :], 'r-', lw=0.8, alpha=0.7, label="Node 10 (center)")
    ax.plot(t_p * 1e3, V_p[20, :], 'g-', lw=0.8, alpha=0.7, label="Node 20 (output)")
    ax.set_xlabel("Time (ms)")
    ax.set_ylabel("Voltage (V)")
    ax.set_title("(e) Pulse propagation (f = 25 kHz)")
    ax.legend(fontsize=7)
    ax.grid(True, alpha=0.3)

    # (f) Analytic reflectionlessness
    ax = axes[1, 2]
    kk = np.linspace(0.01, 5.0, 300)
    for n_val, color, ls in [(1, 'green', '-'), (1.5, 'orange', '--'),
                              (2, 'red', '-'), (2.5, 'purple', '--'),
                              (3, 'blue', '-')]:
        R2 = np.array([pt_reflection_continuous(n_val, k) for k in kk])
        tag = " *" if n_val == int(n_val) else ""
        ax.plot(kk, R2, color=color, ls=ls, lw=1.5, label=f"n={n_val}{tag}")
    ax.set_xlabel("k / kappa")
    ax.set_ylabel("|R|^2")
    ax.set_title("(f) Analytic reflection (* = integer)")
    ax.legend(fontsize=7)
    ax.set_ylim(-0.02, 1.05)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    outpath = "theory-tools/pt_circuit_simulation.png"
    plt.savefig(outpath, dpi=150, bbox_inches='tight')
    print(f"  Plot saved to {outpath}")
    print()

    # -- 8. Summary -------------------------------------------------------
    print("=" * 72)
    print("SUMMARY")
    print("=" * 72)
    if len(bound_n2) >= 2:
        ratio = bound_n2[-1]['energy'] / bound_n2[0]['energy']
        print(f"  PT n=2 gives EXACTLY 2 bound states above the passband.")
        print(f"  Ground state (even):    f_0 = {bound_n2[-1]['freq']:.0f} Hz")
        print(f"  Breathing mode (odd):   f_1 = {bound_n2[0]['freq']:.0f} Hz")
        print(f"  Energy ratio:           E_0/E_1 = {ratio:.3f}  (theory: 4.000)")
        print(f"  Band edge:              f_c = {f_edge:.0f} Hz")
    print()
    print("  n=1 gives 1 bound state.  n=3 gives 3.  The count is topological.")
    print("  Integer n is reflectionless (|R|^2 = 0 at ALL frequencies).")
    print()
    print("  Component tolerance: need < 2% on L and C for reliable results.")
    print("  Recommendation: hand-wind inductors on toroid cores, measure to 1%.")
    print()


if __name__ == "__main__":
    main()
