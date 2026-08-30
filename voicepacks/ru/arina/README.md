# Somnori RU voice — Arina

Decision date: 2026-08-23

## Decision

Primary Russian Somnori voice direction: **ElevenLabs / Arina**.

Physical listening ranking:
- Arina — selected primary voice.
- Bella and Sarah — strong ElevenLabs references but not selected.
- Piper Irina — acceptable offline fallback/control.
- Yandex SpeechKit — rejected by listening.
- Android system TTS — rejected.
- Supertonic 3 — rejected.
- Chatterbox Multilingual V3 — rejected due audible foreign accent.

## Pilot first

Do not bulk-generate a production pack until the pilot is physically approved in the real nighttime use context.

Pilot manifest: `pilot-pack.json`.

For a free-tier UI test, generate the pilot in the ElevenLabs web UI with Arina and listen from the phone at low volume. `pilot-master-multilingual-v2.txt` is a one-generation master strip with 2-second breaks for Multilingual v2.

## Automated pack generation

`.github/workflows/elevenlabs-arina-pilot-pack.yml` is manual-only (`workflow_dispatch`) so normal CI cannot spend ElevenLabs credits.

It requires repository secret `ELEVENLABS_API_KEY`. Never commit or paste an API key into source files, issues, PR comments, or workflow inputs.

The workflow:
1. checks subscription/quota;
2. resolves Arina by voice ID or exact name;
3. generates each pilot phrase as a separate MP3;
4. writes a resolved manifest with SHA-256 checksums;
5. uploads a ZIP artifact.

ElevenLabs Voice Library voices are not available through the API on the free tier, so the web UI is the zero-cost pilot path. Use the API workflow only after an eligible paid tier is intentionally enabled.

## Architecture rule

Critical nighttime playback must not depend on a live network request at the moment it is needed.

- Static phrases: ship or cache local Arina audio.
- Custom alarm phrase: synthesize when the alarm is configured and cache locally before sleep.
- Current time / other dynamic speech: online Arina when available; offline fallback remains a separate decision. Do not pre-generate 1440 time phrases during the pilot.
