from pathlib import Path

repo = Path(__file__).resolve().parents[1]
p = repo / 'quiet-diary' / 'app' / 'src' / 'main' / 'java' / 'com' / 'quietdiary' / 'app' / 'NightCaptureService.java'
lines = p.read_text(encoding='utf-8').splitlines()

for start, end, title in [
    (1000, 1070, 'recording start'),
    (1120, 1320, 'alarm dialog'),
    (1510, 1605, 'save entry'),
    (1660, 1710, 'verification abort'),
]:
    print(f'\n===== {title} {start}-{end} =====')
    for n in range(start, min(end, len(lines)) + 1):
        print(f'{n:04d}: {lines[n-1]}')
