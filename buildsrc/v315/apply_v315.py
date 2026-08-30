from pathlib import Path
import shutil

repo = Path(__file__).resolve().parents[1]
app = repo / 'quiet-diary' / 'app'
raw = app / 'src' / 'main' / 'res' / 'raw'
raw.mkdir(parents=True, exist_ok=True)

music = repo / 'v315' / 'music'
tracks = {
    'music_sea_harp.mp3': 180,
    'music_calm_energy.mp3': 240,
    'music_quiet_meditation.mp3': 360,
    'nature_forest.mp3': 240,
}
for name in tracks:
    src = music / name
    assert src.is_file(), f'missing {src}'
    shutil.copy2(src, raw / name)

build = app / 'build.gradle.kts'
s = build.read_text(encoding='utf-8')
assert 'versionCode = 30140' in s
assert 'versionName = "0.31.4-arina-errors"' in s
s = s.replace('versionCode = 30140', 'versionCode = 30150', 1)
s = s.replace('versionName = "0.31.4-arina-errors"', 'versionName = "0.31.5-night-music"', 1)
build.write_text(s, encoding='utf-8')

print('Applied Somnori 0.31.5 full offline night music')
