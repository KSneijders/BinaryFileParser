import struct

from binary_file_parser.types.parseable import Parseable
from binary_file_parser.types.byte_stream import ByteStream
from binary_file_parser.types.version import Version


class Float(Parseable):
    __slots__ = "struct_symbol"

    def __init__(self, size: int, struct_symbol: str):
        super().__init__(size)
        self.struct_symbol = struct_symbol

    def _from_stream(self, stream: ByteStream, *, struct_ver: Version = Version((0,))) -> float:
        return self._from_bytes(stream.get(self._size))

    def _from_bytes(self, bytes_: bytes, *, struct_ver: Version = Version((0,))) -> float:
        return struct.unpack(self.struct_symbol, bytes_)[0]

    def _to_bytes(self, value: float) -> bytes:
        return struct.pack(self.struct_symbol, value)

float16 = Float(2, "<e")
float32 = Float(4, "<f")
float64 = Float(8, "<d")
