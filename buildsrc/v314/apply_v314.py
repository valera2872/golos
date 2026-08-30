from pathlib import Path
import shutil

repo = Path(__file__).resolve().parents[1]
app = repo / 'quiet-diary' / 'app'
main = app / 'src' / 'main'
java = main / 'java' / 'com' / 'quietdiary' / 'app'
assets = main / 'assets'
assets.mkdir(parents=True, exist_ok=True)

# Runtime ElevenLabs audio itself is not stored in public GitHub.
# CI provides a placeholder ZIP with the exact same 147-component shape.
shutil.copy2(repo / 'v314' / 'arina_core_v5.zip', assets / 'arina_core_v5.zip')
old_asset = assets / 'arina_core_v4.zip'
if old_asset.exists():
    old_asset.unlink()

build = app / 'build.gradle.kts'
s = build.read_text(encoding='utf-8')
assert 'versionCode = 30130' in s
assert 'versionName = "0.31.3-arina-flow-polish"' in s
s = s.replace('versionCode = 30130', 'versionCode = 30140', 1)
s = s.replace('versionName = "0.31.3-arina-flow-polish"', 'versionName = "0.31.4-arina-errors"', 1)
build.write_text(s, encoding='utf-8')

voice = java / 'ArinaVoicePack.java'
s = voice.read_text(encoding='utf-8')
s = s.replace('private static final String ASSET = "arina_core_v4.zip";', 'private static final String ASSET = "arina_core_v5.zip";', 1)
s = s.replace('private static final String DIR = "arina_voice_core_v4";', 'private static final String DIR = "arina_voice_core_v5";', 1)
s = s.replace('private static final String MARKER = ".installed_v4";', 'private static final String MARKER = ".installed_v5";', 1)
s = s.replace('Somnori Arina core v4\\n', 'Somnori Arina core v5\\n', 1)

anchor = '''    public static final String PHRASE_ALARM_STOPPED = "alarm/alarm_11.mp3";
'''
addition = '''    public static final String PHRASE_ALARM_STOPPED = "alarm/alarm_11.mp3";

    public static final String PHRASE_ERROR_NOT_HEARD = "errors/error_01.mp3";
    public static final String PHRASE_ERROR_NOT_UNDERSTOOD = "errors/error_02.mp3";
    public static final String PHRASE_ERROR_COMMAND = "errors/error_03.mp3";
    public static final String PHRASE_ERROR_TIME = "errors/error_04.mp3";
    public static final String PHRASE_ERROR_ALARM_TIME = "errors/error_05.mp3";
    public static final String PHRASE_ERROR_GENERIC = "errors/error_06.mp3";
    public static final String PHRASE_ERROR_RECORD_START = "errors/error_07.mp3";
    public static final String PHRASE_ERROR_RECORD_SAVE = "errors/error_08.mp3";
'''
assert anchor in s
s = s.replace(anchor, addition, 1)

old = '''        for (int i = 1; i <= 11; i++) {
            if (!new File(dir, String.format(Locale.US, "alarm/alarm_%02d.mp3", i)).isFile()) return false;
        }
        return true;'''
new = '''        for (int i = 1; i <= 11; i++) {
            if (!new File(dir, String.format(Locale.US, "alarm/alarm_%02d.mp3", i)).isFile()) return false;
        }
        for (int i = 1; i <= 8; i++) {
            if (!new File(dir, String.format(Locale.US, "errors/error_%02d.mp3", i)).isFile()) return false;
        }
        return true;'''
assert old in s
s = s.replace(old, new, 1)

old = '''                || name.matches("recording/record_0[1-9]\\\\.mp3")
                || name.matches("alarm/alarm_(0[1-9]|1[01])\\\\.mp3");'''
new = '''                || name.matches("recording/record_0[1-9]\\\\.mp3")
                || name.matches("alarm/alarm_(0[1-9]|1[01])\\\\.mp3")
                || name.matches("errors/error_0[1-8]\\\\.mp3");'''
assert old in s
s = s.replace(old, new, 1)
voice.write_text(s, encoding='utf-8')

night = java / 'NightCaptureService.java'
s = night.read_text(encoding='utf-8')

# A timed-out alarm dialog returns to waiting. Use a short human voice instead of a
# mechanical sentence; the user can invoke the alarm command again.
s = s.replace(
    'finishAlarmDialogByVoice("Не услышал новое время. Будильник не изменён.");',
    'finishAlarmDialogByArina(ArinaVoicePack.PHRASE_ERROR_GENERIC, "Что-то не получилось. Попробуй ещё раз.");',
    1)

old = '''        if (!result.error.isEmpty()) {
            if (alarmDialogAttempts < 2) {
                retryAlarmDialogByVoice("Не расслышал время. Повторите, например: двенадцать тридцать два.");
            } else {
                finishAlarmDialogByVoice("Не удалось распознать время. Будильник не изменён.");
            }
            return;
        }'''
new = '''        if (!result.error.isEmpty()) {
            if (alarmDialogAttempts < 2) {
                retryAlarmDialogByArina(ArinaVoicePack.PHRASE_ERROR_ALARM_TIME,
                        "Не услышала время будильника. Назови его ещё раз.");
            } else {
                finishAlarmDialogByArina(ArinaVoicePack.PHRASE_ERROR_GENERIC,
                        "Что-то не получилось. Попробуй ещё раз.");
            }
            return;
        }'''
assert old in s
s = s.replace(old, new, 1)

s = s.replace(
    'finishAlarmDialogByVoice("Я не установил будильник. Сначала разрешите точные будильники в настройках Somnori.");',
    'finishAlarmDialogByArina(ArinaVoicePack.PHRASE_ERROR_GENERIC, "Я не установил будильник. Сначала разрешите точные будильники в настройках Somnori.");',
    1)
s = s.replace(
    'finishAlarmDialogByVoice("Не удалось установить будильник. Проверьте разрешение будильников Android.");',
    'finishAlarmDialogByArina(ArinaVoicePack.PHRASE_ERROR_GENERIC, "Не удалось установить будильник. Проверьте разрешение будильников Android.");',
    1)

old = '''        String detail = parsed.error.isEmpty() ? "Не понял время." : parsed.error + ".";
        if (alarmDialogAttempts < 2) {
            retryAlarmDialogByVoice(detail + " Повторите, например: двенадцать тридцать два.");
        } else {
            finishAlarmDialogByVoice(detail + " Будильник не изменён.");
        }'''
new = '''        String detail = parsed.error.isEmpty() ? "Не понял время." : parsed.error + ".";
        if (alarmDialogAttempts < 2) {
            retryAlarmDialogByArina(ArinaVoicePack.PHRASE_ERROR_TIME,
                    "Не поняла время. Назови часы и минуты.");
        } else {
            finishAlarmDialogByArina(ArinaVoicePack.PHRASE_ERROR_GENERIC,
                    detail + " Будильник не изменён.");
        }'''
assert old in s
s = s.replace(old, new, 1)

needle = '''    private void retryAlarmDialogByVoice(String spoken) {
'''
addition = '''    private void retryAlarmDialogByArina(String phrasePath, String fallback) {
        alarmDialogListening = false;
        alarmDialogTranscribing = false;
        alarmDialogStartedAt = 0L;
        alarmDialogResult.set(null);
        alarmUtteranceCollector.reset();
        setMode(MODE_SPEAKING);
        updateNotification(fallback);
        pauseAudioInputForSpeech();
        boolean voiced = ArinaVoicePack.playPhraseIfEnabled(this, phrasePath);
        if (!voiced) speakAndWait(fallback);
        if (!running.get()) return;
        beginAlarmDialogListening();
    }

'''
assert needle in s
s = s.replace(needle, addition + needle, 1)
night.write_text(s, encoding='utf-8')

print('Applied Somnori 0.31.4 Arina error voice pack')
