"""学習とかで使う汎用的な関数などを定義する
"""
from contextlib import contextmanager
from importlib import import_module
from logging import getLogger, StreamHandler, FileHandler, Formatter
from time import time
import numpy as np
import requests
import seaborn as sns
from tqdm import tqdm

def ipython_debug(function):

    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Exception as e:
            from IPython.core.debugger import set_trace
            set_trace()
    return wrapper

def import_string(dotted_path):
    """
    Import a dotted module path and return the attribute/class designated by the
    last name in the path. Raise ImportError if the import failed.
    """
    try:
        module_path, class_name = dotted_path.rsplit('.', 1)
    except ValueError as err:
        raise ImportError("%s doesn't look like a module path" % dotted_path) from err
    module = import_module(module_path)
    try:
        return getattr(module, class_name)
    except AttributeError as err:
        raise ImportError('Module "%s" does not define a "%s" attribute/class' % (module_path, class_name)) from err

def set_optuna_silent():
    import optuna
    optuna.logging.set_verbosity(optuna.logging.WARNING)

def set_default_style(style='ticks', font='Noto Sans CJK JP', colors=None):
    """
    matplotlib, seaborn でのグラフ描写スタイルを標準的仕様に設定するメソッド
    このメソッドの呼び出しは破壊的です。

    Args:
        style(str):
        font(str):
        colors(None | list[str]):

    Returns: None

    """
    sns.set(style=style, font=font)
    if colors is None:
        colors = ['windows blue', 'amber', 'greyish', 'faded green', 'dusty purple']
        sns.set_palette(sns.xkcd_palette(colors))
    return

class Timer:

    def __init__(self, logger=None, format_str='{:.3f}[s]', prefix=None, suffix=None, sep=' '):
        if prefix:
            format_str = str(prefix) + sep + format_str
        if suffix:
            format_str = format_str + sep + str(suffix)
        self.format_str = format_str
        self.logger = logger
        self.start = None
        self.end = None

    @property
    def duration(self):
        if self.end is None:
            return 0
        return self.end - self.start

    def __enter__(self):
        self.start = time()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end = time()
        out_str = self.format_str.format(self.duration)
        if self.logger:
            self.logger.info(out_str)
        else:
            print(out_str)

def timer(logger=None, format_str='{:.3f}[s]', prefix=None, suffix=None, sep=' '):
    return Timer(logger=logger, format_str=format_str, prefix=prefix, suffix=suffix, sep=sep)

def get_logger(name, log_level='DEBUG', output_file=None, handler_level='INFO', output_level='DEBUG', format_str='%(message)s'):
    """
    :param str name:
    :param str log_level:
    :param str | None output_file:
    :return: logger
    """
    logger = getLogger(name)
    formatter = Formatter(format_str)
    handler = StreamHandler()
    logger.setLevel(log_level)
    handler.setLevel(handler_level)
    handler.setFormatter(formatter)
    logger.handlers = []
    logger.addHandler(handler)
    if output_file:
        file_handler = FileHandler(output_file)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(output_level)
        logger.addHandler(file_handler)
    return logger
logger = get_logger(__name__)

def get_train_valid_set(fold, X, y):
    if len(X) != len(y):
        raise ValueError()
    items = []
    for train_idx, test_idx in fold.split(X, y):
        item = ((X[train_idx], y[train_idx]), (X[test_idx], y[test_idx]), (train_idx, test_idx))
        items.append(item)
    return items

def download_from_gdrive(id, destination):
    """
    Download file from Google Drive
    :param str id: g-drive id
    :param str destination: output path
    :return:
    """
    url = 'https://docs.google.com/uc?export=download'
    session = requests.Session()
    response = session.get(url, params={'id': id}, stream=True)
    token = get_confirm_token(response)
    if token:
        logger.info('get download warning. set confirm token.')
        params = {'id': id, 'confirm': token}
        response = session.get(url, params=params, stream=True)
    save_response_content(response, destination)

def get_confirm_token(response):
    """
    verify whether warned or not.

    [note] In Google Drive Api, if requests content size is large,
    the user are send to verification page.

    :param requests.Response response:
    :return:
    """
    for k, v in response.cookies.items():
        if k.startswith('download_warning'):
            return v
    return None

def save_response_content(response, destination):
    """
    :param requests.Response response:
    :param str destination:
    :return:
    """
    chunk_size = 1024 * 1024
    logger.info('start downloading...')
    with open(destination, 'wb') as f:
        for chunk in tqdm(response.iter_content(chunk_size), unit='MB'):
            f.write(chunk)
    logger.info('Finish!!')
    logger.info('Save to:{}'.format(destination))

def sigmoid(x: np.ndarray, threshold=15.0) -> np.ndarray:
    """
    apply sigmoid function safety

    Args:
        x:
        threshold:

    Returns:

    """
    x = np.clip(x, -threshold, threshold)
    return 1.0 / (1.0 + np.exp(-x))

def param_to_name(params: dict, key_sep='_', key_value_sep='=') -> str:
    """
    dict を `key=value` で連結した string に変換します.

    Args:
        params:
        key_sep:
            key 同士を連結する際に使う文字列.
        key_value_sep:
            それぞれの key / value を連結するのに使う文字列.
            `"="` が指定されると例えば { 'foo': 10 } は `"foo=10"` に変換されます.

    Returns:
        文字列化した dict
    """
    sorted_params = sorted(params.items())
    return key_sep.join(map(lambda x: key_value_sep.join(map(str, x)), sorted_params))