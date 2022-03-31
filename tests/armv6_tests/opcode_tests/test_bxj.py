from armulator.armv6.opcodes.concrete.bxj_a1 import BxjA1
from armulator.armv6.opcodes.concrete.bxj_t1 import BxjT1


def test_bxj_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11110011110000001000111100000000
    prev_pc = 0x0F000000
    arm.registers.branch_to(prev_pc)
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, BxjT1)
    assert opcode.m == 0
    assert opcode.instruction == arm.opcode
    arm.registers.set(0, 0x0000ff00)
    arm.emulate_cycle()
    assert arm.registers.pc_store_value() == 0x0000ff00


def test_bxj_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100001001011111111111100100000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, BxjA1)
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    arm.registers.set(opcode.m, 0x0000ff00)
    arm.emulate_cycle()
    assert arm.registers.pc_store_value() == 0x0000ff00
