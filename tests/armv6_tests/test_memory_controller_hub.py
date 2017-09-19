from bitstring import BitArray
from armulator.armv6.memory_controller_hub import MemoryController, MemoryControllerHub
from armulator.armv6.memory_types import RAM
from armulator.armv6.address_descriptor import AddressDescriptor


def test_set():
    value = BitArray(hex="0x00000012")
    address_descriptor = AddressDescriptor()
    address_descriptor.paddress.physicaladdress = BitArray(uint=0x0F000000, length=40)
    ram_memory = RAM(0x100)
    ram_memory[0, 4] = "\x00\x00\x00\x00"
    mc = MemoryController(ram_memory, 0x0F000000, 0x0F000100)
    mch = MemoryControllerHub()
    mch.memories.append(mc)
    mch[address_descriptor, 4] = value
    assert ram_memory[0, 4] == "\x12\x00\x00\x00"
    assert value == BitArray(hex="0x00000012")
