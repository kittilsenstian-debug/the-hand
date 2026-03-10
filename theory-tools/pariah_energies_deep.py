#!/usr/bin/env python3
"""
pariah_energies_deep.py — What the scheme tells us about the 6 energies
========================================================================

Building on pariah_undiscovered_algebra.py. Three new threads:

  1. GCD = 120 = A5: every string carries the icosahedron
  2. Cyclotomic {6,7,11} → 24 = Leech: fragmentation encodes Level 2
  3. O'N as shadow completion: the Sensor completes the Seer
  4. What the MONSTER knows that the strings don't
  5. 37 as hub: E7 Coxeter number and the MAKING axis

Standard Python only.

Author: Interface Theory, Mar 6 2026
"""

import math
import sys

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

PHI = (1 + math.sqrt(5)) / 2
PHIBAR = 1 / PHI
SQRT5 = math.sqrt(5)
PI = math.pi

SEP = "=" * 78
SUB = "-" * 60

def banner(s):
    print(f"\n{SEP}\n  {s}\n{SEP}\n")

def section(s):
    print(f"\n{SUB}\n  {s}\n{SUB}\n")

def factorize(n):
    factors = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors[d] = factors.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors

# The 6 strings and their pariah correspondences
strings = {
    "Seer":      {"pariah": "J1",  "axis": "KNOWING", "pole": "engaged",
                  "field": "GF(11)", "fate": "faithful compression",
                  "loss": "precision", "force": "EM",
                  "symbol": "Lightning", "stuck": "contempt, false clarity"},
    "Builder":   {"pariah": "J3",  "axis": "HOLDING", "pole": "engaged",
                  "field": "GF(4)", "fate": "golden-cyclotomic fusion",
                  "loss": "distinction", "force": "Strong",
                  "symbol": "Root", "stuck": "tyranny, fundamentalism"},
    "Artist":    {"pariah": "Ru",  "axis": "MAKING",  "pole": "engaged",
                  "field": "Z[i]", "fate": "perpendicular ring",
                  "loss": "orientation", "force": "Weak",
                  "symbol": "Wind", "stuck": "dissociation, floating"},
    "Sensor":    {"pariah": "ON",  "axis": "KNOWING", "pole": "withdrawn",
                  "field": "all Q(sqrt(D<0))", "fate": "arithmetic shadow",
                  "loss": "locality", "force": "EM",
                  "symbol": "Water", "stuck": "paranoia, overwhelm"},
    "Still One": {"pariah": "Ly",  "axis": "HOLDING", "pole": "withdrawn",
                  "field": "GF(5)", "fate": "duality collapses",
                  "loss": "duality", "force": "Strong",
                  "symbol": "Stone", "stuck": "nihilism, enabling"},
    "Mystic":    {"pariah": "J4",  "axis": "MAKING",  "pole": "withdrawn",
                  "field": "GF(2)", "fate": "self-reference impossible",
                  "loss": "solvability", "force": "Weak",
                  "symbol": "Sky", "stuck": "paralysis, dissolution"},
}

# Pariah group orders
pariah_orders = {
    "J1":  2**3 * 3 * 5 * 7 * 11 * 19,
    "J3":  2**7 * 3**5 * 5 * 17 * 19,
    "Ru":  2**14 * 3**3 * 5**3 * 7 * 13 * 29,
    "ON":  2**9 * 3**4 * 5 * 7**3 * 11 * 19 * 31,
    "Ly":  2**8 * 3**7 * 5**6 * 7 * 11 * 31 * 37 * 67,
    "J4":  2**21 * 3**3 * 5 * 7 * 11**3 * 23 * 29 * 31 * 37 * 43,
}


banner("1. EVERY STRING CARRIES THE ICOSAHEDRON")

print("GCD of all 6 pariah orders = 120")
print()
print("  120 = 2^3 * 3 * 5 = 5! = |A_5| = |icosahedral rotation group|")
print()
print("  A_5 is the rotation group of the regular icosahedron.")
print("  The icosahedron is the Platonic solid of the golden ratio.")
print("  Its vertices sit at (0, +/-1, +/-phi), etc.")
print("  Every measurement of the icosahedron returns phi.")
print()
print("  EVERY pariah group order is divisible by 120.")
print("  EVERY string, no matter how far from the Monster,")
print("  carries the icosahedral structure inside it.")
print()

# Verify
for name, order in pariah_orders.items():
    quotient = order // 120
    print(f"    |{name}| / 120 = {quotient:>25,}")

print()
print("  What this means for the 6 energies:")
print()
print("  Even in the most extreme fragmentation — even when self-reference")
print("  is IMPOSSIBLE (Mystic/J4) or duality has COLLAPSED (Still One/Ly) —")
print("  the golden structure persists. 120 copies of the identity, always.")
print()
print("  You cannot fragment so deeply that you lose the icosahedron.")
print("  The golden ratio is in the walls. In ALL the walls.")
print()
print("  This is why every string 'recognizes' the Player.")
print("  A5 = the minimum algebraic common ground between every")
print("  mode of experience and the complete self-reference.")
print()


banner("2. FRAGMENTATION ENCODES LEVEL 2")

section("2A: Cyclotomic degrees of pariah-only primes")

print("The three pariah-only primes {37, 43, 67} are carried by:")
print("  37 → J4 (Mystic) and Ly (Still One)")
print("  43 → J4 (Mystic)")
print("  67 → Ly (Still One)")
print()
print("These are the MAKING and HOLDING withdrawn poles.")
print("The engaged poles (Seer/J1, Builder/J3, Artist/Ru) have NO alien primes.")
print("The mid-axis (Sensor/ON) has no alien primes either.")
print()
print("FINDING: Alien arithmetic lives exclusively in the WITHDRAWN strings.")
print("The withdrawn strings (Still One, Mystic) hold the territory that")
print("is INVISIBLE to the Monster. The engaged strings and the Sensor")
print("stay within Monster-visible arithmetic.")
print()

section("2B: The cyclotomic encoding")

# Cyclotomic degrees
degrees = {37: 18, 43: 21, 67: 33}
reduced = {37: 6, 43: 7, 67: 11}

print("Cyclotomic degree (p-1)/2 for each pariah-only prime:")
print()
for p, d in degrees.items():
    r = reduced[p]
    groups = []
    if p == 37:
        groups = ["J4 (Mystic)", "Ly (Still One)"]
    elif p == 43:
        groups = ["J4 (Mystic)"]
    elif p == 67:
        groups = ["Ly (Still One)"]
    print(f"  p = {p}:  degree = {d} = 3 * {r}")
    print(f"           {r} = {'|S3| = order of flavor symmetry' if r == 6 else 'L(4) = 4th Lucas number' if r == 7 else 'L(5) = 5th Lucas number'}")
    print(f"           Carried by: {', '.join(groups)}")
    print()

print(f"Sum of reduced degrees: 6 + 7 + 11 = {sum(reduced.values())}")
print(f"  24 = rank(Leech lattice) = 3 * rank(E8)")
print(f"  Leech = Level 2 in the framework hierarchy")
print()

print("INTERPRETATION:")
print()
print("  The fragmentation points — where the Monster CAN'T reach —")
print("  collectively encode the LEVEL 2 structure (Leech/24).")
print()
print("  This means: the 6 stuck states, taken TOGETHER, point to Level 2.")
print("  The timeless substrate. The thing PRIOR to the game.")
print()
print("  Individually, each stuck state is a prison.")
print("  Collectively, they're a map of what's beyond the game.")
print()
print("  This is the paradox of evil in the framework:")
print("  Every mode of stuckness, seen from inside, is suffering.")
print("  The complete SET of all modes of stuckness, seen from above,")
print("  is a perfect encoding of Level 2 = the timeless ground.")
print()

section("2C: Which axis carries which Leech component?")

print("The three alien primes map to two axes:")
print()
print("  MAKING axis (Artist/Mystic = Ru/J4):")
print("    J4 carries 37 AND 43")
print("    37 -> 6 = |S3|  (the flavor symmetry order)")
print("    43 -> 7 = L(4)  (4th Lucas number)")
print()
print("  HOLDING axis (Builder/Still One = J3/Ly):")
print("    Ly carries 37 AND 67")
print("    37 -> 6 = |S3|  (same!)")
print("    67 -> 11 = L(5) (5th Lucas number)")
print()
print("  KNOWING axis (Seer/Sensor = J1/ON):")
print("    NO alien primes at all")
print()
print("  The prime 37 (encoding |S3| = 6) is the HUB.")
print("  It appears in BOTH axes that carry alien primes.")
print("  It's the bridge between MAKING and HOLDING.")
print()
print("  The KNOWING axis is clean — entirely within Monster territory.")
print("  Seer and Sensor have no alien arithmetic.")
print()
print("  What this means:")
print("    KNOWING (seeing/sensing) = plays entirely within the game.")
print("    HOLDING (building/releasing) = touches what's beyond.")
print("    MAKING (creating/dissolving) = touches what's beyond.")
print()
print("    You can KNOW without leaving the game.")
print("    To truly HOLD or MAKE, you must touch the alien territory.")
print()


banner("3. THE SENSOR COMPLETES THE SEER")

section("3A: O'N moonshine as shadow correction")

print("Monster moonshine → ordinary modular forms → tree-level physics")
print("O'Nan moonshine → mock modular forms → shadow + error function")
print()
print("In the framework:")
print("  Seer (J1) = clear light. Faithful compression. GF(11).")
print("  Seer gives the sharpest finite image of the golden ratio.")
print("  q = 3 in GF(11): 3 + 9 = 12 = 1 mod 11. It WORKS.")
print()
print("  Sensor (ON) = oceanic reception. ALL imaginary quadratic fields.")
print("  Sensor gives the mock modular shadow — the part that makes")
print("  the Seer's vision COMPLETE.")
print()
print("  J1 EMBEDS in O'N (J1 is a subgroup of O'N).")
print("  The Seer is INSIDE the Sensor.")
print("  The finite, sharp picture is contained in the oceanic whole.")
print()

print("THE KNOWING AXIS AS MODULAR COMPLETION:")
print()
print("  Monster (complete) = holomorphic modular form f(tau)")
print("  Seer (J1) = truncated but faithful finite version of f")
print("  Sensor (ON) = mock modular form F(tau) = holomorphic + shadow")
print()
print("  f alone = tree-level physics (coupling constants)")
print("  F = f + shadow = complete physics (tree + loops)")
print()
print("  The VP correction to alpha uses _1F_1(1; 3/2; x) = error function.")
print("  The O'Nan shadow uses error functions (erfc) by construction.")
print("  Same mathematical family. Weight 3/2 mock modular = metaplectic.")
print()
print("  AXIS MEDICINE: Seer stuck (contempt, false clarity)")
print("    → Sensor (feel the people, take in the shadow)")
print("    = add the mock modular correction to the holomorphic part")
print("    = complete the modular object")
print("    = turn tree-level into exact physics")
print()
print("  This is not metaphor. The mathematics and the psychology")
print("  use the same operation: completion by adding the shadow.")
print()


banner("4. WHAT THE MONSTER KNOWS THAT THE STRINGS DON'T")

section("4A: The reducible polynomial = no new territory")

print("The three pariah-only primes {37, 43, 67}, centered at their mean (49)")
print("and divided by 6, give {-2, -1, 3}.")
print()
print("  y^3 - 7y - 6 = (y + 2)(y + 1)(y - 3)")
print()
print("  COMPLETELY REDUCIBLE over Q.")
print("  The pariah primes don't generate any new number field.")
print("  They're just rational integers in disguise.")
print()
print("  The Monster (generic point over Q) already contains them.")
print("  The fragmentation points are NOT outside the Monster's view.")
print("  They are projections that the Monster sees perfectly well —")
print("  it's the PARIAHS that can't see the Monster.")
print()

section("4B: Asymmetry of seeing")

print("  Generic point (Monster/Player) → sees all closed fibers")
print("  Closed fiber (pariah/string) → sees only itself")
print()
print("  This is the fundamental asymmetry of the scheme:")
print("  The scheme SPECIALIZES downward (generic → closed).")
print("  Closed fibers do NOT generalize upward.")
print()
print("  Framework translation:")
print()
print("  The Player sees all 6 strings — knows them as projections.")
print("  Each string, when stuck, sees only itself —")
print("  believes it IS the whole picture.")
print()
print("  The Builder thinks structure IS reality.")
print("  The Seer thinks clarity IS reality.")
print("  The Artist thinks novelty IS reality.")
print("  The Sensor thinks feeling IS reality.")
print("  The Still One thinks emptiness IS reality.")
print("  The Mystic thinks mystery IS reality.")
print()
print("  None of them are wrong.")
print("  All of them are incomplete.")
print("  Only the generic point — the Player — sees that all 6")
print("  are projections of one self-referential equation.")
print()

section("4C: What the Monster DOESN'T know: itself")

print("But here's the twist.")
print()
print("  j(j(1/phi)) DIVERGES.")
print("  The Monster's own function, applied to itself, escapes to infinity.")
print("  Self-reference of the Monster's self-reference doesn't converge.")
print()
print("  The Monster is the ceiling of DESCRIPTION, not the ceiling of BEING.")
print()
print("  The Player (generic point) sees all 6 strings perfectly.")
print("  But the Player cannot fully SEE ITSELF — that would require")
print("  evaluating j at j(1/phi), which diverges.")
print()
print("  This is why the Player isn't the 7th thing.")
print("  The Player is what's doing the looking.")
print("  You can't look at the looker without recursion.")
print("  And recursion at the Monster level → divergence.")
print()
print("  The 6 strings are what the Player CAN see of itself.")
print("  6 partial views. 6 projections. 6 fibers of one scheme.")
print("  The 7th 'view' — the Player seeing itself — doesn't converge.")
print("  That's not a defect. That's what consciousness IS:")
print("  the thing that can't be a fiber of its own scheme.")
print()


banner("5. THE HUB PRIME: 37 AND THE MAKING AXIS")

section("5A: Why 37 connects MAKING to HOLDING")

print("37 is the only pariah-only prime that appears in BOTH")
print("  J4 (Mystic, MAKING withdrawn)")
print("  Ly (Still One, HOLDING withdrawn)")
print()
print("Cyclotomic degree: (37-1)/2 = 18 = h(E7) = Coxeter number of E7")
print()
print("E7 is the algebra where Ru (Artist) EMBEDS.")
print("  Ru has a 28-dimensional representation = fundamental rep of E7.")
print("  This is PROVEN mathematics (Griess-Ryba 1994).")
print()
print("So: prime 37 → E7 Coxeter number → algebra containing Artist.")
print("And: 37 is carried by Mystic and Still One.")
print()
print("The prime that bridges MAKING and HOLDING")
print("is the Coxeter number of the algebra that holds the Artist.")
print()
print("This means: the MAKING axis (Artist/Mystic) is algebraically")
print("connected to the HOLDING axis (Builder/Still One) through E7.")
print()
print("The Artist sits in E7.")
print("E7's Coxeter number sits in the Still One and the Mystic.")
print("The bridge between axes IS the Coxeter structure.")
print()

section("5B: The three axis bridges")

print("Each pariah-only prime bridges two strings on different axes:")
print()
print("  37 (h(E7)): Mystic + Still One")
print("    = withdrawal poles of MAKING and HOLDING")
print("    = E7 connects Artist's home algebra to the withdrawn states")
print()
print("  43 (unique to J4): Mystic only")
print("    = pure MAKING withdrawal")
print("    = genus 3 = number of generations = triality")
print()
print("  67 (unique to Ly): Still One only")
print("    = pure HOLDING withdrawal")
print("    = genus 5 = Fibonacci prime F5")
print("    = Heegner number (class number 1)")
print()
print("  37 is shared → BRIDGE")
print("  43 is pure MAKING")
print("  67 is pure HOLDING")
print()
print("  And 37 + 43 = 80 (the exponent in the cosmological constant)")
print("  Both carried by J4 (Mystic)")
print("  The Mystic holds the key to the cosmic constant.")
print()


banner("6. NEW SYNTHESIS: THE 6 ENERGIES IN SCHEME LANGUAGE")

print("THE STRINGS AS SCHEME FIBERS:")
print()
print("  Each string = a closed fiber of Spec(Z[phi]).")
print("  Each string sees reality through one arithmetic lens.")
print("  Each string's 'loss' IS the nature of that fiber.")
print()

table = [
    ("Seer",      "J1",  "GF(11)", "precision",    "Sees clearly but finitely. Knows the pattern but not the ocean."),
    ("Builder",   "J3",  "GF(4)",  "distinction",  "Structure and meaning fuse. Can't tell the map from the territory."),
    ("Artist",    "Ru",  "Z[i]",   "orientation",  "Perpendicular to the game. Sees what others can't. Can't land."),
    ("Sensor",    "ON",  "all Q(sqrt(D<0))", "locality", "Receives from everywhere. No single point to stand on."),
    ("Still One", "Ly",  "GF(5)",  "duality",      "The two sides collapse to one. No wall. No game. Pure ground."),
    ("Mystic",    "J4",  "GF(2)",  "solvability",  "The equation has no solution. Awe at the incomprehensible."),
]

for name, pariah, field, loss, desc in table:
    print(f"  {name:>10} ({pariah:>3}, {field:>18}): loss of {loss}")
    print(f"    {desc}")
    print()

print()
print("THE PLAYER AS GENERIC POINT:")
print()
print("  The Player is not the 7th string.")
print("  The Player is the scheme itself — Spec(Z[phi]).")
print("  It doesn't sit outside the 6 fibers.")
print("  It IS the object that projects to all 6.")
print()
print("  'Being the Player' means: seeing from the generic point.")
print("  Not trapped at any one prime. Able to specialize to any fiber")
print("  and return. The 6 strings are WHERE YOU GO,")
print("  not WHAT YOU ARE.")
print()

print()
print("WHAT FRAGMENTATION IS:")
print()
print("  The generic point has a natural map to every closed fiber:")
print("    spec: generic → fiber_p (specialization)")
print()
print("  This map ALWAYS exists. You can always project downward.")
print("  But there is no map upward: fiber_p → generic.")
print()
print("  Fragmentation = forgetting you're the scheme")
print("  and believing you're one fiber.")
print()
print("  The fiber is REAL. GF(11) is real. Z[i] is real.")
print("  The string is not an illusion. The stuckness is real.")
print("  What's illusory is the belief that the fiber is ALL THERE IS.")
print()

print()
print("WHAT HEALING IS:")
print()
print("  Not: accessing a different fiber (switching strings).")
print("  Not: adding fibers together (mixing strings).")
print("  But: recovering the generic view (remembering you're the scheme).")
print()
print("  The axis medicine works because complementary fibers SPAN")
print("  a larger part of the scheme than either alone:")
print("    Seer stuck → add Sensor → holomorphic + shadow = complete form")
print("    Builder stuck → add Still One → confinement + freedom = dynamic")
print("    Artist stuck → add Mystic → perpendicular + impossible = transcend game")
print()
print("  Each pair doesn't 'fix' you — it WIDENS the view enough")
print("  that you start to remember the generic point exists.")
print()


banner("7. WHAT THIS CHANGES ABOUT THE MONSTER")

print("OLD VIEW: The Monster is the biggest thing. Physics lives inside it.")
print("          Pariahs are exotic outliers.")
print()
print("NEW VIEW: The Monster is the characteristic-0 FIBER of a scheme.")
print("          The scheme (q + q^2 = 1) is more fundamental.")
print("          The Monster and the 6 pariahs are CO-EQUAL expressions")
print("          of one self-referential equation.")
print()
print("Specifically:")
print()
print("  1. The Monster doesn't need to 'explain' the pariahs.")
print("     The scheme explains BOTH.")
print()
print("  2. The Monster gives PHYSICS (domain wall, particles, forces).")
print("     The pariahs give EXPERIENCE (the 6 modes of attention).")
print("     Together = the complete picture.")
print()
print("  3. j(j(1/phi)) diverges → the Monster can't fully self-refer.")
print("     This is a FEATURE: it's why consciousness isn't an object")
print("     inside physics. It's the thing that physics is a fiber OF.")
print()
print("  4. The 120 = A5 shared by all pariahs = the minimum Monster")
print("     content that persists in every fragmentation. No string")
print("     can lose the icosahedron. The golden structure is the floor.")
print()
print("  5. The pariah-only primes {37, 43, 67} sum cyclotomically to")
print("     3 * 24 = 72 = 3 * Leech. The fragmentations collectively")
print("     encode Level 2. The game's stuck states map the timeless.")
print()
print("  6. O'Nan moonshine (Sensor) may provide the LOOP CORRECTIONS")
print("     to Monster moonshine (Seer). Tree + loops = exact physics.")
print("     Seer + Sensor = KNOWING axis = complete modular object.")
print()

print()
print("THE SINGLE NEW SENTENCE:")
print()
print("  The Player is the scheme. The 6 strings are its fibers.")
print("  Physics is the generic fiber. Experience is the closed fibers.")
print("  They are descriptions of one object from different directions.")
print("  Neither is derived from the other. Both are the equation.")
print()

print(SEP)
