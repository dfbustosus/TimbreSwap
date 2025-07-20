# TimbreSwap

TimbreSwap is a Python-based command-line tool for advanced audio analysis and manipulation. It provides two main features:

1.  **Rhythm Slicer**: Analyzes an audio file, separates its harmonic and percussive components, and slices the percussive part into individual rhythmic events.
2.  **Timbre Matcher**: Finds segments in a source audio file that have a similar timbre to a given target audio snippet.

## Features

### Rhythm Slicer

-   Separates harmonic and percussive elements from an audio file.
-   Detects onset events (peaks) in the percussive signal.
-   Slices the percussive audio into individual files based on the detected onsets.
-   Exports the harmonic component and the percussive slices as WAV files.

### Timbre Matcher

-   Analyzes the timbral fingerprint of a target audio snippet using MFCCs.
-   Searches a source audio file for segments with the most similar timbre.
-   Saves the best matching segments to a specified output directory.

## Installation

1.  Clone the repository:

    ```bash
    git clone https://github.com/your-username/TimbreSwap.git
    cd TimbreSwap
    ```

2.  Create and activate a virtual environment:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  Install the required dependencies:

    ```bash
    pip install -e .[dev]
    ```

## Usage

### Rhythm Slicer

To use the Rhythm Slicer, run the `rhythmslicer` command with the path to your audio file:

```bash
rhythmslicer process /path/to/your/audio.wav --output output_directory
```

**Parameters:**
- `process`: The command to process an audio file.
- `/path/to/your/audio.wav`: Path to the input audio file.
- `--output` or `-o`: Directory where the processed files will be saved.

**Example:**
```bash
# Process a saxophone recording and save the results to a specific directory
rhythmslicer process assets/saxophone-playing-242340.wav --output output/sax_slices
```

**Using the Python API:**
You can also use the Rhythm Slicer directly from Python:

```python
from rhythmslicer.pipeline import run_slicing_pipeline

run_slicing_pipeline(
    input_file="assets/saxophone-playing-242340.wav",
    output_dir="output/rhythm_slices"
)
```

### Timbre Matcher

To use the Timbre Matcher, you need a target audio snippet and a source audio file. The target snippet should be shorter than the source file. Run the `timbrematcher` command with the paths to both files:

```bash
timbrematcher /path/to/your/target.wav /path/to/your/source.wav --out output_directory --top-n 5
```

**Parameters:**
-   `--out` or `-o`: Specifies the directory to save the matched segments (defaults to `output/timbre_matches`).
-   `--top-n` or `-n`: The number of best matches to find (defaults to 5).

**Example:**
```bash
# Find 3 segments in a saxophone recording that match the timbre of a guitar loop
timbrematcher assets/acoustic-guitar-loop-f-91bpm-132687.mp3 assets/saxophone-playing-242340.wav --out output/guitar_in_sax --top-n 3
```

**Using the Python API:**
You can also use the Timbre Matcher directly from Python:

```python
from timbrematcher.pipeline import run_timbre_matching_pipeline

run_timbre_matching_pipeline(
    target_file="assets/acoustic-guitar-loop-f-91bpm-132687.mp3",
    source_file="assets/saxophone-playing-242340.wav",
    output_dir="output/timbre_matches_run",
    top_n=3,
)
```
