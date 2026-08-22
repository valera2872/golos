from pathlib import Path
import base64
import gzip

ROOT = Path("buildsrc/quiet-diary")
PAYLOADS = Path("buildsrc/v303/layouts")

for name in [
    "activity_self_suggestion.xml",
    "activity_wake_settings.xml",
    "activity_wake_alarm.xml",
]:
    payload = (PAYLOADS / f"{name}.gz.b64").read_text(encoding="utf-8").strip()
    data = gzip.decompress(base64.b64decode(payload))
    target = ROOT / "app/src/main/res/layout" / name
    target.write_bytes(data)

gradle = ROOT / "app/build.gradle.kts"
text = gradle.read_text(encoding="utf-8")
old = '        versionCode = 30021\n        versionName = "0.30.2.1"\n'
new = '        versionCode = 30030\n        versionName = "0.30.3"\n'
if old not in text:
    raise SystemExit("0.30.2.1 version block not found")
gradle.write_text(text.replace(old, new, 1), encoding="utf-8")

print("Somnori 0.30.3 Premium Pass B applied")
