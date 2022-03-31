from armulator.armv6.opcodes.concrete.uxth_a1 import UxthA1
from armulator.armv6.opcodes.concrete.uxth_t1 import UxthT1
from armulator.armv6.opcodes.concrete.uxth_t2 import UxthT2


def test_uxth_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b1011001010001000
    arm.opcode_len = 16
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == UxthT1
    assert opcode.instruction == arm.opcode
    assert opcode.m == 1
    assert opcode.d == 0
    assert opcode.rotation == 0
    arm.registers.set(1, 0xFFFFF000)
    arm.emulate_cycle()
    assert arm.registers.get(0) == 0x0000F000


def test_uxth_t2(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11111010000111111111001010010000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == UxthT2
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.d == 2
    assert opcode.rotation == 8
    arm.registers.set(opcode.m, 0x00F00000)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0x0000F000


def test_uxth_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100110111111110001010001110000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, UxthA1)
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.d == 1
    assert opcode.rotation == 8
    arm.registers.set(opcode.m, 0x00F00000)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0x0000F000
