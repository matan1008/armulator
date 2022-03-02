from armulator.armv6.opcodes.concrete.uqsub16_a1 import Uqsub16A1
from armulator.armv6.opcodes.concrete.uqsub16_t1 import Uqsub16T1


def test_uqsub16_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11111010110100011111001001010000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == Uqsub16T1
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.n == 1
    assert opcode.d == 2
    arm.registers.set(opcode.m, 0x0003FFFE)
    arm.registers.set(opcode.n, 0x80000005)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0x7FFD0000


def test_uqsub16_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100110011000010010111101110000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, Uqsub16A1)
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.n == 1
    assert opcode.d == 2
    arm.registers.set(opcode.m, 0x0003FFFE)
    arm.registers.set(opcode.n, 0x80000005)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0x7FFD0000
