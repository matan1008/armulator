from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.concrete.adc_register_t1 import AdcRegisterT1
from armulator.armv6.opcodes.concrete.and_register_t1 import AndRegisterT1
from armulator.armv6.opcodes.concrete.asr_register_t1 import AsrRegisterT1
from armulator.armv6.opcodes.concrete.bic_register_t1 import BicRegisterT1
from armulator.armv6.opcodes.concrete.cmn_register_t1 import CmnRegisterT1
from armulator.armv6.opcodes.concrete.cmp_register_t1 import CmpRegisterT1
from armulator.armv6.opcodes.concrete.eor_register_t1 import EorRegisterT1
from armulator.armv6.opcodes.concrete.lsl_register_t1 import LslRegisterT1
from armulator.armv6.opcodes.concrete.lsr_register_t1 import LsrRegisterT1
from armulator.armv6.opcodes.concrete.mul_t1 import MulT1
from armulator.armv6.opcodes.concrete.mvn_register_t1 import MvnRegisterT1
from armulator.armv6.opcodes.concrete.orr_register_t1 import OrrRegisterT1
from armulator.armv6.opcodes.concrete.ror_register_t1 import RorRegisterT1
from armulator.armv6.opcodes.concrete.rsb_immediate_t1 import RsbImmediateT1
from armulator.armv6.opcodes.concrete.sbc_register_t1 import SbcRegisterT1
from armulator.armv6.opcodes.concrete.tst_register_t1 import TstRegisterT1


def decode_instruction(instr):
    instr_9_6 = substring(instr, 9, 6)
    if instr_9_6 == 0b0000:
        # Bitwise AND
        return AndRegisterT1
    elif instr_9_6 == 0b0001:
        # Bitwise Exclusive OR
        return EorRegisterT1
    elif instr_9_6 == 0b0010:
        # Logical Shift Left
        return LslRegisterT1
    elif instr_9_6 == 0b0011:
        # Logical Shift Right
        return LsrRegisterT1
    elif instr_9_6 == 0b0100:
        # Arithmetic Shift Right
        return AsrRegisterT1
    elif instr_9_6 == 0b0101:
        # Add with Carry
        return AdcRegisterT1
    elif instr_9_6 == 0b0110:
        # Subtract with Carry
        return SbcRegisterT1
    elif instr_9_6 == 0b0111:
        # Rotate Right
        return RorRegisterT1
    elif instr_9_6 == 0b1000:
        # Test
        return TstRegisterT1
    elif instr_9_6 == 0b1001:
        # Reverse Subtract from 0
        return RsbImmediateT1
    elif instr_9_6 == 0b1010:
        # Compare
        return CmpRegisterT1
    elif instr_9_6 == 0b1011:
        # Compare Negative
        return CmnRegisterT1
    elif instr_9_6 == 0b1100:
        # Bitwise OR
        return OrrRegisterT1
    elif instr_9_6 == 0b1101:
        # Multiply
        return MulT1
    elif instr_9_6 == 0b1110:
        # Bitwise Bit Clear
        return BicRegisterT1
    elif instr_9_6 == 0b1111:
        # Bitwise NOT
        return MvnRegisterT1
