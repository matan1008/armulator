from armulator.armv6.opcodes.concrete.cdp_cdp2_a1 import CdpCdp2A1
from armulator.armv6.opcodes.concrete.cdp_cdp2_a2 import CdpCdp2A2
from armulator.armv6.opcodes.concrete.cdp_cdp2_t1 import CdpCdp2T1
from armulator.armv6.opcodes.concrete.cdp_cdp2_t2 import CdpCdp2T2


def test_cdp_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11101110000100010010000100000000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == CdpCdp2T1
    assert opcode.instruction == arm.opcode
    assert opcode.cp == 1
    arm.registers.branch_to(0xFF000000)
    arm.emulate_cycle()
    assert arm.registers.pc_store_value() == 0x00000004


def test_cdp2_t2(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11111110000100010010000100000000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == CdpCdp2T2
    assert opcode.instruction == arm.opcode
    assert opcode.cp == 1
    arm.registers.branch_to(0xFF000000)
    arm.emulate_cycle()
    assert arm.registers.pc_store_value() == 0x00000004


def test_cdp_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11101110000100010010000100000000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, CdpCdp2A1)
    assert opcode.instruction == arm.opcode
    assert opcode.cp == 1
    arm.registers.branch_to(0xFF000000)
    arm.emulate_cycle()
    assert arm.registers.pc_store_value() == 0x00000004


def test_cdp2_a2(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11111110000100010010000100000000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, CdpCdp2A2)
    assert opcode.instruction == arm.opcode
    assert opcode.cp == 1
    arm.registers.branch_to(0xFF000000)
    arm.emulate_cycle()
    assert arm.registers.pc_store_value() == 0x00000004
