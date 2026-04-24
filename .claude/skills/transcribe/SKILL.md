---
name: transcribe
description: Transcribe audio files using whisper-cpp (whisper-cli) with automatic format conversion.
---

# Transcribe Audio

Transcribe audio files to text using whisper-cpp locally on your Mac.

## Your Task

Given an audio file path as argument:

1. **Resolve the file path** — expand `~` and verify the file exists
2. **Convert to WAV if needed** — if the file is not `.wav`, convert it using ffmpeg:
   ```bash
   ffmpeg -i <input> -ar 16000 -ac 1 /tmp/whisper_transcribe_tmp.wav
   ```
3. **Run whisper-cli** to transcribe:
   ```bash
   whisper-cli -m /opt/homebrew/share/whisper-cpp/ggml-medium.bin -l <lang> -np <wav_file>
   ```
   - Default language: `fr` (French)
   - If the user specifies a language (e.g., `/transcribe file.opus en`), use that instead
   - The `-np` flag suppresses debug output, showing only transcription results
4. **Output the clean transcription** — present only the transcribed text to the user, stripping timestamps
5. **Clean up** — if a temp WAV was created, delete `/tmp/whisper_transcribe_tmp.wav`

## Guidelines

**DO:**
- Always check the file exists before processing
- Convert non-WAV files (opus, mp3, ogg, m4a, flac, etc.) to WAV first
- Use `-ar 16000 -ac 1` for WAV conversion (16kHz mono, optimal for Whisper)
- Strip timestamps from output to give clean text
- Redirect ffmpeg and whisper stderr to /dev/null for clean output

**DON'T:**
- Don't try to pass non-WAV files directly to whisper-cli (it only reads WAV)
- Don't leave temp files behind after transcription
- Don't include whisper debug/timing output in the result

## Input Handling

- **Single argument**: audio file path (e.g., `/transcribe ~/Downloads/audio.opus`)
- **With language**: file path + language code (e.g., `/transcribe ~/Downloads/audio.opus en`)
- **No argument**: ask the user for the file path

## Tools Used

- **Bash**: for running ffmpeg (conversion) and whisper-cli (transcription)

## Dependencies

- `whisper-cpp` (installed via Homebrew, provides `whisper-cli`)
- `ffmpeg` (installed via Homebrew, for audio format conversion)
- Model file: `/opt/homebrew/share/whisper-cpp/ggml-medium.bin`

## Example Usage

```
/transcribe ~/Downloads/voice-message.opus
/transcribe ~/Downloads/meeting.mp3 en
/transcribe ~/Desktop/recording.wav
```
