import pytest

from armulator.armv6.opcodes.concrete.sub_immediate_arm_a1 import SubImmediateArmA1
from armulator.armv6.opcodes.concrete.sub_immediate_thumb_t1 import SubImmediateThumbT1
from armulator.armv6.opcodes.concrete.sub_immediate_thumb_t2 import SubImmediateThumbT2
from armulator.armv6.opcodes.concrete.sub_immediate_thumb_t3 import SubImmediateThumbT3
from armulator.armv6.opcodes.concrete.sub_immediate_thumb_t4 import SubImmediateThumbT4
from armulator.armv6.opcodes.concrete.sub_register_a1 import SubRegisterA1
from armulator.armv6.opcodes.concrete.sub_register_shifted_register_a1 import SubRegisterShiftedRegisterA1
from armulator.armv6.opcodes.concrete.sub_register_t1 import SubRegisterT1
from armulator.armv6.opcodes.concrete.sub_register_t2 import SubRegisterT2
from armulator.armv6.opcodes.concrete.sub_sp_minus_immediate_a1 import SubSpMinusImmediateA1
from armulator.armv6.opcodes.concrete.sub_sp_minus_immediate_t1 import SubSpMinusImmediateT1
from armulator.armv6.opcodes.concrete.sub_sp_minus_immediate_t2 import SubSpMinusImmediateT2
from armulator.armv6.opcodes.concrete.sub_sp_minus_immediate_t3 import SubSpMinusImmediateT3
from armulator.armv6.opcodes.concrete.sub_sp_minus_register_a1 import SubSpMinusRegisterA1
from armulator.armv6.opcodes.concrete.sub_sp_minus_register_t1 import SubSpMinusRegisterT1
from armulator.armv6.opcodes.concrete.subs_pc_lr_arm_a1 import SubsPcLrArmA1
from armulator.armv6.opcodes.concrete.subs_pc_lr_arm_a2 import SubsPcLrArmA2
from armulator.armv6.opcodes.concrete.subs_pc_lr_thumb_t1 import SubsPcLrThumbT1
from armulator.armv6.shift import SRType


def test_sub_register_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b0001101000001010
    arm.opcode_len = 16
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == SubRegisterT1
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.d == 2
    assert opcode.n == 1
    assert opcode.shift_t == SRType.LSL
    assert opcode.shift_n == 0
    assert opcode.setflags
    arm.registers.set(0, 4)
    arm.registers.set(1, 4)
    arm.emulate_cycle()
    assert arm.registers.get(2) == 0
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 1
    assert arm.registers.cpsr.c == 1
    assert arm.registers.cpsr.v == 0


def test_sub_immediate_thumb_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b0001111001001010
    arm.opcode_len = 16
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == SubImmediateThumbT1
    assert opcode.instruction == arm.opcode
    assert opcode.imm32 == 1
    assert opcode.d == 2
    assert opcode.n == 1
    assert opcode.setflags
    arm.registers.set(1, 4)
    arm.emulate_cycle()
    assert arm.registers.get(2) == 3
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 1
    assert arm.registers.cpsr.v == 0


def test_sub_immediate_thumb_t2(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b0011100000000001
    arm.opcode_len = 16
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == SubImmediateThumbT2
    assert opcode.instruction == arm.opcode
    assert opcode.imm32 == 1
    assert opcode.d == 0
    assert opcode.n == 0
    assert opcode.setflags
    arm.registers.set(0, 4)
    arm.emulate_cycle()
    assert arm.registers.get(0) == 3
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 1
    assert arm.registers.cpsr.v == 0


def test_sub_sp_minus_immediate_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b1011000010000001
    arm.opcode_len = 16
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == SubSpMinusImmediateT1
    assert opcode.instruction == arm.opcode
    assert opcode.imm32 == 4
    assert opcode.d == 13
    assert not opcode.setflags
    arm.registers.set(13, 4)
    arm.emulate_cycle()
    assert arm.registers.get(13) == 0
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0


def test_sub_sp_minus_register_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11101011101111010000000101000000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == SubSpMinusRegisterT1
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.d == 1
    assert opcode.shift_t == SRType.LSL
    assert opcode.shift_n == 1
    assert opcode.setflags
    arm.registers.set(0, 1)
    arm.registers.set(13, 4)
    arm.emulate_cycle()
    assert arm.registers.get(1) == 2
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 1
    assert arm.registers.cpsr.v == 0


def test_sub_register_t2(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11101011101100010000001001000000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == SubRegisterT2
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.d == 2
    assert opcode.n == 1
    assert opcode.shift_t == SRType.LSL
    assert opcode.shift_n == 1
    assert opcode.setflags
    arm.registers.set(0, 2)
    arm.registers.set(1, 4)
    arm.emulate_cycle()
    assert arm.registers.get(2) == 0
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 1
    assert arm.registers.cpsr.c == 1
    assert arm.registers.cpsr.v == 0


def test_sub_sp_minus_immediate_t2(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11110001101111010000000000000100
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == SubSpMinusImmediateT2
    assert opcode.instruction == arm.opcode
    assert opcode.imm32 == 4
    assert opcode.d == 0
    assert opcode.setflags
    arm.registers.set(13, 4)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 1
    assert arm.registers.cpsr.c == 1
    assert arm.registers.cpsr.v == 0


def test_sub_immediate_thumb_t3(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11110001101100000000000100000001
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == SubImmediateThumbT3
    assert opcode.instruction == arm.opcode
    assert opcode.imm32 == 1
    assert opcode.d == 1
    assert opcode.n == 0
    assert opcode.setflags
    arm.registers.set(opcode.n, 4)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 3
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 1
    assert arm.registers.cpsr.v == 0


def test_subw_sp_minus_immediate_t3(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11110010101011010000000000000100
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == SubSpMinusImmediateT3
    assert opcode.instruction == arm.opcode
    assert opcode.imm32 == 4
    assert opcode.d == 0
    assert not opcode.setflags
    arm.registers.set(13, 4)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0


def test_subw_immediate_thumb_t4(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11110010101000000000000100000001
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == SubImmediateThumbT4
    assert opcode.instruction == arm.opcode
    assert opcode.imm32 == 1
    assert opcode.d == 1
    assert opcode.n == 0
    assert not opcode.setflags
    arm.registers.set(opcode.n, 4)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 3
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0


def test_subs_pc_lr_thumb_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11110011110111101000111100000100
    prev_pc = 0x0F000000
    arm.registers.branch_to(prev_pc)
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, SubsPcLrThumbT1)
    assert opcode.imm32 == 4
    assert opcode.n == 14
    assert opcode.instruction == arm.opcode
    arm.registers.set_spsr(0b10001)
    arm.registers.set(14, 0x0000ff00)
    arm.emulate_cycle()
    assert arm.registers.pc_store_value() == 0x0000ff00 - 4


@pytest.mark.parametrize('instr, pc_opcode, m, pc, shift_t', [
    (0b11100000000100011111000010000000, 0b0000, 0x0000FF80, 0x0000FF00, SRType.LSL),
    (0b11100000001100011111000010000000, 0b0001, 0x00007800, 0x00000F00, SRType.LSL),
    (0b11100000010100011111000010000000, 0b0010, 0x00000780, 0x0000F000, SRType.LSL),
    (0b11100000011100011111000010000000, 0b0011, 0x00008700, 0x00000F00, SRType.LSL),
    (0b11100000100100011111000010000000, 0b0100, 0x00000078, 0x0000FFF0, SRType.LSL),
    (0b11100000101100011111000010000000, 0b0101, 0x00000078, 0x0000FFF0, SRType.LSL),
    (0b11100000110100011111000010000000, 0b0110, 0x0000077F, 0x0000F000, SRType.LSL),
    (0b11100000111100011111000010000000, 0b0111, 0x00008702, 0x00000F00, SRType.LSL),
    (0b11100001100100011111000010000000, 0b1100, 0x000007F8, 0x0000FFF0, SRType.LSL),
    (0b11100001101100011111000010000000, 0b1101, 0x00003300, 0x00006600, SRType.LSL),
    (0b11100001101100011111000010100000, 0b1101, 0xF0006600, 0x78003300, SRType.LSR),
    (0b11100001101100011111000011000000, 0b1101, 0xF0006600, 0xF8003300, SRType.ASR),
    (0b11100001101100011111000011100000, 0b1101, 0x40006601, 0xA0003300, SRType.ROR),
    (0b11100001110100011111000010000000, 0b1110, 0x00000C00, 0x0000E700, SRType.LSL),
    (0b11100001111100011111000010000000, 0b1111, 0x00003300, 0xFFFF99FC, SRType.LSL),
])
def test_subs_pc_lr_arm_a2(arm_v6_without_fetch, instr, pc_opcode, m, pc, shift_t):
    arm = arm_v6_without_fetch
    arm.opcode = instr
    prev_pc = 0x0F000000
    arm.registers.branch_to(prev_pc)
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, SubsPcLrArmA2)
    assert opcode.instruction == arm.opcode
    assert opcode.register_form
    assert opcode.n == 1
    assert opcode.opcode == pc_opcode
    assert opcode.m == 0
    assert opcode.shift_t == shift_t
    assert opcode.shift_n == 1
    arm.registers.set_spsr(0b10001)
    arm.registers.set(opcode.n, 0x0000FF00)
    arm.registers.set(opcode.m, m)
    arm.emulate_cycle()
    assert arm.registers.pc_store_value() == pc


def test_sub_sp_minus_register_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100000010111010010000010000000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, SubSpMinusRegisterA1)
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.d == 2
    assert opcode.shift_t == SRType.LSL
    assert opcode.shift_n == 1
    assert opcode.setflags
    arm.registers.set(opcode.m, 1)
    arm.registers.set(13, 4)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 2
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 1
    assert arm.registers.cpsr.v == 0


def test_sub_register_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100000010100010010000010000000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, SubRegisterA1)
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.d == 2
    assert opcode.n == 1
    assert opcode.shift_t == SRType.LSL
    assert opcode.shift_n == 1
    assert opcode.setflags
    arm.registers.set(opcode.n, 4)
    arm.registers.set(opcode.m, 2)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 1
    assert arm.registers.cpsr.c == 1
    assert arm.registers.cpsr.v == 0


def test_sub_register_shifted_register_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100000010100010010001100010000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, SubRegisterShiftedRegisterA1)
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.d == 2
    assert opcode.n == 1
    assert opcode.s == 3
    assert opcode.shift_t == SRType.LSL
    assert opcode.setflags
    arm.registers.set(opcode.n, 4)
    arm.registers.set(opcode.m, 2)
    arm.registers.set(opcode.s, 1)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 1
    assert arm.registers.cpsr.c == 1
    assert arm.registers.cpsr.v == 0


@pytest.mark.parametrize('instr, pc_opcode, n, imm32, pc', [
    (0b11100010000100001111111011110000, 0b0000, 0xFF00, 0xF00, 0x00000F00),
    (0b11100010001100001111111011110000, 0b0001, 0xFF00, 0xF00, 0x0000F000),
    (0b11100010010100001111111010000000, 0b0010, 0x10000, 0x800, 0x0000F800),
    (0b11100010011100001111111011110000, 0b0011, 0x80, 0xF00, 0x00000E80),
    (0b11100010100100001111111011110000, 0b0100, 0xF100, 0xF00, 0x10000),
    (0b11100010101100001111111011110000, 0b0101, 0xF100, 0xF00, 0x10000),
    (0b11100010110100001111111010000000, 0b0110, 0x10001, 0x800, 0x0000F800),
    (0b11100010111100001111111011110000, 0b0111, 0x7F, 0xF00, 0x00000E80),
    (0b11100011100100001111111011110000, 0b1100, 0xF800, 0xF00, 0x0000FF00),
    (0b11100011101100001111111011110000, 0b1101, 0xF800, 0xF00, 0xF00),
    (0b11100011110100001111111011110000, 0b1110, 0xF800, 0xF00, 0x0000F000),
    (0b11100011111100001111111011110000, 0b1111, 0xF800, 0xF00, 0xFFFFF0FC),
])
def test_subs_pc_lr_arm_a1(arm_v6_without_fetch, instr, pc_opcode, n, imm32, pc):
    arm = arm_v6_without_fetch
    arm.opcode = instr
    prev_pc = 0x0000FF00
    arm.registers.branch_to(prev_pc)
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, SubsPcLrArmA1)
    assert opcode.instruction == arm.opcode
    assert not opcode.register_form
    assert opcode.n == 0
    assert opcode.opcode == pc_opcode
    assert opcode.imm32 == imm32
    arm.registers.set_spsr(0b10001)
    arm.registers.set(opcode.n, n)
    arm.emulate_cycle()
    assert arm.registers.pc_store_value() == pc


def test_sub_sp_minus_immediate_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100010010111010001000000000100
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, SubSpMinusImmediateA1)
    assert opcode.instruction == arm.opcode
    assert opcode.imm32 == 4
    assert opcode.d == 1
    assert opcode.setflags
    arm.registers.set(13, 4)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 1
    assert arm.registers.cpsr.c == 1
    assert arm.registers.cpsr.v == 0


def test_sub_immediate_arm_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100010010100000001000000000001
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, SubImmediateArmA1)
    assert opcode.instruction == arm.opcode
    assert opcode.imm32 == 1
    assert opcode.d == 1
    assert opcode.n == 0
    assert opcode.setflags
    arm.registers.set(opcode.n, 4)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 3
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 1
    assert arm.registers.cpsr.v == 0
