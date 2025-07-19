# src/rhythmslicer/analysis.py

import librosa
import numpy as np
import logging
from typing import Tuple, Any

from .config import config

logger = logging.getLogger(__name__)

def analyze_audio(file_path: str) -> Tuple[np.ndarray, np.ndarray, float, np.ndarray, int]:
    """
    Loads and analyzes an audio file for its rhythmic and harmonic components.

    This function performs the following steps:
    1. Loads the audio file.
    2. Separates the audio into harmonic and percussive components using HPSS.
    3. Tracks the beats and estimates the tempo from the percussive component.

    Args:
        file_path: The full path to the input audio file.

    Returns:
        A tuple containing:
        - y_percussive (np.ndarray): The percussive component of the audio.
        - y_harmonic (np.ndarray): The harmonic component of the audio.
        - tempo (float): The estimated tempo in beats per minute (BPM).
        - beat_frames (np.ndarray): An array of frame indices corresponding to beat events.
        - sr (int): The sample rate of the audio.
    
    Raises:
        FileNotFoundError: If the input file does not exist.
    """
    logger.info(f"Starting analysis for: {file_path}")
    
    # 1. Load audio file
    y, sr = librosa.load(file_path, sr=None)

    # 2. Get HPSS parameters from config and perform separation
    hpss_params = config.get('hpss', {})
    y_harmonic, y_percussive = librosa.effects.hpss(y, **hpss_params)
    logger.info("Separated audio into harmonic and percussive components.")


    # 3. Get beat tracking parameters from config and analyze rhythm
    beat_tracker_params = config.get('beat_tracker', {})
    tempo, beat_frames = librosa.beat.beat_track(
        y=y_percussive, 
        sr=sr,
        **beat_tracker_params
    )
    logger.info(f"Analysis complete. Detected Tempo: {np.mean(tempo):.2f} BPM.")

    return y_percussive, y_harmonic, tempo, beat_frames, sr