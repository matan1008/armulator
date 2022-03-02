from armulator.armv6.opcodes.concrete.qsub_a1 import QsubA1
from armulator.armv6.opcodes.concrete.qsub_t1 import QsubT1


def test_qsub16_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11111010100000001111001010100001
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == QsubT1
    assert opcode.instruction == arm.opcode
    assert opcode.m == 1
    assert opcode.n == 0
    assert opcode.d == 2
    arm.registers.set(opcode.m, 0x0003FFFE)
    arm.registers.set(opcode.n, 0x80000005)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0x7fffffff
    assert arm.registers.cpsr.q == 1


def test_qsub_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100001001000000010000001010001
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, QsubA1)
    assert opcode.instruction == arm.opcode
    assert opcode.m == 1
    assert opcode.n == 0
    assert opcode.d == 2
    arm.registers.set(opcode.m, 0x0003FFFE)
    arm.registers.set(opcode.n, 0x80000005)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0x7fffffff
    assert arm.registers.cpsr.q == 1
