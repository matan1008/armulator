import pytest

from armulator.armv6.memory_controller_hub import MemoryController
from armulator.armv6.memory_types import RAM
from armulator.armv6.opcodes.concrete.strd_immediate_a1 import StrdImmediateA1
from armulator.armv6.opcodes.concrete.strd_immediate_t1 import StrdImmediateT1
from armulator.armv6.opcodes.concrete.strd_register_a1 import StrdRegisterA1


@pytest.mark.parametrize('instruction, index, mem_offset', [
    (0b11101000111000000001001000000001, 0, 0),
    (0b11101001111000000001001000000001, 1, 4),
])
def test_strd_immediate_t1(thumb_v6_without_fetch, instruction, index, mem_offset):
    arm = thumb_v6_without_fetch
    arm.opcode = instruction
    arm.opcode_len = 32
    # setting Data Region registers
    arm.registers.drsrs[0].en = 1  # enabling memory region
    arm.registers.drsrs[0].rsize = 0b00011  # setting region size
    arm.registers.drbars[0] = 0x0F000000  # setting region base address
    arm.registers.dracrs[0].ap = 0b011  # setting access permissions
    arm.registers.mpuir.iregion = 0x01  # declaring the region
    arm.registers.mpuir.dregion = 0x01  # declaring the region
    ram_memory = RAM(0x100)
    mc = MemoryController(ram_memory, 0x0F000000, 0x0F000100)
    arm.mem.memories.append(mc)
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == StrdImmediateT1
    assert opcode.wback
    assert opcode.n == 0
    assert opcode.index == index
    assert opcode.add
    assert opcode.imm32 == 4
    assert opcode.t == 1
    assert opcode.t2 == 2
    arm.registers.set(opcode.n, 0x0F000000)
    arm.registers.set(opcode.t, 0x11223344)
    arm.registers.set(opcode.t2, 0x55667788)
    arm.emulate_cycle()
    assert ram_memory[mem_offset, 8] == b'\x44\x33\x22\x11\x88\x77\x66\x55'
    assert arm.registers.get(opcode.n) == 0x0F000004


def test_strd_register_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100001101000010010000011110000
    arm.opcode_len = 32
    # setting Data Region registers
    arm.registers.drsrs[0].en = 1  # enabling memory region
    arm.registers.drsrs[0].rsize = 0b00011  # setting region size
    arm.registers.drbars[0] = 0x0F000000  # setting region base address
    arm.registers.dracrs[0].ap = 0b011  # setting access permissions
    arm.registers.mpuir.iregion = 0x01  # declaring the region
    arm.registers.mpuir.dregion = 0x01  # declaring the region
    ram_memory = RAM(0x100)
    mc = MemoryController(ram_memory, 0x0F000000, 0x0F000100)
    arm.mem.memories.append(mc)
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, StrdRegisterA1)
    assert opcode.wback
    assert opcode.n == 1
    assert opcode.index
    assert opcode.add
    assert opcode.m == 0
    assert opcode.t == 2
    assert opcode.t2 == 3
    arm.registers.set(opcode.n, 0x0F000000)
    arm.registers.set(opcode.m, 4)
    arm.registers.set(opcode.t, 0x11223344)
    arm.registers.set(opcode.t2, 0x55667788)
    arm.emulate_cycle()
    assert ram_memory[4, 8] == b'\x44\x33\x22\x11\x88\x77\x66\x55'
    assert arm.registers.get(opcode.n) == 0x0F000004


def test_strd_immediate_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    instr = 0b11100001110011010000000011110000  # Store double to SP
    arm.opcode_len = 32
    arm.registers.drsrs[0].en = 1  # enabling memory region
    arm.registers.drsrs[0].rsize = 0b01000  # setting region size
    arm.registers.drbars[0] = 0x0F000000  # setting region base address
    arm.registers.dracrs[0].ap = 0b011  # setting access permissions
    arm.registers.mpuir.iregion = 0x01  # declaring the region
    arm.registers.mpuir.dregion = 0x01  # declaring the region
    ram_memory = RAM(0x100)
    mc = MemoryController(ram_memory, 0x0F000000, 0x0F000100)
    arm.mem.memories.append(mc)
    arm.opcode = instr
    opcode = arm.decode_instruction(instr)
    opcode = opcode.from_bitarray(instr, arm)
    assert isinstance(opcode, StrdImmediateA1)
    assert not opcode.wback
    assert opcode.n == 13
    assert opcode.index
    assert opcode.add
    assert opcode.imm32 == 0
    assert opcode.t == 0
    assert opcode.t2 == 1
    arm.registers.set(opcode.n, 0x0F000004)
    arm.registers.set(opcode.t, 0x11223344)
    arm.registers.set(opcode.t2, 0x55667788)
    arm.emulate_cycle()
    assert ram_memory[4, 8] == b'\x44\x33\x22\x11\x88\x77\x66\x55'
