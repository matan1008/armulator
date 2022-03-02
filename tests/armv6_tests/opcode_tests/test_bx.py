from armulator.armv6.opcodes.concrete.bx_a1 import BxA1
from armulator.armv6.opcodes.concrete.bx_t1 import BxT1


def test_bx_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b0100011100001000
    prev_pc = 0x0F000000
    arm.registers.branch_to(prev_pc)
    arm.opcode_len = 16
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == BxT1
    assert opcode.m == 1
    assert opcode.instruction == arm.opcode
    arm.registers.set(1, 0x0000ff00)
    arm.emulate_cycle()
    assert arm.registers.pc_store_value() == 0x0000ff00


def test_bx_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100001001011111111111100010000
    prev_pc = 0x0F000000
    arm.registers.branch_to(prev_pc)
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, BxA1)
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    arm.registers.set(opcode.m, 0x0000ff00)
    arm.emulate_cycle()
    assert arm.registers.pc_store_value() == 0x0000ff00
