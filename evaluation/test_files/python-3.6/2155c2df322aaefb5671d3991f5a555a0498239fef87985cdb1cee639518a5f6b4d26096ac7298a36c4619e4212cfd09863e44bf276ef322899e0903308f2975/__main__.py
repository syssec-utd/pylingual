import builtins
import os
import sys
import logging
from pathlib import Path
from .version import VERSION
install_code = "\n# 添加 python_devtools中`debug` 函数到builtins中\nimport builtins\ntry:\n    from python_devtools import debug\nexcept ImportError:\n    pass\nelse:\n    setattr(builtins, 'debug', debug)\n"
logger = logging.getLogger(__name__)

def print_code() -> int:
    print(install_code)
    return 0

def install() -> int:
    print('警告:此命令是实验性的，请在github.com/llango/sha_python_devtools报告问题]\n')
    if hasattr(builtins, 'debug'):
        print('python_devtools 开发工具似乎已经安装好了')
        return 0
    try:
        import sitecustomize
    except ImportError:
        paths = [Path(p) for p in sys.path]
        try:
            path = next((p for p in paths if p.is_dir() and p.name == 'site-packages'))
        except StopIteration:
            logger.info(f'无法文件一个合适的路径来保存`sitecustomize.py`sys.path:{paths}')
            return 1
        else:
            install_path = path / 'sitecustomize.py'
    else:
        install_path = Path(sitecustomize.__file__)
    print(f'已找到路径 "{install_path}" 来安装 python_devtools 到 __builtins__')
    print('为了安装python_devtools, 运行如下命令:\n')
    if os.access(install_path, os.W_OK):
        print(f'    python -m python_devtools print-code >> {install_path}\n')
    else:
        print(f'    python -m python_devtools print-code | sudo tee -a {install_path} > /dev/null\n')
        print('注意:“sudo”是必需的，因为当前用户不能写该路径。')
    return 0
if __name__ == '__main__':
    if 'install' in sys.argv:
        sys.exit(install())
    elif 'print-code' in sys.argv:
        sys.exit(print_code())
    else:
        print(f'python_devtools v{VERSION}, CLI 使用方式: python -m python_devtools [install|print-code]')
        sys.exit(1)