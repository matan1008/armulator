
from armulator.armv6.memory_controller_hub import MemoryController, MemoryControllerHub
from armulator.armv6.memory_types import RAM
from armulator.armv6.address_descriptor import AddressDescriptor


def test_set():
    value = 0x00000012
    address_descriptor = AddressDescriptor()
    address_descriptor.paddress.physicaladdress = 0x0F000000
    ram_memory = RAM(0x100)
    ram_memory[0, 4] = b'\x00\x00\x00\x00'
    mc = MemoryController(ram_memory, 0x0F000000, 0x0F000100)
    mch = MemoryControllerHub()
    mch.memories.append(mc)
    mch[address_descriptor, 4] = value
    assert ram_memory[0, 4] == b'\x12\x00\x00\x00'
    assert value == 0x00000012
