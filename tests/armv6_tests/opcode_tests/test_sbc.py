from armulator.armv6.opcodes.concrete.sbc_immediate_a1 import SbcImmediateA1
from armulator.armv6.opcodes.concrete.sbc_immediate_t1 import SbcImmediateT1
from armulator.armv6.opcodes.concrete.sbc_register_a1 import SbcRegisterA1
from armulator.armv6.opcodes.concrete.sbc_register_shifted_register_a1 import SbcRegisterShiftedRegisterA1
from armulator.armv6.opcodes.concrete.sbc_register_t1 import SbcRegisterT1
from armulator.armv6.opcodes.concrete.sbc_register_t2 import SbcRegisterT2
from armulator.armv6.shift import SRType


def test_sbc_register_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b0100000110000001
    arm.opcode_len = 16
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == SbcRegisterT1
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.d == 1
    assert opcode.n == 1
    assert opcode.shift_t == SRType.LSL
    assert opcode.shift_n == 0
    assert opcode.setflags
    arm.registers.cpsr.c = 1
    arm.registers.set(0, 1)
    arm.registers.set(1, 4)
    arm.emulate_cycle()
    assert arm.registers.get(1) == 3
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 1
    assert arm.registers.cpsr.v == 0


def test_sbc_register_t2(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11101011011100010000001001000000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == SbcRegisterT2
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.d == 2
    assert opcode.n == 1
    assert opcode.shift_t == SRType.LSL
    assert opcode.shift_n == 1
    assert opcode.setflags
    arm.registers.cpsr.c = 1
    arm.registers.set(0, 1)
    arm.registers.set(1, 4)
    arm.emulate_cycle()
    assert arm.registers.get(2) == 2
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 1
    assert arm.registers.cpsr.v == 0


def test_sbc_immediate_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11110001011100000000000100000010
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == SbcImmediateT1
    assert opcode.instruction == arm.opcode
    assert opcode.imm32 == 2
    assert opcode.d == 1
    assert opcode.n == 0
    assert opcode.setflags
    arm.registers.cpsr.c = 1
    arm.registers.set(opcode.n, 4)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 2
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 1
    assert arm.registers.cpsr.v == 0


def test_sbc_register_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100000110100010010000010000000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, SbcRegisterA1)
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.d == 2
    assert opcode.n == 1
    assert opcode.shift_t == SRType.LSL
    assert opcode.shift_n == 1
    assert opcode.setflags
    arm.registers.cpsr.c = 1
    arm.registers.set(opcode.n, 4)
    arm.registers.set(opcode.m, 1)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 2
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 1
    assert arm.registers.cpsr.v == 0


def test_sbc_register_shifted_register_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100000110100010010001100010000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, SbcRegisterShiftedRegisterA1)
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.d == 2
    assert opcode.n == 1
    assert opcode.s == 3
    assert opcode.shift_t == SRType.LSL
    assert opcode.setflags
    arm.registers.cpsr.c = 1
    arm.registers.set(opcode.n, 4)
    arm.registers.set(opcode.m, 1)
    arm.registers.set(opcode.s, 1)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 2
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 1
    assert arm.registers.cpsr.v == 0


def test_sbc_immediate_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100010110100000001000000000010
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, SbcImmediateA1)
    assert opcode.instruction == arm.opcode
    assert opcode.imm32 == 2
    assert opcode.d == 1
    assert opcode.n == 0
    assert opcode.setflags
    arm.registers.cpsr.c = 1
    arm.registers.set(opcode.n, 4)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 2
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 1
    assert arm.registers.cpsr.v == 0
