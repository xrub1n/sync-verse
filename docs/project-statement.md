# **Project Statement: SyncVerse**

## **1\. Purpose of This Document**

This document defines the initial vision, scope, and technical direction for a software project focused on AI-assisted lyric alignment and lyric video creation. The goal is to move from a broad idea into a clearer engineering plan that can later be expanded into formal requirements, architecture diagrams, user stories, milestones, and implementation tasks.

This project is currently in the planning stage. The purpose of this document is not to finalize every technical detail, but to establish the core problem, intended users, expected workflow, input and output formats, and the reasoning behind major design decisions such as building the tool as a local-first desktop application rather than a traditional cloud-based SaaS product.

---

## **2\. Project Vision**

The project is an open-source, local-first lyric alignment and lyric video creation tool. The application allows users to provide an audio file and a lyric document, then uses AI-assisted processing to generate a structured mapping between the lyrics and timestamps in the song.

Once this synced lyric data is created, users can review, edit, export, and reuse it in multiple formats. The synced data can also be used to generate lyric videos, sing-along videos, caption-style videos, or karaoke-style visualizations.

The project is not intended to be only a one-click karaoke generator. Instead, the main value of the project is the lyric alignment engine: a reusable system that can take raw song audio and plain-text lyrics and produce accurate, editable, portable timestamped lyric data.

---

## **3\. Problem Statement**

Many songs either do not have synced lyrics available or have lyric timing that is inaccurate, incomplete, or unavailable outside of closed platforms. Existing tools may provide lyric video generation or karaoke creation, but many are cloud-based, limited by subscriptions, focused only on finished video output, or not designed around developer-friendly reusable lyric data.

Creators, musicians, developers, and hobbyists may want a tool that can:

* Align lyrics to a song automatically.  
* Let users manually correct imperfect timing.  
* Export synced lyrics into standard formats.  
* Keep audio files private and local.  
* Support lyric video generation without requiring vocal removal.  
* Provide a reusable alignment engine for other applications.

This project aims to solve that problem by creating a local-first tool that treats synced lyric data as the core product, with lyric video rendering as an additional output built on top of that data.

---

## **4\. Target Users**

The project is intended for several overlapping groups of users:

### **Music creators and artists**

Artists can use the tool to create synced lyric files or lyric videos for their own songs, especially for unreleased or independent music where they may not want to upload files to a third-party service.

### **Video creators**

YouTubers, editors, and social media creators can use the tool to generate lyric videos, sing-along videos, captions, or music visualizers using the original song audio.

### **Developers**

Developers can use the underlying lyric alignment engine or API to integrate lyric syncing into other apps, music tools, captioning systems, or media workflows.

### **Karaoke and sing-along users**

Although the project is not limited to traditional karaoke, users can still use the synced data to create karaoke-style visuals where lyrics are highlighted in time with the song.

---

## **5\. Why Local-First Instead of SaaS**

A local-first approach is a major design decision for this project. Rather than requiring users to upload their songs and lyrics to a remote server, the core workflow should run on the user’s machine whenever possible.

### **Privacy**

Many users may be working with unreleased songs, personal recordings, demos, commissions, or copyrighted material. Keeping the workflow local reduces the need to trust an external service with sensitive audio files.

### **Offline access**

A local desktop app allows users to work without a constant internet connection. This is especially useful for creators who want to work while traveling, in studios, or in environments where internet access is limited.

### **No upload limits**

Cloud-based tools often have file size limits, usage credits, subscriptions, or processing queues. A local-first tool can avoid many of these limitations by using the user’s own hardware.

### **Open-source transparency**

Because the project is intended to be open-source, users and developers can inspect how files are processed, how lyric alignment is performed, and what data is stored. This makes the project more trustworthy and easier to contribute to.

### **Developer flexibility**

A local alignment engine can be used as a CLI tool, library, or desktop app backend. This gives the project more flexibility than a web-only SaaS product.

---

## **6\. Core Product Concept**

The core product is a lyric alignment system.

At its most basic level, the system takes:

1. An audio file.  
2. A lyric text file.

Then it produces:

1. A structured timestamped lyric data file.  
2. Optional standard lyric/subtitle exports.  
3. Optional lyric video output.

The synced lyric data should include line-level timestamps first, and later word-level timestamps. Each lyric line or word should ideally include start time, end time, text content, and a confidence score indicating how reliable the alignment is.

The desktop app acts as a visual editor for this data. The video rendering feature then uses the corrected synced lyric data to generate a final lyric video.

---

## **7\. General Workflow**

### **Step 1: Import audio**

The user selects or uploads a song file from their local machine.

Expected supported audio formats may include:

* `.mp3`  
* `.wav`  
* `.flac`  
* `.m4a`  
* `.ogg`

The application should read the file, extract basic metadata when available, and prepare it for alignment.

### **Step 2: Import lyrics**

The user provides lyrics for the song.

Expected supported lyric input formats may include:

* `.txt`  
* `.md`  
* pasted plain text  
* existing `.lrc` files  
* existing `.srt` or `.vtt` files in future versions

Initially, the project can focus on plain-text lyrics with no timestamps.

### **Step 3: Preprocess lyrics**

The application cleans and structures the lyric text before alignment.

This may include:

* Splitting lyrics into lines.  
* Removing unnecessary whitespace.  
* Preserving sections such as `[Verse]`, `[Chorus]`, or `[Bridge]` as metadata.  
* Handling repeated choruses.  
* Normalizing punctuation.  
* Preparing lyric text for comparison against audio transcription.

### **Step 4: Analyze audio**

The application processes the audio to detect spoken or sung words.

This step may involve:

* Speech-to-text transcription.  
* Forced alignment.  
* Audio segmentation.  
* Word-level timing detection.  
* Confidence scoring.

The exact AI model or alignment technique can be decided later, but the main goal is to identify where each lyric line or word occurs in the song.

### **Step 5: Generate synced lyric data**

The alignment engine maps the provided lyrics to timestamps in the audio.

The first version should prioritize line-level sync because it is more realistic for an MVP. Later versions can add word-level sync for karaoke-style highlighting and more advanced lyric video effects.

### **Step 6: Review and manually correct**

Because AI alignment will not always be perfect, the user should be able to review and adjust the synced lyrics.

Important editing features may include:

* Play/pause audio.  
* Jump to a lyric line.  
* Drag lyric timestamps on a timeline.  
* Shift a line, section, or entire song forward/backward.  
* Split or merge lyric lines.  
* Mark low-confidence areas for review.  
* Preview lyric timing in real time.

This manual correction workflow is a key part of the project because it allows the tool to produce high-quality results even when AI alignment is imperfect.

### **Step 7: Export synced lyrics**

After alignment and correction, the user can export the synced lyrics.

Expected output formats may include:

* `.json` for the project’s internal structured format.  
* `.lrc` for standard synced lyrics.  
* `.srt` for subtitle workflows.  
* `.vtt` for web captions.  
* `.ass` for advanced styled lyric or karaoke effects.

### **Step 8: Generate lyric video**

The user can optionally use the synced lyric data to generate a lyric video.

This feature is focused on lyric videos rather than traditional karaoke tracks. The default assumption is that the original song audio, including the artist’s vocals, remains in the final video. Users should be able to create videos where lyrics appear, animate, or highlight in time with the song.

Possible lyric video features include:

* Basic text-over-background lyric video.  
* Line-by-line lyric display.  
* Word-by-word highlighting.  
* Custom fonts and colors.  
* Background image or video support.  
* Audio-reactive visualizer elements.  
* Export to `.mp4`.

---

## **8\. Expected Inputs**

The application should eventually support several input types.

### **Audio inputs**

Primary audio input formats:

* `.mp3`  
* `.wav`  
* `.flac`  
* `.m4a`  
* `.ogg`

### **Lyric inputs**

Primary lyric input formats:

* `.txt`  
* pasted plain text  
* `.md`

Future lyric input formats:

* `.lrc`  
* `.srt`  
* `.vtt`  
* `.ass`

### **Visual inputs for lyric videos**

Optional visual inputs may include:

* `.png`  
* `.jpg`  
* `.webp`  
* `.mp4` background video  
* custom fonts  
* project themes or presets

---

## **9\. Expected Outputs**

The project should be designed around portable, reusable outputs.

### **Internal JSON alignment file**

The main output should be a structured JSON file containing the synced lyric data. This format should act as the source of truth for editing, exporting, and rendering.

Example structure:

```json
{
  "metadata": {
    "title": "Unknown Title",
    "artist": "Unknown Artist",
    "language": "en",
    "alignmentVersion": "1.0"
  },
  "audio": {
    "filename": "song.mp3",
    "duration": 213.42
  },
  "lines": [
    {
      "index": 0,
      "text": "Example lyric line",
      "start": 12.31,
      "end": 15.82,
      "confidence": 0.93,
      "words": [
        {
          "text": "Example",
          "start": 12.31,
          "end": 12.9,
          "confidence": 0.91
        },
        {
          "text": "lyric",
          "start": 13.0,
          "end": 13.4,
          "confidence": 0.94
        },
        {
          "text": "line",
          "start": 13.5,
          "end": 15.82,
          "confidence": 0.92
        }
      ]
    }
  ]
}
```

### **Standard lyric and subtitle exports**

The application should export to common formats so the synced lyrics can be used outside the app.

Planned export formats:

* `.lrc` for synced lyric players.  
* `.srt` for subtitle tools.  
* `.vtt` for web-based captions.  
* `.ass` for advanced subtitle styling and karaoke-like effects.

### **Lyric video export**

The video renderer should export a finished lyric video.

Expected video output:

* `.mp4`

Future possible outputs:

* `.mov`  
* `.webm`  
* image sequence exports for advanced editors

### **Project package file**

The application may eventually support a custom project file. This would not replace standard formats, but would make it easier to save and reopen full projects.

Possible names include:

* `.syncverseproj`  
* `.lyricproj`  
* `.svproj`

A project package could be a zip-based folder structure such as:

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

This would allow users to move an entire lyric video or lyric sync project as one file.

---

## **10\. Developer API and CLI Direction**

In addition to the desktop app, the project should expose the lyric alignment engine in a developer-friendly way.

The goal is for other developers to use the alignment functionality without needing the full desktop interface.

### **Possible CLI usage**

```shell
sync-verse align song.mp3 lyrics.txt --output lyrics.lrc
```

```shell
sync-verse align song.mp3 lyrics.txt --json lyrics.json --lrc lyrics.lrc
```

```shell
sync-verse render song.mp3 lyrics.json --output lyric-video.mp4
```

### **Possible library usage**

```py
from sync-verse import align

result = align(
    audio_path="song.mp3",
    lyrics_path="lyrics.txt",
    granularity="line"
)

result.export("lyrics.json")
result.export("lyrics.lrc")
```

The developer API should make the alignment engine useful for other platforms, tools, and workflows. For example, another application could use the engine to generate synced lyrics for a custom music player, captioning tool, or creator platform.

---

## **11\. Scope Prioritization**

The project should be built in stages to avoid becoming too large too early.

### **MVP 1: Lyric alignment CLI**

The first version should focus on proving the core engine works.

Core features:

* Accept one audio file.  
* Accept one plain-text lyric file.  
* Generate line-level timestamped lyrics.  
* Export JSON.  
* Export `.lrc`.

This MVP proves the core value of the project without needing a full user interface or video renderer.

### **MVP 2: Desktop editor**

The second version should provide a visual interface for reviewing and correcting lyric timing.

Core features:

* Import audio.  
* Import lyrics.  
* Run alignment.  
* Display lyrics with timestamps.  
* Play audio.  
* Adjust line timings.  
* Export corrected files.

### **MVP 3: Word-level alignment**

The third version should improve the precision of the sync data.

Core features:

* Generate word-level timestamps.  
* Add confidence scores.  
* Preview word-level highlighting.  
* Export advanced formats.

### **MVP 4: Lyric video rendering**

The fourth version should use the synced lyric data to generate videos.

Core features:

* Render lyrics over original song audio.  
* Support simple backgrounds.  
* Support basic text styling.  
* Export `.mp4`.

### **MVP 5: Project package format**

The fifth version should introduce a portable project file.

Core features:

* Save project files.  
* Reopen project files.  
* Store audio references, synced lyrics, visual styles, and assets together.

---

## **12\. Out of Scope for Early Versions**

To keep the project realistic, some features should not be prioritized in the earliest versions.

Early versions should avoid:

* Direct Spotify integration.  
* Full cloud hosting or SaaS accounts.  
* Mobile apps.  
* Real-time collaborative editing.  
* Advanced video editor features.  
* Automatic music distribution platform uploads.  
* Complex vocal removal or instrumental generation.

These features may be considered later, but they are not required to prove the main value of the project.

---

## **13\. Risks and Challenges**

### **Lyric alignment accuracy**

AI-generated alignment may be imperfect, especially with repeated choruses, background vocals, unclear vocals, live recordings, or lyrics that do not exactly match the song.

### **Word-level timing difficulty**

Line-level timestamps are more achievable for an early version. Word-level timestamps are more difficult and should be treated as a later milestone.

### **Copyright and content ownership**

Users may work with copyrighted songs. The app should avoid hosting or distributing copyrighted material. A local-first design helps reduce platform responsibility, but the project should still make it clear that users are responsible for the files they process and export.

### **Performance**

Audio transcription, alignment, and video rendering can be resource-intensive. The app should be designed with progress indicators, background processing, and reasonable performance expectations.

### **File format complexity**

Supporting many export formats can become complicated. The project should start with JSON and `.lrc`, then expand to subtitle and advanced styling formats after the core alignment is stable.

---

## **14\. Success Criteria**

The project can be considered successful if it can reliably perform the following workflow:

1. A user selects a song file.  
2. A user provides plain-text lyrics.  
3. The application generates timestamped lyric data.  
4. The user can review and correct the timing.  
5. The user can export the synced lyrics to a reusable format.  
6. The user can optionally generate a lyric video using the original song audio.

From an engineering perspective, success also means that the alignment engine is modular enough to be used by both the desktop app and a developer-facing CLI or API.

---

## **15\. Project Summary**

This project is an open-source, local-first AI lyric alignment and lyric video creation tool. It allows users to provide a song and lyric file, automatically generates timestamped lyric data, gives users tools to correct the timing, and exports the results in portable formats such as JSON, `.lrc`, `.srt`, `.vtt`, and `.ass`.

The project’s main focus is not simply generating karaoke videos. Instead, the core product is accurate, editable lyric synchronization data. Lyric video rendering is an important feature built on top of that data, allowing users to create visual lyric videos using the original song audio, with optional karaoke-style highlighting.

By prioritizing local processing, open-source development, reusable output formats, and a developer-friendly alignment engine, the project can serve creators, musicians, developers, and hobbyists while occupying a clearer niche than a generic cloud-based karaoke generator.

