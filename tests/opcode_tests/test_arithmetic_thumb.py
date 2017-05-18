from armulator.arm1176 import ARM1176
from bitstring import BitArray
from armulator.opcodes.thumb_instruction_set.thumb_instruction_set_encoding_16_bit.thumb_shift_immediate_add_subtract_move_and_compare.add_immediate_thumb_t1 import AddImmediateThumbT1
from armulator.opcodes.thumb_instruction_set.thumb_instruction_set_encoding_16_bit.thumb_shift_immediate_add_subtract_move_and_compare.lsl_immediate_t1 import LslImmediateT1

def test_add_immediate_thumb():
    arm = ARM1176()
    arm.take_reset()
    instr = BitArray(bin="0001110001000001")
    opcode = arm.decode_instruction(instr)
    opcode = opcode.from_bitarray(instr, arm)
    assert type(opcode) == AddImmediateThumbT1
    assert opcode.setflags == True
    assert opcode.d == 1
    assert opcode.n == 0
    assert opcode.imm32 == BitArray(hex="0x00000001")
    arm.core_registers.set(opcode.n, BitArray(hex="0x00000000"))
    arm.execute_instruction(opcode)
    assert arm.core_registers.get(opcode.d) == BitArray(hex="0x00000001")
    assert arm.core_registers.get_cpsr_n() == "0"
    assert arm.core_registers.get_cpsr_z() == "0"
    assert arm.core_registers.get_cpsr_c() == "0"
    assert arm.core_registers.get_cpsr_v() == "0"

def test_lsl_immediate_thumb():
    arm = ARM1176()
    arm.take_reset()
    instr = BitArray(bin="0000000010111000")
    opcode = arm.decode_instruction(instr)
    opcode = opcode.from_bitarray(instr, arm)
    assert type(opcode) == LslImmediateT1
    assert opcode.setflags == True
    assert opcode.d == 0
    assert opcode.m == 7
    assert opcode.shift_n == 2
    arm.core_registers.set(opcode.m, BitArray(hex="0x00000002"))
    arm.execute_instruction(opcode)
    assert arm.core_registers.get(opcode.d) == BitArray(hex="0x00000008")
    assert arm.core_registers.get_cpsr_n() == "0"
    assert arm.core_registers.get_cpsr_z() == "0"
    assert arm.core_registers.get_cpsr_c() == "0"