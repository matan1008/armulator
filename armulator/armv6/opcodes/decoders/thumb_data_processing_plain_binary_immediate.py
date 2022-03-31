from armulator.armv6.bits_ops import substring, chain
from armulator.armv6.opcodes.concrete.add_immediate_thumb_t4 import AddImmediateThumbT4
from armulator.armv6.opcodes.concrete.add_sp_plus_immediate_t4 import AddSpPlusImmediateT4
from armulator.armv6.opcodes.concrete.adr_t2 import AdrT2
from armulator.armv6.opcodes.concrete.adr_t3 import AdrT3
from armulator.armv6.opcodes.concrete.bfc_t1 import BfcT1
from armulator.armv6.opcodes.concrete.bfi_t1 import BfiT1
from armulator.armv6.opcodes.concrete.mov_immediate_t3 import MovImmediateT3
from armulator.armv6.opcodes.concrete.movt_t1 import MovtT1
from armulator.armv6.opcodes.concrete.sbfx_t1 import SbfxT1
from armulator.armv6.opcodes.concrete.ssat16_t1 import Ssat16T1
from armulator.armv6.opcodes.concrete.ssat_t1 import SsatT1
from armulator.armv6.opcodes.concrete.sub_immediate_thumb_t4 import SubImmediateThumbT4
from armulator.armv6.opcodes.concrete.sub_sp_minus_immediate_t3 import SubSpMinusImmediateT3
from armulator.armv6.opcodes.concrete.usat16_t1 import Usat16T1
from armulator.armv6.opcodes.concrete.usat_t1 import UsatT1
from armulator.armv6.opcodes.concrete.ubfx_t1 import UbfxT1


def decode_instruction(instr):
    instr_op = substring(instr, 24, 20)
    instr_rn = substring(instr, 19, 16)
    instr_14_12_7_6 = chain(substring(instr, 14, 12), substring(instr, 7, 6), 2)
    if instr_op == 0b00000 and instr_rn != 0b1111:
        # Add Wide (12-bit)
        if instr_rn == 0b1101:
            return AddSpPlusImmediateT4
        else:
            return AddImmediateThumbT4
    elif instr_op == 0b00000 and instr_rn == 0b1111:
        # Form PC-relative Address
        return AdrT3
    elif instr_op == 0b00100:
        # Move Wide (16-bit)
        return MovImmediateT3
    elif instr_op == 0b01010 and instr_rn != 0b1111:
        # Subtract Wide (12-bit)
        if instr_rn == 0b1101:
            return SubSpMinusImmediateT3
        else:
            return SubImmediateThumbT4
    elif instr_op == 0b01010 and instr_rn == 0b1111:
        # Form PC-relative Address
        return AdrT2
    elif instr_op == 0b01100:
        # Move Top (16-bit)
        return MovtT1
    elif instr_op == 0b10000 or (instr_op == 0b10010 and not (instr_14_12_7_6 == 0b00000)):
        # Signed Saturate
        return SsatT1
    elif instr_op == 0b10010 and (instr_14_12_7_6 == 0b00000):
        # Signed Saturate, two 16-bit
        return Ssat16T1
    elif instr_op == 0b10100:
        # Signed Bit Field Extract
        return SbfxT1
    elif instr_op == 0b10110 and instr_rn != 0b1111:
        # Bit Field Insert
        return BfiT1
    elif instr_op == 0b10110 and instr_rn == 0b1111:
        # Bit Field Clear
        return BfcT1
    elif instr_op == 0b11000 or (instr_op == 0b11010 and not (instr_14_12_7_6 == 0b00000)):
        # Unsigned Saturate
        return UsatT1
    elif instr_op == 0b11010 and (instr_14_12_7_6 == 0b00000):
        # Unsigned Saturate, two 16-bit
        return Usat16T1
    elif instr_op == 0b11100:
        # Unsigned Bit Field Extract
        return UbfxT1
