import arm_parallel_addition_and_subtraction_signed
import arm_parallel_addition_and_subtraction_unsigned
import arm_packing_unpacking_saturation_and_reversal
import arm_signed_multiply_signed_and_unsigned_divide
from usad8_a1 import Usad8A1
from usada8_a1 import Usada8A1
from sbfx_a1 import SbfxA1
from bfc_a1 import BfcA1
from bfi_a1 import BfiA1
from ubfx_a1 import UbfxA1
from udf_a1 import UdfA1


def decode_instruction(instr):
    if instr[7:10] == "0b000":
        # Parallel addition and subtraction, signed
        return arm_parallel_addition_and_subtraction_signed.decode_instruction(instr)
    elif instr[7:10] == "0b001":
        # Parallel addition and subtraction, unsigned
        return arm_parallel_addition_and_subtraction_unsigned.decode_instruction(instr)
    elif instr[7:9] == "0b01":
        # Packing, unpacking, saturation, and reversal
        return arm_packing_unpacking_saturation_and_reversal.decode_instruction(instr)
    elif instr[7:9] == "0b10":
        # Signed multiply, signed and unsigned divide
        return arm_signed_multiply_signed_and_unsigned_divide.decode_instruction(instr)
    elif instr[7:12] == "0b11000" and instr[24:27] == "0b000" and instr[16:20] == "0b1111":
        # Unsigned Sum of Absolute Differences
        return Usad8A1
    elif instr[7:12] == "0b11000" and instr[24:27] == "0b000" and instr[16:20] != "0b1111":
        # Unsigned Sum of Absolute Differences and Accumulate
        return Usada8A1
    elif instr[7:11] == "0b1101" and instr[25:27] == "0b10":
        # Signed Bit Field Extract
        return SbfxA1
    elif instr[7:11] == "0b1110" and instr[25:27] == "0b00" and instr[28:32] == "0b1111":
        # Bit Field Clear
        return BfcA1
    elif instr[7:11] == "0b1110" and instr[25:27] == "0b00" and instr[28:32] != "0b1111":
        # Bit Field Insert
        return BfiA1
    elif instr[7:11] == "0b1111" and instr[25:27] == "0b10":
        # Unsigned Bit Field Extract
        return UbfxA1
    elif instr[7:12] == "0b11111" and instr[24:27] == "0b111" and instr[0:4] == "0b1110":
        # Permanently UNDEFINED
        return UdfA1
