from armulator.armv6.bits_ops import substring, chain, bit_at
from armulator.armv6.opcodes.concrete.adc_register_t2 import AdcRegisterT2
from armulator.armv6.opcodes.concrete.add_register_thumb_t3 import AddRegisterThumbT3
from armulator.armv6.opcodes.concrete.add_sp_plus_register_thumb_t3 import AddSpPlusRegisterThumbT3
from armulator.armv6.opcodes.concrete.and_register_t2 import AndRegisterT2
from armulator.armv6.opcodes.concrete.bic_register_t2 import BicRegisterT2
from armulator.armv6.opcodes.concrete.cmn_register_t2 import CmnRegisterT2
from armulator.armv6.opcodes.concrete.cmp_register_t3 import CmpRegisterT3
from armulator.armv6.opcodes.concrete.eor_register_t2 import EorRegisterT2
from armulator.armv6.opcodes.concrete.mvn_register_t2 import MvnRegisterT2
from armulator.armv6.opcodes.concrete.orn_register_t1 import OrnRegisterT1
from armulator.armv6.opcodes.concrete.orr_register_t2 import OrrRegisterT2
from armulator.armv6.opcodes.concrete.pkh_t1 import PkhT1
from armulator.armv6.opcodes.concrete.rsb_register_t1 import RsbRegisterT1
from armulator.armv6.opcodes.concrete.sbc_register_t2 import SbcRegisterT2
from armulator.armv6.opcodes.concrete.sub_register_t2 import SubRegisterT2
from armulator.armv6.opcodes.concrete.sub_sp_minus_register_t1 import SubSpMinusRegisterT1
from armulator.armv6.opcodes.concrete.teq_register_t1 import TeqRegisterT1
from armulator.armv6.opcodes.concrete.tst_register_t2 import TstRegisterT2
from armulator.armv6.opcodes.decoders import thumb_move_register_and_immediate_shifts


def decode_instruction(instr):
    instr_op = substring(instr, 24, 21)
    instr_rd_s = chain(substring(instr, 11, 8), bit_at(instr, 20), 1)
    instr_rn = substring(instr, 19, 16)
    if instr_op == 0b0000 and instr_rd_s != 0b11111:
        # Bitwise AND
        return AndRegisterT2
    elif instr_op == 0b0000 and instr_rd_s == 0b11111:
        # Test
        return TstRegisterT2
    elif instr_op == 0b0001:
        # Bitwise Bit Clear
        return BicRegisterT2
    elif instr_op == 0b0010 and instr_rn != 0b1111:
        # Bitwise OR
        return OrrRegisterT2
    elif instr_op == 0b0010 and instr_rn == 0b1111:
        # Move register and immediate shifts
        return thumb_move_register_and_immediate_shifts.decode_instruction(instr)
    elif instr_op == 0b0011 and instr_rn != 0b1111:
        # Bitwise OR NOT
        return OrnRegisterT1
    elif instr_op == 0b0011 and instr_rn == 0b1111:
        # Bitwise NOT
        return MvnRegisterT2
    elif instr_op == 0b0100 and instr_rd_s != 0b11111:
        # Bitwise Exclusive OR
        return EorRegisterT2
    elif instr_op == 0b0100 and instr_rd_s == 0b11111:
        # Test Equivalence
        return TeqRegisterT1
    elif instr_op == 0b0110:
        # Pack Halfword
        return PkhT1
    elif instr_op == 0b1000 and instr_rd_s != 0b11111:
        # Add
        if instr_rn == 0b1101:
            return AddSpPlusRegisterThumbT3
        else:
            return AddRegisterThumbT3
    elif instr_op == 0b1000 and instr_rd_s == 0b11111:
        # Compare Negative
        return CmnRegisterT2
    elif instr_op == 0b1010:
        # Add with Carry
        return AdcRegisterT2
    elif instr_op == 0b1011:
        # Subtract with Carry
        return SbcRegisterT2
    elif instr_op == 0b1101 and instr_rd_s != 0b11111:
        # Subtract
        if instr_rn == 0b1101:
            return SubSpMinusRegisterT1
        else:
            return SubRegisterT2
    elif instr_op == 0b1101 and instr_rd_s == 0b11111:
        # Compare
        return CmpRegisterT3
    elif instr_op == 0b1110:
        # Reverse Subtract
        return RsbRegisterT1
