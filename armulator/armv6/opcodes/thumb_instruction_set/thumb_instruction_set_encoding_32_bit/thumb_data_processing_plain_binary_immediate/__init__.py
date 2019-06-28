from __future__ import absolute_import
from .add_sp_plus_immediate_t4 import AddSpPlusImmediateT4
from .add_immediate_thumb_t4 import AddImmediateThumbT4
from .adr_t3 import AdrT3
from .mov_immediate_t3 import MovImmediateT3
from .sub_sp_minus_immediate_t3 import SubSpMinusImmediateT3
from .sub_immediate_thumb_t4 import SubImmediateThumbT4
from .adr_t2 import AdrT2
from .movt_t1 import MovtT1
from .ssat_t1 import SsatT1
from .ssat16_t1 import Ssat16T1
from .sbfx_t1 import SbfxT1
from .bfi_t1 import BfiT1
from .bfc_t1 import BfcT1
from .usat_t1 import UsatT1
from .usat16_t1 import Usat16T1
from .ubfx_t1 import UbfxT1


def decode_instruction(instr):
    if instr[7:12] == "0b00000" and instr[12:16] != "0b1111":
        # Add Wide (12-bit)
        if instr[12:16] == "0b1101":
            return AddSpPlusImmediateT4
        else:
            return AddImmediateThumbT4
    elif instr[7:12] == "0b00000" and instr[12:16] == "0b1111":
        # Form PC-relative Address
        return AdrT3
    elif instr[7:12] == "0b00100":
        # Move Wide (16-bit)
        return MovImmediateT3
    elif instr[7:12] == "0b01010" and instr[12:16] != "0b1111":
        # Subtract Wide (12-bit)
        if instr[12:16] == "0b1101":
            return SubSpMinusImmediateT3
        else:
            return SubImmediateThumbT4
    elif instr[7:12] == "0b01010" and instr[12:16] == "0b1111":
        # Form PC-relative Address
        return AdrT2
    elif instr[7:12] == "0b01100":
        # Move Top (16-bit)
        return MovtT1
    elif instr[7:12] == "0b10000" or (instr[7:12] == "0b10010" and not (instr[17:20] + instr[24:26] == "0b00000")):
        # Signed Saturate
        return SsatT1
    elif instr[7:12] == "0b10010" and (instr[17:20] + instr[24:26] == "0b00000"):
        # Signed Saturate, two 16-bit
        return Ssat16T1
    elif instr[7:12] == "0b10100":
        # Signed Bit Field Extract
        return SbfxT1
    elif instr[7:12] == "0b10110" and instr[12:16] != "0b1111":
        # Bit Field Insert
        return BfiT1
    elif instr[7:12] == "0b10110" and instr[12:16] == "0b1111":
        # Bit Field Clear
        return BfcT1
    elif instr[7:12] == "0b11000" or (instr[7:12] == "0b11010" and not (instr[17:20] + instr[24:26] == "0b00000")):
        # Unsigned Saturate
        return UsatT1
    elif instr[7:12] == "0b11010" and (instr[17:20] + instr[24:26] == "0b00000"):
        # Unsigned Saturate, two 16-bit
        return Usat16T1
    elif instr[7:12] == "0b11100":
        # Unsigned Bit Field Extract
        return UbfxT1
