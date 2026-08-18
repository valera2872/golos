from pathlib import Path
import xml.etree.ElementTree as ET

ANDROID='http://schemas.android.com/apk/res/android'
ET.register_namespace('android', ANDROID)
A=lambda n:f'{{{ANDROID}}}{n}'

project=Path('buildsrc/quiet-diary')
main=project/'app/src/main/res/layout/activity_main.xml'
gradle=project/'app/build.gradle.kts'
main_activity=project/'app/src/main/java/com/quietdiary/app/MainActivity.java'

# 0.29.9 -> 0.29.10 hotfix
g=gradle.read_text(encoding='utf-8')
if 'versionCode = 2909' not in g or 'versionName = "0.29.9"' not in g:
    raise SystemExit('expected 0.29.9 base')
g=g.replace('versionCode = 2909','versionCode = 2910').replace('versionName = "0.29.9"','versionName = "0.29.10"')
gradle.write_text(g,encoding='utf-8')

tree=ET.parse(main)
root=tree.getroot()

def by_id(view_id):
    for e in root.iter():
        if e.attrib.get(A('id'))==f'@+id/{view_id}': return e
    raise SystemExit(f'missing {view_id}')

night=by_id('dashboardNightCard')
# Never clip hero content on devices with larger system font scale.
night.set(A('layout_height'),'wrap_content')
night.set(A('minHeight'),'246dp')
night.set(A('clickable'),'true')
night.set(A('focusable'),'true')

# Locate the main vertical text/CTA column inside the hero.
column=None
for child in list(night):
    if child.tag.endswith('LinearLayout') and child.attrib.get(A('orientation'))=='vertical':
        column=child
        break
if column is None:
    raise SystemExit('night hero column missing')
column.set(A('layout_height'),'wrap_content')
column.set(A('minHeight'),'214dp')
column.set(A('paddingEnd'),'122dp')

# Weighted spacer caused the CTA/status area to be pushed outside a fixed-height card.
# Replace it with a small deterministic gap so wrap_content can measure correctly.
for child in list(column):
    if child.tag.endswith('Space'):
        child.attrib.pop(A('layout_weight'),None)
        child.set(A('layout_height'),'8dp')

# Give body copy enough lines at real Xiaomi font scaling.
for e in column.iter():
    text=e.attrib.get(A('text'),'')
    if text=='Голосом — без касания телефона':
        e.set(A('maxLines'),'3')
        e.set(A('textSize'),'12.5sp')
    elif text=='Запись мыслей и снов • время • будильник':
        e.set(A('maxLines'),'3')
    elif e.attrib.get(A('id'))=='@+id/dashboardNightStatus':
        e.set(A('maxLines'),'3')

# Keep the artwork in the right zone and vertically centered as the card grows.
for child in list(night):
    src=child.attrib.get(A('src'),'')
    bg=child.attrib.get(A('background'),'')
    if src=='@drawable/somnori_assistant_scene':
        child.set(A('layout_width'),'148dp')
        child.set(A('layout_height'),'204dp')
        child.set(A('layout_gravity'),'end|center_vertical')
    elif bg=='@drawable/somnori_scene_left_fade':
        child.set(A('layout_height'),'204dp')
        child.set(A('layout_gravity'),'end|center_vertical')
        child.set(A('layout_marginEnd'),'104dp')

tree.write(main,encoding='utf-8',xml_declaration=True)

# Functional bug: the whole card previously did nothing while night mode was OFF.
s=main_activity.read_text(encoding='utf-8')
old='''        findViewById(R.id.dashboardNightCard).setOnClickListener(v -> {\n            if (serviceRunning) openNightAssistant();\n        });'''
new='''        findViewById(R.id.dashboardNightCard).setOnClickListener(v -> {\n            if (serviceRunning) openNightAssistant();\n            else ensurePermissionsAndStart();\n        });'''
if old not in s:
    raise SystemExit('dashboardNightCard click listener pattern not found')
s=s.replace(old,new,1)
main_activity.write_text(s,encoding='utf-8')

# Regression guards.
x=main.read_text(encoding='utf-8')
assert 'android:layout_height="wrap_content"' in x
assert 'android:minHeight="246dp"' in x
assert 'somnori_assistant_scene' in x
assert 'somnori_practice_scene' not in x
assert 'somnori_sleep_scene' not in x
m=main_activity.read_text(encoding='utf-8')
assert 'if (serviceRunning) openNightAssistant();\n            else ensurePermissionsAndStart();' in m
assert 'SAFE_END_SILENCE_BLOCKS = 11' in (project/'app/src/main/java/com/quietdiary/app/AcousticWakeDetector.java').read_text(encoding='utf-8')
print('Somnori 0.29.10 hero click/clip hotfix applied')
