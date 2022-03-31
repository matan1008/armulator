from armulator.armv6.arm_v6 import ArmV6
from armulator.armv6.opcodes.concrete.b_a1 import BA1

from armulator.armv6.opcodes.concrete.b_t1 import BT1
from armulator.armv6.opcodes.concrete.b_t2 import BT2
from armulator.armv6.opcodes.concrete.b_t3 import BT3
from armulator.armv6.opcodes.concrete.b_t4 import BT4


def test_b_t1():
    arm = ArmV6()
    arm.take_reset()
    instr = 0b1101000000000100
    prev_pc = 0x0F000000
    arm.registers.branch_to(prev_pc)
    arm.opcode_len = 16
    opcode = arm.decode_instruction(instr)
    opcode = opcode.from_bitarray(instr, arm)
    assert type(opcode) == BT1
    assert opcode.imm32 == 0x00000008
    assert opcode.instruction == instr
    arm.registers.cpsr.n = 0
    arm.registers.cpsr.z = 1
    arm.registers.cpsr.c = 0
    arm.registers.cpsr.v = 0
    arm.execute_instruction(opcode)
    assert arm.registers.pc_store_value() == 0x0F00000C


def test_b_t2(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b1110000000000100
    arm.opcode_len = 16
    prev_pc = 0x0F000000
    arm.registers.branch_to(prev_pc)
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == BT2
    assert opcode.imm32 == 0x00000008
    assert opcode.instruction == arm.opcode
    arm.emulate_cycle()
    assert arm.registers.pc_store_value() == 0x0F00000C


def test_b_t3(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11110000010000001000000000000100
    arm.opcode_len = 32
    prev_pc = 0x0F000000
    arm.registers.branch_to(prev_pc)
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == BT3
    assert opcode.imm32 == 0x00000008
    assert opcode.instruction == arm.opcode
    arm.emulate_cycle()
    assert arm.registers.pc_store_value() == 0x0F00000C


def test_b_t4(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11110000000000001011100000000100
    arm.opcode_len = 32
    prev_pc = 0x0F000000
    arm.registers.branch_to(prev_pc)
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == BT4
    assert opcode.imm32 == 0x00000008
    assert opcode.instruction == arm.opcode
    arm.emulate_cycle()
    assert arm.registers.pc_store_value() == 0x0F00000C


def test_b_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11101010000000000000000000001000
    arm.opcode_len = 32
    prev_pc = 0x0F000000
    arm.registers.branch_to(prev_pc)
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, BA1)
    assert opcode.imm32 == 0x00000020
    assert opcode.instruction == arm.opcode
    arm.emulate_cycle()
    assert arm.registers.pc_store_value() == 0x0F000028
