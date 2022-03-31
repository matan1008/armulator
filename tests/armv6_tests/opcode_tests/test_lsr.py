import pytest

from armulator.armv6.opcodes.concrete.lsr_immediate_a1 import LsrImmediateA1
from armulator.armv6.opcodes.concrete.lsr_immediate_t1 import LsrImmediateT1
from armulator.armv6.opcodes.concrete.lsr_immediate_t2 import LsrImmediateT2
from armulator.armv6.opcodes.concrete.lsr_register_a1 import LsrRegisterA1
from armulator.armv6.opcodes.concrete.lsr_register_t1 import LsrRegisterT1
from armulator.armv6.opcodes.concrete.lsr_register_t2 import LsrRegisterT2


@pytest.mark.parametrize('rm, rd', [
    (4, 2),
    (0xffffff00, 0x7fffff80),
])
def test_lsr_immediate_t1(thumb_v6_without_fetch, rm, rd):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b0000100001000001
    arm.opcode_len = 16
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == LsrImmediateT1
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.d == 1
    assert opcode.shift_n == 1
    assert opcode.setflags
    arm.registers.set(0, rm)
    arm.emulate_cycle()
    assert arm.registers.get(1) == rd
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0


@pytest.mark.parametrize('rn, rm, rd', [
    (4, 1, 2),
    (0xffffff00, 4, 0x0ffffff0),
])
def test_lsr_register_t1(thumb_v6_without_fetch, rn, rm, rd):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b0100000011000001
    arm.opcode_len = 16
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == LsrRegisterT1
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.d == 1
    assert opcode.n == 1
    assert opcode.setflags
    arm.registers.set(0, rm)
    arm.registers.set(1, rn)
    arm.emulate_cycle()
    assert arm.registers.get(1) == rd
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0


def test_lsr_immediate_t2(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11101010010111110000000101010000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == LsrImmediateT2
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.d == 1
    assert opcode.shift_n == 1
    assert opcode.setflags
    arm.registers.set(0, 4)
    arm.emulate_cycle()
    assert arm.registers.get(1) == 2
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0


@pytest.mark.parametrize('rn, rm, rd', [
    (4, 1, 2),
    (0xffffff00, 4, 0x0ffffff0),
])
def test_lsr_register_t2(thumb_v6_without_fetch, rn, rm, rd):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11111010001100011111001000000000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == LsrRegisterT2
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.d == 2
    assert opcode.n == 1
    assert opcode.setflags
    arm.registers.set(opcode.m, rm)
    arm.registers.set(opcode.n, rn)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == rd
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0


def test_lsr_immediate_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100001101100010010000010100000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, LsrImmediateA1)
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.d == 2
    assert opcode.shift_n == 1
    assert opcode.setflags
    arm.registers.set(opcode.m, 4)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 2
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0


def test_lsr_register_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100001101100000010000000110001
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, LsrRegisterA1)
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.d == 2
    assert opcode.n == 1
    assert opcode.setflags
    arm.registers.set(opcode.n, 4)
    arm.registers.set(opcode.m, 1)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 2
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0
