import struct

from armulator.armv6.memory_types import MEMORY_TYPE_DICT

LENGTH_FORMATS = {
    1: 'B',
    2: '<H',
    4: '<I',
    8: '<Q',
}


def to_int(bytes_: bytes, length: int) -> int:
    return struct.unpack(LENGTH_FORMATS[length], bytes_)[0]


def from_int(int_: int, length: int) -> bytes:
    return struct.pack(LENGTH_FORMATS[length], int_)


class MemoryController:
    """
    One memory or i/o device
    """

    def __init__(self, mem, beginning, end):
        self.mem = mem
        self.beginning = beginning
        self.end = end


class MemoryControllerHub:
    """
    Provides the CPU and memory and input/output devices to interact
    """

    def __init__(self):
        self.memories = []

    @staticmethod
    def from_memory_list(memory_list):
        mch = MemoryControllerHub()
        for memory in memory_list:
            mch.add_memory(**memory)
        return mch

    def add_memory(self, mem_type, beginning, end):
        mem = MEMORY_TYPE_DICT[mem_type](end - beginning)
        self.memories.append(MemoryController(mem, beginning, end))

    def get_memory_by_address(self, address):
        for memory in self.memories:
            if memory.beginning <= address < memory.end:
                return memory

    def __getitem__(self, memaddrdesc_size):
        """
        Reads memory as a little endian
        :memaddrdesc: AddressDescriptor object
        :size: Size in bytes to read
        :return: BitArray of data
        """
        (memaddrdesc, size) = memaddrdesc_size
        assert size == 1 or size == 2 or size == 4 or size == 8
        mc = self.get_memory_by_address(memaddrdesc.paddress.physicaladdress)
        if mc is not None:
            data = mc.mem[memaddrdesc.paddress.physicaladdress - mc.beginning, size]
            return to_int(data, size)
        return 0

    def __setitem__(self, memaddrdesc_size, value):
        """
        Writes memory as a little endian
        :memaddrdesc_size: tuple AddressDescriptor object and size in bytes
        :value: Bytes to write
        """
        memaddrdesc = memaddrdesc_size[0]
        size = memaddrdesc_size[1]
        assert size == 1 or size == 2 or size == 4 or size == 8
        mc = self.get_memory_by_address(memaddrdesc.paddress.physicaladdress)
        if mc is not None:
            mc.mem[memaddrdesc.paddress.physicaladdress - mc.beginning, size] = from_int(value, size)

    def set_bits(self, memaddrdesc, size, ind, amount, bits):
        # mock
        raise NotImplementedError()
