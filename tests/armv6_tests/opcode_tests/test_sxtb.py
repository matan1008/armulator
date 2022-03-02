from armulator.armv6.opcodes.concrete.sxtb_a1 import SxtbA1
from armulator.armv6.opcodes.concrete.sxtb_t1 import SxtbT1
from armulator.armv6.opcodes.concrete.sxtb_t2 import SxtbT2


def test_sxtb_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b1011001001001000
    arm.opcode_len = 16
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == SxtbT1
    assert opcode.instruction == arm.opcode
    assert opcode.m == 1
    assert opcode.d == 0
    assert opcode.rotation == 0
    arm.registers.set(1, 0x000000F0)
    arm.emulate_cycle()
    assert arm.registers.get(0) == 0xFFFFFFF0


def test_sxtb_t2(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11111010010011111111001010010000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == SxtbT2
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.d == 2
    assert opcode.rotation == 8
    arm.registers.set(opcode.m, 0x0000F000)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0xFFFFFFF0


def test_sxtb_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100110101011110001010001110000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, SxtbA1)
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.d == 1
    assert opcode.rotation == 8
    arm.registers.set(opcode.m, 0x0000F000)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0xFFFFFFF0
