# Somnori 0.31.8 — practice listener handoff hotfix

This hotfix addresses a physical-device state bug found after training and arming the standalone `Начать практику` listener.

## Reproduction fixed

1. Train the practice-start phrase.
2. In the self-suggestion screen arm `Ждать команду «Начать практику»`.
3. Disable that waiting mode and leave the practice screen.
4. Start Night mode from the main screen.
5. Previously, the stale standalone Coué listener/status could remain `WAITING`, own the microphone, and the app appeared to wait only for the practice command. Other night commands such as `Который час` did not get the normal night listener.

## 0.31.8 behavior

- Destroying/stopping `CouePracticeService` while it is in `WAITING` or `VERIFYING` always publishes `MODE_OFF`.
- Starting `NightCaptureService` detects a stale/active standalone practice waiter and explicitly stops it before opening the all-night microphone.
- Only that handoff gets a short 180 ms microphone-release window; ordinary Night-mode startup is unchanged.
- Night mode remains the single all-night listener and continues to expose entry, dream, time, alarm, stop and trained practice-start detectors together.
- Practice templates remain in their own `coue_start_templates_v1` store and do not replace the normal night-command templates.

## Physical acceptance

Repeat the exact reproduction above, then in Night mode verify at least:

- `Который час` works;
- one normal record/dream command works;
- `Начать практику` also works;
- after the practice finishes, Somnori automatically returns to the same all-command Night mode.
