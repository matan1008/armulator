from armulator.armv6.opcodes.concrete.tst_immediate_a1 import TstImmediateA1
from armulator.armv6.opcodes.concrete.tst_immediate_t1 import TstImmediateT1
from armulator.armv6.opcodes.concrete.tst_register_a1 import TstRegisterA1
from armulator.armv6.opcodes.concrete.tst_register_shifted_register_a1 import TstRegisterShiftedRegisterA1
from armulator.armv6.opcodes.concrete.tst_register_t1 import TstRegisterT1
from armulator.armv6.opcodes.concrete.tst_register_t2 import TstRegisterT2
from armulator.armv6.shift import SRType


def test_tst_register_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b0100001000000001
    arm.opcode_len = 16
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == TstRegisterT1
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.n == 1
    assert opcode.shift_t == SRType.LSL
    assert opcode.shift_n == 0
    arm.registers.set(0, 4)
    arm.registers.set(1, 5)
    arm.emulate_cycle()
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0


def test_tst_register_t2(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11101010000100010000111101000000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == TstRegisterT2
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.n == 1
    assert opcode.shift_t == SRType.LSL
    assert opcode.shift_n == 1
    arm.registers.set(0, 4)
    arm.registers.set(1, 5)
    arm.emulate_cycle()
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 1
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0


def test_tst_immediate_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11110000000100010000111100001000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == TstImmediateT1
    assert opcode.instruction == arm.opcode
    assert opcode.imm32 == 8
    assert opcode.n == 1
    assert opcode.carry == 0
    arm.registers.set(opcode.n, 5)
    arm.emulate_cycle()
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 1
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0


def test_tst_register_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100001000100010000000010000000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, TstRegisterA1)
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.n == 1
    assert opcode.shift_t == SRType.LSL
    assert opcode.shift_n == 1
    arm.registers.set(0, 4)
    arm.registers.set(1, 5)
    arm.emulate_cycle()
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 1
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0


def test_tst_register_shifted_register_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100001000100100000000000010001
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, TstRegisterShiftedRegisterA1)
    assert opcode.instruction == arm.opcode
    assert opcode.s == 0
    assert opcode.m == 1
    assert opcode.n == 2
    assert opcode.shift_t == SRType.LSL
    arm.registers.set(opcode.m, 4)
    arm.registers.set(opcode.n, 5)
    arm.registers.set(opcode.s, 1)
    arm.emulate_cycle()
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 1
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0


def test_tst_immediate_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100011000100000000000000001000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, TstImmediateA1)
    assert opcode.instruction == arm.opcode
    assert opcode.imm32 == 8
    assert opcode.n == 0
    assert opcode.carry == 0
    arm.registers.set(opcode.n, 5)
    arm.emulate_cycle()
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 1
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0
