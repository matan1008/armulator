from armulator.armv6.opcodes.concrete.eret_t1 import EretT1


def test_eret_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11110011110111101000111100000000
    prev_pc = 0x0F000000
    arm.registers.branch_to(prev_pc)
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, EretT1)
    assert opcode.instruction == arm.opcode
    arm.registers.set_spsr(0b10001)
    arm.registers.set(14, 0x0000ff00)
    arm.emulate_cycle()
    assert arm.registers.pc_store_value() == 0x0000ff00
