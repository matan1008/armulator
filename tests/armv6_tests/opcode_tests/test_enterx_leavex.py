from armulator.armv6.enums import InstrSet
from armulator.armv6.opcodes.concrete.enterx_leavex_t1 import EnterxLeavexT1


def test_leavex_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11110011101111111000111100001111
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, EnterxLeavexT1)
    assert not opcode.is_enterx
    arm.registers.select_instr_set(InstrSet.THUMB_EE)
    arm.emulate_cycle()
    assert arm.registers.current_instr_set() == InstrSet.THUMB


def test_enterx_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11110011101111111000111100011111
    arm.opcode_len = 32
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, EnterxLeavexT1)
    assert opcode.is_enterx
    arm.emulate_cycle()
    assert arm.registers.current_instr_set() == InstrSet.THUMB_EE
