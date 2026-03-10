#!/usr/bin/env python3
"""
factor_8_derivation.py -- Investigate the factor of 8 in the Born-Oppenheimer
chain: f_mol = 8 * f_Rydberg / sqrt(mu) = 614.2 THz

The formula gives the closest first-principles match to the Craddock aromatic
consciousness frequency (613 +/- 8 THz).  This script systematically asks:
  1. Where does the 8 come from?
  2. Is it the *only* good prefactor?
  3. Does it connect to framework numbers {phi, eta, theta, 3, 2/3, E8}?
  4. Can modular forms at q = 1/phi produce 3/16 or related fractions?

Author: Interface Theory project
Date: 2026-02-25
"""

import math

# ===========================================================================
# FUNDAMENTAL CONSTANTS (NIST 2022 CODATA)
# ===========================================================================
c      = 2.99792458e8       # m/s
h_pl   = 6.62607015e-34     # J s
hbar   = 1.054571817e-34    # J s
m_e    = 9.1093837015e-31   # kg
m_p    = 1.67262192369e-27  # kg
e_ch   = 1.602176634e-19    # C
eps0   = 8.8541878128e-12   # F/m
k_B    = 1.380649e-23       # J/K

alpha  = 7.2973525693e-3
mu     = m_p / m_e          # 1836.15267...
phi    = (1 + math.sqrt(5)) / 2

# Rydberg frequency
R_inf  = m_e * e_ch**4 / (8 * eps0**2 * h_pl**3 * c)
f_R    = R_inf * c          # Hz  (~3.2898e15)
E_R_eV = 13.605693122994    # eV

# Target
f_target = 613e12           # Hz  (Craddock 2017)
f_target_THz = 613.0

SEP  = "=" * 78
DASH = "-" * 78

print(SEP)
print("FACTOR-8 DERIVATION:  8 * f_Rydberg / sqrt(mu) = 614 THz")
print(SEP)
print()
print(f"  mu          = {mu:.8f}")
print(f"  phi         = {phi:.10f}")
print(f"  alpha       = 1/{1/alpha:.6f}")
print(f"  f_Rydberg   = {f_R:.6e} Hz  = {f_R/1e12:.2f} THz")
print(f"  Target      = {f_target_THz:.1f} +/- 8 THz  (Craddock 2017)")
print()

# ===========================================================================
# PART 1: The Born-Oppenheimer energy hierarchy
# ===========================================================================
print(SEP)
print("PART 1:  BORN-OPPENHEIMER ENERGY HIERARCHY")
print(SEP)
print("""
  Standard BO theory (Born & Oppenheimer 1927, Annalen der Physik):
  The expansion parameter is kappa = (m_e / M_nuclear)^(1/4).

  For a hydrogen-mass nucleus (proton), kappa = mu^(-1/4) = 0.1527.

  Energy scales:
    Electronic  :  E_el  ~ E_R             =  13.6 eV
    Vibrational :  E_vib ~ E_el * kappa^2  =  E_R / sqrt(mu) =  0.317 eV
    Rotational  :  E_rot ~ E_el * kappa^4  =  E_R / mu       =  7.4 meV

  The BO vibrational frequency scale is:
    f_vib(BO) = f_R / sqrt(mu) = f_R * kappa^2
""")

f_BO = f_R / math.sqrt(mu)
print(f"  f_BO = f_R / sqrt(mu)  = {f_BO/1e12:.4f} THz")
print(f"  This is the VIBRATIONAL scale, not the electronic scale.")
print(f"  Measured O-H stretch ~ 102 THz.  Ratio to f_BO = {102e12/f_BO:.4f}")
print(f"    (close to 4/3 = 1.3333, but this is empirical)")
print()

# The formula 8 * f_R / sqrt(mu) is NOT simply f_BO.
# It is 8 * f_BO.  The factor 8 raises the VIBRATIONAL scale back toward
# the ELECTRONIC scale, but by a specific amount.
print(f"  8 * f_BO = {8*f_BO/1e12:.4f} THz   <-- this is the claimed formula")
print(f"  Target   = {f_target_THz:.1f} THz")
print(f"  Match    = {100*(1-abs(8*f_BO/1e12 - f_target_THz)/f_target_THz):.2f}%")
print()

# ===========================================================================
# PART 2:  The Balmer-beta connection
# ===========================================================================
print(SEP)
print("PART 2:  THE BALMER-BETA CONNECTION")
print(SEP)
print("""
  The REAL origin of the formula is NOT "f_BO times 8."
  Rather, 8 * f_R / sqrt(mu) can be rewritten as:

    f_mol = (128/3) * f_Balmer-beta / sqrt(mu)?    [NO -- let us work it out]

  Actually:
    f_Balmer-beta  = f_R * (1/n1^2 - 1/n2^2)
                   = f_R * (1/4 - 1/16)
                   = f_R * 3/16

  So:  8 * f_R / sqrt(mu)
     = 8/1 * f_R / sqrt(mu)
     = (8 * 16/3) * (3/16) * f_R / sqrt(mu)
     = (128/3)    * f_Balmer-beta / sqrt(mu)    -- ugly

  The factor 8 does NOT come from the Balmer-beta line directly.
  Let's understand it properly.
""")

f_Hbeta = f_R * 3.0/16.0
print(f"  f_Balmer-beta = f_R * 3/16  = {f_Hbeta/1e12:.4f} THz  = {c/f_Hbeta*1e9:.1f} nm")
print(f"  (This is the H-beta line at 486 nm -- blue hydrogen line)")
print()

# Key observation: the 613 THz target IS very close to f_Balmer-beta
print(f"  DIRECT COMPARISON:")
print(f"    f_target / f_Balmer-beta = {f_target / f_Hbeta:.6f}")
print(f"    f_target = f_Balmer-beta * {f_target / f_Hbeta:.4f}")
print(f"    f_target IS the Balmer-beta line to {abs(1 - f_target/f_Hbeta)*100:.2f}%")
print()

# f_Craddock / f_Rydberg
ratio_to_R = f_target / f_R
print(f"  f_Craddock / f_Rydberg = {ratio_to_R:.6f}")
print(f"  3/16 = {3/16:.6f}")
print(f"  Match = {100*(1-abs(ratio_to_R - 3/16)/(3/16)):.2f}%")
print()

# ===========================================================================
# PART 3:  DECOMPOSING THE FACTOR 8
# ===========================================================================
print(SEP)
print("PART 3:  DECOMPOSING THE FACTOR 8")
print(SEP)
print("""
  The formula is:  f_mol = 8 * f_R / sqrt(mu)

  Let us see what 8/sqrt(mu) IS in terms of hydrogen quantum numbers.

  f_R / sqrt(mu) = BO vibrational scale = 76.77 THz.
  But molecular ELECTRONIC transitions are NOT at the BO vib scale.
  They are at the ATOMIC electronic scale times a factor < 1.

  In a free-electron model of conjugated pi-electrons:
    E_HOMO-LUMO = (hbar^2 / 2 m_e) * (pi/L)^2 * (2N+1)

  where L = ring circumference (or box length) and N = number of
  filled orbitals.

  For benzene (particle on a ring, 6 pi electrons, 3 filled levels):
    E = (hbar^2 / m_e) * 7 / (2 R_ring^2)
  with R_ring ~ 140 pm * 6 / (2*pi) = 133.7 pm.
  Predicted lambda ~ 194 nm (experiment: 256 nm first allowed transition).

  In the Huckel model, benzene HOMO-LUMO gap = 2*beta where beta ~ 2.4 eV.
  So E_gap ~ 4.8 eV -> 1160 THz.  INDIVIDUAL benzene absorbs at ~256 nm
  = 1172 THz.  This is ~1170 THz, almost exactly TWICE the target 613 THz.

  The factor of ~2 reduction from individual to collective is precisely
  what London-force coupling of ~86 oscillators produces (Craddock 2017).

  So the PHYSICAL decomposition is:
    613 THz = (individual aromatic pi*-pi* ~ 1170 THz) / ~1.9

  And 1170 THz / f_R = 0.356 = roughly 3/8.
  So INDIVIDUAL aromatic ~ (3/8) * f_Rydberg.
  And COLLECTIVE aromatic ~ (3/16) * f_Rydberg = Balmer-beta.

  The factor 2 reduction from individual to collective is the
  London-force coupling effect, NOT a fundamental constant.
""")

# Benzene first UV absorption
f_benzene_UV = c / (256e-9)  # Hz
print(f"  Benzene 1st UV absorption: {f_benzene_UV/1e12:.1f} THz  (256 nm)")
print(f"  Ratio to 613 THz: {f_benzene_UV/f_target:.3f}")
print(f"  Ratio to f_R:     {f_benzene_UV/f_R:.4f}  (vs 3/8 = {3/8:.4f})")
print()

# ===========================================================================
# PART 4:  SYSTEMATIC SCAN OF ALL HYDROGEN TRANSITIONS
# ===========================================================================
print(SEP)
print("PART 4:  SYSTEMATIC SCAN -- ALL HYDROGEN LINES vs 613 THz")
print(SEP)
print("""
  For each hydrogen transition n2 -> n1, compute f = f_R * (1/n1^2 - 1/n2^2).
  Compare directly with f_target = 613 THz.
  Also check f / sqrt(mu) and C * f_R / sqrt(mu) for integer C.
""")

print(f"  {'n1':>3} {'n2':>3} {'Series':>10} {'Greek':>6} {'f (THz)':>12} "
      f"{'lam (nm)':>10} {'vs 613':>10} {'f/target':>10}")
print(f"  {'-'*3} {'-'*3} {'-'*10} {'-'*6} {'-'*12} {'-'*10} {'-'*10} {'-'*10}")

series_names = {1: "Lyman", 2: "Balmer", 3: "Paschen", 4: "Brackett"}
greek_names = {0: "alpha", 1: "beta", 2: "gamma", 3: "delta", 4: "eps"}

best_match = None
best_err = 999.0

for n1 in range(1, 8):
    for n2 in range(n1+1, min(n1+8, 20)):
        f_line = f_R * (1.0/n1**2 - 1.0/n2**2)
        lam_nm = c / f_line * 1e9
        ratio = f_line / f_target
        err = abs(1.0 - ratio)
        series = series_names.get(n1, f"n1={n1}")
        greek = greek_names.get(n2-n1-1, str(n2-n1))

        if err < 0.02:  # within 2%
            marker = " <---"
        else:
            marker = ""

        if err < best_err:
            best_err = err
            best_match = (n1, n2, f_line, lam_nm, ratio)

        print(f"  {n1:>3} {n2:>3} {series:>10} {greek:>6} {f_line/1e12:>10.3f}   "
              f"{lam_nm:>8.1f}   {err*100:>8.2f}%   {ratio:>8.4f}{marker}")

n1b, n2b, fb, lamb, rb = best_match
print(f"\n  BEST MATCH: n={n2b} -> n={n1b}  "
      f"f = {fb/1e12:.3f} THz  lambda = {lamb:.1f} nm  "
      f"error = {abs(1-rb)*100:.3f}%")
print(f"  This is the BALMER-BETA line (n=4 -> n=2).")
print()

# ===========================================================================
# PART 5:  SCAN INTEGER PREFACTORS for C * f_R / sqrt(mu) = 613 THz
# ===========================================================================
print(SEP)
print("PART 5:  SCAN PREFACTORS  C * f_R / sqrt(mu)")
print(SEP)
print()

# f_R / sqrt(mu) = BO vibrational scale
f_BO_val = f_R / math.sqrt(mu)
C_exact = f_target / f_BO_val
print(f"  f_R / sqrt(mu) = {f_BO_val/1e12:.4f} THz")
print(f"  Exact prefactor C = {f_target_THz} / {f_BO_val/1e12:.4f} = {C_exact:.6f}")
print(f"  Nearest integer = {round(C_exact)}")
print()

# Scan C from 1 to 20
print(f"  {'C':>4} {'f_pred (THz)':>14} {'Error vs 613':>14} {'Framework connection':>40}")
print(f"  {'-'*4} {'-'*14} {'-'*14} {'-'*40}")

for C in range(1, 21):
    f_pred = C * f_BO_val / 1e12
    err = abs(f_pred - f_target_THz) / f_target_THz * 100
    # Check framework connections
    notes = ""
    if C == 1:   notes = "trivial BO scale"
    elif C == 2: notes = "n=2 (PT bound states)"
    elif C == 3: notes = "triality"
    elif C == 4: notes = "L(3) = 4"
    elif C == 6: notes = "benzene carbons"
    elif C == 7: notes = "L(4) = 7"
    elif C == 8: notes = "*** rank(E8) = 8 = dim of Cartan"
    elif C == 10: notes = "h/3 = Coxeter/triality"
    elif C == 11: notes = "L(5) = 11"
    elif C == 18: notes = "L(6) = 18 = water molar mass"

    marker = " <---" if C == 8 else ""
    print(f"  {C:>4} {f_pred:>12.2f}   {err:>11.2f}%   {notes:>40}{marker}")

print()

# Also scan half-integer and rational prefactors
print(f"  Rational prefactors (p/q for small p,q):")
print(f"  {'p/q':>8} {'C':>10} {'f_pred':>12} {'Error':>10} {'Note':>30}")
print(f"  {'-'*8} {'-'*10} {'-'*12} {'-'*10} {'-'*30}")

best_rational = []
for p in range(1, 30):
    for q in range(1, 15):
        C_rat = p / q
        if C_rat < 3 or C_rat > 15:
            continue
        f_pred = C_rat * f_BO_val / 1e12
        err = abs(f_pred - f_target_THz) / f_target_THz * 100
        if err < 1.0:
            note = ""
            if p == 8 and q == 1: note = "8 = rank(E8)"
            if p == 16 and q == 2: note = "= 8"
            if p == 24 and q == 3: note = "= 8 = 24/3 (24=|roots(4A2)|)"
            if abs(C_rat - 3*math.sqrt(mu)/16/f_R*f_target) < 0.01:
                note = "related to 3/16 Balmer"
            best_rational.append((p, q, C_rat, f_pred, err, note))

best_rational.sort(key=lambda x: x[4])
for p, q, C_rat, f_pred, err, note in best_rational[:15]:
    print(f"  {p:>3}/{q:<3}  {C_rat:>10.4f} {f_pred:>10.2f}   {err:>8.4f}%   {note:>30}")

print()

# ===========================================================================
# PART 6:  MODULAR FORMS AND 3/16
# ===========================================================================
print(SEP)
print("PART 6:  CAN MODULAR FORMS AT q = 1/phi PRODUCE 3/16?")
print(SEP)
print()

# Compute modular forms at q = 1/phi
q_val = 1.0 / phi
N_terms = 200

# Dedekind eta
eta_prod = 1.0
for n in range(1, N_terms+1):
    eta_prod *= (1.0 - q_val**n)
eta = q_val**(1.0/24.0) * eta_prod

# Jacobi theta functions
theta2 = 0.0
for n in range(N_terms):
    theta2 += q_val**(n*(n+1))
theta2 *= 2.0 * q_val**0.25

theta3 = 1.0
for n in range(1, N_terms+1):
    theta3 += 2.0 * q_val**(n*n)

theta4 = 1.0
for n in range(1, N_terms+1):
    theta4 += 2.0 * ((-1)**n) * q_val**(n*n)

print(f"  Modular form values at q = 1/phi = {q_val:.10f}:")
print(f"    eta    = {eta:.10f}")
print(f"    theta2 = {theta2:.10f}")
print(f"    theta3 = {theta3:.10f}")
print(f"    theta4 = {theta4:.10f}")
print()

# Target: 3/16 = 0.1875
target_frac = 3.0/16.0
print(f"  Target fraction: 3/16 = {target_frac:.6f}")
print(f"  (This is f_Craddock / f_Rydberg = {f_target/f_R:.6f})")
print()

# Systematic search: ratios and products of modular forms
print(f"  {'Expression':>40} {'Value':>14} {'vs 3/16':>10} {'Error':>10}")
print(f"  {'-'*40} {'-'*14} {'-'*10} {'-'*10}")

combos = [
    ("eta", eta),
    ("theta4", theta4),
    ("eta * theta4", eta * theta4),
    ("eta^2", eta**2),
    ("eta / theta3", eta / theta3),
    ("eta / theta2", eta / theta2),
    ("theta4 / theta3", theta4 / theta3),
    ("theta4 / theta2", theta4 / theta2),
    ("theta4^2", theta4**2),
    ("eta * theta4 / 2", eta * theta4 / 2),
    ("3 * eta * theta4 / 2", 3 * eta * theta4 / 2),
    ("eta^2 / theta4", eta**2 / theta4),
    ("theta4 / phi", theta4 / phi),
    ("eta / phi", eta / phi),
    ("3 * theta4 / phi", 3 * theta4 / phi),
    ("eta * phi", eta * phi),
    ("3 * eta / (8 * phi)", 3 * eta / (8 * phi)),
    ("eta^3 / theta4", eta**3 / theta4),
    ("theta4 * phi^2", theta4 * phi**2),
    ("3 * theta4 * phi", 3 * theta4 * phi),
    ("eta / (phi * theta4)", eta / (phi * theta4)),
    ("sqrt(eta * theta4)", math.sqrt(eta * theta4)),
    ("eta^2 / (2 * theta3)", eta**2 / (2 * theta3)),  # = sin^2(theta_W) ~ 0.231
    ("3 * theta4 / (2 * eta)", 3 * theta4 / (2 * eta)),
    ("theta4 * sqrt(3)", theta4 * math.sqrt(3)),
    ("eta * theta4 * phi", eta * theta4 * phi),
    ("eta * theta4 * phi^2", eta * theta4 * phi**2),
    ("eta / (4 * phi)", eta / (4 * phi)),
    ("3 / (16)", 3/16),
    ("eta^2 + theta4", eta**2 + theta4),
    ("eta - theta4 / 2", eta - theta4 / 2),
    ("(theta4 / eta)^2 * 3/16", (theta4/eta)**2 * 3/16),
    ("phi * theta4 + eta^2/4", phi * theta4 + eta**2/4),
    ("eta * theta4 * 3", eta * theta4 * 3),
]

results = []
for name, val in combos:
    err = abs(val - target_frac) / target_frac * 100
    results.append((name, val, err))

results.sort(key=lambda x: x[2])
for name, val, err in results[:20]:
    marker = " ***" if err < 1.0 else ""
    print(f"  {name:>40} {val:>12.8f} {target_frac:>10.6f} {err:>8.3f}%{marker}")

print()

# ===========================================================================
# PART 7:  THE PHYSICAL MEANING OF 8 * f_R / sqrt(mu)
# ===========================================================================
print(SEP)
print("PART 7:  PHYSICAL MEANING -- WHAT IS 8 * f_R / sqrt(mu)?")
print(SEP)
print()

# Key rewriting using the core identity alpha^(3/2) * mu * phi^2 = 3
core_id = alpha**1.5 * mu * phi**2
print(f"  Core identity: alpha^(3/2) * mu * phi^2 = {core_id:.6f}  (target: 3)")
print()

# f_R = alpha^2 * m_e * c^2 / (2h)    (in SI)
# f_R = alpha^2 * f_electron / 2       where f_electron = m_e c^2 / h
f_electron = m_e * c**2 / h_pl  # Hz
print(f"  f_electron = m_e c^2 / h = {f_electron:.6e} Hz")
print(f"  f_R = alpha^2 * f_electron / 2 = {alpha**2 * f_electron / 2:.6e} Hz")
print(f"  Check: f_R = {f_R:.6e} Hz  -- match: {abs(1-alpha**2*f_electron/2/f_R)*100:.6f}%")
print()

# Now: 8 * f_R / sqrt(mu)
# = 8 * alpha^2 * f_electron / (2 * sqrt(mu))
# = 4 * alpha^2 * f_electron / sqrt(mu)
print(f"  8 * f_R / sqrt(mu)")
print(f"  = 4 * alpha^2 * f_electron / sqrt(mu)")
print(f"  = 4 * alpha^2 * (m_e c^2 / h) / sqrt(mu)")
print()

# Using the core identity: mu = 3 / (alpha^(3/2) * phi^2)
# sqrt(mu) = sqrt(3) / (alpha^(3/4) * phi)
print(f"  Substituting mu = 3 / (alpha^(3/2) * phi^2):")
print(f"    sqrt(mu) = sqrt(3) / (alpha^(3/4) * phi)")
print()
print(f"  8 * f_R / sqrt(mu)")
print(f"    = 4 * alpha^2 * f_el / [sqrt(3) / (alpha^(3/4) * phi)]")
print(f"    = 4 * alpha^2 * alpha^(3/4) * phi * f_el / sqrt(3)")
print(f"    = 4 * alpha^(11/4) * phi / sqrt(3) * f_el")
print()

# Evaluate
f_mol_formula = 4.0 * alpha**(11.0/4.0) * phi / math.sqrt(3) * f_electron
print(f"  f_mol = 4 * alpha^(11/4) * phi / sqrt(3) * f_electron")
print(f"        = {f_mol_formula/1e12:.4f} THz")
print(f"  Target  = 613 THz")
print(f"  Match   = {100*(1-abs(f_mol_formula/1e12 - 613)/613):.2f}%")
print()

# The exponent 11/4
print(f"  The golden ratio phi and the exponent 11/4 appear explicitly.")
print(f"  11/4 = (2 + 3/4) = 2 (from f_R = alpha^2...) + 3/4 (from 1/sqrt(mu))")
print(f"  The 3/4 comes from the core identity: mu ~ alpha^(-3/2) => sqrt(mu) ~ alpha^(-3/4)")
print()

# Framework significance of 11/4
print(f"  Framework significance of 11/4:")
print(f"    11 = L(5)  (5th Lucas number)")
print(f"    4  = L(3)  (3rd Lucas number)")
print(f"    11/4 = L(5) / L(3)")
print(f"    This is a ratio of Lucas numbers!")
print()

# ===========================================================================
# PART 8:  WHERE DOES THE "8" REALLY COME FROM?
# ===========================================================================
print(SEP)
print("PART 8:  DISSECTING THE FACTOR 8 = 4 * 2")
print(SEP)
print("""
  The formula  f_mol = 8 * f_R / sqrt(mu)  can be rewritten as:

    f_mol = 4 * (2 * f_R) / sqrt(mu)
          = 4 * E_R_hartree_freq / sqrt(mu)

  where 2*f_R = f_Rydberg * 2 = the Hartree frequency (= alpha^2 * f_electron).

  In atomic units, the Hartree energy E_h = 2 * E_R = 27.211 eV.

  So:  f_mol = 4 * f_Hartree / sqrt(mu)

  The factor 4:
    In the particle-on-a-ring model of benzene, the HOMO-LUMO gap energy
    involves quantum numbers n1=1, n2=2.  The energy difference scales as
    (n2^2 - n1^2) = 3.  But for a 6-carbon ring, with 3 filled orbitals,
    the gap energy E = (hbar^2/m_e*R^2) * (2*n_HOMO + 1).

    More directly: in the Huckel model, benzene's gap = 2*beta.
    And 2*beta ~ 0.36 * E_Hartree (using beta = 2.4 eV, E_H = 27.2 eV).
    0.36 ~ 3/8.  And 3/8 * 2 = 3/4.  Hmm.

    The factor 4 has a cleaner interpretation:
      4 = 2^2 = (n_upper of Balmer-beta)^0 * n_lower^2 ?  No.
      4 = n_upper in H-beta (n=4->2).
      4 = L(3), 3rd Lucas number.
      4 = 2 * n_PT  (2 times PT n=2 bound states).

    But the most physical interpretation is simpler:
      8 * f_R = 4 * f_Hartree
      f_Hartree is the natural atomic energy unit.
      4 is a small integer prefactor related to the ratio of molecular to
      atomic electronic energy scales.

  The chain:
    f_Hartree / sqrt(mu) = BO ELECTRONIC transition of a molecule
                         = scale at which molecular electronic gaps appear
                         ~ 154 THz (too low by factor ~4)
    4 * f_Hartree / sqrt(mu) = 614 THz
    The factor 4 accounts for the ~4x enhancement of electronic transition
    frequencies in ring-conjugated systems over the bare BO electronic scale.
""")

f_Hartree = 2 * f_R
print(f"  f_Hartree = 2 * f_R = {f_Hartree/1e12:.2f} THz")
print(f"  f_Hartree / sqrt(mu) = {f_Hartree/math.sqrt(mu)/1e12:.2f} THz")
print(f"  4 * f_Hartree / sqrt(mu) = {4*f_Hartree/math.sqrt(mu)/1e12:.2f} THz")
print()

# ===========================================================================
# PART 9:  THE BALMER-BETA / GFP CONNECTION
# ===========================================================================
print(SEP)
print("PART 9:  BALMER-BETA AND GFP -- IS THERE A DEEP CONNECTION?")
print(SEP)
print("""
  The hydrogen Balmer-beta line:  n=4 -> n=2
    wavelength = 486.1 nm = 616.8 THz

  GFP chromophore absorption (anionic form):
    wavelength = 489 nm = 613 THz

  Craddock aromatic collective mode:
    frequency = 613 +/- 8 THz

  ALL THREE are within 4 THz of each other.
""")

f_Hbeta_THz = f_Hbeta / 1e12
f_GFP_THz = c / (489e-9) / 1e12

print(f"  H-beta:     {f_Hbeta_THz:.2f} THz  ({c/f_Hbeta*1e9:.1f} nm)")
print(f"  GFP:        {f_GFP_THz:.2f} THz  (489 nm)")
print(f"  Craddock:   613.0 THz  (489 nm)")
print(f"  8*f_R/sqmu: {8*f_BO_val/1e12:.2f} THz")
print()

# Physical argument for WHY Balmer-beta is selected
print(f"  PHYSICAL ARGUMENT FOR BALMER-BETA SELECTION:")
print(f"  ---------------------------------------------")
print(f"  1. Aromatic pi-electrons occupy roughly n=2 orbital character")
print(f"     (6 electrons in 3 pairs, effectively filling up to n=2)")
print(f"  2. The HOMO-LUMO gap of a ring conjugated system corresponds to")
print(f"     exciting one electron from an 'n=2-like' to an 'n=4-like' state")
print(f"  3. This is EXACTLY the Balmer-beta transition: n=4 -> n=2")
print(f"  4. The molecule's effective Z (screened nuclear charge seen by")
print(f"     pi-electrons) is ~1, so hydrogen-like scaling applies")
print(f"  5. The molecular bond length (~140 pm for C-C) is close to")
print(f"     the hydrogen Bohr radius (a0 = 52.9 pm) times n^2 for n=2:")
print(f"     a0 * 4 = {52.9*4:.0f} pm  (vs C-C bond length 140 pm)")
print()

# n=2 orbital radius comparison
a0_pm = 52.9  # Bohr radius in pm
for n in range(1, 6):
    r_n = a0_pm * n**2
    print(f"    n={n}: r_n = a0*n^2 = {r_n:.0f} pm", end="")
    if abs(r_n - 140) < 80:
        print(f"  <-- near C-C bond length 140 pm", end="")
    if abs(r_n - 840/6) < 50:
        print(f"  <-- near benzene ring radius", end="")
    print()

print()

# ===========================================================================
# PART 10:  FRAMEWORK CONNECTIONS FOR 8
# ===========================================================================
print(SEP)
print("PART 10:  FRAMEWORK CONNECTIONS FOR THE NUMBER 8")
print(SEP)
print()

connections_8 = [
    ("rank(E8)", 8, "Dimension of E8 Cartan subalgebra"),
    ("dim(E8 root space)", 8, "E8 lives in 8 dimensions"),
    ("Z2 * S4 factor", 8, "Symmetry breaking: 62208/7776 = 8"),
    ("2^3", 8, "2 = PT bound states, cubed"),
    ("L(3) * 2", 8, "L(3)=4 times vacuum degeneracy 2"),
    ("24/3", 8, "24 = |roots(4A2)| / triality"),
    ("4 * 2", 8, "Hartree factor 2 * molecular enhancement 4"),
    ("n_upper * n_lower (Balmer-beta)", 8, "4 * 2 = product of quantum numbers"),
]

print(f"  {'Connection':>35} {'Value':>6} {'Explanation':>50}")
print(f"  {'-'*35} {'-'*6} {'-'*50}")
for name, val, expl in connections_8:
    print(f"  {name:>35} {val:>6} {expl:>50}")

print()
print(f"  The MOST natural framework interpretation of 8:")
print(f"    8 = 62208 / 7776 = |Normalizer(4A2)| / N")
print(f"      = 2 (Z2 vacuum selection) * 4 (S4->S3 breaking)")
print(f"      = the symmetry-breaking factor that derives N = 6^5")
print(f"")
print(f"  This is the SAME factor that appears in:")
print(f"    62208 / 8 = 7776 = 6^5 = N")
print(f"")
print(f"  So the formula becomes:")
print(f"    f_mol = (62208/N) * f_R / sqrt(mu)")
print(f"          = |Normalizer| / N * f_Rydberg / sqrt(mu)")
print()

# ===========================================================================
# PART 11:  FRAMEWORK CONNECTIONS FOR 3/16
# ===========================================================================
print(SEP)
print("PART 11:  FRAMEWORK CONNECTIONS FOR 3/16")
print(SEP)
print()

# 3/16 decomposition
print(f"  3/16 = {3/16}")
print(f"  16 = 2^4")
print(f"  3/16 = 3 / 2^4")
print(f"  In the framework: 3 = triality, 2^4 = 16")
print()

# Is 16 a Lucas number? No.
lucas_nums = []
a, b = 2, 1
for i in range(15):
    lucas_nums.append(a)
    a, b = a + b, a
print(f"  Lucas numbers: {lucas_nums}")
print(f"  16 is NOT a Lucas number.")
print()

# Can 3/16 be expressed using phi?
print(f"  Phi-based expressions:")
print(f"    3/(8*phi^2) = {3/(8*phi**2):.6f}  (vs 3/16 = {3/16:.6f}, error = {abs(3/(8*phi**2)-3/16)/(3/16)*100:.2f}%)")
print(f"    phi^(-7) = {phi**(-7):.6f}  (vs 3/16 = {3/16:.6f}, error = {abs(phi**(-7)-3/16)/(3/16)*100:.2f}%)")
print(f"    (phi-1)^3 = phibar^3 = {(1/phi)**3:.6f}")
print(f"    3*phibar^4 = {3/phi**4:.6f}")
print(f"    phibar^3/2 = {1/(2*phi**3):.6f}  = alpha_s prediction!")
print()

# Actually phi^(-7/2) is interesting for scaling
print(f"  f_R / phi^(7/2) = {f_R / phi**3.5 / 1e12:.2f} THz  (this was the 'golden ratio scaling' route)")
print(f"    Match to 613: {100*(1-abs(f_R/phi**3.5/1e12-613)/613):.2f}%")
print()

# The three routes to 613 THz compared
print(f"  THREE ROUTES TO 613 THz:")
print(f"  {'Route':>35} {'Value (THz)':>14} {'Error':>10}")
print(f"  {'-'*35} {'-'*14} {'-'*10}")

routes = [
    ("8 * f_R / sqrt(mu)", 8 * f_R / math.sqrt(mu) / 1e12),
    ("(3/16) * f_R", 3/16 * f_R / 1e12),
    ("f_R / phi^(7/2)", f_R / phi**3.5 / 1e12),
    ("4*alpha^(11/4)*phi/sqrt(3)*f_el", f_mol_formula / 1e12),
    ("mu/3 (THz units)", mu/3),
]

for name, val in routes:
    err = abs(val - 613) / 613 * 100
    print(f"  {name:>35} {val:>12.2f}   {err:>8.3f}%")

print()

# ===========================================================================
# PART 12:  THE CORE IDENTITY CHAIN -- ALL IN ONE
# ===========================================================================
print(SEP)
print("PART 12:  THE COMPLETE CHAIN")
print(SEP)
print("""
  Starting from E8 algebra, ending at 613 THz:

  STEP 1 (proven):  E8 contains Z[phi]^4
                     => phi is algebraically forced

  STEP 2 (proven):  V(Phi) = lambda * (Phi^2 - Phi - 1)^2
                     => two vacua, domain wall, PT n=2

  STEP 3 (proven):  5 arguments force q = 1/phi
                     => all modular forms determined

  STEP 4 (derived): alpha^(3/2) * mu * phi^2 = 3
                     => alpha and mu are related through phi

  STEP 5 (physics): f_Rydberg = alpha^2 * m_e c^2 / (2h)
                     => atomic energy scale from alpha

  STEP 6 (BO theory): f_mol ~ f_Rydberg / sqrt(mu)
                       => molecular scale from mu

  STEP 7 (??):      f_mol = 8 * f_Rydberg / sqrt(mu)
                     The factor 8 has MULTIPLE interpretations:

     (a) HYDROGEN:  8 = 16 * (3/16) / (Balmer coeff)
         -- selects the n=4->2 transition, but WHY this transition?

     (b) ATOMIC UNITS:  8 = 4 * 2
         -- 2 converts Rydberg to Hartree
         -- 4 is the molecular enhancement over bare BO electronic scale
         -- But WHY 4 specifically?

     (c) E8 FRAMEWORK:  8 = 62208 / 7776 = |Norm(4A2)| / N
         -- the symmetry-breaking factor
         -- this gives f_mol = |Norm| / N * f_R / sqrt(mu)

     (d) LUCAS:  8 = 2 * L(3)
         -- L(3) = 4, times the vacuum degeneracy Z2

  STEP 8 (substitution): Using alpha^(3/2)*mu*phi^2 = 3:
     f_mol = 4 * alpha^(11/4) * phi / sqrt(3) * f_electron

     Golden ratio phi appears EXPLICITLY.
     Exponent 11/4 = L(5)/L(3).
""")

# Final verdict
print(SEP)
print("PART 13:  VERDICT -- STATUS OF THE FACTOR 8")
print(SEP)
print(f"""
  WHAT IS ESTABLISHED:
  - 8 * f_R / sqrt(mu) = {8*f_R/math.sqrt(mu)/1e12:.2f} THz matches 613+/-8 THz (99.8%)
  - 8 = rank(E8) = dim(E8 Cartan) = |Norm(4A2)|/N
  - After core identity substitution, phi appears explicitly
  - The exponent 11/4 = L(5)/L(3) is a Lucas ratio
  - The formula is dimensionally correct and unit-independent

  WHAT IS NOT ESTABLISHED:
  - No first-principles derivation of WHY 8 (not 7 or 9)
  - The Balmer-beta selection argument is heuristic, not derived
  - The particle-on-a-ring model gives ~194 nm, not 486 nm
  - The factor 4 in f_mol = 4*f_Hartree/sqrt(mu) is empirical
  - Interpretation (c) (E8 symmetry breaking) is suggestive but
    no calculation shows the kink produces the factor |Norm|/N

  BEST CANDIDATE EXPLANATION:
  The most promising path is (c): 8 = |Normalizer(W(4A2))| / N.
  This is the SAME factor that produces N = 7776 = 6^5 from the
  E8 Weyl group.  If the domain wall's coupling to molecular
  electrons involves the full normalizer structure, the factor 8
  would be derived from E8 representation theory.

  This would give:
    f_mol = |Norm_W(4A2)| / N * f_Rydberg / sqrt(mu)
          = (Z2 * S4->S3) * (alpha^2 / 2) * f_electron / sqrt(mu)
          = (vacuum * breaking) * (Rydberg / sqrt(mu))

  The factor 8 = 2*4 then means:
    - Factor 2 (Z2): both vacua contribute to molecular electron dynamics
    - Factor 4 (S4/S3): the breaking pattern that selects 3 generations
      also sets the molecular energy scale

  STATUS: SUGGESTIVE but UNPROVEN.  The derivation requires showing that
  the E8 normalizer structure enters the molecular Hamiltonian, which has
  not been done.
""")

print(SEP)
print("END OF FACTOR-8 ANALYSIS")
print(SEP)
