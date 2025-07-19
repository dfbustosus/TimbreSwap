# src/rhythmslicer/processing.py

import librosa
import numpy as np
import logging
from typing import List

logger = logging.getLogger(__name__)

def slice_audio_on_beats(
    waveform: np.ndarray,
    beat_frames: np.ndarray
) -> List[np.ndarray]:
    """
    Slices an audio waveform into chunks based on detected beat frames.
    """
    logger.info(f"Slicing waveform into {len(beat_frames)} beat-synced chunks.")

    beat_samples = librosa.frames_to_samples(beat_frames)
    slice_points = np.concatenate([[0], beat_samples, [len(waveform)]])

    slices = []
    for i in range(len(slice_points) - 1):
        start = slice_points[i]
        end = slice_points[i+1]
        slices.append(waveform[start:end])

    logger.info("Slicing process complete.")
    return slices # <--- ADD THIS LINE