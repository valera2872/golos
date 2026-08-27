from pathlib import Path

repo = Path(__file__).resolve().parents[1]
app = repo / 'quiet-diary' / 'app'
java = app / 'src' / 'main' / 'java' / 'com' / 'quietdiary' / 'app'

build = app / 'build.gradle.kts'
s = build.read_text(encoding='utf-8')
assert 'versionCode = 30160' in s
assert 'versionName = "0.31.6-night-practice"' in s
s = s.replace('versionCode = 30160', 'versionCode = 30170', 1)
s = s.replace('versionName = "0.31.6-night-practice"', 'versionName = "0.31.7-arina-gapless"', 1)
build.write_text(s, encoding='utf-8')

voice = java / 'ArinaVoicePack.java'
s = voice.read_text(encoding='utf-8')

old = '''    public static boolean playTime(Context context, int hour, int minute, int volumePercent) {
        if (!ensureInstalled(context) || !validClock(hour, minute)) return false;
        if (!playFile(context, String.format(Locale.US, "hours/hour_%02d.mp3", hour), 100)) return false;
        return minute == 0 || playMinuteAfterGap(context, minute, 100);
    }

    public static boolean playAlarmTime(Context context, int hour, int minute, int volumePercent) {
        if (!ensureInstalled(context) || !validClock(hour, minute)) return false;
        if (!playFile(context, String.format(Locale.US, "alarm_hours/alarm_hour_%02d.mp3", hour), 100)) return false;
        return minute == 0 || playMinuteAfterGap(context, minute, 100);
    }'''
new = '''    public static boolean playTime(Context context, int hour, int minute, int volumePercent) {
        if (!ensureInstalled(context) || !validClock(hour, minute)) return false;
        String hourPath = String.format(Locale.US, "hours/hour_%02d.mp3", hour);
        if (minute == 0) return playFile(context, hourPath, 100);
        String minutePath = String.format(Locale.US, "minutes/minute_%02d.mp3", minute);
        return playGaplessPair(context, hourPath, minutePath, 100);
    }

    public static boolean playAlarmTime(Context context, int hour, int minute, int volumePercent) {
        if (!ensureInstalled(context) || !validClock(hour, minute)) return false;
        String hourPath = String.format(Locale.US, "alarm_hours/alarm_hour_%02d.mp3", hour);
        if (minute == 0) return playFile(context, hourPath, 100);
        String minutePath = String.format(Locale.US, "minutes/minute_%02d.mp3", minute);
        return playGaplessPair(context, hourPath, minutePath, 100);
    }'''
assert old in s
s = s.replace(old, new, 1)

old = '''    private static boolean playMinuteAfterGap(Context context, int minute, int volumePercent) {
        // v4 audio trims the excess blank-line silence from both sides of the join,
        // so an extra artificial delay is no longer needed.
        return playFile(context, String.format(Locale.US, "minutes/minute_%02d.mp3", minute), volumePercent);
    }'''
new = '''    /**
     * Plays the two locally bundled Arina fragments as one prepared MediaPlayer chain.
     *
     * Older builds waited for the first MediaPlayer to complete, released it and only
     * then prepared the minute player. Even after the recorded edge silence was trimmed,
     * that lifecycle added an audible digital seam between the hour and minute. Android's
     * setNextMediaPlayer() prepares both clips up front and hands the decoder directly to
     * the second player, so the human recording keeps its intended cadence offline.
     */
    private static boolean playGaplessPair(Context context, String firstPath,
                                           String secondPath, int volumePercent) {
        File firstAudio = new File(directory(context), firstPath);
        File secondAudio = new File(directory(context), secondPath);
        if (!firstAudio.isFile() || !secondAudio.isFile()) return false;

        CountDownLatch done = new CountDownLatch(1);
        MediaPlayer first = new MediaPlayer();
        MediaPlayer second = new MediaPlayer();
        try {
            AudioAttributes attributes = new AudioAttributes.Builder()
                    .setUsage(AudioAttributes.USAGE_MEDIA)
                    .setContentType(AudioAttributes.CONTENT_TYPE_SPEECH)
                    .build();
            float volume = Math.max(0.08f, Math.min(1.0f, volumePercent / 100f));

            first.setAudioAttributes(attributes);
            second.setAudioAttributes(attributes);
            first.setDataSource(firstAudio.getAbsolutePath());
            second.setDataSource(secondAudio.getAbsolutePath());
            first.setVolume(volume, volume);
            second.setVolume(volume, volume);

            first.setOnErrorListener((mp, what, extra) -> {
                done.countDown();
                return true;
            });
            second.setOnCompletionListener(mp -> done.countDown());
            second.setOnErrorListener((mp, what, extra) -> {
                done.countDown();
                return true;
            });

            // Prepare both decoders before playback. This is the important difference
            // from the old sequential playFile() calls: there is no second prepare/start
            // operation in the audible path between the two spoken fragments.
            first.prepare();
            second.prepare();
            first.setNextMediaPlayer(second);
            first.start();
            return done.await(12L, TimeUnit.SECONDS);
        } catch (Exception e) {
            Log.w(TAG, "Unable to play gapless Arina pair " + firstPath + " + " + secondPath, e);
            return false;
        } finally {
            try { if (first.isPlaying()) first.stop(); } catch (Exception ignored) {}
            try { if (second.isPlaying()) second.stop(); } catch (Exception ignored) {}
            try { first.setNextMediaPlayer(null); } catch (Exception ignored) {}
            try { first.release(); } catch (Exception ignored) {}
            try { second.release(); } catch (Exception ignored) {}
        }
    }'''
assert old in s
s = s.replace(old, new, 1)

# Deliberately keep arina_core_v5.zip and its private install directory unchanged.
# A real Arina pack already installed on the phone therefore survives this update;
# 0.31.7 changes only playback continuity, not the commercial voice assets.
assert 'private static final String ASSET = "arina_core_v5.zip";' in s
assert 'private static final String DIR = "arina_voice_core_v5";' in s

voice.write_text(s, encoding='utf-8')
print('Applied Somnori 0.31.7 gapless local Arina voice polish')
