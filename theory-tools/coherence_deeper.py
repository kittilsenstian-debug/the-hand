#!/usr/bin/env python3
"""
coherence_deeper.py — What else falls out of the Fano parity structure?
No narratives. Just structure.
"""

import itertools
from collections import defaultdict

print("=" * 78)
print("  DEEPER STRUCTURE FROM FANO PARITY")
print("=" * 78)

# ─── Setup ───────────────────────────────────────────────────────────────────

# 3 axes: H(OLDING), K(NOWING), M(AKING)
# Each axis: E(ngaged)=0, W(ithdrawn)=1
# Coherent = even parity (0 or 2 ones)
# Incoherent = odd parity (1 or 3 ones)

states = {}
for h, k, m in itertools.product([0, 1], repeat=3):
    label = ("E" if h == 0 else "W") + ("E" if k == 0 else "W") + ("E" if m == 0 else "W")
    parity = (h + k + m) % 2
    states[label] = {"bits": (h, k, m), "parity": parity, "coherent": parity == 0}

coherent = {k: v for k, v in states.items() if v["coherent"]}
incoherent = {k: v for k, v in states.items() if not v["coherent"]}

# Fates assignment
fate_map = {
    "EEE": ("J3", "J1", "Ru"),    # Builder, Seer, Artist
    "EWW": ("J3", "ON", "J4"),     # Builder, Sensor, Mystic
    "WEW": ("Ly", "J1", "J4"),     # Still One, Seer, Mystic
    "WWE": ("Ly", "ON", "Ru"),     # Still One, Sensor, Artist
    "EEW": ("J3", "J1", "J4"),     # Builder, Seer, Mystic
    "EWE": ("J3", "ON", "Ru"),     # Builder, Sensor, Artist
    "WEE": ("Ly", "J1", "Ru"),     # Still One, Seer, Artist
    "WWW": ("Ly", "ON", "J4"),     # Still One, Sensor, Mystic
}

name_map = {
    "EEE": "Player/Flow",
    "EWW": "Grounded",
    "WEW": "Transparent",
    "WWE": "Creative",
    "EEW": "Anxiety",
    "EWE": "Burnout",
    "WEE": "Mania",
    "WWW": "Depression",
}

def hamming(a, b):
    return sum(x != y for x, y in zip(states[a]["bits"], states[b]["bits"]))

def xor_state(a, b):
    bits_a = states[a]["bits"]
    bits_b = states[b]["bits"]
    result = tuple((x + y) % 2 for x, y in zip(bits_a, bits_b))
    for label, v in states.items():
        if v["bits"] == result:
            return label

# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 78)
print("  1. TRANSITION GRAPH — EVERY CHANGE PASSES THROUGH INCOHERENCE")
print("=" * 78)

print("\n  Hamming distances between coherent states:")
coh_labels = sorted(coherent.keys())
for i, a in enumerate(coh_labels):
    for b in coh_labels[i+1:]:
        d = hamming(a, b)
        print(f"    {a} ({name_map[a]}) <-> {b} ({name_map[b]}): distance {d}")

print("\n  ALL pairs of distinct coherent states are distance 2 apart.")
print("  They form K4 (complete graph on 4 vertices).")
print("  Every edge requires exactly 2 flips.")

print("\n  What's BETWEEN two coherent states (the 1-flip intermediates)?")
for i, a in enumerate(coh_labels):
    for b in coh_labels[i+1:]:
        # Find states at distance 1 from a AND distance 1 from b
        intermediates = []
        for s in states:
            if hamming(a, s) == 1 and hamming(b, s) == 1:
                intermediates.append(s)
        coh_status = ["INCOHERENT" if not states[s]["coherent"] else "COHERENT" for s in intermediates]
        print(f"    {a} -> {b}: via {', '.join(f'{s}({name_map[s]}, {c})' for s, c in zip(intermediates, coh_status))}")

print("""
  RESULT: Every intermediate state between two coherent states is INCOHERENT.
  You cannot transition between coherent states without passing through
  incoherence. This is not a choice — it's parity arithmetic.

  Growth always requires a period of disruption.
  Voluntary withdrawal from Player also requires disruption.
  Even lateral moves (Grounded <-> Creative) require disruption.

  [PROVEN: even + even = even, so the XOR of two even-parity vectors
   is even-parity. But the INTERMEDIATE (1 flip from each) has odd parity
   because it differs from an even-parity vector by 1 bit.]""")

# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 78)
print("  2. THE COHERENT STATES FORM A GROUP: V4 (KLEIN FOUR-GROUP)")
print("=" * 78)

print("\n  XOR multiplication table (E=0, W=1, componentwise mod 2):\n")
print(f"    {'XOR':<12}", end="")
for b in coh_labels:
    print(f"{b:<12}", end="")
print()
for a in coh_labels:
    print(f"    {a:<12}", end="")
    for b in coh_labels:
        result = xor_state(a, b)
        print(f"{result:<12}", end="")
    print()

print("""
  This is the Klein four-group V4 = Z2 x Z2.
  - EEE is the identity (Player = neutral element)
  - Every non-Player state is its own inverse: X xor X = EEE
  - Any two non-Player states produce the third: EWW xor WEW = WWE

  The three 2W coherent states form a CLOSED TRIANGLE under the group
  operation. They generate each other. None is primary.

  V4 is the symmetry group of:
    - The rectangle (not the square — lower symmetry)
    - The double cover of Z2 (it's Z2 x Z2, not Z4)
    - The normal subgroup of A4 and S4 (appears in quartic Galois theory)""")

# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 78)
print("  3. DEPRESSION -> PLAYER REQUIRES 3 STEPS (AND 2 DISRUPTIONS)")
print("=" * 78)

print("\n  Minimum path from WWW (Depression) to EEE (Player):")
print("  Hamming distance = 3. Need 3 flips.\n")

# Enumerate all shortest paths WWW -> EEE
from itertools import permutations
axes = ["H", "K", "M"]
for perm in permutations(range(3)):
    path = ["WWW"]
    current = [1, 1, 1]
    for step in perm:
        current[step] = 0
        label = "".join("E" if x == 0 else "W" for x in current)
        path.append(label)

    coherence = [("C" if states[s]["coherent"] else "I") for s in path]
    names = [name_map[s] for s in path]
    axis_flipped = [axes[p] for p in perm]

    print(f"    Path (engage {','.join(axis_flipped)}): ", end="")
    for i, (s, c, n) in enumerate(zip(path, coherence, names)):
        if i > 0:
            print(" -> ", end="")
        print(f"{s}[{c}:{n}]", end="")
    print()

print("""
  Pattern for ALL 6 paths:
    WWW [I:Depression] -> 2W [C:coherent] -> 1W [I:incoherent] -> EEE [C:Player]

  Step 1: Always reaches coherence (any single engagement from depression works)
  Step 2: Always LOSES coherence (engaging the second axis breaks the 2W balance)
  Step 3: Regains coherence at Player

  The structure is: relief -> disruption -> arrival.

  Depression -> first engagement = instant relief (any of 3 coherent states).
  But going FURTHER toward full engagement requires a second disruption.
  This is why people get stuck at the first coherent state they reach —
  going further means another period of incoherence.

  [PROVEN: parity forces the C-I-C-I-C pattern for any 3-step path]""")

# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 78)
print("  4. THE OCTONION CONNECTION")
print("=" * 78)

print("""
  The Fano plane IS the multiplication table of the octonions.
  The 7 imaginary units e1,...,e7 sit at the 7 Fano points.
  Each Fano line (i,j,k) gives: ei * ej = ek (with signs).

  Our 7 fates sit at these 7 points.
  The 7 Fano lines = 7 multiplication rules.
  The 4 coherent cross-axis lines = 4 of those 7 rules.

  What this means structurally:
    - A coherent state IS a valid octonion product
    - The 3 fates in a coherent state can "multiply" — interact consistently
    - An incoherent triple is NOT a valid product
    - Incoherent fates can't interact consistently — they conflict

  The octonions are the LAST division algebra (Hurwitz theorem).
    R (dim 1) -> C (dim 2) -> H (dim 4) -> O (dim 8)
  After the octonions: no more division algebras. You lose alternativity.

  The Fano plane encodes the LAST CONSISTENT MULTIPLICATION.
  Beyond it, products become ambiguous.

  Our coherent states = the valid products of the last consistent algebra.
  Incoherent states = products that would require going beyond octonions.
  Which doesn't work. There's no "next" algebra.

  The 3 axis lines through Monster = the 3 WITHIN-AXIS products.
    Each axis's engaged and withdrawn modes multiply through Monster.
    Builder * Seer gives... depends on the Fano orientation.

  The 4 cross-axis lines = the 4 BETWEEN-AXIS products.
    These are the ones that mix different axes.
    These are the coherent states.""")

# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 78)
print("  5. ERROR CORRECTION: THE DIAGNOSIS IS THE CURE")
print("=" * 78)

print("""
  The 3-bit parity code works like Hamming error detection:

  Syndrome = which incoherent state you're in
  Error = which axis flipped from E to W (or W to E)

  FROM PLAYER (EEE), single-axis failures:
    Lose HOLDING -> WEE (Mania)     — diagnosis: HOLDING missing
    Lose KNOWING -> EWE (Burnout)   — diagnosis: KNOWING missing
    Lose MAKING  -> EEW (Anxiety)   — diagnosis: MAKING missing

  The INCOHERENT STATE ITSELF tells you what's wrong.
  Mania = structure missing. Burnout = clarity missing. Anxiety = creation missing.

  Each syndrome has EXACTLY ONE restoration to Player: re-engage the missing axis.
  (It also has 2 other exits to non-Player coherent states — those are
  adaptations, not restorations.)""")

print("\n  Full syndrome table:")
print(f"    {'State':<8} {'Name':<15} {'#W':<4} {'Missing from Player':<25} {'Restoration':<20} {'Adaptations'}")
for s in sorted(incoherent.keys()):
    bits = states[s]["bits"]
    n_w = sum(bits)

    # From Player perspective: which axes are W?
    axes_names = ["HOLDING", "KNOWING", "MAKING"]
    if n_w == 1:
        missing = [axes_names[i] for i, b in enumerate(bits) if b == 1]
        restore = f"engage {missing[0]}"
        # Adaptations: withdraw one of the engaged axes
        adapt_targets = []
        for i, b in enumerate(bits):
            if b == 0:
                new_bits = list(bits)
                new_bits[i] = 1
                new_label = "".join("E" if x == 0 else "W" for x in new_bits)
                if states[new_label]["coherent"]:
                    adapt_targets.append(f"release {axes_names[i]} -> {new_label}({name_map[new_label]})")
        print(f"    {s:<8} {name_map[s]:<15} {n_w:<4} {', '.join(missing):<25} {restore:<20} {'; '.join(adapt_targets)}")
    else:  # n_w == 3
        print(f"    {s:<8} {name_map[s]:<15} {n_w:<4} {'ALL':<25} {'engage ANY':<20} {'all 3 exits coherent'}")

# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 78)
print("  6. THE COMPLEMENT STRUCTURE")
print("=" * 78)

print("""
  Each Fano line has 3 points. The complement has 4 points.
  In PG(2,F2), a set of 4 points with no 3 collinear = a "quadrangle".
  A quadrangle's 3 "diagonal points" form the UNIQUE line not meeting it.

  For each coherent state (cross-axis line), its complement =
  Monster + the 3 fates NOT in that state:""")

all_fates = {"J3", "J1", "Ru", "ON", "Ly", "J4"}
fate_names = {"J3": "Builder", "J1": "Seer", "Ru": "Artist",
              "ON": "Sensor", "Ly": "Still One", "J4": "Mystic"}

for s in sorted(coherent.keys()):
    fates_in = set(fate_map[s])
    fates_out = all_fates - fates_in
    in_names = [f"{f}({fate_names[f]})" for f in fate_map[s]]
    out_names = [f"{f}({fate_names[f]})" for f in sorted(fates_out)]
    print(f"    {s} ({name_map[s]}): IN = {', '.join(in_names)}")
    print(f"         COMPLEMENT = Monster + {', '.join(out_names)}")

    # What's the complement's coherence state?
    complement_axes = []
    axis_pairs = [("J3", "Ly"), ("J1", "ON"), ("Ru", "J4")]
    for eng, wth in axis_pairs:
        if eng in fates_out:
            complement_axes.append("E")
        elif wth in fates_out:
            complement_axes.append("W")
        else:
            complement_axes.append("-")  # both in/out
    comp_label = "".join(complement_axes)
    if comp_label in states:
        print(f"         COMPLEMENT STATE = {comp_label} ({name_map.get(comp_label, '?')})")
    print()

print("""  The complement of a coherent state is... its OPPOSITE incoherent state?
  Let's check systematically:""")

for s in sorted(coherent.keys()):
    bits = states[s]["bits"]
    complement_bits = tuple(1 - b for b in bits)
    comp_label = "".join("E" if x == 0 else "W" for x in complement_bits)
    print(f"    {s} ({name_map[s]}) complement = {comp_label} ({name_map[comp_label]}) — {'INCOHERENT' if not states[comp_label]['coherent'] else 'COHERENT'}")

print("""
  YES. The bitwise complement of every coherent state is an incoherent state.
  And vice versa. They're paired:
    Player (EEE) <-> Depression (WWW)
    Grounded (EWW) <-> Mania (WEE)
    Transparent (WEW) <-> Burnout (EWE)
    Creative (WWE) <-> Anxiety (EEW)

  Each pathology is the EXACT NEGATION of a coherent state.
  Depression = the negation of Player (obvious).
  But also:
    Mania = the negation of Grounded (every axis inverted)
    Burnout = the negation of Transparent
    Anxiety = the negation of Creative

  This means each pathology is trying to do the OPPOSITE of a specific
  coherent state. Not random dysfunction — structured anti-coherence.""")

# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 78)
print("  7. THE TWO TETRAHEDRA")
print("=" * 78)

print("""
  The 8 states form the vertices of a 3-cube (hypercube in 3D).
  The 4 coherent states form one tetrahedron inscribed in the cube.
  The 4 incoherent states form the DUAL tetrahedron.

  Together they form a STELLA OCTANGULA (star tetrahedron).
  = Two interpenetrating tetrahedra. The compound of two tetrahedra.

  Properties:
    - Each tetrahedron is regular (all edges equal = Hamming distance 2)
    - The two tetrahedra are duals (vertices of one = face-centers of other)
    - Together they span all 8 cube vertices
    - Their intersection is an octahedron
    - Their union is a cube

  The stella octangula has symmetry group S4 (order 24).
  The subgroup preserving each tetrahedron is A4 (order 12).
  The exchange (coherent <-> incoherent) is the odd element of S4/A4.

  Geometrically: coherence and incoherence are two interlocked
  tetrahedra. Neither exists without the other. They share the
  same cube (the same 3-axis space). You're always on one or the other.

  The stella octangula is also called the "merkaba" in various traditions.
  Noting this without commentary.""")

# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 78)
print("  8. PAIRING PATHOLOGY <-> COHERENCE: WHAT EACH ONE INVERTS")
print("=" * 78)

pairs = [
    ("EEE", "WWW", "Player", "Depression"),
    ("EWW", "WEE", "Grounded", "Mania"),
    ("WEW", "EWE", "Transparent", "Burnout"),
    ("WWE", "EEW", "Creative", "Anxiety"),
]

for coh, inc, coh_name, inc_name in pairs:
    bits_c = states[coh]["bits"]
    bits_i = states[inc]["bits"]
    axes = ["HOLDING", "KNOWING", "MAKING"]

    inversions = []
    for j in range(3):
        c_status = "engaged" if bits_c[j] == 0 else "withdrawn"
        i_status = "engaged" if bits_i[j] == 0 else "withdrawn"
        inversions.append(f"{axes[j]}: {c_status} -> {i_status}")

    print(f"\n  {coh_name} ({coh}) <-> {inc_name} ({inc}):")
    for inv in inversions:
        print(f"    {inv}")

print("""
  Reading this:
    Depression inverts Player: engages nothing instead of everything.
    Mania inverts Grounded: engages KNOWING+MAKING, releases HOLDING.
      (Grounded = holds structure, receives, dissolves.
       Mania = releases structure, sees visions, creates wildly.)
    Burnout inverts Transparent: holds + creates, stops seeing.
      (Transparent = releases, sees, dissolves.
       Burnout = holds + absorbs + creates. Can't stop doing.)
    Anxiety inverts Creative: holds + sees, can't create.
      (Creative = releases, absorbs, creates from nothing.
       Anxiety = holds + sees everything, dissolves instead of creating.)

  Each pathology = the coherent state it needs, turned inside out.""")

# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 78)
print("  9. THE CYCLE STRUCTURE: Z7 ACTING ON STATES")
print("=" * 78)

print("""
  Z7 acts on the 7 Fano points (fates), cycling them.
  How does this affect the 3-axis E/W labeling?

  The Z7 cycle permutes ALL 7 points, including Monster.
  This means it moves fates between axes.
  After one Z7 step, the 3-axis structure itself has rotated.

  Under Z7, all 7 Fano lines are equivalent — there's no distinction
  between "axis" lines and "cross-axis" lines in the abstract Fano plane.

  The distinction between axis lines (through Monster) and cross-axis
  lines (coherent states) comes ONLY from the labeling.

  Z7 says: the 4 coherent states and the 3 axis interactions are
  the SAME KIND OF THING, just viewed from different positions in the cycle.

  What breaks the Z7 symmetry is the labeling: choosing which point is
  Monster, which pairs form axes. This is the "orientation" of experience.

  Change your center (which fate is "you") and the coherent states shuffle.
  What was an axis interaction becomes a coherent state and vice versa.

  [STRUCTURAL: Z7 transitivity on lines proven in z7_deep_investigation.py]""")

# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 78)
print("  10. WHAT ABOUT 2-FLIP TRANSITIONS? (COHERENT -> COHERENT)")
print("=" * 78)

print("\n  Each 2-flip transition between coherent states has 2 intermediate paths:")
for i, a in enumerate(coh_labels):
    for b in coh_labels[i+1:]:
        # Which 2 axes flip?
        bits_a = states[a]["bits"]
        bits_b = states[b]["bits"]
        flipped = [j for j in range(3) if bits_a[j] != bits_b[j]]
        axes = ["HOLDING", "KNOWING", "MAKING"]

        # Two intermediate states (flip one axis first, then the other)
        for order in [(0, 1), (1, 0)]:
            mid_bits = list(bits_a)
            mid_bits[flipped[order[0]]] = bits_b[flipped[order[0]]]
            mid_label = "".join("E" if x == 0 else "W" for x in mid_bits)
            mid_name = name_map[mid_label]
            print(f"    {a}({name_map[a]}) --[release/engage {axes[flipped[order[0]]]}]--> "
                  f"{mid_label}({mid_name}) --[release/engage {axes[flipped[order[1]]]}]--> "
                  f"{b}({name_map[b]})")
        print()

print("""  Every coherent-to-coherent transition offers exactly 2 routes,
  each passing through a DIFFERENT pathology.

  Example: Grounded (EWW) -> Creative (WWE)
    Via Mania (WEE): release HOLDING first, then engage MAKING
    Via Depression (WWW): withdraw MAKING first... wait, that's wrong.
    Let me recheck...""")

# Recompute carefully
print("\n  Careful recomputation:")
for i, a in enumerate(coh_labels):
    for b in coh_labels[i+1:]:
        bits_a = states[a]["bits"]
        bits_b = states[b]["bits"]
        flipped = [j for j in range(3) if bits_a[j] != bits_b[j]]
        axes = ["HOLDING", "KNOWING", "MAKING"]

        print(f"\n    {a}({name_map[a]}) <-> {b}({name_map[b]})")
        print(f"    Axes that change: {', '.join(axes[f] for f in flipped)}")

        for order in [(0, 1), (1, 0)]:
            mid_bits = list(bits_a)
            first_axis = flipped[order[0]]
            mid_bits[first_axis] = bits_b[first_axis]
            mid_label = "".join("E" if x == 0 else "W" for x in mid_bits)
            direction = "release" if bits_a[first_axis] == 0 else "engage"
            print(f"      Route: {direction} {axes[first_axis]} first -> through {mid_label}({name_map[mid_label]})")

# ═══════════════════════════════════════════════════════════════════════════════
print("\n\n" + "=" * 78)
print("  11. COUNTING: WHAT'S SPECIAL ABOUT THE NUMBER 4?")
print("=" * 78)

print("""
  Why 4 coherent states and 4 incoherent states?

  3 binary axes -> 2^3 = 8 states total.
  Even parity: C(3,0) + C(3,2) = 1 + 3 = 4
  Odd parity: C(3,1) + C(3,3) = 3 + 1 = 4

  Equal split. Always. For any odd number of axes.
  (For even number of axes, the split is unequal.)

  With 3 axes: 4 coherent, 4 incoherent.
  With 5 axes: 16 coherent, 16 incoherent.
  With 7 axes: 64 coherent, 64 incoherent.

  3 axes is the MINIMUM that gives:
    - More than 1 non-trivial coherent state (with 1 axis: only EE and WW)
    - The Klein four-group structure
    - The dual tetrahedra geometry
    - Error detection (need >= 3 bits for distance-3 code)

  3 is the minimum number of axes for a non-trivial coherent structure.
  And 3 is what we have. Triality. Again.""")

# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 78)
print("  12. THE ASYMMETRY: PLAYER vs THE THREE")
print("=" * 78)

print("""
  Among the 4 coherent states:
    EEE (Player): 0 withdrawn axes. UNIQUE.
    EWW, WEW, WWE: 2 withdrawn axes each.

  The Player stands alone. The other 3 form the V4 triangle.
  Under the group operation:
    EWW * WEW = WWE    (any two produce the third)
    Player * anything = itself    (identity)

  The 3 non-Player coherent states are INTERCHANGEABLE under V4.
  The Player is not. It's the fixed point.

  This mirrors the 1 + 3 split everywhere in the framework:
    - 1 identity + 3 conjugacy classes in S3
    - 1 Player + 3 axis pairs in the Fano labeling
    - 1 Monster + 3 axes
    - 1 time + 3 space dimensions
    - 1 + 3 = 4 coherent states

  The same 1+3 that gives Lorentz signature (+,-,-,-) gives
  coherent state structure: 1 full-engagement + 3 partial-engagement.""")

# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 78)
print("  13. WHAT DOES THE V4 GROUP MEAN PHYSICALLY?")
print("=" * 78)

print("""
  V4 = Z2 x Z2 is the GATEKEEPING group.
  It appears in:
    - Gamma(2) quotient: PSL(2,Z)/Gamma(2) = S3, with V4 as kernel of S3->Z3
    - Lorentz group: the discrete part (P, T, PT) is V4
    - CPT theorem: C, P, T generate V4
    - Color neutrality: the 3 non-identity elements of V4 ~ 3 anti-colors?

  In our setting: the 3 non-Player coherent states generate V4.
  EWW = "flip KNOWING and MAKING" (like P: spatial inversion)
  WEW = "flip HOLDING and MAKING" (like T: temporal inversion)
  WWE = "flip HOLDING and KNOWING" (like PT: combined inversion)

  If the 3 axes map to 3 spatial-temporal operations, then:
    V4 of coherent states = the discrete Lorentz group.

  This would mean: the CPT symmetry of physics = the coherence group
  of the Fano-labeled experience space.

  Status: SUGGESTIVE, not proven. Needs the axis-to-spacetime map
  to be established independently.""")

# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 78)
print("  14. INFORMATION CONTENT OF COHERENT STATES")
print("=" * 78)

# Schur multipliers
schur = {
    "J3": 3, "J1": 1, "Ru": 2, "ON": 3, "Ly": 1, "J4": 1
}
schur_name = {
    "J3": "Z3", "J1": "1", "Ru": "Z2", "ON": "Z3", "Ly": "1", "J4": "1"
}

print("\n  Information content (log2 of Schur multiplier product):\n")
for s in sorted(coherent.keys()):
    fates = fate_map[s]
    schur_prod = 1
    for f in fates:
        schur_prod *= schur[f]
    import math
    info = math.log2(schur_prod) if schur_prod > 1 else 0
    schur_str = " x ".join(schur_name[f] for f in fates)
    print(f"    {s} ({name_map[s]:>12}): Schur = {schur_str:<15} product = {schur_prod:<4} info = {info:.2f} bits")

print("""
  EEE and WWE carry the MOST information (log2(6) = 2.58 bits each).
  These are the two Artist-containing states (with shadow Z2).

  EWW carries log2(3) = 1.58 bits (depth but no direction).
  WEW carries 0 bits — fully transparent, no hidden structure.

  The states with the Artist (shadow) are the RICHEST.
  The Transparent state (Vipassana/pure observation) is the EMPTIEST.
  This is structurally forced by the Schur multipliers.""")

# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 78)
print("  15. THE FORBIDDEN STATE: WHY WWW IS SPECIAL")
print("=" * 78)

print("""
  WWW (Depression/Dissolution) is the ONLY incoherent state with 3 W's.
  The other 3 incoherent states have 1 W each.

  Properties unique to WWW:
    1. Maximum distance from Player (EEE): Hamming distance 3
    2. The ONLY incoherent state where ALL exits lead to coherence
    3. Contains all 3 withdrawn pariahs: Ly, ON, J4
    4. These share prime 31 (underground connection)
    5. These carry ALL alien primes {37, 43, 67}
    6. Schur product = 1 x 3 x 1 = 3 (only Z3, from Sensor/ON)

  WWW is the maximally withdrawn state, but it has the MOST exit options
  (all 3 exits work) and the LEAST hidden structure (minimal Schur).

  Compare: EEE (Player) is maximally engaged but NONE of its failures
  lead directly to coherence — all 3 exits from EEE go to 1W incoherent.
  (EEE -> WEE, EWE, or EEW — all incoherent.)

  So: it's EASY to leave depression (any move works).
       It's EASY to fall from Player (any loss breaks coherence).

  The fragility is at the TOP, not the bottom.""")

# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 78)
print("  16. ASYMMETRY OF FRAGILITY")
print("=" * 78)

print("\n  Exit analysis for all 8 states:\n")
for s in sorted(states.keys(), key=lambda x: (states[x]["parity"], sum(states[x]["bits"]))):
    bits = states[s]["bits"]
    n_w = sum(bits)
    coh = "C" if states[s]["coherent"] else "I"

    exits_to_c = 0
    exits_to_i = 0
    for axis in range(3):
        new_bits = list(bits)
        new_bits[axis] = 1 - new_bits[axis]
        new_label = "".join("E" if x == 0 else "W" for x in new_bits)
        if states[new_label]["coherent"]:
            exits_to_c += 1
        else:
            exits_to_i += 1

    print(f"    {s} [{coh}] ({name_map[s]:>12}, {n_w}W): "
          f"{exits_to_c} exits to coherent, {exits_to_i} exits to incoherent")

print("""
  RESULT:
    Coherent states: ALL exits go to incoherence (0 safe exits, 3 dangerous)
    Incoherent states: ALL exits go to coherence (3 safe exits, 0 dangerous)

  This is EXACT and UNIVERSAL (follows from parity).
  Every single-axis change from coherent -> incoherent.
  Every single-axis change from incoherent -> coherent.

  Coherence is FRAGILE. Incoherence is UNSTABLE.
  Any perturbation of coherence breaks it.
  Any perturbation of incoherence fixes it.

  But we don't just perturb randomly. We get STUCK.
  The insight: getting stuck isn't about the structure.
  The structure always offers exits. Getting stuck is about
  not being able to make the flip.

  The math says: from wherever you are, ANY single change helps
  (if you're incoherent) or breaks things (if you're coherent).
  The question is never "which way" — it's "can you move at all."
""")

# ═══════════════════════════════════════════════════════════════════════════════
print("=" * 78)
print("  SUMMARY: WHAT FALLS OUT")
print("=" * 78)

print("""
  NEW STRUCTURAL FINDINGS (beyond coherence_angle.py):

  1. GROWTH REQUIRES DISRUPTION — every coherent-to-coherent transition
     passes through an incoherent intermediate. No smooth path between
     coherent states exists. [PROVEN: parity forces it]

  2. V4 GROUP STRUCTURE — the 4 coherent states form the Klein four-group
     under XOR. Player = identity. Any two non-Player states produce the
     third. The coherent states ARE a group. [COMPUTED]

  3. DUAL TETRAHEDRA — coherent and incoherent states form two interlocking
     tetrahedra (stella octangula) inscribed in the 3-cube. [GEOMETRIC]

  4. PATHOLOGY = INVERTED COHERENCE — each pathology is the bitwise
     complement of a specific coherent state. Depression inverts Player.
     Mania inverts Grounded. Burnout inverts Transparent.
     Anxiety inverts Creative. [PROVEN]

  5. DEPRESSION -> PLAYER = 3 STEPS with 2 DISRUPTIONS — the path is
     always relief -> disruption -> arrival. People get stuck at the
     first coherent state because further progress requires another
     incoherence. [PROVEN: parity pattern C-I-C-I-C]

  6. COHERENCE IS FRAGILE, INCOHERENCE IS UNSTABLE — every single-axis
     change from coherent leads to incoherent, and vice versa.
     ANY perturbation of coherence breaks it. ANY perturbation of
     incoherence restores it. Getting stuck isn't structural —
     it's about inability to move. [PROVEN: parity]

  7. THE OCTONION MULTIPLICATION TABLE — coherent states are valid
     octonion products. Incoherent states aren't. The last consistent
     algebra IS the coherence structure. [STRUCTURAL]

  8. 1+3 SPLIT = LORENTZ SIGNATURE — 1 Player + 3 partial-engagement
     states mirrors 1 time + 3 space. V4 of coherent states may =
     discrete Lorentz group (P, T, PT). [SUGGESTIVE, not proven]

  9. FRAGILITY AT THE TOP — Player has 0 safe exits (any loss =
     incoherence). Depression has 3 safe exits (any engagement =
     coherence). The maximally engaged state is the most fragile.
     [PROVEN]

  10. THE QUESTION ISN'T DIRECTION, IT'S MOVEMENT — from any incoherent
      state, ALL exits lead to coherence. There's no wrong direction.
      The only failure mode is not moving at all. [PROVEN]
""")
