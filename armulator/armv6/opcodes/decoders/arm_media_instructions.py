from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.concrete.bfc_a1 import BfcA1
from armulator.armv6.opcodes.concrete.bfi_a1 import BfiA1
from armulator.armv6.opcodes.concrete.sbfx_a1 import SbfxA1
from armulator.armv6.opcodes.concrete.ubfx_a1 import UbfxA1
from armulator.armv6.opcodes.concrete.udf_a1 import UdfA1
from armulator.armv6.opcodes.concrete.usad8_a1 import Usad8A1
from armulator.armv6.opcodes.concrete.usada8_a1 import Usada8A1
from armulator.armv6.opcodes.decoders import arm_packing_unpacking_saturation_and_reversal
from armulator.armv6.opcodes.decoders import arm_parallel_addition_and_subtraction_signed
from armulator.armv6.opcodes.decoders import arm_parallel_addition_and_subtraction_unsigned
from armulator.armv6.opcodes.decoders import arm_signed_multiply_signed_and_unsigned_divide


def decode_instruction(instr):
    instr_24_22 = substring(instr, 24, 22)
    instr_24_23 = substring(instr, 24, 23)
    op1 = substring(instr, 24, 20)
    op2 = substring(instr, 7, 5)
    rd = substring(instr, 15, 12)
    rn = substring(instr, 3, 0)
    instr_24_21 = substring(instr, 24, 21)
    instr_6_5 = substring(instr, 6, 5)
    if instr_24_22 == 0b000:
        # Parallel addition and subtraction, signed
        return arm_parallel_addition_and_subtraction_signed.decode_instruction(instr)
    elif instr_24_22 == 0b001:
        # Parallel addition and subtraction, unsigned
        return arm_parallel_addition_and_subtraction_unsigned.decode_instruction(instr)
    elif instr_24_23 == 0b01:
        # Packing, unpacking, saturation, and reversal
        return arm_packing_unpacking_saturation_and_reversal.decode_instruction(instr)
    elif instr_24_23 == 0b10:
        # Signed multiply, signed and unsigned divide
        return arm_signed_multiply_signed_and_unsigned_divide.decode_instruction(instr)
    elif op1 == 0b11000 and op2 == 0b000 and rd == 0b1111:
        # Unsigned Sum of Absolute Differences
        return Usad8A1
    elif op1 == 0b11000 and op2 == 0b000 and rd != 0b1111:
        # Unsigned Sum of Absolute Differences and Accumulate
        return Usada8A1
    elif instr_24_21 == 0b1101 and instr_6_5 == 0b10:
        # Signed Bit Field Extract
        return SbfxA1
    elif instr_24_21 == 0b1110 and instr_6_5 == 0b00 and rn == 0b1111:
        # Bit Field Clear
        return BfcA1
    elif instr_24_21 == 0b1110 and instr_6_5 == 0b00 and rn != 0b1111:
        # Bit Field Insert
        return BfiA1
    elif instr_24_21 == 0b1111 and instr_6_5 == 0b10:
        # Unsigned Bit Field Extract
        return UbfxA1
    elif op1 == 0b11111 and op2 == 0b111 and substring(instr, 31, 28) == 0b1110:
        # Permanently UNDEFINED
        return UdfA1
