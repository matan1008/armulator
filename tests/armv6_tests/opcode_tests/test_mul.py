from armulator.armv6.opcodes.concrete.mul_a1 import MulA1
from armulator.armv6.opcodes.concrete.mul_t1 import MulT1
from armulator.armv6.opcodes.concrete.mul_t2 import MulT2


def test_mul_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b0100001101000001
    arm.opcode_len = 16
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == MulT1
    assert opcode.instruction == arm.opcode
    assert opcode.m == 1
    assert opcode.d == 1
    assert opcode.n == 0
    assert opcode.setflags
    arm.registers.set(0, 5)
    arm.registers.set(1, 4)
    arm.emulate_cycle()
    assert arm.registers.get(1) == 20
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0


def test_mul_t2(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11111011000000001111001000000001
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, MulT2)
    assert opcode.setflags is False
    assert opcode.n == 0
    assert opcode.m == 1
    assert opcode.d == 2
    arm.registers.set(opcode.n, 0x00000004)
    arm.registers.set(opcode.m, 0x00000002)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0x00000008
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0


def test_mul_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100000000100100000000010010001
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, MulA1)
    assert opcode.setflags
    assert opcode.n == 1
    assert opcode.m == 0
    assert opcode.d == 2
    arm.registers.set(opcode.n, 0x00000004)
    arm.registers.set(opcode.m, 0x00000002)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0x00000008
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0
