from armulator.armv6.opcodes.concrete.sxtah_a1 import SxtahA1
from armulator.armv6.opcodes.concrete.sxtah_t1 import SxtahT1


def test_sxtah_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11111010000000011111001010010000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == SxtahT1
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.d == 2
    assert opcode.n == 1
    assert opcode.rotation == 8
    arm.registers.set(opcode.m, 0xfffffeff)
    arm.registers.set(opcode.n, 5)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 3


def test_sxtah_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100110101100010010010001110000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, SxtahA1)
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.d == 2
    assert opcode.n == 1
    assert opcode.rotation == 8
    arm.registers.set(opcode.m, 0xfffffeff)
    arm.registers.set(opcode.n, 5)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 3
