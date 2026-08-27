# Somnori 0.31.7 — Arina gapless voice polish

0.31.7 is a deliberately narrow voice-quality release on top of 0.31.6.

## What changes

- Current-time playback and alarm-time confirmation no longer create a second `MediaPlayer` after the hour fragment finishes.
- Both local Arina fragments are prepared in advance and linked with Android `setNextMediaPlayer()`.
- For a command such as setting 07:30, the intended audible result is one continuous phrase: `Будильник установлен на семь тридцать`, without the technical player-start gap between `семь` and `тридцать`.
- The same continuity fix applies to the ordinary current-time response.

## What deliberately does not change

- `arina_core_v5.zip`, its private install directory and all 147 expected voice components remain unchanged. A real Arina pack already installed on a test phone survives the APK update.
- No new online TTS dependency is introduced.
- Alarm parsing, wake phrases, recording, music, time/alarm detectors and error replies are unchanged.
- The 0.31.6 morning hands-free route remains unchanged: night mode -> `Начать практику` -> recorded self-suggestion -> automatic return to night listening.

## Physical acceptance

1. Upgrade over the existing Arina-enabled Somnori installation; do not clear app data.
2. In night mode say the alarm command and set a non-zero-minute time such as 07:30 or 06:45.
3. Listen specifically to the hour/minute boundary. There should be no artificial pause caused by starting a second player.
4. Ask the current time at a non-zero minute and check the same boundary.
5. Run `Начать практику` once from night mode and verify that completion still returns to night listening.

This release improves the playback transport around the existing human Arina recordings. It does not claim to regenerate or replace those commercial recordings in the public CI scaffold.

CI checks the exact gapless link and cleanup calls separately, while freezing the 0.31.6 night/practice runtime and Arina v5 asset byte-for-byte.
