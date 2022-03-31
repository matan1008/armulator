from armulator.armv6.arm_exceptions import UndefinedInstructionException
from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.opcodes.concrete.cdp_cdp2_a1 import CdpCdp2A1
from armulator.armv6.opcodes.concrete.ldc_immediate_a1 import LdcLdc2ImmediateA1
from armulator.armv6.opcodes.concrete.ldc_literal_a1 import LdcLdc2LiteralA1
from armulator.armv6.opcodes.concrete.mcr_mcr2_a1 import McrMcr2A1
from armulator.armv6.opcodes.concrete.mcrr_mcrr2_a1 import McrrMcrr2A1
from armulator.armv6.opcodes.concrete.mrc_mrc2_a1 import MrcMrc2A1
from armulator.armv6.opcodes.concrete.mrrc_mrrc2_a1 import MrrcMrrc2A1
from armulator.armv6.opcodes.concrete.stc_a1 import StcStc2A1
from armulator.armv6.opcodes.concrete.svc_a1 import SvcA1


def decode_instruction(instr):
    instr_25_21 = substring(instr, 25, 21)
    instr_25_24 = substring(instr, 25, 24)
    instr_11_9 = substring(instr, 11, 9)
    instr_25 = bit_at(instr, 25)
    instr_20 = bit_at(instr, 20)
    instr_21 = bit_at(instr, 21)
    instr_24 = bit_at(instr, 24)
    instr_23 = bit_at(instr, 23)
    op = bit_at(instr, 4)
    op1 = substring(instr, 25, 20)
    rn = substring(instr, 19, 16)
    if instr_25_21 == 0b00000:
        raise UndefinedInstructionException()
    elif instr_25_24 == 0b11:
        # Supervisor Call
        return SvcA1
    elif instr_11_9 != 0b101 and not instr_25 and not instr_20 and not (not instr_24 and not instr_23 and not instr_21):
        # Store Coprocessor
        return StcStc2A1
    elif instr_11_9 != 0b101 and not instr_25 and instr_20 and not (
            not instr_24 and not instr_23 and not instr_21) and rn != 0b1111:
        # Load Coprocessor (immediate)
        return LdcLdc2ImmediateA1
    elif instr_11_9 != 0b101 and not instr_25 and instr_20 and not (
            not instr_24 and not instr_23 and not instr_21) and rn == 0b1111:
        # Load Coprocessor (literal)
        return LdcLdc2LiteralA1
    elif instr_11_9 != 0b101 and op1 == 0b000100:
        # Move to Coprocessor from two ARM core registers
        return McrrMcrr2A1
    elif instr_11_9 != 0b101 and op1 == 0b000101:
        # Move to two ARM core registers from Coprocessor
        return MrrcMrrc2A1
    elif instr_11_9 != 0b101 and instr_25_24 == 0b10 and not op:
        # Coprocessor data operations
        return CdpCdp2A1
    elif instr_11_9 != 0b101 and instr_25_24 == 0b10 and op and not instr_20:
        # Move to Coprocessor from ARM core register
        return McrMcr2A1
    elif instr_11_9 != 0b101 and instr_25_24 == 0b10 and op and instr_20:
        # Move to ARM core register from Coprocessor
        return MrcMrc2A1
    elif instr_11_9 != 0b101 and not instr_25 and not (not instr_24 and not instr_23 and not instr_21):
        # Advanced SIMD, Floating-point
        raise NotImplementedError()
    elif instr_11_9 != 0b101 and instr_25_21 == 0b00010:
        # Advanced SIMD, Floating-point
        raise NotImplementedError()
    elif instr_11_9 != 0b101 and instr_25_24 == 0b10 and not op:
        # Floating-point data processing
        raise NotImplementedError()
    elif instr_11_9 != 0b101 and instr_25_24 == 0b10 and op:
        # Advanced SIMD, Floating-point
        raise NotImplementedError()
