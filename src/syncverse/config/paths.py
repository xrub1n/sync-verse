"""Path resolution helpers for SyncVerse local workspaces."""

from __future__ import annotations

from dataclasses import dataclass
from os import PathLike
from pathlib import Path

from syncverse.config.settings import SyncVerseSettings


@dataclass(frozen=True)
class WorkspacePaths:
    """Common directories used by one local pipeline workspace."""

    root: Path
    input_dir: Path
    working_dir: Path
    mfa_input_dir: Path
    alignment_dir: Path
    output_dir: Path
    logs_dir: Path


def resolve_path(path: str | PathLike[str], *, base_dir: Path | None = None) -> Path:
    """Resolve a path relative to ``base_dir`` without requiring it to exist."""

    raw_path = Path(path).expanduser()
    if raw_path.is_absolute():
        return raw_path.resolve(strict=False)
    base = Path.cwd() if base_dir is None else base_dir
    return (base / raw_path).resolve(strict=False)


def resolve_settings_paths(
    settings: SyncVerseSettings, *, base_dir: Path | None = None
) -> SyncVerseSettings:
    """Return settings with local directory paths resolved against ``base_dir``."""

    return settings.with_overrides(
        projects_dir=resolve_path(settings.projects_dir, base_dir=base_dir),
        output_dir=resolve_path(settings.output_dir, base_dir=base_dir),
        intermediate_dir=resolve_path(settings.intermediate_dir, base_dir=base_dir),
        models_dir=resolve_path(settings.models_dir, base_dir=base_dir),
    )


def build_workspace_paths(project_dir: str | PathLike[str]) -> WorkspacePaths:
    """Build the standard MVP 1 workspace directory layout for a project."""

    root = Path(project_dir)
    return WorkspacePaths(
        root=root,
        input_dir=root / "input",
        working_dir=root / "working",
        mfa_input_dir=root / "working" / "mfa_input",
        alignment_dir=root / "alignment",
        output_dir=root / "output",
        logs_dir=root / "logs",
    )


def ensure_directories(paths: list[Path] | tuple[Path, ...]) -> None:
    """Create local directories needed by a caller-owned pipeline step."""

    for path in paths:
        path.mkdir(parents=True, exist_ok=True)
