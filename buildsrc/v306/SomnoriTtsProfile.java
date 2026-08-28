package com.quietdiary.app;

import android.content.Context;
import android.content.SharedPreferences;
import android.speech.tts.TextToSpeech;
import android.speech.tts.Voice;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Locale;
import java.util.Set;

/** Shared, offline-first voice profile for Somnori's night clock and wake alarm. */
public final class SomnoriTtsProfile {
    public static final float DEFAULT_RATE = 0.82f;
    public static final float DEFAULT_PITCH = 0.97f;

    private static final String PREFS = "somnori_tts_profile";
    private static final String KEY_VOICE = "voice_name";
    private static final String KEY_RATE = "speech_rate";
    private static final String KEY_PITCH = "speech_pitch";

    private SomnoriTtsProfile() {}

    public static int configure(Context context, TextToSpeech tts) {
        return configure(context, tts, DEFAULT_RATE, DEFAULT_PITCH);
    }

    public static int configure(Context context, TextToSpeech tts, float fallbackRate, float fallbackPitch) {
        int language = tts.setLanguage(new Locale("ru", "RU"));
        if (language == TextToSpeech.LANG_MISSING_DATA || language == TextToSpeech.LANG_NOT_SUPPORTED) {
            language = tts.setLanguage(Locale.getDefault());
        }

        SharedPreferences prefs = prefs(context);
        Voice chosen = null;
        String savedName = prefs.getString(KEY_VOICE, "");
        List<Voice> russian = russianVoices(tts);
        if (!savedName.isEmpty()) {
            for (Voice voice : russian) {
                if (savedName.equals(voice.getName()) && isInstalled(voice) && !voice.isNetworkConnectionRequired()) {
                    chosen = voice;
                    break;
                }
            }
        }
        if (chosen == null) {
            for (Voice voice : russian) {
                if (isInstalled(voice) && !voice.isNetworkConnectionRequired()) {
                    chosen = voice;
                    break;
                }
            }
        }
        if (chosen == null && !russian.isEmpty()) chosen = russian.get(0);
        if (chosen != null) {
            try { tts.setVoice(chosen); } catch (Exception ignored) { }
        }

        float rate = prefs.contains(KEY_RATE) ? prefs.getFloat(KEY_RATE, fallbackRate) : fallbackRate;
        float pitch = prefs.contains(KEY_PITCH) ? prefs.getFloat(KEY_PITCH, fallbackPitch) : fallbackPitch;
        tts.setSpeechRate(clamp(rate, 0.65f, 1.25f));
        tts.setPitch(clamp(pitch, 0.80f, 1.20f));
        return language;
    }

    public static List<Voice> russianVoices(TextToSpeech tts) {
        ArrayList<Voice> result = new ArrayList<>();
        try {
            Set<Voice> available = tts.getVoices();
            if (available != null) {
                for (Voice voice : available) {
                    if (voice == null || voice.getLocale() == null) continue;
                    if (!"ru".equalsIgnoreCase(voice.getLocale().getLanguage())) continue;
                    result.add(voice);
                }
            }
        } catch (Exception ignored) { }
        result.sort(Comparator
                .comparing((Voice v) -> !isInstalled(v))
                .thenComparing(Voice::isNetworkConnectionRequired)
                .thenComparing((Voice v) -> -v.getQuality())
                .thenComparingInt(Voice::getLatency)
                .thenComparing(Voice::getName));
        return result;
    }

    public static boolean isInstalled(Voice voice) {
        if (voice == null) return false;
        try {
            Set<String> features = voice.getFeatures();
            return features == null || !features.contains(TextToSpeech.Engine.KEY_FEATURE_NOT_INSTALLED);
        } catch (Exception ignored) {
            return true;
        }
    }

    public static String savedVoiceName(Context context) {
        return prefs(context).getString(KEY_VOICE, "");
    }

    public static float savedRate(Context context) {
        return prefs(context).getFloat(KEY_RATE, DEFAULT_RATE);
    }

    public static float savedPitch(Context context) {
        return prefs(context).getFloat(KEY_PITCH, DEFAULT_PITCH);
    }

    public static boolean hasSavedVoice(Context context) {
        return !savedVoiceName(context).isEmpty();
    }

    public static void save(Context context, Voice voice, float rate, float pitch) {
        if (voice == null || !isInstalled(voice) || voice.isNetworkConnectionRequired()) return;
        prefs(context).edit()
                .putString(KEY_VOICE, voice.getName())
                .putFloat(KEY_RATE, clamp(rate, 0.65f, 1.25f))
                .putFloat(KEY_PITCH, clamp(pitch, 0.80f, 1.20f))
                .apply();
    }

    public static void clear(Context context) {
        prefs(context).edit().clear().apply();
    }

    private static SharedPreferences prefs(Context context) {
        return context.getSharedPreferences(PREFS, Context.MODE_PRIVATE);
    }

    private static float clamp(float value, float min, float max) {
        return Math.max(min, Math.min(max, value));
    }
}
