import struct

from binary_file_parser.types.byte_stream import ByteStream
from binary_file_parser.types.parseable import Parseable
from binary_file_parser.types.version import Version


class Bool(Parseable):
    __slots__ = "struct_symbol"

    def __init__(self, size: int, struct_symbol: str):
        super().__init__(size)
        self.struct_symbol = struct_symbol

    def _from_stream(self, stream: ByteStream, *, struct_ver: Version = Version((0,))) -> bool:
        return self._from_bytes(stream.get(self._size), struct_ver = struct_ver)

    def _from_bytes(self, bytes_: bytes, *, struct_ver: Version = Version((0,))) -> bool:
        return not not struct.unpack(self.struct_symbol, bytes_)[0]

    def _to_bytes(self, value: bool) -> bytes:
        return struct.pack(self.struct_symbol, 1 if value else 0)


bool8 = Bool(1, "<B")
bool16 = Bool(2, "<H")
bool32 = Bool(4, "<I")
bool64 = Bool(8, "<Q")
