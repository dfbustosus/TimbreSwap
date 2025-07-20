from timbrematcher.pipeline import run_timbre_matching_pipeline

run_timbre_matching_pipeline(
    target_file="assets/acoustic-guitar-loop-f-91bpm-132687.mp3",
    source_file="assets/saxophone-playing-242340.wav",
    output_dir="output/timbre_matches_run",
    top_n=3,
)
