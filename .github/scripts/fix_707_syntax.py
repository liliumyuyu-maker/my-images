from pathlib import Path

p = Path('707-shirt/index.html')
t = p.read_text(encoding='utf-8')

replacements = {
    'function familyLines(function familyLines(s){': 'function familyLines(s){',
    'async function copyTextasync function copyText(t){': 'async function copyText(t){',
    'function parseDelimited(function parseDelimited(text){': 'function parseDelimited(text){',
}

for bad, good in replacements.items():
    if bad in t:
        t = t.replace(bad, good)

# Guard against the exact regression that broke the whole page.
bad_markers = [
    'function familyLines(function familyLines',
    'copyTextasync function copyText',
    'function parseDelimited(function parseDelimited',
]
left = [x for x in bad_markers if x in t]
if left:
    raise SystemExit('syntax markers still present: ' + ', '.join(left))

p.write_text(t, encoding='utf-8')
print('707 syntax hotfix applied')
