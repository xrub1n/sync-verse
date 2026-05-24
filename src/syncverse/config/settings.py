"""Central configuration values for the local-first SyncVerse pipeline.

Future modules should add new settings here instead of hardcoding environment
variable names or local paths in pipeline, CLI, MFA, or export code.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from os import PathLike, environ
from pathlib import Path
from typing import Mapping


DEFAULT_MFA_BINARY_PATH = "mfa"
DEFAULT_MFA_ACOUSTIC_MODEL = "english_us_arpa"
DEFAULT_MFA_DICTIONARY_MODEL = "english_us_arpa"
DEFAULT_PROJECTS_DIR = Path("./projects")
DEFAULT_OUTPUT_DIR = Path("./output")
DEFAULT_INTERMEDIATE_DIR = Path("./output/intermediate")
DEFAULT_MODELS_DIR = Path("./models")
DEFAULT_DEBUG = False


@dataclass(frozen=True)
class SyncVerseSettings:
    """Resolved MVP 1 configuration.

    CLI-provided values should be applied through ``with_overrides`` or the
    ``overrides`` argument to ``load_settings`` so command arguments take
    precedence over environment defaults.
    """

    mfa_binary_path: str = DEFAULT_MFA_BINARY_PATH
    mfa_acoustic_model: str = DEFAULT_MFA_ACOUSTIC_MODEL
    mfa_dictionary_model: str = DEFAULT_MFA_DICTIONARY_MODEL
    projects_dir: Path = DEFAULT_PROJECTS_DIR
    output_dir: Path = DEFAULT_OUTPUT_DIR
    intermediate_dir: Path = DEFAULT_INTERMEDIATE_DIR
    models_dir: Path = DEFAULT_MODELS_DIR
    debug: bool = DEFAULT_DEBUG

    def with_overrides(
        self,
        *,
        mfa_binary_path: str | None = None,
        mfa_acoustic_model: str | None = None,
        mfa_dictionary_model: str | None = None,
        projects_dir: str | PathLike[str] | None = None,
        output_dir: str | PathLike[str] | None = None,
        intermediate_dir: str | PathLike[str] | None = None,
        models_dir: str | PathLike[str] | None = None,
        debug: bool | None = None,
    ) -> "SyncVerseSettings":
        """Return a copy with explicit CLI-style overrides applied."""

        updates: dict[str, object] = {}
        if mfa_binary_path is not None:
            updates["mfa_binary_path"] = mfa_binary_path
        if mfa_acoustic_model is not None:
            updates["mfa_acoustic_model"] = mfa_acoustic_model
        if mfa_dictionary_model is not None:
            updates["mfa_dictionary_model"] = mfa_dictionary_model
        if projects_dir is not None:
            updates["projects_dir"] = Path(projects_dir)
        if output_dir is not None:
            updates["output_dir"] = Path(output_dir)
        if intermediate_dir is not None:
            updates["intermediate_dir"] = Path(intermediate_dir)
        if models_dir is not None:
            updates["models_dir"] = Path(models_dir)
        if debug is not None:
            updates["debug"] = debug
        return replace(self, **updates)


def load_settings(
    env: Mapping[str, str] | None = None,
    *,
    overrides: Mapping[str, object] | None = None,
) -> SyncVerseSettings:
    """Load settings from defaults, environment values, then explicit overrides."""

    source = environ if env is None else env
    settings = SyncVerseSettings(
        mfa_binary_path=source.get("MFA_BINARY_PATH", DEFAULT_MFA_BINARY_PATH),
        mfa_acoustic_model=source.get("MFA_ACOUSTIC_MODEL", DEFAULT_MFA_ACOUSTIC_MODEL),
        mfa_dictionary_model=source.get(
            "MFA_DICTIONARY_MODEL", DEFAULT_MFA_DICTIONARY_MODEL
        ),
        projects_dir=_path_from_env(source, "SYNCVERSE_PROJECTS_DIR", DEFAULT_PROJECTS_DIR),
        output_dir=_path_from_env(source, "SYNCVERSE_OUTPUT_DIR", DEFAULT_OUTPUT_DIR),
        intermediate_dir=_path_from_env(
            source, "SYNCVERSE_INTERMEDIATE_DIR", DEFAULT_INTERMEDIATE_DIR
        ),
        models_dir=_path_from_env(source, "SYNCVERSE_MODELS_DIR", DEFAULT_MODELS_DIR),
        debug=_bool_from_env(source.get("SYNCVERSE_DEBUG"), DEFAULT_DEBUG),
    )

    if not overrides:
        return settings

    return settings.with_overrides(
        mfa_binary_path=_optional_str(overrides.get("mfa_binary_path")),
        mfa_acoustic_model=_optional_str(overrides.get("mfa_acoustic_model")),
        mfa_dictionary_model=_optional_str(overrides.get("mfa_dictionary_model")),
        projects_dir=_optional_pathlike(overrides.get("projects_dir")),
        output_dir=_optional_pathlike(overrides.get("output_dir")),
        intermediate_dir=_optional_pathlike(overrides.get("intermediate_dir")),
        models_dir=_optional_pathlike(overrides.get("models_dir")),
        debug=_optional_bool(overrides.get("debug")),
    )


def _path_from_env(
    env: Mapping[str, str], key: str, default: Path
) -> Path:
    value = env.get(key)
    return Path(value) if value else default


def _bool_from_env(value: str | None, default: bool) -> bool:
    if value is None or value == "":
        return default
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    raise ValueError(f"Invalid boolean value for SYNCVERSE_DEBUG: {value!r}")


def _optional_str(value: object) -> str | None:
    if value is None:
        return None
    return str(value)


def _optional_pathlike(value: object) -> str | PathLike[str] | None:
    if value is None:
        return None
    if isinstance(value, str):
        return value
    if isinstance(value, PathLike):
        return value
    raise TypeError(f"Expected a path-like override, got {type(value).__name__}")


def _optional_bool(value: object) -> bool | None:
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    raise TypeError(f"Expected a boolean debug override, got {type(value).__name__}")
