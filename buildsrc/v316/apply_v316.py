from pathlib import Path

repo = Path(__file__).resolve().parents[1]
app = repo / 'quiet-diary' / 'app'
java = app / 'src' / 'main' / 'java' / 'com' / 'quietdiary' / 'app'

build = app / 'build.gradle.kts'
s = build.read_text(encoding='utf-8')
assert 'versionCode = 30150' in s
assert 'versionName = "0.31.5-night-music"' in s
s = s.replace('versionCode = 30150', 'versionCode = 30160', 1)
s = s.replace('versionName = "0.31.5-night-music"', 'versionName = "0.31.6-night-practice"', 1)
build.write_text(s, encoding='utf-8')

# User recordings naturally contain a little edge silence. A three-second scheduler
# gap therefore sounded longer than five seconds in the physical test. Shorten only
# the explicit gap; never destructively trim the user's recording.
for name, const in [('CouePracticeService.java', 'PAUSE_MS'), ('NightProgramService.java', 'COUE_PAUSE_MS')]:
    p = java / name
    s = p.read_text(encoding='utf-8')
    old = f'private static final long {const} = 3000L;'
    new = f'private static final long {const} = 1500L;'
    assert old in s, (name, old)
    s = s.replace(old, new, 1)
    p.write_text(s, encoding='utf-8')

selfui = java / 'SelfSuggestionActivity.java'
s = selfui.read_text(encoding='utf-8')
s = s.replace(
    '// Approximation only: a short phrase plus a calm 5-second pause.\n        int approxSeconds = repetitions * 8;',
    '// Approximation only: the recording itself includes natural edge silence;\n        // 0.31.6 shortens the explicit gap so the heard pause is about three seconds.\n        int approxSeconds = repetitions * 6;',
    1)
selfui.write_text(s, encoding='utf-8')

night = java / 'NightCaptureService.java'
s = night.read_text(encoding='utf-8')

s = s.replace(
    'private enum VerificationPurpose { ENTRY, DREAM, TIME, ALARM, STOP }',
    'private enum VerificationPurpose { ENTRY, DREAM, TIME, ALARM, STOP, PRACTICE }', 1)
s = s.replace(
    '    private AcousticWakeDetector stopDetector;\n',
    '    private AcousticWakeDetector stopDetector;\n    private AcousticWakeDetector practiceDetector;\n', 1)
s = s.replace(
    '    private List<short[]> stopTemplates;\n',
    '    private List<short[]> stopTemplates;\n    private List<short[]> practiceTemplates;\n', 1)
s = s.replace(
    '    private double stopStoredThreshold;\n',
    '    private double stopStoredThreshold;\n    private double practiceStoredThreshold;\n', 1)
s = s.replace(
    '    private String stopLabel = "Ночь стоп";\n',
    '    private String stopLabel = "Ночь стоп";\n    private String practiceLabel = CouePracticeService.DEFAULT_START_PHRASE;\n', 1)

old = '''            stopTemplates = WakeTemplateStore.loadStopForDetection(this);\n            stopStoredThreshold = WakeTemplateStore.stopThreshold(this);\n            SharedPreferences preferences = getSharedPreferences("settings", MODE_PRIVATE);'''
new = '''            stopTemplates = WakeTemplateStore.loadStopForDetection(this);\n            stopStoredThreshold = WakeTemplateStore.stopThreshold(this);\n            practiceTemplates = CoueStartTemplateStore.loadAll(this);\n            practiceStoredThreshold = CoueStartTemplateStore.threshold(this);\n            SharedPreferences preferences = getSharedPreferences("settings", MODE_PRIVATE);'''
assert old in s
s = s.replace(old, new, 1)

old = '''            String savedStopLabel = preferences.getString("stop_night_phrase", "Ночь стоп");\n            if (savedStopLabel != null && !savedStopLabel.trim().isEmpty()) stopLabel = savedStopLabel.trim();\n            recreateWakeDetector();'''
new = '''            String savedStopLabel = preferences.getString("stop_night_phrase", "Ночь стоп");\n            if (savedStopLabel != null && !savedStopLabel.trim().isEmpty()) stopLabel = savedStopLabel.trim();\n            String savedPracticeLabel = preferences.getString(CouePracticeService.KEY_START_PHRASE,\n                    CouePracticeService.DEFAULT_START_PHRASE);\n            if (savedPracticeLabel != null && !savedPracticeLabel.trim().isEmpty()) {\n                practiceLabel = savedPracticeLabel.trim();\n            }\n            recreateWakeDetector();'''
assert old in s
s = s.replace(old, new, 1)

s = s.replace(
    '            if (completed.error.isEmpty() && !completed.recognizedText.isEmpty()) {',
    '            if (completedPurpose != VerificationPurpose.PRACTICE\n                    && completed.error.isEmpty() && !completed.recognizedText.isEmpty()) {', 1)

old = '''                if (completedPurpose == VerificationPurpose.TIME) {\n                    wakeCandidateDreamHint = false;\n                    clearWakeVerificationBuffer();\n                    answerCurrentTimeByVoice("самостоятельная команда «" + timeLabel + "»");\n                    return;\n                }'''
new = '''                if (completedPurpose == VerificationPurpose.PRACTICE) {\n                    wakeCandidateDreamHint = false;\n                    clearWakeVerificationBuffer();\n                    startPracticeFromNight();\n                    return;\n                }\n                if (completedPurpose == VerificationPurpose.TIME) {\n                    wakeCandidateDreamHint = false;\n                    clearWakeVerificationBuffer();\n                    answerCurrentTimeByVoice("самостоятельная команда «" + timeLabel + "»");\n                    return;\n                }'''
assert old in s
s = s.replace(old, new, 1)

old = '''                        : completedPurpose == VerificationPurpose.DREAM\n                        ? "Команда сна не подтверждена · " + detail\n                        : "Кодовая фраза не подтверждена · " + detail);'''
new = '''                        : completedPurpose == VerificationPurpose.DREAM\n                        ? "Команда сна не подтверждена · " + detail\n                        : completedPurpose == VerificationPurpose.PRACTICE\n                        ? "Команда практики не подтверждена · " + detail\n                        : "Кодовая фраза не подтверждена · " + detail);'''
assert old in s
s = s.replace(old, new, 1)

marker = '''        if (timeDetector != null) {\n'''
block = '''        if (practiceDetector != null) {\n            boolean practiceMatched = practiceDetector.accept(buffer, count);\n            practiceDetector.consumeCandidateFinished();\n            if (practiceMatched) {\n                short[] practiceCandidate = practiceDetector.consumeMatchedCandidate();\n                if (practiceCandidate != null && practiceCandidate.length > 0) {\n                    wakeArmed = false;\n                    if (wakeDetector != null) wakeDetector.reset();\n                    if (dreamDetector != null) dreamDetector.reset();\n                    if (timeDetector != null) timeDetector.reset();\n                    if (alarmDetector != null) alarmDetector.reset();\n                    if (stopDetector != null) stopDetector.reset();\n                    DiagnosticsStore.record(this, DiagnosticsStore.ACOUSTIC_MATCH,\n                            "самостоятельная команда практики · " + practiceCandidate.length + " отсчётов",\n                            0L, MODE_WAITING);\n                    startPracticeTextVerification(practiceCandidate);\n                    return;\n                }\n            }\n        }\n\n'''
pos = s.find(marker, s.find('if (stopDetector != null)'))
assert pos >= 0
s = s[:pos] + block + s[pos:]

marker = '''    private void startTimeTextVerification(short[] candidate) {\n'''
method = '''    private void startPracticeTextVerification(short[] candidate) {\n        verificationPurpose = VerificationPurpose.PRACTICE;\n        wakeCandidateDreamHint = false;\n        clearWakeVerificationBuffer();\n        wakeVerificationResult.set(null);\n        final long generation = wakeVerificationGeneration.incrementAndGet();\n        wakeVerificationStartedAt = System.currentTimeMillis();\n        wakeVerificationInProgress.set(true);\n        setMode(MODE_VERIFYING);\n        vibratePattern(new long[]{0, 70});\n        updateNotification("Команда практики услышана · проверяю…");\n        DiagnosticsStore.record(this, DiagnosticsStore.VERIFY_START,\n                "голосовой запуск практики: " + practiceLabel, 0L, MODE_VERIFYING);\n\n        GoogleSpeechTranscriber.transcribeSamples(candidate,\n                new GoogleSpeechTranscriber.TranscriptionListener() {\n                    @Override public void onComplete(String text) {\n                        if (wakeVerificationGeneration.get() != generation || !running.get()) return;\n                        WakePhraseTextMatcher.MatchResult custom =\n                                WakePhraseTextMatcher.match(practiceLabel, text);\n                        wakeVerificationResult.set(new WakeVerificationResult(\n                                custom.matched, text, "", custom.matchedAnchor));\n                    }\n\n                    @Override public void onError(String message) {\n                        if (wakeVerificationGeneration.get() != generation || !running.get()) return;\n                        wakeVerificationResult.set(new WakeVerificationResult(false, "", message, ""));\n                    }\n                });\n    }\n\n'''
assert marker in s
s = s.replace(marker, method + marker, 1)

marker = '''    private void stopNightModeByVoice() {\n'''
method = '''    private void startPracticeFromNight() {\n        File coueDir = new File(getFilesDir(), "coue");\n        File voice = new File(coueDir, "my_formula.wav");\n        if (!voice.isFile()) voice = new File(coueDir, "my_formula.m4a");\n        if (!voice.isFile() || voice.length() < 1000L) {\n            earlyStartCuePlayed = false;\n            scheduleWakeRearm(RETRY_QUIET_MS);\n            setMode(MODE_WAITING);\n            updateNotification("Практика не запущена · сначала запишите формулу своим голосом");\n            return;\n        }\n\n        long duration = currentStartedAt <= 0L ? 0L : System.currentTimeMillis() - currentStartedAt;\n        wakeVerificationGeneration.incrementAndGet();\n        wakeVerificationStartedAt = 0L;\n        wakeVerificationInProgress.set(false);\n        wakeVerificationResult.set(null);\n        verificationPurpose = VerificationPurpose.ENTRY;\n        clearWakeVerificationBuffer();\n        earlyStartCuePlayed = false;\n        stopCommandRecognizer();\n        closeCurrentWriters();\n        if (currentAudioFile != null) currentAudioFile.delete();\n        if (currentPcmFile != null) currentPcmFile.delete();\n        clearCurrentEntryState();\n        DiagnosticsStore.record(this, DiagnosticsStore.SERVICE_STOP,\n                "ночной режим → практика по голосовой команде", duration, mode);\n\n        SharedPreferences settings = getSharedPreferences("settings", MODE_PRIVATE);\n        settings.edit().putBoolean(CouePracticeActivity.KEY_AUTO_NIGHT, true).apply();\n        statusText = "Запускаю практику · после неё вернусь в ночной режим";\n        pauseAudioInputForSpeech();\n        finalizeNightSession();\n        running.set(false);\n        setMode(MODE_OFF);\n        updateNotification(statusText);\n\n        try {\n            Intent practice = new Intent(this, CouePracticeService.class)\n                    .setAction(CouePracticeService.ACTION_START_PRACTICE);\n            ContextCompat.startForegroundService(this, practice);\n            stopForeground(STOP_FOREGROUND_REMOVE);\n            stopSelf();\n        } catch (Exception error) {\n            Log.e(TAG, "Unable to start practice from night mode", error);\n            running.set(true);\n            try {\n                restartAudioInput();\n                enterWaitingMode(false);\n            } catch (Exception restartError) {\n                running.set(false);\n                setMode(MODE_OFF);\n                updateNotification("Не удалось запустить практику");\n            }\n        }\n    }\n\n'''
assert marker in s
s = s.replace(marker, method + marker, 1)

s = s.replace(
    '        if (stopDetector != null) stopDetector.reset();\n    }\n\n    private void abortWakeVerification',
    '        if (stopDetector != null) stopDetector.reset();\n        if (practiceDetector != null) practiceDetector.reset();\n    }\n\n    private void abortWakeVerification', 1)

old = '''                : abortedPurpose == VerificationPurpose.DREAM\n                ? "Проверка команды сна сброшена · "\n                : "Проверка кодовой фразы сброшена · ") + detail);'''
new = '''                : abortedPurpose == VerificationPurpose.DREAM\n                ? "Проверка команды сна сброшена · "\n                : abortedPurpose == VerificationPurpose.PRACTICE\n                ? "Проверка команды практики сброшена · "\n                : "Проверка кодовой фразы сброшена · ") + detail);'''
assert old in s
s = s.replace(old, new, 1)

old = '''        if (stopTemplates != null && stopTemplates.size() >= WakeTemplateStore.REQUIRED_STOP_SAMPLES) {\n            stopDetector = new AcousticWakeDetector(stopTemplates, stopStoredThreshold, false);\n        } else {\n            stopDetector = null;\n        }\n    }'''
new = '''        if (stopTemplates != null && stopTemplates.size() >= WakeTemplateStore.REQUIRED_STOP_SAMPLES) {\n            stopDetector = new AcousticWakeDetector(stopTemplates, stopStoredThreshold, false);\n        } else {\n            stopDetector = null;\n        }\n        if (practiceTemplates != null\n                && practiceTemplates.size() >= CoueStartTemplateStore.REQUIRED_SAMPLES) {\n            practiceDetector = new AcousticWakeDetector(practiceTemplates, practiceStoredThreshold, false);\n        } else {\n            practiceDetector = null;\n        }\n    }'''
assert old in s
s = s.replace(old, new, 1)

old = '''        boolean stopReady = stopTemplates != null\n                && stopTemplates.size() >= WakeTemplateStore.REQUIRED_STOP_SAMPLES;\n        StringBuilder result = new StringBuilder("Жду «").append(wakeLabel).append("»");'''
new = '''        boolean stopReady = stopTemplates != null\n                && stopTemplates.size() >= WakeTemplateStore.REQUIRED_STOP_SAMPLES;\n        boolean practiceReady = practiceTemplates != null\n                && practiceTemplates.size() >= CoueStartTemplateStore.REQUIRED_SAMPLES;\n        StringBuilder result = new StringBuilder("Жду «").append(wakeLabel).append("»");'''
assert old in s
s = s.replace(old, new, 1)
old = '''        if (alarmReady) result.append(", «").append(alarmLabel).append("»");\n        if (stopReady) result.append(" или «").append(stopLabel).append("»");\n        return result.append(" · звук не сохраняется").toString();'''
new = '''        if (alarmReady) result.append(", «").append(alarmLabel).append("»");\n        if (practiceReady) result.append(", «").append(practiceLabel).append("»");\n        if (stopReady) result.append(" или «").append(stopLabel).append("»");\n        return result.append(" · звук не сохраняется").toString();'''
assert old in s
s = s.replace(old, new, 1)

night.write_text(s, encoding='utf-8')
print('Applied Somnori 0.31.6 night practice voice command')
