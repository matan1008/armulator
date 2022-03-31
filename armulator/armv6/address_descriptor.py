from armulator.armv6.memory_attributes import MemoryAttributes
from armulator.armv6.full_address import FullAddress


class AddressDescriptor:
    def __init__(self):
        self.memattrs = MemoryAttributes()
        self.paddress = FullAddress()
