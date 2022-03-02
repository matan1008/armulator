from armulator.armv6.arm_exceptions import UndefinedInstructionException
from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.opcodes.concrete.cdp_cdp2_t1 import CdpCdp2T1
from armulator.armv6.opcodes.concrete.cdp_cdp2_t2 import CdpCdp2T2
from armulator.armv6.opcodes.concrete.ldc_ldc2_immediate_t1 import LdcLdc2ImmediateT1
from armulator.armv6.opcodes.concrete.ldc_ldc2_immediate_t2 import LdcLdc2ImmediateT2
from armulator.armv6.opcodes.concrete.ldc_ldc2_literal_t1 import LdcLdc2LiteralT1
from armulator.armv6.opcodes.concrete.ldc_ldc2_literal_t2 import LdcLdc2LiteralT2
from armulator.armv6.opcodes.concrete.mcr_mcr2_t1 import McrMcr2T1
from armulator.armv6.opcodes.concrete.mcr_mcr2_t2 import McrMcr2T2
from armulator.armv6.opcodes.concrete.mcrr_mcrr2_t1 import McrrMcrr2T1
from armulator.armv6.opcodes.concrete.mcrr_mcrr2_t2 import McrrMcrr2T2
from armulator.armv6.opcodes.concrete.mrc_mrc2_t1 import MrcMrc2T1
from armulator.armv6.opcodes.concrete.mrc_mrc2_t2 import MrcMrc2T2
from armulator.armv6.opcodes.concrete.mrrc_mrrc2_t1 import MrrcMrrc2T1
from armulator.armv6.opcodes.concrete.mrrc_mrrc2_t2 import MrrcMrrc2T2
from armulator.armv6.opcodes.concrete.stc_stc2_t1 import StcStc2T1
from armulator.armv6.opcodes.concrete.stc_stc2_t2 import StcStc2T2


def decode_instruction(instr):
    instr_11_9 = substring(instr, 11, 9)
    instr_25 = bit_at(instr, 25)
    instr_20 = bit_at(instr, 20)
    instr_21 = bit_at(instr, 21)
    instr_rn = substring(instr, 19, 16)
    if substring(instr, 25, 21) == 0b00000:
        raise UndefinedInstructionException()
    elif substring(instr, 25, 24) == 0b11:
        # Advanced SIMD, will not be implemented
        raise NotImplementedError
    elif instr_11_9 != 0b101 and not instr_25 and not instr_20 and not (
            substring(instr, 24, 23) == 0b00 and not instr_21):
        # Store Coprocessor
        if not bit_at(instr, 28):
            return StcStc2T1
        else:
            return StcStc2T2
    elif instr_11_9 != 0b101 and not instr_25 and instr_20 and not (
            substring(instr, 24, 23) == 0b00 and not instr_21) and instr_rn != 0b1111:
        # Load Coprocessor (immediate)
        if not bit_at(instr, 28):
            return LdcLdc2ImmediateT1
        else:
            return LdcLdc2ImmediateT2
    elif instr_11_9 != 0b101 and not instr_25 and instr_20 and not (
            substring(instr, 24, 23) == 0b00 and not instr_21) and instr_rn == 0b1111:
        # Load Coprocessor (literal)
        if not bit_at(instr, 28):
            return LdcLdc2LiteralT1
        else:
            return LdcLdc2LiteralT2
    elif instr_11_9 != 0b101 and substring(instr, 25, 20) == 0b000100:
        # Move to Coprocessor from two ARM core registers
        if not bit_at(instr, 28):
            return McrrMcrr2T1
        else:
            return McrrMcrr2T2
    elif instr_11_9 != 0b101 and substring(instr, 25, 20) == 0b000101:
        # Move to two ARM core registers from Coprocessor
        if not bit_at(instr, 28):
            return MrrcMrrc2T1
        else:
            return MrrcMrrc2T2
    elif instr_11_9 != 0b101 and substring(instr, 25, 24) == 0b10 and not bit_at(instr, 4):
        # Coprocessor data operations
        if not bit_at(instr, 28):
            return CdpCdp2T1
        else:
            return CdpCdp2T2
    elif instr_11_9 != 0b101 and substring(instr, 25, 24) == 0b10 and not instr_20 and bit_at(instr, 4):
        # Move to Coprocessor from ARM core register
        if not bit_at(instr, 28):
            return McrMcr2T1
        else:
            return McrMcr2T2
    elif instr_11_9 != 0b101 and substring(instr, 25, 24) == 0b10 and instr_20 and bit_at(instr, 4):
        # Move to ARM core register from Coprocessor
        if not bit_at(instr, 28):
            return MrcMrc2T1
        else:
            return MrcMrc2T2
    elif instr_11_9 == 0b101 and not instr_25 and not (substring(instr, 25, 23) == 0b000 and not instr_21):
        # Extension register load/store instructions
        raise NotImplementedError()
    elif instr_11_9 == 0b101 and substring(instr, 25, 21) == 0b00010:
        # 64-bit transfers between ARM core and extension registers
        raise NotImplementedError()
    elif instr_11_9 == 0b101 and substring(instr, 25, 24) == 0b10 and not bit_at(instr, 4):
        # Floating-point data-processing instructions
        raise NotImplementedError()
    elif instr_11_9 == 0b101 and substring(instr, 25, 24) == 0b10 and bit_at(instr, 4):
        # 8, 16, and 32-bit transfer between ARM core and extension registers
        raise NotImplementedError()
