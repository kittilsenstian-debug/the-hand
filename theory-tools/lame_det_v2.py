#!/usr/bin/env python3
"""
lame_det_v2.py -- Lame Functional Determinant v2: Correct Approach
===================================================================

The v1 computation revealed that uniform grids cannot resolve the kink
at k~1 (where cn^2(x) ≈ sech^2(x) is extremely peaked). The lowest
eigenvalue came out as ~0.032 instead of ~0 (zero mode).

FIX: Use the Gelfand-Yaglom method (ODE integration) which doesn't
need grid discretization. For the Dirichlet determinant:

  det_Dir(H - E) / det_Dir(H_0 - E) = y_2(L, E) / y_2^free(L, E)

where y_2 is the solution with y_2(0) = 0, y_2'(0) = 1.

Also compute the RELATIVE DETERMINANT:
  log det(H + s) - log det(H_0 + s) = integral_0^s [Tr R(E) - Tr R_0(E)] dE
where R(E) = (H-E)^{-1} is the resolvent.

And the KEY physical quantity from Dunne-Rao:
  det'(M) / det(M_0) = product_{j>0} [lambda_j / lambda_j^{free}]
  For isolated PT kink (n=2): = 1/12

References: Dunne arXiv:0711.1178, Dunne-Rao hep-th/9906113
"""

import sys
import numpy as np

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import mpmath
from mpmath import mp, mpf, pi, sqrt, log, exp, cosh, tanh, sech
from mpmath import ellipk, ellipe

mp.dps = 40

phi = (1 + sqrt(5)) / 2
phibar = 1 / phi
ln_phi = log(phi)

def eta_d(q, N=3000):
    r = q ** (mpf(1)/24)
    for n in range(1, N+1):
        r *= (1 - q**n)
        if abs(q**n) < mpf(10)**(-mp.dps): break
    return r

def theta_f(idx, q, N=3000):
    if idx == 2:
        s = sum(q**(n*(n+1)) for n in range(N))
        return 2 * q**mpf('0.25') * s
    elif idx == 3:
        return 1 + 2*sum(q**(n*n) for n in range(1, N))
    elif idx == 4:
        return 1 + 2*sum((-1)**n * q**(n*n) for n in range(1, N))

q = phibar
eta_v = eta_d(q)
t4 = theta_f(4, q)
t3 = theta_f(3, q)
t2 = theta_f(2, q)
eta_dark = eta_d(q**2)
C_loop = eta_v * t4 / 2

k = t2**2 / t3**2
kp = t4**2 / t3**2
m_par = k**2
K_val = ellipk(m_par)
T_period = 2 * K_val

print("=" * 80)
print("  LAME FUNCTIONAL DETERMINANT v2: GELFAND-YAGLOM APPROACH")
print("=" * 80)
print()
print(f"  q = 1/phi, k = {mpmath.nstr(k, 15)}, K = {mpmath.nstr(K_val, 12)}")
print(f"  eta = {mpmath.nstr(eta_v, 15)}, t4 = {mpmath.nstr(t4, 12)}")
print()

# =================================================================
# THE CORRECT PHYSICAL SETUP
# =================================================================
# The phi^4 kink fluctuation operator in standard normalization:
#   M = -d^2/dx^2 + V''(phi_kink(x))
# where V''(phi_kink) = m^2 - n(n+1)*kappa^2*sech^2(kappa*x)
# with n=2 and in our units kappa = 1:
#   M = -d^2 + m^2 - 6*sech^2(x)
# The PT spectrum: E_0=0 (zero mode), E_1=m^2-1 (breathing), continuum at m^2
# With m^2 = 4 (standard): E_0=0, E_1=3, continuum at 4.
#
# For the LAME (periodic) version: sech^2(x) -> k^2*sn^2(x,k)*(from sign convention)
# Actually: -6*sech^2(x) has eigenvalues -4, -1, 0+p^2 (continuous)
# And sech^2(x) = 1 - tanh^2(x) -> cn^2(x,k) = 1 - sn^2(x,k) as k->1
# So: V_kink = -6*cn^2(x,k) [matches -6*sech^2 as k->1]
# Full operator: M_kink = -d^2 + m^2 - 6*k^2*cn^2(x,k) = -d^2 + 6k^2*sn^2(x,k) + (m^2 - 6k^2)

# Wait: let me be very precise. In Dunne-Rao, the Lame potential is:
# V(x) = n(n+1)*k^2*sn^2(x,k)
# and the fluctuation operator about the periodic instanton is:
# M = -d^2 + n(n+1)*k^2*sn^2(x,k)
# This is the POSITIVE Lame operator (it has the instanton at the TOP of the potential).
#
# The Gelfand-Yaglom formula for the DIRICHLET determinant is:
# det_Dir(M) / det_Dir(-d^2) = y_2(T) / T
# (at E=0, where y_2 is normalized y_2(0)=0, y_2'(0)=1)

# The issue is: for the POSITIVE Lame, E=0 is BELOW the spectrum (all eigs > 0).
# So det_Dir(M) at E=0 is the product of ALL eigenvalues, none removed.
# For the free operator: det_Dir(-d^2) = product of (n*pi/T)^2, also all positive.
# This ratio is well-defined and FINITE.

# For Dirichlet BC on [0, T]: eigenvalues of -d^2 are (n*pi/T)^2, n=1,2,...

# =================================================================
# PART 1: GELFAND-YAGLOM FOR POSITIVE LAME (DIRICHLET)
# =================================================================
print("=" * 80)
print("  PART 1: GELFAND-YAGLOM FOR POSITIVE LAME (DIRICHLET BC)")
print("=" * 80)
print()

def integrate_gy(V_func, T, E_val, nsteps=50000):
    """Integrate y'' = [V(x) - E]*y with y(0)=0, y'(0)=1 over [0, T].
    Returns y(T) = GY numerator for Dirichlet BC.
    V_func(x) returns the potential at x.
    """
    h = T / nsteps

    def rhs(x, state):
        y, yp = state
        return [yp, (V_func(x) - E_val) * y]

    def rk4(f, t, y, h):
        k1 = f(t, y)
        k2 = f(t+h/2, [y[i]+h/2*k1[i] for i in range(2)])
        k3 = f(t+h/2, [y[i]+h/2*k2[i] for i in range(2)])
        k4 = f(t+h,   [y[i]+h*k3[i] for i in range(2)])
        return [y[i]+h/6*(k1[i]+2*k2[i]+2*k3[i]+k4[i]) for i in range(2)]

    state = [mpf(0), mpf(1)]
    x = mpf(0)
    for _ in range(nsteps):
        state = rk4(rhs, x, state, h)
        x += h
    return state[0]  # y(T)

# Positive Lame potential: V(x) = 6*k^2*sn^2(x,k)
def V_pos_lame(x):
    sn = mpmath.ellipfun('sn', x, m=m_par)
    return 6 * m_par * sn**2

# Free potential: V(x) = 0
# Free GY: y_free(T) = T (the solution is y(x) = x)

# Compute GY at E=0 for positive Lame on [0, T = 2K]:
print("  Computing y_2(T) for positive Lame on [0, 2K], E=0...")
y2_pos_T = integrate_gy(V_pos_lame, T_period, mpf(0), nsteps=50000)
GY_pos = y2_pos_T / T_period

print(f"  y_2(T) = {mpmath.nstr(y2_pos_T, 20)}")
print(f"  T = 2K = {mpmath.nstr(T_period, 15)}")
print(f"  GY ratio = y_2(T)/T = {mpmath.nstr(GY_pos, 20)}")
print(f"  = det_Dir(H_+) / det_Dir(-d^2) [at E=0]")
print()

# =================================================================
# PART 2: GY FOR THE KINK OPERATOR (DIRICHLET)
# =================================================================
print("=" * 80)
print("  PART 2: GY FOR KINK OPERATOR -d^2 + 6k^2*cn^2(x,k) [DIRICHLET]")
print("=" * 80)
print()

# Kink operator: V(x) = 6*k^2*cn^2(x,k)
def V_kink_lame(x):
    sn = mpmath.ellipfun('sn', x, m=m_par)
    return 6 * m_par * (1 - sn**2)  # cn^2 = 1 - sn^2

print("  Computing y_2(T) for kink operator on [0, 2K], E=0...")
y2_kink_T = integrate_gy(V_kink_lame, T_period, mpf(0), nsteps=50000)
GY_kink = y2_kink_T / T_period

print(f"  y_2(T) = {mpmath.nstr(y2_kink_T, 20)}")
print(f"  GY ratio = {mpmath.nstr(GY_kink, 20)}")
print()

# =================================================================
# PART 3: GY ON HALF PERIOD (SINGLE KINK)
# =================================================================
print("=" * 80)
print("  PART 3: GY ON HALF PERIOD [0, K] (SINGLE KINK)")
print("=" * 80)
print()

# On [0, K], the kink operator has a single sech^2-like well
print("  Computing y_2(K) for kink operator on [0, K], E=0...")
y2_kink_K = integrate_gy(V_kink_lame, K_val, mpf(0), nsteps=50000)
GY_kink_half = y2_kink_K / K_val

print(f"  y_2(K) = {mpmath.nstr(y2_kink_K, 20)}")
print(f"  K = {mpmath.nstr(K_val, 15)}")
print(f"  GY ratio = y_2(K)/K = {mpmath.nstr(GY_kink_half, 20)}")
print()

# Also for positive Lame on [0, K]:
print("  Computing y_2(K) for positive Lame on [0, K], E=0...")
y2_pos_K = integrate_gy(V_pos_lame, K_val, mpf(0), nsteps=50000)
GY_pos_half = y2_pos_K / K_val

print(f"  y_2(K) [positive] = {mpmath.nstr(y2_pos_K, 20)}")
print(f"  GY ratio [positive] = {mpmath.nstr(GY_pos_half, 20)}")
print()

# =================================================================
# PART 4: GY AT SHIFTED ENERGY (MASSIVE COMPARISON)
# =================================================================
print("=" * 80)
print("  PART 4: GY AT VARIOUS E VALUES (SHIFTED OPERATOR)")
print("=" * 80)
print()

# det_Dir(H - E) / det_Dir(-d^2 - E) = y_2(T, E) / sin(sqrt(E)*T)/sqrt(E)
# At E = -s (shift): det_Dir(H + s) / det_Dir(-d^2 + s)
# The free solution at E=-s: y'' = s*y, y(0)=0, y'(0)=1
# => y(x) = sinh(sqrt(s)*x)/sqrt(s)
# So: det ratio = y_2(T, -s) * sqrt(s) / sinh(sqrt(s)*T)

print("  Dirichlet determinant ratio at shifted E = -s:")
print(f"  det_Dir(H_kink + s) / det_Dir(-d^2 + s)")
print()
print(f"  {'s':>8} {'y_2(T,-s)':>22} {'free sinh/sqrt(s)':>22} {'ratio':>22}")
print(f"  {'-'*8} {'-'*22} {'-'*22} {'-'*22}")

ratios_shifted = {}
for s_val in [mpf('0.1'), mpf('0.5'), mpf(1), mpf(2), mpf(4), mpf(6), mpf(10)]:
    y2_s = integrate_gy(V_kink_lame, T_period, -s_val, nsteps=30000)
    sqrt_s = sqrt(s_val)
    y2_free_s = mpmath.sinh(sqrt_s * T_period) / sqrt_s
    ratio = y2_s / y2_free_s
    ratios_shifted[float(s_val)] = float(ratio)
    print(f"  {mpmath.nstr(s_val, 4):>8} {mpmath.nstr(y2_s, 14):>22} {mpmath.nstr(y2_free_s, 14):>22} {mpmath.nstr(ratio, 14):>22}")

print()

# The PT limit result: det_Dir(M_PT) / det_Dir(-d^2 + 4) on the FULL line
# gives 1/12. On a finite interval, it's different.
# But the RATIO of GY ratios for kink vs free-massive:
# det_Dir(H_kink) / det_Dir(-d^2 + m^2) = y_2_kink(T) / y_2_massive(T)
# At E=0, m^2 = 6k^2:
# y_2_massive(T) = sinh(sqrt(6k^2)*T)/sqrt(6k^2)

m_sq = 6 * m_par
sqrt_m = sqrt(m_sq)
y2_massive_T = mpmath.sinh(sqrt_m * T_period) / sqrt_m

ratio_to_massive = y2_kink_T / y2_massive_T
print(f"  KINK vs MASSIVE comparison at E=0:")
print(f"    y_2_kink(T)    = {mpmath.nstr(y2_kink_T, 18)}")
print(f"    y_2_massive(T) = {mpmath.nstr(y2_massive_T, 18)} [mass = sqrt(6k^2)]")
print(f"    Ratio = {mpmath.nstr(ratio_to_massive, 18)}")
print(f"    (Dunne-Rao isolated kink: 1/12 = {mpmath.nstr(mpf(1)/12, 15)})")
print()

# The Dunne-Rao value 1/12 is for the INFINITE line (isolated kink).
# On a finite period, there's a correction. Let's see how this ratio
# depends on the period by varying q.

# =================================================================
# PART 5: EXHAUSTIVE MODULAR FORM COMPARISON
# =================================================================
print("=" * 80)
print("  PART 5: EXHAUSTIVE MODULAR FORM COMPARISON")
print("=" * 80)
print()

print(f"  KEY GY RESULTS:")
print(f"    Full period Dirichlet, positive Lame: GY_+ = {mpmath.nstr(GY_pos, 15)}")
print(f"    Full period Dirichlet, kink:          GY_k = {mpmath.nstr(GY_kink, 15)}")
print(f"    Half period Dirichlet, kink:          GY_k/2 = {mpmath.nstr(GY_kink_half, 15)}")
print(f"    Half period Dirichlet, positive:      GY_+/2 = {mpmath.nstr(GY_pos_half, 15)}")
print(f"    Kink / massive at E=0:                R_m = {mpmath.nstr(ratio_to_massive, 15)}")
print()

# Now check each against modular forms
targets = [
    ("eta", eta_v),
    ("eta^2", eta_v**2),
    ("eta^3", eta_v**3),
    ("eta^4", eta_v**4),
    ("eta^6", eta_v**6),
    ("eta^12", eta_v**12),
    ("eta^24", eta_v**24),
    ("1/eta", 1/eta_v),
    ("1/eta^2", 1/eta_v**2),
    ("1/eta^4", 1/eta_v**4),
    ("theta_4", t4),
    ("theta_4^2", t4**2),
    ("theta_3", t3),
    ("theta_3^2", t3**2),
    ("eta*t4", eta_v*t4),
    ("eta^2/t4", eta_v**2/t4),
    ("eta_dark", eta_dark),
    ("eta_d/eta", eta_dark/eta_v),
    ("eta/eta_d", eta_v/eta_dark),
    ("t4/(2*eta)", t4/(2*eta_v)),
    ("C=eta*t4/2", C_loop),
    ("sin2tW=eta^2/(2t4)", eta_v**2/(2*t4)),
    ("phi", phi),
    ("phi^2", phi**2),
    ("phibar", phibar),
    ("phibar^2", phibar**2),
    ("SQRT5", sqrt(5)),
    ("3", mpf(3)),
    ("12", mpf(12)),
    ("1/12", mpf(1)/12),
    ("2K/pi", T_period/pi),
    ("(2K/pi)^2", (T_period/pi)**2),
    ("pi/(2K)", pi/T_period),
    ("(pi/(2K))^2", (pi/T_period)**2),
    ("K/pi", K_val/pi),
    ("pi/K", pi/K_val),
]

quantities = [
    ("GY_+ (full)", GY_pos),
    ("GY_k (full)", GY_kink),
    ("GY_k (half)", GY_kink_half),
    ("GY_+ (half)", GY_pos_half),
    ("R_massive", ratio_to_massive),
]

for qname, qval in quantities:
    print(f"  {qname} = {mpmath.nstr(qval, 15)}")
    print(f"  {'target':>20} {'value':>18} {'q/target':>18} {'log(q/t)':>12} {'notes':>10}")
    print(f"  {'-'*20} {'-'*18} {'-'*18} {'-'*12} {'-'*10}")
    for tname, tval in targets:
        if abs(tval) > mpf(10)**(-35):
            r = qval / tval
            lr = log(abs(r))
            note = ""
            if abs(lr) < mpf('0.02'):
                note = "MATCH!"
            elif abs(r - 1) < mpf('0.02'):
                note = "~1"
            elif abs(r - 2) < mpf('0.1'):
                note = "~2"
            elif abs(r - 3) < mpf('0.1'):
                note = "~3"
            elif abs(r - 4) < mpf('0.1'):
                note = "~4"
            elif abs(r + 1) < mpf('0.1'):
                note = "~-1"
            elif abs(r - mpf('0.5')) < mpf('0.05'):
                note = "~1/2"
            # Check simple fractions
            for d in range(1, 13):
                n_int = round(float(r) * d)
                if abs(float(r) - n_int/d) < 0.005 and n_int != 0:
                    note = f"~{n_int}/{d}"
                    break
            if abs(float(r)) < 100 and abs(float(r)) > 0.01:
                print(f"  {tname:>20} {mpmath.nstr(tval, 10):>18} {mpmath.nstr(r, 10):>18} {mpmath.nstr(lr, 8):>12} {note:>10}")
    print()

# =================================================================
# PART 6: THE RATIO R_massive AND ITS q-DEPENDENCE
# =================================================================
print("=" * 80)
print("  PART 6: R_massive AS A FUNCTION OF q")
print("=" * 80)
print()

# Compute R_massive(q) = y_2_kink(2K)/y_2_massive(2K) for several q values.
# This should approach 1/12 as q -> 0 (isolated kink limit).

print(f"  {'q':>10} {'R_massive':>18} {'1/R':>14} {'12*R':>14} {'R/(1/12)':>12}")
print(f"  {'-'*10} {'-'*18} {'-'*14} {'-'*14} {'-'*12}")

def compute_R_at_q(q_val, nsteps=20000):
    """Compute R_massive = y2_kink(2K)/y2_massive(2K) at nome q."""
    t2_q = theta_f(2, mpf(q_val))
    t3_q = theta_f(3, mpf(q_val))
    k_q = t2_q**2 / t3_q**2
    m_q = k_q**2
    K_q = ellipk(m_q)
    T_q = 2*K_q
    m_sq_q = 6*m_q

    def V_k(x):
        sn = mpmath.ellipfun('sn', x, m=m_q)
        return 6 * m_q * (1 - sn**2)

    y2_k = integrate_gy(V_k, T_q, mpf(0), nsteps=nsteps)
    sqrt_m_q = sqrt(m_sq_q)
    y2_m = mpmath.sinh(sqrt_m_q * T_q) / sqrt_m_q
    return y2_k / y2_m

for q_test in [0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, float(phibar), 0.65, 0.7]:
    mp.dps = 30
    try:
        R = compute_R_at_q(q_test, nsteps=15000)
        R_f = float(R)
        inv_R = 1/R_f if R_f != 0 else float('inf')
        print(f"  {q_test:10.4f} {R_f:18.12f} {inv_R:14.6f} {12*R_f:14.10f} {R_f*12:12.8f}")
    except Exception as e:
        print(f"  {q_test:10.4f} ERROR: {e}")

mp.dps = 40
print()

# =================================================================
# PART 7: THE DIRICHLET det RATIO AND ITS RELATION TO ETA
# =================================================================
print("=" * 80)
print("  PART 7: GY RATIOS AS FUNCTION OF q -- TRACKING ETA")
print("=" * 80)
print()

# The Dirichlet det ratio for the POSITIVE Lame:
# GY_+(q) = y_2(2K(q), E=0) / (2K(q))
# As q->0 (isolated sn^2 well), this should approach the PT result.

# For the PT operator -d^2 + 6*sech^2(x) on [0, L] with Dirichlet BC:
# det_Dir / det_Dir_free = y_2(L) / L
# For L -> inf: this diverges (the sech^2 well creates bound states).

print(f"  {'q':>10} {'GY_+(2K)':>18} {'GY_k(2K)':>18} {'GY_+(K)':>18} {'GY_k(K)':>18}")
print(f"  {'-'*10} {'-'*18} {'-'*18} {'-'*18} {'-'*18}")

for q_test in [0.1, 0.2, 0.3, 0.4, 0.5, float(phibar), 0.65, 0.7]:
    mp.dps = 25
    try:
        t2_q = theta_f(2, mpf(q_test))
        t3_q = theta_f(3, mpf(q_test))
        k_q = t2_q**2 / t3_q**2
        m_q = k_q**2
        K_q = ellipk(m_q)
        T_q = 2*K_q

        def V_p(x):
            sn = mpmath.ellipfun('sn', x, m=m_q)
            return 6 * m_q * sn**2
        def V_k(x):
            sn = mpmath.ellipfun('sn', x, m=m_q)
            return 6 * m_q * (1 - sn**2)

        y2_p_T = integrate_gy(V_p, T_q, mpf(0), nsteps=12000)
        y2_k_T = integrate_gy(V_k, T_q, mpf(0), nsteps=12000)
        y2_p_K = integrate_gy(V_p, K_q, mpf(0), nsteps=8000)
        y2_k_K = integrate_gy(V_k, K_q, mpf(0), nsteps=8000)

        gy_p = y2_p_T / T_q
        gy_k = y2_k_T / T_q
        gy_pk = y2_p_K / K_q
        gy_kk = y2_k_K / K_q

        marker = " <-" if abs(q_test - float(phibar)) < 0.01 else ""
        print(f"  {q_test:10.4f} {float(gy_p):18.10f} {float(gy_k):18.10f} {float(gy_pk):18.10f} {float(gy_kk):18.10f}{marker}")
    except Exception as e:
        print(f"  {q_test:10.4f} ERROR: {e}")

mp.dps = 40
print()

# =================================================================
# PART 8: CHECK IF log(GY) IS LINEAR IN log(eta)
# =================================================================
print("=" * 80)
print("  PART 8: CHECK IF GY = eta^alpha FOR SOME alpha")
print("=" * 80)
print()

print(f"  At q = 1/phi:")
print(f"    GY_+ (full) = {float(GY_pos):.12f}")
print(f"    GY_k (full) = {float(GY_kink):.12f}")
print(f"    GY_k (half) = {float(GY_kink_half):.12f}")
print(f"    R_massive   = {float(ratio_to_massive):.15e}")
print()

eta_f = float(eta_v)
print(f"    eta = {eta_f:.12f}")
print(f"    log(eta) = {np.log(eta_f):.12f}")
print()

for name, val in [("GY_+_full", float(GY_pos)),
                  ("GY_k_full", float(GY_kink)),
                  ("GY_k_half", float(GY_kink_half)),
                  ("GY_+_half", float(GY_pos_half))]:
    if val > 0:
        alpha = np.log(val) / np.log(eta_f)
        print(f"    log({name})/log(eta) = {alpha:.10f}")
        print(f"      Nearest integer: {round(alpha)}")
        for d in range(1, 7):
            n = round(alpha * d)
            frac = n/d
            if abs(frac - alpha) < 0.05:
                print(f"      Close to {n}/{d} = {frac:.6f} (error {abs(frac-alpha):.6f})")

print()

# =================================================================
# PART 9: THE PRODUCT GY_+ * GY_k (SUPERSYMMETRIC COMBINATION)
# =================================================================
print("=" * 80)
print("  PART 9: PRODUCTS AND RATIOS OF GY VALUES")
print("=" * 80)
print()

# det(H_+) * det(H_kink) might simplify (supersymmetric pairing)
# because H_+ + H_kink = -2d^2 + 6k^2

product_gy = GY_pos * GY_kink
ratio_gy = GY_pos / GY_kink
sum_gy = GY_pos + GY_kink

print(f"  GY_+ = {mpmath.nstr(GY_pos, 15)}")
print(f"  GY_k = {mpmath.nstr(GY_kink, 15)}")
print(f"  GY_+ * GY_k = {mpmath.nstr(product_gy, 15)}")
print(f"  GY_+ / GY_k = {mpmath.nstr(ratio_gy, 15)}")
print(f"  GY_+ + GY_k = {mpmath.nstr(sum_gy, 15)}")
print()

# Check these against targets
for name, val in [("GY_+*GY_k", product_gy),
                  ("GY_+/GY_k", ratio_gy),
                  ("GY_++GY_k", sum_gy)]:
    print(f"  {name} = {mpmath.nstr(val, 15)}")
    for tname, tval in targets:
        if abs(tval) > mpf(10)**(-35):
            r = val / tval
            if abs(r) > mpf('0.01') and abs(r) < mpf(100):
                note = ""
                for d in range(1, 13):
                    n_int = round(float(r) * d)
                    if n_int != 0 and abs(float(r) - n_int/d) < 0.005:
                        note = f" ~{n_int}/{d}"
                        break
                if abs(float(r)-1) < 0.02:
                    note = " MATCH!"
                if note:
                    print(f"    {name}/{tname} = {mpmath.nstr(r, 10)}{note}")
    print()

# =================================================================
# PART 10: FINAL HONEST ASSESSMENT
# =================================================================
print("=" * 80)
print("  PART 10: FINAL HONEST ASSESSMENT")
print("=" * 80)
print()

print("""
  SUMMARY OF COMPUTATION:
  =======================

  We computed the Gelfand-Yaglom functional determinant ratio
  det_Dir(H)/det_Dir(-d^2) = y_2(T)/T for the Lame equation at the
  golden nome q = 1/phi.

  Two operators were studied:
    H_+ = -d^2 + 6k^2*sn^2(x,k)     [positive Lame]
    H_k = -d^2 + 6k^2*cn^2(x,k)     [kink fluctuation]

  Both on [0, 2K] with Dirichlet boundary conditions.

  The GY ratios are:
""")
print(f"    GY_+ = {mpmath.nstr(GY_pos, 15)}")
print(f"    GY_k = {mpmath.nstr(GY_kink, 15)}")
print()

# Check specific interesting matches
print("  NOTABLE COMPARISONS:")
for tname, tval in targets:
    for qname, qval in quantities:
        if abs(tval) > mpf(10)**(-35):
            r = qval / tval
            if abs(float(r) - round(float(r))) < 0.01 and abs(float(r)) < 200 and abs(float(r)) > 0:
                print(f"    {qname} / {tname} = {mpmath.nstr(r, 12)} ~ {round(float(r))}")
            elif abs(float(r*12) - round(float(r*12))) < 0.05 and abs(float(r*12)) < 200:
                print(f"    {qname} / {tname} = {mpmath.nstr(r, 12)} ~ {round(float(r*12))}/12")

print()
print("  Script complete.")
print("=" * 80)
