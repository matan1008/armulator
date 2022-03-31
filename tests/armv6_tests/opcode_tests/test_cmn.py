from armulator.armv6.opcodes.concrete.cmn_immediate_a1 import CmnImmediateA1
from armulator.armv6.opcodes.concrete.cmn_immediate_t1 import CmnImmediateT1
from armulator.armv6.opcodes.concrete.cmn_register_a1 import CmnRegisterA1
from armulator.armv6.opcodes.concrete.cmn_register_shifted_register_a1 import CmnRegisterShiftedRegisterA1
from armulator.armv6.opcodes.concrete.cmn_register_t1 import CmnRegisterT1
from armulator.armv6.opcodes.concrete.cmn_register_t2 import CmnRegisterT2
from armulator.armv6.shift import SRType


def test_cmn_register_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b0100001011000001
    arm.opcode_len = 16
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == CmnRegisterT1
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.n == 1
    assert opcode.shift_t == SRType.LSL
    assert opcode.shift_n == 0
    arm.registers.set(0, 1)
    arm.registers.set(1, 0xffffffff)
    arm.emulate_cycle()
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 1
    assert arm.registers.cpsr.c == 1
    assert arm.registers.cpsr.v == 0


def test_cmn_register_t2(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11101011000100010000111101000000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == CmnRegisterT2
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.n == 1
    assert opcode.shift_t == SRType.LSL
    assert opcode.shift_n == 1
    arm.registers.set(0, 1)
    arm.registers.set(1, 0xfffffffe)
    arm.emulate_cycle()
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 1
    assert arm.registers.cpsr.c == 1
    assert arm.registers.cpsr.v == 0


def test_cmn_immediate_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11110001000100000000111100000010
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == CmnImmediateT1
    assert opcode.instruction == arm.opcode
    assert opcode.imm32 == 2
    assert opcode.n == 0
    arm.registers.set(opcode.n, 0xfffffffe)
    arm.emulate_cycle()
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 1
    assert arm.registers.cpsr.c == 1
    assert arm.registers.cpsr.v == 0


def test_cmn_register_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100001011100010000000010000000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, CmnRegisterA1)
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.n == 1
    assert opcode.shift_t == SRType.LSL
    assert opcode.shift_n == 1
    arm.registers.set(opcode.m, 1)
    arm.registers.set(opcode.n, 0xfffffffe)
    arm.emulate_cycle()
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 1
    assert arm.registers.cpsr.c == 1
    assert arm.registers.cpsr.v == 0


def test_cmn_register_shifted_register_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100001011100100000000000010001
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, CmnRegisterShiftedRegisterA1)
    assert opcode.instruction == arm.opcode
    assert opcode.s == 0
    assert opcode.m == 1
    assert opcode.n == 2
    assert opcode.shift_t == SRType.LSL
    arm.registers.set(opcode.m, 1)
    arm.registers.set(opcode.n, 0xfffffffe)
    arm.registers.set(opcode.s, 1)
    arm.emulate_cycle()
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 1
    assert arm.registers.cpsr.c == 1
    assert arm.registers.cpsr.v == 0


def test_cmn_immediate_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100011011100000000000000000010
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, CmnImmediateA1)
    assert opcode.instruction == arm.opcode
    assert opcode.imm32 == 2
    assert opcode.n == 0
    arm.registers.set(opcode.n, 0xFFFFFFFE)
    arm.emulate_cycle()
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 1
    assert arm.registers.cpsr.c == 1
    assert arm.registers.cpsr.v == 0
