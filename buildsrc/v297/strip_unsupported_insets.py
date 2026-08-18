from pathlib import Path
import xml.etree.ElementTree as ET

APP = "http://schemas.android.com/apk/res-auto"
ANDROID = "http://schemas.android.com/apk/res/android"
TOOLS = "http://schemas.android.com/tools"
ET.register_namespace("android", ANDROID)
ET.register_namespace("app", APP)
ET.register_namespace("tools", TOOLS)

root = Path("buildsrc/quiet-diary/app/src/main/res/layout")
keys = {f"{{{APP}}}insetTop", f"{{{APP}}}insetBottom"}
removed = 0
for name in ("activity_main.xml", "view_bottom_navigation.xml"):
    path = root / name
    tree = ET.parse(path)
    for node in tree.getroot().iter():
        for key in list(node.attrib):
            if key in keys:
                del node.attrib[key]
                removed += 1
    tree.write(path, encoding="utf-8", xml_declaration=True)

if removed < 1:
    raise RuntimeError("Expected unsupported inset attributes were not found")
print(f"Removed {removed} unsupported MaterialButton inset attributes")
