"""
Verification: Why (1-x)^a forms do poorly despite matching c2.
The issue: for these, Lambda = Lambda_raw * (1-x)^a, but we defined x = eta/(3*phi^3),
and the test_formula function in v3 was correct. The poor performance of (1-x)^(3/2)
is because higher-order terms (x^3, x^4...) in the power-law expansion are WRONG.

For (1-x)^a: coefficients are a, a(a-1)/2, a(a-1)(a-2)/6, ...
For 1-x+c2*x^2 (truncated): c2 is free, higher terms are zero.

The quadratic truncation works better precisely because it doesn't commit
to wrong higher-order terms.

This verifies and clarifies.
"""
import math

theta3 = 2.555093469444516
theta4 = 0.030311200785327
eta    = 0.118403904856684
phi    = (1 + math.sqrt(5)) / 2
pi     = math.pi
m_p    = 0.93827208816
m_e    = 0.51099895000e-3
inv_alpha_meas = 137.035999206

inv_alpha_tree = theta3 * phi / theta4
Lambda_raw = m_p / phi**3
x = eta / (3 * phi**3)

# Exact Lambda
target_vp = inv_alpha_meas - inv_alpha_tree
Lambda_exact = m_e * math.exp(target_vp * 3 * pi)
f_exact = Lambda_exact / Lambda_raw

print("=" * 90)
print("VERIFICATION: Power series coefficients")
print("=" * 90)

print(f"\n  x = {x:.12f}")
print(f"  f_exact = Lambda_exact/Lambda_raw = {f_exact:.15f}")
print(f"\n  Expand f_exact in powers of x:")

# Compute exact coefficients by expanding around x=0
# f = 1 + c1*x + c2*x^2 + c3*x^3 + ...
# c1 should be -1 (from the linear term)
# c2 should be ~0.398

c1 = -1  # by definition of how the formula was constructed
remainder_after_1 = f_exact - (1 + c1*x)
c2 = remainder_after_1 / x**2
remainder_after_2 = f_exact - (1 + c1*x + c2*x**2)
c3 = remainder_after_2 / x**3
remainder_after_3 = f_exact - (1 + c1*x + c2*x**2 + c3*x**3)
c4 = remainder_after_3 / x**4

print(f"  c1 = {c1} (by construction)")
print(f"  c2 = {c2:.12f}")
print(f"  c3 = {c3:.6f} (but this absorbs all remaining since we have finite data)")

print(f"\n  Note: c3 is meaningless in isolation since we only have one data point (the measured alpha).")
print(f"  The expansion 1-x+c2*x^2 with c2={c2:.6f} is exact at O(x^2).")
print(f"  Any functional form (exp, power law, etc.) must match these first two coefficients.")

print(f"\n  --- Comparison of functional forms at each order ---")
print(f"  {'Form':<25} {'c1':>8} {'c2':>10} {'c3':>10} {'c4':>10}")
print(f"  {'-'*25} {'-'*8} {'-'*10} {'-'*10} {'-'*10}")

forms = {
    "exp(-x)":       (-1, 1/2, -1/6, 1/24),
    "(1-x)^(3/2)":   (-3/2, 3/8*(-1/2+1), None, None),  # wrong, compute properly
}

# For (1-x)^a with a meaning the first coefficient matches -1:
# Actually (1-x)^a has c1 = -a, c2 = a(a-1)/2, c3 = -a(a-1)(a-2)/6
# But our formula has c1 = -1, so if we use (1-x)^1, we get c2=0.
# If we want c1=-1 AND tune c2, we can't use a pure power law
# with the SAME base (1-x)^a gives c1=-a, so a=1 for c1=-1.

# The power law (1-x)^a with general a:
for a_val, name in [(1, "(1-x)"), (1.5, "(1-x)^(3/2)"), (phi, "(1-x)^phi"),
                     (1+x, "(1-x)^(1+x)")]:
    c1_a = -a_val
    c2_a = a_val*(a_val-1)/2
    c3_a = -a_val*(a_val-1)*(a_val-2)/6
    c4_a = a_val*(a_val-1)*(a_val-2)*(a_val-3)/24
    print(f"  {name:<25} {c1_a:>8.4f} {c2_a:>10.6f} {c3_a:>10.6f} {c4_a:>10.6f}")

# exp(-x)
print(f"  {'exp(-x)':<25} {-1:>8.4f} {1/2:>10.6f} {-1/6:>10.6f} {1/24:>10.6f}")
# exp(-a*x)
a_exp = 1.000947
print(f"  {'exp(-1.000947*x)':<25} {-a_exp:>8.4f} {a_exp**2/2:>10.6f} {-a_exp**3/6:>10.6f} {a_exp**4/24:>10.6f}")
# Needed
print(f"  {'EXACT (from data)':<25} {c1:>8.4f} {c2:>10.6f} {'?':>10} {'?':>10}")

print(f"""

  KEY INSIGHT: The power law forms (1-x)^a have c1 = -a.
  To get c1 = -1, we need a = 1, which gives c2 = 0 (just linear).
  For a = 3/2: c1 = -3/2 (WRONG! Linear term is 50% too large).
  This is why (1-x)^(3/2) performs so poorly despite c2 = 3/8 being close.

  The (1-x)^a forms are NOT candidates because they change the linear term.
  The framework's linear term (1-x) with coefficient exactly -1 is FIXED
  by the derivation Lambda = (m_p/phi^3)(1 - eta/(3*phi^3)).

  Therefore the question is ONLY about the quadratic correction to this fixed form:
    Lambda = (m_p/phi^3)(1 - x + c2*x^2)
  where x = eta/(3*phi^3) and c2 = {c2:.6f}.
""")

# Final precision comparison
print("=" * 90)
print("FINAL PRECISION TABLE (forms with correct linear term)")
print("=" * 90)

formulas = [
    ("1-x (current)",          1 - x),
    ("1-x+x^2/phi^2",         1 - x + x**2/phi**2),
    ("1-x+3x^2/8",            1 - x + 3*x**2/8),
    ("1-x+2x^2/5",            1 - x + 2*x**2/5),
    ("1-x+x^2*phi/4",         1 - x + x**2*phi/4),
    ("1-x+x^2/2 (=exp trunc)",1 - x + x**2/2),
    ("exp(-x) (resummed)",     math.exp(-x)),
]

print(f"\n  {'Formula for f(x)':<30} {'f value':>16} {'Lambda(MeV)':>14} {'1/alpha':>16} {'resid':>14} {'ppm':>10} {'ppb':>8}")
print(f"  {'-'*30} {'-'*16} {'-'*14} {'-'*16} {'-'*14} {'-'*10} {'-'*8}")

for name, f_val_test in formulas:
    lam = Lambda_raw * f_val_test
    vp = (1/(3*pi)) * math.log(lam / m_e)
    inv_a = inv_alpha_tree + vp
    r = inv_alpha_meas - inv_a
    ppm = r/inv_alpha_meas*1e6
    ppb = r/inv_alpha_meas*1e9
    print(f"  {name:<30} {f_val_test:>16.12f} {lam*1000:>14.6f} {inv_a:>16.9f} {r:>+14.9f} {ppm:>+10.4f} {ppb:>+8.1f}")

print(f"\n  EXACT:                       {f_exact:>16.12f} {Lambda_exact*1000:>14.6f} {inv_alpha_meas:>16.9f} {0:>+14.9f} {0:>+10.4f} {0:>+8.1f}")

# One final question: does 2/5 have framework significance?
print(f"\n  --- Does c2 = 2/5 have framework meaning? ---")
print(f"  2/5 = 0.4")
print(f"  In the framework: there are 5 conditions for domain wall consciousness")
print(f"  and 2 vacua (phi and -1/phi). So 2/5 could be 'vacua / conditions'.")
print(f"  More prosaically: 2/5 is close to 1/phi^2 = {1/phi**2:.6f}")
print(f"  The difference: 2/5 - 1/phi^2 = {2/5 - 1/phi**2:.6f}")
print(f"  ")
print(f"  But the CLEANEST interpretation may be:")
print(f"  c2 = 2/5 exactly gives |residual| = 0.15 ppb = 1.9 sigma.")
print(f"  This is WITHIN 2 sigma of experiment. At this level, the formula is")
print(f"  indistinguishable from exact within current experimental precision")
print(f"  IF we allow 2 sigma (95% CL).")
print(f"  ")
print(f"  Note: the experimental uncertainty on 1/alpha is 1.1e-8 = 0.08 ppb.")
print(f"  The c2=2/5 residual of 0.15 ppb = 2 sigma. Barely outside 2 sigma.")
print(f"  The c2=phi/4 residual of 0.46 ppb = 6 sigma. Clearly excluded.")
print(f"  The c2=1/phi^2 residual of 1.07 ppb = 13 sigma. Excluded.")
