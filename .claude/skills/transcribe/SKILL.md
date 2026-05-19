---
name: transcribe
description: Transcribe audio files using the local `transcribe` CLI (WhisperX large-v3 + diarisation + optional LLM correction).
title: /transcribe
parent: Skills
permalink: /skills/transcribe/
nav_order: 19
---

# Transcribe Audio

Delegate to the local `transcribe` CLI from `~/dev/personal/transcribe/` (symlinked into `~/.local/bin/`, so callable from anywhere). Do NOT call `whisper-cli` directly — the CLI uses a better model (WhisperX `large-v3`), adds speaker diarisation, EBU R128 normalisation, and resumable caching.

## Your Task

Given an audio file path as argument:

1. **Resolve the file path** — expand `~` and verify the file exists.
2. **Run `transcribe`**:
   ```bash
   transcribe <audio-file> [lang] [output-dir]
   ```
   - `lang`: `fr` by default, `auto` to autodetect, or any whisper language code.
   - `output-dir`: `.` by default. Pass an explicit directory if the user specifies one or if the audio is somewhere they don't want output files dropped.
3. **Report where outputs landed** — `out/<safe>.txt`, `.srt`, `.json`, etc. The basename is sanitised (ASCII, lowercase, dashes, ≤60 chars).
4. **Offer LLM correction** if the transcript looks rough or the user cares about accuracy:
   ```bash
   correct <out/...json> [model]
   ```
   Default model is `mistral-nemo:12b`. Produces `<safe>.corrected.txt` and `<safe>.diff` next to the JSON.

## Guidelines

**DO:**
- Always use the `transcribe` CLI, not raw `whisper-cli` or `ffmpeg + whisper-cpp` pipelines.
- Trust the CLI's caching — re-running the same command resumes from the last completed stage, so it's safe to re-invoke.
- Surface the output path so the user can open the files.
- Suggest `correct` as a follow-up step, don't run it automatically (it's slow and uses Ollama).

**DON'T:**
- Don't reimplement the pipeline inline. If something's broken, fix it in `~/dev/personal/transcribe/`.
- Don't pass non-WAV files through manual ffmpeg conversion — the CLI handles all input formats.
- Don't worry about the medium-model whisper-cpp setup — it's been replaced.

## Input Handling

- **Single argument**: audio file path (e.g., `/transcribe ~/Downloads/audio.opus`)
- **With language**: file path + language code (e.g., `/transcribe ~/Downloads/audio.m4a en`)
- **With output dir**: file + lang + dir (e.g., `/transcribe ~/Downloads/audio.m4a fr ~/transcripts/`)
- **No argument**: ask the user for the file path.

## Tools Used

- **Bash**: `transcribe` and `correct` CLIs (in `~/.local/bin/`).

## Dependencies

Set up once per machine — see `~/dev/personal/transcribe/README.md` for full instructions:
- `uv tool install whisperx`
- Hugging Face token at `~/.config/whisperx/token` (for diarisation; delete the file to skip diarisation)
- `brew install ollama`, `ollama pull mistral-nemo:12b` (only needed for `correct`)

## Example Usage

```
/transcribe ~/Downloads/voice-message.opus
/transcribe ~/Downloads/meeting.mp3 en
/transcribe ~/Downloads/seance.m4a fr ~/transcripts/
```
