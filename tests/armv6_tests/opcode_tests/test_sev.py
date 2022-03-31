import pytest

from armulator.armv6.opcodes.concrete.sev_a1 import SevA1
from armulator.armv6.opcodes.concrete.sev_t1 import SevT1


def test_sev_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b1011111101000000
    arm.opcode_len = 16
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, SevT1)
    assert opcode.instruction == arm.opcode
    with pytest.raises(NotImplementedError):
        arm.emulate_cycle()


def test_sev_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100011001000001111000000000100
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, SevA1)
    assert opcode.instruction == arm.opcode
    with pytest.raises(NotImplementedError):
        arm.emulate_cycle()
