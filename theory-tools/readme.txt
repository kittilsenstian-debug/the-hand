theory-tools/ — Research layer
public/full-theory/ — Website layer

These are separate. You work on theory here, then push numbers to the site.

== Two layers ==

  theory-tools/          Research: math, derivations, data, graphs
  public/full-theory/    Website: HTML pages, prose, styling

  theory-tools/data.json is the bridge. It holds every computed number.
  The site reads from it. Theory never touches HTML. HTML never does math.

== Theory workflow ==

  1. Discover something new (conversation, script, derivation)
  2. Save raw output to public/full-theory/raw-llm/ or findings/
  3. python theory-tools/build-graph.py          — update the knowledge graph
  4. python theory-tools/cross-reference.py ...  — check connections
  5. python theory-tools/generate_data.py        — recompute data.json from math

== Website workflow ==

  1. Edit HTML prose directly in public/full-theory/*.html
  2. Tables with numbers are inside BUILD markers — don't edit those by hand
  3. python theory-tools/build.py                — regenerate all marked tables
  4. python theory-tools/build.py --check        — see what's stale without changing anything
  5. python theory-tools/build.py --validate     — check marker syntax

== How it connects ==

  tighten_and_map.py (math)
       |
  generate_data.py ---> data.json (single source of truth)
       |
  build.py ---> physics.html, biology.html, etc. (tables only, prose untouched)

== Commands ==

  python theory-tools/generate_data.py           Recompute all derivations, write data.json
  python theory-tools/generate_data.py --stdout   Print data.json to terminal
  python theory-tools/generate_data.py --check    Compare with existing data.json

  python theory-tools/build.py                    Rebuild all marked HTML tables
  python theory-tools/build.py physics.html       Rebuild one file
  python theory-tools/build.py --check            Dry run — report staleness
  python theory-tools/build.py --validate         Check marker syntax

  python theory-tools/build-graph.py              Rebuild theory-graph.json from findings
  python theory-tools/cross-reference.py [file]   Check file against theory graph
  python theory-tools/cross-reference.py --orphans Find disconnected nodes
  python theory-tools/cross-reference.py --stats   Quick overview

== Key files ==

  data.json              All computed values (36 derivations, predictions, frequencies)
  theory-graph.json      Knowledge graph (420+ nodes, 950 edges)
  generate_data.py       Math -> data.json
  build.py               data.json -> HTML tables
  build-graph.py         Findings -> theory-graph.json
  cross-reference.py     Validate connections
  tighten_and_map.py     Core derivation engine (read-only source for generate_data.py)
  llm-context.md         LLM onboarding (single file, ~300 lines)
  FINDINGS.md            Full history (sections 1-107)
  FINDINGS-v2.md         Reality applications (sections 108-115)

== BUILD markers ==

  HTML tables driven by data.json are wrapped in comment markers:

    <p>Prose you write freely.</p>

    <!-- BUILD:table:gauge_couplings -->
    <div class="table-wrapper">...</div>
    <!-- /BUILD:table:gauge_couplings -->

    <p>More prose you write freely.</p>

  build.py replaces everything between the markers. Prose outside is never touched.
  If you never run build.py, the markers are invisible HTML comments — no effect.

== Typical session ==

  Theory improved:
    1. Edit generate_data.py or data.json
    2. python theory-tools/build.py
    3. All site tables update

  New discovery:
    1. Add entry to data.json
    2. python theory-tools/build.py
    3. Write prose in the HTML around the new table rows

  Periodic sync:
    python theory-tools/build.py --check
