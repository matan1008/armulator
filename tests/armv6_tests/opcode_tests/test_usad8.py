from armulator.armv6.opcodes.concrete.usad8_a1 import Usad8A1
from armulator.armv6.opcodes.concrete.usad8_t1 import Usad8T1


def test_usad8_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11111011011100101111001100000001
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, Usad8T1)
    assert opcode.instruction == arm.opcode
    assert opcode.m == 1
    assert opcode.n == 2
    assert opcode.d == 3
    arm.registers.set(opcode.m, 0x00030004)
    arm.registers.set(opcode.n, 0x0001FFFF)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 508


def test_usad8_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100111100000101111000000010001
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, Usad8A1)
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.n == 1
    assert opcode.d == 2
    arm.registers.set(opcode.m, 0x00030004)
    arm.registers.set(opcode.n, 0x0001FFFF)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 508
