# Somnori 0.31.5 — offline night music

Replaces the four sub-second placeholder raw resources with full-length offline audio while preserving the existing SoundscapeService and night-program wiring.

Expected resources:
- `music_sea_harp.mp3` — 3 min
- `music_calm_energy.mp3` — 4 min
- `music_quiet_meditation.mp3` — 6 min
- `nature_forest.mp3` — 4 min auxiliary nature bed

The user-facing prototype uses original procedurally composed Somnori audio generated locally, avoiding third-party licensing dependencies. CI generates deterministic non-silent scaffold audio with the same durations; the richer prototype masters are injected only into the local test APK.

No Arina/night-recognition logic is changed in this slice.
