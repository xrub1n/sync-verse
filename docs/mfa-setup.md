# Montreal Forced Aligner Setup

## Purpose

This document explains how to install and configure **Montreal Forced Aligner (MFA)** for **SyncVerse MVP 1**.

MFA is the forced-alignment tool used by SyncVerse MVP 1 to align a song audio file with a lyrics transcript and produce word-level timing data.

This document is meant to be used alongside:

- `docs/requirements.md`
- `docs/pipeline.md`
- `docs/architecture.md`
- `docs/json-schema.md`
- `docs/troubleshooting.md`

The pipeline document explains how MFA fits into the SyncVerse workflow. This document explains how to get MFA working locally.

---

## What MFA Does in SyncVerse

SyncVerse MVP 1 uses MFA to convert:

```txt
audio file + normalized lyrics transcript
```

into:

```txt
TextGrid alignment file
```

The TextGrid file contains timed intervals for words detected in the audio.

SyncVerse then parses the TextGrid and converts the timing data into the final `.syncverse.json` output format.

The simplified MVP 1 flow is:

```txt
audio.wav + lyrics.txt
        ↓
lyrics normalization
        ↓
MFA-ready transcript
        ↓
Montreal Forced Aligner
        ↓
.TextGrid file
        ↓
SyncVerse JSON output
```

---

## Important MVP 1 Assumptions

For MVP 1, SyncVerse assumes:

- The user has one audio file.
- The user has one plain-text lyrics file.
- The lyrics are in English.
- MFA is installed locally.
- MFA can be run from the command line.
- The required MFA acoustic model and dictionary are available locally.
- SyncVerse prepares MFA input files in an intermediate folder.
- SyncVerse does not commit large MFA model files to the GitHub repo.

---

## Recommended Install Method

The recommended way to install MFA is with Conda or Mamba.

MFA's official documentation recommends creating a dedicated environment and installing MFA from `conda-forge`.

Recommended environment name:

```txt
aligner
```

---

## Install Conda or Miniconda

If Conda is not installed, install Miniconda or Anaconda first.

Recommended:

- Miniconda for a lightweight install
- Anaconda if you already use it for other development work

After installation, verify Conda is available:

```bash
conda --version
```

---

## Option A: Install MFA with Conda

Create a new environment and install MFA:

```bash
conda create -n aligner -c conda-forge montreal-forced-aligner
```

Activate the environment:

```bash
conda activate aligner
```

Verify MFA is installed:

```bash
mfa version
```

You can also check the help output:

```bash
mfa --help
```

---

## Option B: Install MFA with Mamba

Mamba is a faster drop-in replacement for Conda.

Install Mamba into the base Conda environment:

```bash
conda activate base
conda install -c conda-forge mamba
```

Create the MFA environment:

```bash
mamba create -n aligner -c conda-forge montreal-forced-aligner
```

Activate the environment:

```bash
conda activate aligner
```

Verify MFA is installed:

```bash
mfa version
```

---

## Required MFA Models for MVP 1

SyncVerse MVP 1 should use English MFA models.

Recommended models:

```txt
english_us_arpa
```

For MVP 1, use:

```bash
mfa model download acoustic english_us_arpa
mfa model download dictionary english_us_arpa
```

After downloading, verify the acoustic model:

```bash
mfa model inspect acoustic english_us_arpa
```

Verify the dictionary:

```bash
mfa model inspect dictionary english_us_arpa
```

You can also list installed models:

```bash
mfa model list acoustic
mfa model list dictionary
```

---

## Model Storage Policy

Large MFA model files should **not** be committed to the SyncVerse GitHub repo.

Instead, the repo should document how to download the models locally.

There are two acceptable approaches.

---

## Option 1: Use MFA's Default Model Storage

This is the recommended MVP 1 approach.

When running:

```bash
mfa model download acoustic english_us_arpa
mfa model download dictionary english_us_arpa
```

MFA stores the models in its own local model directory.

Then SyncVerse can refer to the models by name:

```txt
english_us_arpa
```

This keeps the SyncVerse repo lightweight and avoids tracking large model files.

---

## Option 2: Use a Local `models/` Folder

If the project needs a visible local location for models, use:

```txt
models/
  README.md
  .gitkeep
```

The actual model files should still be ignored by Git.

The `models/README.md` file should explain:

- Which MFA models are required
- How to download them
- Where to place them if manually downloaded
- Whether SyncVerse expects model names or local paths

Recommended `.gitignore` entry:

```txt
models/*
!models/README.md
!models/.gitkeep
```

For MVP 1, prefer model names over hardcoded local model paths.

---

## Expected MFA Input Structure

SyncVerse should prepare MFA input files in an intermediate working directory.

Example project workspace:

```txt
projects/
  example_song/
    input/
      example_song.wav
      example_lyrics.txt

    working/
      normalized_lyrics.txt
      mfa_transcript.txt
      mfa_input/
        example_song.wav
        example_song.lab

    alignment/
      example_song.TextGrid

    output/
      example_song.syncverse.json

    logs/
      pipeline.log
```

The key MFA input folder is:

```txt
working/mfa_input/
```

For MVP 1, SyncVerse should place paired audio and transcript files there.

Example:

```txt
working/mfa_input/
  example_song.wav
  example_song.lab
```

The audio file and transcript file should share the same base name:

```txt
example_song.wav
example_song.lab
```

This pairing is important for MFA.

---

## Transcript Format

For MVP 1, SyncVerse should generate a `.lab` transcript file for MFA.

Example:

```txt
working/mfa_input/example_song.lab
```

The `.lab` file should contain the normalized lyrics transcript.

Example:

```txt
never gonna give you up
never gonna let you down
never gonna run around and desert you
```

The transcript should be alignment-friendly:

- Lowercased if configured
- Punctuation removed if configured
- Blank lines removed if configured
- Non-lyric annotations removed or handled
- Original lyrics preserved separately in the final JSON

The final JSON should still preserve the original lyric text.

---

## Audio Format for MFA

MFA generally works best when audio is in a clean, predictable format.

For MVP 1, SyncVerse should normalize audio used for alignment to:

```txt
wav
mono
16000 Hz
```

The original audio file should remain untouched.

The processed audio used for alignment should be written to an intermediate location.

Example:

```txt
output/intermediate/example_song_normalized.wav
```

In the final JSON, this distinction should be recorded:

```json
"processing": {
  "audio": {
    "input_file": "examples/audio/example_song.wav",
    "used_for_alignment": "output/intermediate/example_song_normalized.wav",
    "duration_seconds": 183.42,
    "sample_rate": 16000,
    "channels": 1,
    "format": "wav"
  }
}
```

---

## Manual MFA Validation Command

Before running the full SyncVerse pipeline, it is useful to manually validate the MFA input folder.

Example:

```bash
mfa validate ./working/mfa_input english_us_arpa english_us_arpa
```

This checks whether the corpus, dictionary, and acoustic model are usable.

Use this when debugging setup problems.

---

## Manual MFA Alignment Command

A typical manual MFA command for MVP 1 looks like:

```bash
mfa align ./working/mfa_input english_us_arpa english_us_arpa ./alignment
```

The general format is:

```bash
mfa align <corpus_directory> <dictionary> <acoustic_model> <output_directory>
```

For SyncVerse MVP 1:

```txt
<corpus_directory> = working/mfa_input
<dictionary>       = english_us_arpa
<acoustic_model>   = english_us_arpa
<output_directory> = alignment
```

After alignment succeeds, MFA should produce a TextGrid file.

Example:

```txt
alignment/example_song.TextGrid
```

---

## How SyncVerse Should Call MFA

In the actual SyncVerse implementation, MFA should be called from a dedicated module.

Recommended file:

```txt
src/syncverse/alignment/mfa_runner.py
```

This file should be responsible for:

- Building the MFA command
- Running MFA as a subprocess
- Capturing stdout and stderr
- Detecting failures
- Locating the generated `.TextGrid` file
- Returning useful errors to the pipeline

The CLI should not contain raw MFA subprocess logic.

The JSON builder should not contain raw MFA subprocess logic.

---

## Recommended SyncVerse MFA Configuration

SyncVerse should store MFA-related settings in a config module.

Recommended file:

```txt
src/syncverse/config/settings.py
```

Suggested settings:

```txt
MFA_BINARY_PATH=mfa
MFA_DICTIONARY_MODEL=english_us_arpa
MFA_ACOUSTIC_MODEL=english_us_arpa
MFA_TEMP_DIR=working/mfa_input
MFA_OUTPUT_DIR=alignment
```

If using environment variables, document them in:

```txt
.env.example
```

Example `.env.example` values:

```txt
MFA_BINARY_PATH=mfa
MFA_DICTIONARY_MODEL=english_us_arpa
MFA_ACOUSTIC_MODEL=english_us_arpa
SYNCVERSE_MODELS_DIR=./models
SYNCVERSE_PROJECTS_DIR=./projects
SYNCVERSE_OUTPUT_DIR=./output
```

---

## Expected MVP 1 Pipeline Responsibilities

The SyncVerse pipeline should handle MFA in these stages.

---

### 1. Prepare MFA Input

Recommended file:

```txt
src/syncverse/alignment/mfa_prepare.py
```

Responsibilities:

- Create the MFA working directory
- Copy or convert audio to the MFA input folder
- Generate the `.lab` transcript file
- Ensure audio and transcript base names match
- Store prepared paths in the pipeline context

---

### 2. Validate MFA Setup

Recommended file:

```txt
src/syncverse/alignment/mfa_models.py
```

Responsibilities:

- Confirm MFA can be called
- Confirm dictionary model is available
- Confirm acoustic model is available
- Provide useful error messages if models are missing

---

### 3. Run MFA

Recommended file:

```txt
src/syncverse/alignment/mfa_runner.py
```

Responsibilities:

- Run `mfa align`
- Capture command output
- Detect failure status
- Find the resulting TextGrid file
- Pass TextGrid path to the next pipeline step

---

### 4. Parse TextGrid

Recommended file:

```txt
src/syncverse/textgrid/parser.py
```

Responsibilities:

- Read the generated TextGrid file
- Extract word intervals
- Ignore empty/silence intervals
- Return structured timing data

---

### 5. Build SyncVerse JSON

Recommended file:

```txt
src/syncverse/export/json_builder.py
```

Responsibilities:

- Combine lyric structure with timing data
- Add processing metadata
- Add alignment backend metadata
- Add warnings if needed
- Produce the final `.syncverse.json` object

---

## Expected TextGrid Output

MFA should produce a `.TextGrid` file.

Example:

```txt
alignment/example_song.TextGrid
```

The TextGrid file is an intermediate output. SyncVerse should parse it and then generate:

```txt
output/example_song.syncverse.json
```

The final JSON should store the TextGrid location if useful for debugging.

Example:

```json
"alignment": {
  "level": "word",
  "quality_score": 0.91,
  "quality_score_method": "syncverse_heuristic_v1",
  "lines": []
}
```

If a future schema adds a direct TextGrid path, it should be documented in `docs/json-schema.md`.

---

## Updating MFA

To update MFA inside the Conda environment:

```bash
conda activate aligner
conda update -c conda-forge montreal-forced-aligner kalpy kaldi=*=cpu* --update-deps
```

Or with Mamba:

```bash
conda activate aligner
mamba update -c conda-forge montreal-forced-aligner kalpy kaldi=*=cpu* --update-deps
```

After updating, verify:

```bash
mfa version
```

---

## Quick Setup Checklist

Use this checklist to verify MFA is ready for SyncVerse MVP 1.

```txt
[ ] Conda or Mamba is installed
[ ] MFA environment exists
[ ] aligner environment is activated
[ ] `mfa version` works
[ ] acoustic model `english_us_arpa` is downloaded
[ ] dictionary `english_us_arpa` is downloaded
[ ] `mfa model inspect acoustic english_us_arpa` works
[ ] `mfa model inspect dictionary english_us_arpa` works
[ ] sample audio file exists
[ ] sample lyrics file exists
[ ] SyncVerse can generate `.lab` transcript files
[ ] audio and `.lab` file names match
[ ] `mfa validate` succeeds on the prepared input folder
[ ] `mfa align` produces a `.TextGrid` file
```

---

## Common Setup Issues

### `mfa` command not found

Possible causes:

- MFA is not installed
- Conda environment is not activated
- Shell/terminal has not refreshed after installation

Try:

```bash
conda activate aligner
mfa version
```

---

### Models are missing

Possible cause:

- Acoustic model or dictionary has not been downloaded

Try:

```bash
mfa model download acoustic english_us_arpa
mfa model download dictionary english_us_arpa
```

Then inspect them:

```bash
mfa model inspect acoustic english_us_arpa
mfa model inspect dictionary english_us_arpa
```

---

### MFA input files are not paired correctly

Possible cause:

- Audio file and transcript file do not share the same base name

Incorrect:

```txt
song.wav
lyrics.lab
```

Correct:

```txt
song.wav
song.lab
```

---

### TextGrid file is not created

Possible causes:

- MFA failed during alignment
- Output directory is wrong
- Input corpus is malformed
- Audio/transcript pairing is incorrect
- Transcript text does not match the audio closely enough

Check:

```txt
logs/pipeline.log
working/mfa_input/
alignment/
```

Try running:

```bash
mfa validate ./working/mfa_input english_us_arpa english_us_arpa
```

---

### Lyrics align poorly

Possible causes:

- Lyrics do not match the recording
- Song has a long intro before vocals
- Lyrics contain annotations like `[Chorus]`
- Background vocals confuse alignment
- Audio is noisy
- The full mix is harder to align than a vocal stem

Potential fixes:

- Clean the lyrics file
- Remove bracketed section labels
- Use a vocal-only stem if available
- Trim unrelated intro/outro sections for testing
- Inspect the generated `.lab` file

---

## Notes for AI Coding Agents

When implementing MFA-related issues:

1. Read `docs/pipeline.md` first.
2. Read `docs/architecture.md` before deciding where MFA code belongs.
3. Keep MFA preparation separate from MFA execution.
4. Keep MFA execution separate from TextGrid parsing.
5. Do not commit downloaded MFA model files.
6. Do not hardcode machine-specific absolute paths.
7. Use configurable model names or paths.
8. Capture MFA stdout and stderr for debugging.
9. Add clear errors when MFA is missing.
10. Add clear errors when models are missing.
11. Add clear errors when TextGrid output is missing.
12. Preserve intermediate files in debug mode.

---

## Summary

MFA is the core external alignment tool for SyncVerse MVP 1.

SyncVerse is responsible for preparing clean audio and transcript files, running MFA locally, parsing the generated TextGrid, and converting alignment results into the finalized SyncVerse JSON format.

The recommended MVP 1 setup is:

```txt
Conda/Mamba environment: aligner
MFA package: montreal-forced-aligner
Acoustic model: english_us_arpa
Dictionary: english_us_arpa
Input format: paired .wav + .lab files
Output format: .TextGrid parsed into .syncverse.json
```
