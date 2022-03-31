import pytest

from armulator.armv6.memory_controller_hub import MemoryController
from armulator.armv6.memory_types import RAM
from armulator.armv6.opcodes.concrete.ldrd_immediate_a1 import LdrdImmediateA1
from armulator.armv6.opcodes.concrete.ldrd_immediate_t1 import LdrdImmediateT1
from armulator.armv6.opcodes.concrete.ldrd_literal_a1 import LdrdLiteralA1
from armulator.armv6.opcodes.concrete.ldrd_literal_t1 import LdrdLiteralT1
from armulator.armv6.opcodes.concrete.ldrd_register_a1 import LdrdRegisterA1


@pytest.mark.parametrize('instruction, index, mem_offset', [
    (0b11101000111100000001001000000001, 0, 0),
    (0b11101001111100000001001000000001, 1, 4),
])
def test_ldrd_immediate_t1(thumb_v6_without_fetch, instruction, index, mem_offset):
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
    ram_memory.write(mem_offset, 8, b'\x44\x33\x22\x11\x88\x77\x66\x55')
    mc = MemoryController(ram_memory, 0x0F000000, 0x0F000100)
    arm.mem.memories.append(mc)
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == LdrdImmediateT1
    assert opcode.wback
    assert opcode.n == 0
    assert opcode.index == index
    assert opcode.add
    assert opcode.imm32 == 4
    assert opcode.t == 1
    assert opcode.t2 == 2
    arm.registers.set(opcode.n, 0x0F000000)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.t) == 0x11223344
    assert arm.registers.get(opcode.t2) == 0x55667788
    assert arm.registers.get(opcode.n) == 0x0F000004


def test_ldrd_literal_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11101001110111110001001000000001
    arm.opcode_len = 32
    # setting Data Region registers
    arm.registers.drsrs[0].en = 1  # enabling memory region
    arm.registers.drsrs[0].rsize = 0b00100  # setting region size
    arm.registers.drbars[0] = 0x00000000  # setting region base address
    arm.registers.dracrs[0].ap = 0b011  # setting access permissions
    arm.registers.mpuir.iregion = 0x01  # declaring the region
    arm.registers.mpuir.dregion = 0x01  # declaring the region
    arm.mem.get_memory_by_address(4).mem.write(8, 8, b'\x44\x33\x22\x11\x88\x77\x66\x55')
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == LdrdLiteralT1
    assert opcode.add
    assert opcode.imm32 == 4
    assert opcode.t == 1
    assert opcode.t2 == 2
    arm.emulate_cycle()
    assert arm.registers.get(opcode.t) == 0x11223344
    assert arm.registers.get(opcode.t2) == 0x55667788


@pytest.mark.parametrize('instruction, index, mem_offset', [
    (0b11100000100000010010000011010000, 0, 0),
    (0b11100001101000010010000011010000, 1, 4),
])
def test_ldrd_register_a1(arm_v6_without_fetch, instruction, index, mem_offset):
    arm = arm_v6_without_fetch
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
    ram_memory.write(mem_offset, 8, b'\x44\x33\x22\x11\x88\x77\x66\x55')
    mc = MemoryController(ram_memory, 0x0F000000, 0x0F000100)
    arm.mem.memories.append(mc)
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, LdrdRegisterA1)
    assert opcode.wback
    assert opcode.n == 1
    assert opcode.index == index
    assert opcode.add
    assert opcode.m == 0
    assert opcode.t == 2
    assert opcode.t2 == 3
    arm.registers.set(opcode.n, 0x0F000000)
    arm.registers.set(opcode.m, 4)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.t) == 0x11223344
    assert arm.registers.get(opcode.t2) == 0x55667788
    assert arm.registers.get(opcode.n) == 0x0F000004


@pytest.mark.parametrize('instruction, index, mem_offset', [
    (0b11100000110000010010000011010100, 0, 0),
    (0b11100001111000010010000011010100, 1, 4),
])
def test_ldrd_immediate_a1(arm_v6_without_fetch, instruction, index, mem_offset):
    arm = arm_v6_without_fetch
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
    ram_memory.write(mem_offset, 8, b'\x44\x33\x22\x11\x88\x77\x66\x55')
    mc = MemoryController(ram_memory, 0x0F000000, 0x0F000100)
    arm.mem.memories.append(mc)
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, LdrdImmediateA1)
    assert opcode.wback
    assert opcode.n == 1
    assert opcode.index == index
    assert opcode.add
    assert opcode.imm32 == 4
    assert opcode.t == 2
    assert opcode.t2 == 3
    arm.registers.set(opcode.n, 0x0F000000)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.t) == 0x11223344
    assert arm.registers.get(opcode.t2) == 0x55667788
    assert arm.registers.get(opcode.n) == 0x0F000004


def test_ldrd_literal_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100001110011110010000011010100
    arm.opcode_len = 32
    # setting Data Region registers
    arm.registers.drsrs[0].en = 1  # enabling memory region
    arm.registers.drsrs[0].rsize = 0b00100  # setting region size
    arm.registers.drbars[0] = 0x00000000  # setting region base address
    arm.registers.dracrs[0].ap = 0b011  # setting access permissions
    arm.registers.mpuir.iregion = 0x01  # declaring the region
    arm.registers.mpuir.dregion = 0x01  # declaring the region
    arm.mem.get_memory_by_address(4).mem.write(0xC, 8, b'\x44\x33\x22\x11\x88\x77\x66\x55')
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, LdrdLiteralA1)
    assert opcode.add
    assert opcode.imm32 == 4
    assert opcode.t == 2
    assert opcode.t2 == 3
    arm.emulate_cycle()
    assert arm.registers.get(opcode.t) == 0x11223344
    assert arm.registers.get(opcode.t2) == 0x55667788
