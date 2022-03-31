from abc import ABC, abstractmethod


class MemoryType(ABC):

    @abstractmethod
    def __init__(self, size):
        self.size = size

    def __getitem__(self, address_size):
        (address, size) = address_size
        return self.read(address, size)

    def __setitem__(self, address_size, value):
        self.write(address_size[0], address_size[1], value)

    @abstractmethod
    def read(self, address, size):
        pass

    @abstractmethod
    def write(self, address, size, value):
        pass


class RAM(MemoryType):
    def __init__(self, size):
        super(RAM, self).__init__(size)
        self.memory_array = bytearray(size)

    def read(self, address, size):
        chunk = self.memory_array[address:address + size]
        return chunk

    def write(self, address, size, value):
        self.memory_array[address:address + size] = value


MEMORY_TYPE_DICT = {
    'RAM': RAM
}
