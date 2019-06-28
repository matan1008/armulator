from __future__ import absolute_import
from .and_immediate_t1 import AndImmediateT1
from .tst_immediate_t1 import TstImmediateT1
from .bic_immediate_t1 import BicImmediateT1
from .orr_immediate_t1 import OrrImmediateT1
from .mov_immediate_t2 import MovImmediateT2
from .orn_immediate_t1 import OrnImmediateT1
from .mvn_immediate_t1 import MvnImmediateT1
from .eor_immediate_t1 import EorImmediateT1
from .teq_immediate_t1 import TeqImmediateT1
from .add_sp_plus_immediate_t3 import AddSpPlusImmediateT3
from .add_immediate_thumb_t3 import AddImmediateThumbT3
from .cmn_immediate_t1 import CmnImmediateT1
from .adc_immediate_t1 import AdcImmediateT1
from .sbc_immediate_t1 import SbcImmediateT1
from .sub_sp_minus_immediate_t2 import SubSpMinusImmediateT2
from .sub_immediate_thumb_t3 import SubImmediateThumbT3
from .cmp_immediate_t2 import CmpImmediateT2
from .rsb_immediate_t2 import RsbImmediateT2


def decode_instruction(instr):
    if instr[7:11] == "0b0000" and not (instr[20:24] == "0b1111" and instr[11]):
        # Bitwise AND
        return AndImmediateT1
    elif instr[7:11] == "0b0000" and (instr[20:24] == "0b1111" and instr[11]):
        # Test
        return TstImmediateT1
    elif instr[7:11] == "0b0001":
        # Bitwise Bit Clear
        return BicImmediateT1
    elif instr[7:11] == "0b0010" and instr[12:16] != "0b1111":
        # Bitwise OR
        return OrrImmediateT1
    elif instr[7:11] == "0b0010" and instr[12:16] == "0b1111":
        # Move
        return MovImmediateT2
    elif instr[7:11] == "0b0011" and instr[12:16] != "0b1111":
        # Bitwise OR NOT
        return OrnImmediateT1
    elif instr[7:11] == "0b0011" and instr[12:16] == "0b1111":
        # Bitwise NOT
        return MvnImmediateT1
    elif instr[7:11] == "0b0100" and not (instr[20:24] == "0b1111" and instr[11]):
        # Bitwise Exclusive OR
        return EorImmediateT1
    elif instr[7:11] == "0b0100" and (instr[20:24] == "0b1111" and instr[11]):
        # Test Equivalence
        return TeqImmediateT1
    elif instr[7:11] == "0b1000" and not (instr[20:24] == "0b1111" and instr[11]):
        # Add
        if instr[12:16] == "0b1101":
            return AddSpPlusImmediateT3
        else:
            return AddImmediateThumbT3
    elif instr[7:11] == "0b1000" and (instr[20:24] == "0b1111" and instr[11]):
        # Compare Negative
        return CmnImmediateT1
    elif instr[7:11] == "0b1010":
        # Add with Carry
        return AdcImmediateT1
    elif instr[7:11] == "0b1011":
        # Subtract with Carry
        return SbcImmediateT1
    elif instr[7:11] == "0b1101" and not (instr[20:24] == "0b1111" and instr[11]):
        # Subtract
        if instr[12:16] == "0b1101":
            return SubSpMinusImmediateT2
        else:
            return SubImmediateThumbT3
    elif instr[7:11] == "0b1101" and (instr[20:24] == "0b1111" and instr[11]):
        # Compare
        return CmpImmediateT2
    elif instr[7:11] == "0b1110":
        # Reverse Subtract
        return RsbImmediateT2
