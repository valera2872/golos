package com.quietdiary.app;

import android.content.Context;
import android.media.AudioAttributes;
import android.media.MediaPlayer;
import android.os.SystemClock;
import android.util.Log;

import java.io.File;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.util.Locale;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;
import java.util.zip.ZipEntry;
import java.util.zip.ZipInputStream;

/** Offline playback of the pre-generated ElevenLabs Arina time pack. */
public final class SomnoriArinaVoice {
    private static final String TAG = "SomnoriArinaVoice";
    private static final String ASSET = "arina_time_pack.zip";
    private static final String PACK_VERSION = "arina-time-v1";
    private static final Object LOCK = new Object();

    private SomnoriArinaVoice() {}

    public static boolean playTimeAndWait(Context context, int hour, int minute, float volume) {
        if (context == null || hour < 0 || hour > 23 || minute < 0 || minute > 59) return false;
        File root = ensureExtracted(context.getApplicationContext());
        if (root == null) return false;
        File hourFile = new File(root, String.format(Locale.US, "hours/hour_%02d.ogg", hour));
        if (!playFileAndWait(hourFile, volume)) return false;
        if (minute == 0) return true;
        SystemClock.sleep(110L);
        File minuteFile = new File(root, String.format(Locale.US, "minutes/minute_%02d.ogg", minute));
        return playFileAndWait(minuteFile, volume);
    }

    private static File ensureExtracted(Context context) {
        File root = new File(context.getFilesDir(), PACK_VERSION);
        File ready = new File(root, ".ready");
        if (ready.isFile()) return root;
        synchronized (LOCK) {
            if (ready.isFile()) return root;
            deleteRecursively(root);
            if (!root.mkdirs() && !root.isDirectory()) return null;
            try (InputStream raw = context.getAssets().open(ASSET);
                 ZipInputStream zip = new ZipInputStream(raw)) {
                ZipEntry entry;
                byte[] buffer = new byte[16 * 1024];
                String canonicalRoot = root.getCanonicalPath() + File.separator;
                while ((entry = zip.getNextEntry()) != null) {
                    if (entry.isDirectory()) continue;
                    File out = new File(root, entry.getName());
                    String canonicalOut = out.getCanonicalPath();
                    if (!canonicalOut.startsWith(canonicalRoot)) throw new SecurityException("Bad voice-pack path");
                    File parent = out.getParentFile();
                    if (parent != null && !parent.exists() && !parent.mkdirs()) throw new IllegalStateException("Cannot create voice directory");
                    try (FileOutputStream fos = new FileOutputStream(out)) {
                        int n;
                        while ((n = zip.read(buffer)) > 0) fos.write(buffer, 0, n);
                    }
                }
                if (!new File(root, "hours/hour_00.ogg").isFile()
                        || !new File(root, "hours/hour_23.ogg").isFile()
                        || !new File(root, "minutes/minute_01.ogg").isFile()
                        || !new File(root, "minutes/minute_59.ogg").isFile()) {
                    throw new IllegalStateException("Incomplete Arina time pack");
                }
                try (FileOutputStream marker = new FileOutputStream(ready)) {
                    marker.write('1');
                }
                return root;
            } catch (Exception error) {
                Log.w(TAG, "Unable to unpack Arina voice", error);
                deleteRecursively(root);
                return null;
            }
        }
    }

    private static boolean playFileAndWait(File file, float requestedVolume) {
        if (file == null || !file.isFile()) return false;
        float volume = Math.max(0.08f, Math.min(1.0f, requestedVolume));
        CountDownLatch completed = new CountDownLatch(1);
        MediaPlayer player = new MediaPlayer();
        try {
            player.setAudioAttributes(new AudioAttributes.Builder()
                    .setUsage(AudioAttributes.USAGE_ALARM)
                    .setContentType(AudioAttributes.CONTENT_TYPE_SPEECH)
                    .build());
            player.setDataSource(file.getAbsolutePath());
            player.setVolume(volume, volume);
            player.setOnCompletionListener(mp -> completed.countDown());
            player.setOnErrorListener((mp, what, extra) -> { completed.countDown(); return true; });
            player.prepare();
            player.start();
            return completed.await(8L, TimeUnit.SECONDS);
        } catch (Exception error) {
            Log.w(TAG, "Arina playback failed: " + file.getName(), error);
            return false;
        } finally {
            try { player.stop(); } catch (Exception ignored) {}
            try { player.release(); } catch (Exception ignored) {}
        }
    }

    private static void deleteRecursively(File file) {
        if (file == null || !file.exists()) return;
        File[] children = file.listFiles();
        if (children != null) for (File child : children) deleteRecursively(child);
        try { file.delete(); } catch (Exception ignored) {}
    }
}
