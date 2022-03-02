from armulator.armv6.opcodes.concrete.rev_a1 import RevA1
from armulator.armv6.opcodes.concrete.rev_t1 import RevT1
from armulator.armv6.opcodes.concrete.rev_t2 import RevT2


def test_rev_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b1011101000001000
    arm.opcode_len = 16
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == RevT1
    assert opcode.instruction == arm.opcode
    assert opcode.m == 1
    assert opcode.d == 0
    arm.registers.set(1, 0xAABBCCDD)
    arm.emulate_cycle()
    assert arm.registers.get(0) == 0xDDCCBBAA


def test_rev_t2(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11111010100100011111001010000001
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == RevT2
    assert opcode.instruction == arm.opcode
    assert opcode.m == 1
    assert opcode.d == 2
    arm.registers.set(opcode.m, 0xAABBCCDD)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0xDDCCBBAA


def test_rev_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100110101111110001111100110000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, RevA1)
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.d == 1
    arm.registers.set(opcode.m, 0xAABBCCDD)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0xDDCCBBAA
