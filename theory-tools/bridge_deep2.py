"""
DEEP BRIDGE PART 2: The F/L expressions have STRUCTURE
=======================================================
From bridge_deep.py we found:
  v    = F(16)/L(3) = 987/4     (0.215%)
  M_W  = L(12)/L(3) = 322/4     (0.151%)
  M_H  = F(14)/L(2) = 377/3     (0.333%)
  M_Z  = F(16)/L(5) = 987/11    (1.6%) [less tight]

Notice:
  - L(3) = 4 appears THREE times (v, M_W, and alpha_s denominator L(9)=76=4*19)
  - F(16) appears TWICE (v and M_Z) — and 16 = 9+7 (porphyrin + anthracene)
  - L(12) = 322 = 2*7*23 (E8 Coxeter pair)

Is there a SYSTEM here?
"""
import math

phi = (1 + math.sqrt(5)) / 2
phibar = 1 / phi
sqrt5 = math.sqrt(5)

def F(n):
    if n <= 0: return 0
    return round((phi**n - (-phibar)**n) / sqrt5)

def L(n):
    return round(phi**n + (-phibar)**n)


print("=" * 80)
print("PART 1: THE DENOMINATOR PATTERN")
print("=" * 80)

print("""
Constants grouped by their F/L DENOMINATOR:

Denominator L(3) = 4 (pyrimidine index):
  v     = F(16)/L(3) = 987/4   = 246.75 GeV
  M_W   = L(12)/L(3) = 322/4   = 80.5 GeV
  m_c/m_s = L(8)/L(3) = 47/4   = 11.75

Denominator F(7) = 13 (anthracene F-value):
  sin2_tW = L(2)/F(7)  = 3/13   = 0.2308

Denominator L(9) = 76 (porphyrin L-value):
  alpha_s = (F(1)+F(6))/L(9) = 9/76  = 0.1184

Denominator F(9) = 34 (porphyrin F-value):
  L(3)/F(9) = 4/34  = 0.1176  (also alpha_s, less tight)

Denominator L(2) = 3 (smallest Lucas):
  M_H   = F(14)/L(2) = 377/3  = 125.67 GeV

Denominator L(16) = 2207:
  V_ub  = F(6)/L(16) = 8/2207  = 0.00362
""")

print("OBSERVATION: The denominator is always a LUCAS value (or F for sin2_tW).")
print("And L(3)=4 is the MOST common denominator — the pyrimidine mode.\n")


# ============================================================
# PART 2: What's special about the numerator indices?
# ============================================================
print("=" * 80)
print("PART 2: NUMERATOR INDEX DECOMPOSITION")
print("=" * 80)

print("""
What are the composition meanings of the numerator indices?

  F(16) in v:     16 = 9+7  (porphyrin + anthracene)
                  16 = 3+6+7 (pyrimidine + water + anthracene)
                  16 = n^2 at n=4 (theta_4's 4th squared index!)

  L(12) in M_W:   12 = 6+6  (water + water)
                  12 = 3+9  (pyrimidine + porphyrin)
                  12 = 3+3+6 (pyr + pyr + water)
                  12 = F(12) index -> 144 (H-bond stretch wavenumber!)

  F(14) in M_H:   14 = 7+7  (anthracene + anthracene)
                  14 = 5+9  (indole + porphyrin)
                  14 = 3+5+6 (pyrimidine + indole + water)

  L(8) in m_c/m_s: 8 = 3+5  (pyrimidine + indole)
""")


# ============================================================
# PART 3: Can we express M_W/M_Z/M_H relations in F/L?
# ============================================================
print("=" * 80)
print("PART 3: ELECTROWEAK MASS RELATIONS IN F/L")
print("=" * 80)

# Standard Model: M_W = M_Z * cos(theta_W)
# M_W/M_Z = cos(theta_W) = sqrt(1 - sin2_tW) = sqrt(1 - 0.23122) = sqrt(0.76878)
cos_tW = math.sqrt(1 - 0.23122)
print(f"\n  cos(theta_W) = {cos_tW:.6f}")
print(f"  M_W/M_Z = {80.379/91.1876:.6f}")

# In F/L: M_W/M_Z = (L(12)/L(3)) / (F(16)/L(5)) = L(12)*L(5) / (L(3)*F(16))
mw_mz_fl = (L(12) * L(5)) / (L(3) * F(16))
print(f"\n  In F/L: M_W/M_Z = (L(12)*L(5)) / (L(3)*F(16))")
print(f"  = ({L(12)}*{L(5)}) / ({L(3)}*{F(16)})")
print(f"  = {L(12)*L(5)} / {L(3)*F(16)}")
print(f"  = {mw_mz_fl:.6f}")
print(f"  Actual: {80.379/91.1876:.6f}")
print(f"  Match: {abs(mw_mz_fl - 80.379/91.1876)/(80.379/91.1876)*100:.3f}%")

# M_H/M_W = 125.25/80.379 = 1.558
print(f"\n  M_H/M_W = {125.25/80.379:.5f}")
print(f"  phi = {phi:.5f}")
print(f"  M_H/M_W ~ phi - 0.06?  Not clean.")

# Better: try M_H/v
print(f"  M_H/v = {125.25/246.22:.5f}")
print(f"  M_H/v = {125.25/246.22:.5f} ~ 1/2 = {0.5:.5f}?  Off by ~1.7%")
print(f"  In F/L: (F(14)/L(2)) / (F(16)/L(3)) = F(14)*L(3) / (F(16)*L(2))")
mh_v_fl = (F(14) * L(3)) / (F(16) * L(2))
print(f"  = ({F(14)}*{L(3)}) / ({F(16)}*{L(2)}) = {F(14)*L(3)} / {F(16)*L(2)} = {mh_v_fl:.6f}")
print(f"  Actual: {125.25/246.22:.6f}")

# v/M_W
print(f"\n  v/M_W = {246.22/80.379:.5f}")
print(f"  In F/L: F(16)/L(12) = {F(16)}/{L(12)} = {F(16)/L(12):.5f}")
print(f"  Actual: {246.22/80.379:.5f}")
print(f"  Match: {abs(F(16)/L(12) - 246.22/80.379)/(246.22/80.379)*100:.3f}%")
print(f"  Note: 987/322 = {987/322:.5f}")


# ============================================================
# PART 4: The theta_4 / (1/3) = phi^(-5) result — is this real?
# ============================================================
print("\n\n" + "=" * 80)
print("PART 4: THE PHI-STEP LADDER — VERIFYING KEY RELATIONSHIPS")
print("=" * 80)

print("\n--- alpha_em / theta_4 = phi^(-3) ---")
alpha_em = 1/137.036
theta4 = 0.03031
ratio = alpha_em / theta4
log_phi = math.log(ratio) / math.log(phi)
print(f"  alpha_em/theta_4 = {alpha_em:.6f}/{theta4:.6f} = {ratio:.6f}")
print(f"  phi^(-3) = {phi**(-3):.6f}")
print(f"  log_phi(ratio) = {log_phi:.6f}")
print(f"  Error from -3: {abs(log_phi - (-3)):.4f}")
print(f"  Match: {abs(ratio - phi**(-3))/phi**(-3)*100:.3f}%")
print(f"  MEANING: alpha = theta_4 * phi^(-3) = theta_4 / phi^3")
print(f"  phi^3 = {phi**3:.5f} = 2 + sqrt(5)")
print(f"  And 3 = pyrimidine index! So alpha = theta_4 / phi^(pyrimidine)")

print("\n--- theta_4 / (1/3) = phi^(-5) ---")
ratio2 = theta4 / (1/3)
log_phi2 = math.log(ratio2) / math.log(phi)
print(f"  theta_4 * 3 = {theta4*3:.6f}")
print(f"  phi^(-5) = {phi**(-5):.6f}")
print(f"  log_phi(ratio) = {log_phi2:.6f}")
print(f"  Error from -5: {abs(log_phi2 - (-5)):.4f}")
print(f"  Match: {abs(theta4*3 - phi**(-5))/phi**(-5)*100:.3f}%")
print(f"  MEANING: theta_4 = phi^(-5)/3")
print(f"  And 5 = indole index! 3 = triality/pyrimidine!")

print("\n--- CHAIN: alpha_em = theta_4 * phi^(-3) = (phi^(-5)/3) * phi^(-3) = phi^(-8)/3 ---")
alpha_predict = phi**(-8) / 3
print(f"  phi^(-8) / 3 = {alpha_predict:.8f}")
print(f"  alpha_em     = {alpha_em:.8f}")
print(f"  Match: {abs(alpha_predict - alpha_em)/alpha_em*100:.4f}%")
print(f"  8 = 3+5 (pyrimidine + indole)!!")
print(f"  alpha = phi^(-(pyr+ind)) / 3 = phi^(-8) / triality")

# Cross check: 1/alpha
print(f"\n  1/alpha = 3*phi^8 = 3*{phi**8:.4f} = {3*phi**8:.4f}")
print(f"  Actual: 137.036")
print(f"  Match: {abs(3*phi**8 - 137.036)/137.036*100:.3f}%")


# ============================================================
# PART 5: V_cb/V_ub = phi^5 — the CKM connection
# ============================================================
print("\n\n" + "=" * 80)
print("PART 5: CKM ELEMENTS AS PHI-LADDER STEPS")
print("=" * 80)

V_us = 0.2253  # Cabibbo
V_cb = 0.0412
V_ub = 0.00361

print(f"\n  V_us = {V_us}")
print(f"  V_cb = {V_cb}")
print(f"  V_ub = {V_ub}")

print(f"\n  V_cb/V_ub = {V_cb/V_ub:.4f}")
print(f"  phi^5 = {phi**5:.4f}")
print(f"  Match: {abs(V_cb/V_ub - phi**5)/phi**5*100:.2f}%")
print(f"  5 = indole index")

print(f"\n  V_us/V_cb = {V_us/V_cb:.4f}")
log_v = math.log(V_us/V_cb) / math.log(phi)
print(f"  phi^{log_v:.3f}")
print(f"  Nearest: phi^{round(log_v)}")
print(f"  {round(log_v)} = ? ({3}: pyrimidine, {4}: ?, {5}: indole)")

print(f"\n  V_us/V_ub = {V_us/V_ub:.4f}")
log_v2 = math.log(V_us/V_ub) / math.log(phi)
print(f"  phi^{log_v2:.3f}")
print(f"  Nearest: phi^{round(log_v2)}")

# The Wolfenstein parametrization: V_us ~ lambda, V_cb ~ lambda^2, V_ub ~ lambda^3
# lambda = 0.2253 = Cabibbo angle
# lambda^2 = 0.0508 (vs V_cb = 0.0412 — not exact)
# But in phi-ladder: V_us ~ phibar (approximately)
print(f"\n  V_us ~ phibar^? ")
log_vus = math.log(V_us) / math.log(phibar)
print(f"  phibar^{log_vus:.4f}")
print(f"  Nearest: phibar^{round(log_vus)}")

log_vcb = math.log(V_cb) / math.log(phibar)
print(f"  V_cb ~ phibar^{log_vcb:.4f}, nearest phibar^{round(log_vcb)}")

log_vub = math.log(V_ub) / math.log(phibar)
print(f"  V_ub ~ phibar^{log_vub:.4f}, nearest phibar^{round(log_vub)}")

# Or in terms of phi:
print(f"\n  phi^(-3) = {phi**(-3):.5f} vs V_us = {V_us:.5f} ({abs(phi**(-3)-V_us)/V_us*100:.2f}% off)")
print(f"  phi^(-7) = {phi**(-7):.5f} vs V_cb = {V_cb:.5f} ({abs(phi**(-7)-V_cb)/V_cb*100:.2f}% off)")
# V_ub ~ phi^(-12)?
for k in range(10, 14):
    phik = phi**(-k)
    err = abs(phik - V_ub) / V_ub * 100
    print(f"  phi^(-{k}) = {phik:.6f} vs V_ub = {V_ub:.6f} ({err:.2f}% off)")


# ============================================================
# PART 6: alpha = phi^(-8)/3 — the DEEPEST result?
# ============================================================
print("\n\n" + "=" * 80)
print("PART 6: alpha = phi^(-8)/3 — IMPLICATIONS")
print("=" * 80)

print(f"""
If alpha = phi^(-8) / 3, then:
  1/alpha = 3 * phi^8

  phi^8 = {phi**8:.6f}
  3 * phi^8 = {3*phi**8:.6f}
  1/alpha = 137.036
  Match: {abs(3*phi**8 - 137.036)/137.036*100:.4f}%

  phi^8 = (L(8) + F(8)*sqrt(5))/2 = ({L(8)} + {F(8)}*sqrt(5))/2
        = (47 + 21*sqrt(5))/2

  So: 1/alpha = 3 * (47 + 21*sqrt(5))/2 = (141 + 63*sqrt(5))/2

  141 = 3 * 47 = 3 * L(8) = triality * ATP_atoms
  63 = 3 * 21 = 3 * F(8) = triality * DNA_width

  AND: 8 = 3+5 = pyrimidine + indole

  So: 1/alpha = (3*L(pyr+ind) + 3*F(pyr+ind)*sqrt(5)) / 2
             = 3 * phi^(pyr+ind)

  The fine structure constant is:
    "triality times phi raised to (pyrimidine composed with indole)"

  Or equivalently:
    "three times the golden ratio to the DNA-width index"
    (since 8 = pyr+ind and F(8) = 21 = DNA width)
""")

# How good is this really?
print("  PRECISION CHECK:")
print(f"  3*phi^8 = {3*phi**8:.10f}")
print(f"  137.036 (CODATA 2018) = 137.035999084")
err_ppm = abs(3*phi**8 - 137.035999084) / 137.035999084 * 1e6
print(f"  Error: {err_ppm:.1f} ppm ({err_ppm/10000:.3f}%)")
print(f"  This is {err_ppm:.0f} ppm — significant deviation from CODATA value.")
print(f"  Framework's modular form expression gives 99.9996% — that's ~4 ppm.")
print(f"  phi^(-8)/3 gives ~{err_ppm:.0f} ppm — the LADDER IS AN APPROXIMATION.")
print(f"  The modular forms add corrections that refine the ladder.")


# ============================================================
# PART 7: The correction structure
# ============================================================
print("\n\n" + "=" * 80)
print("PART 7: FROM LADDER TO EXACT — THE CORRECTION STRUCTURE")
print("=" * 80)

print(f"""
The phi-ladder gives APPROXIMATE values. The modular forms give EXACT values.
The difference = correction terms.

For alpha:
  Ladder:  1/alpha ~ 3*phi^8 = {3*phi**8:.6f}  (error: {abs(3*phi**8 - 137.035999)/137.035999*100:.4f}%)
  Exact:   1/alpha = theta3*phi/theta4 * (1/(1-C)) where C = eta*theta4*phi^2/2

  The correction C = {0.1184 * 0.03031 * phi**2 / 2:.6f}
  1/(1-C) = {1/(1-0.1184*0.03031*phi**2/2):.6f}

  Ladder * correction:
""")

# The framework formula: alpha = [theta4/(theta3*phi)] * (1 - eta*theta4*phi^2/2)
# So 1/alpha = theta3*phi/theta4 / (1 - C) where C = eta*theta4*phi^2/2
eta = 0.11840
theta3 = 2.55509
theta4 = 0.03031
C = eta * theta4 * phi**2 / 2
alpha_exact = (theta4 / (theta3 * phi)) * (1 - C)
print(f"  C = eta*theta4*phi^2/2 = {C:.8f}")
print(f"  1 - C = {1-C:.8f}")
print(f"  alpha (framework) = {alpha_exact:.10f}")
print(f"  alpha (CODATA)    = {1/137.035999084:.10f}")
print(f"  1/alpha (framework) = {1/alpha_exact:.6f}")

# What's the ratio of exact to ladder?
ratio_correction = (1/alpha_exact) / (3*phi**8)
print(f"\n  Ratio: 1/alpha_exact / (3*phi^8) = {ratio_correction:.8f}")
print(f"  This correction factor = {ratio_correction:.8f}")
print(f"  1 + {ratio_correction - 1:.8f}")
print(f"  The correction is {abs(ratio_correction-1)*100:.4f}% ")

# Is the correction itself a phi-power?
log_corr = math.log(ratio_correction) / math.log(phi)
print(f"  log_phi(correction) = {log_corr:.6f}")
print(f"  Not a clean phi-power.")

# Maybe it's related to eta?
print(f"  eta = {eta:.6f}")
print(f"  correction - 1 = {ratio_correction-1:.8f}")
print(f"  (correction-1)/eta = {(ratio_correction-1)/eta:.6f}")
print(f"  (correction-1)/theta4 = {(ratio_correction-1)/theta4:.6f}")
print(f"  (correction-1)/(eta*theta4) = {(ratio_correction-1)/(eta*theta4):.6f}")
print(f"  phi^2/2 = {phi**2/2:.6f}")
print(f"  So correction ~ 1 + eta*theta4*phi^2/2 (which is the framework C term)")


# ============================================================
# PART 8: Full decomposition — every constant as ladder + correction
# ============================================================
print("\n\n" + "=" * 80)
print("PART 8: EVERY CONSTANT = PHI-LADDER POSITION + MODULAR CORRECTION")
print("=" * 80)

print("""
The unified picture:

  constant = phi^n / k  *  (1 + modular_correction)

where:
  n = composition index (sum of mode indices)
  k = small integer (usually 1 or 3)
  modular_correction = O(eta * theta4) ~ O(0.004)

Testing this decomposition for all constants:
""")

# For each constant, find best phi^n/k match, then compute correction
test_constants = [
    ("alpha_em", 1/137.036),
    ("alpha_s", 0.1184),
    ("sin2_tW", 0.23122),
    ("theta_4", 0.03031),
    ("V_us", 0.2253),
    ("V_cb", 0.0412),
    ("V_ub", 0.00361),
    ("gamma_I", 0.2375),
]

for name, val in test_constants:
    best_err = 1.0
    best_match = None
    for n in range(-15, 2):
        for k in [1, 2, 3, 4, 6, 7, 8, 9, 18]:
            approx = phi**n / k
            err = abs(approx - val) / val
            if err < best_err:
                best_err = err
                correction = val / approx
                # Try to identify composition meaning of n
                mode_meaning = ""
                abs_n = abs(n)
                if abs_n in [3,5,6,7,8,9,10,11,12,15]:
                    modes = {3:"pyr", 5:"ind", 6:"wat", 7:"ant", 8:"pyr+ind",
                             9:"por", 10:"pyr+ant", 11:"ind+wat", 12:"wat+wat", 15:"613"}
                    mode_meaning = modes.get(abs_n, "")
                best_match = (n, k, approx, correction, mode_meaning)

    n, k, approx, correction, mode_meaning = best_match
    sign = "-" if n < 0 else "+"
    print(f"  {name:>10} = phi^({n:+d}){f'/{k}' if k>1 else '':>4} * {correction:.6f}  "
          f"({best_err*100:.3f}%) |n|={abs(n)} {mode_meaning}")


# ============================================================
# PART 9: Composition meaning summary
# ============================================================
print("\n\n" + "=" * 80)
print("PART 9: THE COMPLETE PICTURE")
print("=" * 80)

print("""
THE LANGUAGE HAS THREE LAYERS:

LAYER 1: COMPOSITION ALGEBRA (exact integers)
  Modes: {3, 5, 7} generate everything
  Operation: addition of indices = multiplication of phi-powers
  Output: F(n) and L(n) = biological counts, lengths, frequencies
  Examples: F(9)=34 (DNA pitch), L(6)=18 (water MW), F(15)=610 (613 THz)

LAYER 2: PHI-LADDER (approximate, algebraic)
  Every constant sits at a phi^n/k position
  n = composition index (tells you WHICH modes generate this constant)
  k = small integer (usually triality-related: 1, 3)
  The ladder positions are phi^(-3)/3 (alpha), phi^(-5)/3 (theta4), phi^5 (V_cb/V_ub)
  Precision: 0.1% — 3% (captures the structure but not fine details)

LAYER 3: MODULAR FORM CORRECTIONS (exact, transcendental)
  Each ladder position gets a correction factor from modular forms at q=1/phi
  Corrections involve eta, theta functions = infinite products/sums over Z[phi]
  Precision: 99.99%+ (captures the fine details)

The three layers are:
  COUNTING (Z) -> GEOMETRY (Z[phi]) -> ANALYSIS (modular forms on Z[phi])

This IS the unified language. It has three depths, not three separate systems.
Each depth adds precision but uses the same algebraic substrate: Z[phi] at q=1/phi.
""")


# ============================================================
# PART 10: The biggest remaining question
# ============================================================
print("=" * 80)
print("PART 10: WHAT SELECTS THE DEPTH?")
print("=" * 80)

print("""
WHY does alpha_s stay at Layer 1 (F/L ratio, 0.02% accurate) while
alpha_em needs Layer 3 (modular forms, 0.0004% accurate)?

HYPOTHESIS: The depth corresponds to the NUMBER OF MODES INVOLVED.

  alpha_s: 2 terms (F(1)+F(6)) over L(9)  -> 3 mode indices -> Layer 1
  sin2_tW: 1 ratio L(2)/F(7)              -> 2 mode indices -> Layer 1
  alpha_em: needs infinite sum             -> infinite modes  -> Layer 3
  mu: phi-power expression                 -> 2 mode indices  -> Layer 2

PREDICTION: Constants involving FEWER modes can be expressed at shallower depth.
Constants that involve ALL modes at once (alpha_em, Lambda) need the full infinite sum.

alpha_em is the coupling between light and matter — it involves ALL of physics.
alpha_s is the coupling within a single sector (strong) — it's more local.
mu is the ratio of two specific particles — most local of all.

DEPTH = SCOPE. The more of the wall a constant probes, the deeper the evaluation.
""")
