from armulator.armv6.opcodes.concrete.teq_immediate_a1 import TeqImmediateA1
from armulator.armv6.opcodes.concrete.teq_immediate_t1 import TeqImmediateT1
from armulator.armv6.opcodes.concrete.teq_register_a1 import TeqRegisterA1
from armulator.armv6.opcodes.concrete.teq_register_shifted_register_a1 import TeqRegisterShiftedRegisterA1
from armulator.armv6.opcodes.concrete.teq_register_t1 import TeqRegisterT1
from armulator.armv6.shift import SRType


def test_teq_register_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11101010100100010000111101000000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == TeqRegisterT1
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.n == 1
    assert opcode.shift_t == SRType.LSL
    assert opcode.shift_n == 1
    arm.registers.set(0, 2)
    arm.registers.set(1, 4)
    arm.emulate_cycle()
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 1
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0


def test_teq_immediate_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11110000100100000000111100000100
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == TeqImmediateT1
    assert opcode.instruction == arm.opcode
    assert opcode.imm32 == 4
    assert opcode.n == 0
    assert opcode.carry == 0
    arm.registers.set(opcode.n, 4)
    arm.emulate_cycle()
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 1
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0


def test_teq_register_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100001001100010000000010000000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, TeqRegisterA1)
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.n == 1
    assert opcode.shift_t == SRType.LSL
    assert opcode.shift_n == 1
    arm.registers.set(opcode.m, 2)
    arm.registers.set(opcode.n, 4)
    arm.emulate_cycle()
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 1
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0


def test_teq_register_shifted_register_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100001001100100000000000010001
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, TeqRegisterShiftedRegisterA1)
    assert opcode.instruction == arm.opcode
    assert opcode.s == 0
    assert opcode.m == 1
    assert opcode.n == 2
    assert opcode.shift_t == SRType.LSL
    arm.registers.set(opcode.m, 2)
    arm.registers.set(opcode.n, 4)
    arm.registers.set(opcode.s, 1)
    arm.emulate_cycle()
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 1
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0


def test_teq_immediate_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100011001100000000000000000100
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, TeqImmediateA1)
    assert opcode.instruction == arm.opcode
    assert opcode.imm32 == 4
    assert opcode.n == 0
    assert opcode.carry == 0
    arm.registers.set(opcode.n, 4)
    arm.emulate_cycle()
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 1
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0
