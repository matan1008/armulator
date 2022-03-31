from armulator.armv6.opcodes.concrete.smc_a1 import SmcA1
from armulator.armv6.opcodes.concrete.smc_t1 import SmcT1


def test_smc_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11110111111100001000000000000000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, SmcT1)
    arm.emulate_cycle()
    assert arm.registers.cpsr.m == 0b10110


def test_smc_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100001011000000000000001110001
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, SmcA1)
    arm.emulate_cycle()
    assert arm.registers.cpsr.m == 0b10110
