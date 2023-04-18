import zlib

from binary_file_parser import BaseStruct, Retriever, Version
from binary_file_parser.types import Bytes, ByteStream
from testing.sections.BackgroundImage import BackgroundImage
from testing.sections.Cinematics import Cinematics
from testing.sections.DataHeader import DataHeader
from testing.sections.Diplomacy import Diplomacy
from testing.sections.FileData import FileData
from testing.sections.FileHeader import FileHeader
from testing.sections.GlobalVictory import GlobalVictory
from testing.sections.MapData import MapData
from testing.sections.Messages import Messages
from testing.sections.Options import Options
from testing.sections.PlayerData2 import PlayerData2
from testing.sections.TriggerData import TriggerData
from testing.sections.UnitData import UnitData


class ScenarioSections(BaseStruct):
    file_header: FileHeader = Retriever(FileHeader, default = FileHeader())
    data_header: DataHeader = Retriever(DataHeader, default = DataHeader(), remaining_compressed = True)
    messages: Messages = Retriever(Messages, default = Messages())
    cinematics: Cinematics = Retriever(Cinematics, default = Cinematics())
    background_image: BackgroundImage = Retriever(BackgroundImage, default = BackgroundImage())
    player_data2: PlayerData2 = Retriever(PlayerData2, default = PlayerData2())
    global_victory  : GlobalVictory = Retriever(GlobalVictory, default = GlobalVictory())
    diplomacy: Diplomacy = Retriever(Diplomacy, default = Diplomacy())
    options: Options = Retriever(Options, default = Options())
    map_data: MapData = Retriever(MapData, default = MapData())
    unit_data: UnitData = Retriever(UnitData, default = UnitData())
    trigger_data: TriggerData = Retriever(TriggerData, default = TriggerData())
    file_data: FileData = Retriever(FileData, default = FileData(), min_ver = Version((1, 40)))
    unknown1: bytes = Retriever(Bytes[8], default = b"\x00"*8, max_ver = Version((1, 37)))

    @classmethod
    def decompress(cls, bytes_: bytes) -> bytes:
        return zlib.decompress(bytes_, -zlib.MAX_WBITS)

    @classmethod
    def compress(cls, bytes_: bytes) -> bytes:
        deflate_obj = zlib.compressobj(9, zlib.DEFLATED, -zlib.MAX_WBITS)
        compressed = deflate_obj.compress(bytes_) + deflate_obj.flush()
        return compressed

    @classmethod
    def get_version(
        cls,
        stream: ByteStream,
        struct_version: Version = Version((0,)),
        parent: BaseStruct = None,
    ) -> Version:
        ver_str = stream.peek(4).decode("ASCII")
        return Version(map(int, ver_str.split(".")))

    def __init__(self, struct_version: Version = Version((1, 47)), parent: BaseStruct = None, initialise_defaults = True, **retriever_inits):
        super().__init__(struct_version, parent, initialise_defaults, **retriever_inits)
