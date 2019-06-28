from __future__ import absolute_import
from armulator.armv6.arm_exceptions import UndefinedInstructionException
from .stc_t1 import StcT1
from .stc_t2 import StcT2
from .ldc_immediate_t1 import LdcImmediateT1
from .ldc_immediate_t2 import LdcImmediateT2
from .ldc_literal_t1 import LdcLiteralT1
from .ldc_literal_t2 import LdcLiteralT2
from .mcrr_t1 import McrrT1
from .mcrr_t2 import McrrT2
from .mrrc_t1 import MrrcT1
from .mrrc_t2 import MrrcT2
from .cdp_t1 import CdpT1
from .cdp_t2 import CdpT2
from .mcr_t1 import McrT1
from .mcr_t2 import McrT2
from .mrc_t1 import MrcT1
from .mrc_t2 import MrcT2


def decode_instruction(instr):
    if instr[6:11] == "0b00000":
        raise UndefinedInstructionException()
    elif instr[6:8] == "0b11":
        # Advanced SIMD, will not be implemented
        raise NotImplementedError
    elif instr[20:23] != "0b101" and not instr[6] and not instr[11] and not (instr[7:9] == "0b00" and not instr[10]):
        # Store Coprocessor
        if not instr[3]:
            return StcT1
        else:
            return StcT2
    elif instr[20:23] != "0b101" and not instr[6] and instr[11] and not (
            instr[7:9] == "0b00" and not instr[10]) and instr[12:16] != "0b1111":
        # Load Coprocessor (immediate)
        if not instr[3]:
            return LdcImmediateT1
        else:
            return LdcImmediateT2
    elif instr[20:23] != "0b101" and not instr[6] and instr[11] and not (
            instr[7:9] == "0b00" and not instr[10]) and instr[12:16] == "0b1111":
        # Load Coprocessor (literal)
        if not instr[3]:
            return LdcLiteralT1
        else:
            return LdcLiteralT2
    elif instr[20:23] != "0b101" and instr[6:12] == "0b000100":
        # Move to Coprocessor from two ARM core registers
        if not instr[3]:
            return McrrT1
        else:
            return McrrT2
    elif instr[20:23] != "0b101" and instr[6:12] == "0b000101":
        # Move to two ARM core registers from Coprocessor
        if not instr[3]:
            return MrrcT1
        else:
            return MrrcT2
    elif instr[20:23] != "0b101" and instr[6:8] == "0b10" and not instr[27]:
        # Coprocessor data operations
        if not instr[3]:
            return CdpT1
        else:
            return CdpT2
    elif instr[20:23] != "0b101" and instr[6:8] == "0b10" and not instr[11] and instr[27]:
        # Move to Coprocessor from ARM core register
        if not instr[3]:
            return McrT1
        else:
            return McrT2
    elif instr[20:23] != "0b101" and instr[6:8] == "0b10" and instr[11] and instr[27]:
        # Move to ARM core register from Coprocessor
        if not instr[3]:
            return MrcT1
        else:
            return MrcT2
    elif instr[20:23] == "0b101" and not instr[6] and not (instr[6:9] == "0b000" and not instr[10]):
        # Extension register load/store instructions
        raise NotImplementedError()
    elif instr[20:23] == "0b101" and instr[6:11] == "0b00010":
        # 64-bit transfers between ARM core and extension registers
        raise NotImplementedError()
    elif instr[20:23] == "0b101" and instr[6:8] == "0b10" and not instr[27]:
        # Floating-point data-processing instructions
        raise NotImplementedError()
    elif instr[20:23] == "0b101" and instr[6:8] == "0b10" and instr[27]:
        # 8, 16, and 32-bit transfer between ARM core and extension registers
        raise NotImplementedError()
