from armulator.armv6.opcodes.concrete.qdadd_a1 import QdaddA1
from armulator.armv6.opcodes.concrete.qdadd_t1 import QdaddT1


def test_qdadd_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11111010100000001111001010010001
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == QdaddT1
    assert opcode.instruction == arm.opcode
    assert opcode.m == 1
    assert opcode.n == 0
    assert opcode.d == 2
    arm.registers.set(opcode.m, 0x7FFFFFFE)
    arm.registers.set(opcode.n, 0x3FFF0005)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0x7FFFFFFF
    assert arm.registers.cpsr.q == 1


def test_qdadd_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100001010000000010000001010001
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, QdaddA1)
    assert opcode.instruction == arm.opcode
    assert opcode.m == 1
    assert opcode.n == 0
    assert opcode.d == 2
    arm.registers.set(opcode.m, 0x7FFFFFFE)
    arm.registers.set(opcode.n, 0x3FFF0005)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0x7fffffff
    assert arm.registers.cpsr.q == 1
