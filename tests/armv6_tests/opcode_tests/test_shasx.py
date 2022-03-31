from armulator.armv6.opcodes.concrete.shasx_a1 import ShasxA1
from armulator.armv6.opcodes.concrete.shasx_t1 import ShasxT1


def test_shasx_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11111010101000011111001000100000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == ShasxT1
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.n == 1
    assert opcode.d == 2
    arm.registers.set(opcode.m, 0x0003FFFE)
    arm.registers.set(opcode.n, 0x00050005)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0x00010001


def test_shasx_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100110001100010010111100110000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, ShasxA1)
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.n == 1
    assert opcode.d == 2
    arm.registers.set(opcode.m, 0x0003FFFE)
    arm.registers.set(opcode.n, 0x00050005)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0x00010001
