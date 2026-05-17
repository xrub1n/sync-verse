# SyncVerse Architecture

## Purpose of This Document

This document describes the MVP 1 architecture for **SyncVerse**.

The goal of this document is to explain how the codebase should be organized, where files should live, what each major module is responsible for, and how data moves through the system.

This document should be used alongside the other SyncVerse planning documents:

- `project-statement.md` explains the overall purpose, motivation, and product direction.
- `requirements.md` defines what MVP 1 must and must not do.
- `pipeline.md` defines the step-by-step processing flow from audio and lyrics input to final timed lyric JSON output.
- `architecture.md` explains how the project should be structured in code so the pipeline can be implemented cleanly.

The pipeline document should be treated as the source of truth for the MVP 1 workflow. This architecture document translates that pipeline into a codebase structure that both human developers and AI coding agents can follow.

---

## High-Level MVP 1 Architecture

SyncVerse MVP 1 is a **local-first forced-alignment pipeline**.

At a high level, the system takes:

1. An input audio file
2. A plain-text lyrics file
3. Local configuration/settings

And produces:

1. A finalized SyncVerse timing JSON file
2. Intermediate alignment files for debugging and traceability
3. Logs describing the success or failure of the pipeline run

The MVP 1 flow is:

```txt
Audio file + lyrics file
        ↓
Input validation
        ↓
Lyrics normalization and parsing
        ↓
MFA preparation
        ↓
Montreal Forced Aligner execution
        ↓
TextGrid parsing
        ↓
Word-level timing extraction
        ↓
Line-level timing construction
        ↓
Final SyncVerse JSON export
```

MVP 1 is focused on producing accurate lyric timing data. It does **not** include video rendering, a visual editor, SaaS deployment, user accounts, cloud storage, or a full GUI.

---

## Architectural Principles

The MVP 1 architecture should follow these principles:

### 1. Local-first

SyncVerse should run locally on the developer or artist's machine. Input files, intermediate files, model files, and final outputs should remain on the local file system.

This keeps MVP 1 simpler, avoids cloud costs, avoids account/authentication complexity, and better matches the target workflow for artists who may already have local audio files and lyrics.

### 2. Pipeline-oriented

The system should be structured around a clear pipeline where each step has a specific responsibility.

Each pipeline step should be small enough that it can be tested, debugged, and worked on independently.

### 3. File-system based

MVP 1 should use folders and files as the main interface between stages of the pipeline.

For example:

- Raw input files live in a project input folder.
- MFA-ready files live in an intermediate working folder.
- MFA output files live in an alignment output folder.
- Final SyncVerse JSON lives in a final output folder.

### 4. Expandable JSON output

The MVP 1 JSON structure should support the current needs of word-level and line-level lyric timing, while leaving room for future features such as:

- Pipeline versions
- Multiple audio sources
- Vocal-only stems
- Manual edits
- Confidence values
- Video rendering metadata
- Multiple exports
- Editor state

### 5. AI-agent friendly

The repo should be structured and documented clearly enough that AI coding agents can safely work on individual GitHub issues without needing to understand the entire project at once.

That means:

- Clear module boundaries
- Clear file responsibilities
- Clear naming conventions
- Clear documentation
- Clear test expectations
- Clear sample input/output files

---

## Recommended Repository Structure

The MVP 1 repo should use a structure similar to the one defined in the pipeline document.

```txt
syncverse/
  README.md
  .gitignore
  pyproject.toml / package.json
  .env.example

  docs/
    project-statement.md
    requirements.md
    pipeline.md
    architecture.md
    mfa-setup.md
    json-schema.md
    troubleshooting.md

  samples/
    README.md
    input/
      sample_song.wav
      sample_lyrics.txt
    expected-output/
      sample_song.syncverse.json

  projects/
    .gitkeep

  src/
    syncverse/
      __init__.py

      cli/
        __init__.py
        main.py

      config/
        __init__.py
        settings.py
        paths.py

      pipeline/
        __init__.py
        runner.py
        context.py
        steps.py

      input/
        __init__.py
        validators.py
        loaders.py

      lyrics/
        __init__.py
        normalizer.py
        parser.py
        models.py

      alignment/
        __init__.py
        mfa_runner.py
        mfa_prepare.py
        mfa_models.py

      textgrid/
        __init__.py
        parser.py
        models.py

      export/
        __init__.py
        json_builder.py
        writer.py
        schema.py

      logging/
        __init__.py
        logger.py

      errors/
        __init__.py
        exceptions.py

  tests/
    test_input_validation.py
    test_lyrics_normalizer.py
    test_lyrics_parser.py
    test_textgrid_parser.py
    test_json_builder.py
    test_pipeline_runner.py

  output/
    .gitkeep

  models/
    README.md
    .gitkeep
```

The exact runtime stack may change depending on the final implementation choice, but the conceptual separation should remain the same.

If the project uses Python, the `src/syncverse/` structure above is recommended.

If the project uses Node/TypeScript instead, the same architecture should still apply conceptually, but files would use `.ts` and the package structure would be adjusted accordingly.

---

## Root-Level Files

### `README.md`

The README should explain what SyncVerse is, how to set up the project, how to run MVP 1, and where to find the major docs.

It should include:

- Short project summary
- MVP 1 scope
- Setup instructions
- Basic usage example
- Link to `docs/pipeline.md`
- Link to `docs/requirements.md`
- Link to `docs/architecture.md`

The README should not contain every detail. It should act as the entry point into the project.

---

### `.gitignore`

The `.gitignore` file should prevent large, generated, or local-only files from being committed.

It should ignore:

```txt
output/
projects/
*.wav
*.mp3
*.flac
*.TextGrid
*.log
.env
.venv/
node_modules/
__pycache__/
models/*
```

The repo may keep placeholder files such as `.gitkeep` or README files inside otherwise ignored directories.

---

### `pyproject.toml` / `package.json`

This file defines the project dependencies and development commands.

For a Python implementation, `pyproject.toml` should contain:

- Project metadata
- Python version requirement
- Runtime dependencies
- Dev/test dependencies
- CLI entry point if applicable

For a TypeScript implementation, `package.json` should contain:

- Scripts
- Dependencies
- Dev dependencies
- Build/test commands

---

### `.env.example`

The `.env.example` file should document optional local environment variables.

For MVP 1, this may include:

```txt
SYNCVERSE_PROJECTS_DIR=./projects
SYNCVERSE_OUTPUT_DIR=./output
SYNCVERSE_MODELS_DIR=./models
MFA_BINARY_PATH=mfa
MFA_ACOUSTIC_MODEL=english_us_arpa
MFA_DICTIONARY_MODEL=english_us_arpa
```

Actual `.env` files should not be committed.

---

## Documentation Folder

### `docs/project-statement.md`

This document explains the overall project vision.

It should answer:

- What is SyncVerse?
- Who is it for?
- What problem does it solve?
- Why is the project local-first?
- What is the long-term product direction?
- How does MVP 1 fit into the larger vision?

This document is product-facing and vision-facing.

---

### `docs/requirements.md`

This document defines the MVP 1 requirements.

It should include:

- MVP 1 functional requirements
- MVP 1 non-functional requirements
- In-scope features
- Out-of-scope features
- Input requirements
- Output requirements
- Error handling expectations
- Acceptance criteria

This document answers what the system must do.

---

### `docs/pipeline.md`

This document defines the exact MVP 1 pipeline.

It should include:

- Required input files
- Expected output files
- Step-by-step pipeline flow
- Intermediate files
- MFA preparation process
- MFA execution process
- TextGrid parsing process
- JSON export process
- Validation expectations
- Troubleshooting notes

This document answers how the system processes files from start to finish.

The pipeline document should be treated as the source of truth for the processing flow.

---

### `docs/architecture.md`

This document explains how the project is organized in code.

It should include:

- Repository structure
- Folder responsibilities
- Module responsibilities
- Data flow between modules
- Important design decisions
- Future expansion points

This document answers where code belongs and how the codebase should be organized.

---

### `docs/mfa-setup.md`

This document should explain how to install and configure Montreal Forced Aligner for local development.

It should include:

- MFA installation instructions
- Required MFA models
- Where model files should live
- How to verify MFA is installed
- How to run a basic MFA command manually
- Common MFA setup issues

Large MFA model files should generally not be committed directly into the GitHub repo.

Instead, the repo should document how to download them, where to place them locally, and how the pipeline expects to find them.

---

### `docs/json-schema.md`

This document should explain the finalized MVP 1 SyncVerse JSON structure.

It should include:

- Top-level JSON fields
- Project metadata fields
- Input metadata fields
- Pipeline metadata fields
- Word timing fields
- Line timing fields
- Future expansion fields
- Example JSON object

This document should match the JSON schema implemented in `src/syncverse/export/schema.py`.

---

### `docs/troubleshooting.md`

This document should collect common errors and solutions.

For MVP 1, likely troubleshooting topics include:

- MFA is not installed
- MFA binary cannot be found
- MFA model is missing
- Audio file format is unsupported
- Lyrics file is empty or malformed
- TextGrid output is missing
- Alignment failed
- JSON output validation failed

---

## Samples Folder

The `samples/` folder should contain small files that demonstrate the expected MVP 1 workflow.

### `samples/README.md`

This file should explain how to use the sample input files.

It should include:

- What sample files are included
- How to run the pipeline on the sample files
- What output should be produced
- Where expected output is stored

---

### `samples/input/sample_song.wav`

This is a small sample audio file used for local testing and demonstration.

The sample should be short enough to keep the repository lightweight.

If the audio file is too large or cannot be committed for licensing reasons, use a placeholder and document where the developer should place their own sample file.

---

### `samples/input/sample_lyrics.txt`

This is the lyrics file paired with the sample audio file.

For MVP 1, the lyrics file should be plain text.

The lyrics should be formatted in a way that reflects expected user input.

Example:

```txt
First line of the song
Second line of the song
Third line of the song
```

---

### `samples/expected-output/sample_song.syncverse.json`

This file should show the expected final JSON output shape for the sample input.

It does not need to be perfect at first, but it should represent the target output format for MVP 1.

This file helps AI agents and human developers understand what the final pipeline result should look like.

---

## Projects Folder

### `projects/`

The `projects/` folder is intended for local user/project workspaces.

A project workspace may look like this:

```txt
projects/
  sample_song_project/
    input/
      audio.wav
      lyrics.txt

    working/
      normalized_lyrics.txt
      mfa_transcript.txt
      mfa_input/
        sample_song.wav
        sample_song.lab

    alignment/
      sample_song.TextGrid

    output/
      sample_song.syncverse.json

    logs/
      pipeline.log
```

The project folder structure mirrors the pipeline document.

Each project should keep its inputs, intermediate files, alignment outputs, final outputs, and logs grouped together.

In MVP 1, this can be simple and file-system based. A database is not required.

---

## Source Folder

The source folder contains the actual MVP 1 implementation.

For a Python implementation, all main project code should live under:

```txt
src/syncverse/
```

---

## CLI Module

### `src/syncverse/cli/main.py`

This file is the command-line entry point for MVP 1.

Responsibilities:

- Accept user-provided input paths
- Accept output/project directory options
- Load configuration
- Create a pipeline context
- Start the pipeline runner
- Print clear success or failure messages

Example CLI usage:

```bash
syncverse align --audio ./samples/input/sample_song.wav --lyrics ./samples/input/sample_lyrics.txt --output ./output/sample_song.syncverse.json
```

The CLI should not contain the full pipeline logic. It should delegate to the pipeline module.

---

## Config Module

### `src/syncverse/config/settings.py`

This file stores project-level settings.

Responsibilities:

- Load default settings
- Load optional environment variables
- Store MFA configuration
- Store default folder paths
- Store debug mode settings

Example settings:

- Default projects directory
- Default output directory
- Default models directory
- MFA binary path
- MFA acoustic model name/path
- MFA dictionary model name/path

---

### `src/syncverse/config/paths.py`

This file handles path construction and path normalization.

Responsibilities:

- Resolve project root paths
- Build project workspace paths
- Build working directory paths
- Build MFA input/output paths
- Build final output paths
- Ensure required directories exist

The pipeline should use this module rather than manually assembling paths throughout the codebase.

---

## Pipeline Module

### `src/syncverse/pipeline/context.py`

This file defines the pipeline context object.

The context object should carry shared data through the pipeline.

It may include:

- Audio input path
- Lyrics input path
- Project directory
- Working directory
- MFA output path
- Final JSON output path
- Loaded settings
- Debug mode flag
- Intermediate result references

The context object helps avoid passing many separate arguments between pipeline steps.

---

### `src/syncverse/pipeline/runner.py`

This file orchestrates the full MVP 1 pipeline.

Responsibilities:

- Run each pipeline step in order
- Stop the pipeline if a required step fails
- Log progress
- Return a clear success/failure result
- Avoid containing low-level parsing or MFA details directly

The runner should follow the sequence defined in `docs/pipeline.md`.

Expected order:

1. Validate inputs
2. Load lyrics
3. Normalize lyrics
4. Parse lyrics into lines/words
5. Prepare MFA files
6. Run MFA
7. Parse TextGrid output
8. Build SyncVerse JSON
9. Validate JSON
10. Write final output

---

### `src/syncverse/pipeline/steps.py`

This file may contain wrapper functions for individual pipeline stages.

Responsibilities:

- Provide clean step-level functions
- Keep `runner.py` readable
- Make individual pipeline stages easier to test or replace

Example functions:

```py
validate_inputs_step(context)
load_lyrics_step(context)
normalize_lyrics_step(context)
prepare_mfa_step(context)
run_mfa_step(context)
parse_textgrid_step(context)
build_json_step(context)
write_output_step(context)
```

---

## Input Module

### `src/syncverse/input/validators.py`

This file validates required MVP 1 inputs.

Responsibilities:

- Confirm the audio file exists
- Confirm the lyrics file exists
- Confirm the lyrics file is not empty
- Confirm file extensions are acceptable
- Confirm output directory can be created/written to

Validation should happen early in the pipeline so failures are clear.

---

### `src/syncverse/input/loaders.py`

This file loads input file contents.

Responsibilities:

- Read lyrics text from disk
- Load basic audio file metadata if needed
- Return clean input data structures
- Avoid performing normalization directly

This module should load data, not transform it deeply.

---

## Lyrics Module

### `src/syncverse/lyrics/normalizer.py`

This file normalizes lyrics for alignment.

Responsibilities:

- Normalize whitespace
- Preserve line breaks where needed
- Remove or standardize characters that may confuse MFA
- Create MFA-friendly transcript text
- Preserve references to the original lyrics text

The normalizer should be careful not to destroy useful lyric structure.

MVP 1 should preserve enough information to reconstruct line-level timing from word-level alignment.

---

### `src/syncverse/lyrics/parser.py`

This file parses lyrics into structured line and word objects.

Responsibilities:

- Split lyrics into lines
- Split lines into words/tokens
- Assign line indexes
- Assign word indexes
- Preserve original text
- Preserve normalized text

The parser prepares lyrics data for later matching with TextGrid word timings.

---

### `src/syncverse/lyrics/models.py`

This file defines internal lyric data models.

Possible models:

- `LyricLine`
- `LyricWord`
- `ParsedLyrics`

Example conceptual structure:

```py
LyricLine:
  line_index: int
  original_text: str
  normalized_text: str
  words: list[LyricWord]

LyricWord:
  word_index: int
  line_index: int
  original_text: str
  normalized_text: str
```

These models are internal pipeline structures, not necessarily the same as the final JSON format.

---

## Alignment Module

### `src/syncverse/alignment/mfa_prepare.py`

This file prepares files for Montreal Forced Aligner.

Responsibilities:

- Create MFA working directory
- Copy or convert audio into the MFA input location
- Create transcript/lab files expected by MFA
- Ensure file names match MFA expectations
- Store prepared MFA input paths in the pipeline context

MFA usually expects paired audio and transcript files in a specific corpus format. This module isolates those details.

---

### `src/syncverse/alignment/mfa_runner.py`

This file runs Montreal Forced Aligner.

Responsibilities:

- Build the MFA command
- Execute MFA as a subprocess
- Capture stdout/stderr
- Detect command success/failure
- Locate the generated TextGrid output
- Report meaningful errors when MFA fails

This module should not parse TextGrid files. It should only run MFA and return the path to MFA output.

---

### `src/syncverse/alignment/mfa_models.py`

This file stores logic related to MFA model configuration.

Responsibilities:

- Resolve acoustic model path/name
- Resolve dictionary model path/name
- Validate required models are available
- Provide helpful messages if models are missing

Large model files should not be hardcoded into the repo. This module should support local paths or model names depending on how MFA is configured.

---

## TextGrid Module

### `src/syncverse/textgrid/parser.py`

This file parses MFA TextGrid output.

Responsibilities:

- Read TextGrid files
- Extract word intervals
- Ignore silence/spn/empty intervals where appropriate
- Convert intervals into internal word timing objects
- Preserve start and end times

This parser should produce clean internal timing data that the export module can use.

---

### `src/syncverse/textgrid/models.py`

This file defines internal TextGrid timing models.

Possible models:

- `AlignedWord`
- `AlignmentResult`

Example conceptual structure:

```py
AlignedWord:
  text: str
  start: float
  end: float
  confidence: float | None

AlignmentResult:
  words: list[AlignedWord]
  source_textgrid_path: str
```

MFA may not provide confidence values directly in MVP 1. If confidence is not available, the field can be omitted or set to `null` depending on the finalized JSON schema.

---

## Export Module

### `src/syncverse/export/json_builder.py`

This file builds the final SyncVerse JSON object.

Responsibilities:

- Combine input metadata, parsed lyrics, and alignment timings
- Create word-level timing entries
- Create line-level timing entries
- Preserve original lyric text
- Add pipeline metadata
- Add source file metadata
- Follow the finalized MVP 1 JSON structure

This module should be the main bridge between internal pipeline data and the final public output format.

---

### `src/syncverse/export/writer.py`

This file writes final output files to disk.

Responsibilities:

- Create output directories if needed
- Write JSON files
- Format JSON consistently
- Avoid overwriting files unexpectedly unless explicitly allowed
- Return the final output path

---

### `src/syncverse/export/schema.py`

This file defines or loads the MVP 1 JSON schema.

Responsibilities:

- Store the expected JSON schema
- Validate generated JSON before writing or after building
- Provide clear validation errors

This module should match the structure documented in `docs/json-schema.md`.

---

## Logging Module

### `src/syncverse/logging/logger.py`

This file centralizes logging behavior.

Responsibilities:

- Configure console logging
- Configure optional file logging
- Provide consistent log formatting
- Support debug mode
- Avoid scattered print statements throughout the codebase

Pipeline steps should use this logger for progress and error reporting.

---

## Errors Module

### `src/syncverse/errors/exceptions.py`

This file defines custom exceptions.

Possible exceptions:

- `SyncVerseError`
- `InputValidationError`
- `LyricsParsingError`
- `MFASetupError`
- `MFARuntimeError`
- `TextGridParsingError`
- `JSONExportError`

Custom exceptions make it easier for the CLI and pipeline runner to provide clear user-facing error messages.

---

## Tests Folder

The `tests/` folder should verify that major MVP 1 modules work independently and together.

### `tests/test_input_validation.py`

Tests for:

- Missing audio file
- Missing lyrics file
- Empty lyrics file
- Invalid output directory
- Unsupported file extension

---

### `tests/test_lyrics_normalizer.py`

Tests for:

- Whitespace normalization
- Punctuation handling
- Line preservation
- Empty line handling
- Special character handling

---

### `tests/test_lyrics_parser.py`

Tests for:

- Splitting lyrics into lines
- Splitting lines into words
- Preserving original text
- Assigning line indexes
- Assigning word indexes

---

### `tests/test_textgrid_parser.py`

Tests for:

- Reading TextGrid files
- Extracting word intervals
- Ignoring silence intervals
- Handling empty intervals
- Returning correct start/end times

---

### `tests/test_json_builder.py`

Tests for:

- Required top-level JSON fields
- Word-level timing output
- Line-level timing output
- Metadata fields
- Schema validation

---

### `tests/test_pipeline_runner.py`

Tests for:

- Pipeline step ordering
- Successful sample run
- Failure behavior when inputs are missing
- Failure behavior when MFA output is missing

Full integration tests that require MFA may be optional or marked separately because MFA setup can vary between environments.

---

## Output Folder

### `output/`

The `output/` folder is the default location for generated final files.

Example:

```txt
output/
  sample_song.syncverse.json
```

Generated output files should generally not be committed unless they are small sample outputs used for documentation or testing.

---

## Models Folder

### `models/`

The `models/` folder is the suggested local location for MFA-related models if the developer chooses to store them inside the project directory.

Example:

```txt
models/
  acoustic/
  dictionaries/
```

However, large model files should usually not be committed to GitHub.

The repo should include:

```txt
models/
  README.md
  .gitkeep
```

The `models/README.md` file should explain:

- Which MFA models are required
- How to download them
- Where to place them
- Whether the pipeline expects model names or local paths

---

## Data Flow Between Modules

The MVP 1 runtime data flow should look like this:

```txt
CLI
 ↓
Config + Path Setup
 ↓
Pipeline Context
 ↓
Input Validators / Loaders
 ↓
Lyrics Normalizer / Parser
 ↓
MFA Preparation
 ↓
MFA Runner
 ↓
TextGrid Parser
 ↓
JSON Builder
 ↓
Schema Validator
 ↓
Output Writer
```

Each module should pass structured data forward rather than relying on global state.

The pipeline context may be used to hold paths and intermediate results, but individual modules should still have clear inputs and outputs.

---

## MVP 1 Runtime Flow

A typical MVP 1 run should follow this sequence:

1. User runs the CLI with an audio file and lyrics file.
2. CLI loads settings and creates a pipeline context.
3. Input validator confirms required files exist.
4. Lyrics loader reads the lyrics text.
5. Lyrics normalizer creates MFA-friendly lyric text.
6. Lyrics parser creates structured lyric line and word objects.
7. MFA preparation creates the expected MFA corpus files.
8. MFA runner executes Montreal Forced Aligner.
9. MFA outputs a TextGrid file.
10. TextGrid parser extracts word-level timing intervals.
11. JSON builder combines lyrics and timing data.
12. Schema validator checks the final JSON structure.
13. Writer saves the final `.syncverse.json` file.
14. CLI prints the final output path and success message.

---

## Intermediate Files

MVP 1 should preserve intermediate files when debug mode is enabled.

Useful intermediate files include:

```txt
working/
  normalized_lyrics.txt
  mfa_transcript.txt
  mfa_input/
    audio.wav
    audio.lab

alignment/
  audio.TextGrid

logs/
  pipeline.log
```

Keeping these files makes debugging much easier, especially when MFA fails or when alignment output looks incorrect.

In non-debug mode, the pipeline may clean up temporary files, but it should never delete user-provided input files.

---

## Final JSON Output Responsibility

The final SyncVerse JSON file is the main MVP 1 product output.

It should contain:

- Project metadata
- Input file metadata
- Pipeline metadata
- Original lyric lines
- Normalized lyric lines
- Word-level timings
- Line-level timings
- Alignment source information
- Future expansion fields where appropriate

The exact structure should match the finalized MVP 1 JSON structure defined in the pipeline and JSON schema documentation.

The JSON builder should be the only module responsible for assembling this final structure.

---

## External Dependencies

MVP 1 depends on Montreal Forced Aligner.

Other likely dependencies may include:

- A TextGrid parsing library, or a custom parser
- JSON schema validation library
- Audio metadata library, if needed
- CLI argument parsing library
- Testing framework

External dependencies should be documented clearly in setup instructions.

---

## Montreal Forced Aligner Boundary

MFA should be treated as an external tool.

The SyncVerse codebase should be responsible for:

- Preparing MFA input files
- Running MFA
- Capturing errors
- Reading MFA output

The SyncVerse codebase should not attempt to modify MFA internals.

This separation keeps MVP 1 realistic and makes the project easier to debug.

---

## Error Handling Strategy

MVP 1 should fail clearly and early.

Examples:

- If the audio file is missing, fail during input validation.
- If the lyrics file is empty, fail during input validation.
- If MFA is not installed, fail during MFA setup validation.
- If MFA does not produce a TextGrid file, fail during alignment output validation.
- If JSON validation fails, fail before writing or clearly mark the output as invalid.

Errors should be written in a way that helps both users and AI agents understand what went wrong.

---

## Logging Strategy

The pipeline should log major stages:

```txt
Starting SyncVerse MVP 1 pipeline
Validating inputs
Loading lyrics
Normalizing lyrics
Preparing MFA input
Running Montreal Forced Aligner
Parsing TextGrid output
Building SyncVerse JSON
Writing output file
Pipeline completed successfully
```

When failures happen, logs should include enough information to diagnose the problem without overwhelming the user.

---

## MVP 1 Boundaries

MVP 1 includes:

- Local CLI pipeline
- Audio + lyrics input
- Lyrics preprocessing
- MFA integration
- TextGrid parsing
- Word-level timing output
- Line-level timing output
- Final SyncVerse JSON export
- Basic validation
- Basic tests
- Documentation for setup and usage

MVP 1 does not include:

- SaaS deployment
- User accounts
- Cloud file storage
- Web-based editor
- Manual timing correction UI
- Video rendering
- Lyric video templates
- Demucs vocal separation as a required step
- Multi-song project management
- Advanced confidence scoring
- Real-time playback preview

---

## Future Expansion Points

The architecture should leave room for:

### Optional vocal separation

A future module could be added:

```txt
src/syncverse/audio/
  demucs_runner.py
  stem_selector.py
```

This would allow the pipeline to optionally create or use a vocal-only stem before alignment.

---

### Video rendering

A future module could be added:

```txt
src/syncverse/rendering/
  lyric_video_renderer.py
  templates.py
```

This would use the finalized timing JSON to generate lyric videos.

---

### Manual timing editor

A future editor could use the JSON output as its main data source.

Potential future folders:

```txt
app/
  frontend/
  backend/
```

or:

```txt
editor/
```

---

### Pipeline versioning

Future JSON files may include detailed pipeline version metadata.

Example:

```json
{
  "pipeline": {
    "name": "syncverse-mvp1-alignment",
    "version": "1.0.0",
    "steps": []
  }
}
```

This allows future versions of SyncVerse to understand how an output file was produced.

---

### Multiple audio sources

Future versions may support:

- Original full mix
- Vocal-only stem
- Instrumental stem
- User-provided alternate audio
- Generated preview audio

The MVP 1 JSON should not block this future expansion.

---

## AI Agent Implementation Guidance

AI coding agents should follow these rules when working in the repo:

1. Read `docs/requirements.md` before implementing a feature.
2. Read `docs/pipeline.md` before modifying pipeline behavior.
3. Read `docs/architecture.md` before deciding where files or code should go.
4. Keep modules focused on their stated responsibilities.
5. Do not place full pipeline logic inside the CLI.
6. Do not place MFA subprocess logic inside the JSON export module.
7. Do not place TextGrid parsing logic inside the MFA runner.
8. Add or update tests when implementing behavior.
9. Preserve the finalized MVP 1 JSON structure.
10. Keep future expansion in mind, but do not overbuild beyond MVP 1 requirements.

---

## Summary

The SyncVerse MVP 1 architecture should be simple, local-first, and pipeline-focused.

The main architectural goal is to keep the system modular enough that each part of the forced-alignment workflow can be implemented, tested, debugged, and expanded independently.

The pipeline document defines what happens.

The architecture document defines where that behavior belongs in the codebase.
