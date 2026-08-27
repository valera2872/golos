from pathlib import Path

repo = Path(__file__).resolve().parents[1]
app = repo / 'quiet-diary' / 'app'
java = app / 'src' / 'main' / 'java' / 'com' / 'quietdiary' / 'app'

build = app / 'build.gradle.kts'
s = build.read_text(encoding='utf-8')
assert 'versionCode = 30170' in s
assert 'versionName = "0.31.7-arina-gapless"' in s
s = s.replace('versionCode = 30170', 'versionCode = 30180', 1)
s = s.replace('versionName = "0.31.7-arina-gapless"', 'versionName = "0.31.8-practice-handoff"', 1)
build.write_text(s, encoding='utf-8')

# 1) A standalone practice-listener must never leave a stale WAITING/VERIFYING state
# after Android destroys/stops the service. Otherwise the next screen can believe the
# practice listener still owns the microphone.
coue = java / 'CouePracticeService.java'
s = coue.read_text(encoding='utf-8')
old = '''    @Override public void onDestroy() {
        cleanupWaiting();
        cleanupPlayer();
        releaseWakeLock();
        handler.removeCallbacksAndMessages(null);
        super.onDestroy();
    }'''
new = '''    @Override public void onDestroy() {
        boolean wasVoiceWait = MODE_WAITING.equals(mode) || MODE_VERIFYING.equals(mode);
        cleanupWaiting();
        cleanupPlayer();
        releaseWakeLock();
        handler.removeCallbacksAndMessages(null);
        if (wasVoiceWait) {
            publish(MODE_OFF, "Ожидание команды практики отключено", completed);
        }
        super.onDestroy();
    }'''
assert old in s
s = s.replace(old, new, 1)

# Make the toggle itself immediately unambiguous in the practice screen.
old = '''        if (CouePracticeService.MODE_WAITING.equals(mode)
                || CouePracticeService.MODE_VERIFYING.equals(mode)) {
            startCoueService(CouePracticeService.ACTION_STOP);
            renderRunning(false);
            return;
        }'''
new = '''        if (CouePracticeService.MODE_WAITING.equals(mode)
                || CouePracticeService.MODE_VERIFYING.equals(mode)) {
            voiceStartStatus.setText("Отключаю ожидание команды…");
            startCoueService(CouePracticeService.ACTION_STOP);
            renderRunning(false);
            return;
        }'''
selfui = java / 'SelfSuggestionActivity.java'
ui = selfui.read_text(encoding='utf-8')
assert old in ui
ui = ui.replace(old, new, 1)
selfui.write_text(ui, encoding='utf-8')

coue.write_text(s, encoding='utf-8')

# 2) Night mode is the owner of all-night voice listening. If the short standalone
# practice waiter is still active (or merely left stale state), explicitly disarm it
# before the night capture worker opens the microphone.
night = java / 'NightCaptureService.java'
s = night.read_text(encoding='utf-8')
old = '''        if (ACTION_CANCEL.equals(action)) {
            if (MODE_RECORDING.equals(mode)) {
                pendingCommand.set(PendingCommand.CANCEL);
                updateNotification("Отменяю запись…");
            }
            return START_NOT_STICKY;
        }
        if (running.compareAndSet(false, true)) {'''
new = '''        if (ACTION_CANCEL.equals(action)) {
            if (MODE_RECORDING.equals(mode)) {
                pendingCommand.set(PendingCommand.CANCEL);
                updateNotification("Отменяю запись…");
            }
            return START_NOT_STICKY;
        }

        // 0.31.8: the standalone Coué waiter is only for the practice screen.
        // When the user switches to Night mode, NightCaptureService becomes the single
        // microphone owner and already contains the trained practice detector alongside
        // time/alarm/dream/entry/stop. Disarm any old standalone waiter first.
        SharedPreferences handoffPrefs = getSharedPreferences("settings", MODE_PRIVATE);
        String coueMode = handoffPrefs.getString(CouePracticeService.KEY_MODE,
                CouePracticeService.MODE_OFF);
        boolean handoffFromPracticeWait = CouePracticeService.MODE_WAITING.equals(coueMode)
                || CouePracticeService.MODE_VERIFYING.equals(coueMode);
        if (handoffFromPracticeWait) {
            stopService(new Intent(this, CouePracticeService.class));
            handoffPrefs.edit()
                    .putString(CouePracticeService.KEY_MODE, CouePracticeService.MODE_OFF)
                    .putString(CouePracticeService.KEY_STATUS,
                            "Ожидание практики передано ночному режиму")
                    .putInt(CouePracticeService.KEY_PROGRESS, 0)
                    .apply();
        }
        if (running.compareAndSet(false, true)) {'''
assert old in s
s = s.replace(old, new, 1)

# Give Android a very short handoff window only when we actually stopped the old
# microphone owner. Normal night-mode startup remains unchanged.
old = '''            startForeground(NOTIFICATION_ID, buildNotification(statusText));
            worker = new Thread(this::captureLoop, "quiet-diary-capture");
            worker.start();
            setMode(MODE_WAITING);'''
new = '''            startForeground(NOTIFICATION_ID, buildNotification(statusText));
            final boolean waitForPracticeMicHandoff = handoffFromPracticeWait;
            worker = new Thread(() -> {
                if (waitForPracticeMicHandoff) {
                    try { Thread.sleep(180L); }
                    catch (InterruptedException e) { Thread.currentThread().interrupt(); }
                }
                captureLoop();
            }, "quiet-diary-capture");
            worker.start();
            setMode(MODE_WAITING);'''
assert old in s
s = s.replace(old, new, 1)

night.write_text(s, encoding='utf-8')
print('Applied Somnori 0.31.8 practice-listener -> night-mode handoff hotfix')
