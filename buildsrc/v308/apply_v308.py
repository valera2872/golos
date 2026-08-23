from pathlib import Path
import shutil

root = Path('buildsrc/quiet-diary')
java = root / 'app/src/main/java/com/quietdiary/app'
assets = root / 'app/src/main/assets'
assets.mkdir(parents=True, exist_ok=True)

shutil.copyfile(Path('buildsrc/v308/SomnoriArinaVoice.java'), java / 'SomnoriArinaVoice.java')

p = java / 'NightCaptureService.java'
s = p.read_text(encoding='utf-8')
old = '''        String spoken = formatCurrentTime();\n'''
new = '''        Calendar arinaNow = Calendar.getInstance();\n        int arinaHour = arinaNow.get(Calendar.HOUR_OF_DAY);\n        int arinaMinute = arinaNow.get(Calendar.MINUTE);\n        String spoken = SomnoriVoiceTools.compactTime(arinaHour, arinaMinute);\n'''
assert old in s
s = s.replace(old, new, 1)

old = '''        pauseAudioInputForSpeech();\n        boolean voiced = speakAndWait(spoken);\n'''
new = '''        pauseAudioInputForSpeech();\n        boolean voiced = SomnoriArinaVoice.playTimeAndWait(\n                getApplicationContext(), arinaHour, arinaMinute, nightVoiceVolume());\n        if (!voiced) voiced = speakAndWait(spoken);\n'''
assert old in s
s = s.replace(old, new, 1)

old = '''        SharedPreferences prefs = getSharedPreferences("settings", MODE_PRIVATE);\n        float volume = Math.max(0.08f, Math.min(1.0f, prefs.getInt("sound_volume", 45) / 100f));\n        Bundle parameters = new Bundle();\n'''
new = '''        float volume = nightVoiceVolume();\n        Bundle parameters = new Bundle();\n'''
assert old in s
s = s.replace(old, new, 1)

marker = '''    private String formatCurrentTime() {\n'''
helper = '''    private float nightVoiceVolume() {\n        SharedPreferences prefs = getSharedPreferences("settings", MODE_PRIVATE);\n        return Math.max(0.08f, Math.min(1.0f, prefs.getInt("sound_volume", 45) / 100f));\n    }\n\n'''
assert marker in s and 'private float nightVoiceVolume()' not in s
s = s.replace(marker, helper + marker, 1)
p.write_text(s, encoding='utf-8')

p = root / 'app/build.gradle.kts'
s = p.read_text(encoding='utf-8')
assert 'versionCode = 30050' in s and 'versionName = "0.30.5"' in s
s = s.replace('versionCode = 30050', 'versionCode = 30080', 1)
s = s.replace('versionName = "0.30.5"', 'versionName = "0.30.8-arina-live"', 1)
p.write_text(s, encoding='utf-8')

print('Somnori 0.30.8 Arina Live patch applied')
