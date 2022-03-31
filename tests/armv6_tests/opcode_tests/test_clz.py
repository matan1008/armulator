from armulator.armv6.opcodes.concrete.clz_a1 import ClzA1
from armulator.armv6.opcodes.concrete.clz_t1 import ClzT1


def test_clz_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11111010101100011111001010000001
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == ClzT1
    assert opcode.instruction == arm.opcode
    assert opcode.m == 1
    assert opcode.d == 2
    arm.registers.set(opcode.m, 0x03BBCCDD)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 6


def test_clz_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100001011011110010111100010001
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, ClzA1)
    assert opcode.instruction == arm.opcode
    assert opcode.m == 1
    assert opcode.d == 2
    arm.registers.set(opcode.m, 0x03BBCCDD)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 6
