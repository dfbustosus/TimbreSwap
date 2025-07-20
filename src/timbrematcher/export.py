"""Functions for exporting matched audio segments."""
import os
import soundfile as sf
import numpy as np
import librosa

def save_matched_segments(
    source_path: str,
    output_dir: str,
    matches: list[tuple[float, float]],
    y: np.ndarray,
    sr: int,
):
    """
    Saves the matched audio segments to disk.

    Args:
        source_path: Path to the source audio file.
        output_dir: Directory to save the output files.
        matches: A list of (start_time, end_time) tuples for the matches.
        y: The audio time series of the source file.
        sr: The sampling rate of the source file.
    """
    os.makedirs(output_dir, exist_ok=True)
    base_name = os.path.splitext(os.path.basename(source_path))[0]

    for i, (start_time, end_time) in enumerate(matches):
        start_sample = librosa.time_to_samples(start_time, sr=sr)
        end_sample = librosa.time_to_samples(end_time, sr=sr)
        segment = y[start_sample:end_sample]

        output_filename = f"{base_name}_match_{i+1:03d}.wav"
        output_path = os.path.join(output_dir, output_filename)
        sf.write(output_path, segment, sr)
        print(f"Saved matched segment to {output_path}")
