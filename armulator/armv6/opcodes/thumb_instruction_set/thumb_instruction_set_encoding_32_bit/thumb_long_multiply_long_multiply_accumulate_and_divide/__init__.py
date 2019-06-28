from __future__ import absolute_import
from .smull_t1 import SmullT1
from .sdiv_t1 import SdivT1
from .umull_t1 import UmullT1
from .udiv_t1 import UdivT1
from .smlal_t1 import SmlalT1
from .smlalxy_t1 import SmlalxyT1
from .smlald_t1 import SmlaldT1
from .smlsld_t1 import SmlsldT1
from .umlal_t1 import UmlalT1
from .umaal_t1 import UmaalT1


def decode_instruction(instr):
    if instr[9:12] == "0b000" and instr[24:28] == "0b0000":
        # Signed Multiply Long
        return SmullT1
    elif instr[9:12] == "0b001" and instr[24:28] == "0b1111":
        # Signed Divide
        return SdivT1
    elif instr[9:12] == "0b010" and instr[24:28] == "0b0000":
        # Unsigned Multiply Long
        return UmullT1
    elif instr[9:12] == "0b011" and instr[24:28] == "0b1111":
        # Unsigned Divide
        return UdivT1
    elif instr[9:12] == "0b100" and instr[24:28] == "0b0000":
        # Signed Multiply Accumulate Long
        return SmlalT1
    elif instr[9:12] == "0b100" and instr[24:26] == "0b10":
        # Signed Multiply Accumulate Long (Halfwords)
        return SmlalxyT1
    elif instr[9:12] == "0b100" and instr[24:27] == "0b110":
        # Signed Multiply Accumulate Long Dual
        return SmlaldT1
    elif instr[9:12] == "0b101" and instr[24:27] == "0b110":
        # Signed Multiply Subtract Long Dual
        return SmlsldT1
    elif instr[9:12] == "0b110" and instr[24:28] == "0b0000":
        # Unsigned Multiply Accumulate Long
        return UmlalT1
    elif instr[9:12] == "0b110" and instr[24:28] == "0b0110":
        # Unsigned Multiply Accumulate Accumulate Long
        return UmaalT1
