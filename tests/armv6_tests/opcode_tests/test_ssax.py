from armulator.armv6.opcodes.concrete.ssax_a1 import SsaxA1
from armulator.armv6.opcodes.concrete.ssax_t1 import SsaxT1


def test_ssax_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11111010111000011111001000000000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == SsaxT1
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.n == 1
    assert opcode.d == 2
    arm.registers.set(opcode.m, 0x0003FFFE)
    arm.registers.set(opcode.n, 0x00050005)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0x0070008
    assert arm.registers.cpsr.ge == 0b1111


def test_ssax_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100110000100010010111101010000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, SsaxA1)
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.n == 1
    assert opcode.d == 2
    arm.registers.set(opcode.m, 0x0003FFFE)
    arm.registers.set(opcode.n, 0x00050005)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0x0070008
    assert arm.registers.cpsr.ge == 0b1111
