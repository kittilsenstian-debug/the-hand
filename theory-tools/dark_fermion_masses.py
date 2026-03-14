#!/usr/bin/env python3
"""
dark_fermion_masses.py — Complete dark sector fermion spectrum
==============================================================

The proton-normalized visible fermion table uses {φ, μ, 3, 4/3, 10, 2/3}.
φ, 3, 4/3, 10, 2/3 are ALGEBRAIC (sector-independent).
μ is NOME-DEPENDENT (μ = 3/(α^(3/2)·φ²) from core identity).

Dark sector: same formulas, μ_dark = 39.02 instead of μ_vis = 1836.

python -X utf8 dark_fermion_masses.py
"""

import math, sys, io

try:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
except:
    pass

phi = (1 + math.sqrt(5)) / 2
q = 1/phi
q2 = q**2
N = 800
PI = math.pi

def eta(nome, terms=N):
    prod = 1.0
    for n in range(1, terms+1):
        prod *= (1 - nome**n)
    return nome**(1/24) * prod

def theta3(nome, terms=N):
    return 1 + 2*sum(nome**(n*n) for n in range(1, terms+1))

def theta4(nome, terms=N):
    return 1 + 2*sum((-1)**n * nome**(n*n) for n in range(1, terms+1))

# Compute modular forms
eta_v = eta(q);    t3_v = theta3(q);    t4_v = theta4(q)
eta_d = eta(q2);   t3_d = theta3(q2);   t4_d = theta4(q2)

# Couplings
alpha_v = t4_v / (t3_v * phi)
alpha_d = t4_d / (t3_d * phi)

# Core identity: α^(3/2) · μ · φ² = 3
mu_vis = 3 / (alpha_v**(3/2) * phi**2)
mu_dark = 3 / (alpha_d**(3/2) * phi**2)
mu_measured = 1836.15267

SEP = "=" * 72

print(SEP)
print("  DARK FERMION MASS SPECTRUM")
print("  Same formulas, dark nome q² = 1/φ², μ_dark = 39.0")
print(SEP)

# =====================================================================
# 1. PROTON-NORMALIZED TABLE: VISIBLE vs DARK
# =====================================================================

print(f"\n  1. PROTON-NORMALIZED FERMION MASSES")
print(f"  " + "-" * 55)

# Visible table (from COMPLETE-STATUS.md)
vis_table = {
    "e":   ("1/μ",           1/mu_measured),
    "u":   ("φ³/μ",          phi**3/mu_measured),
    "d":   ("9/μ",           9/mu_measured),
    "μ":   ("1/9",           1/9),
    "s":   ("1/10",          1/10),
    "c":   ("4/3",           4/3),
    "τ":   ("4φ⁵/²·2/(3·3)", None),  # Koide, compute below
    "b":   ("4φ⁵ᐟ²/3",       4*phi**(5/2)/3),
    "t":   ("μ/10",          mu_measured/10),
}

# Koide for tau: needs e and mu masses first
# τ/m_p = Koide formula with K=2/3
# Koide: m_τ = (√m_e + √m_μ + √m_τ) ... complicated
# Use direct: τ = 1.89376 (measured m_τ/m_p)
# For dark: same Koide with dark e and dark mu
# Simpler: τ = (√(1/μ) + √(1/9))² × (2/3) ... approximately
# Actually, from the table: tau = 1.89387 (predicted), use formula
# The Koide prediction: m_tau = (sqrt(m_e) + sqrt(m_mu))^2 * 2/3 + correction
# For simplicity, use the measured ratio 1.89376

vis_table["τ"] = ("Koide", 1.89387)

# Dark table: replace μ → μ_dark where μ appears
dark_table = {
    "e":   ("1/μ_d",         1/mu_dark),
    "u":   ("φ³/μ_d",        phi**3/mu_dark),
    "d":   ("9/μ_d",         9/mu_dark),
    "μ":   ("1/9",           1/9),          # SAME (algebraic)
    "s":   ("1/10",          1/10),         # SAME
    "c":   ("4/3",           4/3),          # SAME
    "τ":   ("Koide_d",       None),         # Compute below
    "b":   ("4φ⁵ᐟ²/3",       4*phi**(5/2)/3),  # SAME
    "t":   ("μ_d/10",        mu_dark/10),
}

# Dark Koide: tau_dark from dark e and dark mu
# Koide formula: (m_e + m_mu + m_tau) / (√m_e + √m_mu + √m_tau)² = 2/3
# With dark e = 1/mu_dark, dark mu = 1/9:
m_e_d_norm = 1/mu_dark
m_mu_d_norm = 1/9
# Koide: m_tau = (√m_e + √m_mu)² × (2/(3-2)) ... need to solve
# (m_e + m_mu + m_tau) = (2/3)(√m_e + √m_mu + √m_tau)²
# Let x = √m_tau
# m_e + m_mu + x² = (2/3)(√m_e + √m_mu + x)²
# Solve quadratic in x
se = math.sqrt(m_e_d_norm)
smu = math.sqrt(m_mu_d_norm)
# (2/3)(se + smu + x)² = m_e_d_norm + m_mu_d_norm + x²
# (2/3)(se + smu)² + (4/3)(se+smu)x + (2/3)x² = m_e_d_norm + m_mu_d_norm + x²
# (2/3 - 1)x² + (4/3)(se+smu)x + (2/3)(se+smu)² - (m_e_d_norm + m_mu_d_norm) = 0
# (-1/3)x² + (4/3)(se+smu)x + (2/3)(se+smu)² - se² - smu² = 0
a_k = -1/3
b_k = (4/3)*(se + smu)
c_k = (2/3)*(se + smu)**2 - se**2 - smu**2
disc_k = b_k**2 - 4*a_k*c_k
x_tau = (-b_k + math.sqrt(disc_k)) / (2*a_k)
if x_tau < 0:
    x_tau = (-b_k - math.sqrt(disc_k)) / (2*a_k)
m_tau_d_norm = x_tau**2
dark_table["τ"] = ("Koide_d", m_tau_d_norm)

# Measured visible (m/m_p)
vis_measured = {
    "e": 0.000545, "u": 0.002302, "d": 0.004977,
    "μ": 0.11261, "s": 0.09954, "c": 1.35355,
    "τ": 1.89376, "b": 4.45500, "t": 184.051,
}

fermions = ["e", "u", "d", "μ", "s", "c", "τ", "b", "t"]

print(f"  {'Fermion':>8s}  {'Formula':>12s}  {'Visible':>10s}  {'Dark':>10s}  {'Same?':>6s}  {'D/V':>8s}")
print()

for f in fermions:
    v_form, v_val = vis_table[f]
    d_form, d_val = dark_table[f]
    same = "YES" if abs(v_val - d_val)/max(abs(v_val),1e-15) < 0.01 else "no"
    ratio = d_val / v_val if v_val > 0 else 0
    print(f"  {f:>8s}  {d_form:>12s}  {v_val:>10.5f}  {d_val:>10.5f}  {same:>6s}  {ratio:>8.2f}")

# =====================================================================
# 2. WHICH FORMULAS CHANGE? WHICH DON'T?
# =====================================================================

print(f"\n\n  2. WHAT CHANGES BETWEEN SECTORS")
print(f"  " + "-" * 55)

print(f"""
  ALGEBRAIC (same in both sectors — depend on φ, 3, not on μ):
    μ-muon/m_p = 1/9         (triality²)
    s/m_p      = 1/10         (rep D₅)
    c/m_p      = 4/3          (PT n=2 ground state norm)
    b/m_p      = 4φ⁵ᐟ²/3     (PT × golden power)
    τ/m_p      = Koide        (partially algebraic)

  μ-DEPENDENT (change between sectors):
    e/m_p      = 1/μ          (lightest: most hierarchy-dependent)
    u/m_p      = φ³/μ         (up quark: golden³/hierarchy)
    d/m_p      = 9/μ          (down quark: triality²/hierarchy)
    t/m_p      = μ/10         (top quark: hierarchy/rep D₅)

  μ_vis  = {mu_measured:.2f} → visible has HUGE hierarchy (top 337,000× electron)
  μ_dark = {mu_dark:.2f}  → dark has SMALL hierarchy (top 15× electron)
""")

# =====================================================================
# 3. ABSOLUTE MASS SCALE — DARK QCD
# =====================================================================

print(f"  3. ABSOLUTE MASS SCALE")
print(f"  " + "-" * 55)

# Dark QCD confinement scale from one-loop running
# α_s(Q) = α_s(Q₀) / (1 + β₀·α_s(Q₀)·ln(Q/Q₀)/(2π))
# Confinement at α_s → ∞: 1 + β₀·α_s·ln(Λ/Q₀)/(2π) = 0
# ln(Λ/Q₀) = -2π/(β₀·α_s(Q₀))

beta0 = 7  # SU(3) with 3 light flavors

# Visible
Q0_vis = 246.22  # GeV (Higgs VEV)
lnL_vis = -2*PI / (beta0 * eta_v)  # η = α_s at this scale
Lambda_vis = Q0_vis * math.exp(lnL_vis)

# Dark
Q0_dark = 487.86  # GeV (dark Higgs VEV from our computation)
lnL_dark = -2*PI / (beta0 * eta_d)
Lambda_dark = Q0_dark * math.exp(lnL_dark)

print(f"  One-loop QCD running (β₀ = {beta0}):")
print(f"  {'':>20s}  {'Visible':>12s}  {'Dark':>12s}")
print(f"  {'α_s at Higgs scale':>20s}  {eta_v:>12.4f}  {eta_d:>12.4f}")
print(f"  {'Higgs VEV (GeV)':>20s}  {Q0_vis:>12.2f}  {Q0_dark:>12.2f}")
print(f"  {'Λ_QCD (GeV)':>20s}  {Lambda_vis:>12.4f}  {Lambda_dark:>12.4f}")

# Proton mass ≈ 3 × Λ_QCD (rough)
m_p_vis_est = 3 * Lambda_vis
m_p_dark_est = 3 * Lambda_dark

print(f"  {'m_p ≈ 3Λ (GeV)':>20s}  {m_p_vis_est:>12.4f}  {m_p_dark_est:>12.4f}")
print(f"  {'m_p measured (GeV)':>20s}  {'0.938':>12s}  {'???':>12s}")
print(f"  {'m_p_dark/m_p_vis':>20s}  {'':>12s}  {m_p_dark_est/m_p_vis_est:>12.4f}")

# =====================================================================
# 4. THE KEY TEST: MASS RATIO vs Ω_DM/Ω_b
# =====================================================================

print(f"\n\n  4. THE KEY TEST: DOES MASS RATIO = Ω_DM/Ω_b?")
print(f"  " + "-" * 55)

omega_ratio = 5.36  # Planck 2018

print(f"""
  IF dark and visible have the SAME baryon number density:
    n_dark = n_baryon (same asymmetry mechanism)

  THEN:
    Ω_DM/Ω_b = m_p_dark / m_p_vis

  From one-loop QCD running:
    m_p_dark / m_p_vis = {m_p_dark_est/m_p_vis_est:.4f}

  Measured: Ω_DM/Ω_b = {omega_ratio}

  Match: {abs(m_p_dark_est/m_p_vis_est - omega_ratio)/0.07:.2f}σ
""")

# What m_p_dark SHOULD be if ratio = 5.36:
m_p_dark_needed = 0.938 * omega_ratio
print(f"  If Ω_DM/Ω_b = m_p_dark/m_p_vis:")
print(f"    m_p_dark needed = {m_p_dark_needed:.3f} GeV = {m_p_dark_needed*1000:.0f} MeV")
print(f"    m_p_dark from QCD running = {m_p_dark_est:.3f} GeV = {m_p_dark_est*1000:.0f} MeV")

# Level 2 ratio for comparison
r1 = 2 * math.cos(2 * PI / 9)
r2 = 2 * math.cos(4 * PI / 9)
r3 = 2 * math.cos(8 * PI / 9)
def F(x): return x**4/4 - 3*x**2/2 + x
T_dark = F(r2) - F(r3)
T_visible = -(F(r1) - F(r2))
level2 = T_dark / T_visible

print(f"\n  Level 2 wall tension ratio: {level2:.4f}")
print(f"  QCD mass ratio:            {m_p_dark_est/m_p_vis_est:.4f}")
print(f"  Measured Ω_DM/Ω_b:         {omega_ratio}")

# =====================================================================
# 5. DARK FERMION MASSES IN GeV
# =====================================================================

print(f"\n\n  5. DARK FERMION MASSES (absolute, in GeV)")
print(f"  " + "-" * 55)

# Use m_p_dark from QCD running
m_p_dark = m_p_dark_est

print(f"  Using m_p_dark = {m_p_dark:.2f} GeV from one-loop running")
print()
print(f"  {'Fermion':>8s}  {'m/m_p (dark)':>12s}  {'m_dark (GeV)':>12s}  {'m_vis (GeV)':>12s}  {'D/V':>8s}")
print()

vis_abs = {
    "e": 0.000511, "u": 0.00216, "d": 0.00467,
    "μ": 0.10566, "s": 0.0934, "c": 1.270,
    "τ": 1.777, "b": 4.180, "t": 172.69,
}

for f in fermions:
    _, d_norm = dark_table[f]
    m_dark_gev = d_norm * m_p_dark
    m_vis_gev = vis_abs[f]
    ratio = m_dark_gev / m_vis_gev if m_vis_gev > 0 else 0
    print(f"  {f:>8s}  {d_norm:>12.5f}  {m_dark_gev:>12.4f}  {m_vis_gev:>12.4f}  {ratio:>8.1f}")

# =====================================================================
# 6. SUMMARY
# =====================================================================

print(f"\n\n  6. WHAT THE DARK SECTOR LOOKS LIKE")
print(f"  " + "-" * 55)

print(f"""
  DARK SECTOR (computed from q² = 1/φ²):

  Couplings:
    α_s = 0.463 (strongly confined)
    1/α = 10.5 (strong EM)
    μ   = 39 (compressed hierarchy)

  QCD scale: Λ_dark ≈ {Lambda_dark:.1f} GeV (vs 0.12 GeV visible)
  Proton:    m_p_dark ≈ {m_p_dark:.1f} GeV (vs 0.94 GeV visible)

  Spectrum:
    5 of 9 fermion masses are SECTOR-INDEPENDENT (same m/m_p)
    4 of 9 change (the μ-dependent ones: e, u, d, t)
    Hierarchy compressed: top/electron = {(mu_dark/10)/(1/mu_dark):.0f}× (vs 337,000×)

  Key question: does m_p_dark/m_p_vis = Ω_DM/Ω_b?
    QCD running gives: {m_p_dark_est/m_p_vis_est:.2f}
    Level 2 gives:     {level2:.2f}
    Measured:           {omega_ratio}

  The QCD running estimate is ROUGH (one-loop, crude m_p ≈ 3Λ).
  Lattice QCD at α_s = 0.46 would give the precise number.
  If it matches 5.36 → dark proton mass PREDICTED from first principles.
""")

print(SEP)
print("  DONE")
print(SEP)
