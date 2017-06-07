from abc import ABCMeta, abstractmethod


class MemoryType(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, size):
        pass

    @staticmethod
    def __getitem__(self, (address, size)):
        pass

    @abstractmethod
    def __setitem__(self, address_size, value):
        pass

    @abstractmethod
    def read(self, address, size):
        pass

    @staticmethod
    def write(self, address, size, value):
        pass


class RAM(MemoryType):
    def __init__(self, size):
        super(RAM, self).__init__(size)
        self.memory_array = bytearray(size)

    def __getitem__(self, (address, size)):
        chunk = self.memory_array[address:address + size]
        return chunk

    def __setitem__(self, address_size, value):
        self.memory_array[address_size[0]:address_size[0] + address_size[1]] = value

    def read(self, address, size):
        return self[address, size]

    def write(self, address, size, value):
        self.__setitem__((address, size), value)


MEMORY_TYPE_DICT = {
    "RAM": RAM
}
