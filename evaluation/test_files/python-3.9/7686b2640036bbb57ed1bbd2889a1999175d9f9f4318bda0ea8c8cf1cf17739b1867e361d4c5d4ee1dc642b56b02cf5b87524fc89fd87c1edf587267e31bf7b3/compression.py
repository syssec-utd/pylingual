from __future__ import annotations
import importlib
from typing import Optional
from dissect.squashfs.c_squashfs import c_squashfs

def initialize(id: int, options: Optional[bytes]) -> Compression:
    modules = {c_squashfs.ZLIB_COMPRESSION: (NativeZlib,), c_squashfs.LZMA_COMPRESSION: (NativeLZMA,), c_squashfs.LZO_COMPRESSION: (NativeLZO, PythonLZO), c_squashfs.XZ_COMPRESSION: (NativeXZ,), c_squashfs.LZ4_COMPRESSION: (NativeLZ4, PythonLZ4), c_squashfs.ZSTD_COMPRESSION: (NativeZSTD,)}
    try:
        for mod in modules[id]:
            try:
                return mod()
            except ModuleNotFoundError:
                pass
        else:
            raise ImportError(f'No modules available ({modules[id]})')
    except ImportError:
        raise ValueError(f'Compression ID {id} requested but module ({modules[id]}) is not available')
    except KeyError:
        raise NotImplementedError(f'Unsupported compression ID: {id}')

class Compression:
    module = None

    def __init__(self):
        self._module = importlib.import_module(self.module)

    def compress(self, data: bytes) -> bytes:
        raise NotImplementedError()

    def decompress(self, data: bytes, expected: int) -> bytes:
        raise NotImplementedError()

class NativeZlib(Compression):
    module = 'zlib'

    def decompress(self, data: bytes, expected: int) -> bytes:
        return self._module.decompress(data)

class NativeLZMA(Compression):
    module = 'lzma'

    def decompress(self, data: bytes, expected: int) -> bytes:
        return self._module.decompress(data)

class NativeLZO(Compression):
    module = 'lzo'

    def decompress(self, data: bytes, expected: int) -> bytes:
        return self._module.decompress(data, False, expected)

class PythonLZO(Compression):
    module = 'dissect.util.compression.lzo'

    def decompress(self, data: bytes, expected: int) -> bytes:
        return self._module.decompress(data, False, expected)

class NativeXZ(Compression):
    module = 'lzma'

    def decompress(self, data: bytes, expected: int) -> bytes:
        return self._module.decompress(data)

class NativeLZ4(Compression):
    module = 'lz4.block'

    def decompress(self, data: bytes, expected: int) -> bytes:
        return self._module.decompress(data, expected)

class PythonLZ4(Compression):
    module = 'dissect.util.compression.lz4'

    def decompress(self, data: bytes, expected: int) -> bytes:
        return self._module.decompress(data)

class NativeZSTD(Compression):
    module = 'zstandard'

    def decompress(self, data: bytes, expected: int) -> bytes:
        return self._module.decompress(data)