import struct

from armulator.armv6.memory_controller_hub import MemoryController
from armulator.armv6.memory_types import RAM
from armulator.armv6.opcodes.concrete.pop_arm_a1 import PopArmA1
from armulator.armv6.opcodes.concrete.pop_arm_a2 import PopArmA2
from armulator.armv6.opcodes.concrete.pop_thumb_t1 import PopThumbT1
from armulator.armv6.opcodes.concrete.pop_thumb_t2 import PopThumbT2
from armulator.armv6.opcodes.concrete.pop_thumb_t3 import PopThumbT3


def test_pop_thumb_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b1011110100000001
    arm.opcode_len = 16
    arm.registers.drsrs[0].en = 1  # enabling memory region
    arm.registers.drsrs[0].rsize = 0b01000  # setting region size
    arm.registers.drbars[0] = 0x0F000000  # setting region base address
    arm.registers.dracrs[0].ap = 0b011  # setting access permissions
    arm.registers.mpuir.iregion = 0x01  # declaring the region
    arm.registers.mpuir.dregion = 0x01  # declaring the region
    ram_memory = RAM(0x100)
    ram_memory.write(0x0, 8, b'VERY\xffICE')
    mc = MemoryController(ram_memory, 0x0F000000, 0x0F000100)
    arm.mem.memories.append(mc)
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, PopThumbT1)
    assert opcode.registers == 0b1000000000000001
    assert not opcode.unaligned_allowed
    arm.registers.set_sp(0x0F000000)
    arm.emulate_cycle()
    assert arm.registers.get_sp() == 0x0F000008
    assert arm.registers.get(0) == struct.unpack('>I', b'YREV')[0]
    assert arm.registers.get_pc() == struct.unpack('>I', b'ECI\xfe')[0] + 4


def test_pop_thumb_t2(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11101000101111011000000000000001
    arm.opcode_len = 32
    arm.registers.drsrs[0].en = 1  # enabling memory region
    arm.registers.drsrs[0].rsize = 0b01000  # setting region size
    arm.registers.drbars[0] = 0x0F000000  # setting region base address
    arm.registers.dracrs[0].ap = 0b011  # setting access permissions
    arm.registers.mpuir.iregion = 0x01  # declaring the region
    arm.registers.mpuir.dregion = 0x01  # declaring the region
    ram_memory = RAM(0x100)
    ram_memory.write(0x0, 8, b'VERY\xffICE')
    mc = MemoryController(ram_memory, 0x0F000000, 0x0F000100)
    arm.mem.memories.append(mc)
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, PopThumbT2)
    assert opcode.registers == 0b1000000000000001
    assert not opcode.unaligned_allowed
    arm.registers.set_sp(0x0F000000)
    arm.emulate_cycle()
    assert arm.registers.get_sp() == 0x0F000008
    assert arm.registers.get(0) == struct.unpack('>I', b'YREV')[0]
    assert arm.registers.get_pc() == struct.unpack('>I', b'ECI\xfe')[0] + 4


def test_pop_thumb_t3(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11111000010111010000101100000100
    arm.opcode_len = 32
    arm.registers.drsrs[0].en = 1  # enabling memory region
    arm.registers.drsrs[0].rsize = 0b01000  # setting region size
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
    assert isinstance(opcode, PopThumbT3)
    assert opcode.registers == 0b0000000000000001
    assert opcode.unaligned_allowed
    arm.registers.set_sp(0x0F000000)
    arm.emulate_cycle()
    assert arm.registers.get_sp() == 0x0F000004
    assert arm.registers.get(0) == 0x11223344


def test_pop_arm_a2(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100100100111010000000000000100
    arm.opcode_len = 32
    arm.registers.drsrs[0].en = 1  # enabling memory region
    arm.registers.drsrs[0].rsize = 0b01000  # setting region size
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
    assert isinstance(opcode, PopArmA2)
    assert opcode.registers == 0b0000000000000001
    assert opcode.unaligned_allowed
    arm.registers.set_sp(0x0F000000)
    arm.emulate_cycle()
    assert arm.registers.get_sp() == 0x0F000004
    assert arm.registers.get(0) == 0x11223344


def test_pop_arm_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11101000101111011000000000000001
    arm.opcode_len = 32
    arm.registers.drsrs[0].en = 1  # enabling memory region
    arm.registers.drsrs[0].rsize = 0b01000  # setting region size
    arm.registers.drbars[0] = 0x0F000000  # setting region base address
    arm.registers.dracrs[0].ap = 0b011  # setting access permissions
    arm.registers.mpuir.iregion = 0x01  # declaring the region
    arm.registers.mpuir.dregion = 0x01  # declaring the region
    ram_memory = RAM(0x100)
    ram_memory.write(0x0, 8, b'\x11\x22\x33\x44\x55\x66\x77\x88')
    mc = MemoryController(ram_memory, 0x0F000000, 0x0F000100)
    arm.mem.memories.append(mc)
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, PopArmA1)
    assert opcode.registers == 0b1000000000000001
    assert not opcode.unaligned_allowed
    arm.registers.set_sp(0x0F000000)
    arm.emulate_cycle()
    assert arm.registers.get_sp() == 0x0F000008
    assert arm.registers.get(0) == 0x44332211
    assert arm.registers.get_pc() == 0x88776658
