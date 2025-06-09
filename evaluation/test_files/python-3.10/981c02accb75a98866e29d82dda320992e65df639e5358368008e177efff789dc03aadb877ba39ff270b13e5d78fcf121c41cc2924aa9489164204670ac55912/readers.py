import json
import paramiko
from sdc_dp_helpers.api_utilities.file_managers import load_file
from sdc_dp_helpers.api_utilities.retry_managers import retry_handler
from sdc_dp_helpers.api_utilities.date_managers import date_range, date_string_change_format

class SFTPReader:
    """
    Custom FTP Reader
    """

    def __init__(self, creds_file, config_file):
        self._creds: dict = load_file(creds_file, 'yml')
        self.config = load_file(config_file)
        self._connect()

    def _connect(self):
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=str(self.config.get('hostname')), port=self.config.get('port', 22), username=str(self._creds.get('user')), password=str(self._creds.get('password')))
        self.sftp = ssh_client.open_sftp()

    @retry_handler(exceptions=TimeoutError, total_tries=2, initial_wait=60)
    def _query_handler(self, params: dict) -> dict:
        """
        Fetch XML from url
        """
        self._connect()
        file_path_var = self.config['file_path']
        file_path = file_path_var.format(dir_var=params.get('dir_var'), date_dir=params.get('date_dir'), date=params.get('date'))
        try:
            with self.sftp.open(file_path, 'r') as file:
                file.seek(0, 0)
                data = json.load(file)
                return {'data': data, 'dir_var': params.get('dir_var'), 'date': params.get('date').replace('-', '')}
        except FileNotFoundError:
            print(f'No file called: {file_path}')
            return {'data': None, 'dir_var': None, 'date': None}

    def run_query(self) -> list:
        start_date: str = self.config['start_date']
        end_date: str = self.config['end_date']
        for dir_var in self.config['directory_variables']:
            for date in date_range(start_date=start_date, end_date=end_date):
                date_dir = date_string_change_format(date_string=date, output_format='%Y/%-m/%-d')
                yield self._query_handler(params={'dir_var': dir_var, 'date_dir': date_dir, 'date': date})