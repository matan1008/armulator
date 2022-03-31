from armulator.armv6.enums import InstrSet
from armulator.armv6.opcodes.concrete.bl_blx_immediate_t1 import BlBlxImmediateT1
from armulator.armv6.opcodes.concrete.bl_blx_immediate_t2 import BlBlxImmediateT2
from armulator.armv6.opcodes.concrete.bl_immediate_a1 import BlBlxImmediateA1
from armulator.armv6.opcodes.concrete.bl_immediate_a2 import BlBlxImmediateA2
from armulator.armv6.opcodes.concrete.blx_register_a1 import BlxRegisterA1
from armulator.armv6.opcodes.concrete.blx_register_t1 import BlxRegisterT1


def test_blx_register_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b0100011110001000
    prev_pc = 0x0F000000
    arm.registers.branch_to(prev_pc)
    arm.opcode_len = 16
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == BlxRegisterT1
    assert opcode.m == 1
    assert opcode.instruction == arm.opcode
    arm.registers.set(1, 0x0000ff00)
    arm.emulate_cycle()
    assert arm.registers.pc_store_value() == 0x0000ff00
    assert arm.registers.get_lr() == 0x0F000003


def test_blx_immediate_t2(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11110000000000001110100000000010
    prev_pc = 0x0F000000
    arm.registers.branch_to(prev_pc)
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, BlBlxImmediateT2)
    assert opcode.target_instr_set == InstrSet.ARM
    assert opcode.imm32 == 4
    assert opcode.instruction == arm.opcode
    arm.emulate_cycle()
    assert arm.registers.pc_store_value() == 0x0F000008
    assert arm.registers.get_lr() == 0x0F000005
    assert arm.registers.current_instr_set() == InstrSet.ARM


def test_bl_immediate_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11110000000000001111100000000010
    prev_pc = 0x0F000000
    arm.registers.branch_to(prev_pc)
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, BlBlxImmediateT1)
    assert opcode.target_instr_set == InstrSet.THUMB
    assert opcode.imm32 == 4
    assert opcode.instruction == arm.opcode
    arm.emulate_cycle()
    assert arm.registers.pc_store_value() == 0x0F000008
    assert arm.registers.get_lr() == 0x0F000005
    assert arm.registers.current_instr_set() == InstrSet.THUMB


def test_blx_register_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100001001011111111111100110000
    arm.opcode_len = 32
    prev_pc = 0x0F000000
    arm.registers.branch_to(prev_pc)
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, BlxRegisterA1)
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    arm.registers.set(opcode.m, 0x0000ff00)
    arm.emulate_cycle()
    assert arm.registers.pc_store_value() == 0x0000ff00
    assert arm.registers.get_lr() == 0x0F000004


def test_bl_immediate_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11101011000000000000000000001000
    prev_pc = 0x0F000000
    arm.registers.branch_to(prev_pc)
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, BlBlxImmediateA1)
    assert opcode.target_instr_set == InstrSet.ARM
    assert opcode.imm32 == 0x20
    assert opcode.instruction == arm.opcode
    arm.emulate_cycle()
    assert arm.registers.pc_store_value() == 0x0F000028
    assert arm.registers.get_lr() == 0x0F000004
    assert arm.registers.current_instr_set() == InstrSet.ARM


def test_bl_immediate_a2(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11111010000000000000000000001000
    prev_pc = 0x0F000000
    arm.registers.branch_to(prev_pc)
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, BlBlxImmediateA2)
    assert opcode.target_instr_set == InstrSet.THUMB
    assert opcode.imm32 == 0x20
    assert opcode.instruction == arm.opcode
    arm.emulate_cycle()
    assert arm.registers.pc_store_value() == 0x0F000028
    assert arm.registers.get_lr() == 0x0F000004
    assert arm.registers.current_instr_set() == InstrSet.THUMB
