from armulator.armv6.opcodes.concrete.adr_a1 import AdrA1
from armulator.armv6.opcodes.concrete.adr_a2 import AdrA2
from armulator.armv6.opcodes.concrete.adr_t1 import AdrT1
from armulator.armv6.opcodes.concrete.adr_t2 import AdrT2
from armulator.armv6.opcodes.concrete.adr_t3 import AdrT3


def test_adr_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b1010000000000001
    arm.opcode_len = 16
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == AdrT1
    assert opcode.imm32 == 4
    assert opcode.add
    assert opcode.d == 0
    pc = arm.registers.get_pc()
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == pc + opcode.imm32


def test_adr_t3(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11110010000011110000000000000100
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == AdrT3
    assert opcode.imm32 == 4
    assert opcode.add
    assert opcode.d == 0
    pc = arm.registers.get_pc()
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == pc + opcode.imm32


def test_adr_t2(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11110010101011110000000000000100
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == AdrT2
    assert opcode.imm32 == 4
    assert not opcode.add
    assert opcode.d == 0
    arm.registers.branch_to(0x0F000000)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0x0F000004 - opcode.imm32


def test_adr_a2(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100010010011110000000000000100
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, AdrA2)
    assert opcode.imm32 == 4
    assert not opcode.add
    assert opcode.d == 0
    arm.registers.branch_to(0x0F000000)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0x0F000008 - opcode.imm32


def test_adr_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100010100011110000000000000100
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, AdrA1)
    assert opcode.imm32 == 4
    assert opcode.add
    assert opcode.d == 0
    arm.registers.branch_to(0x0F000000)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0x0F000008 + opcode.imm32
