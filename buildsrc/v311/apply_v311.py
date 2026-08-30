from pathlib import Path
import shutil

repo = Path(__file__).resolve().parents[1]
app = repo / 'quiet-diary' / 'app'
main = app / 'src' / 'main'
java = main / 'java' / 'com' / 'quietdiary' / 'app'
assets = main / 'assets'
assets.mkdir(parents=True, exist_ok=True)

shutil.copy2(repo / 'v311' / 'ArinaVoicePack.java', java / 'ArinaVoicePack.java')
shutil.copy2(repo / 'v311' / 'arina_core_v3.zip', assets / 'arina_core_v3.zip')
old_asset = assets / 'arina_core_v2.zip'
if old_asset.exists():
    old_asset.unlink()

build = app / 'build.gradle.kts'
s = build.read_text(encoding='utf-8')
assert 'versionCode = 30100' in s
assert 'versionName = "0.31.0-arina-alarm"' in s
s = s.replace('versionCode = 30100', 'versionCode = 30110', 1)
s = s.replace('versionName = "0.31.0-arina-alarm"', 'versionName = "0.31.1-arina-alarm-time"', 1)
build.write_text(s, encoding='utf-8')

night = java / 'NightCaptureService.java'
s = night.read_text(encoding='utf-8')

old = '''            if (next > System.currentTimeMillis()) {
                finishAlarmDialogByVoice(currentAlarmStatusSpeech());
            } else {
                finishAlarmDialogByArina(ArinaVoicePack.PHRASE_ALARM_NONE,
                        "У тебя нет активного будильника.");
            }'''
new = '''            if (next > System.currentTimeMillis()) {
                Calendar alarm = Calendar.getInstance();
                alarm.setTimeInMillis(next);
                int hour = alarm.get(Calendar.HOUR_OF_DAY);
                int minute = alarm.get(Calendar.MINUTE);
                finishAlarmDialogByArinaTime(hour, minute, currentAlarmStatusSpeech());
            } else {
                finishAlarmDialogByArina(ArinaVoicePack.PHRASE_ALARM_NONE,
                        "У тебя нет активного будильника.");
            }'''
assert old in s
s = s.replace(old, new, 1)

old = '''            boolean scheduled = WakeAlarmScheduler.scheduleVoiceTime(this, parsed.hour, parsed.minute);
            if (scheduled) {
                finishAlarmDialogByVoice("Будильник установлен на "
                        + spokenClock(parsed.hour, parsed.minute) + ".");
            } else {'''
new = '''            boolean scheduled = WakeAlarmScheduler.scheduleVoiceTime(this, parsed.hour, parsed.minute);
            if (scheduled) {
                finishAlarmDialogByArinaTime(parsed.hour, parsed.minute,
                        "Будильник установлен на " + spokenClock(parsed.hour, parsed.minute) + ".");
            } else {'''
assert old in s
s = s.replace(old, new, 1)

needle = '    private void finishAlarmDialogByArina(String phrasePath, String fallback) {\n'
addition = '''    private void finishAlarmDialogByArinaTime(int hour, int minute, String fallback) {
        alarmDialogListening = false;
        alarmDialogTranscribing = false;
        alarmDialogStartedAt = 0L;
        alarmDialogResult.set(null);
        alarmUtteranceCollector.reset();
        setMode(MODE_SPEAKING);
        updateNotification(fallback);
        pauseAudioInputForSpeech();
        SharedPreferences prefs = getSharedPreferences("settings", MODE_PRIVATE);
        int volume = prefs.getInt("sound_volume", 45);
        boolean voiced = ArinaVoicePack.playAlarmTime(this, hour, minute, volume);
        if (!voiced) speakAndWait(fallback);
        if (!running.get()) return;
        try {
            restartAudioInput();
            lastAudioReadAt = System.currentTimeMillis();
            consecutiveReadErrors = 0;
            enterWaitingMode(false);
        } catch (Exception e) {
            setMode(MODE_WAITING);
            requestRecovery("не удалось вернуться после голосового времени будильника: " + safeMessage(e));
        }
    }

'''
assert needle in s
s = s.replace(needle, addition + needle, 1)
night.write_text(s, encoding='utf-8')

print('Applied Somnori 0.31.1 Arina compositional alarm time')
