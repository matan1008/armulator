from armulator.armv6.opcodes.concrete.uadd8_a1 import Uadd8A1
from armulator.armv6.opcodes.concrete.uadd8_t1 import Uadd8T1


def test_uadd8_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11111010100000011111001001000000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == Uadd8T1
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.n == 1
    assert opcode.d == 2
    arm.registers.set(opcode.m, 0x0103FFFE)
    arm.registers.set(opcode.n, 0x7F04FF05)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0x8007FE03
    assert arm.registers.cpsr.ge == 0b0011


def test_uadd8_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100110010100010010111110010000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, Uadd8A1)
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.n == 1
    assert opcode.d == 2
    arm.registers.set(opcode.m, 0x0103FFFE)
    arm.registers.set(opcode.n, 0x7F04FF05)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0x8007FE03
    assert arm.registers.cpsr.ge == 0b0011
