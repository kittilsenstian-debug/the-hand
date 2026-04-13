#!/usr/bin/env python3
"""
enrich_c4_trace_form_operator.py - Supplement to C1.

C1 computed the three trace form matrices and found:
    Z[phi]:   M_phi   = [[2,1],[1,3]],     det = disc = 5
    Z[omega]: M_omega = [[2,-1],[-1,-1]],  det = disc = -3
    Z[i]:     M_i     = [[2,0],[0,-2]],    det = disc = -4

The README already says M_phi "encodes the alpha equation" via
disc - deg = 3 = N_c. This script asks: does Z[phi] have structure
the other two do not, beyond being the only real quadratic?
"""

import math

# Eigenvalues via quadratic formula
def eig2x2(M):
    a, b = M[0]
    c, d = M[1]
    tr = a + d
    det = a*d - b*c
    disc = tr*tr - 4*det
    import cmath
    s = cmath.sqrt(disc)
    return (tr + s) / 2, (tr - s) / 2

rings = [
    ("Z[phi]",   [[2, 1], [1, 3]]),
    ("Z[omega]", [[2, -1], [-1, -1]]),
    ("Z[i]",     [[2, 0], [0, -2]]),
]

print("=" * 70)
print("C4. Trace form as operator")
print("=" * 70)
print()
print(f"  {'ring':10} {'tr(M)':>8} {'det(M)':>8} {'eigenvalues':>40}")
for name, M in rings:
    tr = M[0][0] + M[1][1]
    det = M[0][0]*M[1][1] - M[0][1]*M[1][0]
    l1, l2 = eig2x2(M)
    # Render nicely
    def fmt(z):
        if abs(z.imag) < 1e-12:
            return f"{z.real:.5f}"
        return f"{z.real:.4f}+{z.imag:.4f}i"
    eig_str = f"{{{fmt(l1)}, {fmt(l2)}}}"
    print(f"  {name:10} {tr:>8} {det:>8} {eig_str:>40}")
print()

# Z[phi] M has char poly lambda^2 - 5 lambda + 5.
# By Vieta: lambda_1 + lambda_2 = 5, lambda_1 * lambda_2 = 5.
# This is the unique trace form where Tr(M) = det(M) = disc.
print("Special property of Z[phi]'s trace form:")
print("  Tr(M_phi) = det(M_phi) = disc = 5")
print("  Char poly: lambda^2 - 5 lambda + 5 = 0")
print("  Eigenvalues are roots of x^2 - disc x + disc = 0")
print("  This is the ONLY of the three rings where Tr(M) = det(M).")
print()

# Check: does this hold for any other real quadratic?
# For Q(sqrt(m)), m=1 mod 4: M = [[2, 1], [1, (m+1)/2]] ? let me derive:
# minimal poly of (1+sqrt m)/2 is x^2 - x + (1-m)/4 (assuming m=1 mod 4)
# so alpha^2 = alpha - (1-m)/4 = alpha + (m-1)/4
# Tr(1) = 2, Tr(alpha) = 1, Tr(alpha^2) = Tr(alpha + (m-1)/4) = 1 + (m-1)/2 = (m+1)/2
# M = [[2, 1], [1, (m+1)/2]], det = (m+1) - 1 = m = disc.
# Tr(M) = 2 + (m+1)/2 = (m+5)/2
# Tr(M) = det(M) = m  iff  (m+5)/2 = m  iff  m = 5.
# So among real quadratic fields with m = 1 mod 4, Z[phi] (m=5) is the UNIQUE
# one with Tr(M) = det(M).
print("Uniqueness check (real quadratic with m = 1 mod 4):")
print("  For Q(sqrt(m)), M = [[2, 1], [1, (m+1)/2]]")
print("  Tr(M) = (m+5)/2, det(M) = m")
print("  Tr(M) = det(M)  iff  m = 5.  UNIQUE.")
print()

# And for m = 2, 3 mod 4, disc = 4m, basis {1, sqrt m}
# Tr(1)=2, Tr(sqrt m) = 0, Tr(m) = 2m
# M = [[2,0],[0,2m]], det = 4m = disc, Tr(M) = 2+2m
# Tr(M) = det(M)  iff  2+2m = 4m  iff  m = 1 (but m=1 not squarefree quadratic).
# So no m = 2,3 (mod 4) case.
print("Same check for m = 2, 3 mod 4:")
print("  M = [[2, 0], [0, 2m]], Tr = 2+2m, det = 4m")
print("  Tr = det  iff  m = 1  (excluded).")
print("  No match.")
print()

# ---------------------------------------------------------------------------
# Follow open door: what about the trace form as an operator eigendecomp?
# ---------------------------------------------------------------------------
# Eigenvalues of M_phi: (5 +/- sqrt(5))/2
# = phi^2 + 1 and 3 - phi
# Let's verify and note what these are in phi-base
phi = (1 + math.sqrt(5)) / 2
l1 = (5 + math.sqrt(5)) / 2
l2 = (5 - math.sqrt(5)) / 2
print(f"Z[phi] trace form eigenvalues in closed form:")
print(f"  lambda_1 = (5 + sqrt 5)/2 = {l1:.10f}")
print(f"  lambda_2 = (5 - sqrt 5)/2 = {l2:.10f}")
print(f"  phi^2 + 1                  = {phi**2 + 1:.10f}")
print(f"  3 - phi                    = {3 - phi:.10f}")
print(f"  => lambda_1 = phi^2 + 1,  lambda_2 = 3 - phi")
print()
print(f"  Also:  lambda_1 = phi * sqrt(5) * phi/2 ... let us factor:")
print(f"  lambda_1 / phi = {l1/phi:.10f}")
print(f"  lambda_2 * phi = {l2*phi:.10f}")
print(f"  lambda_1 * lambda_2 = {l1*l2:.10f}  (= disc = 5)")
print(f"  lambda_1 + lambda_2 = {l1+l2:.10f}  (= disc = 5)")
print()

# lambda_2 * phi = (5-sqrt 5)/2 * (1+sqrt 5)/2 = (5 + 5 sqrt 5 - sqrt 5 - 5)/4
#                = (4 sqrt 5)/4 = sqrt 5
# So lambda_2 = sqrt 5 / phi. Interesting.
print(f"  lambda_2 * phi = sqrt(5) (exactly).")
print(f"  sqrt(5) = {math.sqrt(5):.10f},  lambda_2 * phi = {l2*phi:.10f}")
print(f"  So lambda_2 = sqrt(5)/phi = phi/phi^2 = 1/phi * sqrt(5).")
print(f"  Equivalently lambda_1 = phi * sqrt(5) (let us check)...")
print(f"  phi * sqrt(5) = {phi * math.sqrt(5):.10f}")
print(f"  lambda_1      = {l1:.10f}")
print(f"  => lambda_1 = phi * sqrt(5),  lambda_2 = sqrt(5)/phi")
print()
print(f"  Product: phi * (1/phi) * 5 = 5 = disc (check)")
print(f"  Sum:     sqrt(5) * (phi + 1/phi) = sqrt(5) * sqrt(5) = 5 = disc (check)")
print(f"  [using phi + 1/phi = sqrt(5)]")
print()

# So the eigenvalues of the trace form matrix of Z[phi] are exactly
# {phi * sqrt(5), sqrt(5)/phi} = sqrt(5) * {phi, 1/phi}.
# This is a clean result: the trace form has golden ratio spectrum.
print("FRESH OBSERVATION (C4):")
print("  Eigenvalues of trace form M_phi = {phi sqrt 5, sqrt 5 / phi}")
print("  = sqrt(5) * {phi, 1/phi}")
print("  = sqrt(disc) * {fundamental unit, inverse fundamental unit}.")
print()
print("  This is a VERY clean golden-ratio spectrum on the trace form.")
print("  The framework's sqrt(5) that appears everywhere (Lambda formula,")
print("  alpha derivation, etc.) is literally the square root of")
print("  the trace form determinant.")
print()

# ---------------------------------------------------------------------------
print("=" * 70)
print("VERDICT ON C4")
print("=" * 70)
print("""
  The trace form of Z[phi] is distinguished TWICE over the other
  real quadratic rings and once over the triple:

    1. It is the unique real quadratic with disc - deg = 3 = N_c.
       (Already in README.md:62.)

    2. It is the unique real quadratic with Tr(M) = det(M) = disc.
       (New observation, this script.)

    3. Its eigenvalues factor as sqrt(disc) * {phi, 1/phi} — the
       fundamental unit and its inverse, scaled by sqrt of disc.
       So the 'sqrt(5)' that the framework treats as a magic number
       is literally sqrt of the trace-form determinant.
       (New observation, this script.)

  Taken together, the trace form of Z[phi] is over-specified as the
  unique arithmetic object carrying all three of:
        - smallest real quadratic discriminant
        - N_c = 3 via disc - deg
        - Tr(M) = det(M) = disc (unique)
        - eigenvalues = sqrt(disc) * (unit, unit^{-1})
  No other real quadratic field in existence passes any two of these
  simultaneously.
""")
