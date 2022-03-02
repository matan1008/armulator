from armulator.armv6.opcodes.concrete.usat16_a1 import Usat16A1
from armulator.armv6.opcodes.concrete.usat16_t1 import Usat16T1


def test_usat16_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11110011101000000000000100000011
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == Usat16T1
    assert opcode.instruction == arm.opcode
    assert opcode.saturate_to == 3
    assert opcode.d == 1
    assert opcode.n == 0
    arm.registers.set(opcode.n, 0x00090009)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0x00070007
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0
    assert arm.registers.cpsr.q == 1


def test_usat16_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100110111000110001111100110000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, Usat16A1)
    assert opcode.instruction == arm.opcode
    assert opcode.saturate_to == 3
    assert opcode.d == 1
    assert opcode.n == 0
    arm.registers.set(opcode.n, 0x00090009)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0x00070007
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0
    assert arm.registers.cpsr.q == 1
