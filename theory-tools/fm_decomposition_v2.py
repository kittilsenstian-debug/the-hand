#!/usr/bin/env python3
"""
FM ALGEBRAIC DECOMPOSITION v2 — WITH NULL MODEL
=================================================
Addresses three critiques:
1. Proper null/control comparison (Monte Carlo, 10,000 trials)
2. Separates structural counts from physical measurements (Svedberg etc.)
3. Honest about what's shown (correlation) vs what's claimed (identity)

Every count tagged as:
  "count"       — discrete count of objects (proteins, subunits, genes)
  "measurement" — continuous physical quantity (Svedberg, nm, degrees)
  "derived"     — computed from other counts (jumps, totals)

Reports results THREE ways:
  ALL        — everything included
  COUNTS     — structural counts only (no measurements)
  LARGE      — counts > 12 only (small numbers match trivially)

The null model: for each biological value, generate random integer in
[max(1, v//2), v*2]. Same magnitude distribution, different specific values.
10,000 trials. Compare observed match rate to null distribution.
"""

import json, math, sys, io, random
from collections import OrderedDict

random.seed(42)  # reproducible

# ═══════════════════════════════════════════════════════════════════
# ALGEBRAIC VOCABULARY (same as v1)
# ═══════════════════════════════════════════════════════════════════

def build_vocabulary():
    V = {}
    def add(n, source, level):
        if n not in V: V[n] = []
        V[n].append({"source": source, "level": level})

    # Level 0: Axiom
    add(1, "unity", 0); add(2, "Z₂ (domain wall)", 0)
    # Level 1: E₈
    add(248, "dim(E₈)", 1); add(240, "roots(E₈)", 1)
    add(8, "rank(E₈)", 1); add(30, "h(E₈)", 1)
    add(120, "|S₅| = 240/2", 1); add(80, "240/3", 1)
    add(60, "240/4 = |A₅|", 1); add(48, "240/5", 1); add(40, "240/6", 1)
    # Level 2: E₇
    add(133, "dim(E₇)", 2); add(126, "roots(E₇)", 2)
    add(56, "fund(E₇)", 2); add(7, "rank(E₇)", 2); add(18, "h(E₇)", 2)
    # Level 3: E₆
    add(78, "dim(E₆)", 3); add(72, "roots(E₆)", 3)
    add(27, "fund(E₆)", 3); add(6, "rank(E₆)=|S₃|", 3); add(12, "h(E₆)", 3)
    # Level 4: D₅
    add(45, "dim(D₅)", 4); add(16, "spinor(D₅)", 4)
    add(10, "vector(D₅)", 4); add(5, "rank(D₅)", 4)
    add(28, "dim(so(8))=T(7)", 4); add(14, "dim(G₂)", 4); add(36, "dim(so(9))", 4)
    # Level 5: A₄
    add(24, "dim(A₄)", 5); add(20, "roots(A₄)=icosahedron", 5)
    add(4, "rank(A₄)", 5); add(15, "dim(A₃)", 5)
    add(21, "dim(sp(6))", 5); add(35, "dim(so(7))", 5)
    # Level 6: SM
    add(3, "triality", 6); add(8, "dim(su(3))", 6)
    # Level 7: Sporadic/Pariah
    add(26, "sporadic count", 7); add(28, "dim(2.Ru)", 7)
    add(37, "pariah J₁", 7); add(43, "pariah J₄", 7)
    add(67, "pariah", 7); add(71, "pariah Ly", 7)
    add(744, "j-invariant", 0)
    return V


# ═══════════════════════════════════════════════════════════════════
# MATCHING ENGINE (tightened: exact and product only for large)
# ═══════════════════════════════════════════════════════════════════

def match_count(n, vocab):
    """Match n against vocabulary. Returns (type, explanation)."""
    primary = set(vocab.keys())
    if n == 0: return ("TRIVIAL", "zero")
    if n in primary:
        best = max(vocab[n], key=lambda s: s["level"])
        return ("EXACT", best["source"])
    # Root quotient: 240/n is integer and that divisor is algebraic
    if n > 0 and 240 % n == 0:
        k = 240 // n
        if k > 1 and k in primary:
            return ("ROOT_QUOTIENT", f"240/{k}")
    # Product: n = a × b, both algebraic, both > 1
    for a in sorted(primary):
        if a < 2: continue
        if a * a > n: break
        if n % a == 0:
            b = n // a
            if b in primary and b >= a:
                sa = vocab[a][0]["source"]
                sb = vocab[b][0]["source"]
                return ("PRODUCT", f"{a} × {b}")
    # Decomposition: n = a + b, both algebraic, both > 0
    for a in sorted(primary):
        if a >= n: break
        b = n - a
        if b in primary and b >= a:
            return ("DECOMPOSITION", f"{a} + {b}")
    return ("MISS", "")


def is_hit(match_type):
    """Is this a 'strong' match? (exact or root quotient)"""
    return match_type in ("EXACT", "ROOT_QUOTIENT")


def is_any_match(match_type):
    """Any non-miss match?"""
    return match_type not in ("MISS", "TRIVIAL")


# ═══════════════════════════════════════════════════════════════════
# BIOLOGICAL SYSTEMS — every count tagged
# ═══════════════════════════════════════════════════════════════════

def build_systems():
    return [
        {
            "name": "Icosahedral Virus Capsids",
            "source": "Caspar & Klug 1962",
            "counts": [
                # T=1
                {"name": "T=1 subunits", "value": 60, "ctype": "count"},
                {"name": "T=1 pentamers", "value": 12, "ctype": "count"},
                # T=3
                {"name": "T=3 subunits", "value": 180, "ctype": "count"},
                {"name": "T=3 pentamers", "value": 12, "ctype": "count"},
                {"name": "T=3 hexamers", "value": 20, "ctype": "count"},
                # T=4
                {"name": "T=4 subunits", "value": 240, "ctype": "count"},
                {"name": "T=4 pentamers", "value": 12, "ctype": "count"},
                {"name": "T=4 hexamers", "value": 30, "ctype": "count"},
                # T=7
                {"name": "T=7 subunits", "value": 420, "ctype": "count"},
                {"name": "T=7 pentamers", "value": 12, "ctype": "count"},
                {"name": "T=7 hexamers", "value": 60, "ctype": "count"},
                {"name": "T=7 capsomeres", "value": 72, "ctype": "count"},
                # T=13
                {"name": "T=13 subunits", "value": 780, "ctype": "count"},
                {"name": "T=13 hexamers", "value": 120, "ctype": "count"},
                # Icosahedron geometry
                {"name": "Icosahedron vertices", "value": 12, "ctype": "count"},
                {"name": "Icosahedron faces", "value": 20, "ctype": "count"},
                {"name": "Icosahedron edges", "value": 30, "ctype": "count"},
            ]
        },
        {
            "name": "PhiX174 Bacteriophage",
            "source": "McKenna 1992; Sanger 1977",
            "counts": [
                {"name": "gpF coat copies", "value": 60, "ctype": "count"},
                {"name": "gpG spike copies", "value": 60, "ctype": "count"},
                {"name": "Pentameric spikes", "value": 12, "ctype": "count"},
                {"name": "gpJ copies", "value": 60, "ctype": "count"},
                {"name": "gpH pilot copies", "value": 12, "ctype": "count"},
                {"name": "Structural protein types", "value": 4, "ctype": "count"},
                {"name": "Genes", "value": 11, "ctype": "count"},
                {"name": "Genome size (nt)", "value": 5386, "ctype": "measurement"},
            ]
        },
        {
            "name": "Ribosome (Euk + Prok comparison)",
            "source": "Anger 2013; Ban 2000; Wilson 2012",
            "counts": [
                # Svedberg coefficients — TAGGED AS MEASUREMENT
                {"name": "Euk ribosome (Svedberg)", "value": 80, "ctype": "measurement"},
                {"name": "Euk small (Svedberg)", "value": 40, "ctype": "measurement"},
                {"name": "Euk large (Svedberg)", "value": 60, "ctype": "measurement"},
                {"name": "Prok ribosome (Svedberg)", "value": 70, "ctype": "measurement"},
                {"name": "Prok small (Svedberg)", "value": 30, "ctype": "measurement"},
                {"name": "Prok large (Svedberg)", "value": 50, "ctype": "measurement"},
                {"name": "Mito small (Svedberg)", "value": 28, "ctype": "measurement"},
                # PROTEIN COUNTS — the real structural data
                {"name": "Human 40S proteins", "value": 33, "ctype": "count"},
                {"name": "Human 60S proteins", "value": 47, "ctype": "count"},
                {"name": "Human total proteins", "value": 80, "ctype": "count"},
                {"name": "E.coli 30S proteins", "value": 21, "ctype": "count"},
                {"name": "E.coli 50S proteins", "value": 33, "ctype": "count"},
                {"name": "E.coli total proteins", "value": 54, "ctype": "count"},
                # EVOLUTIONARY JUMPS — derived
                {"name": "Prok→Euk small jump", "value": 12, "ctype": "derived"},
                {"name": "Prok→Euk large jump", "value": 14, "ctype": "derived"},
                {"name": "Prok→Euk total jump", "value": 26, "ctype": "derived"},
                # Other structural
                {"name": "rRNA molecules", "value": 4, "ctype": "count"},
                {"name": "5S rRNA length (nt)", "value": 120, "ctype": "count"},
                {"name": "Amino acids", "value": 20, "ctype": "count"},
                {"name": "tRNA binding sites", "value": 3, "ctype": "count"},
            ]
        },
        {
            "name": "20S Proteasome Core",
            "source": "Groll 1997",
            "counts": [
                {"name": "Total subunits", "value": 28, "ctype": "count"},
                {"name": "Heptameric rings", "value": 4, "ctype": "count"},
                {"name": "Subunits per ring", "value": 7, "ctype": "count"},
                {"name": "Unique protein types", "value": 14, "ctype": "count"},
                {"name": "Catalytic per beta-ring", "value": 3, "ctype": "count"},
                {"name": "Total catalytic sites", "value": 6, "ctype": "count"},
                {"name": "19S cap subunits", "value": 19, "ctype": "count"},
                {"name": "26S (Svedberg)", "value": 26, "ctype": "measurement"},
            ]
        },
        {
            "name": "Nucleosome",
            "source": "Luger 1997",
            "counts": [
                {"name": "Histone octamer", "value": 8, "ctype": "count"},
                {"name": "Histone types", "value": 4, "ctype": "count"},
                {"name": "Copies each type", "value": 2, "ctype": "count"},
                {"name": "DNA wrapped (bp)", "value": 147, "ctype": "count"},
            ]
        },
        {
            "name": "ATP Synthase F₁",
            "source": "Abrahams 1994; Zhou 2015",
            "counts": [
                {"name": "alpha subunits", "value": 3, "ctype": "count"},
                {"name": "beta subunits", "value": 3, "ctype": "count"},
                {"name": "Catalytic sites", "value": 3, "ctype": "count"},
                {"name": "Rotation per step (deg)", "value": 120, "ctype": "measurement"},
                {"name": "c-ring subunits (human)", "value": 8, "ctype": "count"},
                {"name": "Central stalk subunits", "value": 3, "ctype": "count"},
            ]
        },
        {
            "name": "Collagen Type I",
            "source": "Orgel 2006",
            "counts": [
                {"name": "Chains (triple helix)", "value": 3, "ctype": "count"},
                {"name": "D-period (nm)", "value": 67, "ctype": "measurement"},
                {"name": "Tropocollagen per microfibril", "value": 5, "ctype": "count"},
            ]
        },
        {
            "name": "IgG Antibody",
            "source": "Harris 1992",
            "counts": [
                {"name": "Ig domains", "value": 12, "ctype": "count"},
                {"name": "Polypeptide chains", "value": 4, "ctype": "count"},
                {"name": "Fab arms", "value": 2, "ctype": "count"},
                {"name": "Heavy chain domains", "value": 4, "ctype": "count"},
                {"name": "Light chain domains", "value": 2, "ctype": "count"},
            ]
        },
    ]


# ═══════════════════════════════════════════════════════════════════
# NULL MODEL — Monte Carlo
# ═══════════════════════════════════════════════════════════════════

def run_null_model(values, vocab, n_trials=10000):
    """Generate random integers with same magnitude distribution.
    For each value v, random from [max(1, v//2), v*2].
    Returns distribution of match counts."""
    results = {"exact": [], "any": [], "large_exact": []}

    for _ in range(n_trials):
        exact_count = 0
        any_count = 0
        large_exact = 0

        for v in values:
            lo = max(1, v // 2)
            hi = max(lo + 1, v * 2)
            r = random.randint(lo, hi)
            mt, _ = match_count(r, vocab)
            if is_hit(mt):
                exact_count += 1
                if r > 12:
                    large_exact += 1
            if is_any_match(mt):
                any_count += 1

        results["exact"].append(exact_count)
        results["any"].append(any_count)
        results["large_exact"].append(large_exact)

    return results


def null_stats(observed, distribution):
    """Compute mean, std, p-value from null distribution."""
    n = len(distribution)
    mean = sum(distribution) / n
    var = sum((x - mean)**2 for x in distribution) / n
    std = math.sqrt(var) if var > 0 else 0.001
    z = (observed - mean) / std if std > 0 else 0
    p_above = sum(1 for x in distribution if x >= observed) / n
    return mean, std, z, p_above


# ═══════════════════════════════════════════════════════════════════
# ANALYSIS
# ═══════════════════════════════════════════════════════════════════

def analyze(systems, vocab, filter_ctype=None):
    """Analyze all systems. If filter_ctype given, only include those types."""
    all_values = []
    total = {"exact": 0, "root_q": 0, "product": 0, "decomp": 0, "miss": 0, "trivial": 0}
    large = {"exact": 0, "total": 0}
    system_results = []

    for system in systems:
        counts = system["counts"]
        if filter_ctype:
            counts = [c for c in counts if c["ctype"] in filter_ctype]

        sys_exact = 0
        sys_total = 0
        sys_results = []

        for c in counts:
            v = c["value"]
            if v == 0:
                total["trivial"] += 1
                continue
            all_values.append(v)
            mt, expl = match_count(v, vocab)
            sys_results.append({"name": c["name"], "value": v, "ctype": c["ctype"],
                                "match": mt, "expl": expl})
            sys_total += 1

            if mt == "EXACT": total["exact"] += 1
            elif mt == "ROOT_QUOTIENT": total["root_q"] += 1
            elif mt == "PRODUCT": total["product"] += 1
            elif mt == "DECOMPOSITION": total["decomp"] += 1
            elif mt == "MISS": total["miss"] += 1

            if is_hit(mt): sys_exact += 1
            if v > 12:
                large["total"] += 1
                if is_hit(mt): large["exact"] += 1

        system_results.append({
            "name": system["name"],
            "results": sys_results,
            "exact": sys_exact,
            "total": sys_total,
        })

    return all_values, total, large, system_results


# ═══════════════════════════════════════════════════════════════════
# REPORT
# ═══════════════════════════════════════════════════════════════════

def print_analysis(label, systems, vocab, filter_ctype=None, run_null=True):
    """Run and print complete analysis with optional null model."""

    G = "\033[92m"; B = "\033[94m"; Y = "\033[93m"; R = "\033[91m"
    M = "\033[95m"; C = "\033[96m"; D = "\033[90m"; X = "\033[0m"

    values, total, large, sys_results = analyze(systems, vocab, filter_ctype)

    n = total["exact"] + total["root_q"] + total["product"] + total["decomp"] + total["miss"]
    exact = total["exact"] + total["root_q"]

    print(f"\n{'='*72}")
    print(f"  {label}")
    print(f"{'='*72}")

    # Per-system
    for sr in sys_results:
        pct = (sr["exact"]/sr["total"]*100) if sr["total"] > 0 else 0
        print(f"\n  {sr['name']}: {sr['exact']}/{sr['total']} exact ({pct:.0f}%)")
        for r in sr["results"]:
            sym = {
                "EXACT": f"{G}■ EXACT{X}",
                "ROOT_QUOTIENT": f"{C}◆ ROOT_Q{X}",
                "PRODUCT": f"{M}▲ PROD{X}",
                "DECOMPOSITION": f"{B}● DECOMP{X}",
                "MISS": f"{R}✗ MISS{X}",
            }.get(r["match"], f"{D}?{X}")
            tag = f"[{r['ctype'][:5]}]" if filter_ctype is None else ""
            print(f"    {r['name']:<40} {r['value']:>6}  {sym:<30} {r['expl']}")

    # Summary
    print(f"\n  {'─'*68}")
    print(f"  Total counts:     {n}")
    print(f"  Exact algebraic:  {exact} ({exact/n*100:.1f}%)")
    print(f"  Product:          {total['product']}")
    print(f"  Decomposition:    {total['decomp']}")
    print(f"  {R}Miss:             {total['miss']}{X}")
    print(f"\n  Large (>12):      {large['exact']}/{large['total']} exact")

    # Null model
    if run_null and values:
        print(f"\n  {'─'*68}")
        print(f"  NULL MODEL (10,000 random trials, same magnitude distribution)")
        null = run_null_model(values, vocab, 10000)

        # Exact matches
        obs_exact = exact
        mean_e, std_e, z_e, p_e = null_stats(obs_exact, null["exact"])
        print(f"\n    Exact matches:  observed={obs_exact}  null={mean_e:.1f}±{std_e:.1f}  z={z_e:.1f}  p={p_e:.4f}")

        # Any match
        obs_any = exact + total["product"] + total["decomp"]
        mean_a, std_a, z_a, p_a = null_stats(obs_any, null["any"])
        print(f"    Any match:      observed={obs_any}  null={mean_a:.1f}±{std_a:.1f}  z={z_a:.1f}  p={p_a:.4f}")

        # Large exact
        obs_le = large["exact"]
        mean_l, std_l, z_l, p_l = null_stats(obs_le, null["large_exact"])
        print(f"    Large exact:    observed={obs_le}  null={mean_l:.1f}±{std_l:.1f}  z={z_l:.1f}  p={p_l:.4f}")

        if p_l < 0.001:
            print(f"\n    {G}★ Large exact matches: p < 0.001 — signal is real{X}")
        elif p_l < 0.05:
            print(f"\n    {Y}● Large exact matches: p < 0.05 — suggestive{X}")
        else:
            print(f"\n    {R}✗ Large exact matches: p = {p_l:.3f} — NOT significant{X}")

    print()
    return values, total, large


# ═══════════════════════════════════════════════════════════════════
# HTML (simplified, focused on null model results)
# ═══════════════════════════════════════════════════════════════════

def generate_html(systems, vocab):
    """Generate self-contained HTML with null model results."""

    # Run all three analyses
    v_all, t_all, l_all, sr_all = analyze(systems, vocab, None)
    v_cnt, t_cnt, l_cnt, sr_cnt = analyze(systems, vocab, {"count", "derived"})

    # Run null models
    null_all = run_null_model(v_all, vocab, 10000)
    null_cnt = run_null_model(v_cnt, vocab, 10000)

    exact_all = t_all["exact"] + t_all["root_q"]
    exact_cnt = t_cnt["exact"] + t_cnt["root_q"]

    _, _, z_all, p_all = null_stats(l_all["exact"], null_all["large_exact"])
    _, _, z_cnt, p_cnt = null_stats(l_cnt["exact"], null_cnt["large_exact"])
    m_all, s_all, _, _ = null_stats(l_all["exact"], null_all["large_exact"])
    m_cnt, s_cnt, _, _ = null_stats(l_cnt["exact"], null_cnt["large_exact"])

    # Build system detail JSON
    sys_json = []
    for sr in sr_all:
        sys_json.append({
            "name": sr["name"],
            "exact": sr["exact"], "total": sr["total"],
            "counts": sr["results"]
        })

    data = json.dumps({
        "systems": sys_json,
        "null_model": {
            "all": {"observed_large": l_all["exact"], "total_large": l_all["total"],
                    "null_mean": round(m_all, 1), "null_std": round(s_all, 1),
                    "z": round(z_all, 1), "p": round(p_all, 4)},
            "counts_only": {"observed_large": l_cnt["exact"], "total_large": l_cnt["total"],
                           "null_mean": round(m_cnt, 1), "null_std": round(s_cnt, 1),
                           "z": round(z_cnt, 1), "p": round(p_cnt, 4)},
        },
        "totals": {
            "all": {"n": sum(t_all.values())-t_all["trivial"], "exact": exact_all, "miss": t_all["miss"]},
            "counts_only": {"n": sum(t_cnt.values())-t_cnt["trivial"], "exact": exact_cnt, "miss": t_cnt["miss"]},
        }
    }, indent=2, ensure_ascii=False)

    html = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<title>FM Algebraic Decomposition v2</title>
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ font-family: 'Palatino Linotype', Georgia, serif; background:#fafafa;
       color:#1a1a1a; max-width:900px; margin:0 auto; padding:20px 30px; line-height:1.5; }}
h1 {{ font-size:24px; font-weight:normal; letter-spacing:2px; text-transform:uppercase;
     border-bottom:2px solid #1a1a1a; padding-bottom:6px; margin:20px 0 5px; }}
.sub {{ font-size:13px; color:#666; margin-bottom:20px; }}
.null-box {{ background:#fff; border:2px solid #1a1a1a; padding:16px 20px; margin:20px 0; }}
.null-box h2 {{ font-size:16px; margin-bottom:10px; }}
.null-row {{ display:flex; gap:30px; margin:8px 0; font-size:14px; }}
.null-label {{ width:120px; font-weight:bold; }}
.verdict {{ font-size:18px; font-weight:bold; margin-top:12px; padding:8px 12px; }}
.sig {{ background:#c8e6c9; color:#2e7d32; }}
.nosig {{ background:#ffcdd2; color:#c62828; }}
.system {{ margin:15px 0; border:1px solid #ddd; background:#fff; }}
.sys-h {{ padding:10px 16px; background:#f5f5f5; cursor:pointer; display:flex;
          justify-content:space-between; border-bottom:1px solid #ddd; font-size:15px; }}
.sys-h:hover {{ background:#eee; }}
.sys-b {{ display:none; padding:0; }}
.sys-b.open {{ display:block; }}
table {{ width:100%; border-collapse:collapse; font-size:13px; }}
th {{ text-align:left; padding:6px 10px; background:#fafafa; border-bottom:2px solid #ddd;
     font-size:10px; text-transform:uppercase; letter-spacing:1px; color:#888; }}
td {{ padding:5px 10px; border-bottom:1px solid #f0f0f0; }}
.v {{ font-family:monospace; font-weight:bold; text-align:right; }}
.EXACT {{ color:#2e7d32; font-weight:bold; }}
.ROOT_QUOTIENT {{ color:#0277bd; font-weight:bold; }}
.PRODUCT {{ color:#6a1b9a; }}
.DECOMPOSITION {{ color:#1565c0; }}
.MISS {{ color:#c62828; font-weight:bold; }}
.tag {{ font-size:10px; color:#999; margin-left:4px; }}
footer {{ margin-top:30px; padding-top:10px; border-top:1px solid #ddd;
         font-size:11px; color:#888; text-align:center; }}
</style></head><body>
<h1>FM Algebraic Decomposition v2</h1>
<p class="sub">With null model. Structural counts separated from physical measurements.</p>

<div class="null-box">
<h2>NULL MODEL — Is the signal real?</h2>
<p style="font-size:12px;color:#666;margin-bottom:10px;">
10,000 trials. Each biological value replaced with random integer of same magnitude.
Key test: large numbers (&gt;12) where trivial matches are excluded.</p>

<div class="null-row"><div class="null-label">ALL VALUES</div>
<div>Large exact: <b id="a-obs"></b> observed vs <b id="a-null"></b> null &nbsp;|&nbsp;
z = <b id="a-z"></b> &nbsp;|&nbsp; p = <b id="a-p"></b></div></div>

<div class="null-row"><div class="null-label">COUNTS ONLY</div>
<div>Large exact: <b id="c-obs"></b> observed vs <b id="c-null"></b> null &nbsp;|&nbsp;
z = <b id="c-z"></b> &nbsp;|&nbsp; p = <b id="c-p"></b></div></div>

<div class="verdict" id="verdict"></div>
</div>

<div id="systems"></div>

<footer>FM Algebraic Decomposition v2 — Null model addresses the critique.<br>
Algebra IS physics at structural resolution. The null model tests whether this is distinguishable from noise.</footer>

<script>
const D = {data};
const nm = D.null_model;
document.getElementById('a-obs').textContent = nm.all.observed_large + '/' + nm.all.total_large;
document.getElementById('a-null').textContent = nm.all.null_mean + '±' + nm.all.null_std;
document.getElementById('a-z').textContent = nm.all.z;
document.getElementById('a-p').textContent = nm.all.p < 0.001 ? '<0.001' : nm.all.p;
document.getElementById('c-obs').textContent = nm.counts_only.observed_large + '/' + nm.counts_only.total_large;
document.getElementById('c-null').textContent = nm.counts_only.null_mean + '±' + nm.counts_only.null_std;
document.getElementById('c-z').textContent = nm.counts_only.z;
document.getElementById('c-p').textContent = nm.counts_only.p < 0.001 ? '<0.001' : nm.counts_only.p;

const pVal = nm.counts_only.p;
const vEl = document.getElementById('verdict');
if (pVal < 0.001) {{
    vEl.className = 'verdict sig';
    vEl.textContent = 'SIGNAL IS REAL — structural counts match algebra far beyond chance (p < 0.001)';
}} else if (pVal < 0.05) {{
    vEl.className = 'verdict sig';
    vEl.textContent = 'SUGGESTIVE — p = ' + pVal + ' (below 0.05 threshold)';
}} else {{
    vEl.className = 'verdict nosig';
    vEl.textContent = 'NOT SIGNIFICANT — random numbers match at similar rate (p = ' + pVal + ')';
}}

const container = document.getElementById('systems');
D.systems.forEach((s, i) => {{
    const pct = s.total > 0 ? ((s.exact/s.total)*100).toFixed(0) : 0;
    let rows = '';
    s.counts.forEach(c => {{
        const cls = c.match;
        const tag = c.ctype !== 'count' ? '<span class="tag">[' + c.ctype + ']</span>' : '';
        rows += '<tr><td>' + c.name + tag + '</td><td class="v">' + c.value +
                '</td><td class="' + cls + '">' + cls.replace('_',' ') +
                '</td><td>' + c.expl + '</td></tr>';
    }});
    container.innerHTML += '<div class="system"><div class="sys-h" onclick="this.nextElementSibling.classList.toggle(\'open\')"><span>' +
        s.name + '</span><span>' + pct + '% exact</span></div>' +
        '<div class="sys-b' + (i===0?' open':'') + '"><table><tr><th>Component</th><th>Value</th><th>Match</th><th>Source</th></tr>' +
        rows + '</table></div></div>';
}});
</script></body></html>"""

    with open("fm-decomposition-v2.html", "w", encoding="utf-8") as f:
        f.write(html)


# ═══════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════

def main():
    import sys as _sys, io as _io
    _sys.stdout = _io.TextIOWrapper(_sys.stdout.buffer, encoding='utf-8', errors='replace')

    vocab = build_vocabulary()
    systems = build_systems()

    print(f"\n  Vocabulary: {len(vocab)} algebraic numbers")
    print(f"  Systems: {len(systems)}")

    # Analysis 1: ALL counts
    print_analysis("ANALYSIS 1: ALL COUNTS (including Svedberg measurements)",
                   systems, vocab, None, run_null=True)

    # Analysis 2: STRUCTURAL COUNTS ONLY
    print_analysis("ANALYSIS 2: STRUCTURAL COUNTS ONLY (no measurements)",
                   systems, vocab, {"count", "derived"}, run_null=True)

    # Generate HTML
    generate_html(systems, vocab)
    print("  Saved: fm-decomposition-v2.html\n")


if __name__ == "__main__":
    main()
