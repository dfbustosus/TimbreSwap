"""Tests for the Timbre Matcher feature."""
import os
import numpy as np
import soundfile as sf
import pytest
from pathlib import Path

from timbrematcher.pipeline import run_timbre_matching_pipeline


@pytest.fixture
def audio_files(tmp_path: Path):
    sr = 22050
    # Create a target sine wave
    target_freq = 440
    target_duration = 1
    target_t = np.linspace(0., target_duration, int(sr * target_duration), endpoint=False)
    target_y = np.sin(2 * np.pi * target_freq * target_t)
    target_file = tmp_path / "target.wav"
    sf.write(target_file, target_y, sr)

    # Create a source with the target sine wave embedded
    source_duration = 5
    source_t = np.linspace(0., source_duration, int(sr * source_duration), endpoint=False)
    source_y = np.random.randn(len(source_t)) * 0.1  # Noise
    start_sample = int(2 * sr)  # Embed at 2 seconds
    end_sample = start_sample + len(target_y)
    source_y[start_sample:end_sample] += target_y
    source_file = tmp_path / "source.wav"
    sf.write(source_file, source_y, sr)

    return str(target_file), str(source_file)


def test_timbre_matching_pipeline(audio_files, tmp_path: Path):
    target_file, source_file = audio_files
    output_dir = tmp_path / "output"

    run_timbre_matching_pipeline(target_file, source_file, str(output_dir), top_n=1)

    assert output_dir.exists(), "Output directory should be created."

    # Check for the matched file
    output_files = list(output_dir.glob("*.wav"))
    assert len(output_files) > 0, "At least one matched file should be created."
