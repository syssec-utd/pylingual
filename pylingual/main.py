from typing import TYPE_CHECKING
import click
import logging
import platform
import subprocess
import os
import shutil
from pathlib import Path

from pylingual.equivalence_check import TestResult
import pylingual.utils.ascii_art as ascii_art
from pylingual.utils.generate_bytecode import CompileError
from pylingual.utils.version import PythonVersion, supported_versions
from pylingual.utils.tracked_list import TrackedList, SEGMENTATION_STEP, TRANSLATION_STEP, CFLOW_STEP, CORRECTION_STEP
from pylingual.utils.lazy import lazy_import
from pylingual.decompiler import decompile

import rich
from rich.align import Align
from rich.console import Group
from rich.live import Live
from rich.logging import RichHandler
from rich.progress import Progress, TextColumn, BarColumn, TaskProgressColumn, TimeElapsedColumn
from rich.rule import Rule
from rich.status import Status
from rich.theme import Theme
from rich.table import Table

if TYPE_CHECKING:
    import transformers
else:
    lazy_import("transformers")

logger = logging.getLogger(__name__)


def print_header():
    console = rich.get_console()
    console.rule()
    console.print(Align(ascii_art.PYLINGUAL_ART, "center"), style="royal_blue1", highlight=False)
    console.print(ascii_art.PYLINGUAL_SUBHEADER, justify="center")
    console.rule()


def print_result(title: str, results: list[TestResult]):
    table = Table(title=title)
    table.add_column("Code Object")
    table.add_column("Success")
    table.add_column("Message")
    for r in results:
        if isinstance(r, CompileError):
            continue
        table.add_row(r.names(), "Success" if r.success else "Failure", r.message, style="red" if not r.success else "")
    if table.rows:
        rich.get_console().print(table, justify="center")


def collect_files(paths: list[Path], out_dir: Path, flatten: bool) -> list[tuple[Path, Path]]:
    file_map: list[tuple[Path, Path]] = []
    seen_outputs: set[Path] = set()

    def add_file(source: Path, dest: Path):
        # Resolve collisions by incrementing a counter
        counter = 1
        original_stem = dest.stem
        while dest in seen_outputs:
            dest = dest.with_stem(f"{original_stem}_{counter}")
            counter += 1

        file_map.append((source, dest))
        seen_outputs.add(dest)

    for path in paths:
        if path.is_file():
            # individual files are saved directly to the output directory
            add_file(path, out_dir / f"decompiled_{path.with_suffix('.py').name}")
        elif path.is_dir():
            # directories are recursively searched for .pyc files
            for pyc_path in path.rglob("*.pyc"):
                target_dir = out_dir
                if not flatten:
                    # mirror the directory structure
                    target_dir /= pyc_path.relative_to(path).parent
                add_file(pyc_path, target_dir / f"decompiled_{pyc_path.with_suffix('.py').name}")

    return file_map


@click.command(help="End to end pipeline to decompile Python bytecode into source code.", context_settings={"help_option_names": ["-h", "--help"]})
@click.argument("files", type=click.Path(exists=True, path_type=Path), nargs=-1, metavar="PATHS")
@click.option("-o", "--out-dir", default=None, type=click.Path(file_okay=False, path_type=Path), help="The directory to export results to.", metavar="PATH")
@click.option("-c", "--config-file", default=None, type=click.Path(exists=True, dir_okay=False, path_type=Path), help="Config file for model information.", metavar="PATH")
@click.option("-v", "--version", default=None, type=PythonVersion, help="Python version of the .pyc, default is auto detection.", metavar="VERSION")
@click.option("-k", "--top-k", default=10, type=int, help="Maximum number of additional segmentations to consider.", metavar="INT")
@click.option("-r", "--redis-host", default=None, envvar="PYLINGUAL_REDIS_HOST", type=str, help="Redis translation cache host. Unset disables caching (default: $PYLINGUAL_REDIS_HOST).", metavar="HOST")
@click.option("--redis-port", default=6379, envvar="PYLINGUAL_REDIS_PORT", type=click.IntRange(min=1, max=65535), help="Redis translation cache port (default: $PYLINGUAL_REDIS_PORT or 6379).", metavar="PORT")
@click.option("-q", "--quiet", is_flag=True, default=False, help="Suppress console output.")
@click.option("--flatten", is_flag=True, default=False, help="Flatten the output directory. (Only used if files list contains directories)")
@click.option("--force", is_flag=True, default=False, help="Overwrite existing output files.")
@click.option("--trust-lnotab", is_flag=True, default=False, help="Use the lnotab for segmentation instead of the segmentation model.")
@click.option("--init-pyenv", is_flag=True, default=False, help="Install pyenv before decompiling.")
@click.option("--timeout", default=None, type=int, help="Maximum time in seconds to allow decompilation to run per file.", metavar="SECONDS")
def main(files: list[Path], out_dir: Path | None, config_file: Path | None, version: PythonVersion | None, top_k: int, flatten: bool, force: bool, trust_lnotab: bool, init_pyenv: bool, quiet: bool, timeout: int | None, redis_host: str | None, redis_port: int):
    rich.reconfigure(markup=False, emoji=False, quiet=quiet, theme=Theme({"logging.keyword": "yellow not bold"}))
    console = rich.get_console()
    log_handler = RichHandler(console=console, rich_tracebacks=True)
    logging.basicConfig(level="INFO", format="%(message)s", datefmt="[%X]", handlers=[log_handler], force=True)

    if not init_pyenv and not files:
        click.echo(click.get_current_context().get_help())
        return

    print_header()

    if init_pyenv and (not install_pyenv() or not files):
        return

    if out_dir:
        Path(out_dir).mkdir(parents=True, exist_ok=True)

    progress = Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        TimeElapsedColumn(),
    )
    status = Status("Initializing...")

    # extend TrackedList to update progress bars
    def init(self):
        self.task = next(x for x in progress.tasks if x.description == self.name)
        self.task.total = len(self.x) + 1
        progress.start_task(self.task.id)

    TrackedList.init = init
    TrackedList.progress = lambda self, i: progress.advance(self.task.id, i)
    # the step is not done until the TrackedList is deleted
    TrackedList.__del__ = lambda self: progress.advance(self.task.id, 9e999)

    tasks_to_process = collect_files(files, out_dir or Path("."), flatten)
    n = len(tasks_to_process)

    if n == 0:
        logger.warning("No pyc files found to process.")
        return

    with Live(Group(Rule(), status, progress), transient=True, console=console, refresh_per_second=12.5) as live:
        transformers.logging.disable_default_handler()
        transformers.logging.add_handler(log_handler)
        progress.add_task(SEGMENTATION_STEP, start=False)
        progress.add_task(TRANSLATION_STEP, start=False)
        progress.add_task(CFLOW_STEP, start=False)
        progress.add_task(CORRECTION_STEP, start=False)

        for i, (pyc_path, save_path) in enumerate(tasks_to_process):
            for task in progress.tasks:
                progress.reset(task.id, start=False)

            # Ensure output directory exists (especially for mirrored structure)
            save_path.parent.mkdir(parents=True, exist_ok=True)

            log_handler.keywords = [str(pyc_path), pyc_path.name, pyc_path.with_suffix(".py").name, save_path.name]
            status.update(f"Decompiling {pyc_path} ({i + 1} / {n})")
            if not pyc_path.exists():
                logger.error(f"pyc file {pyc_path} does not exist")
                continue
            if save_path.exists() and not force:
                logger.warning(f"Output file {save_path} already exists. Skipping.")
                continue

            try:
                result = decompile(
                    pyc=pyc_path,
                    save_to=save_path,
                    config_file=Path(config_file) if config_file else None,
                    version=version,
                    top_k=top_k,
                    trust_lnotab=trust_lnotab,
                    timeout=timeout,
                    redis_cache_server_ip=redis_host or None,
                    redis_port=redis_port,
                )
                pyc = result.original_pyc
                print_result(f"Equivalence Results for {pyc.pyc_path.name if pyc.pyc_path else repr(pyc)}", result.equivalence_results)
            except TimeoutError as e:
                logger.error(str(e))
                continue
            except Exception:
                logger.exception(f"Failed to decompile {pyc_path}")
            console.rule()


def install_pyenv():
    if shutil.which("pyenv") is not None:
        logger.warning("pyenv seems to already be installed, ignoring --init-pyenv...")
        return True
    cmd = "curl -fsSL https://pyenv.run | bash"
    if platform.system() == "Windows":
        cmd = r'''powershell.exe -Command "Invoke-WebRequest -UseBasicParsing -Uri 'https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1' -OutFile './install-pyenv-win.ps1'; &'./install-pyenv-win.ps1'"'''
    elif platform.system() not in ["Linux", "Darwin"] and not click.confirm("pyenv is probably not supported on your operating system. Continue?", default=False):
        return False
    if not click.confirm(f"pyenv will be installed with the following command:\n\n\t{cmd}\n\nContinue?", default=True):
        return False
    if subprocess.run(cmd, shell=True).returncode != 0:
        logger.error("pyenv install failed, exiting...")
        return False
    os.environ["PATH"] = f"{os.environ.get('PYENV_ROOT', os.path.expanduser('~/.pyenv'))}/bin:{os.environ['PATH']}"
    which_pyenv = shutil.which("pyenv")
    if which_pyenv is None:
        logger.error("Could not find pyenv, exiting...")
        return False
    versions = click.prompt(
        "Enter comma-separated Python versions to install (leave empty to install all supported versions)",
        value_proc=lambda s: [PythonVersion(x) for x in s.split(",")] if isinstance(s, str) else s,
        default=supported_versions,
        show_default=False,
    )
    if subprocess.run([which_pyenv, "install", *map(str, versions)]).returncode != 0:
        logger.error("Error installing Python versions, exiting...")
        return False
    return True


if __name__ == "__main__":
    main()
