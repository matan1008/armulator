from armulator.armv6.memory_controller_hub import MemoryController
from armulator.armv6.memory_types import RAM
from armulator.armv6.opcodes.concrete.strbt_a1 import StrbtA1
from armulator.armv6.opcodes.concrete.strbt_a2 import StrbtA2
from armulator.armv6.opcodes.concrete.strbt_t1 import StrbtT1
from armulator.armv6.shift import SRType


def test_strbt_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11111000000000000001111000000000
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
    assert isinstance(opcode, StrbtT1)
    assert opcode.m == 0
    assert opcode.imm32 == 0
    assert opcode.n == 0
    assert opcode.t == 1
    assert opcode.shift_n == 0
    assert opcode.shift_t == SRType.LSL
    assert opcode.add
    assert not opcode.register_form
    assert not opcode.post_index
    arm.registers.set(opcode.n, 0x0F000000)
    arm.registers.set(opcode.t, 0x11223344)
    arm.emulate_cycle()
    assert ram_memory[0, 4] == b'\x44\x00\x00\x00'


def test_strbt_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100100111000000001000000000100
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
    assert isinstance(opcode, StrbtA1)
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
    assert ram_memory[0, 4] == b'\x44\x00\x00\x00'
    assert arm.registers.get(opcode.n) == 0x0F000004


def test_strbt_a2(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100110111000010010000000000000
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
    assert isinstance(opcode, StrbtA2)
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
    assert ram_memory[0, 4] == b'\x44\x00\x00\x00'
    assert arm.registers.get(opcode.n) == 0x0F000004
