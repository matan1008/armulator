from subs_pc_lr_arm_a2 import SubsPcLrArmA2
from and_register_a1 import AndRegisterA1
from eor_register_a1 import EorRegisterA1
from sub_sp_minus_register_a1 import SubSpMinusRegisterA1
from sub_register_a1 import SubRegisterA1
from rsb_register_a1 import RsbRegisterA1
from add_sp_plus_register_arm_a1 import AddSpPlusRegisterArmA1
from add_register_arm_a1 import AddRegisterArmA1
from adc_register_a1 import AdcRegisterA1
from sbc_register_a1 import SbcRegisterA1
from rsc_register_a1 import RscRegisterA1
from tst_register_a1 import TstRegisterA1
from teq_register_a1 import TeqRegisterA1
from cmp_register_a1 import CmpRegisterA1
from cmn_register_a1 import CmnRegisterA1
from orr_register_a1 import OrrRegisterA1
from mov_register_arm_a1 import MovRegisterArmA1
from lsl_immediate_a1 import LslImmediateA1
from lsr_immediate_a1 import LsrImmediateA1
from asr_immediate_a1 import AsrImmediateA1
from rrx_a1 import RrxA1
from ror_immediate_a1 import RorImmediateA1
from bic_register_a1 import BicRegisterA1
from mvn_register_a1 import MvnRegisterA1


def decode_instruction(instr):
    if instr[7:11] == "0b0000":
        # Bitwise AND
        if instr[16:20] == "0b1111" and instr[11]:
            return SubsPcLrArmA2
        else:
            return AndRegisterA1
    elif instr[7:11] == "0b0001":
        # Bitwise Exclusive OR
        if instr[16:20] == "0b1111" and instr[11]:
            return SubsPcLrArmA2
        else:
            return EorRegisterA1
    elif instr[7:11] == "0b0010":
        # Substract
        if instr[16:20] == "0b1111" and instr[11]:
            return SubsPcLrArmA2
        elif instr[12:16] == "0b1101":
            return SubSpMinusRegisterA1
        else:
            return SubRegisterA1
    elif instr[7:11] == "0b0011":
        # Reverse Substract
        if instr[16:20] == "0b1111" and instr[11]:
            return SubsPcLrArmA2
        else:
            return RsbRegisterA1
    elif instr[7:11] == "0b0100":
        # Add
        if instr[16:20] == "0b1111" and instr[11]:
            return SubsPcLrArmA2
        elif instr[12:16] == "0b1101":
            return AddSpPlusRegisterArmA1
        else:
            return AddRegisterArmA1
    elif instr[7:11] == "0b0101":
        # Add with Carry
        if instr[16:20] == "0b1111" and instr[11]:
            return SubsPcLrArmA2
        else:
            return AdcRegisterA1
    elif instr[7:11] == "0b0110":
        # Subtarct with Carry
        if instr[16:20] == "0b1111" and instr[11]:
            return SubsPcLrArmA2
        else:
            return SbcRegisterA1
    elif instr[7:11] == "0b0111":
        # Reverse Subtarct with Carry
        if instr[16:20] == "0b1111" and instr[11]:
            return SubsPcLrArmA2
        else:
            return RscRegisterA1
    elif instr[7:12] == "0b10001":
        # Test
        return TstRegisterA1
    elif instr[7:12] == "0b10011":
        # Test Equivalence
        return TeqRegisterA1
    elif instr.bin[7:12] == "10101":
        # Compare
        return CmpRegisterA1
    elif instr.bin[7:12] == "10111":
        # Compare Negative
        return CmnRegisterA1
    elif instr.bin[7:11] == "1100":
        # Bitwise OR
        if instr[16:20] == "0b1111" and instr[11]:
            return SubsPcLrArmA2
        else:
            return OrrRegisterA1
    elif instr.bin[7:11] == "1100" and instr.bin[25:27] == "00" and instr.bin[20:25] == "00000":
        # Move
        if instr[16:20] == "0b1111" and instr[11]:
            return SubsPcLrArmA2
        else:
            return MovRegisterArmA1
    elif instr.bin[7:11] == "1100" and instr.bin[25:27] == "00" and instr.bin[20:25] != "00000":
        # Logical Shift Left
        if instr[16:20] == "0b1111" and instr[11]:
            return SubsPcLrArmA2
        else:
            return LslImmediateA1
    elif instr.bin[7:11] == "1100" and instr.bin[25:27] == "01":
        # Logical Shift Right
        if instr[16:20] == "0b1111" and instr[11]:
            return SubsPcLrArmA2
        else:
            return LsrImmediateA1
    elif instr.bin[7:11] == "1100" and instr.bin[25:27] == "10":
        # Arithmetic Shift Right
        if instr[16:20] == "0b1111" and instr[11]:
            return SubsPcLrArmA2
        else:
            return AsrImmediateA1
    elif instr.bin[7:11] == "1100" and instr.bin[25:27] == "11" and instr.bin[20:25] == "00000":
        # Rotate Right with Extend
        if instr[16:20] == "0b1111" and instr[11]:
            return SubsPcLrArmA2
        else:
            return RrxA1
    elif instr.bin[7:11] == "1100" and instr.bin[25:27] == "11" and instr.bin[20:25] != "00000":
        # Rotate Right
        if instr[16:20] == "0b1111" and instr[11]:
            return SubsPcLrArmA2
        else:
            return RorImmediateA1
    elif instr.bin[7:11] == "1110":
        # Bitwise Bit Clear
        if instr[16:20] == "0b1111" and instr[11]:
            return SubsPcLrArmA2
        else:
            return BicRegisterA1
    elif instr.bin[7:11] == "1111":
        # Bitwise NOT
        if instr[16:20] == "0b1111" and instr[11]:
            return SubsPcLrArmA2
        else:
            return MvnRegisterA1
