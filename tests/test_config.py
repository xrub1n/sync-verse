from pathlib import Path

import pytest

from syncverse.config.paths import build_workspace_paths, resolve_settings_paths
from syncverse.config.settings import SyncVerseSettings, load_settings


def test_load_settings_uses_mvp_defaults():
    settings = load_settings(env={})

    assert settings == SyncVerseSettings()
    assert settings.mfa_binary_path == "mfa"
    assert settings.mfa_acoustic_model == "english_us_arpa"
    assert settings.mfa_dictionary_model == "english_us_arpa"
    assert settings.projects_dir == Path("./projects")
    assert settings.output_dir == Path("./output")
    assert settings.intermediate_dir == Path("./output/intermediate")
    assert settings.models_dir == Path("./models")
    assert settings.debug is False


def test_load_settings_reads_environment_values():
    settings = load_settings(
        env={
            "MFA_BINARY_PATH": "/usr/local/bin/mfa",
            "MFA_ACOUSTIC_MODEL": "custom_acoustic",
            "MFA_DICTIONARY_MODEL": "custom_dictionary",
            "SYNCVERSE_PROJECTS_DIR": "local-projects",
            "SYNCVERSE_OUTPUT_DIR": "local-output",
            "SYNCVERSE_INTERMEDIATE_DIR": "local-output/work",
            "SYNCVERSE_MODELS_DIR": "local-models",
            "SYNCVERSE_DEBUG": "true",
        }
    )

    assert settings.mfa_binary_path == "/usr/local/bin/mfa"
    assert settings.mfa_acoustic_model == "custom_acoustic"
    assert settings.mfa_dictionary_model == "custom_dictionary"
    assert settings.projects_dir == Path("local-projects")
    assert settings.output_dir == Path("local-output")
    assert settings.intermediate_dir == Path("local-output/work")
    assert settings.models_dir == Path("local-models")
    assert settings.debug is True


def test_cli_overrides_take_precedence_over_environment_values():
    settings = load_settings(
        env={"SYNCVERSE_OUTPUT_DIR": "env-output", "SYNCVERSE_DEBUG": "false"},
        overrides={"output_dir": "cli-output", "debug": True},
    )

    assert settings.output_dir == Path("cli-output")
    assert settings.debug is True


def test_load_settings_rejects_invalid_debug_value():
    with pytest.raises(ValueError, match="Invalid boolean"):
        load_settings(env={"SYNCVERSE_DEBUG": "sometimes"})


def test_resolve_settings_paths_uses_base_directory(tmp_path):
    settings = SyncVerseSettings(projects_dir=Path("projects"), output_dir=Path("out"))

    resolved = resolve_settings_paths(settings, base_dir=tmp_path)

    assert resolved.projects_dir == tmp_path / "projects"
    assert resolved.output_dir == tmp_path / "out"
    assert resolved.intermediate_dir == tmp_path / "output" / "intermediate"
    assert resolved.models_dir == tmp_path / "models"


def test_build_workspace_paths_matches_pipeline_layout():
    paths = build_workspace_paths(Path("projects/song"))

    assert paths.input_dir == Path("projects/song/input")
    assert paths.working_dir == Path("projects/song/working")
    assert paths.mfa_input_dir == Path("projects/song/working/mfa_input")
    assert paths.alignment_dir == Path("projects/song/alignment")
    assert paths.output_dir == Path("projects/song/output")
    assert paths.logs_dir == Path("projects/song/logs")
