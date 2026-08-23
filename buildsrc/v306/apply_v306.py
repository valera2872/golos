from pathlib import Path
import re
import shutil

root = Path('buildsrc/quiet-diary')
java = root / 'app/src/main/java/com/quietdiary/app'
layout = root / 'app/src/main/res/layout'
assets = Path('buildsrc/v306')

shutil.copyfile(assets / 'SomnoriTtsProfile.java', java / 'SomnoriTtsProfile.java')
shutil.copyfile(assets / 'VoiceLabActivity.java', java / 'VoiceLabActivity.java')
shutil.copyfile(assets / 'activity_voice_lab.xml', layout / 'activity_voice_lab.xml')

# Manifest: register the diagnostic screen.
p = root / 'app/src/main/AndroidManifest.xml'
s = p.read_text(encoding='utf-8')
marker = '        <activity android:name=".SettingsActivity" android:exported="false" />\n'
assert marker in s and 'android:name=".VoiceLabActivity"' not in s
s = s.replace(marker, marker + '        <activity android:name=".VoiceLabActivity" android:exported="false" />\n', 1)
p.write_text(s, encoding='utf-8')

# Settings: add one temporary entry point near diagnostics.
p = layout / 'activity_settings.xml'
s = p.read_text(encoding='utf-8')
marker = '''            <com.google.android.material.button.MaterialButton\n                android:id="@+id/openDiagnosticsButton"'''
assert marker in s and 'openVoiceLabButton' not in s
button = '''            <com.google.android.material.button.MaterialButton\n                android:id="@+id/openVoiceLabButton"\n                style="?attr/materialButtonOutlinedStyle"\n                android:layout_width="match_parent"\n                android:layout_height="wrap_content"\n                android:maxLines="3"\n                android:minHeight="52dp"\n                android:layout_marginTop="8dp"\n                android:text="Тест голоса Somnori"\n                android:textAllCaps="false"\n                android:textColor="@color/qd_text"\n                app:cornerRadius="17dp"  android:letterSpacing="0" />\n\n'''
s = s.replace(marker, button + marker, 1)
p.write_text(s, encoding='utf-8')

p = java / 'SettingsActivity.java'
s = p.read_text(encoding='utf-8')
marker = '''        findViewById(R.id.openDiagnosticsButton).setOnClickListener(v ->\n                startActivity(new Intent(this, DiagnosticsActivity.class)));\n'''
assert marker in s and 'openVoiceLabButton' not in s
insert = '''        findViewById(R.id.openVoiceLabButton).setOnClickListener(v ->\n                startActivity(new Intent(this, VoiceLabActivity.class)));\n'''
s = s.replace(marker, insert + marker, 1)
p.write_text(s, encoding='utf-8')

# Night clock: preserve all recognition/routing code; replace only the TTS profile chooser.
p = java / 'NightCaptureService.java'
s = p.read_text(encoding='utf-8')
pattern = re.compile(r'    /\*\* Chooses the best installed Russian voice without making night mode depend on network\. \*/\n    private int configureSomnoriVoice\(TextToSpeech active\) \{.*?\n    \}\n\n    private void startAlarmVoiceDialog\(\)', re.S)
replacement = '''    /** Chooses the saved Voice Lab profile, otherwise the best installed Russian offline voice. */\n    private int configureSomnoriVoice(TextToSpeech active) {\n        return SomnoriTtsProfile.configure(getApplicationContext(), active);\n    }\n\n    private void startAlarmVoiceDialog()'''
s2, count = pattern.subn(replacement, s, count=1)
assert count == 1
p.write_text(s2, encoding='utf-8')

# Wake screen previously used a separate generic ru-RU voice. Make it use the same profile.
p = java / 'WakeAlarmActivity.java'
s = p.read_text(encoding='utf-8')
old = '''    private void initTts() {\n        tts = new TextToSpeech(this, result -> {\n            if (result != TextToSpeech.SUCCESS) return;\n            tts.setLanguage(new Locale("ru", "RU"));\n            tts.setSpeechRate(0.86f);\n            tts.setPitch(1.02f);\n            tts.setAudioAttributes(new AudioAttributes.Builder().setUsage(AudioAttributes.USAGE_ALARM).setContentType(AudioAttributes.CONTENT_TYPE_SPEECH).build());\n        });\n    }\n'''
assert old in s
new = '''    private void initTts() {\n        tts = new TextToSpeech(this, result -> {\n            if (result != TextToSpeech.SUCCESS) return;\n            SomnoriTtsProfile.configure(this, tts);\n            tts.setAudioAttributes(new AudioAttributes.Builder().setUsage(AudioAttributes.USAGE_ALARM).setContentType(AudioAttributes.CONTENT_TYPE_SPEECH).build());\n        });\n    }\n'''
s = s.replace(old, new, 1)
p.write_text(s, encoding='utf-8')

# Diagnostic version; main/product branches remain untouched.
p = root / 'app/build.gradle.kts'
s = p.read_text(encoding='utf-8')
assert 'versionCode = 30050' in s and 'versionName = "0.30.5"' in s
s = s.replace('versionCode = 30050', 'versionCode = 30060', 1)
s = s.replace('versionName = "0.30.5"', 'versionName = "0.30.6-voice-lab"', 1)
p.write_text(s, encoding='utf-8')

print('Somnori 0.30.6 Voice Lab patch applied')
