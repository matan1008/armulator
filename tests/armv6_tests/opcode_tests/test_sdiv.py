from armulator.armv6.opcodes.concrete.sdiv_a1 import SdivA1
from armulator.armv6.opcodes.concrete.sdiv_t1 import SdivT1


def test_sdiv_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11111011100100010011001011110000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, SdivT1)
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.n == 1
    assert opcode.d == 2
    arm.registers.set(opcode.m, 0xFFFFFFFD)
    arm.registers.set(opcode.n, 0x00000004)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0xFFFFFFFF


def test_sdiv_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100111000100101111000000010001
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, SdivA1)
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.n == 1
    assert opcode.d == 2
    arm.registers.set(opcode.m, 0xFFFFFFFD)
    arm.registers.set(opcode.n, 0x00000004)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0xFFFFFFFF
