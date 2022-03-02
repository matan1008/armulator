from armulator.armv6.opcodes.concrete.wfi_a1 import WfiA1
from armulator.armv6.opcodes.concrete.wfi_t1 import WfiT1
from armulator.armv6.opcodes.concrete.wfi_t2 import WfiT2


def test_wfi_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b1011111100110000
    arm.opcode_len = 16
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, WfiT1)
    assert opcode.instruction == arm.opcode
    arm.emulate_cycle()


def test_wfi_t2(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11110011101011111000000000000011
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, WfiT2)
    assert opcode.instruction == arm.opcode
    arm.emulate_cycle()


def test_wfi_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100011001000001111000000000011
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, WfiA1)
    assert opcode.instruction == arm.opcode
    arm.emulate_cycle()
