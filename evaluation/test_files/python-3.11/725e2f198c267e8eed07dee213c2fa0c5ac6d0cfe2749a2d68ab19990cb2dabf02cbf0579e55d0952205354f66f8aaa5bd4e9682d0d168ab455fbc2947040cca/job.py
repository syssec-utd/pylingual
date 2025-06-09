import base64
import sys
import time
from collections import OrderedDict
from urllib.parse import urlparse
import requests
from biolib import api, utils
from biolib.biolib_binary_format.stdout_and_stderr import StdoutAndStderr
from biolib.biolib_errors import BioLibError, CloudJobFinishedError
from biolib.biolib_logging import logger, logger_no_user_data
from biolib.compute_node.utils import SystemExceptionCodeMap, SystemExceptionCodes
from biolib.jobs.job_result import JobResult
from biolib.jobs.types import JobDict, CloudJobStartedDict, CloudJobDict
from biolib.tables import BioLibTable
from biolib.typing_utils import Optional, List, cast
from biolib.utils import IS_RUNNING_IN_NOTEBOOK

class Job:
    table_columns_to_row_map = OrderedDict({'ID': {'key': 'uuid', 'params': {'width': 36}}, 'Application': {'key': 'app_uri', 'params': {}}, 'Status': {'key': 'state', 'params': {}}, 'Started At': {'key': 'started_at', 'params': {}}})

    def __init__(self, job_dict: JobDict):
        self._uuid: str = job_dict['uuid']
        self._auth_token: str = job_dict['auth_token']
        self._job_dict: JobDict = job_dict
        self._result: Optional[JobResult] = None

    def __str__(self):
        return f"Job for {self._job_dict['app_uri']} created at {self._job_dict['created_at']} ({self._uuid})"

    def __repr__(self):
        return f'Job: {self._uuid}'

    @property
    def id(self) -> str:
        return self._uuid

    @property
    def result(self) -> JobResult:
        if not self._result:
            self._result = JobResult(job_uuid=self._uuid, job_auth_token=self._auth_token)
        return self._result

    def get_stdout(self) -> bytes:
        return self.result.get_stdout()

    def get_stderr(self) -> bytes:
        return self.result.get_stderr()

    def get_exit_code(self) -> int:
        return self.result.get_exit_code()

    def save_files(self, output_dir: str) -> None:
        self.result.save_files(output_dir=output_dir)

    def get_status(self) -> str:
        self._refetch_job_dict()
        return self._job_dict['state']

    def _get_cloud_job(self) -> CloudJobDict:
        self._refetch_job_dict()
        if self._job_dict['cloud_job'] is None:
            raise BioLibError(f'Job {self._uuid} did not register correctly. Try creating a new job.')
        return self._job_dict['cloud_job']

    @staticmethod
    def fetch_jobs(count: int) -> List['Job']:
        job_dicts = Job._get_job_dicts(count)
        return [Job(job_dict) for job_dict in job_dicts]

    @staticmethod
    def show_jobs(count: int=25) -> None:
        job_dicts = Job._get_job_dicts(count)
        BioLibTable(columns_to_row_map=Job.table_columns_to_row_map, rows=job_dicts, title='Jobs').print_table()

    @staticmethod
    def _get_job_dicts(count: int) -> List['JobDict']:
        job_dicts: List['JobDict'] = api.client.get(url='/jobs/', params={'page_size': str(count)}).json()['results']
        return job_dicts

    @staticmethod
    def _get_job_dict(uuid: str, auth_token: Optional[str]=None) -> JobDict:
        job_dict: JobDict = api.client.get(url=f'/jobs/{uuid}/', headers={'Job-Auth-Token': auth_token} if auth_token else None).json()
        return job_dict

    @staticmethod
    def create_from_uuid(uuid: str, auth_token: Optional[str]=None) -> 'Job':
        job_dict = Job._get_job_dict(uuid=uuid, auth_token=auth_token)
        return Job(job_dict)

    @staticmethod
    def print_logs_packages(stdout_and_stderr_packages_b64):
        for stdout_and_stderr_package_b64 in stdout_and_stderr_packages_b64:
            stdout_and_stderr_package = base64.b64decode(stdout_and_stderr_package_b64)
            stdout_and_stderr = StdoutAndStderr(stdout_and_stderr_package).deserialize()
            sys.stdout.write(stdout_and_stderr.decode())
            if not IS_RUNNING_IN_NOTEBOOK:
                sys.stdout.flush()
        sys.stdout.flush()

    def show(self) -> None:
        self._refetch_job_dict()
        BioLibTable(columns_to_row_map=Job.table_columns_to_row_map, rows=[self._job_dict], title=f'Job: {self._uuid}').print_table()

    def stream_logs(self) -> None:
        self._stream_logs()

    def _stream_logs(self, enable_print: bool=True) -> None:
        cloud_job = self._get_cloud_job_awaiting_started()
        compute_node_url = cloud_job['compute_node_url']
        logger_no_user_data.debug(f'Using compute node URL "{compute_node_url}"')
        if utils.BIOLIB_CLOUD_BASE_URL:
            compute_node_url = utils.BIOLIB_CLOUD_BASE_URL + str(urlparse(compute_node_url).path)
            logger_no_user_data.debug(f'Using cloud proxy URL from env var BIOLIB_CLOUD_BASE_URL: {compute_node_url}')
        if enable_print:
            self._print_full_logs(node_url=compute_node_url)
        final_status_messages: List[str] = []
        while True:
            time.sleep(2)
            status_json = self._get_job_status_from_compute_node(compute_node_url)
            job_is_completed = status_json['is_completed']
            for status_update in status_json['status_updates']:
                if job_is_completed:
                    final_status_messages.append(status_update['log_message'])
                else:
                    logger.info(f"Cloud: {status_update['log_message']}")
            if 'stdout_and_stderr_packages_b64' and enable_print:
                self.print_logs_packages(status_json['stdout_and_stderr_packages_b64'])
            if 'error_code' in status_json:
                error_code = status_json['error_code']
                error_message = SystemExceptionCodeMap.get(error_code, f'Unknown error code {error_code}')
                raise BioLibError(f'Cloud: {error_message}')
            if job_is_completed:
                break
        for message in final_status_messages:
            logger.info(f'Cloud: {message}')

    def _print_full_logs(self, node_url: str) -> None:
        try:
            response = requests.get(f'{node_url}/v1/job/{self._uuid}/status/?logs=full')
            if not response.ok:
                raise BioLibError(response.content)
        except Exception as error:
            logger.error(f'Could not get full streamed logs due to: {error}')
            raise BioLibError from error
        self.print_logs_packages(response.json()['streamed_logs_packages_b64'])

    def _get_cloud_job_awaiting_started(self) -> CloudJobStartedDict:
        max_retry_attempts = 100
        retry_interval_seconds = 10
        for _ in range(max_retry_attempts):
            cloud_job = self._get_cloud_job()
            if cloud_job['finished_at']:
                raise CloudJobFinishedError(f'The job {self._uuid} is already finished. Get its logs by calling `.get_stdout()`')
            if cloud_job and cloud_job['started_at']:
                if not cloud_job['compute_node_url']:
                    raise BioLibError(f'Failed to get URL to compute node for job {self._uuid}')
                return cast(CloudJobStartedDict, cloud_job)
            logger.info('Cloud: The job has been queued. Please wait...')
            time.sleep(retry_interval_seconds)
        raise BioLibError('Cloud: Timed out waiting for the job to start.')

    def _get_job_status_from_compute_node(self, compute_node_url):
        for _ in range(15):
            try:
                response = requests.get(f'{compute_node_url}/v1/job/{self._uuid}/status/')
                if not response.ok:
                    raise BioLibError(response.content)
                return response.json()
            except Exception:
                cloud_job = self._get_cloud_job()
                logger.debug('Failed to get status from compute node, retrying...')
                if cloud_job['finished_at']:
                    logger.debug('Job no longer exists on compute node, checking for error...')
                    if cloud_job['error_code'] != SystemExceptionCodes.COMPLETED_SUCCESSFULLY.value:
                        error_message = SystemExceptionCodeMap.get(cloud_job['error_code'], f"Unknown error code {cloud_job['error_code']}")
                        raise BioLibError(f'Cloud: {error_message}') from None
                    else:
                        logger.info(f'The job {self._uuid} is finished. Get its output by calling `.result()`')
                        return
                time.sleep(2)
        raise BioLibError('Failed to stream logs, did you lose internet connection?\nCall `.stream_logs()` on your job to resume streaming logs.')

    def _refetch_job_dict(self) -> None:
        self._job_dict = self._get_job_dict(self._uuid, self._auth_token)