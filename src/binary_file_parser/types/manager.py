from __future__ import annotations

from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from binary_file_parser.retrievers import RetrieverRef
    from binary_file_parser.types.base_struct import BaseStruct

class Manager:
    """
    Superclass for creating grouped retriever references and functions on them. Use this to provide a more coherent API
    for struct modification when the internal struct is messy
    """
    __slots__ = '_struct'

    _refs: list[RetrieverRef] = []

    @classmethod
    def _add_ref(cls, ref: RetrieverRef):
        cls._refs.append(ref)

    def __init__(self, struct: BaseStruct):
        self._struct = struct

    def __str__(self):
        strings = [f"\n{self.__class__.__name__}:"]

        attributes = [
            attr for attr in dir(self)
            if not attr.startswith('_') and type(getattr(self, attr)).__name__ != 'method'
        ]

        table = {}
        for attr in attributes:
            value = Manager._format_value(getattr(self, attr))
            table[attr] = value

        longest_key = 0
        for key in table:
            if len(key) > longest_key:
                longest_key = len(key)

        for key, value in table.items():
            strings.append(f"\t{key.ljust(longest_key)} = {value}")

        return '\n'.join(strings)

    @staticmethod
    def _format_value(value: Any) -> str:
        if type(value) is str:
            return f"'{value}'"
        if type(value) is bytes:
            return f"b'{value.hex()}'"
        if isinstance(value, list) and len(value) > 0:
            item_string = Manager._format_value(value[0])
            if len(value) > 1:
                item_string += ', ' + Manager._format_value(value[1])
            if len(value) > 2:
                item_string += ', + ' + str(len(value) - 2) + ' more'

            return f"[{item_string}]"
        # Type check (with inheritance without needing import) ThxSO
        if 'BaseStruct' in [t.__name__ for t in type(value).__mro__]:
            return value.__class__.__name__

        return str(value)
