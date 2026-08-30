from pathlib import Path
import shutil

repo = Path(__file__).resolve().parents[1]
app = repo / 'quiet-diary' / 'app'
main = app / 'src' / 'main'
java = main / 'java' / 'com' / 'quietdiary' / 'app'
assets = main / 'assets'
assets.mkdir(parents=True, exist_ok=True)

# Runtime audio itself is not stored in public GitHub. CI creates a placeholder with the same shape.
shutil.copy2(repo / 'v313' / 'arina_core_v4.zip', assets / 'arina_core_v4.zip')
old_asset = assets / 'arina_core_v3.zip'
if old_asset.exists():
    old_asset.unlink()

build = app / 'build.gradle.kts'
s = build.read_text(encoding='utf-8')
assert 'versionCode = 30120' in s
assert 'versionName = "0.31.2-arina-volume"' in s
s = s.replace('versionCode = 30120', 'versionCode = 30130', 1)
s = s.replace('versionName = "0.31.2-arina-volume"', 'versionName = "0.31.3-arina-flow-polish"', 1)
build.write_text(s, encoding='utf-8')

voice = java / 'ArinaVoicePack.java'
s = voice.read_text(encoding='utf-8')
s = s.replace('private static final String ASSET = "arina_core_v3.zip";', 'private static final String ASSET = "arina_core_v4.zip";', 1)
s = s.replace('private static final String DIR = "arina_voice_core_v3";', 'private static final String DIR = "arina_voice_core_v4";', 1)
s = s.replace('private static final String MARKER = ".installed_v3";', 'private static final String MARKER = ".installed_v4";', 1)
s = s.replace('Somnori Arina core v3\\n', 'Somnori Arina core v4\\n', 1)
old = '''    private static boolean playMinuteAfterGap(Context context, int minute, int volumePercent) {
        try { Thread.sleep(110L); }
        catch (InterruptedException e) { Thread.currentThread().interrupt(); return false; }
        return playFile(context, String.format(Locale.US, "minutes/minute_%02d.mp3", minute), volumePercent);
    }'''
new = '''    private static boolean playMinuteAfterGap(Context context, int minute, int volumePercent) {
        // v4 audio trims the excess blank-line silence from both sides of the join,
        // so an extra artificial delay is no longer needed.
        return playFile(context, String.format(Locale.US, "minutes/minute_%02d.mp3", minute), volumePercent);
    }'''
assert old in s
s = s.replace(old, new, 1)
voice.write_text(s, encoding='utf-8')

wake = java / 'WakeAlarmActivity.java'
s = wake.read_text(encoding='utf-8')
old = '''        ((TextView) findViewById(R.id.wakeAlarmHint)).setText("Сделайте спокойный вдох. Выберите одно действительно важное действие на сегодня.");
        if (tts != null) tts.speak("Сделайте спокойный вдох. Сегодня не нужно решать всё сразу. Выберите одно действительно важное действие и начните с него.", TextToSpeech.QUEUE_FLUSH, null, "morning-setting");'''
new = '''        ((TextView) findViewById(R.id.wakeAlarmHint)).setText("Сегодня не нужно решать всё сразу. Выберите одно действительно важное действие и начните с него.");
        new Thread(() -> ArinaVoicePack.playPhrase(
                getApplicationContext(), ArinaVoicePack.PHRASE_GOOD_MORNING, 100),
                "arina-morning-setting").start();'''
assert old in s
s = s.replace(old, new, 1)
wake.write_text(s, encoding='utf-8')

print('Applied Somnori 0.31.3 Arina flow polish')
