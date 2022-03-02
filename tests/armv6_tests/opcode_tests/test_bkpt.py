import pytest

from armulator.armv6.opcodes.concrete.bkpt_a1 import BkptA1
from armulator.armv6.opcodes.concrete.bkpt_t1 import BkptT1


def test_bkpt_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b1011111000000001
    arm.opcode_len = 16
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, BkptT1)
    assert opcode.instruction == arm.opcode
    with pytest.raises(NotImplementedError):
        arm.emulate_cycle()


def test_bkpt_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100001001000000000000001110001
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, BkptA1)
    assert opcode.instruction == arm.opcode
    with pytest.raises(NotImplementedError):
        arm.emulate_cycle()
