from pathlib import Path

root = Path(__file__).resolve().parents[1] / 'dist'

pages = {
    'voice-dream-journal/index.html': {
        'intent': 'Voice Dream Journal',
        'markers': ['Dream recording is one use of the same nighttime capture system.', 'Thoughts · ideas · dreams'],
    },
    'hands-free-dream-journal/index.html': {
        'intent': 'Record a Dream Without Unlocking Your Phone',
        'markers': ['Time and alarm are not side decorations', 'Hands-free night capture'],
    },
    'remember-dreams/index.html': {
        'intent': 'How to Remember Dreams Before They Fade',
        'markers': ['A recall routine works better when the night is already prepared.', 'Dreams are one Somnori layer'],
    },
    'dream-journal/index.html': {
        'intent': 'A Dream Journal Designed Around the Night Itself',
        'markers': ['The dream journal is a major Somnori layer', 'The important change: dreams are not the only reason to use Somnori'],
    },
}

for rel, cfg in pages.items():
    path = root / rel
    assert path.exists(), f'missing v2.3 page: {rel}'
    html = path.read_text(encoding='utf-8')
    assert cfg['intent'] in html, f'SEO intent/H1 drift: {rel}'
    assert 'seo-product-bridge' in html, f'product bridge missing: {rel}'
    assert 'data-screenshot-slot=' in html, f'neutral screenshot slot missing: {rel}'
    for marker in cfg['markers']:
        assert marker in html, f'v2.3 marker missing in {rel}: {marker}'

# Guard against the old dream-only positioning returning.
for rel in ['hands-free-dream-journal/index.html', 'dream-journal/index.html']:
    html = (root / rel).read_text(encoding='utf-8')
    forbidden = [
        'They are not the main reason to install Somnori',
        'They are not the reason Somnori exists',
        'Time, alarms, music and nighttime utility commands are useful conveniences',
    ]
    for phrase in forbidden:
        assert phrase not in html, f'old dream-only positioning leaked into {rel}: {phrase}'

print('Somnori Web v2.3 SEO/product alignment OK')
print('Validated SEO pages:', len(pages))
