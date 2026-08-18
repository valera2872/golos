from pathlib import Path
import xml.etree.ElementTree as ET

ANDROID='http://schemas.android.com/apk/res/android'
APP='http://schemas.android.com/apk/res-auto'
ET.register_namespace('android',ANDROID); ET.register_namespace('app',APP)
A=lambda n:f'{{{ANDROID}}}{n}'

project=Path('buildsrc/quiet-diary')
res=project/'app/src/main/res'
java=project/'app/src/main/java/com/quietdiary/app'

# Version: Morning is now layered on the physically tested 0.29.10 hotfix line.
gradle=project/'app/build.gradle.kts'
g=gradle.read_text(encoding='utf-8')
if 'versionCode = 2910' not in g or 'versionName = "0.29.10"' not in g:
    raise SystemExit('expected 0.29.10 base')
g=g.replace('versionCode = 2910','versionCode = 3000').replace('versionName = "0.29.10"','versionName = "0.30.0"')
gradle.write_text(g,encoding='utf-8')

# Copy Morning implementation templates.
for name in ('MorningTools.java','MorningActivity.java'):
    (java/name).write_text((Path('buildsrc/v300')/name).read_text(encoding='utf-8'),encoding='utf-8')
(res/'layout/activity_morning.xml').write_text(Path('buildsrc/v300/activity_morning.xml').read_text(encoding='utf-8'),encoding='utf-8')
(res/'drawable/somnori_morning_card_background.xml').write_text('''<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android" android:shape="rectangle">
    <corners android:radius="24dp" />
    <gradient android:angle="0" android:startColor="#241C46" android:centerColor="#171735" android:endColor="#10132C" />
    <stroke android:width="1dp" android:color="#4A3E78" />
</shape>
''',encoding='utf-8')

# Register activity.
manifest=project/'app/src/main/AndroidManifest.xml'
m=manifest.read_text(encoding='utf-8')
needle='        <activity android:name=".ManualRecordActivity" android:exported="false" />'
if needle not in m: raise SystemExit('manifest insertion point missing')
m=m.replace(needle,needle+'\n        <activity android:name=".MorningActivity" android:exported="false" />',1)
manifest.write_text(m,encoding='utf-8')

# Add a clean Morning card to home between tonight plan and dream journal.
main=res/'layout/activity_main.xml'
tree=ET.parse(main); root=tree.getroot()
parent={c:p for p in root.iter() for c in p}
def by_id(view_id):
    for e in root.iter():
        if e.attrib.get(A('id'))==f'@+id/{view_id}': return e
    raise SystemExit(f'missing {view_id}')

dream=by_id('dashboardDreamCard')
p=parent[dream]; idx=list(p).index(dream)
morning=ET.fromstring('''<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android" xmlns:app="http://schemas.android.com/apk/res-auto"
    android:id="@+id/dashboardMorningCard"
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:layout_marginTop="10dp"
    android:background="@drawable/somnori_morning_card_background"
    android:clickable="true"
    android:focusable="true"
    android:gravity="center_vertical"
    android:orientation="horizontal"
    android:padding="15dp">
    <LinearLayout android:layout_width="0dp" android:layout_height="wrap_content" android:layout_weight="1" android:orientation="vertical">
        <TextView android:layout_width="match_parent" android:layout_height="wrap_content" android:text="Утро в Somnori" android:textColor="@color/qd_text" android:textSize="17sp" android:textStyle="bold" />
        <TextView android:id="@+id/dashboardMorningStatus" android:layout_width="match_parent" android:layout_height="wrap_content" android:layout_marginTop="4dp" android:maxLines="2" android:text="Сны и записи этой ночи будут ждать вас утром" android:textColor="@color/qd_on_night_muted" android:textSize="10.5sp" />
    </LinearLayout>
    <com.google.android.material.button.MaterialButton
        android:id="@+id/dashboardMorningButton"
        android:layout_width="wrap_content"
        android:layout_height="42dp"
        android:layout_marginStart="10dp"
        android:minWidth="0dp"
        android:minHeight="0dp"
        android:text="Открыть"
        android:textAllCaps="false"
        android:textColor="@color/qd_primary_dark"
        android:textSize="10.5sp"
        app:backgroundTint="@color/qd_primary"
        app:cornerRadius="18dp" />
</LinearLayout>''')
p.insert(idx,morning)
tree.write(main,encoding='utf-8',xml_declaration=True)

# Wire main dashboard.
activity=java/'MainActivity.java'
s=activity.read_text(encoding='utf-8')
needle='    private TextView dashboardDreamSnippet;'
if needle not in s: raise SystemExit('field insertion missing')
s=s.replace(needle,needle+'\n    private TextView dashboardMorningStatus;',1)
needle='        dashboardDreamSnippet = findViewById(R.id.dashboardDreamSnippet);'
if needle not in s: raise SystemExit('binding insertion missing')
s=s.replace(needle,needle+'\n        dashboardMorningStatus = findViewById(R.id.dashboardMorningStatus);',1)
needle='''        findViewById(R.id.dashboardDreamsButton).setOnClickListener(v ->
                startActivity(new Intent(this, DreamHubActivity.class)));'''
if needle not in s: raise SystemExit('listener insertion missing')
s=s.replace(needle,needle+'''\n        findViewById(R.id.dashboardMorningCard).setOnClickListener(v ->
                startActivity(new Intent(this, MorningActivity.class)));
        findViewById(R.id.dashboardMorningButton).setOnClickListener(v ->
                startActivity(new Intent(this, MorningActivity.class)));''',1)
needle='''        renderDashboardAlarm();
        renderServiceState();
    }

    private void renderMorningSummary() {'''
if needle not in s: raise SystemExit('render insertion missing')
replacement='''        renderDashboardAlarm();
        renderServiceState();
        renderMorningDashboard();
    }

    private void renderMorningDashboard() {
        if (dashboardMorningStatus == null) return;
        MorningTools.Summary data = MorningTools.latestSummary(this);
        if (data.session == null) {
            dashboardMorningStatus.setText("После первой ночи здесь появятся сохранённые сны и утренний разбор");
            return;
        }
        int left = Math.max(0, data.dreams - data.reviewedDreams);
        StringBuilder text = new StringBuilder();
        if (data.dreams > 0) text.append(data.dreams).append(" ").append(plural(data.dreams, "сон", "сна", "снов"));
        if (data.notes > 0) {
            if (text.length() > 0) text.append(" · ");
            text.append(data.notes).append(" ").append(plural(data.notes, "запись", "записи", "записей"));
        }
        if (text.length() == 0) text.append("Ночь сохранена");
        if (left > 0) text.append(" · разобрать ").append(left);
        else if (data.dreams > 0) text.append(" · разбор завершён");
        dashboardMorningStatus.setText(text.toString());
    }

    private void renderMorningSummary() {'''
s=s.replace(needle,replacement,1)
activity.write_text(s,encoding='utf-8')

# Validate XML and key invariants, including the 0.29.10 fixes that must survive Morning.
for pth in res.rglob('*.xml'): ET.parse(pth)
main_text=main.read_text(encoding='utf-8')
main_java=activity.read_text(encoding='utf-8')
assert 'MorningActivity' in manifest.read_text(encoding='utf-8')
assert 'dashboardMorningCard' in main_text
assert 'android:minHeight="246dp"' in main_text
assert 'if (serviceRunning) openNightAssistant();\n            else ensurePermissionsAndStart();' in main_java
assert 'SAFE_END_SILENCE_BLOCKS = 11' in (java/'AcousticWakeDetector.java').read_text(encoding='utf-8')
print('Somnori 0.30.0 Morning applied on top of 0.29.10')
