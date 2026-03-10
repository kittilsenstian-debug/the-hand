#!/usr/bin/env python3
"""Build viewer.html with book.json + fieldguide.json inlined — run this after editing either"""
import json, os

dir_path = os.path.dirname(os.path.abspath(__file__))

# Load book data
with open(os.path.join(dir_path, 'book.json'), 'r', encoding='utf-8') as f:
    book_data = f.read().strip()
json.loads(book_data)  # validate

# Load field guide data
guide_path = os.path.join(dir_path, 'fieldguide.json')
if os.path.exists(guide_path):
    with open(guide_path, 'r', encoding='utf-8') as f:
        guide_data = f.read().strip()
    json.loads(guide_data)  # validate
else:
    guide_data = '{"title":"FIELD GUIDE","subtitle":"Coming soon","intro":"","chains":[],"observations":[],"species":{"psi0":{"name":"","signature":[]},"psi1":{"name":"","signature":[]}},"three_states":[]}'

with open(os.path.join(dir_path, 'viewer-template.html'), 'r', encoding='utf-8') as f:
    template = f.read()

output = template.replace('%%BOOK_DATA%%', book_data).replace('%%GUIDE_DATA%%', guide_data)

with open(os.path.join(dir_path, 'viewer.html'), 'w', encoding='utf-8') as f:
    f.write(output)

print(f"Built viewer.html ({len(output):,} bytes)")
print(f"  Book data: {len(book_data):,} bytes")
print(f"  Guide data: {len(guide_data):,} bytes")
