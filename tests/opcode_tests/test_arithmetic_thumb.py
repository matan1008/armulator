from armulator.arm1176 import ARM1176
from bitstring import BitArray
from armulator.shift import SRType
from armulator.opcodes.thumb_instruction_set.thumb_instruction_set_encoding_16_bit.thumb_shift_immediate_add_subtract_move_and_compare.add_immediate_thumb_t1 import AddImmediateThumbT1
from armulator.opcodes.thumb_instruction_set.thumb_instruction_set_encoding_16_bit.thumb_shift_immediate_add_subtract_move_and_compare.lsl_immediate_t1 import LslImmediateT1
from armulator.opcodes.thumb_instruction_set.thumb_instruction_set_encoding_16_bit.thumb_shift_immediate_add_subtract_move_and_compare.add_register_thumb_t1 import AddRegisterThumbT1
from armulator.opcodes.thumb_instruction_set.thumb_instruction_set_encoding_16_bit.thumb_shift_immediate_add_subtract_move_and_compare.cmp_immediate_t1 import CmpImmediateT1

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

def test_add_register_thumb():
    arm = ARM1176()
    arm.take_reset()
    instr = BitArray(bin="0001100001010011")
    opcode = arm.decode_instruction(instr)
    opcode = opcode.from_bitarray(instr, arm)
    assert type(opcode) == AddRegisterThumbT1
    assert opcode.setflags == True
    assert opcode.m == 1
    assert opcode.d == 3
    assert opcode.n == 2
    assert opcode.shift_n == 0
    assert opcode.shift_t == SRType.SRType_LSL
    arm.core_registers.set(opcode.n, BitArray(hex="0x70000000"))
    arm.core_registers.set(opcode.m, BitArray(hex="0x10000001"))
    arm.execute_instruction(opcode)
    assert arm.core_registers.get(opcode.d) == BitArray(hex="0x80000001")
    assert arm.core_registers.get_cpsr_n() == "1"
    assert arm.core_registers.get_cpsr_z() == "0"
    assert arm.core_registers.get_cpsr_c() == "0"
    assert arm.core_registers.get_cpsr_v() == "1"

def test_cmp_immediate_thumb():
    arm = ARM1176()
    arm.take_reset()
    instr = BitArray(bin="0010100000000101")
    opcode = arm.decode_instruction(instr)
    opcode = opcode.from_bitarray(instr, arm)
    assert type(opcode) == CmpImmediateT1
    assert opcode.n == 0
    assert opcode.imm32 == BitArray(hex="0x00000005")
    arm.core_registers.set(opcode.n, BitArray(hex="0x00000004"))
    arm.execute_instruction(opcode)
    assert arm.core_registers.get_cpsr_n() == "1"
    assert arm.core_registers.get_cpsr_z() == "0"
    assert arm.core_registers.get_cpsr_c() == "0"
    assert arm.core_registers.get_cpsr_v() == "0"
