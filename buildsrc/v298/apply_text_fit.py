from pathlib import Path
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
gradle_path = project / "app/build.gradle.kts"

A = lambda name: f"{{{ANDROID}}}{name}"

# Version only; product/night logic remains untouched.
gradle = gradle_path.read_text(encoding="utf-8")
if 'versionCode = 2907' not in gradle or 'versionName = "0.29.7"' not in gradle:
    raise RuntimeError("Expected 0.29.7 base")
gradle = gradle.replace("versionCode = 2907", "versionCode = 2908")
gradle = gradle.replace('versionName = "0.29.7"', 'versionName = "0.29.8"')
gradle_path.write_text(gradle, encoding="utf-8")

# A small, concept-like status strip for the two compact cards.
(res / "drawable/somnori_mini_status_pill.xml").write_text(
    '''<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android" android:shape="rectangle">
    <solid android:color="#2A29335A" />
    <stroke android:width="1dp" android:color="#354E5E92" />
    <corners android:radius="11dp" />
</shape>
''',
    encoding="utf-8",
)

tree = ET.parse(main_path)
root = tree.getroot()

def by_id(view_id):
    target = f"@+id/{view_id}"
    for node in root.iter():
        if node.attrib.get(A("id")) == target:
            return node
    raise RuntimeError(f"missing id {view_id}")

def by_src(src):
    for node in root.iter():
        if node.attrib.get(A("src")) == src:
            return node
    raise RuntimeError(f"missing src {src}")

def set_a(node, **attrs):
    for key, value in attrs.items():
        node.set(A(key), str(value))

for card_id, status_id, scene in (
    ("dashboardPracticeCard", "dashboardPracticeStatus", "@drawable/somnori_practice_scene"),
    ("dashboardBeforeSleepCard", "dashboardBeforeSleepStatus", "@drawable/somnori_sleep_scene"),
):
    card = by_id(card_id)
    set_a(card, layout_height="202dp")

    scene_view = by_src(scene)
    set_a(
        scene_view,
        layout_width="76dp",
        layout_height="68dp",
        layout_marginBottom="40dp",
        alpha="0.84",
    )

    # The direct vertical text column used 70dp bottom padding in 0.29.7,
    # which left too little room on a real 360dp phone. Keep the same
    # composition but give the copy enough vertical space.
    text_column = None
    for child in card:
        if child.tag.endswith("LinearLayout") and child.attrib.get(A("orientation")) == "vertical":
            text_column = child
            break
    if text_column is None:
        raise RuntimeError(f"{card_id}: text column missing")
    set_a(text_column, paddingBottom="50dp")

    text_children = [c for c in list(text_column) if c.tag.endswith("TextView")]
    if len(text_children) < 3:
        raise RuntimeError(f"{card_id}: expected title + two copy lines")
    # Keep title size; slightly tighten body text only where necessary.
    set_a(text_children[1], textSize="10sp", maxLines="3")
    set_a(text_children[2], textSize="8.8sp", maxLines="2")

    status = by_id(status_id)
    # Critical 0.29.7 bug: paddingEnd=82dp squeezed dynamic labels into a
    # tiny column ("Выбрат / ь прак", "Выбрат / ь звуч"). Give the status
    # the full card width and a fixed two-line-safe strip.
    status.attrib.pop(A("paddingEnd"), None)
    set_a(
        status,
        layout_height="38dp",
        paddingStart="9dp",
        paddingEnd="9dp",
        gravity="center_vertical",
        maxLines="2",
        textSize="8.8sp",
        background="@drawable/somnori_mini_status_pill",
    )

# Parse all XML after writing and guard the exact regression.
tree.write(main_path, encoding="utf-8", xml_declaration=True)
for p in res.rglob("*.xml"):
    ET.parse(p)

main = main_path.read_text(encoding="utf-8")
for expected in (
    'android:id="@+id/dashboardPracticeCard"',
    'android:id="@+id/dashboardBeforeSleepCard"',
    'android:id="@+id/dashboardPracticeStatus"',
    'android:id="@+id/dashboardBeforeSleepStatus"',
    'android:layout_height="202dp"',
    'android:background="@drawable/somnori_mini_status_pill"',
):
    if expected not in main:
        raise RuntimeError(f"missing 0.29.8 UI guard: {expected}")

# Specifically forbid the 0.29.7 squeeze that caused the screenshots.
for status_id in ("dashboardPracticeStatus", "dashboardBeforeSleepStatus"):
    pos = main.index(f'android:id="@+id/{status_id}"')
    block = main[pos:pos+650]
    if 'android:paddingEnd="82dp"' in block:
        raise RuntimeError(f"{status_id}: old clipping padding survived")

print("Somnori 0.29.8 compact-card text-fit patch: OK")
