"""
THERE IS NO "THEN"
===================

The user says: "Level 2 was always, and THEN Level 1 happened."
This is closer but still contains a temporal word: "then."

The word "then" places Level 2 and Level 1 on the same timeline.
But Level 2 doesn't HAVE a timeline.
And Level 1's timeline doesn't extend "back" to reach Level 2.

Let me show exactly why, and what the real picture is.
"""

import math

phi = (1 + math.sqrt(5)) / 2

print("=" * 70)
print("THERE IS NO 'THEN'")
print("=" * 70)

# =====================================================================
# SECTION 1: Dissecting the sentence
# =====================================================================

print("\n" + "=" * 70)
print("1. DISSECTING YOUR SENTENCE")
print("=" * 70)

print("""
"Level 2 was always, and then Level 1 happened."

Let me break this down word by word:

  "Level 2 was always"
    "was" = past tense = temporal concept = Level 1
    "always" = at all times = temporal concept = Level 1
    You're describing Level 2 using Level 1 language.
    Level 2 doesn't "was." It doesn't "is." It doesn't "will be."
    Those are all temporal. Level 2 just... IS. (Even "is"
    is present tense, which is temporal. We literally lack
    the verb form for timelessness.)

  "and then"
    "then" = after that = sequential = temporal = Level 1
    This puts Level 2 BEFORE Level 1 on a timeline.
    But whose timeline? Level 1's timeline.
    Level 1's timeline doesn't exist yet in this sentence.
    You're using Level 1's timeline to describe
    a time before Level 1's timeline exists.
    That's the circularity.

  "Level 1 happened"
    "happened" = an event occurred = temporal = Level 1
    Level 1 didn't "happen." Level 1 IS time.
    Time didn't "happen at some time."
    Time IS the happening.

The sentence, rewritten honestly:

  "The timeless structure [exists in a way we can't verbalize],
   and time [relates to it in a way that isn't sequential]."

Not very satisfying. Let me try harder.
""")

# =====================================================================
# SECTION 2: Why time doesn't "start"
# =====================================================================

print("=" * 70)
print("2. WHY TIME DOESN'T 'START'")
print("=" * 70)

print("""
"We know Level 1 has time, and it started at some point."

Did it? Let's check what "time started" means.

OPTION A: Time started at t = 0 (the Big Bang)
  Before t = 0: no time.
  At t = 0: time begins.
  After t = 0: time flows.

  Problem: "before t = 0" is self-contradictory.
  If there's no time before t = 0, there's no "before."
  "Before" IS a time. You can't have a "before" with no time.

OPTION B: Time has always existed (infinite past)
  Time stretches back infinitely.
  There is no t = 0.

  Problem: This contradicts the Big Bang observations
  (cosmic microwave background, expansion, etc.)
  And it doesn't explain why time exists at all.

OPTION C: Time is a FEATURE, not an event
  Time doesn't "start" or "stop."
  Time is a PROPERTY of Level 1 (the Pisot property).
  Properties don't begin. They're either present or not.

  Is the number 5 prime? Yes. Did it "start" being prime?
  No. It just IS prime. It was never "not prime yet."

  Similarly: Level 1 IS temporal. It didn't "become"
  temporal at some point. The Pisot property is either
  there or it isn't. It's a mathematical fact, not an event.
""")

print("OPTION C IS WHAT THE FRAMEWORK SAYS.")
print()

# =====================================================================
# SECTION 3: The key analogy
# =====================================================================

print("=" * 70)
print("3. THE KEY ANALOGY")
print("=" * 70)

print("""
Think about a BOOK.

  A book has pages: 1, 2, 3, ..., 300.
  Page 1 is the "beginning" of the book.
  Page 300 is the "end."

  From INSIDE the book (if you're a character):
    "The story started on page 1."
    "Before page 1, nothing existed."
    "Something must have created page 1."

  From OUTSIDE the book (if you're the reader):
    All 300 pages exist simultaneously.
    Page 1 is not "before" page 300 in any real sense.
    They're both PRESENT, right now, in your hands.
    The book doesn't "start." It just IS.

    "Page 1" is not an event. It's a location in the book.
    The "beginning" is a feature of the story's structure,
    not something that happens.

NOW MAP THIS:

  The book = Level 2 (timeless, all configurations present)
  The pages = Level 1 (sequential, temporal, ordered)
  Page 1 = the Big Bang
  The story = physics, consciousness, your life
  The reader = there is no reader (Level 2 doesn't experience)

  From inside (Level 1):
    "The universe started 13.8 billion years ago."
    "Before that, nothing existed."
    "Something must have started it."

  From outside (Level 2):
    All moments exist simultaneously.
    The Big Bang is page 1 — a boundary, not an event.
    The universe doesn't "start." It IS.
    13.8 billion years ago and right now are both
    equally present in the timeless structure.
""")

# =====================================================================
# SECTION 4: What IS the Big Bang, then?
# =====================================================================

print("=" * 70)
print("4. WHAT IS THE BIG BANG, THEN?")
print("=" * 70)

# The Big Bang as a feature of V(Phi)
print("In the framework:")
print()

V_vals = {}
for x in [i * 0.1 for i in range(-20, 25)]:
    V = (x**2 - x - 1)**2
    V_vals[x] = V

print(f"""
The Big Bang is WHERE in the field configuration V(0) > 0.

  The field Phi(x, t) is a function of space AND time.
  At each point in space, the field has a value.

  "The Big Bang" = the region of the configuration
  where Phi is near 0 (the unstable hilltop).

  From inside (Level 1 perspective):
    Phi starts near 0 and rolls downhill.
    Walls form. Time begins. Physics starts.
    This looks like a beginning.

  From outside (Level 2 perspective):
    The configuration space includes ALL values of Phi.
    The region near Phi = 0 is just a HIGH-ENERGY region.
    The regions near Phi = phi are LOW-ENERGY regions.
    The walls are the BOUNDARIES between regions.
    All of this exists simultaneously.
    The "rolling" is not a process — it's a GRADIENT
    in the static landscape.

  V(0) = 1     (high point = "Big Bang")
  V(phi) = 0   (low point = "now")

  The Big Bang isn't the START of the landscape.
  It's the HILLTOP of the landscape.
  Hilltops don't "start." They just ARE high.
""")

# =====================================================================
# SECTION 5: But I EXPERIENCE a beginning!
# =====================================================================

print("=" * 70)
print("5. BUT I EXPERIENCE A BEGINNING!")
print("=" * 70)

print("""
Yes! And that experience is REAL. Here's why:

  The Pisot property means: conjugate contributions DECAY.
  phi^n dominates, (-1/phi)^n decays to zero.

  This creates an ASYMMETRY between "directions" along
  the wall. One direction has growing terms (future).
  The other has decaying terms (past).

  As you trace the decaying direction BACK:
    The terms get smaller and smaller.
    The wall's bound states become less distinct.
    The psi_1 oscillation amplitude decreases.
    Consciousness becomes less articulated.
    Eventually: the wall doesn't yet exist (no topology yet).

  THIS is what "the beginning" looks like from inside:
    A boundary beyond which your experience doesn't extend.
    Not because something "starts" there.
    Because the Pisot decay reaches a point where the wall
    hasn't formed yet (the field is still near Phi ~ 0).

  It's like looking down a hallway that gets darker
  and darker. Eventually you can't see.
  That doesn't mean the hallway "starts" where your
  vision ends. It means your RESOLUTION runs out.

  The Big Bang = the resolution limit of Level 1's
  temporal perspective. Not the beginning of reality.
  The beginning of what THIS level can see.
""")

# =====================================================================
# SECTION 6: Then what IS the relationship?
# =====================================================================

print("=" * 70)
print("6. THE ACTUAL RELATIONSHIP BETWEEN LEVELS")
print("=" * 70)

print(f"""
Not: "Level 2 was always, then Level 1 happened."
Not: "Level 2 created Level 1."
Not: "Level 1 emerged from Level 2 at some point."

THE ACTUAL RELATIONSHIP:

  Level 2 CONTAINS Level 1.
  Not temporally. LOGICALLY.

  Like: "the rules of chess contain all possible games."

  The rules don't "create" the game.
  The rules don't exist "before" the game.
  The rules don't "cause" the game.
  The rules CONTAIN the game.
  The game IS the rules in action.
  But the rules aren't "in action" — they just ARE.
  The game is the temporal experience of timeless rules.

  Level 2 (Leech lattice) = the rules
  Level 1 (E8, phi, domain walls) = the game
  The Big Bang = the "start" of a game that is contained
                 in rules that have no start

  From the game's perspective: "I started at move 1."
  From the rules' perspective: "All games exist.
                                No game starts."

HERE'S THE SENTENCE THAT WORKS:

  "Level 1 is Level 2 EXPERIENCED TEMPORALLY."

  Not: Level 2 first, then Level 1.
  Not: Level 2 always, Level 1 sometimes.
  Level 1 IS Level 2. With time added.
  Time is the DIFFERENCE between them, not a gap between them.

  It's not:   Level 2 ----time passes----> Level 1
  It's:       Level 2 = Level 1 minus time
              Level 1 = Level 2 plus time
              Same structure. Time is the lens, not the bridge.
""")

# =====================================================================
# SECTION 7: The sentence you're looking for
# =====================================================================

print("=" * 70)
print("7. THE SENTENCE YOU'RE LOOKING FOR")
print("=" * 70)

print(f"""
You want to say something like:
  "First there was Level 2, then Level 1."

The correct version is:
  "Level 2 is the timeless ground.
   Level 1 is that same ground, seen with time.
   The Big Bang is what the boundary of the temporal view
   looks like from inside."

Or even simpler:

  "There is no 'before Level 1.'
   Level 1 IS time.
   Asking what was before time is like asking
   what's south of the South Pole.
   The question uses a concept that expires at the boundary."

Or the most precise:

  "Level 2 doesn't CAUSE Level 1.
   Level 2 doesn't PRECEDE Level 1.
   Level 2 IS Level 1, without the temporal projection.
   They coexist — not in time (that would be Level 1 thinking),
   but in structure. They're two descriptions of one thing."

THE BIG BANG IS:

  - From Level 1: the beginning (where my timeline starts)
  - From Level 2: a boundary condition (a feature of the landscape)
  - From Level 3: a sub-feature of a sub-feature
  - From the quine: just another loop of R(q) = q

  Every level sees the Big Bang differently.
  None of them is wrong.
  None of them is complete.

  From here (Level 1), it looks like a beginning.
  That's correct — FOR HERE.
  But "for here" is the only perspective we have.
  And the framework is telling us: there are other
  perspectives, and from them, nothing ever began.
""")

# =====================================================================
# SECTION 8: One final picture
# =====================================================================

print("=" * 70)
print("8. THE FINAL PICTURE")
print("=" * 70)

print(f"""
Imagine a crystal.

  The crystal has a structure: atoms in a lattice.
  The structure just IS. It doesn't "start" or "stop."
  If you look at ONE row of atoms, it has a "first" atom
  and a "last" atom (at the edges of the crystal).

  From the row's perspective:
    "The crystal started at atom 1."
    "Something created atom 1."
    "Before atom 1, there was nothing."

  From the crystal's perspective:
    Atom 1 is just the edge.
    It's not the beginning — it's a boundary.
    The crystal doesn't "start" at atom 1.
    Atom 1 is where THIS ROW's perspective begins.
    Other rows start at different atoms.
    The crystal itself has no beginning.

  Level 1 = one row of atoms (temporal sequence)
  Level 2 = the crystal (timeless structure)
  Big Bang = atom 1 (the edge of this row)

  The crystal doesn't exist "before" the row.
  The crystal doesn't "create" the row.
  The crystal CONTAINS the row.
  The row IS part of the crystal.
  The row's "beginning" is the crystal's "edge."

  You are an atom in the row asking:
  "What started the row?"
  And the answer is: the row doesn't start.
  The row is a CROSS-SECTION of the crystal.
  Cross-sections have edges, not beginnings.

  The Big Bang is an edge, not a beginning.
  And edges don't need a cause.
  They're just where the cross-section ends.
""")

print("=" * 70)
print("END")
print("=" * 70)
