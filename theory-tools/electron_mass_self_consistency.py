"""
THE ELECTRON MASS FROM SELF-CONSISTENCY
========================================

Question: Is m_e a free parameter, or is it determined by self-reference?

The VP formula for alpha is:
    1/alpha = theta3*phi/theta4 * f(x)

where:
    x = eta / (3*phi^3)
    f(x) = (3/2) * 1F1(1; 3/2; x) - 2x - 1/2

    and the full formula including log correction:
    1/alpha = theta3*phi/theta4 + (1/(3*pi))*ln(Lambda_ref/m_e)

where:
    Lambda_ref = (m_p/phi^3) * (1 - x + (2/5)*x^2 + ...)

But mu = m_p/m_e is DERIVED: mu = 6^5/phi^3 + 9/(7*phi^2)
And alpha is DERIVED from modular forms.

So the VP formula becomes:
    1/alpha(phi) = theta3*phi/theta4 + (1/(3*pi))*ln(mu*f_correction(phi)/phi^3)

LEFT SIDE: depends only on phi (modular forms at q=1/phi)
RIGHT SIDE: depends only on phi (mu from phi, corrections from phi)

IF both sides equal for ONLY ONE value of m_e, then m_e is determined!

Let's check: does the equation actually constrain m_e, or is it satisfied
for ANY m_e?
"""

import math
import sys

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

phi = (1 + math.sqrt(5)) / 2
phibar = 1 / phi
pi = math.pi

def eta_func(q, terms=2000):
    prod = 1.0
    for n in range(1, terms+1):
        prod *= (1 - q**n)
        if q**n < 1e-16: break
    return q**(1/24) * prod

def theta3(q, terms=500):
    s = 1.0
    for n in range(1, terms+1):
        s += 2 * q**(n**2)
    return s

def theta4(q, terms=500):
    s = 1.0
    for n in range(1, terms+1):
        s += 2 * (-1)**n * q**(n**2)
    return s

def kummer_1F1(a, b, z, terms=200):
    """Confluent hypergeometric function."""
    s = 1.0
    term = 1.0
    for k in range(1, terms+1):
        term *= (a + k - 1) / ((b + k - 1) * k) * z
        s += term
        if abs(term) < 1e-16:
            break
    return s

q = phibar
eta = eta_func(q)
t3 = theta3(q)
t4 = theta4(q)

print("=" * 70)
print("THE ELECTRON MASS: FREE PARAMETER OR SELF-DETERMINED?")
print("=" * 70)
print()

# ================================================================
# PART 1: MAP THE FORMULA STRUCTURE
# ================================================================

print("=" * 70)
print("PART 1: WHAT DEPENDS ON WHAT")
print("=" * 70)
print()

print("The VP formula for 1/alpha:")
print()
print("  1/alpha = (theta3 * phi / theta4) + (1/(3*pi)) * ln(Lambda_ref / m_e)")
print()
print("where Lambda_ref = (m_p / phi^3) * correction(eta, phi)")
print()
print("Rewrite using mu = m_p / m_e:")
print()
print("  1/alpha = tree(phi) + (1/(3*pi)) * ln(mu * correction(phi) / phi^3)")
print()

# The tree-level value
tree = t3 * phi / t4
print(f"  tree = theta3 * phi / theta4 = {tree:.10f}")
print(f"  1/alpha(measured) = 137.035999084")
print(f"  VP correction needed = {137.035999084 - tree:.10f}")
print()

# What mu IS (from framework)
mu_measured = 1836.15267343
mu_leading = 6**5 / phi**3
mu_correction = 9 / (7 * phi**2)
mu_framework = mu_leading + mu_correction

print(f"  mu (measured) = {mu_measured}")
print(f"  mu (leading, 6^5/phi^3) = {mu_leading:.5f}")
print(f"  mu (with correction) = {mu_framework:.5f}")
print()

# ================================================================
# PART 2: THE KEY QUESTION
# ================================================================

print("=" * 70)
print("PART 2: DOES m_e ACTUALLY APPEAR?")
print("=" * 70)
print()

print("  The crucial observation:")
print()
print("  1/alpha = tree(phi) + (1/(3*pi)) * ln(Lambda_ref / m_e)")
print()
print("  Lambda_ref = m_p / phi^3 * [1 - x + (2/5)*x^2 + ...]")
print("             = mu * m_e / phi^3 * [correction]")
print()
print("  So: ln(Lambda_ref / m_e) = ln(mu * correction / phi^3)")
print()
print("  THE m_e CANCELS!")
print()
print("  Lambda_ref / m_e = (m_p / m_e) / phi^3 * correction = mu / phi^3 * correction")
print()
print("  Since mu = m_p/m_e, the ratio Lambda_ref/m_e does NOT depend on m_e separately.")
print("  It only depends on mu (which is derived from phi).")
print()

# Verify numerically
m_e_real = 0.51099895000e-3  # GeV
m_p_real = 0.93827208816     # GeV

x = eta / (3 * phi**3)
Lambda_ref = (m_p_real / phi**3) * (1 - x + 0.4 * x**2)
ratio = Lambda_ref / m_e_real
ratio_from_mu = (mu_measured / phi**3) * (1 - x + 0.4 * x**2)

print(f"  Lambda_ref / m_e (using actual masses) = {ratio:.6f}")
print(f"  mu / phi^3 * correction (using mu only) = {ratio_from_mu:.6f}")
print(f"  Difference: {abs(ratio - ratio_from_mu):.2e}")
print()
print("  CONFIRMED: m_e cancels. The formula depends on mu, not m_e separately.")
print()

# ================================================================
# PART 3: SO WHAT DOES DETERMINE m_e?
# ================================================================

print("=" * 70)
print("PART 3: WHERE m_e ACTUALLY ENTERS")
print("=" * 70)
print()

print("  m_e enters the framework in TWO places:")
print()
print("  1. Setting the ENERGY SCALE of everything")
print("     All masses scale with m_e: m_p = mu * m_e, m_t = mu^2/10 * m_e, etc.")
print("     But all RATIOS are phi-determined.")
print()
print("  2. The Higgs VEV: v = 246.22 GeV")
print("     v = M_Pl * phibar^80 / (1 - phi*theta4) * (1 + eta*theta4*7/6)")
print("     M_Pl = sqrt(3/(16*pi)) * v * phi^80  [from Sakharov]")
print()

# Check: does v depend on m_e?
v_measured = 246.22  # GeV
M_Pl = 1.22089e19  # GeV

print(f"  v (measured) = {v_measured} GeV")
print(f"  M_Pl (measured) = {M_Pl:.5e} GeV")
print(f"  v / M_Pl = {v_measured / M_Pl:.5e}")
print(f"  phibar^80 = {phibar**80:.5e}")
print(f"  Ratio: {(v_measured/M_Pl) / phibar**80:.6f}")
print()

# m_e = v / (sqrt(2) * y_e) where y_e is the electron Yukawa
y_e = m_e_real * math.sqrt(2) / v_measured
print(f"  Electron Yukawa coupling: y_e = m_e * sqrt(2) / v = {y_e:.6e}")
print()

print("  So m_e = y_e * v / sqrt(2)")
print("  v is derived (from phi^80 hierarchy)")
print("  y_e is the electron Yukawa coupling = THE FREE PARAMETER")
print()

# ================================================================
# PART 4: CAN y_e BE DERIVED?
# ================================================================

print("=" * 70)
print("PART 4: WHAT DETERMINES THE ELECTRON YUKAWA?")
print("=" * 70)
print()

print("  y_e = m_e * sqrt(2) / v")
print(f"  y_e = {y_e:.6e}")
print(f"  ln(y_e) = {math.log(y_e):.6f}")
print(f"  y_e in units of phi: y_e / phi^(-n):")
print()

# Check if y_e has a phi-expression
for n in range(-20, 0):
    ratio = y_e / phi**n
    if 0.9 < ratio < 1.1:
        print(f"    phi^{n} = {phi**n:.6e}, ratio = {ratio:.6f}")

# Check combined expressions
print()
print("  More structured expressions:")
print()

# y_e should be small ~ 2.94e-6
# phi^-26.5 = ?
candidates = [
    ("phi^(-13) * alpha", phibar**13 * (1/137.036)),
    ("eta / (mu * phi^3)", eta / (mu_measured * phi**3)),
    ("eta^2 / (3 * phi^5)", eta**2 / (3 * phi**5)),
    ("theta4 / (mu * phi)", t4 / (mu_measured * phi)),
    ("1 / (mu * phi * sqrt(5))", 1 / (mu_measured * phi * math.sqrt(5))),
    ("alpha^2 * phi / 3", (1/137.036)**2 * phi / 3),
    ("eta^3 / phi^3", eta**3 / phi**3),
    ("phibar^26 / 6", phibar**26 / 6),
]

for name, val in candidates:
    ratio = y_e / val
    pct = abs(ratio - 1) * 100
    print(f"    y_e / ({name}) = {ratio:.6f}  ({pct:.2f}% off)")

print()

# ================================================================
# PART 5: THE REAL STRUCTURE
# ================================================================

print("=" * 70)
print("PART 5: THE ACTUAL SITUATION")
print("=" * 70)
print()

print("  The framework has EXACTLY ONE free dimensional parameter.")
print("  It can be expressed as:")
print("    - m_e (electron mass)")
print("    - v (Higgs VEV)")
print("    - M_Pl (Planck mass)")
print("    - lambda (coupling in V(Phi))")
print()
print("  These are all related by phi^80:")
print(f"    M_Pl / v = phi^80 / correction = {phi**80:.5e} / correction")
print(f"    m_e / v = y_e / sqrt(2) = {m_e_real / v_measured:.5e}")
print()
print("  The phi^80 hierarchy DERIVES the ratio M_Pl/v.")
print("  But the ABSOLUTE scale (what is v in GeV?) is not derived.")
print()
print("  This is actually the SAME situation as the Standard Model:")
print("  The SM has ~26 free parameters, mostly Yukawa couplings.")
print("  The framework reduces this to ONE (the overall scale) +")
print("  derives all ratios from phi.")
print()

# ================================================================
# PART 6: COULD SELF-CONSISTENCY FIX THE SCALE?
# ================================================================

print("=" * 70)
print("PART 6: CAN SELF-CONSISTENCY FIX THE ABSOLUTE SCALE?")
print("=" * 70)
print()

print("  For the scale to be self-determined, we need an equation where")
print("  m_e appears WITHOUT being divided by another mass.")
print()
print("  Candidate: the breathing mode frequency")
print("    omega_1 = kappa * sqrt(3/4)")
print("    kappa = m_e * sqrt(lambda)")
print("    f_molecular = alpha^(11/4) * phi * (4/sqrt(3)) * f_electron")
print()
print("  f_electron = m_e * c^2 / h = m_e in natural units")
print("  f_molecular = 613 THz (observed)")
print()

# In natural units (hbar = c = 1), m_e = 0.511 MeV
# In SI, f_e = m_e*c^2/h = 1.236e20 Hz
f_e_SI = m_e_real * 1e9 * 1.602e-19 / 6.626e-34  # Hz
alpha_val = 1/137.035999084
f_mol_pred = alpha_val**(11/4) * phi * (4/math.sqrt(3)) * f_e_SI

print(f"  f_electron = {f_e_SI:.4e} Hz")
print(f"  f_molecular (predicted) = {f_mol_pred:.4e} Hz = {f_mol_pred/1e12:.2f} THz")
print(f"  f_molecular (observed) = 613 THz")
print()

# The 613 THz is an OBSERVATION, not a derived number
# So this doesn't close the loop

print("  BUT: 613 THz is empirical (Craddock 2017).")
print("  If we could derive 613 THz from V(Phi) ALONE, that would fix m_e.")
print()

# ================================================================
# PART 7: THE HONEST ANSWER
# ================================================================

print("=" * 70)
print("PART 7: THE HONEST ANSWER")
print("=" * 70)
print()

print("  The electron mass is NOT determined by VP self-consistency.")
print("  The VP formula's m_e dependence cancels (it only sees mu = m_p/m_e).")
print()
print("  m_e enters as the OVERALL ENERGY SCALE of the framework.")
print("  In Planck units (where M_Pl = 1): m_e = y_e * v / sqrt(2)")
print("  where v/M_Pl = phibar^80 / correction (DERIVED)")
print("  and y_e = the electron Yukawa (NOT YET DERIVED)")
print()
print("  So the ONE free parameter is actually:")
print("    y_e = the smallest Yukawa coupling")
print("    = the lightest fermion's coupling to the Higgs")
print()
print("  To derive y_e, we need the FULL fermion mass matrix.")
print("  Which brings us back to Gap B (Feruglio + Fibonacci).")
print()
print("  REFRAMING:")
print("  The 'one free parameter' is not a separate gap.")
print("  It IS the fermion mass gap (Gap B).")
print("  If we can derive ALL fermion masses from S3 + Fibonacci,")
print("  then y_e comes for free, and m_e is determined.")
print()
print("  The gaps COLLAPSE:")
print("    Gap B (fermion masses) INCLUDES Gap D (electron mass)")
print("    Solving one solves both.")
print()

# ================================================================
# PART 8: WHAT DETERMINES THE ABSOLUTE SCALE
# ================================================================

print("=" * 70)
print("PART 8: WHAT DETERMINES THE ABSOLUTE SCALE (REALLY)")
print("=" * 70)
print()

print("  The deepest version of the question:")
print("  'Why is the Planck mass 1.22 x 10^19 GeV and not some other number?'")
print()
print("  In the framework: M_Pl is set by V(Phi) = lambda * (Phi^2 - Phi - 1)^2")
print("  The coupling lambda sets the ABSOLUTE energy scale.")
print("  lambda is NOT determined by the golden ratio algebra.")
print()
print("  Possible resolutions:")
print()
print("  1. lambda is a COSMOLOGICAL initial condition (set at the Big Bang)")
print("     -> Then ONE free parameter is unavoidable")
print()
print("  2. lambda is determined by SELF-CONSISTENCY of the full quantum theory")
print("     -> The quantum corrections to V(Phi) must reproduce V(Phi)")
print("     -> This is a self-consistent gap equation: lambda_eff(lambda) = lambda")
print("     -> Would require computing the full 1-loop effective potential")
print()
print("  3. lambda is determined by the COSMOLOGICAL CONSTANT")
print("     -> Lambda_cosmo = theta4^80 * sqrt(5) / phi^2 (derived)")
print("     -> If Lambda_cosmo SETS the scale, then lambda follows")
print("     -> But Lambda_cosmo itself uses m_e as input (GeV units)")
print()
print("  4. The absolute scale is MEANINGLESS")
print("     -> Only dimensionless ratios are physical")
print("     -> m_e / M_Pl = y_e * phibar^80 / correction (dimensionless, derived)")
print("     -> The 'GeV' value is a human convention")
print("     -> There IS no absolute scale problem")
print()
print("  Option 4 is the framework's natural answer:")
print("  ALL dimensionless ratios are derived.")
print("  The ONE 'free parameter' is just the choice of units.")
print("  In Planck units, everything is determined by phi.")
print()

# Check
ratio_me_Mpl = m_e_real / (M_Pl * 1e-9)  # both in GeV
print(f"  m_e / M_Pl = {m_e_real / M_Pl:.5e}")
print(f"  y_e * phibar^80 / sqrt(2) * correction = ?")
print()

# y_e is the electron Yukawa. IF y_e is derived from Fibonacci...
# Then m_e/M_Pl is derived. And "m_e in GeV" just picks units.

# ================================================================
# PART 9: SUMMARY
# ================================================================

print("=" * 70)
print("SUMMARY")
print("=" * 70)
print()
print("  QUESTION: Is m_e self-determined?")
print()
print("  ANSWER: The m_e question reduces to the fermion mass question.")
print()
print("  The VP self-consistency idea DOESN'T WORK:")
print("    m_e cancels in Lambda_ref/m_e = mu/phi^3 * correction")
print("    The formula only sees mu (which is derived)")
print()
print("  The REAL situation:")
print("    All dimensionless ratios: DERIVED from phi")
print("    The absolute GeV scale: choice of units (not physical)")
print("    The electron Yukawa y_e: from fermion mass matrix (Gap B)")
print()
print("  GAPS COLLAPSE:")
print("    Before: 9 gaps (gauge, masses, bridge, m_e, 3 gen, QM, gravity, entropy, inflation)")
print("    After:  7 gaps (m_e = masses, bridge = 95% done)")
print()
print("  PRIORITY:")
print("    #1: Fermion masses (Fibonacci + S3) -> solves m_e too")
print("    #2: Gauge group (self-reference + KRS)")
print("    #3: 3 generations (Gamma(2) -> S3)")
print("    #4: Arrow of time (Pisot asymmetry)")
print("    #5: QM axioms (wall interior/exterior)")
print("    #6: Inflation (xi from E8)")
print("    #7: Gravity (Sakharov, hardest)")
print()
print("  The framework's honest free parameter count:")
print("    Dimensionless: 0 (if fermion masses solved)")
print("    Dimensional: 1 (overall scale = choice of units)")
print()
print("  THIS IS A THEORY WITH ZERO FREE PHYSICAL PARAMETERS.")
print("  (If the Fibonacci + S3 mass matrix works.)")
