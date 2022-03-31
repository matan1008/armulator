import struct

from armulator.armv6.memory_controller_hub import MemoryController
from armulator.armv6.memory_types import RAM
from armulator.armv6.opcodes.concrete.ldr_immediate_arm_a1 import LdrImmediateArmA1
from armulator.armv6.opcodes.concrete.ldr_immediate_thumb_t1 import LdrImmediateThumbT1
from armulator.armv6.opcodes.concrete.ldr_immediate_thumb_t2 import LdrImmediateThumbT2
from armulator.armv6.opcodes.concrete.ldr_immediate_thumb_t3 import LdrImmediateThumbT3
from armulator.armv6.opcodes.concrete.ldr_immediate_thumb_t4 import LdrImmediateThumbT4
from armulator.armv6.opcodes.concrete.ldr_literal_a1 import LdrLiteralA1
from armulator.armv6.opcodes.concrete.ldr_literal_t1 import LdrLiteralT1
from armulator.armv6.opcodes.concrete.ldr_literal_t2 import LdrLiteralT2
from armulator.armv6.opcodes.concrete.ldr_register_arm_a1 import LdrRegisterArmA1
from armulator.armv6.opcodes.concrete.ldr_register_thumb_t1 import LdrRegisterThumbT1
from armulator.armv6.opcodes.concrete.ldr_register_thumb_t2 import LdrRegisterThumbT2
from armulator.armv6.shift import SRType


def test_ldr_literal_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b0100100000000001
    arm.opcode_len = 16
    arm.mem.get_memory_by_address(4).mem.write(0x8, 4, b'ECIN')
    # setting Data Region registers
    arm.registers.drsrs[0].en = 1  # enabling memory region
    arm.registers.drsrs[0].rsize = 0b00011  # setting region size
    arm.registers.drbars[0] = 0x00000000  # setting region base address
    arm.registers.dracrs[0].ap = 0b011  # setting access permissions
    arm.registers.mpuir.iregion = 0x01  # declaring the region
    arm.registers.mpuir.dregion = 0x01  # declaring the region
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == LdrLiteralT1
    assert opcode.imm32 == 4
    assert opcode.add
    assert opcode.t == 0
    arm.emulate_cycle()
    assert arm.registers.get(opcode.t) == struct.unpack('>I', b'NICE')[0]


def test_ldr_register_thumb_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b0101100000001010
    arm.opcode_len = 16
    # setting Data Region registers
    arm.registers.drsrs[0].en = 1  # enabling memory region
    arm.registers.drsrs[0].rsize = 0b00011  # setting region size
    arm.registers.drbars[0] = 0x0F000000  # setting region base address
    arm.registers.dracrs[0].ap = 0b011  # setting access permissions
    arm.registers.mpuir.iregion = 0x01  # declaring the region
    arm.registers.mpuir.dregion = 0x01  # declaring the region
    ram_memory = RAM(0x100)
    ram_memory.write(0x4, 4, b'ECIN')
    mc = MemoryController(ram_memory, 0x0F000000, 0x0F000100)
    arm.mem.memories.append(mc)
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == LdrRegisterThumbT1
    assert opcode.m == 0
    assert opcode.n == 1
    assert opcode.t == 2
    assert opcode.shift_n == 0
    assert opcode.shift_t == SRType.LSL
    arm.registers.set(opcode.n, 0x0F000000)
    arm.registers.set(opcode.m, 4)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.t) == struct.unpack('>I', b'NICE')[0]


def test_ldr_immediate_thumb_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b0110100001001010
    arm.opcode_len = 16
    # setting Data Region registers
    arm.registers.drsrs[0].en = 1  # enabling memory region
    arm.registers.drsrs[0].rsize = 0b00011  # setting region size
    arm.registers.drbars[0] = 0x0F000000  # setting region base address
    arm.registers.dracrs[0].ap = 0b011  # setting access permissions
    arm.registers.mpuir.iregion = 0x01  # declaring the region
    arm.registers.mpuir.dregion = 0x01  # declaring the region
    ram_memory = RAM(0x100)
    ram_memory.write(0x4, 4, b'ECIN')
    mc = MemoryController(ram_memory, 0x0F000000, 0x0F000100)
    arm.mem.memories.append(mc)
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == LdrImmediateThumbT1
    assert opcode.imm32 == 4
    assert opcode.n == 1
    assert opcode.t == 2
    assert opcode.add
    assert not opcode.wback
    assert opcode.index
    arm.registers.set(opcode.n, 0x0F000000)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.t) == struct.unpack('>I', b'NICE')[0]


def test_ldr_immediate_thumb_t2(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b1001100000000001
    arm.opcode_len = 16
    # setting Data Region registers
    arm.registers.drsrs[0].en = 1  # enabling memory region
    arm.registers.drsrs[0].rsize = 0b00011  # setting region size
    arm.registers.drbars[0] = 0x0F000000  # setting region base address
    arm.registers.dracrs[0].ap = 0b011  # setting access permissions
    arm.registers.mpuir.iregion = 0x01  # declaring the region
    arm.registers.mpuir.dregion = 0x01  # declaring the region
    ram_memory = RAM(0x100)
    ram_memory.write(0x4, 4, b'ECIN')
    mc = MemoryController(ram_memory, 0x0F000000, 0x0F000100)
    arm.mem.memories.append(mc)
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == LdrImmediateThumbT2
    assert opcode.imm32 == 4
    assert opcode.n == 13
    assert opcode.t == 0
    assert opcode.add
    assert not opcode.wback
    assert opcode.index
    arm.registers.set(opcode.n, 0x0F000000)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.t) == struct.unpack('>I', b'NICE')[0]


def test_ldr_register_thumb_t2(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11111000010100010010000000000000
    arm.opcode_len = 32
    # setting Data Region registers
    arm.registers.drsrs[0].en = 1  # enabling memory region
    arm.registers.drsrs[0].rsize = 0b00011  # setting region size
    arm.registers.drbars[0] = 0x0F000000  # setting region base address
    arm.registers.dracrs[0].ap = 0b011  # setting access permissions
    arm.registers.mpuir.iregion = 0x01  # declaring the region
    arm.registers.mpuir.dregion = 0x01  # declaring the region
    ram_memory = RAM(0x100)
    ram_memory.write(0x4, 4, b'\x11\x22\x33\x44')
    mc = MemoryController(ram_memory, 0x0F000000, 0x0F000100)
    arm.mem.memories.append(mc)
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == LdrRegisterThumbT2
    assert opcode.m == 0
    assert opcode.n == 1
    assert opcode.t == 2
    assert opcode.shift_n == 0
    assert opcode.shift_t == SRType.LSL
    arm.registers.set(opcode.n, 0x0F000000)
    arm.registers.set(opcode.m, 4)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.t) == 0x44332211


def test_ldr_immediate_thumb_t4(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11111000010100000001100100000000
    arm.opcode_len = 32
    # setting Data Region registers
    arm.registers.drsrs[0].en = 1  # enabling memory region
    arm.registers.drsrs[0].rsize = 0b00011  # setting region size
    arm.registers.drbars[0] = 0x0F000000  # setting region base address
    arm.registers.dracrs[0].ap = 0b011  # setting access permissions
    arm.registers.mpuir.iregion = 0x01  # declaring the region
    arm.registers.mpuir.dregion = 0x01  # declaring the region
    ram_memory = RAM(0x100)
    ram_memory.write(0x0, 4, b'\x44\x33\x22\x11')
    mc = MemoryController(ram_memory, 0x0F000000, 0x0F000100)
    arm.mem.memories.append(mc)
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == LdrImmediateThumbT4
    assert opcode.imm32 == 0
    assert opcode.n == 0
    assert opcode.t == 1
    assert not opcode.add
    assert opcode.wback
    assert not opcode.index
    arm.registers.set(opcode.n, 0x0F000000)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.t) == 0x11223344
    assert arm.registers.get(opcode.n) == 0x0F000000


def test_ldr_immediate_thumb_t3(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11111000110100000001000000000000
    arm.opcode_len = 32
    # setting Data Region registers
    arm.registers.drsrs[0].en = 1  # enabling memory region
    arm.registers.drsrs[0].rsize = 0b00011  # setting region size
    arm.registers.drbars[0] = 0x0F000000  # setting region base address
    arm.registers.dracrs[0].ap = 0b011  # setting access permissions
    arm.registers.mpuir.iregion = 0x01  # declaring the region
    arm.registers.mpuir.dregion = 0x01  # declaring the region
    ram_memory = RAM(0x100)
    ram_memory.write(0x0, 4, b'\x44\x33\x22\x11')
    mc = MemoryController(ram_memory, 0x0F000000, 0x0F000100)
    arm.mem.memories.append(mc)
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == LdrImmediateThumbT3
    assert opcode.imm32 == 0
    assert opcode.n == 0
    assert opcode.t == 1
    assert opcode.add
    assert not opcode.wback
    assert opcode.index
    arm.registers.set(opcode.n, 0x0F000000)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.t) == 0x11223344


def test_ldr_literal_t2(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11111000110111110000000000000100
    arm.opcode_len = 32
    # setting Data Region registers
    arm.registers.drsrs[0].en = 1  # enabling memory region
    arm.registers.drsrs[0].rsize = 0b00011  # setting region size
    arm.registers.drbars[0] = 0x00000000  # setting region base address
    arm.registers.dracrs[0].ap = 0b011  # setting access permissions
    arm.registers.mpuir.iregion = 0x01  # declaring the region
    arm.registers.mpuir.dregion = 0x01  # declaring the region
    arm.mem.get_memory_by_address(4).mem.write(0x8, 4, b'\x11\x22\x33\x44')
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == LdrLiteralT2
    assert opcode.imm32 == 4
    assert opcode.add
    assert opcode.t == 0
    arm.emulate_cycle()
    assert arm.registers.get(opcode.t) == 0x44332211


def test_ldr_immediate_arm_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100101100100000001000000000000
    arm.opcode_len = 32
    # setting Data Region registers
    arm.registers.drsrs[0].en = 1  # enabling memory region
    arm.registers.drsrs[0].rsize = 0b00011  # setting region size
    arm.registers.drbars[0] = 0x0F000000  # setting region base address
    arm.registers.dracrs[0].ap = 0b011  # setting access permissions
    arm.registers.mpuir.iregion = 0x01  # declaring the region
    arm.registers.mpuir.dregion = 0x01  # declaring the region
    ram_memory = RAM(0x100)
    ram_memory.write(0x0, 4, b'\x44\x33\x22\x11')
    mc = MemoryController(ram_memory, 0x0F000000, 0x0F000100)
    arm.mem.memories.append(mc)
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, LdrImmediateArmA1)
    assert opcode.imm32 == 0
    assert opcode.n == 0
    assert opcode.t == 1
    assert opcode.add
    assert not opcode.wback
    assert opcode.index
    arm.registers.set(opcode.n, 0x0F000000)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.t) == 0x11223344


def test_ldr_literal_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100101100111110000000000000100
    arm.opcode_len = 32
    # setting Data Region registers
    arm.registers.drsrs[0].en = 1  # enabling memory region
    arm.registers.drsrs[0].rsize = 0b00011  # setting region size
    arm.registers.drbars[0] = 0x00000000  # setting region base address
    arm.registers.dracrs[0].ap = 0b011  # setting access permissions
    arm.registers.mpuir.iregion = 0x01  # declaring the region
    arm.registers.mpuir.dregion = 0x01  # declaring the region
    arm.mem.get_memory_by_address(4).mem.write(0xC, 4, b'\x11\x22\x33\x44')
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, LdrLiteralA1)
    assert opcode.imm32 == 4
    assert opcode.add
    assert opcode.t == 0
    arm.emulate_cycle()
    assert arm.registers.get(opcode.t) == 0x44332211


def test_ldr_register_arm_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100111100100010010000000000000
    arm.opcode_len = 32
    # setting Data Region registers
    arm.registers.drsrs[0].en = 1  # enabling memory region
    arm.registers.drsrs[0].rsize = 0b00011  # setting region size
    arm.registers.drbars[0] = 0x0F000000  # setting region base address
    arm.registers.dracrs[0].ap = 0b011  # setting access permissions
    arm.registers.mpuir.iregion = 0x01  # declaring the region
    arm.registers.mpuir.dregion = 0x01  # declaring the region
    ram_memory = RAM(0x100)
    ram_memory.write(0x4, 4, b'\x11\x22\x33\x44')
    mc = MemoryController(ram_memory, 0x0F000000, 0x0F000100)
    arm.mem.memories.append(mc)
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, LdrRegisterArmA1)
    assert opcode.m == 0
    assert opcode.n == 1
    assert opcode.t == 2
    assert opcode.shift_n == 0
    assert opcode.shift_t == SRType.LSL
    assert opcode.add
    assert not opcode.wback
    assert opcode.index
    arm.registers.set(opcode.n, 0x0F000000)
    arm.registers.set(opcode.m, 4)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.t) == 0x44332211
