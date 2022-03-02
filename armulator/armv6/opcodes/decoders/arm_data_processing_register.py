from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.opcodes.concrete.adc_register_a1 import AdcRegisterA1
from armulator.armv6.opcodes.concrete.add_register_arm_a1 import AddRegisterArmA1
from armulator.armv6.opcodes.concrete.add_sp_plus_register_arm_a1 import AddSpPlusRegisterArmA1
from armulator.armv6.opcodes.concrete.and_register_a1 import AndRegisterA1
from armulator.armv6.opcodes.concrete.asr_immediate_a1 import AsrImmediateA1
from armulator.armv6.opcodes.concrete.bic_register_a1 import BicRegisterA1
from armulator.armv6.opcodes.concrete.cmn_register_a1 import CmnRegisterA1
from armulator.armv6.opcodes.concrete.cmp_register_a1 import CmpRegisterA1
from armulator.armv6.opcodes.concrete.eor_register_a1 import EorRegisterA1
from armulator.armv6.opcodes.concrete.lsl_immediate_a1 import LslImmediateA1
from armulator.armv6.opcodes.concrete.lsr_immediate_a1 import LsrImmediateA1
from armulator.armv6.opcodes.concrete.mov_register_arm_a1 import MovRegisterArmA1
from armulator.armv6.opcodes.concrete.mvn_register_a1 import MvnRegisterA1
from armulator.armv6.opcodes.concrete.orr_register_a1 import OrrRegisterA1
from armulator.armv6.opcodes.concrete.ror_immediate_a1 import RorImmediateA1
from armulator.armv6.opcodes.concrete.rrx_a1 import RrxA1
from armulator.armv6.opcodes.concrete.rsb_register_a1 import RsbRegisterA1
from armulator.armv6.opcodes.concrete.rsc_register_a1 import RscRegisterA1
from armulator.armv6.opcodes.concrete.sbc_register_a1 import SbcRegisterA1
from armulator.armv6.opcodes.concrete.sub_register_a1 import SubRegisterA1
from armulator.armv6.opcodes.concrete.sub_sp_minus_register_a1 import SubSpMinusRegisterA1
from armulator.armv6.opcodes.concrete.subs_pc_lr_arm_a2 import SubsPcLrArmA2
from armulator.armv6.opcodes.concrete.teq_register_a1 import TeqRegisterA1
from armulator.armv6.opcodes.concrete.tst_register_a1 import TstRegisterA1


def decode_instruction(instr):
    instr_24_21 = substring(instr, 24, 21)
    instr_15_12 = substring(instr, 15, 12)
    instr_20 = bit_at(instr, 20)
    instr_19_16 = substring(instr, 19, 16)
    op = substring(instr, 24, 20)
    op2 = substring(instr, 6, 5)
    imm5 = substring(instr, 11, 7)
    if instr_24_21 == 0b0000:
        # Bitwise AND
        if instr_15_12 == 0b1111 and instr_20:
            return SubsPcLrArmA2
        else:
            return AndRegisterA1
    elif instr_24_21 == 0b0001:
        # Bitwise Exclusive OR
        if instr_15_12 == 0b1111 and instr_20:
            return SubsPcLrArmA2
        else:
            return EorRegisterA1
    elif instr_24_21 == 0b0010:
        # Subtract
        if instr_15_12 == 0b1111 and instr_20:
            return SubsPcLrArmA2
        elif instr_19_16 == 0b1101:
            return SubSpMinusRegisterA1
        else:
            return SubRegisterA1
    elif instr_24_21 == 0b0011:
        # Reverse Subtract
        if instr_15_12 == 0b1111 and instr_20:
            return SubsPcLrArmA2
        else:
            return RsbRegisterA1
    elif instr_24_21 == 0b0100:
        # Add
        if instr_15_12 == 0b1111 and instr_20:
            return SubsPcLrArmA2
        elif instr_19_16 == 0b1101:
            return AddSpPlusRegisterArmA1
        else:
            return AddRegisterArmA1
    elif instr_24_21 == 0b0101:
        # Add with Carry
        if instr_15_12 == 0b1111 and instr_20:
            return SubsPcLrArmA2
        else:
            return AdcRegisterA1
    elif instr_24_21 == 0b0110:
        # Subtarct with Carry
        if instr_15_12 == 0b1111 and instr_20:
            return SubsPcLrArmA2
        else:
            return SbcRegisterA1
    elif instr_24_21 == 0b0111:
        # Reverse Subtarct with Carry
        if instr_15_12 == 0b1111 and instr_20:
            return SubsPcLrArmA2
        else:
            return RscRegisterA1
    elif op == 0b10001:
        # Test
        return TstRegisterA1
    elif op == 0b10011:
        # Test Equivalence
        return TeqRegisterA1
    elif op == 0b10101:
        # Compare
        return CmpRegisterA1
    elif op == 0b10111:
        # Compare Negative
        return CmnRegisterA1
    elif instr_24_21 == 0b1100:
        # Bitwise OR
        if instr_15_12 == 0b1111 and instr_20:
            return SubsPcLrArmA2
        else:
            return OrrRegisterA1
    elif instr_24_21 == 0b1101 and op2 == 0b00 and imm5 == 0b00000:
        # Move
        if instr_15_12 == 0b1111 and instr_20:
            return SubsPcLrArmA2
        else:
            return MovRegisterArmA1
    elif instr_24_21 == 0b1101 and op2 == 0b00 and imm5 != 0b00000:
        # Logical Shift Left
        if instr_15_12 == 0b1111 and instr_20:
            return SubsPcLrArmA2
        else:
            return LslImmediateA1
    elif instr_24_21 == 0b1101 and op2 == 0b01:
        # Logical Shift Right
        if instr_15_12 == 0b1111 and instr_20:
            return SubsPcLrArmA2
        else:
            return LsrImmediateA1
    elif instr_24_21 == 0b1101 and op2 == 0b10:
        # Arithmetic Shift Right
        if instr_15_12 == 0b1111 and instr_20:
            return SubsPcLrArmA2
        else:
            return AsrImmediateA1
    elif instr_24_21 == 0b1101 and op2 == 0b11 and imm5 == 0b00000:
        # Rotate Right with Extend
        if instr_15_12 == 0b1111 and instr_20:
            return SubsPcLrArmA2
        else:
            return RrxA1
    elif instr_24_21 == 0b1101 and op2 == 0b11 and imm5 != 0b00000:
        # Rotate Right
        if instr_15_12 == 0b1111 and instr_20:
            return SubsPcLrArmA2
        else:
            return RorImmediateA1
    elif instr_24_21 == 0b1110:
        # Bitwise Bit Clear
        if instr_15_12 == 0b1111 and instr_20:
            return SubsPcLrArmA2
        else:
            return BicRegisterA1
    elif instr_24_21 == 0b1111:
        # Bitwise NOT
        if instr_15_12 == 0b1111 and instr_20:
            return SubsPcLrArmA2
        else:
            return MvnRegisterA1
