from and_register_shifted_register_a1 import AndRegisterShiftedRegisterA1
from eor_register_shifted_register_a1 import EorRegisterShiftedRegisterA1
from sub_register_shifted_register_a1 import SubRegisterShiftedRegisterA1
from rsb_register_shifted_register_a1 import RsbRegisterShiftedRegisterA1
from add_register_shifted_register_a1 import AddRegisterShiftedRegisterA1
from adc_register_shifted_register_a1 import AdcRegisterShiftedRegisterA1
from sbc_register_shifted_register_a1 import SbcRegisterShiftedRegisterA1
from rsc_register_shifted_register_a1 import RscRegisterShiftedRegisterA1
from tst_register_shifted_register_a1 import TstRegisterShiftedRegisterA1
from teq_register_shifted_register_a1 import TeqRegisterShiftedRegisterA1
from cmp_register_shifted_register_a1 import CmpRegisterShiftedRegisterA1
from cmn_register_shifted_register_a1 import CmnRegisterShiftedRegisterA1
from orr_register_shifted_register_a1 import OrrRegisterShiftedRegisterA1
from lsl_register_a1 import LslRegisterA1
from lsr_register_a1 import LsrRegisterA1
from asr_register_a1 import AsrRegisterA1
from ror_register_a1 import RorRegisterA1
from bic_register_shifted_register_a1 import BicRegisterShiftedRegisterA1
from mvn_register_shifted_register_a1 import MvnRegisterShiftedRegisterA1


def decode_instruction(instr):
    if instr[7:11] == "0b0000":
        # Bitwise AND
        return AndRegisterShiftedRegisterA1
    elif instr[7:11] == "0b0001":
        # Bitwise Exclusive OR
        return EorRegisterShiftedRegisterA1
    elif instr[7:11] == "0b0010":
        # Subtract
        return SubRegisterShiftedRegisterA1
    elif instr[7:11] == "0b0011":
        # Reverse Subtract
        return RsbRegisterShiftedRegisterA1
    elif instr[7:11] == "0b0100":
        # Add
        return AddRegisterShiftedRegisterA1
    elif instr[7:11] == "0b0101":
        # Add with Carry
        return AdcRegisterShiftedRegisterA1
    elif instr[7:11] == "0b0110":
        # Subtract with Carry
        return SbcRegisterShiftedRegisterA1
    elif instr[7:11] == "0b0111":
        # Reverse Subtract with Carry
        return RscRegisterShiftedRegisterA1
    elif instr[7:12] == "0b10001":
        # Test
        return TstRegisterShiftedRegisterA1
    elif instr[7:12] == "0b10011":
        # Test Equivalence
        return TeqRegisterShiftedRegisterA1
    elif instr[7:12] == "0b10101":
        # Compare
        return CmpRegisterShiftedRegisterA1
    elif instr[7:12] == "0b10111":
        # Compare Negative
        return CmnRegisterShiftedRegisterA1
    elif instr[7:11] == "0b1100":
        # Bitwise OR
        return OrrRegisterShiftedRegisterA1
    elif instr[7:11] == "0b1101" and instr[25:27] == "0b00":
        # Logical Shift Left
        return LslRegisterA1
    elif instr[7:11] == "0b1101" and instr[25:27] == "0b01":
        # Logical Shift Right
        return LsrRegisterA1
    elif instr[7:11] == "0b1101" and instr[25:27] == "0b10":
        # Arithmetic Shift Right
        return AsrRegisterA1
    elif instr[7:11] == "0b1101" and instr[25:27] == "0b11":
        # Rotate Right
        return RorRegisterA1
    elif instr[7:11] == "0b1110":
        # Bitwise Bit Clear
        return BicRegisterShiftedRegisterA1
    elif instr[7:11] == "0b1111":
        # Bitwise NOT
        return MvnRegisterShiftedRegisterA1
