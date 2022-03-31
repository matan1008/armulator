from armulator.armv6.opcodes.concrete.rrx_a1 import RrxA1
from armulator.armv6.opcodes.concrete.rrx_t1 import RrxT1


def test_rrx_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11101010010111110000000100110000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == RrxT1
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.d == 1
    assert opcode.setflags
    arm.registers.cpsr.c = 1
    arm.registers.set(0, 0x0000FFFF)
    arm.emulate_cycle()
    assert arm.registers.get(1) == 0x80007FFF
    assert arm.registers.cpsr.n == 1
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 1
    assert arm.registers.cpsr.v == 0


def test_rrx_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100001101100010010000001100000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, RrxA1)
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.d == 2
    assert opcode.setflags
    arm.registers.cpsr.c = 1
    arm.registers.set(opcode.m, 0x0000FFFE)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0x80007FFF
    assert arm.registers.cpsr.n == 1
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0
