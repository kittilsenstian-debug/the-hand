#!/usr/bin/env python3
import math

PHI = (1 + math.sqrt(5)) / 2
PHIBAR = 1 / PHI
SQRT5 = math.sqrt(5)
SQRT2 = math.sqrt(2)

def fib(n):
    if n <= 0: return 0
    if n == 1 or n == 2: return 1
    a, b = 1, 1
    for _ in range(n - 2):
        a, b = b, a + b
    return b

def luc(n):
    if n == 0: return 2
    if n == 1: return 1
    a, b = 2, 1
    for _ in range(n - 1):
        a, b = b, a + b
    return b

F = {n: fib(n) for n in range(0, 51)}
L = {n: luc(n) for n in range(0, 51)}

SEP = "=" * 108

print(SEP)
print("UNIFIED LANGUAGE DICTIONARY -- RIGOROUS VERIFICATION")
print(SEP)
print()
print("Reference: Fibonacci F(n) and Lucas L(n) values")
print("-" * 60)
for nn in [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]:
    print("  F(%2d) = %7d    L(%2d) = %7d" % (nn, F[nn], nn, L[nn]))
for nn in [20,22,25,29,30,34,36]:
    print("  F(%2d) = %10d    L(%2d) = %10d" % (nn, F[nn], nn, L[nn]))
print()
print("  phi    = %.10f" % PHI)
print("  phibar = %.10f" % PHIBAR)
print()

entries = []

def add(name, cat, formula, computed, measured, source="PDG 2024"):
    entries.append(dict(name=name, cat=cat, formula=formula,
                        computed=computed, measured=measured, source=source))

# ---- GAUGE COUPLINGS (8) ----
add("alpha_s", "Gauge", "L(3)*L(6)/F(15) = 4*18/610", L[3]*L[6]/F[15], 0.1179)
add("sin2_tW", "Gauge", "L(2)*L(8)/F(15) = 3*47/610", L[2]*L[8]/F[15], 0.23121)
add("alpha_em (F/L)", "Gauge", "(F(5)+F(8))/L(17) = 26/3571", (F[5]+F[8])/L[17], 1.0/137.036)
add("1/3 (charge q)", "Gauge", "L(4)*L(7)/F(15) = 203/610", L[4]*L[7]/F[15], 1.0/3)
add("gamma_Immirzi", "Gauge", "F(5)*L(7)/F(15) = 145/610", F[5]*L[7]/F[15], 0.2375)
add("alpha_2 (weak)", "Gauge", "L(2)/F(11) = 3/89", L[2]/F[11], 0.03378)
add("g/2 (weak/2)", "Gauge", "L(8)/F(12) = 47/144", L[8]/F[12], 0.32645)
add("a_e (g-2)_e", "Gauge", "L(2)/F(18) = 3/2584", L[2]/F[18], 0.00115965)

# ---- CKM MATRIX (9) ----
add("V_ud", "CKM", "1-F(3)/L(9) = 1-2/76", 1.0-F[3]/L[9], 0.97373)
add("V_us", "CKM", "F(11)/(L(6)+F(14)) = 89/395", F[11]/(L[6]+F[14]), 0.2243)
add("V_ub", "CKM", "1/(L(7)+F(13)) = 1/262", 1.0/(L[7]+F[13]), 0.00382)
add("V_cd", "CKM", "L(7)/(F(6)+L(10)) = 29/131", L[7]/(F[6]+L[10]), 0.221)
add("V_cs", "CKM", "1-L(5)/(F(4)+L(14)) = 1-11/846", 1.0-L[5]/(F[4]+L[14]), 0.975)
add("V_cb", "CKM", "(L(4)+L(6))/F(15) = 25/610", (L[4]+L[6])/F[15], 0.0406)
add("V_td", "CKM", "1/(F(3)+L(10)) = 1/125", 1.0/(F[3]+L[10]), 0.0080)
add("V_ts", "CKM", "F(7)/(F(7)+L(12)) = 13/335", F[7]/(F[7]+L[12]), 0.0388)
add("V_tb", "CKM", "1-F(6)/L(19) = 1-8/9349", 1.0-F[6]/L[19], 0.99917)

# ---- PMNS MATRIX (3) ----
add("sin2_12 (PMNS)", "PMNS", "1/3-F(3)/L(9) = 1/3-2/76", 1.0/3-F[3]/L[9], 0.307)
add("sin2_23 (PMNS)", "PMNS", "(L(5)+L(12))/F(15) = 333/610", (L[5]+L[12])/F[15], 0.546)
add("sin2_13 (PMNS)", "PMNS", "L(5)/(L(10)+F(14)) = 11/500", L[5]/(L[10]+F[14]), 0.0220)

# ---- PARTICLE MASSES (18) ----
add("m_e (keV)", "Mass", "L(13)-F(3)*F(5) = 521-10", float(L[13]-F[3]*F[5]), 511.0)
add("m_t (GeV)", "Mass", "L(13)/L(2) = 521/3", L[13]/L[2], 172.69)
add("M_H (GeV)", "Mass", "F(14)/L(2) = 377/3", F[14]/L[2], 125.10)
add("v (Higgs GeV)", "Mass", "F(16)/L(3) = 987/4", F[16]/L[3], 246.22)
add("M_W (GeV)", "Mass", "L(12)/L(3) = 322/4", L[12]/L[3], 80.377)
add("m_b (GeV)", "Mass", "F(8)/F(5) = 21/5", F[8]/F[5], 4.18)
add("m_c (GeV)", "Mass", "F(5)/L(3) = 5/4", F[5]/L[3], 1.27)
add("m_proton (MeV)", "Mass", "F(16)-L(4)^2 = 987-49", float(F[16]-L[4]**2), 938.3)
add("m_neutron (MeV)", "Mass", "F(16)-L(8) = 987-47", float(F[16]-L[8]), 939.6)
add("m_tau (MeV)", "Mass", "L(16)-F(4)*F(12) = 2207-432", float(L[16]-F[4]*F[12]), 1776.9)
add("m_mu (GeV)", "Mass", "F(7)*F(8)/F(18) = 273/2584", F[7]*F[8]/F[18], 0.10566)
add("M_Z (GeV)", "Mass", "L(10)-L(3)*F(6) = 123-32", float(L[10]-L[3]*F[6]), 91.188)
add("M_W (GeV alt)", "Mass", "F(11)-F(4)^2 = 89-9", float(F[11]-F[4]**2), 80.377)
add("m_u (GeV)", "Mass", "L(2)^2/F(19) = 9/4181", L[2]**2/F[19], 0.00216)
add("m_d (GeV)", "Mass", "v*F(3)/(F(25)*sqrt2)", 246.22*F[3]/(F[25]*SQRT2), 0.00467)
add("m_s (GeV)", "Mass", "v*F(5)/(L(19)*sqrt2)", 246.22*F[5]/(L[19]*SQRT2), 0.0934)
add("f_pi (MeV)", "Mass", "L(13)/L(3) = 521/4", L[13]/L[3], 130.41)
add("m_e (GeV alt)", "Mass", "L(2)/L(18) = 3/5778", L[2]/L[18], 0.000511)

# ---- MASS RATIOS (11) ----
add("m_t/m_c", "Ratio", "L(3)*F(9) = 4*34 = 136", float(L[3]*F[9]), 172.69/1.27)
add("m_s/m_d", "Ratio", "L(3)*F(5) = 4*5 = 20", float(L[3]*F[5]), 93.4/4.67)
add("m_H/m_Z", "Ratio", "L(5)/F(6) = 11/8", L[5]/F[6], 125.10/91.188)
add("m_t/m_Z", "Ratio", "F(11)/L(8) = 89/47", F[11]/L[8], 172.69/91.188)
add("m_t/m_H", "Ratio", "L(7)^2/F(15) = 841/610", L[7]**2/F[15], 172.69/125.10)
add("m_b/m_s", "Ratio", "L(3)*L(10)/L(5) = 492/11", L[3]*L[10]/L[5], 4.18/0.0934)
add("m_tau/m_mu", "Ratio", "L(3)*F(8)/F(5) = 84/5", L[3]*F[8]/F[5], 1776.9/105.66)
add("m_mu/m_e", "Ratio", "L(4)*F(11)/F(4) = 623/3", L[4]*F[11]/F[4], 105.66/0.51100)
add("m_c/m_s", "Ratio", "L(8)/L(3) = 47/4", L[8]/L[3], 1270.0/93.4)
add("mu (p/e mod)", "Ratio", "6^5/phi^3+9/(7*phi^2)", 6**5/PHI**3+9.0/(7*PHI**2), 1836.153)
add("mu (p/e F/L)", "Ratio", "F(7)*F(16)/L(4)=12831/7", F[7]*F[16]/L[4], 1836.153)

# ---- YUKAWA COUPLINGS (9) ----
add("y_t", "Yukawa", "L(5)*L(8)/L(13) = 517/521", L[5]*L[8]/L[13], 0.9934)
add("y_b", "Yukawa", "L(2)^2/F(14) = 9/377", L[2]**2/F[14], 0.0240)
add("y_tau", "Yukawa", "F(3)*L(4)/L(15) = 14/1364", F[3]*L[4]/L[15], 0.01021)
add("y_c", "Yukawa", "F(3)*F(7)/L(17) = 26/3571", F[3]*F[7]/L[17], 0.00726)
add("y_mu", "Yukawa", "L(2)*F(6)/L(22) = 24/39603", L[2]*F[6]/L[22], 0.000607)
add("y_s", "Yukawa", "F(5)/L(19) = 5/9349", F[5]/L[19], 0.000538)
add("y_e", "Yukawa", "(2/3)*F(8)*L(4)/L(36)", (2.0/3)*F[8]*L[4]/L[36], 0.00000294)
add("y_u", "Yukawa", "(1/2)*L(6)^2/L(34)", 0.5*L[6]**2/L[34], 0.0000127)
add("y_d", "Yukawa", "F(1)/L(22) = 1/39603", F[1]/L[22], 0.0000268)

# ---- KOIDE (3) ----
add("Koide(leptons)", "Koide", "F(3)/F(4) = 2/3", F[3]/F[4], 0.66667)
add("Koide(up q)", "Koide", "L(5)/F(7) = 11/13", L[5]/F[7], 0.8462)
add("Koide(down q)", "Koide", "F(6)/L(5) = 8/11", F[6]/L[5], 0.7273)

# ---- COSMOLOGICAL (7) ----
add("Omega_m", "Cosmo", "L(7)/(F(4)+F(11)) = 29/92", L[7]/(F[4]+F[11]), 0.315)
add("Omega_L", "Cosmo", "F(13)/(L(6)+L(12))=233/340", F[13]/(L[6]+L[12]), 0.685)
add("H0 (km/s/Mpc)", "Cosmo", "(L(6)+L(13))/F(6) = 539/8", (L[6]+L[13])/F[6], 67.4)
add("n_s", "Cosmo", "F(10)/(F(3)+F(10)) = 55/57", F[10]/(F[3]+F[10]), 0.965)
add("sigma_8", "Cosmo", "L(8)/(L(5)+L(8)) = 47/58", L[8]/(L[5]+L[8]), 0.811)
add("eta_B", "Cosmo", "3*F(4)/(F(18)*F(34))", 3.0*F[4]/(F[18]*F[34]), 6.12e-10)
add("Omega_b", "Cosmo", "(L(4)+L(11))/F(19)=206/4181", (L[4]+L[11])/F[19], 0.0493)

# ---- OTHER (2) ----
add("R_c", "Other", "F(5)/L(7) = 5/29", F[5]/L[7], 0.1721)
add("r_tensor", "Other", "L(6)/L(12) = 18/322", L[6]/L[12], 0.056)

# ============================================================
# COMPUTE AND DISPLAY
# ============================================================
print(SEP)
hfmt = "%-4s %-21s %-7s %-43s %13s %13s %9s %s"
print(hfmt % ("#", "Quantity", "Cat", "F/L Formula", "F/L Value", "Measured", "Error%", "Status"))
print(SEP)

n_total = 0
n_below_01 = 0
n_below_05 = 0
n_below_1 = 0
n_above_1 = 0
n_above_5 = 0
n_factor2 = 0
flagged = []
all_errors = []

for i, e in enumerate(entries):
    n_total += 1
    comp = e["computed"]
    meas = e["measured"]
    if meas != 0:
        error_pct = abs(comp - meas) / abs(meas) * 100.0
    else:
        error_pct = 0.0 if comp == 0 else float("inf")

    all_errors.append(error_pct)

    if error_pct < 0.005:
        status = "EXACT"
    elif error_pct < 0.1:
        status = "OK"
    elif error_pct < 0.5:
        status = "ok"
    elif error_pct < 1.0:
        status = "~ok"
    elif error_pct < 5.0:
        status = "** >1% **"
    else:
        status = "*** BAD ***"

    if meas != 0:
        ratio = comp / meas
        if ratio > 2.0 or ratio < 0.5:
            status = "!!! WRONG !!!"
            n_factor2 += 1

    if error_pct < 0.1: n_below_01 += 1
    if error_pct < 0.5: n_below_05 += 1
    if error_pct < 1.0: n_below_1 += 1
    if error_pct >= 1.0: n_above_1 += 1
    if error_pct >= 5.0: n_above_5 += 1

    if error_pct >= 1.0:
        flagged.append(e)

    if abs(comp) >= 100:
        cs = "%.4f" % comp
    elif abs(comp) >= 1:
        cs = "%.6f" % comp
    elif abs(comp) >= 0.001:
        cs = "%.8f" % comp
    elif abs(comp) >= 1e-6:
        cs = "%.6e" % comp
    else:
        cs = "%.6e" % comp

    if abs(meas) >= 100:
        ms = "%.4f" % meas
    elif abs(meas) >= 1:
        ms = "%.6f" % meas
    elif abs(meas) >= 0.001:
        ms = "%.8f" % meas
    elif abs(meas) >= 1e-6:
        ms = "%.6e" % meas
    else:
        ms = "%.6e" % meas

    print("%-4d %-21s %-7s %-43s %13s %13s %8.4f%% %s" % (
        i+1, e["name"], e["cat"], e["formula"][:43],
        cs, ms, error_pct, status))

print(SEP)
print()
# ============================================================
# SUMMARY
# ============================================================
print("=" * 78)
print("SUMMARY TABLE")
print("=" * 78)
print()
print("  Total entries verified:           %d" % n_total)
print()
print("  Error < 0.1%%  (excellent):        %d  (%.1f%%)" % (n_below_01, 100.0*n_below_01/n_total))
print("  Error < 0.5%%  (good):             %d  (%.1f%%)" % (n_below_05, 100.0*n_below_05/n_total))
print("  Error < 1.0%%  (acceptable):       %d  (%.1f%%)" % (n_below_1, 100.0*n_below_1/n_total))
print("  Error >= 1.0%% (FLAGGED):          %d  (%.1f%%)" % (n_above_1, 100.0*n_above_1/n_total))
print("  Error >= 5.0%% (SERIOUSLY BAD):    %d" % n_above_5)
print("  Factor-of-2 wrong (INCORRECT):    %d" % n_factor2)
print()

avg_err = sum(all_errors)/len(all_errors) if all_errors else 0
med_err = sorted(all_errors)[len(all_errors)//2] if all_errors else 0
max_err = max(all_errors) if all_errors else 0

print("  Average error: %.4f%%" % avg_err)
print("  Median error:  %.4f%%" % med_err)
print("  Maximum error: %.4f%%" % max_err)
print()

if flagged:
    print("  FLAGGED entries (error >= 1%):")
    for e in flagged:
        comp = e["computed"]; meas = e["measured"]
        err = abs(comp-meas)/abs(meas)*100 if meas != 0 else 0
        print("    - %-22s  error=%.3f%%  computed=%.7e  measured=%.7e" % (
            e["name"], err, comp, meas))
    print()

# ============================================================
# CATEGORY BREAKDOWN
# ============================================================
print("=" * 78)
print("CATEGORY BREAKDOWN")
print("=" * 78)
print()

cats = {}
for e in entries:
    c = e["cat"]
    if c not in cats:
        cats[c] = dict(total=0, b01=0, b05=0, b1=0, a1=0, errs=[])
    comp = e["computed"]; meas = e["measured"]
    err = abs(comp-meas)/abs(meas)*100 if meas != 0 else 0
    cats[c]["total"] += 1
    cats[c]["errs"].append(err)
    if err < 0.1: cats[c]["b01"] += 1
    if err < 0.5: cats[c]["b05"] += 1
    if err < 1.0: cats[c]["b1"] += 1
    if err >= 1.0: cats[c]["a1"] += 1

print("  %-12s %5s %8s %8s %8s %8s %10s" % (
    "Category", "Total", "<0.1%", "<0.5%", "<1.0%", ">=1.0%", "Avg err%"))
print("  " + "-" * 65)
for c in ["Gauge","CKM","PMNS","Mass","Ratio","Yukawa","Koide","Cosmo","Other"]:
    if c in cats:
        d = cats[c]
        a = sum(d["errs"])/len(d["errs"]) if d["errs"] else 0
        print("  %-12s %5d %8d %8d %8d %8d %9.3f%%" % (
            c, d["total"], d["b01"], d["b05"], d["b1"], d["a1"], a))

print()
# ============================================================
# CLAIMED vs ACTUAL
# ============================================================
print("=" * 78)
print("CLAIMED vs ACTUAL STATISTICS")
print("=" * 78)
print()
print("  The working document claims:")
print("    - 68/68 below 1%")
print("    - 43/68 below 0.1%")
print("    - Average error ~0.15%")
print()
print("  ACTUAL (this verification, %d entries):" % n_total)
print("    - %d/%d below 1%%" % (n_below_1, n_total))
print("    - %d/%d below 0.1%%" % (n_below_01, n_total))
print("    - Average error: %.4f%%" % avg_err)
print("    - Median error:  %.4f%%" % med_err)
print()
if n_above_1 > 0:
    print("  *** DISCREPANCY: %d entries ABOVE 1%%, contradicting 68/68 claim." % n_above_1)
    print()

# ============================================================
# DETAILED FLAGGED
# ============================================================
if flagged:
    print("=" * 78)
    print("DETAILED ANALYSIS OF FLAGGED ENTRIES (error >= 1%)")
    print("=" * 78)
    print()
    for e in flagged:
        comp = e["computed"]; meas = e["measured"]
        err = abs(comp-meas)/abs(meas)*100 if meas != 0 else 0
        ratio = comp/meas if meas != 0 else float("inf")
        print("  %s" % e["name"])
        print("    Formula:  %s" % e["formula"])
        print("    Computed: %.10e" % comp)
        print("    Measured: %.10e (%s)" % (meas, e["source"]))
        print("    Error:    %.4f%%" % err)
        f2 = "YES" if (ratio > 2 or ratio < 0.5) else "no"
        print("    Ratio:    %.6f (factor-of-2 wrong: %s)" % (ratio, f2))
        print()

# ============================================================
# F/L ARITHMETIC CROSS-CHECK
# ============================================================
print("=" * 78)
print("F/L ARITHMETIC CROSS-CHECK")
print("=" * 78)
print()
checks = [
    ("F(3)", F[3], 2), ("F(4)", F[4], 3), ("F(5)", F[5], 5),
    ("F(6)", F[6], 8), ("F(7)", F[7], 13), ("F(8)", F[8], 21),
    ("F(9)", F[9], 34), ("F(10)", F[10], 55), ("F(11)", F[11], 89),
    ("F(12)", F[12], 144), ("F(13)", F[13], 233), ("F(14)", F[14], 377),
    ("F(15)", F[15], 610), ("F(16)", F[16], 987), ("F(18)", F[18], 2584),
    ("F(19)", F[19], 4181), ("F(25)", F[25], 75025), ("F(34)", F[34], 5702887),
    ("L(2)", L[2], 3), ("L(3)", L[3], 4), ("L(4)", L[4], 7),
    ("L(5)", L[5], 11), ("L(6)", L[6], 18), ("L(7)", L[7], 29),
    ("L(8)", L[8], 47), ("L(9)", L[9], 76), ("L(10)", L[10], 123),
    ("L(11)", L[11], 199), ("L(12)", L[12], 322), ("L(13)", L[13], 521),
    ("L(14)", L[14], 843), ("L(15)", L[15], 1364), ("L(16)", L[16], 2207),
    ("L(17)", L[17], 3571), ("L(19)", L[19], 9349), ("L(22)", L[22], 39603),
]
all_ok = True
for name, val, exp in checks:
    ok = (val == exp)
    if not ok: all_ok = False
    s = "OK" if ok else "MISMATCH (expected %d)" % exp
    print("  %-8s = %12d  %s" % (name, val, s))
print()
print("  L(34) = %d" % L[34])
print("  L(36) = %d" % L[36])
print()
if all_ok:
    print("  All F/L arithmetic checks PASS.")
else:
    print("  *** SOME F/L VALUES DO NOT MATCH ***")

print()
print("=" * 78)
print("VERIFICATION COMPLETE")
print("=" * 78)
