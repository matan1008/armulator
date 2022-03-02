from armulator.armv6.opcodes.concrete.mla_a1 import MlaA1
from armulator.armv6.opcodes.concrete.mla_t1 import MlaT1


def test_mla_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11111011000000100000001100000001
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, MlaT1)
    assert opcode.instruction == arm.opcode
    assert opcode.a == 0
    assert opcode.m == 1
    assert opcode.n == 2
    assert opcode.d == 3
    assert not opcode.setflags
    arm.registers.set(opcode.a, 3)
    arm.registers.set(opcode.m, 4)
    arm.registers.set(opcode.n, 5)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 23


def test_mla_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100000001100110000000110010010
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, MlaA1)
    assert opcode.setflags
    assert opcode.n == 2
    assert opcode.m == 1
    assert opcode.d == 3
    assert opcode.a == 0
    arm.registers.set(opcode.a, 3)
    arm.registers.set(opcode.m, 4)
    arm.registers.set(opcode.n, 5)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 23
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0
