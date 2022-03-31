from armulator.armv6.memory_controller_hub import MemoryController
from armulator.armv6.memory_types import RAM
from armulator.armv6.opcodes.concrete.stc_a1 import StcStc2A1
from armulator.armv6.opcodes.concrete.stc_stc2_a2 import StcStc2A2
from armulator.armv6.opcodes.concrete.stc_stc2_t1 import StcStc2T1
from armulator.armv6.opcodes.concrete.stc_stc2_t2 import StcStc2T2


def test_stc_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11101100100000000000000100000001
    arm.opcode_len = 32
    # setting Data Region registers
    arm.registers.drsrs[0].en = 1  # enabling memory region
    arm.registers.drsrs[0].rsize = 0b00100  # setting region size
    arm.registers.drbars[0] = 0x0F000000  # setting region base address
    arm.registers.dracrs[0].ap = 0b011  # setting access permissions
    arm.registers.mpuir.iregion = 0x01  # declaring the region
    arm.registers.mpuir.dregion = 0x01  # declaring the region
    ram_memory = RAM(0x100)
    mc = MemoryController(ram_memory, 0x0F000000, 0x0F000100)
    arm.mem.memories.append(mc)
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == StcStc2T1
    assert opcode.cp == 1
    assert opcode.n == 0
    assert opcode.add
    assert opcode.imm32 == 4
    assert not opcode.index
    assert not opcode.wback
    arm.registers.set(opcode.n, 0x0F000000)
    arm.registers.branch_to(0xFF000000)
    arm.emulate_cycle()
    assert arm.registers.pc_store_value() == 0x00000004


def test_stc2_t2(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11111100100000000000000100000001
    arm.opcode_len = 32
    # setting Data Region registers
    arm.registers.drsrs[0].en = 1  # enabling memory region
    arm.registers.drsrs[0].rsize = 0b00100  # setting region size
    arm.registers.drbars[0] = 0x0F000000  # setting region base address
    arm.registers.dracrs[0].ap = 0b011  # setting access permissions
    arm.registers.mpuir.iregion = 0x01  # declaring the region
    arm.registers.mpuir.dregion = 0x01  # declaring the region
    ram_memory = RAM(0x100)
    mc = MemoryController(ram_memory, 0x0F000000, 0x0F000100)
    arm.mem.memories.append(mc)
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == StcStc2T2
    assert opcode.cp == 1
    assert opcode.n == 0
    assert opcode.add
    assert opcode.imm32 == 4
    assert not opcode.index
    assert not opcode.wback
    arm.registers.set(opcode.n, 0x0F000000)
    arm.registers.branch_to(0xFF000000)
    arm.emulate_cycle()
    assert arm.registers.pc_store_value() == 0x00000004


def test_stc_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11101100100000000000000100000001
    arm.opcode_len = 32
    # setting Data Region registers
    arm.registers.drsrs[0].en = 1  # enabling memory region
    arm.registers.drsrs[0].rsize = 0b00100  # setting region size
    arm.registers.drbars[0] = 0x0F000000  # setting region base address
    arm.registers.dracrs[0].ap = 0b011  # setting access permissions
    arm.registers.mpuir.iregion = 0x01  # declaring the region
    arm.registers.mpuir.dregion = 0x01  # declaring the region
    ram_memory = RAM(0x100)
    mc = MemoryController(ram_memory, 0x0F000000, 0x0F000100)
    arm.mem.memories.append(mc)
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, StcStc2A1)
    assert opcode.cp == 1
    assert opcode.n == 0
    assert opcode.add
    assert opcode.imm32 == 4
    assert not opcode.index
    assert not opcode.wback
    arm.registers.set(opcode.n, 0x0F000000)
    arm.registers.branch_to(0xFF000000)
    arm.emulate_cycle()
    assert arm.registers.pc_store_value() == 0x00000004


def test_stc2_a2(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11111100100000000000000100000001
    arm.opcode_len = 32
    # setting Data Region registers
    arm.registers.drsrs[0].en = 1  # enabling memory region
    arm.registers.drsrs[0].rsize = 0b00100  # setting region size
    arm.registers.drbars[0] = 0x0F000000  # setting region base address
    arm.registers.dracrs[0].ap = 0b011  # setting access permissions
    arm.registers.mpuir.iregion = 0x01  # declaring the region
    arm.registers.mpuir.dregion = 0x01  # declaring the region
    ram_memory = RAM(0x100)
    mc = MemoryController(ram_memory, 0x0F000000, 0x0F000100)
    arm.mem.memories.append(mc)
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, StcStc2A2)
    assert opcode.cp == 1
    assert opcode.n == 0
    assert opcode.add
    assert opcode.imm32 == 4
    assert not opcode.index
    assert not opcode.wback
    arm.registers.set(opcode.n, 0x0F000000)
    arm.registers.branch_to(0xFF000000)
    arm.emulate_cycle()
    assert arm.registers.pc_store_value() == 0x00000004
