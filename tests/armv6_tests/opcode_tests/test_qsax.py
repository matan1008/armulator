from armulator.armv6.opcodes.concrete.qsax_a1 import QsaxA1
from armulator.armv6.opcodes.concrete.qsax_t1 import QsaxT1


def test_qsax_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11111010111000011111001000010000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == QsaxT1
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.n == 1
    assert opcode.d == 2
    arm.registers.set(opcode.m, 0x00030002)
    arm.registers.set(opcode.n, 0x80000005)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0x80000008


def test_qsax_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100110001000010010111101010000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, QsaxA1)
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.n == 1
    assert opcode.d == 2
    arm.registers.set(opcode.m, 0x00030002)
    arm.registers.set(opcode.n, 0x80000005)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0x80000008
