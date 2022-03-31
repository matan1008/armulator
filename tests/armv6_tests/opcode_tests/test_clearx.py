from armulator.armv6.opcodes.concrete.clrex_a1 import ClrexA1
from armulator.armv6.opcodes.concrete.clrex_t1 import ClrexT1


def test_clearx_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11110011101111111000111100101111
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, ClrexT1)
    arm.emulate_cycle()


def test_clearx_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11110101011111111111000000011111
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, ClrexA1)
    arm.emulate_cycle()
