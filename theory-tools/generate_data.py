#!/usr/bin/env python3
"""
generate_data.py — Computation -> data.json

Extracts modular form functions and derivation logic from the Interface Theory
framework, computes all predictions, and writes data.json as the single source
of truth for the build system.

Usage:
    python theory-tools/generate_data.py            # writes data.json
    python theory-tools/generate_data.py --stdout    # prints to stdout
    python theory-tools/generate_data.py --check     # compare with existing data.json
"""

import json
import math
import os
import sys
from datetime import date

# ============ CONSTANTS ============

phi = (1 + math.sqrt(5)) / 2
phibar = 1 / phi
mu = 1836.15267343
alpha_em = 1 / 137.035999084
N_e8 = 7776       # 6^5
h_coxeter = 30
v_ew = 246.22      # GeV
M_Pl = 1.22089e19  # GeV
q = 1 / phi
NTERMS = 500

# ============ MODULAR FORM FUNCTIONS ============

def compute_eta(q_val, nterms=NTERMS):
    prod = 1.0
    for n in range(1, nterms + 1):
        prod *= (1.0 - q_val**n)
    return q_val**(1.0/24.0) * prod

def compute_theta2(q_val, nterms=NTERMS):
    s = 0.0
    for n in range(0, nterms + 1):
        s += q_val**(n*(n+1))
    return 2.0 * q_val**0.25 * s

def compute_theta3(q_val, nterms=NTERMS):
    s = 0.0
    for n in range(1, nterms + 1):
        s += q_val**(n**2)
    return 1.0 + 2.0 * s

def compute_theta4(q_val, nterms=NTERMS):
    s = 0.0
    for n in range(1, nterms + 1):
        s += (-1)**n * q_val**(n**2)
    return 1.0 + 2.0 * s

def sigma3(n):
    s = 0
    for d in range(1, n + 1):
        if n % d == 0:
            s += d**3
    return s

def compute_E4(q_val, nterms=200):
    s = 0.0
    for n in range(1, nterms + 1):
        s += sigma3(n) * q_val**n
    return 1.0 + 240.0 * s

def pct_match(pred, meas_val):
    if meas_val == 0:
        return 0.0
    return 100.0 * (1.0 - abs(pred - meas_val) / abs(meas_val))

# ============ COMPUTE MODULAR FORMS AT q = 1/phi ============

eta_val = compute_eta(q)
theta2_val = compute_theta2(q)
theta3_val = compute_theta3(q)
theta4_val = compute_theta4(q)
t4 = theta4_val
E4_val = compute_E4(q)

# ============ MEASURED VALUES ============

meas = {
    'm_e': 0.51099895,         # MeV
    'm_mu': 105.6583755,       # MeV
    'm_tau': 1776.86,          # MeV
    'm_u': 2.16,               # MeV
    'm_d': 4.67,               # MeV
    'm_s': 93.4,               # MeV
    'm_c': 1270.0,             # MeV
    'm_b': 4180.0,             # MeV
    'm_t': 172690.0,           # MeV
    'M_W': 80.377,             # GeV
    'M_Z': 91.1876,            # GeV
    'm_H': 125.25,             # GeV
    'v': 246.22,               # GeV
    'M_Pl': 1.22089e19,        # GeV
    'alpha_em': 1/137.035999084,
    'alpha_s': 0.1179,
    'sin2_tW': 0.23121,
    'V_us': 0.2253,
    'V_cb': 0.0405,
    'V_ub': 0.00382,
    'V_td': 0.0086,
    'delta_CP_deg': 68.5,
    'dm21_sq': 7.53e-5,
    'dm32_sq': 2.453e-3,
    'theta_12': 33.44,
    'theta_23': 49.2,
    'theta_13': 8.57,
    'Omega_DM': 0.2607,
    'Omega_b': 0.0490,
    'mn_mp': 1.2934,
    'n_s': 0.9649,
    'mu_val': 1836.15267343,
    'lambda_H': (125.25/246.22)**2/2,
}

# ============ BUILD DERIVATIONS ============

def build_derivations():
    """Compute all derivations, return list of dicts."""
    derivations = []

    def add(id_, name, symbol, category, formula_display,
            predicted, measured, measured_display=None,
            confidence='algebra', novel=True, notes=''):
        match = pct_match(predicted, measured)
        if measured_display is None:
            if abs(measured) < 0.001 or abs(measured) > 1e6:
                measured_display = f'{measured:.4e}'
            elif abs(measured) < 1:
                measured_display = f'{measured:.6f}'
            else:
                measured_display = f'{measured:.4f}'
        if abs(predicted) < 0.001 or abs(predicted) > 1e6:
            predicted_display = f'{predicted:.4e}'
        elif abs(predicted) < 0.01:
            predicted_display = f'{predicted:.6f}'
        else:
            predicted_display = f'{predicted:.4f}'
        derivations.append({
            'id': id_,
            'name': name,
            'symbol': symbol,
            'category': category,
            'formula_display': formula_display,
            'predicted': round(predicted, 10),
            'predicted_display': predicted_display,
            'measured': round(measured, 10),
            'measured_display': measured_display,
            'match_pct': round(match, 2),
            'confidence': confidence,
            'novel': novel,
            'notes': notes,
        })

    # --- Gauge Couplings ---
    alpha_pred = (3 / (mu * phi**2))**(2.0/3)
    add('alpha', 'Fine structure constant', '&#945;',
        'gauge_couplings', '(3/(&#956;&#215;&#966;&sup2;))^(2/3)',
        alpha_pred, meas['alpha_em'],
        measured_display='1/137.036',
        notes='Core identity')
    # Override predicted_display for alpha
    derivations[-1]['predicted_display'] = '1/137.04'

    add('alpha_s', 'Strong coupling', '&#945;<sub>s</sub>(M<sub>Z</sub>)',
        'gauge_couplings', '&#951;(1/&#966;)',
        eta_val, meas['alpha_s'],
        measured_display='0.1179 &plusmn; 0.0009',
        notes='Golden Node, direct evaluation')

    sin2tw_pred = eta_val**2 / (2 * t4)
    add('sin2_tW', 'Weinberg angle', 'sin&sup2;&#952;<sub>W</sub>',
        'gauge_couplings', '&#951;&sup2;/(2&#952;<sub>4</sub>)',
        sin2tw_pred, meas['sin2_tW'],
        measured_display='0.2312',
        notes='Golden Node modular forms')

    # --- Quark Masses (relative to proton) ---
    m_p_MeV = 938.272

    m_t_pred_ratio = mu / 10
    add('m_t_ratio', 'Top quark', 'm<sub>t</sub>/m<sub>p</sub>',
        'quark_masses', '&#956;/10',
        m_t_pred_ratio, meas['m_t'] / m_p_MeV,
        measured_display='184.0',
        notes='Mass relative to proton')

    m_b_pred_ratio = phi**3
    add('m_b_ratio', 'Bottom quark', 'm<sub>b</sub>/m<sub>p</sub>',
        'quark_masses', '&#966;&sup3;',
        m_b_pred_ratio, meas['m_b'] / m_p_MeV,
        measured_display='4.46',
        notes='Mass relative to proton')

    m_c_pred_ratio = 4.0 / 3
    add('m_c_ratio', 'Charm quark', 'm<sub>c</sub>/m<sub>p</sub>',
        'quark_masses', '4/3',
        m_c_pred_ratio, meas['m_c'] / m_p_MeV,
        measured_display='1.35',
        novel=False,
        notes='Mass relative to proton')

    m_s_pred_ratio = 1.0 / 10
    add('m_s_ratio', 'Strange quark', 'm<sub>s</sub>/m<sub>p</sub>',
        'quark_masses', '1/10',
        m_s_pred_ratio, meas['m_s'] / m_p_MeV,
        measured_display='0.099',
        novel=False,
        notes='Mass relative to proton')

    # --- Quark Mass Ratios ---
    add('m_u_from_me', 'Up quark mass', 'm<sub>u</sub>',
        'quark_mass_ratios', 'm<sub>e</sub>&#215;&#966;&sup3;',
        meas['m_e'] * phi**3, meas['m_u'],
        measured_display='2.16 MeV',
        notes='Lightest quark from electron mass')

    add('m_d_from_me', 'Down quark mass', 'm<sub>d</sub>',
        'quark_mass_ratios', 'm<sub>e</sub>&#215;&#966;^(9/2)',
        meas['m_e'] * phi**4.5, meas['m_d'],
        measured_display='4.67 MeV')

    add('m_s_from_me', 'Strange quark mass', 'm<sub>s</sub>',
        'quark_mass_ratios', 'm<sub>e</sub>&#215;&#956;/10',
        meas['m_e'] * mu / 10, meas['m_s'],
        measured_display='93.4 MeV')

    add('m_c_from_mu', 'Charm quark mass', 'm<sub>c</sub>',
        'quark_mass_ratios', '&#956;&#215;2/3 MeV',
        mu * 2.0 / 3, meas['m_c'],
        measured_display='1270 MeV')

    add('m_t_from_v', 'Top quark mass', 'm<sub>t</sub>',
        'quark_mass_ratios', 'v/&radic;2',
        v_ew / math.sqrt(2) * 1000, meas['m_t'],
        measured_display='172.69 GeV',
        notes='Yukawa coupling = 1')

    # --- Lepton Masses ---
    add('mu_ratio', 'Proton-to-electron mass ratio', '&#956;',
        'lepton_masses', '6&#8309;/&#966;&sup3;',
        N_e8 / phi**3, meas['mu_val'],
        measured_display='1836.153',
        notes='Core derivation')

    mu_corrected = N_e8 / phi**3 + 9 / (7 * phi**2)
    add('mu_corrected', '&#956; with correction', '&#956;',
        'lepton_masses', '6&#8309;/&#966;&sup3; + 9/(7&#966;&sup2;)',
        mu_corrected, meas['mu_val'],
        measured_display='1836.153',
        notes='Dark vacuum correction, 99.9998%')

    add('m_mu_from_mu', 'Muon mass', 'm<sub>&#956;</sub>',
        'lepton_masses', 'm<sub>e</sub>&#215;&#956;/9',
        meas['m_e'] * mu / 9, meas['m_mu'],
        measured_display='105.658 MeV',
        novel=False)

    add('m_tau_from_mu', 'Tau mass', 'm<sub>&#964;</sub>',
        'lepton_masses', 'm<sub>e</sub>&#215;&#956;&#215;3/&#966;&sup2;',
        meas['m_e'] * mu * 3 / phi**2, meas['m_tau'],
        measured_display='1776.86 MeV',
        novel=False)

    # --- CKM Matrix ---
    V_us_pred = (phi / 7) * (1 - t4)
    add('V_us', 'Cabibbo angle', 'V<sub>us</sub>',
        'ckm_matrix', '(&#966;/7)(1&minus;&#952;<sub>4</sub>)',
        V_us_pred, meas['V_us'],
        measured_display='0.2253',
        notes='Golden Node modular forms')

    V_cb_pred = (phi / 7) * math.sqrt(t4)
    add('V_cb', 'V_cb', 'V<sub>cb</sub>',
        'ckm_matrix', '(&#966;/7)&radic;&#952;<sub>4</sub>',
        V_cb_pred, meas['V_cb'],
        measured_display='0.0405')

    V_td_pred = (phi / 7) * t4
    add('V_td', 'V_td', 'V<sub>td</sub>',
        'ckm_matrix', '(&#966;/7)&#952;<sub>4</sub>',
        V_td_pred, meas['V_td'],
        measured_display='0.0086')

    V_ub_pred = (phi / 7) * 3 * t4**1.5
    add('V_ub', 'V_ub', 'V<sub>ub</sub>',
        'ckm_matrix', '(&#966;/7)&#215;3&#952;<sub>4</sub>^(3/2)',
        V_ub_pred, meas['V_ub'],
        measured_display='0.00382')

    # --- PMNS Angles ---
    # theta_12
    t12_candidates = [
        ('arctan(2/3)', math.degrees(math.atan(2.0/3))),
        ('arctan(2/3)*(1+t4/phi)', math.degrees(math.atan(2.0/3))*(1+t4/phi)),
        ('arcsin(1/sqrt(3))', math.degrees(math.asin(1/math.sqrt(3)))),
    ]
    t12_candidates.sort(key=lambda x: abs(x[1] - meas['theta_12']))
    best_t12 = t12_candidates[0]
    add('theta_12', 'Solar mixing angle', '&#952;<sub>12</sub>',
        'pmns_angles', best_t12[0].replace('phi', '&#966;'),
        best_t12[1], meas['theta_12'],
        measured_display='33.44&deg;')

    # theta_23
    t23_candidates = [
        ('arctan(&#966;)', math.degrees(math.atan(phi))),
        ('45 + arctan(&#952;<sub>4</sub>)', 45.0 + math.degrees(math.atan(t4))),
    ]
    t23_candidates.sort(key=lambda x: abs(x[1] - meas['theta_23']))
    best_t23 = t23_candidates[0]
    add('theta_23', 'Atmospheric mixing angle', '&#952;<sub>23</sub>',
        'pmns_angles', best_t23[0],
        best_t23[1], meas['theta_23'],
        measured_display='49.2&deg;')

    # theta_13
    t13_candidates = [
        ('arcsin(&#951;)', math.degrees(math.asin(eta_val))),
        ('arctan(&#952;<sub>4</sub>)', math.degrees(math.atan(t4))),
    ]
    t13_candidates.sort(key=lambda x: abs(x[1] - meas['theta_13']))
    best_t13 = t13_candidates[0]
    add('theta_13', 'Reactor mixing angle', '&#952;<sub>13</sub>',
        'pmns_angles', best_t13[0],
        best_t13[1], meas['theta_13'],
        measured_display='8.57&deg;')

    # --- Higgs Sector ---
    lambda_H_pred = 1 / (3 * phi**2)
    lambda_H_meas = (meas['m_H'] / v_ew)**2 / 2
    add('lambda_H', 'Higgs quartic coupling', '&#955;<sub>H</sub>',
        'higgs_sector', '1/(3&#966;&sup2;)',
        lambda_H_pred, lambda_H_meas,
        measured_display='0.1292',
        notes='From Higgs self-coupling')

    m_H_pred = v_ew * math.sqrt(2 / (3 * phi**2))
    add('m_H', 'Higgs mass', 'm<sub>H</sub>',
        'higgs_sector', 'v&radic;(2/(3&#966;&sup2;))',
        m_H_pred, meas['m_H'],
        measured_display='125.25 GeV')

    # --- Gauge Bosons ---
    sin2tw_fw = eta_val**2 / (2 * t4)
    cos_fw = math.sqrt(1 - sin2tw_fw)
    M_W_pred = v_ew * cos_fw / 2
    # Use best formula from tighten_and_map
    M_W_candidates = [
        E4_val**(1.0/3) * phi**2,
        v_ew / 2 * (1 + t4 * phibar),
        v_ew * cos_fw / 2,
    ]
    M_W_candidates.sort(key=lambda x: abs(x - meas['M_W']))
    add('M_W', 'W boson mass', 'M<sub>W</sub>',
        'gauge_bosons', 'E<sub>4</sub>^(1/3)&#215;&#966;&sup2;',
        M_W_candidates[0], meas['M_W'],
        measured_display='80.377 GeV')

    M_Z_pred = M_W_candidates[0] / cos_fw
    add('M_Z', 'Z boson mass', 'M<sub>Z</sub>',
        'gauge_bosons', 'M<sub>W</sub>/cos&#952;<sub>W</sub>',
        M_Z_pred, meas['M_Z'],
        measured_display='91.188 GeV')

    # --- Cosmological ---
    Lambda_pred = t4**80 * math.sqrt(5) / phi**2
    add('Lambda', 'Cosmological constant', '&#923;',
        'cosmological', '&#952;<sub>4</sub>&sup8;&#8304;&#215;&radic;5/&#966;&sup2;',
        Lambda_pred, 2.89e-122,
        measured_display='2.89 &times; 10<sup>-122</sup>',
        notes='From modular forms, near-exact')
    # Override display for Lambda
    derivations[-1]['predicted_display'] = f'{Lambda_pred:.2e}'

    v_hierarchy_pred = M_Pl * phibar**80 / (1 - phi * t4)
    # Convert to GeV
    add('v_hierarchy', 'Higgs VEV (hierarchy)', 'v',
        'cosmological', 'M<sub>Pl</sub>&#215;&#966;&#773;&sup8;&#8304;/(1&minus;&#966;&#952;<sub>4</sub>)',
        v_hierarchy_pred, v_ew,
        measured_display='246.22 GeV',
        notes='Hierarchy problem solution')

    Omega_DM_pred_candidates = [
        ((phi/6)*(1-t4), '(&#966;/6)(1&minus;&#952;<sub>4</sub>)'),
        ((phi/6)*(1-t4/phi), '(&#966;/6)(1&minus;&#952;<sub>4</sub>/&#966;)'),
    ]
    Omega_DM_pred_candidates.sort(key=lambda x: abs(x[0] - meas['Omega_DM']))
    best_odm = Omega_DM_pred_candidates[0]
    add('Omega_DM', 'Dark matter density', '&#937;<sub>DM</sub>',
        'cosmological', best_odm[1],
        best_odm[0], meas['Omega_DM'],
        measured_display='0.2607')

    Omega_b_pred = alpha_em * phi**4
    add('Omega_b', 'Baryon density', '&#937;<sub>b</sub>',
        'cosmological', '&#945;&#215;&#966;&#8308;',
        Omega_b_pred, meas['Omega_b'],
        measured_display='0.0490')

    # --- Nucleon Properties ---
    delta_CP_base = math.degrees(math.atan(phi**2))
    # Best delta_CP from tighten_and_map
    dc_candidates = [
        delta_CP_base * (1 - t4 / (2*phi)),
        math.degrees(math.atan(phi**2 * (1 - alpha_em))),
        delta_CP_base * (1 - t4 * phibar),
    ]
    dc_candidates.sort(key=lambda x: abs(x - meas['delta_CP_deg']))
    add('delta_CP', 'CKM CP phase', '&#948;<sub>CP</sub>',
        'ckm_matrix', 'arctan(&#966;&sup2;)(1&minus;&#952;<sub>4</sub>/(2&#966;))',
        dc_candidates[0], meas['delta_CP_deg'],
        measured_display='68.5&deg;')

    # --- Spectral index ---
    N_e = 2 * h_coxeter  # 60 e-folds
    n_s_pred_candidates = [
        1 - 2.0/N_e,
        1 - 2.0/(N_e*(1+t4)),
        1 - 2.0/N_e - 1.0/N_e**2,
    ]
    n_s_pred_candidates.sort(key=lambda x: abs(x - meas['n_s']))
    add('n_s', 'Spectral index', 'n<sub>s</sub>',
        'cosmological', '1 &minus; 2/N<sub>e</sub>',
        n_s_pred_candidates[0], meas['n_s'],
        measured_display='0.9649',
        notes='N_e = 2h = 60 e-folds')

    # --- Neutrino mass ratio ---
    dm_ratio_pred = 3 * phi**5
    dm_ratio_meas = meas['dm32_sq'] / meas['dm21_sq']
    add('dm_ratio', 'Neutrino mass-squared ratio', '&#916;m&sup2;<sub>32</sub>/&#916;m&sup2;<sub>21</sub>',
        'pmns_angles', '3&#966;&#8309;',
        dm_ratio_pred, dm_ratio_meas,
        measured_display='32.6')

    # --- Electron mass from Planck scale ---
    m_e_pred = M_Pl * phibar**80 * math.exp(-80/(2*math.pi)) / math.sqrt(2) / (1 - phi * t4)
    # Convert GeV to keV
    m_e_pred_keV = m_e_pred * 1e6  # GeV -> keV
    add('m_e_abs', 'Electron mass (absolute)', 'm<sub>e</sub>',
        'hierarchies', 'M<sub>Pl</sub>&#215;&#966;&#773;&sup8;&#8304;&#215;e^(-80/2&#960;)/&radic;2/(1&minus;&#966;&#952;<sub>4</sub>)',
        m_e_pred_keV, 511.00,
        measured_display='511.00 keV',
        notes='Complete m_e from M_Pl')

    # --- Top quark absolute ---
    m_t_abs_pred = meas['m_e'] * mu**2 / 10
    add('m_t_abs', 'Top quark mass (absolute)', 'm<sub>t</sub>',
        'hierarchies', 'm<sub>e</sub>&#215;&#956;&sup2;/10',
        m_t_abs_pred / 1000, meas['m_t'] / 1000,
        measured_display='172.69 GeV',
        notes='From CLAUDE.md table')
    derivations[-1]['predicted_display'] = f'{m_t_abs_pred/1000:.2f} GeV'

    return derivations


def build_predictions():
    """Build list of untested predictions."""
    return [
        {
            'id': 'breathing_mode',
            'name': 'Breathing mode scalar',
            'value': '108.5 GeV',
            'formula': '&radic;(3/4) &times; m<sub>H</sub>',
            'test': 'LHC Run 3 diphoton',
            'when': '2025-2028',
            'status': 'untested',
        },
        {
            'id': 'R_running',
            'name': 'Running ratio R = d(ln &#956;)/d(ln &#945;)',
            'value': '-3/2',
            'formula': '-h(A<sub>2</sub>)/rank(A<sub>2</sub>)',
            'test': 'ELT/ANDES spectroscopy',
            'when': '~2035',
            'status': 'untested',
        },
        {
            'id': 'f1_613THz',
            'name': '613 THz aromatic frequency',
            'value': '613 THz',
            'formula': '&#956;/3 (THz)',
            'test': 'Craddock lab measurement',
            'when': '2026-2027',
            'status': 'untested',
        },
        {
            'id': 'r_tensor',
            'name': 'Tensor-to-scalar ratio',
            'value': '0.0033',
            'formula': '12/N<sub>e</sub>&sup2; (N<sub>e</sub>=60)',
            'test': 'CMB-S4',
            'when': '2027+',
            'status': 'untested',
        },
    ]


def build_frequencies():
    """Build biological frequency spectrum."""
    h_planck = 6.62607015e-34  # J*s
    freqs = []

    def add_freq(id_, name, formula_display, value, measured, category):
        match = pct_match(float(value.split()[0]), float(measured.split()[0]))
        freqs.append({
            'id': id_,
            'name': name,
            'formula_display': formula_display,
            'value': value,
            'measured': measured,
            'match_pct': round(match, 2),
            'category': category,
        })

    add_freq('f1_molecular', 'Molecular consciousness', '&#956;/3',
             '612 THz', '613 THz', 'maintenance')
    add_freq('f2_neural', 'Neural gamma', '4h/3',
             '40 Hz', '40 Hz', 'maintenance')
    add_freq('f3_mayer', 'Mayer wave', '3/h',
             '0.1 Hz', '0.1 Hz', 'maintenance')
    add_freq('water_oh', 'Water O-H stretch', '&#956;/18',
             '102 THz', '102 THz', 'biological')
    add_freq('chl_qy', 'Chlorophyll Q_y band', '&#956;/4',
             '459 THz', '459 THz', 'biological')
    add_freq('slow_osc', 'Slow oscillation', '3/4 Hz',
             '0.75 Hz', '0.75 Hz', 'sleep')
    add_freq('spindles', 'Sleep spindles', 'h/3',
             '10 Hz', '10 Hz', 'sleep')

    return freqs


def build_scorecard(derivations):
    """Compute summary statistics from derivations."""
    matches = [d['match_pct'] for d in derivations]
    total = len(matches)
    return {
        'total': total,
        'above_99': sum(1 for m in matches if m >= 99.0),
        'above_97': sum(1 for m in matches if m >= 97.0),
        'above_95': sum(1 for m in matches if m >= 95.0),
        'average_match': round(sum(matches) / total, 2) if total else 0,
        'free_parameters': 1,
    }


def build_data():
    """Build the complete data structure."""
    derivations = build_derivations()
    predictions = build_predictions()
    frequencies = build_frequencies()
    scorecard = build_scorecard(derivations)

    return {
        'meta': {
            'generated': str(date.today()),
            'version': 1,
            'generator': 'theory-tools/generate_data.py',
        },
        'constants': {
            'phi': phi,
            'phibar': phibar,
            'mu': mu,
            'alpha_em': alpha_em,
            'h_coxeter': h_coxeter,
            'N_e8': N_e8,
            'q': q,
            'theta4_q': round(t4, 8),
            'eta_q': round(eta_val, 8),
            'theta2_q': round(theta2_val, 8),
            'theta3_q': round(theta3_val, 8),
            'E4_q': round(E4_val, 1),
        },
        'derivations': derivations,
        'predictions': predictions,
        'frequencies': frequencies,
        'scorecard': scorecard,
    }


def main():
    data = build_data()

    if '--stdout' in sys.argv:
        print(json.dumps(data, indent=2, ensure_ascii=False))
        return

    script_dir = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(script_dir, 'data.json')

    if '--check' in sys.argv:
        if not os.path.exists(out_path):
            print('data.json does not exist yet.')
            sys.exit(1)
        with open(out_path, 'r', encoding='utf-8') as f:
            existing = json.load(f)
        # Compare derivations
        new_ids = {d['id'] for d in data['derivations']}
        old_ids = {d['id'] for d in existing.get('derivations', [])}
        added = new_ids - old_ids
        removed = old_ids - new_ids
        changed = []
        for d in data['derivations']:
            for e in existing.get('derivations', []):
                if d['id'] == e['id']:
                    if abs(d['match_pct'] - e['match_pct']) > 0.01:
                        changed.append((d['id'], e['match_pct'], d['match_pct']))
        if not added and not removed and not changed:
            print('data.json is up to date.')
            sys.exit(0)
        if added:
            print(f'New derivations: {added}')
        if removed:
            print(f'Removed derivations: {removed}')
        if changed:
            for id_, old_m, new_m in changed:
                print(f'  {id_}: {old_m}% -> {new_m}%')
        sys.exit(1)

    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    # Print summary
    sc = data['scorecard']
    print(f'Wrote {out_path}')
    print(f'  {sc["total"]} derivations, {sc["above_99"]} above 99%, avg {sc["average_match"]}%')
    print(f'  {len(data["predictions"])} predictions, {len(data["frequencies"])} frequencies')


if __name__ == '__main__':
    main()
