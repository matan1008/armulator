from armulator.armv6.opcodes.concrete.bfi_a1 import BfiA1
from armulator.armv6.opcodes.concrete.bfi_t1 import BfiT1


def test_bfi_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11110011011000000000000111000111
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == BfiT1
    assert opcode.instruction == arm.opcode
    assert opcode.lsbit == 3
    assert opcode.msbit == 7
    assert opcode.n == 0
    assert opcode.d == 1
    arm.registers.set(opcode.n, 0x00000088)
    arm.registers.set(opcode.d, 0xF0000070)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0xF0000088
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0


def test_bfi_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100111110001110001000110010000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, BfiA1)
    assert opcode.instruction == arm.opcode
    assert opcode.lsbit == 3
    assert opcode.msbit == 7
    assert opcode.n == 0
    assert opcode.d == 1
    arm.registers.set(opcode.n, 0x00000088)
    arm.registers.set(opcode.d, 0xF0000070)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0xF0000088
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0
