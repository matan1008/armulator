from armulator.armv6.opcodes.concrete.pkh_a1 import PkhA1
from armulator.armv6.opcodes.concrete.pkh_t1 import PkhT1
from armulator.armv6.shift import SRType


def test_pkh_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11101010110000010000001001000000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == PkhT1
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.d == 2
    assert opcode.n == 1
    assert opcode.shift_t == SRType.LSL
    assert opcode.shift_n == 1
    assert not opcode.tb_form
    arm.registers.set(opcode.m, 0x555de66e)
    arm.registers.set(opcode.n, 0x11223344)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0xaabb3344
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0


def test_pkh_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100110100000010010000010010000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, PkhA1)
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.d == 2
    assert opcode.n == 1
    assert opcode.shift_t == SRType.LSL
    assert opcode.shift_n == 1
    assert not opcode.tb_form
    arm.registers.set(opcode.m, 0x555de66e)
    arm.registers.set(opcode.n, 0x11223344)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0xaabb3344
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0
