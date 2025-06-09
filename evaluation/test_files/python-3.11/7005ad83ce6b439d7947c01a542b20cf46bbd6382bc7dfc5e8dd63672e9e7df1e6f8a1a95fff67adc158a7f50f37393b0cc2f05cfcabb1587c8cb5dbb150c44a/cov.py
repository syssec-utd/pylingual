from functools import cached_property
from pathlib import Path
from shlex import quote
from typing import Union
from cicd.core.syntax.json import JSON
from cicd.core.utils.sh import sh
from .config import CovConfig
from .report import CovReport

class Cov:

    def __init__(self, xcresult_path: Union[str, Path], config_path: Union[str, Path, None]=None):
        self.xcresult_path = xcresult_path
        self.config_path = config_path or '.cov.yml'

    @cached_property
    def report(self) -> CovReport:
        cmd = f'xcrun xccov view --report --json {quote(str(self.xcresult_path))}'
        raw = JSON.from_str(sh.exec(cmd))
        config = CovConfig(path=self.config_path)
        return CovReport(raw=raw, config=config)