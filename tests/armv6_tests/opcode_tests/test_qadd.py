from armulator.armv6.opcodes.concrete.qadd_a1 import QaddA1
from armulator.armv6.opcodes.concrete.qadd_t1 import QaddT1


def test_qadd_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11111010100000001111001010000001
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == QaddT1
    assert opcode.instruction == arm.opcode
    assert opcode.m == 1
    assert opcode.n == 0
    assert opcode.d == 2
    arm.registers.set(opcode.m, 0x7FFFFFFE)
    arm.registers.set(opcode.n, 0x7FFF0005)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0x7FFFFFFF
    assert arm.registers.cpsr.q == 1


def test_qadd_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100001000000000010000001010001
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, QaddA1)
    assert opcode.instruction == arm.opcode
    assert opcode.m == 1
    assert opcode.n == 0
    assert opcode.d == 2
    arm.registers.set(opcode.m, 0x7FFFFFFE)
    arm.registers.set(opcode.n, 0x7FFF0005)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0x7FFFFFFF
    assert arm.registers.cpsr.q == 1
