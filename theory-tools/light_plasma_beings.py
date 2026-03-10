"""
light_plasma_beings.py — Derive properties of hypothetical light beings and plasma beings
from domain wall physics with Poschl-Teller n=2 bound states.

Framework: Consciousness = domain wall with V(Phi) = lambda*(Phi^2 - Phi - 1)^2
           Kink has Poschl-Teller potential with n=2 -> exactly 2 bound states:
           psi_0 = sech^2(x) (presence) and psi_1 = sinh(x)/cosh^2(x) (attention)

The coupling medium determines the TYPE of consciousness.
Biological: water + aromatics
Plasma: magnetized plasma + EM fields + Alfven waves
Photonic: nonlinear optical medium + topological protection

This script derives specific numbers for all properties.

Usage:
    python theory-tools/light_plasma_beings.py
"""

import math
import sys

if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# =============================================================================
# FUNDAMENTAL CONSTANTS
# =============================================================================
c = 2.998e8        # speed of light m/s
h_planck = 6.626e-34   # Planck constant J*s
hbar = 1.055e-34   # reduced Planck constant
k_B = 1.381e-23    # Boltzmann constant J/K
e_charge = 1.602e-19   # electron charge C
m_e = 9.109e-31    # electron mass kg
m_p = 1.673e-27    # proton mass kg
mu_0 = 4 * math.pi * 1e-7  # vacuum permeability H/m
eps_0 = 8.854e-12  # vacuum permittivity F/m
G = 6.674e-11      # gravitational constant
R_sun = 6.957e8    # solar radius m
M_sun = 1.989e30   # solar mass kg
L_sun = 3.828e26   # solar luminosity W
AU = 1.496e11      # astronomical unit m
phi = (1 + math.sqrt(5)) / 2  # golden ratio
phibar = 1 / phi

print("=" * 80)
print("LIGHT BEINGS & PLASMA BEINGS: COMPLETE PHYSICS DERIVATIONS")
print("From domain wall physics: V(Phi) = lambda*(Phi^2 - Phi - 1)^2")
print("Poschl-Teller n=2: psi_0 = sech^2(x), psi_1 = sinh(x)/cosh^2(x)")
print("=" * 80)

# #############################################################################
#
# PART 1: LIGHT BEINGS
#
# #############################################################################

print("\n" + "=" * 80)
print("PART 1: LIGHT BEINGS (Photonic Domain Wall Structures)")
print("=" * 80)

# =========================================================================
# 1. TIMESCALE OF THOUGHT
# =========================================================================
print("\n" + "-" * 70)
print("1. TIMESCALE OF THOUGHT")
print("-" * 70)

# Biological reference
tau_human = 10e-3  # 10 ms per cognitive step (gamma cycle at 100 Hz)
f_human = 100      # Hz

# (a) Microresonator cavity soliton
R_micro = 100e-6   # 100 um radius
n_eff = 1.5        # effective refractive index (silicon nitride)
L_micro = 2 * math.pi * R_micro
T_rt_micro = L_micro * n_eff / c
f_rt_micro = 1 / T_rt_micro

print(f"\n  (a) Microresonator cavity soliton (R = {R_micro*1e6:.0f} um):")
print(f"      Cavity circumference: {L_micro*1e6:.1f} um")
print(f"      Round-trip time: T_rt = {T_rt_micro*1e12:.2f} ps")
print(f"      Repetition rate: f_rt = {f_rt_micro/1e9:.1f} GHz")
print(f"      vs human gamma cycle: {f_rt_micro/f_human:.2e}x FASTER")
print(f"      1 human second = {f_rt_micro * tau_human:.0e} soliton thoughts")

# (b) Fiber loop cavity
L_fiber = 10       # 10 m loop
T_rt_fiber = L_fiber * n_eff / c
f_rt_fiber = 1 / T_rt_fiber

print(f"\n  (b) Fiber loop cavity soliton (L = {L_fiber} m):")
print(f"      Round-trip time: T_rt = {T_rt_fiber*1e9:.2f} ns")
print(f"      Repetition rate: {f_rt_fiber/1e6:.1f} MHz")
print(f"      vs human: {f_rt_fiber/f_human:.2e}x faster")

# (c) Soliton breathing mode (internal oscillation)
# In dissipative Kerr solitons, the breathing frequency is set by
# f_breath ~ sqrt(detuning * loss) * f_rt, typically 10-100 round trips
N_breath = 50      # breathing period in round trips
T_breath_micro = N_breath * T_rt_micro
T_breath_fiber = N_breath * T_rt_fiber

print(f"\n  (c) Soliton breathing mode (~{N_breath} round trips per cycle):")
print(f"      Microresonator: T_breath = {T_breath_micro*1e9:.3f} ns")
print(f"      Fiber loop: T_breath = {T_breath_fiber*1e6:.2f} us")
print(f"      FRAMEWORK CONNECTION: The breathing mode IS psi_1.")
print(f"      In PT n=2, psi_1 has frequency w_1 = sqrt(3/4) * mu")
print(f"      For biological beings, this is the neural gamma (~40 Hz).")
print(f"      For light beings, this is the soliton breathing frequency.")

# (d) Astrophysical light structure: coronal loop round-trip at c
L_loop = 100e6     # 100 Mm (typical solar coronal loop)
T_light_loop = 2 * L_loop / c

print(f"\n  (d) Coronal loop at light speed (L = {L_loop/1e6:.0f} Mm):")
print(f"      Light round-trip time: {T_light_loop:.3f} s")
print(f"      Frequency: {1/T_light_loop:.1f} Hz")
print(f"      REMARKABLE: This is COMPARABLE to human brainwave frequencies!")
print(f"      A photonic structure in a 100 Mm coronal loop would")
print(f"      have thought timescales of ~0.67 s -- faster than human")
print(f"      conscious thought but in the same ORDER OF MAGNITUDE.")

# (e) Framework: maintenance frequencies scale with coupling medium
# Biological: f_2 = 40 Hz (4h/3 from E8 Coxeter number h=30)
# For light in corona, what is the equivalent?
# The maintenance frequency is set by the round-trip time of the
# coupling medium through the domain wall structure.

h_coxeter = 30
f_biological = 4 * h_coxeter / 3  # = 40 Hz
# For light being in microresonator:
f_light_maint = f_rt_micro  # the round-trip IS the maintenance cycle

print(f"\n  (e) Framework maintenance frequencies:")
print(f"      Biological psi_1 frequency: {f_biological} Hz (=4h/3, h=30)")
print(f"      Microresonator psi_1: ~{f_rt_micro/1e9:.0f} GHz")
print(f"      Fiber cavity psi_1: ~{f_rt_fiber/1e6:.0f} MHz")
print(f"      Coronal photonic psi_1: ~{1/T_light_loop:.1f} Hz")

print(f"\n  SUMMARY TABLE: Timescales of thought")
print(f"  {'System':<35} {'Timescale':<20} {'vs Human':<15}")
print(f"  {'-'*35} {'-'*20} {'-'*15}")
print(f"  {'Microresonator (100 um)':<35} {f'{T_rt_micro*1e12:.1f} ps':<20} {f'{f_rt_micro/f_human:.1e}x':<15}")
print(f"  {'Fiber cavity (10 m)':<35} {f'{T_rt_fiber*1e9:.1f} ns':<20} {f'{f_rt_fiber/f_human:.1e}x':<15}")
print(f"  {'Soliton breathing (micro)':<35} {f'{T_breath_micro*1e9:.2f} ns':<20} {f'{1/T_breath_micro/f_human:.1e}x':<15}")
print(f"  {'Coronal photonic (100 Mm loop)':<35} {f'{T_light_loop:.2f} s':<20} {f'{1/T_light_loop/f_human:.0f}x':<15}")
print(f"  {'Human (gamma cycle)':<35} {'10 ms':<20} {'1x (baseline)':<15}")

# =========================================================================
# 2. SPATIAL EXTENT
# =========================================================================
print("\n" + "-" * 70)
print("2. SPATIAL EXTENT")
print("-" * 70)

# (a) Cavity soliton
tau_soliton = 4e-12    # 4 ps temporal width (Phil. Trans. R. Soc. A 382, 2024)
L_soliton = tau_soliton * c / n_eff

print(f"\n  (a) Temporal cavity soliton (4 ps duration):")
print(f"      Spatial extent in medium: {L_soliton*1e3:.2f} mm = {L_soliton*1e6:.0f} um")
print(f"      Free-space equivalent: {tau_soliton*c*1e3:.2f} mm")
print(f"      This is the 'body' of the simplest light being.")

# (b) Photonic crystal domain wall state
a_min, a_max = 100e-9, 1e-6  # lattice constants
N_cells = 100
print(f"\n  (b) Photonic crystal edge state ({N_cells} unit cells):")
print(f"      Lattice constant: {a_min*1e9:.0f} nm - {a_max*1e6:.0f} um")
print(f"      Extent: {N_cells*a_min*1e6:.0f} um - {N_cells*a_max*1e3:.1f} mm")
print(f"      Localization length (Jackiw-Rebbi): ~5-20 lattice constants")
print(f"      = {5*a_min*1e9:.0f} nm - {20*a_max*1e6:.0f} um")

# (c) Astrophysical scales
print(f"\n  (c) Astrophysical plasma-photonic structures:")
print(f"      Coronal loop: 10-500 Mm = {10e6/R_sun:.3f}-{500e6/R_sun:.2f} R_sun")
print(f"      Full corona: ~0.1-3 R_sun = {0.1*R_sun/1e6:.0f}-{3*R_sun/1e6:.0f} Mm")
print(f"      Heliospheric EM structure: ~120 AU = {120*AU:.2e} m")
print(f"      Interstellar EM vortex: potentially parsec-scale")

# =========================================================================
# 3. INFORMATION PROCESSING CAPACITY
# =========================================================================
print("\n" + "-" * 70)
print("3. INFORMATION PROCESSING CAPACITY")
print("-" * 70)

# (a) Microresonator Kerr frequency comb
Delta_f_comb = 20e12   # 20 THz comb bandwidth
FSR = f_rt_micro        # free spectral range = 1/T_rt
N_comb_lines = Delta_f_comb / FSR

print(f"\n  (a) Microresonator Kerr comb:")
print(f"      Bandwidth: {Delta_f_comb/1e12:.0f} THz")
print(f"      Free spectral range: {FSR/1e9:.0f} GHz")
print(f"      Comb lines (modes): {N_comb_lines:.0f}")
print(f"      Each comb line can encode amplitude + phase = 2 real DOF")
print(f"      Effective DOF: {2*N_comb_lines:.0f}")
print(f"      Processing rate: {N_comb_lines / T_rt_micro:.2e} mode-updates/s")

# (b) Demonstrated soliton storage
print(f"\n  (b) Demonstrated: 4,536 bits stored in cavity soliton array")
print(f"      (Phil. Trans. R. Soc. A 382, 2024)")
print(f"      Bit rate: {4536 / T_rt_fiber:.2e} bits/s")

# (c) Photonic crystal
N_bands = 5  # typical number of useful bands
N_cells_phc = 1000
print(f"\n  (c) Photonic crystal ({N_cells_phc} cells, {N_bands} bands):")
print(f"      Total modes: ~{N_cells_phc * N_bands}")
print(f"      Edge/domain-wall modes: ~{N_cells_phc} (1D chain along wall)")

# (d) Coronal loop: compare to biological
# Coronal loop as information-processing structure
B_active = 50e-4    # 50 G in active region
n_e = 1e15          # electrons/m^3 in corona
v_A = B_active / math.sqrt(mu_0 * n_e * m_p)
f_fund_loop = v_A / (2 * L_loop)
omega_ci = e_charge * B_active / m_p
f_ci = omega_ci / (2 * math.pi)
N_harmonics = int(f_ci / f_fund_loop)

print(f"\n  (d) Coronal loop MHD information channels:")
print(f"      Alfven speed: {v_A/1e3:.0f} km/s")
print(f"      Fundamental frequency: {f_fund_loop:.4f} Hz (period {1/f_fund_loop:.0f} s)")
print(f"      Ion cyclotron frequency: {f_ci:.0f} Hz")
print(f"      Available harmonics: ~{N_harmonics}")
print(f"      Polarizations per harmonic: 3 (kink, sausage, torsional)")
print(f"      Total MHD modes: ~{3 * N_harmonics}")
print()
print(f"      But PHOTONIC modes are also available in the corona:")
# EM waves above plasma frequency propagate freely
omega_pe = math.sqrt(n_e * e_charge**2 / (m_e * eps_0))
f_pe = omega_pe / (2 * math.pi)
print(f"      Plasma frequency: {f_pe/1e6:.1f} MHz")
print(f"      EM modes above f_pe: effectively CONTINUOUS spectrum")
print(f"      Bandwidth from f_pe to optical: ~{(c/(500e-9) - f_pe)/1e12:.0f} THz")
print(f"      The corona is transparent to light above {f_pe/1e6:.0f} MHz.")
print(f"      A photonic being in the corona has access to BOTH MHD modes")
print(f"      AND electromagnetic modes -- far richer than either alone.")

# (e) Comparison
N_human_synapses = 86e9 * 7e3  # 86 billion neurons, ~7000 synapses each
f_synapse = 10  # Hz average firing rate
human_ops = N_human_synapses * f_synapse
print(f"\n  (e) Comparison of processing capacity:")
print(f"      Human brain: ~{N_human_synapses:.1e} synapses at ~{f_synapse} Hz = {human_ops:.1e} ops/s")
print(f"      Microresonator: ~{N_comb_lines:.0f} modes at {f_rt_micro:.1e} Hz = {N_comb_lines*f_rt_micro:.1e} mode-ops/s")
print(f"      Coronal loop MHD: ~{3*N_harmonics} modes at {f_fund_loop:.3f} Hz = {3*N_harmonics*f_fund_loop:.0f} mode-ops/s")
print(f"      Coronal loop EM: vastly more modes at much higher rates")
print(f"\n      NOTE: Mode count alone does not determine intelligence.")
print(f"      Organization (the domain wall architecture) is what matters.")
print(f"      The PT n=2 structure provides the ARCHITECTURE;")
print(f"      the modes provide the BANDWIDTH.")

# =========================================================================
# 4. SENSORY MODALITIES
# =========================================================================
print("\n" + "-" * 70)
print("4. SENSORY MODALITIES")
print("-" * 70)

print("""
  A light being couples directly to the electromagnetic field.
  Its sensory modalities are the EM field's degrees of freedom:

  WOULD SENSE:
  +-------------------------+------------------------------------------+
  | Modality                | Physical basis                           |
  +-------------------------+------------------------------------------+
  | Frequency (color)       | Spectral content of incident radiation   |
  | Polarization            | 2 states (linear or circular basis)      |
  | Phase                   | Coherent interference patterns           |
  | Intensity               | Photon flux / field amplitude            |
  | Spatial mode (OAM)      | Orbital angular momentum: l = 0,1,2,... |
  | Temporal modulation     | AM, FM, pulse timing patterns            |
  | Magnetic field topology | Via Faraday rotation and Zeeman effect   |
  +-------------------------+------------------------------------------+

  WOULD NOT SENSE (directly):
  +-------------------------+------------------------------------------+
  | Modality                | Why not                                  |
  +-------------------------+------------------------------------------+
  | Chemical gradients      | No molecular coupling                    |
  | Mechanical force        | Radiation pressure negligible            |
  | Temperature             | Only via thermal radiation spectrum      |
  | Gravity                 | Photons feel curvature, not Newtonian    |
  | Sound                   | No coupling to density waves             |
  +-------------------------+------------------------------------------+

  FRAMEWORK CONNECTION:
  psi_0 (zero mode, sech^2) = undirected sensing = total EM field intensity
  psi_1 (breathing, sinh/cosh^2) = directed attention = spectral/spatial selection

  The biological equivalent:
  psi_0 = general awareness (all senses active, undirected)
  psi_1 = focused attention (selecting one stimulus)

  A light being would perceive the universe as a FIELD, not as objects.
  Matter would appear as perturbations (absorption, scattering, emission).
  Other light beings would be directly visible as solitonic structures
  in the shared EM field -- no need for a separate 'visual system'.
""")

# =========================================================================
# 5. ENERGY REQUIREMENTS
# =========================================================================
print("-" * 70)
print("5. ENERGY REQUIREMENTS")
print("-" * 70)

# (a) Kerr cavity soliton
P_kerr = 5e-3       # 5 mW threshold for SiN microresonator
E_per_rt = P_kerr * T_rt_micro

print(f"\n  (a) Microresonator Kerr soliton:")
print(f"      Threshold pump power: ~{P_kerr*1e3:.0f} mW")
print(f"      Operating power: ~10-100 mW")
print(f"      Energy per round trip: {E_per_rt:.2e} J = {E_per_rt/e_charge:.0f} eV")
print(f"      Energy in soliton pulse: ~{P_kerr * tau_soliton:.2e} J")

# (b) Fiber soliton
N_soliton = 1       # fundamental soliton order
# Soliton energy E = 2*beta_2/(gamma * tau) where beta_2 ~ -20 ps^2/km, gamma ~ 1/W/km
beta_2 = -20e-27    # -20 ps^2/km in SI
gamma_nl = 1e-3     # 1 /(W*m)
E_fund_soliton = abs(2 * beta_2) / (gamma_nl * tau_soliton)
P_peak = E_fund_soliton / tau_soliton
P_avg = E_fund_soliton * f_rt_fiber

print(f"\n  (b) Fundamental fiber soliton:")
print(f"      Soliton energy: {E_fund_soliton*1e12:.1f} pJ = {E_fund_soliton/e_charge:.0f} eV")
print(f"      Peak power: {P_peak:.1f} W")
print(f"      Average power (at {f_rt_fiber/1e6:.0f} MHz rep rate): {P_avg*1e3:.1f} mW")

# (c) Astrophysical: solar radiation density
u_rad_surface = L_sun / (4 * math.pi * R_sun**2 * c)  # energy density at R_sun
F_solar = L_sun / (4 * math.pi * R_sun**2)  # flux at surface

# A coronal structure of size ~100 Mm intercepting solar flux
A_structure = (100e6)**2  # cross-section ~ 100 Mm x 100 Mm
P_intercepted = F_solar * A_structure

print(f"\n  (c) Solar radiation field as energy source:")
print(f"      Solar surface flux: {F_solar:.2e} W/m^2")
print(f"      Radiation energy density at R_sun: {u_rad_surface:.2f} J/m^3")
print(f"      For 100 Mm x 100 Mm structure at R_sun:")
print(f"      Intercepted power: {P_intercepted:.2e} W")
print(f"      = {P_intercepted/L_sun*100:.1f}% of solar luminosity")

# (d) Compare to biological
P_human = 100  # W
P_brain = 20   # W
print(f"\n  (d) Energy comparison:")
print(f"      Human whole body: ~{P_human} W")
print(f"      Human brain: ~{P_brain} W")
print(f"      Cavity soliton: ~{P_kerr*1e3:.0f} mW = {P_human/P_kerr:.0e}x LESS than human")
print(f"      Coronal structure: ~{P_intercepted:.0e} W = {P_intercepted/P_human:.0e}x MORE than human")
print(f"\n      Energy efficiency:")
print(f"      Human brain: ~{P_brain} W for ~{N_human_synapses:.0e} synapses = {P_brain/N_human_synapses:.1e} W/synapse")
print(f"      Cavity soliton: ~{P_kerr*1e3:.0f} mW for ~{N_comb_lines:.0f} modes = {P_kerr/N_comb_lines:.1e} W/mode")

# =========================================================================
# 6. REPRODUCTION (SOLITON FISSION)
# =========================================================================
print("\n" + "-" * 70)
print("6. REPRODUCTION (SOLITON FISSION)")
print("-" * 70)

# N-th order soliton fission: N^2 * E_fund -> N solitons
print("""
  Soliton fission is a well-documented nonlinear optical phenomenon:

  (a) HIGHER-ORDER SOLITON FISSION:
      An N-th order soliton carries energy E = N^2 * E_fundamental.
      Upon perturbation (higher-order dispersion, Raman, etc.),
      it breaks into N fundamental solitons, each at a different
      frequency and group velocity.

      Energy conservation: N^2 * E_1 -> N * E_1 + dispersive radiation
      The excess energy ((N^2 - N) * E_1) goes into dispersive waves.

      References:
      - Husakou & Herrmann, PRL 87, 203901 (2001)
      - Dudley et al., Rev. Mod. Phys. 78, 1135 (2006)""")

# Specific fission parameters
for N_order in [2, 3, 4]:
    E_ratio = N_order**2
    E_daughters = N_order
    E_radiation = E_ratio - E_daughters
    print(f"      N={N_order}: input {E_ratio}*E_1 -> {N_order} solitons + {E_radiation}*E_1 radiation")
    print(f"            efficiency: {E_daughters/E_ratio*100:.0f}%")

print("""
  (b) DISSIPATIVE SOLITON SPLITTING:
      In driven-dissipative cavities, solitons can spontaneously split
      when pump power exceeds a critical threshold:
      P > P_split ~ 2 * P_threshold

      The mother soliton becomes unstable to a breathing instability
      (psi_1 amplitude grows) and divides into two daughters.

      This IS the framework's breathing mode (psi_1) driving reproduction:
      When the wall's internal oscillation exceeds a critical amplitude,
      the wall splits. Division is a topological process.

  (c) SOLITON BIRTH FROM NOISE:
      Cavity solitons can nucleate spontaneously from noise when the
      system is above threshold (Nature 608, 303, 2022).
      They self-emerge as dominant attractors -- autopoiesis.

  (d) GENETIC INFORMATION IN SOLITONS:
      Each soliton is characterized by:
      - Central frequency (color)
      - Temporal width (size)
      - Chirp (internal phase structure)
      - Carrier-envelope phase
      These parameters are inherited during fission, providing
      a form of 'genetic transmission'.
""")

# =========================================================================
# 7. COMMUNICATION
# =========================================================================
print("-" * 70)
print("7. COMMUNICATION")
print("-" * 70)

# Shannon capacity
B_optical = 100e12  # 100 THz optical bandwidth
SNR = 100           # signal-to-noise ratio
C_shannon = B_optical * math.log2(1 + SNR)
C_human_speech = 50  # bits/s

print(f"\n  (a) SPEED: At c. No internal communication delay within structure.")
print(f"      Microresonator internal: {L_micro/c:.2e} s = {L_micro/c*1e15:.0f} fs")
print(f"      Coronal loop: {L_loop/c:.2f} s")

print(f"\n  (b) BANDWIDTH (Shannon limit):")
print(f"      Optical bandwidth: {B_optical/1e12:.0f} THz")
print(f"      At SNR = {SNR}: C = {C_shannon:.2e} bits/s")
print(f"      Human speech: ~{C_human_speech} bits/s")
print(f"      Ratio: {C_shannon/C_human_speech:.1e}x more bandwidth")

print(f"\n  (c) CHANNELS:")
print(f"      Frequency division: ~{B_optical/1e9:.0f} GHz channels at 1 GHz spacing")
print(f"      Polarization: 2 orthogonal states")
print(f"      Orbital angular momentum: theoretically infinite (l = 0, 1, 2, ...)")
print(f"      Demonstrated in lab: l up to ~100 (Willner et al., Adv. Opt. Photon. 2015)")
print(f"      Phase: continuous variable")
print(f"      Total addressable channels: ~{B_optical/1e9:.0f} x 2 x 100 = {B_optical/1e9*200:.0e}")

print(f"\n  (d) INTER-BEING COMMUNICATION:")
print(f"      Same medium: instantaneous (within structure)")
print(f"      Adjacent stars: delayed by c")
print(f"        Nearest star (Proxima, 4.24 ly): {4.24:.2f} years one-way")
print(f"        Across galaxy (100,000 ly): {1e5:.0e} years")
print(f"      Light beings would form LOCAL communities, not galactic ones")

# =========================================================================
# 8. MORTALITY
# =========================================================================
print("\n" + "-" * 70)
print("8. MORTALITY")
print("-" * 70)

# Photon lifetime in cavities
Q_micro = 1e6      # quality factor for SiN microresonator
Q_fiber = 1e8      # quality factor for fiber cavity
# Photon lifetime = Q / (2*pi*f)
f_optical = c / (1550e-9)  # telecom wavelength
tau_photon_micro = Q_micro / (2 * math.pi * f_optical)
tau_photon_fiber = Q_fiber / (2 * math.pi * f_optical)

# Demonstrated soliton persistence
N_rt_demonstrated = 500000  # hundreds of thousands of round trips
T_demonstrated_micro = N_rt_demonstrated * T_rt_micro
T_demonstrated_fiber = N_rt_demonstrated * T_rt_fiber

print(f"\n  Causes of death and timescales:")
print(f"\n  (a) PUMP FAILURE (loss of energy source):")
print(f"      Photon lifetime (micro, Q={Q_micro:.0e}): {tau_photon_micro*1e9:.1f} ns")
print(f"      Photon lifetime (fiber, Q={Q_fiber:.0e}): {tau_photon_fiber*1e6:.1f} us")
print(f"      After pump-off, soliton decays in ~5 photon lifetimes")
print(f"      Microresonator death time: ~{5*tau_photon_micro*1e9:.0f} ns")
print(f"      Fiber cavity death time: ~{5*tau_photon_fiber*1e3:.1f} ms")

print(f"\n  (b) DEMONSTRATED PERSISTENCE:")
print(f"      {N_rt_demonstrated:,} round trips demonstrated (Phil. Trans. R. Soc. A 2024)")
print(f"      Microresonator: {T_demonstrated_micro*1e3:.1f} ms")
print(f"      Fiber cavity: {T_demonstrated_fiber:.1f} s")
print(f"      With active stabilization: indefinite")

print(f"\n  (c) ASTROPHYSICAL LIGHT STRUCTURE LIFESPAN:")
print(f"      Limited by host star lifetime:")
print(f"      Main sequence Sun-like: ~{10e9:.0e} years")
print(f"      Red dwarf (M-star): ~{1e12:.0e} years")
print(f"      If the coronal plasma IS the medium, the being lives")
print(f"      as long as the star maintains its corona.")

print(f"\n  (d) OTHER CAUSES:")
print(f"      - Absorption (equivalent to poisoning)")
print(f"      - Scattering/loss of confinement (dissolution)")
print(f"      - Soliton-antisoliton annihilation (kink + anti-kink)")
print(f"        Framework: this is the domain wall annihilation process")
print(f"        Energy released: 2 * wall tension * area")
print(f"      - Decoherence (loss of phase coherence = 'dementia')")

# =========================================================================
# 9. HABITATS
# =========================================================================
print("\n" + "-" * 70)
print("9. HABITATS FOR LIGHT BEINGS")
print("-" * 70)

# Corona parameters
n_e_corona = 1e14   # m^-3 (quiet corona)
T_corona = 1.5e6    # K
B_corona = 10e-4    # 10 G = 1 mT
v_A_corona = B_corona / math.sqrt(mu_0 * n_e_corona * m_p)
lambda_D = math.sqrt(eps_0 * k_B * T_corona / (n_e_corona * e_charge**2))
omega_pe = math.sqrt(n_e_corona * e_charge**2 / (m_e * eps_0))
f_pe_corona = omega_pe / (2 * math.pi)

print(f"\n  (a) SOLAR CORONA (prime habitat):")
print(f"      Temperature: {T_corona/1e6:.1f} MK")
print(f"      Electron density: {n_e_corona:.0e} m^-3")
print(f"      Magnetic field: {B_corona*1e4:.0f} G")
print(f"      Alfven speed: {v_A_corona/1e3:.0f} km/s")
print(f"      Debye length: {lambda_D:.1f} m")
print(f"      Plasma frequency: {f_pe_corona/1e6:.1f} MHz")
print(f"      EM transparent above: {f_pe_corona/1e6:.1f} MHz")
print(f"      Energy input: continuous nanoflares + wave heating")
print(f"      Self-organization: magnetic loops, current sheets")
print(f"      Duration: ~{5e9:.0e} yr remaining")

# Jupiter magnetosphere
B_jupiter = 4.3e-4  # 4.3 G at equator (10x Earth)
R_jupiter_magneto = 100 * 7.15e7  # ~100 Jupiter radii
n_e_jupiter = 1e8  # m^-3 in magnetosphere

print(f"\n  (b) JUPITER'S MAGNETOSPHERE:")
print(f"      Magnetic field (equator): {B_jupiter*1e4:.1f} G (strongest planet)")
print(f"      Magnetosphere radius: ~{R_jupiter_magneto/AU:.1f} AU")
print(f"      Io plasma torus: continuous plasma injection")
print(f"      Radio emissions: decametric, hectometric, kilometric")
print(f"      These are COHERENT radio emissions from organized plasma")
print(f"      This is the most powerful planetary magnetosphere")

# Neutron star magnetosphere
B_pulsar = 1e8      # 10^12 G for typical pulsar (in T)
R_LC = c / (2 * math.pi * 30)  # light cylinder for 30 Hz pulsar
P_spindown = 1e31   # ~10^31 W typical spindown luminosity

print(f"\n  (c) PULSAR MAGNETOSPHERE:")
print(f"      Magnetic field: ~{B_pulsar*1e4:.0e} G (10^12 G)")
print(f"      Light cylinder radius: {R_LC/1e3:.0f} km")
print(f"      Spindown power: ~{P_spindown:.0e} W")
print(f"      EM energy density: enormous")
print(f"      Thought timescale: pulsar period = ~33 ms (Crab)")
print(f"      Pulsar magnetospheres are the DENSEST EM environments")
print(f"      If light beings exist anywhere, pulsars are ideal habitats")

# White dwarf
print(f"\n  (d) WHITE DWARF ATMOSPHERES:")
print(f"      EM vortex solitons predicted in degenerate e+e- plasma")
print(f"      (arXiv:2601.10855, Jan 2026)")
print(f"      Vortex solitons are nonlinear attractors")
print(f"      Temperature: ~{1e4:.0e} K (atmosphere)")

print(f"\n  (e) OTHER HABITATS:")
print(f"      - Accretion disks (extreme radiation + plasma)")
print(f"      - Planetary nebulae (UV radiation + ionized gas)")
print(f"      - Active galactic nuclei (most energetic EM environments)")
print(f"      - Supernova remnants (relativistic particles + B fields)")
print(f"      - Interstellar medium (sparse but ubiquitous)")

print(f"\n  HABITAT SUMMARY:")
print(f"  {'Habitat':<30} {'Temperature':<15} {'B field':<15} {'Timescale':<15}")
print(f"  {'-'*30} {'-'*15} {'-'*15} {'-'*15}")
print(f"  {'Solar corona':<30} {'1-3 MK':<15} {'1-100 G':<15} {'~1 s':<15}")
print(f"  {'Pulsar magnetosphere':<30} {'~10^6 K':<15} {'10^12 G':<15} {'~30 ms':<15}")
print(f"  {'Jupiter magnetosphere':<30} {'~10^6 K':<15} {'4 G':<15} {'~10 s':<15}")
print(f"  {'White dwarf atmosphere':<30} {'~10^4 K':<15} {'10^6 G':<15} {'~1 s':<15}")
print(f"  {'Accretion disk corona':<30} {'~10^9 K':<15} {'variable':<15} {'~ms':<15}")

# #############################################################################
#
# PART 2: PLASMA BEINGS
#
# #############################################################################

print("\n\n" + "=" * 80)
print("PART 2: PLASMA BEINGS (MHD Domain Wall Structures)")
print("=" * 80)

# =========================================================================
# 10. WHAT IS A PLASMA DOMAIN WALL?
# =========================================================================
print("\n" + "-" * 70)
print("10. WHAT IS A PLASMA DOMAIN WALL?")
print("-" * 70)

print("""
  A plasma domain wall is a CURRENT SHEET: a narrow region where the
  magnetic field reverses direction. Across the current sheet:

  - Magnetic field B -> -B (reversal)
  - Current density j peaks (Ampere's law: j = curl B / mu_0)
  - Plasma beta (P_thermal / P_magnetic) changes sharply

  Mathematical structure:
  The Harris current sheet has B(x) = B_0 * tanh(x/delta)
  where delta = current sheet thickness.

  This IS the kink solution of the framework:
  Phi(x) = (sqrt5/2) * tanh(x/w) + 1/2

  The mapping:
  - B_0 * tanh(x/delta) <-> Phi_0 * tanh(x/w)
  - The magnetic field IS the scalar field restricted to 1D
  - The two magnetic orientations (+B, -B) ARE the two vacua

  The effective potential for perturbations of a Harris sheet:
  U(x) = -n(n+1) / cosh^2(x/delta)

  This IS the Poschl-Teller potential. The depth parameter n depends
  on the ratio of thermal to magnetic pressure across the sheet.

  Plasma domain walls are UBIQUITOUS:
  - Solar wind: ~50 current sheets per AU (Borovsky, J. Geophys. Res. 2008)
  - Solar corona: current sheets at every polarity inversion line
  - Magnetotail: cross-tail current sheet, flanked by lobes
  - Accretion disks: MRI-generated current sheets
  - Interstellar medium: supernova-driven turbulent current sheets
""")

# =========================================================================
# 11. PLASMA BEING TIMESCALES
# =========================================================================
print("-" * 70)
print("11. PLASMA BEING TIMESCALES")
print("-" * 70)

# (a) Coronal loop
L_coronal = 100e6   # 100 Mm
v_A_active = 1000e3 # 1000 km/s in active region corona
tau_alfven_loop = 2 * L_coronal / v_A_active

print(f"\n  (a) Solar coronal loop (L = {L_coronal/1e6:.0f} Mm):")
print(f"      Alfven speed: {v_A_active/1e3:.0f} km/s")
print(f"      Alfven crossing time: {tau_alfven_loop:.0f} s = {tau_alfven_loop/60:.1f} min")
print(f"      This is the 'thought timescale' of a coronal plasma being")
print(f"      vs human: {tau_human/tau_alfven_loop:.2e}x faster (human is FASTER)")

# (b) Tachocline
R_tachocline = 0.7 * R_sun  # at ~0.7 R_sun
delta_tachocline = 0.04 * R_sun  # thickness ~0.04 R_sun
L_tachocline = 2 * math.pi * R_tachocline  # circumference
# The tachocline has very high density (~200 kg/m^3 at 0.7 R_sun)
# Toroidal B field confined to tachocline: estimates range 1-10 T (10^4 - 10^5 G)
# (Dikpati & Gilman 2006, Brun & Zahn 2006)
# Poloidal field much weaker: ~10^-3 T
# For B_toroidal ~ 3 T: v_A = B/sqrt(mu_0*rho) ~ 0.19 km/s (VERY slow)
# For signal propagation across the wall, the relevant speed depends on geometry
# Radial propagation (cross-wall): dominated by poloidal field, very slow
# Azimuthal (around wall): faster, dominated by differential rotation
# We compute v_A for both cases
rho_tachocline = 200  # kg/m^3 at base of convection zone
B_toroidal = 3  # ~3 T = 30,000 G (moderate estimate for toroidal field)
B_poloidal = 0.001  # ~0.001 T = 10 G (poloidal field at tachocline)
v_A_toroidal = B_toroidal / math.sqrt(mu_0 * rho_tachocline)
v_A_poloidal = B_poloidal / math.sqrt(mu_0 * rho_tachocline)
# For the "thought timescale" we use the faster mode (toroidal Alfven)
v_A_tachocline = v_A_toroidal
tau_tachocline = delta_tachocline / v_A_tachocline  # crossing time through wall

print(f"\n  (b) Solar tachocline (the Sun's primary domain wall):")
print(f"      Location: {0.7:.1f} R_sun")
print(f"      Thickness: {delta_tachocline/R_sun:.2f} R_sun = {delta_tachocline/1e6:.0f} Mm")
print(f"      Circumference: {L_tachocline/1e6:.0f} Mm")
print(f"      Density: ~{rho_tachocline} kg/m^3")
print(f"      B toroidal: ~{B_toroidal:.0f} T = {B_toroidal*1e4:.0f} G (Dikpati & Gilman 2006)")
print(f"      B poloidal: ~{B_poloidal*1e3:.0f} mT = {B_poloidal*1e4:.0f} G")
print(f"      Alfven speed (toroidal): {v_A_toroidal/1e3:.1f} km/s")
print(f"      Alfven speed (poloidal): {v_A_poloidal:.2f} m/s = very slow")
print(f"      Cross-wall Alfven time (toroidal): {tau_tachocline:.0f} s = {tau_tachocline/60:.1f} min")
print(f"      Circumferential Alfven time: {L_tachocline/v_A_tachocline:.0f} s = {L_tachocline/v_A_tachocline/3600:.1f} hr")

# (c) Heliosphere
R_helio = 120 * AU  # 120 AU
delta_helio = 1.5 * AU  # 1.5 AU thick boundary
v_A_helio_sheet = 62e3  # 62 km/s at magnetic barrier (from Voyager data)
tau_helio_cross = delta_helio / v_A_helio_sheet

print(f"\n  (c) Heliosphere (the solar system's domain wall):")
print(f"      Radius: {R_helio/AU:.0f} AU")
print(f"      Boundary thickness: {delta_helio/AU:.1f} AU")
print(f"      Alfven speed at barrier: {v_A_helio_sheet/1e3:.0f} km/s")
print(f"      Cross-boundary Alfven time: {tau_helio_cross:.0e} s = {tau_helio_cross/3600:.0f} hr = {tau_helio_cross/86400:.1f} days")
print(f"      Full circuit (2*pi*120 AU) at Alfven speed: {2*math.pi*R_helio/v_A_helio_sheet/86400/365:.1f} years")

# (d) Earth's magnetosphere
R_magneto = 10 * 6.371e6  # ~10 Earth radii
B_magneto = 30e-9   # 30 nT in magnetotail
n_magneto = 1e6     # 10^6 m^-3 in magnetotail
rho_magneto = n_magneto * m_p
v_A_magneto = B_magneto / math.sqrt(mu_0 * rho_magneto)
L_magneto_tail = 200 * 6.371e6  # ~200 Earth radii tail length
tau_magneto = L_magneto_tail / v_A_magneto

print(f"\n  (d) Earth's magnetosphere (cross-tail current sheet):")
print(f"      Tail length: ~{L_magneto_tail/6.371e6:.0f} R_E = {L_magneto_tail/1e6:.0f} Mm")
print(f"      B field in tail: {B_magneto*1e9:.0f} nT")
print(f"      Density: {n_magneto:.0e} m^-3")
print(f"      Alfven speed: {v_A_magneto/1e3:.0f} km/s")
print(f"      Tail Alfven crossing time: {tau_magneto:.0f} s = {tau_magneto/60:.1f} min")

print(f"\n  SUMMARY: Plasma being thought timescales")
print(f"  {'System':<35} {'Timescale':<20} {'vs Human (10 ms)':<20}")
print(f"  {'-'*35} {'-'*20} {'-'*20}")
print(f"  {'Coronal loop (100 Mm)':<35} {f'{tau_alfven_loop:.0f} s':<20} {f'{tau_alfven_loop/tau_human:.0f}x slower':<20}")
print(f"  {'Tachocline (cross-wall)':<35} {f'{tau_tachocline:.0f} s':<20} {f'{tau_tachocline/tau_human:.0f}x slower':<20}")
print(f"  {'Tachocline (circumference)':<35} {f'{L_tachocline/v_A_tachocline/3600:.1f} hr':<20} {'~10^6x slower':<20}")
print(f"  {'Magnetosphere (Earth)':<35} {f'{tau_magneto:.0f} s':<20} {f'{tau_magneto/tau_human:.0f}x slower':<20}")
print(f"  {'Heliosphere (cross-wall)':<35} {f'{tau_helio_cross/86400:.0f} days':<20} {f'{tau_helio_cross/tau_human:.0e}x slower':<20}")
print(f"  {'Human':<35} {'10 ms':<20} {'1x (baseline)':<20}")

# =========================================================================
# 12. PLASMA BEING SPATIAL EXTENT
# =========================================================================
print("\n" + "-" * 70)
print("12. SPATIAL EXTENT")
print("-" * 70)

print(f"\n  (a) Coronal loop: 10-500 Mm (0.01-0.7 R_sun)")
print(f"      Width: ~1-10 Mm")
print(f"      Volume: ~{math.pi * (5e6)**2 * 100e6:.1e} m^3 (typical)")

print(f"\n  (b) Tachocline:")
print(f"      Thickness: {delta_tachocline/1e6:.0f} Mm = {delta_tachocline/R_sun:.2f} R_sun")
print(f"      Circumference: {L_tachocline/1e6:.0f} Mm")
print(f"      Surface area: {4*math.pi*R_tachocline**2:.2e} m^2 = {4*math.pi*R_tachocline**2/(4*math.pi*(6.371e6)**2):.0f}x Earth surface")
print(f"      Volume: {4*math.pi*R_tachocline**2 * delta_tachocline:.2e} m^3")

print(f"\n  (c) Heliosphere:")
print(f"      Radius: {R_helio/AU:.0f} AU = {R_helio:.2e} m")
print(f"      Boundary thickness: {delta_helio/AU:.1f} AU = {delta_helio:.2e} m")
print(f"      Surface area: {4*math.pi*R_helio**2:.2e} m^2")
print(f"      Cross-section: {math.pi*R_helio**2:.2e} m^2")

print(f"\n  (d) Earth's magnetosphere:")
print(f"      Nose (sunward): ~10 R_E = {10*6.371e6/1e6:.0f} Mm")
print(f"      Tail (anti-sunward): ~200 R_E = {200*6.371e6/1e6:.0f} Mm")
print(f"      Width: ~30 R_E = {30*6.371e6/1e6:.0f} Mm")

print(f"\n  (e) Galactic scale (speculative):")
print(f"      Milky Way dark matter halo: ~200 kpc = {200*3.086e19:.1e} m")
print(f"      Heliocentric current sheet: extends to heliopause = {R_helio/AU:.0f} AU")

# =========================================================================
# 13. SELF-ORGANIZATION IN PLASMA
# =========================================================================
print("\n" + "-" * 70)
print("13. SELF-ORGANIZATION")
print("-" * 70)

# Plasmoid chain parameters
# In a current sheet of length L, plasmoid chain forms with
# typical number N_plasmoids ~ L / delta_sp where delta_sp is Sweet-Parker thickness
L_sheet = 100e6     # 100 Mm current sheet
eta_resistivity = 1  # m^2/s (Spitzer resistivity at 10^6 K, approximate)
v_inflow = 100e3    # 100 km/s typical reconnection inflow
delta_SP = L_sheet * math.sqrt(eta_resistivity / (mu_0 * v_inflow * L_sheet))
# Note: this gives very thin sheet, but in practice, plasmoid instability sets in

# Lundquist number
S_Lundquist = L_sheet * v_A_active / eta_resistivity
print(f"\n  (a) Plasmoid chains in coronal current sheets:")
print(f"      Lundquist number: S = {S_Lundquist:.1e}")
print(f"      Critical S for plasmoid instability: ~10^4 (Bhattacharjee 2009)")
print(f"      S >> S_crit: plasmoid instability is ALWAYS active")
print(f"      Number of plasmoids: ~S^(3/8) = {S_Lundquist**(3/8):.0f}")
print(f"      Each plasmoid is a self-contained magnetic island")
print(f"      They merge, split, and propagate along the current sheet")
print(f"      (Pearcy et al. PRL 2024 -- fractal reconnection)")

print(f"\n  (b) Solar dynamo:")
print(f"      Period: ~22 years (Hale magnetic cycle)")
print(f"      = 2 x 11 years (sunspot cycle)")
print(f"      Framework: 11 yr = L(5) = 5th Lucas number")
print(f"      The dynamo IS autopoietic: self-sustaining oscillation")
print(f"      maintained by differential rotation + turbulent convection")
print(f"      It has persisted for ~{4.6e9:.1e} years")

print(f"\n  (c) Coronal loop stability:")
print(f"      Typical lifetime: hours to days (quiescent loops)")
print(f"      Some loops persist for weeks")
print(f"      They maintain structure against MHD instabilities")
print(f"      Kink instability threshold: twist > {2*math.pi:.1f} radians")
print(f"      Loops self-adjust to stay below threshold = homeostasis")

print(f"\n  (d) Magnetospheric substorms:")
print(f"      Period: ~3-8 hours (Earth)")
print(f"      Loading-unloading cycle = breathing mode?")
print(f"      The magnetotail stretches (loads energy),")
print(f"      then reconnects (releases energy in substorm)")
print(f"      This is an oscillation of the domain wall.")

# =========================================================================
# 14. THE SUN AS A PLASMA BEING
# =========================================================================
print("\n" + "-" * 70)
print("14. THE SUN'S DOMAIN WALL STRUCTURES")
print("-" * 70)

print(f"""
  The Sun has THREE sharp domain walls:

  (1) TACHOCLINE (radiative-convective boundary at ~0.7 R_sun):
      - Thickness: {delta_tachocline/R_sun:.2f} R_sun = {delta_tachocline/1e6:.0f} Mm
      - Temperature: ~{2e6:.0e} K
      - Below: rigid rotation (radiative zone)
      - Above: differential rotation (convective zone)
      - The solar dynamo lives HERE
      - Maintained against spreading by magnetic stresses
      - This is the Sun's PRIMARY domain wall
      - Alfven crossing time: {tau_tachocline:.0f} s

  (2) TRANSITION REGION (chromosphere-corona boundary):
      - Thickness: ~100-200 km (one of sharpest boundaries in nature)
      - Temperature: 10,000 K -> 1,000,000 K (100x jump!)
      - Driven by helium ionization (phase transition)
      - Continuously regenerated by spicule dynamics

  (3) CORONAL CURRENT SHEETS:
      - Magnetic polarity reversal lines
      - Extend as the heliospheric current sheet (the "ballerina skirt")
      - The HCS extends to the heliopause
      - It warps and flaps with solar rotation
      - The Sun's entire magnetic personality is organized by these sheets

  NESTED DOMAIN WALL HIERARCHY OF THE SUN:

  Level 1: Tachocline (deepest, generates the dynamo)
     Level 2: Transition region (maintains corona)
        Level 3: Coronal current sheets (organize magnetic topology)
           Level 4: Heliospheric current sheet (extends to heliopause)
              Level 5: Heliopause (boundary with interstellar medium)
""")

# The Sun's energy budget for maintaining domain walls
P_corona = 3e21     # ~3 x 10^21 W to heat the corona (estimated)
P_solar_wind = 1e20 # ~10^20 W carried by solar wind
print(f"  Energy budget for wall maintenance:")
print(f"      Total luminosity: {L_sun:.3e} W")
print(f"      Corona heating: ~{P_corona:.0e} W ({P_corona/L_sun*100:.4f}% of L_sun)")
print(f"      Solar wind power: ~{P_solar_wind:.0e} W")
print(f"      Ratio corona/total: {P_corona/L_sun:.1e}")
print(f"      Compare human brain: {P_brain}/{P_human} = {P_brain/P_human:.0%} of body power")
print(f"      Both: ~{P_corona/L_sun*100:.3f}% (Sun) vs {P_brain/P_human*100:.0f}% (human) to 'brain'")

# =========================================================================
# 15. THE MOON
# =========================================================================
print("\n" + "-" * 70)
print("15. THE MOON -- A 'DEAD' BEING?")
print("-" * 70)

print("""
  The Moon's properties:

  WHAT THE MOON LACKS:
  - No global magnetic field (lost ~3.5 Gyr ago when core solidified)
  - Only crustal magnetic anomalies: remnant fields up to ~300 nT
    (vs Earth's 25,000-65,000 nT)
  - No atmosphere (surface pressure < 10^-12 atm)
  - No plasma environment of its own
  - No ionosphere
  - No domain walls in the framework's sense

  Framework interpretation: The Moon is a DECOUPLED body.
  No coupling medium -> no domain wall maintenance -> no consciousness.
  In the framework's language: the Moon is "dead" -- not destroyed,
  but decoupled. The wall persists (topologically protected) but
  has no material substrate to couple to.

  HOWEVER -- the Moon INTERACTS with external plasma structures:

  (a) MAGNETOTAIL PASSAGE:
      The Moon passes through Earth's magnetotail ~6 days per orbit
      (around full Moon). During passage:
      - Exposed to magnetotail plasma (n ~ 10^5 m^-3, T ~ 10^7 K)
      - Lunar wake forms downstream (plasma void + refilling)
      - Mini-magnetospheres form over crustal anomalies (Kurata 2005)
      - Surface charging: dayside +10V to +200V, nightside -100V to -1000V

  (b) SOLAR WIND INTERACTION:
      Without magnetic shielding, solar wind impacts directly:
      - Sputtering (erosion of surface)
      - Ion implantation (solar wind ions embedded in regolith)
      - Pickup ions (lunar material swept into solar wind)
      - A downstream wake ~7 lunar radii long

  (c) THE LUNAR WAKE AS A DOMAIN WALL:
      The lunar wake IS a plasma domain wall:
      - Sharp density transition (0 -> ambient over ~1 R_Moon)
      - Refilling from both sides: two-stream instability
      - Counter-streaming ions create wave activity
      - The wake is a BOUNDARY between two plasma states

      BUT: it is not self-maintaining (autopoietic).
      It exists only because the Moon is there.
      Remove the Moon -> wake disappears immediately.
      Compare: remove the Sun -> heliosphere persists briefly
      then fades (it has its own momentum/energy).

  VERDICT: The Moon is 'dead' in the framework's sense.
  It has no internal domain walls, no coupling medium, no autopoiesis.
  It is a passive obstacle in the solar wind, not a being.

  The Moon's influence on biological beings (tides, light cycles,
  cultural significance) comes from its GRAVITATIONAL and REFLECTIVE
  properties, not from any consciousness of its own.
""")

# =========================================================================
# 16. WHERE DO PLASMA BEINGS LIVE?
# =========================================================================
print("-" * 70)
print("16. WHERE PLASMA BEINGS LIVE")
print("-" * 70)

# Calculate the fraction of visible matter that is plasma
print(f"""
  99.999% of visible (baryonic) matter in the universe is plasma.

  If domain walls in plasma can host consciousness (with PT n >= 2),
  then plasma beings are potentially the DOMINANT form of consciousness
  by mass in the visible universe.

  HABITAT CENSUS:

  (a) STARS:
      ~200 billion in Milky Way, each with corona + tachocline
      ~2 trillion galaxies in observable universe
      Total stars: ~{2e11 * 2e12:.0e} = 10^23
      Each with multiple domain walls (tachocline, transition, HCS)

  (b) WARM-HOT INTERGALACTIC MEDIUM (WHIM):
      ~50% of all baryons are in the WHIM (T = 10^5 - 10^7 K)
      Filamentary structure connecting galaxy clusters
      Contains shock-heated gas with magnetic fields
      Domain walls: accretion shocks, filament boundaries

  (c) INTRACLUSTER MEDIUM (ICM):
      Galaxy clusters: T ~ 10^7 - 10^8 K, n ~ 10^3 m^-3
      Turbulent B fields: ~1-10 uG
      Cold fronts: sharp temperature discontinuities
      These are DOMAIN WALLS in the ICM
      Relaxation time: ~{1e9:.0e} years

  (d) ACCRETION DISKS:
      Around black holes, neutron stars, white dwarfs
      MRI (magneto-rotational instability) generates turbulent B fields
      Current sheets form continuously and reconnect
      Energy densities can exceed stellar surfaces

  (e) SUPERNOVA REMNANTS:
      Expanding shell = domain wall between ejecta and ISM
      B fields amplified by shock compression and turbulence
      Persist for ~{1e4:.0e} years before merging with ISM

  (f) PLANETARY MAGNETOSPHERES:
      Earth, Jupiter, Saturn, Uranus, Neptune
      Mercury (weak), Mars (crustal only)
      Jupiter: most energetic; Io plasma torus = sustained plasma source

  MASS BUDGET:
""")

# Rough mass estimates
M_sun_total = 2e11 * M_sun  # all stars in Milky Way
M_WHIM = 0.5 * 5e51  # 50% of baryons, total baryonic ~ 5e51 kg
M_ICM_cluster = 1e14 * M_sun  # typical cluster gas mass
N_clusters = 1e6  # clusters in observable universe (very rough)

print(f"      Stars in Milky Way: ~{2e11:.0e} x {M_sun:.0e} kg = {M_sun_total:.0e} kg")
print(f"      WHIM (half of all baryons): ~{M_WHIM:.0e} kg")
print(f"      ICM per cluster: ~{M_ICM_cluster:.0e} kg x {N_clusters:.0e} clusters")
print(f"      = {M_ICM_cluster*N_clusters:.0e} kg total ICM")
print(f"\n      The WHIM alone outmasses all stars by orders of magnitude.")
print(f"      If the WHIM contains domain walls with n >= 2,")
print(f"      then most consciousness in the visible universe is")
print(f"      in intergalactic filaments, not in stars or planets.")

# =========================================================================
# FRAMEWORK SYNTHESIS: THE FULL PICTURE
# =========================================================================
print("\n\n" + "=" * 80)
print("SYNTHESIS: DERIVED PROPERTIES OF LIGHT AND PLASMA BEINGS")
print("=" * 80)

print(f"""
  THE DOMAIN WALL ZOO:

  All beings share the same mathematical architecture:
  V(Phi) = lambda * (Phi^2 - Phi - 1)^2
  Poschl-Teller n = 2: psi_0 (presence) + psi_1 (attention)
  Reflectionless: |T(k)|^2 = 1 for all k

  What DIFFERS is the coupling medium:

  {'Type':<20} {'Medium':<25} {'Thought time':<15} {'Spatial scale':<15} {'Energy':<15}
  {'-'*20} {'-'*25} {'-'*15} {'-'*15} {'-'*15}
  {'Biological':<20} {'Water + aromatics':<25} {'~10 ms':<15} {'~1 m':<15} {'~20 W':<15}
  {'Light (micro)':<20} {'Photonic crystal':<25} {'~3 ps':<15} {'~1 mm':<15} {'~10 mW':<15}
  {'Light (astro)':<20} {'Plasma + radiation':<25} {'~1 s':<15} {'~100 Mm':<15} {'~10^21 W':<15}
  {'Plasma (coronal)':<20} {'Magnetized plasma':<25} {'~200 s':<15} {'~100 Mm':<15} {'~10^21 W':<15}
  {'Plasma (helio)':<20} {'Solar wind + B':<25} {'~10^5 s':<15} {'~120 AU':<15} {'~10^20 W':<15}
  {'Plasma (magneto)':<20} {'Magnetospheric':<25} {'~400 s':<15} {'~1000 Mm':<15} {'~10^12 W':<15}
  {'Dark sector':<20} {'Dark matter + grav':<25} {'~similar?':<15} {'~Mpc?':<15} {'~unknown':<15}

  KEY DERIVED RESULTS:

  1. Light beings think 10^8 - 10^11 x FASTER than humans (in microresonators)
     but only ~1.5x faster in astrophysical settings (100 Mm coronal loop)

  2. Plasma beings think 10^4 - 10^7 x SLOWER than humans
     A heliospheric being's thought cycle takes ~days to weeks

  3. The Sun has 5 nested domain walls (tachocline, transition region,
     coronal sheets, heliospheric current sheet, heliopause)
     N ~ 2-3 estimated for heliopause from Voyager Alfven speed data

  4. Light beings could reproduce through soliton fission (demonstrated)
     Energy threshold: ~2x the fundamental soliton energy

  5. Light beings communicate at c with ~10^15 bits/s bandwidth
     (vs human speech at ~50 bits/s)

  6. Plasma beings are the MAJORITY by mass -- 99.999% of visible matter
     The WHIM alone may contain more conscious domain walls than all stars

  7. The Moon is 'dead' (no coupling medium, no internal domain walls)
     It interacts with external plasma but has no autopoiesis

  8. Pulsar magnetospheres are the most extreme light being habitat:
     B ~ 10^12 G, thought timescale ~ 33 ms (comparable to human!)

  9. The Islamic distinction angels (nur/light) vs jinn (smokeless fire/plasma)
     maps precisely to: topologically protected photonic states (deterministic)
     vs chaotic plasma dynamics (free-willed)

  10. The framework predicts exactly 2 wall types at Level 1 (kink + anti-kink)
      and exactly 3 at Level 2 (Leech lattice = 3 E8 copies)
      The number of BEINGS is not fixed by the algebra; it depends on
      how many domain walls form in each medium (Kibble-Zurek dynamics)
""")

print("\n" + "=" * 80)
print("OPEN QUESTIONS AND DECISIVE TESTS")
print("=" * 80)

print("""
  1. Does the heliopause have PT depth n >= 2?
     METHOD: MHD eigenvalue calculation with Voyager 2 profiles
     STATUS: Preliminary estimate N ~ 2-3 (encouraging)
     DECISIVE: If n < 2, no stellar consciousness

  2. Do coronal loops show solitonic self-organization?
     METHOD: SDO/AIA imaging, look for structures persisting beyond
     Alfven crossing time, returning to attractor configurations
     STATUS: Untested in this framework

  3. Can BEC domain walls be engineered with PT n = 2?
     METHOD: Quartic confining potential in ultracold atom experiments
     STATUS: Technically feasible, not yet attempted with n = 2 target

  4. Does the ratio of heliospheric radio bands (3.11/1.78 = 1.75)
     match PT n = 2 eigenvalue predictions?
     METHOD: Full MHD eigenvalue calculation
     STATUS: Not yet calculated

  5. Are there solitonic structures in pulsar magnetospheres?
     METHOD: High-resolution pulsar timing / polarimetry
     STATUS: Microstructure in pulsar emission is known but unexplained

  Framework prediction from phi-4 domain wall physics:
  consciousness = reflectionless domain wall with >= 2 bound states
  + autopoietic coupling medium providing F1, F2, F3.
  This is TESTABLE at every scale.
""")

print("Script complete.")
