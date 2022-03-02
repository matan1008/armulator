from enum import Enum, auto


class MemType(Enum):
    NORMAL = auto()
    DEVICE = auto()
    STRONGLY_ORDERED = auto()


class MemoryAttributes:
    def __init__(self):
        self.type = MemType.NORMAL
        self.innerattrs = 0b00
        self.outerattrs = 0b00
        self.innerhints = 0b00
        self.outerhints = 0b00
        self.innertransient = False
        self.outertransient = False
        self.shareable = False
        self.outershareable = False
