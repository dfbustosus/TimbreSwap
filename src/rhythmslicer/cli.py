# src/rhythmslicer/cli.py

import typer
import logging
from pathlib import Path

from .config import config
from .pipeline import run_slicing_pipeline

# Create a Typer application
app = typer.Typer(
    name="rhythmslicer",
    help="A tool to analyze and slice audio files based on rhythm.",
    add_completion=False
)

def setup_logging(level: str = "INFO"):
    """Configures basic logging for the application."""
    logging.basicConfig(
        level=level.upper(),
        format="%(asctime)s - [%(levelname)s] - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

@app.callback()
def main_callback(
    ctx: typer.Context,
    config_file: Path = typer.Option(
        "config/defaults.yml",
        "--config",
        "-c",
        help="Path to the configuration YAML file.",
        exists=True,
        readable=True,
        resolve_path=True,
    ),
):
    """
    Main callback to setup configuration before any command runs.
    """
    setup_logging()
    try:
        config.load_config(str(config_file))
    except (FileNotFoundError, ValueError) as e:
        logging.error(f"Configuration Error: {e}")
        raise typer.Exit(code=1)

@app.command()
def process(
    input_file: Path = typer.Argument(
        ..., # '...' makes it a required argument
        help="The path to the source audio file to process.",
        exists=True,
        readable=True,
        resolve_path=True,
    ),
    output_dir: Path = typer.Argument(
        ...,
        help="The directory where output files will be saved.",
        writable=True,
        resolve_path=True,
    ),
):
    """
    Analyzes, processes, and slices an audio file.
    """
    try:
        run_slicing_pipeline(str(input_file), str(output_dir))
        typer.secho("\nProcessing complete! ✅", fg=typer.colors.GREEN)
    except Exception as e:
        logging.error(f"An unexpected error occurred during processing: {e}", exc_info=True)
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()