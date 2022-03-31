from armulator.armv6.opcodes.concrete.cps_arm_a1 import CpsArmA1
from armulator.armv6.opcodes.concrete.cps_thumb_t1 import CpsThumbT1
from armulator.armv6.opcodes.concrete.cps_thumb_t2 import CpsThumbT2


def test_cps_thumb_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b1011011001110001
    arm.opcode_len = 16
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, CpsThumbT1)
    assert not opcode.affect_a
    assert not opcode.affect_i
    assert opcode.affect_f
    assert not opcode.enable
    assert opcode.disable
    assert not opcode.change_mode
    assert opcode.mode == 0b00000
    arm.registers.cpsr.f = 0
    arm.emulate_cycle()
    assert arm.registers.cpsr.f == 1


def test_cps_thumb_t2(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11110011101011111000011000100000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, CpsThumbT2)
    assert not opcode.affect_a
    assert not opcode.affect_i
    assert opcode.affect_f
    assert not opcode.enable
    assert opcode.disable
    assert not opcode.change_mode
    assert opcode.mode == 0b00000
    arm.registers.cpsr.f = 0
    arm.emulate_cycle()
    assert arm.registers.cpsr.f == 1


def test_cps_arm_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11110001000011000000000001000000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, CpsArmA1)
    assert not opcode.affect_a
    assert not opcode.affect_i
    assert opcode.affect_f
    assert not opcode.enable
    assert opcode.disable
    assert not opcode.change_mode
    assert opcode.mode == 0b00000
    arm.registers.cpsr.f = 0
    arm.emulate_cycle()
    assert arm.registers.cpsr.f == 1
