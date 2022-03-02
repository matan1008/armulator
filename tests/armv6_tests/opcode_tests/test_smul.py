from armulator.armv6.opcodes.concrete.smul_a1 import SmulA1
from armulator.armv6.opcodes.concrete.smul_t1 import SmulT1


def test_smul_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11111011000100101111001100010001
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, SmulT1)
    assert opcode.instruction == arm.opcode
    assert opcode.m == 1
    assert opcode.n == 2
    assert opcode.d == 3
    assert opcode.m_high
    assert not opcode.n_high
    arm.registers.set(opcode.m, 0x00030004)
    arm.registers.set(opcode.n, 0x0000FFFF)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0xfffffffd


def test_smul_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100001011000110000000111000010
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, SmulA1)
    assert opcode.instruction == arm.opcode
    assert opcode.m == 1
    assert opcode.n == 2
    assert opcode.d == 3
    assert opcode.m_high
    assert not opcode.n_high
    arm.registers.set(opcode.m, 0x00030004)
    arm.registers.set(opcode.n, 0x0000FFFF)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0xfffffffd
