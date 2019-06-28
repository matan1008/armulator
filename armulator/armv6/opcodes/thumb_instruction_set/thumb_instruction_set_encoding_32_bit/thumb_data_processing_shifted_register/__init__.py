from __future__ import absolute_import
from .and_register_t2 import AndRegisterT2
from .tst_register_t2 import TstRegisterT2
from .bic_register_t2 import BicRegisterT2
from .orr_register_t2 import OrrRegisterT2
from . import thumb_move_register_and_immediate_shifts
from .orn_register_t1 import OrnRegisterT1
from .mvn_register_t2 import MvnRegisterT2
from .eor_register_t2 import EorRegisterT2
from .teq_register_t1 import TeqRegisterT1
from .pkhbt_t1 import PkhbtT1
from .add_register_thumb_t3 import AddRegisterThumbT3
from .add_sp_plus_register_thumb_t3 import AddSpPlusRegisterThumbT3
from .cmn_register_t2 import CmnRegisterT2
from .adc_register_t2 import AdcRegisterT2
from .sbc_register_t2 import SbcRegisterT2
from .sub_register_t2 import SubRegisterT2
from .sub_sp_minus_register_t1 import SubSpMinusRegisterT1
from .cmp_register_t3 import CmpRegisterT3
from .rsb_register_t1 import RsbRegisterT1


def decode_instruction(instr):
    if instr[7:11] == "0b0000" and (instr[20:24] + instr[11:12] != "0b11111"):
        # Bitwise AND
        return AndRegisterT2
    elif instr[7:11] == "0b0000" and (instr[20:24] + instr[11:12] == "0b11111"):
        # Test
        return TstRegisterT2
    elif instr[7:11] == "0b0001":
        # Bitwise Bit Clear
        return BicRegisterT2
    elif instr[7:11] == "0b0010" and instr[12:16] != "0b1111":
        # Bitwise OR
        return OrrRegisterT2
    elif instr[7:11] == "0b0010" and instr[12:16] == "0b1111":
        # Move register and immediate shifts
        return thumb_move_register_and_immediate_shifts.decode_instruction(instr)
    elif instr[7:11] == "0b0011" and instr[12:16] != "0b1111":
        # Bitwise OR NOT
        return OrnRegisterT1
    elif instr[7:11] == "0b0011" and instr[12:16] == "0b1111":
        # Bitwise NOT
        return MvnRegisterT2
    elif instr[7:11] == "0b0100" and (instr[20:24] + instr[11:12] != "0b11111"):
        # Bitwise Exclusive OR
        return EorRegisterT2
    elif instr[7:11] == "0b0100" and (instr[20:24] + instr[11:12] == "0b11111"):
        # Test Equivalence
        return TeqRegisterT1
    elif instr[7:11] == "0b0110":
        # Pack Halfword
        return PkhbtT1
    elif instr[7:11] == "0b1000" and (instr[20:24] + instr[11:12] != "0b11111"):
        # Add
        if instr[12:16] == "0b1101":
            return AddSpPlusRegisterThumbT3
        else:
            return AddRegisterThumbT3
    elif instr[7:11] == "0b1000" and (instr[20:24] + instr[11:12] == "0b11111"):
        # Compare Negative
        return CmnRegisterT2
    elif instr[7:11] == "0b1010":
        # Add with Carry
        return AdcRegisterT2
    elif instr[7:11] == "0b1011":
        # Subtract with Carry
        return SbcRegisterT2
    elif instr[7:11] == "0b1101" and (instr[20:24] + instr[11:12] != "0b11111"):
        # Subtract
        if instr[12:16] == "0b1101":
            return SubSpMinusRegisterT1
        else:
            return SubRegisterT2
    elif instr[7:11] == "0b1101" and (instr[20:24] + instr[11:12] == "0b11111"):
        # Compare
        return CmpRegisterT3
    elif instr[7:11] == "0b1110":
        # Reverse Subtract
        return RsbRegisterT1
