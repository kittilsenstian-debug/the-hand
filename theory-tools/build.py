#!/usr/bin/env python3
"""
build.py — Data -> HTML in-place

Reads data.json, scans HTML files for BUILD markers, regenerates content
between markers. Prose outside markers is never touched.

Usage:
    python theory-tools/build.py                    # rebuild all marked files
    python theory-tools/build.py physics.html       # rebuild one file
    python theory-tools/build.py --check            # dry run, report staleness
    python theory-tools/build.py --validate         # check marker syntax

Marker types:
    <!-- BUILD:table:category_name -->  ... <!-- /BUILD:table:category_name -->
    <!-- BUILD:value:path.to.value -->  ... <!-- /BUILD:value:path.to.value -->
    <!-- BUILD:scorecard -->            ... <!-- /BUILD:scorecard -->
"""

import json
import os
import re
import sys
import glob as glob_mod

# ============ PATHS ============

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(SCRIPT_DIR, 'data.json')
SITE_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), 'public', 'full-theory')

# ============ MARKER REGEX ============

# Matches: <!-- BUILD:type:name --> ... <!-- /BUILD:type:name -->
MARKER_RE = re.compile(
    r'([ \t]*)(<!-- BUILD:(\w+):([\w.]+) -->)\n'
    r'(.*?)'
    r'([ \t]*<!-- /BUILD:\3:\4 -->)',
    re.DOTALL
)

# Simpler pattern for scorecard (no second param)
SCORECARD_RE = re.compile(
    r'([ \t]*)(<!-- BUILD:scorecard -->)\n'
    r'(.*?)'
    r'([ \t]*<!-- /BUILD:scorecard -->)',
    re.DOTALL
)

# ============ LOAD DATA ============

def load_data():
    """Load data.json and return dict."""
    if not os.path.exists(DATA_PATH):
        print(f'Error: {DATA_PATH} not found. Run generate_data.py first.')
        sys.exit(1)
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


# ============ RENDERERS ============

def match_class(pct):
    """Return CSS class for match percentage."""
    if pct >= 99.0:
        return 'match-high'
    elif pct >= 95.0:
        return 'match-good'
    return ''


def render_table(data, category, indent=''):
    """Render a derivation table for the given category."""
    items = [d for d in data['derivations'] if d['category'] == category]
    if not items:
        return f'{indent}<p><em>No derivations found for category: {category}</em></p>\n'

    lines = []
    lines.append(f'{indent}<div class="table-wrapper">')
    lines.append(f'{indent}    <table>')
    lines.append(f'{indent}        <tr>')
    lines.append(f'{indent}            <th>Quantity</th>')
    lines.append(f'{indent}            <th>Formula</th>')
    lines.append(f'{indent}            <th>Predicted</th>')
    lines.append(f'{indent}            <th>Measured</th>')
    lines.append(f'{indent}            <th>Match</th>')
    lines.append(f'{indent}        </tr>')

    for d in items:
        novel_class = ' class="novel"' if d['novel'] else ''
        mcls = match_class(d['match_pct'])
        match_td_class = f' class="{mcls}"' if mcls else ''
        match_display = f'{d["match_pct"]:.1f}%' if d['match_pct'] < 100 else '~100%'

        lines.append(f'{indent}        <tr{novel_class}>')
        lines.append(f'{indent}            <td>{d["name"]}</td>')
        lines.append(f'{indent}            <td><code>{d["formula_display"]}</code></td>')
        lines.append(f'{indent}            <td>{d["predicted_display"]}</td>')
        lines.append(f'{indent}            <td>{d["measured_display"]}</td>')
        lines.append(f'{indent}            <td{match_td_class}>{match_display}</td>')
        lines.append(f'{indent}        </tr>')

    lines.append(f'{indent}    </table>')
    lines.append(f'{indent}</div>')

    return '\n'.join(lines) + '\n'


def resolve_value_path(data, path):
    """Resolve a dotted path like 'scorecard.total' into data."""
    parts = path.split('.')
    obj = data
    for part in parts:
        if isinstance(obj, dict):
            obj = obj.get(part)
        elif isinstance(obj, list):
            try:
                obj = obj[int(part)]
            except (ValueError, IndexError):
                return None
        else:
            return None
        if obj is None:
            return None
    return obj


def render_value(data, path, indent=''):
    """Render a single inline value."""
    val = resolve_value_path(data, path)
    if val is None:
        return f'{indent}<span class="build-error">Unknown path: {path}</span>\n'
    return f'{indent}<span class="build-value">{val}</span>\n'


def render_scorecard(data, indent=''):
    """Render the scorecard summary block."""
    sc = data['scorecard']
    lines = []
    lines.append(f'{indent}<div class="scorecard-compact">')
    lines.append(f'{indent}    <div class="scorecard-stat">')
    lines.append(f'{indent}        <div class="scorecard-number">{sc["total"]}</div>')
    lines.append(f'{indent}        <div class="scorecard-label">derivations</div>')
    lines.append(f'{indent}    </div>')
    lines.append(f'{indent}    <div class="scorecard-stat">')
    lines.append(f'{indent}        <div class="scorecard-number">{sc["above_99"]}</div>')
    lines.append(f'{indent}        <div class="scorecard-label">above 99%</div>')
    lines.append(f'{indent}    </div>')
    lines.append(f'{indent}    <div class="scorecard-stat">')
    lines.append(f'{indent}        <div class="scorecard-number">{sc["above_95"]}</div>')
    lines.append(f'{indent}        <div class="scorecard-label">above 95%</div>')
    lines.append(f'{indent}    </div>')
    lines.append(f'{indent}    <div class="scorecard-stat">')
    lines.append(f'{indent}        <div class="scorecard-number">{sc["average_match"]}%</div>')
    lines.append(f'{indent}        <div class="scorecard-label">average match</div>')
    lines.append(f'{indent}    </div>')
    lines.append(f'{indent}    <div class="scorecard-stat">')
    lines.append(f'{indent}        <div class="scorecard-number">{sc["free_parameters"]}</div>')
    lines.append(f'{indent}        <div class="scorecard-label">free parameter</div>')
    lines.append(f'{indent}    </div>')
    lines.append(f'{indent}</div>')
    return '\n'.join(lines) + '\n'


# ============ PROCESS FILE ============

def process_file(filepath, data, check_only=False):
    """Process a single HTML file. Returns (changed, messages)."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    messages = []
    new_content = content

    def replace_marker(m):
        indent = m.group(1)
        open_tag = m.group(2)
        marker_type = m.group(3)
        marker_name = m.group(4)
        old_content = m.group(5)
        close_tag = m.group(6)

        if marker_type == 'table':
            generated = render_table(data, marker_name, indent + '    ')
        elif marker_type == 'value':
            generated = render_value(data, marker_name, indent + '    ')
        else:
            messages.append(f'  Unknown marker type: {marker_type}')
            return m.group(0)

        if old_content.strip() == generated.strip():
            return m.group(0)

        messages.append(f'  {marker_type}:{marker_name} — updated')
        return f'{indent}{open_tag}\n{generated}{close_tag}'

    def replace_scorecard(m):
        indent = m.group(1)
        open_tag = m.group(2)
        old_content = m.group(3)
        close_tag = m.group(4)

        generated = render_scorecard(data, indent + '    ')

        if old_content.strip() == generated.strip():
            return m.group(0)

        messages.append(f'  scorecard — updated')
        return f'{indent}{open_tag}\n{generated}{close_tag}'

    new_content = MARKER_RE.sub(replace_marker, new_content)
    new_content = SCORECARD_RE.sub(replace_scorecard, new_content)

    changed = new_content != content
    rel_path = os.path.relpath(filepath, os.path.dirname(SCRIPT_DIR))

    if changed:
        if check_only:
            messages.insert(0, f'{rel_path}: STALE')
        else:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            messages.insert(0, f'{rel_path}: updated')
    else:
        if not messages:
            messages.append(f'{rel_path}: up to date')

    return changed, messages


# ============ VALIDATE ============

def validate_file(filepath, data):
    """Validate marker syntax in a file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    errors = []
    rel_path = os.path.relpath(filepath, os.path.dirname(SCRIPT_DIR))

    # Find all opening markers
    opens = re.findall(r'<!-- BUILD:(\w+):([\w.]+) -->', content)
    closes = re.findall(r'<!-- /BUILD:(\w+):([\w.]+) -->', content)

    open_set = set(opens)
    close_set = set(closes)

    for o in open_set:
        if o not in close_set:
            errors.append(f'{rel_path}: unclosed marker BUILD:{o[0]}:{o[1]}')

    for c in close_set:
        if c not in open_set:
            errors.append(f'{rel_path}: orphan close marker /BUILD:{c[0]}:{c[1]}')

    # Check scorecard markers
    sc_opens = len(re.findall(r'<!-- BUILD:scorecard -->', content))
    sc_closes = len(re.findall(r'<!-- /BUILD:scorecard -->', content))
    if sc_opens != sc_closes:
        errors.append(f'{rel_path}: mismatched scorecard markers ({sc_opens} opens, {sc_closes} closes)')

    # Check table categories exist in data
    categories = {d['category'] for d in data['derivations']}
    for marker_type, marker_name in opens:
        if marker_type == 'table' and marker_name not in categories:
            errors.append(f'{rel_path}: BUILD:table:{marker_name} — category not in data.json')
        elif marker_type == 'value':
            val = resolve_value_path(data, marker_name)
            if val is None:
                errors.append(f'{rel_path}: BUILD:value:{marker_name} — path not in data.json')

    return errors


# ============ FIND HTML FILES ============

def find_html_files():
    """Find all HTML files in the site directory."""
    pattern = os.path.join(SITE_DIR, '**', '*.html')
    return glob_mod.glob(pattern, recursive=True)


def has_markers(filepath):
    """Check if file contains any BUILD markers."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    return '<!-- BUILD:' in content


# ============ MAIN ============

def main():
    data = load_data()

    check_only = '--check' in sys.argv
    validate_only = '--validate' in sys.argv

    # Get target files
    args = [a for a in sys.argv[1:] if not a.startswith('--')]

    if args:
        # Specific file(s)
        files = []
        for arg in args:
            path = os.path.join(SITE_DIR, arg)
            if os.path.exists(path):
                files.append(path)
            elif os.path.exists(arg):
                files.append(os.path.abspath(arg))
            else:
                print(f'File not found: {arg}')
                sys.exit(1)
    else:
        # All files with markers
        files = [f for f in find_html_files() if has_markers(f)]

    if not files:
        print('No files with BUILD markers found.')
        return

    if validate_only:
        all_errors = []
        for filepath in files:
            errors = validate_file(filepath, data)
            all_errors.extend(errors)

        if all_errors:
            for e in all_errors:
                print(f'ERROR: {e}')
            sys.exit(1)
        else:
            print(f'All {len(files)} file(s) valid.')
            sys.exit(0)

    any_changed = False
    for filepath in files:
        changed, messages = process_file(filepath, data, check_only=check_only)
        for msg in messages:
            print(msg)
        if changed:
            any_changed = True

    if check_only:
        if any_changed:
            print()
            print('Some files are stale. Run `python theory-tools/build.py` to update.')
            sys.exit(1)
        else:
            print()
            print('All files up to date.')
            sys.exit(0)


if __name__ == '__main__':
    main()
