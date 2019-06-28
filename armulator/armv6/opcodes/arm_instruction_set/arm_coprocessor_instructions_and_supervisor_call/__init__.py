from __future__ import absolute_import
from armulator.armv6.arm_exceptions import UndefinedInstructionException
from .svc_a1 import SvcA1
from .stc_a1 import StcA1
from .ldc_immediate_a1 import LdcImmediateA1
from .ldc_literal_a1 import LdcLiteralA1
from .mcrr_a1 import McrrA1
from .mrrc_a1 import MrrcA1
from .cdp_a1 import CdpA1
from .mcr_a1 import McrA1
from .mrc_a1 import MrcA1


def decode_instruction(instr):
    if instr[6:11] == "0b00000":
        raise UndefinedInstructionException()
    elif instr[6:8] == "0b11":
        # Supervisor Call
        return SvcA1
    elif instr[20:23] != "0b101" and not instr[6] and not instr[11] and not (
                    not instr[7] and not instr[8] and not instr[10]):
        # Store Coprocessor
        return StcA1
    elif instr[20:23] != "0b101" and not instr[6] and instr[11] and not (
                    not instr[7] and not instr[8] and not instr[10]) and instr[12:16] != "0b1111":
        # Load Coprocessor (immediate)
        return LdcImmediateA1
    elif instr[20:23] != "0b101" and not instr[6] and instr[11] and not (
                    not instr[7] and not instr[8] and not instr[10]) and instr[12:16] == "0b1111":
        # Load Coprocessor (literal)
        return LdcLiteralA1
    elif instr[20:23] != "0b101" and instr[6:12] == "0b000100":
        # Move to Coprocessor from two ARM core registers
        return McrrA1
    elif instr[20:23] != "0b101" and instr[6:12] == "0b000101":
        # Move to two ARM core registers from Coprocessor
        return MrrcA1
    elif instr[20:23] != "0b101" and instr[6:8] == "0b10" and not instr[27]:
        # Coprocessor data operations
        return CdpA1
    elif instr[20:23] != "0b101" and instr[6:8] == "0b10" and instr[27] and not instr[11]:
        # Move to Coprocessor from ARM core register
        return McrA1
    elif instr[20:23] != "0b101" and instr[6:8] == "0b10" and instr[27] and instr[11]:
        # Move to ARM core register from Coprocessor
        return MrcA1
    elif instr[20:23] != "0b101" and not instr[6] and not (instr[6:9] == "0b000" and not instr[10]):
        # Advanced SIMD, Floating-point
        raise NotImplementedError()
    elif instr[20:23] != "0b101" and instr[6:11] == "0b00010":
        # Advanced SIMD, Floating-point
        raise NotImplementedError()
    elif instr[20:23] != "0b101" and instr[6:8] == "0b10" and not instr[27]:
        # Floating-point data processing
        raise NotImplementedError()
    elif instr[20:23] != "0b101" and instr[6:8] == "0b10" and instr[27]:
        # Advanced SIMD, Floating-point
        raise NotImplementedError()
