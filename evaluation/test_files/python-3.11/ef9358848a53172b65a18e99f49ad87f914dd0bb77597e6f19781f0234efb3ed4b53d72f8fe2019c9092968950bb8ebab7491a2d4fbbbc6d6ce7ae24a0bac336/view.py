import sys
import typing as t
from rich import box
from loguru import logger
from rich.panel import Panel
from rich.table import Table
from rich.pretty import Pretty
from rich.columns import Columns
from starwhale.utils import Order, console, sort_obj_list
from starwhale.consts import DEFAULT_PAGE_IDX, DEFAULT_PAGE_SIZE, SHORT_VERSION_CNT, DEFAULT_REPORT_COLS, DEFAULT_MANIFEST_NAME
from starwhale.base.uri import URI
from starwhale.base.type import URIType, InstanceType, JobOperationType
from starwhale.base.view import BaseTermView
from starwhale.core.eval.model import EvaluationJob
from starwhale.api._impl.metric import MetricKind

class JobTermView(BaseTermView):

    def __init__(self, job_uri: str) -> None:
        super().__init__()
        self.raw_uri = job_uri
        self.uri = URI(job_uri, expected_type=URIType.EVALUATION)
        logger.debug(f'eval job:{self.raw_uri}')
        self.job = EvaluationJob.get_job(self.uri)
        self._action_run_map = {JobOperationType.CANCEL: self.job.cancel, JobOperationType.RESUME: self.job.resume, JobOperationType.REMOVE: self.job.remove, JobOperationType.RECOVER: self.job.recover, JobOperationType.PAUSE: self.job.pause}

    def recover(self, force: bool=False) -> None:
        self._do_action(JobOperationType.RECOVER, force)

    def remove(self, force: bool=False) -> None:
        self._do_action(JobOperationType.REMOVE, force)

    def cancel(self, force: bool=False) -> None:
        self._do_action(JobOperationType.CANCEL, force)

    def resume(self, force: bool=False) -> None:
        self._do_action(JobOperationType.RESUME, force)

    def pause(self, force: bool=False) -> None:
        self._do_action(JobOperationType.PAUSE, force)

    @BaseTermView._simple_action_print
    def _do_action(self, action: str, force: bool=False) -> t.Tuple[bool, str]:
        return self._action_run_map[action](force)

    @BaseTermView._only_standalone
    @BaseTermView._header
    def compare(self, job_uris: t.List[str]) -> None:
        if self.uri.instance_type != InstanceType.STANDALONE:
            console.print(':dragon_face: Today job compare only works for standalone instance')
            sys.exit(1)
        jobs = []
        for _u in job_uris:
            _uri = URI(_u, expected_type=URIType.EVALUATION)
            jobs.append(EvaluationJob.get_job(_uri))
        rt = self.job.compare(jobs)
        table = Table(box=box.ASCII, title=f":leafy_green: {rt['kind'].upper()} Job Compare Summary", caption=f":cactus: base job:{rt['base']['uri']}", expand=True)
        table.add_column('', justify='left', no_wrap=True, style='cyan')
        for _v in rt['versions']:
            table.add_column(_v[:SHORT_VERSION_CNT])
        for _k, _vs in rt['summary'].items():
            _ts = [_k]
            _is_empty = all([_v['value'] is None for _v in _vs])
            if _is_empty:
                continue
            for _v in _vs:
                if _v['base']:
                    _ts.append(f":triangular_flag: {_v['value']}")
                elif _v['delta'] is None:
                    _ts.append(_v['value'])
                else:
                    if _v['delta'] > 0:
                        _text = f":chart_with_upwards_trend: [green]{_v['value']}[/]"
                    elif _v['delta'] < 0:
                        _text = f":chart_with_downwards_trend: [red]{_v['value']}[/]"
                    else:
                        _text = f":white_circle: {_v['value']}"
                    _ts.append(_text)
            table.add_row(*[str(_t) for _t in _ts])
        console.print(table)

    @BaseTermView._header
    def info(self, page: int=DEFAULT_PAGE_IDX, size: int=DEFAULT_PAGE_SIZE, max_report_cols: int=DEFAULT_REPORT_COLS) -> None:
        _rt = self.job.info(page, size)
        if not _rt:
            console.print(':tea: not found info')
            return
        if _rt.get('manifest'):
            console.rule(f'[green bold]Inspect {DEFAULT_MANIFEST_NAME} for eval:{self.uri}')
            console.print(Pretty(_rt['manifest'], expand_all=True))
        if 'location' in _rt:
            console.rule('Evaluation process dirs')
            console.print(f":cactus: ppl: {_rt['location']['ppl']}")
            console.print(f":camel: cmp: {_rt['location']['cmp']}")
        if 'tasks' in _rt:
            self._print_tasks(_rt['tasks'][0])
        if 'report' in _rt:
            _report = _rt['report']
            _kind = _rt['report'].get('kind', '')
            if 'summary' in _report:
                self._render_summary_report(_report['summary'], _kind)
            if _kind == MetricKind.MultiClassification.value:
                self._render_multi_classification_job_report(_rt['report'], max_report_cols)

    def _render_summary_report(self, summary: t.Dict[str, t.Any], kind: str) -> None:
        console.rule(f'[bold green]{kind.upper()} Summary')
        contents = [Panel(f'[b]{k}[/b]\n[yellow]{v}', expand=True) for k, v in summary.items()]
        console.print(Columns(contents))

    def _print_tasks(self, tasks: t.List[t.Dict[str, t.Any]]) -> None:
        table = Table(box=box.SIMPLE)
        table.add_column('ID', justify='left', style='cyan', no_wrap=True)
        table.add_column('UUID')
        table.add_column('Status', style='magenta')
        table.add_column('Duration')
        table.add_column('Created')
        table.add_column('Finished')
        for _t in tasks:
            status, style, icon = self.pretty_status(_t['taskStatus'])
            table.add_row(_t['id'], _t['uuid'], f'[{style}]{icon}{status}[/]', '', _t['created_at'], '')
        console.rule(f'[bold green]Project({self.uri.project} Job({self.job.name}) Tasks List')
        console.print(table)

    def _render_multi_classification_job_report(self, report: t.Dict[str, t.Any], max_report_cols: int) -> None:
        if not report:
            console.print(':turtle: no report')
            return
        labels: t.Dict[str, t.Any] = report.get('labels', {})
        sort_label_names = sorted(list(labels.keys()))

        def _print_labels() -> None:
            if len(labels) == 0:
                return
            table = Table(box=box.SIMPLE)
            table.add_column('Label', style='cyan')
            keys = labels[sort_label_names[0]]
            for idx, _k in enumerate(keys):
                if _k == 'id':
                    continue
                if idx < max_report_cols + 1:
                    table.add_column(_k.capitalize())
                else:
                    table.add_column('...')
                    break
            for _k, _v in labels.items():
                table.add_row(_k, *(f'{float(_v[_k2]):.4f}' for idx, _k2 in enumerate(keys) if _k2 != 'id' and idx < max_report_cols + 1))
            console.rule(f"[bold green]{report['kind'].upper()} Label Metrics Report")
            console.print(table)

        def _print_confusion_matrix() -> None:
            cm = report.get('confusion_matrix', {})
            if not cm:
                return
            btable = Table(box=box.ROUNDED)
            btable.add_column('', style='cyan')
            for idx, n in enumerate(sort_label_names):
                if idx < max_report_cols:
                    btable.add_column(n)
                else:
                    btable.add_column('...')
                    break
            for idx, bl in enumerate(cm.get('binarylabel', [])):
                btable.add_row(sort_label_names[idx], *[f'{float(bl[i]):.4f}' for idx, i in enumerate(bl) if i != 'id' and idx < max_report_cols + 1])
            console.rule(f"[bold green]{report['kind'].upper()} Confusion Matrix")
            console.print(btable)
        _print_labels()
        _print_confusion_matrix()

    @classmethod
    def run(cls, project_uri: str, model_uri: str, dataset_uris: t.List[str], runtime_uri: str, version: str='', name: str='', desc: str='', step_spec: str='', resource_pool: str='', gencmd: bool=False, use_docker: bool=False, step: str='', task_index: int=0, task_num: int=0) -> str:
        _project_uri = URI(project_uri, expected_type=URIType.PROJECT)
        ok, version = EvaluationJob.run(_project_uri, model_uri, dataset_uris, runtime_uri, version=version, name=name, desc=desc, step_spec=step_spec, resource_pool=resource_pool, gencmd=gencmd, use_docker=use_docker, step=step, task_index=task_index, task_num=task_num)
        if ok:
            console.print(f':clap: success to create job(project id: [red]{_project_uri.full_uri}[/])')
            if _project_uri.instance_type == InstanceType.CLOUD:
                _job_uri = f'{_project_uri.full_uri}/evaluation/{version}'
            else:
                _job_uri = f'{version[:SHORT_VERSION_CNT]}'
            console.print(f':bird: run cmd to fetch eval info: [bold green]swcli eval info {_job_uri}[/]')
            return version
        else:
            console.print(f':collision: failed to create eval job, notice: [red]{version}[/]')
            return ''

    @classmethod
    def list(cls, project_uri: str='', fullname: bool=False, show_removed: bool=False, page: int=DEFAULT_PAGE_IDX, size: int=DEFAULT_PAGE_SIZE) -> t.Tuple[t.List[t.Any], t.Dict[str, t.Any]]:
        jobs, pager = EvaluationJob.list(URI(project_uri, expected_type=URIType.PROJECT), page, size)
        jobs = sort_obj_list(jobs, [Order('manifest.created_at', True)])
        return (jobs, pager)

class JobTermViewRich(JobTermView):

    @classmethod
    @BaseTermView._pager
    @BaseTermView._header
    def list(cls, project_uri: str='', fullname: bool=False, show_removed: bool=False, page: int=DEFAULT_PAGE_IDX, size: int=DEFAULT_PAGE_SIZE) -> t.Tuple[t.List[t.Any], t.Dict[str, t.Any]]:
        _jobs, _pager = super().list(project_uri, fullname, show_removed, page, size)
        table = Table(title='Job List', box=box.SIMPLE, expand=True)
        table.add_column('Name', justify='left', style='cyan', no_wrap=True)
        table.add_column('Model', no_wrap=True)
        table.add_column('Datasets')
        table.add_column('Runtime')
        table.add_column('Status', style='red')
        table.add_column('Resource', style='blue')
        table.add_column('Created At', style='magenta')
        table.add_column('Finished At', style='magenta')

        def _s(x: str) -> str:
            _end = -1 if fullname else SHORT_VERSION_CNT
            if ':' in x:
                _n, _v = x.split(':')
                return f'{_n}:{_v[:_end]}'
            else:
                return x[:_end]
        for _job in _jobs:
            if show_removed ^ _job.get('is_removed', False):
                continue
            _m = _job['manifest']
            _status, _style, _icon = cls.pretty_status(_m.get('jobStatus') or _m.get('status'))
            _datasets = '--'
            if _m.get('datasets'):
                _datasets = '\n'.join([_s(d) for d in _m['datasets']])
            _model = '--'
            if 'model' in _m:
                _model = _s(_m['model'])
            else:
                _model = f"{_m['modelName']}:{_s(_m['modelVersion'])}"
            _name = '--'
            if 'id' in _m:
                _name = _m['id']
            else:
                _name = _m['version'] if show_removed else _s(_m['version'])
            _runtime = '--'
            if 'runtime' in _m:
                if isinstance(_m['runtime'], str):
                    _runtime = _m['runtime']
                else:
                    _r = _m['runtime']
                    _runtime = f"[{_r['version']['id']}] {_r['name']}:{_r['version']['name'][:SHORT_VERSION_CNT]}"
            table.add_row(_name, _model, _datasets, _runtime, f'[{_style}]{_icon}{_status}[/]', f"{_m['device']}:{_m['deviceAmount']}" if 'device' in _m else '--', _m['created_at'], _m['finished_at'])
        console.print(table)
        return (_jobs, _pager)

class JobTermViewJson(JobTermView):

    @classmethod
    def list(cls, project_uri: str='', fullname: bool=False, show_removed: bool=False, page: int=DEFAULT_PAGE_IDX, size: int=DEFAULT_PAGE_SIZE) -> None:
        _data, _ = super().list(project_uri, fullname, show_removed, page, size)
        cls.pretty_json(_data)

    def info(self, page: int=DEFAULT_PAGE_IDX, size: int=DEFAULT_PAGE_SIZE, max_report_cols: int=DEFAULT_REPORT_COLS) -> None:
        _rt = self.job.info(page, size)
        if not _rt:
            console.print(':tea: not found info')
            return
        self.pretty_json(_rt)

def get_term_view(ctx_obj: t.Dict) -> t.Type[JobTermView]:
    return JobTermViewJson if ctx_obj.get('output') == 'json' else JobTermViewRich