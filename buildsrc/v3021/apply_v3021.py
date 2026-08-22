from pathlib import Path

ROOT = Path('buildsrc/quiet-diary')

practice = ROOT / 'app/src/main/res/layout/activity_practice_hub.xml'
practice.write_text(r'''<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android" xmlns:app="http://schemas.android.com/apk/res-auto" android:layout_width="match_parent" android:layout_height="match_parent" android:background="@drawable/main_background" android:orientation="vertical">
<ScrollView android:layout_width="match_parent" android:layout_height="0dp" android:layout_weight="1" android:fillViewport="true" android:overScrollMode="never">
<LinearLayout android:layout_width="match_parent" android:layout_height="wrap_content" android:orientation="vertical" android:paddingStart="18dp" android:paddingTop="16dp" android:paddingEnd="18dp" android:paddingBottom="30dp">
    <LinearLayout android:layout_width="match_parent" android:layout_height="wrap_content" android:gravity="center_vertical" android:orientation="horizontal">
        <LinearLayout android:layout_width="0dp" android:layout_height="wrap_content" android:layout_weight="1" android:orientation="vertical">
            <TextView android:layout_width="wrap_content" android:layout_height="wrap_content" android:letterSpacing="0.14" android:text="SOMNORI · ПРАКТИКИ" android:textColor="@color/qd_primary" android:textSize="9sp" android:textStyle="bold"/>
            <TextView android:layout_width="match_parent" android:layout_height="wrap_content" android:layout_marginTop="5dp" android:text="Как войти в эту ночь?" android:textColor="@color/qd_text" android:textSize="29sp" android:textStyle="bold"/>
            <TextView android:layout_width="match_parent" android:layout_height="wrap_content" android:layout_marginTop="5dp" android:text="Музыка, фраза, практика или готовый сценарий — выберите одно действие." android:textColor="@color/qd_muted" android:textSize="13sp"/>
        </LinearLayout>
        <com.google.android.material.button.MaterialButton android:id="@+id/practiceSettingsButton" android:layout_width="44dp" android:layout_height="wrap_content" android:minHeight="44dp" android:contentDescription="Настройки" android:insetLeft="0dp" android:insetRight="0dp" android:minWidth="0dp" android:text="" app:icon="@drawable/ic_settings" app:iconPadding="0dp" app:iconSize="20dp"/>
    </LinearLayout>

    <FrameLayout android:id="@+id/practiceNightProgramCard" android:layout_width="match_parent" android:layout_height="wrap_content" android:minHeight="214dp" android:layout_marginTop="18dp" android:background="@drawable/premium_header_background" android:clickable="true" android:focusable="true">
        <ImageView android:layout_width="136dp" android:layout_height="match_parent" android:layout_gravity="end" android:alpha="0.84" android:contentDescription="" android:scaleType="centerCrop" android:src="@drawable/somnori_practice_scene"/>
        <LinearLayout android:layout_width="match_parent" android:layout_height="wrap_content" android:orientation="vertical" android:paddingStart="20dp" android:paddingTop="20dp" android:paddingEnd="126dp" android:paddingBottom="20dp">
            <TextView android:layout_width="wrap_content" android:layout_height="wrap_content" android:background="@drawable/night_chip_background" android:text="МОЯ НОЧЬ" android:textColor="@color/qd_on_night" android:textSize="9sp" android:textStyle="bold"/>
            <TextView android:layout_width="match_parent" android:layout_height="wrap_content" android:layout_marginTop="13dp" android:maxLines="2" android:text="Собрать\nсценарий" android:textColor="@color/qd_on_night" android:textSize="24sp" android:textStyle="bold"/>
            <TextView android:layout_width="match_parent" android:layout_height="wrap_content" android:layout_marginTop="7dp" android:maxLines="2" android:text="Музыка → фраза → ночной режим" android:textColor="@color/qd_on_night_muted" android:textSize="12sp"/>
            <TextView android:layout_width="match_parent" android:layout_height="wrap_content" android:layout_marginTop="13dp" android:text="Настроить ночь  →" android:textColor="@color/qd_primary" android:textSize="14sp" android:textStyle="bold"/>
        </LinearLayout>
    </FrameLayout>

    <LinearLayout android:id="@+id/practiceMusicCard" android:layout_width="match_parent" android:layout_height="wrap_content" android:minHeight="126dp" android:layout_marginTop="12dp" android:background="@drawable/premium_showcase_blue" android:clickable="true" android:focusable="true" android:gravity="center_vertical" android:orientation="horizontal" android:padding="16dp">
        <ImageView android:layout_width="42dp" android:layout_height="42dp" android:background="@drawable/orb_background" android:padding="10dp" android:src="@drawable/ic_music" android:tint="@color/qd_time"/>
        <LinearLayout android:layout_width="0dp" android:layout_height="wrap_content" android:layout_marginStart="14dp" android:layout_weight="1" android:orientation="vertical">
            <TextView android:layout_width="match_parent" android:layout_height="wrap_content" android:maxLines="1" android:text="Музыка" android:textColor="@color/qd_text" android:textSize="21sp" android:textStyle="bold"/>
            <TextView android:layout_width="match_parent" android:layout_height="wrap_content" android:layout_marginTop="4dp" android:maxLines="2" android:text="Три встроенные мелодии для спокойного засыпания." android:textColor="@color/qd_muted" android:textSize="12sp"/>
            <TextView android:layout_width="match_parent" android:layout_height="wrap_content" android:layout_marginTop="8dp" android:text="Открыть  →" android:textColor="@color/qd_time" android:textSize="13sp" android:textStyle="bold"/>
        </LinearLayout>
    </LinearLayout>

    <LinearLayout android:id="@+id/practiceSuggestionCard" android:layout_width="match_parent" android:layout_height="wrap_content" android:minHeight="126dp" android:layout_marginTop="10dp" android:background="@drawable/premium_showcase_warm" android:clickable="true" android:focusable="true" android:gravity="center_vertical" android:orientation="horizontal" android:padding="16dp">
        <ImageView android:layout_width="42dp" android:layout_height="42dp" android:background="@drawable/orb_background" android:padding="10dp" android:src="@drawable/ic_practice" android:tint="@color/qd_practice"/>
        <LinearLayout android:layout_width="0dp" android:layout_height="wrap_content" android:layout_marginStart="14dp" android:layout_weight="1" android:orientation="vertical">
            <TextView android:layout_width="match_parent" android:layout_height="wrap_content" android:maxLines="2" android:text="Самовнушение" android:textColor="@color/qd_text" android:textSize="21sp" android:textStyle="bold"/>
            <TextView android:layout_width="match_parent" android:layout_height="wrap_content" android:layout_marginTop="4dp" android:maxLines="2" android:text="Своя фраза для сна и ночного настроя." android:textColor="@color/qd_muted" android:textSize="12sp"/>
            <TextView android:layout_width="match_parent" android:layout_height="wrap_content" android:layout_marginTop="8dp" android:text="Настроить  →" android:textColor="@color/qd_practice" android:textSize="13sp" android:textStyle="bold"/>
        </LinearLayout>
    </LinearLayout>

    <LinearLayout android:id="@+id/practiceWakeCard" android:layout_width="match_parent" android:layout_height="wrap_content" android:layout_marginTop="12dp" android:background="@drawable/dream_card_background" android:clickable="true" android:focusable="true" android:gravity="center_vertical" android:orientation="horizontal">
        <ImageView android:layout_width="46dp" android:layout_height="46dp" android:background="@drawable/orb_background" android:padding="12dp" android:src="@drawable/ic_time" android:tint="@color/qd_dream"/>
        <LinearLayout android:layout_width="0dp" android:layout_height="wrap_content" android:layout_marginStart="14dp" android:layout_weight="1" android:orientation="vertical">
            <TextView android:layout_width="match_parent" android:layout_height="wrap_content" android:maxLines="2" android:text="Как я хочу проснуться" android:textColor="@color/qd_text" android:textSize="20sp" android:textStyle="bold"/>
            <TextView android:layout_width="match_parent" android:layout_height="wrap_content" android:layout_marginTop="5dp" android:maxLines="3" android:text="Время, мягкий сигнал и то, что услышать после него." android:textColor="@color/qd_muted" android:textSize="12sp"/>
        </LinearLayout>
        <TextView android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="→" android:textColor="@color/qd_dream" android:textSize="20sp"/>
    </LinearLayout>

    <LinearLayout android:id="@+id/practiceSleepHelpCard" android:layout_width="match_parent" android:layout_height="wrap_content" android:layout_marginTop="12dp" android:background="@drawable/surface_glass_background" android:clickable="true" android:focusable="true" android:orientation="vertical">
        <TextView android:layout_width="wrap_content" android:layout_height="wrap_content" android:background="@drawable/chip_background" android:text="СЕЙЧАС" android:textColor="@color/qd_primary" android:textSize="9sp" android:textStyle="bold"/>
        <TextView android:layout_width="match_parent" android:layout_height="wrap_content" android:layout_marginTop="9dp" android:text="Не могу заснуть" android:textColor="@color/qd_text" android:textSize="20sp" android:textStyle="bold"/>
        <TextView android:layout_width="match_parent" android:layout_height="wrap_content" android:layout_marginTop="5dp" android:text="Короткий подбор последовательности именно на эту ночь." android:textColor="@color/qd_muted" android:textSize="12sp"/>
    </LinearLayout>

    <TextView android:layout_width="match_parent" android:layout_height="wrap_content" android:layout_marginTop="24dp" android:text="Ещё практики" android:textColor="@color/qd_text" android:textSize="18sp" android:textStyle="bold"/>
    <LinearLayout android:id="@+id/practiceRelaxCard" android:layout_width="match_parent" android:layout_height="wrap_content" android:layout_marginTop="10dp" android:background="@drawable/card_background" android:clickable="true" android:focusable="true" android:gravity="center_vertical" android:orientation="horizontal"><TextView android:layout_width="0dp" android:layout_height="wrap_content" android:layout_weight="1" android:text="Расслабление и аутогенная тренировка" android:textColor="@color/qd_text" android:textSize="17sp" android:textStyle="bold"/><TextView android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="→" android:textColor="@color/qd_primary" android:textSize="18sp"/></LinearLayout>
    <LinearLayout android:id="@+id/practiceRecallCard" android:layout_width="match_parent" android:layout_height="wrap_content" android:layout_marginTop="8dp" android:background="@drawable/card_background" android:clickable="true" android:focusable="true" android:gravity="center_vertical" android:orientation="horizontal"><TextView android:layout_width="0dp" android:layout_height="wrap_content" android:layout_weight="1" android:text="Вспомнить и сохранить сон" android:textColor="@color/qd_text" android:textSize="17sp" android:textStyle="bold"/><TextView android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="→" android:textColor="@color/qd_primary" android:textSize="18sp"/></LinearLayout>
    <LinearLayout android:id="@+id/practiceLucidCard" android:layout_width="match_parent" android:layout_height="wrap_content" android:layout_marginTop="8dp" android:background="@drawable/card_background" android:clickable="true" android:focusable="true" android:gravity="center_vertical" android:orientation="horizontal"><TextView android:layout_width="0dp" android:layout_height="wrap_content" android:layout_weight="1" android:text="Осознанные сновидения" android:textColor="@color/qd_text" android:textSize="17sp" android:textStyle="bold"/><TextView android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="→" android:textColor="@color/qd_primary" android:textSize="18sp"/></LinearLayout>
    <LinearLayout android:id="@+id/practiceStoriesCard" android:layout_width="match_parent" android:layout_height="wrap_content" android:layout_marginTop="8dp" android:background="@drawable/card_background" android:clickable="true" android:focusable="true" android:gravity="center_vertical" android:orientation="horizontal"><TextView android:layout_width="0dp" android:layout_height="wrap_content" android:layout_weight="1" android:text="Истории перед сном" android:textColor="@color/qd_text" android:textSize="17sp" android:textStyle="bold"/><TextView android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="СКОРО" android:textColor="@color/qd_muted" android:textSize="9sp" android:textStyle="bold"/></LinearLayout>
</LinearLayout>
</ScrollView>
<include layout="@layout/view_bottom_navigation"/>
</LinearLayout>
''', encoding='utf-8')

gradle = ROOT / 'app/build.gradle.kts'
text = gradle.read_text(encoding='utf-8')
old = '        versionCode = 3002\n        versionName = "0.30.2"\n'
new = '        versionCode = 30021\n        versionName = "0.30.2.1"\n'
if old not in text:
    raise SystemExit('0.30.2 version block not found')
gradle.write_text(text.replace(old, new, 1), encoding='utf-8')

print('Somnori 0.30.2.1 responsive Premium Pass A fix applied')
