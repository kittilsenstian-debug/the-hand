#!/usr/bin/env python3
"""
eta_nonperturbative.py — WHY does alpha_s = eta(1/phi) in N=0?

The Dedekind eta function eta(q) = q^(1/24) * prod_{n=1}^inf (1-q^n) is
fundamentally a NON-PERTURBATIVE object (infinite product over all modes).
The strong coupling alpha_s is also fundamentally non-perturbative (the
coupling at the QCD scale where perturbation theory breaks down).

This script investigates 7 specific angles connecting these two facts:

  (a) Kink partition function / functional determinant
  (b) Spectral zeta function of the Poschl-Teller spectrum
  (c) Witten index and eta
  (d) Bosonic string connection (Z = 1/eta^24)
  (e) Resurgence: trans-series parameter sigma = 1/phi?
  (f) QCD vacuum energy and gluon condensate
  (g) Chern-Simons partition function

The central question: in what precise sense is the strong coupling
"counting" something that the infinite product eta also counts?

Usage:
    python theory-tools/eta_nonperturbative.py
"""

import math
import sys

if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# =================================================================
# SETUP: Constants and modular form computations
# =================================================================

phi = (1 + math.sqrt(5)) / 2
phibar = 1 / phi
sqrt5 = math.sqrt(5)
q = phibar  # the golden nome
NTERMS = 500

# Modular forms at q = 1/phi
def eta_func(q, N=NTERMS):
    prod = 1.0
    for n in range(1, N+1):
        prod *= (1 - q**n)
    return q**(1.0/24) * prod

def eta_product_only(q, N=NTERMS):
    """Just the infinite product part, without q^(1/24)."""
    prod = 1.0
    for n in range(1, N+1):
        prod *= (1 - q**n)
    return prod

def theta3(q, N=NTERMS):
    s = 0.0
    for n in range(1, N+1):
        s += q**(n**2)
    return 1 + 2*s

def theta4(q, N=NTERMS):
    s = 0.0
    for n in range(1, N+1):
        s += (-1)**n * q**(n**2)
    return 1 + 2*s

def sigma_k(n, k):
    return sum(d**k for d in range(1, n+1) if n % d == 0)

def E4_func(q, N=200):
    return 1 + 240*sum(sigma_k(n,3)*q**n for n in range(1, N+1))

# Precompute
eta_val = eta_func(q)
prod_val = eta_product_only(q)
q_24th = q**(1.0/24)
t3 = theta3(q)
t4 = theta4(q)
e4 = E4_func(q)
tau_im = math.log(phi) / (2 * math.pi)
alpha_sw = 1.0 / (2 * tau_im)

# Physical constants
alpha_s_measured = 0.1179   # PDG
mu_pe = 1836.15267          # proton-to-electron mass ratio
lam = 1.0 / (3 * phi**2)   # Higgs quartic = 1/(3*phi^2) in framework

# Kink mass parameters
m_scalar = math.sqrt(10 * lam)  # mass around each vacuum
Delta_phi = sqrt5               # field distance between vacua

# Exact kink action: S_kink = sqrt(2*lam) * 5*sqrt(5)/6
S_kink = math.sqrt(2 * lam) * 5 * sqrt5 / 6

print('='*80)
print('  WHY alpha_s = eta(1/phi) IN N=0 PHYSICS?')
print('  Seven Non-Perturbative Angles')
print('='*80)
print()
print(f'  eta(1/phi) = {eta_val:.10f}')
print(f'  alpha_s    = {alpha_s_measured}')
print(f'  Match: {(1 - abs(eta_val - alpha_s_measured)/alpha_s_measured)*100:.2f}%')
print()
print(f'  Decomposition: eta = q^(1/24) * prod(1-q^n)')
print(f'    q^(1/24)        = {q_24th:.10f}')
print(f'    prod(1-q^n)     = {prod_val:.10f}')
print(f'    Product: {q_24th:.6f} * {prod_val:.6f} = {eta_val:.6f}')
print()

# =================================================================
# ANGLE (a): KINK PARTITION FUNCTION AND FUNCTIONAL DETERMINANT
# =================================================================

print('='*80)
print('ANGLE (a): KINK PARTITION FUNCTION / FUNCTIONAL DETERMINANT')
print('='*80)
print()

# The semiclassical partition function around a kink is:
#   Z_kink = (det'[-d^2/dx^2 + V''(Phi_kink)])^(-1/2) * exp(-S_kink)
# where det' means the zero-mode is removed.
#
# For the Poschl-Teller potential with n=2:
#   V''(Phi_kink) - m^2 = -n(n+1) * m^2/4 / cosh^2(m*x/2)
#   with n(n+1) = 6, so n = 2
#
# The RATIO of determinants det'(-d^2 + V''_kink) / det(-d^2 + m^2)
# is known EXACTLY for Poschl-Teller potentials (Dunne-Feinberg 1998,
# Forman 1987, McKane-Tarlie 1995):
#
# For PT with n bound states (including zero mode):
#   det'(-d^2 + V_PT) / det(-d^2 + m^2) = prod_{k=1}^{n} (k/n)^2
#
# WAIT: this is the functional determinant on a LINE (infinite extent).
# The result depends on boundary conditions. For infinite line:
#
# The functional determinant ratio for PT-n on R is:
#   det' / det_0 = n! * n! / (2n)!  (for n=2: 2!*2!/4! = 4/24 = 1/6)
# This is the Jost function / reflection coefficient.
#
# Actually, let me be more precise. For the modified PT potential
#   U(x) = -s(s+1)/cosh^2(x) with s = 2
# on the full real line, the ratio of functional determinants
# (zero mode excluded) is related to the Jost function.
#
# For s = 2 (n = 2 in our notation), the scattering matrix gives:
#   |S(k)|^2 = [(k^2 + 1)(k^2 + 4)] / [(k^2 + 1)(k^2 + 4)] = 1
#   (reflectionless potential!)
#
# The functional determinant ratio for a REFLECTIONLESS potential is:
#   det'/det_0 = prod_{j=1}^{n} (kappa_j)^2 / prod_{j<k} (kappa_j^2 - kappa_k^2)^2
#   where kappa_j^2 are the bound-state "eigenvalues" (decay constants).
#
# For PT n=2: kappa_1 = 1 (breathing mode), kappa_2 = 2 (zero mode,
# removed). So det'/det_0 depends on kappa_1 = 1 only.
#
# The standard result for the 1-kink contribution to the free energy
# of a scalar field with a double-well potential is:
#
#   Z_kink / Z_0 = L * m * sqrt(S_kink / (2*pi)) * exp(-S_kink)
#                  * (det'/det_0)^(-1/2) * (1 + O(lambda))
#
# where L is the spatial extent, m is the mass, and det'/det_0 is
# the ratio with zero mode removed.

# For our potential V(Phi) = lambda*(Phi^2 - Phi - 1)^2:
print(f'  Kink action S_kink = sqrt(2*lam) * 5*sqrt(5)/6 = {S_kink:.8f}')
print(f'  exp(-S_kink) = {math.exp(-S_kink):.8f}')
print(f'  Compare phibar = {phibar:.8f}')
print()

# The KEY question: does det'/det_0 for PT n=2 involve eta?
#
# The functional determinant of -d^2/dx^2 + m^2 - V_0/cosh^2(ax) on [0, L]
# with periodic boundary conditions involves theta functions!
# Specifically, on a circle of circumference beta (thermal partition function):
#
#   Z(beta) = Tr exp(-beta*H) = sum_n exp(-beta*E_n)
#
# For the free massive boson (no potential):
#   Z_free(beta) = prod_{n} (1/(2*sinh(beta*omega_n/2)))
#   where omega_n = sqrt(m^2 + (2*pi*n/L)^2)
#
# In the limit L -> infinity, the partition function per unit length is:
#   z_free = exp(-beta*m / (4*pi*beta))  (roughly)
#
# For the PT potential on a circle, the exact partition function involves
# the Selberg zeta function, which is related to eta for constant
# negative curvature spaces.

# Let me compute something more concrete.
# The spectral zeta function of the PT Hamiltonian:

# For the free massive boson on R (per unit length):
# The "partition function" involves eta only when we compactify.

# KEY COMPUTATION: What is the ratio of functional determinants
# for PT n=2 vs free massive boson, on a circle of circumference L?
#
# On a circle of circumference L with mass m:
#   det(-d^2 + m^2) = prod_n (m^2 + (2*pi*n/L)^2)
#   = m * L * prod_{n=1}^inf [(2*pi*n/L)^2 + m^2] / (2*pi*n/L)^2
#   * prod_{n=1}^inf (2*pi*n/L)^2
#   Using the known identity for sinh:
#   = 2*sinh(m*L/2)
#   (after zeta-function regularization)
#
# For the PT potential on a circle:
# The eigenvalues shift, and the functional determinant changes.
# In the limit L -> infinity, the bound states and continuum separate.
#
# The CONTINUUM contribution to the ratio is:
#   det'_cont / det_cont^free = prod_k (k^2 + 1)(k^2 + 4) / (k^2)(k^2 + 4)...
#   This is NOT related to eta in any obvious way.

print('  ASSESSMENT: The kink partition function on a LINE (R^1) gives')
print('  rational/algebraic functional determinant ratios, not eta.')
print('  On a CIRCLE (thermal), it gives sinh-type functions.')
print('  Neither naturally produces the eta function.')
print()
print('  However, on a TORUS (2D compactification), the partition function')
print('  of the kink sector DOES involve eta -- this is the instanton')
print('  contribution to the 2D partition function.')
print()

# Can we get eta from compactifying the kink on a circle?
# If the kink lives on a circle of circumference beta = 2*pi*Im(tau),
# then the kink-antikink gas partition function is:
#   Z_KAK = sum_{N=0}^inf (z_1 * L)^(2N) / (2N)! * exp(-2N*S_kink)
#   = cosh(z_1 * L * exp(-S_kink))
# where z_1 is the single-kink fugacity.
#
# This gives a SHIFT in the ground-state energy but not eta.
# So angle (a) is not promising for a DIRECT eta connection.

print('  VERDICT: The kink functional determinant does NOT directly')
print('  produce eta. The connection, if any, requires going to 2D')
print('  (torus) where the theory becomes a 2D CFT whose partition')
print('  function naturally involves eta.')
print()


# =================================================================
# ANGLE (b): SPECTRAL ZETA FUNCTION OF THE PT SPECTRUM
# =================================================================

print('='*80)
print('ANGLE (b): SPECTRAL ZETA FUNCTION OF PT SPECTRUM')
print('='*80)
print()

# The PT n=2 spectrum:
#   E_0 = 0 (zero mode, excluded)
#   E_1 = 3*m^2/4 (breathing mode)
#   Continuum: E_k = m^2 + k^2 for k > 0
#
# The spectral zeta function (with zero mode removed) is:
#   zeta_PT(s) = (3*m^2/4)^(-s) + integral_0^inf rho(E) * E^(-s) dE
# where rho(E) is the density of states in the continuum.
#
# For the PT potential, the density of states (phase shift) is known:
#   delta(k) = sum_{j=1}^{n} arctan(k/j) - n*k*pi/L (for large L)
#   delta(k) = arctan(k) + arctan(k/2)  (for n=2)
#
# The spectral zeta function is related to eta via the Mellin transform:
#   eta(s) = sum_{n=1}^inf (-1)^(n+1) / n^s  (Dirichlet eta function)
# This is a DIFFERENT eta from Dedekind! The Dirichlet eta is
#   eta_D(s) = (1 - 2^(1-s)) * zeta(s)
#
# The Dedekind eta is related to the PARTITION FUNCTION (q-series),
# not to the spectral zeta function directly.

# The connection between spectral zeta and Dedekind eta goes through:
#   For a free boson on a torus with modular parameter tau:
#   zeta_spec(s) = sum_{m,n} (|m + n*tau|^2 / Im(tau))^(-s)
#   This is the Epstein zeta function, and it's related to E_s(tau)
#   (the non-holomorphic Eisenstein series), not to eta.
#
# BUT: the DETERMINANT of the Laplacian on a torus IS given by eta:
#   det'(-Delta) = (2*pi)^2 * Im(tau) * |eta(tau)|^4
# This is the famous Kronecker first limit formula / Ray-Singer analytic torsion.

print('  The Laplacian determinant on a flat torus with parameter tau:')
print('    det\'(-Delta) = (2*pi)^2 * Im(tau) * |eta(tau)|^4')
print()
print(f'  At tau = i*ln(phi)/(2*pi), i.e., q = 1/phi:')
print(f'    Im(tau) = {tau_im:.8f}')
print(f'    |eta|^4 = {eta_val**4:.8e}')
det_torus = (2*math.pi)**2 * tau_im * eta_val**4
print(f'    det\'(-Delta) = (2*pi)^2 * {tau_im:.6f} * {eta_val**4:.6e}')
print(f'                  = {det_torus:.8e}')
print()

# What if the coupling IS related to this determinant?
# alpha_s = eta means eta^2 = eta^2.
# det' = (2*pi)^2 * tau * eta^4 = (2*pi)^2 * tau * alpha_s^4  (if alpha_s = eta)
# So: alpha_s = (det' / ((2*pi)^2 * tau))^(1/4)
#     alpha_s = (2*pi)^(-1/2) * tau^(-1/4) * (det')^(1/4)

alpha_s_from_det = (det_torus / ((2*math.pi)**2 * tau_im))**(0.25)
print(f'  alpha_s = (det\' / ((2*pi)^2*tau))^(1/4) = {alpha_s_from_det:.8f}')
print(f'  This is just eta by construction -- tautological.')
print()

# The REAL question: is the PT spectrum on a torus related to eta
# in a non-trivial way?
#
# For the PT Hamiltonian on a torus, the determinant is NOT simply
# (2*pi)^2 * tau * eta^4, because the potential breaks translation
# invariance. The determinant would be:
#   det'(-d^2/dx^2 + V''(Phi_kink)) on a torus
# This is NOT a known closed form in terms of eta.

print('  VERDICT: The spectral zeta function of the PT Hamiltonian')
print('  on a LINE does not involve eta. On a TORUS, the free boson')
print('  determinant gives eta^4, but the PT potential breaks the')
print('  connection. This angle suggests that eta appears when the')
print('  kink physics is embedded in a 2D torus geometry.')
print()


# =================================================================
# ANGLE (c): WITTEN INDEX AND eta
# =================================================================

print('='*80)
print('ANGLE (c): WITTEN INDEX AND eta')
print('='*80)
print()

# The Witten index for N=1 SUSY QM is:
#   Tr(-1)^F = n_B(E=0) - n_F(E=0)
# counting the difference between bosonic and fermionic zero modes.
#
# For the PT potential with superpotential W(x):
#   H_boson    = -d^2/dx^2 + W'^2 - W''
#   H_fermion  = -d^2/dx^2 + W'^2 + W''
# The Witten index = number of bound states of H_B at E=0 minus
# number of bound states of H_F at E=0.
#
# For N=2 SUSY in 2D (1+1D), the partition function on a torus involves:
#   Z(tau) = Tr(-1)^F * q^{L_0 - c/24} * qbar^{Lbar_0 - c/24}
#          = |eta(tau)/theta_i(tau)|^2  (for various boundary conditions)
#
# For a 2D theory with target space S^1 (c=1):
#   Z_NS = |theta_3(tau)/eta(tau)|^2   (NS sector)
#   Z_R  = |theta_4(tau)/eta(tau)|^2   (R sector)
#   Witten index = Z_R(tau -> 0) = |theta_2(tau)/eta(tau)|^2  (twisted)
#
# For our golden potential, we don't have SUSY.
# But we can define a "quasi-Witten index" using the N=0 kink spectrum.

# For a NONSUPERSYMMETRIC 2D theory, the partition function is:
#   Z = Tr exp(-beta*H) = sum_n exp(-beta*E_n)
# This involves eta only through the free-field contribution.

# The key formula connecting eta to the Witten index of a FREE fermion:
#   Tr(-1)^F q^{H} = prod_{n=1}^inf (1-q^n)  (for one real fermion)
#   = eta(q) / q^(1/24)

# So: prod(1-q^n) = eta/q^(1/24) IS the Witten index of one free fermion!
# At q = 1/phi:

witten_fermion = prod_val  # = prod(1-q^n) = eta/q^(1/24)
print(f'  Witten index of 1 free fermion: prod(1-q^n) = {witten_fermion:.8f}')
print(f'  eta(1/phi)                                  = {eta_val:.8f}')
print(f'  q^(1/24)                                    = {q_24th:.8f}')
print(f'  eta / q^(1/24) = {eta_val/q_24th:.8f} (= prod, check: {abs(witten_fermion - eta_val/q_24th) < 1e-10})')
print()

# Now: alpha_s = eta = q^(1/24) * prod(1-q^n)
#                    = q^(1/24) * Tr_fermion[(-1)^F q^H]
# The coupling IS the vacuum energy factor times the fermionic index!

# For D free fermions:
#   prod(1-q^n)^D
# So eta^D = q^(D/24) * prod(1-q^n)^D

# For the BOSONIC STRING in D dimensions:
#   Z_bos = 1/eta(q)^D  (D transverse dimensions)
# The physical bosonic string has D = 24.
#   Z_bos = 1/eta^24 = 1/Delta(q)  (the modular discriminant!)

# For our purposes: alpha_s = eta^1 corresponds to D = 1.
# One dimension! This is the kink direction itself!

print('  KEY OBSERVATION:')
print('  alpha_s = eta = q^(1/24) * [Witten index of 1 free fermion]')
print()
print('  The "1" in eta^1 corresponds to ONE dimension.')
print('  This is naturally the kink direction (the 1D domain wall).')
print('  The coupling constant is the 1D partition function density!')
print()
print('  Compare: bosonic string in D=24: Z = 1/eta^24.')
print('  Here: alpha_s = eta^1 = 1/(1/eta) = 1/Z_{1D-boson}.')
print('  The coupling is the INVERSE of a 1D bosonic partition function.')
print()

# But this is suggestive rather than rigorous.
# Let me check: is alpha_s = 1/Z for Z = some specific partition function?

Z_1d_boson = 1.0 / prod_val  # = 1/prod(1-q^n) = partition function
print(f'  Z_{{1D boson}} = 1/prod(1-q^n) = {Z_1d_boson:.6f}')
print(f'  = sum p(k) * q^k = {Z_1d_boson:.6f}  (q-expansion of partitions)')
print(f'  alpha_s = q^(1/24) / Z = {q_24th / Z_1d_boson:.6f} vs {eta_val:.6f}')
print(f'  ... which is just eta by definition. Tautological again.')
print()

# The NON-tautological question: WHY should the QCD coupling at M_Z
# equal the partition function density of one dimension's worth of
# bosonic/fermionic oscillators at temperature T = 1/(2*pi*Im(tau))?

# Check the "temperature":
T_eff = 1.0 / (2 * math.pi * tau_im)  # = 1/(ln(phi)) = 2.078
print(f'  Effective "temperature": T = 1/(2*pi*Im(tau)) = {T_eff:.6f}')
print(f'  = 1/ln(phi) = {1/math.log(phi):.6f}')
print(f'  = pi/ln(phi) / pi = alpha_SW / pi = {alpha_sw/math.pi:.6f}')
print()

# Hmm. T = 1/ln(phi) is interesting but doesn't immediately connect to QCD.

print('  VERDICT: The Witten index interpretation is the MOST')
print('  illuminating so far. alpha_s = eta = q^(c/24) * [fermionic')
print('  partition function in 1D] naturally associates the coupling')
print('  with the domain wall direction. But the argument is formal:')
print('  it doesn\'t explain WHY the QCD coupling should equal this')
print('  1D partition function density. Needs a mechanism.')
print()


# =================================================================
# ANGLE (d): BOSONIC STRING CONNECTION (Z = 1/eta^24)
# =================================================================

print('='*80)
print('ANGLE (d): BOSONIC STRING AND E8 LATTICE')
print('='*80)
print()

# The bosonic string partition function:
#   Z_bos(tau) = 1/|eta(tau)|^{2*24} * (volume factor)
# The 24 comes from 26 - 2 = 24 transverse dimensions.
#
# For a heterotic string with E8 x E8 gauge group:
#   Z_het = Theta_{E8}(tau) * Theta_{E8}(tau) / eta(tau)^{16}
#   (16 = left-moving + right-moving internal dimensions)
#   where Theta_{E8} = E4 is the E8 lattice theta function.
#
# In the heterotic string, the GAUGE COUPLING is:
#   1/g^2 = Re(S) where S is the dilaton modulus
# The tree-level coupling is NOT given by eta.
#
# BUT: at one loop, threshold corrections ARE given by:
#   Delta_a = -b_a * ln(|eta(T)|^4 * Im(T)) + (model-dependent)
#   (Dixon-Kaplunovsky-Louis 1991)
# where T is the Kahler modulus.
#
# The DKL formula gives corrections involving ln(eta), not eta directly!
# So: 1/alpha_a = 1/alpha_GUT + b_a/(2*pi) * ln(M_GUT/M_Z) + Delta_a
# Delta_a involves ln(|eta|^4 * Im(T)), which is LOGARITHMIC in eta.
#
# This is the standard objection: string theory gives ln(eta) in
# coupling corrections, not eta itself.

print('  Standard DKL threshold correction:')
DKL_val = math.log(eta_val**4 * tau_im)
print(f'    Delta_a = -b_a * ln(|eta|^4 * Im(T))')
print(f'    ln(|eta|^4 * Im(T)) = ln({eta_val**4:.6e} * {tau_im:.6f})')
print(f'                        = {DKL_val:.6f}')
print()

# What if the coupling is NOT 1/alpha = 1/alpha_GUT + Delta (additive)
# but rather alpha = alpha_GUT * eta^p (multiplicative)?
#
# In a theory where the coupling is an ETA FUNCTION itself (not its log),
# the natural origin would be the PARTITION FUNCTION of the internal
# theory, not a threshold correction.

# For the E8 lattice theory (not string, just lattice):
# Theta_{E8}(q) = E4(q) = 1 + 240*q + 2160*q^2 + ...
# This is the theta function = partition function of the E8 lattice.
# It counts vectors in the E8 lattice by norm:
#   a_n = number of E8 vectors with |v|^2 = 2n

print('  E8 lattice theta function at q = 1/phi:')
print(f'    Theta_E8 = E4(1/phi) = {e4:.4f}')
print(f'    eta^24 = Delta = {eta_val**24:.6e}')
print(f'    j = E4^3/eta^24 = {e4**3/eta_val**24:.4e}')
print()

# For the E8 theory: the relevant partition function is
#   Z_E8 = Theta_{E8} / eta^8
# (8 = rank of E8, each contributing one eta factor)
Z_E8 = e4 / eta_val**8
print(f'    Z_E8 = Theta_E8 / eta^8 = {e4:.4f} / {eta_val**8:.6e} = {Z_E8:.4e}')
print()

# What if alpha_s is related to eta^8/E4?
# alpha_s = eta^8/E4 would give:
ratio_test = eta_val**8 / e4
print(f'    eta^8 / E4 = {ratio_test:.6e}')
print(f'    Very small, not alpha_s.')
print()

# What about per-dimension decomposition?
# The E8 lattice has 8 dimensions. If the coupling comes from
# "one dimension's worth" of the E8 partition function:
# alpha_s ~ (eta^8/E4)^(1/8) * eta ???
# This is getting speculative.

# More concrete: the ONE-LOOP vacuum energy per dimension for
# a bosonic string is proportional to -ln(|eta|^2 * Im(tau)).
# The coupling shift per dimension: Delta ~ -ln(eta) ~ 2.1.
# Not useful numerically.

# However, there IS a natural way eta appears without logarithms:
# The SUSY index of the heterotic string:
#   Z_het = Theta_{E8}^2 / eta^{24}
# At q = 1/phi:
Z_het = e4**2 / eta_val**24
print(f'    Z_het = Theta_E8^2 / eta^24 = {Z_het:.4e}')
print()

# And Theta_E8/eta^8 per copy:
Z_per_E8 = e4 / eta_val**8
print(f'    Per E8 copy: Theta_E8/eta^8 = {Z_per_E8:.4e}')
print()

# Under E8 -> 4A2:
# Theta_{E8} = sum over 9 coset classes of Theta_{A2}^4
# At q = 1/phi: E4/Theta_A2^4 = 9 (each coset contributes equally)
# So: Theta_{A2}^4 = E4/9
Theta_A2_4 = e4 / 9
Theta_A2 = Theta_A2_4**0.25
print(f'    Under E8 -> 4A2: Theta_A2 = (E4/9)^(1/4) = {Theta_A2:.4f}')
print(f'    Theta_A2 / eta^2 = {Theta_A2 / eta_val**2:.4f}')
print(f'    (One A2 partition function, 2 = rank of A2)')
print()

# Can the coupling of one SU(3) be Theta_A2/eta^2?
# Theta_A2/eta^2 = 40.55... That's huge.
# What about eta^2/Theta_A2?
ratio_A2 = eta_val**2 / Theta_A2
print(f'    eta^2 / Theta_A2 = {ratio_A2:.6f}')
print(f'    Compare alpha_em = {1/137.036:.6f}')
print(f'    Hmm, not matching either.')
print()

print('  VERDICT: The bosonic string and E8 lattice naturally produce')
print('  eta through partition functions. The DKL formula gives ln(eta)')
print('  in threshold corrections (not eta itself). The E8/4A2')
print('  decomposition gives specific partition function ratios, but')
print('  none simply equal alpha_s = 0.1184. The "per-dimension"')
print('  interpretation (alpha_s = eta^1 = one dimension of oscillators)')
print('  remains the most suggestive connection.')
print()


# =================================================================
# ANGLE (e): RESURGENCE — IS sigma = 1/phi?
# =================================================================

print('='*80)
print('ANGLE (e): RESURGENCE AND TRANS-SERIES')
print('='*80)
print()

# In resurgent trans-series, the full non-perturbative answer is:
#   F(g) = sum_k sigma^k * exp(-k*A/g) * sum_n a_{k,n} * g^n
# where A is the instanton action and sigma is the trans-series
# parameter encoding which Stokes sector we're in.
#
# The physical vacuum corresponds to a specific value of sigma
# determined by the Stokes automorphism.
#
# HYPOTHESIS: Could sigma = 1/phi be the physical trans-series parameter?
# If so, the full resurgent series would be:
#   F = sum_k (1/phi)^k * exp(-k*A/g) * perturbative
#   = sum_k phibar^k * instanton_k
# This is a q-series with q = phibar * exp(-A/g)!

# For our potential: A = S_kink (the kink action)
# The effective "nome" of the trans-series would be:
#   q_eff = phibar * exp(-S_kink)

q_eff_1 = phibar * math.exp(-S_kink)
q_eff_2 = phibar * math.exp(-S_kink / lam)  # if g = lambda

print(f'  Kink action S = {S_kink:.6f}')
print(f'  Coupling lambda = {lam:.6f}')
print(f'  S/lambda = {S_kink/lam:.4f}')
print()
print(f'  If sigma = 1/phi:')
print(f'    q_eff = phibar * exp(-S) = {q_eff_1:.6e}')
print(f'    q_eff = phibar * exp(-S/lambda) = {q_eff_2:.10e}')
print(f'    Both are extremely small -- not useful for a q-series.')
print()

# Alternative: what if the trans-series IS the eta product?
# eta(q) = q^(1/24) * prod(1-q^n)
# = q^(1/24) * (1-q)(1-q^2)(1-q^3)...
# Each factor (1-q^n) could be one instanton-anti-instanton sector:
# The n-th mode has action n*A, and (1-q^n) = 1 - exp(-n*A/T)
# where T is the temperature.
#
# If q = exp(-A/T) = 1/phi, then A/T = ln(phi) = 0.4812.
# The instanton action in units of temperature is ln(phi).

A_over_T = math.log(phi)
print(f'  If q = exp(-A/T) = 1/phi, then A/T = ln(phi) = {A_over_T:.6f}')
print()
print(f'  Each factor in eta:')
print(f'    (1 - q^n) = (1 - exp(-n*A/T)) = (1 - phibar^n)')
print()

# Compute the first few factors:
print(f'  n  |  phibar^n   |  1-phibar^n  |  cumulative product')
print(f'  ---|-------------|--------------|--------------------')
cumulative = 1.0
for n in range(1, 16):
    pbn = phibar**n
    factor = 1 - pbn
    cumulative *= factor
    mark = ''
    if n == 1:
        mark = '  <-- (1-phibar) = phibar^2 = phi-conjugate'
    elif n == 2:
        mark = '  <-- (1-phibar^2) = 1-phibar^2 = phi*phibar^2+phibar^2'
    print(f'  {n:2d} | {pbn:11.8f} | {factor:12.8f} | {cumulative:.8f}{mark}')

print()
print(f'  Full product (500 terms) = {prod_val:.10f}')
print(f'  q^(1/24) * product       = {eta_val:.10f} = alpha_s')
print()

# The first factor (1 - phibar) = phibar^2 is DOMINANT.
# In fact: phibar^2 = 1 - phibar = 1 - 1/phi = (phi-1)/phi = phibar
# Wait: 1 - phibar = 1 - 0.618 = 0.382 = phibar^2. Yes.
# So the first factor encodes the fundamental identity phi*phibar = 1,
# or equivalently phi - 1 = 1/phi.

print('  CRITICAL OBSERVATION:')
print(f'  The first factor (1 - q) = (1 - 1/phi) = phibar^2 = {phibar**2:.6f}')
print(f'  This IS the golden ratio self-referential identity:')
print(f'  phi = 1 + 1/phi  =>  1 - 1/phi = phi - 1 - 1 + 1 = 1/phi^2')
print()
print(f'  Each subsequent factor (1-q^n) = 1 - phibar^n captures')
print(f'  the n-th "harmonic" of the self-referential identity.')
print(f'  The PRODUCT over all harmonics gives the "arithmetic"')
print(f'  partition function -- the total non-perturbative content.')
print()

# Connection to resurgence:
# In resurgence, the Borel sum of the perturbative series has
# singularities at t = n*A (multiples of the instanton action).
# The discontinuity at each singularity is the n-instanton contribution.
#
# If A = ln(phi) (so exp(-A) = phibar), then:
# The Borel singularities are at t = n*ln(phi) for n = 1, 2, 3, ...
# The discontinuity at the n-th singularity contributes a factor
# related to (1-phibar^n).
#
# In the simple resurgent structure (like the Airy function):
# The full answer = perturbative * prod(discontinuity_corrections)
# = perturbative * prod(1 - something*phibar^n)
#
# If the "something" is exactly 1 for all n, we get prod(1-phibar^n) = eta/q^(1/24)!
#
# This is the MEDIAN RESUMMATION prescription:
# F_median = F_pert * prod_{n=1}^inf (1 - S_{2n-1} * exp(-n*A/g))
# where S_{2n-1} are the Stokes constants.
#
# If ALL Stokes constants S_{2n-1} = 1 (the "maximally unstable" case),
# and exp(-A/g) = phibar, then:
# F_median = F_pert * prod(1 - phibar^n) = F_pert * eta(phibar)/phibar^(1/24)

print('  RESURGENCE CONNECTION:')
print('  If the instanton action A = ln(phi), and ALL Stokes constants')
print('  equal 1 (maximally non-perturbative), then:')
print('    F_median = F_pert * prod(1-phibar^n) = F_pert * eta(phibar)/phibar^(1/24)')
print(f'    = F_pert * {prod_val:.6f}')
print()
print('  For alpha_s = eta = q^(1/24) * prod(1-q^n):')
print('  The q^(1/24) = phibar^(1/24) factor is the CASIMIR ENERGY')
print('  (vacuum zero-point energy from 1/24 of a free boson).')
print('  The product is the NON-PERTURBATIVE MEDIAN RESUMMATION')
print('  with unit Stokes constants and golden-ratio instanton action.')
print()

print('  VERDICT: This is the most promising angle so far.')
print('  eta appears naturally in resurgence when:')
print('    1. The instanton action is A = ln(phi) (so exp(-A) = 1/phi)')
print('    2. All Stokes constants are 1 (maximally non-perturbative)')
print('    3. The vacuum energy factor is 1/24 (one free boson)')
print('  The question becomes: can we show that the QCD instanton')
print('  action at the golden-ratio domain wall is ln(phi)?')
print()


# =================================================================
# ANGLE (f): QCD VACUUM ENERGY AND GLUON CONDENSATE
# =================================================================

print('='*80)
print('ANGLE (f): QCD VACUUM ENERGY AND GLUON CONDENSATE')
print('='*80)
print()

# The QCD vacuum is characterized by:
#   <(alpha_s/pi) * G_mu_nu^a * G^{a,mu_nu}> = (0.012 +/- 0.006) GeV^4
#                                                (SVZ sum rules)
# This is the gluon condensate. In bag models:
#   B = (bag constant) ~ (0.145 GeV)^4 ~ (145 MeV)^4
# B represents the energy density difference between perturbative
# and non-perturbative QCD vacuum.

B_bag = 0.145**4  # GeV^4
gluon_condensate = 0.012  # GeV^4, central value
Lambda_QCD = 0.217  # GeV (MS-bar, N_f=5)

print(f'  QCD vacuum parameters:')
print(f'    <(alpha_s/pi)*G^2> = {gluon_condensate:.4f} GeV^4')
print(f'    Bag constant B^(1/4) = 0.145 GeV')
print(f'    Lambda_QCD = {Lambda_QCD:.3f} GeV')
print()

# Can B or Lambda_QCD be expressed in terms of eta?
# B ~ Lambda_QCD^4 by dimensional analysis.
# Lambda_QCD / v = 0.217 / 246.22 = 8.82e-4
# Compare: phibar^7 = 0.02129, phibar^8 = 0.01316, phibar^14 = 4.54e-4
# Not matching cleanly.

# More interesting: the RATIO alpha_s * <G^2> / Lambda_QCD^4
ratio_vacuum = gluon_condensate / Lambda_QCD**4
print(f'  <alpha_s*G^2/pi> / Lambda_QCD^4 = {ratio_vacuum:.4f}')
print(f'  = {ratio_vacuum:.4f}')
print()

# What about the vacuum energy density in terms of eta?
# If the QCD vacuum energy per dimension is ~eta, then the total
# 4D vacuum energy would involve eta^4.
# eta^4 = (0.1184)^4 = 1.96e-4
# <alpha_s*G^2/pi> = 0.012 GeV^4
# Ratio: 0.012/1.96e-4 = 61 ~ mu/30 = 61.2 !!!

ratio_g2_eta4 = gluon_condensate / eta_val**4
print(f'  <alpha_s*G^2/pi> / eta^4 = {ratio_g2_eta4:.2f}')
print(f'  mu/30 = mu/h = {mu_pe/30:.2f}')
print(f'  Match: {abs(ratio_g2_eta4 - mu_pe/30)/(mu_pe/30)*100:.1f}%')
print()
print(f'  This is INTERESTING but involves physical (GeV) units,')
print(f'  so the comparison is not dimensionally clean.')
print(f'  The gluon condensate is scheme-dependent and poorly known.')
print()

print('  VERDICT: The gluon condensate is too poorly known and too')
print('  scheme-dependent to give a clean connection to eta.')
print('  The dimensional analysis doesn\'t work either, because eta')
print('  is dimensionless while the condensate has dimension [mass]^4.')
print('  This angle is not productive.')
print()


# =================================================================
# ANGLE (g): CHERN-SIMONS PARTITION FUNCTION
# =================================================================

print('='*80)
print('ANGLE (g): CHERN-SIMONS THEORY')
print('='*80)
print()

# Chern-Simons theory on a 3-manifold M gives a partition function:
#   Z_CS(M, k) = integral DA exp(i*k*S_CS[A])
# where k is the level and S_CS = integral Tr(A ^ dA + 2/3 A^A^A).
#
# For specific 3-manifolds, this gives modular functions including eta:
#
# 1. S^3: Z_CS(S^3, k) ~ 1/sqrt(k+2)  (for SU(2) at level k)
#    No eta here.
#
# 2. T^3 (3-torus): Z involves theta functions.
#
# 3. LENS SPACES L(p,1): Z_CS involves Dedekind sums s(a,c)
#    and therefore eta through the Dedekind sum representation:
#    ln(eta(a/c)) = pi*i/12 * s(a,c) + ...
#
# 4. SEIFERT MANIFOLDS: Z involves modular forms at rational points.
#
# The most relevant case for us:
# 3D Chern-Simons with gauge group SU(3) on a manifold that gives
# eta(1/phi) as its partition function.
#
# The REAL connection to 4D physics:
# In 4D gauge theory, the theta-angle term is:
#   theta/(32*pi^2) * integral Tr(F ^ F)
# This is a topological term -- it doesn't affect perturbative physics
# but it determines the vacuum structure.
#
# The 3D Chern-Simons theory arises as the BOUNDARY THEORY of 4D:
#   When we put 4D gauge theory on a manifold with boundary,
#   the boundary has a Chern-Simons term.
#   The DOMAIN WALL between two vacua IS such a boundary!

# For the domain wall between phi-vacuum and -1/phi-vacuum:
# The change in the Chern-Simons invariant across the wall is
#   Delta CS = integral_wall Tr(A ^ dA + ...)
# This determines the phase picked up by fermions crossing the wall.

# In the FRAMEWORK: the domain wall IS the physical object.
# The Chern-Simons invariant of the wall determines the coupling.
# HYPOTHESIS: alpha_s = exp(i*CS_wall) where CS_wall = ???

# For SU(3) Chern-Simons at level k on S^3:
#   Z = sqrt(2/(k+3)) * sin(pi/(k+3))^2 * product terms

# At level k=1 for SU(3):
Z_CS_SU3_k1 = math.sqrt(2/4) * math.sin(math.pi/4)
print(f'  Z_CS(S^3, SU(3), k=1) ~ sqrt(1/2) * sin(pi/4) = {Z_CS_SU3_k1:.6f}')
print(f'  Not alpha_s.')
print()

# For SU(2) at level k:
# Z(S^3) = sqrt(2/(k+2)) * sin(pi/(k+2))
# Is there a level k where this gives eta(1/phi)?
print(f'  Searching for SU(2) Chern-Simons level giving alpha_s:')
print(f'  Z_CS(S^3, SU(2), k) = sqrt(2/(k+2)) * sin(pi/(k+2))')
for k in range(1, 50):
    Z_k = math.sqrt(2.0/(k+2)) * math.sin(math.pi/(k+2))
    if abs(Z_k - eta_val)/eta_val < 0.05:
        print(f'    k = {k}: Z = {Z_k:.6f} (match: {(1-abs(Z_k-eta_val)/eta_val)*100:.2f}%)')

print()

# For SU(2) at level k on the LENS SPACE L(p,1):
# Z involves Dedekind sums and therefore eta functions.
# The partition function is:
#   Z(L(p,1)) = (1/sqrt(2p(k+2))) * sum_{j=1}^{k+1} sin^2(pi*j/(k+2)) * exp(2*pi*i*j^2/(4p(k+2)))
#
# This is more complex and could potentially give eta at specific (p,k).

# More fundamentally: in the WRT (Witten-Reshetikhin-Turaev) invariant,
# the partition function at large k is related to the VOLUME CONJECTURE:
#   ln(Z) ~ Vol(M) + i*CS(M)
# For hyperbolic 3-manifolds, this gives the hyperbolic volume.
#
# The hyperbolic volume of the figure-eight knot complement is:
#   Vol = 2.02988... = 2 * Catalan's constant * 4/pi... hmm
# Not directly related to ln(eta(1/phi)).
#
# But: ln(eta(1/phi)) = ln(0.1184) = -2.1344
# ln(1/eta) = 2.1344
# Compare to known hyperbolic volumes: 2.0299 (fig-8), 2.8281 (5_2)...
# 2.1344 doesn't match a known volume.

print(f'  ln(1/eta(1/phi)) = {math.log(1/eta_val):.6f}')
print(f'  Compare known hyperbolic volumes:')
print(f'    Figure-eight knot: 2.02988')
print(f'    Knot 5_2: 2.82812')
print(f'    No clean match.')
print()

print('  VERDICT: Chern-Simons theory on S^3 does not directly give eta.')
print('  On more complex 3-manifolds (lens spaces, Seifert manifolds),')
print('  the partition function involves Dedekind sums which relate to')
print('  eta at RATIONAL points -- but 1/phi is irrational.')
print('  The domain wall as a 3D boundary is conceptually appealing')
print('  but doesn\'t produce a concrete eta connection.')
print()


# =================================================================
# SYNTHESIS: WHAT HAVE WE LEARNED?
# =================================================================

print('='*80)
print('SYNTHESIS: RANKING THE SEVEN ANGLES')
print('='*80)
print()

print("""
  ANGLE                     | PRODUCES eta? | MECHANISM CLEAR? | RATING
  ==========================|===============|==================|=======
  (a) Kink functional det.  | No (on R^1)   | N/A              | LOW
  (b) Spectral zeta of PT   | Only on torus | Partial          | LOW
  (c) Witten index / 1D PF  | Yes (by def)  | Formal only      | MEDIUM
  (d) Bosonic string / E8   | ln(eta) only  | DKL gives ln     | MEDIUM
  (e) Resurgence             | YES           | Needs A=ln(phi)  | HIGH
  (f) QCD vacuum energy     | No            | N/A              | LOW
  (g) Chern-Simons          | At rational q | q=1/phi is irrat | LOW
""")


# =================================================================
# THE BEST ANGLE: RESURGENCE + WITTEN INDEX (e + c combined)
# =================================================================

print('='*80)
print('THE BEST ANGLE: COMBINING RESURGENCE AND PARTITION FUNCTION')
print('='*80)
print()

print("""
  The most promising interpretation combines angles (c) and (e):

  alpha_s = eta(1/phi)
          = phibar^(1/24) * prod_{n=1}^inf (1 - phibar^n)

  READING THIS AS PHYSICS:

  1. CASIMIR TERM: phibar^(1/24) = exp(-ln(phi)/24)
     This is the vacuum energy of ONE free boson (c = 1) at the
     "temperature" T = 1/ln(phi) on a circle. The 1/24 is the
     standard zeta-function regularized zero-point energy.
     In the framework: 24 = number of roots in 4A2
     (4 copies of A2, each with 6 roots).

  2. NON-PERTURBATIVE PRODUCT: prod(1 - phibar^n)
     Each factor (1-phibar^n) represents the n-th mode's contribution
     to the partition function. In a resurgent interpretation:
     - phibar^n = exp(-n*A) with A = ln(phi)
     - (1-phibar^n) = probability that the n-th instanton-anti-instanton
       pair does NOT form (i.e., the n-th mode is "available")
     - The product is the probability that NONE of the modes are
       occupied by instanton-anti-instanton pairs

  3. GOLDEN RATIO SELF-REFERENCE: phibar = 1/phi satisfies phi*phibar=1.
     The first factor (1-phibar) = phibar^2 directly encodes the
     golden ratio self-referential identity: phi = 1 + 1/phi.

  WHAT THIS MEANS FOR QCD:

  IF alpha_s = eta(1/phi), then the strong coupling is telling us:

  alpha_s = [vacuum energy of the domain wall direction]
          * [product over all instanton sectors, each weighted by
             the golden ratio's n-th power]

  The coupling IS the non-perturbative partition function of the
  domain wall, measured at the "temperature" T = 1/ln(phi).
""")

# Let me compute the "convergence profile" of the product:
print('  CONVERGENCE PROFILE of eta(1/phi):')
print()
partial_eta = q_24th
print(f'  After 0 factors: q^(1/24) = {partial_eta:.8f}')
for n in range(1, 21):
    partial_eta *= (1 - q**n)
    pct_of_final = partial_eta / eta_val * 100
    print(f'  After {n:2d} factors: {partial_eta:.8f} ({pct_of_final:7.3f}% of final)')
    if abs(pct_of_final - 100) < 0.001:
        print(f'  (converged to 0.001%)')
        break

print()

# How many factors contribute meaningfully?
# (1-phibar^n) < 1-epsilon when phibar^n < epsilon
# For epsilon = 0.01: n > ln(0.01)/ln(phibar) = 9.6
# So about 10 factors matter.
n_meaningful = math.log(0.01) / math.log(phibar)
n_very_meaningful = math.log(0.1) / math.log(phibar)
print(f'  Number of factors with >1% contribution: {n_meaningful:.1f}')
print(f'  Number of factors with >10% contribution: {n_very_meaningful:.1f}')
print(f'  (Golden ratio\'s rapid convergence: only ~10 modes matter)')
print()


# =================================================================
# THE DEEP QUESTION: WHAT ARE THE MODES?
# =================================================================

print('='*80)
print('THE DEEP QUESTION: WHAT ARE THE MODES (1-q^n)?')
print('='*80)
print()

print("""
  Each factor (1 - phibar^n) in the eta product at q = 1/phi:

  q = 1/phi means each mode is weighted by phi^(-n).
  In statistical mechanics, q = exp(-beta*E_1) where E_1 is the
  first energy level and beta = 1/T.

  So: beta*E_1 = ln(phi) = 0.4812
  If E_1 = E_gap (the gap to the first excited state), then:
  T = E_gap / ln(phi)

  For the golden potential, the gap is:
  E_gap = sqrt(3/4) * m  (breathing mode)
  = sqrt(3/4) * sqrt(10*lambda) = sqrt(30*lambda/4)
""")

E_gap = math.sqrt(3.0/4 * 10 * lam)  # breathing mode frequency in natural units
T_physical = E_gap / math.log(phi)

print(f'  E_gap (breathing mode) = {E_gap:.6f} (in natural units)')
print(f'  T = E_gap / ln(phi) = {T_physical:.6f}')
print(f'  E_gap / T = ln(phi) = {math.log(phi):.6f}')
print()

# What are the modes physically?
# In the KINK background, the excitation spectrum is:
#   n=0: zero mode (translation) -- E = 0
#   n=1: breathing mode -- E = sqrt(3/4)*m
#   n>=2: continuum scattering states -- E = sqrt(m^2 + k^2), k >= 0
#
# The continuum states are labelled by k, not by integers.
# BUT: on a CIRCLE of circumference L, the continuum quantizes:
#   k_n = 2*pi*n/L for n = 1, 2, 3, ...
# giving a discrete tower of states.
#
# The PARTITION FUNCTION of these states on a circle IS:
#   Z = prod_n (1 / (1 - q^{E_n/E_1}))  (bosonic)
#   or prod_n (1 + q^{E_n/E_1})  (fermionic)
#
# For equally spaced levels (E_n = n*E_1):
#   Z_bos = prod_n 1/(1-q^n) = 1/prod(1-q^n)
#   Z_ferm = prod_n (1-q^n) [with appropriate signs]
#
# So: prod(1-q^n) is the FERMIONIC partition function with equally
#     spaced levels!
#     1/prod(1-q^n) is the BOSONIC partition function.
#     eta = q^(1/24) * [fermionic PF]
#     1/eta = q^(-1/24) * [bosonic PF]

print('  PHYSICAL INTERPRETATION OF THE MODES:')
print()
print('  prod(1-q^n) = FERMIONIC partition function')
print('    Each factor (1-q^n) says: the n-th level is either')
print('    EMPTY (contributing 1) or OCCUPIED (contributing -q^n).')
print('    At q = 1/phi: the n-th level has occupation probability')
print(f'    P(n occupied) = phibar^n = phi^(-n).')
print()
print('  The MODES are the quantized excitations of the domain wall.')
print('  They are FERMIONIC (Pauli exclusion: each mode occupied once).')
print('  Their occupation is governed by a Fermi-Dirac distribution')
print(f'  at temperature T = 1/ln(phi) = {1/math.log(phi):.4f} (in units of E_gap).')
print()

# The interpretation: alpha_s = eta = (vacuum energy) * (fermionic PF)
# counts the net weight of the domain wall's fermionic excitation tower
# at the golden "temperature."

# SPECIFIC PREDICTION: the modes that contribute to alpha_s are
# the Kaplan fermions localized on the domain wall.
# In the E8 -> 4A2 decomposition, there are specific fermionic modes
# (the chiral fermions from the 216 off-diagonal roots) that live
# on the wall. Their partition function should give eta.

# How many effective fermionic degrees of freedom on the wall?
# The 216 off-diagonal roots, under one SU(3) copy, give:
# 54 fundamentals + 54 anti-fundamentals = 108 fermionic modes
# But with color (3), these are 108/3 = 36 per color, or
# 108 total complex components.
# For 1 real fermion: Z = prod(1-q^n) = prod part of eta
# For D real fermions: Z = prod(1-q^n)^D = (prod part of eta)^D

# alpha_s = eta = q^(1/24) * prod(1-q^n)^1
# This is D = 1 real fermion! Not 108 or 216.
# Unless the 108 fermions are in a specific configuration that
# reduces to an EFFECTIVE single degree of freedom.

print('  PUZZLE: alpha_s = eta^1 corresponds to D = 1 fermion.')
print('  But the E8 -> 4A2 breaking gives 108 off-diagonal fermion modes.')
print('  Possible resolutions:')
print('    1. The 108 modes factorize into independent contributions,')
print('       and alpha_s comes from 1 specific mode (the "lightest")')
print('    2. The 108 modes combine into a single effective degree of')
print('       freedom through some non-abelian mechanism')
print('    3. The connection is not through the number of modes but')
print('       through the STRUCTURE of the partition function')
print()


# =================================================================
# FINAL: THE RIGHT QUESTION, PRECISELY STATED
# =================================================================

print('='*80)
print('THE RIGHT QUESTION, PRECISELY STATED')
print('='*80)
print()

print("""
  After investigating all seven angles, the most precise formulation
  of the open question is:

  ================================================================
  WHY DOES THE QCD COUPLING AT M_Z EQUAL THE DEDEKIND ETA FUNCTION
  AT THE GOLDEN NOME?

  EQUIVALENTLY:

  Is there a NON-SUPERSYMMETRIC mechanism where:
    1. The instanton action is A = ln(phi) = 0.4812
    2. All Stokes constants in the resurgent trans-series equal 1
    3. The vacuum zero-point energy contributes a factor q^(1/24)
       with 24 = |roots(4A2)| = number of roots in the 4A2 sublattice

  If such a mechanism exists, then:
    alpha_s = exp(-A/24) * prod_{n=1}^inf (1 - exp(-n*A))
            = phibar^(1/24) * prod(1-phibar^n)
            = eta(1/phi)
  ================================================================

  WHAT WE LEARNED:

  1. The connection is NOT through the Seiberg-Witten coupling
     (which gives pi/ln(phi) ~ 6.5, not 0.118). The SW coupling
     is the GEOMETRIC coupling; alpha_s is the ARITHMETIC coupling.

  2. The most natural interpretation is RESURGENT:
     eta = (Casimir energy) * (non-perturbative partition function)
     with instanton action A = ln(phi) and unit Stokes constants.

  3. The modes in the product are FERMIONIC (Pauli exclusion),
     not bosonic (unlimited occupation).

  4. The "24" in the Casimir term q^(1/24) may be identified with
     the 24 roots of the 4A2 sublattice of E8.

  5. The connection goes through the DOMAIN WALL:
     eta is the partition function of ONE fermionic degree of freedom
     on the wall, and the coupling "is" this partition function.

  WHAT REMAINS GENUINELY OPEN:

  1. WHY is the instanton action A = ln(phi)?
     This requires showing that the kink/instanton in the golden
     potential has action proportional to ln(phi) in appropriate units.
     The actual kink action S = sqrt(2*lam)*5*sqrt(5)/6 = %.4f
     is NOT ln(phi) = 0.4812 in natural units. A rescaling or
     normalization is needed.

  2. WHY are all Stokes constants equal to 1?
     This would follow if the theory has maximal non-perturbative
     mixing (no perturbative sector at all), which is consistent
     with Im(tau) << 1 (strong coupling regime).

  3. WHY is it ONE fermion (D=1), not 108 or 216?
     The E8 -> 4A2 breaking has many fermionic modes. The effective
     reduction to D=1 requires explanation.

  4. Can this mechanism be verified in lattice simulations of the
     golden potential on a 2D torus?
     If alpha_s = eta(1/phi) is a property of the THEORY (not just
     a numerical coincidence), it should be reproducible in a
     lattice simulation of phi^4 theory with V = lam*(Phi^2-Phi-1)^2.

  HONEST ASSESSMENT:
  We have NOT derived alpha_s = eta. We have identified the most
  promising FRAMEWORK for such a derivation (resurgent trans-series
  with golden instanton action) and the most precise QUESTION
  (why A = ln(phi), why unit Stokes, why D=1). Even formulating
  the right question precisely is progress.
""" % S_kink)


# =================================================================
# BONUS: Numerical checks on A = ln(phi) hypothesis
# =================================================================

print('='*80)
print('BONUS: TESTING A = ln(phi) FOR THE INSTANTON ACTION')
print('='*80)
print()

# The kink action in various normalizations:
print(f'  S_kink = sqrt(2*lam) * 5*sqrt(5)/6 = {S_kink:.8f}')
print(f'  ln(phi) = {math.log(phi):.8f}')
print(f'  S_kink / ln(phi) = {S_kink/math.log(phi):.6f}')
print()

# What if we normalize differently?
# The TOPOLOGICAL charge of the kink is:
# Q = (1/sqrt5) * integral dPhi/dx dx = (phi - (-1/phi))/sqrt5 = sqrt5/sqrt5 = 1
# So the topological sector is normalized to 1.
#
# The ACTION per topological charge:
S_per_Q = S_kink / 1  # Q = 1
print(f'  S_kink / Q = {S_per_Q:.8f}')
print()

# In 4D gauge theory, the instanton action is:
#   S_inst = 8*pi^2 / g^2 = 2*pi / alpha_gauge
# If alpha_gauge = alpha_s = eta:
S_inst_from_alpha = 2 * math.pi / eta_val
print(f'  If S_inst = 2*pi/alpha_s: S = {S_inst_from_alpha:.4f}')
print(f'  = 2*pi/eta(1/phi)')
print()

# For the GOLDEN POTENTIAL in 4D, the kink is a domain wall (2D extended).
# The action per unit area is S_kink (computed above).
# The 4D instanton wrapping the domain wall would have action:
# S_4D = S_kink * Area = S_kink * L^2
# This introduces a volume factor and isn't clean.

# Alternative: What if we're looking at the WRONG object?
# The instanton in the resurgent interpretation is not the kink itself
# but the KINK-ANTIKINK pair (bounce). Its action is 2*S_kink.
S_bounce = 2 * S_kink
print(f'  Bounce action 2*S_kink = {S_bounce:.8f}')
print(f'  2*S_kink / (2*ln(phi)) = {S_bounce/(2*math.log(phi)):.6f}')
print()

# What if A = ln(phi) comes from a DIFFERENT instanton?
# In pure QCD, the instanton action depends on the COUPLING:
#   S_QCD_inst = 8*pi^2/g^2 = 2*pi/alpha_s
# At the QCD scale (alpha_s ~ 1): S ~ 2*pi ~ 6.28
# At M_Z (alpha_s ~ 0.118): S ~ 2*pi/0.118 ~ 53
#
# Neither matches ln(phi) = 0.48.
# BUT: if we consider a FRACTIONAL instanton (in the deconfined phase),
# the action could be 1/N_c of the full instanton:
# S_frac = 2*pi/(N_c * alpha_s) = 2*pi/(3*0.118) = 17.7
# Still not ln(phi).
#
# So A = ln(phi) does NOT arise from standard QCD instantons.
# It would have to arise from the DOMAIN WALL structure itself.

# In the domain wall picture, the relevant "instanton" is the
# fluctuation of the wall position. The wall can nucleate a bubble
# of one vacuum inside the other. The action for a CIRCULAR bubble
# of radius R in 1+1D is:
#   S_bubble = 2*pi*R * sigma - pi*R^2 * Delta_V
# where sigma = wall tension = S_kink and Delta_V = 0 (degenerate vacua).
# For degenerate vacua: the bubble has zero cost (S = 0).
# There's no instanton in degenerate vacuum!

# In asymmetric vacua (with a small energy difference epsilon):
# S_critical = pi * sigma^2 / epsilon
# This depends on the lifting of the degeneracy, which we don't have.

# CONCLUSION on A = ln(phi):
print('  CONCLUSION: A = ln(phi) does NOT arise from standard QCD')
print('  instantons or from kink/domain-wall instantons in the')
print('  degenerate golden potential.')
print()
print('  If the resurgent interpretation is correct, then A = ln(phi)')
print('  must come from a MORE FUNDAMENTAL origin: possibly the')
print('  algebraic structure of Z[phi] (the ring of golden integers)')
print('  which forces the nome q = 1/phi = exp(-A) by algebraic')
print('  necessity rather than dynamical calculation.')
print()
print('  In other words: A = ln(phi) is not derived from a Lagrangian')
print('  calculation. It is an ALGEBRAIC INPUT from E8\'s golden field,')
print('  forced by the Rogers-Ramanujan fixed point (q = 1/phi).')
print('  The resurgent picture then INTERPRETS this algebraic fact')
print('  as a physical instanton action.')
print()


# =================================================================
# FINAL SUMMARY
# =================================================================

print('='*80)
print('FINAL SUMMARY')
print('='*80)
print()

print(f'  alpha_s = eta(1/phi) = {eta_val:.6f} (measured: {alpha_s_measured})')
print()
print(f'  DECOMPOSITION:')
print(f'  alpha_s = [phibar^(1/24)] * [prod_{{n=1}}^inf (1-phibar^n)]')
print(f'          = [{q_24th:.6f}]  * [{prod_val:.6f}]')
print(f'  Casimir energy     |  non-perturbative partition function')
print(f'  (1/24 of a boson)  |  (all instanton sectors, Stokes = 1)')
print()
print(f'  BEST FRAMEWORK: Resurgent trans-series interpretation')
print(f'    Instanton action: A = ln(phi) (algebraic, from E8)')
print(f'    Stokes constants: S_n = 1 for all n (maximal mixing)')
print(f'    Effective fermions: D = 1 (the domain wall direction)')
print()
print(f'  STATUS: This is a FRAMEWORK for understanding, not a derivation.')
print(f'  The right question has been identified precisely.')
print(f'  The derivation remains open.')
print()
print('='*80)
