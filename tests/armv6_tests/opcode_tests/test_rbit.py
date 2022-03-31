from armulator.armv6.opcodes.concrete.rbit_a1 import RbitA1
from armulator.armv6.opcodes.concrete.rbit_t1 import RbitT1


def test_rbit_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11111010100100011111001010100001
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == RbitT1
    assert opcode.instruction == arm.opcode
    assert opcode.m == 1
    assert opcode.d == 2
    arm.registers.set(opcode.m, 0xAABBCCDD)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0xBB33DD55


def test_rbit_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100110111111110001111100110000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, RbitA1)
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.d == 1
    arm.registers.set(opcode.m, 0xAABBCCDD)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0xBB33DD55
