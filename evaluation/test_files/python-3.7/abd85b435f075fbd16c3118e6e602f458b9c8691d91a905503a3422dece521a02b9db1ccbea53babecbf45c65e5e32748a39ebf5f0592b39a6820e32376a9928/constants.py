from enum import Enum
import os
import sys
PREFIXES = ['sl.', 'sl_', 'SL.', 'SL_']
TOKEN_FILE = 'sltoken.txt'
BUILD_SESSION_ID_FILE = 'buildSessionId.txt'
CONFIG_ENV_VARIABLE = 'sl_configuration'
AGENT_EVENT_BUILD_SCAN_ERROR = 4005
AGENT_EVENT_FOOTPRINTS_SUBMIT_ERROR = 4006
AGENT_EVENT_TEST_SUBMIT_ERROR = 4007
AGENT_EVENT_HEARTBEAT = 1003
AGENT_EVENT_HEARTBEAT_INTERVAL = 120
AGENT_EVENT_START = 1001
AGENT_EVENT_STOP = 1002
TECHNOLOGY = 'python'
DEFAULT_ENV = 'Unit Tests'
DEFAULT_LAB_ID = 'DefaultLabId'
TEST_IDENTIFIER = 'x-sl-testid'
PYTHON_FILES_REG = '^[^.#~!$@%^&*()+=,]+\\.pyw?$'
INIT_TEST_NAME = '__init'
INITIAL_COLOR = '00000000-0000-0000-0000-000000000000/__init'
MAX_ITEMS_IN_QUEUE = 5000
INTERVAL_IN_MILLISECONDS = 10000
INTERVAL_IN_SECONDS = INTERVAL_IN_MILLISECONDS / 1000
ACTIVE_EXECUTION_INTERVAL_IN_MILLISECONDS = 5000
WINDOWS = sys.platform.startswith('win')
LINUX = sys.platform.startswith('linux')
IN_TEST = os.environ.get('SL_TEST')
DEFAULT_WORKSPACEPATH = os.path.relpath(os.getcwd())
DEFAULT_BRANCH_NAME = 'main'
DEFAULT_COMMIT_LOG_SIZE = 100
NONE_SCM = 'none'
GIT_SCM = 'git'
GITHUB = 'Github'
WAIT_TIMEOUT = 120.0
XDIST_EXIT_TIMEOUT_IN_SECONDS = 60
AGENT_TYPE_TEST_LISTENER = 'TestListener'
AGENT_TYPE_BUILD_SCANNER = 'BuildScanner'
FUTURE_STATEMENTS = {'generators': 0, 'nested_scopes': 16, 'division': 8192, 'absolute_import': 16384, 'with_statement': 32768, 'print_function': 65536, 'unicode_literals': 131072}
MESSAGES_CANNOT_BE_NONE = " cannot be 'None'."

class MetadataKeys(object):
    APP_NAME = 'appName'
    BUILD = 'build'
    BRANCH = 'branch'
    CUSTOMER_ID = 'customerId'
    GENERATED = 'generated'
    TECHNOLOGY = 'technology'
    SCM_PROVIDER = 'scmProvider'
    SCM_VERSION = 'scmVersion'
    SCM_BASE_URL = 'scmBaseUrl'
    SCM = 'scm'
    COMMIT = 'commit'
    HISTORY = 'history'
    COMMIT_LOG = 'commitLog'
    CONTRIBUTORS = 'contributors'
    REPOSITORY_URL = 'repositoryUrl'
AST_ARGUMENTS_EMPTY_VALUES = {'args': [], 'vararg': None, 'kwarg': None, 'defaults': [], 'kw_defaults': [], 'kwonlyargs': [], 'posonlyargs': [], 'varargannotation': None, 'kwargannotation': None}

class TEST_RECOMMENDATION(object):
    timeout_sec = 60
    interval_sec = 5
    RSS = 'recommendationSetStatus'
    RSS_NOT_READY = 'notReady'
    RSS_NO_HISTORY = 'noHistory'
    RSS_READY = 'ready'
    RSS_ERROR = 'error'
    RSS_WONT_BE_READY = 'wontBeReady'
    TEST_SELECTION_ENABLED = 'testSelectionEnabled'

class TestSelectionStatus(str, Enum):
    RECOMMENDED_TESTS = 'recommendedTests'
    DISABLED = 'disabled'
    DISABLED_BY_CONFIGURATION = 'disabledByConfiguration'
    RECOMMENDATIONS_TIMEOUT = 'recommendationsTimeout'
    RECOMMENDATIONS_TIMEOUT_SERVER = 'recommendationsTimeoutOnServer'
    ERROR = 'error'