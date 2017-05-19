from bitstring import BitArray
from configurations import *
from memory_types import *


class Memory(object):
    def __init__(self):
        self.memories = []
        self.__init_memory__()

    def __init_memory__(self):
        for i in memory_list:
            mem = MemoryTypeDict[i[0]](i[2] - i[1])
            self.memories.append((mem, (i[1], i[2])))

    def get_memory_by_address(self, address):
        for memory in self.memories:
            if memory[1][0] <= address < memory[1][1]:
                return memory

    def __getitem__(self, (memaddrdesc, size)):
        # mock
        assert size == 1 or size == 2 or size == 4 or size == 8
        memory = self.get_memory_by_address(memaddrdesc.paddress.physicaladdress.uint)
        if memory is not None:
            data = BitArray(bytes=memory[0][memaddrdesc.paddress.physicaladdress.uint - memory[1][0], size])
            data.byteswap()
            return data
        return BitArray(length=size * 8)

    def __setitem__(self, memaddrdesc_size, value):
        # mock
        memaddrdesc = memaddrdesc_size[0]
        size = memaddrdesc_size[1]
        assert size == 1 or size == 2 or size == 4 or size == 8
        memory = self.get_memory_by_address(memaddrdesc.paddress.physicaladdress.uint)
        if memory:
            memory[0][memaddrdesc.paddress.physicaladdress.uint - memory[1][0], size] = value.hex.decode("hex")

    def set_bits(self, memaddrdesc, size, ind, amount, bits):
        # mock
        raise NotImplementedError()
