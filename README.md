# SyncVerse

SyncVerse is a local-first lyric synchronization tool that aligns plain-text lyrics with an audio file and exports synced lyric formats such as `.lrc`.

## MVP 1 Goals

- Command-line interface
- Audio file input
- Plain-text lyric file input
- Line-level lyric alignment
- Internal JSON output
- `.lrc` export
- Basic error handling
- Basic documentation

## Development Setup

For local development instructions, see [docs/development-setup.md](docs/development-setup.md).

The short version is:

```bash
python -m venv .venv
python -m pip install -e ".[dev]"
python -m pytest
```

MVP 1 also depends on Montreal Forced Aligner for the planned alignment pipeline. See [docs/mfa-setup.md](docs/mfa-setup.md) for MFA installation and model setup.

## Local Files

Generated outputs, project workspaces, audio files, MFA model files, and environment files are intentionally ignored by Git. See [docs/local-file-storage.md](docs/local-file-storage.md) for the repository storage conventions.

## Project Docs

- [Project statement](docs/project-statement.md)
- [Requirements](docs/requirements.md)
- [Architecture](docs/architecture.md)
- [Pipeline](docs/pipeline.md)
