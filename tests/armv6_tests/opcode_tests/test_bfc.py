from armulator.armv6.opcodes.concrete.bfc_a1 import BfcA1
from armulator.armv6.opcodes.concrete.bfc_t1 import BfcT1


def test_bfc_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11110011011011110000000111000111
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == BfcT1
    assert opcode.instruction == arm.opcode
    assert opcode.lsbit == 3
    assert opcode.msbit == 7
    assert opcode.d == 1
    arm.registers.set(opcode.d, 0xF00000FF)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0xF0000007
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0


def test_bfc_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100111110001110001000110011111
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, BfcA1)
    assert opcode.instruction == arm.opcode
    assert opcode.lsbit == 3
    assert opcode.msbit == 7
    assert opcode.d == 1
    arm.registers.set(opcode.d, 0xF00000FF)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0xF0000007
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0
