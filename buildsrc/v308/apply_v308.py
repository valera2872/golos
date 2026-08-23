from pathlib import Path
import shutil

repo = Path(__file__).resolve().parents[1]
app = repo / 'quiet-diary' / 'app'
main = app / 'src' / 'main'
java = main / 'java' / 'com' / 'quietdiary' / 'app'

shutil.copy2(repo / 'v308' / 'ArinaVoicePack.java', java / 'ArinaVoicePack.java')

build = app / 'build.gradle.kts'
s = build.read_text(encoding='utf-8')
assert 'versionCode = 30060' in s
assert 'versionName = "0.30.6-voice-lab"' in s
s = s.replace('versionCode = 30060', 'versionCode = 30080', 1)
s = s.replace('versionName = "0.30.6-voice-lab"', 'versionName = "0.30.8-arina-runtime"', 1)
build.write_text(s, encoding='utf-8')

night = java / 'NightCaptureService.java'
s = night.read_text(encoding='utf-8')
old = '        String spoken = formatCurrentTime();\n'
new = '''        Calendar spokenNow = Calendar.getInstance();\n        int spokenHour = spokenNow.get(Calendar.HOUR_OF_DAY);\n        int spokenMinute = spokenNow.get(Calendar.MINUTE);\n        String spoken = SomnoriVoiceTools.compactTime(spokenHour, spokenMinute);\n'''
assert old in s
s = s.replace(old, new, 1)
old = '''        pauseAudioInputForSpeech();\n        boolean voiced = speakAndWait(spoken);\n        if (!running.get()) return;'''
new = '''        pauseAudioInputForSpeech();\n        SharedPreferences arinaPrefs = getSharedPreferences("settings", MODE_PRIVATE);\n        int arinaVolume = arinaPrefs.getInt("sound_volume", 45);\n        boolean voiced = ArinaVoicePack.playTime(this, spokenHour, spokenMinute, arinaVolume);\n        if (!voiced) voiced = speakAndWait(spoken);\n        if (!running.get()) return;'''
assert old in s
s = s.replace(old, new, 1)
night.write_text(s, encoding='utf-8')

voice = java / 'VoiceLabActivity.java'
s = voice.read_text(encoding='utf-8')
s = s.replace('import android.widget.Toast;\n', 'import android.widget.Toast;\n\nimport androidx.activity.result.ActivityResultLauncher;\nimport androidx.activity.result.contract.ActivityResultContracts;\n', 1)
s = s.replace('    private MaterialButton applyButton;\n', '''    private MaterialButton applyButton;\n    private TextView arinaStatus;\n\n    private final ActivityResultLauncher<String[]> arinaPackPicker = registerForActivityResult(\n            new ActivityResultContracts.OpenDocument(), uri -> {\n                if (uri == null) return;\n                arinaStatus.setText("Устанавливаю пакет Arina…");\n                new Thread(() -> {\n                    boolean ok = ArinaVoicePack.install(getApplicationContext(), uri);\n                    runOnUiThread(() -> {\n                        renderArinaStatus();\n                        Toast.makeText(this, ok\n                                ? "Arina установлена. Голосовые часы теперь работают офлайн."\n                                : "Не удалось установить пакет. Нужен Somnori Arina TIME PACK.",\n                                Toast.LENGTH_LONG).show();\n                    });\n                }, "arina-pack-import").start();\n            });\n''', 1)
s = s.replace('        applyButton = findViewById(R.id.voiceLabApplyButton);\n', '''        applyButton = findViewById(R.id.voiceLabApplyButton);\n        arinaStatus = findViewById(R.id.voiceLabArinaStatus);\n''', 1)
s = s.replace('        renderSavedStatus();\n\n        rateSeek.setOnSeekBarChangeListener', '        renderSavedStatus();\n        renderArinaStatus();\n\n        rateSeek.setOnSeekBarChangeListener', 1)
s = s.replace('        findViewById(R.id.voiceLabTimeButton).setOnClickListener(v -> speak(currentTimePhrase()));\n', '''        findViewById(R.id.voiceLabTimeButton).setOnClickListener(v -> previewCurrentTime());\n        findViewById(R.id.voiceLabImportArinaButton).setOnClickListener(v ->\n                arinaPackPicker.launch(new String[]{"application/zip", "application/octet-stream"}));\n''', 1)
insert_before = '    private void initTts() {\n'
addition = '''    private void previewCurrentTime() {\n        Calendar now = Calendar.getInstance();\n        int hour = now.get(Calendar.HOUR_OF_DAY);\n        int minute = now.get(Calendar.MINUTE);\n        if (!ArinaVoicePack.isInstalled(this)) {\n            speak(SomnoriVoiceTools.compactTime(hour, minute));\n            return;\n        }\n        int volume = getSharedPreferences("settings", MODE_PRIVATE).getInt("sound_volume", 45);\n        new Thread(() -> {\n            boolean ok = ArinaVoicePack.playTime(getApplicationContext(), hour, minute, volume);\n            if (!ok) runOnUiThread(() -> speak(SomnoriVoiceTools.compactTime(hour, minute)));\n        }, "arina-time-preview").start();\n    }\n\n    private void renderArinaStatus() {\n        if (arinaStatus == null) return;\n        if (ArinaVoicePack.isInstalled(this)) {\n            arinaStatus.setText("Arina · установлена · 83 компонента · голосовые часы офлайн");\n        } else {\n            arinaStatus.setText("Arina ещё не установлена. Выберите Somnori-Arina-TIME-PACK-v1.zip.");\n        }\n    }\n\n'''
assert insert_before in s
s = s.replace(insert_before, addition + insert_before, 1)
voice.write_text(s, encoding='utf-8')

layout = main / 'res' / 'layout' / 'activity_voice_lab.xml'
s = layout.read_text(encoding='utf-8')
needle = '''            <TextView\n                android:id="@+id/voiceLabSavedStatus"'''
assert needle in s
block = '''            <TextView\n                android:id="@+id/voiceLabArinaStatus"\n                android:layout_width="match_parent"\n                android:layout_height="wrap_content"\n                android:layout_marginTop="11dp"\n                android:lineSpacingExtra="2dp"\n                android:text="Arina ещё не установлена"\n                android:textColor="@color/qd_text"\n                android:textSize="14sp"\n                android:textStyle="bold" />\n\n            <com.google.android.material.button.MaterialButton\n                android:id="@+id/voiceLabImportArinaButton"\n                android:layout_width="match_parent"\n                android:layout_height="wrap_content"\n                android:layout_marginTop="9dp"\n                android:minHeight="52dp"\n                android:text="Установить пакет Arina (.zip)"\n                android:textAllCaps="false"\n                android:textColor="@color/qd_primary_dark"\n                android:textStyle="bold"\n                app:backgroundTint="@color/qd_primary"\n                app:cornerRadius="18dp" />\n\n'''
s = s.replace(needle, block + needle, 1)
layout.write_text(s, encoding='utf-8')

print('Applied Somnori 0.30.8 Arina runtime voice-pack integration')
