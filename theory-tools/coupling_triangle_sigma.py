"""
coupling_triangle_sigma.py

Non-tautological test of the framework's three core coupling formulas:
  alpha_s^2 / (sin^2theta_W * alpha_em) = 2*theta3(1/phi)*phi

Uses MEASURED experimental values (PDG 2024 / CODATA) for LHS.
Uses framework modular form prediction for RHS.

Scale discussion:
  - alpha_s(M_Z) and sin^2theta_W(M_Z) are clearly at M_Z scale
  - Framework gives 1/alpha = theta3*phi/theta4 ~ 136.39, closest to alpha(q=0)=1/137.036
    NOT to alpha(M_Z)=1/127.951
  => Option A: all at M_Z
  => Option B: alpha_s, sin^2theta_W at M_Z; alpha_em at q=0 (what framework formulas actually give)
"""

from mpmath import mp, mpf, sqrt, jtheta, log, pi, nstr

mp.dps = 50  # 50 decimal places

# ---------------------------------------------
# Constants
# ---------------------------------------------
phi = (1 + sqrt(5)) / 2
q   = 1 / phi        # Golden nome

# ---------------------------------------------
# Modular forms at q = 1/phi
# mpmath.jtheta(n, z, q): Jacobi theta function theta_n(z|q)
# For z=0: theta2(0,q), theta3(0,q), theta4(0,q)
# eta(q) = q^(1/24) * prod_{n=1}^inf (1-q^n)
# mpmath.eta(tau) where q = exp(2pii*tau) => tau = ln(q)/(2pii)
# For real q=1/phi: tau = ln(1/phi)/(2pii) = -ln(phi)/(2pii) = i*ln(phi)/(2pi)
# ---------------------------------------------
from mpmath import im, re, log as mplog, mpc, exp

tau = mpc(0, mplog(phi) / (2 * pi))   # purely imaginary: i*ln(phi)/(2pi)

# Theta functions (z=0 arg for Jacobi theta)
th2 = jtheta(2, 0, q)
th3 = jtheta(3, 0, q)
th4 = jtheta(4, 0, q)

# Dedekind eta via product definition (more direct)
# eta(q) = q^(1/24) * Pi_{n>=1}(1-q^n)
from mpmath import qp  # q-Pochhammer symbol
eta_val = q**(mpf(1)/24) * qp(q, q)   # qp(a,q) = (a;q)_inf, so qp(q,q) = (q;q)_inf

# Verify: eta_val should ~ 0.11840 for this framework
# Framework: alpha_s = eta(1/phi) ~ 0.11840

# Framework RHS
RHS = 2 * th3 * phi

print("=" * 65)
print("COUPLING TRIANGLE NON-TAUTOLOGICAL TEST")
print("alpha_s^2 / (sin^2theta_W * alpha_em) = 2*theta3(1/phi)*phi")
print("=" * 65)
print()
print("-- Modular form values at q = 1/phi --------------------------")
print(f"  phi          = {nstr(phi, 12)}")
print(f"  q = 1/phi    = {nstr(q,   12)}")
print(f"  theta2(1/phi)    = {nstr(th2, 12)}")
print(f"  theta3(1/phi)    = {nstr(th3, 12)}")
print(f"  theta4(1/phi)    = {nstr(th4, 12)}")
print(f"  eta(1/phi)     = {nstr(eta_val, 12)}")
print()
print(f"  RHS = 2*theta3*phi = {nstr(RHS, 12)}")
print(f"  sqrtRHS        = {nstr(sqrt(RHS), 12)}")
print()

# ---------------------------------------------
# Framework-predicted coupling values
# ---------------------------------------------
alpha_s_fw    = eta_val                    # eta(1/phi)
sin2W_fw      = eta_val**2 / (2 * th4)    # eta^2/(2theta4)
inv_alpha_fw  = th3 * phi / th4           # theta3*phi/theta4  (tree, ~136.39)
alpha_em_fw   = 1 / inv_alpha_fw

print("-- Framework-predicted coupling values ---------------------")
print(f"  alpha_s (framework)       = eta(1/phi)       = {nstr(alpha_s_fw, 8)}")
print(f"  sin^2theta_W (framework)   = eta^2/(2theta4)     = {nstr(sin2W_fw,  8)}")
print(f"  1/alpha_em (framework)    = theta3*phi/theta4      = {nstr(inv_alpha_fw, 8)}")
print(f"  alpha_em (framework)      =               = {nstr(alpha_em_fw, 8)}")
print()

# ---------------------------------------------
# MEASURED values (PDG 2024 / CODATA 2018)
# ---------------------------------------------
# alpha_s(M_Z), MS-bar
as_meas   = mpf("0.1180")
as_err    = mpf("0.0009")

# sin^2theta_W(MS-bar, M_Z)
sW_meas   = mpf("0.23122")
sW_err    = mpf("0.00004")

# alpha_em at M_Z (running)
inv_a_MZ  = mpf("127.951")
inv_a_MZ_err = mpf("0.009")
a_MZ      = 1 / inv_a_MZ
a_MZ_err  = a_MZ**2 * inv_a_MZ_err   # sigma(alpha) = alpha^2*sigma(1/alpha)

# alpha_em at q=0 (Thomson limit / CODATA)
inv_a_0   = mpf("137.035999084")
inv_a_0_err = mpf("0.000000021")
a_0       = 1 / inv_a_0
a_0_err   = a_0**2 * inv_a_0_err

print("-- Measured values (PDG 2024 / CODATA) ---------------------")
print(f"  alpha_s(M_Z)       = {as_meas} +- {as_err}")
print(f"  sin^2theta_W(M_Z)   = {sW_meas} +- {sW_err}")
print(f"  1/alpha_em(M_Z)    = {inv_a_MZ} +- {inv_a_MZ_err}")
print(f"  1/alpha_em(q=0)    = {inv_a_0} +- {inv_a_0_err}")
print()

# ---------------------------------------------
# OPTION A: all at M_Z
# LHS_A = alpha_s^2 / (sin^2theta_W * alpha_em(M_Z))
# ---------------------------------------------
LHS_A = as_meas**2 / (sW_meas * a_MZ)

# Error propagation:  LHS = f(alphas, sW, alpha)
# d(ln LHS)/d(alphas)  = 2/alphas
# d(ln LHS)/d(sW)  = -1/sW
# d(ln LHS)/d(alpha)   = -1/alpha  (but sigma_alpha small; use sigma_{1/alpha} -> sigma_alpha = alpha^2*sigma_{1/alpha})
rel_err_A = sqrt(
    (2 * as_err / as_meas)**2 +
    (sW_err / sW_meas)**2 +
    (a_MZ_err / a_MZ)**2
)
sigma_LHS_A = LHS_A * rel_err_A

dev_A       = LHS_A - RHS
sigma_A     = float(dev_A / sigma_LHS_A)
match_A     = float(100 * (1 - abs(dev_A) / RHS))

print("=" * 65)
print("OPTION A: all couplings at M_Z scale")
print("=" * 65)
print(f"  LHS_A = alpha_s(MZ)^2 / [sin^2theta_W(MZ)*alpha_em(MZ)]")
print(f"        = {nstr(as_meas,4)}^2 / ({nstr(sW_meas,6)} x {nstr(a_MZ,6)})")
print(f"        = {nstr(LHS_A, 8)}")
print(f"  RHS   = 2*theta3*phi = {nstr(RHS, 8)}")
print(f"  Match         = {match_A:.2f}%")
print(f"  Deviation     = {nstr(dev_A, 4)} ({100*float(dev_A/RHS):.2f}%)")
print(f"  sigma(LHS_A)      = {nstr(sigma_LHS_A, 4)} (rel {float(rel_err_A)*100:.2f}%)")
print(f"  Significance  = {sigma_A:.2f} sigma")
if abs(sigma_A) < 2:
    print(f"  STATUS: CONSISTENT (<2sigma)")
elif abs(sigma_A) < 3:
    print(f"  STATUS: MILD TENSION (2-3sigma)")
else:
    print(f"  STATUS: TENSION (>{abs(sigma_A):.1f}sigma) -- scale mixing matters!")
print()

# ---------------------------------------------
# OPTION B: alpha_s, sin^2theta_W at M_Z; alpha_em at q=0
# (matches what framework formulas actually give)
# ---------------------------------------------
LHS_B = as_meas**2 / (sW_meas * a_0)

rel_err_B = sqrt(
    (2 * as_err / as_meas)**2 +
    (sW_err / sW_meas)**2 +
    (a_0_err / a_0)**2
)
sigma_LHS_B = LHS_B * rel_err_B

dev_B       = LHS_B - RHS
sigma_B     = float(dev_B / sigma_LHS_B)
match_B     = float(100 * (1 - abs(dev_B) / RHS))

print("=" * 65)
print("OPTION B: alpha_s, sin^2theta_W at M_Z; alpha_em at q=0 (Thomson limit)")
print("  (This is what framework formulas actually predict,")
print("   since theta3*phi/theta4 ~ 136.39, close to 137.04 not 127.95)")
print("=" * 65)
print(f"  LHS_B = alpha_s(MZ)^2 / [sin^2theta_W(MZ)*alpha_em(0)]")
print(f"        = {nstr(as_meas,4)}^2 / ({nstr(sW_meas,6)} x {nstr(a_0,8)})")
print(f"        = {nstr(LHS_B, 8)}")
print(f"  RHS   = 2*theta3*phi = {nstr(RHS, 8)}")
print(f"  Match         = {match_B:.2f}%")
print(f"  Deviation     = {nstr(dev_B, 4)} ({100*float(dev_B/RHS):.2f}%)")
print(f"  sigma(LHS_B)      = {nstr(sigma_LHS_B, 4)} (rel {float(rel_err_B)*100:.2f}%)")
print(f"  Significance  = {sigma_B:.2f} sigma")
if abs(sigma_B) < 2:
    print(f"  STATUS: CONSISTENT (<2sigma)")
elif abs(sigma_B) < 3:
    print(f"  STATUS: MILD TENSION (2-3sigma)")
else:
    print(f"  STATUS: TENSION (>{abs(sigma_B):.1f}sigma)")
print()

# ---------------------------------------------
# TAUTOLOGICAL (framework-internal) version
# ---------------------------------------------
LHS_fw = alpha_s_fw**2 / (sin2W_fw * alpha_em_fw)
dev_fw = float((LHS_fw - RHS) / RHS)

print("=" * 65)
print("FRAMEWORK-INTERNAL (tautological) version")
print("  Uses eta, eta^2/(2theta4), theta3*phi/theta4 -- all at same q=1/phi")
print("=" * 65)
print(f"  LHS_fw = {nstr(LHS_fw, 10)}")
print(f"  RHS    = {nstr(RHS,    10)}")
print(f"  Match  = {(1-abs(dev_fw))*100:.6f}%  (this IS tautological)")
print()
# Verify analytically: LHS_fw = eta^2 / (eta^2/(2theta4) * theta4/(theta3phi))
#                             = eta^2 * 2theta4 * theta3phi / (eta^2 * theta4)
#                             = 2*theta3*phi   OK
print("  Analytical check: LHS_fw = eta^2/(eta^2/2theta4 * theta4/theta3phi) = 2theta3phi = RHS")
print("  => This collapses to an identity. Zero information content.")
print()

# ---------------------------------------------
# SIMPLE RATIO TEST: R = alpha_s / sqrt(sin^2theta_W * alpha_em)
# Framework: R = sqrt(2*theta3*phi)
# ---------------------------------------------
R_fw      = sqrt(RHS)

# Option B (mixed scale -- framework-natural)
R_B_meas  = as_meas / sqrt(sW_meas * a_0)
rel_err_R = sqrt(
    (as_err / as_meas)**2 +
    (sW_err / sW_meas / 2)**2 +
    (a_0_err / a_0 / 2)**2
)
sigma_R_B = R_B_meas * rel_err_R
dev_R_B   = float((R_B_meas - R_fw) / sigma_R_B)

# Option A (all M_Z)
R_A_meas  = as_meas / sqrt(sW_meas * a_MZ)
rel_err_RA = sqrt(
    (as_err / as_meas)**2 +
    (sW_err / sW_meas / 2)**2 +
    (a_MZ_err / a_MZ / 2)**2
)
sigma_R_A  = R_A_meas * rel_err_RA
dev_R_A    = float((R_A_meas - R_fw) / sigma_R_A)

print("=" * 65)
print("SIMPLE RATIO: R = alpha_s / sqrt(sin^2theta_W * alpha_em)")
print(f"  Framework: sqrt(2theta3phi) = {nstr(R_fw, 8)}")
print("=" * 65)
print(f"  Option A (all M_Z):  R = {nstr(R_A_meas,6)} +- {nstr(sigma_R_A,3)}")
print(f"    Deviation: {dev_R_A:.2f} sigma")
print(f"  Option B (mixed):    R = {nstr(R_B_meas,6)} +- {nstr(sigma_R_B,3)}")
print(f"    Deviation: {dev_R_B:.2f} sigma")
print()

# ---------------------------------------------
# SCALE-CORRECTION VERSION: what if we correct alpha_s and sin^2theta_W to q=0?
# alpha_s(q->0) is not well-defined (confinement), but sin^2theta_W(q=0)~0.2387 (on-shell)
# alpha_em(q=0) = 1/137.036
# Let's also try with on-shell sin^2theta_W for completeness
# ---------------------------------------------
sW_onshell     = mpf("0.22290")   # sin^2theta_W (on-shell/PDG)
sW_onshell_err = mpf("0.00030")

LHS_OS = as_meas**2 / (sW_onshell * a_0)
rel_err_OS = sqrt(
    (2 * as_err / as_meas)**2 +
    (sW_onshell_err / sW_onshell)**2 +
    (a_0_err / a_0)**2
)
sigma_LHS_OS = LHS_OS * rel_err_OS
dev_OS       = LHS_OS - RHS
sigma_OS_val = float(dev_OS / sigma_LHS_OS)
match_OS     = float(100 * (1 - abs(dev_OS) / RHS))

print("=" * 65)
print("OPTION C: alpha_s(M_Z), sin^2theta_W on-shell (0.22290), alpha_em(q=0)")
print("  (checking scale sensitivity)")
print("=" * 65)
print(f"  LHS   = {nstr(LHS_OS, 8)}")
print(f"  RHS   = {nstr(RHS,    8)}")
print(f"  Match = {match_OS:.2f}%")
print(f"  Deviation = {sigma_OS_val:.2f} sigma")
print()

# ---------------------------------------------
# INTERPRETATION SUMMARY
# ---------------------------------------------
print("=" * 65)
print("SUMMARY")
print("=" * 65)
print()
print(f"  RHS (framework) = 2*theta3(1/phi)*phi = {nstr(RHS, 8)}")
print()
print(f"  {'Option':<30} {'LHS':>10} {'Deviation':>14} {'sigma':>8}")
print(f"  {'-'*30} {'-'*10} {'-'*14} {'-'*8}")
print(f"  {'A: all M_Z':<30} {float(LHS_A):>10.4f} {float(LHS_A-RHS):>+14.4f} {sigma_A:>+8.2f}")
print(f"  {'B: mixed (fw-natural)':<30} {float(LHS_B):>10.4f} {float(LHS_B-RHS):>+14.4f} {sigma_B:>+8.2f}")
print(f"  {'C: on-shell sin^2theta_W':<30} {float(LHS_OS):>10.4f} {float(LHS_OS-RHS):>+14.4f} {sigma_OS_val:>+8.2f}")
print(f"  {'FW-internal (tautological)':<30} {float(LHS_fw):>10.4f} {'[tautology]':>14} {'---':>8}")
print()
print("  INTERPRETATION:")
print()
print(f"  Option A ({sigma_A:+.1f}sigma): Including alpha running to M_Z reveals a")
print(f"    ~{abs(float(LHS_A-RHS)/float(RHS))*100:.1f}% gap. The framework does NOT predict alpha running.")
print(f"    This is genuine tension -- the framework treats alpha as fixed at")
print(f"    its low-energy value while using other couplings at M_Z.")
print()
print(f"  Option B ({sigma_B:+.1f}sigma): Using framework-natural scales (1/alpha~136.39,")
print(f"    the test is {'CONSISTENT' if abs(sigma_B)<2 else 'MILDLY INCONSISTENT'}.")
print(f"    But mixing scales is physically ad hoc and must be justified.")
print()
print(f"  Option C ({sigma_OS_val:+.1f}sigma): On-shell sin^2theta_W gives larger mismatch.")
print()
print("  NON-TAUTOLOGICAL CONTENT:")
print("  The framework-internal (Option FW) collapses to an algebraic")
print("  identity 2theta3phi = 2theta3phi -- zero information. The real test is")
print("  whether measured values satisfy the relation AT ALL.")
print()
print("  BOTTOM LINE:")
if abs(sigma_B) < 1:
    verdict_B = "strong consistency"
elif abs(sigma_B) < 2:
    verdict_B = "consistency"
else:
    verdict_B = "tension"

if abs(sigma_A) > 3:
    print(f"  - Framework-natural (Option B): {sigma_B:.2f}sigma -> {verdict_B}")
    print(f"  - All-M_Z (Option A): {sigma_A:.2f}sigma -> SCALE MIXING IS THE KEY ISSUE")
    print(f"  - The test is consistent only if alpha is taken at q=0.")
    print(f"  - This raises a genuine open question: WHY does the framework")
    print(f"    mix alpha(q=0) with the others at M_Z?")
    print(f"  - One possible answer: the wall lives at a scale between M_Z")
    print(f"    and M_Pl where alpha has NOT yet run significantly from q=0,")
    print(f"    but alpha_s and sin^2theta_W have already decoupled.")
else:
    print(f"  - Option B: {sigma_B:.2f}sigma (consistent at mixed scale)")
    print(f"  - Option A: {sigma_A:.2f}sigma (tension at uniform M_Z scale)")

print()
print("  Dominant uncertainty source: alpha_s (+-{:.2f}%, contributes {:.1f}sigma eq.)".format(
    float(as_err/as_meas)*100*2,
    float(2*as_err/as_meas / rel_err_B)
))
print()
print("  LIVE TEST: alpha_s will be remeasured to +-0.0002 precision by")
print("  CODATA 2026-2027. If alpha_s -> 0.11840 (framework value), both")
print("  the direct alpha_s test AND this triangle test improve significantly.")
