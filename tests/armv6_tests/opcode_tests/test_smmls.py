from armulator.armv6.opcodes.concrete.smmls_a1 import SmmlsA1
from armulator.armv6.opcodes.concrete.smmls_t1 import SmmlsT1


def test_smmls_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11111011011000100000001100000001
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, SmmlsT1)
    assert opcode.instruction == arm.opcode
    assert opcode.a == 0
    assert opcode.m == 1
    assert opcode.n == 2
    assert opcode.d == 3
    assert not opcode.round
    arm.registers.set(opcode.a, 9)
    arm.registers.set(opcode.m, 0x70030004)
    arm.registers.set(opcode.n, 0xFFFFFFF0)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 16


def test_smmls_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100111010100110000000111010010
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, SmmlsA1)
    assert opcode.instruction == arm.opcode
    assert opcode.a == 0
    assert opcode.m == 1
    assert opcode.n == 2
    assert opcode.d == 3
    assert not opcode.round
    arm.registers.set(opcode.a, 9)
    arm.registers.set(opcode.m, 0x70030004)
    arm.registers.set(opcode.n, 0xFFFFFFF0)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 16
