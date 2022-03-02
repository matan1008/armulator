from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.opcodes.concrete.adc_immediate_t1 import AdcImmediateT1
from armulator.armv6.opcodes.concrete.add_immediate_thumb_t3 import AddImmediateThumbT3
from armulator.armv6.opcodes.concrete.add_sp_plus_immediate_t3 import AddSpPlusImmediateT3
from armulator.armv6.opcodes.concrete.and_immediate_t1 import AndImmediateT1
from armulator.armv6.opcodes.concrete.bic_immediate_t1 import BicImmediateT1
from armulator.armv6.opcodes.concrete.cmn_immediate_t1 import CmnImmediateT1
from armulator.armv6.opcodes.concrete.eor_immediate_t1 import EorImmediateT1
from armulator.armv6.opcodes.concrete.mov_immediate_t2 import MovImmediateT2
from armulator.armv6.opcodes.concrete.mvn_immediate_t1 import MvnImmediateT1
from armulator.armv6.opcodes.concrete.orn_immediate_t1 import OrnImmediateT1
from armulator.armv6.opcodes.concrete.orr_immediate_t1 import OrrImmediateT1
from armulator.armv6.opcodes.concrete.sbc_immediate_t1 import SbcImmediateT1
from armulator.armv6.opcodes.concrete.teq_immediate_t1 import TeqImmediateT1
from armulator.armv6.opcodes.concrete.tst_immediate_t1 import TstImmediateT1
from armulator.armv6.opcodes.concrete.cmp_immediate_t2 import CmpImmediateT2
from armulator.armv6.opcodes.concrete.rsb_immediate_t2 import RsbImmediateT2
from armulator.armv6.opcodes.concrete.sub_immediate_thumb_t3 import SubImmediateThumbT3
from armulator.armv6.opcodes.concrete.sub_sp_minus_immediate_t2 import SubSpMinusImmediateT2


def decode_instruction(instr):
    instr_op = substring(instr, 24, 21)
    instr_rd = substring(instr, 11, 8)
    instr_s = bit_at(instr, 20)
    instr_rn = substring(instr, 19, 16)
    if instr_op == 0b0000 and not (instr_rd == 0b1111 and instr_s):
        # Bitwise AND
        return AndImmediateT1
    elif instr_op == 0b0000 and (instr_rd == 0b1111 and instr_s):
        # Test
        return TstImmediateT1
    elif instr_op == 0b0001:
        # Bitwise Bit Clear
        return BicImmediateT1
    elif instr_op == 0b0010 and instr_rn != 0b1111:
        # Bitwise OR
        return OrrImmediateT1
    elif instr_op == 0b0010 and instr_rn == 0b1111:
        # Move
        return MovImmediateT2
    elif instr_op == 0b0011 and instr_rn != 0b1111:
        # Bitwise OR NOT
        return OrnImmediateT1
    elif instr_op == 0b0011 and instr_rn == 0b1111:
        # Bitwise NOT
        return MvnImmediateT1
    elif instr_op == 0b0100 and not (instr_rd == 0b1111 and instr_s):
        # Bitwise Exclusive OR
        return EorImmediateT1
    elif instr_op == 0b0100 and (instr_rd == 0b1111 and instr_s):
        # Test Equivalence
        return TeqImmediateT1
    elif instr_op == 0b1000 and not (instr_rd == 0b1111 and instr_s):
        # Add
        if instr_rn == 0b1101:
            return AddSpPlusImmediateT3
        else:
            return AddImmediateThumbT3
    elif instr_op == 0b1000 and (instr_rd == 0b1111 and instr_s):
        # Compare Negative
        return CmnImmediateT1
    elif instr_op == 0b1010:
        # Add with Carry
        return AdcImmediateT1
    elif instr_op == 0b1011:
        # Subtract with Carry
        return SbcImmediateT1
    elif instr_op == 0b1101 and not (instr_rd == 0b1111 and instr_s):
        # Subtract
        if instr_rn == 0b1101:
            return SubSpMinusImmediateT2
        else:
            return SubImmediateThumbT3
    elif instr_op == 0b1101 and (instr_rd == 0b1111 and instr_s):
        # Compare
        return CmpImmediateT2
    elif instr_op == 0b1110:
        # Reverse Subtract
        return RsbImmediateT2
