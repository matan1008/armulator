from enum import Enum, auto

from armulator.armv6.address_descriptor import AddressDescriptor
from armulator.armv6.permissions import Permissions


class TLBRecType(Enum):
    SMALL_PAGE = auto()
    LARGE_PAGE = auto()
    SECTION = auto()
    SUPERSECTION = auto()
    MMU_DISABLED = auto()


class TLBRecord:
    def __init__(self):
        self.perms = Permissions()
        self.ng = 0
        self.domain = 0b0000
        self.contiguousbit = 0
        self.level = 0
        self.blocksize = 0
        self.addrdesc = AddressDescriptor()
