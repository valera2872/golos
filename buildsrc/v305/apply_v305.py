from pathlib import Path

ROOT = Path('buildsrc/quiet-diary')

def replace(path, old, new):
    p = ROOT / path
    text = p.read_text(encoding='utf-8')
    if old not in text:
        raise SystemExit(f'expected text not found in {path}: {old[:120]!r}')
    p.write_text(text.replace(old, new, 1), encoding='utf-8')

# Version.
replace('app/build.gradle.kts', 'versionCode = 30040', 'versionCode = 30050')
replace('app/build.gradle.kts', 'versionName = "0.30.4"', 'versionName = "0.30.5"')

# Night Assistant: remove fixed-height showcase hero that clips on real devices/font metrics.
replace(
    'app/src/main/res/layout/activity_night_assistant.xml',
    '<FrameLayout android:layout_width="match_parent" android:layout_height="142dp" android:layout_marginTop="14dp" android:background="@drawable/somnori_assistant_card_background">\n        <LinearLayout android:layout_width="match_parent" android:layout_height="match_parent" android:gravity="center_vertical" android:orientation="vertical" android:paddingEnd="118dp">',
    '<FrameLayout android:layout_width="match_parent" android:layout_height="wrap_content" android:layout_marginTop="14dp" android:background="@drawable/somnori_assistant_card_background" android:minHeight="172dp">\n        <LinearLayout android:layout_width="match_parent" android:layout_height="wrap_content" android:gravity="center_vertical" android:minHeight="172dp" android:orientation="vertical" android:paddingTop="18dp" android:paddingEnd="118dp" android:paddingBottom="18dp">'
)

# Natural Russian copy in Self-suggestion.
replace(
    'app/src/main/res/layout/activity_self_suggestion.xml',
    'android:maxLines="3"\n                android:text="Выберите смысл, запишите фразу один раз — Somnori повторит её вашим голосом, пока вы отдыхаете."',
    'android:maxLines="4"\n                android:text="Выберите фразу для самовнушения и запишите её один раз — Somnori повторит её вашим голосом."'
)
replace('app/src/main/res/layout/activity_self_suggestion.xml', 'android:text="Что хотите укрепить?"', 'android:text="Выберите фразу"')
replace(
    'app/src/main/res/layout/activity_self_suggestion.xml',
    'android:text="Возьмите готовую формулу или напишите свою."',
    'android:text="Используйте готовую фразу для самовнушения или напишите свою."'
)

# Settings/training state reliability.
path = ROOT / 'app/src/main/java/com/quietdiary/app/SettingsActivity.java'
text = path.read_text(encoding='utf-8')

def one(old, new):
    global text
    if old not in text:
        raise SystemExit(f'expected SettingsActivity fragment not found: {old[:140]!r}')
    text = text.replace(old, new, 1)

one(
    '    private boolean serviceRunning;\n\n    // UI recovery guard:',
    '    private boolean serviceRunning;\n    private SharedPreferences settingsPrefs;\n    private boolean settingsListenerRegistered;\n\n    // UI recovery guard:'
)
one(
    '        @Override public void run() {\n            if (WakeWordTrainer.isBusy() || WakePhraseTester.isBusy()) {',
    '        @Override public void run() {\n            refreshServiceRunningState();\n            if (WakeWordTrainer.isBusy() || WakePhraseTester.isBusy()) {'
)
one(
    '    };\n\n    private final ActivityResultLauncher<String> trainingPermissionLauncher =',
    '    };\n\n    private final SharedPreferences.OnSharedPreferenceChangeListener settingsStateListener =\n            (prefs, key) -> {\n                if (!"service_running".equals(key)) return;\n                runOnUiThread(() -> {\n                    refreshServiceRunningState();\n                    renderTrainingState();\n                });\n            };\n\n    private final ActivityResultLauncher<String> trainingPermissionLauncher ='
)
one(
    '        SharedPreferences prefs = getSharedPreferences("settings", MODE_PRIVATE);',
    '        SharedPreferences prefs = getSharedPreferences("settings", MODE_PRIVATE);\n        settingsPrefs = prefs;'
)
one(
    '''    @Override protected void onStart() {\n        super.onStart();\n        serviceRunning = getSharedPreferences("settings", MODE_PRIVATE)\n                .getBoolean("service_running", false);\n        renderTrainingState();\n        scheduleTrainingControlsRecovery(80L);\n    }\n\n    @Override protected void onResume() {\n        super.onResume();\n        scheduleTrainingControlsRecovery(80L);\n    }\n\n    @Override protected void onDestroy() {\n        trainingUiHandler.removeCallbacks(trainingControlsRecovery);\n        super.onDestroy();\n    }''',
    '''    @Override protected void onStart() {\n        super.onStart();\n        if (settingsPrefs == null) settingsPrefs = getSharedPreferences("settings", MODE_PRIVATE);\n        if (!settingsListenerRegistered) {\n            settingsPrefs.registerOnSharedPreferenceChangeListener(settingsStateListener);\n            settingsListenerRegistered = true;\n        }\n        refreshServiceRunningState();\n        renderTrainingState();\n        scheduleTrainingControlsRecovery(80L);\n    }\n\n    @Override protected void onResume() {\n        super.onResume();\n        refreshServiceRunningState();\n        renderTrainingState();\n        scheduleTrainingControlsRecovery(80L);\n    }\n\n    @Override protected void onStop() {\n        if (settingsListenerRegistered && settingsPrefs != null) {\n            settingsPrefs.unregisterOnSharedPreferenceChangeListener(settingsStateListener);\n            settingsListenerRegistered = false;\n        }\n        super.onStop();\n    }\n\n    @Override protected void onDestroy() {\n        trainingUiHandler.removeCallbacks(trainingControlsRecovery);\n        super.onDestroy();\n    }'''
)
one(
    '''        setTrainingControlsEnabled(false);\n        trainingStatus.setText("Повтор " + target + " из " + visibleTarget + ". Приготовьтесь…");\n        WakeWordTrainer.recordSample(this, new WakeWordTrainer.Listener() {\n            @Override public void onReadyToSpeak() {\n                runOnUiThread(() -> {\n                    trainingStatus.setText("Скажите фразу спокойно и естественно…");\n                    vibrate(70);\n                });\n            }''',
    '''        setTrainingControlsEnabled(false);\n        trainWakeButton.setText("Записываю повтор " + target + " из " + visibleTarget + "…");\n        if (trainingProgressLabel != null) {\n            trainingProgressLabel.setText("Записываю повтор " + target + " из " + visibleTarget);\n        }\n        if (trainingProgress != null) {\n            trainingProgress.setProgress(Math.min(existing, WakeTemplateStore.MAX_REQUIRED_SAMPLES));\n        }\n        trainingStatus.setText("Повтор " + target + " из " + visibleTarget + ". Приготовьтесь…");\n        WakeWordTrainer.recordSample(this, new WakeWordTrainer.Listener() {\n            @Override public void onReadyToSpeak() {\n                runOnUiThread(() -> {\n                    trainWakeButton.setText("Говорите…");\n                    trainingStatus.setText("Скажите фразу спокойно и естественно…");\n                    vibrate(70);\n                });\n            }'''
)
one(
    '''    private boolean canTrain() {\n        if (serviceRunning) {\n            Toast.makeText(this, "Сначала завершите ночной режим", Toast.LENGTH_SHORT).show();\n            return false;\n        }\n        return true;\n    }''',
    '''    private boolean canTrain() {\n        refreshServiceRunningState();\n        if (serviceRunning) {\n            Toast.makeText(this, "Сначала завершите ночной режим", Toast.LENGTH_SHORT).show();\n            scheduleTrainingControlsRecovery(120L);\n            return false;\n        }\n        if (WakeWordTrainer.isBusy() || WakePhraseTester.isBusy()) {\n            Toast.makeText(this, "Предыдущая запись ещё завершается", Toast.LENGTH_SHORT).show();\n            scheduleTrainingControlsRecovery(120L);\n            return false;\n        }\n        return true;\n    }\n\n    private void refreshServiceRunningState() {\n        SharedPreferences prefs = settingsPrefs != null\n                ? settingsPrefs : getSharedPreferences("settings", MODE_PRIVATE);\n        serviceRunning = prefs.getBoolean("service_running", false);\n    }'''
)
one(
    '        wakePhraseInput.setEnabled(enabled);\n        timePhraseInput.setEnabled(enabled);',
    '        wakePhraseInput.setEnabled(enabled);\n        dreamPhraseInput.setEnabled(enabled);\n        timePhraseInput.setEnabled(enabled);'
)
one(
    '    private void renderTrainingState() {\n        int count = WakeTemplateStore.count(this);',
    '    private void renderTrainingState() {\n        refreshServiceRunningState();\n        int count = WakeTemplateStore.count(this);'
)
one(
    '        boolean busy = WakeWordTrainer.isBusy() || WakePhraseTester.isBusy();\n        WakeTemplateStore.TrainingAssessment assessment',
    '        boolean busy = WakeWordTrainer.isBusy() || WakePhraseTester.isBusy();\n        if (busy) scheduleTrainingControlsRecovery(180L);\n        else trainingUiHandler.removeCallbacks(trainingControlsRecovery);\n        WakeTemplateStore.TrainingAssessment assessment'
)
one(
    '        wakePhraseInput.setEnabled(!serviceRunning && !busy);\n        timePhraseInput.setEnabled(!serviceRunning && !busy);',
    '        wakePhraseInput.setEnabled(!serviceRunning && !busy);\n        dreamPhraseInput.setEnabled(!serviceRunning && !busy);\n        timePhraseInput.setEnabled(!serviceRunning && !busy);'
)
one(
    '''    private void applyWakePreset(String phrase) {\n        if (serviceRunning || WakeWordTrainer.isBusy() || WakePhraseTester.isBusy()) return;\n        wakePhraseInput.setText(phrase);''',
    '''    private void applyWakePreset(String phrase) {\n        if (!canTrain()) return;\n        wakePhraseInput.setText(phrase);'''
)

path.write_text(text, encoding='utf-8')
print('Applied Somnori 0.30.5 RU UI + training-state reliability patch')
