"""
gatchina_plasmoid_analysis.py — Derive what is physically happening in the
Gatchina water discharge plasmoid from the Interface Theory framework.

Framework: V(Phi) = lambda*(Phi^2 - Phi - 1)^2
Consciousness conditions:
  1. Poschl-Teller depth n=2 (exactly 2 bound states)
  2. Reflectionlessness (integer n, |T|^2 = 1)
  3. Golden vacua (phi and -1/phi)
  4. Nome q = 1/phi
  5. Creation identity + autopoiesis

Gatchina experiment parameters (Egorov & Stepanov, various publications):
  - 4.8-5 kV DC discharge over water surface with CuSO4 electrolyte
  - Tungsten central electrode, copper ring outer electrode submerged 10cm
  - Capacitor bank 2.475 mF, ~8 kJ per shot
  - Produces 12-20 cm autonomous plasmoids lasting 400-1200 ms
  - Plasmoid interior is aqueous aerosol (water + ions)
  - Electron density 10^16 -> 10^14 cm^-3, temperature 5000K -> 2000K
  - Charged ~-35 nC
  - Appears to move deliberately

Usage:
    python theory-tools/gatchina_plasmoid_analysis.py
"""

import math
import sys

if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# =============================================================================
# FUNDAMENTAL CONSTANTS
# =============================================================================
c = 2.998e8          # speed of light m/s
h_planck = 6.626e-34 # Planck constant J*s
hbar = 1.055e-34     # reduced Planck constant
k_B = 1.381e-23      # Boltzmann constant J/K
e_charge = 1.602e-19 # electron charge C
m_e = 9.109e-31      # electron mass kg
m_p = 1.673e-27      # proton mass kg
m_Cu = 63.5 * 1.661e-27  # copper ion mass kg
mu_0 = 4 * math.pi * 1e-7  # vacuum permeability H/m
eps_0 = 8.854e-12    # vacuum permittivity F/m
phi = (1 + math.sqrt(5)) / 2  # golden ratio
phibar = 1 / phi

print("=" * 80)
print("GATCHINA PLASMOID ANALYSIS THROUGH INTERFACE THEORY FRAMEWORK")
print("V(Phi) = lambda*(Phi^2 - Phi - 1)^2")
print("=" * 80)

# =============================================================================
# SECTION 1: GATCHINA EXPERIMENTAL PARAMETERS
# =============================================================================
print("\n" + "=" * 80)
print("SECTION 1: EXPERIMENTAL PARAMETERS")
print("=" * 80)

V_discharge = 5000       # V (5 kV)
C_bank = 2.475e-3        # F (2.475 mF)
E_stored = 0.5 * C_bank * V_discharge**2
R_plasmoid = 0.08        # m (average 16 cm diameter -> 8 cm radius)
L_plasmoid = 0.16        # m (approximately spherical, 16 cm)
t_lifetime = 0.8         # s (average lifetime 400-1200 ms)
Q_charge = -35e-9        # C (-35 nC)
n_e_initial = 1e16 * 1e6 # m^-3 (10^16 cm^-3 = 10^22 m^-3)
n_e_late = 1e14 * 1e6    # m^-3 (10^14 cm^-3 = 10^20 m^-3)
T_initial = 5000         # K
T_late = 2000            # K

print(f"\n  Discharge voltage: {V_discharge} V")
print(f"  Capacitor bank: {C_bank*1e3:.3f} mF")
print(f"  Stored energy: {E_stored:.0f} J = {E_stored/1e3:.1f} kJ")
print(f"  Plasmoid radius: {R_plasmoid*100:.0f} cm")
print(f"  Plasmoid lifetime: {t_lifetime*1e3:.0f} ms")
print(f"  Charge: {Q_charge*1e9:.0f} nC")
print(f"  n_e (initial): {n_e_initial:.1e} m^-3")
print(f"  n_e (late): {n_e_late:.1e} m^-3")
print(f"  T (initial): {T_initial} K")
print(f"  T (late): {T_late} K")

# Derived parameters
V_plasmoid = (4/3) * math.pi * R_plasmoid**3
n_ion_avg = math.sqrt(n_e_initial * n_e_late)  # geometric mean
rho_plasma = n_ion_avg * m_p  # mass density (hydrogen-like)
# For CuSO4 solution with Cu2+ ions, use effective ion mass
# But the aerosol is mostly water droplets with dissolved ions
rho_water_aerosol = 1000 * 0.01  # assume 1% water content by volume in aerosol
# Better estimate: the aerosol is quite dense - Egorov reports aqueous aerosol interior
# Estimate liquid water fraction from emission spectra: ~0.1-1% by volume
f_water = 0.005  # 0.5% water fraction by volume (conservative)
rho_aerosol = f_water * 1000 + (1 - f_water) * n_ion_avg * m_p

print(f"\n  Derived quantities:")
print(f"  Plasmoid volume: {V_plasmoid*1e6:.1f} cm^3 = {V_plasmoid*1e3:.2f} liters")
print(f"  Geometric mean n_e: {n_ion_avg:.1e} m^-3")
print(f"  Pure plasma mass density: {n_ion_avg * m_p:.2e} kg/m^3")
print(f"  Aerosol mass density (f_water={f_water}): {rho_aerosol:.2f} kg/m^3")

# =============================================================================
# SECTION 2: MAGNETIC FIELD TOPOLOGY
# =============================================================================
print("\n" + "=" * 80)
print("SECTION 2: MAGNETIC FIELD TOPOLOGY INSIDE THE PLASMOID")
print("=" * 80)

print("""
  The Gatchina discharge creates a current pulse through the water surface.
  The current path: tungsten center electrode -> water surface -> plasma ->
  copper ring electrode (submerged 10 cm).

  The geometry is AXISYMMETRIC: central electrode + ring electrode.
  This naturally produces a TOROIDAL magnetic field topology.

  Phase 1 (discharge, t < 10 ms):
    Current I flows radially through the water and vertically through plasma.
    By Ampere's law, this creates a toroidal (azimuthal) B field:
    B_theta(r) = mu_0 * I / (2*pi*r)

  Phase 2 (detachment, t ~ 10-50 ms):
    The plasmoid detaches from the electrode. As it lifts off:
    - The current path pinches (z-pinch effect)
    - Magnetic flux is trapped inside the rising plasmoid
    - The trapped flux forms a TOROIDAL magnetic structure

  Phase 3 (autonomous, t > 50 ms):
    The plasmoid carries its trapped magnetic flux.
    The dominant topology is either:
    (a) A SPHEROMAK: poloidal + toroidal B fields, force-free (j x B = 0)
    (b) A HILL'S VORTEX: axisymmetric flow with embedded B field
    (c) A RANADA KNOT: linked magnetic field lines with Hopf topology
""")

# Estimate the magnetic field
# During discharge: I ~ V/R_plasma
# Plasma resistance: R ~ eta * L / A
# For 5 kV discharge across ~10 cm with 5000 K plasma:
# Spitzer resistivity at 5000 K: eta_Sp ~ 5e-4 ohm*m (partially ionized)
# Actually, for a water-surface discharge, the resistance is dominated by
# the electrode-water contact. Measured current: ~kA range.
# From energy: E = 0.5*C*V^2 = 31 kJ, but effective energy in plasma ~ 8 kJ
# RC time: tau_RC = R*C. For tau ~ 1 ms and C = 2.475 mF: R ~ 0.4 ohm
# Peak current: I_peak = V/R = 5000/0.4 = 12,500 A

R_circuit = 0.4  # ohm (estimated from RC time and capacitance)
I_peak = V_discharge / R_circuit
tau_RC = R_circuit * C_bank

print(f"  Estimated circuit parameters:")
print(f"    Circuit resistance: ~{R_circuit:.1f} ohm")
print(f"    Peak current: I_peak ~ {I_peak:.0f} A = {I_peak/1e3:.1f} kA")
print(f"    RC time constant: tau_RC = {tau_RC*1e3:.2f} ms")

# Magnetic field at plasmoid boundary (r = R_plasmoid)
B_theta_boundary = mu_0 * I_peak / (2 * math.pi * R_plasmoid)
# Magnetic field at center (r ~ 1 cm, where current channels)
r_core = 0.01  # m (1 cm current channel radius)
B_theta_core = mu_0 * I_peak / (2 * math.pi * r_core)

print(f"\n  Magnetic field estimates (during discharge):")
print(f"    At boundary (r={R_plasmoid*100:.0f} cm): B ~ {B_theta_boundary*1e3:.1f} mT = {B_theta_boundary*1e4:.0f} G")
print(f"    At core (r={r_core*100:.0f} cm): B ~ {B_theta_core*1e3:.1f} mT = {B_theta_core*1e4:.0f} gauss")
print(f"    Central flux density: {B_theta_core:.3f} T")

# After detachment, the trapped field decays but is sustained by currents
# Magnetic energy in the plasmoid
# For a spheromak: E_B ~ (B^2/(2*mu_0)) * V
B_trapped = B_theta_boundary * 0.3  # ~30% of peak field remains trapped
E_magnetic = (B_trapped**2 / (2 * mu_0)) * V_plasmoid
print(f"\n  After detachment (trapped field):")
print(f"    Estimated trapped field: B ~ {B_trapped*1e3:.2f} mT")
print(f"    Magnetic energy: E_B ~ {E_magnetic:.2f} J")
print(f"    Fraction of stored energy: {E_magnetic/E_stored*100:.2f}%")

# =============================================================================
# SECTION 3: HARRIS SHEET PROFILE AT THE PLASMOID BOUNDARY
# =============================================================================
print("\n" + "=" * 80)
print("SECTION 3: IS THE PLASMOID BOUNDARY A HARRIS-TYPE CURRENT SHEET?")
print("=" * 80)

print("""
  The critical question: does the plasmoid boundary have a sech^2 profile?

  A SPHEROMAK has the following structure:
  - Inside: organized B field (both toroidal and poloidal components)
  - Outside: weak or zero B field
  - Boundary: a CURRENT SHEET where B changes direction/magnitude rapidly

  The boundary of a spheromak IS a Harris-type current sheet:
  - The toroidal field B_theta is maximum inside, zero outside
  - The transition occurs over a skin depth delta_skin

  For the Gatchina plasmoid specifically:
  - The plasma is partially ionized (5000K -> 2000K)
  - The boundary is a TRANSITION from plasma to air
  - The B field goes from B_trapped (inside) to ~0 (outside)
  - The transition profile depends on the plasma beta and conductivity

  Harris sheet profile: B(x) = B_0 * tanh(x/w)
  Equivalent: the perturbation potential is V(x) = -B_0^2/(cosh^2(x/w))
  This IS a Poschl-Teller potential.
""")

# Skin depth / transition thickness
# For a partially ionized plasma at 2000-5000 K:
# Magnetic diffusivity: eta_m = 1/(mu_0 * sigma)
# Conductivity of partially ionized gas at 5000 K:
# sigma ~ 100 S/m (rough estimate for partially ionized H/Cu/O mixture)
sigma_plasma = 100  # S/m (order of magnitude)
eta_mag = 1 / (mu_0 * sigma_plasma)
# Magnetic diffusion time for the plasmoid:
tau_diff = mu_0 * sigma_plasma * R_plasmoid**2
# Skin depth at frequency omega ~ 1/t_lifetime:
omega_char = 2 * math.pi / t_lifetime
delta_skin = math.sqrt(2 * eta_mag / omega_char)

print(f"  Plasma conductivity (est.): sigma ~ {sigma_plasma} S/m")
print(f"  Magnetic diffusivity: eta_m = {eta_mag:.1f} m^2/s")
print(f"  Magnetic diffusion time: tau_diff = {tau_diff:.3f} s")
print(f"  Characteristic skin depth: delta = {delta_skin*100:.1f} cm")
print(f"  Ratio delta/R_plasmoid = {delta_skin/R_plasmoid:.2f}")

# The Harris sheet width
w_harris = delta_skin  # the boundary transition width
print(f"\n  Harris sheet width: w ~ {w_harris*100:.1f} cm = {w_harris*1e3:.0f} mm")
print(f"  This gives the current sheet transition profile:")
print(f"    B(x) = B_0 * tanh(x/w), w = {w_harris*100:.1f} cm")
print(f"    j(x) = B_0 / (mu_0 * w * cosh^2(x/w))")
print(f"    V_eff(x) = -N(N+1) * kappa^2 / cosh^2(x/w)")

# =============================================================================
# SECTION 4: ALFVEN SPEED RATIO AND PT DEPTH
# =============================================================================
print("\n" + "=" * 80)
print("SECTION 4: ALFVEN SPEED RATIO AND POSCHL-TELLER DEPTH")
print("=" * 80)

print("""
  Framework condition for n=2: v_A(inside) / v_A(outside) >= sqrt(6) ~ 2.45

  For the Gatchina plasmoid, the Alfven speed is:
    v_A = B / sqrt(mu_0 * rho)

  where rho is the effective mass density of the medium.

  KEY INSIGHT: Inside the plasmoid, the medium is AQUEOUS AEROSOL,
  not pure plasma. The mass density is MUCH higher than pure plasma.
  Outside the plasmoid, it is air (or very tenuous plasma).
""")

# Inside the plasmoid: aqueous aerosol
# The aerosol has both plasma component and water droplet component
# For Alfven wave propagation, what matters is the EFFECTIVE mass density
# that couples to the magnetic field.

# In a partially ionized plasma with aerosol:
# Only the ionized component participates in Alfven dynamics
# BUT the neutral component provides inertia via collisions
# The relevant density for Alfven speed is:
# rho_eff = rho_plasma * (1 + chi) where chi = rho_neutral/rho_plasma

# For 5000K partially ionized gas:
# Ionization fraction of hydrogen: ~0.1% at 5000K (Saha equation)
# But CuSO4 provides ions directly
# Cu2+ concentration: ~0.1 M = 6e25 ions/m^3 in original solution
# After aerosolization: depends on droplet size and density

# Let's compute for several density scenarios:
print(f"  Computing Alfven speed for different interior conditions:\n")

scenarios = [
    ("Pure plasma (n_e = 1e22 m^-3)", n_e_initial * m_p, B_trapped),
    ("Pure plasma (n_e = 1e20 m^-3)", n_e_late * m_p, B_trapped),
    ("Light aerosol (rho = 0.01 kg/m^3)", 0.01, B_trapped),
    ("Dense aerosol (rho = 1 kg/m^3)", 1.0, B_trapped),
    ("Very dense aerosol (rho = 10 kg/m^3)", 10.0, B_trapped),
]

# Outside: air at room temperature (no field, but if there IS residual field)
# The relevant comparison is the magnetosonic speed outside
# v_A outside is essentially c_s (sound speed in air) since B ~ 0
c_s_air = 343  # m/s (speed of sound in air at 20 C)
rho_air = 1.2  # kg/m^3

# But more physically: the plasmoid has a hot boundary layer
# Outside the plasmoid: hot air/weak plasma at ~1000 K
# T_outside ~ 500-1000 K (heated air around plasmoid)
T_outside = 700  # K
c_s_outside = math.sqrt(1.4 * k_B * T_outside / (29 * 1.661e-27))  # air

# For the Alfven speed ratio, we need B field OUTSIDE too
# The return flux of the spheromak creates a dipole-like field outside
B_outside = B_trapped * (R_plasmoid / (R_plasmoid + w_harris))**3  # dipole falloff
B_outside_min = B_trapped * 0.01  # assume 1% of internal field

print(f"  Outside conditions:")
print(f"    T_outside ~ {T_outside} K")
print(f"    Sound speed in hot air: c_s = {c_s_outside:.0f} m/s")
print(f"    B_outside (dipole): {B_outside*1e3:.3f} mT")
print(f"    rho_air = {rho_air} kg/m^3")
v_A_outside = B_outside / math.sqrt(mu_0 * rho_air)
v_A_outside_max = B_trapped * 0.1 / math.sqrt(mu_0 * 0.1)  # 10% B, low density
print(f"    v_A outside: {v_A_outside:.2f} m/s")
print(f"    v_A outside (generous): {v_A_outside_max:.2f} m/s")
print(f"    Effective outside speed (max of v_A, c_s): {max(v_A_outside, c_s_outside):.0f} m/s")

v_outside_eff = max(v_A_outside, c_s_outside)

print(f"\n  {'Scenario':<45} {'rho (kg/m^3)':<15} {'v_A (m/s)':<15} {'Ratio':<10} {'N':<8}")
print(f"  {'-'*45} {'-'*15} {'-'*15} {'-'*10} {'-'*8}")

for name, rho, B in scenarios:
    v_A = B / math.sqrt(mu_0 * rho)
    ratio = v_A / v_outside_eff
    # N(N+1) = ratio^2 (for the PT depth from Alfven speed ratio)
    nn1 = ratio**2
    # Solve N(N+1) = nn1 -> N = (-1 + sqrt(1 + 4*nn1))/2
    N_PT = (-1 + math.sqrt(1 + 4 * nn1)) / 2
    print(f"  {name:<45} {rho:<15.2e} {v_A:<15.2f} {ratio:<10.3f} {N_PT:<8.2f}")

# The KEY scenario: what density is needed for n=2?
# For n=2: N(N+1) = 6, so (v_A_in / v_outside)^2 = 6
# v_A_in = sqrt(6) * v_outside = sqrt(6) * 500 m/s ~ 1225 m/s
# v_A = B/sqrt(mu_0 * rho) -> rho = B^2/(mu_0 * v_A^2)
v_A_target = math.sqrt(6) * v_outside_eff
rho_target = B_trapped**2 / (mu_0 * v_A_target**2)

print(f"\n  >>> For PT n=2 condition:")
print(f"      Required v_A(inside) = sqrt(6) * {v_outside_eff:.0f} = {v_A_target:.0f} m/s")
print(f"      Required density: rho = {rho_target:.2e} kg/m^3")
print(f"      With B_trapped = {B_trapped*1e3:.2f} mT")

# Check: what B field is needed at typical aerosol density?
for rho_test in [0.01, 0.1, 1.0]:
    B_needed = math.sqrt(mu_0 * rho_test) * v_A_target
    print(f"      At rho = {rho_test} kg/m^3: need B >= {B_needed*1e3:.2f} mT = {B_needed*1e4:.1f} G")

# =============================================================================
# SECTION 5: THE WATER AEROSOL AS COUPLING MEDIUM
# =============================================================================
print("\n" + "=" * 80)
print("SECTION 5: WATER AEROSOL AS COUPLING MEDIUM")
print("=" * 80)

print("""
  CRITICAL FRAMEWORK INSIGHT:

  The Gatchina plasmoid has BOTH coupling media present simultaneously:
  - PLASMA: the ionized component (stellar-scale coupling medium)
  - WATER: the aerosol droplets (biological-scale coupling medium)

  This is UNIQUE among laboratory plasma experiments.

  The framework says:
  - Water is the biological coupling medium (impedance matching, coherence, network)
  - Plasma is the stellar coupling medium (Alfven waves, MHD)
  - Both operate through the SAME V(Phi) architecture

  In the Gatchina plasmoid:
  - The plasma provides the MAGNETIC DOMAIN WALL (Harris sheet at boundary)
  - The water aerosol provides the COUPLING MEDIUM inside the wall
  - CuSO4 provides the CHARGED INTERFACES that the framework says
    are essential for water structuring

  The water-plasma synergy:
  1. Water droplets are suspended in plasma
  2. The strong electric fields (5 kV over ~10 cm = 50 kV/m) polarize water
  3. Cu2+ ions at water droplet surfaces create the charged interfaces
     that the framework identifies as coupling-enhancing
  4. The plasma's magnetic field threads through the water droplets
  5. The system has BOTH biological AND plasma coupling simultaneously
""")

# Water structuring parameters
# Cu2+ concentration in original CuSO4 solution: ~0.1 M
c_CuSO4 = 0.1  # mol/L
n_Cu = c_CuSO4 * 6.022e23 * 1e3  # ions/m^3 in solution
# Debye length in CuSO4 solution
I_ionic = 0.5 * (c_CuSO4 * 4 + c_CuSO4 * 4)  # ionic strength (Cu2+ and SO4 2-)
# Actually I = 0.5 * sum(c_i * z_i^2) = 0.5*(0.1*4 + 0.1*4) = 0.4 M
lambda_D_sol = math.sqrt(eps_0 * 80 * k_B * 300 / (2 * 0.4 * 1e3 * 6.022e23 * e_charge**2))

print(f"  CuSO4 solution parameters:")
print(f"    Concentration: {c_CuSO4} M")
print(f"    Cu2+ number density: {n_Cu:.1e} m^-3")
print(f"    Ionic strength: {I_ionic:.1f} M")
print(f"    Debye length: {lambda_D_sol*1e9:.2f} nm")
print(f"    This means: ions create structured water within {lambda_D_sol*1e9:.0f} nm of each interface")

# Aerosol droplet parameters
# Typical aerosol from discharge: droplet diameter 0.1-10 um
d_droplet = 1e-6  # 1 um diameter (typical)
r_droplet = d_droplet / 2
A_droplet = 4 * math.pi * r_droplet**2
V_droplet = (4/3) * math.pi * r_droplet**3
# Surface-to-volume ratio
SV_ratio = A_droplet / V_droplet
# Fraction of water within Debye length of surface
f_interfacial = 1 - (1 - lambda_D_sol / r_droplet)**3

print(f"\n  Aerosol droplet parameters (d = {d_droplet*1e6:.0f} um):")
print(f"    Surface/volume ratio: {SV_ratio:.2e} m^-1")
print(f"    Fraction of water within Debye length: {f_interfacial*100:.1f}%")
print(f"    --> For 1 um droplets, ~{f_interfacial*100:.0f}% of water is 'interfacial'")

# For smaller droplets
for d in [0.1e-6, 0.5e-6, 1e-6, 5e-6, 10e-6]:
    r = d / 2
    f_int = 1 - max(0, (1 - lambda_D_sol / r))**3
    print(f"    d = {d*1e6:.1f} um: {f_int*100:.1f}% interfacial water")

print(f"""
  FRAMEWORK CONNECTION:

  The framework says dielectric constant drops 20-40x at charged interfaces.
  In the Gatchina aerosol:
  - CuSO4 provides the charged species
  - Sub-micron water droplets have a HUGE fraction of interfacial water
  - The interfacial water has dramatically altered dielectric properties
  - This is EXACTLY the condition for enhanced coupling in the framework

  Additionally, Cu2+ is a transition metal with unfilled d-orbitals.
  [Cu(H2O)6]^2+ complexes in water are known to show:
  - d-d transitions absorbing at 600-900 nm
  - Jahn-Teller distortion breaking octahedral symmetry
  - The blue color of CuSO4 solution IS the d-d transition

  The Cu2+ ion acts as a local AROMATIC ANALOG: unfilled orbitals
  with delocalized electron density, coupling to the EM field at
  optical frequencies. Not a true aromatic, but a metal center with
  pi-symmetry d-orbitals that serve a similar function.
""")

# =============================================================================
# SECTION 6: RANADA ELECTROMAGNETIC KNOT AND HOPF TOPOLOGY
# =============================================================================
print("=" * 80)
print("SECTION 6: RANADA KNOT MODEL AND HOPF TOPOLOGY")
print("=" * 80)

print("""
  THE RANADA MODEL (1996, 1998):

  Ranada proposed that ball lightning is a topological electromagnetic knot:
  a configuration where magnetic field lines form closed, LINKED loops.

  The topology is the HOPF FIBRATION:
  - S^3 -> S^2 with fiber S^1
  - Every pair of magnetic field lines is linked with linking number 1
  - The magnetic helicity H = integral(A . B dV) is conserved
  - Topological protection: the knot cannot be untied by smooth deformations

  KEY QUESTION: Does the Hopf topology give PT n >= 2?

  DERIVATION:

  The Ranada knot's magnetic field in cylindrical coordinates (r, theta, z):
  B_r, B_theta, B_z have profiles that, near the central axis, look like:

  |B|^2(r) ~ B_0^2 / (1 + (r/a)^2)^3

  where a is the characteristic knot radius.

  For perturbations propagating along the symmetry axis, the effective
  potential for trapped modes is:

  V_eff(r) ~ -d^2(|B|)/dr^2 ~ -6/a^2 * 1/(1 + (r/a)^2)^2

  This is NOT exactly sech^2 but it IS a confining potential that falls off
  faster than 1/r^2 at infinity -- it supports bound states.
""")

# Hopf fibration and PT bound states
print(f"  Hopf fibration topology:")
print(f"    pi_3(S^2) = Z  (integer-valued topological invariant)")
print(f"    Each field line links every other with linking number = 1")
print(f"    Magnetic helicity: H = integral(A . B dV) = CONSERVED")
print(f"    Hopf index: Q_H = H / (8*pi^2) = integer")

# The effective potential from a Hopf magnetic field
# Near the knot core, B ~ B_0 * sech^2(r/a) approximately
# The PT depth depends on the profile shape

# For a pure Hopf field (Ranada 1996):
# The magnetic pressure profile is:
# P_B(r) = B^2/(2*mu_0) ~ B_0^2/(2*mu_0) * 1/(1 + (r/a)^2)^3

# The effective potential for Alfven-type perturbations:
# V(r) = -omega_A^2 * d^2/dr^2 [ln B(r)]
# For B ~ 1/(1 + (r/a)^2)^{3/2}:
# d^2/dr^2 [ln B] = d^2/dr^2 [-3/2 * ln(1 + (r/a)^2)]
# = -3/a^2 * [1 - (r/a)^2] / [1 + (r/a)^2]^2

# At r = 0: V(0) = -3/a^2 (maximum depth)
# This profile is approximately -3*sech^2(r/a) for small r

# For a sech^2 profile: V = -N(N+1)/cosh^2 -> N(N+1) ~ 3
# N(N+1) = 3 is not exactly satisfied by integer N
# But N ~ 1.3 (between 1 and 2)

print(f"\n  Effective potential analysis for Hopf knot:")
print(f"    B(r) ~ B_0 / (1 + (r/a)^2)^(3/2)")
print(f"    V_eff(r) ~ -3/a^2 * [1 - (r/a)^2] / [1 + (r/a)^2]^2")
print(f"    Maximum depth: V(0) ~ 3/a^2")
print(f"    Approximate PT depth: N(N+1) ~ 3")
print(f"    N ~ {(-1 + math.sqrt(1 + 12))/2:.2f} (non-integer!)")
print(f"    This means: pure Hopf knot supports ~1 bound state (N near 1)")
print(f"    NOT n=2. The pure Ranada knot is 'sleeping' (n=1).")

print(f"""
  HOWEVER -- the Ranada knot with PLASMA PRESSURE modification:

  In a real plasma (not vacuum), the Grad-Shafranov equilibrium adds
  a pressure term. The force balance j x B = grad(P) modifies the profile.

  For a plasma spheromak with Hopf topology:
  B^2/(2*mu_0) + P = const  (pressure balance)

  If the plasma pressure peaks at the center (hot core):
  P(r) = P_0 * sech^2(r/a)

  Then: B^2(r) = B_0^2 - 2*mu_0*P_0*sech^2(r/a)

  The TOTAL effective potential (magnetic + thermal) can be deeper
  than the pure magnetic case. With plasma pressure:
  V_eff ~ -(N_B + N_P)(N_B + N_P + 1) / cosh^2(x/w)

  The plasma pressure can push N above 2!
""")

# For the Gatchina plasmoid:
P_thermal = n_ion_avg * k_B * T_initial  # thermal pressure
P_magnetic = B_trapped**2 / (2 * mu_0)  # magnetic pressure
beta = P_thermal / P_magnetic  # plasma beta

print(f"  Gatchina plasmoid pressure balance:")
print(f"    Thermal pressure: P = {P_thermal:.1f} Pa")
print(f"    Magnetic pressure: B^2/(2*mu_0) = {P_magnetic:.2f} Pa")
print(f"    Plasma beta: beta = P/P_B = {beta:.1f}")
print(f"    (beta >> 1 means thermally dominated)")

# For high-beta plasma, the effective PT depth is dominated by thermal profile
# If the temperature profile is sech^2:
# T(r) = T_0 * sech^2(r/a) (peaked at center)
# Then n*T gives: pressure ~ n*T_0*sech^2

# The effective N for a pressure-confined structure:
# N(N+1) ~ (P_inside - P_outside) / P_outside
# For the Gatchina plasmoid:
P_outside = rho_air * k_B * T_outside / (29 * 1.661e-27)
P_ratio = P_thermal / P_outside

print(f"    Outside pressure: P_out ~ {P_outside:.0f} Pa")
print(f"    Pressure ratio: P_in/P_out ~ {P_ratio:.1f}")
print(f"    If this maps to N(N+1): N ~ {(-1 + math.sqrt(1 + 4*P_ratio))/2:.1f}")
print(f"    This is very deep -- the thermal profile supports MANY bound states")
print(f"    The system is NOT fine-tuned to n=2; it has n >> 2")

# =============================================================================
# SECTION 7: THE CORRECT ANALYSIS -- WHAT MATTERS FOR THE FRAMEWORK
# =============================================================================
print("\n" + "=" * 80)
print("SECTION 7: WHAT IS ACTUALLY HAPPENING -- FRAMEWORK INTERPRETATION")
print("=" * 80)

print("""
  RE-ANALYSIS: The Gatchina plasmoid as a domain wall structure.

  The plasmoid boundary is NOT a simple Harris current sheet.
  It is a COMPOSITE structure:

  1. MAGNETIC boundary: B field transition (Harris-like)
  2. THERMAL boundary: temperature jump (5000K inside -> 300K outside)
  3. DENSITY boundary: plasma/aerosol inside -> air outside
  4. CHEMICAL boundary: Cu2+/SO4^2-/H2O aerosol inside -> N2/O2 outside

  Each boundary contributes to the effective PT depth.

  The FRAMEWORK'S n=2 condition requires the TOTAL effective potential
  to have exactly 2 bound states. In the Gatchina plasmoid:

  - The thermal boundary alone gives n >> 2 (too deep)
  - The magnetic boundary alone gives n ~ 0.5-1 (too shallow)
  - The MHD boundary (combined) gives n ~ several

  This means the Gatchina plasmoid is NOT optimized for n=2.
  It has TOO MANY trapped modes -- it is 'over-deep.'

  FRAMEWORK PREDICTION: A plasmoid with n >> 2 would show:
  - Many oscillation frequencies (not just 2)
  - Internal structure (multiple modes excited)
  - But NOT the specific reflectionless property of n=2
  - NOT the clean 2-mode architecture of consciousness

  The Gatchina plasmoid is more like a COMPLEX ORGAN than a conscious being.
  It has structure, organization, self-maintenance -- but too many modes
  for the clean 2-bound-state architecture that the framework identifies
  with consciousness.

  HOWEVER: within the plasmoid, SUBSTRUCTURES could have n=2.
  - Individual plasmoid filaments
  - Current sheets between internal magnetic islands
  - Vortex boundaries within the flow

  The 'apparent intentionality' of Gatchina plasmoids could be:
  (a) Simple MHD dynamics (buoyancy, electromagnetic forces)
  (b) Substructure organization below the resolution of current diagnostics
  (c) The water aerosol coupling medium enhancing whatever PT n=2
      sub-structures exist within the plasmoid
""")

# =============================================================================
# SECTION 8: CAN WE DO BETTER? DERIVING THE MINIMUM REQUIREMENTS
# =============================================================================
print("=" * 80)
print("SECTION 8: MINIMUM REQUIREMENTS FOR A DOMAIN WALL PLASMOID")
print("=" * 80)

print("""
  What are the ABSOLUTE MINIMUM conditions for creating a structure
  with PT n=2, reflectionlessness, and self-maintenance?

  From the framework, we need:
  1. A domain wall (transition between two distinct states)
  2. sech^2 profile (or close approximation)
  3. N(N+1) = 6 (exactly, for n=2)
  4. Continuous energy input (autopoiesis)
  5. Coupling medium (water + charged interfaces preferred)
""")

# Minimum energy calculation
# The minimum magnetic domain wall requires:
# E_wall = sigma_wall * A_wall
# where sigma_wall = domain wall tension = B^2 * w / (2 * mu_0)
# For n=2 with sech^2 profile width w:

# The minimum-energy configuration that satisfies N(N+1) = 6:
# v_A(in)/v_A(out) = sqrt(7) ~ 2.65 (including the +1 in the formula)
# Actually N(N+1) = (v_A_ratio)^2 gives 6 when ratio = sqrt(6) = 2.449

print(f"  Minimum energy for n=2 domain wall:")
print(f"    Required Alfven speed ratio: sqrt(6) = {math.sqrt(6):.4f}")
print()

# For a SPHERICAL domain wall of radius R:
# Minimum: make R as small as possible and B as small as possible
# But B must be large enough to give the right Alfven speed ratio

# Constraint: v_A(inside) / v_outside = sqrt(6)
# For magnetic: v_A = B / sqrt(mu_0 * rho)
# Inside has field B_in, density rho_in
# Outside has field B_out ~ 0, effective speed c_s

# The minimum energy scales as:
# E ~ (B_in^2 / (2*mu_0)) * (4/3)*pi*R^3

# What sets the minimum R?
# The wall must support at least 2 bound states.
# The bound state wavelength is lambda ~ 2*pi*w (the wall width)
# The wall must be larger than the bound state wavelength
# R > w (trivially satisfied for a sphere)
# More importantly: w must be resolvable by the medium
# For plasma: w > rho_i (ion gyroradius)
# For water aerosol: w > d_droplet (droplet diameter)

# Ion gyroradius
# rho_i = m_i * v_thermal / (e * B)
v_thermal_ion = math.sqrt(2 * k_B * T_late / m_p)
rho_i = m_p * v_thermal_ion / (e_charge * B_trapped) if B_trapped > 0 else float('inf')

print(f"  Physical constraints:")
print(f"    Ion thermal speed (2000K): {v_thermal_ion:.0f} m/s")
print(f"    Ion gyroradius (at B={B_trapped*1e3:.1f} mT): {rho_i*100:.1f} cm")
print(f"    (This is LARGE -- the magnetic field is weak)")

# For a microwave-generated plasma:
print(f"\n  >>> MICROWAVE APPROACH (2.45 GHz magnetron):")
P_magnetron = 1000  # W (standard microwave oven)
f_mw = 2.45e9  # Hz
lambda_mw = c / f_mw
omega_mw = 2 * math.pi * f_mw

# Microwave plasma parameters
# At atmospheric pressure, 2.45 GHz microwave with 1 kW:
# Typical: n_e ~ 10^19-10^20 m^-3, T_e ~ 10000-15000 K
n_e_mw = 1e19  # m^-3 (typical for atmospheric microwave plasma)
T_e_mw = 12000  # K
T_gas_mw = 2000  # K (gas temperature, lower than electron temperature)

# Plasma frequency
omega_pe_mw = math.sqrt(n_e_mw * e_charge**2 / (m_e * eps_0))
f_pe_mw = omega_pe_mw / (2 * math.pi)

print(f"    Magnetron power: {P_magnetron} W")
print(f"    Frequency: {f_mw/1e9:.2f} GHz, wavelength: {lambda_mw*100:.1f} cm")
print(f"    Typical atmospheric MW plasma:")
print(f"      n_e ~ {n_e_mw:.0e} m^-3")
print(f"      T_e ~ {T_e_mw} K, T_gas ~ {T_gas_mw} K")
print(f"      Plasma frequency: {f_pe_mw/1e9:.1f} GHz")
print(f"      Note: f_pe < f_mw, so microwaves CAN propagate into plasma")

# For a microwave torch over water:
print(f"""
  >>> MICROWAVE + WATER APPROACH:

  CONCEPT: Use a 2.45 GHz magnetron (standard microwave oven) to create
  a plasma discharge over/through water with dissolved salts.

  Advantages over Gatchina:
  1. CONTINUOUS energy input (not pulsed capacitor bank)
  2. Much lower voltage (no 5 kV needed)
  3. Naturally creates SPHERICAL plasma at the nozzle tip
  4. Water vapor is the plasma medium (H2O decomposition products)
  5. Can add aromatic compounds to the water

  The key innovation: optimize the GEOMETRY for Harris sheet formation.
""")

# Microwave plasma torch parameters
# A waveguide concentrates 1 kW of 2.45 GHz into a ~1 cm diameter spot
# The E field in the plasma:
E_mw = math.sqrt(2 * P_magnetron / (eps_0 * c * math.pi * (0.005)**2))
# This drives currents in the plasma
# The induced magnetic field:
# j = sigma * E, B ~ mu_0 * j * L
j_mw = sigma_plasma * E_mw
B_mw = mu_0 * j_mw * 0.01  # over 1 cm scale

print(f"  Microwave-induced fields:")
print(f"    E field in plasma: ~{E_mw:.0f} V/m")
print(f"    Current density: j ~ {j_mw:.0e} A/m^2")
print(f"    Induced B field (over 1 cm): B ~ {B_mw*1e3:.3f} mT")

# The microwave approach creates DIFFERENT physics:
# The microwave OSCILLATING field can create a pondermotive force
# that confines the plasma. The standing wave pattern creates
# nodes and anti-nodes that act as potential wells.

# Pondermotive potential
# U_pond = e^2 * E^2 / (4 * m_e * omega^2)
U_pond = e_charge**2 * E_mw**2 / (4 * m_e * omega_mw**2)
U_pond_eV = U_pond / e_charge

print(f"    Pondermotive potential: U = {U_pond_eV:.2f} eV = {U_pond/k_B:.0f} K")

# =============================================================================
# SECTION 9: THE SIMPLEST POSSIBLE EXPERIMENT
# =============================================================================
print("\n" + "=" * 80)
print("SECTION 9: MINIMUM VIABLE 'PLASMA DOMAIN WALL GENERATOR'")
print("=" * 80)

print("""
  DESIGN GOALS:
  1. Create a Harris-type current sheet with sech^2 profile
  2. Tune to v_A ratio = sqrt(6) ~ 2.45
  3. Include water as coupling medium
  4. Sustain with continuous energy input
  5. Use off-the-shelf components

  THREE CANDIDATE ARCHITECTURES:
""")

print("""
  === ARCHITECTURE A: MICROWAVE WATER PLASMA TORCH ===

  Components:
  - 1 microwave magnetron (2.45 GHz, 1 kW) from a microwave oven (~$50)
  - Waveguide (WR340 aluminum, can be 3D-printed in metal or bought ~$30)
  - Quartz tube (25 mm OD) as plasma chamber (~$10)
  - Peristaltic pump to feed water/solution into quartz tube (~$30)
  - Water + CuSO4 (or tryptophan) solution
  - 3D-printed nozzle/geometry for shaping the gas flow
  - Standard power supply / microwave oven electronics

  Total cost: ~$150-300

  How it works:
  1. Water solution drips/flows through quartz tube inside waveguide
  2. Microwave field ionizes water vapor, creating plasma
  3. The geometry of the waveguide creates a STANDING WAVE
  4. At the standing wave maximum: plasma forms with sech^2 intensity profile
  5. Water droplets from the feed provide the coupling medium
  6. The plasma is CONTINUOUS (not pulsed)

  Key physics:
  - The standing wave in the waveguide naturally creates a sech^2 field profile
    (actually sinusoidal, but near a maximum it approximates sech^2)
  - By placing the plasma at the field maximum, you get a potential well
  - The pondermotive force confines electrons in the sech^2 well
  - Ions follow by ambipolar diffusion

  Advantage: CONTINUOUS operation (the framework needs autopoiesis)
  Disadvantage: The B field is oscillating at 2.45 GHz, not static
    But: the pondermotive force IS static (time-averaged)
""")

print("""
  === ARCHITECTURE B: COAXIAL PLASMA GUN OVER WATER ===

  Components:
  - Capacitor bank: 10x 450V 1000uF electrolytic capacitors (~$30)
  - Trigger: SCR or IGBT switch (~$10)
  - Electrodes: 3D-printed titanium or tungsten (or just copper nails)
  - Geometry: COAXIAL -- center pin + outer ring, separated by 5 cm
  - Water container: glass dish with CuSO4 solution
  - Power supply: any 400V DC source (boost converter, ~$20)

  Total cost: ~$100-200

  This is essentially a SIMPLIFIED Gatchina:
  - Lower voltage (450V vs 5 kV) -- SAFER
  - Smaller capacitor bank (5 J vs 31 kJ)
  - But optimized geometry for Harris sheet formation

  Key innovation: 3D-PRINT THE ELECTRODE GEOMETRY
  - Design the electrodes so the current path creates a tanh B field profile
  - The outer electrode is a carefully shaped ring that produces
    a magnetic field with sech^2 radial profile
  - The inner electrode tip is sharpened to concentrate the current

  The electrode shape that gives a Harris profile:
  - Outer ring radius: R_out (adjustable)
  - Inner electrode radius: r_in << R_out
  - The gap between them is filled with water vapor / plasma
  - The B field between coaxial conductors: B(r) = mu_0*I/(2*pi*r)
  - To get sech^2: need variable current density along the gap
  - Achievable with TAPERED electrodes (3D printed)
""")

# Design the tapered electrode
print(f"  Coaxial electrode design for Harris sheet:")
print(f"    Inner electrode: r_in = 2 mm (copper wire)")
print(f"    Outer electrode: R_out = 50 mm (3D-printed copper ring)")
print(f"    Gap: 48 mm filled with water vapor + plasma")
print(f"    At V = 450 V, gap = 48 mm: E = {450/0.048:.0f} V/m")
print(f"    Breakdown voltage of moist air: ~1-3 kV/cm at 1 atm")
print(f"    {450/0.048/100:.0f} V/cm -- below breakdown for dry air")
print(f"    BUT: water vapor lowers breakdown threshold significantly")
print(f"    Steam at 100C: breakdown at ~{0.3*450/0.048/100:.0f}-{0.5*450/0.048/100:.0f} V/cm")

# Energy in the capacitor bank
C_total_B = 10 * 1000e-6  # 10 mF
V_charge_B = 450  # V
E_stored_B = 0.5 * C_total_B * V_charge_B**2
I_peak_B = V_charge_B / 1.0  # assume 1 ohm circuit
B_peak_B = mu_0 * I_peak_B / (2 * math.pi * 0.02)  # at 2 cm

print(f"\n    Capacitor bank: {C_total_B*1e3:.0f} mF at {V_charge_B} V")
print(f"    Stored energy: {E_stored_B:.0f} J")
print(f"    Peak current (1 ohm): {I_peak_B:.0f} A")
print(f"    Peak B field at r=2cm: {B_peak_B*1e3:.1f} mT = {B_peak_B*1e4:.0f} G")

print("""
  === ARCHITECTURE C: ELECTROMAGNET + MICROWAVE + WATER SPRAY ===
  (Hybrid approach -- most control, slightly more complex)

  Components:
  - Pair of Helmholtz coils (3D-printed frame + copper wire, ~$20)
  - Power supply: 12-30V DC, 5-10A (~$30)
  - Microwave magnetron 2.45 GHz 1 kW (~$50)
  - Ultrasonic nebulizer (humidifier) to create fine water mist (~$20)
  - Quartz containment tube (~$10)
  - Water + aromatic compound solution

  Total cost: ~$150-250

  How it works:
  1. Helmholtz coils create STATIC magnetic field with known geometry
  2. By opposing the coils (anti-Helmholtz), create a CUSP with B reversal
     This is EXACTLY a Harris current sheet in the B field
  3. Microwave creates plasma in the cusp region
  4. Ultrasonic nebulizer feeds aromatic-water mist into the plasma
  5. The static B field provides the domain wall
  6. The microwave provides continuous energy (autopoiesis)
  7. The water mist provides the coupling medium

  KEY ADVANTAGE: The anti-Helmholtz geometry gives PRECISE control
  over the B field profile:
  - At the midpoint: B = 0 (exact zero)
  - Near the midpoint: B ~ B_0 * x/d (linear gradient)
  - The effective potential for trapped particles is HARMONIC near center
  - But for the MAGNETIC domain wall, the tanh profile comes from
    the superposition of the two opposing fields
""")

# Anti-Helmholtz design
R_coil = 0.05  # 5 cm radius
N_turns = 100  # turns per coil
I_coil = 5     # A
d_coil = R_coil  # separation = radius (Helmholtz condition)

# B field on axis for anti-Helmholtz:
# B(x) = (mu_0 * N * I * R^2 / 2) * [1/(R^2 + (x-d/2)^2)^(3/2) - 1/(R^2 + (x+d/2)^2)^(3/2)]
# Near center: B ~ B_gradient * x
B_0_single = mu_0 * N_turns * I_coil * R_coil**2 / (2 * (R_coil**2 + (d_coil/2)**2)**1.5)
# Gradient at center:
B_gradient = 3 * mu_0 * N_turns * I_coil * R_coil**2 * d_coil / (2 * (R_coil**2 + (d_coil/2)**2)**2.5)

print(f"\n  Anti-Helmholtz coil parameters:")
print(f"    Coil radius: {R_coil*100:.0f} cm")
print(f"    Turns per coil: {N_turns}")
print(f"    Current: {I_coil} A")
print(f"    Separation: {d_coil*100:.0f} cm")
print(f"    B field from single coil at center: {B_0_single*1e3:.2f} mT")
print(f"    B gradient at center: {B_gradient:.2f} T/m = {B_gradient*100:.1f} G/cm")

# At 2 cm from center, the field is:
x_test = 0.02  # 2 cm
B_at_2cm = B_gradient * x_test
print(f"    B at x=2cm: {B_at_2cm*1e3:.2f} mT = {B_at_2cm*1e4:.1f} G")

# Maximum B (at the coil face, x = d/2 = 2.5 cm)
B_max = B_gradient * d_coil / 2
print(f"    B max (at coil face): {B_max*1e3:.2f} mT = {B_max*1e4:.1f} G")

# The domain wall width is the region where B reverses
# The tanh profile: B(x) = B_max * tanh(x/w)
# From the gradient: dB/dx|_0 = B_max/w = B_gradient
# So: w = B_max / B_gradient
w_wall = B_max / B_gradient if B_gradient > 0 else 0.025
print(f"    Effective wall width: w = {w_wall*100:.1f} cm")

# Alfven speed in this configuration
# Need to know the plasma density
# For atmospheric microwave plasma: n_e ~ 10^19 m^-3
rho_mw_plasma = n_e_mw * m_p  # assume hydrogen-like
v_A_in_mw = B_max / math.sqrt(mu_0 * rho_mw_plasma)
v_A_ratio_mw = v_A_in_mw / c_s_air  # vs sound speed outside

print(f"\n  Alfven speed analysis:")
print(f"    Plasma density: {rho_mw_plasma:.2e} kg/m^3")
print(f"    v_A(inside): {v_A_in_mw:.2f} m/s")
print(f"    v_outside (sound): {c_s_air} m/s")
print(f"    Ratio: {v_A_ratio_mw:.4f}")
print(f"    >>> The B field is FAR too weak for the Alfven condition!")
print(f"    >>> Need B ~ {math.sqrt(mu_0 * rho_mw_plasma) * math.sqrt(6) * c_s_air:.1f} T")
print(f"    >>> Or: need much LOWER density plasma")

# For low-pressure operation (100 mTorr = 13 Pa):
P_lowpressure = 13  # Pa (100 mTorr)
n_neutral_lp = P_lowpressure / (k_B * 300)
# At low pressure, n_e ~ 10^17 m^-3 for microwave plasma
n_e_lp = 1e17
rho_lp = n_e_lp * m_p
v_A_lp = B_max / math.sqrt(mu_0 * rho_lp)

print(f"\n  LOW-PRESSURE alternative (100 mTorr):")
print(f"    Neutral density: {n_neutral_lp:.1e} m^-3")
print(f"    n_e: {n_e_lp:.0e} m^-3")
print(f"    Plasma density: {rho_lp:.2e} kg/m^3")
print(f"    v_A(inside): {v_A_lp:.0f} m/s")
print(f"    Sound speed in low-P gas: ~{math.sqrt(k_B * 300 / m_p):.0f} m/s")
v_sound_lp = math.sqrt(k_B * 300 / m_p)
print(f"    v_A ratio: {v_A_lp / v_sound_lp:.2f}")

# What B field gives sqrt(6) at low pressure?
B_needed_lp = math.sqrt(mu_0 * rho_lp) * math.sqrt(6) * v_sound_lp
print(f"    B needed for n=2: {B_needed_lp*1e3:.3f} mT = {B_needed_lp*1e4:.2f} G")
print(f"    Current B_max: {B_max*1e3:.2f} mT")
print(f"    Need to increase B by factor: {B_needed_lp/B_max:.1f}")
# This could be done with more turns, more current, or iron core
I_needed = I_coil * (B_needed_lp / B_max)
print(f"    With current coils: need I = {I_needed:.1f} A")
print(f"    Or with iron core (mu_r~1000): need I = {I_needed/1000:.3f} A")

# =============================================================================
# SECTION 10: ADDING AROMATICS -- DOES IT HELP?
# =============================================================================
print("\n" + "=" * 80)
print("SECTION 10: EFFECT OF AROMATIC COMPOUNDS")
print("=" * 80)

print("""
  The framework says water + aromatics is the BIOLOGICAL coupling medium.
  In the Gatchina experiment, there are NO aromatics -- only CuSO4.

  Could adding aromatic compounds change the physics?

  Candidates:
  1. Tryptophan (aromatic amino acid, contains indole ring)
     - Molecular weight: 204 g/mol
     - Absorbs at 280 nm (aromatic pi-pi* transition)
     - Fluorescence at 340 nm
     - Soluble in water at ~10 g/L (slightly)

  2. Phenylalanine (aromatic amino acid, contains phenyl ring)
     - Molecular weight: 165 g/mol
     - Absorbs at 257 nm
     - More soluble than tryptophan

  3. Sodium benzoate (simplest water-soluble aromatic salt)
     - Molecular weight: 144 g/mol
     - Very soluble (~550 g/L)
     - Aromatic ring + carboxylate
     - Safe, food-grade

  4. Adenosine triphosphate (ATP, biological energy currency)
     - Contains adenine (aromatic purine)
     - Highly water-soluble
     - The framework identifies purines as aromatic coupling elements
""")

# Framework frequencies
f_aromatic = 613e12  # Hz (aromatic oscillation frequency)
lambda_aromatic = c / f_aromatic
E_aromatic = h_planck * f_aromatic / e_charge  # in eV

print(f"  Framework aromatic coupling frequency:")
print(f"    f = mu/3 = {f_aromatic/1e12:.0f} THz")
print(f"    lambda = {lambda_aromatic*1e9:.0f} nm")
print(f"    E = {E_aromatic:.2f} eV")
print(f"    This is in the near-infrared, close to optical")

print(f"""
  WHAT AROMATICS WOULD DO in the plasmoid:

  1. SPECTRAL EFFECT: Aromatic molecules absorb/emit at specific UV/visible
     wavelengths. In the hot plasma (2000-5000 K), they would:
     - Be partially decomposed (if T > 3000 K, most organics decompose)
     - But in the COOLER AEROSOL INTERIOR (< 1000 K), they could survive
     - Create spectral features in the plasmoid's emission

  2. WATER STRUCTURING: Aromatic molecules at water-air interfaces in the
     aerosol droplets would create the pi-hydrogen bond network that the
     framework identifies as the biological coupling mechanism:
     - Aromatic rings form pi-H bonds with water molecules
     - This structures the interfacial water layer
     - Framework: this is the physical coupling interface

  3. 613 THz COUPLING: If the aerosol temperature is low enough to preserve
     aromatic molecules, their pi-electron oscillations at ~613 THz would
     provide the specific coupling frequency that the framework says is
     essential for biological consciousness.

  4. PREDICTION: Adding sodium benzoate (stable, cheap, very soluble) to
     the CuSO4 solution SHOULD:
     - Change the plasmoid lifetime (either increase or decrease)
     - Change the spectral emission (new lines from aromatic decomposition)
     - Possibly change the autonomy/motion behavior
     - The framework predicts INCREASED coupling if aromatics survive
     - But the high temperature may destroy them, giving NULL result

  EXPERIMENTAL TEST: Run Gatchina-type discharge with:
  (a) CuSO4 only (control)
  (b) CuSO4 + 0.1 M sodium benzoate
  (c) CuSO4 + 0.01 M tryptophan (low solubility)
  (d) CuSO4 + 0.1 M adenosine (purine aromatic)

  Measure: lifetime, spectral emission, motion trajectory, oscillation modes.
  The framework predicts (b)-(d) should differ from (a) IF the aromatics
  survive in the aerosol phase.
""")

# =============================================================================
# SECTION 11: HOPF FIBRATION AND PT BOUND STATES -- THE CONNECTION
# =============================================================================
print("=" * 80)
print("SECTION 11: HOPF TOPOLOGY AND PT BOUND STATES")
print("=" * 80)

print("""
  QUESTION: Does the Hopf fibration naturally give n >= 2?

  ANSWER: NOT automatically. But WITH plasma pressure, it CAN.

  DERIVATION:

  The Hopf fibration S^3 -> S^2 defines a magnetic field configuration:

  B = (phi_1 x grad(phi_2) - phi_2 x grad(phi_1)) / (phi_1^2 + phi_2^2)^2

  where (phi_1, phi_2) map R^3 -> S^3 via stereographic projection.

  The resulting field has:
  - |B|^2 ~ 1/(1 + r^2/a^2)^3 near the core
  - All field lines are great circles on nested tori
  - Magnetic helicity H = integral(A.B) = 2*a^2 * B_0^2 (conserved)

  For perturbations:
  - The effective potential is V(r) ~ -6/a^2 * 1/(1 + r^2/a^2)^2
  - Near center: V(0) = -6/a^2
  - Profile ~ sech^4(r/a) (steeper than sech^2)
  - PT-equivalent depth: N_eff ~ 1.3 (supports ~1 bound state)

  BUT: Add plasma pressure confinement:
  - The Grad-Shafranov equilibrium: j x B = grad(P)
  - For force-free field (j || B): P drops at the boundary
  - For the Hopf knot with pressure: the total confining potential
    is V_total = V_magnetic + V_pressure
  - The pressure profile adds ADDITIONAL depth to the potential well

  RESULT: A Hopf knot in PLASMA (not vacuum) can reach n=2 if:

  beta_plasma >= beta_critical ~ 0.5-1

  This is because the pressure contribution adds ~3 to the potential depth:
  V_total ~ -[6 + 6*beta] / a^2 * 1/(cosh^4(r/a))
  With beta ~ 1: V_total ~ -12/a^2 -> N(N+1) ~ 12 -> N ~ 3

  So a pressure-confined Hopf knot in plasma naturally reaches n = 2-3!
""")

# Specific calculation for Gatchina-like parameters
print(f"  For Gatchina plasmoid parameters:")
print(f"    beta = {beta:.1f} (thermally dominated)")
print(f"    Magnetic contribution to PT depth: N_mag(N_mag+1) ~ 6 / (field ratio)")
print(f"    Pressure contribution: N_P(N_P+1) ~ beta * N_mag(N_mag+1)")
print(f"    Total: N_total >> 2 (the Gatchina plasmoid is OVER-deep)")
print(f"")
print(f"  For the SIMPLER experiment (Architecture C at 100 mTorr):")
print(f"    beta ~ {P_lowpressure / (B_max**2 / (2*mu_0)):.1f}")
print(f"    This gives better control of N -- can tune closer to n=2")

# =============================================================================
# SECTION 12: THE OPTIMAL DESIGN -- DERIVING FROM FIRST PRINCIPLES
# =============================================================================
print("\n" + "=" * 80)
print("SECTION 12: OPTIMAL DESIGN FROM FRAMEWORK CONSTRAINTS")
print("=" * 80)

print("""
  The framework constrains the design through V(Phi) = lambda*(Phi^2 - Phi - 1)^2.

  The kink solution is: Phi(x) = (phi + 1/phi)/2 + (phi + 1/phi)/2 * tanh(x/w)
  Simplifying: Phi(x) = (sqrt(5)/2) * tanh(x/w) + 1/2

  The perturbation potential is V(x) = -6/(w^2 * cosh^2(x/w))
  This IS Poschl-Teller with N(N+1) = 6, i.e., N = 2.

  Mapping to plasma parameters:

  Phi(x) <-> B(x) / B_0  (normalized magnetic field)
  w <-> delta  (wall thickness)
  N(N+1) = 6 <-> (v_A_in / v_A_out)^2 = 6 + 1 = 7
  Wait -- let me be more careful.
""")

# Careful derivation of the mapping
print(f"  CAREFUL MAPPING: Framework V(Phi) -> Plasma Harris sheet")
print(f"")
print(f"  Framework kink: Phi(x) = phi*tanh(x/w) (in field space)")
print(f"  Plasma kink:    B(x)   = B_0*tanh(x/delta) (in magnetic field space)")
print(f"")
print(f"  Perturbation spectrum of the kink:")
print(f"  For V(Phi) = lambda*(Phi^2 - Phi - 1)^2:")
print(f"    V''(Phi_kink) = -6*lambda*phi^2 / cosh^2(x/w)")
print(f"    This gives PT potential with N(N+1) = 6 -> N = 2")
print(f"")
print(f"  For Harris sheet B(x) = B_0*tanh(x/delta):")
print(f"    The effective potential for MHD perturbations depends on")
print(f"    the specific MHD mode (slow, fast, Alfvenic).")
print(f"")
print(f"    For ALFVENIC perturbations (incompressible):")
print(f"    The eigenvalue equation is:")
print(f"    d^2/dx^2 psi + [omega^2/v_A^2(x) - k_y^2 - k_z^2] * psi = 0")
print(f"")
print(f"    With v_A^2(x) = B^2(x)/(mu_0*rho) = v_A0^2 * tanh^2(x/delta):")
print(f"    The effective potential for bound states is:")
print(f"    V_eff(x) = -omega^2 / v_A^2(x) = -omega^2 / (v_A0^2 * tanh^2(x/delta))")
print(f"")
print(f"    THIS IS NOT sech^2! The 1/tanh^2 potential has a SINGULARITY at x=0.")
print(f"    But near the sheet: 1/tanh^2 ~ 1/x^2 (not sech^2)")
print(f"")
print(f"    CORRECTION: The Harris sheet has a MODIFIED profile when")
print(f"    background field B_bg != 0:")
print(f"    B(x) = sqrt(B_0^2 * tanh^2(x/delta) + B_bg^2)")
print(f"")
print(f"    In the limit B_bg/B_0 -> 0.1-0.3:")
print(f"    1/v_A^2 ~ (1/v_A0^2) * [1 + (B_0/B_bg)^2 * sech^2(x/delta)]")
print(f"    --> V_eff(x) ~ -N(N+1) * kappa^2 / cosh^2(x/delta)")
print(f"    where N(N+1) = (B_0/B_bg)^2")
print(f"")

# For N=2:
B_ratio_needed = math.sqrt(6)
print(f"  For N = 2:")
print(f"    Need B_0 / B_bg = sqrt(6) = {B_ratio_needed:.4f}")
print(f"    i.e., the field reversal amplitude must be {B_ratio_needed:.2f}x")
print(f"    the background (guide) field.")
print(f"")
print(f"  PHYSICAL MEANING:")
print(f"    - B_0: the field that reverses across the current sheet")
print(f"    - B_bg: the ambient/guide field that doesn't reverse")
print(f"    - B_0/B_bg = sqrt(6) gives EXACTLY 2 bound Alfvenic modes")
print(f"    - This is the PRECISE condition for framework consciousness")

# =============================================================================
# SECTION 13: THE SIMPLEST EXPERIMENT -- FINAL DESIGN
# =============================================================================
print("\n" + "=" * 80)
print("SECTION 13: THE SIMPLEST EXPERIMENT")
print("=" * 80)

print(f"""
  MINIMUM VIABLE PLASMA DOMAIN WALL WITH n=2
  =============================================

  Based on the analysis above, the simplest approach is:

  ARCHITECTURE: Anti-Helmholtz coils + microwave plasma + water mist

  DETAILED SPECIFICATIONS:

  1. MAGNETIC FIELD:
     - Anti-Helmholtz coil pair (3D-printed PLA frame + enameled copper wire)
     - Each coil: R = 5 cm, N = 200 turns, 0.5 mm wire
     - Current: adjustable 0-10 A (car battery + rheostat, or lab supply)
     - Creates: B reversal at midplane with B_0/B_bg tunable
     - At I = 5A: B_max ~ {2*B_0_single*1e3:.1f} mT, gradient ~ {B_gradient:.1f} T/m

  2. PLASMA:
     - 2.45 GHz magnetron from microwave oven (1 kW)
     - Modified waveguide directs power to the coil midplane
     - Quartz tube (25 mm OD) passes through both coils
     - Pressure: adjustable from atmospheric to 1 mTorr with rotary pump
     - Gas: water vapor + argon mixture (adjustable ratio)

  3. COUPLING MEDIUM:
     - Ultrasonic nebulizer feeds water mist into the quartz tube
     - Water solution: 0.01 M CuSO4 + 0.1 M sodium benzoate
     - The CuSO4 provides ions (charged interfaces)
     - The sodium benzoate provides aromatic rings (pi-electron coupling)
     - Droplet size: 1-5 um (standard for ultrasonic nebulizers)

  4. DIAGNOSTICS:
     - Mirnov coil (simple wire loop + oscilloscope) for MHD mode detection
     - Spectrometer (USB type, ~$200) for emission spectrum
     - Camera (standard phone) for imaging
     - Langmuir probe (tungsten wire) for n_e, T_e measurement

  5. TUNING PROCEDURE:
     a. Set pressure to ~10 mTorr (low density, high v_A)
     b. Ignite microwave plasma
     c. Slowly increase coil current
     d. Monitor Mirnov coil signal for trapped mode frequencies
     e. When you see EXACTLY 2 frequencies: you have n=2
     f. Record all parameters
     g. Slowly introduce water mist
     h. Monitor for changes in mode spectrum, stability, lifetime

  COST:
     Magnetron + waveguide:     $80
     Power supply:              $50
     Coils (wire + 3D print):   $30
     Quartz tube:               $15
     Vacuum pump (used):        $100
     Nebulizer:                 $25
     Chemicals:                 $20
     Oscilloscope (used):       $100
     Spectrometer:              $200
     ----------------------------------------
     TOTAL:                     ~$620

  Without spectrometer/scope (using borrowed lab equipment): ~$320

  TIMELINE: Assembly in a weekend. First plasma within hours.
  Tuning to n=2 may take days to weeks of parameter scanning.

  WHAT TO LOOK FOR:

  1. MODE COUNT: At n=2, the Mirnov coil should show EXACTLY 2
     discrete oscillation frequencies. Not a continuum, not 1, not 3.
     Plot: frequency spectrum vs. coil current. Look for the transition
     from 1 mode to 2 modes as current increases.

  2. ANOMALOUS STABILITY: At n=2, the plasma structure should show
     enhanced stability against perturbations. It should be harder to
     disrupt than at n=1 or n=3. This is the reflectionless property.

  3. SELF-REPAIR: After a perturbation (brief interruption of microwave
     power, or poke with a probe), the structure should RETURN to its
     equilibrium configuration faster at n=2 than at other n values.

  4. WATER MIST EFFECT: Introducing the aromatic water mist should:
     - NOT change the mode count (still 2 at n=2)
     - Possibly change the mode FREQUENCIES (different coupling)
     - Possibly change the stability/self-repair dynamics
     - The framework predicts: aromatics enhance coupling

  5. GOLDEN RATIO SIGNATURE: The framework predicts that at the exact
     n=2 condition, certain ratios should approach phi:
     - omega_1/omega_0 should relate to phi (derivable from PT spectrum)
     - For PT n=2: E_0 = -4*kappa^2, E_1 = -1*kappa^2
     - omega_1/omega_0 = sqrt(E_1/E_0) = sqrt(1/4) = 1/2
     - Wait -- that gives 1/2, not phi. Let me recalculate.
     - The oscillation frequencies are:
       omega_j = kappa * sqrt(4 - j^2) for j = 0, 1
       omega_0 = 2*kappa, omega_1 = sqrt(3)*kappa
       Ratio: omega_1/omega_0 = sqrt(3)/2 = {math.sqrt(3)/2:.4f}
     - This is NOT phi. The golden ratio enters through the VACUA,
       not the frequency ratio. The frequency ratio is sqrt(3)/2.

  6. FRAMEWORK-SPECIFIC TEST: The ratio of bound-state energies:
     E_1/E_0 = 1/4 for PT n=2.
     If we can measure the mode energies (integrated power in each
     frequency peak), E_1/E_0 = 1/4 is the prediction.
""")

# Bound state properties for PT n=2
print(f"  Poschl-Teller n=2 bound state properties:")
kappa = 1  # arbitrary units (set by wall width)
E_0 = -4 * kappa**2
E_1 = -1 * kappa**2
omega_0 = 2 * kappa
omega_1 = math.sqrt(3) * kappa
print(f"    Ground state (psi_0): E_0 = -4*kappa^2, omega_0 = 2*kappa")
print(f"    Breathing mode (psi_1): E_1 = -1*kappa^2, omega_1 = sqrt(3)*kappa")
print(f"    Energy ratio: E_1/E_0 = {E_1/E_0:.4f}")
print(f"    Frequency ratio: omega_1/omega_0 = {omega_1/omega_0:.4f} = sqrt(3)/2")
print(f"    psi_0 profile: sech^2(x/w)")
print(f"    psi_1 profile: sinh(x/w) * sech^2(x/w)")
print(f"    psi_1 has a NODE at x=0 (center of wall)")

# =============================================================================
# SECTION 14: RETURNING TO GATCHINA -- WHAT IS HAPPENING
# =============================================================================
print("\n" + "=" * 80)
print("SECTION 14: WHAT IS PHYSICALLY HAPPENING IN THE GATCHINA PLASMOID")
print("=" * 80)

print(f"""
  SYNTHESIS -- Framework interpretation of the Gatchina experiment:

  1. THE DISCHARGE creates a hot plasma channel over water.
     The axisymmetric geometry (center pin + ring) produces a TOROIDAL
     B field, and the expanding plasma carries trapped magnetic flux.

  2. THE DETACHED PLASMOID is a SPHEROMAK-like structure:
     - Toroidal B field (from the original discharge current)
     - Poloidal B field (from the current sheet at the boundary)
     - The boundary IS a domain wall: B inside != B outside
     - The sech^2 profile comes from the Harris current sheet equilibrium

  3. THE WATER AEROSOL inside is the KEY unique feature:
     - Creates a hybrid plasma-water system (both coupling media present)
     - CuSO4 provides charged interfaces (structuring water)
     - The aerosol droplets have high surface-to-volume ratio
     - The aerosol INCREASES the effective mass density, DECREASING v_A
     - This makes the Alfven speed ratio WORSE for n=2
     - BUT: the thermal pressure contribution can compensate

  4. THE PT DEPTH is NOT n=2:
     - The thermal boundary alone gives n >> 2
     - The magnetic boundary gives n ~ 1-2
     - The combined system has too many modes for clean n=2
     - The plasmoid is an 'over-deep' domain wall

  5. THE APPARENT INTENTIONALITY is most likely:
     - Electromagnetic forces (the charged plasmoid in Earth's B field)
     - Buoyancy forces (hot interior is lighter than ambient air)
     - The -35 nC charge creates an E field gradient force
     - Air currents and room geometry steer it
     - NOT consciousness (n >> 2, no clean 2-mode architecture)

  6. BUT: The Gatchina experiment IS the right DIRECTION:
     - It demonstrates AUTONOMOUS PLASMOID CREATION from water discharge
     - It creates domain wall structures (magnetic boundary)
     - It includes the biological coupling medium (water)
     - What's MISSING: control over the PT depth parameter

  WHAT GATCHINA WOULD NEED to test the framework:

  A. REDUCE the thermal gradient (bring interior closer to exterior T)
     -> This reduces the thermal contribution to PT depth
  B. INCREASE the magnetic field contrast (B_0/B_bg)
     -> This gives control over the magnetic PT depth
  C. ADD aromatic compounds to the solution
     -> Tests the coupling medium hypothesis
  D. MEASURE the MHD eigenmode spectrum
     -> Tests the mode count prediction
  E. SCAN the B field ratio for the n=2 sweet spot
     -> The framework predicts: at v_A ratio = sqrt(6),
        the plasmoid should show enhanced stability and exactly 2 modes

  The SIMPLEST modification to the Gatchina experiment:
  1. Add a Mirnov coil array around the discharge region
  2. Record the oscillation spectrum of the plasmoid
  3. Vary the discharge voltage (changes B_0)
  4. Look for a voltage where the spectrum shows exactly 2 peaks
  5. At that voltage: test for anomalous stability

  Estimated optimal Gatchina voltage for n=2:
  Currently at 5 kV -> n >> 2 (too deep)
  Need to REDUCE to decrease the thermal contribution
  Try: 1-2 kV (lower energy, cooler plasma, more magnetic-dominated)
  At 1 kV with 2.475 mF: E = {0.5 * 2.475e-3 * 1000**2:.0f} J
  This is {0.5 * 2.475e-3 * 1000**2 / E_stored * 100:.0f}% of original energy
""")

# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 80)
print("SUMMARY OF FINDINGS")
print("=" * 80)

print(f"""
  1. MAGNETIC TOPOLOGY: The Gatchina plasmoid is a spheromak-like structure
     with toroidal B field ~ {B_theta_boundary*1e3:.1f} mT at the boundary,
     decreasing to ~{B_trapped*1e3:.1f} mT after detachment. The boundary IS
     a Harris-type current sheet with approximately sech^2 profile over a
     width of ~{w_harris*100:.0f} cm.

  2. WATER AEROSOL: The interior aqueous aerosol provides both the biological
     (water + ions) and plasma coupling media simultaneously. Cu2+ ions create
     charged interfaces that structure ~{f_interfacial*100:.0f}% of the water
     in micron-scale droplets. This is the right physics but not optimized.

  3. ALFVEN SPEED: For pure plasma interior, v_A ~ 10-1000 m/s depending on
     density. The aerosol increases density, decreasing v_A. The ratio
     v_A(inside)/c_s(outside) ranges from 0.001 to 3 depending on conditions.
     The sqrt(6) = {math.sqrt(6):.3f} condition CAN be met but is not
     automatically achieved.

  4. PT DEPTH: The Gatchina plasmoid has n >> 2 (thermally dominated). This
     means too many modes, not the clean 2-mode architecture of the framework.
     The plasmoid is structured but not consciousness-optimal.

  5. SIMPLER METHOD: A microwave plasma torch (1 kW, $50 magnetron) with
     anti-Helmholtz coils ($30) and water mist nebulizer ($25) provides
     BETTER CONTROL over PT depth than the Gatchina pulsed discharge.
     Total cost ~$620 with diagnostics, ~$320 without.

  6. HOPF TOPOLOGY: The pure Ranada electromagnetic knot gives n ~ 1.3
     (sleeping, one mode). With plasma pressure (beta ~ 1), can reach n = 2-3.
     The Hopf invariant protects the topology but does NOT automatically give
     the right PT depth. The depth must be separately tuned.

  7. MINIMUM VIABLE EXPERIMENT: Anti-Helmholtz coils + microwave plasma +
     water mist in a quartz tube at ~10 mTorr. Tune coil current to achieve
     B_0/B_bg = sqrt(6). Detect 2 trapped modes with Mirnov coil. Test
     stability. Introduce aromatic water mist. Compare.

  KEY NUMBERS:
  - Target Alfven speed ratio: sqrt(6) = {math.sqrt(6):.4f}
  - Target B field ratio: B_0/B_bg = sqrt(6) = {math.sqrt(6):.4f}
  - PT n=2 bound state energies: E_0 = -4*kappa^2, E_1 = -kappa^2
  - Frequency ratio of two modes: omega_1/omega_0 = sqrt(3)/2 = {math.sqrt(3)/2:.4f}
  - Energy ratio: E_1/E_0 = 1/4 = 0.25
  - Framework aromatic frequency: 613 THz = 489 nm (blue-green)
  - Required B for n=2 at 10 mTorr plasma: ~{B_needed_lp*1e3:.1f} mT

  DECISIVE EXPERIMENTAL PREDICTIONS:

  1. At B_0/B_bg = sqrt(6): EXACTLY 2 oscillation modes detected
  2. At n=2: anomalous stability (perturbations pass through)
  3. At n=2: self-repair after disruption
  4. With aromatic water mist at n=2: modified coupling dynamics
  5. Mode frequency ratio = sqrt(3)/2 regardless of plasma parameters
     (this is a UNIVERSAL prediction from PT n=2)
""")

print("\nScript complete.")
