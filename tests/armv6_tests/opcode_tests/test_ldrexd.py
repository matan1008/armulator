from armulator.armv6.memory_controller_hub import MemoryController
from armulator.armv6.memory_types import RAM
from armulator.armv6.opcodes.concrete.ldrexd_a1 import LdrexdA1
from armulator.armv6.opcodes.concrete.ldrexd_t1 import LdrexdT1


def test_ldrexd_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11101000110100100001001101111111
    arm.opcode_len = 32
    # setting Data Region registers
    arm.registers.drsrs[0].en = 1  # enabling memory region
    arm.registers.drsrs[0].rsize = 0b00011  # setting region size
    arm.registers.drbars[0] = 0x0F000000  # setting region base address
    arm.registers.dracrs[0].ap = 0b011  # setting access permissions
    arm.registers.mpuir.iregion = 0x01  # declaring the region
    arm.registers.mpuir.dregion = 0x01  # declaring the region
    ram_memory = RAM(0x100)
    ram_memory.write(0, 8, b'\xaa\xbb\xcc\xdd\x11\x22\x33\x44')
    mc = MemoryController(ram_memory, 0x0F000000, 0x0F000100)
    arm.mem.memories.append(mc)
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == LdrexdT1
    assert opcode.n == 2
    assert opcode.t == 1
    assert opcode.t2 == 3
    arm.registers.set(opcode.n, 0x0F000000)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.t) == 0xDDCCBBAA
    assert arm.registers.get(opcode.t2) == 0x44332211


def test_ldrexd_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100001101100000010111110011111
    arm.opcode_len = 32
    # setting Data Region registers
    arm.registers.drsrs[0].en = 1  # enabling memory region
    arm.registers.drsrs[0].rsize = 0b00011  # setting region size
    arm.registers.drbars[0] = 0x0F000000  # setting region base address
    arm.registers.dracrs[0].ap = 0b011  # setting access permissions
    arm.registers.mpuir.iregion = 0x01  # declaring the region
    arm.registers.mpuir.dregion = 0x01  # declaring the region
    ram_memory = RAM(0x100)
    ram_memory.write(0, 8, b'\xaa\xbb\xcc\xdd\x11\x22\x33\x44')
    mc = MemoryController(ram_memory, 0x0F000000, 0x0F000100)
    arm.mem.memories.append(mc)
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, LdrexdA1)
    assert opcode.n == 0
    assert opcode.t == 2
    assert opcode.t2 == 3
    arm.registers.set(opcode.n, 0x0F000000)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.t) == 0xDDCCBBAA
    assert arm.registers.get(opcode.t2) == 0x44332211
