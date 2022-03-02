from armulator.armv6.opcodes.concrete.udiv_a1 import UdivA1
from armulator.armv6.opcodes.concrete.udiv_t1 import UdivT1


def test_udiv_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11111011101100010011001011110000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, UdivT1)
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.n == 1
    assert opcode.d == 2
    arm.registers.set(opcode.m, 0x00000004)
    arm.registers.set(opcode.n, 0xFFFFFFFD)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0x3FFFFFFF


def test_udiv_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100111001100101111000000010001
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, UdivA1)
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.n == 1
    assert opcode.d == 2
    arm.registers.set(opcode.m, 0x00000004)
    arm.registers.set(opcode.n, 0xFFFFFFFD)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0x3FFFFFFF
