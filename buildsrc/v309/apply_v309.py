from pathlib import Path
import shutil

repo = Path(__file__).resolve().parents[1]
app = repo / 'quiet-diary' / 'app'
main = app / 'src' / 'main'
java = main / 'java' / 'com' / 'quietdiary' / 'app'
assets = main / 'assets'
assets.mkdir(parents=True, exist_ok=True)

shutil.copy2(repo / 'v309' / 'ArinaVoicePack.java', java / 'ArinaVoicePack.java')
shutil.copy2(repo / 'v309' / 'arina_core_v1.zip', assets / 'arina_core_v1.zip')

build = app / 'build.gradle.kts'
s = build.read_text(encoding='utf-8')
assert 'versionCode = 30060' in s
assert 'versionName = "0.30.6-voice-lab"' in s
s = s.replace('versionCode = 30060', 'versionCode = 30090', 1)
s = s.replace('versionName = "0.30.6-voice-lab"', 'versionName = "0.30.9-arina-bundled-core"', 1)
build.write_text(s, encoding='utf-8')

night = java / 'NightCaptureService.java'
s = night.read_text(encoding='utf-8')

old = '''    public void onCreate() {
        super.onCreate();
        createNotificationChannel();
        initializeVoiceClock();
    }'''
new = '''    public void onCreate() {
        super.onCreate();
        createNotificationChannel();
        ArinaVoicePack.ensureInstalled(this);
        initializeVoiceClock();
    }'''
assert old in s
s = s.replace(old, new, 1)

old = '        String spoken = formatCurrentTime();\n'
new = '''        Calendar spokenNow = Calendar.getInstance();
        int spokenHour = spokenNow.get(Calendar.HOUR_OF_DAY);
        int spokenMinute = spokenNow.get(Calendar.MINUTE);
        String spoken = SomnoriVoiceTools.compactTime(spokenHour, spokenMinute);
'''
assert old in s
s = s.replace(old, new, 1)

old = '''        pauseAudioInputForSpeech();
        boolean voiced = speakAndWait(spoken);
        if (!running.get()) return;'''
new = '''        pauseAudioInputForSpeech();
        SharedPreferences arinaPrefs = getSharedPreferences("settings", MODE_PRIVATE);
        int arinaVolume = arinaPrefs.getInt("sound_volume", 45);
        boolean voiced = ArinaVoicePack.playTime(this, spokenHour, spokenMinute, arinaVolume);
        if (!voiced) voiced = speakAndWait(spoken);
        if (!running.get()) return;'''
assert old in s
s = s.replace(old, new, 1)

old = '''            playSignal(Signal.SAVED);
            notifyEntriesChanged();
            DiagnosticsStore.record(this, DiagnosticsStore.SAVED,
                    reason, System.currentTimeMillis() - entryId, MODE_SAVING);
            updateNotification("Сохранено · дождитесь тройной вибрации готовности");'''
new = '''            playSignal(Signal.SAVED);
            playArinaAfterSignal("сон".equals(savedCategory)
                    ? ArinaVoicePack.PHRASE_SAVED_DREAM
                    : ArinaVoicePack.PHRASE_SAVED_THOUGHT);
            notifyEntriesChanged();
            DiagnosticsStore.record(this, DiagnosticsStore.SAVED,
                    reason, System.currentTimeMillis() - entryId, MODE_SAVING);
            updateNotification("Сохранено · дождитесь тройной вибрации готовности");'''
assert old in s
s = s.replace(old, new, 1)

old = '''        vibratePattern(new long[]{0, 220});
        playSignal(Signal.CANCELLED);
        DiagnosticsStore.record(this, DiagnosticsStore.CANCELLED,'''
new = '''        vibratePattern(new long[]{0, 220});
        playSignal(Signal.CANCELLED);
        playArinaAfterSignal(ArinaVoicePack.PHRASE_CANCELLED);
        DiagnosticsStore.record(this, DiagnosticsStore.CANCELLED,'''
assert old in s
s = s.replace(old, new, 1)

old = '''        DiagnosticsStore.record(this, DiagnosticsStore.SERVICE_STOP,
                "голосовая команда ночь стоп", duration, mode);
        statusText = "Ночной режим выключен голосовой командой";
        finalizeNightSession();'''
new = '''        DiagnosticsStore.record(this, DiagnosticsStore.SERVICE_STOP,
                "голосовая команда ночь стоп", duration, mode);
        statusText = "Ночной режим выключен голосовой командой";
        pauseAudioInputForSpeech();
        ArinaVoicePack.playPhraseIfEnabled(this, ArinaVoicePack.PHRASE_SLEEP_WELL);
        finalizeNightSession();'''
assert old in s
s = s.replace(old, new, 1)

needle = '    private void stopCommandRecognizer() {\n'
addition = '''    private void playArinaAfterSignal(String phrase) {
        SharedPreferences prefs = getSharedPreferences("settings", MODE_PRIVATE);
        if (!prefs.getBoolean("sound_enabled", true)) return;
        try { Thread.sleep(280L); }
        catch (InterruptedException e) { Thread.currentThread().interrupt(); return; }
        ArinaVoicePack.playPhraseIfEnabled(this, phrase);
    }

'''
assert needle in s
s = s.replace(needle, addition + needle, 1)
night.write_text(s, encoding='utf-8')

voice = java / 'VoiceLabActivity.java'
s = voice.read_text(encoding='utf-8')
needle = '        renderSavedStatus();\n\n        rateSeek.setOnSeekBarChangeListener'
assert needle in s
s = s.replace(needle,
              '        ArinaVoicePack.ensureInstalled(this);\n        renderSavedStatus();\n\n        rateSeek.setOnSeekBarChangeListener', 1)
needle = '        findViewById(R.id.voiceLabTimeButton).setOnClickListener(v -> speak(currentTimePhrase()));\n'
assert needle in s
s = s.replace(needle,
              '        findViewById(R.id.voiceLabTimeButton).setOnClickListener(v -> previewArinaCurrentTime());\n', 1)

insert_before = '    private void initTts() {\n'
addition = '''    private void previewArinaCurrentTime() {
        Calendar now = Calendar.getInstance();
        int hour = now.get(Calendar.HOUR_OF_DAY);
        int minute = now.get(Calendar.MINUTE);
        int volume = getSharedPreferences("settings", MODE_PRIVATE).getInt("sound_volume", 45);
        new Thread(() -> {
            boolean ok = ArinaVoicePack.playTime(getApplicationContext(), hour, minute, volume);
            if (!ok) runOnUiThread(() -> speak(SomnoriVoiceTools.compactTime(hour, minute)));
        }, "arina-time-preview").start();
    }

'''
assert insert_before in s
s = s.replace(insert_before, addition + insert_before, 1)

old = '''        if (SomnoriTtsProfile.hasSavedVoice(this)) {
            savedStatus.setText("Сейчас выбрано для Somnori: " + SomnoriTtsProfile.savedVoiceName(this)
                    + String.format(Locale.US, " · %.2f / %.2f", SomnoriTtsProfile.savedRate(this), SomnoriTtsProfile.savedPitch(this)));
        } else {
            savedStatus.setText("Сейчас: автоматический выбор лучшего установленного офлайн-голоса · 0.82 / 0.97");
        }'''
new = '''        String fallback = SomnoriTtsProfile.hasSavedVoice(this)
                ? SomnoriTtsProfile.savedVoiceName(this)
                : "автоматический офлайн-голос Android";
        savedStatus.setText("Основной голос Somnori: Arina · встроена · офлайн · "
                + ArinaVoicePack.componentCount(this) + " компонентов. Резерв: " + fallback);'''
assert old in s
s = s.replace(old, new, 1)
s = s.replace('Голос сохранён. Он будет использоваться временем и будильником.',
              'Резервный системный голос сохранён для пока неозвученных Arina фраз.', 1)
voice.write_text(s, encoding='utf-8')

print('Applied Somnori 0.30.9 bundled Arina core')
