"""Core analysis functions for timbre matching."""
import librosa
import numpy as np

def calculate_mfcc(y: np.ndarray, sr: int, n_mfcc: int = 13) -> np.ndarray:
    """
    Calculates the Mel-Frequency Cepstral Coefficients (MFCCs) for an audio signal.

    Args:
        y: The audio time series.
        sr: The sampling rate of the audio.
        n_mfcc: The number of MFCCs to return.

    Returns:
        The MFCCs, with shape (n_mfcc, time).
    """
    return librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)

def timbral_fingerprint(mfccs: np.ndarray) -> np.ndarray:
    """
    Creates a timbral fingerprint from MFCCs by taking the mean and standard deviation
    across time.

    Args:
        mfccs: The MFCCs, with shape (n_mfcc, time).

    Returns:
        A 1D array representing the timbral fingerprint.
    """
    return np.hstack([np.mean(mfccs, axis=1), np.std(mfccs, axis=1)])
