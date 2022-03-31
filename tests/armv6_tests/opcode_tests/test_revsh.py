from armulator.armv6.opcodes.concrete.revsh_a1 import RevshA1
from armulator.armv6.opcodes.concrete.revsh_t1 import RevshT1
from armulator.armv6.opcodes.concrete.revsh_t2 import RevshT2


def test_revsh_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b1011101011001000
    arm.opcode_len = 16
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == RevshT1
    assert opcode.instruction == arm.opcode
    assert opcode.m == 1
    assert opcode.d == 0
    arm.registers.set(1, 0x00CCDD)
    arm.emulate_cycle()
    assert arm.registers.get(0) == 0xFFFFDDCC


def test_revsh_t2(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11111010100100011111001010110001
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == RevshT2
    assert opcode.instruction == arm.opcode
    assert opcode.m == 1
    assert opcode.d == 2
    arm.registers.set(opcode.m, 0x00CCDD)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0xFFFFDDCC


def test_revsh_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100110111111110001111110110000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, RevshA1)
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.d == 1
    arm.registers.set(opcode.m, 0x00CCDD)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0xFFFFDDCC
