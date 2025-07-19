# tests/test_pipeline.py

import numpy as np
import soundfile as sf
from pathlib import Path

from rhythmslicer.pipeline import run_slicing_pipeline

def create_dummy_audio_file(file_path: Path, sr=22050, duration=5, tempo=120):
    """
    Generates a simple test audio file with a predictable beat.
    """
    # Create a sine wave for the harmonic part
    t = np.linspace(0., duration, int(sr * duration), endpoint=False)
    y_harmonic = 0.5 * np.sin(2 * np.pi * 220 * t)

    # Create clicks for the percussive part
    y_percussive = np.zeros_like(t)
    samples_per_beat = int(sr * 60 / tempo)
    for i in range(0, len(t), samples_per_beat):
        y_percussive[i:i+100] = 1.0  # Make a short click

    # Combine them and save
    y_combined = y_harmonic + y_percussive
    sf.write(file_path, y_combined, sr)


def test_full_pipeline(tmp_path: Path):
    """
    An integration test for the full analysis and slicing pipeline.

    Args:
        tmp_path: A built-in pytest fixture that provides a temporary directory.
    """
    # 1. SETUP: Create a temporary directory structure and a dummy audio file
    input_file = tmp_path / "test_song.wav"
    output_dir = tmp_path / "output"
    create_dummy_audio_file(input_file)

    # 2. EXECUTION: Run the main application pipeline
    run_slicing_pipeline(str(input_file), str(output_dir))

    # 3. ASSERTION: Check if the expected output files were created
    assert output_dir.exists(), "Output directory should be created."

    # Check for the harmonic file
    expected_harmonic_file = output_dir / "test_song_harmonic.wav"
    assert expected_harmonic_file.exists(), "Harmonic output file should exist."

    # Check for the slices subdirectory
    slices_dir = output_dir / "percussive_slices"
    assert slices_dir.exists(), "Slices subdirectory should be created."

    # Check that at least one slice file was generated
    wav_slices = list(slices_dir.glob("*.wav"))
    assert len(wav_slices) > 0, "At least one percussive slice file should be created."