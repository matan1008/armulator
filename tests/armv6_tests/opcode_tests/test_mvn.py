from armulator.armv6.opcodes.concrete.mvn_immediate_a1 import MvnImmediateA1
from armulator.armv6.opcodes.concrete.mvn_immediate_t1 import MvnImmediateT1
from armulator.armv6.opcodes.concrete.mvn_register_a1 import MvnRegisterA1
from armulator.armv6.opcodes.concrete.mvn_register_shifted_register_a1 import MvnRegisterShiftedRegisterA1
from armulator.armv6.opcodes.concrete.mvn_register_t1 import MvnRegisterT1
from armulator.armv6.opcodes.concrete.mvn_register_t2 import MvnRegisterT2
from armulator.armv6.shift import SRType


def test_mvn_register_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b0100001111000001
    arm.opcode_len = 16
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == MvnRegisterT1
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.d == 1
    assert opcode.shift_t == SRType.LSL
    assert opcode.shift_n == 0
    assert opcode.setflags
    arm.registers.set(0, 1)
    arm.emulate_cycle()
    assert arm.registers.get(1) == 0xfffffffe
    assert arm.registers.cpsr.n == 1
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0


def test_mvn_register_t2(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11101010011111110000000101000000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == MvnRegisterT2
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.d == 1
    assert opcode.shift_t == SRType.LSL
    assert opcode.shift_n == 1
    assert opcode.setflags
    arm.registers.set(0, 1)
    arm.emulate_cycle()
    assert arm.registers.get(1) == 0xfffffffd
    assert arm.registers.cpsr.n == 1
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0


def test_mvn_immediate_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11110000011111110000000100000010
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == MvnImmediateT1
    assert opcode.instruction == arm.opcode
    assert opcode.imm32 == 2
    assert opcode.d == 1
    assert opcode.setflags
    assert opcode.carry == 0
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0xfffffffd
    assert arm.registers.cpsr.n == 1
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0


def test_mvn_register_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100001111100010010000010000000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, MvnRegisterA1)
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.d == 2
    assert opcode.shift_t == SRType.LSL
    assert opcode.shift_n == 1
    assert opcode.setflags
    arm.registers.set(opcode.m, 1)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0xFFFFFFFD
    assert arm.registers.cpsr.n == 1
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0


def test_mvn_register_shifted_register_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100001111100000010000000010001
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, MvnRegisterShiftedRegisterA1)
    assert opcode.instruction == arm.opcode
    assert opcode.m == 1
    assert opcode.d == 2
    assert opcode.s == 0
    assert opcode.shift_t == SRType.LSL
    assert opcode.setflags
    arm.registers.set(opcode.m, 1)
    arm.registers.set(opcode.s, 1)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0xFFFFFFFD
    assert arm.registers.cpsr.n == 1
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0


def test_mvn_immediate_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100011111100000001000000000001
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, MvnImmediateA1)
    assert opcode.instruction == arm.opcode
    assert opcode.imm32 == 1
    assert opcode.d == 1
    assert opcode.carry == 0
    assert opcode.setflags
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0xFFFFFFFE
    assert arm.registers.cpsr.n == 1
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0
