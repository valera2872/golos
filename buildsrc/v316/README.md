# Somnori 0.31.6 — night practice UX

Physical-test follow-up from 0.31.5.

Implemented scope:
- explicit self-suggestion scheduler gap reduced from 3000 ms to 1500 ms in both standalone practice and the evening program; the user's own recorded clip is left untouched, so the audible pause should land near three seconds instead of >5 seconds;
- the already-trained practice-start samples are loaded into the active NightCaptureService detector set;
- while night mode is listening, the saved phrase (default: «Начать практику») can start the user's existing recorded practice hands-free;
- night capture releases the microphone before CouePracticeService starts;
- the command forces auto-night for that run, so completion returns automatically to night listening;
- time, alarm, dream, entry, stop, Arina and music behavior otherwise remains unchanged.

Alarm wording is deliberately not changed in this pass: the existing sliced assets cannot form «Будильник установлен на …» cleanly without a redundant or mechanical splice. That voice polish is deferred until a dedicated voice regeneration pass.
