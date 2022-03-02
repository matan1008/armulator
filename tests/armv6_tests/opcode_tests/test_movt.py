from armulator.armv6.opcodes.concrete.movt_a1 import MovtA1
from armulator.armv6.opcodes.concrete.movt_t1 import MovtT1


def test_movt_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11110110110010100010000010111011
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == MovtT1
    assert opcode.instruction == arm.opcode
    assert opcode.imm16 == 0xAABB
    assert opcode.d == 0
    arm.registers.set(opcode.d, 0x11223344)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0xAABB3344
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0


def test_movt_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100011010010100000101010111011
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, MovtA1)
    assert opcode.instruction == arm.opcode
    assert opcode.imm16 == 0xAABB
    assert opcode.d == 0
    arm.registers.set(opcode.d, 0x11223344)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0xAABB3344
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0
