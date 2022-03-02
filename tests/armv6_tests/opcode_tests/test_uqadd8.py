from armulator.armv6.opcodes.concrete.uqadd8_a1 import Uqadd8A1
from armulator.armv6.opcodes.concrete.uqadd8_t1 import Uqadd8T1


def test_uqadd8_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11111010100000011111001001010000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == Uqadd8T1
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.n == 1
    assert opcode.d == 2
    arm.registers.set(opcode.m, 0x0103FFFE)
    arm.registers.set(opcode.n, 0x7F04FF05)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0x8007FFFF


def test_uqadd8_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100110011000010010111110010000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, Uqadd8A1)
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.n == 1
    assert opcode.d == 2
    arm.registers.set(opcode.m, 0x0103FFFE)
    arm.registers.set(opcode.n, 0x7F04FF05)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0x8007FFFF
