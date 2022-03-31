from armulator.armv6.opcodes.concrete.mrs_application_a1 import MrsApplicationA1
from armulator.armv6.opcodes.concrete.mrs_application_t1 import MrsApplicationT1
from armulator.armv6.opcodes.concrete.mrs_system_a1 import MrsSystemA1
from armulator.armv6.opcodes.concrete.mrs_system_t1 import MrsSystemT1


def test_mrs_application_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11110011111011111000000000000000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, MrsApplicationT1)
    assert opcode.d == 0
    arm.registers.cpsr.z = 1
    arm.registers.cpsr.q = 1
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0x48000000


def test_msr_system_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11110011111111111000000000000000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, MrsSystemT1)
    assert opcode.read_spsr
    assert opcode.d == 0
    arm.registers.set_spsr(0x11223344)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0x11223344


def test_mrs_application_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100001000011110000000000000000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, MrsApplicationA1)
    assert opcode.d == 0
    arm.registers.cpsr.z = 1
    arm.registers.cpsr.q = 1
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0x48000000


def test_mrs_system_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100001010011110000000000000000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, MrsSystemA1)
    assert opcode.read_spsr
    assert opcode.d == 0
    arm.registers.set_spsr(0x11223344)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0x11223344
