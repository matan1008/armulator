from armulator.armv6.bits_ops import substring, chain
from armulator.armv6.opcodes.concrete.asr_immediate_t2 import AsrImmediateT2
from armulator.armv6.opcodes.concrete.lsl_immediate_t2 import LslImmediateT2
from armulator.armv6.opcodes.concrete.lsr_immediate_t2 import LsrImmediateT2
from armulator.armv6.opcodes.concrete.mov_register_thumb_t3 import MovRegisterThumbT3
from armulator.armv6.opcodes.concrete.ror_immediate_t1 import RorImmediateT1
from armulator.armv6.opcodes.concrete.rrx_t1 import RrxT1


def decode_instruction(instr):
    instr_type = substring(instr, 5, 4)
    instr_imm3_imm2 = chain(substring(instr, 14, 12), substring(instr, 7, 6), 2)
    if instr_type == 0b00 and instr_imm3_imm2 == 0b00000:
        # Move
        return MovRegisterThumbT3
    elif instr_type == 0b00 and instr_imm3_imm2 != 0b00000:
        # Logical Shift Left
        return LslImmediateT2
    elif instr_type == 0b01:
        # Logical Shift Right
        return LsrImmediateT2
    elif instr_type == 0b10:
        # Arithmetic Shift Right
        return AsrImmediateT2
    elif instr_type == 0b11 and instr_imm3_imm2 == 0b00000:
        # Rotate Right with Extend
        return RrxT1
    elif instr_type == 0b11 and instr_imm3_imm2 != 0b00000:
        # Rotate Right
        return RorImmediateT1
