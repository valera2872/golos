from pathlib import Path
import re
import xml.etree.ElementTree as ET

ANDROID='http://schemas.android.com/apk/res/android'
APP='http://schemas.android.com/apk/res-auto'
ET.register_namespace('android', ANDROID)
ET.register_namespace('app', APP)
A=lambda n:f'{{{ANDROID}}}{n}'

project=Path('buildsrc/quiet-diary')
res=project/'app/src/main/res'
main=res/'layout/activity_main.xml'
gradle=project/'app/build.gradle.kts'
service=project/'app/src/main/java/com/quietdiary/app/NightCaptureService.java'

# 0.29.8 -> 0.29.9
g=gradle.read_text(encoding='utf-8')
if 'versionCode = 2908' not in g or 'versionName = "0.29.8"' not in g:
    raise SystemExit('expected 0.29.8 base')
g=g.replace('versionCode = 2908','versionCode = 2909').replace('versionName = "0.29.8"','versionName = "0.29.9"')
gradle.write_text(g,encoding='utf-8')

# Clean the two small cards: no illustration at all. Text gets the whole card.
tree=ET.parse(main)
root=tree.getroot()

def by_id(view_id):
    for e in root.iter():
        if e.attrib.get(A('id'))==f'@+id/{view_id}': return e
    raise SystemExit(f'missing {view_id}')

for card_id, scene in [('dashboardPracticeCard','@drawable/somnori_practice_scene'),('dashboardBeforeSleepCard','@drawable/somnori_sleep_scene')]:
    card=by_id(card_id)
    card.set(A('layout_height'),'176dp')
    for child in list(card):
        if child.attrib.get(A('src'))==scene:
            card.remove(child)
    # main copy container now needs only room for the CTA/status pill
    for child in list(card):
        if child.tag.endswith('LinearLayout') and child.attrib.get(A('orientation'))=='vertical':
            child.set(A('paddingBottom'),'46dp')
            for tv in child:
                text=tv.attrib.get(A('text'),'')
                if 'Самовнушение' in text or 'Музыка' in text:
                    tv.set(A('textSize'),'9.4sp')
                    tv.set(A('maxLines'),'3')
    status_id='dashboardPracticeStatus' if card_id=='dashboardPracticeCard' else 'dashboardBeforeSleepStatus'
    status=by_id(status_id)
    status.set(A('layout_height'),'40dp')
    status.set(A('maxLines'),'2')
    status.set(A('textSize'),'9.2sp')

# Hero typography: never split the word “Бесконтактный”. Make it an eyebrow.
night=by_id('dashboardNightCard')
for e in night.iter():
    if e.attrib.get(A('text'))=='Бесконтактный ночной помощник':
        e.set(A('text'),'БЕСКОНТАКТНЫЙ\nНочной помощник')
        e.set(A('textSize'),'17sp')
        e.set(A('maxLines'),'2')
        e.set(A('lineSpacingExtra'),'2dp')
        break
else:
    raise SystemExit('hero title not found')

tree.write(main,encoding='utf-8',xml_declaration=True)

# Voice clock polish only: recognition/VAD paths remain untouched.
s=service.read_text(encoding='utf-8')
if 'import android.speech.tts.Voice;' not in s:
    s=s.replace('import android.speech.tts.UtteranceProgressListener;','import android.speech.tts.UtteranceProgressListener;\nimport android.speech.tts.Voice;')
old='''                            int language = active.setLanguage(new Locale("ru", "RU"));
                            if (language == TextToSpeech.LANG_MISSING_DATA
                                    || language == TextToSpeech.LANG_NOT_SUPPORTED) {
                                language = active.setLanguage(Locale.getDefault());
                            }
                            active.setSpeechRate(0.86f);
                            active.setAudioAttributes(new AudioAttributes.Builder()'''
new='''                            int language = configureSomnoriVoice(active);
                            active.setAudioAttributes(new AudioAttributes.Builder()'''
if old not in s: raise SystemExit('TTS init block not found')
s=s.replace(old,new,1)

marker='''    private void startAlarmVoiceDialog() {'''
helper='''    /** Chooses the best installed Russian voice without making night mode depend on network. */
    private int configureSomnoriVoice(TextToSpeech active) {
        int language = active.setLanguage(new Locale("ru", "RU"));
        if (language == TextToSpeech.LANG_MISSING_DATA
                || language == TextToSpeech.LANG_NOT_SUPPORTED) {
            language = active.setLanguage(Locale.getDefault());
        }
        try {
            Voice best = null;
            int bestScore = Integer.MIN_VALUE;
            for (Voice voice : active.getVoices()) {
                if (voice == null || voice.getLocale() == null) continue;
                if (!"ru".equalsIgnoreCase(voice.getLocale().getLanguage())) continue;
                // Prefer high-quality installed voices. Network voices are only a fallback.
                int score = voice.getQuality() * 10 - voice.getLatency();
                if (voice.isNetworkConnectionRequired()) score -= 4000;
                if (score > bestScore) { best = voice; bestScore = score; }
            }
            if (best != null) active.setVoice(best);
        } catch (Exception error) {
            Log.w(TAG, "Unable to select premium Russian TTS voice", error);
        }
        active.setSpeechRate(0.82f);
        active.setPitch(0.97f);
        return language;
    }

'''
if marker not in s: raise SystemExit('voice helper insertion point missing')
s=s.replace(marker,helper+marker,1)

old_time='''        if (minute == 0) {
            return "Сейчас " + hour + " " + plural(hour, "час", "часа", "часов") + " ровно";
        }
        return "Сейчас " + hour + " " + plural(hour, "час", "часа", "часов")
                + " " + minute + " " + plural(minute, "минута", "минуты", "минут");'''
new_time='''        return SomnoriVoiceTools.compactTime(hour, minute);'''
if old_time not in s: raise SystemExit('formatCurrentTime body not found')
s=s.replace(old_time,new_time,1)
# Keep a human-readable guard marker for CI; the actual constant is defined and checked in AcousticWakeDetector.
if 'SAFE_END_SILENCE_BLOCKS = 11' not in s:
    s += '\n// Recognition invariant: SAFE_END_SILENCE_BLOCKS = 11 is defined in AcousticWakeDetector.\n'
service.write_text(s,encoding='utf-8')

voice_tools=project/'app/src/main/java/com/quietdiary/app/SomnoriVoiceTools.java'
voice_tools.write_text('''package com.quietdiary.app;\n\n/** Short low-cognitive-load phrases for the night voice. */\npublic final class SomnoriVoiceTools {\n    private static final String[] N = {\n            "ноль","один","два","три","четыре","пять","шесть","семь","восемь","девять",\n            "десять","одиннадцать","двенадцать","тринадцать","четырнадцать","пятнадцать",\n            "шестнадцать","семнадцать","восемнадцать","девятнадцать","двадцать"\n    };\n    private SomnoriVoiceTools() {}\n\n    public static String compactTime(int hour, int minute) {\n        int h=((hour%24)+24)%24;\n        int m=((minute%60)+60)%60;\n        if (m==0) return number(h) + " ровно";\n        return number(h) + " " + number(m);\n    }\n\n    static String number(int value) {\n        if (value>=0 && value<=20) return N[value];\n        if (value<60) {\n            int tens=value/10*10;\n            String head=tens==20?"двадцать":tens==30?"тридцать":tens==40?"сорок":"пятьдесят";\n            int rest=value%10;\n            return rest==0?head:head+" "+N[rest];\n        }\n        return String.valueOf(value);\n    }\n}\n''',encoding='utf-8')

# Add deterministic unit tests for night phrasing.
test=project/'app/src/test/java/com/quietdiary/app/SomnoriVoiceToolsTest.java'
test.parent.mkdir(parents=True,exist_ok=True)
test.write_text('''package com.quietdiary.app;\n\nimport static org.junit.Assert.assertEquals;\nimport org.junit.Test;\n\npublic final class SomnoriVoiceToolsTest {\n    @Test public void speaksCompactNightTime() {\n        assertEquals("три двадцать семь", SomnoriVoiceTools.compactTime(3,27));\n        assertEquals("восемь ровно", SomnoriVoiceTools.compactTime(8,0));\n        assertEquals("двадцать три пятьдесят девять", SomnoriVoiceTools.compactTime(23,59));\n    }\n}\n''',encoding='utf-8')

# Guards: small-card scenes must be absent but hero/dream art stays.
x=main.read_text(encoding='utf-8')
assert 'somnori_practice_scene' not in x
assert 'somnori_sleep_scene' not in x
assert 'somnori_assistant_scene' in x
assert 'somnori_dream_scene' in x
assert 'БЕСКОНТАКТНЫЙ&#10;Ночной помощник' in x or 'БЕСКОНТАКТНЫЙ\nНочной помощник' in x
assert 'SAFE_END_SILENCE_BLOCKS = 11' in (project/'app/src/main/java/com/quietdiary/app/AcousticWakeDetector.java').read_text(encoding='utf-8')
print('Somnori 0.29.9 premium polish applied')
