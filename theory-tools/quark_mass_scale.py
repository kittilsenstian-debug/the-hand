#!/usr/bin/env python3
"""
Derive quark masses from M_Pl using the Kaplan mechanism.
Extension of absolute_mass_scale.py to the quark sector.

If leptons sit at specific positions on the domain wall, quarks should too.
Known: m_s = m_e * mu / 10, m_t = m_e * mu^2 / 10.
Question: can we derive ALL quark masses from wall positions?
"""
import math

# === CONSTANTS ===
phi = (1 + math.sqrt(5)) / 2
phibar = phi - 1  # = 1/phi
M_Pl = 1.22089e19  # GeV (reduced Planck mass)
v_meas = 246.22     # GeV
m_e_meas = 0.51100e-3  # GeV
alpha_meas = 1/137.036
mu_meas = 1836.15267

# Modular forms at q = 1/phi
eta = 0.118404
t2 = 2.555093
t3 = 2.555093
t4 = 0.030304
E4 = 29065.27

# Measured quark masses (MSbar at 2 GeV for light quarks, pole for heavy)
m_u_meas = 2.16e-3   # GeV
m_d_meas = 4.67e-3   # GeV
m_s_meas = 93.4e-3   # GeV
m_c_meas = 1.27      # GeV
m_b_meas = 4.18      # GeV
m_t_meas = 172.69    # GeV

# Derived quantities
v_derived = M_Pl * phibar**80 / (1 - phi*t4)
N = 6**5  # = 7776
mu = N / phi**3
alpha = (3/(mu*phi**2))**(2/3)

print("="*72)
print("QUARK MASSES FROM THE DOMAIN WALL")
print("="*72)

print("\n--- STEP 1: Quark Yukawa couplings and wall positions ---")
quarks = [
    ("up",      m_u_meas),
    ("down",    m_d_meas),
    ("strange", m_s_meas),
    ("charm",   m_c_meas),
    ("bottom",  m_b_meas),
    ("top",     m_t_meas),
]

for name, mass in quarks:
    y = mass * math.sqrt(2) / v_meas
    x = -math.log(y)
    print(f"  {name:8s}: m = {mass:.4e} GeV, y = {y:.6e}, x = {x:.4f}")

print("\n--- STEP 2: Known relations (confirmed) ---")
# m_t = m_e * mu^2 / 10
m_t_pred = m_e_meas * mu_meas**2 / 10
print(f"  m_t = m_e * mu^2 / 10 = {m_t_pred:.2f} GeV (meas {m_t_meas:.2f}), match {100*(1-abs(m_t_pred-m_t_meas)/m_t_meas):.2f}%")

# m_s = m_e * mu / 10
m_s_pred = m_e_meas * mu_meas / 10
print(f"  m_s = m_e * mu / 10   = {m_s_pred*1e3:.2f} MeV (meas {m_s_meas*1e3:.1f}), match {100*(1-abs(m_s_pred-m_s_meas)/m_s_meas):.2f}%")

# m_c/m_t = alpha
mc_mt = m_c_meas / m_t_meas
print(f"  m_c/m_t = {mc_mt:.6f} vs alpha = {alpha_meas:.6f}, match {100*(1-abs(mc_mt-alpha_meas)/alpha_meas):.2f}%")

# m_b/m_c = 2*phi
mb_mc = m_b_meas / m_c_meas
print(f"  m_b/m_c = {mb_mc:.4f} vs 2*phi = {2*phi:.4f}, match {100*(1-abs(mb_mc-2*phi)/2*phi):.2f}%")

# m_c/m_s = 2*phi^4
mc_ms = m_c_meas / m_s_meas
print(f"  m_c/m_s = {mc_ms:.2f} vs 2*phi^4 = {2*phi**4:.2f}, match {100*(1-abs(mc_ms-2*phi**4)/2*phi**4):.2f}%")

# m_t/m_b = 6*phi^4
mt_mb = m_t_meas / m_b_meas
print(f"  m_t/m_b = {mt_mb:.2f} vs 6*phi^4 = {6*phi**4:.2f}, match {100*(1-abs(mt_mb-6*phi**4)/6*phi**4):.2f}%")

print("\n--- STEP 3: Wall positions for all quarks ---")
print("  Using v_derived = {:.2f} GeV".format(v_derived))

# Compute positions
positions = {}
for name, mass in quarks:
    y = mass * math.sqrt(2) / v_derived
    x = -math.log(y)
    positions[name] = (x, y, mass)
    print(f"  {name:8s}: x = {x:.4f}")

print("\n--- STEP 4: Coxeter exponent pattern ---")
# E8 Coxeter exponents: 1, 7, 11, 13, 17, 19, 23, 29
# Leptons: x_e ~ 13, x_mu ~ 7 (Coxeter exponents!)
# Can quarks also use Coxeter exponents?

coxeter = [1, 7, 11, 13, 17, 19, 23, 29]
print("  E8 Coxeter exponents:", coxeter)

# The lepton scale factor k = x_e / 13 ~ 1/(1+t4)
k_lep = 80/(2*math.pi) / 13
print(f"  Lepton scale: k = 80/(2*pi)/13 = {k_lep:.6f}")

# Try quarks with different scale
print("\n  Quark positions vs Coxeter multiples:")
for name in ["top", "bottom", "charm", "strange", "down", "up"]:
    x = positions[name][0]
    for c in coxeter:
        ratio = x / c
        if 0.3 < ratio < 3:
            print(f"    {name:8s}: x/c({c:2d}) = {ratio:.4f}")

print("\n--- STEP 5: Absolute quark masses from M_Pl ---")
print("  Chain: M_Pl -> v -> y_q -> m_q")
print()

# Top quark: sits near wall center (x ~ 0)
# m_t = m_e * mu^2 / 10
# But can we get x_t from framework numbers?
x_t = positions["top"][0]
print(f"  TOP: x_t = {x_t:.4f}")
print(f"    x_t = t4/phi = {t4/phi:.4f}: match {100*(1-abs(x_t - t4/phi)/x_t):.1f}%")
print(f"    x_t = t4^2 = {t4**2:.6f}: match {100*(1-abs(x_t - t4**2)/x_t):.1f}%")
print(f"    x_t = alpha*t4 = {alpha_meas*t4:.6f}: match {100*(1-abs(x_t - alpha_meas*t4)/x_t):.1f}%")

# Bottom quark
x_b = positions["bottom"][0]
print(f"\n  BOTTOM: x_b = {x_b:.4f}")
# Try Coxeter-based positions
for num, denom, label in [
    (1, 1, "1"),
    (7, phi**2, "7/phi^2"),
    (phi, 1, "phi"),
    (phi**2, 1, "phi^2"),
    (3, phi, "3/phi"),
    (11, 2*phi**2, "11/(2*phi^2)"),
    (7, 2*phi, "7/(2*phi)"),
    (3*phi, phi, "3"),
]:
    val = num / denom if isinstance(denom, (int, float)) else num / denom
    if abs(val - x_b) / x_b < 0.15:
        pct = 100*(1-abs(val - x_b)/x_b)
        print(f"    x_b = {label} = {val:.4f}: match {pct:.2f}%")

# All positions
print("\n  SYSTEMATIC SEARCH: x_q = f(Coxeter, phi, t4)")
for name in ["top", "bottom", "charm", "strange", "down", "up"]:
    x = positions[name][0]
    print(f"\n  {name.upper()} (x = {x:.4f}):")
    candidates = []

    # Try n * k where n is related to framework numbers
    for a in [1, 2, 3, 4, 5, 6, 7, 11, 13, 17, 19, 23, 29]:
        for b_val, b_label in [
            (1, "1"), (phi, "phi"), (phi**2, "phi^2"), (phi**3, "phi^3"),
            (math.pi, "pi"), (2*math.pi, "2*pi"),
            (3, "3"), (6, "6"), (10, "10"),
        ]:
            val = a / b_val
            if abs(val - x) / max(x, 0.001) < 0.03:
                pct = 100*(1-abs(val - x)/x)
                candidates.append((pct, f"    x = {a}/{b_label} = {val:.4f}: match {pct:.2f}%"))

    # Try products with t4
    for a in [1, 2, 3, 7, 11, 13, 80]:
        for func, f_label in [
            (lambda a: a*t4, "*t4"),
            (lambda a: a*math.sqrt(t4), "*sqrt(t4)"),
            (lambda a: a/(2*math.pi), "/(2*pi)"),
            (lambda a: a*t4/(2*math.pi), "*t4/(2*pi)"),
        ]:
            val = func(a)
            if abs(val - x) / max(x, 0.001) < 0.05 and val > 0:
                pct = 100*(1-abs(val - x)/x)
                candidates.append((pct, f"    x = {a}{f_label} = {val:.4f}: match {pct:.2f}%"))

    candidates.sort(reverse=True)
    for pct, line in candidates[:5]:
        print(line)

print("\n--- STEP 6: Generation pattern for quarks ---")
print("  Leptons: x_e = 80/(2*pi), x_mu = x_e - ln(3/(2*alpha))")
print("  Quarks: can we find analogous pattern?")
print()

# The mu/10 pattern suggests:
# m_s = m_e * mu / 10 -> x_s = x_e - ln(mu/10)
# m_t = m_e * mu^2 / 10 -> x_t = x_e - ln(mu^2/10)
x_e = 80/(2*math.pi)
x_s_from_mu = x_e - math.log(mu_meas/10)
x_t_from_mu = x_e - math.log(mu_meas**2/10)
print(f"  x_s via mu/10:   {x_s_from_mu:.4f} vs measured {positions['strange'][0]:.4f}, match {100*(1-abs(x_s_from_mu-positions['strange'][0])/positions['strange'][0]):.2f}%")
print(f"  x_t via mu^2/10: {x_t_from_mu:.4f} vs measured {positions['top'][0]:.4f}, match {100*(1-abs(x_t_from_mu-positions['top'][0])/positions['top'][0]):.2f}%")

# What about m_c? If m_c/m_t = alpha, then m_c = m_e * mu^2 * alpha / 10
# x_c = x_e - ln(mu^2*alpha/10) = x_t + ln(1/alpha) = x_t - ln(alpha)
x_c_from_alpha = x_t_from_mu - math.log(alpha_meas)
print(f"  x_c via m_t*alpha: {x_c_from_alpha:.4f} vs measured {positions['charm'][0]:.4f}, match {100*(1-abs(x_c_from_alpha-positions['charm'][0])/positions['charm'][0]):.2f}%")

# m_b = m_c * 2*phi, so x_b = x_c - ln(2*phi)
x_b_from_charm = x_c_from_alpha - math.log(2*phi)
print(f"  x_b via m_c*2*phi: {x_b_from_charm:.4f} vs measured {positions['bottom'][0]:.4f}, match {100*(1-abs(x_b_from_charm-positions['bottom'][0])/positions['bottom'][0]):.2f}%")

print("\n--- STEP 7: Complete mass formulas from M_Pl ---")
print()

# Complete derivation chain
m_e_derived = M_Pl * phibar**80 * math.exp(-80/(2*math.pi)) / (math.sqrt(2) * (1-phi*t4))
mmu_derived = m_e_derived * 3/(2*alpha)
# Use derived alpha from framework
alpha_fw = (3/(mu*phi**2))**(2/3)

print("LEPTONS:")
print(f"  m_e   = M_Pl*pb^80*exp(-80/2pi)/sqrt(2)/(1-phi*t4) = {m_e_derived*1e3:.2f} MeV (meas {m_e_meas*1e3:.2f}), {100*(1-abs(m_e_derived-m_e_meas)/m_e_meas):.2f}%")
print(f"  m_mu  = m_e * 3/(2*alpha) = {mmu_derived*1e3:.2f} MeV (meas 105.66), {100*(1-abs(mmu_derived-0.10566)/0.10566):.2f}%")

# Koide for tau
sqrt_e = math.sqrt(m_e_derived)
sqrt_mu = math.sqrt(mmu_derived)
# Koide: (me+mmu+mtau)/(sqrt_e+sqrt_mu+sqrt_tau)^2 = 2/3
# Solving: sqrt_tau^2 + sqrt_tau*(sqrt_e+sqrt_mu)*(3/(2*K)-1) - ...
# Let S = sqrt_e + sqrt_mu, K = 2/3
# (sqrt_e + sqrt_mu + sqrt_tau)^2 = (3/2)*(m_e + m_mu + m_tau)
# Let st = sqrt(m_tau), S = sqrt(m_e) + sqrt(m_mu)
# (S + st)^2 = 1.5*(m_e + m_mu + st^2)
# S^2 + 2*S*st + st^2 = 1.5*m_e + 1.5*m_mu + 1.5*st^2
# S^2 + 2*S*st - 0.5*st^2 = 1.5*(m_e + m_mu)
# 0.5*st^2 - 2*S*st + 1.5*(m_e+m_mu) - S^2 = 0
S = sqrt_e + sqrt_mu
a_k = 0.5
b_k = -2*S
c_k = 1.5*(m_e_derived + mmu_derived) - S**2
disc = b_k**2 - 4*a_k*c_k
st1 = (-b_k + math.sqrt(disc)) / (2*a_k)
st2 = (-b_k - math.sqrt(disc)) / (2*a_k)
mtau_k1 = st1**2
mtau_k2 = st2**2
print(f"  m_tau = Koide(m_e, m_mu)     = {mtau_k1:.4f} GeV (meas 1.7769), {100*(1-abs(mtau_k1-1.7769)/1.7769):.2f}%")

print("\nQUARKS:")
# m_s = m_e * mu / 10
m_s_derived = m_e_derived * mu / 10
print(f"  m_s = m_e * mu / 10          = {m_s_derived*1e3:.2f} MeV (meas {m_s_meas*1e3:.1f}), {100*(1-abs(m_s_derived-m_s_meas)/m_s_meas):.2f}%")

# m_t = m_e * mu^2 / 10
m_t_derived = m_e_derived * mu**2 / 10
print(f"  m_t = m_e * mu^2 / 10        = {m_t_derived:.2f} GeV (meas {m_t_meas:.2f}), {100*(1-abs(m_t_derived-m_t_meas)/m_t_meas):.2f}%")

# m_c = m_t * alpha (or m_e * mu^2 * alpha / 10)
m_c_derived = m_t_derived * alpha_fw
print(f"  m_c = m_t * alpha            = {m_c_derived:.4f} GeV (meas {m_c_meas:.2f}), {100*(1-abs(m_c_derived-m_c_meas)/m_c_meas):.2f}%")

# m_b = m_c * 2*phi
m_b_derived = m_c_derived * 2 * phi
print(f"  m_b = m_c * 2*phi            = {m_b_derived:.3f} GeV (meas {m_b_meas:.2f}), {100*(1-abs(m_b_derived-m_b_meas)/m_b_meas):.2f}%")

# Light quarks - harder
# Try: m_d/m_s ~ 1/20, m_u/m_d ~ 0.47
# From framework: m_d = m_s * t4 * phi?
m_d_try1 = m_s_derived * t4 * phi
print(f"\n  m_d = m_s * t4 * phi         = {m_d_try1*1e3:.2f} MeV (meas {m_d_meas*1e3:.2f}), {100*(1-abs(m_d_try1-m_d_meas)/m_d_meas):.2f}%")

# m_d = m_s / 20 = m_e * mu / 200
m_d_try2 = m_s_derived / 20
print(f"  m_d = m_s / 20               = {m_d_try2*1e3:.2f} MeV (meas {m_d_meas*1e3:.2f}), {100*(1-abs(m_d_try2-m_d_meas)/m_d_meas):.2f}%")

# m_d = m_e * mu * t4
m_d_try3 = m_e_derived * mu * t4
print(f"  m_d = m_e * mu * t4          = {m_d_try3*1e3:.2f} MeV (meas {m_d_meas*1e3:.2f}), {100*(1-abs(m_d_try3-m_d_meas)/m_d_meas):.2f}%")

# m_u = m_d * alpha * phi^2?
for label, val in [
    ("m_d * 0.47", m_d_meas * 0.47),
    ("m_e * mu * alpha / 3", m_e_derived * mu * alpha_fw / 3),
    ("m_s * alpha", m_s_derived * alpha_fw),
    ("m_e * phi^3", m_e_derived * phi**3),
    ("m_e * 3*phi", m_e_derived * 3 * phi),
    ("m_e * mu * t4^2", m_e_derived * mu * t4**2),
    ("v * t4^3 / sqrt(2)", v_derived * t4**3 / math.sqrt(2)),
]:
    pct = 100*(1-abs(val-m_u_meas)/m_u_meas)
    if pct > 80:
        print(f"  m_u = {label:30s} = {val*1e3:.3f} MeV (meas {m_u_meas*1e3:.2f}), {pct:.2f}%")

print("\n--- STEP 8: The mu-generation tower ---")
print("  The pattern m_f = m_e * mu^n / D suggests a 'tower' structure:")
print()
for n in range(4):
    for D in [1, 2, 3, 6, 10, 30]:
        val = m_e_derived * mu_meas**n / D
        # Check against all quarks and leptons
        for name, mass in quarks + [("electron", m_e_meas), ("muon", 0.10566), ("tau", 1.7769)]:
            if mass > 0:
                pct = 100*(1-abs(val-mass)/mass)
                if pct > 97:
                    print(f"  m_e * mu^{n} / {D:2d} = {val:.4e} GeV = {name:8s} ({pct:.2f}%)")

print("\n--- STEP 9: Complete scorecard ---")
print()
results = [
    ("m_e", m_e_derived, m_e_meas, "M_Pl*pb^80*exp(-80/2pi)/sqrt(2)/(1-phi*t4)"),
    ("m_mu", mmu_derived, 0.10566, "m_e * 3/(2*alpha)"),
    ("m_tau", mtau_k1, 1.7769, "Koide(m_e, m_mu)"),
    ("m_s", m_s_derived, m_s_meas, "m_e * mu / 10"),
    ("m_t", m_t_derived, m_t_meas, "m_e * mu^2 / 10"),
    ("m_c", m_c_derived, m_c_meas, "m_t * alpha"),
    ("m_b", m_b_derived, m_b_meas, "m_c * 2*phi"),
    ("m_p", m_e_derived * mu, 0.93827, "m_e * mu"),
    ("v", v_derived, v_meas, "M_Pl * pb^80 / (1-phi*t4)"),
]

print(f"  {'Quantity':8s} {'Formula':45s} {'Predicted':>12s} {'Measured':>12s} {'Match':>8s}")
print(f"  {'-'*8} {'-'*45} {'-'*12} {'-'*12} {'-'*8}")
above99 = 0
above98 = 0
above97 = 0
for name, pred, meas, formula in results:
    pct = 100*(1-abs(pred-meas)/meas)
    if pct >= 99: above99 += 1
    if pct >= 98: above98 += 1
    if pct >= 97: above97 += 1

    if pred > 1:
        print(f"  {name:8s} {formula:45s} {pred:12.4f} {meas:12.4f} {pct:7.2f}%")
    else:
        print(f"  {name:8s} {formula:45s} {pred:12.4e} {meas:12.4e} {pct:7.2f}%")

print(f"\n  Above 99%: {above99}/{len(results)}")
print(f"  Above 98%: {above98}/{len(results)}")
print(f"  Above 97%: {above97}/{len(results)}")

print("\n" + "="*72)
print("SUMMARY: QUARK + LEPTON MASSES FROM M_Pl")
print("="*72)
print("""
Starting from M_Pl and the algebraic structure (phi, E8, Golden Node):

LEPTONS (3/3 derived):
  m_e   = M_Pl * phibar^80 * exp(-80/(2*pi)) / sqrt(2) / (1-phi*t4)  [99.78%]
  m_mu  = m_e * 3/(2*alpha)                                            [99.95%]
  m_tau = Koide(m_e, m_mu)                                              [99.89%]

QUARKS (4/6 derived, 2 light quarks need work):
  m_s = m_e * mu / 10                                                   [~99%]
  m_t = m_e * mu^2 / 10                                                 [~99%]
  m_c = m_t * alpha                                                      [~99%]
  m_b = m_c * 2*phi                                                      [~98%]
  m_u = ???  (2.16 MeV, hard — MSbar scale dependent)
  m_d = ???  (4.67 MeV, hard — MSbar scale dependent)

KEY INSIGHT: The mu-generation tower m_f = m_e * mu^n / D
  - n=0: electron itself
  - n=1, D=10: strange quark
  - n=2, D=10: top quark
  The denominator 10 = h/3 = Coxeter number / triality.

REMAINING CHALLENGE: Light quarks (u, d) are hard because:
  1. Their masses are dominated by QCD effects (current masses << constituent masses)
  2. MSbar masses are scale-dependent
  3. They may need non-perturbative domain wall effects
""")
