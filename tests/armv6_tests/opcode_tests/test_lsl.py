import pytest

from armulator.armv6.opcodes.concrete.lsl_immediate_a1 import LslImmediateA1
from armulator.armv6.opcodes.concrete.lsl_immediate_t1 import LslImmediateT1
from armulator.armv6.opcodes.concrete.lsl_immediate_t2 import LslImmediateT2
from armulator.armv6.opcodes.concrete.lsl_register_a1 import LslRegisterA1
from armulator.armv6.opcodes.concrete.lsl_register_t1 import LslRegisterT1
from armulator.armv6.opcodes.concrete.lsl_register_t2 import LslRegisterT2


@pytest.mark.parametrize('rm, rd, neg, carry', [
    (1, 2, 0, 0),
    (0xfffff800, 0xfffff000, 1, 1),
])
def test_lsl_immediate_t1(thumb_v6_without_fetch, rm, rd, neg, carry):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b0000000001000001
    arm.opcode_len = 16
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == LslImmediateT1
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.d == 1
    assert opcode.shift_n == 1
    assert opcode.setflags
    arm.registers.set(0, rm)
    arm.emulate_cycle()
    assert arm.registers.get(1) == rd
    assert arm.registers.cpsr.n == neg
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == carry
    assert arm.registers.cpsr.v == 0


@pytest.mark.parametrize('rn, rm, rd, neg, carry', [
    (4, 1, 8, 0, 0),
    (0xffffff00, 4, 0xfffff000, 1, 1),
])
def test_lsl_register_t1(thumb_v6_without_fetch, rn, rm, rd, neg, carry):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b0100000010000001
    arm.opcode_len = 16
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == LslRegisterT1
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


def test_lsl_immediate_t2(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11101010010111110000000101000000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == LslImmediateT2
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.d == 1
    assert opcode.shift_n == 1
    assert opcode.setflags
    arm.registers.set(0, 4)
    arm.emulate_cycle()
    assert arm.registers.get(1) == 8
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0


@pytest.mark.parametrize('rn, rm, rd, neg, carry', [
    (4, 1, 8, 0, 0),
    (0xffffff00, 4, 0xfffff000, 1, 1),
])
def test_lsl_register_t2(thumb_v6_without_fetch, rn, rm, rd, neg, carry):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11111010000100011111001000000000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == LslRegisterT2
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


def test_lsl_immediate_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100001101100010010000010000000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, LslImmediateA1)
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.d == 2
    assert opcode.shift_n == 1
    assert opcode.setflags
    arm.registers.set(opcode.m, 0b0011)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0b0110
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0


def test_lsl_register_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100001101100000010000000010001
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, LslRegisterA1)
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.d == 2
    assert opcode.n == 1
    assert opcode.setflags
    arm.registers.set(opcode.n, 0b0011)
    arm.registers.set(opcode.m, 1)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0b0110
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0
