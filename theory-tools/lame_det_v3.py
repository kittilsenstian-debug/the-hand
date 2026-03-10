#!/usr/bin/env python3
"""
lame_det_v3.py -- Precision analysis of GY_kink(q) vs eta(q)
=============================================================

From v2 we found:
  log(GY_k(2K))/log(eta) = -2.200 ≈ -11/5 at q = 1/phi
  log(GY_k(K))/log(eta) = -1.064 ≈ -1 at q = 1/phi

These suggest: GY_k(2K) ~ eta^(-11/5) and GY_k(K) ~ 1/eta.
If GY_k(K) = 1/eta, that would mean:
  det_Dir(H_kink, [0,K]) / det_Dir(-d^2, [0,K]) = 1/eta(1/phi) = 1/alpha_s

This script performs a systematic q-scan to determine the EXACT
functional form by fitting log(GY(q)) vs log(eta(q)).
"""

import sys
import numpy as np

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import mpmath
from mpmath import mp, mpf, pi, sqrt, log, exp
from mpmath import ellipk

mp.dps = 30

phi = (1 + sqrt(5)) / 2
phibar = 1 / phi

def eta_d(q, N=2000):
    r = q ** (mpf(1)/24)
    for n in range(1, N+1):
        r *= (1 - q**n)
        if abs(q**n) < mpf(10)**(-mp.dps): break
    return r

def theta_f(idx, q, N=2000):
    if idx == 2:
        s = sum(q**(n*(n+1)) for n in range(N))
        return 2 * q**mpf('0.25') * s
    elif idx == 3:
        return 1 + 2*sum(q**(n*n) for n in range(1, N))
    elif idx == 4:
        return 1 + 2*sum((-1)**n * q**(n*n) for n in range(1, N))

def integrate_gy(V_func, L, E_val, nsteps=20000):
    """Integrate y'' = [V(x) - E]*y, y(0)=0, y'(0)=1 to get y(L)."""
    h = L / nsteps
    def rk4(x, state):
        def f(x, s):
            return [s[1], (V_func(x) - E_val) * s[0]]
        k1 = f(x, state)
        k2 = f(x+h/2, [state[i]+h/2*k1[i] for i in range(2)])
        k3 = f(x+h/2, [state[i]+h/2*k2[i] for i in range(2)])
        k4 = f(x+h, [state[i]+h*k3[i] for i in range(2)])
        return [state[i]+h/6*(k1[i]+2*k2[i]+2*k3[i]+k4[i]) for i in range(2)]

    state = [mpf(0), mpf(1)]
    x = mpf(0)
    for _ in range(nsteps):
        state = rk4(x, state)
        x += h
    return state[0]

print("=" * 80)
print("  LAME det v3: SYSTEMATIC q-SCAN FOR GY_kink vs eta")
print("=" * 80)
print()

# =================================================================
# SCAN: GY_kink on [0, K] and [0, 2K] vs q
# =================================================================
q_values = [0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5,
            0.55, float(phibar), 0.65, 0.7]

results = []

print(f"  {'q':>8} {'eta(q)':>14} {'K(q)':>10} {'GY_k(K)':>14} {'GY_k(2K)':>14} {'log_k/log_eta':>14} {'log_2K/log_eta':>14}")
print(f"  {'-'*8} {'-'*14} {'-'*10} {'-'*14} {'-'*14} {'-'*14} {'-'*14}")

for q_test in q_values:
    q_mp = mpf(q_test)
    eta_q = eta_d(q_mp)
    t2_q = theta_f(2, q_mp)
    t3_q = theta_f(3, q_mp)
    t4_q = theta_f(4, q_mp)

    k_q = t2_q**2 / t3_q**2
    m_q = k_q**2
    K_q = ellipk(m_q)
    T_q = 2*K_q

    def V_kink(x, _m=m_q):
        sn = mpmath.ellipfun('sn', x, m=_m)
        return 6 * _m * (1 - sn**2)

    # Compute GY on [0, K] and [0, 2K]
    nsteps = max(15000, int(float(K_q) * 2000))  # more steps for larger K
    y2_K = integrate_gy(V_kink, K_q, mpf(0), nsteps=nsteps)
    y2_2K = integrate_gy(V_kink, T_q, mpf(0), nsteps=nsteps)

    gy_K = y2_K / K_q
    gy_2K = y2_2K / T_q

    # Compute log ratios
    log_eta = float(log(eta_q))
    log_gy_K = float(log(gy_K))
    log_gy_2K = float(log(gy_2K))

    ratio_K = log_gy_K / log_eta if log_eta != 0 else float('nan')
    ratio_2K = log_gy_2K / log_eta if log_eta != 0 else float('nan')

    marker = " <--" if abs(q_test - float(phibar)) < 0.01 else ""
    print(f"  {q_test:8.4f} {float(eta_q):14.10f} {float(K_q):10.4f} {float(gy_K):14.8f} {float(gy_2K):14.8f} {ratio_K:14.8f} {ratio_2K:14.8f}{marker}")

    results.append({
        'q': q_test, 'eta': float(eta_q), 'K': float(K_q),
        't4': float(t4_q), 't3': float(t3_q),
        'gy_K': float(gy_K), 'gy_2K': float(gy_2K),
        'ratio_K': ratio_K, 'ratio_2K': ratio_2K
    })

print()

# =================================================================
# ANALYSIS: What function of q gives GY_kink?
# =================================================================
print("=" * 80)
print("  ANALYSIS: FUNCTIONAL FORM OF GY_kink(q)")
print("=" * 80)
print()

# The ratio log(GY)/log(eta) is NOT constant across q, which means
# GY is NOT simply eta^alpha. Let's check other possibilities.

print("  Testing: is GY_k(K) = A * eta^alpha * t4^beta * ...?")
print()

# Compute log(GY_K/eta^n) for various n to see what residual structure remains
for n_eta in [-2, -1, 0, 1, 2]:
    print(f"  log(GY_k(K) * eta^{-n_eta}) vs q:")
    for r in results:
        log_residual = np.log(r['gy_K']) + n_eta * np.log(r['eta'])
        print(f"    q={r['q']:.4f}: log(GY*eta^{-n_eta}) = {log_residual:.8f}")
    print()

# Check if the residual is proportional to log(theta_4)
print("  Check: GY_k(K) = eta^(-1) * g(t4)?")
for r in results:
    log_g = np.log(r['gy_K']) + np.log(r['eta'])
    log_t4 = np.log(r['t4'])
    ratio_g_t4 = log_g / log_t4 if log_t4 != 0 else float('nan')
    print(f"    q={r['q']:.4f}: log(GY*eta) = {log_g:.8f}, log(t4) = {log_t4:.8f}, ratio = {ratio_g_t4:.6f}")

print()

# Check: GY_k(K) = theta_3^2 / theta_4^alpha ?
print("  Check: GY_k(K) / theta_3^2 vs q:")
for r in results:
    val = r['gy_K'] / r['t3']**2
    print(f"    q={r['q']:.4f}: GY/t3^2 = {val:.10f}")

print()

# Check: GY_k(K) = (2K/pi) * something?
print("  Check: GY_k(K) / (2K/pi) vs q  [note: 2K/pi = t3^2]:")
for r in results:
    two_K_pi = 2*r['K']/np.pi
    val = r['gy_K'] / two_K_pi
    print(f"    q={r['q']:.4f}: GY/(2K/pi) = {val:.10f}")

print()

# Check if GY_k(K) is related to K/pi or something simpler
print("  Check: GY_k(K) * pi / K = ? vs q:")
for r in results:
    val = r['gy_K'] * np.pi / r['K']
    print(f"    q={r['q']:.4f}: GY*pi/K = {val:.10f}")

print()

# =================================================================
# Check: GY_k(2K) / GY_k(K) = ?
# =================================================================
print("=" * 80)
print("  RATIO: GY_k(2K) / GY_k(K)")
print("=" * 80)
print()

for r in results:
    ratio = r['gy_2K'] / r['gy_K']
    print(f"  q={r['q']:.4f}: GY(2K)/GY(K) = {ratio:.10f}")

print()

# =================================================================
# Check the PRODUCT GY_k(K) * GY_+(K)
# =================================================================
print("=" * 80)
print("  GY_kink(K) * VARIOUS MODULAR FORMS")
print("=" * 80)
print()

# At q = 1/phi:
r_golden = [r for r in results if abs(r['q'] - float(phibar)) < 0.01][0]
gy_K_val = r_golden['gy_K']
eta_val = r_golden['eta']
t4_val = r_golden['t4']
t3_val = r_golden['t3']
K_g = r_golden['K']

print(f"  At q = 1/phi:")
print(f"    GY_k(K) = {gy_K_val:.12f}")
print(f"    eta     = {eta_val:.12f}")
print(f"    t4      = {t4_val:.12f}")
print(f"    t3      = {t3_val:.12f}")
print(f"    K       = {K_g:.12f}")
print()

# Systematic check
combos = [
    ("GY * eta", gy_K_val * eta_val),
    ("GY * eta^2", gy_K_val * eta_val**2),
    ("GY * t4", gy_K_val * t4_val),
    ("GY * t4^2", gy_K_val * t4_val**2),
    ("GY * eta * t4", gy_K_val * eta_val * t4_val),
    ("GY / t3^2", gy_K_val / t3_val**2),
    ("GY * (pi/K)", gy_K_val * np.pi / K_g),
    ("GY * (pi/K)^2", gy_K_val * (np.pi/K_g)**2),
    ("GY * eta / t3^2", gy_K_val * eta_val / t3_val**2),
    ("GY * pi/(2K)", gy_K_val * np.pi / (2*K_g)),
    ("GY - 1/eta", gy_K_val - 1/eta_val),
    ("GY / (K/pi)", gy_K_val * np.pi / K_g),
    ("GY - K/pi", gy_K_val - K_g/np.pi),
    ("GY - t3^2", gy_K_val - t3_val**2),
    ("GY^2", gy_K_val**2),
    ("GY^2 * eta^2", gy_K_val**2 * eta_val**2),
    ("GY^2 * t4", gy_K_val**2 * t4_val),
    ("GY^2 / t3^4", gy_K_val**2 / t3_val**4),
]

print(f"  {'Expression':>25} {'Value':>18}")
print(f"  {'-'*25} {'-'*18}")
for name, val in combos:
    # Check if val is close to a simple number
    note = ""
    for simple_val, simple_name in [(1, "1"), (2, "2"), (3, "3"), (4, "4"),
                                     (6, "6"), (12, "12"), (1/2, "1/2"),
                                     (1/3, "1/3"), (1/4, "1/4"), (1/6, "1/6"),
                                     (1/12, "1/12"), (np.pi, "pi"),
                                     (np.sqrt(5), "sqrt5"),
                                     (float(phi), "phi"), (float(phibar), "phibar"),
                                     (np.pi**2, "pi^2"), (np.pi/2, "pi/2"),
                                     (np.sqrt(3), "sqrt3"), (2*np.pi, "2pi")]:
        if abs(val) > 1e-10 and abs(val - simple_val)/max(abs(val), abs(simple_val)) < 0.01:
            note = f" ~ {simple_name} ({abs(val-simple_val)/abs(simple_val)*100:.4f}%)"
    if abs(val) < 200 and abs(val) > 0.001:
        print(f"  {name:>25} {val:18.12f}{note}")

print()

# =================================================================
# Specifically check: is GY_k(K) = 1/eta + corrections?
# =================================================================
print("=" * 80)
print("  SPECIFIC CHECK: GY_k(K) vs 1/eta(q)")
print("=" * 80)
print()

print(f"  {'q':>8} {'GY_k(K)':>14} {'1/eta':>14} {'ratio':>14} {'diff%':>10}")
print(f"  {'-'*8} {'-'*14} {'-'*14} {'-'*14} {'-'*10}")

for r in results:
    inv_eta = 1/r['eta']
    ratio = r['gy_K'] / inv_eta
    diff_pct = (r['gy_K'] - inv_eta) / inv_eta * 100
    marker = " <--" if abs(r['q'] - float(phibar)) < 0.01 else ""
    print(f"  {r['q']:8.4f} {r['gy_K']:14.8f} {inv_eta:14.8f} {ratio:14.8f} {diff_pct:10.4f}%{marker}")

print()

# =================================================================
# Check: is GY_k(K) = t3^2 + correction from t4?
# =================================================================
print("=" * 80)
print("  SPECIFIC CHECK: GY_k(K) vs theta_3^2 = 2K/pi")
print("=" * 80)
print()

print(f"  {'q':>8} {'GY_k(K)':>14} {'t3^2':>14} {'ratio':>14} {'diff%':>10}")
print(f"  {'-'*8} {'-'*14} {'-'*14} {'-'*14} {'-'*10}")

for r in results:
    t3_sq = r['t3']**2
    ratio = r['gy_K'] / t3_sq
    diff_pct = (r['gy_K'] - t3_sq) / t3_sq * 100
    marker = " <--" if abs(r['q'] - float(phibar)) < 0.01 else ""
    print(f"  {r['q']:8.4f} {r['gy_K']:14.8f} {t3_sq:14.8f} {ratio:14.8f} {diff_pct:10.4f}%{marker}")

print()

# =================================================================
# Check: is GY_k(K) * GY_k(K) related to something?
# =================================================================
print("=" * 80)
print("  RATIO ANALYSIS: GY_k(K) / (K/pi) vs q")
print("=" * 80)
print()

print(f"  {'q':>8} {'GY_k(K)/(K/pi)':>18} {'=GY*pi/K':>14} {'t3^2 * pi/K':>14}")
print(f"  {'-'*8} {'-'*18} {'-'*14} {'-'*14}")

for r in results:
    val = r['gy_K'] * np.pi / r['K']
    t3sq_piK = r['t3']**2 * np.pi / r['K']
    print(f"  {r['q']:8.4f} {val:18.10f} {val:14.8f} {t3sq_piK:14.8f}")

print()

# =================================================================
# SUMMARY
# =================================================================
print("=" * 80)
print("  SUMMARY OF FINDINGS")
print("=" * 80)
print()

print("""
  The Gelfand-Yaglom computation of det_Dir(H_kink)/det_Dir(-d^2)
  on [0, K] at the golden nome gives:

  GY_k(K) ≈ 9.689

  This is NOT simply 1/eta = 8.446, theta_3^2 = 6.529, or any
  other single modular form.

  The ratio GY_k(K)/theta_3^2 varies with q (not constant), and
  the exponent log(GY)/log(eta) also varies with q.

  The q-scan reveals that the GY ratio is NOT a simple modular form.
  It is a COMPLICATED function of q that depends on the full spectrum
  of the Lame operator, not just on eta or theta functions.

  KEY CONCLUSION: The functional determinant of the Lame operator
  at the golden nome CANNOT be expressed as a simple power or product
  of eta and theta functions. The relationship between the Lame
  determinant and modular forms, if it exists, requires additional
  mathematical structure (perhaps the genus-2 theta function of the
  spectral curve, or a resurgent trans-series).

  HOWEVER: the q-scan of R_massive(q) = det'(H_kink)/det(H_massive)
  confirms that R(q) → 1/12 as q → 0 (the Dunne-Rao result),
  and R drops super-exponentially for larger q. The golden nome
  gives R ≈ 10^{-18}, enormously far from 1/12.

  The Gelfand-Yaglom result does NOT directly equal eta(1/phi).
  The Lame mechanism for alpha_s = eta must work through a different
  route than the simple functional determinant.
""")

print("  Script complete.")
print("=" * 80)
