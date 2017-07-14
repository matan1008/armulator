from armulator.armv6.arm_exceptions import UndefinedInstructionException
from mul_a1 import MulA1
from mla_a1 import MlaA1
from umaal_a1 import UmaalA1
from mls_a1 import MlsA1
from umull_a1 import UmullA1
from umlal_a1 import UmlalA1
from smull_a1 import SmullA1
from smlal_a1 import SmlalA1


def decode_instruction(instr):
    if instr[8:11] == "0b000":
        # Multiply
        return MulA1
    elif instr[8:11] == "0b001":
        # Multiply Accumulate
        return MlaA1
    elif instr[8:12] == "0b0100":
        # Unsigned Multiply Accumulate Accumulate Long
        return UmaalA1
    elif instr[8:12] == "0b0101":
        raise UndefinedInstructionException()
    elif instr[8:12] == "0b0110":
        # Multiply and Subtract
        return MlsA1
    elif instr[8:12] == "0b0111":
        raise UndefinedInstructionException()
    elif instr[8:11] == "0b100":
        # Unsigned Multiply Long
        return UmullA1
    elif instr[8:11] == "0b101":
        # Unsigned Multiply Accumulate Long
        return UmlalA1
    elif instr[8:11] == "0b110":
        # Signed Multiply Long
        return SmullA1
    elif instr[8:11] == "0b111":
        # Signed Multiply Accumulate Long
        return SmlalA1
