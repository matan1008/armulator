from armulator.armv6.opcodes.concrete.sxtab_a1 import SxtabA1
from armulator.armv6.opcodes.concrete.sxtab_t1 import SxtabT1


def test_sxtab_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11111010010000011111001010010000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == SxtabT1
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.d == 2
    assert opcode.n == 1
    assert opcode.rotation == 8
    arm.registers.set(opcode.m, 0x0000fe00)
    arm.registers.set(opcode.n, 5)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 3


def test_sxtab_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100110101000010010010001110000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, SxtabA1)
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.d == 2
    assert opcode.n == 1
    assert opcode.rotation == 8
    arm.registers.set(opcode.m, 0x0000fe00)
    arm.registers.set(opcode.n, 5)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 3
