from pathlib import Path
import xml.etree.ElementTree as ET

ANDROID='http://schemas.android.com/apk/res/android'
APP='http://schemas.android.com/apk/res-auto'
ET.register_namespace('android',ANDROID); ET.register_namespace('app',APP)
A=lambda n:f'{{{ANDROID}}}{n}'

path=Path('buildsrc/quiet-diary/app/src/main/res/layout/activity_main.xml')
tree=ET.parse(path); root=tree.getroot()
parent={c:p for p in root.iter() for c in p}
for e in root.iter():
    text=e.attrib.get(A('text'),'')
    if 'БЕСКОНТАКТНЫЙ' in text and 'Ночной помощник' in text:
        p=parent[e]; idx=list(p).index(e)
        e.set(A('text'),'БЕСКОНТАКТНЫЙ')
        e.set(A('textSize'),'9sp')
        e.set(A('maxLines'),'1')
        e.set(A('letterSpacing'),'0.12')
        e.set(A('textColor'),'#C9A7FF')
        e.set(A('textStyle'),'bold')
        title=ET.fromstring('''<TextView xmlns:android="http://schemas.android.com/apk/res/android"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:layout_marginTop="3dp"
            android:maxLines="2"
            android:text="Ночной помощник"
            android:textColor="#FFF9FF"
            android:textSize="18sp"
            android:textStyle="bold" />''')
        p.insert(idx+1,title)
        break
else:
    raise SystemExit('combined hero title not found')
tree.write(path,encoding='utf-8',xml_declaration=True)
x=path.read_text(encoding='utf-8')
assert 'android:text="БЕСКОНТАКТНЫЙ"' in x
assert 'android:text="Ночной помощник"' in x
print('Hero title hierarchy refined')
