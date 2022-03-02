from armulator.armv6.opcodes.concrete.smlaw_a1 import SmlawA1
from armulator.armv6.opcodes.concrete.smlaw_t1 import SmlawT1


def test_smlaw_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11111011001100100000001100000001
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, SmlawT1)
    assert opcode.instruction == arm.opcode
    assert opcode.a == 0
    assert opcode.m == 1
    assert opcode.n == 2
    assert opcode.d == 3
    assert not opcode.m_high
    arm.registers.set(opcode.a, 3)
    arm.registers.set(opcode.m, 0x0003FFFF)
    arm.registers.set(opcode.n, 0x00000004)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 2


def test_smlaw_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100001001000110000000110000010
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, SmlawA1)
    assert opcode.instruction == arm.opcode
    assert opcode.a == 0
    assert opcode.m == 1
    assert opcode.n == 2
    assert opcode.d == 3
    assert not opcode.m_high
    arm.registers.set(opcode.a, 3)
    arm.registers.set(opcode.m, 0x0003FFFF)
    arm.registers.set(opcode.n, 0x00000004)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 2
