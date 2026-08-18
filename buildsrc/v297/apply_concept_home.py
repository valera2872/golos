from pathlib import Path
import re
import xml.etree.ElementTree as ET

ANDROID = "http://schemas.android.com/apk/res/android"
APP = "http://schemas.android.com/apk/res-auto"
TOOLS = "http://schemas.android.com/tools"
ET.register_namespace("android", ANDROID)
ET.register_namespace("app", APP)
ET.register_namespace("tools", TOOLS)

project = Path("buildsrc/quiet-diary")
res = project / "app/src/main/res"
main_path = res / "layout/activity_main.xml"
nav_path = res / "layout/view_bottom_navigation.xml"
gradle_path = project / "app/build.gradle.kts"
ui_nav_path = project / "app/src/main/java/com/quietdiary/app/UiNavigation.java"

A = lambda name: f"{{{ANDROID}}}{name}"
P = lambda name: f"{{{APP}}}{name}"

old_main_text = main_path.read_text(encoding="utf-8")
old_ids = set(re.findall(r'@\+id/([A-Za-z0-9_]+)', old_main_text))

tree = ET.parse(main_path)
root = tree.getroot()
parent = {child: p for p in root.iter() for child in p}

def by_id(view_id):
    for e in root.iter():
        if e.attrib.get(A("id")) == f"@+id/{view_id}":
            return e
    raise RuntimeError(f"missing id {view_id}")

def by_attr(name, value):
    key = A(name)
    for e in root.iter():
        if e.attrib.get(key) == value:
            return e
    raise RuntimeError(f"missing {name}={value}")

def replace_by_id(view_id, xml):
    old = by_id(view_id)
    p = parent[old]
    idx = list(p).index(old)
    new = ET.fromstring(xml)
    p.remove(old)
    p.insert(idx, new)
    parent[new] = p
    for n in new.iter():
        for c in n:
            parent[c] = n
    return new

def set_attr(e, **attrs):
    for k, v in attrs.items():
        if k.startswith("app_"):
            e.set(P(k[4:]), str(v))
        else:
            e.set(A(k), str(v))

def text_views(e):
    for n in e.iter():
        if n.tag.endswith("TextView") or n.tag.endswith("MaterialButton"):
            yield n

# Version only. No product logic is touched.
gradle = gradle_path.read_text(encoding="utf-8")
gradle = gradle.replace("versionCode = 2906", "versionCode = 2907")
gradle = gradle.replace('versionName = "0.29.6"', 'versionName = "0.29.7"')
gradle_path.write_text(gradle, encoding="utf-8")

# Remove bitmap layers from card backgrounds. The same premium gradients/strokes remain;
# illustrations are placed as explicit safe-zone ImageViews in the layout.
for name in (
    "somnori_assistant_card_background",
    "somnori_practice_card_background",
    "somnori_sleep_card_background",
    "somnori_dream_card_background",
):
    p = res / "drawable" / f"{name}.xml"
    t = ET.parse(p)
    r = t.getroot()
    removed = 0
    for item in list(r):
        if any(node.tag.endswith("bitmap") for node in item.iter()):
            r.remove(item)
            removed += 1
    if removed < 1:
        raise RuntimeError(f"{name}: expected bitmap layer")
    t.write(p, encoding="utf-8", xml_declaration=True)

(res / "drawable/somnori_scene_left_fade.xml").write_text(
    '''<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android" android:shape="rectangle">
    <gradient
        android:angle="0"
        android:startColor="#FF11142E"
        android:centerColor="#B811142E"
        android:endColor="#0011142E" />
</shape>
''',
    encoding="utf-8",
)

# Header: same approved artwork, but concept proportions.
header = by_attr("background", "@drawable/somnori_brand_header_background")
set_attr(header, layout_height="126dp")
moon = by_attr("src", "@drawable/somnori_header_moon")
set_attr(moon, layout_width="142dp", layout_height="126dp")
wordmark = by_attr("src", "@drawable/somnori_wordmark")
set_attr(wordmark, layout_width="174dp", layout_height="42dp")
daypart = next(e for e in root.iter() if e.attrib.get(A("text")) == "Вечер  •  Ночь  •  Утро")
set_attr(daypart, textSize="12sp")
help_btn = by_id("openHelpButton")
set_attr(help_btn, layout_width="36dp", layout_height="36dp", minWidth="0dp", minHeight="0dp")
settings_btn = by_id("openSettingsButton")
set_attr(settings_btn, layout_width="36dp", layout_height="36dp", minWidth="0dp", minHeight="0dp")

# Compact central prompt and quick actions.
prompt = next(e for e in root.iter() if e.attrib.get(A("text")) == "Что вы хотите сделать?")
set_attr(prompt, textSize="18sp", gravity="center", layout_marginTop="12dp", layout_marginBottom="8dp")
for vid, text in (
    ("quickRecordThoughtButton", "Записать мысль"),
    ("quickRecordDreamButton", "Записать сон"),
):
    b = by_id(vid)
    set_attr(
        b,
        textSize="13sp",
        minHeight="56dp",
        minWidth="0dp",
        app_insetTop="0dp",
        app_insetBottom="0dp",
    )
    b.set(A("text"), text)

assistant_xml = r'''
<FrameLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:id="@+id/dashboardNightCard"
    android:layout_width="match_parent"
    android:layout_height="214dp"
    android:layout_marginTop="12dp"
    android:background="@drawable/somnori_assistant_card_background"
    android:clickable="true"
    android:focusable="true"
    android:padding="16dp">

    <ImageView
        android:layout_width="158dp"
        android:layout_height="196dp"
        android:layout_gravity="end|bottom"
        android:alpha="0.95"
        android:contentDescription="@null"
        android:scaleType="centerCrop"
        android:src="@drawable/somnori_assistant_scene" />

    <View
        android:layout_width="58dp"
        android:layout_height="196dp"
        android:layout_gravity="end|bottom"
        android:layout_marginEnd="112dp"
        android:background="@drawable/somnori_scene_left_fade" />

    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="match_parent"
        android:orientation="vertical"
        android:paddingEnd="136dp">

        <TextView
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:maxLines="3"
            android:text="Бесконтактный ночной помощник"
            android:textColor="#FFF9FF"
            android:textSize="17sp"
            android:textStyle="bold" />

        <TextView
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:layout_marginTop="5dp"
            android:maxLines="2"
            android:text="Голосом — без касания телефона"
            android:textColor="#D59AFF"
            android:textSize="13sp"
            android:textStyle="bold" />

        <TextView
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:layout_marginTop="8dp"
            android:maxLines="2"
            android:text="Запись мыслей и снов • время • будильник"
            android:textColor="#BDB6D7"
            android:textSize="10.5sp" />

        <Space
            android:layout_width="1dp"
            android:layout_height="0dp"
            android:layout_weight="1" />

        <TextView
            android:id="@+id/dashboardNightStatus"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:maxLines="2"
            android:text="Готов"
            android:textColor="#6CF0BC"
            android:textSize="10.5sp"
            android:textStyle="bold" />

        <LinearLayout
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:layout_marginTop="7dp"
            android:gravity="start|center_vertical"
            android:orientation="horizontal">

            <com.google.android.material.button.MaterialButton
                android:id="@+id/dashboardNightButton"
                android:layout_width="wrap_content"
                android:layout_height="42dp"
                android:minWidth="82dp"
                android:minHeight="0dp"
                android:text="Включить"
                android:textAllCaps="false"
                android:textSize="11sp"
                app:cornerRadius="21dp"
                app:insetBottom="0dp"
                app:insetTop="0dp"
                app:strokeColor="#526CF0BC"
                app:strokeWidth="1dp" />

            <com.google.android.material.button.MaterialButton
                android:id="@+id/dashboardAlarmVoiceButton"
                android:layout_width="wrap_content"
                android:layout_height="40dp"
                android:layout_marginStart="4dp"
                android:minWidth="0dp"
                android:minHeight="0dp"
                android:text="Голос"
                android:textAllCaps="false"
                android:textColor="#BDB6D7"
                android:textSize="10sp"
                app:backgroundTint="@android:color/transparent"
                app:insetBottom="0dp"
                app:insetTop="0dp"
                app:strokeWidth="0dp" />
        </LinearLayout>
    </LinearLayout>
</FrameLayout>
'''
replace_by_id("dashboardNightCard", assistant_xml)

practice_xml = r'''
<FrameLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:id="@+id/dashboardPracticeCard"
    android:layout_width="0dp"
    android:layout_height="184dp"
    android:layout_weight="1"
    android:layout_marginEnd="5dp"
    android:background="@drawable/somnori_practice_card_background"
    android:clickable="true"
    android:focusable="true"
    android:padding="14dp">

    <ImageView
        android:layout_width="84dp"
        android:layout_height="78dp"
        android:layout_gravity="end|bottom"
        android:alpha="0.88"
        android:contentDescription="@null"
        android:scaleType="centerCrop"
        android:src="@drawable/somnori_practice_scene" />

    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="match_parent"
        android:orientation="vertical"
        android:paddingBottom="70dp">

        <TextView
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:text="◎  Практики"
            android:textColor="#FFF9FF"
            android:textSize="15sp"
            android:textStyle="bold" />

        <TextView
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:layout_marginTop="7dp"
            android:maxLines="3"
            android:text="Настройтесь на то, с чем хотите войти в ночь"
            android:textColor="#DED8EE"
            android:textSize="10.5sp" />

        <TextView
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:layout_marginTop="6dp"
            android:maxLines="3"
            android:text="Самовнушение • намерение • техники сна"
            android:textColor="#B8AED4"
            android:textSize="9.5sp" />
    </LinearLayout>

    <TextView
        android:id="@+id/dashboardPracticeStatus"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_gravity="bottom"
        android:paddingEnd="82dp"
        android:maxLines="2"
        android:text="Сегодня: не выбрано"
        android:textColor="#D6C8FF"
        android:textSize="9.5sp" />

    <com.google.android.material.button.MaterialButton
        android:id="@+id/dashboardPracticeButton"
        android:layout_width="1dp"
        android:layout_height="1dp"
        android:visibility="invisible"
        android:text="Открыть" />
</FrameLayout>
'''
replace_by_id("dashboardPracticeCard", practice_xml)

sleep_xml = r'''
<FrameLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:id="@+id/dashboardBeforeSleepCard"
    android:layout_width="0dp"
    android:layout_height="184dp"
    android:layout_weight="1"
    android:layout_marginStart="5dp"
    android:background="@drawable/somnori_sleep_card_background"
    android:clickable="true"
    android:focusable="true"
    android:padding="14dp">

    <ImageView
        android:layout_width="86dp"
        android:layout_height="78dp"
        android:layout_gravity="end|bottom"
        android:alpha="0.88"
        android:contentDescription="@null"
        android:scaleType="centerCrop"
        android:src="@drawable/somnori_sleep_scene" />

    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="match_parent"
        android:orientation="vertical"
        android:paddingBottom="70dp">

        <TextView
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:text="♫  Перед сном"
            android:textColor="#FFF9FF"
            android:textSize="15sp"
            android:textStyle="bold" />

        <TextView
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:layout_marginTop="7dp"
            android:maxLines="3"
            android:text="Выберите, с чем хотите заснуть"
            android:textColor="#DED8EE"
            android:textSize="10.5sp" />

        <TextView
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:layout_marginTop="6dp"
            android:maxLines="3"
            android:text="Музыка • природа • истории • ночная программа"
            android:textColor="#B8AED4"
            android:textSize="9.5sp" />
    </LinearLayout>

    <TextView
        android:id="@+id/dashboardBeforeSleepStatus"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_gravity="bottom"
        android:paddingEnd="82dp"
        android:maxLines="2"
        android:text="Сегодня: не выбрано"
        android:textColor="#C6D4FF"
        android:textSize="9.5sp" />

    <com.google.android.material.button.MaterialButton
        android:id="@+id/dashboardNightProgramButton"
        android:layout_width="1dp"
        android:layout_height="1dp"
        android:visibility="invisible"
        android:text="Открыть" />
</FrameLayout>
'''
replace_by_id("dashboardBeforeSleepCard", sleep_xml)

dream_xml = r'''
<FrameLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:id="@+id/dashboardDreamCard"
    android:layout_width="match_parent"
    android:layout_height="152dp"
    android:layout_marginTop="10dp"
    android:background="@drawable/somnori_dream_card_background"
    android:clickable="true"
    android:focusable="true"
    android:padding="15dp">

    <ImageView
        android:layout_width="132dp"
        android:layout_height="104dp"
        android:layout_gravity="end|top"
        android:alpha="0.92"
        android:contentDescription="@null"
        android:scaleType="centerCrop"
        android:src="@drawable/somnori_dream_scene" />

    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="match_parent"
        android:orientation="vertical"
        android:paddingEnd="124dp">

        <TextView
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:text="Мои сны"
            android:textColor="#FFF9FF"
            android:textSize="17sp"
            android:textStyle="bold" />

        <TextView
            android:id="@+id/dashboardDreamSummary"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:layout_marginTop="3dp"
            android:maxLines="1"
            android:ellipsize="end"
            android:text="0 записей"
            android:textColor="#BDB6D7"
            android:textSize="10sp" />

        <TextView
            android:id="@+id/dashboardDreamSnippet"
            android:layout_width="match_parent"
            android:layout_height="0dp"
            android:layout_marginTop="8dp"
            android:layout_weight="1"
            android:ellipsize="end"
            android:maxLines="3"
            android:text="Сны, которые вы сохранили ночью, появятся здесь."
            android:textColor="#D7D0EA"
            android:textSize="10.5sp" />
    </LinearLayout>

    <com.google.android.material.button.MaterialButton
        android:id="@+id/dashboardDreamsButton"
        android:layout_width="118dp"
        android:layout_height="40dp"
        android:layout_gravity="end|bottom"
        android:minHeight="0dp"
        android:text="Открыть дневник"
        android:textAllCaps="false"
        android:textSize="10sp"
        app:cornerRadius="20dp"
        app:insetBottom="0dp"
        app:insetTop="0dp" />
</FrameLayout>
'''
replace_by_id("dashboardDreamCard", dream_xml)

# Smart alarm: preserve exact IDs and behavior, only compress it.
alarm = by_id("dashboardAlarmBanner")
set_attr(alarm, minHeight="76dp", padding="13dp", layout_marginTop="10dp")
for n in alarm.iter():
    txt = n.attrib.get(A("text"), "")
    vid = n.attrib.get(A("id"), "")
    if txt == "Умный будильник":
        set_attr(n, textSize="15sp")
    elif "dashboardAlarmBannerStatus" in vid:
        set_attr(n, textSize="10.5sp", maxLines="2")
    elif "Установить" in txt and "голос" in txt:
        set_attr(n, visibility="gone")
    elif n.tag.endswith("MaterialButton"):
        set_attr(n, textSize="10.5sp", minHeight="40dp", minWidth="88dp", app_insetTop="0dp", app_insetBottom="0dp")

# Tonight: existing functional row structure is good; use concept density.
tonight = by_id("dashboardTonightCard")
set_attr(tonight, padding="16dp", layout_marginTop="10dp")
for n in text_views(tonight):
    txt = n.attrib.get(A("text"), "")
    vid = n.attrib.get(A("id"), "")
    if txt == "Сегодня ночью":
        set_attr(n, textSize="18sp")
    elif "dashboardStartNightButton" in vid:
        set_attr(n, textSize="12sp", minHeight="48dp", app_insetTop="0dp", app_insetBottom="0dp")
    elif n.tag.endswith("MaterialButton"):
        set_attr(n, textSize="10.5sp", minHeight="38dp", app_insetTop="0dp", app_insetBottom="0dp")
    else:
        set_attr(n, textSize="10.5sp")

# Onboarding: compact strip like the concept.
onboarding_button = by_id("dashboardOnboardingButton")
onboarding_parent = parent[onboarding_button]
set_attr(onboarding_parent, padding="12dp", layout_marginTop="10dp")
for n in text_views(onboarding_parent):
    txt = n.attrib.get(A("text"), "")
    if txt == "Впервые в Somnori?":
        set_attr(n, textSize="15sp")
    elif n is onboarding_button:
        set_attr(n, textSize="10.5sp", minHeight="40dp", app_insetTop="0dp", app_insetBottom="0dp")
    else:
        set_attr(n, textSize="10sp")

tree.write(main_path, encoding="utf-8", xml_declaration=True)

# Concept-like compact bottom nav. Preserve icons, IDs and destinations from 0.29.6.
nav_tree = ET.parse(nav_path)
nav_root = nav_tree.getroot()
set_attr(nav_root, layout_height="68dp", paddingStart="5dp", paddingEnd="5dp", paddingTop="3dp", paddingBottom="3dp")
for b in list(nav_root):
    set_attr(
        b,
        layout_height="match_parent",
        minWidth="0dp",
        minHeight="0dp",
        textSize="9.5sp",
        app_backgroundTint="@android:color/transparent",
        app_cornerRadius="0dp",
        app_iconPadding="2dp",
        app_iconSize="18dp",
        app_insetTop="0dp",
        app_insetBottom="0dp",
        app_strokeWidth="0dp",
    )
nav_tree.write(nav_path, encoding="utf-8", xml_declaration=True)

# Remove the selected "tile" from UiNavigation; selection is communicated by text/icon color + weight.
ui_nav = ui_nav_path.read_text(encoding="utf-8")
needle = "int background = selected ? R.color.qd_nav_selected : android.R.color.transparent;"
if needle not in ui_nav:
    raise RuntimeError("UiNavigation selected background line not found")
ui_nav = ui_nav.replace(needle, "int background = android.R.color.transparent;")
ui_nav_path.write_text(ui_nav, encoding="utf-8")

# Validate: never lose an existing MainActivity view ID while re-composing the dashboard.
new_main_text = main_path.read_text(encoding="utf-8")
new_ids = set(re.findall(r'@\+id/([A-Za-z0-9_]+)', new_main_text))
missing = sorted(old_ids - new_ids)
if missing:
    raise RuntimeError("dashboard rewrite lost ids: " + ", ".join(missing))

for p in res.rglob("*.xml"):
    ET.parse(p)

for needle in (
    "somnori_assistant_scene",
    "somnori_practice_scene",
    "somnori_sleep_scene",
    "somnori_dream_scene",
    "paddingEnd=\"136dp\"",
    "Бесконтактный ночной помощник",
):
    if needle not in new_main_text:
        raise RuntimeError(f"missing visual guard {needle}")

for name in (
    "somnori_assistant_card_background",
    "somnori_practice_card_background",
    "somnori_sleep_card_background",
    "somnori_dream_card_background",
):
    s = (res / "drawable" / f"{name}.xml").read_text(encoding="utf-8")
    if "<bitmap" in s:
        raise RuntimeError(f"{name}: bitmap still embedded under text")

print(f"Somnori 0.29.7 concept-home patch OK; preserved {len(old_ids)} existing main IDs")
