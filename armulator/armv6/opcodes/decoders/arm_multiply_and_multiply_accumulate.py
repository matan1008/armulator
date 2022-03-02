from armulator.armv6.arm_exceptions import UndefinedInstructionException
from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.concrete.mla_a1 import MlaA1
from armulator.armv6.opcodes.concrete.mls_a1 import MlsA1
from armulator.armv6.opcodes.concrete.mul_a1 import MulA1
from armulator.armv6.opcodes.concrete.smlal_a1 import SmlalA1
from armulator.armv6.opcodes.concrete.smull_a1 import SmullA1
from armulator.armv6.opcodes.concrete.umaal_a1 import UmaalA1
from armulator.armv6.opcodes.concrete.umlal_a1 import UmlalA1
from armulator.armv6.opcodes.concrete.umull_a1 import UmullA1


def decode_instruction(instr):
    op = substring(instr, 23, 20)
    instr_23_21 = substring(instr, 23, 21)
    if instr_23_21 == 0b000:
        # Multiply
        return MulA1
    elif instr_23_21 == 0b001:
        # Multiply Accumulate
        return MlaA1
    elif op == 0b0100:
        # Unsigned Multiply Accumulate Accumulate Long
        return UmaalA1
    elif op == 0b0101:
        raise UndefinedInstructionException()
    elif op == 0b0110:
        # Multiply and Subtract
        return MlsA1
    elif op == 0b0111:
        raise UndefinedInstructionException()
    elif instr_23_21 == 0b100:
        # Unsigned Multiply Long
        return UmullA1
    elif instr_23_21 == 0b101:
        # Unsigned Multiply Accumulate Long
        return UmlalA1
    elif instr_23_21 == 0b110:
        # Signed Multiply Long
        return SmullA1
    elif instr_23_21 == 0b111:
        # Signed Multiply Accumulate Long
        return SmlalA1
