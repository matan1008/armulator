from abc import ABCMeta
from bitstring import BitArray
from armulator.armv6.configurations import configurations


class AbstractRegister(object):
    __metaclass__ = ABCMeta

    def __init__(self, length=32):
        reg_value = configurations["reset_values"].get(self.__class__.__name__, "")
        if len(reg_value) in (8, 16) or reg_value.startswith("0x") or reg_value.startswith("0X"):
            self.value = BitArray(hex=reg_value)
        elif len(reg_value) in (32, 64) or reg_value.startswith("0B") or reg_value.startswith("0b"):
            self.value = BitArray(bin=reg_value)
        else:
            self.value = BitArray(length=length)
