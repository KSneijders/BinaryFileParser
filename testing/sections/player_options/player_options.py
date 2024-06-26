from __future__ import annotations

from binary_file_parser import BaseStruct, Retriever, Version
from binary_file_parser.types import int32, str16, uint8
from testing.sections.player_options.legacy_ai_file import LegacyAiFile
from testing.sections.player_options.resources import Resources
from testing.sections.scx_versions import DE_LATEST


class PlayerOptions(BaseStruct):
    # @formatter:off
    build_lists: list[str] =              Retriever(str16,                                    default = "",                   repeat = 16)
    """unused"""
    city_plans: list[str] =               Retriever(str16,                                    default = "",                   repeat = 16)
    """unused"""
    ai_names: list[str] =                 Retriever(str16,        min_ver = Version((1,  8)), default = "",                   repeat = 16)
    ai_files: list[LegacyAiFile] =        Retriever(LegacyAiFile,                             default_factory = LegacyAiFile, repeat = 16)
    ai_types: list[int] =                 Retriever(uint8,        min_ver = Version((1, 20)), default = 1,                    repeat = 16)
    separator1: int =                     Retriever(int32,        min_ver = Version((1,  2)), default = -99)
    starting_resources: list[Resources] = Retriever(Resources,    min_ver = Version((1, 14)), default_factory = Resources,    repeat = 16)
    separator2: int =                     Retriever(int32,        min_ver = Version((1,  2)), default = -99)
    # @formatter:on

    def __init__(self, struct_ver: Version = DE_LATEST, initialise_defaults = True, **retriever_inits):
        super().__init__(struct_ver, initialise_defaults = initialise_defaults, **retriever_inits)
