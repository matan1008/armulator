import pytest
from armulator.armv6.opcodes.concrete.cbz_t1 import CbzT1


@pytest.mark.parametrize('instruction, nonzero, imm32, r0, pc', [
    (0b1011000100100000, 0, 16, 0, 0x0F000014),
    (0b1011001100100000, 0, 0b10010000, 0, 0x0F000094),
    (0b1011100100100000, 1, 16, 1, 0x0F000014),
    (0b1011100100100000, 1, 16, 0, 0x0F000002),
    (0b1011101100100000, 1, 0b10010000, 1, 0x0F000094),
    (0b1011101100100000, 1, 0b10010000, 0, 0x0F000002),
])
def test_cbz_t1(thumb_v6_without_fetch, instruction, nonzero, imm32, r0, pc):
    arm = thumb_v6_without_fetch
    arm.opcode = instruction
    arm.opcode_len = 16
    prev_pc = 0x0F000000
    arm.registers.branch_to(prev_pc)
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == CbzT1
    assert opcode.nonzero == nonzero
    assert opcode.imm32 == imm32
    assert opcode.n == 0
    assert opcode.instruction == arm.opcode
    arm.registers.set(opcode.n, r0)
    arm.emulate_cycle()
    assert arm.registers.pc_store_value() == pc
