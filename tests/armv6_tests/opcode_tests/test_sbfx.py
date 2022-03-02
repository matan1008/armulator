from armulator.armv6.opcodes.concrete.sbfx_a1 import SbfxA1
from armulator.armv6.opcodes.concrete.sbfx_t1 import SbfxT1


def test_sbfx_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11110011010000000000000111000100
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == SbfxT1
    assert opcode.instruction == arm.opcode
    assert opcode.lsbit == 3
    assert opcode.widthminus1 == 4
    assert opcode.n == 0
    assert opcode.d == 1
    arm.registers.set(opcode.n, 0x000000F8)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0xFFFFFFFF
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0


def test_sbfx_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100111101001000001000111010000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, SbfxA1)
    assert opcode.instruction == arm.opcode
    assert opcode.lsbit == 3
    assert opcode.widthminus1 == 4
    assert opcode.n == 0
    assert opcode.d == 1
    arm.registers.set(opcode.n, 0x000000F8)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0xFFFFFFFF
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0
