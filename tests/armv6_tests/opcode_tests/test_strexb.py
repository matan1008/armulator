from armulator.armv6.memory_controller_hub import MemoryController
from armulator.armv6.memory_types import RAM
from armulator.armv6.opcodes.concrete.strexb_a1 import StrexbA1
from armulator.armv6.opcodes.concrete.strexb_t1 import StrexbT1


def test_strexb_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11101000110000100001000001000000
    arm.opcode_len = 32
    # setting Data Region registers
    arm.registers.drsrs[0].en = 1  # enabling memory region
    arm.registers.drsrs[0].rsize = 0b00010  # setting region size
    arm.registers.drbars[0] = 0x0F000000  # setting region base address
    arm.registers.dracrs[0].ap = 0b011  # setting access permissions
    arm.registers.mpuir.iregion = 0x01  # declaring the region
    arm.registers.mpuir.dregion = 0x01  # declaring the region
    ram_memory = RAM(0x100)
    mc = MemoryController(ram_memory, 0x0F000000, 0x0F000100)
    arm.mem.memories.append(mc)
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == StrexbT1
    assert opcode.d == 0
    assert opcode.n == 2
    assert opcode.t == 1
    arm.registers.set(opcode.n, 0x0F000000)
    arm.registers.set(opcode.t, 0xAABBCCDD)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 1
    assert ram_memory[4, 4] == b'\x00\x00\x00\x00'


def test_strexb_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100001110000000010111110010001
    arm.opcode_len = 32
    # setting Data Region registers
    arm.registers.drsrs[0].en = 1  # enabling memory region
    arm.registers.drsrs[0].rsize = 0b00010  # setting region size
    arm.registers.drbars[0] = 0x0F000000  # setting region base address
    arm.registers.dracrs[0].ap = 0b011  # setting access permissions
    arm.registers.mpuir.iregion = 0x01  # declaring the region
    arm.registers.mpuir.dregion = 0x01  # declaring the region
    ram_memory = RAM(0x100)
    mc = MemoryController(ram_memory, 0x0F000000, 0x0F000100)
    arm.mem.memories.append(mc)
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, StrexbA1)
    assert opcode.d == 2
    assert opcode.n == 0
    assert opcode.t == 1
    arm.registers.set(opcode.n, 0x0F000000)
    arm.registers.set(opcode.t, 0xAABBCCDD)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 1
    assert ram_memory[0, 4] == b'\x00\x00\x00\x00'
