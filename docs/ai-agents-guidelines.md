# AI Agent Guidelines

## Project Context
SyncVerse is a local-first lyric video and lyric synchronization tool. MVP 1 focuses on producing accurate word-level lyric alignment data from an audio file and lyrics file.

## Before Implementing
Agents should read:
1. docs/project-statement.md
2. docs/requirements.md
3. docs/pipeline.md
4. docs/example-json-mvp1.json

## Rules
- Do not change the MVP 1 JSON structure unless explicitly asked.
- Keep implementation local-first.
- Do not add SaaS/cloud assumptions.
- Prefer small, testable changes.
- Add or update documentation when behavior changes.
- Use sample files in `data/sample-inputs/` and `data/sample-outputs/`.
- Do not commit large audio files or MFA model files.