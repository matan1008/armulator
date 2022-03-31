from armulator.armv6.opcodes.concrete.sxth_a1 import SxthA1
from armulator.armv6.opcodes.concrete.sxth_t1 import SxthT1
from armulator.armv6.opcodes.concrete.sxth_t2 import SxthT2


def test_sxth_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b1011001000001000
    arm.opcode_len = 16
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == SxthT1
    assert opcode.instruction == arm.opcode
    assert opcode.m == 1
    assert opcode.d == 0
    assert opcode.rotation == 0
    arm.registers.set(1, 0x0000F000)
    arm.emulate_cycle()
    assert arm.registers.get(0) == 0xFFFFF000


def test_sxth_t2(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11111010000011111111001010010000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == SxthT2
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.d == 2
    assert opcode.rotation == 8
    arm.registers.set(opcode.m, 0x00F00000)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0xFFFFF000


def test_sxth_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100110101111110001010001110000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, SxthA1)
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.d == 1
    assert opcode.rotation == 8
    arm.registers.set(opcode.m, 0x00F00000)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0xFFFFF000
