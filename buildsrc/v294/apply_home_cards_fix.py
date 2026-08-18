from pathlib import Path

root = Path('buildsrc/quiet-diary')
layout = root / 'app/src/main/res/layout/activity_main.xml'
gradle = root / 'app/build.gradle.kts'

x = layout.read_text(encoding='utf-8')
replacements = [
    (
        'android:id="@+id/dashboardPracticeCard"\n                    android:layout_width="0dp"\n                    android:layout_height="match_parent"',
        'android:id="@+id/dashboardPracticeCard"\n                    android:layout_width="0dp"\n                    android:layout_height="wrap_content"\n                    android:minHeight="178dp"'
    ),
    (
        'android:id="@+id/dashboardBeforeSleepCard"\n                    android:layout_width="0dp"\n                    android:layout_height="match_parent"',
        'android:id="@+id/dashboardBeforeSleepCard"\n                    android:layout_width="0dp"\n                    android:layout_height="wrap_content"\n                    android:minHeight="178dp"'
    ),
]
for old, new in replacements:
    if old not in x:
        raise SystemExit(f'Expected layout fragment not found: {old[:70]}')
    x = x.replace(old, new, 1)
layout.write_text(x, encoding='utf-8')

g = gradle.read_text(encoding='utf-8')
if 'versionCode = 2903' not in g or 'versionName = "0.29.3"' not in g:
    raise SystemExit('Expected 0.29.3 version markers not found')
g = g.replace('versionCode = 2903', 'versionCode = 2904', 1)
g = g.replace('versionName = "0.29.3"', 'versionName = "0.29.4"', 1)
gradle.write_text(g, encoding='utf-8')

# Strong guards for the exact physical-device regression.
check = layout.read_text(encoding='utf-8')
for card_id in ('dashboardPracticeCard', 'dashboardBeforeSleepCard'):
    marker = f'android:id="@+id/{card_id}"'
    pos = check.index(marker)
    block = check[pos:pos+360]
    assert 'android:layout_height="wrap_content"' in block, card_id
    assert 'android:minHeight="178dp"' in block, card_id
    assert 'android:layout_height="match_parent"' not in block, card_id

print('Somnori 0.29.4 home cards visibility fix: OK')
