from armulator.armv6.opcodes.concrete.mov_immediate_a1 import MovImmediateA1
from armulator.armv6.opcodes.concrete.mov_immediate_a2 import MovImmediateA2
from armulator.armv6.opcodes.concrete.mov_immediate_t1 import MovImmediateT1
from armulator.armv6.opcodes.concrete.mov_immediate_t2 import MovImmediateT2
from armulator.armv6.opcodes.concrete.mov_immediate_t3 import MovImmediateT3
from armulator.armv6.opcodes.concrete.mov_register_arm_a1 import MovRegisterArmA1
from armulator.armv6.opcodes.concrete.mov_register_thumb_t1 import MovRegisterThumbT1
from armulator.armv6.opcodes.concrete.mov_register_thumb_t2 import MovRegisterThumbT2
from armulator.armv6.opcodes.concrete.mov_register_thumb_t3 import MovRegisterThumbT3


def test_mov_immediate_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b0010000000000001
    arm.opcode_len = 16
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == MovImmediateT1
    assert opcode.instruction == arm.opcode
    assert opcode.imm32 == 1
    assert opcode.d == 0
    assert opcode.carry == 0
    assert opcode.setflags
    arm.emulate_cycle()
    assert arm.registers.get(0) == 1
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0


def test_mov_register_thumb_t2(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b0000000000000001
    arm.opcode_len = 16
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == MovRegisterThumbT2
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.d == 1
    assert opcode.setflags
    arm.registers.set(0, 2)
    arm.emulate_cycle()
    assert arm.registers.get(1) == 2
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0


def test_mov_register_thumb_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b0100011000000001
    arm.opcode_len = 16
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == MovRegisterThumbT1
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.d == 1
    assert not opcode.setflags
    arm.registers.set(0, 2)
    arm.emulate_cycle()
    assert arm.registers.get(1) == 2
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0


def test_mov_register_thumb_t3(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11101010010111110000000100000000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == MovRegisterThumbT3
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.d == 1
    assert opcode.setflags
    arm.registers.set(0, 2)
    arm.emulate_cycle()
    assert arm.registers.get(1) == 2
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0


def test_mov_immediate_t2(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11110000010111110000000000000010
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == MovImmediateT2
    assert opcode.instruction == arm.opcode
    assert opcode.imm32 == 2
    assert opcode.d == 0
    assert opcode.setflags
    assert opcode.carry == 0
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 2
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0


def test_movw_immediate_t3(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11110010010000000000000000000010
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == MovImmediateT3
    assert opcode.instruction == arm.opcode
    assert opcode.imm32 == 2
    assert opcode.d == 0
    assert not opcode.setflags
    assert opcode.carry == 0
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 2
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0


def test_mov_register_arm_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100001101100010010000000000000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, MovRegisterArmA1)
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.d == 2
    assert opcode.setflags
    arm.registers.set(opcode.m, 0x11223344)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0x11223344
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0


def test_mov_immediate_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100011101100000001000000000110
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, MovImmediateA1)
    assert opcode.instruction == arm.opcode
    assert opcode.imm32 == 0b110
    assert opcode.d == 1
    assert opcode.carry == 0
    assert opcode.setflags
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0b110
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0


def test_movw_immediate_a2(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100011000011110000000000000000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, MovImmediateA2)
    assert opcode.instruction == arm.opcode
    assert opcode.imm32 == 0b1111000000000000
    assert opcode.d == 0
    assert opcode.carry == 0
    assert not opcode.setflags
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0xF000
    assert arm.registers.cpsr.n == 0
    assert arm.registers.cpsr.z == 0
    assert arm.registers.cpsr.c == 0
    assert arm.registers.cpsr.v == 0
