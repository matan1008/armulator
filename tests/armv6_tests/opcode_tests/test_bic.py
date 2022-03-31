from armulator.armv6.opcodes.concrete.bic_immediate_a1 import BicImmediateA1
from armulator.armv6.opcodes.concrete.bic_immediate_t1 import BicImmediateT1
from armulator.armv6.opcodes.concrete.bic_register_a1 import BicRegisterA1
from armulator.armv6.opcodes.concrete.bic_register_shifted_register_a1 import BicRegisterShiftedRegisterA1
from armulator.armv6.opcodes.concrete.bic_register_t1 import BicRegisterT1
from armulator.armv6.opcodes.concrete.bic_register_t2 import BicRegisterT2
from armulator.armv6.shift import SRType


def test_bic_register_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b0100001110000001
    arm.opcode_len = 16
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == BicRegisterT1
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.d == 1
    assert opcode.n == 1
    assert opcode.shift_t == SRType.LSL
    assert opcode.shift_n == 0
    assert opcode.setflags
    arm.registers.set(0, 3)
    arm.registers.set(1, 5)
    arm.emulate_cycle()
    assert arm.registers.get(1) == 4
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0


def test_bic_register_t2(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11101010001100010000001001000000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == BicRegisterT2
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.d == 2
    assert opcode.n == 1
    assert opcode.shift_t == SRType.LSL
    assert opcode.shift_n == 1
    assert opcode.setflags
    arm.registers.set(0, 3)
    arm.registers.set(1, 5)
    arm.emulate_cycle()
    assert arm.registers.get(2) == 1
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0


def test_bic_immediate_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11110000001100000000000100000110
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == BicImmediateT1
    assert opcode.instruction == arm.opcode
    assert opcode.imm32 == 0b110
    assert opcode.d == 1
    assert opcode.n == 0
    assert opcode.setflags
    assert opcode.carry == 0
    arm.registers.set(opcode.n, 5)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 1
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0


def test_bic_register_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100001110100010010000010000000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, BicRegisterA1)
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.d == 2
    assert opcode.n == 1
    assert opcode.shift_t == SRType.LSL
    assert opcode.shift_n == 1
    assert opcode.setflags
    arm.registers.set(opcode.n, 0b0101)
    arm.registers.set(opcode.m, 0b0011)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0b0001
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0


def test_bic_register_shifted_register_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100001110100010010001100010000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, BicRegisterShiftedRegisterA1)
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.d == 2
    assert opcode.n == 1
    assert opcode.s == 3
    assert opcode.shift_t == SRType.LSL
    assert opcode.setflags
    arm.registers.set(opcode.n, 0b0101)
    arm.registers.set(opcode.m, 0b0011)
    arm.registers.set(opcode.s, 1)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0b0001
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0


def test_bic_immediate_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100011110100000001000000000110
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, BicImmediateA1)
    assert opcode.instruction == arm.opcode
    assert opcode.imm32 == 0b110
    assert opcode.d == 1
    assert opcode.n == 0
    assert opcode.carry == 0
    assert opcode.setflags
    arm.registers.set(opcode.n, 0b0101)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0b001
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0
