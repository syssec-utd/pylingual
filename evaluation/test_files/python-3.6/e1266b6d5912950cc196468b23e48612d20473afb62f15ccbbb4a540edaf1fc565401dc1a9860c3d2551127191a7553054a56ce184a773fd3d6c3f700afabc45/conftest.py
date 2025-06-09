import tempfile
from typing import Iterable
import pytest
from chalk.sql import SQLiteFileSource, TableIngestProtocol
try:
    import dotenv
except ImportError:
    pass
else:
    dotenv.load_dotenv()

@pytest.fixture(scope='module')
def temp_sqlite_source() -> Iterable[TableIngestProtocol]:
    with tempfile.NamedTemporaryFile() as tmpfile:
        yield SQLiteFileSource(filename=tmpfile.name)