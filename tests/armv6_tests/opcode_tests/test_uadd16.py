from armulator.armv6.opcodes.concrete.uadd16_a1 import Uadd16A1
from armulator.armv6.opcodes.concrete.uadd16_t1 import Uadd16T1


def test_uadd16_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11111010100100011111001001000000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == Uadd16T1
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.n == 1
    assert opcode.d == 2
    arm.registers.set(opcode.m, 0x0003FFFE)
    arm.registers.set(opcode.n, 0xFFF00005)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0xFFF30003
    assert arm.registers.cpsr.ge == 0b0011


def test_uadd16_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100110010100010010111100010000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, Uadd16A1)
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.n == 1
    assert opcode.d == 2
    arm.registers.set(opcode.m, 0x0003FFFE)
    arm.registers.set(opcode.n, 0xFFF00005)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0xFFF30003
    assert arm.registers.cpsr.ge == 0b0011
