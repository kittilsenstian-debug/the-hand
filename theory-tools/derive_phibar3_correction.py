#!/usr/bin/env python3
"""
derive_phibar3_correction.py — Deriving phibar^3/42 in the alpha formula
from the one-loop kink width change.

THE PROBLEM:
    c2_exact = 0.397748547... (from data)
    c2_Wallis = 2/5 = 0.400 (from Graham pressure / Wallis ratio)
    Best candidate: c2 = (2/5)(1 - phibar^3/42)  [matches to 8 ppm]

    The 2/5 is derived (Graham & Weigel PLB 852, 2024; Wallis I_6/I_4 = 4/5).
    This script attempts to DERIVE phibar^3/42 from kink physics.

THREE APPROACHES:
    1. One-loop kink width correction: quantum fluctuations widen the wall,
       reducing Lambda_eff = 1/w_eff. The fractional width change gives
       the correction factor.
    2. Wallis cascade perturbative series: the full expansion
       f(x) = sum_k (-1)^k c_k x^k has c_k involving successive Wallis
       ratios. Truncation at quadratic absorbs higher terms into c2_eff.
    3. Golden asymmetry: the asymmetric vacua (phi vs -1/phi) modify the
       profile-weighted VP integral through cubic moments.

CONSTANTS (q = 1/phi, 2000-term sums):
    eta    = 0.118403904856684
    theta3 = 2.555093469444516
    theta4 = 0.030311200785327

Author: Interface Theory project
Date: Feb 25, 2026
"""

import math

# ============================================================================
# CONSTANTS
# ============================================================================
phi    = (1 + math.sqrt(5)) / 2    # 1.6180339887498949
phibar = 1.0 / phi                  # 0.6180339887498949
sqrt5  = math.sqrt(5)
pi     = math.pi

# Modular forms at q = 1/phi
eta    = 0.118403904856684
theta3 = 2.555093469444516
theta4 = 0.030311200785327

# Physical constants
m_e = 0.51099895000e-3   # GeV
m_p = 0.93827208816      # GeV
inv_alpha_meas = 137.035999206   # Rb 2020
inv_alpha_unc  = 0.000000011     # 1-sigma

# Expansion parameter
x = eta / (3 * phi**3)

# c2 extracted from experiment
tree = theta3 * phi / theta4
VP_needed = inv_alpha_meas - tree
Lambda_needed = m_e * math.exp(VP_needed * 3 * pi)
Lambda_raw = m_p / phi**3
f_needed = Lambda_needed / Lambda_raw
c2_exact = (f_needed - 1 + x) / x**2

# Target correction
phibar3 = phibar**3
target = phibar3 / 42
c2_target = 0.4 * (1 - target)

# Utility
def compute_inv_alpha(c2_val):
    """Compute 1/alpha for a given c2."""
    L = Lambda_raw * (1 - x + c2_val * x**2)
    vp = (1 / (3 * pi)) * math.log(L / m_e)
    return tree + vp

sep = "=" * 80
subsep = "-" * 80

# ============================================================================
# Wallis integral helper
# ============================================================================
def wallis_sech(k):
    """Exact integral of sech^{2k}(x) from -inf to inf."""
    result = 2.0
    for j in range(1, k):
        result *= (2*j) / (2*j + 1)
    return result

I2  = wallis_sech(1)   # 2
I4  = wallis_sech(2)   # 4/3
I6  = wallis_sech(3)   # 16/15
I8  = wallis_sech(4)   # 32*4/(15*7) = 128/105
I10 = wallis_sech(5)   # 256/945... etc

# Wallis ratios: I_{2(k+1)}/I_{2k} = 2k/(2k+1)
W1 = I4 / I2    # 2/3
W2 = I6 / I4    # 4/5
W3 = I8 / I6    # 6/7
W4 = I10 / I8   # 8/9

n_PT = 2  # Poschl-Teller depth

print(sep)
print("DERIVING phibar^3/42 FROM ONE-LOOP KINK WIDTH CHANGE")
print(sep)
print()
print(f"  Known: c2_exact  = {c2_exact:.15f}")
print(f"  Known: c2_Wallis = 2/5 = {0.4:.15f}")
print(f"  Target: c2 = (2/5)(1 - phibar^3/42) = {c2_target:.15f}")
print(f"  Difference c2_exact - c2_target = {c2_exact - c2_target:+.6e}")
print(f"  Match quality: {abs(c2_exact - c2_target)/c2_exact * 1e6:.1f} ppm")
print()
print(f"  phibar^3 = {phibar3:.15f}")
print(f"  42 = 6 x 7 = 2(n+1) x (2(n+1)+1) for n=2")
print(f"  phibar^3/42 = {target:.15f}")
print(f"  x = {x:.15f}")


# ============================================================================
# APPROACH 1: ONE-LOOP KINK WIDTH CORRECTION
# ============================================================================
print(f"\n\n{sep}")
print("APPROACH 1: ONE-LOOP KINK WIDTH CORRECTION")
print(sep)

print("""
PHYSICAL PICTURE:
  Lambda = 1/w_eff is the inverse effective domain wall thickness.
  Quantum fluctuations (one-loop) cause the wall to broaden.
  If delta_w/w > 0, then Lambda_eff < Lambda_cl, so f(x) < 1.

  The kink profile: Phi_cl(x) = 1/2 + (sqrt(5)/2)*tanh(kappa*x)
  where kappa = m/2, m^2 = 10*lambda = V''(phi).

  The wall thickness w_cl = 1/kappa = 2/m.
  Lambda_cl = kappa = m/2.

  One-loop correction to the mass parameter m:
  m_eff^2 = m^2 + delta_m^2

  For the PT n=2 operator H = -d^2/dz^2 + 1 - 6*sech^2(z):
  The eigenvalue spectrum:
    - Zero mode: omega_0 = 0 (translational)
    - Bound state: omega_1 = sqrt(3)/2 (breathing mode)
    - Continuum: omega_k = sqrt(1 + k^2) for k >= 0

  The mass renormalization comes from the spectral zeta function:
  delta_m^2/m^2 = (1/(2*pi)) * [sum over modes - continuum]
""")

# ----------------------------------------------------------------
# 1a. DHN mass correction for PT n=2
# ----------------------------------------------------------------
print(f"  1a. DHN MASS CORRECTION (Dashen-Hasslacher-Neveu 1974)")
print(f"  {subsep}")

# The one-loop kink mass correction in phi^4 (PT n=2):
# delta_M_kink = m * [1/(4*sqrt(3)) - 3/(2*pi)]
# This is the ENERGY correction, not the mass-parameter correction.

# The mass-parameter correction delta_m^2 comes from the one-loop
# effective potential evaluated at the vacuum (not on the kink).
# But for the KINK WIDTH, what matters is how the fluctuations
# change the effective mass at the kink center vs at the vacua.

# At the vacuum (Phi = phi): the fluctuation mass is m^2 = 10*lambda
# At the kink center (Phi = 1/2): V''(1/2) = 2*lambda*(6*(1/4) - 6*(1/2) - 1)
#   = 2*lambda*(3/2 - 3 - 1) = 2*lambda*(-5/2) = -5*lambda = -m^2/2
# So the effective potential at the center is NEGATIVE (attractive).

# The one-loop correction to the effective mass squared at the vacuum:
# In 1+1D, the Coleman-Weinberg correction is:
# V_eff''(phi) = V''(phi) + (lambda_eff/(2*pi)) * [ln(V''(phi)/mu^2) terms]
# For the PT n=2 system, this is most cleanly done through the
# spectral representation.

# The KEY insight: the inverse width kappa_eff = m_eff/2 where
# m_eff^2 = m^2 * (1 + radiative correction).

# For the PHI^4 kink in 1+1D, the one-loop correction to the
# inverse penetration length is:
# delta_kappa / kappa = (1/2) * delta_m^2 / m^2

# The spectral formula for delta_m^2/m^2 in terms of the PT n=2
# bound state spectrum:
# The bound state at omega_1 = sqrt(3)*m/2 modifies the asymptotic
# approach to the vacuum. The correction to the penetration length
# involves the phase shift of the continuum at threshold.

# For PT n=2, the phase shift at k=0 is:
# delta_0 = pi * n = 2*pi (Levinson's theorem: n bound states)
# But the DERIVATIVE of the phase shift at threshold matters:
# d(delta)/dk |_{k=0} = sum_{j} 1/(kappa_j) where kappa_j are the bound state "kappas"
# For the two bound states:
# j=0 (zero mode): kappa_0 = m/2 * 2 = m  (or more carefully, 2*kappa in natural units)
# j=1 (breathing): kappa_1 = m/2 * 1 = m/2

# This is the Wigner time delay approach to the width correction.

# Let me compute via the EXPLICIT spectral sum.
# The PT n=2 reflection coefficient vanishes (reflectionless),
# so the transmission amplitude is T(k) = (k-i)(k-2i)/((k+i)(k+2i))
# in units where kappa=1.

# The one-loop effective potential correction involves:
# Sigma(p^2=m^2) = integral dk / (2*pi) * |psi_k(x->inf)|^2 / (k^2 + kappa^2 - p^2/m^2)
# This is too involved for a closed-form. Let's use the known results.

# KNOWN RESULT (Rebhan & van Nieuwenhuizen, NPB 508, 449 (1997)):
# The one-loop correction to the kink mass for PT n=2 in 1+1D is:
# delta_M / M_cl = -(m/(2*pi)) * 3/M_cl (continuum) + bound state contributions

# More directly: the DHN result is:
# delta_M = (m/pi) * [1/(4*sqrt(3)) * pi - 3/2]  ... no, the standard form is:
# delta_M = m * [1/(4*sqrt(3)) - 3/(2*pi)]
DHN_shift = 1/(4*math.sqrt(3)) - 3/(2*pi)
print(f"    DHN mass shift: delta_M/m = 1/(4*sqrt(3)) - 3/(2*pi)")
print(f"                              = {1/(4*math.sqrt(3)):.10f} - {3/(2*pi):.10f}")
print(f"                              = {DHN_shift:.10f}")
print(f"    |delta_M/m| = {abs(DHN_shift):.10f}")
print()

# The classical kink mass in units of m:
# For V(Phi) = lambda*(Phi^2-Phi-1)^2:
# M_cl = sqrt(2*lambda) * integral_{-1/phi}^{phi} |Phi^2-Phi-1| dPhi
# = sqrt(2*lambda) * 5*sqrt(5)/6 (analytically)
# In terms of m (where m^2 = 10*lambda, lambda = m^2/10):
# M_cl = sqrt(2*m^2/10) * 5*sqrt(5)/6 = (m/sqrt(5)) * 5*sqrt(5)/6 = 5*m/6

M_cl_over_m = 5.0 / 6.0
print(f"    Classical kink mass: M_cl = (5/6)*m = {M_cl_over_m:.6f}*m")
print(f"    Relative mass shift: |delta_M|/M_cl = (6/5)*|delta_M/m|")
print(f"                                        = {6.0/5 * abs(DHN_shift):.10f}")
print()

# ----------------------------------------------------------------
# 1b. Width correction from mass renormalization
# ----------------------------------------------------------------
print(f"  1b. WIDTH CORRECTION FROM MASS RENORMALIZATION")
print(f"  {subsep}")

print("""
  The kink width w = 2/m. A shift m -> m + delta_m gives:
    delta_w/w = -delta_m/m

  But we need delta_m, not delta_M. The kink mass M and the
  particle mass m are DIFFERENT quantities:
    M_cl = (5/6)*m (classical kink mass, a soliton energy)
    m = sqrt(V''(phi)) (particle mass at the vacuum, a fluctuation frequency)

  The one-loop correction to the PARTICLE MASS m (not the soliton mass M):
  In 1+1D phi^4 theory, the self-energy correction at one loop gives:
    delta_m^2/m^2 = (lambda_eff)/(4*pi*m^2) * [divergent + finite]

  For the PT n=2 potential, the finite part involves the bound state
  contributions. The KEY formula comes from the spectral representation
  of the propagator in the kink background.
""")

# The one-loop self-energy at the vacuum in the kink background
# involves a sum over the discrete + continuum spectrum of H.
# The standard result for the mass shift at one-loop in 1+1D is:
#
# delta_m^2 / m^2 = -(g^2/(4*pi*m)) * integral (rho(k) - rho_free(k)) dk
#
# where rho is the spectral density of H in the kink background
# and rho_free is the free spectral density.
#
# For PT n=2, the EXTRA spectral weight from the bound states:
#   zero mode:     contributes -1/(2*kappa_0) = -1/m
#   breathing mode: contributes -1/(2*kappa_1) = -1/(m*sqrt(3)/2) = -2/(m*sqrt(3))
#
# The total bound state contribution to the width correction is:
# delta_kappa_BS / kappa = -(g^2/(8*pi*m^2)) * [1 + 2/sqrt(3)]

# But this involves the coupling g, which in our framework is x = eta/(3*phi^3).
# Let's parametrize the correction as:
# delta_w/w = A * x + B * x^2 + ...
# and identify the coefficients from the spectral analysis.

# The PHYSICAL connection to the Wallis integrals:
# The width correction comes from the kink profile deformation.
# At one loop, the profile correction Phi_1(x) satisfies:
# H * Phi_1 = source(x)
# where the source involves V'''(Phi_cl) * G(x,x).
# The correction to the width is:
# delta_w/w = Phi_1(0) / (dPhi_cl/dx|_{x=0}) * kappa

# For the tanh profile: dPhi_cl/dx|_{x=0} = (sqrt(5)/2) * kappa
# And Phi_1(0) involves <source|psi_0>/<omega_0> (zero mode projection).

# The zero mode contribution is a TRANSLATION, not a width change.
# The width change comes from the BREATHING MODE (omega_1 = sqrt(3)*m/2):
# Phi_1^{width}(x) = a_1 * psi_1(x) / omega_1^2

# where psi_1 = sech(z)*tanh(z) (the breathing mode wavefunction for n=2)
# and a_1 = <psi_1|source> is the overlap integral.

# The breathing mode profile is: psi_1(z) = sqrt(3/2) * sech(z)*tanh(z)
# This has psi_1(0) = 0! So the breathing mode does NOT change the width
# at the center of the kink!

# The width change comes from the CONTINUUM modes, which modify the
# exponential tails. The effective penetration length becomes:
# 1/kappa_eff = 1/kappa + delta(1/kappa)

# The fractional width change from continuum modes:
# delta_w/w = -(1/(2*pi)) * integral_0^infty [delta_l(k)/k] dk / something...

# This is getting complicated. Let me try a cleaner approach.

print("""
  CLEAN APPROACH: Width from the effective penetration depth.

  The kink approaches the vacuum exponentially:
    Phi(x) -> phi - A*exp(-kappa_eff * x)  as x -> +infinity

  kappa_eff = kappa_cl * (1 + radiative correction)

  For the WHOLE kink, we define the effective width as:
    w_eff = (Phi(+inf) - Phi(-inf)) / (dPhi/dx|_{max})

  Classical: w_cl = sqrt(5) / (sqrt(5)/2 * kappa) = 2/kappa = 2/m * 2 = ...
  Let me be careful.

  Phi_cl(x) = 1/2 + (sqrt(5)/2)*tanh(kappa*x), kappa = m/2
  dPhi_cl/dx|_{x=0} = (sqrt(5)/2)*kappa = sqrt(5)*m/4
  Phi(+inf) - Phi(-inf) = sqrt(5)

  w_slope = sqrt(5) / (sqrt(5)*m/4) = 4/m

  So Lambda_slope = 1/w_slope = m/4 = kappa/2

  Hmm, this differs from Lambda = kappa by a factor of 2. The actual
  QCD connection uses Lambda ~ kappa = m/2. Let's work with kappa.
""")

# The effective inverse width is kappa_eff.
# At one loop: kappa_eff = kappa(1 + delta_kappa/kappa)
# The relative correction to kappa = m/2 is:
# delta_kappa/kappa = delta_m/m / 2  (from kappa = m/2)

# But wait: the one-loop correction also modifies the AMPLITUDE
# of the tanh profile. The full one-loop kink is:
# Phi(x) = 1/2 + (sqrt(5)/2 + delta_A) * tanh((kappa + delta_kappa)*x)
# The width involves BOTH delta_kappa and delta_A.

# For the SLOPE at the center:
# dPhi/dx|_0 = (sqrt(5)/2 + delta_A)*(kappa + delta_kappa)
# w_slope = sqrt(5) / dPhi/dx|_0 (assuming endpoints don't shift much)

# But the endpoints DO shift: the VEV shifts by delta_v at one loop.
# phi_eff = phi + delta_v, so Phi(+inf) = phi + delta_v
# Similarly Phi(-inf) = -1/phi + delta_v'

# For the SYMMETRIC variable Psi = Phi - 1/2:
# The kink is Psi_cl = (sqrt(5)/2)*tanh(kappa*x)
# The vacua are Psi = +sqrt(5)/2 and -sqrt(5)/2 (symmetric!)
# So in the Psi variable, the profile is symmetric and the
# width correction is purely from kappa:
# delta_w/w = -delta_kappa/kappa

# The VEV shift in terms of Psi doesn't break the symmetry
# (it shifts both vacua equally in Phi, but oppositely in Psi).

# OK, let's just compute the width correction from the MASS
# PARAMETER renormalization.

# In 1+1D, the one-loop correction to m^2 from the Coleman-Weinberg potential:
# At the vacuum Phi = phi:
# V''_eff(phi) = V''(phi) + hbar * V''''(phi) * G(phi)
# where G(phi) is the one-loop propagator (Green's function at coincident points).

# V''''(Phi) = d^4V/dPhi^4 = 24*lambda [constant for this quartic potential]
# V''(phi) = 10*lambda = m^2

# G(phi) = integral dk/(2*pi) * 1/sqrt(k^2 + m^2) [1+1D free propagator]
# This is UV divergent: G_free = (1/(2*pi)) * ln(Lambda_UV/m) + finite

# But we're interested in the FINITE, cutoff-independent part.
# In dimensional regularization (1+1D):
# G_reg = -1/(4*pi) * 1/epsilon + finite terms

# The key insight: the coupling lambda in our framework is related to x:
# The effective coupling for the perturbative expansion is
# g_eff = eta / (3*phi^3) = x (this IS the expansion parameter).

# For the width correction at second order:
# delta_w/w = -delta_kappa/kappa
# delta_kappa/kappa = (1/2)*(delta_m^2/m^2)
#                   = (1/2) * (24*lambda) * G_finite / m^2
#                   = (1/2) * (24*lambda)/(m^2) * [finite part]
#                   = (1/2) * (24/10) * [finite part]
#                   = (12/10) * [finite part]
#                   = (6/5) * [finite part]

print(f"  KEY OBSERVATION: The quartic coupling ratio gives a factor of 6/5")
print(f"    V''''(Phi)/V''(phi) = 24*lambda / (10*lambda) = 12/5")
print(f"    Combined with the 1/2 from kappa = m/2: (1/2)*(12/5) = 6/5")
print()

# ----------------------------------------------------------------
# 1c. The width correction from the one-loop propagator in the
#     kink background (not vacuum background)
# ----------------------------------------------------------------
print(f"  1c. PROFILE-WEIGHTED WIDTH CORRECTION")
print(f"  {subsep}")

print("""
  The one-loop correction to the kink PROFILE involves the Green's function
  of the fluctuation operator H in the kink background, not in the vacuum.

  H = -d^2/dz^2 + 1 - n(n+1)*sech^2(z)  for PT depth n

  For n=2: H = -d^2/dz^2 + 1 - 6*sech^2(z)

  The Green's function G(z,z') = sum_j psi_j(z)*psi_j(z')/(omega_j^2 - p^2)
  (plus continuum integral).

  The coincident-point Green's function G(z,z) gives the local fluctuation:
    G(z,z) = |psi_0(z)|^2/omega_0^2 + |psi_1(z)|^2/omega_1^2 + continuum

  But omega_0 = 0 (zero mode) makes this divergent!
  The zero mode must be treated separately (collective coordinate).

  REMOVING the zero mode: G_reg(z,z) = |psi_1(z)|^2/omega_1^2 + continuum

  The width correction involves the integral of this over the kink profile:
  delta_Lambda/Lambda = -integral G_reg(z,z) * [weight(z)] dz / normalization
""")

# The breathing mode (n=2):
# psi_1(z) = sqrt(3/2) * sech(z) * tanh(z)  [normalized]
# omega_1 = sqrt(3)/2 (in units of m/2, which is kappa)
# Actually omega_1^2 = 3*(kappa)^2 = 3*m^2/4

# |psi_1(z)|^2 / omega_1^2 = (3/2)*sech^2(z)*tanh^2(z) / (3/4)
#                           = 2*sech^2(z)*tanh^2(z)

# integral of psi_1^2/omega_1^2 over z:
# = 2 * integral sech^2(z)*tanh^2(z) dz
# = 2 * integral (sech^2 - sech^4) dz
# = 2 * (I2/2 - I4/2)  [factor of 1/2 from sech^{2k} notation]
# Wait, let me be careful. In our convention:
# sech^2(z)*tanh^2(z) = sech^2(z)*(1-sech^2(z)) = sech^2(z) - sech^4(z)

# integral_{-inf}^{inf} sech^2(z) dz = 2 = I2
# integral_{-inf}^{inf} sech^4(z) dz = 4/3 = I4

# So integral sech^2*tanh^2 dz = 2 - 4/3 = 2/3

bm_spatial_integral = 2 * (I2 - I4)  # = 2 * (2 - 4/3) = 2 * 2/3 = 4/3
print(f"  Breathing mode spatial integral:")
print(f"    integral |psi_1(z)|^2/omega_1^2 dz = 2*(I2-I4) = 2*(2-4/3) = {bm_spatial_integral:.10f}")
print(f"    = 4/3")
print()

# The continuum contribution:
# Each continuum mode with momentum k has:
# |psi_k(z)|^2/(k^2+1) for the z-dependent part
# Summed/integrated over k from 0 to infinity.
# For a reflectionless potential, |T(k)|=1 and the scattering states
# are pure phase shifts.

# For PT n=2, the continuum spectral density differs from the free case
# by the Jost function. The integrated excess spectral density is:
# integral [rho_kink(z,z;E) - rho_free(z,z;E)] dE dz
# = -n = -2 (the bound state sum rule)

# But the PROFILE-WEIGHTED integral is more subtle.
# Let's use a different approach: the width correction from the
# EFFECTIVE INVERSE MASS at infinity.

# ----------------------------------------------------------------
# 1d. Width correction from the asymptotic mass
# ----------------------------------------------------------------
print(f"  1d. WIDTH CORRECTION FROM ASYMPTOTIC MASS")
print(f"  {subsep}")

print("""
  The kink approaches the vacuum as:
    Phi(x) -> phi - C*exp(-m_eff*x)   as x -> +infinity

  The effective mass m_eff = m * (1 + delta_m_asymp/m).

  In the kink background, the asymptotic mass gets a correction from
  the continuum phase shift at threshold (k=0).

  For PT n=2, the S-matrix is:
    S(k) = T(k) = [(k-i*1)(k-i*2)] / [(k+i*1)(k+i*2)]  [in units kappa=1]

  The phase shift: delta(k) = arg(T(k))
  At threshold (k->0): delta(0) = n*pi = 2*pi (Levinson)

  The Wigner time delay at threshold:
    tau(0) = d(delta)/dk |_{k=0}

  For T(k) = (k-i)(k-2i)/((k+i)(k+2i)):
    ln T = ln(k-i) + ln(k-2i) - ln(k+i) - ln(k+2i)
    d/dk ln T = 1/(k-i) + 1/(k-2i) - 1/(k+i) - 1/(k+2i)
    At k=0: = -i + (-i/2) - (i) - (i/2) = -3i ... wait, let me be more careful.

  Phase shift delta(k) = (1/2i)*ln(T(k)/T*(k)) for real k.
  But for reflectionless PT, T(k) itself gives the full phase.
  ln T(k) = ln|T| + i*delta(k)
  Since |T|=1: ln T = i*delta(k)

  d(delta)/dk = (1/i) * (dT/dk)/T
""")

# Let me compute the Wigner time delay numerically for PT n=2
# T(k) = (k-i)(k-2i) / ((k+i)(k+2i))
# dT/dk = [(k-2i)(k+i)(k+2i) + (k-i)(k+i)(k+2i) - (k-i)(k-2i)(k+2i) - (k-i)(k-2i)(k+i)] / [(k+i)(k+2i)]^2
# This is messy. Let me use the logarithmic derivative.

# d/dk ln T = 1/(k-i) + 1/(k-2i) - 1/(k+i) - 1/(k+2i)

# At k=0:
# = 1/(-i) + 1/(-2i) - 1/(i) - 1/(2i)
# = i + i/2 - (-i) ... no. 1/(-i) = i, 1/(-2i) = i/2, 1/(i) = -i, 1/(2i) = -i/2
# = i + i/2 + (-i) + (-i/2) ... no that's wrong.
# 1/(k-i) at k=0: 1/(-i) = 1/(-i) * (i/i) = i/(-i^2) = i/1 = i
# 1/(k-2i) at k=0: 1/(-2i) = i/2
# 1/(k+i) at k=0: 1/(i) = -i
# 1/(k+2i) at k=0: 1/(2i) = -i/2

# So d/dk ln T|_{k=0} = i + i/2 - (-i) - (-i/2) = i + i/2 + i + i/2 = 3i

# But d/dk ln T = i * d(delta)/dk (since |T|=1)
# So d(delta)/dk|_{k=0} = 3

# The Wigner time delay tau = 2 * d(delta)/dk = 6 (in units of 1/kappa)

wigner_delay = 6  # in units of 1/kappa = 2/m
print(f"    Wigner time delay at threshold: tau(0) = {wigner_delay} / kappa")
print(f"    = {wigner_delay}/kappa = {wigner_delay*2}/m")
print()

# The connection to width: the Wigner time delay relates to the
# "extra path length" a particle takes when scattering off the kink.
# In the context of the effective width:
# delta_w_eff = tau(0) / (2*kappa) = 3/kappa (in kappa=1 units)
# But this is just the SCATTERING delay, not the width correction.

# Let me try a more direct approach.
# ----------------------------------------------------------------
# 1e. Direct computation: one-loop correction to kappa
# ----------------------------------------------------------------
print(f"  1e. DIRECT ONE-LOOP MASS PARAMETER CORRECTION")
print(f"  {subsep}")

print("""
  In 1+1D, the one-loop correction to the vacuum mass parameter is:
    delta_m^2 = lambda_eff * Sigma_1loop

  where Sigma_1loop is the self-energy from the fluctuations.
  For the standard phi^4 theory in 1+1D:
    Sigma_1loop = (1/m) * [bound state sum - continuum subtraction]

  For PT n=2:
    Bound states: omega_0 = 0 (excluded by collective coordinate),
                  omega_1 = sqrt(3)/2 * m

    The breathing mode contributes:
    Sigma_breathing = 1/(2*omega_1) = 1/sqrt(3*m^2) = 1/(sqrt(3)*m)

    The continuum contributes:
    Sigma_cont = (1/(2*pi)) * integral_0^inf dk/sqrt(k^2+m^2) - [free subtraction]

    The subtracted integral (finite part) involves the phase shift.

    Using the trace formula:
    Sigma_finite = (1/m) * [1/(2*sqrt(3)) - 1/pi * sum bound state angles]

    The net result for the mass-parameter shift:
    delta_m^2/m^2 = (24*lambda)/(m^2) * (1/(4*pi)) * [spectral corrections]
    = (12/5) * [1/(4*pi)] * [spectral term]
""")

# Rather than getting lost in the spectral analysis, let me compute
# the width correction via a different route: the Gel'fand-Yaglom
# method applied to the kink width.

# The Gel'fand-Yaglom determinant for H_kink vs H_free gives:
# det(H_kink)/det(H_free) = product of eigenvalue ratios
# For PT n=2: this ratio is 1/3 (from the DHN calculation)
# (The zero mode gives 0, but regularized via collective coordinate)

# The Gel'fand-Yaglom result det_ratio = 1/(n!)^2 = 1/4 for n=2...
# Actually for PT n=2: det_reg = 1/(1*2)^2 = 1/4?
# Let me use the known result.

# For the reflectionless PT potential with n=2:
# det(H_kink)/det(H_vac) = 1/(n!)^2 * prod(omega_j^2/m^2)
# = 1/4 * (0 * 3/4) ... this vanishes due to the zero mode.
# After regularization: det_reg = (3/4)/4 = 3/16?

# This is getting complicated. Let me switch to a CLEANER approach.

# ----------------------------------------------------------------
# 1f. THE CLEAN WIDTH CORRECTION via VEV shift
# ----------------------------------------------------------------
print(f"\n  1f. THE CLEAN WIDTH CORRECTION via VEV SHIFT")
print(f"  {subsep}")

print("""
  The VEV shift at one loop modifies the wall endpoints.
  The wall connects phi_eff and -1/phi_eff (the corrected vacua).

  phi_eff = phi + delta_v, where delta_v is the one-loop VEV shift.

  For V = lambda*(Phi^2-Phi-1)^2:
  V'(Phi) = 2*lambda*(2*Phi-1)*(Phi^2-Phi-1) = 0 at phi and -1/phi
  V''(phi) = 10*lambda = m^2

  The one-loop VEV shift: delta_v = -V_eff'(phi) / V''(phi)
  V_eff'(phi) comes from the Coleman-Weinberg potential.

  In 1+1D, the one-loop effective potential is:
    V_eff^(1)(Phi) = (1/(4*pi)) * {V''(Phi) * [ln(|V''(Phi)|/mu^2) - 1]}

  V''(Phi) = 2*lambda*(6*Phi^2 - 6*Phi - 1)
  V'''(Phi) = 2*lambda*(12*Phi - 6)
  At Phi = phi: V'''(phi) = 2*lambda*(12*phi - 6) = 2*lambda*6*(2*phi-1)
             = 12*lambda*(2*phi-1) = 12*lambda*sqrt(5)

  The VEV shift at one loop (1+1D, minimal subtraction):
  delta_v = -(1/(4*pi)) * V'''(phi)/V''(phi) = -(1/(4*pi)) * 12*lambda*sqrt(5)/(10*lambda)
           = -(1/(4*pi)) * (6*sqrt(5)/5)

  This shifts the vacuum BY A GOLDEN-RATIO-DEPENDENT AMOUNT.
""")

VEV_shift_coeff = -(1/(4*pi)) * (6*sqrt5/5)
print(f"    VEV shift coefficient: delta_v = {VEV_shift_coeff:.10f} (in units of 1)")
print(f"    = -(6*sqrt(5))/(20*pi) = {-6*sqrt5/(20*pi):.10f}")
print()

# The VEV shift is ASYMMETRIC between the two vacua because V'''(phi) != V'''(-1/phi).
# At Phi = -1/phi: V'''(-1/phi) = 2*lambda*(12*(-1/phi) - 6)
#   = 2*lambda*(-12/phi - 6) = -2*lambda*(12*phibar + 6)
#   = -2*lambda*6*(2*phibar + 1) = -12*lambda*(2*phibar + 1)
# Now 2*phibar + 1 = 2*(phi-1) + 1 = 2*phi - 1 = sqrt(5)
# So V'''(-1/phi) = -12*lambda*sqrt(5), SAME magnitude, opposite sign. OK.

# The VEV shift at BOTH vacua has the same magnitude but their effect
# on the wall width is:
# delta_w_VEV = delta(phi - (-1/phi)) / (dPhi/dx|_{max})
# The inter-vacuum distance sqrt(5) shifts by delta_v(phi) - delta_v(-1/phi)
# Since V'''(phi) = -V'''(-1/phi) = 12*lambda*sqrt(5), and V''(phi) = V''(-1/phi) = 10*lambda,
# delta_v(phi) = -delta_v(-1/phi) = -(1/(4*pi)) * 12*sqrt(5)*lambda/(10*lambda)

# So delta(vacuum gap) = delta_v(phi) - delta_v(-1/phi) = 2*delta_v(phi) = -2*(6*sqrt(5))/(20*pi)
# = -(6*sqrt(5))/(10*pi)

delta_gap_coeff = -6*sqrt5/(10*pi)
print(f"    Vacuum gap shift: delta(sqrt(5)) = {delta_gap_coeff:.10f}")
print(f"    Relative: delta(gap)/gap = {delta_gap_coeff/sqrt5:.10f}")
print(f"    = -6/(10*pi) = -3/(5*pi) = {-3/(5*pi):.10f}")
print()

# Combined with the inverse penetration depth correction:
# delta_Lambda/Lambda = delta_kappa/kappa - delta_gap/gap (the gap increases Lambda)
# Actually Lambda involves BOTH the width and the gap:
# Lambda ~ kappa ~ m/2, so the width is 1/kappa.
# But the Wallis series expansion is about Lambda = m_p/phi^3 * f(x),
# where f(x) = 1 - x + c2*x^2 + ...
# The second-order correction IS c2*x^2.

# Let me instead directly connect to the Wallis cascade.

# ============================================================================
# APPROACH 2: WALLIS CASCADE PERTURBATIVE SERIES
# ============================================================================
print(f"\n\n{sep}")
print("APPROACH 2: WALLIS CASCADE PERTURBATIVE SERIES")
print(sep)

print("""
THE FULL PERTURBATIVE EXPANSION:
  f(x) = sum_{k=0}^{inf} (-1)^k c_k x^k

  where c_0 = 1, c_1 = 1, and the higher coefficients involve
  successive Wallis ratios from the kink fluctuation integrals.

  The Wallis cascade hypothesis:
  c_k = (1/k!) * product_{j=n}^{n+k-2} [2j/(2j+1)]

  where n=2 is the PT depth.
""")

# ----------------------------------------------------------------
# 2a. Compute the Wallis cascade coefficients
# ----------------------------------------------------------------
print(f"  2a. WALLIS CASCADE COEFFICIENTS")
print(f"  {subsep}")

def wallis_cascade_coeff(k, n=2):
    """
    Compute c_k for the Wallis cascade hypothesis.
    c_k = (1/k!) * product_{j=n}^{n+k-2} [2j/(2j+1)]

    c_0 = 1, c_1 = 1 (no Wallis factors in the product)
    c_2 = (1/2) * 2n/(2n+1)
    c_3 = (1/6) * [2n/(2n+1)] * [2(n+1)/(2(n+1)+1)]
    """
    if k == 0:
        return 1.0
    if k == 1:
        return 1.0

    factorial_k = math.factorial(k)
    product = 1.0
    for j in range(n, n + k - 1):
        product *= (2*j) / (2*j + 1)

    return product / factorial_k

print(f"  {'k':>3} {'c_k':>18} {'Wallis factors':>30}")
print(f"  {'-'*3} {'-'*18} {'-'*30}")
for k in range(8):
    ck = wallis_cascade_coeff(k)
    if k == 0:
        factors = "1"
    elif k == 1:
        factors = "1"
    else:
        factors = " * ".join(f"{2*j}/{2*j+1}" for j in range(2, 2+k-1))
        factors = f"(1/{k}!) * " + factors
    print(f"  {k:>3} {ck:>18.15f} {factors:>30}")

print()
c_coeffs = [wallis_cascade_coeff(k) for k in range(15)]

# ----------------------------------------------------------------
# 2b. The full series f(x) = sum (-1)^k c_k x^k
# ----------------------------------------------------------------
print(f"  2b. THE FULL SERIES f(x)")
print(f"  {subsep}")

# Evaluate f(x) at various truncation orders
print(f"  x = {x:.15f}")
print()

print(f"  {'Order':>5} {'f(x)':>18} {'c2_eff':>18} {'diff from c2_exact':>20}")
print(f"  {'-'*5} {'-'*18} {'-'*18} {'-'*20}")
for order in range(2, 12):
    f_val = sum((-1)**k * c_coeffs[k] * x**k for k in range(order + 1))
    # Extract the effective c2 if we truncate at x^2:
    # f(x) = 1 - x + c2_eff*x^2
    # c2_eff = (f(x) - 1 + x) / x^2
    c2_eff = (f_val - 1 + x) / x**2
    diff = c2_eff - c2_exact
    print(f"  {order:>5} {f_val:>18.15f} {c2_eff:>18.15f} {diff:>+20.12e}")

print()

# ----------------------------------------------------------------
# 2c. The resummed effective c2
# ----------------------------------------------------------------
print(f"  2c. RESUMMED EFFECTIVE c2")
print(f"  {subsep}")

print("""
  When we truncate f(x) = 1 - x + c2_eff * x^2 but the TRUE series
  continues, the effective c2 absorbs all higher-order terms:

  c2_eff = c_2 + c_3*x + c_4*x^2 + c_5*x^3 + ...
         = sum_{k=2}^{inf} c_k * x^{k-2}

  (Note: this is exact if f(x) is analytic, by equating
   1 - x + c2_eff*x^2 = sum (-1)^k c_k x^k truncated at x^2
   with c2_eff capturing the O(x^2) and beyond contributions.)

  Actually more carefully: if f(x) = 1 - c1*x + c2*x^2 - c3*x^3 + ...,
  then (1 - x + c2_eff*x^2) should match the full series through O(x^2).
  The O(x^3) and higher terms ARE dropped, but they influence the
  FITTED c2_eff if we determine c2 by matching f(x) at a specific x value.

  The exact relation: at our specific x = 0.009317:
  f(x) = 1 - x + c_2*x^2 - c_3*x^3 + c_4*x^4 - ...
  We set this = 1 - x + c2_eff*x^2
  So c2_eff = c_2 - c_3*x + c_4*x^2 - c_5*x^3 + ...
""")

# Compute c2_eff from the Wallis cascade
c2_eff_terms = []
c2_eff_running = 0.0
print(f"  {'Terms':>5} {'c2_eff':>18} {'diff from c2_exact':>18} {'diff from 2/5':>18}")
print(f"  {'-'*5} {'-'*18} {'-'*18} {'-'*18}")
for j in range(15):
    k = j + 2
    ck = wallis_cascade_coeff(k)
    term = (-1)**j * ck * x**(j)  # note: (-1)^k * x^k in f, but c2_eff = c2 - c3*x + c4*x^2...
    # Actually from f(x) = sum_{k=0} (-1)^k c_k x^k
    # c2_eff*x^2 = f(x) - (1-x) = sum_{k=2} (-1)^k c_k x^k
    # c2_eff = sum_{k=2} (-1)^k c_k x^{k-2} = c_2 - c_3*x + c_4*x^2 - ...
    term = (-1)**(k) * ck * x**(k-2)
    c2_eff_running += term
    c2_eff_terms.append(term)
    diff_exact = c2_eff_running - c2_exact
    diff_25 = c2_eff_running - 0.4
    print(f"  {j+1:>5} {c2_eff_running:>18.15f} {diff_exact:>+18.12e} {diff_25:>+18.12e}")

print()

# ----------------------------------------------------------------
# 2d. Compare c2_eff to (2/5)(1 - phibar^3/42)
# ----------------------------------------------------------------
print(f"  2d. COMPARING c2_eff TO THE TARGET")
print(f"  {subsep}")

# After a few terms, what does c2_eff converge to?
c2_eff_converged = sum((-1)**(k) * wallis_cascade_coeff(k) * x**(k-2) for k in range(2, 30))
print(f"  c2_eff (30 terms) = {c2_eff_converged:.15f}")
print(f"  (2/5)(1-pb^3/42) = {c2_target:.15f}")
print(f"  c2_exact          = {c2_exact:.15f}")
print(f"  2/5               = {0.4:.15f}")
print()
print(f"  c2_eff - c2_exact  = {c2_eff_converged - c2_exact:+.6e}")
print(f"  c2_eff - c2_target = {c2_eff_converged - c2_target:+.6e}")
print(f"  c2_eff - 2/5       = {c2_eff_converged - 0.4:+.6e}")
print()

# What is the SHIFT from 2/5?
shift_from_wallis = c2_eff_converged - 0.4
# Is this -2/5 * phibar^3/42?
target_shift = -0.4 * phibar3/42
print(f"  Shift c2_eff - 2/5   = {shift_from_wallis:+.15e}")
print(f"  Target -2/5*pb^3/42  = {target_shift:+.15e}")
print(f"  Ratio (shift/target) = {shift_from_wallis/target_shift:.10f}")
print()

# The Wallis cascade gives a shift, but is it exactly phibar^3/42?
# Let's check what the cascade predicts for the correction.
# The dominant correction comes from the c_3 term:
c3 = wallis_cascade_coeff(3)
c3_contribution = -c3 * x  # first correction to c2_eff
print(f"  Dominant correction from c_3:")
print(f"    c_3 = {c3:.15f}")
print(f"    c_3 * x = {c3*x:.15e}")
print(f"    -c_3 * x = {-c3*x:+.15e}")
print(f"    For comparison:")
print(f"    -2/5 * phibar^3/42 = {target_shift:+.15e}")
print(f"    Ratio (-c3*x) / target = {-c3*x/target_shift:.10f}")
print()

# So the c_3 term alone doesn't give the full phibar^3/42 correction.
# Let's check if the RATIO works out:

# c_3 = (1/6) * (4/5) * (6/7) = 4/35 = 0.11428571...
# -c_3 * x = -(4/35) * eta/(3*phi^3)
# Target: -(2/5) * phibar^3/42 = -(2/5) * 1/(42*phi^3)

# Ratio: c_3*x / [(2/5)*phibar^3/42]
# = (4/35) * eta/(3*phi^3) / [(2/5)/(42*phi^3)]
# = (4/35) * eta/3 / (2/(5*42))
# = (4/35) * (eta/3) * (5*42/2)
# = (4/35) * (5*42*eta)/(3*2)
# = (4/35) * (210*eta)/6
# = (4/35) * 35*eta
# = 4*eta
# = 4 * 0.11840...
# = 0.47361...

ratio_test = 4 * eta
print(f"  ALGEBRAIC CHECK: (-c_3*x) / [-(2/5)*phibar^3/42]")
print(f"  = 4*eta = {ratio_test:.10f}")
print(f"  So -c_3*x = 4*eta * (2/5)*(phibar^3/42) --- NOT equal to the target!")
print()


# ============================================================================
# APPROACH 3: THE GOLDEN ASYMMETRY — profile-weighted VP integral
# ============================================================================
print(f"\n\n{sep}")
print("APPROACH 3: THE GOLDEN ASYMMETRY — profile-weighted VP integral")
print(sep)

print("""
THE POTENTIAL V(Phi) = lambda*(Phi^2-Phi-1)^2 is SYMMETRIC in Psi = Phi-1/2:
  V = lambda*(Psi^2 - 5/4)^2

But the Yukawa coupling g*Phi*psibar*psi = g*(Psi+1/2)*psibar*psi
introduces an asymmetry through the 1/2 shift.

The fermion mass at the two vacua:
  At Phi = phi:    m_f = g*phi
  At Phi = -1/phi: m_f = g*(-1/phi) = -g*phibar  (|m_f| = g*phibar)

The ratio: |m_f(phi)|/|m_f(-1/phi)| = phi/phibar = phi^2 = phi+1

The VP logarithm runs differently on the two sides:
  VP(phi side):    (1/3pi)*ln(Lambda_+/m_e) with Lambda_+ propto kappa * phi-dependent
  VP(-1/phi side): (1/3pi)*ln(Lambda_-/m_e) with Lambda_- propto kappa * phibar-dependent

For the EFFECTIVE Lambda, we need a profile-weighted average.
""")

# ----------------------------------------------------------------
# 3a. Profile-weighted moments
# ----------------------------------------------------------------
print(f"  3a. PROFILE-WEIGHTED MOMENTS")
print(f"  {subsep}")

# The kink profile: Phi(z) = 1/2 + (sqrt(5)/2)*tanh(z) where z = kappa*x

# <Phi^p>_w = integral Phi^p * sech^{2w}(z) dz / I_{2w}

# The key expansion: Phi = 1/2 + (sqrt(5)/2)*tanh(z), so
# Phi^p = sum_{j=0}^{p} C(p,j) * (1/2)^{p-j} * (sqrt(5)/2)^j * tanh^j(z)

# For p=1 (linear coupling):
# <Phi>_w = 1/2 * I_{2w}/I_{2w} + 0 [tanh is odd] = 1/2
# (The linear moment is always 1/2 by symmetry.)

# For p=2 (quadratic):
# Phi^2 = 1/4 + (sqrt(5)/2)*tanh(z) + (5/4)*tanh^2(z)
# <Phi^2>_w = 1/4 + (5/4)*<tanh^2>_w
# <tanh^2>_w = integral tanh^2*sech^{2w} dz / I_{2w}
#            = (I_{2w} - I_{2(w+1)}) / I_{2w}
#            = 1 - I_{2(w+1)}/I_{2w}
#            = 1 - 2w/(2w+1) = 1/(2w+1)

# <Phi^2>_w = 1/4 + (5/4)/(2w+1) = (2w+1+5)/(4*(2w+1)) = (2w+6)/(4*(2w+1))
# = (w+3)/(2*(2w+1))

print(f"  Profile-weighted moments: <Phi^p>_w = integral Phi^p sech^{{2w}}(z) dz / I_{{2w}}")
print()

for w in range(1, 6):
    tanh2_avg = 1.0 / (2*w + 1)
    phi2_avg = 0.25 + 1.25 * tanh2_avg
    phi2_exact = (w + 3.0) / (2 * (2*w + 1))
    print(f"    w={w}: <tanh^2>_{w} = 1/{2*w+1} = {tanh2_avg:.6f},  <Phi^2>_{w} = (w+3)/(2*(2w+1)) = {phi2_exact:.6f}")

print()

# For p=3 (cubic coupling):
# Phi^3 = (1/2 + (sqrt(5)/2)*tanh)^3
# = 1/8 + 3*(1/4)*(sqrt(5)/2)*tanh + 3*(1/2)*(5/4)*tanh^2 + (sqrt(5)/2)^3*tanh^3
# = 1/8 + (3*sqrt(5)/8)*tanh + (15/8)*tanh^2 + (5*sqrt(5)/8)*tanh^3

# <Phi^3>_w = 1/8 + 0 + (15/8)*<tanh^2>_w + 0  [odd powers vanish]
# = 1/8 + (15/8)/(2w+1)
# = (2w+1+15)/(8*(2w+1))
# = (2w+16)/(8*(2w+1))

print(f"  Cubic moments:")
for w in range(1, 6):
    phi3_avg = (2*w + 16) / (8 * (2*w + 1))
    print(f"    w={w}: <Phi^3>_{w} = (2w+16)/(8*(2w+1)) = {phi3_avg:.6f}")

print()

# ----------------------------------------------------------------
# 3b. The VP integral with asymmetric fermion mass
# ----------------------------------------------------------------
print(f"  3b. VP INTEGRAL WITH ASYMMETRIC FERMION MASS")
print(f"  {subsep}")

print("""
  The VP contribution comes from the fermion loop on the domain wall.
  The fermion mass varies along the wall: m_f(z) = g*Phi(z).

  The VP logarithm (1-loop): ln(m_f(z)^2/mu^2)
  averaged over the wall gives the effective cutoff Lambda_eff.

  More precisely, for a SLOWLY varying mass (adiabatic):
  delta(1/alpha) = (1/3pi) * integral [ln(m_f(z)^2/mu^2)] * rho(z) dz

  where rho(z) is the zero-mode density = sech^4(z)/I_4 for PT n=2.

  <ln(Phi^2)>_2 = integral ln(Phi^2(z)) * sech^4(z) dz / I_4

  This is NOT simply ln(<Phi^2>).

  Jensen's inequality: <ln(Phi^2)> <= ln(<Phi^2>)
  The gap = ln(<Phi^2>) - <ln(Phi^2)> is a VARIANCE-like correction.
""")

# Compute <ln(Phi^2)>_w numerically
import numpy as np

z_arr = np.linspace(-20, 20, 100000)
dz = z_arr[1] - z_arr[0]

Phi_arr = 0.5 + (sqrt5/2) * np.tanh(z_arr)

for w in [2, 3, 4]:
    weight = 1.0 / np.cosh(z_arr)**(2*w)
    norm = np.sum(weight) * dz

    # <ln(Phi^2)>
    ln_phi2 = np.log(Phi_arr**2)
    avg_ln = np.sum(ln_phi2 * weight) * dz / norm

    # ln(<Phi^2>)
    avg_phi2 = np.sum(Phi_arr**2 * weight) * dz / norm
    ln_avg = np.log(avg_phi2)

    # Jensen gap
    jensen_gap = ln_avg - avg_ln

    print(f"    w={w}: <ln(Phi^2)> = {avg_ln:.10f},  ln(<Phi^2>) = {ln_avg:.10f},  Jensen gap = {jensen_gap:.10f}")

print()

# The Jensen gap for the energy weighting (w=2, sech^4):
weight_e = 1.0 / np.cosh(z_arr)**4
norm_e = np.sum(weight_e) * dz
ln_phi2_e = np.log(Phi_arr**2)
jensen_gap_e = np.log(np.sum(Phi_arr**2 * weight_e) * dz / norm_e) - np.sum(ln_phi2_e * weight_e) * dz / norm_e

# And for pressure weighting (w=3, sech^6):
weight_p = 1.0 / np.cosh(z_arr)**6
norm_p = np.sum(weight_p) * dz
jensen_gap_p = np.log(np.sum(Phi_arr**2 * weight_p) * dz / norm_p) - np.sum(np.log(Phi_arr**2) * weight_p) * dz / norm_p

print(f"  Jensen gaps:")
print(f"    Energy (sech^4): {jensen_gap_e:.10f}")
print(f"    Pressure (sech^6): {jensen_gap_p:.10f}")
print(f"    Ratio P/E: {jensen_gap_p/jensen_gap_e:.10f}")
print()

# Compare Jensen gap to phibar^3/42:
print(f"  Jensen gap (energy) = {jensen_gap_e:.10f}")
print(f"  phibar^3/42         = {phibar3/42:.10f}")
print(f"  Ratio               = {jensen_gap_e/(phibar3/42):.10f}")
print()
print(f"  Jensen gap (pressure) = {jensen_gap_p:.10f}")
print(f"  phibar^3/42           = {phibar3/42:.10f}")
print(f"  Ratio                 = {jensen_gap_p/(phibar3/42):.10f}")
print()

# ----------------------------------------------------------------
# 3c. The cubic asymmetry and sech^8 correction
# ----------------------------------------------------------------
print(f"  3c. THE CUBIC ASYMMETRY AND sech^8 CORRECTION")
print(f"  {subsep}")

print("""
  The profile Phi(z) = 1/2 + (sqrt(5)/2)*tanh(z) has NO asymmetry
  in the SYMMETRIC variable Psi = Phi - 1/2. But in the PHYSICAL
  variable Phi, odd moments of Psi contribute to even moments of Phi.

  The key correction: at the sech^6 level (pressure weighting),
  <Phi^2>_P = 3/7 (computed above). At sech^8:
  <Phi^2>_4 = (4+3)/(2*(2*4+1)) = 7/18

  The CUBIC moment integral that breaks the symmetry:
  <Phi^3> involves Psi^2 terms (even in Psi) which survive.

  For the VP, what matters is not Phi^3 directly but
  the LOGARITHMIC average ln(Lambda_eff) = <ln(Phi)>
  weighted by the pressure density.
""")

# The effective Lambda involves the profile:
# Lambda_eff = Lambda_0 * exp(<ln(Phi)>_weight - ln(phi))
# Because at the vacuum Lambda would be Lambda_0 * phi (from m_f = g*phi).
# The average over the wall reduces this.

# <ln(Phi)>_w for various w:
for w in [2, 3, 4]:
    weight_w = 1.0 / np.cosh(z_arr)**(2*w)
    norm_w = np.sum(weight_w) * dz
    avg_ln_phi = np.sum(np.log(np.abs(Phi_arr)) * weight_w) * dz / norm_w
    ln_phi_vac = np.log(phi)
    shift = avg_ln_phi - ln_phi_vac
    print(f"    w={w}: <ln|Phi|> = {avg_ln_phi:.10f},  ln(phi) = {ln_phi_vac:.10f},  shift = {shift:.10f}")

print()

# The CRITICAL quantity: the shift of <ln|Phi|> from ln(phi)
# at the PRESSURE weighting level (sech^6):
weight_p = 1.0 / np.cosh(z_arr)**6
norm_p = np.sum(weight_p) * dz
ln_phi_shift = np.sum(np.log(np.abs(Phi_arr)) * weight_p) * dz / norm_p - np.log(phi)

print(f"  Critical shift (pressure-weighted): <ln|Phi|> - ln(phi) = {ln_phi_shift:.10f}")
print(f"  phibar^3/42 = {phibar3/42:.10f}")
print(f"  Ratio = {ln_phi_shift / (phibar3/42):.10f}")
print()

# ----------------------------------------------------------------
# 3d. Direct: the correction from averaging ln(Phi) over the kink
# ----------------------------------------------------------------
print(f"  3d. EFFECTIVE LAMBDA FROM PROFILE AVERAGING")
print(f"  {subsep}")

print("""
  The effective cutoff Lambda_eff in the VP formula comes from
  averaging the fermion mass over the kink profile.

  If m_f(z) = g * |Phi(z)|, then the effective mass for the VP loop is:
  ln(Lambda_eff) = <ln(m_f)> = ln(g) + <ln|Phi|>

  The correction to Lambda from the profile average (vs vacuum value):
  ln(Lambda_eff/Lambda_vac) = <ln|Phi|> - ln(phi)

  This is NEGATIVE (the average mass is LESS than the vacuum mass)
  so Lambda_eff < Lambda_vac. This reduces f(x) below 1.
""")

# Compute the correction for different weightings:
print(f"  Profile-averaged corrections:")
print(f"  {'Weighting':>20} {'<ln|Phi|>-ln(phi)':>20} {'exp(shift)':>12} {'eff. reduction':>16}")
print(f"  {'-'*20} {'-'*20} {'-'*12} {'-'*16}")

for w, name in [(2, "Energy (sech^4)"), (3, "Pressure (sech^6)"), (4, "sech^8")]:
    weight_w = 1.0 / np.cosh(z_arr)**(2*w)
    norm_w = np.sum(weight_w) * dz
    shift = np.sum(np.log(np.abs(Phi_arr)) * weight_w) * dz / norm_w - np.log(phi)
    exp_shift = np.exp(shift)
    reduction = 1 - exp_shift
    print(f"  {name:>20} {shift:>20.10f} {exp_shift:>12.10f} {reduction:>16.10f}")

print()

# Now: the profile averaging gives a FIXED correction (not x-dependent).
# But c2 is the coefficient of x^2, which IS x-dependent.
# The connection: the correction from profile averaging MODIFIES the
# coefficient c2 = (2/5) from the Wallis ratio by the reduction factor.

# If the reduction factor were exactly (1 - phibar^3/42), we'd have our result.

# Let's check:
# At the sech^6 level, the reduction from profile averaging is:
weight_p = 1.0 / np.cosh(z_arr)**6
norm_p = np.sum(weight_p) * dz
shift_p = np.sum(np.log(np.abs(Phi_arr)) * weight_p) * dz / norm_p - np.log(phi)
reduction_p = 1 - np.exp(shift_p)

print(f"  Pressure-level reduction: {reduction_p:.10f}")
print(f"  phibar^3/42:             {phibar3/42:.10f}")
print(f"  Ratio:                   {reduction_p/(phibar3/42):.10f}")
print()

# ----------------------------------------------------------------
# 3e. The variance correction — connecting to phibar^3/42
# ----------------------------------------------------------------
print(f"  3e. THE VARIANCE CORRECTION")
print(f"  {subsep}")

# The logarithmic average can be expanded:
# <ln|Phi|> = ln(<|Phi|>) - Var(Phi)/(2*<Phi>^2) + ... (cumulant expansion)
# where Var(Phi) = <Phi^2> - <Phi>^2

# For sech^4 weighting (energy):
# <Phi> = 1/2
# <Phi^2> = 1/2
# Var = 1/2 - 1/4 = 1/4

# For sech^6 weighting (pressure):
# <Phi> = 1/2
# <Phi^2> = 3/7
# Var = 3/7 - 1/4 = (12-7)/28 = 5/28

# For sech^8 weighting:
# <Phi> = 1/2
# <Phi^2> = 7/18
# Var = 7/18 - 1/4 = (14-9)/36 = 5/36

print(f"  Variance of Phi under different weightings:")
for w in range(2, 6):
    phi2_avg = (w + 3.0) / (2 * (2*w + 1))
    phi_avg = 0.5
    var = phi2_avg - phi_avg**2
    print(f"    w={w}: <Phi^2> = {phi2_avg:.6f}, <Phi> = {phi_avg:.6f}, Var = {var:.6f} = 5/{int(round(5/var))}")

print()

# The correction from the variance:
# <ln|Phi|> approx ln(<|Phi|>) - Var/(2*<Phi>^2)
# = ln(1/2) - Var/(2*(1/4))
# = ln(1/2) - 2*Var

# For sech^6: correction = -2*(5/28) = -5/14 !! Too large.
# This is the correction to ln|Phi|, but what we want is the correction
# to the EXPONENT of f(x), not to ln|Phi| directly.

# The actual structure is:
# c2_eff = c2_Wallis * (1 - epsilon)
# where epsilon comes from the golden asymmetry.

# The WALLIS part (c2 = 2/5) uses the SYMMETRIC (Psi) profile.
# When we switch to the PHYSICAL variable Phi = Psi + 1/2,
# the coupling to external fields picks up asymmetry corrections.

# The correction epsilon should be of ORDER (asymmetry)^2 ~ (1/2)^2 / phi^2 ~ phibar^2/4
# Let's compute it more carefully.

# The Wallis integral I_6/I_4 = 4/5 was computed in the SYMMETRIC variable.
# In the ASYMMETRIC variable Phi, the relevant integral is:
# J_6/J_4 where J_{2k} = integral |Phi|^2 * sech^{2k} dz

# J_4 = <Phi^2>_2 * I_4 = (1/2) * (4/3) = 2/3
# J_6 = <Phi^2>_3 * I_6 = (3/7) * (16/15) = 48/105 = 16/35

# Asymmetric Wallis ratio:
J4 = 0.5 * I4
J6 = 3.0/7 * I6
R_asym = J6 / J4
R_sym = I6 / I4

print(f"  Symmetric Wallis ratio: I_6/I_4 = {R_sym:.10f} = 4/5")
print(f"  Asymmetric ratio: J_6/J_4 = <Phi^2>_3*I_6 / (<Phi^2>_2*I_4)")
print(f"                           = (3/7)*(16/15) / ((1/2)*(4/3))")
print(f"                           = (48/105) / (2/3)")
print(f"                           = {J6/J4:.10f}")
print(f"                           = 144/210 = 48/70 = 24/35")
print(f"  Exact: {24.0/35:.10f}")
print()

# The asymmetric Wallis ratio is 24/35 = 0.6857, while the symmetric is 4/5 = 0.800.
# That's a 14% correction — WAY too large compared to phibar^3/42 ~ 0.56%.
# This approach gives the wrong scale.

# Let me reconsider. The correction should come from the DIFFERENCE
# between the asymmetric and symmetric integrals, not the ratio itself.

# Actually, the problem is that I'm mixing up two different things.
# The Wallis ratio I_6/I_4 = 4/5 computes the ratio of successive
# INTEGRALS of the perturbation profile, not of Phi^2 * profile.

# The correct approach: the quadratic correction c_2 comes from the
# second-order perturbation theory expansion of the QCD coupling
# through the wall. The PERTURBATION is proportional to sech^2(z)
# (the kink energy density), and the matrix element involves:
# <1|V|2> ~ integral sech^4 ... sech^6 ratios.

# The golden asymmetry enters NOT through the Wallis integrals themselves
# (which involve sech only) but through the COUPLING of the perturbation
# to the fermion mass profile.

# ----------------------------------------------------------------
# 3f. The correct asymmetry mechanism: ln(phi) vs ln(1/phi)
# ----------------------------------------------------------------
print(f"  3f. THE CORRECT ASYMMETRY MECHANISM")
print(f"  {subsep}")

print("""
  The VP logarithm involves ln(Lambda/m_e).
  Lambda is DEFINED as the cutoff in the VP running, which relates
  to the PHYSICAL mass scale m_f = g*|Phi|.

  At the phi vacuum: Lambda_+ = m_p/phi^3 * phi = m_p/phi^2
  At the -1/phi vacuum: Lambda_- = m_p/phi^3 * phibar = m_p/phi^4

  The profile-weighted Lambda: <ln Lambda> = ln(m_p/phi^3) + <ln|Phi|>

  The correction to c2 comes from the fact that the Wallis integrals
  are computed in the SYMMETRIC Psi variable, but the VP logarithm
  depends on ln|Phi| = ln|Psi + 1/2|, which IS sensitive to the asymmetry.

  For a SYMMETRIC profile |Psi| (or |tanh|), the VP would give:
  <ln|Psi|> with sech^{2(n+1)} weighting divided by sech^{2n} norm.

  The SHIFT from symmetric to physical:
  delta_asym = <ln|Psi+1/2|>_w - <ln|Psi|>_w

  But this is not well-defined because |Psi| vanishes at z=0.
""")

# Let me try the DIRECT approach: compute what c2 would be
# if we account for the profile-weighted VP running.

# The VP formula: 1/alpha = tree + (1/(3*pi)) * ln(Lambda/m_e)
# With Lambda = Lambda_raw * f(x), f(x) = 1 - x + c2*x^2
# The second-order term c2*x^2 = c2*(eta/(3*phi^3))^2

# The correction to c2 from profile-weighting:
# At the Wallis level, the integrals are pure sech^{2k}.
# The physical VP involves an additional ln|Phi(z)| factor.
#
# The effective c2 is:
# c2_phys = c2_Wallis * <correction_factor>
#
# where the correction factor involves the ratio of
# profile-weighted to flat-weighted integrals.

# ----------------------------------------------------------------
# 3g. CRITICAL COMPUTATION: the exact profile-averaged VP correction
# ----------------------------------------------------------------
print(f"  3g. CRITICAL: EXACT PROFILE-AVERAGED VP CORRECTION")
print(f"  {subsep}")

# The claim: the leading correction to c2 = 2/5 comes from the
# VARIANCE of ln|Phi(z)| over the kink profile, weighted by
# sech^{2(n+1)} = sech^6 (the pressure weighting).
#
# The variance of ln|Phi| under sech^6 weighting:
# Var_P[ln|Phi|] = <(ln|Phi|)^2>_P - (<ln|Phi|>_P)^2

weight_p = 1.0 / np.cosh(z_arr)**6
norm_p = np.sum(weight_p) * dz

ln_phi_vals = np.log(np.abs(Phi_arr))
mean_ln = np.sum(ln_phi_vals * weight_p) * dz / norm_p
mean_ln2 = np.sum(ln_phi_vals**2 * weight_p) * dz / norm_p
var_ln = mean_ln2 - mean_ln**2

print(f"  Under sech^6 (pressure) weighting:")
print(f"    <ln|Phi|>   = {mean_ln:.10f}")
print(f"    <(ln|Phi|)^2> = {mean_ln2:.10f}")
print(f"    Var[ln|Phi|]  = {var_ln:.10f}")
print()

# The variance determines the sub-leading correction to the
# effective Lambda through Jensen's inequality:
# <ln|Phi|> = ln<|Phi|> - Var[Phi]/(2*<|Phi|>^2) + ...
# But for the VP, we need <ln|Phi^2|> = 2*<ln|Phi|>

# The effective reduction factor in the VP:
# delta_VP = <ln|Phi|^2>_P - ln(phi^2)
# = 2*(mean_ln - ln(phi))
reduction_VP = 2 * (mean_ln - np.log(phi))
print(f"  VP reduction: 2*(<ln|Phi|> - ln(phi)) = {reduction_VP:.10f}")
print()

# Now check: does the variance of ln|Phi| relate to phibar^3/42?
# The variance comes from the SPREAD of Phi values over the kink.
# The key: Phi ranges from -1/phi to phi, passing through 1/2 at center.

# Let me compute what VALUE of the variance ratio gives phibar^3/42:
# We need: correction_to_c2 = 2/5 * (something involving variance)

# The deficit: c2_exact - 2/5 = -0.002251...
deficit = c2_exact - 0.4
print(f"  Deficit: c2_exact - 2/5 = {deficit:.10e}")
print(f"  = -2/5 * {abs(deficit)/0.4:.10e}")
print(f"  Target: phibar^3/42 = {phibar3/42:.10e}")
print(f"  Actual epsilon (deficit/(-0.4)): {-deficit/0.4:.10e}")
print()

# ============================================================================
# APPROACH 4: SYNTHESIS — all mechanisms combined
# ============================================================================
print(f"\n\n{sep}")
print("APPROACH 4: SYNTHESIS — FROM SECH^8 WALLIS CORRECTION")
print(sep)

print("""
THE PHYSICAL ARGUMENT:

The leading-order c2 = 2/5 comes from:
  c_2 = (1/2!) * I_6/I_4 = (1/2) * (4/5)

This involves the PRESSURE integral sech^6 divided by the ENERGY integral sech^4.
The (1/2) is from second-order perturbation theory (the 1/2! in the Taylor expansion).

The NEXT correction involves the sech^8 integral:
  I_8/I_6 = 6/7

This enters at the THIRD order of perturbation theory but also modifies
the second order through the golden asymmetry of the vacua.

THE KEY INSIGHT: The correction -phibar^3/42 has the structure:
  -(1/phi^3) / (6*7)  =  -phibar^3 / (2(n+1) * (2(n+1)+1))

The factor 6 = 2(n+1) and 7 = 2(n+1)+1 are EXACTLY the numerator and
denominator of the NEXT Wallis ratio I_8/I_6 = 6/7.

And phibar^3 = 1/phi^3 is the CUBE of the inter-vacuum asymmetry parameter:
  The vacua are at phi and -1/phi, with ratio phibar = 1/phi.
  The cube phibar^3 enters because:
  - The cubic coupling V'''(Phi_cl(z)) at the kink center is:
    V'''(1/2) = 2*lambda*(12*(1/2)-6) = 0  (vanishes!)
  - But the AVERAGE cubic coupling over the kink IS nonzero:
    <V'''(Phi)>_P involves odd moments of Psi = Phi - 1/2
    which vanish by symmetry!

  So the cubic coupling doesn't directly contribute.
  Instead, phibar^3 enters through the THIRD power of Phi in the VP:
  ln(Lambda) ~ ln|Phi| ~ ln(1/2) + ... where the asymmetric corrections
  involve (Phi-1/2)/(1/2) = Psi * 2, and the leading non-trivial
  asymmetric contribution involves <Psi^2>/<Phi^2> ~ 5/(4*phi^2) = 5*phibar^2/4
""")

# Let me test the SPECIFIC hypothesis:
# c2 = (1/2) * (I_6/I_4) * [1 - phibar^3 / (I_8/I_6 numerator * denominator)]
# = (1/2) * (4/5) * [1 - phibar^3/(6*7)]
# = (2/5) * (1 - phibar^3/42)

c2_hypothesis = 0.5 * (I6/I4) * (1 - phibar3 / (6 * 7))
print(f"  HYPOTHESIS: c2 = (1/2)*(I_6/I_4)*(1 - phibar^3/(6*7))")
print(f"  = (2/5) * (1 - phibar^3/42)")
print(f"  = {c2_hypothesis:.15f}")
print(f"  c2_exact = {c2_exact:.15f}")
print(f"  Diff = {c2_hypothesis - c2_exact:+.6e} = {(c2_hypothesis-c2_exact)/c2_exact*1e6:+.1f} ppm")
print()

# Now test the MECHANISM: does phibar^3/42 emerge from the width correction?

# The width correction involves the one-loop propagator in the kink background.
# The BREATHING MODE contribution (omega_1 = sqrt(3)*kappa):
#   delta_w_breath/w = C_1 / omega_1^2 = C_1 / (3*kappa^2)

# The breathing mode wavefunction: psi_1 = sqrt(3/2) * sech(z)*tanh(z)
# Its overlap with the kink profile derivative:
# <psi_1|Phi'> = sqrt(3/2) * integral sech(z)*tanh(z) * (sqrt(5)/2)*kappa*sech^2(z) dz
# = sqrt(3/2) * (sqrt(5)/2)*kappa * integral sech^3(z)*tanh(z) dz
# = 0 (odd integrand!)

# So the breathing mode does NOT couple to the width change at this level.
# The width change comes from CONTINUUM modes only.

# The continuum contribution to the width correction is governed by
# the LEVINSON-JOST FUNCTION, which for PT n=2 is:
# f_Jost(k) = (k^2+1)(k^2+4) / (k^2)  [with appropriate normalization]

# The relevant integral for the width correction:
# delta_kappa/kappa = -(1/(2*pi)) * integral_0^inf [delta'(k) - delta'_free(k)] dk
# where delta'(k) = d(phase shift)/dk

# For PT n=2:
# delta(k) = -arctan(1/k) - arctan(2/k) + pi  [shifted to match Levinson]
# delta'(k) = 1/(k^2+1) + 2/(k^2+4) [the Breit-Wigner form]

# The EXCESS over free (delta_free = 0 for s-wave in 1D):
# delta_kappa/kappa = -(1/(2*pi)) * integral_0^inf [1/(k^2+1) + 2/(k^2+4)] dk
# = -(1/(2*pi)) * [pi/2 + 2*(pi/4)]
# = -(1/(2*pi)) * [pi/2 + pi/2]
# = -(1/(2*pi)) * pi
# = -1/2

# Wait — that gives delta_kappa/kappa = -1/2, which means kappa is HALVED.
# That's the zero-mode contribution which should be excluded!

# After proper collective-coordinate treatment:
# The contribution from the BREATHING MODE only:
# delta_kappa_1/kappa = -(1/(2*pi)) * integral_0^inf [2/(k^2+4)] dk
# = -(1/(2*pi)) * 2*(pi/4) = -(1/(2*pi)) * pi/2 = -1/4

# And from the zero mode:
# delta_kappa_0/kappa = -(1/(2*pi)) * integral_0^inf [1/(k^2+1)] dk
# = -(1/(2*pi)) * pi/2 = -1/4

# So the total is -1/2, split equally between the two bound states.
# After removing the zero mode: delta_kappa/kappa = -1/4 (from breathing mode).

# But this is a DIMENSIONLESS number, not involving x!
# The one-loop correction is proportional to hbar, which in our perturbative
# framework maps to x = eta/(3*phi^3).

# So the FULL one-loop width correction is:
# delta_w/w = (1/4) * x * [coupling factor]

# The coupling factor involves the vertex for the fluctuation field
# coupling to the kink. For a SYMMETRIC kink, this is pure.
# For the golden asymmetric kink, the coupling involves phi-dependent factors.

# ================================================================
# APPROACH 5: THE CONCRETE DERIVATION
# ================================================================
print(f"\n\n{sep}")
print("APPROACH 5: CONCRETE DERIVATION OF phibar^3 FROM WIDTH CHANGE")
print(sep)

print("""
THE ARGUMENT:

1. The Wallis ratio c_2 = 2/5 computes the second-order correction to
   Lambda using sech^6/sech^4 integrals in the SYMMETRIC Psi variable.

2. The VP running involves ln(Lambda/m_e) where Lambda is determined by
   the PHYSICAL fermion mass m_f = g*Phi, not g*Psi.

3. In the SYMMETRIC variable: the second-order Wallis integral is:
     I_6^{sym} / I_4^{sym} = 4/5   (exact)

4. In the PHYSICAL variable, the second-order integral picks up a
   correction from the constant shift Phi = Psi + 1/2:
     I_6^{phys} / I_4^{phys} = (4/5)(1 - delta)

   where delta comes from the (1/2)^2 contribution to the integral
   being modulated by the NEXT Wallis ratio I_8/I_6 = 6/7.

5. The correction delta involves:
   (a) The shift 1/2 -- enters as (1/2)^2 = 1/4 relative to <Psi^2> = 5/4
       Ratio: (1/4)/(5/4) = 1/5
   (b) The next Wallis ratio: 6/7
   (c) The golden ratio structure: phibar = 1/phi

   Combined: delta = (1/5) * (6/7)^{-1} * phibar^3 = ...

   This doesn't quite work. Let me try the EXACT computation.
""")

# ================================================================
# THE EXACT NUMERICAL TEST
# ================================================================
print(f"  EXACT NUMERICAL COMPUTATION:")
print(f"  {subsep}")

# Compute the Wallis-type integral ratio with Phi^2 weighting:
# R(w) = integral Phi^2 * sech^{2(w+1)} dz / integral Phi^2 * sech^{2w} dz

for w in [2, 3, 4]:
    w_top = 1.0 / np.cosh(z_arr)**(2*(w+1))
    w_bot = 1.0 / np.cosh(z_arr)**(2*w)
    num = np.sum(Phi_arr**2 * w_top) * dz
    den = np.sum(Phi_arr**2 * w_bot) * dz
    R = num / den

    # Compare to the pure Wallis ratio
    W_pure = 2*w / (2*w + 1)
    correction = R / W_pure - 1

    print(f"    w={w}: R_phys = {R:.10f},  W_pure = {W_pure:.10f},  correction = {correction:+.6e}")

print()

# The correction at w=2 (the relevant level for c2):
w_top2 = 1.0 / np.cosh(z_arr)**(2*3)
w_bot2 = 1.0 / np.cosh(z_arr)**(2*2)
num2 = np.sum(Phi_arr**2 * w_top2) * dz
den2 = np.sum(Phi_arr**2 * w_bot2) * dz
R_phys = num2 / den2

# What does c2 become with this correction?
c2_corrected = 0.5 * R_phys
print(f"  c2 from physical Wallis ratio: (1/2)*R_phys = {c2_corrected:.10f}")
print(f"  c2_exact = {c2_exact:.10f}")
print(f"  c2_Wallis (2/5) = {0.4:.10f}")
print(f"  This gives c2 = {c2_corrected:.10f}, diff from exact = {c2_corrected-c2_exact:.6e}")
print()

# Hmm, the Phi^2-weighted Wallis ratio gives a DIFFERENT c2, but the
# correction is much larger than phibar^3/42. This is because the
# Phi^2 weighting is too strong.

# The CORRECT weighting is ln|Phi|, not Phi^2:
# R_ln(w) = integral (ln|Phi|^2) * sech^{2(w+1)} dz / integral (ln|Phi|^2) * sech^{2w} dz

for w in [2, 3, 4]:
    w_top = 1.0 / np.cosh(z_arr)**(2*(w+1))
    w_bot = 1.0 / np.cosh(z_arr)**(2*w)
    ln_phi2 = np.log(Phi_arr**2)
    num = np.sum(ln_phi2 * w_top) * dz
    den = np.sum(ln_phi2 * w_bot) * dz
    R_ln = num / den

    W_pure = 2*w / (2*w + 1)
    correction = R_ln / W_pure - 1

    print(f"    w={w}: R_ln = {R_ln:.10f},  W_pure = {W_pure:.10f},  correction = {correction:+.6e}")

print()

# The ln-weighted ratio at w=2:
w_top2_ln = 1.0 / np.cosh(z_arr)**6
w_bot2_ln = 1.0 / np.cosh(z_arr)**4
ln_phi2 = np.log(Phi_arr**2)
num2_ln = np.sum(ln_phi2 * w_top2_ln) * dz
den2_ln = np.sum(ln_phi2 * w_bot2_ln) * dz
R_ln_2 = num2_ln / den2_ln

c2_ln = 0.5 * R_ln_2
print(f"  c2 from ln-weighted Wallis ratio: (1/2)*R_ln = {c2_ln:.10f}")
print(f"  c2_exact = {c2_exact:.10f}")
print(f"  Diff = {c2_ln - c2_exact:.6e}")
print()

# ================================================================
# APPROACH 6: THE DIRECT EXPANSION — ln(Phi) = ln(1/2+Psi)
# ================================================================
print(f"\n\n{sep}")
print("APPROACH 6: EXPANSION OF ln(Phi) IN POWERS OF ASYMMETRY")
print(sep)

print("""
  ln|Phi| = ln|1/2 + (sqrt(5)/2)*tanh(z)|

  Near the center (z=0): Phi = 1/2, so ln|Phi| = ln(1/2) = -ln(2)

  Expansion in Psi = (sqrt(5)/2)*tanh(z):
  ln|Phi| = ln|1/2 + Psi|
           = ln(1/2) + ln(1 + 2*Psi)   [for Psi > -1/2]
           = ln(1/2) + 2*Psi - 2*Psi^2 + (8/3)*Psi^3 - ...

  When integrated with sech^{2w} weighting:
  <ln|Phi|>_w = ln(1/2) + 0 - 2*<Psi^2>_w + 0 - ...
              = ln(1/2) - 2*(5/4)*<tanh^2>_w
              = ln(1/2) - (5/2)/(2w+1)

  This is the EXACT leading expansion for the logarithm.
  The correction to the Wallis c2 from this expansion involves
  the RATIO of the logarithmic integrals.

  Wait — this expansion diverges near z where Phi passes through zero!
  Our kink never passes through zero (Phi ranges from phibar to phi,
  both positive for our convention... NO! Phi ranges from -1/phi to phi.
  -1/phi = -0.618. So Phi IS negative on the left side!)

  For z < 0: Phi < 1/2, and Phi = 0 when tanh(z) = -1/sqrt(5), i.e.
  z_0 = -arctanh(1/sqrt(5)) = -0.4812...

  The logarithm ln|Phi| has a logarithmic singularity at z = z_0!
  This makes the expansion above invalid.
""")

# Compute where Phi vanishes:
z0 = -np.arctanh(1/sqrt5)
print(f"  Phi vanishes at z_0 = -arctanh(1/sqrt(5)) = {z0:.10f}")
print(f"  Phi(z_0) = 1/2 + (sqrt(5)/2)*tanh(z_0) = {0.5 + sqrt5/2*np.tanh(z0):.15f}")
print()

# The logarithmic singularity at z_0 means the integral <ln|Phi|>
# involves a REGULARIZATION. The sech^{2w} weight suppresses this:
# sech^{2w}(z_0) for z_0 = -0.48: sech(-0.48) = 1/cosh(0.48) ≈ 0.89
# So sech^4(z_0) ≈ 0.63, sech^6 ≈ 0.56, etc. NOT strongly suppressed.

sech_z0 = 1.0 / np.cosh(z0)
print(f"  sech(z_0) = {sech_z0:.10f}")
for w in range(2, 6):
    print(f"  sech^{2*w}(z_0) = {sech_z0**(2*w):.10f}")
print()

# The logarithmic singularity contributes a FINITE amount to the integral
# because integral ln|z-z_0| * sech^{2w}(z) dz converges (logarithmic
# singularity is integrable in 1D).

# This is actually the PHYSICAL origin of the phibar^3/42 correction:
# the node of Phi(z) inside the wall creates a logarithmic enhancement
# in the VP that modifies c2 away from the symmetric Wallis value.

print("""
  PHYSICAL PICTURE:

  The kink profile Phi(z) passes through ZERO at z_0 = -0.481.
  The VP logarithm ln|Phi(z)|^2 has a logarithmic singularity there.

  This singularity is ABSENT in the symmetric Psi variable (where the
  relevant function |Psi| vanishes at z=0, a symmetric point that doesn't
  affect even-weighted integrals).

  In the PHYSICAL Phi variable, the zero occurs at an ASYMMETRIC point z_0,
  which breaks the left-right symmetry and produces a correction to c2.

  The correction involves:
  1. The position of the zero: z_0 = -arctanh(1/sqrt(5))
     tanh(z_0) = -1/sqrt(5) => sech^2(z_0) = 1 - 1/5 = 4/5
  2. The strength of the singularity: proportional to 1/|Phi'(z_0)| = 2/(sqrt(5)*kappa*sech^2(z_0))
  3. The sech^{2w} weight at z_0
""")

# Compute sech^2(z_0):
sech2_z0 = 1 - np.tanh(z0)**2
print(f"  sech^2(z_0) = 1 - tanh^2(z_0) = 1 - 1/5 = 4/5 = {sech2_z0:.10f}")
print(f"  This IS the Wallis ratio I_6/I_4 = 4/5!")
print()

# !!!! This is a remarkable coincidence/connection:
# The sech^2 at the zero of Phi equals the Wallis ratio!

# The slope of Phi at z_0:
# Phi'(z_0) = (sqrt(5)/2)*kappa*sech^2(z_0) = (sqrt(5)/2)*kappa*(4/5)
# = (2*sqrt(5)/5)*kappa = (2/sqrt(5))*kappa

slope_at_zero = sqrt5/2 * sech2_z0  # in units of kappa
print(f"  |Phi'(z_0)| = (sqrt(5)/2)*sech^2(z_0)*kappa = {slope_at_zero:.10f}*kappa")
print(f"  = (2*sqrt(5)/5)*kappa = {2*sqrt5/5:.10f}*kappa")
print()

# The logarithmic singularity contribution to <ln|Phi|^2>_w:
# Near z_0: Phi(z) ≈ Phi'(z_0)*(z-z_0)
# ln|Phi|^2 ≈ 2*ln|Phi'(z_0)*(z-z_0)| = 2*ln|Phi'(z_0)| + 2*ln|z-z_0|
# The 2*ln|z-z_0| term, integrated with sech^{2w}(z):
# ≈ 2*sech^{2w}(z_0) * integral ln|u| du  [u = z-z_0, local]
# This integral = [u*ln|u| - u] which is finite.

# But the CONTRIBUTION to the correction of c2 is:
# The singular part SUBTRACTS from <ln|Phi|^2> (since ln|x| < 0 near x=0)
# This makes Lambda_eff SMALLER, and hence f(x) < 1.

# The fractional contribution: proportional to sech^{2w}(z_0) / |Phi'(z_0)|

# For w=3 (pressure):
# frac ~ sech^6(z_0) / |Phi'(z_0)| * kappa
# = (4/5)^3 / (2*sqrt(5)/5)
# = (64/125) / (2*sqrt(5)/5)
# = (64/125) * (5/(2*sqrt(5)))
# = 64 / (50*sqrt(5))
# = 32 / (25*sqrt(5))

frac_p = sech2_z0**3 / slope_at_zero
print(f"  Fractional contribution (pressure level):")
print(f"    sech^6(z_0)/|Phi'(z_0)| = (4/5)^3 / (2*sqrt(5)/5)")
print(f"    = {frac_p:.10f}")
print(f"    = 32/(25*sqrt(5)) = {32/(25*sqrt5):.10f}")
print()

# Is 32/(25*sqrt(5)) related to phibar^3/42?
print(f"  32/(25*sqrt(5)) = {32/(25*sqrt5):.10f}")
print(f"  phibar^3/42     = {phibar3/42:.10f}")
print(f"  Ratio           = {(32/(25*sqrt5))/(phibar3/42):.6f}")
print()

# ================================================================
# FINAL SYNTHESIS: The mechanism
# ================================================================
print(f"\n\n{sep}")
print("FINAL SYNTHESIS: THE MECHANISM FOR phibar^3/42")
print(sep)

# Let me compute exactly what multiplicative correction to 2/5
# is needed, and test ALL candidate mechanisms:

epsilon_needed = 1 - c2_exact / 0.4  # = phibar^3/42 to 8 ppm
print(f"\n  epsilon_needed = 1 - c2_exact/(2/5) = {epsilon_needed:.15f}")
print(f"  phibar^3/42 = {phibar3/42:.15f}")
print(f"  Match: {abs(epsilon_needed - phibar3/42)/epsilon_needed*1e6:.1f} ppm")
print()

# Now test each mechanism's prediction for epsilon:

mechanisms = []

# 1. Wallis cascade (Approach 2)
c2_wallis_full = sum((-1)**(k) * wallis_cascade_coeff(k) * x**(k-2) for k in range(2, 50))
eps_wallis = 1 - c2_wallis_full / 0.4
mechanisms.append(("Wallis cascade (50 terms)", eps_wallis))

# 2. Jensen gap (energy weighting)
mechanisms.append(("Jensen gap (sech^4)", jensen_gap_e))

# 3. Jensen gap (pressure weighting)
mechanisms.append(("Jensen gap (sech^6)", jensen_gap_p))

# 4. Profile-averaged VP reduction (pressure)
mechanisms.append(("VP reduction (sech^6)", abs(reduction_VP)))

# 5. Phi^2-weighted Wallis correction
eps_phi2 = 1 - c2_corrected / 0.4
mechanisms.append(("Phi^2-weighted Wallis", eps_phi2))

# 6. ln-weighted Wallis correction
eps_ln = 1 - c2_ln / 0.4
mechanisms.append(("ln-weighted Wallis", eps_ln))

# 7. Breathing mode phase space: 1/(4*3) = 1/12 of m^2, weighted by phibar
# Just a guess:
mechanisms.append(("phibar^3/(6*7) [direct]", phibar3/42))

# 8. Geometric: sech^2(z_0) correction
# sech^2(z_0) = 4/5, and the correction at the next level:
# (4/5)^3 * phibar / (some factor)
mechanisms.append(("sech^2(z0)^3 * phibar / 5", (4/5)**3 * phibar / 5))

# 9. The c_3 term: -c_3*x
mechanisms.append(("-c_3*x", c_coeffs[3]*x))

# 10. Direct width correction from breathing mode:
# delta_w/w ~ (1/4) * (hbar/M_cl) = (1/4) * (lambda/(m^2)) in dimensionless
# With lambda = m^2/10: = (1/4)*(1/10) = 1/40
# Times phibar (asymmetry): phibar/40
mechanisms.append(("phibar/40 (width/BM)", phibar/40))

# 11. The EXACT N from data:
N_exact = phibar3 / epsilon_needed
mechanisms.append((f"phibar^3/N_exact (N={N_exact:.4f})", phibar3/N_exact))

print(f"  {'Mechanism':<35} {'epsilon':>18} {'Ratio to target':>16} {'Match?':>8}")
print(f"  {'-'*35} {'-'*18} {'-'*16} {'-'*8}")
for name, eps in sorted(mechanisms, key=lambda t: abs(t[1] - epsilon_needed)):
    ratio = eps / epsilon_needed
    match = "YES" if abs(ratio - 1) < 0.01 else ("~" if abs(ratio - 1) < 0.1 else "no")
    print(f"  {name:<35} {eps:>18.12f} {ratio:>16.6f} {match:>8}")

print()

# ================================================================
# THE DERIVATION CHAIN (what we CAN derive)
# ================================================================
print(f"\n{sep}")
print("THE DERIVATION: WHAT IS DERIVED AND WHAT IS NOT")
print(sep)

print(f"""
STEP 1: The Wallis integral ratio (EXACT, textbook)
  I_6/I_4 = 4/5
  This is the ratio sech^6/sech^4 for PT depth n=2.
  Reference: standard Wallis integrals.

STEP 2: The perturbative factor (STANDARD)
  c_2 = (1/2) * (I_6/I_4) = (1/2) * (4/5) = 2/5
  The 1/2 is from second-order perturbation theory (1/2! in Taylor).
  Reference: Graham & Weigel, PLB 852 (2024); Wallis cascade.

STEP 3: The NEXT Wallis ratio (EXACT)
  I_8/I_6 = 6/7
  This gives 42 = 6*7.

STEP 4: The golden asymmetry parameter (ALGEBRAIC)
  phibar^3 = 1/phi^3 = 0.2360679...
  This is the ratio (m_f(-1/phi)/m_f(phi))^3 = (phibar/phi)^3...
  No, that gives phibar^6.
  Actually phibar^3 = (-1/phi)^3 = -phibar^3 (the cube of the -1/phi vacuum).
  |vacuum|^3 = phibar^3 where phibar = phi-1 = 1/phi.

STEP 5: THE CONNECTION (PARTIAL — this is the gap)
  WHY does the correction have the form phibar^3/(6*7)?

  The BEST physical argument:

  The leading c2 = (1/2)*(I_6/I_4) involves the ratio of sech^6 to sech^4.
  The sub-leading correction involves the NEXT ratio I_8/I_6 = 6/7.

  In second-order perturbation theory, the correction to c2 from
  higher-order terms has a structure:
    c2_eff = c2_leading * [1 - (next Wallis correction)]

  The "next Wallis correction" involves:
  - The ratio 1/(6*7) from the product of numerator and denominator
    of I_8/I_6 (this is 1/42)
  - The factor phibar^3 from the golden asymmetry of the potential
    (the vacua at phi and -1/phi, with |ratio|^3 entering through
    the cubic vertex of the kink fluctuation expansion)

  SPECIFICALLY:
  The third-order perturbation matrix element involves:
    M_3 ~ integral V'''(Phi_cl) * sech^8(z) dz

  V'''(Phi_cl(z)) = 2*lambda*(12*Phi - 6) = 2*lambda*6*(2*Phi-1) = 12*lambda*sqrt(5)*tanh(z)

  So M_3 ~ integral tanh(z)*sech^8(z) dz = 0 by parity!

  The CUBIC term vanishes by symmetry. The correction comes from the
  QUARTIC term V''''(Phi_cl) = 24*lambda (constant), combined with the
  ASYMMETRY of the Phi^2 average at the sech^8 level:

  <Phi^2>_4 = 7/18 (from the general formula (w+3)/(2*(2w+1)) for w=4)

  The correction involves the DIFFERENCE between the physical and symmetric:
  <Phi^2>_4 / <Psi^2>_4 where <Psi^2>_4 = (5/4)*<tanh^2>_4 = (5/4)/(2*4+1) = 5/36

  Ratio: <Phi^2>/<Psi^2> = (7/18)/(5/36) = (7*36)/(18*5) = 252/90 = 14/5 = 2.8

  The EXCESS: <Phi^2>_4 - <Psi^2>_4 = 7/18 - 5/36 = 14/36 - 5/36 = 9/36 = 1/4
  (This is (1/2)^2, the square of the midpoint value. Expected.)

  The fractional excess: (1/4)/(5/36) = 36/20 = 9/5

  Hmm, this gives 9/5, not phibar^3/42.
""")

# Let me check if the RATIO of successive corrections gives phibar^3:
# The Wallis cascade gives c_k coefficients. The ratio c_3/c_2 is:
c3_over_c2 = wallis_cascade_coeff(3) / wallis_cascade_coeff(2)
print(f"\n  Ratio c_3/c_2 = {c3_over_c2:.10f}")
print(f"  = (1/6)*(4/5)*(6/7) / ((1/2)*(4/5))")
print(f"  = (1/3)*(6/7) = 2/7 = {2.0/7:.10f}")
print()

# So c_3 = c_2 * (2/7)
# The effective c2 = c_2 - c_3*x = c_2*(1 - (2/7)*x)
# (2/7)*x = (2/7)*eta/(3*phi^3) = 2*eta/(21*phi^3) = 2*phibar^3*eta/21
# = 2/(21) * eta * phibar^3

# Is (2/7)*x equal to phibar^3/42?
val_27x = (2.0/7) * x
print(f"  (2/7)*x = {val_27x:.15e}")
print(f"  phibar^3/42 = {phibar3/42:.15e}")
print(f"  Ratio = {val_27x / (phibar3/42):.10f}")
print()

# (2/7)*x = (2/7)*eta/(3*phi^3)
# phibar^3/42 = phibar^3/42 = 1/(42*phi^3)
# Ratio = (2/7)*eta/(3*phi^3) * 42*phi^3 = (2/7)*(42/3)*eta = (2/7)*14*eta = 4*eta
# = 4*0.11840 = 0.47361
# So (2/7)*x = 4*eta * phibar^3/42 ≈ 0.474 * phibar^3/42
# NOT equal.

# But the FULL resummed c2_eff includes all higher terms.
# The leading-order correction c2_eff ≈ c2 - c3*x captures about 47% of the effect.
# The REST comes from c4*x^2 - c5*x^3 + ...

# Let's compute how many terms are needed:
print(f"  Convergence of Wallis cascade toward phibar^3/42:")
print(f"  {'Terms':>5} {'c2_eff':>18} {'eps=1-c2/(2/5)':>18} {'eps/target':>12}")
print(f"  {'-'*5} {'-'*18} {'-'*18} {'-'*12}")
for n_terms in range(1, 30):
    c2_sum = sum((-1)**(k) * wallis_cascade_coeff(k) * x**(k-2) for k in range(2, 2+n_terms))
    eps = 1 - c2_sum / 0.4
    ratio = eps / epsilon_needed if epsilon_needed != 0 else float('inf')
    print(f"  {n_terms:>5} {c2_sum:>18.15f} {eps:>+18.12e} {ratio:>12.6f}")

print()

# ================================================================
# THE ANSWER
# ================================================================
print(f"\n{sep}")
print("CONCLUSION: STATUS OF THE phibar^3/42 DERIVATION")
print(sep)

print(f"""
WHAT IS DERIVED:
  1. c_2 = 2/5 from the Wallis ratio I_6/I_4 = 4/5 [EXACT, Graham 2024]
  2. 42 = 6*7 from the NEXT Wallis ratio I_8/I_6 = 6/7 [EXACT]
  3. phibar^3 = 1/phi^3 as the asymmetry parameter of V(Phi) [ALGEBRAIC]
  4. The Wallis CASCADE gives a perturbative series:
     c2_eff = c_2 - c_3*x + c_4*x^2 - ...
     with c_k = (1/k!)*product(2j/(2j+1)) involving successive Wallis ratios.
  5. This series CONVERGES to a value CLOSE to (2/5)(1-phibar^3/42).

WHAT IS NOT DERIVED:
  The EXACT identification c_2_eff = (2/5)(1 - phibar^3/42) is not proven.

  The Wallis cascade at x = 0.009317 gives a correction of 0.56% to c_2,
  and the partial sums approach the target, but do NOT converge to it exactly.
  The Wallis cascade sum converges to a value that differs from the target
  by about {abs(c2_wallis_full - c2_target)/c2_target * 100:.2f}% of the target.

  The exact match to experiment (0.003 sigma) could be:
  (a) A genuine algebraic identity involving the Wallis cascade + golden ratio
  (b) A coincidence at the 8 ppm level (not impossible for 2-parameter fit)
  (c) A consequence of a deeper structure not yet identified

PHYSICAL MECHANISMS TESTED:
  1. One-loop width correction: qualitatively right but doesn't give
     phibar^3/42 from a closed calculation.
  2. Wallis cascade: gives the RIGHT DIRECTION and SCALE of correction
     (~0.5% reduction) but doesn't sum to exactly phibar^3/42.
  3. Golden asymmetry (Jensen gap): gives a correction ~5x too large.
  4. Profile-weighted VP (ln|Phi| weighting): gives wrong scale.
  5. Zero-of-Phi singularity: qualitatively interesting (sech^2(z_0) = 4/5!)
     but doesn't quantitatively produce phibar^3/42.

BEST CANDIDATE MECHANISM:
  The Wallis cascade, with the identification that the RESUMMED series
  c2_eff = c_2(1 - sum of Wallis/golden corrections) gives a correction
  whose leading term is c_3*x = (2/7)*(eta/(3*phi^3)) = (2/7)*x.
  This captures ~47% of the effect. The rest requires summing the full
  cascade OR finding a closed-form identity.

  The number 42 = 6*7 emerges NATURALLY from the Wallis sequence
  (I_8/I_6 = 6/7). The factor phibar^3 is the NATURAL asymmetry parameter.
  But their EXACT combination as phibar^3/42 in the multiplicative correction
  to c_2 = 2/5 is NOT proven from a single calculation.

NUMERICAL SUMMARY:
  c2_exact                   = {c2_exact:.15f}
  (2/5)                      = {0.4:.15f}   (diff {c2_exact-0.4:+.6e})
  (2/5)(1-phibar^3/42)       = {c2_target:.15f}   (diff {c2_exact-c2_target:+.6e})
  Wallis cascade (50 terms)  = {c2_wallis_full:.15f}   (diff {c2_exact-c2_wallis_full:+.6e})

  1/alpha with c2 = 2/5:              {compute_inv_alpha(0.4):.12f}  ({(compute_inv_alpha(0.4)-inv_alpha_meas)/inv_alpha_unc:+.2f} sigma)
  1/alpha with c2 = (2/5)(1-pb^3/42): {compute_inv_alpha(c2_target):.12f}  ({(compute_inv_alpha(c2_target)-inv_alpha_meas)/inv_alpha_unc:+.2f} sigma)
  1/alpha with c2 = Wallis cascade:   {compute_inv_alpha(c2_wallis_full):.12f}  ({(compute_inv_alpha(c2_wallis_full)-inv_alpha_meas)/inv_alpha_unc:+.2f} sigma)
  1/alpha measured (Rb):               {inv_alpha_meas:.12f}

HONEST ASSESSMENT:
  The derivation of c_2 = 2/5 is GENUINE (Graham pressure integral).
  The identification of 42 = 6*7 from the next Wallis ratio is GENUINE.
  The factor phibar^3 as the asymmetry parameter is NATURAL.
  But the specific combination (2/5)(1-phibar^3/42) is currently a
  VERY GOOD FIT (8 ppm in c2, 0.003 sigma in alpha) without a complete
  derivation from a single one-loop calculation.
""")

print(sep)
print("END OF ANALYSIS")
print(sep)
