package com.quietdiary.app;

import android.content.Context;
import android.content.SharedPreferences;
import android.media.AudioAttributes;
import android.media.MediaPlayer;
import android.util.Log;

import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.File;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.util.Locale;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;
import java.util.zip.ZipEntry;
import java.util.zip.ZipInputStream;

/**
 * Bundled local Arina voice core.
 *
 * The user never installs a separate voice pack. The verified audio pack ships in
 * app assets and is unpacked once into private app storage. All covered night
 * phrases then work offline. Android TTS remains the fallback for phrases not yet
 * recorded with Arina.
 */
public final class ArinaVoicePack {
    private static final String TAG = "ArinaVoicePack";
    private static final String ASSET = "arina_core_v1.zip";
    private static final String DIR = "arina_voice_core_v1";
    private static final String MARKER = ".installed_v1";
    private static final int HOURS = 24;
    private static final int MINUTES = 59;
    private static final Object INSTALL_LOCK = new Object();

    public static final String PHRASE_SAVED_THOUGHT = "recording/record_06.mp3";
    public static final String PHRASE_SAVED_DREAM = "recording/record_07.mp3";
    public static final String PHRASE_CANCELLED = "recording/record_08.mp3";
    public static final String PHRASE_SLEEP_WELL = "night/night_09.mp3";

    private ArinaVoicePack() {}

    public static File directory(Context context) {
        return new File(context.getFilesDir(), DIR);
    }

    /** Ensures the embedded pack is ready. Safe to call repeatedly. */
    public static boolean ensureInstalled(Context context) {
        if (context == null) return false;
        if (hasCoreFiles(context)) return true;
        synchronized (INSTALL_LOCK) {
            if (hasCoreFiles(context)) return true;
            File dir = directory(context);
            deleteRecursive(dir);
            if (!dir.mkdirs() && !dir.isDirectory()) return false;
            try (InputStream raw = context.getAssets().open(ASSET);
                 ZipInputStream zis = new ZipInputStream(new BufferedInputStream(raw))) {
                ZipEntry entry;
                byte[] buffer = new byte[16 * 1024];
                while ((entry = zis.getNextEntry()) != null) {
                    if (entry.isDirectory()) continue;
                    String name = normalizedEntry(entry.getName());
                    if (!isAllowed(name)) continue;
                    File target = new File(dir, name);
                    File parent = target.getParentFile();
                    if (parent != null && !parent.mkdirs() && !parent.isDirectory()) {
                        throw new IllegalStateException("Cannot create voice directory");
                    }
                    String root = dir.getCanonicalPath() + File.separator;
                    if (!target.getCanonicalPath().startsWith(root)) {
                        throw new SecurityException("Invalid voice-pack path");
                    }
                    try (BufferedOutputStream out = new BufferedOutputStream(new FileOutputStream(target))) {
                        int n;
                        while ((n = zis.read(buffer)) > 0) out.write(buffer, 0, n);
                    }
                }
                File marker = new File(dir, MARKER);
                try (FileOutputStream out = new FileOutputStream(marker)) {
                    out.write("Somnori Arina core v1\n".getBytes(java.nio.charset.StandardCharsets.UTF_8));
                }
            } catch (Exception e) {
                Log.w(TAG, "Unable to unpack bundled Arina voice", e);
                deleteRecursive(dir);
                return false;
            }
            boolean valid = hasCoreFiles(context);
            if (!valid) deleteRecursive(dir);
            return valid;
        }
    }

    public static boolean isInstalled(Context context) {
        return hasCoreFiles(context);
    }

    public static int componentCount(Context context) {
        File dir = directory(context);
        return countMp3(dir);
    }

    public static boolean playTime(Context context, int hour, int minute, int volumePercent) {
        if (!ensureInstalled(context) || hour < 0 || hour > 23 || minute < 0 || minute > 59) return false;
        if (!playFile(context, String.format(Locale.US, "hours/hour_%02d.mp3", hour), volumePercent)) return false;
        if (minute == 0) return true;
        try { Thread.sleep(110L); }
        catch (InterruptedException e) { Thread.currentThread().interrupt(); return false; }
        return playFile(context, String.format(Locale.US, "minutes/minute_%02d.mp3", minute), volumePercent);
    }

    public static boolean playPhrase(Context context, String relativePath, int volumePercent) {
        return ensureInstalled(context) && isAllowed(relativePath)
                && playFile(context, relativePath, volumePercent);
    }

    public static boolean playPhraseIfEnabled(Context context, String relativePath) {
        if (context == null) return false;
        SharedPreferences prefs = context.getSharedPreferences("settings", Context.MODE_PRIVATE);
        if (!prefs.getBoolean("sound_enabled", true)) return false;
        int volume = prefs.getInt("sound_volume", 45);
        return playPhrase(context, relativePath, volume);
    }

    private static boolean hasCoreFiles(Context context) {
        File dir = directory(context);
        if (!new File(dir, MARKER).isFile()) return false;
        for (int h = 0; h < HOURS; h++) {
            if (!new File(dir, String.format(Locale.US, "hours/hour_%02d.mp3", h)).isFile()) return false;
        }
        for (int m = 1; m <= MINUTES; m++) {
            if (!new File(dir, String.format(Locale.US, "minutes/minute_%02d.mp3", m)).isFile()) return false;
        }
        return new File(dir, PHRASE_SAVED_THOUGHT).isFile()
                && new File(dir, PHRASE_SAVED_DREAM).isFile()
                && new File(dir, PHRASE_CANCELLED).isFile()
                && new File(dir, PHRASE_SLEEP_WELL).isFile();
    }

    private static boolean playFile(Context context, String relativePath, int volumePercent) {
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
    }

    private static String normalizedEntry(String name) {
        return name == null ? "" : name.replace('\\', '/').replaceAll("^/+", "");
    }

    private static boolean isAllowed(String name) {
        if (name == null) return false;
        return name.matches("hours/hour_[0-2][0-9]\\.mp3")
                || name.matches("minutes/minute_[0-5][0-9]\\.mp3")
                || name.matches("night/night_(0[1-9]|1[0-2])\\.mp3")
                || name.matches("recording/record_0[1-9]\\.mp3");
    }

    private static int countMp3(File file) {
        if (file == null || !file.exists()) return 0;
        if (file.isFile()) return file.getName().endsWith(".mp3") ? 1 : 0;
        int count = 0;
        File[] children = file.listFiles();
        if (children != null) for (File child : children) count += countMp3(child);
        return count;
    }

    private static void deleteRecursive(File file) {
        if (file == null || !file.exists()) return;
        if (file.isDirectory()) {
            File[] children = file.listFiles();
            if (children != null) for (File child : children) deleteRecursive(child);
        }
        try { file.delete(); } catch (Exception ignored) {}
    }
}
