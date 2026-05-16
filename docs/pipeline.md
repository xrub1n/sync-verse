# SyncVerse MVP 1 Pipeline Reference

## Purpose

SyncVerse MVP 1 is a local-first command-line lyric synchronization tool.

The user provides:

```txt
1. An audio file
2. A plain-text lyric file
```

SyncVerse produces:

```txt
1. An internal JSON alignment file
2. A basic .lrc export
```

The internal JSON is the **source of truth**. Export formats such as `.lrc` are generated from the JSON and should not be treated as the main project data format.

MVP 1 focuses on **local forced alignment** using Montreal Forced Aligner, or MFA. The system should support word-level timing internally, even if the `.lrc` export is line-level.

---

## MVP 1 Scope

### Included in MVP 1

MVP 1 shall include:

```txt
Command-line interface
Audio file input
Plain-text lyric file input
Local forced-alignment backend
Montreal Forced Aligner integration
Word-level internal alignment
Line-level lyric grouping
Internal JSON output
Basic .lrc export
Basic error handling
Basic documentation for running the tool
```

### Not Included in MVP 1

MVP 1 shall not include:

```txt
Cloud-based transcription APIs
Demucs vocal separation
Custom MFA model training
GUI
Manual timing editor
Lyric video rendering
Enhanced .lrc export
ASS/SRT subtitle export
Multi-language model selection UI
Batch processing
```

These features may be added in future versions, but the MVP 1 architecture should not block them.

---

## Core Design Principles

### 1. Local-First Processing

SyncVerse should prioritize local processing.

MVP 1 should not depend on cloud-based audio processing or transcription APIs.

The primary alignment backend is:

```txt
Montreal Forced Aligner
```

---

### 2. Lyrics Are the Source of Truth

The lyric file provided by the user is assumed to be:

```txt
Correct
Chronological
Representative of the song’s performed lyrics
```

The alignment system should not attempt to rewrite, regenerate, or replace the lyrics during MVP 1.

---

### 3. Internal JSON Is Canonical

The internal JSON output is the canonical SyncVerse output.

The `.lrc` file is only an export generated from the internal JSON.

Correct data flow:

```txt
MFA output → SyncVerse internal JSON → .lrc export
```

Incorrect data flow:

```txt
MFA output → .lrc export directly
```

---

### 4. Alignment Backend Should Be Swappable

The MFA integration should be implemented behind an interface so that future alignment backends can be added later.

Possible backends:

```txt
MFAAlignmentBackend
FutureWhisperXBackend
FutureCustomSingingAlignmentBackend
FutureManualAlignmentBackend
```

The rest of the application should not depend directly on MFA-specific command structure or output formats.

---

## High-Level Pipeline

```txt
User CLI Command
        ↓
Input Validation
        ↓
Audio Preprocessing
        ↓
Lyric Parsing and Normalization
        ↓
MFA Corpus Preparation
        ↓
Forced Alignment Backend
        ↓
MFA Output Parsing
        ↓
Word-to-Line Reconstruction
        ↓
Quality Checks and Warnings
        ↓
Internal JSON Generation
        ↓
.lrc Export
        ↓
CLI Summary Output
```

---

## Example CLI Command

The primary MVP 1 command should eventually look like this:

```bash
syncverse align examples/audio/song.wav examples/lyrics/lyrics.txt --out output/
```

Expected outputs:

```txt
output/alignment.json
output/song.lrc
```

Optional future command examples, not required for MVP 1:

```bash
syncverse align song.mp3 lyrics.txt --out output/ --separate-vocals
```

```bash
syncverse align vocals.wav lyrics.txt --out output/ --input-is-vocals
```

---

# Detailed Pipeline Steps

## Step 1: CLI Input

The user runs:

```bash
syncverse align <audio_file> <lyrics_file> --out <output_directory>
```

Example:

```bash
syncverse align song.wav lyrics.txt --out output/
```

The CLI should collect:

```txt
audio_file
lyrics_file
output_directory
optional flags
```

For MVP 1, keep flags minimal.

Suggested MVP 1 flags:

```txt
--out
--keep-intermediate
--verbose
```

Future flags may include:

```txt
--backend
--separate-vocals
--input-is-vocals
--language
--dictionary
--acoustic-model
```

---

## Step 2: Input Validation

Before doing any processing, SyncVerse should validate the inputs.

Validate the audio file:

```txt
File exists
File is readable
File extension is supported
File is not empty
```

Recommended MVP 1 supported audio formats:

```txt
.wav
.mp3
.flac
.m4a
```

Internally, audio should be converted to WAV if needed.

Validate the lyric file:

```txt
File exists
File is readable
File extension is .txt
File is not empty
Contains at least one non-empty lyric line
```

Validate output directory:

```txt
Create it if it does not exist
Ensure it is writable
```

If validation fails, the CLI should show a clear error and stop.

Example:

```txt
Error: Lyrics file is empty: examples/lyrics/lyrics.txt
```

---

## Step 3: Audio Preprocessing

MVP 1 should prepare the audio into a format suitable for alignment.

The alignment audio should be:

```txt
WAV format
Mono
Consistent sample rate
Readable by MFA
```

Recommended target format:

```txt
.wav
mono
16000 Hz or MFA-compatible default
```

The output should be stored as an intermediate file.

Example:

```txt
output/intermediate/song_normalized.wav
```

The internal JSON should store both:

```txt
Original audio file path
Actual audio file used for alignment
```

Example:

```json
"source": {
  "audio_file": "examples/audio/song.mp3",
  "lyrics_file": "examples/lyrics/lyrics.txt"
},
"processing": {
  "audio": {
    "input_file": "examples/audio/song.mp3",
    "used_for_alignment": "output/intermediate/song_normalized.wav"
  }
}
```

For MVP 1, vocal separation is not required.

Future extension point:

```txt
If the user provides a vocal-only stem or enables vocal separation, used_for_alignment may point to vocals.wav instead of the normalized original mix.
```

---

## Step 4: Lyric Parsing

The lyric file should be parsed into line objects.

Input example:

```txt
Never gonna give you up
Never gonna let you down
Never gonna run around and desert you
```

Parsed structure:

```json
{
  "id": 0,
  "text": "Never gonna give you up",
  "normalized_text": "never gonna give you up",
  "words": [
    {
      "id": 0,
      "text": "Never",
      "normalized_text": "never"
    },
    {
      "id": 1,
      "text": "gonna",
      "normalized_text": "gonna"
    }
  ]
}
```

MVP 1 lyric parsing rules:

```txt
Preserve original line text
Remove blank lines from alignment input
Assign each lyric line a stable numeric ID
Split each line into words
Assign each word a line-local numeric ID
Store both original text and normalized text
```

Recommended normalization for MVP 1:

```txt
Lowercase text for alignment
Remove most punctuation for alignment
Preserve apostrophes only if needed by dictionary behavior
Normalize repeated whitespace
Preserve original text for final output
```

Important:

```txt
Do not overwrite the original lyrics.
Do not ask an AI model to rewrite the lyrics.
Do not reorder lyrics.
```

---

## Step 5: MFA Corpus Preparation

MFA expects audio and transcript files in a corpus-like structure.

SyncVerse should generate a temporary MFA working directory.

Example:

```txt
output/intermediate/mfa_corpus/
├── song.wav
└── song.txt
```

The transcript file should contain the normalized lyric text in chronological order.

Example generated transcript:

```txt
never gonna give you up
never gonna let you down
never gonna run around and desert you
```

The generated transcript should be suitable for MFA alignment.

SyncVerse should keep enough metadata to map MFA’s output words back to the original lyric lines and word IDs.

This mapping is critical.

Recommended internal mapping concept:

```txt
normalized transcript word position
        ↓
original lyric line ID
        ↓
line-local word ID
        ↓
original displayed word
```

Example:

```json
{
  "global_word_index": 0,
  "line_id": 0,
  "line_word_id": 0,
  "text": "Never",
  "normalized_text": "never"
}
```

This mapping does not necessarily need to appear in final MVP 1 JSON, but it should exist internally during processing.

---

## Step 6: Alignment Backend Execution

MVP 1 should use MFA through an alignment backend interface.

Conceptual interface:

```python
class AlignmentBackend:
    def align(self, audio_path: str, transcript_path: str, output_dir: str) -> AlignmentBackendResult:
        raise NotImplementedError
```

MFA implementation:

```python
class MFAAlignmentBackend(AlignmentBackend):
    def align(self, audio_path: str, transcript_path: str, output_dir: str) -> AlignmentBackendResult:
        ...
```

The rest of SyncVerse should call the interface, not hardcode MFA logic throughout the app.

The MFA backend should be responsible for:

```txt
Preparing MFA command arguments
Running MFA
Capturing stdout/stderr
Detecting backend failure
Locating MFA output files
Returning paths to generated alignment files
```

MFA output will commonly involve TextGrid files.

Example intermediate output:

```txt
output/intermediate/mfa_output/song.TextGrid
```

---

## Step 7: MFA Output Parsing

SyncVerse should parse MFA output and extract word-level timings.

For MVP 1, extract:

```txt
word text
start time
end time
duration
```

Example parsed word timing:

```json
{
  "text": "never",
  "start": 12.34,
  "end": 12.78,
  "duration": 0.44,
  "source": "mfa"
}
```

The parser should ignore silence intervals and non-word labels as needed.

Common labels to handle carefully:

```txt
sil
sp
empty intervals
unknown tokens
```

The parser should not assume MFA output is perfect.

If MFA produces words that cannot be mapped cleanly back to the original lyrics, SyncVerse should create warnings.

---

## Step 8: Word-to-Line Reconstruction

After word timings are extracted, SyncVerse should map each aligned word back to the original lyric structure.

The final alignment should be grouped by lyric line.

Example:

```json
{
  "line_id": 0,
  "text": "Never gonna give you up",
  "start": 12.34,
  "end": 14.82,
  "duration": 2.48,
  "words": [
    {
      "line_word_id": 0,
      "text": "Never",
      "start": 12.34,
      "end": 12.78
    },
    {
      "line_word_id": 1,
      "text": "gonna",
      "start": 12.79,
      "end": 13.18
    }
  ]
}
```

Line timing rules:

```txt
Line start = start time of first aligned word in the line
Line end = end time of last aligned word in the line
Line duration = line end - line start
```

If a line has missing word timings:

```txt
Use available word timings if possible
Set missing word timing fields to null
Create a warning
Lower the line quality score
```

---

## Step 9: Quality Scoring

MVP 1 should use the term:

```txt
quality_score
```

not:

```txt
confidence
```

Reason:

```txt
MFA may not provide reliable per-word confidence scores.
SyncVerse can compute its own heuristic quality score.
```

The quality score should represent SyncVerse’s judgment of alignment quality.

Recommended range:

```txt
0.0 to 1.0
```

Example:

```json
"quality_score": 0.91,
"quality_score_method": "syncverse_heuristic_v1"
```

MVP 1 quality scoring can be simple.

Possible signals:

```txt
All words aligned successfully
No missing timestamps
Word durations are reasonable
Line durations are reasonable
Timestamps are chronological
No line overlaps unexpectedly
No unexplained huge gaps inside a line
```

Suggested MVP 1 scoring approach:

```txt
Start with 1.0
Subtract penalties for detected issues
Clamp final score between 0.0 and 1.0
```

Example penalties:

```txt
Missing word timing: -0.15
Suspiciously short word duration: -0.05
Suspiciously long word duration: -0.05
Non-chronological timestamp: -0.25
Line overlap: -0.15
Very long unexplained gap inside a line: -0.10
```

The exact values can change later, but the field name should remain stable.

---

## Step 10: Warning Generation

Warnings should be kept in MVP 1.

Warnings allow the pipeline to complete while still marking suspicious areas for review.

Top-level warning format:

```json
{
  "type": "suspicious_word_duration",
  "severity": "info",
  "line_id": 2,
  "word_id": 4,
  "message": "Word duration is shorter than expected.",
  "details": {
    "word": "and",
    "duration": 0.18
  }
}
```

Recommended severity levels:

```txt
info
warning
error
```

Recommended MVP 1 warning types:

```txt
missing_alignment
unknown_word
long_gap
line_overlap
non_chronological_timestamp
suspicious_word_duration
suspicious_line_duration
empty_lyric_line
backend_error
```

Warnings should be stored in:

```json
"warnings": []
```

Warnings should also influence quality scores when appropriate.

---

## Step 11: Internal JSON Generation

After alignment and validation, SyncVerse should write the final internal JSON file.

Default output path:

```txt
output/alignment.json
```

The official MVP 1 JSON structure should use the following top-level fields:

```txt
schema_version
created_at
source
processing
lyrics
alignment
warnings
exports
```

Example minimal complete structure:

```json
{
  "schema_version": "0.1.0",
  "created_at": "2026-05-16T14:30:00-04:00",
  "source": {
    "audio_file": "examples/audio/example_song.wav",
    "lyrics_file": "examples/lyrics/example_lyrics.txt"
  },
  "processing": {
    "alignment_backend": {
      "name": "mfa",
      "version": "3.0.0",
      "acoustic_model": "english_us_arpa",
      "dictionary": "english_us_arpa"
    },
    "audio": {
      "input_file": "examples/audio/example_song.wav",
      "used_for_alignment": "output/intermediate/example_song_normalized.wav",
      "duration_seconds": 183.42,
      "sample_rate": 16000,
      "channels": 1,
      "format": "wav"
    },
    "lyrics": {
      "normalization": {
        "case_folded": true,
        "punctuation_removed_for_alignment": true,
        "blank_lines_removed": true,
        "original_text_preserved": true
      }
    }
  },
  "lyrics": {
    "line_count": 1,
    "lines": [
      {
        "id": 0,
        "text": "Never gonna give you up",
        "normalized_text": "never gonna give you up",
        "words": [
          {
            "id": 0,
            "text": "Never",
            "normalized_text": "never"
          },
          {
            "id": 1,
            "text": "gonna",
            "normalized_text": "gonna"
          },
          {
            "id": 2,
            "text": "give",
            "normalized_text": "give"
          },
          {
            "id": 3,
            "text": "you",
            "normalized_text": "you"
          },
          {
            "id": 4,
            "text": "up",
            "normalized_text": "up"
          }
        ]
      }
    ]
  },
  "alignment": {
    "level": "word",
    "quality_score": 0.94,
    "quality_score_method": "syncverse_heuristic_v1",
    "lines": [
      {
        "line_id": 0,
        "text": "Never gonna give you up",
        "start": 12.34,
        "end": 14.82,
        "duration": 2.48,
        "quality_score": 0.94,
        "words": [
          {
            "line_word_id": 0,
            "text": "Never",
            "start": 12.34,
            "end": 12.78,
            "duration": 0.44,
            "quality_score": 0.95,
            "source": "mfa"
          },
          {
            "line_word_id": 1,
            "text": "gonna",
            "start": 12.79,
            "end": 13.18,
            "duration": 0.39,
            "quality_score": 0.93,
            "source": "mfa"
          },
          {
            "line_word_id": 2,
            "text": "give",
            "start": 13.19,
            "end": 13.68,
            "duration": 0.49,
            "quality_score": 0.94,
            "source": "mfa"
          },
          {
            "line_word_id": 3,
            "text": "you",
            "start": 13.69,
            "end": 14.02,
            "duration": 0.33,
            "quality_score": 0.92,
            "source": "mfa"
          },
          {
            "line_word_id": 4,
            "text": "up",
            "start": 14.03,
            "end": 14.82,
            "duration": 0.79,
            "quality_score": 0.91,
            "source": "mfa"
          }
        ]
      }
    ]
  },
  "warnings": [],
  "exports": {
    "lrc": "output/example_song.lrc"
  }
}
```

---

## Step 12: `.lrc` Export

The `.lrc` export should be generated from:

```json
alignment.lines
```

not directly from MFA output.

Basic `.lrc` uses line-level timestamps.

Example:

```lrc
[00:12.34]Never gonna give you up
[00:15.10]Never gonna let you down
[00:18.05]Never gonna run around and desert you
```

Timestamp format:

```txt
[mm:ss.xx]
```

Conversion rule:

```txt
seconds → minutes, seconds, hundredths
```

Example:

```txt
12.34 seconds → [00:12.34]
75.82 seconds → [01:15.82]
```

If a line has no valid start timestamp:

```txt
Skip it and create a warning
```

or:

```txt
Include it without timestamp only if explicitly supported later
```

For MVP 1, skipping invalid lines with a warning is acceptable.

The `.lrc` output path should be recorded in:

```json
"exports": {
  "lrc": "output/song.lrc"
}
```

---

## Step 13: CLI Summary Output

After successful execution, the CLI should print a concise summary.

Example:

```txt
SyncVerse alignment complete.

Audio: examples/audio/song.wav
Lyrics: examples/lyrics/lyrics.txt
Backend: MFA
Aligned lines: 42
Warnings: 2

Outputs:
- JSON: output/alignment.json
- LRC: output/song.lrc
```

If warnings exist:

```txt
Warnings were generated. Review output/alignment.json for details.
```

If alignment fails:

```txt
Error: MFA alignment failed.
Details: output/logs/mfa_error.log
```

---

# Recommended MVP 1 Project Modules

Suggested Python package structure:

```txt
src/
└── syncverse/
    ├── __init__.py
    ├── cli.py
    ├── audio/
    │   ├── __init__.py
    │   ├── preprocess.py
    │   └── metadata.py
    ├── lyrics/
    │   ├── __init__.py
    │   ├── parser.py
    │   └── normalize.py
    ├── alignment/
    │   ├── __init__.py
    │   ├── base.py
    │   ├── mfa_backend.py
    │   ├── textgrid_parser.py
    │   └── reconstruct.py
    ├── quality/
    │   ├── __init__.py
    │   ├── scoring.py
    │   └── warnings.py
    ├── export/
    │   ├── __init__.py
    │   └── lrc.py
    ├── schema/
    │   ├── __init__.py
    │   └── models.py
    └── common/
        ├── __init__.py
        ├── paths.py
        └── errors.py
```

---

# Responsibilities by Module

## `cli.py`

Responsible for:

```txt
Parsing command-line arguments
Calling the pipeline
Displaying success/error summaries
```

Should not contain deep alignment logic.

---

## `audio/preprocess.py`

Responsible for:

```txt
Validating audio
Converting audio to MFA-compatible WAV
Creating intermediate audio files
```

Future extension:

```txt
Vocal separation support
User-provided vocal stem handling
```

---

## `lyrics/parser.py`

Responsible for:

```txt
Reading lyric text files
Splitting lines
Removing blank lines for MVP 1
Creating lyric line objects
```

---

## `lyrics/normalize.py`

Responsible for:

```txt
Lowercasing
Punctuation handling
Whitespace normalization
Alignment-safe text generation
```

---

## `alignment/base.py`

Defines the alignment backend interface.

Should contain something like:

```python
class AlignmentBackend:
    def align(self, audio_path, transcript_path, output_dir):
        raise NotImplementedError
```

---

## `alignment/mfa_backend.py`

Responsible for:

```txt
Preparing MFA command
Running MFA locally
Handling MFA errors
Returning MFA output file paths
```

Should be the only module that knows the details of MFA commands.

---

## `alignment/textgrid_parser.py`

Responsible for:

```txt
Reading MFA TextGrid output
Extracting word intervals
Ignoring silence intervals
Returning raw word timing objects
```

---

## `alignment/reconstruct.py`

Responsible for:

```txt
Mapping aligned words back to lyric lines
Creating line-level timing
Creating word-level timing under each line
```

---

## `quality/scoring.py`

Responsible for:

```txt
Computing word quality scores
Computing line quality scores
Computing overall alignment quality score
```

---

## `quality/warnings.py`

Responsible for:

```txt
Detecting suspicious timing
Generating warning objects
Assigning severity levels
```

---

## `export/lrc.py`

Responsible for:

```txt
Reading alignment lines
Formatting timestamps
Writing .lrc files
```

Should not depend on MFA.

---

## `schema/models.py`

Responsible for:

```txt
Defining internal data models
Ensuring JSON output shape stays consistent
```

This may use:

```txt
dataclasses
Pydantic
TypedDict
```

For MVP 1, Pydantic is nice but not mandatory.

---

# AI Agent Instructions

AI agents working on SyncVerse should follow these rules.

## Do Not Break the JSON Schema

The top-level MVP 1 JSON fields are fixed:

```txt
schema_version
created_at
source
processing
lyrics
alignment
warnings
exports
```

Do not rename these fields without explicit approval.

---

## Do Not Hardcode MFA Throughout the App

MFA-specific logic belongs in:

```txt
alignment/mfa_backend.py
alignment/textgrid_parser.py
```

Other modules should use generic alignment data structures.

---

## Do Not Introduce Cloud Dependencies

MVP 1 is local-first.

Do not add OpenAI transcription, cloud ASR, or cloud alignment APIs unless explicitly requested.

---

## Preserve Original Lyric Text

Normalized text may be used for alignment, but original lyric text must be preserved for:

```txt
JSON output
.lrc export
future lyric video rendering
```

---

## Keep `.lrc` Export Dependent on Internal JSON

The `.lrc` exporter should consume SyncVerse alignment data, not MFA files directly.

Correct:

```txt
MFA → SyncVerse JSON → LRC
```

Incorrect:

```txt
MFA → LRC
```

---

## Warnings Are Part of the Product

Do not treat warnings as optional logs only.

Warnings should be stored in the final JSON.

---

# Future Extension Points

The MVP 1 pipeline should leave room for these future additions.

## Optional Vocal Separation

Future pipeline:

```txt
Input song
  ↓
Demucs vocal separation
  ↓
vocals.wav
  ↓
MFA alignment
```

Future JSON location:

```json
"processing": {
  "vocal_separation": {
    "enabled": true,
    "backend": "demucs",
    "model": "htdemucs",
    "output_file": "output/intermediate/vocals.wav"
  }
}
```

---

## User-Provided Vocal Stem

Future CLI:

```bash
syncverse align vocals.wav lyrics.txt --input-is-vocals --out output/
```

The JSON can store:

```json
"processing": {
  "audio": {
    "input_file": "vocals.wav",
    "used_for_alignment": "vocals.wav",
    "audio_mode": "user_provided_vocals"
  }
}
```

---

## Enhanced LRC

Future export:

```lrc
[00:12.34]<00:12.34>Never <00:12.79>gonna <00:13.19>give <00:13.69>you <00:14.03>up
```

Future JSON location:

```json
"exports": {
  "lrc": "output/song.lrc",
  "enhanced_lrc": "output/song.enhanced.lrc"
}
```

---

## Lyric Video Rendering

Future renderer should consume:

```txt
alignment.lines
alignment.lines[].words
```

not `.lrc`.

---

## Custom MFA Model Training

Future versions may support custom-trained or adapted MFA acoustic models.

The JSON already supports this through:

```json
"processing": {
  "alignment_backend": {
    "name": "mfa",
    "version": "3.0.0",
    "acoustic_model": "custom_singing_model",
    "dictionary": "english_us_arpa"
  }
}
```

---

# Final MVP 1 Pipeline Summary

The MVP 1 pipeline is:

```txt
1. User runs syncverse align audio lyrics --out output
2. CLI validates audio, lyrics, and output path
3. Audio is converted to normalized WAV
4. Lyrics are parsed into lines and words
5. Lyrics are normalized for alignment while preserving original text
6. SyncVerse prepares an MFA-compatible corpus
7. MFA runs locally as the forced-alignment backend
8. SyncVerse parses MFA TextGrid output
9. Word timings are mapped back to original lyric lines
10. Line timings are calculated from word timings
11. Quality scores and warnings are generated
12. Internal alignment JSON is written
13. Basic line-level .lrc is exported from the JSON
14. CLI prints a summary of outputs and warnings
```

The most important implementation rule:

```txt
MFA is the alignment engine.
SyncVerse is the pipeline, schema, validator, exporter, and future lyric-video platform.
```

