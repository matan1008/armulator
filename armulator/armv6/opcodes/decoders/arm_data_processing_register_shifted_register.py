from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.concrete.adc_register_shifted_register_a1 import AdcRegisterShiftedRegisterA1
from armulator.armv6.opcodes.concrete.add_register_shifted_register_a1 import AddRegisterShiftedRegisterA1
from armulator.armv6.opcodes.concrete.and_register_shifted_register_a1 import AndRegisterShiftedRegisterA1
from armulator.armv6.opcodes.concrete.asr_register_a1 import AsrRegisterA1
from armulator.armv6.opcodes.concrete.bic_register_shifted_register_a1 import BicRegisterShiftedRegisterA1
from armulator.armv6.opcodes.concrete.cmn_register_shifted_register_a1 import CmnRegisterShiftedRegisterA1
from armulator.armv6.opcodes.concrete.cmp_register_shifted_register_a1 import CmpRegisterShiftedRegisterA1
from armulator.armv6.opcodes.concrete.eor_register_shifted_register_a1 import EorRegisterShiftedRegisterA1
from armulator.armv6.opcodes.concrete.lsl_register_a1 import LslRegisterA1
from armulator.armv6.opcodes.concrete.lsr_register_a1 import LsrRegisterA1
from armulator.armv6.opcodes.concrete.mvn_register_shifted_register_a1 import MvnRegisterShiftedRegisterA1
from armulator.armv6.opcodes.concrete.orr_register_shifted_register_a1 import OrrRegisterShiftedRegisterA1
from armulator.armv6.opcodes.concrete.ror_register_a1 import RorRegisterA1
from armulator.armv6.opcodes.concrete.rsb_register_shifted_register_a1 import RsbRegisterShiftedRegisterA1
from armulator.armv6.opcodes.concrete.rsc_register_shifted_register_a1 import RscRegisterShiftedRegisterA1
from armulator.armv6.opcodes.concrete.sbc_register_shifted_register_a1 import SbcRegisterShiftedRegisterA1
from armulator.armv6.opcodes.concrete.sub_register_shifted_register_a1 import SubRegisterShiftedRegisterA1
from armulator.armv6.opcodes.concrete.teq_register_shifted_register_a1 import TeqRegisterShiftedRegisterA1
from armulator.armv6.opcodes.concrete.tst_register_shifted_register_a1 import TstRegisterShiftedRegisterA1


def decode_instruction(instr):
    instr_24_21 = substring(instr, 24, 21)
    op1 = substring(instr, 24, 20)
    op2 = substring(instr, 6, 5)
    if instr_24_21 == 0b0000:
        # Bitwise AND
        return AndRegisterShiftedRegisterA1
    elif instr_24_21 == 0b0001:
        # Bitwise Exclusive OR
        return EorRegisterShiftedRegisterA1
    elif instr_24_21 == 0b0010:
        # Subtract
        return SubRegisterShiftedRegisterA1
    elif instr_24_21 == 0b0011:
        # Reverse Subtract
        return RsbRegisterShiftedRegisterA1
    elif instr_24_21 == 0b0100:
        # Add
        return AddRegisterShiftedRegisterA1
    elif instr_24_21 == 0b0101:
        # Add with Carry
        return AdcRegisterShiftedRegisterA1
    elif instr_24_21 == 0b0110:
        # Subtract with Carry
        return SbcRegisterShiftedRegisterA1
    elif instr_24_21 == 0b0111:
        # Reverse Subtract with Carry
        return RscRegisterShiftedRegisterA1
    elif op1 == 0b10001:
        # Test
        return TstRegisterShiftedRegisterA1
    elif op1 == 0b10011:
        # Test Equivalence
        return TeqRegisterShiftedRegisterA1
    elif op1 == 0b10101:
        # Compare
        return CmpRegisterShiftedRegisterA1
    elif op1 == 0b10111:
        # Compare Negative
        return CmnRegisterShiftedRegisterA1
    elif instr_24_21 == 0b1100:
        # Bitwise OR
        return OrrRegisterShiftedRegisterA1
    elif instr_24_21 == 0b1101 and op2 == 0b00:
        # Logical Shift Left
        return LslRegisterA1
    elif instr_24_21 == 0b1101 and op2 == 0b01:
        # Logical Shift Right
        return LsrRegisterA1
    elif instr_24_21 == 0b1101 and op2 == 0b10:
        # Arithmetic Shift Right
        return AsrRegisterA1
    elif instr_24_21 == 0b1101 and op2 == 0b11:
        # Rotate Right
        return RorRegisterA1
    elif instr_24_21 == 0b1110:
        # Bitwise Bit Clear
        return BicRegisterShiftedRegisterA1
    elif instr_24_21 == 0b1111:
        # Bitwise NOT
        return MvnRegisterShiftedRegisterA1
