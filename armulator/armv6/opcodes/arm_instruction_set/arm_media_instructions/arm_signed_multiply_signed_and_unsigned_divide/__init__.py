from __future__ import absolute_import
from .smlad_a1 import SmladA1
from .smuad_a1 import SmuadA1
from .smlsd_a1 import SmlsdA1
from .smusd_a1 import SmusdA1
from .sdiv_a1 import SdivA1
from .udiv_a1 import UdivA1
from .smlald_a1 import SmlaldA1
from .smlsld_a1 import SmlsldA1
from .smmla_a1 import SmmlaA1
from .smmul_a1 import SmmulA1
from .smmls_a1 import SmmlsA1


def decode_instruction(instr):
    if instr[9:12] == "0b000" and instr[24:26] == "0b00" and instr[16:20] != "0b1111":
        # Signed Multiply Accumulate Dual
        return SmladA1
    elif instr[9:12] == "0b000" and instr[24:26] == "0b00" and instr[16:20] == "0b1111":
        # Signed Dual Multiply Add
        return SmuadA1
    elif instr[9:12] == "0b000" and instr[24:26] == "0b01" and instr[16:20] != "0b1111":
        # Signed Multiply Subtract Dual
        return SmlsdA1
    elif instr[9:12] == "0b000" and instr[24:26] == "0b01" and instr[16:20] == "0b1111":
        # Signed Dual Multiply Subtract
        return SmusdA1
    elif instr[9:12] == "0b001" and instr[24:27] == "0b000":
        # Signed Divide
        return SdivA1
    elif instr[9:12] == "0b011" and instr[24:27] == "0b000":
        # Unsigned Divide
        return UdivA1
    elif instr[9:12] == "0b100" and instr[24:26] == "0b00":
        # Signed Multiply Accumulate Long Dual
        return SmlaldA1
    elif instr[9:12] == "0b100" and instr[24:26] == "0b01":
        # Signed Multiply Subtract Long Dual
        return SmlsldA1
    elif instr[9:12] == "0b101" and instr[24:26] == "0b00" and instr[16:20] != "0b1111":
        # Signed Most Significant Word Multiply Accumulate
        return SmmlaA1
    elif instr[9:12] == "0b101" and instr[24:26] == "0b00" and instr[16:20] == "0b1111":
        # Signed Most Significant Word Multiply
        return SmmulA1
    elif instr[9:12] == "0b101" and instr[24:26] == "0b11":
        # Signed Most Significant Word Multiply Subtract
        return SmmlsA1
