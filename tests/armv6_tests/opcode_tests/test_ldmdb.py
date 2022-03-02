from armulator.armv6.memory_controller_hub import MemoryController
from armulator.armv6.memory_types import RAM
from armulator.armv6.opcodes.concrete.ldmdb_a1 import LdmdbA1
from armulator.armv6.opcodes.concrete.ldmdb_t1 import LdmdbT1


def test_ldmdb_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11101001001100001000000000000010
    arm.opcode_len = 32
    arm.registers.drsrs[0].en = 1  # enabling memory region
    arm.registers.drsrs[0].rsize = 0b01000  # setting region size
    arm.registers.drbars[0] = 0x0F000000  # setting region base address
    arm.registers.dracrs[0].ap = 0b011  # setting access permissions
    arm.registers.mpuir.iregion = 0x01  # declaring the region
    arm.registers.mpuir.dregion = 0x01  # declaring the region
    ram_memory = RAM(0x100)
    ram_memory.write(0x4, 8, b'\xAA\xBB\xCC\xDD\x55\x44\x33\x22')
    mc = MemoryController(ram_memory, 0x0F000000, 0x0F000100)
    arm.mem.memories.append(mc)
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, LdmdbT1)
    assert opcode.wback
    assert opcode.n == 0
    assert opcode.registers == 0b1000000000000010
    arm.registers.set(opcode.n, 0x0F00000C)
    arm.emulate_cycle()
    assert arm.registers.get(1) == 0xDDCCBBAA
    assert arm.registers.get(0) == 0x0F000004
    assert arm.registers.pc_store_value() == 0x22334454


def test_ldmdb_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11101001001100001000000000000010
    arm.opcode_len = 32
    arm.registers.drsrs[0].en = 1  # enabling memory region
    arm.registers.drsrs[0].rsize = 0b01000  # setting region size
    arm.registers.drbars[0] = 0x0F000000  # setting region base address
    arm.registers.dracrs[0].ap = 0b011  # setting access permissions
    arm.registers.mpuir.iregion = 0x01  # declaring the region
    arm.registers.mpuir.dregion = 0x01  # declaring the region
    ram_memory = RAM(0x100)
    ram_memory.write(0x4, 8, b'\xAA\xBB\xCC\xDD\x55\x44\x33\x22')
    mc = MemoryController(ram_memory, 0x0F000000, 0x0F000100)
    arm.mem.memories.append(mc)
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, LdmdbA1)
    assert opcode.wback
    assert opcode.n == 0
    assert opcode.registers == 0b1000000000000010
    arm.registers.set(opcode.n, 0x0F00000C)
    arm.emulate_cycle()
    assert arm.registers.get(1) == 0xDDCCBBAA
    assert arm.registers.get(0) == 0x0F000004
    assert arm.registers.pc_store_value() == 0x22334454
