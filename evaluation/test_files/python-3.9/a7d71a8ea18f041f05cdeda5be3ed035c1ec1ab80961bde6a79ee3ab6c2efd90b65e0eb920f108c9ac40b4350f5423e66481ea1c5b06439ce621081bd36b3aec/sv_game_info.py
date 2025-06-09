from twnet_parser.pretty_print import PrettyPrint
from twnet_parser.packer import Unpacker
from twnet_parser.chunk_header import ChunkHeader
from twnet_parser.packer import pack_int
from typing import Literal

class MsgSvGameInfo(PrettyPrint):

    def __init__(self, chunk_header: ChunkHeader=ChunkHeader(), game_flags: int=0, score_limit: int=0, time_limit: int=0, match_num: int=0, match_current: int=0) -> None:
        self.message_type: Literal['system', 'game'] = 'game'
        self.message_name: str = 'sv_game_info'
        self.system_message: bool = False
        self.message_id: int = 19
        self.header: ChunkHeader = chunk_header
        self.game_flags: int = game_flags
        self.score_limit: int = score_limit
        self.time_limit: int = time_limit
        self.match_num: int = match_num
        self.match_current: int = match_current

    def unpack(self, data: bytes) -> bool:
        unpacker = Unpacker(data)
        self.game_flags = unpacker.get_int()
        self.score_limit = unpacker.get_int()
        self.time_limit = unpacker.get_int()
        self.match_num = unpacker.get_int()
        self.match_current = unpacker.get_int()
        return True

    def pack(self) -> bytes:
        return pack_int(self.game_flags) + pack_int(self.score_limit) + pack_int(self.time_limit) + pack_int(self.match_num) + pack_int(self.match_current)