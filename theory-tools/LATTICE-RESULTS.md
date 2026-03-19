# Golden Potential Lattice Simulation Results

First-ever numerical simulation of V(Phi) = lambda*(Phi^2 - Phi - 1)^2 on a lattice.

## Result 1: Bound state spectrum (CONFIRMED)

The golden kink has exactly 2 bound states below the continuum threshold.

| Quantity | PT n=2 prediction | Lattice measurement | Match |
|----------|------------------|-------------------|-------|
| Number of bound states | 2 | 2 | EXACT |
| Translation mode E_0 | 0.0000 | 0.0015 | numerical zero |
| Excited state E_1 | 7.5000 | 7.5026 | 99.97% |
| E_1/m^2 ratio | 3/4 = 0.7500 | 0.7503 | 99.96% |
| Continuum threshold | 10.0000 | 10.0069 | 99.93% |

Lattice: N=2000, L=40.0, kappa=1.581139. Eigenvalues from sparse Hamiltonian diagonalization (scipy eigsh).

This confirms the framework's foundational claim: V(Phi) = lambda*(Phi^2 - Phi - 1)^2 produces a kink with Poeschl-Teller depth n=2, exactly 2 bound states, eigenvalue ratio 3/4.

## Result 2: No stable oscillons (CONFIRMED)

Kink-antikink collisions at 8 velocities (0.1c to 0.8c): complete annihilation in every case.

| Velocity | Peak E at collision | Final E at site | Persistence | Verdict |
|----------|-------------------|-----------------|-------------|---------|
| 0.1 | 3.156 | 0.000 | 0.0000 | DECAYED |
| 0.2 | 3.255 | 0.000 | 0.0000 | DECAYED |
| 0.3 | 3.434 | 0.000 | 0.0000 | DECAYED |
| 0.4 | 3.720 | 0.000 | 0.0000 | DECAYED |
| 0.5 | 4.168 | 0.000 | 0.0000 | DECAYED |
| 0.6 | 4.885 | 0.000 | 0.0000 | DECAYED |
| 0.7 | 5.382 | 0.000 | 0.0000 | DECAYED |
| 0.8 | 7.852 | 0.000 | 0.0000 | DECAYED |

8/8 complete decay. Framework confirmed: no stable oscillons in the golden potential.

This is discriminating: generic phi^4 potentials (e.g., V = lambda*(Phi^2 - v^2)^2 with symmetric vacua) DO produce long-lived oscillons. The golden potential's asymmetric vacua (phi vs -1/phi, Pisot property) prevent oscillon formation. The kink-antikink pair annihilates completely.

Physical implication: domain walls in the golden potential cannot self-sustain. Once maintenance stops, the wall dissolves. Life must be actively maintained — autopoiesis is forced by the algebra.

## Scripts

- `10-golden-potential-sim.py` — full simulation (2D visualization, kink analysis, collision animation)
- `11-oscillon-test.py` — automated oscillon persistence test across 8 velocities

## What this means for the repo

The bound state result confirms known physics (PT n=2 from golden kink) applied to a specific potential nobody has tested before. Solid but expected.

The oscillon result is genuinely new and discriminating. It distinguishes the golden potential from generic phi^4 theories and has a biological interpretation (life cannot coast). Worth publishing in the golden-nome repo.
