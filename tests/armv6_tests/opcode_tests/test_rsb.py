from armulator.armv6.opcodes.concrete.rsb_immediate_a1 import RsbImmediateA1
from armulator.armv6.opcodes.concrete.rsb_immediate_t1 import RsbImmediateT1
from armulator.armv6.opcodes.concrete.rsb_immediate_t2 import RsbImmediateT2
from armulator.armv6.opcodes.concrete.rsb_register_a1 import RsbRegisterA1
from armulator.armv6.opcodes.concrete.rsb_register_shifted_register_a1 import RsbRegisterShiftedRegisterA1
from armulator.armv6.opcodes.concrete.rsb_register_t1 import RsbRegisterT1
from armulator.armv6.shift import SRType


def test_rsb_immediate_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b0100001001000001
    arm.opcode_len = 16
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == RsbImmediateT1
    assert opcode.instruction == arm.opcode
    assert opcode.imm32 == 0
    assert opcode.d == 1
    assert opcode.n == 0
    assert opcode.setflags
    arm.registers.set(0, 5)
    arm.emulate_cycle()
    assert arm.registers.get(1) == 4294967291
    assert arm.registers.cpsr.n == 1
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0


def test_rsb_register_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11101011110100010000001001000000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == RsbRegisterT1
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.d == 2
    assert opcode.n == 1
    assert opcode.shift_n == 1
    assert opcode.shift_t == SRType.LSL
    assert opcode.setflags
    arm.registers.set(0, 0)
    arm.registers.set(1, 5)
    arm.emulate_cycle()
    assert arm.registers.get(2) == 4294967291
    assert arm.registers.cpsr.n == 1
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0


def test_rsb_immediate_t2(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11110001110100000000000100000000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == RsbImmediateT2
    assert opcode.instruction == arm.opcode
    assert opcode.imm32 == 0
    assert opcode.d == 1
    assert opcode.n == 0
    assert opcode.setflags
    arm.registers.set(opcode.n, 5)
    arm.emulate_cycle()
    assert arm.registers.get(1) == 4294967291
    assert arm.registers.cpsr.n == 1
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0


def test_rsb_register_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100000011100010010000010000000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, RsbRegisterA1)
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.d == 2
    assert opcode.n == 1
    assert opcode.shift_t == SRType.LSL
    assert opcode.shift_n == 1
    assert opcode.setflags
    arm.registers.set(opcode.n, 5)
    arm.registers.set(opcode.m, 0)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 4294967291
    assert arm.registers.cpsr.n == 1
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0


def test_rsb_register_shifted_register_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100000011100010010001100010000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, RsbRegisterShiftedRegisterA1)
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.d == 2
    assert opcode.n == 1
    assert opcode.s == 3
    assert opcode.shift_t == SRType.LSL
    assert opcode.setflags
    arm.registers.set(opcode.n, 5)
    arm.registers.set(opcode.m, 0)
    arm.registers.set(opcode.s, 1)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 4294967291
    assert arm.registers.cpsr.n == 1
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0


def test_rsb_immediate_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100010011100000001000000000000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, RsbImmediateA1)
    assert opcode.instruction == arm.opcode
    assert opcode.imm32 == 0
    assert opcode.d == 1
    assert opcode.n == 0
    assert opcode.setflags
    arm.registers.set(opcode.n, 5)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 4294967291
    assert arm.registers.cpsr.n == 1
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0
