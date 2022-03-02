from armulator.armv6.opcodes.concrete.umaal_a1 import UmaalA1
from armulator.armv6.opcodes.concrete.umaal_t1 import UmaalT1


def test_umaal_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11111011111000010011001001100000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, UmaalT1)
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.n == 1
    assert opcode.d_hi == 2
    assert opcode.d_lo == 3
    arm.registers.set(opcode.m, 0x70000000)
    arm.registers.set(opcode.n, 0xFFFFFF00)
    arm.registers.set(opcode.d_hi, 0x00000010)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d_hi) == 0x6FFFFF90
    assert arm.registers.get(opcode.d_lo) == 0x00000010


def test_umaal_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100000010000110000000110010010
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, UmaalA1)
    assert opcode.n == 2
    assert opcode.m == 1
    assert opcode.d_hi == 3
    assert opcode.d_lo == 0
    arm.registers.set(opcode.m, 0x70000000)
    arm.registers.set(opcode.n, 0xFFFFFF00)
    arm.registers.set(opcode.d_hi, 0x00000010)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d_hi) == 0x6FFFFF90
    assert arm.registers.get(opcode.d_lo) == 0x00000010
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0
