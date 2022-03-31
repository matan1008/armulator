from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.concrete.sdiv_a1 import SdivA1
from armulator.armv6.opcodes.concrete.smlad_a1 import SmladA1
from armulator.armv6.opcodes.concrete.smlald_a1 import SmlaldA1
from armulator.armv6.opcodes.concrete.smlsd_a1 import SmlsdA1
from armulator.armv6.opcodes.concrete.smlsld_a1 import SmlsldA1
from armulator.armv6.opcodes.concrete.smmla_a1 import SmmlaA1
from armulator.armv6.opcodes.concrete.smmls_a1 import SmmlsA1
from armulator.armv6.opcodes.concrete.smmul_a1 import SmmulA1
from armulator.armv6.opcodes.concrete.smuad_a1 import SmuadA1
from armulator.armv6.opcodes.concrete.smusd_a1 import SmusdA1
from armulator.armv6.opcodes.concrete.udiv_a1 import UdivA1


def decode_instruction(instr):
    op1 = substring(instr, 22, 20)
    a = substring(instr, 15, 12)
    instr_7_6 = substring(instr, 7, 6)
    op2 = substring(instr, 7, 5)
    if op1 == 0b000 and instr_7_6 == 0b00 and a != 0b1111:
        # Signed Multiply Accumulate Dual
        return SmladA1
    elif op1 == 0b000 and instr_7_6 == 0b00 and a == 0b1111:
        # Signed Dual Multiply Add
        return SmuadA1
    elif op1 == 0b000 and instr_7_6 == 0b01 and a != 0b1111:
        # Signed Multiply Subtract Dual
        return SmlsdA1
    elif op1 == 0b000 and instr_7_6 == 0b01 and a == 0b1111:
        # Signed Dual Multiply Subtract
        return SmusdA1
    elif op1 == 0b001 and op2 == 0b000:
        # Signed Divide
        return SdivA1
    elif op1 == 0b011 and op2 == 0b000:
        # Unsigned Divide
        return UdivA1
    elif op1 == 0b100 and instr_7_6 == 0b00:
        # Signed Multiply Accumulate Long Dual
        return SmlaldA1
    elif op1 == 0b100 and instr_7_6 == 0b01:
        # Signed Multiply Subtract Long Dual
        return SmlsldA1
    elif op1 == 0b101 and instr_7_6 == 0b00 and a != 0b1111:
        # Signed Most Significant Word Multiply Accumulate
        return SmmlaA1
    elif op1 == 0b101 and instr_7_6 == 0b00 and a == 0b1111:
        # Signed Most Significant Word Multiply
        return SmmulA1
    elif op1 == 0b101 and instr_7_6 == 0b11:
        # Signed Most Significant Word Multiply Subtract
        return SmmlsA1
