import pytest

from armulator.armv6.opcodes.concrete.yield_a1 import YieldA1
from armulator.armv6.opcodes.concrete.yield_t1 import YieldT1
from armulator.armv6.opcodes.concrete.yield_t2 import YieldT2


def test_yield_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b1011111100010000
    arm.opcode_len = 16
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, YieldT1)
    assert opcode.instruction == arm.opcode
    with pytest.raises(NotImplementedError):
        arm.emulate_cycle()


def test_yield_t2(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11110011101011111000000000000001
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, YieldT2)
    assert opcode.instruction == arm.opcode
    with pytest.raises(NotImplementedError):
        arm.emulate_cycle()


def test_yield_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100011001000001111000000000001
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, YieldA1)
    assert opcode.instruction == arm.opcode
    with pytest.raises(NotImplementedError):
        arm.emulate_cycle()
