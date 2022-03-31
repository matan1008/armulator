from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.opcodes.concrete.adc_immediate_a1 import AdcImmediateA1
from armulator.armv6.opcodes.concrete.add_immediate_arm_a1 import AddImmediateArmA1
from armulator.armv6.opcodes.concrete.add_sp_plus_immediate_a1 import AddSpPlusImmediateA1
from armulator.armv6.opcodes.concrete.adr_a1 import AdrA1
from armulator.armv6.opcodes.concrete.adr_a2 import AdrA2
from armulator.armv6.opcodes.concrete.and_immediate_a1 import AndImmediateA1
from armulator.armv6.opcodes.concrete.bic_immediate_a1 import BicImmediateA1
from armulator.armv6.opcodes.concrete.cmn_immediate_a1 import CmnImmediateA1
from armulator.armv6.opcodes.concrete.cmp_immediate_a1 import CmpImmediateA1
from armulator.armv6.opcodes.concrete.eor_immediate_a1 import EorImmediateA1
from armulator.armv6.opcodes.concrete.mov_immediate_a1 import MovImmediateA1
from armulator.armv6.opcodes.concrete.mvn_immediate_a1 import MvnImmediateA1
from armulator.armv6.opcodes.concrete.orr_immediate_a1 import OrrImmediateA1
from armulator.armv6.opcodes.concrete.rsb_immediate_a1 import RsbImmediateA1
from armulator.armv6.opcodes.concrete.rsc_immediate_a1 import RscImmediateA1
from armulator.armv6.opcodes.concrete.sbc_immediate_a1 import SbcImmediateA1
from armulator.armv6.opcodes.concrete.sub_immediate_arm_a1 import SubImmediateArmA1
from armulator.armv6.opcodes.concrete.sub_sp_minus_immediate_a1 import SubSpMinusImmediateA1
from armulator.armv6.opcodes.concrete.subs_pc_lr_arm_a1 import SubsPcLrArmA1
from armulator.armv6.opcodes.concrete.teq_immediate_a1 import TeqImmediateA1
from armulator.armv6.opcodes.concrete.tst_immediate_a1 import TstImmediateA1


def decode_instruction(instr):
    instr_24_21 = substring(instr, 24, 21)
    op = substring(instr, 24, 20)
    rn = substring(instr, 19, 16)
    instr_15_12 = substring(instr, 15, 12)
    instr_20 = bit_at(instr, 20)
    if instr_24_21 == 0b0000:
        # Bitwise AND
        if instr_15_12 == 0b1111 and instr_20:
            return SubsPcLrArmA1
        else:
            return AndImmediateA1
    elif instr_24_21 == 0b0001:
        # Bitwise Exclusive OR
        if instr_15_12 == 0b1111 and instr_20:
            return SubsPcLrArmA1
        else:
            return EorImmediateA1
    elif instr_24_21 == 0b0010 and rn != 0b1111:
        # Subtract
        if instr_15_12 == 0b1111 and instr_20:
            return SubsPcLrArmA1
        elif rn == 0b1101:
            return SubSpMinusImmediateA1
        else:
            return SubImmediateArmA1
    elif instr_24_21 == 0b0010 and rn == 0b1111:
        # Form PC-relative address
        return AdrA2
    elif instr_24_21 == 0b0011:
        # Reverse Subtract
        if instr_15_12 == 0b1111 and instr_20:
            return SubsPcLrArmA1
        else:
            return RsbImmediateA1
    elif instr_24_21 == 0b0100 and rn != 0b1111:
        # Add
        if instr_15_12 == 0b1111 and instr_20:
            return SubsPcLrArmA1
        elif rn == 0b1101:
            return AddSpPlusImmediateA1
        else:
            return AddImmediateArmA1
    elif instr_24_21 == 0b0100 and rn == 0b1111:
        # Form PC-relative address
        return AdrA1
    elif instr_24_21 == 0b0101:
        # Add with Carry
        if instr_15_12 == 0b1111 and instr_20:
            return SubsPcLrArmA1
        else:
            return AdcImmediateA1
    elif instr_24_21 == 0b0110:
        # Subtract with Carry
        if instr_15_12 == 0b1111 and instr_20:
            return SubsPcLrArmA1
        else:
            return SbcImmediateA1
    elif instr_24_21 == 0b0111:
        # Reverse Subtract with Carry
        if instr_15_12 == 0b1111 and instr_20:
            return SubsPcLrArmA1
        else:
            return RscImmediateA1
    elif op == 0b10001:
        # Test
        return TstImmediateA1
    elif op == 0b10011:
        # Test Equivalence
        return TeqImmediateA1
    elif op == 0b10101:
        # Compare
        return CmpImmediateA1
    elif op == 0b10111:
        # Compare Negative
        return CmnImmediateA1
    elif instr_24_21 == 0b1100:
        # Bitwise OR
        if instr_15_12 == 0b1111 and instr_20:
            return SubsPcLrArmA1
        else:
            return OrrImmediateA1
    elif instr_24_21 == 0b1101:
        # Move
        if instr_15_12 == 0b1111 and instr_20:
            return SubsPcLrArmA1
        else:
            return MovImmediateA1
    elif instr_24_21 == 0b1110:
        # Bitwise Bit Clear
        if instr_15_12 == 0b1111 and instr_20:
            return SubsPcLrArmA1
        else:
            return BicImmediateA1
    elif instr_24_21 == 0b1111:
        # Bitwise NOT
        if instr_15_12 == 0b1111 and instr_20:
            return SubsPcLrArmA1
        else:
            return MvnImmediateA1
