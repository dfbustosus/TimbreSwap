"""Core processing functions for finding timbre matches."""
import librosa
import numpy as np
from scipy.spatial.distance import cdist

from .analysis import calculate_mfcc, timbral_fingerprint

def find_best_match(
    target_y: np.ndarray,
    target_sr: int,
    source_y: np.ndarray,
    source_sr: int,
    n_mfcc: int = 13,
    top_n: int = 1,
) -> list[tuple[float, float]]:
    """
    Finds the best matching segment(s) in a source audio file for a given target snippet.

    Args:
        target_y: The audio time series of the target snippet.
        target_sr: The sampling rate of the target snippet.
        source_y: The audio time series of the source file.
        source_sr: The sampling rate of the source file.
        n_mfcc: The number of MFCCs to use for the analysis.
        top_n: The number of best matches to return.

    Returns:
        A list of tuples, where each tuple contains the start and end time
        of a matched segment in the source audio.
    """
    # Resample if necessary
    if target_sr != source_sr:
        target_y = librosa.resample(target_y, orig_sr=target_sr, target_sr=source_sr)

    # Calculate target fingerprint
    target_mfcc = calculate_mfcc(target_y, source_sr, n_mfcc)
    target_fp = timbral_fingerprint(target_mfcc)

    # Create overlapping frames from the source audio
    frame_length = len(target_y)
    hop_length = frame_length // 4  # 75% overlap
    source_frames = librosa.util.frame(source_y, frame_length=frame_length, hop_length=hop_length).T

    # Calculate fingerprint for each source frame
    source_fps = []
    for frame in source_frames:
        frame_mfcc = calculate_mfcc(frame, source_sr, n_mfcc)
        source_fps.append(timbral_fingerprint(frame_mfcc))

    # Find the closest matches
    distances = cdist([target_fp], source_fps, metric='euclidean')[0]
    best_indices = np.argsort(distances)[:top_n]

    # Convert frame indices to time
    matches = []
    for i in best_indices:
        start_sample = i * hop_length
        end_sample = start_sample + frame_length
        start_time = start_sample / source_sr
        end_time = end_sample / source_sr
        matches.append((start_time, end_time))

    return matches
