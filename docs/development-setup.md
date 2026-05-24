# Development Setup

This guide explains how to get SyncVerse ready for local development.

SyncVerse MVP 1 is a local-first Python project. It expects local audio and lyric files, uses Montreal Forced Aligner (MFA) for alignment, and keeps generated outputs on your machine.

## Prerequisites

- Git
- Python 3.11 or newer
- Conda or Mamba for the MFA environment
- Montreal Forced Aligner and the required English MFA models

## 1. Clone the Repository

```bash
git clone https://github.com/xrub1n/sync-verse.git
cd sync-verse
```

## 2. Create a Python Virtual Environment

On macOS or Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

## 3. Install Python Dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

The project currently has no runtime Python dependencies. The development extra installs test tooling.

## 4. Configure Local Environment Variables

Copy the example environment file if you want local overrides:

```bash
cp .env.example .env
```

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Do not commit `.env`.

## 5. Install and Activate MFA

Follow the full MFA instructions in `docs/mfa-setup.md`.

Recommended Conda setup:

```bash
conda create -n aligner -c conda-forge montreal-forced-aligner
conda activate aligner
mfa version
```

Download the MVP 1 English models:

```bash
mfa model download acoustic english_us_arpa
mfa model download dictionary english_us_arpa
```

## 6. Add Local Sample Files

Place local sample files under:

```txt
samples/input/
```

Expected MVP 1 sample names:

```txt
samples/input/sample_song.wav
samples/input/sample_lyrics.txt
```

Large audio files are ignored by Git. Keep sample audio local unless a future issue explicitly adds a small licensed fixture.

## 7. Run the Sample Pipeline

The CLI pipeline is not implemented yet. The intended MVP 1 command shape is:

```bash
syncverse align samples/input/sample_song.wav samples/input/sample_lyrics.txt --out output/
```

Until the CLI is implemented, use `docs/pipeline.md` and `docs/mfa-setup.md` as the source of truth for the expected flow.

## 8. Run Tests

```bash
python -m pytest
```

The test suite is currently a placeholder until feature implementation issues add behavior.

## Related Documentation

- `docs/pipeline.md`
- `docs/architecture.md`
- `docs/mfa-setup.md`
- `docs/local-file-storage.md`
- `docs/troubleshooting.md`
