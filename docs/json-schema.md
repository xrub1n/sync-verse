# SyncVerse MVP 1 JSON Schema

## Purpose

This document defines the expected JSON output structure for **SyncVerse MVP 1**.

The final MVP 1 JSON file is the main output of the SyncVerse forced-alignment pipeline. It stores:

- Source input file references
- Processing and alignment metadata
- Original and normalized lyrics
- Line-level alignment timings
- Word-level alignment timings
- Quality scores and warnings
- Optional export file references

This document is meant to be used alongside:

- `docs/project-statement.md`
- `docs/requirements.md`
- `docs/pipeline.md`
- `docs/architecture.md`
- `example-json-mvp1.json`

The `example-json-mvp1.json` file is a concrete example of this schema using sample song data. This document explains the structure, meaning, and rules behind that example.

---

## Relationship to `example-json-mvp1.json`

The file:

```txt
example-json-mvp1.json
```

is an example instance of the MVP 1 output format.

It answers:

> What should a real SyncVerse MVP 1 JSON output look like?

This document answers:

> What does each field mean, which fields are required, and what rules should generated JSON files follow?

If the example JSON changes, this schema document should be updated. If this schema document changes, the example JSON should be updated.

---

## Top-Level Structure

Every SyncVerse MVP 1 output JSON file should follow this structure:

```json
{
  "schema_version": "0.1.0",
  "created_at": "2026-05-16T14:30:00-04:00",
  "source": {},
  "processing": {},
  "lyrics": {},
  "alignment": {},
  "warnings": [],
  "exports": {}
}
```

## Required Top-Level Fields

| Field | Type | Required | Description |
|---|---|---:|---|
| `schema_version` | string | yes | Version of the SyncVerse JSON schema |
| `created_at` | string | yes | Timestamp when the JSON output was created |
| `source` | object | yes | References to the original source files |
| `processing` | object | yes | Metadata about audio, lyrics, and alignment processing |
| `lyrics` | object | yes | Original and normalized lyric structure |
| `alignment` | object | yes | Timed line-level and word-level alignment results |
| `warnings` | array | yes | Non-fatal warnings produced during processing |
| `exports` | object | no | Paths to optional derived export files |

---

# `schema_version`

## Example

```json
"schema_version": "0.1.0"
```

## Type

`string`

## Required

Yes

## Description

Identifies the version of the SyncVerse JSON schema.

This value represents the output JSON structure, not the application version or the Montreal Forced Aligner version.

## MVP 1 Rule

For MVP 1 planning, use:

```json
"schema_version": "0.1.0"
```

This can be updated later if the JSON structure changes before or after MVP 1.

---

# `created_at`

## Example

```json
"created_at": "2026-05-16T14:30:00-04:00"
```

## Type

`string`

## Required

Yes

## Description

Timestamp for when the SyncVerse JSON output file was generated.

## Format

Use ISO 8601 format.

Examples:

```txt
2026-05-16T14:30:00-04:00
2026-05-16T18:30:00Z
```

---

# `source`

## Example

```json
"source": {
  "audio_file": "examples/audio/example_song.wav",
  "lyrics_file": "examples/lyrics/example_lyrics.txt"
}
```

## Type

`object`

## Required

Yes

## Description

Stores references to the original user-provided source files.

This section should point to the source files before SyncVerse performs normalization, conversion, or alignment preparation.

## Fields

| Field | Type | Required | Description |
|---|---|---:|---|
| `audio_file` | string | yes | Path to the original audio file provided to SyncVerse |
| `lyrics_file` | string | yes | Path to the original lyrics text file provided to SyncVerse |

## Notes

Paths should preferably be relative to the project root or project workspace when possible.

Example:

```json
"audio_file": "examples/audio/example_song.wav"
```

Avoid storing machine-specific absolute paths unless needed for local debugging.

---

# `processing`

## Example

```json
"processing": {
  "alignment_backend": {},
  "audio": {},
  "lyrics": {}
}
```

## Type

`object`

## Required

Yes

## Description

Stores information about how the source files were processed.

This section is useful for debugging and reproducibility. It lets a developer or AI agent understand what tool was used, what models were used, how the audio was prepared, and how the lyrics were normalized.

## Required Child Fields

| Field | Type | Required | Description |
|---|---|---:|---|
| `alignment_backend` | object | yes | Information about the forced-alignment tool |
| `audio` | object | yes | Audio processing metadata |
| `lyrics` | object | yes | Lyrics normalization metadata |

---

# `processing.alignment_backend`

## Example

```json
"alignment_backend": {
  "name": "mfa",
  "version": "3.0.0",
  "acoustic_model": "english_us_arpa",
  "dictionary": "english_us_arpa"
}
```

## Type

`object`

## Required

Yes

## Description

Identifies the forced-alignment backend and model configuration used to generate the timing data.

For MVP 1, the backend is Montreal Forced Aligner.

## Fields

| Field | Type | Required | Description |
|---|---|---:|---|
| `name` | string | yes | Short name of the alignment backend |
| `version` | string or null | no | Version of the alignment backend |
| `acoustic_model` | string or null | yes | Acoustic model used by MFA |
| `dictionary` | string or null | yes | Pronunciation dictionary used by MFA |

## MVP 1 Rule

For MVP 1, use:

```json
"name": "mfa"
```

Recommended model values:

```json
"acoustic_model": "english_us_arpa",
"dictionary": "english_us_arpa"
```

---

# `processing.audio`

## Example

```json
"audio": {
  "input_file": "examples/audio/example_song.wav",
  "used_for_alignment": "output/intermediate/example_song_normalized.wav",
  "duration_seconds": 183.42,
  "sample_rate": 16000,
  "channels": 1,
  "format": "wav"
}
```

## Type

`object`

## Required

Yes

## Description

Stores information about the audio file used by the pipeline.

This section distinguishes between the original audio input and any processed or normalized audio file actually sent into MFA.

## Fields

| Field | Type | Required | Description |
|---|---|---:|---|
| `input_file` | string | yes | Original audio file path |
| `used_for_alignment` | string | yes | Audio file path actually used by MFA |
| `duration_seconds` | number or null | no | Duration of the audio in seconds |
| `sample_rate` | number or null | no | Sample rate of the audio used for alignment |
| `channels` | number or null | no | Number of audio channels used for alignment |
| `format` | string or null | no | Audio format used for alignment |

## MVP 1 Notes

For MVP 1, MFA-friendly audio should generally be normalized into a format such as:

```txt
wav, 16000 Hz, mono
```

If SyncVerse converts the source audio before MFA, `input_file` and `used_for_alignment` may be different.

Example:

```json
"input_file": "examples/audio/example_song.mp3",
"used_for_alignment": "output/intermediate/example_song_normalized.wav"
```

---

# `processing.lyrics`

## Example

```json
"lyrics": {
  "normalization": {
    "case_folded": true,
    "punctuation_removed_for_alignment": true,
    "blank_lines_removed": true,
    "original_text_preserved": true
  }
}
```

## Type

`object`

## Required

Yes

## Description

Stores metadata about how lyrics were normalized before alignment.

## Fields

| Field | Type | Required | Description |
|---|---|---:|---|
| `normalization` | object | yes | Details about lyric normalization behavior |

---

# `processing.lyrics.normalization`

## Type

`object`

## Required

Yes

## Fields

| Field | Type | Required | Description |
|---|---|---:|---|
| `case_folded` | boolean | yes | Whether lyrics were lowercased for alignment |
| `punctuation_removed_for_alignment` | boolean | yes | Whether punctuation was removed from alignment text |
| `blank_lines_removed` | boolean | yes | Whether blank lines were removed during processing |
| `original_text_preserved` | boolean | yes | Whether original text was preserved in the JSON |

## MVP 1 Rule

Original lyric text should always be preserved.

Therefore:

```json
"original_text_preserved": true
```

---

# `lyrics`

## Example

```json
"lyrics": {
  "line_count": 3,
  "lines": []
}
```

## Type

`object`

## Required

Yes

## Description

Stores the lyric text structure before timing alignment is applied.

This section is primarily about the lyrics themselves:

- How many lines exist
- What each original line says
- What each normalized line says
- What words belong to each line

Timing data belongs in the `alignment` section, not this section.

## Fields

| Field | Type | Required | Description |
|---|---|---:|---|
| `line_count` | number | yes | Number of lyric lines |
| `lines` | array | yes | Ordered lyric line objects |

---

# `lyrics.lines`

## Example

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
    }
  ]
}
```

## Type

`array<object>`

## Required

Yes

## Description

Each object in `lyrics.lines` represents one lyric line from the source lyrics file.

## Fields

| Field | Type | Required | Description |
|---|---|---:|---|
| `id` | number | yes | Zero-based line ID |
| `text` | string | yes | Original lyric line text |
| `normalized_text` | string | yes | Normalized lyric line text used for alignment |
| `words` | array | yes | Ordered words belonging to this lyric line |

## Line ID Rule

Line IDs should be zero-based and should match the line IDs used in `alignment.lines`.

Example:

```json
"id": 0
```

The first lyric line has ID `0`, the second has ID `1`, and so on.

---

# `lyrics.lines.words`

## Example

```json
{
  "id": 0,
  "text": "Never",
  "normalized_text": "never"
}
```

## Type

`array<object>`

## Required

Yes

## Description

Each object in `lyrics.lines[].words` represents a word/token from a lyric line before timing is applied.

This section preserves the lyric structure. The timed version of each word appears later in `alignment.lines[].words`.

## Fields

| Field | Type | Required | Description |
|---|---|---:|---|
| `id` | number | yes | Zero-based word ID within the line |
| `text` | string | yes | Original word text |
| `normalized_text` | string | yes | Normalized word text used for alignment |

## Word ID Rule

Word IDs are zero-based **within each line**.

Example:

```txt
line 0: word ids 0, 1, 2, 3, 4
line 1: word ids 0, 1, 2, 3, 4
line 2: word ids 0, 1, 2, 3, 4, 5, 6
```

Because word IDs reset for each line, timed words in the `alignment` section use `line_word_id` to refer back to these IDs.

---

# `alignment`

## Example

```json
"alignment": {
  "level": "word",
  "quality_score": 0.91,
  "quality_score_method": "syncverse_heuristic_v1",
  "lines": []
}
```

## Type

`object`

## Required

Yes

## Description

Stores the timed alignment result produced by the MVP 1 pipeline.

This section contains the final timing data that lyric video rendering, future editing tools, or export tools would consume.

## Fields

| Field | Type | Required | Description |
|---|---|---:|---|
| `level` | string | yes | Granularity of the alignment |
| `quality_score` | number or null | no | Overall alignment quality score |
| `quality_score_method` | string or null | no | Method used to calculate quality score |
| `lines` | array | yes | Timed line-level alignment objects |

## MVP 1 Rule

For MVP 1, alignment level should be:

```json
"level": "word"
```

This means the file includes word-level timings, with line-level timings derived from word timings.

---

# `alignment.quality_score`

## Example

```json
"quality_score": 0.91
```

## Type

`number` or `null`

## Required

No

## Description

Represents an overall estimated alignment quality score.

## Range

If present, the value should be between:

```txt
0.0 and 1.0
```

Where:

- `1.0` means very high quality
- `0.0` means very poor quality

## MVP 1 Note

This is not necessarily a confidence score from MFA.

For MVP 1, this may be calculated by SyncVerse using a heuristic, such as:

```json
"quality_score_method": "syncverse_heuristic_v1"
```

If no quality score is calculated, use:

```json
"quality_score": null
```

---

# `alignment.lines`

## Example

```json
{
  "line_id": 0,
  "text": "Never gonna give you up",
  "start": 12.34,
  "end": 14.82,
  "duration": 2.48,
  "quality_score": 0.94,
  "words": []
}
```

## Type

`array<object>`

## Required

Yes

## Description

Each object in `alignment.lines` represents a timed lyric line.

A timed line should correspond to a lyric line in `lyrics.lines`.

## Fields

| Field | Type | Required | Description |
|---|---|---:|---|
| `line_id` | number | yes | ID of the matching lyric line from `lyrics.lines` |
| `text` | string | yes | Original lyric line text |
| `start` | number or null | yes | Start time in seconds |
| `end` | number or null | yes | End time in seconds |
| `duration` | number or null | yes | Duration in seconds |
| `quality_score` | number or null | no | Estimated quality score for the line |
| `words` | array | yes | Timed word objects for the line |

## Line Timing Rules

`start` should be the start time of the first aligned word in the line.

`end` should be the end time of the last aligned word in the line.

`duration` should equal:

```txt
end - start
```

If a line cannot be aligned, use:

```json
"start": null,
"end": null,
"duration": null
```

Do not invent fake timings.

---

# `alignment.lines.words`

## Example

```json
{
  "line_word_id": 0,
  "text": "Never",
  "start": 12.34,
  "end": 12.78,
  "duration": 0.44,
  "quality_score": 0.95,
  "source": "mfa"
}
```

## Type

`array<object>`

## Required

Yes

## Description

Each object in `alignment.lines[].words` represents one timed word in a lyric line.

This is the core timing output of MVP 1.

## Fields

| Field | Type | Required | Description |
|---|---|---:|---|
| `line_word_id` | number | yes | Word ID within the matching lyric line |
| `text` | string | yes | Word text |
| `start` | number or null | yes | Word start time in seconds |
| `end` | number or null | yes | Word end time in seconds |
| `duration` | number or null | yes | Word duration in seconds |
| `quality_score` | number or null | no | Estimated quality score for this word |
| `source` | string | yes | Source of the timing data |

## Word Timing Rules

`start` and `end` should be represented as seconds.

Example:

```json
"start": 12.34,
"end": 12.78
```

`duration` should equal:

```txt
end - start
```

If a word cannot be aligned, use:

```json
"start": null,
"end": null,
"duration": null
```

Do not invent fake timings.

## Source Values

For MVP 1, the expected source value is:

```json
"source": "mfa"
```

Future versions may support values such as:

```txt
manual
demucs_assisted
imported
edited
```

---

# `warnings`

## Example

```json
"warnings": [
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
]
```

## Type

`array<object>`

## Required

Yes

## Description

Stores non-fatal warnings produced during the pipeline.

Warnings should not necessarily mean the pipeline failed. They are used to highlight suspicious or imperfect output that may be useful for debugging or future manual review.

If there are no warnings, use an empty array:

```json
"warnings": []
```

## Warning Fields

| Field | Type | Required | Description |
|---|---|---:|---|
| `type` | string | yes | Machine-readable warning type |
| `severity` | string | yes | Warning severity |
| `line_id` | number or null | no | Related lyric line ID, if applicable |
| `word_id` | number or null | no | Related word ID, if applicable |
| `message` | string | yes | Human-readable warning message |
| `details` | object | no | Additional structured warning details |

## Severity Values

Recommended severity values:

```txt
info
warning
error
```

### `info`

Useful note. The output may still be good.

### `warning`

Potential issue that may affect quality.

### `error`

A serious problem occurred, but the JSON file may still have been generated for debugging.

---

# `exports`

## Example

```json
"exports": {
  "lrc": "output/example_song.lrc"
}
```

## Type

`object`

## Required

No

## Description

Stores paths to optional files exported from the SyncVerse timing data.

For MVP 1, the primary output is the JSON file itself. Other exports are optional.

## Fields

| Field | Type | Required | Description |
|---|---|---:|---|
| `lrc` | string | no | Path to an exported `.lrc` lyrics file |

## MVP 1 Notes

If no additional exports are generated, this can be:

```json
"exports": {}
```

or omitted, depending on implementation preference.

If this field is included in the schema, prefer using an empty object over omitting it.

---

# Timing Format Rules

All timing values in MVP 1 should be represented as numbers in seconds.

Use this:

```json
"start": 12.34
```

Do not use this:

```json
"start": "00:12.34"
```

## Timing Fields

The main timing fields are:

- `alignment.lines[].start`
- `alignment.lines[].end`
- `alignment.lines[].duration`
- `alignment.lines[].words[].start`
- `alignment.lines[].words[].end`
- `alignment.lines[].words[].duration`
- `processing.audio.duration_seconds`

## Precision

Timing values should generally use decimal seconds.

Examples:

```json
12.34
12.345
12.3456
```

The exact decimal precision can be decided by implementation, but it should be consistent within a generated file.

---

# Null Timing Rules

If a timing value is unknown or could not be produced, it should be represented as `null`.

Example:

```json
{
  "start": null,
  "end": null,
  "duration": null
}
```

Do not use placeholder values like:

```json
{
  "start": -1,
  "end": -1,
  "duration": -1
}
```

The pipeline should not invent timings for unaligned lyrics.

---

# Text Preservation Rules

MVP 1 should preserve both original and normalized lyric text.

## Original Text

Original text should preserve what the user provided as much as possible.

Example:

```json
"text": "Never gonna give you up"
```

## Normalized Text

Normalized text should reflect the version used for alignment.

Example:

```json
"normalized_text": "never gonna give you up"
```

This makes it easier to debug cases where the alignment text differs from the original lyrics.

---

# Relationship Between `lyrics` and `alignment`

The `lyrics` section stores the untimed lyric structure.

The `alignment` section stores the timed version of that structure.

These sections should correspond to each other.

## Line Relationship

Each item in:

```txt
alignment.lines
```

should reference a matching item in:

```txt
lyrics.lines
```

using:

```json
"line_id": 0
```

This should match:

```json
"lyrics": {
  "lines": [
    {
      "id": 0
    }
  ]
}
```

## Word Relationship

Each item in:

```txt
alignment.lines[].words
```

should reference a matching word in:

```txt
lyrics.lines[].words
```

using:

```json
"line_word_id": 0
```

This should match:

```json
"lyrics": {
  "lines": [
    {
      "words": [
        {
          "id": 0
        }
      ]
    }
  ]
}
```

## Important Rule

Word IDs reset within each line.

That means the pair:

```txt
line_id + line_word_id
```

uniquely identifies a word within the song.

---

# Quality Score Rules

Quality scores are optional but useful.

## Format

Quality scores should be numbers between:

```txt
0.0 and 1.0
```

or `null` if unavailable.

## Score Locations

Quality scores may appear at:

- `alignment.quality_score`
- `alignment.lines[].quality_score`
- `alignment.lines[].words[].quality_score`

## MVP 1 Note

MFA may not directly provide confidence scores for each aligned word.

If SyncVerse includes quality scores in MVP 1, they should be treated as SyncVerse heuristic scores, not official MFA confidence values.

The scoring method should be documented in:

```json
"quality_score_method": "syncverse_heuristic_v1"
```

---

# Required MVP 1 Output Guarantees

Every valid MVP 1 SyncVerse JSON file should guarantee:

1. The file has a `schema_version`.
2. The file has a `created_at` timestamp.
3. The file includes original source file references.
4. The file identifies the alignment backend.
5. The file stores audio processing metadata.
6. The file stores lyrics normalization metadata.
7. The file preserves original lyric text at the line and word level.
8. The file preserves normalized lyric text at the line and word level.
9. The file includes line-level timing data.
10. The file includes word-level timing data.
11. Line IDs in `alignment.lines` match line IDs in `lyrics.lines`.
12. Word IDs in `alignment.lines[].words` match word IDs in `lyrics.lines[].words`.
13. All timing values are represented in seconds.
14. Missing or unavailable timing values are represented with `null`.
15. Warnings are represented as structured objects.
16. Optional exports are listed in `exports`.

---

# MVP 1 Validation Checklist

The implementation should validate the final JSON before treating the pipeline as successful.

## Top-Level Validation

- `schema_version` exists and is a string.
- `created_at` exists and is a string.
- `source` exists and is an object.
- `processing` exists and is an object.
- `lyrics` exists and is an object.
- `alignment` exists and is an object.
- `warnings` exists and is an array.

## Source Validation

- `source.audio_file` exists.
- `source.lyrics_file` exists.

## Processing Validation

- `processing.alignment_backend.name` exists.
- `processing.alignment_backend.acoustic_model` exists or is explicitly `null`.
- `processing.alignment_backend.dictionary` exists or is explicitly `null`.
- `processing.audio.input_file` exists.
- `processing.audio.used_for_alignment` exists.
- `processing.lyrics.normalization` exists.

## Lyrics Validation

- `lyrics.line_count` exists.
- `lyrics.lines` is an array.
- `lyrics.line_count` matches the length of `lyrics.lines`.
- Every lyric line has an `id`.
- Every lyric line has `text`.
- Every lyric line has `normalized_text`.
- Every lyric line has a `words` array.
- Every lyric word has an `id`.
- Every lyric word has `text`.
- Every lyric word has `normalized_text`.

## Alignment Validation

- `alignment.level` exists.
- `alignment.lines` is an array.
- Every aligned line has a valid `line_id`.
- Every aligned line has `text`.
- Every aligned line has `start`, `end`, and `duration`.
- Every aligned line has a `words` array.
- Every aligned word has `line_word_id`.
- Every aligned word has `text`.
- Every aligned word has `start`, `end`, and `duration`.
- Every aligned word has a `source`.

## Timing Validation

- Timing values are numbers or `null`.
- Timing values are not negative.
- If `start` and `end` are numbers, `end` should be greater than or equal to `start`.
- If `start`, `end`, and `duration` are numbers, `duration` should approximately equal `end - start`.

## Relationship Validation

- Every `alignment.lines[].line_id` exists in `lyrics.lines[].id`.
- Every `alignment.lines[].words[].line_word_id` exists in the matching lyric line's `words[].id`.
- The text in aligned lines should match the text in the corresponding lyric lines.
- The text in aligned words should match the text in the corresponding lyric words.

---

# Minimal Valid MVP 1 Example

This is a small structural example. The full example output should live in `example-json-mvp1.json`.

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
          }
        ]
      }
    ]
  },
  "alignment": {
    "level": "word",
    "quality_score": 0.91,
    "quality_score_method": "syncverse_heuristic_v1",
    "lines": [
      {
        "line_id": 0,
        "text": "Never gonna give you up",
        "start": 12.34,
        "end": 13.18,
        "duration": 0.84,
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
          }
        ]
      }
    ]
  },
  "warnings": [],
  "exports": {}
}
```

---

# Future Expansion Fields

The MVP 1 schema should avoid overbuilding, but it should not block future SyncVerse features.

Future versions may add fields for:

- Multiple audio sources
- Vocal-only stems
- Instrumental stems
- Demucs processing information
- Manual timing corrections
- Editor state
- Lyric video rendering settings
- Multiple export formats
- Per-line styling
- Per-word animation metadata
- Pipeline step history
- Advanced confidence scoring
- User review status

Future fields should be added in a way that preserves backward compatibility when possible.

---

# Implementation Notes for AI Agents

AI coding agents should follow these rules when working with the JSON output:

1. Do not change the JSON structure without updating this document.
2. Do not update `example-json-mvp1.json` without checking this schema document.
3. Preserve both original and normalized lyric text.
4. Use seconds for all timing values.
5. Use `null` for unknown timing values.
6. Do not invent fake timings.
7. Keep `lyrics` and `alignment` references consistent.
8. Treat `line_id + line_word_id` as the unique reference for an aligned word.
9. Validate the final JSON before treating the pipeline as successful.
10. Keep MVP 1 focused on timing data, not video rendering metadata.

---

# Summary

The SyncVerse MVP 1 JSON schema is designed to represent the output of a local forced-alignment pipeline.

The JSON file should preserve source file references, document how processing was performed, preserve original and normalized lyrics, store line-level and word-level timing data, include quality and warning information, and optionally reference additional exports.

The example file `example-json-mvp1.json` should be treated as a concrete example of this schema, while this document should be treated as the human-readable definition of the schema.
