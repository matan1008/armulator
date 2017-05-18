import arm_memory_hints_advanced_simd_instructions_and_miscellaneous_instructions
from srs_arm_a1 import SrsArmA1
from rfe_a1 import RfeA1
from bl_immediate_a2 import BlImmediateA2
from stc_a2 import StcA2
from ldc_immediate_a2 import LdcImmediateA2
from ldc_literal_a2 import LdcLiteralA2
from mcrr_a2 import McrrA2
from mrrc_a2 import MrrcA2
from cdp_a2 import CdpA2
from mcr_a2 import McrA2
from mrc_a2 import MrcA2


def decode_instruction(instr):
    if not instr[4]:
        # Memory hints, Advanced SIMD instructions, and miscellaneous instructions
        return arm_memory_hints_advanced_simd_instructions_and_miscellaneous_instructions.decode_instruction(instr)
    elif instr[4:7] == "0b100" and instr[9] and not instr[11]:
        # Store Return State
        return SrsArmA1
    elif instr[4:7] == "0b100" and not instr[9] and instr[11]:
        # Return From Exception
        return RfeA1
    elif instr[4:7] == "0b101":
        # Branch with Link and Exchange
        return BlImmediateA2
    elif instr[4:7] == "0b110" and not instr[11] and not (not instr[7] and not instr[8] and not instr[10]):
        # Store Coprocessor
        return StcA2
    elif instr[4:7] == "0b110" and instr[11] and not (
                    not instr[7] and not instr[8] and not instr[10]) and instr[12:16] != "0b1111":
        # Load Coprocessor (immediate)
        return LdcImmediateA2
    elif instr[4:7] == "0b110" and instr[11] and not (
                    not instr[7] and not instr[8] and not instr[10]) and instr[12:16] == "0b1111":
        # Load Coprocessor (literal)
        return LdcLiteralA2
    elif instr[4:12] == "0b11000100":
        # Move to Coprocessor from two ARM core registers
        return McrrA2
    elif instr[4:12] == "0b11000101":
        # Move to two ARM core registers from Coprocessor
        return MrrcA2
    elif instr[4:8] == "0b1110" and not instr[27]:
        # Coprocessor data operations
        return CdpA2
    elif instr[4:8] == "0b1110" and not instr[11] and instr[27]:
        # Move to Coprocessor from ARM core register
        return McrA2
    elif instr[4:8] == "0b1110" and instr[11] and instr[27]:
        # Move to ARM core register from Coprocessor
        return MrcA2
