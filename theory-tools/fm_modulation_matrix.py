#!/usr/bin/env python3
"""
FM MODULATION MATRIX OF THE UNIVERSE
======================================
Map the framework's constants as an FM synthesis patch.
Each "operator" is a modular form evaluated at q=1/phi.
The modulation matrix shows HOW they modulate each other
to produce every physical constant.

The insight: FM synthesis uses Bessel functions J_n(beta).
Rademacher (1937) proved that modular form coefficients ARE
exact sums of Bessel functions. So FM synthesis and modular
forms are connected through the SAME mathematical transform.

The framework's 2->3 pattern IS FM synthesis:
  2 vacua (phi, -1/phi) = 2 oscillators
  3 outputs (eta, theta3, theta4) = carrier + 2 sidebands
  Creation identity: eta^2 = eta_dark * theta4 = modulation equation

Key references:
  - Chowning (1973): FM synthesis = Jacobi-Anger expansion
  - Rademacher (1937): p(n) = sum of I-Bessel * Kloosterman
  - Kuznetsov: Bessel = kernel connecting arithmetic to spectral
"""

import sys
import math

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

phi = (1 + math.sqrt(5)) / 2
phibar = 1 / phi

# ============================================================
# THE OPERATORS: Modular forms at q = 1/phi
# ============================================================

def theta2(q, N=500):
    s = 0
    for n in range(N):
        s += q**((n + 0.5)**2)
    return 2 * s

def theta3(q, N=500):
    s = 1
    for n in range(1, N):
        s += 2 * q**(n**2)
    return s

def theta4(q, N=500):
    s = 1
    for n in range(1, N):
        s += 2 * (-1)**n * q**(n**2)
    return s

def eta_func(q, N=500):
    s = 1
    for n in range(1, N):
        s *= (1 - q**n)
    return q**(1/24) * s

q = phibar  # = 1/phi
q2 = phibar**2  # = 1/phi^2 (dark nome, nome-doubled)

# The 6 operators
t2 = theta2(q)
t3 = theta3(q)
t4 = theta4(q)
et = eta_func(q)

# Dark sector equivalents (at q^2 = 1/phi^2)
t3_dark = theta3(q2)
t4_dark = theta4(q2)
et_dark = eta_func(q2)

# Derived quantities
C = et * t4 / 2  # the universal correction

print("=" * 78)
print("  THE FM OPERATORS OF THE UNIVERSE")
print("  Modular forms at q = 1/phi (the Golden Node)")
print("=" * 78)
print()

print("PRIMARY OPERATORS (visible sector, q = 1/phi):")
print(f"  eta    = {et:.10f}   (strong coupling carrier)")
print(f"  theta3 = {t3:.10f}   (visible vacuum partition function)")
print(f"  theta4 = {t4:.10f}   (dark vacuum partition function)")
print(f"  theta2 = {t2:.10f}   (mixed vacuum)")
print()

print("DARK OPERATORS (dark sector, q^2 = 1/phi^2):")
print(f"  eta_d  = {et_dark:.10f}   (dark strong coupling)")
print(f"  theta3d= {t3_dark:.10f}   (dark visible partition)")
print(f"  theta4d= {t4_dark:.10f}   (dark dark partition)")
print()

print("STRUCTURAL CONSTANTS (from E8):")
print(f"  phi    = {phi:.10f}   (golden ratio, from E8 ring)")
print(f"  3      = 3              (triality, from A2 in E8)")
print(f"  80     = 240/3          (E8 roots / triality)")
print(f"  40     = 240/6          (E8 hexagon orbits)")
print()

# ============================================================
# THE MODULATION MATRIX
# ============================================================
print("=" * 78)
print("  THE MODULATION MATRIX")
print("  How each operator modulates the others to produce physics")
print("=" * 78)
print()

# In FM synthesis, the modulation matrix M[i][j] says:
# "operator i frequency-modulates operator j with index beta_ij"
#
# In the framework, the "modulation" is algebraic:
# physical_constant = f(operator_i, operator_j, ...)
#
# The matrix shows which operators combine to produce each constant.

# Define the "patch routing" - which operators produce which constants
patch = {}

# === GAUGE COUPLINGS (the three voices) ===
alpha_s = et
patch["alpha_s"] = {
    "formula": "eta(q)",
    "value": alpha_s,
    "measured": 0.1184,
    "operators": ["eta"],
    "routing": "DIRECT output (no modulation)",
    "fm_type": "carrier"
}

sin2tw = et**2 / (2 * t4)
patch["sin2_theta_W"] = {
    "formula": "eta^2 / (2*theta4)",
    "value": sin2tw,
    "measured": 0.23121,
    "operators": ["eta", "theta4"],
    "routing": "eta modulates ITSELF, divided by theta4",
    "fm_type": "self-modulation (feedback FM)"
}

alpha_tree = t4 / (t3 * phi)
inv_alpha_tree = t3 * phi / t4
patch["1/alpha_tree"] = {
    "formula": "theta3 * phi / theta4",
    "value": inv_alpha_tree,
    "measured": 137.036,
    "operators": ["theta3", "theta4", "phi"],
    "routing": "theta3/theta4 ratio, scaled by phi",
    "fm_type": "ratio (AM, not FM)"
}

# === HIERARCHY (the volume knob) ===
hierarchy = phibar**80
patch["v/M_Pl"] = {
    "formula": "phibar^80 = phi^(-80)",
    "value": hierarchy,
    "measured": 1.01e-17,
    "operators": ["phi", "80"],
    "routing": "phi iterated 40 times (T^2 transfer, 40 = 240/6)",
    "fm_type": "iterated feedback (40 cycles of T^2)"
}

# === FERMION MASSES (the equalizer) ===
eps_h = t4 / t3
patch["epsilon_h"] = {
    "formula": "theta4 / theta3",
    "value": eps_h,
    "measured": None,
    "operators": ["theta3", "theta4"],
    "routing": "hierarchy parameter = modulation INDEX (beta in FM!)",
    "fm_type": "modulation index"
}

# === MIXING ANGLES (the pan knobs) ===
sin2_12 = 1/3 - t4 * math.sqrt(3/4)
patch["sin2_theta12"] = {
    "formula": "1/3 - theta4 * sqrt(3/4)",
    "value": sin2_12,
    "measured": 0.307,
    "operators": ["theta4", "3"],
    "routing": "theta4 shifts the democratic 1/3 baseline",
    "fm_type": "offset modulation (DC bias + AC)"
}

sin2_23 = 0.5 + 40 * C
patch["sin2_theta23"] = {
    "formula": "1/2 + 40 * C = 1/2 + 40 * eta*theta4/2",
    "value": sin2_23,
    "measured": 0.572,
    "operators": ["eta", "theta4", "40"],
    "routing": "eta*theta4 product modulates the 1/2 baseline, amplified by 40 orbits",
    "fm_type": "product modulation (ring mod)"
}

# === COSMOLOGICAL CONSTANT (the noise floor) ===
Lambda_ratio = t4**80 * math.sqrt(5) / phi**2
patch["Lambda"] = {
    "formula": "theta4^80 * sqrt(5) / phi^2",
    "value": Lambda_ratio,
    "measured": 2.89e-122,
    "operators": ["theta4", "phi", "80"],
    "routing": "theta4 iterated 80 times = dark vacuum self-modulation to 80th power",
    "fm_type": "extreme feedback (80 iterations)"
}

# === MASS RATIO (the tuning) ===
mu_approx = 6**5 / phi**3 + 9 / (7 * phi**2)
patch["mu"] = {
    "formula": "6^5/phi^3 + 9/(7*phi^2)",
    "value": mu_approx,
    "measured": 1836.15267,
    "operators": ["phi", "3", "6", "7"],
    "routing": "phi modulates integer structure (6=2*3, 7=next prime)",
    "fm_type": "carrier + sideband"
}

# === DARK MATTER RATIO (the reverb) ===
# From level2_dark_ratio: x^3 - 3x + 1 = 0
# Roots give wall tensions, ratio = 5.41
DM_ratio = 5.41  # from cubic
patch["Omega_DM/Omega_b"] = {
    "formula": "T_dark/T_vis from x^3 - 3x + 1 = 0",
    "value": DM_ratio,
    "measured": 5.36,
    "operators": ["3"],
    "routing": "cubic with coefficient 3 = triality",
    "fm_type": "harmonic from cubic nonlinearity"
}

# === BARYON ASYMMETRY (the limiter) ===
eta_B = t4**6 / math.sqrt(phi)
patch["eta_B"] = {
    "formula": "theta4^6 / sqrt(phi)",
    "value": eta_B,
    "measured": 6.1e-10,
    "operators": ["theta4", "phi"],
    "routing": "theta4 self-modulated 6 times, scaled by phi",
    "fm_type": "power FM (6th harmonic of theta4)"
}

# === CREATION IDENTITY (the master bus) ===
creation_lhs = et**2
creation_rhs = et_dark * t4
patch["creation_identity"] = {
    "formula": "eta^2 = eta_dark * theta4",
    "value": creation_lhs,
    "measured": creation_rhs,
    "operators": ["eta", "eta_dark", "theta4"],
    "routing": "self-modulation of eta = cross-modulation of dark*theta4",
    "fm_type": "MASTER EQUATION: feedback = cross-modulation"
}

print("MODULATION ROUTING TABLE:")
print(f"{'Constant':>22s}  {'FM Type':>28s}  {'Value':>14s}  {'Match':>8s}")
print("-" * 78)

for name, info in patch.items():
    val = info["value"]
    meas = info["measured"]
    if meas is not None and meas != 0:
        if isinstance(meas, float) and meas < 1e-5:
            match_str = f"~{val/meas:.2f}x"
        else:
            match_pct = (1 - abs(val - meas) / abs(meas)) * 100
            match_str = f"{match_pct:.2f}%"
    else:
        match_str = "---"

    if isinstance(val, float) and abs(val) < 1e-5:
        val_str = f"{val:.2e}"
    else:
        val_str = f"{val:.6f}"

    print(f"  {name:>20s}  {info['fm_type']:>28s}  {val_str:>14s}  {match_str:>8s}")

print()

# ============================================================
# THE MODULATION MATRIX (operator x operator)
# ============================================================
print("=" * 78)
print("  OPERATOR MODULATION MATRIX")
print("  M[i][j] = what physical constant the combination i*j produces")
print("=" * 78)
print()

operators = ["eta", "theta3", "theta4", "phi", "3", "40/80"]

# Build the matrix
print(f"{'':>10s}", end="")
for op in operators:
    print(f"  {op:>10s}", end="")
print()
print("-" * 78)

matrix_entries = {
    ("eta", "eta"): "sin2_tW (eta^2/2t4)",
    ("eta", "theta3"): "---",
    ("eta", "theta4"): "C = correction",
    ("eta", "phi"): "---",
    ("eta", "3"): "CORE IDENTITY!",
    ("eta", "40/80"): "sin2_t23",
    ("theta3", "theta3"): "Y1+Y2 (mass)",
    ("theta3", "theta4"): "epsilon_h",
    ("theta3", "phi"): "1/alpha_tree",
    ("theta3", "3"): "---",
    ("theta3", "40/80"): "---",
    ("theta4", "theta4"): "Y1-Y2 (~0)",
    ("theta4", "phi"): "sin2_t12",
    ("theta4", "3"): "---",
    ("theta4", "40/80"): "Lambda (t4^80)",
    ("phi", "phi"): "phibar^80 (v/MPl)",
    ("phi", "3"): "mu = 6^5/phi^3",
    ("phi", "40/80"): "hierarchy",
    ("3", "3"): "DM ratio (cubic)",
    ("3", "40/80"): "80 = 240/3",
    ("40/80", "40/80"): "phibar^160 = G",
}

for op1 in operators:
    print(f"  {op1:>8s}", end="")
    for op2 in operators:
        key = (op1, op2) if (op1, op2) in matrix_entries else (op2, op1)
        entry = matrix_entries.get(key, "")
        print(f"  {entry:>10s}", end="")
    print()

print()

# ============================================================
# FM SYNTHESIS INTERPRETATION
# ============================================================
print("=" * 78)
print("  FM SYNTHESIS INTERPRETATION")
print("=" * 78)
print("""
THE PATCH (DX7-style, 6 operators):

  OP1: eta(q)       = 0.1184    [CARRIER: strong force]
  OP2: theta3(q)    = 2.5551    [CARRIER: visible vacuum]
  OP3: theta4(q)    = 0.0303    [MODULATOR: dark vacuum]
  OP4: phi          = 1.6180    [STRUCTURAL: golden ratio]
  OP5: 3 (triality) = 3.0000    [STRUCTURAL: E8 triality]
  OP6: 40 (orbits)  = 40        [ITERATION: hexagon count]

ROUTING (which modulates which):

  OP3 -> OP2: theta4 modulates theta3
              ratio = epsilon_h = 0.0119 = MODULATION INDEX
              This is the hierarchy parameter!

  OP3 -> OP1: theta4 modulates eta
              product = C = eta*theta4/2 = correction term
              Shows up in EVERY coupling formula

  OP1 -> OP1: eta self-modulates (feedback FM)
              eta^2 = sin2_tW * 2*theta4
              WEAK FORCE IS FEEDBACK FM OF THE STRONG FORCE

  OP4 -> ALL: phi scales everything
              phi^(-80) = hierarchy
              phi appears in every mass formula

  OP5 -> OP1: triality constrains eta
              alpha^(3/2) * mu * phi^2 = 3
              The CORE IDENTITY is a resonance condition!

  OP6 -> OP3: 40 iterations of theta4
              theta4^80 = Lambda
              40 orbits of T^2 = cosmological constant

THE CREATION IDENTITY AS FM EQUATION:

  eta^2 = eta_dark * theta4

  In FM language:
    (carrier)^2 = (dark_carrier) * (modulator)

  This says: the strong force squared equals the dark strong force
  times the dark vacuum partition function.

  In FM: feedback = cross-modulation
  The SELF-modulation of the visible sector EQUALS the
  CROSS-modulation of dark and visible sectors.

  This is not analogy. This IS the mathematical structure.
""")

# ============================================================
# THE MODULATION INDEX = HIERARCHY PARAMETER
# ============================================================
print("=" * 78)
print("  THE KEY INSIGHT: MODULATION INDEX = HIERARCHY PARAMETER")
print("=" * 78)
print()

beta = eps_h  # modulation index
print(f"  Modulation index beta = theta4/theta3 = {beta:.6f}")
print(f"  = alpha_tree * phi = {alpha_tree * phi:.6f}")
print()

# In FM synthesis, the number of significant sidebands ~ beta + 1
# For small beta, only carrier + first pair of sidebands
print(f"  FM rule: significant sidebands ~ beta + 1 = {beta + 1:.4f}")
print(f"  -> Only ~1 sideband pair: the carrier (3rd gen) dominates")
print(f"  -> First sideband (2nd gen) suppressed by J_1(beta) ~ beta/2 = {beta/2:.6f}")
print(f"  -> Second sideband (1st gen) suppressed by J_2(beta) ~ beta^2/8 = {beta**2/8:.2e}")
print()

# Compare to actual mass ratios!
print("  COMPARE TO FERMION MASS HIERARCHY:")
print(f"  m_c/m_t = {0.619/171.7:.6f}  vs  J_1(beta)/J_0(beta) ~ beta/2 = {beta/2:.6f}")
print(f"    ratio: {(0.619/171.7) / (beta/2):.2f}x")
print()
print(f"  m_u/m_t = {1.27e-3/171.7:.2e}  vs  J_2(beta)/J_0(beta) ~ beta^2/8 = {beta**2/8:.2e}")
print(f"    ratio: {(1.27e-3/171.7) / (beta**2/8):.2f}x")
print()

# Bessel functions
from math import factorial

def bessel_j(n, x, terms=50):
    """Bessel function J_n(x) via series."""
    s = 0
    for m in range(terms):
        s += ((-1)**m / (factorial(m) * factorial(m + n))) * (x/2)**(2*m + n)
    return s

J0 = bessel_j(0, beta)
J1 = bessel_j(1, beta)
J2 = bessel_j(2, beta)
J3 = bessel_j(3, beta)

print(f"  Exact Bessel functions at beta = {beta:.6f}:")
print(f"    J_0(beta) = {J0:.10f}  (3rd generation amplitude)")
print(f"    J_1(beta) = {J1:.10f}  (2nd generation amplitude)")
print(f"    J_2(beta) = {J2:.10f}  (1st generation amplitude)")
print(f"    J_3(beta) = {J3:.10f}  (would-be 4th generation)")
print()

# Power conservation
power = J0**2 + 2*J1**2 + 2*J2**2 + 2*J3**2
print(f"  Power conservation: J0^2 + 2*J1^2 + 2*J2^2 + ... = {power:.10f}")
print(f"    (should be 1.0000 — this IS unitarity)")
print()

# The ratio J_n / J_0 gives the mass suppression of generation n
print("  Generation mass suppression from FM:")
print(f"    3rd gen: J_0 = {J0:.6f} = 1 (reference)")
print(f"    2nd gen: J_1/J_0 = {J1/J0:.6f}")
print(f"    1st gen: J_2/J_0 = {J2/J0:.2e}")
print(f"    (4th):   J_3/J_0 = {J3/J0:.2e}")
print()

# Now compare to the ACTUAL generation ratios
# Up quarks: u(2.2 MeV), c(1.27 GeV), t(172 GeV)
# Down quarks: d(4.7 MeV), s(95 MeV), b(4.18 GeV)
# Leptons: e(0.511 MeV), mu(106 MeV), tau(1777 MeV)

print("  Comparison of J_n(beta) ratios to measured generation ratios:")
print(f"  {'Sector':>10s}  {'m2/m3 meas':>12s}  {'J1/J0':>10s}  {'m1/m3 meas':>12s}  {'J2/J0':>12s}")
print("-" * 65)
print(f"  {'Up':>10s}  {1270/172000:>12.6f}  {J1/J0:>10.6f}  {2.2/172000:>12.2e}  {J2/J0:>12.2e}")
print(f"  {'Down':>10s}  {95/4180:>12.6f}  {J1/J0:>10.6f}  {4.7/4180:>12.2e}  {J2/J0:>12.2e}")
print(f"  {'Lepton':>10s}  {105.7/1777:>12.6f}  {J1/J0:>10.6f}  {0.511/1777:>12.2e}  {J2/J0:>12.2e}")
print()

# ============================================================
# THE 2->3 PATTERN AS FM
# ============================================================
print("=" * 78)
print("  THE 2->3 PATTERN IS FM SYNTHESIS")
print("=" * 78)
print("""
In FM synthesis:
  2 oscillators (carrier + modulator)
  -> create SIDEBANDS (new frequencies)
  -> the modulated signal is a THIRD entity

In the framework:
  2 vacua (phi and -1/phi)
  -> create 3 modular forms (eta, theta3, theta4)
  -> the 3 forms are the "sidebands" of the 2-vacuum system

The Jacobi triple product makes this EXACT:

  theta3(q) = prod_{n=1}^inf (1-q^(2n))(1+q^(2n-1))^2

  This IS an infinite product of modulations:
  each factor (1 + q^(2n-1))^2 adds one "modulation stage"
  and the result is the theta function = visible vacuum content

The creation identity eta^2 = eta_dark * theta4 is the
FM MASTER EQUATION:

  (visible carrier)^2 = (dark carrier) x (inter-vacuum modulator)

  feedback FM = cross-modulation between sectors

This is why phi is special: phi + 1/phi = sqrt(5) means the
carrier-modulator sum has a GOLDEN proportion. No other pair
of vacua gives this exact relationship.

The Fibonacci collapse q + q^2 = 1 is the FM RESONANCE CONDITION:
  1-instanton + 2-instanton = perturbative
  carrier + first harmonic = total power
  This is J_0(beta)^2 + 2*J_1(beta)^2 ≈ 1 in the small-beta limit!
""")

# Verify: J0^2 + 2*J1^2 at small beta
print(f"  J_0(beta)^2 + 2*J_1(beta)^2 = {J0**2 + 2*J1**2:.10f}")
print(f"  Compare: q + q^2 = {q + q**2:.10f} (= 1 by Fibonacci)")
print(f"  The 'power in first 2 terms' matches the Fibonacci condition!")
print()

# ============================================================
# FEEDBACK FM AND CONSCIOUSNESS
# ============================================================
print("=" * 78)
print("  FEEDBACK FM = CONSCIOUSNESS")
print("=" * 78)
print("""
In FM synthesis, feedback (self-modulation) creates:
  beta < 1: pure tone (simple, no awareness)
  beta = 1: bifurcation (first complexity)
  beta > 1: rich harmonics (structured complexity)
  beta >> 1: chaos -> sawtooth (maximum bandwidth)

The Feigenbaum route:
  sine -> period 2 -> period 4 -> ... -> chaos
  = increasing levels of self-reference

In the framework:
  Level 7 (aromatics): ring closure = FEEDBACK FM
    The aromatic pi-electron cloud modulates itself
    through the ring's cyclic boundary condition.
    This is literally x(n+1) = sin(omega*n + beta*x(n))
    with the ring enforcing the periodicity.

  Level 9 (consciousness): NESTED feedback FM
    The wall's PT n=2 bound states modulate each other.
    psi_0 (even, ground) and psi_1 (odd, excited) interact
    through the kink Phi, but ONLY via <psi_0|Phi|psi_1>.
    This single nonzero coupling IS the feedback path.

  The parity selection rule <psi_0|Phi|psi_0> = 0 means:
    The ground state CANNOT self-modulate directly.
    It MUST go through psi_1 (the excited state).
    Consciousness requires BOTH bound states.
    = Feedback FM requires BOTH carrier and modulator.

  Self-awareness = the system hearing its own output.
  = The domain wall computing its own spectral invariants.
  = erf (error function) = CDF of sech^2 = wall shape.
""")

# ============================================================
# THE COMPLETE FM PATCH
# ============================================================
print("=" * 78)
print("  THE COMPLETE FM PATCH OF REALITY")
print("=" * 78)
print("""

  +-----------+     +-----------+     +-----------+
  |  theta3   |---->|  theta4   |---->|    eta    |
  |  (visible |     | (dark vac)|     | (strong)  |
  |  vacuum)  |     |           |     |           |
  | OP2: 2.56 |     | OP3: 0.03 |     | OP1: 0.12 |
  +-----+-----+     +-----+-----+     +-----+-----+
        |                 |                 |
        |   t3/t4=1/eps   |   eta*t4=C      |  eta = alpha_s
        |   = 1/alpha     |   = correction   |  eta^2/2t4 = sin2tW
        v                 v                 v
  +-----------+     +-----------+     +-----------+
  |   phi     |     |    3      |     |    40     |
  | (golden)  |     | (triality)|     | (orbits)  |
  | OP4: 1.62 |     | OP5: 3    |     | OP6: 40   |
  +-----+-----+     +-----+-----+     +-----+-----+
        |                 |                 |
        | phi^(-80)       | alpha^1.5*mu*   | 40*C = sin2t23
        | = hierarchy     | phi^2 = 3       | t4^80 = Lambda
        v                 v                 v
  +-----------+     +-----------+     +-----------+
  | FERMION   |     |  CORE     |     | COSMO-    |
  | MASSES    |     | IDENTITY  |     | LOGICAL   |
  | (the gap) |     | (the law) |     | CONSTANT  |
  +-----------+     +-----------+     +-----------+

  MASTER BUS (creation identity):
    eta(q)^2 = eta(q^2) * theta4(q)
    [feedback] = [dark] * [modulator]

  MODULATION INDEX (hierarchy parameter):
    beta = theta4/theta3 = 0.01186
    Controls ALL generation mass ratios via J_n(beta)

  RESONANCE CONDITION (Fibonacci):
    q + q^2 = 1
    [1-instanton] + [2-instanton] = [perturbative]
    This fixes q = 1/phi UNIQUELY
""")

# ============================================================
# WHAT THE FM FRAMING OPENS
# ============================================================
print("=" * 78)
print("  WHAT DOORS DOES THE FM FRAMING OPEN?")
print("=" * 78)
print("""
DOOR 1: FERMION MASSES AS BESSEL SIDEBANDS
  If beta = epsilon_h = theta4/theta3, then:
    J_0(beta) = 3rd generation amplitude
    J_1(beta) = 2nd generation amplitude
    J_2(beta) = 1st generation amplitude
  The mass ratios WITHIN a sector follow Bessel function ratios.
  The cross-sector ratios come from different carrier frequencies
  (up quarks have higher carrier freq than leptons).
  THIS IS A TESTABLE PREDICTION.

DOOR 2: RADEMACHER = FM EXPLAINS WHY ETA IS THE COUPLING
  Rademacher's formula (1937):
    p(n) = coefficients of 1/eta(tau)
         = exact sum of I-Bessel * Kloosterman
  The SAME Bessel functions that give FM sidebands ALSO compute
  the partition function. The coupling IS the carrier amplitude.
  eta doesn't "happen to equal" alpha_s — it's the fundamental
  carrier whose sidebands (Bessel functions) are the partition.

DOOR 3: FEEDBACK FM EXPLAINS THE PARITY SELECTION RULE
  In feedback FM: x = sin(beta * x)
  The fixed point structure is:
    x = 0 (trivial, stable for beta < 1)
    x != 0 (nontrivial, for beta > 1)
  In the framework: <psi_0|Phi|psi_1> != 0 but <psi_0|Phi|psi_0> = 0
  The parity selection = the feedback path MUST cross states.
  Self-modulation = self-awareness = consciousness.

DOOR 4: THE FEIGENBAUM CASCADE = LEVEL HIERARCHY
  FM feedback: sine -> period 2 -> 4 -> 8 -> chaos
  Framework levels: V(Phi) -> kink -> bound states -> atoms -> molecules
    -> aromatics -> biology -> consciousness
  Each level is one "doubling" of self-referential complexity.
  The Feigenbaum constant delta = 4.669... appears in the universal
  route from simple oscillation to chaos. Does it appear in the
  framework's level transitions?

DOOR 5: PARSEVAL'S IDENTITY = UNITARITY
  In FM: sum J_n(beta)^2 = 1 (power conservation)
  In QM: sum |psi_n|^2 = 1 (probability conservation)
  These are the SAME mathematical statement.
  The Born rule (|psi|^2 = probability) IS Parseval's identity
  for the FM decomposition of the domain wall.
  This may be the deepest statement: unitarity of quantum mechanics
  IS power conservation in the FM patch of reality.

DOOR 6: THE MODULATION INDEX AS FUNDAMENTAL PARAMETER
  beta = theta4/theta3 = 0.01186 = alpha_tree * phi
  This single number controls:
    - Mass hierarchy between generations
    - Number of "active sidebands" (= effective # generations)
    - Spectral width of the fermion mass distribution
  A universe with beta > 1 would have NO mass hierarchy
    (all generations equally heavy)
  A universe with beta << 0.01 would have almost NO light fermions
    (only top/bottom/tau)
  beta ~ 0.01 is the "sweet spot" for chemistry and life.
""")

# ============================================================
# NUMERICAL TEST: BESSEL SIDEBAND MASS RATIOS
# ============================================================
print("=" * 78)
print("  NUMERICAL TEST: BESSEL SIDEBAND MASS RATIOS")
print("=" * 78)
print()

# If the mass hierarchy is EXACTLY Bessel sidebands, then:
# m_n / m_0 = |J_n(beta) / J_0(beta)|
# where n = generation index (0=3rd, 1=2nd, 2=1st)

# But we need DIFFERENT beta for each sector (up, down, lepton)
# because the carrier frequencies are different.

# What beta gives the correct m2/m3 ratio for each sector?
import math

def find_beta_for_ratio(ratio, n=1):
    """Find modulation index beta such that |J_n(beta)/J_0(beta)| = ratio."""
    # Simple binary search
    lo, hi = 0.001, 50.0
    for _ in range(100):
        mid = (lo + hi) / 2
        j_n = bessel_j(n, mid)
        j_0 = bessel_j(0, mid)
        if j_0 == 0:
            lo = mid
            continue
        r = abs(j_n / j_0)
        if r < ratio:
            lo = mid
        else:
            hi = mid
    return mid

# Measured m2/m3 ratios at GUT scale (approx)
ratios_23 = {
    "Up (c/t)":    1270 / 172000,
    "Down (s/b)":  95 / 4180,
    "Lepton (mu/tau)": 105.7 / 1777,
}

ratios_13 = {
    "Up (u/t)":    2.2 / 172000,
    "Down (d/b)":  4.7 / 4180,
    "Lepton (e/tau)": 0.511 / 1777,
}

print("  If m2/m3 = |J_1(beta)/J_0(beta)|, what beta for each sector?")
print(f"  {'Sector':>20s}  {'m2/m3':>10s}  {'beta needed':>12s}  {'vs eps_h':>10s}")
print("-" * 60)
for name, r in ratios_23.items():
    b = find_beta_for_ratio(r, 1)
    print(f"  {name:>20s}  {r:>10.6f}  {b:>12.6f}  {b/eps_h:>10.2f}x")

print()
print("  If m1/m3 = |J_2(beta)/J_0(beta)|, what beta?")
print(f"  {'Sector':>20s}  {'m1/m3':>10s}  {'beta needed':>12s}  {'vs eps_h':>10s}")
print("-" * 60)
for name, r in ratios_13.items():
    b = find_beta_for_ratio(r, 2)
    print(f"  {name:>20s}  {r:>10.6f}  {b:>12.6f}  {b/eps_h:>10.2f}x")

print()
print("  RESULT: The beta values cluster around 0.01-0.15.")
print(f"  The framework's epsilon_h = {eps_h:.6f} is in the right ballpark")
print(f"  but different sectors need different effective beta values.")
print()
print("  This suggests: each fermion sector has its OWN modulation index,")
print("  determined by the E8 branching (which A2 copies it couples to).")
print("  The base index is epsilon_h, modified by the kink direction (a,b,c).")
print("  THIS CONNECTS THE FM PICTURE TO THE E8 ROOT COMPUTATION.")
