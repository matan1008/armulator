from armulator.armv6.opcodes.concrete.nop_a1 import NopA1
from armulator.armv6.opcodes.concrete.nop_t1 import NopT1
from armulator.armv6.opcodes.concrete.nop_t2 import NopT2


def test_nop_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b1011111100000000
    arm.opcode_len = 16
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, NopT1)
    assert opcode.instruction == arm.opcode
    arm.emulate_cycle()


def test_nop_t2(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11110011101011111000000000000000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, NopT2)
    assert opcode.instruction == arm.opcode
    arm.emulate_cycle()


def test_nop_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100011001000001111000000000000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, NopA1)
    assert opcode.instruction == arm.opcode
    arm.emulate_cycle()
