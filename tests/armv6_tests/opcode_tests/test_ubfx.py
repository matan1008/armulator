from armulator.armv6.opcodes.concrete.ubfx_a1 import UbfxA1
from armulator.armv6.opcodes.concrete.ubfx_t1 import UbfxT1


def test_ubfx_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11110011110000000000000111000100
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == UbfxT1
    assert opcode.instruction == arm.opcode
    assert opcode.lsbit == 3
    assert opcode.widthminus1 == 4
    assert opcode.n == 0
    assert opcode.d == 1
    arm.registers.set(opcode.n, 0x000000F8)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0x0000001F
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0


def test_ubfx_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100111111001000001000111010000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, UbfxA1)
    assert opcode.instruction == arm.opcode
    assert opcode.lsbit == 3
    assert opcode.widthminus1 == 4
    assert opcode.n == 0
    assert opcode.d == 1
    arm.registers.set(opcode.n, 0x000000F8)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0x0000001F
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0
