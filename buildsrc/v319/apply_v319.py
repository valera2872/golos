from pathlib import Path

repo = Path(__file__).resolve().parents[1]
app = repo / 'quiet-diary' / 'app'
java = app / 'src' / 'main' / 'java' / 'com' / 'quietdiary' / 'app'
tests = app / 'src' / 'test' / 'java' / 'com' / 'quietdiary' / 'app'

build = app / 'build.gradle.kts'
s = build.read_text(encoding='utf-8')
assert 'versionCode = 30180' in s
assert 'versionName = "0.31.8-practice-handoff"' in s
s = s.replace('versionCode = 30180', 'versionCode = 30190', 1)
s = s.replace('versionName = "0.31.8-practice-handoff"',
              'versionName = "0.31.9-unified-night-routing"', 1)
build.write_text(s, encoding='utf-8')

# 0.31.6 added the practice acoustic detector before TIME/ALARM/DREAM/ENTRY. That is
# fine only if every acoustic hit is treated as a gate and final intent is selected from
# STT text. PRACTICE was accidentally excluded from the existing NightCommandRouter,
# so a permissive practice acoustic hit could consume a clock/alarm/dream/entry phrase.
# Extend the already-proven text arbiter instead of changing detector sensitivity/order.
router = java / 'NightCommandRouter.java'
old_router = router.read_text(encoding='utf-8')
assert 'public enum Kind { ENTRY, DREAM, TIME, ALARM, STOP, NONE }' in old_router
assert 'VoiceCommandMatcher.isAlarmTrigger(recognized)' in old_router
assert 'VoiceCommandMatcher.isStopNight(recognized, stopLabel)' in old_router

router.write_text('''package com.quietdiary.app;

/** Final command arbitration after speech-to-text. Acoustic matches are gates only. */
public final class NightCommandRouter {
    public enum Kind { ENTRY, DREAM, TIME, ALARM, PRACTICE, STOP, NONE }

    public static final class Decision {
        public final Kind kind;
        public final String matchedAnchor;
        Decision(Kind kind, String matchedAnchor) {
            this.kind = kind == null ? Kind.NONE : kind;
            this.matchedAnchor = matchedAnchor == null ? "" : matchedAnchor;
        }
    }

    private NightCommandRouter() {}

    /** Compatibility overload retained for existing tests/callers without PRACTICE. */
    public static Decision route(String recognized, String wakeLabel, String dreamLabel,
                                 String timeLabel, String alarmLabel, String stopLabel,
                                 Kind preferredAcousticGate) {
        return route(recognized, wakeLabel, dreamLabel, timeLabel, alarmLabel, "",
                stopLabel, preferredAcousticGate);
    }

    /**
     * One text arbiter for every all-night command. The acoustic detector that woke first
     * is only a tie-breaker; recognized words decide the action whenever they are clear.
     */
    public static Decision route(String recognized, String wakeLabel, String dreamLabel,
                                 String timeLabel, String alarmLabel, String practiceLabel,
                                 String stopLabel, Kind preferredAcousticGate) {
        WakePhraseTextMatcher.MatchResult entry = WakePhraseTextMatcher.match(wakeLabel, recognized);
        WakePhraseTextMatcher.MatchResult dream = WakePhraseTextMatcher.match(dreamLabel, recognized);
        WakePhraseTextMatcher.MatchResult time = WakePhraseTextMatcher.match(timeLabel, recognized);
        WakePhraseTextMatcher.MatchResult alarm = WakePhraseTextMatcher.match(alarmLabel, recognized);
        WakePhraseTextMatcher.MatchResult stop = WakePhraseTextMatcher.match(stopLabel, recognized);
        WakePhraseTextMatcher.MatchResult practice = practiceLabel == null || practiceLabel.trim().isEmpty()
                ? null : WakePhraseTextMatcher.match(practiceLabel, recognized);

        boolean explicitDream = DreamTools.isDreamWakePhrase(recognized);
        boolean fullEntry = entry.fullPhrase;
        boolean fullDream = dream.fullPhrase || explicitDream;
        boolean timeMatched = time.matched || VoiceCommandMatcher.isTimeRequest(recognized);
        boolean alarmMatched = alarm.matched || VoiceCommandMatcher.isAlarmTrigger(recognized);
        boolean stopMatched = stop.matched || VoiceCommandMatcher.isStopNight(recognized, stopLabel);
        boolean practiceFull = practice != null && practice.fullPhrase;
        boolean practiceAnchor = practice != null && practice.matched;

        // Specific semantic/full-phrase evidence wins over whichever acoustic bank fired.
        if (fullDream) return new Decision(Kind.DREAM,
                dream.matchedAnchor.isEmpty() ? "дневник сон" : dream.matchedAnchor);
        if (fullEntry) return new Decision(Kind.ENTRY, entry.matchedAnchor);
        if (practiceFull && !alarmMatched && !timeMatched && !stopMatched) {
            return new Decision(Kind.PRACTICE, practice.matchedAnchor);
        }
        if (alarmMatched && !timeMatched && !stopMatched && !practiceFull) {
            return new Decision(Kind.ALARM, alarm.matchedAnchor);
        }
        if (stopMatched && !timeMatched && !alarmMatched && !practiceFull) {
            return new Decision(Kind.STOP, stop.matchedAnchor);
        }
        if (timeMatched && !stopMatched && !alarmMatched && !practiceFull) {
            return new Decision(Kind.TIME, time.matchedAnchor);
        }

        // Partial STT is accepted only when it agrees with the trained acoustic gate.
        boolean entryAnchor = entry.matched;
        boolean dreamAnchor = dream.matched;
        if (preferredAcousticGate == Kind.PRACTICE && practiceAnchor) {
            return new Decision(Kind.PRACTICE, practice.matchedAnchor);
        }
        if (preferredAcousticGate == Kind.ALARM && alarmMatched) return new Decision(Kind.ALARM, alarm.matchedAnchor);
        if (preferredAcousticGate == Kind.DREAM && dreamAnchor) return new Decision(Kind.DREAM, dream.matchedAnchor);
        if (preferredAcousticGate == Kind.ENTRY && entryAnchor) return new Decision(Kind.ENTRY, entry.matchedAnchor);
        if (preferredAcousticGate == Kind.TIME && timeMatched) return new Decision(Kind.TIME, time.matchedAnchor);
        if (preferredAcousticGate == Kind.STOP && stopMatched) return new Decision(Kind.STOP, stop.matchedAnchor);

        // A different acoustic detector may have stolen a clear phrase. Route it back by text.
        if (entryAnchor && !explicitDream) return new Decision(Kind.ENTRY, entry.matchedAnchor);
        if (dreamAnchor && explicitDream) return new Decision(Kind.DREAM, dream.matchedAnchor);
        if (practiceFull) return new Decision(Kind.PRACTICE, practice.matchedAnchor);
        if (alarmMatched) return new Decision(Kind.ALARM, alarm.matchedAnchor);
        if (timeMatched) return new Decision(Kind.TIME, time.matchedAnchor);
        if (stopMatched) return new Decision(Kind.STOP, stop.matchedAnchor);
        return new Decision(Kind.NONE, "");
    }
}
''', encoding='utf-8')

night = java / 'NightCaptureService.java'
s = night.read_text(encoding='utf-8')

# PRACTICE must go through the same text router as TIME/ALARM/DREAM/ENTRY/STOP.
old = '''            if (completedPurpose != VerificationPurpose.PRACTICE
                    && completed.error.isEmpty() && !completed.recognizedText.isEmpty()) {'''
new = '''            if (completed.error.isEmpty() && !completed.recognizedText.isEmpty()) {'''
assert old in s
s = s.replace(old, new, 1)

old = '''                NightCommandRouter.Kind preferredKind = completedPurpose == VerificationPurpose.TIME
                        ? NightCommandRouter.Kind.TIME
                        : completedPurpose == VerificationPurpose.ALARM
                        ? NightCommandRouter.Kind.ALARM
                        : completedPurpose == VerificationPurpose.STOP
                        ? NightCommandRouter.Kind.STOP
                        : completedPurpose == VerificationPurpose.DREAM
                        ? NightCommandRouter.Kind.DREAM
                        : NightCommandRouter.Kind.ENTRY;'''
new = '''                NightCommandRouter.Kind preferredKind = completedPurpose == VerificationPurpose.TIME
                        ? NightCommandRouter.Kind.TIME
                        : completedPurpose == VerificationPurpose.ALARM
                        ? NightCommandRouter.Kind.ALARM
                        : completedPurpose == VerificationPurpose.PRACTICE
                        ? NightCommandRouter.Kind.PRACTICE
                        : completedPurpose == VerificationPurpose.STOP
                        ? NightCommandRouter.Kind.STOP
                        : completedPurpose == VerificationPurpose.DREAM
                        ? NightCommandRouter.Kind.DREAM
                        : NightCommandRouter.Kind.ENTRY;'''
assert old in s
s = s.replace(old, new, 1)

old = '''                NightCommandRouter.Decision routed = NightCommandRouter.route(
                        completed.recognizedText, wakeLabel, dreamLabel, timeLabel, alarmLabel, stopLabel, preferredKind);'''
new = '''                NightCommandRouter.Decision routed = NightCommandRouter.route(
                        completed.recognizedText, wakeLabel, dreamLabel, timeLabel, alarmLabel,
                        practiceLabel, stopLabel, preferredKind);'''
assert old in s
s = s.replace(old, new, 1)

old = '''                    VerificationPurpose routedPurpose = routed.kind == NightCommandRouter.Kind.TIME
                            ? VerificationPurpose.TIME
                            : routed.kind == NightCommandRouter.Kind.ALARM
                            ? VerificationPurpose.ALARM
                            : routed.kind == NightCommandRouter.Kind.STOP
                            ? VerificationPurpose.STOP
                            : routed.kind == NightCommandRouter.Kind.DREAM
                            ? VerificationPurpose.DREAM
                            : VerificationPurpose.ENTRY;'''
new = '''                    VerificationPurpose routedPurpose = routed.kind == NightCommandRouter.Kind.TIME
                            ? VerificationPurpose.TIME
                            : routed.kind == NightCommandRouter.Kind.ALARM
                            ? VerificationPurpose.ALARM
                            : routed.kind == NightCommandRouter.Kind.PRACTICE
                            ? VerificationPurpose.PRACTICE
                            : routed.kind == NightCommandRouter.Kind.STOP
                            ? VerificationPurpose.STOP
                            : routed.kind == NightCommandRouter.Kind.DREAM
                            ? VerificationPurpose.DREAM
                            : VerificationPurpose.ENTRY;'''
assert old in s
s = s.replace(old, new, 1)
night.write_text(s, encoding='utf-8')

# Regression tests model the physical failure: the PRACTICE acoustic bank may wake first,
# but it must not steal any of the established night commands.
tests.mkdir(parents=True, exist_ok=True)
(tests / 'NightCommandRouterPracticeTest.java').write_text('''package com.quietdiary.app;

import static org.junit.Assert.assertEquals;

import org.junit.Test;

public class NightCommandRouterPracticeTest {
    private static final String ENTRY = "Дневник запись";
    private static final String DREAM = "Дневник сон";
    private static final String TIME = "Который час";
    private static final String ALARM = "Будильник";
    private static final String PRACTICE = "Начать практику";
    private static final String STOP = "Ночь стоп";

    private NightCommandRouter.Decision fromPracticeGate(String recognized) {
        return NightCommandRouter.route(recognized, ENTRY, DREAM, TIME, ALARM, PRACTICE, STOP,
                NightCommandRouter.Kind.PRACTICE);
    }

    @Test public void practiceGateCannotStealClock() {
        assertEquals(NightCommandRouter.Kind.TIME, fromPracticeGate("который час").kind);
    }

    @Test public void practiceGateCannotStealAlarm() {
        assertEquals(NightCommandRouter.Kind.ALARM, fromPracticeGate("будильник").kind);
    }

    @Test public void practiceGateCannotStealDream() {
        assertEquals(NightCommandRouter.Kind.DREAM, fromPracticeGate("дневник сон").kind);
    }

    @Test public void practiceGateCannotStealDiaryEntry() {
        assertEquals(NightCommandRouter.Kind.ENTRY, fromPracticeGate("дневник запись").kind);
    }

    @Test public void practiceGateCannotStealStop() {
        assertEquals(NightCommandRouter.Kind.STOP, fromPracticeGate("ночь стоп").kind);
    }

    @Test public void anotherGateRoutesFullPracticePhraseBackToPractice() {
        NightCommandRouter.Decision d = NightCommandRouter.route(
                "начать практику", ENTRY, DREAM, TIME, ALARM, PRACTICE, STOP,
                NightCommandRouter.Kind.TIME);
        assertEquals(NightCommandRouter.Kind.PRACTICE, d.kind);
    }
}
''', encoding='utf-8')

print('Applied Somnori 0.31.9 unified all-night command routing')
