from armulator.armv6.opcodes.concrete.eor_immediate_a1 import EorImmediateA1
from armulator.armv6.opcodes.concrete.eor_immediate_t1 import EorImmediateT1
from armulator.armv6.opcodes.concrete.eor_register_a1 import EorRegisterA1
from armulator.armv6.opcodes.concrete.eor_register_shifted_register_a1 import EorRegisterShiftedRegisterA1
from armulator.armv6.opcodes.concrete.eor_register_t1 import EorRegisterT1
from armulator.armv6.opcodes.concrete.eor_register_t2 import EorRegisterT2
from armulator.armv6.shift import SRType


def test_eor_register_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b0100000001000001
    arm.opcode_len = 16
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == EorRegisterT1
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.d == 1
    assert opcode.n == 1
    assert opcode.shift_t == SRType.LSL
    assert opcode.shift_n == 0
    assert opcode.setflags
    arm.registers.set(0, 4)
    arm.registers.set(1, 5)
    arm.emulate_cycle()
    assert arm.registers.get(1) == 1
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0


def test_eor_register_t2(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11101010100100010000001001000000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == EorRegisterT2
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.d == 2
    assert opcode.n == 1
    assert opcode.shift_t == SRType.LSL
    assert opcode.shift_n == 1
    assert opcode.setflags
    arm.registers.set(0, 2)
    arm.registers.set(1, 5)
    arm.emulate_cycle()
    assert arm.registers.get(2) == 1
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0


def test_eor_immediate_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11110000100100000000000100000100
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == EorImmediateT1
    assert opcode.instruction == arm.opcode
    assert opcode.imm32 == 4
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


def test_eor_register_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100000001100010010000010000000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, EorRegisterA1)
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.d == 2
    assert opcode.n == 1
    assert opcode.shift_t == SRType.LSL
    assert opcode.shift_n == 1
    assert opcode.setflags
    arm.registers.set(opcode.n, 5)
    arm.registers.set(opcode.m, 2)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 1
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0


def test_eor_register_shifted_register_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100000001100010010001100010000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, EorRegisterShiftedRegisterA1)
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.d == 2
    assert opcode.n == 1
    assert opcode.s == 3
    assert opcode.shift_t == SRType.LSL
    assert opcode.setflags
    arm.registers.set(opcode.n, 5)
    arm.registers.set(opcode.m, 2)
    arm.registers.set(opcode.s, 1)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 1
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0


def test_eor_immediate_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100010001100000001000000000100
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, EorImmediateA1)
    assert opcode.instruction == arm.opcode
    assert opcode.imm32 == 4
    assert opcode.d == 1
    assert opcode.n == 0
    assert opcode.carry == 0
    assert opcode.setflags
    arm.registers.set(opcode.n, 5)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 1
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0
