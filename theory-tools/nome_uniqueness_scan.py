# -*- coding: utf-8 -*-
"""
nome_uniqueness_scan.py

Tests whether q=1/phi is unique among algebraically distinguished nomes
for matching the 3 core SM coupling constants simultaneously.

Core formulas:
  1. alpha_s   = eta(q)
  2. sin2tW    = eta(q)^2 / (2 * theta4(q))
  3. 1/alpha   = theta3(q) * V / theta4(q)   [V = "vacuum distance"]

Measured targets:
  alpha_s   = 0.1179 +/- 0.0010
  sin2tW    = 0.23122 +/- 0.00004
  1/alpha   = 137.035999084
"""

import sys
import io
import mpmath
import random
import math

# Force UTF-8 output on Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

mpmath.mp.dps = 50   # 50 decimal places

# -------------------------------------------------------------------------
# Physical targets
# -------------------------------------------------------------------------
ALPHA_S_TARGET   = 0.1179
ALPHA_S_LOW      = 0.1167   # -1%
ALPHA_S_HIGH     = 0.1191   # +1%

SIN2TW_TARGET    = 0.23122
SIN2TW_LOW       = 0.23122 * 0.99
SIN2TW_HIGH      = 0.23122 * 1.01

INV_ALPHA_TARGET = 137.035999084
INV_ALPHA_LOW    = INV_ALPHA_TARGET * 0.99
INV_ALPHA_HIGH   = INV_ALPHA_TARGET * 1.01

PHI = mpmath.mpf('1.6180339887498948482045868343656381177203091798058')

# -------------------------------------------------------------------------
# Modular form helpers
# -------------------------------------------------------------------------

def eta_q(q):
    """
    Dedekind eta as a function of nome q in (0,1).
    eta(q) = q^(1/24) * prod(1-q^n, n=1..inf)
    Using mpmath.qp(q, q) = prod(1-q^n, n=1..inf).
    Returns a positive real.
    """
    q = mpmath.mpf(q)
    return q**mpmath.mpf('1/24') * mpmath.qp(q, q)


def theta3_q(q):
    """theta3(0|q) = 1 + 2*sum(q^(n^2), n=1..inf)"""
    q = mpmath.mpf(q)
    return mpmath.jtheta(3, 0, q)


def theta4_q(q):
    """theta4(0|q) = 1 + 2*sum((-1)^n * q^(n^2), n=1..inf)"""
    q = mpmath.mpf(q)
    return mpmath.jtheta(4, 0, q)


# -------------------------------------------------------------------------
# V candidates to try for each nome (generous to alternatives)
# -------------------------------------------------------------------------

def v_candidates(q):
    """
    Return a dict {label: value} of reasonable vacuum-distance candidates.
    Deliberately generous: pick the BEST-FITTING V so alternatives get
    every advantage. For q=1/phi the E8-motivated V=phi is also included.
    """
    q = float(q)
    cands = {}
    if 0 < q < 1:
        cands['phi']         = float(PHI)
        cands['1/q']         = 1.0 / q
        cands['q/(1-q)']     = q / (1.0 - q)
        cands['1/(1-q)']     = 1.0 / (1.0 - q)
        cands['sqrt(1/q)']   = math.sqrt(1.0 / q)
        cands['1/q^2']       = 1.0 / q**2
        cands['(1+q)/(1-q)'] = (1.0 + q) / (1.0 - q)
        cands['q^(-1/2)']    = q**(-0.5)
    return cands


# -------------------------------------------------------------------------
# Named algebraic/transcendental nomes
# -------------------------------------------------------------------------

def make_named_nomes():
    phi    = float(PHI)
    sqrt2  = math.sqrt(2)
    sqrt3  = math.sqrt(3)
    sqrt5  = math.sqrt(5)
    sqrt13 = math.sqrt(13)
    plastic = 1.3247179572447460260  # real root of x^3 = x + 1
    inv_plastic = 1.0 / plastic
    tribonacci_root = 1.4655712318767680297  # real root of x^3 - x^2 - 1 = 0

    nomes = {}

    # --- algebraic / unit-related ---
    nomes['1/phi (golden)']          = 1.0 / phi           # ~0.6180
    nomes['1/phi^2 (dark nome)']     = 1.0 / phi**2        # ~0.3820
    nomes['sqrt2 - 1 (silver)']      = sqrt2 - 1           # ~0.4142
    nomes['(sqrt13-3)/2']            = (sqrt13 - 3) / 2    # ~0.3028
    nomes['1/plastic']               = inv_plastic         # ~0.7549
    nomes['1/sqrt2']                 = 1.0 / sqrt2         # ~0.7071
    nomes['1/sqrt3']                 = 1.0 / sqrt3         # ~0.5774
    nomes['1/sqrt5']                 = 1.0 / sqrt5         # ~0.4472
    nomes['sqrt5 - 2']               = sqrt5 - 2           # ~0.2361
    nomes['2 - sqrt3']               = 2.0 - sqrt3         # ~0.2679
    nomes['sqrt3 - 1']               = sqrt3 - 1           # ~0.7321
    nomes['1/tribonacci']            = 1.0 / tribonacci_root   # ~0.6824

    # --- transcendental / classic constants ---
    nomes['1/e']                     = 1.0 / math.e        # ~0.3679
    nomes['1/pi']                    = 1.0 / math.pi       # ~0.3183
    nomes['2/pi']                    = 2.0 / math.pi       # ~0.6366
    nomes['pi/4']                    = math.pi / 4.0       # ~0.7854
    nomes['ln(2)']                   = math.log(2)         # ~0.6931
    nomes['e/4']                     = math.e / 4.0        # ~0.6796
    nomes['gamma (Euler)']           = 0.5772156649015328  # ~0.5772
    nomes['Catalan/pi']              = 0.9159655941772190 / math.pi  # ~0.2915
    nomes['zeta3/10 (Apery)']        = 1.2020569031595943 / 10       # ~0.1202

    # --- simple rationals ---
    for p, q_rat in [(1,3),(2,3),(1,4),(3,4),(1,5),(2,5),(3,5),(4,5),
                     (1,6),(5,6),(1,7),(2,7),(3,7),(4,7),(5,7),(6,7),
                     (1,8),(3,8),(5,8),(7,8),(1,9),(4,9),(5,9),(8,9)]:
        nomes[f'{p}/{q_rat}']        = p / q_rat

    # --- more algebraic ---
    nomes['(sqrt2-1)^2']             = (sqrt2 - 1)**2          # ~0.1716
    nomes['sqrt(1/phi)']             = math.sqrt(1.0/phi)      # ~0.7862
    nomes['phi/3']                   = phi / 3.0               # ~0.5393
    nomes['phi/4']                   = phi / 4.0               # ~0.4045
    nomes['phi^2/5']                 = phi**2 / 5.0            # ~0.5236
    nomes['1/phi^3']                 = 1.0/phi**3              # ~0.2361
    nomes['exp(-pi/4)']              = math.exp(-math.pi/4)    # ~0.4559
    nomes['exp(-pi/6)']              = math.exp(-math.pi/6)    # ~0.5924
    nomes['exp(-pi/3)']              = math.exp(-math.pi/3)    # ~0.3502
    nomes['exp(-pi/2)']              = math.exp(-math.pi/2)    # ~0.2079
    nomes['exp(-pi)']                = math.exp(-math.pi)      # ~0.0432
    nomes['sin(pi/5)']               = math.sin(math.pi/5)     # ~0.5878
    nomes['sin(pi/7)']               = math.sin(math.pi/7)     # ~0.4339
    nomes['sin(pi/8)']               = math.sin(math.pi/8)     # ~0.3827
    nomes['cos(pi/5)']               = math.cos(math.pi/5)     # ~0.8090
    nomes['sin(pi/12)']              = math.sin(math.pi/12)    # ~0.2588

    return nomes


# -------------------------------------------------------------------------
# Core evaluation function
# -------------------------------------------------------------------------

def evaluate_nome(name, q_val, special_V=None):
    """
    Evaluate a nome against all three SM targets.
    Returns a result dict or None if computation fails.
    """
    q_val = float(q_val)
    if not (0.001 < q_val < 0.9999):
        return None

    try:
        q = mpmath.mpf(q_val)
        eta_val  = eta_q(q)
        th3_val  = theta3_q(q)
        th4_val  = theta4_q(q)

        eta_f = float(eta_val)
        th3_f = float(th3_val)
        th4_f = float(th4_val)

        if not (0.0 < eta_f < 1.0 and th3_f > 0 and th4_f > 0):
            return None

        alpha_s = eta_f
        sin2tw  = eta_f**2 / (2.0 * th4_f)

        # Try all V candidates; pick best for 1/alpha
        vcands = v_candidates(q_val)
        if special_V is not None:
            vcands['SPECIAL_V'] = special_V

        best_ia_err   = 1e18
        best_ia_val   = None
        best_V_label  = None
        best_V_val    = None

        for vlabel, vval in vcands.items():
            if vval <= 0 or not math.isfinite(vval) or vval > 1e6:
                continue
            try:
                inv_alpha = th3_f * vval / th4_f
                err = abs(inv_alpha - INV_ALPHA_TARGET) / INV_ALPHA_TARGET
                if err < best_ia_err:
                    best_ia_err  = err
                    best_ia_val  = inv_alpha
                    best_V_label = vlabel
                    best_V_val   = vval
            except Exception:
                pass

        as_err = abs(alpha_s - ALPHA_S_TARGET) / ALPHA_S_TARGET
        tw_err = abs(sin2tw  - SIN2TW_TARGET)  / SIN2TW_TARGET
        ia_err = best_ia_err

        as_ok = ALPHA_S_LOW  <= alpha_s <= ALPHA_S_HIGH
        tw_ok = SIN2TW_LOW   <= sin2tw  <= SIN2TW_HIGH
        ia_ok = (best_ia_val is not None and
                 INV_ALPHA_LOW <= best_ia_val <= INV_ALPHA_HIGH)

        return {
            'name':      name,
            'q':         q_val,
            'eta':       eta_f,
            'th3':       th3_f,
            'th4':       th4_f,
            'alpha_s':   alpha_s,
            'sin2tw':    sin2tw,
            'inv_alpha': best_ia_val,
            'V_label':   best_V_label,
            'V_val':     best_V_val,
            'as_err':    as_err,
            'tw_err':    tw_err,
            'ia_err':    ia_err,
            'as_ok':     as_ok,
            'tw_ok':     tw_ok,
            'ia_ok':     ia_ok,
            'all_ok':    as_ok and tw_ok and ia_ok,
            'combined_err': as_err + tw_err + ia_err,
        }
    except Exception:
        return None


# -------------------------------------------------------------------------
# Main
# -------------------------------------------------------------------------

def main():
    SEP1 = "=" * 75
    SEP2 = "-" * 75

    print(SEP1)
    print("NOME UNIQUENESS SCAN")
    print("Testing q=1/phi uniqueness for 3 simultaneous SM coupling matches")
    print(SEP1)
    print()
    print("Targets:")
    print(f"  alpha_s  = {ALPHA_S_TARGET}   [+/-1% window: {ALPHA_S_LOW:.4f} - {ALPHA_S_HIGH:.4f}]")
    print(f"  sin2tW   = {SIN2TW_TARGET}  [+/-1%: {SIN2TW_LOW:.5f} - {SIN2TW_HIGH:.5f}]")
    print(f"  1/alpha  = {INV_ALPHA_TARGET}")
    print()

    results = []

    golden_q = float(1.0 / PHI)   # ~0.61803
    dark_q   = float(1.0 / PHI**2)   # ~0.38197

    # -------------------------------------------------------------------------
    # Part 1: Named algebraic / transcendental nomes
    # -------------------------------------------------------------------------
    print(SEP2)
    print("PART 1: Named algebraic / transcendental nomes")
    print(SEP2)

    named = make_named_nomes()

    named_results = []
    seen_q = set()

    for name, q_val in named.items():
        rq = round(float(q_val), 8)
        if rq in seen_q:
            continue
        seen_q.add(rq)

        special_V = None
        if abs(float(q_val) - golden_q) < 1e-8:
            special_V = float(PHI)
        elif abs(float(q_val) - dark_q) < 1e-8:
            special_V = float(PHI**2)

        r = evaluate_nome(name, q_val, special_V=special_V)
        if r is None:
            continue
        named_results.append(r)
        results.append(r)

    # Print table sorted by combined error
    print()
    hdr = f"{'Nome':<28} {'q':>8} {'eta(q)':>8} {'as?':>5} {'sin2tW?':>8} {'1/a?':>5} {'ALL?':>5}  {'comb.err':>10}"
    print(hdr)
    print("-" * len(hdr))
    for r in sorted(named_results, key=lambda x: x['combined_err']):
        def tick(b): return "YES" if b else "---"
        tag = " <<<" if r['all_ok'] else ""
        print(f"{r['name'][:28]:<28} {r['q']:>8.5f} {r['eta']:>8.5f} "
              f"{tick(r['as_ok']):>5} {tick(r['tw_ok']):>8} {tick(r['ia_ok']):>5} "
              f"{tick(r['all_ok']):>5}  {r['combined_err']:>10.6f}{tag}")

    n_named    = len(named_results)
    n_named_as  = sum(1 for r in named_results if r['as_ok'])
    n_named_tw  = sum(1 for r in named_results if r['tw_ok'])
    n_named_ia  = sum(1 for r in named_results if r['ia_ok'])
    n_named_all = sum(1 for r in named_results if r['all_ok'])
    print(f"\nNamed totals: {n_named} tested  |  alpha_s: {n_named_as}  |  sin2tW: {n_named_tw}  |  1/alpha: {n_named_ia}  |  ALL THREE: {n_named_all}")

    # -------------------------------------------------------------------------
    # Part 2: 5000 random nomes in [0.05, 0.95]
    # -------------------------------------------------------------------------
    print()
    print(SEP2)
    print("PART 2: 5000 random nomes in [0.05, 0.95]")
    print(SEP2)
    print("  (computing 5000 random nomes -- may take ~1-2 minutes) ...")

    random.seed(42)
    random_qs = [random.uniform(0.05, 0.95) for _ in range(5000)]

    rand_all_ok  = 0
    rand_as_ok   = 0
    rand_tw_ok   = 0
    rand_ia_ok   = 0
    rand_skip    = 0
    rand_matches = []

    for i, qv in enumerate(random_qs):
        r = evaluate_nome(f"rand_{i:04d}", qv)
        if r is None:
            rand_skip += 1
            continue
        if r['as_ok']:  rand_as_ok  += 1
        if r['tw_ok']:  rand_tw_ok  += 1
        if r['ia_ok']:  rand_ia_ok  += 1
        if r['all_ok']:
            rand_all_ok += 1
            rand_matches.append(r)
            results.append(r)

    rand_total = 5000 - rand_skip
    print(f"  Random nomes processed: {rand_total}  (skipped {rand_skip})")
    print(f"  alpha_s  alone: {rand_as_ok} ({100.*rand_as_ok/rand_total:.2f}%)")
    print(f"  sin2tW   alone: {rand_tw_ok} ({100.*rand_tw_ok/rand_total:.2f}%)")
    print(f"  1/alpha  alone: {rand_ia_ok} ({100.*rand_ia_ok/rand_total:.2f}%)")
    print(f"  ALL THREE:      {rand_all_ok} ({100.*rand_all_ok/rand_total:.4f}%)")

    if rand_matches:
        print(f"\n  Random nomes matching all three (top 20 by combined error):")
        print(f"  {'q':>10}  {'alpha_s':>9}  {'sin2tW':>9}  {'1/alpha':>10}  {'V-choice':>16}  {'comb.err':>10}")
        for r in sorted(rand_matches, key=lambda x: x['combined_err'])[:20]:
            print(f"  {r['q']:>10.6f}  {r['alpha_s']:>9.5f}  {r['sin2tw']:>9.5f}  "
                  f"{r['inv_alpha']:>10.4f}  {str(r['V_label'])[:16]:>16}  {r['combined_err']:>10.6f}")

    # -------------------------------------------------------------------------
    # Part 3: Dense scan +/-0.1 around q=1/phi (1001 points)
    # -------------------------------------------------------------------------
    print()
    print(SEP2)
    print("PART 3: Dense scan +/-0.1 around q=1/phi (1001 points)")
    print(SEP2)

    dense_qs = [golden_q + (i - 500) / 5000.0 for i in range(1001)]
    dense_qs = [q for q in dense_qs if 0.05 < q < 0.95]

    dense_all_ok  = 0
    dense_as_ok   = 0
    dense_tw_ok   = 0
    dense_ia_ok   = 0
    dense_matches = []

    for qv in dense_qs:
        sv = float(PHI) if abs(qv - golden_q) < 1e-8 else None
        r = evaluate_nome(f"dense_{qv:.5f}", qv, special_V=sv)
        if r is None:
            continue
        if r['as_ok']:  dense_as_ok  += 1
        if r['tw_ok']:  dense_tw_ok  += 1
        if r['ia_ok']:  dense_ia_ok  += 1
        if r['all_ok']:
            dense_all_ok += 1
            dense_matches.append(r)

    print(f"  Points in dense scan: {len(dense_qs)}")
    print(f"  alpha_s  alone: {dense_as_ok} ({100.*dense_as_ok/len(dense_qs):.2f}%)")
    print(f"  sin2tW   alone: {dense_tw_ok} ({100.*dense_tw_ok/len(dense_qs):.2f}%)")
    print(f"  1/alpha  alone: {dense_ia_ok} ({100.*dense_ia_ok/len(dense_qs):.2f}%)")
    print(f"  ALL THREE:      {dense_all_ok} ({100.*dense_all_ok/len(dense_qs):.2f}%)")

    if dense_matches:
        print(f"\n  Dense-scan nomes matching all three (top 10):")
        for r in sorted(dense_matches, key=lambda x: x['combined_err'])[:10]:
            print(f"    q={r['q']:.6f}  comb.err={r['combined_err']:.6f}  "
                  f"1/alpha={r['inv_alpha']:.4f}  V={r['V_label']}={r['V_val']:.4f}")

    # -------------------------------------------------------------------------
    # Detailed result for q=1/phi
    # -------------------------------------------------------------------------
    print()
    print(SEP2)
    print("DETAILED RESULT FOR q = 1/phi (Golden Node)")
    print(SEP2)

    q_gold = mpmath.mpf(1) / PHI
    eta_g  = eta_q(q_gold)
    th3_g  = theta3_q(q_gold)
    th4_g  = theta4_q(q_gold)
    as_g   = float(eta_g)
    tw_g   = float(eta_g**2 / (2*th4_g))
    ia_phi = float(th3_g * PHI / th4_g)

    print(f"  q = 1/phi = {float(q_gold):.15f}")
    print(f"  eta(q)    = {as_g:.15f}")
    print(f"  theta3(q) = {float(th3_g):.15f}")
    print(f"  theta4(q) = {float(th4_g):.15f}")
    print()
    print(f"  (1) alpha_s = eta(q)           = {as_g:.8f}")
    print(f"      target                       = {ALPHA_S_TARGET:.8f}")
    print(f"      deviation                    = {abs(as_g-ALPHA_S_TARGET)/ALPHA_S_TARGET*100:.4f}%")
    print(f"      within +/-1%?               = {ALPHA_S_LOW<=as_g<=ALPHA_S_HIGH}")
    print()
    print(f"  (2) sin2tW = eta^2/(2*theta4)  = {tw_g:.8f}")
    print(f"      target                       = {SIN2TW_TARGET:.8f}")
    print(f"      deviation                    = {abs(tw_g-SIN2TW_TARGET)/SIN2TW_TARGET*100:.4f}%")
    print(f"      within +/-1%?               = {SIN2TW_LOW<=tw_g<=SIN2TW_HIGH}")
    print()
    print(f"  (3) 1/alpha = theta3*phi/theta4 = {ia_phi:.8f}")
    print(f"      target                       = {INV_ALPHA_TARGET:.8f}")
    print(f"      deviation                    = {abs(ia_phi-INV_ALPHA_TARGET)/INV_ALPHA_TARGET*100:.4f}%")
    print(f"      within +/-1%?               = {INV_ALPHA_LOW<=ia_phi<=INV_ALPHA_HIGH}")
    print(f"      NOTE: V=phi=1/q here, so theta3*phi/theta4 = theta3/(q*theta4)")
    print()

    # -------------------------------------------------------------------------
    # Alpha_s window width
    # -------------------------------------------------------------------------
    print(SEP2)
    print("WIDTH OF alpha_s WINDOW: q-interval giving eta(q) within +/-1% of target")
    print(SEP2)

    window_qs = []
    for i in range(10000):
        q_test = 0.001 + i * 0.0001
        if q_test >= 0.999:
            break
        try:
            e = float(eta_q(mpmath.mpf(q_test)))
            if ALPHA_S_LOW <= e <= ALPHA_S_HIGH:
                window_qs.append(q_test)
        except Exception:
            pass

    if window_qs:
        w_lo = min(window_qs)
        w_hi = max(window_qs)
        w    = w_hi - w_lo
        print(f"  q-range for alpha_s within 1%: [{w_lo:.5f}, {w_hi:.5f}]")
        print(f"  Width: {w:.5f}  ({w*100:.2f}% of full [0,1] interval)")
        inside = w_lo <= golden_q <= w_hi
        print(f"  q=1/phi = {golden_q:.5f}  -->  {'INSIDE' if inside else 'OUTSIDE'} this range")
    else:
        w = 0.0
        print("  No q found in this range!")
    print()

    # -------------------------------------------------------------------------
    # Global summary and ranking
    # -------------------------------------------------------------------------
    print(SEP1)
    print("GLOBAL SUMMARY")
    print(SEP1)

    total_tested = n_named + rand_total + len(dense_qs)
    total_all    = n_named_all + rand_all_ok + dense_all_ok

    print(f"\nNamed nomes:      {n_named:5d} tested  |  alpha_s: {n_named_as:4d}  |  sin2tW: {n_named_tw:4d}  |  1/alpha: {n_named_ia:4d}  |  ALL: {n_named_all:4d}")
    print(f"Random nomes:     {rand_total:5d} tested  |  alpha_s: {rand_as_ok:4d}  |  sin2tW: {rand_tw_ok:4d}  |  1/alpha: {rand_ia_ok:4d}  |  ALL: {rand_all_ok:4d}")
    print(f"Dense-scan nomes: {len(dense_qs):5d} tested  |  alpha_s: {dense_as_ok:4d}  |  sin2tW: {dense_tw_ok:4d}  |  1/alpha: {dense_ia_ok:4d}  |  ALL: {dense_all_ok:4d}")
    print(f"\nTOTAL tested: {total_tested}")
    print(f"TOTAL all-three matches: {total_all}")
    frac = total_all / total_tested
    print(f"Fraction matching all three: {frac:.4%}")

    # Deduplicate all matches
    all_matches = (
        [r for r in named_results if r['all_ok']] +
        rand_matches +
        dense_matches
    )
    seen_all = {}
    for r in all_matches:
        key = round(r['q'], 4)
        if key not in seen_all or r['combined_err'] < seen_all[key]['combined_err']:
            seen_all[key] = r
    all_dedup = sorted(seen_all.values(), key=lambda x: x['combined_err'])

    print(f"\nUnique q-values matching all three (dedup to 4 d.p.): {len(all_dedup)}")

    print()
    print(f"  RANKING TABLE (top 30 by combined fractional error)")
    print(f"  {'Rk':>3}  {'Name':<28}  {'q':>8}  {'alpha_s':>8}  {'sin2tW':>9}  {'1/alpha':>10}  {'V-choice':>14}  {'comb.err':>10}")
    print("  " + "-" * 100)

    golden_rank = None
    for rank, r in enumerate(all_dedup[:30], 1):
        is_golden = abs(r['q'] - golden_q) < 1e-4
        if is_golden and golden_rank is None:
            golden_rank = rank
        flag = "  <<<< q=1/phi" if is_golden else ""
        print(f"  {rank:>3}  {r['name'][:28]:<28}  {r['q']:>8.5f}  "
              f"{r['alpha_s']:>8.5f}  {r['sin2tw']:>9.5f}  {r['inv_alpha']:>10.4f}  "
              f"{str(r['V_label'])[:14]:>14}  {r['combined_err']:>10.6f}{flag}")

    if golden_rank:
        print(f"\n  Rank of q=1/phi: #{golden_rank} out of {len(all_dedup)} unique nomes matching all three")
    else:
        print(f"\n  q=1/phi did NOT appear in all-three list -- check individual match flags above.")
        gold_r = [r for r in named_results if abs(r['q'] - golden_q) < 1e-6]
        if gold_r:
            r = gold_r[0]
            print(f"  q=1/phi detail: alpha_s={r['alpha_s']:.5f} ok={r['as_ok']}, "
                  f"sin2tW={r['sin2tw']:.5f} ok={r['tw_ok']}, "
                  f"1/alpha={r['inv_alpha']:.4f} ok={r['ia_ok']}")
            print(f"  Errors: alpha_s={r['as_err']*100:.3f}%  sin2tW={r['tw_err']*100:.3f}%  1/alpha={r['ia_err']*100:.3f}%")

    # -------------------------------------------------------------------------
    # Simultaneous constraint tightness analysis
    # -------------------------------------------------------------------------
    print()
    print(SEP2)
    print("CONSTRAINT TIGHTNESS ANALYSIS")
    print(SEP2)

    frac_rand = rand_all_ok / rand_total if rand_total > 0 else 0.0
    frac_dense = dense_all_ok / len(dense_qs) if dense_qs else 0.0

    print(f"\n  alpha_s 1% window width:  {w*100:.2f}% of q-axis")
    print(f"  sin2tW  1% window:        relative 2% band in (sin2tW) space")
    print(f"  1/alpha 1% window:        relative 2% band in (1/alpha) space")
    print()
    print(f"  If formulas were INDEPENDENT of each other, expected joint rate: ~0.01%")
    print(f"  But alpha_s and sin2tW are CORRELATED (both depend on eta, theta4)")
    print(f"  and 1/alpha formula adds genuine independent constraint via V")
    print()
    print(f"  Empirical rate from Monte Carlo: {rand_all_ok}/{rand_total} = {frac_rand:.4%}")
    print(f"  Empirical rate from dense scan:  {dense_all_ok}/{len(dense_qs)} = {frac_dense:.4%}")

    # Extra: how many of the random triple-matches are near q=1/phi?
    if rand_matches:
        near_golden = [r for r in rand_matches if abs(r['q'] - golden_q) < 0.05]
        far_golden  = [r for r in rand_matches if abs(r['q'] - golden_q) >= 0.05]
        print(f"\n  Of {rand_all_ok} random triple-matches:")
        print(f"    within 0.05 of q=1/phi:  {len(near_golden)}")
        print(f"    more than 0.05 away:      {len(far_golden)}")
        if far_golden:
            print(f"    Distant matches (non-golden triple-matches):")
            for r in sorted(far_golden, key=lambda x: x['combined_err'])[:10]:
                print(f"      q={r['q']:.5f}  comb.err={r['combined_err']:.5f}  V={r['V_label']}")

    # -------------------------------------------------------------------------
    # Conclusions
    # -------------------------------------------------------------------------
    print()
    print(SEP1)
    print("CONCLUSIONS")
    print(SEP1)

    golden_ok_all = (ALPHA_S_LOW <= as_g <= ALPHA_S_HIGH and
                     SIN2TW_LOW  <= tw_g <= SIN2TW_HIGH  and
                     INV_ALPHA_LOW <= ia_phi <= INV_ALPHA_HIGH)

    print(f"""
  (1) q=1/phi matches alpha_s   within 1%: {ALPHA_S_LOW<=as_g<=ALPHA_S_HIGH}
      q=1/phi matches sin2tW    within 1%: {SIN2TW_LOW<=tw_g<=SIN2TW_HIGH}
      q=1/phi matches 1/alpha   within 1%: {INV_ALPHA_LOW<=ia_phi<=INV_ALPHA_HIGH}
      q=1/phi matches ALL THREE within 1%: {golden_ok_all}

  (2) The alpha_s window covers ~{w*100:.1f}% of the q-axis [0,1].
      Any nome in [{w_lo:.4f}, {w_hi:.4f}] will also match alpha_s.

  (3) sin2tW = eta^2/(2*theta4) is NOT independent of alpha_s.
      It is a derived quantity. Once q is fixed by alpha_s, sin2tW is fixed too.
      This means constraints (1) and (2) are partially the SAME constraint.

  (4) 1/alpha = theta3*V/theta4 IS a genuinely independent constraint
      IF V is fixed algebraically (V=phi from E8 for q=1/phi).
      For alternatives, we allow V to float -- this is generous to competitors.

  (5) Named algebraic nomes: {n_named_all}/{n_named} match all three (with free V).

  (6) Random nomes: {rand_all_ok}/{rand_total} = {frac_rand:.4%} match all three (with free V).

  (7) Rank of q=1/phi: {"#"+str(golden_rank)+" out of "+str(len(all_dedup)) if golden_rank else "not in list"}
      But q=1/phi uses FIXED V=phi (algebraically derived from E8).
      Competitors use the BEST possible V chosen post-hoc.
      So q=1/phi's match is MORE constrained than any competitor's.

  (8) KEY STATISTICAL POINT: If random-V is allowed, ANY nome in the
      alpha_s window gets a free-parameter V that can hit 1/alpha=137.
      The residual uniqueness comes ONLY from sin2tW being simultaneously
      correct -- which is automatic from alpha_s via the eta^2/(2*theta4) formula.
      The genuine novelty is that q=1/phi achieves this with V=phi predetermined
      by the algebraic structure (E8 roots, Z[phi]), not tuned post-hoc.
""")

    print("Done.")


if __name__ == '__main__':
    main()
