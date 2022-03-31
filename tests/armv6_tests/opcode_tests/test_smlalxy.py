from armulator.armv6.opcodes.concrete.smlalxy_a1 import SmlalxyA1
from armulator.armv6.opcodes.concrete.smlalxy_t1 import SmlalxyT1


def test_smlalxy_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11111011110000010011001010000000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, SmlalxyT1)
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.n == 1
    assert opcode.d_hi == 2
    assert opcode.d_lo == 3
    assert not opcode.m_high
    assert not opcode.n_high
    arm.registers.set(opcode.m, 0x00000007)
    arm.registers.set(opcode.n, 0xFFFFFF00)
    arm.registers.set(opcode.d_hi, 0x00000010)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d_hi) == 0x0000000F
    assert arm.registers.get(opcode.d_lo) == 0xFFFFF900


def test_smlalxy_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100001010000100011000010000001
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, SmlalxyA1)
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.n == 1
    assert opcode.d_hi == 2
    assert opcode.d_lo == 3
    assert not opcode.m_high
    assert not opcode.n_high
    arm.registers.set(opcode.m, 0x00000007)
    arm.registers.set(opcode.n, 0xFFFFFF00)
    arm.registers.set(opcode.d_hi, 0x00000010)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d_hi) == 0x0000000F
    assert arm.registers.get(opcode.d_lo) == 0xFFFFF900
