import pytest

from armulator.armv6.arm_exceptions import UndefinedInstructionException
from armulator.armv6.opcodes.concrete.udf_a1 import UdfA1
from armulator.armv6.opcodes.concrete.udf_t1 import UdfT1
from armulator.armv6.opcodes.concrete.udf_t2 import UdfT2


def test_udf_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b1101111000000100
    arm.opcode_len = 16
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == UdfT1
    assert opcode.instruction == arm.opcode
    arm.registers.branch_to(0x0F000000)
    arm.emulate_cycle()
    assert arm.registers.pc_store_value() == 0x00000004


def test_thumb32_undefined(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11101100000000010000001000010000
    arm.opcode_len = 32
    with pytest.raises(UndefinedInstructionException):
        arm.decode_instruction(arm.opcode)
    arm.registers.branch_to(0x0F000000)
    arm.emulate_cycle()
    assert arm.registers.pc_store_value() == 0x00000004


def test_udf_t2(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11110111111100001010000000000000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, UdfT2)
    assert opcode.instruction == arm.opcode
    arm.registers.branch_to(0x0F000000)
    arm.emulate_cycle()
    assert arm.registers.pc_store_value() == 0x00000004


def test_thumb32_undefined_2(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11111000011100000000000000000000
    arm.opcode_len = 32
    with pytest.raises(UndefinedInstructionException):
        arm.decode_instruction(arm.opcode)
    arm.registers.branch_to(0x0F000000)
    arm.emulate_cycle()
    assert arm.registers.pc_store_value() == 0x00000004


def test_udf_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100111111100000000000011110000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, UdfA1)
    assert opcode.instruction == arm.opcode
    arm.registers.branch_to(0x0F000000)
    arm.emulate_cycle()
    assert arm.registers.pc_store_value() == 0x00000004


def test_arm_undefined_1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11101100000111110000111100001111
    arm.opcode_len = 32
    with pytest.raises(UndefinedInstructionException):
        arm.decode_instruction(arm.opcode)
    arm.registers.branch_to(0x0F000000)
    arm.emulate_cycle()
    assert arm.registers.pc_store_value() == 0x00000004


def test_arm_undefined_2(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11110111111100000000000011110000
    arm.opcode_len = 32
    with pytest.raises(UndefinedInstructionException):
        arm.decode_instruction(arm.opcode)
    arm.registers.branch_to(0x0F000000)
    arm.emulate_cycle()
    assert arm.registers.pc_store_value() == 0x00000004
