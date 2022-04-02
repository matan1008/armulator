from armulator.armv6.opcodes.concrete.mrrc_mrrc2_a1 import MrrcMrrc2A1
from armulator.armv6.opcodes.concrete.mrrc_mrrc2_a2 import MrrcMrrc2A2
from armulator.armv6.opcodes.concrete.mrrc_mrrc2_t1 import MrrcMrrc2T1
from armulator.armv6.opcodes.concrete.mrrc_mrrc2_t2 import MrrcMrrc2T2


def test_mrrc_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11101100010100010010000100010000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == MrrcMrrc2T1
    assert opcode.instruction == arm.opcode
    assert opcode.t == 2
    assert opcode.t2 == 1
    assert opcode.cp == 1
    arm.registers.branch_to(0xFF000000)
    arm.emulate_cycle()
    assert arm.registers.pc_store_value() == 0x00000004


def test_mrrc2_t2(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11111100010100010010000100010000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == MrrcMrrc2T2
    assert opcode.instruction == arm.opcode
    assert opcode.t == 2
    assert opcode.t2 == 1
    assert opcode.cp == 1
    arm.registers.branch_to(0xFF000000)
    arm.emulate_cycle()
    assert arm.registers.pc_store_value() == 0x00000004


def test_mrrc_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11101100010100010010000100010000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, MrrcMrrc2A1)
    assert opcode.instruction == arm.opcode
    assert opcode.t == 2
    assert opcode.t2 == 1
    assert opcode.cp == 1
    arm.registers.branch_to(0xFF000000)
    arm.emulate_cycle()
    assert arm.registers.pc_store_value() == 0x00000004


def test_mrrc2_a2(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11111100010100010010000100010000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, MrrcMrrc2A2)
    assert opcode.instruction == arm.opcode
    assert opcode.t == 2
    assert opcode.t2 == 1
    assert opcode.cp == 1
    arm.registers.branch_to(0xFF000000)
    arm.emulate_cycle()
    assert arm.registers.pc_store_value() == 0x00000004
