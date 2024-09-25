import contextlib
from io import StringIO


class TabbedStringIO(StringIO):
    def __init__(self, ident: int = 0):
        super().__init__()
        self.ident = ident

    @contextlib.contextmanager
    def tabbed(self):
        self.ident += 4
        yield
        self.ident -= 4

    def _tab(self) -> str:
        return ' ' * self.ident

    def writeln(self, string: str = "") -> int:
        return self.write("\n" + self._tab() + string)


class BytePrefixStringIO(TabbedStringIO):

    def __init__(self, ident: int = 0, *, hex_block_count = 8):
        super().__init__(ident)

        self.hex_block_count = hex_block_count

    @property
    def hex_width(self):
        return self.hex_block_count * 3

    @property
    def prefix_width(self):
        return self.hex_width + 1

    def write(self, s, /, prefixed = False) -> int:
        if prefixed:
            s = " " * self.prefix_width + s
        return super().write(s)

    def writepref(self, string: str):
        return self.write(string, prefixed = True)

    def writeln(self, string: str = "", hex_prefix: bytes = b"", force_single_line: bool = False) -> int:
        if string == "":
            return super().writeln(string)

        hex_lines = self._to_hex_lines(hex_prefix)
        string_lines = string.splitlines()

        is_single_line = len(hex_lines) <= 1 and len(string_lines) <= 1 or hex_prefix == b""
        if is_single_line or force_single_line:
            return self.writepref("\n" + hex_lines[0] + self._tab() + string)

        max_len = max(len(hex_lines), len(string_lines))

        hex_iter = iter(hex_lines)
        str_iter = iter(string_lines)

        complete_string = "\n".join(
            next(hex_iter, ' ' * self.prefix_width) + self._tab() + next(str_iter, '') for _ in range(max_len)
        )

        return self.writepref("\n" + complete_string)

    def _to_hex_lines(self, bytes_: bytes) -> list[str]:
        hex_repr = bytes_.hex()

        hex_blocks = [hex_repr[i:i + 2] for i in range(0, max(len(hex_repr), 1), 2)]
        hex_lines = [hex_blocks[i:i + self.hex_block_count] for i in range(0, len(hex_blocks), self.hex_block_count)]

        return [" ".join(line).ljust(self.prefix_width) for line in hex_lines]

    def copy(self):
        return BytePrefixStringIO(self.ident, hex_block_count = self.hex_block_count)
