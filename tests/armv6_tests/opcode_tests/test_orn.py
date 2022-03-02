from armulator.armv6.opcodes.concrete.orn_immediate_t1 import OrnImmediateT1
from armulator.armv6.opcodes.concrete.orn_register_t1 import OrnRegisterT1
from armulator.armv6.shift import SRType


def test_orn_register_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11101010011100010000001001000000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == OrnRegisterT1
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.d == 2
    assert opcode.n == 1
    assert opcode.shift_t == SRType.LSL
    assert opcode.shift_n == 1
    assert opcode.setflags
    arm.registers.set(0, 0b0011)
    arm.registers.set(1, 0b0101)
    arm.emulate_cycle()
    assert arm.registers.get(2) == 0b11111111111111111111111111111101
    assert arm.registers.cpsr.n == 1
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0


def test_orn_immediate_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11110000011100000000000100000110
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == OrnImmediateT1
    assert opcode.instruction == arm.opcode
    assert opcode.imm32 == 0b110
    assert opcode.d == 1
    assert opcode.n == 0
    assert opcode.setflags
    assert opcode.carry == 0
    arm.registers.set(opcode.n, 0b0101)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0b11111111111111111111111111111101
    assert arm.registers.cpsr.n == 1
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0
