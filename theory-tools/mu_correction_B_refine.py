#!/usr/bin/env python3
"""
mu_correction_B_refine.py -- Fix sign error and find clean B refinement
Feb 26, 2026
"""
import mpmath
from mpmath import mp, mpf, sqrt, log, pi

mp.dps = 60

phi = (1 + sqrt(5)) / 2
q = 1 / phi
alpha = 1 / mpf("137.035999084")
mu_meas = mpf("1836.15267343")
mu_unc = mpf("0.00000011")

N = 500
eta_p = mpf(1)
for n in range(1, N + 1):
    eta_p *= (1 - q**n)
eta = q ** (mpf(1)/24) * eta_p

theta4_sum = mpf(0)
for n in range(1, N + 1):
    v = q ** (n*n)
    if v < mpf(10)**(-50): break
    theta4_sum += ((-1)**n) * v
theta4 = 1 + 2 * theta4_sum

mu_0 = mpf(6)**5 / phi**3
mu_1 = 9 / (7 * phi**2)
mu_pred = mu_0 + mu_1
delta = mu_pred - mu_meas

# Candidate B: correction = (7/2)*alpha*eta
corr_B = mpf(7)/2 * alpha * eta
mu_B = mu_pred - corr_B
res_B = mu_B - mu_meas
# res_B is NEGATIVE (mu_B < mu_meas), so B overcorrects

print("=" * 78)
print("CANDIDATE B SIGN-CORRECT REFINEMENT")
print("=" * 78)
print(f"delta = {float(delta):.15e}")
print(f"corr_B = (7/2)*alpha*eta = {float(corr_B):.15e}")
print(f"corr_B - delta = {float(corr_B - delta):.15e}")
print(f"So corr_B > delta: B OVERCORRECTS by {float(corr_B-delta):.6e}")
print(f"mu_B = {float(mu_B):.15f}")
print(f"mu_meas = {float(mu_meas):.15f}")
print(f"res_B = mu_B - mu_meas = {float(res_B):.6e} (NEGATIVE: mu_B too small)")
print()
print("To fix: we need to ADD something back.")
print("The third correction should be POSITIVE (adding to mu).")
print("mu = 6^5/phi^3 + 9/(7*phi^2) - (7/2)*alpha*eta + X, X > 0")
print("X should be ~ 5.36e-6")

X_needed = mu_meas - mu_B  # positive
print(f"\nX needed = {float(X_needed):.15e}")
print(f"X/alpha^2 = {float(X_needed/alpha**2):.10f}")
print(f"X/alpha = {float(X_needed/alpha):.10e}")
print(f"X/(alpha*eta) = {float(X_needed/(alpha*eta)):.10e}")
print(f"X/(alpha^2*eta) = {float(X_needed/(alpha**2*eta)):.10f}")

# X/alpha^2 ~ 0.1006
c = X_needed / alpha**2
print(f"\nLooking for clean expression for c = X/alpha^2 = {float(c):.15f}")

# Check candidates
candidates = [
    ("1/10", mpf(1)/10),
    ("1/pi^2", 1/pi**2),
    ("3/29", mpf(3)/29),
    ("phi/16", phi/16),
    ("1/(3*sqrt(phi))", 1/(3*sqrt(phi))),
    ("eta/eta (trivial)", eta/eta * mpf("0.1006")),  # skip
    ("theta4/eta^2", theta4/eta**2),
    ("theta4^2/eta^3", theta4**2/eta**3),
    ("1/(phi^5-1)", 1/(phi**5-1)),
    ("1/(phi^5)", 1/phi**5),
    ("phi^(-5)", phi**(-5)),
    ("(sqrt(5)-2)/10", (sqrt(5)-2)/10),
    ("3/30", mpf(3)/30),
    ("3/(L(7)+1)", mpf(3)/30),
    ("1/(2*phi^4-4)", 1/(2*phi**4-4)),
    ("3*theta4", 3*theta4),
    ("eta^2/phi", eta**2/phi),
    ("theta4/3", theta4/3),
    ("sqrt(eta)", sqrt(eta)),
    ("eta/(phi+1/phi)", eta/(phi+1/phi)),
    ("eta/sqrt(5)", eta/sqrt(5)),
    ("1/(10+1/phi^2)", 1/(10+1/phi**2)),
    ("alpha*phi", alpha*phi),
]

results = []
for label, val in candidates:
    err = float(abs(val - c)/c * 100)
    if err < 10:
        mu_test = mu_B + alpha**2 * val
        ppb = float((mu_test - mu_meas)/mu_meas*1e9)
        sig = float((mu_test - mu_meas)/mu_unc)
        results.append((abs(float(ppb)), label, float(val), ppb, sig))

results.sort()
print(f"\n{'Expression':30s} {'value':>14s} {'err%':>8s} {'mu ppb':>8s} {'sigma':>8s}")
print("-"*78)
for _, label, val, ppb, sig in results:
    err = abs(val - float(c))/float(c)*100
    print(f"{label:30s} {val:14.10f} {err:8.4f} {ppb:8.3f} {sig:8.2f}")

# Now search systematically: X = alpha^2 * n/m
print(f"\n{'='*78}")
print("SYSTEMATIC: X = alpha^2 * a/b (a,b integers)")
print(f"{'='*78}")

best_ab = []
for a in range(1, 50):
    for b in range(1, 200):
        val = mpf(a)/b
        err = float(abs(val - c)/c * 100)
        if err < 0.5:
            mu_test = mu_B + alpha**2 * val
            ppb = float((mu_test - mu_meas)/mu_meas*1e9)
            sig = float((mu_test - mu_meas)/mu_unc)
            best_ab.append((abs(float(ppb)), f"{a}/{b}", float(val), ppb, sig))

best_ab.sort()
print(f"\nTOP 10 rational X/alpha^2:")
print(f"{'a/b':>12s} {'value':>14s} {'err%':>8s} {'mu ppb':>8s} {'sigma':>8s}")
print("-"*60)
for _, label, val, ppb, sig in best_ab[:10]:
    err = abs(val - float(c))/float(c)*100
    print(f"{label:>12s} {val:14.10f} {err:8.4f} {ppb:8.3f} {sig:8.2f}")

# Also try X = alpha^2 * phi-expression
print(f"\n{'='*78}")
print("SYSTEMATIC: X = alpha^2 * a/(b*phi^c)")
print(f"{'='*78}")

best_phi = []
for a in range(1, 30):
    for b in range(1, 50):
        for c_pow in range(-4, 5):
            val = mpf(a) / (mpf(b) * phi**c_pow)
            err = float(abs(val - c)/c * 100)
            if err < 0.05:
                mu_test = mu_B + alpha**2 * val
                ppb = float((mu_test - mu_meas)/mu_meas*1e9)
                sig = float((mu_test - mu_meas)/mu_unc)
                best_phi.append((abs(float(ppb)), f"{a}/({b}*phi^{c_pow})", float(val), ppb, sig))

best_phi.sort()
print(f"\nTOP 10 phi-power X/alpha^2:")
print(f"{'Expression':>25s} {'value':>14s} {'err%':>8s} {'mu ppb':>8s} {'sigma':>8s}")
print("-"*73)
for _, label, val, ppb, sig in best_phi[:10]:
    err = abs(val - float(c))/float(c)*100
    print(f"{label:>25s} {val:14.10f} {err:8.4f} {ppb:8.3f} {sig:8.2f}")

# ====================================================================
# THE BIG PICTURE: WHAT IF CANDIDATE E IS THE CORRECT 2nd CORRECTION?
# Then we need a 3rd correction for the -0.45 ppb residual
# ====================================================================
print(f"\n{'='*78}")
print("IF CANDIDATE E IS CORRECT: 3rd CORRECTION FOR -0.45 ppb")
print(f"{'='*78}")

corr_E = 12 * alpha / 29
mu_E = mu_pred - corr_E
res_E = mu_E - mu_meas  # ~ -0.83e-6

print(f"mu_E = {float(mu_E):.15f}")
print(f"res_E = {float(res_E):.6e} (need to ADD {float(-res_E):.6e})")
print(f"res_E/alpha^2 = {float(res_E/alpha**2):.6f}")
print(f"res_E/alpha^3 = {float(res_E/alpha**3):.6f}")
print(f"res_E/(alpha^2*eta) = {float(res_E/(alpha**2*eta)):.6f}")

# res_E/alpha^2 ~ -0.0156
# Try: -alpha^2/(64) = -0.01563... VERY close!
print(f"\nalpha^2/64 = {float(alpha**2/64):.15e}")
print(f"|res_E|     = {float(abs(res_E)):.15e}")
print(f"Ratio: {float(abs(res_E)/(alpha**2/64)):.10f}")
# Nope, res_E is -8.3e-7, alpha^2/64 = 8.3e-7... wait that's actually right!
print(f"res_E + alpha^2/64 = {float(res_E + alpha**2/64):.6e}")

# Fourth term: +alpha^2/(64)
mu_E3 = mu_E + alpha**2/64
res_E3 = mu_E3 - mu_meas
print(f"\nmu = 6^5/phi^3 + 9/(7*phi^2) - 12*alpha/29 + alpha^2/64")
print(f"mu = {float(mu_E3):.15f}")
print(f"ppb = {float(res_E3/mu_meas*1e9):.3f}")
print(f"sigma = {float(res_E3/mu_unc):.2f}")

# Also try alpha^2 * phi^k / m
for a in range(1, 20):
    for b in [1,2,3,4,5,6,7,8,9,10,12,14,16,18,20,24,29,30,32,36,47,48,49,64]:
        for c_pow in range(-3, 4):
            val = mpf(a) / (mpf(b) * phi**c_pow)
            test = alpha**2 * val
            new_res = mu_E + test - mu_meas
            ppb = float(abs(new_res/mu_meas*1e9))
            if ppb < 0.1:
                sig = float(new_res/mu_unc)
                print(f"  + alpha^2*{a}/({b}*phi^{c_pow}) = {float(test):.8e} -> ppb={float(new_res/mu_meas*1e9):.4f}, sigma={sig:.2f}")

# ====================================================================
# FINAL DEFINITIVE TABLE
# ====================================================================
print(f"\n{'#'*78}")
print("DEFINITIVE FORMULAS FOR MU")
print(f"{'#'*78}")
print()

formulas = [
    ("LEADING ORDER", "6^5/phi^3 + 9/(7*phi^2)", mu_pred, 2, "number-theoretic"),
    ("+ COUPLING", "... - (7/2)*alpha*alpha_s", mu_B, 0, "QCD-QED mixed"),
    ("+ COUPLING", "... - 12*alpha/29", mu_E, 1, "Lucas convergent"),
    ("+ COUPLING", "... - alpha*(sqrt(2)-1)", mu_pred - alpha*(sqrt(2)-1), 1, "kink mass?"),
    ("+ 2-LOOP", "... - alpha*(sqrt(2)-1) + alpha^2/(2*phi^4)", mu_pred - alpha*(sqrt(2)-1) + alpha**2/(2*phi**4), 2, "kink+phi"),
]

print(f"{'Type':12s} {'Formula':50s} {'ppb':>8s} {'sigma':>8s} {'Free':>5s} {'Note':20s}")
print("-"*110)
for typ, formula, mu_val, free, note in formulas:
    res = mu_val - mu_meas
    ppb = float(res/mu_meas*1e9)
    sig = float(res/mu_unc)
    print(f"{typ:12s} {formula:50s} {ppb:8.2f} {sig:8.1f} {free:5d} {note:20s}")

print(f"\nMeasurement: mu = 1836.15267343 +/- 0.00000011 (0.06 ppb, 1 sigma)")
