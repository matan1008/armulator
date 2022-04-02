from armulator.armv6.memory_controller_hub import MemoryController
from armulator.armv6.memory_types import RAM
from armulator.armv6.opcodes.concrete.ldc_immediate_a1 import LdcLdc2ImmediateA1
from armulator.armv6.opcodes.concrete.ldc_ldc2_immediate_a2 import LdcLdc2ImmediateA2
from armulator.armv6.opcodes.concrete.ldc_ldc2_immediate_t1 import LdcLdc2ImmediateT1
from armulator.armv6.opcodes.concrete.ldc_ldc2_immediate_t2 import LdcLdc2ImmediateT2
from armulator.armv6.opcodes.concrete.ldc_ldc2_literal_a2 import LdcLdc2LiteralA2
from armulator.armv6.opcodes.concrete.ldc_ldc2_literal_t1 import LdcLdc2LiteralT1
from armulator.armv6.opcodes.concrete.ldc_ldc2_literal_t2 import LdcLdc2LiteralT2
from armulator.armv6.opcodes.concrete.ldc_literal_a1 import LdcLdc2LiteralA1


def test_ldc_immediate_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11101100100100000001000100000001
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
    assert type(opcode) == LdcLdc2ImmediateT1
    assert opcode.imm32 == 4
    assert opcode.n == 0
    assert opcode.cp == 1
    assert opcode.add
    assert not opcode.wback
    assert not opcode.index
    arm.registers.set(opcode.n, 0x0F000000)
    arm.registers.branch_to(0xFF000000)
    arm.emulate_cycle()
    assert arm.registers.pc_store_value() == 0x00000004


def test_ldc2_immediate_t2(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11111100100100000001000100000001
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
    assert type(opcode) == LdcLdc2ImmediateT2
    assert opcode.imm32 == 4
    assert opcode.n == 0
    assert opcode.cp == 1
    assert opcode.add
    assert not opcode.wback
    assert not opcode.index
    arm.registers.set(opcode.n, 0x0F000000)
    arm.registers.branch_to(0xFF000000)
    arm.emulate_cycle()
    assert arm.registers.pc_store_value() == 0x00000004


def test_ldc_literal_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11101101100111110001000100000001
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
    assert type(opcode) == LdcLdc2LiteralT1
    assert opcode.imm32 == 4
    assert opcode.cp == 1
    assert opcode.add
    assert opcode.index
    arm.registers.branch_to(0xFF000000)
    arm.emulate_cycle()
    assert arm.registers.pc_store_value() == 0x00000004


def test_ldc2_literal_t2(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11111101100111110001000100000001
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
    assert type(opcode) == LdcLdc2LiteralT2
    assert opcode.imm32 == 4
    assert opcode.cp == 1
    assert opcode.add
    assert opcode.index
    arm.registers.branch_to(0xFF000000)
    arm.emulate_cycle()
    assert arm.registers.pc_store_value() == 0x00000004


def test_ldc_immediate_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11101100100100000001000100000001
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
    assert isinstance(opcode, LdcLdc2ImmediateA1)
    assert opcode.imm32 == 4
    assert opcode.n == 0
    assert opcode.cp == 1
    assert opcode.add
    assert not opcode.wback
    assert not opcode.index
    arm.registers.set(opcode.n, 0x0F000000)
    arm.registers.branch_to(0xFF000000)
    arm.emulate_cycle()
    assert arm.registers.pc_store_value() == 0x00000004


def test_ldc_literal_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11101101100111110001000100000001
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
    assert isinstance(opcode, LdcLdc2LiteralA1)
    assert opcode.imm32 == 4
    assert opcode.cp == 1
    assert opcode.add
    assert opcode.index
    arm.registers.branch_to(0xFF000000)
    arm.emulate_cycle()
    assert arm.registers.pc_store_value() == 0x00000004


def test_ldc2_immediate_a2(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11111100100100000001000100000001
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
    assert isinstance(opcode, LdcLdc2ImmediateA2)
    assert opcode.imm32 == 4
    assert opcode.n == 0
    assert opcode.cp == 1
    assert opcode.add
    assert not opcode.wback
    assert not opcode.index
    arm.registers.set(opcode.n, 0x0F000000)
    arm.registers.branch_to(0xFF000000)
    arm.emulate_cycle()
    assert arm.registers.pc_store_value() == 0x00000004


def test_ldc2_literal_a2(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11111101100111110001000100000001
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
    assert isinstance(opcode, LdcLdc2LiteralA2)
    assert opcode.imm32 == 4
    assert opcode.cp == 1
    assert opcode.add
    assert opcode.index
    arm.registers.branch_to(0xFF000000)
    arm.emulate_cycle()
    assert arm.registers.pc_store_value() == 0x00000004
