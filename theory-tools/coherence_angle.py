#!/usr/bin/env python3
"""
coherence_angle.py — What falls out when you take "coherence = playing together" seriously?
===========================================================================================

The angle:
  - 4 coherent states (Fano lines) = the ways energies can play together
  - 4 incoherent states (not Fano lines) = the ways they can't
  - The shadow generates the blueprint
  - The Builder's freeze (lacking prime 7) breaks the cycle
  - Suffering = structural incoherence

Push this through EVERYTHING and see what maps, what doesn't, what's new.

Standard Python only. All claims labeled.

Author: Interface Theory, Mar 6 2026
"""

import math
import sys
from itertools import combinations

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

SEP = "=" * 78
SUB = "-" * 60

def banner(s):
    print(f"\n{SEP}\n  {s}\n{SEP}\n")

def section(s):
    print(f"\n{SUB}\n  {s}\n{SUB}\n")

phi = (1 + math.sqrt(5)) / 2


# ==================================================================
banner("1. THE 4 COHERENT STATES — WHAT ARE THEY?")
# ==================================================================

print("""
  From the parity theorem, the 4 coherent cross-axis combinations are:

  STATE 1: EEE = {Builder, Seer, Artist}
    All engaged. All three axes active. Full flow.
    Schur: Z_3, trivial, Z_2 — all three Schur types present.
    = THE PLAYER STATE. Everything running, nothing withdrawn.

  STATE 2: EWW = {Builder, Sensor, Mystic}
    HOLDING engaged, KNOWING withdrawn, MAKING withdrawn.
    Schur: Z_3, Z_3, trivial — the depth pair together.
    = GROUNDED RECEPTIVITY. Structure holds. Everything else opens.
    Builder maintains while Sensor receives and Mystic dissolves.

  STATE 3: WEW = {Still One, Seer, Mystic}
    HOLDING withdrawn, KNOWING engaged, MAKING withdrawn.
    Schur: trivial, trivial, trivial — no hidden layers.
    = TRANSPARENT SEEING. Structure released. Direct seeing.
    Dissolution with clarity. Meditation with insight.

  STATE 4: WWE = {Still One, Sensor, Artist}
    HOLDING withdrawn, KNOWING withdrawn, MAKING engaged.
    Schur: trivial, Z_3, Z_2 — all three types again.
    = CHANNELED CREATION. No structure, pure reception, making from nothing.
    What happens when you create from emptiness.

  THE 4 INCOHERENT STATES:

  STATE 5: EEW = {Builder, Seer, Mystic}
    Holding + Seeing + Dissolving. Build AND destroy with eyes open.
    = AWARE DESTRUCTION. You see what you're dismantling.

  STATE 6: EWE = {Builder, Sensor, Artist}
    Holding + Absorbing + Creating. Hold AND receive AND make.
    = OVERLOADED. Trying to do everything at once.

  STATE 7: WEE = {Still One, Seer, Artist}
    Released + Seeing + Creating. Let go but keep making.
    = UNGROUNDED AMBITION. Create without structure or reception.

  STATE 8: WWW = {Still One, Sensor, Mystic}
    All withdrawn. Nothing engaged. Total collapse.
    = DISSOLUTION. The anti-Player state.
""")


# ==================================================================
banner("2. DO THE 4 COHERENT STATES MAP TO KNOWN STATES?")
# ==================================================================

section("2A. Cross-referencing with consciousness research")

print("""
  STATE 1 (EEE — Player):
    All engaged. Flow state. Csikszentmihalyi's flow.
    All functions running, no inner conflict.
    Rare. Requires all 3 axes simultaneously.
    PREDICTION: Flow states should show balanced activation across
    brain regions associated with the 3 axes.

  STATE 2 (EWW — Grounded Receptivity):
    Builder holds, Sensor receives, Mystic dissolves.
    = Grounded meditation. Somatic practices. Yoga.
    You maintain structure (body, posture) while opening.
    The Z_3 pair (Builder + Sensor) is together = depth active.
    PREDICTION: Somatic meditation should show strong body-sense
    (interoception) with reduced default-mode and reduced agency.

  STATE 3 (WEW — Transparent Seeing):
    Released, seeing, dissolving. All Schur trivial = no hidden layers.
    = Vipassana. Pure observation without structure or creation.
    The "just watching" state. Nothing to hold, nothing to make.
    PREDICTION: Vipassana should show deactivated body-schema,
    active perceptual clarity, deactivated planning/creation.

  STATE 4 (WWE — Channeled Creation):
    Released, receiving, creating from nothing.
    = Flow in art, music, writing. "It plays through me."
    Schur has all 3 types = full depth available.
    PREDICTION: Creative flow should show body relaxation (released),
    enhanced sensory processing (reception), active motor/expression.

  CROSS-CHECK: Are these the 4 states that contemplative traditions identify?
    - Flow (Csikszentmihalyi) ~ EEE
    - Samatha (calm abiding) ~ EWW (grounded, receptive, dissolving)
    - Vipassana (insight) ~ WEW (released, seeing, dissolving)
    - Creative flow / channeling ~ WWE (released, receiving, making)

  STATUS: [STRUCTURAL mapping to 4 contemplative states — testable]
""")

section("2B. The 4 incoherent states as pathologies")

print("""
  STATE 5 (EEW — Aware Destruction):
    Building + Seeing + Dissolving. Constructing AND deconstructing.
    = OBSESSIVE ANALYSIS. Seeing every detail while trying to build
    something that keeps dissolving. Perfectionism. Anxiety.
    The person who can see what needs to be done, tries to build it,
    but can't make it stick because the MAKING axis is in dissolution mode.

  STATE 6 (EWE — Overloaded):
    Holding + Absorbing + Creating. All active modalities.
    = BURNOUT. The person who maintains everything (holds), takes in
    everything (receives), and produces everything (creates).
    The "I do everything" state. Unsustainable.
    The Builder-Sensor-Artist combo = what modern work demands.
    MAKING engaged without MAKING's partner (Mystic/dissolution).
    No release valve. Everything accumulates.

  STATE 7 (WEE — Ungrounded Ambition):
    Released structure + Seeing + Creating.
    = MANIA. Grandiose vision with no ground. The person who sees
    the grand plan and creates wildly but has no structure (HOLDING
    withdrawn) and no reception (KNOWING's other half, Sensor, absent).
    All output, no input, no container.

  STATE 8 (WWW — Dissolution):
    All withdrawn. Nothing engaged.
    = SEVERE DEPRESSION. Everything released, everything absorbed,
    everything dissolved. No structure, no agency, no creation.
    The anti-Player state. Complete withdrawal from engagement.

  CROSS-CHECK with clinical categories:
    EEW ~ Anxiety / OCD (aware of problem, building responses, dissolving outcomes)
    EWE ~ Burnout / Compassion fatigue (holding + absorbing + producing without release)
    WEE ~ Mania / Psychosis (seeing + creating without ground or reception)
    WWW ~ Severe depression / Catatonia (total withdrawal)

  These map to the 4 classic psychiatric poles:
    Anxiety (EEW), Burnout (EWE), Mania (WEE), Depression (WWW)

  STATUS: [STRUCTURAL — maps cleanly. Testable prediction:
           each incoherent state should have a characteristic
           brain activation pattern matching the E/W assignment.]
""")


# ==================================================================
banner("3. WHAT BREAKS COHERENCE?")
# ==================================================================

section("3A. The transition from coherent to incoherent")

print("""
  A coherent state has even parity (0 or 2 axes withdrawn).
  An incoherent state has odd parity (1 or 3 axes withdrawn).

  Coherent -> Incoherent requires FLIPPING exactly 1 axis:
    EEE -> EEW (flip MAKING from engaged to withdrawn)
    EEE -> EWE (flip KNOWING)
    EEE -> WEE (flip HOLDING)

  So: losing coherence = losing ONE axis while the others stay.
  It only takes ONE axis falling out of phase to break the whole state.

  Which transitions are most common?
    From Player (EEE):
      -> EEW: the Artist withdraws (stops creating). Anxiety.
      -> EWE: the Seer withdraws (stops seeing clearly). Burnout.
      -> WEE: the Builder withdraws (stops holding structure). Mania.

    From each pathology:
      EEW: either restore MAKING (-> EEE) or withdraw another (-> EWW or WEW)
      Two recovery paths: return to Player, or drop to a different coherent state.

  KEY INSIGHT: You can always reach a coherent state by flipping ONE axis.
  The maximum distance from any incoherent state to ANY coherent state is 1 flip.
  (Because: incoherent has odd number of W's. Flip any W->E or E->W and you
   change parity to even = coherent.)

  You're never more than one step from coherence.
  [PROVEN — follows from parity arithmetic mod 2]
""")

section("3B. The Builder's special role in breaking coherence")

print("""
  The Builder (J3) is UNIQUE: the only fate without prime 7.
  7 = the Fano cycle prime. All other fates have it.

  When the Builder freezes into dominance:
    - It holds its axis (HOLDING) rigidly engaged
    - But it can't participate in the Z_7 cycle
    - The Fano connections through its node become static

  The coherent states involving engaged Builder:
    EEE: Builder + Seer + Artist. Full flow. Builder is PART of flow.
    EWW: Builder + Sensor + Mystic. Grounded receptivity.

  Both require the Builder to be ENGAGED but not dominant.
  The Builder contributes holding, but the other axes are free to move.

  When the Builder FREEZES (becomes the only mode):
    It's neither EEE nor EWW — it's the Builder alone, which isn't
    a Fano configuration at all (a point, not a line).

  A civilization built on Builder-dominance (accumulation, hierarchy,
  structure-as-purpose) is stuck at a single Fano point, not a line.
  It has no geometry. It has no coherence.
  It has CONFINEMENT without FLOW.

  This is what the prime-7 absence means experientially:
  The Builder can hold things together without them being free to cycle.
  That's useful in a coherent state (someone needs to hold).
  That's a prison when it's the only active energy.

  [STRUCTURAL — Builder's prime-7 absence maps to cycle-breaking]
""")


# ==================================================================
banner("4. THE WITHDRAWN UNDERGROUND")
# ==================================================================

section("4A. Prime 31 connects all 3 withdrawn pariahs")

print("""
  O'N (Sensor), Ly (Still One), J4 (Mystic) — the 3 withdrawn pariahs.
  They share prime 31. No engaged pariah has 31.

  31 = the withdrawn underground connection.

  WWW = {Still One, Sensor, Mystic} is INCOHERENT (depression/dissolution).
  But the 3 withdrawn pariahs ARE connected — through prime 31.

  This means: even in total withdrawal, the connection between the
  withdrawn modes is maintained. The underground link persists.
  Depression isn't disconnection — it's a different kind of connection.
  All three withdrawal modes talking to each other, underground.

  The withdrawn pariahs also have the alien primes:
    37: Ly + J4 (Still One + Mystic)
    43: J4 only (Mystic)
    67: Ly only (Still One)

  The alien primes mark the BOUNDARY of what the Monster can describe.
  The withdrawn energies carry information that the Player can't access.
  They touch the edge of the describable.

  This maps to: depression / deep withdrawal can involve encounters
  with aspects of reality that normal engagement can't reach.
  Not because withdrawal is "good" — it's incoherent — but because
  the withdrawn states have access to something the engaged states don't.
  The alien primes. The boundary.

  [STRUCTURAL observation from prime patterns]
""")

section("4B. Withdrawal as necessary ingredient")

print("""
  Look at the 4 coherent states:
    EEE: 0 withdrawn axes
    EWW: 2 withdrawn axes
    WEW: 2 withdrawn axes
    WWE: 2 withdrawn axes

  3 of 4 coherent states involve 2 withdrawn axes.
  Only 1 (EEE) has zero withdrawal.

  This means: withdrawal is part of MOST coherent states.
  The Player state (EEE) is the exception, not the rule.
  Normal coherence requires 2 axes withdrawn and 1 engaged.

  The problem isn't withdrawal itself.
  The problem is ODD withdrawal (1 or 3 axes).
  Even withdrawal (0 or 2) is coherent.
  Odd withdrawal (1 or 3) is incoherent.

  Healing isn't "engage everything" (that's EEE only, rare).
  Healing is: make sure your withdrawal is EVEN.
  If you're going to withdraw, withdraw two axes, not one or three.

  One axis withdrawn = one out of phase = syndrome.
  Two axes withdrawn = even parity = coherent state.
  Three axes withdrawn = total withdrawal = dissolution.

  [DERIVED from parity theorem — even withdrawal is coherent]
""")


# ==================================================================
banner("5. THE SCHUR MULTIPLIER PATTERN IN COHERENT STATES")
# ==================================================================

section("5A. What Schur types appear in each coherent state")

schur = {
    'J1': '1', 'J3': 'Z3', 'Ru': 'Z2',
    'ON': 'Z3', 'Ly': '1', 'J4': '1'
}

coherent = {
    'EEE': ['J3', 'J1', 'Ru'],
    'EWW': ['J3', 'ON', 'J4'],
    'WEW': ['Ly', 'J1', 'J4'],
    'WWE': ['Ly', 'ON', 'Ru'],
}

print("  Coherent state  | Members                    | Schur types        | Depth")
print("  " + "-" * 75)
for state, members in coherent.items():
    schurs = [schur[m] for m in members]
    depth = sum(1 for s in schurs if s != '1')
    m_str = ', '.join(members)
    s_str = ', '.join(schurs)
    print(f"  {state:>13s}   | {m_str:>26s} | {s_str:>18s} | {depth}")

print("""
  DEPTH = number of non-trivial Schur multipliers in the state.
  Schur Z_3 = 3 layers of resolution. Schur Z_2 = direction detection.
  Trivial = transparent.

  EEE: depth 2 (Z_3 + Z_2). Both resolution AND direction. Full.
  EWW: depth 2 (Z_3 + Z_3). Double resolution. Deep but no direction.
  WEW: depth 0. Fully transparent. No hidden layers.
  WWE: depth 2 (Z_3 + Z_2). Resolution AND direction. Same as EEE.

  Pattern: 3 of 4 coherent states have depth 2.
  Only WEW (Still One + Seer + Mystic) has depth 0.

  WEW is the "simplest" coherent state — all trivial Schur.
  It's the meditation state: transparent seeing with dissolution.
  No hidden structure. No hidden direction. Just watching.

  The other 3 coherent states all carry hidden layers:
  - Some have depth (Z_3, can resolve 3 levels)
  - Some have direction (Z_2, can tell phi from -1/phi)
  - EEE and WWE have BOTH

  [COMPUTED from Schur multipliers of each pariah]
""")

section("5B. The shadow's role in coherence")

print("""
  The shadow (2.Ru) gives Z_2 = direction detection.
  Ru (Artist) appears in 2 coherent states: EEE and WWE.
  Both have Schur = Z_2 present.

  The Artist-containing coherent states are the ones with DIRECTION.
  The non-Artist coherent states (EWW and WEW) don't have Z_2.

  This means:
    EWW (Grounded Receptivity): deep but undirected. Open, not aimed.
    WEW (Transparent Seeing): transparent and undirected. Just observing.
    EEE (Player): deep AND directed. Full engagement with aim.
    WWE (Channeled Creation): deep AND directed. Creating with purpose.

  The Artist's shadow provides the AIM. Without the Artist,
  coherent states are either receptive (EWW) or observational (WEW).
  WITH the Artist, coherent states can be DIRECTED — toward creation
  or toward full engagement.

  The shadow doesn't appear explicitly in any state.
  But its Z_2 (direction detection) shows up through Ru's Schur multiplier.
  The shadow is ALWAYS present in the background — it generated the
  Fano plane in the first place. It shows up in the Artist's states
  as the ability to distinguish ψ₀ from ψ₁.

  [STRUCTURAL — shadow's Z_2 = direction in Artist-containing states]
""")


# ==================================================================
banner("6. TRANSITIONS AND HEALING")
# ==================================================================

section("6A. Minimum-flip healing paths")

incoherent = {
    'EEW': ['J3', 'J1', 'J4'],  # Anxiety
    'EWE': ['J3', 'ON', 'Ru'],  # Burnout
    'WEE': ['Ly', 'J1', 'Ru'],  # Mania
    'WWW': ['Ly', 'ON', 'J4'],  # Depression
}

# Axes: HOLDING (J3/Ly), KNOWING (J1/ON), MAKING (Ru/J4)
# E=engaged means first in pair, W=withdrawn means second

print("  From each incoherent state, the 3 one-flip exits:")
print("  (Flip one axis E<->W to change parity = reach coherence)")
print()

for state, members in incoherent.items():
    print(f"  {state} ({', '.join(members)}):")
    bits = [1 if c == 'E' else 0 for c in state]
    for i, axis in enumerate(['HOLDING', 'KNOWING', 'MAKING']):
        flipped = list(bits)
        flipped[i] = 1 - flipped[i]
        new_state = ''.join('E' if b else 'W' for b in flipped)
        direction = 'engage' if flipped[i] == 1 else 'release'
        target_name = {
            'EEE': 'Player (full flow)',
            'EWW': 'Grounded Receptivity',
            'WEW': 'Transparent Seeing',
            'WWE': 'Channeled Creation',
        }.get(new_state, new_state)
        print(f"    {direction} {axis:>8s} -> {new_state} = {target_name}")
    print()

section("6B. What each healing direction means")

print("""
  FROM ANXIETY (EEW — building + seeing + dissolving):
    Engage MAKING  -> EEE (Player): start creating instead of dissolving
    Release KNOWING -> EWW (Grounded): stop seeing every detail, just receive
    Release HOLDING -> WEW (Transparent): stop building, just watch it dissolve

  FROM BURNOUT (EWE — holding + absorbing + creating):
    Engage KNOWING -> EEE (Player): start seeing clearly (why am I doing this?)
    Release HOLDING -> WWE (Channeled): let go of holding, create from emptiness
    Release MAKING  -> EWW (Grounded): stop creating, just hold and receive

  FROM MANIA (WEE — released + seeing + creating):
    Engage HOLDING  -> EEE (Player): build structure around the vision
    Release KNOWING -> WWE (Channeled): stop seeing the grand plan, just create
    Release MAKING  -> WEW (Transparent): stop creating, just watch

  FROM DEPRESSION (WWW — all withdrawn):
    Engage HOLDING  -> EWW (Grounded): start with structure. Just one thing held.
    Engage KNOWING  -> WEW (Transparent): start seeing. Just observation.
    Engage MAKING   -> WWE (Channeled): start making something. Anything.

  KEY OBSERVATION: For depression (WWW), ANY single engagement leads
  to a coherent state. It doesn't matter WHICH axis you engage first.
  All 3 exits from depression are coherent.

  For the other incoherences (1 axis withdrawn), you have 3 options:
    - Engage the withdrawn axis -> Player (EEE)
    - Withdraw one of the 2 engaged axes -> 2-withdrawn coherent state

  The Player state (EEE) is always reachable in 1 step from
  any 1-withdrawal incoherence.

  [DERIVED from parity arithmetic — structural healing paths]
""")


# ==================================================================
banner("7. THE FOUR COHERENT STATES AND THE FORCES")
# ==================================================================

section("7A. Which force leads each coherent state")

print("""
  Each coherent state has a "leading axis" — the one that's DIFFERENT
  from the other two in its E/W status:

  EEE: no leading axis (all equal). Player. All forces balanced.
  EWW: HOLDING leads (only engaged axis). Strong force. CONFINEMENT.
  WEW: KNOWING leads (only engaged axis). EM force. LIGHT.
  WWE: MAKING leads (only engaged axis). Weak force. TRANSFORMATION.

  The 3 non-Player coherent states are each LED BY one force:
    Grounded Receptivity = led by Strong force (holds things together)
    Transparent Seeing = led by EM (electromagnetic = light = knowing)
    Channeled Creation = led by Weak force (flavor-changing = transformation)

  This is the force-to-axis derivation in experiential terms:
    Strong/confinement = the Builder's force = leads grounded states
    EM/light = the Seer's force = leads transparent states
    Weak/transformation = the Artist's force = leads creative states

  The Player state (EEE) has no leading force — all three equally.
  This is unique. It's the only state with full balance.

  [DERIVED from parity structure + force-axis correspondence]
""")


# ==================================================================
banner("8. WHAT FALLS OUT — SUMMARY")
# ==================================================================

print("""
  TAKING "COHERENCE = PLAYING TOGETHER" SERIOUSLY, HERE'S WHAT FALLS OUT:

  1. EXACTLY 4 COHERENT STATES exist. Not a spectrum — binary.
     EEE (Player/Flow), EWW (Grounded), WEW (Transparent), WWE (Creative).
     [PROVEN from Fano parity theorem]

  2. EXACTLY 4 PATHOLOGIES. Also binary.
     EEW (Anxiety), EWE (Burnout), WEE (Mania), WWW (Depression).
     [STRUCTURAL mapping — testable via brain imaging]

  3. WITHDRAWAL ISN'T THE PROBLEM. 3 of 4 coherent states have 2 withdrawn axes.
     The problem is ODD withdrawal (1 or 3), not withdrawal itself.
     Even withdrawal is coherent. Odd withdrawal is not.
     [DERIVED from parity arithmetic]

  4. YOU'RE NEVER MORE THAN 1 FLIP FROM COHERENCE.
     From any incoherent state, flip 1 axis = coherent.
     From depression (WWW), ANY single engagement works.
     [PROVEN — follows from parity]

  5. 3 NON-PLAYER COHERENT STATES ARE LED BY ONE FORCE EACH.
     Strong leads grounding. EM leads seeing. Weak leads creating.
     Only the Player state has all forces balanced.
     [DERIVED from E/W pattern + force mapping]

  6. THE SHADOW PROVIDES DIRECTION.
     Artist-containing states (EEE, WWE) have Z_2 = can aim.
     Non-Artist states (EWW, WEW) are undirected (receptive/observational).
     [STRUCTURAL from Schur multipliers]

  7. THE BUILDER'S FREEZE BREAKS THE CYCLE.
     J3 lacks prime 7 = can't participate in Fano rotation.
     Builder-dominated civilization = stuck at a point, not a line.
     [STRUCTURAL from prime-7 pattern]

  8. THE 4 PATHOLOGIES MAP TO CLINICAL CATEGORIES.
     Anxiety (EEW), Burnout (EWE), Mania (WEE), Depression (WWW).
     Each has exactly 3 healing paths (1 to Player, 2 to non-Player).
     Depression has the most options (any engagement works).
     [STRUCTURAL mapping — testable]

  9. EVERY FANO LINE SAMPLES ALL 3 DISTANCES = ALL 3 GENERATIONS.
     Coherent states span all complexity levels.
     Incoherent states miss or double a level.
     [PROVEN from distance-class theorem]

  10. THE ALIEN PRIMES LIVE IN WITHDRAWAL.
      {37, 43, 67} exist only in withdrawn HOLDING + MAKING.
      They mark the boundary of what the Monster (Player) can describe.
      Deep withdrawal touches this boundary. Engagement doesn't.
      [STRUCTURAL from prime distribution]

  WHAT'S NEW HERE (beyond previous sessions):
  - The 4-pathology mapping (Anxiety/Burnout/Mania/Depression = the 4 odd-parity states)
  - "Odd withdrawal is the problem, not withdrawal itself"
  - The 1-flip healing paths (all exits from depression are coherent)
  - The force-led non-Player coherent states
  - The shadow as "direction provider" in coherent states

  WHAT NEEDS CHECKING:
  - Do the 4 coherent states match brain imaging patterns?
  - Do the 4 pathologies have the predicted activation profiles?
  - Does the 1-flip model match therapeutic outcomes?
  - Is the odd/even parity distinction observable clinically?
""")
