# Local File Storage Conventions

SyncVerse is local-first. User audio, lyrics, generated alignment files, MFA output, and downloaded models should stay on the developer's machine unless a future issue explicitly marks a small fixture as safe to commit.

## Tracked Project Files

Commit source code, documentation, configuration examples, tests, and small text fixtures.

Examples:

```txt
src/
docs/
tests/
samples/README.md
samples/input/.gitkeep
samples/expected-output/.gitkeep
.env.example
pyproject.toml
```

## Ignored Local Files

The repository ignores generated and machine-local files, including:

```txt
.env
.venv/
__pycache__/
output/*
projects/*
models/*
*.wav
*.mp3
*.flac
*.m4a
*.ogg
*.lab
*.TextGrid
*.log
```

Placeholder files such as `.gitkeep` may be committed so required directories exist in a fresh clone.

## Directory Conventions

Use `samples/input/` for local sample audio and lyrics while developing.

Use `projects/` for per-song workspaces that contain copied inputs, working files, MFA corpus files, alignment output, final output, and logs.

Use `output/` for generated JSON and `.lrc` files that are not tied to a full project workspace.

Use `models/` only for local model storage notes or manually managed model files. Do not commit downloaded MFA models.

## Example Project Workspace

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
      example_song.lrc
    logs/
      pipeline.log
```

Generated project workspace contents should remain untracked by default.
