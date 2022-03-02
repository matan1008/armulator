from armulator.armv6.memory_controller_hub import MemoryController
from armulator.armv6.memory_types import RAM
from armulator.armv6.opcodes.concrete.rfe_a1 import RfeA1
from armulator.armv6.opcodes.concrete.rfe_t1 import RfeT1
from armulator.armv6.opcodes.concrete.rfe_t2 import RfeT2


def test_rfe_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11101000000100001100000000000000
    arm.opcode_len = 32
    # setting Data Region registers
    arm.registers.drsrs[0].en = 1  # enabling memory region
    arm.registers.drsrs[0].rsize = 0b00010  # setting region size
    arm.registers.drbars[0] = 0x0F000000  # setting region base address
    arm.registers.dracrs[0].ap = 0b011  # setting access permissions
    arm.registers.mpuir.iregion = 0x01  # declaring the region
    arm.registers.mpuir.dregion = 0x01  # declaring the region
    ram_memory = RAM(0x100)
    ram_memory[0, 8] = b'\xDD\xcc\xbb\xaa\xf2\x33\x22\x11'
    mc = MemoryController(ram_memory, 0x0F000000, 0x0F000100)
    arm.mem.memories.append(mc)
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == RfeT1
    assert not opcode.increment
    assert not opcode.word_higher
    assert opcode.wback == 0
    assert opcode.n == 0
    arm.registers.set(0, 0x0F000008)
    arm.emulate_cycle()
    assert arm.registers.pc_store_value() == 0xAABBCCDC
    assert arm.registers.cpsr.value == 0x110233f2


def test_rfe_t2(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11101001100100001100000000000000
    arm.opcode_len = 32
    # setting Data Region registers
    arm.registers.drsrs[0].en = 1  # enabling memory region
    arm.registers.drsrs[0].rsize = 0b00010  # setting region size
    arm.registers.drbars[0] = 0x0F000000  # setting region base address
    arm.registers.dracrs[0].ap = 0b011  # setting access permissions
    arm.registers.mpuir.iregion = 0x01  # declaring the region
    arm.registers.mpuir.dregion = 0x01  # declaring the region
    ram_memory = RAM(0x100)
    ram_memory[0, 8] = b'\xDD\xcc\xbb\xaa\xf2\x33\x22\x11'
    mc = MemoryController(ram_memory, 0x0F000000, 0x0F000100)
    arm.mem.memories.append(mc)
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == RfeT2
    assert opcode.increment
    assert not opcode.word_higher
    assert opcode.wback == 0
    assert opcode.n == 0
    arm.registers.set(0, 0x0F000000)
    arm.emulate_cycle()
    assert arm.registers.pc_store_value() == 0xAABBCCDC
    assert arm.registers.cpsr.value == 0x110233f2


def test_rfe_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11111000100100000000101000000000
    arm.opcode_len = 32
    # setting Data Region registers
    arm.registers.drsrs[0].en = 1  # enabling memory region
    arm.registers.drsrs[0].rsize = 0b00010  # setting region size
    arm.registers.drbars[0] = 0x0F000000  # setting region base address
    arm.registers.dracrs[0].ap = 0b011  # setting access permissions
    arm.registers.mpuir.iregion = 0x01  # declaring the region
    arm.registers.mpuir.dregion = 0x01  # declaring the region
    ram_memory = RAM(0x100)
    ram_memory[0, 8] = b'\xDD\xcc\xbb\xaa\xf2\x33\x22\x11'
    mc = MemoryController(ram_memory, 0x0F000000, 0x0F000100)
    arm.mem.memories.append(mc)
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, RfeA1)
    assert opcode.increment
    assert not opcode.word_higher
    assert opcode.wback == 0
    assert opcode.n == 0
    arm.registers.set(0, 0x0F000000)
    arm.emulate_cycle()
    assert arm.registers.pc_store_value() == 0xAABBCCDC
    assert arm.registers.cpsr.value == 0x110233f2
