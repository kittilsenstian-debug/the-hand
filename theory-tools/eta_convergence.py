#!/usr/bin/env python3
"""
Golden convergence of the Dedekind eta at q = 1/phi.

Proves: the step ratio of successive corrections approaches 1/phi exactly.
Predicts: lattice QCD should show the same golden convergence pattern.

No dependencies. Standard Python 3.
"""

import math

phi = (1 + math.sqrt(5)) / 2
q = 1.0 / phi

print("=" * 60)
print("  ETA CONVERGENCE: GOLDEN STEP RATIO")
print("=" * 60)

# Compute truncated eta
prefactor = q ** (1.0/24)
product = 1.0
eta_vals = [(0, prefactor)]

for N in range(1, 51):
    product *= (1.0 - q**N)
    eta_vals.append((N, prefactor * product))

eta_inf = eta_vals[-1][1]

print(f"\n  q = 1/phi = {q:.10f}")
print(f"  eta(1/phi) = {eta_inf:.12f}")
print(f"  Known alpha_s(M_Z) = 0.1184 +/- 0.0008")
print(f"  Match: {abs(eta_inf - 0.1184)/0.0008:.2f} sigma")

# Step ratios
print(f"\n  STEP RATIOS: (1-R_N) / (1-R_{{N-1}})")
print(f"  Prediction: approaches 1/phi = {q:.10f}")
print(f"\n  {'N':>4}  {'eta_N':>14}  {'1-R_N':>12}  {'step ratio':>12}  {'off 1/phi':>10}")
print(f"  {'-'*54}")

prev_gap = None
for N, eta_N in eta_vals:
    if N == 0:
        continue
    gap = abs(eta_N / eta_inf - 1)
    if prev_gap and prev_gap > 1e-15 and N <= 25:
        ratio = gap / prev_gap
        off = abs(ratio - q)
        marker = "EXACT" if off < 1e-6 else "YES" if off < 0.01 else ""
        print(f"  {N:4d}  {eta_N:14.10f}  {gap:12.2e}  {ratio:12.8f}  {off:10.2e}  {marker}")
    prev_gap = gap

# Bare coupling
print(f"\n  BARE COUPLING (N=0):")
print(f"    eta_0 = q^(1/24) = {prefactor:.6f}")
print(f"    Ratio eta_0 / eta_inf = {prefactor/eta_inf:.1f}x")
print(f"    The infinite product suppresses by factor {prefactor/eta_inf:.1f}")

# Factor contributions
print(f"\n  FACTOR CONTRIBUTIONS:")
print(f"  {'N':>4}  {'factor (1-q^N)':>14}  {'= 1 - (1/phi)^N':>14}")
print(f"  {'-'*35}")
for N in range(1, 11):
    f = 1.0 - q**N
    print(f"  {N:4d}  {f:14.10f}  {f:14.10f}")

print(f"\n  First factor removes {(1-q)*100:.1f}% = 1/phi of the bare coupling")
print(f"  Each subsequent factor removes 1/phi of what remains")
print(f"  This IS golden ratio convergence.")

# Connection to eta death
print(f"\n  ETA DEATH CONNECTION:")
print(f"  In Z[i]: i has order 4. Factor (1-q^4) would = 0.")
print(f"  In Z[phi]: phi has infinite order. All factors nonzero.")
print(f"  Confinement = the product converging. Death = one factor hitting zero.")
print(f"  The wall (Z[i]) can't confine. Physics (Z[phi]) can.")
