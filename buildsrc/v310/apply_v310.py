from pathlib import Path
import shutil

repo = Path(__file__).resolve().parents[1]
app = repo / 'quiet-diary' / 'app'
main = app / 'src' / 'main'
java = main / 'java' / 'com' / 'quietdiary' / 'app'
assets = main / 'assets'
assets.mkdir(parents=True, exist_ok=True)

shutil.copy2(repo / 'v310' / 'ArinaVoicePack.java', java / 'ArinaVoicePack.java')
shutil.copy2(repo / 'v310' / 'arina_core_v2.zip', assets / 'arina_core_v2.zip')
old_asset = assets / 'arina_core_v1.zip'
if old_asset.exists():
    old_asset.unlink()

build = app / 'build.gradle.kts'
s = build.read_text(encoding='utf-8')
assert 'versionCode = 30090' in s
assert 'versionName = "0.30.9-arina-bundled-core"' in s
s = s.replace('versionCode = 30090', 'versionCode = 30100', 1)
s = s.replace('versionName = "0.30.9-arina-bundled-core"', 'versionName = "0.31.0-arina-alarm"', 1)
build.write_text(s, encoding='utf-8')

wake = java / 'WakeAlarmActivity.java'
s = wake.read_text(encoding='utf-8')

old = '''    private boolean closed;
'''
new = '''    private boolean closed;
    private int alarmCycleNumber;
'''
assert old in s
s = s.replace(old, new, 1)

old = '''        prefs = getSharedPreferences(WakeAlarmScheduler.PREFS, MODE_PRIVATE);
        phrase = prefs.getString(WakeAlarmScheduler.KEY_PHRASE, WakeAlarmScheduler.DEFAULT_PHRASE);'''
new = '''        prefs = getSharedPreferences(WakeAlarmScheduler.PREFS, MODE_PRIVATE);
        ArinaVoicePack.ensureInstalled(this);
        phrase = prefs.getString(WakeAlarmScheduler.KEY_PHRASE, WakeAlarmScheduler.DEFAULT_PHRASE);'''
assert old in s
s = s.replace(old, new, 1)

old = '        findViewById(R.id.wakeAlarmAwakeButton).setOnClickListener(v -> openMain());\n'
new = '        findViewById(R.id.wakeAlarmAwakeButton).setOnClickListener(v -> confirmAwake());\n'
assert old in s
s = s.replace(old, new, 1)

old = '''    private void beginAlarmCycle() {
        if (closed) return;'''
new = '''    private void beginAlarmCycle() {
        if (closed) return;
        alarmCycleNumber++;'''
assert old in s
s = s.replace(old, new, 1)

old = '''        if (WakeAlarmScheduler.MESSAGE_AUDIO.equals(messageType)) playCustomAudio();
        else if (tts != null) tts.speak(phrase, TextToSpeech.QUEUE_FLUSH, null, "wake-phrase");'''
new = '''        if (WakeAlarmScheduler.MESSAGE_AUDIO.equals(messageType)) {
            playCustomAudio();
        } else if (WakeAlarmScheduler.DEFAULT_PHRASE.equals(phrase)) {
            String arina = alarmCycleNumber > 1
                    ? ArinaVoicePack.PHRASE_GET_UP
                    : ArinaVoicePack.PHRASE_WAKE_UP;
            String fallback = alarmCycleNumber > 1
                    ? "Пора вставать."
                    : "Доброе утро. Пора просыпаться.";
            playArinaWake(arina, fallback);
        } else if (tts != null) {
            tts.speak(phrase, TextToSpeech.QUEUE_FLUSH, null, "wake-phrase");
        }'''
assert old in s
s = s.replace(old, new, 1)

needle = '    private void playCustomAudio() {\n'
addition = '''    private void playArinaWake(String relativePath, String fallback) {
        new Thread(() -> {
            boolean ok = ArinaVoicePack.playPhrase(getApplicationContext(), relativePath, 82);
            if (!ok && !closed && tts != null) {
                runOnUiThread(() -> {
                    if (!closed && tts != null) {
                        tts.speak(fallback, TextToSpeech.QUEUE_FLUSH, null, "wake-arina-fallback");
                    }
                });
            }
        }, "arina-wake-message").start();
    }

    private void confirmAwake() {
        stopEverything();
        new Thread(() -> ArinaVoicePack.playPhrase(
                getApplicationContext(), ArinaVoicePack.PHRASE_ALARM_STOPPED, 72),
                "arina-alarm-stopped").start();
        openMain();
    }

'''
assert needle in s
s = s.replace(needle, addition + needle, 1)
wake.write_text(s, encoding='utf-8')

night = java / 'NightCaptureService.java'
s = night.read_text(encoding='utf-8')
old = '''        if (parsed.action == RussianAlarmCommandParser.Action.CANCEL) {
            WakeAlarmScheduler.cancelFromVoice(this);
            finishAlarmDialogByVoice("Будильник выключен.");
            return;
        }
        if (parsed.action == RussianAlarmCommandParser.Action.QUERY
                || parsed.action == RussianAlarmCommandParser.Action.KEEP) {
            finishAlarmDialogByVoice(currentAlarmStatusSpeech());
            return;
        }'''
new = '''        if (parsed.action == RussianAlarmCommandParser.Action.CANCEL) {
            WakeAlarmScheduler.cancelFromVoice(this);
            finishAlarmDialogByArina(ArinaVoicePack.PHRASE_ALARM_OFF, "Будильник выключен.");
            return;
        }
        if (parsed.action == RussianAlarmCommandParser.Action.QUERY
                || parsed.action == RussianAlarmCommandParser.Action.KEEP) {
            long next = getSharedPreferences(WakeAlarmScheduler.PREFS, MODE_PRIVATE)
                    .getLong(WakeAlarmScheduler.KEY_NEXT_AT, 0L);
            if (next > System.currentTimeMillis()) {
                finishAlarmDialogByVoice(currentAlarmStatusSpeech());
            } else {
                finishAlarmDialogByArina(ArinaVoicePack.PHRASE_ALARM_NONE,
                        "У тебя нет активного будильника.");
            }
            return;
        }'''
assert old in s
s = s.replace(old, new, 1)

needle = '    private void finishAlarmDialogByVoice(String spoken) {\n'
addition = '''    private void finishAlarmDialogByArina(String phrasePath, String fallback) {
        alarmDialogListening = false;
        alarmDialogTranscribing = false;
        alarmDialogStartedAt = 0L;
        alarmDialogResult.set(null);
        alarmUtteranceCollector.reset();
        setMode(MODE_SPEAKING);
        updateNotification(fallback);
        pauseAudioInputForSpeech();
        boolean voiced = ArinaVoicePack.playPhraseIfEnabled(this, phrasePath);
        if (!voiced) speakAndWait(fallback);
        if (!running.get()) return;
        try {
            restartAudioInput();
            lastAudioReadAt = System.currentTimeMillis();
            consecutiveReadErrors = 0;
            enterWaitingMode(false);
        } catch (Exception e) {
            setMode(MODE_WAITING);
            requestRecovery("не удалось вернуться после голосового будильника: " + safeMessage(e));
        }
    }

'''
assert needle in s
s = s.replace(needle, addition + needle, 1)
night.write_text(s, encoding='utf-8')

print('Applied Somnori 0.31.0 Arina alarm integration')
