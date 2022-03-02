from armulator.armv6.opcodes.concrete.qdsub_a1 import QdsubA1
from armulator.armv6.opcodes.concrete.qdsub_t1 import QdsubT1


def test_qdsub16_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11111010100000001111001010110001
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == QdsubT1
    assert opcode.instruction == arm.opcode
    assert opcode.m == 1
    assert opcode.n == 0
    assert opcode.d == 2
    arm.registers.set(opcode.m, 0x0003FFFE)
    arm.registers.set(opcode.n, 0xC0000005)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0x7fffffff
    assert arm.registers.cpsr.q == 1


def test_qdsub_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100001011000000010000001010001
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, QdsubA1)
    assert opcode.instruction == arm.opcode
    assert opcode.m == 1
    assert opcode.n == 0
    assert opcode.d == 2
    arm.registers.set(opcode.m, 0x0003FFFE)
    arm.registers.set(opcode.n, 0xC0000005)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0x7fffffff
    assert arm.registers.cpsr.q == 1
