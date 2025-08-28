import shutil
import subprocess
import sys
import json
import click
from pathlib import Path
from rich.console import Console
from rich.table import Table
from datetime import datetime

# --- Constants and Configuration ---
# Project root is the parent directory of this script's location
PROJECT_ROOT = Path(__file__).parent.parent.resolve()
HARNESS_DIR = PROJECT_ROOT / ".eval_harness"
CACHE_DIR = HARNESS_DIR / "results_cache"
HEAD_WORKSPACE = HARNESS_DIR / "head"
LOCAL_WORKSPACE = HARNESS_DIR / "local"

# Rich console for pretty printing
console = Console()


def run_command(command, cwd=None, capture_output=False, text=True):
    """A helper to run a shell command and handle errors."""
    try:
        # If the command is a string, use shell=True for commands like 'git archive | tar'
        use_shell = isinstance(command, str)
        process = subprocess.run(
            command,
            cwd=cwd,
            check=True,
            capture_output=capture_output,
            text=text,
            shell=use_shell,
        )
        return process
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]Error running command:[/bold red] {command}")
        console.print(f"[red]Return Code:[/red] {e.returncode}")
        console.print(f"[red]Output:[/red]\n{e.stdout or e.stderr}")
        sys.exit(1)
    except FileNotFoundError:
        # This error is more common on Windows if git isn't in the PATH
        cmd_name = command[0] if isinstance(command, list) else command.split()[0]
        console.print(f"[bold red]Error: Command not found.[/bold red] Is '{cmd_name}' in your system's PATH?")
        sys.exit(1)


def get_head_commit_hash():
    """Gets the short hash of the current HEAD commit."""
    return run_command(["git", "rev-parse", "--short", "HEAD"], capture_output=True).stdout.strip()


def setup_workspace(workspace_path: Path, version_name: str, head_commit_hash: str = None):
    """Prepares a clean workspace for an evaluation run."""
    console.print(f"\n[bold cyan]Setting up '{version_name}' workspace...[/bold cyan]")

    # Clean up previous workspace if it exists
    if workspace_path.exists():
        shutil.rmtree(workspace_path)
    workspace_path.mkdir(parents=True)

    code_dir = workspace_path / "code"
    venv_dir = workspace_path / "venv"
    # Handle OS-specific executable paths
    pip_executable = venv_dir / "Scripts" / "pip.exe" if sys.platform == "win32" else venv_dir / "bin" / "pip"

    # 1. Get the source code
    if version_name == "head":
        console.print(f"  -> Exporting code from HEAD ({head_commit_hash})...")
        code_dir.mkdir()
        # Using git archive is a clean way to export the repo content
        git_archive_command = f"git archive {head_commit_hash} | tar -x -C {code_dir}"
        run_command(git_archive_command, cwd=PROJECT_ROOT)
    else: # "local"
        console.print("  -> Copying current project state...")
        # Ignore git, the harness, and other noise
        shutil.copytree(
            PROJECT_ROOT,
            code_dir,
            ignore=shutil.ignore_patterns(".git", ".eval_harness", "__pycache__", "*.pyc", ".idea"),
        )

    # 2. Create virtual environment
    console.print(f"  -> Creating virtual environment at [italic]{venv_dir}[/italic]...")
    run_command([sys.executable, "-m", "venv", str(venv_dir)])

    # 3. Install dependencies
    console.print("  -> Installing project dependencies...")
    run_command([str(pip_executable), "install", "-e", "."], cwd=code_dir)

    return code_dir, venv_dir


def run_evaluation(workspace_path: Path, venv_dir: Path, input_file: Path, python_version: str):
    """Runs the cflow.py evaluation script within a given workspace."""
    version_name = workspace_path.name
    console.print(f"\n[bold green]Running evaluation for '{version_name}' on Python {python_version}...[/bold green]")

    code_dir = workspace_path / "code"
    output_dir = workspace_path / "output" / python_version # Use a sub-dir for version-specific output
    output_dir.mkdir(parents=True, exist_ok=True)
    results_file = output_dir / python_version / f"{input_file.stem}_0" / "results.json"
    
    # Clean previous results for this version if they exist
    if results_file.exists():
        results_file.unlink()

    cflow_script = code_dir / "dev_scripts" / "cflow.py"
    python_executable = venv_dir / "Scripts" / "python.exe" if sys.platform == "win32" else venv_dir / "bin" / "python"

    command = [
        str(python_executable),
        str(cflow_script),
        input_file,
        "--version",
        python_version,
        "--prefix",
        str(output_dir),
    ]

    run_command(command)

    if not results_file.exists():
        console.print(f"[bold red]Error:[/bold red] Evaluation for '{version_name}' finished but 'results.json' was not created.")
        sys.exit(1)

    with open(results_file) as f:
        return json.load(f)


def compare_and_report(head_results, local_results, report_path: Path):
    """Compares two sets of results and prints a detailed report to console and a file."""
    # Setup a new console to capture the report text to a file
    with report_path.open("w", encoding="utf-8") as f:
        report_console = Console(file=f, width=120, record=True)

        title = "[bold magenta]Evaluation Comparison Report[/bold magenta]"
        console.print("\n\n" + title)
        report_console.print(title)

        # 1. Summary Table
        table = Table(title="Comparison Summary")
        table.add_column("Category", justify="right", style="cyan", no_wrap=True)
        table.add_column("HEAD", justify="center", style="green")
        table.add_column("Local", justify="center", style="yellow")
        table.add_column("Change", justify="center")

        categories = sorted(list(set(list(head_results.keys()) + list(local_results.keys()))))
        for cat in categories:
            head_count = len(head_results.get(cat, []))
            local_count = len(local_results.get(cat, []))
            change = local_count - head_count
            change_str = f"[red]+{change}[/red]" if change > 0 else f"[green]{change}[/green]" if change < 0 else "0"
            table.add_row(cat.replace("_", " ").title(), str(head_count), str(local_count), change_str)

        console.print(table)
        report_console.print(table)

        # 2. Detailed Deltas
        head_map = {path: cat for cat, paths in head_results.items() for path in paths}
        local_map = {path: cat for cat, paths in local_results.items() for path in paths}
        all_paths = set(head_map.keys()) | set(local_map.keys())

        regressions = sorted([(path, local_map.get(path)) for path in all_paths if head_map.get(path) == "success" and local_map.get(path) != "success"])
        improvements = sorted([(path, head_map.get(path)) for path in all_paths if local_map.get(path) == "success" and head_map.get(path) != "success"])
        side_moves = sorted([(path, head_map.get(path), local_map.get(path)) for path in all_paths if head_map.get(path) != local_map.get(path) and "success" not in [head_map.get(path), local_map.get(path)]])

        def print_section(title, items, format_func):
            if items:
                console.print(f"\n{title}")
                report_console.print(f"\n{title}")
                for item in items:
                    line = format_func(*item)
                    console.print(line)
                    report_console.print(line)

        print_section("[bold red]Regressions (Success -> Other)[/bold red]", regressions, lambda p, new: f"- {p}  ([green]success[/green] -> [yellow]{new}[/yellow])")
        print_section("[bold green]Improvements (Other -> Success)[/bold green]", improvements, lambda p, old: f"- {p}  ([yellow]{old}[/yellow] -> [green]success[/green])")
        print_section("[bold yellow]Side Moves (Error -> Error)[/bold yellow]", side_moves, lambda p, old, new: f"- {p}  ([cyan]{old}[/cyan] -> [cyan]{new}[/cyan])")
    
    console.print(f"\n-> Comparison report saved to [italic]{report_path}[/italic]")

@click.command()
@click.option('--input-file', required=True, type=click.Path(exists=True, dir_okay=False, resolve_path=True, path_type=Path), help='Path to the input file listing test cases.')
@click.option('--python-version', 'python_versions', required=True, multiple=True, type=str, help='Python version to evaluate. Can be specified multiple times.')
@click.option('--no-cache', is_flag=True, default=False, help='Force re-evaluation of the HEAD commit for all specified Python versions.')
def main(input_file, python_versions, no_cache):
    """
    An evaluation framework to compare the performance of the current project
    state against the most recent git commit (HEAD).
    """
    HARNESS_DIR.mkdir(exist_ok=True)
    CACHE_DIR.mkdir(exist_ok=True)
    run_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    head_commit = get_head_commit_hash()
    input_filename = Path(input_file).name

    # Determine if we need to setup the HEAD workspace
    head_is_setup = False
    head_venv_dir = None
    if no_cache or not all((CACHE_DIR / f"{head_commit}_{input_filename}_{py_ver}.json").exists() for py_ver in python_versions):
        _, head_venv_dir = setup_workspace(HEAD_WORKSPACE, "head", head_commit)
        head_is_setup = True

    # Always setup the local workspace
    _, local_venv_dir = setup_workspace(LOCAL_WORKSPACE, "local")

    for python_version in python_versions:
        console.print(f"\n[bold rule dark_orange]Processing Python Version: {python_version}[/bold rule dark_orange]")

        # --- HEAD Evaluation ---
        cache_filename = f"{head_commit}_{input_filename}_{python_version}.json"
        cached_result_file = CACHE_DIR / cache_filename

        if not no_cache and cached_result_file.exists():
            console.print(f"[bold green]Using cached result for HEAD ({head_commit}) on Python {python_version}...[/bold green]")
            with open(cached_result_file) as f:
                head_results = json.load(f)
        else:
            if not head_is_setup: # Should not happen if logic is correct, but as a safeguard
                 _, head_venv_dir = setup_workspace(HEAD_WORKSPACE, "head", head_commit)
                 head_is_setup = True
            assert head_venv_dir is not None
            head_results = run_evaluation(HEAD_WORKSPACE, head_venv_dir, input_file, python_version)
            with open(cached_result_file, "w") as f:
                json.dump(head_results, f, indent=2)
            console.print(f"-> Caching result to [italic]{cached_result_file}[/italic]")

        # --- Local Evaluation ---
        local_results = run_evaluation(LOCAL_WORKSPACE, local_venv_dir, input_file, python_version)
        
        # --- Save Local Results Artifact ---
        local_artifact_path = CACHE_DIR / f"local_results_{run_timestamp}_{python_version}.json"
        with open(local_artifact_path, "w") as f:
            json.dump(local_results, f, indent=2)
        console.print(f"-> Local results saved to [italic]{local_artifact_path}[/italic]")

        # --- Comparison ---
        report_artifact_path = CACHE_DIR / f"comparison_report_{run_timestamp}_{python_version}.txt"
        compare_and_report(head_results, local_results, report_artifact_path)

    # --- Final Cleanup ---
    console.print("\n[bold]Cleaning up workspaces...[/bold]")
    if head_is_setup:
        shutil.rmtree(HEAD_WORKSPACE)
    shutil.rmtree(LOCAL_WORKSPACE)
    console.print("Done.")

if __name__ == "__main__":
    main()