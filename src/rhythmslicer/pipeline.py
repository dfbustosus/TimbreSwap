# src/rhythmslicer/pipeline.py

import os
import logging
import numpy as np

from .analysis import analyze_audio
from .processing import slice_audio_on_beats
from .export import save_processed_files

logger = logging.getLogger(__name__)

def run_slicing_pipeline(input_file: str, output_dir: str):
    """
    Executes the full audio analysis, processing, and exporting pipeline.

    Args:
        input_file: The path to the source audio file.
        output_dir: The path to the directory where results will be saved.
    """
    logger.info("--- RhythmSlicer Pipeline Started ---")

    # 1. Analyze the audio. This now returns a single 'AudioAnalysisResult' object.
    analysis_result = analyze_audio(input_file)

    # 2. Process the percussive component by accessing the object's attributes.
    percussive_slices = slice_audio_on_beats(
        waveform=analysis_result.y_percussive, 
        beat_frames=analysis_result.beat_frames
    )

    # 3. Export all the resulting audio files using attributes from the result object.
    base_filename = os.path.splitext(os.path.basename(input_file))[0]
    save_processed_files(
        output_dir=output_dir,
        base_filename=base_filename,
        harmonic_track=analysis_result.y_harmonic,
        percussive_slices=percussive_slices,
        sample_rate=analysis_result.sr
    )

    logger.info(f"--- RhythmSlicer Pipeline Finished for {input_file} ---")
    print(f"\nAverage Tempo: {np.mean(analysis_result.tempo):.2f} BPM")
    print(f"Output files saved in: {output_dir}")