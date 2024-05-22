from __future__ import annotations

from binary_file_parser import BaseStruct, Retriever, RetrieverCombiner, Version
from binary_file_parser.types import FixedLenArray, int32


class LegacyDisables(BaseStruct):
    @staticmethod
    def sync_num_techs(_, instance: LegacyDisables):
        num = len(instance._disabled_tech_ids)
        if num > LegacyDisables._disabled_tech_ids.dtype.length:
            raise ValueError(f"Cannot disable more than {num} techs")
        instance._num_disabled_techs = num

    @staticmethod
    def sync_num_units(_, instance: LegacyDisables):
        num = len(instance._disabled_unit_ids)
        if num > LegacyDisables._disabled_unit_ids.dtype.length:
            raise ValueError(f"Cannot disable more than {num} units")
        instance._num_disabled_units = num

    @staticmethod
    def sync_num_buildings(_, instance: LegacyDisables):
        num = len(instance._disabled_building_ids)
        if num > LegacyDisables._disabled_building_ids.dtype.length:
            raise ValueError(f"Cannot disable more than {num} buildings")
        instance._num_disabled_buildings = num

    # @formatter:off
    _num_disabled_techs: list[int] =              Retriever(int32,                    min_ver = Version((1, 18)), default = 0,                         repeat = 16, on_write = [sync_num_techs])
    _disabled_tech_ids_old: list[list[int]] =     Retriever(FixedLenArray[int32, 20], max_ver = Version((1, 17)), default_factory = lambda _: [-1]*20, repeat = 16)
    _disabled_tech_ids: list[list[int]] =         Retriever(FixedLenArray[int32, 30], min_ver = Version((1, 18)), default_factory = lambda _: [-1]*30, repeat = 16)

    _num_disabled_units: list[int] =              Retriever(int32,                    min_ver = Version((1, 18)), default = 0,                         repeat = 16, on_write = [sync_num_units])
    disabled_unit_ids: list[list[int]] =          Retriever(FixedLenArray[int32, 30], min_ver = Version((1, 18)), default_factory = lambda _: [-1]*30, repeat = 16)

    _num_disabled_buildings: list[int] =          Retriever(int32,                    min_ver = Version((1, 18)),                             default = 0,                         repeat = 16, on_write = [sync_num_buildings])
    _disabled_building_ids_old: list[list[int]] = Retriever(FixedLenArray[int32, 20], min_ver = Version((1, 18)), max_ver = Version((1, 24)), default_factory = lambda _: [-1]*20, repeat = 16)
    _disabled_building_ids: list[list[int]] =     Retriever(FixedLenArray[int32, 30], min_ver = Version((1, 25)),                             default_factory = lambda _: [-1]*30, repeat = 16)

    # references
    disabled_tech_ids: list[list[int]] =     RetrieverCombiner(_disabled_tech_ids_old,     _disabled_tech_ids)
    disabled_building_ids: list[list[int]] = RetrieverCombiner(_disabled_building_ids_old, _disabled_building_ids)
    # @formatter:on

    def __init__(self, struct_ver: Version = Version((1, 27)), initialise_defaults = True, **retriever_inits):
        super().__init__(struct_ver, initialise_defaults = initialise_defaults, **retriever_inits)
