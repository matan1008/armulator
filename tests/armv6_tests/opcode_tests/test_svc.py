from armulator.armv6.opcodes.concrete.svc_a1 import SvcA1
from armulator.armv6.opcodes.concrete.svc_t1 import SvcT1


def test_svc_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b1101111100000100
    arm.opcode_len = 16
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == SvcT1
    assert opcode.instruction == arm.opcode
    arm.registers.branch_to(0x0F000000)
    arm.emulate_cycle()
    assert arm.registers.pc_store_value() == 0x00000008


def test_svc_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11101111000000000000000000000100
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, SvcA1)
    assert opcode.instruction == arm.opcode
    arm.registers.branch_to(0x0F000000)
    arm.emulate_cycle()
    assert arm.registers.pc_store_value() == 0x00000008
