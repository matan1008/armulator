from bitstring import BitArray

from armulator.armv6.configurations import configurations
from armulator.armv6.exclusive_monitors import GlobalExclusiveMonitor
from armulator.armv6.memory_types import MEMORY_TYPE_DICT


class MemoryController(object):
    """
    One memory or i/o device
    """

    def __init__(self, mem, beginning, end):
        self.mem = mem
        self.beginning = beginning
        self.end = end


class MemoryControllerHub(object):
    """
    Provides the CPU and memory and input/output devices to interact
    """

    def __init__(self):
        self.memories = []
        self.init_memory()
        if configurations["impdef_exclusive_monitors"]:
            self.global_monitor = GlobalExclusiveMonitor(configurations["impdef_exclusives_reservation_granule"])

    def init_memory(self):
        for memory in configurations["memory_list"]:
            self.add_memory(**memory)

    def add_memory(self, mem_type, beginning, end):
        mem = MEMORY_TYPE_DICT[mem_type](end - beginning)
        self.memories.append(MemoryController(mem, beginning, end))

    def get_memory_by_address(self, address):
        for memory in self.memories:
            if memory.beginning <= address < memory.end:
                return memory

    def __getitem__(self, (memaddrdesc, size)):
        """
        Reads memory as a little endian
        :memaddrdesc: AddressDescriptor object
        :size: Size in bytes to read
        :return: BitArray of data
        """
        assert size == 1 or size == 2 or size == 4 or size == 8
        mc = self.get_memory_by_address(memaddrdesc.paddress.physicaladdress.uint)
        if mc is not None:
            data = BitArray(bytes=mc.mem[memaddrdesc.paddress.physicaladdress.uint - mc.beginning, size])
            data.byteswap()
            return data
        return BitArray(length=size * 8)

    def __setitem__(self, memaddrdesc_size, value):
        """
        Writes memory as a little endian
        :memaddrdesc_size: tuple AddressDescriptor object and size in bytes
        :value: Bytes to write
        """
        memaddrdesc = memaddrdesc_size[0]
        size = memaddrdesc_size[1]
        assert size == 1 or size == 2 or size == 4 or size == 8
        mc = self.get_memory_by_address(memaddrdesc.paddress.physicaladdress.uint)
        if mc is not None:
            value.byteswap()
            mc.mem[memaddrdesc.paddress.physicaladdress.uint - mc.beginning, size] = value.hex.decode("hex")

    def set_bits(self, memaddrdesc, size, ind, amount, bits):
        # mock
        raise NotImplementedError()
