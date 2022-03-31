from armulator.armv6.bits_ops import bit_at, substring
from armulator.armv6.opcodes.concrete.bl_immediate_a2 import BlBlxImmediateA2
from armulator.armv6.opcodes.concrete.cdp_cdp2_a2 import CdpCdp2A2
from armulator.armv6.opcodes.concrete.ldc_ldc2_immediate_a2 import LdcLdc2ImmediateA2
from armulator.armv6.opcodes.concrete.ldc_ldc2_literal_a2 import LdcLdc2LiteralA2
from armulator.armv6.opcodes.concrete.mcr_mcr2_a2 import McrMcr2A2
from armulator.armv6.opcodes.concrete.mcrr_mcrr2_a2 import McrrMcrr2A2
from armulator.armv6.opcodes.concrete.mrc_mrc2_a2 import MrcMrc2A2
from armulator.armv6.opcodes.concrete.mrrc_mrrc2_a2 import MrrcMrrc2A2
from armulator.armv6.opcodes.concrete.rfe_a1 import RfeA1
from armulator.armv6.opcodes.concrete.srs_arm_a1 import SrsArmA1
from armulator.armv6.opcodes.concrete.stc_stc2_a2 import StcStc2A2
from armulator.armv6.opcodes.decoders import arm_memory_hints_advanced_simd_instructions_and_miscellaneous_instructions


def decode_instruction(instr):
    instr_27 = bit_at(instr, 27)
    instr_27_25 = substring(instr, 27, 25)
    instr_27_24 = substring(instr, 27, 24)
    instr_22 = bit_at(instr, 22)
    instr_20 = bit_at(instr, 20)
    instr_24 = bit_at(instr, 24)
    instr_23 = bit_at(instr, 23)
    instr_21 = bit_at(instr, 21)
    op = bit_at(instr, 4)
    rn = substring(instr, 19, 16)
    op1 = substring(instr, 27, 20)
    if not instr_27:
        # Memory hints, Advanced SIMD instructions, and miscellaneous instructions
        return arm_memory_hints_advanced_simd_instructions_and_miscellaneous_instructions.decode_instruction(instr)
    elif instr_27_25 == 0b100 and instr_22 and not instr_20:
        # Store Return State
        return SrsArmA1
    elif instr_27_25 == 0b100 and not instr_22 and instr_20:
        # Return From Exception
        return RfeA1
    elif instr_27_25 == 0b101:
        # Branch with Link and Exchange
        return BlBlxImmediateA2
    elif instr_27_25 == 0b110 and not instr_20 and not (not instr_24 and not instr_23 and not instr_21):
        # Store Coprocessor
        return StcStc2A2
    elif instr_27_25 == 0b110 and instr_20 and not (not instr_24 and not instr_23 and not instr_21) and rn != 0b1111:
        # Load Coprocessor (immediate)
        return LdcLdc2ImmediateA2
    elif instr_27_25 == 0b110 and instr_20 and not (not instr_24 and not instr_23 and not instr_21) and rn == 0b1111:
        # Load Coprocessor (literal)
        return LdcLdc2LiteralA2
    elif op1 == 0b11000100:
        # Move to Coprocessor from two ARM core registers
        return McrrMcrr2A2
    elif op1 == 0b11000101:
        # Move to two ARM core registers from Coprocessor
        return MrrcMrrc2A2
    elif instr_27_24 == 0b1110 and not op:
        # Coprocessor data operations
        return CdpCdp2A2
    elif instr_27_24 == 0b1110 and not instr_20 and op:
        # Move to Coprocessor from ARM core register
        return McrMcr2A2
    elif instr_27_24 == 0b1110 and instr_20 and op:
        # Move to ARM core register from Coprocessor
        return MrcMrc2A2
