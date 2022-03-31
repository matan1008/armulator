from abc import ABC

from armulator.armv6.bits_ops import bit_at, set_bit_at, substring, set_substring
from armulator.armv6.configurations import configurations


class AbstractRegister(ABC):
    def __init__(self, length=32):
        self.length = length
        reg_value = configurations.reset_values.get(self.__class__.__name__, '')
        if reg_value:
            self.value = int(reg_value, 0)
        else:
            self.value = 0

    def _at(self, index):
        return bit_at(self.value, index)

    def _set_at(self, index, value):
        self.value = set_bit_at(self.value, index, value)

    def __getitem__(self, item):
        if isinstance(item, int):
            return bit_at(self.value, item)
        return substring(self.value, item.start, item.stop)

    def __setitem__(self, item, value):
        if isinstance(item, int):
            self.value = set_bit_at(self.value, item, value)
            return
        self.value = set_substring(self.value, item.start, item.stop, value)
