from armulator.armv6.opcodes.concrete.ssat_a1 import SsatA1
from armulator.armv6.opcodes.concrete.ssat_t1 import SsatT1
from armulator.armv6.shift import SRType


def test_ssat_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11110011000000000000000101000011
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == SsatT1
    assert opcode.instruction == arm.opcode
    assert opcode.saturate_to == 4
    assert opcode.d == 1
    assert opcode.n == 0
    assert opcode.shift_t == SRType.LSL
    assert opcode.shift_n == 1
    arm.registers.set(opcode.n, 9)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 7
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0
    assert arm.registers.cpsr.q == 1


def test_ssat_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100110101000110001000010010000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, SsatA1)
    assert opcode.instruction == arm.opcode
    assert opcode.saturate_to == 4
    assert opcode.d == 1
    assert opcode.n == 0
    assert opcode.shift_t == SRType.LSL
    assert opcode.shift_n == 1
    arm.registers.set(opcode.n, 9)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 7
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0
    assert arm.registers.cpsr.q == 1
