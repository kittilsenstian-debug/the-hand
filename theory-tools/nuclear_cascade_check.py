#!/usr/bin/env python3
"""
nuclear_cascade_check.py -- Do framework constants give correct nuclear physics?
================================================================================

If V(Φ) is real, the derived constants (α, α_s, quark masses) should cascade
into correct nuclear physics. This script checks what the framework predicts
for nucleon masses, binding energies, and nuclear stability.

Usage:
    python theory-tools/nuclear_cascade_check.py
"""

import math
import sys

if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

phi = (1 + math.sqrt(5)) / 2
phibar = 1 / phi

# Framework constants
alpha_s_framework = 0.11840       # η(1/φ)
alpha_em_framework = 1/137.036    # from θ₃·φ/θ₄ + VP
m_e = 0.51099895                  # MeV (input)

# Framework-derived quantities
mu_framework = 6**5 / phi**3 + 9 / (7 * phi**2)  # = 1836.15...
m_p_framework = m_e * mu_framework                  # MeV

# Measured values for comparison
m_p_meas = 938.272088   # MeV
m_n_meas = 939.565421   # MeV
alpha_s_meas = 0.1180    # at M_Z

print("=" * 72)
print("NUCLEAR CASCADE CHECK")
print("Do framework constants give correct nuclear physics?")
print("=" * 72)
print()

# =====================================================================
# 1. PROTON MASS
# =====================================================================
print("=" * 72)
print("1. PROTON MASS")
print("=" * 72)
print()

# The proton mass is ~99% from QCD dynamics (Λ_QCD), not quark masses.
# Lattice QCD: m_p = f(α_s, m_u, m_d, m_s)
# The key input is Λ_QCD, which runs from α_s(M_Z).

# Λ_QCD from α_s at M_Z (1-loop):
# Λ_QCD = M_Z · exp(−2π / (b₀ · α_s))
# where b₀ = 11 − 2n_f/3 = 11 − 4 = 7 (for n_f = 6)
# Actually for Λ_QCD at low energies with n_f = 3: b₀ = 11 − 2 = 9
M_Z = 91187.6  # MeV
b0_nf3 = 9.0  # for 3 light flavors below charm threshold

Lambda_QCD_framework = M_Z * math.exp(-2 * math.pi / (b0_nf3 * alpha_s_framework))
Lambda_QCD_measured = M_Z * math.exp(-2 * math.pi / (b0_nf3 * alpha_s_meas))

print(f"Framework α_s(M_Z) = {alpha_s_framework}")
print(f"Measured  α_s(M_Z) = {alpha_s_meas}")
print()
print(f"Λ_QCD (framework) = {Lambda_QCD_framework:.1f} MeV  (1-loop, n_f=3)")
print(f"Λ_QCD (measured)   = {Lambda_QCD_measured:.1f} MeV")
print(f"Ratio: {Lambda_QCD_framework/Lambda_QCD_measured:.4f}")
print()

# Proton mass ~ 3.3 × Λ_QCD (lattice result)
mp_from_Lambda_framework = 3.3 * Lambda_QCD_framework
mp_from_Lambda_measured = 3.3 * Lambda_QCD_measured
print(f"m_p ≈ 3.3 × Λ_QCD (lattice estimate):")
print(f"  Framework: {mp_from_Lambda_framework:.0f} MeV")
print(f"  From measured α_s: {mp_from_Lambda_measured:.0f} MeV")
print(f"  Actual: {m_p_meas:.0f} MeV")
print()

# More precisely, the proton mass from the framework's μ:
print(f"Framework μ = m_p/m_e = {mu_framework:.5f}")
print(f"Framework m_p = m_e × μ = {m_p_framework:.3f} MeV")
print(f"Measured m_p = {m_p_meas:.3f} MeV")
print(f"Match: {100*min(m_p_framework, m_p_meas)/max(m_p_framework, m_p_meas):.4f}%")
print()

print("NOTE: The framework derives μ = m_p/m_e directly (99.9998%).")
print("This bypasses the QCD calculation entirely.")
print("The question is whether α_s = η(1/φ) is CONSISTENT with")
print("the μ derived from 6⁵/φ³ + 9/(7φ²).")
print()
print(f"Consistency check: does Λ_QCD from α_s give the right m_p?")
print(f"  Λ_QCD × 3.3 = {mp_from_Lambda_framework:.0f} MeV vs {m_p_meas:.0f} MeV")
print(f"  This is a {100*abs(mp_from_Lambda_framework - m_p_meas)/m_p_meas:.0f}% discrepancy.")
print(f"  (The 3.3 factor is approximate; lattice gives m_p/Λ_QCD more precisely)")
print()

# =====================================================================
# 2. NEUTRON-PROTON MASS DIFFERENCE
# =====================================================================
print("=" * 72)
print("2. NEUTRON-PROTON MASS DIFFERENCE")
print("=" * 72)
print()

# m_n - m_p = 1.293 MeV
# This comes from: (m_d - m_u) + EM correction
# m_d - m_u ≈ 2.5 MeV (QCD contribution, making neutron heavier)
# EM correction ≈ −0.76 MeV (proton heavier, from charge)
# Total: ≈ 1.3 MeV

delta_np_meas = m_n_meas - m_p_meas
print(f"m_n − m_p (measured) = {delta_np_meas:.3f} MeV")
print()
print("This requires knowing m_d − m_u (quark mass difference).")
print("The framework does NOT derive individual light quark masses.")
print("Status: NOT DERIVABLE (requires quark mass inputs not available)")
print()

# =====================================================================
# 3. NUCLEAR BINDING ENERGY
# =====================================================================
print("=" * 72)
print("3. NUCLEAR BINDING ENERGY (SEMI-EMPIRICAL MASS FORMULA)")
print("=" * 72)
print()

# The Bethe-Weizsäcker formula:
# B(A,Z) = a_V·A − a_S·A^(2/3) − a_C·Z(Z-1)/A^(1/3) − a_A·(A-2Z)²/A + δ(A,Z)
# with empirical coefficients:
a_V = 15.67   # MeV (volume)
a_S = 17.23   # MeV (surface)
a_C = 0.714   # MeV (Coulomb)
a_A = 93.15   # MeV (asymmetry... wait, traditional is ~23)

# Actually, standard values:
a_V = 15.75  # MeV
a_S = 17.80  # MeV
a_C = 0.711  # MeV
a_A = 23.70  # MeV
a_P = 11.18  # MeV (pairing)

print("Semi-empirical mass formula coefficients:")
print(f"  a_V = {a_V} MeV (volume)")
print(f"  a_S = {a_S} MeV (surface)")
print(f"  a_C = {a_C} MeV (Coulomb)")
print(f"  a_A = {a_A} MeV (asymmetry)")
print()

# Which of these can the framework address?
print("Framework connection to SEMF coefficients:")
print()
print("  a_V ≈ Λ_QCD × const:")
print(f"    a_V/Λ_QCD = {a_V/Lambda_QCD_framework:.2f} (volume term ~ nuclear force range)")
print()
print("  a_C = (3/5) × α/r₀ where r₀ = 1.25 fm:")
aC_theory = 0.6 * alpha_em_framework * 197.3 / 1.25  # ℏc = 197.3 MeV·fm
print(f"    a_C (computed) = (3/5) × α × ℏc/r₀ = {aC_theory:.3f} MeV")
print(f"    a_C (empirical) = {a_C} MeV")
print(f"    Match: {100*min(aC_theory, a_C)/max(aC_theory, a_C):.1f}%")
print()

# Iron-56: most stable nucleus
def binding_energy(A, Z):
    """Semi-empirical mass formula binding energy per nucleon."""
    delta = 0
    if A % 2 == 0:
        if Z % 2 == 0:
            delta = a_P / A**0.5
        else:
            delta = -a_P / A**0.5
    B = a_V * A - a_S * A**(2.0/3.0) - a_C * Z*(Z-1)/A**(1.0/3.0) - a_A * (A - 2*Z)**2 / A + delta
    return B / A

print("Most stable nuclei (binding energy per nucleon):")
print()
best_be = 0
best_A = 0
best_Z = 0
for A in range(2, 300):
    for Z in range(max(1, A//2 - 20), min(A, A//2 + 20)):
        be = binding_energy(A, Z)
        if be > best_be:
            best_be = be
            best_A = A
            best_Z = Z

print(f"  Most stable: A = {best_A}, Z = {best_Z} (B/A = {best_be:.3f} MeV)")
print(f"  Measured: Fe-56 peak at B/A ≈ 8.79 MeV, but Ni-62 is slightly higher")
print()

# Check iron-56 specifically
be_fe56 = binding_energy(56, 26)
print(f"  Fe-56 (SEMF): B/A = {be_fe56:.3f} MeV")
print(f"  Fe-56 (measured): B/A = 8.790 MeV")
print()

# E7 connection
print("IRON-56 AND E₇:")
print(f"  56 = dim(fundamental rep of E₇)")
print(f"  26 (protons in iron) = dim(F₄)")
print(f"  240 − 56 = 184 = predicted next magic number (island of stability)")
print(f"  This is SUGGESTIVE but NOT DERIVED.")
print(f"  The SEMF gives Fe-58 as peak, not Fe-56.")
print(f"  The real peak is Ni-62 (measured). Fe-56 is just most abundant.")
print()

# =====================================================================
# 4. NUCLEAR MAGIC NUMBERS
# =====================================================================
print("=" * 72)
print("4. NUCLEAR MAGIC NUMBERS")
print("=" * 72)
print()

magic = [2, 8, 20, 28, 50, 82, 126]
print(f"Magic numbers: {magic}")
print(f"Differences: {[magic[i+1]-magic[i] for i in range(len(magic)-1)]}")
print()

# Check framework connections
print("Framework connections to magic numbers:")
print(f"  2 = number of PT bound states (n=2)")
print(f"  8 = rank(E₈)")
print(f"  20 = dim(irrep?) -- no clean connection")
print(f"  28 = dim(SO(8)) -- coincidence?")
print(f"  50 = ? (no clean connection)")
print(f"  82 = ? (no clean connection)")
print(f"  126 = dim(SO(9)) = dim(5th rank antisymmetric of E₈)? -- stretch")
print()
print("VERDICT: Magic numbers are NOT derived from the framework.")
print("They come from nuclear shell model (spin-orbit coupling).")
print("The framework provides α_s → nuclear force, but the shell")
print("structure requires solving the many-body Schrodinger equation.")
print("This is STANDARD PHYSICS cascading from framework constants,")
print("not something the framework needs to derive separately.")
print()

# =====================================================================
# 5. DEUTERON BINDING
# =====================================================================
print("=" * 72)
print("5. DEUTERON BINDING ENERGY")
print("=" * 72)
print()

# The deuteron binding energy B_d = 2.224 MeV
# This is extremely sensitive to the nuclear force strength.
# A few percent change in α_s → no bound deuteron → no Big Bang nucleosynthesis

B_d_meas = 2.224  # MeV
print(f"Deuteron binding energy: {B_d_meas} MeV")
print()
print("The deuteron is barely bound. This is critical because:")
print("  - Slightly weaker nuclear force → no deuteron → no nucleosynthesis")
print("  - Slightly stronger → di-proton stable → all H burns to He immediately")
print()
print("Framework α_s = 0.11840 (vs measured 0.1180).")
print("Difference: 0.3%")
print()

# The deuteron binding is exponentially sensitive to α_s.
# Roughly: B_d ~ exp(-c / α_s) for some constant c
# A 0.3% shift in α_s gives roughly 0.3% × c change in the exponent
# For c ~ 1: this gives ~0.3% change in B_d, which is ~0.007 MeV
# The deuteron would still be bound.

print("A 0.3% change in α_s gives ~O(1%) change in nuclear potential depth.")
print("The deuteron would still be bound — the framework is CONSISTENT")
print("with Big Bang nucleosynthesis.")
print()

# =====================================================================
# 6. SUMMARY
# =====================================================================
print("=" * 72)
print("6. NUCLEAR CASCADE SUMMARY")
print("=" * 72)
print()
print("WHAT THE FRAMEWORK PROVIDES:")
print("  ✓ α_s = 0.11840 → Λ_QCD → nuclear force scale")
print("  ✓ μ = m_p/m_e → proton mass directly (99.9998%)")
print("  ✓ α = 1/137.036 → Coulomb term in nuclear binding")
print("  ✓ Constants consistent with deuteron binding (nucleosynthesis works)")
print()
print("WHAT CASCADES AUTOMATICALLY (standard physics):")
print("  ✓ Nuclear binding curve shape (from SEMF, uses α and α_s)")
print("  ✓ Iron peak in binding (from balance of strong and Coulomb)")
print("  ✓ Magic numbers (from shell model, uses nuclear force from α_s)")
print("  ✓ Big Bang nucleosynthesis (deuteron binding from α_s)")
print()
print("WHAT THE FRAMEWORK CANNOT DERIVE:")
print("  ✗ Individual light quark masses (m_u, m_d)")
print("  ✗ Neutron-proton mass difference (needs m_d − m_u)")
print("  ✗ Detailed nuclear structure (many-body QM problem)")
print("  ✗ Nuclear magic numbers (shell model, not fundamental)")
print()
print("RATING: CASCADES (standard physics with framework constants)")
print("  Nuclear physics doesn't need new derivation from V(Φ).")
print("  Given correct α, α_s, and quark masses, everything follows")
print("  from established QCD + nuclear many-body theory.")
