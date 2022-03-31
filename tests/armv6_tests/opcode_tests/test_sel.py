from armulator.armv6.opcodes.concrete.sel_a1 import SelA1
from armulator.armv6.opcodes.concrete.sel_t1 import SelT1


def test_sel_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11111010101000001111001010000001
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == SelT1
    assert opcode.instruction == arm.opcode
    assert opcode.n == 0
    assert opcode.m == 1
    assert opcode.d == 2
    arm.registers.set(opcode.n, 0x11223344)
    arm.registers.set(opcode.m, 0xAABBCCDD)
    arm.registers.cpsr.ge = 0b1100
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0x1122CCDD


def test_sel_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100110100000010010111110110000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, SelA1)
    assert opcode.instruction == arm.opcode
    assert opcode.n == 1
    assert opcode.m == 0
    assert opcode.d == 2
    arm.registers.set(opcode.n, 0x11223344)
    arm.registers.set(opcode.m, 0xAABBCCDD)
    arm.registers.cpsr.ge = 0b1100
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0x1122CCDD
