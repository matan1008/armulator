from armulator.armv6.opcodes.concrete.add_immediate_arm_a1 import AddImmediateArmA1
from armulator.armv6.opcodes.concrete.add_immediate_thumb_t1 import AddImmediateThumbT1
from armulator.armv6.opcodes.concrete.add_immediate_thumb_t2 import AddImmediateThumbT2
from armulator.armv6.opcodes.concrete.add_immediate_thumb_t3 import AddImmediateThumbT3
from armulator.armv6.opcodes.concrete.add_immediate_thumb_t4 import AddImmediateThumbT4
from armulator.armv6.opcodes.concrete.add_register_arm_a1 import AddRegisterArmA1
from armulator.armv6.opcodes.concrete.add_register_shifted_register_a1 import AddRegisterShiftedRegisterA1
from armulator.armv6.opcodes.concrete.add_register_thumb_t1 import AddRegisterThumbT1
from armulator.armv6.opcodes.concrete.add_register_thumb_t2 import AddRegisterThumbT2
from armulator.armv6.opcodes.concrete.add_register_thumb_t3 import AddRegisterThumbT3
from armulator.armv6.opcodes.concrete.add_sp_plus_immediate_a1 import AddSpPlusImmediateA1
from armulator.armv6.opcodes.concrete.add_sp_plus_immediate_t1 import AddSpPlusImmediateT1
from armulator.armv6.opcodes.concrete.add_sp_plus_immediate_t2 import AddSpPlusImmediateT2
from armulator.armv6.opcodes.concrete.add_sp_plus_immediate_t3 import AddSpPlusImmediateT3
from armulator.armv6.opcodes.concrete.add_sp_plus_immediate_t4 import AddSpPlusImmediateT4
from armulator.armv6.opcodes.concrete.add_sp_plus_register_arm_a1 import AddSpPlusRegisterArmA1
from armulator.armv6.opcodes.concrete.add_sp_plus_register_thumb_t1 import AddSpPlusRegisterThumbT1
from armulator.armv6.opcodes.concrete.add_sp_plus_register_thumb_t2 import AddSpPlusRegisterThumbT2
from armulator.armv6.opcodes.concrete.add_sp_plus_register_thumb_t3 import AddSpPlusRegisterThumbT3
from armulator.armv6.shift import SRType


def test_add_register_thumb_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b0001100000001010
    arm.opcode_len = 16
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == AddRegisterThumbT1
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.d == 2
    assert opcode.n == 1
    assert opcode.shift_t == SRType.LSL
    assert opcode.shift_n == 0
    assert opcode.setflags
    arm.registers.set(0, 5)
    arm.registers.set(1, 4)
    arm.emulate_cycle()
    assert arm.registers.get(2) == 9
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0


def test_add_immediate_thumb_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b0001110001001010
    arm.opcode_len = 16
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == AddImmediateThumbT1
    assert opcode.instruction == arm.opcode
    assert opcode.imm32 == 1
    assert opcode.d == 2
    assert opcode.n == 1
    assert opcode.setflags
    arm.registers.set(1, 4)
    arm.emulate_cycle()
    assert arm.registers.get(2) == 5
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0


def test_add_immediate_thumb_t2(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b0011000000000001
    arm.opcode_len = 16
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == AddImmediateThumbT2
    assert opcode.instruction == arm.opcode
    assert opcode.imm32 == 1
    assert opcode.d == 0
    assert opcode.n == 0
    assert opcode.setflags
    arm.registers.set(0, 4)
    arm.emulate_cycle()
    assert arm.registers.get(0) == 5
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0


def test_add_sp_plus_register_thumb_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b0100010011101001
    arm.opcode_len = 16
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == AddSpPlusRegisterThumbT1
    assert opcode.instruction == arm.opcode
    assert opcode.m == 9
    assert opcode.d == 9
    assert opcode.shift_t == SRType.LSL
    assert opcode.shift_n == 0
    assert not opcode.setflags
    arm.registers.set(9, 6)
    arm.registers.set(13, 4)
    arm.emulate_cycle()
    assert arm.registers.get(9) == 10
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0


def test_add_sp_plus_register_thumb_t2(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b0100010010001101
    arm.opcode_len = 16
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == AddSpPlusRegisterThumbT2
    assert opcode.instruction == arm.opcode
    assert opcode.m == 1
    assert opcode.d == 13
    assert opcode.shift_t == SRType.LSL
    assert opcode.shift_n == 0
    assert not opcode.setflags
    arm.registers.set(1, 6)
    arm.registers.set(13, 4)
    arm.emulate_cycle()
    assert arm.registers.get(13) == 10
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0


def test_add_register_thumb_t2(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b0100010000000001
    arm.opcode_len = 16
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == AddRegisterThumbT2
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.d == 1
    assert opcode.n == 1
    assert opcode.shift_t == SRType.LSL
    assert opcode.shift_n == 0
    assert not opcode.setflags
    arm.registers.set(0, 5)
    arm.registers.set(1, 4)
    arm.emulate_cycle()
    assert arm.registers.get(1) == 9
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0


def test_add_sp_plus_immediate_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b1010100000000001
    arm.opcode_len = 16
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == AddSpPlusImmediateT1
    assert opcode.instruction == arm.opcode
    assert opcode.imm32 == 4
    assert opcode.d == 0
    assert not opcode.setflags
    arm.registers.set(13, 4)
    arm.emulate_cycle()
    assert arm.registers.get(0) == 8
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0


def test_add_sp_plus_immediate_t2(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b1011000000000001
    arm.opcode_len = 16
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == AddSpPlusImmediateT2
    assert opcode.instruction == arm.opcode
    assert opcode.imm32 == 4
    assert opcode.d == 13
    assert not opcode.setflags
    arm.registers.set(13, 4)
    arm.emulate_cycle()
    assert arm.registers.get(13) == 8
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0


def test_add_sp_plus_register_thumb_t3(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11101011000111010000000101000000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == AddSpPlusRegisterThumbT3
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.d == 1
    assert opcode.shift_t == SRType.LSL
    assert opcode.shift_n == 1
    assert opcode.setflags
    arm.registers.set(0, 3)
    arm.registers.set(13, 4)
    arm.emulate_cycle()
    assert arm.registers.get(1) == 10
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0


def test_add_register_thumb_t3(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11101011000100010000001001000000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == AddRegisterThumbT3
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.d == 2
    assert opcode.n == 1
    assert opcode.shift_t == SRType.LSL
    assert opcode.shift_n == 1
    assert opcode.setflags
    arm.registers.set(0, 3)
    arm.registers.set(1, 4)
    arm.emulate_cycle()
    assert arm.registers.get(2) == 10
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0


def test_add_sp_plus_immediate_t3(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11110001000111010000000000000100
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == AddSpPlusImmediateT3
    assert opcode.instruction == arm.opcode
    assert opcode.imm32 == 4
    assert opcode.d == 0
    assert opcode.setflags
    arm.registers.set(13, 4)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 8
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0


def test_add_immediate_thumb_t3(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11110001000100000000000100000001
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == AddImmediateThumbT3
    assert opcode.instruction == arm.opcode
    assert opcode.imm32 == 1
    assert opcode.d == 1
    assert opcode.n == 0
    assert opcode.setflags
    arm.registers.set(opcode.n, 4)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 5
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0


def test_add_sp_plus_immediate_t4(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11110010000011010000000000000100
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == AddSpPlusImmediateT4
    assert opcode.instruction == arm.opcode
    assert opcode.imm32 == 4
    assert opcode.d == 0
    assert not opcode.setflags
    arm.registers.set(13, 4)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 8
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0


def test_addw_immediate_thumb_t4(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11110010000000000000000100000001
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == AddImmediateThumbT4
    assert opcode.instruction == arm.opcode
    assert opcode.imm32 == 1
    assert opcode.d == 1
    assert opcode.n == 0
    assert not opcode.setflags
    arm.registers.set(opcode.n, 4)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 5
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0


def test_add_sp_plus_immediate_arm_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100000100111010010000010000000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, AddSpPlusRegisterArmA1)
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.d == 2
    assert opcode.shift_t == SRType.LSL
    assert opcode.shift_n == 1
    assert opcode.setflags
    arm.registers.set(13, 4)
    arm.registers.set(opcode.m, 2)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 8
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0


def test_add_register_arm_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100000100100010010000010000000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, AddRegisterArmA1)
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.d == 2
    assert opcode.n == 1
    assert opcode.shift_t == SRType.LSL
    assert opcode.shift_n == 1
    assert opcode.setflags
    arm.registers.set(opcode.n, 5)
    arm.registers.set(opcode.m, 1)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 7
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0


def test_add_register_shifted_register_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100000100100010010001100010000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, AddRegisterShiftedRegisterA1)
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.d == 2
    assert opcode.n == 1
    assert opcode.s == 3
    assert opcode.shift_t == SRType.LSL
    assert opcode.setflags
    arm.registers.set(opcode.n, 5)
    arm.registers.set(opcode.m, 1)
    arm.registers.set(opcode.s, 1)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 7
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0


def test_add_sp_plus_immediate_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100010100111010001000000000100
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, AddSpPlusImmediateA1)
    assert opcode.instruction == arm.opcode
    assert opcode.imm32 == 4
    assert opcode.d == 1
    assert opcode.setflags
    arm.registers.set(13, 4)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 8
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0


def test_add_immediate_arm_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100010100100000001000000000001
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, AddImmediateArmA1)
    assert opcode.instruction == arm.opcode
    assert opcode.imm32 == 1
    assert opcode.d == 1
    assert opcode.n == 0
    assert opcode.setflags
    arm.registers.set(opcode.n, 4)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 5
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0
