import pytest

from armulator.armv6.opcodes.concrete.asr_immediate_a1 import AsrImmediateA1
from armulator.armv6.opcodes.concrete.asr_immediate_t1 import AsrImmediateT1
from armulator.armv6.opcodes.concrete.asr_immediate_t2 import AsrImmediateT2
from armulator.armv6.opcodes.concrete.asr_register_a1 import AsrRegisterA1
from armulator.armv6.opcodes.concrete.asr_register_t1 import AsrRegisterT1
from armulator.armv6.opcodes.concrete.asr_register_t2 import AsrRegisterT2


@pytest.mark.parametrize('rm, rd, neg', [
    (4, 2, 0),
    (0xffffff00, 0xffffff80, 1),
])
def test_asr_immediate_t1(thumb_v6_without_fetch, rm, rd, neg):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b0001000001000001
    arm.opcode_len = 16
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == AsrImmediateT1
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
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0


@pytest.mark.parametrize('rn, rm, rd, neg', [
    (4, 1, 2, 0),
    (0xffffff00, 4, 0xfffffff0, 1),
])
def test_asr_register_t1(thumb_v6_without_fetch, rn, rm, rd, neg):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b0100000100000001
    arm.opcode_len = 16
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == AsrRegisterT1
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
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0


def test_asr_immediate_t2(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11101010010111110000000101100000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == AsrImmediateT2
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.d == 1
    assert opcode.shift_n == 1
    assert opcode.setflags
    arm.registers.set(0, 8)
    arm.emulate_cycle()
    assert arm.registers.get(1) == 4
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0


@pytest.mark.parametrize('rn, rm, rd, neg', [
    (4, 1, 2, 0),
    (0xffffff00, 4, 0xfffffff0, 1),
])
def test_asr_register_t2(thumb_v6_without_fetch, rn, rm, rd, neg):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11111010010100011111001000000000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == AsrRegisterT2
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
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0


def test_asr_immediate_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100001101100010010000011000000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, AsrImmediateA1)
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.d == 2
    assert opcode.shift_n == 1
    assert opcode.setflags
    arm.registers.set(opcode.m, 0xF0000080)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0xF8000040
    assert arm.registers.cpsr.n == 1
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0


def test_asr_register_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100001101100000010000001010001
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, AsrRegisterA1)
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.d == 2
    assert opcode.n == 1
    assert opcode.setflags
    arm.registers.set(opcode.n, 0xF0000080)
    arm.registers.set(opcode.m, 1)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0xF8000040
    assert arm.registers.cpsr.n == 1
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0
