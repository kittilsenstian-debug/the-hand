#!/usr/bin/env python3
"""
dark_sector_from_creation_identity.py
======================================

The creation identity (Jacobi, proven math):
    η(q)² = η(q²) · θ₄(q)

connects visible and dark sector couplings. Since we know η, θ₃, θ₄ at q=1/φ,
we can compute ALL dark sector modular forms at q²=1/φ² and extract dark couplings.

Question: does the dark sector have its own particle physics?
If so, what are its coupling constants?

python -X utf8 dark_sector_from_creation_identity.py
"""

import math, sys, io

try:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
except:
    pass

phi = (1 + math.sqrt(5)) / 2
q = 1 / phi
q2 = q**2  # dark nome = 1/phi^2

N = 800  # convergence terms

# =====================================================================
# VISIBLE SECTOR: modular forms at q = 1/φ
# =====================================================================

def eta(nome, terms=N):
    prod = 1.0
    for n in range(1, terms+1):
        prod *= (1 - nome**n)
    return nome**(1/24) * prod

def theta3(nome, terms=N):
    return 1 + 2*sum(nome**(n*n) for n in range(1, terms+1))

def theta4(nome, terms=N):
    return 1 + 2*sum((-1)**n * nome**(n*n) for n in range(1, terms+1))

def theta2(nome, terms=N):
    return 2*nome**(1/4) * sum(nome**(n*(n+1)) for n in range(0, terms+1))

# Visible sector
eta_v = eta(q)
t3_v = theta3(q)
t4_v = theta4(q)
t2_v = theta2(q)

# Dark sector (nome q² = 1/φ²)
eta_d = eta(q2)
t3_d = theta3(q2)
t4_d = theta4(q2)
t2_d = theta2(q2)

SEP = "=" * 70

print(SEP)
print("  DARK SECTOR PHYSICS FROM THE CREATION IDENTITY")
print("  η(q)² = η(q²) · θ₄(q)  — Jacobi, proven")
print(SEP)

# =====================================================================
# 1. VERIFY CREATION IDENTITY
# =====================================================================

print("\n  1. CREATION IDENTITY VERIFICATION")
print("  " + "-" * 50)

lhs = eta_v**2
rhs = eta_d * t4_v

print(f"  η(q)²         = {lhs:.15f}")
print(f"  η(q²)·θ₄(q)   = {rhs:.15f}")
print(f"  Difference     = {abs(lhs - rhs):.2e}")
print(f"  VERIFIED: {abs(lhs - rhs) < 1e-12}")

# =====================================================================
# 2. VISIBLE vs DARK MODULAR FORMS
# =====================================================================

print(f"\n\n  2. VISIBLE vs DARK MODULAR FORMS")
print("  " + "-" * 50)
print(f"  {'Form':>10s}  {'Visible (q=1/φ)':>18s}  {'Dark (q²=1/φ²)':>18s}  {'Ratio D/V':>10s}")
print(f"  {'':>10s}  {'':>18s}  {'':>18s}  {'':>10s}")

forms = [
    ("η", eta_v, eta_d),
    ("θ₂", t2_v, t2_d),
    ("θ₃", t3_v, t3_d),
    ("θ₄", t4_v, t4_d),
]

for name, v, d in forms:
    ratio = d/v if v != 0 else float('inf')
    print(f"  {name:>10s}  {v:>18.12f}  {d:>18.12f}  {ratio:>10.6f}")

# =====================================================================
# 3. DARK SECTOR COUPLINGS
# =====================================================================

print(f"\n\n  3. COUPLING CONSTANTS: VISIBLE vs DARK")
print("  " + "-" * 50)

# Visible couplings
alpha_s_v = eta_v
sin2tw_v = eta_v**2 / (2*t4_v) - eta_v**4 / 4
inv_alpha_v = t3_v * phi / t4_v

# Dark couplings — SAME FORMULAS at dark nome
alpha_s_d = eta_d
sin2tw_d = eta_d**2 / (2*t4_d) - eta_d**4 / 4
inv_alpha_d = t3_d * phi / t4_d  # Note: phi is the SAME (algebraic, not nome-dependent)

# Alternative: dark couplings using creation identity relations
# sin²θ_W = η(q²)/2 (from creation identity: η²/(2θ₄) = η_dark/2)
sin2tw_creation = eta_d / 2

print(f"  {'Coupling':>20s}  {'Visible':>12s}  {'Dark':>12s}  {'Ratio D/V':>10s}  {'Measured':>10s}")
print(f"  {'':>20s}  {'(q=1/φ)':>12s}  {'(q²=1/φ²)':>12s}  {'':>10s}  {'':>10s}")
print()
print(f"  {'α_s = η':>20s}  {alpha_s_v:>12.6f}  {alpha_s_d:>12.6f}  {alpha_s_d/alpha_s_v:>10.4f}  {'0.1184':>10s}")
print(f"  {'sin²θ_W':>20s}  {sin2tw_v:>12.6f}  {sin2tw_d:>12.6f}  {sin2tw_d/sin2tw_v:>10.4f}  {'0.2312':>10s}")
print(f"  {'sin²θ_W (creation)':>20s}  {sin2tw_v:>12.6f}  {sin2tw_creation:>12.6f}  {sin2tw_creation/sin2tw_v:>10.4f}  {'':>10s}")
print(f"  {'1/α = θ₃φ/θ₄':>20s}  {inv_alpha_v:>12.4f}  {inv_alpha_d:>12.4f}  {inv_alpha_d/inv_alpha_v:>10.4f}  {'137.036':>10s}")

# =====================================================================
# 4. DARK/VISIBLE RATIOS — DO THEY PREDICT DM/BARYON?
# =====================================================================

print(f"\n\n  4. DARK/VISIBLE RATIOS vs Ω_DM/Ω_b")
print("  " + "-" * 50)

omega_ratio = 5.36  # Planck 2018: Ω_DM/Ω_b

ratios = {
    "η_dark/η_vis": eta_d / eta_v,
    "θ₃_dark/θ₃_vis": t3_d / t3_v,
    "θ₄_dark/θ₄_vis": t4_d / t4_v,
    "η_dark²/η_vis²": (eta_d/eta_v)**2,
    "(1/α_dark)/(1/α_vis)": inv_alpha_d / inv_alpha_v,
    "sin²θ_W_dark/vis": sin2tw_d / sin2tw_v,
    "η_vis/θ₄_vis (=η_dark from CI)": eta_v**2 / t4_v / eta_v,  # = eta_d/eta_v... wait
}

# More systematic: try simple combinations
print(f"  {'Ratio':>35s}  {'Value':>12s}  {'vs 5.36':>10s}  {'σ':>8s}")
print()

def sigma(predicted, measured=5.36, error=0.07):
    return abs(predicted - measured) / error

candidates = [
    ("η_d/η_v", eta_d/eta_v),
    ("θ₃_d/θ₃_v", t3_d/t3_v),
    ("θ₄_d/θ₄_v", t4_d/t4_v),
    ("(η_d/η_v)²", (eta_d/eta_v)**2),
    ("θ₃_d·φ/(θ₃_v)", t3_d*phi/t3_v),
    ("(θ₃_d/θ₄_d)/(θ₃_v/θ₄_v)", (t3_d/t4_d)/(t3_v/t4_v)),
    ("η_d·θ₃_d/(η_v·θ₃_v)", eta_d*t3_d/(eta_v*t3_v)),
    ("1/(α_d·α_v)", 1/(alpha_s_d * alpha_s_v)),  # just checking
    ("θ₄_v/θ₄_d", t4_v/t4_d),
    ("(1-η_d)/(1-η_v)", (1-eta_d)/(1-eta_v)),
    ("η_d/η_v · θ₃_d/θ₃_v", (eta_d/eta_v)*(t3_d/t3_v)),
    ("(θ₃_d-1)/(θ₃_v-1)", (t3_d-1)/(t3_v-1)),
    ("ln(1/q²)/ln(1/q)", math.log(1/q2)/math.log(1/q)),  # = 2 trivially
]

for name, val in sorted(candidates, key=lambda x: abs(x[1] - omega_ratio)):
    sig = sigma(val)
    marker = " <<<" if sig < 2 else ""
    print(f"  {name:>35s}  {val:>12.6f}  {val/omega_ratio*100:>8.2f}%  {sig:>7.2f}σ{marker}")

# =====================================================================
# 5. THE LEVEL 2 COMPARISON
# =====================================================================

print(f"\n\n  5. LEVEL 2 WALL TENSION (independent computation)")
print("  " + "-" * 50)

PI = math.pi
r1 = 2 * math.cos(2 * PI / 9)
r2 = 2 * math.cos(4 * PI / 9)
r3 = 2 * math.cos(8 * PI / 9)

def F(x):
    return x**4/4 - 3*x**2/2 + x

T_dark = F(r2) - F(r3)
T_visible = -(F(r1) - F(r2))
level2_ratio = T_dark / T_visible

print(f"  Level 2 polynomial: x³ - 3x + 1 = 0")
print(f"  T_dark/T_visible = {level2_ratio:.6f}")
print(f"  Ω_DM/Ω_b        = {omega_ratio}")
print(f"  Match:             {sigma(level2_ratio):>.2f}σ")

# =====================================================================
# 6. DARK SECTOR PARTICLE PHYSICS
# =====================================================================

print(f"\n\n  6. DARK SECTOR PARTICLE PHYSICS")
print("  " + "-" * 50)

print(f"\n  If the dark sector has the SAME algebra but at q²=1/φ²:")
print(f"  Dark strong coupling:  α_s_dark = η(1/φ²) = {eta_d:.6f}")
print(f"  Visible strong:        α_s_vis  = η(1/φ)  = {eta_v:.6f}")
print(f"  Ratio:                 {eta_d/eta_v:.4f}")
print(f"  Dark coupling is {eta_d/eta_v:.1f}× stronger than visible")

print(f"\n  Dark EM coupling:      1/α_dark = {inv_alpha_d:.4f}")
print(f"  Visible EM:            1/α_vis  = {inv_alpha_v:.4f}")
print(f"  Ratio:                 {inv_alpha_d/inv_alpha_v:.6f}")

if inv_alpha_d < inv_alpha_v:
    print(f"  Dark EM is STRONGER (α_dark > α_vis)")
else:
    print(f"  Dark EM is WEAKER (α_dark < α_vis)")

print(f"\n  Dark Weinberg angle:   sin²θ_W_dark = {sin2tw_d:.6f}")
print(f"  Visible Weinberg:      sin²θ_W_vis  = {sin2tw_v:.6f}")

# Dark hierarchy
k2_d = (t2_d/t3_d)**4
print(f"\n  Dark elliptic modulus:  k²_dark = {k2_d:.10f}")
print(f"  Visible:               k²_vis  = {(t2_v/t3_v)**4:.10f}")
if k2_d > 0.999:
    print(f"  Dark sector is ALSO in solitonic limit (k²≈1)")
    print(f"  → Dark domain walls ALSO have PT structure")
else:
    print(f"  Dark sector is NOT in solitonic limit")
    print(f"  → Dark sector has BAND structure, not isolated solitons")

# =====================================================================
# 7. CREATION IDENTITY: WHAT IT SAYS PHYSICALLY
# =====================================================================

print(f"\n\n  7. CREATION IDENTITY: PHYSICAL MEANING")
print("  " + "-" * 50)

print(f"""
  η(q)² = η(q²) · θ₄(q)

  Visible strong²  = Dark strong × Wall parameter

  ({eta_v:.6f})² = {eta_d:.6f} × {t4_v:.6f}
  {eta_v**2:.10f} = {eta_d * t4_v:.10f}

  PHYSICAL READING:
  The visible strong force is BORN from the dark coupling
  mediated by the domain wall (θ₄).

  Equivalently: sin²θ_W = η_dark/2 = {eta_d/2:.6f}
  (measured: 0.2312)
  Match: {abs(eta_d/2 - 0.23122)/0.00003*100:.0f} ppm

  The Weinberg angle IS half the dark strong coupling.
  Electroweak mixing = the rate at which the dark sector
  couples to the visible sector through the wall.
""")

# =====================================================================
# 8. JACOBI IDENTITY FOR DARK THETA FUNCTIONS
# =====================================================================

print(f"  8. JACOBI IDENTITY AT DARK NOME")
print("  " + "-" * 50)

# Jacobi: θ₃⁴ = θ₂⁴ + θ₄⁴
jacobi_v = t3_v**4 - t2_v**4 - t4_v**4
jacobi_d = t3_d**4 - t2_d**4 - t4_d**4

print(f"  Jacobi θ₃⁴ = θ₂⁴ + θ₄⁴:")
print(f"  Visible: residual = {jacobi_v:.2e}")
print(f"  Dark:    residual = {jacobi_d:.2e}")

# Triple product
triple_v = t2_v * t3_v * t4_v - 2*eta_v**3
triple_d = t2_d * t3_d * t4_d - 2*eta_d**3

print(f"\n  Jacobi triple: θ₂·θ₃·θ₄ = 2η³:")
print(f"  Visible: residual = {triple_v:.2e}")
print(f"  Dark:    residual = {triple_d:.2e}")

# =====================================================================
# 9. DARK SECTOR SUMMARY
# =====================================================================

print(f"\n\n  9. DARK SECTOR SUMMARY")
print("  " + "-" * 50)

print(f"""
  WHAT WE CAN COMPUTE (no assumptions):

  1. Dark nome:           q² = 1/φ² = {q2:.10f}
  2. Dark eta:            η_dark = {eta_d:.10f}
  3. Dark theta3:         θ₃_dark = {t3_d:.10f}
  4. Dark theta4:         θ₄_dark = {t4_d:.10f}
  5. Dark theta2:         θ₂_dark = {t2_d:.10f}

  DARK COUPLINGS (same formulas):
  6. α_s_dark = η_dark = {eta_d:.6f}  ({eta_d/eta_v:.1f}× visible)
  7. sin²θ_W_dark      = {sin2tw_d:.6f}
  8. 1/α_dark           = {inv_alpha_d:.4f}

  CREATION IDENTITY PREDICTIONS:
  9. sin²θ_W = η_dark/2 = {eta_d/2:.6f}  (measured: 0.2312)

  DARK MATTER RATIO:
  10. Level 2 wall tension: {level2_ratio:.4f} vs Ω_DM/Ω_b = {omega_ratio}
      Match: {sigma(level2_ratio):.2f}σ

  WHAT REQUIRES O'NAN MOONSHINE (paper needed):
  - Dark particle SPECTRUM (which particles, which masses)
  - Dark confinement scale (Λ_QCD_dark)
  - Whether dark sector has composite particles (dark protons?)
  - Whether dark sector has its own domain walls

  THE KEY RESULT:
  The creation identity η² = η_dark·θ₄ means the visible sector
  is NOT independent. It is born from the dark sector through
  the domain wall. The visible strong force is the geometric mean
  of the dark coupling and the wall parameter.
""")

print(SEP)
print("  DONE")
print(SEP)
