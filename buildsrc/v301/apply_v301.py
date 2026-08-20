from pathlib import Path

ROOT = Path('buildsrc/quiet-diary')


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding='utf-8')
    if old not in text:
        raise SystemExit(f'expected block not found in {path}: {old[:90]!r}')
    path.write_text(text.replace(old, new, 1), encoding='utf-8')


# Night Assistant: make every visible state element derive from the same service snapshot.
night = ROOT / 'app/src/main/java/com/quietdiary/app/NightAssistantActivity.java'
replace_once(night,
    '    private TextView status;\n',
    '    private TextView status;\n    private TextView micStatus;\n')
replace_once(night,
    '        status = findViewById(R.id.nightAssistantStatus);\n',
    '        status = findViewById(R.id.nightAssistantStatus);\n        micStatus = findViewById(R.id.nightAssistantMicStatus);\n')
replace_once(night,
    '''        SharedPreferences prefs = getSharedPreferences("settings", MODE_PRIVATE);\n        serviceRunning = prefs.getBoolean("service_running", false);\n        serviceMode = prefs.getString("service_mode",\n                serviceRunning ? NightCaptureService.MODE_WAITING : NightCaptureService.MODE_OFF);\n        serviceStatusText = prefs.getString("service_status", "");\n        verificationStartedAt = prefs.getLong("verification_started_at", 0L);\n        renderCommands(prefs);\n''',
    '''        SharedPreferences prefs = getSharedPreferences("settings", MODE_PRIVATE);\n        syncServiceStateFromPreferences(prefs);\n        renderCommands(prefs);\n''')
replace_once(night,
    '''        SharedPreferences prefs = getSharedPreferences("settings", MODE_PRIVATE);\n        serviceRunning = prefs.getBoolean("service_running", serviceRunning);\n        serviceMode = prefs.getString("service_mode", serviceMode);\n        serviceStatusText = prefs.getString("service_status", serviceStatusText);\n        verificationStartedAt = prefs.getLong("verification_started_at", verificationStartedAt);\n        renderState();\n''',
    '''        SharedPreferences prefs = getSharedPreferences("settings", MODE_PRIVATE);\n        syncServiceStateFromPreferences(prefs);\n        renderState();\n''')
replace_once(night,
    '    private void renderCommands(SharedPreferences prefs) {\n',
    '''    private void syncServiceStateFromPreferences(SharedPreferences prefs) {\n        serviceRunning = prefs.getBoolean("service_running", false);\n        serviceMode = prefs.getString("service_mode",\n                serviceRunning ? NightCaptureService.MODE_WAITING : NightCaptureService.MODE_OFF);\n        serviceStatusText = prefs.getString("service_status", "");\n        verificationStartedAt = prefs.getLong("verification_started_at", 0L);\n        if (!serviceRunning || serviceMode == null) {\n            serviceMode = serviceRunning ? NightCaptureService.MODE_WAITING : NightCaptureService.MODE_OFF;\n        }\n        if (serviceStatusText == null) serviceStatusText = "";\n        if (!serviceRunning) verificationStartedAt = 0L;\n    }\n\n    private void renderCommands(SharedPreferences prefs) {\n''')
replace_once(night,
    '''        stopButton.setEnabled(false);\n        stateTitle.setText("Выключаю ночной режим…");\n''',
    '''        stopButton.setEnabled(false);\n        stopButton.setText("Выключаю…");\n        stateTitle.setText("Выключаю ночной режим…");\n''')
replace_once(night,
    '''    private void renderState() {\n        stopButton.setEnabled(serviceRunning);\n''',
    '''    private void renderState() {\n        micStatus.setText(serviceRunning ? "МИКРОФОН · ВКЛ" : "МИКРОФОН · ВЫКЛ");\n        stopButton.setText("Выключить ночной режим");\n        stopButton.setEnabled(serviceRunning);\n        stopButton.setVisibility(serviceRunning ? View.VISIBLE : View.GONE);\n''')

# Give the microphone status a real view id so it cannot remain a static XML label.
layout = ROOT / 'app/src/main/res/layout/activity_night_assistant.xml'
replace_once(layout,
    '''                    <TextView\n                        android:layout_width="0dp"\n                        android:layout_height="wrap_content"\n                        android:layout_marginStart="10dp"\n                        android:layout_weight="1"\n                        android:gravity="end"\n                        android:text="Микрофон активен"\n                        android:textColor="@color/qd_on_night_muted"\n                        android:textSize="10sp" />\n''',
    '''                    <TextView\n                        android:id="@+id/nightAssistantMicStatus"\n                        android:layout_width="0dp"\n                        android:layout_height="wrap_content"\n                        android:layout_marginStart="10dp"\n                        android:layout_weight="1"\n                        android:gravity="end"\n                        android:maxLines="1"\n                        android:text="МИКРОФОН · ВЫКЛ"\n                        android:textColor="@color/qd_on_night_muted"\n                        android:textSize="9sp" />\n''')

# Main screen: when returning from another Activity / screen-off state, refresh the service
# snapshot from the same preferences written by NightCaptureService before rendering buttons.
main = ROOT / 'app/src/main/java/com/quietdiary/app/MainActivity.java'
replace_once(main,
    '''        serviceRunning = prefs.getBoolean("service_running", false);\n        serviceMode = prefs.getString("service_mode",\n                serviceRunning ? NightCaptureService.MODE_WAITING : NightCaptureService.MODE_OFF);\n        serviceStatusText = prefs.getString("service_status", "");\n        verificationStartedAt = prefs.getLong("verification_started_at", 0L);\n''',
    '        syncServiceStateFromPreferences(prefs);\n')
replace_once(main,
    '''        ContextCompat.registerReceiver(this, stateReceiver, filter, ContextCompat.RECEIVER_NOT_EXPORTED);\n        NightSessionStore.syncFromPreferences(this);\n        renderServiceState();\n''',
    '''        ContextCompat.registerReceiver(this, stateReceiver, filter, ContextCompat.RECEIVER_NOT_EXPORTED);\n        syncServiceStateFromPreferences(getSharedPreferences("settings", MODE_PRIVATE));\n        NightSessionStore.syncFromPreferences(this);\n        renderServiceState();\n''')
replace_once(main,
    '    private void prepareRecognitionSilently() {\n',
    '''    private void syncServiceStateFromPreferences(SharedPreferences prefs) {\n        serviceRunning = prefs.getBoolean("service_running", false);\n        serviceMode = prefs.getString("service_mode",\n                serviceRunning ? NightCaptureService.MODE_WAITING : NightCaptureService.MODE_OFF);\n        serviceStatusText = prefs.getString("service_status", "");\n        verificationStartedAt = prefs.getLong("verification_started_at", 0L);\n        if (!serviceRunning || serviceMode == null) {\n            serviceMode = serviceRunning ? NightCaptureService.MODE_WAITING : NightCaptureService.MODE_OFF;\n        }\n        if (serviceStatusText == null) serviceStatusText = "";\n        if (!serviceRunning) verificationStartedAt = 0L;\n    }\n\n    private void prepareRecognitionSilently() {\n''')

# Version this physical hotfix separately from the accepted 0.30 source.
gradle = ROOT / 'app/build.gradle.kts'
replace_once(gradle, '        versionCode = 3000\n        versionName = "0.30.0"\n',
                    '        versionCode = 3001\n        versionName = "0.30.1"\n')

print('Somnori 0.30.1 night UI state hotfix applied')
