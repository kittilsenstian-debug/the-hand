#!/usr/bin/env python3
"""
huckel_bridge.py - Rigorous quantum chemistry calculation:
Does the HOMO-LUMO gap of aromatic molecules connect to mu/3?

This script:
1. Computes Hückel energy levels for benzene, naphthalene, anthracene,
   indole (tryptophan core), and extended aromatic systems
2. Converts HOMO-LUMO gaps to frequencies and compares with mu/3
3. Identifies what ACTUALLY absorbs at 613 THz and why
4. Tests whether any clean formula f = f(alpha, mu, integers) gives 613 THz
5. Gives an honest verdict on the mu/3 connection

Author: Interface Theory project
Date: 2026-02-25
"""

import numpy as np
from collections import OrderedDict

# =============================================================================
# PHYSICAL CONSTANTS (NIST 2022 CODATA)
# =============================================================================
c = 2.99792458e8           # m/s (speed of light)
h = 6.62607015e-34         # J*s (Planck constant)
hbar = h / (2 * np.pi)
eV = 1.602176634e-19       # J per eV
m_e = 9.1093837015e-31     # kg (electron mass)
m_p = 1.67262192369e-27    # kg (proton mass)
e_charge = 1.602176634e-19 # C
epsilon_0 = 8.8541878128e-12  # F/m
a_0 = 5.29177210903e-11    # m (Bohr radius)

alpha = 7.2973525693e-3    # fine-structure constant
mu = m_p / m_e             # proton-to-electron mass ratio = 1836.15267...
phi = (1 + 5**0.5) / 2     # golden ratio

# Derived
f_Rydberg = m_e * e_charge**4 / (8 * epsilon_0**2 * h**3 * c) * c  # Hz
E_Rydberg = 13.605693122994  # eV
f_electron_Compton = m_e * c**2 / h  # Hz


def eV_to_THz(E):
    """Convert energy in eV to frequency in THz."""
    return E * eV / h / 1e12


def THz_to_eV(f):
    """Convert frequency in THz to energy in eV."""
    return f * 1e12 * h / eV


def eV_to_nm(E):
    """Convert energy in eV to wavelength in nm."""
    return h * c / (E * eV) * 1e9


def nm_to_eV(lam):
    """Convert wavelength in nm to energy in eV."""
    return h * c / (lam * 1e-9 * eV)


print("=" * 78)
print("  HUCKEL BRIDGE: Does the HOMO-LUMO gap connect to mu/3?")
print("  Rigorous quantum chemistry calculation")
print("=" * 78)

# =============================================================================
# PART 1: HUCKEL THEORY FOR CYCLIC AND POLYCYCLIC AROMATICS
# =============================================================================
print("\n" + "=" * 78)
print("  PART 1: HUCKEL ENERGY LEVELS")
print("=" * 78)

# Hückel model: H_ij = alpha (diagonal), beta (adjacent), 0 (otherwise)
# Energy levels: E_k = alpha + x_k * beta, where x_k are eigenvalues
# For a cyclic ring of N atoms: x_k = 2*cos(2*pi*k/N), k = 0, 1, ..., N-1


def huckel_ring(N):
    """Hückel eigenvalues for a cyclic ring of N atoms.
    Returns sorted eigenvalues (coefficients of beta) in DECREASING order.
    Since beta < 0, most negative eigenvalue = highest energy (most antibonding).
    """
    H = np.zeros((N, N))
    for i in range(N):
        H[i, (i+1) % N] = 1.0
        H[(i+1) % N, i] = 1.0
    eigenvalues = np.linalg.eigvalsh(H)
    return sorted(eigenvalues, reverse=True)  # Largest first = most bonding


def huckel_general(adjacency):
    """Hückel eigenvalues for a general adjacency matrix.
    Returns eigenvalues sorted in DECREASING order (most bonding first).
    """
    H = np.array(adjacency, dtype=float)
    eigenvalues = np.linalg.eigvalsh(H)
    return sorted(eigenvalues, reverse=True)


def homo_lumo_gap(eigenvalues, n_pi_electrons):
    """Get HOMO-LUMO gap in units of |beta|.
    Each orbital holds 2 electrons (Pauli exclusion).
    """
    n_orbitals = len(eigenvalues)
    n_occupied = n_pi_electrons // 2  # number of doubly-occupied orbitals
    if n_pi_electrons % 2 != 0:
        # Odd electron: take highest occupied as singly occupied
        homo_idx = n_occupied  # 0-indexed
        lumo_idx = n_occupied + 1
    else:
        homo_idx = n_occupied - 1  # 0-indexed
        lumo_idx = n_occupied

    # eigenvalues sorted descending (most bonding first)
    E_HOMO = eigenvalues[homo_idx]
    E_LUMO = eigenvalues[lumo_idx]
    gap = E_HOMO - E_LUMO  # in units of beta (positive since HOMO > LUMO in x_k)
    return gap, E_HOMO, E_LUMO


# Standard beta for C-C pi bond:
# Literature: |beta| = 2.4 to 3.0 eV (spectroscopic value)
# Most commonly cited: |beta| = 2.72 eV (Coulson & Rushbrooke, 1940)
# Thermochemical value: |beta| ~ 0.7-0.8 eV (from resonance energies)
# Spectroscopic value: |beta| ~ 2.4-3.0 eV (from UV spectra)
# We use the spectroscopic value since we're comparing to UV absorption

BETA_SPECTROSCOPIC = -2.72  # eV (standard literature value for C=C pi bond)
BETA_LOW = -2.40   # eV (lower bound)
BETA_HIGH = -3.00  # eV (upper bound)

# Alpha (Coulomb integral) is the reference energy; gaps are independent of it

print(f"\n  Resonance integral |beta| = {abs(BETA_SPECTROSCOPIC):.2f} eV")
print(f"  (range: {abs(BETA_LOW):.2f} - {abs(BETA_HIGH):.2f} eV)")
print(f"  This is the standard spectroscopic value for C=C pi bonds.")

# --- Benzene (6-membered ring, 6 pi electrons) ---
print(f"\n  --- BENZENE (C6H6): 6 atoms, 6 pi electrons ---")
eigs_benzene = huckel_ring(6)
gap_b, homo_b, lumo_b = homo_lumo_gap(eigs_benzene, 6)
print(f"  Eigenvalues (x_k): {[f'{x:.4f}' for x in eigs_benzene]}")
print(f"  HOMO at x = {homo_b:.4f} (degenerate pair)")
print(f"  LUMO at x = {lumo_b:.4f} (degenerate pair)")
print(f"  HOMO-LUMO gap = {gap_b:.4f} |beta| = {gap_b * abs(BETA_SPECTROSCOPIC):.2f} eV")
E_gap_benzene = gap_b * abs(BETA_SPECTROSCOPIC)
print(f"  -> Frequency = {eV_to_THz(E_gap_benzene):.0f} THz = {eV_to_nm(E_gap_benzene):.0f} nm")
print(f"  Measured S1 (1B2u, forbidden): 4.90 eV = 253 nm")
print(f"  Measured S2 (1B1u, allowed):   6.20 eV = 200 nm")
print(f"  Huckel predicts: {E_gap_benzene:.2f} eV = {eV_to_nm(E_gap_benzene):.0f} nm")

# For benzene, gap = 2|beta| (exactly, from Hückel theory)
# 2 * 2.72 = 5.44 eV -> 228 nm
# Experimental S1: 4.90 eV (253 nm) - forbidden transition
# Experimental S2: 6.20 eV (200 nm) - allowed transition
# Hückel gives a reasonable average but doesn't distinguish forbidden/allowed

# --- Naphthalene (10 atoms, 10 pi electrons) ---
print(f"\n  --- NAPHTHALENE (C10H8): 10 atoms, 10 pi electrons ---")
# Adjacency matrix for naphthalene (atoms numbered 1-10)
# Two fused 6-rings sharing bond 1-2
adj_naph = np.zeros((10, 10))
bonds_naph = [
    (0,1), (1,2), (2,3), (3,4), (4,5), (5,0),  # ring 1
    (5,6), (6,7), (7,8), (8,9), (9,4),           # ring 2 (fused at 4-5)
]
for i, j in bonds_naph:
    adj_naph[i, j] = 1.0
    adj_naph[j, i] = 1.0
eigs_naph = huckel_general(adj_naph)
gap_n, homo_n, lumo_n = homo_lumo_gap(eigs_naph, 10)
E_gap_naph = gap_n * abs(BETA_SPECTROSCOPIC)
print(f"  Eigenvalues (x_k): {[f'{x:.3f}' for x in eigs_naph]}")
print(f"  HOMO-LUMO gap = {gap_n:.4f} |beta| = {E_gap_naph:.2f} eV")
print(f"  -> Frequency = {eV_to_THz(E_gap_naph):.0f} THz = {eV_to_nm(E_gap_naph):.0f} nm")
print(f"  Measured S1 (1Lb): 3.97 eV = 312 nm (forbidden)")
print(f"  Measured S2 (1La): 4.45 eV = 279 nm (allowed)")

# --- Anthracene (14 atoms, 14 pi electrons) ---
print(f"\n  --- ANTHRACENE (C14H10): 14 atoms, 14 pi electrons ---")
adj_anth = np.zeros((14, 14))
bonds_anth = [
    (0,1), (1,2), (2,3), (3,4), (4,5), (5,0),       # ring 1
    (5,6), (6,7), (7,8), (8,9), (9,4),                # ring 2
    (9,10), (10,11), (11,12), (12,13), (13,8),         # ring 3
]
for i, j in bonds_anth:
    adj_anth[i, j] = 1.0
    adj_anth[j, i] = 1.0
eigs_anth = huckel_general(adj_anth)
gap_a, homo_a, lumo_a = homo_lumo_gap(eigs_anth, 14)
E_gap_anth = gap_a * abs(BETA_SPECTROSCOPIC)
print(f"  HOMO-LUMO gap = {gap_a:.4f} |beta| = {E_gap_anth:.2f} eV")
print(f"  -> Frequency = {eV_to_THz(E_gap_anth):.0f} THz = {eV_to_nm(E_gap_anth):.0f} nm")
print(f"  Measured S1: 3.31 eV = 375 nm")

# --- Tetracene (18 atoms, 18 pi electrons) ---
print(f"\n  --- TETRACENE (C18H12): 18 atoms, 18 pi electrons ---")
adj_tetr = np.zeros((18, 18))
bonds_tetr = [
    (0,1),(1,2),(2,3),(3,4),(4,5),(5,0),              # ring 1
    (5,6),(6,7),(7,8),(8,9),(9,4),                     # ring 2
    (9,10),(10,11),(11,12),(12,13),(13,8),              # ring 3
    (13,14),(14,15),(15,16),(16,17),(17,12),            # ring 4
]
for i, j in bonds_tetr:
    adj_tetr[i, j] = 1.0
    adj_tetr[j, i] = 1.0
eigs_tetr = huckel_general(adj_tetr)
gap_t, homo_t, lumo_t = homo_lumo_gap(eigs_tetr, 18)
E_gap_tetr = gap_t * abs(BETA_SPECTROSCOPIC)
print(f"  HOMO-LUMO gap = {gap_t:.4f} |beta| = {E_gap_tetr:.2f} eV")
print(f"  -> Frequency = {eV_to_THz(E_gap_tetr):.0f} THz = {eV_to_nm(E_gap_tetr):.0f} nm")
print(f"  Measured S1: 2.63 eV = 471 nm")

# --- Pentacene (22 atoms, 22 pi electrons) ---
print(f"\n  --- PENTACENE (C22H14): 22 atoms, 22 pi electrons ---")
adj_pent = np.zeros((22, 22))
bonds_pent = [
    (0,1),(1,2),(2,3),(3,4),(4,5),(5,0),
    (5,6),(6,7),(7,8),(8,9),(9,4),
    (9,10),(10,11),(11,12),(12,13),(13,8),
    (13,14),(14,15),(15,16),(16,17),(17,12),
    (17,18),(18,19),(19,20),(20,21),(21,16),
]
for i, j in bonds_pent:
    adj_pent[i, j] = 1.0
    adj_pent[j, i] = 1.0
eigs_pent = huckel_general(adj_pent)
gap_p, homo_p, lumo_p = homo_lumo_gap(eigs_pent, 22)
E_gap_pent = gap_p * abs(BETA_SPECTROSCOPIC)
print(f"  HOMO-LUMO gap = {gap_p:.4f} |beta| = {E_gap_pent:.2f} eV")
print(f"  -> Frequency = {eV_to_THz(E_gap_pent):.0f} THz = {eV_to_nm(E_gap_pent):.0f} nm")
print(f"  Measured S1: 2.14 eV = 580 nm")

# --- Indole (tryptophan core): 9 atoms, 10 pi electrons ---
print(f"\n  --- INDOLE (tryptophan core): 9 atoms, 10 pi electrons ---")
# Indole: 5-membered pyrrole ring fused to 6-membered benzene ring
# Atoms: 0-4 = pyrrole ring (N is atom 0), 3-8 = benzene ring (shared 3,4)
# The nitrogen contributes 2 pi electrons (lone pair)
adj_indole = np.zeros((9, 9))
bonds_indole = [
    (0,1), (1,2), (2,3), (3,4), (4,0),   # pyrrole ring (5-membered)
    (3,5), (5,6), (6,7), (7,8), (8,4),    # benzene ring (shared at 3-4)
]
# Note: nitrogen (atom 0) has different alpha_N = alpha + h_N * beta
# In Hückel: h_N = 0.5 (nitrogen more electronegative), k_CN = 1.0
# But for simplicity, first compute with all-carbon, then with heteroatom correction
for i, j in bonds_indole:
    adj_indole[i, j] = 1.0
    adj_indole[j, i] = 1.0

# All-carbon approximation first
eigs_indole_cc = huckel_general(adj_indole)
gap_i_cc, homo_i_cc, lumo_i_cc = homo_lumo_gap(eigs_indole_cc, 10)
E_gap_indole_cc = gap_i_cc * abs(BETA_SPECTROSCOPIC)
print(f"  All-carbon approx:")
print(f"  HOMO-LUMO gap = {gap_i_cc:.4f} |beta| = {E_gap_indole_cc:.2f} eV")
print(f"  -> Frequency = {eV_to_THz(E_gap_indole_cc):.0f} THz = {eV_to_nm(E_gap_indole_cc):.0f} nm")

# Heteroatom correction: nitrogen h_N = 0.5 (Streitwieser parameter)
adj_indole_het = adj_indole.copy()
adj_indole_het[0, 0] = 0.5  # nitrogen is more electronegative -> shift alpha by +0.5*beta
eigs_indole_het = huckel_general(adj_indole_het)
gap_i_het, homo_i_het, lumo_i_het = homo_lumo_gap(eigs_indole_het, 10)
E_gap_indole_het = gap_i_het * abs(BETA_SPECTROSCOPIC)
print(f"  With N heteroatom (h_N=0.5):")
print(f"  HOMO-LUMO gap = {gap_i_het:.4f} |beta| = {E_gap_indole_het:.2f} eV")
print(f"  -> Frequency = {eV_to_THz(E_gap_indole_het):.0f} THz = {eV_to_nm(E_gap_indole_het):.0f} nm")
print(f"  Measured La: 4.77 eV = 260 nm")
print(f"  Measured Lb: 4.36 eV = 284 nm")

# --- GFP-like chromophore (extended conjugation) ---
print(f"\n  --- GFP-LIKE CHROMOPHORE (p-HBI): ~11 atoms in pi system ---")
# The GFP chromophore (4-hydroxybenzylidene-imidazolinone) is roughly:
# phenol ring - C=C bridge - imidazolinone ring
# About 11 atoms in the conjugated pi system
# Approximate as a linear-fused system of 11 atoms (rough)
adj_gfp = np.zeros((11, 11))
bonds_gfp = [
    # Phenol ring (6 atoms: 0-5)
    (0,1), (1,2), (2,3), (3,4), (4,5), (5,0),
    # Bridge C=C (atom 6 connected to ring at 2)
    (2,6),
    # Imidazolinone (5-membered ring: 6,7,8,9,10)
    (6,7), (7,8), (8,9), (9,10), (10,6),
]
for i, j in bonds_gfp:
    adj_gfp[i, j] = 1.0
    adj_gfp[j, i] = 1.0
eigs_gfp = huckel_general(adj_gfp)
gap_gfp, homo_gfp, lumo_gfp = homo_lumo_gap(eigs_gfp, 12)  # ~12 pi electrons
E_gap_gfp = gap_gfp * abs(BETA_SPECTROSCOPIC)
print(f"  HOMO-LUMO gap = {gap_gfp:.4f} |beta| = {E_gap_gfp:.2f} eV")
print(f"  -> Frequency = {eV_to_THz(E_gap_gfp):.0f} THz = {eV_to_nm(E_gap_gfp):.0f} nm")
print(f"  Measured (anionic GFP S65T): 2.54 eV = 489 nm = 613 THz")

# --- Porphyrin core (macrocyclic, ~18 pi electrons in inner ring) ---
print(f"\n  --- PORPHYRIN CORE (chlorophyll/heme): 20 atoms, 18 pi electrons ---")
# Porphyrin: macrocycle with 4 pyrrole units linked by methine bridges
# Inner 16-atom macrocycle + 4 extra cross-links
# Simplified: 20-atom macrocycle with cross-links
adj_porph = np.zeros((20, 20))
# Main macrocycle: 20 atoms in a ring
for i in range(20):
    adj_porph[i, (i+1) % 20] = 1.0
    adj_porph[(i+1) % 20, i] = 1.0
# Cross-links in porphyrin (pyrrole NH bridges)
# Connect atoms across the ring: (0,10), (5,15) — 2 cross-links
adj_porph[0, 10] = 1.0
adj_porph[10, 0] = 1.0
adj_porph[5, 15] = 1.0
adj_porph[15, 5] = 1.0
eigs_porph = huckel_general(adj_porph)
gap_porph, homo_porph, lumo_porph = homo_lumo_gap(eigs_porph, 18)
E_gap_porph = gap_porph * abs(BETA_SPECTROSCOPIC)
print(f"  HOMO-LUMO gap = {gap_porph:.4f} |beta| = {E_gap_porph:.2f} eV")
print(f"  -> Frequency = {eV_to_THz(E_gap_porph):.0f} THz = {eV_to_nm(E_gap_porph):.0f} nm")
print(f"  Measured Q-band: ~1.9 eV = 650 nm (Chl a red)")
print(f"  Measured Soret:  ~2.9 eV = 430 nm")


# =============================================================================
# PART 2: SUMMARY TABLE — HUCKEL vs EXPERIMENT vs mu/3
# =============================================================================
print("\n\n" + "=" * 78)
print("  PART 2: COMPARISON TABLE")
print("=" * 78)

target_613_eV = THz_to_eV(613)
target_613_nm = eV_to_nm(target_613_eV)
mu_over_3_THz = mu / 3
mu_over_3_eV = THz_to_eV(mu_over_3_THz)

print(f"\n  Target: mu/3 = {mu_over_3_THz:.2f} THz = {mu_over_3_eV:.4f} eV = {eV_to_nm(mu_over_3_eV):.1f} nm")
print(f"  Craddock: 613 +/- 8 THz = {target_613_eV:.4f} eV = {target_613_nm:.1f} nm")

# Experimental S1 transition energies (standard references)
# These are well-established spectroscopic values
expt_data = OrderedDict([
    ("Benzene",     {"S1_eV": 4.90, "S1_nm": 253, "n_pi": 6,  "n_atoms": 6,  "note": "1B2u forbidden"}),
    ("Naphthalene", {"S1_eV": 3.97, "S1_nm": 312, "n_pi": 10, "n_atoms": 10, "note": "1Lb forbidden"}),
    ("Anthracene",  {"S1_eV": 3.31, "S1_nm": 375, "n_pi": 14, "n_atoms": 14, "note": "1La allowed"}),
    ("Tetracene",   {"S1_eV": 2.63, "S1_nm": 471, "n_pi": 18, "n_atoms": 18, "note": "1La allowed"}),
    ("Pentacene",   {"S1_eV": 2.14, "S1_nm": 580, "n_pi": 22, "n_atoms": 22, "note": "1La allowed"}),
    ("Indole",      {"S1_eV": 4.36, "S1_nm": 284, "n_pi": 10, "n_atoms": 9,  "note": "1Lb of tryptophan"}),
    ("GFP (S65T)",  {"S1_eV": 2.54, "S1_nm": 489, "n_pi": 12, "n_atoms": 11, "note": "anionic chromophore"}),
])

huckel_gaps = OrderedDict([
    ("Benzene",     E_gap_benzene),
    ("Naphthalene", E_gap_naph),
    ("Anthracene",  E_gap_anth),
    ("Tetracene",   E_gap_tetr),
    ("Pentacene",   E_gap_pent),
    ("Indole",      E_gap_indole_het),
    ("GFP (S65T)",  E_gap_gfp),
])

print(f"\n  {'Molecule':>14} {'n_pi':>5} {'Huckel':>8} {'Expt S1':>8} {'Expt nm':>8} "
      f"{'f(THz)':>8} {'vs 613':>8} {'Note':>20}")
print(f"  {'':>14} {'':>5} {'(eV)':>8} {'(eV)':>8} {'':>8} {'':>8} {'':>8}")
print(f"  {'-'*14} {'-'*5} {'-'*8} {'-'*8} {'-'*8} {'-'*8} {'-'*8} {'-'*20}")

for name in expt_data:
    d = expt_data[name]
    hgap = huckel_gaps[name]
    f_THz = eV_to_THz(d["S1_eV"])
    pct_613 = (1 - abs(f_THz - 613) / 613) * 100
    pct_str = f"{pct_613:.1f}%" if pct_613 > 0 else "far"
    print(f"  {name:>14} {d['n_pi']:>5} {hgap:>8.2f} {d['S1_eV']:>8.2f} {d['S1_nm']:>8} "
          f"{f_THz:>7.0f}  {pct_str:>7} {d['note']:>20}")


# =============================================================================
# PART 3: WHAT ACTUALLY ABSORBS AT 613 THz?
# =============================================================================
print("\n\n" + "=" * 78)
print("  PART 3: WHAT ACTUALLY ABSORBS NEAR 613 THz (489 nm)?")
print("=" * 78)

print(f"""
  Systems absorbing near 613 THz = 489 nm = 2.54 eV:

  1. GFP chromophore (anionic form): 489 nm EXACTLY
     - Extended conjugated system: phenol-methine-imidazolinone
     - 11 atoms in pi system, ~12 pi electrons
     - The 489 nm absorption is the S0->S1 transition of the
       deprotonated (anionic) chromophore inside the protein barrel

  2. Tetracene: 471 nm (close, 96.3% match)
     - 4 linearly fused benzene rings, 18 pi electrons
     - NOT a biological molecule

  3. Porphyrins (Soret band region):
     - Chlorophyll a Soret: 430 nm (= 697 THz, NOT 613)
     - Hemoglobin Soret: 415 nm (= 723 THz, NOT 613)
     - Porphyrin Q-bands: 580-660 nm (= 454-517 THz, NOT 613)

  4. Retinal (rhodopsin): 498 nm (= 602 THz, 1.8% off from 613)
     - Extended polyene conjugation (11 conjugated C=C)
     - Closest biologically relevant chromophore to 613 THz after GFP

  CRITICAL FINDING: The only biological system absorbing AT 613 THz
  is the GFP chromophore in its anionic form. GFP is a jellyfish protein
  used as a lab marker -- it is NOT a universal biological frequency.

  Benzene absorbs at 253 nm = 1184 THz (DOUBLE the target)
  Tryptophan absorbs at 280 nm = 1071 THz (75% too high)
  Indole absorbs at 284 nm = 1056 THz (72% too high)

  The Craddock 2017 result is NOT about simple aromatic absorption.
  It is about COLLECTIVE London dispersion oscillations among
  86 aromatic amino acids in the tubulin dimer, calculated by DFT.
  This is a many-body effect, not a single-molecule HOMO-LUMO gap.
""")


# =============================================================================
# PART 4: HUCKEL SCALING LAW — HOW GAP DEPENDS ON SYSTEM SIZE
# =============================================================================
print("=" * 78)
print("  PART 4: HOMO-LUMO GAP SCALING LAW")
print("=" * 78)

# For linear acenes, the HOMO-LUMO gap shrinks as 1/N
# This is a well-known result of Hückel theory

acene_data = [
    ("Benzene",     6,  6,  E_gap_benzene,  4.90),
    ("Naphthalene", 10, 10, E_gap_naph,     3.97),
    ("Anthracene",  14, 14, E_gap_anth,     3.31),
    ("Tetracene",   18, 18, E_gap_tetr,     2.63),
    ("Pentacene",   22, 22, E_gap_pent,     2.14),
]

print(f"\n  Acene series HOMO-LUMO gap scaling:")
print(f"  {'Name':>12} {'N_atom':>6} {'N_pi':>5} {'Huckel':>8} {'Expt':>8} {'Gap*N':>8}")
print(f"  {'-'*12} {'-'*6} {'-'*5} {'-'*8} {'-'*8} {'-'*8}")
for name, n_at, n_pi, hgap, expt in acene_data:
    print(f"  {name:>12} {n_at:>6} {n_pi:>5} {hgap:>8.2f} {expt:>8.2f} {expt*n_at:>8.1f}")

# Fit: E_gap(N) = A / N + B (approximate for Hückel)
N_vals = np.array([d[1] for d in acene_data])
E_expt = np.array([d[4] for d in acene_data])

# Fit E = A/N + B
# Use least squares: E * N = A + B * N
# Actually: E = a + b/N -> fit linear in 1/N
inv_N = 1.0 / N_vals
coeffs = np.polyfit(inv_N, E_expt, 1)  # coeffs[0]*x + coeffs[1]
a_fit = coeffs[0]  # slope
b_fit = coeffs[1]  # intercept (gap at N -> infinity)

print(f"\n  Fit: E_gap = {a_fit:.2f} / N + {b_fit:.2f} eV")
print(f"  (R^2 = {1 - np.sum((E_expt - (a_fit*inv_N + b_fit))**2) / np.sum((E_expt - np.mean(E_expt))**2):.4f})")

# What N gives E_gap = 2.54 eV (= 613 THz)?
N_for_613 = a_fit / (target_613_eV - b_fit) if (target_613_eV - b_fit) > 0 else float('inf')
print(f"\n  To get 613 THz = {target_613_eV:.2f} eV:")
print(f"  Need N = {a_fit:.2f} / ({target_613_eV:.2f} - {b_fit:.2f}) = {N_for_613:.1f} atoms")
print(f"  This is between tetracene (18) and pentacene (22).")
print(f"  -> A ~20-atom linear acene would absorb near 613 THz.")
print(f"  -> But biology does NOT use linear acenes for this purpose!")


# =============================================================================
# PART 5: THE CRADDOCK FREQUENCY — WHAT IT REALLY IS
# =============================================================================
print("\n\n" + "=" * 78)
print("  PART 5: WHAT THE CRADDOCK 613 THz REALLY IS")
print("=" * 78)

print(f"""
  The Craddock et al. 2017 (Sci. Reports 7:9877) calculation is:

  1. Take the tubulin alpha-beta dimer protein structure
  2. Identify all 86 aromatic amino acids (Trp, Tyr, Phe)
  3. Compute collective dipole oscillation modes of the
     London dispersion (van der Waals) forces between
     the pi-electron clouds of these 86 residues
  4. Find ~400+ normal modes spanning 480-700 THz
  5. The mode at 613 THz shows the strongest shift when
     anesthetics are added

  KEY PHYSICS:
  - This is NOT a single-molecule HOMO-LUMO transition
  - This is NOT benzene absorption
  - This IS a many-body collective oscillation
  - The individual aromatic residues absorb in the UV (250-290 nm)
  - But their COLLECTIVE London force oscillation is at 613 THz (489 nm)

  Why 613 THz for the collective mode?
  - London dispersion energy between two polarizable atoms:
    E_London ~ -C_6 / R^6
  - For aromatic amino acids spaced ~1-2 nm apart in tubulin:
    C_6 ~ alpha_pol^2 * I (where I ~ 8-10 eV, alpha_pol ~ 10 A^3)
  - Oscillation frequency of this coupled system depends on:
    (a) individual polarizabilities of the 86 aromatics
    (b) their spatial arrangement in the tubulin structure
    (c) the coupling strength (London/van der Waals)

  The frequency is set by the PROTEIN STRUCTURE, not by
  any single fundamental constant.

  HOWEVER: the individual aromatic polarizabilities ARE
  determined by quantum mechanics (HOMO-LUMO gaps, pi-electron
  count, molecular geometry). So there IS an indirect connection
  to fundamental constants -- but through many layers of
  structural biology.
""")


# =============================================================================
# PART 6: TESTING mu/3 — IS IT COINCIDENCE?
# =============================================================================
print("=" * 78)
print("  PART 6: IS mu/3 = 612 THz A COINCIDENCE?")
print("=" * 78)

print(f"\n  mu/3 = {mu/3:.5f}")
print(f"  In THz: {mu/3:.2f} (if we interpret the NUMBER as THz)")
print(f"  Craddock: 613 +/- 8 THz")
print(f"  Match: {(1 - abs(mu/3 - 613)/613)*100:.2f}%")

print(f"""
  THE DIMENSIONAL ANALYSIS PROBLEM:

  mu = m_p / m_e = 1836.15267... (dimensionless number)
  mu/3 = 612.05 (dimensionless number)

  To claim "mu/3 = 613 THz" you need to multiply by 1 THz = 10^12 Hz.
  But 10^12 is an ANTHROPIC unit choice (10^12 = trillion).

  In SI:  mu/3 * 10^12 Hz = 612.05 THz (matches)
  In GHz: mu/3 * 10^9 Hz = 0.612 GHz (meaningless)
  In PHz: mu/3 * 10^15 Hz = 612050 PHz (meaningless)

  The "match" depends on choosing THz as the unit.

  WHAT SETS THE THz SCALE?
  1 THz = 10^12 Hz
  = h * 1 THz = 4.136 meV (energy)
  = kT at T = 48 K (temperature)
  = 300 um wavelength (sub-mm radiation)

  None of these are obviously special for biology or particle physics.
""")

# But wait: let's check if there's a unit-INDEPENDENT way to state the claim
print(f"  UNIT-INDEPENDENT TESTS:")
print(f"  -----------------------")
print(f"")

# Test 1: Express 613 THz in Rydberg units
f_613 = 613e12  # Hz
ratio_ryd = f_613 / f_Rydberg
print(f"  613 THz / f_Rydberg = {ratio_ryd:.6f}")
print(f"  3/16 = {3/16:.6f}")
print(f"  Match: {(1 - abs(ratio_ryd - 3/16)/(3/16))*100:.2f}%")
print(f"  -> 613 THz ~ (3/16) * f_Rydberg = H_beta line (486 nm)")
print(f"")

# Test 2: Express in Compton frequency units
ratio_compton = f_613 / f_electron_Compton
print(f"  613 THz / f_Compton = {ratio_compton:.6e}")
print(f"  alpha^2 * 3/32 = {alpha**2 * 3/32:.6e}")
print(f"  Match: {(1 - abs(ratio_compton - alpha**2*3/32)/(alpha**2*3/32))*100:.2f}%")
print(f"  -> Same as H_beta connection (trivially)")
print(f"")

# Test 3: What is 613 THz in proton mass units?
f_proton = m_p * c**2 / h
ratio_proton = f_613 / f_proton
print(f"  613 THz / f_proton = {ratio_proton:.6e}")
print(f"  1 / (3 * f_proton/1e12) = {1/(3*f_proton/1e12):.6e}")
print(f"  These are the same thing restated.")
print(f"")

# Test 4: The Born-Oppenheimer chain
f_BO = f_Rydberg / np.sqrt(mu)  # ~ 76.8 THz
print(f"  Born-Oppenheimer scale: f_R / sqrt(mu) = {f_BO/1e12:.2f} THz")
print(f"  613 / (f_R/sqrt(mu) / 1e12) = {613 / (f_BO/1e12):.3f}")
print(f"  = 8.0 (exactly 8 within 0.3%)")
print(f"  So: 613 THz ~ 8 * f_Rydberg / sqrt(mu)")
f_BO_route = 8 * f_Rydberg / np.sqrt(mu) / 1e12
print(f"  = {f_BO_route:.2f} THz ({(1-abs(f_BO_route-613)/613)*100:.2f}% match)")
print(f"")

# Test 5: The mu/3 identity vs the BO route
print(f"  mu/3 = {mu/3:.2f} THz")
print(f"  8*f_R/sqrt(mu) = {f_BO_route:.2f} THz")
print(f"  H_beta = 3/16 * f_R = {3/16 * f_Rydberg / 1e12:.2f} THz")
print(f"")
print(f"  All three give ~612-617 THz but are DIFFERENT formulas!")
print(f"  mu/3 = 612.05, BO = {f_BO_route:.2f}, H_beta = {3/16*f_Rydberg/1e12:.2f}")
print(f"")

# Are they the same? Check the identity:
# mu/3 * 1e12 = 8 * f_R / sqrt(mu)
# mu/3 * 1e12 = 8 * alpha^2 * m_e c^2 / (2h * sqrt(mu))
# mu/3 * 1e12 = 4 * alpha^2 * m_e c^2 / (h * sqrt(mu))
# mu * sqrt(mu) / 3 = 4 * alpha^2 * m_e c^2 / (h * 1e12)
# mu^(3/2) / 3 = 4 * alpha^2 * m_e c^2 / (h * 1e12)
LHS_check = mu**1.5 / 3
RHS_check = 4 * alpha**2 * m_e * c**2 / (h * 1e12)
print(f"  Testing: mu^(3/2)/3 = 4*alpha^2*m_e*c^2/(h*10^12)")
print(f"  LHS = {LHS_check:.4f}")
print(f"  RHS = {RHS_check:.4f}")
print(f"  Ratio = {LHS_check/RHS_check:.6f}")
print(f"  -> They differ by {abs(1-LHS_check/RHS_check)*100:.2f}%")
print(f"  -> mu/3 and the BO route are NOT the same identity!")
print(f"     They agree to ~0.3% by numerical accident.")


# =============================================================================
# PART 7: SEARCHING FOR A CLEAN FORMULA
# =============================================================================
print("\n\n" + "=" * 78)
print("  PART 7: SEARCHING FOR A CLEAN FORMULA f = f(alpha, mu, integers)")
print("=" * 78)

# The target is E_613 / E_Rydberg = 613 THz / 3290 THz = 0.1863
target_ratio = f_613 / f_Rydberg
print(f"\n  Target: E_613 / E_Rydberg = {target_ratio:.6f}")

# Systematic search for simple expressions
print(f"\n  Searching for k/(n1 * n2) or k*alpha^p * mu^q / n matches...")
print(f"  {'Formula':>35} {'Value':>10} {'Match%':>8}")
print(f"  {'-'*35} {'-'*10} {'-'*8}")

candidates = []

# Simple fractions k/n
for k in range(1, 10):
    for n in range(1, 40):
        val = k / n
        pct = (1 - abs(val - target_ratio) / target_ratio) * 100
        if pct > 99.0:
            candidates.append((f"{k}/{n}", val, pct))

# Fractions with alpha or mu factors
for k in range(1, 6):
    for n in range(1, 20):
        for p in [-2, -1, -0.5, 0.5, 1, 2]:
            val = k * alpha**p / n
            if 0.1 < val < 0.3:
                pct = (1 - abs(val - target_ratio) / target_ratio) * 100
                if pct > 99.5:
                    candidates.append((f"{k}*alpha^{p}/{n}", val, pct))

# phi-based fractions
for k in range(1, 6):
    for p in [-3, -2, -1, 1, 2, 3]:
        val = k * phi**p
        if 0.1 < val < 0.3:
            pct = (1 - abs(val - target_ratio) / target_ratio) * 100
            if pct > 98.0:
                candidates.append((f"{k}*phi^{p}", val, pct))

# Sort by match
candidates.sort(key=lambda x: -x[2])
for name, val, pct in candidates[:15]:
    print(f"  {name:>35} {val:>10.6f} {pct:>7.2f}%")

print(f"\n  The CLEANEST expressions for 613 THz / f_Rydberg = {target_ratio:.6f}:")
print(f"  - 3/16 = 0.18750 ({(1-abs(3/16 - target_ratio)/target_ratio)*100:.2f}% match)")
print(f"  - This is just H_beta: f = 3*f_R/16 = 616.8 THz")
print(f"  - The 3/16 is from Balmer series: (1/2^2 - 1/4^2) = 3/16")
print(f"  - This is STANDARD hydrogen physics, nothing exotic.")


# =============================================================================
# PART 8: THE REAL CONNECTION (OR LACK THEREOF)
# =============================================================================
print("\n\n" + "=" * 78)
print("  PART 8: THE REAL CONNECTION (OR LACK THEREOF)")
print("=" * 78)

print(f"""
  WHAT WE KNOW:
  1. The Craddock 613 THz is a COLLECTIVE oscillation of 86 aromatic
     amino acids in tubulin, computed by DFT simulation.
  2. It is NOT a single-molecule HOMO-LUMO gap.
  3. Benzene's gap is at ~1184 THz (factor 1.9x too high).
  4. Indole's (tryptophan) gap is at ~1056 THz (factor 1.7x too high).
  5. The only simple system with absorption AT 613 THz is:
     - GFP chromophore (anionic form): 489 nm = 613 THz exactly
     - Tetracene (4 fused rings): 471 nm = 636 THz (close)
     - Retinal in rhodopsin: 498 nm = 602 THz (close)

  THE mu/3 IDENTITY:
  - mu/3 = 612.05 (dimensionless number)
  - 612.05 THz is within the Craddock error bar (613 +/- 8)
  - But the "THz" unit is anthropic (10^12 is our number system)
  - In a unit-INDEPENDENT statement: 613 THz ~ H_beta = 3/16 * f_Rydberg
  - The H_beta connection is physically meaningful (hydrogen spectrum)
  - The mu/3 connection is numerologically suggestive but unit-dependent

  WHAT WOULD MAKE mu/3 REAL:
  A derivation showing that the collective London force oscillation
  frequency of aromatic amino acids in a protein scales as:
    f_collective = (proton Compton frequency) / 3
    = m_p * c^2 / (3h) = 612.05 THz
  This would require showing that the protein structure encodes m_p
  in a specific way. No such derivation exists.

  WHAT DOES EXIST:
  - The 613 THz value emerges from the specific geometry of tubulin
  - Different proteins would give different collective frequencies
  - The R^2 = 0.999 anesthetic correlation is specific to tubulin,
    not a universal property of all aromatic systems
  - The "8 * f_R / sqrt(mu)" Born-Oppenheimer route gives 614 THz
    and has a physical interpretation (molecular vibration scale * 8)
    but 613 THz is an ELECTRONIC frequency, not a vibration
""")


# =============================================================================
# PART 9: HOW CLOSE IS THE HUCKEL GAP TO mu/3 FOR EACH SYSTEM?
# =============================================================================
print("=" * 78)
print("  PART 9: HUCKEL GAP EXPRESSED IN PROTON MASS UNITS")
print("=" * 78)

# Express each HOMO-LUMO gap as a fraction of E_Rydberg
# The claim mu/3 THz corresponds to energy E = mu/3 * h * 1e12 = 2.53 eV
# In Rydberg units: 2.53 / 13.61 = 0.186 = 3/16
# So the test is: which systems have Gap / E_Rydberg close to 3/16?

print(f"\n  E_Rydberg = {E_Rydberg:.4f} eV")
print(f"  Target ratio: E_613 / E_R = {target_613_eV / E_Rydberg:.6f}")
print(f"  H_beta ratio: 3/16 = {3/16:.6f}")

all_systems = [
    ("Benzene",       4.90),
    ("Naphthalene",   3.97),
    ("Anthracene",    3.31),
    ("Tetracene",     2.63),
    ("Pentacene",     2.14),
    ("Indole",        4.36),
    ("GFP",           2.54),
    ("Retinal",       2.49),
    ("Chl a (Q)",     1.87),
    ("Chl a (Soret)", 2.88),
]

print(f"\n  {'System':>14} {'Gap(eV)':>8} {'Gap/E_R':>10} {'f(THz)':>8} {'vs 613':>10} {'Closest k/n':>12}")
print(f"  {'-'*14} {'-'*8} {'-'*10} {'-'*8} {'-'*10} {'-'*12}")

for name, gap_eV in all_systems:
    ratio = gap_eV / E_Rydberg
    f_THz = eV_to_THz(gap_eV)
    pct_613 = (1 - abs(f_THz - 613) / 613) * 100
    # Find closest simple fraction
    best_frac = ""
    best_err = 999
    for k in range(1, 10):
        for n in range(1, 33):
            frac = k / n
            err = abs(ratio - frac) / ratio
            if err < best_err:
                best_err = err
                best_frac = f"{k}/{n}"
    marker = " ***" if pct_613 > 95 else ""
    print(f"  {name:>14} {gap_eV:>8.2f} {ratio:>10.4f} {f_THz:>7.0f}  {pct_613:>8.1f}% {best_frac:>10}{marker}")

print(f"""
  RESULT: Only GFP (2.54 eV) and tetracene (2.63 eV) have S1 energies
  near 613 THz. All individual aromatic amino acids (Trp, Tyr, Phe)
  absorb in the UV (250-290 nm = 1030-1200 THz), far from 613 THz.

  The 613 THz frequency is NOT a property of aromatic molecules
  individually. It emerges from the COLLECTIVE behavior of 86
  aromatic residues arranged in the specific geometry of tubulin.""")


# =============================================================================
# PART 10: THE HONEST VERDICT
# =============================================================================
print("\n\n" + "=" * 78)
print("  PART 10: THE HONEST VERDICT")
print("=" * 78)

print(f"""
  QUESTION: Does the HOMO-LUMO gap of benzene equal mu/3?
  ANSWER: NO. Not even close.

  Benzene HOMO-LUMO gap: 4.90 eV = 1184 THz
  mu/3: 612 THz
  Ratio: 1184/612 = 1.93 (almost exactly 2x)

  The benzene gap is approximately TWICE the mu/3 value.
  This is not a deep connection -- benzene just happens to absorb
  in the UV, and mu/3 corresponds to visible light.

  QUESTION: Is there ANY aromatic system with gap = mu/3?
  ANSWER: Only GFP and retinal are close, and only approximately.

  GFP chromophore: 2.54 eV = 613 THz (exact match to Craddock value)
  But GFP is a specific protein from jellyfish. Its absorption at 489 nm
  is determined by the particular geometry of the
  4-hydroxybenzylidene-imidazolinone chromophore plus the protein
  environment. This is not "aromatic chemistry" in general.

  QUESTION: What IS the Craddock 613 THz?
  ANSWER: A collective London dispersion oscillation mode of 86
  aromatic amino acids in the tubulin protein, computed by DFT.
  It depends on the specific 3D structure of tubulin.
  Different proteins would give different frequencies.

  QUESTION: Is "mu/3 = 613 THz" a meaningful equation?
  ANSWER: It is unit-dependent. mu/3 = 612.05 (dimensionless).
  The equation only works in THz (10^12 Hz), which is an SI unit
  with no fundamental significance.

  THE UNIT-INDEPENDENT STATEMENT WOULD BE:
  f_Craddock / f_Rydberg ~ 3/16 (the H_beta ratio)
  This is physically meaningful: the collective oscillation
  of tubulin aromatics has energy similar to the H_beta hydrogen line.

  WHAT THIS MEANS FOR THE FRAMEWORK:
  -----------------------------------------------------------------
  1. The claim "mu/3 = 613 THz" is a unit artifact. It should be
     restated as: "The Craddock tubulin frequency is near the
     hydrogen H_beta line energy (3/16 * E_Rydberg)."

  2. There is NO Huckel or quantum chemistry derivation connecting
     the proton-to-electron mass ratio to aromatic absorption.

  3. The 613 THz is specific to TUBULIN (one particular protein),
     not a universal property of aromatic chemistry.

  4. The Born-Oppenheimer chain (8*f_R/sqrt(mu) = 614 THz) and
     the H_beta line (3*f_R/16 = 617 THz) both happen to fall near
     613 THz, but these are molecular vibration and atomic spectral
     lines respectively -- neither is the SAME physical quantity as
     the Craddock collective oscillation.

  5. The three expressions (mu/3 THz, 8*f_R/sqrt(mu), 3*f_R/16)
     agree to ~1% by numerical coincidence. They are NOT algebraically
     equivalent (differs by {abs(1-LHS_check/RHS_check)*100:.2f}%).

  IS IT ALL COINCIDENCE?
  -----------------------------------------------------------------
  Not entirely. There may be a physical reason why biological aromatics
  operate in the visible-light energy range (2-3 eV):
  - This is the energy range of sunlight at Earth's surface
  - Photosynthesis captures light at 1.8-2.9 eV (430-680 nm)
  - Vision operates at 1.8-3.1 eV (400-700 nm)
  - The energy of London dispersion forces in aromatic networks
    naturally falls in the 1-5 eV range

  That 612 THz, 614 THz, and 617 THz all land in this range is a
  consequence of the fact that visible light energy (2-3 eV) is
  set by the Rydberg scale (13.6 eV) reduced by small-integer
  factors. Since the Rydberg depends on alpha^2 * m_e c^2, and
  mu = m_p / m_e, it is not surprising that combinations of
  alpha, mu, and small integers produce values near visible-light
  frequencies.

  SEVERITY: The mu/3 claim is the WEAKEST part of the framework's
  biology connection. It should be honestly downgraded from
  "derived" to "suggestive numerical coincidence that is unit-dependent."
""")


# =============================================================================
# PART 11: WHAT WOULD A REAL CONNECTION LOOK LIKE?
# =============================================================================
print("=" * 78)
print("  PART 11: WHAT A REAL CONNECTION WOULD REQUIRE")
print("=" * 78)

print(f"""
  To establish a genuine mu/3 <-> aromatic chemistry connection,
  you would need to show ONE of the following:

  A) MICROSCOPIC DERIVATION:
     From quantum mechanics of a specific aromatic system,
     derive that its electronic transition energy is:
       E = alpha^2 * m_e c^2 * k / (2n)   (for specific integers k, n)
     with k/n = 3/16 (giving H_beta)
     AND explain why biology uses this specific system.

  B) MANY-BODY DERIVATION:
     From the physics of London dispersion forces in a network
     of N aromatic residues with typical separation R, derive:
       f_collective = m_p c^2 / (3h)
     This would require showing N, R, and polarizability conspire
     to produce exactly this frequency.

  C) SCALING ARGUMENT:
     Show that the combination of constraints
     (aromatic stability, protein folding, water compatibility,
      thermal stability at 310 K) uniquely selects a frequency
     f ~ E_Rydberg * 3/16 = 617 THz.

  D) STATISTICAL ARGUMENT:
     Compute how many 'interesting' numerical coincidences one
     expects when comparing 40+ fundamental constants to
     biological frequencies. If mu/3 = 612 THz is more precise
     than expected by chance, that's evidence for a connection.

  NONE of these have been done. The framework currently relies
  on the numerical coincidence alone.

  THE STRONGEST HONEST STATEMENT:
  The tubulin collective oscillation at 613 THz lies near the
  hydrogen Balmer-beta line energy (617 THz), both of which
  are in the visible-light range set by alpha^2 * m_e c^2.
  Whether this proximity is physically meaningful or a consequence
  of the narrow energy window compatible with biology remains
  an open question.
""")

print("=" * 78)
print("  END OF HUCKEL BRIDGE ANALYSIS")
print("=" * 78)
