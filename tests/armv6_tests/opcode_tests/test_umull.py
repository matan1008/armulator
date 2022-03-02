from armulator.armv6.opcodes.concrete.umull_a1 import UmullA1
from armulator.armv6.opcodes.concrete.umull_t1 import UmullT1


def test_umull_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11111011101000010011001000000000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, UmullT1)
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.n == 1
    assert opcode.d_hi == 2
    assert opcode.d_lo == 3
    assert not opcode.setflags
    arm.registers.set(opcode.m, 0x70000000)
    arm.registers.set(opcode.n, 0xFFFFFF00)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d_hi) == 0x6FFFFF90
    assert arm.registers.get(opcode.d_lo) == 0x00000000
    assert arm.registers.cpsr.n == 0


def test_umull_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100000100100110000000110010010
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, UmullA1)
    assert opcode.setflags
    assert opcode.n == 2
    assert opcode.m == 1
    assert opcode.d_hi == 3
    assert opcode.d_lo == 0
    arm.registers.set(opcode.m, 0x70000000)
    arm.registers.set(opcode.n, 0xFFFFFF00)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d_hi) == 0x6FFFFF90
    assert arm.registers.get(opcode.d_lo) == 0x00000000
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0
