from armulator.armv6.opcodes.concrete.sxtab16_a1 import Sxtab16A1
from armulator.armv6.opcodes.concrete.sxtab16_t1 import Sxtab16T1


def test_sxtab16_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11111010001000011111001010010000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == Sxtab16T1
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.d == 2
    assert opcode.n == 1
    assert opcode.rotation == 8
    arm.registers.set(opcode.m, 0xfefffeff)
    arm.registers.set(opcode.n, 0x00050005)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0x00030003


def test_sxtab16_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100110100000010010010001110000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, Sxtab16A1)
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.d == 2
    assert opcode.n == 1
    assert opcode.rotation == 8
    arm.registers.set(opcode.m, 0xfefffeff)
    arm.registers.set(opcode.n, 0x00050005)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0x00030003
