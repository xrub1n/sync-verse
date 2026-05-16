# **Requirements Document: SyncVerse**

## **1\. Document Purpose**

This document defines the initial functional, non-functional, data, and system requirements for the Local-First AI Lyric Alignment and Lyric Video Creation Tool.

The purpose of this document is to turn the project vision into a more concrete engineering reference. It should help guide design decisions, implementation planning, MVP scope, testing, and future development.

This document is written for the early planning phase of the project. Requirements may change as technical research, prototyping, and user testing reveal new constraints.

---

## **2\. Project Overview**

The project is an open-source, local-first software tool that allows users to provide an audio file and a lyric document, then uses AI-assisted processing to generate timestamped lyric data.

The timestamped lyric data can be reviewed, manually corrected, exported to standard formats, and eventually used to generate lyric videos using the original song audio.

The core product is not the video renderer itself. The core product is the lyric alignment engine: a reusable system that converts audio and lyrics into accurate, editable, portable synced lyric data.

---

## **3\. Product Goals**

The project should achieve the following major goals:

1. Provide a local-first workflow for syncing lyrics to music.  
2. Generate line-level lyric timestamps from an audio file and plain-text lyrics.  
3. Store aligned lyrics in a structured internal JSON format.  
4. Export aligned lyrics to standard lyric and subtitle formats.  
5. Provide a developer-friendly CLI and eventually a reusable API/library.  
6. Provide a desktop editor for reviewing and correcting lyric timing.  
7. Eventually generate lyric videos using synced lyrics and the original song audio.  
8. Remain open-source, modular, and extensible.

---

## **4\. MVP Scope**

The first MVP should focus only on proving the lyric alignment engine.

### **4.1 Included in MVP 1**

MVP 1 shall include:

* A command-line interface.  
* Audio file input.  
* Plain-text lyric file input.  
* Line-level lyric alignment.  
* Internal JSON output.  
* `.lrc` export.  
* Basic error handling.  
* Basic documentation for running the tool.

### **4.2 Excluded from MVP 1**

MVP 1 shall not include:

* Desktop GUI.  
* Video rendering.  
* Word-level lyric highlighting.  
* Custom project package files.  
* Cloud accounts or user login.  
* Direct Spotify, Apple Music, YouTube, or Musixmatch integration.  
* Full subtitle format support beyond `.lrc`.  
* Real-time collaboration.  
* Mobile app support.

---

## **5\. System Users**

### **5.1 Primary Users**

The primary users are:

* Independent musicians.  
* Video creators.  
* Developers.  
* Hobbyists creating lyric or sing-along videos.  
* Users who want to sync lyrics locally without uploading audio to a cloud service.

### **5.2 Developer Users**

Developer users may interact with the project through:

* CLI commands.  
* JSON files.  
* Exported lyric files.  
* A future library or API.

### **5.3 Desktop App Users**

Desktop app users, in later versions, may interact with the project through:

* File pickers.  
* Timeline views.  
* Audio playback controls.  
* Lyric editing panels.  
* Export menus.  
* Video rendering controls.

---

## **6\. Functional Requirements**

### **6.1 Audio Input Requirements**

**FR-AUDIO-1:** The system shall allow the user to provide an audio file as input.

**FR-AUDIO-2:** The MVP shall support at least `.mp3` and `.wav` audio files.

**FR-AUDIO-3:** The system should eventually support additional formats including `.flac`, `.m4a`, and `.ogg`.

**FR-AUDIO-4:** The system shall validate that the provided audio file exists before processing.

**FR-AUDIO-5:** The system shall return a clear error message if the audio file is missing, unsupported, corrupted, or unreadable.

**FR-AUDIO-6:** The system should extract basic audio metadata when available, including duration, filename, and format.

---

### **6.2 Lyric Input Requirements**

**FR-LYRICS-1:** The system shall allow the user to provide a lyric file as input.

**FR-LYRICS-2:** The MVP shall support plain-text `.txt` lyric files.

**FR-LYRICS-3:** The system should eventually support pasted text, `.md`, `.lrc`, `.srt`, `.vtt`, and `.ass` lyric or subtitle inputs.

**FR-LYRICS-4:** The system shall validate that the provided lyric file exists before processing.

**FR-LYRICS-5:** The system shall return a clear error message if the lyric file is missing, empty, unsupported, or unreadable.

**FR-LYRICS-6:** The system shall preserve the original lyric line order.

**FR-LYRICS-7:** The system should preserve section markers such as `[Verse]`, `[Chorus]`, `[Bridge]`, and `[Outro]` as metadata when possible.

**FR-LYRICS-8:** The system should normalize lyric text for alignment while preserving the original display text for output.

---

### **6.3 Lyric Preprocessing Requirements**

**FR-PRE-1:** The system shall split plain-text lyrics into individual lyric lines.

**FR-PRE-2:** The system shall remove unnecessary leading and trailing whitespace from each line.

**FR-PRE-3:** The system should ignore empty lines for alignment unless they are needed for section structure.

**FR-PRE-4:** The system should detect and handle repeated lyric sections when possible.

**FR-PRE-5:** The system should normalize punctuation, casing, and common contractions during matching.

**FR-PRE-6:** The system shall retain the original unmodified lyric text for display and export.

---

### **6.4 Audio Analysis Requirements**

**FR-ANALYSIS-1:** The system shall process the audio file to identify vocal or lyrical content.

**FR-ANALYSIS-2:** The system shall generate timing information that can be mapped to the provided lyrics.

**FR-ANALYSIS-3:** The MVP should prioritize line-level timing over word-level timing.

**FR-ANALYSIS-4:** The system should use an AI-assisted transcription or alignment model to estimate lyric timing.

**FR-ANALYSIS-5:** The system should store confidence information when available.

**FR-ANALYSIS-6:** The system shall handle songs with instrumental sections before, between, or after lyric sections.

---

### **6.5 Alignment Requirements**

**FR-ALIGN-1:** The system shall map lyric lines to timestamps in the audio file.

**FR-ALIGN-2:** Each aligned lyric line shall include a start timestamp.

**FR-ALIGN-3:** Each aligned lyric line should include an end timestamp.

**FR-ALIGN-4:** Each aligned lyric line should include a confidence score when possible.

**FR-ALIGN-5:** The system shall preserve lyric line order in the output.

**FR-ALIGN-6:** The system should detect lines that could not be confidently aligned.

**FR-ALIGN-7:** The system should mark low-confidence or failed alignments for manual review.

**FR-ALIGN-8:** The system should support songs where lyrics do not begin at the start of the audio file.

**FR-ALIGN-9:** The system should support repeated choruses and repeated lyric lines.

**FR-ALIGN-10:** The system should not silently drop lyric lines that could not be aligned.

---

### **6.6 JSON Output Requirements**

**FR-JSON-1:** The system shall export aligned lyrics to a structured JSON file.

**FR-JSON-2:** The JSON output shall include project metadata.

**FR-JSON-3:** The JSON output shall include audio metadata.

**FR-JSON-4:** The JSON output shall include an ordered list of lyric lines.

**FR-JSON-5:** Each lyric line object shall include an index, text, start time, end time, and confidence field.

**FR-JSON-6:** Each lyric line object should include a `words` array, even if word-level timestamps are not yet supported.

**FR-JSON-7:** The JSON output shall be valid, parseable JSON.

**FR-JSON-8:** The JSON output should include a schema version or alignment format version.

Example expected JSON structure:

```json
{
  "metadata": {
    "title": "Unknown Title",
    "artist": "Unknown Artist",
    "language": "en",
    "alignmentVersion": "0.1.0"
  },
  "audio": {
    "filename": "song.mp3",
    "duration": 213.42,
    "format": "mp3"
  },
  "lines": [
    {
      "index": 0,
      "text": "Example lyric line",
      "start": 12.31,
      "end": 15.82,
      "confidence": 0.91,
      "words": []
    }
  ]
}
```

---

### **6.7 LRC Export Requirements**

**FR-LRC-1:** The system shall export aligned lyric lines to an `.lrc` file.

**FR-LRC-2:** Each aligned lyric line in the `.lrc` output shall include a timestamp and lyric text.

**FR-LRC-3:** The `.lrc` output shall preserve the original lyric display text.

**FR-LRC-4:** The `.lrc` output should include metadata tags when available, such as title, artist, album, and creator.

**FR-LRC-5:** Lines that could not be aligned should either be omitted with a warning or included in a clearly documented way.

Example `.lrc` output:

```
[ti:Unknown Title]
[ar:Unknown Artist]
[by:Local Lyric Alignment Tool]

[00:12.31]Example lyric line
[00:15.90]Another lyric line
```

---

### **6.8 CLI Requirements**

**FR-CLI-1:** The MVP shall provide a command-line interface.

**FR-CLI-2:** The CLI shall provide an `align` command.

**FR-CLI-3:** The `align` command shall accept an audio file path and lyric file path.

**FR-CLI-4:** The CLI shall allow the user to specify an output path for the JSON result.

**FR-CLI-5:** The CLI should allow the user to export `.lrc` directly during alignment.

**FR-CLI-6:** The CLI shall display progress or status messages during processing.

**FR-CLI-7:** The CLI shall display clear error messages when processing fails.

**FR-CLI-8:** The CLI should provide a `validate` command for checking JSON alignment files.

**FR-CLI-9:** The CLI should provide an `export` command for converting JSON alignment files into other formats.

Example CLI commands:

```shell
lyric-align align song.mp3 lyrics.txt --json output/lyrics.json
```

```shell
lyric-align align song.mp3 lyrics.txt --json output/lyrics.json --lrc output/lyrics.lrc
```

```shell
lyric-align export output/lyrics.json --format lrc --output output/lyrics.lrc
```

---

### **6.9 Desktop Editor Requirements, Future Version**

**FR-EDITOR-1:** The system should eventually provide a desktop graphical interface.

**FR-EDITOR-2:** The desktop editor should allow users to import an audio file.

**FR-EDITOR-3:** The desktop editor should allow users to import or paste lyrics.

**FR-EDITOR-4:** The desktop editor should allow users to run lyric alignment from the interface.

**FR-EDITOR-5:** The desktop editor should display lyric lines with their timestamps.

**FR-EDITOR-6:** The desktop editor should provide audio playback controls.

**FR-EDITOR-7:** The desktop editor should allow users to manually adjust lyric line timing.

**FR-EDITOR-8:** The desktop editor should visually indicate low-confidence lines.

**FR-EDITOR-9:** The desktop editor should allow users to export corrected lyric data.

**FR-EDITOR-10:** The desktop editor should eventually display a waveform or timeline view.

---

### **6.10 Word-Level Alignment Requirements, Future Version**

**FR-WORD-1:** The system should eventually support word-level timestamps.

**FR-WORD-2:** Each word object should include text, start time, end time, and confidence score.

**FR-WORD-3:** Word-level timing should be stored inside the corresponding lyric line object.

**FR-WORD-4:** Word-level timing should support karaoke-style highlighting and animated lyric video effects.

**FR-WORD-5:** The system should allow word-level timestamps to be manually corrected in a future editor version.

---

### **6.11 Lyric Video Rendering Requirements, Future Version**

**FR-VIDEO-1:** The system should eventually generate lyric videos using synced lyric data.

**FR-VIDEO-2:** The video renderer shall use the original song audio by default.

**FR-VIDEO-3:** The video renderer should not require vocal removal.

**FR-VIDEO-4:** The video renderer should display lyrics in sync with the song.

**FR-VIDEO-5:** The video renderer should support at least one simple visual layout in its first version.

**FR-VIDEO-6:** The video renderer should export video as `.mp4`.

**FR-VIDEO-7:** The video renderer should eventually support custom backgrounds, fonts, colors, and text animations.

**FR-VIDEO-8:** The video renderer should eventually support karaoke-style highlighting as an optional effect.

**FR-VIDEO-9:** The video renderer should use the corrected JSON alignment file as its source of truth.

---

### **6.12 Project Package Requirements, Future Version**

**FR-PROJECT-1:** The system should eventually support saving and reopening full project files.

**FR-PROJECT-2:** A project file should store or reference the audio file, aligned lyric data, visual settings, and project metadata.

**FR-PROJECT-3:** A project package may use a zip-based structure.

**FR-PROJECT-4:** The project package extension should avoid conflicting with the existing `.kar` karaoke MIDI format.

**FR-PROJECT-5:** Possible project package extensions include `.kproj`, `.lyricproj`, or `.karaokeproj`.

Example project package structure:

```
song.kproj
├── manifest.json
├── audio.mp3
├── lyrics.json
├── lyrics.lrc
├── styles.json
└── assets/
    ├── background.png
    └── font.ttf
```

---

## **7\. Non-Functional Requirements**

### **7.1 Privacy Requirements**

**NFR-PRIVACY-1:** The system shall prioritize local processing whenever possible.

**NFR-PRIVACY-2:** The MVP shall not require users to upload audio or lyrics to a remote server.

**NFR-PRIVACY-3:** The system shall not collect user audio, lyric files, or generated outputs by default.

**NFR-PRIVACY-4:** If any future cloud features are added, they must be optional and clearly disclosed.

---

### **7.2 Performance Requirements**

**NFR-PERF-1:** The system should process typical song-length audio files, approximately 2 to 8 minutes long.

**NFR-PERF-2:** The system should provide progress feedback during long-running tasks.

**NFR-PERF-3:** The system should avoid freezing the user interface in future desktop versions.

**NFR-PERF-4:** The system should use efficient file handling to avoid unnecessary duplication of large audio files.

**NFR-PERF-5:** The system should document expected hardware requirements once the AI model choice is known.

---

### **7.3 Reliability Requirements**

**NFR-REL-1:** The system shall not crash silently when alignment fails.

**NFR-REL-2:** The system shall provide meaningful error messages.

**NFR-REL-3:** The system shall preserve user input files and never overwrite them without explicit permission.

**NFR-REL-4:** The system should write output files atomically when possible to avoid corrupted partial files.

**NFR-REL-5:** The system should log alignment warnings and low-confidence results.

---

### **7.4 Usability Requirements**

**NFR-USE-1:** CLI commands should be simple and documented.

**NFR-USE-2:** Error messages should explain what went wrong and suggest how to fix the issue when possible.

**NFR-USE-3:** Output files should use predictable names when the user does not provide custom names.

**NFR-USE-4:** Future desktop interfaces should prioritize a clear workflow: import, align, review, export, render.

---

### **7.5 Maintainability Requirements**

**NFR-MAINT-1:** The codebase shall separate the alignment engine from the CLI interface.

**NFR-MAINT-2:** The codebase should separate import, preprocessing, alignment, export, and rendering logic into distinct modules.

**NFR-MAINT-3:** The internal JSON format should be versioned.

**NFR-MAINT-4:** The project should include automated tests for core data formatting and export behavior.

**NFR-MAINT-5:** The project should include clear contribution instructions once it is ready for public open-source use.

---

### **7.6 Portability Requirements**

**NFR-PORT-1:** The project should support common desktop operating systems over time, including Windows, macOS, and Linux.

**NFR-PORT-2:** MVP development may prioritize one operating system first, depending on the developer environment.

**NFR-PORT-3:** Output files should be platform-independent and usable outside the application.

---

### **7.7 Open-Source Requirements**

**NFR-OSS-1:** The project should be structured in a way that is understandable to outside contributors.

**NFR-OSS-2:** The repository should include a clear README.

**NFR-OSS-3:** The repository should include setup instructions.

**NFR-OSS-4:** The repository should include license information before public release.

**NFR-OSS-5:** The repository should document limitations around copyrighted material and user responsibility.

---

## **8\. Data Requirements**

### **8.1 Internal Alignment Data**

The system shall use a structured internal data format for aligned lyrics.

Required line-level fields:

* `index`  
* `text`  
* `start`  
* `end`  
* `confidence`  
* `words`

Required metadata fields:

* `title`  
* `artist`  
* `language`  
* `alignmentVersion`

Required audio fields:

* `filename`  
* `duration`  
* `format`

---

### **8.2 Time Format Requirements**

**DATA-TIME-1:** Internal timestamps shall be stored as seconds using decimal numbers.

Example:

```json
"start": 12.31
```

**DATA-TIME-2:** Exporters shall convert internal timestamps into the required format for each output type.

Example `.lrc` timestamp:

```
[00:12.31]
```

---

### **8.3 Confidence Score Requirements**

**DATA-CONF-1:** Confidence scores should use a decimal range from `0.0` to `1.0`.

**DATA-CONF-2:** A confidence score of `1.0` represents highest confidence.

**DATA-CONF-3:** A confidence score of `0.0` represents no confidence or failed alignment.

**DATA-CONF-4:** If the alignment method cannot provide confidence, the system should use `null` or a documented placeholder value.

---

## **9\. Error Handling Requirements**

**ERR-1:** The system shall detect missing audio files.

**ERR-2:** The system shall detect missing lyric files.

**ERR-3:** The system shall detect empty lyric files.

**ERR-4:** The system shall detect unsupported audio formats.

**ERR-5:** The system shall detect invalid output paths when possible.

**ERR-6:** The system shall report when alignment fails.

**ERR-7:** The system shall warn the user when some lines could not be aligned confidently.

**ERR-8:** The system shall avoid overwriting existing files unless the user confirms or provides an overwrite flag.

---

## **10\. Testing Requirements**

### **10.1 Unit Testing**

The project should include unit tests for:

* Lyric file parsing.  
* Lyric preprocessing.  
* JSON output generation.  
* `.lrc` export.  
* Timestamp formatting.  
* Input validation.  
* Error handling.

### **10.2 Integration Testing**

The project should include integration tests for:

* Full CLI alignment workflow.  
* Audio plus lyrics input processing.  
* JSON plus `.lrc` output generation.  
* Exporting from existing JSON alignment files.

### **10.3 Manual Testing**

Manual testing should include songs with:

* Clear vocals.  
* Slow lyrics.  
* Instrumental intros.  
* Repeated choruses.  
* Fast lyrics.  
* Background vocals.  
* Lyrics that do not exactly match the audio.

### **10.4 Accuracy Evaluation**

The project should eventually track alignment quality using metrics such as:

* Average timestamp error per line.  
* Percentage of lines within ±0.5 seconds.  
* Percentage of lines within ±1.0 seconds.  
* Number of lines requiring manual correction.  
* Number of failed or low-confidence alignments.

---

## **11\. Suggested Repository Structure**

An initial repository may use the following structure:

```
lyric-align/
├── docs/
│   ├── project-statement.md
│   ├── requirements.md
│   └── mvp-plan.md
├── src/
│   ├── cli/
│   ├── core/
│   │   ├── audio/
│   │   ├── lyrics/
│   │   ├── alignment/
│   │   └── export/
│   └── models/
├── tests/
│   ├── unit/
│   └── integration/
├── test_songs/
├── outputs/
├── README.md
├── TODO.md
└── LICENSE
```

---

## **12\. Requirement Priority Levels**

Requirements can be prioritized using the following levels:

* **P0:** Required for MVP 1\.  
* **P1:** Important shortly after MVP 1\.  
* **P2:** Future version requirement.  
* **P3:** Nice-to-have or experimental.

### **12.1 P0 Requirements**

P0 requirements include:

* Audio file input.  
* Plain-text lyric input.  
* Basic lyric preprocessing.  
* Line-level alignment.  
* JSON output.  
* `.lrc` output.  
* CLI interface.  
* Basic error handling.  
* Local processing.

### **12.2 P1 Requirements**

P1 requirements include:

* Improved confidence scoring.  
* Better repeated chorus handling.  
* Export command.  
* Validation command.  
* More robust tests.  
* Additional audio format support.

### **12.3 P2 Requirements**

P2 requirements include:

* Desktop editor.  
* Manual timing correction.  
* Waveform display.  
* Word-level alignment.  
* `.srt`, `.vtt`, and `.ass` export.

### **12.4 P3 Requirements**

P3 requirements include:

* Lyric video rendering.  
* Custom project package format.  
* Advanced animation presets.  
* Background video support.  
* Optional plugin system.

---

## **13\. Assumptions**

The current requirements assume:

* The project will begin as a local CLI tool.  
* The first alignment goal is line-level timing, not word-level timing.  
* The first lyric input format is plain text.  
* The first export formats are JSON and `.lrc`.  
* The project will eventually become a desktop app, but the GUI is not required for MVP 1\.  
* The video renderer is a later feature built on top of the synced lyric data.  
* Users are responsible for ensuring they have the rights to process and export content using the tool.

---

## **14\. Open Questions**

The following questions should be answered during technical research and prototyping:

1. Which AI transcription or alignment model should be used first?  
2. Should the first implementation be written in Python, JavaScript/TypeScript, or another language?  
3. What accuracy is acceptable for MVP 1?  
4. How should the system handle lyrics that differ from the actual sung words?  
5. How should repeated choruses be detected and aligned?  
6. Should the desktop app be built with Electron, Tauri, a Python GUI framework, or another technology?  
7. How should large local AI models be packaged for non-technical users?  
8. Should the project prioritize CPU compatibility, GPU acceleration, or both?  
9. What should the final project name be?  
10. What open-source license should the project use?

---

## **15\. Acceptance Criteria for MVP 1**

MVP 1 can be considered complete when the following criteria are met:

1. The user can run a CLI command with an audio file and lyric file.  
2. The system validates the provided input files.  
3. The system generates line-level timestamped lyric data.  
4. The system exports a valid JSON alignment file.  
5. The system exports a valid `.lrc` file.  
6. The `.lrc` file can be opened in a compatible lyric player or inspected manually.  
7. The JSON file follows the documented internal structure.  
8. The CLI provides useful messages during success and failure cases.  
9. The codebase separates core alignment logic from CLI logic.  
10. Basic tests exist for lyric parsing, JSON export, and LRC export.

---

## **16\. Summary**

This requirements document defines the first engineering direction for the Local-First AI Lyric Alignment and Lyric Video Creation Tool.

The most important early requirement is to build a reliable lyric alignment engine that accepts an audio file and plain-text lyrics, then outputs structured timestamped lyric data. The project should begin with a CLI-based MVP and expand later into a desktop editor, word-level alignment, additional export formats, project files, and lyric video rendering.

By focusing first on reusable synced lyric data, the project remains technically meaningful, modular, and useful beyond a single lyric video generation workflow.

