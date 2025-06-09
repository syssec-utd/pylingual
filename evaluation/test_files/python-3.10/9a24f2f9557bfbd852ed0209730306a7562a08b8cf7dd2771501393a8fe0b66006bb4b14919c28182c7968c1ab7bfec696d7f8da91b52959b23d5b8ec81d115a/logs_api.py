import logging
from datetime import datetime as dt
from pathlib import Path
from typing import Optional
from urllib.parse import quote
from vmngclient.session import vManageSession
logger = logging.getLogger(__name__)

class LogsAPI:

    def __init__(self, session: vManageSession) -> None:
        self.session = session

    def get_auditlogs(self, file_path: Optional[str]=None, n_hours: int=1) -> None:
        query = {'query': {'condition': 'AND', 'rules': [{'field': 'entry_time', 'type': 'date', 'value': [f'{n_hours}'], 'operator': 'last_n_hours'}]}}
        addon_to_url = quote(str(query), safe='').replace('%27', '%22')
        url_path = f'/dataservice/auditlog/severity?query={addon_to_url}'
        logs = self.session.get_data(url_path)
        if file_path is None:
            file_path = str(Path(__file__).parents[0] / 'audit.log')
        with open(file_path, 'w') as file:
            for log in logs:
                time = dt.utcfromtimestamp(log['entry_time'] / 1000)
                time_readable = time.strftime('%Y-%m-%d %H:%M:%S')
                file.write(f"Entry time: {time_readable} - LogId: {log['logid']} - Log message: {log['logmessage']} - TenantId: {log['tenant']}\n")
        logger.info(f'Logs saved to {file_path}')
        return None