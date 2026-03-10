#!/usr/bin/env python3
import math

PHI = (1 + math.sqrt(5)) / 2
PHIBAR = 1 / PHI
SQRT5 = math.sqrt(5)

def fib(n):
    if n <= 0: return 0
    return round((PHI**n - (-PHIBAR)**n) / SQRT5)

def luc(n):
    if n == 0: return 2
    return round(PHI**n + (-PHIBAR)**n)

MAX_N = 50
F = {}; L = {}
for i in range(1, MAX_N + 1):
    F[i] = fib(i); L[i] = luc(i)

q = PHIBAR; N_terms = 2000
eta_val = q**(1.0/24)
for n in range(1, N_terms): eta_val *= (1 - q**n)
t4 = 1.0
for n in range(1, N_terms): t4 *= (1 - q**(2*n)) * (1 - q**(2*n-1))**2
t3 = 1.0
for n in range(1, N_terms): t3 *= (1 - q**(2*n)) * (1 + q**(2*n-1))**2
C_loop = eta_val * t4 / 2

TARGETS = {"y_e": 2.935e-6, "y_u": 1.27e-5, "eta_B": 6.12e-10, "v/M_Pl": 2.013e-17}

def ep(val, target):
    if val <= 0 or target <= 0: return 1e10
    return abs(val - target) / target * 100

def search(name, target):
    results = []
    pf = {"": 1, "(1/6)*": 1.0/6, "(1/3)*": 1.0/3, "(1/2)*": 0.5,
          "(2/3)*": 2.0/3, "2*": 2, "3*": 3, "6*": 6,
          "(1/phi)*": PHIBAR, "phi*": PHI}
    SQ = {"F": F, "L": L}
    for n1,s1 in SQ.items():
        for n2,s2 in SQ.items():
            for a in range(1,16):
                if not s1.get(a): continue
                for b in range(15,46):
                    if not s2.get(b): continue
                    val = s1[a]/s2[b]
                    for pn,pv in pf.items():
                        v = pv*val; e = ep(v,target)
                        if e < 5: results.append((e, pn+n1+"("+str(a)+")/"+n2+"("+str(b)+")", v))
    for n1,s1 in SQ.items():
        for n2,s2 in SQ.items():
            for n3,s3 in SQ.items():
                for a in range(1,11):
                    if not s1.get(a): continue
                    for b in range(1,11):
                        if not s2.get(b): continue
                        for c in range(20,46):
                            if not s3.get(c): continue
                            val = s1[a]*s2[b]/s3[c]
                            for pn,pv in pf.items():
                                v = pv*val; e = ep(v,target)
                                if e < 2: results.append((e, pn+n1+"("+str(a)+")*"+n2+"("+str(b)+")/"+n3+"("+str(c)+")", v))
    for k in range(20,101):
        val = PHIBAR**k
        for pn,pv in pf.items():
            v = pv*val; e = ep(v,target)
            if e < 5: results.append((e, pn+"phibar^"+str(k), v))
    for n in range(3,11):
        for sn,s in SQ.items():
            xp = s.get(n,0)
            if 0 < xp < 200:
                val = PHIBAR**xp
                for pn,pv in pf.items():
                    v = pv*val; e = ep(v,target)
                    if e < 5: results.append((e, pn+"phibar^"+sn+"("+str(n)+")", v))
    for n1,s1 in SQ.items():
        for n2,s2 in SQ.items():
            for n3,s3 in SQ.items():
                for a in range(1,11):
                    if not s1.get(a): continue
                    for b in range(10,35):
                        if not s2.get(b): continue
                        for c in range(10,35):
                            if not s3.get(c): continue
                            dn = s2[b]*s3[c]
                            if dn==0: continue
                            val = s1[a]/dn
                            for pn,pv in pf.items():
                                v = pv*val; e = ep(v,target)
                                if e < 2: results.append((e, pn+n1+"("+str(a)+")/("+n2+"("+str(b)+")*"+n3+"("+str(c)+"))", v))
    for a in range(-80,-10):
        pp = PHI**a
        for sn,s in SQ.items():
            for b in range(1,11):
                if not s.get(b): continue
                val = pp*s[b]; e = ep(val,target)
                if e < 2: results.append((e, "phibar^"+str(-a)+"*"+sn+"("+str(b)+")", val))
                val = pp/s[b]; e = ep(val,target)
                if e < 2: results.append((e, "phibar^"+str(-a)+"/"+sn+"("+str(b)+")", val))
    for k in range(10,90):
        bs = PHIBAR**k
        for n1,s1 in SQ.items():
            for n2,s2 in SQ.items():
                for a in range(1,11):
                    if not s1.get(a): continue
                    for b in range(1,11):
                        if not s2.get(b): continue
                        if a==b and n1==n2: continue
                        val = bs*s1[a]/s2[b]; e = ep(val,target)
                        if e < 1: results.append((e, "phibar^"+str(k)+"*"+n1+"("+str(a)+")/"+n2+"("+str(b)+")", val))
    for k in range(20,101):
        bs = PHIBAR**k
        for d in [2,3,4,5,6,7,8,9,10,12,15,18,21,24,36]:
            val = bs/d; e = ep(val,target)
            if e < 3: results.append((e, "phibar^"+str(k)+"/"+str(d), val))
            val = bs*d; e = ep(val,target)
            if e < 3: results.append((e, str(d)+"*phibar^"+str(k), val))
    for n1,s1 in SQ.items():
        for n2,s2 in SQ.items():
            for a in range(5,30):
                if not s1.get(a): continue
                for b in range(5,30):
                    if not s2.get(b): continue
                    val = 1.0/(s1[a]*s2[b])
                    for pn,pv in pf.items():
                        v = pv*val; e = ep(v,target)
                        if e < 3: results.append((e, pn+"1/("+n1+"("+str(a)+")*"+n2+"("+str(b)+"))", v))
    for sn,s in SQ.items():
        for a in range(5,46):
            if not s.get(a): continue
            for p in [2,3]:
                val = 1.0/s[a]**p
                for pn,pv in pf.items():
                    v = pv*val; e = ep(v,target)
                    if e < 3: results.append((e, pn+"1/"+sn+"("+str(a)+")^"+str(p), v))
    if target < 1e-12:
        for n1,s1 in SQ.items():
            for n2,s2 in SQ.items():
                for n3,s3 in SQ.items():
                    for a in range(5,20):
                        if not s1.get(a): continue
                        for b in range(5,20):
                            if not s2.get(b): continue
                            for ci in range(5,20):
                                if not s3.get(ci): continue
                                val = 1.0/(s1[a]*s2[b]*s3[ci])
                                for pn,pv in pf.items():
                                    v = pv*val; e = ep(v,target)
                                    if e < 2: results.append((e, pn+"1/("+n1+"("+str(a)+")*"+n2+"("+str(b)+")*"+n3+"("+str(ci)+"))", v))
    lg = {"phi": PHI, "phi2": PHI**2, "phibar": PHIBAR, "sqrt5": SQRT5, "1": 1.0, "2": 2.0, "3": 3.0}
    for k in range(20,101):
        bs = PHIBAR**k
        for gn,gv in lg.items():
            for sgn in [1,-1]:
                cv = bs*(1+sgn*C_loop*gv); e = ep(cv,target)
                if e < 3:
                    ss = "+" if sgn > 0 else "-"
                    results.append((e, "phibar^"+str(k)+"*(1"+ss+"C*"+gn+")", cv))
    results.sort(key=lambda x:x[0])
    seen = set(); u = []
    for er,fm,vl in results:
        ky = round(vl,25)
        if ky not in seen: seen.add(ky); u.append((er,fm,vl))
        if len(u) >= 20: break
    return u


if __name__ == "__main__":
    print("=" * 95)
    print("CLOSE LAST GAPS: Systematic Fibonacci/Lucas/phi search")
    print("=" * 95)
    print()
    print("  phi=%.10f phibar=%.10f" % (PHI, PHIBAR))
    print("  eta=%.10f t4=%.10f t3=%.10f C=%.10f" % (eta_val, t4, t3, C_loop))
    print()
    for n in [20, 25, 30, 35, 40, 45]:
        print("    F(%d)=%20d  L(%d)=%20d" % (n, F[n], n, L[n]))
    print()
    for name, target in TARGETS.items():
        print("=" * 95)
        print("  %s = %.4e" % (name, target))
        print("-" * 95)
        results = search(name, target)
        if not results:
            print("  No matches found.")
        else:
            print("  %-6s %-12s %-50s %-16s %-16s" % ("Rank", "Error%", "Formula", "Value", "Target"))
            print("  " + "-"*6 + " " + "-"*12 + " " + "-"*50 + " " + "-"*16 + " " + "-"*16)
            for i, (er, fm, vl) in enumerate(results[:15]):
                mk = " <<<" if er < 0.1 else (" **" if er < 0.5 else "")
                print("  %-6d %-12.6f %-50s %-16.6e %-16.6e%s" % (i+1, er, fm, vl, target, mk))
        print()

    # Deep modular combo search for each target
    for yname, ytarget in TARGETS.items():
        print("=" * 95)
        print("DEEP SEARCH: %s = %.4e (modular form combos)" % (yname, ytarget))
        print("=" * 95)
        dy = []
        # eta^a * theta4^b * phi^c
        for a in range(0, 10):
            for b in range(0, 10):
                if a + b == 0: continue
                for c in range(-10, 15):
                    v = eta_val**a * t4**b * PHI**c; e = ep(v, ytarget)
                    if e < 1:
                        t = []
                        if a > 0: t.append(("eta^" + str(a)) if a > 1 else "eta")
                        if b > 0: t.append(("theta4^" + str(b)) if b > 1 else "theta4")
                        if c > 0: t.append(("phi^" + str(c)) if c > 1 else "phi")
                        elif c < 0: t.append(("phibar^" + str(-c)) if c < -1 else "phibar")
                        dy.append((e, "*".join(t), v))
        # eta^a * theta4^b * sqrt5 * phi^c
        for a in range(0, 8):
            for b in range(0, 8):
                if a + b == 0: continue
                for c in range(-10, 10):
                    v = eta_val**a * t4**b * SQRT5 * PHI**c; e = ep(v, ytarget)
                    if e < 1:
                        t = []
                        if a > 0: t.append(("eta^" + str(a)) if a > 1 else "eta")
                        if b > 0: t.append(("theta4^" + str(b)) if b > 1 else "theta4")
                        t.append("sqrt5")
                        if c > 0: t.append(("phi^" + str(c)) if c > 1 else "phi")
                        elif c < 0: t.append(("phibar^" + str(-c)) if c < -1 else "phibar")
                        dy.append((e, "*".join(t), v))
        # eta^a * theta3^b * theta4^c * phi^d
        for a in range(0, 6):
            for b in range(0, 6):
                for c in range(0, 6):
                    if a+b+c == 0: continue
                    for d in range(-8, 12):
                        v = eta_val**a * t3**b * t4**c * PHI**d; e = ep(v, ytarget)
                        if e < 0.5:
                            t = []
                            if a > 0: t.append(("eta^" + str(a)) if a > 1 else "eta")
                            if b > 0: t.append(("theta3^" + str(b)) if b > 1 else "theta3")
                            if c > 0: t.append(("theta4^" + str(c)) if c > 1 else "theta4")
                            if d > 0: t.append(("phi^" + str(d)) if d > 1 else "phi")
                            elif d < 0: t.append(("phibar^" + str(-d)) if d < -1 else "phibar")
                            dy.append((e, "*".join(t), v))
        # phibar^k combos
        for k in range(20, 90):
            bs = PHIBAR**k
            for a in range(1, 8):
                for b in range(1, 8):
                    if a == b: continue
                    for n1, s1 in [("F", F), ("L", L)]:
                        for n2, s2 in [("F", F), ("L", L)]:
                            r = s1[a]/s2[b] if s2[b] != 0 else 0
                            if r > 0:
                                v = bs*r; e = ep(v, ytarget)
                                if e < 1: dy.append((e, "phibar^"+str(k)+"*"+n1+"("+str(a)+")/"+n2+"("+str(b)+")", v))
            for d in range(2, 50):
                v = bs/d; e = ep(v, ytarget)
                if e < 1: dy.append((e, "phibar^"+str(k)+"/"+str(d), v))
                v = bs*d; e = ep(v, ytarget)
                if e < 1: dy.append((e, str(d)+"*phibar^"+str(k), v))
        dy.sort(key=lambda x: x[0])
        if dy:
            seen = set(); cnt = 0
            print("  %-6s %-12s %-55s %-16s %-16s" % ("Rank", "Error%", "Formula", "Value", "Target"))
            print("  " + "-"*6 + " " + "-"*12 + " " + "-"*55 + " " + "-"*16 + " " + "-"*16)
            for er, fm, vl in dy:
                ky = round(vl, 18)
                if ky in seen: continue
                seen.add(ky); cnt += 1
                mk = " <<<" if er < 0.1 else (" **" if er < 0.5 else "")
                print("  %-6d %-12.6f %-55s %-16.6e %-16.6e%s" % (cnt, er, fm, vl, ytarget, mk))
                if cnt >= 20: break
        else:
            print("  No deep matches found.")
        print()

    # Summary
    print("=" * 95)
    print("SUMMARY: Best candidate for each quantity")
    print("=" * 95)
    print()
    for name, target in TARGETS.items():
        results = search(name, target)
        if results:
            best = results[0]
            if best[0] < 0.1: st = "CLOSED(<0.1%)"
            elif best[0] < 0.5: st = "CLOSED(<0.5%)"
            elif best[0] < 1.0: st = "CLOSED(<1%)"
            elif best[0] < 3.0: st = "IMPROVED"
            else: st = "OPEN"
            print("  %-10s  %-18s  %.4f%%  %s" % (name, st, best[0], best[1]))
        else:
            print("  %-10s  NO MATCH" % name)
    print()
    print("Done.")
