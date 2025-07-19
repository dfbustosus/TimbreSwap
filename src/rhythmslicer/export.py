# src/rhythmslicer/export.py

import os
import soundfile as sf
import numpy as np
import logging
from typing import List

logger = logging.getLogger(__name__)

def save_processed_files(
    output_dir: str,
    base_filename: str,
    harmonic_track: np.ndarray,
    percussive_slices: List[np.ndarray],
    sample_rate: int
):
    """
    Saves the harmonic track and all percussive slices to the output directory.

    Args:
        output_dir: The directory where all files will be saved.
        base_filename: The original name of the file, used for naming outputs.
        harmonic_track: The waveform of the harmonic component.
        percussive_slices: A list of waveforms for each percussive slice.
        sample_rate: The sample rate to use for saving the WAV files.
    """
    logger.info(f"Exporting files to directory: {output_dir}")
    os.makedirs(output_dir, exist_ok=True)

    # Save the full-length harmonic track
    harmonic_path = os.path.join(output_dir, f"{base_filename}_harmonic.wav")
    sf.write(harmonic_path, harmonic_track, sample_rate)
    logger.info(f"Successfully saved harmonic track: {harmonic_path}")

    # Create a subdirectory for the slices
    slices_dir = os.path.join(output_dir, "percussive_slices")
    os.makedirs(slices_dir, exist_ok=True)

    # Save each percussive slice as a separate file
    for i, audio_slice in enumerate(percussive_slices):
        slice_path = os.path.join(slices_dir, f"{base_filename}_slice_{i+1:03d}.wav")
        sf.write(slice_path, audio_slice, sample_rate)

    logger.info(f"Successfully saved {len(percussive_slices)} slices to '{slices_dir}'.")