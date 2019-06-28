from armulator.armv6.permissions import Permissions
from armulator.armv6.address_descriptor import AddressDescriptor
from bitstring import BitArray
from enum import Enum

TLBRecType = Enum(
        "TLBRecType",
        "TLBRecType_SmallPage TLBRecType_LargePage TLBRecType_Section TLBRecType_Supersection TLBRecType_MMUDisabled"
)


class TLBRecord(object):
    def __init__(self):
        self.perms = Permissions()
        self.ng = False
        self.domain = BitArray(length=4)
        self.contiguousbit = False
        self.level = 0
        self.blocksize = 0
        self.addrdesc = AddressDescriptor()
