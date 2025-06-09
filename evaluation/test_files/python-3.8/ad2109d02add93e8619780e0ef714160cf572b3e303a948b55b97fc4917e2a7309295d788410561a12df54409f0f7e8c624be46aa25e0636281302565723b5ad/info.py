"""ppm cache info命令的处理."""
import warnings
from pathlib import Path
from pmfp.utils.endpoint import EndPoint
from pmfp.utils.tools_info_utils import get_cache_dir, get_config_info
from pmfp.utils.remote_cache_utils import SourcePack
from .core import cache

class Info(EndPoint):
    """获取当前基本环境信息."""
    argparse_noflag = 'source_pack_string'
    schema = {'$schema': 'http://json-schema.org/draft-07/schema#', 'type': 'object', 'required': ['source_pack_string'], 'properties': {'source_pack_string': {'type': 'string', 'description': '资源包路径'}}}

    def do_main(self) -> None:
        cache_dir = get_cache_dir()
        conf = get_config_info()
        print('[cache dir]:')
        print(cache_dir)
        sourcepack = SourcePack.from_sourcepack_string(self.config.get('source_pack_string'))
        pack_dir = sourcepack.source_pack_path(cache_dir)
        if not pack_dir.is_dir():
            warnings.warn(f'{pack_dir} is not dir, not found')
            return
        else:
            with open(pack_dir.joinpath(conf['template_config_name']), encoding='utf-8') as f:
                print('[template info]:')
                print(f.read())
cache_info = cache.regist_sub(Info)