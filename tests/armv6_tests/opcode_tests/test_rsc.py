from armulator.armv6.opcodes.concrete.rsc_immediate_a1 import RscImmediateA1
from armulator.armv6.opcodes.concrete.rsc_register_a1 import RscRegisterA1
from armulator.armv6.opcodes.concrete.rsc_register_shifted_register_a1 import RscRegisterShiftedRegisterA1
from armulator.armv6.shift import SRType


def test_rsc_register_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100000111100010010000010000000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, RscRegisterA1)
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.d == 2
    assert opcode.n == 1
    assert opcode.shift_t == SRType.LSL
    assert opcode.shift_n == 1
    assert opcode.setflags
    arm.registers.cpsr.c = 1
    arm.registers.set(opcode.n, 1)
    arm.registers.set(opcode.m, 2)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 3
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 1
    assert arm.registers.cpsr.v == 0


def test_rsc_register_shifted_register_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100000111100010010001100010000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, RscRegisterShiftedRegisterA1)
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.d == 2
    assert opcode.n == 1
    assert opcode.s == 3
    assert opcode.shift_t == SRType.LSL
    assert opcode.setflags
    arm.registers.cpsr.c = 1
    arm.registers.set(opcode.n, 1)
    arm.registers.set(opcode.m, 2)
    arm.registers.set(opcode.s, 1)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 3
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 1
    assert arm.registers.cpsr.v == 0


def test_rsc_immediate_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100010111100000001000000000100
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, RscImmediateA1)
    assert opcode.instruction == arm.opcode
    assert opcode.imm32 == 4
    assert opcode.d == 1
    assert opcode.n == 0
    assert opcode.setflags
    arm.registers.cpsr.c = 1
    arm.registers.set(opcode.n, 1)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 3
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 1
    assert arm.registers.cpsr.v == 0
