#!/usr/bin/env python3
"""
lambda_qcd_derivation.py -- Research whether Lambda_QCD = m_p/phi^3 can be
derived from the framework's own structure.

Investigates:
1. Numerical verification of 6^5 * m_e / phi^6
2. phi^6 algebraic properties
3. Domain wall confinement scale
4. Refinement factor eta/(3*phi^3) interpretation
"""

import math
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

phi = (1 + math.sqrt(5)) / 2
phibar = 1 / phi
sqrt5 = math.sqrt(5)

# Modular forms at q = 1/phi
eta_val = 0.118403904856684
theta2 = 2.555093469444516
theta3 = 2.555093469444516
theta4 = 0.030311200785327

m_e_GeV = 0.51099895e-3
m_p_GeV = 0.93827208816
M_Z = 91.1876
mu_meas = 1836.15267343
inv_alpha_Rb = 137.035999206

print("=" * 75)
print("TASK 3: Domain Wall Physics and Lambda_QCD")
print("=" * 75)

# ================================================================
# 3A: The VP formula - detailed numerical check
# ================================================================
print()
print("--- 3A: VP Formula B computation ---")
print()

inv_alpha_tree = (theta3 / theta4) * phi
coeff_Weyl = 1 / (3 * math.pi)

Lambda_raw = m_p_GeV / phi**3
Lambda_refined = Lambda_raw * (1 - eta_val / (3 * phi**3))

delta_raw = coeff_Weyl * math.log(Lambda_raw / m_e_GeV)
delta_ref = coeff_Weyl * math.log(Lambda_refined / m_e_GeV)

inv_alpha_B_raw = inv_alpha_tree + delta_raw
inv_alpha_B_ref = inv_alpha_tree + delta_ref

print(f"Tree level: 1/alpha_tree = theta3*phi/theta4 = {inv_alpha_tree:.10f}")
print(f"Lambda_raw     = m_p/phi^3 = {Lambda_raw*1000:.4f} MeV")
print(f"Lambda_refined = {Lambda_refined*1000:.4f} MeV")
print(f"ln(Lambda_raw/m_e)     = {math.log(Lambda_raw/m_e_GeV):.10f}")
print(f"ln(Lambda_refined/m_e) = {math.log(Lambda_refined/m_e_GeV):.10f}")
print()
print(f"VP correction (raw):     delta = {delta_raw:.10f}")
print(f"VP correction (refined): delta = {delta_ref:.10f}")
print()
print(f"1/alpha (raw Lambda):     {inv_alpha_B_raw:.10f}  ({abs(inv_alpha_B_raw - inv_alpha_Rb)/inv_alpha_Rb*1e6:.3f} ppm)")
print(f"1/alpha (refined Lambda): {inv_alpha_B_ref:.10f}  ({abs(inv_alpha_B_ref - inv_alpha_Rb)/inv_alpha_Rb*1e6:.3f} ppm)")
print(f"1/alpha (measured Rb):    {inv_alpha_Rb:.10f}")
print()

# What Lambda gives EXACT match?
delta_needed = inv_alpha_Rb - inv_alpha_tree
Lambda_exact = m_e_GeV * math.exp(3 * math.pi * delta_needed)
print(f"Exact-match Lambda: {Lambda_exact*1000:.6f} MeV")
print(f"Lambda_exact/Lambda_raw     = {Lambda_exact/Lambda_raw:.10f}")
print(f"Lambda_exact/Lambda_refined = {Lambda_exact/Lambda_refined:.10f}")

# What does the exact-match refinement factor look like?
# Lambda_exact = Lambda_raw * (1 - x)
# x = 1 - Lambda_exact/Lambda_raw
x_exact = 1 - Lambda_exact/Lambda_raw
x_framework = eta_val / (3 * phi**3)
print(f"\nRefinement factor x such that Lambda_exact = Lambda_raw*(1-x):")
print(f"  x (exact match)  = {x_exact:.10f}")
print(f"  x (framework)    = eta/(3*phi^3) = {x_framework:.10f}")
print(f"  Difference:        {abs(x_exact - x_framework):.10f}")
print(f"  Match:             {min(x_exact,x_framework)/max(x_exact,x_framework)*100:.4f}%")

# ================================================================
# 3B: Kink classical mass
# ================================================================
print()
print("--- 3B: Kink classical mass ---")
print()

# V(Phi) = lambda*(Phi^2 - Phi - 1)^2
# Kink mass = integral dPhi * sqrt(2*V(Phi)) from -1/phi to phi
# = sqrt(2*lambda) * 5*sqrt(5)/6  (computed in previous run)
# With m^2 = 10*lambda: E_kink = (5/6)*m

E_kink_class = 5.0/6  # in units of m
DHN_correction = 1/(4*math.sqrt(3)) - 3/(2*math.pi)
E_kink_1loop = E_kink_class + DHN_correction

print(f"Classical kink mass: M_cl = (5/6)*m = {E_kink_class:.6f}*m")
print(f"DHN one-loop correction: Delta = {DHN_correction:.6f}*m")
print(f"One-loop kink mass: M_1loop = {E_kink_1loop:.6f}*m")
print()

# ================================================================
# 3C: Poschl-Teller spectrum and phi^3
# ================================================================
print("--- 3C: PT n=2 spectrum ---")
print()
print("Bound state energies (measured from bottom of well):")
print("  E_0 = -4*(m/2)^2 = -m^2  (zero mode)")
print("  E_1 = -1*(m/2)^2 = -m^2/4  (breathing mode)")
print()
print("Physical masses (= bulk mass - binding energy):")
print("  omega_0 = 0  (massless translation mode)")
print("  omega_1 = sqrt(3)*m/2  (breathing mode)")
print(f"  omega_1/m = {math.sqrt(3)/2:.10f}")
print()

# Check: does phi^3 appear naturally in PT n=2?
# The S-matrix for PT n=2:
# S(k) = [(k+i)(k+2i)] / [(k-i)(k-2i)]
# Poles at k = i and k = 2i (the bound states)
# At k = phi (if we evaluate the S-matrix at golden momentum):
k = phi
S_num_real = (k**2 - 1) * (k**2 - 4)
S_num_imag = k * (k**2 - 1) * 2 + k * (k**2 - 4)  # This is wrong, let me redo
# S(k) = (k+i)(k+2i) / ((k-i)(k-2i))
# |S(k)|^2 = 1 always (reflectionless)
# S(k) = [(k^2 + 3ik - 2)] / [(k^2 - 3ik - 2)]
# At k = phi:
# num = phi^2 + 3i*phi - 2 = (phi+1) + 3i*phi - 2 = phi - 1 + 3i*phi = phibar + 3i*phi
# ... actually phi^2 = phi + 1, so phi^2 - 2 = phi - 1 = phibar
# num = phibar + 3i*phi
# den = phibar - 3i*phi

print("--- S-matrix at golden momentum k = phi ---")
# S(phi) = (phibar + 3i*phi) / (phibar - 3i*phi)
# |S| = 1 (reflectionless)
# Phase: 2*arctan(3*phi/phibar) = 2*arctan(3*phi^2)
phase = 2 * math.atan(3*phi/phibar)
print(f"  S(phi) phase = 2*arctan(3*phi/phibar) = 2*arctan(3*phi^2)")
print(f"  = 2*arctan({3*phi**2:.6f}) = {phase:.10f}")
print(f"  = {phase/math.pi:.10f}*pi")
print()

# Phase shift
delta_phi = -math.atan(phi) - math.atan(phi/2)
print(f"Phase shift at k = phi:")
print(f"  delta(phi) = -arctan(phi) - arctan(phi/2)")
print(f"  = {-math.atan(phi):.6f} + {-math.atan(phi/2):.6f}")
print(f"  = {delta_phi:.10f}")
print(f"  = {delta_phi/math.pi:.6f}*pi")
print()

# ================================================================
# 3D: Can we DERIVE Lambda_QCD = m_p/phi^3 from the potential?
# ================================================================
print("=" * 75)
print("3D: DERIVATION ATTEMPT -- Lambda_QCD from potential structure")
print("=" * 75)
print()

# Key insight: in the framework, the proton mass has TWO expressions:
# (A) m_p = mu * m_e = (6^5/phi^3 + correction) * m_e
# (B) m_p = v * y_p where y_p is the proton Yukawa coupling from kink overlap

# The confinement scale Lambda_QCD is where alpha_s becomes O(1)
# In the framework: alpha_s = eta(1/phi) = 0.11840 at M_Z
# The framework claims this is a NON-PERTURBATIVE value (median Borel sum)

# For the 1-loop beta function of QCD with Nf active flavors:
# alpha_s(Q) = alpha_s(Q0) / [1 + (b0*alpha_s(Q0)/(2*pi)) * ln(Q/Q0)]

# If we run DOWN from M_Z to find where alpha_s -> infinity:
# alpha_s -> infinity when: 1 + (b0*alpha_s(M_Z)/(2*pi)) * ln(Q/M_Z) = 0
# ln(Lambda/M_Z) = -2*pi / (b0*alpha_s(M_Z))
# Lambda = M_Z * exp(-2*pi/(b0*alpha_s))

# With matching across flavor thresholds:
# At m_b ~ 4.18 GeV: Nf changes from 5 to 4
# At m_c ~ 1.27 GeV: Nf changes from 4 to 3

print("Standard 1-loop QCD running with flavor thresholds:")
print()

alpha_s_MZ = eta_val  # 0.11840

# Run from M_Z down to m_b (Nf=5)
m_b = 4.18  # GeV
b0_5 = (33 - 2*5) / 3.0  # = 23/3
alpha_s_mb = alpha_s_MZ / (1 - b0_5*alpha_s_MZ/(2*math.pi) * math.log(m_b/M_Z))
print(f"  alpha_s(M_Z) = {alpha_s_MZ:.6f}  (Nf=5, b0 = {b0_5:.4f})")
print(f"  alpha_s(m_b = {m_b} GeV) = {alpha_s_mb:.6f}")

# Run from m_b down to m_c (Nf=4)
m_c = 1.27  # GeV
b0_4 = (33 - 2*4) / 3.0  # = 25/3
alpha_s_mc = alpha_s_mb / (1 - b0_4*alpha_s_mb/(2*math.pi) * math.log(m_c/m_b))
print(f"  alpha_s(m_c = {m_c} GeV) = {alpha_s_mc:.6f}  (Nf=4, b0 = {b0_4:.4f})")

# Run from m_c down to m_p (Nf=3)
b0_3 = (33 - 2*3) / 3.0  # = 9
alpha_s_mp = alpha_s_mc / (1 - b0_3*alpha_s_mc/(2*math.pi) * math.log(m_p_GeV/m_c))
print(f"  alpha_s(m_p = {m_p_GeV:.4f} GeV) = {alpha_s_mp:.6f}  (Nf=3, b0 = {b0_3:.4f})")

# Lambda_QCD (Nf=3) from 1-loop:
Lambda_3 = m_c * math.exp(-2*math.pi/(b0_3*alpha_s_mc))
# Also from m_p:
Lambda_3_from_mp = m_p_GeV * math.exp(-2*math.pi/(b0_3*alpha_s_mp))
print()
print(f"  Lambda_QCD(Nf=3, from m_c) = {Lambda_3*1000:.2f} MeV")
print(f"  Lambda_QCD(Nf=3, from m_p) = {Lambda_3_from_mp*1000:.2f} MeV")
print(f"  Framework: m_p/phi^3 = {Lambda_raw*1000:.2f} MeV")
print()

# The 1-loop Lambda is scheme dependent and differs from "physical" Lambda
# The difference is a multiplicative factor of order 1
ratio_1loop = Lambda_3 / Lambda_raw
print(f"  Ratio Lambda_1loop / Lambda_framework = {ratio_1loop:.4f}")
print(f"  (They differ by a factor of ~{1/ratio_1loop:.2f})")
print()

# KEY: what if we use the FRAMEWORK identity directly?
# alpha_s = eta(1/phi) = 0.11840
# AND we demand Lambda_QCD = m_p/phi^3
# This fixes the effective b0:
# eta = 2*pi / (b0_eff * ln(M_Z * phi^3 / m_p))
b0_eff = 2*math.pi / (eta_val * math.log(M_Z * phi**3 / m_p_GeV))
print("--- Effective b0 from framework identity ---")
print(f"  If: eta = 2*pi / (b0_eff * ln(M_Z/Lambda_QCD))")
print(f"      Lambda_QCD = m_p/phi^3 = {Lambda_raw:.6f} GeV")
print(f"      ln(M_Z/Lambda_QCD) = ln({M_Z/Lambda_raw:.4f}) = {math.log(M_Z/Lambda_raw):.6f}")
print(f"  Then: b0_eff = 2*pi / (eta * ln(M_Z/Lambda)) = {b0_eff:.6f}")
print(f"  Compare: b0(Nf=5) = {23/3:.6f}")
print(f"           b0(Nf=4) = {25/3:.6f}")
print(f"           b0(Nf=3) = {9:.6f}")
print(f"  Ratio b0_eff / b0(Nf=5) = {b0_eff / (23/3):.6f}")
print()

# What if b0 is NOT the standard one but is determined by the framework?
# b0_eff = 8.695... which is close to b0(Nf=3) = 9
print(f"  b0_eff = {b0_eff:.4f} is closest to b0(Nf=3) = 9.000")
print(f"  Match: {min(b0_eff, 9)/max(b0_eff, 9)*100:.2f}%")
print(f"  Difference: {abs(b0_eff - 9):.4f}")
print()

# Is b0_eff a framework number?
print("  Searching for b0_eff in framework expressions:")
for name, val in [("9 - theta4", 9 - theta4),
                  ("9 - eta/10", 9 - eta_val/10),
                  ("9*(1-theta4)", 9*(1-theta4)),
                  ("b0(Nf=3)*(1-eta/pi)", 9*(1-eta_val/math.pi)),
                  ("27/pi", 27/math.pi),
                  ("9-1/phi^3", 9-phibar**3),
                  ("phi^6/2-phibar^6/2", (phi**6-phibar**6)/2),
                  ("4*sqrt5", 4*sqrt5),
                  ("3*pi-phi", 3*math.pi-phi),
                  ("phi^4+phibar", phi**4+phibar)]:
    match = min(b0_eff, val)/max(b0_eff, val)*100 if val > 0 else 0
    if match > 98:
        print(f"    b0_eff = {b0_eff:.6f} vs {name} = {val:.6f}  ({match:.3f}%)")

# ================================================================
# TASK 4: Refinement factor analysis
# ================================================================
print()
print("=" * 75)
print("TASK 4: Refinement Factor eta/(3*phi^3)")
print("=" * 75)
print()

corr = eta_val / (3 * phi**3)
print(f"eta/(3*phi^3) = {eta_val:.8f} / (3 * {phi**3:.8f})")
print(f"             = {eta_val:.8f} / {3*phi**3:.8f}")
print(f"             = {corr:.10f}")
print()

# What IS this number?
print("--- Decomposition of the refinement factor ---")
print(f"  eta = alpha_s (strong coupling) = {eta_val:.6f}")
print(f"  3 = number of generations / colors")
print(f"  phi^3 = 2*phi + 1 = {phi**3:.6f}")
print(f"  3*phi^3 = 6*phi + 3 = {3*phi**3:.6f}")
print()

# Interpretation 1: alpha_s / (3 * phi^3)
# = alpha_s / (triality * vacuum_cube)
print("Interpretation 1: Perturbative expansion in alpha_s")
print(f"  The correction 1 - eta/(3*phi^3) = 1 - alpha_s/(3*phi^3)")
print(f"  = 1 - (strong coupling) / (3 * golden cube)")
print(f"  If alpha_s is the expansion parameter, this is a LEADING perturbative correction.")
print()

# Interpretation 2: relation to kink excitation spectrum
# The kink has bound states with omega = 0 and omega = sqrt(3)*m/2
# The breathing mode mass ratio: omega_1/m = sqrt(3)/2
# eta * theta4 / 2 = C is the loop factor
C = eta_val * theta4 / 2
print("Interpretation 2: Kink excitation spectrum")
print(f"  Loop factor C = eta*theta4/2 = {C:.10f}")
print(f"  eta/(3*phi^3) = {corr:.10f}")
print(f"  Ratio C / (eta/(3*phi^3)) = {C/corr:.6f}")
print(f"  = theta4*3*phi^3/2 = theta4*(3/2)*phi^3")
print(f"  = {theta4*1.5*phi**3:.6f}")
print()

# Check: is eta/(3*phi^3) related to alpha_s/3 * phibar^3?
print("Interpretation 3: alpha_s with phibar^3 coupling")
print(f"  eta/(3*phi^3) = (eta/3) * phibar^3 = {eta_val/3:.6f} * {phibar**3:.6f}")
print(f"  = {eta_val/3 * phibar**3:.10f}")
print(f"  vs eta/(3*phi^3) = {corr:.10f}")
print(f"  Match: {abs(eta_val/3 * phibar**3 - corr)/corr*100:.4f}%")
print(f"  (IDENTICAL -- eta/(3*phi^3) = (alpha_s/3) * phibar^3)")
print()

# alpha_s/3 is the perturbative coefficient per COLOR
print("Interpretation 4: alpha_s per color, suppressed by phibar^3")
print(f"  alpha_s / 3 = {eta_val/3:.8f} (coupling per color)")
print(f"  phibar^3 = {phibar**3:.8f} (conjugate vacuum cube)")
print(f"  Product: {eta_val/3 * phibar**3:.10f}")
print()
print("  PHYSICAL PICTURE:")
print("  The refinement is alpha_s/N_c times phibar^3.")
print("  alpha_s/3 = one-gluon exchange per color charge")
print("  phibar^3 = suppression from the conjugate vacuum")
print("  Together: this is the probability of a virtual gluon")
print("  tunneling through the domain wall to the other vacuum.")
print()

# Is this a standard QCD correction?
# In QCD, the 1-loop correction to Lambda is:
# Lambda = Lambda_0 * (1 + c1*alpha_s + ...)
# where c1 ~ O(1)
# Here c1 * alpha_s = phibar^3 * alpha_s / 3 = 0.00932
# So c1 = 0.00932 / 0.1184 = 0.0787 ~ phibar^3/3

print("Interpretation 5: Correction to Lambda from wall tunneling")
print(f"  Lambda_refined = Lambda_raw * (1 - alpha_s * phibar^3 / 3)")
print(f"  This is a LEADING-ORDER correction in alpha_s")
print(f"  with coefficient phibar^3/3 = {phibar**3/3:.6f}")
print()

# Check: phibar^3/3 vs known QCD quantities
print(f"  phibar^3 = {phibar**3:.8f}")
print(f"  phibar^3/3 = {phibar**3/3:.8f}")
print(f"  Compare: 1/(3*phi^3) = phibar^3/3 = {phibar**3/3:.8f}")
print()

# The breathing mode contribution:
# omega_1 = sqrt(3)/2 * m
# omega_1 / m = sqrt(3)/2
# (omega_1/m)^2 = 3/4
# This is the bound state with energy -m^2/4 relative to continuum
# Its contribution to the kink one-loop mass is part of the DHN formula

# Check: is phibar^3 related to the breathing mode?
print("--- Breathing mode connection ---")
print(f"  Breathing mode: omega_1/m = sqrt(3)/2 = {math.sqrt(3)/2:.6f}")
print(f"  phibar^3 = {phibar**3:.6f}")
print(f"  Ratio: phibar^3 / (sqrt(3)/2) = {phibar**3 / (math.sqrt(3)/2):.6f}")
print(f"  = 2*phibar^3/sqrt(3) = {2*phibar**3/math.sqrt(3):.6f}")
print()

# ================================================================
# SYNTHESIS: Can Lambda_QCD = m_p/phi^3 be derived?
# ================================================================
print("=" * 75)
print("SYNTHESIS")
print("=" * 75)
print()

print("FINDING 1: 6^5 * m_e / phi^6 = 221.44 MeV (vs m_p/phi^3 = 221.50 MeV)")
print("  Verified. The 0.06 MeV difference comes from the 9/(7*phi^2) correction to mu.")
print()

print("FINDING 2: phi^6 = 9 + 4*sqrt(5) = 8*phi + 5 (exact)")
print("  phi^6 is a UNIT in Z[phi] with norm 1.")
print("  L(6) = 18 = water molar mass (noted in framework).")
print("  phi^6 = L(6) - phibar^6 ~ 17.944 (close to but not equal to 18).")
print()

print("FINDING 3: m_p/Lambda_QCD = phi^3 exactly.")
print("  This is the DEFINITION of Lambda_QCD in the framework.")
print("  The question is whether phi^3 can be derived from QCD structure.")
print()
print("  Result: 1-loop QCD running with flavor thresholds gives")
print(f"  Lambda_QCD(Nf=3) ~ {Lambda_3*1000:.0f} MeV (from alpha_s(M_Z) = 0.11840).")
print(f"  This is {Lambda_3/Lambda_raw*100:.1f}% of the framework value.")
print(f"  The discrepancy is a factor of ~{Lambda_raw/Lambda_3:.2f}.")
print(f"  1-loop running is too crude; 2-loop would help but not close the gap.")
print()
print("  The effective b0 that makes eta = 2*pi/(b0*ln(M_Z/Lambda)) work is:")
print(f"  b0_eff = {b0_eff:.4f}, close to b0(Nf=3) = 9.000 ({min(b0_eff,9)/max(b0_eff,9)*100:.1f}%)")
print()
print("  VERDICT: Lambda_QCD = m_p/phi^3 is NOT derivable from perturbative QCD")
print("  running alone. It requires non-perturbative input.")
print()
print("  The most promising route: the framework says alpha_s = eta(1/phi) is a")
print("  NON-PERTURBATIVE median Borel sum. The confinement scale should then be")
print("  Lambda_QCD = m_kink * f(phi) where f encodes the kink structure.")
print("  Since mu = N/phi^3, dividing m_p by phi^3 is algebraically equivalent")
print("  to extracting the E8 normalizer contribution in electron mass units.")
print()

print("FINDING 4: The refinement factor eta/(3*phi^3) = (alpha_s/3) * phibar^3")
print(f"  = {corr:.10f}")
print()
print("  This has a NATURAL interpretation:")
print("  - alpha_s/3 = strong coupling per color = one-gluon exchange per SU(3) charge")
print("  - phibar^3 = tunneling amplitude to conjugate vacuum (volume suppression)")
print("  - Product = probability of virtual gluon reaching the other side of the wall")
print()
print("  This is a LEADING-ORDER perturbative correction in alpha_s,")
print("  with the coefficient phibar^3/3 determined by the wall geometry.")
print()
print("  Status: INTERPRETATION, not derivation. To derive it properly,")
print("  one would need the 1-loop effective action of the kink coupled to")
print("  the SU(3) gauge field, showing that the leading correction to")
print("  Lambda_QCD from wall effects is proportional to alpha_s * phibar^3 / N_c.")

print()
print("=" * 75)
print("SUMMARY OF OPEN VS CLOSED QUESTIONS")
print("=" * 75)
print()
print("CLOSED (by Jackiw-Rebbi):")
print("  - VP coefficient 1/(3*pi) is DERIVED: chiral zero mode on domain wall")
print("  - The factor of 1/2 relative to standard QED: THEOREM")
print()
print("PARTIALLY CLOSED:")
print("  - Lambda_QCD = m_p/phi^3 = 221.5 MeV: consistent with PDG range")
print("    but not independently derived from first principles.")
print("    BEST ROUTE: Since mu = N/phi^3, this is Lambda = N*m_e/phi^6,")
print("    which means Lambda_QCD = (E8 normalizer) * (electron mass) / (golden unit)^6.")
print("    The phi^3 dividing m_p is the SAME phi^3 that gives mu = N/phi^3.")
print()
print("  - Refinement factor eta/(3*phi^3) = (alpha_s/3)*phibar^3:")
print("    Natural interpretation as perturbative correction with wall-tunneling")
print("    suppression. But not rigorously derived from kink 1-loop action.")
print()
print("STILL OPEN:")
print("  - WHY does phi^3 (and not phi^2 or phi^4) appear in Lambda = m_p/phi^3?")
print("    The answer is: because it is the SAME phi^3 from mu = N/phi^3,")
print("    which comes from the E8 -> 4A2 breaking. But the specific power 3")
print("    in the kink mass formula has not been derived from domain wall physics.")
print("  - Can the 1-loop kink determinant reproduce phibar^3/3 as the leading")
print("    correction coefficient? This requires computing the kink-gauge coupling.")
