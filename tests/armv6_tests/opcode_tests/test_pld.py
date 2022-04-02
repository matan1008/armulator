import pytest

from armulator.armv6.opcodes.concrete.pld_immediate_a1 import PldImmediateA1
from armulator.armv6.opcodes.concrete.pld_immediate_t1 import PldImmediateT1
from armulator.armv6.opcodes.concrete.pld_immediate_t2 import PldImmediateT2
from armulator.armv6.opcodes.concrete.pld_literal_a1 import PldLiteralA1
from armulator.armv6.opcodes.concrete.pld_literal_t1 import PldLiteralT1
from armulator.armv6.opcodes.concrete.pld_register_a1 import PldRegisterA1
from armulator.armv6.opcodes.concrete.pld_register_t1 import PldRegisterT1
from armulator.armv6.shift import SRType


@pytest.mark.parametrize('instruction, is_pldw', [
    (0b11111000000100011111000000000000, 0),
    (0b11111000001100011111000000000000, 1),
])
def test_pld_register_t1(thumb_v6_without_fetch, instruction, is_pldw):
    arm = thumb_v6_without_fetch
    arm.opcode = instruction
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, PldRegisterT1)
    assert opcode.instruction == arm.opcode
    assert opcode.add
    assert opcode.is_pldw == is_pldw
    assert opcode.m == 0
    assert opcode.n == 1
    assert opcode.shift_t == SRType.LSL
    assert opcode.shift_n == 0
    with pytest.raises(NotImplementedError):
        arm.emulate_cycle()


@pytest.mark.parametrize('instruction', [
    0b11111000000111111111000000000000,
    0b11111000001111111111000000000000,
])
def test_pld_literal_t1(thumb_v6_without_fetch, instruction):
    arm = thumb_v6_without_fetch
    arm.opcode = instruction
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, PldLiteralT1)
    assert opcode.instruction == arm.opcode
    assert not opcode.add
    assert opcode.imm32 == 0
    with pytest.raises(NotImplementedError):
        arm.emulate_cycle()


@pytest.mark.parametrize('instruction, is_pldw', [
    (0b11111000000100011111110000000000, 0),
    (0b11111000001100011111110000000000, 1),
])
def test_pld_immediate_t2(thumb_v6_without_fetch, instruction, is_pldw):
    arm = thumb_v6_without_fetch
    arm.opcode = instruction
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, PldImmediateT2)
    assert opcode.instruction == arm.opcode
    assert not opcode.add
    assert opcode.imm32 == 0
    assert opcode.is_pldw == is_pldw
    assert opcode.n == 1
    with pytest.raises(NotImplementedError):
        arm.emulate_cycle()


@pytest.mark.parametrize('instruction, is_pldw', [
    (0b11111000100100001111000000000000, 0),
    (0b11111000101100001111000000000000, 1),
])
def test_pld_immediate_t1(thumb_v6_without_fetch, instruction, is_pldw):
    arm = thumb_v6_without_fetch
    arm.opcode = instruction
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, PldImmediateT1)
    assert opcode.instruction == arm.opcode
    assert opcode.add
    assert opcode.imm32 == 0
    assert opcode.is_pldw == is_pldw
    assert opcode.n == 0
    with pytest.raises(NotImplementedError):
        arm.emulate_cycle()


def test_pld_immediate_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11110101110100001111000000000000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, PldImmediateA1)
    assert opcode.instruction == arm.opcode
    assert opcode.add
    assert opcode.imm32 == 0
    assert not opcode.is_pldw
    assert opcode.n == 0
    with pytest.raises(NotImplementedError):
        arm.emulate_cycle()


def test_pld_literal_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11110101110111111111000000000000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, PldLiteralA1)
    assert opcode.instruction == arm.opcode
    assert opcode.add
    assert opcode.imm32 == 0
    with pytest.raises(NotImplementedError):
        arm.emulate_cycle()


def test_pld_register_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11110111110100011111000000000000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, PldRegisterA1)
    assert opcode.instruction == arm.opcode
    assert opcode.add
    assert not opcode.is_pldw
    assert opcode.m == 0
    assert opcode.n == 1
    assert opcode.shift_t == SRType.LSL
    assert opcode.shift_n == 0
    with pytest.raises(NotImplementedError):
        arm.emulate_cycle()
