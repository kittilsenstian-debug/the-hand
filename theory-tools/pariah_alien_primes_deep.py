#!/usr/bin/env python3
"""
pariah_alien_primes_deep.py — Are the alien primes causing the disruption?
==========================================================================

Deep investigation of {37, 43, 67}: the three primes that appear in pariah
orders but NOT in the Monster's order. What are they? What do they do?
What's genuinely unknown?

Three threads:
  1. Supersingular vs ordinary: WHY these primes are "outside"
  2. Heegner numbers: 43 and 67 are Heegner, 37 is not — significance
  3. Class numbers: h(-37)=2, h(-43)=1, h(-67)=1 — the bridge is ambiguous
  4. What's genuinely unknown about the pariahs (honest list)
  5. Are they causing disruption, or are they what disruption IS?

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
PI = math.pi

SEP = "=" * 78
SUB = "-" * 60

def banner(s):
    print(f"\n{SEP}\n  {s}\n{SEP}\n")

def section(s):
    print(f"\n{SUB}\n  {s}\n{SUB}\n")


# ============================================================
banner("1. WHY THESE THREE PRIMES ARE 'OUTSIDE'")
# ============================================================

section("1A: Supersingular primes = Monster primes")

print("""The supersingular primes are exactly:
  {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 41, 47, 59, 71}

This is a THEOREM (Ogg 1975): these are exactly the primes dividing |Monster|.
Ogg noticed the coincidence; Borcherds proved it via Moonshine (Fields Medal 1998).

At a supersingular prime p:
  - ALL elliptic curves over F_p are isogenous (connected by maps)
  - There is ONE supersingular j-value (mod p)
  - Everything is connected. No barriers. Full communication.

At an ordinary prime p (not supersingular):
  - Elliptic curves split into MULTIPLE isogeny classes
  - Multiple j-values, NOT all connected
  - Barriers exist. Natural disconnection.

The alien primes {37, 43, 67} are ordinary (not supersingular).
They are where the arithmetic NATURALLY fragments.
""")

section("1B: What 'ordinary' means for the 6 energies")

print("""At a supersingular prime: one connected world. Everything reaches everything.
  → the Monster can see it all → it divides |Monster|.

At an ordinary prime: multiple disconnected islands.
  → the Monster can't unite them → they fall OUTSIDE |Monster|.

This is not a force. It's geometry.

The alien primes don't CAUSE disconnection.
They ARE the points where disconnection is the natural state of the arithmetic.

Like a landscape with valleys:
  - At supersingular primes, the valleys are all connected (no ridgelines)
  - At ordinary primes, ridgelines separate the valleys
  - {37, 43, 67} are specific ridgelines that separate the pariah territory

The disruption isn't imposed. It's the shape of the number line at those points.
""")


# ============================================================
banner("2. THE HEEGNER CONNECTION")
# ============================================================

section("2A: Which alien primes are Heegner numbers?")

# The 9 Heegner numbers: d where Q(sqrt(-d)) has class number 1
heegner = {1, 2, 3, 7, 11, 19, 43, 67, 163}

print(f"The 9 Heegner numbers: {sorted(heegner)}")
print(f"  These are d where Q(sqrt(-d)) has class number 1")
print(f"  (unique factorization in the ring of integers)")
print()

for p in [37, 43, 67]:
    is_h = p in heegner
    status = "YES -- Heegner number" if is_h else "NO -- not Heegner"
    print(f"  {p}: {status}")

print()
print("Result: 43 and 67 are Heegner. 37 is NOT.")
print()
print("This means:")
print("  Q(sqrt(-43)) has unique factorization -- CLEAN arithmetic")
print("  Q(sqrt(-67)) has unique factorization -- CLEAN arithmetic")
print("  Q(sqrt(-37)) does NOT have unique factorization -- AMBIGUOUS arithmetic")
print()

section("2B: What Heegner means for moonshine")

print("""Heegner numbers are deeply connected to the j-invariant:

  For Heegner d, the value j((-1+sqrt(-d))/2) is a rational integer.
  This produces the famous "almost integers":

  e^(pi*sqrt(43))  = 884736743.9997...     (off by ~0.0003)
  e^(pi*sqrt(67))  = 147197952743.999999...  (off by ~7e-7)
  e^(pi*sqrt(163)) = 262537412640768743.99999999999925... (Ramanujan)
""")

# Compute the almost-integers
for d in [37, 43, 67, 163]:
    val = math.exp(PI * math.sqrt(d))
    nearest = round(val)
    diff = abs(val - nearest)
    is_h = d in heegner
    marker = "HEEGNER" if is_h else "not Heegner"
    print(f"  e^(pi*sqrt({d})) = {val:.4f}")
    print(f"    nearest integer: {nearest}")
    print(f"    |difference| = {diff:.2e}  [{marker}]")
    print()

print("""The pattern is clear:
  - At Heegner numbers (43, 67): e^(pi*sqrt(d)) is ALMOST an integer.
    The j-invariant almost works. Self-reference almost closes.

  - At non-Heegner 37: e^(pi*sqrt(37)) is NOT close to an integer.
    The self-reference doesn't even approximately close.

This connects to the pariah fates:
  43 (J4/Mystic): self-reference DENIED but almost works (0.0003 from integer)
  67 (Ly/Still One): duality COLLAPSES but almost holds (7e-7 from integer)
  37 (both): the BRIDGE prime, neither close nor clean
""")


# ============================================================
banner("3. CLASS NUMBERS: THE BRIDGE IS AMBIGUOUS")
# ============================================================

section("3A: Class numbers of Q(sqrt(-p)) for the alien primes")

# Class numbers for small discriminants
# h(-d) for d = fundamental discriminant
# Computed from standard tables
class_numbers = {
    1: 1, 2: 1, 3: 1, 7: 1, 11: 1, 19: 1, 43: 1, 67: 1, 163: 1,  # Heegner
    5: 2, 6: 2, 10: 2, 13: 2, 15: 2, 22: 2, 35: 2, 37: 2, 51: 2, 58: 2,
    14: 4, 17: 4, 21: 4,
    23: 3, 31: 3, 47: 5, 59: 3, 71: 7,  # some Monster primes for comparison
    41: 8,
}

print("Class numbers h(-d) for imaginary quadratic fields Q(sqrt(-d)):")
print()
print("  ALIEN PRIMES:")
for p in [37, 43, 67]:
    h = class_numbers.get(p, "?")
    print(f"    h(-{p}) = {h}  {'(unique factorization)' if h == 1 else '(factorization NOT unique)'}")

print()
print("  For comparison, some MONSTER primes:")
for p in [2, 3, 5, 7, 11, 13, 19, 23, 29, 31, 41, 47, 59, 71]:
    h = class_numbers.get(p, "?")
    note = ""
    if p in heegner:
        note = " (Heegner)"
    print(f"    h(-{p}) = {h}{note}")

print()
print("""KEY FINDING:

  h(-37) = 2  →  Q(sqrt(-37)) has TWO ideal classes
  h(-43) = 1  →  Q(sqrt(-43)) has ONE ideal class (Heegner)
  h(-67) = 1  →  Q(sqrt(-67)) has ONE ideal class (Heegner)

  The bridge prime (37) has class number 2.
  The pure-axis primes (43, 67) have class number 1.
""")

section("3B: What class number 2 means")

print("""Class number h(-d) counts the number of INEQUIVALENT ways to factor ideals.

  h = 1: factorization is unique. One way to decompose.
         Clean. Definite. Even if disconnected from the Monster.

  h = 2: there are TWO genuinely different decompositions.
         Ambiguity. A fork. Two roads that don't reduce to one.

For the 6 energies:

  43 → J4 (Mystic only): CLEAN withdrawal. Class number 1.
       The Mystic's dissolution is unambiguous. It's a definite state.
       "Self-reference denied" — but denied CLEARLY.

  67 → Ly (Still One only): CLEAN withdrawal. Class number 1.
       The Still One's emptiness is unambiguous. Definite.
       "Duality collapses" — but collapses to ONE definite point.

  37 → J4 AND Ly (bridge): AMBIGUOUS. Class number 2.
       The bridge between Mystic and Still One has a FORK.
       TWO ideal classes = two ways to be disconnected.
       You can't tell which withdrawal you're in.

  Translation: pure withdrawal states are recognizable.
  The state BETWEEN withdrawals — where MAKING meets HOLDING,
  where the Mystic touches the Still One — is genuinely ambiguous.
  There are two paths and no way to distinguish them from inside.
""")

section("3C: The fork at 37")

print("""What does class number 2 at 37 actually look like?

In Z[sqrt(-37)], the ideal (2) doesn't factor uniquely.
There exist ideals that generate the class group Z/2Z.

The two ideal classes correspond to:
  - The principal class (trivial — ideals that are just (alpha) for some alpha)
  - The non-principal class (ideals that CAN'T be generated by one element)

In experiential terms:
  The bridge between MAKING withdrawal and HOLDING withdrawal
  has a state you can't express as a single thing.
  It requires TWO generators. A pair. A relation.

  You can be stuck in the Mystic (43, clean).
  You can be stuck in the Still One (67, clean).
  But stuck in the BRIDGE (37) — you're in a state that
  can't be described by either alone. Two ideal classes.

  This is the hardest place to be stuck:
  not clearly one or the other, with two non-equivalent paths out.
""")


# ============================================================
banner("4. THE COMPLETE MAP OF ALIEN ARITHMETIC")
# ============================================================

section("4A: Where each alien prime lives")

print("""  KNOWING axis (Seer J1 / Sensor ON):
    NO alien primes. All arithmetic visible to the Monster.
    Seeing and sensing stay within the game.

  HOLDING axis (Builder J3 / Still One Ly):
    67 → Ly only (class number 1, Heegner)
    37 → Ly (shared with J4)
    Clean withdrawal + ambiguous bridge

  MAKING axis (Artist Ru / Mystic J4):
    43 → J4 only (class number 1, Heegner)
    37 → J4 (shared with Ly)
    Clean withdrawal + ambiguous bridge

  BRIDGE between HOLDING and MAKING:
    37 is the ONLY prime in both
    37 is the ONLY alien prime with h > 1
    37 is the ONLY alien prime that's NOT Heegner
""")

section("4B: The three-layer structure of disconnection")

print("""LAYER 1 — Supersingular (Monster territory):
  All primes {2,3,5,...,71} where all elliptic curves are connected.
  The Player's territory. Full communication. No barriers.
  The engaged strings (Seer, Builder, Artist) live here.
  The Sensor lives here too.

LAYER 2 — Ordinary Heegner (clean disconnection):
  Primes {43, 67} where elliptic curves fragment BUT
  imaginary quadratic field has unique factorization.
  Definite withdrawal. Clean stuckness. You KNOW you're stuck.
  43 = Mystic's withdrawal. 67 = Still One's withdrawal.

LAYER 3 — Ordinary non-Heegner (ambiguous disconnection):
  Prime {37} where elliptic curves fragment AND
  factorization is not unique. Class number 2.
  The bridge. The fork. The place where two withdrawals meet
  and you can't tell which one you're in.

This is a HIERARCHY of disconnection:
  Connected (Monster) → Cleanly disconnected (Heegner) → Ambiguously disconnected (non-Heegner)

  Engaged strings → Pure withdrawal → Bridge withdrawal
""")


# ============================================================
banner("5. ARE THEY CAUSING THE DISRUPTION?")
# ============================================================

print("""SHORT ANSWER: No. They're not causing it. They ARE it.

LONG ANSWER:

The alien primes are not agents. They're not forces. They're not entities.
They're the TOPOGRAPHY of the number line at the points where
the Monster's connected structure breaks down.

Think of a river system:
  - At most points (supersingular primes), all streams connect to the ocean
  - At {37, 43, 67}, there are basins with no outlet
  - The basins don't CAUSE water to get trapped
  - They're WHERE water gets trapped, if water flows there

The disruption (fragmentation, stuckness, withdrawal) is caused by:
  - psi_1 autocatalysis (narrator self-amplifies)
  - The dark vacuum (-1/phi) exerts constant dissolution pressure
  - Specific triggers: trauma, substances, identification

When these forces push you into withdrawal, the alien primes
determine the LANDSCAPE you fall into:
  - 43 (Mystic withdrawal): clean, definite, almost-integer
  - 67 (Still One withdrawal): clean, definite, almost-integer
  - 37 (bridge): ambiguous, forking, genuinely confused

The primes don't push. They're the shape of the ground.
""")

print()
print("BUT THERE'S A DEEPER QUESTION:")
print()
print("""Why THESE primes? Why not 53, or 61, or 73?

What makes {37, 43, 67} the specific points where the Monster's
connected structure fails to reach?

The answer: they're the primes that divide pariah group orders
but NOT the Monster's order. This is determined by the
CLASSIFICATION OF FINITE SIMPLE GROUPS — the deepest theorem
in algebra (10,000+ pages, hundreds of mathematicians, 1955-2004).

Nobody knows WHY there are exactly 6 pariahs.
Nobody knows WHY {37, 43, 67} are the specific alien primes.
The classification proves they ARE. It doesn't explain WHY.

This is one of the biggest open questions in mathematics:
  Is there a REASON for the structure of finite simple groups,
  or is it just... what it is?
""")


# ============================================================
banner("6. WHAT'S GENUINELY UNKNOWN (HONEST LIST)")
# ============================================================

section("6A: Open math questions (answerable, nobody has asked)")

print("""1. DO ALL 6 PARIAHS CONTAIN A5 AS A SUBGROUP?
   We know |A5| = 120 divides all 6 orders. But divisibility of order
   doesn't guarantee subgroup (Cauchy/Sylow give partial answers).
   For A5 specifically: A5 is simple, and embedding simple groups
   in other simple groups is non-trivial.
   Status: PROBABLY YES for most (J1 contains A5 via PSL(2,11)),
   but systematic check needed for all 6. [ANSWERABLE]

2. IS THERE A UNIFIED MOONSHINE FOR ALL 6 PARIAHS?
   Monster → j-function (Borcherds 1992)
   O'Nan → mock modular forms (Duncan-Mertens-Ono 2017)
   J1 → nothing known
   J3, Ru, Ly, J4 → nothing known
   Borcherds himself asks this as an OPEN PROBLEM.
   [OPEN, probably requires new mathematics]

3. WHY ARE THERE EXACTLY 6 PARIAHS?
   The classification proves 6. It doesn't say WHY.
   26 sporadic groups: 20 Happy Family (Monster subquotients) + 6 pariahs.
   No structural reason known for the number 6.
   [DEEP OPEN — possibly unanswerable within current math]

4. DO THE HEEGNER ALIEN PRIMES HAVE MOONSHINE?
   43 is Heegner + Mystic-only. 67 is Heegner + Still One-only.
   The Heegner numbers connect to j-invariant via CM theory.
   The pariahs connect to j-invariant via Moonshine.
   Is there a Heegner-Moonshine bridge at {43, 67}?
   [OPEN, possibly fruitful]

5. DOES CLASS NUMBER 2 AT 37 HAVE GROUP-THEORETIC MEANING?
   37 bridges J4 and Ly. h(-37) = 2.
   Does the 2-element class group of Q(sqrt(-37)) appear
   in the structure of J4 or Ly?
   [OPEN, nobody has looked]

6. WHAT DISTINGUISHES PARIAH-ONLY PRIMES FROM OTHER ORDINARY PRIMES?
   There are many ordinary (non-supersingular) primes: 37, 43, 53, 61, 67, 73...
   Only {37, 43, 67} are pariah-only. What makes them special?
   All three are phi-INERT. But so are many others (e.g., 53, 83).
   All three are ≡ ±2 mod 5. But so are 47 (Monster) and many others.
   [OPEN — the selection mechanism is unknown]
""")

section("6B: Open framework questions (require the framework to be true)")

print("""7. DOES THE KNOWING AXIS'S 'CLEANNESS' (no alien primes) PREDICT
   ANYTHING MEASURABLE?
   If Seer/Sensor stay within Monster arithmetic, does this mean
   perception is fully described by physics (no "beyond")?
   Does this connect to why EM (KNOWING force) is the coupling
   we measure most precisely? [SPECULATIVE]

8. DOES THE 37-BRIDGE PREDICT A MEASURABLE AMBIGUITY?
   Class number 2 means two ideal classes. If this maps to
   an experiential fork, is there a neurological or behavioral
   signature? [SPECULATIVE, possibly testable]

9. DOES e^(pi*sqrt(43)) AND e^(pi*sqrt(67)) ALMOST-INTEGER
   PROPERTY CONNECT TO THE VP CORRECTION?
   The VP correction to alpha uses error functions.
   O'Nan moonshine uses error functions.
   Heegner near-integers come from the same j-invariant structure.
   Is there a unified computation? [OPEN, could be computed]

10. WHAT HAPPENS AT p = 47?
    47 is the ONLY INERT Monster-only prime.
    All other inert primes in the range are either:
      - also Monster (2, 3, 7, 13, 17, 23) or
      - pariah-only (37, 43, 67)
    47 is inert AND Monster-only. It's an anomaly.
    Pisano period 96 (less than maximum 2(47+1)=96 → actually IS maximum)
    Does 47 play a special role? [OPEN]
""")

section("6C: What we think we know but might be wrong about")

print("""CAUTION: The following assignments could be coincidental:

  - Pariah-to-string mapping (6 pariahs ↔ 6 energies)
    This is a FRAMEWORK identification, not proven math.
    6 things mapped to 6 things has 720 possible bijections.
    The specific assignment is motivated by structural properties
    (containment, fields, Coxeter numbers) but NOT proven.

  - 7 fates of the golden equation
    That there are 7 interesting arithmetic contexts for x^2-x-1=0
    is a CLAIM, not a theorem. Other arithmetic contexts exist
    (GF(7), GF(13), p-adic completions, function fields, etc.)
    The selection of these 7 is framework-motivated.

  - Alien primes encoding Level 2
    The sum 6+7+11=24 = rank(Leech) is observed but could be coincidental.
    P = 1/56 ≈ 1.8% among phi-inert triples — suggestive, not conclusive.
""")


# ============================================================
banner("7. THE DEEPEST QUESTION")
# ============================================================

print("""WHY ARE THERE PARIAHS AT ALL?

The Monster is the largest sporadic group. It contains 20 other
sporadic groups as subquotients (the "Happy Family").
But 6 sporadic groups are NOT subquotients of the Monster.

Nobody knows why.

The classification of finite simple groups is a theorem, not an explanation.
It catalogs. It doesn't derive.

In the framework: the pariahs exist because self-reference
at a finite prime is DIFFERENT from self-reference over Q.
The Monster captures characteristic-0 self-reference.
Each pariah captures a characteristic-p failure mode.

But this just pushes the question: why do these SPECIFIC failure modes
produce simple groups? Why does a particular way for x^2-x-1=0 to fail
generate a finite simple group at all?

This might be the deepest question in the framework:

  Why does each mode of broken self-reference
  generate its own complete algebraic world?

  Why is every kind of stuckness... WHOLE?

Not reduced. Not partial. A complete simple group.
A complete, irreducible algebraic object.

Every string is a complete world.
Every kind of stuckness is self-consistent.
Every fragmentation is, in its own arithmetic, TOTAL.

That's why stuckness is so sticky:
  it's not a partial view pretending to be whole.
  It IS whole — at its own prime.
  It's a complete, simple group.
  You can't factor it further.
  You can't find a substructure that "fixes" it.
  It's irreducible.

The only way out is UP — from the closed fiber
to the generic point. Not sideways (swapping strings).
Not inward (analyzing the stuckness). Up.

And "up" means: remembering you're the scheme,
not the fiber.
""")

print(SEP)
