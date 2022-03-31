from armulator.armv6.opcodes.concrete.smmla_a1 import SmmlaA1
from armulator.armv6.opcodes.concrete.smmla_t1 import SmmlaT1


def test_smmla_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11111011010100100000001100000001
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, SmmlaT1)
    assert opcode.instruction == arm.opcode
    assert opcode.a == 0
    assert opcode.m == 1
    assert opcode.n == 2
    assert opcode.d == 3
    assert not opcode.round
    arm.registers.set(opcode.a, 3)
    arm.registers.set(opcode.m, 0x00030004)
    arm.registers.set(opcode.n, 0x0001FFFF)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 9


def test_smmla_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100111010100110000000100010010
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, SmmlaA1)
    assert opcode.instruction == arm.opcode
    assert opcode.a == 0
    assert opcode.m == 1
    assert opcode.n == 2
    assert opcode.d == 3
    assert not opcode.round
    arm.registers.set(opcode.a, 3)
    arm.registers.set(opcode.m, 0x00030004)
    arm.registers.set(opcode.n, 0x0001FFFF)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 9
