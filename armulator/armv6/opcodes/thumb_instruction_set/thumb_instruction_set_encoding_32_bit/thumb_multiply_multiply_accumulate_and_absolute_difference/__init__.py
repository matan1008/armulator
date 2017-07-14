from mla_t1 import MlaT1
from mul_t2 import MulT2
from mls_t1 import MlsT1
from smla_t1 import SmlaT1
from smul_t1 import SmulT1
from smlad_t1 import SmladT1
from smuad_t1 import SmuadT1
from smlaw_t1 import SmlawT1
from smulw_t1 import SmulwT1
from smlsd_t1 import SmlsdT1
from smusd_t1 import SmusdT1
from smmla_t1 import SmmlaT1
from smmul_t1 import SmmulT1
from smmls_t1 import SmmlsT1
from usada8_t1 import Usada8T1
from usad8_t1 import Usad8T1


def decode_instruction(instr):
    if instr[9:12] == "0b000" and instr[26:28] == "0b00" and instr[16:20] != "0b1111":
        # Multiply Accumulate
        return MlaT1
    elif instr[9:12] == "0b000" and instr[26:28] == "0b00" and instr[16:20] == "0b1111":
        # Multiply Accumulate
        return MulT2
    elif instr[9:12] == "0b000" and instr[26:28] == "0b01":
        # Multiply and Subtract
        return MlsT1
    elif instr[9:12] == "0b001" and instr[16:20] != "0b1111":
        # Signed Multiply Accumulate (Halfwords)
        return SmlaT1
    elif instr[9:12] == "0b001" and instr[16:20] == "0b1111":
        # Signed Multiply (Halfwords)
        return SmulT1
    elif instr[9:12] == "0b010" and not instr[26] and instr[16:20] != "0b1111":
        # Signed Multiply Accumulate Dual
        return SmladT1
    elif instr[9:12] == "0b010" and not instr[26] and instr[16:20] == "0b1111":
        # Signed Dual Multiply Add
        return SmuadT1
    elif instr[9:12] == "0b011" and not instr[26] and instr[16:20] != "0b1111":
        # Signed Multiply Accumulate (Word by halfword)
        return SmlawT1
    elif instr[9:12] == "0b011" and not instr[26] and instr[16:20] == "0b1111":
        # Signed Multiply (Word by halfword)
        return SmulwT1
    elif instr[9:12] == "0b100" and not instr[26] and instr[16:20] != "0b1111":
        # Signed Multiply Subtract Dual
        return SmlsdT1
    elif instr[9:12] == "0b100" and not instr[26] and instr[16:20] == "0b1111":
        # Signed Dual Multiply Subtract
        return SmusdT1
    elif instr[9:12] == "0b101" and not instr[26] and instr[16:20] != "0b1111":
        # Signed Most Significant Word Multiply Accumulate
        return SmmlaT1
    elif instr[9:12] == "0b101" and not instr[26] and instr[16:20] == "0b1111":
        # Signed Most Significant Word Multiply
        return SmmulT1
    elif instr[9:12] == "0b110" and not instr[26]:
        # Signed Most Significant Word Multiply Subtract
        return SmmlsT1
    elif instr[9:12] == "0b111" and instr[26:28] == "0b00" and instr[16:20] != "0b1111":
        # Unsigned Sum of Absolute Differences, Accumulate
        return Usada8T1
    elif instr[9:12] == "0b111" and instr[26:28] == "0b00" and instr[16:20] == "0b1111":
        # Unsigned Sum of Absolute Differences
        return Usad8T1
