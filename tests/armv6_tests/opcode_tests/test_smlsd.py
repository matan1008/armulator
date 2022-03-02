from armulator.armv6.opcodes.concrete.smlsd_a1 import SmlsdA1
from armulator.armv6.opcodes.concrete.smlsd_t1 import SmlsdT1


def test_smlsd_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11111011010000100000001100000001
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, SmlsdT1)
    assert opcode.instruction == arm.opcode
    assert opcode.a == 0
    assert opcode.m == 1
    assert opcode.n == 2
    assert opcode.d == 3
    assert not opcode.m_swap
    arm.registers.set(opcode.a, 3)
    arm.registers.set(opcode.m, 0x00030004)
    arm.registers.set(opcode.n, 0x0001FFFF)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0xFFFFFFFC


def test_smlsd_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100111000000110000000101010010
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, SmlsdA1)
    assert opcode.instruction == arm.opcode
    assert opcode.a == 0
    assert opcode.m == 1
    assert opcode.n == 2
    assert opcode.d == 3
    assert not opcode.m_swap
    arm.registers.set(opcode.a, 3)
    arm.registers.set(opcode.m, 0x00030004)
    arm.registers.set(opcode.n, 0x0001FFFF)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0xFFFFFFFC
