from armulator.armv6.opcodes.concrete.usax_a1 import UsaxA1
from armulator.armv6.opcodes.concrete.usax_t1 import UsaxT1


def test_usax_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11111010111000011111001001000000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == UsaxT1
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.n == 1
    assert opcode.d == 2
    arm.registers.set(opcode.m, 0x0003FFFE)
    arm.registers.set(opcode.n, 0x00050005)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0x0070008
    assert arm.registers.cpsr.ge == 0b0000


def test_usax_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100110010100010010111101010000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, UsaxA1)
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.n == 1
    assert opcode.d == 2
    arm.registers.set(opcode.m, 0x0003FFFE)
    arm.registers.set(opcode.n, 0x00050005)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0x0070008
    assert arm.registers.cpsr.ge == 0b0000
