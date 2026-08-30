from pathlib import Path

repo = Path(__file__).resolve().parents[1]
app = repo / 'quiet-diary' / 'app'
main = app / 'src' / 'main'
java = main / 'java' / 'com' / 'quietdiary' / 'app'

build = app / 'build.gradle.kts'
s = build.read_text(encoding='utf-8')
assert 'versionCode = 30110' in s
assert 'versionName = "0.31.1-arina-alarm-time"' in s
s = s.replace('versionCode = 30110', 'versionCode = 30120', 1)
s = s.replace('versionName = "0.31.1-arina-alarm-time"', 'versionName = "0.31.2-arina-volume"', 1)
build.write_text(s, encoding='utf-8')

voice = java / 'ArinaVoicePack.java'
s = voice.read_text(encoding='utf-8')

old = '''    public static boolean playTime(Context context, int hour, int minute, int volumePercent) {
        if (!ensureInstalled(context) || !validClock(hour, minute)) return false;
        if (!playFile(context, String.format(Locale.US, "hours/hour_%02d.mp3", hour), volumePercent)) return false;
        return minute == 0 || playMinuteAfterGap(context, minute, volumePercent);
    }

    public static boolean playAlarmTime(Context context, int hour, int minute, int volumePercent) {
        if (!ensureInstalled(context) || !validClock(hour, minute)) return false;
        if (!playFile(context, String.format(Locale.US, "alarm_hours/alarm_hour_%02d.mp3", hour), volumePercent)) return false;
        return minute == 0 || playMinuteAfterGap(context, minute, volumePercent);
    }'''
new = '''    public static boolean playTime(Context context, int hour, int minute, int volumePercent) {
        if (!ensureInstalled(context) || !validClock(hour, minute)) return false;
        if (!playFile(context, String.format(Locale.US, "hours/hour_%02d.mp3", hour), 100)) return false;
        return minute == 0 || playMinuteAfterGap(context, minute, 100);
    }

    public static boolean playAlarmTime(Context context, int hour, int minute, int volumePercent) {
        if (!ensureInstalled(context) || !validClock(hour, minute)) return false;
        if (!playFile(context, String.format(Locale.US, "alarm_hours/alarm_hour_%02d.mp3", hour), 100)) return false;
        return minute == 0 || playMinuteAfterGap(context, minute, 100);
    }'''
assert old in s
s = s.replace(old, new, 1)

old = '''    public static boolean playPhraseIfEnabled(Context context, String relativePath) {
        if (context == null) return false;
        SharedPreferences prefs = context.getSharedPreferences("settings", Context.MODE_PRIVATE);
        if (!prefs.getBoolean("sound_enabled", true)) return false;
        int volume = prefs.getInt("sound_volume", 45);
        return playPhrase(context, relativePath, volume);
    }'''
new = '''    public static boolean playPhraseIfEnabled(Context context, String relativePath) {
        if (context == null) return false;
        SharedPreferences prefs = context.getSharedPreferences("settings", Context.MODE_PRIVATE);
        if (!prefs.getBoolean("sound_enabled", true)) return false;
        return playPhrase(context, relativePath, 100);
    }

    public static boolean playAlarmPhrase(Context context, String relativePath, int volumePercent) {
        return ensureInstalled(context) && isAllowed(relativePath)
                && playFileWithUsage(context, relativePath, 100, AudioAttributes.USAGE_ALARM);
    }'''
assert old in s
s = s.replace(old, new, 1)

old = '''    private static boolean playFile(Context context, String relativePath, int volumePercent) {
        File audio = new File(directory(context), relativePath);
        if (!audio.isFile()) return false;
        CountDownLatch done = new CountDownLatch(1);
        MediaPlayer player = new MediaPlayer();
        try {
            player.setAudioAttributes(new AudioAttributes.Builder()
                    .setUsage(AudioAttributes.USAGE_ALARM)
                    .setContentType(AudioAttributes.CONTENT_TYPE_SPEECH)
                    .build());
            player.setDataSource(audio.getAbsolutePath());
            float volume = Math.max(0.08f, Math.min(1.0f, volumePercent / 100f));
            player.setVolume(volume, volume);
            player.setOnCompletionListener(mp -> done.countDown());
            player.setOnErrorListener((mp, what, extra) -> { done.countDown(); return true; });
            player.prepare();
            player.start();
            return done.await(12L, TimeUnit.SECONDS);
        } catch (Exception e) {
            Log.w(TAG, "Unable to play " + relativePath, e);
            return false;
        } finally {
            try { if (player.isPlaying()) player.stop(); } catch (Exception ignored) {}
            try { player.release(); } catch (Exception ignored) {}
        }
    }'''
new = '''    private static boolean playFile(Context context, String relativePath, int volumePercent) {
        return playFileWithUsage(context, relativePath, volumePercent, AudioAttributes.USAGE_MEDIA);
    }

    private static boolean playFileWithUsage(Context context, String relativePath,
                                             int volumePercent, int usage) {
        File audio = new File(directory(context), relativePath);
        if (!audio.isFile()) return false;
        CountDownLatch done = new CountDownLatch(1);
        MediaPlayer player = new MediaPlayer();
        try {
            player.setAudioAttributes(new AudioAttributes.Builder()
                    .setUsage(usage)
                    .setContentType(AudioAttributes.CONTENT_TYPE_SPEECH)
                    .build());
            player.setDataSource(audio.getAbsolutePath());
            float volume = Math.max(0.08f, Math.min(1.0f, volumePercent / 100f));
            player.setVolume(volume, volume);
            player.setOnCompletionListener(mp -> done.countDown());
            player.setOnErrorListener((mp, what, extra) -> { done.countDown(); return true; });
            player.prepare();
            player.start();
            return done.await(12L, TimeUnit.SECONDS);
        } catch (Exception e) {
            Log.w(TAG, "Unable to play " + relativePath, e);
            return false;
        } finally {
            try { if (player.isPlaying()) player.stop(); } catch (Exception ignored) {}
            try { player.release(); } catch (Exception ignored) {}
        }
    }'''
assert old in s
s = s.replace(old, new, 1)
voice.write_text(s, encoding='utf-8')

night = java / 'NightCaptureService.java'
s = night.read_text(encoding='utf-8')
old = '''        long next = getSharedPreferences(WakeAlarmScheduler.PREFS, MODE_PRIVATE)
                .getLong(WakeAlarmScheduler.KEY_NEXT_AT, 0L);
        String prompt = next > System.currentTimeMillis()
                ? "Будильник установлен на " + formatAlarmTime(next)
                    + ". Назовите новое время или скажите выключить будильник."
                : "Будильник не установлен. Назовите время, например восемь тридцать.";
        setMode(MODE_SPEAKING);
        updateNotification(prompt);
        pauseAudioInputForSpeech();
        speakAndWait(prompt);
        if (!running.get()) return;
        beginAlarmDialogListening();'''
new = '''        long next = getSharedPreferences(WakeAlarmScheduler.PREFS, MODE_PRIVATE)
                .getLong(WakeAlarmScheduler.KEY_NEXT_AT, 0L);
        boolean activeAlarm = next > System.currentTimeMillis();
        String prompt = activeAlarm
                ? "Будильник установлен на " + formatAlarmTime(next)
                    + ". Назовите новое время или скажите выключить будильник."
                : "У тебя нет активного будильника.";
        setMode(MODE_SPEAKING);
        updateNotification(prompt);
        pauseAudioInputForSpeech();
        boolean voiced;
        if (activeAlarm) {
            Calendar alarm = Calendar.getInstance();
            alarm.setTimeInMillis(next);
            voiced = ArinaVoicePack.playAlarmTime(this,
                    alarm.get(Calendar.HOUR_OF_DAY), alarm.get(Calendar.MINUTE), 100);
        } else {
            voiced = ArinaVoicePack.playPhraseIfEnabled(this, ArinaVoicePack.PHRASE_ALARM_NONE);
        }
        if (!voiced) speakAndWait(prompt);
        if (!running.get()) return;
        beginAlarmDialogListening();'''
assert old in s
s = s.replace(old, new, 1)
night.write_text(s, encoding='utf-8')

wake = java / 'WakeAlarmActivity.java'
s = wake.read_text(encoding='utf-8')
old = '            boolean ok = ArinaVoicePack.playPhrase(getApplicationContext(), relativePath, 82);\n'
new = '            boolean ok = ArinaVoicePack.playAlarmPhrase(getApplicationContext(), relativePath, 100);\n'
assert old in s
s = s.replace(old, new, 1)
old = '''        new Thread(() -> ArinaVoicePack.playPhrase(
                getApplicationContext(), ArinaVoicePack.PHRASE_ALARM_STOPPED, 72),
                "arina-alarm-stopped").start();'''
new = '''        new Thread(() -> ArinaVoicePack.playPhrase(
                getApplicationContext(), ArinaVoicePack.PHRASE_ALARM_STOPPED, 100),
                "arina-alarm-stopped").start();'''
assert old in s
s = s.replace(old, new, 1)
wake.write_text(s, encoding='utf-8')

print('Applied Somnori 0.31.2 Arina volume + alarm-entry TTS cleanup')
