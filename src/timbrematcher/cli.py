"""Command-line interface for the Timbre Matcher."""
import typer
from .pipeline import run_timbre_matching_pipeline

app = typer.Typer(
    name="timbrematcher",
    help="Finds audio segments with a similar timbre to a target snippet.",
    add_completion=False,
    no_args_is_help=True,
)

@app.callback(invoke_without_command=True)
def main(
    target_file: str = typer.Argument(..., help="Path to the target audio snippet."),
    source_file: str = typer.Argument(..., help="Path to the source audio file to search within."),
    output_dir: str = typer.Option("output/timbre_matches", "--out", "-o", help="Directory to save matched segments."),
    top_n: int = typer.Option(5, "--top-n", "-n", help="Number of best matches to find."),
):
    """
    Finds and saves the best timbral matches from a source file.
    """
    try:
        run_timbre_matching_pipeline(target_file, source_file, output_dir, top_n)
    except Exception as e:
        print(f"An error occurred: {e}")
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
