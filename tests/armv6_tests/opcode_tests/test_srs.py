from armulator.armv6.memory_controller_hub import MemoryController
from armulator.armv6.memory_types import RAM
from armulator.armv6.opcodes.concrete.srs_arm_a1 import SrsArmA1
from armulator.armv6.opcodes.concrete.srs_thumb_t1 import SrsThumbT1
from armulator.armv6.opcodes.concrete.srs_thumb_t2 import SrsThumbT2


def test_srs_thumb_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11101000000011011100000000010010
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
    assert type(opcode) == SrsThumbT1
    assert not opcode.increment
    assert not opcode.word_higher
    assert opcode.wback == 0
    assert opcode.mode == 0b10010
    arm.registers.cpsr.m = 0b10011
    arm.registers.set_rmode(13, opcode.mode, 0x0F000008)
    arm.registers.set_lr(0xAABBCCDD)
    arm.registers.spsr_svc = 0x11223344
    arm.emulate_cycle()
    assert ram_memory[0, 8] == b'\xdd\xcc\xbb\xaa\x44\x33\x22\x11'


def test_srs_thumb_t2(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11101001100011011100000000010010
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
    assert type(opcode) == SrsThumbT2
    assert opcode.increment
    assert not opcode.word_higher
    assert opcode.wback == 0
    assert opcode.mode == 0b10010
    arm.registers.cpsr.m = 0b10011
    arm.registers.set_rmode(13, opcode.mode, 0x0F000000)
    arm.registers.set_lr(0xAABBCCDD)
    arm.registers.spsr_svc = 0x11223344
    arm.emulate_cycle()
    assert ram_memory[0, 8] == b'\xdd\xcc\xbb\xaa\x44\x33\x22\x11'


def test_srs_arm_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11111000110011010000010100010010
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
    assert isinstance(opcode, SrsArmA1)
    assert opcode.increment
    assert not opcode.word_higher
    assert not opcode.wback
    assert opcode.mode == 0b10010
    arm.registers.cpsr.m = 0b10011
    arm.registers.set_rmode(13, opcode.mode, 0x0F000000)
    arm.registers.set_lr(0xAABBCCDD)
    arm.registers.spsr_svc = 0x11223344
    arm.emulate_cycle()
    assert ram_memory[0, 8] == b'\xdd\xcc\xbb\xaa\x44\x33\x22\x11'
