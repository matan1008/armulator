import pytest

from armulator.armv6.memory_controller_hub import MemoryController
from armulator.armv6.memory_types import RAM
from armulator.armv6.opcodes.concrete.tbb_tbh_t1 import TbbTbhT1


@pytest.mark.parametrize('instruction, is_tbh, pc', [
    (0b11101000110100001111000000000001, 0, 0x44),
    (0b11101000110100001111000000010001, 1, 0x8064),
])
def test_tbb_tbh_t1(thumb_v6_without_fetch, instruction, is_tbh, pc):
    arm = thumb_v6_without_fetch
    arm.opcode = instruction
    arm.opcode_len = 32
    # setting Data Region registers
    arm.registers.drsrs[0].en = 1  # enabling memory region
    arm.registers.drsrs[0].rsize = 0b00011  # setting region size
    arm.registers.drbars[0] = 0x0F000000  # setting region base address
    arm.registers.dracrs[0].ap = 0b011  # setting access permissions
    arm.registers.mpuir.iregion = 0x01  # declaring the region
    arm.registers.mpuir.dregion = 0x01  # declaring the region
    ram_memory = RAM(0x100)
    ram_memory.write(0, 4, b'\x10\x20\x30\x40')
    mc = MemoryController(ram_memory, 0x0F000000, 0x0F000100)
    arm.mem.memories.append(mc)
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == TbbTbhT1
    assert opcode.is_tbh == is_tbh
    assert opcode.instruction == arm.opcode
    assert opcode.n == 0
    assert opcode.m == 1
    arm.registers.set(opcode.n, 0x0F000000)
    arm.registers.set(opcode.m, 1)
    arm.emulate_cycle()
    assert arm.registers.pc_store_value() == pc
