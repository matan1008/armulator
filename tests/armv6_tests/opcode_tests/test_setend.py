from armulator.armv6.opcodes.concrete.setend_a1 import SetendA1
from armulator.armv6.opcodes.concrete.setend_t1 import SetendT1


def test_setend_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b1011011001011000
    arm.opcode_len = 16
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, SetendT1)
    assert opcode.set_bigend
    arm.emulate_cycle()
    assert arm.registers.cpsr.e


def test_setend_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11110001000000010000001000000000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, SetendA1)
    assert opcode.set_bigend
    arm.emulate_cycle()
    assert arm.registers.cpsr.e
