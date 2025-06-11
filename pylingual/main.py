from typing import TYPE_CHECKING
import click
import logging
import shutil
import platform
import subprocess
import os
from pathlib import Path

import pylingual.utils.ascii_art as ascii_art
from pylingual.utils.generate_bytecode import CompileError
from pylingual.utils.version import PythonVersion, supported_versions
from pylingual.utils.tracked_list import TrackedList, SEGMENTATION_STEP, TRANSLATION_STEP, CFLOW_STEP, CORRECTION_STEP
from pylingual.utils.lazy import lazy_import
from pylingual.decompiler import DecompilerResult, decompile

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


def print_result(file: str, result: DecompilerResult):
    table = Table(title=f"Equivalence Results for {file}")
    table.add_column("Code Object")
    table.add_column("Success")
    table.add_column("Message")
    for r in result.equivalence_results:
        if isinstance(r, CompileError):
            continue
        table.add_row(r.names(), "Success" if r.success else "Failure", r.message, style="red" if not r.success else "")
    if table.rows:
        rich.get_console().print(table, justify="center")


@click.command(help="End to end pipeline to decompile Python bytecode into source code.", context_settings={"help_option_names": ["-h", "--help"]})
@click.argument("files", nargs=-1)
@click.option("-o", "--out-dir", default=None, type=Path, help="The directory to export results to.", metavar="PATH")
@click.option("-c", "--config-file", default=None, type=Path, help="Config file for model information.", metavar="PATH")
@click.option("-v", "--version", default=None, type=PythonVersion, help="Python version of the .pyc, default is auto detection.", metavar="VERSION")
@click.option("-k", "--top-k", default=10, type=int, help="Maximum number of additional segmentations to consider.", metavar="INT")
@click.option("-q", "--quiet", is_flag=True, default=False, help="Suppress console output.")
@click.option("--trust-lnotab", is_flag=True, default=False, help="Use the lnotab for segmentation instead of the segmentation model.")
@click.option("--init-pyenv", is_flag=True, default=False, help="Install pyenv before decompiling.")
def main(files: list[str], out_dir: Path | None, config_file: Path | None, version: PythonVersion | None, top_k: int, trust_lnotab: bool, init_pyenv: bool, quiet: bool):
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

    if out_dir is not None:
        out_dir.mkdir(parents=True, exist_ok=True)

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
    TrackedList.__del__ = lambda self: progress.advance(self.task.id, float("inf"))

    n = len(files)
    with Live(Group(Rule(), status, progress), transient=True, console=console, refresh_per_second=12.5):
        transformers.logging.disable_default_handler()
        transformers.logging.add_handler(log_handler)
        progress.add_task(SEGMENTATION_STEP, start=False)
        progress.add_task(TRANSLATION_STEP, start=False)
        progress.add_task(CFLOW_STEP, start=False)
        progress.add_task(CORRECTION_STEP, start=False)
        for i, file in enumerate(files):
            for task in progress.tasks:
                progress.reset(task.id, start=False)
            pyc_path = Path(file)
            log_handler.keywords = [file, pyc_path.name, pyc_path.with_suffix(".py").name]
            status.update(f"Decompiling {pyc_path} ({i + 1} / {n})")
            if not pyc_path.exists():
                raise FileNotFoundError(f"pyc file {pyc_path} does not exist")

            try:
                result = decompile(
                    file=pyc_path,
                    out_dir=out_dir / f"decompiled_{pyc_path.stem}" if out_dir is not None else Path(f"decompiled_{pyc_path.stem}"),
                    config_file=Path(config_file) if config_file else None,
                    version=version,
                    top_k=top_k,
                    trust_lnotab=trust_lnotab,
                )
                print_result(pyc_path.name, result)
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
