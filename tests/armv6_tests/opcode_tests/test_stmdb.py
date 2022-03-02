from armulator.armv6.memory_controller_hub import MemoryController
from armulator.armv6.memory_types import RAM
from armulator.armv6.opcodes.concrete.stmdb_a1 import StmdbA1
from armulator.armv6.opcodes.concrete.stmdb_t1 import StmdbT1


def test_stmdb_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11101001001000010100000000100100
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
    assert isinstance(opcode, StmdbT1)
    assert opcode.wback
    assert opcode.n == 1
    assert opcode.registers == 0b0100000000100100
    arm.registers.set(opcode.n, 0x0F000010)
    arm.registers.set(2, 0x44332211)
    arm.registers.set(5, 0x88776655)
    arm.registers.set_lr(0xAABBCCDD)
    arm.emulate_cycle()
    assert ram_memory[4, 12] == b'\x11\x22\x33\x44\x55\x66\x77\x88\xDD\xCC\xBB\xAA'
    assert arm.registers.get(opcode.n) == 0x0F000004


def test_stmdb_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11101001001000010100000000100100
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
    assert isinstance(opcode, StmdbA1)
    assert opcode.wback
    assert opcode.n == 1
    assert opcode.registers == 0b0100000000100100
    arm.registers.set(opcode.n, 0x0F000010)
    arm.registers.set(2, 0x44332211)
    arm.registers.set(5, 0x88776655)
    arm.registers.set_lr(0xAABBCCDD)
    arm.emulate_cycle()
    assert ram_memory[4, 12] == b'\x11\x22\x33\x44\x55\x66\x77\x88\xDD\xCC\xBB\xAA'
    assert arm.registers.get(opcode.n) == 0x0F000004
