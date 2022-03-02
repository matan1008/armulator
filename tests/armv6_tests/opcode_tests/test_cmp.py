from armulator.armv6.opcodes.concrete.cmp_immediate_a1 import CmpImmediateA1
from armulator.armv6.opcodes.concrete.cmp_immediate_t1 import CmpImmediateT1
from armulator.armv6.opcodes.concrete.cmp_immediate_t2 import CmpImmediateT2
from armulator.armv6.opcodes.concrete.cmp_register_a1 import CmpRegisterA1
from armulator.armv6.opcodes.concrete.cmp_register_shifted_register_a1 import CmpRegisterShiftedRegisterA1
from armulator.armv6.opcodes.concrete.cmp_register_t1 import CmpRegisterT1
from armulator.armv6.opcodes.concrete.cmp_register_t2 import CmpRegisterT2
from armulator.armv6.opcodes.concrete.cmp_register_t3 import CmpRegisterT3
from armulator.armv6.shift import SRType


def test_cmp_immediate_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b0010100000000001
    arm.opcode_len = 16
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == CmpImmediateT1
    assert opcode.instruction == arm.opcode
    assert opcode.imm32 == 1
    assert opcode.n == 0
    arm.registers.set(0, 1)
    arm.emulate_cycle()
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 1
    assert arm.registers.cpsr.c == 1
    assert arm.registers.cpsr.v == 0


def test_cmp_register_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b0100001010000001
    arm.opcode_len = 16
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == CmpRegisterT1
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.n == 1
    assert opcode.shift_t == SRType.LSL
    assert opcode.shift_n == 0
    arm.registers.set(0, 5)
    arm.registers.set(1, 5)
    arm.emulate_cycle()
    assert arm.registers.get(1) == 5
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 1
    assert arm.registers.cpsr.c == 1
    assert arm.registers.cpsr.v == 0


def test_cmp_register_t2(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b0100010101000001
    arm.opcode_len = 16
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == CmpRegisterT2
    assert opcode.instruction == arm.opcode
    assert opcode.m == 8
    assert opcode.n == 1
    assert opcode.shift_t == SRType.LSL
    assert opcode.shift_n == 0
    arm.registers.set(8, 5)
    arm.registers.set(1, 5)
    arm.emulate_cycle()
    assert arm.registers.get(1) == 5
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 1
    assert arm.registers.cpsr.c == 1
    assert arm.registers.cpsr.v == 0


def test_cmp_register_t3(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11101011101100010000111101000000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == CmpRegisterT3
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
    assert arm.registers.cpsr.c == 1
    assert arm.registers.cpsr.v == 0


def test_cmp_immediate_t2(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11110001101100000000111100000001
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == CmpImmediateT2
    assert opcode.instruction == arm.opcode
    assert opcode.imm32 == 1
    assert opcode.n == 0
    arm.registers.set(opcode.n, 1)
    arm.emulate_cycle()
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 1
    assert arm.registers.cpsr.c == 1
    assert arm.registers.cpsr.v == 0


def test_cmp_register_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100001010100010000000010000000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, CmpRegisterA1)
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
    assert arm.registers.cpsr.c == 1
    assert arm.registers.cpsr.v == 0


def test_cmp_register_shifted_register_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100001010100100000000000010001
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, CmpRegisterShiftedRegisterA1)
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
    assert arm.registers.cpsr.c == 1
    assert arm.registers.cpsr.v == 0


def test_cmp_immediate_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100011010100000000000000000100
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, CmpImmediateA1)
    assert opcode.instruction == arm.opcode
    assert opcode.imm32 == 4
    assert opcode.n == 0
    arm.registers.set(opcode.n, 4)
    arm.emulate_cycle()
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 1
    assert arm.registers.cpsr.c == 1
    assert arm.registers.cpsr.v == 0
