#!/usr/bin/env python3
"""
mu_correction_analysis.py
Explores corrections to mu_0 = 6^5 / phi^3 to close the 27-sigma gap
to the measured proton-to-electron mass ratio.

Framework elements: {mu, phi, 3, 2/3}
Core identity: alpha^(3/2) * mu * phi^2 = 3
"""

import math
from itertools import product as iterproduct

phi = (1 + math.sqrt(5)) / 2
alpha = 1 / 137.035999084
mu_measured = 1836.15267343
mu_measured_unc = 0.00000011
mu_0 = 6**5 / phi**3
delta = mu_measured - mu_0
SEP = '=' * 72

print(SEP)
print('  SECTION 1: THE GAP')
print(SEP)
print()
print(f'  phi            = {phi:.15f}')
print(f'  phi^3          = {phi**3:.15f}')
print(f'  6^5            = {6**5}')
print(f'  mu_0 = 6^5/phi^3 = {mu_0:.10f}')
print(f'  mu_measured      = {mu_measured:.10f}')
print(f'  mu_uncertainty   = {mu_measured_unc:.11f}')
print()
print(f'  delta = mu_meas - mu_0 = {delta:.10f}')
print(f'  Relative gap:  delta/mu_0 = {delta/mu_0:.8e} = {delta/mu_0*100:.6f}%')
print(f'  Gap in sigma:  {delta / mu_measured_unc:.1f} sigma')
print()
print('  Delta expressed as framework quantities:')
print(f'    delta                       = {delta:.10f}')
print(f'    1/2                         = {0.5:.10f}   (ratio: {delta/0.5:.8f})')
print(f'    phi/3                       = {phi/3:.10f}   (ratio: {delta/(phi/3):.8f})')
print(f'    sqrt(5)/phi^2               = {math.sqrt(5)/phi**2:.10f}   (ratio: {delta/(math.sqrt(5)/phi**2):.8f})')
print(f'    1/phi                       = {1/phi:.10f}   (ratio: {delta/(1/phi):.8f})')
print(f'    alpha * mu_0                = {alpha*mu_0:.10f}   (ratio: {delta/(alpha*mu_0):.8f})')
print(f'    3*alpha*mu_0/(4*pi)         = {3*alpha*mu_0/(4*math.pi):.10f}   (ratio: {delta/(3*alpha*mu_0/(4*math.pi)):.8f})')
print()
# SECTION 2: SYSTEMATIC SEARCH
print(SEP)
print('  SECTION 2: SYSTEMATIC SEARCH')
print('  mu = mu_0 * (1 + f(alpha, phi, 3, 2/3))')
print(SEP)
print()

results = []
alpha_powers = {
    'alpha': alpha, 'alpha^2': alpha**2, 'alpha^(1/2)': alpha**0.5,
    'alpha^(3/2)': alpha**(3/2), 'alpha^(2/3)': alpha**(2/3), 'alpha^(1/3)': alpha**(1/3),
}
multipliers = {
    '1': 1, 'phi': phi, '1/phi': 1/phi, 'phi^2': phi**2, '1/phi^2': 1/phi**2,
    '3': 3, '1/3': 1/3, '2/3': 2/3, '2': 2, '1/2': 0.5,
    '2*pi': 2*math.pi, '1/(2*pi)': 1/(2*math.pi), 'pi': math.pi, '1/pi': 1/math.pi,
    'sqrt(5)': math.sqrt(5), '3/phi': 3/phi, 'phi/3': phi/3, '3*phi': 3*phi,
}

for (ap_name, ap_val), (m_name, m_val) in iterproduct(alpha_powers.items(), multipliers.items()):
    f_val = ap_val * m_val
    mu_test = mu_0 * (1 + f_val)
    residual = abs(mu_test - mu_measured)
    label = f'{ap_name} * {m_name}' if m_name != '1' else ap_name
    results.append((label, f_val, mu_test, residual, residual/mu_measured_unc))

for n in range(1, 6):
    val = n / 27
    mu_test = mu_0 * (1 + val)
    residual = abs(mu_test - mu_measured)
    results.append((f'{n}/27', val, mu_test, residual, residual/mu_measured_unc))

for n in range(1, 10):
    val = alpha / n
    mu_test = mu_0 * (1 + val)
    residual = abs(mu_test - mu_measured)
    results.append((f'alpha/{n}', val, mu_test, residual, residual/mu_measured_unc))

additive_results = []
add_cands = {
    '1/2': 0.5, 'phi/3': phi/3, '1/phi': 1/phi, 'phi^2/3': phi**2/3,
    'sqrt(5)/phi^2': math.sqrt(5)/phi**2, '1/3': 1/3, '2/3': 2/3,
    'phi - 1': phi - 1, '3 - phi^2': 3 - phi**2,
    'alpha*mu_0': alpha * mu_0, '3*alpha*mu_0/(4*pi)': 3*alpha*mu_0/(4*math.pi),
}
for name, val in add_cands.items():
    mu_test = mu_0 + val
    residual = abs(mu_test - mu_measured)
    additive_results.append((f'mu_0 + {name}', val, mu_test, residual, residual/mu_measured_unc))

results.sort(key=lambda x: x[3])
print('  --- Top 20 multiplicative corrections: mu = mu_0 * (1 + f) ---')
hdr = '  %-30s %-16s %-16s %-14s %-10s' % ('Correction f', 'f value', 'mu_predicted', 'residual', 'sigma')
print(hdr)
print('  ' + '-' * 86)
for label, f_val, mu_test, residual, sigma in results[:20]:
    marker = ' <<<' if sigma < 10 else ''
    print(f'  {label:<30} {f_val:<16.10e} {mu_test:<16.8f} {residual:<14.8e} {sigma:<10.1f}{marker}')
print()

additive_results.sort(key=lambda x: x[3])
print('  --- Additive corrections: mu = mu_0 + f ---')
hdr2 = '  %-35s %-14s %-16s %-14s %-10s' % ('Correction', 'f value', 'mu_predicted', 'residual', 'sigma')
print(hdr2)
print('  ' + '-' * 89)
for label, f_val, mu_test, residual, sigma in additive_results:
    marker = ' <<<' if sigma < 100 else ''
    print(f'  {label:<35} {f_val:<14.8f} {mu_test:<16.8f} {residual:<14.8e} {sigma:<10.1f}{marker}')
print()
# SECTION 3: SELF-CONSISTENT CORRECTION
print(SEP)
print('  SECTION 3: SELF-CONSISTENT CORRECTION')
print('  If alpha^(3/2) * mu * phi^2 = 3 is exact, then')
print('  mu_exact = 3 / (alpha^(3/2) * phi^2)')
print(SEP)
print()

mu_from_identity = 3 / (alpha**(3/2) * phi**2)
identity_delta = mu_measured - mu_from_identity
identity_check = alpha**(3/2) * mu_measured * phi**2

print(f'  alpha^(3/2) * mu_measured * phi^2 = {identity_check:.10f}')
print(f'  (Should be 3 if identity is exact)')
print(f'  Deviation from 3: {identity_check - 3:.10e} = {(identity_check-3)/3*100:.6f}%')
print()
print(f'  mu_from_identity = 3/(alpha^(3/2)*phi^2) = {mu_from_identity:.10f}')
print(f'  mu_measured                               = {mu_measured:.10f}')
print(f'  mu_0 = 6^5/phi^3                          = {mu_0:.10f}')
print()
print(f'  Gap identity vs measured:  {identity_delta:.10f} = {abs(identity_delta)/mu_measured_unc:.1f} sigma')
print(f'  Gap mu_0 vs measured:      {delta:.10f} = {abs(delta)/mu_measured_unc:.1f} sigma')
print()

if abs(identity_delta) < abs(delta):
    print('  ==> The core identity mu = 3/(alpha^(3/2)*phi^2) is CLOSER to measurement')
    print(f'      by a factor of {abs(delta)/abs(identity_delta):.2f}')
else:
    print('  ==> The formula mu_0 = 6^5/phi^3 is CLOSER to measurement')
    print(f'      by a factor of {abs(identity_delta)/abs(delta):.2f}')
print()

correction_identity = mu_from_identity / mu_0 - 1
print(f'  If identity is exact: mu_identity/mu_0 - 1 = {correction_identity:.10e}')
print(f'  Compare alpha         = {alpha:.10e}')
print(f'  Compare alpha/2       = {alpha/2:.10e}')
print(f'  Compare alpha*phi/3   = {alpha*phi/3:.10e}')
print(f'  Compare 2*alpha/(3)   = {2*alpha/3:.10e}')
print(f'  Ratio (correction/alpha) = {correction_identity/alpha:.8f}')
print()
# SECTION 4: IS THE GAP ITSELF A FRAMEWORK QUANTITY?
print(SEP)
print('  SECTION 4: IS THE GAP ITSELF A FRAMEWORK QUANTITY?')
print(f'  delta = {delta:.10f}')
print(SEP)
print()

gap_candidates = {}
for a_exp in [-2, -1, -0.5, 0, 0.5, 1, 2]:
    for phi_exp in [-3, -2, -1, 0, 1, 2, 3]:
        for three_exp in [-2, -1, 0, 1, 2]:
            val = (alpha**a_exp if a_exp != 0 else 1) * (phi**phi_exp) * (3**three_exp)
            if 0.01 < abs(val) < 100:
                name = ''
                if a_exp != 0: name += f'alpha^{a_exp} * '
                if phi_exp != 0: name += f'phi^{phi_exp} * '
                if three_exp != 0: name += f'3^{three_exp} * '
                name = name.rstrip(' * ') if name else '1'
                ratio = delta / val
                gap_candidates[name] = (val, ratio, abs(ratio - round(ratio)))

print('  Candidates where delta/f is close to a simple integer:')
hdr3 = '  %-40s %-14s %-14s %-12s %-12s' % ('Expression', 'Value', 'delta/f', 'Nearest int', 'Frac err')
print(hdr3)
print('  ' + '-' * 92)
sorted_gaps = sorted(gap_candidates.items(), key=lambda x: x[1][2])
count = 0
for name, (val, ratio, frac_err) in sorted_gaps:
    if frac_err < 0.05 and count < 25:
        nearest = round(ratio)
        if nearest != 0:
            print(f'  {name:<40} {val:<14.8f} {ratio:<14.8f} {nearest:<12d} {frac_err:<12.8f}')
            count += 1

print()
print('  Candidates where delta/f is close to 1/n (n=2..12):')
found_any = False
for name, (val, ratio, _) in gap_candidates.items():
    for n in range(2, 13):
        if abs(ratio - 1/n) < 0.01:
            print(f'  {name:<40} delta/f = {ratio:.8f} ~ 1/{n} (err = {abs(ratio - 1/n):.6e})')
            found_any = True
if not found_any:
    print('  (None found with < 1% error)')
print()
# SECTION 5: RADIATIVE / QED CORRECTION PERSPECTIVE
print(SEP)
print('  SECTION 5: RADIATIVE / QED CORRECTION PERSPECTIVE')
print(SEP)
print()

ln_mu = math.log(mu_measured)
qed_1 = 3 * alpha / (4 * math.pi) * ln_mu
qed_2 = alpha / math.pi
qed_3 = alpha / (2 * math.pi) * ln_mu
qed_4 = 3 * alpha / (4 * math.pi)

print(f'  ln(mu) = {ln_mu:.8f}')
print(f'  Measured relative gap: delta/mu_0 = {delta/mu_0:.10e}')
print()
print('  Various QED-like corrections (relative):')
print(f'    3*alpha/(4*pi) * ln(mu)   = {qed_1:.10e}  (ratio to gap: {qed_1/(delta/mu_0):.4f})')
print(f'    alpha/pi                  = {qed_2:.10e}  (ratio to gap: {qed_2/(delta/mu_0):.4f})')
print(f'    alpha/(2*pi) * ln(mu)     = {qed_3:.10e}  (ratio to gap: {qed_3/(delta/mu_0):.4f})')
print(f'    3*alpha/(4*pi)            = {qed_4:.10e}  (ratio to gap: {qed_4/(delta/mu_0):.4f})')
print(f'    alpha * phi / (2*pi)      = {alpha*phi/(2*math.pi):.10e}  (ratio to gap: {alpha*phi/(2*math.pi)/(delta/mu_0):.4f})')
print()

x_alpha = delta / (mu_0 * alpha)
print(f'  If delta/mu_0 = x * alpha, then x = {x_alpha:.10f}')
print('  This should be a simple function of phi and 3:')
combos = {
    '1/phi^2': 1/phi**2, '1/3': 1/3, '1/(3*phi)': 1/(3*phi),
    'phi/3': phi/3, '1/(phi*sqrt(3))': 1/(phi*math.sqrt(3)),
    'ln(phi)/pi': math.log(phi)/(math.pi), '3/(4*pi)': 3/(4*math.pi),
    'phi/(4*pi)': phi/(4*math.pi), 'sqrt(phi)/3': math.sqrt(phi)/3,
    'phi^2/(3*pi)': phi**2/(3*math.pi), '1/(2*phi)': 1/(2*phi),
    'sqrt(5)/(4*pi)': math.sqrt(5)/(4*math.pi), '1/phi^3': 1/phi**3,
    '2/(3*phi^2)': 2/(3*phi**2), '2/(3*pi)': 2/(3*math.pi),
}
hdr4 = '  %-25s %-16s %-16s' % ('Expression', 'Value', 'Ratio (corr/alpha)/expr')
print(hdr4)
print('  ' + '-' * 57)
for name, val in sorted(combos.items(), key=lambda x: abs(x_alpha/x[1] - 1)):
    r = x_alpha / val
    if abs(r - 1) < 0.3:
        marker = '<<<' if abs(r-1) < 0.05 else ''
        print(f'  {name:<25} {val:<16.10f} {r:<16.10f} {marker}')
print()

print(f'  Absolute QED-like corrections (compare to delta = {delta:.6f}):')
abs_corrs = {
    '3*alpha*mu_0/(4*pi)*ln(mu)': 3*alpha*mu_0/(4*math.pi)*ln_mu,
    'alpha*mu_0/pi': alpha*mu_0/math.pi,
    'alpha*mu_0/(2*pi)*ln(mu)': alpha*mu_0/(2*math.pi)*ln_mu,
    'alpha*mu_0*phi/(2*pi)': alpha*mu_0*phi/(2*math.pi),
    'alpha*mu_0/(3*phi)': alpha*mu_0/(3*phi),
    'alpha*mu_0/3': alpha*mu_0/3,
    'alpha*mu_0*phi/3': alpha*mu_0*phi/3,
    'alpha^2*mu_0*ln(mu)^2': alpha**2*mu_0*ln_mu**2,
}
for name, val in sorted(abs_corrs.items(), key=lambda x: abs(x[1] - delta)):
    print(f'    {name:<35} = {val:<14.8f}  (ratio to delta: {val/delta:.6f})')
print()
# SECTION 6: LUCAS NUMBER CONNECTION
print(SEP)
print('  SECTION 6: LUCAS NUMBER CONNECTION')
print('  mu = 6^5/phi^3 + f(Lucas numbers)')
print(SEP)
print()

def lucas(n):
    if n == 0: return 2
    if n == 1: return 1
    a, b = 2, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

lucas_nums = {n: lucas(n) for n in range(0, 15)}
print('  Lucas numbers: ', {n: lucas_nums[n] for n in range(11)})
print(f'  delta = {delta:.10f}')
print()

lucas_results = []
for n in range(0, 12):
    for m in range(1, 12):
        if n != m:
            val = lucas_nums[n] / lucas_nums[m]
            mu_test = mu_0 + val
            residual = abs(mu_test - mu_measured)
            sigma = residual / mu_measured_unc
            lucas_results.append((f'L({n})/L({m})', val, mu_test, residual, sigma))

for n in range(0, 10):
    for k in range(-4, 5):
        val = lucas_nums[n] * phi**k
        mu_test = mu_0 + val
        residual = abs(mu_test - mu_measured)
        sigma = residual / mu_measured_unc
        lucas_results.append((f'L({n})*phi^{k}', val, mu_test, residual, sigma))

for n in range(0, 10):
    val = lucas_nums[n] * alpha * mu_0
    mu_test = mu_0 + val
    residual = abs(mu_test - mu_measured)
    sigma = residual / mu_measured_unc
    lucas_results.append((f'L({n})*alpha*mu_0', val, mu_test, residual, sigma))

for n in range(0, 10):
    for m in range(-3, 4):
        for k in range(-2, 3):
            val = lucas_nums[n] / (phi**m * 3**k)
            if 0.01 < val < 10:
                mu_test = mu_0 + val
                residual = abs(mu_test - mu_measured)
                sigma = residual / mu_measured_unc
                lucas_results.append((f'L({n})/(phi^{m}*3^{k})', val, mu_test, residual, sigma))

lucas_results.sort(key=lambda x: x[3])
print('  --- Top 15 Lucas-based additive corrections ---')
hdr5 = '  %-25s %-14s %-16s %-14s %-10s' % ('Formula', 'Value', 'mu_predicted', 'residual', 'sigma')
print(hdr5)
print('  ' + '-' * 79)
for label, val, mu_test, residual, sigma in lucas_results[:15]:
    marker = ' <<<' if sigma < 100 else ''
    print(f'  {label:<25} {val:<14.8f} {mu_test:<16.8f} {residual:<14.8e} {sigma:<10.1f}{marker}')
print()
# SECTION 7: TOP 5 OVERALL
print(SEP)
print('  SECTION 7: TOP 5 BEST CORRECTIONS OVERALL')
print(SEP)
print()

all_results = []
for label, f_val, mu_test, residual, sigma in results:
    all_results.append((f'mu_0*(1 + {label})', mu_test, residual, sigma))
for label, f_val, mu_test, residual, sigma in additive_results:
    all_results.append((label, mu_test, residual, sigma))
all_results.append(('3/(alpha^(3/2)*phi^2) [identity]', mu_from_identity,
                     abs(mu_from_identity - mu_measured),
                     abs(mu_from_identity - mu_measured)/mu_measured_unc))
for label, val, mu_test, residual, sigma in lucas_results:
    all_results.append((f'mu_0 + {label}', mu_test, residual, sigma))

all_results.sort(key=lambda x: x[2])
filtered = []
for item in all_results:
    is_dup = False
    for existing in filtered:
        if abs(item[1] - existing[1]) < 1e-10:
            is_dup = True
            break
    if not is_dup:
        filtered.append(item)

hdr6 = '  %-4s %-55s %-18s %-16s %-10s' % ('#', 'Formula', 'mu_predicted', 'residual', 'sigma')
print(hdr6)
print('  ' + '-' * 103)
for i, (label, mu_test, residual, sigma) in enumerate(filtered[:10]):
    print(f'  {i+1:<4d} {label:<55} {mu_test:<18.10f} {residual:<16.10e} {sigma:<10.1f}')
print()
# SECTION 8: DEEPER ANALYSIS
print(SEP)
print('  SECTION 8: DEEPER ANALYSIS OF BEST CANDIDATES')
print(SEP)
print()

print('  --- Core identity: alpha^(3/2) * mu * phi^2 = 3 ---')
print(f'  mu_identity = {mu_from_identity:.12f}')
print(f'  mu_measured = {mu_measured:.12f}')
print(f'  The identity gives mu to within {abs(mu_from_identity - mu_measured)/mu_measured*100:.4f}%')
print(f'  ({abs(mu_from_identity - mu_measured)/mu_measured_unc:.1f} sigma)')
print()

print('  --- Combining: mu = 6^5/phi^3 requires correction ---')
correction_needed = delta / mu_0
print(f'  Required relative correction: {correction_needed:.12e}')
print()

ratio_to_alpha = correction_needed / alpha
print(f'  correction / alpha = {ratio_to_alpha:.10f}')
print('  This should be a simple function of phi and 3:')
combos2 = {
    '1/phi^2': 1/phi**2, '1/3': 1/3, '1/(3*phi)': 1/(3*phi),
    'phi/3': phi/3, '1/(phi*sqrt(3))': 1/(phi*math.sqrt(3)),
    'ln(phi)/pi': math.log(phi)/(math.pi), '3/(4*pi)': 3/(4*math.pi),
    'phi/(4*pi)': phi/(4*math.pi), 'sqrt(phi)/3': math.sqrt(phi)/3,
    'phi^2/(3*pi)': phi**2/(3*math.pi), '1/(2*phi)': 1/(2*phi),
    'sqrt(5)/(4*pi)': math.sqrt(5)/(4*math.pi), '1/phi^3': 1/phi**3,
    '2/(3*phi^2)': 2/(3*phi**2), '2/(3*pi)': 2/(3*math.pi),
    '1/(2*pi)': 1/(2*math.pi), 'phi^2/9': phi**2/9,
    '1/sqrt(3*phi)': 1/math.sqrt(3*phi),
    'ln(mu)/(4*pi)': math.log(mu_measured)/(4*math.pi),
}
hdr7 = '  %-25s %-16s %-16s' % ('Expression', 'Value', 'Ratio to target')
print(hdr7)
print('  ' + '-' * 57)
for name, val in sorted(combos2.items(), key=lambda x: abs(ratio_to_alpha/x[1] - 1)):
    r = ratio_to_alpha / val
    if abs(r - 1) < 0.3:
        marker = '<<<' if abs(r-1) < 0.05 else ''
        print(f'  {name:<25} {val:<16.10f} {r:<16.10f} {marker}')
print()
# SUMMARY
print(SEP)
print('  SUMMARY')
print(SEP)
print()
print(f'  mu_0 = 6^5/phi^3 = {mu_0:.10f}  (off by {delta/mu_measured_unc:.0f} sigma)')
print(f'  mu_identity = 3/(alpha^(3/2)*phi^2) = {mu_from_identity:.10f}  (off by {abs(mu_from_identity - mu_measured)/mu_measured_unc:.0f} sigma)')
print()
print('  Key findings:')
print(f'  1. The core identity alpha^(3/2)*mu*phi^2 gives mu = {mu_from_identity:.6f}')
id_sigma = abs(mu_from_identity - mu_measured)/mu_measured_unc
mu0_sigma = abs(delta)/mu_measured_unc
if id_sigma > mu0_sigma:
    print(f'     which is {id_sigma/mu0_sigma:.1f}x farther from measurement than 6^5/phi^3')
else:
    print(f'     which is {mu0_sigma/id_sigma:.1f}x closer to measurement than 6^5/phi^3')
print(f'     Identity check: alpha^(3/2)*mu_meas*phi^2 = {identity_check:.10f} (vs 3)')
print()
print(f'  2. Required correction to mu_0: delta/mu_0 = {correction_needed:.10e}')
print(f'     = {ratio_to_alpha:.6f} * alpha')
print('     Closest framework expression for coefficient: see Section 8 table')
print()

best_label, best_mu, best_res, best_sig = filtered[0]
print(f'  3. Best formula found: {best_label}')
print(f'     mu = {best_mu:.10f}, residual = {best_res:.2e}, {best_sig:.1f} sigma')
print()

print('  TWO PICTURES:')
print('    A) 6^5/phi^3 is fundamental, needs alpha-dependent QED correction')
print('    B) 3/(alpha^(3/2)*phi^2) is fundamental, approximate = 6^5/phi^3')
print(f'    Picture A residual: {delta:.8f} ({delta/mu_measured_unc:.0f} sigma)')
ab = abs(mu_from_identity - mu_measured)
print(f'    Picture B residual: {ab:.8f} ({ab/mu_measured_unc:.0f} sigma)')
if ab > abs(delta):
    print('    ==> Picture A (6^5/phi^3 + correction) is more promising')
else:
    print('    ==> Picture B (identity is exact) is more promising')
print()
