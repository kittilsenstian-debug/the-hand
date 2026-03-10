#!/usr/bin/env python3
# verify_golden_node.py
# Independent verification of Golden Node claims
# Modular forms at the golden ratio nome q = 1/phi
# Uses mpmath for high-precision computation (80 digits)

import mpmath
from mpmath import mp, mpf, sqrt, log, pi, power

mp.dps = 80

phi = (1 + sqrt(5)) / 2
phibar = 1 / phi
q = phibar

alpha_s_meas = mpf("0.1179")
sin2tW_meas = mpf("0.23121")
inv_alpha_meas = mpf("137.035999084")
mu_meas = mpf("1836.15267343")
v_meas = mpf("246.22")
M_Pl = mpf("1.22089e19")
Lambda_meas = mpf("2.89e-122")

SEP = "=" * 72
DASH = "-" * 72
N_terms = 500

def sigma_k(n, k):
    s = mpf(0)
    for d in range(1, n + 1):
        if n % d == 0:
            s += power(d, k)
    return s

def pct_dev(pred, meas):
    return float(abs(pred - meas) / abs(meas) * 100)

def pf(pct, thr=1.0):
    if pct < thr: return "PASS"
    if pct < 5.0: return "MARGINAL"
    return "FAIL"

print(SEP)
print("GOLDEN NODE VERIFICATION")
print("Modular forms at q = 1/phi")
print(SEP)
print()
print("phi    = {:.10f}".format(float(phi)))
print("1/phi  = {:.10f}".format(float(phibar)))
print()

# ===== 1. DEDEKIND ETA =====
print(DASH)
print("1. DEDEKIND ETA FUNCTION at q = 1/phi")
print(DASH)
eta_product = mpf(1)
for n in range(1, N_terms + 1):
    eta_product *= (1 - q**n)
eta_val = q ** (mpf(1) / 24) * eta_product

print("eta(1/phi) = {:.10f}".format(float(eta_val)))
print("alpha_s(M_Z) measured = 0.1179 +/- 0.0009")
d = pct_dev(eta_val, alpha_s_meas)
print("Difference: {:.6e}".format(float(abs(eta_val - alpha_s_meas))))
print("Relative deviation: {:.4f}%%".format(d))
print("RESULT: [{}]".format(pf(d)))
print()

# ===== 2. JACOBI THETA =====
print(DASH)
print("2. JACOBI THETA FUNCTIONS at q = 1/phi")
print(DASH)
theta2_sum = mpf(0)
for n in range(N_terms):
    theta2_sum += q ** (n * (n + 1))
theta2 = 2 * q ** (mpf(1) / 4) * theta2_sum

theta3_sum = mpf(0)
for n in range(1, N_terms + 1):
    val = q ** (n * n)
    if val < mpf(10) ** (-70): break
    theta3_sum += val
theta3 = 1 + 2 * theta3_sum

theta4_sum = mpf(0)
for n in range(1, N_terms + 1):
    val = q ** (n * n)
    if val < mpf(10) ** (-70): break
    theta4_sum += ((-1) ** n) * val
theta4 = 1 + 2 * theta4_sum

print("theta_2(1/phi) = {:.10f}".format(float(theta2)))
print("theta_3(1/phi) = {:.10f}".format(float(theta3)))
print("theta_4(1/phi) = {:.10f}".format(float(theta4)))
print()
print("CHECK: theta_2 =? theta_3")
diff_23 = abs(theta2 - theta3)
print("  |theta_2 - theta_3| = {:.4e}".format(float(diff_23)))
if diff_23 < mpf(10) ** (-8):
    print("  RESULT: theta_2 = theta_3 to 8+ decimal places  [PASS]")
else:
    print("  RESULT: theta_2 != theta_3 to 8 decimal places  [FAIL]")
    if diff_23 > 0:
        print("  (They differ at the {:.1f}-th decimal place)".format(float(-log(diff_23, 10))))
print()
print("  theta_3 / theta_4 = {:.10f}".format(float(theta3 / theta4)))
print("  theta_2 / theta_3 = {:.10f}".format(float(theta2 / theta3)))
print("  theta_2 / theta_4 = {:.10f}".format(float(theta2 / theta4)))
print()

# ===== 3. EISENSTEIN =====
print(DASH)
print("3. EISENSTEIN SERIES E4, E6 at q = 1/phi")
print(DASH)
N_eis = 200
e4_sum = mpf(0)
for n in range(1, N_eis + 1):
    e4_sum += sigma_k(n, 3) * q**n
E4 = 1 + 240 * e4_sum

e6_sum = mpf(0)
for n in range(1, N_eis + 1):
    e6_sum += sigma_k(n, 5) * q**n
E6 = 1 - 504 * e6_sum

print("E4(1/phi) = {:.10f}".format(float(E4)))
print("E6(1/phi) = {:.10f}".format(float(E6)))
print()
print("j-invariant = 1728 * E4^3 / (E4^3 - E6^2)")
denom_j = E4**3 - E6**2
if abs(denom_j) > mpf(10)**(-20):
    j_inv = 1728 * E4**3 / denom_j
    print("j(q=1/phi) = {:.10f}".format(float(j_inv)))
else:
    print("j-invariant: denominator near zero!")
print()

# ===== 4. PHYSICAL CONSTANTS =====
print(DASH)
print("4. PHYSICAL CONSTANT FORMULAS")
print(DASH)

print("(a) alpha_s = eta(1/phi)")
print("    Predicted:  {:.10f}".format(float(eta_val)))
print("    Measured:   0.1179 +/- 0.0009")
print()

sin2_pred = eta_val**2 / (2 * theta4)
print("(b) sin^2(theta_W) = eta^2 / (2*theta_4)")
print("    Predicted:  {:.10f}".format(float(sin2_pred)))
print("    Measured:   {:.10f}".format(float(sin2tW_meas)))
d = pct_dev(sin2_pred, sin2tW_meas)
print("    Deviation:  {:.4f}%%".format(d))
print("    RESULT: [{}]".format(pf(d)))
print()

inv_alpha_pred = (theta3 / theta4) * phi
print("(c) 1/alpha = (theta_3/theta_4) * phi")
print("    Predicted:  {:.10f}".format(float(inv_alpha_pred)))
print("    Measured:   {:.10f}".format(float(inv_alpha_meas)))
d = pct_dev(inv_alpha_pred, inv_alpha_meas)
print("    Deviation:  {:.4f}%%".format(d))
print("    RESULT: [{}]".format(pf(d)))
print()

mw_proxy = E4 ** (mpf(1) / 3) * phi**2
print("(d) M_W proxy = E4^(1/3) * phi^2")
print("    Value:      {:.10f}".format(float(mw_proxy)))
print("    (This is a dimensionless proxy; would need energy scale for GeV)")
print()

# ===== 5. MU CORRECTION =====
print(DASH)
print("5. PROTON-TO-ELECTRON MASS RATIO (mu) CORRECTION")
print(DASH)

mu_0 = mpf(6)**5 / phi**3
mu_corrected = mu_0 + 9 * phibar**2 / 7

print("mu_0 = 6^5 / phi^3 = {:.10f}".format(float(mu_0)))
print("Correction = 9*(1/phi)^2 / 7 = {:.10f}".format(float(9 * phibar**2 / 7)))
print("mu_corrected = mu_0 + correction = {:.10f}".format(float(mu_corrected)))
print("mu_measured  = {:.10f}".format(float(mu_meas)))
d = pct_dev(mu_corrected, mu_meas)
print("Deviation:   {:.4f}%%".format(d))
if d < 0.1:
    print("RESULT: [PASS] (within 0.1%%)")
elif d < 1.0:
    print("RESULT: [MARGINAL] (within 1%%)")
else:
    print("RESULT: [FAIL]")
print()

# ===== 6. HIERARCHY =====
print(DASH)
print("6. ELECTROWEAK HIERARCHY FORMULA")
print(DASH)

denominator_h = 1 - phi * theta4
v_pred = M_Pl * phibar**80 / denominator_h

print("phibar^80 = {:.6e}".format(float(phibar**80)))
print("1 - phi*theta_4 = {:.10f}".format(float(denominator_h)))
print("v_predicted = M_Pl * phibar^80 / (1 - phi*theta_4)")
print("            = {:.6e} GeV".format(float(v_pred)))
print("v_measured  = {:.2f} GeV".format(float(v_meas)))

if abs(denominator_h) < mpf(10)**(-10):
    print("WARNING: Denominator is near zero, formula is singular")
else:
    d = pct_dev(v_pred, v_meas)
    print("Deviation:    {:.4f}%%".format(d))
    if d < 1.0:
        print("RESULT: [PASS]")
    elif d < 10.0:
        print("RESULT: [MARGINAL]")
    else:
        ratio = float(v_pred / v_meas)
        print("RESULT: [FAIL] (ratio predicted/measured = {:.4e})".format(ratio))
print()

# ===== 7. COSMOLOGICAL CONSTANT =====
print(DASH)
print("7. COSMOLOGICAL CONSTANT FORMULA")
print(DASH)

Lambda_pred = theta4**80 * sqrt(5) / phi**2

print("theta_4^80     = {:.6e}".format(float(theta4**80)))
print("sqrt(5)/phi^2  = {:.10f}".format(float(sqrt(5) / phi**2)))
print("Lambda/M_Pl^4 predicted = theta_4^80 * sqrt(5)/phi^2")
print("              = {:.6e}".format(float(Lambda_pred)))
print("Lambda/M_Pl^4 measured  ~ {:.2e}".format(float(Lambda_meas)))

if Lambda_pred > 0:
    log_pred = float(log(Lambda_pred, 10))
    log_meas = float(log(Lambda_meas, 10))
    print("log10(predicted) = {:.2f}".format(log_pred))
    print("log10(measured)  = {:.2f}".format(log_meas))
    print("Exponent difference: {:.2f}".format(abs(log_pred - log_meas)))
    if abs(log_pred - log_meas) < 2:
        print("RESULT: [PASS] (correct order of magnitude)")
    elif abs(log_pred - log_meas) < 5:
        print("RESULT: [MARGINAL]")
    else:
        print("RESULT: [FAIL]")
else:
    print("RESULT: Predicted value is not positive [FAIL]")
print()

# ===== 8. ROGERS-RAMANUJAN =====
print(DASH)
print("8. ROGERS-RAMANUJAN CONTINUED FRACTION at q = 1/phi")
print(DASH)

rr_product = mpf(1)
for n in range(1, N_terms + 1):
    num = (1 - q**(5*n - 4)) * (1 - q**(5*n - 1))
    den = (1 - q**(5*n - 3)) * (1 - q**(5*n - 2))
    rr_product *= num / den

R_val = q ** (mpf(1) / 5) * rr_product

print("R(1/phi) = {:.10f}".format(float(R_val)))
print("1/phi    = {:.10f}".format(float(phibar)))
print("|R(1/phi) - 1/phi| = {:.4e}".format(float(abs(R_val - phibar))))
print()
print("Other comparisons:")
print("  phi - 1        = {:.10f}  (same as 1/phi)".format(float(phi - 1)))
print("  (sqrt(5)-1)/2  = {:.10f}".format(float((sqrt(5) - 1) / 2)))

diff = abs(R_val - phibar)
d = float(diff / phibar * 100)
print("  Deviation from 1/phi: {:.4f}%%".format(d))
if d < 0.01:
    print("RESULT: R(1/phi) = 1/phi to high precision  [PASS]")
elif d < 1.0:
    print("RESULT: R(1/phi) ~ 1/phi approximately  [MARGINAL]")
else:
    print("RESULT: R(1/phi) != 1/phi  [FAIL]")
print()

# ===== 9. RAMANUJAN DISCRIMINANT =====
print(DASH)
print("9. RAMANUJAN DISCRIMINANT: Delta = eta^24")
print(DASH)

Delta_val = eta_val ** 24
alpha_s_24 = alpha_s_meas ** 24

print("eta(1/phi)^24    = {:.6e}".format(float(Delta_val)))
print("alpha_s^24       = {:.6e}".format(float(alpha_s_24)))
print("|Delta - alpha_s^24| = {:.4e}".format(float(abs(Delta_val - alpha_s_24))))

if abs(alpha_s_24) > 0:
    d = pct_dev(Delta_val, alpha_s_24)
    print("Relative deviation: {:.4f}%%".format(d))

print()
print("Note: If eta(1/phi) = alpha_s, then Delta(1/phi) = alpha_s^24 by definition.")
print("This is tautological IF claim 1 holds.")
print()

# ===== 10. UNIQUENESS TEST =====
print(DASH)
print("10. UNIQUENESS TEST: Scanning q from 0.50 to 0.70")
print(DASH)

mp.dps = 30
N_scan = 200

def eta_quick(qq, nterms=N_scan):
    prod = mpf(1)
    for n in range(1, nterms + 1):
        prod *= (1 - qq**n)
    return qq ** (mpf(1)/24) * prod

def theta3_quick(qq, nterms=N_scan):
    s = mpf(0)
    for n in range(1, nterms + 1):
        val = qq ** (n*n)
        if val < mpf(10)**(-25): break
        s += val
    return 1 + 2*s

def theta4_quick(qq, nterms=N_scan):
    s = mpf(0)
    for n in range(1, nterms + 1):
        val = qq ** (n*n)
        if val < mpf(10)**(-25): break
        s += ((-1)**n) * val
    return 1 + 2*s

target_as  = mpf("0.1179")
target_sw  = mpf("0.23121")
target_inv = mpf("137.036")
phi_scan   = (1 + sqrt(5)) / 2

print("For each q, checking 3 conditions (within 1%% of measured):")
print("  (A) |eta(q) - 0.1179| / 0.1179 < 1%%")
print("  (B) |eta^2/(2*theta_4) - 0.2312| / 0.2312 < 1%%")
print("  (C) |(theta_3/theta_4)*phi - 137.036| / 137.036 < 1%%")
print()

results = []
for i in range(201):
    qq = mpf("0.50") + mpf(i) / 1000
    e = eta_quick(qq)
    t3 = theta3_quick(qq)
    t4 = theta4_quick(qq)
    dev_a = float(abs(e - target_as) / target_as * 100)
    pass_a = dev_a < 1.0
    sw = e**2 / (2 * t4)
    dev_b = float(abs(sw - target_sw) / target_sw * 100)
    pass_b = dev_b < 1.0
    inv_a = (t3 / t4) * phi_scan
    dev_c = float(abs(inv_a - target_inv) / target_inv * 100)
    pass_c = dev_c < 1.0
    n_pass = sum([pass_a, pass_b, pass_c])
    if n_pass >= 2:
        results.append((float(qq), n_pass, dev_a, dev_b, dev_c,
                        float(e), float(sw), float(inv_a)))

print("q values satisfying 2 or more conditions:")
hdr = "{:>6s}  {:>5s}  {:>8s}  {:>8s}  {:>8s}  {:>10s}  {:>10s}  {:>10s}"
print(hdr.format("q", "N_OK", "dev_A%%", "dev_B%%", "dev_C%%", "eta", "sin2tW", "1/alpha"))
print("-" * 80)

for (qq, n_pass, da, db, dc, ev, sw, ia) in results:
    marker = " <-- 1/phi" if abs(qq - 0.618) < 0.001 else ""
    row = "{:6.3f}  {:5d}  {:8.4f}  {:8.4f}  {:8.4f}  {:10.6f}  {:10.6f}  {:10.4f}{}"
    print(row.format(qq, n_pass, da, db, dc, ev, sw, ia, marker))

print()
print("Total q values (of 201 scanned) matching 2+ conditions: {}".format(len(results)))

all3 = [r for r in results if r[1] == 3]
print("Total q values matching ALL 3 conditions:               {}".format(len(all3)))

if len(all3) == 0:
    print()
    print("No q value matches all 3 simultaneously within 1%%.")
    print("Checking with 5%% tolerance...")
    results_5pct = []
    for i in range(201):
        qq = mpf("0.50") + mpf(i) / 1000
        e = eta_quick(qq)
        t3 = theta3_quick(qq)
        t4 = theta4_quick(qq)
        dev_a = float(abs(e - target_as) / target_as * 100)
        sw = e**2 / (2 * t4)
        dev_b = float(abs(sw - target_sw) / target_sw * 100)
        inv_a = (t3 / t4) * phi_scan
        dev_c = float(abs(inv_a - target_inv) / target_inv * 100)
        if dev_a < 5 and dev_b < 5 and dev_c < 5:
            results_5pct.append((float(qq), dev_a, dev_b, dev_c))
    print("q values matching all 3 within 5%%:")
    for (qq, da, db, dc) in results_5pct:
        marker = " <-- 1/phi" if abs(qq - 0.618) < 0.001 else ""
        print("  q={:.3f}  dev_A={:.2f}%%  dev_B={:.2f}%%  dev_C={:.2f}%%{}".format(
            qq, da, db, dc, marker))
    if len(results_5pct) == 0:
        print("  (none)")
print()

# Reset precision for summary
mp.dps = 80

# ===== SUMMARY =====
print(SEP)
print("SUMMARY OF ALL VERIFICATIONS")
print(SEP)
print()

q = phibar
eta_product = mpf(1)
for n in range(1, 501):
    eta_product *= (1 - q**n)
eta_val = q ** (mpf(1)/24) * eta_product

theta3_sum = mpf(0)
for n in range(1, 501):
    val = q ** (n*n)
    if val < mpf(10)**(-70): break
    theta3_sum += val
theta3 = 1 + 2 * theta3_sum

theta4_sum = mpf(0)
for n in range(1, 501):
    val = q ** (n*n)
    if val < mpf(10)**(-70): break
    theta4_sum += ((-1)**n) * val
theta4 = 1 + 2 * theta4_sum

theta2_sum = mpf(0)
for n in range(500):
    theta2_sum += q ** (n*(n+1))
theta2 = 2 * q**(mpf(1)/4) * theta2_sum

rr_product = mpf(1)
for n in range(1, 501):
    num = (1 - q**(5*n-4)) * (1 - q**(5*n-1))
    den = (1 - q**(5*n-3)) * (1 - q**(5*n-2))
    rr_product *= num / den
R_val = q**(mpf(1)/5) * rr_product

mu_0 = mpf(6)**5 / phi**3
mu_corrected = mu_0 + 9*phibar**2 / 7

results_summary = [
    ("1. eta(1/phi) vs alpha_s",
     float(eta_val), 0.1179,
     pct_dev(eta_val, mpf("0.1179"))),
    ("2. theta_2 =? theta_3",
     float(theta2), float(theta3),
     float(abs(theta2 - theta3))),
    ("4a. alpha_s = eta(1/phi)",
     float(eta_val), 0.1179,
     pct_dev(eta_val, mpf("0.1179"))),
    ("4b. sin2_tW = eta^2/(2*theta_4)",
     float(eta_val**2 / (2*theta4)), 0.23121,
     pct_dev(eta_val**2/(2*theta4), mpf("0.23121"))),
    ("4c. 1/alpha = (theta_3/theta_4)*phi",
     float((theta3/theta4)*phi), 137.036,
     pct_dev((theta3/theta4)*phi, mpf("137.036"))),
    ("5. mu corrected",
     float(mu_corrected), float(mu_meas),
     pct_dev(mu_corrected, mu_meas)),
    ("8. R(1/phi) vs 1/phi",
     float(R_val), float(phibar),
     pct_dev(R_val, phibar)),
]

hdr2 = "{:<35s}  {:>12s}  {:>12s}  {:>10s}"
print(hdr2.format("Claim", "Predicted", "Target", "Dev (%%)"))
print("-" * 72)

for (name, pred, targ, dev) in results_summary:
    if name.startswith("2."):
        print("{:<35s}  {:>12.8f}  {:>12.8f}  |diff|={:.2e}".format(
            name, pred, targ, dev))
    else:
        status = pf(dev)
        print("{:<35s}  {:>12.8f}  {:>12.8f}  {:>8.4f}%%  [{}]".format(
            name, pred, targ, dev, status))

print()
print("KEY MODULAR FORM VALUES AT q = 1/phi:")
print("  eta(1/phi)    = {:.15f}".format(float(eta_val)))
print("  theta_2(1/phi)= {:.15f}".format(float(theta2)))
print("  theta_3(1/phi)= {:.15f}".format(float(theta3)))
print("  theta_4(1/phi)= {:.15f}".format(float(theta4)))
print("  R(1/phi)      = {:.15f}".format(float(R_val)))
print("  1/phi         = {:.15f}".format(float(phibar)))
print()
print(SEP)
print("END OF VERIFICATION")
print(SEP)
