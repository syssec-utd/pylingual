from functools import cache
from enum import Enum
from typing import Any
from erdb.table import Table
from erdb.loaders import GAME_VERSIONS
from erdb.typing.game_version import GameVersion
from erdb.typing.api_version import ApiVersion
GameVersionEnum = Enum('GameVersionEnum', {'latest': 'latest'} | {str(v).replace('.', '_'): str(v) for v in GAME_VERSIONS})

@cache
def generate(api: ApiVersion, game_version: GameVersionEnum, table: Table) -> dict:
    if game_version == GameVersionEnum.latest:
        return generate(api, list(GameVersionEnum)[1], table)
    ver = GameVersion.from_string(game_version.value)
    return table.make_generator(ver).generate(api)

def precache_data():
    for game_version in GameVersionEnum:
        print(f'>>> Precaching version {game_version.value}:', flush=True)
        for tb in Table.effective():
            for api in tb.spec.model.keys():
                print(f'> {tb.title} [v{api}]', flush=True)
                generate(api, game_version, tb)
        print(flush=True)

def as_str(obj: Any, field: str) -> str:
    v = getattr(obj, field)
    return v.value if isinstance(v, Enum) else str(v)