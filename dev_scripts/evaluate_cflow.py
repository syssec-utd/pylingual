import shutil
import subprocess
import sys
import json
import click
from pathlib import Path
from rich.console import Console
from rich.table import Table
from datetime import datetime

from dataclasses import dataclass, asdict

@dataclass
class EvaluationResult:
    success: set[Path]
    failure: set[Path]
    compile_error: set[Path]
    error: set[Path]

    @classmethod
    def from_dict(cls, data: dict[str, list[Path]]) -> 'EvaluationResult':
        return cls(
            success = set(data.get('success', [])),
            failure = set(data.get('failure', [])),
            compile_error = set(data.get('compile_error', [])),
            error = set(data.get('error', [])),
        )
    
    @classmethod
    def import_json(cls, json_path: Path) -> 'EvaluationResult':
        with json_path.open("r") as f:
            return cls.from_dict(json.load(f))
    
    def to_dict(self):
        return asdict(self)

    def export_json(self, json_path: Path):
        jsonable_dict = {
            'success': sorted(self.success),
            'failure': sorted(self.failure),
            'compile_error': sorted(self.compile_error),
            'error': sorted(self.error),
        }
        with json_path.open("w") as f:
            json.dump(jsonable_dict, f, indent=2)

    def __post_init__(self):
        assert len(set.intersection(self.success, self.failure, self.compile_error, self.error)) == 0, 'Malformed evaluation result. Paths appear in multiple categories.'


# --- Constants and Configuration ---
# Project root is the parent directory of this script's location
PROJECT_ROOT = Path(__file__).parent.parent.resolve()
HARNESS_DIR = PROJECT_ROOT / ".eval_harness"
CACHE_DIR = HARNESS_DIR / "results_cache"
LOCAL_WORKSPACE = HARNESS_DIR / "local"

SUPPORTED_PYTHON_VERSIONS = ('3.6', '3.7', '3.8', '3.9', '3.10', '3.11', '3.12', '3.13')

# Rich console for pretty printing
console = Console()

def _get_cache_path(commit_hash: str, eval_file_list_path: Path, python_version: str) -> Path:
    cache_path = CACHE_DIR / python_version / commit_hash / eval_file_list_path.with_suffix('.json').name
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    return cache_path

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


def setup_workspace(workspace_path: Path, version_name: str, commit_hash: str = ''):
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
    if version_name == "local":
        console.print("  -> Copying current project state...")
        # Ignore git, the harness, and other noise
        shutil.copytree(
            PROJECT_ROOT,
            code_dir,
            ignore=shutil.ignore_patterns(".git", ".eval_harness", "__pycache__", "*.pyc", ".idea"),
        )
    else:
        console.print(f"  -> Exporting code from {version_name} ({commit_hash})...")
        code_dir.mkdir()
        # Using git archive is a clean way to export the repo content
        git_archive_command = f"git archive {commit_hash} | tar -x -C {code_dir}"
        run_command(git_archive_command, cwd=PROJECT_ROOT)

    # 2. Create virtual environment
    console.print(f"  -> Creating virtual environment at [italic]{venv_dir}[/italic]...")
    run_command([sys.executable, "-m", "venv", str(venv_dir)])

    # 3. Install dependencies
    console.print("  -> Installing project dependencies...")
    run_command([str(pip_executable), "install", "-e", "."], cwd=code_dir, capture_output=True)

    return code_dir, venv_dir


def run_evaluation(workspace_path: Path, venv_dir: Path, input_file: Path, python_version: str) -> EvaluationResult:
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

    return EvaluationResult.import_json(results_file)

def compare_and_report(commit_results: EvaluationResult, local_results: EvaluationResult, report_path: Path, compare_to_commit: str, python_version: str):
    """Compares two sets of results and prints a detailed report to console and a file."""
    with report_path.open("w", encoding="utf-8") as f:
        report_console = Console(file=f)

        title = f"[bold magenta]Evaluation Comparison Report (Python {python_version})[/bold magenta]"
        console.print(f"\n\n{title}")
        report_console.print(title)

        categories = ["success", "failure", "compile_error", "error"]
        commit_dict = commit_results.to_dict()
        local_dict = local_results.to_dict()

        # 1. Movement Matrix
        table = Table(title="Evaluation Movement Matrix")
        table.add_column(f"From ({compare_to_commit})", justify="right", style="cyan", no_wrap=True)
        for category in categories:
            table.add_column(
                f"To (Local)\n{category.replace('_', ' ').title()}",
                justify="center",
            )

        commit_map = {path: cat for cat, paths in commit_dict.items() for path in paths}
        local_map = {path: cat for cat, paths in local_dict.items() for path in paths}
        all_paths = set(commit_map.keys()) | set(local_map.keys())
        
        movement_matrix = {cat: {cat2: 0 for cat2 in categories} for cat in categories}
        for path in all_paths:
            from_cat = commit_map.get(path)
            to_cat = local_map.get(path)
            if from_cat and to_cat:
                movement_matrix[from_cat][to_cat] += 1

        for from_cat in categories:
            row = [from_cat.replace("_", " ").title()]
            for to_cat in categories:
                count = movement_matrix[from_cat][to_cat]
                if count == 0:
                    row.append("[bright_black]-[/bright_black]")
                    continue

                if from_cat == to_cat:
                    style = "blue"
                elif from_cat == "success":
                    style = "bold red" # Regression from success
                elif to_cat == "success":
                    style = "bold green" # Improvement to success
                else:
                    style = "tan" # Side-move
                row.append(f"[{style}]{'+' if from_cat != to_cat else ''}{count}[/{style}]")
            table.add_row(*row)

        console.print(table)
        report_console.print(table)

        # 2. Detailed Deltas by Movement Category
        for from_cat in categories:
            for to_cat in categories:
                if from_cat == to_cat:
                    continue

                moved_paths = sorted([
                    p for p in all_paths
                    if commit_map.get(p) == from_cat and local_map.get(p) == to_cat
                ])

                if not moved_paths:
                    continue

                # Determine style and title
                if from_cat == "success":
                    style = "bold red"  # Regression
                elif to_cat == "success":
                    style = "bold green"  # Improvement
                else:
                    style = "bold yellow"  # Side-move

                title = f"[{style}]{from_cat.replace('_', ' ').title()} -> {to_cat.replace('_', ' ').title()}[/{style}]"
                console.print(f"\n{title}")
                report_console.print(f"\n{title}")
                for p in moved_paths:
                    console.print(f"- {p}")
                    report_console.print(f"- {p}", soft_wrap=True)
        
        # 3. New and Removed Items
        new_items = sorted([p for p in all_paths if commit_map.get(p) is None])
        removed_items = sorted([p for p in all_paths if local_map.get(p) is None])

        def print_list_section(title, items, format_func):
            if items:
                console.print(f"\n{title}")
                report_console.print(f"\n{title}")
                for item in items:
                    line = format_func(item)
                    console.print(line)
                    report_console.print(line)
        
        print_list_section(
            "\n[bold blue]New Items[/bold blue]",
            new_items,
            lambda p: f"- {p} (Added as [cyan]{local_map.get(p)}[/cyan])",
        )

        print_list_section(
            "[bold gray50]Removed Items[/bold gray50]",
            removed_items,
            lambda p: f"- {p} (Removed from [cyan]{commit_map.get(p)}[/cyan])",
        )

    console.print(f"\n-> Comparison report saved to [italic]{report_path}[/italic]")

@click.command()
@click.option('--input-file', required=True, type=click.Path(exists=True, dir_okay=False, resolve_path=True, path_type=Path), help='Path to the input file listing test cases.')
@click.option('--python-version', 'python_versions', multiple=True, type=str, help='Python version to evaluate. Can be specified multiple times. Defaults to all supported versions.', default=SUPPORTED_PYTHON_VERSIONS)
@click.option('--compare-to-commit', type=str, help='The git commit hash to compare to. Defaults to HEAD.', default='HEAD')
@click.option('--no-cache', is_flag=True, default=False, help='Force re-evaluation of the comparison commit for all specified Python versions.')
def main(input_file: Path, python_versions: list[str], compare_to_commit: str, no_cache: bool):
    """
    An evaluation framework to compare the performance of the current project
    state against a previous git commit.
    """
    HARNESS_DIR.mkdir(exist_ok=True)
    run_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    commit_version = compare_to_commit
    if compare_to_commit.lower() == 'head':
        compare_to_commit = get_head_commit_hash()
        console.print(f"[bold green]Resolved HEAD to commit {compare_to_commit}.[/bold green]")
    else:
        compare_to_commit = compare_to_commit[:7].lower() # shorten and lowercase for consistency 

    COMMIT_WORKSPACE = HARNESS_DIR / compare_to_commit

    # Always setup the local workspace
    _, local_venv_dir = setup_workspace(LOCAL_WORKSPACE, "local")
    # Only setup the commit workspace on demand
    commit_venv_dir = None

    for python_version in python_versions:
        console.print(f"\n[bold rule dark_orange]Processing Python Version: {python_version}[/bold rule dark_orange]")

        # --- Commit Evaluation ---
        cached_result_file = _get_cache_path(compare_to_commit, input_file, python_version)

        if not no_cache and cached_result_file.exists():
            console.print(f"[bold green]Using cached result for ({compare_to_commit}) on Python {python_version}...[/bold green]")
            commit_results = EvaluationResult.import_json(cached_result_file)
        else:
            if commit_venv_dir is None:
                _, commit_venv_dir = setup_workspace(COMMIT_WORKSPACE, commit_version, compare_to_commit)
            
            assert commit_venv_dir is not None
            commit_results = run_evaluation(COMMIT_WORKSPACE, commit_venv_dir, input_file, python_version)
            commit_results.export_json(cached_result_file)
            console.print(f"-> Caching result to [italic]{cached_result_file}[/italic]")

        # --- Local Evaluation ---
        local_results = run_evaluation(LOCAL_WORKSPACE, local_venv_dir, input_file, python_version)
        
        # --- Save Local Results Artifact ---
        local_artifact_path = CACHE_DIR / python_version / f"local_results_{run_timestamp}.json"
        local_results.export_json(local_artifact_path)
        console.print(f"-> Local results saved to [italic]{local_artifact_path}[/italic]")

        # --- Comparison ---
        report_artifact_path = CACHE_DIR / python_version / f"comparison_report_{run_timestamp}.txt"
        compare_and_report(commit_results, local_results, report_artifact_path, compare_to_commit, python_version)

    # --- Final Cleanup ---
    console.print("\n[bold]Cleaning up workspaces...[/bold]")
    if commit_venv_dir is not None:
        shutil.rmtree(COMMIT_WORKSPACE)
    shutil.rmtree(LOCAL_WORKSPACE)
    console.print("Done.")

if __name__ == "__main__":
    main()