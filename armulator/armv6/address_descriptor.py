from __future__ import absolute_import
from .memory_attributes import MemoryAttributes
from .full_address import FullAddress


class AddressDescriptor(object):
    def __init__(self):
        self.memattrs = MemoryAttributes()
        self.paddress = FullAddress()
