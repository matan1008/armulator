from __future__ import absolute_import
from .subs_pc_lr_arm_a1 import SubsPcLrArmA1
from .and_immediate_a1 import AndImmediateA1
from .eor_immediate_a1 import EorImmediateA1
from .sub_sp_minus_immediate_a1 import SubSpMinusImmediateA1
from .sub_immediate_arm_a1 import SubImmediateArmA1
from .adr_a2 import AdrA2
from .rsb_immediate_a1 import RsbImmediateA1
from .add_sp_plus_immediate_a1 import AddSpPlusImmediateA1
from .add_immediate_arm_a1 import AddImmediateArmA1
from .adr_a1 import AdrA1
from .adc_immediate_a1 import AdcImmediateA1
from .sbc_immediate_a1 import SbcImmediateA1
from .rsc_immediate_a1 import RscImmediateA1
from .tst_immediate_a1 import TstImmediateA1
from .teq_immediate_a1 import TeqImmediateA1
from .cmp_immediate_a1 import CmpImmediateA1
from .cmn_immediate_a1 import CmnImmediateA1
from .orr_immediate_a1 import OrrImmediateA1
from .mov_immediate_a1 import MovImmediateA1
from .bic_immediate_a1 import BicImmediateA1
from .mvn_immediate_a1 import MvnImmediateA1


def decode_instruction(instr):
    if instr[7:11] == "0b0000":
        # Bitwise AND
        if instr[16:20] == "0b1111" and instr[11]:
            return SubsPcLrArmA1
        else:
            return AndImmediateA1
    elif instr[7:11] == "0b0001":
        # Bitwise Exclusive OR
        if instr[16:20] == "0b1111" and instr[11]:
            return SubsPcLrArmA1
        else:
            return EorImmediateA1
    elif instr[7:11] == "0b0010" and instr[12:16] != "0b1111":
        # Subtract
        if instr[16:20] == "0b1111" and instr[11]:
            return SubsPcLrArmA1
        elif instr[12:16] == "0b1101":
            return SubSpMinusImmediateA1
        else:
            return SubImmediateArmA1
    elif instr[7:11] == "0b0010" and instr[12:16] == "0b1111":
        # Form PC-relative address
        return AdrA2
    elif instr[7:11] == "0b0011":
        # Reverse Subtract
        if instr[16:20] == "0b1111" and instr[11]:
            return SubsPcLrArmA1
        else:
            return RsbImmediateA1
    elif instr[7:11] == "0b0100" and instr[12:16] != "0b1111":
        # Add
        if instr[16:20] == "0b1111" and instr[11]:
            return SubsPcLrArmA1
        elif instr[12:16] == "0b1101":
            return AddSpPlusImmediateA1
        else:
            return AddImmediateArmA1
    elif instr[7:11] == "0b0100" and instr[12:16] == "0b1111":
        # Form PC-relative address
        return AdrA1
    elif instr[7:11] == "0b0101":
        # Add with Carry
        if instr[16:20] == "0b1111" and instr[11]:
            return SubsPcLrArmA1
        else:
            return AdcImmediateA1
    elif instr[7:11] == "0b0110":
        # Subtract with Carry
        if instr[16:20] == "0b1111" and instr[11]:
            return SubsPcLrArmA1
        else:
            return SbcImmediateA1
    elif instr[7:11] == "0b0111":
        # Reverse Subtract with Carry
        if instr[16:20] == "0b1111" and instr[11]:
            return SubsPcLrArmA1
        else:
            return RscImmediateA1
    elif instr[7:12] == "0b10001":
        # Test
        return TstImmediateA1
    elif instr[7:12] == "0b10011":
        # Test Equivalence
        return TeqImmediateA1
    elif instr[7:12] == "0b10101":
        # Compare
        return CmpImmediateA1
    elif instr[7:12] == "0b10111":
        # Compare Negative
        return CmnImmediateA1
    elif instr[7:11] == "0b1100":
        # Bitwise OR
        if instr[16:20] == "0b1111" and instr[11]:
            return SubsPcLrArmA1
        else:
            return OrrImmediateA1
    elif instr[7:11] == "0b1101":
        # Move
        if instr[16:20] == "0b1111" and instr[11]:
            return SubsPcLrArmA1
        else:
            return MovImmediateA1
    elif instr[7:11] == "0b1110":
        # Bitwise Bit Clear
        if instr[16:20] == "0b1111" and instr[11]:
            return SubsPcLrArmA1
        else:
            return BicImmediateA1
    elif instr[7:11] == "0b1111":
        # Bitwise NOT
        if instr[16:20] == "0b1111" and instr[11]:
            return SubsPcLrArmA1
        else:
            return MvnImmediateA1
