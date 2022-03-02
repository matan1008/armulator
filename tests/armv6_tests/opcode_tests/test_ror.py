import pytest

from armulator.armv6.opcodes.concrete.ror_immediate_a1 import RorImmediateA1
from armulator.armv6.opcodes.concrete.ror_immediate_t1 import RorImmediateT1
from armulator.armv6.opcodes.concrete.ror_register_a1 import RorRegisterA1
from armulator.armv6.opcodes.concrete.ror_register_t1 import RorRegisterT1
from armulator.armv6.opcodes.concrete.ror_register_t2 import RorRegisterT2


@pytest.mark.parametrize('rn, rm, rd, neg, carry', [
    (4, 1, 2, 0, 0),
    (0xffffff0f, 4, 0xfffffff0, 1, 1),
])
def test_ror_register_t1(thumb_v6_without_fetch, rn, rm, rd, neg, carry):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b0100000111000001
    arm.opcode_len = 16
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == RorRegisterT1
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.d == 1
    assert opcode.n == 1
    assert opcode.setflags
    arm.registers.set(0, rm)
    arm.registers.set(1, rn)
    arm.emulate_cycle()
    assert arm.registers.get(1) == rd
    assert arm.registers.cpsr.n == neg
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == carry
    assert arm.registers.cpsr.v == 0


def test_ror_immediate_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11101010010111110000000101110000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == RorImmediateT1
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.d == 1
    assert opcode.shift_n == 1
    assert opcode.setflags
    arm.registers.set(0, 0xffffff0f)
    arm.emulate_cycle()
    assert arm.registers.get(1) == 0xFFFFFF87
    assert arm.registers.cpsr.n == 1
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 1
    assert arm.registers.cpsr.v == 0


@pytest.mark.parametrize('rn, rm, rd, neg, carry', [
    (4, 1, 2, 0, 0),
    (0xffffff0f, 4, 0xfffffff0, 1, 1),
])
def test_ror_register_t2(thumb_v6_without_fetch, rn, rm, rd, neg, carry):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11111010011100011111001000000000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == RorRegisterT2
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.d == 2
    assert opcode.n == 1
    assert opcode.setflags
    arm.registers.set(opcode.m, rm)
    arm.registers.set(opcode.n, rn)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == rd
    assert arm.registers.cpsr.n == neg
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == carry
    assert arm.registers.cpsr.v == 0


def test_ror_immediate_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100001101100010010000011100000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, RorImmediateA1)
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.d == 2
    assert opcode.shift_n == 1
    assert opcode.setflags
    arm.registers.set(opcode.m, 0xFFFFFF0F)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0xFFFFFF87
    assert arm.registers.cpsr.n == 1
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 1
    assert arm.registers.cpsr.v == 0


def test_ror_register_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100001101100000010000001110001
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, RorRegisterA1)
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.d == 2
    assert opcode.n == 1
    assert opcode.setflags
    arm.registers.set(opcode.n, 0xFFFFFF0F)
    arm.registers.set(opcode.m, 1)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0xFFFFFF87
    assert arm.registers.cpsr.n == 1
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 1
    assert arm.registers.cpsr.v == 0
