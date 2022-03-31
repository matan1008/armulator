from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.opcodes.concrete.mla_t1 import MlaT1
from armulator.armv6.opcodes.concrete.mls_t1 import MlsT1
from armulator.armv6.opcodes.concrete.mul_t2 import MulT2
from armulator.armv6.opcodes.concrete.smla_t1 import SmlaT1
from armulator.armv6.opcodes.concrete.smlad_t1 import SmladT1
from armulator.armv6.opcodes.concrete.smlaw_t1 import SmlawT1
from armulator.armv6.opcodes.concrete.smlsd_t1 import SmlsdT1
from armulator.armv6.opcodes.concrete.smmla_t1 import SmmlaT1
from armulator.armv6.opcodes.concrete.smmls_t1 import SmmlsT1
from armulator.armv6.opcodes.concrete.smmul_t1 import SmmulT1
from armulator.armv6.opcodes.concrete.smuad_t1 import SmuadT1
from armulator.armv6.opcodes.concrete.smul_t1 import SmulT1
from armulator.armv6.opcodes.concrete.smulw_t1 import SmulwT1
from armulator.armv6.opcodes.concrete.smusd_t1 import SmusdT1
from armulator.armv6.opcodes.concrete.usad8_t1 import Usad8T1
from armulator.armv6.opcodes.concrete.usada8_t1 import Usada8T1


def decode_instruction(instr):
    if substring(instr, 22, 20) == 0b000 and substring(instr, 5, 4) == 0b00 and substring(instr, 15, 12) != 0b1111:
        # Multiply Accumulate
        return MlaT1
    elif substring(instr, 22, 20) == 0b000 and substring(instr, 5, 4) == 0b00 and substring(instr, 15, 12) == 0b1111:
        # Multiply Accumulate
        return MulT2
    elif substring(instr, 22, 20) == 0b000 and substring(instr, 5, 4) == 0b01:
        # Multiply and Subtract
        return MlsT1
    elif substring(instr, 22, 20) == 0b001 and substring(instr, 15, 12) != 0b1111:
        # Signed Multiply Accumulate (Halfwords)
        return SmlaT1
    elif substring(instr, 22, 20) == 0b001 and substring(instr, 15, 12) == 0b1111:
        # Signed Multiply (Halfwords)
        return SmulT1
    elif substring(instr, 22, 20) == 0b010 and not bit_at(instr, 5) and substring(instr, 15, 12) != 0b1111:
        # Signed Multiply Accumulate Dual
        return SmladT1
    elif substring(instr, 22, 20) == 0b010 and not bit_at(instr, 5) and substring(instr, 15, 12) == 0b1111:
        # Signed Dual Multiply Add
        return SmuadT1
    elif substring(instr, 22, 20) == 0b011 and not bit_at(instr, 5) and substring(instr, 15, 12) != 0b1111:
        # Signed Multiply Accumulate (Word by halfword)
        return SmlawT1
    elif substring(instr, 22, 20) == 0b011 and not bit_at(instr, 5) and substring(instr, 15, 12) == 0b1111:
        # Signed Multiply (Word by halfword)
        return SmulwT1
    elif substring(instr, 22, 20) == 0b100 and not bit_at(instr, 5) and substring(instr, 15, 12) != 0b1111:
        # Signed Multiply Subtract Dual
        return SmlsdT1
    elif substring(instr, 22, 20) == 0b100 and not bit_at(instr, 5) and substring(instr, 15, 12) == 0b1111:
        # Signed Dual Multiply Subtract
        return SmusdT1
    elif substring(instr, 22, 20) == 0b101 and not bit_at(instr, 5) and substring(instr, 15, 12) != 0b1111:
        # Signed Most Significant Word Multiply Accumulate
        return SmmlaT1
    elif substring(instr, 22, 20) == 0b101 and not bit_at(instr, 5) and substring(instr, 15, 12) == 0b1111:
        # Signed Most Significant Word Multiply
        return SmmulT1
    elif substring(instr, 22, 20) == 0b110 and not bit_at(instr, 5):
        # Signed Most Significant Word Multiply Subtract
        return SmmlsT1
    elif substring(instr, 22, 20) == 0b111 and substring(instr, 5, 4) == 0b00 and substring(instr, 15, 12) != 0b1111:
        # Unsigned Sum of Absolute Differences, Accumulate
        return Usada8T1
    elif substring(instr, 22, 20) == 0b111 and substring(instr, 5, 4) == 0b00 and substring(instr, 15, 12) == 0b1111:
        # Unsigned Sum of Absolute Differences
        return Usad8T1
