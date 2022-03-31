from armulator.armv6.opcodes.concrete.msr_immediate_application_a1 import MsrImmediateApplicationA1
from armulator.armv6.opcodes.concrete.msr_immediate_system_a1 import MsrImmediateSystemA1
from armulator.armv6.opcodes.concrete.msr_register_application_a1 import MsrRegisterApplicationA1
from armulator.armv6.opcodes.concrete.msr_register_application_t1 import MsrRegisterApplicationT1
from armulator.armv6.opcodes.concrete.msr_register_system_a1 import MsrRegisterSystemA1
from armulator.armv6.opcodes.concrete.msr_register_system_t1 import MsrRegisterSystemT1


def test_msr_application_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11110011100000001000100000000000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, MsrRegisterApplicationT1)
    assert opcode.write_nzcvq
    assert not opcode.write_g
    assert opcode.n == 0
    arm.registers.set(0, 0x80000000)
    arm.registers.cpsr.z = 1
    arm.registers.cpsr.q = 1
    arm.emulate_cycle()
    assert arm.registers.cpsr.n
    assert not arm.registers.cpsr.z
    assert not arm.registers.cpsr.c
    assert not arm.registers.cpsr.v
    assert not arm.registers.cpsr.q


def test_msr_system_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11110011100000001000100100000000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, MsrRegisterSystemT1)
    assert not opcode.write_spsr
    assert opcode.mask == 0b1001
    assert opcode.n == 0
    arm.registers.set(0, 0x80000173)
    arm.registers.cpsr.z = 1
    arm.registers.cpsr.q = 1
    arm.emulate_cycle()
    assert arm.registers.cpsr.n
    assert not arm.registers.cpsr.z
    assert not arm.registers.cpsr.c
    assert not arm.registers.cpsr.v
    assert not arm.registers.cpsr.q
    assert not arm.registers.cpsr.i


def test_msr_register_application_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100001001010001111000000000000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, MsrRegisterApplicationA1)
    assert opcode.write_nzcvq
    assert not opcode.write_g
    assert opcode.n == 0
    arm.registers.set(0, 0x80000000)
    arm.registers.cpsr.z = 1
    arm.registers.cpsr.q = 1
    arm.emulate_cycle()
    assert arm.registers.cpsr.n
    assert not arm.registers.cpsr.z
    assert not arm.registers.cpsr.c
    assert not arm.registers.cpsr.v
    assert not arm.registers.cpsr.q


def test_msr_register_system_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100001001010011111000000000000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, MsrRegisterSystemA1)
    assert not opcode.write_spsr
    assert opcode.mask == 0b1001
    assert opcode.n == 0
    arm.registers.set(0, 0x80000173)
    arm.registers.cpsr.z = 1
    arm.registers.cpsr.q = 1
    arm.emulate_cycle()
    assert arm.registers.cpsr.n
    assert not arm.registers.cpsr.z
    assert not arm.registers.cpsr.c
    assert not arm.registers.cpsr.v
    assert not arm.registers.cpsr.q
    assert not arm.registers.cpsr.i


def test_msr_immediate_application_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100011001010001111010010000000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, MsrImmediateApplicationA1)
    assert opcode.write_nzcvq
    assert not opcode.write_g
    assert opcode.imm32 == 0x80000000
    arm.registers.cpsr.z = 1
    arm.registers.cpsr.q = 1
    arm.emulate_cycle()
    assert arm.registers.cpsr.n
    assert not arm.registers.cpsr.z
    assert not arm.registers.cpsr.c
    assert not arm.registers.cpsr.v
    assert not arm.registers.cpsr.q


def test_msr_immediate_system_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100011001000011111000001110011
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, MsrImmediateSystemA1)
    assert not opcode.write_spsr
    assert opcode.mask == 0b0001
    assert opcode.imm32 == 0x73
    arm.registers.cpsr.z = 1
    arm.registers.cpsr.q = 1
    arm.registers.cpsr.i = 1
    arm.emulate_cycle()
    assert not arm.registers.cpsr.n
    assert arm.registers.cpsr.z
    assert not arm.registers.cpsr.c
    assert not arm.registers.cpsr.v
    assert arm.registers.cpsr.q
    assert not arm.registers.cpsr.i
