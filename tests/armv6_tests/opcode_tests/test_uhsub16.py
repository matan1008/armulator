from armulator.armv6.opcodes.concrete.uhsub16_a1 import Uhsub16A1
from armulator.armv6.opcodes.concrete.uhsub16_t1 import Uhsub16T1


def test_uhsub16_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11111010110100011111001001100000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == Uhsub16T1
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.n == 1
    assert opcode.d == 2
    arm.registers.set(opcode.m, 0x0003FFFE)
    arm.registers.set(opcode.n, 0xFFF00005)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0x7FF68003


def test_uhsub16_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100110011100010010111101110000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, Uhsub16A1)
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.n == 1
    assert opcode.d == 2
    arm.registers.set(opcode.m, 0x0003FFFE)
    arm.registers.set(opcode.n, 0xFFF00005)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0x7FF68003
