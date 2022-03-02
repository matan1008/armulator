import pytest

from armulator.armv6.opcodes.concrete.isb_a1 import IsbA1
from armulator.armv6.opcodes.concrete.isb_t1 import IsbT1


def test_isb_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11110011101111111000111101101111
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, IsbT1)
    with pytest.raises(NotImplementedError):
        arm.emulate_cycle()


def test_isb_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11110101011111111111000001101111
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, IsbA1)
    with pytest.raises(NotImplementedError):
        arm.emulate_cycle()
