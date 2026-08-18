from pathlib import Path
import xml.etree.ElementTree as ET

ANDROID='http://schemas.android.com/apk/res/android'
APP='http://schemas.android.com/apk/res-auto'
ET.register_namespace('android',ANDROID); ET.register_namespace('app',APP)
A=lambda n:f'{{{ANDROID}}}{n}'

project=Path('buildsrc/quiet-diary')
res=project/'app/src/main/res'
java=project/'app/src/main/java/com/quietdiary/app'

# Version 0.30.0 -> 0.30.1
gradle=project/'app/build.gradle.kts'
g=gradle.read_text(encoding='utf-8')
if 'versionCode = 3000' not in g or 'versionName = "0.30.0"' not in g:
    raise SystemExit('expected 0.30.0 base')
g=g.replace('versionCode = 3000','versionCode = 3001').replace('versionName = "0.30.0"','versionName = "0.30.1"')
gradle.write_text(g,encoding='utf-8')

# Standalone soundscape is allowed to survive screen-off/home, but not an explicit task removal.
manifest=project/'app/src/main/AndroidManifest.xml'
m=manifest.read_text(encoding='utf-8')
old='''        <service
            android:name=".SoundscapeService"
            android:exported="false"
            android:foregroundServiceType="mediaPlayback"
            android:stopWithTask="false" />'''
new='''        <service
            android:name=".SoundscapeService"
            android:exported="false"
            android:foregroundServiceType="mediaPlayback"
            android:stopWithTask="true" />'''
if old not in m: raise SystemExit('SoundscapeService manifest block missing')
m=m.replace(old,new,1)
manifest.write_text(m,encoding='utf-8')

# Persist current sound name and stop playback when the standalone Somnori task is explicitly removed.
service=java/'SoundscapeService.java'
s=service.read_text(encoding='utf-8')
needle='''    public static final String KEY_RUNNING = "soundscape_running";
    public static final String KEY_STATUS = "soundscape_status";'''
if needle not in s: raise SystemExit('SoundscapeService keys missing')
s=s.replace(needle,needle+'\n    public static final String KEY_NAME = "soundscape_name";',1)
needle='''    @Nullable @Override public IBinder onBind(Intent intent) { return null; }

    @Override public void onDestroy() {'''
replacement='''    @Nullable @Override public IBinder onBind(Intent intent) { return null; }

    @Override public void onTaskRemoved(Intent rootIntent) {
        stopPlayback("Звук остановлен");
        super.onTaskRemoved(rootIntent);
    }

    @Override public void onDestroy() {'''
if needle not in s: raise SystemExit('SoundscapeService lifecycle insertion missing')
s=s.replace(needle,replacement,1)
needle='''            running = true;
            prefs.edit().putBoolean(KEY_RUNNING, true).apply();
            player.start();'''
replacement='''            running = true;
            prefs.edit()
                    .putBoolean(KEY_RUNNING, true)
                    .putString(KEY_NAME, soundName)
                    .apply();
            player.start();'''
if needle not in s: raise SystemExit('SoundscapeService start state missing')
s=s.replace(needle,replacement,1)
needle='''        prefs.edit().putBoolean(KEY_RUNNING, false).putString(KEY_STATUS, status).apply();'''
replacement='''        prefs.edit()
                .putBoolean(KEY_RUNNING, false)
                .putString(KEY_STATUS, status)
                .remove(KEY_NAME)
                .apply();'''
if needle not in s: raise SystemExit('SoundscapeService stop state missing')
s=s.replace(needle,replacement,1)
service.write_text(s,encoding='utf-8')

# Move current-selection/status/stop controls to the top of the sound library so Stop is always obvious.
sound_layout=res/'layout/activity_sound_library.xml'
tree=ET.parse(sound_layout); root=tree.getroot()
container=list(root)[0]

def by_id(parent, view_id):
    for e in parent.iter():
        if e.attrib.get(A('id'))==f'@+id/{view_id}': return e
    raise SystemExit(f'missing {view_id}')

selected=by_id(container,'soundSelectedLabel')
status=by_id(container,'soundStatus')
stop=by_id(container,'soundStopButton')
for node in (selected,status,stop):
    container.remove(node)
# Insert immediately after intro subtitle, before the MUSIC heading.
music_idx=None
for i,node in enumerate(list(container)):
    if node.attrib.get(A('text'))=='МУЗЫКА':
        music_idx=i; break
if music_idx is None: raise SystemExit('MUSIC heading missing')
selected.set(A('layout_marginTop'),'16dp')
selected.set(A('text'),'Сейчас ничего не играет')
status.set(A('layout_marginTop'),'4dp')
stop.set(A('layout_marginTop'),'9dp')
stop.set(A('visibility'),'gone')
container.insert(music_idx,selected)
container.insert(music_idx+1,status)
container.insert(music_idx+2,stop)
tree.write(sound_layout,encoding='utf-8',xml_declaration=True)

# Sound library renders actual service state and makes Stop disappear after use.
activity=java/'SoundLibraryActivity.java'
s=activity.read_text(encoding='utf-8')
needle='''        findViewById(R.id.soundStopButton).setOnClickListener(v -> {
            startService(new Intent(this, SoundscapeService.class).setAction(SoundscapeService.ACTION_STOP));
            status.setText("Звук остановлен");
        });'''
replacement='''        findViewById(R.id.soundStopButton).setOnClickListener(v -> {
            startService(new Intent(this, SoundscapeService.class).setAction(SoundscapeService.ACTION_STOP));
            status.setText("Звук остановлен");
            selected.setText("Сейчас ничего не играет");
            findViewById(R.id.soundStopButton).setVisibility(View.GONE);
        });'''
if needle not in s: raise SystemExit('sound stop listener missing')
s=s.replace(needle,replacement,1)
needle='''        ContextCompat.startForegroundService(this, intent);
        status.setText(selectedName + " · играет");'''
replacement='''        ContextCompat.startForegroundService(this, intent);
        selected.setText("Сейчас играет: " + selectedName);
        status.setText(selectedName + " · играет");
        findViewById(R.id.soundStopButton).setVisibility(View.VISIBLE);'''
if needle not in s: raise SystemExit('sound start state missing')
s=s.replace(needle,replacement,1)
old_render='''    private void render() {
        selected.setText("Выбрано: " + selectedName);
        status.setText("Нажмите на звук — он начнёт играть сразу");
        renderTrackSelection();
        renderCustomButton();
    }'''
new_render='''    private void render() {
        boolean running = prefs.getBoolean(SoundscapeService.KEY_RUNNING, false);
        String currentName = prefs.getString(SoundscapeService.KEY_NAME, "");
        String currentStatus = prefs.getString(SoundscapeService.KEY_STATUS, "");
        if (running) {
            selected.setText("Сейчас играет: " + (currentName == null || currentName.trim().isEmpty() ? selectedName : currentName));
            status.setText(currentStatus == null || currentStatus.trim().isEmpty() ? "Звук играет в фоне" : currentStatus);
            findViewById(R.id.soundStopButton).setVisibility(View.VISIBLE);
        } else {
            selected.setText("Сейчас ничего не играет");
            status.setText("Нажмите на звук — он начнёт играть сразу");
            findViewById(R.id.soundStopButton).setVisibility(View.GONE);
        }
        renderTrackSelection();
        renderCustomButton();
    }

    @Override protected void onResume() {
        super.onResume();
        if (prefs != null) render();
    }'''
if old_render not in s: raise SystemExit('SoundLibrary render block missing')
s=s.replace(old_render,new_render,1)
activity.write_text(s,encoding='utf-8')

# Add a compact global now-playing bar to the main dashboard, only visible while standalone music plays.
main=res/'layout/activity_main.xml'
tree=ET.parse(main); root=tree.getroot(); parents={c:p for p in root.iter() for c in p}
def main_by_id(view_id):
    for e in root.iter():
        if e.attrib.get(A('id'))==f'@+id/{view_id}': return e
    raise SystemExit(f'missing main id {view_id}')
hero=main_by_id('dashboardNightCard')
p=parents[hero]; idx=list(p).index(hero)
bar=ET.fromstring('''<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android" xmlns:app="http://schemas.android.com/apk/res-auto"
    android:id="@+id/dashboardSoundscapeBar"
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:layout_marginTop="10dp"
    android:background="@drawable/somnori_soundscape_now_background"
    android:gravity="center_vertical"
    android:orientation="horizontal"
    android:paddingStart="14dp"
    android:paddingTop="10dp"
    android:paddingEnd="10dp"
    android:paddingBottom="10dp"
    android:visibility="gone">
    <TextView
        android:id="@+id/dashboardSoundscapeStatus"
        android:layout_width="0dp"
        android:layout_height="wrap_content"
        android:layout_weight="1"
        android:maxLines="2"
        android:ellipsize="end"
        android:text="♫ Сейчас играет"
        android:textColor="@color/qd_text"
        android:textSize="11sp"
        android:textStyle="bold" />
    <com.google.android.material.button.MaterialButton
        android:id="@+id/dashboardSoundscapeStopButton"
        android:layout_width="wrap_content"
        android:layout_height="40dp"
        android:layout_marginStart="8dp"
        android:minWidth="0dp"
        android:minHeight="0dp"
        android:text="Стоп"
        android:textAllCaps="false"
        android:textSize="10.5sp"
        app:backgroundTint="@android:color/transparent"
        app:cornerRadius="18dp"
        app:strokeColor="@color/qd_border_bright"
        app:strokeWidth="1dp" />
</LinearLayout>''')
p.insert(idx,bar)
tree.write(main,encoding='utf-8',xml_declaration=True)

(res/'drawable/somnori_soundscape_now_background.xml').write_text('''<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android" android:shape="rectangle">
    <corners android:radius="18dp" />
    <gradient android:angle="0" android:startColor="#2C214B" android:endColor="#15162F" />
    <stroke android:width="1dp" android:color="#5A4B83" />
</shape>
''',encoding='utf-8')

# MainActivity listens for SoundscapeService state and exposes a global Stop control.
main_activity=java/'MainActivity.java'
s=main_activity.read_text(encoding='utf-8')
needle='''    private TextView dashboardMorningStatus;'''
if needle not in s: raise SystemExit('MainActivity field insertion missing')
s=s.replace(needle,needle+'\n    private View dashboardSoundscapeBar;\n    private TextView dashboardSoundscapeStatus;',1)
needle='''        dashboardMorningStatus = findViewById(R.id.dashboardMorningStatus);'''
if needle not in s: raise SystemExit('MainActivity binding insertion missing')
s=s.replace(needle,needle+'\n        dashboardSoundscapeBar = findViewById(R.id.dashboardSoundscapeBar);\n        dashboardSoundscapeStatus = findViewById(R.id.dashboardSoundscapeStatus);',1)
needle='''        findViewById(R.id.dashboardMorningButton).setOnClickListener(v ->
                startActivity(new Intent(this, MorningActivity.class)));'''
if needle not in s: raise SystemExit('MainActivity listener insertion missing')
s=s.replace(needle,needle+'''\n        findViewById(R.id.dashboardSoundscapeStopButton).setOnClickListener(v -> {
            startService(new Intent(this, SoundscapeService.class).setAction(SoundscapeService.ACTION_STOP));
            renderSoundscapeDashboard();
        });''',1)
needle='''            } else if (ACTION_ENTRIES_CHANGED.equals(intent.getAction())) {'''
replacement='''            } else if (SoundscapeService.ACTION_STATE.equals(intent.getAction())) {
                renderSoundscapeDashboard();
            } else if (ACTION_ENTRIES_CHANGED.equals(intent.getAction())) {'''
if needle not in s: raise SystemExit('MainActivity receiver insertion missing')
s=s.replace(needle,replacement,1)
needle='''        filter.addAction(ACTION_ENTRIES_CHANGED);'''
if needle not in s: raise SystemExit('MainActivity filter insertion missing')
s=s.replace(needle,needle+'\n        filter.addAction(SoundscapeService.ACTION_STATE);',1)
needle='''        renderDashboardAlarm();
        renderServiceState();
        renderMorningDashboard();
    }

    private void renderMorningDashboard() {'''
replacement='''        renderDashboardAlarm();
        renderServiceState();
        renderMorningDashboard();
        renderSoundscapeDashboard();
    }

    private void renderSoundscapeDashboard() {
        if (dashboardSoundscapeBar == null || dashboardSoundscapeStatus == null) return;
        SharedPreferences prefs = getSharedPreferences("settings", MODE_PRIVATE);
        boolean running = prefs.getBoolean(SoundscapeService.KEY_RUNNING, false);
        dashboardSoundscapeBar.setVisibility(running ? View.VISIBLE : View.GONE);
        if (!running) return;
        String name = prefs.getString(SoundscapeService.KEY_NAME, "");
        String statusText = prefs.getString(SoundscapeService.KEY_STATUS, "");
        if (name == null || name.trim().isEmpty()) name = "Звук для сна";
        if (statusText == null || statusText.trim().isEmpty()) statusText = "играет в фоне";
        dashboardSoundscapeStatus.setText("♫  " + name + " · " + statusText.replace(name + " · ", ""));
    }

    private void renderMorningDashboard() {'''
if needle not in s: raise SystemExit('MainActivity render insertion missing')
s=s.replace(needle,replacement,1)
main_activity.write_text(s,encoding='utf-8')

# Regression guards.
for pth in res.rglob('*.xml'): ET.parse(pth)
assert 'android:stopWithTask="true"' in manifest.read_text(encoding='utf-8')
assert 'onTaskRemoved' in service.read_text(encoding='utf-8')
assert 'dashboardSoundscapeBar' in main.read_text(encoding='utf-8')
assert 'dashboardSoundscapeStopButton' in main.read_text(encoding='utf-8')
assert 'SoundscapeService.ACTION_STATE' in main_activity.read_text(encoding='utf-8')
assert 'soundStopButton' in sound_layout.read_text(encoding='utf-8')
assert 'SAFE_END_SILENCE_BLOCKS = 11' in (java/'AcousticWakeDetector.java').read_text(encoding='utf-8')
print('Somnori 0.30.1 audio stop UX hotfix applied')
