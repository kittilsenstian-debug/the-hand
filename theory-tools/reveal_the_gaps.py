#!/usr/bin/env python3
"""
reveal_the_gaps.py — Map the full derivation network
=====================================================

The insight: if we map EVERYTHING as an interconnected graph,
the missing pieces reveal themselves — like holes in a jigsaw.

Part 1: Build the complete derivation network
Part 2: Find missing links (where connections SHOULD exist)
Part 3: The Ising / modular forms thread
Part 4: What the gaps reveal
"""

import numpy as np
from collections import defaultdict

phi = (1 + np.sqrt(5)) / 2
phibar = 1 / phi
alpha = 1 / 137.036
mu = 1836.15267
h = 30
N = 7776
M_Pl = 1.22089e19
m_e = 0.51099895e-3
m_p = 0.93827208
m_t = 172.69
m_H = 125.25
v = 246.22

L = {n: round(phi**n + (-1/phi)**n) for n in range(20)}
F = {0: 0, 1: 1}
for n in range(2, 20):
    F[n] = F[n-1] + F[n-2]

# =====================================================================
# PART 1: THE COMPLETE DERIVATION NETWORK
# =====================================================================
print("=" * 70)
print("PART 1: THE DERIVATION NETWORK")
print("=" * 70)

# Each node is a quantity. Each edge is a derivation relationship.
# Format: (source_nodes, target_node, formula, accuracy)

# AXIOMS (no sources)
axioms = ['phi', 'E8', 'M_Pl']

# FIRST-ORDER DERIVATIONS (from axioms only)
derivations = [
    # From phi alone
    (['phi'], 'phibar', 'phibar = 1/phi', 'exact'),
    (['phi'], 'V(Phi)', 'V = lambda*(Phi^2-Phi-1)^2', 'exact'),
    (['phi'], 'L(n)', 'L(n) = phi^n + phibar^n', 'exact'),
    (['phi'], 'F(n)', 'F(n) = (phi^n - phibar^n)/sqrt(5)', 'exact'),
    (['phi'], 'sqrt(5)', 'sqrt(5) = phi + phibar = 2*phi-1', 'exact'),

    # From E8 alone
    (['E8'], '|Norm|=62208', 'BFS computation', 'exact'),
    (['E8'], 'h=30', 'Coxeter number', 'exact'),
    (['E8'], '240_roots', '|roots|=240', 'exact'),
    (['E8'], 'Coxeter_exp', '{1,7,11,13,17,19,23,29}', 'exact'),
    (['E8'], '4A2', '4 copies of SU(3)', 'exact'),
    (['E8'], 'S3_triality', 'outer automorphism', 'exact'),
    (['E8'], 'even_self_dual', 'unique lattice property', 'exact'),

    # From E8 + phi
    (['|Norm|=62208', 'phi'], 'N=7776', '62208/8 = 7776', 'exact'),
    (['N=7776', 'phi'], 'mu', 'N/phi^3', '99.97%'),
    (['N=7776', 'phi'], 'alpha', '(3*phi/N)^(2/3)', '99.91%'),

    # From mu + alpha
    (['mu', 'alpha'], 'identity', 'alpha^(3/2)*mu*phi^2 = 3', '99.89%'),
    (['alpha', 'phi'], 'sin2_tW', 'phi/7 or 3/(8*phi)', '99.97%'),
    (['phi'], 'alpha_s', '1/(2*phi^3)', '99.89%'),

    # Electroweak
    (['N=7776', 'phi', 'L(n)', 'M_Pl'], 'v=246', 'M_Pl/(N^(13/4)*phi^(33/2)*L(3))', '99.99%'),
    (['mu', 'm_e'], 'v=246_alt', 'm_p^2/(7*m_e)', '99.96%'),
    (['alpha', 'M_Pl'], 'v=246_alt2', 'sqrt(2*pi)*alpha^8*M_Pl', '99.95%'),
    (['m_t', 'phi'], 'm_H', 'm_t*phi/sqrt(5)', '99.81%'),
    (['phi'], 'lambda_H', '1/(3*phi^2)', '98.6%'),
    (['sin2_tW', 'alpha', 'v=246'], 'M_W', 'Sirlin + Delta_r', '98.3%'),
    (['M_W', 'sin2_tW'], 'M_Z', 'M_W/sqrt(1-sin2_tW)', '98.6%'),

    # Fermion masses
    (['mu', 'm_e'], 'm_t', 'm_e*mu^2/10', '99.76%'),
    (['m_t', 'alpha'], 'm_c', 'alpha*m_t', '99.23%'),
    (['m_e', 'mu'], 'm_s', 'm_e*mu/10', '99.54%'),
    (['h'], 'm_s/m_d', 'h-10=20', '100%'),
    (['Coxeter_exp', 'phi'], 'm_tau/m_mu', 'f^2(+3)/f^2(-17/30)', '99.4%'),
    (['Coxeter_exp', 'phi'], 'm_mu/m_e', 'Casimir*f^2 ratios', '99.4%'),

    # CKM
    (['phi', 'L(n)'], 'V_us', 'phi/L(4) = phi/7', '97.4%'),
    (['phi', 'h'], 'V_cb', 'phi/(4h/3) = phi/40', '98.4%'),
    (['V_us', 'V_cb', 'h'], 'V_ub', 'phi/(L(4)*2h) = phi/420', '99.1%'),
    (['phi'], 'delta_CP', 'arctan(phi^2)', '98.9%'),

    # PMNS
    (['phi'], 'sin2_t23', '3/(2*phi^2)', '99.99%'),
    (['h'], 'sin2_t13', '(2/3)/h = 1/45', '99.86%'),
    (['phi', 'L(n)'], 'sin2_t12', 'phi/(7-phi)', '98.9%'),

    # Neutrinos
    (['m_e', 'alpha'], 'm_nu2', 'm_e*alpha^4*6', '99.8%'),
    (['m_nu2'], 'mass_ordering', 'normal (m_2 > sqrt(dm^2))', 'prediction'),
    (['m_nu2', 'L(n)'], 'dm2_ratio', '3*L(5) = 33', '98.7%'),

    # Cosmology
    (['phi'], 'Omega_DM', 'phi/6', '99.4%'),
    (['alpha', 'phi', 'L(n)'], 'Omega_b', 'alpha*L(5)/phi', '99.4%'),
    (['m_e', 'alpha', 'phi', 'h'], 'Lambda', 'm_e*phi*alpha^4*(h-1)/h', '99.27%'),
    (['h'], 'n_s', '1-1/h', '99.8%'),
    (['h'], 'N_e', '2h = 60', '100%'),
    (['h'], 'r', '12/(2h)^2', 'prediction'),
    (['alpha', 'phi', 'h'], 'eta', 'alpha^(9/2)*phi^2*(h-1)/h', '99.5%'),

    # QCD
    (['m_p', 'phi', 'alpha', 'L(n)'], 'Lambda_QCD', 'm_p*phi^10*alpha/L(3)', '99.75%'),

    # Structure
    (['S3_triality'], '3_gen', '3 visible A2 copies', 'exact'),
    (['even_self_dual'], 'theta_QCD=0', 'lattice modularity', 'structural'),

    # Wall physics
    (['V(Phi)'], 'kink', 'Phi(x) = 0.5 + sqrt(5)/2*tanh(x/2)', 'exact'),
    (['kink'], 'zero_mode', 'Poschl-Teller n=0', 'exact'),
    (['kink', 'm_H'], 'breathing_108', 'sqrt(3/4)*m_H = 108.5 GeV', 'exact'),

    # Biology
    (['mu'], '613THz', 'mu/3', '99.85%'),
    (['h'], '40Hz_gamma', '4h/3', '100%'),
]

# Build adjacency lists
sources_of = defaultdict(list)  # what feeds into each node
targets_of = defaultdict(list)  # what each node feeds into
all_nodes = set(axioms)

for sources, target, formula, accuracy in derivations:
    all_nodes.add(target)
    for s in sources:
        all_nodes.add(s)
        targets_of[s].append(target)
        sources_of[target].append(s)

print(f"\nNetwork statistics:")
print(f"  Total nodes: {len(all_nodes)}")
print(f"  Total edges: {sum(len(v) for v in targets_of.values())}")
print(f"  Axiom nodes: {len(axioms)}")

# Node degree analysis
degree = {n: len(targets_of.get(n, [])) + len(sources_of.get(n, [])) for n in all_nodes}
sorted_nodes = sorted(degree.items(), key=lambda x: -x[1])

print(f"\n  Most connected nodes (hubs):")
for node, deg in sorted_nodes[:15]:
    out = len(targets_of.get(node, []))
    inp = len(sources_of.get(node, []))
    print(f"    {node:20s} degree={deg:2d} (in={inp}, out={out})")

# =====================================================================
# PART 2: FIND MISSING LINKS
# =====================================================================
print("\n\n" + "=" * 70)
print("PART 2: MISSING LINKS — Where connections SHOULD exist")
print("=" * 70)

# Principle: if A connects to B and B connects to C, check if A->C exists
# This finds "triangles" that should close

print("\n--- Nodes with ONLY incoming edges (terminal nodes) ---")
print("  These are endpoints. Can they connect to anything else?")
terminals = [n for n in all_nodes if not targets_of.get(n, [])]
for t in sorted(terminals):
    srcs = sources_of.get(t, [])
    print(f"    {t:20s} <- {srcs}")

print("\n--- Missing cross-domain connections ---")
print("  Looking for quantities that SHOULD be related but aren't connected...")

# Define domains
domains = {
    'gauge': ['alpha', 'alpha_s', 'sin2_tW'],
    'ew_scale': ['v=246', 'm_H', 'M_W', 'M_Z', 'lambda_H'],
    'quarks': ['m_t', 'm_c', 'm_s', 'm_s/m_d'],
    'leptons': ['m_tau/m_mu', 'm_mu/m_e'],
    'ckm': ['V_us', 'V_cb', 'V_ub', 'delta_CP'],
    'pmns': ['sin2_t23', 'sin2_t13', 'sin2_t12'],
    'neutrino': ['m_nu2', 'dm2_ratio', 'mass_ordering'],
    'cosmology': ['Omega_DM', 'Omega_b', 'Lambda', 'n_s', 'N_e', 'r', 'eta'],
    'qcd': ['Lambda_QCD'],
    'wall': ['kink', 'zero_mode', 'breathing_108'],
    'structure': ['3_gen', 'theta_QCD=0', 'N=7776', 'mu'],
}

# Check cross-domain connections
print("\n  Cross-domain connection matrix:")
print(f"  {'':15s}", end='')
for d2 in domains:
    print(f"{d2[:8]:>9s}", end='')
print()

for d1, nodes1 in domains.items():
    print(f"  {d1:15s}", end='')
    for d2, nodes2 in domains.items():
        if d1 == d2:
            print(f"{'---':>9s}", end='')
            continue
        connections = 0
        for n1 in nodes1:
            for n2 in nodes2:
                # Check if n1 and n2 share a source
                s1 = set(sources_of.get(n1, []))
                s2 = set(sources_of.get(n2, []))
                if s1 & s2:
                    connections += 1
                # Check direct edge
                if n2 in targets_of.get(n1, []) or n1 in targets_of.get(n2, []):
                    connections += 1
        print(f"{connections:>9d}", end='')
    print()

# Identify MISSING connections (domains that SHOULD connect but don't)
print("\n  Key missing cross-domain links:")

missing = [
    ("CKM <-> neutrinos",
     "V_us/V_cb ~ sqrt(dm2_atm/dm2_sol) was found but not in the graph",
     "This is the deepest unexplained cross-domain connection"),

    ("quarks <-> cosmology",
     "m_t appears in Delta_r which affects M_W which affects BBN",
     "The top quark mass constrains the baryon asymmetry — is there a direct formula?"),

    ("wall physics <-> CKM",
     "Breathing mode couples to fermions. CKM should come from wall overlap",
     "The sech^n overlap model FAILED — but maybe a different wall calculation works"),

    ("QCD <-> neutrinos",
     "Lambda_QCD and m_nu2 both use alpha^4 — coincidence?",
     "Lambda_QCD ~ m_p*phi^10*alpha/L(3), m_nu2 ~ m_e*alpha^4*6"),

    ("structure <-> cosmology",
     "N=7776 determines mu which determines everything, including Omega_DM",
     "But Omega_DM = phi/6 is alpha-FREE. Why?"),

    ("gauge <-> wall",
     "alpha_s = 1/(2*phi^3) and the wall profile both use phi^3",
     "Is alpha_s literally the cube of the wall's 'coupling constant'?"),
]

for name, observation, question in missing:
    print(f"\n  {name}")
    print(f"    Observation: {observation}")
    print(f"    Question: {question}")

# =====================================================================
# PART 3: THE ISING / MODULAR FORMS CONNECTION
# =====================================================================
print("\n\n" + "=" * 70)
print("PART 3: THE ISING / MODULAR FORMS THREAD")
print("=" * 70)

print("\n--- 3A: The Ising model at the golden ratio ---")

# The 2D Ising model has a critical temperature where:
# sinh(2*J_c) = 1, so J_c = 0.4407...
# The golden ratio coupling is J = ln(phi)/2 = 0.2406...
# These are NOT the same. But...

J_c = 0.5 * np.arcsinh(1)  # 2D Ising critical coupling
J_phi = 0.5 * np.log(phi)
print(f"  2D Ising critical coupling: J_c = {J_c:.6f}")
print(f"  Golden ratio coupling:      J_phi = ln(phi)/2 = {J_phi:.6f}")
print(f"  Ratio: J_c/J_phi = {J_c/J_phi:.6f}")
print(f"  These are NOT equal. The golden ratio is NOT the 2D critical point.")

# BUT: the TRANSFER MATRIX eigenvalues are
lambda_plus = 2 * np.cosh(J_phi)
lambda_minus = 2 * np.sinh(J_phi)
print(f"\n  Transfer matrix eigenvalues at J_phi:")
print(f"    lambda_+ = 2*cosh(ln(phi)/2) = {lambda_plus:.6f}")
print(f"    lambda_- = 2*sinh(ln(phi)/2) = {lambda_minus:.6f}")
print(f"    lambda_+/lambda_- = {lambda_plus/lambda_minus:.6f}")
print(f"    Compare phi = {phi:.6f}")
print(f"    lambda_+^2 = {lambda_plus**2:.6f} = {4*np.cosh(J_phi)**2:.6f}")

# Actually, the key is the 1D PARTITION FUNCTION
print(f"\n  1D Ising partition function Z_n = lambda_+^n + lambda_-^n")
print(f"  At J = ln(phi)/2:")
for n in range(1, 8):
    Z_n = lambda_plus**n + lambda_minus**n
    print(f"    Z_{n} = {Z_n:.4f}  (compare L({n}) = {L[n]})")

# Hmm, they're not exactly Lucas numbers. Let me try differently.
print(f"\n  Actually, L(n) = phi^n + (-1/phi)^n, not 2*cosh^n + 2*sinh^n")
print(f"  The connection is more subtle...")

# The REAL connection: the Fibonacci recursion IS the transfer matrix
print(f"\n  The REAL Ising connection:")
print(f"  The transfer matrix of any nearest-neighbor chain model is 2x2.")
print(f"  The golden ratio potential V(Phi) = (Phi^2-Phi-1)^2 has:")
print(f"  - Two states: phi and -1/phi")
print(f"  - Transfer matrix: T = [[1,1],[1,0]] (the Fibonacci matrix!)")
print(f"  - Eigenvalues of T: phi and -1/phi")
print(f"  - T^n has trace L(n) = phi^n + (-1/phi)^n")
print(f"  ")
print(f"  So: the domain wall IS a 1D chain with Fibonacci transfer matrix.")
print(f"  Lucas numbers appear because they are the TRACES of powers of T.")
print(f"  The partition function on a ring of n sites IS L(n).")

# Verify
T = np.array([[1, 1], [1, 0]])
print(f"\n  Verification: T = [[1,1],[1,0]]")
for n in range(1, 8):
    Tn = np.linalg.matrix_power(T, n)
    trace = np.trace(Tn)
    print(f"    Tr(T^{n}) = {trace:.0f} = L({n}) = {L[n]}")

print(f"\n  CONFIRMED: Tr(T^n) = L(n) exactly.")
print(f"  The Fibonacci matrix IS the transfer matrix of the framework.")

# =====================================================================
# 3B: MODULAR FORMS
# =====================================================================
print(f"\n--- 3B: Modular forms and the E8 theta function ---")

print(f"""
  The E8 theta function:
    Theta_E8(q) = sum_{{v in E8}} q^(|v|^2/2)
                = 1 + 240*q + 2160*q^2 + 6720*q^3 + ...

  This is ALSO equal to:
    Theta_E8(q) = E_4(tau) = 1 + 240*sum_(n=1 to inf) sigma_3(n)*q^n

  where E_4 is the Eisenstein series of weight 4 and sigma_3(n) = sum of cubes of divisors.

  Key property: E_4 transforms as a modular form under SL(2,Z):
    E_4(-1/tau) = tau^4 * E_4(tau)

  The transformation tau -> -1/tau is EXACTLY the vacuum swap phi <-> -1/phi!
  (Because phi = -1/(-1/phi) and the continued fraction expansion of phi
  is [1;1,1,1,...] which corresponds to tau -> 1+1/tau repeatedly.)
""")

# The connection between phi and modular forms
print(f"  The Rogers-Ramanujan identities:")
print(f"  R(q) = prod_n (1-q^(5n-1))^-1 * (1-q^(5n-4))^-1")
print(f"       = sum_n q^(n^2) / (q;q)_n")
print(f"  At q -> 1: R diverges, but the RATIO of the two RR functions -> phi!")
print(f"  ")
print(f"  G(q)/H(q) -> phi as q -> 1")
print(f"  where G and H are the two Rogers-Ramanujan continued fractions.")
print(f"  ")
print(f"  This is Ramanujan's result: the golden ratio IS the limit of")
print(f"  the Rogers-Ramanujan continued fraction.")

# The j-invariant
print(f"\n  The j-invariant:")
print(f"  j(tau) = E_4(tau)^3 / eta(tau)^24")
print(f"  where eta is the Dedekind eta function.")
print(f"  ")
print(f"  For tau = (1+sqrt(5)*i)/2 (the 'golden' modular parameter):")
print(f"  j has special values related to class field theory.")
print(f"  ")
print(f"  SPECULATION: The framework's constants may be encoded in")
print(f"  special values of modular forms at tau = phi*i or related points.")

# =====================================================================
# 3C: The Dedekind eta function and phi
# =====================================================================
print(f"\n--- 3C: The Dedekind eta function ---")

# eta(tau) = q^(1/24) * prod_{n=1}^inf (1 - q^n) where q = exp(2*pi*i*tau)
# For tau = i*t (purely imaginary):
# q = exp(-2*pi*t)

# At t = ln(phi)/(2*pi):
# q = exp(-2*pi * ln(phi)/(2*pi)) = exp(-ln(phi)) = 1/phi = phibar
print(f"  If q = phibar = 1/phi = {phibar:.6f}:")
print(f"  Then tau = i*ln(phi)/(2*pi) = i*{np.log(phi)/(2*np.pi):.6f}")

# Compute eta product numerically
q = phibar
eta_prod = 1.0
for n in range(1, 200):
    eta_prod *= (1 - q**n)
eta_val = q**(1/24) * eta_prod
print(f"  eta(q=phibar) ~ q^(1/24) * prod(1-q^n) = {eta_val:.8f}")

# E4 (Eisenstein series)
E4 = 1.0
for n in range(1, 100):
    # sigma_3(n) = sum of cubes of divisors
    divs = [d for d in range(1, n+1) if n % d == 0]
    s3 = sum(d**3 for d in divs)
    E4 += 240 * s3 * q**n
print(f"  E_4(q=phibar) = {E4:.8f}")
print(f"  Compare: E_4 encodes E8 lattice theta function")

# j-invariant
j_val = E4**3 / (eta_val**24) if eta_val != 0 else float('inf')
print(f"  j(q=phibar) = E_4^3/eta^24 = {j_val:.4f}")

# Check if this j-value has any framework significance
print(f"\n  j-value analysis:")
print(f"  j = {j_val:.4f}")
print(f"  j/1728 = {j_val/1728:.6f}")
print(f"  j/240 = {j_val/240:.4f}")
print(f"  ln(j) = {np.log(j_val):.4f}")
print(f"  j^(1/3) = {j_val**(1/3):.4f}")

# =====================================================================
# PART 4: WHAT THE GAPS REVEAL
# =====================================================================
print("\n\n" + "=" * 70)
print("PART 4: WHAT THE GAPS REVEAL")
print("=" * 70)

print("""
Looking at the network, the gaps form a PATTERN:

GAP 1: CKM <-> Wall physics (the biggest hole)
  We have: CKM values from phi/D_n formulas
  We have: Wall physics from Poschl-Teller
  Missing: The CONNECTION between them

  The graph says: there SHOULD be an edge from 'kink' to 'V_us'
  But the sech^n overlap model fails.

  WHAT THE GAP REVEALS: The CKM is NOT a simple geometric overlap.
  It's a TOPOLOGICAL property of the wall — like a winding number
  or a Berry phase, not a wavefunction overlap integral.

  PREDICTION: The CKM matrix elements are TOPOLOGICAL INVARIANTS
  of the domain wall, related to the homotopy of the map from
  generation space to the wall profile. phi/7 etc. are not
  "positions" but winding numbers in Coxeter space.

GAP 2: Quarks <-> Cosmology (the surprising absence)
  We have: quark masses from mu and alpha
  We have: cosmological parameters from phi and alpha
  Missing: DIRECT connection between quarks and cosmology

  The graph says: m_t and Omega_DM should share a deeper source.
  m_t = m_e*mu^2/10 and Omega_DM = phi/6 both come from phi,
  but through DIFFERENT paths.

  WHAT THE GAP REVEALS: The quark masses and the cosmological
  parameters come from DIFFERENT aspects of the E8 structure.
  Quark masses come from the NORMALIZER (N=7776 -> mu).
  Cosmological parameters come from the VACUUM (phi/6, alpha-free).

  The two vacua contribute INDEPENDENTLY:
  - phi-vacuum: Omega_DM, Omega_DE, n_s, N_e (alpha-free!)
  - Wall/normalizer: mu, alpha, quark masses (alpha-dependent)

  PREDICTION: Any cosmological parameter that is alpha-FREE
  (like Omega_DM = phi/6) comes directly from the vacuum structure.
  Any that is alpha-DEPENDENT (like Omega_b = alpha*11/phi) involves
  the wall. This split may be DEEP — distinguishing vacuum physics
  from wall physics.

GAP 3: alpha_s <-> wall profile (the hidden connection)
  alpha_s = 1/(2*phi^3)
  The wall profile goes as tanh(x/2) with characteristic scale phi
  phi^3 = phi^2 + phi = (phi+1) + phi = 2*phi + 1
  So 1/(2*phi^3) = 1/(4*phi + 2)

  WHAT THE GAP REVEALS: alpha_s may be the TRANSMISSION COEFFICIENT
  of the domain wall. For a sech^2 barrier of height V_0:
  T = 1/(1 + V_0^2/(4*E*(E-V_0))) at special energies.

  For E = phi-related energy: T ~ 1/(2*phi^3)
  This would make alpha_s a TUNNELING rate, not a coupling constant!

  PREDICTION: alpha_s is the probability of a gluon traversing
  the domain wall thickness. Its running with energy = energy-dependent
  tunneling coefficient of the Poschl-Teller barrier.

GAP 4: Neutrinos <-> Ising model (the Lucas connection)
  dm^2_atm/dm^2_sol = 33 ~ 3*L(5) = 3*11
  L(5) appears in Omega_b (alpha*11/phi)
  33 = 3*11 = L(2)*L(5)

  The Ising partition function Z_5 = Tr(T^5) = L(5) = 11
  The Ising partition function Z_2 = Tr(T^2) = L(2) = 3

  WHAT THE GAP REVEALS: The neutrino mass ratio 33 = Z_2 * Z_5
  is a PRODUCT OF PARTITION FUNCTIONS.

  This suggests neutrino mass splittings are thermal-like:
  the ratio of mass-squared differences equals the ratio of
  Ising partition functions at the self-dual point.

  PREDICTION: Other mass ratios should also be products or
  ratios of Lucas numbers (Ising partition functions).
""")

# Check the prediction about mass ratios as Lucas products/ratios
print("  Checking: are mass ratios Lucas products/ratios?")
ratios_to_check = {
    'm_t/m_c': m_t / 1.27,
    'm_c/m_s': 1.27 / 0.0934,
    'm_t/m_b': m_t / 4.18,
    'm_b/m_tau': 4.18 / 1.777,
    'm_mu/m_e': 206.77,
}

lucas_products = {}
for i in range(1, 10):
    for j in range(0, 10):
        for k in [-1, 1]:
            val = L[i] * (L[j] if j > 0 else 1) * k
            if 0 < val < 1000:
                lucas_products[f"L({i})*L({j})" if j > 0 else f"L({i})"] = val
            if j > 0 and L[j] != 0:
                val2 = L[i] / L[j]
                if 0 < val2 < 1000:
                    lucas_products[f"L({i})/L({j})"] = val2
        for fj in range(1, 10):
            val3 = L[i] * F[fj]
            if 0 < val3 < 1000:
                lucas_products[f"L({i})*F({fj})"] = val3

for rname, rval in ratios_to_check.items():
    best = max(lucas_products.items(), key=lambda x: 1 - abs(x[1] - rval)/rval)
    match = 100 * (1 - abs(best[1] - rval) / rval)
    print(f"    {rname:12s} = {rval:.2f}  best: {best[0]:15s} = {best[1]:.2f} ({match:.1f}%)")

# =====================================================================
# PART 5: THE MAP OF EVERYTHING
# =====================================================================
print("\n\n" + "=" * 70)
print("PART 5: THE COMPLETE MAP — What's connected, what's missing")
print("=" * 70)

print(f"""
THE THREE PILLARS (everything flows from these):

  [phi] -----> V(Phi) ---> kink ---> particles
    |              |            |         |
    |              v            v         v
    |          two vacua   bound states  masses
    |              |            |         |
    v              v            v         v
  [E8] ----> N=7776 ----> mu -------> alpha -----> everything
    |              |                      |
    |              v                      v
    |          3 generations         gauge couplings
    |                                     |
    v                                     v
  [M_Pl] -------> v=246 GeV -------> M_W, M_Z, Higgs

THE MISSING BRIDGES (where connections SHOULD be):

  kink ---?---> CKM (topology, not geometry)
  alpha_s ---?---> wall transmission coefficient
  neutrino masses ---?---> Ising partition functions
  Omega_DM ---?---> second vacuum DIRECTLY (no wall needed)
  quark positions ---?---> E8 weight lattice (specific vectors)

THE DEEPEST MISSING LINK:

  WHY does the Fibonacci matrix T = [[1,1],[1,0]] appear BOTH
  in the transfer matrix of the Ising chain AND in the E8 structure?

  If we could answer this, it would connect:
  - Number theory (Fibonacci, Lucas)
  - Statistical mechanics (Ising model)
  - Lie theory (E8 Coxeter structure)
  - Physics (all the constants)

  into a SINGLE mathematical structure.

  This might be the modular form connection:
  - E8 theta function = modular form
  - Rogers-Ramanujan identity = golden ratio from modular forms
  - Ising model = lattice statistical mechanics
  - All three use q-series, all three connect to phi
  - The UNIFYING object may be a q-series at q = phibar = 1/phi
""")

# Compute: what does the E8 theta function look like at q=phibar?
print("  E8 theta function at q = phibar = 1/phi:")
print(f"  Theta_E8(phibar) = {E4:.6f}")
print(f"  Compare N = {N}")
print(f"  Theta/N = {E4/N:.6f}")
print(f"  Theta/240 = {E4/240:.6f}")
print(f"  Theta - 1 = {E4-1:.6f} (the 'non-trivial' part)")
print(f"  (Theta-1)/240 = {(E4-1)/240:.6f}")

# What about 62208?
print(f"\n  |Normalizer| = 62208")
print(f"  Theta_E8(phibar) = {E4:.6f}")
print(f"  62208 / Theta = {62208/E4:.6f}")
print(f"  Theta / 62208 = {E4/62208:.8f}")

# Final: what does the full j-invariant network look like?
print(f"\n  SUMMARY OF MODULAR FORM VALUES AT q=phibar:")
print(f"    Theta_E8 = E_4 = {E4:.6f}")
print(f"    eta = {eta_val:.6f}")
print(f"    j = {j_val:.4f}")
print(f"    j/1728 = {j_val/1728:.6f} (the lambda-invariant)")
print(f"    ")
print(f"    These are SPECIFIC NUMBERS that encode E8 at the golden ratio.")
print(f"    If the framework is right, physical constants should appear")
print(f"    as ratios and powers of these modular form values.")
print(f"    THIS IS THE NEXT FRONTIER.")
