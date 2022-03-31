from armulator.armv6.memory_controller_hub import MemoryController
from armulator.armv6.memory_types import RAM
from armulator.armv6.opcodes.concrete.ldrsb_immediate_a1 import LdrsbImmediateA1
from armulator.armv6.opcodes.concrete.ldrsb_immediate_t1 import LdrsbImmediateT1
from armulator.armv6.opcodes.concrete.ldrsb_immediate_t2 import LdrsbImmediateT2
from armulator.armv6.opcodes.concrete.ldrsb_literal_a1 import LdrsbLiteralA1
from armulator.armv6.opcodes.concrete.ldrsb_literal_t1 import LdrsbLiteralT1
from armulator.armv6.opcodes.concrete.ldrsb_register_a1 import LdrsbRegisterA1
from armulator.armv6.opcodes.concrete.ldrsb_register_t1 import LdrsbRegisterT1
from armulator.armv6.opcodes.concrete.ldrsb_register_t2 import LdrsbRegisterT2
from armulator.armv6.shift import SRType


def test_ldrsb_register_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b0101011000001010
    arm.opcode_len = 16
    # setting Data Region registers
    arm.registers.drsrs[0].en = 1  # enabling memory region
    arm.registers.drsrs[0].rsize = 0b00011  # setting region size
    arm.registers.drbars[0] = 0x0F000000  # setting region base address
    arm.registers.dracrs[0].ap = 0b011  # setting access permissions
    arm.registers.mpuir.iregion = 0x01  # declaring the region
    arm.registers.mpuir.dregion = 0x01  # declaring the region
    ram_memory = RAM(0x100)
    ram_memory.write(0x4, 4, b'\x91CIN')
    mc = MemoryController(ram_memory, 0x0F000000, 0x0F000100)
    arm.mem.memories.append(mc)
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == LdrsbRegisterT1
    assert opcode.m == 0
    assert opcode.n == 1
    assert opcode.t == 2
    assert opcode.shift_n == 0
    assert opcode.shift_t == SRType.LSL
    assert opcode.add
    assert opcode.index
    assert not opcode.wback
    arm.registers.set(opcode.n, 0x0F000000)
    arm.registers.set(opcode.m, 4)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.t) == 0xffffff91


def test_ldrsb_register_t2(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11111001000100010010000000000000
    arm.opcode_len = 32
    # setting Data Region registers
    arm.registers.drsrs[0].en = 1  # enabling memory region
    arm.registers.drsrs[0].rsize = 0b00011  # setting region size
    arm.registers.drbars[0] = 0x0F000000  # setting region base address
    arm.registers.dracrs[0].ap = 0b011  # setting access permissions
    arm.registers.mpuir.iregion = 0x01  # declaring the region
    arm.registers.mpuir.dregion = 0x01  # declaring the region
    ram_memory = RAM(0x100)
    ram_memory.write(0x4, 4, b'\x88\x22\x33\x44')
    mc = MemoryController(ram_memory, 0x0F000000, 0x0F000100)
    arm.mem.memories.append(mc)
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == LdrsbRegisterT2
    assert opcode.m == 0
    assert opcode.n == 1
    assert opcode.t == 2
    assert opcode.shift_n == 0
    assert opcode.shift_t == SRType.LSL
    assert opcode.add
    assert opcode.index
    assert not opcode.wback
    arm.registers.set(opcode.n, 0x0F000000)
    arm.registers.set(opcode.m, 4)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.t) == 0xffffff88


def test_ldrsb_literal_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11111001100111110000000000000100
    arm.opcode_len = 32
    # setting Data Region registers
    arm.registers.drsrs[0].en = 1  # enabling memory region
    arm.registers.drsrs[0].rsize = 0b00011  # setting region size
    arm.registers.drbars[0] = 0x00000000  # setting region base address
    arm.registers.dracrs[0].ap = 0b011  # setting access permissions
    arm.registers.mpuir.iregion = 0x01  # declaring the region
    arm.registers.mpuir.dregion = 0x01  # declaring the region
    arm.mem.get_memory_by_address(4).mem.write(0x8, 4, b'\x88\x22\x33\x44')
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == LdrsbLiteralT1
    assert opcode.imm32 == 4
    assert opcode.t == 0
    assert opcode.add
    arm.emulate_cycle()
    assert arm.registers.get(opcode.t) == 0xffffff88


def test_ldrb_immediate_thumb_t2(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11111001000100010010111100000100
    arm.opcode_len = 32
    # setting Data Region registers
    arm.registers.drsrs[0].en = 1  # enabling memory region
    arm.registers.drsrs[0].rsize = 0b00011  # setting region size
    arm.registers.drbars[0] = 0x0F000000  # setting region base address
    arm.registers.dracrs[0].ap = 0b011  # setting access permissions
    arm.registers.mpuir.iregion = 0x01  # declaring the region
    arm.registers.mpuir.dregion = 0x01  # declaring the region
    ram_memory = RAM(0x100)
    ram_memory.write(0x4, 4, b'\x88\x33\x22\x11')
    mc = MemoryController(ram_memory, 0x0F000000, 0x0F000100)
    arm.mem.memories.append(mc)
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == LdrsbImmediateT2
    assert opcode.imm32 == 4
    assert opcode.n == 1
    assert opcode.t == 2
    assert opcode.add
    assert opcode.wback
    assert opcode.index
    arm.registers.set(opcode.n, 0x0F000000)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.t) == 0xffffff88
    assert arm.registers.get(opcode.n) == 0x0F000004


def test_ldrsb_immediate_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11111001100100000001000000000100
    arm.opcode_len = 32
    # setting Data Region registers
    arm.registers.drsrs[0].en = 1  # enabling memory region
    arm.registers.drsrs[0].rsize = 0b00011  # setting region size
    arm.registers.drbars[0] = 0x0F000000  # setting region base address
    arm.registers.dracrs[0].ap = 0b011  # setting access permissions
    arm.registers.mpuir.iregion = 0x01  # declaring the region
    arm.registers.mpuir.dregion = 0x01  # declaring the region
    ram_memory = RAM(0x100)
    ram_memory.write(0x4, 4, b'\x88\x33\x22\x11')
    mc = MemoryController(ram_memory, 0x0F000000, 0x0F000100)
    arm.mem.memories.append(mc)
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == LdrsbImmediateT1
    assert opcode.imm32 == 4
    assert opcode.n == 0
    assert opcode.t == 1
    assert opcode.add
    assert not opcode.wback
    assert opcode.index
    arm.registers.set(opcode.n, 0x0F000000)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.t) == 0xFFFFFF88


def test_ldrsb_register_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100001100100010010000011010000
    arm.opcode_len = 32
    # setting Data Region registers
    arm.registers.drsrs[0].en = 1  # enabling memory region
    arm.registers.drsrs[0].rsize = 0b00011  # setting region size
    arm.registers.drbars[0] = 0x0F000000  # setting region base address
    arm.registers.dracrs[0].ap = 0b011  # setting access permissions
    arm.registers.mpuir.iregion = 0x01  # declaring the region
    arm.registers.mpuir.dregion = 0x01  # declaring the region
    ram_memory = RAM(0x100)
    ram_memory.write(0x4, 4, b'\x88\x22\x33\x44')
    mc = MemoryController(ram_memory, 0x0F000000, 0x0F000100)
    arm.mem.memories.append(mc)
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, LdrsbRegisterA1)
    assert opcode.m == 0
    assert opcode.n == 1
    assert opcode.t == 2
    assert opcode.shift_n == 0
    assert opcode.shift_t == SRType.LSL
    assert opcode.add
    assert opcode.index
    assert not opcode.wback
    arm.registers.set(opcode.n, 0x0F000000)
    arm.registers.set(opcode.m, 4)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.t) == 0xffffff88


def test_ldrsb_immediate_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100001110100010010000011010100
    arm.opcode_len = 32
    # setting Data Region registers
    arm.registers.drsrs[0].en = 1  # enabling memory region
    arm.registers.drsrs[0].rsize = 0b00011  # setting region size
    arm.registers.drbars[0] = 0x0F000000  # setting region base address
    arm.registers.dracrs[0].ap = 0b011  # setting access permissions
    arm.registers.mpuir.iregion = 0x01  # declaring the region
    arm.registers.mpuir.dregion = 0x01  # declaring the region
    ram_memory = RAM(0x100)
    ram_memory.write(0x4, 4, b'\x88\x33\x22\x11')
    mc = MemoryController(ram_memory, 0x0F000000, 0x0F000100)
    arm.mem.memories.append(mc)
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, LdrsbImmediateA1)
    assert opcode.imm32 == 4
    assert opcode.n == 1
    assert opcode.t == 2
    assert opcode.add
    assert not opcode.wback
    assert opcode.index
    arm.registers.set(opcode.n, 0x0F000000)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.t) == 0xFFFFFF88


def test_ldrsb_literal_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100001110111110010000011010100
    arm.opcode_len = 32
    # setting Data Region registers
    arm.registers.drsrs[0].en = 1  # enabling memory region
    arm.registers.drsrs[0].rsize = 0b00011  # setting region size
    arm.registers.drbars[0] = 0x00000000  # setting region base address
    arm.registers.dracrs[0].ap = 0b011  # setting access permissions
    arm.registers.mpuir.iregion = 0x01  # declaring the region
    arm.registers.mpuir.dregion = 0x01  # declaring the region
    arm.mem.get_memory_by_address(4).mem.write(0xc, 4, b'\x88\x22\x33\x44')
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, LdrsbLiteralA1)
    assert opcode.imm32 == 4
    assert opcode.t == 2
    assert opcode.add
    arm.emulate_cycle()
    assert arm.registers.get(opcode.t) == 0xffffff88
