from armulator.armv6.opcodes.concrete.smlsld_a1 import SmlsldA1
from armulator.armv6.opcodes.concrete.smlsld_t1 import SmlsldT1


def test_smlsld_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11111011110100010011001011000000
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, SmlsldT1)
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.n == 1
    assert opcode.d_hi == 2
    assert opcode.d_lo == 3
    assert not opcode.m_swap
    arm.registers.set(opcode.m, 0x70000000)
    arm.registers.set(opcode.n, 0xFFFFFF00)
    arm.registers.set(opcode.d_hi, 0x00000010)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d_hi) == 0x00000010
    assert arm.registers.get(opcode.d_lo) == 0x00007000


def test_smlsld_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100111010000100011000001010001
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, SmlsldA1)
    assert opcode.instruction == arm.opcode
    assert opcode.m == 0
    assert opcode.n == 1
    assert opcode.d_hi == 2
    assert opcode.d_lo == 3
    assert not opcode.m_swap
    arm.registers.set(opcode.m, 0x70000000)
    arm.registers.set(opcode.n, 0xFFFFFF00)
    arm.registers.set(opcode.d_hi, 0x00000010)
    arm.emulate_cycle()
    assert arm.registers.get(opcode.d_hi) == 0x00000010
    assert arm.registers.get(opcode.d_lo) == 0x00007000
