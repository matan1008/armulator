from armulator.armv6.memory_controller_hub import MemoryController
from armulator.armv6.memory_types import RAM
from armulator.armv6.opcodes.concrete.ldrex_a1 import LdrexA1
from armulator.armv6.opcodes.concrete.ldrex_t1 import LdrexT1


def test_ldrex_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11101000010100100001111100000001
    arm.opcode_len = 32
    # setting Data Region registers
    arm.registers.drsrs[0].en = 1  # enabling memory region
    arm.registers.drsrs[0].rsize = 0b00011  # setting region size
    arm.registers.drbars[0] = 0x0F000000  # setting region base address
    arm.registers.dracrs[0].ap = 0b011  # setting access permissions
    arm.registers.mpuir.iregion = 0x01  # declaring the region
    arm.registers.mpuir.dregion = 0x01  # declaring the region
    ram_memory = RAM(0x100)
    ram_memory.write(0x4, 4, b'\xaa\xbb\xcc\xdd')
    mc = MemoryController(ram_memory, 0x0F000000, 0x0F000100)
    arm.mem.memories.append(mc)
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == LdrexT1
    assert opcode.imm32 == 4
    assert opcode.n == 2
    assert opcode.t == 1
    arm.registers.set(opcode.n, 0x0F000000)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.t) == 0xDDCCBBAA


def test_ldrex_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100001100100000010111110011111
    arm.opcode_len = 32
    # setting Data Region registers
    arm.registers.drsrs[0].en = 1  # enabling memory region
    arm.registers.drsrs[0].rsize = 0b00011  # setting region size
    arm.registers.drbars[0] = 0x0F000000  # setting region base address
    arm.registers.dracrs[0].ap = 0b011  # setting access permissions
    arm.registers.mpuir.iregion = 0x01  # declaring the region
    arm.registers.mpuir.dregion = 0x01  # declaring the region
    ram_memory = RAM(0x100)
    ram_memory.write(0, 4, b'\xaa\xbb\xcc\xdd')
    mc = MemoryController(ram_memory, 0x0F000000, 0x0F000100)
    arm.mem.memories.append(mc)
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, LdrexA1)
    assert opcode.imm32 == 0
    assert opcode.n == 0
    assert opcode.t == 2
    arm.registers.set(opcode.n, 0x0F000000)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.t) == 0xDDCCBBAA
