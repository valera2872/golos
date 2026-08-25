from pathlib import Path

repo = Path(__file__).resolve().parents[1]
java = repo / 'quiet-diary' / 'app' / 'src' / 'main' / 'java' / 'com' / 'quietdiary' / 'app'
needles = (
    'speakAndWait', 'tts.speak', 'TextToSpeech', 'finishAlarmDialogByVoice',
    'updateNotification', 'не расслыш', 'Не расслыш', 'не понял', 'Не понял',
    'не удалось', 'Не удалось', 'Попроб', 'повтори', 'Повтори', 'время', 'будильник'
)
for p in sorted(java.glob('*.java')):
    lines = p.read_text(encoding='utf-8').splitlines()
    hits = []
    for i, line in enumerate(lines):
        if any(n in line for n in needles):
            lo, hi = max(0, i-2), min(len(lines), i+3)
            hits.append((i+1, '\n'.join(f'{j+1:04d}: {lines[j]}' for j in range(lo, hi))))
    if hits:
        print('\n===== ' + p.name + ' =====')
        seen = set()
        for _, block in hits:
            if block in seen: continue
            seen.add(block)
            print(block)
            print('---')
