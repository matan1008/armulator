import pytest

from armulator.armv6.opcodes.concrete.dsb_a1 import DsbA1
from armulator.armv6.opcodes.concrete.dsb_t1 import DsbT1


def test_dsb_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11110011101111111000111101001111
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, DsbT1)
    assert opcode.option == 0b1111
    with pytest.raises(NotImplementedError):
        arm.emulate_cycle()


def test_dsb_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11110101011111111111000001001111
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, DsbA1)
    assert opcode.option == 0b1111
    with pytest.raises(NotImplementedError):
        arm.emulate_cycle()
