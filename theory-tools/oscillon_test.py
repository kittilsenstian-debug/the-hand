"""
Oscillon persistence test for V(Phi) = lambda*(Phi^2 - Phi - 1)^2

Framework prediction: NO stable oscillons. Kink-antikink pairs annihilate.
This is a framework-specific prediction — generic phi^4 potentials DO have oscillons.

Tests multiple collision velocities and measures:
- Peak energy density at collision site vs time
- Whether a localized energy lump persists after collision

Result format: velocity, collision_time, peak_E_at_collision, peak_E_after_1000_steps, ratio
If ratio << 1: oscillon decayed (framework confirmed)
If ratio ~ 1: oscillon persists (framework challenged)
"""

import numpy as np
import sys

PHI = (1 + np.sqrt(5)) / 2
LAMBDA = 1.0


def V(phi):
    return LAMBDA * (phi**2 - phi - 1)**2


def dVdphi(phi):
    return 2 * LAMBDA * (phi**2 - phi - 1) * (2 * phi - 1)


def kink_profile(x, x0, width):
    half_range = np.sqrt(5) / 2
    center = 0.5
    return center + half_range * np.tanh((x - x0) / width)


def antikink_profile(x, x0, width):
    half_range = np.sqrt(5) / 2
    center = 0.5
    return center - half_range * np.tanh((x - x0) / width)


def run_collision_test(v, N=4000, L=80.0, post_collision_steps=5000):
    dx = L / N
    dt = dx * 0.15
    x = np.linspace(-L/2, L/2, N)
    kappa = np.sqrt(2 * LAMBDA) * np.sqrt(5) / 2
    width = 1.0 / kappa
    gamma = 1.0 / np.sqrt(1 - v**2)
    separation = 20.0

    # Initialize kink + antikink
    phi_k = kink_profile(x, -separation/2, width / gamma)
    phi_ak = antikink_profile(x, separation/2, width / gamma)
    phi = phi_k + phi_ak - PHI

    # Initial velocities
    phi_dot_k = v * gamma * np.sqrt(5)/2 * kappa / np.cosh(kappa * gamma * (x + separation/2))**2
    phi_dot_ak = -v * gamma * np.sqrt(5)/2 * kappa / np.cosh(kappa * gamma * (x - separation/2))**2
    phi_dot = phi_dot_k + phi_dot_ak

    # Absorbing boundaries
    damp_width = int(0.1 * N)
    damping = np.ones(N)
    damping[:damp_width] = np.linspace(0.05, 1, damp_width)
    damping[-damp_width:] = np.linspace(1, 0.05, damp_width)

    center_region = slice(N//2 - N//10, N//2 + N//10)

    def energy_density():
        grad = (np.roll(phi, -1) - np.roll(phi, 1)) / (2*dx)
        return 0.5 * phi_dot**2 + 0.5 * grad**2 + V(phi)

    # Phase 1: evolve until collision (watch peak E in center rise)
    peak_E_history = []
    collision_detected = False
    collision_step = 0
    peak_at_collision = 0

    total_pre = int(separation / (2 * v * dt)) * 3  # generous time to collide

    for step in range(total_pre):
        accel = (np.roll(phi, 1) + np.roll(phi, -1) - 2*phi) / dx**2 - dVdphi(phi)
        phi_dot *= damping
        phi_dot += accel * dt
        phi += phi_dot * dt

        if step % 50 == 0:
            E = energy_density()
            peak_center = np.max(E[center_region])
            peak_E_history.append(peak_center)

            if not collision_detected and peak_center > 5.0:
                collision_detected = True
                collision_step = step
                peak_at_collision = peak_center

    if not collision_detected:
        peak_at_collision = max(peak_E_history) if peak_E_history else 0
        collision_step = total_pre // 2

    # Phase 2: continue for post_collision_steps, measure persistence
    post_peaks = []
    for step in range(post_collision_steps):
        accel = (np.roll(phi, 1) + np.roll(phi, -1) - 2*phi) / dx**2 - dVdphi(phi)
        phi_dot *= damping
        phi_dot += accel * dt
        phi += phi_dot * dt

        if step % 100 == 0:
            E = energy_density()
            peak_center = np.max(E[center_region])
            post_peaks.append(peak_center)

    # Measure: does energy persist at collision site?
    final_peak = np.mean(post_peaks[-10:]) if len(post_peaks) >= 10 else post_peaks[-1]
    mid_peak = np.mean(post_peaks[len(post_peaks)//3:len(post_peaks)//3+5]) if len(post_peaks) > 10 else final_peak

    return {
        'velocity': v,
        'peak_at_collision': peak_at_collision,
        'mid_peak': mid_peak,
        'final_peak': final_peak,
        'persistence_ratio': final_peak / max(peak_at_collision, 1e-10),
        'mid_ratio': mid_peak / max(peak_at_collision, 1e-10),
    }


if __name__ == '__main__':
    print("=" * 70)
    print("OSCILLON PERSISTENCE TEST")
    print("V(Phi) = lambda*(Phi^2 - Phi - 1)^2")
    print("Framework prediction: NO stable oscillons")
    print("=" * 70)

    velocities = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]

    print(f"\n{'v':>6} {'E_collision':>12} {'E_mid':>12} {'E_final':>12} {'persist':>10} {'verdict':>15}")
    print("-" * 70)

    results = []
    for v in velocities:
        sys.stdout.write(f"  v={v}... ")
        sys.stdout.flush()
        r = run_collision_test(v)
        results.append(r)

        verdict = "DECAYED" if r['persistence_ratio'] < 0.1 else (
                  "PARTIAL" if r['persistence_ratio'] < 0.5 else "PERSISTS")

        print(f"\r{v:>6.1f} {r['peak_at_collision']:>12.3f} {r['mid_peak']:>12.3f} "
              f"{r['final_peak']:>12.3f} {r['persistence_ratio']:>10.4f} {verdict:>15}")

    # Summary
    decayed = sum(1 for r in results if r['persistence_ratio'] < 0.1)
    print(f"\n{'=' * 70}")
    print(f"RESULT: {decayed}/{len(velocities)} collisions show full decay")
    if decayed == len(velocities):
        print("FRAMEWORK CONFIRMED: No stable oscillons in the golden potential")
    elif decayed > len(velocities) * 0.7:
        print("MOSTLY CONFIRMED: Most collisions decay, some resonance windows")
    else:
        print("FRAMEWORK CHALLENGED: Oscillons persist at multiple velocities")
    print(f"{'=' * 70}")
