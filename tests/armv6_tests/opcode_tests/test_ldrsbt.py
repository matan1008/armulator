from armulator.armv6.memory_controller_hub import MemoryController
from armulator.armv6.memory_types import RAM
from armulator.armv6.opcodes.concrete.ldrsbt_a1 import LdrsbtA1
from armulator.armv6.opcodes.concrete.ldrsbt_a2 import LdrsbtA2
from armulator.armv6.opcodes.concrete.ldrsbt_t1 import LdrsbtT1


def test_ldrsbt_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11111001000100000001111000000100
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
    assert isinstance(opcode, LdrsbtT1)
    assert opcode.instruction == arm.opcode
    assert not opcode.register_form
    assert opcode.add
    assert not opcode.post_index
    assert opcode.t == 1
    assert opcode.n == 0
    assert opcode.imm32 == 4
    arm.registers.set(opcode.n, 0x0F000000)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.t) == 0xffffff88


def test_ldrsbt_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100000111100010010000011010100
    arm.opcode_len = 32
    # setting Data Region registers
    arm.registers.drsrs[0].en = 1  # enabling memory region
    arm.registers.drsrs[0].rsize = 0b00011  # setting region size
    arm.registers.drbars[0] = 0x0F000000  # setting region base address
    arm.registers.dracrs[0].ap = 0b011  # setting access permissions
    arm.registers.mpuir.iregion = 0x01  # declaring the region
    arm.registers.mpuir.dregion = 0x01  # declaring the region
    ram_memory = RAM(0x100)
    ram_memory.write(0x0, 4, b'\x88\x33\x22\x11')
    mc = MemoryController(ram_memory, 0x0F000000, 0x0F000100)
    arm.mem.memories.append(mc)
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, LdrsbtA1)
    assert opcode.instruction == arm.opcode
    assert not opcode.register_form
    assert opcode.add
    assert opcode.post_index
    assert opcode.t == 2
    assert opcode.n == 1
    assert opcode.imm32 == 4
    arm.registers.set(opcode.n, 0x0F000000)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.t) == 0xffffff88
    assert arm.registers.get(opcode.n) == 0x0F000004


def test_ldrsbt_a2(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100000101100010010000011010000
    arm.opcode_len = 32
    # setting Data Region registers
    arm.registers.drsrs[0].en = 1  # enabling memory region
    arm.registers.drsrs[0].rsize = 0b00011  # setting region size
    arm.registers.drbars[0] = 0x0F000000  # setting region base address
    arm.registers.dracrs[0].ap = 0b011  # setting access permissions
    arm.registers.mpuir.iregion = 0x01  # declaring the region
    arm.registers.mpuir.dregion = 0x01  # declaring the region
    ram_memory = RAM(0x100)
    ram_memory.write(0x0, 4, b'\x88\x33\x22\x11')
    mc = MemoryController(ram_memory, 0x0F000000, 0x0F000100)
    arm.mem.memories.append(mc)
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, LdrsbtA2)
    assert opcode.instruction == arm.opcode
    assert opcode.register_form
    assert opcode.add
    assert opcode.post_index
    assert opcode.t == 2
    assert opcode.n == 1
    assert opcode.imm32 == 0
    assert opcode.m == 0
    arm.registers.set(opcode.n, 0x0F000000)
    arm.registers.set(opcode.m, 4)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.t) == 0xffffff88
    assert arm.registers.get(opcode.n) == 0x0F000004
