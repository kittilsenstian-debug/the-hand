"""
REFINED analysis of the 0.027 ppm residual in Interface Theory alpha formula.

KEY INSIGHT FROM v1: The muon VP (+0.078), quark VP (+0.82), and 2-loop corrections
are each VASTLY larger than the 0.0000037 gap. This means Formula B is NOT simply
"electron VP only" — the Lambda_ref cutoff is ABSORBING all the other contributions.

The real question: Lambda_ref = m_p/phi^3 * (1 - eta/(3*phi^3)) is a SPECIFIC choice.
The 0.027 ppm residual tells us how well this SPECIFIC Lambda encodes the full running.

This script analyzes the gap at the level where it actually lives: the cutoff scale.
"""
import math

print("=" * 80)
print("REFINED ALPHA RESIDUAL ANALYSIS v2")
print("What the 0.027 ppm gap ACTUALLY tells us")
print("=" * 80)

# Constants
theta3 = 2.555093469444516
theta4 = 0.030311200785327
eta    = 0.118403904856684
phi    = (1 + math.sqrt(5)) / 2
pi     = math.pi

m_p  = 0.93827208816      # GeV
m_e  = 0.51099895000e-3   # GeV
m_mu = 0.1056583755       # GeV

alpha_meas = 1/137.035999206
inv_alpha_meas = 137.035999206

# Formula B computation
inv_alpha_tree = theta3 * phi / theta4
Lambda_raw = m_p / phi**3
refinement = 1 - eta / (3 * phi**3)
Lambda_ref = Lambda_raw * refinement
vp = (1/(3*pi)) * math.log(Lambda_ref / m_e)
inv_alpha_B = inv_alpha_tree + vp
residual = inv_alpha_meas - inv_alpha_B

print(f"\n  Formula B: 1/alpha = {inv_alpha_B:.12f}")
print(f"  Measured:  1/alpha = {inv_alpha_meas:.9f}")
print(f"  Residual:          = {residual:+.12f}  ({residual/inv_alpha_meas*1e6:+.3f} ppm)")

# ============================================================================
# KEY QUESTION: What is the structure of Formula B?
# ============================================================================
print("\n" + "=" * 80)
print("PART 1: What Formula B actually IS")
print("=" * 80)

print(f"""
  Formula B uses a SINGLE logarithm: (1/3pi) * ln(Lambda_ref / m_e)

  In standard QED, 1/alpha(0) comes from running alpha from high scale down to q=0:
    1/alpha(0) = 1/alpha(Lambda) + (2/3pi) * sum_f Nc*Qf^2 * ln(Lambda/mf)

  Formula B replaces this with:
    1/alpha(0) = theta3*phi/theta4 + (1/3pi) * ln(Lambda_ref / m_e)

  The tree level (theta3*phi/theta4 = {inv_alpha_tree:.6f}) is NOT 1/alpha(Lambda).
  Rather, it's a modular form expression that encodes the BARE coupling.

  The VP term uses coefficient 1/(3pi) — exactly HALF the standard 2/(3pi).
  This has been interpreted as Weyl (single chirality) on the domain wall.

  BUT: the formula only sums over the electron. It does NOT include muon, quarks, etc.
  Yet it gives 0.027 ppm precision!

  This means one of two things:
  (A) Lambda_ref implicitly absorbs all non-electron running, OR
  (B) The tree-level modular form already encodes something beyond bare QED
""")

# ============================================================================
# PART 2: Standard QED running — what Lambda_eff should be
# ============================================================================
print("=" * 80)
print("PART 2: Standard QED running analysis")
print("=" * 80)

# In standard QED, the running from scale Lambda down to 0 gives:
# 1/alpha(0) = 1/alpha(Lambda) + (2/3pi) * [ln(Lambda/m_e) + ln(Lambda/m_mu) + ...]
#
# If we rewrite this as a SINGLE effective log:
# 1/alpha(0) = 1/alpha(Lambda) + (2/3pi) * ln(Lambda_eff / m_e)
# where Lambda_eff absorbs all the running, then:
# ln(Lambda_eff/m_e) = ln(Lambda/m_e) + ln(Lambda/m_mu) + Nc*Q^2*ln(Lambda/m_q) + ...
#   = sum_f Nc*Qf^2 * ln(Lambda/mf)
# For single effective log with coefficient (1/3pi) instead of (2/3pi):
# (1/3pi)*ln(Lambda_eff/m_e) = total_running
# ln(Lambda_eff/m_e) = total_running * 3*pi

# But Formula B is NOT standard QED. It uses 1/(3pi) and only electron.
# The fact that it works means Lambda_ref ~ Lambda_eff for electron-only.

# Let's compute what Lambda the formula NEEDS to match experiment exactly:
target_vp = inv_alpha_meas - inv_alpha_tree
ln_needed = target_vp * 3 * pi
Lambda_exact = m_e * math.exp(ln_needed)

print(f"\n  Lambda needed for exact alpha: {Lambda_exact*1000:.6f} MeV")
print(f"  Lambda_ref from framework:     {Lambda_ref*1000:.6f} MeV")
print(f"  Difference:                    {(Lambda_exact - Lambda_ref)*1000:.6f} MeV")
print(f"  Fractional:                    {(Lambda_exact/Lambda_ref - 1)*1e6:.3f} ppm")

# ============================================================================
# PART 3: The coefficient question — is 1/(3pi) exact?
# ============================================================================
print("\n" + "=" * 80)
print("PART 3: The coefficient question")
print("=" * 80)

# Find the exact coefficient that makes Formula B exact with Lambda_ref:
C_exact = (inv_alpha_meas - inv_alpha_tree) / math.log(Lambda_ref / m_e)
C_half = 1 / (3*pi)
C_full = 2 / (3*pi)

print(f"\n  Coefficient analysis (using Lambda_ref = {Lambda_ref*1000:.3f} MeV):")
print(f"  C_exact = (alpha_meas - tree) / ln(Lambda_ref/m_e)")
print(f"  C_exact   = {C_exact:.15f}")
print(f"  C_half    = 1/(3pi) = {C_half:.15f}")
print(f"  C_full    = 2/(3pi) = {C_full:.15f}")
print(f"\n  C_exact / C_half = {C_exact/C_half:.15f}")
print(f"  C_exact - C_half = {C_exact - C_half:+.15e}")
print(f"  Fractional excess = {(C_exact/C_half - 1)*1e6:.3f} ppm of coefficient")

delta_C = C_exact - C_half
print(f"\n  The coefficient needs to be corrected by delta_C = {delta_C:.6e}")
print(f"  Relative to C_half: {delta_C/C_half:.6e}")

# What framework quantity matches this?
print(f"\n  Framework quantities of similar size:")
print(f"  alpha^2/(3pi)      = {alpha_meas**2/(3*pi):.6e}  (ratio: {delta_C/(alpha_meas**2/(3*pi)):.4f})")
print(f"  alpha/(3pi)^2      = {alpha_meas/(3*pi)**2:.6e}  (ratio: {delta_C/(alpha_meas/(3*pi)**2):.4f})")
print(f"  theta4/(3pi)       = {theta4/(3*pi):.6e}  (ratio: {delta_C/(theta4/(3*pi)):.4f})")
print(f"  eta*theta4/(3pi)   = {eta*theta4/(3*pi):.6e}  (ratio: {delta_C/(eta*theta4/(3*pi)):.4f})")
print(f"  theta4^2           = {theta4**2:.6e}  (ratio: {delta_C/theta4**2:.6f})")
print(f"  alpha^2            = {alpha_meas**2:.6e}  (ratio: {delta_C/alpha_meas**2:.6f})")
print(f"  alpha*theta4       = {alpha_meas*theta4:.6e}  (ratio: {delta_C/(alpha_meas*theta4):.4f})")

# ============================================================================
# PART 4: Dual analysis — Lambda shift vs coefficient shift
# ============================================================================
print("\n" + "=" * 80)
print("PART 4: Two equivalent ways to close the gap")
print("=" * 80)

# Way 1: Shift Lambda
dLambda = Lambda_exact - Lambda_ref
print(f"\n  WAY 1: Shift Lambda_ref by {dLambda*1000:+.6f} MeV")
print(f"    Lambda_ref -> {Lambda_exact*1000:.6f} MeV")
print(f"    This requires the refinement factor to change from")
print(f"    {refinement:.15f} to {refinement * Lambda_exact/Lambda_ref:.15f}")
print(f"    Additional refinement: {refinement * (Lambda_exact/Lambda_ref - 1):+.12e}")

# Way 2: Shift coefficient
print(f"\n  WAY 2: Shift coefficient from 1/(3pi) by {delta_C:+.6e}")
print(f"    C -> {C_exact:.15f}")
print(f"    Fractional shift: {delta_C/C_half:+.6e}")

# Way 3: Both together? What if there's a natural 2nd-order correction?
print(f"\n  WAY 3: Framework-natural correction to Lambda")
print(f"    Current: Lambda_ref = (m_p/phi^3) * (1 - eta/(3*phi^3))")
print(f"    = {Lambda_raw*1000:.6f} * (1 - {eta/(3*phi**3):.12f})")
print(f"    = {Lambda_raw*1000:.6f} * {refinement:.12f}")

# The leading refinement is eta/(3*phi^3).
# A natural 2nd-order term would be [eta/(3*phi^3)]^2 or eta^2/(9*phi^6)
eta_term = eta / (3*phi**3)
eta_squared_term = eta_term**2
needed_additional = refinement * (Lambda_exact/Lambda_ref - 1)

print(f"\n    Leading term:     eta/(3*phi^3) = {eta_term:.12f}")
print(f"    Squared term:     [eta/(3*phi^3)]^2 = {eta_squared_term:.12e}")
print(f"    Needed additional: {needed_additional:.12e}")
print(f"    Ratio needed/squared: {needed_additional/eta_squared_term:.6f}")

# What about eta^2/(3*phi^3)?
eta2_3phi3 = eta**2 / (3*phi**3)
print(f"\n    eta^2/(3*phi^3) = {eta2_3phi3:.12e}  (ratio: {needed_additional/eta2_3phi3:.6f})")

# eta*alpha?
eta_alpha = eta * alpha_meas
print(f"    eta*alpha = {eta_alpha:.12e}  (ratio: {needed_additional/eta_alpha:.6f})")

# alpha^2?
alpha2 = alpha_meas**2
print(f"    alpha^2 = {alpha2:.12e}  (ratio: {needed_additional/alpha2:.6f})")

# The actual scale of the needed correction
print(f"\n    Scale comparison:")
print(f"    needed = {needed_additional:.6e}")
print(f"    This is {needed_additional/eta_term:.6e} of the leading correction")
print(f"    = {needed_additional/eta_term*100:.4f}% of eta/(3*phi^3)")

# ============================================================================
# PART 5: Physical interpretation of the gap
# ============================================================================
print("\n" + "=" * 80)
print("PART 5: Physical interpretation")
print("=" * 80)

print(f"""
  THE KEY INSIGHT:

  The residual is +{residual:.9f} in 1/alpha ({residual/inv_alpha_meas*1e6:.3f} ppm).
  This corresponds to shifting Lambda_ref UP by {dLambda*1e6:.3f} keV ({(Lambda_exact/Lambda_ref-1)*1e6:.1f} ppm).

  In standard QED, the VP running of alpha includes ALL charged fermions.
  Formula B includes ONLY the electron. Yet it works to 0.027 ppm.

  This is NOT because the other fermions don't contribute — they contribute
  ENORMOUSLY (muon alone shifts 1/alpha by 0.078, quarks by 0.82).

  It works because the framework's Lambda_ref is not a physical UV cutoff.
  It's a MODULAR FORM QUANTITY: m_p/phi^3 * (1 - eta/(3*phi^3)).
  This specific value, combined with the 1/(3pi) coefficient and electron mass,
  gives 1/alpha to 0.027 ppm precision.

  The residual tells us what the NEXT correction term should be.
""")

# ============================================================================
# PART 6: Systematic search for the correction
# ============================================================================
print("=" * 80)
print("PART 6: Systematic search for correction term")
print("=" * 80)

# The correction could enter either through Lambda or through the coefficient.
# Let's parameterize it as a correction to the VP term:
# VP = (1/3pi) * ln(Lambda_ref/m_e) + delta_VP
# where delta_VP = residual = 0.0000036979

delta_VP = residual  # what we need to add

print(f"\n  We need delta_VP = {delta_VP:+.12f}")
print(f"  = {delta_VP:.6e}")
print(f"\n  Natural expressions of this size:\n")

# Build candidates as products of small framework quantities and 1/(3pi)
candidates = []

# Simple products
expressions = {
    # Pure modular form products
    "eta * theta4 / (3pi)":          eta * theta4 / (3*pi),
    "eta^2 / (9*phi^3*pi)":         eta**2 / (9*phi**3*pi),
    "theta4^2 * phi / (3pi)":       theta4**2 * phi / (3*pi),
    "theta4 * eta * phi / (9pi)":   theta4 * eta * phi / (9*pi),

    # With alpha
    "alpha / pi":                    alpha_meas / pi,
    "alpha^2 * pi":                  alpha_meas**2 * pi,
    "alpha / (3pi^2)":              alpha_meas / (3*pi**2),

    # Mixed
    "eta * theta4^2":               eta * theta4**2,
    "theta4 * (1/3pi) * alpha":    theta4 * (1/(3*pi)) * alpha_meas,
    "eta * alpha / (3pi)":         eta * alpha_meas / (3*pi),

    # With logs
    "(1/3pi) * (alpha/pi) * ln(L/me)":   (1/(3*pi)) * (alpha_meas/pi) * math.log(Lambda_ref/m_e),
    "(1/3pi) * theta4 * ln(L/me)":       (1/(3*pi)) * theta4 * math.log(Lambda_ref/m_e),
    "(1/3pi) * eta*theta4 * ln(L/me)":   (1/(3*pi)) * eta * theta4 * math.log(Lambda_ref/m_e),

    # Specific physical-looking terms
    "(1/3pi)*ln(Lambda/m_mu)*theta4^2":  (1/(3*pi))*math.log(Lambda_ref/m_mu)*theta4**2,
    "eta^2*theta4/(3pi)":                eta**2 * theta4 / (3*pi),
    "theta4^3/(3pi)":                    theta4**3 / (3*pi),

    # The "obvious" kink 1-loop: wall determinant correction
    "alpha^2 * ln(L/me) / (3pi)":       alpha_meas**2 * math.log(Lambda_ref/m_e) / (3*pi),
    "alpha * theta4":                     alpha_meas * theta4,
    "eta * theta4^2 / pi":              eta * theta4**2 / pi,

    # Dimension-like
    "1/(mu*phi)":                        1/(1836.15267343 * phi),
    "theta4/phi^3":                      theta4/phi**3,
    "eta*theta4/phi^4":                  eta*theta4/phi**4,
}

# Sort by closeness to target
results = []
for name, val in expressions.items():
    if val != 0:
        ratio = delta_VP / val
        log_ratio = abs(math.log10(abs(ratio)))
        results.append((log_ratio, ratio, name, val))

results.sort()

print(f"  {'Expression':<45} {'Value':>14} {'ratio target/expr':>18} {'log10|ratio|':>13}")
print(f"  {'-'*45} {'-'*14} {'-'*18} {'-'*13}")
for log_r, ratio, name, val in results[:25]:
    print(f"  {name:<45} {val:>14.6e} {ratio:>+18.6f} {log_r:>13.4f}")

# ============================================================================
# PART 7: The kink determinant angle
# ============================================================================
print("\n" + "=" * 80)
print("PART 7: Kink 1-loop determinant perspective")
print("=" * 80)

print(f"""
  The framework claims the 1/(3pi) coefficient comes from the kink 1-loop
  determinant (Weyl fermion on domain wall = half of Dirac).

  In standard 1-loop VP, the coefficient is 2/(3pi) per Dirac fermion.
  For a Weyl fermion: 1/(3pi). This is what Formula B uses.

  The 1-LOOP DETERMINANT of the Poeschl-Teller potential at n=2 gives
  additional corrections. For the bosonic (scalar) fluctuation determinant:

    ln det(-d^2 + V_PT) / ln det(-d^2) = known function of kink mass

  The question is whether these kink-specific corrections contribute to
  the VP coefficient at order that matches the residual.
""")

# The PT n=2 potential has eigenvalues that modify the fluctuation determinant.
# The bound state at omega^2 = 0 (zero mode) and omega^2 = 3/4 * m_kink^2
# (first excited state) both contribute.

# For the reflectionless PT potential, the 1-loop correction is:
# delta(1/alpha)_kink = (1/3pi) * [phase shift integral]
# The phase shift for PT n=2 is: delta(k) = -arctan(3k/(2-k^2)) - arctan(k) (for unit mass)
# The correction from the phase shift integral:

# Integral of delta'(k) * ln(k^2) dk from 0 to infinity
# For PT n=2: delta(k) = -arctan(3k/(2-k^2)) - arctan(3k/k^2-?) ...
# Actually for PT with V = -n(n+1) sech^2(x), the S-matrix is:
# S(k) = product_{j=1}^{n} (k - ij)/(k + ij)
# For n=2: S(k) = [(k-i)(k-2i)] / [(k+i)(k+2i)]
# Phase shift: delta(k) = -arctan(1/k) - arctan(2/k)  (total phase)

# The 1-loop energy correction from the continuum:
# E_1loop = (1/2) * integral dk/(2pi) * [d(delta)/dk] * sqrt(k^2 + m^2)
# For the VP application, we need the correction to the photon propagator
# from the kink bound states and continuum.

# The SPECTRAL ASYMMETRY of the kink gives an additional contribution:
# For n=2 PT, there are 2 bound states (E=0 and E=3m/4) and a continuum.
# The bound state contribution to VP is:
# delta_bound(1/alpha) ~ (1/3pi) * sum_j ln(Lambda/E_j)

# If the bound state at E = 3*m_kink/4 contributes:
# with m_kink ~ Lambda_ref (the wall energy scale)
E_bound = 0.75 * Lambda_ref  # 3/4 of wall mass for first excited state
delta_bound = (1/(3*pi)) * math.log(Lambda_ref / E_bound)
print(f"  PT n=2 bound state energy: E_1 = (3/4)*Lambda_ref = {E_bound*1000:.3f} MeV")
print(f"  Bound state VP: (1/3pi)*ln(Lambda_ref/E_1) = (1/3pi)*ln(4/3)")
print(f"  = {delta_bound:.12f}")
print(f"  = {delta_bound/inv_alpha_meas*1e6:.6f} ppm")
print(f"  vs needed: {delta_VP:.12f} = {delta_VP/inv_alpha_meas*1e6:.6f} ppm")
print(f"  Ratio: {delta_VP/delta_bound:.6f}")

# Actually ln(4/3) = 0.28768
# (1/3pi) * ln(4/3) = 0.106103 * 0.28768 = 0.03052
# Way too big. But what about the RENORMALIZED bound state contribution?

# The reflectionless condition means the scattering states contribute with
# a specific phase that EXACTLY cancels part of the free propagator.
# Net correction from reflectionlessness:
# For n=2 PT: 2 bound states subtract from the continuum integral.
# The spectral zeta function gives the exact 1-loop determinant:
# ln det = -sum_j ln(a_j^2) + integral terms
# where a_j are the bound state eigenvalues.

# For n=2: bound states at a_1 = 0 (zero mode) and a_2 = sqrt(3)/2
# Zero mode doesn't contribute to VP (it's the Goldstone mode).
# The a_2 = sqrt(3)/2 bound state contribution relative to continuum:
# delta_VP_kink_specific = (1/3pi) * [sum over phase shift corrections]

# Let me compute the actual ln det ratio for PT n=2:
# det(-d^2 + 6*sech^2(x)) / det(-d^2) = ?
# For reflectionless potentials: product_{j=1}^n j^2 / (j+n)!...
# Actually for unit interval: Gamma functions involved.

# The key relation: for PT at depth n, the functional determinant ratio is:
# det'(-d^2 + V) / det(-d^2) = product_{j=1}^{n} (n-j+1)! * j / (n+j)!
# This is analytically known. For n=2:
# Removing zero mode: det' / det = 1 * 2 / (3! * 4!) = 2/720... no, need proper formula.

# Actually for the ratio of determinants on the real line with PT potential:
# det(-d^2 + n(n+1)sech^2 + k^2) / det(-d^2 + k^2) = product_{j=1}^n (k^2 + j^2) / (k^2 + j^2)
# That's trivially 1! No — the scattering matrix approach gives:
# |T(k)|^2 = 1 for all k (reflectionless), so the continuum contribution is trivial.
# The only non-trivial part is the bound states.

# For the VP, the bound state contributions are:
# delta_VP_bound = -(1/3pi) * sum_j [E_j < Lambda] * Q^2 * ln(Lambda/E_j)
# where E_j are the bound state energies.

# This is getting complex. Let me just do the numerical approach:
# What single multiplicative correction to Lambda_ref matches experiment?

print(f"\n  --- Exact Lambda analysis ---")
print(f"  Lambda_ref = {Lambda_ref*1000:.9f} MeV")
print(f"  Lambda_exact = {Lambda_exact*1000:.9f} MeV")
print(f"  Ratio = {Lambda_exact/Lambda_ref:.15f}")
print(f"  = 1 + {Lambda_exact/Lambda_ref - 1:.6e}")
print(f"  = 1 + 3.49e-5")

delta_frac = Lambda_exact/Lambda_ref - 1

# This 3.5e-5 fractional shift — what IS it?
print(f"\n  What is this 3.49e-5 fractional shift?")
print(f"  alpha^2           = {alpha_meas**2:.6e}   ({delta_frac/alpha_meas**2:.4f}x)")
print(f"  alpha/pi * theta4 = {alpha_meas/pi*theta4:.6e}   ({delta_frac/(alpha_meas/pi*theta4):.4f}x)")
print(f"  theta4/phi^2      = {theta4/phi**2:.6e}   ({delta_frac/(theta4/phi**2):.4f}x)")
print(f"  eta*theta4^2      = {eta*theta4**2:.6e}   ({delta_frac/(eta*theta4**2):.4f}x)")

# ============================================================================
# PART 8: What if the answer is simpler? Refinement series
# ============================================================================
print("\n" + "=" * 80)
print("PART 8: Refinement as a series expansion")
print("=" * 80)

# Current: Lambda_ref = Lambda_raw * (1 - x) where x = eta/(3*phi^3)
# What if it's actually Lambda_ref = Lambda_raw * (1 - x + cx^2 + ...) ?
x = eta / (3 * phi**3)
print(f"\n  x = eta/(3*phi^3) = {x:.15f}")
print(f"  x^2 = {x**2:.15e}")
print(f"  x^3 = {x**3:.15e}")

# needed_extra_refinement = refinement * (ratio - 1)
extra = refinement * (Lambda_exact/Lambda_ref - 1)
print(f"\n  Extra refinement needed: {extra:.15e}")
print(f"  x^2 = {x**2:.15e}")
print(f"  Ratio extra/x^2 = {extra/x**2:.6f}")
print(f"  => coefficient c approx {extra/x**2:.6f} if correction is c*x^2")

# What about (1-x)*exp(delta) ~ (1-x)(1+delta)?
# delta = ln(Lambda_exact/Lambda_ref)
delta_ln = math.log(Lambda_exact/Lambda_ref)
print(f"\n  Alternatively: ln(Lambda_exact/Lambda_ref) = {delta_ln:.12e}")
print(f"  This is the fractional shift in the log.")
print(f"  In terms of the VP: delta_VP = (1/3pi) * delta_ln = {(1/(3*pi))*delta_ln:.12e}")
print(f"  Compare to residual: {delta_VP:.12e}")
print(f"  Match: {(1/(3*pi))*delta_ln / delta_VP:.12f}")

# ============================================================================
# PART 9: Comparison with alpha(M_Z) to check consistency
# ============================================================================
print("\n" + "=" * 80)
print("PART 9: Consistency check — comparison with known VP at low energy")
print("=" * 80)

# Standard VP running from 0 to 1 GeV gives:
# delta(1/alpha) ~ 1/alpha(0) - 1/alpha(1 GeV)
# From PDG: 1/alpha(0) = 137.036, 1/alpha(M_Z) = 127.95
# Total running: about 9.09 from 0 to 91 GeV
# From 0 to 1 GeV: mostly electron loop
# Standard electron VP from 0 to Lambda_ref (220 MeV):
# delta = (2/3pi) * ln(220/0.511) = 0.2122 * ln(430.5) = 0.2122 * 6.065 = 1.287
# But Formula B uses HALF this: 0.643

print(f"  Standard VP (2/3pi) from 0 to Lambda_ref ({Lambda_ref*1000:.1f} MeV):")
print(f"    Electron: {2/(3*pi) * math.log(Lambda_ref/m_e):.6f}")
print(f"    Muon:     {2/(3*pi) * math.log(Lambda_ref/m_mu):.6f}")
print(f"  Formula B VP (1/3pi):")
print(f"    Electron: {1/(3*pi) * math.log(Lambda_ref/m_e):.6f}")
print(f"    Muon:     {1/(3*pi) * math.log(Lambda_ref/m_mu):.6f}")
print(f"\n  Formula B electron VP = HALF of standard electron VP")
print(f"  But standard also includes muon (small) + quarks (hidden in hadronic)")
print(f"  at this low scale.")

# The key: Formula B is NOT doing standard running. It's using a modular-form-
# derived cutoff with a specific coefficient. The 0.027 ppm is the accuracy
# of this modular encoding.

# ============================================================================
# PART 10: DEFINITIVE SUMMARY
# ============================================================================
print("\n" + "=" * 80)
print("PART 10: DEFINITIVE SUMMARY")
print("=" * 80)

print(f"""
  FORMULA B: 1/alpha = theta3*phi/theta4 + (1/3pi)*ln(Lambda_ref/m_e)
  where Lambda_ref = (m_p/phi^3) * (1 - eta/(3*phi^3))

  PRECISION: {abs(residual/inv_alpha_meas)*1e6:.3f} ppm = {abs(residual/inv_alpha_meas)*1e9:.1f} ppb
  RESIDUAL:  {residual:+.9f} (Formula B is too LOW)
  IN SIGMA:  {residual/1.1e-8:.0f}sigma from experimental uncertainty

  -----------------------------------------------------------------------
  THE RESIDUAL CAN BE CLOSED BY:
  -----------------------------------------------------------------------

  OPTION A: Shift Lambda_ref up by {(Lambda_exact/Lambda_ref-1)*1e6:.1f} ppm
    Lambda_ref: {Lambda_ref*1000:.6f} MeV  -->  {Lambda_exact*1000:.6f} MeV
    Requires adding +{extra:.6e} to refinement factor
    Natural candidate: +{extra/x**2:.2f} * [eta/(3*phi^3)]^2 (= x^2 correction)
    This would make: Lambda = (m_p/phi^3)(1 - x + {extra/x**2:.2f}*x^2)
    with x = eta/(3*phi^3) = {x:.9f}

  OPTION B: Shift VP coefficient from 1/(3pi) to {C_exact:.15f}
    Fractional shift: {(C_exact/C_half - 1)*1e6:.3f} ppm
    This is {(C_exact/C_half - 1)/(alpha_meas/pi):.6f} times alpha/pi
    Far too small for a standard radiative correction

  OPTION C: Add a SECOND correction term to VP
    Need: delta_VP = {delta_VP:+.9e}
    Possible forms:
      - (1/3pi) * alpha^2 * c:  requires c ~ {delta_VP/((1/(3*pi))*alpha_meas**2):.2f}
      - theta4^2 * c:           requires c ~ {delta_VP/theta4**2:.6f}
      - alpha * theta4 * c:     requires c ~ {delta_VP/(alpha_meas*theta4):.4f}

  -----------------------------------------------------------------------
  WHAT THE GAP IS NOT:
  -----------------------------------------------------------------------

  - NOT muon VP: muon VP (0.078) is 21,000x LARGER than the gap
  - NOT quark VP: quark VP (0.82) is 220,000x LARGER than the gap
  - NOT 2-loop: 2-loop (0.0017) is 460x LARGER than the gap

  All these would DESTROY the precision, not improve it.
  Formula B is NOT "electron VP only with other fermions missing."
  It is a SELF-CONTAINED formula where Lambda_ref encodes the full running.

  -----------------------------------------------------------------------
  MOST LIKELY INTERPRETATION:
  -----------------------------------------------------------------------

  Lambda_ref = (m_p/phi^3)(1 - eta/(3*phi^3)) is an approximation to
  a more precise modular form expression. The 0.027 ppm residual
  represents the NEXT TERM in this expansion.

  The leading correction x = eta/(3*phi^3) = {x:.9f} captures 99.9973%
  of the full result. The residual {extra:.3e} ~ {extra/x**2:.1f}*x^2
  suggests a quadratic correction in the expansion parameter.

  If Lambda_exact has the form:
    Lambda = (m_p/phi^3) * f(eta, theta4, phi)
  then f = 1 - x + {extra/x**2:.2f}*x^2 + ... where x = eta/(3*phi^3)

  The coefficient {extra/x**2:.2f} of x^2 should be derivable from the kink
  1-loop determinant or the modular form expansion at q = 1/phi.
""")

# Quick check: is 0.40 a recognizable number?
c2 = extra/x**2
print(f"  Coefficient of x^2 term: c2 = {c2:.8f}")
print(f"  Close to: 1/phi^4 = {1/phi**4:.8f}  (ratio: {c2/(1/phi**4):.4f})")
print(f"  Close to: 1/3     = {1/3:.8f}  (ratio: {c2/(1/3):.4f})")
print(f"  Close to: phi-1   = {phi-1:.8f}  (ratio: {c2/(phi-1):.4f})")
print(f"  Close to: 1/phi^2 = {1/phi**2:.8f}  (ratio: {c2/(1/phi**2):.4f})")
print(f"  Close to: 1/(2phi)= {1/(2*phi):.8f}  (ratio: {c2/(1/(2*phi)):.4f})")
print(f"  Close to: 2/5     = {0.4:.8f}  (ratio: {c2/0.4:.4f})")
print(f"  Close to: phi/4   = {phi/4:.8f}  (ratio: {c2/(phi/4):.4f})")
print(f"  Close to: 3/8     = {0.375:.8f}  (ratio: {c2/0.375:.4f})")
print(f"  Close to: ln(phi)/2 = {math.log(phi)/2:.8f}  (ratio: {c2/(math.log(phi)/2):.4f})")
print(f"  Close to: theta4  = {theta4:.8f}  (ratio: {c2/theta4:.4f})")
print(f"  Close to: eta/3   = {eta/3:.8f}  (ratio: {c2/(eta/3):.4f})")
print(f"  Close to: 1/e     = {1/math.e:.8f}  (ratio: {c2/(1/math.e):.4f})")

# Also check: what if the expansion parameter is something else?
print(f"\n  Alternative expansion parameters:")
y = eta * theta4
print(f"  y = eta*theta4 = {y:.12f}")
print(f"  extra/y = {extra/y:.6e}  (not clean)")
y2 = theta4 * phi
print(f"  y = theta4*phi = {y2:.12f}")
print(f"  extra/y^2 = {extra/y2**2:.6e}  (not clean)")

# What about eta^2?
print(f"\n  If expansion parameter is eta (not x = eta/(3*phi^3)):")
print(f"  extra/eta^2 = {extra/eta**2:.8f}")
print(f"  Close to 1/(3*phi^3) = {1/(3*phi**3):.8f}  (ratio: {(extra/eta**2)/(1/(3*phi**3)):.4f})")
# That would mean the correction is eta^2/(3*phi^3), and the full formula is:
# Lambda = (m_p/phi^3)(1 - eta/(3*phi^3) + eta^2/(3*phi^3)^2 * c ...)
# Actually extra/eta^2 = extra/(0.01182)^2 = extra/0.01402 = 2.46e-3
# and 1/(3*phi^3) = 0.0787
# ratio = 0.0313 — not clean

# Final check: alpha_s correction?  eta IS alpha_s at this nome.
# So the refinement series in powers of eta = alpha_s:
# Lambda = (m_p/phi^3)(1 - eta/(3*phi^3) + c2*eta^2/(3*phi^3)^2 + ...)
# This looks like a perturbative expansion in the strong coupling!
print(f"\n  As perturbative expansion in eta = alpha_s = {eta:.6f}:")
print(f"  Term 0: 1")
print(f"  Term 1: -eta/(3*phi^3) = -{x:.9f}")
print(f"  Term 2: +c2*[eta/(3*phi^3)]^2 = +{extra:.6e}  (c2 = {c2:.4f})")
print(f"\n  If c2 = 1/2 + O(eta): Lambda = (m_p/phi^3)(1 - x + x^2/2 + ...)")
print(f"    This would be (m_p/phi^3)*exp(-x) to second order!")
print(f"    exp(-x) = {math.exp(-x):.15f}")
print(f"    1-x+x^2/2 = {1 - x + x**2/2:.15f}")
print(f"    1-x       = {1-x:.15f}")

Lambda_exp = Lambda_raw * math.exp(-x)
inv_alpha_exp = inv_alpha_tree + (1/(3*pi)) * math.log(Lambda_exp / m_e)
resid_exp = inv_alpha_meas - inv_alpha_exp
print(f"\n  Lambda_exp = (m_p/phi^3)*exp(-eta/(3*phi^3)) = {Lambda_exp*1000:.9f} MeV")
print(f"  1/alpha_exp = {inv_alpha_exp:.12f}")
print(f"  Residual = {resid_exp:+.12f} ({resid_exp/inv_alpha_meas*1e6:+.6f} ppm)")
print(f"  vs linear: {residual:+.12f} ({residual/inv_alpha_meas*1e6:+.6f} ppm)")
print(f"  Improvement: {abs(residual) - abs(resid_exp):.6e} in 1/alpha")
print(f"  Factor: {abs(residual)/abs(resid_exp):.4f}x closer")

# What about 1/(1+x) = 1-x+x^2-x^3+... ?
Lambda_inv = Lambda_raw / (1 + x)
inv_alpha_inv = inv_alpha_tree + (1/(3*pi)) * math.log(Lambda_inv / m_e)
resid_inv = inv_alpha_meas - inv_alpha_inv
print(f"\n  Lambda_inv = (m_p/phi^3)/(1 + eta/(3*phi^3)) = {Lambda_inv*1000:.9f} MeV")
print(f"  1/alpha_inv = {inv_alpha_inv:.12f}")
print(f"  Residual = {resid_inv:+.12f} ({resid_inv/inv_alpha_meas*1e6:+.6f} ppm)")
print(f"  This is {'WORSE' if abs(resid_inv) > abs(residual) else 'BETTER'}")

# What about (1-x)^(1+delta) for small delta?
# (1-x)^(1+d) ~ (1-x) * (1-x)^d ~ (1-x)(1 + d*ln(1-x))
# We need the extra contribution d*ln(1-x)*(1-x) to equal 'extra'
# d = extra / [(1-x)*ln(1-x)] = extra / [refinement * ln(refinement)]
d_exp = extra / (refinement * math.log(refinement))
print(f"\n  If Lambda = (m_p/phi^3) * (1-x)^(1+d):")
print(f"  d = {d_exp:.8f}")
print(f"  Close to: -eta*phi = {-eta*phi:.8f} (ratio: {d_exp/(-eta*phi):.4f})")
print(f"  Close to: -theta4  = {-theta4:.8f} (ratio: {d_exp/(-theta4):.4f})")

print("\n" + "=" * 80)
print("DONE")
print("=" * 80)
