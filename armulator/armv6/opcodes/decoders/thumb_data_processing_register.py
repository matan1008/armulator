from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.opcodes.concrete.asr_register_t2 import AsrRegisterT2
from armulator.armv6.opcodes.concrete.lsl_register_t2 import LslRegisterT2
from armulator.armv6.opcodes.concrete.lsr_register_t2 import LsrRegisterT2
from armulator.armv6.opcodes.concrete.ror_register_t2 import RorRegisterT2
from armulator.armv6.opcodes.concrete.sxtab16_t1 import Sxtab16T1
from armulator.armv6.opcodes.concrete.sxtab_t1 import SxtabT1
from armulator.armv6.opcodes.concrete.sxtah_t1 import SxtahT1
from armulator.armv6.opcodes.concrete.sxtb16_t1 import Sxtb16T1
from armulator.armv6.opcodes.concrete.sxtb_t2 import SxtbT2
from armulator.armv6.opcodes.concrete.sxth_t2 import SxthT2
from armulator.armv6.opcodes.concrete.uxtab16_t1 import Uxtab16T1
from armulator.armv6.opcodes.concrete.uxtab_t1 import UxtabT1
from armulator.armv6.opcodes.concrete.uxtah_t1 import UxtahT1
from armulator.armv6.opcodes.concrete.uxtb16_t1 import Uxtb16T1
from armulator.armv6.opcodes.concrete.uxtb_t2 import UxtbT2
from armulator.armv6.opcodes.concrete.uxth_t2 import UxthT2
from armulator.armv6.opcodes.decoders import thumb_miscellaneous_operations
from armulator.armv6.opcodes.decoders import thumb_parallel_addition_and_subtraction_signed
from armulator.armv6.opcodes.decoders import thumb_parallel_addition_and_subtraction_unsigned


def decode_instruction(instr):
    instr_23_21 = substring(instr, 23, 21)
    op2 = substring(instr, 7, 4)
    op1 = substring(instr, 23, 20)
    rn = substring(instr, 19, 16)
    instr_7 = bit_at(instr, 7)
    if instr_23_21 == 0b000 and op2 == 0b0000:
        # Logical Shift Left
        return LslRegisterT2
    elif instr_23_21 == 0b001 and op2 == 0b0000:
        # Logical Shift Right
        return LsrRegisterT2
    elif instr_23_21 == 0b010 and op2 == 0b0000:
        # Arithmetic Shift Right
        return AsrRegisterT2
    elif instr_23_21 == 0b011 and op2 == 0b0000:
        # Rotate Right
        return RorRegisterT2
    elif op1 == 0b0000 and instr_7 and rn != 0b1111:
        # Signed Extend and Add Halfword
        return SxtahT1
    elif op1 == 0b0000 and instr_7 and rn == 0b1111:
        # Signed Extend Halfword
        return SxthT2
    elif op1 == 0b0001 and instr_7 and rn != 0b1111:
        # Unsigned Extend and Add Halfword
        return UxtahT1
    elif op1 == 0b0001 and instr_7 and rn == 0b1111:
        # Unsigned Extend Halfword
        return UxthT2
    elif op1 == 0b0010 and instr_7 and rn != 0b1111:
        # Signed Extend and Add Byte 16-bit
        return Sxtab16T1
    elif op1 == 0b0010 and instr_7 and rn == 0b1111:
        # Signed Extend Byte 16-bit
        return Sxtb16T1
    elif op1 == 0b0011 and instr_7 and rn != 0b1111:
        # Unsigned Extend and Add Byte 16-bit
        return Uxtab16T1
    elif op1 == 0b0011 and instr_7 and rn == 0b1111:
        # Unsigned Extend Byte 16-bit
        return Uxtb16T1
    elif op1 == 0b0100 and instr_7 and rn != 0b1111:
        # Signed Extend and Add Byte
        return SxtabT1
    elif op1 == 0b0100 and instr_7 and rn == 0b1111:
        # Signed Extend Byte
        return SxtbT2
    elif op1 == 0b0101 and instr_7 and rn != 0b1111:
        # Unsigned Extend and Add Byte
        return UxtabT1
    elif op1 == 0b0101 and instr_7 and rn == 0b1111:
        # Unsigned Extend Byte
        return UxtbT2
    elif bit_at(instr, 23) and substring(instr, 7, 6) == 0b00:
        # Parallel addition and subtraction, signed
        return thumb_parallel_addition_and_subtraction_signed.decode_instruction(instr)
    elif bit_at(instr, 23) and substring(instr, 7, 6) == 0b01:
        # Parallel addition and subtraction, unsigned
        return thumb_parallel_addition_and_subtraction_unsigned.decode_instruction(instr)
    elif substring(instr, 23, 22) == 0b10 and substring(instr, 7, 6) == 0b10:
        # Miscellaneous operations
        return thumb_miscellaneous_operations.decode_instruction(instr)
