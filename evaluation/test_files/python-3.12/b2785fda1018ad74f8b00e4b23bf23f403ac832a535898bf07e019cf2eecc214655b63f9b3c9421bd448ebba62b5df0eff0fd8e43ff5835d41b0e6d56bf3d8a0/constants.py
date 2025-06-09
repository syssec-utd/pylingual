import datetime
import os
import posixpath
from pathlib import Path
from mlfoundry.internal_namespace import NAMESPACE
DEFAULT_TRACKING_URI = 'https://app.truefoundry.com'
RUN_LOGS_DIR = posixpath.join('mlf', 'run-logs')
MLFOUNDRY_TMP_FOLDER = Path(os.path.abspath('./.mlfoundry'))
RUN_TMP_FOLDER = Path(os.path.join(MLFOUNDRY_TMP_FOLDER, 'logdirs'))
RUN_PREDICTIONS_FOLDER = Path(os.path.join(RUN_TMP_FOLDER, 'predictions'))
RUN_DATASET_FOLDER = Path(os.path.join(RUN_TMP_FOLDER, 'datasets'))
RUN_STATS_FOLDER = Path(os.path.join(RUN_TMP_FOLDER, 'stats'))
RUN_METRICS_FOLDER = Path(os.path.join(RUN_TMP_FOLDER, 'metrics'))
GET_RUN_TMP_FOLDER = Path(os.path.join(MLFOUNDRY_TMP_FOLDER, 'getdirs'))
GET_RUN_PREDICTIONS_FOLDER = Path(os.path.join(GET_RUN_TMP_FOLDER, 'predictions'))
GET_RUN_DATASET_FOLDER = Path(os.path.join(GET_RUN_TMP_FOLDER, 'datasets'))
TIME_LIMIT_THRESHOLD = datetime.timedelta(minutes=1)
FILE_SIZE_LIMIT_THRESHOLD = pow(10, 7)
MULTI_DIMENSIONAL_METRICS = 'multi_dimensional_metrics'
NON_MULTI_DIMENSIONAL_METRICS = 'non_multi_dimensional_metrics'
PROB_MULTI_DIMENSIONAL_METRICS = 'prob_multi_dimensional_metrics'
PROB_NON_MULTI_DIMENSIONAL_METRICS = 'prob_non_multi_dimensional_metrics'
ACTUAL_PREDICTION_COUNTS = 'actuals_predictions_counts'
MLF_FOLDER_NAME = 'mlf'
MLRUNS_FOLDER = 'mlruns'
MLRUNS_FOLDER_NAME = Path(os.path.join(MLF_FOLDER_NAME, MLRUNS_FOLDER))
RUN_ID_COL_NAME = 'run_id'
RUN_NAME_COL_NAME = 'run_name'
TIME_FORMAT = '%Y-%m-%d_%H-%M-%S'
GIT_COMMIT_TAG_NAME = NAMESPACE('git.commit_sha')
GIT_BRANCH_TAG_NAME = NAMESPACE('git.branch_name')
GIT_REMOTE_URL_NAME = NAMESPACE('git.remote_url')
GIT_DIRTY_TAG_NAME = NAMESPACE('git.dirty')
PATCH_FILE_ARTIFACT_DIR = NAMESPACE / 'git'
LOG_DATASET_ARTIFACT_DIR = NAMESPACE / 'datasets'
PATCH_FILE_NAME = 'uncommitted_changes.patch.txt'
PYTHON_VERSION_TAG_NAME = NAMESPACE('python_version')
MLFOUNDRY_VERSION_TAG_NAME = NAMESPACE('mlfoundry_version')
ALM_SCALAR_METRICS_PATTERN = NAMESPACE('auto_logged_metrics.{data_slice}.{metric_name}')
ALM_ARTIFACT_PATH = NAMESPACE / 'auto_logged_metrics'
ALM_METRICS_FILE_NAME = 'metrics.json'