from armulator.armv6.opcodes.concrete.ssub8_a1 import Ssub8A1
from armulator.armv6.opcodes.concrete.ssub8_t1 import Ssub8T1


def test_ssub8_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11111010110000011111001000000000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert type(opcode) == Ssub8T1
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.n == 1
    assert opcode.d == 2
    arm.registers.set(opcode.m, 0x0303FFFE)
    arm.registers.set(opcode.n, 0x0105FF05)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0xFE020007
    assert arm.registers.cpsr.ge == 0b0111


def test_ssub8_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100110000100010010111111110000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, Ssub8A1)
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.n == 1
    assert opcode.d == 2
    arm.registers.set(opcode.m, 0x0303FFFE)
    arm.registers.set(opcode.n, 0x0105FF05)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d) == 0xFE020007
    assert arm.registers.cpsr.ge == 0b0111
