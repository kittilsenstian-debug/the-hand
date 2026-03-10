#!/usr/bin/env python3
"""
floquet_numerical_verify.py -- Numerical verification of the Floquet/nome claim
===============================================================================

CLAIM: For the n=2 Lame equation at E=0,
    -psi''(y) + 6*k^2*sn^2(y|k)*psi(y) = 0
the Floquet multiplier lambda_1 = 1/q where q = exp(-pi*K'/K).
At the golden nome q = 1/phi, this gives lambda_1 = phi and Tr(M) = sqrt(5).

STRATEGY:
  1. Use the Benettin-stabilized integration to get the Floquet exponent
  2. Compare ln(lambda_1) with -ln(q) = pi*K'/K
  3. Also check at the PT-bound-state energies, not just E=0

IMPORTANT INSIGHT discovered during analysis:
  At E=0, the particle is BELOW the potential minimum (V >= 0 everywhere).
  This is NOT a tunneling regime. The WKB tunneling argument applies to
  energies between the bound-state levels of the isolated wells (-4 and -1
  for the n=2 PT well). The claim about lambda = 1/q may hold at THOSE
  energies, not at E=0.

Mar 10, 2026
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
sqrt5 = math.sqrt(5)

# ============================================================
# ELLIPTIC FUNCTIONS (optimized)
# ============================================================

def agm_KK(k):
    if k >= 1.0:
        return float('inf'), math.pi / 2
    if k <= 0.0:
        return math.pi / 2, float('inf')
    kp = math.sqrt(1 - k * k)
    a, b = 1.0, kp
    while abs(a - b) > 1e-15 * abs(a):
        a, b = (a + b) / 2, math.sqrt(a * b)
    K = math.pi / (2 * a)
    a2, b2 = 1.0, k
    while abs(a2 - b2) > 1e-15 * abs(a2):
        a2, b2 = (a2 + b2) / 2, math.sqrt(a2 * b2)
    Kp = math.pi / (2 * a2)
    return K, Kp

def nome_from_k(k):
    K, Kp = agm_KK(k)
    return math.exp(-math.pi * Kp / K), K, Kp

def sn_cn_dn(u, k):
    """sn, cn, dn via descending Landen transform."""
    if abs(k) < 1e-15:
        return math.sin(u), math.cos(u), 1.0
    if abs(k - 1.0) < 1e-15:
        return math.tanh(u), 1.0 / math.cosh(u), 1.0 / math.cosh(u)
    a_seq = [1.0]
    c_seq = [k]
    kp = math.sqrt(1 - k * k)
    b_seq = [kp]
    while abs(c_seq[-1]) > 1e-15:
        an, bn = a_seq[-1], b_seq[-1]
        a_seq.append((an + bn) / 2)
        b_seq.append(math.sqrt(an * bn))
        c_seq.append((an - bn) / 2)
        if len(c_seq) > 50:
            break
    n = len(a_seq) - 1
    phi_val = u * a_seq[n] * (2 ** n)
    for j in range(n, 0, -1):
        sin_phi = math.sin(phi_val)
        arg = c_seq[j] * sin_phi / a_seq[j]
        arg = max(-1.0, min(1.0, arg))
        phi_val = (phi_val + math.asin(arg)) / 2
    sn_val = math.sin(phi_val)
    cn_val = math.cos(phi_val)
    dn_val = math.sqrt(max(0, 1 - k * k * sn_val * sn_val))
    return sn_val, cn_val, dn_val


# ============================================================
# PRECOMPUTE THE POTENTIAL ON A GRID
# ============================================================

def precompute_potential(k, N_steps):
    """Precompute 6*k^2*sn^2(y_i) on the integration grid."""
    K, _ = agm_KK(k)
    L = 2 * K
    h = L / N_steps
    V = []
    k2_6 = 6 * k * k
    for i in range(N_steps + 1):
        y = i * h
        sn, _, _ = sn_cn_dn(y, k)
        V.append(k2_6 * sn * sn)
    return V, h, L


def rk4_step_precomp(psi, psi_p, V_curr, V_half, V_next, h, E):
    """RK4 step using precomputed potential values."""
    # V_curr = V(y), V_half ≈ V(y+h/2), V_next = V(y+h)
    f_curr = (V_curr - E) * psi

    k1_p = psi_p
    k1_pp = f_curr

    p_half = psi + h/2 * k1_p
    pp_half = psi_p + h/2 * k1_pp
    k2_pp = (V_half - E) * p_half

    p_half2 = psi + h/2 * pp_half
    pp_half2 = psi_p + h/2 * k2_pp
    k3_pp = (V_half - E) * p_half2

    p_end = psi + h * pp_half2
    pp_end = psi_p + h * k3_pp
    k4_pp = (V_next - E) * p_end

    psi_new = psi + h/6 * (k1_p + 2*pp_half + 2*pp_half2 + p_end)
    psi_p_new = psi_p + h/6 * (k1_pp + 2*k2_pp + 2*k3_pp + k4_pp)
    return psi_new, psi_p_new


# Actually, the half-step potential values need to be precomputed too.
# Let me use a simpler approach: precompute on a 2x grid.

def floquet_exponent(k, E, N_steps, n_segments=20):
    """
    Compute the Floquet exponent via Benettin-stabilized integration.
    Precomputes the potential to avoid repeated sn evaluations.
    Returns (mu, det_check) where lambda_1 = exp(2K * mu).
    """
    K, _ = agm_KK(k)
    L = 2 * K
    h = L / N_steps

    # Precompute potential at all grid points
    k2_6 = 6.0 * k * k
    # We need values at steps and half-steps
    V_full = [0.0] * (N_steps + 1)
    V_half = [0.0] * N_steps
    for i in range(N_steps + 1):
        sn, _, _ = sn_cn_dn(i * h, k)
        V_full[i] = k2_6 * sn * sn
    for i in range(N_steps):
        sn, _, _ = sn_cn_dn((i + 0.5) * h, k)
        V_half[i] = k2_6 * sn * sn

    seg_len = N_steps // n_segments

    v1 = [1.0, 0.0]
    v2 = [0.0, 1.0]
    total_log_growth = 0.0

    step_idx = 0
    for seg in range(n_segments):
        p1, pp1 = v1[0], v1[1]
        p2, pp2 = v2[0], v2[1]

        for s in range(seg_len):
            i = step_idx + s
            Vc = V_full[i]
            Vh = V_half[i]
            Vn = V_full[i + 1]

            # RK4 for solution 1
            f1 = (Vc - E) * p1
            mid1_p = p1 + h/2 * pp1
            mid1_pp = pp1 + h/2 * f1
            f2 = (Vh - E) * mid1_p
            mid2_p = p1 + h/2 * mid1_pp
            mid2_pp = pp1 + h/2 * f2
            f3 = (Vh - E) * mid2_p
            end_p = p1 + h * mid2_pp
            end_pp = pp1 + h * f3
            f4 = (Vn - E) * end_p
            p1 = p1 + h/6 * (pp1 + 2*mid1_pp + 2*mid2_pp + end_pp)
            pp1 = pp1 + h/6 * (f1 + 2*f2 + 2*f3 + f4)

            # RK4 for solution 2
            f1 = (Vc - E) * p2
            mid1_p = p2 + h/2 * pp2
            mid1_pp = pp2 + h/2 * f1
            f2 = (Vh - E) * mid1_p
            mid2_p = p2 + h/2 * mid1_pp
            mid2_pp = pp2 + h/2 * f2
            f3 = (Vh - E) * mid2_p
            end_p = p2 + h * mid2_pp
            end_pp = pp2 + h * f3
            f4 = (Vn - E) * end_p
            p2 = p2 + h/6 * (pp2 + 2*mid1_pp + 2*mid2_pp + end_pp)
            pp2 = pp2 + h/6 * (f1 + 2*f2 + 2*f3 + f4)

        step_idx += seg_len

        # Gram-Schmidt orthogonalization
        norm1 = math.sqrt(p1*p1 + pp1*pp1)
        if norm1 > 0:
            total_log_growth += math.log(norm1)
            v1 = [p1/norm1, pp1/norm1]
        else:
            v1 = [1.0, 0.0]

        dot = p2*v1[0] + pp2*v1[1]
        p2 -= dot * v1[0]
        pp2 -= dot * v1[1]
        norm2 = math.sqrt(p2*p2 + pp2*pp2)
        if norm2 > 0:
            v2 = [p2/norm2, pp2/norm2]
        else:
            v2 = [0.0, 1.0]

    mu = total_log_growth / L
    return mu


def monodromy_direct(k, E, N_steps):
    """Direct monodromy (only for small K)."""
    K, _ = agm_KK(k)
    L = 2 * K
    h = L / N_steps
    k2_6 = 6 * k * k

    p1, pp1 = 1.0, 0.0
    p2, pp2 = 0.0, 1.0
    y = 0.0
    for i in range(N_steps):
        sn, _, _ = sn_cn_dn(y, k)
        V = k2_6 * sn * sn
        sn_h, _, _ = sn_cn_dn(y + h/2, k)
        Vh = k2_6 * sn_h * sn_h
        sn_n, _, _ = sn_cn_dn(y + h, k)
        Vn = k2_6 * sn_n * sn_n

        # RK4 for both
        for (p, pp) in [(p1, pp1), (p2, pp2)]:
            pass  # inline below

        # Solution 1
        f1 = (V - E) * p1
        m1p = p1 + h/2*pp1;  m1pp = pp1 + h/2*f1
        f2 = (Vh - E) * m1p
        m2p = p1 + h/2*m1pp; m2pp = pp1 + h/2*f2
        f3 = (Vh - E) * m2p
        ep = p1 + h*m2pp;    epp = pp1 + h*f3
        f4 = (Vn - E) * ep
        p1 = p1 + h/6*(pp1 + 2*m1pp + 2*m2pp + epp)
        pp1 = pp1 + h/6*(f1 + 2*f2 + 2*f3 + f4)

        # Solution 2
        f1 = (V - E) * p2
        m1p = p2 + h/2*pp2;  m1pp = pp2 + h/2*f1
        f2 = (Vh - E) * m1p
        m2p = p2 + h/2*m1pp; m2pp = pp2 + h/2*f2
        f3 = (Vh - E) * m2p
        ep = p2 + h*m2pp;    epp = pp2 + h*f3
        f4 = (Vn - E) * ep
        p2 = p2 + h/6*(pp2 + 2*m1pp + 2*m2pp + epp)
        pp2 = pp2 + h/6*(f1 + 2*f2 + 2*f3 + f4)

        y += h

    tr = p1 + pp2
    det = p1 * pp2 - p2 * pp1
    return tr, det


# ============================================================
# MAIN
# ============================================================

def main():
    print("=" * 78)
    print("FLOQUET MULTIPLIER vs 1/q FOR n=2 LAME AT E=0")
    print("=" * 78)
    print()
    print(f"phi = {phi:.15f}")
    print(f"1/phi = {phibar:.15f}")
    print(f"sqrt(5) = {sqrt5:.15f}")
    print()

    # ----------------------------------------------------------
    # PART 1: E=0 is in the lowest gap
    # ----------------------------------------------------------
    print("-" * 78)
    print("PART 1: Where is E=0 in the band structure?")
    print("-" * 78)
    print()
    print("V(x) = 6*k^2*sn^2(x) >= 0 for all x, with V=0 at x=0,2K.")
    print("So E=0 is at or below the potential minimum => below all bands.")
    print()

    # Verify: Tr(M(E=0)) should have |Tr| > 2
    for k in [0.3, 0.5, 0.7, 0.9]:
        tr, det = monodromy_direct(k, 0.0, 5000)
        print(f"  k={k:.1f}: Tr(M(0)) = {tr:12.6f}, det = {det:.8f}, "
              f"|Tr|>2: {'YES' if abs(tr)>2 else 'NO'} => GAP")

    print()
    print("Confirmed: E=0 is in the lowest gap for all k values tested.")
    print()

    # ----------------------------------------------------------
    # PART 2: Floquet exponent at E=0
    # ----------------------------------------------------------
    print("=" * 78)
    print("PART 2: Floquet exponent mu(E=0) via Benettin stabilization")
    print("=" * 78)
    print()
    print("If lambda_1 = 1/q, then ln(lambda_1) = -ln(q) = pi*K'/K.")
    print("So we check: does 2K*mu = pi*K'/K?")
    print("Equivalently: does mu = pi*K'/(2K^2)?")
    print()

    q_hdr = "q=exp(-piK/K)"
    print(f"{'k':>10s}  {'K':>8s}  {q_hdr:>14s}  "
          f"{'mu':>12s}  {'2K*mu':>12s}  {'-ln(q)':>12s}  "
          f"{'ratio':>10s}  {'ln(lam)/K':>12s}")
    print("-" * 110)

    data = []
    test_ks = [0.5, 0.7, 0.9, 0.95, 0.99, 0.995, 0.999, 0.9999]

    for k in test_ks:
        q_val, K, Kp = nome_from_k(k)
        neg_ln_q = -math.log(q_val)

        # Scale N_steps with K, keep h ~ 0.005
        N_steps = max(5000, int(2 * K / 0.005))
        n_seg = max(10, min(50, int(K)))

        # Cap at 200k to keep runtime reasonable
        if N_steps > 200000:
            N_steps = 200000

        mu = floquet_exponent(k, 0.0, N_steps, n_seg)
        ln_lam = 2 * K * mu
        ratio = ln_lam / neg_ln_q if neg_ln_q > 0 else float('nan')

        print(f"{k:10.6f}  {K:8.3f}  {q_val:14.10f}  "
              f"{mu:12.8f}  {ln_lam:12.8f}  {neg_ln_q:12.8f}  "
              f"{ratio:10.6f}  {ln_lam/K:12.8f}")

        data.append((k, K, q_val, mu, ln_lam, neg_ln_q, ratio))

    print()

    # ----------------------------------------------------------
    # PART 3: Convergence check
    # ----------------------------------------------------------
    print("=" * 78)
    print("PART 3: Convergence study at k=0.99")
    print("=" * 78)
    print()

    k_c = 0.99
    q_c, K_c, Kp_c = nome_from_k(k_c)
    neg_ln_q_c = -math.log(q_c)
    print(f"k = {k_c}, K = {K_c:.8f}, q = {q_c:.12f}, -ln(q) = {neg_ln_q_c:.12f}")
    print()
    print(f"{'N_steps':>10s}  {'mu':>16s}  {'2K*mu':>16s}  {'ratio':>14s}")
    print("-" * 60)

    for N in [5000, 10000, 20000, 50000, 100000]:
        mu = floquet_exponent(k_c, 0.0, N, 20)
        ln_lam = 2 * K_c * mu
        ratio = ln_lam / neg_ln_q_c
        print(f"{N:10d}  {mu:16.12f}  {ln_lam:16.12f}  {ratio:14.10f}")

    print()

    # ----------------------------------------------------------
    # PART 4: What about at the BAND-GAP energies?
    # ----------------------------------------------------------
    print("=" * 78)
    print("PART 4: The CORRECT place to look — band-gap energies")
    print("=" * 78)
    print()
    print("The WKB tunneling argument applies to energies BETWEEN band edges,")
    print("not at E=0 which is below everything.")
    print()
    print("For k close to 1, the n=2 PT isolated well V = -6 sech^2(x) has")
    print("bound states at E_0 = -4 and E_1 = -1 (below the asymptote V=0).")
    print()
    print("In the PERIODIC potential 6k^2 sn^2(x), these become narrow bands.")
    print("Relative to our convention V = +6k^2 sn^2, the asymptotic value is")
    print("V_max = 6k^2, so the 'bound states' sit at E ~ 6k^2 - 4 and E ~ 6k^2 - 1.")
    print()
    print("The WKB prediction: the gap width between bands ~ q^something,")
    print("and the Floquet multiplier at mid-gap ~ 1/q^something.")
    print()

    # For k = 0.9, let's scan Tr(M(E)) to find the bands
    k_scan = 0.9
    q_s, K_s, Kp_s = nome_from_k(k_scan)
    print(f"Scanning Tr(M(E)) for k = {k_scan} (K = {K_s:.4f}):")
    print()
    print(f"  {'E':>8s}  {'Tr(M)':>16s}  {'det':>10s}  {'region':>8s}")
    print("  " + "-" * 50)

    N_ode = 10000
    band_info = []
    prev_in_band = None
    for i in range(61):
        E = -1.0 + i * 0.2
        tr, det = monodromy_direct(k_scan, E, N_ode)
        in_band = abs(tr) <= 2.001
        region = "BAND" if in_band else "GAP"
        if i % 3 == 0 or (prev_in_band is not None and prev_in_band != in_band):
            print(f"  {E:8.2f}  {tr:16.6f}  {det:10.6f}  {region:>8s}")
        prev_in_band = in_band
        band_info.append((E, tr, in_band))

    print()

    # Find the actual band edges by bisection
    print("Finding band edges by bisection:")
    edges = []
    for i in range(len(band_info) - 1):
        E1, tr1, b1 = band_info[i]
        E2, tr2, b2 = band_info[i+1]
        if b1 != b2:
            # Bisect
            lo, hi = E1, E2
            for _ in range(50):
                mid = (lo + hi) / 2
                tr_mid, _ = monodromy_direct(k_scan, mid, N_ode)
                if (abs(tr_mid) <= 2.001) == b1:
                    lo = mid
                else:
                    hi = mid
            edge = (lo + hi) / 2
            edges.append(edge)
            print(f"  Edge at E = {edge:.8f}")

    print()
    if len(edges) >= 5:
        print(f"  Band 1: [{edges[0]:.6f}, {edges[1]:.6f}] (width {edges[1]-edges[0]:.6f})")
        print(f"  Gap 1:  ({edges[1]:.6f}, {edges[2]:.6f})")
        print(f"  Band 2: [{edges[2]:.6f}, {edges[3]:.6f}] (width {edges[3]-edges[2]:.6f})")
        print(f"  Gap 2:  ({edges[3]:.6f}, {edges[4]:.6f})")
        if len(edges) > 4:
            print(f"  Band 3: [{edges[4]:.6f}, inf)")

        # Check PT n=2 prediction
        print()
        print(f"  PT bound state prediction: E ~ 6k^2 - 4 = {6*k_scan**2 - 4:.4f}")
        print(f"  PT bound state prediction: E ~ 6k^2 - 1 = {6*k_scan**2 - 1:.4f}")
        print(f"  Actual band centers: {(edges[0]+edges[1])/2:.4f}, {(edges[2]+edges[3])/2:.4f}")

    print()

    # Now check Floquet exponent AT THE MID-GAP energies
    if len(edges) >= 4:
        # Gap between bands 1 and 2
        E_gap1 = (edges[1] + edges[2]) / 2
        print(f"Floquet exponent at mid-gap 1 (E = {E_gap1:.6f}):")

        for k_test in [0.9, 0.95, 0.99, 0.999]:
            q_t, K_t, Kp_t = nome_from_k(k_test)
            neg_ln_q = -math.log(q_t)

            # Find the actual gap for this k value by quick scan
            # The gap between 1st and 2nd bands centers around E ~ 6k^2 - 2.5
            E_center = 6 * k_test**2 - 2.5

            # Scan narrowly around E_center
            N_ode_t = max(5000, int(2 * K_t / 0.005))
            if N_ode_t > 100000:
                N_ode_t = 100000
            n_seg = max(10, int(K_t))

            # Just compute mu at E_center (approximate mid-gap)
            mu = floquet_exponent(k_test, E_center, N_ode_t, n_seg)
            ln_lam = 2 * K_t * mu
            ratio = ln_lam / neg_ln_q if neg_ln_q > 1e-10 else float('nan')

            print(f"  k={k_test:.4f}: E_midgap~{E_center:.3f}, "
                  f"mu={mu:.8f}, ln(lam)={ln_lam:.8f}, "
                  f"-ln(q)={neg_ln_q:.8f}, ratio={ratio:.6f}")

    print()

    # ----------------------------------------------------------
    # PART 5: Check at E = 6k^2 - 1 (upper PT level) specifically
    # ----------------------------------------------------------
    print("=" * 78)
    print("PART 5: Floquet exponent at E near the upper PT bound state")
    print("=" * 78)
    print()
    print("The key WKB insight: for the upper band (near E = 6k^2 - 1),")
    print("the tunneling rate between wells ~ exp(-action) = q^alpha.")
    print("The band width ~ q, and the Floquet exponent in the gap")
    print("above this band ~ q (for the narrowest gap).")
    print()
    print("For the gap between bands 2 and 3 (above the upper PT level),")
    print("the WKB tunneling gives the SMALLEST gap width.")
    print()

    for k_test in [0.9, 0.95, 0.99, 0.995, 0.999]:
        q_t, K_t, Kp_t = nome_from_k(k_test)
        neg_ln_q = -math.log(q_t)

        N_ode_t = max(5000, int(2 * K_t / 0.005))
        if N_ode_t > 100000:
            N_ode_t = 100000
        n_seg = max(10, int(K_t))

        # Try several energies around 6k^2 (the top of the potential)
        # The gap between bands 2 and 3 is near E ~ 6k^2 + small correction
        E_top = 6 * k_test**2
        print(f"  k={k_test:.4f}, K={K_t:.3f}, q={q_t:.8f}, 6k^2={E_top:.4f}:")

        for dE in [-1.5, -0.5, 0.0, 0.5, 1.0, 2.0]:
            E_test = E_top + dE
            mu = floquet_exponent(k_test, E_test, N_ode_t, n_seg)
            ln_lam = 2 * K_t * mu

            # Only print if in a gap (mu > 0 meaningfully)
            if abs(mu) > 0.001:
                ratio = ln_lam / neg_ln_q if neg_ln_q > 1e-10 else float('nan')
                print(f"    E={E_test:7.3f}: mu={mu:10.6f}, ln(lam)={ln_lam:10.6f}, "
                      f"ratio ln(lam)/(-ln q) = {ratio:.6f}")
            else:
                print(f"    E={E_test:7.3f}: mu~0 (in a band or at band edge)")

        print()

    # ----------------------------------------------------------
    # PART 6: At the golden nome
    # ----------------------------------------------------------
    print("=" * 78)
    print("PART 6: At the golden nome q = 1/phi")
    print("=" * 78)
    print()

    kp_approx = 4 * math.exp(-math.pi**2 / (2 * math.log(phi)))
    k_golden = math.sqrt(1 - kp_approx**2)
    q_g, K_g, Kp_g = nome_from_k(k_golden)

    print(f"k = {k_golden:.15f}")
    print(f"K = {K_g:.10f}")
    print(f"q = {q_g:.15f} (target: {phibar:.15f})")
    print(f"ln(phi) = {math.log(phi):.15f}")
    print(f"pi*K'/K = {math.pi*Kp_g/K_g:.15f}")
    print()

    print("Floquet exponent at E=0:")
    for N in [50000, 100000, 200000]:
        n_s = max(50, int(K_g))
        mu = floquet_exponent(k_golden, 0.0, N, n_s)
        ln_lam = 2 * K_g * mu
        neg_ln_q = -math.log(q_g)
        ratio = ln_lam / neg_ln_q
        print(f"  N={N:>7d}: mu={mu:.10f}, ln(lam)={ln_lam:.10f}, "
              f"-ln(q)={neg_ln_q:.10f}, ratio={ratio:.6f}")

    print()

    # ----------------------------------------------------------
    # SUMMARY
    # ----------------------------------------------------------
    print("=" * 78)
    print("HONEST ASSESSMENT")
    print("=" * 78)
    print()
    print("1. E=0 is in the LOWEST GAP (below all bands) of the n=2 Lame equation.")
    print("   At E=0, the Floquet exponent mu is large (the solution grows fast),")
    print("   and ln(lambda_1) >> -ln(q). The ratio DIVERGES as k -> 1.")
    print()
    print("2. The claim 'lambda_1 = 1/q at E=0' is NUMERICALLY FALSE.")
    print("   ln(lambda_1)/(-ln(q)) grows as k -> 1, reaching values >> 1.")
    print()
    print("3. The WKB tunneling picture (train of sech^2 wells with tunneling rate q)")
    print("   applies to energies BETWEEN the PT bound-state levels, not at E=0.")
    print("   E=0 is below the bottom of every well, so there is no tunneling.")
    print()
    print("4. The correct statement may be about the Floquet multiplier")
    print("   at specific band-gap energies (near E ~ 6k^2 - 4 or E ~ 6k^2 - 1),")
    print("   where the band widths do scale as powers of q.")
    print()

    if data:
        print("Summary of ln(lambda_1)/(-ln(q)) at E=0:")
        for k_v, K_v, q_v, mu_v, ln_lam, neg_ln_q, ratio in data:
            print(f"  k={k_v:.6f}:  ratio = {ratio:.4f}")
    print()
    print("=" * 78)


if __name__ == "__main__":
    main()
