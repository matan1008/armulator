from __future__ import absolute_import
from .lsl_register_t2 import LslRegisterT2
from .lsr_register_t2 import LsrRegisterT2
from .asr_register_t2 import AsrRegisterT2
from .ror_register_t2 import RorRegisterT2
from .sxtah_t1 import SxtahT1
from .sxth_t2 import SxthT2
from .uxtah_t1 import UxtahT1
from .uxth_t2 import UxthT2
from .sxtab16_t1 import Sxtab16T1
from .sxtb16_t1 import Sxtb16T1
from .uxtab16_t1 import Uxtab16T1
from .uxtb16_t1 import Uxtb16T1
from .sxtab_t1 import SxtabT1
from .sxtb_t2 import SxtbT2
from .uxtab_t1 import UxtabT1
from .uxtb_t2 import UxtbT2
from . import thumb_parallel_addition_and_subtraction_signed
from . import thumb_parallel_addition_and_subtraction_unsigned
from . import thumb_miscellaneous_operations


def decode_instruction(instr):
    if instr[8:11] == "0b000" and instr[24:28] == "0b0000":
        # Logical Shift Left
        return LslRegisterT2
    elif instr[8:11] == "0b001" and instr[24:28] == "0b0000":
        # Logical Shift Right
        return LsrRegisterT2
    elif instr[8:11] == "0b010" and instr[24:28] == "0b0000":
        # Arithmetic Shift Right
        return AsrRegisterT2
    elif instr[8:11] == "0b011" and instr[24:28] == "0b0000":
        # Rotate Right
        return RorRegisterT2
    elif instr[8:12] == "0b0000" and instr[24] and instr[12:16] != "0b1111":
        # Signed Extend and Add Halfword
        return SxtahT1
    elif instr[8:12] == "0b0000" and instr[24] and instr[12:16] == "0b1111":
        # Signed Extend Halfword
        return SxthT2
    elif instr[8:12] == "0b0001" and instr[24] and instr[12:16] != "0b1111":
        # Unsigned Extend and Add Halfword
        return UxtahT1
    elif instr[8:12] == "0b0001" and instr[24] and instr[12:16] == "0b1111":
        # Unsigned Extend Halfword
        return UxthT2
    elif instr[8:12] == "0b0010" and instr[24] and instr[12:16] != "0b1111":
        # Signed Extend and Add Byte 16-bit
        return Sxtab16T1
    elif instr[8:12] == "0b0010" and instr[24] and instr[12:16] == "0b1111":
        # Signed Extend Byte 16-bit
        return Sxtb16T1
    elif instr[8:12] == "0b0011" and instr[24] and instr[12:16] != "0b1111":
        # Unsigned Extend and Add Byte 16-bit
        return Uxtab16T1
    elif instr[8:12] == "0b0011" and instr[24] and instr[12:16] == "0b1111":
        # Unsigned Extend Byte 16-bit
        return Uxtb16T1
    elif instr[8:12] == "0b0100" and instr[24] and instr[12:16] != "0b1111":
        # Signed Extend and Add Byte
        return SxtabT1
    elif instr[8:12] == "0b0100" and instr[24] and instr[12:16] == "0b1111":
        # Signed Extend Byte
        return SxtbT2
    elif instr[8:12] == "0b0101" and instr[24] and instr[12:16] != "0b1111":
        # Unsigned Extend and Add Byte
        return UxtabT1
    elif instr[8:12] == "0b0101" and instr[24] and instr[12:16] == "0b1111":
        # Unsigned Extend Byte
        return UxtbT2
    elif instr[8] and instr[24:26] == "0b00":
        # Parallel addition and subtraction, signed
        return thumb_parallel_addition_and_subtraction_signed.decode_instruction(instr)
    elif instr[8] and instr[24:26] == "0b01":
        # Parallel addition and subtraction, unsigned
        return thumb_parallel_addition_and_subtraction_unsigned.decode_instruction(instr)
    elif instr[8:10] == "0b01" and instr[24:26] == "0b01":
        # Miscellaneous operations
        return thumb_miscellaneous_operations.decode_instruction(instr)
