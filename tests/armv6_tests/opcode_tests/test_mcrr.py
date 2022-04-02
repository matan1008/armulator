from armulator.armv6.opcodes.concrete.mcrr_mcrr2_a1 import McrrMcrr2A1
from armulator.armv6.opcodes.concrete.mcrr_mcrr2_a2 import McrrMcrr2A2
from armulator.armv6.opcodes.concrete.mcrr_mcrr2_t1 import McrrMcrr2T1
from armulator.armv6.opcodes.concrete.mcrr_mcrr2_t2 import McrrMcrr2T2


def test_mcrr_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11101100010000010010000100010000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == McrrMcrr2T1
    assert opcode.instruction == arm.opcode
    assert opcode.t == 2
    assert opcode.t2 == 1
    assert opcode.cp == 1
    arm.registers.branch_to(0xFF000000)
    arm.emulate_cycle()
    assert arm.registers.pc_store_value() == 0x00000004


def test_mcrr2_t2(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11111100010000010010000100010000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == McrrMcrr2T2
    assert opcode.instruction == arm.opcode
    assert opcode.t == 2
    assert opcode.t2 == 1
    assert opcode.cp == 1
    arm.registers.branch_to(0xFF000000)
    arm.emulate_cycle()
    assert arm.registers.pc_store_value() == 0x00000004


def test_mcrr_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11101100010000010010000100010000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, McrrMcrr2A1)
    assert opcode.instruction == arm.opcode
    assert opcode.t == 2
    assert opcode.t2 == 1
    assert opcode.cp == 1
    arm.registers.branch_to(0xFF000000)
    arm.emulate_cycle()
    assert arm.registers.pc_store_value() == 0x00000004


def test_mcrr2_a2(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11111100010000010010000100010000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, McrrMcrr2A2)
    assert opcode.instruction == arm.opcode
    assert opcode.t == 2
    assert opcode.t2 == 1
    assert opcode.cp == 1
    arm.registers.branch_to(0xFF000000)
    arm.emulate_cycle()
    assert arm.registers.pc_store_value() == 0x00000004
