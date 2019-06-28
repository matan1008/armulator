from __future__ import absolute_import
from .and_register_t1 import AndRegisterT1
from .eor_register_t1 import EorRegisterT1
from .lsl_register_t1 import LslRegisterT1
from .lsr_register_t1 import LsrRegisterT1
from .asr_register_t1 import AsrRegisterT1
from .adc_register_t1 import AdcRegisterT1
from .sbc_register_t1 import SbcRegisterT1
from .ror_register_t1 import RorRegisterT1
from .tst_register_t1 import TstRegisterT1
from .rsb_immediate_t1 import RsbImmediateT1
from .cmp_register_t1 import CmpRegisterT1
from .cmn_register_t1 import CmnRegisterT1
from .orr_register_t1 import OrrRegisterT1
from .mul_t1 import MulT1
from .bic_register_t1 import BicRegisterT1
from .mvn_register_t1 import MvnRegisterT1


def decode_instruction(instr):
    if instr[6:10] == "0b0000":
        # Bitwise AND
        return AndRegisterT1
    elif instr[6:10] == "0b0001":
        # Bitwise Exclusive OR
        return EorRegisterT1
    elif instr[6:10] == "0b0010":
        # Logical Shift Left
        return LslRegisterT1
    elif instr[6:10] == "0b0011":
        # Logical Shift Right
        return LsrRegisterT1
    elif instr[6:10] == "0b0100":
        # Arithmetic Shift Right
        return AsrRegisterT1
    elif instr[6:10] == "0b0101":
        # Add with Carry
        return AdcRegisterT1
    elif instr[6:10] == "0b0110":
        # Subtract with Carry
        return SbcRegisterT1
    elif instr[6:10] == "0b0111":
        # Rotate Right
        return RorRegisterT1
    elif instr[6:10] == "0b1000":
        # Test
        return TstRegisterT1
    elif instr[6:10] == "0b1001":
        # Reverse Subtract from 0
        return RsbImmediateT1
    elif instr[6:10] == "0b1010":
        # Compare
        return CmpRegisterT1
    elif instr[6:10] == "0b1011":
        # Compare Negative
        return CmnRegisterT1
    elif instr[6:10] == "0b1100":
        # Bitwise OR
        return OrrRegisterT1
    elif instr[6:10] == "0b1101":
        # Multiply
        return MulT1
    elif instr[6:10] == "0b1110":
        # Bitwise Bit Clear
        return BicRegisterT1
    elif instr[6:10] == "0b1111":
        # Bitwise NOT
        return MvnRegisterT1
