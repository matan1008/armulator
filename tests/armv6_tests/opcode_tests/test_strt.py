from armulator.armv6.memory_controller_hub import MemoryController
from armulator.armv6.memory_types import RAM
from armulator.armv6.opcodes.concrete.strt_a1 import StrtA1
from armulator.armv6.opcodes.concrete.strt_a2 import StrtA2
from armulator.armv6.opcodes.concrete.strt_t1 import StrtT1


def test_strt_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11111000010000000001111000000000
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
    assert isinstance(opcode, StrtT1)
    assert opcode.m == 0
    assert opcode.imm32 == 0
    assert opcode.n == 0
    assert opcode.t == 1
    assert opcode.add
    assert not opcode.register_form
    assert not opcode.post_index
    arm.registers.set(opcode.n, 0x0F000000)
    arm.registers.set(opcode.t, 0x11223344)
    arm.emulate_cycle()
    assert ram_memory[0, 4] == b'\x44\x33\x22\x11'


def test_strt_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100100101000000001000000000100
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
    assert isinstance(opcode, StrtA1)
    assert opcode.m == 0
    assert opcode.imm32 == 4
    assert opcode.n == 0
    assert opcode.t == 1
    assert opcode.add
    assert not opcode.register_form
    assert opcode.post_index
    arm.registers.set(opcode.n, 0x0F000000)
    arm.registers.set(opcode.t, 0x11223344)
    arm.emulate_cycle()
    assert ram_memory[0, 4] == b'\x44\x33\x22\x11'
    assert arm.registers.get(opcode.n) == 0x0F000004


def test_strt_a2(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100110101000010010000000000000
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
    assert isinstance(opcode, StrtA2)
    assert opcode.m == 0
    assert opcode.imm32 == 0
    assert opcode.n == 1
    assert opcode.t == 2
    assert opcode.add
    assert opcode.register_form
    assert opcode.post_index
    arm.registers.set(opcode.n, 0x0F000000)
    arm.registers.set(opcode.m, 4)
    arm.registers.set(opcode.t, 0x11223344)
    arm.emulate_cycle()
    assert ram_memory[0, 4] == b'\x44\x33\x22\x11'
    assert arm.registers.get(opcode.n) == 0x0F000004
