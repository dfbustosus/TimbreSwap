"""The main pipeline for the timbre matching feature."""
import librosa

from .processing import find_best_match
from .export import save_matched_segments

def run_timbre_matching_pipeline(
    target_file: str,
    source_file: str,
    output_dir: str,
    top_n: int,
):
    """
    The main pipeline for the timbre matching process.

    Args:
        target_file: Path to the target audio snippet.
        source_file: Path to the source audio file to search within.
        output_dir: Directory to save matched segments.
        top_n: Number of best matches to find.
    """
    print(f"Loading target file: {target_file}")
    target_y, target_sr = librosa.load(target_file, sr=None)

    print(f"Loading source file: {source_file}")
    source_y, source_sr = librosa.load(source_file, sr=None)

    print("Finding best matches...")
    matches = find_best_match(
        target_y, target_sr, source_y, source_sr, top_n=top_n
    )

    if not matches:
        print("No suitable matches found.")
        return

    print(f"Found {len(matches)} match(es). Saving segments...")
    save_matched_segments(source_file, output_dir, matches, source_y, source_sr)
