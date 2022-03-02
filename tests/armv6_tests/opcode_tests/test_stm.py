import struct

from armulator.armv6.memory_controller_hub import MemoryController
from armulator.armv6.memory_types import RAM
from armulator.armv6.opcodes.concrete.stm_a1 import StmA1
from armulator.armv6.opcodes.concrete.stm_t1 import StmT1
from armulator.armv6.opcodes.concrete.stm_t2 import StmT2
from armulator.armv6.opcodes.concrete.stm_user_registers_a1 import StmUserRegistersA1


def test_stm_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b1100000100100100
    arm.opcode_len = 16
    arm.registers.drsrs[0].en = 1  # enabling memory region
    arm.registers.drsrs[0].rsize = 0b01000  # setting region size
    arm.registers.drbars[0] = 0x0F000000  # setting region base address
    arm.registers.dracrs[0].ap = 0b011  # setting access permissions
    arm.registers.mpuir.iregion = 0x01  # declaring the region
    arm.registers.mpuir.dregion = 0x01  # declaring the region
    ram_memory = RAM(0x100)
    mc = MemoryController(ram_memory, 0x0F000000, 0x0F000100)
    arm.mem.memories.append(mc)
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, StmT1)
    assert opcode.wback
    assert opcode.n == 1
    assert opcode.registers == 0b0000000000100100
    arm.registers.set(opcode.n, 0x0F000004)
    arm.registers.set(2, struct.unpack('>I', b'YREV')[0])
    arm.registers.set(5, struct.unpack('>I', b'ECIN')[0])
    arm.emulate_cycle()
    assert ram_memory[4, 8] == b'VERYNICE'
    assert arm.registers.get(opcode.n) == 0x0F00000C


def test_stm_t2(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11101000101000010100000000100100
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
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, StmT2)
    assert opcode.wback
    assert opcode.n == 1
    assert opcode.registers == 0b0100000000100100
    arm.registers.set(opcode.n, 0x0F000004)
    arm.registers.set(2, struct.unpack('>I', b'YREV')[0])
    arm.registers.set(5, struct.unpack('>I', b'ECIN')[0])
    arm.registers.set_lr(0xAABBCCDD)
    arm.emulate_cycle()
    assert ram_memory[4, 12] == b'VERYNICE\xDD\xCC\xBB\xAA'
    assert arm.registers.get(opcode.n) == 0x0F000010


def test_stm_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11101000101000010100000000100100
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
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, StmA1)
    assert opcode.wback
    assert opcode.n == 1
    assert opcode.registers == 0b0100000000100100
    arm.registers.set(opcode.n, 0x0F000004)
    arm.registers.set(2, 0x11223344)
    arm.registers.set(5, 0x55667788)
    arm.registers.set_lr(0xAABBCCDD)
    arm.emulate_cycle()
    assert ram_memory[4, 12] == b'\x44\x33\x22\x11\x88\x77\x66\x55\xDD\xCC\xBB\xAA'
    assert arm.registers.get(opcode.n) == 0x0F000010


def test_stm_user_registers_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11101001110000010100000000100100
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
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, StmUserRegistersA1)
    assert opcode.increment
    assert opcode.word_higher
    assert opcode.n == 1
    assert opcode.registers == 0b0100000000100100
    arm.registers.cpsr.m = 0b10000
    arm.registers.set(opcode.n, 0x0F000000)
    arm.registers.set(2, 0x11223344)
    arm.registers.set(5, 0x55667788)
    arm.registers.set_lr(0xAABBCCDD)
    arm.registers.cpsr.m = 0b10011
    arm.emulate_cycle()
    assert ram_memory[4, 12] == b'\x44\x33\x22\x11\x88\x77\x66\x55\xDD\xCC\xBB\xAA'
