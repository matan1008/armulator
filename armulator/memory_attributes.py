from bitstring import BitArray
from enum import Enum

MemType = Enum("MemType", "MemType_Normal MemType_Device MemType_StronglyOrdered")


class MemoryAttributes(object):
    def __init__(self):
        self.type = MemType.MemType_Normal
        self.innerattrs = BitArray(length=2)
        self.outerattrs = BitArray(length=2)
        self.innerhints = BitArray(length=2)
        self.outerhints = BitArray(length=2)
        self.innertransient = False
        self.outertransient = False
        self.shareable = False
        self.outershareable = False
