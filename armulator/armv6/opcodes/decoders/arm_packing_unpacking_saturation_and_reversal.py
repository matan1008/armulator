from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.opcodes.concrete.pkh_a1 import PkhA1
from armulator.armv6.opcodes.concrete.rbit_a1 import RbitA1
from armulator.armv6.opcodes.concrete.rev16_a1 import Rev16A1
from armulator.armv6.opcodes.concrete.rev_a1 import RevA1
from armulator.armv6.opcodes.concrete.revsh_a1 import RevshA1
from armulator.armv6.opcodes.concrete.sel_a1 import SelA1
from armulator.armv6.opcodes.concrete.ssat16_a1 import Ssat16A1
from armulator.armv6.opcodes.concrete.ssat_a1 import SsatA1
from armulator.armv6.opcodes.concrete.sxtab16_a1 import Sxtab16A1
from armulator.armv6.opcodes.concrete.sxtab_a1 import SxtabA1
from armulator.armv6.opcodes.concrete.sxtah_a1 import SxtahA1
from armulator.armv6.opcodes.concrete.sxtb16_a1 import Sxtb16A1
from armulator.armv6.opcodes.concrete.sxtb_a1 import SxtbA1
from armulator.armv6.opcodes.concrete.sxth_a1 import SxthA1
from armulator.armv6.opcodes.concrete.usat16_a1 import Usat16A1
from armulator.armv6.opcodes.concrete.usat_a1 import UsatA1
from armulator.armv6.opcodes.concrete.uxtab16_a1 import Uxtab16A1
from armulator.armv6.opcodes.concrete.uxtab_a1 import UxtabA1
from armulator.armv6.opcodes.concrete.uxtah_a1 import UxtahA1
from armulator.armv6.opcodes.concrete.uxtb16_a1 import Uxtb16A1
from armulator.armv6.opcodes.concrete.uxtb_a1 import UxtbA1
from armulator.armv6.opcodes.concrete.uxth_a1 import UxthA1


def decode_instruction(instr):
    op1 = substring(instr, 22, 20)
    op2 = substring(instr, 7, 5)
    instr_5 = bit_at(instr, 5)
    a = substring(instr, 19, 16)
    instr_22_21 = substring(instr, 22, 21)
    if op1 == 0b000 and not instr_5:
        # Pack Halfword
        return PkhA1
    elif op1 == 0b000 and op2 == 0b011 and a != 0b1111:
        # Signed Extend and Add Byte 16-bit
        return Sxtab16A1
    elif op1 == 0b000 and op2 == 0b011 and a == 0b1111:
        # Signed Extend Byte 16-bit
        return Sxtb16A1
    elif op1 == 0b000 and op2 == 0b101:
        # Select Bytes
        return SelA1
    elif instr_22_21 == 0b01 and not instr_5:
        # Signed Saturate
        return SsatA1
    elif op1 == 0b010 and op2 == 0b001:
        # Signed Saturate, two 16-bit
        return Ssat16A1
    elif op1 == 0b010 and op2 == 0b011 and a != 0b1111:
        # Signed Extend and Add Byte
        return SxtabA1
    elif op1 == 0b010 and op2 == 0b011 and a == 0b1111:
        # Signed Extend Byte
        return SxtbA1
    elif op1 == 0b011 and op2 == 0b001:
        # Byte-Reverse Word
        return RevA1
    elif op1 == 0b011 and op2 == 0b011 and a != 0b1111:
        # Signed Extend and Add Halfword
        return SxtahA1
    elif op1 == 0b011 and op2 == 0b011 and a == 0b1111:
        # Signed Extend Halfword
        return SxthA1
    elif op1 == 0b011 and op2 == 0b101:
        # Byte-Reverse Packed Halfword
        return Rev16A1
    elif op1 == 0b100 and op2 == 0b011 and a != 0b1111:
        # Unsigned Extend and Add Byte 16-bit
        return Uxtab16A1
    elif op1 == 0b100 and op2 == 0b011 and a == 0b1111:
        # Unsigned Extend Byte 16-bit
        return Uxtb16A1
    elif instr_22_21 == 0b11 and not instr_5:
        # Unsigned Saturate
        return UsatA1
    elif op1 == 0b110 and op2 == 0b001:
        # Unsigned Saturate, two 16-bit
        return Usat16A1
    elif op1 == 0b110 and op2 == 0b011 and a != 0b1111:
        # Unsigned Extend and Add Byte
        return UxtabA1
    elif op1 == 0b110 and op2 == 0b011 and a == 0b1111:
        # Unsigned Extend Byte
        return UxtbA1
    elif op1 == 0b111 and op2 == 0b001:
        # Reverse Bits
        return RbitA1
    elif op1 == 0b111 and op2 == 0b011 and a != 0b1111:
        # Unsigned Extend and Add Halfword
        return UxtahA1
    elif op1 == 0b111 and op2 == 0b011 and a == 0b1111:
        # Unsigned Extend Byte
        return UxthA1
    elif op1 == 0b111 and op2 == 0b101:
        # Byte-Reverse Signed Halfword
        return RevshA1
