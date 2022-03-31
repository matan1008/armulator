from armulator.armv6.opcodes.concrete.mls_a1 import MlsA1
from armulator.armv6.opcodes.concrete.mls_t1 import MlsT1


def test_mls_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11111011000000100000001100010001
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, MlsT1)
    assert opcode.instruction == arm.opcode
    assert opcode.a == 0
    assert opcode.m == 1
    assert opcode.n == 2
    assert opcode.d == 3
    arm.registers.set(opcode.a, 21)
    arm.registers.set(opcode.m, 4)
    arm.registers.set(opcode.n, 5)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 1


def test_mls_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100000011000110000000110010010
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, MlsA1)
    assert opcode.n == 2
    assert opcode.m == 1
    assert opcode.d == 3
    assert opcode.a == 0
    arm.registers.set(opcode.a, 21)
    arm.registers.set(opcode.m, 4)
    arm.registers.set(opcode.n, 5)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 1
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0
