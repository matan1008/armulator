from armulator.armv6.opcodes.concrete.qasx_a1 import QasxA1
from armulator.armv6.opcodes.concrete.qasx_t1 import QasxT1


def test_qasx_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11111010101000011111001000010000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == QasxT1
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.n == 1
    assert opcode.d == 2
    arm.registers.set(opcode.m, 0x0003FFFE)
    arm.registers.set(opcode.n, 0x80000005)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0x80000002


def test_qasx_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100110001000010010111100110000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, QasxA1)
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.n == 1
    assert opcode.d == 2
    arm.registers.set(opcode.m, 0x0003FFFE)
    arm.registers.set(opcode.n, 0x80000005)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0x80000002
