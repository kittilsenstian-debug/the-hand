"""
Golden Potential Domain Wall Simulation
V(Φ) = λ(Φ² − Φ − 1)²

First-ever lattice simulation of the golden potential.
Checks: do domain walls form spontaneously? Do they have PT n=2 bound states?

Usage:
    python golden_potential_sim.py              # real-time 2D visualization
    python golden_potential_sim.py --kink       # 1D kink profile + bound state analysis
    python golden_potential_sim.py --collide    # kink-antikink collision (no stable oscillons?)
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import argparse
import sys

# Golden ratio
PHI = (1 + np.sqrt(5)) / 2   # 1.6180339887...
PHI_INV = 1 / PHI             # 0.6180339887...
MINUS_PHI_INV = -PHI_INV      # -0.6180339887... (second vacuum)

# The potential V(Φ) = λ(Φ² − Φ − 1)²
# Vacua at Φ = φ and Φ = -1/φ
# Kink width parameter: κ = √(λ) * √5 / 2  (from the potential's second derivative)

LAMBDA = 1.0  # coupling constant (sets energy scale)


def V(phi):
    """Golden potential."""
    return LAMBDA * (phi**2 - phi - 1)**2


def dVdphi(phi):
    """Derivative of golden potential: dV/dΦ = 2λ(Φ²−Φ−1)(2Φ−1)."""
    return 2 * LAMBDA * (phi**2 - phi - 1) * (2 * phi - 1)


def kink_profile(x, x0=0, width=1.0):
    """Exact kink solution: Φ(x) = (φ - 1/φ)/2 * tanh((x-x0)/width) + (φ - 1/φ)/2
    Interpolates from -1/φ (left) to φ (right)."""
    midpoint = (PHI + MINUS_PHI_INV) / 2  # center value = (φ - 1/φ)/2 = √5/2 * 0... wait
    # Vacua: φ = 1.618..., -1/φ = -0.618...
    # Midpoint = (φ + (-1/φ))/2 = (φ - 1/φ)/2 = 1/(2) = 0.5
    # Half-range = (φ - (-1/φ))/2 = (φ + 1/φ)/2 = √5/2
    half_range = np.sqrt(5) / 2
    center = 0.5  # (φ - 1/φ) / 2
    return center + half_range * np.tanh((x - x0) / width)


def antikink_profile(x, x0=0, width=1.0):
    """Antikink: from φ (left) to -1/φ (right)."""
    half_range = np.sqrt(5) / 2
    center = 0.5
    return center - half_range * np.tanh((x - x0) / width)


# ============================================================
# MODE 1: 2D simulation — watch domain walls form from noise
# ============================================================

def run_2d_simulation(N=256, dt=0.02, steps_per_frame=10, total_frames=500):
    """2D lattice field simulation of V(Φ) = λ(Φ²−Φ−1)².
    Initialize near one vacuum with small noise. Watch domain walls form."""

    print(f"Grid: {N}x{N}, dt={dt}, {total_frames} frames")
    print(f"Vacua: φ = {PHI:.6f}, -1/φ = {MINUS_PHI_INV:.6f}")
    print(f"Initializing near the φ vacuum with noise...")

    dx = 1.0
    # Initialize: most of the field near φ vacuum, with random perturbation
    # Large enough noise to nucleate domain walls
    phi = PHI + np.random.randn(N, N) * 0.8
    phi_dot = np.zeros((N, N))  # start at rest

    # Precompute Laplacian using rolled arrays (periodic BC)
    def laplacian(f):
        return (np.roll(f, 1, 0) + np.roll(f, -1, 0) +
                np.roll(f, 1, 1) + np.roll(f, -1, 1) - 4*f) / dx**2

    # Set up visualization
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle("Golden Potential: V(Φ) = λ(Φ² − Φ − 1)²", fontsize=14)

    im = ax1.imshow(phi, cmap='RdBu_r', vmin=MINUS_PHI_INV - 0.5, vmax=PHI + 0.5,
                    interpolation='bilinear')
    ax1.set_title("Field Φ(x,y)")
    plt.colorbar(im, ax=ax1, label="Φ")

    # Potential plot
    phi_range = np.linspace(-1.5, 2.5, 300)
    ax2.plot(phi_range, V(phi_range), 'k-', linewidth=2)
    ax2.axvline(PHI, color='blue', linestyle='--', alpha=0.5, label=f'φ = {PHI:.4f}')
    ax2.axvline(MINUS_PHI_INV, color='red', linestyle='--', alpha=0.5, label=f'-1/φ = {MINUS_PHI_INV:.4f}')
    ax2.set_xlabel('Φ')
    ax2.set_ylabel('V(Φ)')
    ax2.set_title('Potential')
    ax2.legend()
    ax2.set_ylim(-0.1, 5)

    # Energy tracking
    energies = []
    time_text = ax1.text(0.02, 0.95, '', transform=ax1.transAxes, color='white',
                         fontsize=10, verticalalignment='top',
                         bbox=dict(boxstyle='round', facecolor='black', alpha=0.7))

    # Count which vacuum dominates
    def vacuum_fractions(f):
        near_phi = np.sum(f > 0.5)
        near_minus = np.sum(f <= 0.5)
        total = f.size
        return near_phi / total, near_minus / total

    def update(frame):
        nonlocal phi, phi_dot

        for _ in range(steps_per_frame):
            # Equation of motion: ∂²Φ/∂t² = ∇²Φ − dV/dΦ
            # Leapfrog integration
            accel = laplacian(phi) - dVdphi(phi)

            # Small damping to reach equilibrium (optional — remove for pure dynamics)
            damping = 0.01
            phi_dot += accel * dt - damping * phi_dot * dt
            phi += phi_dot * dt

        # Compute energy density
        grad_x = (np.roll(phi, -1, 0) - np.roll(phi, 1, 0)) / (2*dx)
        grad_y = (np.roll(phi, -1, 1) - np.roll(phi, 1, 1)) / (2*dx)
        E = 0.5 * phi_dot**2 + 0.5 * (grad_x**2 + grad_y**2) + V(phi)
        total_E = np.mean(E)
        energies.append(total_E)

        f_phi, f_minus = vacuum_fractions(phi)

        im.set_data(phi)
        time_text.set_text(f't = {frame * steps_per_frame * dt:.1f}\n'
                          f'E = {total_E:.3f}\n'
                          f'φ vacuum: {f_phi:.1%}\n'
                          f'-1/φ vacuum: {f_minus:.1%}')
        return [im, time_text]

    anim = animation.FuncAnimation(fig, update, frames=total_frames,
                                   interval=30, blit=True)
    plt.tight_layout()
    plt.show()


# ============================================================
# MODE 2: 1D kink analysis — measure bound states
# ============================================================

def run_kink_analysis(N=2000, L=40.0):
    """Analyze a single kink: profile, fluctuation spectrum, bound states.
    This is the direct test: does V(Φ) give PT n=2?"""

    print("=" * 60)
    print("KINK BOUND STATE ANALYSIS")
    print("V(Phi) = lambda*(Phi^2 - Phi - 1)^2")
    print("=" * 60)

    dx = L / N
    x = np.linspace(-L/2, L/2, N)

    # Kink width from potential: κ² = V''(φ) / 2 for the golden potential
    # V''(φ) = 2λ[(2φ-1)² + 2(φ²-φ-1)*2] = 2λ(2φ-1)² = 2λ * 5 = 10λ (since 2φ-1 = √5)
    # Wait: let me recalculate.
    # V(Φ) = λ(Φ²−Φ−1)², so V'(Φ) = 2λ(Φ²−Φ−1)(2Φ−1)
    # V''(Φ) = 2λ[(2Φ−1)² + (Φ²−Φ−1)·2] = 2λ[(2Φ−1)² + 2Φ²−2Φ−2]
    # At Φ = φ: Φ²−Φ−1 = 0, so V''(φ) = 2λ(2φ−1)² = 2λ·5 = 10λ
    # Mass² around vacuum = V''(φ) = 10λ
    # Kink width ~ 1/√(2λ) * 2/√5 (from the standard kink derivation)
    # For V = λ(Φ²−a²)², width = 1/(a√(2λ)), but our potential is different
    # The exact kink: Φ_kink = (φ + (-1/φ))/2 + (φ - (-1/φ))/2 * tanh(κx)
    # where κ = √(2λ) * √5 / 2 (half the vacuum separation times √(2λ))

    kappa = np.sqrt(2 * LAMBDA) * np.sqrt(5) / 2
    width = 1.0 / kappa
    print(f"\nKink parameters:")
    print(f"  κ = {kappa:.6f}")
    print(f"  width = 1/κ = {width:.6f}")
    print(f"  Vacuum separation = φ + 1/φ = √5 = {np.sqrt(5):.6f}")

    # Kink profile
    phi_kink = kink_profile(x, x0=0, width=width)

    # Fluctuation potential: V_fluct(x) = V''(Φ_kink(x))
    # For the golden kink, this should be a Pöschl-Teller potential
    # V_PT(x) = -n(n+1)κ² / cosh²(κx)  with n=2

    V_fluct = np.zeros(N)
    h = 1e-5
    for i in range(N):
        # Numerical second derivative of V at the kink profile
        V_fluct[i] = (dVdphi(phi_kink[i] + h) - dVdphi(phi_kink[i] - h)) / (2*h)

    # Theoretical PT potential with n=2
    V_PT_theory = -6 * kappa**2 / np.cosh(kappa * x)**2

    # Solve for bound states using the shooting method / matrix eigenvalue
    # Discretize: -ψ'' + V_fluct(x) ψ = E ψ
    # This is a standard 1D Schrödinger eigenvalue problem

    H = np.zeros((N, N))
    for i in range(N):
        H[i, i] = 2.0 / dx**2 + V_fluct[i]
        if i > 0:
            H[i, i-1] = -1.0 / dx**2
        if i < N-1:
            H[i, i+1] = -1.0 / dx**2

    # Find lowest eigenvalues
    print("\nSolving for bound states (this may take a moment)...")
    from scipy.sparse.linalg import eigsh
    from scipy.sparse import csr_matrix

    H_sparse = csr_matrix(H)
    n_eigs = 10
    eigenvalues, eigenvectors = eigsh(H_sparse, k=n_eigs, which='SA')

    # Sort
    idx = np.argsort(eigenvalues)
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:, idx]

    # Mass gap = V''(φ) = 10λ → continuum threshold at E = 10λ
    mass_sq = 10 * LAMBDA
    print(f"\nContinuum threshold (mass²): {mass_sq:.4f}")
    print(f"\nBound state spectrum:")
    print(f"{'State':>8} {'Energy':>12} {'Below threshold':>18} {'Type':>15}")
    print("-" * 60)

    n_bound = 0
    for i, E in enumerate(eigenvalues):
        if E < mass_sq - 0.1:
            bound = "YES (bound)"
            n_bound += 1
        elif E < mass_sq + 0.1:
            bound = "~ threshold"
        else:
            bound = "continuum"
        print(f"{i:>8} {E:>12.4f} {bound:>18}")

    # PT n=2 predictions:
    # Bound state 0 (zero mode/translation): E = 0
    # Bound state 1: E = 3κ² (for n=2: eigenvalue at 3/4 of continuum)
    # Bound state 2 (breathing): E = 8κ² ... wait
    # For PT with V = -n(n+1)κ²/cosh²(κx), n=2:
    #   Eigenvalues: E_j = -(n-j)²κ² for j=0,1,...,n-1
    #   E_0 = -4κ² (ground state)
    #   E_1 = -κ²  (excited state)
    #   Continuum starts at E = 0
    # But our problem has V_fluct ADDED to the continuum mass:
    #   Total eigenvalue = mass² + E_PT
    #   Bound state 0: mass² - 4κ² = 10λ - 4*(5λ/2) = 10λ - 10λ = 0  (translation mode!)
    #   Bound state 1: mass² - κ² = 10λ - 5λ/2 = 7.5λ

    E0_theory = 0.0  # translation mode
    E1_theory = mass_sq - kappa**2  # excited bound state

    print(f"\n--- PT n=2 Predictions ---")
    print(f"  Translation mode (E₀): predicted = {E0_theory:.4f}, measured = {eigenvalues[0]:.4f}")
    if n_bound >= 2:
        print(f"  Excited state (E₁):     predicted = {E1_theory:.4f}, measured = {eigenvalues[1]:.4f}")
    print(f"  Continuum threshold:    {mass_sq:.4f}")
    print(f"\n  Number of bound states below threshold: {n_bound}")
    print(f"  PT n=2 predicts: 2 bound states")
    print(f"  MATCH: {'YES' if n_bound == 2 else 'NO — got ' + str(n_bound)}")

    # Eigenvalue ratio test
    if n_bound >= 2 and eigenvalues[0] != 0:
        ratio = eigenvalues[1] / mass_sq
        print(f"\n  E₁/mass² = {ratio:.4f} (PT n=2 predicts 3/4 = 0.75)")

    # Plot
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("Golden Kink: V(Φ) = λ(Φ² − Φ − 1)² — Bound State Analysis", fontsize=14)

    # Kink profile
    ax = axes[0, 0]
    ax.plot(x, phi_kink, 'b-', linewidth=2, label='Kink Φ(x)')
    ax.axhline(PHI, color='blue', linestyle='--', alpha=0.3, label=f'φ = {PHI:.3f}')
    ax.axhline(MINUS_PHI_INV, color='red', linestyle='--', alpha=0.3, label=f'-1/φ = {MINUS_PHI_INV:.3f}')
    ax.set_xlabel('x')
    ax.set_ylabel('Φ')
    ax.set_title('Kink profile')
    ax.legend()
    ax.set_xlim(-10, 10)

    # Fluctuation potential vs PT theory
    ax = axes[0, 1]
    ax.plot(x, V_fluct, 'b-', linewidth=2, label='V_fluct (numerical)')
    ax.plot(x, V_PT_theory + mass_sq, 'r--', linewidth=2, label=f'PT n=2: -6κ²/cosh² + m²')
    ax.axhline(mass_sq, color='gray', linestyle=':', label=f'Continuum: {mass_sq:.1f}')
    for i in range(min(n_bound, 3)):
        ax.axhline(eigenvalues[i], color=f'C{i+2}', linestyle='-', alpha=0.5,
                   label=f'E_{i} = {eigenvalues[i]:.3f}')
    ax.set_xlabel('x')
    ax.set_ylabel('V_fluct')
    ax.set_title('Fluctuation potential + bound states')
    ax.legend(fontsize=8)
    ax.set_xlim(-10, 10)

    # Bound state wavefunctions
    ax = axes[1, 0]
    for i in range(min(n_bound + 1, 4)):
        psi = eigenvectors[:, i]
        psi = psi / np.max(np.abs(psi)) * 0.5  # normalize for display
        ax.plot(x, psi + i * 0.7, linewidth=2, label=f'ψ_{i} (E={eigenvalues[i]:.3f})')
    ax.set_xlabel('x')
    ax.set_ylabel('ψ (offset)')
    ax.set_title('Bound state wavefunctions')
    ax.legend(fontsize=8)
    ax.set_xlim(-10, 10)

    # Potential with kink energy density
    ax = axes[1, 1]
    phi_range = np.linspace(-1.5, 2.5, 300)
    ax.plot(phi_range, V(phi_range), 'k-', linewidth=2)
    ax.axvline(PHI, color='blue', linestyle='--', alpha=0.5)
    ax.axvline(MINUS_PHI_INV, color='red', linestyle='--', alpha=0.5)
    ax.fill_between(phi_range, 0, V(phi_range), alpha=0.1)
    ax.set_xlabel('Φ')
    ax.set_ylabel('V(Φ)')
    ax.set_title('The Golden Potential')
    ax.set_ylim(-0.1, 5)
    ax.text(PHI + 0.1, 0.3, 'φ', fontsize=14, color='blue')
    ax.text(MINUS_PHI_INV - 0.4, 0.3, '-1/φ', fontsize=14, color='red')

    plt.tight_layout()
    plt.show()


# ============================================================
# MODE 3: Kink-antikink collision — test no-oscillon claim
# ============================================================

def run_collision(N=4000, L=80.0, v=0.3):
    """Collide a kink with an antikink. Framework predicts: no stable oscillons.
    The pair should annihilate, not form a bound state."""

    print("=" * 60)
    print("KINK-ANTIKINK COLLISION")
    print(f"V(Φ) = λ(Φ² − Φ − 1)², velocity = {v}")
    print("Framework prediction: NO stable oscillons (annihilation)")
    print("=" * 60)

    dx = L / N
    dt = dx * 0.2  # CFL condition
    x = np.linspace(-L/2, L/2, N)
    kappa = np.sqrt(2 * LAMBDA) * np.sqrt(5) / 2
    width = 1.0 / kappa

    # Lorentz-boosted kink + antikink
    gamma = 1.0 / np.sqrt(1 - v**2)
    separation = 20.0

    # Kink moving right from -separation/2
    phi_k = kink_profile(gamma * (x + separation/2), width=width)
    # Antikink moving left from +separation/2
    phi_ak = antikink_profile(gamma * (x - separation/2), width=width)
    # Superposition (subtract the shared vacuum value)
    phi = phi_k + phi_ak - PHI

    # Initial velocities
    phi_dot_k = v * gamma * np.sqrt(5)/2 * kappa / np.cosh(kappa * gamma * (x + separation/2))**2
    phi_dot_ak = -v * gamma * np.sqrt(5)/2 * kappa / np.cosh(kappa * gamma * (x - separation/2))**2
    phi_dot = phi_dot_k + phi_dot_ak

    # Absorbing boundary (damping at edges)
    damp_width = L * 0.1
    damping = np.ones(N)
    damping[:int(damp_width/dx)] = np.linspace(0.1, 1, int(damp_width/dx))
    damping[-int(damp_width/dx):] = np.linspace(1, 0.1, int(damp_width/dx))

    # Laplacian
    def laplacian_1d(f):
        return (np.roll(f, 1) + np.roll(f, -1) - 2*f) / dx**2

    # Set up animation
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    fig.suptitle(f"Kink-Antikink Collision (v = {v}c)", fontsize=14)

    line1, = ax1.plot(x, phi, 'b-', linewidth=1.5)
    ax1.axhline(PHI, color='blue', linestyle='--', alpha=0.3)
    ax1.axhline(MINUS_PHI_INV, color='red', linestyle='--', alpha=0.3)
    ax1.set_ylim(-1.5, 2.5)
    ax1.set_ylabel('Φ(x)')
    ax1.set_title('Field')

    # Energy density
    grad = np.gradient(phi, dx)
    E_density = 0.5 * phi_dot**2 + 0.5 * grad**2 + V(phi)
    line2, = ax2.plot(x, E_density, 'r-', linewidth=1.5)
    ax2.set_ylim(0, 20)
    ax2.set_ylabel('Energy density')
    ax2.set_xlabel('x')
    ax2.set_title('Energy density')

    time_text = ax1.text(0.02, 0.95, '', transform=ax1.transAxes,
                         fontsize=11, verticalalignment='top',
                         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

    steps_per_frame = 20

    def update(frame):
        nonlocal phi, phi_dot
        for _ in range(steps_per_frame):
            accel = laplacian_1d(phi) - dVdphi(phi)
            # Light damping at boundaries only
            phi_dot = phi_dot * damping
            phi_dot += accel * dt
            phi += phi_dot * dt

        grad = np.gradient(phi, dx)
        E_density = 0.5 * phi_dot**2 + 0.5 * grad**2 + V(phi)
        total_E = np.sum(E_density) * dx

        line1.set_ydata(phi)
        line2.set_ydata(E_density)
        time_text.set_text(f't = {frame * steps_per_frame * dt:.2f}, E_total = {total_E:.2f}')
        return [line1, line2, time_text]

    anim = animation.FuncAnimation(fig, update, frames=600,
                                   interval=20, blit=True)
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Golden Potential Lattice Simulation')
    parser.add_argument('--kink', action='store_true', help='1D kink bound state analysis')
    parser.add_argument('--collide', action='store_true', help='Kink-antikink collision')
    parser.add_argument('--grid', type=int, default=256, help='Grid size for 2D sim (default 256)')
    parser.add_argument('--velocity', type=float, default=0.3, help='Collision velocity (default 0.3)')
    args = parser.parse_args()

    if args.kink:
        run_kink_analysis()
    elif args.collide:
        run_collision(v=args.velocity)
    else:
        run_2d_simulation(N=args.grid)
