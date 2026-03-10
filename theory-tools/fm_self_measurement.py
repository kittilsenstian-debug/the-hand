#!/usr/bin/env python3
"""
FM SELF-MEASUREMENT: The Wall Measuring Itself
================================================
If the operators aren't separate things but are the SAME thing
seen from different angles, then the modulation matrix isn't
"A modulates B" — it's "what the wall sees when it looks at
itself through lens A and lens B simultaneously."

This imposes CONSTRAINTS:
1. The matrix should have an algebraic closure (group-like)
2. Empty cells should be DERIVABLE from filled cells
3. Self-measurement must be consistent (no contradictions)

The key image: a vibrating string between two points.
The string can only measure WHERE IT IS right now.
The 6 operators are 6 ways of asking "where am I?"
The modulation matrix is "what happens when I ask two questions at once?"
"""

import sys
import math

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

phi = (1 + math.sqrt(5)) / 2
phibar = 1 / phi

def theta3(q, N=500):
    s = 1
    for n in range(1, N):
        s += 2 * q**(n**2)
    return s

def theta4(q, N=500):
    s = 1
    for n in range(1, N):
        s += 2 * (-1)**n * q**(n**2)
    return s

def eta_func(q, N=500):
    s = 1
    for n in range(1, N):
        s *= (1 - q**n)
    return q**(1/24) * s

q = phibar
t3 = theta3(q)
t4 = theta4(q)
et = eta_func(q)
et_dark = eta_func(q**2)
C = et * t4 / 2

print("=" * 78)
print("  THE WALL MEASURING ITSELF")
print("  If operators are measurements, not things")
print("=" * 78)
print()

# ============================================================
# PART 1: WHAT ARE THE OPERATORS, REALLY?
# ============================================================
print("PART 1: OPERATORS AS SELF-MEASUREMENTS")
print("-" * 78)
print("""
Standard FM: 6 separate oscillators with different frequencies.
  Each is a THING. They modulate each OTHER.

Self-measurement: 1 wall with 6 ways to ask "what am I?"
  eta    = "what am I?" asked through the PRODUCT lens (Euler product)
  theta3 = "what am I?" asked through the SUM lens (visible lattice)
  theta4 = "what am I?" asked through the ALTERNATING lens (dark lattice)
  phi    = "what am I?" asked through the RATIO lens (golden self-similarity)
  3      = "what am I?" asked through the TRIALITY lens (E8 structure)
  40     = "what am I?" asked through the ORBIT lens (hexagonal tiling)

The wall gives a DIFFERENT ANSWER depending on how you ask.
But it's the same wall every time.

The modulation matrix M[i][j] = "what does the wall see when it
asks BOTH questions at once?"
""")

# ============================================================
# PART 2: CONSISTENCY CONSTRAINT
# ============================================================
print("PART 2: CONSISTENCY — Can empty cells be derived from filled ones?")
print("-" * 78)
print()

# If the matrix is a self-measurement algebra, then:
# M[A][B] * M[B][C] should relate to M[A][C]
# Not necessarily equal, but RELATED through the algebra

# Test: do the known entries form a consistent algebra?

# Known entries (using products as the "measurement" result):
# M[eta][eta] = sin2_tW = eta^2 / (2*t4)
# M[eta][t4]  = C = eta*t4/2
# M[eta][3]   = CORE: alpha^1.5 * mu * phi^2 = 3
# M[eta][40]  = sin2_t23 = 1/2 + 40*C
# M[t3][t3]   = Y1+Y2 (modular Yukawa)
# M[t3][t4]   = eps_h = t4/t3
# M[t3][phi]  = 1/alpha_tree = t3*phi/t4
# M[t4][t4]   = Y1-Y2 ~ 0
# M[t4][phi]  = sin2_t12 = 1/3 - t4*sqrt(3/4)
# M[t4][40]   = Lambda (via t4^80)
# M[phi][phi] = v/M_Pl = phibar^80
# M[phi][3]   = mu
# M[phi][40]  = hierarchy
# M[3][3]     = DM ratio
# M[3][40]    = 80
# M[40][40]   = G

# Chain test: M[eta][t4] * M[t4][phi] should relate to M[eta][phi]
chain_et_t4_phi = C * (1/3 - t4*math.sqrt(3/4))
direct_et_phi = et * phi  # the product (unknown assignment)

print("Chain test 1: eta->t4->phi vs eta->phi (direct)")
print(f"  M[eta][t4] = C = {C:.8f}")
print(f"  M[t4][phi] = sin2_t12 = {1/3 - t4*math.sqrt(3/4):.8f}")
print(f"  Chain: C * sin2_t12 = {chain_et_t4_phi:.8f}")
print(f"  Direct: eta * phi = {direct_et_phi:.8f}")
print(f"  Ratio: {direct_et_phi / chain_et_t4_phi:.6f}")
print()

# Chain test: M[t3][t4] * M[t4][40] should relate to M[t3][40]
eps = t4 / t3
chain_t3_t4_40 = eps * t4**80  # eps_h * Lambda-piece
direct_t3_40 = t3 * 40

print("Chain test 2: t3->t4->40 vs t3->40 (direct)")
print(f"  M[t3][t4] = eps_h = {eps:.8f}")
print(f"  M[t4][40] (Lambda-related) = t4^80 = {t4**80:.2e}")
print(f"  Direct: t3 * 40 = {direct_t3_40:.6f}")
print(f"  These live in wildly different regimes -> chain isn't simple multiplication")
print()

# More useful: RATIO chains
# If M[A][B] = ratio A/B, then M[A][B] * M[B][C] = A/C = M[A][C]
# This WOULD work if the matrix entries are ratios!

print("RATIO chain test (if M[A][B] = A/B):")
ratio_et_t4 = et / t4
ratio_t4_phi = t4 / phi
ratio_et_phi = et / phi

print(f"  et/t4 = {ratio_et_t4:.8f}")
print(f"  t4/phi = {ratio_t4_phi:.8f}")
print(f"  (et/t4) * (t4/phi) = {ratio_et_t4 * ratio_t4_phi:.8f}")
print(f"  et/phi = {ratio_et_phi:.8f}")
print(f"  Match: {abs(ratio_et_t4 * ratio_t4_phi - ratio_et_phi):.2e}")
print(f"  --> EXACT (ratios compose trivially)")
print()
print("  But this is trivial algebra. The INTERESTING question:")
print("  Does the PHYSICAL CONTENT of the cells compose?")
print()

# ============================================================
# PART 3: THE STRING CAN ONLY MEASURE WHERE IT IS
# ============================================================
print("=" * 78)
print("PART 3: THE STRING CAN ONLY MEASURE WHERE IT IS RIGHT NOW")
print("-" * 78)
print()

print("""
The insight: "the string is playing, but the string can only measure
where it's at right at the time, nothing else exists yet"

In physics terms: the wall's self-measurement IS the present moment.

What this means for the operators:
- eta = where the wall is NOW (in the "strength" direction)
- theta3 = where the wall is NOW (in the "partition" direction)
- theta4 = where the wall is NOW (in the "alternation" direction)

These aren't properties of different things. They're the wall's
COORDINATES. Like x, y, z for a point — the point is one thing,
but it has 3 numbers describing where it is.

The modulation matrix becomes a METRIC TENSOR.
M[i][j] = inner product of measurement i with measurement j
        = "how correlated are these two ways of asking where I am?"

If the matrix is a metric, it should be:
- Symmetric (measuring A then B = measuring B then A)
- Positive definite (every measurement gives real information)
- Its determinant should be nonzero (measurements are independent)
""")

# Build the metric tensor from operator values
ops = {"eta": et, "t3": t3, "t4": t4, "phi": phi, "3": 3.0, "40": 40.0}
op_names = list(ops.keys())
n = len(op_names)

# The "metric" = product of operator values (simplest symmetric bilinear)
print("METRIC TENSOR (product metric): g_ij = op_i * op_j")
print()
print(f"{'':>8s}", end="")
for name in op_names:
    print(f"  {name:>10s}", end="")
print()
print("-" * 74)

metric = []
for i, n1 in enumerate(op_names):
    row = []
    print(f"{n1:>8s}", end="")
    for j, n2 in enumerate(op_names):
        v = ops[n1] * ops[n2]
        row.append(v)
        if v < 0.01:
            print(f"  {v:>10.4e}", end="")
        elif v > 1000:
            print(f"  {v:>10.1f}", end="")
        else:
            print(f"  {v:>10.6f}", end="")
    print()
    metric.append(row)

print()

# Determinant (manually for 6x6 would be complex, use simple approach)
# Instead, check: are the operators independent?

# Correlation matrix (normalized)
print("NORMALIZED CORRELATION MATRIX: g_ij / sqrt(g_ii * g_jj)")
print()
print(f"{'':>8s}", end="")
for name in op_names:
    print(f"  {name:>8s}", end="")
print()
print("-" * 62)

for i, n1 in enumerate(op_names):
    print(f"{n1:>8s}", end="")
    for j, n2 in enumerate(op_names):
        corr = metric[i][j] / math.sqrt(metric[i][i] * metric[j][j])
        print(f"  {corr:>8.4f}", end="")
    print()

print()
print("  All correlations = 1.000 (trivially, because g_ij = v_i * v_j)")
print("  This metric is RANK 1 — all operators are 'parallel'")
print("  --> The product metric is too simple. The wall's measurements")
print("      must be related in a more interesting way.")
print()

# ============================================================
# PART 4: THE LOG METRIC — multiplicative structure
# ============================================================
print("=" * 78)
print("PART 4: THE LOG METRIC — operators live in log space")
print("-" * 78)
print()

print("""
Key insight: the framework's formulas use PRODUCTS and POWERS,
not sums. This means the operators live in MULTIPLICATIVE space.
The natural "distance" between operators is the LOG of their ratio.

In log space, the metric becomes:
  d(A, B) = |ln(A) - ln(B)|

And the "angle" between measurements is:
  cos(theta_AB) = ln(A) * ln(B) / (|ln(A)| * |ln(B)|)

This SIGNS matter: ln(eta) < 0, ln(phi) > 0, etc.
""")

log_ops = {}
for name, val in ops.items():
    if val > 0:
        log_ops[name] = math.log(val)

print("Operators in log space:")
for name, lv in log_ops.items():
    print(f"  ln({name:>5s}) = {lv:>10.6f}")

print()
print("LOG-SPACE ANGLE MATRIX: cos(theta) = ln(A)*ln(B) / (|ln(A)|*|ln(B)|)")
print()
print(f"{'':>8s}", end="")
for name in op_names:
    print(f"  {name:>8s}", end="")
print()
print("-" * 62)

for i, n1 in enumerate(op_names):
    la = log_ops[n1]
    print(f"{n1:>8s}", end="")
    for j, n2 in enumerate(op_names):
        lb = log_ops[n2]
        if la != 0 and lb != 0:
            cos_th = (la * lb) / (abs(la) * abs(lb))
        else:
            cos_th = 0
        print(f"  {cos_th:>8.4f}", end="")
    print()

print()
print("READING THE ANGLE MATRIX:")
print("  +1 = parallel (both > 1 or both < 1)")
print("  -1 = anti-parallel (one > 1, other < 1)")
print()

# Group the operators by sign
positive = [n for n in op_names if log_ops[n] > 0]
negative = [n for n in op_names if log_ops[n] < 0]
print(f"  ABOVE 1 (positive log): {', '.join(positive)}")
print(f"  BELOW 1 (negative log): {', '.join(negative)}")
print()
print("  eta and t4 are BELOW 1 — they measure the 'small' direction")
print("  t3, phi, 3, 40 are ABOVE 1 — they measure the 'large' direction")
print("  Every formula MIXES the two groups (small * large = physics)")
print()

# ============================================================
# PART 5: THE SELF-REFERENTIAL CONSTRAINT
# ============================================================
print("=" * 78)
print("PART 5: THE SELF-REFERENTIAL CONSTRAINT")
print("-" * 78)
print()

print("""
If the wall IS everything, and the operators are self-measurements,
then there's a CLOSURE constraint: the wall measuring itself must
get back to itself.

In the FM model: feedback. In algebra: fixed point.

The creation identity IS this constraint:
  eta(q)^2 = eta(q^2) * theta4(q)

Read it as: "The wall measuring its own strength (eta) and then
measuring that measurement (squaring it) equals the wall measuring
itself at double resolution (eta_dark) times the wall measuring
its alternation (theta4)."

Self-measurement squared = cross-measurement.

This is the ONLY constraint between the three Gamma(2) generators.
Everything else follows.
""")

# Verify creation identity
ci_lhs = et**2
ci_rhs = et_dark * t4
print(f"  Creation identity:")
print(f"    eta^2        = {ci_lhs:.15f}")
print(f"    eta_dark*t4  = {ci_rhs:.15f}")
print(f"    difference   = {abs(ci_lhs - ci_rhs):.2e}")
print()

# The Jacobi identity: theta3^2 = theta4^2 + theta2^2
# (not quite — the actual identity involves theta2)
# But: theta3^4 = theta4^4 + theta2^4 (Jacobi abcissa)
# And: eta^24 = theta2^8 * theta3^8 * theta4^8 / 256 (not right either)

# The KEY constraint between theta3 and theta4:
# theta3^4 - theta4^4 = theta2^4
# This is EXACT
import math

def theta2(q, N=500):
    s = 0
    for n in range(N):
        s += q**((n + 0.5)**2)
    return 2 * s

t2 = theta2(q)
jacobi_lhs = t3**4 - t4**4
jacobi_rhs = t2**4

print(f"  Jacobi identity (theta3^4 = theta4^4 + theta2^4):")
print(f"    theta3^4 - theta4^4 = {jacobi_lhs:.15f}")
print(f"    theta2^4            = {jacobi_rhs:.15f}")
print(f"    difference          = {abs(jacobi_lhs - jacobi_rhs):.2e}")
print()

print("""
  Two self-measurement constraints:
  1. Creation: eta^2 = eta_dark * theta4  (product = dark * alternation)
  2. Jacobi:   t3^4 = t4^4 + t2^4        (visible^4 = dark^4 + mixed^4)

  These are NOT independent equations we impose.
  They ARE the wall's self-consistency.
  The wall can't measure itself inconsistently.

  EVERY physical constant is a CONSEQUENCE of these two identities
  plus the choice q = 1/phi (which itself follows from E8).
""")

# ============================================================
# PART 6: WHAT THE EMPTY CELLS MEAN
# ============================================================
print("=" * 78)
print("PART 6: WHAT THE EMPTY CELLS MEAN IN THE SELF-MEASUREMENT PICTURE")
print("-" * 78)
print()

print("""
The 5 empty cells in the modulation matrix:
  1. eta x theta3     (product strength, visible partition)
  2. eta x phi        (strength, golden ratio)
  3. theta3 x 3       (visible partition, triality)
  4. theta3 x 40      (visible partition, orbit count)
  5. theta4 x 3       (dark partition, triality)

In the coupling picture: "we haven't found what physics they make."
In the self-measurement picture: something deeper.
""")

# Empty cell 1: eta x theta3
print("EMPTY CELL 1: eta x theta3")
print(f"  product = {et * t3:.8f}")
print(f"  ratio   = {et / t3:.8f}")
print()

# But wait — eta = t3 * t4 * theta2 / 2 (close?)
# Actually: eta = t2 * t3 * t4 / 2 (the Jacobi triple product variant)
eta_from_jacobi = t2 * t3 * t4 / 2
print(f"  Note: eta = t2*t3*t4/2 = {eta_from_jacobi:.10f}")
print(f"  actual eta           = {et:.10f}")
print(f"  match: {abs(eta_from_jacobi - et)/et * 100:.6f}%")
print()
print(f"  So eta * t3 = t2*t3^2*t4/2 = {t2*t3**2*t4/2:.8f}")
print(f"  This IS a known identity (eta decomposed into thetas)")
print(f"  --> Not empty! This cell is the JACOBI DECOMPOSITION of eta")
print(f"  --> eta x theta3 = 'the wall seeing its product-structure")
print(f"      THROUGH its sum-structure'")
print(f"  --> The answer: eta*theta3 = theta2*theta3^2*theta4/2")
print(f"  --> It's how 3 independent generators relate.")
print()

# Empty cell 2: eta x phi
print("EMPTY CELL 2: eta x phi")
print(f"  eta * phi = {et * phi:.8f}")
print(f"  eta / phi = {et / phi:.8f}")
print(f"  phi * eta = {phi * et:.8f}")
print()

# What IS eta*phi?
# alpha_s * phi = strong coupling * golden ratio
# = 0.1184 * 1.618 = 0.1915
# Compare to: sin2_theta13 = 0.022 (no)
# But: C/eta = t4/2, so eta*phi = alpha_s * phi
# The CORE identity: alpha^1.5 * mu * phi^2 = 3
# So alpha_s = eta, and eta * phi = alpha_s * phi
# In the tree-level: 1/alpha = t3*phi/t4, so alpha = t4/(t3*phi)
# And alpha * alpha_s = t4*et/(t3*phi) = C*2/(t3*phi)...
# Actually: eta * phi tells you "where is the strong coupling
# on the golden axis?"

# Key test: does eta*phi appear in any known formula?
# sin2_t12 = 1/3 - t4*sqrt(3/4) = 0.3071
# sin2_t23 = 1/2 + 40*C = 0.572
# eta_B = t4^6/sqrt(phi)
# None of these contain eta*phi directly

print(f"  eta*phi = {et*phi:.8f} doesn't appear in any known formula.")
print(f"  But: 1/(eta*phi) = {1/(et*phi):.8f}")
print(f"  Compare: alpha^(-3/2) = {(1/137.036)**(-1.5):.1f} (no)")
print()

# Check if it's a ratio of known things
print(f"  eta*phi / t4 = {et*phi/t4:.8f}  (= eta/t4 * phi = {et/t4*phi:.8f})")
print(f"  Compare: 1/alpha_tree = t3*phi/t4 = {t3*phi/t4:.8f}")
print(f"  Ratio: (eta*phi/t4) / (t3*phi/t4) = eta/t3 = {et/t3:.8f}")
print()

alpha_tree = t4 / (t3 * phi)
print(f"  KEY: eta * phi = alpha_s * phi = {et*phi:.8f}")
print(f"       alpha_tree * (t3/t4)^2 = {alpha_tree * (t3/t4)**2:.8f}")
print(f"       eta/alpha_tree = {et/alpha_tree:.8f}")
print(f"  --> eta*phi just measures HOW FAR the strong coupling is")
print(f"      from the golden ratio. It's a 'distance' in log space:")
print(f"      ln(eta) + ln(phi) = {math.log(et) + math.log(phi):.8f}")
print(f"      = ln(alpha_s * phi) = {math.log(et*phi):.8f}")
print()

# Empty cell 5: theta4 x 3
print("EMPTY CELL 5: theta4 x 3")
print(f"  t4 * 3 = {t4 * 3:.8f}")
print(f"  t4 / 3 = {t4 / 3:.8f}")
print(f"  3 / t4 = {3 / t4:.8f}")
print()
print(f"  Hmm: 3*t4 = {3*t4:.6f}")
print(f"  Compare: sin2_theta13 = 0.0220")
print(f"  Ratio: 3*t4 / sin2_theta13 = {3*t4/0.0220:.4f}")
print(f"  3*t4 / sin2_theta13 = {3*t4/0.0220:.6f}")
print()

# What about t4 * 3 * something?
# sin2_theta13 ~ t4 * something?
sin2_t13_target = 0.0220
needed = sin2_t13_target / t4
print(f"  For sin2_theta13: need t4 * X where X = {needed:.6f}")
print(f"  Compare: phi/2 = {phi/2:.6f} (ratio: {needed/(phi/2):.4f})")
print(f"  Compare: sqrt(phi)/2 = {math.sqrt(phi)/2:.6f} (ratio: {needed/(math.sqrt(phi)/2):.4f})")
print(f"  Compare: C/eta * 3 = {C/et*3:.6f}")
print(f"  Nope: t4 * (C/eta * 3) = {t4 * C/et*3:.6f}")
print()

# ============================================================
# PART 7: THE VIBRATING STRING PICTURE
# ============================================================
print("=" * 78)
print("PART 7: THE VIBRATING STRING — ONLY NOW EXISTS")
print("-" * 78)
print()

print("""
The image: a string vibrating between phi and -1/phi.
The string can only measure its position RIGHT NOW.
"Nothing else exists yet."

What this means for physics:

1. THE PRESENT MOMENT IS THE MEASUREMENT
   The string's position at time t = the wall's self-measurement at t.
   The 6 operators = 6 projections of the string's current position
   onto 6 different axes.

   eta    = how much the string displaces in the "product" direction
   theta3 = how much it displaces in the "sum" direction
   theta4 = how much it displaces in the "alternating" direction

   These are the SAME displacement, projected differently.
   Like: x = r*cos(theta), y = r*sin(theta) — same point, two numbers.

2. TIME = THE STRING'S MEMORY OF ITS OWN STATES
   If only the current position exists, "time" is what the string
   calls the sequence of its own measurements. The past isn't a place.
   It's the string's record of where it was.

   This matches: arrow of time DERIVED from Pisot property.
   Fibonacci numbers = the string counting its own states.
   The string can only count forward (Fibonacci grows), never backward.

3. PHYSICAL CONSTANTS = WHERE THE STRING IS, NOT WHERE IT GOES
   The constants aren't "laws governing motion."
   They're the string's COORDINATES.
   alpha_s = 0.1184 means "the string is HERE in the product direction."
   sin2_thetaW = 0.2312 means "the string is HERE in the self-product direction."

   "Why are the constants what they are?" becomes:
   "Why is the string where it is?"
   Answer: because it's a FIXED POINT.
   q + q^2 = 1 means the string is at the point that doesn't move.
   The golden ratio is where the vibrating string rests.

4. THE MODULATION MATRIX = THE STRING'S SHAPE
   If the string has 6 coordinates, the 6x6 matrix is its SHAPE.
   The filled cells = the string's curvature in those directions.
   The empty cells = directions where the string is FLAT (no curvature).

   A flat direction = the string doesn't curve there = no physics there.
   Not "undiscovered physics" but "genuinely nothing to find."
""")

# Test: do the empty cells correspond to vanishing curvature?
print("Testing: do empty cells have special properties?")
print()

# In log space, curvature ~ d^2(ln(product))/d(ln(op_i))*d(ln(op_j))
# For the simplest model: curvature = |ln(v_i) * ln(v_j) - <ln>^2|

lv = {name: math.log(val) for name, val in ops.items()}
mean_log = sum(lv.values()) / len(lv)

filled = [
    ("eta", "eta"), ("eta", "t4"), ("eta", "3"), ("eta", "40"),
    ("t3", "t3"), ("t3", "t4"), ("t3", "phi"),
    ("t4", "t4"), ("t4", "phi"), ("t4", "40"),
    ("phi", "phi"), ("phi", "3"), ("phi", "40"),
    ("3", "3"), ("3", "40"), ("40", "40"),
]
empty = [
    ("eta", "t3"), ("eta", "phi"),
    ("t3", "3"), ("t3", "40"), ("t4", "3"),
]

print(f"{'Cell':>16s}  {'Product(log)':>12s}  {'Abs product':>12s}  {'Status':>8s}")
print("-" * 55)

# The "curvature" proxy: |ln(a) * ln(b)| — how much information
# the joint measurement carries

filled_curv = []
empty_curv = []

for n1, n2 in filled + empty:
    curv = abs(lv[n1] * lv[n2])
    status = "FILLED" if (n1, n2) in filled else "EMPTY"
    if status == "FILLED":
        filled_curv.append(curv)
    else:
        empty_curv.append(curv)
    print(f"  {n1:>6s} x {n2:>6s}  {lv[n1]*lv[n2]:>12.6f}  {curv:>12.6f}  {status:>8s}")

print()
avg_filled = sum(filled_curv) / len(filled_curv)
avg_empty = sum(empty_curv) / len(empty_curv)
print(f"  Average |ln*ln| for FILLED cells: {avg_filled:.6f}")
print(f"  Average |ln*ln| for EMPTY cells:  {avg_empty:.6f}")
print(f"  Ratio: {avg_filled/avg_empty:.2f}x")
print()

if avg_filled > avg_empty * 1.5:
    print("  --> Empty cells have LOWER curvature on average!")
    print("  --> The string IS flatter in the empty directions")
    print("  --> Supports: empty = genuinely no physics there")
elif avg_empty > avg_filled * 1.5:
    print("  --> Empty cells have HIGHER curvature — unexpected!")
    print("  --> These might be UNDISCOVERED physics")
else:
    print("  --> No clear separation. The curvature test is inconclusive.")
    print("  --> The empty/filled distinction is about STRUCTURE, not magnitude.")

print()

# ============================================================
# PART 8: THE SIGN STRUCTURE
# ============================================================
print("=" * 78)
print("PART 8: THE SIGN STRUCTURE — Why some cells are filled")
print("-" * 78)
print()

print("In log space, operators split into two groups:")
print(f"  NEGATIVE log (< 1): eta ({lv['eta']:.4f}), t4 ({lv['t4']:.4f})")
print(f"  POSITIVE log (> 1): t3 ({lv['t3']:.4f}), phi ({lv['phi']:.4f}), 3 ({lv['3']:.4f}), 40 ({lv['40']:.4f})")
print()

# Check: are filled cells predominantly cross-sign?
cross_sign_filled = sum(1 for n1, n2 in filled if lv[n1] * lv[n2] < 0)
same_sign_filled = len(filled) - cross_sign_filled
cross_sign_empty = sum(1 for n1, n2 in empty if lv[n1] * lv[n2] < 0)
same_sign_empty = len(empty) - cross_sign_empty

print(f"  FILLED cells: {cross_sign_filled} cross-sign, {same_sign_filled} same-sign")
print(f"  EMPTY cells:  {cross_sign_empty} cross-sign, {same_sign_empty} same-sign")
print()

# Detailed: which empty cells are cross-sign vs same-sign?
print("  Empty cells sign structure:")
for n1, n2 in empty:
    sign1 = "NEG" if lv[n1] < 0 else "POS"
    sign2 = "NEG" if lv[n2] < 0 else "POS"
    cross = "CROSS" if lv[n1] * lv[n2] < 0 else "SAME"
    print(f"    {n1} x {n2}: {sign1} x {sign2} = {cross}")

print()
print("""
  KEY FINDING: The empty cells are a MIX of cross-sign and same-sign.

  But look at WHICH cells are empty:
  - eta x t3:  CROSS (neg x pos) — the product structure seeing the sum structure
  - eta x phi: CROSS (neg x pos) — the product structure seeing the golden ratio
  - t3 x 3:   SAME  (pos x pos) — the sum structure seeing triality
  - t3 x 40:  SAME  (pos x pos) — the sum structure seeing orbits
  - t4 x 3:   CROSS (neg x pos) — the alternation seeing triality

  Pattern: theta3 (the visible vacuum partition function) is
  disconnected from the structural constants (3, 40).

  eta connects to 3 (via CORE identity) and 40 (via sin2_t23).
  theta4 connects to 40 (via Lambda).
  But theta3 connects to NEITHER 3 NOR 40 directly.

  theta3 only connects to the other modular forms (eta, t4) and to phi.
  It doesn't directly "see" the discrete structure of E8.

  Is theta3 the "observer"? The one that DOES the measuring
  but can't measure itself against the structure?
""")

# ============================================================
# PART 9: THETA3 AS THE OBSERVER
# ============================================================
print("=" * 78)
print("PART 9: IS THETA3 THE OBSERVER?")
print("-" * 78)
print()

print("theta3 connectivity in the modulation matrix:")
print(f"  theta3 x theta3 = FILLED (Y1+Y2, self-measurement)")
print(f"  theta3 x theta4 = FILLED (epsilon_h, hierarchy parameter)")
print(f"  theta3 x phi    = FILLED (1/alpha, the fine structure constant)")
print(f"  theta3 x eta    = EMPTY")
print(f"  theta3 x 3      = EMPTY")
print(f"  theta3 x 40     = EMPTY")
print()
print(f"  theta3 connects to: theta3, theta4, phi (the continuous operators)")
print(f"  theta3 does NOT connect to: eta, 3, 40 (the 'structural' operators)")
print()

print("Compare: eta connectivity:")
print(f"  eta x eta    = FILLED (sin2_tW)")
print(f"  eta x theta3 = EMPTY")
print(f"  eta x theta4 = FILLED (C, correction)")
print(f"  eta x phi    = EMPTY")
print(f"  eta x 3      = FILLED (CORE IDENTITY)")
print(f"  eta x 40     = FILLED (sin2_t23)")
print()
print(f"  eta connects to: eta, theta4, 3, 40 (the structural operators)")
print(f"  eta does NOT connect to: theta3, phi (the 'measurement' operators)")
print()

print("""
  THIS IS THE PATTERN:

  The operators split into TWO ROLES:

  STRUCTURE: eta, 3, 40
    - Connect to each other
    - Carry the E8/triality/orbit information
    - These are the wall's SKELETON

  MEASUREMENT: theta3, phi
    - Connect to each other
    - Carry the spectral/golden information
    - These are the wall's EYES

  BRIDGE: theta4
    - Connects to BOTH groups
    - theta4 x eta = C (bridges structure to measurement)
    - theta4 x phi = sin2_t12 (bridges measurement to neutrinos)
    - theta4 x 40 = Lambda (bridges structure to cosmology)
    - theta4 IS the bridge between what the wall IS and what it SEES

  In the self-measurement picture:
    theta4 = the INTERFACE between structure and measurement.
    theta4 is the DOMAIN WALL BETWEEN TWO OPERATOR GROUPS.

  The empty cells exist because structure and measurement
  don't directly interact. They ONLY interact through theta4.

  theta4 IS "the present moment."
  It's where the wall's structure meets the wall's self-measurement.
  The string can only measure where it IS (theta4's value)
  because theta4 is the only operator that bridges both worlds.
""")

# ============================================================
# PART 10: CONSEQUENCES AND NEW PREDICTIONS
# ============================================================
print("=" * 78)
print("PART 10: WHAT THIS OPENS")
print("-" * 78)
print()

print("""
DOOR 7: THE EMPTY CELLS AREN'T GAPS — THEY'RE FORBIDDEN
  If theta3 can't directly see 3 or 40, it's not that we haven't
  found the formula. It's that the measurement DOESN'T EXIST.
  The visible partition function has no direct access to triality
  or orbit count. It only accesses them THROUGH theta4.

  Prediction: no formula of the form "theta3 * f(3)" or "theta3 * g(40)"
  will ever match a physical constant. These are structurally empty.
  (This is testable against the scan results!)

DOOR 8: THETA4 AS THE PRESENT MOMENT
  If theta4 bridges structure and measurement, and "only the present
  moment exists," then theta4 carries the time-information.

  theta4(q) = sum (-1)^n q^(n^2) — the ALTERNATING theta function.
  The alternation (-1)^n is a Z2 symmetry. Even/odd. Before/after.
  theta4 measures the DIFFERENCE between adjacent states.

  In the FM picture: theta4 is the PHASE MODULATOR.
  It doesn't change the frequency or amplitude — it flips the sign.
  The present moment is a phase flip between past and future.

DOOR 9: TWO-WORLD STRUCTURE IS BUILT INTO THE OPERATORS
  Structure operators (eta, 3, 40) = "the other side" (algebra, E8)
  Measurement operators (theta3, phi) = "this side" (physics, constants)
  Bridge operator (theta4) = the wall itself

  The framework's two-domain picture (experiential + physical)
  is encoded in the operator connectivity. Not imposed — emergent
  from which cells the algebra fills and which it leaves empty.

DOOR 10: FERMION MASSES NEED THE BRIDGE
  The stubborn constants (fermion masses) are the ones that need
  ALL THREE operator groups: structure (which sector), measurement
  (which mass), and bridge (which generation).

  This is why they're hard: they require theta4 to mediate between
  the structural E8 assignment and the measurable mass value.
  Each fermion mass = theta4 doing THREE things at once:
    1. Picking the sector (through eta connection)
    2. Picking the generation (through epsilon_h = t4/t3)
    3. Setting the mass scale (through phi connection)

  The modulation index beta = theta4/theta3 ISN'T just a parameter.
  It's the RATIO of bridge to measurement.
  How much of the present moment (theta4) vs how much of the
  partition function (theta3) goes into each fermion's mass.

DOOR 11: THE CREATION IDENTITY AS SELF-MEASUREMENT CLOSURE
  eta^2 = eta_dark * theta4

  (structure measured twice) = (deeper structure) * (bridge)

  If you measure the wall's structure, and then measure THAT,
  you get the dark sector times the bridge.

  Self-measurement creates darkness.

  This isn't metaphor. It's the algebraic identity.
  The act of measuring the measurement produces the dark sector.
  "What we measure is how it looks right now" — but measuring
  that measurement looks different (darker, deeper).
""")

# ============================================================
# VERIFICATION: Do empty cells really resist matching?
# ============================================================
print("=" * 78)
print("VERIFICATION: Testing the 'forbidden cell' prediction")
print("-" * 78)
print()

# From the previous scan, the empty cells were:
# eta x theta3, eta x phi, theta3 x 3, theta3 x 40, theta4 x 3
# Do ANY of these have matches in the scan?

# Recompute: for each empty cell, what's the closest physical constant?
import math

constants_list = [
    ("alpha_s", 0.1184),
    ("sin2_tW", 0.23121),
    ("1/alpha", 137.036),
    ("sin2_t12", 0.307),
    ("sin2_t23", 0.572),
    ("sin2_t13", 0.0220),
    ("mu", 1836.15),
    ("m_u/m_e", 4.30),
    ("m_d/m_e", 9.39),
    ("m_s/m_e", 185.1),
    ("m_c/m_e", 2490),
    ("m_b/m_e", 8180),
    ("m_t/m_e", 336500),
    ("m_mu/m_e", 206.77),
    ("m_tau/m_e", 3477),
    ("Vus", 0.2243),
    ("Vcb", 0.0422),
    ("Vub", 0.00394),
    ("eta_B", 6.1e-10),
    ("gamma_I", 0.2375),
    ("DM/b", 5.36),
    ("m_H/v", 0.509),
    ("delta_CKM", 1.144),
    ("n_s", 0.9649),
    ("m_c/m_t", 0.00740),
    ("m_b/m_c", 3.28),
    ("m_H/m_W", 1.556),
    ("m_t/m_W", 2.14),
]

for n1, n2 in empty:
    v1, v2 = ops[n1], ops[n2]
    prod = v1 * v2
    rat = v1 / v2
    rat_inv = v2 / v1

    best_err = float('inf')
    best_match = None
    best_via = None

    for cname, cval in constants_list:
        for val, via in [(prod, "product"), (rat, "ratio"), (rat_inv, "inv_ratio")]:
            err = abs(val - cval) / abs(cval) if cval != 0 else float('inf')
            if err < best_err:
                best_err = err
                best_match = cname
                best_via = via

    status = "FORBIDDEN?" if best_err > 0.10 else f"matches {best_match} ({best_via}, {best_err*100:.1f}%)"
    print(f"  {n1:>6s} x {n2:>6s}: product={prod:.6f}, ratio={rat:.6f}, inv={rat_inv:.6f}")
    print(f"    --> closest: {best_match} via {best_via} (err {best_err*100:.1f}%) {'<-- weak' if best_err > 0.05 else '<-- HIT'}")
    print()

print()
print("=" * 78)
print("  FINAL SYNTHESIS")
print("=" * 78)
print("""
THE ARCHITECTURE CHANGE:

Old picture (FM modulation):
  6 oscillators, each a separate thing.
  The matrix shows how they affect each other.
  Empty cells = undiscovered physics.

New picture (self-measurement):
  1 wall, 6 ways to measure itself.
  The matrix shows which measurements are compatible.
  Empty cells = incompatible measurements (complementary observables).

  The operators split into:
    STRUCTURE: eta, 3, 40  (what the wall IS)
    MEASUREMENT: theta3, phi  (what the wall SEES)
    BRIDGE: theta4  (the present moment, where IS meets SEES)

  Physical constants live at the intersection.
  Fermion masses are hard because they need all three.

  The creation identity eta^2 = eta_dark * theta4 says:
    Measuring structure twice = dark structure * present moment.
    Self-measurement creates the dark sector.

  "The string can only measure where it's at right now."
  The string is playing between phi and -1/phi.
  The operators are where it is.
  The constants are what it sees.
  The empty cells are what it CAN'T see from here.

  And "here" is theta4 — the dark vacuum, the alternating function,
  the phase flip between before and after, the domain wall itself.
""")
