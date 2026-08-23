package com.quietdiary.app;

import android.content.SharedPreferences;
import android.media.AudioAttributes;
import android.os.Bundle;
import android.speech.tts.TextToSpeech;
import android.speech.tts.Voice;
import android.widget.EditText;
import android.widget.SeekBar;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import com.google.android.material.button.MaterialButton;

import java.util.ArrayList;
import java.util.Calendar;
import java.util.List;
import java.util.Locale;

/** Temporary on-device lab for choosing a warmer free Android TTS voice. */
public final class VoiceLabActivity extends AppCompatActivity {
    private TextToSpeech tts;
    private final List<Voice> voices = new ArrayList<>();
    private int voiceIndex;
    private boolean ready;

    private TextView engineStatus;
    private TextView voiceName;
    private TextView voiceMeta;
    private TextView rateLabel;
    private TextView pitchLabel;
    private TextView savedStatus;
    private SeekBar rateSeek;
    private SeekBar pitchSeek;
    private EditText customText;
    private MaterialButton applyButton;

    @Override protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_voice_lab);

        engineStatus = findViewById(R.id.voiceLabEngineStatus);
        voiceName = findViewById(R.id.voiceLabVoiceName);
        voiceMeta = findViewById(R.id.voiceLabVoiceMeta);
        rateLabel = findViewById(R.id.voiceLabRateLabel);
        pitchLabel = findViewById(R.id.voiceLabPitchLabel);
        savedStatus = findViewById(R.id.voiceLabSavedStatus);
        rateSeek = findViewById(R.id.voiceLabRateSeek);
        pitchSeek = findViewById(R.id.voiceLabPitchSeek);
        customText = findViewById(R.id.voiceLabCustomText);
        applyButton = findViewById(R.id.voiceLabApplyButton);

        setRate(SomnoriTtsProfile.savedRate(this));
        setPitch(SomnoriTtsProfile.savedPitch(this));
        updateTuningLabels();
        renderSavedStatus();

        rateSeek.setOnSeekBarChangeListener(simpleSeekListener());
        pitchSeek.setOnSeekBarChangeListener(simpleSeekListener());

        findViewById(R.id.voiceLabPrevButton).setOnClickListener(v -> moveVoice(-1));
        findViewById(R.id.voiceLabNextButton).setOnClickListener(v -> moveVoice(1));
        findViewById(R.id.voiceLabTimeButton).setOnClickListener(v -> speak(currentTimePhrase()));
        findViewById(R.id.voiceLabAlarmConfirmButton).setOnClickListener(v -> speak("Хорошо. Будильник на семь тридцать."));
        findViewById(R.id.voiceLabWakeButton).setOnClickListener(v -> speak(currentWakePhrase()));
        findViewById(R.id.voiceLabMorningButton).setOnClickListener(v -> speak("Доброе утро. Не спешите. Сделайте спокойный вдох и начните день с одного простого шага."));
        findViewById(R.id.voiceLabCustomButton).setOnClickListener(v -> {
            String text = customText.getText() == null ? "" : customText.getText().toString().trim();
            if (text.isEmpty()) Toast.makeText(this, "Введите фразу для теста", Toast.LENGTH_SHORT).show();
            else speak(text);
        });
        applyButton.setOnClickListener(v -> saveSelectedVoice());
        findViewById(R.id.voiceLabResetButton).setOnClickListener(v -> resetAutomatic());
        findViewById(R.id.voiceLabBackButton).setOnClickListener(v -> finish());

        initTts();
    }

    private void initTts() {
        engineStatus.setText("Ищу голоса на этом телефоне…");
        tts = new TextToSpeech(getApplicationContext(), status -> runOnUiThread(() -> {
            if (status != TextToSpeech.SUCCESS || tts == null) {
                engineStatus.setText("Системный синтез речи не запустился.");
                return;
            }
            SomnoriTtsProfile.configure(this, tts);
            tts.setAudioAttributes(new AudioAttributes.Builder()
                    .setUsage(AudioAttributes.USAGE_ASSISTANCE_ACCESSIBILITY)
                    .setContentType(AudioAttributes.CONTENT_TYPE_SPEECH)
                    .build());
            voices.clear();
            voices.addAll(SomnoriTtsProfile.russianVoices(tts));
            ready = true;
            String activeName = tts.getVoice() == null ? "" : tts.getVoice().getName();
            String savedName = SomnoriTtsProfile.savedVoiceName(this);
            voiceIndex = findVoiceIndex(!savedName.isEmpty() ? savedName : activeName);
            engineStatus.setText("Движок: " + safe(tts.getDefaultEngine()) + " · русских голосов: " + voices.size());
            renderVoice();
        }));
    }

    private int findVoiceIndex(String name) {
        if (voices.isEmpty()) return 0;
        for (int i = 0; i < voices.size(); i++) if (voices.get(i).getName().equals(name)) return i;
        return 0;
    }

    private void moveVoice(int delta) {
        if (!ready || voices.isEmpty()) return;
        voiceIndex = (voiceIndex + delta + voices.size()) % voices.size();
        renderVoice();
        speak("Добрый вечер. Я Somnori.");
    }

    private void renderVoice() {
        if (voices.isEmpty()) {
            voiceName.setText("Русские голоса не найдены");
            voiceMeta.setText("Проверьте установленные голосовые данные Android.");
            applyButton.setEnabled(false);
            return;
        }
        Voice voice = voices.get(voiceIndex);
        voiceName.setText((voiceIndex + 1) + " из " + voices.size() + " · " + voice.getName());
        String availability = SomnoriTtsProfile.isInstalled(voice) ? "установлен" : "не загружен";
        String connection = voice.isNetworkConnectionRequired() ? "нужен интернет" : "офлайн";
        voiceMeta.setText(localeLabel(voice) + " · " + connection + " · " + availability
                + " · качество " + voice.getQuality() + " · задержка " + voice.getLatency());
        applyButton.setEnabled(SomnoriTtsProfile.isInstalled(voice) && !voice.isNetworkConnectionRequired());
        applyButton.setText(voice.isNetworkConnectionRequired()
                ? "Можно слушать · для будильника нужен офлайн-голос"
                : "Использовать этот голос в Somnori");
    }

    private void speak(String text) {
        if (!ready || tts == null) {
            Toast.makeText(this, "Голос ещё не готов", Toast.LENGTH_SHORT).show();
            return;
        }
        applyPreviewProfile();
        tts.speak(text, TextToSpeech.QUEUE_FLUSH, null, "voice-lab-" + System.nanoTime());
    }

    private void applyPreviewProfile() {
        if (!voices.isEmpty()) {
            try { tts.setVoice(voices.get(voiceIndex)); } catch (Exception ignored) { }
        }
        tts.setSpeechRate(currentRate());
        tts.setPitch(currentPitch());
    }

    private void saveSelectedVoice() {
        if (voices.isEmpty()) return;
        Voice voice = voices.get(voiceIndex);
        if (!SomnoriTtsProfile.isInstalled(voice)) {
            Toast.makeText(this, "Сначала загрузите этот голос в Android", Toast.LENGTH_LONG).show();
            return;
        }
        if (voice.isNetworkConnectionRequired()) {
            Toast.makeText(this, "Для ночного будильника сохраняем только офлайн-голоса", Toast.LENGTH_LONG).show();
            return;
        }
        SomnoriTtsProfile.save(this, voice, currentRate(), currentPitch());
        renderSavedStatus();
        Toast.makeText(this, "Голос сохранён. Он будет использоваться временем и будильником.", Toast.LENGTH_LONG).show();
    }

    private void resetAutomatic() {
        SomnoriTtsProfile.clear(this);
        setRate(SomnoriTtsProfile.DEFAULT_RATE);
        setPitch(SomnoriTtsProfile.DEFAULT_PITCH);
        updateTuningLabels();
        if (tts != null && ready) {
            SomnoriTtsProfile.configure(this, tts);
            String active = tts.getVoice() == null ? "" : tts.getVoice().getName();
            voiceIndex = findVoiceIndex(active);
            renderVoice();
        }
        renderSavedStatus();
        Toast.makeText(this, "Вернул автоматический выбор лучшего офлайн-голоса", Toast.LENGTH_SHORT).show();
    }

    private SeekBar.OnSeekBarChangeListener simpleSeekListener() {
        return new SeekBar.OnSeekBarChangeListener() {
            @Override public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) { updateTuningLabels(); }
            @Override public void onStartTrackingTouch(SeekBar seekBar) { }
            @Override public void onStopTrackingTouch(SeekBar seekBar) {
                if (ready) speak("Добрый вечер. Я Somnori.");
            }
        };
    }

    private float currentRate() { return 0.70f + rateSeek.getProgress() / 100f; }
    private float currentPitch() { return 0.85f + pitchSeek.getProgress() / 100f; }

    private void setRate(float rate) {
        rateSeek.setProgress(Math.round((Math.max(0.70f, Math.min(1.20f, rate)) - 0.70f) * 100f));
    }

    private void setPitch(float pitch) {
        pitchSeek.setProgress(Math.round((Math.max(0.85f, Math.min(1.15f, pitch)) - 0.85f) * 100f));
    }

    private void updateTuningLabels() {
        rateLabel.setText(String.format(Locale.US, "Скорость · %.2f", currentRate()));
        pitchLabel.setText(String.format(Locale.US, "Высота голоса · %.2f", currentPitch()));
    }

    private void renderSavedStatus() {
        if (SomnoriTtsProfile.hasSavedVoice(this)) {
            savedStatus.setText("Сейчас выбрано для Somnori: " + SomnoriTtsProfile.savedVoiceName(this)
                    + String.format(Locale.US, " · %.2f / %.2f", SomnoriTtsProfile.savedRate(this), SomnoriTtsProfile.savedPitch(this)));
        } else {
            savedStatus.setText("Сейчас: автоматический выбор лучшего установленного офлайн-голоса · 0.82 / 0.97");
        }
    }

    private String currentTimePhrase() {
        Calendar now = Calendar.getInstance();
        return SomnoriVoiceTools.compactTime(now.get(Calendar.HOUR_OF_DAY), now.get(Calendar.MINUTE));
    }

    private String currentWakePhrase() {
        SharedPreferences prefs = getSharedPreferences(WakeAlarmScheduler.PREFS, MODE_PRIVATE);
        return prefs.getString(WakeAlarmScheduler.KEY_PHRASE, WakeAlarmScheduler.DEFAULT_PHRASE);
    }

    private static String localeLabel(Voice voice) {
        Locale locale = voice.getLocale();
        String tag = locale == null ? "" : locale.toLanguageTag();
        return tag.isEmpty() ? "ru" : tag;
    }

    private static String safe(String value) { return value == null || value.isEmpty() ? "системный" : value; }

    @Override protected void onDestroy() {
        ready = false;
        if (tts != null) {
            try { tts.stop(); } catch (Exception ignored) { }
            try { tts.shutdown(); } catch (Exception ignored) { }
        }
        tts = null;
        super.onDestroy();
    }
}
