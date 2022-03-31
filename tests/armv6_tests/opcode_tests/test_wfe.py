from armulator.armv6.opcodes.concrete.wfe_a1 import WfeA1
from armulator.armv6.opcodes.concrete.wfe_t1 import WfeT1
from armulator.armv6.opcodes.concrete.wfe_t2 import WfeT2


def test_wfe_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b1011111100100000
    arm.opcode_len = 16
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, WfeT1)
    assert opcode.instruction == arm.opcode
    arm.emulate_cycle()


def test_wfe_t2(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11110011101011111000000000000010
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, WfeT2)
    assert opcode.instruction == arm.opcode
    arm.emulate_cycle()


def test_wfe_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100011001000001111000000000010
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, WfeA1)
    assert opcode.instruction == arm.opcode
    arm.emulate_cycle()
