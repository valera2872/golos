package com.quietdiary.app;

import android.content.Context;
import android.media.AudioAttributes;
import android.media.MediaPlayer;
import android.net.Uri;
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

/** Local installable Arina voice pack. No network is required after import. */
public final class ArinaVoicePack {
    private static final String TAG = "ArinaVoicePack";
    private static final String DIR = "arina_voice_v1";
    private static final int HOURS = 24;
    private static final int MINUTES = 59;

    private ArinaVoicePack() {}

    public static File directory(Context context) {
        return new File(context.getFilesDir(), DIR);
    }

    public static boolean isInstalled(Context context) {
        File dir = directory(context);
        if (!dir.isDirectory()) return false;
        for (int h = 0; h < HOURS; h++) {
            if (!new File(dir, String.format(Locale.US, "hour_%02d.mp3", h)).isFile()) return false;
        }
        for (int m = 1; m <= MINUTES; m++) {
            if (!new File(dir, String.format(Locale.US, "minute_%02d.mp3", m)).isFile()) return false;
        }
        return true;
    }

    public static int componentCount(Context context) {
        File[] files = directory(context).listFiles((dir, name) -> name.endsWith(".mp3"));
        return files == null ? 0 : files.length;
    }

    public static boolean install(Context context, Uri zipUri) {
        if (context == null || zipUri == null) return false;
        File dir = directory(context);
        deleteRecursive(dir);
        if (!dir.mkdirs() && !dir.isDirectory()) return false;
        int copied = 0;
        try (InputStream raw = context.getContentResolver().openInputStream(zipUri)) {
            if (raw == null) return false;
            try (ZipInputStream zis = new ZipInputStream(new BufferedInputStream(raw))) {
                ZipEntry entry;
                byte[] buffer = new byte[16 * 1024];
                while ((entry = zis.getNextEntry()) != null) {
                    if (entry.isDirectory()) continue;
                    String name = new File(entry.getName()).getName();
                    if (!name.matches("hour_[0-2][0-9]\\.mp3") && !name.matches("minute_[0-5][0-9]\\.mp3")) continue;
                    File target = new File(dir, name);
                    try (BufferedOutputStream out = new BufferedOutputStream(new FileOutputStream(target))) {
                        int n;
                        while ((n = zis.read(buffer)) > 0) out.write(buffer, 0, n);
                    }
                    copied++;
                }
            }
        } catch (Exception e) {
            Log.w(TAG, "Unable to import Arina pack", e);
            deleteRecursive(dir);
            return false;
        }
        boolean valid = copied >= HOURS + MINUTES && isInstalled(context);
        if (!valid) deleteRecursive(dir);
        return valid;
    }

    public static boolean playTime(Context context, int hour, int minute, int volumePercent) {
        if (!isInstalled(context) || hour < 0 || hour > 23 || minute < 0 || minute > 59) return false;
        if (!playFile(context, String.format(Locale.US, "hour_%02d.mp3", hour), volumePercent)) return false;
        if (minute == 0) return true;
        try { Thread.sleep(110L); }
        catch (InterruptedException e) { Thread.currentThread().interrupt(); return false; }
        return playFile(context, String.format(Locale.US, "minute_%02d.mp3", minute), volumePercent);
    }

    private static boolean playFile(Context context, String name, int volumePercent) {
        File audio = new File(directory(context), name);
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
            return done.await(10L, TimeUnit.SECONDS);
        } catch (Exception e) {
            Log.w(TAG, "Unable to play " + name, e);
            return false;
        } finally {
            try { if (player.isPlaying()) player.stop(); } catch (Exception ignored) {}
            try { player.release(); } catch (Exception ignored) {}
        }
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
