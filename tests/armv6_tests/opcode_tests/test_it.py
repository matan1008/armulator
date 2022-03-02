from armulator.armv6.opcodes.concrete.it_t1 import ItT1


def test_it_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b1011111100011101
    arm.opcode_len = 16
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, ItT1)
    assert opcode.firstcond == 0b0001
    assert opcode.mask == 0b1101
    arm.emulate_cycle()
    assert arm.registers.cpsr.it == 0b00011101
