from armulator.armv6.opcodes.concrete.smlald_a1 import SmlaldA1
from armulator.armv6.opcodes.concrete.smlald_t1 import SmlaldT1


def test_smlald_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11111011110000010011001011000000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, SmlaldT1)
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.n == 1
    assert opcode.d_hi == 2
    assert opcode.d_lo == 3
    assert not opcode.m_swap
    arm.registers.set(opcode.m, 0x70000000)
    arm.registers.set(opcode.n, 0xFFFFFF00)
    arm.registers.set(opcode.d_hi, 0x00000010)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d_hi) == 0x0000000F
    assert arm.registers.get(opcode.d_lo) == 0xFFFF9000


def test_smlald_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100111010000100011000000010001
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, SmlaldA1)
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.n == 1
    assert opcode.d_hi == 2
    assert opcode.d_lo == 3
    assert not opcode.m_swap
    arm.registers.set(opcode.m, 0x70000000)
    arm.registers.set(opcode.n, 0xFFFFFF00)
    arm.registers.set(opcode.d_hi, 0x00000010)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d_hi) == 0x0000000F
    assert arm.registers.get(opcode.d_lo) == 0xFFFF9000
